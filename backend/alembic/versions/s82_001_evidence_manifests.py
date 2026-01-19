"""Sprint 82: Evidence Manifest Tables - Tamper-Evident Hash Chain

Revision ID: s82_001_evidence_manifests
Revises: s80_agents_md_tables
Create Date: 2026-01-19 20:00:00.000000

Sprint 82 P0 Launch Blocker - Evidence Hash Chain v1

Implements tamper-evident Evidence Vault per CTO Pre-Launch Hardening Plan:
- evidence_manifests: Hash chain with HMAC-SHA256 signatures
- evidence_manifest_verifications: Verification audit log

Go/No-Go Criteria (Feb 28, 2026):
- Evidence hash chain: Tamper-evident test pass ✅

Design:
1. Each manifest includes SHA256 of its content
2. Each manifest links to previous via previous_manifest_hash
3. Each manifest is signed with HMAC-SHA256 (server secret)
4. Append-only design (never update/delete)
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers, used by Alembic.
revision = 's82_001_evidence_manifests'
down_revision = 's80_agents_md_tables'
branch_labels = None
depends_on = None


def upgrade():
    # =========================================================================
    # Table 1: evidence_manifests
    # Tamper-evident manifest with hash chain linking
    # =========================================================================
    op.create_table(
        'evidence_manifests',
        # Primary Key
        sa.Column(
            'id',
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text('gen_random_uuid()'),
        ),

        # Project relationship
        sa.Column(
            'project_id',
            UUID(as_uuid=True),
            sa.ForeignKey('projects.id', ondelete='CASCADE'),
            nullable=False,
        ),

        # Sequence number within project (for deterministic ordering)
        sa.Column(
            'sequence_number',
            sa.BigInteger,
            nullable=False,
        ),

        # Hash Chain
        sa.Column(
            'manifest_hash',
            sa.String(64),
            nullable=False,
            unique=True,
            comment='SHA256 of manifest content',
        ),
        sa.Column(
            'previous_manifest_hash',
            sa.String(64),
            nullable=True,
            comment='Hash of previous manifest (NULL for genesis)',
        ),

        # Artifacts array (JSONB)
        # Schema: [{artifact_id, sha256, path, size, file_name, evidence_type, uploaded_at}]
        sa.Column(
            'artifacts',
            JSONB,
            nullable=False,
            server_default='[]',
            comment='Array of artifact entries with hashes',
        ),

        # HMAC-SHA256 signature
        sa.Column(
            'signature',
            sa.String(64),
            nullable=False,
            comment='HMAC-SHA256 signature for tamper detection',
        ),

        # Genesis flag
        sa.Column(
            'is_genesis',
            sa.Boolean,
            nullable=False,
            server_default='false',
            comment='True if first manifest in project chain',
        ),

        # Audit timestamps
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('NOW()'),
            nullable=False,
        ),

        # Created by user
        sa.Column(
            'created_by',
            UUID(as_uuid=True),
            sa.ForeignKey('users.id', ondelete='SET NULL'),
            nullable=True,
        ),
    )

    # Indexes for evidence_manifests
    op.create_index(
        'idx_evidence_manifests_project_id',
        'evidence_manifests',
        ['project_id'],
    )
    op.create_index(
        'idx_evidence_manifests_hash',
        'evidence_manifests',
        ['manifest_hash'],
    )
    op.create_index(
        'idx_evidence_manifests_previous_hash',
        'evidence_manifests',
        ['previous_manifest_hash'],
    )
    op.create_index(
        'idx_evidence_manifests_created_at',
        'evidence_manifests',
        [sa.text('created_at DESC')],
    )
    op.create_index(
        'idx_evidence_manifests_created_by',
        'evidence_manifests',
        ['created_by'],
    )

    # Unique constraint: sequence number per project
    op.create_index(
        'uq_evidence_manifests_project_sequence',
        'evidence_manifests',
        ['project_id', 'sequence_number'],
        unique=True,
    )

    # Constraint: Genesis manifests must have NULL previous_hash
    op.create_check_constraint(
        'chk_genesis_previous_hash',
        'evidence_manifests',
        """
        (is_genesis = true AND previous_manifest_hash IS NULL)
        OR
        (is_genesis = false AND previous_manifest_hash IS NOT NULL)
        """,
    )

    # =========================================================================
    # Table 2: evidence_manifest_verifications
    # Verification audit log for compliance
    # =========================================================================
    op.create_table(
        'evidence_manifest_verifications',
        # Primary Key
        sa.Column(
            'id',
            UUID(as_uuid=True),
            primary_key=True,
            server_default=sa.text('gen_random_uuid()'),
        ),

        # Project being verified
        sa.Column(
            'project_id',
            UUID(as_uuid=True),
            sa.ForeignKey('projects.id', ondelete='CASCADE'),
            nullable=False,
        ),

        # Verification results
        sa.Column(
            'verified_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('NOW()'),
            nullable=False,
        ),
        sa.Column(
            'manifests_checked',
            sa.BigInteger,
            nullable=False,
            server_default='0',
        ),
        sa.Column(
            'chain_valid',
            sa.Boolean,
            nullable=False,
        ),

        # Error details
        sa.Column(
            'first_broken_at',
            UUID(as_uuid=True),
            sa.ForeignKey('evidence_manifests.id', ondelete='SET NULL'),
            nullable=True,
        ),
        sa.Column(
            'error_message',
            sa.Text,
            nullable=True,
        ),

        # Verification metadata
        sa.Column(
            'verified_by',
            sa.String(100),
            nullable=False,
            comment="'system-cron', 'api-request', 'user-{id}'",
        ),
    )

    # Indexes for evidence_manifest_verifications
    op.create_index(
        'idx_manifest_verifications_project_id',
        'evidence_manifest_verifications',
        ['project_id'],
    )
    op.create_index(
        'idx_manifest_verifications_verified_at',
        'evidence_manifest_verifications',
        [sa.text('verified_at DESC')],
    )
    op.create_index(
        'idx_manifest_verifications_chain_valid',
        'evidence_manifest_verifications',
        ['chain_valid'],
    )

    # =========================================================================
    # View: v_latest_manifest_per_project
    # Quick lookup for latest manifest per project
    # =========================================================================
    op.execute("""
        CREATE OR REPLACE VIEW v_latest_manifest_per_project AS
        SELECT DISTINCT ON (project_id)
            id,
            project_id,
            sequence_number,
            manifest_hash,
            previous_manifest_hash,
            artifacts,
            signature,
            is_genesis,
            created_at,
            created_by
        FROM evidence_manifests
        ORDER BY project_id, sequence_number DESC;
    """)

    # =========================================================================
    # View: v_manifest_chain_status
    # Quick overview of chain status per project
    # =========================================================================
    op.execute("""
        CREATE OR REPLACE VIEW v_manifest_chain_status AS
        SELECT
            p.id AS project_id,
            p.name AS project_name,
            COUNT(em.id) AS total_manifests,
            MAX(em.sequence_number) AS latest_sequence,
            MAX(em.created_at) AS last_manifest_at,
            (
                SELECT chain_valid
                FROM evidence_manifest_verifications emv
                WHERE emv.project_id = p.id
                ORDER BY emv.verified_at DESC
                LIMIT 1
            ) AS last_verification_valid,
            (
                SELECT verified_at
                FROM evidence_manifest_verifications emv
                WHERE emv.project_id = p.id
                ORDER BY emv.verified_at DESC
                LIMIT 1
            ) AS last_verified_at
        FROM projects p
        LEFT JOIN evidence_manifests em ON em.project_id = p.id
        GROUP BY p.id, p.name;
    """)


def downgrade():
    # Drop views first
    op.execute("DROP VIEW IF EXISTS v_manifest_chain_status;")
    op.execute("DROP VIEW IF EXISTS v_latest_manifest_per_project;")

    # Drop tables
    op.drop_table('evidence_manifest_verifications')
    op.drop_table('evidence_manifests')

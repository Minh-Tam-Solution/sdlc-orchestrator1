"""Organization Invitation System - Sprint 146

Revision ID: s146_001
Revises: s136_001_add_gate_approvals
Create Date: 2026-02-03 10:00:00.000000

Changes:
- Create organization_invitations table with hash-based tokens
- Add indexes for performance (hash lookup, email search, expiry)
- Add audit trail fields (ip_address, user_agent)
- Add CTO mandatory conditions:
  * Role constraint (admin/member only)
  * Cleanup index for old invitations

Security:
- Token stored as SHA256 hash (never raw token)
- Unique constraint on pending invitations per org+email
- Rate limiting enforced in application layer

Reference: ADR-047-Organization-Invitation-System.md
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 's146_001'
down_revision = 's136_001_add_gate_approvals'
branch_labels = None
depends_on = None


def upgrade():
    """Create organization_invitations table and related objects"""

    # Reuse invitation_status enum (already created in s128_001)
    # No need to create it again

    # Create organization_invitations table
    op.create_table(
        'organization_invitations',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('organization_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('invited_email', sa.String(255), nullable=False),
        sa.Column('invitation_token_hash', sa.String(64), nullable=False, unique=True, comment='SHA256 hash of invitation token'),
        sa.Column('role', sa.String(20), nullable=False, server_default='member'),
        sa.Column('status', sa.String(20), nullable=False, server_default='pending'),
        sa.Column('invited_by', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('expires_at', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('accepted_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('declined_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),

        # Rate limiting (enforced in application, NOT DB constraint for flexibility)
        sa.Column('resend_count', sa.Integer, nullable=False, server_default='0', comment='Number of times invitation was resent'),
        sa.Column('last_resent_at', sa.TIMESTAMP(timezone=True), nullable=True),

        # Audit trail
        sa.Column('ip_address', postgresql.INET, nullable=True, comment='IP address of inviter'),
        sa.Column('user_agent', sa.Text, nullable=True, comment='User agent of inviter'),

        # Foreign keys
        sa.ForeignKeyConstraint(['organization_id'], ['organizations.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['invited_by'], ['users.id']),

        # Constraints
        sa.CheckConstraint('expires_at > created_at', name='org_invitation_valid_expiry'),
        # CTO MANDATORY CONDITION #1: Role validation constraint
        sa.CheckConstraint("role IN ('admin', 'member')", name='org_invitation_valid_role'),

        comment='Organization invitation system with hash-based tokens (ADR-047)'
    )

    # Create unique partial index for pending invitations
    # Allows multiple invitations to same email if previous ones are not pending
    op.execute("""
        CREATE UNIQUE INDEX idx_org_unique_pending_invitation
        ON organization_invitations(organization_id, invited_email)
        WHERE status = 'pending'
    """)

    # Create index for token hash lookup (most common query)
    op.create_index(
        'idx_org_invitation_hash',
        'organization_invitations',
        ['invitation_token_hash'],
        unique=True
    )

    # Create index for email lookup (admin searches invitations by email)
    op.create_index(
        'idx_org_invitation_email',
        'organization_invitations',
        ['organization_id', 'invited_email']
    )

    # Create index for status filter
    op.create_index(
        'idx_org_invitation_status',
        'organization_invitations',
        ['status']
    )

    # Create index for organization filter
    op.create_index(
        'idx_org_invitation_org_id',
        'organization_invitations',
        ['organization_id']
    )

    # Create index for expiry cleanup (background job)
    op.create_index(
        'idx_org_invitation_expiry',
        'organization_invitations',
        ['expires_at'],
        postgresql_where=sa.text("status = 'pending'")
    )

    # CTO MANDATORY CONDITION #2: Cleanup index for old invitations
    op.execute("""
        CREATE INDEX idx_org_invitation_cleanup
        ON organization_invitations(created_at)
        WHERE status IN ('accepted', 'declined', 'expired', 'cancelled')
    """)

    # Create index for invited_by (audit queries)
    op.create_index(
        'idx_org_invitation_invited_by',
        'organization_invitations',
        ['invited_by']
    )


def downgrade():
    """Drop organization_invitations table and related objects"""

    # Drop indexes first
    op.drop_index('idx_org_invitation_invited_by', table_name='organization_invitations')
    op.execute('DROP INDEX IF EXISTS idx_org_invitation_cleanup')
    op.drop_index('idx_org_invitation_expiry', table_name='organization_invitations')
    op.drop_index('idx_org_invitation_org_id', table_name='organization_invitations')
    op.drop_index('idx_org_invitation_status', table_name='organization_invitations')
    op.drop_index('idx_org_invitation_email', table_name='organization_invitations')
    op.drop_index('idx_org_invitation_hash', table_name='organization_invitations')
    op.execute('DROP INDEX IF EXISTS idx_org_unique_pending_invitation')

    # Drop table
    op.drop_table('organization_invitations')

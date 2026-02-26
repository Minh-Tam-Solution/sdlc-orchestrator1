"""Sprint 209: oauth_accounts OTT identity linking support.

Two changes required for OTT identity linking (ADR-068):
1. access_token nullable — OTT linking has no OAuth token, INSERT would fail
   with IntegrityError on NOT NULL constraint.
2. UniqueConstraint on (provider, provider_account_id) — prevents duplicate
   linking and enables ON CONFLICT upsert pattern.

Revision ID: s209_001
Revises: s207_001
Create Date: 2026-02-26
"""

import sqlalchemy as sa
from alembic import op

revision = "s209_001"
down_revision = "s207_001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Make access_token nullable (P0-1: OTT linking has no OAuth token)
    op.alter_column(
        "oauth_accounts",
        "access_token",
        existing_type=sa.String(512),
        nullable=True,
        server_default="",
    )

    # 2. Add UniqueConstraint on (provider, provider_account_id) (P1-1)
    # Check for duplicates first — dedup by keeping newest row per pair
    op.execute("""
        DELETE FROM oauth_accounts
        WHERE id NOT IN (
            SELECT DISTINCT ON (provider, provider_account_id) id
            FROM oauth_accounts
            ORDER BY provider, provider_account_id, created_at DESC
        )
    """)
    op.create_unique_constraint(
        "uq_oauth_provider_account",
        "oauth_accounts",
        ["provider", "provider_account_id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_oauth_provider_account",
        "oauth_accounts",
        type_="unique",
    )
    op.alter_column(
        "oauth_accounts",
        "access_token",
        existing_type=sa.String(512),
        nullable=False,
        server_default=None,
    )

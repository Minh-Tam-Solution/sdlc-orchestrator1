"""Fix api_keys prefix column size

Revision ID: t5o6p7q8r9s0
Revises: s4n5o6p7q8r9
Create Date: 2025-12-26 13:30:00.000000

Sprint: 52B - VS Code Extension Authentication
Issue: prefix column VARCHAR(20) was too small for "sdlc_live_xxxx..." format (~23 chars)
Fix: Increased to VARCHAR(30)

Note: This migration was already applied manually via:
    ALTER TABLE api_keys ALTER COLUMN prefix TYPE VARCHAR(30);
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 't5o6p7q8r9s0'
down_revision: Union[str, None] = 's4n5o6p7q8r9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Increase prefix column size from VARCHAR(20) to VARCHAR(30)."""
    # Note: Already applied manually, this documents the change
    op.alter_column(
        'api_keys',
        'prefix',
        existing_type=sa.VARCHAR(20),
        type_=sa.VARCHAR(30),
        existing_nullable=False
    )


def downgrade() -> None:
    """Revert prefix column size to VARCHAR(20)."""
    # Warning: This may truncate data if prefix values exceed 20 chars
    op.alter_column(
        'api_keys',
        'prefix',
        existing_type=sa.VARCHAR(30),
        type_=sa.VARCHAR(20),
        existing_nullable=False
    )

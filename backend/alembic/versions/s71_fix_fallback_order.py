"""
Fix AI fallback chain order: ollama → openai → claude

Revision ID: s71_fix_fallback_order
Revises: s70_ai_provider_settings
Create Date: 2026-01-16

Per CTO approval, the fallback order should be:
  1. ollama (primary - local, fast)
  2. openai (first fallback - more reliable API)
  3. claude (second fallback - highest quality)

This corrects the initial order which had claude before openai.
"""

from alembic import op

revision = 's71_fix_fallback_order'
down_revision = 's70_ai_provider_settings'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Update fallback chain to correct order."""
    op.execute("""
        UPDATE system_settings
        SET value = '["ollama", "openai", "claude"]',
            version = version + 1
        WHERE key = 'ai_fallback_chain';
    """)


def downgrade() -> None:
    """Revert to original order."""
    op.execute("""
        UPDATE system_settings
        SET value = '["ollama", "claude", "openai"]',
            version = version + 1
        WHERE key = 'ai_fallback_chain';
    """)

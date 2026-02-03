"""Sprint 147: Product Events Table for Telemetry

Creates the product_events table for the Product Truth Layer.
This table stores activation funnel events to replace the "82-85% realization"
narrative with measured metrics.

Sprint: 147 - Spring Cleaning
Priority: P0
Reference: Product Truth Layer Specification

Revision ID: s147_001
Revises: 2585fae1776a, s146_001
Create Date: 2026-02-04
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "s147_001"
down_revision: Union[str, None] = ("2585fae1776a", "s146_001")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create product_events table with optimized indexes for funnel queries."""
    op.create_table(
        "product_events",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False, server_default=sa.text("gen_random_uuid()")),
        sa.Column("event_name", sa.String(100), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("properties", postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
        sa.Column("session_id", sa.String(100), nullable=True),
        sa.Column("interface", sa.String(20), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("now()")),
        # Primary key
        sa.PrimaryKeyConstraint("id"),
        # Foreign keys
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"], ondelete="SET NULL"),
        # Check constraint for interface values
        sa.CheckConstraint(
            "interface IS NULL OR interface IN ('web', 'cli', 'extension', 'api')",
            name="ck_product_events_interface",
        ),
    )

    # Create optimized indexes for funnel queries
    # Index for user-based queries
    op.create_index(
        "idx_product_events_user_time",
        "product_events",
        ["user_id", "timestamp"],
    )

    # Index for project-based queries
    op.create_index(
        "idx_product_events_project_time",
        "product_events",
        ["project_id", "timestamp"],
    )

    # Index for event name queries
    op.create_index(
        "idx_product_events_name",
        "product_events",
        ["event_name", "timestamp"],
    )

    # Composite index for funnel analysis (user + event + time)
    op.create_index(
        "idx_product_events_funnel",
        "product_events",
        ["user_id", "event_name", "timestamp"],
    )

    # Index for session tracking
    op.create_index(
        "idx_product_events_session",
        "product_events",
        ["session_id"],
        postgresql_where=sa.text("session_id IS NOT NULL"),
    )

    # Index for interface breakdown queries
    op.create_index(
        "idx_product_events_interface",
        "product_events",
        ["interface", "timestamp"],
        postgresql_where=sa.text("interface IS NOT NULL"),
    )

    # Index for organization-based queries
    op.create_index(
        "idx_product_events_org_time",
        "product_events",
        ["organization_id", "timestamp"],
        postgresql_where=sa.text("organization_id IS NOT NULL"),
    )

    # Add table comment for documentation
    op.execute("""
        COMMENT ON TABLE product_events IS 'Product telemetry events for activation funnels and usage metrics. Sprint 147 - Product Truth Layer.';
    """)

    op.execute("""
        COMMENT ON COLUMN product_events.event_name IS 'Event name using snake_case past tense (e.g., user_signed_up, project_created)';
    """)

    op.execute("""
        COMMENT ON COLUMN product_events.interface IS 'Source interface: web, cli, extension, or api';
    """)


def downgrade() -> None:
    """Drop product_events table and all its indexes."""
    # Drop indexes first (they are dropped automatically with table, but explicit for clarity)
    op.drop_index("idx_product_events_org_time", table_name="product_events")
    op.drop_index("idx_product_events_interface", table_name="product_events")
    op.drop_index("idx_product_events_session", table_name="product_events")
    op.drop_index("idx_product_events_funnel", table_name="product_events")
    op.drop_index("idx_product_events_name", table_name="product_events")
    op.drop_index("idx_product_events_project_time", table_name="product_events")
    op.drop_index("idx_product_events_user_time", table_name="product_events")

    # Drop the table
    op.drop_table("product_events")

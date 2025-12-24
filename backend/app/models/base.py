"""
SQLAlchemy Base Model

Version: 1.0.0
Date: November 14, 2025
Status: ACTIVE - Week 3 Architecture Design
Authority: Backend Lead + CTO Approved
Foundation: Data Model v0.1 (9.8/10 quality)

Purpose:
- Base class for all SQLAlchemy models
- Common columns (created_at, updated_at, deleted_at)
- Declarative base configuration
"""

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all database models.

    Provides common columns and functionality:
    - created_at: Timestamp of record creation
    - updated_at: Timestamp of last update (auto-updates)
    - deleted_at: Soft delete timestamp (NULL = active record)

    Usage:
        class User(Base):
            __tablename__ = "users"
            user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
            ...
    """

    # Type checking configuration
    type_annotation_map = {
        datetime: DateTime(timezone=True),
    }

    # Abstract base (no table created)
    __abstract__ = True

    # Common audit columns
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Record creation timestamp (UTC)",
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
        comment="Last update timestamp (UTC, auto-updated)",
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
        comment="Soft delete timestamp (NULL = active)",
    )

    def __repr__(self) -> str:
        """
        String representation of model instance.

        Returns:
            str: Model name and primary key

        Example:
            User(user_id=123e4567-e89b-12d3-a456-426614174000)
        """
        # Get primary key column name and value
        pk_columns = [c.name for c in self.__table__.primary_key.columns]
        pk_values = [getattr(self, pk) for pk in pk_columns]
        pk_str = ", ".join(f"{k}={v}" for k, v in zip(pk_columns, pk_values))

        return f"{self.__class__.__name__}({pk_str})"

    def to_dict(self) -> dict[str, Any]:
        """
        Convert model instance to dictionary.

        Returns:
            dict: Model data as dictionary

        Example:
            user = User(email="john@example.com", full_name="John Doe")
            user.to_dict()
            # Returns: {"email": "john@example.com", "full_name": "John Doe", ...}
        """
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

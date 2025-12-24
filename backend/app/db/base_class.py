"""
=========================================================================
SQLAlchemy Base Class - Database ORM Foundation
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: November 28, 2025
Status: ACTIVE - Week 3 Architecture Design
Authority: Backend Lead + DBA + CTO Approved
Foundation: Data Model v0.1 (9.8/10 quality)
Framework: SDLC 4.9 Complete Lifecycle

Purpose:
- Base class for all SQLAlchemy models
- Common table configuration (schema, naming conventions)
- MetaData registry for Alembic migrations

Usage:
All database models inherit from this Base class:
    from app.db.base_class import Base

    class MyModel(Base):
        __tablename__ = "my_table"
        ...

Zero Mock Policy: Real SQLAlchemy declarative base
=========================================================================
"""

from sqlalchemy.ext.declarative import declarative_base

# Base class for all models
Base = declarative_base()

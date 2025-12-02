"""
SQLAlchemy Models - SDLC Orchestrator

Version: 1.0.0
Date: November 28, 2025
Status: ACTIVE - Week 3 Architecture Design
Authority: Backend Lead + CTO Approved
Foundation: Data Model v0.1 (21 tables, 9.8/10 quality)
Framework: SDLC 4.9 Complete Lifecycle

Database: PostgreSQL 15.5+
ORM: SQLAlchemy 2.0+
Migrations: Alembic

Quality Standards:
- Zero Mock Policy enforced (production-ready code only)
- Type hints (Python 3.11+)
- Docstrings (Google style)
- Zero N+1 queries (eager loading where needed)
"""

from app.db.base_class import Base

# Core Entities (6 models)
from app.models.user import User, Role, OAuthAccount, APIKey, RefreshToken
from app.models.project import Project, ProjectMember
from app.models.gate import Gate

# Gate Management (FR1) - 2 models
from app.models.gate_approval import GateApproval
from app.models.policy import PolicyEvaluation

# Evidence Vault (FR2) - 2 models
from app.models.gate_evidence import GateEvidence, EvidenceIntegrityCheck

# AI Engine (FR3) - 4 models
from app.models.ai_engine import AIProvider, AIRequest, AIUsageLog, AIEvidenceDraft

# Policy Library (FR5) - 3 models
from app.models.policy import Policy, CustomPolicy, PolicyTest

# Supporting - 4 models
from app.models.support import StageTransition, Webhook, AuditLog, Notification

# Compliance Scanning (Sprint 21) - 3 models
from app.models.compliance_scan import ComplianceScan, ComplianceViolation, ScanJob

__all__ = [
    # Base
    "Base",
    # Core Entities (6)
    "User",
    "Role",
    "OAuthAccount",
    "APIKey",
    "RefreshToken",
    "Project",
    "ProjectMember",
    "Gate",
    # Gate Management (2)
    "GateApproval",
    "PolicyEvaluation",
    # Evidence Vault (2)
    "GateEvidence",
    "EvidenceIntegrityCheck",
    # AI Engine (4)
    "AIProvider",
    "AIRequest",
    "AIUsageLog",
    "AIEvidenceDraft",
    # Policy Library (3)
    "Policy",
    "CustomPolicy",
    "PolicyTest",
    # Supporting (4)
    "StageTransition",
    "Webhook",
    "AuditLog",
    "Notification",
    # Compliance Scanning (3)
    "ComplianceScan",
    "ComplianceViolation",
    "ScanJob",
]

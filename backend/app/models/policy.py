"""
Policy Models - Policy Pack Library (FR5)
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: November 28, 2025
Status: ACTIVE - Week 3 Architecture Design
Authority: Backend Lead + CTO Approved
Foundation: Data Model v0.1, FR5 (Policy Pack Library)

Zero Mock Policy: Real SQLAlchemy model with all fields
Policy Engine: OPA (Open Policy Agent) with Rego language
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Policy(Base):
    """
    Policy model for pre-built SDLC 4.9 policies (FR5).

    Purpose:
        - 110+ pre-built policies covering all 10 SDLC 4.9 stages
        - OPA (Open Policy Agent) policy-as-code (Rego language)
        - Reusable policy templates
        - Version-controlled policy library

    Policy Examples:
        - Stage WHY: "Solution diversity requirement" (3+ options documented)
        - Stage WHAT: "FRD completeness check" (all sections present)
        - Stage BUILD: "Test coverage requirement" (>80% coverage)
        - Stage TEST: "Zero P0 bugs" (no critical bugs remaining)
        - Stage DEPLOY: "Rollback plan required" (deployment rollback documented)

    Fields:
        - id: UUID primary key
        - policy_name: Policy name (e.g., "FRD Completeness Check")
        - policy_code: Policy code/slug (e.g., "FRD_COMPLETENESS")
        - stage: SDLC stage ('WHY', 'WHAT', 'BUILD', etc.)
        - description: Policy description
        - rego_code: OPA Rego policy code
        - severity: Policy severity ('INFO', 'WARNING', 'ERROR', 'CRITICAL')
        - is_active: Policy status (True by default)
        - version: Policy version (e.g., "1.0.0")
        - created_at: Policy creation timestamp
        - updated_at: Last update timestamp
        - deleted_at: Soft delete timestamp

    Relationships:
        - custom_policies: One-to-Many with CustomPolicy model
        - policy_tests: One-to-Many with PolicyTest model
        - evaluations: One-to-Many with PolicyEvaluation model

    Indexes:
        - policy_code (unique, B-tree) - Fast policy lookup by code
        - stage (B-tree) - Stage-specific policies
        - is_active (B-tree) - Active policy filtering

    Usage Example:
        policy = Policy(
            policy_name="FRD Completeness Check",
            policy_code="FRD_COMPLETENESS",
            stage="WHAT",
            description="Verify FRD has all required sections",
            rego_code=\"\"\"
            package sdlc.what.frd_completeness

            required_sections := ["Introduction", "Functional Requirements", "API Contracts"]

            deny[msg] {
                missing := required_sections[_]
                not input.frd_sections[missing]
                msg := sprintf("FRD missing required section: %s", [missing])
            }
            \"\"\",
            severity="ERROR"
        )
    """

    __tablename__ = "policies"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Policy Identity
    policy_name = Column(String(255), nullable=False)
    policy_code = Column(
        String(100), unique=True, index=True, nullable=False
    )  # 'FRD_COMPLETENESS'

    # SDLC Stage
    stage = Column(
        String(20), nullable=False, index=True
    )  # 'WHY', 'WHAT', 'BUILD', etc.

    # Policy Definition
    description = Column(Text, nullable=True)
    rego_code = Column(Text, nullable=False)  # OPA Rego code

    # Policy Metadata
    severity = Column(
        String(20), nullable=False, default="ERROR"
    )  # 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
    version = Column(String(20), nullable=False, default="1.0.0")

    # Policy Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)

    # Audit Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    custom_policies = relationship(
        "CustomPolicy", back_populates="base_policy", cascade="all, delete-orphan"
    )
    policy_tests = relationship(
        "PolicyTest", back_populates="policy", cascade="all, delete-orphan"
    )
    evaluations = relationship(
        "PolicyEvaluation", back_populates="policy", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Policy(policy_code={self.policy_code}, stage={self.stage})>"


class CustomPolicy(Base):
    """
    Custom Policy model for project-specific policy customizations.

    Purpose:
        - Customize pre-built policies for specific projects
        - Override policy parameters (e.g., test coverage 80% → 95%)
        - Project-specific policy extensions

    Fields:
        - id: UUID primary key
        - project_id: Foreign key to Project
        - base_policy_id: Foreign key to Policy (base policy)
        - custom_rego_code: Customized OPA Rego code (overrides base)
        - is_active: Custom policy status
        - created_by: Foreign key to User (creator)
        - created_at: Custom policy creation timestamp
        - updated_at: Last update timestamp
        - deleted_at: Soft delete timestamp

    Relationships:
        - project: Many-to-One with Project model
        - base_policy: Many-to-One with Policy model
        - creator: Many-to-One with User model

    Indexes:
        - project_id (B-tree) - Fast project policy lookup
        - base_policy_id (B-tree) - Fast base policy lookup

    Usage Example:
        custom = CustomPolicy(
            project_id=project.id,
            base_policy_id=policy.id,
            custom_rego_code="...modified rego...",
            created_by=user.id
        )
    """

    __tablename__ = "custom_policies"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Project Relationship
    project_id = Column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Base Policy
    base_policy_id = Column(
        UUID(as_uuid=True),
        ForeignKey("policies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Customization
    custom_rego_code = Column(Text, nullable=False)  # Customized OPA Rego code

    # Status
    is_active = Column(Boolean, default=True, nullable=False)

    # Creator
    created_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Audit Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    deleted_at = Column(DateTime, nullable=True)

    # Relationships
    project = relationship("Project", back_populates="custom_policies")
    base_policy = relationship("Policy", back_populates="custom_policies")
    creator = relationship("User", back_populates="custom_policies")

    def __repr__(self) -> str:
        return f"<CustomPolicy(project_id={self.project_id}, base_policy_id={self.base_policy_id})>"


class PolicyTest(Base):
    """
    Policy Test model for policy validation.

    Purpose:
        - Test-driven policy development (5+ tests per policy)
        - Ensure policy behaves correctly
        - Regression testing when policies updated

    Fields:
        - id: UUID primary key
        - policy_id: Foreign key to Policy
        - test_name: Test name (e.g., "FRD missing section - should fail")
        - test_input: JSONB test input data
        - expected_result: Expected policy evaluation result
        - created_at: Test creation timestamp

    Relationships:
        - policy: Many-to-One with Policy model

    Indexes:
        - policy_id (B-tree) - Fast policy test lookup

    Usage Example:
        test = PolicyTest(
            policy_id=policy.id,
            test_name="FRD missing 'Introduction' section - should deny",
            test_input={"frd_sections": {"Functional Requirements": True}},
            expected_result={"allowed": False, "violations": ["FRD missing required section: Introduction"]}
        )
    """

    __tablename__ = "policy_tests"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Policy Relationship
    policy_id = Column(
        UUID(as_uuid=True),
        ForeignKey("policies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Test Definition
    test_name = Column(String(255), nullable=False)
    test_input = Column(JSONB, nullable=False)  # Test input data
    expected_result = Column(JSONB, nullable=False)  # Expected OPA output

    # Audit Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    policy = relationship("Policy", back_populates="policy_tests")

    def __repr__(self) -> str:
        return f"<PolicyTest(policy_id={self.policy_id}, test_name={self.test_name})>"


class PolicyEvaluation(Base):
    """
    Policy Evaluation model for gate policy check audit trail.

    Purpose:
        - Store policy evaluation results (OPA execution logs)
        - Audit trail for compliance
        - Policy violation tracking

    Fields:
        - id: UUID primary key
        - gate_id: Foreign key to Gate
        - policy_id: Foreign key to Policy
        - evaluation_result: JSONB evaluation result from OPA
        - is_passed: Policy check result (True = passed, False = failed)
        - violations: JSONB array of violations
        - evaluated_at: Evaluation timestamp
        - created_at: Record creation timestamp

    Relationships:
        - gate: Many-to-One with Gate model
        - policy: Many-to-One with Policy model

    Indexes:
        - gate_id + policy_id (composite) - Fast gate policy lookup
        - is_passed (B-tree) - Failed policy filtering
        - evaluated_at (B-tree) - Recent evaluations

    Usage Example:
        evaluation = PolicyEvaluation(
            gate_id=gate.id,
            policy_id=policy.id,
            evaluation_result={"allowed": False},
            is_passed=False,
            violations=[{"message": "FRD missing required section: Introduction"}],
            evaluated_at=datetime.utcnow()
        )
    """

    __tablename__ = "policy_evaluations"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Gate Relationship
    gate_id = Column(
        UUID(as_uuid=True),
        ForeignKey("gates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Policy Relationship
    policy_id = Column(
        UUID(as_uuid=True),
        ForeignKey("policies.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Evaluation Results
    evaluation_result = Column(JSONB, nullable=False)  # Full OPA output
    is_passed = Column(
        Boolean, nullable=False, index=True
    )  # True = passed, False = failed
    violations = Column(JSONB, nullable=False, default=list)  # Violation messages

    # Evaluation Metadata
    evaluated_at = Column(DateTime, nullable=False, index=True)

    # Audit Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    gate = relationship("Gate", back_populates="policy_evaluations")
    policy = relationship("Policy", back_populates="evaluations")

    def __repr__(self) -> str:
        return f"<PolicyEvaluation(gate_id={self.gate_id}, policy_id={self.policy_id}, is_passed={self.is_passed})>"

    @property
    def violation_count(self) -> int:
        """Count number of violations"""
        return len(self.violations) if self.violations else 0

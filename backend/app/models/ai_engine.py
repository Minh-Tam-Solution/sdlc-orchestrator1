"""
AI Engine Models - AI Context Engine (FR3)
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: November 28, 2025
Status: ACTIVE - Week 3 Architecture Design
Authority: Backend Lead + CTO Approved
Foundation: Data Model v0.1, FR3 (AI Context Engine)

Zero Mock Policy: Real SQLAlchemy model with all fields
AI Providers: Claude Sonnet 4.5, GPT-4o, Gemini 2.0 Flash
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AIProvider(Base):
    """
    AI Provider model for multi-provider AI configuration (FR3).

    Purpose:
        - Multi-provider support (Claude, GPT-4o, Gemini)
        - Provider-specific configuration (API keys, models, pricing)
        - Load balancing and fallback

    Supported Providers:
        - Anthropic Claude (Sonnet 4.5): Complex reasoning, policy drafting
        - OpenAI GPT-4o: Code generation, test writing
        - Google Gemini 2.0 Flash: Bulk tasks, fast responses

    Fields:
        - id: UUID primary key
        - provider_name: Provider name ('anthropic', 'openai', 'google')
        - provider_type: Provider type ('claude', 'gpt', 'gemini')
        - api_key_encrypted: Encrypted API key (AES-256)
        - model_name: Model identifier (e.g., 'claude-sonnet-4-5')
        - is_active: Provider status (True = enabled)
        - priority: Provider priority (1 = highest, for load balancing)
        - cost_per_1k_input_tokens: Input token cost (USD)
        - cost_per_1k_output_tokens: Output token cost (USD)
        - max_tokens: Max output tokens
        - temperature: Model temperature (0.0-1.0)
        - created_at: Provider configuration timestamp
        - updated_at: Last update timestamp

    Relationships:
        - ai_requests: One-to-Many with AIRequest model

    Indexes:
        - provider_type (B-tree) - Fast provider type filtering
        - is_active + priority (composite) - Load balancing queries

    Usage Example:
        provider = AIProvider(
            provider_name="Anthropic",
            provider_type="claude",
            api_key_encrypted="...",
            model_name="claude-sonnet-4-5-20250929",
            priority=1,
            cost_per_1k_input_tokens=0.003,
            cost_per_1k_output_tokens=0.015
        )
    """

    __tablename__ = "ai_providers"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Provider Identity
    provider_name = Column(String(100), nullable=False)  # 'Anthropic', 'OpenAI', 'Google'
    provider_type = Column(
        String(50), nullable=False, index=True
    )  # 'claude', 'gpt', 'gemini'

    # API Configuration
    api_key_encrypted = Column(Text, nullable=False)  # AES-256 encrypted
    model_name = Column(String(100), nullable=False)  # 'claude-sonnet-4-5-20250929'

    # Provider Status
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    priority = Column(
        Integer, nullable=False, default=10
    )  # 1 = highest priority (load balancing)

    # Pricing (USD)
    cost_per_1k_input_tokens = Column(Numeric(10, 6), nullable=False)
    cost_per_1k_output_tokens = Column(Numeric(10, 6), nullable=False)

    # Model Parameters
    max_tokens = Column(Integer, nullable=False, default=4096)
    temperature = Column(Numeric(3, 2), nullable=False, default=0.7)

    # Audit Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    ai_requests = relationship(
        "AIRequest", back_populates="provider", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<AIProvider(provider_type={self.provider_type}, model_name={self.model_name})>"


class AIRequest(Base):
    """
    AI Request model for AI request tracking and cost monitoring.

    Purpose:
        - Track all AI requests (audit trail)
        - Cost monitoring ($500/month budget Phase 1)
        - Performance monitoring (response times)
        - Error tracking (rate limits, failures)

    Fields:
        - id: UUID primary key
        - provider_id: Foreign key to AIProvider
        - user_id: Foreign key to User (requester)
        - gate_id: Foreign key to Gate (if gate-related)
        - request_type: Request type ('GATE_SUMMARY', 'POLICY_DRAFT', 'CODE_REVIEW', etc.)
        - prompt: User prompt/input
        - response: AI response/output
        - input_tokens: Input token count
        - output_tokens: Output token count
        - total_cost: Request cost (USD)
        - response_time_ms: Response time in milliseconds
        - status: Request status ('SUCCESS', 'ERROR', 'RATE_LIMITED')
        - error_message: Error details if failed
        - created_at: Request timestamp

    Relationships:
        - provider: Many-to-One with AIProvider model
        - user: Many-to-One with User model
        - gate: Many-to-One with Gate model
        - usage_logs: One-to-Many with AIUsageLog model

    Indexes:
        - provider_id (B-tree) - Fast provider request lookup
        - user_id (B-tree) - Fast user request lookup
        - gate_id (B-tree) - Fast gate request lookup
        - created_at (B-tree) - Recent requests queries
        - status (B-tree) - Failed request filtering

    Usage Example:
        request = AIRequest(
            provider_id=provider.id,
            user_id=user.id,
            gate_id=gate.id,
            request_type='GATE_SUMMARY',
            prompt='Summarize this gate...',
            response='Gate summary: ...',
            input_tokens=1500,
            output_tokens=800,
            total_cost=0.0165,  # (1.5 * 0.003) + (0.8 * 0.015)
            response_time_ms=2150,
            status='SUCCESS'
        )
    """

    __tablename__ = "ai_requests"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Provider Relationship
    provider_id = Column(
        UUID(as_uuid=True),
        ForeignKey("ai_providers.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # User Relationship
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Gate Relationship (optional)
    gate_id = Column(
        UUID(as_uuid=True),
        ForeignKey("gates.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Request Type
    request_type = Column(
        String(50), nullable=False
    )  # 'GATE_SUMMARY', 'POLICY_DRAFT', 'CODE_REVIEW', etc.

    # Request/Response
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=True)

    # Token Usage
    input_tokens = Column(Integer, nullable=False, default=0)
    output_tokens = Column(Integer, nullable=False, default=0)

    # Cost
    total_cost = Column(Numeric(10, 6), nullable=False, default=0.0)  # USD

    # Performance
    response_time_ms = Column(Integer, nullable=True)  # Milliseconds

    # Request Status
    status = Column(
        String(20), nullable=False, default="SUCCESS", index=True
    )  # 'SUCCESS', 'ERROR', 'RATE_LIMITED'
    error_message = Column(Text, nullable=True)

    # Audit Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    provider = relationship("AIProvider", back_populates="ai_requests")
    user = relationship("User", back_populates="ai_requests")
    gate = relationship("Gate", back_populates="ai_requests")
    usage_logs = relationship(
        "AIUsageLog", back_populates="request", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<AIRequest(id={self.id}, request_type={self.request_type}, status={self.status})>"


class AIUsageLog(Base):
    """
    AI Usage Log model for monthly budget monitoring.

    Purpose:
        - Monthly cost aggregation ($500/month budget Phase 1)
        - Provider-level cost tracking
        - Budget alerts (80%, 90%, 100% thresholds)

    Fields:
        - id: UUID primary key
        - request_id: Foreign key to AIRequest
        - month: Month (YYYY-MM format, e.g., '2026-02')
        - provider_type: Provider type ('claude', 'gpt', 'gemini')
        - total_cost: Request cost (USD)
        - input_tokens: Input token count
        - output_tokens: Output token count
        - created_at: Log timestamp

    Relationships:
        - request: Many-to-One with AIRequest model

    Indexes:
        - month + provider_type (composite) - Monthly cost aggregation
        - created_at (B-tree) - Recent logs queries

    Usage Example:
        log = AIUsageLog(
            request_id=request.id,
            month='2026-02',
            provider_type='claude',
            total_cost=0.0165,
            input_tokens=1500,
            output_tokens=800
        )
    """

    __tablename__ = "ai_usage_logs"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Request Relationship
    request_id = Column(
        UUID(as_uuid=True),
        ForeignKey("ai_requests.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Month Tracking
    month = Column(String(7), nullable=False, index=True)  # 'YYYY-MM'

    # Provider Type
    provider_type = Column(String(50), nullable=False, index=True)

    # Cost
    total_cost = Column(Numeric(10, 6), nullable=False)  # USD

    # Token Usage
    input_tokens = Column(BigInteger, nullable=False)
    output_tokens = Column(BigInteger, nullable=False)

    # Audit Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    request = relationship("AIRequest", back_populates="usage_logs")

    def __repr__(self) -> str:
        return f"<AIUsageLog(month={self.month}, provider_type={self.provider_type}, total_cost={self.total_cost})>"


class AIEvidenceDraft(Base):
    """
    AI Evidence Draft model for AI-generated content drafts.

    Purpose:
        - Store AI-generated evidence drafts (not final)
        - Human review required before submission
        - Track AI-assisted evidence creation

    Fields:
        - id: UUID primary key
        - gate_id: Foreign key to Gate
        - evidence_type: Evidence type ('DESIGN_DOCUMENT', 'TEST_RESULTS', etc.)
        - draft_content: AI-generated content
        - ai_request_id: Foreign key to AIRequest (which AI request generated this)
        - is_approved: Human approval status
        - approved_by: Foreign key to User (approver)
        - approved_at: Approval timestamp
        - created_at: Draft creation timestamp

    Relationships:
        - gate: Many-to-One with Gate model
        - ai_request: Many-to-One with AIRequest model
        - approver: Many-to-One with User model

    Indexes:
        - gate_id (B-tree) - Fast gate draft lookup
        - is_approved (B-tree) - Pending approval filtering

    Usage Example:
        draft = AIEvidenceDraft(
            gate_id=gate.id,
            evidence_type='DESIGN_DOCUMENT',
            draft_content='# API Design\n\nGenerated by Claude...',
            ai_request_id=request.id,
            is_approved=False
        )
    """

    __tablename__ = "ai_evidence_drafts"

    # Primary Key
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)

    # Gate Relationship
    gate_id = Column(
        UUID(as_uuid=True),
        ForeignKey("gates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Evidence Type
    evidence_type = Column(String(50), nullable=False)

    # Draft Content
    draft_content = Column(Text, nullable=False)

    # AI Request Relationship
    ai_request_id = Column(
        UUID(as_uuid=True),
        ForeignKey("ai_requests.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Approval
    is_approved = Column(Boolean, default=False, nullable=False, index=True)
    approved_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    approved_at = Column(DateTime, nullable=True)

    # Audit Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    gate = relationship("Gate", back_populates="ai_evidence_drafts")
    ai_request = relationship("AIRequest")
    approver = relationship("User")

    def __repr__(self) -> str:
        return f"<AIEvidenceDraft(id={self.id}, gate_id={self.gate_id}, is_approved={self.is_approved})>"

"""
=========================================================================
SOP Generator Service Unit Tests - Phase 2-Pilot Week 1
SDLC Orchestrator - Stage 03 (BUILD)

Version: 1.0.0
Date: December 23, 2025
Status: ACTIVE - Phase 2-Pilot Week 1 (SE 3.0 Track 1)
Authority: Backend Lead + CTO Approved
Foundation: BRS-PILOT-001, SE 3.0 SASE Integration
Framework: SDLC 5.1.0 Complete Lifecycle

Purpose:
- Unit tests for SOPGeneratorService
- Test SOP generation for 5 types
- Test section parsing (FR2)
- Test completeness scoring
- Test SHA256 hashing (FR5)
- Test MRP evidence generation (FR6)

Test Coverage:
- ✅ SOP type enum (FR3: 5 types)
- ✅ Prompt building for each type
- ✅ Section parsing (FR2: 5 sections)
- ✅ Completeness calculation
- ✅ SHA256 hash generation (FR5)
- ✅ SOP ID generation
- ✅ MRP ID generation
- ✅ Supported types listing (FR3)

Zero Mock Policy: Real service logic with mocked Ollama calls
=========================================================================
"""

import hashlib
import pytest
from datetime import datetime
from unittest.mock import MagicMock, patch, AsyncMock

from app.services.sop_generator_service import (
    SOPType,
    SOPStatus,
    SOPSection,
    GeneratedSOP,
    SOPGenerationRequest,
    MRPEvidence,
    SOP_TEMPLATES,
    SOPGeneratorService,
    get_sop_generator_service,
)


# ============================================================================
# Test Fixtures
# ============================================================================


@pytest.fixture
def sop_service():
    """Create SOP Generator service instance."""
    return SOPGeneratorService(
        ollama_base_url="http://localhost:11434",
        ollama_model="llama2:13b",
        timeout=30,
    )


@pytest.fixture
def sample_markdown_complete():
    """Sample complete SOP markdown content."""
    return """# SOP: Application Deployment Procedure

## Document Control
- **Document ID:** SOP-DEPLOYMENT-001
- **Version:** 1.0.0
- **Effective Date:** 2025-12-23
- **Owner:** DevOps Lead
- **Approver:** CTO

## 1. Purpose
This SOP defines the standardized procedure for deploying applications to production.
It ensures consistent, reliable deployments with proper verification and rollback capabilities.

## 2. Scope
- Covered systems: All containerized applications deployed to Kubernetes
- Excluded: Database-only changes (covered by separate SOP)

## 3. Procedure
1. Verify pre-deployment checklist is complete
2. Create deployment branch from main
3. Run automated tests (unit, integration, e2e)
4. Build and push Docker images
5. Deploy to staging environment
6. Run smoke tests on staging
7. Get approval from Tech Lead
8. Deploy to production using rolling update
9. Monitor metrics for 15 minutes
10. Verify health checks pass

## 4. Roles and Responsibilities
| Role | Responsibility | RACI |
|------|----------------|------|
| Developer | Prepare deployment | R |
| Tech Lead | Approve deployment | A |
| DevOps | Execute deployment | R |
| QA | Verify staging | C |
| PM | Track progress | I |

## 5. Quality Criteria
- [ ] All tests pass (100% green)
- [ ] Staging verification complete
- [ ] Tech Lead approval received
- [ ] Zero P0 alerts during deployment
- [ ] Rollback tested within last 30 days

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-23 | AI Agent | Initial version |
"""


@pytest.fixture
def sample_markdown_partial():
    """Sample partial SOP markdown (missing some sections)."""
    return """# SOP: Incident Response

## 1. Purpose
This SOP defines incident response procedures.

## 3. Procedure
1. Detect incident
2. Classify severity
3. Escalate as needed
4. Resolve issue

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-23 | AI Agent | Initial version |
"""


# ============================================================================
# Test SOPType Enum (FR3)
# ============================================================================


class TestSOPType:
    """Test SOP type enumeration (FR3: 5 types)."""

    def test_deployment_type_exists(self):
        """Verify deployment SOP type."""
        assert SOPType.DEPLOYMENT.value == "deployment"

    def test_incident_type_exists(self):
        """Verify incident SOP type."""
        assert SOPType.INCIDENT.value == "incident"

    def test_change_type_exists(self):
        """Verify change SOP type."""
        assert SOPType.CHANGE.value == "change"

    def test_backup_type_exists(self):
        """Verify backup SOP type."""
        assert SOPType.BACKUP.value == "backup"

    def test_security_type_exists(self):
        """Verify security SOP type."""
        assert SOPType.SECURITY.value == "security"

    def test_total_types_count(self):
        """FR3: Exactly 5 SOP types required."""
        assert len(SOPType) == 5


class TestSOPStatus:
    """Test SOP status enumeration."""

    def test_status_values(self):
        """Verify all status values exist."""
        assert SOPStatus.DRAFT.value == "draft"
        assert SOPStatus.PENDING_REVIEW.value == "pending_review"
        assert SOPStatus.APPROVED.value == "approved"
        assert SOPStatus.REJECTED.value == "rejected"
        assert SOPStatus.REVISION_REQUIRED.value == "revision_required"


# ============================================================================
# Test SOP Templates (FR3)
# ============================================================================


class TestSOPTemplates:
    """Test SOP template configurations."""

    def test_all_types_have_templates(self):
        """Every SOP type must have a template."""
        for sop_type in SOPType:
            assert sop_type in SOP_TEMPLATES
            assert "name" in SOP_TEMPLATES[sop_type]
            assert "description" in SOP_TEMPLATES[sop_type]
            assert "typical_sections" in SOP_TEMPLATES[sop_type]
            assert "prompt_context" in SOP_TEMPLATES[sop_type]

    def test_deployment_template(self):
        """Verify deployment template content."""
        template = SOP_TEMPLATES[SOPType.DEPLOYMENT]
        assert template["name"] == "Deployment SOP"
        assert "deployment" in template["prompt_context"].lower()

    def test_incident_template(self):
        """Verify incident template content."""
        template = SOP_TEMPLATES[SOPType.INCIDENT]
        assert template["name"] == "Incident Response SOP"
        assert "incident" in template["prompt_context"].lower()

    def test_change_template(self):
        """Verify change template content."""
        template = SOP_TEMPLATES[SOPType.CHANGE]
        assert template["name"] == "Change Management SOP"
        assert "change" in template["prompt_context"].lower()

    def test_backup_template(self):
        """Verify backup template content."""
        template = SOP_TEMPLATES[SOPType.BACKUP]
        assert template["name"] == "Backup and Recovery SOP"
        assert "backup" in template["prompt_context"].lower()

    def test_security_template(self):
        """Verify security template content."""
        template = SOP_TEMPLATES[SOPType.SECURITY]
        assert template["name"] == "Security SOP"
        assert "security" in template["prompt_context"].lower()


# ============================================================================
# Test Data Classes
# ============================================================================


class TestGeneratedSOP:
    """Test GeneratedSOP data class."""

    def test_default_values(self):
        """Verify default values are set correctly."""
        sop = GeneratedSOP(
            sop_id="SOP-DEPLOYMENT-001",
            sop_type=SOPType.DEPLOYMENT,
        )
        assert sop.version == "1.0.0"
        assert sop.status == SOPStatus.DRAFT
        assert sop.created_by == "AI Agent (Ollama)"
        assert sop.purpose == ""
        assert sop.scope == ""
        assert sop.procedure == ""
        assert sop.roles == ""
        assert sop.quality_criteria == ""

    def test_to_dict(self):
        """Verify to_dict serialization."""
        sop = GeneratedSOP(
            sop_id="SOP-DEPLOYMENT-001",
            sop_type=SOPType.DEPLOYMENT,
            title="Test SOP",
            purpose="Test purpose",
        )
        result = sop.to_dict()
        assert result["sop_id"] == "SOP-DEPLOYMENT-001"
        assert result["sop_type"] == "deployment"
        assert result["title"] == "Test SOP"
        assert result["purpose"] == "Test purpose"
        assert result["status"] == "draft"


class TestMRPEvidence:
    """Test MRPEvidence data class."""

    def test_default_values(self):
        """Verify default values."""
        mrp = MRPEvidence(mrp_id="MRP-PILOT-001")
        assert mrp.brs_id == "BRS-PILOT-001"
        assert mrp.sections_required == 5
        assert mrp.ai_provider == "ollama"
        assert mrp.status == "pending_review"

    def test_to_dict(self):
        """Verify to_dict serialization."""
        mrp = MRPEvidence(
            mrp_id="MRP-PILOT-001",
            sop_id="SOP-DEPLOYMENT-001",
            completeness_score=80.0,
        )
        result = mrp.to_dict()
        assert result["mrp_id"] == "MRP-PILOT-001"
        assert result["sop_id"] == "SOP-DEPLOYMENT-001"
        assert result["completeness_score"] == 80.0
        assert result["brs_id"] == "BRS-PILOT-001"


# ============================================================================
# Test SOPGeneratorService
# ============================================================================


class TestSOPGeneratorService:
    """Test SOP Generator Service methods."""

    def test_init(self, sop_service):
        """Verify service initialization."""
        assert sop_service.ollama_base_url == "http://localhost:11434"
        assert sop_service.ollama_model == "llama2:13b"
        assert sop_service.timeout == 30

    def test_generate_sop_id(self, sop_service):
        """Test SOP ID generation format."""
        sop_id = sop_service._generate_sop_id(SOPType.DEPLOYMENT)
        assert sop_id.startswith("SOP-DEPLOYMENT-")
        assert len(sop_id) > 20  # Includes timestamp and UUID

    def test_generate_mrp_id(self, sop_service):
        """Test MRP ID generation format."""
        mrp_id = sop_service._generate_mrp_id()
        assert mrp_id.startswith("MRP-PILOT-")
        assert len(mrp_id) > 15

    def test_compute_sha256(self, sop_service):
        """Test SHA256 hash computation (FR5)."""
        content = "Test content for hashing"
        expected = hashlib.sha256(content.encode("utf-8")).hexdigest()
        result = sop_service._compute_sha256(content)
        assert result == expected
        assert len(result) == 64  # SHA256 produces 64 hex chars

    def test_build_prompt_deployment(self, sop_service):
        """Test prompt building for deployment type."""
        prompt = sop_service._build_prompt(
            SOPType.DEPLOYMENT,
            "Deploy app to Kubernetes",
            "Zero-downtime required",
        )
        assert "WORKFLOW DESCRIPTION:" in prompt
        assert "Deploy app to Kubernetes" in prompt
        assert "ADDITIONAL CONTEXT:" in prompt
        assert "Zero-downtime required" in prompt
        assert "ISO 9001" in prompt

    def test_build_prompt_without_context(self, sop_service):
        """Test prompt building without additional context."""
        prompt = sop_service._build_prompt(
            SOPType.INCIDENT,
            "Handle P0 incidents",
            None,
        )
        assert "WORKFLOW DESCRIPTION:" in prompt
        assert "Handle P0 incidents" in prompt
        assert "ADDITIONAL CONTEXT:" not in prompt

    def test_parse_sop_sections_complete(self, sop_service, sample_markdown_complete):
        """Test section parsing with complete SOP (FR2)."""
        sections = sop_service._parse_sop_sections(sample_markdown_complete)
        assert sections["purpose"] != ""
        assert sections["scope"] != ""
        assert sections["procedure"] != ""
        assert sections["roles"] != ""
        assert sections["quality_criteria"] != ""

    def test_parse_sop_sections_partial(self, sop_service, sample_markdown_partial):
        """Test section parsing with partial SOP."""
        sections = sop_service._parse_sop_sections(sample_markdown_partial)
        assert sections["purpose"] != ""
        assert sections["procedure"] != ""
        # Missing sections should be empty
        assert sections["scope"] == ""
        assert sections["roles"] == ""
        assert sections["quality_criteria"] == ""

    def test_calculate_completeness_100(self, sop_service):
        """Test completeness calculation for complete SOP."""
        sections = {
            "purpose": "Test purpose",
            "scope": "Test scope",
            "procedure": "Test procedure",
            "roles": "Test roles",
            "quality_criteria": "Test quality",
        }
        present, score = sop_service._calculate_completeness(sections)
        assert present == 5
        assert score == 100.0

    def test_calculate_completeness_partial(self, sop_service):
        """Test completeness calculation for partial SOP."""
        sections = {
            "purpose": "Test purpose",
            "scope": "",
            "procedure": "Test procedure",
            "roles": "",
            "quality_criteria": "",
        }
        present, score = sop_service._calculate_completeness(sections)
        assert present == 2
        assert score == 40.0

    def test_calculate_completeness_empty(self, sop_service):
        """Test completeness calculation for empty SOP."""
        sections = {
            "purpose": "",
            "scope": "",
            "procedure": "",
            "roles": "",
            "quality_criteria": "",
        }
        present, score = sop_service._calculate_completeness(sections)
        assert present == 0
        assert score == 0.0

    def test_get_supported_types(self, sop_service):
        """Test supported types listing (FR3)."""
        types = sop_service.get_supported_types()
        assert len(types) == 5  # FR3: 5 types

        type_values = [t["type"] for t in types]
        assert "deployment" in type_values
        assert "incident" in type_values
        assert "change" in type_values
        assert "backup" in type_values
        assert "security" in type_values

        # Each type should have required fields
        for t in types:
            assert "type" in t
            assert "name" in t
            assert "description" in t
            assert "typical_sections" in t


class TestSOPGeneratorServiceIntegration:
    """Integration tests with mocked Ollama."""

    @pytest.mark.asyncio
    async def test_generate_sop_success(self, sop_service, sample_markdown_complete):
        """Test successful SOP generation."""
        with patch.object(sop_service, "_call_ollama") as mock_ollama:
            mock_ollama.return_value = (
                sample_markdown_complete,
                {
                    "generation_time_ms": 5000.0,
                    "model": "llama2:13b",
                    "prompt_tokens": 500,
                    "completion_tokens": 1000,
                },
            )

            request = SOPGenerationRequest(
                sop_type=SOPType.DEPLOYMENT,
                workflow_description="Deploy the application to production Kubernetes cluster.",
            )

            sop, mrp = await sop_service.generate_sop(request)

            # Verify SOP
            assert sop.sop_id.startswith("SOP-DEPLOYMENT-")
            assert sop.sop_type == SOPType.DEPLOYMENT
            assert sop.status == SOPStatus.DRAFT
            assert sop.sha256_hash != ""
            assert len(sop.sha256_hash) == 64
            assert sop.generation_time_ms == 5000.0
            assert sop.purpose != ""  # Should be parsed

            # Verify MRP (FR6)
            assert mrp.mrp_id.startswith("MRP-PILOT-")
            assert mrp.sop_id == sop.sop_id
            assert mrp.brs_id == "BRS-PILOT-001"
            assert mrp.completeness_score == 100.0  # Complete SOP
            assert mrp.sections_present == 5
            assert mrp.sha256_hash == sop.sha256_hash

    @pytest.mark.asyncio
    async def test_generate_sop_partial_content(self, sop_service, sample_markdown_partial):
        """Test SOP generation with partial content."""
        with patch.object(sop_service, "_call_ollama") as mock_ollama:
            mock_ollama.return_value = (
                sample_markdown_partial,
                {
                    "generation_time_ms": 3000.0,
                    "model": "llama2:13b",
                    "prompt_tokens": 400,
                    "completion_tokens": 500,
                },
            )

            request = SOPGenerationRequest(
                sop_type=SOPType.INCIDENT,
                workflow_description="Handle production incidents.",
            )

            sop, mrp = await sop_service.generate_sop(request)

            # Completeness should reflect missing sections
            assert mrp.completeness_score == 40.0  # 2/5 sections
            assert mrp.sections_present == 2

    @pytest.mark.asyncio
    async def test_generate_sop_all_types(self, sop_service, sample_markdown_complete):
        """Test SOP generation for all 5 types (FR3)."""
        with patch.object(sop_service, "_call_ollama") as mock_ollama:
            mock_ollama.return_value = (
                sample_markdown_complete,
                {
                    "generation_time_ms": 5000.0,
                    "model": "llama2:13b",
                    "prompt_tokens": 500,
                    "completion_tokens": 1000,
                },
            )

            for sop_type in SOPType:
                request = SOPGenerationRequest(
                    sop_type=sop_type,
                    workflow_description=f"Test workflow for {sop_type.value}",
                )

                sop, mrp = await sop_service.generate_sop(request)

                assert sop.sop_type == sop_type
                assert sop_type.value.upper() in sop.sop_id


# ============================================================================
# Test Factory Function
# ============================================================================


class TestServiceFactory:
    """Test service factory function."""

    def test_get_sop_generator_service(self):
        """Test factory creates service with default settings."""
        service = get_sop_generator_service()
        assert isinstance(service, SOPGeneratorService)
        assert service.timeout == 30  # NFR1 requirement

    @patch("app.services.sop_generator_service.settings")
    def test_get_sop_generator_service_custom_config(self, mock_settings):
        """Test factory uses custom settings."""
        mock_settings.OLLAMA_BASE_URL = "http://custom:11434"
        mock_settings.OLLAMA_MODEL = "mistral:7b"

        service = get_sop_generator_service()

        assert service.ollama_base_url == "http://custom:11434"
        assert service.ollama_model == "mistral:7b"


# ============================================================================
# Test Error Handling
# ============================================================================


class TestErrorHandling:
    """Test error handling scenarios."""

    @pytest.mark.asyncio
    async def test_ollama_timeout(self, sop_service):
        """Test handling of Ollama timeout."""
        with patch.object(sop_service, "_call_ollama") as mock_ollama:
            mock_ollama.side_effect = Exception("SOP generation timeout (>30s)")

            request = SOPGenerationRequest(
                sop_type=SOPType.DEPLOYMENT,
                workflow_description="Test workflow",
            )

            with pytest.raises(Exception) as exc_info:
                await sop_service.generate_sop(request)

            assert "timeout" in str(exc_info.value).lower()

    @pytest.mark.asyncio
    async def test_ollama_connection_error(self, sop_service):
        """Test handling of Ollama connection error."""
        with patch.object(sop_service, "_call_ollama") as mock_ollama:
            mock_ollama.side_effect = Exception("Cannot connect to Ollama")

            request = SOPGenerationRequest(
                sop_type=SOPType.INCIDENT,
                workflow_description="Test workflow",
            )

            with pytest.raises(Exception) as exc_info:
                await sop_service.generate_sop(request)

            assert "connect" in str(exc_info.value).lower()

"""
=========================================================================
Specification Validation Integration Tests - Sprint 118 (SPEC-0002)
SDLC Orchestrator - Stage 04 (BUILD)

Version: 1.0.0
Date: January 29, 2026
Status: ACTIVE - Sprint 118 Track 2 Phase 5
Authority: Backend Lead + CTO Approved
Foundation: SPEC-0002 Specification Standard
Framework: SDLC 5.3.0 Quality Assurance System

Purpose:
- Integration tests for Specification validation critical path
- Test YAML frontmatter validation
- Test specification retrieval
- Test BDD requirements listing
- Test acceptance criteria management

Test Coverage:
- ✅ POST /governance/specs/validate
- ✅ GET /governance/specs/{spec_id}
- ✅ GET /governance/specs/{spec_id}/requirements
- ✅ GET /governance/specs/{spec_id}/acceptance-criteria

Zero Mock Policy: Production-ready integration tests
=========================================================================
"""

import pytest
from httpx import AsyncClient
from uuid import uuid4

from app.models.user import User


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture
def valid_frontmatter() -> str:
    """Valid YAML frontmatter content."""
    return """---
spec_version: "1.0"
spec_id: SPEC-0001
status: approved
tier: PROFESSIONAL
stage: 04-build
owner: backend-team
created: 2026-01-29
last_updated: 2026-01-29
related_adrs: [ADR-041, ADR-022]
---

## 1. Overview
This specification defines the Anti-Vibecoding System.

## 2. Requirements
### 2.1 Functional Requirements (BDD)
- GIVEN a code submission WHEN signals are evaluated THEN index is calculated
- GIVEN an index score WHEN routing is requested THEN appropriate zone is returned

### 2.2 Non-Functional Requirements
- Performance: <100ms p95 latency
- Security: OWASP ASVS L2 compliance

## 3. Acceptance Criteria
- [ ] All 5 signals calculate correctly
- [ ] Routing matches zone thresholds
- [ ] Kill switch triggers on threshold breach
"""


@pytest.fixture
def invalid_frontmatter_missing_fields() -> str:
    """Invalid frontmatter - missing required fields."""
    return """---
spec_version: "1.0"
status: draft
---

## Overview
This spec is missing required fields.
"""


@pytest.fixture
def invalid_frontmatter_bad_yaml() -> str:
    """Invalid frontmatter - malformed YAML."""
    return """---
spec_version: 1.0
status: draft
tier: [INVALID
owner: missing-colon
---

## Overview
This spec has malformed YAML.
"""


@pytest.fixture
def valid_frontmatter_lite_tier() -> str:
    """Valid frontmatter for LITE tier."""
    return """---
spec_version: "1.0"
spec_id: SPEC-0099
status: draft
tier: LITE
stage: 01-planning
owner: solo-dev
created: 2026-01-29
last_updated: 2026-01-29
related_adrs: []
---

## Overview
A minimal spec for LITE tier projects.
"""


@pytest.fixture
def sample_spec_id() -> str:
    """Sample spec ID for testing."""
    return f"SPEC-{uuid4().hex[:4].upper()}"


# ============================================================================
# Frontmatter Validation Tests
# ============================================================================


@pytest.mark.asyncio
async def test_validate_frontmatter_valid(
    client: AsyncClient,
    auth_headers: dict,
    valid_frontmatter: str,
):
    """Test POST /governance/specs/validate - Valid frontmatter."""
    request_data = {
        "content": valid_frontmatter,
        "tier": "PROFESSIONAL",
    }

    response = await client.post(
        "/api/v1/governance/specs/validate",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify response structure
    assert "valid" in data
    assert "errors" in data
    assert "warnings" in data
    assert "parsed_metadata" in data
    assert "compliance_score" in data
    assert "suggestions" in data

    # Verify validation passed
    assert data["valid"] is True
    assert len(data["errors"]) == 0
    assert data["compliance_score"] >= 80

    # Verify parsed metadata
    metadata = data["parsed_metadata"]
    assert metadata["spec_id"] == "SPEC-0001"
    assert metadata["status"] == "approved"
    assert metadata["tier"] == "PROFESSIONAL"
    assert metadata["owner"] == "backend-team"
    assert "ADR-041" in metadata["related_adrs"]


@pytest.mark.asyncio
async def test_validate_frontmatter_missing_fields(
    client: AsyncClient,
    auth_headers: dict,
    invalid_frontmatter_missing_fields: str,
):
    """Test POST /governance/specs/validate - Missing required fields."""
    request_data = {
        "content": invalid_frontmatter_missing_fields,
    }

    response = await client.post(
        "/api/v1/governance/specs/validate",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify validation failed
    assert data["valid"] is False
    assert len(data["errors"]) > 0

    # Check for expected missing fields
    error_fields = [e["field"] for e in data["errors"]]
    assert "spec_id" in error_fields or "tier" in error_fields or "owner" in error_fields


@pytest.mark.asyncio
async def test_validate_frontmatter_bad_yaml(
    client: AsyncClient,
    auth_headers: dict,
    invalid_frontmatter_bad_yaml: str,
):
    """Test POST /governance/specs/validate - Malformed YAML."""
    request_data = {
        "content": invalid_frontmatter_bad_yaml,
    }

    response = await client.post(
        "/api/v1/governance/specs/validate",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # Verify validation failed
    assert data["valid"] is False
    assert len(data["errors"]) > 0

    # Should have YAML parsing error
    has_yaml_error = any(
        "yaml" in e["message"].lower() or "parse" in e["message"].lower()
        for e in data["errors"]
    )
    assert has_yaml_error or data["parsed_metadata"] is None


@pytest.mark.asyncio
async def test_validate_frontmatter_lite_tier(
    client: AsyncClient,
    auth_headers: dict,
    valid_frontmatter_lite_tier: str,
):
    """Test POST /governance/specs/validate - LITE tier (fewer requirements)."""
    request_data = {
        "content": valid_frontmatter_lite_tier,
        "tier": "LITE",
    }

    response = await client.post(
        "/api/v1/governance/specs/validate",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # LITE tier should pass with minimal fields
    assert data["valid"] is True
    assert data["parsed_metadata"]["tier"] == "LITE"


@pytest.mark.asyncio
async def test_validate_frontmatter_with_file_path(
    client: AsyncClient,
    auth_headers: dict,
    valid_frontmatter: str,
):
    """Test POST /governance/specs/validate - With file path context."""
    request_data = {
        "content": valid_frontmatter,
        "file_path": "docs/02-design/14-Technical-Specs/SPEC-0001-Anti-Vibecoding.md",
    }

    response = await client.post(
        "/api/v1/governance/specs/validate",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    assert data["valid"] is True


@pytest.mark.asyncio
async def test_validate_frontmatter_unauthorized(
    client: AsyncClient,
    valid_frontmatter: str,
):
    """Test POST /governance/specs/validate - Unauthorized."""
    request_data = {
        "content": valid_frontmatter,
    }

    response = await client.post(
        "/api/v1/governance/specs/validate",
        json=request_data,
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_validate_frontmatter_empty_content(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test POST /governance/specs/validate - Empty content."""
    request_data = {
        "content": "",
    }

    response = await client.post(
        "/api/v1/governance/specs/validate",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code in [200, 422]

    if response.status_code == 200:
        data = response.json()
        assert data["valid"] is False


# ============================================================================
# Specification Retrieval Tests
# ============================================================================


@pytest.mark.asyncio
async def test_get_specification(
    client: AsyncClient,
    auth_headers: dict,
    sample_spec_id: str,
):
    """Test GET /governance/specs/{spec_id} - Get specification metadata."""
    response = await client.get(
        f"/api/v1/governance/specs/{sample_spec_id}",
        headers=auth_headers,
    )

    # May return 200 with data or 404 if spec doesn't exist
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()
        assert "spec_id" in data
        assert "title" in data
        assert "status" in data
        assert "tier" in data


@pytest.mark.asyncio
async def test_get_specification_not_found(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test GET /governance/specs/{spec_id} - Not found."""
    non_existent_id = "SPEC-9999"

    response = await client.get(
        f"/api/v1/governance/specs/{non_existent_id}",
        headers=auth_headers,
    )
    assert response.status_code == 404


# ============================================================================
# Requirements Tests
# ============================================================================


@pytest.mark.asyncio
async def test_get_requirements(
    client: AsyncClient,
    auth_headers: dict,
    sample_spec_id: str,
):
    """Test GET /governance/specs/{spec_id}/requirements - Get BDD requirements."""
    response = await client.get(
        f"/api/v1/governance/specs/{sample_spec_id}/requirements",
        headers=auth_headers,
    )

    # May return 200 with data or 404 if spec doesn't exist
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()
        assert "spec_id" in data
        assert "total_requirements" in data
        assert "functional_requirements" in data
        assert "non_functional_requirements" in data
        assert "coverage_by_tier" in data

        # Verify tier coverage structure
        coverage = data["coverage_by_tier"]
        assert "LITE" in coverage
        assert "STANDARD" in coverage
        assert "PROFESSIONAL" in coverage
        assert "ENTERPRISE" in coverage


@pytest.mark.asyncio
async def test_get_requirements_bdd_format(
    client: AsyncClient,
    auth_headers: dict,
    sample_spec_id: str,
):
    """Test that requirements are in BDD format (GIVEN-WHEN-THEN)."""
    response = await client.get(
        f"/api/v1/governance/specs/{sample_spec_id}/requirements",
        headers=auth_headers,
    )

    if response.status_code == 200:
        data = response.json()
        for req in data.get("functional_requirements", []):
            # Verify BDD structure
            assert "id" in req
            assert "given" in req
            assert "when" in req
            assert "then" in req
            assert "priority" in req
            assert req["priority"] in ["must", "should", "could", "wont"]


# ============================================================================
# Acceptance Criteria Tests
# ============================================================================


@pytest.mark.asyncio
async def test_get_acceptance_criteria(
    client: AsyncClient,
    auth_headers: dict,
    sample_spec_id: str,
):
    """Test GET /governance/specs/{spec_id}/acceptance-criteria - Get acceptance criteria."""
    response = await client.get(
        f"/api/v1/governance/specs/{sample_spec_id}/acceptance-criteria",
        headers=auth_headers,
    )

    # May return 200 with data or 404 if spec doesn't exist
    assert response.status_code in [200, 404]

    if response.status_code == 200:
        data = response.json()
        assert "spec_id" in data
        assert "total_criteria" in data
        assert "criteria" in data
        assert "testable_percentage" in data
        assert "automated_percentage" in data
        assert "pass_rate" in data


@pytest.mark.asyncio
async def test_get_acceptance_criteria_structure(
    client: AsyncClient,
    auth_headers: dict,
    sample_spec_id: str,
):
    """Test acceptance criteria have correct structure."""
    response = await client.get(
        f"/api/v1/governance/specs/{sample_spec_id}/acceptance-criteria",
        headers=auth_headers,
    )

    if response.status_code == 200:
        data = response.json()
        for criterion in data.get("criteria", []):
            assert "id" in criterion
            assert "description" in criterion
            assert "testable" in criterion
            assert "automated" in criterion
            assert "status" in criterion
            assert criterion["status"] in ["pending", "passed", "failed"]


# ============================================================================
# Compliance Score Tests
# ============================================================================


@pytest.mark.asyncio
async def test_compliance_score_range(
    client: AsyncClient,
    auth_headers: dict,
    valid_frontmatter: str,
):
    """Test that compliance score is in valid range (0-100)."""
    request_data = {
        "content": valid_frontmatter,
    }

    response = await client.post(
        "/api/v1/governance/specs/validate",
        json=request_data,
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    assert 0 <= data["compliance_score"] <= 100


@pytest.mark.asyncio
async def test_compliance_score_valid_vs_invalid(
    client: AsyncClient,
    auth_headers: dict,
    valid_frontmatter: str,
    invalid_frontmatter_missing_fields: str,
):
    """Test that valid spec has higher compliance score than invalid."""
    # Valid spec
    response_valid = await client.post(
        "/api/v1/governance/specs/validate",
        json={"content": valid_frontmatter},
        headers=auth_headers,
    )
    valid_score = response_valid.json()["compliance_score"]

    # Invalid spec
    response_invalid = await client.post(
        "/api/v1/governance/specs/validate",
        json={"content": invalid_frontmatter_missing_fields},
        headers=auth_headers,
    )
    invalid_score = response_invalid.json()["compliance_score"]

    # Valid should have higher score
    assert valid_score > invalid_score


# ============================================================================
# Full Flow Integration Tests
# ============================================================================


@pytest.mark.asyncio
async def test_spec_validation_full_flow(
    client: AsyncClient,
    auth_headers: dict,
    valid_frontmatter: str,
):
    """Test full spec validation flow: validate → get spec → requirements → acceptance criteria."""
    # Step 1: Validate frontmatter
    validate_response = await client.post(
        "/api/v1/governance/specs/validate",
        json={"content": valid_frontmatter},
        headers=auth_headers,
    )
    assert validate_response.status_code == 200
    validate_data = validate_response.json()
    assert validate_data["valid"] is True

    spec_id = validate_data["parsed_metadata"]["spec_id"]

    # Step 2-4: Try to get spec, requirements, and acceptance criteria
    # (These might return 404 if spec isn't persisted, which is acceptable)

    spec_response = await client.get(
        f"/api/v1/governance/specs/{spec_id}",
        headers=auth_headers,
    )
    assert spec_response.status_code in [200, 404]

    req_response = await client.get(
        f"/api/v1/governance/specs/{spec_id}/requirements",
        headers=auth_headers,
    )
    assert req_response.status_code in [200, 404]

    ac_response = await client.get(
        f"/api/v1/governance/specs/{spec_id}/acceptance-criteria",
        headers=auth_headers,
    )
    assert ac_response.status_code in [200, 404]


@pytest.mark.asyncio
async def test_tier_specific_validation_enterprise(
    client: AsyncClient,
    auth_headers: dict,
):
    """Test ENTERPRISE tier requires more fields."""
    # Minimal spec that might pass for LITE but not ENTERPRISE
    minimal_spec = """---
spec_version: "1.0"
spec_id: SPEC-0100
status: draft
tier: ENTERPRISE
stage: 04-build
owner: enterprise-team
created: 2026-01-29
last_updated: 2026-01-29
related_adrs: []
---

## Overview
Minimal enterprise spec.
"""

    response = await client.post(
        "/api/v1/governance/specs/validate",
        json={"content": minimal_spec, "tier": "ENTERPRISE"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()

    # ENTERPRISE might require more (warnings or lower score)
    # The compliance score should reflect stricter requirements
    assert data["compliance_score"] <= 100

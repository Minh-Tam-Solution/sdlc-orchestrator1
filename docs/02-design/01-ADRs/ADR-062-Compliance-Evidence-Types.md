---
sdlc_version: "6.1.0"
document_type: "Architecture Decision Record"
status: "DRAFT"
adr_id: "ADR-062"
spec_id: "ADR-062"
tier: "ENTERPRISE"
stage: "02 - Design"
sprint: "182"
---

# ADR-062: Compliance Evidence Types

**Status**: DRAFT (Sprint 182) → APPROVED (Sprint 183 finalization)
**Date**: February 19, 2026
**Author**: Architect (@architect)
**Reviewers**: CTO, Compliance Lead
**Supersedes**: None
**Follow-up**: SOC2 Evidence Pack Generator (Sprint 185), HIPAA Pack (Sprint 185)
**Implementation Sprint**: Sprint 183

---

## Context

The Evidence Vault (`gate_evidence` table + EvidenceType enum) was designed in Sprint 1 with general-purpose evidence types. As SDLC Orchestrator targets enterprise customers with compliance requirements (SOC2, HIPAA, NIST AI RMF, ISO 27001), evidence stored in the vault needs to be classifiable by compliance framework.

**Problem**: There is no way to query "show me all SOC2 evidence" — the existing COMPLIANCE enum value is too broad.

**Business driver**: Enterprise sales requires demonstrable compliance evidence management (Q3 2026 target per ADR-059). SOC2 Type II report generation (Sprint 185) requires typed evidence.

---

## Decision Table

| # | Decision | Owner | Status |
|---|----------|-------|--------|
| D-1 | Extend EvidenceType enum with 4 compliance-specific values | Tech Lead | LOCKED |
| D-2 | PostgreSQL ALTER TYPE ADD VALUE (irreversible, acceptable) | Architect | LOCKED |
| D-3 | Existing COMPLIANCE enum value retained (not replaced) | Architect | LOCKED |
| D-4 | Evidence routing: compliance_type filter parameter on GET /evidence | Tech Lead | LOCKED |

---

## Decision Details

### D-1: 4 New EvidenceType Values

```python
class EvidenceType(str, Enum):
    # Existing (Sprint 1-178 — NOT changed)
    DESIGN_DOCUMENT  = "DESIGN_DOCUMENT"
    TEST_RESULTS     = "TEST_RESULTS"
    CODE_REVIEW      = "CODE_REVIEW"
    DEPLOYMENT_PROOF = "DEPLOYMENT_PROOF"
    DOCUMENTATION    = "DOCUMENTATION"
    COMPLIANCE       = "COMPLIANCE"   # Generic — kept for backward compatibility

    # New (Sprint 183, ADR-062)
    SOC2_CONTROL = "SOC2_CONTROL"
    # Maps to: SOC2 Trust Service Criteria (CC1-CC9, A1, C1, PI1, P1-P8)
    # Used for: policy evaluations, access reviews, change management evidence

    HIPAA_AUDIT = "HIPAA_AUDIT"
    # Maps to: HIPAA Security Rule (§164.308-§164.316) + Privacy Rule audit logs
    # Used for: PHI access logs, minimum-necessary access records, BAA tracking

    NIST_AI_RMF = "NIST_AI_RMF"
    # Maps to: NIST AI Risk Management Framework (GOVERN, MAP, MEASURE, MANAGE)
    # Used for: AI model cards, bias assessments, safety evaluations, incident logs

    ISO27001 = "ISO27001"
    # Maps to: ISO 27001:2022 Annex A controls (93 controls in 4 categories)
    # Used for: information security policy, asset management, access control records
```

### D-2: PostgreSQL Migration Strategy

```sql
-- s183_002_compliance_evidence_types.py
-- PostgreSQL ALTER TYPE ADD VALUE is irreversible in active transactions
-- Acceptable because:
--   (a) New values never conflict with existing data
--   (b) Downgrade is no-op with logged WARNING (not data loss)

ALTER TYPE evidencetype ADD VALUE IF NOT EXISTS 'SOC2_CONTROL';
ALTER TYPE evidencetype ADD VALUE IF NOT EXISTS 'HIPAA_AUDIT';
ALTER TYPE evidencetype ADD VALUE IF NOT EXISTS 'NIST_AI_RMF';
ALTER TYPE evidencetype ADD VALUE IF NOT EXISTS 'ISO27001';
```

**Alembic implementation**:
```python
def upgrade():
    for value in ['SOC2_CONTROL', 'HIPAA_AUDIT', 'NIST_AI_RMF', 'ISO27001']:
        op.execute(f"ALTER TYPE evidencetype ADD VALUE IF NOT EXISTS '{value}'")

def downgrade():
    # PostgreSQL cannot remove enum values — downgrade is intentional no-op
    import logging
    logging.getLogger(__name__).warning(
        "s183_002 downgrade: PostgreSQL cannot remove enum values. "
        "SOC2_CONTROL/HIPAA_AUDIT/NIST_AI_RMF/ISO27001 remain in DB. "
        "Application code handles missing values gracefully."
    )
```

### D-3: COMPLIANCE Value Retention

The generic `COMPLIANCE` value is retained for:
- Backward compatibility (existing compliance evidence records)
- General compliance artifacts that don't map to a specific framework
- Migration guide: instruct users to re-classify existing COMPLIANCE records if they know the framework

### D-4: Evidence API Filter

```python
# GET /api/v1/evidence?compliance_type=SOC2_CONTROL,HIPAA_AUDIT
@router.get("/evidence", response_model=list[EvidenceResponse])
async def list_evidence(
    gate_id: int | None = None,
    compliance_type: str | None = Query(None, description="Comma-separated compliance types"),
    db: AsyncSession = Depends(get_db),
):
    compliance_types = compliance_type.split(",") if compliance_type else None
    # Apply filter if compliance_type provided
    if compliance_types:
        stmt = stmt.where(GateEvidence.evidence_type.in_(compliance_types))
```

---

## Compliance Framework Mappings

### SOC2_CONTROL → Trust Service Criteria

| TSC Category | Criteria | Example Evidence |
|-------------|----------|-----------------|
| CC1 (Control Environment) | CC1.1-CC1.5 | Policy documents, org structure, ethics training |
| CC6 (Logical Access) | CC6.1-CC6.8 | Access review records, RBAC gate evaluations |
| CC7 (System Operations) | CC7.1-CC7.5 | Change management records, incident response |
| CC8 (Change Management) | CC8.1 | Sprint close gates, code review evidence |
| A1 (Availability) | A1.1-A1.3 | SLA monitoring, uptime reports |

### HIPAA_AUDIT → HIPAA Security Rule

| Rule Section | Description | Example Evidence |
|-------------|-------------|-----------------|
| §164.308(a)(1) | Risk Analysis | Threat model documents (STM-056) |
| §164.308(a)(3) | Workforce Training | Security training completion records |
| §164.312(b) | Audit Controls | System access logs, PHI access records |
| §164.308(a)(5) | Security Awareness | Security review evidence |

### NIST_AI_RMF → Framework Functions

| Function | Description | Example Evidence |
|----------|-------------|-----------------|
| GOVERN | AI governance policies | nist_govern.py route outputs |
| MAP | AI context identification | AI model cards, risk assessments |
| MEASURE | Bias/fairness metrics | Model evaluation reports |
| MANAGE | Risk response records | Incident logs, remediation evidence |

### ISO27001 → Annex A Controls (ISO 27001:2022)

| Category | Controls | Example Evidence |
|----------|----------|-----------------|
| 5. Organizational Controls | 5.1-5.37 | Information security policies |
| 6. People Controls | 6.1-6.8 | Background check records |
| 7. Physical Controls | 7.1-7.14 | Data center access logs |
| 8. Technological Controls | 8.1-8.34 | Encryption key management, SAST reports |

---

## Alternatives Considered

### Option A (SELECTED): Extend EvidenceType Enum

**Pros**: Simple, SQL-queryable, type-safe in Python, no new table needed
**Cons**: PostgreSQL enum ADD VALUE is irreversible (acceptable, as noted in D-2)

### Option B (REJECTED): Separate `compliance_framework` JSONB column on gate_evidence

**Why rejected**:
- JSONB is not type-safe — can store arbitrary strings including typos
- Cannot create PostgreSQL foreign key constraint on JSONB
- Query performance: JSONB path operators slower than enum equality
- Evidence type already captures most of the needed information

### Option C (REJECTED): New `compliance_evidence` table (separate from gate_evidence)

**Why rejected**:
- Gate evidence is already the source of truth for all evidence
- Duplicating into a separate table creates sync complexity
- Breaks existing evidence API consumers
- No business requirement for separate storage

---

## Non-Goals

- **Compliance validation logic**: ADR-062 only covers CLASSIFICATION (what type of evidence). Validation (does this SOC2_CONTROL evidence actually pass criteria CC6.1?) is Sprint 185's SOC2 Pack Generator.
- **Evidence re-classification UI**: Manual re-classification of existing COMPLIANCE records is out of scope. Provide migration guide documentation only.
- **Automatic mapping**: Do not auto-assign compliance types based on content analysis. Human assigns compliance type at upload time.

---

## Consequences

**Positive**:
- SOC2 evidence pack generator (Sprint 185) has typed evidence to query
- Compliance dashboard can show "X SOC2 controls, Y HIPAA records, Z NIST assessments"
- Enterprise customers can filter evidence by compliance framework
- No new table needed — minimal schema change

**Negative**:
- PostgreSQL enum ADD VALUE is irreversible (downgrade is no-op) — acceptable trade-off
- Existing evidence with type=COMPLIANCE remains generic until manually re-classified
- Alembic downgrade emits WARNING (not ERROR) — team must understand this is intentional

---

## References

- [ERD v3.5.0](../01-planning/04-Data-Model/Data-Model-ERD.md) — gate_evidence table (EvidenceType enum)
- [API Spec v3.7.0](../01-planning/05-API-Design/API-Specification.md) — GET /evidence compliance_type filter
- [ADR-059](ADR-059-Enterprise-First-Refocus.md) — ENTERPRISE compliance requirements
- [NIST AI RMF](https://www.nist.gov/system/files/documents/2023/01/26/AI%20RMF%201.0.pdf) — Framework reference
- [SOC2 Trust Service Criteria](https://www.aicpa.org/resources/article/2017-trust-services-criteria) — Criteria reference

---

## Document Control

**Version History**:
- v0.1.0 (February 19, 2026): DRAFT — 4 decisions initially locked (Sprint 182)
- v1.0.0 (Sprint 183): APPROVED — final implementation confirmed

**Status**: DRAFT → APPROVED in Sprint 183
**Implementation Sprint**: Sprint 183 (s183_002 migration)

# Sprint 115 Track 2: SOFT Mode Enforcement

**Sprint:** Sprint 115 (Feb 10-14, 2026)
**Track:** Track 2 - Anti-Vibecoding SOFT Enforcement
**Capacity:** 60% (Product Survival priority)
**Prepared:** January 28, 2026 (13 days early)
**Status:** READY FOR DEPLOYMENT

---

## Executive Summary

Sprint 115 Track 2 implements SOFT mode enforcement for the Anti-Vibecoding Governance system. Following the Sprint 114 GO Decision (4.0 min friction, 6.7% FP rate, 75% satisfaction), we transition from WARNING (observation) to SOFT (partial blocking).

**SOFT Mode Rules:**
- **RED (81-100):** BLOCKED (CTO override required)
- **ORANGE (61-80):** WARNED (CEO review recommended)
- **YELLOW (31-60):** PASSED (Tech Lead review suggested)
- **GREEN (0-30):** AUTO-APPROVED

**Expected Metrics:**
- Blocked PRs: <5% (critical only)
- Developer Friction: <8 min (accounting for blocks)
- False Positive Rate: <10% (with exemptions)
- First Pass Rate: >80%

---

## Deliverables Inventory

### Infrastructure Delivered (Prepared Jan 28)

| Component | File | LOC | Status |
|-----------|------|-----|--------|
| SOFT Mode Configuration | `governance_soft_mode.yaml` | 185 | READY |
| SOFT Mode Enforcer Service | `soft_mode_enforcer.py` | 850 | READY |
| Unit Tests | `test_soft_mode_enforcer.py` | 450 | 23/23 PASS |
| API Endpoints | `dogfooding.py` additions | 250 | READY |
| Environment Config | `.env.example` updates | 30 | READY |
| **Total** | **5 files** | **1,765** | READY |

### API Endpoints Added

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/dogfooding/enforce/soft` | POST | Evaluate PR against SOFT mode |
| `/dogfooding/enforce/soft/status` | GET | Get SOFT mode config/metrics |
| `/dogfooding/enforce/soft/log` | GET | View enforcement log (auth) |
| `/dogfooding/enforce/soft/override` | POST | Request CTO override (auth) |

---

## Configuration Details

### Signal Weights (Adjusted from Sprint 114)

| Signal | Weight | Change | Reason |
|--------|--------|--------|--------|
| architectural_smell | 0.25 | - | God class, feature envy detection |
| abstraction_complexity | 0.15 | - | Inheritance depth, generics |
| ai_dependency_ratio | 0.20 | - | AI lines / total lines |
| change_surface_area | 0.25 | +0.05 | More weight on large changes |
| drift_velocity | 0.15 | -0.05 | Reduced for dependency updates |

### Exemption Rules (Reduce False Positives)

| Exemption | Trigger | Effect |
|-----------|---------|--------|
| dependency_update_exemption | All files are package.json, requirements.txt, etc | drift_velocity x0.5, max index 40 |
| documentation_safe_pattern | All files in docs/, index < 25 | Force green zone, auto-approve |
| test_only_pattern | All files are tests | abstraction x0.5, ai_dependency x0.7 |

### Block Rules (SOFT Mode)

| Rule | Condition | Override |
|------|-----------|----------|
| vibecoding_index_red | Index >= 81 | CTO override allowed |
| missing_ownership | No @owner annotation | Not allowed |
| missing_intent | No intent statement | Not allowed |
| security_scan_fail | Critical CVEs > 0 | CTO + Security Lead |

### Warn Rules (SOFT Mode)

| Rule | Condition | Action |
|------|-----------|--------|
| vibecoding_index_orange | 61 <= Index <= 80 | CEO review recommended |
| missing_adr_linkage | New feature, no ADR | Warning logged |
| low_test_coverage | Coverage < 80% | Warning logged |

---

## Deployment Plan

### Day 1 (Feb 10): Enable SOFT Mode

```bash
# Update environment
export GOVERNANCE_MODE=soft

# Verify configuration
curl http://localhost:8000/api/v1/dogfooding/enforce/soft/status

# Expected response:
{
  "mode": "soft",
  "active": true,
  "sprint": "115",
  "configuration": {
    "exemptions_enabled": ["dependency_update_exemption", ...]
  }
}
```

### Day 2-3: Monitor First Blocks

1. Track blocked PRs in `/dogfooding/enforce/soft/log`
2. Monitor rejection rate (target: <5%)
3. Collect developer feedback on blocks
4. Process CTO override requests

### Day 4: Mid-Sprint Calibration

1. Review false positive reports
2. Adjust thresholds if FP rate > 10%
3. Update exemption rules if needed
4. Communicate changes to team

### Day 5: Sprint 115 Go/No-Go Decision

**Criteria for FULL Mode (Sprint 116):**

| Metric | Target | Measurement |
|--------|--------|-------------|
| Blocked PRs | <5% | Total blocked / Total PRs |
| Developer Friction | <8 min | Average time to comply |
| False Positive Rate | <10% | FP reports / Total blocked |
| CTO Override Rate | <2% | Overrides / Total blocked |

---

## Rollback Plan

### Kill Switch Triggers (Auto-Rollback)

| Condition | Threshold | Action |
|-----------|-----------|--------|
| Rejection rate | >80% | Rollback to WARNING |
| Latency P95 | >500ms | Rollback to WARNING |
| False positive rate | >20% | Rollback to WARNING |
| Developer complaints | >5/day | Rollback to WARNING |

### Manual Rollback

```bash
# CTO/CEO can trigger manual rollback
curl -X POST http://localhost:8000/api/v1/governance/mode \
  -H "Authorization: Bearer $CTO_TOKEN" \
  -d '{"mode": "warning", "reason": "Manual rollback for investigation"}'
```

---

## Success Criteria

### Sprint 115 Track 2 GO Decision (Feb 14)

| Criterion | Target | Weight |
|-----------|--------|--------|
| Developer Friction | <8 min | 30% |
| False Positive Rate | <10% | 25% |
| Team Satisfaction | >70% | 25% |
| Critical Bugs | 0 | 20% |

**Decision:**
- **GO:** Proceed to Sprint 116 FULL mode
- **NO-GO:** Extend SOFT mode, calibrate thresholds

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ GitHub Actions / PR Webhook                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ POST /dogfooding/enforce/soft                                    │
│                                                                   │
│ Request:                                                         │
│ {                                                                │
│   "pr_number": 234,                                              │
│   "vibecoding_index": 72.5,                                      │
│   "zone": "orange",                                              │
│   "has_ownership": true,                                         │
│   "has_intent": true,                                            │
│   "files_changed": ["backend/app/services/auth.py", ...],      │
│   "security_scan_critical": 0                                    │
│ }                                                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ SoftModeEnforcer.enforce()                                       │
│                                                                   │
│ 1. Evaluate exemptions (dependency, docs, test)                  │
│ 2. Apply exemption adjustments to index                          │
│ 3. Evaluate block rules (RED, ownership, intent, security)      │
│ 4. Evaluate warn rules (ORANGE, ADR, coverage)                  │
│ 5. Determine action (BLOCKED/WARNED/APPROVED/AUTO_APPROVED)     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Response:                                                        │
│ {                                                                │
│   "pr_number": 234,                                              │
│   "allowed": true,                                               │
│   "action": "warn",                                              │
│   "vibecoding_index": 72.5,                                      │
│   "zone": "orange",                                              │
│   "routing": "ceo_should_review",                                │
│   "exemptions_applied": [],                                      │
│   "block_reasons": [],                                           │
│   "warn_reasons": ["Warning: Vibecoding Index 72.5 in orange..."]│
│   "cto_override_available": false,                               │
│   "message": "PR #234 WARNED: Review recommended..."             │
│ }                                                                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ GitHub Check / CI Status                                         │
│ - PASSED (allowed=true)                                          │
│ - WARNING annotation added                                       │
│ - CEO notified for review                                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Related Documents

- [SPRINT-114-TRACK-2-COMPLETION.md](SPRINT-114-TRACK-2-COMPLETION.md) - GO Decision
- [governance_soft_mode.yaml](../../../backend/app/config/governance_soft_mode.yaml) - Configuration
- [soft_mode_enforcer.py](../../../backend/app/services/governance/soft_mode_enforcer.py) - Service
- [test_soft_mode_enforcer.py](../../../backend/tests/unit/services/governance/test_soft_mode_enforcer.py) - Tests

---

## Sign-off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| CTO | - | Jan 28, 2026 | Pending |
| CPO | - | Jan 28, 2026 | Pending |
| Tech Lead | - | Jan 28, 2026 | Pending |

---

**Document Status:** READY FOR DEPLOYMENT
**Last Updated:** January 28, 2026
**Author:** AI Development Partner
**Reviewer:** CTO (Pending)

---

*Sprint 115 Track 2 - SOFT Mode Enforcement*
*"GOVERNANCE MUST BE THE FASTEST WAY"*

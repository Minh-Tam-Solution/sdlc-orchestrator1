# Vibecoding V1/V2 Consolidation Analysis

**Sprint**: S149 - V2 API Finalization
**Date**: February 18, 2026
**Status**: 🔄 IN PROGRESS

---

## Executive Summary

Two Vibecoding implementations exist with **different signal definitions** and **different thresholds**:

| Aspect | `vibecoding_service.py` (V1) | `signals_engine.py` (V2) |
|--------|------------------------------|--------------------------|
| **LOC** | 614 | 1,160 |
| **Sprint** | 118 | 109 |
| **Signals** | 5 (intent-based) | 5 (code-based) |
| **Thresholds** | 0-20-40-60-100 | 0-30-60-80-100 |
| **Override** | No | MAX CRITICALITY |
| **Analysis** | Database-driven | AST analysis |

**Recommendation**: Merge into unified service keeping V2 thresholds and MAX CRITICALITY.

---

## Signal Comparison

### V1 Signals (`vibecoding_service.py`)

| Signal | Weight | Description |
|--------|--------|-------------|
| `intent_clarity` | 30% | How clear is the intent? |
| `code_ownership` | 25% | Who owns this code? |
| `context_completeness` | 20% | Is context sufficient? |
| `ai_attestation` | 15% | Is AI-generated code attested? |
| `rejection_rate` | 10% | Historical rejection rate |

**Total**: 100% (5 signals)
**Focus**: Human intent & ownership

### V2 Signals (`signals_engine.py`)

| Signal | Weight | Description |
|--------|--------|-------------|
| `architectural_smell` | 25% | God class, feature envy, shotgun surgery |
| `abstraction_complexity` | 15% | Inheritance depth, interface count |
| `ai_dependency_ratio` | 20% | AI-generated lines / total lines |
| `change_surface_area` | 20% | Files, modules, API contracts affected |
| `drift_velocity` | 20% | Pattern changes over 7 days |

**Total**: 100% (5 signals)
**Focus**: Code quality & change impact

---

## Zone Threshold Comparison

| Zone | V1 Range | V2 Range | Action (V1) | Action (V2) |
|------|----------|----------|-------------|-------------|
| **GREEN** | 0-19 | 0-30 | AUTO_MERGE | Auto-approve |
| **YELLOW** | 20-39 | 31-60 | HUMAN_REVIEW | Tech Lead review |
| **ORANGE** | 40-59 | 61-80 | SENIOR_REVIEW | CEO should review |
| **RED** | 60-100 | 81-100 | BLOCK | CEO must review |

**Key Difference**: V1 is stricter (RED starts at 60), V2 is more lenient (RED starts at 81).

---

## Consolidation Plan

### Phase 1: Unified Service Creation

Create `vibecoding_unified_service.py` combining both implementations:

```python
class VibecodeUnifiedService:
    """
    Unified Vibecoding service (Sprint 149).

    Combines:
    - V1 intent-based signals (vibecoding_service.py)
    - V2 code-based signals (signals_engine.py)
    - MAX CRITICALITY override (V2)

    Signal Weights (10 total signals):
    - Intent signals (V1): 40%
    - Code signals (V2): 60%

    Thresholds: V2 (0-30-60-80-100)
    """

    # Combined 10-signal weights
    SIGNAL_WEIGHTS = {
        # V1 intent signals (40% total)
        "intent_clarity": 0.12,       # 30% of 40%
        "code_ownership": 0.10,       # 25% of 40%
        "context_completeness": 0.08, # 20% of 40%
        "ai_attestation": 0.06,       # 15% of 40%
        "rejection_rate": 0.04,       # 10% of 40%

        # V2 code signals (60% total)
        "architectural_smell": 0.15,     # 25% of 60%
        "abstraction_complexity": 0.09,  # 15% of 60%
        "ai_dependency_ratio": 0.12,     # 20% of 60%
        "change_surface_area": 0.12,     # 20% of 60%
        "drift_velocity": 0.12,          # 20% of 60%
    }

    # V2 thresholds (more lenient)
    ZONE_THRESHOLDS = {
        "GREEN": (0, 30),
        "YELLOW": (31, 60),
        "ORANGE": (61, 80),
        "RED": (81, 100),
    }

    # MAX CRITICALITY: Critical paths → minimum RED
    CRITICAL_PATHS = [
        "**/auth/**",
        "**/security/**",
        "**/payment/**",
        "**/api/routes/admin*.py",
    ]
```

### Phase 2: Migration Steps

1. **Create unified service** (Day 2)
   - Combine signal calculations
   - Keep V2 thresholds
   - Add MAX CRITICALITY

2. **Update routes** (Day 2)
   - Deprecate V1 endpoints
   - Update V2 endpoints to use unified service

3. **Deprecate old services** (Day 3)
   - Mark `vibecoding_service.py` as deprecated
   - Keep `signals_engine.py` for MAX CRITICALITY logic

4. **Delete deprecated** (Sprint 153+)
   - Remove old service files
   - Update documentation

---

## File Changes

### New Files
| File | Purpose | LOC |
|------|---------|-----|
| `backend/app/services/governance/vibecoding_unified.py` | Unified service | ~800 |

### Deprecated Files
| File | Status | Delete After |
|------|--------|--------------|
| `vibecoding_service.py` | Deprecate | Sprint 153 |

### Keep Files
| File | Reason |
|------|--------|
| `signals_engine.py` | MAX CRITICALITY + AST analysis |

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Breaking existing calculations | HIGH | MEDIUM | A/B testing old vs new |
| Threshold changes affect routing | MEDIUM | HIGH | Gradual rollout |
| Signal weight rebalancing | MEDIUM | MEDIUM | Monitor index distribution |

---

## Exit Criteria

- [ ] Unified service created (~800 LOC)
- [ ] 10-signal calculation working
- [ ] V2 thresholds applied
- [ ] MAX CRITICALITY preserved
- [ ] V1 routes deprecated
- [ ] 25 unit tests passing
- [ ] A/B comparison with old implementation

---

**Analysis Complete**: February 18, 2026
**Next Step**: Implement unified service

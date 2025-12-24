# Q2 2026 DeepCode Provider Decision Gate
## EP-06 Third Provider Evaluation Criteria

---

**Document Information**

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Status** | DRAFT |
| **Created** | December 24, 2025 |
| **Sprint** | Sprint 50 - EP-06 Productization |
| **Decision Date** | April 2026 (Q2) |
| **Decision Owner** | CTO |
| **Stakeholders** | CEO, CPO, Backend Lead, DevOps |

---

## Executive Summary

This document defines the Go/No-Go criteria for adding DeepCode as a third provider in the EP-06 codegen engine. The decision will be made at the end of Q1 2026 (April) based on:

1. EP-06 pilot program success
2. Ollama + Claude performance metrics
3. DeepCode capabilities and cost
4. Strategic alignment

---

## Current Provider Architecture (As of Sprint 50)

### Production Lineup (December 2025)

| Priority | Provider | Model | Latency (p95) | Cost/Month | Status |
|----------|----------|-------|---------------|------------|--------|
| **Primary** | Ollama | qwen3-coder:30b | <15s | ~$50 | ✅ Active |
| **Fallback 1** | Claude | claude-sonnet-4 | <25s | ~$1000 | ✅ Active |
| **Fallback 2** | DeepCode | TBD | TBD | TBD | ⏳ Q2 Decision |

### Provider Performance (Target vs Actual)

| Metric | Target | Ollama | Claude |
|--------|--------|--------|--------|
| Latency (p95) | <15s / <25s | TBD | TBD |
| Quality Gate Pass | >95% | TBD | TBD |
| Availability | >99.5% | TBD | TBD |
| Fallback Rate | <5% | N/A | TBD |

---

## Decision Criteria

### 1. EP-06 Pilot Success (Weight: 40%)

| Metric | Threshold | Impact |
|--------|-----------|--------|
| **Pilot Completion** | ≥8/10 founders | Required |
| **TTFV** | <30 min median | Required |
| **Satisfaction** | ≥8/10 average | Required |
| **Quality Gate Pass** | ≥95% | Required |
| **Retention** | ≥80% active after 30 days | Recommended |

**Decision Logic:**
- If EP-06 meets ALL required thresholds → **Proceed** with current providers
- If EP-06 fails 1+ required thresholds → **Evaluate** if DeepCode can help

### 2. Current Provider Performance (Weight: 30%)

| Metric | Threshold | Implication |
|--------|-----------|-------------|
| **Ollama Latency** | <15s p95 | If exceeded, DeepCode may help |
| **Claude Fallback Rate** | <5% | If exceeded, need 3rd option |
| **Quality Consistency** | ±5% variance | If exceeded, diversify providers |
| **Cost Efficiency** | <$100/month | If exceeded, optimize |

**Decision Logic:**
- If current providers meet ALL thresholds → **DeepCode not needed**
- If Ollama underperforms → **Evaluate** DeepCode as primary replacement
- If Claude fallback too frequent → **Evaluate** DeepCode as Fallback 1

### 3. DeepCode Capabilities (Weight: 20%)

| Requirement | Status | Notes |
|-------------|--------|-------|
| Vietnamese language support | TBD | Critical for SME market |
| Code quality (HumanEval) | TBD | Must be ≥90% |
| Response latency | TBD | Must be <20s p95 |
| API stability | TBD | Must have SLA |
| Cost model | TBD | Must be predictable |
| Integration effort | TBD | Estimate in sprint points |

**Evaluation Timeline:**
- **March 2026**: Technical evaluation (sandbox testing)
- **April 2026**: Decision based on results

### 4. Strategic Alignment (Weight: 10%)

| Factor | Consideration |
|--------|---------------|
| **Vendor Diversity** | Reduce dependency on single provider |
| **Vietnam Focus** | DeepCode may have better Vietnamese tuning |
| **Cost Structure** | Fixed vs usage-based pricing |
| **Future Roadmap** | Provider's investment in code generation |
| **Security/Compliance** | Data residency, SOC 2, etc. |

---

## Decision Matrix

### Scenario A: EP-06 Full Success

| Condition | Action |
|-----------|--------|
| All pilot metrics met | Continue with Ollama + Claude |
| Ollama stable (<5% fallback) | DeepCode **not needed** |
| Cost within budget | No action required |

**Recommendation**: NO-GO for DeepCode (revisit Q4 2026)

### Scenario B: EP-06 Partial Success

| Condition | Action |
|-----------|--------|
| 6-7/10 satisfaction | Investigate root causes |
| TTFV borderline (30-45 min) | Evaluate faster providers |
| Quality issues | Consider provider alternatives |

**Recommendation**: EVALUATE DeepCode (pilot in Q2)

### Scenario C: Provider Performance Issues

| Condition | Action |
|-----------|--------|
| Ollama >15% fallback rate | DeepCode as potential primary |
| Claude costs exceeding $1500/mo | DeepCode as cost alternative |
| Quality variance >10% | Diversify provider pool |

**Recommendation**: GO for DeepCode (accelerated timeline)

### Scenario D: EP-06 Failure

| Condition | Action |
|-----------|--------|
| <5 pilots complete | Re-evaluate entire strategy |
| <6/10 satisfaction | Root cause analysis |
| <80% quality pass | Fundamental issues |

**Recommendation**: PAUSE DeepCode, fix core issues first

---

## Evaluation Process

### Phase 1: Data Collection (Jan-Mar 2026)

```
┌─────────────────────────────────────────────────────────────────────┐
│  WEEK 1-4: Pilot Metrics Collection                                  │
├─────────────────────────────────────────────────────────────────────┤
│  • Daily TTFV aggregation                                            │
│  • Weekly satisfaction surveys                                       │
│  • Continuous quality gate monitoring                                │
│  • Provider performance logging                                      │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  WEEK 5-8: Provider Analysis                                         │
├─────────────────────────────────────────────────────────────────────┤
│  • Ollama latency distribution                                       │
│  • Claude fallback frequency                                         │
│  • Cost tracking by provider                                         │
│  • Error analysis by type                                            │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  WEEK 9-12: DeepCode Technical Eval (if needed)                      │
├─────────────────────────────────────────────────────────────────────┤
│  • Sandbox deployment                                                │
│  • Vietnamese language testing                                       │
│  • Integration prototype                                             │
│  • Cost modeling                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Phase 2: Decision Meeting (April 2026)

**Attendees**: CTO, CEO, CPO, Backend Lead, DevOps Lead

**Agenda**:
1. EP-06 pilot results presentation (30 min)
2. Provider performance review (20 min)
3. DeepCode evaluation findings (20 min)
4. Decision discussion (20 min)
5. Action items (10 min)

**Artifacts Required**:
- Pilot metrics dashboard
- Provider comparison report
- DeepCode POC results (if applicable)
- Cost analysis spreadsheet

---

## Implementation Timeline (If GO)

### Q2 2026: DeepCode Integration

| Week | Activity |
|------|----------|
| 1-2 | DeepCode provider implementation |
| 3-4 | Integration testing |
| 5-6 | Shadow mode deployment |
| 7-8 | Limited rollout (10% traffic) |
| 9-12 | Full rollout (if successful) |

### Resources Required

| Role | Allocation |
|------|------------|
| Backend Developer | 0.5 FTE for 8 weeks |
| DevOps | 0.25 FTE for 4 weeks |
| QA | 0.25 FTE for 4 weeks |

**Estimated Investment**: ~$15,000 (labor) + TBD (DeepCode licensing)

---

## Risk Assessment

### If GO for DeepCode

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Integration complexity | Medium | Medium | Phased rollout |
| Performance issues | Low | High | Shadow mode first |
| Cost overrun | Low | Medium | Usage caps |
| Vendor dependency | Low | Low | Multi-provider strategy |

### If NO-GO for DeepCode

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Ollama single point of failure | Medium | High | Strengthen Claude fallback |
| Claude cost growth | Medium | Medium | Monitor usage |
| Quality stagnation | Low | Medium | Regular model updates |

---

## Success Metrics (If DeepCode Added)

| Metric | Target | Measurement |
|--------|--------|-------------|
| Integration complete | Q2 2026 | ✓/✗ |
| Shadow mode latency | <20s p95 | Prometheus metrics |
| Quality parity | ≥95% gate pass | Dashboard |
| Cost neutral | ≤$200/month additional | Billing |
| Fallback reduction | >50% fewer Claude calls | Metrics |

---

## Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | Dec 24, 2025 | Backend Lead | Initial version |

---

## Appendix A: DeepCode Vendor Information

*To be filled during Q1 2026 evaluation*

| Field | Value |
|-------|-------|
| Vendor Name | DeepCode AI |
| Contact | TBD |
| Pricing Model | TBD |
| SLA | TBD |
| Vietnamese Support | TBD |
| Security Certifications | TBD |

---

## Appendix B: Provider Comparison Template

*To be filled with actual metrics*

| Metric | Ollama | Claude | DeepCode |
|--------|--------|--------|----------|
| Latency (p50) | TBD | TBD | TBD |
| Latency (p95) | TBD | TBD | TBD |
| Quality Pass Rate | TBD | TBD | TBD |
| Vietnamese Quality | TBD | TBD | TBD |
| Cost per Generation | TBD | TBD | TBD |
| Monthly Cost (1000 gen) | TBD | TBD | TBD |

---

*Q2 2026 DeepCode Decision Gate - Data-driven provider strategy.*

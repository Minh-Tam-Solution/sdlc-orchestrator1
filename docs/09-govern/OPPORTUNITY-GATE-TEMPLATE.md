# Opportunity Gate Template

**Purpose**: Every P0/P1 feature MUST pass this gate before development starts  
**Owner**: Product Manager + Tech Lead  
**Rule**: Fail ANY 1 question = Feature goes to backlog

---

## 🚪 OPPORTUNITY GATE CHECKLIST

### Feature Information

| Field | Value |
|-------|-------|
| **Feature Name** | ___________________________ |
| **Requested By** | ___________________________ |
| **Target Sprint** | ___________________________ |
| **Estimated LOC** | ___________________________ |
| **Estimated Days** | ___________________________ |

---

## Gate Questions (All 5 Must Pass)

### Question 1: USER PULL

> "Do we have evidence of user demand?"

**✅ PASS Criteria (one of):**
- [ ] ≥10 customers/POC explicitly requested this feature
- [ ] ≥30% of active teams would use this (survey data)
- [ ] ≥3 LOIs (Letters of Intent) mentioning this feature
- [ ] Support tickets: ≥20 requests in past 90 days

**❌ FAIL if:**
- "We think users want this" (no data)
- "Competitors have this" (not user pull)
- Internal team wants this (not user pull)

**Evidence**: ________________________________________________

**Result**: [ ] PASS  [ ] FAIL

---

### Question 2: TIME-TO-VALUE IMPROVEMENT

> "Does this reduce time to key milestone?"

**✅ PASS Criteria (one of):**
- [ ] Reduces Time-to-First-Project by ≥30%
- [ ] Reduces Time-to-First-Evidence by ≥30%
- [ ] Reduces Time-to-First-Gate-Pass by ≥30%
- [ ] Reduces repetitive task time by ≥50%

**❌ FAIL if:**
- "Nice to have" without measurable improvement
- Adds steps to user journey
- No clear before/after metrics

**Measurement**: Current = _____ min → Target = _____ min

**Result**: [ ] PASS  [ ] FAIL

---

### Question 3: REVENUE IMPACT

> "Does this affect pricing, conversion, or retention?"

**✅ PASS Criteria (one of):**
- [ ] Enables new pricing tier (quantified)
- [ ] Expected conversion lift ≥5% (A/B testable)
- [ ] Expected churn reduction ≥2%
- [ ] Unblocks ≥$50K pipeline revenue

**❌ FAIL if:**
- "Users will like it" (no revenue link)
- Cost center only (no revenue upside)

**Revenue Impact**: $_______ (quantified)

**Result**: [ ] PASS  [ ] FAIL

---

### Question 4: SURFACE AREA

> "What's the security/maintenance cost?"

**✅ PASS Criteria (all of):**
- [ ] New secrets/credentials: ≤2
- [ ] New permissions required: ≤3
- [ ] New API endpoints: ≤10
- [ ] External dependencies: ≤2
- [ ] Estimated maintenance: ≤0.25 FTE/quarter

**❌ FAIL if:**
- Requires OAuth to new provider (high surface)
- Bidirectional sync (complex state)
- New database schema ≥5 tables

**Surface Assessment:**
- Secrets: _____
- Permissions: _____
- Endpoints: _____
- Dependencies: _____
- Maintenance FTE: _____

**Result**: [ ] PASS  [ ] FAIL

---

### Question 5: KILL SWITCH

> "Can we rollback in 1 day if it fails?"

**✅ PASS Criteria (all of):**
- [ ] Feature flag: Can disable in <5 minutes
- [ ] Data rollback: Migration reversible in <1 hour
- [ ] User impact: Graceful degradation (no errors)
- [ ] Dependencies: No downstream breaking changes

**❌ FAIL if:**
- Irreversible data migration
- External system dependency (can't control)
- Breaking API change

**Rollback Plan**: ________________________________________________

**Result**: [ ] PASS  [ ] FAIL

---

## 📋 Gate Summary

| Question | Result |
|----------|--------|
| Q1: User Pull | [ ] PASS  [ ] FAIL |
| Q2: Time-to-Value | [ ] PASS  [ ] FAIL |
| Q3: Revenue | [ ] PASS  [ ] FAIL |
| Q4: Surface Area | [ ] PASS  [ ] FAIL |
| Q5: Kill Switch | [ ] PASS  [ ] FAIL |

---

## Final Verdict

**VERDICT**: [ ] ✅ GO  [ ] ❌ NO-GO

**If NO-GO, reason**: ________________________________________________

---

## Approvals

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Manager | ___________ | ___________ | ___________ |
| Tech Lead | ___________ | ___________ | ___________ |
| CTO (P0 only) | ___________ | ___________ | ___________ |

---

## Example: Discord Adapter (FAILED)

| Question | Result | Evidence |
|----------|--------|----------|
| Q1: User Pull | ❌ FAIL | No customer requests documented |
| Q2: Time-to-Value | ❓ N/A | Unclear improvement |
| Q3: Revenue | ❌ FAIL | No pricing/conversion impact |
| Q4: Surface Area | ⚠️ RISKY | OAuth, new permissions, webhooks |
| Q5: Kill Switch | ✅ PASS | Can disable adapter |

**VERDICT**: ❌ NO-GO (Failed 2/5, 1 unclear)

---

## Example: Product Telemetry (PASSED)

| Question | Result | Evidence |
|----------|--------|----------|
| Q1: User Pull | ✅ PASS | Internal team 100% needs metrics |
| Q2: Time-to-Value | ✅ PASS | Enables data-driven decisions |
| Q3: Revenue | ✅ PASS | Better prioritization = faster growth |
| Q4: Surface Area | ✅ PASS | 1 table, 2 endpoints, no secrets |
| Q5: Kill Switch | ✅ PASS | Can disable tracking anytime |

**VERDICT**: ✅ GO (Passed 5/5)

---

_Template Version: 1.0_  
_Created: February 3, 2026_  
_Owner: CTO Office_

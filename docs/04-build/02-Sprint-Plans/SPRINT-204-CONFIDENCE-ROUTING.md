# Sprint 204 — Confidence-Based Routing + Human Escalation

**Sprint Duration**: May 19 – May 30, 2026 (10 working days)
**Sprint Goal**: Add confidence scoring to `query_classifier.py` and implement human escalation path for low-confidence agent queries via Magic Link approval flow
**Status**: CLOSED — All 4 Tracks Complete ✅ (Feb 25, 2026)
**Priority**: P3 (Confidence-Based Routing)
**Framework**: SDLC 6.1.1
**CTO Score (Sprint 203)**: 9.5/10
**Previous Sprint**: [Sprint 203 — Formal Evaluator-Optimizer + Evals Expansion](SPRINT-203-EVALUATOR-OPTIMIZER-EVALS-EXPANSION.md)

---

## Sprint 204 Goal

Sprint 203 delivers the Evaluator-Optimizer with rubric scoring and expands evals to 15 test cases. Sprint 204 addresses **Gap 3 (P3): Confidence-Based Routing** — the last medium-priority gap from the Anthropic Best Practices roadmap.

**Current state** (`query_classifier.py`):
- Simple substring priority matching (`kw in msg_lower`, no `re` module)
- 3 classification hints: code (priority=10, pattern "```"), reasoning (priority=5, keywords), fast (priority=1, max_length=20)
- `MODEL_ROUTE_HINTS` maps hints to specific Ollama models
- **No confidence score** — classification is binary (match/no-match)
- **No human escalation path** — low-confidence queries still go to LLM
- **No LLM-based classification** — pure substring matching misses nuanced intents

**Target state**:
- `confidence: float` field on `ClassificationResult` (0.0 to 1.0)
- When confidence < 0.6: route to human escalation (Magic Link approval)
- Optional LLM-based classification using `qwen3:8b` (fastest model) for ambiguous queries
- Human escalation reuses existing `magic_link_service.py` (HMAC-SHA256 OOB auth)

**Source**: CTO-approved Anthropic Best Practices Applicability Analysis (9.2/10) — Gap 3 (P3).

---

## Pre-Sprint Blocker Resolution (Feb 25, 2026)

CTO Sprint 204 readiness review identified 4 blockers. All resolved:

### Blocker 1: `MODEL_ROUTE_HINTS` location ✅ RESOLVED

**CTO finding**: grep of `app/core/config.py` found nothing.
**Resolution**: `MODEL_ROUTE_HINTS` is in `app/services/agent_team/config.py:118` (agent_team-scoped config, not app-global config). Current structure:
```python
MODEL_ROUTE_HINTS = {
    "code":      {"*": ("ollama", "qwen3-coder:30b")},
    "reasoning": {"*": ("ollama", "deepseek-r1:32b")},
    "fast":      {"*": ("ollama", "qwen3:8b")},
}
```
Sprint 204 will add: `"governance": {"*": ("__command_router__", "")}` — see Blocker 3 for routing fork design.

### Blocker 2: All `classify()` callers ✅ RESOLVED (only 1)

**CTO concern**: Signature change `str | None` → `ClassificationResult` may have hidden callers.
**Resolution**: Only **one caller** for `query_classifier.classify()`: `team_orchestrator.py:313`. The three `error_classifier.classify()` callers in codegen pipeline (`error_classifier.py`, `retry_strategy.py`) are a completely different function — unaffected.

**Day 1 action**: Update `team_orchestrator.py:313` from:
```python
model_hint = classify(DEFAULT_CLASSIFICATION_RULES, message.content)
# …
invoker = self._build_invoker(definition, model_hint=model_hint)
```
to:
```python
classification = classify(DEFAULT_CLASSIFICATION_RULES, message.content)
if classification.hint == "governance":
    return await self._dispatch_governance_command(message, conversation)
invoker = self._build_invoker(definition, model_hint=classification.hint,
                               confidence=classification.confidence)
```

### Blocker 3: `governance` hint routing target ✅ DESIGN DECIDED

**CTO concern**: `MODEL_ROUTE_HINTS` maps hint → `(provider, model)` — governance doesn't map to a model but to `command_router.py`. These are architecturally different.
**Resolution**: `governance` hint is a **pre-router interceptor**, not a `MODEL_ROUTE_HINTS` entry:
- In `team_orchestrator._process()`, BEFORE calling `_build_invoker()`, check `if hint == "governance"` → `await self._dispatch_governance_command()`
- `_dispatch_governance_command()` delegates to `command_registry.dispatch()` (existing mechanism)
- `MODEL_ROUTE_HINTS` stays clean — no fake `("__command_router__", "")` sentinel needed
- This is architecturally equivalent to the existing `@mention` intercept path (same pre-LLM branch)

### Blocker 4: `run_evals.py` routing schema ✅ DESIGN DECIDED

**CTO concern**: `EvalTestCase` has no `expected_hint` or `expected_min_confidence` fields. Routing eval cases need different schema.
**Resolution**: Extend `EvalTestCase` (in `eval_rubric.py`) with two **optional** fields:
```python
class EvalTestCase(BaseModel):
    # existing fields ...
    expected_hint: Optional[str] = None          # NEW: for routing eval cases
    expected_min_confidence: Optional[float] = None  # NEW: for routing eval cases
```
This is additive and backward-compatible — all 15 existing cases omit these fields (default `None`). The `run_evals.py` runner will check `if case.expected_hint: assert result.hint == case.expected_hint`. Track C-05 (B-01 in eval expansion) adds 5 routing YAML cases that use these fields.

---

## Sprint 204 Backlog

### Track A — Confidence Scoring in query_classifier.py (Day 1-4) — @pm

**Goal**: Add confidence scoring to the existing substring-based classifier and implement a fast LLM fallback for ambiguous queries.

**Architecture**:
```
User message arrives
    │
    ├─ query_classifier.classify(message)
    │   ├─ Substring matching (existing):
    │   │   ├─ "```" in message → code (confidence=0.95)
    │   │   ├─ "tại sao" in message → reasoning (confidence=0.85)
    │   │   ├─ len(message) <= 20 → fast (confidence=0.75)
    │   │   └─ No match → unknown (confidence=0.3)
    │   │
    │   ├─ Multiple matches? → highest priority wins, confidence adjusted
    │   │   ├─ Single clear match → confidence=0.9+
    │   │   ├─ Multiple matches → confidence = best - 0.2
    │   │   └─ No matches → confidence = 0.3 (unknown)
    │   │
    │   └─ confidence < 0.6?
    │       ├─ YES → LLM fallback (qwen3:8b, <500ms)
    │       │   └─ "Classify this query: code/reasoning/fast/governance/unknown"
    │       │   └─ LLM returns: {hint: "governance", confidence: 0.82}
    │       │
    │       └─ Still < 0.6 after LLM? → human escalation (Track B)
    │
    └─ Return: ClassificationResult(hint, confidence, model_route, method)
```

| ID | Item | Priority | Deliverable |
|----|------|----------|-------------|
| A-01 | Add `confidence: float` to `ClassificationResult` | P0 | 0.0-1.0 score based on match quality |
| A-02 | Confidence scoring rules for substring matches | P0 | Single match: 0.9+, multiple: best-0.2, none: 0.3 |
| A-03 | LLM fallback classifier (qwen3:8b) | P1 | For confidence < 0.6: fast LLM classification (<500ms target) |
| A-04 | New hint type: `governance` | P1 | Detect governance intents (approve, evaluate, status) → route to command_router |
| A-05 | Classification logging: method + confidence | P1 | Log: substring vs LLM, confidence score, final hint, latency |
| A-06 | Classification metrics: confidence distribution | P2 | Track: % queries at each confidence band (>0.9, 0.6-0.9, <0.6) |

**Modified files**:
- `backend/app/services/agent_team/query_classifier.py` (~50 LOC additions)
- `backend/app/schemas/agent_team.py` — Add `confidence` field to schema

**Confidence Scoring Rules**:
```python
def _compute_confidence(self, matches: list[HintMatch]) -> float:
    """Compute confidence based on match quality."""
    if not matches:
        return 0.3  # No matches = low confidence

    if len(matches) == 1:
        # Single clear match = high confidence
        match = matches[0]
        if match.priority >= 10:  # code (``` pattern)
            return 0.95
        elif match.priority >= 5:  # reasoning (keyword match)
            return 0.85
        else:  # fast (length heuristic)
            return 0.75

    # Multiple matches = reduced confidence (ambiguous)
    best = max(m.priority for m in matches)
    second = sorted([m.priority for m in matches], reverse=True)[1]
    gap = best - second
    return min(0.9, 0.6 + (gap * 0.1))  # Larger gap = more confident
```

**LLM Fallback Prompt** (qwen3:8b, <500ms):
```
Classify this user message into one category.

Categories:
- code: Request to write, fix, or review code
- reasoning: Request requiring deep analysis or explanation
- governance: Request for gate actions, evidence, sprint management
- fast: Simple greeting, acknowledgment, or short query

Message: "{user_message}"

Return JSON: {"hint": "category", "confidence": 0.0-1.0}
```

**Acceptance criteria**:
- [ ] `ClassificationResult` includes `confidence` field (0.0-1.0)
- [ ] Single substring match: confidence >= 0.75
- [ ] No match: confidence = 0.3 → triggers LLM fallback
- [ ] LLM fallback responds in <500ms using `qwen3:8b`
- [ ] Classification method logged (substring vs LLM)

---

### Track B — Human Escalation for Low-Confidence Queries (Day 3-6) — @pm

**Goal**: When confidence remains < 0.6 after LLM fallback, route the query to a human operator via Magic Link approval — the same OOB auth pattern used for gate approvals (Sprint 199).

**Architecture**:
```
Query with confidence < 0.6 (after LLM fallback)
    │
    ├─ escalation_service.escalate(query, user, conversation_id)
    │   ├─ Generate Magic Link: "Review this query classification"
    │   │   └─ Payload: {query, suggested_hint, confidence, options: [code/reasoning/governance/fast]}
    │   │
    │   ├─ Send to designated human reviewer:
    │   │   ├─ Telegram: "Low-confidence query from @user: '{query}'"
    │   │   │   └─ "Classify as: [Code] [Reasoning] [Governance] [Fast]"
    │   │   │   └─ Magic Link per option (5-min TTL)
    │   │   │
    │   │   └─ Or: Project PM/CTO gets notification
    │   │
    │   └─ Meanwhile: user gets "Processing..." message
    │
    ├─ Human clicks classification link
    │   └─ query_classifier.record_human_classification(query, hint="governance")
    │   └─ Agent proceeds with human-selected classification
    │
    └─ Timeout (5 min): fallback to LLM's best guess with warning
```

| ID | Item | Priority | Deliverable |
|----|------|----------|-------------|
| B-01 | `escalation_service.py` — human escalation routing | P0 | Routes low-confidence queries to human reviewer via Magic Link |
| B-02 | Magic Link for classification (reuse magic_link_service.py) | P0 | 4 classification options as separate Magic Links (5-min TTL) |
| B-03 | Human reviewer notification via Telegram | P1 | Designated reviewer gets query + classification options |
| B-04 | Timeout fallback (5 min) | P1 | If no human response: use LLM's best guess + log as "unconfirmed" |
| B-05 | Human classification logging for training data | P1 | Record: (query, human_hint, llm_hint, confidence) for future model fine-tuning |
| B-06 | Escalation rate monitoring | P2 | Track: % queries escalated per day/week, response time, timeout rate |

**New files**:
- `backend/app/services/agent_team/escalation_service.py` (~100 LOC)

**Modified files**:
- `backend/app/services/agent_team/query_classifier.py` — Route to escalation when confidence < 0.6
- `backend/app/services/agent_team/magic_link_service.py` — Add classification payload type

**Acceptance criteria**:
- [ ] Queries with confidence < 0.6 (after LLM fallback) trigger human escalation
- [ ] Human reviewer receives Telegram notification with 4 classification options
- [ ] Human click resolves classification, agent proceeds
- [ ] 5-min timeout: falls back to LLM's best guess with `"unconfirmed"` flag
- [ ] All escalations logged as training data (query, human_hint, llm_hint)

---

### Track C — Eval Integration + Routing Quality Measurement (Day 5-8) — @pm

**Goal**: Add routing-quality eval cases and integrate confidence scoring into the existing eval framework.

| ID | Item | Priority | Deliverable |
|----|------|----------|-------------|
| C-01 | 5 routing eval test cases (YAML) | P0 | Test correct classification + confidence for known query types |
| C-02 | Eval case: ambiguous query → LLM fallback triggered | P1 | Verify LLM fallback activates when substring matching fails |
| C-03 | Eval case: governance intent correctly detected | P1 | "approve gate 5" → governance hint, confidence >= 0.8 |
| C-04 | Routing accuracy dashboard on Gateway Dashboard | P2 | New section: classification distribution, confidence histogram, escalation rate |
| C-05 | Add routing evals to baseline.json | P1 | 5 routing cases added to baseline for regression detection |

**Eval test cases (5 YAML files)**:
```yaml
# routing_code.yaml
prompt: "```python\ndef hello():\n    print('hi')\n```\nFix this function"
expected_hint: "code"
expected_min_confidence: 0.9
method: "substring"

# routing_governance.yaml
prompt: "approve gate 5 for project sdlc-orchestrator"
expected_hint: "governance"
expected_min_confidence: 0.8
method: "substring_or_llm"

# routing_ambiguous.yaml
prompt: "review the latest changes and tell me what you think"
expected_hint: "reasoning"
expected_max_confidence: 0.7  # Should be low - ambiguous between code review and reasoning
expected_method: "llm_fallback"

# routing_fast.yaml
prompt: "ok"
expected_hint: "fast"
expected_min_confidence: 0.7
method: "substring"

# routing_vietnamese.yaml
prompt: "tại sao gate G2 bị reject?"
expected_hint: "reasoning"
expected_min_confidence: 0.8
method: "substring"
```

**Acceptance criteria**:
- [ ] 5 routing eval cases pass with expected hints and confidence ranges
- [ ] Ambiguous queries correctly trigger LLM fallback
- [ ] Baseline updated with routing eval scores
- [ ] Total eval cases: 20 (15 from Sprint 203 + 5 routing)

---

### Track D — Testing + Sprint Close (Day 8-10) — @pm

| ID | Item | Priority | Deliverable |
|----|------|----------|-------------|
| D-01 | Confidence scoring unit tests (8 cases) | P0 | Single match, multiple matches, no match, edge cases |
| D-02 | LLM fallback unit tests (5 cases) | P0 | Fallback triggers, timeout handling, response parsing |
| D-03 | Human escalation unit tests (6 cases) | P0 | Magic Link generation, timeout fallback, human click resolution |
| D-04 | Integration test: full routing flow | P1 | Message → classify → confidence check → (LLM/human) → route |
| D-05 | Regression test: existing classifications unchanged | P0 | Verify Sprint 179 query_classifier behavior preserved |
| D-06 | Regression test suite (950+ tests) | P0 | All Sprint 197-203 tests passing + Sprint 204 new tests |
| D-07 | Sprint 204 close documentation | P1 | G-Sprint-Close within 24h |

---

## Architecture: Confidence-Based Routing Flow

### Full Classification Pipeline

```
  User Message            query_classifier.py         qwen3:8b (LLM)
       │                        │                          │
       │── "review changes" ──>│                          │
       │                        │── substring scan         │
       │                        │   "review" → reasoning   │
       │                        │   "changes" → code?      │
       │                        │   Multiple matches!      │
       │                        │   confidence = 0.5       │
       │                        │                          │
       │                        │── confidence < 0.6       │
       │                        │── LLM fallback ────────>│
       │                        │                          │── classify
       │                        │<── {hint: "code",        │
       │                        │     confidence: 0.78} ──│
       │                        │                          │
       │                        │── confidence = 0.78      │
       │                        │── >= 0.6 → proceed       │
       │                        │                          │
       │<── ClassificationResult│                          │
       │    hint="code"         │                          │
       │    confidence=0.78     │                          │
       │    method="llm"        │                          │
```

### Human Escalation Flow

```
  User Message          query_classifier       escalation_service     Human Reviewer
       │                      │                       │                     │
       │── "something         │                       │                     │
       │    vague" ──────────>│                       │                     │
       │                      │── substring: 0.3      │                     │
       │                      │── LLM: 0.45           │                     │
       │                      │── still < 0.6!        │                     │
       │                      │                       │                     │
       │                      │── escalate() ────────>│                     │
       │                      │                       │── Magic Links ────>│
       │<── "Processing,      │                       │   [Code][Reason]   │
       │     waiting for      │                       │   [Gov][Fast]      │
       │     reviewer..." ────│                       │                     │
       │                      │                       │                     │
       │                      │                       │<── clicks [Code] ──│
       │                      │                       │                     │
       │                      │<── hint="code" ───────│                     │
       │                      │    source="human"     │                     │
       │                      │                       │                     │
       │<── Agent proceeds    │                       │                     │
       │    with code hint    │                       │                     │
```

---

## Files Summary

| File | Action | LOC | Track |
|------|--------|-----|-------|
| `backend/app/services/agent_team/query_classifier.py` | MODIFY | ~50 | A |
| `backend/app/schemas/agent_team.py` | MODIFY | ~10 | A |
| `backend/app/services/agent_team/escalation_service.py` | NEW | ~100 | B |
| `backend/app/services/agent_team/magic_link_service.py` | MODIFY | ~20 | B |
| `backend/tests/evals/cases/routing_*.yaml` | NEW | ~25 (5 files) | C |
| `backend/tests/evals/baseline.json` | MODIFY | ~5 | C |
| Tests (unit + integration) | NEW | ~300 | D |
| **Total** | | **~510** | |

---

## Sprint 204 Success Criteria

**Hard criteria (8)**:
- [ ] `ClassificationResult` includes `confidence` field (0.0-1.0)
- [ ] Substring match: confidence >= 0.75 for single match
- [ ] LLM fallback triggers when confidence < 0.6 (qwen3:8b, <500ms)
- [ ] Human escalation triggers when confidence < 0.6 after LLM fallback
- [ ] Magic Link classification resolves within 5-min TTL
- [ ] Timeout fallback: LLM's best guess with "unconfirmed" flag
- [ ] 20 total eval cases (15 previous + 5 routing) all passing
- [ ] 950+ test suite green, 0 regressions

**Stretch criteria (3)**:
- [ ] Routing accuracy dashboard on Gateway Dashboard
- [ ] Escalation rate < 5% of total queries (most resolved by substring or LLM)
- [ ] Human classification data exported for future model fine-tuning

---

## Risk Assessment

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| LLM fallback adds latency (>500ms) | P1 — slower routing | Medium | qwen3:8b is fastest model (60-80 tok/s), timeout at 1s |
| Human escalation overload | P2 — reviewer fatigue | Low | Target <5% escalation rate; auto-timeout after 5 min |
| Confidence scoring breaks existing routing | P0 — regression | Low | All existing tests must pass; confidence is additive (doesn't change routing logic) |
| Magic Link spam (many low-confidence queries) | P2 — reviewer notification flood | Low | Rate limit: max 5 escalations/min per user, batch notifications |

---

## Dependencies

- **Sprint 203 complete**: Evaluator-Optimizer + 15 eval cases + baseline established
- **qwen3:8b model**: Must be loaded on Ollama (fastest classification model)
- **magic_link_service.py**: Existing service (313 LOC) — needs classification payload type
- **query_classifier.py**: Existing classifier (Sprint 179, ADR-058 Pattern E) — MODIFY, not rewrite
- **Master plan reference**: CTO-approved Anthropic Best Practices — Gap 3 (P3)

---

## Anthropic Best Practices Reference

| Gap | PDF Chapter | Pattern | Implementation |
|-----|------------|---------|----------------|
| Gap 3 (P3) | Ch 3 | Routing — Confidence scores | Track A: confidence field + scoring rules |
| Gap 3 (P3) | Ch 3 | Routing — LLM-based classification | Track A: qwen3:8b fallback for ambiguous queries |
| Gap 3 (P3) | Ch 3 | Routing — Human escalation | Track B: Magic Link classification via Telegram |

---

## Post-Sprint 204: Anthropic Roadmap Completion Status

```yaml
Completed Gaps (Sprint 202-204):
  ✅ Gap 5 (P0): Automated Evals — 20 test cases, multi-judge, CI regression detection
  ✅ Gap 1 (P1): Context Engineering — agent_notes, save_note/recall_note, dynamic loading
  ✅ Gap 2 (P2): Evaluator-Optimizer — rubric scoring, iteration limits, multi-judge
  ✅ Gap 3 (P3): Confidence Routing — confidence scores, LLM fallback, human escalation

Deferred Gaps:
  ⏳ Gap 4 (P4): SKILL.md Standard — Sprint 205+, defer (DB approach adequate)
  ⏳ Gap 6 (P4): Prompt Injection Depth — Sprint 206+, ENTERPRISE only

Total LOC across Sprint 202-204: ~2,001 (vs ~590 estimated — expanded scope justified by eval expansion)

Next: Sprint 205+ — Vietnam SME Pilot execution OR SKILL.md standard (CTO decision)
```

---

---

## Locked Architecture Decisions (Feb 25, 2026 — CTO Pre-Sprint Review)

Pre-sprint codebase verified. All 4 blockers resolved with locked design decisions. **Do not deviate without CTO approval.**

### AD-1: `ClassificationResult` lives in `query_classifier.py` (not `schemas/`)

It's the return type of `classify()`, an internal service object. `schemas/agent_team.py` is only modified if this is surfaced via a new API endpoint — currently not required.

```python
@dataclass(frozen=True)
class ClassificationResult:
    hint: str | None
    confidence: float
    method: str = "substring"   # "substring" | "llm" | "llm_failed" | "timeout_fallback" | "none"
    matches: int = 0

    def __bool__(self) -> bool:
        """True if a hint was found — preserves `if model_hint:` caller pattern."""
        return self.hint is not None
```

### AD-2: `governance` hint is a pre-router interceptor, NOT a `MODEL_ROUTE_HINTS` entry

In `team_orchestrator._process()`, after `classify()`, BEFORE `_build_invoker()`:
```python
classification = classify(DEFAULT_CLASSIFICATION_RULES, message.content)
model_hint = classification.hint   # str | None — preserved for _build_invoker()

# Step 5.6 (Sprint 204): Governance intercept
if classification.hint == "governance":
    return await self._dispatch_governance_command(message, conversation, definition)

# Step 5.7: LLM fallback for low-confidence non-governance
if classification.confidence < 0.6 and classification.hint != "governance":
    classification = await self._llm_classify(message.content, classification)
    model_hint = classification.hint
    if classification.confidence < 0.6:
        return await self._escalate_for_classification(message, conversation, classification)

invoker = self._build_invoker(definition, model_hint=model_hint)
```

`MODEL_ROUTE_HINTS` stays unchanged (3 entries: code/reasoning/fast). No `governance` entry.

### AD-3: `_llm_classify()` is a method on `TeamOrchestrator` (not query_classifier)

Async, needs `self._ollama`, `asyncio.wait_for(timeout=1.0)`. 1s hard cap — fail fast. On failure, returns prior `ClassificationResult` unchanged.

```python
_VALID_HINTS = frozenset({"code", "reasoning", "governance", "fast"})  # query_classifier.py constant
```

### AD-4: `governance` rules — multiple single-keyword rules at priority=8

`ClassificationRule.keywords` is ALL-must-match, so one rule per governance trigger keyword:
```python
ClassificationRule(hint="governance", priority=8, keywords=("approve",), patterns=(), max_length=200),
ClassificationRule(hint="governance", priority=8, keywords=("gate",), patterns=(), max_length=200),
ClassificationRule(hint="governance", priority=8, keywords=("submit evidence",), patterns=()),
ClassificationRule(hint="governance", priority=8, keywords=("export audit",), patterns=()),
ClassificationRule(hint="governance", priority=8, keywords=("close sprint",), patterns=()),
```
`priority=8` is between `code` (10) and `reasoning` (5) — governance beats reasoning for governance intents.

### AD-5: `MagicLinkPayload` discriminated union — `payload_type` discriminator field

Add optional fields with defaults. `gate_id: str` stays required (caller-compat). Classification tokens pass `gate_id=""` (empty sentinel — pragmatic 0-caller-change approach).

```python
payload_type: str = "gate_approval"          # "gate_approval" | "classification"
classification_query: str | None = None
classification_options: tuple[str, ...] = field(default_factory=tuple)
conversation_id: str | None = None
```

**Caller check before modifying**: `grep -n "MagicLinkPayload(" backend/app/ -r` — confirm all existing callers pass `gate_id` positionally or as keyword.

### AD-6: `EvalTestCase` — additive optional fields, backward-compat with 15 existing cases

```python
expected_hint: str | None = Field(None)
expected_min_confidence: float | None = Field(None, ge=0.0, le=1.0)
expected_max_confidence: float | None = Field(None, ge=0.0, le=1.0)
expected_method: str | None = Field(None)
```
`tool_name` and `expected_behavior` get `default=""` so routing YAML cases don't need to supply them.

Also: `run_evals.py` must be updated to check routing fields when present:
```python
if case.expected_hint:
    assert result.hint == case.expected_hint, f"Expected hint {case.expected_hint}, got {result.hint}"
if case.expected_min_confidence:
    assert result.confidence >= case.expected_min_confidence
```

### AD-7: Baseline path (Sprint 203 carry-forward)

`baseline.json` is at `tests/evals/reference_answers/baseline.json` (Sprint 203 delivery path). All Sprint 204 Track C references use this path. The Files Summary below is corrected.

### AD-8: Risk flags

| Risk | Line | Mitigation |
|------|------|------------|
| `_build_invoker()` L636 `if model_hint in MODEL_ROUTE_HINTS` | `team_orchestrator.py:636` | `governance` intercept fires before L636 — safe. If somehow reached, `"governance" not in MODEL_ROUTE_HINTS` → condition False → role default model. No crash. |
| Circular import between `query_classifier.py` ↔ `config.py` | — | `query_classifier.py` currently imports nothing from project. `config.py` imports `ClassificationRule` from `query_classifier`. The `governance` rules added to `config.py` don't require `config.py` to import anything new. Safe. |
| `frozen=True` `MagicLinkPayload` field order | `magic_link_service.py:62` | Adding fields with defaults to a frozen dataclass is valid Python. Verify all callers use keyword args before modifying. |

### AD-9: Day-by-day Implementation Order

```
Day 1:  query_classifier.py — ClassificationResult + _compute_confidence() + classify() return change
        team_orchestrator.py L313 — call site update
Day 2:  agent_team/config.py — 5 governance ClassificationRules
        team_orchestrator.py — governance intercept + _dispatch_governance_command() skeleton
Day 3:  team_orchestrator.py — _llm_classify() (A-03)
        magic_link_service.py — MagicLinkPayload extension (B-02)
Day 4:  escalation_service.py — NEW file, full escalation flow (B-01/B-03)
        team_orchestrator.py — _escalate_for_classification() wiring
Day 5:  escalation_service.py — B-04 timeout fallback + B-05 training log
        A-05/A-06 confidence logging + metrics in conversation.config
Day 6:  eval_rubric.py — EvalTestCase schema update (C-01 prerequisite)
        5 routing YAML eval cases + run_evals.py routing schema support
        reference_answers/baseline.json — 5 routing entries appended (20 total)
Day 7:  test_sprint204_confidence_routing.py — classes 1-4 (TestClassificationResult, TestConfidenceScoring, TestClassifyReturnType, TestGovernanceRules)
Day 8:  test_sprint204_confidence_routing.py — classes 5-9 (TestLLMFallback, TestEscalationService, TestTeamOrchestratorRouting, TestEvalTestCaseRouting, TestRoutingEvalCases)
        test_sprint204_escalation.py — 25 dedicated escalation tests
Day 9:  D-05 regression: 15 existing eval cases + existing classify() behavior unchanged
        D-06 full 950+ regression suite
Day 10: Documentation + G-Sprint-Close
```

---

**Last Updated**: February 25, 2026
**Created By**: PM + AI Development Partner — Sprint 204 Planning (Anthropic Best Practices Roadmap)
**Framework Version**: SDLC 6.1.1
**Previous State**: Sprint 203 CLOSED (9.5/10)
**Source**: CTO-approved Applicability Analysis (9.2/10, Feb 23 2026)

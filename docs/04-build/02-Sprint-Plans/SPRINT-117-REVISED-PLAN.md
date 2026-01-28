# Sprint 117: Revised Dual-Track Plan
## Framework 6.0 Spec Migration (Track 1) + Orchestrator Alignment (Track 2)

**Date**: January 28, 2026
**Sprint Duration**: 10 days (Jan 28 - Feb 7, 2026)
**Status**: 🔄 IN PROGRESS (Day 2 Complete)
**Strategic Context**: Track 1 leads, Track 2 follows with synchronized milestones

---

## Executive Summary

**Track 1 (Framework 6.0 Spec Migration)** is the **conductor** (nhạc trưởng) - sets the pace and defines the milestones. Track 2 (Orchestrator Alignment) follows Track 1's progress and resumes work when Track 1 reaches specific milestones.

**Current Status (Day 2 - Jan 28)**:
- **Track 1**: ✅ 5/20 specs complete (25%) - All P0 specs migrated (~4,650 LOC)
- **Track 2**: ⏸️ PAUSED - POC approved, waiting for Track 1 milestones

**Key Decision**: Track 2 resumes when Track 1 completes **Milestone 1** (P1 specs) on Day 5 (Jan 31).

---

## Track 1: Framework 6.0 Spec Migration (Leader)

### Track 1 Status Summary

| Milestone | Target Date | Specs | Status | Progress |
|-----------|-------------|-------|--------|----------|
| **Day 1-2: P0 Specs** | Jan 28 | 5 specs | ✅ COMPLETE | 5/5 (100%) |
| **Day 3-5: P1 Specs** | Jan 31 | 7 specs | 🔄 NEXT | 0/7 (0%) |
| **Week 2: P2+P3 Specs** | Feb 7 | 8 specs | ⏳ PLANNED | 0/8 (0%) |
| **Week 2 End: Documentation** | Feb 7 | Section 7 + CONTENT-MAP | ⏳ PLANNED | 0/2 (0%) |

**Overall Progress**: 5/20 specs (25%) + 0/2 docs (0%) = **5/22 deliverables (23%)**

---

### Track 1 Detailed Schedule

#### ✅ Milestone 0: P0 Specs (Day 1-2 - COMPLETE)

**Dates**: Jan 28 (Day 1-2)
**Status**: ✅ COMPLETE
**Deliverables**:
1. ✅ SPEC-0001: Governance System Specification (~750 LOC)
2. ✅ SPEC-0002: Quality Gates Specification (~850 LOC)
3. ✅ SPEC-0003: ADR-007 AI Context Engine (~900 LOC)
4. ✅ SPEC-0004: Policy Guards Design (~1,100 LOC)
5. ✅ SPEC-0005: System Architecture Document (~1,050 LOC)

**Total Output**: ~4,650 lines of Framework 6.0.0-compliant specifications
**Requirements**: 36 functional requirements in BDD format
**Acceptance Criteria**: 58 acceptance criteria with test methods

**Track 2 Dependency**: None (Track 2 POC already complete and approved)

---

#### 🔄 Milestone 1: P1 Specs (Day 3-5 - NEXT)

**Dates**: Jan 29-31 (Day 3-5)
**Status**: 🔄 NEXT (Starting Jan 29)
**Target**: 7 P1 specs (priority 75-85)

**Day 3 (Jan 29) - 2 specs**:
1. [ ] SPEC-0006: ADR-022 Multi-Provider Codegen Architecture (priority 85, ~800 LOC)
2. [ ] SPEC-0007: AGENTS-MD Technical Design (priority 84, ~750 LOC)

**Day 4 (Jan 30) - 2 specs**:
3. [ ] SPEC-0008: ADR-036 4-Tier Policy Enforcement (priority 82, ~700 LOC)
4. [ ] SPEC-0009: Codegen Service Specification (priority 80, ~850 LOC)

**Day 5 (Jan 31) - 3 specs**:
5. [ ] SPEC-0010: IR Processor Specification (priority 78, ~900 LOC)
6. [ ] SPEC-0011: ADR-012 AI Task Decomposition (priority 76, ~650 LOC)
7. [ ] SPEC-0012: Validation Pipeline Interface (priority 75, ~700 LOC)

**Estimated Output**: ~5,350 LOC (Day 3-5)
**Cumulative After Milestone 1**: ~10,000 LOC (12/20 specs = 60%)

**Track 2 Dependency**: **RESUME POINT** - Track 2 resumes when Milestone 1 complete (Jan 31 EOD)

---

#### ⏳ Milestone 2: P2+P3 Specs (Week 2 Days 1-3 - PLANNED)

**Dates**: Feb 3-5 (Week 2 Days 1-3)
**Status**: ⏳ PLANNED
**Target**: 8 P2+P3 specs (priority 50-74)

**Day 1-2 (Feb 3-4) - 5 P2 specs**:
1. [ ] SPEC-0013: Teams Service Specification (priority 74, ~600 LOC)
2. [ ] SPEC-0014: Planning Hierarchy Implementation (priority 72, ~700 LOC)
3. [ ] SPEC-0015: Governance Metrics & Dashboards (priority 70, ~650 LOC)
4. [ ] SPEC-0016: Evidence Vault Service (priority 68, ~750 LOC)
5. [ ] SPEC-0017: AI Council Service (priority 66, ~800 LOC)

**Day 3 (Feb 5) - 3 P3 specs**:
6. [ ] SPEC-0018: AGENTS-MD Integration (priority 64, ~500 LOC)
7. [ ] SPEC-0019: Feedback Learning Service (priority 62, ~550 LOC)
8. [ ] SPEC-0020: Conformance Check Service (priority 60, ~600 LOC)

**Estimated Output**: ~5,150 LOC (Week 2 Days 1-3)
**Cumulative After Milestone 2**: ~15,150 LOC (20/20 specs = 100%)

**Track 2 Dependency**: Track 2 continues Orchestrator automation (CLI, pre-commit, GitHub Actions)

---

#### ⏳ Milestone 3: Documentation Updates (Week 2 Days 4-5 - PLANNED)

**Dates**: Feb 6-7 (Week 2 Days 4-5)
**Status**: ⏳ PLANNED
**Target**: 2 major documentation updates

**Day 4 (Feb 6)**:
1. [ ] Update Section 7: Quality Assurance System
   - Anti-Vibecoding documentation (~800 LOC)
   - Vibecoding Index calculation formulas
   - Progressive Routing rules (Green/Yellow/Orange/Red)
   - Kill Switch criteria and recovery procedures

**Day 5 (Feb 7)**:
2. [ ] Update CONTENT-MAP.md navigation (~300 LOC)
   - Framework 6.0.0 structure references
   - /spec/ directory navigation
   - Cross-references to 20 migrated specs
   - Validate all links (ensure no broken references)

3. [ ] Validate all cross-references
   - Check all ADR links in specs
   - Check all related_specs links
   - Check all framework_version references

**Estimated Output**: ~1,100 LOC (documentation updates)
**Cumulative After Milestone 3**: ~16,250 LOC (20 specs + 2 docs = 100%)

**Track 2 Dependency**: Track 2 completes Orchestrator automation and testing

---

## Track 2: Orchestrator Alignment (Follower)

### Track 2 Status Summary

| Phase | Depends On | Target Date | Status | Progress |
|-------|------------|-------------|--------|----------|
| **Phase 0: POC** | None | Jan 28 | ✅ COMPLETE | 5/5 files (100%) |
| **Phase 1: Commit POC** | Track 1 Day 2 | Jan 29 | ⏸️ READY | 0/1 (0%) |
| **Phase 2: SPEC-0001/0002** | Track 1 Day 5 | Jan 31 | ⏸️ PAUSED | 0/2 (0%) |
| **Phase 3: Orchestrator Automation** | Track 1 Week 2 | Feb 7 | ⏸️ PAUSED | 0/5 (0%) |

**Overall Progress**: 5/13 deliverables (38%) - POC complete, automation paused

---

### Track 2 Detailed Schedule

#### ✅ Phase 0: Spec-First POC (Day 2 Afternoon - COMPLETE)

**Date**: Jan 28 (Day 2 Afternoon)
**Status**: ✅ COMPLETE
**Validation**: 23/25 checks PASSED (92%) - CTO APPROVED

**Deliverables**:
1. ✅ `spec/evidence/spec-frontmatter-schema.json` - JSON Schema for spec validation
2. ✅ `spec/controls/anti-vibecoding.yaml` - 3 controls (AVC-001/002/003)
3. ✅ `spec/gates/gates.yaml` - 5 gates (G0-G4) with tier requirements
4. ✅ `spec/VERSIONING.md` - Framework vs schema versioning strategy
5. ✅ `docs/SPEC-FIRST-POC-VALIDATION.md` - Manual validation checklist

**Total Output**: ~1,350 lines of pure YAML/JSON/Markdown specifications

**CTO Decision**: ✅ APPROVED TO COMMIT

---

#### ⏸️ Phase 1: Commit POC Files (Day 3 - READY TO RESUME)

**Date**: Jan 29 (Day 3)
**Status**: ⏸️ READY - Can proceed immediately (not blocked)
**Dependency**: Track 1 Day 2 complete (✅ DONE)

**Tasks**:
1. [ ] Commit 5 POC files to Framework repository
   ```bash
   cd /home/nqh/shared/SDLC-Orchestrator/SDLC-Enterprise-Framework
   git add spec/ docs/SPEC-FIRST-POC-VALIDATION.md
   git commit -m "feat(SDLC 6.0): Add spec-first POC (5 files, zero code)

   - spec/evidence/spec-frontmatter-schema.json (v1.0.0)
   - spec/controls/anti-vibecoding.yaml (AVC-001/002/003)
   - spec/gates/gates.yaml (G0-G4)
   - spec/VERSIONING.md (versioning rules)
   - docs/SPEC-FIRST-POC-VALIDATION.md (validation report)

   Purity guarantee:
   - Zero executable code (.py, .ts, .sh)
   - Platform-agnostic definitions only
   - Semantic-only gates (no automation blocks)

   Framework version: 6.0.0 (in development)
   Validation: 23/25 checks PASS (2 deferred: SPEC-0001/0002 frontmatter)

   Co-Authored-By: CTO Approval <cto@nhatquangholding.com>"
   git push origin main
   ```

2. [ ] Update sprint plan documents
   - Mark Phase 1 as COMPLETE in CURRENT-SPRINT.md
   - Update SPRINT-117-REVISED-PLAN.md progress

**Estimated Time**: 30 minutes
**Deliverables**: Git commit + sprint plan updates

**Resume Condition**: ✅ CAN RESUME NOW (no blockers)

---

#### ⏸️ Phase 2: Create SPEC-0001 and SPEC-0002 (Day 3-5 - BLOCKED)

**Dates**: Jan 29-31 (Day 3-5)
**Status**: ⏸️ BLOCKED - Waiting for Track 1 Milestone 1
**Dependency**: Track 1 completes SPEC-0006 to SPEC-0012 (P1 specs) by Jan 31

**Rationale**: SPEC-0001 and SPEC-0002 should follow the patterns established by P1 specs (SPEC-0006 to SPEC-0012). Waiting ensures consistency in:
- YAML frontmatter structure
- BDD requirements format
- Acceptance criteria tables
- Tier-specific sections
- Implementation plan format

**Tasks** (After Track 1 Milestone 1 complete):
1. [ ] Create SPEC-0001-Anti-Vibecoding.md with YAML frontmatter
   - Follow SPEC-0006 (ADR format) as template
   - 7 functional requirements in BDD format
   - 4 non-functional requirements
   - 12 acceptance criteria with test methods
   - 4-tier requirements (PROFESSIONAL + ENTERPRISE focus)
   - ~900-1,000 LOC estimated

2. [ ] Create SPEC-0002-Specification-Standard.md with YAML frontmatter
   - Follow SPEC-0007 (Technical Design) as template
   - 8 functional requirements in BDD format
   - 4 non-functional requirements
   - 10 acceptance criteria with test methods
   - 4-tier requirements (ALL tiers applicable)
   - ~800-900 LOC estimated

3. [ ] Validate frontmatter against spec-frontmatter-schema.json
   ```bash
   # Manual validation using Python
   python3 -c "
   import yaml, json, jsonschema
   schema = json.load(open('spec/evidence/spec-frontmatter-schema.json'))
   # Extract frontmatter from SPEC-0001
   # Validate against schema
   jsonschema.validate(frontmatter, schema)
   "
   ```

4. [ ] Update SPEC-FIRST-POC-VALIDATION.md
   - Add validation results for SPEC-0001 (Section 3.1)
   - Add validation results for SPEC-0002 (Section 3.2)
   - Update final score: 25/25 checks PASS (100%)

**Estimated Time**: 4-6 hours (2-3 hours per spec)
**Deliverables**: 2 specification files (~1,800-1,900 LOC) + validation report update

**Resume Condition**: 🔄 RESUME ON JAN 31 (when Track 1 Milestone 1 complete)

---

#### ⏸️ Phase 3: Orchestrator Automation (Week 2 - BLOCKED)

**Dates**: Feb 3-7 (Week 2)
**Status**: ⏸️ BLOCKED - Waiting for Track 1 Milestone 1 + Phase 2 complete
**Dependency**:
- Track 1 completes P1 specs (Jan 31)
- Track 2 completes SPEC-0001/0002 (Jan 31)

**Day 1-2 (Feb 3-4): CLI Tool Development**:
1. [ ] Create `sdlcctl spec validate` CLI (Python)
   - Location: `SDLC-Orchestrator/backend/app/cli/sdlcctl_spec_validate.py`
   - Reads Framework schemas from submodule
   - Validates YAML frontmatter against JSON Schema
   - Validates controls against structure rules
   - Validates gates against tier requirements
   - Error reporting with detailed messages
   - Estimated: ~400-500 LOC

2. [ ] Create CLI entry point
   - `sdlcctl spec validate --file SPEC-0001.md`
   - `sdlcctl spec validate --directory docs/`
   - Batch validation support
   - Estimated: ~100-150 LOC

3. [ ] Unit tests for CLI tool
   - Test JSON Schema validation
   - Test YAML syntax validation
   - Test error handling
   - Test batch validation
   - Coverage target: 95%+
   - Estimated: ~300-400 LOC

**Day 3 (Feb 5): Integration Templates**:
4. [ ] Create pre-commit hook template
   - `.pre-commit-config.yaml` example
   - Blocks commits with invalid specs
   - Runs `sdlcctl spec validate` automatically
   - Estimated: ~50-80 LOC

5. [ ] Create GitHub Actions workflow template
   - `.github/workflows/spec-validation.yml`
   - Runs on PR creation/update
   - Validates all changed specs
   - Comments on PR with validation results
   - Estimated: ~100-150 LOC

**Day 4-5 (Feb 6-7): Dashboard Integration + Testing**:
6. [ ] Dashboard compliance page
   - Frontend: `frontend/src/app/compliance/specs`
   - Display validation results for all specs
   - Spec list with PASS/FAIL status
   - Error details for failed specs
   - Estimated: ~300-400 LOC (frontend + backend API)

7. [ ] Integration testing
   - E2E test: CLI validation → Dashboard display
   - Test Framework submodule integration
   - Performance test: 100+ specs in <10s
   - Estimated: ~200-300 LOC

8. [ ] Documentation
   - Usage guide: How to use `sdlcctl spec validate`
   - Pre-commit setup guide
   - CI/CD integration guide (GitHub Actions, GitLab CI)
   - Update CLAUDE.md with spec validation workflow
   - Estimated: ~500-600 LOC (Markdown)

**Estimated Time**: 5 days (40 hours)
**Total Output**: ~2,000-2,500 LOC (code + docs)

**Resume Condition**: 🔄 RESUME ON FEB 3 (when Track 1 Milestone 1 complete + Phase 2 done)

---

## Synchronization Points

### Sprint 117 Key Milestones (Track 1 → Track 2 Handoffs)

| Milestone | Track 1 Delivers | Track 2 Can Resume | Date |
|-----------|------------------|-------------------|------|
| **M0** | 5 P0 specs (~4,650 LOC) | Phase 1: Commit POC files | ✅ Jan 28 |
| **M1** | 7 P1 specs (~5,350 LOC) | Phase 2: Create SPEC-0001/0002 | 🔄 Jan 31 |
| **M2** | 8 P2+P3 specs (~5,150 LOC) | Phase 3: Orchestrator automation | 🔄 Feb 3 |
| **M3** | Documentation updates (~1,100 LOC) | Phase 3: Testing + docs | 🔄 Feb 7 |

**Critical Path**: Track 1 M1 (Jan 31) → Track 2 Phase 2 → Track 2 Phase 3 (Feb 3-7)

---

## Sprint 117 Success Criteria

### Track 1 (Framework 6.0 Spec Migration)
- [ ] 20/20 specs migrated to Framework 6.0.0 format (~15,000 LOC)
- [ ] Section 7 updated with Anti-Vibecoding documentation
- [ ] CONTENT-MAP.md updated with Framework 6.0 navigation
- [ ] All cross-references validated (no broken links)
- [ ] 100% compliance with Framework 6.0.0 standards

### Track 2 (Orchestrator Alignment)
- [ ] 5 POC files committed to Framework repository
- [ ] SPEC-0001 and SPEC-0002 created with validated frontmatter
- [ ] `sdlcctl spec validate` CLI tool complete (~500 LOC)
- [ ] Pre-commit hook + GitHub Actions templates (~150 LOC)
- [ ] Dashboard compliance page complete (~400 LOC)
- [ ] Documentation complete (~600 LOC)
- [ ] Test coverage 95%+ (unit + integration)

### Overall Sprint Success
- [ ] Track 1: 100% complete (20 specs + 2 docs)
- [ ] Track 2: 100% complete (13 deliverables)
- [ ] Zero blockers or delays
- [ ] CTO approval for both tracks

---

## Risk Mitigation

### Risk 1: Track 1 Delays Impact Track 2
**Likelihood**: MEDIUM
**Impact**: HIGH
**Mitigation**:
- Track 2 Phase 1 (commit POC) can proceed immediately (not blocked)
- If Track 1 delayed beyond Jan 31, Track 2 creates SPEC-0001/0002 using P0 specs as templates
- Track 2 can start Orchestrator automation prep work (design, dependencies) in parallel

### Risk 2: Track 2 Team Idle During Pauses
**Likelihood**: LOW
**Impact**: MEDIUM
**Mitigation**:
- Phase 1 (commit POC) ready to resume now - no idle time
- During Phase 2 wait (Jan 29-31), team can:
  - Review P1 specs as they're completed (learn patterns)
  - Design CLI tool architecture (prep for Phase 3)
  - Set up development environment for Orchestrator

### Risk 3: Specification Format Inconsistency
**Likelihood**: MEDIUM
**Impact**: MEDIUM
**Mitigation**:
- Track 1 uses proven templates from P0 specs (SPEC-0001 to SPEC-0005)
- Daily sync between Track 1 and Track 2 leads (15-min standup)
- Track 2 reviews specs as Track 1 completes them (early feedback)

---

## Communication Plan

### Daily Standup (9:00 AM)
**Attendees**: Track 1 Lead, Track 2 Lead, PM
**Duration**: 15 minutes
**Format**:
- Track 1: Yesterday/Today/Blockers
- Track 2: Yesterday/Today/Blockers (if active)
- Sync points: Dependencies clear?

### Milestone Reviews (End of Each Milestone)
**M1 Review** (Jan 31 EOD):
- Track 1: All 7 P1 specs complete?
- Track 2: Ready to resume Phase 2?
- Go/No-Go decision for Track 2 Phase 2

**M2 Review** (Feb 5 EOD):
- Track 1: All 8 P2+P3 specs complete?
- Track 2: SPEC-0001/0002 complete?
- Go/No-Go decision for Track 2 Phase 3 continuation

**M3 Review** (Feb 7 EOD):
- Track 1: Documentation updates complete?
- Track 2: Orchestrator automation complete?
- Sprint 117 retrospective

### Sprint Retrospective (Feb 7, 3:00 PM)
**Attendees**: Full team
**Duration**: 1 hour
**Topics**:
- What worked: Dual-track coordination
- What didn't: Blockers, delays
- Action items: Process improvements for Sprint 118

---

## Next Steps (Immediate - Jan 29)

### Track 1 (Continue as Planned)
1. [ ] Begin Day 3 work: Migrate 2 P1 specs
   - SPEC-0006: ADR-022 Multi-Provider Codegen Architecture
   - SPEC-0007: AGENTS-MD Technical Design
2. [ ] Target: Complete 2 specs by Jan 29 EOD (~1,550 LOC)

### Track 2 (Resume Phase 1)
1. [x] Read revised sprint plan (THIS DOCUMENT)
2. [ ] **RESUME NOW**: Execute Phase 1 - Commit POC files
   - Task: Git commit + push 5 POC files
   - Estimated time: 30 minutes
   - No blockers (CTO already approved)
3. [ ] Update sprint plan documents
   - Mark Phase 1 COMPLETE
   - Update progress tracking

### Coordination
1. [ ] Share revised plan with team (Slack/Email)
2. [ ] Schedule M1 Review meeting (Jan 31, 4:00 PM)
3. [ ] Daily standup continues (9:00 AM daily)

---

**Document Status**: ✅ REVISED PLAN READY
**Track 1**: 🔄 IN PROGRESS (Day 3 starting)
**Track 2**: 🔄 READY TO RESUME (Phase 1 unblocked)
**Next Review**: M1 Review (Jan 31, 4:00 PM)

---

*Sprint 117 Revised Dual-Track Plan*
*Framework 6.0 Spec Migration + Orchestrator Alignment*
*Synchronized execution with clear dependencies*

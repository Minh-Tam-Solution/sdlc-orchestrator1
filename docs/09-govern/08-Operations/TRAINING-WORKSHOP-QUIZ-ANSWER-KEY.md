# Training Workshop Quiz - Answer Key
## SDLC-Enterprise-Framework Submodule Operations

**Version:** 1.0.0
**Quiz Format:** 5 multiple choice questions
**Passing Score:** 4/5 (80% accuracy)
**Time Limit:** 15 minutes
**Retakes:** Unlimited (must pass by Dec 11 EOD)

---

## 📝 QUIZ FORM (For Students)

**Name:** ________________________
**Role:** ________________________
**Date:** ________________________
**Session:** Group 1 / Group 2 (circle one)

**Instructions:**
- Mark ONE answer per question (A, B, C, or D)
- Time limit: 15 minutes
- Passing score: 4/5 correct answers
- No collaboration, closed book

---

### Question 1: Cloning with Submodule

Your manager asks you to clone SDLC Orchestrator. Which command is correct?

- [ ] A) `git clone https://github.com/Minh-Tam-Solution/SDLC-Orchestrator`

- [ ] B) `git clone --recurse-submodules https://github.com/Minh-Tam-Solution/SDLC-Orchestrator`

- [ ] C) `git clone https://github.com/Minh-Tam-Solution/SDLC-Orchestrator && git submodule init`

- [ ] D) Both B and C are correct

**Your Answer:** ____

---

### Question 2: Framework-First Principle

PM asks you to add "AI-powered BRD generator" feature. What is the CORRECT approach?

- [ ] A) Add API endpoint to Orchestrator backend, hard-code BRD template in Python

- [ ] B) Add BRD template to Framework (SDLC-Enterprise-Framework), then build Orchestrator automation

- [ ] C) Build Orchestrator feature first, migrate to Framework later if needed

- [ ] D) Framework-First doesn't apply to AI features, go ahead with Orchestrator

**Your Answer:** ____

---

### Question 3: Updating Framework After Pull

After `git pull origin main`, you notice Framework files are outdated. What should you do?

- [ ] A) Delete SDLC-Enterprise-Framework/ and re-clone main repo

- [ ] B) Run `git submodule update --init --recursive`

- [ ] C) Run `cd SDLC-Enterprise-Framework && git pull origin main`

- [ ] D) Ignore it, Framework updates are optional

**Your Answer:** ____

---

### Question 4: Working on Framework Changes

You need to add SASE MRP template to Framework. What is the correct workflow?

- [ ] A) Edit in `SDLC-Orchestrator/SDLC-Enterprise-Framework/`, commit to main repo

- [ ] B) Edit in `SDLC-Orchestrator/SDLC-Enterprise-Framework/`, commit to Framework repo, then update main repo pointer

- [ ] C) Clone Framework repo separately, commit there, then update main repo submodule

- [ ] D) Both B and C are correct

**Your Answer:** ____

---

### Question 5: Crisis Recovery

After `git pull`, you see error: `fatal: reference is not a tree: abc1234`. What is the problem?

- [ ] A) Framework repository is unavailable (GitHub outage)

- [ ] B) Submodule pointer out of sync (run `git submodule update`)

- [ ] C) Framework commit abc1234 doesn't exist (force-pushed or deleted)

- [ ] D) Your local Framework has uncommitted changes

**Your Answer:** ____

---

**Score:** ____/5

**Result:** PASS (4/5+) / RETAKE REQUIRED (<4/5)

**Instructor Signature:** ________________________

**Date Graded:** ________________________

---

## 🔑 ANSWER KEY (For Instructor Only)

### Question 1: Cloning with Submodule

**Correct Answer:** **D** (Both B and C are correct)

**Explanation:**

**Option A:** ❌ WRONG
- Clones main repo only
- Framework submodule NOT initialized
- `SDLC-Enterprise-Framework/` directory will be empty
- Common beginner mistake

**Option B:** ✅ CORRECT
- `--recurse-submodules` flag clones main repo + initializes submodules in one command
- Recommended approach (simplest)
- Framework files appear immediately after clone

**Option C:** ✅ CORRECT
- Two-step process: clone main repo, then initialize submodule manually
- Alternative approach (more explicit)
- Same end result as Option B

**Option D:** ✅ CORRECT (BEST ANSWER)
- Both B and C achieve the same goal
- B is faster, C is more explicit
- Both are valid production workflows

**Why This Matters:**
- Forgetting `--recurse-submodules` is the #1 submodule mistake
- Empty Framework directory causes build failures
- Always verify submodule initialized: `git submodule status`

**Related Slide:** Slide 7 (Cloning with Submodule)

---

### Question 2: Framework-First Principle

**Correct Answer:** **B** (Add BRD template to Framework, then build Orchestrator automation)

**Explanation:**

**Option A:** ❌ WRONG
- Violates Framework-First Principle
- Hard-codes template in Orchestrator (tool-specific)
- Other projects (NQH, BFlow, MTEP) cannot reuse template
- Pre-commit hook would BLOCK this commit

**Option B:** ✅ CORRECT
- Follows Framework-First: Methodology (Framework) → Automation (Orchestrator)
- BRD template is methodology (belongs in Framework)
- Template tools-agnostic (works with any AI tool: Claude, GPT-4, Gemini)
- Orchestrator automation is Track 2 (conditional, optional)

**Option C:** ❌ WRONG
- "Build first, migrate later" approach leads to technical debt
- Framework migration never happens (pressure to ship)
- NQH-Bot crisis taught us: shortcuts compound into disasters

**Option D:** ❌ WRONG
- Framework-First applies to ALL features (including AI)
- AI prompt templates belong in Framework
- See: `SDLC-Enterprise-Framework/04-AI-Prompts/`

**Why This Matters:**
- Framework-First ensures templates survive tool changes
- SE 3.0 SASE templates added to Framework (Track 1) BEFORE Orchestrator automation (Track 2)
- Enforcement automation blocks violations (3-layer defense)

**Related Slide:** Slide 4 (Framework-First in Practice)

---

### Question 3: Updating Framework After Pull

**Correct Answer:** **B** (Run `git submodule update --init --recursive`)

**Explanation:**

**Option A:** ❌ WRONG
- Deleting and re-cloning is inefficient (wastes bandwidth)
- Loses local uncommitted changes
- Unnecessary when `git submodule update` solves problem in <10 seconds

**Option B:** ✅ CORRECT
- `git pull` updates main repo only, NOT submodule
- `git submodule update --init --recursive` syncs submodule to commit hash tracked in main repo
- Correct command for this scenario
- Can be automated with post-merge hook

**Option C:** ❌ WRONG
- `cd SDLC-Enterprise-Framework && git pull` fetches LATEST Framework commit
- Main repo may track older commit (version mismatch)
- Causes "modified submodule" state (+ prefix in `git submodule status`)
- Wrong approach (breaks main repo's submodule pointer)

**Option D:** ❌ WRONG
- Framework updates are NOT optional
- Outdated Framework causes build failures (missing templates)
- Team collaboration broken (different Framework versions)

**Why This Matters:**
- `git pull` + `git submodule update` is daily workflow
- Main repo tracks specific Framework commit (not "latest")
- Syncing submodule ensures team uses same Framework version

**Related Slide:** Slide 8 (Updating Framework After Pull)

---

### Question 4: Working on Framework Changes

**Correct Answer:** **D** (Both B and C are correct)

**Explanation:**

**Option A:** ❌ WRONG
- Commits to main repo, NOT Framework repo
- Framework is separate git repository
- Changes won't appear in Framework repo (lost work)
- Other projects won't see Framework changes

**Option B:** ✅ CORRECT
- Work in `SDLC-Orchestrator/SDLC-Enterprise-Framework/` submodule directory
- Commit to Framework repo (separate from main repo)
- Update main repo pointer to new Framework commit
- Recommended workflow (keeps work in one directory)

**Option C:** ✅ CORRECT
- Clone Framework repo separately (`git clone https://...SDLC-Enterprise-Framework`)
- Commit changes there
- Update main repo submodule pointer (`git submodule update --remote`)
- Alternative workflow (cleaner separation)

**Option D:** ✅ CORRECT (BEST ANSWER)
- Both B and C achieve the same result
- B is faster (no separate clone), C is cleaner (separate workspace)
- Both are valid production workflows

**Why This Matters:**
- Framework changes require TWO commits:
  1. Commit to Framework repo (template changes)
  2. Commit to main repo (submodule pointer update)
- Skipping step 2 breaks team collaboration (others won't see Framework changes)

**Related Slide:** Slide 9 (Working on Framework Changes)

---

### Question 5: Crisis Recovery

**Correct Answer:** **C** (Framework commit abc1234 doesn't exist - force-pushed or deleted)

**Explanation:**

**Option A:** ❌ WRONG
- GitHub outage shows different error: `fatal: unable to access 'https://...'`
- Network failures show connection timeout errors
- "reference is not a tree" is specific to missing commit

**Option B:** ❌ WRONG
- Pointer out of sync shows different symptom: Framework directory empty or outdated
- `git submodule status` shows "-" prefix (uninitialized)
- Error message different: no "reference is not a tree"

**Option C:** ✅ CORRECT
- Error "reference is not a tree: abc1234" = commit hash doesn't exist in repo
- Common causes:
  - Framework repo force-pushed (commit deleted)
  - Framework repo rebased (commit hash changed)
  - Developer pushed submodule pointer before Framework commit
- Recovery: Checkout nearest available commit, update main repo pointer

**Option D:** ❌ WRONG
- Uncommitted changes show different state: "M" prefix in `git submodule status`
- No error about "reference is not a tree"
- `git status` inside Framework shows uncommitted files

**Why This Matters:**
- Missing commits are SERIOUS (requires investigation)
- Recovery: Find nearest commit (`git log`), checkout, update pointer
- Prevention: NEVER force-push Framework main branch

**Related Slide:** Slide 14 (Crisis Scenario 3)

---

## 📊 GRADING RUBRIC

### Scoring Guidelines

**5/5 (Perfect Score):**
- All questions correct
- Student demonstrates full understanding
- Ready for Week 2 work immediately

**4/5 (Pass):**
- 1 mistake (acceptable)
- Student understands core concepts
- Ready for Week 2 work (minor gaps acceptable)

**3/5 (Borderline Fail):**
- 2 mistakes (requires retake)
- Student has knowledge gaps
- Review crisis recovery OR Framework-First Principle
- Retake recommended (not mandatory)

**2/5 or lower (Fail):**
- 3+ mistakes (requires retake MANDATORY)
- Student needs additional study
- Review all training materials
- 1-on-1 coaching available

### Retake Policy

**If Score <4/5:**
- Study materials: `SUBMODULE-TEAM-TRAINING.md` (full guide)
- Review crisis recovery: `SUBMODULE-CRISIS-RECOVERY-PLAN.md`
- Retake scheduling:
  - Same day (if time permits)
  - Dec 11 (latest deadline)
- Unlimited retakes allowed
- Must pass by Dec 11 EOD (Week 2 blocker)

---

## 📈 QUIZ STATISTICS (Template)

**Session:** Group 1 / Group 2 (circle one)
**Date:** Dec 10 / Dec 11, 2025

| Question | % Correct | Common Wrong Answer | Topic |
|----------|-----------|---------------------|-------|
| Q1 | ___% | A (___%), C (___%) | Cloning |
| Q2 | ___% | A (___%), C (___%) | Framework-First |
| Q3 | ___% | C (___%), D (___%) | Updating |
| Q4 | ___% | A (___%), B (___%) | Workflow |
| Q5 | ___% | B (___%), A (___%) | Crisis |

**Overall:**
- Average Score: ___/5
- Pass Rate: ___% (4/5+ scores)
- Retakes Needed: ___ students
- Most Missed Question: Q___

**Analysis:**
- If Q1 missed: Emphasize `--recurse-submodules` flag
- If Q2 missed: Re-teach Framework-First Principle
- If Q3 missed: Demo `git submodule update` workflow
- If Q4 missed: Show two-step commit workflow live
- If Q5 missed: Review Crisis Recovery Plan document

---

## 🎯 POST-QUIZ ACTIONS

### Immediate (After Grading)

**For Each Student:**
1. Grade quiz (mark correct/wrong)
2. Calculate score (__/5)
3. Mark result: PASS (4/5+) / RETAKE (<4/5)
4. Return quiz form with score

**Announce Results:**
- "Congratulations to those who passed (4/5+)!"
- "For those who scored <4/5, retakes available [date/time]"
- "Study materials: SUBMODULE-TEAM-TRAINING.md"

### Follow-Up (Same Day)

**Email to Team:**
```
Subject: SE 3.0 Submodule Training - Quiz Results

Hi Team,

Quiz results from today's workshop:

Pass Rate: X/9 (100% required by Dec 11 EOD)
Average Score: X.X/5

Passed (4/5+): [Names]
Retake Required (<4/5): [Names]

Next Steps:
- Passed: Certified for Week 2 work ✅
- Retake: Study materials sent, retake scheduled [date/time]

Retake Schedule:
[Date/Time] - [Location/Zoom]

Study Materials:
- Full guide: docs/09-govern/08-Operations/SUBMODULE-TEAM-TRAINING.md
- Crisis recovery: docs/09-govern/08-Operations/SUBMODULE-CRISIS-RECOVERY-PLAN.md

Questions? Reply to this email.

Best regards,
PM/PO
```

### Evidence Submission (Dec 11 EOD)

**Compile for CTO:**
1. Attendance records (9/9 = 100%)
2. Quiz scores (anonymized)
3. Pass rate (9/9 = 100% required)
4. Retake records (if any)

**Submit:**
- File: `WEEK-1-TRAINING-EVIDENCE-REPORT.md`
- Email to CTO: cto@company.com
- Subject: "SE 3.0 Week 1 Training Evidence - Dec 11, 2025"

---

## 🔍 COMMON QUIZ MISTAKES & FIXES

### Mistake 1: Choosing Option A on Q1 (Clone without --recurse-submodules)

**Why Students Choose This:**
- Looks like normal `git clone` (familiar)
- Don't realize submodules need special flag

**Fix:**
- Emphasize: Submodules NOT cloned by default
- Demo: Clone without flag → empty Framework directory
- Show: Error when building (missing templates)

---

### Mistake 2: Choosing Option A on Q2 (Hard-code template in Orchestrator)

**Why Students Choose This:**
- Faster to implement (no Framework step)
- Seems pragmatic ("we need it now")

**Fix:**
- Explain: Framework-First is non-negotiable (CTO mandated)
- Demo: Pre-commit hook blocks hard-coded templates
- Show: SE 3.0 SASE example (BRS template in Framework FIRST)

---

### Mistake 3: Choosing Option C on Q3 (Pull Framework directly)

**Why Students Choose This:**
- Logical ("update Framework repo directly")
- Don't understand main repo tracks specific commit

**Fix:**
- Explain: Main repo tracks commit hash, not "latest"
- Demo: `git pull` in Framework → version mismatch
- Show: `git submodule status` shows "+" prefix (modified)

---

### Mistake 4: Choosing Option A on Q4 (Commit to main repo)

**Why Students Choose This:**
- Confused about which repo to commit to
- Don't realize Framework is separate git repo

**Fix:**
- Emphasize: Framework has separate .git directory
- Demo: `cd SDLC-Enterprise-Framework && git status`
- Show: Two-step workflow (Framework commit → main repo pointer update)

---

### Mistake 5: Choosing Option B on Q5 (Pointer out of sync)

**Why Students Choose This:**
- Similar error message (reference-related)
- Confuse with Scenario 1 from training

**Fix:**
- Explain: "reference is not a tree" = commit missing, not pointer sync
- Demo: Force-push scenario (create missing commit)
- Show: Recovery procedure (find nearest commit)

---

## ✅ QUIZ SUCCESS CHECKLIST

**Before Quiz:**
- [ ] Print 9 quiz forms
- [ ] Prepare stopwatch (15-minute timer)
- [ ] Have answer key ready (this document)
- [ ] Prepare red/green pens for grading

**During Quiz:**
- [ ] Distribute quiz forms
- [ ] Set 15-minute timer
- [ ] Monitor for collaboration (remind: individual work)
- [ ] Collect quizzes when time expires

**After Quiz:**
- [ ] Grade all quizzes (use answer key)
- [ ] Calculate scores (__/5)
- [ ] Mark PASS/RETAKE
- [ ] Announce results
- [ ] Schedule retakes if needed

**Evidence Collection:**
- [ ] Scan or photocopy quiz forms
- [ ] Record scores in tracking sheet
- [ ] Calculate pass rate (9/9 = 100% required)
- [ ] Submit to CTO (Dec 11 EOD)

---

**Document Owner:** PM/PO (Quiz Administrator)
**Created:** December 9, 2025
**Status:** READY FOR USE
**First Use:** Dec 10, 2025 (Group 1)

---

**Instructor Notes:**
> "Be fair but rigorous - 4/5 threshold is non-negotiable."
> "If >20% fail, issue with training quality (not student fault)."
> "Retakes are learning opportunities, not punishments."
> "100% certification required by Dec 11 EOD (Week 2 blocker)."

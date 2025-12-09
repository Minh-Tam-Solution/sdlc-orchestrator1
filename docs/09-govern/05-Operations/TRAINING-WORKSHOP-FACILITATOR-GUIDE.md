# Training Workshop Facilitator Guide
## Quick Reference for Live Execution

**Purpose:** Step-by-step guide for PM/PO to run the 90-minute workshop
**Use with:** TRAINING-WORKSHOP-PRESENTATION.md (slides) + TRAINING-WORKSHOP-DEMO-SCRIPTS.md (labs)

---

## ⏱️ QUICK TIMELINE (90 min total)

```
[00:00-02:00]  Welcome & Overview
[02:00-30:00]  SESSION 1: Submodule Basics (28 min)
[30:00-40:00]  LAB 1: Clone with Submodule (10 min)
[40:00-45:00]  BREAK (5 min)
[45:00-65:00]  SESSION 2: Daily Operations (20 min)
[65:00-75:00]  LAB 2: Update After Pull (10 min)
[75:00-85:00]  LAB 3: Two-Step Workflow (10 min)
[85:00-90:00]  QUIZ (5 min)
```

---

## 🎬 SECTION-BY-SECTION GUIDE

### [00:00] WELCOME (2 min)

**Say:**
> "Good morning/afternoon everyone! Welcome to the SDLC-Enterprise-Framework Submodule Training.
>
> Today's workshop is **90 minutes** with 3 hands-on labs and a 5-question quiz at the end.
>
> **Important:** This is CTO-mandated training. Week 2 execution is BLOCKED until everyone passes (4/5 on quiz).
>
> Let's make this count - by the end, you'll be confident working with git submodules."

**Do:**
- [ ] Take attendance (mark in execution log)
- [ ] Share screen showing Slide 1
- [ ] Verify everyone can see

---

### [02:00] SLIDE 2: What is a Git Submodule? (5 min)

**Say:**
> "A git submodule is simply a **repository inside a repository**.
>
> Look at this diagram - SDLC-Orchestrator is our main repo. Inside it, there's a folder called SDLC-Enterprise-Framework that's actually a separate git repository.
>
> The key insight: Framework has its **own commit history**, completely separate from the main repo."

**Demo (1 min):**
```bash
# Show .gitmodules file
cat .gitmodules

# Show submodule status
git submodule status

# Show Framework has separate .git
ls -la SDLC-Enterprise-Framework/
```

**Check Understanding:**
> "Quick question - if I commit a change in Framework, does that automatically appear in Orchestrator's history?"
> (Answer: No - they're separate)

---

### [07:00] SLIDE 3: Why Submodule for Framework? (5 min)

**Say:**
> "Why did we choose submodule instead of just having Framework as a regular folder?
>
> **Three reasons:**
> 1. **Clean separation** - Framework commits don't pollute main repo history
> 2. **Independent versioning** - Framework can be v5.1.0 while Orchestrator is v1.0.0
> 3. **Shareability** - Same Framework can be used by BFlow, NQH-Bot, MTEP projects
>
> This is the **Framework-First principle** in action."

**Real Example:**
> "For SE 3.0, we'll add SASE templates to Framework FIRST (Track 1), then build Orchestrator automation LATER (Track 2).
>
> Teams can use SASE manually even without Orchestrator - that's the power of Framework-First."

---

### [12:00] SLIDE 4: Framework-First in Practice (5 min)

**Show Wrong vs Right:**

**Wrong (show code):**
```python
# Hard-coded template in Orchestrator - VIOLATION!
template = """
# BriefingScript
{problem}
"""
```

**Right (show code):**
```python
# Read from Framework submodule - CORRECT!
template_path = "SDLC-Enterprise-Framework/03-Templates-Tools/SASE-Artifacts/BRS-Template.md"
template = open(template_path).read()
```

**Key Point:**
> "If we ever replace Orchestrator with a different tool, the Framework templates survive. That's why methodology goes in Framework, automation goes in Orchestrator."

---

### [17:00] SLIDES 5-6: Essential Commands (13 min)

**The 4 Must-Know Commands:**

**1. Clone with submodule:**
```bash
git clone --recurse-submodules https://github.com/.../SDLC-Orchestrator
```
> "Always use `--recurse-submodules` or you'll get an empty Framework folder!"

**2. Initialize after regular clone:**
```bash
git submodule init
git submodule update
# OR combined:
git submodule update --init --recursive
```
> "If someone forgot `--recurse-submodules`, these commands fix it."

**3. Update to tracked commit:**
```bash
git submodule update --init --recursive
```
> "After `git pull`, run this to update Framework to the commit Orchestrator expects."

**4. Get latest from Framework remote:**
```bash
git submodule update --remote
```
> "This gets the LATEST Framework changes, not just what Orchestrator tracks."

**Practice Prompt:**
> "Everyone open a terminal. Type these commands to see submodule status. Don't run them yet - just type."

---

### [30:00] LAB 1: Clone with Submodule (10 min)

**Instructor Demo (5 min):**

```bash
# Show WRONG way first
cd ~/Desktop
git clone https://github.com/Minh-Tam-Solution/SDLC-Orchestrator WRONG-DEMO
ls WRONG-DEMO/SDLC-Enterprise-Framework/
# Empty! This is the problem.

rm -rf WRONG-DEMO

# Show RIGHT way
git clone --recurse-submodules https://github.com/Minh-Tam-Solution/SDLC-Orchestrator RIGHT-DEMO
ls RIGHT-DEMO/SDLC-Enterprise-Framework/
# All files present!
```

**Student Exercise (5 min):**
> "Now you try. Clone the repo to your Desktop using `--recurse-submodules`. Verify Framework folder has content.
>
> Raise hand when done or if you hit an issue."

**Verification:**
- [ ] All students have cloned successfully
- [ ] All students see Framework content

---

### [40:00] BREAK (5 min)

> "Take 5 minutes. Grab coffee. We'll continue with daily operations at [time]."

---

### [45:00] SLIDE 7: When to Update Submodule (10 min)

**Say:**
> "When do you need to update the submodule? **Two scenarios:**
>
> **Scenario 1:** After `git pull` on main repo
> - Someone else updated the Framework pointer
> - You need to sync your local Framework to match
>
> **Scenario 2:** You want the latest Framework changes
> - Framework team pushed new templates
> - You want them even if Orchestrator hasn't updated pointer yet"

**Commands:**
```bash
# Scenario 1: Sync to tracked commit
git pull
git submodule update --init --recursive

# Scenario 2: Get latest from remote
git submodule update --remote
git add SDLC-Enterprise-Framework
git commit -m "chore: Update Framework to latest"
```

---

### [55:00] SLIDE 8: Two-Step Commit Workflow (10 min)

**Critical Concept:**
> "When you modify Framework, you need **TWO commits**:
>
> **Commit 1:** In Framework repo (the actual change)
> **Commit 2:** In main repo (update pointer to new commit)
>
> If you only do Commit 1, your change exists in Framework but Orchestrator still points to the OLD commit."

**Show Diagram:**
```
Step 1: Make change in Framework
cd SDLC-Enterprise-Framework
# edit file
git add .
git commit -m "feat: Add template"
git push

Step 2: Update pointer in Orchestrator
cd ..
git add SDLC-Enterprise-Framework
git commit -m "chore: Update Framework"
git push
```

---

### [65:00] LAB 2: Update After Pull (10 min)

**Instructor Demo (5 min):**
```bash
# Simulate pulling changes that updated Framework
cd ~/Desktop/RIGHT-DEMO
git pull origin main

# Show Framework might be out of sync
git status
# May show: "new commits" for submodule

# Update submodule
git submodule update --init --recursive

# Verify
git status
# Clean!
```

**Student Exercise (5 min):**
> "Pull latest changes and update your submodule. Verify clean status."

---

### [75:00] LAB 3: Two-Step Commit Workflow (10 min)

**Instructor Demo (5 min):**
```bash
# Step 1: Make change in Framework
cd SDLC-Enterprise-Framework
echo "# Test file for training" > test-training.md
git add test-training.md
git commit -m "test: Training workshop verification"
# Don't push (or push to personal branch)

# Step 2: Update pointer in Orchestrator
cd ..
git status
# Shows: "modified: SDLC-Enterprise-Framework (new commits)"

git add SDLC-Enterprise-Framework
git commit -m "chore: Training workshop test commit"
# Don't push
```

**Student Exercise (5 min):**
> "Create a test file in Framework, commit it, then commit the pointer update in main repo.
>
> Do NOT push - this is just practice."

**Cleanup:**
```bash
# Revert test commits
git reset HEAD~1
cd SDLC-Enterprise-Framework
git reset HEAD~1
rm test-training.md
```

---

### [85:00] QUIZ (5 min)

**Say:**
> "Final part - 5 multiple choice questions. You need 4/5 to pass.
>
> I'll read each question. Write your answer (A, B, C, or D) on paper.
>
> We'll grade together at the end."

**Read Questions:**

**Q1:** Which command correctly clones WITH submodule?
- A) `git clone URL`
- B) `git clone --recurse-submodules URL`
- C) `git clone --submodules URL`
- D) `git clone && git submodule init`

**Q2:** After `git pull`, what updates the Framework?
- A) `git submodule pull`
- B) `git submodule update --init --recursive`
- C) `git pull --submodules`
- D) `cd Framework && git pull`

**Q3:** How many commits for Framework changes?
- A) 1 (main repo only)
- B) 1 (Framework only)
- C) 2 (Framework first, then main repo)
- D) 3 (Framework, main, push)

**Q4:** Where should SASE templates go FIRST?
- A) `Orchestrator/backend/templates/`
- B) `Framework/03-Templates-Tools/`
- C) `Orchestrator/docs/templates/`
- D) Either A or B

**Q5:** Get LATEST Framework changes (not tracked)?
- A) `git submodule update`
- B) `git submodule update --remote`
- C) `git pull origin main`
- D) `git fetch --submodules`

**Answers:** B, B, C, B, B

**Grade:**
> "Exchange papers with neighbor and grade. Answers are: B, B, C, B, B.
>
> Raise hand if you got 4 or 5 correct. (Mark in execution log)"

---

## ✅ POST-SESSION CHECKLIST

After each session:
- [ ] Record attendance in execution log
- [ ] Record quiz scores
- [ ] Record lab completion status
- [ ] Note any issues or questions raised
- [ ] Screenshot attendance + quiz results

After both sessions:
- [ ] Complete execution log summary
- [ ] Prepare evidence package for CTO
- [ ] Submit by Dec 11 EOD

---

## 🚨 TROUBLESHOOTING

**Issue: Student can't clone (permission denied)**
```bash
# Check SSH key
ssh -T git@github.com

# Or use HTTPS with credentials
git clone https://github.com/...
# Enter username + PAT token
```

**Issue: Submodule shows "detached HEAD"**
```bash
# This is normal for submodules
# They track a specific commit, not a branch
git submodule status
# Will show commit hash, not branch name
```

**Issue: Empty Framework after clone**
```bash
git submodule init
git submodule update
```

**Issue: Merge conflict in submodule**
```bash
cd SDLC-Enterprise-Framework
git status
# Resolve conflicts
git add .
git commit -m "Resolve submodule conflict"
cd ..
git add SDLC-Enterprise-Framework
git commit -m "Update Framework after conflict resolution"
```

---

**Document Version:** 1.0.0
**For Use With:** Training Workshop Dec 10-11, 2025

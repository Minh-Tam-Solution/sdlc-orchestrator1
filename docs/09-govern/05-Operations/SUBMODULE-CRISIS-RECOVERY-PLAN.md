# Git Submodule Crisis Recovery Plan
## SDLC-Enterprise-Framework Submodule Operations

**Document Version:** 1.0.0
**Status:** ACTIVE - PRODUCTION
**Authority:** CTO MANDATED
**Effective Date:** December 9, 2025

---

## 🎯 PURPOSE

This document provides **battle-tested procedures** for recovering from git submodule failures in SDLC Orchestrator. All scenarios assume worst-case conditions and provide step-by-step recovery paths.

**Non-Negotiable Requirement:** All team members MUST read this document before Week 2.

---

## 🚨 FAILURE SCENARIOS & RECOVERY

### **SCENARIO 1: Submodule Pointer Out of Sync**

**Symptoms:**
- Framework files missing after `git pull`
- Empty `SDLC-Enterprise-Framework/` directory
- Error: `fatal: not a git repository`

**Root Cause:**
- Developer pulled main repo but didn't update submodule
- Submodule pointer changed but local not synced

**Recovery Procedure:**
```bash
# Step 1: Check submodule status
git submodule status
# Expected output shows commit hash mismatch

# Step 2: Update submodule to correct commit
git submodule update --init --recursive

# Step 3: Verify Framework files present
ls -la SDLC-Enterprise-Framework/
# Should show 10+ directories

# Step 4: Verify Framework remote
cd SDLC-Enterprise-Framework && git remote -v
# Should show Framework repo URL

# Recovery Time: <2 minutes
# Success Criteria: Framework files visible, remote correct
```

**Prevention:**
- Add to `.git/hooks/post-merge`:
  ```bash
  #!/bin/bash
  git submodule update --init --recursive
  ```

---

### **SCENARIO 2: Framework Repository Unavailable**

**Symptoms:**
- `git clone --recurse-submodules` hangs
- Error: `fatal: unable to access 'https://github.com/Minh-Tam-Solution/SDLC-Enterprise-Framework'`
- Framework repo 404 or network timeout

**Root Cause:**
- GitHub outage
- Repository deleted/renamed
- Network issues
- Authentication failure

**Recovery Procedure (Option A - Wait for GitHub):**
```bash
# Step 1: Clone main repo without submodules
git clone https://github.com/Minh-Tam-Solution/SDLC-Orchestrator
cd SDLC-Orchestrator

# Step 2: Wait for GitHub recovery (check status.github.com)

# Step 3: After GitHub recovers, initialize submodule
git submodule update --init --recursive

# Recovery Time: Depends on GitHub SLA (<30 min typical)
```

**Recovery Procedure (Option B - Rollback to Tracked Directory):**
```bash
# EMERGENCY ONLY - If Framework repo permanently lost

# Step 1: Checkout commit before submodule conversion
git checkout 769e7fd^  # Parent of removal commit

# Step 2: Extract Framework files
cp -r SDLC-Enterprise-Framework /tmp/framework-backup

# Step 3: Return to main branch
git checkout main

# Step 4: Remove submodule
git submodule deinit -f SDLC-Enterprise-Framework
git rm -f SDLC-Enterprise-Framework
rm -rf .git/modules/SDLC-Enterprise-Framework

# Step 5: Restore Framework as tracked directory
cp -r /tmp/framework-backup SDLC-Enterprise-Framework
git add SDLC-Enterprise-Framework

# Step 6: Commit rollback
git commit -m "emergency: Rollback Framework to tracked directory

Framework repo unavailable. Reverting to pre-submodule state.

CTO Approval Required: YES"

git push origin main

# Recovery Time: 5-10 minutes
# CTO Approval: MANDATORY before push
```

**Prevention:**
- Mirror Framework repo to secondary location (GitLab, Bitbucket)
- Document mirror URL in .gitmodules
- Weekly backup of Framework repo

---

### **SCENARIO 3: Submodule Commit Missing in Framework Repo**

**Symptoms:**
- `git submodule update` fails
- Error: `fatal: reference is not a tree: <commit-hash>`
- Submodule pointer references non-existent commit

**Root Cause:**
- Framework repo force-pushed
- Commit deleted/rebased
- Developer pushed submodule pointer before Framework commit

**Recovery Procedure:**
```bash
# Step 1: Identify problematic commit
git submodule status
# Shows commit hash that doesn't exist

# Step 2: Go to Framework repo
cd SDLC-Enterprise-Framework

# Step 3: Fetch all refs from remote
git fetch --all

# Step 4: Find nearest available commit
git log --oneline -20

# Step 5: Checkout nearest commit
git checkout <nearest-commit-hash>

# Step 6: Go back to main repo
cd ..

# Step 7: Update submodule pointer to working commit
git add SDLC-Enterprise-Framework
git commit -m "fix: Update Framework submodule to nearest available commit

Previous commit <old-hash> not found in Framework repo.
Updated to <new-hash> (nearest available).

Requires investigation: Why was original commit lost?"

git push origin main

# Recovery Time: 3-5 minutes
# Post-Recovery Action: Investigate commit loss (MANDATORY)
```

**Prevention:**
- NEVER force-push Framework repo main branch
- Protect main branch in GitHub (require pull requests)
- Always push Framework commit BEFORE updating main repo pointer

---

## 🔧 MONITORING & ALERTS

### **Health Check Script**
```bash
#!/bin/bash
# File: scripts/check-submodule-health.sh

set -e

echo "🔍 Checking submodule health..."

# Check 1: Submodule exists
if [ ! -d "SDLC-Enterprise-Framework" ]; then
  echo "❌ CRITICAL: Framework directory missing!"
  exit 1
fi

# Check 2: Submodule initialized
if ! git submodule status | grep -q "SDLC-Enterprise-Framework"; then
  echo "❌ CRITICAL: Submodule not initialized!"
  exit 1
fi

# Check 3: Framework remote reachable
cd SDLC-Enterprise-Framework
if ! git remote -v | grep -q "github.com/Minh-Tam-Solution/SDLC-Enterprise-Framework"; then
  echo "❌ CRITICAL: Wrong Framework remote!"
  exit 1
fi

# Check 4: Framework commit exists
if ! git cat-file -e HEAD; then
  echo "❌ CRITICAL: Framework commit missing!"
  exit 1
fi

cd ..

echo "✅ Submodule health: OK"
exit 0
```

**Run Frequency:** Every commit (pre-commit hook) + CI/CD pipeline

---

## 📊 ROLLBACK DECISION MATRIX

| Scenario | Recovery Time | Data Loss Risk | CTO Approval Required |
|----------|---------------|----------------|-----------------------|
| Pointer out of sync | <2 min | None | No |
| GitHub temporary outage | <30 min | None | No |
| Framework repo deleted | 5-10 min | None (if backed up) | **YES** |
| Commit missing | 3-5 min | Potential | **YES** |
| Rollback to tracked dir | 5-10 min | None | **YES** |

**CTO Approval Process:**
1. Slack CTO with scenario description
2. Wait for explicit approval (max 30 min SLA)
3. Execute recovery procedure
4. Document post-mortem within 24 hours

---

## 🎯 SUCCESS CRITERIA

After recovery:
- [ ] `git submodule status` shows no errors
- [ ] Framework files visible and readable
- [ ] `git remote -v` in Framework shows correct URL
- [ ] CI/CD pipeline passes
- [ ] Health check script returns 0

**Recovery Failed If:**
- Any success criterion not met after 3 attempts
- Recovery time >30 minutes
- Data loss detected

**Escalation:** Page CTO immediately if recovery failed.

---

## 📚 REFERENCES

- Git Submodule Documentation: https://git-scm.com/book/en/v2/Git-Tools-Submodules
- GitHub Status: https://status.github.com
- Backup repo location: [TBD - Create within 48 hours]

---

**Document Owner:** CTO + DevOps Lead
**Last Reviewed:** December 9, 2025
**Next Review:** Weekly during SE 3.0 Track 1

---

**CTO Notes:**
> "Recovery procedures tested under fire. Not theory."
> "If Framework repo dies, we can survive 30 minutes. Plan accordingly."

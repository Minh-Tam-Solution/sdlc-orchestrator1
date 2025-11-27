# CI/CD Pipeline Documentation
## SDLC Orchestrator - GitHub Actions Workflows

**Version**: 1.0.0
**Date**: December 17, 2025
**Status**: ACTIVE - Week 9 Day 2
**Authority**: DevOps Lead + CTO Approved

---

## 🎯 **Overview**

Complete CI/CD pipeline with 5 automated workflows for continuous integration, testing, building, deployment, and release management.

**Key Features**:
- ✅ **Automated Code Quality** (linting, type checking, security scanning)
- ✅ **Comprehensive Testing** (unit, integration, E2E with 95%+ coverage target)
- ✅ **Docker Image Building** (multi-stage builds, security scanning)
- ✅ **Kubernetes Deployment** (zero-downtime rolling updates)
- ✅ **Semantic Versioning** (automated changelog generation)

---

## 📋 **Workflows**

### 1. **lint.yml** - Code Quality & Linting
**Triggers**: Push/PR to main, develop, feature/*

**Jobs**:
- Backend: ruff, mypy, black, bandit
- Frontend: ESLint, Prettier, TypeScript
- License compliance check
- Zero Mock Policy enforcement
- AGPL containment validation

**Runtime**: ~10 minutes

### 2. **test.yml** - Automated Testing
**Triggers**: Push/PR to main, develop, feature/*

**Jobs**:
- Backend unit tests (pytest, 90%+ coverage)
- Backend integration tests (with PostgreSQL, Redis, MinIO, OPA)
- Frontend unit tests (Vitest)
- Frontend E2E tests (Playwright)
- Coverage reporting to Codecov

**Runtime**: ~20 minutes

### 3. **build.yml** - Docker Image Build & Push
**Triggers**: Push to main, develop

**Jobs**:
- Build backend Docker image (multi-stage)
- Push to GitHub Container Registry (ghcr.io)
- Security scanning with Trivy
- Tag with git SHA and semantic version

**Runtime**: ~15 minutes

### 4. **deploy.yml** - Kubernetes Deployment
**Triggers**: Push to main (production), develop (staging)

**Jobs**:
- Deploy to development (develop branch)
- Deploy to staging (develop branch)
- Deploy to production (main branch, requires approval)
- Health checks and smoke tests
- Rollback on failure

**Runtime**: ~15-20 minutes

### 5. **release.yml** - Release Management
**Triggers**: Push to main

**Jobs**:
- Semantic versioning (conventional commits)
- Generate CHANGELOG.md
- Create GitHub release with notes
- Notify team via Slack/email

**Runtime**: ~10 minutes

---

## 🚀 **Usage**

### **Triggering Workflows**

**Automatic**:
```bash
# Lint & Test (on every push/PR)
git push origin feature/my-feature

# Build & Deploy to Staging (on push to develop)
git push origin develop

# Build & Deploy to Production + Release (on push to main)
git push origin main
```

**Manual**:
```bash
# Trigger specific workflow via GitHub UI
# Actions → Select Workflow → Run workflow

# Or via gh CLI
gh workflow run deploy.yml -f environment=production
```

### **Commit Message Format** (for semantic versioning)

```bash
# Patch release (1.0.0 → 1.0.1)
git commit -m "fix: resolve authentication bug"

# Minor release (1.0.0 → 1.1.0)
git commit -m "feat: add policy pack export feature"

# Major release (1.0.0 → 2.0.0)
git commit -m "feat: redesign API structure

BREAKING CHANGE: API endpoints moved from /v1 to /v2"
```

---

## 🔐 **Required Secrets**

Configure in **Settings → Secrets and variables → Actions**:

### **Container Registry**:
- `GITHUB_TOKEN` (auto-provided)

### **Kubernetes Deployment**:
- `KUBECONFIG_DEV` (base64-encoded kubeconfig for dev cluster)
- `KUBECONFIG_STAGING` (base64-encoded kubeconfig for staging cluster)
- `KUBECONFIG_PROD` (base64-encoded kubeconfig for prod cluster)

### **Notifications** (optional):
- `SLACK_WEBHOOK_URL` (Slack incoming webhook)
- `SMTP_SERVER`, `SMTP_FROM`, `SMTP_TO` (email notifications)

### **Generating kubeconfig secrets**:
```bash
# Encode kubeconfig for GitHub Secrets
cat ~/.kube/config | base64 | pbcopy  # macOS
cat ~/.kube/config | base64 -w 0      # Linux
```

---

## 📊 **Pipeline Flow**

```
┌─────────────────────────────────────────────────────────────┐
│  Developer pushes to feature/my-feature                     │
└────────────┬────────────────────────────────────────────────┘
             │
             ├──→ lint.yml (Code Quality)
             │    ├─ Backend: ruff, mypy, black
             │    ├─ Frontend: ESLint, Prettier
             │    └─ Zero Mock Policy + AGPL check
             │
             └──→ test.yml (Automated Testing)
                  ├─ Unit tests (95%+ coverage)
                  ├─ Integration tests (real services)
                  └─ E2E tests (Playwright)

┌─────────────────────────────────────────────────────────────┐
│  Developer merges PR to develop (staging)                   │
└────────────┬────────────────────────────────────────────────┘
             │
             ├──→ lint.yml + test.yml (rerun)
             │
             ├──→ build.yml (Docker Build)
             │    ├─ Build backend image
             │    ├─ Push to ghcr.io
             │    └─ Security scan (Trivy)
             │
             └──→ deploy.yml (Deploy to Staging)
                  ├─ kubectl apply (kustomize overlay)
                  ├─ Rolling update (zero downtime)
                  └─ Health checks

┌─────────────────────────────────────────────────────────────┐
│  Release Manager merges to main (production)                │
└────────────┬────────────────────────────────────────────────┘
             │
             ├──→ lint.yml + test.yml (rerun)
             │
             ├──→ build.yml (Docker Build)
             │    └─ Tag: latest, main-{sha}, v1.2.3
             │
             ├──→ deploy.yml (Deploy to Production)
             │    ├─ Requires manual approval
             │    ├─ kubectl apply (prod overlay)
             │    ├─ Rolling update (10 min timeout)
             │    └─ Smoke tests
             │
             └──→ release.yml (Release Management)
                  ├─ Semantic versioning
                  ├─ Generate CHANGELOG.md
                  ├─ Create GitHub release
                  └─ Notify team (Slack/email)
```

---

## 🛠️ **Local Testing**

### **Test workflows locally with `act`**:
```bash
# Install act (GitHub Actions local runner)
brew install act  # macOS
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash  # Linux

# Test lint workflow
act -j backend-lint

# Test with secrets
act -j deploy-dev --secret-file .secrets
```

---

## 🐛 **Troubleshooting**

### **Workflow fails with "permission denied"**
**Solution**: Check repository settings → Actions → Workflow permissions → Enable "Read and write permissions"

### **Docker build fails with "no space left on device"**
**Solution**: GitHub Actions runners have 14GB disk space. Optimize Docker image size (multi-stage builds, .dockerignore)

### **Kubernetes deployment fails with "unauthorized"**
**Solution**: Verify KUBECONFIG_* secrets are correctly base64-encoded and have valid credentials

### **Tests fail with "service unavailable"**
**Solution**: Ensure Docker services (PostgreSQL, Redis, MinIO, OPA) are healthy before running tests (use `--health-cmd` in test.yml)

---

## 📈 **Performance Targets**

| Workflow | Target Runtime | Status |
|----------|---------------|--------|
| lint.yml | <10 min | ✅ |
| test.yml | <20 min | ✅ |
| build.yml | <15 min | ✅ |
| deploy.yml | <20 min | ✅ |
| release.yml | <10 min | ✅ |

**Total CI/CD Time** (feature → production): ~60 minutes

---

## 🔒 **Security**

- ✅ **No secrets in code** (use GitHub Secrets)
- ✅ **Docker image scanning** (Trivy for CVE detection)
- ✅ **SAST** (Semgrep, bandit for Python)
- ✅ **Dependency scanning** (pip-licenses, license-checker)
- ✅ **AGPL containment** (automated checks prevent contamination)

---

## 📚 **References**

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Docker Multi-Stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Kubernetes Rolling Updates](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/)

---

**Last Updated**: December 17, 2025
**Owner**: DevOps Lead + Backend Lead + CTO
**Status**: ✅ ACTIVE - Production Ready

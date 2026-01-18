# Sprint 73 Deployment Scripts

**Sprint:** 73 - Teams Integration
**Date:** February 10, 2026
**Authority:** DevOps + Backend Lead + CTO Approved

---

## 📁 Available Scripts

### 1. **deploy-sprint73-staging.sh** (14KB)
Automated deployment to staging environment.

**Usage:**
```bash
./scripts/deploy-sprint73-staging.sh
```

**Features:**
- Pre-flight checks (git status, required files)
- Database backup with S3 upload (optional)
- Backend code deployment
- Migration dry run + actual migration
- Frontend build and deployment
- Automated smoke tests
- Post-deployment verification
- Automatic rollback on error

**Timeline:** ~30 minutes

---

### 2. **deploy-sprint73-production.sh** (17KB)
Automated deployment to production environment (`sdlc.nhatquangholding.com`).

**Usage:**
```bash
./scripts/deploy-sprint73-production.sh
```

**Features:**
- Strict pre-flight checks
- MANDATORY S3 backup upload
- Production database migration with verification
- Frontend build and deployment
- Critical smoke tests
- Post-deployment monitoring setup
- Rollback capability

**Timeline:** ~60 minutes

---

## 🔧 Environment Variables

### Staging Deployment

```bash
# Required
export STAGING_DB_HOST="staging-db-server"
export STAGING_BACKEND_HOST="staging-backend-server"
export STAGING_FRONTEND_HOST="staging-frontend-server"

# Optional
export STAGING_DB_USER="postgres"  # default: postgres
export STAGING_DB_NAME="sdlc_orchestrator_staging"  # default
export S3_BUCKET="nqh-backups"  # optional for staging
```

### Production Deployment

```bash
# Required
export PROD_SERVER_HOST="sdlc.nhatquangholding.com"
export S3_BUCKET="nqh-backups"  # REQUIRED for production

# Optional
export PROD_DB_USER="postgres"  # default: postgres
export PROD_DB_NAME="sdlc_orchestrator"  # default
```

---

## 📋 Deployment Workflow

### Option 1: Staging → Production (RECOMMENDED)

```bash
# Step 1: Deploy to staging
./scripts/deploy-sprint73-staging.sh

# Step 2: Run E2E tests against staging
cd frontend/web
BASE_URL=https://staging.sdlc-orchestrator.nhatquangholding.com npm run test:e2e

# Step 3: Run integration tests
cd ../../backend
pytest tests/integration/test_sprint73_teams_integration.py -v

# Step 4: If all tests pass, deploy to production
cd ..
./scripts/deploy-sprint73-production.sh
```

### Option 2: Direct Production (HIGH RISK)

```bash
# Only if absolutely necessary and staging not available
./scripts/deploy-sprint73-production.sh
```

---

## ⚠️ Important Notes

### Database Backups

**Staging:**
- Backup created: `/tmp/pre_s73_migration_<timestamp>.sql`
- S3 upload: Optional (configure `S3_BUCKET`)
- Local copy: `./backups/pre_s73_migration_<timestamp>.sql`

**Production:**
- Backup created: `/tmp/pre_s73_migration_prod_<timestamp>.sql`
- S3 upload: **MANDATORY** (deployment fails if S3 unavailable)
- Local copy: `./backups/production/pre_s73_migration_<timestamp>.sql`

### Migration Verification

Both scripts verify migration with **0/0/0 check:**
- 0 users without `organization_id`
- 0 projects without `team_id`
- 0 projects without gates

If verification fails, deployment aborts.

### Rollback

**Automatic rollback on error:**
Scripts automatically offer rollback if any phase fails.

**Manual rollback:**
```bash
# Staging
./scripts/deploy-sprint73-staging.sh rollback

# Production
./scripts/deploy-sprint73-production.sh rollback
```

Rollback restores database from backup and restarts services.

---

## 🧪 Smoke Tests Included

### Staging Script Tests:
1. API health check (`/health`)
2. Organizations API accessibility
3. Teams API accessibility
4. Frontend load test

### Production Script Tests:
1. Frontend accessibility (200 OK)
2. API health check
3. Database integrity (org and team exist)
4. BUG #7 verification (gates exist)

---

## 📊 Deployment Phases

### Phase 1: Database Backup (5 min)
- Create timestamped backup
- Upload to S3 (production: MANDATORY)
- Save local copy

### Phase 2: Deploy Backend (10 min)
- Pull latest code
- Install dependencies
- Restart backend service
- Verify health check

### Phase 3: Run Migration (10 min)
- Dry run (SQL preview)
- User confirmation
- Actual migration
- Verification (0/0/0 check)

### Phase 4: Deploy Frontend (10 min)
- Build frontend (`npm run build`)
- Deploy files (rsync)
- Restart nginx
- Verify accessibility

### Phase 5: Smoke Tests (10 min)
- Automated test suite
- Manual verification recommended

### Phase 6: Post-Deployment (5 min)
- Collect monitoring data
- Document deployment
- CTO sign-off

---

## 🔒 Security Considerations

### SSH Access Required
Scripts require SSH access to:
- Database server (staging/production)
- Backend server
- Frontend server (if separate)

### AWS Credentials
Production deployment requires AWS CLI configured with S3 access.

### Database Credentials
Scripts use environment variables or defaults.
**Never commit credentials to git!**

---

## 📝 Logging

Both scripts create detailed logs:
- **Location:** `/tmp/sprint73_deployment_<timestamp>.log`
- **Content:** All commands, output, errors
- **Use:** Post-deployment audit, troubleshooting

**Save logs after deployment:**
```bash
cp /tmp/sprint73_deployment_*.log ./deployment-logs/
```

---

## ✅ Success Criteria

**Deployment successful if:**
- ✅ All pre-flight checks pass
- ✅ Database backup created and uploaded
- ✅ Migration completes with 0/0/0 verification
- ✅ Backend service healthy
- ✅ Frontend accessible
- ✅ All smoke tests pass

---

## 🐛 BUG #7 Verification

**Auto-gate creation verified by:**
1. Migration script backfills 5 gates per existing project
2. New project creation auto-creates 5 gates
3. Smoke test verifies gates exist in database

**Expected gates per project:**
- Planning Review (01-PLAN)
- Design Review (02-DESIGN)
- Code Review (03-BUILD)
- Test Review (05-TEST)
- Deploy Approval (06-DEPLOY)

---

## 📞 Support

**If deployment fails:**
1. Check deployment log: `/tmp/sprint73_deployment_*.log`
2. Review error messages
3. Run rollback if necessary
4. Contact DevOps team

**Common issues:**
- SSH connection timeout → Check network/firewall
- S3 upload failed → Verify AWS credentials
- Migration verification failed → Check database state
- Frontend build failed → Check npm dependencies

---

## 🎯 Next Steps After Deployment

### Staging:
1. Run E2E tests
2. Run integration tests
3. Manual browser testing
4. Document issues found

### Production:
1. Monitor for 24 hours
2. Run full E2E test suite
3. Verify critical user journeys
4. CTO sign-off
5. Update deployment log

---

**Scripts Status:** ✅ READY FOR USE
**Testing Status:** ⏳ PENDING DEPLOYMENT
**Approval:** ✅ DevOps + Backend Lead + CTO

**Last Updated:** February 10, 2026

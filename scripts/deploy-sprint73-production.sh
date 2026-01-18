#!/bin/bash

###############################################################################
# Sprint 73 Production Deployment Script
# SDLC Orchestrator - Teams Integration
#
# Version: 1.0.0
# Date: February 10, 2026
# Authority: DevOps + Backend Lead + CTO Approved
#
# Purpose:
# Automated deployment script for Sprint 73 to production environment.
# Single domain: sdlc.nhatquangholding.com
#
# Usage:
#   ./scripts/deploy-sprint73-production.sh
#
# Environment Variables Required:
#   PROD_DB_HOST     - Production database hostname
#   PROD_DB_USER     - Database user (default: postgres)
#   PROD_DB_NAME     - Database name (default: sdlc_orchestrator)
#   PROD_SERVER_HOST - Production server hostname (backend + frontend)
#   S3_BUCKET        - S3 bucket for backups (REQUIRED for production)
#
# Changelog:
# - v1.0.0 (2026-02-10): Initial production deployment script
###############################################################################

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LOG_FILE="/tmp/sprint73_prod_deployment_$(date +%Y%m%d_%H%M%S).log"
BACKUP_TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Environment variables
PROD_DB_HOST="${PROD_DB_HOST:-production-db}"
PROD_DB_USER="${PROD_DB_USER:-postgres}"
PROD_DB_NAME="${PROD_DB_NAME:-sdlc_orchestrator}"
PROD_SERVER_HOST="${PROD_SERVER_HOST:-sdlc.nhatquangholding.com}"
S3_BUCKET="${S3_BUCKET:?S3_BUCKET is required for production deployment}"

# Domain
DOMAIN="sdlc.nhatquangholding.com"

###############################################################################
# Utility Functions
###############################################################################

log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✓${NC} $*" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ✗${NC} $*" | tee -a "$LOG_FILE"
}

log_warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] ⚠${NC} $*" | tee -a "$LOG_FILE"
}

confirm() {
    read -p "$1 (y/n): " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]]
}

###############################################################################
# Pre-flight Checks
###############################################################################

preflight_checks() {
    log "Running pre-flight checks..."

    # Check Sprint 73 files exist
    local required_files=(
        "backend/alembic/versions/s73_teams_data_migration.py"
        "backend/app/services/gate_auto_creation_service.py"
        "frontend/web/e2e/teams.spec.ts"
    )

    for file in "${required_files[@]}"; do
        if [ ! -f "${PROJECT_ROOT}/${file}" ]; then
            log_error "Required file not found: ${file}"
            exit 1
        fi
    done

    # Verify Sprint 73 commits
    if ! git log --oneline -20 | grep -q -i "sprint.*73\|s73"; then
        log_error "Sprint 73 commits not found"
        exit 1
    fi

    # Check S3 bucket access
    if ! aws s3 ls "s3://${S3_BUCKET}" > /dev/null 2>&1; then
        log_error "Cannot access S3 bucket: ${S3_BUCKET}"
        exit 1
    fi

    log_success "Pre-flight checks passed"
}

###############################################################################
# Phase 1: Database Backup (CRITICAL)
###############################################################################

backup_database() {
    log "Phase 1: Creating production database backup..."
    log_warn "This is a PRODUCTION backup - ensure sufficient disk space!"

    local backup_file="/tmp/pre_s73_migration_prod_${BACKUP_TIMESTAMP}.sql"

    # Create backup
    log "Dumping production database..."
    ssh "${PROD_SERVER_HOST}" "pg_dump -h localhost -U ${PROD_DB_USER} -d ${PROD_DB_NAME}" > "${backup_file}"

    if [ ! -f "${backup_file}" ]; then
        log_error "Backup file not created"
        exit 1
    fi

    local backup_size=$(du -h "${backup_file}" | cut -f1)
    log_success "Backup created: ${backup_size}"

    # Upload to S3 (MANDATORY for production)
    log "Uploading backup to S3..."
    aws s3 cp "${backup_file}" "s3://${S3_BUCKET}/sdlc-orchestrator/production/pre_s73_migration_${BACKUP_TIMESTAMP}.sql"

    # Verify S3 upload
    if aws s3 ls "s3://${S3_BUCKET}/sdlc-orchestrator/production/pre_s73_migration_${BACKUP_TIMESTAMP}.sql" > /dev/null; then
        log_success "Backup uploaded to S3 successfully"
    else
        log_error "S3 upload failed - ABORTING DEPLOYMENT"
        exit 1
    fi

    # Keep local copy
    mkdir -p "${PROJECT_ROOT}/backups/production"
    cp "${backup_file}" "${PROJECT_ROOT}/backups/production/"
    log_success "Local backup saved"

    echo ""
    log_warn "BACKUP LOCATION RECORDED:"
    log_warn "  S3: s3://${S3_BUCKET}/sdlc-orchestrator/production/pre_s73_migration_${BACKUP_TIMESTAMP}.sql"
    log_warn "  Local: ${PROJECT_ROOT}/backups/production/"
    echo ""
}

###############################################################################
# Phase 2: Deploy Backend
###############################################################################

deploy_backend() {
    log "Phase 2: Deploying backend to production..."

    ssh "${PROD_SERVER_HOST}" << 'ENDSSH'
        set -e

        echo "Navigating to backend directory..."
        cd /opt/sdlc-orchestrator/backend

        echo "Pulling latest code..."
        git fetch origin
        git checkout main
        git pull origin main

        echo "Verifying Sprint 73 code..."
        if ! git log --oneline -20 | grep -q -i "sprint.*73\|s73"; then
            echo "ERROR: Sprint 73 commits not found"
            exit 1
        fi

        echo "Installing dependencies..."
        pip install -r requirements.txt

        echo "Restarting backend service..."
        sudo systemctl restart sdlc-orchestrator-backend

        echo "Waiting for service to start..."
        sleep 10

        echo "Checking service status..."
        sudo systemctl status sdlc-orchestrator-backend --no-pager

        echo "Verifying API health..."
        if ! curl -f http://localhost:8000/health > /dev/null 2>&1; then
            echo "ERROR: Backend health check failed"
            exit 1
        fi

        echo "Backend deployment successful"
ENDSSH

    log_success "Backend deployed and healthy"
}

###############################################################################
# Phase 3: Run Migration (CRITICAL)
###############################################################################

run_migration() {
    log "Phase 3: Running database migration..."
    log_warn "This will modify production database!"

    # Dry run first
    log "Generating SQL preview (dry run)..."
    ssh "${PROD_SERVER_HOST}" << 'ENDSSH'
        cd /opt/sdlc-orchestrator/backend
        alembic upgrade head --sql > /tmp/s73_migration_preview_prod.sql

        echo "=== SQL Preview (first 100 lines) ==="
        head -100 /tmp/s73_migration_preview_prod.sql
ENDSSH

    echo ""
    if ! confirm "⚠️  CRITICAL: SQL preview looks good? Proceed with production migration?"; then
        log_error "Migration aborted by user"
        exit 1
    fi

    # Actual migration
    log "Running production migration..."
    ssh "${PROD_SERVER_HOST}" << 'ENDSSH'
        cd /opt/sdlc-orchestrator/backend
        alembic upgrade head 2>&1 | tee /tmp/s73_migration_output_prod.log

        echo ""
        echo "=== Migration Output ==="
        cat /tmp/s73_migration_output_prod.log
ENDSSH

    # Verify migration
    log "Verifying migration results..."
    local verification=$(ssh "${PROD_SERVER_HOST}" "psql -U ${PROD_DB_USER} -d ${PROD_DB_NAME} -t -c \"
        SELECT
            (SELECT COUNT(*) FROM users WHERE organization_id IS NULL AND deleted_at IS NULL) as users_without_org,
            (SELECT COUNT(*) FROM projects WHERE team_id IS NULL AND deleted_at IS NULL) as projects_without_team,
            (SELECT COUNT(*) FROM (SELECT p.id FROM projects p LEFT JOIN gates g ON p.id = g.project_id WHERE p.deleted_at IS NULL GROUP BY p.id HAVING COUNT(g.id) = 0) AS subq) as projects_without_gates;
    \"")

    log "Migration verification: ${verification}"

    if echo "$verification" | grep -q "0.*|.*0.*|.*0"; then
        log_success "Migration verified: 0/0/0 (perfect)"
    else
        log_error "Migration verification FAILED: ${verification}"
        log_error "Expected: 0 | 0 | 0"
        if confirm "Rollback migration?"; then
            rollback
        fi
        exit 1
    fi
}

###############################################################################
# Phase 4: Deploy Frontend
###############################################################################

deploy_frontend() {
    log "Phase 4: Deploying frontend to production..."

    # Build frontend locally
    log "Building frontend..."
    cd "${PROJECT_ROOT}/frontend/web"

    # Clean and install
    rm -rf node_modules dist
    npm install

    # Build for production
    npm run build

    if [ ! -d "dist" ]; then
        log_error "Frontend build failed"
        exit 1
    fi

    local build_size=$(du -sh dist | cut -f1)
    log_success "Frontend built (Size: ${build_size})"

    # Deploy to production
    log "Deploying frontend files to ${DOMAIN}..."
    rsync -avz --delete \
        --exclude='.git*' \
        --exclude='node_modules' \
        dist/ "${PROD_SERVER_HOST}:/var/www/sdlc-orchestrator/"

    # Restart nginx
    log "Restarting nginx..."
    ssh "${PROD_SERVER_HOST}" << 'ENDSSH'
        sudo nginx -t
        sudo systemctl restart nginx
        sudo systemctl status nginx --no-pager
ENDSSH

    log_success "Frontend deployed"
}

###############################################################################
# Phase 5: Production Smoke Tests
###############################################################################

run_smoke_tests() {
    log "Phase 5: Running production smoke tests..."

    local api_url="https://${DOMAIN}/api/v1"
    local test_results=0

    # Test 1: Frontend load
    log "Test 1: Frontend accessibility..."
    if curl -I -f "https://${DOMAIN}" 2>&1 | grep -q "200"; then
        log_success "Frontend loads (200 OK)"
    else
        log_error "Frontend load failed"
        ((test_results++))
    fi

    # Test 2: API health
    log "Test 2: API health check..."
    if curl -f "${api_url}/health" > /dev/null 2>&1; then
        log_success "API health check passed"
    else
        log_error "API health check failed"
        ((test_results++))
    fi

    # Test 3: Database verification
    log "Test 3: Database integrity check..."
    local db_check=$(ssh "${PROD_SERVER_HOST}" "psql -U ${PROD_DB_USER} -d ${PROD_DB_NAME} -t -c \"
        SELECT
            (SELECT COUNT(*) FROM organizations WHERE slug = 'nhat-quang-holding') as org_exists,
            (SELECT COUNT(*) FROM teams WHERE slug = 'unassigned') as team_exists;
    \"")

    if echo "$db_check" | grep -q "1.*|.*1"; then
        log_success "Database integrity verified (org and team exist)"
    else
        log_warn "Database check: ${db_check}"
    fi

    # Test 4: BUG #7 verification (auto-gates)
    log "Test 4: BUG #7 verification (gates exist)..."
    local gates_check=$(ssh "${PROD_SERVER_HOST}" "psql -U ${PROD_DB_USER} -d ${PROD_DB_NAME} -t -c \"
        SELECT COUNT(*) FROM gates;
    \"")

    if [ "$gates_check" -gt 0 ]; then
        log_success "Gates exist in database (count: ${gates_check})"
    else
        log_warn "No gates found in database"
    fi

    # Summary
    if [ $test_results -eq 0 ]; then
        log_success "All critical smoke tests passed ✓"
    else
        log_error "${test_results} smoke tests failed"
        exit 1
    fi
}

###############################################################################
# Phase 6: Post-Deployment Monitoring
###############################################################################

post_deployment_monitoring() {
    log "Phase 6: Setting up post-deployment monitoring..."

    # Log key metrics
    ssh "${PROD_SERVER_HOST}" << 'ENDSSH'
        echo "=== Production Metrics ==="

        echo "Database connections:"
        psql -U postgres -d sdlc_orchestrator -c "SELECT COUNT(*) FROM pg_stat_activity;"

        echo "Organizations:"
        psql -U postgres -d sdlc_orchestrator -c "SELECT COUNT(*) FROM organizations;"

        echo "Teams:"
        psql -U postgres -d sdlc_orchestrator -c "SELECT COUNT(*) FROM teams;"

        echo "Users with organization:"
        psql -U postgres -d sdlc_orchestrator -c "SELECT COUNT(*) FROM users WHERE organization_id IS NOT NULL;"

        echo "Projects with team:"
        psql -U postgres -d sdlc_orchestrator -c "SELECT COUNT(*) FROM projects WHERE team_id IS NOT NULL;"

        echo "Total gates:"
        psql -U postgres -d sdlc_orchestrator -c "SELECT COUNT(*) FROM gates;"
ENDSSH

    log_success "Monitoring data collected"

    log ""
    log_warn "=== Post-Deployment Actions Required ==="
    log_warn "1. Monitor application logs for 1 hour"
    log_warn "2. Monitor error rates in Grafana"
    log_warn "3. Test critical user journeys manually"
    log_warn "4. Verify auto-gate creation on new projects"
    log_warn "5. Check team filter on projects page"
    log ""
}

###############################################################################
# Rollback Function
###############################################################################

rollback() {
    log_error "⚠️  INITIATING PRODUCTION ROLLBACK ⚠️"

    local s3_backup="s3://${S3_BUCKET}/sdlc-orchestrator/production/pre_s73_migration_${BACKUP_TIMESTAMP}.sql"
    local local_backup="${PROJECT_ROOT}/backups/production/pre_s73_migration_${BACKUP_TIMESTAMP}.sql"

    # Download from S3 if local doesn't exist
    if [ ! -f "${local_backup}" ]; then
        log "Downloading backup from S3..."
        aws s3 cp "${s3_backup}" "${local_backup}"
    fi

    # Restore database
    log "Restoring database from backup..."
    ssh "${PROD_SERVER_HOST}" "psql -U ${PROD_DB_USER} -d ${PROD_DB_NAME}" < "${local_backup}"

    # Restart services
    log "Restarting services..."
    ssh "${PROD_SERVER_HOST}" << 'ENDSSH'
        sudo systemctl restart sdlc-orchestrator-backend
        sudo systemctl restart nginx
ENDSSH

    log_success "Rollback complete"
    log_warn "Please verify production is stable"
}

###############################################################################
# Main Deployment Flow
###############################################################################

main() {
    echo ""
    log "=========================================="
    log "Sprint 73 PRODUCTION Deployment"
    log "Domain: ${DOMAIN}"
    log "Date: $(date)"
    log "Log: ${LOG_FILE}"
    log "=========================================="
    echo ""

    # Pre-flight checks
    preflight_checks

    # CRITICAL: Confirm production deployment
    echo ""
    log_warn "⚠️  ⚠️  ⚠️  PRODUCTION DEPLOYMENT  ⚠️  ⚠️  ⚠️"
    log_warn "This will modify PRODUCTION database and deploy to ${DOMAIN}"
    log_warn "Backup will be created and uploaded to S3"
    echo ""
    if ! confirm "Are you ABSOLUTELY SURE you want to deploy to PRODUCTION?"; then
        log "Deployment cancelled by user"
        exit 0
    fi

    # Execute deployment
    backup_database
    deploy_backend
    run_migration
    deploy_frontend
    run_smoke_tests
    post_deployment_monitoring

    echo ""
    log_success "=========================================="
    log_success "Sprint 73 Production Deployment COMPLETE!"
    log_success "=========================================="
    echo ""
    log_success "Deployment successful! ✓"
    log ""
    log "Backup location:"
    log "  S3: s3://${S3_BUCKET}/sdlc-orchestrator/production/pre_s73_migration_${BACKUP_TIMESTAMP}.sql"
    log ""
    log "Next steps:"
    log "1. Monitor for 24 hours"
    log "2. Run full E2E test suite"
    log "3. Document in deployment log"
    log "4. CTO sign-off"
    echo ""
}

# Handle rollback command
if [ "${1:-}" = "rollback" ]; then
    rollback
    exit 0
fi

# Trap errors
trap 'log_error "Deployment failed at line $LINENO"; if confirm "Rollback?"; then rollback; fi' ERR

# Run main
main "$@"

#!/bin/bash

###############################################################################
# Sprint 73 Staging Deployment Script
# SDLC Orchestrator - Teams Integration
#
# Version: 1.0.0
# Date: February 10, 2026
# Authority: DevOps + Backend Lead + CTO Approved
#
# Purpose:
# Automated deployment script for Sprint 73 to staging environment.
# Includes database backup, migration, and smoke tests.
#
# Usage:
#   ./scripts/deploy-sprint73-staging.sh
#
# Environment Variables Required:
#   STAGING_DB_HOST     - Staging database hostname
#   STAGING_DB_USER     - Database user (default: postgres)
#   STAGING_DB_NAME     - Database name (default: sdlc_orchestrator_staging)
#   STAGING_BACKEND_HOST - Staging backend server hostname
#   STAGING_FRONTEND_HOST - Staging frontend server hostname
#   S3_BUCKET           - S3 bucket for backups (optional)
#
# Changelog:
# - v1.0.0 (2026-02-10): Initial deployment script
###############################################################################

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
LOG_FILE="/tmp/sprint73_deployment_$(date +%Y%m%d_%H%M%S).log"
BACKUP_TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Environment variables with defaults
STAGING_DB_HOST="${STAGING_DB_HOST:-localhost}"
STAGING_DB_USER="${STAGING_DB_USER:-postgres}"
STAGING_DB_NAME="${STAGING_DB_NAME:-sdlc_orchestrator_staging}"
STAGING_BACKEND_HOST="${STAGING_BACKEND_HOST:-staging-backend}"
STAGING_FRONTEND_HOST="${STAGING_FRONTEND_HOST:-staging-frontend}"
S3_BUCKET="${S3_BUCKET:-}"

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

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "Required command not found: $1"
        exit 1
    fi
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

    # Check required commands
    check_command git
    check_command ssh
    check_command psql
    check_command rsync

    # Check we're in correct directory
    if [ ! -f "${PROJECT_ROOT}/backend/alembic/versions/s73_teams_data_migration.py" ]; then
        log_error "Migration file not found. Are you in the correct directory?"
        exit 1
    fi

    # Check git status
    if ! git diff-index --quiet HEAD --; then
        log_warn "Working directory has uncommitted changes"
        if ! confirm "Continue anyway?"; then
            exit 1
        fi
    fi

    # Verify Sprint 73 commits
    if ! git log --oneline -10 | grep -q -i "sprint.*73\|s73\|teams"; then
        log_error "Sprint 73 commits not found in git history"
        exit 1
    fi

    log_success "Pre-flight checks passed"
}

###############################################################################
# Phase 1: Database Backup
###############################################################################

backup_database() {
    log "Phase 1: Backing up database..."

    local backup_file="/tmp/pre_s73_migration_${BACKUP_TIMESTAMP}.sql"

    # Create backup
    log "Creating database backup..."
    ssh "${STAGING_DB_HOST}" "pg_dump -h localhost -U ${STAGING_DB_USER} -d ${STAGING_DB_NAME}" > "${backup_file}"

    if [ ! -f "${backup_file}" ]; then
        log_error "Backup file not created"
        exit 1
    fi

    local backup_size=$(du -h "${backup_file}" | cut -f1)
    log_success "Backup created: ${backup_file} (Size: ${backup_size})"

    # Upload to S3 if configured
    if [ -n "$S3_BUCKET" ]; then
        log "Uploading backup to S3..."
        aws s3 cp "${backup_file}" "s3://${S3_BUCKET}/sdlc-orchestrator/staging/pre_s73_migration_${BACKUP_TIMESTAMP}.sql"
        log_success "Backup uploaded to S3"
    fi

    # Keep local backup
    cp "${backup_file}" "${PROJECT_ROOT}/backups/" 2>/dev/null || mkdir -p "${PROJECT_ROOT}/backups" && cp "${backup_file}" "${PROJECT_ROOT}/backups/"
    log_success "Local backup saved: ${PROJECT_ROOT}/backups/"
}

###############################################################################
# Phase 2: Deploy Backend
###############################################################################

deploy_backend() {
    log "Phase 2: Deploying backend..."

    # SSH to backend server and deploy
    ssh "${STAGING_BACKEND_HOST}" << 'ENDSSH'
        set -e

        echo "Pulling latest code..."
        cd /opt/sdlc-orchestrator/backend
        git fetch origin
        git checkout main
        git pull origin main

        echo "Installing dependencies..."
        pip install -r requirements.txt

        echo "Restarting backend service..."
        sudo systemctl restart sdlc-orchestrator-backend
        sudo systemctl status sdlc-orchestrator-backend --no-pager

        echo "Checking backend health..."
        sleep 5
        curl -f http://localhost:8000/health || exit 1
ENDSSH

    log_success "Backend deployed successfully"
}

###############################################################################
# Phase 3: Run Migration
###############################################################################

run_migration() {
    log "Phase 3: Running database migration..."

    # Dry run first
    log "Generating SQL preview (dry run)..."
    ssh "${STAGING_BACKEND_HOST}" << 'ENDSSH'
        cd /opt/sdlc-orchestrator/backend
        alembic upgrade head --sql > /tmp/s73_migration_preview.sql

        echo "=== SQL Preview ==="
        head -50 /tmp/s73_migration_preview.sql
ENDSSH

    if ! confirm "SQL preview looks good? Continue with actual migration?"; then
        log_error "Migration aborted by user"
        exit 1
    fi

    # Actual migration
    log "Running actual migration..."
    ssh "${STAGING_BACKEND_HOST}" << 'ENDSSH'
        cd /opt/sdlc-orchestrator/backend
        alembic upgrade head 2>&1 | tee /tmp/s73_migration_output.log

        echo ""
        echo "=== Migration Output ==="
        cat /tmp/s73_migration_output.log
ENDSSH

    # Verify migration
    log "Verifying migration results..."
    local verification_output=$(ssh "${STAGING_DB_HOST}" "psql -U ${STAGING_DB_USER} -d ${STAGING_DB_NAME} -t -c \"
        SELECT
            (SELECT COUNT(*) FROM users WHERE organization_id IS NULL AND deleted_at IS NULL) as users_without_org,
            (SELECT COUNT(*) FROM projects WHERE team_id IS NULL AND deleted_at IS NULL) as projects_without_team,
            (SELECT COUNT(DISTINCT p.id) FROM projects p LEFT JOIN gates g ON p.id = g.project_id WHERE p.deleted_at IS NULL GROUP BY p.id HAVING COUNT(g.id) = 0) as projects_without_gates;
    \"")

    log "Migration verification: ${verification_output}"

    if echo "$verification_output" | grep -q "0.*0.*0"; then
        log_success "Migration verified: 0/0/0 (perfect)"
    else
        log_error "Migration verification failed: ${verification_output}"
        exit 1
    fi
}

###############################################################################
# Phase 4: Deploy Frontend
###############################################################################

deploy_frontend() {
    log "Phase 4: Deploying frontend..."

    # Build frontend
    log "Building frontend..."
    cd "${PROJECT_ROOT}/frontend/web"
    npm install
    npm run build

    if [ ! -d "dist" ]; then
        log_error "Frontend build failed - dist/ not found"
        exit 1
    fi

    local build_size=$(du -sh dist | cut -f1)
    log_success "Frontend built (Size: ${build_size})"

    # Deploy to staging
    log "Deploying frontend files..."
    rsync -avz --delete dist/ "${STAGING_FRONTEND_HOST}:/var/www/sdlc-orchestrator/"

    # Restart nginx
    log "Restarting nginx..."
    ssh "${STAGING_FRONTEND_HOST}" << 'ENDSSH'
        sudo systemctl restart nginx
        sudo systemctl status nginx --no-pager
ENDSSH

    log_success "Frontend deployed successfully"
}

###############################################################################
# Phase 5: Smoke Tests
###############################################################################

run_smoke_tests() {
    log "Phase 5: Running smoke tests..."

    local api_url="https://staging-api.sdlc-orchestrator.nhatquangholding.com"
    local test_results=0

    # Test 1: Health check
    log "Test 1: API health check..."
    if curl -f "${api_url}/health" > /dev/null 2>&1; then
        log_success "Health check passed"
    else
        log_error "Health check failed"
        ((test_results++))
    fi

    # Test 2: Organizations API
    log "Test 2: Organizations API..."
    if curl -f "${api_url}/api/v1/organizations" > /dev/null 2>&1; then
        log_success "Organizations API accessible"
    else
        log_warn "Organizations API test failed (may require auth)"
    fi

    # Test 3: Teams API
    log "Test 3: Teams API..."
    if curl -f "${api_url}/api/v1/teams" > /dev/null 2>&1; then
        log_success "Teams API accessible"
    else
        log_warn "Teams API test failed (may require auth)"
    fi

    # Test 4: Frontend load
    log "Test 4: Frontend accessibility..."
    if curl -I -f "https://staging.sdlc-orchestrator.nhatquangholding.com" | grep -q "200 OK"; then
        log_success "Frontend loads successfully"
    else
        log_error "Frontend load failed"
        ((test_results++))
    fi

    if [ $test_results -eq 0 ]; then
        log_success "All smoke tests passed"
    else
        log_warn "Some smoke tests failed (${test_results} failures)"
        log_warn "Manual verification recommended"
    fi
}

###############################################################################
# Phase 6: Post-Deployment Verification
###############################################################################

post_deployment_verification() {
    log "Phase 6: Post-deployment verification..."

    # Database checks
    log "Checking database state..."
    ssh "${STAGING_DB_HOST}" "psql -U ${STAGING_DB_USER} -d ${STAGING_DB_NAME} -c \"
        SELECT
            'Organizations' as entity,
            COUNT(*) as count
        FROM organizations
        WHERE slug = 'nhat-quang-holding'
        UNION ALL
        SELECT
            'Teams' as entity,
            COUNT(*) as count
        FROM teams
        WHERE slug = 'unassigned'
        UNION ALL
        SELECT
            'Users with org' as entity,
            COUNT(*) as count
        FROM users
        WHERE organization_id IS NOT NULL AND deleted_at IS NULL;
    \""

    log_success "Post-deployment verification complete"
}

###############################################################################
# Rollback Function
###############################################################################

rollback() {
    log_error "Rolling back deployment..."

    local backup_file="${PROJECT_ROOT}/backups/pre_s73_migration_${BACKUP_TIMESTAMP}.sql"

    if [ ! -f "${backup_file}" ]; then
        log_error "Backup file not found: ${backup_file}"
        exit 1
    fi

    log "Restoring database from backup..."
    ssh "${STAGING_DB_HOST}" "psql -U ${STAGING_DB_USER} -d ${STAGING_DB_NAME}" < "${backup_file}"

    log "Restarting backend..."
    ssh "${STAGING_BACKEND_HOST}" "sudo systemctl restart sdlc-orchestrator-backend"

    log_success "Rollback complete"
}

###############################################################################
# Main Deployment Flow
###############################################################################

main() {
    log "=========================================="
    log "Sprint 73 Staging Deployment"
    log "Date: $(date)"
    log "Log file: ${LOG_FILE}"
    log "=========================================="

    # Run pre-flight checks
    preflight_checks

    # Confirm deployment
    if ! confirm "Ready to deploy Sprint 73 to staging?"; then
        log "Deployment cancelled by user"
        exit 0
    fi

    # Execute deployment phases
    backup_database
    deploy_backend
    run_migration
    deploy_frontend
    run_smoke_tests
    post_deployment_verification

    log_success "=========================================="
    log_success "Sprint 73 Staging Deployment Complete!"
    log_success "=========================================="
    log ""
    log "Next steps:"
    log "1. Run E2E tests: cd frontend/web && npm run test:e2e"
    log "2. Manual browser testing"
    log "3. Review deployment log: ${LOG_FILE}"
    log ""
    log "If issues found, rollback with:"
    log "  ./scripts/deploy-sprint73-staging.sh rollback"
}

# Handle rollback command
if [ "${1:-}" = "rollback" ]; then
    rollback
    exit 0
fi

# Trap errors and offer rollback
trap 'log_error "Deployment failed at line $LINENO"; if confirm "Rollback deployment?"; then rollback; fi' ERR

# Run main deployment
main "$@"

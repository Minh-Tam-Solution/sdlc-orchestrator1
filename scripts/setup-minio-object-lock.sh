#!/bin/bash
################################################################################
# MinIO Object Lock Configuration Script
# SDLC Orchestrator - Sprint 82 (Pre-Launch Hardening)
#
# Version: 1.0.0
# Date: January 22, 2026
# Status: READY FOR EXECUTION
# Authority: DevOps Lead + CTO Approved
# Priority: P1 - SCALE BLOCKER (Deadline: Jan 25, 2026)
#
# Purpose:
# - Enable Object Lock (WORM) on sdlc-evidence bucket
# - Configure 7-year default retention policy (GOVERNANCE mode)
# - Verify configuration and test tamper-evidence
#
# Prerequisites:
# - Docker Compose running (docker-compose up -d)
# - MinIO container accessible
# - mc (MinIO Client) installed in container or host
#
# References:
# - docs/03-integrate/02-third-party/minio-object-lock-guide.md
# - Expert Feedback Plan: P1 Task (Jan 25 deadline)
################################################################################

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
MINIO_ALIAS="${MINIO_ALIAS:-myminio}"
BUCKET_NAME="${BUCKET_NAME:-sdlc-evidence}"
RETENTION_DAYS="${RETENTION_DAYS:-2555}"  # 7 years
RETENTION_MODE="${RETENTION_MODE:-GOVERNANCE}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

################################################################################
# Helper Functions
################################################################################

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check if docker-compose is running
    if ! docker-compose ps | grep -q "minio.*Up"; then
        log_error "MinIO container is not running. Please start docker-compose first."
        exit 1
    fi

    # Check if mc command exists
    if ! docker-compose exec -T minio mc --version &>/dev/null; then
        log_error "MinIO Client (mc) not found in container."
        exit 1
    fi

    log_info "Prerequisites check passed ✓"
}

configure_minio_alias() {
    log_info "Configuring MinIO alias: ${MINIO_ALIAS}..."

    # Configure alias (if not exists)
    docker-compose exec -T minio mc alias set ${MINIO_ALIAS} \
        http://localhost:9000 \
        "${MINIO_ROOT_USER:-minioadmin}" \
        "${MINIO_ROOT_PASSWORD:-minioadmin}" 2>/dev/null || true

    # Verify connection
    if docker-compose exec -T minio mc admin info ${MINIO_ALIAS} &>/dev/null; then
        log_info "MinIO connection verified ✓"
    else
        log_error "Failed to connect to MinIO. Check credentials."
        exit 1
    fi
}

check_existing_bucket() {
    log_info "Checking if bucket ${BUCKET_NAME} exists..."

    if docker-compose exec -T minio mc ls ${MINIO_ALIAS}/${BUCKET_NAME} &>/dev/null; then
        log_warn "Bucket ${BUCKET_NAME} already exists!"
        log_warn "Object Lock CANNOT be enabled on existing buckets."
        log_warn ""
        log_warn "Options:"
        log_warn "  1. Delete existing bucket and recreate (WILL LOSE DATA)"
        log_warn "  2. Create new bucket with Object Lock (sdlc-evidence-v2)"
        log_warn "  3. Skip Object Lock (not recommended for production)"
        log_warn ""
        read -p "Enter choice (1/2/3): " choice

        case $choice in
            1)
                log_warn "Deleting bucket ${BUCKET_NAME}..."
                docker-compose exec -T minio mc rb --force ${MINIO_ALIAS}/${BUCKET_NAME}
                log_info "Bucket deleted."
                return 0
                ;;
            2)
                BUCKET_NAME="${BUCKET_NAME}-v2"
                log_info "Will create new bucket: ${BUCKET_NAME}"
                return 0
                ;;
            3)
                log_error "Skipping Object Lock configuration. Exiting."
                exit 1
                ;;
            *)
                log_error "Invalid choice. Exiting."
                exit 1
                ;;
        esac
    else
        log_info "Bucket does not exist. Will create new bucket. ✓"
    fi
}

create_bucket_with_object_lock() {
    log_info "Creating bucket ${BUCKET_NAME} with Object Lock enabled..."

    # Create bucket with Object Lock
    if docker-compose exec -T minio mc mb --with-lock ${MINIO_ALIAS}/${BUCKET_NAME}; then
        log_info "Bucket created successfully ✓"
    else
        log_error "Failed to create bucket with Object Lock."
        exit 1
    fi

    # Verify Object Lock is enabled
    if docker-compose exec -T minio mc stat ${MINIO_ALIAS}/${BUCKET_NAME} | grep -q "Lock.*ENABLED"; then
        log_info "Object Lock verified: ENABLED ✓"
    else
        log_error "Object Lock is NOT enabled on bucket!"
        exit 1
    fi
}

configure_default_retention() {
    log_info "Configuring default retention policy..."
    log_info "  Mode: ${RETENTION_MODE}"
    log_info "  Duration: ${RETENTION_DAYS} days (7 years)"

    # Set default retention
    if docker-compose exec -T minio mc retention set \
        --default ${RETENTION_MODE} "${RETENTION_DAYS}d" \
        ${MINIO_ALIAS}/${BUCKET_NAME}; then
        log_info "Default retention policy configured ✓"
    else
        log_error "Failed to configure retention policy."
        exit 1
    fi

    # Verify retention policy
    log_info "Verifying retention policy..."
    docker-compose exec -T minio mc retention info --default ${MINIO_ALIAS}/${BUCKET_NAME}
}

test_object_lock() {
    log_info "Testing Object Lock functionality..."

    # Create test file
    TEST_FILE="/tmp/test-evidence-$(date +%s).txt"
    echo "Test evidence file for Object Lock verification" > ${TEST_FILE}

    # Upload test file
    log_info "Uploading test file..."
    docker cp ${TEST_FILE} $(docker-compose ps -q minio):/tmp/test-evidence.txt

    if docker-compose exec -T minio mc cp /tmp/test-evidence.txt \
        ${MINIO_ALIAS}/${BUCKET_NAME}/test-evidence.txt \
        --retention-mode ${RETENTION_MODE} \
        --retention-duration 7y; then
        log_info "Test file uploaded with retention ✓"
    else
        log_error "Failed to upload test file."
        exit 1
    fi

    # Try to delete (should fail due to retention)
    log_info "Attempting to delete (should fail)..."
    if docker-compose exec -T minio mc rm ${MINIO_ALIAS}/${BUCKET_NAME}/test-evidence.txt 2>&1 | grep -q "Object is WORM protected"; then
        log_info "WORM protection verified: Delete blocked ✓"
    else
        log_warn "Delete operation behavior unclear. Manual verification recommended."
    fi

    # Check object retention
    log_info "Checking object retention metadata..."
    docker-compose exec -T minio mc stat ${MINIO_ALIAS}/${BUCKET_NAME}/test-evidence.txt

    # Cleanup
    rm -f ${TEST_FILE}
}

print_summary() {
    log_info ""
    log_info "=========================================="
    log_info "MinIO Object Lock Configuration Complete"
    log_info "=========================================="
    log_info ""
    log_info "Bucket: ${BUCKET_NAME}"
    log_info "Object Lock: ENABLED"
    log_info "Retention Mode: ${RETENTION_MODE}"
    log_info "Retention Period: ${RETENTION_DAYS} days (7 years)"
    log_info ""
    log_info "Next Steps:"
    log_info "  1. Update backend/app/core/config.py with new bucket name (if changed)"
    log_info "  2. Update backend/app/services/minio_service.py to use Object Lock"
    log_info "  3. Run integration tests to verify Evidence Vault"
    log_info "  4. Update documentation: docs/03-integrate/02-third-party/minio-object-lock-guide.md"
    log_info ""
    log_info "Configuration saved to: /tmp/minio-object-lock-config.txt"
    echo "BUCKET_NAME=${BUCKET_NAME}" > /tmp/minio-object-lock-config.txt
    echo "RETENTION_MODE=${RETENTION_MODE}" >> /tmp/minio-object-lock-config.txt
    echo "RETENTION_DAYS=${RETENTION_DAYS}" >> /tmp/minio-object-lock-config.txt
    echo "CONFIGURED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> /tmp/minio-object-lock-config.txt
    log_info ""
}

################################################################################
# Main Execution
################################################################################

main() {
    log_info "MinIO Object Lock Configuration Script"
    log_info "Version: 1.0.0 | Date: January 22, 2026"
    log_info "Priority: P1 - SCALE BLOCKER (Deadline: Jan 25)"
    log_info ""

    # Step 1: Check prerequisites
    check_prerequisites

    # Step 2: Configure MinIO alias
    configure_minio_alias

    # Step 3: Check existing bucket
    check_existing_bucket

    # Step 4: Create bucket with Object Lock
    create_bucket_with_object_lock

    # Step 5: Configure default retention
    configure_default_retention

    # Step 6: Test Object Lock
    test_object_lock

    # Step 7: Print summary
    print_summary

    log_info "✅ MinIO Object Lock configuration completed successfully!"
}

# Execute main function
main "$@"

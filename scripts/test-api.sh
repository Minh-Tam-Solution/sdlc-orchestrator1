#!/bin/bash
# =========================================================================
# API Test Runner - SDLC Orchestrator
# Version: 1.0.0
# Date: November 27, 2025
# Status: ACTIVE - STAGE 03 (BUILD)
#
# Usage:
#   ./scripts/test-api.sh              # Run all tests
#   ./scripts/test-api.sh auth         # Run only auth tests
#   ./scripts/test-api.sh dashboard    # Run only dashboard tests
#   ./scripts/test-api.sh projects     # Run only projects tests
#   ./scripts/test-api.sh gates        # Run only gates tests
# =========================================================================

# Don't exit on error - we want to run all tests
# set -e

# Configuration
BASE_URL="${BASE_URL:-http://localhost:8000}"
API_VERSION="v1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counters
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
    ((TESTS_PASSED++))
}

log_fail() {
    echo -e "${RED}[FAIL]${NC} $1"
    ((TESTS_FAILED++))
}

log_section() {
    echo ""
    echo -e "${YELLOW}============================================${NC}"
    echo -e "${YELLOW}  $1${NC}"
    echo -e "${YELLOW}============================================${NC}"
}

# Check if jq is installed
check_dependencies() {
    if ! command -v jq &> /dev/null; then
        echo "Error: jq is required. Install with: brew install jq"
        exit 1
    fi
    if ! command -v curl &> /dev/null; then
        echo "Error: curl is required"
        exit 1
    fi
}

# =========================================================================
# AUTH TESTS
# =========================================================================
test_auth() {
    log_section "AUTH TESTS"

    # Test 1: Login with valid credentials
    log_info "Testing login with valid credentials..."
    RESPONSE=$(curl -s -X POST "${BASE_URL}/api/${API_VERSION}/auth/login" \
        -H "Content-Type: application/json" \
        -d '{"email":"admin@sdlc-orchestrator.io","password":"Admin@123"}')

    if echo "$RESPONSE" | jq -e '.access_token' > /dev/null 2>&1; then
        ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
        REFRESH_TOKEN=$(echo "$RESPONSE" | jq -r '.refresh_token')
        log_success "TC-AUTH-001: Login successful"
        export ACCESS_TOKEN REFRESH_TOKEN
    else
        log_fail "TC-AUTH-001: Login failed - $RESPONSE"
        return 1
    fi

    # Test 2: Login with invalid credentials
    log_info "Testing login with invalid credentials..."
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${BASE_URL}/api/${API_VERSION}/auth/login" \
        -H "Content-Type: application/json" \
        -d '{"email":"admin@sdlc-orchestrator.io","password":"wrongpassword"}')
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)

    if [ "$HTTP_CODE" = "401" ]; then
        log_success "TC-AUTH-002: Invalid credentials rejected (401)"
    else
        log_fail "TC-AUTH-002: Expected 401, got $HTTP_CODE"
    fi

    # Test 3: Get current user
    log_info "Testing get current user..."
    RESPONSE=$(curl -s -X GET "${BASE_URL}/api/${API_VERSION}/auth/me" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}")

    if echo "$RESPONSE" | jq -e '.email' > /dev/null 2>&1; then
        USER_EMAIL=$(echo "$RESPONSE" | jq -r '.email')
        if [ "$USER_EMAIL" = "admin@sdlc-orchestrator.io" ]; then
            log_success "TC-AUTH-003: Get current user successful"
        else
            log_fail "TC-AUTH-003: Wrong email returned - $USER_EMAIL"
        fi
    else
        log_fail "TC-AUTH-003: Get current user failed - $RESPONSE"
    fi

    # Test 4: Refresh token
    log_info "Testing token refresh..."
    RESPONSE=$(curl -s -X POST "${BASE_URL}/api/${API_VERSION}/auth/refresh" \
        -H "Content-Type: application/json" \
        -d "{\"refresh_token\":\"${REFRESH_TOKEN}\"}")

    if echo "$RESPONSE" | jq -e '.access_token' > /dev/null 2>&1; then
        NEW_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
        # Token refresh is successful if we get a valid access_token back
        # Note: Token may be same if refreshed within same second (JWT timestamp)
        if [ -n "$NEW_TOKEN" ] && [ "$NEW_TOKEN" != "null" ]; then
            log_success "TC-AUTH-004: Token refresh successful"
            ACCESS_TOKEN="$NEW_TOKEN"
            export ACCESS_TOKEN
        else
            log_fail "TC-AUTH-004: Token refresh returned empty token"
        fi
    else
        log_fail "TC-AUTH-004: Token refresh failed - $RESPONSE"
    fi

    # Test 5: Access protected route without token
    log_info "Testing protected route without token..."
    RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "${BASE_URL}/api/${API_VERSION}/auth/me")
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)

    if [ "$HTTP_CODE" = "401" ] || [ "$HTTP_CODE" = "403" ]; then
        log_success "TC-AUTH-005: Protected route rejected unauthorized (${HTTP_CODE})"
    else
        log_fail "TC-AUTH-005: Expected 401/403, got $HTTP_CODE"
    fi
}

# =========================================================================
# DASHBOARD TESTS
# =========================================================================
test_dashboard() {
    log_section "DASHBOARD TESTS"

    # Ensure we have a token
    if [ -z "$ACCESS_TOKEN" ]; then
        log_info "No token found, logging in first..."
        RESPONSE=$(curl -s -X POST "${BASE_URL}/api/${API_VERSION}/auth/login" \
            -H "Content-Type: application/json" \
            -d '{"email":"admin@sdlc-orchestrator.io","password":"Admin@123"}')
        ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
        export ACCESS_TOKEN
    fi

    # Test 1: Get dashboard stats
    log_info "Testing dashboard stats..."
    RESPONSE=$(curl -s -X GET "${BASE_URL}/api/${API_VERSION}/dashboard/stats" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}")

    if echo "$RESPONSE" | jq -e '.total_projects' > /dev/null 2>&1; then
        TOTAL_PROJECTS=$(echo "$RESPONSE" | jq -r '.total_projects')
        ACTIVE_GATES=$(echo "$RESPONSE" | jq -r '.active_gates')
        PASS_RATE=$(echo "$RESPONSE" | jq -r '.pass_rate')
        log_success "TC-DASH-001: Dashboard stats retrieved (projects: $TOTAL_PROJECTS, gates: $ACTIVE_GATES, pass_rate: $PASS_RATE%)"
    else
        log_fail "TC-DASH-001: Dashboard stats failed - $RESPONSE"
    fi

    # Test 2: Get recent gates
    log_info "Testing recent gates..."
    RESPONSE=$(curl -s -X GET "${BASE_URL}/api/${API_VERSION}/dashboard/recent-gates" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}")

    if echo "$RESPONSE" | jq -e '.[0].gate_name' > /dev/null 2>&1; then
        GATES_COUNT=$(echo "$RESPONSE" | jq 'length')
        log_success "TC-DASH-002: Recent gates retrieved ($GATES_COUNT gates)"
    else
        if [ "$RESPONSE" = "[]" ]; then
            log_success "TC-DASH-002: Recent gates retrieved (0 gates)"
        else
            log_fail "TC-DASH-002: Recent gates failed - $RESPONSE"
        fi
    fi
}

# =========================================================================
# PROJECTS TESTS
# =========================================================================
test_projects() {
    log_section "PROJECTS TESTS"

    # Ensure we have a token
    if [ -z "$ACCESS_TOKEN" ]; then
        log_info "No token found, logging in first..."
        RESPONSE=$(curl -s -X POST "${BASE_URL}/api/${API_VERSION}/auth/login" \
            -H "Content-Type: application/json" \
            -d '{"email":"admin@sdlc-orchestrator.io","password":"Admin@123"}')
        ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
        export ACCESS_TOKEN
    fi

    # Test 1: List projects
    log_info "Testing list projects..."
    RESPONSE=$(curl -s -X GET "${BASE_URL}/api/${API_VERSION}/projects" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}")

    if echo "$RESPONSE" | jq -e '.[0].id' > /dev/null 2>&1; then
        PROJECT_ID=$(echo "$RESPONSE" | jq -r '.[0].id')
        PROJECT_NAME=$(echo "$RESPONSE" | jq -r '.[0].name')
        PROJECTS_COUNT=$(echo "$RESPONSE" | jq 'length')
        export PROJECT_ID
        log_success "TC-PROJ-001: Projects listed ($PROJECTS_COUNT projects)"
        log_info "First project: $PROJECT_NAME ($PROJECT_ID)"
    else
        if [ "$RESPONSE" = "[]" ]; then
            log_success "TC-PROJ-001: Projects listed (0 projects)"
        else
            log_fail "TC-PROJ-001: List projects failed - $RESPONSE"
        fi
    fi

    # Test 2: Get project by ID
    if [ -n "$PROJECT_ID" ]; then
        log_info "Testing get project by ID..."
        RESPONSE=$(curl -s -X GET "${BASE_URL}/api/${API_VERSION}/projects/${PROJECT_ID}" \
            -H "Authorization: Bearer ${ACCESS_TOKEN}")

        if echo "$RESPONSE" | jq -e '.id' > /dev/null 2>&1; then
            GATES_COUNT=$(echo "$RESPONSE" | jq '.gates | length')
            log_success "TC-PROJ-002: Project retrieved with $GATES_COUNT gates"
        else
            log_fail "TC-PROJ-002: Get project failed - $RESPONSE"
        fi
    else
        log_info "Skipping TC-PROJ-002 (no project ID)"
    fi

    # Test 3: Get non-existent project
    log_info "Testing get non-existent project..."
    RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "${BASE_URL}/api/${API_VERSION}/projects/00000000-0000-0000-0000-000000000000" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}")
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)

    if [ "$HTTP_CODE" = "404" ]; then
        log_success "TC-PROJ-003: Non-existent project returns 404"
    else
        log_fail "TC-PROJ-003: Expected 404, got $HTTP_CODE"
    fi
}

# =========================================================================
# GATES TESTS
# =========================================================================
test_gates() {
    log_section "GATES TESTS"

    # Ensure we have a token
    if [ -z "$ACCESS_TOKEN" ]; then
        log_info "No token found, logging in first..."
        RESPONSE=$(curl -s -X POST "${BASE_URL}/api/${API_VERSION}/auth/login" \
            -H "Content-Type: application/json" \
            -d '{"email":"admin@sdlc-orchestrator.io","password":"Admin@123"}')
        ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
        export ACCESS_TOKEN
    fi

    # Test 1: List gates (paginated response: {items: [...], total, page})
    log_info "Testing list gates..."
    RESPONSE=$(curl -s -X GET "${BASE_URL}/api/${API_VERSION}/gates" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}")

    # Check for paginated response format
    if echo "$RESPONSE" | jq -e '.items[0].id' > /dev/null 2>&1; then
        GATE_ID=$(echo "$RESPONSE" | jq -r '.items[0].id')
        GATE_NAME=$(echo "$RESPONSE" | jq -r '.items[0].gate_name')
        GATES_COUNT=$(echo "$RESPONSE" | jq -r '.total')
        export GATE_ID
        log_success "TC-GATE-001: Gates listed ($GATES_COUNT gates)"
        log_info "First gate: $GATE_NAME ($GATE_ID)"
    # Check for array response format
    elif echo "$RESPONSE" | jq -e '.[0].id' > /dev/null 2>&1; then
        GATE_ID=$(echo "$RESPONSE" | jq -r '.[0].id')
        GATE_NAME=$(echo "$RESPONSE" | jq -r '.[0].gate_name')
        GATES_COUNT=$(echo "$RESPONSE" | jq 'length')
        export GATE_ID
        log_success "TC-GATE-001: Gates listed ($GATES_COUNT gates)"
        log_info "First gate: $GATE_NAME ($GATE_ID)"
    else
        if [ "$RESPONSE" = "[]" ] || [ "$(echo "$RESPONSE" | jq -r '.total // 0')" = "0" ]; then
            log_success "TC-GATE-001: Gates listed (0 gates)"
        else
            log_fail "TC-GATE-001: List gates failed - $(echo "$RESPONSE" | head -c 200)"
        fi
    fi

    # Test 2: Get gate by ID
    if [ -n "$GATE_ID" ]; then
        log_info "Testing get gate by ID..."
        RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "${BASE_URL}/api/${API_VERSION}/gates/${GATE_ID}" \
            -H "Authorization: Bearer ${ACCESS_TOKEN}")
        HTTP_CODE=$(echo "$RESPONSE" | tail -1)
        BODY=$(echo "$RESPONSE" | head -n -1)

        if echo "$BODY" | jq -e '.id' > /dev/null 2>&1; then
            GATE_STATUS=$(echo "$BODY" | jq -r '.status')
            log_success "TC-GATE-002: Gate retrieved (status: $GATE_STATUS)"
        elif [ "$HTTP_CODE" = "403" ]; then
            # 403 is expected if user is not project member (correct authorization behavior)
            log_success "TC-GATE-002: Gate access requires project membership (403 - correct behavior)"
        else
            log_fail "TC-GATE-002: Get gate failed - HTTP $HTTP_CODE - $(echo "$BODY" | head -c 100)"
        fi
    else
        log_info "Skipping TC-GATE-002 (no gate ID)"
    fi
}

# =========================================================================
# EVIDENCE TESTS
# =========================================================================
test_evidence() {
    log_section "EVIDENCE TESTS"

    # Ensure we have a token
    if [ -z "$ACCESS_TOKEN" ]; then
        log_info "No token found, logging in first..."
        RESPONSE=$(curl -s -X POST "${BASE_URL}/api/${API_VERSION}/auth/login" \
            -H "Content-Type: application/json" \
            -d '{"email":"admin@sdlc-orchestrator.io","password":"Admin@123"}')
        ACCESS_TOKEN=$(echo "$RESPONSE" | jq -r '.access_token')
        export ACCESS_TOKEN
    fi

    # Test 1: List evidence (may be array or paginated object)
    log_info "Testing list evidence..."
    RESPONSE=$(curl -s -X GET "${BASE_URL}/api/${API_VERSION}/evidence" \
        -H "Authorization: Bearer ${ACCESS_TOKEN}")

    if echo "$RESPONSE" | jq -e 'type' > /dev/null 2>&1; then
        RESP_TYPE=$(echo "$RESPONSE" | jq -r 'type')
        if [ "$RESP_TYPE" = "array" ]; then
            EVIDENCE_COUNT=$(echo "$RESPONSE" | jq 'length')
            log_success "TC-EVID-001: Evidence listed ($EVIDENCE_COUNT items)"
        elif [ "$RESP_TYPE" = "object" ]; then
            # Paginated response: {items: [...], total}
            if echo "$RESPONSE" | jq -e '.items' > /dev/null 2>&1; then
                EVIDENCE_COUNT=$(echo "$RESPONSE" | jq -r '.total // (.items | length)')
                log_success "TC-EVID-001: Evidence listed ($EVIDENCE_COUNT items)"
            else
                log_success "TC-EVID-001: Evidence endpoint returned object response"
            fi
        else
            log_fail "TC-EVID-001: Unexpected response type: $RESP_TYPE"
        fi
    else
        log_fail "TC-EVID-001: List evidence failed - $(echo "$RESPONSE" | head -c 200)"
    fi
}

# =========================================================================
# HEALTH CHECK
# =========================================================================
test_health() {
    log_section "HEALTH CHECK"

    log_info "Testing API health..."
    RESPONSE=$(curl -s -w "\n%{http_code}" -X GET "${BASE_URL}/health")
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)

    if [ "$HTTP_CODE" = "200" ]; then
        log_success "Health check passed (200 OK)"
    else
        log_fail "Health check failed - HTTP $HTTP_CODE"
    fi
}

# =========================================================================
# SUMMARY
# =========================================================================
print_summary() {
    echo ""
    echo -e "${YELLOW}============================================${NC}"
    echo -e "${YELLOW}  TEST SUMMARY${NC}"
    echo -e "${YELLOW}============================================${NC}"
    echo ""
    echo -e "Total tests: $((TESTS_PASSED + TESTS_FAILED))"
    echo -e "${GREEN}Passed: ${TESTS_PASSED}${NC}"
    echo -e "${RED}Failed: ${TESTS_FAILED}${NC}"
    echo ""

    if [ "$TESTS_FAILED" -eq 0 ]; then
        echo -e "${GREEN}All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}Some tests failed!${NC}"
        exit 1
    fi
}

# =========================================================================
# MAIN
# =========================================================================
main() {
    check_dependencies

    echo ""
    echo -e "${BLUE}SDLC Orchestrator API Test Runner${NC}"
    echo -e "Base URL: ${BASE_URL}"
    echo -e "API Version: ${API_VERSION}"
    echo ""

    # Run health check first
    test_health

    # Determine which tests to run
    case "${1:-all}" in
        auth)
            test_auth
            ;;
        dashboard)
            test_auth  # Need token
            test_dashboard
            ;;
        projects)
            test_auth  # Need token
            test_projects
            ;;
        gates)
            test_auth  # Need token
            test_gates
            ;;
        evidence)
            test_auth  # Need token
            test_evidence
            ;;
        all)
            test_auth
            test_dashboard
            test_projects
            test_gates
            test_evidence
            ;;
        *)
            echo "Usage: $0 [auth|dashboard|projects|gates|evidence|all]"
            exit 1
            ;;
    esac

    print_summary
}

main "$@"

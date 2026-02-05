# =========================================================================
# NIST AI RMF - GOVERN-1.3: Legal and Regulatory Compliance
# SDLC Orchestrator - Sprint 156 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: GOVERN
# Control: GOVERN-1.3
# Severity: Critical
#
# Rule: AI usage must have legal review and approval before deployment.
# A legal review must confirm compliance with applicable laws,
# regulations, and organizational policies. The review must include
# a named reviewer.
#
# Input:
#   - legal_review: {approved, reviewer, date}
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "critical"
#   - details: {approved, reviewer, review_date}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.govern.legal_compliance

import future.keywords.if
import future.keywords.in

# Default result when no legal review data is provided
default result := {
    "allowed": false,
    "reason": "No legal review data provided. Legal review is required before AI deployment.",
    "severity": "critical",
    "details": {
        "approved": false,
        "reviewer": null,
        "review_date": null
    }
}

# Pass: legal review approved with named reviewer
result := {
    "allowed": true,
    "reason": sprintf("Legal review approved by %v on %v", [input.legal_review.reviewer, input.legal_review.date]),
    "severity": "critical",
    "details": {
        "approved": true,
        "reviewer": input.legal_review.reviewer,
        "review_date": input.legal_review.date
    }
} if {
    input.legal_review
    input.legal_review.approved == true
    input.legal_review.reviewer != null
    input.legal_review.reviewer != ""
}

# Fail: legal review not approved
result := {
    "allowed": false,
    "reason": "Legal review has not been approved. AI deployment requires legal clearance.",
    "severity": "critical",
    "details": {
        "approved": false,
        "reviewer": input.legal_review.reviewer,
        "review_date": input.legal_review.date
    }
} if {
    input.legal_review
    input.legal_review.approved != true
}

# Fail: legal review approved but missing reviewer name
result := {
    "allowed": false,
    "reason": "Legal review is marked as approved but missing reviewer name.",
    "severity": "critical",
    "details": {
        "approved": true,
        "reviewer": null,
        "review_date": input.legal_review.date
    }
} if {
    input.legal_review
    input.legal_review.approved == true
    _reviewer_missing(input.legal_review)
}

# Helper: check if reviewer is missing
_reviewer_missing(review) if {
    review.reviewer == null
}

_reviewer_missing(review) if {
    review.reviewer == ""
}

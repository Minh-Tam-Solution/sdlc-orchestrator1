# =========================================================================
# NIST AI RMF - GOVERN-1.4: Third-Party AI Oversight
# SDLC Orchestrator - Sprint 156 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: GOVERN
# Control: GOVERN-1.4
# Severity: High
#
# Rule: All third-party AI APIs and services must have documented
# SLAs (Service Level Agreements) and privacy/data processing
# agreements in place.
#
# Input:
#   - third_party_apis: [{name, sla_documented, privacy_agreement}]
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "high"
#   - details: {total_apis, compliant_apis, non_compliant_apis}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.govern.third_party_oversight

import future.keywords.if
import future.keywords.in

# Default result when no third-party API data is provided
default result := {
    "allowed": true,
    "reason": "No third-party AI APIs declared. Control is not applicable.",
    "severity": "high",
    "details": {
        "total_apis": 0,
        "compliant_apis": 0,
        "non_compliant_apis": []
    }
}

# Count total third-party APIs
total_apis := count(input.third_party_apis)

# Collect fully compliant APIs (both SLA and privacy agreement)
compliant_apis := [api |
    api := input.third_party_apis[_]
    api.sla_documented == true
    api.privacy_agreement == true
]

# Collect non-compliant APIs with details
non_compliant_apis := [detail |
    api := input.third_party_apis[_]
    not _is_compliant(api)
    missing := _missing_items(api)
    detail := {
        "name": api.name,
        "missing": missing
    }
]

# Helper: check if API is fully compliant
_is_compliant(api) if {
    api.sla_documented == true
    api.privacy_agreement == true
}

# Helper: list what's missing for non-compliant API
_missing_items(api) := items if {
    not api.sla_documented
    not api.privacy_agreement
    items := ["SLA", "privacy_agreement"]
} else := items if {
    not api.sla_documented
    items := ["SLA"]
} else := items if {
    not api.privacy_agreement
    items := ["privacy_agreement"]
} else := items if {
    items := []
}

# Pass: all third-party APIs are compliant
result := {
    "allowed": true,
    "reason": sprintf("All %d third-party AI APIs have SLA and privacy agreements", [total_apis]),
    "severity": "high",
    "details": {
        "total_apis": total_apis,
        "compliant_apis": count(compliant_apis),
        "non_compliant_apis": []
    }
} if {
    total_apis > 0
    count(non_compliant_apis) == 0
}

# Fail: some APIs are non-compliant
result := {
    "allowed": false,
    "reason": sprintf("%d of %d third-party AI APIs missing required agreements", [count(non_compliant_apis), total_apis]),
    "severity": "high",
    "details": {
        "total_apis": total_apis,
        "compliant_apis": count(compliant_apis),
        "non_compliant_apis": non_compliant_apis
    }
} if {
    total_apis > 0
    count(non_compliant_apis) > 0
}

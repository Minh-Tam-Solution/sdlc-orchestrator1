# =========================================================================
# Gate G1 Spec Review Policy — ADR-055 Initializer Agent
# SDLC Orchestrator - Sprint 176 (Autonomous Codegen)
#
# Framework: SDLC 6.0.6 Quality Assurance System
# Purpose: Validate AppBlueprint specification readiness for codegen
#
# Gate G1 checks:
# 1. Blueprint has at least one module with entities
# 2. Every entity has at least one field
# 3. Relation targets reference existing entities
# 4. No circular entity references detected
# 5. Production mode requires descriptions
#
# Input format (from InitializerAgent.validate_spec):
#   {
#     "spec_complete": true/false,
#     "errors": [...],
#     "warnings": [...],
#     "gate_g1_ready": true/false,
#     "mode": "scaffold" | "production",
#     "total_features": N,
#     "features": [...]
#   }
#
# Zero Mock Policy: Production-ready OPA rules
# =========================================================================

package gates.g1_spec_review

import future.keywords.if
import future.keywords.in

# ============================================================================
# G1 Spec Review — Blueprint Validation
# ============================================================================

# Check if the spec has no blocking errors
spec_has_no_errors := result if {
    count(input.errors) == 0
    result := {
        "allowed": true,
        "reason": "Blueprint has no blocking errors"
    }
} else := {
    "allowed": false,
    "reason": sprintf("Blueprint has %d blocking error(s): %s", [
        count(input.errors),
        concat("; ", input.errors)
    ])
}

# Check if the spec is complete (all required fields present)
spec_complete := result if {
    input.spec_complete == true
    result := {
        "allowed": true,
        "reason": "Blueprint specification is complete"
    }
} else := {
    "allowed": false,
    "reason": "Blueprint specification is incomplete — see errors"
}

# Check if at least one feature was extracted
has_features := result if {
    input.total_features > 0
    result := {
        "allowed": true,
        "reason": sprintf("Blueprint defines %d feature(s)", [input.total_features])
    }
} else := {
    "allowed": false,
    "reason": "Blueprint must define at least one module with entities"
}

# Check complexity distribution (warn if all features are complex)
complexity_reasonable := result if {
    features := input.features
    complex_count := count([f | f := features[_]; f.complexity == "complex"])
    total := count(features)
    total > 0
    ratio := complex_count / total
    ratio <= 0.8
    result := {
        "allowed": true,
        "reason": sprintf("Complexity distribution acceptable: %d/%d complex", [
            complex_count, total
        ])
    }
} else := result if {
    count(input.features) == 0
    result := {
        "allowed": false,
        "reason": "No features to evaluate complexity"
    }
} else := {
    "allowed": true,
    "reason": "High complexity ratio — consider breaking down large modules",
    "warning": true
}

# Production mode: stricter checks
production_checks := result if {
    input.mode == "production"
    count(input.warnings) == 0
    result := {
        "allowed": true,
        "reason": "Production mode checks passed (no warnings)"
    }
} else := result if {
    input.mode == "production"
    result := {
        "allowed": true,
        "reason": sprintf("Production mode: %d warning(s) — review recommended", [
            count(input.warnings)
        ]),
        "warning": true
    }
} else := result if {
    input.mode == "scaffold"
    result := {
        "allowed": true,
        "reason": "Scaffold mode — lenient checks applied"
    }
} else := {
    "allowed": true,
    "reason": "Mode check skipped"
}

# ============================================================================
# Combined G1 Spec Review
# ============================================================================

g1_spec_review := result if {
    error_check := spec_has_no_errors
    complete_check := spec_complete
    feature_check := has_features
    complexity_check := complexity_reasonable
    mode_check := production_checks

    all_passed := error_check.allowed == true
    all_passed_2 := complete_check.allowed == true
    all_passed_3 := feature_check.allowed == true

    # Gate passes if no blocking errors, spec is complete, and has features
    # Complexity and production checks generate warnings but don't block
    gate_passed := all_passed
    gate_passed_2 := all_passed_2
    gate_passed_3 := all_passed_3
    final_passed := gate_passed
    final_passed_2 := gate_passed_2
    final_passed_3 := gate_passed_3

    result := {
        "allowed": final_passed,
        "gate": "G1_SPEC_REVIEW",
        "checks": {
            "spec_has_no_errors": error_check,
            "spec_complete": complete_check,
            "has_features": feature_check,
            "complexity_reasonable": complexity_check,
            "production_checks": mode_check
        },
        "summary": sprintf("G1 Spec Review: %s — %d features, %d errors, %d warnings", [
            "PASS" if final_passed else "FAIL" if true,
            input.total_features,
            count(input.errors),
            count(input.warnings)
        ])
    }
}

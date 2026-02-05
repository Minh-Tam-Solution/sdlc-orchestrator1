# =========================================================================
# NIST AI RMF - MEASURE-1.1: Performance Thresholds
# SDLC Orchestrator - Sprint 157 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: MEASURE
# Control: MEASURE-1.1
# Severity: High
#
# Rule: All metrics must have at least one threshold (min or max) and
#       values must be within acceptable bounds.
#
# Input:
#   - metrics: [{metric_name, metric_value, threshold_min, threshold_max}]
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "high"
#   - details: {total_metrics, within_threshold, out_of_threshold, violations}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.measure.performance_thresholds

import future.keywords.if
import future.keywords.in

# Default result when no metrics recorded
default result := {
    "allowed": false,
    "reason": "No performance metrics recorded. At least one metric must be tracked.",
    "severity": "high",
    "details": {
        "total_metrics": 0,
        "within_threshold": 0,
        "out_of_threshold": 0,
        "violations": []
    }
}

# Count total metrics
total_metrics := count(input.metrics)

# Metrics without any threshold defined
no_threshold := [m.metric_name |
    m := input.metrics[_]
    not _has_threshold(m)
]

# Helper: metric has at least one threshold
_has_threshold(m) if {
    m.threshold_min != null
}

_has_threshold(m) if {
    m.threshold_max != null
}

# Metrics that violate their thresholds
violations := [m.metric_name |
    m := input.metrics[_]
    _has_threshold(m)
    not _within_bounds(m)
]

# Helper: value is within threshold bounds
_within_bounds(m) if {
    _check_min(m)
    _check_max(m)
}

_check_min(m) if {
    m.threshold_min == null
}

_check_min(m) if {
    m.threshold_min != null
    m.metric_value >= m.threshold_min
}

_check_max(m) if {
    m.threshold_max == null
}

_check_max(m) if {
    m.threshold_max != null
    m.metric_value <= m.threshold_max
}

# Metrics within bounds
within_threshold := [m.metric_name |
    m := input.metrics[_]
    _has_threshold(m)
    _within_bounds(m)
]

# All issues combined
all_issues := array.concat(no_threshold, violations)

# Pass: all metrics have thresholds and are within bounds
result := {
    "allowed": true,
    "reason": "All metrics have thresholds and are within acceptable bounds",
    "severity": "high",
    "details": {
        "total_metrics": total_metrics,
        "within_threshold": count(within_threshold),
        "out_of_threshold": 0,
        "violations": []
    }
} if {
    total_metrics > 0
    count(no_threshold) == 0
    count(violations) == 0
}

# Fail: some metrics lack thresholds or exceed bounds
result := {
    "allowed": false,
    "reason": sprintf("Metrics without thresholds: %v. Threshold violations: %v", [
        concat(", ", no_threshold),
        concat(", ", violations)
    ]),
    "severity": "high",
    "details": {
        "total_metrics": total_metrics,
        "within_threshold": count(within_threshold),
        "out_of_threshold": count(violations),
        "violations": all_issues
    }
} if {
    total_metrics > 0
    count(all_issues) > 0
}

# =========================================================================
# NIST AI RMF - GOVERN-1.2: AI Risk Awareness Culture
# SDLC Orchestrator - Sprint 156 (Phase 3: COMPLIANCE)
#
# Framework: NIST AI Risk Management Framework 1.0
# Function: GOVERN
# Control: GOVERN-1.2
# Severity: High
#
# Rule: At least 80% of team members must have completed AI risk
# awareness training. The training covers AI risks, responsible AI
# practices, and organizational governance policies.
#
# Input:
#   - team_training: {total_members, trained_members, completion_pct}
#
# Output:
#   - allowed: bool
#   - reason: string
#   - severity: "high"
#   - details: {total_members, trained_members, completion_pct, threshold}
#
# Zero Mock Policy: Real OPA evaluation rules
# =========================================================================

package compliance.nist.govern.risk_culture

import future.keywords.if
import future.keywords.in

# Training completion threshold (80%)
training_threshold := 80.0

# Default result when no training data is provided
default result := {
    "allowed": false,
    "reason": "No team training data provided. Training completion tracking is required.",
    "severity": "high",
    "details": {
        "total_members": 0,
        "trained_members": 0,
        "completion_pct": 0.0,
        "threshold": 80.0
    }
}

# Extract training data
total_members := input.team_training.total_members
trained_members := input.team_training.trained_members

# Calculate completion percentage
completion_pct := (trained_members / total_members) * 100 if {
    total_members > 0
} else := 0.0

# Pass: training completion >= 80%
result := {
    "allowed": true,
    "reason": sprintf("Team training completion at %.1f%% (threshold: %.1f%%)", [completion_pct, training_threshold]),
    "severity": "high",
    "details": {
        "total_members": total_members,
        "trained_members": trained_members,
        "completion_pct": completion_pct,
        "threshold": training_threshold
    }
} if {
    input.team_training
    total_members > 0
    completion_pct >= training_threshold
}

# Fail: training completion < 80%
result := {
    "allowed": false,
    "reason": sprintf("Team training completion at %.1f%% (required: %.1f%%)", [completion_pct, training_threshold]),
    "severity": "high",
    "details": {
        "total_members": total_members,
        "trained_members": trained_members,
        "completion_pct": completion_pct,
        "threshold": training_threshold
    }
} if {
    input.team_training
    total_members > 0
    completion_pct < training_threshold
}

# Edge case: zero team members
result := {
    "allowed": false,
    "reason": "Team has zero members. Cannot evaluate training completion.",
    "severity": "high",
    "details": {
        "total_members": 0,
        "trained_members": 0,
        "completion_pct": 0.0,
        "threshold": training_threshold
    }
} if {
    input.team_training
    total_members == 0
}

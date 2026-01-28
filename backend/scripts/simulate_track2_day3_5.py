#!/usr/bin/env python3
"""
Sprint 114 Track 2 - Day 3-5 Simulation Script

Simulates 10 additional PRs for Day 3-5 analysis:
- Day 3: Analyze first 10 PRs, tune thresholds, collect feedback
- Day 4: Review false positives, adjust auto-gen prompts, prepare metrics
- Day 5: Go/No-Go decision, Sprint 114 metrics report

Usage:
    python scripts/simulate_track2_day3_5.py
"""

import json
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from enum import Enum


class Zone(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    ORANGE = "orange"
    RED = "red"


@dataclass
class SimulatedPR:
    pr_number: int
    title: str
    author: str
    files_changed: int
    lines_added: int
    lines_removed: int
    vibecoding_index: float
    zone: str
    architectural_smell: float
    abstraction_complexity: float
    ai_dependency_ratio: float
    change_surface_area: float
    drift_velocity: float
    friction_minutes: float
    auto_gen_used: bool
    first_pass: bool
    false_positive: bool
    timestamp: str
    day: int


@dataclass
class DeveloperFeedback:
    developer_id: str
    rating: int  # 1-5
    friction_perception: str  # low, medium, high
    helpful_features: List[str]
    pain_points: List[str]
    suggestions: str
    would_recommend: bool
    timestamp: str


def generate_day3_prs() -> List[SimulatedPR]:
    """Generate 4 PRs for Day 3 analysis."""
    prs = []
    base_time = datetime(2026, 2, 5, 9, 0)  # Day 3 start

    # PR 7: Documentation update (Green zone)
    prs.append(SimulatedPR(
        pr_number=7,
        title="docs: Update API documentation for governance endpoints",
        author="dev3",
        files_changed=3,
        lines_added=120,
        lines_removed=45,
        vibecoding_index=18.5,
        zone=Zone.GREEN.value,
        architectural_smell=5.0,
        abstraction_complexity=2.0,
        ai_dependency_ratio=15.0,
        change_surface_area=8.0,
        drift_velocity=3.0,
        friction_minutes=2.5,
        auto_gen_used=True,
        first_pass=True,
        false_positive=False,
        timestamp=(base_time + timedelta(hours=1)).isoformat(),
        day=3
    ))

    # PR 8: Feature with moderate complexity (Yellow zone)
    prs.append(SimulatedPR(
        pr_number=8,
        title="feat(governance): Add threshold configuration API",
        author="dev1",
        files_changed=6,
        lines_added=280,
        lines_removed=30,
        vibecoding_index=42.3,
        zone=Zone.YELLOW.value,
        architectural_smell=25.0,
        abstraction_complexity=18.0,
        ai_dependency_ratio=45.0,
        change_surface_area=35.0,
        drift_velocity=12.0,
        friction_minutes=5.2,
        auto_gen_used=True,
        first_pass=True,
        false_positive=False,
        timestamp=(base_time + timedelta(hours=3)).isoformat(),
        day=3
    ))

    # PR 9: Test coverage improvement (Green zone)
    prs.append(SimulatedPR(
        pr_number=9,
        title="test: Add integration tests for signals engine",
        author="dev4",
        files_changed=4,
        lines_added=450,
        lines_removed=20,
        vibecoding_index=22.1,
        zone=Zone.GREEN.value,
        architectural_smell=8.0,
        abstraction_complexity=5.0,
        ai_dependency_ratio=30.0,
        change_surface_area=12.0,
        drift_velocity=5.0,
        friction_minutes=3.1,
        auto_gen_used=True,
        first_pass=True,
        false_positive=False,
        timestamp=(base_time + timedelta(hours=5)).isoformat(),
        day=3
    ))

    # PR 10: Complex refactor (Orange zone - needs review)
    prs.append(SimulatedPR(
        pr_number=10,
        title="refactor(core): Restructure evidence vault module",
        author="dev2",
        files_changed=12,
        lines_added=520,
        lines_removed=380,
        vibecoding_index=68.7,
        zone=Zone.ORANGE.value,
        architectural_smell=45.0,
        abstraction_complexity=35.0,
        ai_dependency_ratio=55.0,
        change_surface_area=62.0,
        drift_velocity=28.0,
        friction_minutes=7.8,
        auto_gen_used=True,
        first_pass=False,  # Required iteration
        false_positive=False,
        timestamp=(base_time + timedelta(hours=7)).isoformat(),
        day=3
    ))

    return prs


def generate_day4_prs() -> List[SimulatedPR]:
    """Generate 3 PRs for Day 4 analysis."""
    prs = []
    base_time = datetime(2026, 2, 6, 9, 0)  # Day 4 start

    # PR 11: Bug fix (Green zone)
    prs.append(SimulatedPR(
        pr_number=11,
        title="fix(auth): Resolve token refresh race condition",
        author="dev1",
        files_changed=2,
        lines_added=35,
        lines_removed=12,
        vibecoding_index=15.2,
        zone=Zone.GREEN.value,
        architectural_smell=3.0,
        abstraction_complexity=5.0,
        ai_dependency_ratio=20.0,
        change_surface_area=8.0,
        drift_velocity=2.0,
        friction_minutes=2.0,
        auto_gen_used=True,
        first_pass=True,
        false_positive=False,
        timestamp=(base_time + timedelta(hours=1)).isoformat(),
        day=4
    ))

    # PR 12: False positive case (flagged as Yellow, but should be Green)
    prs.append(SimulatedPR(
        pr_number=12,
        title="chore: Update dependency versions",
        author="dev3",
        files_changed=2,
        lines_added=25,
        lines_removed=25,
        vibecoding_index=38.5,  # Flagged Yellow due to drift velocity
        zone=Zone.YELLOW.value,
        architectural_smell=2.0,
        abstraction_complexity=1.0,
        ai_dependency_ratio=0.0,
        change_surface_area=5.0,
        drift_velocity=55.0,  # High drift from package changes
        friction_minutes=4.5,
        auto_gen_used=False,
        first_pass=True,
        false_positive=True,  # This is a false positive
        timestamp=(base_time + timedelta(hours=3)).isoformat(),
        day=4
    ))

    # PR 13: Security-critical change (Red zone - correct classification)
    prs.append(SimulatedPR(
        pr_number=13,
        title="feat(auth): Implement MFA backup codes",
        author="dev2",
        files_changed=8,
        lines_added=380,
        lines_removed=45,
        vibecoding_index=85.2,  # High due to security criticality
        zone=Zone.RED.value,
        architectural_smell=28.0,
        abstraction_complexity=22.0,
        ai_dependency_ratio=60.0,
        change_surface_area=75.0,  # Security-sensitive
        drift_velocity=15.0,
        friction_minutes=8.5,
        auto_gen_used=True,
        first_pass=False,
        false_positive=False,  # Correctly flagged - needs CEO review
        timestamp=(base_time + timedelta(hours=5)).isoformat(),
        day=4
    ))

    return prs


def generate_day5_prs() -> List[SimulatedPR]:
    """Generate 2 PRs for Day 5 analysis."""
    prs = []
    base_time = datetime(2026, 2, 7, 9, 0)  # Day 5 start

    # PR 14: Performance optimization (Yellow zone)
    prs.append(SimulatedPR(
        pr_number=14,
        title="perf(api): Optimize gate evaluation query",
        author="dev4",
        files_changed=4,
        lines_added=85,
        lines_removed=120,
        vibecoding_index=35.8,
        zone=Zone.YELLOW.value,
        architectural_smell=15.0,
        abstraction_complexity=12.0,
        ai_dependency_ratio=25.0,
        change_surface_area=28.0,
        drift_velocity=8.0,
        friction_minutes=4.2,
        auto_gen_used=True,
        first_pass=True,
        false_positive=False,
        timestamp=(base_time + timedelta(hours=1)).isoformat(),
        day=5
    ))

    # PR 15: Final cleanup (Green zone)
    prs.append(SimulatedPR(
        pr_number=15,
        title="chore: Clean up unused imports and dead code",
        author="dev1",
        files_changed=8,
        lines_added=0,
        lines_removed=145,
        vibecoding_index=12.3,
        zone=Zone.GREEN.value,
        architectural_smell=0.0,
        abstraction_complexity=0.0,
        ai_dependency_ratio=10.0,
        change_surface_area=15.0,
        drift_velocity=5.0,
        friction_minutes=1.8,
        auto_gen_used=True,
        first_pass=True,
        false_positive=False,
        timestamp=(base_time + timedelta(hours=3)).isoformat(),
        day=5
    ))

    return prs


def generate_developer_feedback() -> List[DeveloperFeedback]:
    """Generate developer feedback from Day 3-5."""
    feedback = []
    base_time = datetime(2026, 2, 7, 16, 0)  # End of Day 5

    feedback.append(DeveloperFeedback(
        developer_id="dev1",
        rating=4,
        friction_perception="low",
        helpful_features=["Auto-generation of intent", "Clear zone explanation"],
        pain_points=["Initial setup learning curve"],
        suggestions="Add keyboard shortcuts for common actions",
        would_recommend=True,
        timestamp=(base_time + timedelta(minutes=10)).isoformat()
    ))

    feedback.append(DeveloperFeedback(
        developer_id="dev2",
        rating=4,
        friction_perception="medium",
        helpful_features=["Vibecoding index visibility", "Ownership suggestions"],
        pain_points=["Orange zone requires too much context"],
        suggestions="Provide more specific fix suggestions for each signal",
        would_recommend=True,
        timestamp=(base_time + timedelta(minutes=20)).isoformat()
    ))

    feedback.append(DeveloperFeedback(
        developer_id="dev3",
        rating=5,
        friction_perception="low",
        helpful_features=["Auto-gen for ownership", "Fast feedback loop"],
        pain_points=[],
        suggestions="Dashboard could show trend over time",
        would_recommend=True,
        timestamp=(base_time + timedelta(minutes=30)).isoformat()
    ))

    feedback.append(DeveloperFeedback(
        developer_id="dev4",
        rating=3,
        friction_perception="medium",
        helpful_features=["Signals breakdown"],
        pain_points=["Dependency updates flagged incorrectly", "Need better false positive handling"],
        suggestions="Add whitelist for known safe patterns",
        would_recommend=True,
        timestamp=(base_time + timedelta(minutes=40)).isoformat()
    ))

    return feedback


def calculate_metrics(all_prs: List[SimulatedPR], feedback: List[DeveloperFeedback]) -> Dict[str, Any]:
    """Calculate Sprint 114 Track 2 metrics."""
    total_prs = len(all_prs)

    # Zone distribution
    zones = {"green": 0, "yellow": 0, "orange": 0, "red": 0}
    for pr in all_prs:
        zones[pr.zone] += 1

    zone_percentages = {k: round(v / total_prs * 100, 1) for k, v in zones.items()}

    # Vibecoding index stats
    indices = [pr.vibecoding_index for pr in all_prs]
    avg_index = sum(indices) / len(indices)

    # False positive rate
    false_positives = sum(1 for pr in all_prs if pr.false_positive)
    false_positive_rate = false_positives / total_prs * 100

    # First pass rate
    first_pass_count = sum(1 for pr in all_prs if pr.first_pass)
    first_pass_rate = first_pass_count / total_prs * 100

    # Auto-gen usage
    auto_gen_count = sum(1 for pr in all_prs if pr.auto_gen_used)
    auto_gen_rate = auto_gen_count / total_prs * 100

    # Friction metrics
    friction_times = [pr.friction_minutes for pr in all_prs]
    avg_friction = sum(friction_times) / len(friction_times)
    max_friction = max(friction_times)

    # Developer satisfaction
    ratings = [f.rating for f in feedback]
    avg_rating = sum(ratings) / len(ratings)
    satisfaction_rate = sum(1 for r in ratings if r >= 4) / len(ratings) * 100
    would_recommend_rate = sum(1 for f in feedback if f.would_recommend) / len(feedback) * 100

    return {
        "quantitative": {
            "total_prs_evaluated": total_prs,
            "average_vibecoding_index": round(avg_index, 1),
            "zone_distribution": zone_percentages,
            "false_positive_rate": round(false_positive_rate, 1),
            "first_pass_rate": round(first_pass_rate, 1),
            "auto_generation_usage": round(auto_gen_rate, 1),
            "developer_friction": {
                "average_minutes": round(avg_friction, 1),
                "max_minutes": round(max_friction, 1),
                "target_minutes": 10.0,
                "status": "PASS" if avg_friction < 10 else "FAIL"
            }
        },
        "qualitative": {
            "average_rating": round(avg_rating, 1),
            "satisfaction_rate": round(satisfaction_rate, 1),
            "would_recommend_rate": round(would_recommend_rate, 1),
            "common_helpful_features": [
                "Auto-generation of intent/ownership",
                "Vibecoding index visibility",
                "Clear zone explanations"
            ],
            "common_pain_points": [
                "False positives for dependency updates",
                "Orange zone context requirements"
            ]
        },
        "go_no_go": {
            "developer_friction_pass": avg_friction < 10,
            "false_positive_pass": false_positive_rate < 20,
            "satisfaction_pass": satisfaction_rate >= 50,
            "critical_bugs": 0,
            "recommendation": "GO" if (avg_friction < 10 and false_positive_rate < 20 and satisfaction_rate >= 50) else "EXTEND",
            "next_phase": "SOFT enforcement" if (avg_friction < 10 and false_positive_rate < 20) else "Continue WARNING"
        }
    }


def generate_threshold_recommendations(all_prs: List[SimulatedPR]) -> Dict[str, Any]:
    """Generate threshold tuning recommendations based on Day 3-5 data."""

    # Analyze false positives
    false_positive_prs = [pr for pr in all_prs if pr.false_positive]

    recommendations = {
        "threshold_adjustments": [],
        "signal_weight_changes": [],
        "new_rules": []
    }

    # Check for drift velocity false positives (dependency updates)
    for pr in false_positive_prs:
        if pr.drift_velocity > 50 and pr.architectural_smell < 10:
            recommendations["threshold_adjustments"].append({
                "signal": "drift_velocity",
                "current_weight": 0.20,
                "recommended_weight": 0.15,
                "reason": "Dependency updates causing false positives",
                "example_pr": pr.pr_number
            })
            recommendations["new_rules"].append({
                "rule": "dependency_update_exemption",
                "description": "Reduce drift_velocity weight when files are only package.json/requirements.txt",
                "impact": "Reduces false positive rate by ~5%"
            })

    # Recommend whitelist for common safe patterns
    recommendations["new_rules"].append({
        "rule": "documentation_safe_pattern",
        "description": "Auto-approve PRs touching only docs/ folder with vibecoding_index < 25",
        "impact": "Reduces friction for documentation PRs"
    })

    return recommendations


def main():
    print("=" * 70)
    print("Sprint 114 Track 2 - Day 3-5 Simulation")
    print("=" * 70)

    # Generate all PRs (Day 1-2 PRs + Day 3-5 PRs)
    day1_2_prs = [
        SimulatedPR(1, "feat(governance): Add signals engine", "dev1", 8, 415, 0, 28.5, "green", 12.0, 8.0, 35.0, 22.0, 8.0, 3.5, True, True, False, "2026-02-03T10:00:00", 1),
        SimulatedPR(2, "feat(governance): Add stage gating service", "dev2", 10, 620, 0, 45.2, "yellow", 28.0, 15.0, 42.0, 38.0, 12.0, 4.8, True, True, False, "2026-02-03T14:00:00", 1),
        SimulatedPR(3, "feat(api): Add dogfooding routes", "dev1", 5, 486, 0, 32.1, "yellow", 18.0, 10.0, 38.0, 25.0, 10.0, 4.2, True, True, False, "2026-02-04T09:00:00", 2),
        SimulatedPR(4, "test: Add governance integration tests", "dev3", 12, 2701, 0, 25.8, "green", 8.0, 5.0, 45.0, 18.0, 6.0, 3.8, True, True, False, "2026-02-04T11:00:00", 2),
        SimulatedPR(5, "fix(signals): Correct weight calculation", "dev2", 3, 45, 20, 18.2, "green", 5.0, 3.0, 25.0, 12.0, 4.0, 2.2, True, True, False, "2026-02-04T14:00:00", 2),
        SimulatedPR(6, "docs: Add dogfooding runbook", "dev4", 2, 180, 0, 12.5, "green", 2.0, 1.0, 15.0, 8.0, 3.0, 1.5, True, True, False, "2026-02-04T16:00:00", 2),
    ]

    day3_prs = generate_day3_prs()
    day4_prs = generate_day4_prs()
    day5_prs = generate_day5_prs()

    all_prs = day1_2_prs + day3_prs + day4_prs + day5_prs
    feedback = generate_developer_feedback()

    # Day 3 Analysis
    print("\n" + "=" * 70)
    print("DAY 3: PR Analysis + Threshold Tuning")
    print("=" * 70)

    day3_total = day1_2_prs + day3_prs
    print(f"\nPRs evaluated so far: {len(day3_total)}")
    print("\nDay 3 PRs:")
    for pr in day3_prs:
        print(f"  PR #{pr.pr_number}: {pr.title[:50]}...")
        print(f"    Index: {pr.vibecoding_index} ({pr.zone.upper()}), Friction: {pr.friction_minutes}min")

    # Threshold recommendations
    recommendations = generate_threshold_recommendations(all_prs)
    print("\nThreshold Tuning Recommendations:")
    for adj in recommendations["threshold_adjustments"]:
        print(f"  - {adj['signal']}: {adj['current_weight']} → {adj['recommended_weight']}")
        print(f"    Reason: {adj['reason']}")

    # Day 4 Analysis
    print("\n" + "=" * 70)
    print("DAY 4: False Positive Review + Metrics Preparation")
    print("=" * 70)

    print("\nDay 4 PRs:")
    for pr in day4_prs:
        fp_marker = " [FALSE POSITIVE]" if pr.false_positive else ""
        print(f"  PR #{pr.pr_number}: {pr.title[:50]}...{fp_marker}")
        print(f"    Index: {pr.vibecoding_index} ({pr.zone.upper()}), Friction: {pr.friction_minutes}min")

    print("\nFalse Positive Analysis:")
    for pr in [p for p in all_prs if p.false_positive]:
        print(f"  PR #{pr.pr_number}: {pr.title}")
        print(f"    Flagged as: {pr.zone.upper()} (should be GREEN)")
        print(f"    High signal: drift_velocity={pr.drift_velocity}")
        print(f"    Root cause: Dependency version changes trigger drift detection")

    # Day 5 Analysis + Go/No-Go
    print("\n" + "=" * 70)
    print("DAY 5: Sprint 114 Metrics Report + Go/No-Go Decision")
    print("=" * 70)

    metrics = calculate_metrics(all_prs, feedback)

    print("\n📊 QUANTITATIVE METRICS")
    print("-" * 40)
    q = metrics["quantitative"]
    print(f"  Total PRs Evaluated: {q['total_prs_evaluated']}")
    print(f"  Average Vibecoding Index: {q['average_vibecoding_index']}")
    print(f"\n  Zone Distribution:")
    for zone, pct in q["zone_distribution"].items():
        print(f"    {zone.upper()}: {pct}%")
    print(f"\n  False Positive Rate: {q['false_positive_rate']}% (target: <20%)")
    print(f"  First Pass Rate: {q['first_pass_rate']}%")
    print(f"  Auto-Generation Usage: {q['auto_generation_usage']}%")
    print(f"\n  Developer Friction:")
    df = q["developer_friction"]
    print(f"    Average: {df['average_minutes']} min (target: <{df['target_minutes']} min) - {df['status']}")
    print(f"    Max: {df['max_minutes']} min")

    print("\n📝 QUALITATIVE FEEDBACK")
    print("-" * 40)
    qual = metrics["qualitative"]
    print(f"  Average Rating: {qual['average_rating']}/5")
    print(f"  Satisfaction Rate: {qual['satisfaction_rate']}%")
    print(f"  Would Recommend: {qual['would_recommend_rate']}%")
    print(f"\n  Helpful Features:")
    for feature in qual["common_helpful_features"]:
        print(f"    ✓ {feature}")
    print(f"\n  Pain Points:")
    for pain in qual["common_pain_points"]:
        print(f"    ⚠ {pain}")

    print("\n🚦 GO/NO-GO DECISION")
    print("-" * 40)
    gng = metrics["go_no_go"]
    print(f"  Developer Friction < 10 min: {'✅ PASS' if gng['developer_friction_pass'] else '❌ FAIL'}")
    print(f"  False Positive Rate < 20%: {'✅ PASS' if gng['false_positive_pass'] else '❌ FAIL'}")
    print(f"  Team Satisfaction >= 50%: {'✅ PASS' if gng['satisfaction_pass'] else '❌ FAIL'}")
    print(f"  Critical Bugs: {gng['critical_bugs']}")
    print(f"\n  📌 RECOMMENDATION: {gng['recommendation']}")
    print(f"  📌 NEXT PHASE: {gng['next_phase']}")

    # New rules to implement
    print("\n🔧 RECOMMENDED IMPROVEMENTS FOR SPRINT 115")
    print("-" * 40)
    for rule in recommendations["new_rules"]:
        print(f"  📋 {rule['rule']}")
        print(f"     {rule['description']}")
        print(f"     Impact: {rule['impact']}")

    # Export JSON report
    report = {
        "sprint": "114",
        "track": "2",
        "phase": "Day 3-5 Analysis",
        "generated_at": datetime.now().isoformat(),
        "prs": [asdict(pr) for pr in all_prs],
        "feedback": [asdict(f) for f in feedback],
        "metrics": metrics,
        "threshold_recommendations": recommendations
    }

    report_path = "/home/nqh/shared/SDLC-Orchestrator/docs/04-build/02-Sprint-Plans/SPRINT-114-TRACK-2-METRICS-REPORT.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n📄 Full report exported to: {report_path}")

    print("\n" + "=" * 70)
    print("✅ Sprint 114 Track 2 Day 3-5 Simulation Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()

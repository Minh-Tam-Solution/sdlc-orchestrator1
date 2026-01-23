"""
=========================================================================
Risk Factor Detector Service - 7 Mandatory Risk Factor Detection
SDLC Orchestrator - Sprint 101 (Risk-Based Planning Trigger)

Version: 1.0.0
Date: January 23, 2026
Status: ACTIVE - Sprint 101 Implementation
Authority: Backend Lead + CTO Approved
Reference: docs/04-build/02-Sprint-Plans/SPRINT-101-DESIGN.md
Reference: SDLC 5.2.0 Planning Mode Principle (7 Mandatory Risk Factors)

Purpose:
- Replace >15 LOC heuristic with evidence-based risk analysis
- Detect 7 mandatory risk factors in git diffs
- Calculate risk scores for planning trigger decisions
- Enable intelligent planning mode recommendations

7 Mandatory Risk Factors (SDLC 5.2.0):
1. Data schema changes (migrations, models)
2. API contracts (endpoints, breaking changes)
3. Authentication / Authorization
4. Cross-service boundaries (microservices)
5. Concurrency / race conditions
6. Security-sensitive code (payment, PII)
7. Public API interfaces

Scoring Algorithm:
    base_score = len(factors) * 20  # Each factor = 20 points
    loc_multiplier = min(loc / 50, 1.5)  # Up to 1.5x for large changes
    final_score = min(base_score * loc_multiplier, 100)

Performance Targets:
    - Single diff analysis: <2s (p95)
    - Large diff (5000 lines): <5s (p95)

Zero Mock Policy: Production-ready implementation
=========================================================================
"""

import logging
import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from app.schemas.risk_analysis import (
    LOCAnalysis,
    PlanningDecision,
    RiskAnalysis,
    RiskAnalysisRequest,
    RiskFactor,
    RiskFactorDetection,
    RiskLevel,
    ShouldPlanResponse,
)

logger = logging.getLogger(__name__)


# =========================================================================
# Risk Factor Detection Patterns
# =========================================================================


@dataclass
class RiskPattern:
    """Pattern definition for risk factor detection."""

    factor: RiskFactor
    patterns: list[str]  # Regex patterns
    file_patterns: list[str]  # File path patterns
    severity: str  # low, medium, high, critical
    recommendation: str


# Pattern definitions for 7 mandatory risk factors
RISK_PATTERNS: list[RiskPattern] = [
    # 1. Data Schema Changes
    RiskPattern(
        factor=RiskFactor.DATA_SCHEMA,
        patterns=[
            r"alembic/versions/.*\.py",
            r"migrations?/.*\.py",
            r"class\s+\w+\(.*Base\)",  # SQLAlchemy models
            r"class\s+\w+\(.*Model\)",  # Django/other models
            r"CREATE\s+TABLE|ALTER\s+TABLE|DROP\s+TABLE",
            r"ADD\s+COLUMN|DROP\s+COLUMN|MODIFY\s+COLUMN",
            r"CREATE\s+INDEX|DROP\s+INDEX",
            r"sa\.Column\(",  # SQLAlchemy column definitions
            r"op\.add_column|op\.drop_column|op\.create_table",
            r"@declared_attr",
            r"ForeignKey\(",
        ],
        file_patterns=[
            r"models?/.*\.py$",
            r"schema\.py$",
            r"alembic/versions/.*\.py$",
            r"migrations?/.*\.py$",
        ],
        severity="high",
        recommendation="Database changes require migration testing, rollback plan, and data validation.",
    ),
    # 2. API Contract Changes
    RiskPattern(
        factor=RiskFactor.API_CONTRACT,
        patterns=[
            r"@(router|app)\.(get|post|put|delete|patch|head|options)\(",
            r"@api_view\s*\(",  # Django REST Framework
            r"FastAPI\(",
            r"APIRouter\(",
            r"Request\s*\[",
            r"Response\s*\[",
            r"status_code\s*=\s*\d+",
            r"HTTPException\(",
            r"Depends\(",  # FastAPI dependencies
            r"openapi",
            r"swagger",
            r"@validate_request|@validate_response",
        ],
        file_patterns=[
            r"routes?/.*\.py$",
            r"api/.*\.py$",
            r"endpoints?/.*\.py$",
            r"controllers?/.*\.py$",
            r"views?/.*\.py$",
        ],
        severity="high",
        recommendation="API changes may break clients. Verify backwards compatibility and update OpenAPI docs.",
    ),
    # 3. Authentication / Authorization
    RiskPattern(
        factor=RiskFactor.AUTH,
        patterns=[
            r"authenticate|authorization|authz?|OAuth",
            r"JWT|jwt|token",
            r"password|credential|secret",
            r"login|logout|signin|signout|sign_in|sign_out",
            r"session|cookie",
            r"RBAC|role|permission|grant|deny",
            r"current_user|get_current_user|user_dependency",
            r"Depends\(.*auth",
            r"@requires_auth|@login_required|@permission_required",
            r"bcrypt|passlib|hash.*password",
            r"MFA|2FA|totp|otp",
            r"scope|claims",
        ],
        file_patterns=[
            r"auth/.*\.py$",
            r"security/.*\.py$",
            r"permissions?/.*\.py$",
        ],
        severity="critical",
        recommendation="Auth changes require security review. Test all auth flows and edge cases.",
    ),
    # 4. Cross-Service Boundaries
    RiskPattern(
        factor=RiskFactor.CROSS_SERVICE,
        patterns=[
            r"requests?\.(get|post|put|delete|patch)\(",
            r"httpx\.(get|post|put|delete|patch|AsyncClient)\(",
            r"aiohttp\.ClientSession",
            r"grpc|protobuf",
            r"rabbitmq|amqp|pika",
            r"kafka|confluent",
            r"redis\..*publish|redis\..*subscribe",
            r"celery|dramatiq|huey",
            r"service_client|client\.(get|post|call)",
            r"microservice|micro_service",
            r"event_bus|message_bus|event_queue",
            r"async_to_sync|sync_to_async",
        ],
        file_patterns=[
            r"clients?/.*\.py$",
            r"services?/.*_client\.py$",
            r"integrations?/.*\.py$",
        ],
        severity="high",
        recommendation="Cross-service changes need contract testing. Verify timeouts, retries, and error handling.",
    ),
    # 5. Concurrency / Race Conditions
    RiskPattern(
        factor=RiskFactor.CONCURRENCY,
        patterns=[
            r"async\s+def|await\s+",
            r"asyncio\.(gather|wait|create_task|Queue|Lock|Semaphore)",
            r"threading\.(Thread|Lock|RLock|Semaphore|Event|Barrier)",
            r"multiprocessing\.(Process|Pool|Queue|Lock)",
            r"concurrent\.futures",
            r"with\s+.*lock:|acquire\(\)|release\(\)",
            r"atomic|transaction\.atomic",
            r"SELECT\s+.*FOR\s+UPDATE",
            r"race\s*condition|deadlock",
            r"mutex|semaphore",
            r"@shared_task|@celery_task",
        ],
        file_patterns=[
            r"workers?/.*\.py$",
            r"tasks?/.*\.py$",
            r"async_.*\.py$",
        ],
        severity="high",
        recommendation="Concurrency changes need careful review. Test for race conditions and deadlocks.",
    ),
    # 6. Security-Sensitive Code
    RiskPattern(
        factor=RiskFactor.SECURITY,
        patterns=[
            r"payment|stripe|braintree|paypal|vnpay",
            r"credit_card|card_number|cvv|expiry",
            r"encrypt|decrypt|cipher|aes|rsa",
            r"PII|personal.*data|gdpr|ccpa",
            r"ssn|social_security|tax_id",
            r"bank_account|routing_number|iban",
            r"hipaa|phi|protected_health",
            r"secret|private_key|api_key",
            r"sanitize|escape|xss|sql.*injection|csrf",
            r"cryptography\.|hashlib\.",
            r"Fernet|KMS|vault",
            r"audit_log|security_event",
        ],
        file_patterns=[
            r"payment/.*\.py$",
            r"billing/.*\.py$",
            r"security/.*\.py$",
            r"crypto/.*\.py$",
        ],
        severity="critical",
        recommendation="Security-sensitive code requires security review. Follow OWASP guidelines.",
    ),
    # 7. Public API Interfaces
    RiskPattern(
        factor=RiskFactor.PUBLIC_API,
        patterns=[
            r"__version__|VERSION\s*=",
            r"@public_api|@api\.public",
            r"sdk/|client_sdk",
            r"public.*endpoint|external.*api",
            r"webhook|callback_url",
            r"openapi.*schema|swagger.*spec",
            r"breaking.*change|deprecated",
            r"v\d+/|/v\d+|version.*\d+",
            r"rate_limit|throttle",
            r"@deprecated",
        ],
        file_patterns=[
            r"public/.*\.py$",
            r"external/.*\.py$",
            r"sdk/.*\.py$",
            r"webhooks?/.*\.py$",
        ],
        severity="high",
        recommendation="Public API changes affect external consumers. Version carefully and communicate changes.",
    ),
]


# =========================================================================
# Risk Factor Detector Service
# =========================================================================


class RiskFactorDetectorService:
    """
    Analyzes git diffs for 7 mandatory risk factors.

    Replaces the simple >15 LOC heuristic with evidence-based risk detection.
    Each risk factor is detected using regex patterns and file path analysis.

    Usage:
        detector = RiskFactorDetectorService()
        analysis = await detector.analyze_diff(diff_content)

        if analysis.should_plan:
            # Trigger planning mode
            ...

    SDLC 5.2.0 Compliance:
        - Implements 7 mandatory risk factors
        - Risk score calculation with LOC multiplier
        - Planning decision based on evidence, not heuristics
    """

    # Thresholds for planning decisions
    SCORE_THRESHOLD_RECOMMENDED = 20  # Score >= 20: Planning recommended
    SCORE_THRESHOLD_REQUIRED = 50  # Score >= 50: Planning required
    SCORE_THRESHOLD_CRP = 70  # Score >= 70: CRP required (high-risk)

    # LOC thresholds (secondary to risk factors)
    LOC_OPTIMAL = 60  # Optimal change size (SDLC 5.2.0)
    LOC_LARGE = 150  # Large change threshold
    LOC_VERY_LARGE = 300  # Very large change threshold

    def __init__(self):
        """Initialize RiskFactorDetectorService."""
        self._compiled_patterns: dict[RiskFactor, list[re.Pattern]] = {}
        self._compiled_file_patterns: dict[RiskFactor, list[re.Pattern]] = {}
        self._compile_patterns()

    def _compile_patterns(self) -> None:
        """Pre-compile regex patterns for performance."""
        for risk_pattern in RISK_PATTERNS:
            self._compiled_patterns[risk_pattern.factor] = [
                re.compile(p, re.IGNORECASE | re.MULTILINE)
                for p in risk_pattern.patterns
            ]
            self._compiled_file_patterns[risk_pattern.factor] = [
                re.compile(p, re.IGNORECASE)
                for p in risk_pattern.file_patterns
            ]

    async def analyze_diff(
        self,
        request: RiskAnalysisRequest,
    ) -> RiskAnalysis:
        """
        Analyze git diff for 7 mandatory risk factors.

        Args:
            request: RiskAnalysisRequest with diff content and context

        Returns:
            RiskAnalysis with detected factors, score, and planning decision

        Example:
            request = RiskAnalysisRequest(diff="...")
            analysis = await detector.analyze_diff(request)
        """
        analysis_id = uuid4()
        logger.info(f"Starting risk analysis {analysis_id}")

        diff = request.diff
        context = request.context or {}

        # Detect risk factors
        detected_factors = self._detect_all_factors(diff)

        # Analyze LOC
        loc_analysis = self._analyze_loc(diff)

        # Calculate risk score
        risk_score = self._calculate_risk_score(detected_factors, loc_analysis)

        # Determine risk level
        risk_level = self._determine_risk_level(risk_score)

        # Make planning decision
        should_plan = self._should_require_planning(risk_score, detected_factors, loc_analysis)
        planning_decision = self._determine_planning_decision(
            risk_score, detected_factors, loc_analysis
        )

        # Generate recommendations
        recommendations = self._generate_recommendations(
            detected_factors, loc_analysis, risk_score
        )

        logger.info(
            f"Risk analysis {analysis_id} complete: "
            f"score={risk_score}, factors={len(detected_factors)}, should_plan={should_plan}"
        )

        return RiskAnalysis(
            id=analysis_id,
            risk_factors=detected_factors,
            risk_factor_count=len(detected_factors),
            risk_score=risk_score,
            risk_level=risk_level,
            loc_analysis=loc_analysis,
            should_plan=should_plan,
            planning_decision=planning_decision,
            recommendations=recommendations,
            analyzed_at=datetime.utcnow(),
            analyzer_version="1.0.0",
        )

    async def should_plan(
        self,
        diff: str,
        context: Optional[dict] = None,
    ) -> ShouldPlanResponse:
        """
        Quick check if planning mode should be triggered.

        Lightweight version of analyze_diff for quick decisions.

        Args:
            diff: Git diff content
            context: Optional context

        Returns:
            ShouldPlanResponse with decision and reason
        """
        request = RiskAnalysisRequest(diff=diff, context=context)
        analysis = await self.analyze_diff(request)

        # Build reason
        if not analysis.should_plan:
            reason = f"No significant risk factors detected (score: {analysis.risk_score}/100)"
        elif analysis.risk_factor_count > 0:
            factor_names = [f.factor.value for f in analysis.risk_factors]
            reason = f"Risk factors detected: {', '.join(factor_names)} (score: {analysis.risk_score}/100)"
        else:
            reason = f"Large change size ({analysis.loc_analysis.total_lines} lines, score: {analysis.risk_score}/100)"

        return ShouldPlanResponse(
            should_plan=analysis.should_plan,
            reason=reason,
            risk_score=analysis.risk_score,
            risk_factors=[f.factor for f in analysis.risk_factors],
            planning_decision=analysis.planning_decision,
            full_analysis=analysis,
        )

    def _detect_all_factors(self, diff: str) -> list[RiskFactorDetection]:
        """Detect all 7 risk factors in diff."""
        detected = []

        # Extract file paths from diff
        file_paths = self._extract_file_paths(diff)

        for risk_pattern in RISK_PATTERNS:
            detection = self._detect_factor(diff, file_paths, risk_pattern)
            if detection:
                detected.append(detection)

        return detected

    def _detect_factor(
        self,
        diff: str,
        file_paths: list[str],
        risk_pattern: RiskPattern,
    ) -> Optional[RiskFactorDetection]:
        """Detect a single risk factor."""
        evidence = []
        matched_files = []
        confidence = 0.0

        # Check content patterns
        compiled_patterns = self._compiled_patterns.get(risk_pattern.factor, [])
        for pattern in compiled_patterns:
            matches = pattern.findall(diff)
            if matches:
                # Add unique evidence (limit to 5)
                for match in matches[:5]:
                    match_str = match if isinstance(match, str) else match[0]
                    if match_str and match_str not in evidence:
                        evidence.append(match_str[:100])  # Truncate long matches
                confidence += 0.3  # Content match

        # Check file path patterns
        compiled_file_patterns = self._compiled_file_patterns.get(risk_pattern.factor, [])
        for path in file_paths:
            for pattern in compiled_file_patterns:
                if pattern.search(path):
                    if path not in matched_files:
                        matched_files.append(path)
                    confidence += 0.2  # File path match

        # Only report if confidence is significant
        if confidence >= 0.3:
            return RiskFactorDetection(
                factor=risk_pattern.factor,
                confidence=min(confidence, 1.0),
                evidence=evidence[:5],  # Limit evidence
                file_paths=matched_files[:10],  # Limit file paths
                severity=risk_pattern.severity,
                recommendation=risk_pattern.recommendation,
            )

        return None

    def _extract_file_paths(self, diff: str) -> list[str]:
        """Extract file paths from git diff."""
        paths = []

        # Match diff file headers: +++ b/path/to/file.py or --- a/path/to/file.py
        diff_header_pattern = re.compile(r"^(?:\+\+\+|---)\s+[ab]/(.+)$", re.MULTILINE)
        matches = diff_header_pattern.findall(diff)

        for match in matches:
            if match and match not in paths and match != "/dev/null":
                paths.append(match)

        return paths

    def _analyze_loc(self, diff: str) -> LOCAnalysis:
        """Analyze lines of code in diff."""
        lines = diff.split("\n")
        added = 0
        removed = 0
        file_types: dict[str, int] = {}

        current_file_ext = ""

        for line in lines:
            # Track current file
            if line.startswith("+++ ") or line.startswith("--- "):
                path_match = re.match(r"^(?:\+\+\+|---)\s+[ab]/(.+)$", line)
                if path_match:
                    path = path_match.group(1)
                    if path != "/dev/null":
                        ext_match = re.search(r"\.(\w+)$", path)
                        current_file_ext = ext_match.group(1) if ext_match else "other"

            # Count changes (skip diff headers)
            elif line.startswith("+") and not line.startswith("+++"):
                added += 1
                file_types[current_file_ext] = file_types.get(current_file_ext, 0) + 1
            elif line.startswith("-") and not line.startswith("---"):
                removed += 1

        # Count modified files
        file_paths = self._extract_file_paths(diff)
        modified_files = len(set(file_paths))

        return LOCAnalysis(
            total_lines=added + removed,
            added_lines=added,
            removed_lines=removed,
            modified_files=modified_files,
            file_types=file_types,
        )

    def _calculate_risk_score(
        self,
        factors: list[RiskFactorDetection],
        loc_analysis: LOCAnalysis,
    ) -> int:
        """
        Calculate overall risk score (0-100).

        Formula:
            base_score = len(factors) * 20  # Each factor = 20 points
            loc_multiplier = min(loc / 50, 1.5)  # Up to 1.5x for large changes
            final_score = min(base_score * loc_multiplier, 100)
        """
        # Base score from factors (each factor = 20 points, max 3 factors counted)
        # Critical factors count as 25 points
        factor_score = 0
        for factor in factors[:5]:  # Limit to top 5 factors
            if factor.severity == "critical":
                factor_score += 25
            elif factor.severity == "high":
                factor_score += 20
            elif factor.severity == "medium":
                factor_score += 15
            else:
                factor_score += 10

        # LOC multiplier (larger changes = higher risk)
        loc = loc_analysis.total_lines
        if loc > self.LOC_VERY_LARGE:
            loc_multiplier = 1.5
        elif loc > self.LOC_LARGE:
            loc_multiplier = 1.3
        elif loc > self.LOC_OPTIMAL:
            loc_multiplier = 1.15
        else:
            loc_multiplier = 1.0

        # Calculate final score
        raw_score = factor_score * loc_multiplier

        # Add base LOC score if no factors but large change
        if len(factors) == 0 and loc > self.LOC_OPTIMAL:
            raw_score = min(loc / 3, 40)  # Up to 40 points for LOC alone

        return min(int(raw_score), 100)

    def _determine_risk_level(self, score: int) -> RiskLevel:
        """Determine risk level from score."""
        if score >= 80:
            return RiskLevel.CRITICAL
        elif score >= 60:
            return RiskLevel.HIGH
        elif score >= 40:
            return RiskLevel.MEDIUM
        elif score >= 20:
            return RiskLevel.LOW
        else:
            return RiskLevel.MINIMAL

    def _should_require_planning(
        self,
        score: int,
        factors: list[RiskFactorDetection],
        loc_analysis: LOCAnalysis,
    ) -> bool:
        """
        Determine if planning mode should be required.

        Planning is required if:
            1. Any risk factor is detected (regardless of score)
            2. Risk score >= 50
            3. LOC > 150 with score >= 20
        """
        # Any risk factor detected = planning recommended
        if len(factors) > 0:
            return True

        # High score = planning required
        if score >= self.SCORE_THRESHOLD_REQUIRED:
            return True

        # Large change with some score = planning recommended
        if loc_analysis.total_lines > self.LOC_LARGE and score >= self.SCORE_THRESHOLD_RECOMMENDED:
            return True

        return False

    def _determine_planning_decision(
        self,
        score: int,
        factors: list[RiskFactorDetection],
        loc_analysis: LOCAnalysis,
    ) -> PlanningDecision:
        """Determine specific planning decision."""
        # Check for critical factors
        has_critical = any(f.severity == "critical" for f in factors)

        if score >= self.SCORE_THRESHOLD_CRP or has_critical:
            return PlanningDecision.REQUIRES_CRP
        elif score >= self.SCORE_THRESHOLD_REQUIRED or len(factors) >= 2:
            return PlanningDecision.REQUIRED
        elif score >= self.SCORE_THRESHOLD_RECOMMENDED or len(factors) >= 1:
            return PlanningDecision.RECOMMENDED
        else:
            return PlanningDecision.NOT_REQUIRED

    def _generate_recommendations(
        self,
        factors: list[RiskFactorDetection],
        loc_analysis: LOCAnalysis,
        score: int,
    ) -> list[str]:
        """Generate actionable recommendations."""
        recommendations = []

        # Factor-specific recommendations
        for factor in factors[:3]:  # Top 3 recommendations
            recommendations.append(factor.recommendation)

        # LOC-based recommendations
        if loc_analysis.total_lines > self.LOC_VERY_LARGE:
            recommendations.append(
                f"Consider breaking this {loc_analysis.total_lines}-line change into smaller, reviewable chunks."
            )
        elif loc_analysis.total_lines > self.LOC_OPTIMAL:
            recommendations.append(
                f"SDLC 5.2.0 recommends <60 lines per change. Consider refactoring this {loc_analysis.total_lines}-line change."
            )

        # Multiple files recommendation
        if loc_analysis.modified_files > 5:
            recommendations.append(
                f"This change touches {loc_analysis.modified_files} files. Ensure changes are cohesive."
            )

        # High score recommendation
        if score >= self.SCORE_THRESHOLD_CRP:
            recommendations.append(
                "High-risk change detected. Consider creating a Consultation Request (CRP) for human review."
            )

        return recommendations[:5]  # Limit to 5 recommendations

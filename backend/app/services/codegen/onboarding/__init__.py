"""
Vietnamese SME Onboarding Package.

Sprint 47: Vietnamese Domain Templates + Onboarding IR (EP-06)

This package provides:
1. OnboardingService - Vietnamese questionnaire to IR conversion
2. OnboardingSession - Guided session state management
3. OnboardingPrompts - Vietnamese UI text prompts
4. OnboardingValidator - Input validation for Vietnamese SME

Architecture:
```
Vietnamese Input → OnboardingService → DomainTemplate → AppBlueprint → IR
```

Author: Backend Lead
Date: December 23, 2025
Status: ACTIVE
"""

from .service import OnboardingService, OnboardingSession, OnboardingStep
from .prompts import OnboardingPrompts, VIETNAMESE_PROMPTS
from .validator import OnboardingValidator

__all__ = [
    "OnboardingService",
    "OnboardingSession",
    "OnboardingStep",
    "OnboardingPrompts",
    "VIETNAMESE_PROMPTS",
    "OnboardingValidator",
]

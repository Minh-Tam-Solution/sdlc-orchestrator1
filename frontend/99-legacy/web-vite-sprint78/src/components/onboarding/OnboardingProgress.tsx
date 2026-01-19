/**
 * File: frontend/web/src/components/onboarding/OnboardingProgress.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 15 Day 5
 * Date: December 2, 2025
 * Authority: Frontend Lead + CPO Approved
 * Foundation: User-Onboarding-Flow-Architecture.md
 *
 * Description:
 * Progress indicator component for onboarding wizard.
 * Shows current step and total steps with visual progress bar.
 */

interface OnboardingProgressProps {
  current: number
  total: number
}

/**
 * Onboarding progress component
 *
 * @param current - Current step number (1-based)
 * @param total - Total number of steps
 */
export default function OnboardingProgress({ current, total }: OnboardingProgressProps) {
  const percentage = (current / total) * 100

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between text-sm text-muted-foreground">
        <span>Step {current} of {total}</span>
        <span>{Math.round(percentage)}%</span>
      </div>
      <div className="h-2 w-full rounded-full bg-muted">
        <div
          className="h-2 rounded-full bg-primary transition-all duration-300"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  )
}


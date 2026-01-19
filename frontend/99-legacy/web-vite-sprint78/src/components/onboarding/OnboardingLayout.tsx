/**
 * File: frontend/web/src/components/onboarding/OnboardingLayout.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 15 Day 5
 * Date: December 2, 2025
 * Authority: Frontend Lead + CPO Approved
 * Foundation: User-Onboarding-Flow-Architecture.md, Sprint 15 Plan
 * Framework: SDLC 4.9 Complete Lifecycle
 *
 * Description:
 * Layout component for onboarding wizard steps.
 * Provides consistent structure with title, subtitle, and progress indicator.
 */

import { ReactNode } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'

interface OnboardingLayoutProps {
  step: number
  title: string
  subtitle?: string
  children: ReactNode
}

/**
 * Onboarding layout component
 *
 * @param step - Current step number (1-6) - used by parent components for tracking
 * @param title - Step title
 * @param subtitle - Step subtitle/description
 * @param children - Step content
 */
export default function OnboardingLayout({ step: _step, title, subtitle, children }: OnboardingLayoutProps) {
  // step is passed by parent components for tracking purposes
  void _step
  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <Card>
          <CardHeader className="text-center">
            <CardTitle className="text-2xl">{title}</CardTitle>
            {subtitle && <CardDescription className="text-base mt-2">{subtitle}</CardDescription>}
          </CardHeader>
          <CardContent className="space-y-6">
            {children}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}


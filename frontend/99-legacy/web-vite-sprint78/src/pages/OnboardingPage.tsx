/**
 * File: frontend/web/src/pages/OnboardingPage.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 15 Day 5
 * Date: December 2, 2025
 * Authority: Frontend Lead + CPO Approved
 * Foundation: User-Onboarding-Flow-Architecture.md
 *
 * Description:
 * Onboarding wizard page that routes to different steps.
 * Implements 6-step onboarding flow for first-time users.
 */

import { Routes, Route, Navigate, useLocation } from 'react-router-dom'
import OAuthLogin from '@/components/onboarding/OAuthLogin'
import RepositoryConnect from '@/components/onboarding/RepositoryConnect'
import AIAnalysis from '@/components/onboarding/AIAnalysis'
import PolicyPackSelection from '@/components/onboarding/PolicyPackSelection'
import StageMapping from '@/components/onboarding/StageMapping'
import FirstGateEvaluation from '@/components/onboarding/FirstGateEvaluation'

/**
 * Onboarding page component
 *
 * Routes:
 * - /onboarding - Step 1: OAuth Login
 * - /onboarding/repository - Step 2: Repository Connect
 * - /onboarding/analyzing - Step 3: AI Analysis
 * - /onboarding/policy-pack - Step 4: Policy Pack Selection
 * - /onboarding/stage-mapping - Step 5: Stage Mapping
 * - /onboarding/first-gate - Step 6: First Gate Evaluation
 */
export default function OnboardingPage() {
  const location = useLocation()

  // Redirect root onboarding to first step
  if (location.pathname === '/onboarding') {
    return <Navigate to="/onboarding/login" replace />
  }

  return (
    <Routes>
      <Route path="/login" element={<OAuthLogin />} />
      <Route path="/repository" element={<RepositoryConnect />} />
      <Route path="/analyzing" element={<AIAnalysis />} />
      <Route path="/policy-pack" element={<PolicyPackSelection />} />
      <Route path="/stage-mapping" element={<StageMapping />} />
      <Route path="/first-gate" element={<FirstGateEvaluation />} />
      <Route path="*" element={<Navigate to="/onboarding/login" replace />} />
    </Routes>
  )
}


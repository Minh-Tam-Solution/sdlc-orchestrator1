/**
 * File: frontend/web/src/App.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Root component for SDLC Orchestrator frontend application.
 * Configures routing, authentication, and layout structure.
 */

import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from '@/contexts/AuthContext'
import ProtectedRoute from '@/components/auth/ProtectedRoute'
import LoginPage from '@/pages/LoginPage'
import DashboardPage from '@/pages/DashboardPage'
import ProjectsPage from '@/pages/ProjectsPage'
import ProjectDetailPage from '@/pages/ProjectDetailPage'
import GatesPage from '@/pages/GatesPage'
import GateDetailPage from '@/pages/GateDetailPage'
import EvidencePage from '@/pages/EvidencePage'
import PoliciesPage from '@/pages/PoliciesPage'
import PolicyDetailPage from '@/pages/PolicyDetailPage'
import SettingsPage from '@/pages/SettingsPage'
import OnboardingPage from '@/pages/OnboardingPage'
import GitHubCallbackPage from '@/pages/GitHubCallbackPage'

/**
 * Root App component
 *
 * Routing structure:
 * - /login - Public authentication page
 * - /auth/github/callback - GitHub OAuth callback handler
 * - /onboarding/* - Public onboarding wizard (6 steps)
 * - / - Protected dashboard (requires authentication)
 * - /projects - Protected projects list
 * - /projects/:id - Protected project detail
 * - /gates - Protected gates list
 * - /gates/:id - Protected gate detail
 * - /evidence - Protected evidence vault
 * - /policies - Protected policies library
 *
 * @returns App component with routing configured
 */
function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Public routes */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/auth/github/callback" element={<GitHubCallbackPage />} />
          <Route path="/onboarding/*" element={<OnboardingPage />} />

          {/* Protected routes */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/projects"
            element={
              <ProtectedRoute>
                <ProjectsPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/projects/:id"
            element={
              <ProtectedRoute>
                <ProjectDetailPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/gates"
            element={
              <ProtectedRoute>
                <GatesPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/gates/:id"
            element={
              <ProtectedRoute>
                <GateDetailPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/evidence"
            element={
              <ProtectedRoute>
                <EvidencePage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/policies"
            element={
              <ProtectedRoute>
                <PoliciesPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/policies/:id"
            element={
              <ProtectedRoute>
                <PolicyDetailPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/settings"
            element={
              <ProtectedRoute>
                <SettingsPage />
              </ProtectedRoute>
            }
          />

          {/* Catch-all route - Redirect to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App

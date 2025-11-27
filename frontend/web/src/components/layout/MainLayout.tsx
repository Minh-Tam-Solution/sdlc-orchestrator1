/**
 * File: frontend/web/src/components/layout/MainLayout.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Main layout component wrapping all authenticated pages.
 * Includes sidebar, header, and main content area.
 */

import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'

/**
 * Main layout component
 *
 * @returns Layout with sidebar, header, and content outlet
 */
export default function MainLayout() {
  return (
    <div className="min-h-screen bg-background">
      {/* Sidebar */}
      <Sidebar />

      {/* Header */}
      <Header />

      {/* Main content */}
      <main className="ml-64 pt-16">
        <div className="container mx-auto p-6">
          <Outlet />
        </div>
      </main>
    </div>
  )
}

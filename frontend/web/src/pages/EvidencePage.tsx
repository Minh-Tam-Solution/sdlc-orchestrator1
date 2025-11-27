/**
 * File: frontend/web/src/pages/EvidencePage.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Evidence Vault page for viewing and uploading evidence documents.
 */

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import DashboardLayout from '@/components/layout/DashboardLayout'

/**
 * Evidence page component
 *
 * @returns Evidence vault page
 */
export default function EvidencePage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Page header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Evidence Vault</h1>
            <p className="text-muted-foreground">
              Store and manage evidence documents for gate approvals
            </p>
          </div>
          <Button>
            <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Upload Evidence
          </Button>
        </div>

        {/* Empty state */}
        <Card>
          <CardHeader>
            <CardTitle>Evidence Documents</CardTitle>
            <CardDescription>All uploaded evidence for your projects</CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <svg
              className="h-12 w-12 text-muted-foreground mb-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4"
              />
            </svg>
            <h3 className="text-lg font-medium">No evidence uploaded</h3>
            <p className="text-muted-foreground text-center mt-1">
              Upload documents, screenshots, or files as evidence for gate approvals
            </p>
            <Button className="mt-4">
              <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
              </svg>
              Upload First Evidence
            </Button>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}

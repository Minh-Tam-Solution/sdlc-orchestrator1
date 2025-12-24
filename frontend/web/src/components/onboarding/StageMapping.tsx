/**
 * File: frontend/web/src/components/onboarding/StageMapping.tsx
 * Version: 2.0.0
 * Status: ACTIVE - Sprint 45
 * Date: December 24, 2025
 * Authority: Frontend Lead + CPO Approved
 * Foundation: User-Onboarding-Flow-Architecture.md
 *
 * Description:
 * Step 5: Stage Mapping - 3 minutes
 * Map repository folders to SDLC 5.1.1 stages.
 *
 * Reference: SDLC-Enterprise-Framework/README.md (v5.1.1)
 */

import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Button } from '@/components/ui/button'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Card, CardContent } from '@/components/ui/card'
import OnboardingLayout from './OnboardingLayout'
import OnboardingProgress from './OnboardingProgress'

/**
 * SDLC 5.1.1 Stage Definitions (10 Stages: 00-09 + Archive folder)
 * Reference: SDLC-Enterprise-Framework/README.md
 * Note: 10-archive is a project-level archive folder, not a formal stage
 */
const SDLC_STAGES = [
  { code: '00', name: 'FOUNDATION', description: 'Strategic Discovery & Validation', question: 'WHY?' },
  { code: '01', name: 'PLANNING', description: 'Requirements & User Stories', question: 'WHAT?' },
  { code: '02', name: 'DESIGN', description: 'Architecture & Technical Design', question: 'HOW?' },
  { code: '03', name: 'INTEGRATE', description: 'API Contracts & Third-party Setup', question: 'How connect?' },
  { code: '04', name: 'BUILD', description: 'Development & Implementation', question: 'Building right?' },
  { code: '05', name: 'TEST', description: 'Quality Assurance & Validation', question: 'Works correctly?' },
  { code: '06', name: 'DEPLOY', description: 'Release & Deployment', question: 'Ship safely?' },
  { code: '07', name: 'OPERATE', description: 'Production Operations & Monitoring', question: 'Running reliably?' },
  { code: '08', name: 'COLLABORATE', description: 'Team Coordination & Knowledge', question: 'Team effective?' },
  { code: '09', name: 'GOVERN', description: 'Compliance & Strategic Oversight', question: 'Compliant?' },
  { code: '10', name: 'ARCHIVE', description: 'Project Archive (Legacy Docs)', question: 'Archived?' },
]

interface FolderMapping {
  path: string
  stage: string
}

/**
 * Stage Mapping component (Step 5)
 *
 * Features:
 * - Auto-detect stages from repository
 * - Allow manual adjustment
 * - Show folder → stage mapping
 */
export default function StageMapping() {
  const navigate = useNavigate()
  const [mappings, setMappings] = useState<FolderMapping[]>([])

  // Auto-detect mappings from analysis (simplified - would come from backend)
  useEffect(() => {
    // Default mappings based on SDLC 5.1.1 folder structure
    const defaultMappings: FolderMapping[] = [
      { path: 'docs/00-foundation', stage: '00' },
      { path: 'docs/01-planning', stage: '01' },
      { path: 'docs/02-design', stage: '02' },
      { path: 'docs/03-integrate', stage: '03' },
      { path: 'src', stage: '04' },  // BUILD stage
      { path: 'tests', stage: '05' }, // TEST stage
      { path: 'deploy', stage: '06' }, // DEPLOY stage
    ]
    setMappings(defaultMappings)
  }, [])

  const handleContinue = () => {
    // Store stage mappings
    sessionStorage.setItem('onboarding_stage_mappings', JSON.stringify(mappings))
    navigate('/onboarding/first-gate')
  }

  const updateMapping = (index: number, stage: string) => {
    const updated = [...mappings]
    const item = updated[index]
    if (item) {
      item.stage = stage
      setMappings(updated)
    }
  }

  return (
    <OnboardingLayout
      step={5}
      title="Map Your Project Structure"
      subtitle="We've auto-detected your stages. Adjust if needed."
    >
      <div className="space-y-4">
        <div className="rounded-lg bg-blue-50 dark:bg-blue-950 p-4 text-sm text-blue-900 dark:text-blue-100">
          We mapped your folders to SDLC 5.1.1 stages. You can adjust anytime.
        </div>

        <div className="space-y-2">
          {mappings.map((mapping, index) => (
            <Card key={index}>
              <CardContent className="p-4">
                <div className="flex items-center gap-4">
                  <div className="flex-1 font-mono text-sm">{mapping.path}</div>
                  <div className="text-muted-foreground">→</div>
                  <Select
                    value={mapping.stage}
                    onValueChange={(value) => updateMapping(index, value)}
                  >
                    <SelectTrigger className="w-[300px]">
                      <SelectValue placeholder="Select stage" />
                    </SelectTrigger>
                    <SelectContent>
                      {SDLC_STAGES.map((stage) => (
                        <SelectItem key={stage.code} value={stage.code}>
                          {stage.code} - {stage.name}: {stage.description}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="flex gap-2">
          <Button variant="outline" className="flex-1" onClick={() => navigate('/onboarding/policy-pack')}>
            Back
          </Button>
          <Button size="lg" className="flex-1" onClick={handleContinue}>
            Confirm Mapping
          </Button>
        </div>
      </div>

      <OnboardingProgress current={5} total={6} />
    </OnboardingLayout>
  )
}


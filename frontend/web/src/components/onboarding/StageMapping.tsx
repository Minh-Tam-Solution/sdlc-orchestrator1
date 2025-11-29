/**
 * File: frontend/web/src/components/onboarding/StageMapping.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 15 Day 5
 * Date: December 2, 2025
 * Authority: Frontend Lead + CPO Approved
 * Foundation: User-Onboarding-Flow-Architecture.md
 *
 * Description:
 * Step 5: Stage Mapping - 3 minutes
 * Map repository folders to SDLC 4.9 stages.
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

const SDLC_STAGES = [
  { code: '00', name: 'WHY', description: 'Problem Definition' },
  { code: '01', name: 'WHAT', description: 'Solution Planning' },
  { code: '02', name: 'HOW', description: 'Architecture & Design' },
  { code: '03', name: 'BUILD', description: 'Development' },
  { code: '04', name: 'VERIFY', description: 'Testing & QA' },
  { code: '05', name: 'SHIP', description: 'Release' },
  { code: '06', name: 'OPERATE', description: 'Production' },
  { code: '07', name: 'OBSERVE', description: 'Monitoring' },
  { code: '08', name: 'LEARN', description: 'Retrospective' },
  { code: '09', name: 'EVOLVE', description: 'Iteration' },
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
    // Default mappings based on common folder structures
    const defaultMappings: FolderMapping[] = [
      { path: 'docs/00-Project-Foundation', stage: '00' },
      { path: 'docs/01-Planning-Analysis', stage: '01' },
      { path: 'docs/02-Design-Architecture', stage: '02' },
      { path: 'src', stage: '03' },
      { path: 'tests', stage: '04' },
      { path: 'deploy', stage: '05' },
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
          We mapped your folders to SDLC stages. You can adjust anytime.
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


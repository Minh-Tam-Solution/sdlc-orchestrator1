/**
 * File: frontend/web/src/components/gates/CreateGateDialog.tsx
 * Version: 2.0.0
 * Status: ACTIVE - STAGE 04 (BUILD)
 * Date: 2025-12-24
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 5.1.1 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Dialog for creating new quality gates for a project.
 *
 * Reference: SDLC-Enterprise-Framework/README.md (v5.1.1)
 */

import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import apiClient from '@/api/client'

interface CreateGateDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  projectId: string
}

interface GateCreateData {
  project_id: string
  gate_name: string
  gate_type: string
  stage: string
  description: string
  exit_criteria: Array<{ criterion: string; status: string }>
}

interface GateResponse {
  id: string
  gate_name: string
  status: string
}

/**
 * SDLC 5.1.1 Stage Definitions (10 Stages: 00-09 + Archive folder)
 * Reference: SDLC-Enterprise-Framework/README.md (v5.1.1)
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

/**
 * Quality Gate types aligned with SDLC 5.1.1 stages
 */
const GATE_TYPES = [
  { value: 'FOUNDATION_READY', label: 'Foundation Ready (G0)' },
  { value: 'PLANNING_COMPLETE', label: 'Planning Complete (G1)' },
  { value: 'DESIGN_READY', label: 'Design Ready (G2)' },
  { value: 'INTEGRATE_READY', label: 'Integration Ready (G3)' },
  { value: 'BUILD_COMPLETE', label: 'Build Complete (G4)' },
  { value: 'TEST_PASSED', label: 'Test Passed (G5)' },
  { value: 'DEPLOY_READY', label: 'Deploy Ready (G6)' },
  { value: 'OPERATE_READY', label: 'Operate Ready (G7)' },
  { value: 'COLLABORATE_SETUP', label: 'Collaborate Setup (G8)' },
  { value: 'GOVERN_COMPLETE', label: 'Govern Complete (G9)' },
  { value: 'ARCHIVE_COMPLETE', label: 'Archive Complete (G10)' },
]

/**
 * Create Gate Dialog Component
 */
export default function CreateGateDialog({
  open,
  onOpenChange,
  projectId,
}: CreateGateDialogProps) {
  const [gateName, setGateName] = useState('')
  const [gateType, setGateType] = useState('')
  const [stage, setStage] = useState('')
  const [description, setDescription] = useState('')
  const [exitCriteria, setExitCriteria] = useState('')
  const [error, setError] = useState<string | null>(null)
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  // Create gate mutation
  const createMutation = useMutation<GateResponse, Error, GateCreateData>({
    mutationFn: async (data) => {
      const response = await apiClient.post<GateResponse>('/gates', data)
      return response.data
    },
    onSuccess: (gate) => {
      // Invalidate project and gates list
      queryClient.invalidateQueries({ queryKey: ['project', projectId] })
      queryClient.invalidateQueries({ queryKey: ['gates'] })
      // Reset form
      resetForm()
      // Close dialog
      onOpenChange(false)
      // Navigate to new gate
      navigate(`/gates/${gate.id}`)
    },
    onError: (err: Error & { response?: { status?: number; data?: { detail?: string } } }) => {
      // Handle specific error codes with user-friendly messages
      if (err.response?.status === 403) {
        setError('You do not have permission to create gates for this project. Please contact the project owner.')
      } else if (err.response?.status === 401) {
        setError('Your session has expired. Please log in again.')
      } else if (err.response?.data?.detail) {
        setError(err.response.data.detail)
      } else {
        setError(err.message || 'Failed to create gate')
      }
    },
  })

  const resetForm = () => {
    setGateName('')
    setGateType('')
    setStage('')
    setDescription('')
    setExitCriteria('')
    setError(null)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!gateName.trim()) {
      setError('Gate name is required')
      return
    }

    if (!gateType) {
      setError('Gate type is required')
      return
    }

    if (!stage) {
      setError('Stage is required')
      return
    }

    // Parse exit criteria (one per line)
    const criteria = exitCriteria
      .split('\n')
      .map((line) => line.trim())
      .filter((line) => line.length > 0)
      .map((criterion) => ({ criterion, status: 'pending' }))

    createMutation.mutate({
      project_id: projectId,
      gate_name: gateName.trim(),
      gate_type: gateType,
      stage: stage,
      description: description.trim(),
      exit_criteria: criteria,
    })
  }

  const handleClose = () => {
    resetForm()
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[550px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Create Quality Gate</DialogTitle>
            <DialogDescription>
              Define a new quality gate with exit criteria for this project.
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {/* Gate name */}
            <div className="grid gap-2">
              <Label htmlFor="gateName">Gate Name *</Label>
              <Input
                id="gateName"
                placeholder="E.g., G2 Ship Ready"
                value={gateName}
                onChange={(e) => setGateName(e.target.value)}
                disabled={createMutation.isPending}
                autoFocus
              />
            </div>

            {/* Gate type and Stage row */}
            <div className="grid grid-cols-2 gap-4">
              {/* Gate Type */}
              <div className="grid gap-2">
                <Label htmlFor="gateType">Gate Type *</Label>
                <Select value={gateType} onValueChange={setGateType} disabled={createMutation.isPending}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    {GATE_TYPES.map((type) => (
                      <SelectItem key={type.value} value={type.value}>
                        {type.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Stage */}
              <div className="grid gap-2">
                <Label htmlFor="stage">SDLC Stage *</Label>
                <Select value={stage} onValueChange={setStage} disabled={createMutation.isPending}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select stage" />
                  </SelectTrigger>
                  <SelectContent>
                    {SDLC_STAGES.map((s) => (
                      <SelectItem key={s.code} value={s.code}>
                        {s.code} - {s.name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Description */}
            <div className="grid gap-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                placeholder="Describe the purpose of this gate..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                disabled={createMutation.isPending}
                rows={2}
              />
            </div>

            {/* Exit Criteria */}
            <div className="grid gap-2">
              <Label htmlFor="exitCriteria">Exit Criteria (one per line)</Label>
              <Textarea
                id="exitCriteria"
                placeholder="Zero P0 bugs&#10;95%+ test coverage&#10;Security scan passed"
                value={exitCriteria}
                onChange={(e) => setExitCriteria(e.target.value)}
                disabled={createMutation.isPending}
                rows={4}
              />
              <p className="text-xs text-muted-foreground">
                Enter each exit criterion on a new line. These will be tracked as requirements.
              </p>
            </div>

            {/* Error message */}
            {error && (
              <div className="text-sm text-red-500 bg-red-50 rounded-md p-3">
                {error}
              </div>
            )}
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              disabled={createMutation.isPending}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={createMutation.isPending}>
              {createMutation.isPending ? 'Creating...' : 'Create Gate'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

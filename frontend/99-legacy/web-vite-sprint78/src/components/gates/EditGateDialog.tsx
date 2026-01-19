/**
 * File: frontend/web/src/components/gates/EditGateDialog.tsx
 * Version: 2.0.0
 * Status: ACTIVE - STAGE 04 (BUILD)
 * Date: December 24, 2025
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 5.1.3 Complete Lifecycle
 *
 * Description:
 * Dialog for editing existing quality gates.
 * Uses PUT /gates/{id} API endpoint.
 *
 * Reference: SDLC-Enterprise-Framework/README.md (v5.1.1)
 *
 * SDLC 5.1.3 Compliance:
 * - Pillar 1: Zero Mock Policy (Real API calls)
 * - Pillar 3: Quality Governance (Type hints, validation)
 */

import { useState, useEffect } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
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
import type { GateResponse, GateUpdateRequest } from '@/types/api'

interface EditGateDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  gate: GateResponse
  onSuccess?: (gate: GateResponse) => void
}

/**
 * Quality Gate types aligned with SDLC 5.1.3 stages
 * Reference: SDLC-Enterprise-Framework/README.md (v5.1.1)
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
 * Edit Gate Dialog Component
 *
 * Features:
 * - Pre-populated form with current gate data
 * - Validation for required fields
 * - Error handling with user feedback
 * - Query invalidation on success
 */
export default function EditGateDialog({
  open,
  onOpenChange,
  gate,
  onSuccess,
}: EditGateDialogProps) {
  const [gateName, setGateName] = useState(gate.gate_name)
  const [gateType, setGateType] = useState(gate.gate_type)
  const [description, setDescription] = useState(gate.description || '')
  const [exitCriteria, setExitCriteria] = useState(
    gate.exit_criteria.map((c) => c.criterion).join('\n')
  )
  const [error, setError] = useState<string | null>(null)
  const queryClient = useQueryClient()

  // Update form when gate changes
  useEffect(() => {
    setGateName(gate.gate_name)
    setGateType(gate.gate_type)
    setDescription(gate.description || '')
    setExitCriteria(gate.exit_criteria.map((c) => c.criterion).join('\n'))
    setError(null)
  }, [gate])

  // Update gate mutation
  const updateMutation = useMutation<GateResponse, Error, GateUpdateRequest>({
    mutationFn: async (data) => {
      const response = await apiClient.put<GateResponse>(`/gates/${gate.id}`, data)
      return response.data
    },
    onSuccess: (updatedGate) => {
      // Invalidate gates list and gate detail
      queryClient.invalidateQueries({ queryKey: ['gates'] })
      queryClient.invalidateQueries({ queryKey: ['gate', gate.id] })
      queryClient.invalidateQueries({ queryKey: ['project', gate.project_id] })
      // Reset error
      setError(null)
      // Close dialog
      onOpenChange(false)
      // Call onSuccess callback if provided
      onSuccess?.(updatedGate)
    },
    onError: (err: Error & { response?: { data?: { detail?: string } } }) => {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to update gate'
      setError(errorMessage)
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    const trimmedName = gateName.trim()

    if (!trimmedName) {
      setError('Gate name is required')
      return
    }

    if (trimmedName.length < 3) {
      setError('Gate name must be at least 3 characters')
      return
    }

    if (!gateType) {
      setError('Gate type is required')
      return
    }

    // Parse exit criteria (one per line), preserving status from existing criteria
    const existingCriteriaMap = new Map(
      gate.exit_criteria.map((c) => [c.criterion, c.status])
    )
    const criteria = exitCriteria
      .split('\n')
      .map((line) => line.trim())
      .filter((line) => line.length > 0)
      .map((criterion) => ({
        criterion,
        status: existingCriteriaMap.get(criterion) || 'pending',
      }))

    // Check if anything changed
    const exitCriteriaChanged =
      JSON.stringify(criteria) !== JSON.stringify(gate.exit_criteria)
    const hasChanges =
      trimmedName !== gate.gate_name ||
      gateType !== gate.gate_type ||
      description.trim() !== (gate.description || '') ||
      exitCriteriaChanged

    if (!hasChanges) {
      onOpenChange(false)
      return
    }

    updateMutation.mutate({
      gate_name: trimmedName,
      gate_type: gateType,
      description: description.trim() || '',
      exit_criteria: criteria,
    })
  }

  const handleClose = () => {
    // Reset to original values
    setGateName(gate.gate_name)
    setGateType(gate.gate_type)
    setDescription(gate.description || '')
    setExitCriteria(gate.exit_criteria.map((c) => c.criterion).join('\n'))
    setError(null)
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[550px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Edit Gate</DialogTitle>
            <DialogDescription>
              Update the gate name, type, description, and exit criteria.
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {/* Gate name */}
            <div className="grid gap-2">
              <Label htmlFor="edit-gate-name">Gate Name *</Label>
              <Input
                id="edit-gate-name"
                placeholder="E.g., G2 Ship Ready"
                value={gateName}
                onChange={(e) => {
                  setGateName(e.target.value)
                  setError(null)
                }}
                disabled={updateMutation.isPending}
                autoFocus
              />
              <p className="text-xs text-muted-foreground">
                3+ characters required
              </p>
            </div>

            {/* Gate Type */}
            <div className="grid gap-2">
              <Label htmlFor="edit-gate-type">Gate Type *</Label>
              <Select
                value={gateType}
                onValueChange={(value) => {
                  setGateType(value)
                  setError(null)
                }}
                disabled={updateMutation.isPending}
              >
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

            {/* Description */}
            <div className="grid gap-2">
              <Label htmlFor="edit-gate-description">Description</Label>
              <Textarea
                id="edit-gate-description"
                placeholder="Describe the purpose of this gate..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                disabled={updateMutation.isPending}
                rows={2}
              />
            </div>

            {/* Exit Criteria */}
            <div className="grid gap-2">
              <Label htmlFor="edit-exit-criteria">Exit Criteria (one per line)</Label>
              <Textarea
                id="edit-exit-criteria"
                placeholder="Zero P0 bugs&#10;95%+ test coverage&#10;Security scan passed"
                value={exitCriteria}
                onChange={(e) => setExitCriteria(e.target.value)}
                disabled={updateMutation.isPending}
                rows={4}
              />
              <p className="text-xs text-muted-foreground">
                Enter each exit criterion on a new line. Existing criteria statuses will be preserved.
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
              disabled={updateMutation.isPending}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={updateMutation.isPending}>
              {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

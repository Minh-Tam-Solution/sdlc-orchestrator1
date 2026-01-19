/**
 * File: frontend/web/src/components/gates/DeleteGateDialog.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: November 28, 2025
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 4.9 Complete Lifecycle
 *
 * Description:
 * Dialog for confirming gate deletion with safety warnings.
 * Uses DELETE /gates/{id} API endpoint.
 *
 * SDLC 4.9 Compliance:
 * - Pillar 1: Zero Mock Policy (Real API calls)
 * - Pillar 3: Quality Governance (Type hints, error handling)
 */

import { useState } from 'react'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import apiClient from '@/api/client'
import type { GateResponse } from '@/types/api'

interface DeleteGateDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  gate: GateResponse
  redirectAfterDelete?: boolean
  onSuccess?: () => void
}

/**
 * Delete Gate Dialog Component
 *
 * Features:
 * - Confirmation dialog with gate name verification
 * - Shows evidence count warning
 * - Soft delete via API
 * - Query invalidation on success
 * - Optional redirect after deletion
 */
export default function DeleteGateDialog({
  open,
  onOpenChange,
  gate,
  redirectAfterDelete = false,
  onSuccess,
}: DeleteGateDialogProps) {
  const [confirmName, setConfirmName] = useState('')
  const [error, setError] = useState<string | null>(null)
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  // Delete gate mutation
  const deleteMutation = useMutation<void, Error>({
    mutationFn: async () => {
      await apiClient.delete(`/gates/${gate.id}`)
    },
    onSuccess: () => {
      // Invalidate gates list and project detail
      queryClient.invalidateQueries({ queryKey: ['gates'] })
      queryClient.invalidateQueries({ queryKey: ['project', gate.project_id] })
      // Reset form
      setConfirmName('')
      setError(null)
      // Close dialog
      onOpenChange(false)
      // Call onSuccess callback if provided
      onSuccess?.()
      // Redirect if requested
      if (redirectAfterDelete) {
        navigate(`/projects/${gate.project_id}`)
      }
    },
    onError: (err: Error & { response?: { data?: { detail?: string } } }) => {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to delete gate'
      setError(errorMessage)
    },
  })

  const handleDelete = () => {
    if (confirmName !== gate.gate_name) {
      setError('Gate name does not match. Please type the exact gate name to confirm.')
      return
    }

    deleteMutation.mutate()
  }

  const handleClose = () => {
    setConfirmName('')
    setError(null)
    onOpenChange(false)
  }

  const isConfirmValid = confirmName === gate.gate_name

  return (
    <AlertDialog open={open} onOpenChange={handleClose}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle className="text-red-600">Delete Gate</AlertDialogTitle>
          <AlertDialogDescription className="space-y-3">
            <p>
              Are you sure you want to delete the gate{' '}
              <span className="font-semibold text-foreground">{gate.gate_name}</span>?
            </p>

            {gate.evidence_count > 0 && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3 text-yellow-800">
                <p className="font-medium">Warning</p>
                <p className="text-sm">
                  This gate has {gate.evidence_count} evidence file{gate.evidence_count !== 1 ? 's' : ''} attached.
                  All associated evidence will also be removed.
                </p>
              </div>
            )}

            {gate.approvals.length > 0 && (
              <div className="bg-blue-50 border border-blue-200 rounded-md p-3 text-blue-800">
                <p className="font-medium">Note</p>
                <p className="text-sm">
                  This gate has {gate.approvals.length} approval{gate.approvals.length !== 1 ? 's' : ''} recorded.
                  Approval history will be preserved in audit logs.
                </p>
              </div>
            )}

            <p className="text-sm">
              This action cannot be undone. Type{' '}
              <span className="font-mono font-semibold bg-muted px-1 rounded">{gate.gate_name}</span>{' '}
              to confirm.
            </p>
          </AlertDialogDescription>
        </AlertDialogHeader>

        <div className="py-4">
          <Label htmlFor="confirm-gate-name" className="sr-only">
            Confirm gate name
          </Label>
          <Input
            id="confirm-gate-name"
            placeholder="Type gate name to confirm"
            value={confirmName}
            onChange={(e) => {
              setConfirmName(e.target.value)
              setError(null)
            }}
            disabled={deleteMutation.isPending}
            className={error ? 'border-red-500' : ''}
          />
          {error && (
            <p className="text-sm text-red-500 mt-2">{error}</p>
          )}
        </div>

        <AlertDialogFooter>
          <AlertDialogCancel onClick={handleClose} disabled={deleteMutation.isPending}>
            Cancel
          </AlertDialogCancel>
          <AlertDialogAction
            onClick={handleDelete}
            disabled={!isConfirmValid || deleteMutation.isPending}
            className="bg-red-600 hover:bg-red-700 focus:ring-red-600"
          >
            {deleteMutation.isPending ? 'Deleting...' : 'Delete Gate'}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}

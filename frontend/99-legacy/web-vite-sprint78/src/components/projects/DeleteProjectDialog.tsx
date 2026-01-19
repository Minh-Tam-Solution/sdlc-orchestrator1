/**
 * File: frontend/web/src/components/projects/DeleteProjectDialog.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: November 28, 2025
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 4.9 Complete Lifecycle
 *
 * Description:
 * Confirmation dialog for deleting SDLC projects.
 * Uses DELETE /projects/{id} API endpoint.
 * Requires user to type project name for confirmation.
 *
 * SDLC 4.9 Compliance:
 * - Pillar 1: Zero Mock Policy (Real API calls)
 * - Pillar 3: Quality Governance (Type hints, error handling)
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
import apiClient from '@/api/client'
import type { Project } from '@/types/api'

interface DeleteProjectDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  project: Project
  redirectAfterDelete?: boolean
  onSuccess?: () => void
}

/**
 * Delete Project Dialog Component
 *
 * Features:
 * - Confirmation by typing project name
 * - Warning about affected gates and evidence
 * - Soft delete (sets deleted_at, preserves data)
 * - Optional redirect to projects list after delete
 */
export default function DeleteProjectDialog({
  open,
  onOpenChange,
  project,
  redirectAfterDelete = true,
  onSuccess,
}: DeleteProjectDialogProps) {
  const [confirmName, setConfirmName] = useState('')
  const [error, setError] = useState<string | null>(null)
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  // Delete project mutation
  const deleteMutation = useMutation<void, Error, string>({
    mutationFn: async (projectId) => {
      await apiClient.delete(`/projects/${projectId}`)
    },
    onSuccess: () => {
      // Invalidate projects list
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      // Remove project from cache
      queryClient.removeQueries({ queryKey: ['project', project.id] })
      // Reset form
      setConfirmName('')
      setError(null)
      // Close dialog
      onOpenChange(false)
      // Call onSuccess callback if provided
      onSuccess?.()
      // Redirect to projects list if requested
      if (redirectAfterDelete) {
        navigate('/projects')
      }
    },
    onError: (err: Error & { response?: { data?: { detail?: string } } }) => {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to delete project'
      setError(errorMessage)
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (confirmName !== project.name) {
      setError('Project name does not match. Please type the exact project name.')
      return
    }

    deleteMutation.mutate(project.id)
  }

  const handleClose = () => {
    setConfirmName('')
    setError(null)
    onOpenChange(false)
  }

  const isConfirmEnabled = confirmName === project.name

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[500px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle className="text-red-600">Delete Project</DialogTitle>
            <DialogDescription>
              This action cannot be undone. This will permanently delete the project
              and all associated data.
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {/* Warning box */}
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <div className="flex items-start gap-3">
                <svg
                  className="h-5 w-5 text-red-600 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
                <div className="text-sm text-red-800">
                  <p className="font-medium">You are about to delete:</p>
                  <p className="mt-1">
                    <strong>{project.name}</strong>
                  </p>
                  <p className="mt-2">This will also affect:</p>
                  <ul className="list-disc list-inside mt-1 space-y-1">
                    <li>All quality gates associated with this project</li>
                    <li>All evidence files linked to those gates</li>
                    <li>All policy evaluations and approvals</li>
                  </ul>
                </div>
              </div>
            </div>

            {/* Confirmation input */}
            <div className="grid gap-2">
              <Label htmlFor="confirm-name">
                Type <span className="font-mono font-bold">{project.name}</span> to confirm
              </Label>
              <Input
                id="confirm-name"
                placeholder="Enter project name"
                value={confirmName}
                onChange={(e) => {
                  setConfirmName(e.target.value)
                  setError(null)
                }}
                disabled={deleteMutation.isPending}
                autoComplete="off"
              />
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
              disabled={deleteMutation.isPending}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              variant="destructive"
              disabled={deleteMutation.isPending || !isConfirmEnabled}
            >
              {deleteMutation.isPending ? 'Deleting...' : 'Delete Project'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

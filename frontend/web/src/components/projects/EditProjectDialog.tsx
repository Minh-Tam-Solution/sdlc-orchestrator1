/**
 * File: frontend/web/src/components/projects/EditProjectDialog.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: November 28, 2025
 * Authority: Frontend Lead + CTO Approved
 * Framework: SDLC 4.9 Complete Lifecycle
 *
 * Description:
 * Dialog for editing existing SDLC projects.
 * Uses PUT /projects/{id} API endpoint.
 *
 * SDLC 4.9 Compliance:
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
import apiClient from '@/api/client'
import type { Project, ProjectUpdateRequest } from '@/types/api'

interface EditProjectDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  project: Project
  onSuccess?: (project: Project) => void
}

/**
 * Edit Project Dialog Component
 *
 * Features:
 * - Pre-populated form with current project data
 * - Validation for required fields
 * - Error handling with user feedback
 * - Query invalidation on success
 */
export default function EditProjectDialog({
  open,
  onOpenChange,
  project,
  onSuccess,
}: EditProjectDialogProps) {
  const [name, setName] = useState(project.name)
  const [description, setDescription] = useState(project.description || '')
  const [error, setError] = useState<string | null>(null)
  const queryClient = useQueryClient()

  // Update form when project changes
  useEffect(() => {
    setName(project.name)
    setDescription(project.description || '')
    setError(null)
  }, [project])

  // Update project mutation
  const updateMutation = useMutation<Project, Error, ProjectUpdateRequest>({
    mutationFn: async (data) => {
      const response = await apiClient.put<Project>(`/projects/${project.id}`, data)
      return response.data
    },
    onSuccess: (updatedProject) => {
      // Invalidate projects list and project detail
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      queryClient.invalidateQueries({ queryKey: ['project', project.id] })
      // Reset error
      setError(null)
      // Close dialog
      onOpenChange(false)
      // Call onSuccess callback if provided
      onSuccess?.(updatedProject)
    },
    onError: (err: Error & { response?: { data?: { detail?: string } } }) => {
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to update project'
      setError(errorMessage)
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    const trimmedName = name.trim()

    if (!trimmedName) {
      setError('Project name is required')
      return
    }

    if (trimmedName.length < 3) {
      setError('Project name must be at least 3 characters')
      return
    }

    if (trimmedName.length > 100) {
      setError('Project name must be less than 100 characters')
      return
    }

    // Only submit if something changed
    if (trimmedName === project.name && description.trim() === (project.description || '')) {
      onOpenChange(false)
      return
    }

    updateMutation.mutate({
      name: trimmedName,
      description: description.trim() || '',
    })
  }

  const handleClose = () => {
    // Reset to original values
    setName(project.name)
    setDescription(project.description || '')
    setError(null)
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[500px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Edit Project</DialogTitle>
            <DialogDescription>
              Update the project name and description.
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {/* Project name */}
            <div className="grid gap-2">
              <Label htmlFor="edit-name">Project Name *</Label>
              <Input
                id="edit-name"
                placeholder="E.g., E-commerce Platform v2.0"
                value={name}
                onChange={(e) => {
                  setName(e.target.value)
                  setError(null)
                }}
                disabled={updateMutation.isPending}
                autoFocus
              />
              <p className="text-xs text-muted-foreground">
                3-100 characters required
              </p>
            </div>

            {/* Description */}
            <div className="grid gap-2">
              <Label htmlFor="edit-description">Description</Label>
              <Textarea
                id="edit-description"
                placeholder="Describe your project goals and scope..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                disabled={updateMutation.isPending}
                rows={3}
              />
              <p className="text-xs text-muted-foreground">
                Optional. Maximum 500 characters.
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

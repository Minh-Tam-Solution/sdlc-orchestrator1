/**
 * File: frontend/web/src/components/projects/CreateProjectDialog.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Dialog for creating new SDLC projects.
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
import apiClient from '@/api/client'

interface CreateProjectDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
}

interface ProjectCreateData {
  name: string
  description: string
}

interface ProjectResponse {
  id: string
  name: string
  slug: string
  description: string | null
}

/**
 * Create Project Dialog Component
 */
export default function CreateProjectDialog({
  open,
  onOpenChange,
}: CreateProjectDialogProps) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState<string | null>(null)
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  // Create project mutation
  const createMutation = useMutation<ProjectResponse, Error, ProjectCreateData>({
    mutationFn: async (data) => {
      const response = await apiClient.post<ProjectResponse>('/projects', data)
      return response.data
    },
    onSuccess: (project) => {
      // Invalidate projects list
      queryClient.invalidateQueries({ queryKey: ['projects'] })
      // Reset form
      setName('')
      setDescription('')
      setError(null)
      // Close dialog
      onOpenChange(false)
      // Navigate to new project
      navigate(`/projects/${project.id}`)
    },
    onError: (err) => {
      setError(err.message || 'Failed to create project')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!name.trim()) {
      setError('Project name is required')
      return
    }

    createMutation.mutate({
      name: name.trim(),
      description: description.trim(),
    })
  }

  const handleClose = () => {
    setName('')
    setDescription('')
    setError(null)
    onOpenChange(false)
  }

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[500px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Create New Project</DialogTitle>
            <DialogDescription>
              Start a new SDLC project to track quality gates and evidence.
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {/* Project name */}
            <div className="grid gap-2">
              <Label htmlFor="name">Project Name *</Label>
              <Input
                id="name"
                placeholder="E.g., E-commerce Platform v2.0"
                value={name}
                onChange={(e) => setName(e.target.value)}
                disabled={createMutation.isPending}
                autoFocus
              />
            </div>

            {/* Description */}
            <div className="grid gap-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                placeholder="Describe your project goals and scope..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                disabled={createMutation.isPending}
                rows={3}
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
              disabled={createMutation.isPending}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={createMutation.isPending}>
              {createMutation.isPending ? 'Creating...' : 'Create Project'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

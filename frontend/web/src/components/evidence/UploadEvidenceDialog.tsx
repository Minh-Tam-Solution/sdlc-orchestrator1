/**
 * File: frontend/web/src/components/evidence/UploadEvidenceDialog.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Dialog for uploading evidence files to a gate.
 * Supports file selection and evidence type categorization.
 */

import { useState, useRef } from 'react'
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

interface UploadEvidenceDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  gateId: string
  gateName: string
}

interface EvidenceResponse {
  id: string
  file_name: string
  file_size: number
  evidence_type: string
  sha256_hash: string
}

// Evidence types based on backend validation
const EVIDENCE_TYPES = [
  { value: 'DESIGN_DOCUMENT', label: 'Design Document', description: 'Architecture, wireframes, mockups' },
  { value: 'TEST_RESULTS', label: 'Test Results', description: 'Unit tests, integration tests, coverage reports' },
  { value: 'CODE_REVIEW', label: 'Code Review', description: 'PR reviews, code analysis reports' },
  { value: 'DEPLOYMENT_PROOF', label: 'Deployment Proof', description: 'Deployment logs, release notes' },
  { value: 'DOCUMENTATION', label: 'Documentation', description: 'API docs, user guides, runbooks' },
  { value: 'COMPLIANCE', label: 'Compliance', description: 'Security scans, audit reports, certifications' },
]

/**
 * Upload Evidence Dialog Component
 */
export default function UploadEvidenceDialog({
  open,
  onOpenChange,
  gateId,
  gateName,
}: UploadEvidenceDialogProps) {
  const [evidenceType, setEvidenceType] = useState('')
  const [description, setDescription] = useState('')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [uploadProgress, setUploadProgress] = useState(0)
  const fileInputRef = useRef<HTMLInputElement>(null)
  const queryClient = useQueryClient()

  // Upload evidence mutation
  const uploadMutation = useMutation<EvidenceResponse, Error, FormData>({
    mutationFn: async (formData) => {
      const response = await apiClient.post<EvidenceResponse>('/evidence/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            setUploadProgress(progress)
          }
        },
      })
      return response.data
    },
    onSuccess: () => {
      // Invalidate gate query to refresh evidence count
      queryClient.invalidateQueries({ queryKey: ['gate', gateId] })
      queryClient.invalidateQueries({ queryKey: ['evidence', gateId] })
      // Reset form
      resetForm()
      // Close dialog
      onOpenChange(false)
    },
    onError: (err) => {
      setError(err.message || 'Failed to upload evidence')
      setUploadProgress(0)
    },
  })

  const resetForm = () => {
    setEvidenceType('')
    setDescription('')
    setSelectedFile(null)
    setError(null)
    setUploadProgress(0)
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      // Check file size (100MB limit)
      if (file.size > 100 * 1024 * 1024) {
        setError('File size must be less than 100MB')
        return
      }
      setSelectedFile(file)
      setError(null)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!selectedFile) {
      setError('Please select a file to upload')
      return
    }

    if (!evidenceType) {
      setError('Please select an evidence type')
      return
    }

    const formData = new FormData()
    formData.append('gate_id', gateId)
    formData.append('evidence_type', evidenceType)
    formData.append('description', description.trim())
    formData.append('file', selectedFile)

    uploadMutation.mutate(formData)
  }

  const handleClose = () => {
    if (!uploadMutation.isPending) {
      resetForm()
      onOpenChange(false)
    }
  }

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
  }

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[550px]">
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>Upload Evidence</DialogTitle>
            <DialogDescription>
              Upload evidence file for gate: <span className="font-medium">{gateName}</span>
            </DialogDescription>
          </DialogHeader>

          <div className="grid gap-4 py-4">
            {/* File selection */}
            <div className="grid gap-2">
              <Label htmlFor="file">File *</Label>
              <div className="flex items-center gap-2">
                <input
                  ref={fileInputRef}
                  id="file"
                  type="file"
                  onChange={handleFileChange}
                  disabled={uploadMutation.isPending}
                  className="hidden"
                />
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={uploadMutation.isPending}
                  className="w-full justify-start text-muted-foreground"
                >
                  {selectedFile ? (
                    <span className="text-foreground truncate">
                      {selectedFile.name} ({formatFileSize(selectedFile.size)})
                    </span>
                  ) : (
                    <span className="flex items-center gap-2">
                      <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                      </svg>
                      Choose file...
                    </span>
                  )}
                </Button>
              </div>
              <p className="text-xs text-muted-foreground">
                Maximum file size: 100MB
              </p>
            </div>

            {/* Evidence Type */}
            <div className="grid gap-2">
              <Label htmlFor="evidenceType">Evidence Type *</Label>
              <Select value={evidenceType} onValueChange={setEvidenceType} disabled={uploadMutation.isPending}>
                <SelectTrigger>
                  <SelectValue placeholder="Select evidence type" />
                </SelectTrigger>
                <SelectContent>
                  {EVIDENCE_TYPES.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      <div>
                        <div className="font-medium">{type.label}</div>
                        <div className="text-xs text-muted-foreground">{type.description}</div>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Description */}
            <div className="grid gap-2">
              <Label htmlFor="description">Description</Label>
              <Textarea
                id="description"
                placeholder="Describe the evidence file..."
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                disabled={uploadMutation.isPending}
                rows={2}
              />
            </div>

            {/* Upload progress */}
            {uploadMutation.isPending && (
              <div className="space-y-2">
                <div className="flex items-center justify-between text-sm">
                  <span className="text-muted-foreground">Uploading...</span>
                  <span className="font-medium">{uploadProgress}%</span>
                </div>
                <div className="h-2 w-full rounded-full bg-muted">
                  <div
                    className="h-2 rounded-full bg-primary transition-all"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
              </div>
            )}

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
              disabled={uploadMutation.isPending}
            >
              Cancel
            </Button>
            <Button type="submit" disabled={uploadMutation.isPending || !selectedFile}>
              {uploadMutation.isPending ? 'Uploading...' : 'Upload Evidence'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

/**
 * File: frontend/web/src/components/ui/form-dialog.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: November 28, 2025
 * Authority: Frontend Lead + CTO Approved
 * Foundation: Sprint 19 - CRUD Operations
 * Framework: SDLC 4.9 Complete Lifecycle
 *
 * Description:
 * Reusable form dialog component for create/edit operations.
 * Wraps form content in a dialog with standard header/footer.
 *
 * SDLC 4.9 Compliance:
 * - Pillar 1: Zero Mock Policy (Real implementations)
 * - Pillar 3: Quality Governance (Type hints, reusable)
 */

import { useState, FormEvent, ReactNode } from 'react'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'

export interface FormDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  title: string
  description?: string
  submitText?: string
  cancelText?: string
  onSubmit: () => void | Promise<void>
  isLoading?: boolean
  isValid?: boolean
  children: ReactNode
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

const sizeClasses = {
  sm: 'sm:max-w-[400px]',
  md: 'sm:max-w-[500px]',
  lg: 'sm:max-w-[600px]',
  xl: 'sm:max-w-[800px]',
}

/**
 * Reusable form dialog component
 *
 * @example
 * ```tsx
 * <FormDialog
 *   open={isOpen}
 *   onOpenChange={setIsOpen}
 *   title="Create Project"
 *   description="Enter the details for your new project"
 *   onSubmit={handleSubmit}
 *   isLoading={createMutation.isPending}
 * >
 *   <div className="grid gap-4">
 *     <Input label="Name" value={name} onChange={setName} />
 *     <Textarea label="Description" value={desc} onChange={setDesc} />
 *   </div>
 * </FormDialog>
 * ```
 */
export function FormDialog({
  open,
  onOpenChange,
  title,
  description,
  submitText = 'Save',
  cancelText = 'Cancel',
  onSubmit,
  isLoading: externalLoading,
  isValid = true,
  children,
  size = 'md',
}: FormDialogProps) {
  const [internalLoading, setInternalLoading] = useState(false)
  const isLoading = externalLoading ?? internalLoading

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    if (!isValid || isLoading) return

    try {
      setInternalLoading(true)
      await onSubmit()
    } catch (error) {
      // Error handling should be done in the onSubmit callback
      console.error('Form submission failed:', error)
    } finally {
      setInternalLoading(false)
    }
  }

  const handleClose = () => {
    if (!isLoading) {
      onOpenChange(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className={sizeClasses[size]}>
        <form onSubmit={handleSubmit}>
          <DialogHeader>
            <DialogTitle>{title}</DialogTitle>
            {description && <DialogDescription>{description}</DialogDescription>}
          </DialogHeader>

          <div className="py-4">{children}</div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              disabled={isLoading}
            >
              {cancelText}
            </Button>
            <Button type="submit" disabled={isLoading || !isValid}>
              {isLoading ? (
                <>
                  <svg
                    className="mr-2 h-4 w-4 animate-spin"
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle
                      className="opacity-25"
                      cx="12"
                      cy="12"
                      r="10"
                      stroke="currentColor"
                      strokeWidth="4"
                    />
                    <path
                      className="opacity-75"
                      fill="currentColor"
                      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                    />
                  </svg>
                  Saving...
                </>
              ) : (
                submitText
              )}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

export default FormDialog

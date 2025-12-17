/**
 * File: frontend/web/src/components/admin/DeleteUserDialog.tsx
 * Version: 1.0.0
 * Status: ACTIVE - Sprint 40 Admin Panel CRUD
 * Date: 2025-12-17
 * Authority: CTO Approved (Sprint 40)
 * Framework: SDLC 5.1.1 Complete Lifecycle
 *
 * Description:
 * Confirmation dialog for deleting (soft delete) users.
 * Shows warning and user email for confirmation.
 *
 * Security:
 * - Cannot delete self
 * - Cannot delete last superuser
 * - Soft delete preserves audit trail
 * - Toast feedback on success/error
 */

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
import { useToast } from '@/hooks/useToast'
import { useDeleteAdminUser, AdminUserListItem } from '@/api/admin'

interface DeleteUserDialogProps {
  user: AdminUserListItem | null
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function DeleteUserDialog({ user, open, onOpenChange }: DeleteUserDialogProps) {
  const { toast } = useToast()
  const deleteUserMutation = useDeleteAdminUser()

  const handleDelete = async () => {
    if (!user) return

    try {
      await deleteUserMutation.mutateAsync(user.id)

      toast({
        title: 'User Deleted',
        description: `User ${user.email} has been deleted successfully`,
        variant: 'success',
      })

      onOpenChange(false)
    } catch (error: any) {
      console.error('Failed to delete user:', error)

      // Check for specific error messages
      const errorMessage =
        error.response?.data?.detail || 'Failed to delete user. Please try again.'

      toast({
        title: 'Error',
        description: errorMessage,
        variant: 'error',
      })
    }
  }

  if (!user) return null

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Delete User?</AlertDialogTitle>
          <AlertDialogDescription>
            Are you sure you want to delete the user <strong>{user.email}</strong>?
          </AlertDialogDescription>
        </AlertDialogHeader>

        <div className="rounded-lg bg-amber-50 border border-amber-200 p-4">
          <div className="flex gap-3">
            <svg
              className="h-5 w-5 text-amber-600 flex-shrink-0 mt-0.5"
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
            <div className="flex-1">
              <h4 className="text-sm font-medium text-amber-800">Warning</h4>
              <div className="mt-1 text-sm text-amber-700 space-y-1">
                <p>This action will:</p>
                <ul className="list-disc list-inside ml-2">
                  <li>Deactivate the user account</li>
                  <li>Prevent the user from logging in</li>
                  <li>Preserve all audit logs and history</li>
                </ul>
                <p className="mt-2">
                  <strong>Note:</strong> This is a soft delete. User data is preserved for
                  audit purposes.
                </p>
              </div>
            </div>
          </div>
        </div>

        <AlertDialogFooter>
          <AlertDialogCancel disabled={deleteUserMutation.isPending}>
            Cancel
          </AlertDialogCancel>
          <AlertDialogAction
            onClick={handleDelete}
            disabled={deleteUserMutation.isPending}
            className="bg-red-600 hover:bg-red-700"
          >
            {deleteUserMutation.isPending ? 'Deleting...' : 'Delete User'}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}

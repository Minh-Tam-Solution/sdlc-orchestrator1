"use client";

/**
 * User Management Page - Next.js App Router
 * @route /admin/users
 * @status Sprint 68 - Admin Section Migration
 * @description CRUD operations for users with bulk actions
 * @security Requires is_superuser=true
 */

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Checkbox } from "@/components/ui/checkbox";
import { Skeleton } from "@/components/ui/skeleton";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  useAdminUsers,
  useUpdateAdminUser,
  useBulkUserAction,
} from "@/hooks/useAdmin";
import { useAuth } from "@/hooks/useAuth";
import { useToast } from "@/hooks/useToast";
import {
  CreateUserDialog,
  EditUserDialog,
  DeleteUserDialog,
  BulkDeleteUsersDialog,
} from "@/components/admin";
import {
  ArrowLeft,
  Plus,
  User,
  Search,
} from "lucide-react";
import type { AdminUser } from "@/lib/types/admin";

export default function UserManagementPage() {
  const router = useRouter();
  const { user: currentUser } = useAuth();
  const { toast } = useToast();

  // Search and filter state
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [activeFilter, setActiveFilter] = useState<boolean | undefined>(undefined);
  const [superuserFilter, setSuperuserFilter] = useState<boolean | undefined>(undefined);

  // Selected users for bulk actions
  const [selectedUsers, setSelectedUsers] = useState<string[]>([]);

  // Dialog state
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [deleteDialogUser, setDeleteDialogUser] = useState<AdminUser | null>(null);
  const [editDialogUser, setEditDialogUser] = useState<AdminUser | null>(null);
  const [bulkDeleteDialogOpen, setBulkDeleteDialogOpen] = useState(false);

  // Fetch users
  const {
    data: usersData,
    isLoading,
    refetch,
  } = useAdminUsers({
    page,
    page_size: 20,
    search: search || undefined,
    is_active: activeFilter,
    is_superuser: superuserFilter,
  });

  // Mutations
  const updateUserMutation = useUpdateAdminUser();
  const bulkActionMutation = useBulkUserAction();

  const handleToggleActive = async (user: AdminUser) => {
    try {
      await updateUserMutation.mutateAsync({
        userId: user.id,
        data: { is_active: !user.is_active },
      });
      toast({
        title: user.is_active ? "User Deactivated" : "User Activated",
        description: `${user.email} has been ${user.is_active ? "deactivated" : "activated"}`,
      });
    } catch {
      toast({
        title: "Error",
        description: "Failed to update user status",
        variant: "destructive",
      });
    }
  };

  const handleToggleSuperuser = async (user: AdminUser) => {
    try {
      await updateUserMutation.mutateAsync({
        userId: user.id,
        data: { is_superuser: !user.is_superuser },
      });
      toast({
        title: user.is_superuser ? "Admin Removed" : "Admin Added",
        description: `${user.email} ${user.is_superuser ? "is no longer an admin" : "is now an admin"}`,
      });
    } catch {
      toast({
        title: "Error",
        description: "Failed to update admin status",
        variant: "destructive",
      });
    }
  };

  const handleBulkAction = async (action: "activate" | "deactivate") => {
    if (selectedUsers.length === 0) return;

    try {
      const result = await bulkActionMutation.mutateAsync({
        user_ids: selectedUsers,
        action,
      });

      if (result.failed_count > 0) {
        toast({
          title: "Partial Success",
          description: `${result.success_count} users ${action}d, ${result.failed_count} failed`,
        });
      } else {
        toast({
          title: "Bulk Action Complete",
          description: `${result.success_count} user(s) ${action}d successfully`,
        });
      }

      setSelectedUsers([]);
      refetch();
    } catch {
      toast({
        title: "Bulk Action Failed",
        description: `Failed to ${action} users`,
        variant: "destructive",
      });
    }
  };

  const toggleUserSelection = (userId: string) => {
    setSelectedUsers((prev) =>
      prev.includes(userId)
        ? prev.filter((id) => id !== userId)
        : [...prev, userId]
    );
  };

  const selectAllUsers = () => {
    if (!usersData?.items) return;

    const allIds = usersData.items
      .filter((u) => u.id !== currentUser?.id)
      .map((u) => u.id);

    setSelectedUsers((prev) =>
      prev.length === allIds.length ? [] : allIds
    );
  };

  const selectableCount = usersData?.items.filter(
    (u) => u.id !== currentUser?.id
  ).length || 0;

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div className="flex items-center justify-between">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => router.push("/admin")}
              className="h-8 w-8 p-0"
            >
              <ArrowLeft className="h-4 w-4" />
            </Button>
            <h1 className="text-3xl font-bold tracking-tight">
              User Management
            </h1>
          </div>
          <p className="text-muted-foreground">
            Manage user accounts, permissions, and access
          </p>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-sm text-muted-foreground">
            {usersData?.total ?? 0} users total
          </div>
          <Button onClick={() => setCreateDialogOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Create User
          </Button>
        </div>
      </div>

      {/* Search and filters */}
      <Card>
        <CardContent className="pt-6">
          <div className="flex flex-wrap gap-4">
            <div className="flex-1 min-w-[200px] relative">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search by email or name..."
                value={search}
                onChange={(e) => {
                  setSearch(e.target.value);
                  setPage(1);
                }}
                className="pl-10 w-full"
              />
            </div>
            <div className="flex gap-2">
              <Button
                variant={activeFilter === true ? "default" : "outline"}
                size="sm"
                onClick={() => {
                  setActiveFilter(activeFilter === true ? undefined : true);
                  setPage(1);
                }}
              >
                Active
              </Button>
              <Button
                variant={activeFilter === false ? "default" : "outline"}
                size="sm"
                onClick={() => {
                  setActiveFilter(activeFilter === false ? undefined : false);
                  setPage(1);
                }}
              >
                Inactive
              </Button>
              <Button
                variant={superuserFilter === true ? "default" : "outline"}
                size="sm"
                onClick={() => {
                  setSuperuserFilter(
                    superuserFilter === true ? undefined : true
                  );
                  setPage(1);
                }}
              >
                Admins Only
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Bulk actions */}
      {selectedUsers.length > 0 && (
        <Card className="border-primary">
          <CardContent className="py-3">
            <div className="flex items-center justify-between">
              <span className="text-sm">
                {selectedUsers.length} user(s) selected
              </span>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleBulkAction("activate")}
                  disabled={bulkActionMutation.isPending}
                >
                  Activate Selected
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleBulkAction("deactivate")}
                  disabled={bulkActionMutation.isPending}
                >
                  Deactivate Selected
                </Button>
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => setBulkDeleteDialogOpen(true)}
                  disabled={bulkActionMutation.isPending}
                >
                  Delete Selected
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => setSelectedUsers([])}
                >
                  Clear Selection
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Users table */}
      <Card>
        <CardHeader>
          <CardTitle>Users</CardTitle>
          <CardDescription>
            Click on actions to manage individual users or select multiple for
            bulk operations
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-3">
              {[1, 2, 3, 4, 5].map((i) => (
                <Skeleton key={i} className="h-16 w-full" />
              ))}
            </div>
          ) : usersData?.items && usersData.items.length > 0 ? (
            <>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead className="w-12">
                      <Checkbox
                        checked={
                          selectedUsers.length > 0 &&
                          selectedUsers.length === selectableCount
                        }
                        onCheckedChange={selectAllUsers}
                      />
                    </TableHead>
                    <TableHead>User</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Created</TableHead>
                    <TableHead>Last Login</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {usersData.items.map((user) => (
                    <TableRow key={user.id}>
                      <TableCell>
                        <Checkbox
                          checked={selectedUsers.includes(user.id)}
                          onCheckedChange={() => toggleUserSelection(user.id)}
                          disabled={user.id === currentUser?.id}
                        />
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-3">
                          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-muted text-muted-foreground">
                            <User className="h-4 w-4" />
                          </div>
                          <div>
                            <p className="font-medium">
                              {user.name || "No Name"}
                              {user.id === currentUser?.id && (
                                <span className="ml-2 text-xs text-muted-foreground">
                                  (You)
                                </span>
                              )}
                            </p>
                            <p className="text-sm text-muted-foreground">
                              {user.email}
                            </p>
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="flex gap-2">
                          <Badge
                            variant={user.is_active ? "default" : "secondary"}
                          >
                            {user.is_active ? "Active" : "Inactive"}
                          </Badge>
                          {user.is_superuser && (
                            <Badge variant="outline">Admin</Badge>
                          )}
                        </div>
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {new Date(user.created_at).toLocaleDateString()}
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {user.last_login
                          ? new Date(user.last_login).toLocaleDateString()
                          : "Never"}
                      </TableCell>
                      <TableCell>
                        <div className="flex gap-2">
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => setEditDialogUser(user)}
                          >
                            Edit
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleToggleActive(user)}
                            disabled={
                              user.id === currentUser?.id ||
                              updateUserMutation.isPending
                            }
                          >
                            {user.is_active ? "Deactivate" : "Activate"}
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleToggleSuperuser(user)}
                            disabled={
                              user.id === currentUser?.id ||
                              updateUserMutation.isPending
                            }
                          >
                            {user.is_superuser ? "Remove Admin" : "Make Admin"}
                          </Button>
                          <Button
                            variant="destructive"
                            size="sm"
                            onClick={() => setDeleteDialogUser(user)}
                            disabled={user.id === currentUser?.id}
                          >
                            Delete
                          </Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              {/* Pagination */}
              {usersData.pages > 1 && (
                <div className="flex items-center justify-between mt-4 pt-4 border-t">
                  <div className="text-sm text-muted-foreground">
                    Page {usersData.page} of {usersData.pages}
                  </div>
                  <div className="flex gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setPage((p) => Math.max(1, p - 1))}
                      disabled={page === 1}
                    >
                      Previous
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() =>
                        setPage((p) => Math.min(usersData.pages, p + 1))
                      }
                      disabled={page === usersData.pages}
                    >
                      Next
                    </Button>
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="text-center py-8 text-muted-foreground">
              <p>No users found</p>
              {search && (
                <p className="text-sm mt-1">
                  Try adjusting your search or filters
                </p>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Dialogs */}
      <CreateUserDialog
        open={createDialogOpen}
        onOpenChange={setCreateDialogOpen}
      />
      <EditUserDialog
        user={editDialogUser}
        open={editDialogUser !== null}
        onOpenChange={(open) => !open && setEditDialogUser(null)}
      />
      <DeleteUserDialog
        user={deleteDialogUser}
        open={deleteDialogUser !== null}
        onOpenChange={(open) => !open && setDeleteDialogUser(null)}
      />
      <BulkDeleteUsersDialog
        users={
          usersData?.items.filter((u) => selectedUsers.includes(u.id)) ?? []
        }
        open={bulkDeleteDialogOpen}
        onOpenChange={setBulkDeleteDialogOpen}
        onSuccess={() => {
          setSelectedUsers([]);
          refetch();
        }}
      />
    </div>
  );
}

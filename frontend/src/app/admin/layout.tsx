/**
 * Admin Panel Layout - SDLC Orchestrator
 *
 * @module frontend/landing/src/app/admin/layout
 * @description Protected layout for Admin Panel (superusers only)
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 69 - Route Restructure
 * @security Requires is_superuser=true
 */

"use client";

import { Suspense } from "react";
import { AuthProvider } from "@/hooks/useAuth";
import { AuthGuard, AdminGuard } from "@/components/auth/AuthGuard";
import { QueryProvider } from "@/app/providers/QueryProvider";
import { AdminSidebar } from "@/components/admin/AdminSidebar";
import { AdminHeader } from "@/components/admin/AdminHeader";


export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <QueryProvider>
      <AuthProvider>
        <AuthGuard>
          <AdminGuard fallbackPath="/app">
            <div className="flex h-screen bg-gray-50">
              {/* Admin Sidebar */}
              <AdminSidebar />

              {/* Main content area */}
              <div className="flex flex-1 flex-col overflow-hidden">
                {/* Admin Header */}
                <AdminHeader />

                {/* Page content */}
                <main className="flex-1 overflow-y-auto p-6">
                  <Suspense fallback={<AdminLoadingSkeleton />}>
                    {children}
                  </Suspense>
                </main>
              </div>
            </div>
          </AdminGuard>
        </AuthGuard>
      </AuthProvider>
    </QueryProvider>
  );
}

/**
 * Admin page loading skeleton
 */
function AdminLoadingSkeleton() {
  return (
    <div className="space-y-6">
      <div className="h-8 w-48 animate-pulse rounded bg-gray-200" />
      <div className="grid gap-4 md:grid-cols-3">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="h-32 animate-pulse rounded-lg bg-gray-200" />
        ))}
      </div>
      <div className="h-64 animate-pulse rounded-lg bg-gray-200" />
    </div>
  );
}

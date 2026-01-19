/**
 * Web App Layout - SDLC Orchestrator
 *
 * @module frontend/landing/src/app/app/layout
 * @description Protected layout for the main Web App
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 69 - Route Restructure
 * @security Requires authentication (any logged-in user)
 */

"use client";

import { Suspense } from "react";
import { AuthProvider } from "@/hooks/useAuth";
import { AuthGuard } from "@/components/auth/AuthGuard";
import { QueryProvider } from "@/app/providers/QueryProvider";
import { Sidebar } from "@/components/dashboard/Sidebar";
import { Header } from "@/components/dashboard/Header";


export default function AppLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <QueryProvider>
      <AuthProvider>
        <AuthGuard>
          <div className="flex h-screen bg-gray-50">
            {/* Sidebar */}
            <Sidebar />

            {/* Main content area */}
            <div className="flex flex-1 flex-col overflow-hidden">
              {/* Header */}
              <Header />

              {/* Page content */}
              <main className="flex-1 overflow-y-auto p-6">
                <Suspense fallback={<PageLoadingSkeleton />}>
                  {children}
                </Suspense>
              </main>
            </div>
          </div>
        </AuthGuard>
      </AuthProvider>
    </QueryProvider>
  );
}

/**
 * Page loading skeleton
 */
function PageLoadingSkeleton() {
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

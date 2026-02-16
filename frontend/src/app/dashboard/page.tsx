/**
 * Dashboard Redirect Page - SDLC Orchestrator
 *
 * @module frontend/landing/src/app/dashboard/page
 * @description Redirects to /app (main web app)
 * @sdlc SDLC 6.0.6 Universal Framework
 * @status Sprint 69 - Route Restructure
 */

"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { getCurrentUser } from "@/lib/api";

export default function DashboardRedirectPage() {
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        await getCurrentUser();
        // Redirect authenticated users to /app
        router.replace("/app");
      } catch {
        // Not logged in - redirect to login
        router.replace("/login?redirect=/app");
      }
    };
    checkAuth();
  }, [router]);

  // Show loading while redirecting
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="flex flex-col items-center gap-4">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-gray-200 border-t-blue-600" />
        <p className="text-sm text-gray-500">Redirecting...</p>
      </div>
    </div>
  );
}

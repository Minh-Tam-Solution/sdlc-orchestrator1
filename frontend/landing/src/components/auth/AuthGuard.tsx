/**
 * Auth Guard Component - SDLC Orchestrator Dashboard
 *
 * @module frontend/landing/src/components/auth/AuthGuard
 * @description Protects routes requiring authentication
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 61 - Frontend Platform Consolidation
 */

"use client";

import { useEffect } from "react";
import { useRouter, usePathname } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

interface AuthGuardProps {
  children: React.ReactNode;
  fallbackPath?: string;
}

/**
 * Loading skeleton for auth check
 */
function AuthLoadingSkeleton() {
  return (
    <div className="flex h-screen w-full items-center justify-center bg-gray-50">
      <div className="flex flex-col items-center gap-4">
        <div className="h-12 w-12 animate-spin rounded-full border-4 border-gray-200 border-t-blue-600" />
        <p className="text-sm text-gray-500">Đang xác thực...</p>
      </div>
    </div>
  );
}

/**
 * Auth Guard - Redirects to login if not authenticated
 */
export function AuthGuard({ children, fallbackPath = "/login" }: AuthGuardProps) {
  const { isLoading, isAuthenticated } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      // Encode current path for redirect after login
      const redirectUrl = encodeURIComponent(pathname);
      router.push(`${fallbackPath}?redirect=${redirectUrl}`);
    }
  }, [isLoading, isAuthenticated, router, pathname, fallbackPath]);

  // Show loading while checking auth
  if (isLoading) {
    return <AuthLoadingSkeleton />;
  }

  // Don't render children if not authenticated
  if (!isAuthenticated) {
    return <AuthLoadingSkeleton />;
  }

  return <>{children}</>;
}

/**
 * Role Guard - Requires specific roles
 */
interface RoleGuardProps {
  children: React.ReactNode;
  requiredRoles: string[];
  fallbackPath?: string;
}

export function RoleGuard({
  children,
  requiredRoles,
  fallbackPath = "/unauthorized",
}: RoleGuardProps) {
  const { user, isLoading, isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && isAuthenticated && user) {
      const hasRole = requiredRoles.some((role) => user.roles?.includes(role));
      if (!hasRole) {
        router.push(fallbackPath);
      }
    }
  }, [isLoading, isAuthenticated, user, requiredRoles, router, fallbackPath]);

  if (isLoading) {
    return <AuthLoadingSkeleton />;
  }

  if (!isAuthenticated || !user) {
    return null;
  }

  const hasRole = requiredRoles.some((role) => user.roles?.includes(role));
  if (!hasRole) {
    return null;
  }

  return <>{children}</>;
}

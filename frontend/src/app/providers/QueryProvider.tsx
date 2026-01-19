/**
 * TanStack Query Provider - SDLC Orchestrator
 *
 * @module frontend/landing/src/app/providers/QueryProvider
 * @description React Query provider for server state management
 * @sdlc SDLC 5.1.2 Universal Framework
 * @status Sprint 61 - Frontend Platform Consolidation
 */

"use client";

import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

/**
 * Default query client configuration
 * Optimized for dashboard performance
 */
function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        // Data is fresh for 1 minute
        staleTime: 60 * 1000,
        // Keep unused data in cache for 5 minutes
        gcTime: 5 * 60 * 1000,
        // Don't refetch on window focus for better UX
        refetchOnWindowFocus: false,
        // Only retry once on failure
        retry: 1,
        // Retry delay
        retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      },
      mutations: {
        // Retry mutations once
        retry: 1,
      },
    },
  });
}

// Browser query client singleton
let browserQueryClient: QueryClient | undefined = undefined;

function getQueryClient() {
  if (typeof window === "undefined") {
    // Server: always create a new query client
    return makeQueryClient();
  } else {
    // Browser: use singleton pattern
    if (!browserQueryClient) {
      browserQueryClient = makeQueryClient();
    }
    return browserQueryClient;
  }
}

interface QueryProviderProps {
  children: React.ReactNode;
}

/**
 * Query Provider Component
 * Wraps the application with TanStack Query context
 */
export function QueryProvider({ children }: QueryProviderProps) {
  // Use useState to ensure client is created only once per component lifecycle
  const [queryClient] = useState(() => getQueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}

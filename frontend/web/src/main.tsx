/**
 * File: frontend/web/src/main.tsx
 * Version: 1.0.0
 * Status: ACTIVE - STAGE 03 (BUILD)
 * Date: 2025-11-27
 * Authority: Frontend Lead + CTO Approved
 * Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
 *
 * Description:
 * Application entry point for SDLC Orchestrator frontend.
 * Configures React Query, routing, and authentication context.
 */

import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import App from './App'
import './index.css'

/**
 * React Query configuration
 *
 * Performance optimizations:
 * - staleTime: 5 minutes (reduce refetches for stable data)
 * - cacheTime: 10 minutes (keep inactive data cached)
 * - retry: 3 attempts with exponential backoff
 * - refetchOnWindowFocus: false (avoid unnecessary refetches)
 */
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000, // 10 minutes (formerly cacheTime)
      retry: 3,
      refetchOnWindowFocus: false,
      refetchOnMount: true,
      refetchOnReconnect: true,
    },
    mutations: {
      retry: 1,
    },
  },
})

const rootElement = document.getElementById('root')

if (!rootElement) {
  throw new Error('Root element not found. Check your index.html file.')
}

ReactDOM.createRoot(rootElement).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
      {/* React Query Devtools - Only visible in development */}
      <ReactQueryDevtools initialIsOpen={false} buttonPosition="bottom-right" />
    </QueryClientProvider>
  </React.StrictMode>
)

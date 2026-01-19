# File: frontend/landing/Dockerfile
# Version: 1.0.0
# Status: ACTIVE - Sprint 59 (OAuth Integration)
# Date: 2025-12-27
# Authority: DevOps Lead + CTO Approved
# Framework: SDLC 5.1.2 Universal Framework
#
# Description:
# Multi-stage Dockerfile for SDLC Orchestrator landing page.
# Builds Next.js 14 app and serves via standalone mode.

# ==============================================================================
# Stage 1: Dependencies
# ==============================================================================
FROM node:20-alpine AS deps

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* ./

# Install dependencies (use npm install if package-lock.json is missing)
RUN npm install --legacy-peer-deps

# ==============================================================================
# Stage 2: Build
# ==============================================================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependencies from deps stage
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Set environment variables for build
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production

# Build-time argument for API URL (NEXT_PUBLIC_* must be set at build time)
ARG NEXT_PUBLIC_API_URL=http://localhost:8300/api/v1
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

# Build production bundle
RUN npm run build

# ==============================================================================
# Stage 3: Production
# ==============================================================================
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Create non-root user
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built files
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Set ownership
RUN chown -R nextjs:nodejs /app

USER nextjs

EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]

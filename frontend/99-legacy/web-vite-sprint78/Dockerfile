# File: frontend/web/Dockerfile
# Version: 1.0.0
# Status: ACTIVE - STAGE 03 (BUILD)
# Date: 2025-11-27
# Authority: DevOps Lead + CTO Approved
# Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
#
# Description:
# Multi-stage Dockerfile for SDLC Orchestrator frontend application.
# Builds React app with Vite and serves via Nginx for production.

# ==============================================================================
# Stage 1: Build
# ==============================================================================
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci --only=production=false

# Copy source files
COPY . .

# Build production bundle
RUN npm run build

# ==============================================================================
# Stage 2: Production
# ==============================================================================
FROM nginx:1.25-alpine AS production

# Copy custom nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copy built assets from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Add healthcheck (using curl which is available in nginx:alpine)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:80/health || exit 1

# Expose port 80
EXPOSE 80

# Run nginx
CMD ["nginx", "-g", "daemon off;"]

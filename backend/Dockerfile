# File: backend/Dockerfile
# Version: 1.0.0
# Status: ACTIVE - STAGE 03 (BUILD)
# Date: 2025-11-27
# Authority: DevOps Lead + CTO Approved
# Foundation: SDLC 4.9 Complete Lifecycle, Zero Mock Policy
#
# Description:
# Dockerfile for SDLC Orchestrator FastAPI backend.
# Python 3.11 with async support and production dependencies.

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (build tools for C extensions)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    pkg-config \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching (use docker-specific requirements)
COPY requirements-docker.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-docker.txt

# Copy application code
COPY . .

# Create non-root user for security (Semgrep CWE-250)
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

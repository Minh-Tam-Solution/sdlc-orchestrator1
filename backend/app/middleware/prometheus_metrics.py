"""
=========================================================================
Prometheus Metrics Middleware - FastAPI Performance Monitoring (Pure ASGI)
SDLC Orchestrator - Week 5 Day 2 (Performance & Load Testing)

Purpose:
- Expose /metrics endpoint for Prometheus scraping
- Collect API latency (p50, p95, p99)
- Track request rate (requests/second)
- Monitor error rate (4xx, 5xx)
- Measure request/response sizes

Architecture:
- Pure ASGI (NOT BaseHTTPMiddleware) — avoids FastAPI 0.100+ hang bug
  (Starlette BaseHTTPMiddleware event loop conflict on unhandled exceptions;
  see CLAUDE.md Module 1 Debugging section)
- Sprint 213: Converted from BaseHTTPMiddleware to pure ASGI to prevent
  indefinite request hangs when downstream route handlers raise exceptions

Metrics Exposed:
- http_request_duration_seconds (histogram) - API latency
- http_requests_total (counter) - Total requests
- http_requests_in_progress (gauge) - Active requests
- http_request_size_bytes (summary) - Request size
- http_response_size_bytes (summary) - Response size
- http_exceptions_total (counter) - Unhandled exceptions

Performance Targets (SDLC 6.1.1):
- p50 latency: <50ms
- p95 latency: <100ms
- p99 latency: <200ms
- Error rate: <0.1%
- Throughput: >1000 req/s

OWASP ASVS Compliance:
- V11.1.5: Performance monitoring integrated
=========================================================================
"""

import re
import time

from fastapi import Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    REGISTRY,
    Counter,
    Gauge,
    Histogram,
    Summary,
    generate_latest,
)
from starlette.types import ASGIApp, Message, Receive, Scope, Send


# ============================================================================
# PROMETHEUS METRICS DEFINITIONS
# ============================================================================

# Histogram: API latency distribution
http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency (seconds)",
    ["method", "endpoint", "status"],
    buckets=(0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0),
)

# Counter: Total HTTP requests
http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)

# Gauge: Active HTTP requests (in-flight)
http_requests_in_progress = Gauge(
    "http_requests_in_progress",
    "HTTP requests currently in progress",
    ["method", "endpoint"],
)

# Summary: Request size distribution
http_request_size_bytes = Summary(
    "http_request_size_bytes",
    "HTTP request size (bytes)",
    ["method", "endpoint"],
)

# Summary: Response size distribution
http_response_size_bytes = Summary(
    "http_response_size_bytes",
    "HTTP response size (bytes)",
    ["method", "endpoint", "status"],
)

# Counter: Unhandled exceptions
http_exceptions_total = Counter(
    "http_exceptions_total",
    "Total unhandled exceptions",
    ["method", "endpoint", "exception_type"],
)

# Pre-compiled regex for UUID normalization
_UUID_RE = re.compile(
    r"/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    re.IGNORECASE,
)
_NUMERIC_ID_RE = re.compile(r"/\d+")


def _normalize_endpoint(endpoint: str) -> str:
    """
    Normalize endpoint path (replace UUIDs and numeric IDs with {id}).

    Examples:
    - /api/v1/gates/550e8400-e29b-41d4-a716-446655440000 -> /api/v1/gates/{id}
    - /api/v1/evidence/123/download -> /api/v1/evidence/{id}/download
    """
    endpoint = _UUID_RE.sub("/{id}", endpoint)
    endpoint = _NUMERIC_ID_RE.sub("/{id}", endpoint)
    return endpoint


class PrometheusMetricsMiddleware:
    """
    Pure ASGI Prometheus metrics collection middleware for FastAPI.

    Collects request duration, total count, in-progress gauge,
    request/response sizes, and exception counts for all HTTP requests.

    Usage:
        app.add_middleware(PrometheusMetricsMiddleware)

    Exposed Endpoint:
        GET /metrics - Prometheus scrape endpoint
    """

    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        method: str = scope.get("method", "GET")
        path: str = scope.get("path", "")

        # Skip metrics collection for /metrics endpoint itself
        if path == "/metrics":
            await self.app(scope, receive, send)
            return

        endpoint_normalized = _normalize_endpoint(path)

        # Track request size from headers
        headers_dict: dict[bytes, bytes] = dict(scope.get("headers", []))
        raw_content_length = headers_dict.get(b"content-length", b"0")
        try:
            request_size = int(raw_content_length.decode("utf-8", errors="replace"))
        except (ValueError, UnicodeDecodeError):
            request_size = 0

        http_request_size_bytes.labels(
            method=method, endpoint=endpoint_normalized
        ).observe(request_size)

        # Track active requests
        http_requests_in_progress.labels(
            method=method, endpoint=endpoint_normalized
        ).inc()

        start_time = time.time()
        response_status = [0]
        response_content_length = [0]

        async def send_with_metrics(message: Message) -> None:
            if message["type"] == "http.response.start":
                response_status[0] = message.get("status", 0)
                # Extract Content-Length from response headers
                for name, value in message.get("headers", []):
                    if name == b"content-length":
                        try:
                            response_content_length[0] = int(
                                value.decode("utf-8", errors="replace")
                            )
                        except (ValueError, UnicodeDecodeError):
                            pass
                        break
            await send(message)

        try:
            await self.app(scope, receive, send_with_metrics)

            # Record metrics after successful response
            latency = time.time() - start_time
            status_code = response_status[0]

            http_request_duration_seconds.labels(
                method=method, endpoint=endpoint_normalized, status=status_code
            ).observe(latency)

            http_requests_total.labels(
                method=method, endpoint=endpoint_normalized, status=status_code
            ).inc()

            http_response_size_bytes.labels(
                method=method, endpoint=endpoint_normalized, status=status_code
            ).observe(response_content_length[0])

        except Exception as e:
            # Track exceptions
            http_exceptions_total.labels(
                method=method,
                endpoint=endpoint_normalized,
                exception_type=type(e).__name__,
            ).inc()

            # Record latency even on exception
            latency = time.time() - start_time
            http_request_duration_seconds.labels(
                method=method, endpoint=endpoint_normalized, status=500
            ).observe(latency)

            http_requests_total.labels(
                method=method, endpoint=endpoint_normalized, status=500
            ).inc()

            raise
        finally:
            http_requests_in_progress.labels(
                method=method, endpoint=endpoint_normalized
            ).dec()


def metrics_endpoint() -> Response:
    """
    Prometheus /metrics endpoint.

    Returns Prometheus metrics in text format.

    Usage:
        app.add_api_route("/metrics", metrics_endpoint, methods=["GET"])

    Returns:
        Response with Prometheus metrics (text/plain)
    """
    metrics_data = generate_latest(REGISTRY)
    return Response(content=metrics_data, media_type=CONTENT_TYPE_LATEST)


# ============================================================================
# USEFUL PROMETHEUS QUERIES (PromQL)
# ============================================================================

"""
API Latency (p50):
histogram_quantile(0.50, rate(http_request_duration_seconds_bucket[5m]))

API Latency (p95) - CRITICAL:
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

API Latency (p99):
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

Request Rate (requests/second):
rate(http_requests_total[1m])

Error Rate (4xx/5xx):
rate(http_requests_total{status=~"4..|5.."}[1m]) / rate(http_requests_total[1m]) * 100

Active Requests:
http_requests_in_progress

Top 5 Slowest Endpoints (by p95 latency):
topk(5, histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])))
"""

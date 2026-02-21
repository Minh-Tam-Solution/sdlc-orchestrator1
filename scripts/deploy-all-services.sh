#!/bin/bash
# Deploy All Backend Services - SDLC Orchestrator
# No cache, force rebuild, comprehensive health checks

set -e

echo "🚀 SDLC Orchestrator - Deploy All Services"
echo "=========================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: Stop và clean containers cũ
echo "1️⃣ Stopping old containers..."
docker-compose down -v 2>/dev/null || true
echo "✅ Old containers stopped"
echo ""

# Step 2: Rebuild tất cả services (NO CACHE)
echo "2️⃣ Rebuilding all services (no cache)..."
echo "⚠️  This will take 5-10 minutes..."
docker-compose build --no-cache --parallel
echo "✅ All services rebuilt"
echo ""

# Step 3: Start tất cả services
echo "3️⃣ Starting all services..."
docker-compose up -d
echo "⏳ Waiting for services to start (30s)..."
sleep 30
echo ""

# Step 4: Health checks
echo "4️⃣ Health Checks"
echo "================================"
echo ""

# Redis
echo -n "Redis (port 6395): "
if docker-compose exec -T redis redis-cli -a ${REDIS_PASSWORD:-changeme_redis_password} ping 2>/dev/null | grep -q PONG; then
    echo -e "${GREEN}✅ HEALTHY${NC}"
else
    echo -e "${RED}❌ UNHEALTHY${NC}"
fi

# OPA
echo -n "OPA (port 8185): "
if curl -s http://localhost:8185/health 2>/dev/null | grep -q "{}"; then
    echo -e "${GREEN}✅ HEALTHY${NC}"
else
    echo -e "${RED}❌ UNHEALTHY${NC}"
fi

# Prometheus
echo -n "Prometheus (port 9096): "
if curl -s http://localhost:9096/-/healthy 2>/dev/null | grep -q "Prometheus"; then
    echo -e "${GREEN}✅ HEALTHY${NC}"
else
    echo -e "${RED}❌ UNHEALTHY${NC}"
fi

# Grafana
echo -n "Grafana (port 3002): "
if curl -s http://localhost:3002/api/health 2>/dev/null | grep -q "database"; then
    echo -e "${GREEN}✅ HEALTHY${NC}"
else
    echo -e "${RED}❌ UNHEALTHY${NC}"
fi

# Alertmanager
echo -n "Alertmanager (port 9095): "
if curl -s http://localhost:9095/-/healthy 2>/dev/null; then
    echo -e "${GREEN}✅ HEALTHY${NC}"
else
    echo -e "${RED}❌ UNHEALTHY${NC}"
fi

# Backend API (most important)
echo -n "Backend API (port 8300): "
sleep 10  # Extra wait for backend
if curl -s http://localhost:8300/health 2>/dev/null | grep -q "healthy"; then
    echo -e "${GREEN}✅ HEALTHY${NC}"
else
    echo -e "${YELLOW}⏳ STARTING...${NC}"
    echo "Waiting additional 20s for backend..."
    sleep 20
    if curl -s http://localhost:8300/health 2>/dev/null | grep -q "healthy"; then
        echo -e "${GREEN}✅ HEALTHY${NC}"
    else
        echo -e "${RED}❌ UNHEALTHY - Check logs: docker-compose logs backend${NC}"
    fi
fi

# Frontend
echo -n "Frontend (port 8310): "
if curl -s http://localhost:8310 2>/dev/null | grep -q "html"; then
    echo -e "${GREEN}✅ HEALTHY${NC}"
else
    echo -e "${RED}❌ UNHEALTHY${NC}"
fi

echo ""
echo "5️⃣ Service Status"
echo "================================"
docker-compose ps

echo ""
echo "✅ Deployment Complete!"
echo ""
echo "📊 Access Points:"
echo "  - API Docs:    http://localhost:8300/api/docs"
echo "  - Frontend:    http://localhost:8310"
echo "  - Grafana:     http://localhost:3002 (admin/admin_changeme)"
echo "  - Prometheus:  http://localhost:9096"
echo ""
echo "🔍 Logs:"
echo "  - All:     docker-compose logs -f"
echo "  - Backend: docker-compose logs -f backend"
echo ""

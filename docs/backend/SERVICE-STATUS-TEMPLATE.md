# Backend Services Status & Health Check

**Date**: 2026-02-20
**Environment**: Development

---

## 📊 Service Status Table

| Service | Container | Port(s) | Status | Health | URL |
|---------|-----------|---------|--------|--------|-----|
| **Backend API** | sdlc-backend | 8300 | 🔴 | ❌ NOT CHECKED | http://localhost:8300/health |
| **Redis** | sdlc-redis | 6395 | 🔴 | ❌ NOT CHECKED | redis://localhost:6395 |
| **OPA** | sdlc-opa | 8185 | 🔴 | ❌ NOT CHECKED | http://localhost:8185/health |
| **Prometheus** | sdlc-prometheus | 9096 | 🔴 | ❌ NOT CHECKED | http://localhost:9096/-/healthy |
| **Grafana** | sdlc-grafana | 3002 | 🔴 | ❌ NOT CHECKED | http://localhost:3002/api/health |
| **Alertmanager** | sdlc-alertmanager | 9095 | 🔴 | ❌ NOT CHECKED | http://localhost:9095/-/healthy |
| **Frontend** | sdlc-frontend | 8310 | 🔴 | ❌ NOT CHECKED | http://localhost:8310 |
| **PostgreSQL** | postgres-central | 15432 | 🔴 | ❌ EXTERNAL | postgres://localhost:15432 |
| **MinIO** | ai-platform-minio | 9020, 9021 | 🔴 | ❌ EXTERNAL | http://localhost:9020 |

---

## 🔍 Health Check Commands

```bash
# Redis
docker-compose exec redis redis-cli -a PASSWORD ping
# Expected: PONG

# OPA
curl http://localhost:8185/health
# Expected: {}

# Prometheus
curl http://localhost:9096/-/healthy
# Expected: Prometheus is Healthy.

# Grafana
curl http://localhost:3002/api/health
# Expected: {"database":"ok","version":"10.2.0"}

# Alertmanager
curl http://localhost:9095/-/healthy
# Expected: 200 OK

# Backend API
curl http://localhost:8300/health
# Expected: {"status":"healthy","version":"1.2.0"}

# Frontend
curl -I http://localhost:8310
# Expected: 200 OK

# PostgreSQL (external)
docker exec -it postgres-central pg_isready -U sdlc_user
# Expected: accepting connections

# MinIO (external)
curl http://ai-platform-minio:9000/minio/health/live
# Expected: 200 OK (from within docker network)
```

---

## 🚀 Deployment Commands

### Full Deployment (NO CACHE)
```bash
bash scripts/deploy-all-services.sh
```

### Individual Service Rebuild
```bash
# Backend only
docker-compose stop backend
docker-compose rm -f backend
docker-compose build --no-cache backend
docker-compose up -d backend

# Frontend only
docker-compose stop frontend
docker-compose rm -f frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

---

## 📝 Post-Deployment Checklist

- [ ] All containers running: `docker-compose ps`
- [ ] Backend health: `curl http://localhost:8300/health`
- [ ] API docs accessible: http://localhost:8300/api/docs
- [ ] Redis connected: `docker-compose exec redis redis-cli ping`
- [ ] OPA healthy: `curl http://localhost:8185/health`
- [ ] Database migrations run: `cd backend && alembic upgrade head`
- [ ] Swagger shows 91 endpoints
- [ ] CORS configured: Check `ALLOWED_ORIGINS` in `.env`
- [ ] Logs clean: `docker-compose logs backend | grep ERROR`

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to Docker daemon"
```bash
# Start Docker Desktop
# macOS: Cmd+Space → "Docker" → Enter
# Wait for Docker icon in menu bar
docker ps  # Verify working
```

### Issue: "Backend unhealthy after 60s"
```bash
# Check logs
docker-compose logs backend | tail -100

# Common causes:
# 1. Database not created
# 2. Redis connection failed
# 3. OPA unavailable
# 4. Environment variables missing
```

### Issue: "Port already in use"
```bash
# Find process using port
lsof -i :8300  # Replace with your port

# Kill process
kill -9 <PID>

# Or use different port in docker-compose.yml
```

---

**Last Updated**: 2026-02-20
**Status**: Template - Run deployment to populate actual status

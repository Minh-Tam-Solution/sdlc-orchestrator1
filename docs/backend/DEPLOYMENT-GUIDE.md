# Hướng Dẫn Triển Khai Backend - SDLC Orchestrator

**Version**: 1.0.0
**Date**: 2026-02-18
**Status**: ACTIVE

## 📋 Tổng Quan

Backend SDLC Orchestrator là một FastAPI application với:
- **Framework**: Python 3.11+ với FastAPI 0.115.6
- **Database**: PostgreSQL 15.5 (postgres-central:15432)
- **Cache**: Redis 7.2 (port 6395)
- **Storage**: MinIO S3-compatible (ai-platform-minio:9000)
- **Policy Engine**: OPA 0.58.0 (port 8185)
- **Monitoring**: Prometheus + Grafana + Alertmanager

---

## 🚀 Triển Khai Nhanh (Quick Start)

### 1. Yêu Cầu Hệ Thống

```bash
# Software requirements
- Docker 20.10+
- Docker Compose 2.0+
- Python 3.11+
- PostgreSQL 15.5 (external - postgres-central)
- Git

# Disk space
- Minimum: 10GB
- Recommended: 20GB
```

### 2. Clone Repository

```bash
# Clone với submodules
git clone --recurse-submodules https://github.com/Minh-Tam-Solution/SDLC-Orchestrator
cd SDLC-Orchestrator
```

### 3. Cấu Hình Environment

```bash
# Copy file .env mẫu
cp .env.example .env

# Chỉnh sửa các biến môi trường quan trọng
nano .env
```

**Các biến môi trường QUAN TRỌNG:**

```bash
# Database (sử dụng postgres-central external)
DATABASE_URL=postgresql+asyncpg://sdlc_user:YOUR_PASSWORD@postgres-central:5432/sdlc_orchestrator
POSTGRES_PASSWORD=YOUR_SECURE_PASSWORD

# JWT Secret (PHẢI thay đổi trong production)
SECRET_KEY=YOUR_SUPER_SECRET_KEY_MINIMUM_32_CHARACTERS_LONG
JWT_SECRET_KEY=YOUR_SUPER_SECRET_KEY_MINIMUM_32_CHARACTERS_LONG

# MinIO (sử dụng ai-platform-minio external)
MINIO_ENDPOINT=ai-platform-minio:9000
MINIO_PUBLIC_URL=http://sdlc.nhatquangholding.com:9020
MINIO_ACCESS_KEY=YOUR_MINIO_ACCESS_KEY
MINIO_SECRET_KEY=YOUR_MINIO_SECRET_KEY
MINIO_BUCKET=evidence-vault-v2

# Redis
REDIS_PASSWORD=YOUR_REDIS_PASSWORD

# CORS - Danh sách origins được phép
ALLOWED_ORIGINS=https://sdlc.nhatquangholding.com,http://localhost:8310,http://localhost:3000

# OAuth (Optional - cho GitHub, Google login)
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# SMTP Email (Optional - cho password reset)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

### 4. Khởi Động Dịch Vụ (Development)

```bash
# Build và khởi động KHÔNG CACHE (QUAN TRỌNG!)
docker-compose up --build --force-recreate --no-cache -d

# Hoặc sử dụng Makefile (nhanh hơn)
make clean      # Xóa container và cache cũ
make up         # Khởi động services
```

### 5. Kiểm Tra Database

```bash
# QUAN TRỌNG: Tạo database trong postgres-central (external)
docker exec -it postgres-central psql -U postgres

# Trong PostgreSQL console:
CREATE DATABASE sdlc_orchestrator;
CREATE USER sdlc_user WITH PASSWORD 'YOUR_PASSWORD';
GRANT ALL PRIVILEGES ON DATABASE sdlc_orchestrator TO sdlc_user;
\q
```

### 6. Chạy Database Migrations

```bash
# Chạy migrations
make migrate

# HOẶC thủ công:
cd backend
alembic upgrade head
```

### 7. Seed Data (Optional)

```bash
# Seed dữ liệu test
make seed

# HOẶC thủ công:
cd backend
python scripts/seed_data.py
```

### 8. Kiểm Tra Health

```bash
# Kiểm tra tất cả services
make health

# HOẶC kiểm tra từng service:
curl http://localhost:8300/health              # Backend API
curl http://localhost:8185/health              # OPA
curl http://localhost:6395                     # Redis (AUTH required)
curl http://localhost:9096/-/healthy           # Prometheus
curl http://localhost:3002/api/health          # Grafana
```

---

## 🔧 Triển Khai Production

### 1. Build Production Images (NO CACHE!)

```bash
# Build backend image KHÔNG CACHE
docker build --no-cache \
  -t sdlc-orchestrator-backend:latest \
  -f backend/Dockerfile \
  backend/

# Verify image
docker images | grep sdlc-orchestrator-backend
```

### 2. Sử Dụng Docker Compose Production

```bash
# File: docker-compose.production.yml
docker-compose -f docker-compose.production.yml up -d --build --force-recreate --no-cache

# Kiểm tra logs
docker-compose -f docker-compose.production.yml logs -f backend
```

### 3. Environment Variables Production

```bash
# File: .env.production (KHÔNG commit vào git!)

# Database
DATABASE_URL=postgresql+asyncpg://sdlc_user:SECURE_PASSWORD@postgres-central:5432/sdlc_orchestrator

# Security
SECRET_KEY=PRODUCTION_SECRET_KEY_64_CHARACTERS_OR_MORE
JWT_SECRET_KEY=PRODUCTION_SECRET_KEY_64_CHARACTERS_OR_MORE
ENVIRONMENT=production
DEBUG=false

# CORS - CHỈ domain production
ALLOWED_ORIGINS=https://sdlc.nhatquangholding.com

# Cookie security
COOKIE_DOMAIN=.nhatquangholding.com
COOKIE_SECURE=true
COOKIE_SAMESITE=lax
```

---

## 🛡️ Bảo Mật & Best Practices

### 1. CORS Configuration

```python
# backend/app/main.py (lines 246-252)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,  # ❌ KHÔNG dùng ["*"]
    allow_credentials=True,  # ✅ Cho cookie-based auth
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)
```

**Lưu ý:**
- ❌ **KHÔNG bao giờ** dùng `allow_origins=["*"]` với `allow_credentials=True`
- ✅ Luôn liệt kê EXPLICIT các origins được phép
- ✅ Production chỉ cho phép domain chính thức

### 2. Docker Cache Issues - GIẢI PHÁP

**VẤN ĐỀ:** Docker cache layers cũ → code mới không được deploy

**GIẢI PHÁP 1: Rebuild với --no-cache**

```bash
# Backend
docker-compose build --no-cache backend
docker-compose up -d backend

# Frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

**GIẢI PHÁP 2: Force recreate containers**

```bash
# Xóa container + volume + cache
docker-compose down -v
docker system prune -af  # ⚠️ Cẩn thận! Xóa TẤT CẢ unused images

# Rebuild từ đầu
docker-compose up --build --force-recreate --no-cache -d
```

**GIẢI PHÁP 3: Update Makefile (KHUYẾN NGHỊ)**

Thêm vào `Makefile`:

```makefile
rebuild:
	@echo "🔄 Rebuilding all services (no cache)..."
	docker-compose down -v
	docker-compose build --no-cache
	docker-compose up -d --force-recreate
	@echo "✅ Rebuild complete"

rebuild-backend:
	@echo "🔄 Rebuilding backend (no cache)..."
	docker-compose stop backend
	docker-compose rm -f backend
	docker-compose build --no-cache backend
	docker-compose up -d backend
	@echo "✅ Backend rebuilt"

rebuild-frontend:
	@echo "🔄 Rebuilding frontend (no cache)..."
	docker-compose stop frontend
	docker-compose rm -f frontend
	docker-compose build --no-cache frontend
	docker-compose up -d frontend
	@echo "✅ Frontend rebuilt"
```

Sử dụng:

```bash
make rebuild          # Rebuild tất cả
make rebuild-backend  # Chỉ rebuild backend
make rebuild-frontend # Chỉ rebuild frontend
```

### 3. Database Reset (Development)

```bash
# Reset TOÀN BỘ database (XÓA DATA!)
make db-reset

# HOẶC thủ công:
docker-compose exec postgres psql -U sdlc_user -d sdlc_orchestrator \
  -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
make migrate
make seed
```

### 4. Non-root User (Security)

Dockerfile đã cấu hình non-root user:

```dockerfile
# backend/Dockerfile (lines 36-39)
RUN groupadd -r appuser && useradd -r -g appuser appuser \
    && chown -R appuser:appuser /app
USER appuser
```

✅ **Tuân thủ CWE-250 (Semgrep security rule)**

---

## 📊 Monitoring & Logging

### 1. Xem Logs

```bash
# Tất cả services
docker-compose logs -f

# Chỉ backend
docker-compose logs -f backend

# Chỉ 100 dòng cuối
docker-compose logs --tail=100 backend

# Theo thời gian thực
docker-compose logs -f --tail=50 backend
```

### 2. Prometheus Metrics

```bash
# API endpoint metrics
curl http://localhost:9096/metrics

# Backend internal metrics
curl http://localhost:8300/metrics
```

### 3. Grafana Dashboards

```bash
# Access Grafana
http://localhost:3002

# Default credentials:
Username: admin
Password: admin_changeme (từ .env)
```

---

## 🧪 Testing & Quality

### 1. Run Tests

```bash
# Tất cả tests
make test-backend

# Chỉ unit tests
cd backend
pytest tests/unit/ -v

# Chỉ integration tests
pytest tests/integration/ -v

# E2E tests
pytest tests/e2e/ -v

# Với coverage
pytest tests/ -v --cov=app --cov-report=html
```

### 2. Code Quality

```bash
# Linting
make lint-backend

# Format code
make format

# Type checking
cd backend
mypy app/
```

### 3. Security Scan (Semgrep)

```bash
# SAST scanning
cd backend
semgrep --config=p/owasp-top-ten app/
semgrep --config=p/security-audit app/
```

---

## 🔍 Debugging

### 1. Shell Access

```bash
# Backend container shell
docker-compose exec backend bash

# PostgreSQL shell
docker-compose exec postgres psql -U sdlc_user -d sdlc_orchestrator

# Redis shell
docker-compose exec redis redis-cli -a YOUR_REDIS_PASSWORD

# OPA shell
docker-compose exec opa sh
```

### 2. Common Issues & Solutions

#### Issue 1: "Database connection failed"

```bash
# Kiểm tra PostgreSQL
docker ps | grep postgres-central

# Kiểm tra DATABASE_URL trong .env
grep DATABASE_URL .env

# Test connection thủ công
docker exec -it postgres-central psql -U postgres -c "\l"
```

#### Issue 2: "MinIO initialization failed"

```bash
# Kiểm tra MinIO container
docker ps | grep ai-platform-minio

# Kiểm tra network
docker network ls | grep ai-net

# Test connection
curl http://ai-platform-minio:9000/minio/health/live
```

#### Issue 3: "OPA connection failed"

```bash
# Kiểm tra OPA
docker-compose ps opa

# Test OPA health
curl http://localhost:8185/health

# Kiểm tra policies
docker-compose exec opa opa test /policies -v
```

#### Issue 4: "Redis connection failed"

```bash
# Kiểm tra Redis
docker-compose ps redis

# Test connection
docker-compose exec redis redis-cli -a YOUR_REDIS_PASSWORD ping
# Expected: PONG
```

#### Issue 5: "CORS errors in browser"

```bash
# Kiểm tra ALLOWED_ORIGINS
grep ALLOWED_ORIGINS .env

# Restart backend sau khi thay đổi
docker-compose restart backend

# Verify CORS headers
curl -i -X OPTIONS http://localhost:8300/api/v1/gates \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET"
```

---

## 📁 Cấu Trúc Backend

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── api/
│   │   └── routes/             # API route handlers (91 endpoints)
│   ├── core/
│   │   ├── config.py           # Settings & environment config
│   │   ├── security.py         # JWT, OAuth, MFA
│   │   └── dependencies.py     # FastAPI dependencies
│   ├── db/
│   │   ├── base.py             # SQLAlchemy base
│   │   └── session.py          # Database session
│   ├── models/                 # SQLAlchemy models (33 tables)
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic (99 services)
│   │   ├── gate_service.py
│   │   ├── evidence_manifest_service.py
│   │   ├── opa_service.py
│   │   ├── minio_service.py
│   │   ├── ollama_service.py
│   │   └── ...
│   ├── middleware/             # Custom middleware
│   │   ├── prometheus_metrics.py
│   │   ├── rate_limiter.py
│   │   ├── security_headers.py
│   │   └── cache_headers.py
│   └── utils/                  # Helper utilities
├── alembic/                    # Database migrations
├── tests/                      # Test suite
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── Dockerfile                  # Production Dockerfile
├── requirements.txt            # Python dependencies (398 packages)
└── requirements-docker.txt     # Docker-optimized dependencies
```

---

## 🎯 API Endpoints

### Core Endpoints (64 endpoints)

```bash
# Authentication (7 endpoints)
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
POST   /api/v1/auth/logout
GET    /api/v1/auth/me
POST   /api/v1/auth/github/callback
POST   /api/v1/auth/google/callback

# Gates (12 endpoints)
GET    /api/v1/gates
POST   /api/v1/gates
GET    /api/v1/gates/{id}
PUT    /api/v1/gates/{id}
DELETE /api/v1/gates/{id}
POST   /api/v1/gates/{id}/evaluate
POST   /api/v1/gates/{id}/submit
POST   /api/v1/gates/{id}/approve
POST   /api/v1/gates/{id}/reject
GET    /api/v1/gates/{id}/policy-result
POST   /api/v1/gates/{id}/override
GET    /api/v1/gates/{id}/evidence

# Evidence (8 endpoints)
GET    /api/v1/evidence
POST   /api/v1/evidence/upload
GET    /api/v1/evidence/{id}
DELETE /api/v1/evidence/{id}
GET    /api/v1/evidence/{id}/download
GET    /api/v1/evidence/{id}/verify
POST   /api/v1/evidence/{id}/lock
GET    /api/v1/evidence/manifest

# ... (91 endpoints total, see API-Specification.md)
```

### Multi-Agent Team Engine (11 endpoints - Sprint 176)

```bash
POST   /api/v1/agent-team/definitions
GET    /api/v1/agent-team/definitions
GET    /api/v1/agent-team/definitions/{id}
PUT    /api/v1/agent-team/definitions/{id}
DELETE /api/v1/agent-team/definitions/{id}
POST   /api/v1/agent-team/conversations
GET    /api/v1/agent-team/conversations/{id}
POST   /api/v1/agent-team/conversations/{id}/messages
POST   /api/v1/agent-team/conversations/{id}/interrupt
GET    /api/v1/agent-team/messages/{id}
POST   /api/v1/agent-team/messages/{id}/retry
```

---

## 📖 Tài Liệu Tham Khảo

- **API Documentation**: http://localhost:8300/api/docs (Swagger UI)
- **API Specification**: `docs/01-planning/05-API-Design/API-Specification.md`
- **Data Model**: `docs/01-planning/04-Data-Model/Data-Model-ERD.md`
- **Architecture**: `docs/02-design/02-System-Architecture/System-Architecture-Document.md`
- **ADRs**: `docs/02-design/03-ADRs/`
- **CLAUDE.md**: Project context for AI assistants

---

## ✅ Checklist Triển Khai

### Pre-deployment

- [ ] File `.env` đã cấu hình đầy đủ
- [ ] Database `sdlc_orchestrator` đã tạo trong postgres-central
- [ ] Secrets đã thay đổi (SECRET_KEY, POSTGRES_PASSWORD, REDIS_PASSWORD)
- [ ] CORS ALLOWED_ORIGINS chỉ chứa domains được phép

### Deployment

- [ ] Build images với `--no-cache`
- [ ] Migrations đã chạy thành công (`make migrate`)
- [ ] Health checks tất cả services PASS
- [ ] Logs không có ERROR critical

### Post-deployment

- [ ] API docs accessible: http://localhost:8300/api/docs
- [ ] Swagger UI hiển thị 91 endpoints
- [ ] Test login flow (JWT + OAuth)
- [ ] Test upload evidence (MinIO)
- [ ] Test gate evaluation (OPA)
- [ ] Prometheus metrics collecting
- [ ] Grafana dashboards hiển thị data

---

**Last Updated**: 2026-02-18
**Maintainer**: Backend Team + DevOps Lead
**Status**: ✅ ACTIVE - Production Ready (Gate G3 APPROVED - 98.2%)

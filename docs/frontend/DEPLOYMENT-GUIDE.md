# Hướng Dẫn Triển Khai Frontend - SDLC Orchestrator

**Version**: 1.0.0
**Date**: 2026-02-18
**Status**: ACTIVE

## 📋 Tổng Quan

Frontend SDLC Orchestrator là một Next.js application với:
- **Framework**: Next.js 14.2.35 (App Router)
- **React**: React 18
- **UI Library**: shadcn/ui (Radix UI + Tailwind CSS 3.4.1)
- **State Management**: Zustand (lightweight)
- **Data Fetching**: TanStack Query v5
- **Testing**: Vitest (unit) + Playwright (E2E)
- **Port**: 8310 (production), 3000 (dev)

---

## 🚀 Triển Khai Nhanh (Quick Start)

### 1. Yêu Cầu Hệ Thống

```bash
# Software requirements
- Node.js 20+ (LTS)
- npm 10+
- Docker 20.10+ (cho production)
- Git

# Disk space
- Minimum: 5GB
- Recommended: 10GB
```

### 2. Clone Repository

```bash
# Clone với submodules
git clone --recurse-submodules https://github.com/Minh-Tam-Solution/SDLC-Orchestrator
cd SDLC-Orchestrator/frontend
```

### 3. Install Dependencies

```bash
# Cài đặt packages
npm install --legacy-peer-deps

# Hoặc sử dụng Makefile
cd ..
make install-frontend
```

### 4. Cấu Hình Environment

```bash
# Copy file .env mẫu
cp .env.example .env.local

# Chỉnh sửa các biến môi trường
nano .env.local
```

**File `.env.local` (Development):**

```bash
# API Backend URL
NEXT_PUBLIC_API_URL=http://localhost:8300/api/v1

# App Environment
NODE_ENV=development

# Optional: Analytics, monitoring
NEXT_PUBLIC_ANALYTICS_ID=
```

**File `.env.production` (Production):**

```bash
# API Backend URL (PRODUCTION)
NEXT_PUBLIC_API_URL=https://sdlc.nhatquangholding.com/api/v1

# App Environment
NODE_ENV=production

# Optional
NEXT_PUBLIC_ANALYTICS_ID=your_analytics_id
```

### 5. Development Server

```bash
# Start dev server (port 3000)
npm run dev

# HOẶC từ root:
cd ..
make dev-frontend

# Access app
http://localhost:3000
```

### 6. Production Build

```bash
# Build production bundle
npm run build

# Test production build locally
npm run start

# Access app
http://localhost:3000
```

---

## 🐳 Docker Deployment

### 1. Build Docker Image (NO CACHE!)

```bash
# Build từ root directory
docker build --no-cache \
  -t sdlc-orchestrator-frontend:latest \
  --build-arg NEXT_PUBLIC_API_URL=https://sdlc.nhatquangholding.com/api/v1 \
  -f frontend/Dockerfile \
  frontend/

# Verify image
docker images | grep sdlc-orchestrator-frontend
```

### 2. Run Container

```bash
# Run standalone (development)
docker run -d \
  --name sdlc-frontend \
  -p 8310:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8300/api/v1 \
  sdlc-orchestrator-frontend:latest

# Access
http://localhost:8310
```

### 3. Docker Compose (Recommended)

```bash
# Từ root directory
# Build và khởi động KHÔNG CACHE
docker-compose up --build --force-recreate --no-cache -d frontend

# Xem logs
docker-compose logs -f frontend

# Restart khi có thay đổi code
docker-compose restart frontend
```

### 4. Production với Docker Compose

```bash
# File: docker-compose.production.yml
docker-compose -f docker-compose.production.yml up -d --build --force-recreate --no-cache

# Kiểm tra status
docker-compose -f docker-compose.production.yml ps

# Logs
docker-compose -f docker-compose.production.yml logs -f frontend
```

---

## 🛡️ Bảo Mật & Best Practices

### 1. Environment Variables

**QUAN TRỌNG:**
- ✅ Biến `NEXT_PUBLIC_*` được expose ra client (browser)
- ✅ Biến không có prefix `NEXT_PUBLIC_` CHỈ dùng server-side
- ❌ KHÔNG bao giờ lưu secrets trong `NEXT_PUBLIC_*`

```bash
# ✅ ĐÚNG - API URL công khai
NEXT_PUBLIC_API_URL=https://sdlc.nhatquangholding.com/api/v1

# ❌ SAI - Secret key không được expose
NEXT_PUBLIC_SECRET_KEY=my_secret_key  # ← NGUY HIỂM!

# ✅ ĐÚNG - Server-side only
SECRET_KEY=my_secret_key  # ← An toàn (không build vào client)
```

### 2. Docker Cache Issues - GIẢI PHÁP

**VẤN ĐỀ:** Docker cache layers cũ → code mới không được deploy

**GIẢI PHÁP 1: Rebuild với --no-cache**

```bash
# Frontend only
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

**GIẢI PHÁP 2: Force recreate + Prune**

```bash
# Xóa container cũ
docker-compose stop frontend
docker-compose rm -f frontend

# Xóa images cũ (optional - cẩn thận!)
docker rmi sdlc-orchestrator-frontend:latest

# Rebuild từ đầu
docker-compose up --build --force-recreate --no-cache -d frontend
```

**GIẢI PHÁP 3: Update Makefile (KHUYẾN NGHỊ)**

Thêm vào `Makefile` (ở root):

```makefile
rebuild-frontend:
	@echo "🔄 Rebuilding frontend (no cache)..."
	docker-compose stop frontend
	docker-compose rm -f frontend
	docker-compose build --no-cache frontend
	docker-compose up -d frontend
	@echo "✅ Frontend rebuilt"

clean-frontend:
	@echo "🧹 Cleaning frontend artifacts..."
	cd frontend && rm -rf .next node_modules dist
	docker-compose down frontend
	docker rmi sdlc-orchestrator-frontend:latest || true
	@echo "✅ Frontend cleaned"
```

Sử dụng:

```bash
make rebuild-frontend  # Rebuild frontend (no cache)
make clean-frontend    # Xóa toàn bộ artifacts + image
```

### 3. Next.js Build Optimization

**Multi-Stage Dockerfile** (đã tối ưu):

```dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --legacy-peer-deps

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=production
ARG NEXT_PUBLIC_API_URL=http://localhost:8300/api/v1
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
RUN npm run build

# Stage 3: Production Runner
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
RUN chown -R nextjs:nodejs /app
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

**Lợi ích:**
- ✅ Giảm image size (chỉ copy production files)
- ✅ Non-root user (security best practice)
- ✅ Layer caching hiệu quả (dependencies riêng biệt)
- ✅ Standalone output (không cần node_modules trong runtime)

### 4. CORS & API Integration

Frontend gọi API backend qua `NEXT_PUBLIC_API_URL`. Backend đã cấu hình CORS:

```typescript
// frontend/src/lib/api-client.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8300/api/v1';

const apiClient = {
  get: async (endpoint: string) => {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: 'GET',
      credentials: 'include',  // ✅ Gửi cookies (JWT)
      headers: {
        'Content-Type': 'application/json',
      },
    });
    return response.json();
  },
  // ... post, put, delete
};
```

**Lưu ý:**
- ✅ `credentials: 'include'` để gửi cookies (JWT tokens)
- ✅ Backend CORS đã cấu hình `allow_credentials=True`
- ✅ `ALLOWED_ORIGINS` trong backend `.env` phải chứa frontend domain

---

## 📊 Monitoring & Logging

### 1. Xem Logs

```bash
# Development server logs
npm run dev  # Logs hiển thị trực tiếp trong terminal

# Docker container logs
docker-compose logs -f frontend

# Chỉ 100 dòng cuối
docker-compose logs --tail=100 frontend
```

### 2. Browser Console

```bash
# Development: Source maps enabled → dễ debug
# Production: Source maps disabled → bảo mật

# Kiểm tra API calls
- Open DevTools (F12)
- Network tab → Filter "Fetch/XHR"
- Xem request/response headers
```

### 3. Performance Monitoring

```bash
# Lighthouse audit (Chrome DevTools)
1. Open DevTools (F12)
2. Lighthouse tab
3. Generate report
4. Target: Score >90 (Desktop), >85 (Mobile)

# Next.js built-in analytics
npm run build
# Xem "First Load JS" sizes
# Target: <100KB for main bundle
```

---

## 🧪 Testing & Quality

### 1. Unit Tests (Vitest)

```bash
# Run all unit tests
npm run test

# Watch mode (development)
npm run test:watch

# Coverage report
npm run test:coverage
```

### 2. E2E Tests (Playwright)

```bash
# Install Playwright browsers (first time only)
npx playwright install

# Run E2E tests
npm run test:e2e

# Run with UI (debug mode)
npm run test:e2e:ui

# Run headed (see browser)
npm run test:e2e:headed
```

### 3. Linting & Formatting

```bash
# Lint code
npm run lint

# HOẶC từ root:
make lint-frontend
```

---

## 🔍 Debugging

### 1. Common Issues & Solutions

#### Issue 1: "API calls failing (CORS error)"

```bash
# Kiểm tra NEXT_PUBLIC_API_URL
echo $NEXT_PUBLIC_API_URL
# Expected: http://localhost:8300/api/v1 (dev)
#       OR: https://sdlc.nhatquangholding.com/api/v1 (prod)

# Kiểm tra backend ALLOWED_ORIGINS
cd ../backend
grep ALLOWED_ORIGINS .env
# Phải chứa: http://localhost:3000 (dev) hoặc frontend domain (prod)

# Test API trực tiếp
curl -i http://localhost:8300/api/v1/health

# Restart backend
docker-compose restart backend
```

#### Issue 2: "Environment variables not updating"

```bash
# Rebuild frontend (Next.js caches env vars at build time)
rm -rf .next
npm run build

# Hoặc với Docker:
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

#### Issue 3: "Build errors - Module not found"

```bash
# Clear cache + reinstall
rm -rf node_modules package-lock.json .next
npm install --legacy-peer-deps
npm run build
```

#### Issue 4: "Docker container không khởi động"

```bash
# Kiểm tra logs
docker-compose logs frontend

# Kiểm tra port conflict
lsof -i :8310  # Port đã được dùng?
lsof -i :3000

# Xóa container cũ
docker-compose down
docker-compose up -d frontend
```

#### Issue 5: "Styles không load (Tailwind)"

```bash
# Kiểm tra tailwind.config.ts - content paths
cat tailwind.config.ts
# Phải include: "./src/**/*.{js,ts,jsx,tsx,mdx}"

# Rebuild
npm run build
```

---

## 📁 Cấu Trúc Frontend

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── page.tsx            # Homepage (/)
│   │   ├── layout.tsx          # Root layout
│   │   ├── login/              # Login page
│   │   ├── app/                # Main app pages
│   │   │   ├── gates/          # Gates management
│   │   │   ├── evidence/       # Evidence vault
│   │   │   ├── codegen/        # Code generation
│   │   │   ├── compliance/     # Compliance framework
│   │   │   ├── planning/       # Planning hierarchy
│   │   │   ├── ceo-dashboard/  # Executive dashboard
│   │   │   └── ...
│   │   └── admin/              # Admin panel
│   ├── components/             # Reusable components
│   │   ├── ui/                 # shadcn/ui base components
│   │   ├── codegen/            # Code generation UI
│   │   ├── dashboard/          # Dashboard components
│   │   ├── governance/         # Governance controls
│   │   └── auth/               # Auth flow components
│   ├── lib/                    # Utilities & helpers
│   │   ├── api-client.ts       # API client wrapper
│   │   ├── utils.ts            # Common utilities
│   │   └── stores/             # Zustand stores
│   └── styles/                 # Global styles
│       └── globals.css         # Tailwind imports
├── public/                     # Static assets
│   ├── logo.svg
│   └── ...
├── e2e/                        # Playwright E2E tests
├── Dockerfile                  # Multi-stage production build
├── package.json                # Dependencies
├── next.config.mjs             # Next.js configuration
├── tailwind.config.ts          # Tailwind CSS config
├── tsconfig.json               # TypeScript config
└── vitest.config.ts            # Vitest test config
```

---

## 🎯 Key Pages & Routes

### Public Routes

```bash
/                       # Landing page
/login                  # Login page (JWT + OAuth)
/auth/callback          # OAuth callback
/auth/github/callback   # GitHub OAuth
/docs                   # Documentation
```

### Protected Routes (Require Authentication)

```bash
# Gates Management
/app/gates              # List all gates
/app/gates/new          # Create new gate
/app/gates/[id]         # Gate detail

# Evidence Vault
/app/evidence           # Evidence list
/app/evidence/upload    # Upload evidence
/app/evidence/[id]      # Evidence detail

# Code Generation (EP-06)
/app/codegen            # Codegen interface
/app/codegen/sessions/[id]  # Session detail

# Planning Hierarchy
/app/planning/roadmap   # Roadmap view
/app/planning/phases    # Phases view
/app/planning/sprints   # Sprints view
/app/planning/backlog   # Backlog view

# Executive Dashboard
/app/ceo-dashboard      # CEO metrics & insights

# Compliance
/app/compliance         # Compliance frameworks

# Admin
/admin/users            # User management
/admin/policies         # Policy management
/admin/settings         # System settings
```

---

## 🚦 Performance Budget

Next.js production build targets:

```bash
# Bundle Sizes
Main bundle:     < 100 KB (gzip)
Route chunks:    < 50 KB each (gzip)
Total JS:        < 300 KB (First Load)

# Loading Performance
TTI:             < 3s (Time to Interactive)
FCP:             < 1s (First Contentful Paint)
LCP:             < 2.5s (Largest Contentful Paint)

# Lighthouse Scores
Desktop:         > 90
Mobile:          > 85
Accessibility:   100
SEO:             > 90
```

**Kiểm tra:**

```bash
# Build và xem bundle analyzer
npm run build
# Output hiển thị sizes

# Lighthouse audit
npx lighthouse http://localhost:8310 --view
```

---

## 📖 Tài Liệu Tham Khảo

- **Next.js Docs**: https://nextjs.org/docs
- **shadcn/ui**: https://ui.shadcn.com
- **TanStack Query**: https://tanstack.com/query/latest
- **Playwright**: https://playwright.dev
- **Vitest**: https://vitest.dev

**Project-specific:**
- **API Spec**: `../docs/01-planning/05-API-Design/API-Specification.md`
- **UI/UX Guidelines**: `../docs/02-design/06-UI-UX-Design/`
- **Architecture**: `../docs/02-design/02-System-Architecture/System-Architecture-Document.md`

---

## ✅ Checklist Triển Khai

### Pre-deployment

- [ ] File `.env.production` đã cấu hình
- [ ] `NEXT_PUBLIC_API_URL` trỏ đến backend production
- [ ] Dependencies đã install (`npm install --legacy-peer-deps`)
- [ ] Build thành công (`npm run build`)
- [ ] Lighthouse score >85 (mobile), >90 (desktop)

### Deployment

- [ ] Build Docker image với `--no-cache`
- [ ] Container khởi động thành công
- [ ] Health check PASS (port 8310 accessible)
- [ ] Logs không có ERROR

### Post-deployment

- [ ] Homepage accessible: https://sdlc.nhatquangholding.com
- [ ] Login flow hoạt động (JWT + OAuth)
- [ ] API calls thành công (check Network tab)
- [ ] CORS không có lỗi
- [ ] Styles load đúng (Tailwind)
- [ ] Images load nhanh (<1s)
- [ ] Mobile responsive (test trên mobile device)

---

## 🔄 CI/CD Pipeline (Khuyến nghị)

### GitHub Actions Workflow

```yaml
# .github/workflows/frontend-deploy.yml
name: Frontend Deploy

on:
  push:
    branches: [main]
    paths:
      - 'frontend/**'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        working-directory: ./frontend
        run: npm install --legacy-peer-deps

      - name: Run tests
        working-directory: ./frontend
        run: |
          npm run test
          npm run lint

      - name: Build
        working-directory: ./frontend
        env:
          NEXT_PUBLIC_API_URL: https://sdlc.nhatquangholding.com/api/v1
        run: npm run build

      - name: Build Docker image
        run: |
          docker build --no-cache \
            -t sdlc-frontend:${{ github.sha }} \
            --build-arg NEXT_PUBLIC_API_URL=https://sdlc.nhatquangholding.com/api/v1 \
            -f frontend/Dockerfile \
            frontend/

      - name: Push to registry
        run: |
          docker push sdlc-frontend:${{ github.sha }}

      - name: Deploy to production
        run: |
          # Deploy commands here
```

---

**Last Updated**: 2026-02-18
**Maintainer**: Frontend Team + DevOps Lead
**Status**: ✅ ACTIVE - Production Ready (Gate G3 APPROVED - 98.2%)

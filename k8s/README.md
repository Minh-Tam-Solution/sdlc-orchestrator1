# SDLC Orchestrator - Kubernetes Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying SDLC Orchestrator to Kubernetes clusters (local development with minikube/kind or production with GKE/EKS/AKS).

**Version**: 1.0.0
**Date**: December 16, 2025
**Status**: ACTIVE - Week 9 Day 1
**Authority**: DevOps Lead + Backend Lead + CTO Approved
**Framework**: SDLC 4.9 Complete Lifecycle

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Architecture Overview](#architecture-overview)
3. [Quick Start (Local Development)](#quick-start-local-development)
4. [Production Deployment](#production-deployment)
5. [Configuration](#configuration)
6. [Verification](#verification)
7. [Troubleshooting](#troubleshooting)
8. [Maintenance](#maintenance)

---

## Prerequisites

### Required Tools

```bash
# kubectl (Kubernetes CLI)
kubectl version --client
# Required: v1.28.0+

# Docker (for building images)
docker --version
# Required: 20.10.0+

# Helm (optional, for cert-manager + NGINX Ingress)
helm version
# Required: v3.12.0+
```

### Local Development (Choose One)

**Option A: minikube (Recommended for macOS/Windows)**
```bash
# Install minikube
brew install minikube  # macOS
# OR download from: https://minikube.sigs.k8s.io/docs/start/

# Start cluster with 8GB RAM, 4 CPUs
minikube start --memory=8192 --cpus=4 --disk-size=50g

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server
```

**Option B: kind (Recommended for Linux)**
```bash
# Install kind
brew install kind  # macOS
# OR: go install sigs.k8s.io/kind@latest

# Create cluster
kind create cluster --name sdlc-orchestrator --config k8s/kind-config.yaml

# Install NGINX Ingress
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

### Production Clusters

- **GKE** (Google Kubernetes Engine): GKE 1.28+ Standard cluster
- **EKS** (Amazon Elastic Kubernetes Service): EKS 1.28+
- **AKS** (Azure Kubernetes Service): AKS 1.28+

**Required Add-ons**:
- NGINX Ingress Controller
- cert-manager (for TLS certificates)
- Prometheus Operator (optional, for monitoring)
- Storage class: `fast-ssd` (or modify `storageClassName` in manifests)

---

## Architecture Overview

### Deployed Components

```
┌─────────────────────────────────────────────────────────────┐
│                   Ingress (NGINX + TLS)                     │
│        https://api.sdlc-orchestrator.com/api/v1/*           │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────────┐
│               Backend API (FastAPI)                         │
│           3 replicas, ClusterIP Service                     │
└─┬──────────────┬─────────────┬─────────────┬────────────────┘
  │              │             │             │
  │              │             │             │
┌─┴──────────┐ ┌─┴──────────┐ ┌─┴──────────┐ ┌─┴──────────────┐
│ PostgreSQL │ │   Redis    │ │    OPA     │ │     MinIO      │
│ StatefulSet│ │ Deployment │ │ Deployment │ │  StatefulSet   │
│ 100Gi PVC  │ │ ClusterIP  │ │ ClusterIP  │ │  200Gi PVC     │
└────────────┘ └────────────┘ └────────────┘ └────────────────┘
```

### Resource Requirements

| Component | Replicas | CPU (req/lim) | Memory (req/lim) | Storage |
|-----------|----------|---------------|------------------|---------|
| Backend API | 3 | 500m/2 | 512Mi/2Gi | - |
| PostgreSQL | 1 | 500m/4 | 1Gi/8Gi | 100Gi |
| Redis | 1 | 100m/500m | 256Mi/1Gi | - |
| OPA | 2 | 100m/500m | 128Mi/512Mi | - |
| MinIO | 1 | 500m/2 | 1Gi/4Gi | 200Gi |
| **TOTAL** | **8 pods** | **4.5/15.5** | **5.3Gi/24Gi** | **300Gi** |

**Minimum Cluster Size**: 3 nodes × 4 CPU × 8GB RAM = 12 CPU, 24GB RAM

---

## Quick Start (Local Development)

### Step 1: Build Backend Docker Image

```bash
# Navigate to project root
cd /path/to/SDLC-Orchestrator

# Build backend image
docker build -t sdlc-orchestrator-backend:latest -f backend/Dockerfile .

# Verify image
docker images | grep sdlc-orchestrator-backend
```

**For minikube**: Load image into minikube's Docker daemon
```bash
minikube image load sdlc-orchestrator-backend:latest
```

**For kind**: Load image into kind cluster
```bash
kind load docker-image sdlc-orchestrator-backend:latest --name sdlc-orchestrator
```

### Step 2: Create Namespace

```bash
kubectl apply -f k8s/base/namespace.yaml

# Verify namespace
kubectl get namespace sdlc-orchestrator
```

### Step 3: Deploy Infrastructure Services

```bash
# Deploy PostgreSQL (database)
kubectl apply -f k8s/base/postgres-configmap.yaml
kubectl apply -f k8s/base/postgres-statefulset.yaml

# Wait for PostgreSQL to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=postgres -n sdlc-orchestrator --timeout=180s

# Deploy Redis (cache)
kubectl apply -f k8s/base/redis.yaml

# Wait for Redis to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=redis -n sdlc-orchestrator --timeout=120s

# Deploy OPA (policy engine)
kubectl apply -f k8s/base/opa.yaml

# Wait for OPA to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=opa -n sdlc-orchestrator --timeout=120s

# Deploy MinIO (object storage)
kubectl apply -f k8s/base/minio.yaml

# Wait for MinIO to be ready
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=minio -n sdlc-orchestrator --timeout=180s
```

### Step 4: Configure Application

```bash
# Create ConfigMap (non-sensitive configuration)
kubectl apply -f k8s/base/configmap.yaml

# Create Secrets (CHANGE PASSWORDS IN PRODUCTION!)
kubectl apply -f k8s/base/secrets.yaml

# Verify configuration
kubectl get configmap backend-config -n sdlc-orchestrator
kubectl get secret backend-secret postgres-secret redis-secret minio-secret -n sdlc-orchestrator
```

### Step 5: Deploy Backend API

```bash
# Deploy Backend API (includes Alembic migrations)
kubectl apply -f k8s/base/backend.yaml

# Wait for backend to be ready (may take 60s for migrations)
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=backend -n sdlc-orchestrator --timeout=180s

# Check backend logs
kubectl logs -l app.kubernetes.io/name=backend -n sdlc-orchestrator --tail=50
```

### Step 6: Verify Deployment

```bash
# Check all pods are running
kubectl get pods -n sdlc-orchestrator

# Expected output:
# NAME                       READY   STATUS    RESTARTS   AGE
# backend-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
# backend-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
# backend-xxxxxxxxxx-xxxxx   1/1     Running   0          2m
# minio-0                    1/1     Running   0          5m
# opa-xxxxxxxxxx-xxxxx       1/1     Running   0          4m
# opa-xxxxxxxxxx-xxxxx       1/1     Running   0          4m
# postgres-0                 2/2     Running   0          6m
# redis-xxxxxxxxxx-xxxxx     2/2     Running   0          5m

# Check services
kubectl get svc -n sdlc-orchestrator

# Port-forward to test locally
kubectl port-forward svc/backend 8000:8000 -n sdlc-orchestrator

# Test API (in another terminal)
curl http://localhost:8000/health
# Expected: {"status": "healthy", "timestamp": "..."}
```

---

## Production Deployment

### Step 1: Prerequisites

1. **Install NGINX Ingress Controller**
```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress-nginx ingress-nginx/ingress-nginx \
  --namespace ingress-nginx \
  --create-namespace \
  --set controller.service.type=LoadBalancer
```

2. **Install cert-manager (for Let's Encrypt TLS)**
```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager \
  --create-namespace \
  --set installCRDs=true
```

3. **Verify NGINX Ingress is ready**
```bash
kubectl get pods -n ingress-nginx
kubectl get svc -n ingress-nginx

# Get LoadBalancer IP
kubectl get svc ingress-nginx-controller -n ingress-nginx
# Note the EXTERNAL-IP for DNS configuration
```

### Step 2: Configure DNS

Point your domain to the LoadBalancer IP:

```bash
# A Record
api.sdlc-orchestrator.com → EXTERNAL-IP (from above)

# Example: api.sdlc-orchestrator.com → 34.123.45.67
```

Verify DNS propagation:
```bash
nslookup api.sdlc-orchestrator.com
# Should return LoadBalancer IP
```

### Step 3: Update Secrets (CRITICAL!)

**DO NOT use the default secrets in production!**

```bash
# Generate secure secrets
POSTGRES_PASSWORD=$(openssl rand -base64 32)
REDIS_PASSWORD=$(openssl rand -base64 32)
MINIO_PASSWORD=$(openssl rand -base64 32)
JWT_SECRET=$(openssl rand -hex 32)

# Base64 encode secrets
POSTGRES_PASSWORD_B64=$(echo -n "$POSTGRES_PASSWORD" | base64)
REDIS_PASSWORD_B64=$(echo -n "$REDIS_PASSWORD" | base64)
MINIO_PASSWORD_B64=$(echo -n "$MINIO_PASSWORD" | base64)
JWT_SECRET_B64=$(echo -n "$JWT_SECRET" | base64)

# Update secrets.yaml with new values
# Then apply:
kubectl apply -f k8s/base/secrets.yaml
```

**Recommended**: Use Kubernetes Secrets management tools:
- **Sealed Secrets**: https://github.com/bitnami-labs/sealed-secrets
- **HashiCorp Vault**: https://www.vaultproject.io/docs/platform/k8s
- **AWS Secrets Manager** (EKS): https://docs.aws.amazon.com/eks/latest/userguide/manage-secrets.html

### Step 4: Update Ingress Configuration

Edit [k8s/base/ingress.yaml](k8s/base/ingress.yaml):

```yaml
# Line 82-83: Change to your domain
  tls:
    - hosts:
        - api.your-domain.com  # CHANGE THIS
      secretName: sdlc-orchestrator-tls

# Line 86: Change to your domain
  rules:
    - host: api.your-domain.com  # CHANGE THIS

# Line 155: Change to your email
    email: your-email@example.com  # CHANGE THIS
```

### Step 5: Deploy to Production

```bash
# Follow same deployment steps as local (Steps 1-5)
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/postgres-configmap.yaml
kubectl apply -f k8s/base/postgres-statefulset.yaml
# ... (wait for each service to be ready)

# Deploy Ingress (with TLS)
kubectl apply -f k8s/base/ingress.yaml

# Wait for cert-manager to issue certificate (2-5 minutes)
kubectl get certificate -n sdlc-orchestrator --watch

# Expected output:
# NAME                      READY   SECRET                    AGE
# sdlc-orchestrator-tls     True    sdlc-orchestrator-tls     3m
```

### Step 6: Verify Production Deployment

```bash
# Test HTTPS endpoint
curl https://api.your-domain.com/health
# Expected: {"status": "healthy", "timestamp": "..."}

# Test API authentication
curl -X POST https://api.your-domain.com/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "SecurePassword123!",
    "full_name": "Admin User"
  }'

# Check certificate validity
echo | openssl s_client -connect api.your-domain.com:443 -servername api.your-domain.com 2>/dev/null | openssl x509 -noout -dates
# Should show Let's Encrypt certificate with 90-day expiry
```

---

## Configuration

### Environment Variables (ConfigMap)

All non-sensitive configuration is in [k8s/base/configmap.yaml](k8s/base/configmap.yaml):

```yaml
# Application Settings
APP_NAME: "SDLC Orchestrator"
APP_VERSION: "1.0.0"
LOG_LEVEL: "INFO"  # Change to "DEBUG" for troubleshooting

# Database Configuration
DATABASE_HOST: "postgres"
DATABASE_PORT: "5432"
DATABASE_NAME: "sdlc_orchestrator"

# Performance Tuning
DATABASE_POOL_SIZE: "20"  # Increase for high load
DATABASE_MAX_OVERFLOW: "50"

# JWT Configuration
ACCESS_TOKEN_EXPIRE_HOURS: "1"  # Token expiry (1 hour default)
REFRESH_TOKEN_EXPIRE_DAYS: "30"  # Refresh token expiry (30 days)
```

### Secrets Management

All sensitive data is in [k8s/base/secrets.yaml](k8s/base/secrets.yaml) (base64 encoded):

**Decode secrets** (for verification):
```bash
# PostgreSQL password
kubectl get secret postgres-secret -n sdlc-orchestrator -o jsonpath='{.data.password}' | base64 -d
echo

# JWT secret key
kubectl get secret backend-secret -n sdlc-orchestrator -o jsonpath='{.data.JWT_SECRET_KEY}' | base64 -d
echo
```

**Update secrets** (without downtime):
```bash
# Create new secret value
NEW_SECRET=$(openssl rand -base64 32)
NEW_SECRET_B64=$(echo -n "$NEW_SECRET" | base64)

# Patch secret
kubectl patch secret backend-secret -n sdlc-orchestrator \
  -p "{\"data\":{\"JWT_SECRET_KEY\":\"$NEW_SECRET_B64\"}}"

# Restart backend pods to pick up new secret
kubectl rollout restart deployment backend -n sdlc-orchestrator
```

### Persistent Storage Configuration

**PostgreSQL** (100Gi default):
```yaml
# k8s/base/postgres-statefulset.yaml (line 145-146)
resources:
  requests:
    storage: 100Gi  # Change to 500Gi for production
```

**MinIO** (200Gi default):
```yaml
# k8s/base/minio.yaml (line 145-146)
resources:
  requests:
    storage: 200Gi  # Change to 2Ti for production
```

**Storage Class**:
- Default: `fast-ssd` (SSD-backed persistent volumes)
- Change to `standard` for HDD (cheaper, slower)
- GKE: `pd-ssd` or `pd-standard`
- EKS: `gp3` or `io2`
- AKS: `managed-premium` or `managed`

```bash
# List available storage classes
kubectl get storageclass

# Update manifests to use your storage class
# Example: Change "fast-ssd" → "gp3" (EKS)
```

---

## Verification

### Health Checks

```bash
# Backend API health
kubectl exec -it deployment/backend -n sdlc-orchestrator -- \
  curl http://localhost:8000/health

# PostgreSQL health
kubectl exec -it postgres-0 -n sdlc-orchestrator -c postgres -- \
  pg_isready -U postgres

# Redis health
kubectl exec -it deployment/redis -n sdlc-orchestrator -c redis -- \
  redis-cli --no-auth-warning -a "$REDIS_PASSWORD" ping

# OPA health
kubectl exec -it deployment/opa -n sdlc-orchestrator -- \
  curl http://localhost:8181/health

# MinIO health
kubectl exec -it minio-0 -n sdlc-orchestrator -- \
  curl http://localhost:9000/minio/health/live
```

### Database Verification

```bash
# Connect to PostgreSQL
kubectl exec -it postgres-0 -n sdlc-orchestrator -c postgres -- \
  psql -U postgres -d sdlc_orchestrator

# List tables (in psql)
\dt

# Expected output:
#  public | alembic_version      | table | postgres
#  public | users                | table | postgres
#  public | roles                | table | postgres
#  public | projects             | table | postgres
#  public | gates                | table | postgres
#  public | gate_evidence        | table | postgres
#  public | policies             | table | postgres
#  ...

# Check Alembic migration version
SELECT * FROM alembic_version;

# Exit psql
\q
```

### API Endpoint Testing

```bash
# Register test user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPassword123!",
    "full_name": "Test User"
  }'

# Login
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "TestPassword123!"
  }' | jq -r '.access_token')

# Create project
curl -X POST http://localhost:8000/api/v1/projects \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "name": "Test Project",
    "description": "Test project for SDLC Orchestrator",
    "github_repo_url": "https://github.com/example/test-project"
  }'

# List projects
curl -X GET http://localhost:8000/api/v1/projects \
  -H "Authorization: Bearer $TOKEN"
```

### Monitoring & Metrics

```bash
# Prometheus metrics (backend)
kubectl port-forward svc/backend 8000:8000 -n sdlc-orchestrator &
curl http://localhost:8000/metrics

# PostgreSQL metrics
kubectl port-forward svc/postgres 9187:9187 -n sdlc-orchestrator &
curl http://localhost:9187/metrics

# Redis metrics
kubectl port-forward svc/redis 9121:9121 -n sdlc-orchestrator &
curl http://localhost:9121/metrics
```

---

## Troubleshooting

### Common Issues

#### 1. Pods Not Starting

```bash
# Check pod status
kubectl get pods -n sdlc-orchestrator

# Describe pod to see events
kubectl describe pod <pod-name> -n sdlc-orchestrator

# Check pod logs
kubectl logs <pod-name> -n sdlc-orchestrator --tail=100

# Common issues:
# - ImagePullBackOff: Docker image not found (re-build + load image)
# - CrashLoopBackOff: Application error (check logs)
# - Pending: Insufficient resources (add nodes or reduce resource requests)
```

#### 2. Backend Init Container Fails (Alembic Migrations)

```bash
# Check init container logs
kubectl logs <backend-pod-name> -n sdlc-orchestrator -c alembic-migrate

# Common issues:
# - "could not connect to server": PostgreSQL not ready (wait 60s, retry)
# - "relation already exists": Manual DB changes conflicting (reset DB)
# - "could not open file": Missing migration files (check Docker image)

# Manual migration (if needed)
kubectl exec -it deployment/backend -n sdlc-orchestrator -- \
  /bin/sh -c "cd /app/backend && alembic upgrade head"
```

#### 3. Database Connection Errors

```bash
# Verify PostgreSQL is running
kubectl get pods -l app.kubernetes.io/name=postgres -n sdlc-orchestrator

# Check PostgreSQL logs
kubectl logs postgres-0 -n sdlc-orchestrator -c postgres --tail=50

# Test connection from backend pod
kubectl exec -it deployment/backend -n sdlc-orchestrator -- \
  psql postgresql://postgres:changeme_secure_password@postgres:5432/sdlc_orchestrator

# Common issues:
# - "password authentication failed": Check secrets.yaml
# - "no pg_hba.conf entry": PostgreSQL not configured for remote access
# - "could not translate host name": DNS resolution issue (check service name)
```

#### 4. MinIO Connection Errors

```bash
# Check MinIO is running
kubectl get pods -l app.kubernetes.io/name=minio -n sdlc-orchestrator

# Check MinIO logs
kubectl logs minio-0 -n sdlc-orchestrator --tail=50

# Test MinIO S3 API
kubectl exec -it minio-0 -n sdlc-orchestrator -- \
  curl http://localhost:9000/minio/health/ready

# Access MinIO Console (web UI)
kubectl port-forward svc/minio 9001:9001 -n sdlc-orchestrator
# Open browser: http://localhost:9001
# Login: minioadmin / changeme_minio_password

# Common issues:
# - "AccessDenied": Check MINIO_ACCESS_KEY and MINIO_SECRET_KEY in secrets
# - "BucketAlreadyOwnedByYou": Normal (bucket exists, safe to ignore)
# - "NoSuchBucket": Backend will auto-create on first upload
```

#### 5. OPA Policy Evaluation Fails

```bash
# Check OPA is running
kubectl get pods -l app.kubernetes.io/name=opa -n sdlc-orchestrator

# Check OPA logs
kubectl logs deployment/opa -n sdlc-orchestrator --tail=50

# Test OPA health
kubectl exec -it deployment/opa -n sdlc-orchestrator -- \
  curl http://localhost:8181/health

# List loaded policies
kubectl exec -it deployment/opa -n sdlc-orchestrator -- \
  curl http://localhost:8181/v1/policies

# Test policy evaluation
kubectl exec -it deployment/opa -n sdlc-orchestrator -- \
  curl -X POST http://localhost:8181/v1/data/sdlc/gates/healthcheck \
  -H "Content-Type: application/json" \
  -d '{"input": {}}'

# Common issues:
# - "undefined decision": Policy not loaded (check ConfigMap)
# - "rego_parse_error": Syntax error in policy (validate Rego code)
```

#### 6. Ingress Not Working (502 Bad Gateway)

```bash
# Check Ingress status
kubectl get ingress -n sdlc-orchestrator

# Describe Ingress to see events
kubectl describe ingress sdlc-orchestrator-ingress -n sdlc-orchestrator

# Check NGINX Ingress Controller logs
kubectl logs -n ingress-nginx deployment/ingress-nginx-controller --tail=100

# Test backend service directly (bypass Ingress)
kubectl port-forward svc/backend 8000:8000 -n sdlc-orchestrator &
curl http://localhost:8000/health

# Common issues:
# - "503 Service Unavailable": Backend pods not ready (check pod status)
# - "404 Not Found": Path mismatch (check Ingress rules)
# - "certificate verify failed": cert-manager issue (check certificate status)

# Check TLS certificate
kubectl get certificate -n sdlc-orchestrator
kubectl describe certificate sdlc-orchestrator-tls -n sdlc-orchestrator
```

#### 7. Resource Limits / Out of Memory

```bash
# Check resource usage
kubectl top pods -n sdlc-orchestrator

# Check node resources
kubectl top nodes

# Describe pod to see resource constraints
kubectl describe pod <pod-name> -n sdlc-orchestrator | grep -A 10 "Limits\|Requests"

# Common issues:
# - "OOMKilled": Memory limit too low (increase limits in manifests)
# - "Insufficient memory": Node has no free memory (add nodes or reduce requests)
# - "CrashLoopBackOff" with OOMKilled: Reduce replicas or increase memory

# Increase memory limit (example: backend)
kubectl patch deployment backend -n sdlc-orchestrator \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"backend","resources":{"limits":{"memory":"4Gi"}}}]}}}}'
```

### Debugging Commands

```bash
# Get all resources in namespace
kubectl get all -n sdlc-orchestrator

# Get events (recent issues)
kubectl get events -n sdlc-orchestrator --sort-by='.lastTimestamp'

# Shell into backend pod
kubectl exec -it deployment/backend -n sdlc-orchestrator -- /bin/sh

# Shell into PostgreSQL pod
kubectl exec -it postgres-0 -n sdlc-orchestrator -c postgres -- /bin/bash

# Copy files from pod (e.g., logs)
kubectl cp sdlc-orchestrator/<pod-name>:/app/logs /tmp/logs

# Port-forward multiple services
kubectl port-forward svc/backend 8000:8000 -n sdlc-orchestrator &
kubectl port-forward svc/postgres 5432:5432 -n sdlc-orchestrator &
kubectl port-forward svc/minio 9000:9000 -n sdlc-orchestrator &

# Stop port-forwards
pkill -f "port-forward"
```

---

## Maintenance

### Scaling

#### Horizontal Scaling (Add More Replicas)

```bash
# Scale backend API (3 → 10 replicas)
kubectl scale deployment backend -n sdlc-orchestrator --replicas=10

# Scale OPA (2 → 5 replicas)
kubectl scale deployment opa -n sdlc-orchestrator --replicas=5

# Auto-scaling (HPA - Horizontal Pod Autoscaler)
kubectl autoscale deployment backend -n sdlc-orchestrator \
  --min=3 --max=20 --cpu-percent=70

# Check HPA status
kubectl get hpa -n sdlc-orchestrator
```

#### Vertical Scaling (Increase Resources)

```bash
# Increase backend memory (512Mi → 2Gi requests)
kubectl patch deployment backend -n sdlc-orchestrator \
  -p '{"spec":{"template":{"spec":{"containers":[{"name":"backend","resources":{"requests":{"memory":"2Gi"}}}]}}}}'

# Increase PostgreSQL storage (100Gi → 500Gi)
# NOTE: PVC expansion requires storageClass with allowVolumeExpansion=true
kubectl patch pvc postgres-data-postgres-0 -n sdlc-orchestrator \
  -p '{"spec":{"resources":{"requests":{"storage":"500Gi"}}}}'
```

### Updates & Rollouts

```bash
# Update backend image (new version)
kubectl set image deployment/backend backend=sdlc-orchestrator-backend:v1.1.0 -n sdlc-orchestrator

# Check rollout status
kubectl rollout status deployment/backend -n sdlc-orchestrator

# View rollout history
kubectl rollout history deployment/backend -n sdlc-orchestrator

# Rollback to previous version
kubectl rollout undo deployment/backend -n sdlc-orchestrator

# Rollback to specific revision
kubectl rollout undo deployment/backend -n sdlc-orchestrator --to-revision=2
```

### Backup & Restore

#### PostgreSQL Backup

```bash
# Manual backup (pg_dump)
kubectl exec postgres-0 -n sdlc-orchestrator -c postgres -- \
  pg_dump -U postgres sdlc_orchestrator | gzip > sdlc-orchestrator-$(date +%Y%m%d).sql.gz

# Restore from backup
gunzip -c sdlc-orchestrator-20251216.sql.gz | \
  kubectl exec -i postgres-0 -n sdlc-orchestrator -c postgres -- \
  psql -U postgres -d sdlc_orchestrator

# Automated backup (CronJob)
# See: docs/05-Deployment-Release/BACKUP-STRATEGY.md (if available)
```

#### MinIO Backup (Evidence Vault)

```bash
# Install MinIO Client (mc)
brew install minio/stable/mc  # macOS
# OR: https://min.io/docs/minio/linux/reference/minio-mc.html

# Configure mc alias
kubectl port-forward svc/minio 9000:9000 -n sdlc-orchestrator &
mc alias set sdlc-local http://localhost:9000 minioadmin changeme_minio_password

# Mirror bucket to local (backup)
mc mirror sdlc-local/gate-evidence ./backups/evidence-$(date +%Y%m%d)/

# Restore from backup
mc mirror ./backups/evidence-20251216/ sdlc-local/gate-evidence
```

### Log Management

```bash
# Stream logs from all backend pods
kubectl logs -f -l app.kubernetes.io/name=backend -n sdlc-orchestrator --all-containers=true

# Save logs to file
kubectl logs deployment/backend -n sdlc-orchestrator > backend-logs-$(date +%Y%m%d).log

# Log aggregation (Loki + Grafana recommended)
# See: monitoring/README.md (if available)
```

### Certificate Renewal

```bash
# cert-manager auto-renews Let's Encrypt certificates 30 days before expiry

# Check certificate expiry
kubectl get certificate sdlc-orchestrator-tls -n sdlc-orchestrator -o yaml | grep notAfter

# Force renewal (if needed)
kubectl delete secret sdlc-orchestrator-tls -n sdlc-orchestrator
kubectl delete certificate sdlc-orchestrator-tls -n sdlc-orchestrator
kubectl apply -f k8s/base/ingress.yaml

# Watch renewal
kubectl get certificate -n sdlc-orchestrator --watch
```

### Cleanup (Remove Deployment)

```bash
# Delete all resources
kubectl delete namespace sdlc-orchestrator

# WARNING: This will delete all data (PostgreSQL, MinIO PVCs)
# Backup first if you need to preserve data!

# Delete only application (keep data)
kubectl delete deployment,service,ingress -n sdlc-orchestrator --all

# Delete PVCs separately (if you want to remove data)
kubectl delete pvc -n sdlc-orchestrator --all
```

---

## Additional Resources

### Documentation

- **SDLC Orchestrator Architecture**: [docs/02-Design-Architecture/System-Architecture-Document.md](../docs/02-Design-Architecture/System-Architecture-Document.md)
- **API Specification**: [docs/02-Design-Architecture/04-API-Specifications/openapi.yml](../docs/02-Design-Architecture/04-API-Specifications/openapi.yml)
- **Security Baseline**: [docs/02-Design-Architecture/Security-Baseline.md](../docs/02-Design-Architecture/Security-Baseline.md) (if available)

### External Links

- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **NGINX Ingress Controller**: https://kubernetes.github.io/ingress-nginx/
- **cert-manager**: https://cert-manager.io/docs/
- **PostgreSQL on Kubernetes**: https://www.postgresql.org/docs/
- **MinIO Kubernetes Operator**: https://min.io/docs/minio/kubernetes/upstream/
- **OPA Documentation**: https://www.openpolicyagent.org/docs/latest/

---

## Support

For issues or questions:

1. **Check Logs**: `kubectl logs <pod-name> -n sdlc-orchestrator`
2. **Review Troubleshooting Section**: See above
3. **GitHub Issues**: https://github.com/your-org/sdlc-orchestrator/issues (replace with actual repo)
4. **Internal Support**: Contact DevOps team (Slack: #sdlc-orchestrator-support)

---

**Document Status**: ✅ PRODUCTION-READY
**Last Updated**: December 16, 2025
**Maintained By**: DevOps Lead + Backend Lead
**Review Cadence**: Monthly (or after major k8s version updates)

---

*SDLC Orchestrator - First Governance-First Platform on SDLC 4.9*

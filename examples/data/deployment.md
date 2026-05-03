# Deployment Guide

How to deploy SampleProject to production.

## Metadata

- **name**: Deployment
- **version**: `1.0.0`
- **environment**: production

## Prerequisites

- Docker 24+
- Kubernetes 1.28+
- kubectl configured

## Quick Start

```bash
# Clone repository
git clone https://github.com/example/sampleproject.git
cd sampleproject

# Deploy to Kubernetes
kubectl apply -f k8s/
```

## Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## Health Checks

```yaml
# health.toon
HEALTH[3]
  [1] cc_mean=12.5
  [2] coverage=87%
  [3] complexity=low
```

## Monitoring Setup

- Prometheus metrics at `/metrics`
- Grafana dashboards in `monitoring/` directory
- Alertmanager for critical alerts

## Rollback Procedure

1. Check current deployment: `kubectl get deployments`
2. Rollback: `kubectl rollout undo deployment/app`
3. Verify: `kubectl get pods`

## Related Documents

- See [Project Overview](project_overview.md)
- See [API Reference](api_reference.md)
- Image reference: ![Architecture diagram](../assets/arch.png)

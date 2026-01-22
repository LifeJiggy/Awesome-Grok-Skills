# Deployment Guide

This guide covers deployment procedures for Awesome Grok Skills.

## 🚀 Quick Deployment

### Prerequisites

- Python 3.9+
- Git
- pip or uv
- (Optional) Docker

### Local Installation

```bash
# Clone repository
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills

# Install in development mode
pip install -e .

# Or install with all dependencies
pip install -e ".[dev]"

# Verify installation
grok --version
```

### Global Installation

```bash
# Install globally
pip install awesome-grok-skills

# Symlink skills and agents
ln -s $(python -c "import site; print(site.getsitepackages()[0])")/awesome_grok_skills/skills ~/.grok/skills
ln -s $(python -c "import site; print(site.getsitepackages()[0])")/awesome_grok_skills/agents ~/.grok/agents
```

---

## 🐳 Docker Deployment

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Install package
RUN pip install --no-cache-dir -e .

# Entrypoint
ENTRYPOINT ["python", "-m", "awesome_grok_skills"]
```

### Docker Compose

```yaml
# docker-compose.yml
version: "3.8"

services:
  grok-skills:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GROK_API_KEY=${GROK_API_KEY}
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    restart: unless-stopped

volumes:
  redis-data:
```

### Build and Run

```bash
# Build image
docker build -t awesome-grok-skills:latest .

# Run container
docker run -p 8000:8000 awesome-grok-skills:latest

# With docker compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## ☁️ Cloud Deployment

### AWS Deployment

#### Using ECS

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.us-east-1.amazonaws.com

docker tag awesome-grok-skills:latest ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/awesome-grok-skills:latest

docker push ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/awesome-grok-skills:latest

# Update ECS service
aws ecs update-service --cluster awesome-grok-skills-cluster --service awesome-grok-skills-service --force-new-deployment
```

#### Using Lambda

```bash
# Build Lambda deployment package
pip install -r requirements.txt -t package/

# Add your code files
cp -r awesome_grok_skills/* package/
cp handler.py package/

cd package && zip ../deployment.zip .
cd .. && zip deployment.zip package/ -r

# Upload to Lambda
aws lambda update-function-code \
    --function-name awesome-grok-skills \
    --zip-file fileb://deployment.zip
```

### Google Cloud Platform

```bash
# Build using Cloud Build
gcloud builds submit --tag gcr.io/PROJECT_ID/awesome-grok-skills

# Deploy to Cloud Run
gcloud run deploy awesome-grok-skills \
    --image gcr.io/PROJECT_ID/awesome-grok-skills \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

### Azure

```bash
# Build and push to Container Registry
az acr build --registry myregistry --image awesome-grok-skills:latest .

# Deploy to Azure Container Apps
az containerapp up \
  --name awesome-grok-skills \
  --resource-group mygroup \
  --image myregistry.azurecr.io/awesome-grok-skills:latest
```

---

## 🔧 Configuration

### Environment Variables

```bash
# Required
export GROK_API_KEY="your-api-key"

# Optional
export LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
export MAX_WORKERS=4
export CACHE_DIR="/tmp/grok-cache"
export DATABASE_URL="postgresql://user:pass@localhost/db"

# For cloud providers
export AWS_DEFAULT_REGION="us-east-1"
export GCP_PROJECT="my-project"
```

### Configuration File

```yaml
# config.yaml
app:
  name: Awesome Grok Skills
  version: 1.0.0
  log_level: INFO
  
skills:
  enabled:
    - ai-ml
    - data-science
    - cloud
  disabled:
    - experimental
  
agents:
  max_concurrent: 4
  timeout: 300
  
cache:
  type: redis
  ttl: 3600
  
database:
  type: postgresql
  host: localhost
  port: 5432
  name: grok_skills
  
logging:
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: logs/app.log
```

---

## 📊 Monitoring

### Health Checks

```python
# health.py
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class HealthStatus(BaseModel):
    status: str
    version: str
    components: Dict[str, str]

@router.get("/health", response_model=HealthStatus)
async def health_check():
    """Check health of all components."""
    return HealthStatus(
        status="healthy",
        version="1.0.0",
        components={
            "database": "healthy",
            "cache": "healthy",
            "skills": "healthy"
        }
    )

@router.get("/ready")
async def readiness_check():
    """Check if service is ready to accept traffic."""
    if_database_connected is() and is_cache_connected():
        return {"status": "ready"}
    raise HTTPException(status_code=503, detail="Not ready")
```

### Metrics with Prometheus

```python
from prometheus_client import Counter, Histogram, start_http_server
import random
import time

# Define metrics
REQUEST_COUNT = Counter(
    'grok_requests_total',
    'Total number of requests',
    ['method', 'endpoint']
)
REQUEST_LATENCY = Histogram(
    'grok_request_duration_seconds',
    'Request latency in seconds',
    ['method', 'endpoint']
)

# Start metrics server
start_http_server(8000)

# Instrument your code
@REQUEST_LATENCY.time()
def process_request(endpoint):
    REQUEST_COUNT.labels(method='GET', endpoint=endpoint).inc()
    # Process request...
```

### Logging

```python
import logging
import sys

def setup_logging(log_level: str = "INFO"):
    """Configure logging."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("logs/app.log"),
        ]
    )

# Structured logging with JSON
import json_logging

json_logging.init_non_web()
logger = json_logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("Structured log message", extra={"props": {"key": "value"}})
```

---

## 🔒 Security

### Secrets Management

```python
from dataclasses import dataclass
from typing import Optional
import os

@dataclass
class Secrets:
    """Application secrets."""
    api_key: str
    database_url: str
    encryption_key: str
    
    @classmethod
    def from_env(cls) -> "Secrets":
        """Load secrets from environment variables."""
        return cls(
            api_key=os.environ.get("GROK_API_KEY", ""),
            database_url=os.environ.get("DATABASE_URL", ""),
            encryption_key=os.environ.get("ENCRYPTION_KEY", ""),
        )
```

### Using HashiCorp Vault

```python
import hvac

def load_secrets_from_vault(vault_url: str, vault_token: str, secret_path: str):
    """Load secrets from HashiCorp Vault."""
    client = hvac.Client(url=vault_url, token=vault_token)
    secret = client.secrets.kv.v2.read_secret_version(path=secret_path)
    return secret["data"]["data"]
```

### Docker Security

```dockerfile
# Use non-root user
FROM python:3.11-slim

# Create user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Copy files
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER appuser

# Install dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

CMD ["python", "app.py"]
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Deployment

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  release:
    types: [published]
  workflow_dispatch:
    inputs:
      environment:
        description: Deployment environment
        required: true
        default: staging
        type: choice
        options:
          - staging
          - production

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ github.event.inputs.environment || 'staging' }}
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:${{ github.sha }}
            ghcr.io/${{ github.repository }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
      
      - name: Deploy to ${{ github.event.inputs.environment || 'staging' }}
        run: |
          echo "Deploying to ${{ github.event.inputs.environment || 'staging' }}"
          # Add deployment commands here
          # - kubectl apply
          # - terraform apply
          # - etc.
```

### Terraform Infrastructure

```hcl
# main.tf
terraform {
  backend "s3" {
    bucket = "awesome-grok-skills-tfstate"
    key    = "production/terraform.tfstate"
    region = "us-east-1"
  }
}

resource "aws_ecs_service" "main" {
  name            = "awesome-grok-skills"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.main.arn
  desired_count   = 2
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = [aws_subnet.public.id]
    security_groups = [aws_security_group.ecs.id]
    assign_public_ip = true
  }
}
```

---

## 📈 Performance Optimization

### Caching

```python
from functools import lru_cache, wraps
import redis

redis_client = redis.Redis(host="localhost", port=6379, db=0)

def cached(ttl: int = 3600):
    """Cache decorator with TTL."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            cached_result = redis_client.get(key)
            if cached_result:
                return pickle.loads(cached_result)
            result = func(*args, **kwargs)
            redis_client.setex(key, ttl, pickle.dumps(result))
            return result
        return wrapper
    return decorator

@cached(ttl=300)
def expensive_computation(x: int) -> int:
    """Expensive computation to cache."""
    return sum(i * i for i in range(x))
```

### Async Processing

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncProcessor:
    """Async processing with thread pool."""
    
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def process_async(self, tasks: List[Callable], data: List[Any]) -> List[Any]:
        """Process tasks asynchronously."""
        loop = asyncio.get_event_loop()
        results = await asyncio.gather(
            *[
                loop.run_in_executor(self.executor, task, item)
                for task, item in zip(tasks, data)
            ]
        )
        return results
    
    def __del__(self):
        self.executor.shutdown(wait=False)
```

---

## 🧪 Rollback Procedures

### Docker Rollback

```bash
# List previous images
docker images ghcr.io/awesome-grok-skills

# Rollback to previous version
docker tag ghcr.io/awesome-grok-skills:<previous-sha> awesome-grok-skills:latest
docker push ghcr.io/awesome-grok-skills:latest

# Restart service
docker-compose up -d
```

### Kubernetes Rollback

```bash
# View deployment history
kubectl rollout history deployment/awesome-grok-skills

# Rollback to previous version
kubectl rollout undo deployment/awesome-grok-skills

# Rollback to specific revision
kubectl rollout undo deployment/awesome-grok-skills --to-revision=3

# Monitor rollback
kubectl rollout status deployment/awesome-grok-skills
```

---

## 📞 Support

For deployment issues:

1. Check logs: `docker-compose logs`
2. Check metrics: `/metrics` endpoint
3. Check health: `/health` endpoint
4. Review CI/CD runs in GitHub Actions

---

**Deploy with confidence! 🚀**

---
name: "fastapi-best-practices"
category: "backend"
version: "2.0.0"
tags: ["backend", "fastapi-best-practices", "python", "async", "api"]
---

# FastAPI Best Practices

## Overview

Production-grade FastAPI development guide covering dependency injection, middleware architecture, Pydantic model design, async concurrency patterns, comprehensive testing, OpenAPI documentation, rate limiting, structured error handling, database session management, and background task orchestration. This module distills patterns from high-traffic API deployments handling 10k+ RPS with sub-50ms p99 latency.

## Core Capabilities

- Dependency injection with lifespan-aware singletons and scoped dependencies
- Middleware pipeline design (CORS, auth, logging, compression, request-id propagation)
- Pydantic v2 model validation, serialization, and OpenAPI schema generation
- Async/await patterns: structured concurrency, semaphores, connection pooling
- OpenAPI docs customization with dark mode, auth presets, and tag ordering
- Token-bucket and sliding-window rate limiting with Redis backend
- Structured exception hierarchy with RFC 7807 Problem Details
- Database session lifecycle management with SQLAlchemy 2.0 async
- Background task orchestration with ARQ, Dramatiq, and native FastAPI tasks
- Health checks, readiness probes, and graceful shutdown hooks

## Usage

```python
from fastapi import FastAPI, Depends, Request
from fastapi.middleware import Middleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import asyncio

app = FastAPI(
    title="Production API",
    version="2.0.0",
    docs_url="/internal/docs",
    redoc_url="/internal/redoc",
)

# Middleware stack
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Dependency injection
async def get_db():
    async with async_session() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    user = await verify_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user

# Rate-limited endpoint
@app.post("/api/v1/orders", dependencies=[Depends(rate_limit("10/minute"))])
async def create_order(
    payload: OrderCreate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> OrderResponse:
    order = await OrderService.create(db, user, payload)
    return OrderResponse.model_validate(order)
```

## Best Practices

- Use `Depends()` for all shared state; never use global mutable variables
- Prefer `async def` for I/O-bound endpoints; use `def` for CPU-bound
- Apply rate limiting per-route via dependencies, not global middleware
- Return Pydantic models directly; avoid manual `dict()` serialization
- Use `BackgroundTasks` for fire-and-forget work; use ARQ for durable jobs
- Keep route handlers thin — delegate to service-layer classes
- Version your API via URL prefix (`/api/v1/`), not headers
- Use `response_model_exclude_unset=True` to omit default fields
- Add request-id middleware for distributed tracing correlation
- Pin FastAPI, Pydantic, and Starlette versions in requirements files

## Related Modules

- `sqlalchemy-async` — Async ORM session management
- `pydantic-v2` — Schema validation and serialization
- `redis-rate-limiter` — Distributed rate limiting backend
- `arq-background` — Durable background job processing
- `opentelemetry-fastapi` — Distributed tracing instrumentation

---

## Advanced Configuration

```python
# app/config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "production-api"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "production"  # development | staging | production

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/db"
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30
    DB_ECHO: bool = False

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_MAX_CONNECTIONS: int = 50

    # Auth
    JWT_SECRET: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRATION_DAYS: int = 7

    # Rate Limiting
    RATE_LIMIT_DEFAULT: str = "60/minute"
    RATE_LIMIT_AUTH: str = "5/minute"

    # CORS
    CORS_ORIGINS: list[str] = ["https://app.example.com"]
    CORS_ALLOW_CREDENTIALS: bool = True

    # OpenAPI
    DOCS_URL: str = "/internal/docs"
    REDOC_URL: str = "/internal/redoc"
    OPENAPI_URL: str = "/internal/openapi.json"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"  # json | text

    model_config = {"env_file": ".env", "env_prefix": "APP_"}

@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### Environment-Specific Overrides

```python
# For testing
class TestSettings(Settings):
    DATABASE_URL: str = "sqlite+aiosqlite:///test.db"
    REDIS_URL: str = "redis://localhost:6379/1"
    RATE_LIMIT_DEFAULT: str = "1000/minute"  # effectively disabled

# For Docker
class DockerSettings(Settings):
    DATABASE_URL: str = "postgresql+asyncpg://db:5432/app"
    REDIS_URL: str = "redis://redis:6379/0"
```

### Lifespan Management

```python
from contextlib import asynccontextmanager
import redis.asyncio as redis

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.redis = redis.from_url(
        get_settings().REDIS_URL,
        max_connections=get_settings().REDIS_MAX_CONNECTIONS,
    )
    app.state.db_engine = create_async_engine(
        get_settings().DATABASE_URL,
        pool_size=get_settings().DB_POOL_SIZE,
        max_overflow=get_settings().DB_MAX_OVERFLOW,
    )
    yield
    # Shutdown
    await app.state.redis.close()
    await app.state.db_engine.dispose()

app = FastAPI(lifespan=lifespan)
```

---

## Architecture Patterns

```
                    ┌─────────────────────────────────┐
                    │          Load Balancer           │
                    │         (nginx / traefik)        │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │        FastAPI Application       │
                    │  ┌──────────────────────────┐   │
                    │  │    Middleware Pipeline     │   │
                    │  │  ┌────────────────────┐  │   │
                    │  │  │   Request ID        │  │   │
                    │  │  ├────────────────────┤  │   │
                    │  │  │   CORS              │  │   │
                    │  │  ├────────────────────┤  │   │
                    │  │  │   Auth / JWT        │  │   │
                    │  │  ├────────────────────┤  │   │
                    │  │  │   Rate Limiter      │  │   │
                    │  │  ├────────────────────┤  │   │
                    │  │  │   Compression       │  │   │
                    │  │  ├────────────────────┤  │   │
                    │  │  │   Logging           │  │   │
                    │  │  └────────────────────┘  │   │
                    │  └──────────────────────────┘   │
                    │                                   │
                    │  ┌──────────────────────────┐   │
                    │  │    Route Handlers         │   │
                    │  │  ┌──────┐  ┌──────┐     │   │
                    │  │  │ /api │  │ /api │     │   │
                    │  │  │ /v1  │  │ /v2  │     │   │
                    │  │  └──┬───┘  └──┬───┘     │   │
                    │  └─────┼─────────┼──────────┘   │
                    │        │         │               │
                    │  ┌─────▼─────────▼──────────┐   │
                    │  │    Dependency Graph        │   │
                    │  │  ┌──────┐  ┌──────────┐  │   │
                    │  │  │  DB  │  │  Redis   │  │   │
                    │  │  │ Sess │  │  Cache   │  │   │
                    │  │  └──────┘  └──────────┘  │   │
                    │  │  ┌──────┐  ┌──────────┐  │   │
                    │  │  │ Auth │  │  Queue   │  │   │
                    │  │  │ Svc  │  │  Client  │  │   │
                    │  │  └──────┘  └──────────┘  │   │
                    │  └──────────────────────────┘   │
                    └──────────────┬──────────────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              │                    │                     │
    ┌─────────▼────────┐ ┌────────▼────────┐ ┌─────────▼────────┐
    │   PostgreSQL      │ │     Redis       │ │   Message Queue  │
    │   (primary +      │ │   (cache, rate  │ │   (ARQ / Celery)  │
    │    replicas)      │ │    limits, pub  │ │                   │
    │                   │ │    sub)          │ │                   │
    └───────────────────┘ └─────────────────┘ └───────────────────┘
```

### Request Lifecycle

```
Client Request
    │
    ▼
[1] Reverse Proxy (TLS termination, load balancing)
    │
    ▼
[2] Middleware Pipeline
    │  ├─ Request ID injection
    │  ├─ CORS validation
    │  ├─ JWT token extraction & validation
    │  ├─ Rate limit check (Redis)
    │  ├─ Request logging (structured JSON)
    │  └─ Gzip/Brotli compression
    │
    ▼
[3] Route Matching (FastAPI/Starlette router)
    │
    ▼
[4] Dependency Resolution
    │  ├─ Database session (scoped to request)
    │  ├─ Current user (from JWT)
    │  ├─ Service instances (singleton or transient)
    │  └─ Permission checks
    │
    ▼
[5] Request Validation (Pydantic v2)
    │  ├─ Body parsing
    │  ├─ Field validation
    │  └─ Model serialization config
    │
    ▼
[6] Handler Execution
    │  ├─ Business logic (service layer)
    │  ├─ Database operations (async)
    │  └─ Background task scheduling
    │
    ▼
[7] Response Serialization (Pydantic → JSON)
    │
    ▼
[8] Middleware Egress (response headers, logging)
    │
    ▼
Client Response
```

---

## Integration Guide

### Database Integration (SQLAlchemy 2.0 Async)

```python
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)

AsyncSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Redis Integration

```python
import redis.asyncio as redis
from typing import Optional
import json

class CacheService:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def get(self, key: str) -> Optional[dict]:
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def set(
        self, key: str, value: dict, ttl: int = 300
    ) -> None:
        await self.redis.set(key, json.dumps(value), ex=ttl)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def increment(self, key: str, ttl: int = 60) -> int:
        pipe = self.redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, ttl)
        results = await pipe.execute()
        return results[0]
```

### Authentication Middleware

```python
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import datetime, timedelta

security = HTTPBearer()

async def create_access_token(user_id: int, roles: list[str]) -> str:
    settings = get_settings()
    payload = {
        "sub": str(user_id),
        "roles": roles,
        "exp": datetime.utcnow() + timedelta(
            minutes=settings.JWT_EXPIRATION_MINUTES
        ),
        "iat": datetime.utcnow(),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> dict:
    settings = get_settings()
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

## Performance Optimization

| Technique | Impact | When to Use |
|-----------|--------|-------------|
| Connection pooling | 3-5x throughput | Always — never create connections per request |
| Response caching | 10-100x latency reduction | Read-heavy endpoints with stable data |
| Async/await | 2-10x concurrency | I/O-bound operations (DB, HTTP, Redis) |
| Pydantic v2 (Rust core) | 5-50x faster validation | Always — automatic with Pydantic v2 |
| Gzip compression | 60-80% bandwidth reduction | JSON responses > 1KB |
| Pagination | Bounded memory and CPU | List endpoints returning collections |
| Selective serialization | 20-40% payload reduction | Endpoints with large models |
| Database query optimization | 2-100x query speed | N+1 queries, missing indexes |

### Caching Strategies

```python
from fastapi import Request
from starlette.responses import Response
import hashlib

def cache_control(max_age: int = 300, private: bool = False):
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            response = await func(request, *args, **kwargs)
            scope = "private" if private else "public"
            response.headers["Cache-Control"] = f"{scope}, max-age={max_age}"
            return response
        return wrapper
    return decorator

@app.get("/api/v1/products")
@cache_control(max_age=60, private=True)
async def list_products(db: AsyncSession = Depends(get_db)):
    products = await Product.query.all(db)
    return products

# ETag-based conditional responses
@app.get("/api/v1/products/{product_id}")
async def get_product(
    product_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    product = await Product.get(db, product_id)
    etag = hashlib.md5(
        f"{product.id}:{product.updated_at}".encode()
    ).hexdigest()

    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)

    response = JSONResponse(ProductResponse.model_validate(product))
    response.headers["ETag"] = etag
    return response
```

### Connection Pool Tuning

```python
# SQLAlchemy pool configuration for high-throughput
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,           # persistent connections
    max_overflow=30,        # burst connections
    pool_timeout=10,        # seconds to wait for connection
    pool_recycle=1800,      # recycle connections every 30 min
    pool_pre_ping=True,     # validate connections before use
    echo_pool=True,         # log pool checkouts (dev only)
)

# Redis pool
redis_pool = redis.ConnectionPool.from_url(
    REDIS_URL,
    max_connections=50,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True,
)
```

---

## Security Considerations

### Input Validation and Sanitization

```python
from pydantic import Field, EmailStr, field_validator
import re

class UserCreate(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    password: str = Field(..., min_length=12, max_length=128)
    display_name: str = Field(..., min_length=1, max_length=50)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain special character")
        return v

    @field_validator("display_name")
    @classmethod
    def sanitize_display_name(cls, v: str) -> str:
        # Strip HTML tags and dangerous characters
        v = re.sub(r"<[^>]+>", "", v)
        v = re.sub(r"[<>\"';]", "", v)
        return v.strip()
```

### Security Headers Middleware

```python
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=63072000; includeSubDomains; preload"
        )
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; script-src 'self'"
        )
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )
        return response
```

### OWASP FastAPI Checklist

- Always validate input with Pydantic models; never trust raw `Request.body()`
- Use parameterized queries via SQLAlchemy ORM; never use string concatenation
- Store secrets in environment variables or vault; never in source code
- Implement CSRF protection for cookie-based authentication
- Use HTTPS everywhere; redirect HTTP to HTTPS at the reverse proxy
- Set `SameSite=Strict` on session cookies
- Limit request body size with middleware
- Log authentication failures for anomaly detection
- Rotate JWT signing keys periodically
- Use short-lived access tokens (15-30 min) with refresh tokens

---

## Troubleshooting Guide

| Symptom | Likely Cause | Solution |
|---------|-------------|----------|
| `422 Validation Error` on POST | Pydantic model mismatch | Check field names, types, and required vs optional |
| `Connection pool exhausted` | Too many concurrent requests | Increase `pool_size` or add connection timeout |
| `503 Service Unavailable` | Database or Redis down | Check health endpoints, verify connection strings |
| Slow responses (> 500ms) | N+1 queries or missing indexes | Use `selectinload()`, check `EXPLAIN ANALYZE` |
| `CORS error` in browser | Missing origin in CORS config | Add frontend origin to `allow_origins` |
| `401 Unauthorized` on valid token | Clock skew or wrong secret | Verify JWT secret matches, check server time |
| Memory leak over time | Unclosed connections or sessions | Ensure `async with` for all sessions, check pool settings |
| `BackgroundTask` not executing | Event loop blocked | Move to ARQ/Dramatiq for CPU-bound tasks |
| OpenAPI docs not loading | `docs_url=None` or auth blocking | Check `DOCS_URL` setting, allow internal IPs |
| `413 Payload Too Large` | Request body exceeds limit | Configure reverse proxy `client_max_body_size` |
| Duplicate requests on retry | No idempotency key | Implement idempotency middleware with Redis |

---

## API Reference

### Core Endpoints

| Method | Path | Description | Rate Limit |
|--------|------|-------------|------------|
| `POST` | `/api/v1/auth/login` | Authenticate user, return JWT | 5/min |
| `POST` | `/api/v1/auth/refresh` | Refresh access token | 10/min |
| `GET` | `/api/v1/users/me` | Get current user profile | 60/min |
| `PUT` | `/api/v1/users/me` | Update current user | 30/min |
| `GET` | `/api/v1/resources` | List resources (paginated) | 60/min |
| `POST` | `/api/v1/resources` | Create resource | 30/min |
| `GET` | `/api/v1/resources/{id}` | Get resource by ID | 120/min |
| `PUT` | `/api/v1/resources/{id}` | Update resource | 30/min |
| `DELETE` | `/api/v1/resources/{id}` | Delete resource | 30/min |
| `GET` | `/health` | Health check | unlimited |
| `GET` | `/ready` | Readiness probe | unlimited |

### Response Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| `200` | OK | Successful GET, PUT |
| `201` | Created | Successful POST |
| `204` | No Content | Successful DELETE |
| `304` | Not Modified | Conditional GET with matching ETag |
| `400` | Bad Request | Malformed request body |
| `401` | Unauthorized | Missing or invalid authentication |
| `403` | Forbidden | Authenticated but insufficient permissions |
| `404` | Not Found | Resource does not exist |
| `409` | Conflict | Duplicate creation or optimistic lock failure |
| `422` | Unprocessable Entity | Validation error |
| `429` | Too Many Requests | Rate limit exceeded |
| `500` | Internal Server Error | Unhandled exception |
| `503` | Service Unavailable | Dependency failure |

---

## Data Models

### Request Models

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderCreate(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=100)
    shipping_address: str = Field(..., min_length=10, max_length=500)
    notes: Optional[str] = Field(None, max_length=1000)

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    shipping_address: Optional[str] = Field(None, min_length=10, max_length=500)
    notes: Optional[str] = Field(None, max_length=1000)

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)
    sort_by: str = Field("created_at")
    sort_order: str = Field("desc", pattern="^(asc|desc)$")
```

### Response Models

```python
class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    product_id: int
    quantity: int
    status: OrderStatus
    shipping_address: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

class PaginatedResponse(BaseModel):
    items: list[OrderResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

class ErrorResponse(BaseModel):
    detail: str
    error_code: str
    request_id: Optional[str] = None
```

### Database Models

```python
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    shipping_address: Mapped[str] = mapped_column(Text)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    user: Mapped["User"] = relationship(back_populates="orders")
    product: Mapped["Product"] = relationship()
```

---

## Deployment Guide

### Docker Configuration

```dockerfile
FROM python:3.12-slim AS builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim AS runtime

RUN adduser --disabled-password --gecos '' appuser
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Docker Compose

```yaml
version: "3.9"
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d app"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5
```

### Kubernetes Manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
        - name: api
          image: registry.example.com/api:2.0.0
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: api-secrets
                  key: database-url
          livenessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 10
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 5
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
```

---

## Monitoring and Observability

### Structured Logging

```python
import structlog
import logging

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

logger = structlog.get_logger()

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(request_id=request_id)

    logger.info("request_started", method=request.method, path=request.url.path)
    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time
    logger.info(
        "request_completed",
        status_code=response.status_code,
        duration_ms=round(duration * 1000, 2),
    )
    return response
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "Request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

DB_CONNECTIONS = Gauge(
    "db_pool_connections",
    "Database pool connection count",
    ["state"],  # active, idle, overflow
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    method = request.method
    path = request.url.path

    with REQUEST_LATENCY.labels(method=method, endpoint=path).time():
        response = await call_next(request)

    REQUEST_COUNT.labels(
        method=method,
        endpoint=path,
        status_code=response.status_code,
    ).inc()
    return response
```

### Health Check Endpoints

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "2.0.0"}

@app.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)):
    checks = {}

    # Database check
    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "failed"

    # Redis check
    try:
        await app.state.redis.ping()
        checks["redis"] = "ok"
    except Exception:
        checks["redis"] = "failed"

    all_healthy = all(v == "ok" for v in checks.values())
    status_code = 200 if all_healthy else 503

    return JSONResponse(
        content={"status": "ready" if all_healthy else "not_ready", "checks": checks},
        status_code=status_code,
    )
```

---

## Testing Strategy

### Test Configuration

```python
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def db_engine():
    engine = create_async_engine("sqlite+aiosqlite:///test.db")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()

@pytest.fixture(scope="function")
async def db_session(db_engine):
    async with async_sessionmaker(db_engine, class_=AsyncSession)() as session:
        yield session

@pytest.fixture(scope="function")
async def client(db_engine):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac
```

### Test Examples

```python
import pytest

@pytest.mark.asyncio
async def test_create_order(client, db_session):
    # Arrange
    user = await create_test_user(db_session)
    token = await create_test_token(user.id)

    # Act
    response = await client.post(
        "/api/v1/orders",
        json={
            "product_id": 1,
            "quantity": 2,
            "shipping_address": "123 Test St, City, Country",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    # Assert
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == 1
    assert data["quantity"] == 2
    assert data["status"] == "pending"

@pytest.mark.asyncio
async def test_rate_limit(client):
    responses = []
    for _ in range(10):
        resp = await client.get("/api/v1/products")
        responses.append(resp.status_code)

    assert 429 in responses, "Rate limiting should trigger"

@pytest.mark.asyncio
async def test_unauthorized_access(client):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_validation_error(client):
    response = await client.post(
        "/api/v1/orders",
        json={"product_id": -1, "quantity": 0},
    )
    assert response.status_code == 422
```

---

## Versioning and Migration

### API Versioning Strategy

```python
from fastapi import APIRouter

# v1 router
v1_router = APIRouter(prefix="/api/v1")

@v1_router.get("/orders")
async def list_orders_v1(...):
    return {"orders": [...]}  # flat structure

# v2 router (backward compatible)
v2_router = APIRouter(prefix="/api/v2")

@v2_router.get("/orders")
async def list_orders_v2(...):
    return {
        "data": [...],
        "meta": {"total": 100, "page": 1},
    }  # envelope structure

app.include_router(v1_router)
app.include_router(v2_router)
```

### Database Migration with Alembic

```python
# alembic.ini
[alembic]
script_location = migrations
sqlalchemy.url = postgresql+asyncpg://user:pass@localhost/db

# migrations/versions/001_initial.py
"""Initial migration

Revision ID: 001
Revises:
Create Date: 2024-01-01
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])

def downgrade():
    op.drop_table("users")
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **Dependency Injection** | FastAPI's mechanism for providing shared resources (DB sessions, auth) to route handlers via `Depends()` |
| **Pydantic** | Data validation library using Python type annotations; FastAPI's default for request/response models |
| **Async/await** | Python concurrency model for non-blocking I/O; essential for high-throughput FastAPI apps |
| **Middleware** | Components that process requests before/after route handlers (CORS, auth, logging) |
| **OpenAPI** | Specification standard for describing REST APIs; FastAPI generates it automatically |
| **Lifespan** | FastAPI startup/shutdown context manager replacing deprecated `on_event` decorators |
| **Connection Pool** | Pre-allocated database connections reused across requests to avoid connection overhead |
| **Rate Limiting** | Controlling request frequency per client/IP to prevent abuse |
| **Structured Logging** | Machine-parseable JSON logs with consistent fields for log aggregation |
| **Health Check** | Endpoint verifying application and dependency readiness for load balancers |

---

## Changelog

### 2.0.0 (2024-12-01)

- Added Pydantic v2 migration patterns and configuration
- Updated SQLAlchemy 2.0 async session management
- Added structured logging with structlog
- Added Prometheus metrics middleware
- Expanded Kubernetes deployment guide
- Added comprehensive testing strategy

### 1.1.0 (2024-06-15)

- Added rate limiting patterns
- Added Redis caching integration
- Added security headers middleware
- Updated authentication patterns

### 1.0.0 (2024-01-01)

- Initial release
- Core FastAPI patterns
- Basic dependency injection
- OpenAPI documentation

---

## Contributing Guidelines

1. Fork the repository and create a feature branch
2. Follow the existing code style and patterns
3. Add tests for new patterns (target: 90% coverage)
4. Update this document for any new patterns or changes
5. Run `ruff check` and `ruff format` before committing
6. Submit a pull request with a clear description

### Code Style

- Use `ruff` for linting and formatting
- Follow PEP 8 naming conventions
- Use type hints everywhere
- Keep functions under 30 lines
- Maximum line length: 88 characters

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---
name: Backend Architecture Agent
category: agents
difficulty: advanced
time_estimate: "6-8 hours"
dependencies: ["backend", "database", "security", "devops"]
tags: ["backend", "architecture", "api-design", "microservices", "scalability", "security"]
grok_personality: "backend-architect"
description: "Expert backend architect that designs scalable, secure, and efficient server-side systems"
version: "2.0.0"
author: "Awesome Grok Skills"
---

# Backend Architecture Agent

## Overview

Grok, you'll act as a backend architecture expert that designs robust, scalable, and efficient server-side systems. This agent specializes in API design, database architecture, microservices, and backend best practices.

### Core Competencies

**System Design**
- Microservices architecture
- Monolithic architecture
- Serverless architecture
- Event-driven architecture
- Layered architecture
- Hexagonal architecture

**API Design**
- RESTful API design
- GraphQL schema design
- API versioning strategies
- Rate limiting and throttling
- Authentication and authorization
- API documentation (OpenAPI/Swagger)

**Database Architecture**
- Relational database design (PostgreSQL, MySQL)
- NoSQL data modeling (MongoDB, Cassandra)
- Database indexing strategies
- Query optimization
- Data migration strategies
- Replication and sharding
- ACID compliance

**Performance & Scalability**
- Caching strategies (Redis, Memcached)
- Load balancing
- Horizontal vs vertical scaling
- Performance monitoring
- Bottleneck analysis
- Capacity planning
- CDN integration

**Security**
- Authentication (JWT, OAuth2, API Keys)
- Authorization (RBAC, ABAC)
- Input validation and sanitization
- SQL injection prevention
- XSS prevention
- Rate limiting
- Data encryption
- Secret management

**DevOps & Deployment**
- CI/CD pipelines
- Docker containerization
- Kubernetes orchestration
- Infrastructure as Code (Terraform, CloudFormation)
- Monitoring and observability
- Logging strategies
- Health checks

## Agent Capabilities

### 1. API Design

**RESTful API Design**
- Resource-oriented URL design
- HTTP method semantics (GET, POST, PUT, DELETE, PATCH)
- Status code usage (200, 201, 400, 401, 403, 404, 500, etc.)
- Request/response formatting
- Pagination strategies
- Filtering and sorting
- HATEOAS (Hypermedia as the Engine of Application State)

**GraphQL Schema Design**
- Type definitions
- Query and mutation design
- Subscription support
- Input and payload types
- Interface and union types
- Custom directives
- Resolver implementation
- DataLoader for N+1 prevention

**API Versioning**
- URL path versioning (/v1/, /v2/)
- Header versioning (X-API-Version)
- Query parameter versioning (?version=1)
- Deprecation strategies
- Backward compatibility

**Rate Limiting**
- Token bucket algorithm
- Sliding window algorithm
- Fixed window algorithm
- Rate limit headers (X-RateLimit-Limit, X-RateLimit-Remaining)
- Rate limit exceeded responses (429 Too Many Requests)

**Authentication & Authorization**
- JWT (JSON Web Tokens)
- OAuth2 flows (Authorization Code, Client Credentials)
- API keys
- Session-based authentication
- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)

**API Documentation**
- OpenAPI 3.0 specification
- Swagger UI integration
- Request/response examples
- Error code documentation
- Authentication documentation

### 2. Database Architecture

**Schema Design**
- Entity relationship modeling
- Normalization (1NF, 2NF, 3NF, BCNF)
- Denormalization for performance
- Primary and foreign keys
- Unique constraints
- Check constraints

**Indexing Strategies**
- Primary key indexes (clustered)
- Secondary indexes (non-clustered)
- Composite indexes
- Partial indexes
- Full-text search indexes
- Index usage analysis
- Index maintenance

**Query Optimization**
- Query execution plan analysis
- JOIN optimization
- Subquery optimization
- Index usage verification
- Query caching
- Prepared statements
- Connection pooling

**Data Migration**
- Schema migrations
- Data migrations
- Zero-downtime migrations
- Rollback strategies
- Migration testing
- Migration tools (Alembic, Flyway, Liquibase)

**Replication & Sharding**
- Master-slave replication
- Multi-master replication
- Read replicas
- Horizontal sharding
- Vertical sharding
- Sharding key selection

**NoSQL Data Modeling**
- Document modeling (MongoDB)
- Key-value modeling (Redis, DynamoDB)
- Column-family modeling (Cassandra)
- Graph modeling (Neo4j)
- Time-series modeling (InfluxDB)

### 3. Microservices Architecture

**Service Decomposition**
- Domain-Driven Design (DDD)
- Bounded contexts
- Service responsibility definition
- Service size guidelines
- Team ownership alignment

**Inter-Service Communication**
- Synchronous (HTTP/REST, gRPC)
- Asynchronous (message queues, event streaming)
- Service mesh (Istio, Linkerd)
- API gateway patterns
- Service discovery

**Service Discovery**
- Client-side discovery
- Server-side discovery
- Service registry (Consul, Eureka, etcd)
- Health checking
- Load balancing

**API Gateway**
- Request routing
- Authentication/authorization
- Rate limiting
- Request/response transformation
- Caching
- Circuit breaking

**Distributed Transactions**
- Two-phase commit (2PC)
- Three-phase commit (3PC)
- Saga pattern
- Eventual consistency
- Compensation transactions

**Event-Driven Architecture**
- Event publishing/subscription
- Event sourcing
- CQRS (Command Query Responsibility Segregation)
- Message brokers (RabbitMQ, Kafka)
- Event streams

### 4. Performance & Scalability

**Caching Strategies**
- Application-level caching
- Database query caching
- CDN caching
- Cache invalidation strategies
- Cache warming
- Distributed caching (Redis Cluster)

**Load Balancing**
- Round-robin
- Weighted round-robin
- Least connections
- IP hash
- Least response time
- Health-based routing

**Horizontal Scaling**
- Stateless service design
- Session management
- Database scaling
- Cache scaling
- Message queue scaling

**Vertical Scaling**
- Resource optimization
- Performance profiling
- Bottleneck identification
- Capacity planning

**Database Performance**
- Query optimization
- Index optimization
- Connection pooling
- Read replicas
- Database sharding
- Partitioning

**Application Performance**
- Async/await patterns
- Connection pooling
- Request batching
- Response compression
- Lazy loading
- Code profiling

### 5. Security

**Authentication**
- JWT implementation
- OAuth2 flows
- API key management
- Session management
- Multi-factor authentication
- Single sign-on (SSO)

**Authorization**
- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)
- Policy-based access control
- Permission management
- Resource ownership

**Input Validation**
- Request validation
- Schema validation
- Type checking
- Range validation
- Format validation
- Sanitization

**Output Encoding**
- XSS prevention
- CSRF protection
- SQL injection prevention
- Command injection prevention
- Path traversal prevention

**Data Protection**
- Encryption at rest
- Encryption in transit (TLS)
- Data masking
- Data anonymization
- PII protection
- GDPR compliance

**Secret Management**
- Environment variables
- Secret management systems (Vault, AWS Secrets Manager)
- Secret rotation
- Secret scanning
- Access control for secrets

**Security Monitoring**
- Audit logging
- Intrusion detection
- Anomaly detection
- Security event monitoring
- Incident response

## Architecture Framework

### 1. API Design Template

```yaml
# RESTful API specification template
api_specification:
  base_url: "https://api.example.com/v1"
  versioning: "url_path"
  
  authentication:
    type: "bearer_token"
    token_source: "jwt"
    refresh_endpoint: "/auth/refresh"
    expiration: 3600
  
  rate_limiting:
    default: "1000 requests/hour"
    authenticated: "5000 requests/hour"
    algorithm: "token_bucket"
    headers:
      limit: "X-RateLimit-Limit"
      remaining: "X-RateLimit-Remaining"
      reset: "X-RateLimit-Reset"
  
  cors:
    allowed_origins: ["https://example.com"]
    allowed_methods: ["GET", "POST", "PUT", "DELETE"]
    allowed_headers: ["Content-Type", "Authorization"]
    max_age: 86400
  
  endpoints:
    users:
      list:
        method: "GET"
        path: "/users"
        query_params:
          - name: "page"
            type: "integer"
            required: false
            default: 1
          - name: "limit"
            type: "integer"
            required: false
            default: 10
        responses:
          200: "users_list"
          400: "bad_request"
          401: "unauthorized"
       
      get:
        method: "GET"
        path: "/users/{id}"
        path_params:
          - name: "id"
            type: "string"
            format: "uuid"
        responses:
          200: "user_detail"
          404: "not_found"
       
      create:
        method: "POST"
        path: "/users"
        request_body: "user_create"
        responses:
          201: "user_detail"
          400: "validation_error"
          409: "conflict"
```

### 2. Database Schema Design

```yaml
# Database schema template
database_schema:
  tables:
    users:
      columns:
        id:
          type: "uuid"
          primary_key: true
          default: "gen_random_uuid()"
          description: "Unique user identifier"
        
        email:
          type: "varchar(255)"
          unique: true
          not_null: true
          index: true
          description: "User email address"
        
        password_hash:
          type: "varchar(255)"
          not_null: true
          description: "Hashed password"
        
        name:
          type: "varchar(100)"
          not_null: true
          description: "User full name"
        
        created_at:
          type: "timestamp"
          default: "now()"
          description: "Record creation timestamp"
        
        updated_at:
          type: "timestamp"
          default: "now()"
          on_update: "now()"
          description: "Record update timestamp"
        
        deleted_at:
          type: "timestamp"
          nullable: true
          description: "Soft delete timestamp"
       
      indexes:
        - name: "idx_users_email"
          columns: ["email"]
          unique: true
          description: "Unique index for email lookups"
         
        - name: "idx_users_created"
          columns: ["created_at"]
          description: "Index for date-range queries"
    
    orders:
      columns:
        id:
          type: "uuid"
          primary_key: true
          default: "gen_random_uuid()"
        
        user_id:
          type: "uuid"
          foreign_key: "users(id)"
          not_null: true
          index: true
          description: "Reference to user"
        
        status:
          type: "varchar(50)"
          not_null: true
          default: "pending"
          enum: ["pending", "processing", "shipped", "delivered", "cancelled"]
          description: "Order status"
        
        total:
          type: "decimal(10,2)"
          not_null: true
          description: "Order total amount"
       
      indexes:
        - name: "idx_orders_user_id"
          columns: ["user_id"]
         
        - name: "idx_orders_status"
          columns: ["status"]
         
        - name: "idx_orders_created"
          columns: ["created_at"]
   
  relationships:
    - from: "orders"
      to: "users"
      type: "many_to_one"
      foreign_key: "user_id"
      on_delete: "CASCADE"
      description: "Orders belong to users"
```

### 3. Microservices Architecture

```yaml
# Microservices architecture template
microservices:
  services:
    user_service:
      description: "User management and authentication"
      responsibilities:
        - "user registration"
        - "authentication"
        - "user profile management"
        - "password reset"
      
      api:
        endpoints:
          - "POST /api/v1/users/register"
          - "POST /api/v1/auth/login"
          - "POST /api/v1/auth/refresh"
          - "GET /api/v1/users/{id}"
          - "PUT /api/v1/users/{id}"
          - "DELETE /api/v1/users/{id}"
      
      database:
        type: "postgresql"
        tables: ["users", "sessions", "permissions", "roles"]
      
      events:
        publishes:
          - "user.created"
          - "user.updated"
          - "user.deleted"
        subscribes:
          - "order.created"
          - "payment.succeeded"
      
      dependencies:
        - "notification_service"
        - "email_service"
    
    order_service:
      description: "Order management and processing"
      responsibilities:
        - "order creation"
        - "order management"
        - "payment processing"
        - "inventory management"
      
      api:
        endpoints:
          - "POST /api/v1/orders"
          - "GET /api/v1/orders/{id}"
          - "PATCH /api/v1/orders/{id}/status"
          - "GET /api/v1/orders"
      
      database:
        type: "postgresql"
        tables: ["orders", "order_items", "payments"]
      
      events:
        publishes:
          - "order.created"
          - "order.paid"
          - "order.shipped"
          - "order.delivered"
        subscribes:
          - "user.verified"
          - "payment.succeeded"
          - "inventory.updated"
      
      dependencies:
        - "user_service"
        - "payment_service"
        - "inventory_service"
    
    notification_service:
      description: "Multi-channel notification delivery"
      responsibilities:
        - "email notifications"
        - "SMS notifications"
        - "push notifications"
        - "notification preferences"
      
      api:
        endpoints:
          - "POST /api/v1/notifications/send"
          - "GET /api/v1/notifications/{id}"
          - "PUT /api/v1/notifications/preferences"
      
      events:
        subscribes:
          - "order.created"
          - "order.shipped"
          - "user.registered"
          - "payment.succeeded"
      
      dependencies:
        - "email_service"
        - "sms_service"
        - "push_service"
   
  infrastructure:
    api_gateway:
      provider: "kong"
      features:
        - "rate limiting"
        - "authentication"
        - "request logging"
        - "caching"
        - "circuit breaking"
      routes:
        - path: "/api/v1/users/*"
          service: "user_service"
        - path: "/api/v1/orders/*"
          service: "order_service"
        - path: "/api/v1/notifications/*"
          service: "notification_service"
    
    service_discovery:
      provider: "consul"
      features:
        - "service registration"
        - "health checking"
        - "load balancing"
    
    message_broker:
      provider: "rabbitmq"
      exchanges:
        - name: "orders"
          type: "topic"
        - name: "notifications"
          type: "fanout"
        - name: "users"
          type: "direct"
    
    monitoring:
      metrics: "prometheus"
      visualization: "grafana"
      alerting: "alertmanager"
      logging: "elk-stack"
    
    tracing:
      provider: "jaeger"
      sampling: "probabilistic"
      rate: 0.1
```

### 4. Performance & Scalability Template

```yaml
# Performance configuration
performance:
  caching:
    layers:
      - level: "cdn"
        provider: "cloudflare"
        ttl: 86400
        cache_static: true
      
      - level: "application"
        provider: "redis"
        ttl: 3600
        strategy: "lru"
        max_size: "10GB"
      
      - level: "database"
        provider: "postgresql"
        query_cache: true
        shared_buffers: "4GB"
    
    invalidation:
      strategy: "event-based"
      events:
        - "user.updated"
        - "order.created"
  
  database:
    connection_pool:
      min_size: 5
      max_size: 20
      timeout: 30
    
    queries:
      slow_query_log: true
      slow_query_threshold: 1000  # ms
      explain_analyze: true
    
    indexes:
      auto_create: false
      missing_indexes_report: true
  
  scaling:
    horizontal:
      min_instances: 2
      max_instances: 20
      target_cpu: 70
      target_memory: 80
    
    vertical:
      instance_type: "m5.large"
      cpu: 2
      memory: "8GB"
  
  load_balancing:
    algorithm: "round_robin"
    health_check:
      path: "/health"
      interval: 30
      timeout: 5
      healthy_threshold: 2
      unhealthy_threshold: 3
```

### 5. Security Configuration Template

```yaml
# Security configuration
security:
  authentication:
    primary: "jwt"
    secondary: "api_key"
    mfa:
      enabled: true
      methods: ["totp", "sms"]
  
  authorization:
    type: "rbac"
    roles:
      - name: "admin"
        permissions: ["*"]
      - name: "user"
        permissions: ["read:own", "write:own"]
      - name: "viewer"
        permissions: ["read:public"]
  
  encryption:
    at_rest:
      algorithm: "AES-256-GCM"
      key_rotation: 90  # days
    in_transit:
      protocol: "TLS 1.3"
      cipher_suites:
        - "TLS_AES_256_GCM_SHA384"
        - "TLS_CHACHA20_POLY1305_SHA256"
  
  input_validation:
    max_request_size: "10MB"
    max_json_depth: 10
    sanitize_html: true
    block_sql_injection: true
    block_xss: true
  
  rate_limiting:
    enabled: true
    default:
      requests: 100
      window: 60  # seconds
    authenticated:
      requests: 1000
      window: 60
    endpoints:
      - path: "/api/v1/auth/login"
        requests: 5
        window: 60
      - path: "/api/v1/auth/register"
        requests: 3
        window: 3600
  
  secrets:
    management: "vault"
    rotation:
      enabled: true
      interval: 90  # days
    scanning:
      enabled: true
      tools: ["gitleaks", "truffleHog"]
  
  logging:
    audit:
      enabled: true
      events:
        - "authentication.success"
        - "authentication.failure"
        - "authorization.failure"
        - "data.access"
        - "configuration.change"
    retention: 2555  # days (7 years)
```

## Quick Start Examples

### 1. RESTful API Implementation

```python
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime

app = FastAPI(
    title="User API",
    version="2.0.0",
    description="User management microservice"
)

# Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    name: str = Field(min_length=1, max_length=100)

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    page: int
    limit: int

# In-memory database (replace with real DB)
users_db = {}

@app.post("/api/v1/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    # Check if user exists
    for user in users_db.values():
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User already exists"
            )
    
    # Create user
    user_id = str(uuid.uuid4())
    user = {
        "id": user_id,
        "email": user_data.email,
        "name": user_data.name,
        "password_hash": hash_password(user_data.password),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    users_db[user_id] = user
    
    return UserResponse(**user)

@app.get("/api/v1/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse(**user)

@app.get("/api/v1/users", response_model=UserListResponse)
async def list_users(page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit
    
    users_list = list(users_db.values())[start:end]
    
    return UserListResponse(
        users=[UserResponse(**u) for u in users_list],
        total=len(users_db),
        page=page,
        limit=limit
    )

@app.put("/api/v1/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user_data: UserCreate):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user["email"] = user_data.email
    user["name"] = user_data.name
    user["updated_at"] = datetime.now()
    
    return UserResponse(**user)

@app.delete("/api/v1/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    user = users_db.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    del users_db[user_id]
    return None

def hash_password(password: str) -> str:
    """Hash password using SHA-256 (use bcrypt in production)"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()
```

### 2. Database Migration

```python
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('password_hash', sa.String(255), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()')),
        sa.Column('deleted_at', sa.TIMESTAMP(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    # Create indexes
    op.create_index('idx_users_email', 'users', ['email'], unique=True)
    op.create_index('idx_users_created', 'users', ['created_at'])
    
    # Create orders table
    op.create_table(
        'orders',
        sa.Column('id', postgresql.UUID(), nullable=False, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', postgresql.UUID(), nullable=False),
        sa.Column('total', sa.Numeric(10, 2), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, server_default='pending'),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_index('idx_orders_user_id', 'orders', ['user_id'])
    op.create_index('idx_orders_status', 'orders', ['status'])
    
    # Add foreign key
    op.create_foreign_key(
        'fk_orders_user_id',
        'orders', 'users',
        ['user_id'], ['id'],
        ondelete='CASCADE'
    )

def downgrade():
    # Drop foreign key
    op.drop_constraint('fk_orders_user_id', 'orders', type_='foreignkey')
    
    # Drop indexes
    op.drop_index('idx_orders_status', table_name='orders')
    op.drop_index('idx_orders_user_id', table_name='orders')
    op.drop_index('idx_users_created', table_name='users')
    op.drop_index('idx_users_email', table_name='users')
    
    # Drop tables
    op.drop_table('orders')
    op.drop_table('users')
```

### 3. Caching Strategy

```python
from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import redis
from typing import Optional

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis_client = redis.Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")

@app.get("/api/v1/products/{product_id}")
@cache(expire=60, namespace="products")
async def get_product(product_id: str):
    # Cache result for 60 seconds
    product = fetch_product_from_db(product_id)
    return product

@app.get("/api/v1/users/{user_id}")
@cache(expire=300, namespace="users")  # Cache for 5 minutes
async def get_user(user_id: str):
    user = fetch_user_from_db(user_id)
    return user

@app.delete("/api/v1/products/{product_id}")
async def update_product(product_id: str):
    # Invalidate cache when product is updated
    await FastAPICache.clear(namespace="products")
    # Update product in database
    return {"status": "updated"}
```

### 4. Circuit Breaker Implementation

```python
import time
from enum import Enum
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        half_open_requests: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_requests = half_open_requests
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == CircuitState.OPEN:
            if self._can_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _can_attempt_reset(self) -> bool:
        return (
            self.last_failure_time and
            time.time() - self.last_failure_time > self.recovery_timeout
        )
    
    def _on_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.half_open_requests:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        else:
            self.failure_count = 0
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

# Usage
circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)

def call_external_api():
    # This could fail
    pass

try:
    result = circuit_breaker.call(call_external_api)
except Exception as e:
    # Fallback behavior
    result = get_cached_data()
```

### 5. JWT Authentication

```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Configuration
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user(user_id)
    if user is None:
        raise credentials_exception
    
    return user

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```

## Best Practices

### API Design Best Practices

1. **Use RESTful conventions**: Proper HTTP methods (GET, POST, PUT, DELETE)
2. **Version your API**: Include version in URL path or header
3. **Use consistent naming**: Plural nouns for resources
4. **Implement pagination**: For large datasets (limit/offset or cursor)
5. **Use proper status codes**: Match HTTP semantics
6. **Document endpoints**: Use OpenAPI/Swagger
7. **Implement rate limiting**: Prevent abuse
8. **Use HTTPS**: Always encrypt in transit
9. **Implement idempotency**: For safe retries
10. **Provide error details**: Help clients debug

### Security Best Practices

1. **Always validate input**: Never trust user input
2. **Use parameterized queries**: Prevent SQL injection
3. **Hash passwords**: Use bcrypt or Argon2
4. **Use HTTPS**: TLS 1.3 or higher
5. **Implement rate limiting**: Prevent brute force
6. **Use JWT correctly**: Short expiration, secure storage
7. **Implement CORS properly**: Restrict origins
8. **Log security events**: Authentication, authorization, errors
9. **Encrypt sensitive data**: At rest and in transit
10. **Regular security audits**: Penetration testing, vulnerability scanning

### Database Best Practices

1. **Use migrations**: Version control your schema
2. **Index strategically**: Index frequently queried columns
3. **Avoid N+1 queries**: Use joins or batch loading
4. **Use connection pooling**: Manage connections efficiently
5. **Normalize appropriately**: Balance normalization vs performance
6. **Use soft deletes**: Preserve data history
7. **Audit changes**: Track who changed what and when
8. **Backup regularly**: Test restores
9. **Monitor performance**: Slow query logs
10. **Use transactions**: Ensure data consistency

### Performance Best Practices

1. **Cache aggressively**: Cache frequently accessed data
2. **Use CDN**: For static assets
3. **Optimize queries**: Use indexes, avoid complex joins
4. **Use async**: For I/O-bound operations
5. **Connection pooling**: For DB and external services
6. **Compress responses**: Gzip/Brotli
7. **Batch operations**: Reduce round trips
8. **Monitor performance**: Track metrics
9. **Load test**: Before production
10. **Profile regularly**: Identify bottlenecks

### Error Handling Best Practices

1. **Use specific exceptions**: Don't use generic Exception
2. **Include context**: Help debugging
3. **Log errors**: With stack traces
4. **Return appropriate status codes**: Match HTTP semantics
5. **Don't expose internals**: Sanitize error messages
6. **Implement retries**: With backoff for transient errors
7. **Use circuit breakers**: Prevent cascading failures
8. **Graceful degradation**: Fallback behavior
9. **Monitor errors**: Track error rates
10. **Alert on errors**: Notify on-call team

## Troubleshooting

### Common Issues

**Issue: High API latency**
- Check database query performance
- Verify cache hit rates
- Review network latency
- Check for N+1 queries
- Profile application code

**Issue: Database connection pool exhaustion**
- Increase pool size
- Check for connection leaks
- Reduce query execution time
- Use connection pooling correctly

**Issue: Circuit breaker always open**
- Check external service health
- Verify timeout configuration
- Review failure threshold
- Check fallback implementation

**Issue: Cache not working**
- Verify cache configuration
- Check cache key generation
- Review TTL settings
- Check cache invalidation logic

**Issue: Authentication failures**
- Verify JWT secret key
- Check token expiration
- Review token validation
- Check clock synchronization

## Integration with Other Skills

### Related Skills

- **fastapi-best-practices**: For FastAPI-specific patterns
- **security**: For secure authentication and authorization
- **testing**: For backend testing strategies
- **devops**: For deployment and infrastructure
- **database-design**: For database schema design
- **api-design**: For API design patterns
- **microservices**: For microservices architecture
- **performance**: For performance optimization

### Integration Points

**With Security Skill**
```python
# Use security skill for authentication
from skills.security import AuthenticationManager

auth = AuthenticationManager()
```

**With Testing Skill**
```python
# Use testing skill for test generation
from skills.testing import TestGenerator

test_gen = TestGenerator()
tests = test_gen.generate_tests(api_builder)
```

**With DevOps Skill**
```python
# Use devops skill for deployment
from skills.devops import DeploymentManager

deploy = DeploymentManager()
deploy.deploy(stack)
```

## Reference Materials

### Recommended Reading

- **Books**
  - "Designing Data-Intensive Applications" by Martin Kleppmann
  - "Building Microservices" by Sam Newman
  - "Clean Architecture" by Robert C. Martin
  - "The Phoenix Project" by Gene Kim

- **Documentation**
  - FastAPI: https://fastapi.tiangolo.com/
  - Express.js: https://expressjs.com/
  - PostgreSQL: https://www.postgresql.org/docs/
  - Redis: https://redis.io/docs/
  - GraphQL: https://graphql.org/learn/

- **Standards**
  - OpenAPI Specification: https://swagger.io/specification/
  - JSON Web Tokens: https://jwt.io/
  - OAuth 2.0: https://oauth.net/2/
  - HTTP Semantics: https://tools.ietf.org/html/rfc7231

### Tools

- **API Testing**: Postman, Insomnia, curl
- **Database**: pgAdmin, DBeaver, MongoDB Compass
- **Monitoring**: Prometheus, Grafana, Datadog
- **Logging**: ELK Stack, Splunk, CloudWatch
- **Deployment**: Docker, Kubernetes, Terraform

Remember: Good backend architecture is invisible to users but essential for scalability and maintainability. Design systems that are simple, secure, and performant. Always consider the trade-offs between complexity, performance, and maintainability.

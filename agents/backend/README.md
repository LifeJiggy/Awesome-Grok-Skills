# Backend Agent

Advanced backend development and API automation agent with comprehensive features for building scalable, secure, and maintainable server-side systems.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Backend Agent is a comprehensive toolkit for backend development that provides:

- **API Builder**: Multi-framework API generation (FastAPI, Express, Spring, Django, Flask, GraphQL)
- **Database Manager**: Advanced ORM model generation, migrations, and query building
- **Cache Manager**: Sophisticated caching with multiple strategies (LRU, LFU, TTL, FIFO)
- **Queue Manager**: Message queue operations with priority, delays, and dead-letter queues
- **GraphQL Generator**: Complete GraphQL schema and resolver generation
- **Authentication**: JWT-based authentication and authorization
- **API Gateway**: Routing, load balancing, and rate limiting
- **Service Registry**: Service discovery and health checking
- **Metrics**: Prometheus-compatible metrics collection
- **Circuit Breaker**: Fault tolerance and resilience patterns

## Features

### API Development

- Multi-framework support (FastAPI, Express, Spring Boot, Django, Flask, GraphQL)
- Automatic OpenAPI/Swagger specification generation
- Request/response schema validation
- Middleware support with priority ordering
- Rate limiting and throttling
- Authentication and authorization
- API versioning
- Comprehensive error handling
- Input validation and sanitization

### Database Operations

- Multi-database support (PostgreSQL, MySQL, SQLite, MongoDB)
- ORM model generation (SQLAlchemy, Django ORM, Mongoose)
- Automatic migration generation
- Relationship management (one-to-many, many-to-many, many-to-one)
- Connection pooling
- Query builder with filters, ordering, and pagination
- Index and constraint generation
- Database-agnostic schema definitions

### Caching

- Multiple caching strategies (LRU, LFU, TTL, FIFO)
- TTL-based expiration
- Pattern-based invalidation
- Cache statistics and hit rate monitoring
- Cache warming and preloading
- Distributed cache support

### Message Queuing

- Priority-based message queuing
- Delayed message delivery
- Visibility timeout for processing
- Dead-letter queues for failed messages
- Retry logic with configurable max retries
- Queue statistics and monitoring
- Worker management

### GraphQL

- Complete GraphQL schema generation
- Type, Query, Mutation, Subscription support
- Interface and Union types
- Custom directives
- Input type generation
- Resolver code generation (Python, JavaScript)

### Authentication & Authorization

- JWT token management
- Token creation, verification, and revocation
- Password hashing and verification
- Role-based access control (RBAC)
- API key support
- OAuth2 integration points
- Session management

### Observability

- Structured logging
- Metrics collection (counters, histograms, gauges)
- Prometheus export format
- Health checks with critical/non-critical designation
- Performance monitoring
- Request tracing

### Resilience

- Circuit breaker pattern implementation
- Retry logic with exponential backoff
- Timeout configuration
- Fallback behavior
- Bulkhead pattern
- Rate limiting

### Infrastructure

- API Gateway with routing and load balancing
- Service registry and discovery
- Health monitoring
- Load balancer strategies (round-robin, random)
- Docker and Docker Compose generation
- Multi-environment configuration

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills/agents/backend

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from agents.backend.agent import BackendAgent, APIFramework

# Initialize agent
agent = BackendAgent()

# Add API endpoints
agent.add_endpoint(
    "/users",
    "GET",
    "Get all users",
    params={
        "page": {"type": "integer", "required": False},
        "limit": {"type": "integer", "required": False}
    },
    response_schema={"type": "array", "items": {"type": "object"}},
    auth_required=True,
    rate_limit=100,
    cache_ttl=300,
    tags=["users"]
)

# Add database model
agent.db_manager.create_model(
    "User",
    {
        "name": "str",
        "email": "str",
        "age": "int"
    }
)

# Generate output
result = agent.run()
print(result)
```

### Run Demo

```bash
python agents/backend/agent.py
```

## Installation

### Prerequisites

- Python 3.9+
- pip package manager
- Virtual environment (recommended)

### Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install package in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### Dependencies

**Core:**
- Python 3.9+
- typing-extensions
- dataclasses
- pydantic (for validation)

**Optional:**
- fastapi (for FastAPI framework)
- express (Node.js, for Express framework)
- sqlalchemy (for database ORM)
- redis (for caching)
- pyjwt (for authentication)
- prometheus-client (for metrics)

## Usage

### Creating an API

```python
from agents.backend.agent import BackendAgent, APIFramework, ModelField

# Initialize with configuration
config = {
    "api": {
        "title": "User Service API",
        "version": "2.0.0",
        "description": "User management microservice"
    },
    "database": {
        "url": "postgresql://user:pass@localhost:5432/mydb"
    },
    "cache": {
        "type": "redis",
        "url": "redis://localhost:6379"
    }
}

agent = BackendAgent(config)

# Setup authentication
auth = agent.setup_auth(secret_key="your-secret-key")

# Define API endpoints
agent.add_endpoint(
    "/users",
    "GET",
    "List all users with pagination",
    params={
        "page": {"type": "integer", "required": False, "default": 1},
        "limit": {"type": "integer", "required": False, "default": 10},
        "sort": {"type": "string", "required": False, "default": "created_at"}
    },
    response_schema={
        "type": "object",
        "properties": {
            "users": {"type": "array"},
            "total": {"type": "integer"},
            "page": {"type": "integer"}
        }
    },
    auth_required=True,
    rate_limit=100,
    cache_ttl=300,
    tags=["users", "public"]
)

agent.add_endpoint(
    "/users/{id}",
    "GET",
    "Get user by ID",
    params={"id": {"type": "string", "required": True, "format": "uuid"}},
    response_schema={"type": "object"},
    auth_required=True,
    tags=["users"]
)

agent.add_endpoint(
    "/users",
    "POST",
    "Create new user",
    request_body={
        "type": "object",
        "properties": {
            "name": {"type": "string", "minLength": 1, "maxLength": 100},
            "email": {"type": "string", "format": "email"},
            "password": {"type": "string", "format": "password", "minLength": 8}
        },
        "required": ["name", "email", "password"]
    },
    response_schema={"type": "object"},
    auth_required=False,
    error_responses={
        "400": {"description": "Validation error"},
        "409": {"description": "User already exists"}
    },
    tags=["users", "admin"]
)

# Define database models
user_model = agent.db_manager.create_model(
    "User",
    [
        ModelField("id", "uuid", primary_key=True),
        ModelField("name", "str", max_length=100, required=True),
        ModelField("email", "str", max_length=255, unique=True, required=True),
        ModelField("password_hash", "str", max_length=255, required=True),
        ModelField("created_at", "datetime", default="NOW()"),
        ModelField("updated_at", "datetime", default="NOW()")
    ],
    indexes=[
        {"name": "idx_users_email", "columns": ["email"], "unique": True},
        {"name": "idx_users_created", "columns": ["created_at"]}
    ]
)

agent.db_manager.add_relationship("User", "one_to_many", "Order", "user_id")

# Setup circuit breakers
agent.add_circuit_breaker(
    "database",
    failure_threshold=5,
    recovery_timeout=60
)

# Add health checks
agent.add_health_check(
    "database",
    lambda: check_db_connection(),
    critical=True
)

# Generate full stack
stack = agent.generate_full_stack(APIFramework.FASTAPI)

# Run agent
result = agent.run()
```

### Database Operations

```python
# Create models with relationships
agent.db_manager.create_model(
    "Order",
    {
        "user_id": "uuid",
        "total": "decimal(10,2)",
        "status": "str"
    }
)

agent.db_manager.add_relationship(
    "Order",
    "many_to_one",
    "User",
    "user_id",
    on_delete="CASCADE"
)

# Generate migrations
migration_sql = agent.db_manager.generate_migrations("User")
print(migration_sql)

# Generate ORM models
models_code = agent.db_manager.generate_models(framework="sqlalchemy")
print(models_code)
```

### Caching

```python
# Set cache with TTL
agent.cache_manager.set("user:123", {"name": "John"}, ttl=3600)

# Get from cache
user = agent.cache_manager.get("user:123")

# Invalidate by pattern
agent.cache_manager.invalidate_pattern("user:.*")

# Get cache statistics
stats = agent.cache_manager.get_stats()
print(f"Hit rate: {stats['hit_rate']}%")
```

### Message Queuing

```python
# Add queue
agent.queue_manager.add_queue(
    "notifications",
    worker_count=5,
    max_retries=3,
    visibility_timeout=30
)

# Enqueue message with priority
agent.queue_manager.enqueue(
    "notifications",
    {
        "type": "email",
        "to": "user@example.com",
        "subject": "Welcome!"
    },
    priority=1
)

# Dequeue message
message = agent.queue_manager.dequeue("notifications")

# Acknowledge processing
agent.queue_manager.acknowledge("notifications", message["id"])

# Get queue stats
stats = agent.queue_manager.get_stats("notifications")
print(f"Pending: {stats['pending']}, Processed: {stats['processed']}")
```

### GraphQL

```python
# Define types
agent.graphql_generator.add_type(
    "User",
    {
        "id": "ID!",
        "name": "String!",
        "email": "String!",
        "orders": "[Order!]!"
    },
    description="User account"
)

# Add queries
agent.graphql_generator.add_query(
    "getUser",
    "User",
    "resolve_user",
    args={"id": "ID!"},
    description="Get user by ID"
)

# Add mutations
agent.graphql_generator.add_mutation(
    "createUser",
    "CreateUserInput!",
    "User!",
    "resolve_create_user",
    description="Create new user"
)

# Generate schema
schema = agent.graphql_generator.generate_schema()
print(schema)

# Generate resolvers
resolvers = agent.graphql_generator.generate_resolvers(framework="python")
```

### API Gateway

```python
# Configure routes
agent.api_gateway.add_route(
    "/api/users/*",
    "user-service",
    methods=["GET", "POST"],
    auth_required=True,
    rate_limit=100
)

# Configure load balancer
agent.api_gateway.add_load_balancer(
    "user-service",
    ["http://user-service-1:8001", "http://user-service-2:8001"],
    strategy="round_robin"
)

# Route request
target = agent.api_gateway.route("/api/users", "GET")
```

### Service Registry

```python
# Register services
agent.service_registry.register(
    "user-service",
    "localhost",
    8001,
    health_check=lambda: check_user_service(),
    metadata={"version": "1.0.0", "env": "production"}
)

# Discover service
service_url = agent.service_registry.discover("user-service")

# Check health
health = agent.service_registry.check_health("user-service")
```

### Metrics and Monitoring

```python
# Record metrics
agent.record_metric("request_duration", 0.125, tags={"endpoint": "/users"})
agent.metrics.increment("requests_total", tags={"method": "GET", "status": "200"})
agent.metrics.histogram("response_size", 1024, tags={"endpoint": "/users"})

# Export Prometheus metrics
prometheus_output = agent.export_metrics()
print(prometheus_output)

# Get metric stats
stats = agent.metrics.get_stats("request_duration")
print(f"P95: {stats['p95']}s")
```

## API Reference

### BackendAgent

Main orchestrator class that coordinates all components.

```python
class BackendAgent:
    def __init__(self, config: Dict = None)
    def add_endpoint(self, path, method, description, **kwargs) -> Endpoint
    def generate_openapi(self) -> Dict
    def generate_routes(self, framework: APIFramework) -> str
    def setup_auth(self, secret_key: str) -> AuthenticationManager
    def add_circuit_breaker(self, name: str, **kwargs) -> CircuitBreaker
    def add_health_check(self, name: str, check_func: Callable, critical: bool)
    def run_health_checks(self) -> Dict
    def record_metric(self, name: str, value: float, tags: Dict)
    def export_metrics(self) -> str
    def validate_api(self) -> List[Dict]
    def generate_full_stack(self, framework: APIFramework) -> Dict
    def generate_api_client(self, language: str) -> str
    def run(self) -> Dict
```

### APIBuilder

Build and generate API endpoints.

```python
class APIBuilder:
    def __init__(self, title: str, version: str, description: str)
    def add_middleware(self, name: str, func: Callable, priority: int) -> Middleware
    def add_endpoint(self, path, method, description, **kwargs) -> Endpoint
    def generate_openapi(self) -> Dict
    def generate_routes(self, framework: APIFramework) -> str
    def validate_endpoints(self) -> List[Dict]
    def export_to_collection(self, format: str) -> Dict
```

### DatabaseManager

Manage database models and operations.

```python
class DatabaseManager:
    def add_connection(self, name: str, db_type: str, connection_str: str, **kwargs)
    def create_model(self, name: str, fields: Union[Dict, List[ModelField]], **kwargs) -> Dict
    def add_relationship(self, model_name: str, relationship_type: str, target_model: str, **kwargs)
    def generate_migrations(self, model_name: str) -> str
    def generate_models(self, framework: str) -> str
    def generate_query_builder(self, model_name: str) -> str
```

### CacheManager

Manage caching operations.

```python
class CacheManager:
    def __init__(self, strategy: CacheStrategy, default_ttl: int)
    def get(self, key: str) -> Optional[Any]
    def set(self, key: str, value: Any, ttl: Optional[int])
    def invalidate(self, key: str)
    def invalidate_pattern(self, pattern: str)
    def clear(self)
    def get_stats(self) -> Dict
    def cleanup_expired(self)
```

### QueueManager

Manage message queues.

```python
class QueueManager:
    def add_queue(self, name: str, worker_count: int, max_retries: int, visibility_timeout: int)
    def enqueue(self, queue_name: str, message: Dict, priority: int, delay: int) -> bool
    def dequeue(self, queue_name: str, visibility_timeout: Optional[int]) -> Optional[Dict]
    def acknowledge(self, queue_name: str, message_id: str) -> bool
    def reject(self, queue_name: str, message_id: str, requeue: bool)
    def get_stats(self, queue_name: str) -> Dict
    def purge(self, queue_name: str) -> int
```

## Examples

### Example 1: REST API with FastAPI

```python
from agents.backend.agent import BackendAgent, APIFramework, ModelField

agent = BackendAgent(config={"api": {"title": "Blog API", "version": "1.0.0"}})

# Posts endpoint
agent.add_endpoint(
    "/posts",
    "GET",
    "List all blog posts",
    params={"page": {"type": "integer"}, "limit": {"type": "integer"}},
    response_schema={"type": "array"},
    auth_required=False,
    cache_ttl=600,
    tags=["posts"]
)

agent.add_endpoint(
    "/posts",
    "POST",
    "Create new post",
    request_body={
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "content": {"type": "string"},
            "author_id": {"type": "string"}
        },
        "required": ["title", "content", "author_id"]
    },
    response_schema={"type": "object"},
    auth_required=True,
    tags=["posts"]
)

# Models
agent.db_manager.create_model(
    "Post",
    [
        ModelField("id", "uuid", primary_key=True),
        ModelField("title", "str", max_length=200, required=True),
        ModelField("content", "text", required=True),
        ModelField("author_id", "uuid", required=True),
        ModelField("published", "bool", default=False)
    ]
)

# Generate FastAPI code
fastapi_code = agent.generate_routes(APIFramework.FASTAPI)
print(fastapi_code)
```

### Example 2: Express.js API

```python
from agents.backend.agent import BackendAgent, APIFramework

agent = BackendAgent(config={"api": {"title": "Node API", "version": "1.0.0"}})

# Add endpoints
agent.add_endpoint("/api/products", "GET", "List products", tags=["products"])
agent.add_endpoint("/api/products", "POST", "Create product", tags=["products"])
agent.add_endpoint("/api/products/{id}", "GET", "Get product", tags=["products"])

# Generate Express routes
express_code = agent.generate_routes(APIFramework.EXPRESS)
print(express_code)
```

### Example 3: Microservices Architecture

```python
from agents.backend.agent import BackendAgent

# User Service
user_service = BackendAgent(config={"service": {"name": "user-service", "port": 8001}})
user_service.add_endpoint("/health", "GET", "Health check")
user_service.add_endpoint("/users", "POST", "Create user")

# Order Service
order_service = BackendAgent(config={"service": {"name": "order-service", "port": 8002}})
order_service.add_endpoint("/orders", "POST", "Create order")

# Register services
user_service.service_registry.register("user-service", "localhost", 8001)
order_service.service_registry.register("order-service", "localhost", 8002)

# Gateway routes
gateway = APIGateway()
gateway.add_route("/api/users/*", "user-service")
gateway.add_route("/api/orders/*", "order-service")
```

### Example 4: Full Stack Generation

```python
from agents.backend.agent import BackendAgent, APIFramework

agent = BackendAgent()

# Configure API
agent.add_endpoint("/api/users", "GET", "Get users")
agent.add_endpoint("/api/users", "POST", "Create user")

# Configure database
agent.db_manager.create_model("User", {"name": "str", "email": "str"})

# Generate complete stack
stack = agent.generate_full_stack(APIFramework.FASTAPI)

# Save generated files
with open("routes.py", "w") as f:
    f.write(stack["routes"])

with open("requirements.txt", "w") as f:
    f.write(stack["requirements"])

with open("docker-compose.yml", "w") as f:
    f.write(stack["docker_compose"])
```

## Configuration

### Agent Configuration

```yaml
api:
  title: "My API"
  version: "1.0.0"
  description: "API description"
  base_path: "/api/v1"

auth:
  type: "jwt"
  secret_key: "your-secret-key"
  algorithm: "HS256"
  expiration: 3600

database:
  type: "postgresql"
  url: "postgresql://user:pass@localhost:5432/mydb"
  pool_size: 5
  max_overflow: 10

cache:
  type: "redis"
  url: "redis://localhost:6379"
  strategy: "ttl"
  default_ttl: 3600

queue:
  type: "rabbitmq"
  url: "amqp://localhost:5672"

rate_limiting:
  default_limit: 100
  window: 60

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Environment Variables

```bash
# API Configuration
API_TITLE=My API
API_VERSION=1.0.0
API_BASE_PATH=/api/v1

# Authentication
AUTH_SECRET_KEY=your-secret-key
AUTH_ALGORITHM=HS256
AUTH_EXPIRATION=3600

# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
DATABASE_POOL_SIZE=5

# Cache
CACHE_URL=redis://localhost:6379
CACHE_TTL=3600

# Queue
QUEUE_URL=amqp://localhost:5672

# Rate Limiting
RATE_LIMIT_DEFAULT=100
RATE_LIMIT_WINDOW=60

# Logging
LOG_LEVEL=INFO
```

## Best Practices

### API Design

1. **Use RESTful conventions**: Proper HTTP methods (GET, POST, PUT, DELETE)
2. **Version your API**: Include version in URL path or header
3. **Use consistent naming**: Plural nouns for resources ( `/users`, `/posts`)
4. **Implement pagination**: For large datasets
5. **Use proper status codes**: 200, 201, 400, 401, 403, 404, 500
6. **Document endpoints**: Use OpenAPI/Swagger

### Security

1. **Always use HTTPS**: Never transmit sensitive data over HTTP
2. **Implement authentication**: Use JWT or OAuth2
3. **Validate all inputs**: Never trust user input
4. **Use parameterized queries**: Prevent SQL injection
5. **Implement rate limiting**: Prevent abuse
6. **Hash passwords**: Use bcrypt or Argon2
7. **Encrypt sensitive data**: At rest and in transit

### Database

1. **Use migrations**: Version control your schema
2. **Index strategically**: Index frequently queried fields
3. **Normalize appropriately**: Balance normalization vs performance
4. **Use connection pooling**: Manage database connections efficiently
5. **Implement soft deletes**: Preserve data history

### Caching

1. **Cache appropriately**: Cache frequently accessed, rarely changed data
2. **Set appropriate TTLs**: Balance freshness vs performance
3. **Invalidate on updates**: Keep cache coherent
4. **Monitor hit rates**: Aim for > 80% hit rate
5. **Use cache warming**: Preload frequently accessed data

### Error Handling

1. **Use specific error types**: AuthenticationError, RateLimitError, etc.
2. **Include error details**: Message, code, stack trace (in development)
3. **Log errors**: With context for debugging
4. **Return appropriate status codes**: Match HTTP semantics
5. **Don't expose internals**: Sanitize error messages for production

### Testing

1. **Unit test all components**: Models, services, utilities
2. **Integration test APIs**: Test complete request/response cycle
3. **Test error paths**: Don't just test happy paths
4. **Use test databases**: Isolate test data
5. **Mock external services**: For reliable tests

### Performance

1. **Use connection pooling**: For database and external services
2. **Implement caching**: Reduce database load
3. **Use async operations**: For I/O-bound tasks
4. **Optimize queries**: Use indexes, avoid N+1 queries
5. **Monitor performance**: Track latency, throughput, errors

## Troubleshooting

### Common Issues

**Issue: Import errors**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python version
python --version  # Should be 3.9+
```

**Issue: Database connection errors**
```python
# Verify database URL
print(agent.config.get("database.url"))

# Test connection
agent.db_manager.add_connection("test", "postgresql", "postgresql://localhost:5432/test")
```

**Issue: Cache not working**
```python
# Check cache configuration
print(agent.cache_manager.get_stats())

# Verify cache key
print(agent.cache_manager.get("your-key"))
```

**Issue: Rate limiting too aggressive**
```python
# Adjust rate limit
agent.add_endpoint("/api/endpoint", "GET", "Description", rate_limit=200)
```

### Debug Mode

```python
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

# Initialize agent with debug
agent = BackendAgent(config={"logging": {"level": "DEBUG"}})
```

### Performance Profiling

```python
import cProfile
import pstats

# Profile agent execution
profiler = cProfile.Profile()
profiler.enable()

result = agent.run()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone repository
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills/agents/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
pylint agents/backend/agent.py
```

## License

MIT License - see LICENSE file for details.

## Support

- Documentation: [Link to documentation]
- Issues: [GitHub Issues]
- Discussions: [GitHub Discussions]
- Email: [support email]

## Changelog

### Version 2.0.0 (2026-06-05)

- Complete rewrite with comprehensive features
- Multi-framework support (FastAPI, Express, Spring, Django, Flask, GraphQL)
- Advanced database operations with ORM generation
- Sophisticated caching with multiple strategies
- Message queue with priority and retry support
- Complete GraphQL schema generation
- Authentication and authorization
- Circuit breaker pattern
- Metrics and monitoring
- API Gateway
- Service registry and discovery
- Health checks
- Docker and Docker Compose generation
- Multi-language API client generation

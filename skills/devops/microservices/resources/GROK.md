# Microservices

## Overview

Microservices is an architectural style that structures an application as a collection of loosely coupled, independently deployable services. This skill covers decomposition strategies, inter-service communication, resilience patterns, and operational considerations. Microservices enable scalability, flexibility, and faster development cycles compared to monolithic architectures.

## Core Capabilities

Service decomposition defines bounded contexts and domain boundaries for each service. API gateways provide unified entry points with routing, authentication, and rate limiting. Service mesh provides observability, security, and traffic management. Service discovery enables dynamic service location and health monitoring.

Circuit breakers prevent cascade failures when services are unavailable. Saga patterns manage distributed transactions across services. Event sourcing and CQRS enable flexible data management patterns. Container orchestration automates deployment and scaling.

## Usage Examples

```python
from microservices import Microservices

ms = Microservices()

ms.define_architecture(
    name="E-Commerce Platform",
    pattern="event-driven"
)

order_service = ms.create_service(
    service_name="order-service",
    domain="orders",
    responsibilities=["Order management", "Order history", "Order status"],
    technologies={"language": "python", "framework": "fastapi", "database": "postgresql"}
)

order_service.add_endpoint("/orders")
order_service.add_endpoint("/orders/{order_id}")
order_service.add_dependency("inventory-service", "sync")
order_service.add_dependency("payment-service", "sync")
order_service.add_event("order.created", "domain")
order_service.add_event("order.shipped", "domain")

inventory_service = ms.create_service(
    service_name="inventory-service",
    domain="inventory",
    responsibilities=["Stock management", "Reservation", "SKU tracking"],
    technologies={"language": "go", "database": "mongodb"}
)

api_gateway = ms.define_api_gateway(
    name="api-gateway",
    routes=[
        {"path": "/api/orders", "service": "order-service"},
        {"path": "/api/products", "product-service"},
        {"path": "/api/users", "user-service"}
    ],
    authentication={"type": "oauth2", "issuer": "auth-service"},
    rate_limiting={"requests_per_minute": 1000}
)

service_mesh = ms.define_service_mesh(
    name="service-mesh",
    mesh_type="istio",
    observability={"tracing": True, "metrics": True, "logging": True},
    security={"mtls": True, "authorization": True}
)

circuit_breaker = ms.define_circuit_breaker(
    service_name="payment-service",
    failure_threshold=5,
    reset_timeout_seconds=60
)

retry_policy = ms.define_retry_policy(
    service_name="payment-service",
    max_attempts=3,
    backoff_multiplier=2,
    max_backoff_ms=10000
)

saga = ms.define_saga_pattern(
    saga_name="order-creation",
    compensation_strategy="sequential"
)

ms.add_saga_step(saga, "step1", "order-service", "create_order", "cancel_order")
ms.add_saga_step(saga, "step2", "inventory-service", "reserve_inventory", "release_inventory")
ms.add_saga_step(saga, "step3", "payment-service", "process_payment", "refund_payment")

health_checks = ms.configure_health_checks(
    service_name="order-service",
    checks=[
        {"type": "liveness", "endpoint": "/health", "interval_seconds": 30},
        {"type": "readiness", "endpoint": "/ready", "interval_seconds": 10}
    ]
)

slo = ms.define_service_level_objectives(
    service_name="order-service",
    slo_config=[
        {"name": "availability", "target": 0.999, "window": "30d"},
        {"name": "latency_p99", "target": 200, "unit": "ms", "window": "7d"},
        {"name": "error_rate", "target": 0.001, "window": "1h"}
    ]
)

tracing = ms.configure_distributed_tracing(
    service_name="order-service",
    tracer="jaeger",
    sample_rate=0.01
)

deployment = ms.define_deployment_strategy(
    service_name="order-service",
    strategy="canary",
    canary_config={
        "initial_percentage": 5,
        "increment": 5,
        "pause_duration_minutes": 10,
        "metrics_based": True
    }
)

event_sourcing = ms.define_event_sourcing(
    service_name="order-service",
    event_store={"type": "kafka", "topic": "order-events"},
    snapshot_policy={"interval_events": 1000}
)

cqrs = ms.define_cqrs_pattern(
    service_name="order-service",
    read_model={"type": "projection", "refresh": "eventual"},
    write_model={"type": "aggregate"}
)
```

## Best Practices

Start with a monolith and extract services incrementally based on need. Design services around business capabilities, not technical layers. Make services independently deployable and scalable. Use asynchronous communication for better resilience.

Implement proper observability with distributed tracing, metrics, and logs. Set up circuit breakers and timeouts for all service calls. Define clear API contracts and version them carefully. Keep services small but not too granular to avoid distributed monoliths.

## Related Skills

- Container Orchestration (Kubernetes)
- Service Mesh (Istio)
- API Design (REST/GraphQL)
- Event-Driven Architecture (Kafka)

## Use Cases

E-commerce platforms decompose into order, inventory, payment, and user services. Streaming services use microservices for content delivery, recommendations, and user profiles. Financial systems separate trading, risk, and reporting services. Healthcare platforms isolate patient records, appointments, and billing.

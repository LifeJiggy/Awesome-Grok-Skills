---
name: "serverless"
category: "cloud"
version: "2.0.0"
tags: ["cloud", "serverless", "FaaS", "event-driven", "managed-services"]
---

# Serverless

## Overview

The Serverless module provides comprehensive guidance for designing, building, and operating serverless applications across cloud providers. It covers Function-as-a-Service (FaaS), Backend-as-a-Service (BaaS), event-driven architectures, serverless databases, API gateways, and serverless-first design patterns. The module addresses cold start optimization, cost modeling, testing strategies, and production operations.

This skill is essential for serverless architects, cloud-native developers, and teams adopting event-driven, serverless-first architectures.

## Core Capabilities

- **FaaS Platforms**: AWS Lambda, Azure Functions, Google Cloud Functions, and Cloudflare Workers patterns
- **Event-Driven Design**: EventBridge/Event Grid patterns, pub/sub architectures, and event sourcing
- **Serverless APIs**: API Gateway + Lambda patterns, AppSync GraphQL, and HTTP API design
- **Serverless Databases**: DynamoDB, Cosmos DB serverless, PlanetScale, Aurora Serverless, and Fauna
- **Orchestration**: Step Functions, Durable Functions, and workflow engines for multi-step processes
- **Cold Start Optimization**: Provisioned concurrency, connection pooling, and runtime optimization
- **Serverless Storage**: S3, Blob Storage, and file-based serverless patterns
- **Cost Modeling**: Pay-per-request pricing analysis, cost comparison vs containerized, and optimization

## Usage Examples

```python
from serverless import (
    ServerlessArchitect,
    ColdStartOptimizer,
    CostModeler,
    EventDrivenDesigner,
    ServerlessAPIBuilder,
)

# --- Architecture Design ---
architect = ServerlessArchitect()
arch = architect.design(
    workload="e-commerce-api",
    traffic_pattern="bursty",
    data_volume_gb=100,
    concurrent_users=10000,
)
print(f"Compute: {arch.compute_service}")
print(f"Database: {arch.database_service}")
print(f"Storage: {arch.storage_service}")
print(f"Est monthly cost: ${arch.estimated_cost:.0f}")

# --- Cold Start Optimization ---
optimizer = ColdStartOptimizer()
optimization = optimizer.optimize(
    runtime="python3.11",
    memory_mb=1024,
    package_size_mb=50,
    vpc_enabled=True,
    cold_start_ms=3000,
)
print(f"Optimized cold start: {optimization.optimized_ms:.0f}ms")
print(f"Techniques: {', '.join(optimization.techniques)}")

# --- Cost Modeling ---
modeler = CostModeler()
comparison = modeler.compare(
    requests_per_month=10_000_000,
    avg_duration_ms=200,
    memory_mb=256,
    alternative_instance="t3.medium",
)
print(f"Serverless: ${comparison.serverless_cost:.0f}/month")
print(f"EC2 equivalent: ${comparison.container_cost:.0f}/month")
print(f"Savings: ${comparison.savings:.0f}/month")

# --- Event-Driven Design ---
designer = EventDrivenDesigner()
design = designer.design_order_flow(
    steps=["validate", "process_payment", "fulfill", "notify"],
    error_handling="dead_letter_queue",
    saga_pattern=True,
)
print(f"Events: {design.event_count}")
print(f"Steps: {len(design.steps)}")

# --- Serverless API ---
api = ServerlessAPIBuilder()
spec = api.build_rest_api(
    name="orders-api",
    endpoints=[
        {"method": "POST", "path": "/orders", "handler": "create_order"},
        {"method": "GET", "path": "/orders/{id}", "handler": "get_order"},
        {"method": "PUT", "path": "/orders/{id}/status", "handler": "update_status"},
    ],
    auth="cognito",
    throttling=10000,
)
print(f"Endpoints: {len(spec.endpoints)}")
print(f"Auth: {spec.auth_type}")
```

## Best Practices

- Design functions to be idempotent — serverless platforms may retry failed invocations
- Minimize package size — include only required dependencies for faster cold starts
- Use provisioned concurrency for latency-sensitive production workloads
- Implement dead-letter queues for all async invocations to capture failures
- Use environment variables for configuration — never hardcode in function code
- Implement structured logging (JSON) for machine-parseable observability
- Set appropriate memory allocation — more memory = more CPU = faster execution
- Use API Gateway caching for frequently accessed, slow-to-generate responses
- Design for eventual consistency — serverless databases often have read-after-write lag
- Implement circuit breakers for external service calls to prevent cascade failures

## Related Modules

- **aws-architecture**: AWS serverless services and patterns
- **azure-services**: Azure Functions and Durable Functions patterns
- **gcp-platform**: Cloud Functions and Cloud Run patterns
- **multi-cloud**: Serverless patterns that work across providers

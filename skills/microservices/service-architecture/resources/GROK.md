# Microservices Agent

## Overview

The **Microservices Agent** provides comprehensive microservice architecture capabilities including service design, service mesh management, event-driven architecture, and chaos engineering. This agent enables building resilient, scalable distributed systems.

## Core Capabilities

### 1. Service Design
Design and architect microservices:
- **Service Boundaries**: Bounded context mapping
- **API Contracts**: Interface definition
- **Database per Service**: Data isolation patterns
- **Event Contracts**: Async communication
- **Scaling Strategies**: Horizontal/vertical

### 2. Service Mesh Management
Configure and manage service meshes:
- **Traffic Management**: Routing, load balancing
- **Security**: mTLS, access control
- **Observability**: Metrics, tracing, logging
- **Resiliency**: Retries, timeouts, circuit breakers
- **Policies**: Rate limiting, quotas

### 3. Event-Driven Architecture
Build event-driven systems:
- **Event Sourcing**: State as event sequence
- **CQRS**: Command Query Responsibility Segregation
- **Message Brokers**: Kafka, RabbitMQ, Pub/Sub
- **Saga Orchestration**: Distributed transactions
- **Dead Letter Queues**: Error handling

### 4. Chaos Engineering
Test system resilience:
- **Fault Injection**: Network delays, failures
- **Failure Modes**: Pod kill, CPU stress
- **Experiment Design**: Hypothesis-driven testing
- **Blast Radius**: Controlled experimentation
- **Recovery Testing**: Failover verification

## Usage Examples

### Design Service

```python
from microservices import ServiceDesigner

designer = ServiceDesigner()
service = designer.design_service(
    name='orders',
    bounded_context='order-management',
    capabilities=['create', 'list', 'cancel', 'track']
)
api = designer.define_api_contract('orders', [
    {'method': 'GET', 'path': '/orders', 'summary': 'List orders'},
    {'method': 'POST', 'path': '/orders', 'summary': 'Create order'}
])
scaffold = designer.generate_service_scaffold(
    ServiceDefinition(
        service_name='orders',
        language='python',
        framework='fastapi',
        dependencies=['database', 'cache'],
        ports=[8080]
    )
)
```

### Service Mesh (Istio)

```python
from microservices import ServiceMeshManager

mesh = ServiceMeshManager()
istio = mesh.install_istio('1.18')
virtual_service = mesh.configure_virtual_service(
    'orders-service',
    'orders',
    [{'route': {'destination': {'host': 'orders-v2'}}, 'weight': 50}]
)
mtls = mesh.setup_mtls('orders', 'STRICT')
circuit_breaker = mesh.configure_circuit_breaker(
    'orders-cb',
    {'connections': 100, 'pending': 1000}
)
```

### Event-Driven Architecture

```python
from microservices import EventDrivenArchitecture

events = EventDrivenArchitecture()
topic = events.create_topic('orders', partitions=6, replication=3)
published = events.publish_event('orders', 'order.created', {'order_id': '123'})
consumer_group = events.create_consumer_group('order-processors', ['orders'])
saga = events.setup_saga_orchestration(
    'order-saga',
    steps=[
        {'name': 'validate', 'compensation': 'validate_undo'},
        {'name': 'reserve', 'compensation': 'reserve_undo'},
        {'name': 'ship', 'compensation': 'ship_undo'}
    ]
)
```

### API Gateway

```python
from microservices import APIGatewayManager

gateway = APIGatewayManager()
api = gateway.create_api('orders-api', '/api/v1/orders')
route = gateway.configure_route(
    '/orders/{id}',
    'orders-service',
    ['GET', 'PUT', 'DELETE']
)
auth = gateway.configure_auth(api['api'], 'jwt')
rate_limit = gateway.configure_rate_limiting(api['api'], 100)
```

### Chaos Engineering

```python
from microservices import ChaosEngineering

chaos = ChaosEngineering()
experiment = chaos.design_experiment(
    target='orders-service',
    fault='pod_kill',
    duration=60
)
network_delay = chaos.inject_network_delay('orders', delay_ms=100)
failure = chaos.inject_failure('orders', 'abort')
results = chaos.run_experiment(experiment['experiment'])
```

## Service Patterns

### Communication Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| REST | HTTP-based API | Synchronous calls |
| gRPC | High-performance RPC | Internal services |
| GraphQL | Flexible queries | Frontend APIs |
| Message Queue | Async messaging | Event-driven |
| Serverless | Function as service | Event processing |

### Data Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Database per Service | Isolated data | Full ownership |
| Saga | Distributed transactions | Multi-service operations |
| CQRS | Read/Write separation | Complex domains |
| Event Sourcing | Event log | Audit trails |

## Service Mesh Features

### Istio Capabilities
- **Virtual Services**: Traffic routing
- **Destination Rules**: Load balancing, subsets
- **Gateways**: Ingress/egress control
- **mTLS**: Automatic encryption
- **Circuit Breaking**: Failure isolation
- **Retries**: Automatic retry with backoff

### Traffic Management
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: orders
spec:
  hosts:
  - orders
  http:
  - route:
    - destination:
        host: orders
        subset: v2
      weight: 90
    - destination:
        host: orders
        subset: v1
      weight: 10
```

## Event-Driven Patterns

### Event Sourcing
```
Command → Event → State
┌──────────┐    ┌──────────┐    ┌──────────┐
│ Create   │───▶│ Order    │───▶│ Order    │
│ Order    │    │ Created  │    │ State    │
└──────────┘    └──────────┘    └──────────┘
```

### Saga Pattern
```
┌──────────────────────────────────────────────────┐
│                 Order Saga                        │
├──────────────────────────────────────────────────┤
│  1. Validate Order                                │
│  2. Reserve Inventory ──┬─ Compensation ──► Undo │
│  3. Process Payment  ───┴─ Compensation ──► Refund│
│  4. Confirm Order                               │
└──────────────────────────────────────────────────┘
```

## Chaos Engineering Experiments

### Common Faults
| Fault | Description | Target |
|-------|-------------|--------|
| Pod Kill | Delete pods | Kubernetes |
| Network Delay | Add latency | Network |
| CPU Stress | Consume CPU | Nodes |
| Memory Stress | Consume memory | Nodes |
| DNS Error | Fail DNS | Services |
| AWS Failure | Simulate AWS issues | Cloud |

### Experiment Design
1. **Define Steady State**: Normal operation metrics
2. **Hypothesis**: Expected behavior under fault
3. **Introduce Fault**: Apply the fault
4. **Measure**: Observe system response
5. **Analyze**: Compare to hypothesis
6. **Remediate**: Fix identified issues

## Service Discovery

### Discovery Patterns
- **Client-Side Discovery**: Client finds services
- **Server-Side Discovery**: Load balancer finds services
- **Service Registry**: Central service directory

### Health Checking
- **Active Checks**: Periodic health probes
- **Passive Checks**: Observe traffic health
- **Custom Checks**: Application-specific health

## Use Cases

### 1. E-Commerce Platform
- User service
- Product catalog
- Order management
- Payment processing
- Inventory tracking

### 2. Banking System
- Account management
- Transaction processing
- Fraud detection
- Notification service
- Regulatory reporting

### 3. Streaming Platform
- User authentication
- Content catalog
- Streaming engine
- Recommendation engine
- Analytics pipeline

## Related Skills

- [Infrastructure as Code](../iac/terraform-cloudformation/README.md) - Deployment
- [Observability](../observability/monitoring/README.md) - Monitoring
- [Zero Trust Architecture](../zero-trust/security-framework/README.md) - Security

---

**File Path**: `skills/microservices/service-architecture/resources/microservices.py`

---
name: "event-driven"
category: "microservices"
version: "2.0.0"
tags: ["microservices", "event-driven", "kafka", "messaging", "cqrs"]
description: "Event-driven architecture patterns for microservices"
---

# Event-Driven Architecture

## Overview

The Event-Driven Architecture module provides patterns and tools for implementing event-driven microservices. It covers event sourcing, CQRS, message brokers, saga patterns, and event schemas for building loosely coupled, scalable systems.

## Core Capabilities

- **Event Sourcing**: Store state changes as event sequences
- **CQRS**: Separate read and write models
- **Message Brokers**: Kafka, RabbitMQ, NATS integration
- **Saga Patterns**: Choreography and orchestration sagas
- **Event Schemas**: Schema registry and evolution
- **Event Handlers**: Configure event processing pipelines
- **Dead Letter Queues**: Handle failed event processing
- **Event Replay**: Replay events for debugging and recovery

## Usage Examples

### Event Definition

```python
from event_driven import Event, EventSchema

# Define event
order_created = Event(
    type="OrderCreated",
    source="order-service",
    data={
        "order_id": "ORD-001",
        "customer_id": "CUST-001",
        "items": [{"product_id": "PROD-001", "quantity": 2}],
        "total": 99.99,
    },
    schema_version="1.0",
)

print(f"Event: {order_created.type}")
print(f"  Source: {order_created.source}")
print(f"  ID: {order_created.event_id}")
```

### Event Store

```python
from event_driven import EventStore

store = EventStore()

# Append event
store.append(order_created)

# Read events
events = store.read_stream("OrderCreated", stream_id="ORD-001")
print(f"Events: {len(events)}")
```

### Saga Pattern

```python
from event_driven import Saga, SagaStep, SagaStatus

saga = Saga(
    name="OrderProcessing",
    steps=[
        SagaStep(action="reserve_inventory", compensation="release_inventory"),
        SagaStep(action="process_payment", compensation="refund_payment"),
        SagaStep(action="ship_order", compensation="cancel_shipment"),
    ],
)

# Execute saga
result = saga.execute(context={"order_id": "ORD-001"})
print(f"Saga: {result.status}")
print(f"  Steps Completed: {result.completed_steps}")
```

### CQRS

```python
from event_driven import CommandBus, QueryBus, EventBus

command_bus = CommandBus()
query_bus = QueryBus()
event_bus = EventBus()

# Register handlers
command_bus.register("CreateOrder", create_order_handler)
query_bus.register("GetOrder", get_order_handler)
event_bus.subscribe("OrderCreated", order_created_handler)
```

## Best Practices

- **Event Immutability**: Events should be immutable
- **Event Versioning**: Plan for event schema evolution
- **Idempotency**: Design event handlers to be idempotent
- **Event Ordering**: Consider event ordering requirements
- **Error Handling**: Implement dead letter queues
- **Event Documentation**: Document event schemas
- **Event Monitoring**: Monitor event flow and processing
- **Event Security**: Secure event data

## Related Modules

- **distributed-tracing**: Trace events across services
- **service-mesh**: Mesh for event routing
- **service-architecture**: Service design for events

## Advanced Configuration

### Event Store Configuration

```python
from event_driven import EventStoreConfig, StorageBackend

config = EventStoreConfig(
    # Storage backends
    backends={
        StorageBackend.POSTGRES: {
            "description": "PostgreSQL event store",
            "features": ["transactions", "json_support", "full_text_search"],
            "use_case": "small_to_medium_scale",
        },
        StorageBackend.MONGODB: {
            "description": "MongoDB event store",
            "features": ["flexible_schema", "horizontal_scaling", "aggregation"],
            "use_case": "document_oriented",
        },
        StorageBackend.EVENTSTOREDB: {
            "description": "EventStoreDB",
            "features": ["native_event_sourcing", "projections", "subscriptions"],
            "use_case": "event_sourcing_native",
        },
        StorageBackend.KAFKA: {
            "description": "Apache Kafka as event store",
            "features": ["high_throughput", "retention", "compaction"],
            "use_case": "high_volume_streaming",
        },
    },
    # Event storage settings
    storage={
        "max_event_size": "1MB",
        "compression": True,
        "encryption": True,
        "retention_days": 365,
    },
    # Snapshot settings
    snapshots={
        "enabled": True,
        "interval": 100,  # events
        "max_snapshots": 10,
    },
)

event_store = EventStore(config)
```

### Message Broker Configuration

```python
from event_driven import BrokerConfig, BrokerType

broker_config = BrokerConfig(
    # Broker types
    brokers={
        BrokerType.KAFKA: {
            "description": "Apache Kafka",
            "features": ["high_throughput", "ordering", "retention"],
            "use_case": "event_streaming",
            "components": ["broker", "zookeeper", "schema_registry"],
        },
        BrokerType.RABBITMQ: {
            "description": "RabbitMQ",
            "features": ["routing", "acknowledgments", "priority"],
            "use_case": "traditional_messaging",
            "components": ["broker", "management_ui"],
        },
        BrokerType.NATS: {
            "description": "NATS",
            "features": ["lightweight", "fast", "clustering"],
            "use_case": "microservices_messaging",
            "components": ["nats_server", "jetstream"],
        },
        BrokerType.REDIS: {
            "description": "Redis Streams",
            "features": ["in_memory", "pub_sub", "consumer_groups"],
            "use_case": "lightweight_streaming",
        },
    },
    # Kafka-specific configuration
    kafka={
        "bootstrap_servers": ["localhost:9092"],
        "schema_registry": "http://localhost:8081",
        "num_partitions": 6,
        "replication_factor": 3,
        "retention_ms": 604800000,  # 7 days
        "cleanup_policy": "delete",
    },
    # RabbitMQ-specific configuration
    rabbitmq={
        "host": "localhost",
        "port": 5672,
        "virtual_host": "/",
        "heartbeat": 60,
        "prefetch_count": 10,
    },
)

broker = MessageBroker(broker_config)
```

### CQRS Configuration

```python
from event_driven import CQRSConfig, ProjectionType

cqrS_config = CQRSConfig(
    # Projection types
    projections={
        ProjectionType.READ_MODEL: {
            "description": "Denormalized read model",
            "update_strategy": "real_time",
            "use_case": "query_optimization",
        },
        ProjectionType.PROJECTION: {
            "description": "Event projection",
            "update_strategy": "event_driven",
            "use_case": "materialized_views",
        },
        ProjectionType.SUBSCRIPTION: {
            "description": "Event subscription",
            "update_strategy": "catch_up",
            "use_case": "event_processors",
        },
    },
    # Command/Query separation
    separation={
        "command_model": {
            "database": "write_db",
            "optimization": "consistency",
        },
        "query_model": {
            "database": "read_db",
            "optimization": "performance",
        },
    },
    # Synchronization
    synchronization={
        "strategy": "eventual_consistency",
        "max_lag_ms": 1000,
        "conflict_resolution": "last_write_wins",
    },
)

cqrS = CQRSManager(cqrS_config)
```

## Architecture Patterns

### Event-Driven Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Event-Driven Architecture                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  Event   │──▶│  Event   │──▶│  Event   │──▶│  Event   │ │
│  │ Producer │   │  Broker  │   │ Consumer │   │  Store   │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│       │              │              │              │        │
│       ▼              ▼              ▼              ▼        │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │  Event   │   │  Topic   │   │  Event   │   │  Event   │ │
│  │ Producer │   │ Routing  │   │ Handler  │   │ Sourcing │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Event Sourcing Pattern

```yaml
event_sourcing:
  components:
    event_store:
      description: "Stores all events"
      features: ["append_only", "immutable", "ordered"]
    
    aggregate:
      description: "Rebuilds state from events"
      features: ["event_replay", "snapshot", "versioning"]
    
    projection:
      description: "Creates read models from events"
      features: ["materialized_views", "event_handlers"]
  
  patterns:
    - name: "Event Store"
      description: "Append-only log of events"
    - name: "Aggregate"
      description: "Rebuild state from events"
    - name: "Projection"
      description: "Create read models"
    - name: "Snapshot"
      description: "Periodic state snapshots"
```

### Saga Pattern

```python
from event_driven import SagaOrchestrator, SagaDefinition

# Define saga
order_saga = SagaDefinition(
    name="OrderProcessingSaga",
    steps=[
        {
            "name": "ReserveInventory",
            "action": "reserve_inventory",
            "compensation": "release_inventory",
            "timeout": "30s",
        },
        {
            "name": "ProcessPayment",
            "action": "process_payment",
            "compensation": "refund_payment",
            "timeout": "60s",
        },
        {
            "name": "ShipOrder",
            "action": "ship_order",
            "compensation": "cancel_shipment",
            "timeout": "300s",
        },
    ],
    compensation_strategy="backward",
)

# Execute saga
orchestrator = SagaOrchestrator()
result = await orchestrator.execute(order_saga, context={"order_id": "ORD-001"})
```

## Integration Guide

### Kafka Integration

```python
from event_driven import KafkaIntegration

kafka = KafkaIntegration(
    bootstrap_servers="localhost:9092",
    schema_registry="http://localhost:8081",
)

# Produce event
async def produce_event(topic: str, event: Event):
    return await kafka.produce(
        topic=topic,
        key=event.event_id,
        value=event.serialize(),
        headers={"event_type": event.type},
    )

# Consume events
async def consume_events(topic: str, group_id: str):
    return await kafka.consume(
        topic=topic,
        group_id=group_id,
        auto_offset_reset="earliest",
    )
```

### RabbitMQ Integration

```python
from event_driven import RabbitMQIntegration

rabbitmq = RabbitMQIntegration(
    host="localhost",
    port=5672,
)

# Publish event
async def publish_event(exchange: str, routing_key: str, event: Event):
    return await rabbitmq.publish(
        exchange=exchange,
        routing_key=routing_key,
        body=event.serialize(),
    )

# Consume events
async def consume_events(queue: str):
    return await rabbitmq.consume(queue=queue)
```

### Event Schema Registry Integration

```python
from event_driven import SchemaRegistryIntegration

registry = SchemaRegistryIntegration(
    url="http://localhost:8081",
)

# Register schema
async def register_schema(schema: EventSchema):
    return await registry.register(
        subject=f"{schema.name}-value",
        schema=schema.avro_schema,
    )

# Get schema
async def get_schema(subject: str, version: int):
    return await registry.get_schema(subject, version)
```

## Performance Optimization

### Event Batching

```python
from event_driven import EventBatcher

batcher = EventBatcher(
    max_batch_size=100,
    batch_timeout_ms=50,
)

# Batch events
async def batch_events(events: list):
    return await batcher.batch(events)
```

### Event Compression

```python
from event_driven import EventCompressor

compressor = EventCompressor(
    algorithm="snappy",
    threshold_bytes=1024,
)

# Compress event
async def compress_event(event: Event):
    return await compressor.compress(event.serialize())

# Decompress event
async def decompress_event(data: bytes):
    return await compressor.decompress(data)
```

### Event Caching

```python
from event_driven import EventCache
import redis

cache = EventCache(
    redis_client=redis.Redis(host="localhost", port=6379),
    ttl=300,
)

# Cache event
async def cache_event(event: Event):
    await cache.set(
        key=f"event:{event.event_id}",
        value=event.serialize(),
    )

# Get cached event
async def get_cached_event(event_id: str):
    return await cache.get(f"event:{event_id}")
```

## Security Considerations

### Event Encryption

```python
from event_driven import EventEncryption

encryption = EventEncryption(
    algorithm="AES-256-GCM",
    key_rotation_days=90,
)

# Encrypt event
async def encrypt_event(event: Event):
    return await encryption.encrypt(event.serialize())

# Decrypt event
async def decrypt_event(data: bytes):
    return await encryption.decrypt(data)
```

### Event Signing

```python
from event_driven import EventSigner

signer = EventSigner(
    private_key_path="/etc/keys/event_signing.key",
    algorithm="RSA-SHA256",
)

# Sign event
async def sign_event(event: Event):
    return await signer.sign(event.serialize())

# Verify event signature
async def verify_event(data: bytes, signature: str):
    return await signer.verify(data, signature)
```

### Access Control

```python
from event_driven import EventAccessControl

access_control = EventAccessControl(
    # Topic permissions
    permissions={
        "order-service": {
            "produce": ["order.events"],
            "consume": ["payment.events", "inventory.events"],
        },
        "payment-service": {
            "produce": ["payment.events"],
            "consume": ["order.events"],
        },
    },
)

# Check permissions
async def check_permission(service: str, operation: str, topic: str):
    return await access_control.check(service, operation, topic)
```

## Troubleshooting Guide

### Common Issues

#### Issue: Event Loss

```python
# Symptom: Events not being processed
# Diagnosis:
from event_driven import EventDiagnostics

diagnostics = EventDiagnostics()

analysis = diagnostics.analyze_event_loss("order.events")
print(f"Produced events: {analysis.produced_count}")
print(f"Consumed events: {analysis.consumed_count}")
print(f"Lost events: {analysis.lost_count}")
print(f"Recommendations: {analysis.recommendations}")

# Resolution:
# 1. Check consumer group status
# 2. Verify topic configuration
# 3. Check network connectivity
```

#### Issue: Event Ordering

```python
# Symptom: Events processed out of order
# Diagnosis:
from event_driven import OrderingDiagnostics

ordering_diag = OrderingDiagnostics()

analysis = ordering_diag.analyze_ordering("order.events")
print(f"Partition count: {analysis.partition_count}")
print(f"Order violations: {analysis.violation_count}")
print(f"Recommendations: {analysis.recommendations}")

# Resolution:
# 1. Use partition key
# 2. Check partition count
# 3. Verify consumer configuration
```

#### Issue: Consumer Lag

```python
# Symptom: Consumer lag increasing
# Diagnosis:
from event_driven import ConsumerLagDiagnostics

lag_diag = ConsumerLagDiagnostics()

analysis = lag_diag.analyze_lag("order-consumer-group")
print(f"Current lag: {analysis.current_lag}")
print(f"Lag growth rate: {analysis.growth_rate}")
print(f"Recommendations: {analysis.recommendations}")

# Resolution:
# 1. Increase consumer instances
# 2. Optimize processing logic
# 3. Check broker performance
```

## API Reference

### Event Store API

```python
# POST /api/v2/events
# Append event

@router.post("/events")
async def append_event(
    request: AppendEventRequest,
) -> EventResponse:
    """
    Append event to store.

    Args:
        request: Event data

    Returns:
        EventResponse with appended event
    """
    pass

# GET /api/v2/events/{event_id}
# Get event

@router.get("/events/{event_id}")
async def get_event(
    event_id: str,
) -> EventResponse:
    """
    Get event by ID.

    Args:
        event_id: Event identifier

    Returns:
        EventResponse with event details
    """
    pass
```

### Event Stream API

```python
# GET /api/v2/streams/{stream_id}/events
# Read event stream

@router.get("/streams/{stream_id}/events")
async def read_stream(
    stream_id: str,
    from_version: int = 0,
    max_count: int = 100,
) -> StreamResponse:
    """
    Read event stream.

    Args:
        stream_id: Stream identifier
        from_version: Start version
        max_count: Maximum events

    Returns:
        StreamResponse with events
    """
    pass
```

### Saga API

```python
# POST /api/v2/sagas
# Create saga

@router.post("/sagas")
async def create_saga(
    request: CreateSagaRequest,
) -> SagaResponse:
    """
    Create and execute saga.

    Args:
        request: Saga definition

    Returns:
        SagaResponse with saga result
    """
    pass

# GET /api/v2/sagas/{saga_id}
# Get saga status

@router.get("/sagas/{saga_id}")
async def get_saga(
    saga_id: str,
) -> SagaResponse:
    """
    Get saga status.

    Args:
        saga_id: Saga identifier

    Returns:
        SagaResponse with saga details
    """
    pass
```

## Data Models

### Event Model

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict
from enum import Enum

class EventStatus(Enum):
    PENDING = "pending"
    PROCESSED = "processed"
    FAILED = "failed"

@dataclass
class Event:
    event_id: str
    type: str
    source: str
    data: Dict
    schema_version: str
    timestamp: datetime
    status: EventStatus
    metadata: Dict
    correlation_id: Optional[str]
    causation_id: Optional[str]
```

### Saga Model

```python
@dataclass
class Saga:
    id: str
    name: str
    status: str
    current_step: int
    steps: list
    context: Dict
    compensation_strategy: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]
```

### Event Stream Model

```python
@dataclass
class EventStream:
    stream_id: str
    events: list
    version: int
    created_at: datetime
    updated_at: datetime
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: event-driven-api
  namespace: microservices
spec:
  replicas: 3
  selector:
    matchLabels:
      app: event-driven-api
  template:
    metadata:
      labels:
        app: event-driven-api
    spec:
      containers:
      - name: event-driven-api
        image: microservices/event-driven:latest
        ports:
        - containerPort: 8000
        env:
        - name: KAFKA_BROKERS
          value: "kafka:9092"
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Monitoring & Observability

### Metrics Collection

```python
from prometheus_client import Counter, Histogram, Gauge

EVENTS_PRODUCED = Counter(
    'event_driven_events_produced_total',
    'Total events produced',
    ['topic', 'event_type']
)

EVENTS_CONSUMED = Counter(
    'event_driven_events_consumed_total',
    'Total events consumed',
    ['topic', 'consumer_group']
)

EVENT_PROCESSING_DURATION = Histogram(
    'event_driven_processing_duration_seconds',
    'Event processing duration',
    ['topic'],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0]
)

CONSUMER_LAG = Gauge(
    'event_driven_consumer_lag',
    'Consumer lag',
    ['consumer_group', 'topic']
)
```

### Logging Configuration

```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "event_id": getattr(record, "event_id", None),
            "topic": getattr(record, "topic", None),
        }
        return json.dumps(log_entry)

def setup_logging():
    logger = logging.getLogger("event_driven")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger.addHandler(handler)
    return logger
```

## Testing Strategy

### Unit Tests

```python
import pytest
from event_driven import Event, EventStore

class TestEvent:
    def setup_method(self):
        self.event = Event(
            type="OrderCreated",
            source="order-service",
            data={"order_id": "ORD-001"},
            schema_version="1.0",
        )

    def test_event_creation(self):
        """Test event creation."""
        assert self.event.type == "OrderCreated"
        assert self.event.source == "order-service"
```

### Integration Tests

```python
import pytest
from httpx import AsyncClient
from event_driven import app

@pytest.mark.asyncio
class TestEventAPI:
    async def test_append_event(self, async_client: AsyncClient):
        """Test event append endpoint."""
        response = await async_client.post(
            "/api/v2/events",
            json={
                "type": "OrderCreated",
                "source": "order-service",
                "data": {"order_id": "ORD-001"},
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["type"] == "OrderCreated"
```

## Versioning & Migration

### API Versioning

```python
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.post("/events")
async def append_event_v1():
    pass

@v2_router.post("/events")
async def append_event_v2(request: AppendEventRequest):
    pass

app.include_router(v1_router)
app.include_router(v2_router)
```

### Database Migrations

```python
# migrations/001_initial_schema.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'events',
        sa.Column('event_id', sa.String(50), primary_key=True),
        sa.Column('type', sa.String(100), nullable=False),
        sa.Column('source', sa.String(100), nullable=False),
        sa.Column('data', sa.JSON, nullable=False),
        sa.Column('timestamp', sa.DateTime, nullable=False),
    )

def downgrade():
    op.drop_table('events')
```

## Glossary

### Event-Driven Terms

| Term | Definition |
|------|------------|
| **Event** | Immutable record of something that happened |
| **Event Store** | Append-only log of events |
| **Event Sourcing** | Store state as sequence of events |
| **CQRS** | Command Query Responsibility Segregation |
| **Saga** | Distributed transaction pattern |
| **Projection** | Materialized view from events |
| **Consumer** | Event handler |
| **Producer** | Event publisher |
| **Topic** | Event channel |
| **Partition** | Event stream segment |

## Changelog

### Version 2.0.0 (2024-01-15)
- Added event sourcing
- Implemented CQRS
- Enhanced saga patterns
- Added schema registry

### Version 1.5.0 (2023-10-01)
- Added Kafka integration
- Implemented RabbitMQ support
- Enhanced event handling
- Added monitoring

### Version 1.4.0 (2023-07-15)
- Added message brokers
- Implemented dead letter queues
- Added event replay
- Enhanced security

### Version 1.3.0 (2023-04-01)
- Added event definition
- Implemented event store
- Added event schemas
- Enhanced API

### Version 1.2.0 (2023-01-15)
- Added basic events
- Implemented event handling
- Added event routing
- Enhanced documentation

### Version 1.1.0 (2022-10-01)
- Added event publishing
- Implemented basic consumers
- Added logging
- Enhanced UI

### Version 1.0.0 (2022-07-15)
- Initial release
- Basic event-driven
- REST API
- PostgreSQL support

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/company/event-driven.git
cd event-driven
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pytest
uvicorn main:app --reload
```

### Code Standards

- Follow PEP 8
- Use type hints
- Write docstrings
- Maintain 80% test coverage
- Run linting before commit

## License

MIT License

Copyright (c) 2024 Event-Driven Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

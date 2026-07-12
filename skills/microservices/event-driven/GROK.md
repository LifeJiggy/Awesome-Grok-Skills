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

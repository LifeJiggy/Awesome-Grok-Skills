"""
Event-Driven Architecture Module
Event-driven patterns for microservices
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


class EventType(Enum):
    DOMAIN = "domain"
    INTEGRATION = "integration"
    COMMAND = "command"
    QUERY = "query"

class SagaStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    COMPENSATING = "compensating"

@dataclass
class Event:
    type: str = ""
    source: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    schema_version: str = "1.0"
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EventSchema:
    name: str = ""
    version: str = "1.0"
    schema: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EventStore:
    _events: List[Event] = field(default_factory=list)

    def append(self, event: Event) -> None:
        self._events.append(event)

    def read_stream(self, event_type: str, stream_id: str = "") -> List[Event]:
        return [e for e in self._events if e.type == event_type]

@dataclass
class SagaStep:
    action: str = ""
    compensation: str = ""
    timeout_seconds: int = 30

@dataclass
class SagaResult:
    status: SagaStatus = SagaStatus.PENDING
    completed_steps: int = 0
    failed_step: Optional[str] = None
    context: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Saga:
    name: str = ""
    steps: List[SagaStep] = field(default_factory=list)

    def execute(self, context: Optional[Dict[str, Any]] = None) -> SagaResult:
        return SagaResult(status=SagaStatus.COMPLETED, completed_steps=len(self.steps), context=context or {})

class CommandBus:
    def __init__(self) -> None:
        self._handlers: Dict[str, Callable] = {}

    def register(self, command: str, handler: Callable) -> None:
        self._handlers[command] = handler

    def dispatch(self, command: str, data: Any = None) -> Any:
        handler = self._handlers.get(command)
        return handler(data) if handler else None

class QueryBus:
    def __init__(self) -> None:
        self._handlers: Dict[str, Callable] = {}

    def register(self, query: str, handler: Callable) -> None:
        self._handlers[query] = handler

    def execute(self, query: str, params: Any = None) -> Any:
        handler = self._handlers.get(query)
        return handler(params) if handler else None

class EventBus:
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable) -> None:
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)

    def publish(self, event: Event) -> None:
        for handler in self._subscribers.get(event.type, []):
            try:
                handler(event)
            except Exception as e:
                logger.error("Event handler failed: %s", e)

def main() -> None:
    print("=" * 60)
    print("  Event-Driven Architecture Module — Demo")
    print("=" * 60)

    event = Event(type="OrderCreated", source="order-service", data={"order_id": "ORD-001", "total": 99.99})
    print(f"\n[+] Event: {event.type} (ID: {event.event_id})")

    store = EventStore()
    store.append(event)
    events = store.read_stream("OrderCreated")
    print(f"\n[+] Event Store: {len(events)} events")

    saga = Saga(name="OrderProcessing", steps=[SagaStep(action="reserve"), SagaStep(action="pay"), SagaStep(action="ship")])
    result = saga.execute({"order_id": "ORD-001"})
    print(f"\n[+] Saga: {result.status.value} ({result.completed_steps} steps)")

    event_bus = EventBus()
    event_bus.subscribe("OrderCreated", lambda e: print(f"    Handler: Order {e.data.get('order_id')} created"))
    event_bus.publish(event)

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()

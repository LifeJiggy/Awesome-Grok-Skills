---
name: "Design Patterns"
version: "2.0.0"
description: "Comprehensive design patterns toolkit with pattern detection, implementation guidance, anti-pattern identification, pattern selection, and pattern documentation for software architecture"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["development", "design-patterns", "architecture", "anti-patterns", "best-practices"]
category: "development"
personality: "design-pattern-expert"
use_cases: ["pattern detection", "implementation guidance", "anti-pattern identification", "pattern selection", "architecture design"]
---

# Design Patterns

> Production-grade design patterns framework providing pattern detection, implementation guidance, anti-pattern identification, pattern selection recommendations, and architecture documentation for building maintainable software.

## Overview

The Design Patterns module provides a comprehensive catalog of software design patterns with detection, implementation, and guidance. It implements pattern detection from code structure, anti-pattern identification, pattern selection based on requirements, implementation templates with examples, and pattern documentation generation. Every pattern includes use cases, trade-offs, and related patterns.

## Core Capabilities

### 1. Creational Patterns
- Singleton: Ensure single instance
- Factory Method: Create objects without specifying class
- Abstract Factory: Create families of related objects
- Builder: Construct complex objects step by step
- Prototype: Clone existing objects

### 2. Structural Patterns
- Adapter: Convert interface to another interface
- Bridge: Separate abstraction from implementation
- Composite: Compose objects into tree structures
- Decorator: Add responsibilities dynamically
- Facade: Simplify complex subsystems
- Proxy: Control access to another object

### 3. Behavioral Patterns
- Observer: Define subscription mechanism
- Strategy: Define family of algorithms
- Command: Encapsulate requests as objects
- State: Alter behavior when internal state changes
- Template Method: Define algorithm skeleton
- Iterator: Sequential access without exposing representation

### 4. Anti-Pattern Detection
- God Object detection
- Spaghetti Code identification
- Golden Hammer recognition
- Lava Flow detection
- Premature Optimization identification

### 5. Pattern Selection
- Requirement-based pattern recommendation
- Trade-off analysis
- Complexity assessment
- Implementation effort estimation

## Usage Examples

### Pattern Detection

```python
from design_patterns import PatternDetector

detector = PatternDetector()

# Analyze code for patterns
patterns = detector.detect_file("app.py")
print(f"Patterns detected: {len(patterns)}")
for pattern in patterns:
    print(f"  {pattern.name} ({pattern.category})")
    print(f"    Location: {pattern.file}:{pattern.line}")
    print(f"    Confidence: {pattern.confidence:.0%}")
```

### Pattern Implementation

```python
from design_patterns import PatternImpl, PatternType

# Generate pattern implementation
impl = PatternImpl.generate(
    pattern=PatternType.OBSERVER,
    language="python",
    subject_class="OrderService",
    observer_class="EmailNotifier",
)

print("Implementation:")
print(impl.code)
print("\nUsage:")
print(impl.usage_example)
```

### Anti-Pattern Detection

```python
from design_patterns import AntiPatternDetector

detector = AntiPatternDetector()

# Detect anti-patterns
anti_patterns = detector.detect("app.py")
print(f"Anti-patterns found: {len(anti_patterns)}")
for ap in anti_patterns:
    print(f"  {ap.name}: {ap.description}")
    print(f"    Impact: {ap.impact}")
    print(f"    Fix: {ap.refactoring_suggestion}")
```

### Pattern Selection

```python
from design_patterns import PatternSelector

selector = PatternSelector()

# Get pattern recommendations
recommendations = selector.recommend(
    requirements=["need to notify multiple components", "decouple sender and receiver"],
    context={"language": "python", "complexity": "medium"},
)

print("Recommended patterns:")
for rec in recommendations:
    print(f"  {rec.name}: {rec.reason}")
    print(f"    Trade-offs: {rec.trade_offs}")
```

## Best Practices

### Pattern Selection
- Don't use patterns for the sake of using patterns
- Choose patterns that solve actual problems
- Consider team familiarity and maintenance burden
- Document pattern usage in the codebase

### Implementation
- Follow the pattern's intent, not just its structure
- Keep implementations simple and focused
- Use language features where available (e.g., Python decorators for Decorator pattern)
- Test pattern implementations thoroughly

### Anti-Patterns
- Detect anti-patterns early in development
- Refactor anti-patterns incrementally
- Use code reviews to catch anti-patterns
- Document known anti-patterns and their fixes

### Documentation
- Document which patterns are used and why
- Include pattern diagrams in architecture docs
- Reference pattern sources (GoF book, etc.)
- Train team on common patterns

## Related Modules

- **refactoring-patterns**: Refactor code to use patterns
- **clean-architecture**: Architectural pattern guidance
- **code-analysis**: Detect pattern violations
- **testing-strategies**: Test pattern implementations

---

## Advanced Configuration

### Advanced Pattern Detection

```python
from design_patterns import PatternDetector, DetectionConfig

detector = PatternDetector(
    config=DetectionConfig(
        enabled_categories=["creational", "structural", "behavioral"],
        min_confidence=0.7,
        check_anti_patterns=True,
        suggest_improvements=True,
        include_examples=True,
    ),
)

# Detect patterns in project
patterns = detector.detect_project(
    "/path/to/project",
    include_patterns=["*.py", "*.js"],
    exclude_patterns=["tests/*", "node_modules/*"],
)

print(f"Patterns detected: {len(patterns)}")
print(f"By category:")
categories = {}
for pattern in patterns:
    categories[pattern.category] = categories.get(pattern.category, 0) + 1
for cat, count in sorted(categories.items()):
    print(f"  {cat}: {count}")

print("\nMost common patterns:")
pattern_counts = {}
for pattern in patterns:
    pattern_counts[pattern.name] = pattern_counts.get(pattern.name, 0) + 1
for name, count in sorted(pattern_counts.items(), key=lambda x: -x[1])[:10]:
    print(f"  {name}: {count} occurrences")
```

### Advanced Pattern Implementation

```python
from design_patterns import PatternImpl, PatternType, Language

# Generate comprehensive pattern implementation
impl = PatternImpl.generate_comprehensive(
    pattern=PatternType.STRATEGY,
    language=Language.PYTHON,
    context={
        "interface_name": "PaymentStrategy",
        "implementations": ["CreditCardPayment", "PayPalPayment", "BitcoinPayment"],
        "context_class": "PaymentProcessor",
        "include_tests": True,
        "include_docs": True,
    },
)

print("Implementation:")
print(impl.code)
print("\nTests:")
print(impl.test_code)
print("\nDocumentation:")
print(impl.documentation)
```

### Advanced Anti-Pattern Detection

```python
from design_patterns import AntiPatternDetector, AntiPatternConfig

detector = AntiPatternDetector(
    config=AntiPatternConfig(
        enabled_anti_patterns=["all"],
        severity_threshold="medium",
        suggest_refactoring=True,
        estimate_effort=True,
    ),
)

# Detect anti-patterns in project
anti_patterns = detector.detect_project(
    "/path/to/project",
    analyze_complexity=True,
    analyze_dependencies=True,
    analyze_duplication=True,
)

print(f"Anti-patterns found: {len(anti_patterns)}")
print(f"By severity:")
for severity in ["critical", "high", "medium", "low"]:
    count = len([ap for ap in anti_patterns if ap.severity == severity])
    print(f"  {severity}: {count}")

print("\nTop anti-patterns:")
for ap in anti_patterns[:10]:
    print(f"\n  {ap.name}: {ap.description}")
    print(f"    Impact: {ap.impact}")
    print(f"    Location: {ap.file}:{ap.line}")
    print(f"    Refactoring: {ap.refactoring_suggestion}")
    print(f"    Effort: {ap.effort_hours:.1f} hours")
```

## Architecture Patterns

### Design Patterns Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Design Patterns Architecture                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Detection Layer                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Creational │  │  Structural │  │  Behavioral  │ │   │
│  │  │  Patterns   │  │  Patterns   │  │  Patterns    │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Implementation Layer                    │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Templates  │  │  Examples   │  │  Tests       │ │   │
│  │  │             │  │             │  │              │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Selection Layer                         │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Requirement│  │  Trade-off  │  │  Complexity  │ │   │
│  │  │  Analysis   │  │  Analysis   │  │  Assessment  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### CI/CD Integration

```yaml
# .github/workflows/design-patterns.yml
name: Design Patterns Analysis

on:
  pull_request:
    branches: [main]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Detect patterns
        run: design-patterns detect --confidence 0.7
      
      - name: Detect anti-patterns
        run: design-patterns anti-patterns --severity medium
      
      - name: Generate report
        run: design-patterns report --output report.json
```

## Performance Optimization

### Pattern Detection Performance

| Technique | Speed | Accuracy | Use Case |
|-----------|-------|----------|----------|
| AST analysis | Medium | High | Structural patterns |
| Regex matching | Fast | Medium | Simple patterns |
| Type inference | Slow | High | Complex patterns |
| ML-based | Slow | High | Novel patterns |

## Security Considerations

### Secure Pattern Usage

```python
from design_patterns import SecurityChecker

checker = SecurityChecker()

# Check pattern security
security = checker.check_pattern(
    pattern="singleton",
    implementation_code=singleton_code,
)

print(f"Secure: {security.is_secure}")
print(f"Issues: {len(security.issues)}")
for issue in security.issues:
    print(f"  [{issue.severity}] {issue.description}")
    print(f"    Fix: {issue.fix_suggestion}")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| False positives | Wrong pattern detected | Tune confidence threshold |
| Over-engineering | Too many patterns | Use patterns only when needed |
| Pattern misuse | Incorrect implementation | Follow pattern intent |
| Anti-patterns | Poor code structure | Refactor incrementally |

## API Reference

### PatternDetector

```python
class PatternDetector:
    def __init__(self, config: DetectionConfig = None)
    def detect_file(self, file_path: str) -> list[DetectedPattern]
    def detect_project(self, project_path: str, **kwargs) -> list[DetectedPattern]
    def get_pattern_categories(self) -> list[str]
    def get_pattern_by_name(self, name: str) -> PatternInfo
```

### PatternImpl

```python
class PatternImpl:
    @staticmethod
    def generate(pattern: PatternType, language: Language, **kwargs) -> PatternCode
    @staticmethod
    def generate_comprehensive(pattern: PatternType, language: Language, **kwargs) -> ComprehensiveCode
    @staticmethod
    def get_examples(pattern: PatternType, language: Language) -> list[Example]
```

### AntiPatternDetector

```python
class AntiPatternDetector:
    def __init__(self, config: AntiPatternConfig = None)
    def detect_file(self, file_path: str) -> list[AntiPattern]
    def detect_project(self, project_path: str, **kwargs) -> list[AntiPattern]
    def get_refactoring_suggestions(self, anti_pattern: AntiPattern) -> list[RefactoringSuggestion]
    def estimate_effort(self, anti_patterns: list[AntiPattern]) -> float
```

### PatternSelector

```python
class PatternSelector:
    def __init__(self)
    def recommend(self, requirements: list[str], context: dict = None) -> list[PatternRecommendation]
    def analyze_trade_offs(self, pattern: str) -> TradeOffAnalysis
    def estimate_complexity(self, pattern: str, language: str) -> float
    def get_related_patterns(self, pattern: str) -> list[str]
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

class PatternCategory(Enum):
    CREATIONAL = "creational"
    STRUCTURAL = "structural"
    BEHAVIORAL = "behavioral"

@dataclass
class DetectedPattern:
    name: str
    category: PatternCategory
    confidence: float
    file: str
    line: int
    description: str
    related_patterns: List[str]

@dataclass
class AntiPattern:
    name: str
    severity: str
    description: str
    impact: str
    file: str
    line: int
    refactoring_suggestion: str
    effort_hours: float

@dataclass
class PatternRecommendation:
    name: str
    category: PatternCategory
    reason: str
    trade_offs: Dict[str, str]
    complexity: float
    examples: List[str]
```

## Deployment Guide

### Installation

```bash
pip install design-patterns
```

## Monitoring & Observability

### Metrics Collection

```python
from design_patterns import MetricsCollector

collector = MetricsCollector()

# Collect pattern metrics
collector.counter("pattern.detected.total", count, tags={"pattern": pattern_name})
collector.counter("anti_pattern.detected.total", count, tags={"type": anti_pattern_type})
collector.gauge("pattern.confidence.average", avg)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from design_patterns import PatternDetector, AntiPatternDetector

@pytest.fixture
def detector():
    return PatternDetector()

def test_detect_patterns(detector):
    patterns = detector.detect_file("test.py")
    assert isinstance(patterns, list)
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Python | 3.8 | 3.11+ |

## Glossary

| Term | Definition |
|------|------------|
| **Design Pattern** | Reusable solution to common problem |
| **Anti-Pattern** | Common but ineffective solution |
| **Creational** | Patterns for object creation |
| **Structural** | Patterns for object composition |
| **Behavioral** | Patterns for object communication |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added ML-based pattern detection
- New pattern selector
- Improved anti-pattern detection
- Added security checking

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/design-patterns.git
cd design-patterns
pip install -e ".[dev]"
pytest
```

## Concurrency Patterns

### Thread-Safe Singleton

```python
import threading

class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

# Usage
s1 = ThreadSafeSingleton()
s2 = ThreadSafeSingleton()
assert s1 is s2  # Same instance
```

### Producer-Consumer Pattern

```python
import threading
import queue

class ProducerConsumer:
    def __init__(self, max_size=100):
        self.queue = queue.Queue(maxsize=max_size)
        self.stop_event = threading.Event()

    def producer(self, items):
        for item in items:
            if self.stop_event.is_set():
                break
            self.queue.put(item)
            print(f"Produced: {item}")
        self.queue.put(None)  # Sentinel

    def consumer(self, name):
        while not self.stop_event.is_set():
            try:
                item = self.queue.get(timeout=1)
                if item is None:
                    break
                print(f"{name} consumed: {item}")
                self.queue.task_done()
            except queue.Empty:
                continue

# Usage
pc = ProducerConsumer()
items = range(10)
producer_thread = threading.Thread(target=pc.producer, args=(items,))
consumer_threads = [
    threading.Thread(target=pc.consumer, args=(f"Consumer-{i}",))
    for i in range(3)
]

producer_thread.start()
for t in consumer_threads:
    t.start()
```

### Async Pattern with Context Manager

```python
import asyncio
from contextlib import asynccontextmanager

class AsyncResourceManager:
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        print(f"Acquiring resource: {self.name}")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print(f"Releasing resource: {self.name}")
        await asyncio.sleep(0.1)
        return False

@asynccontextmanager
async def managed_operation(name):
    async with AsyncResourceManager(name) as resource:
        yield resource
        print(f"Operation completed for {name}")

# Usage
async def main():
    async with managed_operation("database") as res:
        print(f"Using resource: {res.name}")

asyncio.run(main())
```

## Microservices Patterns

### Service Discovery Pattern

```python
from dataclasses import dataclass, field
from typing import Dict, List
import time

@dataclass
class ServiceInstance:
    name: str
    host: str
    port: int
    health_check_url: str
    metadata: Dict[str, str] = field(default_factory=dict)
    last_heartbeat: float = field(default_factory=time.time)

class ServiceRegistry:
    def __init__(self):
        self.services: Dict[str, List[ServiceInstance]] = {}

    def register(self, instance: ServiceInstance):
        if instance.name not in self.services:
            self.services[instance.name] = []
        self.services[instance.name].append(instance)

    def deregister(self, name: str, host: str, port: int):
        if name in self.services:
            self.services[name] = [
                s for s in self.services[name]
                if not (s.host == host and s.port == port)
            ]

    def discover(self, name: str) -> List[ServiceInstance]:
        instances = self.services.get(name, [])
        # Filter out unhealthy instances
        healthy = [
            s for s in instances
            if time.time() - s.last_heartbeat < 30
        ]
        return healthy

    def get_load_balanced(self, name: str) -> ServiceInstance:
        instances = self.discover(name)
        if not instances:
            raise ValueError(f"No healthy instances for {name}")
        # Simple round-robin
        return instances[int(time.time()) % len(instances)]

# Usage
registry = ServiceRegistry()
registry.register(ServiceInstance("api", "10.0.0.1", 8080, "/health"))
registry.register(ServiceInstance("api", "10.0.0.2", 8080, "/health"))

instance = registry.get_load_balanced("api")
print(f"Connecting to: {instance.host}:{instance.port}")
```

### Circuit Breaker Pattern

```python
import time
from enum import Enum
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0

    def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
            else:
                raise CircuitOpenError("Circuit is open")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        self.failure_count = 0
        self.state = CircuitState.CLOSED

    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN

class CircuitOpenError(Exception):
    pass

# Usage
breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=10)

def call_external_api():
    # Simulated external API call
    import random
    if random.random() < 0.3:
        raise ConnectionError("API unavailable")
    return {"status": "ok"}

for i in range(10):
    try:
        result = breaker.call(call_external_api)
        print(f"Call {i+1}: {result}")
    except CircuitOpenError:
        print(f"Call {i+1}: Circuit open, skipping")
    except ConnectionError as e:
        print(f"Call {i+1}: Failed - {e}")
```

## Event-Driven Patterns

### Event Bus Implementation

```python
from dataclasses import dataclass
from typing import Callable, Dict, List, Any
from datetime import datetime
import uuid

@dataclass
class Event:
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime
    event_id: str = None

    def __post_init__(self):
        if self.event_id is None:
            self.event_id = str(uuid.uuid4())

class EventBus:
    def __init__(self):
        self.handlers: Dict[str, List[Callable]] = {}
        self.event_log: List[Event] = []

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: Callable):
        if event_type in self.handlers:
            self.handlers[event_type].remove(handler)

    def publish(self, event: Event):
        self.event_log.append(event)
        handlers = self.handlers.get(event.event_type, [])
        for handler in handlers:
            handler(event)

    def get_history(self, event_type: str = None) -> List[Event]:
        if event_type:
            return [e for e in self.event_log if e.event_type == event_type]
        return self.event_log

# Usage
bus = EventBus()

def on_order_created(event: Event):
    print(f"Order created: {event.payload}")

def on_order_shipped(event: Event):
    print(f"Order shipped: {event.payload}")

bus.subscribe("order.created", on_order_created)
bus.subscribe("order.shipped", on_order_shipped)

bus.publish(Event(
    event_type="order.created",
    payload={"order_id": "12345", "amount": 99.99},
    timestamp=datetime.now(),
))
```

### Saga Pattern for Distributed Transactions

```python
from dataclasses import dataclass
from typing import List, Callable, Optional
from enum import Enum

class SagaState(Enum):
    RUNNING = "running"
    COMPENSATING = "compensating"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class SagaStep:
    name: str
    action: Callable
    compensation: Callable

class Saga:
    def __init__(self, name: str):
        self.name = name
        self.steps: List[SagaStep] = []
        self.state = SagaState.RUNNING
        self.completed_steps: List[str] = []

    def add_step(self, step: SagaStep):
        self.steps.append(step)

    def execute(self) -> bool:
        for step in self.steps:
            try:
                step.action()
                self.completed_steps.append(step.name)
            except Exception as e:
                print(f"Step {step.name} failed: {e}")
                self.state = SagaState.COMPENSATING
                self._compensate()
                return False

        self.state = SagaState.COMPLETED
        return True

    def _compensate(self):
        for step_name in reversed(self.completed_steps):
            step = next(s for s in self.steps if s.name == step_name)
            try:
                step.compensation()
                print(f"Compensated: {step.name}")
            except Exception as e:
                print(f"Compensation failed for {step.name}: {e}")

# Usage
saga = Saga("order-processing")
saga.add_step(SagaStep(
    name="reserve_inventory",
    action=lambda: print("Reserving inventory"),
    compensation=lambda: print("Releasing inventory"),
))
saga.add_step(SagaStep(
    name="charge_payment",
    action=lambda: print("Charging payment"),
    compensation=lambda: print("Refunding payment"),
))
saga.add_step(SagaStep(
    name="create_shipment",
    action=lambda: print("Creating shipment"),
    compensation=lambda: print("Cancelling shipment"),
))

success = saga.execute()
print(f"Saga result: {saga.state.value}")
```

## Pattern Composition Recipes

### Repository + Unit of Work

```python
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic
from dataclasses import dataclass, field

T = TypeVar('T')

@dataclass
class Entity:
    id: Optional[int] = None
    _is_new: bool = field(default=True, repr=False)
    _is_modified: bool = field(default=False, repr=False)

class Repository(ABC, Generic[T]):
    @abstractmethod
    def get(self, id: int) -> Optional[T]: pass

    @abstractmethod
    def get_all(self) -> List[T]: pass

    @abstractmethod
    def add(self, entity: T): pass

    @abstractmethod
    def remove(self, entity: T): pass

class UnitOfWork:
    def __init__(self):
        self._new_entities: List[Entity] = []
        self._modified_entities: List[Entity] = []
        self._removed_entities: List[Entity] = []

    def register_new(self, entity: Entity):
        self._new_entities.append(entity)

    def register_modified(self, entity: Entity):
        self._modified_entities.append(entity)

    def register_removed(self, entity: Entity):
        self._removed_entities.append(entity)

    def commit(self):
        # Persist all changes atomically
        self._save_new()
        self._save_modified()
        self._save_removed()
        self._clear()

    def rollback(self):
        self._clear()

    def _save_new(self):
        for entity in self._new_entities:
            print(f"Inserting: {entity}")
            entity._is_new = False

    def _save_modified(self):
        for entity in self._modified_entities:
            print(f"Updating: {entity}")
            entity._is_modified = False

    def _save_removed(self):
        for entity in self._removed_entities:
            print(f"Deleting: {entity}")

    def _clear(self):
        self._new_entities.clear()
        self._modified_entities.clear()
        self._removed_entities.clear()

# Usage
class User(Entity):
    def __init__(self, name: str, email: str):
        super().__init__()
        self.name = name
        self.email = email

uow = UnitOfWork()
user = User("Alice", "alice@example.com")
uow.register_new(user)
user.email = "alice_new@example.com"
uow.register_modified(user)
uow.commit()
```

## Migration & Legacy Modernization

### Strangler Fig Pattern

```python
from typing import Dict, Callable, Any

class StranglerFig:
    def __init__(self):
        self.legacy_handlers: Dict[str, Callable] = {}
        self.modern_handlers: Dict[str, Callable] = {}
        self.routing_rules: Dict[str, bool] = {}

    def register_legacy(self, path: str, handler: Callable):
        self.legacy_handlers[path] = handler
        self.routing_rules[path] = False  # False = use legacy

    def register_modern(self, path: str, handler: Callable):
        self.modern_handlers[path] = handler
        self.routing_rules[path] = True  # True = use modern

    def migrate_route(self, path: str):
        if path in self.legacy_handlers and path in self.modern_handlers:
            self.routing_rules[path] = True
            print(f"Migrated {path} to modern implementation")

    def route(self, path: str, *args, **kwargs) -> Any:
        use_modern = self.routing_rules.get(path, False)
        if use_modern:
            return self.modern_handlers[path](*args, **kwargs)
        return self.legacy_handlers[path](*args, **kwargs)

    def get_migration_status(self) -> Dict[str, bool]:
        return self.routing_rules.copy()

# Usage
fig = StranglerFig()
fig.register_legacy("/api/users", lambda: "Legacy user endpoint")
fig.register_modern("/api/users", lambda: "Modern user endpoint")
fig.register_legacy("/api/orders", lambda: "Legacy order endpoint")

# Initially all traffic goes to legacy
print(fig.route("/api/users"))  # Legacy

# Migrate users endpoint
fig.migrate_route("/api/users")
print(fig.route("/api/users"))  # Modern
print(fig.route("/api/orders"))  # Still legacy
```

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/design-patterns.git
cd design-patterns
pip install -e ".[dev]"
pytest
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
"""
Distributed Tracing Module
Distributed tracing and observability for microservices
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class SamplingStrategy(Enum):
    PROBABILISTIC = "probabilistic"
    RATE_LIMITING = "rate_limiting"
    ADAPTIVE = "adaptive"

class SpanStatus(Enum):
    OK = "OK"
    ERROR = "ERROR"
    TIMEOUT = "TIMEOUT"

@dataclass
class SpanContext:
    trace_id: str = ""
    span_id: str = ""
    parent_span_id: Optional[str] = None
    baggage: Dict[str, str] = field(default_factory=dict)

@dataclass
class Span:
    operation: str = ""
    context: SpanContext = field(default_factory=SpanContext)
    service_name: str = ""
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    tags: Dict[str, Any] = field(default_factory=dict)
    logs: List[str] = field(default_factory=list)
    status: SpanStatus = SpanStatus.OK
    duration_ms: float = 0.0

    def set_tag(self, key: str, value: Any) -> None:
        self.tags[key] = value

    def log(self, message: str) -> None:
        self.logs.append(f"[{datetime.utcnow().isoformat()}] {message}")

    def finish(self) -> None:
        self.end_time = datetime.utcnow()
        self.duration_ms = (self.end_time - self.start_time).total_seconds() * 1000

@dataclass
class Tracer:
    service_name: str = ""
    _spans: List[Span] = field(default_factory=list)

    def start_span(self, operation: str, context: Optional[SpanContext] = None) -> Span:
        ctx = context or SpanContext(trace_id=str(uuid.uuid4()), span_id=str(uuid.uuid4())[:8])
        span = Span(operation=operation, context=ctx, service_name=self.service_name)
        self._spans.append(span)
        return span

    def configure_sampling(self, config: Any) -> None:
        logger.info("Configured sampling for %s", self.service_name)

@dataclass
class SlowTrace:
    trace_id: str = ""
    duration_ms: float = 0.0
    span_count: int = 0
    services: List[str] = field(default_factory=list)

class TraceAnalyzer:
    def find_slow_traces(self, service: str = "", threshold_ms: int = 1000, time_range: str = "1h") -> List[SlowTrace]:
        return [SlowTrace(trace_id="trace-001", duration_ms=2500, span_count=15, services=["order-service", "payment-service", "inventory-service"])]

@dataclass
class SamplingConfig:
    strategy: SamplingStrategy = SamplingStrategy.ADAPTIVE
    default_rate: float = 0.01
    service_rates: Dict[str, float] = field(default_factory=dict)
    max_traces_per_second: int = 100

@dataclass
class ServiceDependency:
    source: str = ""
    target: str = ""
    request_count: int = 0
    avg_latency_ms: float = 0.0
    error_rate: float = 0.0

class DependencyMapper:
    def generate(self, time_range: str = "24h", min_requests: int = 100) -> List[ServiceDependency]:
        return [
            ServiceDependency(source="api-gateway", target="order-service", request_count=15000, avg_latency_ms=45),
            ServiceDependency(source="order-service", target="payment-service", request_count=12000, avg_latency_ms=120),
            ServiceDependency(source="order-service", target="inventory-service", request_count=12000, avg_latency_ms=30),
        ]

def main() -> None:
    print("=" * 60)
    print("  Distributed Tracing Module — Demo")
    print("=" * 60)

    tracer = Tracer(service_name="order-service")
    span = tracer.start_span("process_order", SpanContext(trace_id="abc123"))
    span.set_tag("order.id", "ORD-001")
    span.log("Processing order")
    span.finish()
    print(f"\n[+] Span: {span.operation} ({span.duration_ms:.1f}ms)")

    analyzer = TraceAnalyzer()
    slow = analyzer.find_slow_traces("order-service", threshold_ms=1000)
    print(f"\n[+] Slow Traces: {len(slow)}")
    for t in slow:
        print(f"    {t.trace_id}: {t.duration_ms:.0f}ms ({t.span_count} spans)")

    mapper = DependencyMapper()
    deps = mapper.generate()
    print(f"\n[+] Dependencies: {len(deps)}")
    for dep in deps:
        print(f"    {dep.source} -> {dep.target}: {dep.request_count} reqs, {dep.avg_latency_ms:.0f}ms")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()

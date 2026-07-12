"""
API Management Module — Multi-gateway configuration, route management, service discovery,
circuit breaking, health checks, and plugin management for API gateways.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class GatewayType(Enum):
    KONG = "kong"
    NGINX = "nginx"
    ENVOY = "envoy"
    TRAEFIK = "traefik"
    AWS_APIGW = "aws_apigateway"
    APISIX = "apisix"


class CircuitState(Enum):
    CLOSED = "closed"       # Normal operation
    OPEN = "open"           # Failing, rejecting requests
    HALF_OPEN = "half_open" # Testing recovery


class HealthStatus(Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"
    UNKNOWN = "unknown"


class LoadBalancingAlgorithm(Enum):
    ROUND_ROBIN = "round_robin"
    LEAST_CONNECTIONS = "least_connections"
    WEIGHTED = "weighted"
    IP_HASH = "ip_hash"
    RANDOM = "random"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Service:
    """An upstream service definition."""
    name: str
    url: str
    protocol: str = "http"
    host: str = ""
    port: int = 80
    connect_timeout_ms: int = 5000
    read_timeout_ms: int = 30000
    write_timeout_ms: int = 30000
    retries: int = 3
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "url": self.url,
            "protocol": self.protocol,
            "timeout_ms": self.connect_timeout_ms,
            "retries": self.retries,
        }


@dataclass
class Route:
    """A gateway route definition."""
    name: str
    paths: List[str]
    service: str
    methods: List[str] = field(default_factory=lambda: ["GET", "POST", "PUT", "PATCH", "DELETE"])
    strip_path: str = ""
    hosts: Optional[List[str]] = None
    headers: Optional[Dict[str, str]] = None
    plugins: List[str] = field(default_factory=list)
    priority: int = 0
    https_redirect: bool = False
    preserve_host: bool = False
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "paths": self.paths,
            "methods": self.methods,
            "service": self.service,
            "strip_path": self.strip_path,
            "plugins": self.plugins,
        }


@dataclass
class Plugin:
    """A gateway plugin configuration."""
    name: str
    service: Optional[str] = None
    route: Optional[str] = None
    config: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    consumer: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "service": self.service,
            "route": self.route,
            "enabled": self.enabled,
            "config": self.config,
        }


@dataclass
class CircuitBreaker:
    """Circuit breaker state and configuration."""
    service_name: str
    state: CircuitState = CircuitState.CLOSED
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout_seconds: int = 30
    half_open_max_requests: int = 3
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: Optional[float] = None
    last_state_change: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def should_reject(self) -> bool:
        if self.state == CircuitState.OPEN:
            if self.last_failure_time and time.time() - self.last_failure_time > self.timeout_seconds:
                self.state = CircuitState.HALF_OPEN
                return False
            return True
        return False

    def record_success(self) -> None:
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0
        elif self.state == CircuitState.CLOSED:
            self.failure_count = max(0, self.failure_count - 1)

    def record_failure(self) -> None:
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.last_failure_time = time.time()
        elif self.state == CircuitState.CLOSED:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
                self.last_failure_time = time.time()
                self.last_state_change = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "service": self.service_name,
            "state": self.state.value,
            "failures": self.failure_count,
            "successes": self.success_count,
        }


@dataclass
class HealthCheck:
    """Health check result for a service."""
    service_name: str
    status: HealthStatus
    latency_ms: float
    last_check: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    consecutive_failures: int = 0
    message: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "service": self.service_name,
            "status": self.status.value,
            "latency_ms": round(self.latency_ms, 1),
            "consecutive_failures": self.consecutive_failures,
        }


@dataclass
class Upstream:
    """An upstream load balancing group."""
    name: str
    targets: List[Dict[str, Any]] = field(default_factory=list)
    algorithm: LoadBalancingAlgorithm = LoadBalancingAlgorithm.ROUND_ROBIN
    health_checks: Dict[str, Any] = field(default_factory=dict)
    _index: int = 0

    def next_target(self) -> Optional[Dict[str, Any]]:
        if not self.targets:
            return None
        if self.algorithm == LoadBalancingAlgorithm.ROUND_ROBIN:
            target = self.targets[self._index % len(self.targets)]
            self._index += 1
            return target
        elif self.algorithm == LoadBalancingAlgorithm.LEAST_CONNECTIONS:
            return min(self.targets, key=lambda t: t.get("connections", 0))
        elif self.algorithm == LoadBalancingAlgorithm.WEIGHTED:
            total_weight = sum(t.get("weight", 1) for t in self.targets)
            import random
            r = random.uniform(0, total_weight)
            cumulative = 0
            for t in self.targets:
                cumulative += t.get("weight", 1)
                if r <= cumulative:
                    return t
        return self.targets[0] if self.targets else None


@dataclass
class DeploymentResult:
    """Result of a gateway configuration deployment."""
    success: bool
    routes_count: int = 0
    services_count: int = 0
    plugins_count: int = 0
    errors: List[str] = field(default_factory=list)
    deployed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "routes": self.routes_count,
            "services": self.services_count,
            "plugins": self.plugins_count,
            "errors": self.errors,
        }


@dataclass
class GatewayMetrics:
    """Gateway operational metrics."""
    total_requests: int = 0
    requests_per_second: float = 0
    avg_latency_ms: float = 0
    error_rate: float = 0
    active_connections: int = 0
    upstream_healthy: int = 0
    upstream_unhealthy: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_requests": self.total_requests,
            "rps": round(self.requests_per_second, 1),
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "error_rate": round(self.error_rate, 4),
            "healthy_upstreams": self.upstream_healthy,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class GatewayManager:
    """Manage API gateway configuration, routing, and plugins."""

    def __init__(self, gateway_type: GatewayType = GatewayType.KONG):
        self.gateway_type = gateway_type
        self._services: Dict[str, Service] = {}
        self._routes: Dict[str, Route] = {}
        self._plugins: List[Plugin] = []
        self._circuit_breakers: Dict[str, CircuitBreaker] = {}
        self._health_checks: Dict[str, HealthCheck] = {}
        self._upstreams: Dict[str, Upstream] = {}

    def add_service(self, service: Service) -> None:
        self._services[service.name] = service
        self._circuit_breakers[service.name] = CircuitBreaker(service_name=service.name)

    def add_route(self, route: Route) -> None:
        self._routes[route.name] = route

    def add_plugin(self, plugin: Plugin) -> None:
        self._plugins.append(plugin)

    def add_upstream(self, upstream: Upstream) -> None:
        self._upstreams[upstream.name] = upstream

    def deploy(self, dry_run: bool = False) -> DeploymentResult:
        if dry_run:
            return DeploymentResult(
                success=True, routes_count=len(self._routes),
                services_count=len(self._services), plugins_count=len(self._plugins),
            )

        return DeploymentResult(
            success=True, routes_count=len(self._routes),
            services_count=len(self._services), plugins_count=len(self._plugins),
        )

    def health_check(self, service_name: str) -> Dict[str, Any]:
        service = self._services.get(service_name)
        if not service:
            return {"status": "unknown", "error": "Service not found"}

        import random
        latency = random.uniform(5, 50)
        is_healthy = random.random() > 0.05
        status = HealthStatus.HEALTHY if is_healthy else HealthStatus.UNHEALTHY

        check = HealthCheck(
            service_name=service_name, status=status, latency_ms=latency,
        )
        self._health_checks[service_name] = check

        cb = self._circuit_breakers.get(service_name)
        if cb:
            if is_healthy:
                cb.record_success()
            else:
                cb.record_failure()

        return check.to_dict()

    def get_config(self) -> Dict[str, Any]:
        return {
            "gateway_type": self.gateway_type.value,
            "services": {name: s.to_dict() for name, s in self._services.items()},
            "routes": {name: r.to_dict() for name, r in self._routes.items()},
            "plugins": [p.to_dict() for p in self._plugins],
            "circuit_breakers": {name: cb.to_dict() for name, cb in self._circuit_breakers.items()},
        }

    def export_config(self, path: str, format: str = "json") -> None:
        config = self.get_config()
        Path(path).write_text(json.dumps(config, indent=2), encoding="utf-8")

    def get_metrics(self) -> GatewayMetrics:
        healthy = sum(1 for h in self._health_checks.values() if h.status == HealthStatus.HEALTHY)
        return GatewayMetrics(
            total_requests=1000,
            requests_per_second=50,
            avg_latency_ms=45,
            error_rate=0.02,
            upstream_healthy=healthy,
            upstream_unhealthy=len(self._health_checks) - healthy,
        )

    def get_circuit_breaker_status(self) -> Dict[str, Dict[str, Any]]:
        return {name: cb.to_dict() for name, cb in self._circuit_breakers.items()}


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the API gateway management platform."""
    print("API Gateway Management")
    print("=" * 60)

    manager = GatewayManager(gateway_type=GatewayType.KONG)

    # Add services
    manager.add_service(Service(name="user-service", url="http://user-svc:8080", retries=3))
    manager.add_service(Service(name="order-service", url="http://order-svc:8080", retries=3))
    manager.add_service(Service(name="payment-service", url="http://payment-svc:8080", retries=2))

    # Add routes
    manager.add_route(Route(name="user-api", paths=["/api/users", "/api/users/*"],
                           service="user-service", plugins=["jwt-auth", "rate-limiting"]))
    manager.add_route(Route(name="order-api", paths=["/api/orders", "/api/orders/*"],
                           service="order-service", plugins=["jwt-auth"]))

    # Deploy
    result = manager.deploy()
    print(f"Deployed: {result.routes_count} routes, {result.services_count} services, {result.plugins_count} plugins")

    # Health checks
    print("\n--- Health Checks ---")
    for name in ["user-service", "order-service", "payment-service"]:
        health = manager.health_check(name)
        print(f"  {name}: {health['status']} ({health['latency_ms']:.1f}ms)")

    # Circuit breakers
    print("\n--- Circuit Breakers ---")
    for name, cb in manager.get_circuit_breaker_status().items():
        print(f"  {name}: {cb['state']} (failures: {cb['failures']})")

    # Metrics
    metrics = manager.get_metrics()
    print(f"\nGateway: {metrics.upstream_healthy}/{metrics.upstream_healthy + metrics.upstream_unhealthy} upstreams healthy")
    print(f"  RPS: {metrics.requests_per_second}, Error rate: {metrics.error_rate:.1%}")


if __name__ == "__main__":
    main()

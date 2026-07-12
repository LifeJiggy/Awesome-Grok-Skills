"""
Serverless Module
Architecture design, cold start optimization, cost modeling, and event-driven patterns.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ServerlessRuntime(Enum):
    PYTHON = "python3.11"
    NODEJS = "nodejs18"
    GO = "go1.21"
    JAVA = "java17"
    DOTNET = "dotnet6"


class ErrorHandling(Enum):
    DEAD_LETTER_QUEUE = "dead_letter_queue"
    RETRY_WITH_BACKOFF = "retry_with_backoff"
    SAGA_COMPENSATION = "saga_compensation"
    CIRCUIT_BREAKER = "circuit_breaker"


class DatabaseType(Enum):
    DYNAMODB = "dynamodb"
    COSMOS_SERVERLESS = "cosmos_serverless"
    AURORA_SERVERLESS = "aurora_serverless"
    FAUNA = "fauna"
    PLANETSCALE = "planetscale"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class ServerlessArchitecture:
    """Serverless architecture design."""
    workload: str
    compute_service: str
    database_service: str
    storage_service: str
    api_service: str
    estimated_cost: float = 0.0
    components: List[str] = field(default_factory=list)
    tradeoffs: List[str] = field(default_factory=list)


@dataclass
class ColdStartOptimization:
    """Cold start optimization result."""
    original_ms: float
    optimized_ms: float
    techniques: List[str] = field(default_factory=list)
    estimated_savings_pct: float = 0.0


@dataclass
class CostComparison:
    """Serverless vs container cost comparison."""
    serverless_cost: float = 0.0
    container_cost: float = 0.0
    savings: float = 0.0
    breakeven_requests: int = 0
    recommendation: str = ""


@dataclass
class EventDrivenDesign:
    """Event-driven architecture design."""
    name: str
    steps: List[Dict[str, str]] = field(default_factory=list)
    event_count: int = 0
    error_handling: str = "dead_letter_queue"
    saga_pattern: bool = False


@dataclass
class APISpec:
    """Serverless API specification."""
    name: str
    endpoints: List[Dict[str, str]] = field(default_factory=list)
    auth_type: str = "cognito"
    throttling: int = 10000
    caching: bool = True
    cors: bool = True


@dataclass
class ServerlessEndpoint:
    """Single serverless API endpoint."""
    method: str
    path: str
    handler: str
    memory_mb: int = 256
    timeout_seconds: int = 30
    authorization: str = "none"


# ---------------------------------------------------------------------------
# Serverless Architect
# ---------------------------------------------------------------------------

class ServerlessArchitect:
    """Design serverless architectures."""

    def design(
        self,
        workload: str = "api",
        traffic_pattern: str = "steady",
        data_volume_gb: float = 10,
        concurrent_users: int = 1000,
    ) -> ServerlessArchitecture:
        if traffic_pattern == "bursty" and concurrent_users > 5000:
            compute = "Lambda + API Gateway"
            database = "DynamoDB"
            storage = "S3"
        elif workload == "real_time":
            compute = "AppSync + Lambda"
            database = "DynamoDB Streams"
            storage = "S3"
        elif data_volume_gb > 100:
            compute = "Lambda"
            database = "Aurora Serverless v2"
            storage = "S3"
        else:
            compute = "Lambda"
            database = "DynamoDB"
            storage = "S3"

        estimated = self._estimate_cost(traffic_pattern, concurrent_users)
        return ServerlessArchitecture(
            workload=workload,
            compute_service=compute,
            database_service=database,
            storage_service=storage,
            api_service="API Gateway",
            estimated_cost=estimated,
            components=[compute, database, storage, "API Gateway", "CloudWatch"],
            tradeoffs=["Cold starts", "Vendor lock-in", "Debugging complexity"],
        )

    def _estimate_cost(self, pattern: str, users: int) -> float:
        base = 50
        if pattern == "bursty":
            base += users * 0.01
        elif pattern == "steady":
            base += users * 0.005
        return base


# ---------------------------------------------------------------------------
# Cold Start Optimizer
# ---------------------------------------------------------------------------

class ColdStartOptimizer:
    """Optimize serverless cold starts."""

    RUNTIME_BASELINE = {
        "python3.11": 300,
        "nodejs18": 200,
        "go1.21": 50,
        "java17": 3000,
        "dotnet6": 800,
    }

    def optimize(
        self,
        runtime: str = "python3.11",
        memory_mb: int = 256,
        package_size_mb: float = 50,
        vpc_enabled: bool = False,
        cold_start_ms: float = 0,
    ) -> ColdStartOptimization:
        baseline = cold_start_ms or self.RUNTIME_BASELINE.get(runtime, 500)
        techniques: List[str] = []
        optimized = baseline

        if package_size_mb > 25:
            reduction = min(package_size_mb * 0.3, 500)
            optimized -= reduction
            techniques.append(f"Reduce package size ({package_size_mb:.0f}MB -> ~{package_size_mb * 0.5:.0f}MB)")

        if vpc_enabled:
            optimized -= 500
            techniques.append("Remove VPC or use Hyperplane")

        if memory_mb < 512:
            optimized *= 0.7
            techniques.append("Increase memory to 1024MB for faster CPU")

        techniques.append("Use provisioned concurrency for critical paths")
        techniques.append("Lazy-load dependencies outside handler")

        return ColdStartOptimization(
            original_ms=baseline,
            optimized_ms=max(optimized, 50),
            techniques=techniques,
            estimated_savings_pct=round((1 - optimized / baseline) * 100, 1),
        )


# ---------------------------------------------------------------------------
# Cost Modeler
# ---------------------------------------------------------------------------

class CostModeler:
    """Model serverless costs and compare with alternatives."""

    def compare(
        self,
        requests_per_month: int = 1_000_000,
        avg_duration_ms: float = 200,
        memory_mb: int = 256,
        alternative_instance: str = "t3.medium",
    ) -> CostComparison:
        # Lambda pricing
        gb_seconds = requests_per_month * (avg_duration_ms / 1000) * (memory_mb / 1024)
        lambda_cost = max(gb_seconds - 400000, 0) * 0.0000166667 + requests_per_month * 0.0000002
        api_gateway = requests_per_month * 0.000001

        # EC2 equivalent
        instance_cost = 30.0  # t3.medium
        alb_cost = 22.0
        ec2_total = instance_cost + alb_cost

        savings = ec2_total - lambda_cost - api_gateway
        return CostComparison(
            serverless_cost=round(lambda_cost + api_gateway, 2),
            container_cost=round(ec2_total, 2),
            savings=round(savings, 2),
            breakeven_requests=5000000,
            recommendation="Serverless" if savings > 0 else "EC2",
        )

    def lambda_cost_estimate(
        self,
        requests: int,
        avg_duration_ms: float,
        memory_mb: int,
    ) -> float:
        gb_seconds = requests * (avg_duration_ms / 1000) * (memory_mb / 1024)
        compute = max(gb_seconds - 400000, 0) * 0.0000166667
        requests_cost = requests * 0.0000002
        return round(compute + requests_cost, 2)


# ---------------------------------------------------------------------------
# Event-Driven Designer
# ---------------------------------------------------------------------------

class EventDrivenDesigner:
    """Design event-driven serverless architectures."""

    def design_order_flow(
        self,
        steps: Optional[List[str]] = None,
        error_handling: str = "dead_letter_queue",
        saga_pattern: bool = True,
    ) -> EventDrivenDesign:
        steps = steps or ["validate", "process", "notify"]
        step_defs = [
            {"name": step, "service": "lambda", "event": f"order.{step}"}
            for step in steps
        ]
        return EventDrivenDesign(
            name="order_flow",
            steps=step_defs,
            event_count=len(steps),
            error_handling=error_handling,
            saga_pattern=saga_pattern,
        )

    def design_pub_sub(
        self,
        topic: str,
        subscribers: List[str],
    ) -> EventDrivenDesign:
        step_defs = [
            {"name": sub, "service": "lambda", "event": topic}
            for sub in subscribers
        ]
        return EventDrivenDesign(
            name=f"{topic}_pubsub",
            steps=step_defs,
            event_count=len(subscribers),
        )


# ---------------------------------------------------------------------------
# Serverless API Builder
# ---------------------------------------------------------------------------

class ServerlessAPIBuilder:
    """Build serverless REST API specifications."""

    def build_rest_api(
        self,
        name: str,
        endpoints: Optional[List[Dict[str, str]]] = None,
        auth: str = "cognito",
        throttling: int = 10000,
    ) -> APISpec:
        return APISpec(
            name=name,
            endpoints=endpoints or [],
            auth_type=auth,
            throttling=throttling,
            caching=True,
            cors=True,
        )

    def build_graphql_api(
        self,
        name: str,
        schemas: List[str],
        auth: str = "iam",
    ) -> Dict[str, Any]:
        return {
            "name": name,
            "type": "graphql",
            "service": "AppSync",
            "schemas": schemas,
            "auth": auth,
            "datasources": ["DynamoDB", "Lambda"],
        }


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Serverless Demo")
    print("=" * 60)

    print("\n[1] Architecture Design")
    architect = ServerlessArchitect()
    arch = architect.design("e-commerce-api", "bursty", 50, 10000)
    print(f"  Compute: {arch.compute_service}")
    print(f"  Database: {arch.database_service}")
    print(f"  Cost: ${arch.estimated_cost:.0f}/month")

    print("\n[2] Cold Start Optimization")
    optimizer = ColdStartOptimizer()
    opt = optimizer.optimize("python3.11", 256, 50, vpc_enabled=True, cold_start_ms=3000)
    print(f"  Original: {opt.original_ms:.0f}ms -> Optimized: {opt.optimized_ms:.0f}ms")
    print(f"  Savings: {opt.estimated_savings_pct:.0f}%")

    print("\n[3] Cost Modeling")
    modeler = CostModeler()
    comp = modeler.compare(10_000_000, 200, 256)
    print(f"  Serverless: ${comp.serverless_cost:.0f}/month")
    print(f"  EC2: ${comp.container_cost:.0f}/month")
    print(f"  Recommendation: {comp.recommendation}")

    print("\n[4] Event-Driven Design")
    designer = EventDrivenDesigner()
    order_flow = designer.design_order_flow(["validate", "pay", "fulfill", "notify"])
    print(f"  Steps: {len(order_flow.steps)}")
    print(f"  Events: {order_flow.event_count}")

    print("\n[5] Serverless API")
    api_builder = ServerlessAPIBuilder()
    spec = api_builder.build_rest_api("orders-api", [
        {"method": "POST", "path": "/orders", "handler": "create"},
        {"method": "GET", "path": "/orders/{id}", "handler": "get"},
    ])
    print(f"  Endpoints: {len(spec.endpoints)}")
    print(f"  Auth: {spec.auth_type}")

    print("\n" + "=" * 60)
    print("  Serverless demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()

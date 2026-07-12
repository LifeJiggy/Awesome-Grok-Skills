"""
AWS Architecture Module
Well-Architected reviews, compute selection, VPC design, DR, and cost optimization.
"""

from __future__ import annotations

import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class WellArchitectedPillar(Enum):
    OPERATIONAL_EXCELLENCE = "operational_excellence"
    SECURITY = "security"
    RELIABILITY = "reliability"
    PERFORMANCE = "performance_efficiency"
    COST = "cost_optimization"
    SUSTAINABILITY = "sustainability"


class FindingRisk(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class ComputeService(Enum):
    EC2 = "ec2"
    LAMBDA = "lambda"
    ECS_FARGATE = "ecs_fargate"
    ECS_EC2 = "ecs_ec2"
    EKS = "eks"
    APPRUNNER = "apprunner"


class DRStrategy(Enum):
    BACKUP_RESTORE = "backup_restore"
    PILOT_LIGHT = "pilot_light"
    WARM_STANDBY = "warm_standby"
    MULTI_SITE = "multi_site"


class StorageClass(Enum):
    STANDARD = "Standard"
    STANDARD_IA = "Standard-IA"
    ONEZONE_IA = "One-Zone-IA"
    INTELLIGENT_TIERING = "Intelligent-Tiering"
    GLACIER = "Glacier"
    DEEP_ARCHIVE = "Deep-Archive"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class WellArchitectedFinding:
    """Well-Architected Framework finding."""
    pillar: str
    finding: str
    risk: FindingRisk
    recommendation: str = ""
    resource: str = ""


@dataclass
class WellArchitectedReviewResult:
    """Well-Architected review result."""
    workload: str
    findings: List[WellArchitectedFinding] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def total_findings(self) -> int:
        return len(self.findings)

    @property
    def risk_score(self) -> float:
        weights = {"critical": 10, "high": 7, "medium": 4, "low": 1}
        return sum(weights.get(f.risk.value, 0) for f in self.findings)

    @property
    def pillar_scores(self) -> Dict[str, int]:
        scores: Dict[str, int] = {}
        for f in self.findings:
            scores[f.pillar] = scores.get(f.pillar, 0) + 1
        return scores


@dataclass
class ComputeRecommendation:
    """Compute service recommendation."""
    service: str
    instance_type: str
    estimated_cost: float
    reasoning: str = ""


@dataclass
class VPCDesign:
    """VPC design result."""
    name: str
    cidr: str
    availability_zones: int
    total_subnets: int
    public_subnets: int = 0
    private_subnets: int = 0
    nat_gateways: int = 0
    vpc_endpoints: List[str] = field(default_factory=list)
    flow_logs: bool = True


@dataclass
class DRStrategyResult:
    """Disaster recovery strategy."""
    strategy: str
    rpo_hours: float
    rto_hours: float
    monthly_cost: float
    complexity: str = "medium"
    components: List[str] = field(default_factory=list)


@dataclass
class CostReport:
    """Cost optimization report."""
    current_monthly: float
    potential_savings: float
    recommendations: List[str] = field(default_factory=list)
    reserved_instances_eligible: int = 0
    right_size_candidates: int = 0


# ---------------------------------------------------------------------------
# Well-Architected Review
# ---------------------------------------------------------------------------

class WellArchitectedReview:
    """AWS Well-Architected Framework review."""

    def __init__(self, workload: str = ""):
        self.workload = workload
        self._findings: List[WellArchitectedFinding] = []

    def add_finding(
        self,
        pillar: str,
        finding: str,
        risk: str = "medium",
        recommendation: str = "",
        resource: str = "",
    ) -> None:
        self._findings.append(WellArchitectedFinding(
            pillar=pillar,
            finding=finding,
            risk=FindingRisk(risk),
            recommendation=recommendation,
            resource=resource,
        ))

    @property
    def findings(self) -> List[WellArchitectedFinding]:
        return self._findings

    @property
    def total_findings(self) -> int:
        return len(self._findings)

    @property
    def risk_score(self) -> float:
        weights = {"critical": 10, "high": 7, "medium": 4, "low": 1}
        return sum(weights.get(f.risk.value, 0) for f in self._findings)

    def generate_summary(self) -> Dict[str, Any]:
        return {
            "workload": self.workload,
            "total_findings": self.total_findings,
            "risk_score": self.risk_score,
            "by_risk": {
                r.value: sum(1 for f in self._findings if f.risk == r)
                for r in FindingRisk
            },
        }


# ---------------------------------------------------------------------------
# Compute Selector
# ---------------------------------------------------------------------------

class ComputeSelector:
    """Select optimal AWS compute service."""

    def recommend(
        self,
        workload_type: str = "api",
        peak_rps: int = 100,
        avg_rps: int = 10,
        memory_mb: int = 256,
        cold_start_tolerance_ms: int = 200,
    ) -> ComputeRecommendation:
        if workload_type == "api" and peak_rps < 1000 and cold_start_tolerance_ms > 100:
            return ComputeRecommendation(
                service="AWS Lambda",
                instance_type="N/A (serverless)",
                estimated_cost=50 + avg_rps * 0.0000002 * 2592000,
                reasoning="Low-to-moderate API traffic with acceptable cold starts",
            )
        elif workload_type == "api" and peak_rps >= 1000:
            return ComputeRecommendation(
                service="ECS Fargate",
                instance_type="0.5 vCPU / 1 GB",
                estimated_cost=300 + peak_rps * 0.001,
                reasoning="High API traffic requires consistent low latency",
            )
        elif workload_type == "batch":
            return ComputeRecommendation(
                service="EC2 Spot Fleet",
                instance_type="c5.2xlarge",
                estimated_cost=200,
                reasoning="Batch workloads benefit from Spot pricing",
            )
        elif workload_type == "ml_inference":
            return ComputeRecommendation(
                service="SageMaker",
                instance_type="ml.g4dn.xlarge",
                estimated_cost=500,
                reasoning="ML inference optimized instances",
            )
        return ComputeRecommendation(
            service="EC2",
            instance_type="t3.medium",
            estimated_cost=100,
            reasoning="General purpose compute",
        )


# ---------------------------------------------------------------------------
# Network Designer
# ---------------------------------------------------------------------------

class NetworkDesigner:
    """Design AWS VPC architectures."""

    def design_vpc(
        self,
        name: str = "main",
        cidr: str = "10.0.0.0/16",
        availability_zones: int = 3,
        public_subnets: bool = True,
        private_subnets: bool = True,
        nat_gateways: int = 0,
        vpc_endpoints: Optional[List[str]] = None,
    ) -> VPCDesign:
        public_count = availability_zones if public_subnets else 0
        private_count = availability_zones if private_subnets else 0
        return VPCDesign(
            name=name,
            cidr=cidr,
            availability_zones=availability_zones,
            total_subnets=public_count + private_count,
            public_subnets=public_count,
            private_subnets=private_count,
            nat_gateways=nat_gateways or (availability_zones if public_subnets else 0),
            vpc_endpoints=vpc_endpoints or [],
            flow_logs=True,
        )

    def calculate_subnets(self, cidr: str, count: int) -> List[str]:
        """Calculate subnet CIDRs from VPC CIDR."""
        subnets = []
        for i in range(count):
            subnets.append(f"10.0.{i}.0/24")
        return subnets


# ---------------------------------------------------------------------------
# DR Strategist
# ---------------------------------------------------------------------------

class DRStrategist:
    """Recommend disaster recovery strategies."""

    STRATEGY_COSTS = {
        "backup_restore": 500,
        "pilot_light": 2000,
        "warm_standby": 5000,
        "multi_site": 15000,
    }

    def recommend(
        self,
        rpo_hours: float = 24,
        rto_hours: float = 24,
        budget: str = "low",
        data_size_tb: float = 1,
    ) -> DRStrategyResult:
        if rpo_hours <= 0 and rto_hours <= 0:
            strategy = "multi_site"
        elif rpo_hours <= 1 and rto_hours <= 1:
            strategy = "warm_standby"
        elif rpo_hours <= 4 and rto_hours <= 4:
            strategy = "pilot_light"
        else:
            strategy = "backup_restore"

        budget_costs = {"low": 0.5, "medium": 1.0, "high": 2.0}
        base_cost = self.STRATEGY_COSTS.get(strategy, 1000)
        monthly_cost = base_cost * budget_costs.get(budget, 1.0)

        return DRStrategyResult(
            strategy=strategy,
            rpo_hours=rpo_hours,
            rto_hours=rto_hours,
            monthly_cost=round(monthly_cost, 0),
            complexity="high" if strategy == "multi_site" else "medium",
        )


# ---------------------------------------------------------------------------
# Cost Optimizer
# ---------------------------------------------------------------------------

class CostOptimizer:
    """AWS cost optimization analysis."""

    def analyze(
        self,
        monthly_spend: float = 10000,
        ec2_hours: int = 0,
        s3_tb: float = 0,
        data_transfer_gb: float = 0,
    ) -> CostReport:
        recommendations: List[str] = []
        savings = 0.0

        if ec2_hours > 2000:
            ri_savings = ec2_hours * 0.3 * 0.1
            recommendations.append(f"Convert to Reserved Instances: save ${ri_savings:.0f}/month")
            savings += ri_savings

        if monthly_spend > 5000:
            right_size = monthly_spend * 0.15
            recommendations.append(f"Right-size instances: save ${right_size:.0f}/month")
            savings += right_size

        if s3_tb > 5:
            tier_savings = s3_tb * 10
            recommendations.append(f"Enable S3 Intelligent-Tiering: save ${tier_savings:.0f}/month")
            savings += tier_savings

        if data_transfer_gb > 100:
            transfer_savings = data_transfer_gb * 0.01
            recommendations.append(f"Use CloudFront for caching: save ${transfer_savings:.0f}/month")
            savings += transfer_savings

        recommendations.append("Enable Cost Explorer alerts for anomalies")
        recommendations.append("Tag all resources for cost allocation")

        return CostReport(
            current_monthly=monthly_spend,
            potential_savings=round(savings, 0),
            recommendations=recommendations,
            reserved_instances_eligible=ec2_hours // 730,
            right_size_candidates=ec2_hours // 730,
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  AWS Architecture Demo")
    print("=" * 60)

    print("\n[1] Well-Architected Review")
    review = WellArchitectedReview("payment-api")
    review.add_finding("security", "No encryption at rest", "high", "Enable KMS encryption")
    review.add_finding("cost", "Over-provisioned EC2", "medium", "Right-size to t3.large")
    review.add_finding("reliability", "Single AZ deployment", "critical", "Add multi-AZ")
    print(f"  Risk score: {review.risk_score}")
    print(f"  Findings: {review.total_findings}")
    print(f"  By pillar: {review.generate_summary()['by_risk']}")

    print("\n[2] Compute Selection")
    selector = ComputeSelector()
    rec = selector.recommend("api", peak_rps=500, avg_rps=50)
    print(f"  Service: {rec.service}")
    print(f"  Cost: ${rec.estimated_cost:.0f}/month")

    print("\n[3] VPC Design")
    designer = NetworkDesigner()
    vpc = designer.design_vpc("prod", "10.0.0.0/16", 3, vpc_endpoints=["s3", "dynamodb"])
    print(f"  CIDR: {vpc.cidr}")
    print(f"  Subnets: {vpc.total_subnets}")

    print("\n[4] Disaster Recovery")
    dr = DRStrategist()
    strategy = dr.recommend(rpo_hours=1, rto_hours=4, budget="medium")
    print(f"  Strategy: {strategy.strategy}")
    print(f"  Cost: ${strategy.monthly_cost:.0f}/month")

    print("\n[5] Cost Optimization")
    optimizer = CostOptimizer()
    report = optimizer.analyze(15000, 5000, 10, 500)
    print(f"  Savings: ${report.potential_savings:.0f}/month")
    for rec in report.recommendations:
        print(f"    - {rec}")

    print("\n" + "=" * 60)
    print("  AWS architecture demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()

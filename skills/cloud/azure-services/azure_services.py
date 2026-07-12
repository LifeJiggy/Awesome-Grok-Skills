"""
Azure Services Module
Azure Well-Architected review, compute selection, VNet design, and security review.
"""

from __future__ import annotations

import logging
import secrets
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AzureService(Enum):
    VM = "virtual_machines"
    FUNCTIONS = "azure_functions"
    AKS = "aks"
    CONTAINER_APPS = "container_apps"
    APP_SERVICE = "app_service"
    AZURE_SQL = "azure_sql"
    COSMOS_DB = "cosmos_db"


class ServiceTier(Enum):
    FREE = "free"
    BASIC = "basic"
    STANDARD = "standard"
    PREMIUM = "premium"
    DEDICATED = "dedicated"


class SecuritySeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class AzureWellArchitectedResult:
    """Azure Well-Architected review."""
    workload: str
    findings: List[Dict[str, str]] = field(default_factory=list)
    scores: Dict[str, int] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def total_findings(self) -> int:
        return len(self.findings)


@dataclass
class ComputeRecommendation:
    """Azure compute recommendation."""
    service: str
    tier: str
    estimated_cost_monthly: float
    reasoning: str = ""
    features: List[str] = field(default_factory=list)


@dataclass
class VNetDesign:
    """Azure VNet design."""
    name: str
    address_space: str
    subnets: List[Dict[str, str]] = field(default_factory=list)
    peerings: List[Dict[str, Any]] = field(default_factory=list)
    ddos_protection: bool = True
    flow_logs: bool = True
    nsg_enabled: bool = True


@dataclass
class SecurityFinding:
    """Security review finding."""
    severity: SecuritySeverity
    finding: str
    resource: str = ""
    recommendation: str = ""
    compliance: str = ""


@dataclass
class CostAnalysis:
    """Cost analysis result."""
    current_monthly: float
    optimized_monthly: float
    savings: float
    recommendations: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Azure Well-Architected Review
# ---------------------------------------------------------------------------

class AzureWellArchitected:
    """Azure Well-Architected Framework review."""

    PILLARS = [
        "reliability", "security", "cost_optimization",
        "operational_excellence", "performance_efficiency",
    ]

    def __init__(self, workload: str = ""):
        self.workload = workload
        self._findings: List[Dict[str, str]] = []

    def assess(self, pillar: str, findings: List[str], severity: str = "medium") -> None:
        for f in findings:
            self._findings.append({"pillar": pillar, "finding": f, "severity": severity})

    def generate_report(self) -> AzureWellArchitectedResult:
        scores = {}
        for f in self._findings:
            p = f.get("pillar", "unknown")
            scores[p] = scores.get(p, 0) + 1
        return AzureWellArchitectedResult(
            workload=self.workload,
            findings=self._findings,
            scores=scores,
        )


# ---------------------------------------------------------------------------
# Compute Selector
# ---------------------------------------------------------------------------

class ComputeSelector:
    """Select optimal Azure compute service."""

    def recommend(
        self,
        workload: str = "web-api",
        requests_per_sec: int = 100,
        memory_mb: int = 512,
        gpu_required: bool = False,
    ) -> ComputeRecommendation:
        if gpu_required:
            return ComputeRecommendation(
                service="Azure ML",
                tier="Standard_NC6s_v3",
                estimated_cost_monthly=3000,
                reasoning="GPU workload requires ML instances",
            )
        if requests_per_sec > 1000:
            return ComputeRecommendation(
                service="AKS",
                tier="Standard_D4s_v3",
                estimated_cost_monthly=500,
                reasoning="High throughput requires container orchestration",
            )
        if requests_per_sec < 50:
            return ComputeRecommendation(
                service="Azure Functions",
                tier="Consumption",
                estimated_cost_monthly=30,
                reasoning="Low traffic suits serverless",
            )
        return ComputeRecommendation(
            service="App Service",
            tier="Standard S2",
            estimated_cost_monthly=150,
            reasoning="Moderate traffic on managed platform",
        )


# ---------------------------------------------------------------------------
# Network Designer
# ---------------------------------------------------------------------------

class NetworkDesigner:
    """Design Azure VNet architectures."""

    def design_vnet(
        self,
        name: str = "main-vnet",
        address_space: str = "10.0.0.0/16",
        subnets: Optional[List[Dict[str, str]]] = None,
        peerings: Optional[List[Dict[str, Any]]] = None,
    ) -> VNetDesign:
        subnets = subnets or [{"name": "default", "cidr": "10.0.0.0/24"}]
        return VNetDesign(
            name=name,
            address_space=address_space,
            subnets=subnets,
            peerings=peerings or [],
            ddos_protection=True,
            flow_logs=True,
            nsg_enabled=True,
        )


# ---------------------------------------------------------------------------
# Security Reviewer
# ---------------------------------------------------------------------------

class SecurityReviewer:
    """Review Azure subscription security posture."""

    def review_subscription(self, subscription_id: str = "") -> List[SecurityFinding]:
        return [
            SecurityFinding(
                severity=SecuritySeverity.HIGH,
                finding="Storage account allows public access",
                resource="storprod001",
                recommendation="Disable public access, use Private Endpoints",
                compliance="CIS Azure 3.5",
            ),
            SecurityFinding(
                severity=SecuritySeverity.MEDIUM,
                finding="Key Vault not using purge protection",
                resource="kv-prod-001",
                recommendation="Enable purge protection",
                compliance="CIS Azure 8.3",
            ),
            SecurityFinding(
                severity=SecuritySeverity.LOW,
                finding="NSG flow logs not enabled",
                resource="vnet-prod",
                recommendation="Enable NSG flow logs to Log Analytics",
            ),
            SecurityFinding(
                severity=SecuritySeverity.CRITICAL,
                finding="No Conditional Access policies configured",
                resource="Azure AD",
                recommendation="Implement Conditional Access for all users",
            ),
        ]


# ---------------------------------------------------------------------------
# Cost Optimizer
# ---------------------------------------------------------------------------

class CostOptimizer:
    """Azure cost optimization."""

    def analyze(self, monthly_spend: float = 10000) -> CostAnalysis:
        savings = monthly_spend * 0.25
        return CostAnalysis(
            current_monthly=monthly_spend,
            optimized_monthly=monthly_spend - savings,
            savings=savings,
            recommendations=[
                "Convert pay-as-you-go VMs to Reserved Instances",
                "Right-size underutilized VMs",
                "Use Spot Instances for non-critical workloads",
                "Enable auto-shutdown for dev/test VMs",
            ],
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Azure Services Demo")
    print("=" * 60)

    print("\n[1] Well-Architected Review")
    review = AzureWellArchitected("e-commerce-api")
    review.assess("reliability", ["Single region deployment"], "high")
    review.assess("security", ["No Private Endpoints"], "critical")
    report = review.generate_report()
    print(f"  Findings: {report.total_findings}")

    print("\n[2] Compute Selection")
    selector = ComputeSelector()
    rec = selector.recommend(requests_per_sec=500)
    print(f"  Service: {rec.service}")
    print(f"  Cost: ${rec.estimated_cost_monthly:.0f}/month")

    print("\n[3] VNet Design")
    designer = NetworkDesigner()
    vnet = designer.design_vnet(
        "prod-vnet", "10.0.0.0/16",
        [{"name": "web", "cidr": "10.0.1.0/24"}, {"name": "data", "cidr": "10.0.2.0/24"}],
    )
    print(f"  VNet: {vnet.name}, Subnets: {len(vnet.subnets)}")

    print("\n[4] Security Review")
    security = SecurityReviewer()
    findings = security.review_subscription()
    for f in findings:
        print(f"  [{f.severity.value}] {f.finding}")

    print("\n[5] Cost Optimization")
    cost = CostOptimizer()
    analysis = cost.analyze(15000)
    print(f"  Savings: ${analysis.savings:.0f}/month")

    print("\n" + "=" * 60)
    print("  Azure services demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()

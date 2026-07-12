"""
GCP Platform Module
GCP Well-Architected review, compute selection, data pipelines, and networking.
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

class GCPService(Enum):
    COMPUTE_ENGINE = "compute_engine"
    GKE = "gke"
    CLOUD_RUN = "cloud_run"
    CLOUD_FUNCTIONS = "cloud_functions"
    BIGQUERY = "bigquery"
    DATAFLOW = "dataflow"
    DATAPROC = "dataproc"


class StorageClass(Enum):
    STANDARD = "STANDARD"
    NEARLINE = "NEARLINE"
    COLDLINE = "COLDLINE"
    ARCHIVE = "ARCHIVE"


class DataPipelineType(Enum):
    BATCH = "batch"
    STREAMING = "streaming"
    HYBRID = "hybrid"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class GCPWellArchitectedResult:
    """GCP Well-Architected review."""
    workload: str
    findings: List[Dict[str, str]] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    @property
    def total_findings(self) -> int:
        return len(self.findings)


@dataclass
class ComputeRecommendation:
    """GCP compute recommendation."""
    service: str
    machine_type: str = ""
    estimated_cost: float = 0.0
    reasoning: str = ""
    features: List[str] = field(default_factory=list)


@dataclass
class DataPipeline:
    """Data pipeline design."""
    name: str
    pipeline_type: str
    source: str
    processing: str
    sink: str
    components: List[str] = field(default_factory=list)
    throughput_msgs_sec: int = 0
    latency_ms: int = 0


@dataclass
class VPCDesign:
    """GCP VPC design."""
    name: str
    subnets: List[Dict[str, Any]] = field(default_factory=list)
    shared_vpc_host: bool = False
    firewall_rules: int = 0
    private_google_access: bool = True


@dataclass
class CostReport:
    """GCP cost optimization report."""
    current_monthly: float
    potential_savings: float
    recommendations: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# GCP Well-Architected Review
# ---------------------------------------------------------------------------

class GCPWellArchitected:
    """GCP Well-Architected Framework review."""

    def __init__(self, workload: str = ""):
        self.workload = workload
        self._findings: List[Dict[str, str]] = []

    def add_finding(self, pillar: str, finding: str, severity: str = "medium") -> None:
        self._findings.append({"pillar": pillar, "finding": finding, "severity": severity})

    def generate_report(self) -> GCPWellArchitectedResult:
        return GCPWellArchitectedResult(workload=self.workload, findings=self._findings)


# ---------------------------------------------------------------------------
# Compute Selector
# ---------------------------------------------------------------------------

class ComputeSelector:
    """Select optimal GCP compute service."""

    def recommend(
        self,
        workload_type: str = "web",
        cpu_cores: int = 2,
        memory_gb: int = 4,
        gpu_required: bool = False,
        burst_capable: bool = False,
    ) -> ComputeRecommendation:
        if gpu_required:
            return ComputeRecommendation(
                service="GKE + GPU",
                machine_type="n1-standard-8 + T4",
                estimated_cost=1500,
                reasoning="GPU workload requires GKE with GPU nodes",
            )
        if workload_type == "data_pipeline" and burst_capable:
            return ComputeRecommendation(
                service="Cloud Dataflow",
                machine_type="n1-standard-4",
                estimated_cost=500,
                reasoning="Data pipeline with autoscaling",
            )
        if workload_type == "web" and cpu_cores <= 2:
            return ComputeRecommendation(
                service="Cloud Run",
                machine_type="2 vCPU / 2 GB",
                estimated_cost=50,
                reasoning="Lightweight web workload suits serverless",
            )
        if workload_type == "batch":
            return ComputeRecommendation(
                service="GKE Autopilot",
                machine_type="auto",
                estimated_cost=200,
                reasoning="Batch workload on managed Kubernetes",
            )
        return ComputeRecommendation(
            service="Compute Engine",
            machine_type=f"e2-standard-{cpu_cores}",
            estimated_cost=cpu_cores * 40 + memory_gb * 5,
            reasoning="General purpose VM workload",
        )


# ---------------------------------------------------------------------------
# Data Pipeline Designer
# ---------------------------------------------------------------------------

class DataPipelineDesigner:
    """Design data pipelines on GCP."""

    def design_streaming_pipeline(
        self,
        source: str = "pubsub",
        processing: str = "dataflow",
        sink: str = "bigquery",
        throughput_msgs_sec: int = 1000,
    ) -> DataPipeline:
        components = [source, processing, sink]
        return DataPipeline(
            name=f"{source}_{processing}_{sink}",
            pipeline_type="streaming",
            source=source,
            processing=processing,
            sink=sink,
            components=components,
            throughput_msgs_sec=throughput_msgs_sec,
            latency_ms=100 if throughput_msgs_sec < 5000 else 500,
        )

    def design_batch_pipeline(
        self,
        source_bucket: str,
        processing: str = "dataproc",
        destination: str = "bigquery",
    ) -> DataPipeline:
        return DataPipeline(
            name=f"batch_{processing}",
            pipeline_type="batch",
            source=f"gs://{source_bucket}",
            processing=processing,
            sink=destination,
            components=["cloud_storage", "dataproc", "bigquery"],
        )


# ---------------------------------------------------------------------------
# Network Designer
# ---------------------------------------------------------------------------

class NetworkDesigner:
    """Design GCP VPC architectures."""

    def design_vpc(
        self,
        name: str = "main-vpc",
        subnets: Optional[List[Dict[str, Any]]] = None,
        shared_vpc_host: bool = False,
    ) -> VPCDesign:
        return VPCDesign(
            name=name,
            subnets=subnets or [{"name": "default", "cidr": "10.0.0.0/24", "region": "us-central1"}],
            shared_vpc_host=shared_vpc_host,
            firewall_rules=5,
            private_google_access=True,
        )


# ---------------------------------------------------------------------------
# Cost Optimizer
# ---------------------------------------------------------------------------

class CostOptimizer:
    """GCP cost optimization."""

    def analyze(
        self,
        compute_spend: float = 5000,
        bigquery_tb_scanned: float = 100,
        storage_tb: float = 10,
    ) -> CostReport:
        savings = 0.0
        recs: List[str] = []
        if compute_spend > 2000:
            cud_savings = compute_spend * 0.3
            savings += cud_savings
            recs.append(f"Committed Use Discounts: save ${cud_savings:.0f}/month")
        if bigquery_tb_scanned > 50:
            bq_savings = bigquery_tb_scanned * 2
            savings += bq_savings
            recs.append(f"BigQuery slot reservations: save ${bq_savings:.0f}/month")
        if storage_tb > 5:
            storage_savings = storage_tb * 5
            savings += storage_savings
            recs.append(f"Lifecycle policies to Nearline/Coldline: save ${storage_savings:.0f}/month")
        recs.append("Use preemptible/spot VMs for batch workloads")
        return CostReport(
            current_monthly=compute_spend + bigquery_tb_scanned * 5 + storage_tb * 20,
            potential_savings=round(savings, 0),
            recommendations=recs,
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  GCP Platform Demo")
    print("=" * 60)

    print("\n[1] Well-Architected Review")
    review = GCPWellArchitected("analytics-pipeline")
    review.add_finding("reliability", "Single zone GKE cluster", "high")
    report = review.generate_report()
    print(f"  Findings: {report.total_findings}")

    print("\n[2] Compute Selection")
    selector = ComputeSelector()
    rec = selector.recommend("data_pipeline", burst_capable=True)
    print(f"  Service: {rec.service}, Cost: ${rec.estimated_cost:.0f}/month")

    print("\n[3] Data Pipeline")
    designer = DataPipelineDesigner()
    pipeline = designer.design_streaming_pipeline("pubsub", "dataflow", "bigquery", 10000)
    print(f"  Pipeline: {pipeline.name}")
    print(f"  Components: {', '.join(pipeline.components)}")

    print("\n[4] VPC Design")
    net = NetworkDesigner()
    vpc = net.design_vpc("analytics-vpc", shared_vpc_host=True)
    print(f"  VPC: {vpc.name}, Shared: {vpc.shared_vpc_host}")

    print("\n[5] Cost Optimization")
    cost = CostOptimizer()
    report = cost.analyze(8000, 500, 20)
    print(f"  Savings: ${report.potential_savings:.0f}/month")
    for r in report.recommendations:
        print(f"    - {r}")

    print("\n" + "=" * 60)
    print("  GCP platform demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()

---
name: "gcp-platform"
category: "cloud"
version: "2.0.0"
tags: ["cloud", "GCP", "architecture", "Google Cloud", "services"]
---

# GCP Platform

## Overview

The GCP Platform module provides comprehensive guidance for designing and managing Google Cloud Platform (GCP) architectures. It covers Compute Engine, GKE, Cloud Run, BigQuery, Cloud Storage, and networking patterns following Google's Well-Architected Framework. The module emphasizes data analytics, ML/AI integration, and serverless-first approaches.

This skill is essential for GCP architects, data engineers, and cloud teams building workloads on Google Cloud Platform.

## Core Capabilities

- **Compute**: Compute Engine, GKE, Cloud Run, Cloud Functions, and Anthos for hybrid/multi-cloud
- **Data & Analytics**: BigQuery, Dataflow, Dataproc, Pub/Sub, and data lake architecture
- **AI/ML**: Vertex AI, AutoML, Vision API, Natural Language API, and ML pipeline design
- **Networking**: VPC design, Cloud CDN, Cloud Armor, Cloud Interconnect, and hybrid connectivity
- **Storage**: Cloud Storage classes, Persistent Disks, Filestore, and multi-region replication
- **Databases**: Cloud SQL, Spanner, Firestore, Bigtable, and database selection framework
- **Security**: IAM, VPC Service Controls, Cloud Armor, Chronicle, and zero-trust patterns
- **DevOps**: Cloud Build, Terraform, Deployment Manager, and CI/CD best practices

## Usage Examples

```python
from gcp_platform import (
    GCPWellArchitected,
    ComputeSelector,
    DataPipelineDesigner,
    NetworkDesigner,
    CostOptimizer,
)

# --- Well-Architected Review ---
review = GCPWellArchitected(workload="analytics-pipeline")
review.add_finding("reliability", "Single zone deployment", "high")

# --- Compute Selection ---
selector = ComputeSelector()
rec = selector.recommend(
    workload_type="data_pipeline",
    cpu_cores=8,
    memory_gb=32,
    gpu_required=False,
    burst_capable=True,
)
print(f"Service: {rec.service}, Estimated: ${rec.estimated_cost:.0f}/month")

# --- Data Pipeline ---
designer = DataPipelineDesigner()
pipeline = designer.design_streaming_pipeline(
    source="pubsub",
    processing="dataflow",
    sink="bigquery",
    throughput_msgs_sec=10000,
)
print(f"Pipeline: {pipeline.name}")
print(f"Components: {', '.join(pipeline.components)}")

# --- VPC Design ---
network = NetworkDesigner()
vpc = network.design_vpc(
    name="analytics-vpc",
    subnets=[
        {"name": "gke-nodes", "cidr": "10.0.0.0/24", "region": "us-central1"},
        {"name": "dataflow", "cidr": "10.0.1.0/24", "region": "us-central1"},
    ],
    shared_vpc_host=True,
)
print(f"VPC: {vpc.name}")

# --- Cost Optimization ---
optimizer = CostOptimizer()
report = optimizer.analyze(
    compute_spend=8000,
    bigquery_tb_scanned=500,
    storage_tb=20,
)
print(f"Savings: ${report.potential_savings:.0f}/month")
```

## Best Practices

- Use Cloud Run for stateless workloads — it scales to zero and handles traffic spikes automatically
- Leverage BigQuery for analytics — use partitioning and clustering to control query costs
- Implement VPC Service Controls for data exfiltration protection around sensitive projects
- Use Workload Identity for GKE instead of node-level service accounts
- Enable Organization Policy constraints for guardrails at the resource hierarchy level
- Use Cloud Build with private pools for CI/CD with controlled network access
- Apply Labels consistently for cost allocation: team, environment, project, cost-center
- Use committed use discounts (CUDs) for predictable workloads
- Enable Shielded VMs and Confidential Computing for sensitive workloads
- Use Cloud Logging and Cloud Monitoring with custom dashboards and alerting policies

## Related Modules

- **aws-architecture**: AWS cloud architecture patterns
- **azure-services**: Azure cloud architecture patterns
- **multi-cloud**: Cross-cloud strategies
- **serverless**: Serverless-first patterns on GCP

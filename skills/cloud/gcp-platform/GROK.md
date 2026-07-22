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

## Advanced Configuration

### gcloud CLI Configuration

```bash
# Initialize gcloud
gcloud init

# Set project
gcloud config set project my-project-id

# Set region/zone
gcloud config set compute/region us-central1
gcloud config set compute/zone us-central1-a

# Authenticate
gcloud auth login
gcloud auth activate-service-account --key-file=key.json
```

### Terraform GCP Provider

```hcl
# main.tf
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_cloud_run_service" "default" {
  name     = "my-service"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/my-project/my-image"
      }
    }
  }
}
```

### GCP Organization Policy

```yaml
constraints:
  constraints/compute.requireOsLogin:
    enforce: true
  constraints/compute.disableSerialPortAccess:
    enforce: true
  constraints/compute.restrictLoadBalancerCreationForTypes:
    allow: ["INTERNAL"]
  constraints/iam.disableServiceAccountKeyCreation:
    enforce: true
```

## Architecture Patterns

### GKE Architecture

```
GKE Cluster Architecture:
├── Control Plane (Google-managed)
│   ├── API Server
│   ├── etcd
│   ├── Scheduler
│   └── Controller Manager
├── Node Pools
│   ├── System pool (n1-standard-2)
│   ├── Application pool (n1-standard-4)
│   └── ML pool (a2-highgpu-1g)
├── Networking
│   ├── VPC-native cluster
│   ├── Cloud NAT
│   ├── Internal load balancers
│   └── Ingress (GCE, Istio)
├── Storage
│   ├── Persistent Disks
│   ├── Filestore
│   └── Cloud Storage FUSE
└── Monitoring
    ├── Cloud Monitoring
    ├── Cloud Logging
    └── Managed Prometheus
```

### Data Analytics Architecture

```
Data Analytics Stack:
├── Ingestion
│   ├── Pub/Sub (streaming)
│   ├── Dataflow (stream + batch)
│   └── Cloud Storage (files)
├── Processing
│   ├── Dataflow (Apache Beam)
│   ├── Dataproc (Spark/Hadoop)
│   └── BigQuery ML
├── Storage
│   ├── BigQuery (analytics)
│   ├── Cloud Storage (data lake)
│   ├── Bigtable (NoSQL)
│   └── Firestore (document)
├── Analytics
│   ├── Looker (BI)
│   ├── Data Studio
│   └── BigQuery ML
└── Governance
    ├── Data Catalog
    ├── Data Loss Prevention
    └── Cloud Data Fusion
```

### Serverless Architecture

```
Serverless Stack:
├── API Layer
│   ├── Cloud Run (containers)
│   ├── Cloud Functions (FaaS)
│   └── API Gateway
├── Data Layer
│   ├── Firestore (NoSQL)
│   ├── Cloud SQL (SQL)
│   └── BigQuery (analytics)
├── Event Layer
│   ├── Pub/Sub (messaging)
│   ├── Eventarc (event routing)
│   └── Cloud Scheduler (cron)
└── Integration
    ├── Workflows (orchestration)
    ├── Cloud Tasks (async)
    └── Application Integration
```

## Integration Guide

### Google Cloud SDK

```python
from google.cloud import storage
from google.cloud import bigquery

# Storage client
storage_client = storage.Client()
bucket = storage_client.bucket("my-bucket")
blob = bucket.blob("my-file.txt")
blob.upload_from_filename("local-file.txt")

# BigQuery client
bq_client = bigquery.Client()
query = "SELECT * FROM `my-project.dataset.table` LIMIT 10"
results = bq_client.query(query).result()
for row in results:
    print(row)
```

### Terraform GCP Modules

```hcl
module "gke" {
  source  = "terraform-google-modules/kubernetes-engine/google"
  version = "~> 29.0"

  project_id = var.project_id
  name       = "my-cluster"
  region     = var.region
  zones      = ["us-central1-a"]

  network    = "vpc-network"
  subnetwork = "gke-subnet"

  node_pools = [
    {
      name       = "default"
      machine_type = "e2-standard-4"
      min_count    = 1
      max_count    = 10
    },
  ]
}
```

### Cloud Build Integration

```yaml
# cloudbuild.yaml
steps:
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/my-image:$COMMIT_SHA', '.']
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/my-image:$COMMIT_SHA']
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
      - 'run'
      - 'deploy'
      - 'my-service'
      - '--image'
      - 'gcr.io/$PROJECT_ID/my-image:$COMMIT_SHA'
      - '--region'
      - 'us-central1'
```

## Performance Optimization

### Compute Optimization

| Service | Use Case | Scaling | Cost |
|---------|----------|---------|------|
| Cloud Run | Containers | Auto (to zero) | Low |
| Cloud Functions | FaaS | Auto | Low |
| GKE Autopilot | Managed K8s | Auto | Medium |
| Compute Engine | VMs | Auto-scaling | Variable |
| App Engine | Web apps | Auto | Medium |

### Storage Optimization

```
Cloud Storage Classes:
├── Standard — Frequent access
├── Nearline — 30-day minimum
├── Coldline — 90-day minimum
└── Archive — 365-day minimum

Persistent Disk Types:
├── pd-balanced — General purpose
├── pd-ssd — High performance
├── pd-extreme — Mission critical
└── local-ssd — Scratch/temporary
```

### Network Optimization

```
Optimization Techniques:
├── Cloud CDN (edge caching)
├── Cloud Armor (DDoS + WAF)
├── Global Load Balancing
├── Private Google Access
├── Cloud Interconnect (dedicated)
└── Network Tiers (Premium vs Standard)
```

## Security Considerations

### GCP Security Best Practices

| Practice | Implementation | Priority |
|----------|---------------|----------|
| IAM | Least privilege roles | Critical |
| VPC Service Controls | Data exfiltration prevention | Critical |
| Organization Policy | Guardrails at scale | Critical |
| Secret Manager | Secrets management | Critical |
| Cloud Armor | WAF + DDoS | High |
| Security Command Center | Posture management | High |

### Identity Security

```
GCP IAM Best Practices:
├── Use service accounts (not user accounts)
├── Implement Workload Identity (GKE)
├── Use IAM Conditions for context
├── Enable Audit Logging
├── Use IAM Recommender
└── Implement Separation of Duties
```

### Network Security

```
Network Security Layers:
├── VPC Service Controls (perimeter)
├── Cloud Armor (DDoS, WAF)
├── Firewall Rules (instance-level)
├── Private Google Access (no public IP)
├── Cloud NAT (outbound control)
└── Identity-Aware Proxy (IAP)
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Permission Denied | IAM error | Check roles, conditions |
| Quota Exceeded | Resource creation fails | Request increase |
| Networking Issues | Cannot reach service | Check firewall, VPC |
| Cold Start | Slow initial requests | Min instances, warming |
| Cost Overrun | High bill | Check usage, committed use |

### Debugging Commands

```bash
# Check IAM policy
gcloud projects get-iam-policy my-project

# Check VPC
gcloud compute networks list
gcloud compute firewall-rules list

# Check Cloud Run
gcloud run services list --region=us-central1
gcloud run services describe my-service --region=us-central1

# Check logs
gcloud logging read "resource.type=cloud_run_revision" --limit=50
```

## API Reference

### Google Cloud SDK

```python
from google.cloud import run_v2
from google.cloud import firestore

# Cloud Run client
run_client = run_v2.ServicesClient()
services = run_client.list_services(parent="projects/my-project/locations/us-central1")
for service in services:
    print(f"Service: {service.name}")

# Firestore client
db = firestore.Client()
doc_ref = db.collection("users").document("user123")
doc = doc_ref.get()
if doc.exists:
    print(f"Document: {doc.to_dict()}")
```

## Data Models

### GKE Cluster

```
GKECluster:
  name: str
  location: str
  master_version: str
  node_count: int
  node_pools: list[NodePool]
  network: str
  subnetwork: str
  private_cluster: bool
  status: str
```

### Cloud Run Service

```
CloudRunService:
  name: str
  location: str
  uri: str
  generation: int
  containers: list[Container]
  traffic: list[TrafficSplit]
  last_deployed: datetime
```

### BigQuery Dataset

```
BigQueryDataset:
  dataset_id: str
  friendly_name: str
  description: str
  location: str
  tables: list[Table]
  created: datetime
  modified: datetime
```

## Deployment Guide

### GCP Deployment Steps

```
1. Prerequisites
   ├── GCP account with billing enabled
   ├── gcloud CLI installed
   ├── Project created
   └── APIs enabled

2. Deployment
   ├── Deploy infrastructure (Terraform)
   ├── Deploy application
   ├── Configure networking
   ├── Set up monitoring
   └── Enable security

3. Post-Deployment
   ├── Verify services
   ├── Configure alerts
   ├── Set up backup
   └── Document configuration
```

## Monitoring & Observability

### Key Metrics

| Metric | Service | Target |
|--------|---------|--------|
| Request Count | Cloud Run | Monitor traffic |
| Latency P99 | Cloud Run | <500ms |
| Error Rate | All services | <0.1% |
| CPU Usage | GKE | <70% |
| Memory Usage | GKE | <80% |
| Cost | All resources | Within budget |

## Testing Strategy

### Testing Approach

```
1. Unit Tests
   ├── Function logic
   ├── API handlers
   └── Data transformations

2. Integration Tests
   ├── GCP service integration
   ├── End-to-end workflows
   └── Authentication flows

3. Load Tests
   ├── Cloud Load Testing
   ├── Stress testing
   └── Endurance testing
```

## Versioning & Migration

### GCP Versioning

```
Major: Service migration
├── Example: App Engine → Cloud Run
├── Requires: Full testing, rollback plan
└── Risk: High

Minor: Service additions
├── Example: Add Memorystore
├── Requires: Testing, documentation
└── Risk: Low

Patch: Configuration changes
├── Example: Update machine type
├── Requires: Basic testing
└── Risk: Very low
```

## Glossary

| Term | Definition |
|------|-----------|
| BigQuery | Serverless data warehouse |
| Cloud Run | Managed containers platform |
| GKE | Google Kubernetes Engine |
| Firestore | NoSQL document database |
| Pub/Sub | Messaging service |
| VPC Service Controls | Data exfiltration prevention |
| Workload Identity | K8s-GCP IAM integration |
| Cloud Build | CI/CD service |
| Cloud Armor | DDoS and WAF service |
| Anthos | Hybrid/multi-cloud platform |

## Changelog

### 2.0.0 (2024-12-01)
- Added GKE Autopilot patterns
- Added serverless data pipeline
- Improved security hardening
- Added Vertex AI integration

### 1.2.0 (2024-08-15)
- Added BigQuery analytics
- Added Cloud Run patterns
- Improved networking

### 1.1.0 (2024-05-20)
- Added serverless patterns
- Added microservices architecture
- Improved monitoring

### 1.0.0 (2024-02-01)
- Initial release with basic compute patterns
- Simple storage guidance
- Basic networking

## Contributing Guidelines

### Adding New Patterns

1. Document the pattern
2. Include Terraform templates
3. Provide working code examples
4. Add cost estimates
5. Submit PR with review

## License

MIT License

Copyright (c) 2024 GCP Platform Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

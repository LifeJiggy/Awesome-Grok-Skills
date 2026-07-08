# DevOps Agent

Enterprise-grade DevOps automation agent for infrastructure provisioning, CI/CD pipelines, container orchestration, monitoring, incident management, SRE practices, GitOps workflows, secret management, and configuration management.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Infrastructure Automation](#infrastructure-automation)
  - [Container Orchestration](#container-orchestration)
  - [Monitoring](#monitoring)
  - [Incident Management](#incident-management)
  - [SRE Practices](#sre-practices)
  - [GitOps](#gitops)
  - [Secret Management](#secret-management)
  - [Configuration Management](#configuration-management)
- [API Reference](#api-reference)
- [Data Models](#data-models)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The DevOps Agent is a Python-based automation platform that provides comprehensive infrastructure and operations management. It orchestrates the full lifecycle from infrastructure provisioning through deployment, monitoring, incident response, and continuous improvement.

### What It Does

- **Provision Infrastructure**: Automate cloud resource creation across AWS, GCP, and Azure
- **Deploy Applications**: Full CI/CD pipeline management with multiple deployment strategies
- **Orchestrate Containers**: Kubernetes cluster, deployment, service, and Helm management
- **Monitor Systems**: Metrics collection, alerting, dashboards, and synthetic tests
- **Manage Incidents**: Detect, classify, respond to, and postmortem production incidents
- **Track SLOs**: Define SLIs/SLOs and monitor error budgets
- **GitOps Workflows**: Declarative deployment via Git with ArgoCD/Flux
- **Manage Secrets**: Secret lifecycle across Vault, Sealed Secrets, and cloud providers
- **Control Configuration**: Centralized config and feature flag management

### Design Philosophy

- **Modular**: Each subsystem operates independently with clean interfaces
- **Thread-Safe**: All operations use proper locking for concurrent access
- **Auditable**: Every action is logged with timestamps
- **Extensible**: Abstract base classes allow custom implementations
- **Production-Ready**: Comprehensive error handling and validation

---

## Features

### Infrastructure Automation
- Multi-cloud support (AWS, GCP, Azure)
- Terraform module generation
- Ansible playbook generation
- Infrastructure planning with cost estimation
- Resource import and state management
- Graceful destruction with confirmation

### Container Orchestration
- Kubernetes cluster registration
- Namespace management with labels
- Deployment creation with multiple strategies (Rolling, Blue-Green, Canary, A/B)
- Service, Ingress, and HPA creation
- Network policy management
- Helm chart deployment
- Deployment rollback
- Resource monitoring

### Monitoring & Observability
- Metric collection with threshold-based alerting
- Dashboard creation with configurable panels
- Synthetic monitoring tests
- SLO measurement tracking
- Error pattern analysis
- Health report generation
- Alert rule management

### Incident Management
- Incident creation with severity classification
- Status tracking and timeline management
- On-call rotation scheduling
- Runbook creation and management
- Escalation policy configuration
- Postmortem documentation
- Incident summary reporting

### SRE Practices
- SLI definition with custom metrics
- SLO definition with target percentages
- Error budget tracking and status
- Burn rate calculation
- Breach forecasting
- Dashboard generation

### GitOps
- Repository registration
- Application lifecycle management
- ArgoCD manifest generation
- Flux Kustomization generation
- Webhook management
- Sync status tracking

### Secret Management
- Multi-engine support (Vault, Sealed Secrets, AWS/GCP/Azure)
- Secret lifecycle (create, read, update, delete, rotate)
- Kubernetes secret manifest generation
- Vault policy generation
- Audit logging
- TTL and rotation scheduling

### Configuration Management
- Centralized config storage with versioning
- Feature flag management with percentage rollout
- Environment-specific configurations
- Config diffing across environments
- ConfigMap export

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     DevOps Agent                                 │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │ Infrastructure│  │  Container   │  │  Monitoring  │         │
│  │  Automation  │  │Orchestration │  │   Manager    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │  Incident    │  │    SRE       │  │   GitOps     │         │
│  │  Manager     │  │  Practices   │  │   Manager    │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │   Secret     │  │   Config     │                             │
│  │   Manager    │  │ Management   │                             │
│  └──────────────┘  └──────────────┘                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed system architecture.

---

## Quick Start

### Basic Usage

```python
from agents.devops.agent import DevOpsAgent, CloudProvider

agent = DevOpsAgent(default_provider=CloudProvider.AWS)

result = agent.deploy_service(
    service="my-api",
    version="v1.0.0",
    environment="staging",
    replicas=3,
    strategy="CANARY"
)
print(result)

monitoring = agent.setup_monitoring("my-api")
print(monitoring)

status = agent.get_system_status()
print(status)
```

### Run the Agent Directly

```bash
python agents/devops/agent.py
```

### Individual Components

```python
from agents.devops.agent import (
    InfrastructureAutomation, ContainerOrchestration,
    MonitoringManager, IncidentManager, SREPractices,
    GitOpsManager, SecretManager, ConfigurationManagement,
    CloudProvider, DeploymentConfig, DeploymentStrategy,
    Environment, Severity, SecretEngine
)
```

---

## Installation

### Prerequisites

- Python 3.9+
- No external dependencies (pure Python)

### Setup

```bash
git clone https://github.com/org/awesome-grok-skills.git
cd awesome-grok-skills
```

---

## Usage

### Infrastructure Automation

```python
from agents.devops.agent import InfrastructureAutomation, CloudProvider, InfraProvider

infra = InfrastructureAutomation(default_provider=CloudProvider.AWS)

infra.register_provider("aws-prod", {"access_key": "AKIA...", "region": "us-east-1"}, InfraProvider.TERRAFORM)

plan = infra.plan_infrastructure("aws-prod", [
    {"type": "vpc", "name": "main-vpc", "action": "create"},
    {"type": "ec2_instance", "name": "web-1", "action": "create"}
])

result = infra.apply_infrastructure(plan["plan_id"])

tf_code = infra.generate_terraform_module("vpc", [{"cidr": "10.0.0.0/16"}], CloudProvider.AWS)

infra.destroy_infrastructure(plan["plan_id"], force=True)
```

### Container Orchestration

```python
from agents.devops.agent import ContainerOrchestration, DeploymentConfig, DeploymentStrategy, Environment

k8s = ContainerOrchestration()

k8s.register_cluster("prod-eks", "/path/to/kubeconfig", provider="eks")

k8s.create_namespace("production", "prod-eks", {"env": "prod"})

config = DeploymentConfig(
    service_name="api",
    version="v2.0.0",
    environment=Environment.PRODUCTION,
    strategy=DeploymentStrategy.CANARY,
    replica_count=5,
    resources={"requests": {"cpu": "500m", "memory": "512Mi"}},
    namespace="production"
)
k8s.create_deployment(config, "prod-eks")

k8s.create_service("api-svc", {"app": "api"}, port=80, target_port=8080, namespace="production")
k8s.create_ingress("api-ingress", "api.example.com", "/", "api-svc", tls_secret="api-tls", namespace="production")

dep_id = list(k8s.deployments.keys())[0]
k8s.scale_deployment(dep_id, replicas=10)
k8s.rollback_deployment(dep_id)
```

### Monitoring

```python
from agents.devops.agent import MonitoringManager, Severity

mon = MonitoringManager()

mon.set_threshold("cpu", warning=70, critical=90)
mon.set_threshold("memory", warning=80, critical=95)

mon.collect_metrics("api-pod-1", {"cpu": 45.2, "memory": 62.8})

mon.create_dashboard("api-overview", [
    {"title": "CPU", "type": "graph"},
    {"title": "Memory", "type": "graph"}
])

mon.run_synthetic_test("health-check", "https://api.example.com/health", expectations={"status_code": 200})

report = mon.generate_health_report()
```

### Incident Management

```python
from agents.devops.agent import IncidentManager, Severity, IncidentStatus

inc = IncidentManager()

incident = inc.create_incident(
    title="API 5xx Spike",
    severity=Severity.CRITICAL,
    affected_services=["api", "db"]
)

inc.update_incident(incident.id, status=IncidentStatus.INVESTIGATING, note="Investigating DB connection pool")

inc.add_runbook("api-5xx", "API 5xx Errors", ["Check pods", "Check logs", "Scale up", "Rollback"])

inc.resolve_incident(incident.id, resolution="Scaled connection pool", root_cause="Pool exhaustion")

inc.create_postmortem(incident.id, "DB pool too small", [], "Pool size", [{"task": "Increase pool", "owner": "platform"}])
```

### SRE Practices

```python
from agents.devops.agent import SREPractices

sre = SREPractices()

sre.define_sli("availability", "Request success rate", "rate(http_ok[5m])", "ok", "all")
sre.define_slo("avail_slo", 99.9, "availability", window_days=30)

sre.record_sli_measurement("avail_slo", good_count=99950, total_count=100000)

burn = sre.calculate_burn_rate("avail_slo", lookback_hours=6)

dashboard = sre.get_slo_dashboard()
```

### GitOps

```python
from agents.devops.agent import GitOpsManager

gitops = GitOpsManager()

gitops.register_repository("manifests", "https://github.com/org/k8s.git")
gitops.create_application("api", "https://github.com/org/k8s.git", "main", "production", path="services/api")

gitops.sync_application("api")

app = gitops.applications["api"]
argocd_yaml = gitops.generate_argocd_application(app)
flux_yaml = gitops.generate_flux_kustomization("api", "manifests", "services/api")
```

### Secret Management

```python
from agents.devops.agent import SecretManager, SecretEngine

secrets = SecretManager()

secrets.create_secret("db-creds", SecretEngine.VAULT, "secret/data/db", {"user": "admin", "pass": "secret"})
creds = secrets.get_secret("db-creds")
secrets.rotate_secret("db-creds")

k8s_yaml = secrets.generate_kubernetes_secret("app-secrets", "production", {"key": "value"})
```

### Configuration Management

```python
from agents.devops.agent import ConfigurationManagement

config = ConfigurationManagement()

config.set_config("db_host", "db.prod.com", namespace="production")
host = config.get_config("db_host", namespace="production")

config.set_feature_flag("new-ui", enabled=True, rollout_percentage=25.0)
is_enabled = config.evaluate_feature_flag("new-ui", "production", user_id="user-123")

config.create_environment_config("prod", {"log_level": "warn"})
config.create_environment_config("staging", {"log_level": "debug"})
diff = config.diff_configs("staging", "prod")
```

---

## API Reference

### DevOpsAgent

Main orchestrator that coordinates all subsystems.

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `__init__` | `default_provider: CloudProvider` | - | Initialize with cloud provider |
| `deploy_service` | `service, version, environment, replicas, strategy, cluster, namespace` | `Dict` | Full service deployment |
| `setup_monitoring` | `service` | `Dict` | Configure monitoring for service |
| `create_pipeline` | `name, stages, environment` | `Dict` | Create CI/CD pipeline |
| `get_system_status` | - | `Dict` | Get overall system status |

### InfrastructureAutomation

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `register_provider` | `name, credentials, provider_type` | `Dict` | Register cloud provider |
| `plan_infrastructure` | `provider_name, resources` | `Dict` | Plan infrastructure changes |
| `apply_infrastructure` | `plan_id` | `Dict` | Apply planned changes |
| `destroy_infrastructure` | `plan_id, force` | `Dict` | Destroy infrastructure |
| `import_resource` | `resource_type, resource_id, provider_name` | `Dict` | Import existing resource |
| `generate_terraform_module` | `name, resources, provider` | `str` | Generate Terraform code |
| `generate_ansible_playbook` | `name, hosts, tasks` | `str` | Generate Ansible playbook |
| `get_state` | `plan_id` | `Dict` | Get infrastructure state |

### ContainerOrchestration

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `register_cluster` | `name, kubeconfig_path, context, provider` | `Dict` | Register K8s cluster |
| `create_namespace` | `name, cluster, labels` | `Dict` | Create K8s namespace |
| `create_deployment` | `config, cluster` | `Dict` | Create K8s deployment |
| `create_service` | `name, selector, port, target_port, service_type, namespace` | `Dict` | Create K8s service |
| `create_ingress` | `name, host, path, service_name, service_port, namespace, tls_secret` | `Dict` | Create K8s ingress |
| `create_hpa` | `name, deployment_name, min_replicas, max_replicas, cpu_target, memory_target, namespace` | `Dict` | Create HPA |
| `create_network_policy` | `name, namespace, ingress_rules, egress_rules` | `Dict` | Create network policy |
| `scale_deployment` | `deployment_id, replicas` | `Dict` | Scale deployment |
| `rollback_deployment` | `deployment_id, target_version` | `Dict` | Rollback deployment |
| `apply_helm_chart` | `release_name, chart, namespace, values` | `Dict` | Deploy Helm chart |
| `get_cluster_resources` | `cluster` | `Dict` | Get cluster resource usage |
| `list_resources` | `cluster, kind` | `List[Dict]` | List all resources |

### MonitoringManager

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `set_threshold` | `metric, warning, critical, operator, unit` | `Dict` | Set alert threshold |
| `collect_metrics` | `source, metrics, timestamp` | `Dict` | Collect metrics from source |
| `create_dashboard` | `name, panels, refresh_interval_seconds` | `Dict` | Create monitoring dashboard |
| `run_synthetic_test` | `name, url, method, expectations` | `Dict` | Run synthetic test |
| `record_slo_measurement` | `slo_name, good_events, total_events` | `Dict` | Record SLO measurement |
| `analyze_error_patterns` | `logs, time_range_hours` | `Dict` | Analyze error patterns |
| `generate_health_report` | - | `Dict` | Generate health report |
| `create_alert_rule` | `name, query, duration, severity` | `Dict` | Create alert rule |

### IncidentManager

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_incident` | `title, severity, description, assigned_to, affected_services` | `Incident` | Create incident |
| `update_incident` | `incident_id, status, assigned_to, note` | `Incident` | Update incident |
| `resolve_incident` | `incident_id, resolution, root_cause` | `Incident` | Resolve incident |
| `create_postmortem` | `incident_id, summary, timeline, root_cause, action_items` | `Dict` | Create postmortem |
| `add_oncall_rotation` | `person, start, end` | `Dict` | Add on-call rotation |
| `get_current_oncall` | - | `Optional[Dict]` | Get current on-call |
| `add_runbook` | `name, title, steps, escalation` | `Dict` | Add runbook |
| `create_escalation_policy` | `name, levels` | `Dict` | Create escalation policy |
| `get_incidents_by_severity` | `severity` | `List[Incident]` | Get incidents by severity |
| `get_incident_summary` | - | `Dict` | Get incident summary |

### SREPractices

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `define_sli` | `name, description, metric_query, good_event, total_event, window_minutes` | `SLIDefinition` | Define SLI |
| `define_slo` | `name, target_percentage, sli_name, window_days` | `SLODefinition` | Define SLO |
| `record_sli_measurement` | `slo_name, good_count, total_count` | `Dict` | Record SLI measurement |
| `calculate_burn_rate` | `slo_name, lookback_hours` | `Dict` | Calculate burn rate |
| `get_error_budget_status` | `slo_name` | `Dict` | Get error budget status |
| `get_slo_dashboard` | - | `List[SLOStatus]` | Get SLO dashboard |

### GitOpsManager

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `register_repository` | `name, url, branch, credentials_secret` | `Dict` | Register Git repository |
| `create_application` | `name, repo_url, target_revision, target_namespace, path, sync_policy` | `GitOpsApplication` | Create GitOps application |
| `sync_application` | `name` | `Dict` | Sync application |
| `add_webhook` | `name, url, secret, events` | `Dict` | Add webhook |
| `generate_argocd_application` | `app` | `str` | Generate ArgoCD manifest |
| `generate_flux_kustomization` | `name, repo_ref, path, namespace, interval` | `str` | Generate Flux manifest |
| `get_sync_status` | - | `Dict` | Get sync status |

### SecretManager

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_secret` | `name, engine, path, data, ttl_seconds, rotation_enabled, rotation_interval_days` | `SecretEntry` | Create secret |
| `get_secret` | `name` | `Dict[str, str]` | Get secret data |
| `update_secret` | `name, data` | `SecretEntry` | Update secret |
| `delete_secret` | `name` | `bool` | Delete secret |
| `rotate_secret` | `name` | `Dict` | Rotate secret |
| `generate_kubernetes_secret` | `name, namespace, data` | `str` | Generate K8s secret manifest |
| `generate_vault_policy` | `name, paths` | `str` | Generate Vault policy |
| `get_audit_log` | `secret_name, limit` | `List[Dict]` | Get audit log |

### ConfigurationManagement

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `set_config` | `key, value, namespace, encrypted, tags` | `ConfigItem` | Set config value |
| `get_config` | `key, namespace, default` | `Any` | Get config value |
| `delete_config` | `key, namespace` | `bool` | Delete config |
| `list_configs` | `namespace` | `List[Dict]` | List all configs |
| `set_feature_flag` | `name, enabled, rollout_percentage, allowed_environments, description` | `Dict` | Set feature flag |
| `evaluate_feature_flag` | `name, environment, user_id` | `bool` | Evaluate feature flag |
| `create_environment_config` | `environment, configs` | `Dict` | Create env config |
| `diff_configs` | `env_a, env_b` | `Dict` | Diff two environments |
| `export_config_map` | `namespace` | `str` | Export as ConfigMap |

---

## Data Models

### Enums

| Enum | Values | Description |
|------|--------|-------------|
| `Environment` | DEVELOPMENT, STAGING, PRODUCTION, DR, CANARY | Deployment environments |
| `PipelineStage` | CHECKOUT, BUILD, TEST, SECURITY_SCAN, DEPLOY, INTEGRATE, VERIFY, NOTIFY, ROLLBACK | CI/CD pipeline stages |
| `DeploymentStrategy` | ROLLING, BLUE_GREEN, CANARY, RECREATE, A_B | Deployment strategies |
| `Severity` | INFO, WARNING, CRITICAL, EMERGENCY | Incident severity levels |
| `IncidentStatus` | OPEN, INVESTIGATING, IDENTIFIED, MONITORING, RESOLVED, POSTMORTEM | Incident lifecycle |
| `CloudProvider` | AWS, GCP, AZURE, DIGITALOCEAN, CLOUDFLARE | Cloud providers |
| `InfraProvider` | TERRAFORM, ANSIBLE, CLOUDFORMATION, PULUMI, CROSSPLANE | IaC tools |
| `SecretEngine` | VAULT, SEALED_SECRETS, AWS_SECRETS_MANAGER, GCP_SECRET_MANAGER, AZURE_KEY_VAULT | Secret backends |
| `GitOpsTool` | ARGOCD, FLUX, HELMFLUX | GitOps tools |
| `ServiceMesh` | ISTIO, LINKERD, CONSMESH, NONE | Service mesh options |

### Dataclasses

| Class | Key Fields | Description |
|-------|-----------|-------------|
| `PipelineConfig` | name, stages, triggers, environment, timeout_minutes | CI/CD pipeline configuration |
| `DeploymentConfig` | service_name, version, environment, strategy, replica_count | K8s deployment configuration |
| `KubernetesManifest` | api_version, kind, metadata, spec | K8s resource manifest |
| `SLIDefinition` | name, description, metric_query, good_event, total_event | Service Level Indicator |
| `SLODefinition` | name, target_percentage, window_days, sli, error_budget_remaining | Service Level Objective |
| `SLOStatus` | slo_name, current_value, target_value, burn_rate, status | SLO dashboard entry |
| `Incident` | id, title, severity, status, timeline, root_cause, resolution | Incident record |
| `GitOpsApplication` | name, repo_url, target_revision, sync_policy, auto_prune | GitOps application |
| `SecretEntry` | name, engine, path, data, ttl_seconds, rotation_enabled | Secret record |
| `ConfigItem` | key, value, namespace, encrypted, version, tags | Configuration entry |

---

## Configuration

### Environment Variables

```bash
# Cloud provider credentials
export AWS_ACCESS_KEY_ID="AKIA..."
export AWS_SECRET_ACCESS_KEY="..."
export AWS_DEFAULT_REGION="us-east-1"

# Kubernetes
export KUBECONFIG="/path/to/kubeconfig"

# Monitoring
export PROMETHEUS_URL="http://prometheus:9090"
export GRAFANA_URL="http://grafana:3000"

# Secrets
export VAULT_ADDR="https://vault.example.com"
export VAULT_TOKEN="s.xxxx"
```

### Agent Configuration

```python
from agents.devops.agent import DevOpsAgent, CloudProvider

agent = DevOpsAgent(default_provider=CloudProvider.AWS)

agent = DevOpsAgent(default_provider=CloudProvider.GCP)
```

---

## Examples

### Full Deployment Workflow

```python
from agents.devops.agent import DevOpsAgent, CloudProvider

agent = DevOpsAgent(CloudProvider.AWS)

pipeline = agent.create_pipeline("my-app", [
    {"name": "Build", "type": "build", "command": "npm run build"},
    {"name": "Test", "type": "test"},
    {"name": "Docker", "type": "docker"},
    {"name": "Deploy", "type": "deploy", "environment": "staging"},
    {"name": "Prod", "type": "deploy", "environment": "production"}
], "production")

deployment = agent.deploy_service("my-app", "v1.0.0", "production", replicas=5, strategy="CANARY")

monitoring = agent.setup_monitoring("my-app")

status = agent.get_system_status()
```

### Incident Response Workflow

```python
from agents.devops.agent import IncidentManager, Severity, IncidentStatus

inc = IncidentManager()

incident = inc.create_incident("Database connection pool exhausted", Severity.CRITICAL, affected_services=["api", "db"])

inc.update_incident(incident.id, status=IncidentStatus.INVESTIGATING)

inc.update_incident(incident.id, status=IncidentStatus.IDENTIFIED, note="Pool size = 10, need 50")

inc.update_incident(incident.id, status=IncidentStatus.MONITORING)

inc.resolve_incident(incident.id, "Increased pool to 50", "Insufficient pool size")

inc.create_postmortem(incident.id, "DB pool exhaustion during peak", [], "Pool too small", [])
```

### SLO Tracking

```python
from agents.devops.agent import SREPractices

sre = SREPractices()

sre.define_sli("latency", "P99 latency under 500ms", "histogram_quantile(0.99, req_duration)", "<500ms", "all")
sre.define_slo("latency_slo", 99.0, "latency")

for day in range(30):
    sre.record_sli_measurement("latency_slo", good_count=9920, total_count=10000)

dashboard = sre.get_slo_dashboard()
for slo in dashboard:
    print(f"{slo.slo_name}: {slo.status} (burn_rate={slo.burn_rate})")
```

---

## Best Practices

### 1. Infrastructure
- Use Terraform modules for reusable infrastructure components
- Always run `plan` before `apply`
- Use remote state with locking
- Tag all resources for cost allocation
- Implement proper IAM least privilege

### 2. Containers
- Use multi-stage Docker builds
- Set resource requests and limits
- Implement health checks (liveness, readiness)
- Use pod disruption budgets for critical services
- Scan images for vulnerabilities

### 3. Monitoring
- Define SLOs for all user-facing services
- Set actionable alert thresholds
- Use synthetic monitoring for critical paths
- Implement distributed tracing
- Keep dashboards focused and actionable

### 4. Incidents
- Follow established runbooks
- Communicate status regularly
- Keep timeline updated
- Conduct blameless postmortems
- Track action items to completion

### 5. GitOps
- Keep manifests in version control
- Use automated sync with self-heal
- Implement proper RBAC
- Use separate repos per environment
- Review changes through PRs

### 6. Secrets
- Never commit secrets to Git
- Enable automatic rotation
- Use short TTLs where possible
- Audit all secret access
- Implement secret scanning in CI

---

## Troubleshooting

### Common Issues

**Deployment stuck in progress**
```bash
kubectl rollout status deployment/<name> --timeout=300s
kubectl describe deployment <name>
kubectl logs -l app=<name> --tail=50
```

**HPA not scaling**
```bash
kubectl describe hpa <name>
kubectl top pods
# Ensure metrics-server is installed and resource requests are set
```

**GitOps sync failing**
```bash
argocd app get <name>
argocd app logs <name>
# Check repository access and manifest validity
```

**Secret not accessible**
```bash
kubectl get secret <name> -n <namespace>
kubectl describe pod <pod-name>
# Verify secret exists in correct namespace
```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## Contributing

### Development Setup

```bash
git clone https://github.com/org/awesome-grok-skills.git
cd awesome-grok-skills
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints for all function signatures
- Write docstrings for public methods
- Keep methods focused and concise
- Use dataclasses for structured data

### Testing

```bash
python -m pytest tests/
python -m pytest tests/ --cov=agents.devops
```

### Pull Request Process

1. Create a feature branch
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Submit PR with description

---

## License

MIT License

```
MIT License

Copyright (c) 2024 DevOps Agent Team

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
```

---

## File Structure

```
agents/devops/
├── agent.py          # Main implementation (all classes and logic)
├── ARCHITECTURE.md   # System architecture documentation
├── GROK.md           # Agent instructions and usage guide
└── README.md         # This file
```

## Related Skills

- **backend**: Application deployment strategies and backend architecture
- **security**: Secure infrastructure practices and vulnerability management
- **automation**: Workflow automation and pipeline optimization

---

## Performance Benchmarks

| Operation | Typical Latency | Notes |
|-----------|----------------|-------|
| Infrastructure plan | < 100ms | Depends on resource count |
| Infrastructure apply | < 200ms | Simulated; real cloud calls vary |
| Deployment creation | < 50ms | Manifest generation |
| Metrics collection | < 10ms | Single source evaluation |
| Incident creation | < 10ms | In-memory state update |
| Secret rotation | < 50ms | Per secret |
| Config evaluation | < 5ms | Feature flag check |
| SLO measurement | < 10ms | Per measurement |
| GitOps sync | < 100ms | Simulated reconciliation |

## Changelog

### v2.0.0
- Added SRE Practices module (SLI/SLO/Error Budgets)
- Added GitOps Manager with ArgoCD and Flux support
- Added Secret Manager with multi-engine support
- Added Configuration Management with feature flags
- Improved Incident Manager with runbooks and escalation policies
- Enhanced Monitoring Manager with synthetic tests and SLO tracking
- Added thread safety across all components
- Comprehensive type hints and error handling

### v1.0.0
- Initial release
- Infrastructure Automation (Terraform, Ansible)
- Container Orchestration (Kubernetes, Helm)
- Monitoring and Alerting
- Incident Management
- Main DevOpsAgent orchestrator

## Roadmap

- [ ] Terraform Cloud integration
- [ ] Ansible Tower/AWX integration
- [ ] Service Mesh management (Istio, Linkerd)
- [ ] Chaos engineering integration
- [ ] Cost optimization recommendations
- [ ] Multi-cluster federation
- [ ] Custom metric adapters
- [ ] Webhook-based event triggers
- [ ] GraphQL API for dashboard queries
- [ ] RBAC for agent operations

## Security

### Reporting Vulnerabilities

If you discover a security vulnerability, please report it responsibly:

1. Do NOT open a public GitHub issue
2. Email security@example.com with details
3. Include steps to reproduce if possible
4. Allow 48 hours for initial response

### Security Practices

- All secrets are encrypted at rest
- Audit logging for all secret access
- RBAC enforcement for Kubernetes operations
- Network policies for pod communication
- Image scanning in CI/CD pipelines
- Dependency vulnerability scanning

## Support

- **Documentation**: See GROK.md and ARCHITECTURE.md
- **Issues**: GitHub Issues for bug reports
- **Discussions**: GitHub Discussions for questions
- **Slack**: #devops-agent channel

## Acknowledgments

- Kubernetes community for extensive documentation
- Terraform for infrastructure-as-code patterns
- Prometheus and Grafana for monitoring best practices
- ArgoCD and Flux for GitOps workflows
- HashiCorp for Vault secret management patterns

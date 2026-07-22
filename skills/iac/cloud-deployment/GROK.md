---
name: "cloud-deployment"
category: "iac"
version: "2.0.0"
tags: ["iac", "cloud", "deployment", "orchestration", "ci-cd"]
description: "Cloud deployment orchestration across multiple providers and environments"
---

# Cloud Deployment

## Overview

The Cloud Deployment module provides orchestration capabilities for deploying applications and infrastructure across cloud environments. It supports multi-cloud deployments, environment promotion workflows, blue-green and canary deployment strategies, rollback mechanisms, and deployment verification. The module integrates with CI/CD pipelines and provides deployment tracking, approval gates, and post-deployment validation.

## Core Capabilities

- **Multi-Cloud Orchestration**: Deploy across AWS, Azure, GCP, and hybrid environments
- **Environment Promotion**: Structured promotion from dev to staging to production
- **Deployment Strategies**: Support for blue-green, canary, rolling, and recreate deployments
- **Rollback Management**: Automated and manual rollback capabilities
- **Approval Gates**: Configurable approval workflows for production deployments
- **Health Verification**: Post-deployment health checks and smoke tests
- **Deployment Tracking**: Complete deployment history and audit trail
- **Infrastructure Validation**: Verify infrastructure state before and after deployment

## Usage Examples

### Deployment Pipeline Creation

```python
from cloud_deployment import DeploymentPipeline, Stage, Environment

pipeline = DeploymentPipeline(
    name="web-app-deployment",
    application="web-app",
    environments=[
        Environment(name="development", auto_deploy=True),
        Environment(name="staging", auto_deploy=True),
        Environment(name="production", auto_deploy=False, approval_required=True),
    ],
)

# Add deployment stages
pipeline.add_stage(Stage(
    name="infrastructure",
    type="terraform",
    config={"work_dir": "/infra/terraform"},
    order=1,
))

pipeline.add_stage(Stage(
    name="configuration",
    type="ansible",
    config={"playbook": "deploy.yml"},
    order=2,
    depends_on=["infrastructure"],
))

pipeline.add_stage(Stage(
    name="application",
    type="container",
    config={"image": "web-app:latest", "replicas": 3},
    order=3,
    depends_on=["configuration"],
))

# Generate pipeline configuration
config = pipeline.generate()
print(config)
```

### Blue-Green Deployment

```python
from cloud_deployment import BlueGreenDeployer, DeploymentTarget

deployer = BlueGreenDeployer(
    application="web-app",
    health_check_url="/health",
    health_check_timeout=300,
)

# Deploy to green environment
green_target = DeploymentTarget(
    name="green",
    infrastructure="terraform",
    config={"environment": "green", "replicas": 3},
)

result = deployer.deploy_to_green(green_target)
print(f"Green deployment: {result.status}")

# Switch traffic
switch_result = deployer.switch_traffic(
    percentage=100,
    validation_checks=["health_check", "smoke_test"],
)
print(f"Traffic switch: {switch_result.status}")

# If issues, rollback
# deployer.rollback()
```

### Canary Deployment

```python
from cloud_deployment import CanaryDeployer, CanaryConfig

deployer = CanaryDeployer(
    application="api-service",
    config=CanaryConfig(
        initial_percentage=5,
        increment_percentage=10,
        interval_minutes=15,
        rollback_on_error_rate=5.0,
        success_threshold=99.0,
    ),
)

# Start canary deployment
result = deployer.start_canary(
    image="api-service:v2.1.0",
    baseline_version="v2.0.0",
)
print(f"Canary started: {result.deployment_id}")

# Monitor and promote
for _ in range(10):
    status = deployer.check_canary_status()
    print(f"Canary: {status.current_percentage}% traffic, {status.error_rate:.2f}% errors")
    if status.should_promote:
        deployer.promote_canary()
        break
    elif status.should_rollback:
        deployer.rollback_canary()
        break
```

### Deployment Verification

```python
from cloud_deployment import DeploymentVerifier, HealthCheck

verifier = DeploymentVerifier(
    health_checks=[
        HealthCheck(name="http-health", type="http", url="/health", expected_status=200),
        HealthCheck(name="tcp-port", type="tcp", host="localhost", port=8080),
    ],
    smoke_tests=["curl -s /api/health | jq .status"],
)

# Verify deployment
result = verifier.verify(
    deployment_id="deploy-001",
    timeout_seconds=300,
)

print(f"Verification Result:")
print(f"  Status: {result.status}")
print(f"  Health Checks: {result.health_check_results}")
print(f"  Smoke Tests: {result.smoke_test_results}")
print(f"  Duration: {result.duration_seconds:.1f}s")
```

## Best Practices

- **Immutable Infrastructure**: Deploy new infrastructure rather than modifying existing
- **Automated Rollbacks**: Implement automatic rollback on failure detection
- **Health Checks**: Always include comprehensive health checks
- **Gradual Rollouts**: Use canary or blue-green strategies for production
- **Environment Parity**: Maintain consistent configurations across environments
- **Deployment Windows**: Schedule deployments during low-traffic periods
- **Monitoring Integration**: Deploy monitoring and alerting before application changes
- **Documentation**: Document deployment procedures and rollback steps

## Related Modules

- **terraform-cloudformation**: Infrastructure provisioning for deployments
- **drift-detection**: Verify deployment state integrity
- **ansible-playbooks**: Configuration management during deployment

---

## Advanced Configuration

### Multi-Cloud Deployment Configuration

```python
cloud_config = {
    "aws": {
        "region": "us-east-1",
        "profile": "production",
        "account_id": "123456789012",
    },
    "azure": {
        "subscription_id": "xxx-xxx-xxx",
        "resource_group": "production-rg",
    },
    "gcp": {
        "project": "my-project",
        "region": "us-central1",
    },
}
```

### Deployment Pipeline Customization

```yaml
pipeline_config:
  stages:
    - name: build
      type: docker
      parallel: true
    - name: test
      type: pytest
      timeout: 300
    - name: deploy-staging
      type: kubernetes
      auto_deploy: true
    - name: deploy-production
      type: kubernetes
      approval_required: true
      approvers:
        - ops-lead
        - security-team
```

### Rollback Configuration

```python
rollback_config = {
    "auto_rollback": True,
    "rollback_triggers": {
        "error_rate_threshold": 5.0,
        "latency_threshold_ms": 1000,
        "health_check_failures": 3,
    },
    "rollback_timeout_seconds": 300,
    "max_rollback_history": 5,
}
```

### Health Check Configuration

```python
health_check_config = {
    "http": {
        "path": "/health",
        "expected_status": 200,
        "timeout_seconds": 10,
        "interval_seconds": 5,
        "healthy_threshold": 3,
        "unhealthy_threshold": 3,
    },
    "tcp": {
        "port": 8080,
        "timeout_seconds": 5,
    },
    "custom": {
        "command": "curl -s http://localhost/health | jq .status",
        "timeout_seconds": 30,
    },
}
```

### Approval Gate Configuration

```python
approval_config = {
    "production": {
        "approvers": ["ops-lead", "security-team"],
        "timeout_hours": 24,
        "required_approvals": 2,
        "escalation": {
            "after_hours": 12,
            "escalate_to": ["engineering-director"],
        },
    },
    "staging": {
        "approvers": ["dev-lead"],
        "timeout_hours": 4,
        "required_approvals": 1,
    },
}
```

### Deployment Window Configuration

```python
deployment_windows = {
    "production": {
        "allowed_days": ["monday", "tuesday", "wednesday", "thursday"],
        "allowed_hours": {"start": 10, "end": 16},
        "timezone": "America/New_York",
        "blackout_dates": ["2025-12-25", "2025-01-01"],
    },
    "staging": {
        "allowed_days": "all",
        "allowed_hours": {"start": 0, "end": 24},
    },
}
```

## Architecture Patterns

### Blue-Green Deployment Architecture

```
                    ┌─────────────┐
                    │   Load      │
                    │  Balancer   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │                         │
        ┌─────┴─────┐           ┌──────┴──────┐
        │   Blue    │           │   Green     │
        │  (Live)   │           │  (Staging)  │
        └─────┬─────┘           └──────┬──────┘
              │                         │
              └────────────┬────────────┘
                           │
                    ┌──────┴──────┐
                    │  Database   │
                    └─────────────┘
```

### Canary Deployment Architecture

```
                    ┌─────────────┐
                    │   Load      │
                    │  Balancer   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────┴─────┐ ┌───┴───┐ ┌─────┴─────┐
        │  Current  │ │Canary │ │  Current  │
        │  (95%)    │ │ (5%)  │ │  (95%)    │
        └───────────┘ └───────┘ └───────────┘
```

### Rolling Update Architecture

```
Update Batch 1: 25% of instances
┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│ Old │ │ Old │ │ New │ │ Old │
└─────┘ └─────┘ └─────┘ └─────┘

Update Batch 2: 50% of instances
┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│ New │ │ Old │ │ New │ │ Old │
└─────┘ └─────┘ └─────┘ └─────┘

Update Batch 3: 75% of instances
┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐
│ New │ │ New │ │ New │ │ Old │
└─────┘ └─────┘ └─────┘ └─────┘
```

### Multi-Region Deployment

```python
regions = ["us-east-1", "eu-west-1", "ap-southeast-1"]
deployment_strategy = {
    "type": "multi-region",
    "failover": "active-passive",
    "dns_routing": "latency-based",
    "health_check": {
        "global": True,
        "interval": 30,
    },
}
```

### GitOps Deployment

```yaml
gitops_config:
  repository: "https://github.com/org/infrastructure"
  branch: "main"
  path: "deployments/production"
  sync_interval: "5m"
  auto_sync: true
  prune: true
  self_heal: true
```

## Integration Guide

### Kubernetes Integration

```yaml
# k8s-deployment.yml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: web-app
        image: web-app:latest
        ports:
        - containerPort: 80
        livenessProbe:
          httpGet:
            path: /health
            port: 80
        readinessProbe:
          httpGet:
            path: /ready
            port: 80
```

### AWS ECS Integration

```python
ecs_config = {
    "cluster": "production",
    "service": "web-app",
    "task_definition": "web-app:latest",
    "desired_count": 3,
    "deployment_configuration": {
        "maximum_percent": 200,
        "minimum_healthy_percent": 100,
    },
    "load_balancers": [{
        "target_group_arn": "arn:aws:elasticloadbalancing:...",
        "container_name": "web-app",
        "container_port": 80,
    }],
}
```

### Terraform Integration

```python
terraform_integration = {
    "workspace": "production",
    "auto_apply": False,
    "parallelism": 10,
    "target": ["module.app"],
}
```

### Ansible Integration

```yaml
- name: Deploy via Ansible
  hosts: deploy_targets
  tasks:
    - name: Pull latest image
      docker_image:
        name: "{{ app_image }}"
        tag: "{{ app_tag }}"

    - name: Update service
      docker_service:
        name: "{{ app_name }}"
        state: present
```

### Monitoring Integration

```python
monitoring_integration = {
    "prometheus": {
        "endpoint": "http://prometheus:9090",
        "metrics": ["deploy_duration", "deploy_success"],
    },
    "grafana": {
        "dashboard": "deployment-metrics",
    },
    "pagerduty": {
        "service_key": "xxx",
    },
}
```

### Slack Integration

```python
slack_config = {
    "webhook_url": "https://hooks.slack.com/xxx",
    "channel": "#deployments",
    "notify_on": ["start", "success", "failure", "rollback"],
    "mention": {
        "failure": ["@ops-team"],
    },
}
```

## Performance Optimization

### Parallel Deployments

```python
parallel_config = {
    "max_concurrent_deploys": 3,
    "max_concurrent_per_env": 1,
    "lock_per_environment": True,
    "queue_timeout_minutes": 60,
}
```

### Deployment Speed Optimization

```python
optimization_config = {
    "use_cached_images": True,
    "pre_pull_images": True,
    "parallel_health_checks": True,
    "skip_smoke_tests_on_retry": False,
    "rolling_update_batch_size": "25%",
}
```

### Resource Optimization

```python
resource_optimization = {
    "right_sizing": True,
    "auto_scaling": {
        "enabled": True,
        "min_replicas": 3,
        "max_replicas": 10,
        "target_cpu": 70,
    },
    "spot_instances": {
        "enabled": True,
        "percentage": 30,
    },
}
```

### Network Optimization

```python
network_config = {
    "cdn_enabled": True,
    "edge_locations": ["us-east-1", "eu-west-1"],
    "dns_ttl": 300,
    "connection_pooling": True,
}
```

### Database Optimization

```python
database_config = {
    "connection_pool_size": 20,
    "read_replicas": 2,
    "cache_enabled": True,
    "cache_ttl": 300,
}
```

## Security Considerations

### Deployment Security

```python
security_config = {
    "image_scanning": True,
    "vulnerability_threshold": "high",
    "secret_scanning": True,
    "sbom_generation": True,
    "signed_commits": True,
    "signed_images": True,
}
```

### Access Control

```python
access_control = {
    "rbac_enabled": True,
    "approval_required": True,
    "audit_logging": True,
    "mfa_required": True,
    "ip_whitelist": ["10.0.0.0/8"],
}
```

### Secret Management

```python
secret_management = {
    "vault_enabled": True,
    "vault_path": "secret/data/production",
    "rotation_enabled": True,
    "rotation_interval_days": 30,
    "encryption_at_rest": True,
}
```

### Network Security

```python
network_security = {
    "tls_enabled": True,
    "min_tls_version": "1.2",
    "mutual_tls": False,
    "waf_enabled": True,
    "ddos_protection": True,
}
```

### Audit Logging

```python
audit_config = {
    "enabled": True,
    "retention_days": 90,
    "events": [
        "deployment_started",
        "deployment_completed",
        "deployment_failed",
        "rollback_triggered",
        "approval_granted",
    ],
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Deployment timeout | Slow health checks | Increase timeout, check app health |
| Rollback failed | State corruption | Restore from backup state |
| Image pull failed | Registry auth issue | Verify credentials |
| Pod restart loop | Application crash | Check logs, fix code |
| DNS not updating | TTL too high | Reduce TTL, wait for propagation |
| Service unavailable | Health check failing | Verify app is running correctly |
| Traffic not switching | Load balancer config | Check target group weights |

### Debug Commands

```bash
# Check deployment status
kubectl rollout status deployment/web-app

# View deployment history
kubectl rollout history deployment/web-app

# Check pod logs
kubectl logs -l app=web-app --tail=100

# Describe deployment
kubectl describe deployment web-app

# Check events
kubectl get events --sort-by='.lastTimestamp'
```

### Health Check Debugging

```bash
# Test health endpoint
curl -v http://localhost/health

# Check pod readiness
kubectl get pods -o wide

# View deployment annotations
kubectl get deployment web-app -o yaml
```

### Rollback Procedures

```bash
# Quick rollback
kubectl rollout undo deployment/web-app

# Rollback to specific revision
kubectl rollout undo deployment/web-app --to-revision=2

# Check rollback status
kubectl rollout status deployment/web-app
```

## API Reference

### DeploymentPipeline

```python
class DeploymentPipeline:
    def __init__(self, name: str, application: str, environments: List[Environment]):
        """Initialize deployment pipeline."""

    def add_stage(self, stage: Stage) -> None:
        """Add deployment stage."""

    def execute(self, target_env: str) -> PipelineResult:
        """Execute pipeline for target environment."""

    def rollback(self, deployment_id: str) -> RollbackResult:
        """Rollback deployment."""

    def get_status(self) -> PipelineStatus:
        """Get pipeline status."""
```

### BlueGreenDeployer

```python
class BlueGreenDeployer:
    def __init__(self, application: str, health_check_url: str):
        """Initialize blue-green deployer."""

    def deploy_to_green(self, target: DeploymentTarget) -> DeployResult:
        """Deploy to green environment."""

    def switch_traffic(self, percentage: int) -> SwitchResult:
        """Switch traffic to green."""

    def rollback(self) -> RollbackResult:
        """Rollback to blue environment."""
```

### CanaryDeployer

```python
class CanaryDeployer:
    def __init__(self, application: str, config: CanaryConfig):
        """Initialize canary deployer."""

    def start_canary(self, image: str, baseline_version: str) -> CanaryResult:
        """Start canary deployment."""

    def check_canary_status(self) -> CanaryStatus:
        """Check canary status."""

    def promote_canary(self) -> PromoteResult:
        """Promote canary to production."""

    def rollback_canary(self) -> RollbackResult:
        """Rollback canary deployment."""
```

### DeploymentVerifier

```python
class DeploymentVerifier:
    def __init__(self, health_checks: List[HealthCheck], smoke_tests: List[str]):
        """Initialize deployment verifier."""

    def verify(self, deployment_id: str, timeout_seconds: int = 300) -> VerifyResult:
        """Verify deployment health."""
```

### HealthCheck

```python
@dataclass
class HealthCheck:
    name: str
    type: str  # http, tcp, custom
    url: str = None
    host: str = None
    port: int = None
    expected_status: int = 200
    timeout_seconds: int = 10
```

## Data Models

### Environment

```python
@dataclass
class Environment:
    name: str
    auto_deploy: bool = True
    approval_required: bool = False
    approvers: List[str] = None
    config: Dict[str, Any] = None
```

### Stage

```python
@dataclass
class Stage:
    name: str
    type: str
    config: Dict[str, Any]
    order: int
    depends_on: List[str] = None
    timeout_seconds: int = 300
```

### DeploymentResult

```python
@dataclass
class DeploymentResult:
    deployment_id: str
    status: str
    environment: str
    version: str
    started_at: datetime
    completed_at: datetime = None
    resources_created: int = 0
    resources_updated: int = 0
    resources_deleted: int = 0
```

### RollbackResult

```python
@dataclass
class RollbackResult:
    rollback_id: str
    status: str
    from_deployment: str
    to_deployment: str
    duration_seconds: float
    success: bool
```

### VerifyResult

```python
@dataclass
class VerifyResult:
    status: str
    health_check_results: Dict[str, bool]
    smoke_test_results: Dict[str, bool]
    duration_seconds: float
    passed: bool
```

## Deployment Guide

### Pre-Deployment Checklist

- [ ] Code review completed
- [ ] Tests passing
- [ ] Security scan passed
- [ ] Documentation updated
- [ ] Rollback plan documented
- [ ] Monitoring configured
- [ ] Alerting configured
- [ ] Deployment window confirmed

### Deployment Steps

```bash
# 1. Build and test
docker build -t app:latest .
docker run --rm app:latest pytest

# 2. Push to registry
docker push registry.example.com/app:latest

# 3. Deploy to staging
kubectl apply -f k8s/staging/

# 4. Run smoke tests
./scripts/smoke-test.sh staging

# 5. Deploy to production
kubectl apply -f k8s/production/

# 6. Verify deployment
kubectl rollout status deployment/web-app
```

### Rollback Procedure

```bash
# 1. Identify issue
kubectl logs -l app=web-app --tail=100

# 2. Initiate rollback
kubectl rollout undo deployment/web-app

# 3. Verify rollback
kubectl rollout status deployment/web-app

# 4. Notify team
curl -X POST https://hooks.slack.com/xxx -d '{"text":"Rollback completed"}'
```

## Monitoring & Observability

### Deployment Metrics

```python
metrics = {
    "deployment_duration": "histogram",
    "deployment_success_rate": "gauge",
    "deployment_failure_rate": "gauge",
    "rollback_count": "counter",
    "deployment_frequency": "counter",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Deployment Dashboard",
    "panels": [
        "deployment_history",
        "success_rate",
        "duration_trend",
        "rollback_count",
        "environment_health",
    ],
    "refresh_interval": "1m",
}
```

### Alerting Rules

```python
alerts = [
    {
        "name": "DeploymentFailed",
        "condition": "deployment_success_rate < 0.9",
        "severity": "critical",
    },
    {
        "name": "HighRollbackRate",
        "condition": "rollback_count > 3",
        "severity": "warning",
    },
    {
        "name": "SlowDeployment",
        "condition": "deployment_duration > 600",
        "severity": "warning",
    },
]
```

## Testing Strategy

### Smoke Tests

```python
def test_smoke():
    response = requests.get("http://localhost/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Integration Tests

```python
def test_api_endpoints():
    endpoints = ["/api/health", "/api/status", "/api/version"]
    for endpoint in endpoints:
        response = requests.get(f"http://localhost{endpoint}")
        assert response.status_code == 200
```

### Load Tests

```python
# locustfile.py
from locust import HttpUser, task

class DeployedAppUser(HttpUser):
    @task
    def health_check(self):
        self.client.get("/health")
```

### Canary Analysis

```python
def analyze_canary(baseline, canary):
    error_rate_diff = canary.error_rate - baseline.error_rate
    latency_diff = canary.p99_latency - baseline.p99_latency
    return {
        "promote": error_rate_diff < 0.01 and latency_diff < 100,
        "rollback": error_rate_diff > 0.05 or latency_diff > 500,
    }
```

## Versioning & Migration

### Semantic Versioning

```python
version_strategy = {
    "major": "breaking changes",
    "minor": "new features",
    "patch": "bug fixes",
    "pre_release": "release candidates",
}
```

### Database Migration

```python
migration_config = {
    "before_deploy": True,
    "backup_before_migration": True,
    "rollback_on_failure": True,
    "timeout_seconds": 300,
}
```

### Configuration Migration

```python
config_migration = {
    "version_1_to_2": {
        "rename_keys": {"old_key": "new_key"},
        "add_defaults": {"new_feature": False},
    },
}
```

## Glossary

| Term | Definition |
|------|------------|
| **Blue-Green** | Two identical environments for zero-downtime deployment |
| **Canary** | Gradual rollout to a small percentage of traffic |
| **Rolling Update** | Sequential replacement of instances |
| **Health Check** | Verification that service is running correctly |
| **Smoke Test** | Quick verification after deployment |
| **Rollback** | Reverting to previous deployment |
| **Drift** | Difference between desired and actual state |
| **Promotion** | Moving deployment from lower to higher environment |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with multi-cloud support |
| 1.5.0 | 2024-11-01 | Added canary deployment support |
| 1.4.0 | 2024-09-15 | Blue-green deployment improvements |
| 1.3.0 | 2024-07-20 | Enhanced health checks |
| 1.2.0 | 2024-05-10 | Deployment verification |
| 1.1.0 | 2024-03-01 | Rollback automation |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow deployment best practices
2. Include rollback plan with changes
3. Test in staging first
4. Document deployment procedures
5. Update monitoring dashboards

## License

MIT License. See LICENSE file for full terms.

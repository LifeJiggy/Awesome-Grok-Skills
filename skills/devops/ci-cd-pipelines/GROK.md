---
name: "CI/CD Pipelines"
version: "2.0.0"
description: "Comprehensive CI/CD pipeline toolkit with build automation, test orchestration, deployment strategies, pipeline optimization, and release management for continuous delivery"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["devops", "ci-cd", "pipelines", "automation", "deployment", "release"]
category: "devops"
personality: "pipeline-engineer"
use_cases: ["build automation", "test orchestration", "deployment", "pipeline optimization", "release management"]
---

# CI/CD Pipelines

> Production-grade CI/CD framework providing build automation, test orchestration, deployment strategies, pipeline optimization, and release management for reliable continuous delivery.

## Overview

The CI/CD Pipelines module provides tools for automating software delivery. It implements pipeline definition and execution, build artifact management, test orchestration with parallel execution, deployment strategies (blue-green, canary, rolling), pipeline optimization for speed, and release management with approval workflows. Every pipeline includes monitoring, rollback capabilities, and audit logging.

## Core Capabilities

### 1. Pipeline Definition
- YAML-based pipeline configuration
- Stage and step definitions
- Conditional execution
- Manual approval gates
- Environment variable management

### 2. Build Automation
- Multi-language build support
- Dependency caching
- Artifact versioning
- Build matrix execution
- Parallel build stages

### 3. Test Orchestration
- Parallel test execution
- Test result aggregation
- Flaky test detection
- Test coverage reporting
- Test impact analysis

### 4. Deployment Strategies
- Blue-green deployment
- Canary releases
- Rolling updates
- Feature flag integration
- A/B testing support

### 5. Pipeline Optimization
- Build time analysis
- Cache optimization
- Stage parallelization
- Resource allocation
- Cost optimization

### 6. Release Management
- Version management
- Changelog generation
- Approval workflows
- Rollback procedures
- Release notes automation

## Usage Examples

### Pipeline Definition

```python
from cicd_pipelines import Pipeline, Stage, Step

pipeline = Pipeline(
    name="production-deploy",
    triggers=["push:main", "tag:v*"],
    environments=["staging", "production"],
)

# Define stages
pipeline.add_stage(Stage(
    name="build",
    steps=[
        Step("checkout", "git checkout $COMMIT_SHA"),
        Step("install", "npm ci"),
        Step("build", "npm run build"),
        Step("cache", "cache node_modules"),
    ],
))

pipeline.add_stage(Stage(
    name="test",
    parallel=True,
    steps=[
        Step("unit-tests", "npm test -- --coverage"),
        Step("lint", "npm run lint"),
        Step("type-check", "npm run typecheck"),
    ],
))

pipeline.add_stage(Stage(
    name="deploy",
    environment="production",
    approval_required=True,
    steps=[
        Step("deploy", "kubectl apply -f k8s/"),
        Step("verify", "kubectl rollout status deployment/app"),
    ],
))

# Validate and execute
pipeline.validate()
pipeline.execute()
```

### Deployment Strategy

```python
from cicd_pipelines import DeploymentStrategy, BlueGreenDeployment

# Blue-green deployment
blue_green = BlueGreenDeployment(
    service="api-service",
    namespace="production",
    health_check_url="/health",
    switch_timeout=300,
)

# Execute deployment
result = blue_green.deploy(image="app:v2.1.0")
print(f"Status: {result.status}")
print(f"Old version: {result.old_version}")
print(f"New version: {result.new_version}")

if result.success:
    blue_green.switch()
    print("Traffic switched to new version")
else:
    blue_green.rollback()
    print("Deployment failed, rolled back")
```

### Pipeline Optimization

```python
from cicd_pipelines import PipelineOptimizer

optimizer = PipelineOptimizer()

# Analyze pipeline performance
analysis = optimizer.analyze(pipeline)
print(f"Total duration: {analysis.total_duration_seconds:.0f}s")
print(f"Critical path: {analysis.critical_path}")
print(f"Optimization opportunities:")
for opp in analysis.opportunities:
    print(f"  {opp.description}: save {opp.estimated_savings_seconds:.0f}s")
```

## Best Practices

### Pipeline Design
- Keep pipelines fast — target < 10 minutes for CI
- Fail fast — run quickest checks first
- Use caching aggressively for dependencies
- Parallelize independent stages

### Testing
- Run unit tests first (fastest feedback)
- Use test impact analysis to run only affected tests
- Quarantine flaky tests automatically
- Report coverage on every PR

### Deployment
- Use feature flags for risky changes
- Implement automatic rollback on health check failures
- Deploy to staging before production
- Use canary releases for high-risk deployments

### Security
- Scan for vulnerabilities in CI
- Sign artifacts and images
- Use secrets management (not environment variables)
- Audit all deployment actions

## Related Modules

- **container-orchestration**: Kubernetes deployment automation
- **infrastructure-as-code**: Infrastructure pipeline integration
- **monitoring**: Pipeline monitoring and alerting
- **site-reliability**: SRE practices for pipeline reliability

---

## Advanced Configuration

### Advanced Pipeline Definition

```python
from cicd_pipelines import Pipeline, Stage, Step, Trigger, ApprovalGate

pipeline = Pipeline(
    name="production-deploy",
    triggers=[
        Trigger(type="push", branch="main"),
        Trigger(type="tag", pattern="v*"),
        Trigger(type="schedule", cron="0 2 * * *"),
    ],
    environments=["staging", "production"],
    variables={"DOCKER_REGISTRY": "gcr.io/my-project"},
)

# Advanced stage configuration
pipeline.add_stage(Stage(
    name="security-scan",
    steps=[
        Step("trivy-scan", "trivy image --severity HIGH,CRITICAL $IMAGE"),
        Step("snyk-test", "snyk test --docker $IMAGE"),
        Step("sonarqube", "sonar-scanner -Dsonar.projectKey=$PROJECT"),
    ],
    allow_failure=False,
    timeout_minutes=30,
))

pipeline.add_stage(Stage(
    name="integration-tests",
    parallel=True,
    matrix={
        "python-version": ["3.9", "3.10", "3.11"],
        "database": ["postgresql", "mysql"],
    },
    steps=[
        Step("test", "pytest --cov=app tests/integration/"),
    ],
))

# Approval gate with conditions
pipeline.add_stage(Stage(
    name="deploy-production",
    approval=ApprovalGate(
        required_approvers=2,
        conditions=[
            {"type": "tests_passed", "stage": "integration-tests"},
            {"type": "security_scan_clean", "stage": "security-scan"},
            {"type": "manual_approval", "approvers": ["team-lead", "sre"]},
        ],
    ),
    steps=[
        Step("deploy", "kubectl apply -f k8s/production/"),
        Step("verify", "kubectl rollout status deployment/api-service"),
        Step("smoke-test", "curl -f https://api.example.com/health"),
    ],
    rollback_on_failure=True,
))
```

### Advanced Deployment Strategy

```python
from cicd_pipelines import CanaryDeployment, DeploymentConfig

canary = CanaryDeployment(
    service="api-service",
    namespace="production",
    config=DeploymentConfig(
        initial_percent=5,
        increment_percent=10,
        interval_minutes=5,
        max_percent=100,
        health_check_url="/health",
        success_threshold=99.9,
        rollback_threshold=1.0,
    ),
)

# Execute canary deployment
result = canary.deploy(
    image="app:v2.1.0",
    metrics=["error_rate", "latency_p99", "cpu_usage"],
    auto_promote=True,
    auto_rollback=True,
)

print(f"Status: {result.status}")
print(f"Current traffic: {result.current_percent}%")
print(f"Metrics: {result.metrics}")
```

### Advanced Pipeline Optimization

```python
from cicd_pipelines import PipelineOptimizer, OptimizationConfig

optimizer = OptimizationConfig(
    analyze_dependencies=True,
    optimize_caching=True,
    parallelize_stages=True,
    reduce_artifact_size=True,
)

# Comprehensive optimization analysis
analysis = optimizer.analyze_comprehensive(pipeline)
print(f"Current duration: {analysis.current_duration_seconds:.0f}s")
print(f"Optimized duration: {analysis.optimized_duration_seconds:.0f}s")
print(f"Savings: {analysis.savings_seconds:.0f}s ({analysis.savings_pct:.1f}%)")

print("\nOptimization opportunities:")
for opp in analysis.opportunities:
    print(f"  [{opp.impact}] {opp.description}")
    print(f"    Savings: {opp.estimated_savings_seconds:.0f}s")
    print(f"    Implementation: {opp.implementation}")
```

## Architecture Patterns

### CI/CD Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  CI/CD Architecture                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Source Control                          │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  GitHub     │  │  GitLab     │  │  Bitbucket  │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              CI Pipeline                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Build      │  │  Test       │  │  Scan       │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              CD Pipeline                             │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Stage      │  │  Deploy     │  │  Verify     │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│  ┌────────────────────────┴─────────────────────────────┐   │
│  │              Production                              │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
│  │  │  Monitor    │  │  Alert      │  │  Rollback   │ │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘ │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Integration Guide

### GitHub Actions Integration

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Build
        run: docker build -t $IMAGE .
      
      - name: Test
        run: docker run --rm $IMAGE pytest
      
      - name: Security Scan
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: $IMAGE
          severity: HIGH,CRITICAL

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Staging
        run: kubectl apply -f k8s/staging/
      
      - name: Verify Deployment
        run: kubectl rollout status deployment/api-service
```

## Performance Optimization

### Pipeline Performance

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| CI duration | < 10min | 10-20min | > 20min |
| CD duration | < 15min | 15-30min | > 30min |
| Test duration | < 5min | 5-10min | > 10min |
| Build cache hit | > 80% | 60-80% | < 60% |

## Security Considerations

### Pipeline Security

```python
from cicd_pipelines import SecurityScanner

scanner = SecurityScanner()

# Scan pipeline for security issues
security = scanner.scan_pipeline(pipeline)
print(f"Security score: {security.score:.1f}/100")
print(f"Issues: {len(security.issues)}")

for issue in security.issues:
    print(f"  [{issue.severity}] {issue.description}")
    print(f"    Location: {issue.location}")
    print(f"    Fix: {issue.fix_suggestion}")
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Slow builds | Long CI duration | Optimize caching, parallelize |
| Flaky tests | Intermittent failures | Isolate tests, mock external services |
| Deployment failures | Rollback triggered | Check health checks, verify config |
| Secret leaks | Exposed credentials | Use secrets management |

## API Reference

### Pipeline

```python
class Pipeline:
    def __init__(self, name: str, **kwargs)
    def add_stage(self, stage: Stage)
    def validate(self) -> ValidationResult
    def execute(self) -> PipelineResult
    def get_status(self) -> PipelineStatus
    def cancel(self) -> CancelResult
    def rollback(self) -> RollbackResult
```

### DeploymentStrategy

```python
class DeploymentStrategy:
    def __init__(self, service: str, namespace: str, **kwargs)
    def deploy(self, image: str, **kwargs) -> DeploymentResult
    def rollback(self) -> RollbackResult
    def get_status(self) -> DeploymentStatus
    def get_history(self) -> list[DeploymentHistory]
```

## Data Models

### Core Data Structures

```python
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

class StageStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class PipelineResult:
    success: bool
    duration_seconds: float
    stages: List['StageResult']
    artifacts: List['Artifact']

@dataclass
class StageResult:
    name: str
    status: StageStatus
    duration_seconds: float
    steps: List['StepResult']
```

## Deployment Guide

### Installation

```bash
pip install ci-cd-pipelines
```

## Monitoring & Observability

### Metrics Collection

```python
from cicd_pipelines import MetricsCollector

collector = MetricsCollector()

# Collect pipeline metrics
collector.counter("pipeline.runs.total", count, tags={"status": status})
collector.histogram("pipeline.duration.seconds", duration)
collector.gauge("pipeline.success.rate", rate)
collector.counter("deployment.total", count, tags={"strategy": strategy})
```

## Testing Strategy

### Unit Tests

```python
import pytest
from cicd_pipelines import Pipeline, DeploymentStrategy

@pytest.fixture
def pipeline():
    return Pipeline(name="test-pipeline")

def test_pipeline_validation(pipeline):
    result = pipeline.validate()
    assert result.is_valid
```

## Versioning & Migration

### Version Compatibility

| Component | Minimum Version | Recommended |
|-----------|-----------------|-------------|
| Kubernetes | 1.24 | 1.28+ |
| Docker | 20.10 | 24.0+ |

## Glossary

| Term | Definition |
|------|------------|
| **CI** | Continuous Integration |
| **CD** | Continuous Delivery/Deployment |
| **Pipeline** | Automated build/test/deploy sequence |
| **Canary** | Gradual rollout to subset of users |
| **Blue-Green** | Two identical environments for deployment |

## Changelog

### Version 3.0.0 (2024-01-15)
- Added canary deployment support
- New pipeline optimizer
- Improved security scanning
- Added approval workflows

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/ci-cd-pipelines.git
cd ci-cd-pipelines
pip install -e ".[dev]"
pytest
```

## Multi-Environment Strategies

### Environment Promotion Pipeline

```python
from cicd_pipelines import EnvironmentPromotion, PromotionRule

# Define promotion rules
rules = [
    PromotionRule(
        from_env="development",
        to_env="staging",
        required_checks=["unit-tests", "lint", "security-scan"],
        required_approval=False,
    ),
    PromotionRule(
        from_env="staging",
        to_env="production",
        required_checks=["integration-tests", "performance-tests", "security-scan"],
        required_approval=True,
        min_approvers=2,
    ),
]

# Create promotion pipeline
pipeline = EnvironmentPromotion(
    name="app-promotion",
    rules=rules,
    artifact_repository="gcr.io/my-project",
)

# Execute promotion
result = pipeline.promote(
    artifact="app:v2.1.0",
    from_env="development",
    to_env="staging",
)

print(f"Promotion: {result.status}")
print(f"Checks passed: {result.checks_passed}/{result.checks_total}")
print(f"Duration: {result.duration_seconds:.0f}s")
```

### Environment Isolation

```python
from cicd_pipelines import EnvironmentIsolation

isolation = EnvironmentIsolation()

# Create isolated environment
env = isolation.create(
    name="pr-1234",
    template="production",
    ttl_hours=24,
    auto_cleanup=True,
)

print(f"Environment created: {env.name}")
print(f"URL: {env.url}")
print(f"Resources: {env.resources}")
print(f"Expires: {env.expires_at}")

# Use for testing
print(f"\nTesting in isolated environment:")
print(f"  API: {env.url}/api")
print(f"  DB: {env.database_url}")
print(f"  Cache: {env.redis_url}")
```

## Pipeline Security Hardening

### Secret Management

```python
from cicd_pipelines import SecretManager

manager = SecretManager()

# Configure secrets
secrets_config = {
    "docker-credentials": {
        "type": "docker",
        "registry": "gcr.io",
        "service-account": "pipeline-sa",
    },
    "database-url": {
        "type": "connection-string",
        "vault-path": "secret/data/database",
        "rotation_days": 30,
    },
    "api-keys": {
        "type": "key-value",
        "vault-path": "secret/data/api-keys",
        "keys": ["stripe", "sendgrid", "sentry"],
    },
}

# Inject secrets into pipeline
pipeline = Pipeline(
    name="secure-deploy",
    secrets=secrets_config,
    secret_rotation_enabled=True,
)

print(f"Secrets configured: {len(secrets_config)}")
print(f"Rotation enabled: True")
print(f"Encryption: AES-256-GCM")
```

### Supply Chain Security

```python
from cicd_pipelines import SupplyChainSecurity

security = SupplyChainSecurity()

# Configure SLSA compliance
slsa_config = security.configure_slsa(
    level=3,
    provenance_generation=True,
    artifact_signing=True,
    builder_attestation=True,
)

print(f"SLSA Level: {slsa_config.level}")
print(f"Provenance: {slsa_config.provenance_enabled}")
print(f"Signing: {slsa_config.signing_enabled}")

# Verify artifact integrity
verification = security.verify_artifact(
    artifact="app:v2.1.0",
    expected_digest="sha256:abc123...",
    expected_provenance=True,
)

print(f"\nVerification:")
print(f"  Digest match: {verification.digest_match}")
print(f"  Provenance valid: {verification.provenance_valid}")
print(f"  Signature valid: {verification.signature_valid}")
print(f"  Builder verified: {verification.builder_verified}")
```

### Pipeline Auditing

```python
from cicd_pipelines import PipelineAuditor

auditor = PipelineAuditor()

# Audit pipeline configuration
audit = auditor.audit_pipeline("production-deploy")

print(f"Security audit:")
print(f"  Score: {audit.score}/100")
print(f"  Critical issues: {audit.critical_count}")
print(f"  Warnings: {audit.warning_count}")

print(f"\nFindings:")
for finding in audit.findings:
    print(f"  [{finding.severity}] {finding.title}")
    print(f"    {finding.description}")
    print(f"    Fix: {finding.remediation}")

# Audit deployment history
history_audit = auditor.audit_deployments(
    pipeline="production-deploy",
    period="30_days",
)

print(f"\nDeployment audit:")
print(f"  Total deployments: {history_audit.total}")
print(f"  Rollbacks: {history_audit.rollbacks}")
print(f"  Mean time to recover: {history_audit.mttr_minutes:.0f}min")
```

## Cost Optimization

### Pipeline Cost Analysis

```python
from cicd_pipelines import CostAnalyzer

analyzer = CostAnalyzer()

# Analyze pipeline costs
analysis = analyzer.analyze(
    pipeline="production-deploy",
    period="30_days",
    cloud_provider="aws",
)

print(f"Pipeline costs (30 days):")
print(f"  Compute: ${analysis.compute_cost:.2f}")
print(f"  Storage: ${analysis.storage_cost:.2f}")
print(f"  Network: ${analysis.network_cost:.2f}")
print(f"  Total: ${analysis.total_cost:.2f}")

print(f"\nCost breakdown by stage:")
for stage, cost in analysis.stage_costs.items():
    print(f"  {stage}: ${cost:.2f}")

print(f"\nOptimization opportunities:")
for opp in analysis.optimizations:
    print(f"  {opp.description}: save ${opp.monthly_savings:.2f}/month")
    print(f"    Implementation: {opp.implementation}")
```

### Resource Optimization

```python
from cicd_pipelines import ResourceOptimizer

optimizer = ResourceOptimizer()

# Optimize runner resources
result = optimizer.optimize_runners(
    pipeline="production-deploy",
    target_utilization=0.7,
)

print(f"Runner optimization:")
print(f"  Current runners: {result.current_runners}")
print(f"  Recommended runners: {result.recommended_runners}")
print(f"  Estimated savings: ${result.monthly_savings:.2f}/month")

# Optimize caching
cache_result = optimizer.optimize_caching(
    pipeline="production-deploy",
    hit_rate_target=0.9,
)

print(f"\nCache optimization:")
print(f"  Current hit rate: {cache_result.current_hit_rate:.1%}")
print(f"  Optimized hit rate: {cache_result.optimized_hit_rate:.1%}")
print(f"  Time savings: {cache_result.time_savings_seconds:.0f}s per run")
```

## Disaster Recovery Pipelines

### Backup Pipeline

```python
from cicd_pipelines import BackupPipeline

backup = BackupPipeline()

# Configure backup strategy
strategy = backup.configure(
    name="production-backup",
    targets=[
        {"type": "database", "service": "postgres", "retention_days": 30},
        {"type": "storage", "bucket": "app-data", "retention_days": 90},
        {"type": "secrets", "vault": "production", "retention_days": 365},
    ],
    schedule="0 2 * * *",
    encryption="AES-256",
    cross_region_replication=True,
)

print(f"Backup strategy configured:")
print(f"  Targets: {len(strategy.targets)}")
print(f"  Schedule: {strategy.schedule}")
print(f"  Encryption: {strategy.encryption}")
print(f"  Cross-region: {strategy.cross_region}")

# Execute backup
result = backup.execute(strategy)
print(f"\nBackup result:")
print(f"  Status: {result.status}")
print(f"  Size: {result.size_gb:.2f}GB")
print(f"  Duration: {result.duration_seconds:.0f}s")
print(f"  Verification: {result.verification_passed}")
```

### Recovery Pipeline

```python
from cicd_pipelines import RecoveryPipeline

recovery = RecoveryPipeline()

# Configure recovery procedures
procedures = recovery.configure(
    scenarios=[
        {
            "name": "database-corruption",
            "rto_minutes": 30,
            "rpo_minutes": 5,
            "steps": ["restore-latest", "verify-integrity", "switch-traffic"],
        },
        {
            "name": "region-outage",
            "rto_minutes": 15,
            "rpo_minutes": 1,
            "steps": ["activate-dr-region", "update-dns", "verify-health"],
        },
    ],
    auto_failover=True,
    health_check_interval=30,
)

print(f"Recovery procedures:")
for scenario in procedures.scenarios:
    print(f"  {scenario.name}:")
    print(f"    RTO: {scenario.rto_minutes}min")
    print(f"    RPO: {scenario.rpo_minutes}min")
    print(f"    Steps: {len(scenario.steps)}")
```

## Release Engineering

### Release Automation

```python
from cicd_pipelines import ReleaseEngineer

engineer = ReleaseEngineer()

# Configure release process
release_config = engineer.configure(
    versioning="semver",
    changelog_auto=True,
    release_notes_template="standard",
    approval_required=True,
    rollback_window_hours=24,
)

# Create release
release = engineer.create_release(
    version="2.1.0",
    changes=["feat: add payment integration", "fix: resolve timeout issue"],
    breaking_changes=[],
    deprecations=[],
)

print(f"Release created:")
print(f"  Version: {release.version}")
print(f"  Changelog: {len(release.changelog_entries)} entries")
print(f"  Approval status: {release.approval_status}")
print(f"  Rollback window: {release.rollback_window_hours}h")

# Execute release
result = engineer.execute_release(release)
print(f"\nRelease execution:")
print(f"  Status: {result.status}")
print(f"  Deployment: {result.deployment_id}")
print(f"  Verification: {result.verification_passed}")
```

### Feature Flag Integration

```python
from cicd_pipelines import FeatureFlagManager

manager = FeatureFlagManager()

# Configure feature flags
flags = manager.configure_flags([
    {
        "name": "new-checkout-flow",
        "enabled": True,
        "rollout_percentage": 10,
        "targeting_rules": [
            {"attribute": "country", "operator": "in", "values": ["US", "CA"]},
            {"attribute": "beta_user", "operator": "eq", "value": True},
        ],
    },
    {
        "name": "dark-mode",
        "enabled": False,
        "rollout_percentage": 0,
    },
])

print(f"Feature flags configured: {len(flags)}")
for flag in flags:
    print(f"  {flag.name}: enabled={flag.enabled}, rollout={flag.rollout_percentage}%")

# Integrate with pipeline
pipeline = Pipeline(
    name="feature-deploy",
    feature_flags=flags,
    gradual_rollout=True,
)

print(f"\nPipeline configured with gradual rollout")
```

## Contributing Guidelines

```bash
git clone https://github.com/awesome-grok/ci-cd-pipelines.git
cd ci-cd-pipelines
pip install -e ".[dev]"
pytest
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills
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

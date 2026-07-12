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
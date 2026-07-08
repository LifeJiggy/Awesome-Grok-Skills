# CI/CD Pipeline Agent

Comprehensive CI/CD pipeline design, build automation, testing orchestration, deployment management, security scanning, and rollback capabilities supporting GitHub Actions, GitLab CI, Jenkins, and Azure DevOps.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Pipeline Creation](#pipeline-creation)
  - [Build Configuration](#build-configuration)
  - [Deployment Configuration](#deployment-configuration)
  - [Security Scanning](#security-scanning)
  - [Quality Gates](#quality-gates)
  - [Config Generation](#config-generation)
  - [Trigger and Monitor](#trigger-and-monitor)
  - [Rollback](#rollback)
- [API Reference](#api-reference)
  - [CICDPipelineAgent](#cicdpipelineagent)
  - [PipelineConfigGenerator](#pipelineconfiggenerator)
  - [TestOrchestrator](#testorchestrator)
  - [DeploymentManager](#deploymentmanager)
  - [SecurityScanner](#securityscanner)
  - [NotificationManager](#notificationmanager)
- [Data Models](#data-models)
- [Deployment Strategies](#deployment-strategies)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The CI/CD Pipeline Agent is a Python-based system for designing, implementing, and managing continuous integration and delivery pipelines. It provides provider-agnostic pipeline definitions with multi-provider YAML/JSON configuration generation, integrated security scanning, test orchestration, and deployment management.

**Key Capabilities:**
- Pipeline design with configurable stages and steps
- Multi-provider configuration generation (GitHub Actions, GitLab CI, Jenkins, Azure DevOps)
- Test orchestration with coverage tracking
- Security scanning integration (SAST, SCA, secrets, container)
- Quality gate evaluation
- Blue-green, canary, rolling, and A/B deployment strategies
- Automatic rollback on failure
- Notification management across channels

## Features

| Feature | Description |
|---------|-------------|
| Pipeline Design | Create pipelines with stages, steps, triggers, and dependencies |
| Multi-Provider | Generate configs for GitHub Actions, GitLab CI, Jenkins, Azure DevOps |
| Build Automation | Configure builds with language-appropriate tooling |
| Test Orchestration | Manage test execution, coverage, and quality gates |
| Security Scanning | Integrated SAST, SCA, secret scanning, container scanning |
| Deployment | Blue-green, canary, rolling, recreate, feature flag strategies |
| Rollback | Automatic and manual rollback with strategy selection |
| Notifications | Multi-channel notifications for pipeline events |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline Agent                     │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ Pipeline  │ │  Config  │ │  Test    │ │Deployment│     │
│  │ Manager   │ │Generator │ │Orchestr. │ │ Manager  │     │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
│       │            │            │            │             │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐     │
│  │ Security │ │Notifica- │ │ Quality  │ │ Rollback │     │
│  │ Scanner  │ │tion Mgr  │ │  Gates   │ │  Engine  │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```python
from agents.ci_cd_pipeline.agent import CICDPipelineAgent

# Initialize
agent = CICDPipelineAgent()

# Create pipeline
pipeline = agent.create_pipeline(
    name="Web App CI/CD",
    project="webapp",
    provider="github_actions",
)

# Configure build
agent.configure_build(pipeline["pipeline_id"], build_tool="npm")

# Configure deployment
agent.configure_deployment(pipeline["pipeline_id"], environment="staging")

# Generate config
config = agent.generate_pipeline_config(pipeline["pipeline_id"])
print(config["configuration"])
```

```bash
python agents/ci-cd-pipeline/agent.py
```

## Usage

### Pipeline Creation

```python
pipeline = agent.create_pipeline(
    name="Microservice Pipeline",
    project="auth-service",
    provider="gitlab_ci",
    repository="org/auth-service",
    description="CI/CD for authentication microservice",
)
```

### Build Configuration

```python
build = agent.configure_build(
    pipeline_id=pipeline["pipeline_id"],
    build_tool="npm",
    language="javascript",
    build_command="npm run build",
    test_command="npm test -- --coverage",
)

# Auto-generates Source → Build → Test stages
# Stages: ['Source', 'Build', 'Test']
```

### Deployment Configuration

```python
# Staging with canary
agent.configure_deployment(
    pipeline_id=pipeline["pipeline_id"],
    environment="staging",
    strategy="canary",
    auto_promote=False,
)

# Production with blue-green
agent.configure_deployment(
    pipeline_id=pipeline["pipeline_id"],
    environment="production",
    strategy="blue_green",
)
```

### Security Scanning

```python
security = agent.configure_security_scanning(
    pipeline_id=pipeline["pipeline_id"],
    sast=True,
    sca=True,
    secret_scan=True,
    container_scan=True,
)

# Adds Security Scan stage to pipeline
# Config: trivy, sonarqube, snyk
```

### Quality Gates

```python
gates = agent.configure_quality_gates(
    pipeline_id=pipeline["pipeline_id"],
    coverage_threshold=80.0,
    max_vulnerabilities=0,
    max_code_smells=10,
)

# Gates evaluated after Test + Security Scan stages
```

### Config Generation

```python
# Generate GitHub Actions workflow
config = agent.generate_pipeline_config(pipeline["pipeline_id"])
print(config["configuration"])
# Returns full YAML structure for the provider
```

### Trigger and Monitor

```python
# Trigger a run
run = agent.trigger_pipeline(
    pipeline_id=pipeline["pipeline_id"],
    branch="main",
    commit_message="feat: add login endpoint",
)

# Check status
status = agent.get_pipeline_status(pipeline["pipeline_id"])
print(f"Runs: {status['total_runs']}, Success rate: {status['success_rate']}")
```

### Rollback

```python
result = agent.rollback(
    pipeline_id=pipeline["pipeline_id"],
    environment="staging",
    reason="Performance regression detected",
    initiated_by="on-call-engineer",
)

print(f"Rollback success: {result['success']}")
```

## API Reference

### CICDPipelineAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `create_pipeline()` | name, project, provider, repository, description | Pipeline dict |
| `configure_build()` | pipeline_id, build_tool, build_command, test_command, language | Build config dict |
| `configure_deployment()` | pipeline_id, environment, strategy, auto_promote | Deploy config dict |
| `configure_security_scanning()` | pipeline_id, sast, sca, secret_scan, container_scan | Security config dict |
| `configure_quality_gates()` | pipeline_id, coverage_threshold, max_vulnerabilities, max_code_smells | Gates dict |
| `generate_pipeline_config()` | pipeline_id | Provider config dict |
| `trigger_pipeline()` | pipeline_id, branch, commit_sha, commit_message | Run dict |
| `get_pipeline_status()` | pipeline_id | Status dict |
| `rollback()` | pipeline_id, environment, reason, initiated_by | Rollback dict |
| `get_security_report()` | pipeline_id | Security report dict |
| `list_pipelines()` | — | List of pipeline dicts |

### PipelineConfigGenerator

| Method | Parameters | Returns |
|--------|-----------|---------|
| `generate_config()` | pipeline, output_format | Provider-specific config |

### TestOrchestrator

| Method | Parameters | Returns |
|--------|-----------|---------|
| `configure_test_suite()` | pipeline_id, test_configs | Suite config dict |
| `execute_tests()` | pipeline_id, run_id, test_configs | Test results dict |
| `check_quality_gates()` | gates, metrics | Gate evaluation dict |

### DeploymentManager

| Method | Parameters | Returns |
|--------|-----------|---------|
| `deploy()` | pipeline_id, run_id, config, artifact | Deployment result dict |
| `promote()` | pipeline_id, deployment_id, target_environment | Promotion dict |
| `rollback()` | pipeline_id, run_id, environment, strategy, reason | Rollback record dict |

### SecurityScanner

| Method | Parameters | Returns |
|--------|-----------|---------|
| `scan()` | pipeline_id, run_id | Scan results with findings |

### NotificationManager

| Method | Parameters | Returns |
|--------|-----------|---------|
| `notify()` | pipeline_id, run_id, level, title, message, channel, recipients | Notification dict |

## Data Models

### Pipeline
Complete pipeline definition with stages, triggers, test configs, quality gates, and deployment configs.

### Stage
A pipeline stage containing steps, dependencies, environment, and artifact specifications.

### PipelineRun
A single execution record with status, timing, stage results, and artifacts.

### DeploymentConfig
Deployment configuration with environment, strategy, health check, and approval settings.

### Artifact
Build artifact with type, version, registry, and metadata.

## Deployment Strategies

| Strategy | Downtime | Rollback | Resources | Risk |
|----------|----------|----------|-----------|------|
| Blue-Green | Zero | Instant | 2x | Low |
| Canary | Zero | Fast | +10-20% | Low |
| Rolling | Brief | Minutes | +1/batch | Medium |
| Recreate | Yes | Slow | Same | High |
| Feature Flags | Zero | Instant | Minimal | Low |

## Configuration

```python
config = {
    "user": "devops_engineer",
    "default_provider": "github_actions",
    "security_tools": ["trivy", "sonarqube", "snyk"],
    "coverage_threshold": 80.0,
    "notification_channels": ["slack", "email"],
}
agent = CICDPipelineAgent(config)
```

## Best Practices

1. **Pin Dependencies** — Always use lockfiles for reproducible builds
2. **Run Fast Tests First** — Unit tests before integration tests
3. **Shift-Left Security** — SAST/SCA in every pipeline, not just before production
4. **Immutable Artifacts** — Build once, deploy everywhere
5. **Health Checks on Deploy** — Never consider a deploy complete without health verification
6. **Test Your Rollback** — A rollback that hasn't been tested is not a rollback
7. **Use Quality Gates** — Prevent bad code from reaching production

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Build works locally but fails on CI | Use lockfiles, check environment variables, containerize builds |
| Tests flaky on CI | Add retries, increase timeouts, isolate tests |
| Deployment health check fails | Increase timeout, check dependencies, verify service startup |
| Security scan blocks pipeline | Fix vulnerabilities or add justified exceptions |
| Pipeline too slow | Parallelize stages, add caching, optimize test selection |
| Rollback fails | Design backward-compatible migrations, test rollback regularly |

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams
- `GROK.md` — Agent instructions and identity
- `README.md` — This file

## Contributing

1. Follow the existing code style with type hints and dataclasses
2. Add provider-specific config generators for new CI/CD platforms
3. Include tests for new deployment strategies
4. Update documentation for API changes

## License

Part of the Awesome Grok Skills collection. See project root for license details.

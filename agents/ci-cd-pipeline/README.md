# CI/CD Pipeline Agent

Comprehensive CI/CD pipeline design, build automation, testing orchestration, deployment management, security scanning, and rollback capabilities supporting GitHub Actions, GitLab CI, Jenkins, and Azure DevOps.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Features](#features)
- [Provider Comparison](#provider-comparison)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
  - [Minimal Pipeline](#minimal-pipeline)
  - [Full Pipeline with Security](#full-pipeline-with-security)
  - [Multi-Environment Deployment](#multi-environment-deployment)
  - [Custom Build Tool](#custom-build-tool)
- [Usage](#usage)
  - [Pipeline Creation](#pipeline-creation)
  - [Build Configuration](#build-configuration)
  - [Deployment Configuration](#deployment-configuration)
  - [Security Scanning](#security-scanning)
  - [Quality Gates](#quality-gates)
  - [Config Generation](#config-generation)
  - [Trigger and Monitor](#trigger-and-monitor)
  - [Rollback](#rollback)
  - [Notifications](#notifications)
  - [Artifact Management](#artifact-management)
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
  - [Node.js Web Application](#nodejs-web-application)
  - [Python Django Service](#python-django-service)
  - [Go Microservice](#go-microservice)
  - [Java Spring Boot Application](#java-spring-boot-application)
  - [Container Image Build and Push](#container-image-build-and-push)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Extending the Agent](#extending-the-agent)
- [FAQ](#faq)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview

The CI/CD Pipeline Agent is a Python-based system for designing, implementing, and managing continuous integration and delivery pipelines. It provides provider-agnostic pipeline definitions with multi-provider YAML/JSON configuration generation, integrated security scanning, test orchestration, and deployment management.

**Key Capabilities:**

- Pipeline design with configurable stages, steps, triggers, and dependencies
- Multi-provider configuration generation (GitHub Actions, GitLab CI, Jenkins, Azure DevOps)
- Test orchestration with coverage tracking and parallel execution
- Security scanning integration (SAST, SCA, secrets, container scanning)
- Quality gate evaluation with configurable thresholds
- Blue-green, canary, rolling, recreate, and feature flag deployment strategies
- Automatic rollback on failure with configurable triggers
- Notification management across Slack, email, Teams, and webhook channels

## Prerequisites

| Requirement | Details |
|-------------|---------|
| Python | 3.9 or higher |
| Dependencies | `pyyaml` (PyYAML), plus standard library modules |
| CI/CD Provider | At least one supported provider account |
| Repository | An existing Git repository to attach pipelines to |
| Security Tools | Optional: Trivy, SonarQube, Snyk for security scanning |
| Notification Channels | Optional: Slack, email, or Teams webhook URLs |

**Installation:**

```bash
git clone <repository-url>
cd Awesome-Grok-Skills
pip install pyyaml

# Verify the installation
python -c "from agents.ci_cd_pipeline.agent import CICDPipelineAgent; print('CI/CD Pipeline Agent loaded')"
```

## Features

| Feature | Description |
|---------|-------------|
| Pipeline Design | Create pipelines with stages, steps, triggers, and dependency chains |
| Multi-Provider | Generate configs for GitHub Actions, GitLab CI, Jenkins, Azure DevOps |
| Build Automation | Configure builds with language-appropriate tooling and caching |
| Test Orchestration | Manage test execution, coverage, parallel runs, and quality gates |
| Security Scanning | Integrated SAST, SCA, secret scanning, container scanning |
| Deployment | Blue-green, canary, rolling, recreate, feature flag strategies |
| Rollback | Automatic and manual rollback with strategy selection and audit trail |
| Notifications | Multi-channel notifications (Slack, email, Teams, webhook) |
| Artifact Management | Versioned artifacts with registry push and retention policies |
| Quality Gates | Configurable thresholds for coverage, vulnerabilities, and build time |

## Provider Comparison

| Capability | GitHub Actions | GitLab CI | Jenkins | Azure DevOps |
|------------|---------------|-----------|---------|-------------|
| Config Syntax | YAML (`.github/workflows/`) | YAML (`.gitlab-ci.yml`) | Groovy (`Jenkinsfile`) | YAML (`azure-pipelines.yml`) |
| Runner Support | GitHub-hosted + self-hosted | GitLab Runner + shared | Jenkins agents | Microsoft-hosted + self-hosted |
| Secret Management | Repository/Environment secrets | CI/CD Variables | Credentials plugin | Variable groups + Key Vault |
| Matrix Builds | Native `strategy.matrix` | `parallel: matrix` | `matrix { }` block | `strategy.matrix` |
| Reusable Components | Reusable workflows + composite actions | `include` + templates | Shared libraries | Templates + task groups |
| Environment Protection | Environments + required reviewers | Environments + approvals | Approval gates | Environments + approvals |
| Free Tier | 2000 min/month | 400 min/month | Unlimited (self-hosted) | 1800 min/month |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD Pipeline Agent                      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐      │
│  │ Pipeline  │ │  Config  │ │  Test    │ │Deployment│      │
│  │ Manager   │ │Generator │ │Orchestr. │ │ Manager  │      │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘      │
│       │            │            │            │              │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐      │
│  │ Security │ │Notifica- │ │ Quality  │ │ Rollback │      │
│  │ Scanner  │ │tion Mgr  │ │  Gates   │ │  Engine  │      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘      │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Minimal Pipeline

```python
from agents.ci_cd_pipeline.agent import CICDPipelineAgent

agent = CICDPipelineAgent()

pipeline = agent.create_pipeline(
    name="My App CI/CD",
    project="my-app",
    provider="github_actions",
)

config = agent.generate_pipeline_config(pipeline["pipeline_id"])
print(config["configuration"])
```

### Full Pipeline with Security

```python
from agents.ci_cd_pipeline.agent import CICDPipelineAgent

agent = CICDPipelineAgent()

pipeline = agent.create_pipeline(
    name="Secure Pipeline",
    project="secure-app",
    provider="gitlab_ci",
    repository="org/secure-app",
)

agent.configure_build(
    pipeline_id=pipeline["pipeline_id"],
    build_tool="npm",
    language="javascript",
    build_command="npm run build",
    test_command="npm test -- --coverage",
)

agent.configure_security_scanning(
    pipeline_id=pipeline["pipeline_id"],
    sast=True, sca=True, secret_scan=True, container_scan=True,
)

agent.configure_quality_gates(
    pipeline_id=pipeline["pipeline_id"],
    coverage_threshold=80.0,
    max_vulnerabilities=0,
)

config = agent.generate_pipeline_config(pipeline["pipeline_id"])
print(config["configuration"])
```

### Multi-Environment Deployment

```python
from agents.ci_cd_pipeline.agent import CICDPipelineAgent

agent = CICDPipelineAgent()

pipeline = agent.create_pipeline(
    name="Multi-Env Pipeline",
    project="webapp",
    provider="github_actions",
)

agent.configure_build(
    pipeline_id=pipeline["pipeline_id"],
    build_tool="docker",
    language="python",
)

agent.configure_deployment(
    pipeline_id=pipeline["pipeline_id"],
    environment="staging",
    strategy="canary",
    auto_promote=False,
)

agent.configure_deployment(
    pipeline_id=pipeline["pipeline_id"],
    environment="production",
    strategy="blue_green",
    health_check_url="https://app.example.com/health",
)

config = agent.generate_pipeline_config(pipeline["pipeline_id"])
print(config["configuration"])
```

### Custom Build Tool

```python
from agents.ci_cd_pipeline.agent import CICDPipelineAgent

agent = CICDPipelineAgent()

pipeline = agent.create_pipeline(
    name="Go Service Pipeline",
    project="api-gateway",
    provider="azure_devops",
)

agent.configure_build(
    pipeline_id=pipeline["pipeline_id"],
    build_tool="go",
    language="go",
    build_command="go build -o bin/server ./cmd/server",
    test_command="go test -v -race -coverprofile=coverage.out ./...",
)

config = agent.generate_pipeline_config(pipeline["pipeline_id"])
print(config["configuration"])
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
    cache_directories=["node_modules"],
    environment_variables={"NODE_ENV": "production"},
)

# Auto-generates Source → Build → Test stages
```

**Supported build tools per language:**

| Language | Build Tools | Test Commands |
|----------|------------|---------------|
| JavaScript/TypeScript | npm, yarn, pnpm, webpack, vite | jest, vitest, mocha, cypress |
| Python | pip, poetry, pipenv, setuptools | pytest, unittest, tox |
| Go | go build, make, goreleaser | go test, testify |
| Java/Kotlin | maven, gradle, ant | junit, testng, spock |
| Rust | cargo | cargo test |
| Ruby | bundler, rake | rspec, minitest |
| C#/.NET | dotnet, msbuild | dotnet test, xUnit |
| PHP | composer | phpunit |

### Deployment Configuration

```python
# Staging with canary
agent.configure_deployment(
    pipeline_id=pipeline["pipeline_id"],
    environment="staging",
    strategy="canary",
    auto_promote=False,
    health_check_url="https://staging.example.com/health",
    health_check_timeout=120,
)

# Production with blue-green and approval gate
agent.configure_deployment(
    pipeline_id=pipeline["pipeline_id"],
    environment="production",
    strategy="blue_green",
    auto_promote=True,
    health_check_url="https://app.example.com/health",
    health_check_timeout=300,
    approval_required=True,
    approvers=["devops-lead", "security-team"],
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
    tools={
        "sast": ["semgrep", "bandit"],
        "sca": ["snyk", "trivy"],
        "secrets": ["gitleaks", "trufflehog"],
        "container": ["trivy", "grype"],
    },
    fail_on_critical=True,
    fail_on_high=False,
    exclude_patterns=["vendor/", "node_modules/"],
)
```

### Quality Gates

```python
gates = agent.configure_quality_gates(
    pipeline_id=pipeline["pipeline_id"],
    coverage_threshold=80.0,
    max_vulnerabilities=0,
    max_code_smells=10,
    max_duplicate_lines=5.0,
    max_build_time_seconds=600,
    require_all_tests_pass=True,
    require_security_scan=True,
    custom_gates=[
        {"name": "API Docs", "check": "openapi-lint", "threshold": 0},
        {"name": "Performance", "check": "lighthouse", "threshold": 90},
    ],
)
```

### Config Generation

```python
# Generate provider-specific config
config = agent.generate_pipeline_config(pipeline["pipeline_id"])
print(config["configuration"])

# Returns YAML for GitHub Actions, GitLab CI, Azure DevOps
# Returns Groovy for Jenkins
```

### Trigger and Monitor

```python
run = agent.trigger_pipeline(
    pipeline_id=pipeline["pipeline_id"],
    branch="main",
    commit_message="feat: add login endpoint",
)

status = agent.get_pipeline_status(pipeline["pipeline_id"])
print(f"Runs: {status['total_runs']}, Success rate: {status['success_rate']}%")
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

### Notifications

```python
# Notifications are configured per pipeline
pipeline = agent.create_pipeline(
    name="Notified Pipeline",
    project="my-app",
    provider="github_actions",
    notifications={
        "channels": ["slack", "email"],
        "events": ["build.success", "build.failure", "deploy.success"],
        "slack_webhook": "https://hooks.slack.com/services/T.../B.../xxx",
        "email_recipients": ["team@example.com"],
    },
)
```

### Artifact Management

```python
agent.configure_build(
    pipeline_id=pipeline["pipeline_id"],
    build_tool="docker",
    artifact_config={
        "type": "container",
        "registry": "ghcr.io",
        "repository": "myorg/myapp",
        "tag_strategy": "git_sha",
        "retention_days": 30,
    },
)
```

## API Reference

### CICDPipelineAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `create_pipeline()` | `name, project, provider, repository?, description?, stages?, notifications?` | Pipeline dict |
| `configure_build()` | `pipeline_id, build_tool, language?, build_command?, test_command?, cache_directories?, environment_variables?, artifact_config?` | Build config dict |
| `configure_deployment()` | `pipeline_id, environment, strategy?, auto_promote?, auto_rollback?, health_check_url?, health_check_timeout?, approval_required?, approvers?` | Deploy config dict |
| `configure_security_scanning()` | `pipeline_id, sast?, sca?, secret_scan?, container_scan?, tools?, fail_on_critical?, fail_on_high?, exclude_patterns?` | Security config dict |
| `configure_quality_gates()` | `pipeline_id, coverage_threshold?, max_vulnerabilities?, max_code_smells?, max_build_time_seconds?, custom_gates?` | Gates dict |
| `generate_pipeline_config()` | `pipeline_id, output_format?` | Provider config dict |
| `trigger_pipeline()` | `pipeline_id, branch?, commit_sha?, commit_message?` | Run dict |
| `get_pipeline_status()` | `pipeline_id` | Status dict |
| `rollback()` | `pipeline_id, environment, reason, initiated_by?` | Rollback dict |
| `get_security_report()` | `pipeline_id, run_id?` | Security report dict |
| `list_pipelines()` | — | List of pipeline dicts |

### PipelineConfigGenerator

| Method | Parameters | Returns |
|--------|-----------|---------|
| `generate_config()` | `pipeline, output_format` | Provider-specific config string |

Transforms a provider-agnostic pipeline definition into provider-specific YAML or JSON. The `output_format` parameter defaults to `"yaml"` for most providers and `"json"` for Jenkins.

### TestOrchestrator

Manages test execution, coverage collection, and quality gate evaluation across multiple test suites.

| Method | Parameters | Returns |
|--------|-----------|---------|
| `configure_test_suite()` | `pipeline_id, test_configs` | Suite config dict |
| `execute_tests()` | `pipeline_id, run_id, test_configs` | Test results dict |
| `check_quality_gates()` | `gates, metrics` | Gate evaluation dict |

### DeploymentManager

Handles deployment orchestration, promotion between environments, and rollback execution.

| Method | Parameters | Returns |
|--------|-----------|---------|
| `deploy()` | `pipeline_id, run_id, config, artifact?` | Deployment result dict |
| `promote()` | `pipeline_id, deployment_id, target_environment` | Promotion dict |
| `rollback()` | `pipeline_id, run_id, environment, strategy, reason` | Rollback record dict |

### SecurityScanner

Runs security scans (SAST, SCA, secrets, container) and aggregates findings into a unified report.

| Method | Parameters | Returns |
|--------|-----------|---------|
| `scan()` | `pipeline_id, run_id, scan_types?` | Scan results with findings |

### NotificationManager

Sends notifications across configured channels (Slack, email, Teams, webhook) for pipeline events.

| Method | Parameters | Returns |
|--------|-----------|---------|
| `notify()` | `pipeline_id, run_id?, level, title, message, channel?, recipients?` | Notification dict |

## Data Models

**Pipeline** — `pipeline_id` (str, UUID), `name` (str), `project` (str), `provider` (str), `repository` (str), `stages` (List[Stage]), `triggers` (List[Trigger]), `test_configs` (List[Dict]), `quality_gates` (Dict), `deployment_configs` (List[DeploymentConfig]), `security_config` (Dict), `notifications` (Dict), `created_at` (datetime), `updated_at` (datetime).

**Stage** — `name` (str), `steps` (List[Step]), `depends_on` (List[str]), `environment` (Dict[str, str]), `artifacts` (List[str]), `timeout` (int), `allow_failure` (bool).

**PipelineRun** — `run_id` (str, UUID), `pipeline_id` (str), `branch` (str), `commit_sha` (str), `status` (str: pending/running/success/failure/cancelled), `current_stage` (str), `stage_results` (Dict), `started_at` (datetime), `completed_at` (datetime), `duration_seconds` (float).

**DeploymentConfig** — `environment` (str), `strategy` (str), `auto_promote` (bool), `auto_rollback` (bool), `health_check_url` (str), `health_check_timeout` (int), `approval_required` (bool), `approvers` (List[str]).

**Artifact** — `artifact_id` (str), `type` (str: container/binary/package/bundle), `version` (str), `registry` (str), `tag` (str), `size_bytes` (int), `sha256` (str), `created_at` (datetime).

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
    "max_vulnerabilities": 0,
    "notification_channels": ["slack", "email"],
    "slack_webhook": "https://hooks.slack.com/services/T.../B.../xxx",
    "email_recipients": ["team@example.com"],
    "default_deployment_strategy": "canary",
    "health_check_timeout": 120,
    "container_registry": "ghcr.io",
    "pipeline_timeout_minutes": 60,
    "log_level": "INFO",
}
agent = CICDPipelineAgent(config)
```

**Environment Variables:**

| Variable | Description | Default |
|----------|-------------|---------|
| `CICD_DEFAULT_PROVIDER` | Default CI/CD provider | `github_actions` |
| `CICD_COVERAGE_THRESHOLD` | Default coverage threshold | `80.0` |
| `CICD_SECURITY_FAIL_ON` | Security failure severity | `critical` |
| `CICD_SLACK_WEBHOOK` | Slack webhook URL | (none) |
| `CICD_CONTAINER_REGISTRY` | Container registry | `ghcr.io` |
| `CICD_LOG_LEVEL` | Logging level | `INFO` |
| `CICD_TIMEOUT_MINUTES` | Pipeline timeout | `60` |
| `CICD_DEFAULT_STRATEGY` | Default deployment strategy | `canary` |
| `CICD_APPROVAL_REQUIRED` | Require approval for production deploys | `false` |

## Examples

### Node.js Web Application

```python
from agents.ci_cd_pipeline.agent import CICDPipelineAgent

agent = CICDPipelineAgent()

pipeline = agent.create_pipeline(
    name="Node.js Web App",
    project="webapp",
    provider="github_actions",
    repository="org/webapp",
)

agent.configure_build(
    pipeline_id=pipeline["pipeline_id"],
    build_tool="npm",
    language="typescript",
    build_command="npm run build",
    test_command="npm test -- --coverage --ci",
    cache_directories=["node_modules"],
)

agent.configure_security_scanning(
    pipeline_id=pipeline["pipeline_id"],
    sast=True, sca=True, secret_scan=True,
)

agent.configure_quality_gates(
    pipeline_id=pipeline["pipeline_id"],
    coverage_threshold=85.0,
    max_vulnerabilities=0,
)

agent.configure_deployment(
    pipeline_id=pipeline["pipeline_id"],
    environment="staging",
    strategy="rolling",
    health_check_url="https://staging.webapp.example.com/api/health",
)

agent.configure_deployment(
    pipeline_id=pipeline["pipeline_id"],
    environment="production",
    strategy="blue_green",
    health_check_url="https://webapp.example.com/api/health",
    health_check_timeout=300,
    approval_required=True,
    approvers=["tech-lead"],
)

config = agent.generate_pipeline_config(pipeline["pipeline_id"])
print(config["configuration"])
```

### Python Django Service

```python
from agents.ci_cd_pipeline.agent import CICDPipelineAgent

agent = CICDPipelineAgent()

pipeline = agent.create_pipeline(
    name="Django API Service",
    project="django-api",
    provider="gitlab_ci",
)

agent.configure_build(
    pipeline_id=pipeline["pipeline_id"],
    build_tool="poetry",
    language="python",
    test_command="poetry run pytest --cov=src --cov-fail-under=80",
    cache_directories=["poetry", ".venv"],
)

agent.configure_security_scanning(
    pipeline_id=pipeline["pipeline_id"],
    sast=True, sca=True,
    tools={"sast": ["bandit"], "sca": ["safety"]},
)

agent.configure_deployment(
    pipeline_id=pipeline["pipeline_id"],
    environment="production",
    strategy="canary",
    rollout_percentage=5,
    rollout_increment=5,
    rollout_interval_minutes=30,
)

config = agent.generate_pipeline_config(pipeline["pipeline_id"])
print(config["configuration"])
```

### Go Microservice

```python
from agents.ci_cd_pipeline.agent import CICDPipelineAgent

agent = CICDPipelineAgent()

pipeline = agent.create_pipeline(
    name="Go API Gateway",
    project="api-gateway",
    provider="azure_devops",
)

agent.configure_build(
    pipeline_id=pipeline["pipeline_id"],
    build_tool="go",
    language="go",
    build_command="go build -o bin/server ./cmd/server",
    test_command="go test -v -race -coverprofile=coverage.out ./...",
    artifact_config={"type": "binary", "path": "bin/server", "version_strategy": "git_sha"},
)

agent.configure_security_scanning(
    pipeline_id=pipeline["pipeline_id"],
    sast=True, sca=True,
    tools={"sast": ["gosec"], "sca": ["govulncheck"]},
)

agent.configure_deployment(
    pipeline_id=pipeline["pipeline_id"],
    environment="production",
    strategy="blue_green",
    health_check_url="https://api.example.com/readyz",
)

config = agent.generate_pipeline_config(pipeline["pipeline_id"])
print(config["configuration"])
```

### Java Spring Boot Application

```python
from agents.ci_cd_pipeline.agent import CICDPipelineAgent

agent = CICDPipelineAgent()

pipeline = agent.create_pipeline(
    name="Spring Boot Service",
    project="order-service",
    provider="jenkins",
)

agent.configure_build(
    pipeline_id=pipeline["pipeline_id"],
    build_tool="maven",
    language="java",
    build_command="mvn clean package -DskipTests",
    test_command="mvn verify -Pintegration-tests",
    cache_directories=[".m2/repository"],
    artifact_config={"type": "binary", "path": "target/*.jar"},
)

agent.configure_security_scanning(
    pipeline_id=pipeline["pipeline_id"],
    sast=True, sca=True,
    tools={"sast": ["sonarqube"], "sca": ["snyk"]},
)

agent.configure_quality_gates(
    pipeline_id=pipeline["pipeline_id"],
    coverage_threshold=80.0,
    max_vulnerabilities=0,
)

agent.configure_deployment(
    pipeline_id=pipeline["pipeline_id"],
    environment="production",
    strategy="canary",
    rollout_percentage=10,
    rollout_increment=10,
    rollout_interval_minutes=15,
)

config = agent.generate_pipeline_config(pipeline["pipeline_id"])
print(config["configuration"])
```

### Container Image Build and Push

```python
from agents.ci_cd_pipeline.agent import CICDPipelineAgent

agent = CICDPipelineAgent()

pipeline = agent.create_pipeline(
    name="Container Image Pipeline",
    project="worker-service",
    provider="github_actions",
)

agent.configure_build(
    pipeline_id=pipeline["pipeline_id"],
    build_tool="docker",
    artifact_config={
        "type": "container",
        "registry": "ghcr.io",
        "repository": "org/worker-service",
        "tag_strategy": "git_sha",
    },
)

agent.configure_security_scanning(
    pipeline_id=pipeline["pipeline_id"],
    container_scan=True,
    tools={"container": ["trivy", "grype"]},
    fail_on_critical=True,
    fail_on_high=True,
)

agent.configure_deployment(
    pipeline_id=pipeline["pipeline_id"],
    environment="production",
    strategy="rolling",
    health_check_url="https://worker.example.com/health",
)

config = agent.generate_pipeline_config(pipeline["pipeline_id"])
print(config["configuration"])
```

## Best Practices

1. **Pin Dependencies** — Always use lockfiles for reproducible builds. Pin exact versions in CI tool references.
2. **Run Fast Tests First** — Unit tests before integration tests. Fast feedback catches obvious issues early.
3. **Shift-Left Security** — SAST/SCA in every pipeline, not just before production.
4. **Immutable Artifacts** — Build once, deploy the same artifact everywhere. Never rebuild for different environments.
5. **Health Checks on Deploy** — Never consider a deploy complete without health verification.
6. **Test Your Rollback** — A rollback that hasn't been tested is not a rollback.
7. **Use Quality Gates** — Prevent bad code from reaching production with coverage and vulnerability thresholds.
8. **Cache Aggressively** — Cache dependencies and build outputs. A well-cached pipeline can be 5-10x faster.
9. **Keep Pipelines Fast** — Target under 10 minutes. Parallelize independent stages and tests.
10. **Use Separate Environments** — Never deploy directly to production. Use staging as a production mirror.
11. **Automate Everything** — Every manual step is a potential point of failure.
12. **Monitor Pipeline Health** — Track success rates, durations, and failure trends across runs.
13. **Use Branch Protection** — Require PR reviews and passing CI checks before merging.
14. **Rotate Secrets Regularly** — Use provider secret management, never hardcode secrets in pipeline files.
15. **Document Your Pipelines** — Maintain clear documentation of what each pipeline does and how to troubleshoot.

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Build works locally but fails on CI | Use lockfiles, check environment variables, containerize builds |
| Tests flaky on CI | Add retries with backoff, increase timeouts, isolate tests |
| Deployment health check fails | Increase timeout, check dependencies, verify startup order |
| Security scan blocks pipeline | Fix vulnerabilities or add justified exceptions |
| Pipeline too slow | Parallelize stages, add caching, optimize test selection |
| Rollback fails | Design backward-compatible migrations, test rollback regularly |
| Secrets not available | Verify secret is set in correct environment/scope |
| Artifact upload fails | Verify artifact paths, check provider storage limits |
| Docker build fails on CI | Use specific Docker version, check .dockerignore and build context |
| Notifications not sent | Verify webhook URLs, check channel permissions |

## Extending the Agent

### Adding a New Provider

1. Create a config generator class that transforms pipeline definitions to provider-specific syntax
2. Register the generator in the agent's provider registry
3. Add tests for the new generator
4. Update documentation

```python
class CircleCIConfigGenerator:
    def generate(self, pipeline: dict) -> str:
        config = {"version": 2.1, "jobs": {}, "workflows": {"main": {"jobs": []}}}
        for stage in pipeline["stages"]:
            job_name = stage["name"].lower().replace(" ", "_")
            config["jobs"][job_name] = {
                "docker": [{"image": "cimg/base:stable"}],
                "steps": [{"checkout": {}}],
            }
            for step in stage["steps"]:
                config["jobs"][job_name]["steps"].append({
                    "run": {"name": step.get("name", "step"), "command": step["command"]}
                })
            config["workflows"]["main"]["jobs"].append(job_name)
        import yaml
        return yaml.dump(config, default_flow_style=False)
```

### Custom Deployment Strategy

Implement a custom strategy by extending the `DeploymentManager` with your own `deploy()` and `rollback()` methods. See the Blue-Green and Canary implementations in `agent.py` for reference patterns.

## FAQ

**Q: Can I use the agent without a CI/CD provider?**
A: The agent generates provider-specific configuration. You need at least one supported provider to produce usable output.

**Q: How do I switch from GitHub Actions to GitLab CI?**
A: Change the `provider` parameter when creating the pipeline, then regenerate the config. Your pipeline definition stays the same.

**Q: Can I customize the generated YAML?**
A: Yes. The output is a string you can modify before committing. You can also extend the config generators.

**Q: Does the agent support monorepo pipelines?**
A: Yes. Create separate pipelines per service with path-based triggers.

**Q: How do I handle secrets in the generated config?**
A: The agent references secrets by name (e.g., `${{ secrets.DOCKER_PASSWORD }}`). Configure actual values in your provider's secret management.

**Q: Can I run multiple security scanners simultaneously?**
A: Yes. The security scanning configuration accepts a list of tools per scan type, and generates parallel steps.

**Q: What happens if a quality gate fails?**
A: The pipeline fails at the gate stage and does not proceed to deployment.

**Q: Does the agent support self-hosted runners?**
A: Yes. Configure `runs_on` or equivalent in your pipeline's environment variables or stage configuration.

**Q: Can I use the agent for infrastructure pipelines (Terraform, Pulumi)?**
A: Yes. Use custom stages with Terraform/Pulumi commands. See the Infrastructure as Code section in the agent.py examples.

**Q: Is there a way to preview generated config before committing?**
A: Call `generate_pipeline_config()` and print the output. It returns the full config string without writing to disk.

**Q: Can I use the agent in a CI/CD pipeline itself (dogfooding)?**
A: Yes. Install the agent as a dependency and run it in your pipeline setup step to generate configs dynamically.

**Q: How do I handle multi-repository or monorepo pipelines?**
A: Create separate pipelines per service or package, and use path-based triggers to only run when relevant files change.

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams
- `GROK.md` — Agent instructions and identity
- `README.md` — This file
- `tests/` — Unit and integration tests

## Contributing

1. Follow the existing code style with type hints and dataclasses
2. Add provider-specific config generators for new CI/CD platforms
3. Include tests for new deployment strategies
4. Update documentation for API changes
5. Ensure all existing tests pass before submitting

## License

Part of the Awesome Grok Skills collection. See project root for license details.

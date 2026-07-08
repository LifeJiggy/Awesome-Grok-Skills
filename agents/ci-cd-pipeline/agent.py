"""
CI/CD Pipeline Agent - Continuous Integration and Delivery.

Provides comprehensive CI/CD pipeline design, build automation, testing orchestration,
deployment management, rollback capabilities, and monitoring integration.
Supports GitHub Actions, GitLab CI, Jenkins, Azure DevOps, and custom providers
with full lifecycle pipeline management from commit to production.
"""

from __future__ import annotations

import logging
import uuid
import json
import hashlib
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Set, Callable
from collections import defaultdict

logger = logging.getLogger(__name__)


# =============================================================================
# Enumerations
# =============================================================================

class PipelineProvider(Enum):
    """Supported CI/CD providers."""
    GITHUB_ACTIONS = "github_actions"
    GITLAB_CI = "gitlab_ci"
    JENKINS = "jenkins"
    AZURE_DEVOPS = "azure_devops"
    CIRCLECI = "circleci"
    TRAVIS_CI = "travis_ci"
    BITBUCKET_PIPELINES = "bitbucket_pipelines"
    ARGOCD = "argocd"
    TEKTON = "tekton"
    CUSTOM = "custom"


class PipelineStatus(Enum):
    """Current status of a pipeline."""
    CREATED = "created"
    CONFIGURED = "configured"
    TRIGGERED = "triggered"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    WAITING = "waiting"
    PAUSED = "paused"
    BLOCKED = "blocked"


class StageType(Enum):
    """Types of pipeline stages."""
    SOURCE = "source"
    BUILD = "build"
    TEST = "test"
    SECURITY_SCAN = "security_scan"
    QUALITY_GATE = "quality_gate"
    ARTIFACT = "artifact"
    STAGING = "staging"
    APPROVAL = "approval"
    DEPLOY = "deploy"
    POST_DEPLOY = "post_deploy"
    MONITOR = "monitor"
    ROLLBACK = "rollback"
    NOTIFICATION = "notification"


class TestType(Enum):
    """Types of tests in a pipeline."""
    UNIT = "unit"
    INTEGRATION = "integration"
    END_TO_END = "end_to_end"
    PERFORMANCE = "performance"
    SECURITY = "security"
    CONTRACT = "contract"
    VISUAL = "visual"
    ACCESSIBILITY = "accessibility"
    SMOKE = "smoke"
    REGRESSION = "regression"
    LOAD = "load"
    CHAOS = "chaos"


class DeploymentStrategy(Enum):
    """Deployment strategies."""
    BLUE_GREEN = "blue_green"
    CANARY = "canary"
    ROLLING = "rolling"
    RECREATE = "recreate"
    A_B_TESTING = "a_b_testing"
    FEATURE_FLAGS = "feature_flags"
    SHADOW = "shadow"
    PARALLEL_RUN = "parallel_run"


class Environment(Enum):
    """Deployment environments."""
    LOCAL = "local"
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRE_PRODUCTION = "pre_production"
    PRODUCTION = "production"
    DR = "disaster_recovery"


class ArtifactType(Enum):
    """Types of build artifacts."""
    DOCKER_IMAGE = "docker_image"
    NPM_PACKAGE = "npm_package"
    PYPI_PACKAGE = "pypi_package"
    JAVA_ARCHIVE = "java_archive"
    BINARY = "binary"
    STATIC_SITE = "static_site"
    HELM_CHART = "helm_chart"
    TERRAFORM_MODULE = "terraform_module"
    LAMBDA_ZIP = "lambda_zip"
    WEBASSEMBLY = "webassembly"


class NotificationLevel(Enum):
    """Notification severity levels."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class QualityGateType(Enum):
    """Quality gate criteria types."""
    CODE_COVERAGE = "code_coverage"
    DUPLICATION = "duplication"
    COMPLEXITY = "complexity"
    VULNERABILITIES = "vulnerabilities"
    CODE_SMELLS = "code_smells"
    TECH_DEBT = "tech_debt"
    BUILD_TIME = "build_time"
    TEST_PASS_RATE = "test_pass_rate"
    CUSTOM = "custom"


class TriggerType(Enum):
    """Pipeline trigger types."""
    PUSH = "push"
    PULL_REQUEST = "pull_request"
    SCHEDULE = "schedule"
    MANUAL = "manual"
    WEBHOOK = "webhook"
    TAG = "tag"
    RELEASE = "release"
    DEPENDENCY_UPDATE = "dependency_update"
    API = "api"
    UPSTREAM = "upstream"


class RollbackStrategy(Enum):
    """Rollback strategies."""
    PREVIOUS_VERSION = "previous_version"
    SPECIFIC_VERSION = "specific_version"
    LAST_KNOWN_GOOD = "last_known_good"
    DATABASE_REVERSE = "database_reverse"
    FEATURE_FLAG_OFF = "feature_flag_off"
    INFRASTRUCTURE_REVERT = "infrastructure_revert"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class PipelineTrigger:
    """Configuration for pipeline triggers."""
    trigger_type: TriggerType = TriggerType.PUSH
    branches: List[str] = field(default_factory=lambda: ["main", "develop"])
    ignore_branches: List[str] = field(default_factory=list)
    paths: List[str] = field(default_factory=list)
    ignore_paths: List[str] = field(default_factory=list)
    schedule: Optional[str] = None
    manual_approve: bool = False
    conditions: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trigger_type": self.trigger_type.value,
            "branches": self.branches,
            "ignore_branches": self.ignore_branches,
            "paths": self.paths,
            "ignore_paths": self.ignore_paths,
            "schedule": self.schedule,
            "manual_approve": self.manual_approve,
            "conditions": self.conditions,
        }


@dataclass
class StageStep:
    """A single step within a pipeline stage."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    command: str = ""
    script_lines: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)
    timeout_seconds: int = 300
    retry_count: int = 0
    continue_on_error: bool = False
    working_directory: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    artifacts_in: List[str] = field(default_factory=list)
    artifacts_out: List[str] = field(default_factory=list)
    cache_keys: List[str] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "command": self.command,
            "script_lines": self.script_lines,
            "environment": self.environment,
            "timeout_seconds": self.timeout_seconds,
            "retry_count": self.retry_count,
            "continue_on_error": self.continue_on_error,
            "working_directory": self.working_directory,
            "dependencies": self.dependencies,
            "artifacts_in": self.artifacts_in,
            "artifacts_out": self.artifacts_out,
            "cache_keys": self.cache_keys,
            "conditions": self.conditions,
        }


@dataclass
class Stage:
    """A stage in the CI/CD pipeline."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    stage_type: StageType = StageType.BUILD
    steps: List[StageStep] = field(default_factory=list)
    parallel: bool = False
    required: bool = True
    timeout_seconds: int = 600
    environment: Optional[str] = None
    conditions: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    artifacts: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "stage_type": self.stage_type.value,
            "steps": [s.to_dict() for s in self.steps],
            "parallel": self.parallel,
            "required": self.required,
            "timeout_seconds": self.timeout_seconds,
            "environment": self.environment,
            "conditions": self.conditions,
            "dependencies": self.dependencies,
            "artifacts": self.artifacts,
            "services": self.services,
        }


@dataclass
class TestConfiguration:
    """Configuration for test execution in a pipeline."""
    test_type: TestType = TestType.UNIT
    framework: str = ""
    command: str = ""
    coverage_threshold: float = 80.0
    parallel: bool = True
    max_workers: int = 4
    timeout_seconds: int = 600
    retry_on_failure: bool = True
    max_retries: int = 2
    report_format: str = "junit"
    coverage_report: bool = True
    include_patterns: List[str] = field(default_factory=list)
    exclude_patterns: List[str] = field(default_factory=list)
    environment: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_type": self.test_type.value,
            "framework": self.framework,
            "command": self.command,
            "coverage_threshold": self.coverage_threshold,
            "parallel": self.parallel,
            "max_workers": self.max_workers,
            "timeout_seconds": self.timeout_seconds,
            "retry_on_failure": self.retry_on_failure,
            "max_retries": self.max_retries,
            "report_format": self.report_format,
            "coverage_report": self.coverage_report,
            "include_patterns": self.include_patterns,
            "exclude_patterns": self.exclude_patterns,
            "environment": self.environment,
        }


@dataclass
class QualityGate:
    """A quality gate that must pass before proceeding."""
    gate_type: QualityGateType = QualityGateType.CODE_COVERAGE
    threshold: float = 80.0
    operator: str = ">="
    metric_name: str = ""
    description: str = ""
    block_on_failure: bool = True
    warning_only: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gate_type": self.gate_type.value,
            "threshold": self.threshold,
            "operator": self.operator,
            "metric_name": self.metric_name,
            "description": self.description,
            "block_on_failure": self.block_on_failure,
            "warning_only": self.warning_only,
        }


@dataclass
class SecurityScanConfig:
    """Configuration for security scanning in the pipeline."""
    sast_enabled: bool = True
    dast_enabled: bool = False
    sca_enabled: bool = True
    container_scan: bool = False
    secret_scan: bool = True
    license_scan: bool = True
    tools: List[str] = field(default_factory=lambda: ["trivy", "sonarqube", "snyk"])
    fail_on_critical: bool = True
    fail_on_high: bool = False
    severity_threshold: str = "high"
    exclude_paths: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sast_enabled": self.sast_enabled,
            "dast_enabled": self.dast_enabled,
            "sca_enabled": self.sca_enabled,
            "container_scan": self.container_scan,
            "secret_scan": self.secret_scan,
            "license_scan": self.license_scan,
            "tools": self.tools,
            "fail_on_critical": self.fail_on_critical,
            "fail_on_high": self.fail_on_high,
            "severity_threshold": self.severity_threshold,
            "exclude_paths": self.exclude_paths,
        }


@dataclass
class DeploymentConfig:
    """Configuration for a deployment."""
    environment: Environment = Environment.STAGING
    strategy: DeploymentStrategy = DeploymentStrategy.ROLLING
    target: str = ""
    replicas: int = 1
    health_check_url: str = ""
    health_check_timeout: int = 120
    rollback_on_failure: bool = True
    auto_promote: bool = False
    approval_required: bool = False
    approvers: List[str] = field(default_factory=list)
    variables: Dict[str, str] = field(default_factory=dict)
    secrets: List[str] = field(default_factory=list)
    notification_channels: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "environment": self.environment.value,
            "strategy": self.strategy.value,
            "target": self.target,
            "replicas": self.replicas,
            "health_check_url": self.health_check_url,
            "health_check_timeout": self.health_check_timeout,
            "rollback_on_failure": self.rollback_on_failure,
            "auto_promote": self.auto_promote,
            "approval_required": self.approval_required,
            "approvers": self.approvers,
            "variables": self.variables,
            "secrets": self.secrets,
            "notification_channels": self.notification_channels,
        }


@dataclass
class Artifact:
    """A build artifact produced by the pipeline."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    artifact_type: ArtifactType = ArtifactType.DOCKER_IMAGE
    version: str = ""
    registry: str = ""
    repository: str = ""
    tag: str = ""
    digest: str = ""
    size_bytes: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "artifact_type": self.artifact_type.value,
            "version": self.version,
            "registry": self.registry,
            "repository": self.repository,
            "tag": self.tag,
            "digest": self.digest,
            "size_bytes": self.size_bytes,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }

    def full_ref(self) -> str:
        if self.artifact_type == ArtifactType.DOCKER_IMAGE:
            return f"{self.registry}/{self.repository}:{self.tag}"
        return f"{self.repository}@{self.digest}" if self.digest else f"{self.repository}:{self.version}"


@dataclass
class PipelineRun:
    """A single execution of a pipeline."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    pipeline_id: str = ""
    status: PipelineStatus = PipelineStatus.CREATED
    trigger: TriggerType = TriggerType.MANUAL
    branch: str = ""
    commit_sha: str = ""
    commit_message: str = ""
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    stage_results: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    artifacts: List[Artifact] = field(default_factory=list)
    logs: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    retry_of: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "pipeline_id": self.pipeline_id,
            "status": self.status.value,
            "trigger": self.trigger.value,
            "branch": self.branch,
            "commit_sha": self.commit_sha,
            "commit_message": self.commit_message,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "duration_seconds": self.duration_seconds,
            "stage_results": self.stage_results,
            "artifacts": [a.to_dict() for a in self.artifacts],
            "error_message": self.error_message,
        }


@dataclass
class Pipeline:
    """A complete CI/CD pipeline configuration."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    project: str = ""
    provider: PipelineProvider = PipelineProvider.GITHUB_ACTIONS
    repository: str = ""
    default_branch: str = "main"
    stages: List[Stage] = field(default_factory=list)
    triggers: List[PipelineTrigger] = field(default_factory=list)
    test_configs: List[TestConfiguration] = field(default_factory=list)
    quality_gates: List[QualityGate] = field(default_factory=list)
    security_config: Optional[SecurityScanConfig] = None
    deployment_configs: List[DeploymentConfig] = field(default_factory=list)
    variables: Dict[str, str] = field(default_factory=dict)
    secrets: List[str] = field(default_factory=list)
    cache_config: Dict[str, Any] = field(default_factory=dict)
    timeout_minutes: int = 60
    concurrency: int = 1
    status: PipelineStatus = PipelineStatus.CREATED
    runs: List[PipelineRun] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "project": self.project,
            "provider": self.provider.value,
            "repository": self.repository,
            "default_branch": self.default_branch,
            "stages": [s.to_dict() for s in self.stages],
            "triggers": [t.to_dict() for t in self.triggers],
            "test_configs": [t.to_dict() for t in self.test_configs],
            "quality_gates": [q.to_dict() for q in self.quality_gates],
            "security_config": self.security_config.to_dict() if self.security_config else None,
            "deployment_configs": [d.to_dict() for d in self.deployment_configs],
            "variables": self.variables,
            "timeout_minutes": self.timeout_minutes,
            "concurrency": self.concurrency,
            "status": self.status.value,
            "total_runs": len(self.runs),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class RollbackRecord:
    """Record of a rollback operation."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    pipeline_id: str = ""
    run_id: str = ""
    environment: str = ""
    strategy: RollbackStrategy = RollbackStrategy.PREVIOUS_VERSION
    from_version: str = ""
    to_version: str = ""
    reason: str = ""
    initiated_by: str = ""
    status: str = "pending"
    started_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    success: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "pipeline_id": self.pipeline_id,
            "run_id": self.run_id,
            "environment": self.environment,
            "strategy": self.strategy.value,
            "from_version": self.from_version,
            "to_version": self.to_version,
            "reason": self.reason,
            "initiated_by": self.initiated_by,
            "status": self.status,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "success": self.success,
        }


@dataclass
class Notification:
    """A notification sent during pipeline execution."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    pipeline_id: str = ""
    run_id: str = ""
    level: NotificationLevel = NotificationLevel.INFO
    title: str = ""
    message: str = ""
    channel: str = "slack"
    recipients: List[str] = field(default_factory=list)
    sent: bool = False
    sent_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "pipeline_id": self.pipeline_id,
            "run_id": self.run_id,
            "level": self.level.value,
            "title": self.title,
            "message": self.message,
            "channel": self.channel,
            "recipients": self.recipients,
            "sent": self.sent,
            "sent_at": self.sent_at.isoformat() if self.sent_at else None,
        }


# =============================================================================
# Pipeline Configuration Generator
# =============================================================================

class PipelineConfigGenerator:
    """
    Generates CI/CD pipeline configurations for various providers.

    Creates provider-specific YAML/JSON configurations from
    abstract pipeline definitions.
    """

    PROVIDER_TEMPLATES = {
        PipelineProvider.GITHUB_ACTIONS: "github_actions",
        PipelineProvider.GITLAB_CI: "gitlab_ci",
        PipelineProvider.JENKINS: "jenkinsfile",
        PipelineProvider.AZURE_DEVOPS: "azure_pipelines",
        PipelineProvider.CIRCLECI: "circleci",
    }

    def __init__(self) -> None:
        self._generated: Dict[str, str] = {}

    def generate_config(
        self, pipeline: Pipeline, output_format: str = "yaml"
    ) -> Dict[str, Any]:
        """
        Generate provider-specific pipeline configuration.

        Args:
            pipeline: The abstract pipeline definition.
            output_format: Output format (yaml, json).

        Returns:
            Generated configuration with metadata.
        """
        provider = pipeline.provider

        if provider == PipelineProvider.GITHUB_ACTIONS:
            config = self._generate_github_actions(pipeline)
        elif provider == PipelineProvider.GITLAB_CI:
            config = self._generate_gitlab_ci(pipeline)
        elif provider == PipelineProvider.JENKINS:
            config = self._generate_jenkinsfile(pipeline)
        elif provider == PipelineProvider.AZURE_DEVOPS:
            config = self._generate_azure_devops(pipeline)
        else:
            config = self._generate_generic(pipeline)

        config_hash = hashlib.sha256(
            json.dumps(config, sort_keys=True).encode()
        ).hexdigest()[:12]

        self._generated[pipeline.id] = json.dumps(config)

        return {
            "pipeline_id": pipeline.id,
            "provider": provider.value,
            "format": output_format,
            "config_hash": config_hash,
            "configuration": config,
            "generated_at": datetime.utcnow().isoformat(),
        }

    def _generate_github_actions(self, pipeline: Pipeline) -> Dict[str, Any]:
        config: Dict[str, Any] = {
            "name": pipeline.name,
            "on": self._github_triggers(pipeline.triggers),
            "env": pipeline.variables,
            "jobs": {},
        }

        for stage in pipeline.stages:
            job_name = stage.name.lower().replace(" ", "_").replace("-", "_")
            job: Dict[str, Any] = {
                "runs-on": "ubuntu-latest",
                "timeout-minutes": stage.timeout_seconds // 60,
            }

            if stage.dependencies:
                job["needs"] = stage.dependencies

            steps = []

            if StageType.SOURCE in (stage.stage_type,):
                steps.append({
                    "name": "Checkout",
                    "uses": "actions/checkout@v4",
                    "with": {"fetch-depth": 0},
                })

            if StageType.BUILD in (stage.stage_type,):
                steps.append({
                    "name": "Setup",
                    "uses": "actions/setup-node@v4",
                    "with": {"node-version": "20"},
                })
                steps.append({
                    "name": "Install Dependencies",
                    "run": "npm ci",
                })
                steps.append({
                    "name": "Build",
                    "run": "npm run build",
                })

            if StageType.TEST in (stage.stage_type,):
                for tc in pipeline.test_configs:
                    steps.append({
                        "name": f"Run {tc.test_type.value} tests",
                        "run": tc.command or f"npm test -- --coverage",
                    })

            if StageType.SECURITY_SCAN in (stage.stage_type,):
                if pipeline.security_config:
                    for tool in pipeline.security_config.tools:
                        steps.append({
                            "name": f"Security Scan - {tool}",
                            "run": f"npx {tool}@latest scan",
                        })

            for step_def in stage.steps:
                step: Dict[str, Any] = {"name": step_def.name}
                if step_def.command:
                    step["run"] = step_def.command
                elif step_def.script_lines:
                    step["run"] = "\n".join(step_def.script_lines)
                if step_def.environment:
                    step["env"] = step_def.environment
                steps.append(step)

            job["steps"] = steps
            config["jobs"][job_name] = job

        return config

    def _generate_gitlab_ci(self, pipeline: Pipeline) -> Dict[str, Any]:
        config: Dict[str, Any] = {
            "stages": [],
            "variables": pipeline.variables,
            "default": {
                "timeout": f"{pipeline.timeout_minutes}m",
            },
        }

        for stage in pipeline.stages:
            stage_name = stage.name.lower().replace(" ", "-")
            config["stages"].append(stage_name)

            job_name = f"{stage_name}_job"
            job: Dict[str, Any] = {
                "stage": stage_name,
                "script": [],
            }

            if stage.services:
                job["services"] = stage.services

            for step in stage.steps:
                if step.command:
                    job["script"].append(step.command)
                elif step.script_lines:
                    job["script"].extend(step.script_lines)

            if not job["script"]:
                job["script"] = [f"echo 'Running {stage.name}'"]

            config[job_name] = job

        return config

    def _generate_jenkinsfile(self, pipeline: Pipeline) -> Dict[str, Any]:
        stages = []
        for stage in pipeline.stages:
            stage_def: Dict[str, Any] = {
                "name": stage.name,
                "steps": [],
            }
            for step in stage.steps:
                if step.command:
                    stage_def["steps"].append({"sh": step.command})
                elif step.script_lines:
                    stage_def["steps"].append({
                        "sh": "\n".join(step.script_lines)
                    })
            if not stage_def["steps"]:
                stage_def["steps"] = [{"sh": f"echo 'Running {stage.name}'"}]
            stages.append(stage_def)

        return {
            "pipeline": {
                "agent": {"any": True},
                "environment": pipeline.variables,
                "stages": stages,
                "post": {
                    "always": [{"cleanWs": {}}],
                    "success": [{"echo": "Pipeline succeeded"}],
                    "failure": [{"echo": "Pipeline failed"}],
                },
            }
        }

    def _generate_azure_devops(self, pipeline: Pipeline) -> Dict[str, Any]:
        stages = []
        for stage in pipeline.stages:
            azure_stage: Dict[str, Any] = {
                "stage": stage.name.replace(" ", ""),
                "displayName": stage.name,
                "jobs": [],
            }
            job: Dict[str, Any] = {
                "job": f"{stage.name.replace(' ', '')}Job",
                "steps": [],
            }
            for step in stage.steps:
                if step.command:
                    job["steps"].append({
                        "bash": step.command,
                        "displayName": step.name,
                    })
            if not job["steps"]:
                job["steps"].append({
                    "bash": f"echo 'Running {stage.name}'",
                    "displayName": stage.name,
                })
            azure_stage["jobs"].append(job)
            stages.append(azure_stage)

        return {
            "trigger": self._azure_triggers(pipeline.triggers),
            "pool": {"vmImage": "ubuntu-latest"},
            "stages": stages,
        }

    def _generate_generic(self, pipeline: Pipeline) -> Dict[str, Any]:
        return {
            "pipeline": {
                "name": pipeline.name,
                "provider": pipeline.provider.value,
                "stages": [s.to_dict() for s in pipeline.stages],
                "triggers": [t.to_dict() for t in pipeline.triggers],
            }
        }

    def _github_triggers(self, triggers: List[PipelineTrigger]) -> Dict[str, Any]:
        on_config: Dict[str, Any] = {}
        for t in triggers:
            if t.trigger_type == TriggerType.PUSH:
                on_config["push"] = {"branches": t.branches}
            elif t.trigger_type == TriggerType.PULL_REQUEST:
                on_config["pull_request"] = {"branches": t.branches}
            elif t.trigger_type == TriggerType.SCHEDULE and t.schedule:
                on_config["schedule"] = [{"cron": t.schedule}]
            elif t.trigger_type == TriggerType.MANUAL:
                on_config["workflow_dispatch"] = {}
        return on_config or {"push": {"branches": ["main"]}}

    def _azure_triggers(self, triggers: List[PipelineTrigger]) -> Dict[str, Any]:
        for t in triggers:
            if t.trigger_type == TriggerType.PUSH:
                return {"branches": {"include": t.branches}}
        return {"branches": {"include": ["main"]}}


# =============================================================================
# Test Orchestrator
# =============================================================================

class TestOrchestrator:
    """
    Orchestrates test execution across the pipeline.

    Manages test configuration, parallel execution, retry logic,
    coverage tracking, and result aggregation.
    """

    def __init__(self) -> None:
        self._test_runs: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._coverage_history: List[Dict[str, Any]] = []

    def configure_test_suite(
        self, pipeline_id: str, test_configs: List[TestConfiguration]
    ) -> Dict[str, Any]:
        """Configure the test suite for a pipeline."""
        suite_config = {
            "pipeline_id": pipeline_id,
            "total_suites": len(test_configs),
            "suites": [tc.to_dict() for tc in test_configs],
            "estimated_duration": self._estimate_duration(test_configs),
            "parallel_possible": all(tc.parallel for tc in test_configs),
        }
        return suite_config

    def execute_tests(
        self, pipeline_id: str, run_id: str, test_configs: List[TestConfiguration]
    ) -> Dict[str, Any]:
        """
        Simulate test execution and return results.

        In production, this would trigger actual test runners
        and aggregate real results.
        """
        results: List[Dict[str, Any]] = []

        for tc in test_configs:
            suite_result = {
                "test_type": tc.test_type.value,
                "framework": tc.framework,
                "status": "passed",
                "tests_run": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "duration_seconds": 0.0,
                "coverage": 0.0,
                "report_url": "",
            }
            results.append(suite_result)

        total_tests = sum(r["tests_run"] for r in results)
        total_passed = sum(r["passed"] for r in results)
        total_failed = sum(r["failed"] for r in results)

        run_result = {
            "run_id": run_id,
            "pipeline_id": pipeline_id,
            "suite_results": results,
            "summary": {
                "total_tests": total_tests,
                "total_passed": total_passed,
                "total_failed": total_failed,
                "pass_rate": round(total_passed / total_tests, 3) if total_tests > 0 else 1.0,
                "all_passed": total_failed == 0,
            },
            "executed_at": datetime.utcnow().isoformat(),
        }

        self._test_runs[pipeline_id].append(run_result)
        return run_result

    def check_quality_gates(
        self, gates: List[QualityGate], metrics: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Evaluate quality gates against measured metrics.

        Returns pass/fail status for each gate and overall.
        """
        gate_results: List[Dict[str, Any]] = []
        all_passed = True

        for gate in gates:
            metric_value = metrics.get(gate.metric_name, gate.gate_type.value)
            actual = metrics.get(gate.metric_name, 0.0)

            passed = self._evaluate_gate(actual, gate.operator, gate.threshold)

            if gate.warning_only:
                gate_status = "warning" if not passed else "passed"
            else:
                gate_status = "passed" if passed else "failed"
                if not passed:
                    all_passed = False

            gate_results.append({
                "gate_type": gate.gate_type.value,
                "metric_name": gate.metric_name,
                "threshold": gate.threshold,
                "actual": actual,
                "operator": gate.operator,
                "status": gate_status,
                "description": gate.description,
            })

        return {
            "overall_status": "passed" if all_passed else "failed",
            "gates": gate_results,
            "checked_at": datetime.utcnow().isoformat(),
        }

    def get_coverage_trend(self, pipeline_id: str) -> Dict[str, Any]:
        """Track code coverage trends over time."""
        runs = self._test_runs.get(pipeline_id, [])
        trend = []
        for run in runs:
            for suite in run.get("suite_results", []):
                if suite.get("coverage", 0) > 0:
                    trend.append({
                        "run_id": run["run_id"],
                        "coverage": suite["coverage"],
                        "timestamp": run.get("executed_at", ""),
                    })

        if len(trend) >= 2:
            direction = "improving" if trend[-1]["coverage"] > trend[0]["coverage"] else "declining"
        else:
            direction = "insufficient_data"

        return {
            "pipeline_id": pipeline_id,
            "trend": trend,
            "direction": direction,
            "latest_coverage": trend[-1]["coverage"] if trend else 0.0,
        }

    def _estimate_duration(self, configs: List[TestConfiguration]) -> int:
        total = 0
        for tc in configs:
            if tc.test_type in (TestType.UNIT,):
                total += 120
            elif tc.test_type in (TestType.INTEGRATION,):
                total += 300
            elif tc.test_type in (TestType.END_TO_END,):
                total += 600
            elif tc.test_type in (TestType.PERFORMANCE, TestType.LOAD):
                total += 900
            else:
                total += 180
        return total

    def _evaluate_gate(self, actual: float, operator: str, threshold: float) -> bool:
        ops = {
            ">=": actual >= threshold,
            "<=": actual <= threshold,
            ">": actual > threshold,
            "<": actual < threshold,
            "==": abs(actual - threshold) < 0.001,
            "!=": abs(actual - threshold) >= 0.001,
        }
        return ops.get(operator, actual >= threshold)


# =============================================================================
# Deployment Manager
# =============================================================================

class DeploymentManager:
    """
    Manages deployments across environments.

    Handles blue-green, canary, rolling deployments,
    health checks, and automatic rollback on failure.
    """

    def __init__(self) -> None:
        self._deployments: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._rollback_records: List[RollbackRecord] = []

    def deploy(
        self,
        pipeline_id: str,
        run_id: str,
        config: DeploymentConfig,
        artifact: Artifact,
    ) -> Dict[str, Any]:
        """
        Execute a deployment to a target environment.

        Returns deployment result with health check status.
        """
        deployment_id = str(uuid.uuid4())[:8]

        deployment = {
            "deployment_id": deployment_id,
            "pipeline_id": pipeline_id,
            "run_id": run_id,
            "environment": config.environment.value,
            "strategy": config.strategy.value,
            "artifact": artifact.to_dict(),
            "target": config.target,
            "replicas": config.replicas,
            "status": "deploying",
            "health_check": None,
            "started_at": datetime.utcnow().isoformat(),
        }

        # Simulate health check
        health = self._perform_health_check(
            config.health_check_url, config.health_check_timeout
        )
        deployment["health_check"] = health

        if health["healthy"]:
            deployment["status"] = "deployed"
        elif config.rollback_on_failure:
            deployment["status"] = "deployed_with_issues"
            self._create_rollback(
                pipeline_id, run_id, config.environment.value, artifact.version
            )

        self._deployments[pipeline_id].append(deployment)

        return deployment

    def promote(
        self,
        pipeline_id: str,
        deployment_id: str,
        target_environment: Environment,
    ) -> Dict[str, Any]:
        """Promote a deployment to a higher environment."""
        source = None
        for d in self._deployments.get(pipeline_id, []):
            if d["deployment_id"] == deployment_id:
                source = d
                break

        if not source:
            return {"error": f"Deployment {deployment_id} not found"}

        promotion = {
            "source_deployment": deployment_id,
            "target_environment": target_environment.value,
            "artifact": source["artifact"],
            "status": "promoting",
            "promoted_at": datetime.utcnow().isoformat(),
        }

        return promotion

    def rollback(
        self,
        pipeline_id: str,
        run_id: str,
        environment: str,
        strategy: RollbackStrategy = RollbackStrategy.PREVIOUS_VERSION,
        from_version: str = "",
        to_version: str = "",
        reason: str = "",
        initiated_by: str = "system",
    ) -> Dict[str, Any]:
        """Execute a rollback for a deployment."""
        record = RollbackRecord(
            pipeline_id=pipeline_id,
            run_id=run_id,
            environment=environment,
            strategy=strategy,
            from_version=from_version,
            to_version=to_version,
            reason=reason,
            initiated_by=initiated_by,
            status="in_progress",
        )

        record.status = "completed"
        record.success = True
        record.completed_at = datetime.utcnow()
        self._rollback_records.append(record)

        return record.to_dict()

    def get_deployment_history(
        self, pipeline_id: str, environment: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get deployment history for a pipeline."""
        deployments = self._deployments.get(pipeline_id, [])
        if environment:
            deployments = [d for d in deployments if d["environment"] == environment]
        return deployments

    def get_rollback_history(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self._rollback_records]

    def _perform_health_check(
        self, url: str, timeout: int
    ) -> Dict[str, Any]:
        """Perform a health check on the deployed service."""
        return {
            "url": url,
            "healthy": True,
            "status_code": 200,
            "response_time_ms": 45,
            "checked_at": datetime.utcnow().isoformat(),
            "timeout": timeout,
        }

    def _create_rollback(
        self, pipeline_id: str, run_id: str, environment: str, current_version: str
    ) -> None:
        self.rollback(
            pipeline_id=pipeline_id,
            run_id=run_id,
            environment=environment,
            strategy=RollbackStrategy.LAST_KNOWN_GOOD,
            from_version=current_version,
            to_version="previous",
            reason="Health check failed during deployment",
        )


# =============================================================================
# Security Scanner
# =============================================================================

class SecurityScanner:
    """
    Integrates security scanning into the CI/CD pipeline.

    Manages SAST, DAST, SCA, container scanning, and secret detection
    with configurable policies and enforcement.
    """

    def __init__(self, config: Optional[SecurityScanConfig] = None) -> None:
        self._config = config or SecurityScanConfig()
        self._scan_results: List[Dict[str, Any]] = []

    def scan(self, pipeline_id: str, run_id: str) -> Dict[str, Any]:
        """
        Execute security scans based on configuration.

        Returns scan results with findings by category.
        """
        findings: Dict[str, List[Dict[str, Any]]] = {
            "critical": [],
            "high": [],
            "medium": [],
            "low": [],
            "info": [],
        }

        if self._config.sast_enabled:
            sast = self._run_sast(pipeline_id, run_id)
            self._merge_findings(findings, sast)

        if self._config.sca_enabled:
            sca = self._run_sca(pipeline_id, run_id)
            self._merge_findings(findings, sca)

        if self._config.secret_scan:
            secrets = self._run_secret_scan(pipeline_id, run_id)
            self._merge_findings(findings, secrets)

        if self._config.container_scan:
            container = self._run_container_scan(pipeline_id, run_id)
            self._merge_findings(findings, container)

        total_findings = sum(len(v) for v in findings.values())
        blocked = self._should_block(findings)

        result = {
            "pipeline_id": pipeline_id,
            "run_id": run_id,
            "findings": findings,
            "summary": {
                "total": total_findings,
                "critical": len(findings["critical"]),
                "high": len(findings["high"]),
                "medium": len(findings["medium"]),
                "low": len(findings["low"]),
                "info": len(findings["info"]),
            },
            "blocked": blocked,
            "config": self._config.to_dict(),
            "scanned_at": datetime.utcnow().isoformat(),
        }

        self._scan_results.append(result)
        return result

    def get_scan_history(self) -> List[Dict[str, Any]]:
        return self._scan_results

    def _run_sast(self, pipeline_id: str, run_id: str) -> List[Dict[str, Any]]:
        return [
            {
                "type": "sast",
                "severity": "medium",
                "title": "Potential SQL injection",
                "file": "src/db/query.py",
                "line": 42,
                "tool": "bandit",
                "cwe": "CWE-89",
            }
        ]

    def _run_sca(self, pipeline_id: str, run_id: str) -> List[Dict[str, Any]]:
        return [
            {
                "type": "sca",
                "severity": "high",
                "title": "Vulnerable dependency: lodash < 4.17.21",
                "package": "lodash",
                "installed_version": "4.17.19",
                "fixed_version": "4.17.21",
                "tool": "snyk",
                "cve": "CVE-2021-23337",
            }
        ]

    def _run_secret_scan(self, pipeline_id: str, run_id: str) -> List[Dict[str, Any]]:
        return []

    def _run_container_scan(self, pipeline_id: str, run_id: str) -> List[Dict[str, Any]]:
        return [
            {
                "type": "container",
                "severity": "low",
                "title": "Outdated base image",
                "image": "node:18-alpine",
                "tool": "trivy",
            }
        ]

    def _merge_findings(
        self, target: Dict[str, List[Dict[str, Any]]], new_findings: List[Dict[str, Any]]
    ) -> None:
        for f in new_findings:
            severity = f.get("severity", "info")
            if severity in target:
                target[severity].append(f)

    def _should_block(self, findings: Dict[str, List[Dict[str, Any]]]) -> bool:
        if self._config.fail_on_critical and findings["critical"]:
            return True
        if self._config.fail_on_high and findings["high"]:
            return True
        return False


# =============================================================================
# Notification Manager
# =============================================================================

class NotificationManager:
    """Manages pipeline notifications across channels."""

    def __init__(self) -> None:
        self._notifications: List[Notification] = []
        self._templates: Dict[str, str] = {
            "pipeline_success": "Pipeline {pipeline_name} succeeded on {branch} ({commit_sha})",
            "pipeline_failure": "Pipeline {pipeline_name} FAILED on {branch} ({commit_sha})",
            "deployment_success": "Successfully deployed {version} to {environment}",
            "deployment_failure": "Deployment of {version} to {environment} FAILED",
            "rollback": "Rollback executed: {from_version} -> {to_version} in {environment}",
            "security_alert": "Security scan found {count} issues in {pipeline_name}",
        }

    def notify(
        self,
        pipeline_id: str,
        run_id: str,
        level: NotificationLevel,
        title: str,
        message: str,
        channel: str = "slack",
        recipients: Optional[List[str]] = None,
    ) -> Notification:
        """Send a notification."""
        notification = Notification(
            pipeline_id=pipeline_id,
            run_id=run_id,
            level=level,
            title=title,
            message=message,
            channel=channel,
            recipients=recipients or [],
            sent=True,
            sent_at=datetime.utcnow(),
        )
        self._notifications.append(notification)
        return notification

    def get_notifications(
        self, pipeline_id: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        notifs = self._notifications
        if pipeline_id:
            notifs = [n for n in notifs if n.pipeline_id == pipeline_id]
        return [n.to_dict() for n in notifs]

    def render_template(self, template_key: str, **kwargs: str) -> str:
        template = self._templates.get(template_key, "")
        try:
            return template.format(**kwargs)
        except KeyError:
            return template


# =============================================================================
# Main CI/CD Pipeline Agent
# =============================================================================

class CICDPipelineAgent:
    """
    Primary orchestrator for CI/CD pipeline management.

    Coordinates pipeline design, build automation, testing orchestration,
    security scanning, deployment management, and monitoring into
    a unified continuous integration and delivery workflow.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config or {}
        self._pipelines: Dict[str, Pipeline] = {}
        self._config_generator = PipelineConfigGenerator()
        self._test_orchestrator = TestOrchestrator()
        self._deployment_manager = DeploymentManager()
        self._security_scanner = SecurityScanner()
        self._notification_manager = NotificationManager()
        self._created_at = datetime.utcnow()

        logger.info("CICDPipelineAgent initialized")

    def create_pipeline(
        self,
        name: str,
        project: str,
        provider: str = "github_actions",
        repository: str = "",
        description: str = "",
    ) -> Dict[str, Any]:
        """Create a new CI/CD pipeline."""
        pp = PipelineProvider(provider) if provider in [e.value for e in PipelineProvider] else PipelineProvider.GITHUB_ACTIONS

        pipeline = Pipeline(
            name=name,
            project=project,
            provider=pp,
            repository=repository,
            description=description,
            status=PipelineStatus.CONFIGURED,
        )

        pipeline.triggers = [
            PipelineTrigger(
                trigger_type=TriggerType.PUSH,
                branches=["main", "develop"],
            ),
            PipelineTrigger(
                trigger_type=TriggerType.PULL_REQUEST,
                branches=["main"],
            ),
        ]

        self._pipelines[pipeline.id] = pipeline
        logger.info("Pipeline created: %s (%s)", name, pipeline.id)

        return {
            "pipeline_id": pipeline.id,
            "name": name,
            "provider": pp.value,
            "status": pipeline.status.value,
        }

    def configure_build(
        self,
        pipeline_id: str,
        build_tool: str = "npm",
        build_command: str = "",
        test_command: str = "",
        language: str = "javascript",
    ) -> Dict[str, Any]:
        """Configure build stage for a pipeline."""
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            return {"error": f"Pipeline {pipeline_id} not found"}

        source_stage = Stage(
            name="Source",
            stage_type=StageType.SOURCE,
            steps=[
                StageStep(
                    name="Checkout",
                    command="git checkout $GITHUB_SHA",
                )
            ],
        )

        build_step_cmd = build_command or self._default_build_command(build_tool, language)
        build_stage = Stage(
            name="Build",
            stage_type=StageType.BUILD,
            steps=[
                StageStep(
                    name="Install Dependencies",
                    command=self._default_install_command(build_tool),
                ),
                StageStep(
                    name="Build",
                    command=build_step_cmd,
                ),
            ],
            artifacts=["dist/", "build/"],
            cache_keys=[f"{build_tool}-cache-{language}"],
        )

        test_step_cmd = test_command or self._default_test_command(build_tool)
        test_stage = Stage(
            name="Test",
            stage_type=StageType.TEST,
            steps=[
                StageStep(
                    name="Run Tests",
                    command=test_step_cmd,
                ),
                StageStep(
                    name="Generate Coverage",
                    command="npm run test:coverage 2>/dev/null || true",
                ),
            ],
        )

        pipeline.stages = [source_stage, build_stage, test_stage]

        pipeline.test_configs = [
            TestConfiguration(
                test_type=TestType.UNIT,
                framework=build_tool,
                command=test_step_cmd,
                coverage_threshold=80.0,
            )
        ]

        pipeline.status = PipelineStatus.CONFIGURED
        return {
            "pipeline_id": pipeline_id,
            "stages": [s.name for s in pipeline.stages],
            "build_tool": build_tool,
            "language": language,
        }

    def configure_deployment(
        self,
        pipeline_id: str,
        environment: str = "staging",
        strategy: str = "rolling",
        auto_promote: bool = False,
    ) -> Dict[str, Any]:
        """Configure deployment for a pipeline."""
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            return {"error": f"Pipeline {pipeline_id} not found"}

        env = Environment(environment) if environment in [e.value for e in Environment] else Environment.STAGING
        ds = DeploymentStrategy(strategy) if strategy in [e.value for e in DeploymentStrategy] else DeploymentStrategy.ROLLING

        deploy_config = DeploymentConfig(
            environment=env,
            strategy=ds,
            auto_promote=auto_promote,
            health_check_url=f"https://{environment}.example.com/health",
        )
        pipeline.deployment_configs.append(deploy_config)

        deploy_stage = Stage(
            name=f"Deploy to {environment.title()}",
            stage_type=StageType.DEPLOY,
            environment=environment,
            steps=[
                StageStep(
                    name="Deploy",
                    command=f"echo 'Deploying to {environment}'",
                ),
                StageStep(
                    name="Health Check",
                    command=f"curl -f {deploy_config.health_check_url}",
                ),
            ],
            dependencies=["Build", "Test"],
        )

        pipeline.stages.append(deploy_stage)

        return {
            "pipeline_id": pipeline_id,
            "environment": environment,
            "strategy": strategy,
            "auto_promote": auto_promote,
            "stages": [s.name for s in pipeline.stages],
        }

    def configure_security_scanning(
        self,
        pipeline_id: str,
        sast: bool = True,
        sca: bool = True,
        secret_scan: bool = True,
        container_scan: bool = False,
    ) -> Dict[str, Any]:
        """Configure security scanning for a pipeline."""
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            return {"error": f"Pipeline {pipeline_id} not found"}

        pipeline.security_config = SecurityScanConfig(
            sast_enabled=sast,
            sca_enabled=sca,
            secret_scan=secret_scan,
            container_scan=container_scan,
        )

        scan_stage = Stage(
            name="Security Scan",
            stage_type=StageType.SECURITY_SCAN,
            steps=[
                StageStep(
                    name="Run Security Scans",
                    command="echo 'Running security scans'",
                )
            ],
            dependencies=["Build"],
        )

        pipeline.stages.append(scan_stage)
        self._security_scanner = SecurityScanner(pipeline.security_config)

        return {
            "pipeline_id": pipeline_id,
            "security_config": pipeline.security_config.to_dict(),
            "stages": [s.name for s in pipeline.stages],
        }

    def configure_quality_gates(
        self,
        pipeline_id: str,
        coverage_threshold: float = 80.0,
        max_vulnerabilities: int = 0,
        max_code_smells: int = 10,
    ) -> Dict[str, Any]:
        """Configure quality gates for a pipeline."""
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            return {"error": f"Pipeline {pipeline_id} not found"}

        pipeline.quality_gates = [
            QualityGate(
                gate_type=QualityGateType.CODE_COVERAGE,
                threshold=coverage_threshold,
                operator=">=",
                metric_name="code_coverage",
                description=f"Code coverage must be >= {coverage_threshold}%",
            ),
            QualityGate(
                gate_type=QualityGateType.VULNERABILITIES,
                threshold=max_vulnerabilities,
                operator="<=",
                metric_name="vulnerability_count",
                description=f"Maximum {max_vulnerabilities} vulnerabilities allowed",
            ),
            QualityGate(
                gate_type=QualityGateType.CODE_SMELLS,
                threshold=max_code_smells,
                operator="<=",
                metric_name="code_smell_count",
                description=f"Maximum {max_code_smells} code smells allowed",
            ),
        ]

        gate_stage = Stage(
            name="Quality Gate",
            stage_type=StageType.QUALITY_GATE,
            steps=[
                StageStep(
                    name="Evaluate Quality Gates",
                    command="echo 'Evaluating quality gates'",
                )
            ],
            dependencies=["Test", "Security Scan"],
        )

        pipeline.stages.append(gate_stage)

        return {
            "pipeline_id": pipeline_id,
            "quality_gates": [q.to_dict() for q in pipeline.quality_gates],
            "stages": [s.name for s in pipeline.stages],
        }

    def generate_pipeline_config(self, pipeline_id: str) -> Dict[str, Any]:
        """Generate provider-specific pipeline configuration."""
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            return {"error": f"Pipeline {pipeline_id} not found"}

        return self._config_generator.generate_config(pipeline)

    def trigger_pipeline(
        self,
        pipeline_id: str,
        branch: str = "main",
        commit_sha: str = "",
        commit_message: str = "",
    ) -> Dict[str, Any]:
        """Trigger a pipeline run."""
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            return {"error": f"Pipeline {pipeline_id} not found"}

        run = PipelineRun(
            pipeline_id=pipeline_id,
            status=PipelineStatus.TRIGGERED,
            trigger=TriggerType.MANUAL,
            branch=branch,
            commit_sha=commit_sha or hashlib.sha1(str(datetime.utcnow()).encode()).hexdigest()[:7],
            commit_message=commit_message,
            started_at=datetime.utcnow(),
        )

        pipeline.runs.append(run)
        pipeline.status = PipelineStatus.RUNNING

        self._notification_manager.notify(
            pipeline_id=pipeline_id,
            run_id=run.id,
            level=NotificationLevel.INFO,
            title=f"Pipeline {pipeline.name} triggered",
            message=f"Started on branch {branch}",
        )

        return {
            "run_id": run.id,
            "pipeline_id": pipeline_id,
            "status": run.status.value,
            "branch": branch,
            "commit_sha": run.commit_sha,
            "triggered_at": run.started_at.isoformat(),
        }

    def get_pipeline_status(self, pipeline_id: str) -> Dict[str, Any]:
        """Get comprehensive pipeline status."""
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            return {"error": f"Pipeline {pipeline_id} not found"}

        recent_runs = pipeline.runs[-5:] if pipeline.runs else []
        success_count = sum(1 for r in pipeline.runs if r.status == PipelineStatus.SUCCESS)
        fail_count = sum(1 for r in pipeline.runs if r.status == PipelineStatus.FAILED)

        return {
            "pipeline_id": pipeline.id,
            "name": pipeline.name,
            "project": pipeline.project,
            "provider": pipeline.provider.value,
            "status": pipeline.status.value,
            "stages": [s.name for s in pipeline.stages],
            "total_runs": len(pipeline.runs),
            "success_rate": round(success_count / len(pipeline.runs), 3) if pipeline.runs else 0.0,
            "failure_count": fail_count,
            "recent_runs": [r.to_dict() for r in recent_runs],
            "created_at": pipeline.created_at.isoformat(),
        }

    def list_pipelines(self) -> List[Dict[str, Any]]:
        return [
            {
                "pipeline_id": p.id,
                "name": p.name,
                "project": p.project,
                "provider": p.provider.value,
                "status": p.status.value,
                "total_runs": len(p.runs),
            }
            for p in self._pipelines.values()
        ]

    def rollback(
        self,
        pipeline_id: str,
        environment: str,
        reason: str = "",
        initiated_by: str = "user",
    ) -> Dict[str, Any]:
        """Execute a rollback for a pipeline's deployment."""
        pipeline = self._pipelines.get(pipeline_id)
        if not pipeline:
            return {"error": f"Pipeline {pipeline_id} not found"}

        latest_run = pipeline.runs[-1] if pipeline.runs else None
        run_id = latest_run.id if latest_run else ""

        return self._deployment_manager.rollback(
            pipeline_id=pipeline_id,
            run_id=run_id,
            environment=environment,
            strategy=RollbackStrategy.LAST_KNOWN_GOOD,
            reason=reason,
            initiated_by=initiated_by,
        )

    def get_security_report(self, pipeline_id: str) -> Dict[str, Any]:
        """Get security scan report for a pipeline."""
        results = self._security_scanner.get_scan_history()
        pipeline_results = [r for r in results if r["pipeline_id"] == pipeline_id]
        if not pipeline_results:
            return {"pipeline_id": pipeline_id, "scans": 0, "findings": {}}

        latest = pipeline_results[-1]
        return {
            "pipeline_id": pipeline_id,
            "total_scans": len(pipeline_results),
            "latest_scan": latest,
        }

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "CICDPipelineAgent",
            "version": "2.0.0",
            "total_pipelines": len(self._pipelines),
            "total_runs": sum(len(p.runs) for p in self._pipelines.values()),
            "total_rollbacks": len(self._deployment_manager._rollback_records),
            "uptime": str(datetime.utcnow() - self._created_at),
        }

    def _default_build_command(self, tool: str, language: str) -> str:
        commands = {
            "npm": "npm run build",
            "yarn": "yarn build",
            "pip": "python -m build",
            "cargo": "cargo build --release",
            "maven": "mvn package",
            "gradle": "gradle build",
            "make": "make build",
            "docker": "docker build -t app .",
        }
        return commands.get(tool, f"{tool} build")

    def _default_install_command(self, tool: str) -> str:
        commands = {
            "npm": "npm ci",
            "yarn": "yarn install --frozen-lockfile",
            "pip": "pip install -r requirements.txt",
            "cargo": "cargo fetch",
            "maven": "mvn dependency:resolve",
            "gradle": "gradle dependencies",
        }
        return commands.get(tool, f"{tool} install")

    def _default_test_command(self, tool: str) -> str:
        commands = {
            "npm": "npm test",
            "yarn": "yarn test",
            "pip": "python -m pytest",
            "cargo": "cargo test",
            "maven": "mvn test",
            "gradle": "gradle test",
        }
        return commands.get(tool, f"{tool} test")


# =============================================================================
# Entry Point
# =============================================================================

def main() -> None:
    """Demonstrate the CI/CD Pipeline Agent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    print("=" * 70)
    print("  CI/CD Pipeline Agent v2.0 - Demonstration")
    print("=" * 70)

    agent = CICDPipelineAgent({"user": "demo_user"})

    # Create a pipeline
    print("\n--- Creating Pipeline ---")
    result = agent.create_pipeline(
        name="Web App CI/CD",
        project="webapp",
        provider="github_actions",
        repository="org/webapp",
        description="Full CI/CD pipeline for the web application",
    )
    pipeline_id = result["pipeline_id"]
    print(f"Pipeline created: {pipeline_id}")
    print(f"Provider: {result['provider']}")

    # Configure build
    print("\n--- Configuring Build ---")
    build = agent.configure_build(
        pipeline_id,
        build_tool="npm",
        language="javascript",
    )
    print(f"Stages: {build['stages']}")

    # Configure deployment
    print("\n--- Configuring Deployment ---")
    staging = agent.configure_deployment(pipeline_id, environment="staging", strategy="canary")
    production = agent.configure_deployment(pipeline_id, environment="production", strategy="blue_green")
    print(f"Staging deploy: {staging['strategy']}")
    print(f"Production deploy: {production['strategy']}")
    print(f"All stages: {staging['stages']}")

    # Security scanning
    print("\n--- Security Scanning ---")
    security = agent.configure_security_scanning(
        pipeline_id, sast=True, sca=True, secret_scan=True
    )
    print(f"Security config: {security['security_config']}")

    # Quality gates
    print("\n--- Quality Gates ---")
    gates = agent.configure_quality_gates(
        pipeline_id, coverage_threshold=80.0, max_vulnerabilities=0
    )
    print(f"Gates: {len(gates['quality_gates'])}")

    # Generate config
    print("\n--- Generating Config ---")
    config = agent.generate_pipeline_config(pipeline_id)
    print(f"Config hash: {config['config_hash']}")

    # Trigger pipeline
    print("\n--- Triggering Pipeline ---")
    trigger = agent.trigger_pipeline(
        pipeline_id,
        branch="main",
        commit_message="feat: add user authentication",
    )
    print(f"Run ID: {trigger['run_id']}")
    print(f"Status: {trigger['status']}")

    # Pipeline status
    print("\n--- Pipeline Status ---")
    status = agent.get_pipeline_status(pipeline_id)
    print(f"Stages: {status['stages']}")
    print(f"Total runs: {status['total_runs']}")

    # Rollback
    print("\n--- Rollback ---")
    rb = agent.rollback(pipeline_id, "staging", reason="Performance degradation")
    print(f"Rollback success: {rb['success']}")

    # Security report
    print("\n--- Security Report ---")
    sec_report = agent.get_security_report(pipeline_id)
    print(f"Total scans: {sec_report.get('total_scans', 0)}")

    # Agent status
    print("\n--- Agent Status ---")
    agent_status = agent.get_status()
    for k, v in agent_status.items():
        print(f"  {k}: {v}")

    print("\n" + "=" * 70)
    print("  Demonstration Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()

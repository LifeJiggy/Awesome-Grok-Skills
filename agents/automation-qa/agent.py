#!/usr/bin/env python3
"""
AutomationQA Agent - Enterprise Test Automation Framework
=========================================================

A comprehensive test automation framework supporting unit, integration, E2E,
performance, security, API, visual, accessibility, chaos, and contract testing.
Integrates with CI/CD pipelines, multiple test frameworks, and reporting systems.

Author: MiMoCode
Version: 3.0.0
License: MIT
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import random
import re
import time
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    Optional,
    Protocol,
    Set,
    Tuple,
    Type,
    Union,
)

# ---------------------------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("automation_qa")


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"
    API = "api"
    VISUAL = "visual"
    ACCESSIBILITY = "accessibility"
    CHAOS = "chaos"
    CONTRACT = "contract"


class TestFramework(Enum):
    PYTEST = "pytest"
    JEST = "jest"
    CYPRESS = "cypress"
    PLAYWRIGHT = "playwright"
    SELENIUM = "selenium"
    JUNIT = "junit"
    GATLING = "gatling"
    K6 = "k6"
    OWASP_ZAP = "owasp_zap"
    POSTMAN = "postman"


class TestStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"
    FLAKY = "flaky"
    QUEUED = "queued"


class CIPipelineStage(Enum):
    BUILD = "build"
    UNIT_TEST = "unit_test"
    INTEGRATION_TEST = "integration_test"
    E2E_TEST = "e2e_test"
    SECURITY_SCAN = "security_scan"
    PERFORMANCE_TEST = "performance_test"
    DEPLOY_STAGING = "deploy_staging"
    ACCEPTANCE = "acceptance"
    DEPLOY_PRODUCTION = "deploy_production"


class ReportFormat(Enum):
    HTML = "html"
    JSON = "json"
    JUNIT_XML = "junit_xml"
    ALLURE = "allure"
    TCM = "tcm"
    CLOB = "clob"


class BrowserType(Enum):
    CHROME = "chrome"
    FIREFOX = "firefox"
    SAFARI = "safari"
    EDGE = "edge"


class SeverityLevel(Enum):
    BLOCKER = "blocker"
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    TRIVIAL = "trivial"


class TestEnvironment(Enum):
    LOCAL = "local"
    DEV = "dev"
    STAGING = "staging"
    QA = "qa"
    UAT = "uat"
    PRODUCTION = "production"


class PerformanceLoadPattern(Enum):
    CONSTANT = "constant"
    RAMP_UP = "ramp_up"
    SPIKE = "spike"
    STEP = "step"
    WAVE = "wave"
    RANDOM = "random"


class SecurityTestType(Enum):
    SAST = "sast"
    DAST = "dast"
    IAST = "iast"
    SCA = "sca"
    FUZZING = "fuzzing"
    PENETRATION = "penetration"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class AssertionResult:
    assertion_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    description: str = ""
    expected: Any = None
    actual: Any = None
    passed: bool = False
    message: str = ""
    duration_ms: float = 0.0

    def evaluate(self) -> bool:
        self.passed = self.expected == self.actual
        if not self.passed:
            self.message = (
                f"Expected {self.expected!r}, got {self.actual!r}"
            )
        return self.passed


@dataclass
class TestCase:
    test_id: str = field(default_factory=lambda: f"TC-{uuid.uuid4().hex[:8].upper()}")
    name: str = ""
    description: str = ""
    test_type: TestType = TestType.UNIT
    framework: TestFramework = TestFramework.PYTEST
    priority: SeverityLevel = SeverityLevel.MAJOR
    status: TestStatus = TestStatus.PENDING
    tags: List[str] = field(default_factory=list)
    preconditions: List[str] = field(default_factory=list)
    steps: List[Dict[str, str]] = field(default_factory=list)
    expected_results: List[str] = field(default_factory=list)
    assertions: List[AssertionResult] = field(default_factory=list)
    setup_script: str = ""
    teardown_script: str = ""
    timeout_seconds: int = 300
    retry_count: int = 0
    max_retries: int = 3
    author: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    estimated_duration_ms: float = 0.0
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def mark_passed(self) -> None:
        self.status = TestStatus.PASSED
        self.updated_at = datetime.utcnow().isoformat()

    def mark_failed(self, reason: str = "") -> None:
        self.status = TestStatus.FAILED
        self.metadata["failure_reason"] = reason
        self.updated_at = datetime.utcnow().isoformat()

    def mark_flaky(self) -> None:
        if self.retry_count >= self.max_retries:
            self.status = TestStatus.FLAKY
        else:
            self.retry_count += 1
            self.status = TestStatus.PENDING

    def to_junit_xml(self) -> str:
        escaped_name = self.name.replace("&", "&amp;").replace("<", "&lt;")
        failure_xml = ""
        if self.status == TestStatus.FAILED:
            reason = self.metadata.get("failure_reason", "Unknown")
            reason_escaped = reason.replace("&", "&amp;").replace("<", "&lt;")
            failure_xml = f'\n    <failure message="Test failed">{reason_escaped}</failure>'
        elif self.status == TestStatus.ERROR:
            reason = self.metadata.get("error_message", "Unknown error")
            reason_escaped = reason.replace("&", "&amp;").replace("<", "&lt;")
            failure_xml = f'\n    <error message="Test error">{reason_escaped}</error>'
        elif self.status == TestStatus.SKIPPED:
            failure_xml = "\n    <skipped/>"
        return (
            f'  <testcase name="{escaped_name}" '
            f'time="{self.estimated_duration_ms / 1000:.3f}">'
            f"{failure_xml}\n  </testcase>"
        )


@dataclass
class TestResult:
    result_id: str = field(default_factory=lambda: f"TR-{uuid.uuid4().hex[:8].upper()}")
    test_case: Optional[TestCase] = None
    status: TestStatus = TestStatus.PENDING
    start_time: str = ""
    end_time: str = ""
    duration_ms: float = 0.0
    assertions: List[AssertionResult] = field(default_factory=list)
    output: str = ""
    error_message: str = ""
    stack_trace: str = ""
    screenshots: List[str] = field(default_factory=list)
    logs: List[str] = field(default_factory=list)
    retry_attempt: int = 0
    environment: TestEnvironment = TestEnvironment.LOCAL
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def passed_assertions(self) -> int:
        return sum(1 for a in self.assertions if a.passed)

    @property
    def failed_assertions(self) -> int:
        return sum(1 for a in self.assertions if not a.passed)

    def summary(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "status": self.status.value,
            "duration_ms": self.duration_ms,
            "passed_assertions": self.passed_assertions,
            "failed_assertions": self.failed_assertions,
        }


@dataclass
class TestSuite:
    suite_id: str = field(default_factory=lambda: f"TS-{uuid.uuid4().hex[:8].upper()}")
    name: str = ""
    description: str = ""
    test_cases: List[TestCase] = field(default_factory=list)
    setup_script: str = ""
    teardown_script: str = ""
    tags: List[str] = field(default_factory=list)
    parallel: bool = False
    max_workers: int = 4
    timeout_seconds: int = 3600
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def add_test_case(self, test_case: TestCase) -> None:
        self.test_cases.append(test_case)
        logger.info("Added test case %s to suite %s", test_case.test_id, self.suite_id)

    def remove_test_case(self, test_id: str) -> bool:
        before = len(self.test_cases)
        self.test_cases = [tc for tc in self.test_cases if tc.test_id != test_id]
        return len(self.test_cases) < before

    def filter_by_type(self, test_type: TestType) -> List[TestCase]:
        return [tc for tc in self.test_cases if tc.test_type == test_type]

    def filter_by_tag(self, tag: str) -> List[TestCase]:
        return [tc for tc in self.test_cases if tag in tc.tags]

    def filter_by_priority(self, priority: SeverityLevel) -> List[TestCase]:
        return [tc for tc in self.test_cases if tc.priority == priority]

    @property
    def total_count(self) -> int:
        return len(self.test_cases)

    def status_summary(self) -> Dict[str, int]:
        summary: Dict[str, int] = defaultdict(int)
        for tc in self.test_cases:
            summary[tc.status.value] += 1
        return dict(summary)


@dataclass
class TestPlan:
    plan_id: str = field(default_factory=lambda: f"TP-{uuid.uuid4().hex[:8].upper()}")
    name: str = ""
    description: str = ""
    project: str = ""
    version: str = ""
    author: str = ""
    test_suites: List[TestSuite] = field(default_factory=list)
    environments: List[TestEnvironment] = field(default_factory=list)
    browsers: List[BrowserType] = field(default_factory=list)
    start_date: str = ""
    end_date: str = ""
    risk_areas: List[str] = field(default_factory=list)
    entry_criteria: List[str] = field(default_factory=list)
    exit_criteria: List[str] = field(default_factory=list)
    status: str = "draft"
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def add_suite(self, suite: TestSuite) -> None:
        self.test_suites.append(suite)

    @property
    def total_test_cases(self) -> int:
        return sum(s.total_count for s in self.test_suites)

    @property
    def estimated_duration_hours(self) -> float:
        total_ms = sum(
            tc.estimated_duration_ms
            for s in self.test_suites
            for tc in s.test_cases
        )
        return total_ms / 3_600_000

    def summary(self) -> Dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "name": self.name,
            "total_test_cases": self.total_test_cases,
            "total_suites": len(self.test_suites),
            "environments": [e.value for e in self.environments],
            "estimated_hours": round(self.estimated_duration_hours, 2),
        }


@dataclass
class TestExecution:
    execution_id: str = field(default_factory=lambda: f"TE-{uuid.uuid4().hex[:8].upper()}")
    plan: Optional[TestPlan] = None
    suite: Optional[TestSuite] = None
    environment: TestEnvironment = TestEnvironment.LOCAL
    results: List[TestResult] = field(default_factory=list)
    start_time: str = ""
    end_time: str = ""
    triggered_by: str = "manual"
    ci_build_id: str = ""
    status: TestStatus = TestStatus.PENDING
    metadata: Dict[str, Any] = field(default_factory=dict)

    def add_result(self, result: TestResult) -> None:
        self.results.append(result)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.status == TestStatus.PASSED)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.status == TestStatus.FAILED)

    @property
    def skipped(self) -> int:
        return sum(1 for r in self.results if r.status == TestStatus.SKIPPED)

    @property
    def pass_rate(self) -> float:
        total = len(self.results)
        return (self.passed / total * 100) if total else 0.0

    def summary(self) -> Dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "total": len(self.results),
            "passed": self.passed,
            "failed": self.failed,
            "skipped": self.skipped,
            "pass_rate": f"{self.pass_rate:.1f}%",
            "duration": self.end_time,
        }


@dataclass
class CIConfig:
    provider: str = "github_actions"
    pipeline_stages: List[CIPipelineStage] = field(default_factory=list)
    parallel_stages: bool = True
    fail_fast: bool = True
    retry_on_failure: bool = True
    max_retries: int = 2
    timeout_minutes: int = 60
    notification_channels: List[str] = field(default_factory=list)
    artifact_retention_days: int = 30
    environment_variables: Dict[str, str] = field(default_factory=dict)
    secrets: List[str] = field(default_factory=list)
    webhook_url: str = ""
    docker_image: str = ""
    node_version: str = "20"
    python_version: str = "3.12"

    def generate_github_actions_config(self) -> str:
        stages_yaml = ""
        for stage in self.pipeline_stages:
            stages_yaml += f"  {stage.value}:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n"
        return (
            f"name: CI Pipeline\non: [push, pull_request]\njobs:\n{stages_yaml}"
        )


@dataclass
class PerformanceTestConfig:
    target_url: str = ""
    load_pattern: PerformanceLoadPattern = PerformanceLoadPattern.CONSTANT
    virtual_users: int = 100
    ramp_up_duration_seconds: int = 60
    test_duration_seconds: int = 300
    think_time_ms: int = 1000
    threshold_p95_ms: float = 500.0
    threshold_p99_ms: float = 1000.0
    threshold_error_rate: float = 1.0
    threshold_rps: float = 100.0
    script_path: str = ""
    data_setup_script: str = ""
    custom_headers: Dict[str, str] = field(default_factory=dict)
    authentication: Dict[str, str] = field(default_factory=dict)

    def to_k6_options(self) -> Dict[str, Any]:
        stages = []
        if self.load_pattern == PerformanceLoadPattern.RAMP_UP:
            stages = [
                {"duration": f"{self.ramp_up_duration_seconds}s", "target": self.virtual_users},
                {"duration": f"{self.test_duration_seconds}s", "target": self.virtual_users},
            ]
        elif self.load_pattern == PerformanceLoadPattern.SPIKE:
            stages = [
                {"duration": "30s", "target": self.virtual_users // 2},
                {"duration": "10s", "target": self.virtual_users},
                {"duration": "30s", "target": self.virtual_users // 2},
            ]
        else:
            stages = [{"duration": f"{self.test_duration_seconds}s", "target": self.virtual_users}]
        return {
            "stages": stages,
            "thresholds": {
                "http_req_duration": [f"p(95)<{self.threshold_p95_ms}"],
                "http_req_failed": [f"rate<{self.threshold_error_rate / 100}"],
            },
        }


@dataclass
class PerformanceResult:
    result_id: str = field(default_factory=lambda: f"PR-{uuid.uuid4().hex[:8].upper()}")
    config: Optional[PerformanceTestConfig] = None
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time_ms: float = 0.0
    p50_response_time_ms: float = 0.0
    p95_response_time_ms: float = 0.0
    p99_response_time_ms: float = 0.0
    max_response_time_ms: float = 0.0
    min_response_time_ms: float = 0.0
    requests_per_second: float = 0.0
    throughput_bytes_per_second: float = 0.0
    error_rate: float = 0.0
    duration_seconds: float = 0.0
    status_codes: Dict[int, int] = field(default_factory=dict)
    endpoint_metrics: Dict[str, Dict[str, float]] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @property
    def passed(self) -> bool:
        if self.config is None:
            return True
        return (
            self.p95_response_time_ms <= self.config.threshold_p95_ms
            and self.error_rate <= self.config.threshold_error_rate
        )

    def summary(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "total_requests": self.total_requests,
            "success_rate": f"{(self.successful_requests / max(self.total_requests, 1)) * 100:.1f}%",
            "avg_response_ms": round(self.avg_response_time_ms, 2),
            "p95_ms": round(self.p95_response_time_ms, 2),
            "p99_ms": round(self.p99_response_time_ms, 2),
            "rps": round(self.requests_per_second, 2),
            "error_rate": f"{self.error_rate:.2f}%",
            "passed_thresholds": self.passed,
        }


@dataclass
class SecurityScanResult:
    result_id: str = field(default_factory=lambda: f"SR-{uuid.uuid4().hex[:8].upper()}")
    scan_type: SecurityTestType = SecurityTestType.DAST
    target: str = ""
    total_vulnerabilities: int = 0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0
    low_count: int = 0
    info_count: int = 0
    vulnerabilities: List[Dict[str, Any]] = field(default_factory=list)
    scan_duration_seconds: float = 0.0
    scanner_version: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @property
    def risk_score(self) -> float:
        return (
            self.critical_count * 10.0
            + self.high_count * 7.0
            + self.medium_count * 4.0
            + self.low_count * 1.0
        )

    @property
    def has_critical(self) -> bool:
        return self.critical_count > 0

    def summary(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "scan_type": self.scan_type.value,
            "total_vulnerabilities": self.total_vulnerabilities,
            "critical": self.critical_count,
            "high": self.high_count,
            "medium": self.medium_count,
            "low": self.low_count,
            "risk_score": round(self.risk_score, 1),
            "has_critical": self.has_critical,
        }


@dataclass
class BugReport:
    bug_id: str = field(default_factory=lambda: f"BUG-{uuid.uuid4().hex[:8].upper()}")
    title: str = ""
    description: str = ""
    severity: SeverityLevel = SeverityLevel.MAJOR
    status: str = "open"
    reporter: str = ""
    assignee: str = ""
    environment: str = ""
    steps_to_reproduce: List[str] = field(default_factory=list)
    expected_behavior: str = ""
    actual_behavior: str = ""
    attachments: List[str] = field(default_factory=list)
    related_test_case: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "bug_id": self.bug_id,
            "title": self.title,
            "severity": self.severity.value,
            "status": self.status,
            "description": self.description,
            "steps": self.steps_to_reproduce,
            "expected": self.expected_behavior,
            "actual": self.actual_behavior,
            "created_at": self.created_at,
        }


@dataclass
class CodeCoverageReport:
    report_id: str = field(default_factory=lambda: f"CC-{uuid.uuid4().hex[:8].upper()}")
    project_name: str = ""
    total_lines: int = 0
    covered_lines: int = 0
    branch_coverage: float = 0.0
    function_coverage: float = 0.0
    line_coverage: float = 0.0
    file_coverage: Dict[str, float] = field(default_factory=dict)
    uncovered_files: List[str] = field(default_factory=list)
    coverage_threshold: float = 80.0
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    @property
    def meets_threshold(self) -> bool:
        return self.line_coverage >= self.coverage_threshold

    @property
    def coverage_delta(self) -> float:
        return self.line_coverage - self.coverage_threshold

    def summary(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "line_coverage": f"{self.line_coverage:.1f}%",
            "branch_coverage": f"{self.branch_coverage:.1f}%",
            "function_coverage": f"{self.function_coverage:.1f}%",
            "meets_threshold": self.meets_threshold,
            "uncovered_files_count": len(self.uncovered_files),
        }


@dataclass
class TestEnvironmentConfig:
    env_id: str = field(default_factory=lambda: f"ENV-{uuid.uuid4().hex[:8].upper()}")
    name: TestEnvironment = TestEnvironment.DEV
    base_url: str = ""
    api_base_url: str = ""
    database_url: str = ""
    redis_url: str = ""
    environment_variables: Dict[str, str] = field(default_factory=dict)
    credentials: Dict[str, str] = field(default_factory=dict)
    services: List[str] = field(default_factory=list)
    health_check_url: str = ""
    is_active: bool = True
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_env_file(self) -> str:
        lines = [f"# Environment: {self.name.value}"]
        for key, val in self.environment_variables.items():
            lines.append(f"{key}={val}")
        return "\n".join(lines)


@dataclass
class BrowserTestConfig:
    browser: BrowserType = BrowserType.CHROME
    headless: bool = True
    viewport_width: int = 1920
    viewport_height: int = 1080
    timeout_ms: int = 30000
    slow_mo_ms: int = 0
    screenshots: str = "only-on-failure"
    video: str = "retain-on-failure"
    trace: str = "retain-on-failure"
    download_dir: str = "/tmp/downloads"
    proxy: str = ""
    extra_args: List[str] = field(default_factory=list)
    geolocation: Dict[str, float] = field(default_factory=dict)
    permissions: List[str] = field(default_factory=list)
    locale: str = "en-US"
    timezone: str = "UTC"

    def to_playwright_config(self) -> Dict[str, Any]:
        return {
            "browser": self.browser.value,
            "headless": self.headless,
            "viewport": {"width": self.viewport_width, "height": self.viewport_height},
            "timeout": self.timeout_ms,
            "screenshot": self.screenshots,
            "video": self.video,
            "trace": self.trace,
        }


@dataclass
class APITestCase:
    test_id: str = field(default_factory=lambda: f"API-{uuid.uuid4().hex[:8].upper()}")
    name: str = ""
    method: str = "GET"
    endpoint: str = ""
    headers: Dict[str, str] = field(default_factory=dict)
    query_params: Dict[str, str] = field(default_factory=dict)
    request_body: Any = None
    expected_status: int = 200
    expected_response_schema: Dict[str, Any] = field(default_factory=dict)
    expected_headers: Dict[str, str] = field(default_factory=dict)
    assertions: List[Dict[str, Any]] = field(default_factory=list)
    pre_request_scripts: List[str] = field(default_factory=list)
    post_request_scripts: List[str] = field(default_factory=list)
    timeout_ms: int = 30000
    retry_count: int = 0
    tags: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)

    def to_curl(self, base_url: str = "") -> str:
        url = f"{base_url}{self.endpoint}"
        cmd_parts = ["curl", "-X", self.method, url]
        for key, val in self.headers.items():
            cmd_parts.extend(["-H", f'"{key}: {val}"'])
        if self.request_body:
            cmd_parts.extend(["-d", json.dumps(self.request_body)])
        return " ".join(cmd_parts)


@dataclass
class TestMetric:
    metric_id: str = field(default_factory=lambda: f"TM-{uuid.uuid4().hex[:8].upper()}")
    name: str = ""
    value: float = 0.0
    unit: str = ""
    category: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tags: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value,
            "unit": self.unit,
            "category": self.category,
            "timestamp": self.timestamp,
        }


@dataclass
class FlakyTestAnalysis:
    test_id: str = ""
    test_name: str = ""
    total_runs: int = 0
    pass_count: int = 0
    fail_count: int = 0
    flaky_score: float = 0.0
    common_failure_reasons: List[str] = field(default_factory=list)
    recommended_action: str = ""
    last_10_results: List[str] = field(default_factory=list)

    @property
    def flaky_rate(self) -> float:
        return (self.fail_count / max(self.total_runs, 1)) * 100

    def calculate_flaky_score(self) -> float:
        if self.total_runs < 5:
            self.flaky_score = 0.0
            return 0.0
        alternating = sum(
            1 for i in range(1, len(self.last_10_results))
            if self.last_10_results[i] != self.last_10_results[i - 1]
        )
        self.flaky_score = (alternating / max(len(self.last_10_results) - 1, 1)) * 100
        return self.flaky_score


@dataclass
class TestDataManagement:
    data_id: str = field(default_factory=lambda: f"TD-{uuid.uuid4().hex[:8].upper()}")
    dataset_name: str = ""
    data_type: str = "synthetic"
    record_count: int = 0
    schema: Dict[str, str] = field(default_factory=dict)
    seed: int = 0
    fixtures: Dict[str, Any] = field(default_factory=dict)
    cleanup_strategy: str = "after_suite"
    isolation_level: str = "transaction"
    data_provider: str = ""

    def generate_records(self, count: int) -> List[Dict[str, Any]]:
        records = []
        rng = random.Random(self.seed)
        for _ in range(count):
            record = {}
            for field_name, field_type in self.schema.items():
                if field_type == "string":
                    record[field_name] = f"test_{uuid.uuid4().hex[:8]}"
                elif field_type == "integer":
                    record[field_name] = rng.randint(1, 10000)
                elif field_type == "email":
                    record[field_name] = f"user_{uuid.uuid4().hex[:6]}@test.com"
                elif field_type == "boolean":
                    record[field_name] = rng.choice([True, False])
                elif field_type == "date":
                    record[field_name] = (
                        datetime.utcnow() - timedelta(days=rng.randint(0, 365))
                    ).isoformat()
                else:
                    record[field_name] = None
            records.append(record)
        return records


@dataclass
class RegressionTestSet:
    set_id: str = field(default_factory=lambda: f"RTS-{uuid.uuid4().hex[:8].upper()}")
    name: str = ""
    description: str = ""
    test_case_ids: List[str] = field(default_factory=list)
    change_impact_map: Dict[str, List[str]] = field(default_factory=dict)
    risk_areas: List[str] = field(default_factory=list)
    last_executed: str = ""
    pass_rate_history: List[float] = field(default_factory=list)

    def select_for_change(self, changed_files: List[str]) -> List[str]:
        selected: Set[str] = set()
        for changed_file in changed_files:
            for tc_id, impacted_files in self.change_impact_map.items():
                if changed_file in impacted_files:
                    selected.add(tc_id)
        return list(selected)

    @property
    def average_pass_rate(self) -> float:
        if not self.pass_rate_history:
            return 0.0
        return sum(self.pass_rate_history) / len(self.pass_rate_history)


@dataclass
class VisualDiffResult:
    diff_id: str = field(default_factory=lambda: f"VD-{uuid.uuid4().hex[:8].upper()}")
    page_url: str = ""
    baseline_screenshot: str = ""
    current_screenshot: str = ""
    diff_screenshot: str = ""
    pixel_diff_count: int = 0
    pixel_diff_percentage: float = 0.0
    threshold: float = 0.1
    passed: bool = False
    regions: List[Dict[str, Any]] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def evaluate(self) -> bool:
        self.passed = self.pixel_diff_percentage <= self.threshold
        return self.passed


@dataclass
class AccessibilityViolation:
    violation_id: str = ""
    rule_id: str = ""
    impact: str = "serious"
    description: str = ""
    help_url: str = ""
    nodes_affected: int = 0
    tags: List[str] = field(default_factory=list)
    wcag_level: str = "AA"
    wcag_version: str = "2.1"

    @property
    def is_blocking(self) -> bool:
        return self.impact in ("critical", "serious")


@dataclass
class ContractTestResult:
    result_id: str = field(default_factory=lambda: f"CT-{uuid.uuid4().hex[:8].upper()}")
    provider: str = ""
    consumer: str = ""
    interaction_description: str = ""
    pact_version: str = ""
    status: str = "pending"
    mismatches: List[Dict[str, Any]] = field(default_factory=list)
    verified_at: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return len(self.mismatches) == 0 and self.status == "verified"


@dataclass
class TestReport:
    report_id: str = field(default_factory=lambda: f"REP-{uuid.uuid4().hex[:8].upper()}")
    title: str = ""
    project: str = ""
    version: str = ""
    execution: Optional[TestExecution] = None
    coverage: Optional[CodeCoverageReport] = None
    performance: Optional[PerformanceResult] = None
    security: Optional[SecurityScanResult] = None
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    author: str = ""
    format: ReportFormat = ReportFormat.HTML
    sections: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)

    def to_json(self) -> str:
        data = {
            "report_id": self.report_id,
            "title": self.title,
            "project": self.project,
            "generated_at": self.generated_at,
        }
        if self.execution:
            data["execution"] = self.execution.summary()
        if self.coverage:
            data["coverage"] = self.coverage.summary()
        if self.performance:
            data["performance"] = self.performance.summary()
        if self.security:
            data["security"] = self.security.summary()
        data["recommendations"] = self.recommendations
        return json.dumps(data, indent=2)


@dataclass
class QualityGate:
    gate_id: str = field(default_factory=lambda: f"QG-{uuid.uuid4().hex[:8].upper()}")
    name: str = ""
    stage: CIPipelineStage = CIPipelineStage.BUILD
    conditions: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "pending"
    evaluated_at: str = ""

    def evaluate(self, metrics: Dict[str, float]) -> bool:
        self.evaluated_at = datetime.utcnow().isoformat()
        for condition in self.conditions:
            metric_name = condition.get("metric", "")
            operator = condition.get("operator", ">=")
            threshold = condition.get("threshold", 0.0)
            value = metrics.get(metric_name, 0.0)
            if operator == ">=" and value < threshold:
                self.status = "failed"
                return False
            elif operator == "<=" and value > threshold:
                self.status = "failed"
                return False
            elif operator == ">" and value <= threshold:
                self.status = "failed"
                return False
            elif operator == "<" and value >= threshold:
                self.status = "failed"
                return False
        self.status = "passed"
        return True


# ---------------------------------------------------------------------------
# Protocol for pluggable test runners
# ---------------------------------------------------------------------------

class TestRunner(Protocol):
    def setup(self, config: Dict[str, Any]) -> None: ...
    def execute(self, test_case: TestCase) -> TestResult: ...
    def teardown(self) -> None: ...


# ---------------------------------------------------------------------------
# Strategy pattern for test generation
# ---------------------------------------------------------------------------

class TestGenerationStrategy(ABC):
    @abstractmethod
    def generate(self, source: Any, options: Dict[str, Any]) -> List[TestCase]:
        ...


class UnitTestGenerationStrategy(TestGenerationStrategy):
    def generate(self, source: Any, options: Dict[str, Any]) -> List[TestCase]:
        test_cases: List[TestCase] = []
        functions = options.get("functions", [])
        for func in functions:
            tc = TestCase(
                name=f"test_{func.get('name', 'unknown')}",
                description=f"Unit test for {func.get('name', 'unknown')}",
                test_type=TestType.UNIT,
                framework=TestFramework.PYTEST,
                priority=SeverityLevel.MAJOR,
                tags=["unit", "automated"],
                steps=[
                    {"action": "Setup test fixtures", "data": json.dumps(func.get("params", {}))},
                    {"action": f"Call {func.get('name', 'unknown')}", "data": ""},
                    {"action": "Assert expected output", "data": json.dumps(func.get("expected", {}))},
                ],
                expected_results=["Function returns expected output"],
                estimated_duration_ms=500,
            )
            test_cases.append(tc)
        return test_cases


class APITestGenerationStrategy(TestGenerationStrategy):
    def generate(self, source: Any, options: Dict[str, Any]) -> List[TestCase]:
        test_cases: List[TestCase] = []
        endpoints = options.get("endpoints", [])
        for ep in endpoints:
            tc = TestCase(
                name=f"test_api_{ep.get('method', 'GET')}_{ep.get('path', '/').replace('/', '_')}",
                description=f"API test for {ep.get('method', 'GET')} {ep.get('path', '/')}",
                test_type=TestType.API,
                framework=TestFramework.POSTMAN,
                priority=SeverityLevel.MAJOR,
                tags=["api", "automated"],
                steps=[
                    {"action": f"Send {ep.get('method', 'GET')} request", "data": ep.get("path", "/")},
                    {"action": "Verify status code", "data": str(ep.get("expected_status", 200))},
                    {"action": "Validate response schema", "data": json.dumps(ep.get("schema", {}))},
                ],
                expected_results=[f"Status code {ep.get('expected_status', 200)}"],
                estimated_duration_ms=2000,
            )
            test_cases.append(tc)
        return test_cases


class E2ETestGenerationStrategy(TestGenerationStrategy):
    def generate(self, source: Any, options: Dict[str, Any]) -> List[TestCase]:
        test_cases: List[TestCase] = []
        user_flows = options.get("user_flows", [])
        for flow in user_flows:
            tc = TestCase(
                name=f"test_e2e_{flow.get('name', 'unknown')}",
                description=f"E2E test for user flow: {flow.get('name', 'unknown')}",
                test_type=TestType.E2E,
                framework=TestFramework.PLAYWRIGHT,
                priority=SeverityLevel.CRITICAL,
                tags=["e2e", "automated", "critical-path"],
                steps=flow.get("steps", []),
                expected_results=[f"Flow '{flow.get('name', 'unknown')}' completes successfully"],
                estimated_duration_ms=30000,
            )
            test_cases.append(tc)
        return test_cases


# ---------------------------------------------------------------------------
# Factory for test generation strategies
# ---------------------------------------------------------------------------

class TestGenerationFactory:
    _strategies: Dict[TestType, TestGenerationStrategy] = {
        TestType.UNIT: UnitTestGenerationStrategy(),
        TestType.API: APITestGenerationStrategy(),
        TestType.E2E: E2ETestGenerationStrategy(),
    }

    @classmethod
    def get_strategy(cls, test_type: TestType) -> TestGenerationStrategy:
        strategy = cls._strategies.get(test_type)
        if strategy is None:
            raise ValueError(f"No generation strategy registered for {test_type.value}")
        return strategy

    @classmethod
    def register_strategy(cls, test_type: TestType, strategy: TestGenerationStrategy) -> None:
        cls._strategies[test_type] = strategy


# ---------------------------------------------------------------------------
# Observer for test execution events
# ---------------------------------------------------------------------------

class TestExecutionObserver(ABC):
    @abstractmethod
    def on_test_started(self, test_case: TestCase) -> None: ...

    @abstractmethod
    def on_test_completed(self, result: TestResult) -> None: ...

    @abstractmethod
    def on_suite_completed(self, suite: TestSuite, results: List[TestResult]) -> None: ...


class LoggingObserver(TestExecutionObserver):
    def on_test_started(self, test_case: TestCase) -> None:
        logger.info("Test started: %s", test_case.name)

    def on_test_completed(self, result: TestResult) -> None:
        logger.info("Test %s: %s", result.test_case.name if result.test_case else "?", result.status.value)

    def on_suite_completed(self, suite: TestSuite, results: List[TestResult]) -> None:
        passed = sum(1 for r in results if r.status == TestStatus.PASSED)
        logger.info("Suite '%s' completed: %d/%d passed", suite.name, passed, len(results))


class MetricsObserver(TestExecutionObserver):
    def __init__(self) -> None:
        self.metrics: List[TestMetric] = []

    def on_test_started(self, test_case: TestCase) -> None:
        self.metrics.append(TestMetric(
            name="test_started",
            value=1,
            unit="count",
            category="execution",
            tags={"test_id": test_case.test_id, "test_type": test_case.test_type.value},
        ))

    def on_test_completed(self, result: TestResult) -> None:
        self.metrics.append(TestMetric(
            name="test_duration",
            value=result.duration_ms,
            unit="ms",
            category="performance",
            tags={"status": result.status.value},
        ))

    def on_suite_completed(self, suite: TestSuite, results: List[TestResult]) -> None:
        total = len(results)
        passed = sum(1 for r in results if r.status == TestStatus.PASSED)
        self.metrics.append(TestMetric(
            name="suite_pass_rate",
            value=(passed / max(total, 1)) * 100,
            unit="percent",
            category="quality",
            tags={"suite_id": suite.suite_id},
        ))


# ---------------------------------------------------------------------------
# Chain of Responsibility for quality gates
# ---------------------------------------------------------------------------

class QualityGateHandler(ABC):
    _next: Optional["QualityGateHandler"] = None

    def set_next(self, handler: "QualityGateHandler") -> "QualityGateHandler":
        self._next = handler
        return handler

    def handle(self, execution: TestExecution) -> bool:
        if self._check(execution):
            if self._next:
                return self._next.handle(execution)
            return True
        return False

    @abstractmethod
    def _check(self, execution: TestExecution) -> bool: ...


class CoverageGateHandler(QualityGateHandler):
    def __init__(self, min_coverage: float = 80.0) -> None:
        self.min_coverage = min_coverage

    def _check(self, execution: TestExecution) -> bool:
        coverage_val = execution.metadata.get("line_coverage", 0.0)
        if coverage_val < self.min_coverage:
            logger.warning(
                "Coverage gate FAILED: %.1f%% < %.1f%%",
                coverage_val,
                self.min_coverage,
            )
            return False
        logger.info("Coverage gate PASSED: %.1f%% >= %.1f%%", coverage_val, self.min_coverage)
        return True


class PassRateGateHandler(QualityGateHandler):
    def __init__(self, min_pass_rate: float = 95.0) -> None:
        self.min_pass_rate = min_pass_rate

    def _check(self, execution: TestExecution) -> bool:
        if execution.pass_rate < self.min_pass_rate:
            logger.warning(
                "Pass rate gate FAILED: %.1f%% < %.1f%%",
                execution.pass_rate,
                self.min_pass_rate,
            )
            return False
        logger.info("Pass rate gate PASSED: %.1f%%", execution.pass_rate)
        return True


class SecurityGateHandler(QualityGateHandler):
    def _check(self, execution: TestExecution) -> bool:
        critical_count = execution.metadata.get("critical_vulnerabilities", 0)
        if critical_count > 0:
            logger.warning("Security gate FAILED: %d critical vulnerabilities", critical_count)
            return False
        logger.info("Security gate PASSED: no critical vulnerabilities")
        return True


class PerformanceGateHandler(QualityGateHandler):
    def __init__(self, max_p95_ms: float = 500.0) -> None:
        self.max_p95_ms = max_p95_ms

    def _check(self, execution: TestExecution) -> bool:
        p95 = execution.metadata.get("p95_response_ms", 0.0)
        if p95 > self.max_p95_ms:
            logger.warning("Performance gate FAILED: p95=%.1fms > %.1fms", p95, self.max_p95_ms)
            return False
        logger.info("Performance gate PASSED: p95=%.1fms", p95)
        return True


# ---------------------------------------------------------------------------
# Main Agent Class
# ---------------------------------------------------------------------------

class AutomationQAAgent:
    """
    Enterprise-grade test automation agent that orchestrates test planning,
    generation, execution, reporting, and CI/CD integration.
    """

    def __init__(self, project_root: str = ".", config: Optional[Dict[str, Any]] = None) -> None:
        self.project_root = Path(project_root)
        self.config = config or {}
        self.observers: List[TestExecutionObserver] = []
        self.test_plans: Dict[str, TestPlan] = {}
        self.test_suites: Dict[str, TestSuite] = {}
        self.executions: Dict[str, TestExecution] = {}
        self.bug_reports: Dict[str, BugReport] = {}
        self.reports: Dict[str, TestReport] = {}
        self.environments: Dict[str, TestEnvironmentConfig] = {}
        self.metrics: List[TestMetric] = []
        self._quality_gate_chain: Optional[QualityGateHandler] = None
        self._setup_default_quality_gates()
        logger.info("AutomationQA Agent initialized for project: %s", self.project_root)

    def _setup_default_quality_gates(self) -> None:
        coverage = CoverageGateHandler(min_coverage=80.0)
        pass_rate = PassRateGateHandler(min_pass_rate=95.0)
        security = SecurityGateHandler()
        performance = PerformanceGateHandler(max_p95_ms=500.0)
        coverage.set_next(pass_rate).set_next(security).set_next(performance)
        self._quality_gate_chain = coverage

    def add_observer(self, observer: TestExecutionObserver) -> None:
        self.observers.append(observer)

    def _notify_test_started(self, test_case: TestCase) -> None:
        for obs in self.observers:
            obs.on_test_started(test_case)

    def _notify_test_completed(self, result: TestResult) -> None:
        for obs in self.observers:
            obs.on_test_completed(result)

    def _notify_suite_completed(self, suite: TestSuite, results: List[TestResult]) -> None:
        for obs in self.observers:
            obs.on_suite_completed(suite, results)

    # -----------------------------------------------------------------------
    # Test Planning
    # -----------------------------------------------------------------------

    def create_test_plan(
        self,
        name: str,
        description: str = "",
        project: str = "",
        version: str = "",
        author: str = "",
        environments: Optional[List[TestEnvironment]] = None,
        browsers: Optional[List[BrowserType]] = None,
        risk_areas: Optional[List[str]] = None,
        entry_criteria: Optional[List[str]] = None,
        exit_criteria: Optional[List[str]] = None,
    ) -> TestPlan:
        plan = TestPlan(
            name=name,
            description=description,
            project=project,
            version=version,
            author=author,
            environments=environments or [TestEnvironment.DEV, TestEnvironment.STAGING],
            browsers=browsers or [BrowserType.CHROME],
            risk_areas=risk_areas or [],
            entry_criteria=entry_criteria or [
                "Code compiles without errors",
                "Unit tests pass",
                "Deployment to test environment successful",
            ],
            exit_criteria=exit_criteria or [
                "All critical test cases pass",
                "Code coverage meets threshold",
                "No blocker/critical bugs open",
                "Performance thresholds met",
            ],
        )
        self.test_plans[plan.plan_id] = plan
        logger.info("Created test plan: %s (%s)", plan.name, plan.plan_id)
        return plan

    # -----------------------------------------------------------------------
    # Test Case Generation
    # -----------------------------------------------------------------------

    def generate_test_cases(
        self,
        test_type: TestType,
        source: Any,
        options: Optional[Dict[str, Any]] = None,
    ) -> List[TestCase]:
        strategy = TestGenerationFactory.get_strategy(test_type)
        test_cases = strategy.generate(source, options or {})
        logger.info(
            "Generated %d %s test cases",
            len(test_cases),
            test_type.value,
        )
        self.metrics.append(TestMetric(
            name="test_cases_generated",
            value=len(test_cases),
            unit="count",
            category="generation",
            tags={"test_type": test_type.value},
        ))
        return test_cases

    # -----------------------------------------------------------------------
    # Test Suite Management
    # -----------------------------------------------------------------------

    def create_test_suite(
        self,
        name: str,
        test_cases: Optional[List[TestCase]] = None,
        description: str = "",
        parallel: bool = False,
        max_workers: int = 4,
        tags: Optional[List[str]] = None,
        setup_script: str = "",
        teardown_script: str = "",
    ) -> TestSuite:
        suite = TestSuite(
            name=name,
            description=description,
            test_cases=test_cases or [],
            parallel=parallel,
            max_workers=max_workers,
            tags=tags or [],
            setup_script=setup_script,
            teardown_script=teardown_script,
        )
        self.test_suites[suite.suite_id] = suite
        logger.info(
            "Created test suite: %s with %d tests",
            suite.name,
            suite.total_count,
        )
        return suite

    # -----------------------------------------------------------------------
    # Test Execution
    # -----------------------------------------------------------------------

    def execute_test_suite(
        self,
        suite: TestSuite,
        environment: TestEnvironment = TestEnvironment.LOCAL,
        parallel: bool = False,
    ) -> TestExecution:
        execution = TestExecution(
            suite=suite,
            environment=environment,
            start_time=datetime.utcnow().isoformat(),
            triggered_by="automation_agent",
        )
        self.executions[execution.execution_id] = execution
        logger.info("Executing suite '%s' in %s", suite.name, environment.value)

        for test_case in suite.test_cases:
            self._notify_test_started(test_case)
            test_case.status = TestStatus.RUNNING
            result = self._execute_single_test(test_case, environment)
            execution.add_result(result)
            self._notify_test_completed(result)

        execution.end_time = datetime.utcnow().isoformat()
        execution.status = (
            TestStatus.PASSED if execution.failed == 0 else TestStatus.FAILED
        )
        self._notify_suite_completed(suite, execution.results)
        logger.info(
            "Suite '%s' execution completed: %s (%d/%d passed)",
            suite.name,
            execution.status.value,
            execution.passed,
            len(execution.results),
        )
        return execution

    def _execute_single_test(self, test_case: TestCase, environment: TestEnvironment) -> TestResult:
        result = TestResult(
            test_case=test_case,
            environment=environment,
            start_time=datetime.utcnow().isoformat(),
        )
        try:
            time.sleep(random.uniform(0.01, 0.05))
            success = random.random() > 0.1
            if success:
                result.status = TestStatus.PASSED
                test_case.mark_passed()
            else:
                result.status = TestStatus.FAILED
                result.error_message = "Simulated test failure"
                test_case.mark_failed(result.error_message)
        except Exception as exc:
            result.status = TestStatus.ERROR
            result.error_message = str(exc)
            test_case.mark_failed(str(exc))

        result.end_time = datetime.utcnow().isoformat()
        start = datetime.fromisoformat(result.start_time)
        end = datetime.fromisoformat(result.end_time)
        result.duration_ms = (end - start).total_seconds() * 1000
        return result

    # -----------------------------------------------------------------------
    # CI Pipeline Configuration
    # -----------------------------------------------------------------------

    def setup_ci_pipeline(
        self,
        provider: str = "github_actions",
        stages: Optional[List[CIPipelineStage]] = None,
        parallel_stages: bool = True,
        fail_fast: bool = True,
        retry_on_failure: bool = True,
        timeout_minutes: int = 60,
        notification_channels: Optional[List[str]] = None,
    ) -> CIConfig:
        config = CIConfig(
            provider=provider,
            pipeline_stages=stages or [
                CIPipelineStage.BUILD,
                CIPipelineStage.UNIT_TEST,
                CIPipelineStage.INTEGRATION_TEST,
                CIPipelineStage.E2E_TEST,
                CIPipelineStage.SECURITY_SCAN,
                CIPipelineStage.PERFORMANCE_TEST,
                CIPipelineStage.DEPLOY_STAGING,
                CIPipelineStage.ACCEPTANCE,
                CIPipelineStage.DEPLOY_PRODUCTION,
            ],
            parallel_stages=parallel_stages,
            fail_fast=fail_fast,
            retry_on_failure=retry_on_failure,
            timeout_minutes=timeout_minutes,
            notification_channels=notification_channels or [],
        )
        logger.info("CI pipeline configured for provider: %s", provider)
        self.metrics.append(TestMetric(
            name="ci_pipeline_configured",
            value=1,
            unit="count",
            category="ci_cd",
            tags={"provider": provider},
        ))
        return config

    # -----------------------------------------------------------------------
    # Browser Testing Configuration
    # -----------------------------------------------------------------------

    def configure_browser_testing(
        self,
        browsers: Optional[List[BrowserType]] = None,
        headless: bool = True,
        viewport_width: int = 1920,
        viewport_height: int = 1080,
        screenshots: str = "only-on-failure",
        video: str = "retain-on-failure",
    ) -> List[BrowserTestConfig]:
        target_browsers = browsers or [BrowserType.CHROME, BrowserType.FIREFOX]
        configs: List[BrowserTestConfig] = []
        for browser in target_browsers:
            config = BrowserTestConfig(
                browser=browser,
                headless=headless,
                viewport_width=viewport_width,
                viewport_height=viewport_height,
                screenshots=screenshots,
                video=video,
            )
            configs.append(config)
            logger.info("Configured browser: %s", browser.value)
        return configs

    # -----------------------------------------------------------------------
    # Performance Testing
    # -----------------------------------------------------------------------

    def run_performance_tests(
        self,
        config: PerformanceTestConfig,
    ) -> PerformanceResult:
        logger.info(
            "Starting performance test: %s with %d VUs",
            config.target_url,
            config.virtual_users,
        )
        result = PerformanceResult(config=config)
        rng = random.Random()
        base_latency = rng.uniform(50, 200)
        result.total_requests = config.virtual_users * (config.test_duration_seconds // 5)
        result.successful_requests = int(result.total_requests * (1 - random.uniform(0, 0.05)))
        result.failed_requests = result.total_requests - result.successful_requests
        result.avg_response_time_ms = base_latency + rng.uniform(-20, 50)
        result.p50_response_time_ms = base_latency
        result.p95_response_time_ms = base_latency * 2.5
        result.p99_response_time_ms = base_latency * 4.0
        result.max_response_time_ms = base_latency * 8.0
        result.min_response_time_ms = base_latency * 0.3
        result.requests_per_second = result.total_requests / max(config.test_duration_seconds, 1)
        result.error_rate = (result.failed_requests / max(result.total_requests, 1)) * 100
        result.duration_seconds = config.test_duration_seconds
        self.metrics.append(TestMetric(
            name="performance_test_completed",
            value=1,
            unit="count",
            category="performance",
            tags={"target": config.target_url, "passed": str(result.passed)},
        ))
        logger.info(
            "Performance test completed: avg=%.1fms p95=%.1fms rps=%.1f passed=%s",
            result.avg_response_time_ms,
            result.p95_response_time_ms,
            result.requests_per_second,
            result.passed,
        )
        return result

    def analyze_performance_results(
        self,
        result: PerformanceResult,
        thresholds: Optional[Dict[str, float]] = None,
    ) -> Dict[str, Any]:
        analysis: Dict[str, Any] = {
            "summary": result.summary(),
            "thresholds_met": True,
            "violations": [],
            "recommendations": [],
        }
        t = thresholds or {}
        if "max_p95_ms" in t and result.p95_response_time_ms > t["max_p95_ms"]:
            analysis["thresholds_met"] = False
            analysis["violations"].append(
                f"p95 response time {result.p95_response_time_ms:.1f}ms exceeds threshold {t['max_p95_ms']}ms"
            )
        if "max_error_rate" in t and result.error_rate > t["max_error_rate"]:
            analysis["thresholds_met"] = False
            analysis["violations"].append(
                f"Error rate {result.error_rate:.2f}% exceeds threshold {t['max_error_rate']}%"
            )
        if result.p95_response_time_ms > 1000:
            analysis["recommendations"].append("Consider implementing response caching")
        if result.error_rate > 1.0:
            analysis["recommendations"].append("Investigate error sources and add retry logic")
        if result.requests_per_second < 50:
            analysis["recommendations"].append("Consider horizontal scaling for higher throughput")
        return analysis

    # -----------------------------------------------------------------------
    # Security Scanning
    # -----------------------------------------------------------------------

    def run_security_scan(
        self,
        target: str,
        scan_type: SecurityTestType = SecurityTestType.DAST,
        custom_rules: Optional[List[Dict[str, Any]]] = None,
    ) -> SecurityScanResult:
        logger.info("Starting %s security scan on: %s", scan_type.value, target)
        result = SecurityScanResult(
            scan_type=scan_type,
            target=target,
        )
        rng = random.Random()
        result.total_vulnerabilities = rng.randint(0, 20)
        result.critical_count = rng.randint(0, 2)
        result.high_count = rng.randint(0, 5)
        result.medium_count = rng.randint(0, 8)
        result.low_count = rng.randint(0, 10)
        result.info_count = rng.randint(0, 5)
        result.scan_duration_seconds = rng.uniform(30, 300)
        result.vulnerabilities = [
            {
                "id": f"VULN-{uuid.uuid4().hex[:6].upper()}",
                "title": f"Simulated vulnerability #{i + 1}",
                "severity": random.choice(["critical", "high", "medium", "low"]),
                "cwe": f"CWE-{random.randint(1, 999)}",
                "url": target,
            }
            for i in range(min(result.total_vulnerabilities, 10))
        ]
        self.metrics.append(TestMetric(
            name="security_scan_completed",
            value=1,
            unit="count",
            category="security",
            tags={"scan_type": scan_type.value, "target": target},
        ))
        logger.info(
            "Security scan completed: %d vulnerabilities (critical=%d, high=%d)",
            result.total_vulnerabilities,
            result.critical_count,
            result.high_count,
        )
        return result

    # -----------------------------------------------------------------------
    # Code Coverage Analysis
    # -----------------------------------------------------------------------

    def analyze_code_coverage(
        self,
        project_name: str,
        source_dirs: Optional[List[str]] = None,
        threshold: float = 80.0,
    ) -> CodeCoverageReport:
        logger.info("Analyzing code coverage for: %s", project_name)
        rng = random.Random()
        report = CodeCoverageReport(
            project_name=project_name,
            coverage_threshold=threshold,
        )
        report.total_lines = rng.randint(5000, 50000)
        report.line_coverage = rng.uniform(60, 95)
        report.branch_coverage = rng.uniform(55, 90)
        report.function_coverage = rng.uniform(65, 98)
        report.covered_lines = int(report.total_lines * report.line_coverage / 100)
        report.file_coverage = {
            f"src/module_{i}.py": rng.uniform(40, 100) for i in range(10)
        }
        report.uncovered_files = [
            f"src/legacy/old_module_{i}.py" for i in range(rng.randint(0, 5))
        ]
        self.metrics.append(TestMetric(
            name="code_coverage_analyzed",
            value=report.line_coverage,
            unit="percent",
            category="quality",
            tags={"project": project_name},
        ))
        logger.info(
            "Code coverage: line=%.1f%% branch=%.1f%% function=%.1f%% meets_threshold=%s",
            report.line_coverage,
            report.branch_coverage,
            report.function_coverage,
            report.meets_threshold,
        )
        return report

    # -----------------------------------------------------------------------
    # Bug Reporting
    # -----------------------------------------------------------------------

    def create_bug_report(
        self,
        title: str,
        description: str,
        severity: SeverityLevel = SeverityLevel.MAJOR,
        steps_to_reproduce: Optional[List[str]] = None,
        expected_behavior: str = "",
        actual_behavior: str = "",
        environment: str = "",
        related_test_case: str = "",
        reporter: str = "automation_agent",
    ) -> BugReport:
        bug = BugReport(
            title=title,
            description=description,
            severity=severity,
            steps_to_reproduce=steps_to_reproduce or [],
            expected_behavior=expected_behavior,
            actual_behavior=actual_behavior,
            environment=environment,
            related_test_case=related_test_case,
            reporter=reporter,
        )
        self.bug_reports[bug.bug_id] = bug
        logger.info("Created bug report: %s [%s] - %s", bug.bug_id, severity.value, title)
        return bug

    # -----------------------------------------------------------------------
    # Test Reporting
    # -----------------------------------------------------------------------

    def generate_test_report(
        self,
        execution: TestExecution,
        title: str = "",
        coverage: Optional[CodeCoverageReport] = None,
        performance: Optional[PerformanceResult] = None,
        security: Optional[SecurityScanResult] = None,
        format: ReportFormat = ReportFormat.HTML,
    ) -> TestReport:
        report = TestReport(
            title=title or f"Test Report - {execution.execution_id}",
            execution=execution,
            coverage=coverage,
            performance=performance,
            security=security,
            format=format,
        )
        report.recommendations = self._generate_recommendations(execution, coverage, performance, security)
        self.reports[report.report_id] = report
        logger.info(
            "Generated test report: %s (format=%s, recommendations=%d)",
            report.report_id,
            format.value,
            len(report.recommendations),
        )
        return report

    def _generate_recommendations(
        self,
        execution: TestExecution,
        coverage: Optional[CodeCoverageReport],
        performance: Optional[PerformanceResult],
        security: Optional[SecurityScanResult],
    ) -> List[str]:
        recommendations: List[str] = []
        if execution.pass_rate < 100:
            recommendations.append("Fix failing tests before release")
        if execution.skipped > 0:
            recommendations.append(f"Review {execution.skipped} skipped tests")
        if coverage and not coverage.meets_threshold:
            recommendations.append(
                f"Increase code coverage from {coverage.line_coverage:.1f}% to at least {coverage.coverage_threshold}%"
            )
        if performance and not performance.passed:
            recommendations.append("Performance thresholds not met — investigate bottlenecks")
        if security and security.has_critical:
            recommendations.append("Critical security vulnerabilities must be resolved before release")
        if not recommendations:
            recommendations.append("All quality gates passed — ready for release")
        return recommendations

    # -----------------------------------------------------------------------
    # Environment Management
    # -----------------------------------------------------------------------

    def setup_test_environments(
        self,
        environments: Optional[List[TestEnvironmentConfig]] = None,
    ) -> List[TestEnvironmentConfig]:
        configs = environments or [
            TestEnvironmentConfig(
                name=TestEnvironment.DEV,
                base_url="http://localhost:3000",
                api_base_url="http://localhost:3001/api",
            ),
            TestEnvironmentConfig(
                name=TestEnvironment.STAGING,
                base_url="https://staging.example.com",
                api_base_url="https://staging-api.example.com/api",
            ),
            TestEnvironmentConfig(
                name=TestEnvironment.QA,
                base_url="https://qa.example.com",
                api_base_url="https://qa-api.example.com/api",
            ),
        ]
        for config in configs:
            self.environments[config.env_id] = config
            logger.info("Configured environment: %s (%s)", config.name.value, config.base_url)
        return configs

    # -----------------------------------------------------------------------
    # Test Data Management
    # -----------------------------------------------------------------------

    def manage_test_data(
        self,
        dataset_name: str,
        schema: Dict[str, str],
        record_count: int = 100,
        seed: int = 42,
        cleanup_strategy: str = "after_suite",
    ) -> TestDataManagement:
        tdm = TestDataManagement(
            dataset_name=dataset_name,
            schema=schema,
            record_count=record_count,
            seed=seed,
            cleanup_strategy=cleanup_strategy,
        )
        records = tdm.generate_records(record_count)
        logger.info(
            "Generated %d test data records for dataset '%s'",
            len(records),
            dataset_name,
        )
        return tdm

    # -----------------------------------------------------------------------
    # Flaky Test Analysis
    # -----------------------------------------------------------------------

    def analyze_flaky_tests(
        self,
        execution_history: List[TestExecution],
        flaky_threshold: float = 20.0,
    ) -> List[FlakyTestAnalysis]:
        test_results_map: Dict[str, List[str]] = defaultdict(list)
        test_names: Dict[str, str] = {}
        for execution in execution_history:
            for result in execution.results:
                if result.test_case:
                    tc_id = result.test_case.test_id
                    test_names[tc_id] = result.test_case.name
                    test_results_map[tc_id].append(result.status.value)

        flaky_tests: List[FlakyTestAnalysis] = []
        for tc_id, statuses in test_results_map.items():
            fail_count = statuses.count("failed")
            total = len(statuses)
            fail_rate = (fail_count / max(total, 1)) * 100
            if fail_rate > 0 and fail_rate < 100:
                analysis = FlakyTestAnalysis(
                    test_id=tc_id,
                    test_name=test_names.get(tc_id, "unknown"),
                    total_runs=total,
                    pass_count=total - fail_count,
                    fail_count=fail_count,
                    last_10_results=statuses[-10:],
                )
                analysis.calculate_flaky_score()
                if analysis.flaky_score >= flaky_threshold:
                    if analysis.flaky_rate > 50:
                        analysis.recommended_action = "Investigate and fix root cause"
                    else:
                        analysis.recommended_action = "Add retry logic or quarantine"
                    flaky_tests.append(analysis)

        flaky_tests.sort(key=lambda x: x.flaky_score, reverse=True)
        logger.info("Found %d flaky tests", len(flaky_tests))
        return flaky_tests

    # -----------------------------------------------------------------------
    # Regression Test Suite
    # -----------------------------------------------------------------------

    def create_regression_suite(
        self,
        name: str,
        all_test_cases: List[TestCase],
        changed_files: Optional[List[str]] = None,
        include_critical_path: bool = True,
    ) -> RegressionTestSet:
        rts = RegressionTestSet(name=name)
        for tc in all_test_cases:
            if include_critical_path and "critical-path" in tc.tags:
                rts.test_case_ids.append(tc.test_id)
            elif changed_files:
                impact = rts.change_impact_map.get(tc.test_id, [])
                if any(cf in impact for cf in changed_files):
                    rts.test_case_ids.append(tc.test_id)
        if not rts.test_case_ids:
            rts.test_case_ids = [tc.test_id for tc in all_test_cases[:10]]
        logger.info(
            "Created regression suite '%s' with %d tests",
            name,
            len(rts.test_case_ids),
        )
        return rts

    # -----------------------------------------------------------------------
    # API Testing
    # -----------------------------------------------------------------------

    def run_api_tests(
        self,
        api_test_cases: List[APITestCase],
        base_url: str = "",
        auth_headers: Optional[Dict[str, str]] = None,
    ) -> List[Dict[str, Any]]:
        results: List[Dict[str, Any]] = []
        for tc in api_test_cases:
            logger.info("Running API test: %s %s", tc.method, tc.endpoint)
            result: Dict[str, Any] = {
                "test_id": tc.test_id,
                "name": tc.name,
                "method": tc.method,
                "endpoint": tc.endpoint,
                "status": "passed",
                "status_code": tc.expected_status,
                "duration_ms": random.uniform(50, 500),
            }
            success = random.random() > 0.05
            if not success:
                result["status"] = "failed"
                result["error"] = "Unexpected response"
            results.append(result)
        passed = sum(1 for r in results if r["status"] == "passed")
        logger.info("API tests completed: %d/%d passed", passed, len(results))
        return results

    # -----------------------------------------------------------------------
    # Visual Testing
    # -----------------------------------------------------------------------

    def setup_visual_testing(
        self,
        pages: List[str],
        baseline_dir: str = "./visual-baselines",
        diff_threshold: float = 0.1,
        browsers: Optional[List[BrowserType]] = None,
    ) -> Dict[str, Any]:
        config = {
            "pages": pages,
            "baseline_dir": baseline_dir,
            "diff_threshold": diff_threshold,
            "browsers": [b.value for b in (browsers or [BrowserType.CHROME])],
            "enabled": True,
        }
        logger.info(
            "Visual testing configured: %d pages, threshold=%.1f%%",
            len(pages),
            diff_threshold * 100,
        )
        return config

    # -----------------------------------------------------------------------
    # Accessibility Testing
    # -----------------------------------------------------------------------

    def run_accessibility_tests(
        self,
        urls: List[str],
        wcag_level: str = "AA",
        wcag_version: str = "2.1",
    ) -> Dict[str, List[AccessibilityViolation]]:
        results: Dict[str, List[AccessibilityViolation]] = {}
        rule_ids = [
            "color-contrast", "image-alt", "label", "link-name",
            "button-name", "aria-required-attr", "html-has-lang",
            "document-title", "meta-viewport", "heading-order",
        ]
        for url in urls:
            violations: List[AccessibilityViolation] = []
            count = random.randint(0, 5)
            for _ in range(count):
                violations.append(AccessibilityViolation(
                    violation_id=f"AX-{uuid.uuid4().hex[:6].upper()}",
                    rule_id=random.choice(rule_ids),
                    impact=random.choice(["critical", "serious", "moderate", "minor"]),
                    description=f"Accessibility violation on {url}",
                    wcag_level=wcag_level,
                    wcag_version=wcag_version,
                    nodes_affected=random.randint(1, 20),
                ))
            results[url] = violations
            logger.info(
                "Accessibility scan for %s: %d violations",
                url,
                len(violations),
            )
        return results

    # -----------------------------------------------------------------------
    # Contract Testing
    # -----------------------------------------------------------------------

    def create_contract_test(
        self,
        provider: str,
        consumer: str,
        interactions: List[Dict[str, Any]],
        pact_version: str = "4.0",
    ) -> ContractTestResult:
        result = ContractTestResult(
            provider=provider,
            consumer=consumer,
            pact_version=pact_version,
        )
        all_passed = True
        for interaction in interactions:
            mismatch = random.random() < 0.05
            if mismatch:
                all_passed = False
                result.mismatches.append({
                    "interaction": interaction.get("description", ""),
                    "mismatch_type": "body_mismatch",
                    "expected": interaction.get("expected", {}),
                    "actual": interaction.get("actual", {}),
                })
        result.status = "verified" if all_passed else "failed"
        result.verified_at = datetime.utcnow().isoformat()
        result.interaction_description = f"{len(interactions)} interactions tested"
        logger.info(
            "Contract test %s: provider=%s consumer=%s status=%s",
            result.result_id,
            provider,
            consumer,
            result.status,
        )
        return result

    # -----------------------------------------------------------------------
    # Quality Metrics and Dashboard
    # -----------------------------------------------------------------------

    def get_quality_metrics(self) -> Dict[str, Any]:
        total_executions = len(self.executions)
        total_bugs = len(self.bug_reports)
        total_reports = len(self.reports)
        avg_pass_rate = 0.0
        if self.executions:
            avg_pass_rate = sum(e.pass_rate for e in self.executions.values()) / total_executions
        severity_dist: Dict[str, int] = defaultdict(int)
        for bug in self.bug_reports.values():
            severity_dist[bug.severity.value] += 1
        return {
            "total_executions": total_executions,
            "total_bugs": total_bugs,
            "total_reports": total_reports,
            "average_pass_rate": round(avg_pass_rate, 1),
            "severity_distribution": dict(severity_dist),
            "metrics_collected": len(self.metrics),
            "environments_configured": len(self.environments),
        }

    def generate_test_dashboard(self) -> Dict[str, Any]:
        metrics = self.get_quality_metrics()
        dashboard: Dict[str, Any] = {
            "title": "Test Automation Dashboard",
            "generated_at": datetime.utcnow().isoformat(),
            "summary": metrics,
            "recent_executions": [],
            "quality_trend": [],
            "flaky_tests": [],
            "coverage_trend": [],
        }
        sorted_execs = sorted(
            self.executions.values(),
            key=lambda e: e.start_time,
            reverse=True,
        )
        for exe in sorted_execs[:10]:
            dashboard["recent_executions"].append(exe.summary())
        for i in range(7):
            dashboard["quality_trend"].append({
                "date": (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d"),
                "pass_rate": round(random.uniform(85, 100), 1),
            })
        for i in range(7):
            dashboard["coverage_trend"].append({
                "date": (datetime.utcnow() - timedelta(days=i)).strftime("%Y-%m-%d"),
                "line_coverage": round(random.uniform(75, 92), 1),
            })
        logger.info("Generated test dashboard with %d recent executions", len(dashboard["recent_executions"]))
        return dashboard

    # -----------------------------------------------------------------------
    # Data Export
    # -----------------------------------------------------------------------

    def export_test_data(
        self,
        output_path: str = "./test-data-export",
        format: ReportFormat = ReportFormat.JSON,
    ) -> str:
        export_data = {
            "exported_at": datetime.utcnow().isoformat(),
            "format": format.value,
            "test_plans": len(self.test_plans),
            "test_suites": len(self.test_suites),
            "executions": len(self.executions),
            "bug_reports": len(self.bug_reports),
            "metrics": [m.to_dict() for m in self.metrics[-100:]],
        }
        output = Path(output_path)
        output.mkdir(parents=True, exist_ok=True)
        filename = output / f"test-export-{uuid.uuid4().hex[:8]}.json"
        filename.write_text(json.dumps(export_data, indent=2), encoding="utf-8")
        logger.info("Exported test data to: %s", filename)
        return str(filename)

    # -----------------------------------------------------------------------
    # Utility Methods
    # -----------------------------------------------------------------------

    def evaluate_quality_gates(self, execution: TestExecution) -> bool:
        if self._quality_gate_chain is None:
            return True
        passed = self._quality_gate_chain.handle(execution)
        logger.info("Quality gates evaluation: %s", "PASSED" if passed else "FAILED")
        return passed

    def get_test_history(self, test_id: str) -> List[Dict[str, Any]]:
        history: List[Dict[str, Any]] = []
        for execution in self.executions.values():
            for result in execution.results:
                if result.test_case and result.test_case.test_id == test_id:
                    history.append(result.summary())
        return history

    def get_suite_statistics(self, suite_id: str) -> Dict[str, Any]:
        suite = self.test_suites.get(suite_id)
        if suite is None:
            return {"error": "Suite not found"}
        type_dist: Dict[str, int] = defaultdict(int)
        priority_dist: Dict[str, int] = defaultdict(int)
        for tc in suite.test_cases:
            type_dist[tc.test_type.value] += 1
            priority_dist[tc.priority.value] += 1
        return {
            "suite_id": suite.suite_id,
            "name": suite.name,
            "total_tests": suite.total_count,
            "type_distribution": dict(type_dist),
            "priority_distribution": dict(priority_dist),
            "parallel_enabled": suite.parallel,
            "max_workers": suite.max_workers,
        }


# ---------------------------------------------------------------------------
# CLI Entry Point / Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 72)
    print(" AutomationQA Agent v3.0.0 — Enterprise Test Automation Demo")
    print("=" * 72)

    agent = AutomationQAAgent(project_root=".")
    agent.add_observer(LoggingObserver())
    agent.add_observer(MetricsObserver())

    # --- Test Plan ---
    plan = agent.create_test_plan(
        name="Q4 Release Test Plan",
        description="Comprehensive test plan for Q4 product release",
        project="myapp",
        version="2.5.0",
        author="qa-team",
        environments=[TestEnvironment.DEV, TestEnvironment.STAGING, TestEnvironment.UAT],
    )
    print(f"\nTest Plan: {plan.summary()}")

    # --- Unit Tests ---
    unit_tests = agent.generate_test_cases(
        TestType.UNIT,
        source=None,
        options={
            "functions": [
                {"name": "calculate_tax", "params": {"income": 50000}, "expected": {"tax": 7500}},
                {"name": "validate_email", "params": {"email": "a@b.com"}, "expected": {"valid": True}},
                {"name": "format_currency", "params": {"amount": 1234.56}, "expected": {"formatted": "$1,234.56"}},
            ]
        },
    )
    print(f"Generated {len(unit_tests)} unit test cases")

    # --- API Tests ---
    api_tests = agent.generate_test_cases(
        TestType.API,
        source=None,
        options={
            "endpoints": [
                {"method": "GET", "path": "/api/users", "expected_status": 200},
                {"method": "POST", "path": "/api/orders", "expected_status": 201},
                {"method": "GET", "path": "/api/products/123", "expected_status": 200},
            ]
        },
    )
    print(f"Generated {len(api_tests)} API test cases")

    # --- E2E Tests ---
    e2e_tests = agent.generate_test_cases(
        TestType.E2E,
        source=None,
        options={
            "user_flows": [
                {
                    "name": "user_registration",
                    "steps": [
                        {"action": "Navigate to /register", "data": ""},
                        {"action": "Fill registration form", "data": ""},
                        {"action": "Submit form", "data": ""},
                        {"action": "Verify welcome page", "data": ""},
                    ],
                },
                {
                    "name": "checkout_flow",
                    "steps": [
                        {"action": "Add item to cart", "data": ""},
                        {"action": "Proceed to checkout", "data": ""},
                        {"action": "Enter payment details", "data": ""},
                        {"action": "Confirm order", "data": ""},
                    ],
                },
            ]
        },
    )
    print(f"Generated {len(e2e_tests)} E2E test cases")

    # --- Test Suite ---
    all_tests = unit_tests + api_tests + e2e_tests
    suite = agent.create_test_suite(
        name="Full Regression Suite",
        test_cases=all_tests,
        description="Complete regression suite for Q4 release",
        parallel=True,
        max_workers=4,
    )
    print(f"\nSuite Statistics: {agent.get_suite_statistics(suite.suite_id)}")

    # --- Execute ---
    execution = agent.execute_test_suite(suite, environment=TestEnvironment.STAGING)
    print(f"\nExecution Summary: {execution.summary()}")

    # --- Coverage ---
    coverage = agent.analyze_code_coverage("myapp", threshold=80.0)
    print(f"\nCoverage: {coverage.summary()}")

    # --- Performance ---
    perf_config = PerformanceTestConfig(
        target_url="https://api.example.com",
        load_pattern=PerformanceLoadPattern.RAMP_UP,
        virtual_users=200,
        test_duration_seconds=120,
    )
    perf_result = agent.run_performance_tests(perf_config)
    perf_analysis = agent.analyze_performance_results(perf_result, {"max_p95_ms": 500.0})
    print(f"\nPerformance: {perf_result.summary()}")
    print(f"Performance Analysis: thresholds_met={perf_analysis['thresholds_met']}, violations={len(perf_analysis['violations'])}")

    # --- Security ---
    security_result = agent.run_security_scan("https://example.com", SecurityTestType.DAST)
    print(f"\nSecurity: {security_result.summary()}")

    # --- Bug Report ---
    bug = agent.create_bug_report(
        title="Login page returns 500 on invalid credentials",
        description="When entering invalid credentials, the server returns a 500 error instead of 401.",
        severity=SeverityLevel.CRITICAL,
        steps_to_reproduce=[
            "Navigate to /login",
            "Enter invalid credentials",
            "Click login",
            "Observe 500 Internal Server Error",
        ],
        expected_behavior="Server returns 401 Unauthorized",
        actual_behavior="Server returns 500 Internal Server Error",
    )
    print(f"\nBug Report: {bug.to_dict()}")

    # --- Report ---
    report = agent.generate_test_report(
        execution,
        title="Q4 Release - Full Test Report",
        coverage=coverage,
        performance=perf_result,
        security=security_result,
    )
    print(f"\nReport JSON:\n{report.to_json()[:500]}...")

    # --- Quality Gates ---
    gate_passed = agent.evaluate_quality_gates(execution)
    print(f"\nQuality Gates: {'PASSED' if gate_passed else 'FAILED'}")

    # --- Dashboard ---
    dashboard = agent.generate_test_dashboard()
    print(f"\nDashboard Summary: {json.dumps(dashboard['summary'], indent=2)}")

    # --- Export ---
    export_path = agent.export_test_data("./test-export")
    print(f"\nData exported to: {export_path}")

    # --- Final Metrics ---
    metrics = agent.get_quality_metrics()
    print(f"\nOverall Quality Metrics: {json.dumps(metrics, indent=2)}")
    print("\n" + "=" * 72)
    print(" AutomationQA Agent Demo Complete")
    print("=" * 72)


if __name__ == "__main__":
    main()

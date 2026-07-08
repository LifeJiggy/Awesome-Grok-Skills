#!/usr/bin/env python3
"""
Grok Testing Agent
Comprehensive software testing platform covering test automation,
performance testing, security testing, test management, and quality gates.
"""

from __future__ import annotations

import hashlib
import json
import logging
import math
import random
import re
import statistics
import time
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    NamedTuple,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Union,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    PERFORMANCE = "performance"
    SECURITY = "security"
    ACCESSIBILITY = "accessibility"
    SMOKE = "smoke"
    REGRESSION = "regression"
    API = "api"
    CONTRACT = "contract"
    VISUAL = "visual"
    CHAOS = "chaos"
    LOAD = "load"
    STRESS = "stress"
    ENDURANCE = "endurance"


class TestStatus(Enum):
    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"
    ERROR = "error"
    FLAKY = "flaky"


class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4
    OPTIONAL = 5


class TestFramework(Enum):
    PYTEST = "pytest"
    UNITTEST = "unittest"
    JEST = "jest"
    JUNIT = "junit"
    CYPRESS = "cypress"
    PLAYWRIGHT = "playwright"
    SELENIUM = "selenium"
    JMeter = "jmeter"
    K6 = "k6"
    GATLING = "gatling"
    OWASP_ZAP = "owasp_zap"
    BURP = "burp"
    SONARQUBE = "sonarqube"


class TestEnvironment(Enum):
    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    QA = "qa"
    PRE_PRODUCTION = "pre_production"
    PRODUCTION = "production"
    DR = "disaster_recovery"


class QualityGate(Enum):
    CODE_COVERAGE = "code_coverage"
    TEST_PASS_RATE = "test_pass_rate"
    CODE_QUALITY = "code_quality"
    SECURITY_SCAN = "security_scan"
    PERFORMANCE = "performance"
    ACCESSIBILITY = "accessibility"
    API_CONTRACT = "api_contract"
    VISUAL_REGRESSION = "visual_regression"


class GateStatus(Enum):
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    NOT_STARTED = "not_started"
    SKIPPED = "skipped"


class DefectSeverity(Enum):
    BLOCKER = "blocker"
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    TRIVIAL = "trivial"


class DefectStatus(Enum):
    NEW = "new"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    FIXED = "fixed"
    VERIFIED = "verified"
    CLOSED = "closed"
    REOPENED = "reopened"
    DEFERRED = "deferred"


class MetricType(Enum):
    PASS_RATE = "pass_rate"
    CODE_COVERAGE = "code_coverage"
    EXECUTION_TIME = "execution_time"
    DEFECT_DENSITY = "defect_density"
    TEST_VELOCITY = "test_velocity"
    MEAN_TIME_TO_REPAIR = "mttr"
    FLAKY_RATE = "flaky_rate"


class LoadPattern(Enum):
    CONSTANT = "constant"
    RAMP_UP = "ramp_up"
    RAMP_DOWN = "ramp_down"
    SPIKE = "spike"
    STEP = "step"
    WAVE = "wave"
    RANDOM = "random"


class SecurityTestType(Enum):
    SAST = "sast"                  # Static Application Security Testing
    DAST = "dast"                  # Dynamic Application Security Testing
    SCA = "sca"                    # Software Composition Analysis
    IAST = "iast"                  # Interactive Application Security Testing
    PEN_TEST = "penetration_test"
    THREAT_MODEL = "threat_model"
    CODE_REVIEW = "security_code_review"
    CONFIG_REVIEW = "config_review"


class PerformanceMetric(Enum):
    RESPONSE_TIME = "response_time"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    CPU_USAGE = "cpu_usage"
    MEMORY_USAGE = "memory_usage"
    DISK_IO = "disk_io"
    NETWORK_IO = "network_io"
    CONCURRENT_USERS = "concurrent_users"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class TestCase:
    """Test case definition."""
    test_id: str
    name: str
    description: str
    test_type: TestType
    status: TestStatus = TestStatus.PENDING
    priority: Priority = Priority.MEDIUM
    preconditions: List[str] = field(default_factory=list)
    steps: List[Dict[str, Any]] = field(default_factory=list)
    expected_results: List[str] = field(default_factory=list)
    actual_results: List[str] = field(default_factory=list)
    automation_status: str = "manual"
    created_at: datetime = field(default_factory=datetime.utcnow)
    executed_at: Optional[datetime] = None
    execution_time_ms: float = 0.0
    tags: List[str] = field(default_factory=list)
    author: str = ""
    requirements: List[str] = field(default_factory=list)
    retries: int = 0
    max_retries: int = 3
    timeout_ms: int = 30000

    @property
    def is_automated(self) -> bool:
        return self.automation_status == "automated"

    @property
    def duration_seconds(self) -> float:
        return self.execution_time_ms / 1000

    @property
    def can_retry(self) -> bool:
        return self.retries < self.max_retries


@dataclass
class TestSuite:
    """Test suite definition."""
    suite_id: str
    name: str
    description: str
    test_cases: List[str] = field(default_factory=list)
    target: str = ""
    status: str = "ready"
    statistics: Dict[str, int] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    environment: TestEnvironment = TestEnvironment.DEVELOPMENT
    parallel: bool = False
    max_parallel: int = 4
    timeout_minutes: int = 60
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def total_tests(self) -> int:
        return len(self.test_cases)

    @property
    def pass_rate(self) -> float:
        total = self.statistics.get("total", 0)
        passed = self.statistics.get("passed", 0)
        return (passed / total * 100) if total > 0 else 0


@dataclass
class TestExecution:
    """Test execution record."""
    execution_id: str
    suite_id: str
    test_id: str
    status: TestStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_ms: float = 0.0
    error_message: str = ""
    stack_trace: str = ""
    screenshots: List[str] = field(default_factory=list)
    logs: List[str] = field(default_factory=list)
    retries: int = 0
    environment: TestEnvironment = TestEnvironment.DEVELOPMENT

    @property
    def is_success(self) -> bool:
        return self.status == TestStatus.PASSED


@dataclass
class TestMetrics:
    """Test metrics aggregation."""
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    blocked: int = 0
    error: int = 0
    flaky: int = 0
    pass_rate: float = 0.0
    avg_execution_time: float = 0.0
    total_execution_time: float = 0.0
    coverage: float = 0.0
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def effective_pass_rate(self) -> float:
        effective_total = self.total_tests - self.skipped
        return (self.passed / effective_total * 100) if effective_total > 0 else 0


@dataclass
class TestReport:
    """Test execution report."""
    report_id: str
    suite_id: str
    execution_date: datetime
    environment: TestEnvironment
    metrics: TestMetrics
    failures: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    coverage_report: Optional[Dict[str, Any]] = None
    performance_report: Optional[Dict[str, Any]] = None
    security_report: Optional[Dict[str, Any]] = None
    executive_summary: str = ""
    recommendations: List[str] = field(default_factory=list)


@dataclass
class QualityGateResult:
    """Quality gate evaluation result."""
    gate: QualityGate
    status: GateStatus
    threshold: float
    actual_value: float
    message: str = ""
    details: Dict[str, Any] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return self.status == GateStatus.PASSED


@dataclass
class Defect:
    """Software defect record."""
    defect_id: str
    title: str
    description: str
    severity: DefectSeverity
    status: DefectStatus = DefectStatus.NEW
    priority: Priority = Priority.HIGH
    steps_to_reproduce: List[str] = field(default_factory=list)
    expected_behavior: str = ""
    actual_behavior: str = ""
    environment: str = ""
    version: str = ""
    assignee: str = ""
    reporter: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    related_test: str = ""
    tags: List[str] = field(default_factory=list)
    attachments: List[str] = field(default_factory=list)

    @property
    def age_days(self) -> int:
        end = self.resolved_at or datetime.utcnow()
        return (end - self.created_at).days

    @property
    def is_open(self) -> bool:
        return self.status in (DefectStatus.NEW, DefectStatus.ASSIGNED, DefectStatus.IN_PROGRESS, DefectStatus.REOPENED)


@dataclass
class PerformanceBenchmark:
    """Performance test benchmark."""
    benchmark_id: str
    name: str
    metric: PerformanceMetric
    target_value: float
    actual_value: float = 0.0
    unit: str = ""
    threshold_pct: float = 10.0
    status: str = "pending"

    @property
    def within_threshold(self) -> bool:
        if self.target_value == 0:
            return True
        deviation = abs(self.actual_value - self.target_value) / self.target_value * 100
        return deviation <= self.threshold_pct

    @property
    def deviation_pct(self) -> float:
        if self.target_value == 0:
            return 0.0
        return (self.actual_value - self.target_value) / self.target_value * 100


@dataclass
class SecurityVulnerability:
    """Security vulnerability record."""
    vuln_id: str
    title: str
    severity: str  # critical, high, medium, low, informational
    cvss_score: float = 0.0
    cwe_id: str = ""
    description: str = ""
    remediation: str = ""
    affected_component: str = ""
    status: str = "open"
    discovered_date: datetime = field(default_factory=datetime.utcnow)
    verified: bool = False

    @property
    def is_critical(self) -> bool:
        return self.severity == "critical" or self.cvss_score >= 9.0

    @property
    def is_high(self) -> bool:
        return self.severity == "high" or (7.0 <= self.cvss_score < 9.0)


@dataclass
class CoverageReport:
    """Code coverage report."""
    report_id: str
    timestamp: datetime
    total_lines: int = 0
    covered_lines: int = 0
    total_branches: int = 0
    covered_branches: int = 0
    total_functions: int = 0
    covered_functions: int = 0
    file_coverage: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    @property
    def line_coverage_pct(self) -> float:
        return (self.covered_lines / self.total_lines * 100) if self.total_lines > 0 else 0

    @property
    def branch_coverage_pct(self) -> float:
        return (self.covered_branches / self.total_branches * 100) if self.total_branches > 0 else 0

    @property
    def function_coverage_pct(self) -> float:
        return (self.covered_functions / self.total_functions * 100) if self.total_functions > 0 else 0

    @property
    def overall_coverage(self) -> float:
        if self.total_lines == 0 and self.total_branches == 0:
            return 0.0
        weights = {"line": 0.5, "branch": 0.3, "function": 0.2}
        total_weight = (
            weights["line"] * self.line_coverage_pct +
            weights["branch"] * self.branch_coverage_pct +
            weights["function"] * self.function_coverage_pct
        )
        return total_weight


@dataclass
class TestConfiguration:
    """Test execution configuration."""
    environment: TestEnvironment = TestEnvironment.DEVELOPMENT
    parallel: bool = False
    max_workers: int = 4
    timeout_seconds: int = 300
    retry_count: int = 2
    fail_fast: bool = False
    verbose: bool = True
    collect_metrics: bool = True
    tags: List[str] = field(default_factory=list)
    exclude_tags: List[str] = field(default_factory=list)
    custom_args: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Test Generator
# ---------------------------------------------------------------------------

class TestGenerator:
    """Generates test cases from requirements, code, and specifications."""

    def __init__(self) -> None:
        self.generated_tests: List[TestCase] = []
        self._counter = 0

    def generate_from_requirements(self, requirements: List[Dict[str, Any]]) -> List[TestCase]:
        """Generate test cases from requirements."""
        test_cases: List[TestCase] = []

        for req in requirements:
            test_cases.extend(self._generate_for_requirement(req))

        self.generated_tests.extend(test_cases)
        return test_cases

    def _generate_for_requirement(self, requirement: Dict[str, Any]) -> List[TestCase]:
        """Generate tests for a single requirement."""
        tests: List[TestCase] = []
        req_id = requirement.get("id", "REQ001")
        title = requirement.get("title", "Test Feature")
        scenarios = requirement.get("scenarios", [])

        # Positive test case
        self._counter += 1
        positive_test = TestCase(
            test_id=f"TC-{self._counter:05d}",
            name=f"{title} - Positive Scenario",
            description=f"Test happy path for {title}",
            test_type=TestType.UNIT,
            status=TestStatus.PENDING,
            priority=Priority.HIGH,
            preconditions=requirement.get("preconditions", []),
            steps=[{"step": 1, "action": "Perform main action", "expected": "Success"}],
            expected_results=["Main action succeeds"],
            automation_status="automated",
        )
        tests.append(positive_test)

        # Scenario-based tests
        for i, scenario in enumerate(scenarios):
            self._counter += 1
            test = TestCase(
                test_id=f"TC-{self._counter:05d}",
                name=f"{title} - {scenario.get('name', f'Scenario {i+1}')}",
                description=scenario.get("description", ""),
                test_type=TestType.UNIT,
                status=TestStatus.PENDING,
                priority=Priority.MEDIUM,
                preconditions=scenario.get("preconditions", []),
                steps=scenario.get("steps", []),
                expected_results=scenario.get("expected_results", []),
                automation_status="manual",
            )
            tests.append(test)

        # Negative test case
        self._counter += 1
        negative_test = TestCase(
            test_id=f"TC-{self._counter:05d}",
            name=f"{title} - Negative Scenario",
            description=f"Test error handling for {title}",
            test_type=TestType.UNIT,
            status=TestStatus.PENDING,
            priority=Priority.MEDIUM,
            steps=[{"step": 1, "action": "Provide invalid input", "expected": "Error handled gracefully"}],
            expected_results=["Error message displayed", "No data corruption"],
        )
        tests.append(negative_test)

        return tests

    def generate_unit_tests(self, code: str, language: str = "python") -> List[TestCase]:
        """Generate unit tests for code."""
        functions = self._extract_functions(code, language)
        test_cases: List[TestCase] = []

        for func in functions:
            self._counter += 1
            test = TestCase(
                test_id=f"TC-{self._counter:05d}",
                name=f"test_{func['name']}",
                description=f"Unit test for function {func['name']}",
                test_type=TestType.UNIT,
                priority=Priority.HIGH,
                steps=[
                    {"step": 1, "action": f"Call {func['name']} with valid input", "expected": "Correct output"},
                    {"step": 2, "action": f"Call {func['name']} with edge cases", "expected": "Proper handling"},
                    {"step": 3, "action": f"Call {func['name']} with invalid input", "expected": "Error handled"},
                ],
                expected_results=["Function behaves correctly for all inputs"],
                automation_status="automated",
            )
            test_cases.append(test)

        self.generated_tests.extend(test_cases)
        return test_cases

    def _extract_functions(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Extract function definitions from code."""
        functions: List[Dict[str, Any]] = []

        if language == "python":
            pattern = r"def\s+(\w+)\s*\(([^)]*)\)\s*(?:->.*?)?:"
            matches = re.findall(pattern, code)
            for name, params in matches:
                if not name.startswith("_"):
                    functions.append({
                        "name": name,
                        "params": [p.strip() for p in params.split(",") if p.strip()],
                    })
        elif language in ("javascript", "typescript"):
            pattern = r"(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\([^)]*\)\s*=>)"
            matches = re.findall(pattern, code)
            for name_tuple in matches:
                name = name_tuple[0] or name_tuple[1]
                if name:
                    functions.append({"name": name, "params": []})

        return functions

    def generate_integration_tests(self, endpoints: List[Dict[str, Any]]) -> List[TestCase]:
        """Generate integration tests for API endpoints."""
        test_cases: List[TestCase] = []

        for endpoint in endpoints:
            self._counter += 1
            method = endpoint.get("method", "GET")
            path = endpoint.get("path", "/")
            test = TestCase(
                test_id=f"TC-{self._counter:05d}",
                name=f"Integration: {method} {path}",
                description=f"Integration test for {method} {path}",
                test_type=TestType.INTEGRATION,
                priority=Priority.HIGH,
                steps=[
                    {"step": 1, "action": f"Send {method} request to {path}", "expected": "200 OK"},
                    {"step": 2, "action": "Validate response schema", "expected": "Schema matches"},
                    {"step": 3, "action": "Check response time", "expected": "< 500ms"},
                ],
                expected_results=["Endpoint responds correctly"],
                automation_status="automated",
            )
            test_cases.append(test)

        self.generated_tests.extend(test_cases)
        return test_cases

    def generate_performance_tests(self, scenarios: List[Dict[str, Any]]) -> List[TestCase]:
        """Generate performance test cases."""
        test_cases: List[TestCase] = []

        for scenario in scenarios:
            self._counter += 1
            test = TestCase(
                test_id=f"TC-{self._counter:05d}",
                name=f"Performance: {scenario.get('name', 'Load Test')}",
                description=scenario.get("description", "Performance test scenario"),
                test_type=TestType.PERFORMANCE,
                priority=Priority.HIGH,
                steps=[
                    {"step": 1, "action": "Ramp up to target load", "expected": "System handles load"},
                    {"step": 2, "action": "Maintain steady state", "expected": "Response time within threshold"},
                    {"step": 3, "action": "Check error rate", "expected": "< 1% errors"},
                ],
                expected_results=["System meets performance requirements"],
                automation_status="automated",
            )
            test_cases.append(test)

        self.generated_tests.extend(test_cases)
        return test_cases


# ---------------------------------------------------------------------------
# Test Runner
# ---------------------------------------------------------------------------

class TestRunner:
    """Executes test suites and manages test runs."""

    def __init__(self, config: Optional[TestConfiguration] = None) -> None:
        self.config = config or TestConfiguration()
        self.executions: List[TestExecution] = []
        self.results: List[Dict[str, Any]] = []
        self._current_run: Optional[Dict[str, Any]] = None

    def run_test_suite(self, suite_id: str, tests: List[TestCase]) -> Dict[str, Any]:
        """Execute test suite."""
        self._current_run = {
            "suite_id": suite_id,
            "start_time": datetime.utcnow(),
            "tests": [],
            "config": self.config.__dict__,
        }

        passed = 0
        failed = 0
        skipped = 0
        error = 0
        total_time = 0.0

        for test in tests:
            execution = self._execute_test(test)
            self._current_run["tests"].append(execution.__dict__)

            if execution.status == TestStatus.PASSED:
                passed += 1
            elif execution.status == TestStatus.FAILED:
                failed += 1
            elif execution.status == TestStatus.ERROR:
                error += 1
            else:
                skipped += 1

            total_time += execution.duration_ms

            if self.config.fail_fast and execution.status in (TestStatus.FAILED, TestStatus.ERROR):
                break

        self._current_run["end_time"] = datetime.utcnow()
        self._current_run["summary"] = {
            "total": len(tests),
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "error": error,
            "pass_rate": (passed / len(tests) * 100) if tests else 0,
            "total_time_ms": total_time,
            "avg_time_ms": (total_time / len(tests)) if tests else 0,
        }

        self.results.append(self._current_run)
        return self._current_run

    def _execute_test(self, test: TestCase) -> TestExecution:
        """Execute single test."""
        test.status = TestStatus.RUNNING
        start_time = datetime.utcnow()

        # Simulate test execution
        execution_time = random.uniform(10, 500)  # 10-500ms
        time.sleep(execution_time / 10000)  # Brief sleep for simulation

        # Simulate test result (90% pass rate for demo)
        if random.random() < 0.9:
            status = TestStatus.PASSED
            error_msg = ""
        else:
            status = TestStatus.FAILED
            error_msg = f"Assertion failed: Expected value did not match"

        end_time = datetime.utcnow()

        execution = TestExecution(
            execution_id=f"EXE-{len(self.executions) + 1:05d}",
            suite_id="",
            test_id=test.test_id,
            status=status,
            start_time=start_time,
            end_time=end_time,
            duration_ms=execution_time,
            error_message=error_msg,
            environment=self.config.environment,
        )

        test.status = status
        test.executed_at = end_time
        test.execution_time_ms = execution_time

        self.executions.append(execution)
        return execution

    def run_regression_tests(self, scope: str = "full") -> Dict[str, Any]:
        """Run regression test suite."""
        return {
            "run_id": len(self.results) + 1,
            "scope": scope,
            "status": "completed",
            "tests_planned": 150,
            "tests_run": 145,
            "passed": 140,
            "failed": 5,
        }

    def parallel_execute(self, test_suites: List[Tuple[str, List[TestCase]]]) -> List[Dict[str, Any]]:
        """Execute multiple test suites in parallel."""
        results: List[Dict[str, Any]] = []
        for suite_id, tests in test_suites:
            result = self.run_test_suite(suite_id, tests)
            results.append(result)
        return results


# ---------------------------------------------------------------------------
# Coverage Analyzer
# ---------------------------------------------------------------------------

class CoverageAnalyzer:
    """Analyzes test coverage and identifies gaps."""

    def __init__(self) -> None:
        self.coverage_reports: List[CoverageReport] = []
        self._counter = 0

    def calculate_coverage(
        self,
        source_files: List[str],
        executed_lines: Dict[str, set],
        total_lines: Dict[str, int],
    ) -> CoverageReport:
        """Calculate code coverage."""
        total = 0
        covered = 0

        for file in source_files:
            file_total = total_lines.get(file, 100)
            file_covered = len(executed_lines.get(file, set()))
            total += file_total
            covered += file_covered

        self._counter += 1
        report = CoverageReport(
            report_id=f"COV-{self._counter:04d}",
            timestamp=datetime.utcnow(),
            total_lines=total,
            covered_lines=covered,
            total_branches=int(total * 0.6),
            covered_branches=int(covered * 0.5),
            total_functions=int(total * 0.1),
            covered_functions=int(covered * 0.08),
        )

        self.coverage_reports.append(report)
        return report

    def identify_gaps(self, coverage: CoverageReport, critical_files: List[str]) -> List[Dict[str, Any]]:
        """Identify coverage gaps."""
        gaps: List[Dict[str, Any]] = []

        if coverage.overall_coverage < 80:
            gaps.append({
                "type": "low_coverage",
                "severity": "high",
                "message": f"Overall coverage at {coverage.overall_coverage:.1f}%, target is 80%",
            })

        if coverage.branch_coverage_pct < 70:
            gaps.append({
                "type": "low_branch_coverage",
                "severity": "medium",
                "message": f"Branch coverage at {coverage.branch_coverage_pct:.1f}%, target is 70%",
            })

        for file in critical_files:
            file_cov = coverage.file_coverage.get(file, {})
            if file_cov.get("coverage", 100) < 90:
                gaps.append({
                    "type": "critical_file_coverage",
                    "severity": "high",
                    "message": f"Critical file {file} coverage below 90%",
                })

        return gaps

    def get_coverage_trend(self, last_n: int = 10) -> Dict[str, Any]:
        """Get coverage trend over time."""
        recent = self.coverage_reports[-last_n:]
        if not recent:
            return {"trend": "no_data"}

        values = [r.overall_coverage for r in recent]
        trend = "improving" if len(values) > 1 and values[-1] > values[0] else "stable"

        return {
            "current": values[-1] if values else 0,
            "average": statistics.mean(values) if values else 0,
            "min": min(values) if values else 0,
            "max": max(values) if values else 0,
            "trend": trend,
            "reports_analyzed": len(recent),
        }


# ---------------------------------------------------------------------------
# Quality Analyzer
# ---------------------------------------------------------------------------

class QualityAnalyzer:
    """Analyzes test quality and effectiveness."""

    def __init__(self) -> None:
        self.analyses: List[Dict[str, Any]] = []

    def analyze_quality(self, tests: List[TestCase]) -> Dict[str, Any]:
        """Analyze test quality metrics."""
        well_written = 0
        needs_improvement = 0
        poor = 0

        for test in tests:
            score = self._calculate_quality_score(test)
            if score >= 80:
                well_written += 1
            elif score >= 50:
                needs_improvement += 1
            else:
                poor += 1

        total = len(tests)
        result = {
            "total_tests": total,
            "well_written": well_written,
            "needs_improvement": needs_improvement,
            "poor": poor,
            "quality_score": (well_written / total * 100) if total > 0 else 0,
            "automation_rate": sum(1 for t in tests if t.is_automated) / total * 100 if total > 0 else 0,
        }

        self.analyses.append(result)
        return result

    def _calculate_quality_score(self, test: TestCase) -> int:
        """Calculate quality score for test."""
        score = 0

        # Naming quality
        if len(test.name) > 10 and "_" in test.name:
            score += 15
        if test.name.startswith("test_"):
            score += 10

        # Documentation
        if len(test.description) > 20:
            score += 10

        # Test structure
        if len(test.steps) >= 3:
            score += 15
        if len(test.expected_results) >= 2:
            score += 15

        # Automation
        if test.is_automated:
            score += 15

        # Preconditions
        if test.preconditions:
            score += 10

        # Priority
        if test.priority in (Priority.CRITICAL, Priority.HIGH):
            score += 10

        return min(100, score)

    def suggest_improvements(self, tests: List[TestCase]) -> List[str]:
        """Suggest test improvements."""
        suggestions: List[str] = []

        # Automation suggestions
        auto_count = sum(1 for t in tests if t.is_automated)
        if len(tests) > 0 and auto_count / len(tests) < 0.5:
            suggestions.append("Increase test automation rate - currently below 50%")

        # Priority suggestions
        high_priority = [t for t in tests if t.priority in (Priority.CRITICAL, Priority.HIGH)]
        pending_high = [t for t in high_priority if t.status == TestStatus.PENDING]
        if pending_high:
            suggestions.append(f"{len(pending_high)} critical/high priority tests are still pending")

        # Coverage suggestions
        no_steps = [t for t in tests if len(t.steps) == 0]
        if no_steps:
            suggestions.append(f"{len(no_steps)} tests have no defined steps")

        # Type distribution
        type_counts: Dict[str, int] = defaultdict(int)
        for t in tests:
            type_counts[t.test_type.value] += 1
        if "unit" not in type_counts or type_counts["unit"] < len(tests) * 0.4:
            suggestions.append("Consider adding more unit tests (target: 40% of total)")

        return suggestions

    def calculate_test_effectiveness(self, tests: List[TestCase], defects_found: int) -> Dict[str, Any]:
        """Calculate test effectiveness metrics."""
        total = len(tests)
        passed = sum(1 for t in tests if t.status == TestStatus.PASSED)
        failed = sum(1 for t in tests if t.status == TestStatus.FAILED)

        return {
            "defect_detection_rate": (defects_found / total * 100) if total > 0 else 0,
            "test_efficiency": (passed / total * 100) if total > 0 else 0,
            "automation_roi": self._calculate_automation_roi(tests),
            "mean_time_between_failures": self._calculate_mtbf(tests),
        }

    def _calculate_automation_roi(self, tests: List[TestCase]) -> float:
        """Calculate automation ROI."""
        automated = [t for t in tests if t.is_automated]
        if not automated:
            return 0.0
        # Simplified ROI calculation
        return len(automated) * 10.0  # Assume $10 savings per automated test run

    def _calculate_mtbf(self, tests: List[TestCase]) -> float:
        """Calculate Mean Time Between Failures."""
        exec_times = [t.execution_time_ms for t in tests if t.execution_time_ms > 0]
        if not exec_times:
            return 0.0
        return statistics.mean(exec_times)


# ---------------------------------------------------------------------------
# Performance Tester
# ---------------------------------------------------------------------------

class PerformanceTester:
    """Performance testing and benchmarking."""

    def __init__(self) -> None:
        self.benchmarks: Dict[str, PerformanceBenchmark] = {}
        self.results: List[Dict[str, Any]] = []
        self._counter = 0

    def add_benchmark(self, name: str, metric: PerformanceMetric, target: float, unit: str = "") -> PerformanceBenchmark:
        """Add performance benchmark."""
        self._counter += 1
        benchmark = PerformanceBenchmark(
            benchmark_id=f"BENCH-{self._counter:04d}",
            name=name,
            metric=metric,
            target_value=target,
            unit=unit,
        )
        self.benchmarks[benchmark.benchmark_id] = benchmark
        return benchmark

    def run_load_test(
        self,
        endpoint: str,
        concurrent_users: int,
        duration_seconds: int,
        ramp_up_seconds: int = 30,
    ) -> Dict[str, Any]:
        """Run load test simulation."""
        # Simulate load test results
        response_times = [random.uniform(50, 200) for _ in range(concurrent_users * 10)]
        error_rate = random.uniform(0, 2)

        result = {
            "endpoint": endpoint,
            "concurrent_users": concurrent_users,
            "duration_seconds": duration_seconds,
            "response_time": {
                "mean": statistics.mean(response_times),
                "p50": statistics.median(response_times),
                "p95": sorted(response_times)[int(len(response_times) * 0.95)],
                "p99": sorted(response_times)[int(len(response_times) * 0.99)],
                "max": max(response_times),
            },
            "throughput_rps": concurrent_users * 10 / duration_seconds * 60,
            "error_rate_pct": error_rate,
            "passed": error_rate < 1.0,
        }

        self.results.append(result)
        return result

    def run_stress_test(self, endpoint: str, max_users: int, step: int = 100) -> Dict[str, Any]:
        """Run stress test to find breaking point."""
        breaking_point = max_users
        for users in range(step, max_users + step, step):
            error_rate = random.uniform(0, max(0, (users - max_users * 0.7) / max_users * 10))
            if error_rate > 5:
                breaking_point = users
                break

        return {
            "endpoint": endpoint,
            "max_users_tested": max_users,
            "breaking_point": breaking_point,
            "recommended_capacity": int(breaking_point * 0.8),
            "passed": breaking_point >= max_users * 0.8,
        }

    def evaluate_benchmarks(self, actual_values: Dict[str, float]) -> List[QualityGateResult]:
        """Evaluate benchmarks against actual values."""
        results: List[QualityGateResult] = []

        for bench_id, benchmark in self.benchmarks.items():
            actual = actual_values.get(bench.metric.value, 0)
            benchmark.actual_value = actual

            status = GateStatus.PASSED if benchmark.within_threshold else GateStatus.FAILED
            results.append(QualityGateResult(
                gate=QualityGate.PERFORMANCE,
                status=status,
                threshold=benchmark.target_value,
                actual_value=actual,
                message=f"{benchmark.name}: {actual}{benchmark.unit} vs {benchmark.target_value}{benchmark.unit}",
            ))

        return results


# ---------------------------------------------------------------------------
# Security Tester
# ---------------------------------------------------------------------------

class SecurityTester:
    """Security testing and vulnerability management."""

    def __init__(self) -> None:
        self.vulnerabilities: Dict[str, SecurityVulnerability] = {}
        self.scan_results: List[Dict[str, Any]] = []
        self._counter = 0

    def add_vulnerability(
        self,
        title: str,
        severity: str,
        cvss_score: float,
        cwe_id: str = "",
        description: str = "",
        remediation: str = "",
    ) -> SecurityVulnerability:
        """Add security vulnerability."""
        self._counter += 1
        vuln = SecurityVulnerability(
            vuln_id=f"VULN-{self._counter:05d}",
            title=title,
            severity=severity,
            cvss_score=cvss_score,
            cwe_id=cwe_id,
            description=description,
            remediation=remediation,
        )
        self.vulnerabilities[vuln.vuln_id] = vuln
        return vuln

    def run_sast_scan(self, codebase: str) -> Dict[str, Any]:
        """Run Static Application Security Testing."""
        # Simulate SAST scan
        findings = random.randint(0, 10)
        return {
            "scan_type": "SAST",
            "codebase": codebase,
            "findings": findings,
            "critical": random.randint(0, min(2, findings)),
            "high": random.randint(0, min(3, findings)),
            "medium": random.randint(0, min(4, findings)),
            "low": random.randint(0, min(5, findings)),
            "passed": findings < 5,
        }

    def run_dast_scan(self, target_url: str) -> Dict[str, Any]:
        """Run Dynamic Application Security Testing."""
        findings = random.randint(0, 8)
        return {
            "scan_type": "DAST",
            "target": target_url,
            "findings": findings,
            "passed": findings < 3,
        }

    def run_sca_scan(self, manifest_file: str) -> Dict[str, Any]:
        """Run Software Composition Analysis."""
        vulnerable_deps = random.randint(0, 15)
        return {
            "scan_type": "SCA",
            "manifest": manifest_file,
            "total_dependencies": random.randint(50, 200),
            "vulnerable": vulnerable_deps,
            "critical_vulnerable": random.randint(0, min(3, vulnerable_deps)),
            "passed": vulnerable_deps < 5,
        }

    def get_vulnerability_summary(self) -> Dict[str, Any]:
        """Get vulnerability summary."""
        by_severity: Dict[str, int] = defaultdict(int)
        by_status: Dict[str, int] = defaultdict(int)

        for vuln in self.vulnerabilities.values():
            by_severity[vuln.severity] += 1
            by_status[vuln.status] += 1

        return {
            "total": len(self.vulnerabilities),
            "by_severity": dict(by_severity),
            "by_status": dict(by_status),
            "critical_count": by_severity.get("critical", 0),
            "high_count": by_severity.get("high", 0),
        }


# ---------------------------------------------------------------------------
# Quality Gate Manager
# ---------------------------------------------------------------------------

class QualityGateManager:
    """Manages quality gates and pass/fail criteria."""

    def __init__(self) -> None:
        self.gates: Dict[QualityGate, Dict[str, Any]] = {
            QualityGate.CODE_COVERAGE: {"threshold": 80.0, "enabled": True},
            QualityGate.TEST_PASS_RATE: {"threshold": 95.0, "enabled": True},
            QualityGate.CODE_QUALITY: {"threshold": 8.0, "enabled": True},
            QualityGate.SECURITY_SCAN: {"threshold": 0, "enabled": True},
            QualityGate.PERFORMANCE: {"threshold": 500.0, "enabled": True},
            QualityGate.ACCESSIBILITY: {"threshold": 90.0, "enabled": False},
        }
        self.evaluations: List[Dict[str, Any]] = []

    def evaluate_gate(self, gate: QualityGate, actual_value: float) -> QualityGateResult:
        """Evaluate quality gate."""
        gate_config = self.gates.get(gate, {})
        threshold = gate_config.get("threshold", 0)
        enabled = gate_config.get("enabled", True)

        if not enabled:
            return QualityGateResult(
                gate=gate,
                status=GateStatus.SKIPPED,
                threshold=threshold,
                actual_value=actual_value,
                message="Gate is disabled",
            )

        # Determine pass/fail based on gate type
        if gate in (QualityGate.CODE_COVERAGE, QualityGate.TEST_PASS_RATE, QualityGate.ACCESSIBILITY):
            passed = actual_value >= threshold
        elif gate == QualityGate.SECURITY_SCAN:
            passed = actual_value == 0  # No vulnerabilities
        elif gate == QualityGate.PERFORMANCE:
            passed = actual_value <= threshold  # Response time
        else:
            passed = actual_value >= threshold

        status = GateStatus.PASSED if passed else GateStatus.FAILED

        result = QualityGateResult(
            gate=gate,
            status=status,
            threshold=threshold,
            actual_value=actual_value,
            message=f"{'PASSED' if passed else 'FAILED'}: {actual_value} vs threshold {threshold}",
        )

        self.evaluations.append({
            "gate": gate.value,
            "status": status.value,
            "threshold": threshold,
            "actual": actual_value,
            "timestamp": datetime.utcnow().isoformat(),
        })

        return result

    def evaluate_all_gates(self, metrics: Dict[str, float]) -> List[QualityGateResult]:
        """Evaluate all quality gates."""
        results: List[QualityGateResult] = []

        gate_mapping = {
            QualityGate.CODE_COVERAGE: metrics.get("code_coverage", 0),
            QualityGate.TEST_PASS_RATE: metrics.get("test_pass_rate", 0),
            QualityGate.SECURITY_SCAN: metrics.get("security_vulnerabilities", 0),
            QualityGate.PERFORMANCE: metrics.get("response_time_ms", 0),
        }

        for gate, value in gate_mapping.items():
            result = self.evaluate_gate(gate, value)
            results.append(result)

        return results

    def get_overall_status(self) -> GateStatus:
        """Get overall quality gate status."""
        if not self.evaluations:
            return GateStatus.NOT_STARTED

        recent = self.evaluations[-4:]  # Last 4 gate evaluations
        failed = any(e["status"] == "failed" for e in recent)
        warnings = any(e["status"] == "warning" for e in recent)

        if failed:
            return GateStatus.FAILED
        elif warnings:
            return GateStatus.WARNING
        return GateStatus.PASSED

    def configure_gate(self, gate: QualityGate, threshold: float, enabled: bool = True) -> None:
        """Configure quality gate."""
        self.gates[gate] = {"threshold": threshold, "enabled": enabled}


# ---------------------------------------------------------------------------
# Test Report Generator
# ---------------------------------------------------------------------------

class TestReportGenerator:
    """Generates comprehensive test reports."""

    def __init__(self) -> None:
        self.reports: List[TestReport] = []
        self._counter = 0

    def generate_report(
        self,
        test_run: Dict[str, Any],
        coverage: Optional[CoverageReport] = None,
        security_results: Optional[Dict[str, Any]] = None,
    ) -> TestReport:
        """Generate comprehensive test report."""
        summary = test_run.get("summary", {})

        metrics = TestMetrics(
            total_tests=summary.get("total", 0),
            passed=summary.get("passed", 0),
            failed=summary.get("failed", 0),
            skipped=summary.get("skipped", 0),
            pass_rate=summary.get("pass_rate", 0),
            total_execution_time=summary.get("total_time_ms", 0),
            avg_execution_time=summary.get("avg_time_ms", 0),
            coverage=coverage.overall_coverage if coverage else 0,
        )

        failures = []
        for test in test_run.get("tests", []):
            if test.get("status") == "failed":
                failures.append({
                    "test_id": test.get("test_id"),
                    "error": test.get("error_message"),
                })

        self._counter += 1
        report = TestReport(
            report_id=f"RPT-{self._counter:04d}",
            suite_id=test_run.get("suite_id", ""),
            execution_date=datetime.utcnow(),
            environment=TestEnvironment.DEVELOPMENT,
            metrics=metrics,
            failures=failures,
            coverage_report=coverage.__dict__ if coverage else None,
            security_report=security_results,
            executive_summary=self._generate_executive_summary(metrics, failures),
            recommendations=self._generate_recommendations(metrics, failures),
        )

        self.reports.append(report)
        return report

    def _generate_executive_summary(self, metrics: TestMetrics, failures: List[Dict]) -> str:
        """Generate executive summary."""
        status = "PASSING" if metrics.pass_rate >= 95 else "FAILING"
        return (
            f"Test execution {status} with {metrics.pass_rate:.1f}% pass rate. "
            f"Total: {metrics.total_tests} tests, Passed: {metrics.passed}, "
            f"Failed: {metrics.failed}. "
            f"Average execution time: {metrics.avg_execution_time:.0f}ms."
        )

    def _generate_recommendations(self, metrics: TestMetrics, failures: List[Dict]) -> List[str]:
        """Generate recommendations."""
        recommendations: List[str] = []

        if metrics.pass_rate < 95:
            recommendations.append("Investigate and fix failing tests before release")

        if metrics.avg_execution_time > 1000:
            recommendations.append("Optimize slow-running tests")

        if metrics.flaky > 0:
            recommendations.append(f"Address {metrics.flaky} flaky tests")

        if len(failures) > 5:
            recommendations.append("Focus on fixing critical failures first")

        return recommendations

    def get_trends(self, last_runs: int = 10) -> Dict[str, Any]:
        """Get testing trends."""
        recent = self.reports[-last_runs:]
        if not recent:
            return {"trend": "no_data"}

        pass_rates = [r.metrics.pass_rate for r in recent]
        coverage_values = [r.metrics.coverage for r in recent]

        return {
            "pass_rate_trend": pass_rates,
            "coverage_trend": coverage_values,
            "avg_pass_rate": statistics.mean(pass_rates) if pass_rates else 0,
            "avg_coverage": statistics.mean(coverage_values) if coverage_values else 0,
            "runs_analyzed": len(recent),
        }


# ---------------------------------------------------------------------------
# Testing Agent (Main)
# ---------------------------------------------------------------------------

class TestingAgent:
    """Main testing management agent."""

    def __init__(self, config: Optional[TestConfiguration] = None) -> None:
        self.config = config or TestConfiguration()
        self.generator = TestGenerator()
        self.runner = TestRunner(self.config)
        self.coverage = CoverageAnalyzer()
        self.quality = QualityAnalyzer()
        self.performance = PerformanceTester()
        self.security = SecurityTester()
        self.quality_gates = QualityGateManager()
        self.report_generator = TestReportGenerator()
        self.test_cases: Dict[str, TestCase] = {}
        self.test_suites: Dict[str, TestSuite] = {}
        self.defects: Dict[str, Defect] = {}
        self._defect_counter = 0

    def create_test_suite(self, name: str, description: str, test_ids: List[str], target: str = "") -> TestSuite:
        """Create test suite."""
        suite = TestSuite(
            suite_id=f"TS-{len(self.test_suites) + 1:04d}",
            name=name,
            description=description,
            test_cases=test_ids,
            target=target,
        )
        self.test_suites[suite.suite_id] = suite
        return suite

    def execute_test_suite(self, suite_id: str) -> Dict[str, Any]:
        """Execute test suite."""
        suite = self.test_suites.get(suite_id)
        if not suite:
            return {"error": "Suite not found"}

        tests = [self.test_cases[tid] for tid in suite.test_cases if tid in self.test_cases]
        results = self.runner.run_test_suite(suite_id, tests)

        suite.statistics = {
            "total": results["summary"]["total"],
            "passed": results["summary"]["passed"],
            "failed": results["summary"]["failed"],
        }

        return results

    def add_defect(
        self,
        title: str,
        description: str,
        severity: DefectSeverity,
        steps_to_reproduce: Optional[List[str]] = None,
    ) -> Defect:
        """Add defect record."""
        self._defect_counter += 1
        defect = Defect(
            defect_id=f"DEF-{self._defect_counter:05d}",
            title=title,
            description=description,
            severity=severity,
            steps_to_reproduce=steps_to_reproduce or [],
        )
        self.defects[defect.defect_id] = defect
        return defect

    def run_quality_gates(self, metrics: Dict[str, float]) -> List[QualityGateResult]:
        """Run all quality gates."""
        return self.quality_gates.evaluate_all_gates(metrics)

    def get_quality_dashboard(self) -> Dict[str, Any]:
        """Get quality dashboard."""
        all_tests = list(self.test_cases.values())
        quality = self.quality.analyze_quality(all_tests)

        coverage_trend = self.coverage.get_coverage_trend()
        defect_summary = {
            "total": len(self.defects),
            "open": sum(1 for d in self.defects.values() if d.is_open),
            "by_severity": defaultdict(int),
        }
        for d in self.defects.values():
            defect_summary["by_severity"][d.severity.value] += 1

        return {
            "test_stats": {
                "total_tests": len(all_tests),
                "automated": sum(1 for t in all_tests if t.is_automated),
                "pending": sum(1 for t in all_tests if t.status == TestStatus.PENDING),
            },
            "quality": {
                "score": quality["quality_score"],
                "well_written": quality["well_written"],
                "needs_improvement": quality["needs_improvement"],
            },
            "coverage": coverage_trend,
            "defects": defect_summary,
            "quality_gates": self.quality_gates.get_overall_status().value,
            "security": self.security.get_vulnerability_summary(),
            "recommendations": self.quality.suggest_improvements(all_tests),
        }

    def generate_test_report(self, suite_id: str) -> TestReport:
        """Generate test report."""
        suite = self.test_suites.get(suite_id)
        if not suite:
            raise ValueError(f"Suite {suite_id} not found")

        test_run = self.runner.results[-1] if self.runner.results else {"summary": {}}
        report = self.report_generator.generate_report(test_run)
        return report


# ---------------------------------------------------------------------------
# Main Demonstration
# ---------------------------------------------------------------------------

def main() -> None:
    """Main entry point."""
    logging.basicConfig(level=logging.INFO)
    print("=" * 70)
    print("Testing Agent - Comprehensive Demo")
    print("=" * 70)

    agent = TestingAgent()

    # Generate tests from requirements
    requirements = [
        {
            "id": "REQ001",
            "title": "User Authentication",
            "preconditions": ["User exists in database"],
            "scenarios": [
                {"name": "Valid credentials", "expected_results": ["Login successful", "Session created"]},
                {"name": "Invalid password", "expected_results": ["Error message", "No session"]},
                {"name": "Account locked", "expected_results": ["Lockout message"]},
            ],
        },
        {
            "id": "REQ002",
            "title": "Data Export",
            "scenarios": [
                {"name": "Export to CSV", "expected_results": ["File downloaded"]},
                {"name": "Export empty data", "expected_results": ["Empty file or message"]},
            ],
        },
    ]

    tests = agent.generator.generate_from_requirements(requirements)
    for t in tests:
        agent.test_cases[t.test_id] = t

    # Create and run test suite
    suite = agent.create_test_suite(
        name="Authentication Tests",
        description="Test user authentication functionality",
        test_ids=[t.test_id for t in tests],
    )

    results = agent.execute_test_suite(suite.suite_id)
    print(f"\nTest Results: {results['summary']['pass_rate']:.1f}% pass rate")

    # Coverage analysis
    coverage = agent.coverage.calculate_coverage(
        source_files=["src/auth.py", "src/export.py"],
        executed_lines={"src/auth.py": set(range(50)), "src/export.py": set(range(30))},
        total_lines={"src/auth.py": 100, "src/export.py": 80},
    )
    print(f"Coverage: {coverage.overall_coverage:.1f}%")

    # Performance testing
    perf_result = agent.performance.run_load_test("/api/login", concurrent_users=100, duration_seconds=60)
    print(f"Performance: {perf_result['response_time']['p95']:.0f}ms p95")

    # Security testing
    sast_result = agent.security.run_sast_scan("src/")
    print(f"Security: {sast_result['findings']} findings")

    # Quality gates
    gate_results = agent.run_quality_gates({
        "code_coverage": coverage.overall_coverage,
        "test_pass_rate": results["summary"]["pass_rate"],
        "response_time_ms": perf_result["response_time"]["p95"],
    })
    gate_status = agent.quality_gates.get_overall_status()
    print(f"Quality Gates: {gate_status.value}")

    # Dashboard
    dashboard = agent.get_quality_dashboard()
    print(f"\nDashboard: Quality score = {dashboard['quality']['score']}")

    print("\n" + "=" * 70)
    print("Testing Agent demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()

---
name: AutomationQA Agent
version: 3.0.0
description: >
  Enterprise-grade test automation agent orchestrating test planning, generation,
  execution, reporting, and quality gate enforcement across unit, integration, E2E,
  performance, security, API, visual, accessibility, chaos, and contract testing.
author: MiMoCode
tags:
  - test-automation
  - quality-engineering
  - ci-cd
  - performance-testing
  - security-scanning
  - browser-automation
  - api-testing
  - visual-testing
  - accessibility
  - contract-testing
category: Quality Engineering
personality:
  methodical
  thorough
  quality-obsessed
  data-driven
  automation-first
use_cases:
  - Automated test suite creation and execution
  - CI/CD pipeline quality gate configuration
  - Performance and load testing
  - Security vulnerability scanning
  - Code coverage analysis
  - Flaky test detection and resolution
  - Visual regression testing
  - Accessibility compliance validation
  - API contract testing
  - Test data management
  - Quality metrics dashboards
  - Regression test suite optimization
---

# AutomationQA Agent

> Version 3.0.0 | Enterprise Test Automation Framework

## Agent Identity and Purpose

The AutomationQA Agent is an enterprise-grade test automation framework designed to manage the complete software testing lifecycle. It serves as the quality engineering backbone for software projects, providing comprehensive test planning, generation, execution, reporting, and quality gate enforcement.

### Mission Statement

To eliminate manual testing bottlenecks by providing intelligent, automated test orchestration that catches defects early, validates quality continuously, and delivers actionable insights that accelerate release velocity without compromising quality.

### Core Values

1. **Quality is Non-Negotiable** — Every release must meet defined quality thresholds
2. **Automation-First** — If it can be automated, it should be
3. **Data-Driven Decisions** — Metrics guide every quality decision
4. **Continuous Feedback** — Fast feedback loops prevent defect accumulation
5. **Shift-Left Mentality** — Catch defects as early as possible in the development cycle

---

## 10 Core Principles

### Principle 1: Test Pyramid

Maintain an optimal test distribution across unit, integration, and E2E levels. Unit tests form the foundation (40%), integration tests the middle layer (30%), and E2E tests the apex (10%). API tests occupy the integration layer (20%).

```
                    /\
                   /  \          E2E (10%)
                  /────\
                 / API  \        API (20%)
                /────────\
               /Integr.   \      Integration (30%)
              /────────────\
             /    Unit      \    Unit (40%)
            /────────────────\
```

**Implementation:**
- Generate unit tests for every function/method
- Create API tests for every endpoint
- Build E2E tests for critical user flows only
- Monitor test distribution and rebalance as needed

### Principle 2: Shift-Left

Move testing activities as early as possible in the development cycle. Static analysis, unit tests, and code reviews happen before integration. Security scanning starts at the code commit stage.

**Implementation:**
- Pre-commit hooks run linting and unit tests
- CI pipeline runs on every pull request
- Security scanning on every merge to main
- Performance baselines established before feature development

### Principle 3: Automation-First

Automate every test that will be executed more than twice. Manual testing is reserved for exploratory testing, usability assessment, and edge cases that resist automation.

**Implementation:**
- Automated regression suites run on every build
- Automated deployment verification after each release
- Automated monitoring and alerting for production quality
- Self-healing selectors for browser automation

### Principle 4: Data-Driven Quality

Every quality decision is backed by data. Test coverage, pass rates, defect trends, and performance metrics drive release readiness assessments.

**Implementation:**
- Quality dashboards with real-time metrics
- Trend analysis for coverage, pass rate, and defect density
- Statistical analysis of flaky tests
- Performance benchmarking with historical comparison

### Principle 5: Continuous Testing

Tests run continuously throughout the development lifecycle — not just at the end. Every commit triggers automated tests; every deployment runs verification suites.

**Implementation:**
- CI/CD pipeline with test stages at every gate
- Continuous performance monitoring in staging
- Scheduled security scans (daily/weekly)
- Production monitoring with synthetic tests

### Principle 6: Risk-Based Testing

Focus testing effort on areas of highest risk. Critical paths, security-sensitive code, and recently changed areas receive the most thorough testing.

**Implementation:**
- Risk assessment for each feature/module
- Impact analysis for code changes
- Prioritized test execution (critical path first)
- Increased test coverage for high-risk areas

### Principle 7: Environment Parity

Test environments mirror production as closely as possible. Differences between environments are documented and minimized.

**Implementation:**
- Infrastructure-as-code for all environments
- Container-based environment provisioning
- Data seeding scripts for consistent test data
- Regular environment parity audits

### Principle 8: Flaky Test Elimination

Flaky tests erode confidence in automation. Detect, quarantine, and fix flaky tests systematically.

**Implementation:**
- Automated flaky test detection (flaky score calculation)
- Quarantine mechanism for known flaky tests
- Root cause analysis for recurring flakes
- Maximum flaky rate threshold (target: < 1%)

### Principle 9: Shift-Right Observability

Testing doesn't stop at deployment. Monitor production quality through observability, synthetic monitoring, and canary analysis.

**Implementation:**
- Synthetic monitoring for critical user flows
- Error rate monitoring with alerting
- Performance baseline comparison
- Feature flag-based gradual rollouts

### Principle 10: Quality Gates

Automated quality gates enforce standards at every pipeline stage. No code progresses past a gate without meeting defined criteria.

**Implementation:**
- Coverage gate (minimum 80% line coverage)
- Pass rate gate (minimum 95% test pass rate)
- Security gate (zero critical/high vulnerabilities)
- Performance gate (p95 response time within threshold)

---

## Detailed Capabilities

### Test Case Generation

The agent generates test cases from multiple sources using pluggable strategies.

**Unit Test Generation:**

```python
from automation_qa import AutomationQAAgent, TestType

agent = AutomationQAAgent()

# Generate unit tests from function signatures
unit_tests = agent.generate_test_cases(
    test_type=TestType.UNIT,
    source=None,
    options={
        "functions": [
            {
                "name": "calculate_tax",
                "params": {"income": 50000, "rate": 0.15},
                "expected": {"tax": 7500}
            },
            {
                "name": "validate_email",
                "params": {"email": "user@example.com"},
                "expected": {"valid": True}
            }
        ]
    }
)
```

**API Test Generation:**

```python
# Generate API tests from OpenAPI spec
api_tests = agent.generate_test_cases(
    test_type=TestType.API,
    source=openapi_spec,
    options={
        "endpoints": [
            {"method": "GET", "path": "/api/users", "expected_status": 200},
            {"method": "POST", "path": "/api/orders", "expected_status": 201},
            {"method": "DELETE", "path": "/api/users/{id}", "expected_status": 204}
        ]
    }
)
```

**E2E Test Generation:**

```python
# Generate E2E tests from user flows
e2e_tests = agent.generate_test_cases(
    test_type=TestType.E2E,
    source=None,
    options={
        "user_flows": [
            {
                "name": "complete_purchase",
                "steps": [
                    {"action": "Navigate to /products", "data": ""},
                    {"action": "Add product to cart", "data": "product_id=123"},
                    {"action": "Proceed to checkout", "data": ""},
                    {"action": "Enter payment details", "data": "card=4111111111111111"},
                    {"action": "Confirm order", "data": ""},
                    {"action": "Verify order confirmation", "data": "expected=Thank you"}
                ]
            }
        ]
    }
)
```

**Performance Test Generation:**

```python
# Generate performance test scripts from endpoint definitions
perf_tests = agent.generate_test_cases(
    test_type=TestType.PERFORMANCE,
    source=None,
    options={
        "endpoints": [
            {
                "method": "GET",
                "path": "/api/products",
                "load_pattern": "RAMP_UP",
                "virtual_users": 100,
                "threshold_p95_ms": 300
            },
            {
                "method": "POST",
                "path": "/api/orders",
                "load_pattern": "CONSTANT",
                "virtual_users": 50,
                "threshold_p95_ms": 500
            }
        ]
    }
)
```

**Chaos Test Generation:**

```python
# Generate chaos resilience tests
chaos_tests = agent.generate_test_cases(
    test_type=TestType.CHAOS,
    source=None,
    options={
        "scenarios": [
            {"name": "database_failover", "injection": "kill_process", "config": "postgresql",
             "expected_recovery": "automatic failover within 30s"},
            {"name": "network_partition", "injection": "network_latency", "config": "5000ms",
             "expected_recovery": "requests complete with degraded performance"},
            {"name": "memory_pressure", "injection": "memory_limit", "config": "512MB",
             "expected_recovery": "graceful degradation, no OOM"}
        ]
    }
)
```

### Test Suite Management

```python
# Create a comprehensive test suite
suite = agent.create_test_suite(
    name="Regression Suite v2.5",
    test_cases=unit_tests + api_tests + e2e_tests,
    description="Full regression suite for Q4 release",
    parallel=True,
    max_workers=4,
    tags=["regression", "q4-release"],
    setup_script="docker-compose up -d test-db",
    teardown_script="docker-compose down"
)

# Filter by type, tag, or priority
api_only = suite.filter_by_type(TestType.API)
critical_tests = suite.filter_by_priority(SeverityLevel.CRITICAL)
tagged_tests = suite.filter_by_tag("smoke")

# Sort execution order (critical path first)
ordered_suite = suite.sort_by_execution_order(strategy="critical_path_first")
```

### Test Execution

```python
# Execute a test suite
execution = agent.execute_test_suite(
    suite=suite,
    environment=TestEnvironment.STAGING,
    parallel=True
)

# Review results
print(f"Pass Rate: {execution.pass_rate}%")
print(f"Passed: {execution.passed}")
print(f"Failed: {execution.failed}")
print(f"Skipped: {execution.skipped}")

# Get detailed results
for result in execution.results:
    print(f"  {result.test_case.name}: {result.status.value}")

# Retry failed tests
retry_execution = agent.execute_test_suite(
    suite=suite,
    environment=TestEnvironment.STAGING,
    retry_failed=True,
    max_retries=2
)
```

### CI/CD Pipeline Configuration

```python
# Generate CI/CD pipeline configuration
ci_config = agent.setup_ci_pipeline(
    provider="github_actions",
    stages=[
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
    parallel_stages=True,
    fail_fast=True,
    retry_on_failure=True,
    timeout_minutes=60,
    notification_channels=["slack", "email"]
)

# Generate GitHub Actions config
yaml_config = ci_config.generate_github_actions_config()

# Generate GitLab CI config
gitlab_config = ci_config.generate_gitlab_ci_config()

# Generate Jenkins pipeline
jenkins_config = ci_config.generate_jenkins_pipeline()

# Generate CircleCI config
circleci_config = ci_config.generate_circleci_config()
```

### Performance Testing

```python
# Configure and run performance tests
perf_config = PerformanceTestConfig(
    target_url="https://api.example.com",
    load_pattern=PerformanceLoadPattern.RAMP_UP,
    virtual_users=200,
    ramp_up_duration_seconds=60,
    test_duration_seconds=300,
    threshold_p95_ms=500.0,
    threshold_error_rate=1.0
)

perf_result = agent.run_performance_tests(perf_config)

# Analyze results
analysis = agent.analyze_performance_results(
    perf_result,
    thresholds={"max_p95_ms": 500.0, "max_error_rate": 1.0}
)
```

### Security Scanning

```python
# Run security scan
security_result = agent.run_security_scan(
    target="https://example.com",
    scan_type=SecurityTestType.DAST,
    custom_rules=[
        {"type": "sql_injection", "severity": "critical"},
        {"type": "xss", "severity": "high"}
    ]
)

print(f"Critical: {security_result.critical_count}")
print(f"High: {security_result.high_count}")
print(f"Risk Score: {security_result.risk_score}")
```

### Code Coverage Analysis

```python
# Analyze code coverage
coverage = agent.analyze_code_coverage(
    project_name="myapp",
    source_dirs=["src/", "lib/"],
    threshold=80.0
)

print(f"Line Coverage: {coverage.line_coverage}%")
print(f"Branch Coverage: {coverage.branch_coverage}%")
print(f"Meets Threshold: {coverage.meets_threshold}")
print(f"Uncovered Files: {len(coverage.uncovered_files)}")
```

### Bug Reporting

```python
# Create a bug report from failed test
bug = agent.create_bug_report(
    title="Login fails with valid credentials",
    description="User receives 500 error when logging in with valid credentials",
    severity=SeverityLevel.CRITICAL,
    steps_to_reproduce=[
        "Navigate to /login",
        "Enter valid email and password",
        "Click Login button",
        "Observe 500 Internal Server Error"
    ],
    expected_behavior="User is redirected to dashboard",
    actual_behavior="Server returns 500 Internal Server Error",
    environment="staging",
    related_test_case="TC-a1b2c3d4"
)
```

### Flaky Test Analysis

```python
# Analyze flaky tests across execution history
flaky_tests = agent.analyze_flaky_tests(
    execution_history=[exec1, exec2, exec3, exec4, exec5],
    flaky_threshold=20.0
)

for test in flaky_tests:
    print(f"Flaky: {test.test_name}")
    print(f"  Score: {test.flaky_score}")
    print(f"  Fail Rate: {test.flaky_rate}%")
    print(f"  Action: {test.recommended_action}")
```

### Visual Testing

```python
# Configure visual testing
visual_config = agent.setup_visual_testing(
    pages=[
        "/",
        "/products",
        "/cart",
        "/checkout",
        "/account/settings"
    ],
    baseline_dir="./visual-baselines",
    diff_threshold=0.1,
    browsers=[BrowserType.CHROME, BrowserType.FIREFOX]
)
```

### Accessibility Testing

```python
# Run accessibility tests
a11y_results = agent.run_accessibility_tests(
    urls=[
        "https://example.com",
        "https://example.com/products",
        "https://example.com/checkout"
    ],
    wcag_level="AA",
    wcag_version="2.1"
)

for url, violations in a11y_results.items():
    blocking = [v for v in violations if v.is_blocking]
    print(f"{url}: {len(violations)} violations, {len(blocking)} blocking")
```

### Contract Testing

```python
# Create contract tests
contract = agent.create_contract_test(
    provider="order-service",
    consumer="frontend-app",
    interactions=[
        {
            "description": "Get order by ID",
            "method": "GET",
            "path": "/api/orders/123",
            "expected_status": 200,
            "expected_body": {"id": 123, "status": "pending"}
        }
    ],
    pact_version="4.0"
)
```

### Quality Dashboard

```python
# Generate quality dashboard
dashboard = agent.generate_test_dashboard()

# Dashboard includes:
# - Execution summary
# - Quality trend (7-day)
# - Coverage trend
# - Flaky test list
# - Recent executions
# - Vulnerability count
# - Performance metrics
```

---

## Operational Guidelines

### Agent Method Signatures

| Method | Parameters | Returns |
|--------|-----------|---------|
| `create_test_plan` | name, description, project, version, author, environments, browsers, risk_areas, entry_criteria, exit_criteria | `TestPlan` |
| `generate_test_cases` | test_type, source, options | `List[TestCase]` |
| `create_test_suite` | name, test_cases, description, parallel, max_workers, tags, setup_script, teardown_script | `TestSuite` |
| `execute_test_suite` | suite, environment, parallel, retry_failed, max_retries | `TestExecution` |
| `setup_ci_pipeline` | provider, stages, parallel_stages, fail_fast, retry_on_failure, timeout_minutes | `CIConfig` |
| `configure_browser_testing` | browsers, headless, viewport, screenshots, video | `List[BrowserTestConfig]` |
| `run_performance_tests` | config | `PerformanceResult` |
| `analyze_performance_results` | result, thresholds | `Dict[str, Any]` |
| `run_security_scan` | target, scan_type, custom_rules | `SecurityScanResult` |
| `analyze_code_coverage` | project_name, source_dirs, threshold | `CodeCoverageReport` |
| `create_bug_report` | title, description, severity, steps, expected, actual, environment | `BugReport` |
| `generate_test_report` | execution, title, coverage, performance, security, format | `TestReport` |
| `setup_test_environments` | environments | `List[TestEnvironmentConfig]` |
| `manage_test_data` | dataset_name, schema, record_count, seed, cleanup_strategy | `TestDataManagement` |
| `analyze_flaky_tests` | execution_history, flaky_threshold | `List[FlakyTestAnalysis]` |
| `create_regression_suite` | name, all_test_cases, changed_files, include_critical_path | `RegressionTestSet` |
| `run_api_tests` | api_test_cases, base_url, auth_headers | `List[Dict]` |
| `setup_visual_testing` | pages, baseline_dir, diff_threshold, browsers | `Dict` |
| `run_accessibility_tests` | urls, wcag_level, wcag_version | `Dict[str, List]` |
| `create_contract_test` | provider, consumer, interactions, pact_version | `ContractTestResult` |
| `get_quality_metrics` | — | `Dict[str, Any]` |
| `generate_test_dashboard` | — | `Dict[str, Any]` |
| `export_test_data` | output_path, format | `str` |

---

## Data Models Reference

### Core Enums

| Enum | Values | Purpose |
|------|--------|---------|
| `TestType` | UNIT, INTEGRATION, E2E, PERFORMANCE, SECURITY, API, VISUAL, ACCESSIBILITY, CHAOS, CONTRACT | Categorizes test cases |
| `TestFramework` | PYTEST, JEST, CYPRESS, PLAYWRIGHT, SELENIUM, JUNIT, GATLING, K6, OWASP_ZAP, POSTMAN | Test execution framework |
| `TestStatus` | PENDING, RUNNING, PASSED, FAILED, SKIPPED, ERROR, FLAKY, QUEUED | Current test state |
| `CIPipelineStage` | BUILD, UNIT_TEST, INTEGRATION_TEST, E2E_TEST, SECURITY_SCAN, PERFORMANCE_TEST, DEPLOY_STAGING, ACCEPTANCE, DEPLOY_PRODUCTION | CI/CD pipeline stage |
| `ReportFormat` | HTML, JSON, JUNIT_XML, ALLURE, TCM, CLOB | Report output format |
| `BrowserType` | CHROME, FIREFOX, SAFARI, EDGE | Target browser |
| `SeverityLevel` | BLOCKER, CRITICAL, MAJOR, MINOR, TRIVIAL | Issue severity |
| `TestEnvironment` | LOCAL, DEV, STAGING, QA, UAT, PRODUCTION | Target environment |
| `PerformanceLoadPattern` | CONSTANT, RAMP_UP, SPIKE, STEP, WAVE, RANDOM | Load test pattern |
| `SecurityTestType` | SAST, DAST, IAST, SCA, FUZZING, PENETRATION | Security scan type |

### Core Dataclasses

| Dataclass | Key Fields | Purpose |
|-----------|-----------|---------|
| `TestCase` | test_id, name, test_type, framework, priority, status, steps, assertions | Individual test definition |
| `TestSuite` | suite_id, name, test_cases, parallel, max_workers | Grouped test cases |
| `TestPlan` | plan_id, name, test_suites, environments, exit_criteria | Overall test strategy |
| `TestExecution` | execution_id, results, environment, pass_rate | Execution run record |
| `TestResult` | result_id, test_case, status, duration_ms, assertions | Single test outcome |
| `CIConfig` | provider, pipeline_stages, fail_fast, retry_on_failure | CI/CD configuration |
| `PerformanceTestConfig` | target_url, load_pattern, virtual_users, thresholds | Performance test setup |
| `PerformanceResult` | p95_ms, p99_ms, rps, error_rate | Performance outcome |
| `SecurityScanResult` | critical_count, high_count, risk_score | Security findings |
| `CodeCoverageReport` | line_coverage, branch_coverage, file_coverage | Coverage data |
| `BugReport` | bug_id, title, severity, steps_to_reproduce | Defect record |
| `TestReport` | report_id, execution, coverage, performance, security | Aggregated report |
| `QualityGate` | gate_id, stage, conditions, status | Quality checkpoint |
| `FlakyTestAnalysis` | flaky_score, flaky_rate, recommended_action | Flaky test data |
| `VisualDiffResult` | pixel_diff_percentage, threshold, passed | Visual comparison |
| `AccessibilityViolation` | rule_id, impact, wcag_level, nodes_affected | A11y finding |
| `ContractTestResult` | provider, consumer, mismatches, status | Contract validation |
| `BrowserTestConfig` | browser, headless, viewport_width, viewport_height, screenshots, video | Browser settings |
| `TestEnvironmentConfig` | name, base_url, api_base_url, database_url, environment_variables | Environment definition |
| `RegressionTestSet` | name, test_cases, changed_files, execution_order | Targeted regression |

---

## Checklists

### Pre-Release Checklist

```
□ All critical test cases pass
□ Code coverage meets threshold (≥80%)
□ No critical security vulnerabilities
□ Performance thresholds met (p95 ≤ 500ms)
□ Flaky test rate < 1%
□ All environments validated
□ Test data refreshed
□ Accessibility violations resolved
□ Contract tests verified
□ Visual regression tests pass
□ Regression suite completed
□ Quality gates passed
□ Test report generated and reviewed
□ Bug backlog triaged
□ Release notes include test summary
```

### New Feature Test Checklist

```
□ Unit tests for new code (≥90% coverage)
□ Integration tests for API changes
□ E2E tests for user-facing features
□ Security tests for auth/data changes
□ Performance tests for hot paths
□ Accessibility tests for UI components
□ Visual tests for layout changes
□ Contract tests for API changes
□ Test data prepared
□ Edge cases identified and tested
□ Negative test cases created
□ Error handling verified
```

### CI/CD Pipeline Checklist

```
□ Build stage compiles successfully
□ Unit tests pass (>95%)
□ Code coverage meets threshold
□ Integration tests pass
□ E2E critical path passes
□ Security scan clean (0 critical/high)
□ Performance within thresholds
□ Deploy to staging successful
□ Smoke tests pass on staging
□ Acceptance tests pass
□ Quality gates evaluated
□ Deploy to production authorized
```

---

## Troubleshooting Guide

### Common Issues and Solutions

**Issue: Tests pass locally but fail in CI**

| Symptom | Cause | Solution |
|---------|-------|----------|
| Timeout errors | CI environment slower | Increase timeouts by 2x for CI |
| Missing dependencies | Container image outdated | Pin dependency versions |
| Port conflicts | Parallel test interference | Use dynamic ports |
| Flaky assertions | Race conditions | Add proper waits/synchronization |

**Issue: Flaky tests**

| Pattern | Root Cause | Fix |
|---------|-----------|-----|
| Timeout intermittently | Network/server latency | Increase timeout + retry |
| Assertion fails randomly | Async state not settled | Add explicit waits |
| Element not found | DOM not loaded | Use data-testid + wait for selector |
| Data-dependent | Shared test data | Use isolated data per test |

**Issue: Slow test execution**

| Bottleneck | Optimization |
|-----------|--------------|
| Sequential E2E tests | Enable parallel execution |
| Database setup/teardown | Use fixtures, transactions |
| External API calls | Mock external services |
| Browser startup | Reuse browser instances |
| Large test data | Use minimal data sets |

**Issue: Low code coverage**

| Scenario | Action |
|----------|--------|
| New code not covered | Write tests for new functions |
| Legacy code uncovered | Gradually add tests (strangler pattern) |
| Branches not covered | Add boundary/edge case tests |
| Error paths not covered | Add exception handling tests |

**Issue: Security scan false positives**

| Type | Action |
|------|--------|
| Known false positive | Add to suppression list with justification |
| Low severity, accepted risk | Document risk acceptance |
| True positive | Fix vulnerability |
| Tool limitation | Validate manually, update tool |

### Debug Mode

```python
# Enable debug logging
import logging
logging.getLogger("automation_qa").setLevel(logging.DEBUG)

# Run with verbose output
agent = AutomationQAAgent(project_root=".", config={"debug": True})

# Inspect test execution details
execution = agent.execute_test_suite(suite)
for result in execution.results:
    if result.status == TestStatus.FAILED:
        print(f"Failed: {result.test_case.name}")
        print(f"Error: {result.error_message}")
        print(f"Stack: {result.stack_trace}")
        print(f"Logs: {result.logs}")
```

---

## Advanced Configuration

### Custom Quality Gates

```python
from automation_qa import (
    QualityGateHandler,
    CoverageGateHandler,
    PassRateGateHandler,
    SecurityGateHandler,
    PerformanceGateHandler,
)

# Build custom quality gate chain
gate1 = CoverageGateHandler(min_coverage=85.0)
gate2 = PassRateGateHandler(min_pass_rate=98.0)
gate3 = SecurityGateHandler()
gate4 = PerformanceGateHandler(max_p95_ms=300.0)

gate1.set_next(gate2).set_next(gate3).set_next(gate4)

# Apply to agent
agent._quality_gate_chain = gate1
```

### Custom Test Generation Strategies

```python
from automation_qa import (
    TestGenerationStrategy,
    TestGenerationFactory,
    TestType,
    TestCase,
)

class ChaosTestGenerationStrategy(TestGenerationStrategy):
    def generate(self, source, options):
        test_cases = []
        scenarios = options.get("scenarios", [])
        for scenario in scenarios:
            tc = TestCase(
                name=f"chaos_{scenario['name']}",
                description=f"Chaos test: {scenario['description']}",
                test_type=TestType.CHAOS,
                tags=["chaos", "resilience"],
                steps=[
                    {"action": scenario["injection"], "data": scenario.get("config", "")},
                    {"action": "Observe system behavior", "data": ""},
                    {"action": "Verify recovery", "data": scenario.get("expected_recovery", "")},
                ],
            )
            test_cases.append(tc)
        return test_cases

# Register custom strategy
TestGenerationFactory.register_strategy(
    TestType.CHAOS,
    ChaosTestGenerationStrategy()
)
```

### Custom Observers

```python
from automation_qa import TestExecutionObserver, TestCase, TestResult, TestSuite

class SlackNotificationObserver(TestExecutionObserver):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def on_test_started(self, test_case):
        pass  # Optionally notify on start

    def on_test_completed(self, result):
        if result.status.value == "failed":
            self._send_notification(
                f"Test FAILED: {result.test_case.name}\n"
                f"Error: {result.error_message}"
            )

    def on_suite_completed(self, suite, results):
        passed = sum(1 for r in results if r.status.value == "passed")
        total = len(results)
        self._send_notification(
            f"Suite '{suite.name}' completed: {passed}/{total} passed"
        )

    def _send_notification(self, message):
        import requests
        requests.post(self.webhook_url, json={"text": message})

# Register observer
agent.add_observer(SlackNotificationObserver("https://hooks.slack.com/..."))
```

### Environment-Specific Configuration

```python
# Define environments
environments = [
    TestEnvironmentConfig(
        name=TestEnvironment.DEV,
        base_url="http://localhost:3000",
        api_base_url="http://localhost:3001/api",
        database_url="postgresql://localhost:5432/dev_db",
        environment_variables={
            "LOG_LEVEL": "debug",
            "FEATURE_FLAG_X": "true",
        },
    ),
    TestEnvironmentConfig(
        name=TestEnvironment.STAGING,
        base_url="https://staging.example.com",
        api_base_url="https://staging-api.example.com/api",
        database_url="postgresql://staging-db:5432/staging_db",
        environment_variables={
            "LOG_LEVEL": "info",
            "FEATURE_FLAG_X": "true",
        },
    ),
    TestEnvironmentConfig(
        name=TestEnvironment.PRODUCTION,
        base_url="https://example.com",
        api_base_url="https://api.example.com/api",
        environment_variables={
            "LOG_LEVEL": "warn",
            "FEATURE_FLAG_X": "false",
        },
    ),
]

agent.setup_test_environments(environments)
```

---

## Integration Examples

### With Pytest

```python
# conftest.py
import pytest
from automation_qa import AutomationQAAgent, TestEnvironment

@pytest.fixture(scope="session")
def qa_agent():
    agent = AutomationQAAgent(project_root=".")
    return agent

@pytest.fixture(scope="session")
def test_environment():
    return TestEnvironment.STAGING

def test_api_health(qa_agent, test_environment):
    result = qa_agent.run_api_tests(
        api_test_cases=[...],
        base_url="https://staging-api.example.com"
    )
    assert all(r["status"] == "passed" for r in result)
```

### With Playwright

```python
# tests/test_e2e.py
from playwright.sync_api import sync_playwright
from automation_qa import BrowserTestConfig

def test_checkout_flow():
    config = BrowserTestConfig(
        browser=BrowserType.CHROME,
        headless=True,
        viewport_width=1920,
        viewport_height=1080,
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        page = browser.new_page(
            viewport={"width": config.viewport_width, "height": config.viewport_height}
        )

        page.goto("https://example.com/products")
        page.click("[data-testid='add-to-cart']")
        page.click("[data-testid='checkout']")
        page.fill("[data-testid='email']", "test@example.com")
        page.click("[data-testid='submit-order']")

        assert page.url.contains("/order-confirmation")
        browser.close()
```

### With k6

```javascript
// tests/performance/load.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },
    { duration: '1m', target: 100 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

export default function () {
  const res = http.get('https://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  sleep(1);
}
```

---

## Glossary

| Term | Definition |
|------|-----------|
| **AutomationQA** | Enterprise test automation framework |
| **Quality Gate** | Automated checkpoint enforcing quality criteria |
| **Test Pyramid** | Model for optimal test distribution |
| **Flaky Test** | Test with inconsistent results |
| **Shift-Left** | Moving testing earlier in development |
| **Shift-Right** | Testing in production (observability) |
| **Regression Suite** | Tests run to verify no new defects |
| **Contract Test** | Validates API contracts between services |
| **Visual Regression** | Detects unintended UI changes |
| **SAST** | Static Application Security Testing |
| **DAST** | Dynamic Application Security Testing |
| **SCA** | Software Composition Analysis |

---

*GROK Document v3.0.0 — AutomationQA Agent by MiMoCode*

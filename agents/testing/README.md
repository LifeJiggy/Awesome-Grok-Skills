# Testing Agent

> Comprehensive software testing platform for ensuring code quality through automated testing, performance validation, security scanning, and quality gates.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The Testing Agent provides a complete software testing toolkit covering:

- **Test Generation**: Automated test creation from requirements and code
- **Test Automation**: Execute tests across multiple frameworks
- **Performance Testing**: Load, stress, and endurance testing
- **Security Testing**: SAST, DAST, and SCA scanning
- **Coverage Analysis**: Code coverage tracking and gap identification
- **Quality Gates**: Automated pass/fail criteria enforcement
- **Defect Tracking**: Bug lifecycle management
- **Test Reporting**: Comprehensive test execution reports

---

## Features

### Test Generation
- Generate tests from requirements
- Unit test generation from code
- Integration test generation for APIs
- Performance test scenario creation

### Test Automation
- Parallel test execution
- Retry mechanisms for flaky tests
- Environment-specific configurations
- CI/CD integration support

### Performance Testing
- Load testing with configurable patterns
- Stress testing to find breaking points
- Response time and throughput metrics
- Resource utilization monitoring

### Security Testing
- Static Application Security Testing (SAST)
- Dynamic Application Security Testing (DAST)
- Software Composition Analysis (SCA)
- Vulnerability tracking and management

### Quality Gates
- Configurable thresholds
- Multi-gate evaluation
- Historical trend tracking
- CI/CD pipeline blocking

---

## Quick Start

### Installation

```python
# No external dependencies required - pure Python implementation
from agents.testing.agent import TestingAgent
```

### Basic Usage

```python
from agents.testing.agent import TestingAgent

# Initialize agent
agent = TestingAgent()

# Generate tests from requirements
requirements = [
    {
        "id": "REQ001",
        "title": "User Login",
        "scenarios": [
            {"name": "Valid credentials", "expected_results": ["Login successful"]},
        ]
    }
]

tests = agent.generator.generate_from_requirements(requirements)

# Create and run test suite
suite = agent.create_test_suite(
    name="Login Tests",
    description="Test login functionality",
    test_ids=[t.test_id for t in tests]
)

results = agent.execute_test_suite(suite.suite_id)
print(f"Pass rate: {results['summary']['pass_rate']:.1f}%")
```

### Run the Demo

```bash
python agents/testing/agent.py
```

---

## Usage

### Test Generation

```python
from agents.testing.agent import TestingAgent

agent = TestingAgent()

# Generate from requirements
tests = agent.generator.generate_from_requirements(requirements)

# Generate from code
code = """
def calculate_total(items):
    return sum(item['price'] * item['qty'] for item in items)
"""
unit_tests = agent.generator.generate_unit_tests(code, language="python")

# Generate integration tests
endpoints = [
    {"method": "GET", "path": "/api/users"},
    {"method": "POST", "path": "/api/users"},
]
api_tests = agent.generator.generate_integration_tests(endpoints)
```

### Test Execution

```python
from agents.testing.agent import TestConfiguration, TestEnvironment

# Configure execution
config = TestConfiguration(
    environment=TestEnvironment.STAGING,
    parallel=True,
    max_workers=4,
    retry_count=2,
    fail_fast=True,
)

agent = TestingAgent(config)

# Run tests
results = agent.execute_test_suite(suite.suite_id)

# Check results
print(f"Total: {results['summary']['total']}")
print(f"Passed: {results['summary']['passed']}")
print(f"Failed: {results['summary']['failed']}")
print(f"Pass rate: {results['summary']['pass_rate']:.1f}%")
```

### Coverage Analysis

```python
from agents.testing.agent import CoverageAnalyzer

coverage = CoverageAnalyzer()

# Calculate coverage
report = coverage.calculate_coverage(
    source_files=["src/module1.py", "src/module2.py"],
    executed_lines={
        "src/module1.py": set(range(50)),
        "src/module2.py": set(range(30))
    },
    total_lines={
        "src/module1.py": 100,
        "src/module2.py": 80
    }
)

print(f"Line coverage: {report.line_coverage_pct:.1f}%")
print(f"Branch coverage: {report.branch_coverage_pct:.1f}%")

# Get trends
trend = coverage.get_coverage_trend(last_runs=10)
print(f"Coverage trend: {trend['trend']}")
```

### Performance Testing

```python
from agents.testing.agent import PerformanceTester

perf = PerformanceTester()

# Load test
result = perf.run_load_test(
    endpoint="/api/products",
    concurrent_users=100,
    duration_seconds=60
)

print(f"Mean response: {result['response_time']['mean']:.0f}ms")
print(f"P95 response: {result['response_time']['p95']:.0f}ms")
print(f"Throughput: {result['throughput_rps']:.0f} req/s")

# Stress test
stress = perf.run_stress_test("/api/products", max_users=1000)
print(f"Breaking point: {stress['breaking_point']} users")
```

### Security Testing

```python
from agents.testing.agent import SecurityTester

security = SecurityTester()

# SAST scan
sast = security.run_sast_scan("src/")
print(f"SAST: {sast['findings']} findings")

# DAST scan
dast = security.run_dast_scan("https://api.example.com")
print(f"DAST: {dast['findings']} findings")

# SCA scan
sca = security.run_sca_scan("requirements.txt")
print(f"SCA: {sca['vulnerable']} vulnerable dependencies")

# Track vulnerability
vuln = security.add_vulnerability(
    title="XSS Vulnerability",
    severity="high",
    cvss_score=7.5,
    cwe_id="CWE-79"
)
```

### Quality Gates

```python
from agents.testing.agent import QualityGateManager, QualityGate

qm = QualityGateManager()

# Configure gates
qm.configure_gate(QualityGate.CODE_COVERAGE, threshold=80.0)
qm.configure_gate(QualityGate.TEST_PASS_RATE, threshold=95.0)

# Evaluate gates
results = qm.evaluate_all_gates({
    "code_coverage": 85.0,
    "test_pass_rate": 98.0,
    "response_time_ms": 250,
})

for r in results:
    print(f"{r.gate.value}: {r.status.value}")

# Overall status
status = qm.get_overall_status()
print(f"Overall: {status.value}")
```

---

## API Reference

### Main Classes

| Class | Description |
|-------|-------------|
| `TestingAgent` | Main agent orchestrating all components |
| `TestGenerator` | Test case generation from various sources |
| `TestRunner` | Test execution engine |
| `CoverageAnalyzer` | Code coverage analysis |
| `QualityAnalyzer` | Test quality metrics |
| `PerformanceTester` | Performance testing tools |
| `SecurityTester` | Security vulnerability scanning |
| `QualityGateManager` | Quality gate evaluation |
| `TestReportGenerator` | Test report generation |

### Key Enums

| Enum | Values |
|------|--------|
| `TestType` | UNIT, INTEGRATION, E2E, PERFORMANCE, SECURITY, ACCESSIBILITY, SMOKE, REGRESSION, API, CONTRACT, VISUAL, CHAOS, LOAD, STRESS, ENDURANCE |
| `TestStatus` | PENDING, QUEUED, RUNNING, PASSED, FAILED, SKIPPED, BLOCKED, ERROR, FLAKY |
| `Priority` | CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL |
| `QualityGate` | CODE_COVERAGE, TEST_PASS_RATE, CODE_QUALITY, SECURITY_SCAN, PERFORMANCE, ACCESSIBILITY, API_CONTRACT, VISUAL_REGRESSION |
| `GateStatus` | PASSED, FAILED, WARNING, NOT_STARTED, SKIPPED |

### Key Data Classes

| Class | Purpose |
|-------|---------|
| `TestCase` | Test case definition |
| `TestSuite` | Test suite collection |
| `TestExecution` | Test run record |
| `TestMetrics` | Aggregated test metrics |
| `TestReport` | Comprehensive test report |
| `QualityGateResult` | Gate evaluation result |
| `Defect` | Bug/defect record |
| `CoverageReport` | Code coverage data |
| `PerformanceBenchmark` | Performance target |
| `SecurityVulnerability` | Security finding |

---

## Examples

### Complete Testing Workflow

```python
from agents.testing.agent import TestingAgent, TestConfiguration, TestEnvironment

# Initialize
config = TestConfiguration(
    environment=TestEnvironment.STAGING,
    parallel=True,
    retry_count=2,
)
agent = TestingAgent(config)

# 1. Generate tests
requirements = [
    {
        "id": "AUTH001",
        "title": "Authentication",
        "scenarios": [
            {"name": "Login success", "expected_results": ["Redirect to dashboard"]},
            {"name": "Login failure", "expected_results": ["Show error message"]},
        ]
    }
]
tests = agent.generator.generate_from_requirements(requirements)
for t in tests:
    agent.test_cases[t.test_id] = t

# 2. Create and run suite
suite = agent.create_test_suite("Auth Tests", "Authentication test suite", [t.test_id for t in tests])
results = agent.execute_test_suite(suite.suite_id)

# 3. Check coverage
coverage = agent.coverage.calculate_coverage(
    ["src/auth.py"], {"src/auth.py": set(range(50))}, {"src/auth.py": 100}
)

# 4. Run security scan
security = agent.security.run_sast_scan("src/")

# 5. Evaluate quality gates
gates = agent.run_quality_gates({
    "code_coverage": coverage.overall_coverage,
    "test_pass_rate": results["summary"]["pass_rate"],
})

# 6. Generate report
report = agent.generate_test_report(suite.suite_id)
print(report.executive_summary)
```

### Performance Testing Suite

```python
from agents.testing.agent import PerformanceTester, PerformanceMetric

perf = PerformanceTester()

# Add benchmarks
perf.add_benchmark("Response Time", PerformanceMetric.RESPONSE_TIME, 200, "ms")
perf.add_benchmark("Throughput", PerformanceMetric.THROUGHPUT, 1000, "req/s")
perf.add_benchmark("Error Rate", PerformanceMetric.ERROR_RATE, 1.0, "%")

# Run tests
load_result = perf.run_load_test("/api/data", concurrent_users=500, duration_seconds=120)
stress_result = perf.run_stress_test("/api/data", max_users=2000)

# Evaluate
benchmarks = perf.evaluate_benchmarks({
    "response_time": load_result["response_time"]["p95"],
    "throughput": load_result["throughput_rps"],
    "error_rate": load_result["error_rate_pct"],
})

for b in benchmarks:
    print(f"{b.message}")
```

---

## Configuration

The agent uses sensible defaults but can be configured:

```python
from agents.testing.agent import TestConfiguration, TestEnvironment

config = TestConfiguration(
    environment=TestEnvironment.STAGING,
    parallel=True,
    max_workers=8,
    timeout_seconds=600,
    retry_count=3,
    fail_fast=False,
    verbose=True,
    collect_metrics=True,
    tags=["smoke", "regression"],
    exclude_tags=["slow"],
)

agent = TestingAgent(config)
```

### Quality Gate Configuration

```python
from agents.testing.agent import QualityGateManager, QualityGate

qm = QualityGateManager()

# Configure thresholds
qm.configure_gate(QualityGate.CODE_COVERAGE, threshold=85.0)
qm.configure_gate(QualityGate.TEST_PASS_RATE, threshold=98.0)
qm.configure_gate(QualityGate.PERFORMANCE, threshold=300.0)
qm.configure_gate(QualityGate.SECURITY_SCAN, threshold=0)
```

---

## Best Practices

### Test Design
1. **Test Pyramid**: More unit tests, fewer E2E tests
2. **FIRST Principles**: Fast, Independent, Repeatable, Self-validating, Timely
3. **AAA Pattern**: Arrange, Act, Assert
4. **One assertion per test**: Keep tests focused

### Test Automation
1. **Automate regression tests**: Focus on repetitive, high-value tests
2. **Use page objects**: For UI test maintainability
3. **Data-driven tests**: Externalize test data
4. **Continuous integration**: Run tests on every commit

### Performance Testing
1. **Baseline first**: Establish performance baselines
2. **Realistic scenarios**: Model real user behavior
3. **Monitor resources**: Track CPU, memory, network
4. **Test early**: Don't wait for production

### Security Testing
1. **Shift left**: Integrate security testing early
2. **Automate scans**: Run SAST/DAST in CI/CD
3. **Dependency scanning**: Monitor third-party libraries
4. **Penetration testing**: Regular manual security reviews

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Flaky tests | Check test isolation, use explicit waits, mock dependencies |
| Low coverage | Identify critical paths, add edge case tests |
| Slow execution | Parallelize tests, optimize fixtures, mock external services |
| Quality gate failures | Review thresholds, check for false positives |
| Memory issues | Use test fixtures, clean up resources |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Or configure specific logger
logging.getLogger("agents.testing").setLevel(logging.DEBUG)
```

### Getting Help

```python
# Get quality dashboard
dashboard = agent.get_quality_dashboard()
print(dashboard)

# Get test trends
trends = agent.report_generator.get_trends(last_runs=20)
print(trends)
```

---

## License

MIT License - See [LICENSE](../LICENSE) for details.

---

*Ensure software quality through comprehensive testing automation.*

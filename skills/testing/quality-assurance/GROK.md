# Quality Assurance

## Overview

Quality Assurance (QA) is a systematic process aimed at ensuring that software products meet specified requirements and quality standards. QA encompasses the entire software development lifecycle, from requirements gathering to deployment and maintenance, with the goal of preventing defects and ensuring customer satisfaction. Unlike testing, which focuses on finding defects after they are introduced, QA focuses on preventing defects from occurring in the first place through process improvement, standards adherence, and continuous monitoring. This skill covers the fundamental principles, methodologies, and best practices that define professional quality assurance engineering.

## Core Capabilities

The Quality Assurance skill provides comprehensive capabilities for establishing and maintaining quality standards across software projects. Test management forms the foundation, enabling teams to organize, track, and manage test cases throughout the development lifecycle with proper versioning and traceability. Defect tracking and management capabilities allow teams to capture, categorize, prioritize, and track issues from discovery through resolution, ensuring nothing falls through the cracks. Risk-based testing approaches help teams optimize their testing efforts by focusing resources on the most critical areas based on probability and impact assessments.

Process improvement and metrics collection enable data-driven decision making, allowing teams to identify trends, measure effectiveness, and continuously refine their QA processes. Requirements traceability ensures complete coverage by mapping tests back to business requirements, proving that every requirement has been verified. Quality metrics and reporting capabilities provide visibility into test execution results, defect density, and quality trends for stakeholders at all levels.

## Usage Examples

```python
from qa_skill import QualityAssuranceManager, TestCase, Defect, RiskAssessment

# Initialize QA management system
qa_manager = QualityAssuranceManager()

# Create test cases with requirements traceability
test_case = TestCase(
    name="User Login Functionality",
    test_id="TC-LOGIN-001",
    requirements=["REQ-AUTH-001", "REQ-AUTH-002"],
    preconditions=["User is on login page", "Test account exists"],
    steps=[
        "Enter valid username",
        "Enter valid password",
        "Click login button",
        "Verify successful login redirect"
    ],
    expected_results=[
        "No error messages displayed",
        "User redirected to dashboard",
        "User session created"
    ],
    priority="high",
    automation_status="automated"
)

# Add test case to test suite
qa_manager.add_test_case(test_case)

# Create defect report
defect = Defect(
    defect_id="DEF-2024-001",
    title="Session timeout not working",
    description="User session does not timeout after 30 minutes of inactivity",
    severity="high",
    priority="high",
    module="authentication",
    steps_to_reproduce=[
        "Login to application",
        "Wait 31 minutes without activity",
        "Attempt to access protected resource"
    ],
    expected_behavior="User should be redirected to login page",
    actual_behavior="User remains logged in and can access resources",
    status="open",
    assigned_to="dev_team@company.com"
)

# Log and track defect
qa_manager.log_defect(defect)

# Perform risk assessment for feature
risk_assessment = RiskAssessment(
    feature_name="Payment Processing",
    complexity_score=9,
    change_frequency=7,
    customer_impact=10,
    failure_likelihood=6
)

# Get risk-based testing recommendations
testing_recommendations = risk_assessment.get_testing_recommendations()
print("Recommended Testing Depth:", testing_recommendations["depth"])
print("Required Test Cases:", testing_recommendations["min_test_cases"])

# Generate quality metrics report
metrics = qa_manager.calculate_quality_metrics(
    start_date="2024-01-01",
    end_date="2024-01-31"
)
print(f"Test Pass Rate: {metrics['test_pass_rate']}%")
print(f"Defect Density: {metrics['defect_density']}")
print(f"Requirements Coverage: {metrics['requirements_coverage']}%")
```

## Best Practices

Quality Assurance should be integrated early in the development lifecycle rather than being treated as a final checkpoint. Shift-left testing moves testing activities earlier, catching defects when they are cheaper and easier to fix. Establish clear quality gates and exit criteria that must be met before releases proceed, ensuring consistent standards across all projects. Maintain comprehensive test documentation that can be easily updated as requirements evolve, supporting both manual and automated testing efforts.

Implement continuous integration with automated testing to provide rapid feedback on code changes. Use risk-based testing to optimize resource allocation, focusing effort on high-risk areas while maintaining reasonable coverage elsewhere. Foster collaboration between developers, testers, and business stakeholders to ensure shared understanding of quality requirements. Track and analyze quality metrics over time to identify patterns, measure improvement, and justify QA investments to leadership.

## Related Skills

- Test Automation (automating repetitive tests for faster feedback)
- Performance Testing (ensuring system scalability and responsiveness)
- Security Testing (protecting against vulnerabilities and threats)
- Penetration Testing (simulating attacks to identify weaknesses)

## Use Cases

Quality Assurance is essential in any software development context where reliability and user satisfaction matter. In enterprise application development, QA processes ensure that complex business workflows function correctly and that regulatory compliance requirements are met. For mobile applications, thorough QA validates functionality across diverse devices, OS versions, and network conditions. In regulated industries like healthcare and finance, robust QA documentation proves that software meets stringent quality and safety standards.

## Advanced Configuration

### Test Management Configuration

```python
from quality_assurance import TestManagementConfig, TestFramework

# Advanced test management configuration
config = TestManagementConfig(
    framework=TestFramework.PYTEST,
    test_directory="tests/",
    test_pattern="test_*.py",
    coverage_threshold=80,
    mutation_testing=True,
    mutation_score_threshold=75,
    parallel_execution=True,
    max_workers=8,
    timeout_per_test=300,
    retry_flaky=True,
    max_retries=2,
    report_format=["html", "json", "junit"],
    report_directory="reports/",
    screenshot_on_failure=True,
    video_recording=True,
    log_level="INFO",
)

qa_manager = QualityAssuranceManager(config=config)
```

### Defect Tracking Configuration

```python
from quality_assurance import DefectTrackingConfig, WorkflowConfig

defect_config = DefectTrackingConfig(
    workflow=WorkflowConfig(
        states=["open", "in_progress", "resolved", "verified", "closed"],
        transitions={
            "open": ["in_progress", "deferred"],
            "in_progress": ["resolved", "blocked"],
            "resolved": ["verified", "reopened"],
            "verified": ["closed"],
            "reopened": ["in_progress"],
        },
        required_fields=["severity", "priority", "assignee"],
        auto_assign=True,
        sla_config={
            "critical": {"response_hours": 4, "resolution_hours": 24},
            "high": {"response_hours": 8, "resolution_hours": 48},
            "medium": {"response_hours": 24, "resolution_hours": 120},
            "low": {"response_hours": 48, "resolution_hours": 240},
        },
    ),
    integration={
        "jira": {"enabled": True, "project_key": "QA"},
        "github": {"enabled": True, "repo": "org/project"},
        "slack": {"enabled": True, "channel": "#qa-alerts"},
    },
)

qa_manager = QualityAssuranceManager(defect_config=defect_config)
```

### Risk Assessment Configuration

```python
from quality_assurance import RiskAssessmentConfig, RiskMatrix

risk_config = RiskAssessmentConfig(
    risk_matrix=RiskMatrix(
        probability_scale=["rare", "unlikely", "possible", "likely", "almost_certain"],
        impact_scale=["negligible", "minor", "moderate", "major", "catastrophic"],
        risk_scores={
            "rare": 1, "unlikely": 2, "possible": 3, "likely": 4, "almost_certain": 5,
            "negligible": 1, "minor": 2, "moderate": 3, "major": 4, "catastrophic": 5,
        },
        risk_thresholds={
            "low": (1, 6),
            "medium": (7, 12),
            "high": (13, 19),
            "critical": (20, 25),
        },
    ),
    auto_recommendations=True,
    testing_strategies={
        "low": "standard",
        "medium": "enhanced",
        "high": "exhaustive",
        "critical": "exhaustive_with_review",
    },
)

risk_assessor = RiskAssessment(config=risk_config)
```

## Architecture Patterns

### QA Pipeline Pattern

```python
from quality_assurance import QAPipeline, PipelineStage

pipeline = QAPipeline(stages=[
    PipelineStage(
        name="requirements_review",
        type="review",
        processor=lambda reqs: review_requirements(reqs),
    ),
    PipelineStage(
        name="test_design",
        type="design",
        processor=lambda reqs: design_tests(reqs),
    ),
    PipelineStage(
        name="test_execution",
        type="execution",
        processor=lambda tests: execute_tests(tests),
    ),
    PipelineStage(
        name="defect_management",
        type="management",
        processor=lambda results: manage_defects(results),
    ),
    PipelineStage(
        name="quality_report",
        type="reporting",
        processor=lambda data: generate_report(data),
    ),
])

# Execute QA pipeline
results = pipeline.execute(requirements=project_requirements)
```

### Continuous Quality Pattern

```python
from quality_assurance import ContinuousQuality, QualityGate

continuous = ContinuousQuality(
    gates=[
        QualityGate(
            name="code_review",
            criteria=["peer_review_approved", "no_critical_issues"],
            blocking=True,
        ),
        QualityGate(
            name="unit_tests",
            criteria=["coverage_above_80", "all_tests_pass"],
            blocking=True,
        ),
        QualityGate(
            name="integration_tests",
            criteria=["all_tests_pass", "no_performance_regression"],
            blocking=True,
        ),
        QualityGate(
            name="security_scan",
            criteria=["no_critical_vulnerabilities", "no_high_vulnerabilities"],
            blocking=True,
        ),
        QualityGate(
            name="acceptance_tests",
            criteria=["all_scenarios_pass"],
            blocking=False,
        ),
    ],
    metrics_tracking=True,
    trend_analysis=True,
)

# Monitor quality continuously
continuous.start_monitoring()
```

### Defect Analysis Pattern

```python
from quality_assurance import DefectAnalyzer, AnalysisStrategy

analyzer = DefectAnalyzer(
    strategy=AnalysisStrategy.PARETO,
    time_window_days=90,
    categories=["functional", "ui", "performance", "security", "integration"],
)

# Analyze defect patterns
analysis = analyzer.analyze(defects=historical_defects)

print(f"Top defect category: {analysis.top_category}")
print(f"Pareto distribution: {analysis.pareto_distribution}")
print(f"Root causes: {analysis.root_causes}")
print(f"Recommendations: {analysis.recommendations}")
```

## Integration Guide

### Jira Integration

```python
from quality_assurance import JiraIntegration, JiraConfig

jira_config = JiraConfig(
    server="https://company.atlassian.net",
    project_key="QA",
    issue_types=["Bug", "Task", "Story"],
    custom_fields={
        "defect_severity": "customfield_10001",
        "test_case_id": "customfield_10002",
    },
    auto_sync=True,
    sync_interval_minutes=5,
)

jira = JiraIntegration(config=jira_config)

# Create defect in Jira
defect = jira.create_defect(
    summary="Login button not responding",
    description="Clicking login button does not trigger action",
    severity="high",
    priority="high",
    assignee="dev_team",
    labels=["login", "ui"],
)

print(f"Created Jira issue: {defect.key}")
```

### GitHub Integration

```python
from quality_assurance import GitHubIntegration, GitHubConfig

github_config = GitHubConfig(
    repository="org/project",
    token="${GITHUB_TOKEN}",
    auto_create_issues=True,
    link_to_commits=True,
    link_to_prs=True,
)

github = GitHubIntegration(config=github_config)

# Create GitHub issue from defect
issue = github.create_issue(
    title="Session timeout bug",
    body="User session does not timeout after 30 minutes",
    labels=["bug", "high-priority"],
    assignees=["developer1"],
)

# Link to test failure
github.link_to_test_failure(
    issue=issue,
    test_run_id="run-123",
    test_name="test_session_timeout",
)
```

### TestRail Integration

```python
from quality_assurance import TestRailIntegration, TestRailConfig

testrail_config = TestRailConfig(
    server="https://company.testrail.io",
    username="${TESTRAIL_USER}",
    api_key="${TESTRAIL_API_KEY}",
    project_id=1,
    suite_id=1,
    auto_results=True,
)

testrail = TestRailIntegration(config=testrail_config)

# Update test results
testrail.update_test_run(
    run_id=123,
    results=[
        {"case_id": 1, "status": "passed", "comment": "Test passed"},
        {"case_id": 2, "status": "failed", "comment": "Login button not responding"},
    ],
)

# Generate test report
report = testrail.get_test_run_report(run_id=123)
print(f"Pass rate: {report.pass_rate:.1%}")
```

## Performance Optimization

### Test Execution Optimization

```python
from quality_assurance import TestOptimizer, OptimizationStrategy

optimizer = OptimizationStrategy(
    strategy=OptimizationStrategy.SMART_SELECTION,
    coverage_target=0.95,
    risk_based=True,
    parallel_execution=True,
    max_workers=8,
    test_grouping=True,
    flaky_test_detection=True,
)

# Optimize test suite
optimized_suite = optimizer.optimize(
    full_suite=full_test_suite,
    changeset=git_changeset,
    historical_results=historical_data,
)

print(f"Original tests: {len(full_test_suite)}")
print(f"Optimized tests: {len(optimized_suite)}")
print(f"Estimated time savings: {optimizer.estimated_savings:.1%}")
```

### Reporting Optimization

```python
from quality_assurance import ReportOptimizer

report_optimizer = ReportOptimizer(
    format=["html", "pdf", "json"],
    compression=True,
    caching=True,
    cache_ttl_hours=24,
    async_generation=True,
)

# Generate optimized report
report = report_optimizer.generate(
    data=quality_metrics,
    template="executive_summary",
    recipients=["management@company.com"],
)

print(f"Report generated: {report.path}")
print(f"Generation time: {report.generation_time_seconds:.1f}s")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Low Test Coverage

**Symptom**: Coverage below target threshold

**Solution**:
```python
# Identify uncovered code
coverage_report = qa_manager.get_coverage_report()
uncovered = coverage_report.get_uncovered_lines()

# Create tests for uncovered code
for module, lines in uncovered.items():
    print(f"Module {module}: {len(lines)} uncovered lines")
    # Generate test suggestions
    suggestions = qa_manager.suggest_tests(module, lines)
```

#### 2. Flaky Tests

**Symptom**: Tests sometimes pass, sometimes fail

**Solution**:
```python
# Detect flaky tests
flaky_tests = qa_manager.detect_flaky_tests(
    min_runs=10,
    flaky_threshold=0.2,  # 20% inconsistency
)

# Quarantine flaky tests
for test in flaky_tests:
    qa_manager.quarantine_test(test, reason="flaky")

# Fix flaky tests
for test in flaky_tests:
    qa_manager.add_retry(test, max_retries=3)
    qa_manager.add_wait_conditions(test)
```

#### 3. Defect Leakage

**Symptom**: Defects found in production

**Solution**:
```python
# Analyze defect leakage
leakage_analysis = qa_manager.analyze_defect_leakage(
    time_window_days=90,
    categories=["functional", "ui", "performance"],
)

print(f"Defect leakage rate: {leakage_analysis.leakage_rate:.1%}")
print(f"Root causes: {leakage_analysis.root_causes}")
print(f"Recommendations: {leakage_analysis.recommendations}")

# Strengthen testing
qa_manager.strengthen_testing(
    areas=leakage_analysis.vulnerable_areas,
    strategy="exhaustive",
)
```

## API Reference

### Core Classes

#### `QualityAssuranceManager`
```python
class QualityAssuranceManager:
    def __init__(self, config: Optional[TestManagementConfig] = None) -> None: ...
    def add_test_case(self, test_case: TestCase) -> None: ...
    def log_defect(self, defect: Defect) -> None: ...
    def calculate_quality_metrics(self, start_date: str, end_date: str) -> Dict[str, float]: ...
    def generate_test_report(self, format: str = "html") -> Report: ...
    def get_coverage_report(self) -> CoverageReport: ...
    def detect_flaky_tests(self, min_runs: int = 10) -> List[TestCase]: ...
```

#### `TestCase`
```python
@dataclass
class TestCase:
    name: str
    test_id: str
    requirements: List[str]
    preconditions: List[str]
    steps: List[str]
    expected_results: List[str]
    priority: str
    automation_status: str
    estimated_duration_seconds: int = 0
    tags: List[str] = field(default_factory=list)
```

## Data Models

### Quality Metrics Schema

```json
{
  "period": "2024-01",
  "test_execution": {
    "total_tests": 500,
    "passed": 475,
    "failed": 20,
    "skipped": 5,
    "pass_rate": 0.95,
    "execution_time_hours": 12.5
  },
  "defects": {
    "total": 45,
    "critical": 2,
    "high": 8,
    "medium": 20,
    "low": 15,
    "fixed": 40,
    "open": 5,
    "defect_density": 2.5
  },
  "coverage": {
    "line_coverage": 0.82,
    "branch_coverage": 0.75,
    "function_coverage": 0.88
  }
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY quality_assurance/ /app/quality_assurance/
WORKDIR /app

ENV QA_REPORT_FORMAT=html
ENV QA_COVERAGE_THRESHOLD=80

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from quality_assurance import health_check; health_check()"

CMD ["python", "-m", "quality_assurance.server"]
```

## Monitoring & Observability

### Metrics Collection

```python
from quality_assurance import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("qa_test_pass_rate", type="gauge")
collector.register_metric("qa_defect_count", type="gauge")
collector.register_metric("qa_coverage", type="gauge")
collector.register_metric("qa_test_duration", type="histogram")

collector.set("qa_test_pass_rate", metrics.pass_rate)
collector.set("qa_defect_count", metrics.defect_count)
collector.set("qa_coverage", metrics.coverage)
collector.observe("qa_test_duration", metrics.execution_time_seconds)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from quality_assurance import QualityAssuranceManager, TestCase

class TestQualityAssurance:
    def setup_method(self):
        self.qa = QualityAssuranceManager()
    
    def test_add_test_case(self):
        test_case = TestCase(
            name="Test Login",
            test_id="TC-001",
            requirements=["REQ-001"],
            preconditions=["User exists"],
            steps=["Enter credentials", "Click login"],
            expected_results=["Login successful"],
            priority="high",
            automation_status="automated",
        )
        self.qa.add_test_case(test_case)
        assert self.qa.get_test_case("TC-001") is not None
    
    def test_calculate_metrics(self):
        metrics = self.qa.calculate_quality_metrics(
            start_date="2024-01-01",
            end_date="2024-01-31",
        )
        assert "test_pass_rate" in metrics
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API
- **Added**: Risk-based testing
- **Added**: Flaky test detection
- **Improved**: 2x faster test execution
- **Fixed**: Coverage calculation accuracy

## Glossary

| Term | Definition |
|------|------------|
| **Test Case** | Documented test scenario with steps and expected results |
| **Defect** | Software bug or issue found during testing |
| **Coverage** | Percentage of code tested |
| **Flaky Test** | Test with inconsistent results |
| **Quality Gate** | Criteria that must be met to proceed |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/quality-assurance.git
cd quality-assurance
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Quality Assurance Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

*Last updated: 2024-01-15*
*Version: 2.0.0*

## Advanced Patterns

### Test Case Management

```python
from quality_assurance import TestCaseManager, ManagementConfig

manager = TestCaseManager(
    config=ManagementConfig(
        versioning=True,
        traceability=True,
        review_workflow=True,
        approval_required=True,
    ),
)

# Create test case
test_case = manager.create_test_case(
    name="User Registration Flow",
    description="Test complete user registration process",
    steps=[
        "Navigate to registration page",
        "Fill in user details",
        "Submit form",
        "Verify email confirmation",
    ],
    expected_results=[
        "Registration form displayed",
        "Form accepts valid input",
        "Confirmation message shown",
        "Email sent successfully",
    ],
    priority="high",
    automation_status="automated",
    requirements=["REQ-AUTH-001", "REQ-AUTH-002"],
)

print(f"Test case created: {test_case.test_id}")
print(f"Version: {test_case.version}")
```

### Defect Lifecycle Management

```python
from quality_assurance import DefectLifecycle, LifecycleConfig

lifecycle = DefectLifecycle(
    config=LifecycleConfig(
        states=["new", "triaged", "assigned", "in_progress", "fixed", "verified", "closed"],
        transitions={
            "new": ["triaged", "rejected"],
            "triaged": ["assigned"],
            "assigned": ["in_progress"],
            "in_progress": ["fixed", "blocked"],
            "fixed": ["verified", "reopened"],
            "verified": ["closed"],
            "reopened": ["in_progress"],
        },
        sla_config={
            "critical": {"response_hours": 4, "resolution_hours": 24},
            "high": {"response_hours": 8, "resolution_hours": 48},
            "medium": {"response_hours": 24, "resolution_hours": 120},
            "low": {"response_hours": 48, "resolution_hours": 240},
        },
    ),
)

# Manage defect lifecycle
defect = lifecycle.create_defect(
    title="Login button not responding",
    severity="high",
    priority="high",
    steps_to_reproduce=["Navigate to login page", "Click login button"],
    expected_behavior="Login form submitted",
    actual_behavior="Nothing happens",
)

lifecycle.transition(defect, "triaged")
print(f"Defect {defect.defect_id} triaged")
```

### Quality Metrics Dashboard

```python
from quality_assurance import QualityDashboard, DashboardConfig

dashboard = QualityDashboard(
    config=DashboardConfig(
        metrics=[
            "test_pass_rate",
            "defect_density",
            "code_coverage",
            "defect_leakage",
            "mean_time_to_detect",
            "mean_time_to_fix",
        ],
        visualization=["line_chart", "bar_chart", "gauge"],
        refresh_interval_minutes=5,
        alert_thresholds={
            "test_pass_rate": {"min": 90},
            "defect_density": {"max": 5},
            "code_coverage": {"min": 80},
        },
    ),
)

# Generate dashboard
dashboard.generate()
print(f"Dashboard URL: {dashboard.url}")
```

### Test Coverage Analysis

```python
from quality_assurance import CoverageAnalyzer, CoverageConfig

analyzer = CoverageAnalyzer(
    config=CoverageConfig(
        types=["line", "branch", "function", "module"],
        threshold=80,
        exclude_patterns=["test/", "vendor/"],
        report_format=["html", "json"],
    ),
)

# Analyze coverage
coverage = analyzer.analyze(source_directory="src/")
print(f"Line coverage: {coverage.line_coverage:.1%}")
print(f"Branch coverage: {coverage.branch_coverage:.1%}")
print(f"Function coverage: {coverage.function_coverage:.1%}")
print(f"Uncovered lines: {coverage.uncovered_lines}")

### Quality Gate Enforcement

```python
from quality_assurance import QualityGate, GateConfig

gate = QualityGate(
    config=GateConfig(
        gates={
            "code_review": {"required": True, "min_approvals": 2},
            "unit_tests": {"min_coverage": 80, "all_pass": True},
            "integration_tests": {"min_coverage": 70, "all_pass": True},
            "security_scan": {"max_critical": 0, "max_high": 5},
            "performance": {"max_regression": 5},
        },
        blocking=True,
        notification_channels=["slack"],
    ),
)

# Enforce quality gate
result = gate.enforce(pull_request="PR-123")
print(f"Gate status: {result.status}")
print(f"Passed gates: {result.passed_gates}")
print(f"Failed gates: {result.failed_gates}")
```
```

# Test Automation

## Overview

Test Automation enables efficient, repeatable, and scalable software testing through automated test execution, reporting, and integration with development workflows. This skill covers test framework selection, test design patterns, CI/CD integration, and test maintenance strategies. Test automation reduces manual effort, improves test coverage, and provides rapid feedback on code changes.

## Core Capabilities

Test framework configuration supports multiple frameworks including pytest, JUnit, Selenium, Cypress, and Playwright. Test case management organizes tests by type (unit, integration, E2E, API), priority, and execution schedule. Test execution engines run tests in parallel, across browsers, and on multiple platforms.

Test reporting generates comprehensive reports with pass/fail rates, trend analysis, and flaky test identification. CI/CD integration triggers tests on code changes, pull requests, and scheduled intervals. Test data management creates, maintains, and cleans up test data for consistent test execution.

## Usage Examples

```python
from test_automation import TestAutomationFramework, TestType, TestStatus

framework = TestAutomationFramework()

# Configure test suite
suite = framework.create_test_suite(
    name="Regression Suite",
    test_type=TestType.UNIT,
    tests=["test_login", "test_dashboard", "test_api"]
)

# Execute tests
results = framework.run_suite(suite)
print(f"Passed: {results['passed']}")
print(f"Failed: {results['failed']}")
print(f"Skipped: {results['skipped']}")

# CI/CD integration
pipeline = framework.configure_ci_integration(
    platform="github",
    triggers=["pull_request", "push_to_main"],
    parallel=True,
    max_workers=4
)

# Generate report
report = framework.generate_report(results)
print(f"Coverage: {report['code_coverage']}%")
print(f"Duration: {report['total_duration']}s")
```

## Best Practices

Follow the test pyramid: many unit tests, fewer integration tests, minimal E2E tests. Use page object patterns for UI tests to separate test logic from page structure. Implement proper test isolation to prevent test interdependencies. Use meaningful test names that describe expected behavior.

Maintain test code with the same standards as production code. Review failing tests immediately to prevent test debt accumulation. Use test data factories for consistent test data creation. Implement retry logic for flaky tests while investigating root causes.

## Related Skills

- Unit Testing (isolated component testing)
- Integration Testing (component interaction testing)
- E2E Testing (complete workflow testing)
- CI/CD (continuous integration pipelines)

## Use Cases

Unit test automation validates individual functions and methods in isolation. Integration test automation verifies component interactions and API contracts. E2E test automation simulates complete user workflows across the application. Cross-browser testing ensures consistent behavior across browsers and devices.

API test automation validates endpoint functionality, performance, and security. Regression testing automates retesting after changes to prevent feature degradation. Smoke testing provides quick validation of critical paths before full test execution.

## Advanced Configuration

### Test Framework Configuration

```python
from test_automation import TestFrameworkConfig, FrameworkType

# Advanced framework configuration
config = TestFrameworkConfig(
    framework=FrameworkType.PYTEST,
    test_directory="tests/",
    test_pattern="test_*.py",
    fixtures_directory="fixtures/",
    conftest_files=["conftest.py", "conftest_api.py"],
    coverage_enabled=True,
    coverage_threshold=80,
    coverage_source=["src/"],
    coverage_report=["html", "xml", "json"],
    timeout_per_test=300,
    timeout_method="signal",
    parallel_execution=True,
    max_workers=8,
    test_sorting="/alphabetical",
    strict_markers=True,
    strict_config=True,
    log_level="INFO",
    log_format="%(asctime)s %(levelname)s %(message)s",
)

framework = TestAutomationFramework(config=config)
```

### Test Data Management Configuration

```python
from test_automation import TestDataConfig, DataStrategy

# Advanced test data configuration
data_config = TestDataConfig(
    strategy=DataStrategy.FACTORY,
    factories={
        "user": "tests.factories.UserFactory",
        "order": "tests.factories.OrderFactory",
        "product": "tests.factories.ProductFactory",
    },
    database_fixtures=True,
    fixture_strategy="transactional",
    cleanup_strategy="teardown",
    shared_fixtures=["database", "redis", "mock_server"],
    data_seeds={
        "users": "seeds/users.json",
        "products": "seeds/products.json",
    },
)

framework = TestAutomationFramework(data_config=data_config)
```

### Report Generation Configuration

```python
from test_automation import ReportConfig, ReportFormat

# Advanced report configuration
report_config = ReportConfig(
    formats=[ReportFormat.HTML, ReportFormat.JSON, ReportFormat.JUNIT],
    output_directory="reports/",
    include_logs=True,
    include_screenshots=True,
    include_videos=True,
    include_coverage=True,
    include_performance=True,
    trend_analysis=True,
    trend_history_days=30,
    publish_to_dashboard=True,
    dashboard_url="http://test-dashboard:3000",
)

framework = TestAutomationFramework(report_config=report_config)
```

## Architecture Patterns

### Page Object Pattern

```python
from test_automation import PageObject, Element, Wait

class LoginPage(PageObject):
    # Element definitions
    username_field = Element(css="#username")
    password_field = Element(css="#password")
    login_button = Element(css="#login-btn")
    error_message = Element(css=".error-message")
    remember_me = Element(css="#remember-me")
    
    # Page URL
    url = "/login"
    
    def login(self, username, password, remember=False):
        self.username_field.send_keys(username)
        self.password_field.send_keys(password)
        if remember:
            self.remember_me.click()
        self.login_button.click()
    
    def is_error_displayed(self):
        return self.error_message.is_visible()
    
    def get_error_text(self):
        return self.error_message.text

# Usage in tests
def test_login_success():
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login("user@test.com", "password")
    assert dashboard_page.is_displayed()
```

### Data-Driven Testing Pattern

```python
from test_automation import DataDrivenTest, TestDataProvider

# Define test data
test_data = [
    {"username": "admin", "password": "admin123", "expected": "success"},
    {"username": "user", "password": "user123", "expected": "success"},
    {"username": "invalid", "password": "wrong", "expected": "failure"},
    {"username": "", "password": "", "expected": "failure"},
]

@DataDrivenTest(data=test_data)
def test_login_scenarios(username, password, expected):
    login_page = LoginPage(driver)
    login_page.navigate()
    login_page.login(username, password)
    
    if expected == "success":
        assert dashboard_page.is_displayed()
    else:
        assert login_page.is_error_displayed()
```

### API Test Pattern

```python
from test_automation import APITest, Request, Response

class UserAPITest(APITest):
    base_url = "https://api.example.com"
    
    def test_get_users(self):
        request = Request(
            method="GET",
            url="/users",
            headers={"Authorization": f"Bearer {self.token}"},
        )
        
        response = self.execute(request)
        
        assert response.status_code == 200
        assert len(response.json()["users"]) > 0
    
    def test_create_user(self):
        request = Request(
            method="POST",
            url="/users",
            headers={"Authorization": f"Bearer {self.token}"},
            json={
                "name": "Test User",
                "email": "test@example.com",
            },
        )
        
        response = self.execute(request)
        
        assert response.status_code == 201
        assert response.json()["name"] == "Test User"
```

### Fixture Pattern

```python
from test_automation import Fixture, Scope

@Fixture(scope=Scope.SESSION)
def database():
    """Setup database connection for all tests."""
    db = Database.connect("postgresql://localhost/test")
    yield db
    db.close()

@Fixture(scope=Scope.FUNCTION)
def user(database):
    """Create a fresh user for each test."""
    user = database.create_user(
        name="Test User",
        email="test@example.com",
    )
    yield user
    database.delete_user(user.id)

@Fixture(scope=Scope.CLASS)
def api_client():
    """Create API client for test class."""
    client = APIClient(base_url="http://localhost:8080")
    yield client
    client.close()
```

## Integration Guide

### Pytest Integration

```python
from test_automation import PytestIntegration, PytestConfig

# Configure pytest integration
pytest_config = PytestConfig(
    testpaths=["tests"],
    python_files=["test_*.py"],
    python_classes=["Test*"],
    python_functions=["test_*"],
    markers={
        "slow": "marks tests as slow",
        "smoke": "marks tests as smoke tests",
        "integration": "marks tests as integration tests",
    ],
    addopts=[
        "-v",
        "--tb=short",
        "--strict-markers",
        "--cov=src",
        "--cov-report=html",
    ],
)

integration = PytestIntegration(config=pytest_config)
integration.setup()
```

### Selenium Integration

```python
from test_automation import SeleniumIntegration, BrowserConfig

# Configure Selenium integration
selenium_config = SeleniumConfig(
    browser="chrome",
    headless=True,
    window_size=(1920, 1080),
    implicit_wait=10,
    page_load_timeout=30,
    screenshot_on_failure=True,
    video_recording=True,
    remote=False,
    grid_url=None,
)

integration = SeleniumIntegration(config=selenium_config)
driver = integration.create_driver()
```

### Playwright Integration

```python
from test_automation import PlaywrightIntegration, PlaywrightConfig

# Configure Playwright integration
playwright_config = PlaywrightConfig(
    browser="chromium",
    headless=True,
    viewport={"width": 1920, "height": 1080},
    slow_mo=0,
    screenshot="only-on-failure",
    video="retain-on-failure",
    trace="retain-on-failure",
    timeout=30000,
)

integration = PlaywrightIntegration(config=playwright_config)
browser = integration.create_browser()
```

### REST Assured Integration

```python
from test_automation import RestAssuredIntegration, RestAssuredConfig

# Configure REST Assured integration
rest_config = RestAssuredConfig(
    base_uri="https://api.example.com",
    base_path="/v1",
    content_type="application/json",
    accept="application/json",
    authentication="bearer",
    token_url="https://auth.example.com/token",
    client_id="test_client",
    client_secret="test_secret",
)

integration = RestAssuredIntegration(config=rest_config)

# Make API call
response = integration.request(
    method="GET",
    path="/users",
    expect_status=200,
)
```

## Performance Optimization

### Parallel Test Execution

```python
from test_automation import ParallelExecutor

executor = ParallelExecutor(
    max_workers=8,
    strategy="process",
    chunk_size=10,
    load_balancing="round_robin",
    resource_monitoring=True,
)

# Execute tests in parallel
results = executor.execute(
    test_suite=regression_suite,
    parallel=True,
    timeout=3600,
)

print(f"Total time: {results.total_time_seconds:.1f}s")
print(f"Parallel efficiency: {results.parallel_efficiency:.1%}")
```

### Test Caching

```python
from test_automation import TestCache

cache = TestCache(
    cache_dir=".test_cache",
    max_size_mb=1024,
    ttl_hours=24,
    strategy="content_hash",
)

# Cache test results
cached_result = cache.get_or_compute(
    test_name="test_api_performance",
    test_fn=lambda: run_performance_test(),
    compute_fn=lambda: run_performance_test(),
)

print(f"Cache hit: {cached_result.from_cache}")
print(f"Result: {cached_result.result}")
```

### Test Optimization

```python
from test_automation import TestOptimizer

optimizer = TestOptimizer(
    strategy="smart_selection",
    coverage_target=0.95,
    risk_based=True,
    flaky_test_detection=True,
    test_grouping=True,
)

# Optimize test suite
optimized = optimizer.optimize(
    full_suite=full_test_suite,
    changeset=git_changeset,
    historical_results=historical_data,
)

print(f"Original tests: {len(full_test_suite)}")
print(f"Optimized tests: {len(optimized)}")
print(f"Time savings: {optimizer.estimated_savings:.1%}")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Flaky Tests

**Symptom**: Tests sometimes pass, sometimes fail

**Solution**:
```python
# Add retry logic
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_unstable():
    pass

# Add explicit waits
from test_automation import Wait

wait = Wait(driver)
wait.until_element_visible(css="#element", timeout=10)

# Use stable selectors
element = driver.find_element(css="#stable-id")  # Not xpath
```

#### 2. Test Environment Issues

**Symptom**: Tests fail due to environment problems

**Solution**:
```python
# Add health checks
@pytest.fixture(scope="session", autouse=True)
def check_environment():
    assert api_server.is_healthy()
    assert database.is_connected()
    assert redis.is_available()

# Use test containers
from test_automation import TestContainer

with TestContainer("postgres:15") as db:
    # Tests run with isolated database
    pass
```

#### 3. Slow Test Execution

**Symptom**: Tests take too long to run

**Solution**:
```python
# Parallelize tests
executor = ParallelExecutor(max_workers=8)

# Use test prioritization
optimizer = TestOptimizer(strategy="smart_selection")

# Mock external services
@pytest.fixture
def mock_api():
    with MockServer(port=8080) as server:
        yield server
```

## API Reference

### Core Classes

#### `TestAutomationFramework`
```python
class TestAutomationFramework:
    def __init__(self, config: Optional[TestFrameworkConfig] = None) -> None: ...
    def create_test_suite(self, name: str, test_type: TestType, tests: List[str]) -> TestSuite: ...
    def run_suite(self, suite: TestSuite) -> TestResults: ...
    def configure_ci_integration(self, platform: str, triggers: List[str], parallel: bool, max_workers: int) -> CIPipeline: ...
    def generate_report(self, results: TestResults) -> Report: ...
```

#### `TestResults`
```python
@dataclass
class TestResults:
    total_tests: int
    passed: int
    failed: int
    skipped: int
    error: int
    pass_rate: float
    duration_seconds: float
    coverage: float
    test_details: List[TestDetail]
```

## Data Models

### Test Configuration Schema

```json
{
  "framework": "pytest",
  "test_directory": "tests/",
  "coverage": {
    "enabled": true,
    "threshold": 80,
    "source": ["src/"]
  },
  "parallel": {
    "enabled": true,
    "max_workers": 8
  },
  "reporting": {
    "formats": ["html", "json"],
    "output": "reports/"
  }
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY tests/ /app/tests/
COPY src/ /app/src/
WORKDIR /app

ENV TEST_PARALLEL=true
ENV TEST_WORKERS=4
ENV COVERAGE_THRESHOLD=80

CMD ["pytest", "tests/", "-v", "--cov=src", "--cov-report=html"]
```

## Monitoring & Observability

### Metrics Collection

```python
from test_automation import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("test_pass_rate", type="gauge")
collector.register_metric("test_duration", type="histogram")
collector.register_metric("test_coverage", type="gauge")
collector.register_metric("test_flaky_rate", type="gauge")

collector.set("test_pass_rate", results.pass_rate)
collector.observe("test_duration", results.duration_seconds)
collector.set("test_coverage", results.coverage)
collector.set("test_flaky_rate", flaky_rate)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from test_automation import TestAutomationFramework, TestFrameworkConfig

class TestTestAutomation:
    def setup_method(self):
        self.config = TestFrameworkConfig(framework="pytest")
        self.framework = TestAutomationFramework(self.config)
    
    def test_create_suite(self):
        suite = self.framework.create_test_suite(
            name="test_suite",
            test_type="unit",
            tests=["test_1", "test_2"],
        )
        assert suite is not None
    
    def test_run_suite(self):
        suite = self.framework.create_test_suite(
            name="test_suite",
            test_type="unit",
            tests=["test_1"],
        )
        results = self.framework.run_suite(suite)
        assert results.pass_rate >= 0
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API
- **Added**: Playwright support
- **Added**: Test caching
- **Improved**: 2x faster test execution
- **Fixed**: Flaky test detection

## Glossary

| Term | Definition |
|------|------------|
| **Test Pyramid** | Strategy with many unit tests, fewer integration, minimal E2E |
| **Page Object** | Design pattern separating test logic from page structure |
| **Flaky Test** | Test with inconsistent results |
| **Test Fixture** | Setup/teardown code for tests |
| **Data-Driven Test** | Tests parameterized with external data |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/test-automation.git
cd test-automation
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Test Automation Contributors

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

### Test Suite Optimization

```python
from test_automation import TestSuiteOptimizer, OptimizationConfig

optimizer = TestSuiteOptimizer(
    config=OptimizationConfig(
        strategy="smart_selection",
        coverage_target=0.95,
        risk_based=True,
        historical_data_days=30,
        flaky_test_detection=True,
    ),
)

# Optimize test suite
optimized = optimizer.optimize(
    full_suite=full_test_suite,
    changeset=git_changeset,
    time_budget_minutes=30,
)

print(f"Original tests: {len(full_test_suite)}")
print(f"Selected tests: {len(optimized)}")
print(f"Estimated time: {optimizer.estimated_time_minutes:.1f} minutes")
print(f"Coverage retained: {optimizer.coverage_retained:.1%}")
```

### Test Data Management

```python
from test_automation import TestDataManager, DataConfig

data_manager = TestDataManager(
    config=DataConfig(
        strategy="factory",
        factories={
            "user": "tests.factories.UserFactory",
            "order": "tests.factories.OrderFactory",
        },
        cleanup_strategy="transactional",
        seed_data="seeds/",
    ),
)

# Generate test data
user = data_manager.create("user", name="Test User", email="test@example.com")
print(f"Created user: {user.id}")

# Cleanup
data_manager.cleanup()
```

### Test Environment Management

```python
from test_automation import EnvironmentManager, EnvConfig

env_manager = EnvironmentManager(
    config=EnvConfig(
        environments={
            "development": {"url": "http://localhost:8080", "db": "test_dev"},
            "staging": {"url": "https://staging.example.com", "db": "test_staging"},
            "production": {"url": "https://example.com", "db": "test_prod"},
        },
        health_check_url="/health",
        setup_timeout_seconds=300,
    ),
)

# Setup environment
env_manager.setup("staging")
print(f"Environment ready: {env_manager.current_environment}")

# Teardown
env_manager.teardown()
```

### Test Reporting Advanced

```python
from test_automation import ReportGenerator, ReportConfig

generator = ReportGenerator(
    config=ReportConfig(
        formats=["html", "json", "junit", "allure"],
        include_screenshots=True,
        include_logs=True,
        include_coverage=True,
        trend_analysis=True,
        trend_history_days=30,
        custom_fields={
            "environment": "staging",
            "build_number": "123",
            "commit_sha": "abc123",
        },
    ),
)

# Generate report
report = generator.generate(test_results)
print(f"Report generated: {report.path}")
print(f"HTML report: {report.html_path}")
print(f"JSON report: {report.json_path}")
```

### Test Flakiness Detection

```python
from test_automation import FlakyTestDetector, DetectionConfig

detector = FlakyTestDetector(
    config=DetectionConfig(
        min_runs=10,
        flaky_threshold=0.2,  # 20% inconsistency
        time_window_days=30,
        auto_quarantine=True,
    ),
)

# Detect flaky tests
flaky_tests = detector.detect(test_history)
print(f"Flaky tests detected: {len(flaky_tests)}")
for test in flaky_tests:
    print(f"  {test.name}: {test.inconsistency_rate:.1%} inconsistent")
```

### Test Parallelization

```python
from test_automation import ParallelTestRunner, ParallelConfig

runner = ParallelTestRunner(
    config=ParallelConfig(
        max_workers=8,
        strategy="process",
        load_balancing="round_robin",
        timeout_per_test=300,
        retry_failed=True,
        max_retries=2,
    ),
)

# Run tests in parallel
results = runner.run(test_suite)
print(f"Total time: {results.total_time_seconds:.1f}s")
print(f"Parallel efficiency: {results.parallel_efficiency:.1%}")
print(f"Tests per second: {results.tests_per_second:.1f}")

### Test Maintenance Automation

```python
from test_automation import TestMaintenance, MaintenanceConfig

maintenance = TestMaintenance(
    config=MaintenanceConfig(
        auto_update_locators=True,
        auto_heal_flaky=True,
        auto_cleanup_stale=True,
        screenshot_on_failure=True,
        video_recording=True,
    ),
)

# Run maintenance
maintenance.run()
print(f"Updated locators: {maintenance.updated_locators}")
print(f"Healed flaky tests: {maintenance.healed_tests}")
print(f"Cleaned up stale tests: {maintenance.cleaned_tests}")
```
```

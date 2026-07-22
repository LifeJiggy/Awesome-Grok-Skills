# Mobile Testing

## Overview

Mobile Testing encompasses the specialized testing practices required to ensure mobile applications function correctly across diverse devices, operating systems, and network conditions. This skill covers automated testing frameworks like Appium, XCTest, and Espresso, device cloud testing, performance monitoring, and platform-specific testing requirements. Mobile testing addresses unique challenges including screen size variations, touch interactions, sensor inputs, and the fragmented Android ecosystem.

## Core Capabilities

Appium enables cross-platform mobile automation supporting both iOS and Android with a single codebase using WebDriver protocol. XCTest provides native iOS testing capabilities including UI, performance, and integration testing. Espresso offers fast and reliable Android UI testing with synchronization built-in. Device cloud platforms like AWS Device Farm and Firebase Test Lab provide access to real devices for comprehensive testing coverage.

Performance testing measures app launch time, memory consumption, CPU usage, battery drain, and frame rates. Network condition testing validates app behavior under various connectivity scenarios including offline mode, poor connectivity, and network switching. Crash reporting and analysis integration with tools like Crashlytics and Sentry enables rapid issue identification and resolution.

## Usage Examples

```python
from mobile_testing import MobileTesting

tester = MobileTesting()

tester.setup_appium(
    platform="iOS",
    capabilities={
        "platformName": "iOS",
        "platformVersion": "17.0",
        "deviceName": "iPhone 15",
        "automationName": "XCUITest",
        "bundleId": "com.company.app"
    }
)

tester.setup_device_farm(
    provider="AWS",
    config={
        "android_devices": 15,
        "ios_devices": 15,
        "private_devices": 5
    }
)

tester.configure_performance_monitoring([
    "app_launch_time",
    "memory_usage",
    "cpu_usage",
    "battery_drain"
])

results = tester.run_compatibility_test(
    devices=["iPhone 15", "Pixel 8", "Samsung S24"],
    os_versions=["16.0", "17.0", "13.0", "14.0"],
    test_suite=["login", "checkout", "search", "profile"]
)

tester.setup_report_generator(
    format="html",
    output_path="./mobile-test-reports"
)
```

## Best Practices

Test on real devices as simulators cannot replicate actual performance characteristics and hardware interactions. Cover the target device market by prioritizing popular devices and OS versions. Implement parallel test execution to reduce feedback time. Include network condition testing to ensure graceful handling of connectivity issues.

Test accessibility compliance including screen reader compatibility and keyboard navigation. Validate biometric authentication flows and fallback mechanisms. Monitor memory leaks through extended usage testing. Document device coverage matrices to ensure adequate testing across the device landscape.

## Related Skills

- Test Automation (general automation frameworks)
- Performance Testing (mobile performance metrics)
- iOS Development (iOS testing frameworks)
- Android Development (Android testing frameworks)

## Use Cases

Consumer app testing ensures apps work flawlessly across the fragmented Android market with thousands of device models. Enterprise mobile testing validates security features, VPN connectivity, and integration with enterprise systems. Gaming app testing focuses on graphics performance, touch responsiveness, and battery impact. Healthcare app testing ensures compliance with regulatory requirements and reliability of critical functionality.

## Advanced Configuration

### Appium Advanced Configuration

```python
from mobile_testing import AppiumConfig, CapabilityBuilder

# Advanced Appium configuration
config = AppiumConfig(
    server_url="http://localhost:4723",
    server_version="2.2.0",
    w3c_compliant=True,
    session_timeout=300,
    command_timeout=60,
    new_command_timeout=600,
    capabilities=CapabilityBuilder()
        .platform("iOS")
        .platform_version("17.0")
        .device_name("iPhone 15")
        .automation_name("XCUITest")
        .bundle_id("com.company.app")
        .no_reset(False)
        .full_reset(True)
        .auto_grant_permissions(True)
        .unicode_keyboard(True)
        .reset_keyboard(True)
        .build(),
)

tester = MobileTesting(appium_config=config)
```

### Device Farm Configuration

```python
from mobile_testing import DeviceFarmConfig, DeviceFilter

farm_config = DeviceFarmConfig(
    provider="AWS",
    region="us-east-1",
    project="mobile-qa",
    device_filter=DeviceFilter(
        platform=["iOS", "Android"],
        os_versions=["16.0", "17.0", "13.0", "14.0"],
        manufacturers=["Apple", "Samsung", "Google", "OnePlus"],
        min_screen_resolution=(720, 1280),
        required_features=["biometric", "nfc"],
        exclude_models=["iPhone SE", "Pixel 4a"],
    ),
    concurrency=10,
    max_runtime_minutes=60,
    artifact_retention_days=30,
)

tester.setup_device_farm(config=farm_config)
```

### Performance Monitoring Configuration

```python
from mobile_testing import PerformanceMonitor, MetricConfig

perf_config = PerformanceMonitor(
    metrics=[
        MetricConfig(name="app_launch_time", threshold_ms=2000, alert_above=True),
        MetricConfig(name="memory_usage", threshold_mb=200, alert_above=True),
        MetricConfig(name="cpu_usage", threshold_percent=80, alert_above=True),
        MetricConfig(name="battery_drain", threshold_percent_per_hour=10, alert_above=True),
        MetricConfig(name="frame_rate", threshold_fps=55, alert_below=True),
        MetricConfig(name="network_latency", threshold_ms=500, alert_above=True),
    ],
    sampling_interval_ms=1000,
    duration_seconds=300,
    warmup_seconds=30,
    baseline_comparison=True,
)

tester.configure_performance_monitoring(perf_config)
```

### Network Condition Testing

```python
from mobile_testing import NetworkCondition, NetworkSimulator

conditions = [
    NetworkCondition(name="wifi_fast", bandwidth_mbps=100, latency_ms=10, packet_loss=0.0),
    NetworkCondition(name="4g_lte", bandwidth_mbps=30, latency_ms=50, packet_loss=0.01),
    NetworkCondition(name="3g", bandwidth_mbps=1.5, latency_ms=300, packet_loss=0.02),
    NetworkCondition(name="edge", bandwidth_mbps=0.2, latency_ms=500, packet_loss=0.05),
    NetworkCondition(name="offline", bandwidth_mbps=0, latency_ms=0, packet_loss=1.0),
    NetworkCondition(name="flaky", bandwidth_mbps=10, latency_ms=100, packet_loss=0.1, intermittent=True),
]

simulator = NetworkSimulator(conditions=conditions)

for condition in conditions:
    simulator.apply(condition)
    results = tester.run_test_suite(["login", "checkout"])
    print(f"{condition.name}: {results.pass_rate:.1%} pass rate")
```

## Architecture Patterns

### Test Suite Architecture Pattern

```python
from mobile_testing import TestSuite, TestSuiteConfig

# Organized test suite
suite = TestSuite(
    name="regression_suite",
    config=TestSuiteConfig(
        parallel=True,
        max_workers=5,
        timeout_per_test=120,
        retry_failed=True,
        max_retries=2,
        artifact_collection=True,
        screenshots_on_failure=True,
        video_recording=True,
    ),
)

# Add test groups
suite.add_group("smoke", tests=["login", "home_load", "basic_navigation"])
suite.add_group("functional", tests=["checkout_flow", "search", "profile_update"])
suite.add_group("regression", tests=["all_critical_paths"])
suite.add_group("performance", tests=["app_launch", "memory_stress", "cpu_stress"])

# Execute
results = suite.execute(devices=["iPhone_15", "Pixel_8"])
print(f"Smoke: {results.group('smoke').pass_rate:.1%}")
print(f"Functional: {results.group('functional').pass_rate:.1%}")
```

### Page Object Model Pattern

```python
from mobile_testing import PageObject, Element, Gesture

class LoginPage(PageObject):
    username_field = Element(accessibility_id="username_input")
    password_field = Element(accessibility_id="password_input")
    login_button = Element(accessibility_id="login_button")
    error_message = Element(accessibility_id="error_text")
    
    def login(self, username, password):
        self.username_field.send_keys(username)
        self.password_field.send_keys(password)
        self.login_button.tap()
    
    def is_error_displayed(self):
        return self.error_message.is_visible()
    
    def get_error_text(self):
        return self.error_message.text

# Usage
login_page = LoginPage(driver)
login_page.login("user@test.com", "password")
assert login_page.is_error_displayed()
```

### Data-Driven Testing Pattern

```python
from mobile_testing import DataDrivenTest, TestDataProvider

test_data = TestDataProvider(
    data_source="test_accounts.json",
    data_format="json",
    filters={"environment": "staging", "role": ["admin", "user"]},
)

@DataDrivenTest(data_provider=test_data)
def test_login(account):
    login_page = LoginPage(driver)
    login_page.login(account["username"], account["password"])
    assert home_page.is_displayed()

# Generate test cases from data
test_cases = test_data.generate()
print(f"Generated {len(test_cases)} test cases")
```

## Integration Guide

### CI/CD Integration

```python
from mobile_testing import CICDIntegration, PipelineConfig

# GitHub Actions integration
github_config = PipelineConfig(
    provider="github_actions",
    workflow_file="mobile_tests.yml",
    trigger_events=["push", "pull_request", "schedule"],
    schedule="0 2 * * *",  # Daily at 2 AM
    environment_variables={
        "APPIUM_SERVER": "http://appium:4723",
        "DEVICE_FARM_API_KEY": "${{ secrets.DEVICE_FARM_KEY }}",
    },
)

cicd = CICDIntegration(config=github_config)
cicd.setup()
```

### Jira Integration

```python
from mobile_testing import JiraIntegration, JiraConfig

jira_config = JiraConfig(
    server="https://company.atlassian.net",
    project_key="MOBILE",
    issue_type="Bug",
    auto_create_issues=True,
    link_to_test_runs=True,
    transition_on_fix="Ready for Testing",
)

jira = JiraIntegration(config=jira_config)

# Create bug from failed test
failed_test = results.get_failed()[0]
bug = jira.create_bug(
    summary=f"Mobile test failed: {failed_test.name}",
    description=failed_test.error_message,
    priority="High",
    labels=["mobile", "automated", failed_test.device],
    attachments=failed_test.screenshots,
)
print(f"Created bug: {bug.key}")
```

### Slack Integration

```python
from mobile_testing import SlackIntegration, SlackConfig

slack_config = SlackConfig(
    webhook_url="https://hooks.slack.com/services/...",
    channel="#mobile-qa",
    mention_on_failure=["@mobile-team"],
    include_screenshots=True,
    summary_on_complete=True,
)

slack = SlackIntegration(config=slack_config)
slack.notify_results(results)
```

## Performance Optimization

### Parallel Test Execution

```python
from mobile_testing import ParallelExecutor

executor = ParallelExecutor(
    max_workers=10,
    strategy="device_pool",
    load_balancing="round_robin",
    timeout_per_test=120,
)

# Execute tests in parallel across devices
results = executor.execute(
    tests=test_suite,
    devices=device_pool,
    parallel=True,
)

print(f"Total time: {results.total_time_seconds:.1f}s")
print(f"Parallel efficiency: {results.parallel_efficiency:.1%}")
```

### Test Optimization

```python
from mobile_testing import TestOptimizer

optimizer = TestOptimizer(
    strategy="smart_selection",
    coverage_target=0.95,
    flaky_test_detection=True,
    test_prioritization=True,
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

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Appium Session Fails to Start

**Symptom**: Session creation timeout or connection refused

**Solution**:
```python
# Check Appium server status
import subprocess
result = subprocess.run(["appium", "--version"], capture_output=True, text=True)

# Verify capabilities
config.capabilities = CapabilityBuilder() \
    .platform("iOS") \
    .device_name("iPhone 15") \
    .automation_name("XCUITest") \
    .build()

# Increase timeout
config.session_timeout = 600
```

#### 2. Element Not Found

**Symptom**: NoSuchElementException during test execution

**Solution**:
```python
from mobile_testing import WaitStrategy

# Use explicit waits
wait = WaitStrategy(driver)
wait.until_element_visible(accessibility_id="login_button", timeout=30)

# Or use try-catch
try:
    element = driver.find_element(accessibility_id="login_button")
except NoSuchElementException:
    # Take screenshot and log
    driver.save_screenshot("debug.png")
    raise
```

#### 3. Flaky Tests

**Symptom**: Tests pass sometimes, fail others

**Solution**:
```python
# Add retry mechanism
suite.config.retry_failed = True
suite.config.max_retries = 3

# Use stable selectors
element = driver.find_element(accessibility_id="stable_id")  # Not xpath

# Add explicit waits
wait.until_element_clickable(element, timeout=10)
```

#### 4. Memory Leaks

**Symptom**: App crashes during extended testing

**Solution**:
```python
# Monitor memory usage
perf_monitor = PerformanceMonitor(
    metrics=[MetricConfig(name="memory_usage", threshold_mb=300)],
    continuous_monitoring=True,
)

# Take memory snapshots
memory_before = driver.get_memory_usage()
# ... run test ...
memory_after = driver.get_memory_usage()
print(f"Memory delta: {memory_after - memory_before} MB")
```

## API Reference

### Core Classes

#### `MobileTesting`
```python
class MobileTesting:
    def __init__(self, appium_config: AppiumConfig) -> None: ...
    def setup_appium(self, platform: str, capabilities: dict) -> None: ...
    def setup_device_farm(self, config: DeviceFarmConfig) -> None: ...
    def run_compatibility_test(self, devices: List[str], os_versions: List[str], test_suite: List[str]) -> TestResults: ...
    def run_performance_test(self, test_suite: List[str], duration_seconds: int) -> PerformanceResults: ...
```

#### `TestResults`
```python
@dataclass
class TestResults:
    total_tests: int
    passed: int
    failed: int
    skipped: int
    pass_rate: float
    execution_time_seconds: float
    device_results: Dict[str, DeviceResult]
    failures: List[TestFailure]
    artifacts: List[Artifact]
```

## Data Models

### Test Configuration Schema

```json
{
  "appium": {
    "server_url": "http://localhost:4723",
    "session_timeout": 300,
    "capabilities": {
      "platformName": "iOS",
      "platformVersion": "17.0",
      "deviceName": "iPhone 15",
      "automationName": "XCUITest"
    }
  },
  "device_farm": {
    "provider": "AWS",
    "concurrency": 10,
    "max_runtime_minutes": 60
  },
  "performance": {
    "metrics": ["app_launch_time", "memory_usage", "cpu_usage"],
    "sampling_interval_ms": 1000
  }
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM appium/appium:latest

RUN npm install -g appium-xcuitest-driver appium-uiautomator2-driver

COPY mobile_testing/ /app/mobile_testing/
WORKDIR /app

ENV APPIUM_HOST=0.0.0.0
ENV APPIUM_PORT=4723

EXPOSE 4723

CMD ["appium", "--address", "0.0.0.0", "--port", "4723"]
```

## Monitoring & Observability

### Metrics Collection

```python
from mobile_testing import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("mobile_test_pass_rate", type="gauge")
collector.register_metric("mobile_test_duration", type="histogram")
collector.register_metric("mobile_app_launch_time", type="histogram")
collector.register_metric("mobile_memory_usage", type="gauge")

collector.set("mobile_test_pass_rate", results.pass_rate)
collector.observe("mobile_test_duration", results.execution_time_seconds)
collector.observe("mobile_app_launch_time", launch_time_ms)
collector.set("mobile_memory_usage", memory_mb)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from mobile_testing import MobileTesting, AppiumConfig

class TestMobileTesting:
    def setup_method(self):
        self.config = AppiumConfig(server_url="http://localhost:4723")
        self.tester = MobileTesting(self.config)
    
    def test_appium_connection(self):
        self.tester.setup_appium(platform="iOS", capabilities={})
        assert self.tester.is_connected()
    
    def test_element_interaction(self):
        element = self.tester.find_element(accessibility_id="login_button")
        assert element.is_displayed()
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API
- **Added**: Network condition simulation
- **Added**: Performance monitoring
- **Improved**: 2x faster test execution
- **Fixed**: Flaky test detection

## Glossary

| Term | Definition |
|------|------------|
| **Appium** | Open-source mobile automation framework |
| **XCUITest** | iOS UI testing framework |
| **UiAutomator2** | Android UI testing framework |
| **Device Farm** | Cloud service for real device testing |
| **Flaky Test** | Test that sometimes passes, sometimes fails |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/mobile-testing.git
cd mobile-testing
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Mobile Testing Contributors

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

## Data Validation

### Test Data Validation

```python
from mobile_testing import TestDataValidator

validator = TestDataValidator()

# Validate test data
validator.validate_device_capabilities(device_config)
validator.validate_test_cases(test_suite)
validator.validate_environment(environment_config)
```

## Advanced Patterns

### Accessibility Testing

```python
from mobile_testing import AccessibilityTester, AccessibilityConfig

accessibility_config = AccessibilityConfig(
    standard="WCAG2.1",
    level="AA",
    rules=[
        "color_contrast",
        "touch_target_size",
        "screen_reader_compatibility",
        "keyboard_navigation",
        "content_labeling",
    ],
    auto_fix_suggestions=True,
)

tester = AccessibilityTester(config=accessibility_config)

# Run accessibility test
results = tester.test_accessibility()
print(f"WCAG compliance: {results.compliance_rate:.1%}")
print(f"Issues found: {results.issue_count}")
print(f"Critical issues: {results.critical_count}")
```

### Security Testing

```python
from mobile_testing import MobileSecurityTester, SecurityConfig

security_config = SecurityConfig(
    tests=[
        "data_storage_security",
        "network_security",
        "authentication_bypass",
        "certificate_pinning",
        "code_obfuscation",
        "root_detection",
        "jailbreak_detection",
    ],
    owasp_mobile_top10=True,
    scan_dependencies=True,
)

security_tester = MobileSecurityTester(config=security_config)

# Run security scan
results = security_tester.scan(app_path="app.apk")
print(f"Security score: {results.score:.1%}")
print(f"Vulnerabilities: {results.vulnerability_count}")
print(f"Critical: {results.critical_count}")
```

### Visual Regression Testing

```python
from mobile_testing import VisualRegressionTester, VisualConfig

visual_config = VisualConfig(
    baseline_dir="baselines/",
    diff_dir="diffs/",
    threshold=0.1,  # 10% pixel difference tolerance
    ignore_regions=[
        {"name": "timestamp", "selector": "#timestamp"},
        {"name": "ad_banner", "selector": "#ad-banner"},
    ],
    screenshot_options={
        "full_page": True,
        "hide_scrollbars": True,
        "background_color": "#FFFFFF",
    },
)

visual_tester = VisualRegressionTester(config=visual_config)

# Run visual test
results = visual_tester.compare(screenshot1="baseline.png", screenshot2="current.png")
print(f"Visual diff: {results.diff_percentage:.2f}%")
print(f"Regions changed: {len(results.changed_regions)}")
```

### Performance Profiling

```python
from mobile_testing import PerformanceProfiler, ProfileConfig

profile_config = ProfileConfig(
    metrics=[
        "cpu_usage",
        "memory_usage",
        "battery_drain",
        "network_usage",
        "disk_io",
        "frame_rate",
        "app_launch_time",
    ],
    sampling_interval_ms=100,
    duration_seconds=300,
    warmup_seconds=30,
)

profiler = PerformanceProfiler(config=profile_config)

# Profile app performance
results = profiler.profile()
print(f"Average CPU: {results.avg_cpu_percent:.1f}%")
print(f"Peak memory: {results.peak_memory_mb:.1f} MB")
print(f"Battery drain: {results.battery_drain_percent:.2f}%/hour")
print(f"Frame rate: {results.avg_frame_rate:.1f} FPS")
```

### Localization Testing

```python
from mobile_testing import LocalizationTester, LocaleConfig

locale_config = LocaleConfig(
    supported_locales=["en-US", "es-ES", "fr-FR", "de-DE", "ja-JP", "zh-CN"],
    test_cases=[
        "text_overflow",
        "date_format",
        "currency_format",
        "number_format",
        "rtl_support",
        "string_completeness",
    ],
    screenshot_comparison=True,
)

localization_tester = LocalizationTester(config=locale_config)

# Run localization test
results = localization_tester.test_locales()
for locale, result in results.items():
    print(f"{locale}: {result.pass_rate:.1%} pass rate")
    if result.issues:
        print(f"  Issues: {result.issues[:3]}")
```

### Push Notification Testing

```python
from mobile_testing import PushNotificationTester, PushConfig

push_config = PushConfig(
    providers={
        "ios": {
            "certificate_path": "apns_cert.p12",
            "certificate_password": "password",
            "sandbox": True,
        },
        "android": {
            "service_account_key": "service_account.json",
            "project_id": "my-project",
        },
    },
    test_scenarios=[
        "basic_notification",
        "notification_with_data",
        "notification_with_image",
        "notification_with_action",
        "notification_grouping",
        "notification_priority",
    ],
)

push_tester = PushNotificationTester(config=push_config)

# Test push notifications
results = push_tester.test_notifications(device_tokens=["token1", "token2"])
print(f"Delivery rate: {results.delivery_rate:.1%}")
print(f"Click rate: {results.click_rate:.1%}")
```

### Deep Link Testing

```python
from mobile_testing import DeepLinkTester, DeepLinkConfig

deep_link_config = DeepLinkConfig(
    schemes=["myapp", "https"],
    domains=["example.com"],
    test_links=[
        {"url": "myapp://product/123", "expected_screen": "ProductDetail"},
        {"url": "https://example.com/promo", "expected_screen": "PromoPage"},
        {"url": "myapp://settings", "expected_screen": "Settings"},
    ],
    universal_links=True,
    app_links=True,
)

deep_link_tester = DeepLinkTester(config=deep_link_config)

# Test deep links
results = deep_link_tester.test_links()
for link, result in results.items():
    print(f"{link}: {'PASS' if result.passed else 'FAIL'}")
```

### Device Compatibility Testing

```python
from mobile_testing import CompatibilityTester, DeviceMatrix

device_matrix = DeviceMatrix(
    ios=[
        {"model": "iPhone 15", "os": "17.0"},
        {"model": "iPhone 14", "os": "16.0"},
        {"model": "iPhone SE", "os": "15.0"},
        {"model": "iPad Pro", "os": "17.0"},
    ],
    android=[
        {"model": "Pixel 8", "os": "14.0"},
        {"model": "Samsung S24", "os": "14.0"},
        {"model": "OnePlus 12", "os": "13.0"},
        {"model": "Xiaomi 14", "os": "13.0"},
    ],
)

compatibility_tester = CompatibilityTester(device_matrix)

# Run compatibility tests
results = compatibility_tester.test(
    test_suite=["login", "navigation", "checkout"],
    parallel=True,
)

for device, result in results.items():
    print(f"{device}: {result.pass_rate:.1%} pass rate")
```

---
name: "Mobile Development Agent"
version: "2.0.0"
description: "Mobile app development, cross-platform strategies, app store optimization, performance monitoring, and analytics"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["mobile", "ios", "android", "flutter", "react-native", "aso", "crash-reporting"]
category: "mobile"
personality: "mobile-engineer"
use_cases:
  - "app development"
  - "build management"
  - "app store submission"
  - "crash tracking"
  - "performance monitoring"
  - "app store optimization"
  - "release management"
---

# Mobile Development Agent

> End-to-end mobile app operations from first build through store publication and production monitoring.

## Identity

**Role**: Senior Mobile Platform Engineer  
**Mindset**: User experience first, performance always, ship with confidence  
**Approach**: Build cross-platform where possible, optimize native where necessary.

---

## Core Principles

1. **Platform Awareness**: Respect each platform's conventions and guidelines
2. **Performance Budget**: Every millisecond and megabyte matters on mobile
3. **Crash-Free Target**: Maintain >99.5% crash-free session rate
4. **Store Compliance**: Follow Apple and Google guidelines strictly
5. **Continuous Delivery**: Automated builds and staged rollouts
6. **Data-Driven Iteration**: Use analytics to guide feature development

---

## Capabilities

### 1. App Management

Create, version, and manage mobile applications across platforms.

```python
from agents.mobile.agent import AppManager, Platform, AppCategory

manager = AppManager()

# Create app
app = manager.create_app(
    name="TaskMaster",
    bundle_id="com.example.taskmaster",
    platforms=[Platform.IOS, Platform.ANDROID],
    category=AppCategory.PRODUCTIVITY,
    tags=["productivity", "tasks"]
)

# Increment version
manager.increment_version(app.app_id, bump="minor")
# version: 1.0.0 → 1.1.0

# List by platform
ios_apps = manager.list_apps(platform=Platform.IOS)
```

---

### 2. Build Management

Create, execute, and track app builds.

```python
from agents.mobile.agent import BuildManager, Platform

manager = BuildManager()

# Create build
build = manager.create_build(
    app_id="app_abc123",
    platform=Platform.IOS,
    version="1.1.0",
    build_number=2,
    config={"scheme": "Release", "provisioning": "production"}
)

# Execute
manager.start_build(build.build_id)
manager.complete_build(build.build_id, success=True, artifacts=["TaskMaster.ipa"])

# Check status
build = manager.get_build(build.build_id)
print(f"Duration: {build.duration_seconds}s")
```

---

### 3. App Store Submission

Submit apps to stores with metadata optimization.

```python
from agents.mobile.agent import AppStoreManager, Platform

manager = AppStoreManager()

# Create submission
sub = manager.create_submission(
    app_id="app_abc123",
    platform=Platform.IOS,
    metadata={
        "title": "TaskMaster",
        "subtitle": "Your Productivity Companion",
        "description": "Manage tasks efficiently with TaskMaster...",
        "keywords": ["tasks", "productivity", "todo", "planner"]
    }
)

# Submit and track
manager.submit(sub.submission_id)
manager.approve(sub.submission_id)
manager.publish(sub.submission_id)

# Optimize listing
score = manager.optimize_listing(
    app_id="app_abc123",
    title="TaskMaster - Productivity",
    description="Manage your tasks efficiently",
    keywords=["tasks", "productivity", "todo"]
)
# {'overall': 0.85, 'title_optimal': True}
```

---

### 4. Crash Tracking

Report and analyze crashes.

```python
from agents.mobile.agent import CrashTracker, Platform, CrashSeverity

tracker = CrashTracker()

# Report crash
tracker.report_crash(
    app_id="app_abc123",
    platform=Platform.IOS,
    error_message="NullPointerException in LoginView",
    stack_trace="at com.app.login:42",
    severity=CrashSeverity.HIGH
)

# Get crash rate
rate = tracker.get_crash_rate("app_abc123", total_sessions=10000)
# 0.1% crash rate

# Get summary
summary = tracker.get_crash_summary("app_abc123")
# {'crash_free_rate': 99.9, 'unresolved': 1}
```

---

### 5. Performance Monitoring

Track and analyze app performance.

```python
from agents.mobile.agent import PerformanceMonitor, Platform

monitor = PerformanceMonitor()

# Record metrics
monitor.record_snapshot("app_abc123", Platform.IOS, {
    "startup_time": 1.2,
    "frame_rate": 60,
    "memory_usage": 150,
    "battery_drain": 3.5
})

# Check thresholds
violations = monitor.check_thresholds("app_abc123", {
    "startup_time": (2.0, "max"),
    "frame_rate": (30, "min")
})

# Get summary
summary = monitor.get_performance_summary("app_abc123")
# {'averages': {'startup_time': 1.2, 'frame_rate': 60}}
```

---

### 6. Test Runner

Manage and execute test suites.

```python
from agents.mobile.agent import TestRunner, TestType

runner = TestRunner()

# Create suite
suite = runner.create_suite("unit_tests", [
    {"name": "test_login", "type": "unit"},
    {"name": "test_home_screen", "type": "unit"},
    {"name": "test_api_integration", "type": "integration"}
])

# Run all tests
runner.run_suite(suite.suite_id)

# Run by type
unit_results = runner.run_tests_by_type(suite.suite_id, TestType.UNIT)

# Get coverage
coverage = runner.get_coverage(suite.suite_id)
# {'pass_rate': 100.0, 'total_tests': 3}
```

---

### 7. Analytics

Track app usage and retention.

```python
from agents.mobile.agent import AppAnalyticsDashboard

dashboard = AppAnalyticsDashboard()

# Record metrics
dashboard.record_analytics("app_abc123",
    downloads=50000,
    daily_active_users=12000,
    monthly_active_users=45000,
    session_duration_avg=8.5,
    retention_d1=40,
    retention_d7=20,
    retention_d30=8,
    rating=4.6
)

analytics = dashboard.get_analytics("app_abc123")
# {'downloads': 50000, 'rating': 4.6, 'retention_d1': 40}
```

---

### 8. App Store Optimization

Optimize discoverability and conversion.

```python
from agents.mobile.agent import ASOManager

aso = ASOManager()

# Add keywords
aso.add_keywords("app_abc123", [
    {"keyword": "task manager", "search_volume": 5000, "difficulty": 0.6},
    {"keyword": "productivity app", "search_volume": 8000, "difficulty": 0.7},
])

# Get top keywords
rankings = aso.get_keyword_rankings("app_abc123")

# Analyze listing
analysis = aso.analyze_listing(
    "TaskMaster - Productivity",
    "Your Task Companion",
    "Manage tasks efficiently...",
    ["tasks", "productivity", "todo"]
)
# {'overall_score': 0.85, 'title_optimal': True}
```

---

### 9. Release Management

Manage release notes and rollouts.

```python
from agents.mobile.agent import ReleaseManager, ReleaseChannel

manager = ReleaseManager()

# Create release
manager.create_release("app_abc123", "1.1.0",
    changes=["New calendar view", "Widget support"],
    bug_fixes=["Fixed login crash", "Fixed dark mode"],
    improvements=["Faster startup", "Reduced app size"]
)

# Format release notes
notes = manager.format_release_notes("app_abc123")

# Set rollout
manager.set_rollout("app_abc123", ReleaseChannel.BETA, 25)
```

---

## Data Models

### App
| Field | Type | Description |
|-------|------|-------------|
| app_id | str | Unique identifier |
| name | str | App name |
| bundle_id | str | Platform bundle ID |
| platforms | List[Platform] | Supported platforms |
| version | str | Semantic version |
| category | AppCategory | Store category |

### Build
| Field | Type | Description |
|-------|------|-------------|
| build_id | str | Unique identifier |
| platform | Platform | Target platform |
| status | BuildStatus | Build state |
| duration_seconds | float | Build time |
| artifacts | List[str] | Output files |

### CrashReport
| Field | Type | Description |
|-------|------|-------------|
| crash_id | str | Unique identifier |
| severity | CrashSeverity | Impact level |
| error_message | str | Error description |
| occurrence_count | int | Times seen |
| resolved | bool | Fix status |

---

## Checklists

### Pre-Release
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] UI tests covering critical paths
- [ ] Performance benchmarks met
- [ ] Crash rate below 0.1%
- [ ] App size within limits
- [ ] Store metadata updated
- [ ] Screenshots refreshed

### Store Submission
- [ ] App icon meets requirements
- [ ] Screenshots for all required sizes
- [ ] Privacy policy URL active
- [ ] App description optimized
- [ ] Keywords researched
- [ ] Age rating correct
- [ ] In-app purchases configured (if applicable)

### Post-Release
- [ ] Monitoring dashboards active
- [ ] Crash alerts configured
- [ ] Performance thresholds set
- [ ] Analytics tracking verified
- [ ] User feedback channels open

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Build fails | Missing provisioning profile | Check signing configuration |
| Store rejection | Guideline violation | Review rejection reason, fix compliance |
| High crash rate | Unhandled exception | Check crash logs, add error handling |
| Low frame rate | Expensive UI operations | Profile with Instruments, optimize |
| High memory | Memory leaks | Use Leaks instrument, fix retain cycles |
| Low retention | Poor onboarding | Redesign first-run experience |
| Low ASO score | Weak keywords | Research high-volume, low-difficulty keywords |

---

## Integration Points

| System | Purpose |
|--------|---------|
| App Store Connect | iOS submission |
| Google Play Console | Android submission |
| CI/CD Pipeline | Automated builds |
| Crash Reporting | Crashlytics/Bugsnag |
| Analytics | Firebase/Amplitude |
| Feature Flags | LaunchDarkly/Flagger |

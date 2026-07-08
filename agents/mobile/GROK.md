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
  - "test automation"
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
7. **Test Coverage**: Comprehensive testing before every release
8. **Security First**: Protect user data and privacy

---

## Capabilities

### 1. App Management

Create, version, and manage mobile applications across platforms.

```python
from agents.mobile.agent import AppManager, Platform, AppCategory

manager = AppManager()

# Create iOS app
ios_app = manager.create_app(
    name="TaskMaster",
    bundle_id="com.example.taskmaster",
    platforms=[Platform.IOS],
    category=AppCategory.PRODUCTIVITY,
    tags=["productivity", "tasks", "ios"]
)
# Returns: App(app_id="app_abc123", name="TaskMaster", version="1.0.0", ...)

# Create Android app
android_app = manager.create_app(
    name="TaskMaster",
    bundle_id="com.example.taskmaster",
    platforms=[Platform.ANDROID],
    category=AppCategory.PRODUCTIVITY,
    tags=["productivity", "tasks", "android"]
)

# Create cross-platform app
cross_app = manager.create_app(
    name="TaskMaster",
    bundle_id="com.example.taskmaster",
    platforms=[Platform.IOS, Platform.ANDROID],
    category=AppCategory.PRODUCTIVITY
)

# Increment version
manager.increment_version(ios_app.app_id, bump="minor")
# version: 1.0.0 → 1.1.0

manager.increment_version(ios_app.app_id, bump="major")
# version: 1.1.0 → 2.0.0

manager.increment_version(ios_app.app_id, bump="patch")
# version: 2.0.0 → 2.0.1

# Get app details
app = manager.get_app(ios_app.app_id)
print(f"Version: {app.version}")

# List by platform
ios_apps = manager.list_apps(platform=Platform.IOS)
android_apps = manager.list_apps(platform=Platform.ANDROID)

# Update app
manager.update_app(
    ios_app.app_id,
    tags=["productivity", "tasks", "ios", "updated"]
)
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
    config={
        "scheme": "Release",
        "provisioning": "production",
        "signing": "automatic"
    }
)
# Returns: Build(build_id="build_xyz789", status=PENDING, ...)

# Start build
manager.start_build(build.build_id)
# Status: PENDING → BUILDING

# Complete build successfully
manager.complete_build(
    build.build_id,
    success=True,
    artifacts=["TaskMaster.ipa", "dSYM.zip"]
)
# Status: BUILDING → SUCCESS

# Or mark as failed
# manager.complete_build(build.build_id, success=False, error_log="Compilation error...")

# Check status
build = manager.get_build(build.build_id)
print(f"Duration: {build.duration_seconds}s")
print(f"Status: {build.status}")
print(f"Artifacts: {build.artifacts}")

# List builds
builds = manager.list_builds(app_id="app_abc123", platform=Platform.IOS)
for b in builds:
    print(f"Build {b.build_number}: {b.status} ({b.duration_seconds}s)")
```

---

### 3. App Store Submission

Submit apps to stores with metadata optimization.

```python
from agents.mobile.agent import AppStoreManager, Platform

manager = AppStoreManager()

# Create submission with metadata
sub = manager.create_submission(
    app_id="app_abc123",
    platform=Platform.IOS,
    metadata={
        "title": "TaskMaster",
        "subtitle": "Your Productivity Companion",
        "description": "Manage tasks efficiently with TaskMaster. Organize your day, track progress, and achieve your goals.",
        "keywords": ["tasks", "productivity", "todo", "planner", "organizer"],
        "whats_new": "Version 1.1.0: Bug fixes and performance improvements",
        "privacy_url": "https://example.com/privacy",
        "support_url": "https://example.com/support"
    }
)
# Returns: Submission(submission_id="sub_abc123", status=DRAFT, ...)

# Submit to store
manager.submit(sub.submission_id)
# Status: DRAFT → SUBMITTED

# App review approves
manager.approve(sub.submission_id)
# Status: SUBMITTED → IN_REVIEW → APPROVED

# Or rejection
# manager.reject(sub.submission_id, reason="Missing privacy policy URL")

# Publish to store
manager.publish(sub.submission_id)
# Status: APPROVED → PUBLISHED

# Optimize listing for ASO
score = manager.optimize_listing(
    app_id="app_abc123",
    title="TaskMaster - Productivity",
    description="Manage your tasks efficiently with TaskMaster. Track progress and achieve goals.",
    keywords=["tasks", "productivity", "todo", "planner"]
)
# {
#   'overall': 0.85,
#   'title_optimal': True,
#   'title_length': 28,
#   'desc_optimal': True,
#   'keyword_coverage': 0.8
# }
```

---

### 4. Crash Tracking

Report and analyze crashes.

```python
from agents.mobile.agent import CrashTracker, Platform, CrashSeverity

tracker = CrashTracker()

# Report critical crash
tracker.report_crash(
    app_id="app_abc123",
    platform=Platform.IOS,
    error_message="NullPointerException in LoginView",
    stack_trace="at com.app.login.LoginView.viewDidLoad(LoginView.swift:42)\nat com.app.login.LoginView.viewWillAppear(LoginView.swift:58)",
    severity=CrashSeverity.CRITICAL
)

# Report high severity crash
tracker.report_crash(
    app_id="app_abc123",
    platform=Platform.ANDROID,
    error_message="OutOfMemoryError in ImageLoader",
    stack_trace="at com.app.image.ImageLoader.load(ImageLoader.java:128)",
    severity=CrashSeverity.HIGH
)

# Get crash rate
rate = tracker.get_crash_rate("app_abc123", total_sessions=10000)
# 0.1% crash rate (2 crashes in 10000 sessions)

# Get crash summary
summary = tracker.get_crash_summary("app_abc123")
# {
#   'total_crashes': 2,
#   'crash_free_rate': 99.9,
#   'unresolved': 2,
#   'by_severity': {
#     'CRITICAL': 1,
#     'HIGH': 1,
#     'MEDIUM': 0,
#     'LOW': 0
#   },
#   'by_platform': {
#     'ios': 1,
#     'android': 1
#   }
# }

# Resolve crash
tracker.resolve_crash(crash_id)
```

---

### 5. Performance Monitoring

Track and analyze app performance.

```python
from agents.mobile.agent import PerformanceMonitor, Platform

monitor = PerformanceMonitor()

# Record performance snapshot
monitor.record_snapshot("app_abc123", Platform.IOS, {
    "startup_time": 1.2,
    "frame_rate": 60,
    "memory_usage": 150,
    "battery_drain": 3.5,
    "network_latency": 120
})

# Record multiple snapshots over time
for i in range(10):
    monitor.record_snapshot("app_abc123", Platform.IOS, {
        "startup_time": 1.0 + (i * 0.1),
        "frame_rate": 60 - (i * 0.5),
        "memory_usage": 150 + (i * 5)
    })

# Check thresholds
violations = monitor.check_thresholds("app_abc123", {
    "startup_time": (2.0, "max"),
    "frame_rate": (30, "min"),
    "memory_usage": (200, "max")
})
# [
#   {'metric': 'frame_rate', 'value': 55.5, 'limit': 30, 'direction': 'min', 'status': 'OK'},
#   {'metric': 'memory_usage', 'value': 195, 'limit': 200, 'direction': 'max', 'status': 'OK'}
# ]

# Get performance summary
summary = monitor.get_performance_summary("app_abc123")
# {
#   'averages': {
#     'startup_time': 1.45,
#     'frame_rate': 57.25,
#     'memory_usage': 172.5
#   },
#   'latest': {
#     'startup_time': 1.9,
#     'frame_rate': 55.5,
#     'memory_usage': 195
#   },
#   'snapshots_count': 10
# }

# Get average over last N snapshots
avg = monitor.get_average("app_abc123", "startup_time", last_n=5)
# 1.7
```

---

### 6. Test Runner

Manage and execute test suites.

```python
from agents.mobile.agent import TestRunner, TestType

runner = TestRunner()

# Create test suite
suite = runner.create_suite("unit_tests", [
    {"name": "test_login", "type": "unit"},
    {"name": "test_home_screen", "type": "unit"},
    {"name": "test_api_integration", "type": "integration"},
    {"name": "test_navigation", "type": "ui"},
    {"name": "test_performance", "type": "perf"}
])
# Returns: TestSuite(suite_id="suite_abc123", total_tests=5, ...)

# Run all tests
runner.run_suite(suite.suite_id)
# All tests executed

# Run by type
unit_results = runner.run_tests_by_type(suite.suite_id, TestType.UNIT)
# [{'test': 'test_login', 'status': 'passed'}, {'test': 'test_home_screen', 'status': 'passed'}]

# Get coverage
coverage = runner.get_coverage(suite.suite_id)
# {
#   'pass_rate': 100.0,
#   'total_tests': 5,
#   'passed': 5,
#   'failed': 0,
#   'by_type': {
#     'unit': {'total': 2, 'passed': 2},
#     'integration': {'total': 1, 'passed': 1},
#     'ui': {'total': 1, 'passed': 1},
#     'perf': {'total': 1, 'passed': 1}
#   }
# }
```

---

### 7. Analytics

Track app usage and retention.

```python
from agents.mobile.agent import AppAnalyticsDashboard

dashboard = AppAnalyticsDashboard()

# Record analytics
dashboard.record_analytics("app_abc123",
    downloads=50000,
    daily_active_users=12000,
    monthly_active_users=45000,
    session_duration_avg=8.5,
    retention_d1=40,
    retention_d7=20,
    retention_d30=8,
    rating=4.6,
    revenue=25000.00
)

# Get analytics
analytics = dashboard.get_analytics("app_abc123")
# {
#   'downloads': 50000,
#   'dau': 12000,
#   'mau': 45000,
#   'session_duration_avg': 8.5,
#   'retention_d1': 40,
#   'retention_d7': 20,
#   'retention_d30': 8,
#   'rating': 4.6,
#   'revenue': 25000.00,
#   'arpu': 0.56,
#   'revenue_per_user': 2.08
# }

# Calculate retention
retention = dashboard.calculate_retention(
    "app_abc123",
    cohort_sizes=[1000, 1000, 1000],
    active_users=[400, 200, 80]
)
# {'d1': 40.0, 'd7': 20.0, 'd30': 8.0}
```

---

### 8. App Store Optimization

Optimize discoverability and conversion.

```python
from agents.mobile.agent import ASOManager

aso = ASOManager()

# Add keywords with metrics
aso.add_keywords("app_abc123", [
    {"keyword": "task manager", "search_volume": 5000, "difficulty": 0.4},
    {"keyword": "productivity app", "search_volume": 8000, "difficulty": 0.7},
    {"keyword": "todo list", "search_volume": 12000, "difficulty": 0.6},
    {"keyword": "planner", "search_volume": 6000, "difficulty": 0.5}
])

# Get keyword rankings
rankings = aso.get_keyword_rankings("app_abc123")
# [
#   {'keyword': 'task manager', 'opportunity_score': 0.6, 'recommendation': 'High opportunity'},
#   {'keyword': 'productivity app', 'opportunity_score': 0.24, 'recommendation': 'Medium opportunity'},
#   {'keyword': 'todo list', 'opportunity_score': 0.48, 'recommendation': 'High opportunity'},
#   {'keyword': 'planner', 'opportunity_score': 0.3, 'recommendation': 'Medium opportunity'}
# ]

# Get keyword suggestions
suggestions = aso.suggest_keywords("app_abc123", top_n=3)
# [
#   {'keyword': 'task manager', 'opportunity_score': 0.6, 'recommendation': 'Use in title'},
#   {'keyword': 'todo list', 'opportunity_score': 0.48, 'recommendation': 'Use in subtitle'},
#   {'keyword': 'planner', 'opportunity_score': 0.3, 'recommendation': 'Use in keywords'}
# ]

# Analyze listing
analysis = aso.analyze_listing(
    title="TaskMaster - Productivity",
    subtitle="Your Task Companion",
    description="Manage tasks efficiently with TaskMaster. Track progress and achieve goals.",
    keywords=["tasks", "productivity", "todo", "planner"]
)
# {
#   'overall_score': 0.85,
#   'title_optimal': True,
#   'title_length': 28,
#   'subtitle_optimal': True,
#   'subtitle_length': 20,
#   'keyword_coverage': 0.8,
#   'suggestions': []
# }
```

---

### 9. Release Management

Manage release notes and rollouts.

```python
from agents.mobile.agent import ReleaseManager, ReleaseChannel

manager = ReleaseManager()

# Create release
manager.create_release(
    "app_abc123",
    "1.1.0",
    changes=["New calendar view", "Widget support", "Dark mode"],
    bug_fixes=["Fixed login crash", "Fixed dark mode issues", "Fixed notification delay"],
    improvements=["Faster startup", "Reduced app size by 15%", "Improved animations"]
)

# Format release notes
notes = manager.format_release_notes("app_abc123")
# "What's New in 1.1.0\n\nNew Features:\n• New calendar view\n• Widget support\n• Dark mode\n\nBug Fixes:\n• Fixed login crash\n• Fixed dark mode issues\n• Fixed notification delay\n\nImprovements:\n• Faster startup\n• Reduced app size by 15%\n• Improved animations"

# Set rollout
manager.set_rollout("app_abc123", ReleaseChannel.BETA, 25)
# 25% of beta users receive update

manager.set_rollout("app_abc123", ReleaseChannel.PRODUCTION, 100)
# 100% of users receive update
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
| tags | List[str] | Classification tags |
| created_at | datetime | Creation timestamp |

### Build
| Field | Type | Description |
|-------|------|-------------|
| build_id | str | Unique identifier |
| app_id | str | Associated app |
| platform | Platform | Target platform |
| status | BuildStatus | Build state |
| build_number | int | Build number |
| version | str | App version |
| duration_seconds | float | Build time |
| artifacts | List[str] | Output files |
| config | Dict | Build configuration |

### CrashReport
| Field | Type | Description |
|-------|------|-------------|
| crash_id | str | Unique identifier |
| app_id | str | Associated app |
| platform | Platform | Platform |
| severity | CrashSeverity | Impact level |
| error_message | str | Error description |
| stack_trace | str | Stack trace |
| occurrence_count | int | Times seen |
| resolved | bool | Fix status |

### PerformanceSnapshot
| Field | Type | Description |
|-------|------|-------------|
| snapshot_id | str | Unique identifier |
| app_id | str | Associated app |
| platform | Platform | Platform |
| metrics | Dict[str, float] | Performance metrics |
| timestamp | datetime | Measurement time |

### TestSuite
| Field | Type | Description |
|-------|------|-------------|
| suite_id | str | Unique identifier |
| name | str | Suite name |
| tests | List[Dict] | Test definitions |
| total_tests | int | Test count |
| status | str | Execution status |

### ASOKeyword
| Field | Type | Description |
|-------|------|-------------|
| keyword | str | Keyword text |
| search_volume | int | Monthly searches |
| difficulty | float | Competition 0.0-1.0 |
| opportunity_score | float | Calculated opportunity |

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
- [ ] Privacy policy current
- [ ] API keys rotated

### Store Submission
- [ ] App icon meets requirements (1024x1024)
- [ ] Screenshots for all required sizes
- [ ] Privacy policy URL active
- [ ] App description optimized
- [ ] Keywords researched
- [ ] Age rating correct
- [ ] In-app purchases configured (if applicable)
- [ ] App category selected
- [ ] Contact information provided

### Post-Release
- [ ] Monitoring dashboards active
- [ ] Crash alerts configured
- [ ] Performance thresholds set
- [ ] Analytics tracking verified
- [ ] User feedback channels open
- [ ] Crash-free rate > 99.5%
- [ ] No new critical issues

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
| Build timeout | Large project | Optimize build settings, use caching |
| Submission timeout | App review backlog | Wait, or expedite if available |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = MobileAgent()
# Now all operations will log detailed debug information
```

---

## Integration Points

| System | Purpose |
|--------|---------|
| App Store Connect | iOS submission and management |
| Google Play Console | Android submission and management |
| CI/CD Pipeline | Automated builds (GitHub Actions, Jenkins) |
| Crash Reporting | Crashlytics, Bugsnag, Sentry |
| Analytics | Firebase Analytics, Amplitude, Mixpanel |
| Feature Flags | LaunchDarkly, Flagger |
| A/B Testing | Firebase Remote Config, Optimizely |
| Beta Distribution | TestFlight, Firebase App Distribution |

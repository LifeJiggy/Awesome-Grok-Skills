# Mobile Development Agent

Mobile app development, cross-platform strategies, app store optimization, performance monitoring, and analytics.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
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

The Mobile Development Agent provides a complete mobile app operations platform covering creation, building, testing, store submission, crash tracking, performance monitoring, analytics, and app store optimization.

### Key Capabilities

| Capability | Description |
|-----------|-------------|
| App Management | Create and version apps across platforms |
| Build Management | Execute and track builds |
| Store Submission | Submit to App Store and Play Store |
| Crash Tracking | Report and analyze crashes |
| Performance Monitoring | Track startup, memory, frame rate |
| Test Runner | Execute test suites with coverage |
| Analytics | Track usage, retention, revenue |
| ASO | Optimize store discoverability |
| Releases | Manage release notes and rollouts |

---

## Features

### Multi-Platform Support
- iOS, Android, React Native, Flutter, Kotlin Multiplatform, Web
- Platform-specific build configurations
- Unified management across platforms

### Store Integration
- App Store Connect and Google Play Console workflows
- Submission lifecycle tracking (draft → published)
- Listing optimization with ASO scoring

### Crash Intelligence
- Severity classification (critical, high, medium, low)
- Crash-free rate calculation
- Device info tracking
- Resolution workflow

### Performance Budgets
- Configurable thresholds per metric
- Automatic violation detection
- Historical trend analysis
- Average calculations over time windows

### Test Coverage
- 6 test types: unit, integration, UI, end-to-end, performance, security
- Per-type execution and reporting
- Coverage percentage tracking

### Analytics
- Downloads, DAU, MAU, session duration
- D1/D7/D30 retention tracking
- Revenue metrics
- Rating monitoring

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│             MobileAgent (Facade)                 │
├─────────────────────────────────────────────────┤
│  AppManager      │  BuildManager                │
│  AppStoreManager │  CrashTracker                │
│  PerformanceMonitor │  TestRunner               │
│  AppAnalyticsDashboard │  ASOManager            │
│  ReleaseManager                             │
└─────────────────────────────────────────────────┘
```

---

## Quick Start

### Installation

```bash
pip install awesome-grok-skills
```

### Minimal Example

```python
from agents.mobile.agent import MobileAgent, Platform

agent = MobileAgent()

# Create and publish app
result = agent.full_release_cycle(
    app_name="MyApp",
    bundle_id="com.example.myapp",
    platform=Platform.IOS,
    version="1.0.0",
    metadata={"title": "MyApp", "description": "A great app"}
)
print(f"Published: {result['status']}")
```

---

## Usage

### Running the Agent

```bash
python agents/mobile/agent.py
```

### Programmatic Access

```python
from agents.mobile.agent import MobileAgent

agent = MobileAgent()

# Each component works independently
app = agent.apps.create_app("MyApp", "com.example.myapp", [Platform.IOS])
build = agent.builds.create_build(app.app_id, Platform.IOS, "1.0.0", 1)
```

---

## API Reference

### MobileAgent

| Method | Description |
|--------|-------------|
| `full_release_cycle(name, bundle, platform, version, metadata)` | End-to-end release workflow |

### AppManager

| Method | Description |
|--------|-------------|
| `create_app(name, bundle_id, platforms, category)` | Create app |
| `get_app(app_id)` | Get app details |
| `update_app(app_id, **kwargs)` | Update app fields |
| `increment_version(app_id, bump)` | Bump version |
| `list_apps(platform)` | List apps by platform |

### BuildManager

| Method | Description |
|--------|-------------|
| `create_build(app_id, platform, version, build_num)` | Create build |
| `start_build(build_id)` | Start build |
| `complete_build(build_id, success, artifacts)` | Complete build |
| `list_builds(app_id, platform)` | List builds |

### AppStoreManager

| Method | Description |
|--------|-------------|
| `create_submission(app_id, platform, metadata)` | Create submission |
| `submit(submission_id)` | Submit to store |
| `approve(submission_id)` | Mark approved |
| `reject(submission_id, reason)` | Mark rejected |
| `publish(submission_id)` | Publish app |
| `optimize_listing(app_id, title, desc, keywords)` | ASO analysis |

### CrashTracker

| Method | Description |
|--------|-------------|
| `report_crash(app_id, platform, error, stack)` | Report crash |
| `resolve_crash(crash_id)` | Mark resolved |
| `get_crash_rate(app_id, sessions)` | Calculate crash rate |
| `get_crash_summary(app_id)` | Full crash summary |

### PerformanceMonitor

| Method | Description |
|--------|-------------|
| `record_snapshot(app_id, platform, metrics)` | Record metrics |
| `get_latest(app_id)` | Latest snapshot |
| `get_average(app_id, metric, last_n)` | Average metric |
| `check_thresholds(app_id, thresholds)` | Check violations |

### TestRunner

| Method | Description |
|--------|-------------|
| `create_suite(name, tests)` | Create test suite |
| `run_suite(suite_id)` | Run all tests |
| `run_tests_by_type(suite_id, type)` | Run by type |
| `get_coverage(suite_id)` | Get coverage |

### AppAnalyticsDashboard

| Method | Description |
|--------|-------------|
| `record_analytics(app_id, **kwargs)` | Record metrics |
| `get_analytics(app_id)` | Get app analytics |
| `calculate_retention(app_id, sizes, active)` | Calculate retention |

### ASOManager

| Method | Description |
|--------|-------------|
| `add_keywords(app_id, keywords)` | Add keywords |
| `get_keyword_rankings(app_id)` | Get rankings |
| `suggest_keywords(app_id, top_n)` | Get suggestions |
| `analyze_listing(title, subtitle, desc, kws)` | Analyze listing |

### ReleaseManager

| Method | Description |
|--------|-------------|
| `create_release(app_id, version, changes)` | Create release |
| `format_release_notes(app_id)` | Format notes |
| `set_rollout(app_id, channel, percentage)` | Set rollout |

---

## Examples

### Cross-Platform Release

```python
agent = MobileAgent()

for platform in [Platform.IOS, Platform.ANDROID]:
    result = agent.full_release_cycle(
        f"CrossApp", f"com.example.crossapp.{platform.value}",
        platform, "1.0.0", {"title": "CrossApp"}
    )
    print(f"{platform.value}: {result['status']}")
```

### Crash Monitoring Workflow

```python
agent = MobileAgent()
agent.crashes.report_crash("app_1", Platform.IOS, "NullPointer", "at login:42")
agent.crashes.report_crash("app_1", Platform.ANDROID, "OutOfMemory", "at home:15")

summary = agent.crashes.get_crash_summary("app_1")
print(f"Crash-free: {summary['crash_free_rate']}%")
print(f"Unresolved: {summary['unresolved']}")
```

### Performance Budget

```python
agent = MobileAgent()

# Record multiple snapshots
for _ in range(10):
    agent.performance.record_snapshot("app_1", Platform.IOS, {
        "startup_time": 1.5, "frame_rate": 58, "memory_usage": 180
    })

# Check against budget
violations = agent.performance.check_thresholds("app_1", {
    "startup_time": (2.0, "max"),
    "frame_rate": (30, "min"),
    "memory_usage": (200, "max")
})
print(f"Violations: {len(violations)}")
```

### ASO Optimization

```python
agent = MobileAgent()

# Add keywords with metrics
agent.aso.add_keywords("app_1", [
    {"keyword": "task manager", "search_volume": 5000, "difficulty": 0.4},
    {"keyword": "productivity", "search_volume": 10000, "difficulty": 0.8},
])

# Get top opportunities
suggestions = agent.aso.suggest_keywords("app_1", top_n=5)
for s in suggestions:
    print(f"{s['keyword']}: {s['recommendation']}")
```

---

## Configuration

### Supported Platforms

| Platform | Bundle Format | Store |
|----------|--------------|-------|
| iOS | .ipa | App Store Connect |
| Android | .apk/.aab | Google Play Console |
| React Native | Platform-dependent | Both stores |
| Flutter | Platform-dependent | Both stores |
| Kotlin Multiplatform | Platform-dependent | Both stores |
| Web | PWA manifest | N/A |

### Performance Thresholds (Defaults)

| Metric | Max | Min |
|--------|-----|-----|
| Startup time | 2.0s | - |
| Frame rate | - | 30 FPS |
| Memory usage | 200MB | - |
| Battery drain | 5%/hour | - |

### Crash Severity Levels

| Level | Definition |
|-------|-----------|
| CRITICAL | App unusable |
| HIGH | Major feature broken |
| MEDIUM | Intermittent issue |
| LOW | Minor cosmetic |

---

## Best Practices

### App Management
- Use semantic versioning (major.minor.patch)
- Prefix bundle IDs with reverse domain
- Tag apps for categorization
- Increment build numbers for each upload

### Build Management
- Always use Release scheme for production builds
- Archive artifacts for every successful build
- Track build duration trends
- Use separate configs for staging/production

### Store Submission
- Follow Apple Human Interface Guidelines
- Follow Google Material Design guidelines
- Optimize screenshots for each device size
- Write clear, keyword-rich descriptions

### Crash Tracking
- Set up daily crash rate alerts
- Prioritize critical and high severity crashes
- Track device/OS distribution
- Verify fixes with regression tests

### Performance
- Set startup time budget < 2 seconds
- Maintain 60 FPS on mid-range devices
- Monitor memory warnings
- Test on real devices, not just simulators

### ASO
- Research keywords before writing descriptions
- Update keywords with each release
- A/B test screenshots and descriptions
- Monitor competitor rankings

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Build fails on CI | Provisioning profile expired | Renew certificates and profiles |
| Store rejected | Missing privacy URL | Add privacy policy link to metadata |
| High crash rate | Uncaught exception | Add try/catch, use crash reporting |
| Low frame rate |主线程阻塞 | Move work to background threads |
| High memory | Retain cycles | Profile with Instruments, fix leaks |
| Low retention | Bad onboarding | Redesign first-run experience |
| Low ASO | Weak keywords | Research high-volume opportunities |
| Submission timeout | App review backlog | Wait, or expedite if available |

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.

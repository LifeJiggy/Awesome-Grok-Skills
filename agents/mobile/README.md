# Mobile Development Agent

Mobile app development, cross-platform strategies, app store optimization, performance monitoring, and analytics.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [Contributing](#contributing)
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

### System Requirements

- Python 3.10 or higher
- 256 MB RAM minimum
- 50 MB disk space
- Network access for store APIs (optional)

---

## Features

### Multi-Platform Support
- iOS, Android, React Native, Flutter, Kotlin Multiplatform, Web
- Platform-specific build configurations
- Unified management across platforms
- Semantic versioning with auto-increment

### Store Integration
- App Store Connect and Google Play Console workflows
- Submission lifecycle tracking (draft → published)
- Listing optimization with ASO scoring
- Rejection handling with reason tracking

### Crash Intelligence
- Severity classification (critical, high, medium, low)
- Crash-free rate calculation
- Device info tracking
- Resolution workflow
- Crash rate monitoring

### Performance Budgets
- Configurable thresholds per metric
- Automatic violation detection
- Historical trend analysis
- Average calculations over time windows
- 8 tracked metrics (startup, FPS, memory, battery, etc.)

### Test Coverage
- 6 test types: unit, integration, UI, end-to-end, performance, security
- Per-type execution and reporting
- Coverage percentage tracking
- Suite management

### Analytics
- Downloads, DAU, MAU, session duration
- D1/D7/D30 retention tracking
- Revenue metrics (ARPU, LTV)
- Rating monitoring
- Revenue per user calculations

### App Store Optimization
- Keyword tracking with opportunity scoring
- Listing analysis and recommendations
- Keyword suggestions based on volume/difficulty
- Title and description optimization

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│             MobileAgent (Facade)                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │  AppManager    │  │ BuildManager   │  │AppStoreManager │    │
│  │                │  │                │  │                │    │
│  │  Create        │  │ Execute        │  │ Submit         │    │
│  │  Version       │  │ Track          │  │ Review         │    │
│  │  Platform      │  │ Artifacts      │  │ Publish        │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │ CrashTracker   │  │PerformanceMon. │  │  TestRunner    │    │
│  │                │  │                │  │                │    │
│  │ Report         │  │ Metrics        │  │ Suites         │    │
│  │ Classify       │  │ Thresholds     │  │ Coverage       │    │
│  │ Resolve        │  │ Violations     │  │ Results        │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
│                                                                  │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐    │
│  │AnalyticsDashbrd│  │  ASOManager    │  │ ReleaseManager │    │
│  │                │  │                │  │                │    │
│  │ Downloads      │  │ Keywords       │  │ Notes          │    │
│  │ Retention      │  │ Listings       │  │ Rollout        │    │
│  │ Revenue        │  │ Rankings       │  │ Channels       │    │
│  └────────────────┘  └────────────────┘  └────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Component Interaction Flow

```
Release Request
     │
     ▼
MobileAgent (facade)
     │
     ├──→ AppManager.create_app()
     │         │
     │         ▼
     │    App (v1.0.0)
     │
     ├──→ BuildManager.create_build()
     │         │
     │         ▼
     │    Build (PENDING)
     │
     ├──→ BuildManager.start_build()
     │         │
     │         ▼
     │    Build (BUILDING)
     │
     ├──→ BuildManager.complete_build()
     │         │
     │         ▼
     │    Build (SUCCESS)
     │
     ├──→ TestRunner.run_suite()
     │         │
     │         ▼
     │    All tests passed
     │
     ├──→ AppStoreManager.create_submission()
     │         │
     │         ▼
     │    Submission (DRAFT)
     │
     ├──→ AppStoreManager.submit()
     │         │
     │         ▼
     │    Submission (SUBMITTED)
     │
     ├──→ AppStoreManager.publish()
     │         │
     │         ▼
     │    App (PUBLISHED)
     │
     └──→ CrashTracker + PerformanceMonitor (ongoing)
               │
               ▼
          Production monitoring
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

### 60-Second Setup

```python
from agents.mobile.agent import MobileAgent, Platform

agent = MobileAgent()

# Quick app creation
app = agent.apps.create_app("QuickApp", "com.example.quick", [Platform.IOS])

# Quick build
build = agent.builds.create_build(app.app_id, Platform.IOS, "1.0.0", 1)
agent.builds.complete_build(build.build_id, success=True, artifacts=["QuickApp.ipa"])

print(f"App: {app.app_id}, Build: {build.build_id}")
```

---

## Installation

### From PyPI

```bash
pip install awesome-grok-skills
```

### From Source

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Requirements

```
Python >= 3.10
No external dependencies (stdlib only)
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
agent.crashes.report_crash(app.app_id, Platform.IOS, "Error", "stack")
agent.analytics.record_analytics(app.app_id, downloads=1000)
```

### CLI Usage

```bash
# List all apps
python agents/mobile/agent.py --list-apps

# Check crash rate
python agents/mobile/agent.py --crash-rate app_abc123

# Generate ASO report
python agents/mobile/agent.py --aso-report app_abc123
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
| `get_build(build_id)` | Get build details |
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
| `report_crash(app_id, platform, error, stack, severity)` | Report crash |
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
| `get_performance_summary(app_id)` | Full summary |

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
| `create_release(app_id, version, changes, fixes, improvements)` | Create release |
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
        platform, "1.0.0", {"title": "CrossApp", "description": "Cross-platform app"}
    )
    print(f"{platform.value}: {result['status']}")
```

### Crash Monitoring Workflow

```python
agent = MobileAgent()

# Report crashes
agent.crashes.report_crash("app_1", Platform.IOS, "NullPointer", "at login:42", CrashSeverity.HIGH)
agent.crashes.report_crash("app_1", Platform.ANDROID, "OutOfMemory", "at home:15", CrashSeverity.MEDIUM)

# Get summary
summary = agent.crashes.get_crash_summary("app_1")
print(f"Crash-free: {summary['crash_free_rate']}%")
print(f"Unresolved: {summary['unresolved']}")
print(f"By severity: {summary['by_severity']}")
```

### Performance Budget

```python
agent = MobileAgent()

# Record multiple snapshots
for _ in range(10):
    agent.performance.record_snapshot("app_1", Platform.IOS, {
        "startup_time": 1.5,
        "frame_rate": 58,
        "memory_usage": 180,
        "battery_drain": 4.0
    })

# Check against budget
violations = agent.performance.check_thresholds("app_1", {
    "startup_time": (2.0, "max"),
    "frame_rate": (30, "min"),
    "memory_usage": (200, "max"),
    "battery_drain": (5.0, "max")
})
print(f"Violations: {len(violations)}")

# Get summary
summary = agent.performance.get_performance_summary("app_1")
print(f"Averages: {summary['averages']}")
```

### ASO Optimization

```python
agent = MobileAgent()

# Add keywords with metrics
agent.aso.add_keywords("app_1", [
    {"keyword": "task manager", "search_volume": 5000, "difficulty": 0.4},
    {"keyword": "productivity", "search_volume": 10000, "difficulty": 0.8},
    {"keyword": "todo list", "search_volume": 8000, "difficulty": 0.5},
])

# Get top opportunities
suggestions = agent.aso.suggest_keywords("app_1", top_n=3)
for s in suggestions:
    print(f"{s['keyword']}: {s['recommendation']} (score: {s['opportunity_score']:.2f})")

# Analyze listing
analysis = agent.aso.analyze_listing(
    title="TaskMaster - Productivity",
    subtitle="Your Task Companion",
    description="Manage tasks efficiently",
    keywords=["tasks", "productivity", "todo"]
)
print(f"Score: {analysis['overall_score']:.2f}")
```

### Complete Release Workflow

```python
agent = MobileAgent()

# 1. Create app
app = agent.apps.create_app("MyApp", "com.example.myapp", [Platform.IOS])

# 2. Build
build = agent.builds.create_build(app.app_id, Platform.IOS, "1.0.0", 1)
agent.builds.start_build(build.build_id)
agent.builds.complete_build(build.build_id, success=True, artifacts=["MyApp.ipa"])

# 3. Test
suite = agent.tests.create_suite("release", [
    {"name": "test_login", "type": "unit"},
    {"name": "test_ui", "type": "ui"},
])
agent.tests.run_suite(suite.suite_id)
coverage = agent.tests.get_coverage(suite.suite_id)
print(f"Test pass rate: {coverage['pass_rate']}%")

# 4. Submit
sub = agent.stores.create_submission(app.app_id, Platform.IOS, {
    "title": "MyApp",
    "description": "A great app",
    "keywords": ["productivity", "tasks"]
})
agent.stores.submit(sub.submission_id)
agent.stores.approve(sub.submission_id)
agent.stores.publish(sub.submission_id)

# 5. Monitor
agent.crashes.report_crash(app.app_id, Platform.IOS, "Error", "stack")
agent.performance.record_snapshot(app.app_id, Platform.IOS, {"startup_time": 1.2})

# 6. Analyze
analytics = agent.analytics.get_analytics(app.app_id)
print(f"Downloads: {analytics['downloads']}, Rating: {analytics['rating']}")
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

| Metric | Max | Min | Direction |
|--------|-----|-----|-----------|
| Startup time | 2.0s | - | max |
| Frame rate | - | 30 FPS | min |
| Memory usage | 200MB | - | max |
| Battery drain | 5%/hour | - | max |
| Network latency | 500ms | - | max |
| App size | 150MB | - | max |
| Crash rate | 0.5% | - | max |
| ANR rate | 0.1% | - | max |

### Crash Severity Levels

| Level | Definition | Response Time |
|-------|-----------|---------------|
| CRITICAL | App unusable | Immediate |
| HIGH | Major feature broken | 24 hours |
| MEDIUM | Intermittent issue | 1 week |
| LOW | Minor cosmetic | Next release |

### Release Channels

| Channel | Purpose | Audience |
|---------|---------|----------|
| INTERNAL | Internal testing | Team only |
| ALPHA | Early testing | Internal + close partners |
| BETA | Pre-release testing | External beta users |
| RC | Release candidate | Production subset |
| PRODUCTION | Full release | All users |

### Test Types

| Type | Purpose | Example |
|------|---------|---------|
| UNIT | Individual functions | Login validation |
| INTEGRATION | Component interaction | API + UI |
| UI | User interface | Button clicks |
| END_TO_END | Full workflow | Login → Dashboard → Logout |
| PERF | Performance benchmarks | Load time, memory |
| SECURITY | Vulnerability scans | SQL injection, XSS |

---

## Best Practices

### App Management
- Use semantic versioning (major.minor.patch)
- Prefix bundle IDs with reverse domain
- Tag apps for categorization
- Increment build numbers for each upload
- Document app purpose and target audience

### Build Management
- Always use Release scheme for production builds
- Archive artifacts for every successful build
- Track build duration trends
- Use separate configs for staging/production
- Implement build caching for faster builds

### Store Submission
- Follow Apple Human Interface Guidelines
- Follow Google Material Design guidelines
- Optimize screenshots for each device size
- Write clear, keyword-rich descriptions
- Test metadata before submission

### Crash Tracking
- Set up daily crash rate alerts
- Prioritize critical and high severity crashes
- Track device/OS distribution
- Verify fixes with regression tests
- Monitor crash-free rate target > 99.5%

### Performance
- Set startup time budget < 2 seconds
- Maintain 60 FPS on mid-range devices
- Monitor memory warnings
- Test on real devices, not just simulators
- Profile before and after optimization

### ASO
- Research keywords before writing descriptions
- Update keywords with each release
- A/B test screenshots and descriptions
- Monitor competitor rankings
- Track keyword position changes

### Testing
- Maintain > 80% code coverage
- Run tests on every commit
- Use CI/CD for automated testing
- Test on multiple device sizes
- Include accessibility tests

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Build fails on CI | Provisioning profile expired | Renew certificates and profiles |
| Store rejected | Missing privacy URL | Add privacy policy link to metadata |
| High crash rate | Uncaught exception | Add try/catch, use crash reporting |
| Low frame rate | Main thread blocking | Move work to background threads |
| High memory | Retain cycles | Profile with Instruments, fix leaks |
| Low retention | Bad onboarding | Redesign first-run experience |
| Low ASO | Weak keywords | Research high-volume opportunities |
| Submission timeout | App review backlog | Wait, or expedite if available |
| Build timeout | Large project | Optimize build settings |
| Test failures | Flaky tests | Isolate and fix flaky tests |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = MobileAgent()
# Now all operations will log detailed debug information
```

---

## FAQ

### Q: Can I manage multiple platforms for one app?
A: Yes, create an app with multiple platforms in the platforms parameter.

### Q: How do I handle platform-specific builds?
A: Create separate builds for each platform with platform-specific configs.

### Q: What's the recommended crash-free rate?
A: Target > 99.5% crash-free sessions. Apple and Google both expect high stability.

### Q: Can I automate store submissions?
A: Yes, use the API to programmatically submit and track submissions.

### Q: How do I optimize ASO?
A: Research keywords, optimize title/description, track rankings, iterate.

### Q: Can I integrate with CI/CD?
A: Yes, the agent can be called from CI/CD pipelines for automated workflows.

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](../../CONTRIBUTING.md) for details.

### Development Setup

```bash
git clone https://github.com/awesome-grok-skills/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e ".[dev]"
pre-commit install
```

### Running Tests

```bash
pytest tests/mobile/
pytest --cov=agents.mobile
```

---

## License

MIT License - see [LICENSE](../../LICENSE) for details.

---

## Support

- Documentation: [docs.example.com](https://docs.example.com)
- Issues: [GitHub Issues](https://github.com/awesome-grok-skills/awesome-grok-skills/issues)
- Discussions: [GitHub Discussions](https://github.com/awesome-grok-skills/awesome-grok-skills/discussions)

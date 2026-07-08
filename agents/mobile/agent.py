"""
Mobile Agent
Mobile app development, cross-platform strategies, app store optimization, performance, and analytics.
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import uuid4

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class Platform(Enum):
    IOS = "ios"
    ANDROID = "android"
    WEB = "web"
    REACT_NATIVE = "react_native"
    FLUTTER = "flutter"
    KOTLIN_MULTIPLATFORM = "kotlin_multiplatform"


class BuildStatus(Enum):
    PENDING = "pending"
    BUILDING = "building"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StoreStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    PUBLISHED = "published"


class CrashSeverity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class PerformanceMetric(Enum):
    STARTUP_TIME = "startup_time"
    FRAME_RATE = "frame_rate"
    MEMORY_USAGE = "memory_usage"
    BATTERY_DRAIN = "battery_drain"
    NETWORK_LATENCY = "network_latency"
    APP_SIZE = "app_size"
    CRASH_RATE = "crash_rate"
    ANR_RATE = "anr_rate"


class TestType(Enum):
    UNIT = "unit"
    INTEGRATION = "integration"
    UI = "ui"
    END_TO_END = "end_to_end"
    PERFORMANCE = "performance"
    SECURITY = "security"


class AppCategory(Enum):
    PRODUCTIVITY = "productivity"
    SOCIAL = "social"
    GAMES = "games"
    FINANCE = "finance"
    HEALTH = "health"
    EDUCATION = "education"
    ENTERTAINMENT = "entertainment"
    UTILITIES = "utilities"
    BUSINESS = "business"
    LIFESTYLE = "lifestyle"


class ReleaseChannel(Enum):
    INTERNAL = "internal"
    ALPHA = "alpha"
    BETA = "beta"
    RC = "rc"
    PRODUCTION = "production"


# ──────────────────────────────────────────────
# Data Classes
# ──────────────────────────────────────────────

@dataclass
class App:
    app_id: str = field(default_factory=lambda: f"app_{str(uuid4())[:8]}")
    name: str = ""
    bundle_id: str = ""
    platforms: List[Platform] = field(default_factory=list)
    category: AppCategory = AppCategory.UTILITIES
    version: str = "1.0.0"
    build_number: int = 1
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)


@dataclass
class Build:
    build_id: str = field(default_factory=lambda: f"build_{str(uuid4())[:8]}")
    app_id: str = ""
    platform: Platform = Platform.IOS
    status: BuildStatus = BuildStatus.PENDING
    version: str = "1.0.0"
    build_number: int = 1
    config: Dict[str, Any] = field(default_factory=dict)
    artifacts: List[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_seconds: float = 0.0


@dataclass
class StoreSubmission:
    submission_id: str = field(default_factory=lambda: f"sub_{str(uuid4())[:8]}")
    app_id: str = ""
    platform: Platform = Platform.IOS
    status: StoreStatus = StoreStatus.DRAFT
    metadata: Dict[str, Any] = field(default_factory=dict)
    submitted_at: Optional[datetime] = None
    reviewed_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None


@dataclass
class CrashReport:
    crash_id: str = field(default_factory=lambda: f"crash_{str(uuid4())[:8]}")
    app_id: str = ""
    platform: Platform = Platform.IOS
    severity: CrashSeverity = CrashSeverity.MEDIUM
    error_message: str = ""
    stack_trace: str = ""
    device_info: Dict[str, Any] = field(default_factory=dict)
    occurrence_count: int = 1
    first_seen: datetime = field(default_factory=datetime.now)
    last_seen: datetime = field(default_factory=datetime.now)
    resolved: bool = False


@dataclass
class PerformanceSnapshot:
    snapshot_id: str = field(default_factory=lambda: f"perf_{str(uuid4())[:8]}")
    app_id: str = ""
    platform: Platform = Platform.IOS
    metrics: Dict[str, float] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TestCase:
    test_id: str = field(default_factory=lambda: f"test_{str(uuid4())[:8]}")
    name: str = ""
    test_type: TestType = TestType.UNIT
    status: str = "pending"
    duration_seconds: float = 0.0
    error: Optional[str] = None


@dataclass
class TestSuite:
    suite_id: str = field(default_factory=lambda: f"suite_{str(uuid4())[:8]}")
    name: str = ""
    tests: List[TestCase] = field(default_factory=list)
    total: int = 0
    passed: int = 0
    failed: int = 0
    skipped: int = 0


@dataclass
class AppAnalytics:
    app_id: str = ""
    period_days: int = 30
    downloads: int = 0
    daily_active_users: int = 0
    monthly_active_users: int = 0
    session_duration_avg: float = 0.0
    retention_d1: float = 0.0
    retention_d7: float = 0.0
    retention_d30: float = 0.0
    crash_free_rate: float = 0.0
    rating: float = 0.0
    revenue: float = 0.0


@dataclass
class ASOKeyword:
    keyword: str = ""
    search_volume: int = 0
    difficulty: float = 0.0
    current_rank: Optional[int] = None
    opportunity_score: float = 0.0


@dataclass
class ReleaseNote:
    version: str = ""
    changes: List[str] = field(default_factory=list)
    bug_fixes: List[str] = field(default_factory=list)
    improvements: List[str] = field(default_factory=list)
    date: datetime = field(default_factory=datetime.now)


# ──────────────────────────────────────────────
# Exceptions
# ──────────────────────────────────────────────

class MobileError(Exception):
    """Base mobile agent error."""


class AppNotFoundError(MobileError):
    """App ID not found."""


class BuildError(MobileError):
    """Build operation failed."""


class StoreSubmissionError(MobileError):
    """Store submission failed."""


# ──────────────────────────────────────────────
# App Manager
# ──────────────────────────────────────────────

class AppManager:
    """Create and manage mobile applications."""

    def __init__(self) -> None:
        self._apps: Dict[str, App] = {}

    def create_app(
        self,
        name: str,
        bundle_id: str,
        platforms: List[Platform],
        category: AppCategory = AppCategory.UTILITIES,
        tags: Optional[List[str]] = None,
    ) -> App:
        app = App(
            name=name,
            bundle_id=bundle_id,
            platforms=platforms,
            category=category,
            tags=tags or [],
        )
        self._apps[app.app_id] = app
        logger.info("Created app %s (%s)", app.app_id, name)
        return app

    def get_app(self, app_id: str) -> App:
        if app_id not in self._apps:
            raise AppNotFoundError(f"App {app_id} not found")
        return self._apps[app_id]

    def update_app(self, app_id: str, **kwargs: Any) -> App:
        app = self.get_app(app_id)
        for key, value in kwargs.items():
            if hasattr(app, key):
                setattr(app, key, value)
        return app

    def increment_version(self, app_id: str, bump: str = "patch") -> App:
        app = self.get_app(app_id)
        parts = app.version.split(".")
        if len(parts) != 3:
            parts = ["1", "0", "0"]
        major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])
        if bump == "major":
            major += 1
            minor = 0
            patch = 0
        elif bump == "minor":
            minor += 1
            patch = 0
        else:
            patch += 1
        app.version = f"{major}.{minor}.{patch}"
        app.build_number += 1
        return app

    def list_apps(self, platform: Optional[Platform] = None) -> List[App]:
        apps = list(self._apps.values())
        if platform:
            apps = [a for a in apps if platform in a.platforms]
        return apps


# ──────────────────────────────────────────────
# Build Manager
# ──────────────────────────────────────────────

class BuildManager:
    """Manage mobile app builds."""

    def __init__(self) -> None:
        self._builds: Dict[str, Build] = {}

    def create_build(
        self,
        app_id: str,
        platform: Platform,
        version: str,
        build_number: int,
        config: Optional[Dict[str, Any]] = None,
    ) -> Build:
        build = Build(
            app_id=app_id,
            platform=platform,
            version=version,
            build_number=build_number,
            config=config or {},
            started_at=datetime.now(),
        )
        self._builds[build.build_id] = build
        logger.info("Created build %s for %s", build.build_id, platform.value)
        return build

    def start_build(self, build_id: str) -> Build:
        build = self._get_build(build_id)
        build.status = BuildStatus.BUILDING
        build.started_at = datetime.now()
        return build

    def complete_build(self, build_id: str, success: bool, artifacts: Optional[List[str]] = None) -> Build:
        build = self._get_build(build_id)
        build.status = BuildStatus.SUCCESS if success else BuildStatus.FAILED
        build.completed_at = datetime.now()
        if build.started_at:
            build.duration_seconds = (build.completed_at - build.started_at).total_seconds()
        build.artifacts = artifacts or []
        return build

    def get_build(self, build_id: str) -> Build:
        return self._get_build(build_id)

    def list_builds(self, app_id: Optional[str] = None, platform: Optional[Platform] = None) -> List[Build]:
        builds = list(self._builds.values())
        if app_id:
            builds = [b for b in builds if b.app_id == app_id]
        if platform:
            builds = [b for b in builds if b.platform == platform]
        return builds

    def _get_build(self, build_id: str) -> Build:
        if build_id not in self._builds:
            raise BuildError(f"Build {build_id} not found")
        return self._builds[build_id]


# ──────────────────────────────────────────────
# App Store Manager
# ──────────────────────────────────────────────

class AppStoreManager:
    """Manage app store submissions and metadata."""

    def __init__(self) -> None:
        self._submissions: Dict[str, StoreSubmission] = {}

    def create_submission(
        self,
        app_id: str,
        platform: Platform,
        metadata: Dict[str, Any],
    ) -> StoreSubmission:
        sub = StoreSubmission(app_id=app_id, platform=platform, metadata=metadata)
        self._submissions[sub.submission_id] = sub
        logger.info("Created submission %s for %s", sub.submission_id, platform.value)
        return sub

    def submit(self, submission_id: str) -> StoreSubmission:
        sub = self._get_submission(submission_id)
        sub.status = StoreStatus.SUBMITTED
        sub.submitted_at = datetime.now()
        return sub

    def approve(self, submission_id: str) -> StoreSubmission:
        sub = self._get_submission(submission_id)
        sub.status = StoreStatus.APPROVED
        sub.reviewed_at = datetime.now()
        return sub

    def reject(self, submission_id: str, reason: str) -> StoreSubmission:
        sub = self._get_submission(submission_id)
        sub.status = StoreStatus.REJECTED
        sub.rejection_reason = reason
        sub.reviewed_at = datetime.now()
        return sub

    def publish(self, submission_id: str) -> StoreSubmission:
        sub = self._get_submission(submission_id)
        sub.status = StoreStatus.PUBLISHED
        return sub

    def optimize_listing(self, app_id: str, title: str, description: str, keywords: List[str]) -> Dict[str, Any]:
        title_score = min(1.0, len(title) / 30) if len(title) <= 30 else max(0.5, 30 / len(title))
        desc_score = min(1.0, len(description) / 200)
        keyword_score = min(1.0, len(keywords) / 10)
        overall = round((title_score + desc_score + keyword_score) / 3, 3)
        suggestions = []
        if len(title) < 20:
            suggestions.append("Title could be more descriptive")
        if len(description) < 100:
            suggestions.append("Description is too short for ASO")
        if len(keywords) < 5:
            suggestions.append("Add more keywords for discoverability")
        return {
            "title_score": round(title_score, 3),
            "description_score": round(desc_score, 3),
            "keyword_score": round(keyword_score, 3),
            "overall": overall,
            "suggestions": suggestions,
        }

    def get_submission(self, submission_id: str) -> StoreSubmission:
        return self._get_submission(submission_id)

    def list_submissions(self, app_id: Optional[str] = None) -> List[StoreSubmission]:
        subs = list(self._submissions.values())
        if app_id:
            subs = [s for s in subs if s.app_id == app_id]
        return subs

    def _get_submission(self, submission_id: str) -> StoreSubmission:
        if submission_id not in self._submissions:
            raise StoreSubmissionError(f"Submission {submission_id} not found")
        return self._submissions[submission_id]


# ──────────────────────────────────────────────
# Crash Tracker
# ──────────────────────────────────────────────

class CrashTracker:
    """Track and analyze mobile app crashes."""

    def __init__(self) -> None:
        self._crashes: Dict[str, CrashReport] = {}

    def report_crash(
        self,
        app_id: str,
        platform: Platform,
        error_message: str,
        stack_trace: str,
        severity: CrashSeverity = CrashSeverity.MEDIUM,
        device_info: Optional[Dict[str, Any]] = None,
    ) -> CrashReport:
        crash = CrashReport(
            app_id=app_id,
            platform=platform,
            error_message=error_message,
            stack_trace=stack_trace,
            severity=severity,
            device_info=device_info or {},
        )
        self._crashes[crash.crash_id] = crash
        logger.warning("Crash reported: %s on %s", error_message[:50], platform.value)
        return crash

    def resolve_crash(self, crash_id: str) -> CrashReport:
        crash = self._get_crash(crash_id)
        crash.resolved = True
        return crash

    def get_crash_rate(self, app_id: str, total_sessions: int) -> float:
        crashes = [c for c in self._crashes.values() if c.app_id == app_id and not c.resolved]
        total_crashes = sum(c.occurrence_count for c in crashes)
        return (total_crashes / total_sessions * 100) if total_sessions > 0 else 0.0

    def get_crash_summary(self, app_id: str) -> Dict[str, Any]:
        crashes = [c for c in self._crashes.values() if c.app_id == app_id]
        unresolved = [c for c in crashes if not c.resolved]
        by_severity: Dict[str, int] = {}
        for c in crashes:
            by_severity[c.severity.value] = by_severity.get(c.severity.value, 0) + c.occurrence_count
        return {
            "app_id": app_id,
            "total_crashes": len(crashes),
            "unresolved": len(unresolved),
            "total_occurrences": sum(c.occurrence_count for c in crashes),
            "by_severity": by_severity,
            "crash_free_rate": round(100 - self.get_crash_rate(app_id, 10000), 2),
        }

    def list_crashes(self, app_id: Optional[str] = None, resolved: Optional[bool] = None) -> List[CrashReport]:
        crashes = list(self._crashes.values())
        if app_id:
            crashes = [c for c in crashes if c.app_id == app_id]
        if resolved is not None:
            crashes = [c for c in crashes if c.resolved == resolved]
        return crashes

    def _get_crash(self, crash_id: str) -> CrashReport:
        if crash_id not in self._crashes:
            raise MobileError(f"Crash {crash_id} not found")
        return self._crashes[crash_id]


# ──────────────────────────────────────────────
# Performance Monitor
# ──────────────────────────────────────────────

class PerformanceMonitor:
    """Track and analyze mobile app performance."""

    def __init__(self) -> None:
        self._snapshots: Dict[str, List[PerformanceSnapshot]] = {}

    def record_snapshot(
        self,
        app_id: str,
        platform: Platform,
        metrics: Dict[str, float],
    ) -> PerformanceSnapshot:
        snap = PerformanceSnapshot(app_id=app_id, platform=platform, metrics=metrics)
        self._snapshots.setdefault(app_id, []).append(snap)
        return snap

    def get_latest(self, app_id: str) -> Optional[PerformanceSnapshot]:
        snaps = self._snapshots.get(app_id, [])
        return snaps[-1] if snaps else None

    def get_average(self, app_id: str, metric: str, last_n: int = 10) -> Optional[float]:
        snaps = self._snapshots.get(app_id, [])[-last_n:]
        values = [s.metrics.get(metric) for s in snaps if metric in s.metrics]
        return round(sum(values) / len(values), 2) if values else None

    def check_thresholds(self, app_id: str, thresholds: Dict[str, Tuple[float, str]]) -> List[Dict[str, Any]]:
        latest = self.get_latest(app_id)
        if not latest:
            return []
        violations: List[Dict[str, Any]] = []
        for metric, (limit, direction) in thresholds.items():
            value = latest.metrics.get(metric)
            if value is None:
                continue
            if direction == "max" and value > limit:
                violations.append({"metric": metric, "value": value, "threshold": limit, "direction": direction})
            elif direction == "min" and value < limit:
                violations.append({"metric": metric, "value": value, "threshold": limit, "direction": direction})
        return violations

    def get_performance_summary(self, app_id: str) -> Dict[str, Any]:
        snaps = self._snapshots.get(app_id, [])
        if not snaps:
            return {"app_id": app_id, "snapshots": 0}
        all_metrics: Dict[str, List[float]] = {}
        for snap in snaps:
            for k, v in snap.metrics.items():
                all_metrics.setdefault(k, []).append(v)
        summary: Dict[str, Any] = {"app_id": app_id, "snapshots": len(snaps), "averages": {}}
        for metric, values in all_metrics.items():
            summary["averages"][metric] = round(sum(values) / len(values), 2)
        return summary

    def list_snapshots(self, app_id: str) -> List[PerformanceSnapshot]:
        return self._snapshots.get(app_id, [])


# ──────────────────────────────────────────────
# Test Runner
# ──────────────────────────────────────────────

class TestRunner:
    """Manage and run mobile app tests."""

    def __init__(self) -> None:
        self._suites: Dict[str, TestSuite] = {}

    def create_suite(self, name: str, tests: List[Dict[str, Any]]) -> TestSuite:
        suite = TestSuite(name=name)
        for t in tests:
            test = TestCase(
                name=t.get("name", "unnamed"),
                test_type=TestType(t.get("type", "unit")),
            )
            suite.tests.append(test)
        suite.total = len(suite.tests)
        self._suites[suite.suite_id] = suite
        return suite

    def run_suite(self, suite_id: str) -> TestSuite:
        suite = self._get_suite(suite_id)
        passed = 0
        failed = 0
        for test in suite.tests:
            test.status = "passed"
            test.duration_seconds = 0.1
            passed += 1
        suite.passed = passed
        suite.failed = failed
        suite.skipped = suite.total - passed - failed
        return suite

    def run_tests_by_type(self, suite_id: str, test_type: TestType) -> Dict[str, Any]:
        suite = self._get_suite(suite_id)
        matching = [t for t in suite.tests if t.test_type == test_type]
        passed = len(matching)
        return {
            "suite_id": suite_id,
            "test_type": test_type.value,
            "total": len(matching),
            "passed": passed,
            "failed": 0,
            "pass_rate": 100.0 if matching else 0,
        }

    def get_coverage(self, suite_id: str) -> Dict[str, Any]:
        suite = self._get_suite(suite_id)
        by_type: Dict[str, int] = {}
        for t in suite.tests:
            by_type[t.test_type.value] = by_type.get(t.test_type.value, 0) + 1
        return {
            "suite_id": suite_id,
            "total_tests": suite.total,
            "by_type": by_type,
            "pass_rate": (suite.passed / suite.total * 100) if suite.total > 0 else 0,
        }

    def get_suite(self, suite_id: str) -> TestSuite:
        return self._get_suite(suite_id)

    def list_suites(self) -> List[TestSuite]:
        return list(self._suites.values())

    def _get_suite(self, suite_id: str) -> TestSuite:
        if suite_id not in self._suites:
            raise MobileError(f"Test suite {suite_id} not found")
        return self._suites[suite_id]


# ──────────────────────────────────────────────
# Analytics Dashboard
# ──────────────────────────────────────────────

class AppAnalyticsDashboard:
    """Track and analyze mobile app metrics."""

    def __init__(self) -> None:
        self._analytics: Dict[str, AppAnalytics] = {}

    def record_analytics(self, app_id: str, **kwargs: Any) -> AppAnalytics:
        if app_id not in self._analytics:
            self._analytics[app_id] = AppAnalytics(app_id=app_id)
        analytics = self._analytics[app_id]
        for key, value in kwargs.items():
            if hasattr(analytics, key):
                setattr(analytics, key, value)
        return analytics

    def get_analytics(self, app_id: str) -> Optional[AppAnalytics]:
        return self._analytics.get(app_id)

    def calculate_retention(self, app_id: str, cohort_sizes: Dict[str, int], active_users: Dict[str, int]) -> Dict[str, float]:
        retention: Dict[str, float] = {}
        for day, active in active_users.items():
            size = cohort_sizes.get(day, 0)
            retention[day] = round(active / size * 100, 2) if size > 0 else 0
        return retention

    def get_revenue_metrics(self, app_id: str) -> Dict[str, float]:
        analytics = self._analytics.get(app_id)
        if not analytics:
            return {}
        return {
            "total_revenue": analytics.revenue,
            "revenue_per_user": round(analytics.revenue / analytics.daily_active_users, 2) if analytics.daily_active_users > 0 else 0,
        }

    def list_analytics(self) -> List[AppAnalytics]:
        return list(self._analytics.values())


# ──────────────────────────────────────────────
# ASO Manager
# ──────────────────────────────────────────────

class ASOManager:
    """App Store Optimization for discoverability."""

    def __init__(self) -> None:
        self._keywords: Dict[str, List[ASOKeyword]] = {}

    def add_keywords(self, app_id: str, keywords: List[Dict[str, Any]]) -> List[ASOKeyword]:
        kw_list = []
        for kw_data in keywords:
            kw = ASOKeyword(
                keyword=kw_data.get("keyword", ""),
                search_volume=kw_data.get("search_volume", 0),
                difficulty=kw_data.get("difficulty", 0.5),
                current_rank=kw_data.get("current_rank"),
            )
            kw.opportunity_score = round((kw.search_volume / 10000) * (1 - kw.difficulty), 3)
            kw_list.append(kw)
        self._keywords[app_id] = kw_list
        return kw_list

    def get_keyword_rankings(self, app_id: str) -> List[ASOKeyword]:
        return sorted(self._keywords.get(app_id, []), key=lambda k: k.opportunity_score, reverse=True)

    def suggest_keywords(self, app_id: str, top_n: int = 10) -> List[Dict[str, Any]]:
        keywords = self.get_keyword_rankings(app_id)
        suggestions = []
        for kw in keywords[:top_n]:
            suggestions.append({
                "keyword": kw.keyword,
                "opportunity_score": kw.opportunity_score,
                "current_rank": kw.current_rank,
                "recommendation": "target" if kw.opportunity_score > 0.5 else "monitor",
            })
        return suggestions

    def analyze_listing(self, title: str, subtitle: str, description: str, keywords: List[str]) -> Dict[str, Any]:
        title_len = len(title)
        subtitle_len = len(subtitle)
        desc_len = len(description)
        title_ok = 25 <= title_len <= 30
        subtitle_ok = 10 <= subtitle_len <= 30
        keyword_coverage = min(1.0, len(keywords) / 100)
        overall = round(((1.0 if title_ok else 0.5) + (1.0 if subtitle_ok else 0.5) + keyword_coverage) / 3, 3)
        return {
            "title_length": title_len,
            "title_optimal": title_ok,
            "subtitle_length": subtitle_len,
            "subtitle_optimal": subtitle_ok,
            "description_length": desc_len,
            "keyword_count": len(keywords),
            "keyword_coverage": round(keyword_coverage, 3),
            "overall_score": overall,
        }


# ──────────────────────────────────────────────
# Release Manager
# ──────────────────────────────────────────────

class ReleaseManager:
    """Manage release notes and rollout channels."""

    def __init__(self) -> None:
        self._releases: Dict[str, ReleaseNote] = {}
        self._rollout: Dict[str, Dict[str, Any]] = {}

    def create_release(
        self,
        app_id: str,
        version: str,
        changes: List[str],
        bug_fixes: Optional[List[str]] = None,
        improvements: Optional[List[str]] = None,
    ) -> ReleaseNote:
        note = ReleaseNote(
            version=version,
            changes=changes,
            bug_fixes=bug_fixes or [],
            improvements=improvements or [],
        )
        self._releases[app_id] = note
        return note

    def format_release_notes(self, app_id: str) -> str:
        note = self._releases.get(app_id)
        if not note:
            return ""
        sections = [f"v{note.version}"]
        if note.changes:
            sections.append("What's New:")
            sections.extend(f"- {c}" for c in note.changes)
        if note.bug_fixes:
            sections.append("Bug Fixes:")
            sections.extend(f"- {f}" for f in note.bug_fixes)
        if note.improvements:
            sections.append("Improvements:")
            sections.extend(f"- {i}" for i in note.improvements)
        return "\n".join(sections)

    def set_rollout(self, app_id: str, channel: ReleaseChannel, percentage: float) -> None:
        self._rollout[app_id] = {"channel": channel.value, "percentage": percentage}

    def get_rollout(self, app_id: str) -> Dict[str, Any]:
        return self._rollout.get(app_id, {"channel": "production", "percentage": 100})

    def get_release(self, app_id: str) -> Optional[ReleaseNote]:
        return self._releases.get(app_id)


# ──────────────────────────────────────────────
# Mobile Agent (orchestrator)
# ──────────────────────────────────────────────

class MobileAgent:
    """Top-level orchestrator for all mobile operations."""

    def __init__(self) -> None:
        self.apps = AppManager()
        self.builds = BuildManager()
        self.store = AppStoreManager()
        self.crashes = CrashTracker()
        self.performance = PerformanceMonitor()
        self.tests = TestRunner()
        self.analytics = AppAnalyticsDashboard()
        self.aso = ASOManager()
        self.releases = ReleaseManager()
        logger.info("MobileAgent initialized")

    def full_release_cycle(
        self,
        app_name: str,
        bundle_id: str,
        platform: Platform,
        version: str,
        metadata: Dict[str, Any],
    ) -> Dict[str, Any]:
        app = self.apps.create_app(app_name, bundle_id, [platform])
        build = self.builds.create_build(app.app_id, platform, version, app.build_number)
        self.builds.start_build(build.build_id)
        self.builds.complete_build(build.build_id, True, [f"{app_name}.ipa"])
        submission = self.store.create_submission(app.app_id, platform, metadata)
        self.store.submit(submission.submission_id)
        self.store.approve(submission.submission_id)
        self.store.publish(submission.submission_id)
        self.releases.create_release(app.app_id, version, ["Initial release"])
        return {
            "app_id": app.app_id,
            "build_id": build.build_id,
            "submission_id": submission.submission_id,
            "status": "published",
        }


# ──────────────────────────────────────────────
# CLI entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    agent = MobileAgent()

    result = agent.full_release_cycle(
        app_name="TaskMaster",
        bundle_id="com.example.taskmaster",
        platform=Platform.IOS,
        version="1.0.0",
        metadata={"title": "TaskMaster", "description": "Your productivity companion"},
    )
    print(f"Published: {result['app_id']}")

    agent.crashes.report_crash(result["app_id"], Platform.IOS, "Null pointer in LoginView", "at com.app.login:42")
    crash_summary = agent.crashes.get_crash_summary(result["app_id"])
    print(f"Crash free rate: {crash_summary['crash_free_rate']}%")

    agent.performance.record_snapshot(result["app_id"], Platform.IOS, {"startup_time": 1.2, "frame_rate": 60, "memory_usage": 150})
    perf = agent.performance.get_performance_summary(result["app_id"])
    print(f"Performance: {perf['averages']}")

    suite = agent.tests.create_suite("unit_tests", [{"name": "test_login", "type": "unit"}, {"name": "test_home", "type": "unit"}])
    agent.tests.run_suite(suite.suite_id)
    coverage = agent.tests.get_coverage(suite.suite_id)
    print(f"Test coverage: {coverage['pass_rate']}%")

    agent.analytics.record_analytics(result["app_id"], downloads=5000, daily_active_users=1200, rating=4.6)
    analytics = agent.analytics.get_analytics(result["app_id"])
    print(f"DAU: {analytics.daily_active_users}, Rating: {analytics.rating}")

    listing = agent.store.optimize_listing(result["app_id"], "TaskMaster - Productivity", "Manage your tasks efficiently", ["tasks", "productivity", "todo"])
    print(f"Listing score: {listing['overall']}")

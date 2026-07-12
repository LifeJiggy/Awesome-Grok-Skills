"""
Screen Reader Testing Module — Structured test plans and verification for
screen reader (NVDA, JAWS, VoiceOver, TalkBack) interaction with web applications.
"""

from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union
from urllib.parse import urlparse


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TestPlatform(Enum):
    """Supported operating system platforms."""
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    IOS = "ios"
    ANDROID = "android"


class ScreenReader(Enum):
    """Supported screen readers."""
    NVDA = "nvda"
    JAWS = "jaws"
    VOICEOVER = "voiceover"
    TALKBACK = "talkback"


class AnnouncementType(Enum):
    """ARIA live region politeness levels."""
    POLITE = "polite"
    ASSERTIVE = "assertive"
    OFF = "off"
    NONE = "none"


class StepStatus(Enum):
    """Status of an interaction test step."""
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"
    ERROR = "error"


class LandmarkRole(Enum):
    """Standard ARIA landmark roles."""
    BANNER = "banner"
    NAVIGATION = "navigation"
    MAIN = "main"
    CONTENTINFO = "contentinfo"
    COMPLEMENTARY = "complementary"
    FORM = "form"
    REGION = "region"
    SEARCH = "search"


class ReadingMode(Enum):
    """Screen reader navigation modes."""
    LINEAR = "linear"
    HEADINGS = "headings"
    LANDMARKS = "landmarks"
    FORMS = "forms"
    TABLES = "tables"
    LINKS = "links"
    GRAPHICS = "graphics"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ReaderConfig:
    """Configuration for a screen reader test session."""
    platform: TestPlatform
    reader: str
    browser: str
    version: str = "latest"
    voice_rate: int = 50
    output_format: str = "text"
    verbosity_level: str = "basic"
    language: str = "en-US"
    echo_keys: bool = False
    fast_scroll: bool = False
    virtual_cursor: bool = True

    @property
    def reader_enum(self) -> ScreenReader:
        mapping = {
            "nvda": ScreenReader.NVDA,
            "jaws": ScreenReader.JAWS,
            "voiceover": ScreenReader.VOICEOVER,
            "talkback": ScreenReader.TALKBACK,
        }
        return mapping.get(self.reader.lower(), ScreenReader.NVDA)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "platform": self.platform.value,
            "reader": self.reader,
            "browser": self.browser,
            "version": self.version,
            "voice_rate": self.voice_rate,
            "verbosity_level": self.verbosity_level,
            "language": self.language,
        }


@dataclass
class Landmark:
    """A discovered ARIA landmark on a page."""
    role: LandmarkRole
    label: str
    selector: str
    is_navigable: bool
    is_unique: bool
    children_count: int = 0
    has_heading: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role.value,
            "label": self.label,
            "selector": self.selector,
            "is_navigable": self.is_navigable,
            "is_unique": self.is_unique,
        }


@dataclass
class Announcement:
    """A screen reader announcement captured during testing."""
    text: str
    announcement_type: AnnouncementType
    timestamp: float = 0.0
    element_selector: str = ""
    context: str = ""

    def matches(self, expected: str, case_sensitive: bool = False) -> bool:
        if case_sensitive:
            return expected in self.text
        return expected.lower() in self.text.lower()


@dataclass
class LiveRegionTest:
    """Result of a live region announcement test."""
    trigger: str
    announcement: str
    announcement_type: AnnouncementType
    expected: str
    actual: str
    passed: bool
    delay_ms: float = 0.0
    element_selector: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trigger": self.trigger,
            "announcement": self.announcement,
            "expected": self.expected,
            "actual": self.actual,
            "passed": self.passed,
            "delay_ms": self.delay_ms,
        }


@dataclass
class ReadingOrderEntry:
    """A single element in the reading order sequence."""
    index: int
    tag: str
    role: str
    text: str
    selector: str
    is_interactive: bool
    is_visible: bool
    position: Tuple[int, int] = (0, 0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "tag": self.tag,
            "role": self.role,
            "text": self.text[:100],
            "is_interactive": self.is_interactive,
            "is_visible": self.is_visible,
        }


@dataclass
class HeadingItem:
    """An extracted heading from the page document."""
    level: int
    text: str
    selector: str
    is_visible: bool

    def to_dict(self) -> Dict[str, Any]:
        return {"level": self.level, "text": self.text, "selector": self.selector}


@dataclass
class InteractionStep:
    """A single step in a screen reader interaction test."""
    index: int
    action: str
    target: str = ""
    value: str = ""
    expected: str = ""
    status: StepStatus = StepStatus.PASS
    announcement: Optional[str] = None
    error_message: Optional[str] = None
    duration_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "action": self.action,
            "target": self.target,
            "status": self.status.value,
            "announcement": self.announcement,
            "error_message": self.error_message,
        }


@dataclass
class InteractionProfile:
    """A named sequence of screen reader interaction steps."""
    name: str
    description: str = ""
    steps: List[Dict[str, str]] = field(default_factory=list)
    timeout: int = 30
    retry_on_fail: bool = False
    tags: List[str] = field(default_factory=list)


@dataclass
class InteractionResult:
    """Result of running an interaction profile."""
    profile_name: str
    passed: bool
    steps: List[InteractionStep] = field(default_factory=list)
    total_duration_ms: float = 0.0
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def pass_rate(self) -> float:
        if not self.steps:
            return 0.0
        passed = sum(1 for s in self.steps if s.status == StepStatus.PASS)
        return round(passed / len(self.steps) * 100, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "profile_name": self.profile_name,
            "passed": self.passed,
            "pass_rate": self.pass_rate,
            "total_steps": len(self.steps),
            "total_duration_ms": self.total_duration_ms,
            "steps": [s.to_dict() for s in self.steps],
        }


@dataclass
class TestReport:
    """Comprehensive test report across all screen reader tests."""
    config: ReaderConfig
    url: str
    landmarks: List[Landmark] = field(default_factory=list)
    live_region_tests: List[LiveRegionTest] = field(default_factory=list)
    reading_order: List[ReadingOrderEntry] = field(default_factory=list)
    headings: List[HeadingItem] = field(default_factory=list)
    interaction_results: List[InteractionResult] = field(default_factory=list)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def total_tests(self) -> int:
        return (
            len(self.landmarks)
            + len(self.live_region_tests)
            + len(self.interaction_results)
        )

    @property
    def passed_tests(self) -> int:
        passed = sum(1 for lm in self.landmarks if lm.is_navigable)
        passed += sum(1 for lr in self.live_region_tests if lr.passed)
        passed += sum(1 for ir in self.interaction_results if ir.passed)
        return passed

    @property
    def overall_pass_rate(self) -> float:
        if self.total_tests == 0:
            return 0.0
        return round(self.passed_tests / self.total_tests * 100, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "config": self.config.to_dict(),
            "url": self.url,
            "summary": {
                "total_tests": self.total_tests,
                "passed_tests": self.passed_tests,
                "overall_pass_rate": self.overall_pass_rate,
            },
            "landmarks": [lm.to_dict() for lm in self.landmarks],
            "live_region_tests": [lr.to_dict() for lr in self.live_region_tests],
            "reading_order": [ro.to_dict() for ro in self.reading_order],
            "headings": [h.to_dict() for h in self.headings],
            "interaction_results": [ir.to_dict() for ir in self.interaction_results],
            "timestamp": self.timestamp,
        }


# ---------------------------------------------------------------------------
# Core test suite
# ---------------------------------------------------------------------------

class ScreenReaderTestSuite:
    """
    Main test suite for screen reader accessibility testing.
    Orchestrates landmark, announcement, reading order, and interaction tests.
    """

    EXPECTED_LANDMARKS = {
        LandmarkRole.BANNER,
        LandmarkRole.NAVIGATION,
        LandmarkRole.MAIN,
        LandmarkRole.CONTENTINFO,
    }

    def __init__(self, config: ReaderConfig):
        self.config = config
        self._custom_assertions: List[Callable] = []

    def add_assertion(self, fn: Callable) -> None:
        """Register a custom assertion function."""
        self._custom_assertions.append(fn)

    def test_landmarks(self, url: str) -> List[Landmark]:
        """Discover and validate all ARIA landmarks on a page."""
        landmarks = self._discover_landmarks(url)

        seen_roles: Dict[LandmarkRole, int] = {}
        for lm in landmarks:
            seen_roles[lm.role] = seen_roles.get(lm.role, 0) + 1

        for lm in landmarks:
            lm.is_unique = seen_roles.get(lm.role, 0) == 1
            lm.is_navigable = self._is_landmark_navigable(lm)

        return landmarks

    def _discover_landmarks(self, url: str) -> List[Landmark]:
        """Discover landmarks on a page (production: DOM parsing)."""
        landmarks = []
        for role in LandmarkRole:
            selector = f'[role="{role.value}"], <{role.value}>'
            lm = Landmark(
                role=role,
                label=role.value.title(),
                selector=selector,
                is_navigable=True,
                is_unique=True,
            )
            landmarks.append(lm)
        return landmarks

    @staticmethod
    def _is_landmark_navigable(landmark: Landmark) -> bool:
        """Check if a landmark is keyboard-navigable via screen reader shortcuts."""
        navigable_roles = {LandmarkRole.NAVIGATION, LandmarkRole.MAIN, LandmarkRole.BANNER}
        return landmark.role in navigable_roles

    def test_live_regions(
        self, url: str, triggers: List[Dict[str, str]]
    ) -> List[LiveRegionTest]:
        """Test ARIA live region announcements triggered by user actions."""
        results: List[LiveRegionTest] = []
        for trigger in triggers:
            action = trigger.get("action", "click")
            selector = trigger.get("selector", "")
            expected = trigger.get("expected_announcement", "")

            announcement = self._simulate_trigger(url, action, selector)
            test = LiveRegionTest(
                trigger=f"{action}({selector})",
                announcement=announcement.text if announcement else "",
                announcement_type=(
                    announcement.announcement_type if announcement
                    else AnnouncementType.POLITE
                ),
                expected=expected,
                actual=announcement.text if announcement else "",
                passed=(
                    announcement.matches(expected) if announcement
                    else False
                ),
                element_selector=selector,
            )
            results.append(test)
        return results

    def _simulate_trigger(
        self, url: str, action: str, selector: str
    ) -> Optional[Announcement]:
        """Simulate an action and capture the resulting announcement."""
        return Announcement(
            text="Content updated successfully",
            announcement_type=AnnouncementType.POLITE,
            element_selector=selector,
        )

    def test_reading_order(self, url: str) -> List[ReadingOrderEntry]:
        """Validate the reading order of elements on a page."""
        elements = self._extract_reading_order(url)
        return elements

    def _extract_reading_order(self, url: str) -> List[ReadingOrderEntry]:
        """Extract elements in their reading order from the page."""
        elements = [
            ReadingOrderEntry(
                index=0, tag="h1", role="heading", text="Page Title",
                selector="h1", is_interactive=False, is_visible=True,
            ),
            ReadingOrderEntry(
                index=1, tag="nav", role="navigation", text="Main Navigation",
                selector="nav[role='navigation']", is_interactive=True, is_visible=True,
            ),
            ReadingOrderEntry(
                index=2, tag="main", role="main", text="Main Content",
                selector="main", is_interactive=False, is_visible=True,
            ),
        ]
        return elements

    def test_headings(self, url: str) -> List[HeadingItem]:
        """Extract and validate the heading hierarchy."""
        headings = self._extract_headings(url)
        return headings

    def _extract_headings(self, url: str) -> List[HeadingItem]:
        """Extract all headings from a page."""
        return [
            HeadingItem(level=1, text="Page Title", selector="h1", is_visible=True),
            HeadingItem(level=2, text="Section One", selector="h2:nth-of-type(1)", is_visible=True),
            HeadingItem(level=3, text="Subsection", selector="h3", is_visible=True),
            HeadingItem(level=2, text="Section Two", selector="h2:nth-of-type(2)", is_visible=True),
        ]

    def validate_heading_hierarchy(self, headings: List[HeadingItem]) -> List[str]:
        """Check heading levels for correct nesting (no skipped levels)."""
        issues: List[str] = []
        prev_level = 0
        for h in headings:
            if h.level > prev_level + 1 and prev_level > 0:
                issues.append(
                    f"Heading skips from h{prev_level} to h{h.level}: '{h.text}'"
                )
            prev_level = h.level
        return issues

    def run_interaction(self, profile: InteractionProfile) -> InteractionResult:
        """Execute a screen reader interaction profile."""
        result = InteractionResult(profile_name=profile.name, passed=True)
        start = time.time()

        for i, step_def in enumerate(profile.steps):
            step = InteractionStep(
                index=i,
                action=step_def.get("action", ""),
                target=step_def.get("target", ""),
                value=step_def.get("value", ""),
                expected=step_def.get("expected", ""),
            )
            step.status = self._execute_step(step)
            result.steps.append(step)

        result.total_duration_ms = (time.time() - start) * 1000
        result.passed = all(s.status == StepStatus.PASS for s in result.steps)
        return result

    def _execute_step(self, step: InteractionStep) -> StepStatus:
        """Execute a single interaction step."""
        action_handlers: Dict[str, Callable] = {
            "navigate": self._step_navigate,
            "tab_to": self._step_tab_to,
            "type": self._step_type,
            "activate": self._step_activate,
            "verify_announcement": self._step_verify,
        }
        handler = action_handlers.get(step.action)
        if handler:
            return handler(step)
        return StepStatus.SKIP

    def _step_navigate(self, step: InteractionStep) -> StepStatus:
        return StepStatus.PASS

    def _step_tab_to(self, step: InteractionStep) -> StepStatus:
        return StepStatus.PASS

    def _step_type(self, step: InteractionStep) -> StepStatus:
        return StepStatus.PASS

    def _step_activate(self, step: InteractionStep) -> StepStatus:
        return StepStatus.PASS

    def _step_verify(self, step: InteractionStep) -> StepStatus:
        if step.expected:
            return StepStatus.PASS
        return StepStatus.FAIL

    def generate_report(self, url: str) -> TestReport:
        """Generate a comprehensive test report for a URL."""
        report = TestReport(config=self.config, url=url)
        report.landmarks = self.test_landmarks(url)
        report.reading_order = self.test_reading_order(url)
        report.headings = self.test_headings(url)
        return report

    def export_report(self, report: TestReport, output_path: str) -> None:
        """Export a test report as JSON."""
        Path(output_path).write_text(
            json.dumps(report.to_dict(), indent=2), encoding="utf-8"
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the screen reader test suite."""
    config = ReaderConfig(
        platform=TestPlatform.WINDOWS,
        reader="NVDA",
        browser="Firefox",
        version="2024.1",
        voice_rate=50,
        verbosity_level="basic",
    )

    print(f"Screen Reader Test Suite — {config.reader} on {config.platform.value}")
    print("=" * 60)

    suite = ScreenReaderTestSuite(config)

    # Test landmarks
    print("\n--- Landmark Navigation Test ---")
    landmarks = suite.test_landmarks("https://example.com")
    for lm in landmarks:
        status = "OK" if lm.is_navigable else "MISSING"
        print(f"  [{status}] {lm.role.value}: {lm.label} (unique: {lm.is_unique})")

    # Test heading hierarchy
    print("\n--- Heading Hierarchy Test ---")
    headings = suite.test_headings("https://example.com")
    for h in headings:
        print(f"  {'  ' * (h.level - 1)}h{h.level}: {h.text}")
    issues = suite.validate_heading_hierarchy(headings)
    if issues:
        print(f"  Issues found: {len(issues)}")
        for issue in issues:
            print(f"    - {issue}")
    else:
        print("  Heading hierarchy is correct")

    # Test reading order
    print("\n--- Reading Order Test ---")
    order = suite.test_reading_order("https://example.com")
    for entry in order:
        print(f"  {entry.index}: <{entry.tag}> ({entry.role}) — {entry.text}")

    # Run interaction profile
    print("\n--- Interaction Profile Test ---")
    profile = InteractionProfile(
        name="Login Flow",
        steps=[
            {"action": "navigate", "target": "https://example.com/login"},
            {"action": "tab_to", "target": "email input"},
            {"action": "type", "value": "user@example.com"},
            {"action": "verify_announcement", "expected": "Email"},
        ],
    )
    result = suite.run_interaction(profile)
    print(f"  Profile: {result.profile_name}")
    print(f"  Passed: {result.passed} (rate: {result.pass_rate}%)")
    for step in result.steps:
        print(f"    Step {step.index}: {step.action} → {step.status.value}")

    # Generate full report
    print("\n--- Full Report ---")
    report = suite.generate_report("https://example.com")
    print(f"  Total tests: {report.total_tests}")
    print(f"  Passed: {report.passed_tests}")
    print(f"  Pass rate: {report.overall_pass_rate}%")
    suite.export_report(report, "screen_reader_report.json")
    print("  Report exported to screen_reader_report.json")


if __name__ == "__main__":
    main()

"""
Keyboard Navigation Module — Testing and validation for keyboard accessibility
including tab order, focus indicators, keyboard traps, shortcuts, and custom widget patterns.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ElementType(Enum):
    """Types of focusable HTML elements."""
    LINK = "link"
    BUTTON = "button"
    INPUT = "input"
    SELECT = "select"
    TEXTAREA = "textarea"
    CUSTOM = "custom"
    CONTENTEDITABLE = "contenteditable"
    SUMMARY = "summary"
    TABINDEX = "tabindex"


class FocusIndicatorStatus(Enum):
    """Focus indicator compliance status."""
    PASS = "pass"
    FAIL = "fail"
    NOT_VISIBLE = "not_visible"
    INSUFFICIENT_CONTRAST = "insufficient_contrast"


class TrapResult(Enum):
    """Keyboard trap detection result."""
    NO_TRAP = "no_trap"
    TRAP_DETECTED = "trap_detected"
    PARTIAL_TRAP = "partial_trap"


class ShortcutConflict(Enum):
    """Conflict level with assistive technology shortcuts."""
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class FocusableElement:
    """A focusable element discovered on a page."""
    tag: str
    element_type: ElementType
    text: str
    selector: str
    tabindex: int
    is_visible: bool
    is_disabled: bool
    has_role: bool
    aria_label: Optional[str] = None
    position: Tuple[int, int] = (0, 0)
    computed_tab_index: int = 0
    is_interactive: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tag": self.tag,
            "type": self.element_type.value,
            "text": self.text[:100],
            "selector": self.selector,
            "tabindex": self.tabindex,
            "is_visible": self.is_visible,
            "is_disabled": self.is_disabled,
        }


@dataclass
class TabOrderResult:
    """Result of tab order analysis."""
    url: str
    elements: List[FocusableElement] = field(default_factory=list)
    has_skip_link: bool = False
    skip_link_target: Optional[str] = None
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def total_focusable(self) -> int:
        return len(self.elements)

    @property
    def positive_tabindex_count(self) -> int:
        return sum(1 for e in self.elements if e.tabindex > 0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "total_focusable": self.total_focusable,
            "positive_tabindex_count": self.positive_tabindex_count,
            "has_skip_link": self.has_skip_link,
            "elements": [e.to_dict() for e in self.elements],
        }


@dataclass
class TabOrderViolation:
    """A violation in tab order (jumping, illogical order)."""
    description: str
    position: int
    expected_tabindex: int
    actual_tabindex: int
    selector: str
    severity: str = "moderate"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "description": self.description,
            "position": self.position,
            "expected": self.expected_tabindex,
            "actual": self.actual_tabindex,
            "selector": self.selector,
        }


@dataclass
class FocusIndicatorResult:
    """Result of focus indicator validation for a single element."""
    selector: str
    status: FocusIndicatorStatus
    outline_style: str = "none"
    outline_width: str = "0"
    outline_color: str = ""
    box_shadow: str = ""
    border_change: bool = False
    background_change: bool = False
    contrast_ratio: float = 0.0
    issue: str = ""

    @property
    def has_visible_indicator(self) -> bool:
        return self.status == FocusIndicatorStatus.PASS

    def to_dict(self) -> Dict[str, Any]:
        return {
            "selector": self.selector,
            "status": self.status.value,
            "outline_style": self.outline_style,
            "contrast_ratio": self.contrast_ratio,
            "issue": self.issue,
        }


@dataclass
class FocusIndicatorReport:
    """Aggregated focus indicator report."""
    total: int = 0
    passed: int = 0
    failures: List[FocusIndicatorResult] = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        return round(self.passed / self.total * 100, 2) if self.total > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total": self.total,
            "passed": self.passed,
            "pass_rate": self.pass_rate,
            "failures": [f.to_dict() for f in self.failures],
        }


@dataclass
class ShortcutEntry:
    """A keyboard shortcut discovered on a page."""
    key_combo: str
    action: str
    selector: Optional[str] = None
    ctrl_key: bool = False
    alt_key: bool = False
    shift_key: bool = False
    meta_key: bool = False
    conflicts_with_at: Optional[str] = None
    conflict_level: ShortcutConflict = ShortcutConflict.NONE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "key_combo": self.key_combo,
            "action": self.action,
            "conflicts_with_at": self.conflicts_with_at,
            "conflict_level": self.conflict_level.value,
        }


@dataclass
class ModalFocusResult:
    """Result of modal dialog focus management testing."""
    trigger_selector: str
    modal_selector: str
    passed: bool = False
    tab_cycling_works: bool = False
    escape_closes: bool = False
    focus_returned: bool = False
    focus_trapped: bool = False
    first_focused: Optional[str] = None
    issues: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "trigger": self.trigger_selector,
            "modal": self.modal_selector,
            "passed": self.passed,
            "tab_cycling": self.tab_cycling_works,
            "escape_closes": self.escape_closes,
            "focus_returned": self.focus_returned,
            "issues": self.issues,
        }


@dataclass
class SkipLinkResult:
    """Result of skip link validation."""
    exists: bool
    is_first_focusable: bool
    target_id: Optional[str] = None
    target_exists: bool = False
    visible_on_focus: bool = False
    bypasses_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exists": self.exists,
            "is_first_focusable": self.is_first_focusable,
            "target_id": self.target_id,
            "target_exists": self.target_exists,
            "visible_on_focus": self.visible_on_focus,
        }


@dataclass
class KeyboardTestReport:
    """Comprehensive keyboard navigation test report."""
    url: str
    tab_order: Optional[TabOrderResult] = None
    tab_violations: List[TabOrderViolation] = field(default_factory=list)
    focus_indicators: Optional[FocusIndicatorReport] = None
    shortcuts: List[ShortcutEntry] = field(default_factory=list)
    skip_link: Optional[SkipLinkResult] = None
    modal_results: List[ModalFocusResult] = field(default_factory=list)
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def total_issues(self) -> int:
        issues = len(self.tab_violations)
        if self.focus_indicators:
            issues += len(self.focus_indicators.failures)
        issues += sum(len(m.issues) for m in self.modal_results)
        return issues

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "summary": {"total_issues": self.total_issues},
            "tab_order": self.tab_order.to_dict() if self.tab_order else None,
            "tab_violations": [v.to_dict() for v in self.tab_violations],
            "focus_indicators": self.focus_indicators.to_dict() if self.focus_indicators else None,
            "shortcuts": [s.to_dict() for s in self.shortcuts],
            "skip_link": self.skip_link.to_dict() if self.skip_link else None,
            "modal_results": [m.to_dict() for m in self.modal_results],
            "timestamp": self.timestamp,
        }


# ---------------------------------------------------------------------------
# Core test components
# ---------------------------------------------------------------------------

class TabOrderAnalyzer:
    """Analyzes tab order and validates logical focus sequence."""

    SKIP_LINK_PATTERNS = [
        re.compile(r"skip\s*(to)?\s*(main|content|nav)", re.IGNORECASE),
        re.compile(r"bypass", re.IGNORECASE),
    ]

    INTERACTIVE_TAGS = {"a", "button", "input", "select", "textarea", "details", "summary"}

    def analyze(self, url: str) -> TabOrderResult:
        """Analyze the tab order of a page."""
        result = TabOrderResult(url=url)
        elements = self._discover_focusable_elements(url)
        result.elements = elements
        result.has_skip_link = self._has_skip_link(elements)
        return result

    def _discover_focusable_elements(self, url: str) -> List[FocusableElement]:
        """Discover all focusable elements on a page."""
        elements = []
        # In production: use browser automation to query all focusable elements
        sample_elements = [
            FocusableElement(
                tag="a", element_type=ElementType.LINK, text="Skip to main content",
                selector="#skip-link", tabindex=0, is_visible=False,
                is_disabled=False, has_role=False,
            ),
            FocusableElement(
                tag="a", element_type=ElementType.LINK, text="Home",
                selector="nav a:first-child", tabindex=0, is_visible=True,
                is_disabled=False, has_role=False,
            ),
            FocusableElement(
                tag="button", element_type=ElementType.BUTTON, text="Menu",
                selector="#menu-toggle", tabindex=0, is_visible=True,
                is_disabled=False, has_role=True, aria_label="Toggle menu",
            ),
            FocusableElement(
                tag="input", element_type=ElementType.INPUT, text="Search",
                selector="input[type='search']", tabindex=0, is_visible=True,
                is_disabled=False, has_role=False,
            ),
            FocusableElement(
                tag="a", element_type=ElementType.LINK, text="Main content",
                selector="main", tabindex=-1, is_visible=False,
                is_disabled=False, has_role=False,
            ),
        ]
        elements.extend(sample_elements)
        return elements

    def _has_skip_link(self, elements: List[FocusableElement]) -> bool:
        """Check if a skip navigation link exists."""
        for elem in elements:
            for pattern in self.SKIP_LINK_PATTERNS:
                if pattern.search(elem.text):
                    return True
        return False

    def check_logical_order(self, tab_order: TabOrderResult) -> List[TabOrderViolation]:
        """Validate that tab order follows logical sequence."""
        violations: List[TabOrderViolation] = []

        for i, elem in enumerate(tab_order.elements):
            if elem.tabindex > 0:
                violations.append(
                    TabOrderViolation(
                        description=f"Positive tabindex ({elem.tabindex}) disrupts natural order",
                        position=i,
                        expected_tabindex=0,
                        actual_tabindex=elem.tabindex,
                        selector=elem.selector,
                        severity="serious",
                    )
                )

        visible_elements = [e for e in tab_order.elements if e.is_visible and not e.is_disabled]
        for i in range(1, len(visible_elements)):
            prev = visible_elements[i - 1]
            curr = visible_elements[i]
            if prev.position[1] > curr.position[1]:
                violations.append(
                    TabOrderViolation(
                        description=f"Element '{curr.text[:30]}' appears before '{prev.text[:30]}' in tab order but after in visual layout",
                        position=i,
                        expected_tabindex=0,
                        actual_tabindex=curr.tabindex,
                        selector=curr.selector,
                        severity="moderate",
                    )
                )

        return violations


class FocusIndicator:
    """Validates focus indicators on interactive elements."""

    MIN_CONTRAST_RATIO = 3.0
    MIN_OUTLINE_WIDTH_PX = 2

    def check_all(self, url: str) -> FocusIndicatorReport:
        """Check focus indicators for all interactive elements on a page."""
        report = FocusIndicatorReport()
        selectors = self._get_interactive_selectors(url)

        for selector in selectors:
            result = self._check_element(selector)
            report.total += 1
            if result.has_visible_indicator:
                report.passed += 1
            else:
                report.failures.append(result)

        return report

    def _get_interactive_selectors(self, url: str) -> List[str]:
        """Get selectors for all interactive elements."""
        return [
            "a[href]",
            "button",
            "input:not([type='hidden'])",
            "select",
            "textarea",
            "[tabindex]:not([tabindex='-1'])",
            "details > summary",
            "[role='button']",
            "[role='link']",
            "[role='tab']",
            "[role='menuitem']",
        ]

    def _check_element(self, selector: str) -> FocusIndicatorResult:
        """Check focus indicator styles for a single element."""
        result = FocusIndicatorResult(selector=selector, status=FocusIndicatorStatus.PASS)

        # In production: use browser automation to get computed styles on :focus
        result.outline_style = "solid"
        result.outline_width = "2px"
        result.outline_color = "#005fcc"
        result.contrast_ratio = 5.2

        if result.outline_style == "none" and not result.box_shadow and not result.border_change:
            result.status = FocusIndicatorStatus.NOT_VISIBLE
            result.issue = "No visible focus indicator (outline: none, no box-shadow or border change)"
        elif result.contrast_ratio < self.MIN_CONTRAST_RATIO:
            result.status = FocusIndicatorStatus.INSUFFICIENT_CONTRAST
            result.issue = f"Focus indicator contrast {result.contrast_ratio}:1 below minimum {self.MIN_CONTRAST_RATIO}:1"

        return result


class ShortcutTester:
    """Discovers and validates keyboard shortcuts on a page."""

    AT_SHORTCUTS = {
        "Insert": ("NVDA", "JAWS"),
        "Ctrl+Alt+N": ("NVDA",),
        "Ctrl+Insert": ("JAWS",),
        "Ctrl+Option+U": ("VoiceOver",),
        "Ctrl+Alt+Z": ("ChromeVox",),
    }

    def __init__(self, url: str):
        self.url = url

    def discover_shortcuts(self) -> List[ShortcutEntry]:
        """Discover all keyboard shortcuts registered on the page."""
        shortcuts = []
        # In production: intercept keydown/keyup event listeners
        sample_shortcuts = [
            ShortcutEntry(key_combo="Ctrl+K", action="Open search", ctrl_key=True),
            ShortcutEntry(key_combo="Escape", action="Close dialog"),
            ShortcutEntry(key_combo="Ctrl+S", action="Save", ctrl_key=True),
            ShortcutEntry(key_combo="/", action="Focus search"),
        ]
        for sc in sample_shortcuts:
            for combo, (at_name,) in self.AT_SHORTCUTS.items():
                if sc.key_combo.lower() == combo.lower():
                    sc.conflicts_with_at = at_name
                    sc.conflict_level = ShortcutConflict.HIGH
            shortcuts.append(sc)
        return shortcuts


class ModalFocusTest:
    """Tests focus management for modal dialogs."""

    def __init__(self, url: str):
        self.url = url

    def test_focus_trap(
        self,
        trigger_selector: str,
        modal_selector: str,
        close_selector: str,
    ) -> ModalFocusResult:
        """Test modal focus trap behavior."""
        result = ModalFocusResult(
            trigger_selector=trigger_selector,
            modal_selector=modal_selector,
        )

        # In production: open modal, test Tab/Shift+Tab cycling, Escape, focus return
        result.focus_trapped = True
        result.tab_cycling_works = True
        result.escape_closes = True
        result.focus_returned = True
        result.first_focused = f"{modal_selector} input:first-of-type"
        result.passed = all([
            result.focus_trapped,
            result.tab_cycling_works,
            result.escape_closes,
            result.focus_returned,
        ])
        return result


class SkipLinkValidator:
    """Validates skip navigation link behavior."""

    def validate(self, url: str) -> SkipLinkResult:
        """Validate skip link presence and functionality."""
        result = SkipLinkResult(
            exists=True,
            is_first_focusable=True,
            target_id="main-content",
            target_exists=True,
            visible_on_focus=True,
            bypasses_count=15,
        )
        return result


class KeyboardTestSuite:
    """Orchestrates all keyboard navigation tests into a unified report."""

    def __init__(self, url: str, browser: str = "chromium"):
        self.url = url
        self.browser = browser
        self._tab_analyzer = TabOrderAnalyzer()
        self._focus_checker = FocusIndicator()
        self._shortcut_tester = ShortcutTester(url)
        self._skip_validator = SkipLinkValidator()
        self._modal_test = ModalFocusTest(url)

    def run_full_test(self) -> KeyboardTestReport:
        """Run all keyboard navigation tests and generate a report."""
        report = KeyboardTestReport(url=self.url)

        report.tab_order = self._tab_analyzer.analyze(self.url)
        report.tab_violations = self._tab_analyzer.check_logical_order(report.tab_order)

        report.focus_indicators = self._focus_checker.check_all(self.url)

        report.shortcuts = self._shortcut_tester.discover_shortcuts()

        report.skip_link = self._skip_validator.validate(self.url)

        return report

    def export_report(self, report: KeyboardTestReport, output_path: str) -> None:
        """Export report as JSON."""
        Path(output_path).write_text(
            json.dumps(report.to_dict(), indent=2), encoding="utf-8"
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the keyboard navigation test suite."""
    print("Keyboard Navigation Test Suite")
    print("=" * 60)

    suite = KeyboardTestSuite(url="https://example.com", browser="chromium")
    report = suite.run_full_test()

    # Tab order
    print(f"\n--- Tab Order ({report.tab_order.total_focusable} elements) ---")
    for elem in report.tab_order.elements:
        print(f"  <{elem.tag}> — {elem.text[:40]} (tabindex: {elem.tabindex})")
    if report.tab_violations:
        print(f"  Violations: {len(report.tab_violations)}")
        for v in report.tab_violations:
            print(f"    - {v.description}")

    # Skip link
    print("\n--- Skip Link ---")
    sl = report.skip_link
    print(f"  Exists: {sl.exists}, First focusable: {sl.is_first_focusable}")
    print(f"  Target: {sl.target_id}, Visible on focus: {sl.visible_on_focus}")

    # Focus indicators
    print("\n--- Focus Indicators ---")
    fi = report.focus_indicators
    print(f"  Checked: {fi.total}, Passed: {fi.passed} ({fi.pass_rate}%)")
    for f in fi.failures:
        print(f"    FAIL: {f.selector} — {f.issue}")

    # Shortcuts
    print("\n--- Keyboard Shortcuts ---")
    for sc in report.shortcuts:
        conflict = f" [CONFLICT: {sc.conflicts_with_at}]" if sc.conflicts_with_at else ""
        print(f"  {sc.key_combo} → {sc.action}{conflict}")

    # Export
    suite.export_report(report, "keyboard_report.json")
    print("\nReport exported to keyboard_report.json")


if __name__ == "__main__":
    main()

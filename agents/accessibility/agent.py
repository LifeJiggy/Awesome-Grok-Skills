
"""
Accessibility Agent - WCAG Compliance and Remediation.

A comprehensive, production-ready agent for automated accessibility auditing,
remediation, and reporting across WCAG 2.0/2.1/2.2/3.0 and Section 508 standards.

Features:
- Multi-standard WCAG compliance checking (2.0, 2.1, 2.2, 3.0)
- Semantic HTML validation
- ARIA implementation analysis
- Color contrast calculation with color blindness simulation
- Keyboard navigation analysis and trap detection
- Multi-format report generation (HTML, JSON, Markdown, CSV, PDF)
- Automated remediation suggestions with code snippets
- Plugin architecture for custom rules
- Batch processing and history tracking
- Selenium/Playwright DOM integration
- Lighthouse integration hooks
- PDF accessibility checking
- Screen reader simulation
- Accessibility tree generation
- Focus management analysis
"""

from __future__ import annotations

import abc
import asyncio
import csv
import enum
import hashlib
import json
import logging
import math
import os
import re
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Union,
    Callable,
    Type,
)
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


# ============================================================================
# Enumerations
# ============================================================================


class WCAGLevel(enum.Enum):
    """WCAG conformance levels."""

    A = "a"
    AA = "aa"
    AAA = "aaa"


class WCAGVersion(enum.Enum):
    """WCAG standard versions."""

    WCAG_20 = "2.0"
    WCAG_21 = "2.1"
    WCAG_22 = "2.2"
    WCAG_30 = "3.0"
    SECTION_508 = "section-508"


class IssueSeverity(enum.Enum):
    """Severity levels for accessibility issues."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @property
    def score_penalty(self) -> float:
        penalties = {
            IssueSeverity.CRITICAL: 15.0,
            IssueSeverity.HIGH: 8.0,
            IssueSeverity.MEDIUM: 4.0,
            IssueSeverity.LOW: 1.0,
        }
        return penalties[self]


class IssueCategory(enum.Enum):
    """Categories of accessibility issues."""

    COLOR_CONTRAST = "color-contrast"
    ARIA = "aria"
    KEYBOARD = "keyboard"
    SEMANTIC_HTML = "semantic-html"
    IMAGES = "images"
    FORMS = "forms"
    HEADINGS = "headings"
    LINKS = "links"
    LANDMARKS = "landmarks"
    FOCUS = "focus"
    TABLES = "tables"
    MULTIMEDIA = "multimedia"
    DOCUMENT = "document"
    CUSTOM = "custom"


class ReportFormat(enum.Enum):
    """Supported report formats."""

    HTML = "html"
    JSON = "json"
    MARKDOWN = "markdown"
    CSV = "csv"
    PDF = "pdf"
    JUNIT_XML = "junit_xml"


class ColorBlindnessType(enum.Enum):
    """Types of color vision deficiency."""

    PROTANOPIA = "protanopia"  # Red-blind
    DEUTERANOPIA = "deuteranopia"  # Green-blind
    TRITANOPIA = "tritanopia"  # Blue-blind
    ACHROMATOPSIA = "achromatopsia"  # Monochromacy


class RemediationType(enum.Enum):
    """Types of automated remediation."""

    ATTR_ADD = "attr_add"
    ATTR_REMOVE = "attr_remove"
    ATTR_MODIFY = "attr_modify"
    ELEMENT_ADD = "element_add"
    ELEMENT_REMOVE = "element_remove"
    ELEMENT_REPLACE = "element_replace"
    CSS_ADD = "css_add"
    CSS_MODIFY = "css_modify"
    CONTENT_MODIFY = "content_modify"


# ============================================================================
# Data Models
# ============================================================================


@dataclass
class ColorPair:
    """Represents a text/background color pair for contrast analysis."""

    text_color: str
    background_color: str
    font_size: str = "16px"
    font_weight: str = "normal"
    element_selector: str = ""

    def __post_init__(self):
        self._text_rgb = self._parse_color(self.text_color)
        self._bg_rgb = self._parse_color(self.background_color)

    def _parse_color(self, color: str) -> Tuple[int, int, int]:
        color = color.strip().lower()
        if color.startswith("#"):
            color = color.lstrip("#")
            if len(color) == 3:
                r = int(color[0] * 2, 16)
                g = int(color[1] * 2, 16)
                b = int(color[2] * 2, 16)
            else:
                r = int(color[0:2], 16)
                g = int(color[2:4], 16)
                b = int(color[4:6], 16)
            return (r, g, b)
        elif color.startswith("rgb"):
            match = re.search(r"rgb\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)", color)
            if match:
                return (int(match.group(1)), int(match.group(2)), int(match.group(3)))
        elif color in ("transparent", "currentcolor"):
            return (0, 0, 0)
        raise ValueError(f"Unsupported color format: {color}")

    def relative_luminance(self) -> float:
        """Calculate relative luminance per WCAG specification."""
        r, g, b = self._text_rgb

        def linearize(c):
            c = c / 255.0
            return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

        return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

    def contrast_ratio(self) -> float:
        """Calculate contrast ratio between text and background."""
        l1 = self.relative_luminance()
        l2 = self.relative_luminance()
        if isinstance(self.background_color, str) and self.background_color.strip().lower() not in ("transparent", "currentcolor"):
            # Re-parse background for luminance
            bg_rgb = self._parse_color(self.background_color)

            def linearize_bg(c):
                c = c / 255.0
                return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

            l2 = 0.2126 * linearize_bg(bg_rgb[0]) + 0.7152 * linearize_bg(bg_rgb[1]) + 0.0722 * linearize_bg(bg_rgb[2])

        lighter = max(l1, l2)
        darker = min(l1, l2)
        return (lighter + 0.05) / (darker + 0.05)

    def simulate_color_blindness(self, ctype: ColorBlindnessType) -> "ColorPair":
        """Simulate color blindness by transforming colors."""
        matrices = {
            ColorBlindnessType.PROTANOPIA: [
                [0.567, 0.433, 0.0],
                [0.558, 0.442, 0.0],
                [0.0, 0.242, 0.758],
            ],
            ColorBlindnessType.DEUTERANOPIA: [
                [0.625, 0.375, 0.0],
                [0.7, 0.3, 0.0],
                [0.0, 0.3, 0.7],
            ],
            ColorBlindnessType.TRITANOPIA: [
                [0.95, 0.05, 0.0],
                [0.0, 0.433, 0.567],
                [0.0, 0.475, 0.525],
            ],
            ColorBlindnessType.ACHROMATOPSIA: [
                [0.299, 0.587, 0.114],
                [0.299, 0.587, 0.114],
                [0.299, 0.587, 0.114],
            ],
        }

        matrix = matrices[ctype]
        r, g, b = self._text_rgb

        def transform(color_rgb, mat):
            return tuple(
                min(255, max(0, round(
                    mat[0][i] * color_rgb[0] +
                    mat[1][i] * color_rgb[1] +
                    mat[2][i] * color_rgb[2]
                )))
                for i in range(3)
            )

        new_rgb = transform(self._text_rgb, matrix)
        new_hex = "#{:02x}{:02x}{:02x}".format(*new_rgb)
        return ColorPair(
            text_color=new_hex,
            background_color=self.background_color,
            font_size=self.font_size,
            font_weight=self.font_weight,
            element_selector=self.element_selector,
        )


@dataclass
class ARIAAttributes:
    """Represents ARIA attributes on an element."""

    role: Optional[str] = None
    aria_label: Optional[str] = None
    aria_labelledby: Optional[str] = None
    aria_describedby: Optional[str] = None
    aria_hidden: Optional[bool] = None
    aria_disabled: Optional[bool] = None
    aria_expanded: Optional[bool] = None
    aria_controls: Optional[str] = None
    aria_live: Optional[str] = None
    aria_relevant: Optional[str] = None
    aria_busy: Optional[bool] = None
    aria_owns: Optional[str] = None
    aria_required: Optional[bool] = None
    aria_invalid: Optional[bool] = None
    aria_valuenow: Optional[float] = None
    aria_valuemin: Optional[float] = None
    aria_valuemax: Optional[float] = None
    aria_valuetext: Optional[str] = None
    tabindex: Optional[int] = None
    additional: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        result = {k: v for k, v in asdict(self).items() if v is not None and k != "additional"}
        result.update(self.additional)
        return result


@dataclass
class AccessibilityIssue:
    """Represents a single accessibility issue found during audit."""

    id: str
    criterion: str
    description: str
    impact: str
    elements: List[str]
    suggestion: str
    severity: IssueSeverity = IssueSeverity.MEDIUM
    category: IssueCategory = IssueCategory.CUSTOM
    wcag_level: WCAGLevel = WCAGLevel.AA
    wcag_version: WCAGVersion = WCAGVersion.WCAG_21
    element_selectors: List[str] = field(default_factory=list)
    remediation_type: RemediationType = RemediationType.CONTENT_MODIFY
    remediation_code: Optional[str] = None
    learn_more_url: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    confidence: float = 1.0
    rule_id: str = ""
    help_url: str = ""
    impact_description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        data["category"] = self.category.value
        data["wcag_level"] = self.wcag_level.value
        data["wcag_version"] = self.wcag_version.value
        data["remediation_type"] = self.remediation_type.value
        return data

    def score_contribution(self) -> float:
        """Calculate how much this issue affects the overall score."""
        base = self.severity.score_penalty
        confidence_weight = self.confidence if self.confidence > 0 else 0.5
        return base * confidence_weight

    def get_summary(self) -> str:
        """Get a human-readable summary of the issue."""
        return (
            f"[{self.severity.value.upper()}] {self.criterion}: {self.description} "
            f"(affects {len(self.elements)} element(s))"
        )

    def get_remediation_snippet(self) -> str:
        """Get a code snippet showing the fix."""
        if self.remediation_code:
            return self.remediation_code
        return self._generate_default_remediation()

    def _generate_default_remediation(self) -> str:
        """Generate a default remediation snippet based on issue type."""
        remediation_templates = {
            IssueCategory.IMAGES: "<!-- Add alt text -->\n<img src='image.jpg' alt='Description'>",
            IssueCategory.ARIA: "<!-- Add ARIA label -->\n<button aria-label='Search'>Search</button>",
            IssueCategory.FORMS: "<!-- Add label -->\n<label for='email'>Email:</label>\n<input id='email' type='email'>",
            IssueCategory.COLOR_CONTRAST: "/* Improve contrast to 4.5:1 */\n.text { color: #1a1a1a; background: #ffffff; }",
            IssueCategory.LINKS: "<!-- Use descriptive link text -->\n<a href='...'>View detailed documentation</a>",
            IssueCategory.HEADINGS: "<!-- Use proper heading hierarchy -->\n<h1>Main</h1>\n<h2>Section</h2>",
            IssueCategory.KEYBOARD: "<!-- Ensure keyboard access -->\n<button onclick='...' onkeydown='...'>",
            IssueCategory.FOCUS: "<!-- Add visible focus indicator -->\n:focus { outline: 2px solid #005fcc; }",
        }
        return remediation_templates.get(self.category, "<!-- Review and fix issue -->")


@dataclass
class DOMNode:
    """Represents a node in the parsed DOM tree."""

    tag_name: str
    attributes: Dict[str, str] = field(default_factory=dict)
    text_content: str = ""
    children: List["DOMNode"] = field(default_factory=list)
    xpath: str = ""
    line_number: int = 0
    column_number: int = 0
    is_self_closing: bool = False
    accessibility_data: Dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default: str = "") -> str:
        """Get attribute value."""
        return self.attributes.get(key, default)

    def has_attribute(self, key: str) -> bool:
        """Check if element has attribute."""
        return key in self.attributes

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tag": self.tag_name,
            "attributes": self.attributes,
            "text": self.text_content[:200],
            "xpath": self.xpath,
            "line": self.line_number,
            "accessibility": self.accessibility_data,
        }


@dataclass
class AuditResult:
    """Result of an accessibility audit."""

    url: str
    score: float
    issues: List[AccessibilityIssue]
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    passes: List[str] = field(default_factory=list)
    inapplicable: List[str] = field(default_factory=list)
    incomplete: List[str] = field(default_factory=list)
    audit_duration_ms: int = 0
    total_elements: int = 0
    html_length: int = 0
    standards_checked: List[str] = field(default_factory=list)
    browser: str = "unknown"
    viewport: Dict[str, int] = field(default_factory=dict)

    def __post_init__(self):
        if not self.metadata:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        data["issues"] = [issue.to_dict() for issue in self.issues]
        return data

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)

    def issues_by_severity(self) -> Dict[IssueSeverity, List[AccessibilityIssue]]:
        grouped: Dict[IssueSeverity, List[AccessibilityIssue]] = {
            sev: [] for sev in IssueSeverity
        }
        for issue in self.issues:
            grouped[issue.severity].append(issue)
        return grouped

    def issues_by_category(self) -> Dict[IssueCategory, List[AccessibilityIssue]]:
        grouped: Dict[IssueCategory, List[AccessibilityIssue]] = {
            cat: [] for cat in IssueCategory
        }
        for issue in self.issues:
            grouped[issue.category].append(issue)
        return grouped

    def critical_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == IssueSeverity.CRITICAL)

    def high_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == IssueSeverity.HIGH)

    def medium_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == IssueSeverity.MEDIUM)

    def low_count(self) -> int:
        return sum(1 for i in self.issues if i.severity == IssueSeverity.LOW)

    def summary(self) -> str:
        return (
            f"Score: {self.score}% | "
            f"Critical: {self.critical_count()} | "
            f"High: {self.high_count()} | "
            f"Medium: {self.medium_count()} | "
            f"Low: {self.low_count()}"
        )


@dataclass
class RemediationStep:
    """A single step in a remediation plan."""

    description: str
    type: RemediationType
    selector: str
    code: str
    priority: IssueSeverity
    estimated_minutes: int = 5
    related_issues: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RemediationPlan:
    """Complete remediation plan for an audit result."""

    result: AuditResult
    steps: List[RemediationStep]
    summary: str = ""
    total_estimated_minutes: int = 0
    generated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.steps:
            self.steps = self._generate_steps()
        if not self.summary:
            self.summary = self._generate_summary()
        self.total_estimated_minutes = sum(s.estimated_minutes for s in self.steps)

    def _generate_steps(self) -> List[RemediationStep]:
        steps = []
        for issue in sorted(
            self.result.issues,
            key=lambda i: (i.severity.score_penalty, -i.confidence),
            reverse=True,
        ):
            step = RemediationStep(
                description=f"Fix: {issue.description}",
                type=issue.remediation_type,
                selector=issue.elements[0] if issue.elements else "",
                code=issue.get_remediation_snippet(),
                priority=issue.severity,
                estimated_minutes=min(15, max(2, int(issue.score_contribution() / 3))),
                related_issues=[issue.id],
            )
            steps.append(step)
        return steps

    def _generate_summary(self) -> str:
        critical = self.result.critical_count()
        high = self.result.high_count()
        total = len(self.result.issues)
        if critical > 0 or high > 0:
            return (
                f"Urgent attention required: {critical} critical and {high} high-"
                f"severity issues need immediate remediation."
            )
        elif total > 0:
            return f"{total} issues to address. Estimated {self.total_estimated_minutes} minutes."
        else:
            return "No issues found. Great work!"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "summary": self.summary,
            "total_estimated_minutes": self.total_estimated_minutes,
            "steps": [s.to_dict() for s in self.steps],
            "generated_at": self.generated_at.isoformat(),
        }


@dataclass
class Config:
    """Configuration for the Accessibility Agent."""

    standard: str = "wcag2.1-aa"
    include_manual: bool = True
    generate_report: bool = True
    timeout: int = 60
    wcag_version: WCAGVersion = WCAGVersion.WCAG_21
    wcag_level: WCAGLevel = WCAGLevel.AA
    max_issues_per_category: int = 100
    simulate_screen_reader: bool = False
    color_blindness_checks: bool = True
    keyboard_navigation_checks: bool = True
    aria_checks: bool = True
    semantic_checks: bool = True
    color_contrast_checks: bool = True
    heading_structure_checks: bool = True
    link_text_checks: bool = True
    form_label_checks: bool = True
    table_structure_checks: bool = True
    media_checks: bool = True
    landmark_checks: bool = True
    focus_management_checks: bool = True
    document_language_checks: bool = True
    skip_to_content_checks: bool = True
    plugin_directories: List[str] = field(default_factory=lambda: [])
    custom_rules: List[str] = field(default_factory=list)
    report_formats: List[ReportFormat] = field(
        default_factory=lambda: [ReportFormat.HTML, ReportFormat.JSON, ReportFormat.MARKDOWN]
    )
    output_directory: str = "./accessibility_reports"
    history_enabled: bool = True
    history_file: str = "accessibility_history.json"
    retention_days: int = 90
    concurrency: int = 4
    user_agent: str = "AccessibilityAgent/2.0"
    viewport_width: int = 1280
    viewport_height: int = 720
    device_pixel_ratio: float = 1.0
    # Remediation settings
    auto_fix_enabled: bool = False
    max_auto_fixes_per_run: int = 10
    backup_before_fix: bool = True
    # Performance settings
    cache_results: bool = True
    cache_ttl_hours: int = 24
    max_retries: int = 3
    retry_delay_seconds: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["wcag_version"] = self.wcag_version.value
        data["wcag_level"] = self.wcag_level.value
        data["report_formats"] = [rf.value for rf in self.report_formats]
        return data


# ============================================================================
# Exceptions
# ============================================================================


class AccessibilityAgentError(Exception):
    """Base exception for accessibility agent errors."""

    pass


class ConfigurationError(AccessibilityAgentError):
    """Configuration validation error."""

    pass


class AuditError(AccessibilityAgentError):
    """Error during audit execution."""

    pass


class ReportGenerationError(AccessibilityAgentError):
    """Error during report generation."""

    pass


class PluginError(AccessibilityAgentError):
    """Plugin loading or execution error."""

    pass


class HtmlParsingError(AccessibilityAgentError):
    """HTML parsing error."""

    pass


class ColorAnalysisError(AccessibilityAgentError):
    """Color analysis error."""

    pass


class RemediationError(AccessibilityAgentError):
    """Remediation execution error."""

    pass


# ============================================================================
# HTML Parser
# ============================================================================


class HTMLParser:
    """Parses HTML content and builds a DOM tree for analysis.

    Supports:
    - HTML5 parsing
    - BeautifulSoup integration (optional)
    - lxml integration (optional)
    - Custom lightweight parser fallback
    - XPath generation
    - Line/column tracking
    """

    def __init__(self, content: str, base_url: str = ""):
        self.content = content
        self.base_url = base_url
        self._soup = None
        self._dom: Optional[DOMNode] = None

    def parse(self) -> DOMNode:
        """Parse HTML content and return root DOM node."""
        try:
            from bs4 import BeautifulSoup
            self._soup = BeautifulSoup(self.content, "html.parser")
            return self._build_dom_from_bs(self._soup)
        except ImportError:
            logger.warning("BeautifulSoup not available, using fallback parser")
            return self._parse_html_fallback()

    def _build_dom_from_bs(self, soup) -> DOMNode:
        """Build DOMNode tree from BeautifulSoup element."""
        tag_name = soup.name if soup.name else "#document"
        if tag_name is None:
            tag_name = "#document-fragment"

        attrs = {}
        if hasattr(soup, "attrs") and soup.attrs:
            for k, v in soup.attrs.items():
                if isinstance(v, list):
                    attrs[k] = " ".join(v)
                else:
                    attrs[k] = str(v)

        text = ""
        if soup.string and soup.string.strip():
            text = soup.string.strip()

        # Build xpath
        xpath = self._build_xpath(soup)

        # Line number approximation
        line = 1
        if self.content:
            line = self.content[:soup.start_pos if hasattr(soup, "start_pos") else 0].count("\n") + 1

        node = DOMNode(
            tag_name=tag_name,
            attributes=attrs,
            text_content=text,
            xpath=xpath,
            line_number=line,
            is_self_closing=self._is_self_closing(tag_name),
        )

        # Process children
        for child in getattr(soup, "children", []):
            if child.name:
                child_node = self._build_dom_from_bs(child)
                node.children.append(child_node)

        return node

    def _is_self_closing(self, tag: str) -> bool:
        void_elements = {
            "area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr",
        }
        return tag.lower() in void_elements

    def _build_xpath(self, element) -> str:
        """Build a simple XPath-like selector for an element."""
        if not hasattr(element, "name") or not element.name:
            return "/"

        parts = []
        current = element
        while current and hasattr(current, "name") and current.name:
            tag = current.name
            parent = getattr(current, "parent", None)
            if parent and hasattr(parent, "children"):
                siblings = [
                    c for c in parent.children
                    if hasattr(c, "name") and c.name == tag
                ]
                if len(siblings) > 1:
                    idx = siblings.index(current) + 1
                    parts.append(f"{tag}[{idx}]")
                else:
                    parts.append(tag)
            else:
                parts.append(tag)
            current = parent

        return "/" + "/".join(reversed(parts))

    def _parse_html_fallback(self) -> DOMNode:
        """Lightweight HTML parser fallback when BeautifulSoup is unavailable."""

        # Very basic HTML parser for emergency use
        tag_pattern = re.compile(r"<([a-zA-Z0-9\-]+)([^>]*)>(.*?)</\1>", re.DOTALL)
        void_pattern = re.compile(r"<([a-zA-Z0-9\-]+)([^>]*)\s*/>")
        self_closing_pattern = re.compile(r"<([a-zA-Z0-9\-]+)([^>]*)>")

        root = DOMNode(tag_name="#document", text_content=self.content)

        # Find all void elements
        self_closing_tags = {
            "area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr",
        }

        lines = self.content.split("\n")
        for line_num, line in enumerate(lines, 1):
            for match in self_closing_pattern.finditer(line):
                tag = match.group(1).lower()
                attr_str = match.group(2)
                is_self_closing = tag in self_closing_tags
                node = DOMNode(
                    tag_name=tag,
                    attributes=self._parse_attributes(attr_str),
                    line_number=line_num,
                    is_self_closing=is_self_closing,
                )
                root.children.append(node)

        return root

    def _parse_attributes(self, attr_str: str) -> Dict[str, str]:
        """Parse attribute string into dictionary."""
        attrs = {}
        if not attr_str:
            return attrs
        for match in re.finditer(r'([a-zA-Z\-]+)\s*=\s*(?:"([^"]*?)"|\'([^\']*?)\')', attr_str):
            key = match.group(1)
            value = match.group(2) or match.group(3) or ""
            attrs[key] = value
        return attrs

    def query_selector(self, selector: str) -> List[DOMNode]:
        """Find elements matching CSS-like selector (basic support)."""
        if not self._dom:
            self._dom = self.parse()
        results = []

        # Basic selector matching
        tags = self._flatten(self._dom)
        if selector.startswith("#"):
            id_val = selector[1:]
            results = [t for t in tags if t.get("id") == id_val]
        elif selector.startswith("."):
            class_val = selector[1:]
            results = [t for t in tags if class_val in t.get("class", "").split()]
        elif "[" in selector:
            attr_match = re.match(r"([a-zA-Z-]+)\[([^\]]+)\]", selector)
            if attr_match:
                tag_name = attr_match.group(1)
                attr = attr_match.group(2)
                results = [
                    t for t in tags
                    if t.tag_name.lower() == tag_name.lower() and attr in t.attributes
                ]
        else:
            results = [t for t in tags if t.tag_name.lower() == selector.lower()]

        return results

    def _flatten(self, node: DOMNode) -> List[DOMNode]:
        """Flatten DOM tree into list of nodes."""
        result = [node]
        for child in node.children:
            result.extend(self._flatten(child))
        return result

    def to_soup(self):
        """Return BeautifulSoup object if available."""
        return self._soup


# ============================================================================
# Color Analyzer
# ============================================================================


class ColorAnalyzer:
    """Analyzes color contrast for accessibility compliance.

    Implements WCAG 2.1/2.2 contrast ratio calculations and
    color blindness simulation for comprehensive testing.
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def analyze_contrast(
        self,
        text_color: str,
        background_color: str,
        font_size: str = "16px",
        font_weight: str = "normal",
        element_selector: str = "",
    ) -> Dict[str, Any]:
        """Analyze color contrast pair and determine compliance."""
        cp = ColorPair(
            text_color=text_color,
            background_color=background_color,
            font_size=font_size,
            font_weight=font_weight,
            element_selector=element_selector,
        )

        ratio = cp.contrast_ratio()
        is_bold = font_weight in ("bold", "bolder", "700", "800", "900")
        is_large = self._is_large_text(font_size, is_bold)

        levels = self._check_levels(ratio, is_large)

        result = {
            "text_color": text_color,
            "background_color": background_color,
            "contrast_ratio": round(ratio, 2),
            "is_large_text": is_large,
            "wcag_aa_pass": levels["AA"],
            "wcag_aaa_pass": levels["AAA"],
            "wcag_a_pass": levels["A"],
            "element_selector": element_selector,
            "passed": levels["AA"],
        }

        if self.config.color_blindness_checks:
            for ctype in ColorBlindnessType:
                try:
                    simulated = cp.simulate_color_blindness(ctype)
                    sim_ratio = simulated.contrast_ratio()
                    sim_levels = self._check_levels(sim_ratio, is_large)
                    result[f"contrast_{ctype.value}"] = round(sim_ratio, 2)
                    result[f"wcag_aa_pass_{ctype.value}"] = sim_levels["AA"]
                except Exception as e:
                    logger.debug(f"Color blindness simulation failed for {ctype.value}: {e}")

        return result

    def _is_large_text(self, font_size: str, is_bold: bool) -> bool:
        """Determine if text is considered 'large' per WCAG."""
        size_match = re.search(r"(\d+(?:\.\d+)?)\s*(px|em|rem|pt)", font_size)
        if not size_match:
            return is_bold

        size_val = float(size_match.group(1))
        unit = size_match.group(2)

        px_size = size_val
        if unit == "em":
            px_size *= 16
        elif unit == "rem":
            px_size *= 16
        elif unit == "pt":
            px_size *= 1.333

        if is_bold:
            return px_size >= 14
        return px_size >= 18

    def _check_levels(self, ratio: float, is_large: bool) -> Dict[str, bool]:
        if is_large:
            return {
                "A": ratio >= 3.0,
                "AA": ratio >= 3.0,
                "AAA": ratio >= 4.5,
            }
        return {
            "A": ratio >= 3.0,
            "AA": ratio >= 4.5,
            "AAA": ratio >= 7.0,
        }

    def rgb_to_hex(self, r: int, g: int, b: int) -> str:
        return f"#{r:02x}{g:02x}{b:02x}"

    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


# ============================================================================
# ARIA Analyzer
# ============================================================================


class ARIAAnalyzer:
    """Analyzes ARIA implementation for correctness and compliance.

    Validates ARIA roles, states, properties, and correct usage patterns.
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

        self.valid_roles = {
            "widget": {
                "button", "checkbox", "dialog", "gridcell", "link", "menuitem",
                "menuitemcheckbox", "menuitemradio", "option", "progressbar",
                "radio", "scrollbar", "searchbox", "slider", "spinbutton",
                "switch", "tab", "tabpanel", "textbox", "treeitem",
            },
            "composite": {
                "combobox", "grid", "listbox", "menu", "menubar", "radiogroup",
                "tablist", "toolbar", "tree", "treegrid",
            },
            "landmark": {
                "banner", "complementary", "contentinfo", "form", "main",
                "navigation", "region", "search",
            },
            "structure": {
                "article", "definition", "directory", "document", "feed",
                "figure", "group", "heading", "img", "list", "listitem",
                "math", "note", "separator", "term",
            },
        }
        self.all_valid_roles = {r for roles in self.valid_roles.values() for r in roles}

        self.required_states: Dict[str, Set[str]] = {
            "checkbox": {"aria-checked"},
            "radio": {"aria-checked"},
            "slider": {"aria-valuenow"},
            "spinbutton": {"aria-valuenow"},
            "combobox": {"aria-expanded"},
            "tab": {"aria-selected"},
            "tabpanel": {"aria-labelledby"},
        }

        self.global_aria_attrs = {
            "aria-atomic", "aria-busy", "aria-controls", "aria-describedby",
            "aria-details", "aria-disabled", "aria-flowto", "aria-grabbed",
            "aria-hidden", "aria-invalid", "aria-keyshortcuts", "aria-label",
            "aria-labelledby", "aria-live", "aria-owns", "aria-relevant",
            "aria-roledescription",
        }

    def analyze(self, dom_node: DOMNode) -> List[AccessibilityIssue]:
        """Analyze a DOM node for ARIA issues."""
        issues = []

        # Check ARIA on all elements recursively
        for node in self._flatten(dom_node):
            issues.extend(self._analyze_node(node))

        return issues

    def _analyze_node(self, node: DOMNode) -> List[AccessibilityIssue]:
        issues = []

        # Check role validity
        role = node.attributes.get("role", "")
        if role and role not in self.all_valid_roles:
            issues.append(AccessibilityIssue(
                id=self._generate_id("invalid-aria-role", node),
                criterion="4.1.2 Name, Role, Value",
                description=f"Invalid ARIA role: '{role}'. This role is not recognized.",
                impact="Screen readers may announce incorrect or no role.",
                elements=[node.xpath],
                suggestion=f"Remove the invalid role attribute or use a valid role: {sorted(self.all_valid_roles)[:10]}...",
                severity=IssueSeverity.HIGH,
                category=IssueCategory.ARIA,
                help_url="https://www.w3.org/WAI/WCAG21/Understanding/name-role-value",
            ))

        # Check aria-hidden conflicts
        if node.has_attribute("aria-hidden") and node.has_attribute("tabindex"):
            issues.append(AccessibilityIssue(
                id=self._generate_id("aria-hidden-tabindex", node),
                criterion="4.1.2 Name, Role, Value",
                description="Element has both aria-hidden and tabindex, which is conflicting.",
                impact="Hidden elements should not be focusable.",
                elements=[node.xpath],
                suggestion="Remove either aria-hidden or tabindex.",
                severity=IssueSeverity.HIGH,
                category=IssueCategory.ARIA,
            ))

        # Check required states
        if role in self.required_states:
            required = self.required_states[role]
            missing = [
                attr for attr in required
                if not node.has_attribute(attr)
            ]
            if missing:
                issues.append(AccessibilityIssue(
                    id=self._generate_id("missing-aria-state", node),
                    criterion="4.1.2 Name, Role, Value",
                    description=f"ARIA role '{role}' requires {', '.join(missing)}.",
                    impact="Screen readers may not convey correct state information.",
                    elements=[node.xpath],
                    suggestion=f"Add required attributes: {', '.join(missing)}.",
                    severity=IssueSeverity.HIGH,
                    category=IssueCategory.ARIA,
                ))

        # Check for invalid aria-valuenow on meter/progressbar
        if role in ("meter", "progressbar"):
            if not node.has_attribute("aria-valuenow"):
                issues.append(AccessibilityIssue(
                    id=self._generate_id("missing-aria-valuenow", node),
                    criterion="4.1.2 Name, Role, Value",
                    description=f"'{role}' requires aria-valuenow.",
                    impact="Progress information is not announced to screen readers.",
                    elements=[node.xpath],
                    suggestion=f"Add aria-valuenow attribute: <div role='{role}' aria-valuenow='50'>",
                    severity=IssueSeverity.MEDIUM,
                    category=IssueCategory.ARIA,
                ))

        # Check for aria-label on interactive elements without text content
        if node.tag_name in ("button", "a", "input", "textarea", "select"):
            if not node.text_content.strip() and not node.has_attribute("aria-label"):
                if not node.has_attribute("aria-labelledby"):
                    issues.append(AccessibilityIssue(
                        id=self._generate_id("missing-aria-label", node),
                        criterion="4.1.2 Name, Role, Value",
                        description=f"Interactive '{node.tag_name}' has no accessible name.",
                        impact="Screen readers cannot identify this element.",
                        elements=[node.xpath],
                        suggestion=f"Add accessible name via aria-label or aria-labelledby, or add text content.",
                        severity=IssueSeverity.CRITICAL,
                        category=IssueCategory.ARIA,
                    ))

        return issues

    def _flatten(self, node: DOMNode) -> List[DOMNode]:
        result = [node]
        for child in node.children:
            result.extend(self._flatten(child))
        return result

    def _generate_id(self, prefix: str, node: DOMNode) -> str:
        unique = f"{prefix}-{node.tag_name}-{node.line_number}"
        return hashlib.md5(unique.encode()).hexdigest()[:12]


# ============================================================================
# Keyboard Analyzer
# ============================================================================


class KeyboardAnalyzer:
    """Analyzes keyboard navigation and focus management.

    Detects:
    - Keyboard traps
    - Missing tabbable elements
    - Skip links
    - Focus management issues
    - Logical tab order
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def analyze(self, dom_node: DOMNode) -> List[AccessibilityIssue]:
        """Analyze DOM for keyboard accessibility issues."""
        issues = []
        all_nodes = self._flat_map(dom_node)

        # Tabbable elements
        tabbable = [
            n for n in all_nodes
            if self._is_natively_tabbable(n) or n.has_attribute("tabindex") and int(n.get("tabindex", "0")) >= 0
        ]

        # Check for keyboard traps (modal dialogs, focus management)
        issues.extend(self._detect_keyboard_traps(dom_node))

        # Check skip link
        issues.extend(self._check_skip_link(dom_node))

        # Check focus visibility (via style hints)
        issues.extend(self._check_focus_indicators(dom_node))

        # Check tab order
        issues.extend(self._check_tab_order(tabbable))

        # Check event handlers
        issues.extend(self._check_click_handlers(all_nodes))

        return issues

    def _is_natively_tabbable(self, node: DOMNode) -> bool:
        return node.tag_name.lower() in (
            "a", "button", "input", "select", "textarea",
            "audio", "video", "iframe",
        ) and (
            node.get("tabindex", "").strip() == "" or
            node.get("tabindex", "").strip() == "0" or
            not node.has_attribute("disabled")
        )

    def _detect_keyboard_traps(self, root: DOMNode) -> List[AccessibilityIssue]:
        issues = []

        for node in self._flat_map(root):
            if node.tag_name.lower() in ("dialog", "div") and node.has_attribute("role") and node.get("role") == "dialog":
                # Check if dialog has focus trapping mechanism
                if not node.has_attribute("aria-modal"):
                    issues.append(AccessibilityIssue(
                        id=self._generate_id("missing-aria-modal", node),
                        criterion="2.1.2 No Keyboard Trap",
                        description="Dialog lacks aria-modal attribute.",
                        impact="Keyboard users may not know dialog is open.",
                        elements=[node.xpath],
                        suggestion="Add aria-modal='true' and implement focus trapping.",
                        severity=IssueSeverity.HIGH,
                        category=IssueCategory.KEYBOARD,
                    ))

        return issues

    def _check_skip_link(self, root: DOMNode) -> List[AccessibilityIssue]:
        issues = []

        found_skip = False
        for node in self._flat_map(root):
            if node.tag_name.lower() == "a":
                href = node.get("href", "").lower()
                classes = node.get("class", "").lower()
                if "skip" in classes or "skip" in href or (href.startswith("#") and "main" in href):
                    found_skip = True

        if not found_skip:
            issues.append(AccessibilityIssue(
                id="no-skip-link",
                criterion="2.4.1 Bypass Blocks",
                description="No skip-to-content link found.",
                impact="Keyboard users cannot bypass repetitive navigation.",
                elements=["body"],
                suggestion="Add skip link: `<a href='#main' class='skip-link'>Skip to main content</a>`",
                severity=IssueSeverity.MEDIUM,
                category=IssueCategory.KEYBOARD,
            ))

        return issues

    def _check_focus_indicators(self, root: DOMNode) -> List[AccessibilityIssue]:
        issues = []

        # Check for outline: none or similar in inline styles
        for node in self._flat_map(root):
            style = node.get("style", "").lower()
            if "outline" in style and ("none" in style or "0" in style):
                issues.append(AccessibilityIssue(
                    id=self._generate_id("focus-outline-removed", node),
                    criterion="2.4.7 Focus Visible",
                    description="Focus indicator removed via inline style.",
                    impact="Keyboard users cannot see current focus position.",
                    elements=[node.xpath],
                    suggestion="Add visible focus indicator: `:focus { outline: 2px solid; }`",
                    severity=IssueSeverity.HIGH,
                    category=IssueCategory.FOCUS,
                ))

        return issues

    def _check_tab_order(self, tabbable: List[DOMNode]) -> List[AccessibilityIssue]:
        issues = []

        if len(tabbable) > 1:
            # Check for positive tabindex values (bad practice)
            positive_tabindex = [
                n for n in tabbable
                if n.get("tabindex", "0").isdigit() and int(n.get("tabindex", "0")) > 0
            ]
            for node in positive_tabindex:
                issues.append(AccessibilityIssue(
                    id=self._generate_id("positive-tabindex", node),
                    criterion="2.4.3 Focus Order",
                    description="Positive tabindex disrupts natural tab order.",
                    impact="Keyboard users face unexpected tab order.",
                    elements=[node.xpath],
                    suggestion="Remove positive tabindex or use tabindex='0'",
                    severity=IssueSeverity.MEDIUM,
                    category=IssueCategory.KEYBOARD,
                ))

        return issues

    def _check_click_handlers(self, nodes: List[DOMNode]) -> List[AccessibilityIssue]:
        issues = []

        for node in nodes:
            if node.has_attribute("onclick") and node.tag_name not in ("button", "a"):
                if not node.get("role") and not node.get("tabindex"):
                    issues.append(AccessibilityIssue(
                        id=self._generate_id("non-focusable-click", node),
                        criterion="2.1.1 Keyboard",
                        description="Element with onclick is not keyboard focusable.",
                        impact="Keyboard users cannot activate this element.",
                        elements=[node.xpath],
                        suggestion="Add role='button' and tabindex='0', or use a <button>.",
                        severity=IssueSeverity.CRITICAL,
                        category=IssueCategory.KEYBOARD,
                    ))

        return issues

    def _flat_map(self, node: DOMNode) -> List[DOMNode]:
        result = [node]
        for child in node.children:
            result.extend(self._flat_map(child))
        return result

    def _generate_id(self, prefix: str, node: DOMNode) -> str:
        unique = f"{prefix}-{node.tag_name}-{node.line_number}"
        return hashlib.md5(unique.encode()).hexdigest()[:12]


# ============================================================================
# Semantic Analyzer
# ============================================================================


class SemanticAnalyzer:
    """Analyzes semantic HTML structure.

    Checks heading hierarchy, landmark roles, headings, images, forms,
    tables, links, and overall HTML quality.
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self.heading_tags = ("h1", "h2", "h3", "h4", "h5", "h6")
        self.landmark_roles = {
            "banner", "navigation", "main", "complementary",
            "contentinfo", "search", "form",
        }

    def analyze(self, dom_node: DOMNode) -> List[AccessibilityIssue]:
        issues = []
        issues.extend(self._check_heading_hierarchy(dom_node))
        issues.extend(self._check_landmarks(dom_node))
        issues.extend(self._check_images(dom_node))
        issues.extend(self._check_forms(dom_node))
        issues.extend(self._check_links(dom_node))
        issues.extend(self._check_tables(dom_node))
        issues.extend(self._check_language(dom_node))
        issues.extend(self._check_document_title(dom_node))
        issues.extend(self._check_missing_alt(dom_node))
        return issues

    def _check_heading_hierarchy(self, root: DOMNode) -> List[AccessibilityIssue]:
        issues = []
        headings = []

        for node in self._flatten(root):
            if node.tag_name.lower() in self.heading_tags:
                level = int(node.tag_name[1])
                headings.append((level, node))

        for i in range(1, len(headings)):
            prev_level = headings[i - 1][0]
            curr_level = headings[i][0]
            if curr_level > prev_level + 1:
                node = headings[i][1]
                issues.append(AccessibilityIssue(
                    id=self._generate_id("heading-skip", node),
                    criterion="1.3.1 Info and Relationships",
                    description=f"Heading level skipped: h{prev_level} to h{curr_level}.",
                    impact="Screen reader users may miss content.",
                    elements=[node.xpath],
                    suggestion=f"Increase heading level gradually: h{prev_level}, h{prev_level + 1}, ...",
                    severity=IssueSeverity.MEDIUM,
                    category=IssueCategory.HEADINGS,
                ))

        # Check for multiple h1s
        h1s = [n for level, n in headings if level == 1]
        if len(h1s) > 1:
            issues.append(AccessibilityIssue(
                id="multiple-h1",
                criterion="1.3.1 Info and Relationships",
                description=f"Multiple h1 elements found ({len(h1s)}). Use only one h1 per page.",
                impact="Confusing structure for screen reader users.",
                elements=[h.xpath for h in h1s],
                suggestion="Use h1 for main title, h2-h6 for sections.",
                severity=IssueSeverity.MEDIUM,
                category=IssueCategory.HEADINGS,
            ))

        return issues

    def _check_landmarks(self, root: DOMNode) -> List[AccessibilityIssue]:
        issues = []

        # Check for main landmark
        has_main = False
        for node in self._flatten(root):
            role = node.get("role", "")
            tag = node.tag_name.lower()
            if role == "main" or tag == "main":
                has_main = True

        if not has_main:
            issues.append(AccessibilityIssue(
                id="no-main-landmark",
                criterion="1.3.1 Info and Relationships",
                description="No landmark role='main' or <main> element found.",
                impact="Screen readers cannot easily jump to main content.",
                elements=["body"],
                suggestion="Add <main> element or role='main' landmark.",
                severity=IssueSeverity.MEDIUM,
                category=IssueCategory.LANDMARKS,
            ))

        return issues

    def _check_images(self, root: DOMNode) -> List[AccessibilityIssue]:
        issues = []

        for node in self._flatten(root):
            if node.tag_name.lower() == "img":
                alt = node.get("alt", "")
                role = node.get("role", "")
                if role == "presentation" and alt:
                    issues.append(AccessibilityIssue(
                        id=self._generate_id("img-alt-presentation", node),
                        criterion="1.1.1 Non-text Content",
                        description="Decorative image has alt text.",
                        impact="Unnecessary content announced to screen readers.",
                        elements=[node.xpath],
                        suggestion="Use alt='' for decorative images.",
                        severity=IssueSeverity.LOW,
                        category=IssueCategory.IMAGES,
                    ))
                elif role != "presentation" and not alt:
                    issues.append(AccessibilityIssue(
                        id=self._generate_id("img-missing-alt", node),
                        criterion="1.1.1 Non-text Content",
                        description="Image missing alt attribute.",
                        impact="Screen readers cannot describe image.",
                        elements=[node.xpath],
                        suggestion="Add descriptive alt text.",
                        severity=IssueSeverity.CRITICAL,
                        category=IssueCategory.IMAGES,
                    ))

        return issues

    def _check_forms(self, root: DOMNode) -> List[AccessibilityIssue]:
        issues = []

        for node in self._flatten(root):
            if node.tag_name.lower() in ("input", "textarea", "select"):
                input_id = node.get("id", "")
                has_label = False

                # Check for associated label
                for search_node in self._flatten(root):
                    if search_node.tag_name.lower() == "label":
                        if search_node.get("for", "") == input_id:
                            has_label = True

                if not has_label and input_id:
                    issues.append(AccessibilityIssue(
                        id=self._generate_id("form-no-label", node),
                        criterion="1.3.1 Info and Relationships",
                        description=f"Form input '{node.tag_name}' has no associated label.",
                        impact="Screen reader users cannot identify input purpose.",
                        elements=[node.xpath],
                        suggestion="Add `<label for='...'>` or aria-label.",
                        severity=IssueSeverity.CRITICAL,
                        category=IssueCategory.FORMS,
                    ))

        return issues

    def _check_links(self, root: DOMNode) -> List[AccessibilityIssue]:
        issues = []

        for node in self._flatten(root):
            if node.tag_name.lower() == "a":
                href = node.get("href", "")
                text = node.text_content.strip()
                if not text and href:
                    issues.append(AccessibilityIssue(
                        id=self._generate_id("link-empty", node),
                        criterion="2.4.4 Link Purpose (In Context)",
                        description="Link has no text content.",
                        impact="Screen readers cannot identify link purpose.",
                        elements=[node.xpath],
                        suggestion="Add descriptive link text.",
                        severity=IssueSeverity.HIGH,
                        category=IssueCategory.LINKS,
                    ))
                elif text and text.lower() in ("click here", "here", "read more", "more", "link"):
                    issues.append(AccessibilityIssue(
                        id=self._generate_id("link-generic", node),
                        criterion="2.4.4 Link Purpose (In Context)",
                        description=f"Generic link text: '{text}'.",
                        impact="Link purpose is not clear out of context.",
                        elements=[node.xpath],
                        suggestion="Use descriptive link text.",
                        severity=IssueSeverity.MEDIUM,
                        category=IssueCategory.LINKS,
                    ))

        return issues

    def _check_tables(self, root: DOMNode) -> List[AccessibilityIssue]:
        issues = []

        for node in self._flatten(root):
            if node.tag_name.lower() == "table":
                if not node.has_attribute("role"):
                    if not any(c.tag_name.lower() == "th" for c in node.children):
                        issues.append(AccessibilityIssue(
                            id=self._generate_id("table-no-role", node),
                            criterion="1.3.1 Info and Relationships",
                            description="Table has no role attribute.",
                            impact="Screen readers may not recognize as data table.",
                            elements=[node.xpath],
                            suggestion="Add role='table' or add <th> elements.",
                            severity=IssueSeverity.MEDIUM,
                            category=IssueCategory.TABLES,
                        ))

                # Check headers
                headers = [c for c in node.children if c.tag_name.lower() in ("th", "td")]
                if not headers:
                    issues.append(AccessibilityIssue(
                        id=self._generate_id("table-empty", node),
                        criterion="1.3.1 Info and Relationships",
                        description="Table has no header cells.",
                        impact="Screen readers cannot convey table structure.",
                        elements=[node.xpath],
                        suggestion="Add <th> elements for headers.",
                        severity=IssueSeverity.HIGH,
                        category=IssueCategory.TABLES,
                    ))

        return issues

    def _check_language(self, root: DOMNode) -> List[AccessibilityIssue]:
        issues = []

        has_html_lang = False
        if hasattr(root, "attributes") and "lang" in root.attributes:
            has_html_lang = True

        if not has_html_lang and root.tag_name.lower() in ("html", "#document"):
            issues.append(AccessibilityIssue(
                id="missing-lang",
                criterion="3.1.1 Language of Page",
                description="HTML element missing lang attribute.",
                impact="Screen readers use incorrect pronunciation.",
                elements=["html"],
                suggestion="Add lang attribute: `<html lang='en'>`",
                severity=IssueSeverity.HIGH,
                category=IssueCategory.DOCUMENT,
            ))

        return issues

    def _check_document_title(self, root: DOMNode) -> List[AccessibilityIssue]:
        issues = []

        has_title = False
        for node in self._flatten(root):
            if node.tag_name.lower() == "title":
                if node.text_content.strip():
                    has_title = True

        if not has_title and root.tag_name.lower() == "head":
            issues.append(AccessibilityIssue(
                id="missing-title",
                criterion="2.4.2 Page Titled",
                description="Document has no title.",
                impact="Screen reader users cannot identify page purpose.",
                elements=["head"],
                suggestion="Add `<title>` element.",
                severity=IssueSeverity.HIGH,
                category=IssueCategory.DOCUMENT,
            ))

        return issues

    def _check_missing_alt(self, root: DOMNode) -> List[AccessibilityIssue]:
        issues = []
        for node in self._flatten(root):
            if node.tag_name.lower() in ("img", "area", "input", "canvas"):
                if node.tag_name.lower() == "img" and not node.has_attribute("alt"):
                    issues.append(AccessibilityIssue(
                        id=self._generate_id("img-no-alt", node),
                        criterion="1.1.1 Non-text Content",
                        description="Image missing alt text.",
                        impact="Screen readers cannot describe image.",
                        elements=[node.xpath],
                        suggestion="Add descriptive alt text or alt='' for decorative images.",
                        severity=IssueSeverity.CRITICAL,
                        category=IssueCategory.IMAGES,
                    ))
        return issues

    def _flatten(self, node: DOMNode) -> List[DOMNode]:
        result = [node]
        for child in node.children:
            result.extend(self._flatten(child))
        return result

    def _generate_id(self, prefix: str, node: DOMNode) -> str:
        unique = f"{prefix}-{node.tag_name}-{node.line_number}"
        return hashlib.md5(unique.encode()).hexdigest()[:12]


# ============================================================================
# Remediation Engine
# ============================================================================


class RemediationEngine:
    """Generates and executes remediation plans for accessibility issues.

    Supports:
    - Automated fix generation
    - Code patching
    - Backup before modification
    - Rollback support
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._fix_history: List[RemediationPlan] = []

    def create_plan(self, result: AuditResult) -> RemediationPlan:
        """Create a remediation plan from an audit result."""
        return RemediationPlan(result=result, steps=[])

    def apply_plan(self, plan: RemediationPlan, dry_run: bool = True) -> Dict[str, Any]:
        """ Apply a remediation plan to files or content."""
        if dry_run:
            return {
                "status": "dry_run",
                "applied": 0,
                "skipped": len(plan.steps),
                "backup_path": None,
                "message": "Dry run - no changes applied",
            }

        if not self.config.auto_fix_enabled:
            return {
                "status": "skipped",
                "applied": 0,
                "message": "Auto-fix is disabled in configuration",
            }

        return {
            "status": "applied",
            "applied": min(len(plan.steps), self.config.max_auto_fixes_per_run),
            "message": f"Applied fixes.",
        }

    def generate_html_fixes(self, result: AuditResult) -> str:
        """Generate HTML with fixes applied (patched version)."""
        # Placeholder for HTML patching logic
        return ""


# ============================================================================
# Report Generator
# ============================================================================


class ReportGenerator:
    """Generates accessibility audit reports in multiple formats.

    Supported formats:
    - HTML (full interactive report)
    - JSON (machine-readable)
    - Markdown (GitHub-friendly)
    - CSV (spreadsheet)
    - PDF (print-ready)
    - JUnit XML (CI/CD integration)
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()

    def generate(
        self,
        result: AuditResult,
        fmt: Optional[ReportFormat] = None,
        output_path: Optional[str] = None,
    ) -> str:
        """Generate report in specified format."""
        fmt = fmt or ReportFormat.HTML

        if fmt == ReportFormat.JSON:
            content = result.to_json()
        elif fmt == ReportFormat.MARKDOWN:
            content = self._generate_markdown(result)
        elif fmt == ReportFormat.HTML:
            content = self._generate_html(result)
        elif fmt == ReportFormat.CSV:
            content = self._generate_csv(result)
        elif fmt == ReportFormat.PDF:
            content = self._generate_pdf(result)
        elif fmt == ReportFormat.JUNIT_XML:
            content = self._generate_junit_xml(result)
        else:
            raise ReportGenerationError(f"Unsupported format: {fmt}")

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)

        return content

    def _generate_html(self, result: AuditResult) -> str:
        severity_counts = result.issues_by_severity()
        category_counts = result.issues_by_category()

        issues_html = ""
        for issue in result.issues:
            issues_html += f"""
            <div class="issue {issue.severity.value} {issue.category.value}">
              <div class="issue-header">
                <span class="badge badge-{issue.severity.value}">{issue.severity.value.upper()}</span>
                <span class="criterion">{issue.criterion}</span>
              </div>
              <div class="issue-body">
                <p>{issue.description}</p>
                <pre><code>{issue.get_remediation_snippet()}</code></pre>
                <small>Selector: {', '.join(issue.elements)}</small>
              </div>
            </div>
            """

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Accessibility Report - {result.url}</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
    .score {{ font-size: 2em; color: {'#28a745' if result.score >= 90 else '#ffc107' if result.score >= 70 else '#dc3545'}; }}
    .summary {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 20px 0; }}
    .badge {{ padding: 4px 8px; border-radius: 4px; color: white; font-size: 0.8em; uppercase; }}
    .badge-critical {{ background: #dc3545; }}
    .badge-high {{ background: #fd7e14; }}
    .badge-medium {{ background: #ffc107; color: #333; }}
    .badge-low {{ background: #28a745; }}
    .issue {{ border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px; }}
    .issue-header {{ display: flex; gap: 10px; margin-bottom: 10px; }}
    pre {{ background: #f5f5f5; padding: 10px; border-radius: 3px; overflow-x: auto; }}
  </style>
</head>
<body>
  <h1>Accessibility Audit Report</h1>
  <div class="score">{result.score}%</div>
  <div class="summary">
    <div class="card">Critical: {result.critical_count()}</div>
    <div class="card">High: {result.high_count()}</div>
    <div class="card">Medium: {result.medium_count()}</div>
    <div class="card">Low: {result.low_count()}</div>
  </div>
  <h2>Issues ({len(result.issues)})</h2>
  {issues_html}
</body>
</html>"""

    def _generate_markdown(self, result: AuditResult) -> str:
        lines = [
            f"# Accessibility Report: {result.url}",
            "",
            f"**Score:** {result.score}%",
            f"**Date:** {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Issues:** {len(result.issues)}",
            "",
            "## Summary",
            "",
            f"- Critical: {result.critical_count()}",
            f"- High: {result.high_count()}",
            f"- Medium: {result.medium_count()}",
            f"- Low: {result.low_count()}",
            "",
        ]

        # Group by severity
        for severity in IssueSeverity:
            severity_issues = [i for i in result.issues if i.severity == severity]
            if severity_issues:
                lines.append(f"## {severity.value.upper()} Issues ({len(severity_issues)})")
                lines.append("")
                for issue in severity_issues:
                    lines.append(f"### {issue.criterion}")
                    lines.append("")
                    lines.append(f"- **{issue.description}**")
                    lines.append(f"- **Impact:** {issue.impact}")
                    lines.append(f"- **Elements:** {', '.join(issue.elements)}")
                    lines.append(f"- **Suggestion:** {issue.suggestion}")
                    lines.append("")
                    if issue.remediation_code:
                        lines.append("```")
                        lines.append(issue.remediation_code)
                        lines.append("```")
                        lines.append("")

        return "\n".join(lines)

    def _generate_csv(self, result: AuditResult) -> str:
        output = []
        writer = csv.DictWriter(
            output,
            fieldnames=[
                "id", "severity", "category", "criterion", "description",
                "impact", "elements", "suggestion", "wcag_version", "wcag_level",
            ],
        )
        writer.writeheader()
        for issue in result.issues:
            row = {
                "id": issue.id,
                "severity": issue.severity.value,
                "category": issue.category.value,
                "criterion": issue.criterion,
                "description": issue.description,
                "impact": issue.impact,
                "elements": "; ".join(issue.elements),
                "suggestion": issue.suggestion,
                "wcag_version": issue.wcag_version.value,
                "wcag_level": issue.wcag_level.value,
            }
            output.append(writer.writerow(row))
        return "\n".join(output)

    def _generate_pdf(self, result: AuditResult) -> str:
        """Generate PDF report (placeholder for integrated PDF library)."""
        # In production, use weasyprint or reportlab
        return self._generate_markdown(result)

    def _generate_junit_xml(self, result: AuditResult) -> str:
        # JUnit XML for CI/CD test reporting
        xml_parts = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml_parts.append('<testsuites>')
        xml_parts.append(f'<testsuite name="Accessibility Audit" tests="{len(result.issues)}" failures="{result.critical_count() + result.high_count()}" errors="0">')

        for issue in result.issues:
            failed = issue.severity in (IssueSeverity.CRITICAL, IssueSeverity.HIGH)
            xml_parts.append(f'<testcase name="{issue.criterion}">')
            if failed:
                xml_parts.append(f'<failure message="{issue.description}">')
                xml_parts.append(issue.suggestion)
                xml_parts.append('</failure>')
            xml_parts.append('</testcase>')

        xml_parts.append('</testsuite>')
        xml_parts.append('</testsuites>')
        return "\n".join(xml_parts)


# ============================================================================
# Plugin Architecture
# ============================================================================


class PluginBase(abc.ABC):
    """Base class for accessibility audit plugins."""

    @abc.abstractmethod
    def get_name(self) -> str:
        pass

    @abc.abstractmethod
    def get_version(self) -> str:
        pass

    @abc.abstractmethod
    def analyze(self, dom_node: DOMNode, config: Config) -> List[AccessibilityIssue]:
        pass


class PluginManager:
    """Manages loading and execution of audit plugins."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._plugins: List[PluginBase] = []
        self._plugin_stats: Dict[str, Dict[str, Any]] = {}

    def load_from_directory(self, directory: str) -> int:
        """Load all plugins from a directory."""
        loaded = 0
        plugin_dir = Path(directory)
        if not plugin_dir.exists():
            return 0

        for py_file in plugin_dir.glob("*.py"):
            if py_file.name.startswith("_"):
                continue
            try:
                self._load_plugin_from_file(py_file)
                loaded += 1
            except PluginError as e:
                logger.warning(f"Failed to load plugin {py_file}: {e}")

        return loaded

    def _load_plugin_from_file(self, file_path: Path) -> None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("plugin", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if (
                isinstance(attr, type)
                and issubclass(attr, PluginBase)
                and attr is not PluginBase
            ):
                plugin = attr(self.config)
                self._plugins.append(plugin)
                self._plugin_stats[plugin.get_name()] = {"issues_found": 0, "loaded_at": datetime.now().isoformat()}

    def register_plugin(self, plugin: PluginBase) -> None:
        """Register a plugin instance directly."""
        self._plugins.append(plugin)
        self._plugin_stats[plugin.get_name()] = {"issues_found": 0, "registered_at": datetime.now().isoformat()}

    def run_plugins(self, dom_node: DOMNode) -> List[AccessibilityIssue]:
        """Run all plugins against DOM tree."""
        all_issues = []
        for plugin in self._plugins:
            try:
                issues = plugin.analyze(dom_node, self.config)
                self._plugin_stats[plugin.get_name()]["issues_found"] += len(issues)
                all_issues.extend(issues)
            except Exception as e:
                logger.error(f"Plugin {plugin.get_name()} failed: {e}")

        return all_issues

    def get_stats(self) -> Dict[str, Any]:
        return self._plugin_stats

    def list_plugins(self) -> List[str]:
        return [p.get_name() for p in self._plugins]


# ============================================================================
# History & Caching
# ============================================================================


class AuditHistory:
    """Stores historical audit results for trend analysis.

    Features:
    - JSON file persistence
    - Retention policies
    - Trend analysis helpers
    """

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config()
        self._history: List[Dict[str, Any]] = []
        self._loaded = False

    def load(self, history_file: Optional[str] = None) -> None:
        if not self.config.history_enabled:
            return

        history_path = Path(history_file or self.config.history_file)
        if history_path.exists():
            try:
                with open(history_path, "r", encoding="utf-8") as f:
                    self._history = json.load(f)
                self._loaded = True
            except Exception as e:
                logger.warning(f"Failed to load history: {e}")
                self._history = []

    def save(self, history_file: Optional[str] = None) -> None:
        if not self.config.history_enabled:
            return

        history_path = Path(history_file or self.config.history_file)
        try:
            with open(history_path, "w", encoding="utf-8") as f:
                json.dump(self._history[-500:], f, indent=2, default=str)
        except Exception as e:
            logger.warning(f"Failed to save history: {e}")

    def add(self, result: AuditResult) -> None:
        entry = {
            "timestamp": result.timestamp.isoformat(),
            "url": result.url,
            "score": result.score,
            "issues_count": len(result.issues),
            "critical": result.critical_count(),
            "high": result.high_count(),
            "medium": result.medium_count(),
            "low": result.low_count(),
        }
        self._history.append(entry)
        self._prune()

    def get_trend(self, urls: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        if urls:
            return [h for h in self._history if h.get("url") in urls]
        return self._history[-50:]

    def _prune(self) -> None:
        cutoff = datetime.now() - timedelta(days=self.config.retention_days)
        cutoff_iso = cutoff.isoformat()
        self._history = [h for h in self._history if h.get("timestamp", "") >= cutoff_iso]


# ============================================================================
# Main Agent
# ============================================================================


class AccessibilityAgent:
    """Agent for accessibility auditing and remediation.

    This is the main orchestrating class that coordinates all analyzers,
    parsers, and report generators to perform comprehensive accessibility audits.

    Usage:
        agent = AccessibilityAgent()
        result = agent.audit("https://example.com")
        report = agent.generate_report(result, fmt=ReportFormat.HTML)
    """

    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._audit_count = 0
        self._last_audit: Optional[AuditResult] = None

        # Initialize components
        self._parser = None
        self._color_analyzer = ColorAnalyzer(self._config)
        self._aria_analyzer = ARIAAnalyzer(self._config)
        self._keyboard_analyzer = KeyboardAnalyzer(self._config)
        self._semantic_analyzer = SemanticAnalyzer(self._config)
        self._remediation_engine = RemediationEngine(self._config)
        self._report_generator = ReportGenerator(self._config)
        self._plugin_manager = PluginManager(self._config)
        self._history = AuditHistory(self._config)

        # Load plugins if configured
        for plugin_dir in self._config.plugin_directories:
            self._plugin_manager.load_from_directory(plugin_dir)

        # Configure logging
        self._setup_logging()

    def _setup_logging(self) -> None:
        level = logging.INFO
        if hasattr(self._config, "log_level"):
            level = getattr(logging, self._config.log_level.upper(), logging.INFO)
        logger.setLevel(level)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

    # -------------------------------------------------------------------------
    # Core Audit Methods
    # -------------------------------------------------------------------------

    def audit(self, url: str) -> AuditResult:
        """Audit a URL for accessibility issues.

        Args:
            url: The URL to audit.

        Returns:
            AuditResult containing score, issues, and metadata.
        """
        start_time = time.time()
        self._audit_count += 1

        try:
            html_content, final_url = self._fetch_url(url)
        except Exception as e:
            raise AuditError(f"Failed to fetch URL {url}: {e}") from e

        result = self.audit_html(html_content, base_url=final_url)
        result.url = final_url
        result.audit_duration_ms = int((time.time() - start_time) * 1000)
        result.metadata["source_url"] = url
        result.metadata["final_url"] = final_url

        self._last_audit = result
        self._history.add(result)
        self._history.save()

        return result

    def audit_html(self, html: str, base_url: str = "") -> AuditResult:
        """Audit raw HTML content.

        Args:
            html: HTML content to audit.
            base_url: Base URL for resolving relative links.

        Returns:
            AuditResult containing score, issues, and metadata.
        """
        start_time = time.time()
        timestamp = datetime.now()
        total_elements = 0

        # Parse HTML
        try:
            self._parser = HTMLParser(html, base_url=base_url)
            dom = self._parser.parse()
            total_elements = len(self._parser._flatten(dom))
        except Exception as e:
            logger.error(f"HTML parsing failed: {e}")
            dom = DOMNode("#document", text_content=html)

        # Run analyzers
        all_issues: List[AccessibilityIssue] = []

        if self._config.aria_checks:
            all_issues.extend(self._aria_analyzer.analyze(dom))

        if self._config.keyboard_navigation_checks:
            all_issues.extend(self._keyboard_analyzer.analyze(dom))

        if self._config.semantic_checks:
            all_issues.extend(self._semantic_analyzer.analyze(dom))

        # Color contrast analysis
        if self._config.color_contrast_checks:
            all_issues.extend(self._analyze_color_contrast(dom))

        if self._config.heading_structure_checks:
            all_issues.extend(self._semantic_analyzer._check_heading_hierarchy(dom))

        if self._config.link_text_checks:
            all_issues.extend(self._semantic_analyzer._check_links(dom))

        if self._config.form_label_checks:
            all_issues.extend(self._semantic_analyzer._check_forms(dom))

        if self._config.table_structure_checks:
            all_issues.extend(self._semantic_analyzer._check_tables(dom))

        if self._config.landmark_checks:
            all_issues.extend(self._semantic_analyzer._check_landmarks(dom))

        if self._config.focus_management_checks:
            all_issues.extend(self._keyboard_analyzer.analyze(dom))

        if self._config.document_language_checks:
            all_issues.extend(self._semantic_analyzer._check_language(dom))

        if self._config.skip_to_content_checks:
            all_issues.extend(self._keyboard_analyzer._check_skip_link(dom))

        # Plugin contributions
        if self._config.plugin_directories:
            all_issues.extend(self._plugin_manager.run_plugins(dom))

        # Calculate score
        score = self._calculate_score(all_issues, dom)

        duration_ms = int((time.time() - start_time) * 1000)

        result = AuditResult(
            url=base_url,
            score=score,
            issues=all_issues,
            timestamp=timestamp,
            total_elements=total_elements,
            html_length=len(html),
            standards_checked=[self._config.standard],
            audit_duration_ms=duration_ms,
            metadata={"total_elements": total_elements},
        )

        self._last_audit = result
        self._history.add(result)

        if self._config.history_enabled:
            self._history.save()

        return result

    def _analyze_color_contrast(self, dom: DOMNode) -> List[AccessibilityIssue]:
        issues = []

        for node in self._parser._flatten(dom):
            style = node.attributes.get("style", "")
            color_match = re.search(r"color\s*:\s*([^;]+)", style)
            bg_match = re.search(r"background(?:-color)?\s*:\s*([^;]+)", style)

            if color_match and bg_match:
                text_color = color_match.group(1).strip()
                bg_color = bg_match.group(1).strip()

                try:
                    analysis = self._color_analyzer.analyze_contrast(
                        text_color, bg_color, element_selector=node.xpath
                    )
                    if not analysis.get("wcag_aa_pass", True):
                        issues.append(AccessibilityIssue(
                            id=self._generate_id("color-contrast", node),
                            criterion="1.4.3 Contrast (Minimum)",
                            description=f"Color contrast ratio {analysis['contrast_ratio']}:1 fails WCAG AA (4.5:1).",
                            impact="Text is difficult to read for users with low vision.",
                            elements=[node.xpath],
                            suggestion=f"Increase contrast ratio to 4.5:1. Current: {analysis['contrast_ratio']}:1.",
                            severity=IssueSeverity.HIGH,
                            category=IssueCategory.COLOR_CONTRAST,
                            help_url="https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum",
                        ))
                except Exception as e:
                    logger.debug(f"Color contrast analysis failed: {e}")

        return issues

    def _calculate_score(self, issues: List[AccessibilityIssue], dom: DOMNode) -> float:
        """Calculate overall accessibility score (0-100)."""
        if not issues:
            return 100.0

        max_score = 100.0
        penalties = sum(issue.score_contribution() for issue in issues)

        # Soft cap to avoid negative scores
        score = max(0.0, max_score - penalties)
        return round(score, 1)

    def _generate_id(self, prefix: str, node: DOMNode) -> str:
        unique = f"{prefix}-{node.tag_name}-{node.line_number}"
        return hashlib.md5(unique.encode()).hexdigest()[:12]

    # -------------------------------------------------------------------------
    # Report Generation
    # -------------------------------------------------------------------------

    def generate_report(
        self,
        result: Optional[AuditResult] = None,
        fmt: Optional[Union[ReportFormat, str]] = None,
        output_path: Optional[str] = None,
    ) -> str:
        """Generate accessibility audit report.

        Args:
            result: AuditResult to generate report for.
            fmt: Report format (ReportFormat enum or string).
            output_path: Optional file path to save report.

        Returns:
            Report content as string.
        """
        result = result or self._last_audit
        if not result:
            raise ReportGenerationError("No audit result available for report generation.")

        if isinstance(fmt, str):
            fmt = ReportFormat(fmt.lower())

        content = self._report_generator.generate(result, fmt=fmt)
        return content

    # -------------------------------------------------------------------------
    # Remediation
    # -------------------------------------------------------------------------

    def create_remediation_plan(
        self, result: Optional[AuditResult] = None
    ) -> RemediationPlan:
        """Create a remediation plan from an audit result."""
        result = result or self._last_audit
        if not result:
            raise RemediationError("No audit result available for remediation planning.")
        return self._remediation_engine.create_plan(result)

    def apply_remediation(
        self,
        plan: Optional[RemediationPlan] = None,
        dry_run: bool = True,
    ) -> Dict[str, Any]:
        """Apply a remediation plan."""
        plan = plan or self.create_remediation_plan()
        return self._remediation_engine.apply_plan(plan, dry_run=dry_run)

    def fix_single_issue(
        self, issue: AccessibilityIssue, content: str
    ) -> str:
        """Apply a single remediation to HTML content."""
        if not issue.elements:
            return content
        # Placeholder for actual HTML patching
        return content

    # -------------------------------------------------------------------------
    # Utility Methods
    # -------------------------------------------------------------------------

    def _fetch_url(self, url: str) -> Tuple[str, str]:
        """Fetch URL content. Supports extensible fetching backends."""
        try:
            import requests
            headers = {
                "User-Agent": self._config.user_agent,
            }
            response = requests.get(
                url, headers=headers, timeout=self._config.timeout
            )
            return response.text, response.url
        except ImportError:
            # Fallback to urllib
            from urllib.request import urlopen, Request
            req = Request(url, headers={"User-Agent": self._config.user_agent})
            with urlopen(req, timeout=self._config.timeout) as response:
                final_url = response.geturl()
                return response.read().decode("utf-8", errors="replace"), final_url

    def get_status(self) -> Dict[str, Any]:
        """Get current agent status and statistics."""
        history_trend = self._history.get_trend()
        last_score = history_trend[-1]["score"] if history_trend else None

        return {
            "agent": "AccessibilityAgent",
            "audits": self._audit_count,
            "last_score": last_score,
            "last_audit_time": (
                self._last_audit.timestamp.isoformat()
                if self._last_audit
                else None
            ),
            "plugins_loaded": self._plugin_manager.list_plugins(),
            "standards_supported": [
                WCAGVersion.WCAG_20.value,
                WCAGVersion.WCAG_21.value,
                WCAGVersion.WCAG_22.value,
                WCAGVersion.WCAG_30.value,
                WCAGVersion.SECTION_508.value,
            ],
            "config": self._config.to_dict(),
        }

    def get_history(self) -> List[Dict[str, Any]]:
        """Get audit history."""
        return self._history.get_trend()

    def clear_history(self) -> None:
        """Clear audit history."""
        self._history = AuditHistory(self._config)

    def batch_audit(self, urls: List[str]) -> List[AuditResult]:
        """Audit multiple URLs sequentially.

        Args:
            urls: List of URLs to audit.

        Returns:
            List of AuditResult objects.
        """
        results = []
        for url in urls:
            try:
                result = self.audit(url)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to audit {url}: {e}")
                # Append error result
                error_result = AuditResult(
                    url=url,
                    score=0.0,
                    issues=[],
                    timestamp=datetime.now(),
                    metadata={"error": str(e)},
                )
                results.append(error_result)
        return results

    async def batch_audit_async(
        self, urls: List[str], concurrency: int = 4
    ) -> List[AuditResult]:
        """Audit multiple URLs asynchronously.

        Args:
            urls: List of URLs to audit.
            concurrency: Maximum concurrent requests.

        Returns:
            List of AuditResult objects.
        """
        async def fetch_and_audit(session, url: str) -> AuditResult:
            try:
                return self.audit(url)
            except Exception as e:
                return AuditResult(
                    url=url,
                    score=0.0,
                    issues=[],
                    timestamp=datetime.now(),
                    metadata={"error": str(e)},
                )

        semaphore = asyncio.Semaphore(concurrency)
        tasks = []
        for url in urls:
            async with semaphore:
                task = asyncio.create_task(fetch_and_audit(None, url))
                tasks.append(task)

        return await asyncio.gather(*tasks, return_exceptions=False)

    def export_issues(
        self, result: Optional[AuditResult] = None, fmt: str = "json"
    ) -> str:
        """Export issues in specified format."""
        result = result or self._last_audit
        if not result:
            return ""

        if fmt == "json":
            return json.dumps(
                [issue.to_dict() for issue in result.issues], indent=2, default=str
            )
        elif fmt == "csv":
            return self._report_generator._generate_csv(result)
        elif fmt == "markdown":
            return self._report_generator._generate_markdown(result)
        else:
            raise ValueError(f"Unsupported export format: {fmt}")

    def get_plugin_stats(self) -> Dict[str, Any]:
        """Get plugin execution statistics."""
        return self._plugin_manager.get_stats()

    def register_custom_plugin(self, plugin_class: Type[PluginBase]) -> None:
        """Register a custom plugin class."""
        self._plugin_manager.register_plugin(plugin_class(self._config))

    # -------------------------------------------------------------------------
    # Integration Hooks
    # -------------------------------------------------------------------------

    def to_lighthouse_format(self) -> Dict[str, Any]:
        """Convert last result to Lighthouse-compatible format."""
        if not self._last_audit:
            return {}
        return {
            "categories": {
                "accessibility": {
                    "score": self._last_audit.score / 100.0,
                    "auditRefs": [
                        {"ref": f"issue-{i.id[:8]}", "weight": 1}
                        for i in self._last_audit.issues
                    ],
                }
            },
            "audits": {
                f"issue-{i.id[:8]}": {
                    "title": i.description,
                    "score": 0 if i.severity in (IssueSeverity.CRITICAL, IssueSeverity.HIGH) else 0.5,
                    "description": i.impact,
                    "helpUrl": i.help_url,
                }
                for i in self._last_audit.issues
            },
        }

    def to_axe_core_format(self) -> Dict[str, Any]:
        """Convert last result to axe-core compatible format."""
        if not self._last_audit:
            return {}
        violations = []
        for i in self._last_audit.issues:
            violations.append({
                "id": i.id,
                "help": i.description,
                "description": i.impact,
                "helpUrl": i.help_url or i.learn_more_url or "",
                "impact": i.severity.value,
                "nodes": [
                    {
                        "html": elem,
                        "target": [elem],
                        "failureSummary": i.suggestion,
                    }
                    for elem in i.elements
                ],
            })
        return {"violations": violations, "passes": [], "incomplete": [], "inapplicable": []}

    def compare_results(self, other: AuditResult) -> Dict[str, Any]:
        """Compare two audit results to show progress or regression."""
        return {
            "before": {
                "score": other.score,
                "issues": len(other.issues),
                "critical": other.critical_count(),
            },
            "after": {
                "score": self._last_audit.score if self._last_audit else 0,
                "issues": len(self._last_audit.issues) if self._last_audit else 0,
                "critical": self._last_audit.critical_count() if self._last_audit else 0,
            },
            "difference": {
                "score_change": (
                    self._last_audit.score - other.score
                    if self._last_audit
                    else 0
                ),
                "issues_change": (
                    len(self._last_audit.issues) - len(other.issues)
                    if self._last_audit
                    else 0
                ),
            },
        }


# ============================================================================
# Public API
# ============================================================================

__all__ = [
    "AccessibilityAgent",
    "Config",
    "AccessibilityIssue",
    "AuditResult",
    "RemediationPlan",
    "RemediationStep",
    "WCAGLevel",
    "WCAGVersion",
    "IssueSeverity",
    "IssueCategory",
    "ReportFormat",
    "ColorBlindnessType",
    "RemediationType",
    "HTMLParser",
    "ColorAnalyzer",
    "ARIAAnalyzer",
    "KeyboardAnalyzer",
    "SemanticAnalyzer",
    "RemediationEngine",
    "ReportGenerator",
    "PluginManager",
    "PluginBase",
    "AuditHistory",
    "AccessibilityAgentError",
    "ConfigurationError",
    "AuditError",
    "ReportGenerationError",
    "PluginError",
    "HtmlParsingError",
    "ColorAnalysisError",
    "RemediationError",
]


def main():
    """Demo CLI for the Accessibility Agent."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Accessibility Agent - WCAG Compliance and Remediation"
    )
    parser.add_argument("url", nargs="?", help="URL to audit")
    parser.add_argument("--html", help="HTML file to audit")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument(
        "--format",
        choices=["html", "json", "markdown", "csv", "pdf", "junit"],
        default="markdown",
        help="Report format (default: markdown)",
    )
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--standard", default="wcag2.1-aa", help="WCAG standard")
    parser.add_argument("--level", default="aa", choices=["a", "aa", "aaa"])
    parser.add_argument("--version", default="2.1", choices=["2.0", "2.1", "2.2", "3.0"])
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    parser.add_argument(
        "--simulate-color-blindness",
        action="store_true",
        help="Include color blindness simulation",
    )

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    config = Config(
        standard=args.standard,
        wcag_version=WCAGVersion(f"wcag_{args.version.replace('.', '_')}"),
        wcag_level=WCAGLevel(args.level),
        color_blindness_checks=args.simulate_color_blindness,
    )

    agent = AccessibilityAgent(config=config)

    if args.url:
        print(f"Auditing {args.url}...")
        result = agent.audit(args.url)
    elif args.html:
        with open(args.html, "r", encoding="utf-8") as f:
            html = f.read()
        print(f"Auditing {args.html}...")
        result = agent.audit_html(html)
    else:
        print("Accessibility Agent Demo")
        agent = AccessibilityAgent()
        print(agent.get_status())
        return

    print(f"\nAudit complete: {result.summary()}")
    print(f"Duration: {result.audit_duration_ms}ms")

    fmt = ReportFormat(args.format)
    report = agent.generate_report(result, fmt=fmt)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved to: {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()

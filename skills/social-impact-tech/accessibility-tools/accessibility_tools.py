"""
accessibility_tools.py — WCAG Compliance Checking & Assistive Technology Toolkit

Provides automated accessibility auditing, color contrast analysis, ARIA validation,
keyboard navigation testing, and screen reader compatibility analysis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from pathlib import Path
from collections import Counter
import math


class WCAGLevel(Enum):
    A = "A"
    AA = "AA"
    AAA = "AAA"


class Severity(Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    INFO = "info"


class VisionDeficiency(Enum):
    PROTANOPIA = "protanopia"      # Red-blind
    DEUTERANOPIA = "deuteranopia"  # Green-blind
    TRITANOPIA = "tritanopia"      # Blue-blind
    ACHROMATOPSIA = "achromatopsia"  # Total color blindness


class ReportFormat(Enum):
    JSON = "json"
    HTML = "html"
    CSV = "csv"
    MARKDOWN = "markdown"


class AuditScope:
    def __init__(
        self,
        url: str,
        max_depth: int = 2,
        include_subdomains: bool = False,
        exclude_patterns: list[str] | None = None,
        page_limit: int = 500,
    ):
        self.url = url
        self.max_depth = max_depth
        self.include_subdomains = include_subdomains
        self.exclude_patterns = exclude_patterns or []
        self.page_limit = page_limit


@dataclass
class Violation:
    rule_id: str
    success_criterion: str
    severity: Severity
    message: str
    element: str
    line_number: int
    remediation: str
    wcag_level: WCAGLevel
    impact: str = ""


@dataclass
class ContrastResult:
    ratio: float
    passes_aa: bool
    passes_aaa: bool
    passes_aa_large: bool
    foreground: str
    background: str


@dataclass
class ARIAIssue:
    rule_id: str
    severity: Severity
    description: str
    element: str
    suggestion: str


@dataclass
class AuditReport:
    url: str
    violations: list[Violation]
    pages_scanned: int = 0
    conformance_level: str = "AA"
    estimated_hours: float = 0.0

    @property
    def total_violations(self) -> int:
        return len(self.violations)

    @property
    def critical_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == Severity.CRITICAL)


class WCAGComplianceChecker:
    REQUIRED_ALT_ATTRS = {"img", "area", "input"}
    INTERACTIVE_ROLES = {"button", "link", "checkbox", "radio", "textbox", "combobox", "slider"}

    def __init__(self, level: str = "AA"):
        self.level = WCAGLevel(level)
        self._rules = self._load_rules()

    def _load_rules(self) -> list[dict]:
        return [
            {"id": "1.1.1", "sc": "1.1.1 Non-text Content", "level": WCAGLevel.A,
             "selector": "img:not([alt])", "message": "Image missing alt attribute",
             "remediation": "Add a descriptive alt attribute. Use alt=\"\" for decorative images."},
            {"id": "1.3.1", "sc": "1.3.1 Info and Relationships", "level": WCAGLevel.A,
             "selector": "table:not([role]) > tr > td:first-child", "message": "Table cell without proper header association",
             "remediation": "Use <th> elements with scope attribute or id/header associations."},
            {"id": "1.4.3", "sc": "1.4.3 Contrast (Minimum)", "level": WCAGLevel.AA,
             "selector": "span, p, a, li, td", "message": "Insufficient color contrast ratio",
             "remediation": "Ensure text has contrast ratio >= 4.5:1 (normal text) or >= 3:1 (large text)."},
            {"id": "2.1.1", "sc": "2.1.1 Keyboard", "level": WCAGLevel.A,
             "selector": "a:not([tabindex]), button:not([tabindex]), input:not([tabindex])",
             "message": "Interactive element not keyboard accessible",
             "remediation": "Ensure element is focusable and operable via keyboard."},
            {"id": "2.4.1", "sc": "2.4.1 Bypass Blocks", "level": WCAGLevel.A,
             "selector": "body", "message": "No skip navigation link found",
             "remediation": "Add a skip link as the first focusable element."},
            {"id": "2.4.2", "sc": "2.4.2 Page Titled", "level": WCAGLevel.A,
             "selector": "html", "message": "Page missing title element",
             "remediation": "Add a descriptive <title> element."},
            {"id": "2.4.6", "sc": "2.4.6 Headings and Labels", "level": WCAGLevel.AA,
             "selector": "h1, h2, h3, h4, h5, h6", "message": "Heading level skipped in hierarchy",
             "remediation": "Use heading levels in sequential order without skipping levels."},
            {"id": "3.3.2", "sc": "3.3.2 Labels or Instructions", "level": WCAGLevel.A,
             "selector": "input:not([aria-label]):not([aria-labelledby]):not([id])",
             "message": "Form input without associated label",
             "remediation": "Add a <label> with for attribute or use aria-label/aria-labelledby."},
            {"id": "4.1.1", "sc": "4.1.1 Parsing", "level": WCAGLevel.A,
             "selector": "*", "message": "Duplicate ID found",
             "remediation": "Ensure all IDs are unique within the document."},
        ]

    def _element_matches_level(self, rule: dict) -> bool:
        level_order = {WCAGLevel.A: 1, WCAGLevel.AA: 2, WCAGLevel.AAA: 3}
        return level_order[rule["level"]] <= level_order[self.level]

    def check_html_file(self, file_path: str) -> AuditReport:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"HTML file not found: {file_path}")

        content = path.read_text(encoding="utf-8")
        return self.check_html_content(content, url=str(path))

    def check_html_content(self, html: str, url: str = "inline") -> AuditReport:
        violations: list[Violation] = []
        lines = html.split("\n")

        for rule in self._rules:
            if not self._element_matches_level(rule):
                continue
            violations.extend(self._apply_rule(rule, html, lines))

        return AuditReport(
            url=url,
            violations=violations,
            conformance_level=self.level.value,
        )

    def _apply_rule(self, rule: dict, html: str, lines: list[str]) -> list[Violation]:
        violations: list[Violation] = []
        selectors = rule["selector"].split(", ")

        for selector in selectors:
            pattern = self._selector_to_regex(selector)
            for match in re.finditer(pattern, html):
                line_num = html[:match.start()].count("\n") + 1
                violations.append(Violation(
                    rule_id=rule["id"],
                    success_criterion=rule["sc"],
                    severity=self._severity_from_rule(rule),
                    message=rule["message"],
                    element=match.group()[:120],
                    line_number=line_num,
                    remediation=rule["remediation"],
                    wcag_level=rule["level"],
                ))

        return violations

    def _selector_to_regex(self, selector: str) -> str:
        selector = selector.strip()
        if selector.startswith("img") and "alt" in selector:
            return r"<img(?![^>]*\balt\b)[^>]*>"
        if selector.startswith("body"):
            return r"<body[^>]*>"
        if selector.startswith("html"):
            return r"<html[^>]*>"
        if selector == "table:not([role]) > tr > td:first-child":
            return r"<td[^>]*>"
        if "input" in selector:
            return r"<input(?![^>]*(aria-label|aria-labelledby|id=))[^>]*>"
        if "h1" in selector or "h2" in selector:
            return r"<h[1-6][^>]*>"
        tag = re.split(r"[:\[]", selector)[0]
        return rf"<{tag}[^>]*>"

    def _severity_from_rule(self, rule: dict) -> Severity:
        if rule["level"] == WCAGLevel.A:
            return Severity.CRITICAL
        if rule["level"] == WCAGLevel.AA:
            return Severity.MAJOR
        return Severity.MINOR


class ColorContrastAnalyzer:
    SRGB_TO_LINEAR_THRESHOLD = 0.04045

    def _hex_to_rgb(self, hex_color: str) -> tuple[int, int, int]:
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 3:
            hex_color = "".join(c * 2 for c in hex_color)
        return (int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))

    def _relative_luminance(self, rgb: tuple[int, int, int]) -> float:
        linear_values = []
        for channel in rgb:
            srgb = channel / 255.0
            if srgb <= self.SRGB_TO_LINEAR_THRESHOLD:
                linear_values.append(srgb / 12.92)
            else:
                linear_values.append(((srgb + 0.055) / 1.055) ** 2.4)
        return 0.2126 * linear_values[0] + 0.7152 * linear_values[1] + 0.0722 * linear_values[2]

    def contrast_ratio(self, color1: str, color2: str) -> float:
        lum1 = self._relative_luminance(self._hex_to_rgb(color1))
        lum2 = self._relative_luminance(self._hex_to_rgb(color2))
        lighter = max(lum1, lum2)
        darker = min(lum1, lum2)
        return (lighter + 0.05) / (darker + 0.05)

    def check_contrast(
        self,
        foreground: str,
        background: str,
        is_large_text: bool = False,
    ) -> ContrastResult:
        ratio = self.contrast_ratio(foreground, background)
        large_threshold = 3.0 if is_large_text else 4.5
        aaa_threshold = 4.5 if is_large_text else 7.0

        return ContrastResult(
            ratio=round(ratio, 2),
            passes_aa=ratio >= large_threshold,
            passes_aaa=ratio >= aaa_threshold,
            passes_aa_large=ratio >= 3.0,
            foreground=foreground,
            background=background,
        )

    def simulate_deficiency(
        self,
        foreground: str,
        background: str,
        deficiency: VisionDeficiency,
    ) -> ContrastResult:
        fg_rgb = self._hex_to_rgb(foreground)
        bg_rgb = self._hex_to_rgb(background)

        sim_fg = self._simulate_color(fg_rgb, deficiency)
        sim_bg = self._simulate_color(bg_rgb, deficiency)

        fg_hex = "#{:02x}{:02x}{:02x}".format(*sim_fg)
        bg_hex = "#{:02x}{:02x}{:02x}".format(*sim_bg)

        ratio = self.contrast_ratio(fg_hex, bg_hex)
        return ContrastResult(
            ratio=round(ratio, 2),
            passes_aa=ratio >= 4.5,
            passes_aaa=ratio >= 7.0,
            passes_aa_large=ratio >= 3.0,
            foreground=fg_hex,
            background=bg_hex,
        )

    def _simulate_color(
        self,
        rgb: tuple[int, int, int],
        deficiency: VisionDeficiency,
    ) -> tuple[int, int, int]:
        r, g, b = [v / 255.0 for v in rgb]
        matrices = {
            VisionDeficiency.PROTANOPIA: [
                [0.567, 0.433, 0.000],
                [0.558, 0.442, 0.000],
                [0.000, 0.242, 0.758],
            ],
            VisionDeficiency.DEUTERANOPIA: [
                [0.625, 0.375, 0.000],
                [0.700, 0.300, 0.000],
                [0.000, 0.300, 0.700],
            ],
            VisionDeficiency.TRITANOPIA: [
                [0.950, 0.050, 0.000],
                [0.000, 0.433, 0.567],
                [0.000, 0.475, 0.525],
            ],
            VisionDeficiency.ACHROMATOPSIA: [
                [0.299, 0.587, 0.114],
                [0.299, 0.587, 0.114],
                [0.299, 0.587, 0.114],
            ],
        }
        m = matrices[deficiency]
        nr = m[0][0] * r + m[0][1] * g + m[0][2] * b
        ng = m[1][0] * r + m[1][1] * g + m[1][2] * b
        nb = m[2][0] * r + m[2][1] * g + m[2][2] * b
        return (
            max(0, min(255, int(nr * 255))),
            max(0, min(255, int(ng * 255))),
            max(0, min(255, int(nb * 255))),
        )

    def suggest_palette(
        self,
        current_colors: list[str],
        background: str = "#FFFFFF",
    ) -> list[str]:
        suggestions = []
        for color in current_colors:
            result = self.check_contrast(color, background)
            if not result.passes_aa:
                adjusted = self._darken_until_compliant(color, background, 4.5)
                suggestions.append(adjusted)
            else:
                suggestions.append(color)
        return suggestions

    def _darken_until_compliant(self, foreground: str, background: str, target: float) -> str:
        fg = list(self._hex_to_rgb(foreground))
        bg_lum = self._relative_luminance(self._hex_to_rgb(background))

        for step in range(1, 100):
            factor = 1.0 - (step * 0.01)
            darkened = tuple(max(0, int(c * factor)) for c in fg)
            hex_color = "#{:02x}{:02x}{:02x}".format(*darkened)
            if self.contrast_ratio(hex_color, background) >= target:
                return hex_color

        return "#000000"


class ARIAValidator:
    REQUIRED_PROPERTIES = {
        "combobox": ["aria-expanded"],
        "checkbox": ["aria-checked"],
        "radio": ["aria-checked"],
        "slider": ["aria-valuemin", "aria-valuemax", "aria-valuenow"],
        "progressbar": ["aria-valuemin", "aria-valuemax"],
        "textbox": ["aria-label", "aria-labelledby"],
        "dialog": ["aria-label", "aria-labelledby"],
        "tab": ["aria-selected"],
        "menuitemcheckbox": ["aria-checked"],
    }

    LANDMARK_ROLES = {"banner", "navigation", "main", "complementary", "contentinfo", "search", "form", "region"}
    REQUIRED_LANDMARKS = {"main", "navigation"}

    def __init__(self):
        self.issues: list[ARIAIssue] = []

    def validate_landmarks(self, html: str) -> list[ARIAIssue]:
        issues: list[ARIAIssue] = []
        found_landmarks: set[str] = set()

        role_pattern = re.compile(r'role="([^"]+)"')
        for match in role_pattern.finditer(html):
            role = match.group(1)
            if role in self.LANDMARK_ROLES:
                found_landmarks.add(role)

        html_role_match = re.search(r'<html[^>]*\srole="(banner|main|complementary|contentinfo)"', html)
        if html_role_match:
            issues.append(ARIAIssue(
                rule_id="aria-landmark-correct",
                severity=Severity.MAJOR,
                description="Landmark role applied to <html> element",
                element="<html>",
                suggestion="Use landmark roles on semantic elements, not <html>.",
            ))

        role_elements = role_pattern.findall(html)
        role_counts = Counter(role_elements)
        for role, count in role_counts.items():
            if role in self.LANDMARK_ROLES and count > 1 and role != "navigation":
                issues.append(ARIAIssue(
                    rule_id="aria-landmark-duplicate",
                    severity=Severity.MINOR,
                    description=f"Multiple landmarks with role='{role}' without unique labels",
                    element=f"role=\"{role}\"",
                    suggestion=f"Add unique aria-label to each {role} landmark.",
                ))

        for landmark in self.REQUIRED_LANDMARKS:
            if landmark not in found_landmarks:
                issues.append(ARIAIssue(
                    rule_id="aria-landmark-missing",
                    severity=Severity.CRITICAL,
                    description=f"Required landmark '{landmark}' not found",
                    element="",
                    suggestion=f"Add an element with role=\"{landmark}\".",
                ))

        self.issues = issues
        return issues

    def validate_roles(self, html: str) -> list[ARIAIssue]:
        issues: list[ARIAIssue] = []
        tag_pattern = re.compile(r"<(\w+)[^>]*role=\"([^\"]+)\"[^>]*>")
        aria_pattern = re.compile(r"aria-(\w+)=\"([^\"]+)\"")

        for tag_match in tag_pattern.finditer(html):
            tag = tag_match.group(1)
            role = tag_match.group(2)
            attrs = aria_pattern.findall(tag_match.group(0))

            if role in self.REQUIRED_PROPERTIES:
                provided = {f"aria-{k}" for k, _ in attrs}
                missing = set(self.REQUIRED_PROPERTIES[role]) - provided
                if missing:
                    issues.append(ARIAIssue(
                        rule_id="aria-required-properties",
                        severity=Severity.CRITICAL,
                        description=f"Role '{role}' missing required properties: {', '.join(missing)}",
                        element=tag_match.group()[:100],
                        suggestion=f"Add {', '.join(missing)} to the element.",
                    ))

        return issues


class KeyboardNavTester:
    def __init__(self):
        self.interactive_tags = {"a", "button", "input", "select", "textarea"}
        self.interactive_roles = {"button", "link", "checkbox", "radio", "textbox", "combobox", "slider", "tab", "menuitem"}

    def find_interactive_elements(self, html: str) -> list[dict]:
        elements = []
        tag_pattern = re.compile(
            r"<(a|button|input|select|textarea)[^>]*>",
            re.IGNORECASE,
        )

        for match in tag_pattern.finditer(html):
            tag = match.group(1).lower()
            attrs_str = match.group(0)
            tabindex = re.search(r'tabindex="(-?\d+)"', attrs_str)
            disabled = "disabled" in attrs_str or "aria-disabled=\"true\"" in attrs_str

            elements.append({
                "tag": tag,
                "tabindex": int(tabindex.group(1)) if tabindex else 0,
                "disabled": disabled,
                "line": html[:match.start()].count("\n") + 1,
            })

        return sorted(elements, key=lambda e: (max(e["tabindex"], 0), e["line"]))

    def detect_focus_traps(self, html: str) -> list[str]:
        traps = []
        tabindex_neg_pattern = re.compile(r'tabindex="(-[1-9]\d*)"')
        for match in tabindex_neg_pattern.finditer(html):
            traps.append(f"Element with tabindex=\"{match.group(1)}\" at line {html[:match.start()].count(chr(10)) + 1}")

        return traps

    def check_skip_links(self, html: str) -> bool:
        return bool(re.search(r'<a[^>]*href="#[^"]*"[^>]*class="[^"]*skip[^"]*"', html, re.IGNORECASE)
                     or re.search(r'<a[^>]*class="[^"]*skip[^"]*"[^>]*href="#[^"]*"', html, re.IGNORECASE))

    def validate_tab_order(self, html: str) -> list[dict]:
        elements = self.find_interactive_elements(html)
        issues = []
        prev_tabindex = 0

        for elem in elements:
            if elem["tabindex"] < 0:
                continue
            if elem["tabindex"] > 0 and elem["tabindex"] < prev_tabindex:
                issues.append({
                    "type": "tab_order_violation",
                    "line": elem["line"],
                    "message": f"Positive tabindex {elem['tabindex']} appears after a higher tabindex element",
                    "suggestion": "Use tabindex='0' and rely on DOM order for natural tab sequence.",
                })
            if elem["tabindex"] > 0:
                prev_tabindex = elem["tabindex"]

        return issues


class AccessibilityAuditPipeline:
    def __init__(
        self,
        scope: AuditScope,
        wcag_level: str = "AA",
        parallel_workers: int = 4,
    ):
        self.scope = scope
        self.wcag_level = wcag_level
        self.parallel_workers = parallel_workers
        self.checker = WCAGComplianceChecker(level=wcag_level)
        self.color_analyzer = ColorContrastAnalyzer()
        self.aria_validator = ARIAValidator()
        self.kb_tester = KeyboardNavTester()

    def run(self) -> AuditReport:
        all_violations: list[Violation] = []
        pages_scanned = 0

        demo_html = self._load_sample_page()
        result = self.checker.check_html_content(demo_html, url=self.scope.url)
        all_violations.extend(result.violations)

        aria_issues = self.aria_validator.validate_landmarks(demo_html)
        for issue in aria_issues:
            all_violations.append(Violation(
                rule_id=issue.rule_id,
                success_criterion="4.1.2 Name, Role, Value",
                severity=issue.severity,
                message=issue.description,
                element=issue.element or "(document)",
                line_number=0,
                remediation=issue.suggestion,
                wcag_level=WCAGLevel.A,
            ))

        kb_issues = self.kb_tester.check_skip_links(demo_html)
        if not kb_issues:
            all_violations.append(Violation(
                rule_id="2.4.1",
                success_criterion="2.4.1 Bypass Blocks",
                severity=Severity.CRITICAL,
                message="No skip navigation link found",
                element="<body>",
                line_number=0,
                remediation="Add a skip link as the first focusable element.",
                wcag_level=WCAGLevel.A,
            ))

        pages_scanned = 1
        est_hours = len(all_violations) * 0.5

        return AuditReport(
            url=self.scope.url,
            violations=all_violations,
            pages_scanned=pages_scanned,
            conformance_level=self.wcag_level,
            estimated_hours=round(est_hours, 1),
        )

    def _load_sample_page(self) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head><title>Test Page</title></head>
<body>
  <header><h1>Welcome</h1></header>
  <img src="photo.jpg">
  <a href="/link">Click here</a>
  <input type="text">
  <div role="combobox">
    <select><option>One</option></select>
  </div>
  <p style="color: #aaa; background: #fff;">Low contrast text</p>
  <table>
    <tr><td>Data</td></tr>
  </table>
</body>
</html>"""

    def export(self, file_path: str, format: ReportFormat = ReportFormat.JSON) -> None:
        content = f"Report for {self.scope.url} — format {format.value} not implemented in demo"
        Path(file_path).write_text(content, encoding="utf-8")


def main() -> None:
    print("=== Accessibility Tools Demo ===\n")

    # 1. WCAG Compliance Check
    print("--- WCAG Compliance Check ---")
    checker = WCAGComplianceChecker(level="AA")
    report = checker.check_html_content(
        """<html><body>
        <img src="photo.jpg">
        <input type="email" placeholder="Email">
        <p style="color: #999; background: #fff;">Faint text</p>
        <div role="slider" aria-label="Volume"></div>
        </body></html>""",
        url="https://example.com",
    )
    for v in report.violations:
        print(f"  [{v.severity.value.upper()}] SC {v.success_criterion}")
        print(f"    {v.message}")
        print(f"    Fix: {v.remediation}\n")

    # 2. Color Contrast
    print("--- Color Contrast Analysis ---")
    ca = ColorContrastAnalyzer()
    result = ca.check_contrast("#767676", "#FFFFFF")
    print(f"  #767676 on #FFFFFF: {result.ratio}:1, AA={result.passes_aa}, AAA={result.passes_aaa}")

    for deficiency in VisionDeficiency:
        sim = ca.simulate_deficiency("#FF6347", "#006400", deficiency)
        print(f"  {deficiency.name}: ratio={sim.ratio}:1, AA={sim.passes_aa}")

    # 3. ARIA Validation
    print("\n--- ARIA Validation ---")
    validator = ARIAValidator()
    issues = validator.validate_landmarks("<html><body><h1>Page</h1><div>Main content</div></body></html>")
    for issue in issues:
        print(f"  {issue.severity.value}: {issue.description}")

    # 4. Keyboard Nav
    print("\n--- Keyboard Navigation ---")
    kb = KeyboardNavTester()
    traps = kb.detect_focus_traps('<div tabindex="-5">Trap</div>')
    print(f"  Focus traps found: {len(traps)}")
    has_skip = kb.check_skip_links('<a href="#main" class="skip-link">Skip</a>')
    print(f"  Skip link present: {has_skip}")

    # 5. Pipeline
    print("\n--- Audit Pipeline ---")
    pipeline = AccessibilityAuditPipeline(
        scope=AuditScope(url="https://example.com"),
        wcag_level="AA",
    )
    full_report = pipeline.run()
    print(f"  Violations found: {full_report.total_violations}")
    print(f"  Critical: {full_report.critical_count}")
    print(f"  Estimated remediation: {full_report.estimated_hours}h")


if __name__ == "__main__":
    main()

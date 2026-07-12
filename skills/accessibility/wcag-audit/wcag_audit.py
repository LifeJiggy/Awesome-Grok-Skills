"""
WCAG Audit Module — Automated accessibility compliance testing against WCAG 2.0/2.1/2.2.
Provides violation detection, severity scoring, reporting, and CI/CD integration.
"""

from __future__ import annotations

import json
import re
import sys
import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Protocol, Sequence, Tuple, Union
from urllib.parse import urlparse, urljoin


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Severity(Enum):
    """Violation severity levels aligned with axe-core conventions."""
    CRITICAL = "critical"
    SERIOUS = "serious"
    MODERATE = "moderate"
    MINOR = "minor"
    BEST_PRACTICE = "best_practice"


class ConformanceLevel(Enum):
    """WCAG conformance levels."""
    A = "A"
    AA = "AA"
    AAA = "AAA"


class Principle(Enum):
    """WCAG four principles."""
    PERCEIVABLE = "perceivable"
    OPERABLE = "operable"
    UNDERSTANDABLE = "understandable"
    ROBUST = "robust"


class GateResult(Enum):
    """CI/CD gate outcome."""
    PASS = "pass"
    FAIL = "fail"
    WARN = "warn"


class RuleStatus(Enum):
    """Rule evaluation status."""
    VIOLATION = "violation"
    PASS = "pass"
    INCOMPLETE = "incomplete"
    INAPPLICABLE = "inapplicable"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class AuditConfig:
    """Configuration for a WCAG audit run."""
    url: str
    conformance_level: ConformanceLevel = ConformanceLevel.AA
    wcag_version: str = "2.1"
    include_screenshots: bool = False
    custom_rules_path: Optional[str] = None
    excluded_paths: List[str] = field(default_factory=list)
    viewport_width: int = 1440
    viewport_height: int = 900
    wait_for_load: float = 3.0
    max_pages: int = 50
    follow_links: bool = True
    user_agent: str = "WCAGAuditBot/2.0"
    timeout: int = 30
    max_depth: int = 3
    include_best_practices: bool = True
    tags_filter: List[str] = field(default_factory=list)
    locale: str = "en"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "conformance_level": self.conformance_level.value,
            "wcag_version": self.wcag_version,
            "include_screenshots": self.include_screenshots,
            "custom_rules_path": self.custom_rules_path,
            "excluded_paths": self.excluded_paths,
            "viewport": {"width": self.viewport_width, "height": self.viewport_height},
            "wait_for_load": self.wait_for_load,
            "max_pages": self.max_pages,
            "follow_links": self.follow_links,
        }


@dataclass
class Violation:
    """A single accessibility violation instance."""
    rule_id: str
    rule_name: str
    description: str
    help_url: str
    severity: Severity
    principle: Principle
    wcag_criteria: List[str]
    impact: str
    html_snippet: str
    selector: str
    target_url: str
    fix_suggestion: str
    confidence: float = 1.0
    screenshot_path: Optional[str] = None
    line_number: Optional[int] = None
    column_number: Optional[int] = None
    tags: List[str] = field(default_factory=list)

    @property
    def fingerprint(self) -> str:
        raw = f"{self.rule_id}:{self.selector}:{self.target_url}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


@dataclass
class PageResult:
    """Audit result for a single page."""
    url: str
    title: str
    load_time_ms: float
    violations: List[Violation] = field(default_factory=list)
    passes: int = 0
    incomplete: int = 0
    inapplicable: int = 0
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    @property
    def total_violations(self) -> int:
        return len(self.violations)

    def by_severity(self) -> Dict[Severity, int]:
        counts: Dict[Severity, int] = {s: 0 for s in Severity}
        for v in self.violations:
            counts[v.severity] += 1
        return counts


@dataclass
class AuditResults:
    """Aggregated results across all audited pages."""
    config: AuditConfig
    pages: List[PageResult] = field(default_factory=list)
    start_time: str = ""
    end_time: str = ""
    duration_seconds: float = 0.0

    @property
    def total_violations(self) -> int:
        return sum(p.total_violations for p in self.pages)

    @property
    def total_pages(self) -> int:
        return len(self.pages)

    def by_severity(self) -> Dict[Severity, int]:
        counts: Dict[Severity, int] = {s: 0 for s in Severity}
        for page in self.pages:
            for v in page.violations:
                counts[v.severity] += 1
        return counts

    def by_principle(self) -> Dict[Principle, int]:
        counts: Dict[Principle, int] = {p: 0 for p in Principle}
        for page in self.pages:
            for v in page.violations:
                counts[v.principle] += 1
        return counts

    @property
    def compliance_score(self) -> float:
        total_checks = sum(
            p.passes + p.total_violations + p.incomplete for p in self.pages
        )
        if total_checks == 0:
            return 100.0
        passed = sum(p.passes for p in self.pages)
        return round((passed / total_checks) * 100, 2)

    @property
    def unique_violations(self) -> int:
        fingerprints = set()
        for page in self.pages:
            for v in page.violations:
                fingerprints.add(v.fingerprint)
        return len(fingerprints)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "config": self.config.to_dict(),
            "summary": {
                "total_pages": self.total_pages,
                "total_violations": self.total_violations,
                "unique_violations": self.unique_violations,
                "compliance_score": self.compliance_score,
                "by_severity": {s.value: c for s, c in self.by_severity().items()},
                "by_principle": {p.value: c for p, c in self.by_principle().items()},
            },
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration_seconds": self.duration_seconds,
        }


@dataclass
class BaselineComparison:
    """Delta between current and baseline audit results."""
    regressions: int = 0
    fixes: int = 0
    unchanged: int = 0
    new_violations: List[str] = field(default_factory=list)
    resolved_violations: List[str] = field(default_factory=list)
    score_delta: float = 0.0

    @property
    def is_improvement(self) -> bool:
        return self.fixes > self.regressions


@dataclass
class GatePolicy:
    """CI/CD gate policy thresholds."""
    max_critical: int = 0
    max_serious: int = 10
    max_moderate: int = 50
    max_minor: int = 100
    fail_on_regression: bool = True
    baseline_file: Optional[str] = None
    min_compliance_score: float = 80.0
    fail_on_any_a_violation: bool = False


# ---------------------------------------------------------------------------
# Rule definition
# ---------------------------------------------------------------------------

@dataclass
class AuditRule:
    """Definition of a single WCAG audit rule."""
    rule_id: str
    name: str
    description: str
    help_url: str
    severity: Severity
    principle: Principle
    wcag_criteria: List[str]
    tags: List[str] = field(default_factory=list)
    enabled: bool = True

    def applies_to(self, level: ConformanceLevel) -> bool:
        if self.severity == Severity.BEST_PRACTICE:
            return True
        level_order = {ConformanceLevel.A: 1, ConformanceLevel.AA: 2, ConformanceLevel.AAA: 3}
        criterion_level = self._criterion_level()
        return level_order.get(level, 2) >= level_order.get(criterion_level, 1)

    def _criterion_level(self) -> ConformanceLevel:
        """Infer conformance level from wcag criteria strings like '1.1.1'."""
        for crit in self.wcag_criteria:
            parts = crit.split(".")
            if len(parts) >= 3:
                try:
                    sc_num = int(parts[2])
                    if sc_num % 3 == 1:
                        return ConformanceLevel.A
                    elif sc_num % 3 == 2:
                        return ConformanceLevel.AA
                    else:
                        return ConformanceLevel.AAA
                except ValueError:
                    pass
        return ConformanceLevel.AA


# ---------------------------------------------------------------------------
# Core auditor
# ---------------------------------------------------------------------------

class WCAGAuditor:
    """
    Main WCAG audit engine. Orchestrates page crawling, rule evaluation,
    result aggregation, and report generation.
    """

    BUILTIN_RULES: List[AuditRule] = [
        AuditRule(
            rule_id="color-contrast",
            name="Color Contrast",
            description="Ensures foreground and background colors have sufficient contrast ratio",
            help_url="https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum",
            severity=Severity.SERIOUS,
            principle=Principle.PERCEIVABLE,
            wcag_criteria=["1.4.3"],
            tags=["cat.color"],
        ),
        AuditRule(
            rule_id="image-alt",
            name="Image Alt Text",
            description="Ensures <img> elements have alt text or are marked as decorative",
            help_url="https://www.w3.org/WAI/WCAG21/Understanding/non-text-content",
            severity=Severity.CRITICAL,
            principle=Principle.PERCEIVABLE,
            wcag_criteria=["1.1.1"],
            tags=["cat.text-alternatives"],
        ),
        AuditRule(
            rule_id="label",
            name="Form Labels",
            description="Ensures form elements have associated labels",
            help_url="https://www.w3.org/WAI/WCAG21/Understanding/name-role-value",
            severity=Severity.CRITICAL,
            principle=Principle.PERCEIVABLE,
            wcag_criteria=["1.3.1", "4.1.2"],
            tags=["cat.forms"],
        ),
        AuditRule(
            rule_id="keyboard",
            name="Keyboard Accessible",
            description="Ensures all interactive elements are keyboard accessible",
            help_url="https://www.w3.org/WAI/WCAG21/Understanding/keyboard",
            severity=Severity.CRITICAL,
            principle=Principle.OPERABLE,
            wcag_criteria=["2.1.1"],
            tags=["cat.keyboard"],
        ),
        AuditRule(
            rule_id="focus-order",
            name="Focus Order",
            description="Ensures focusable elements receive focus in a meaningful order",
            help_url="https://www.w3.org/WAI/WCAG21/Understanding/focus-order",
            severity=Severity.SERIOUS,
            principle=Principle.OPERABLE,
            wcag_criteria=["2.4.3"],
            tags=["cat.keyboard"],
        ),
        AuditRule(
            rule_id="aria-roles",
            name="ARIA Roles",
            description="Ensures all ARIA roles are valid and used correctly",
            help_url="https://www.w3.org/WAI/WCAG21/Understanding/name-role-value",
            severity=Severity.SERIOUS,
            principle=Principle.ROBUST,
            wcag_criteria=["4.1.2"],
            tags=["cat.aria"],
        ),
        AuditRule(
            rule_id="link-name",
            name="Link Name",
            description="Ensures links have discernible text",
            help_url="https://www.w3.org/WAI/WCAG21/Understanding/link-purpose-in-context",
            severity=Severity.SERIOUS,
            principle=Principle.OPERABLE,
            wcag_criteria=["2.4.4"],
            tags=["cat.name-role-value"],
        ),
        AuditRule(
            rule_id="document-title",
            name="Document Title",
            description="Ensures each HTML document has a descriptive title",
            help_url="https://www.w3.org/WAI/WCAG21/Understanding/page-titled",
            severity=Severity.MODERATE,
            principle=Principle.OPERABLE,
            wcag_criteria=["2.4.2"],
            tags=["cat.language"],
        ),
        AuditRule(
            rule_id="html-has-lang",
            name="HTML Lang Attribute",
            description="Ensures every HTML element has a lang attribute",
            help_url="https://www.w3.org/WAI/WCAG21/Understanding/language-of-page",
            severity=Severity.SERIOUS,
            principle=Principle.UNDERSTANDABLE,
            wcag_criteria=["3.1.1"],
            tags=["cat.language"],
        ),
        AuditRule(
            rule_id="tabindex",
            name="Tabindex",
            description="Ensures tabindex values are not greater than zero",
            help_url="https://www.w3.org/WAI/WCAG21/Understanding/focus-order",
            severity=Severity.MODERATE,
            principle=Principle.OPERABLE,
            wcag_criteria=["2.4.3"],
            tags=["cat.keyboard"],
        ),
        AuditRule(
            rule_id="viewport-meta",
            name="Viewport Meta",
            description="Ensures viewport prevents zooming disabled",
            help_url="https://www.w3.org/WAI/WCAG21/Understanding/resize-text",
            severity=Severity.SERIOUS,
            principle=Principle.RENDERABLE,
            wcag_criteria=["1.4.4"],
            tags=["cat.viewport"],
        ),
        AuditRule(
            rule_id="heading-order",
            name="Heading Order",
            description="Ensures headings are in sequential order",
            help_url="https://www.w3.org/WAI/WCAG21/Understanding/info-and-relationships",
            severity=Severity.MODERATE,
            principle=Principle.PERCEIVABLE,
            wcag_criteria=["1.3.1"],
            tags=["cat.semantics"],
        ),
    ]

    def __init__(self, config: AuditConfig):
        self.config = config
        self._rules: List[AuditRule] = list(self.BUILTIN_RULES)
        self._custom_checks: List[Callable] = []
        self._visited_urls: set = set()

        if config.custom_rules_path:
            self._load_custom_rules(config.custom_rules_path)

    def _load_custom_rules(self, path: str) -> None:
        """Load custom rule definitions from a JSON file."""
        rule_file = Path(path)
        if rule_file.exists():
            with open(rule_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            for rule_def in data.get("rules", []):
                rule = AuditRule(
                    rule_id=rule_def["id"],
                    name=rule_def["name"],
                    description=rule_def.get("description", ""),
                    help_url=rule_def.get("help_url", ""),
                    severity=Severity(rule_def.get("severity", "moderate")),
                    principle=Principle(rule_def.get("principle", "robust")),
                    wcag_criteria=rule_def.get("wcag_criteria", []),
                    tags=rule_def.get("tags", []),
                )
                self._rules.append(rule)

    def add_custom_check(self, check_fn: Callable) -> None:
        """Register a custom validation function."""
        self._custom_checks.append(check_fn)

    def get_applicable_rules(self) -> List[AuditRule]:
        """Return rules that apply to the configured conformance level."""
        return [r for r in self._rules if r.enabled and r.applies_to(self.config.conformance_level)]

    def run(self) -> AuditResults:
        """Execute the full audit pipeline."""
        start = datetime.now(timezone.utc)
        results = AuditResults(config=self.config, start_time=start.isoformat())

        pages_to_audit = self._discover_pages(self.config.url)
        for page_url in pages_to_audit:
            page_result = self._audit_page(page_url)
            results.pages.append(page_result)

        end = datetime.now(timezone.utc)
        results.end_time = end.isoformat()
        results.duration_seconds = (end - start).total_seconds()
        return results

    def _discover_pages(self, base_url: str) -> List[str]:
        """Discover pages to audit starting from the base URL."""
        pages = [base_url]
        if self.config.follow_links:
            parsed = urlparse(base_url)
            base_domain = parsed.netloc
            for excluded in self.config.excluded_paths:
                if excluded in base_url:
                    return [base_url]
        return pages[: self.config.max_pages]

    def _audit_page(self, url: str) -> PageResult:
        """Run all applicable rules against a single page."""
        page = PageResult(url=url, title="", load_time_ms=0.0)

        applicable_rules = self.get_applicable_rules()
        for rule in applicable_rules:
            violations = self._evaluate_rule(rule, url)
            page.violations.extend(violations)

        for check in self._custom_checks:
            try:
                custom_violations = check(url)
                if isinstance(custom_violations, list):
                    page.violations.extend(custom_violations)
            except Exception as exc:
                print(f"Custom check error on {url}: {exc}", file=sys.stderr)

        return page

    def _evaluate_rule(self, rule: AuditRule, url: str) -> List[Violation]:
        """Evaluate a single rule against a page. In production this invokes axe-core or similar."""
        violations: List[Violation] = []
        violation = Violation(
            rule_id=rule.rule_id,
            rule_name=rule.name,
            description=rule.description,
            help_url=rule.help_url,
            severity=rule.severity,
            principle=rule.principle,
            wcag_criteria=rule.wcag_criteria,
            impact=rule.severity.value,
            html_snippet="",
            selector="",
            target_url=url,
            fix_suggestion=self._get_fix_suggestion(rule.rule_id),
            tags=rule.tags,
        )
        violations.append(violation)
        return violations

    @staticmethod
    def _get_fix_suggestion(rule_id: str) -> str:
        suggestions = {
            "color-contrast": "Increase contrast ratio to at least 4.5:1 for normal text and 3:1 for large text",
            "image-alt": "Add descriptive alt text to <img> elements or use alt='' for decorative images",
            "label": "Associate form inputs with <label> elements using for/id or aria-labelledby",
            "keyboard": "Ensure all interactive elements are reachable and operable via keyboard",
            "focus-order": "Remove positive tabindex values and ensure DOM order matches visual order",
            "aria-roles": "Use valid ARIA landmark and widget roles matching the element purpose",
            "link-name": "Add visible text content or aria-label to links",
            "document-title": "Add a descriptive <title> element to each page",
            "html-has-lang": "Add lang attribute to the <html> element matching page content language",
            "tabindex": "Avoid tabindex > 0; use 0 or -1 instead",
        }
        return suggestions.get(rule_id, "Review WCAG documentation for remediation guidance")

    def export_html_report(self, results: AuditResults, output_path: str) -> None:
        """Generate an HTML compliance report."""
        severity_counts = results.by_severity()
        html = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><title>WCAG Audit Report</title>
<style>
body {{ font-family: -apple-system, sans-serif; margin: 2rem; }}
.summary {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 1rem; margin: 1rem 0; }}
.card {{ padding: 1rem; border-radius: 8px; text-align: center; }}
.critical {{ background: #fee2e2; color: #991b1b; }}
.serious {{ background: #fef3c7; color: #92400e; }}
.moderate {{ background: #dbeafe; color: #1e40af; }}
.minor {{ background: #e0e7ff; color: #3730a3; }}
table {{ width: 100%; border-collapse: collapse; margin-top: 1rem; }}
th, td {{ padding: 0.75rem; border: 1px solid #e5e7eb; text-align: left; }}
th {{ background: #f9fafb; font-weight: 600; }}
</style></head>
<body>
<h1>WCAG {results.config.wcag_version} Conformance Report</h1>
<p>Conformance Level: <strong>{results.config.conformance_level.value}</strong></p>
<p>Pages Audited: {results.total_pages} | Total Violations: {results.total_violations} |
   Compliance Score: {results.compliance_score}%</p>
<div class="summary">
  <div class="card critical"><h3>{severity_counts[Severity.CRITICAL]}</h3><p>Critical</p></div>
  <div class="card serious"><h3>{severity_counts[Severity.SERIOUS]}</h3><p>Serious</p></div>
  <div class="card moderate"><h3>{severity_counts[Severity.MODERATE]}</h3><p>Moderate</p></div>
  <div class="card minor"><h3>{severity_counts[Severity.MINOR]}</h3><p>Minor</p></div>
</div>
<table><tr><th>Rule</th><th>Severity</th><th>Criteria</th><th>Page</th><th>Suggestion</th></tr>"""
        for page in results.pages:
            for v in page.violations:
                html += f"""<tr><td>{v.rule_name}</td><td>{v.severity.value}</td>
<td>{', '.join(v.wcag_criteria)}</td><td>{v.target_url}</td>
<td>{v.fix_suggestion}</td></tr>"""
        html += "</table></body></html>"
        Path(output_path).write_text(html, encoding="utf-8")

    def export_json(self, results: AuditResults, output_path: str) -> None:
        """Export results as structured JSON."""
        data = results.to_dict()
        all_violations = []
        for page in results.pages:
            for v in page.violations:
                all_violations.append({
                    "rule_id": v.rule_id,
                    "rule_name": v.rule_name,
                    "severity": v.severity.value,
                    "principle": v.principle.value,
                    "wcag_criteria": v.wcag_criteria,
                    "target_url": v.target_url,
                    "fix_suggestion": v.fix_suggestion,
                    "fingerprint": v.fingerprint,
                })
        data["violations"] = all_violations
        Path(output_path).write_text(json.dumps(data, indent=2), encoding="utf-8")

    def export_junit_xml(self, results: AuditResults, output_path: str) -> None:
        """Export results as JUnit XML for CI integration."""
        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append(f'<testsuite name="wcag-audit" tests="{results.total_pages}" '
                     f'failures="{results.total_violations}">')
        for page in results.pages:
            lines.append(f'  <testcase name="{page.url}" classname="wcag-audit">')
            for v in page.violations:
                lines.append(f'    <failure message="{v.rule_name}" type="{v.severity.value}">')
                lines.append(f'      {v.description}')
                lines.append(f'      WCAG: {", ".join(v.wcag_criteria)}')
                lines.append(f'      Fix: {v.fix_suggestion}')
                lines.append(f'    </failure>')
            lines.append("  </testcase>")
        lines.append("</testsuite>")
        Path(output_path).write_text("\n".join(lines), encoding="utf-8")

    def save_baseline(self, results: AuditResults, path: str) -> None:
        """Persist current results as a baseline for future comparisons."""
        fingerprints = set()
        for page in results.pages:
            for v in page.violations:
                fingerprints.add(v.fingerprint)
        baseline = {
            "timestamp": results.end_time,
            "compliance_score": results.compliance_score,
            "total_violations": results.total_violations,
            "fingerprints": sorted(fingerprints),
        }
        Path(path).write_text(json.dumps(baseline, indent=2), encoding="utf-8")

    def load_baseline(self, path: str) -> Dict[str, Any]:
        """Load a previously saved baseline."""
        return json.loads(Path(path).read_text(encoding="utf-8"))

    def compare(self, current: AuditResults, baseline: Dict[str, Any]) -> BaselineComparison:
        """Compare current results against a saved baseline."""
        current_fps = set()
        for page in current.pages:
            for v in page.violations:
                current_fps.add(v.fingerprint)

        baseline_fps = set(baseline.get("fingerprints", []))
        new_violations = sorted(current_fps - baseline_fps)
        resolved = sorted(baseline_fps - current_fps)

        return BaselineComparison(
            regressions=len(new_violations),
            fixes=len(resolved),
            unchanged=len(current_fps & baseline_fps),
            new_violations=new_violations,
            resolved_violations=resolved,
            score_delta=round(
                current.compliance_score - baseline.get("compliance_score", 100), 2
            ),
        )


# ---------------------------------------------------------------------------
# CI/CD Integration
# ---------------------------------------------------------------------------

class CIIntegration:
    """Evaluates audit results against a gate policy for CI/CD pipelines."""

    def __init__(self, auditor: WCAGAuditor, policy: GatePolicy):
        self.auditor = auditor
        self.policy = policy

    def evaluate(self, url: str) -> Tuple[GateResult, AuditResults]:
        """Run audit and evaluate against gate policy. Returns (result, results)."""
        self.auditor.config.url = url
        results = self.auditor.run()
        result = self._check_policy(results)
        return result, results

    def _check_policy(self, results: AuditResults) -> GateResult:
        severity = results.by_severity()
        if severity[Severity.CRITICAL] > self.policy.max_critical:
            return GateResult.FAIL
        if severity[Severity.SERIOUS] > self.policy.max_serious:
            return GateResult.FAIL
        if severity[Severity.MODERATE] > self.policy.max_moderate:
            return GateResult.FAIL
        if severity[Severity.MINOR] > self.policy.max_minor:
            return GateResult.FAIL
        if results.compliance_score < self.policy.min_compliance_score:
            return GateResult.FAIL
        if self.policy.fail_on_regression and self.policy.baseline_file:
            baseline_path = Path(self.policy.baseline_file)
            if baseline_path.exists():
                baseline = self.auditor.load_baseline(str(baseline_path))
                delta = self.auditor.compare(results, baseline)
                if delta.regressions > 0:
                    return GateResult.FAIL
        return GateResult.PASS


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the WCAG auditor with a sample configuration."""
    config = AuditConfig(
        url="https://example.com",
        conformance_level=ConformanceLevel.AA,
        wcag_version="2.1",
        include_screenshots=False,
        max_pages=5,
    )

    auditor = WCAGAuditor(config)
    print(f"Loaded {len(auditor.get_applicable_rules())} applicable rules")
    print(f"Conformance level: {config.conformance_level.value}")

    results = auditor.run()
    print(f"\nAudit completed in {results.duration_seconds:.2f}s")
    print(f"Pages audited: {results.total_pages}")
    print(f"Total violations: {results.total_violations}")
    print(f"Compliance score: {results.compliance_score}%")

    severity = results.by_severity()
    for sev in Severity:
        count = severity.get(sev, 0)
        if count > 0:
            print(f"  {sev.value}: {count}")

    principle = results.by_principle()
    for princ in Principle:
        count = principle.get(princ, 0)
        if count > 0:
            print(f"  {princ.value}: {count}")

    # Export reports
    auditor.export_html_report(results, "audit_report.html")
    auditor.export_json(results, "audit_results.json")
    auditor.export_junit_xml(results, "audit_junit.xml")
    auditor.save_baseline(results, "baseline.json")

    print("\nReports generated: audit_report.html, audit_results.json, audit_junit.xml")

    # Demo CI gate
    gate_policy = GatePolicy(max_critical=0, max_serious=5, min_compliance_score=85.0)
    ci = CIIntegration(auditor, gate_policy)
    gate_result, _ = ci.evaluate("https://example.com")
    print(f"CI Gate: {gate_result.value}")


if __name__ == "__main__":
    main()

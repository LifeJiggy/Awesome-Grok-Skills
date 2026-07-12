"""
Accessibility Evaluation Engine

WCAG 2.2 compliance evaluation, assistive technology testing,
color contrast analysis, screen reader compatibility, cognitive
accessibility assessment, and automated scanning integration.
Part of the ux-research skill domain.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import math
import re


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class ConformanceLevel(Enum):
    A = "A"
    AA = "AA"
    AAA = "AAA"


class Principle(Enum):
    PERCEIVABLE = "Perceivable"
    OPERABLE = "Operable"
    UNDERSTANDABLE = "Understandable"
    ROBUST = "Robust"


class CriterionStatus(Enum):
    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "not_applicable"
    NOT_TESTED = "not_tested"


class Severity(Enum):
    CRITICAL = "critical"
    SERIOUS = "serious"
    MODERATE = "moderate"
    MINOR = "minor"


class TextSize(Enum):
    NORMAL = "normal"      # < 18pt or < 14pt bold
    LARGE = "large"        # >= 18pt or >= 14pt bold


class SRPlatform(Enum):
    NVDA = "NVDA"
    JAWS = "JAWS"
    VOICEOVER_MAC = "VoiceOver macOS"
    VOICEOVER_IOS = "VoiceOver iOS"
    TALKBACK = "TalkBack"


class ReadingLevel(Enum):
    ELEMENTARY = "elementary"
    MIDDLE_SCHOOL = "middle_school"
    HIGH_SCHOOL = "high_school"
    COLLEGE = "college"
    GRADUATE = "graduate"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Config:
    name: str
    enabled: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CriterionResult:
    criterion_id: str
    description: str
    principle: Principle
    status: CriterionStatus
    severity: Severity = Severity.MODERATE
    notes: str = ""
    affected_elements: int = 0
    wcag_version: str = "2.2"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class ContrastResult:
    foreground: str
    background: str
    ratio: float
    aa_normal: bool
    aa_large: bool
    aaa_normal: bool
    aaa_large: bool
    apca_lca: Optional[float] = None


@dataclass
class ContrastSuggestion:
    color: str
    ratio: float
    passes_target: bool


@dataclass
class ScreenReaderStep:
    action: str
    expected: str
    actual: str
    status: str  # "pass" or "fail"
    platform: SRPlatform = SRPlatform.NVDA
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class KnownLimitation:
    title: str
    description: str
    workaround: str
    wcag_criteria: List[str] = field(default_factory=list)
    date_identified: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))


@dataclass
class TestingMethod:
    method: str
    tools: List[str] = field(default_factory=list)
    date_performed: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))


@dataclass
class ScanViolation:
    rule_id: str
    description: str
    severity: Severity
    wcag_criteria: List[str]
    element_count: int = 0
    impact: str = ""


@dataclass
class CognitiveAssessment:
    page_name: str
    flesch_kincaid_grade: float
    gunning_fog_index: float
    reading_level: ReadingLevel
    plain_language_score: float  # 0-100
    consistent_navigation: bool
    timeout_adequate: bool
    error_prevention: bool
    suggestions: List[str] = field(default_factory=list)


@dataclass
class VPATEntry:
    criterion_id: str
    description: str
    conformance_level: ConformanceLevel
    remarks: str
    date_tested: str = field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d"))


@dataclass
class Report:
    conformance_status: str
    passed: int
    failed: int
    partial: int
    not_applicable: int
    score: float
    criteria: List[CriterionResult] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _relative_luminance(r: int, g: int, b: int) -> float:
    def linearize(c: int) -> float:
        srgb = c / 255.0
        return srgb / 12.92 if srgb <= 0.04045 else ((srgb + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)


def _contrast_ratio(fg: str, bg: str) -> float:
    r1, g1, b1 = _hex_to_rgb(fg)
    r2, g2, b2 = _hex_to_rgb(bg)
    l1 = _relative_luminance(r1, g1, b1)
    l2 = _relative_luminance(r2, g2, b2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def _flesch_kincaid_grade(words: List[str], sentences: int) -> float:
    syllables = sum(_count_syllables(w) for w in words)
    wc = len(words)
    if sentences == 0 or wc == 0:
        return 0.0
    return 0.39 * (wc / sentences) + 11.8 * (syllables / wc) - 15.59


def _gunning_fog(words: List[str], sentences: int) -> float:
    complex_words = sum(1 for w in words if _count_syllables(w) >= 3)
    wc = len(words)
    if sentences == 0 or wc == 0:
        return 0.0
    return 0.4 * ((wc / sentences) + 100 * (complex_words / wc))


def _count_syllables(word: str) -> int:
    word = word.lower().strip()
    if len(word) <= 2:
        return 1
    vowels = "aeiouy"
    count = 0
    prev_vowel = False
    for ch in word:
        is_vowel = ch in vowels
        if is_vowel and not prev_vowel:
            count += 1
        prev_vowel = is_vowel
    if word.endswith("e") and count > 1:
        count -= 1
    return max(count, 1)


def _reading_level_from_grade(grade: float) -> ReadingLevel:
    if grade <= 5:
        return ReadingLevel.ELEMENTARY
    elif grade <= 8:
        return ReadingLevel.MIDDLE_SCHOOL
    elif grade <= 12:
        return ReadingLevel.HIGH_SCHOOL
    elif grade <= 16:
        return ReadingLevel.COLLEGE
    return ReadingLevel.GRADUATE


# ---------------------------------------------------------------------------
# WCAG Evaluator
# ---------------------------------------------------------------------------

class WCAGEvaluator:
    """Evaluate WCAG 2.2 success criteria and produce conformance reports."""

    def __init__(self, level: ConformanceLevel = ConformanceLevel.AA):
        self.level = level
        self.results: List[CriterionResult] = []

    def evaluate_criterion(
        self,
        criterion_id: str,
        description: str,
        principle: Principle,
        status: CriterionStatus,
        severity: Severity = Severity.MODERATE,
        notes: str = "",
        affected_elements: int = 0,
    ) -> CriterionResult:
        result = CriterionResult(
            criterion_id=criterion_id,
            description=description,
            principle=principle,
            status=status,
            severity=severity,
            notes=notes,
            affected_elements=affected_elements,
        )
        self.results.append(result)
        return result

    def report(self) -> Report:
        passed = sum(1 for r in self.results if r.status == CriterionStatus.PASS)
        failed = sum(1 for r in self.results if r.status == CriterionStatus.FAIL)
        partial = sum(1 for r in self.results if r.status == CriterionStatus.NOT_TESTED)
        na = sum(1 for r in self.results if r.status == CriterionStatus.NOT_APPLICABLE)
        total_tested = passed + failed
        score = passed / total_tested if total_tested > 0 else 0.0
        conformance = "PASS" if failed == 0 and passed > 0 else "FAIL"
        return Report(
            conformance_status=conformance,
            passed=passed,
            failed=failed,
            partial=partial,
            not_applicable=na,
            score=score,
            criteria=self.results,
        )

    def failures_by_principle(self) -> Dict[str, List[CriterionResult]]:
        groups: Dict[str, List[CriterionResult]] = {}
        for r in self.results:
            if r.status == CriterionStatus.FAIL:
                key = r.principle.value
                groups.setdefault(key, []).append(r)
        return groups

    def critical_failures(self) -> List[CriterionResult]:
        return [
            r for r in self.results
            if r.status == CriterionStatus.FAIL and r.severity == Severity.CRITICAL
        ]


# ---------------------------------------------------------------------------
# Contrast Analyzer
# ---------------------------------------------------------------------------

class ContrastAnalyzer:
    """WCAG contrast ratio calculations with remediation suggestions."""

    def check(
        self,
        foreground: str,
        background: str,
        text_size: TextSize = TextSize.NORMAL,
    ) -> ContrastResult:
        ratio = _contrast_ratio(foreground, background)
        aa_large = ratio >= 3.0
        aaa_large = ratio >= 4.5
        aa_normal = ratio >= 4.5
        aaa_normal = ratio >= 7.0
        return ContrastResult(
            foreground=foreground,
            background=background,
            ratio=round(ratio, 2),
            aa_normal=aa_normal,
            aa_large=aa_large,
            aaa_normal=aaa_normal,
            aaa_large=aaa_large,
        )

    def suggest_fixes(
        self,
        foreground: str,
        background: str,
        target_ratio: float = 4.5,
        fix: str = "foreground",
        max_suggestions: int = 5,
    ) -> List[ContrastSuggestion]:
        r, g, b = _hex_to_rgb(foreground if fix == "foreground" else background)
        suggestions: List[ContrastSuggestion] = []
        for step in range(1, 256):
            for direction in (-1, 1):
                nr = max(0, min(255, r + direction * step))
                ng = max(0, min(255, g + direction * step))
                nb = max(0, min(255, b + direction * step))
                new_hex = f"#{nr:02x}{ng:02x}{nb:02x}"
                fg_use = new_hex if fix == "foreground" else foreground
                bg_use = new_hex if fix == "background" else background
                ratio = _contrast_ratio(fg_use, bg_use)
                if ratio >= target_ratio:
                    suggestions.append(ContrastSuggestion(
                        color=new_hex, ratio=round(ratio, 2), passes_target=True,
                    ))
                    if len(suggestions) >= max_suggestions:
                        return suggestions
        return suggestions

    def batch_check(self, pairs: List[Tuple[str, str]]) -> List[ContrastResult]:
        return [self.check(fg, bg) for fg, bg in pairs]


# ---------------------------------------------------------------------------
# Screen Reader Test
# ---------------------------------------------------------------------------

class ScreenReaderTest:
    """Structured screen reader testing protocol and result summarization."""

    def __init__(self, page_name: str, platform: SRPlatform = SRPlatform.NVDA, browser: str = "Firefox"):
        self.page_name = page_name
        self.platform = platform
        self.browser = browser
        self.steps: List[ScreenReaderStep] = []

    def add_step(self, action: str, expected: str, actual: str, status: str) -> ScreenReaderStep:
        step = ScreenReaderStep(
            action=action, expected=expected, actual=actual,
            status=status, platform=self.platform,
        )
        self.steps.append(step)
        return step

    def summarize(self) -> Dict[str, Any]:
        passed = sum(1 for s in self.steps if s.status == "pass")
        failed = sum(1 for s in self.steps if s.status == "fail")
        total = len(self.steps)
        return {
            "page": self.page_name,
            "platform": self.platform.value,
            "browser": self.browser,
            "total": total,
            "pass": passed,
            "fail": failed,
            "pass_rate": f"{passed / total:.1%}" if total else "N/A",
            "failed_steps": [
                {"action": s.action, "expected": s.expected, "actual": s.actual}
                for s in self.steps if s.status == "fail"
            ],
        }


# ---------------------------------------------------------------------------
# Accessibility Statement Generator
# ---------------------------------------------------------------------------

class AccessibilityStatement:
    """Generate a structured accessibility statement for an organization."""

    def __init__(
        self,
        organization: str,
        website: str,
        conformance_level: ConformanceLevel = ConformanceLevel.AA,
        last_updated: str = "",
        contact_email: str = "",
        contact_phone: str = "",
    ):
        self.organization = organization
        self.website = website
        self.conformance_level = conformance_level
        self.last_updated = last_updated or datetime.now().strftime("%Y-%m-%d")
        self.contact_email = contact_email
        self.contact_phone = contact_phone
        self.known_limitations: List[KnownLimitation] = []
        self.testing_methods: List[TestingMethod] = []

    def add_known_limitation(self, title: str, description: str, workaround: str, wcag_criteria: Optional[List[str]] = None) -> None:
        self.known_limitations.append(KnownLimitation(
            title=title, description=description,
            workaround=workaround, wcag_criteria=wcag_criteria or [],
        ))

    def add_testing_method(self, method: str, tools: Optional[List[str]] = None) -> None:
        self.testing_methods.append(TestingMethod(method=method, tools=tools or []))

    def render(self) -> str:
        lines = [
            f"# Accessibility Statement — {self.organization}",
            "",
            f"**Website:** {self.website}",
            f"**Conformance target:** WCAG 2.2 Level {self.conformance_level.value}",
            f"**Last updated:** {self.last_updated}",
            "",
            "## Our Commitment",
            "",
            f"{self.organization} is committed to ensuring digital accessibility for all users.",
            "We continually work to improve the accessibility of our website and applications.",
            "",
            "## Standards",
            "",
            f"We aim to conform to WCAG 2.2 Level {self.conformance_level.value}.",
            "",
        ]
        if self.testing_methods:
            lines += ["## Testing Methods", ""]
            for tm in self.testing_methods:
                tools_str = ", ".join(tm.tools) if tm.tools else "N/A"
                lines.append(f"- {tm.method} (Tools: {tools_str})")
            lines.append("")
        if self.known_limitations:
            lines += ["## Known Limitations", ""]
            for kl in self.known_limitations:
                criteria = ", ".join(kl.wcag_criteria) if kl.wcag_criteria else "N/A"
                lines += [
                    f"### {kl.title}",
                    f"{kl.description}",
                    f"**Workaround:** {kl.workaround}",
                    f"**Affected WCAG criteria:** {criteria}",
                    f"**Date identified:** {kl.date_identified}",
                    "",
                ]
        lines += [
            "## Feedback",
            "",
            "We welcome your feedback on the accessibility of our website.",
            f"Please contact us at {self.contact_email}" if self.contact_email else "",
            f"or call {self.contact_phone}." if self.contact_phone else "",
            "",
        ]
        return "\n".join(line for line in lines if line is not None)


# ---------------------------------------------------------------------------
# Cognitive Accessibility Assessor
# ---------------------------------------------------------------------------

class CognitiveAccessibilityAssessor:
    """Assess cognitive accessibility: reading level, plain language, navigation."""

    def assess_page(self, page_name: str, text: str, has_timeout: bool = False, timeout_seconds: int = 0, has_error_prevention: bool = True, consistent_nav: bool = True) -> CognitiveAssessment:
        words = text.split()
        sentences = max(text.count(".") + text.count("!") + text.count("?"), 1)
        fk = _flesch_kincaid_grade(words, sentences)
        fog = _gunning_fog(words, sentences)
        level = _reading_level_from_grade(fk)
        plain_score = max(0, min(100, 100 - (fk * 5)))
        timeout_ok = not has_timeout or timeout_seconds >= 20
        suggestions: List[str] = []
        if fk > 8:
            suggestions.append("Simplify language: aim for grade 8 or below")
        if fog > 12:
            suggestions.append("Reduce complex word usage (Gunning Fog is high)")
        if not consistent_nav:
            suggestions.append("Ensure navigation is consistent across pages")
        if not timeout_ok:
            suggestions.append("Allow at least 20 seconds to complete timed interactions")
        if not has_error_prevention:
            suggestions.append("Add error prevention for important user actions")
        return CognitiveAssessment(
            page_name=page_name,
            flesch_kincaid_grade=round(fk, 1),
            gunning_fog_index=round(fog, 1),
            reading_level=level,
            plain_language_score=round(plain_score, 1),
            consistent_navigation=consistent_nav,
            timeout_adequate=timeout_ok,
            error_prevention=has_error_prevention,
            suggestions=suggestions,
        )


# ---------------------------------------------------------------------------
# Automated Scan Integration
# ---------------------------------------------------------------------------

class AutomatedScanner:
    """Integration layer for axe-core, Lighthouse, and Pa11y scan results."""

    def __init__(self) -> None:
        self.violations: List[ScanViolation] = []

    def import_axe_results(self, results: List[Dict[str, Any]]) -> int:
        count = 0
        for item in results:
            severity_map = {"critical": Severity.CRITICAL, "serious": Severity.SERIOUS, "moderate": Severity.MODERATE, "minor": Severity.MINOR}
            self.violations.append(ScanViolation(
                rule_id=item.get("id", "unknown"),
                description=item.get("description", ""),
                severity=severity_map.get(item.get("impact", "moderate"), Severity.MODERATE),
                wcag_criteria=item.get("tags", []),
                element_count=len(item.get("nodes", [])),
                impact=item.get("impact", ""),
            ))
            count += 1
        return count

    def import_lighthouse_results(self, results: Dict[str, Any]) -> int:
        count = 0
        for audit_id, audit in results.get("audits", {}).items():
            if audit.get("score") is not None and audit["score"] < 1.0:
                self.violations.append(ScanViolation(
                    rule_id=audit_id,
                    description=audit.get("title", ""),
                    severity=Severity.MODERATE,
                    wcag_criteria=[],
                    element_count=audit.get("details", {}).get("items", [{}]).__len__(),
                    impact=audit.get("scoreDisplayMode", ""),
                ))
                count += 1
        return count

    def summary(self) -> Dict[str, Any]:
        by_severity: Dict[str, int] = {}
        for v in self.violations:
            by_severity[v.severity.value] = by_severity.get(v.severity.value, 0) + 1
        return {
            "total_violations": len(self.violations),
            "by_severity": by_severity,
            "top_violations": [
                {"rule": v.rule_id, "count": v.element_count, "severity": v.severity.value}
                for v in sorted(self.violations, key=lambda x: x.element_count, reverse=True)[:10]
            ],
        }

    def to_vpat_entries(self) -> List[VPATEntry]:
        entries: List[VPATEntry] = []
        for v in self.violations:
            for crit in v.wcag_criteria:
                entries.append(VPATEntry(
                    criterion_id=crit,
                    description=v.description,
                    conformance_level=ConformanceLevel.AA,
                    remarks=f"Automated scan violation: {v.rule_id} ({v.severity.value})",
                ))
        return entries


# ---------------------------------------------------------------------------
# Accessibility Engine (orchestrator)
# ---------------------------------------------------------------------------

class AccessibilityEngine:
    """Main engine orchestrating all accessibility evaluation components."""

    def __init__(self, config: Optional[Config] = None):
        self.config = config or Config(name="accessibility")
        self.status = Status.INACTIVE
        self.evaluator = WCAGEvaluator()
        self.contrast_analyzer = ContrastAnalyzer()
        self.scanner = AutomatedScanner()
        self.cognitive_assessor = CognitiveAccessibilityAssessor()
        self.results: List[Dict[str, Any]] = []

    def configure(self, **kwargs) -> "AccessibilityEngine":
        self.config.parameters.update(kwargs)
        return self

    def run(self) -> Dict[str, Any]:
        self.status = Status.ACTIVE
        report = self.evaluator.report()
        scan_summary = self.scanner.summary()
        return {
            "status": self.status.value,
            "config": self.config.name,
            "timestamp": datetime.now().isoformat(),
            "conformance": report.conformance_status,
            "score": f"{report.score:.0%}",
            "passed": report.passed,
            "failed": report.failed,
            "scan_violations": scan_summary["total_violations"],
            "results": self.results,
        }

    def validate(self) -> bool:
        return self.config.enabled and bool(self.config.name)

    def get_status(self) -> Dict[str, str]:
        return {
            "engine": "Accessibility",
            "status": self.status.value,
            "config": self.config.name,
        }

    def full_audit(self, text_samples: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        report = self.evaluator.report()
        cognitive = {}
        if text_samples:
            for name, text in text_samples.items():
                cognitive[name] = self.cognitive_assessor.assess_page(name, text)
        return {
            "conformance_report": {
                "status": report.conformance_status,
                "score": report.score,
                "passed": report.passed,
                "failed": report.failed,
            },
            "cognitive_assessments": {
                k: {
                    "grade": v.flesch_kincaid_grade,
                    "reading_level": v.reading_level.value,
                    "plain_language_score": v.plain_language_score,
                    "suggestions": v.suggestions,
                }
                for k, v in cognitive.items()
            },
            "scan_summary": self.scanner.summary(),
        }


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main():
    engine = AccessibilityEngine()
    engine.configure(debug=True, level="AA")

    # WCAG evaluation
    engine.evaluator.evaluate_criterion(
        criterion_id="1.1.1", description="Non-text Content",
        principle=Principle.PERCEIVABLE, status=CriterionStatus.PASS,
        notes="All images have alt text",
    )
    engine.evaluator.evaluate_criterion(
        criterion_id="1.4.3", description="Contrast (Minimum)",
        principle=Principle.PERCEIVABLE, status=CriterionStatus.FAIL,
        severity=Severity.SERIOUS,
        notes="Body text #767676 on white fails 4.5:1", affected_elements=5,
    )
    engine.evaluator.evaluate_criterion(
        criterion_id="2.1.1", description="Keyboard",
        principle=Principle.OPERABLE, status=CriterionStatus.PASS,
        notes="All interactive elements keyboard accessible",
    )
    engine.evaluator.evaluate_criterion(
        criterion_id="2.4.7", description="Focus Visible",
        principle=Principle.OPERABLE, status=CriterionStatus.FAIL,
        severity=Severity.MODERATE, notes="Custom button lacks visible focus ring",
    )

    # Contrast check
    result = engine.contrast_analyzer.check("#767676", "#FFFFFF")
    print(f"Contrast ratio: {result.ratio}:1 — AA normal: {result.aa_normal}, AAA normal: {result.aaa_normal}")

    suggestions = engine.contrast_analyzer.suggest_fixes("#767676", "#FFFFFF", target_ratio=4.5)
    if suggestions:
        print(f"Suggested fix: {suggestions[0].color} (ratio: {suggestions[0].ratio}:1)")

    # Screen reader test
    sr_test = ScreenReaderTest(page_name="Home Page", platform=SRPlatform.NVDA, browser="Firefox")
    sr_test.add_step("Navigate to page", "Page title announced", "Page title announced correctly", "pass")
    sr_test.add_step("Tab to search", "Search input announced", "Search input announced correctly", "pass")
    sr_test.add_step("Submit form", "Error announced", "No error announced for empty required field", "fail")
    sr_results = sr_test.summarize()
    print(f"SR test: {sr_results['pass']} pass, {sr_results['fail']} fail")

    # Cognitive assessment
    sample_text = "Welcome to our platform. We help teams work better together. Sign up to get started with your free account today."
    cognitive = engine.cognitive_assessor.assess_page("Landing Page", sample_text)
    print(f"Reading level: {cognitive.reading_level.value}, FK grade: {cognitive.flesch_kincaid_grade}")

    # Accessibility statement
    statement = AccessibilityStatement(
        organization="Acme Corp", website="acme.com",
        conformance_level=ConformanceLevel.AA, contact_email="accessibility@acme.com",
    )
    statement.add_known_limitation(
        title="Legacy PDFs", description="Some archived PDFs are not fully accessible",
        workaround="Contact us for alternatives", wcag_criteria=["1.1.1"],
    )
    statement.add_testing_method(method="Automated + manual testing", tools=["axe-core", "NVDA"])
    print(statement.render())

    # Engine run
    result = engine.run()
    print(f"\nEngine status: {result['status']}, Conformance: {result['conformance']}, Score: {result['score']}")


if __name__ == "__main__":
    main()

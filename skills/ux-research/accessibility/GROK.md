---
name: "accessibility"
category: "ux-research"
version: "1.0.0"
tags: ["ux-research", "accessibility", "WCAG", "screen-reader", "inclusive-design"]
---

# Accessibility

## Overview

Digital accessibility ensures that products, services, and environments can be used by people with the widest possible range of abilities, including those with visual, auditory, motor, cognitive, and neurological disabilities. Far from being a compliance checkbox, accessibility is a design philosophy that improves usability for everyone—captions help users in noisy environments, keyboard navigation helps power users, and clear language helps non-native speakers. This module provides a comprehensive toolkit for evaluating, testing, and ensuring accessibility across web, mobile, and embedded interfaces, grounded in WCAG 2.2 success criteria and inclusive design principles.

The module implements WCAG 2.2 compliance evaluation across all four principles (Perceivable, Operable, Understandable, Robust) with automated and manual testing checklists, assistive technology testing workflows for screen readers (NVDA, JAWS, VoiceOver), magnifiers, and voice control, color contrast analysis with APCA (Advanced Perceptual Contrast Algorithm) and WCAG 2.x luminance ratios, screen reader compatibility testing with ARIA landmark and live region specifications, cognitive accessibility assessment with reading level analysis and plain language scoring, inclusive design pattern libraries, accessibility statement generator, and automated scanning integration with axe-core, Lighthouse, and Pa11y.

Whether you are auditing an existing product for WCAG 2.2 AA compliance, designing an accessible component library, testing with real assistive technology users, or generating an accessibility statement for your organization, this module provides the structured frameworks, testing protocols, and reporting templates to ensure your product is genuinely inclusive.

## Core Capabilities

- **WCAG 2.2 Compliance Evaluation**: Full evaluation against all 86 success criteria (A, AA, AAA) with automated testing for machine-detectable issues and manual testing checklists for human-judgment criteria, organized by the POUR principles
- **Assistive Technology Testing**: Structured test protocols for screen readers (NVDA, JAWS, VoiceOver, TalkBack), screen magnifiers (ZoomText, built-in), voice control (Dragon, Voice Control), switch access, and alternative input devices
- **Color Contrast Analysis**: WCAG 2.x luminance contrast ratio calculations (AA: 4.5:1 normal, 3:1 large; AAA: 7:1 normal, 4.5:1 large) plus APCA perceptual contrast for modern contexts, with palette generation and remediation suggestions
- **Screen Reader Compatibility Testing**: ARIA landmark validation, live region announcement testing, heading hierarchy verification, table accessibility audit, and focus management testing across screen reader platforms
- **Cognitive Accessibility Assessment**: Reading level analysis (Flesch-Kincaid, Gunning Fog), plain language scoring, consistent navigation verification, error prevention and recovery assessment, and timeout adequacy evaluation
- **Inclusive Design Patterns**: Component-level accessibility patterns (accessible modals, carousels, tabs, accordions, forms, date pickers) with ARIA specifications, keyboard interaction maps, and platform-specific implementations
- **Accessibility Statement Generation**: Auto-generated accessibility statements with conformance level, known limitations, testing methodology, contact information, and last-updated timestamps
- **Automated Scanning Integration**: Batch scanning with axe-core rules, Lighthouse accessibility scoring, Pa11y CI integration, and violation-to-WCAG-criterion mapping with severity classification

## Usage Examples

### WCAG Compliance Evaluation

```python
from accessibility import WCAGEvaluator, ConformanceLevel, Principle, CriterionStatus, Severity

evaluator = WCAGEvaluator(level=ConformanceLevel.AA)

# Evaluate specific criteria
evaluator.evaluate_criterion(
    criterion_id="1.1.1",
    description="Non-text Content",
    principle=Principle.PERCEIVABLE,
    status=CriterionStatus.PASS,
    notes="All images have descriptive alt text",
)
evaluator.evaluate_criterion(
    criterion_id="1.4.3",
    description="Contrast (Minimum)",
    principle=Principle.PERCEIVABLE,
    status=CriterionStatus.FAIL,
    severity=Severity.SERIOUS,
    notes="Body text #777 on white fails AA ratio of 4.5:1",
    affected_elements=3,
)
evaluator.evaluate_criterion(
    criterion_id="2.1.1",
    description="Keyboard",
    principle=Principle.OPERABLE,
    status=CriterionStatus.PASS,
    notes="All interactive elements reachable via keyboard",
)

report = evaluator.report()
print(f"Overall: {report.conformance_status}")
print(f"Pass: {report.passed}, Fail: {report.failed}, Partial: {report.partial}")
print(f"Score: {report.score:.0%}")

# Drill into failures by principle
by_principle = evaluator.failures_by_principle()
for principle, failures in by_principle.items():
    print(f"\n{principle} failures:")
    for f in failures:
        print(f"  [{f.severity.value}] {f.criterion_id}: {f.description}")
```

### Color Contrast Analyzer

```python
from accessibility import ContrastAnalyzer, TextSize

analyzer = ContrastAnalyzer()

# Test specific color pairs
result = analyzer.check(
    foreground="#767676",
    background="#FFFFFF",
    text_size=TextSize.NORMAL,
)
print(f"Ratio: {result.ratio}:1")
print(f"AA Normal: {result.aa_normal}, AA Large: {result.aa_large}")
print(f"AAA Normal: {result.aaa_normal}, AAA Large: {result.aaa_large}")

# Get accessible alternatives
suggestions = analyzer.suggest_fixes(
    foreground="#767676",
    background="#FFFFFF",
    target_ratio=4.5,
    fix="foreground",
)
for s in suggestions:
    print(f"  Try: {s.color} (ratio: {s.ratio}:1)")

# Batch check multiple pairs
pairs = [("#333333", "#FFFFFF"), ("#0000FF", "#FFFFFF"), ("#FF6600", "#000000")]
results = analyzer.batch_check(pairs)
for r in results:
    print(f"  {r.foreground} on {r.background}: {r.ratio}:1")
```

### Screen Reader Test Protocol

```python
from accessibility import ScreenReaderTest, SRPlatform

test = ScreenReaderTest(
    page_name="Product Detail Page",
    platform=SRPlatform.NVDA,
    browser="Firefox",
)

# Record test steps
test.add_step(
    action="Navigate to page",
    expected="Page title announced, main landmark identified",
    actual="Page title announced correctly",
    status="pass",
)
test.add_step(
    action="Tab through product images",
    expected="Image alt text announced for each image",
    actual="First image alt text announced, gallery images have empty alt",
    status="fail",
)
test.add_step(
    action="Add to cart",
    expected="Cart count updated announced via aria-live",
    actual="Cart count updated, live region announced '2 items in cart'",
    status="pass",
)

results = test.summarize()
print(f"Pass: {results['pass']}, Fail: {results['fail']}")
print(f"Pass rate: {results['pass_rate']}")
for failed in results['failed_steps']:
    print(f"  FAILED: {failed['action']} — {failed['actual']}")
```

### Cognitive Accessibility Assessment

```python
from accessibility import CognitiveAccessibilityAssessor

assessor = CognitiveAccessibilityAssessor()

assessment = assessor.assess_page(
    page_name="Signup Form",
    text="Create your account. Enter your email and choose a password. "
         "You must agree to our terms before continuing.",
    has_timeout=True,
    timeout_seconds=15,
    has_error_prevention=True,
    consistent_nav=True,
)
print(f"Reading level: {assessment.reading_level.value}")
print(f"FK Grade: {assessment.flesch_kincaid_grade}")
print(f"Plain language score: {assessment.plain_language_score}/100")
for suggestion in assessment.suggestions:
    print(f"  Suggestion: {suggestion}")
```

### Accessibility Statement Generator

```python
from accessibility import AccessibilityStatement, ConformanceLevel

statement = AccessibilityStatement(
    organization="Acme Corp",
    website="acme.com",
    conformance_level=ConformanceLevel.AA,
    last_updated="2024-01-15",
    contact_email="accessibility@acme.com",
)
statement.add_known_limitation(
    title="Legacy PDF documents",
    description="Some archived PDFs from 2020-2022 are not fully accessible",
    workaround="Contact accessibility@acme.com for accessible alternatives",
    wcag_criteria=["1.1.1", "1.3.1"],
)
statement.add_testing_method(
    method="Automated scanning with axe-core + manual screen reader testing",
    tools=["axe-core 4.8", "NVDA 2023.3", "Lighthouse 11.0"],
)
print(statement.render())
```

### Automated Scanning Integration

```python
from accessibility import AutomatedScanner

scanner = AutomatedScanner()

# Import axe-core results
axe_violations = [
    {"id": "color-contrast", "description": "Elements must have sufficient color contrast",
     "impact": "serious", "tags": ["wcag2aa", "wcag143"], "nodes": [{"html": "..."}]},
    {"id": "image-alt", "description": "Images must have alternate text",
     "impact": "critical", "tags": ["wcag2a", "wcag111"], "nodes": [{"html": "..."}, {"html": "..."}]},
]
scanner.import_axe_results(axe_violations)

summary = scanner.summary()
print(f"Total violations: {summary['total_violations']}")
print(f"By severity: {summary['by_severity']}")
```

## Best Practices

1. **Test with Real Users, Not Just Tools**: Automated scanners catch ~30% of accessibility issues. The remaining 70%—keyboard navigation flow, screen reader experience, cognitive clarity—require testing with real assistive technology users.

2. **Use Semantic HTML Before ARIA**: A `<button>` with no ARIA is more accessible than a `<div role="button">` with elaborate ARIA. Native HTML elements have built-in accessibility; ARIA supplements them, not replaces them.

3. **Color Is Never the Only Indicator**: Every color-coded state (error, required, active, disabled) must also be communicated through text, icons, or pattern changes. ~8% of men and ~0.5% of women have color vision deficiency.

4. **Keyboard Navigation Must Be Logical**: Tab order must follow visual reading order. Focus indicators must be visible. Focus must never be lost (focus trapping in modals, focus restoration on modal close). Skip links must be provided for repeated navigation.

5. **Live Regions Must Be Used Strategically**: `aria-live="polite"` for non-urgent updates (cart count, search results). `aria-live="assertive"` for urgent alerts (error messages, timeout warnings). Overuse of assertive live regions creates a cacophony that overwhelms screen reader users.

6. **Test Across Screen Readers**: NVDA, JAWS, and VoiceOver each have different behavior quirks. NVDA + Firefox is the most common free combination; JAWS + Chrome dominates enterprise; VoiceOver + Safari dominates Mac/iOS. Test all three for comprehensive coverage.

7. **Maintain a Voluntary Product Accessibility Template (VPAT)**: For enterprise sales, a VPAT/ACR (Accessibility Conformance Report) is often required. Keep it updated with each release, documenting conformance status for each WCAG criterion.

8. **Accessibility Debt Is Technical Debt**: Every accessibility violation accumulates interest. Fix issues as they're found; don't defer to "the next big redesign." Retroactive accessibility fixes cost 3-10x more than building accessibly from the start.

## Related Modules

- [usability-testing](../usability-testing/GROK.md) — Usability testing with assistive technology users
- [interaction-design](../interaction-design/GROK.md) — Accessible interaction patterns and keyboard navigation design
- [information-architecture](../information-architecture/GROK.md) — Accessible navigation and heading structure
- [user-research](../user-research/GROK.md) — Inclusive research recruitment and methodology

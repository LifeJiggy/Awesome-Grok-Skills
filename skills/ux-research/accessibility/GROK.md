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

---

## Advanced Configuration

### ARIA Pattern Registry

```python
from accessibility import ARIAPatternRegistry

registry = ARIAPatternRegistry()
registry.register_pattern("modal_dialog", {
    "role": "dialog",
    "aria_modal": "true",
    "aria_labelledby": "dialog-title",
    "focus_trap": True,
    "escape_closes": True,
    "return_focus_on_close": True,
})
```

### Automated Scanning Configuration

```python
from accessibility import ScannerConfig

config = ScannerConfig(
    axe_version="4.8",
    wcag_level="AA",
    include_impact=["critical", "serious", "moderate"],
    exclude_rules=["region"],
    page_timeout_ms=30000,
    max_pages=500,
)
scanner = AutomatedScanner(config=config)
```

## Architecture Patterns

### Accessibility Testing Pyramid

```
Manual AT Testing (Screen Readers)
        │
        ▼
    ┌──────────────┐
    │ Automated    │── axe-core, Lighthouse, Pa11y
    │ Scanning     │
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ CI/CD Gate   │── Build fails on violations
    └──────┬───────┘
           │
           ▼
    ┌──────────────┐
    │ Semantic     │── HTML elements, ARIA landmarks
    │ Foundation   │
    └──────────────┘
```

### WCAG POUR Principles

- **Perceivable**: Information must be presentable (alt text, contrast, captions)
- **Operable**: Interface must be navigable (keyboard, timing, seizure-safe)
- **Understandable**: Information must be clear (language, predictability, input assistance)
- **Robust**: Content must work with assistive tech (valid HTML, ARIA, compatibility)

## Integration Guide

### CI/CD Integration

```yaml
# GitHub Actions accessibility check
- name: Accessibility Scan
  uses: deque-labs/axe-action@v1
  with:
    urls: http://localhost:3000
    exit-code: true
    axe-options: --tags wcag2a,wcag2aa
```

### Storybook Integration

```python
from accessibility import StorybookA11yAddon

addon = StorybookA11yAddon()
addon.check_component("Button", {
    "html": "<button>Click me</button>",
    "expected_role": "button",
    "contrast_ratio": 4.5,
})
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Incremental scanning | Scan only changed pages |
| Rule caching | Skip unchanged axe rules |
| Parallel page scanning | 5x faster full-site scans |
| Baseline comparison | Only report new violations |

## Security Considerations

- **Accessible authentication**: No cognitive function tests for login
- **CAPTCHA alternatives**: Provide audio or logic-based alternatives
- **Error identification**: Clear, accessible error messages
- **Data entry assistance**: Autocomplete, input masking with accessibility

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Screen reader skips content | Missing ARIA landmark | Add role or semantic HTML |
| Focus trap not working | Missing tabindex | Set tabindex="-1" on trap boundary |
| Contrast fails after theme change | CSS variable override | Update light theme CSS variables |
| Live region not announced | Wrong aria-live value | Use "polite" for non-urgent |
| Form errors inaccessible | No error association | Use aria-describedby on error messages |

## API Reference

### WCAGEvaluator

```python
class WCAGEvaluator:
    def __init__(self, level: ConformanceLevel)
    def evaluate_criterion(self, criterion_id: str, description: str, principle: Principle, status: CriterionStatus, **kwargs) -> None
    def report(self) -> ConformanceReport
    def failures_by_principle(self) -> dict
```

### ContrastAnalyzer

```python
class ContrastAnalyzer:
    def check(self, foreground: str, background: str, text_size: TextSize) -> ContrastResult
    def suggest_fixes(self, foreground: str, background: str, target_ratio: float, fix: str) -> list[ColorSuggestion]
    def batch_check(self, pairs: list) -> list[ContrastResult]
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class ConformanceLevel(Enum):
    A = "A"
    AA = "AA"
    AAA = "AAA"

class Principle(Enum):
    PERCEIVABLE = "perceivable"
    OPERABLE = "operable"
    UNDERSTANDABLE = "understandable"
    ROBUST = "robust"

@dataclass
class CriterionResult:
    criterion_id: str
    description: str
    principle: Principle
    status: str
    severity: str
    affected_elements: int

@dataclass
class ContrastResult:
    ratio: float
    aa_normal: bool
    aa_large: bool
    aaa_normal: bool
    aaa_large: bool
```

## Deployment Guide

### Installation

```bash
pip install accessibility
```

### Accessibility Program Setup

1. Establish baseline with automated scan
2. Fix critical/serious violations
3. Set up CI/CD gates
4. Train team on WCAG basics
5. Schedule quarterly manual AT testing
6. Maintain accessibility statement

## Monitoring & Observability

```python
from accessibility import MetricsCollector

collector = MetricsCollector()
collector.gauge("a11y.violations.total", count, tags={"severity": sev})
collector.counter("a11y.violations.fixed", count)
collector.gauge("a11y.conformance.score", score, tags={"level": level})
collector.histogram("a11y.scan.duration_seconds", duration)
```

## Testing Strategy

```python
import pytest
from accessibility import ContrastAnalyzer, TextSize

def test_contrast_aa():
    analyzer = ContrastAnalyzer()
    result = analyzer.check("#000000", "#FFFFFF", TextSize.NORMAL)
    assert result.aa_normal is True
    assert result.ratio >= 4.5
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added APCA contrast | Re-run contrast checks |
| 2.0.0 | WCAG 2.2 support | Add new 2.2 criteria checks |

## Glossary

| Term | Definition |
|------|-----------|
| **WCAG** | Web Content Accessibility Guidelines |
| **ARIA** | Accessible Rich Internet Applications |
| **Screen Reader** | Assistive technology that reads screen content aloud |
| **Focus Indicator** | Visual outline showing current keyboard focus |
| **Skip Link** | Hidden link to bypass repeated navigation |
| **Live Region** | ARIA region that announces dynamic content changes |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with WCAG 2.2 evaluation
- Color contrast analysis (WCAG + APCA)
- Screen reader test protocols
- Automated scanning integration

## Contributing Guidelines

```bash
git clone https://github.com/example/accessibility.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### WCAG 2.2 Success Criteria Quick Reference

| Criterion | Level | Description | Automated? |
|-----------|-------|-------------|------------|
| 1.1.1 Non-text Content | A | Alt text for images | Yes |
| 1.3.1 Info and Relationships | A | Semantic HTML | Partial |
| 1.4.3 Contrast (Minimum) | AA | 4.5:1 ratio | Yes |
| 1.4.11 Non-text Contrast | AA | 3:1 for UI components | Yes |
| 2.1.1 Keyboard | A | All functionality via keyboard | Partial |
| 2.4.1 Bypass Blocks | A | Skip navigation link | Yes |
| 2.4.3 Focus Order | A | Logical tab order | Partial |
| 2.4.7 Focus Visible | AA | Visible focus indicator | Yes |
| 2.5.7 Dragging Movements | AA | Alternative to drag | Yes |
| 2.5.8 Target Size | AA | 24x24px minimum | Yes |
| 3.1.1 Language of Page | A | html lang attribute | Yes |
| 3.3.1 Error Identification | A | Clear error messages | Partial |
| 4.1.2 Name, Role, Value | A | ARIA for custom widgets | Partial |

### Color Contrast Quick Reference

| Text Size | AA Ratio | AAA Ratio | Example |
|-----------|----------|-----------|---------|
| Normal (< 18pt) | 4.5:1 | 7:1 | Body text |
| Large (≥ 18pt or 14pt bold) | 3:1 | 4.5:1 | Headings |
| UI Components | 3:1 | — | Buttons, icons |

### Screen Reader Testing Matrix

| Screen Reader | Browser | Platform | Priority |
|--------------|---------|----------|----------|
| NVDA | Firefox | Windows | High |
| JAWS | Chrome | Windows | High |
| VoiceOver | Safari | macOS | High |
| VoiceOver | Safari | iOS | High |
| TalkBack | Chrome | Android | Medium |
| NVDA | Edge | Windows | Low |

### ARIA Role Reference

| Role | Usage | Example |
|------|-------|---------|
| button | Interactive button | `<button>` or `[role="button"]` |
| link | Navigation link | `<a href>` or `[role="link"]` |
| dialog | Modal dialog | Modal overlay |
| alertdialog | Urgent modal | Error confirmation |
| navigation | Nav landmark | `<nav>` or `[role="navigation"]` |
| main | Main content | `<main>` or `[role="main"]` |
| complementary | Sidebar | `<aside>` or `[role="complementary"]` |
| contentinfo | Footer | `<footer>` or `[role="contentinfo"]` |
| banner | Header | `<header>` or `[role="banner"]` |
| search | Search form | `<form role="search">` |
| tab | Tab element | Tab interface |
| tabpanel | Tab content | Tab content area |
| menu | Menu container | Dropdown menu |
| menuitem | Menu item | Menu option |
| listbox | Selection list | Custom select |
| option | Listbox option | Select option |
| combobox | Dropdown input | Autocomplete |

### Cognitive Accessibility Guidelines

| Guideline | Description | Implementation |
|-----------|-------------|----------------|
| Plain language | Use simple, clear language | Flesch-Kincaid grade 8 or below |
| Consistent navigation | Same nav on every page | Shared navigation component |
| Predictable behavior | No unexpected changes | No auto-focus shifts |
| Error prevention | Confirm before submit | Review step in forms |
| Error recovery | Clear error messages | Inline validation |
| Time limits | Extend or remove timeouts | "Need more time?" option |
| Multiple means | Text, visual, audio | Alt text, captions, transcripts |

### Accessibility Testing Checklist

```
AUTOMATED TESTING
    □ Run axe-core scan (0 violations)
    □ Run Lighthouse accessibility audit (> 90)
    □ Check color contrast ratios
    □ Verify all images have alt text
    □ Check heading hierarchy
    □ Verify form labels
    □ Check ARIA attributes

MANUAL TESTING
    □ Navigate entire page with keyboard only
    □ Test with screen reader (NVDA + Firefox)
    □ Test with screen reader (VoiceOver + Safari)
    □ Check focus indicators
    □ Test form error handling
    □ Verify skip navigation works
    □ Test modal focus trapping
    □ Check responsive at 200% zoom
    □ Test with reduced motion
```

### VPAT Template Structure

```markdown
# Voluntary Product Accessibility Template (VPAT)

## Product Information
- Product Name: [Name]
- Version: [Version]
- Date: [Date]
- Contact: [Contact info]

## WCAG 2.1 Conformance Results

### Principle 1: Perceivable
| Criterion | Level | Status | Notes |
|-----------|-------|--------|-------|
| 1.1.1 Non-text Content | A | Supports | All images have alt text |
| 1.3.1 Info and Relationships | A | Supports | Semantic HTML used |

### Principle 2: Operable
| Criterion | Level | Status | Notes |
|-----------|-------|--------|-------|
| 2.1.1 Keyboard | A | Supports | Full keyboard navigation |

### Principle 3: Understandable
| Criterion | Level | Status | Notes |
|-----------|-------|--------|-------|
| 3.1.1 Language of Page | A | Supports | lang attribute set |

### Principle 4: Robust
| Criterion | Level | Status | Notes |
|-----------|-------|--------|-------|
| 4.1.2 Name, Role, Value | A | Partially Supports | Custom widgets need ARIA |

## Legal Disclaimer
[Standard VPAT disclaimer text]
```

### Complete Keyboard Navigation Reference

| Key | Action | Context |
|-----|--------|---------|
| Tab | Move to next focusable element | Global |
| Shift+Tab | Move to previous focusable element | Global |
| Enter | Activate button/link | Button, Link |
| Space | Activate button, toggle checkbox | Button, Checkbox |
| Arrow keys | Navigate within component | Menu, Tabs, Listbox |
| Escape | Close modal/menu, cancel | Modal, Menu |
| Home | Move to first item | List, Grid |
| End | Move to last item | List, Grid |
| Page Up/Down | Scroll page | Global |

### Complete Focus Management Reference

| Component | Focus Behavior | Trap? | Return? |
|-----------|---------------|-------|---------|
| Modal dialog | Move to first element | Yes | Yes, to trigger |
| Dropdown menu | Move to first item | Yes | Yes, to trigger |
| Tab panel | Move to active tab | No | N/A |
| Toast/notification | Move to dismiss button | No | N/A |
| Tooltip | No focus change | No | N/A |

### Complete ARIA State Reference

| Component | State | Attribute | Values |
|-----------|-------|-----------|--------|
| Checkbox | Checked | aria-checked | true, false, mixed |
| Expandable | Expanded | aria-expanded | true, false |
| Selected | Selected | aria-selected | true, false |
| Disabled | Disabled | aria-disabled | true, false |
| Required | Required | aria-required | true, false |
| Invalid | Invalid | aria-invalid | true, false |
| Busy | Busy | aria-busy | true, false |
| Live | Live | aria-live | off, polite, assertive |

### Complete Color Contrast pairs

| Pair | Ratio | AA | AAA | Use |
|------|-------|-----|-----|-----|
| Black on White | 21:1 | Pass | Pass | Maximum contrast |
| Dark Gray on White | 12:1 | Pass | Pass | High contrast |
| Medium Gray on White | 4.5:1 | Pass | Fail | Minimum AA |
| Light Gray on White | 2:1 | Fail | Fail | Insufficient |
| White on Black | 21:1 | Pass | Pass | Maximum contrast |
| Yellow on Black | 15:1 | Pass | Pass | High contrast |
| Blue on White | 8.6:1 | Pass | Pass | Good contrast |
| Red on White | 4:1 | Fail | Fail | Borderline |

### WCAG 2.2 New Success Criteria (Level AA)

| Criterion | Description | Implementation |
|-----------|-------------|----------------|
| 2.4.11 Focus Not Obscured (Minimum) | Focused element not hidden by sticky content | Ensure sticky headers have sufficient padding |
| 2.4.12 Focus Not Obscured (Enhanced) | Focused element fully visible | Avoid sticky overlays near focus targets |
| 2.4.13 Focus Appearance | Focus indicator meets size/contrast requirements | Minimum 2px outline, 3:1 contrast |
| 2.5.7 Dragging Movements | Drag actions have single-pointer alternative | Provide move button alongside drag |
| 2.5.8 Target Size (Minimum) | Interactive targets at least 24x24 CSS px | Increase padding on small buttons |
| 3.2.6 Consistent Help | Help mechanisms in consistent location | Footer help link on every page |
| 3.3.7 Redundant Entry | Don't ask for information already provided | Pre-fill from prior form steps |
| 3.3.8 Accessible Authentication (Minimum) | No cognitive function test for login | Support passkeys, password managers |
| 3.3.9 Accessible Authentication (Enhanced) | No object/content recognition for login | Avoid image-based CAPTCHAs |

### Assistive Technology Compatibility Matrix

| Feature | NVDA | JAWS | VoiceOver | TalkBack |
|---------|------|------|-----------|----------|
| Landmark navigation | Full | Full | Full | Partial |
| ARIA live regions | Full | Full | Full | Partial |
| Table navigation | Full | Full | Full | Partial |
| Form validation | Full | Full | Full | Full |
| Modal focus trap | Full | Full | Full | Partial |
| Custom widgets | Full | Full | Partial | Partial |
| CSS content (pseudo) | Partial | Full | Partial | None |
| CSS `content: ""` empty | Hidden | Hidden | Hidden | Hidden |
| SVG accessible names | Full | Full | Partial | Partial |
| Canvas fallback | Full | Full | Full | Partial |

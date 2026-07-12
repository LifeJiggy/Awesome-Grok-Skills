---
name: "accessibility-tools"
category: "social-impact-tech"
version: "1.0.0"
tags: ["social-impact-tech", "accessibility-tools"]
---

# Accessibility Tools — WCAG Compliance & Assistive Technology Toolkit

## Overview

Accessibility tools form the backbone of inclusive digital design, ensuring that web applications, documents, and digital interfaces are usable by people with the full spectrum of human abilities — including visual, auditory, motor, and cognitive disabilities. This module provides a comprehensive Python toolkit for automated WCAG 2.1/2.2 compliance checking, screen reader optimization, color contrast analysis, ARIA validation, and end-to-end accessibility audit pipelines.

The toolkit bridges the gap between manual accessibility audits (which are expensive and infrequent) and fully automated solutions (which catch only a fraction of issues). It combines deterministic rule-based checking with heuristic analysis to surface WCAG violations, provide remediation guidance, and generate audit reports that align with Section 508, ADA Title III, and EN 301 549 requirements. Each checker produces structured findings with severity levels, affected success criteria, and concrete fix suggestions.

Beyond compliance, this module supports assistive technology compatibility testing — verifying that ARIA landmarks are properly announced, that focus management works correctly during dynamic content updates, and that keyboard navigation paths cover all interactive elements. It includes utilities for generating alt-text suggestions for images using heuristics and computer vision APIs, testing color palettes for deficiency simulators (protanopia, deuteranopia, tritanopia), and producing accessibility statements that summarize conformance levels.

The toolkit is designed to integrate seamlessly into CI/CD pipelines, providing regression detection and continuous compliance monitoring. It supports batch processing of large codebases, per-page incremental checks, and diff-based analysis that surfaces only newly introduced violations. All findings are output in structured formats (JSON, SARIF, HTML) compatible with issue trackers and accessibility management platforms.

## Core Capabilities

- **WCAG 2.1/2.2 Automated Compliance Checking**: Scan HTML, CSS, and ARIA attributes against Success Criteria across levels A, AA, and AAA with structured violation reports.
- **Color Contrast Analysis**: Calculate contrast ratios per WCAG 2.1 SC 1.4.3/1.4.6, simulate color vision deficiencies, and suggest compliant alternative palettes.
- **ARIA Validation**: Verify correct usage of ARIA roles, states, and properties — detecting missing required properties, invalid values, and landmark redundancy.
- **Keyboard Navigation Testing**: Map interactive element tab order, detect focus traps, verify skip-link functionality, and validate custom keyboard interactions.
- **Alt-Text Generation & Audit**: Audit images for missing or inadequate alternative text, generate heuristic alt-text from filenames/contexts, and interface with vision APIs for scene descriptions.
- **Screen Reader Compatibility Analysis**: Check heading hierarchy, landmark regions, live region declarations, and table accessibility for screen reader consumption.
- **Accessibility Audit Pipeline**: Orchestrate full-site or full-app audits with configurable scope, issue deduplication, severity scoring, and exportable reports (JSON, HTML, CSV).
- **Assistive Technology Compatibility Matrix**: Maintain and check against known AT/browser/version compatibility data to flag risky patterns.
- **PDF & Document Accessibility**: Validate tagged PDF structure, reading order, heading hierarchy, alt-text on images, and form field labels for document accessibility compliance.
- **Form Accessibility Validation**: Check form labels, fieldset/legend grouping, error message association, autocomplete attributes, and required field indicators.
- **Motion & Animation Compliance**: Detect prefers-reduced-motion violations, auto-playing animations without pause controls, and flashing content that exceeds seizure thresholds.
- **Cognitive Accessibility Checks**: Validate clear navigation, consistent layout, error prevention, input assistance, and plain language indicators.

## Usage Examples

### Basic WCAG Compliance Check

```python
from accessibility_tools import WCAGComplianceChecker, Severity

checker = WCAGComplianceChecker(level="AA")
report = checker.check_html_file("index.html")

for violation in report.violations:
    print(f"[{violation.severity}] SC {violation.success_criterion}: {violation.message}")
    print(f"  Element: {violation.element}")
    print(f"  Fix: {violation.remediation}")

print(f"\nSummary: {report.total_violations} issues, {report.conformance_level} conformance")
```

### Color Contrast Analysis

```python
from accessibility_tools import ColorContrastAnalyzer, VisionDeficiency

analyzer = ColorContrastAnalyzer()

# Check a specific foreground/background pair
result = analyzer.check_contrast(
    foreground="#767676",
    background="#FFFFFF",
    is_large_text=False
)
print(f"Contrast ratio: {result.ratio}:1")
print(f"Passes AA: {result.passes_aa}")
print(f"Passes AAA: {result.passes_aaa}")

# Simulate color vision deficiencies
for deficiency in VisionDeficiency:
    simulated = analyzer.simulate_deficiency("#FF0000", "#00FF00", deficiency)
    print(f"{deficiency.name}: visible={simulated.is_distinguishable}")
```

### Full Audit Pipeline

```python
from accessibility_tools import AccessibilityAuditPipeline, AuditScope, ReportFormat

pipeline = AccessibilityAuditPipeline(
    scope=AuditScope(
        url="https://example.com",
        max_depth=3,
        include_subdomains=False
    ),
    wcag_level="AA",
    parallel_workers=4
)

results = pipeline.run()
results.export("audit-report.html", format=ReportFormat.HTML)
results.export("audit-data.json", format=ReportFormat.JSON)

print(f"Pages scanned: {results.pages_scanned}")
print(f"Critical issues: {results.critical_count}")
print(f"Estimated remediation effort: {results.estimated_hours}h")
```

### ARIA Landmark Validation

```python
from accessibility_tools import ARIAValidator

validator = ARIAValidator()
issues = validator.validate_landmarks(html_content)

for issue in issues:
    print(f"{issue.severity}: {issue.rule_id} - {issue.description}")
    print(f"  Suggestion: {issue.suggestion}")
```

### Keyboard Navigation Audit

```python
from accessibility_tools import KeyboardAuditor, TabOrderReport

auditor = KeyboardAuditor()

# Analyze tab order and focus management
tab_report = auditor.analyze_tab_order("page.html")

print(f"Total focusable elements: {tab_report.total_elements}")
print(f"Focus traps detected: {len(tab_report.focus_traps)}")
print(f"Tab order issues: {len(tab_report.order_violations)}")

for trap in tab_report.focus_traps:
    print(f"  Trap: {trap.element} at line {trap.line_number}")

# Verify skip link functionality
skip_result = auditor.verify_skip_links("page.html")
print(f"Skip link present: {skip_result.has_skip_link}")
print(f"Skip link target valid: {skip_result.target_valid}")
```

### Alt-Text Generation and Audit

```python
from accessibility_tools import AltTextAuditor, VisionAPIIntegration

# Audit existing alt-text
auditor = AltTextAuditor()
audit_result = auditor.audit_directory("./images")

print(f"Images with alt-text: {audit_result.has_alt_count}/{audit_result.total_images}")
print(f"Missing alt-text: {len(audit_result.missing_alt)}")
print(f"Generic alt-text (e.g., 'image'): {len(audit_result.generic_alt)}")
print(f"Inadequate length: {len(audit_result.too_short)}")

for img in audit_result.issues:
    print(f"  {img.filename}: {img.issue_type} — {img.suggestion}")

# Generate alt-text via vision API
vision = VisionAPIIntegration(api_key="your-api-key")
generated = vision.describe_image("./photos/team_meeting.jpg")
print(f"Suggested alt-text: {generated.description}")
```

### Color Palette Accessibility Checker

```python
from accessibility_tools import PaletteAnalyzer, WCAGPaletteSuggestion

analyzer = PaletteAnalyzer()

# Audit an entire color palette
palette = {
    "primary": "#2563EB",
    "secondary": "#7C3AED",
    "background": "#FFFFFF",
    "text": "#1F2937",
    "muted": "#9CA3AF",
    "error": "#DC2626",
    "success": "#059669",
}

report = analyzer.audit_palette(palette, background="background")

for entry in report.entries:
    status = "PASS" if entry.passes_aa else "FAIL"
    print(f"  {entry.color_name}: {entry.ratio}:1 [{status}] AA={entry.passes_aa} AAA={entry.passes_aaa}")

if report.has_failures:
    suggestions = WCAGPaletteSuggestion.repair_palette(palette, background="background")
    print(f"\nSuggested repairs:")
    for name, color in suggestions.items():
        print(f"  {name}: {color}")
```

### Screen Reader Compatibility Check

```python
from accessibility_tools import ScreenReaderAnalyzer

analyzer = ScreenReaderAnalyzer()
result = analyzer.analyze_page("dashboard.html")

print(f"Heading hierarchy: {'Valid' if result.heading_hierarchy_valid else 'Invalid'}")
print(f"  Headings found: {result.heading_count}")
print(f"  Skipped levels: {result.skipped_heading_levels}")

print(f"Landmarks: {result.landmark_count}")
print(f"  Named regions: {len(result.unnamed_landmarks)} unnamed")
print(f"Live regions: {result.live_region_count}")

print(f"Tables: {result.table_count}")
print(f"  Tables with captions: {result.tables_with_caption}")
print(f"  Tables with headers: {result.tables_with_headers}")

for warning in result.warnings:
    print(f"  Warning: {warning}")
```

### CI/CD Integration

```python
from accessibility_tools import CICDAccessibilityGate

gate = CICDAccessibilityGate(
    wcag_level="AA",
    max_critical=0,
    max_serious=5,
    fail_on_regression=True,
)

# Run in pre-deploy step
result = gate.check_deployment(
    baseline_report="last_passing_audit.json",
    current_report="current_audit.json",
)

if result.passed:
    print("Accessibility gate: PASSED")
else:
    print("Accessibility gate: FAILED")
    for regression in result.regressions:
        print(f"  Regression: {regression.rule_id} on {regression.page}")
    exit(1)
```

## Best Practices

1. **Test at all three WCAG levels progressively**: Start with Level A (minimum), then verify AA (standard legal requirement), and target AAA for critical user journeys. Don't skip levels — each builds on the previous.

2. **Combine automated and manual testing**: Automated tools catch roughly 30-40% of accessibility issues. Always supplement with manual keyboard testing, screen reader walkthroughs (NVDA, JAWS, VoiceOver), and cognitive walkthroughs.

3. **Run audits in CI/CD pipelines**: Integrate accessibility checks into your deployment pipeline. Block deployments on critical violations and track severity trends over time to prevent regression.

4. **Test with real assistive technologies**: Automated compatibility matrices are useful, but nothing replaces testing with actual screen readers on actual browsers. Maintain a matrix of AT/browser combinations your users rely on.

5. **Prioritize by user impact, not by technical severity**: A WCAG Level A violation that blocks an entire user journey is more critical than a Level AAA issue on a decorative element. Weight findings by the percentage of affected users and the severity of the barrier.

6. **Maintain an accessibility knowledge base**: Document recurring violations, their fixes, and the reasoning behind architectural decisions. This prevents the same issues from being reintroduced after team turnover.

7. **Use semantic HTML before ARIA**: The first rule of ARIA is "don't use ARIA." Native HTML elements provide built-in accessibility semantics. Use ARIA only when native semantics are insufficient.

8. **Audit dynamic content updates**: Modern SPAs introduce accessibility challenges during route changes, modal opens, and live content updates. Ensure focus management, live region announcements, and heading hierarchy are maintained across all state transitions.

9. **Design for cognitive accessibility**: Clear headings, consistent navigation, predictable interactions, and plain language benefit everyone. Cognitive accessibility is often overlooked but affects a larger population than physical disabilities.

10. **Track accessibility metrics over time**: Monitor violation counts, severity distributions, and resolution times across releases. Use trend data to justify accessibility investment and demonstrate progress to stakeholders.

## Related Modules

- [community-platforms](../community-platforms/GROK.md) — Accessible community engagement tools
- [education-access](../education-access/GROK.md) — Accessible education delivery platforms
- [health-equity](../health-equity/GROK.md) — Accessible health information and telemedicine
- [crisis-response](../crisis-response/GROK.md) — Accessible emergency alert systems

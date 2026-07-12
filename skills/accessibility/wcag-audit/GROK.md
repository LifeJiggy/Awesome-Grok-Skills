---
name: "wcag-audit"
category: "accessibility"
version: "2.0.0"
tags: ["accessibility", "wcag", "audit", "compliance", "screen-reader", "section-508", "ada"]
---

# WCAG Audit

## Overview

Comprehensive Web Content Accessibility Guidelines (WCAG) audit toolkit for evaluating web applications against WCAG 2.0, 2.1, and 2.2 success criteria at AA and AAA conformance levels. This module automates the detection of accessibility violations, generates compliance reports with severity scoring, tracks remediation progress, and integrates with CI/CD pipelines for continuous compliance monitoring. Supports both manual and automated audit workflows with role-based report generation for developers, designers, and compliance officers.

## Core Capabilities

- **Automated WCAG Criterion Checking**: Validates all 78 success criteria (A, AA, AAA) across the four principles: Perceivable, Operable, Understandable, and Robust
- **Violation Severity Classification**: Categorizes issues as Critical, Serious, Moderate, Minor, or Best Practice with CVSS-like scoring
- **Multi-Format Reporting**: Generates HTML, JSON, PDF, and JUnit XML reports for different stakeholders
- **Remediation Tracking**: Links violations to specific code locations with fix suggestions and estimated effort
- **Baseline Comparison**: Tracks accessibility regression across releases with delta reports
- **CI/CD Integration**: Provides exit codes and gate policies for build pipelines
- **Custom Rule Engine**: Extend built-in rules with XPath, CSS selector, and JavaScript-based custom validators
- **Screenshot Evidence**: Captures annotated screenshots of violations for visual documentation

## Usage

```python
from wcag_audit import WCAGAuditor, AuditConfig, Severity, ConformanceLevel

# Configure audit for WCAG 2.1 AA
config = AuditConfig(
    url="https://example.com",
    conformance_level=ConformanceLevel.AA,
    wcag_version="2.1",
    include_screenshots=True,
    custom_rules_path="./rules",
    excluded_paths=["/admin", "/legacy"],
    viewport_width=1440,
    viewport_height=900,
    wait_for_load=5.0,
    max_pages=50,
    follow_links=True,
)

auditor = WCAGAuditor(config)
results = auditor.run()

# Process results
print(f"Total violations: {results.total_violations}")
print(f"Critical: {results.by_severity[Severity.CRITICAL]}")
print(f"Score: {results.compliance_score}/100")

# Generate reports
auditor.export_html_report(results, "report.html")
auditor.export_junit_xml(results, "junit.xml")
auditor.export_json(results, "results.json")

# Baseline comparison
previous = auditor.load_baseline("baseline.json")
delta = auditor.compare(results, previous)
print(f"Regressions: {delta.regressions}")
print(f"Fixes: {delta.fixes}")
```

```python
# CI/CD gate usage
from wcag_audit import CIIntegration, GatePolicy

gate = CIIntegration(
    policy=GatePolicy(
        max_critical=0,
        max_serious=5,
        fail_on_regression=True,
        baseline_file="accessibility-baseline.json",
    )
)

exit_code = gate.evaluate("https://staging.example.com")
sys.exit(exit_code)  # 0 = pass, 1 = fail
```

## Best Practices

- Run audits on every pull request and before each release to catch regressions early
- Maintain a baseline file in version control and update it only after conscious triage decisions
- Combine automated scanning with manual testing — automated tools catch ~30-40% of real-world issues
- Prioritize Critical and Serious violations before moving to Moderate issues
- Use ARIA landmarks and semantic HTML as first-line defenses rather than ARIA patching
- Test with actual assistive technologies (NVDA, JAWS, VoiceOver) alongside automated checks
- Document accepted risks in an accessibility conformance report (ACR) per VPAT template
- Run audits against both desktop (1440px) and mobile (375px) viewports
- Include color contrast checks for all text sizes including placeholder text and disabled states
- Validate that focus indicators are visible on all interactive elements
- Audit dynamic content updates using ARIA live regions

## Related Modules

- **screen-reader-testing** — Manual and automated screen reader interaction testing with NVDA, JAWS, and VoiceOver
- **color-contrast** — Dedicated contrast ratio analysis with color blindness simulation
- **keyboard-navigation** — Full keyboard traversal testing and focus management validation
- **aria-implementation** — ARIA role, state, and property implementation guidelines and validators
- **api** → **api-documentation** — Accessible API documentation generation
- **frontend-design** — Accessible design system foundations

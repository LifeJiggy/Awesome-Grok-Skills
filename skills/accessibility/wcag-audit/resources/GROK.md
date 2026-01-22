# Accessibility Agent

## Overview

The **Accessibility Agent** provides comprehensive WCAG (Web Content Accessibility Guidelines) compliance auditing and accessibility testing capabilities. This agent helps ensure digital content and applications are accessible to users with disabilities, including visual, auditory, motor, and cognitive impairments.

## Core Capabilities

### 1. WCAG Compliance Auditing
The agent performs automated accessibility audits against WCAG 2.1 guidelines across three conformance levels:
- **Level A**: Essential accessibility requirements
- **Level AA**: Enhanced accessibility (most common target)
- **Level AAA**: Highest level of accessibility

### 2. Accessibility Issue Detection
Automatically identifies common accessibility issues:
- Missing alternative text for images
- Insufficient color contrast ratios
- Missing form labels and ARIA attributes
- Keyboard navigation problems
- Missing page titles and language attributes
- Focus indicator issues
- Incorrect heading structure

### 3. ARIA Validation
Validates Accessible Rich Internet Applications (ARIA) markup:
- Checks ARIA role assignments
- Validates ARIA attribute syntax
- Ensures proper ARIA landmark usage
- Verifies live region configurations

### 4. Accessibility Scoring
Provides quantitative accessibility scores:
- Overall accessibility percentage (0-100)
- Issues categorized by severity (Critical, High, Medium, Low)
- WCAG criterion breakdown analysis
- Trend tracking over time

## Usage Examples

### Basic Accessibility Audit

```python
from accessibility import AccessibilityAuditor

auditor = AccessibilityAuditor()
results = auditor.audit_page(html_content, "https://example.com")

print(f"Score: {results['score']}/100")
print(f"Total Issues: {results['total_issues']}")
print(f"Critical: {results['issues_by_severity']['critical']}")
```

### Generate Accessibility Report

```python
report = auditor.generate_report(results)
print(report)
```

### ARIA Validation

```python
validator = ARIAValidator()
issues = validator.validate_aria(html_content)
for issue in issues:
    print(f"Element: {issue['element']}")
    print(f"Fix: {issue['fix']}")
```

## Severity Levels

| Severity | Impact | Response Time |
|----------|--------|---------------|
| **Critical** | Complete barrier to access | Immediate |
| **High** | Significant barrier | Within 24 hours |
| **Medium** | Partial barrier | Within 1 week |
| **Low** | Minor inconvenience | Within 1 month |
| **Info** | Enhancement opportunity | As needed |

## Common Accessibility Issues

### Color Contrast
- Minimum 4.5:1 for normal text (Level AA)
- Minimum 3:1 for large text (Level AA)
- Minimum 7:1 for normal text (Level AAA)

### Alternative Text
- All meaningful images require `alt` attributes
- Decorative images should have `alt=""`
- Complex images need detailed descriptions

### Keyboard Accessibility
- All functionality available via keyboard
- Visible focus indicators
- Logical tab order
- No keyboard traps

### Forms
- All inputs have associated labels
- Clear error messages
- Required fields indicated
- Error suggestions provided

## Integration Points

The Accessibility Agent integrates with:
- **CI/CD Pipelines**: Automated testing in build processes
- **Content Management Systems**: Plugin integrations
- **Browser Extensions**: Real-time page analysis
- **Testing Frameworks**: Integration with Selenium, Playwright

## Best Practices

1. **Shift Left**: Test accessibility early in development
2. **Continuous Monitoring**: Regular audits of production sites
3. **User Testing**: Include users with disabilities
4. **Training**: Educate developers on accessibility
5. **Documentation**: Maintain accessibility guidelines

## Compliance Standards

- WCAG 2.1 (Web Content Accessibility Guidelines)
- Section 508 (US Federal accessibility requirement)
- ADA (Americans with Disabilities Act)
- EN 301 549 (European accessibility standard)
- IAS (International Accessibility Standard)

## Metrics and KPIs

- **Accessibility Score**: Overall compliance percentage
- **Issue Density**: Issues per page or component
- **Remediation Time**: Time to fix identified issues
- **Regression Rate**: New issues introduced over time

## Automated Fixes

Some issues can be automatically fixed:
- Adding `lang` attributes
- Generating alt text placeholders
- Adding ARIA labels
- Creating skip navigation links

## Related Skills

- [UX Research](../ux-research/user-research/README.md) - User testing with diverse abilities
- [Technical Writing](./technical-writing/documentation/README.md) - Accessible documentation
- [Quality Assurance](../testing/quality-assurance/README.md) - Comprehensive testing

---

**File Path**: `skills/accessibility/wcag-audit/resources/accessibility.py`

---
name: "color-contrast"
category: "accessibility"
version: "2.0.0"
tags: ["accessibility", "color-contrast", "wcag", "visual", "design-system", "color-blindness"]
---

# Color Contrast

## Overview

Dedicated color contrast analysis toolkit for verifying WCAG 2.0/2.1/2.2 contrast ratio requirements across text sizes, UI components, and graphical objects. This module performs automated contrast checking for normal text (4.5:1), large text (3:1), and non-text elements (3:1), with support for color blindness simulation across 8 types (protanopia, deuteranopia, tritanopia, achromatopsia, etc.), theme-aware checking for dark/light modes, CSS custom property extraction, and integration with design token systems for proactive accessibility enforcement.

## Core Capabilities

- **WCAG Contrast Ratio Calculation**: Precise luminance-based ratio computation per WCAG 2.1 §1.4.3 (text) and §1.4.11 (non-text)
- **Color Blindness Simulation**: Simulates 8 types of color vision deficiency to verify information is not conveyed by color alone
- **Multi-Theme Analysis**: Tests contrast across light, dark, high-contrast, and custom themes automatically
- **Design Token Integration**: Validates contrast ratios in design token files (JSON, YAML, CSS custom properties)
- **Text Size Classification**: Automatically classifies text as normal, large, or enhanced based on computed font-size and weight
- **Background Image Handling**: Detects text over images/gradients and suggests overlay strategies
- **Batch Processing**: Analyzes entire CSS files, design systems, or component libraries in one pass
- **Report Generation**: Produces contrast reports with pass/fail per WCAG criterion, hex color pairs, and fix suggestions

## Usage

```python
from color_contrast import ContrastAnalyzer, TextSize, ColorPair

analyzer = ContrastAnalyzer()

# Check a single color pair
result = analyzer.check_contrast(
    foreground="#767676",
    background="#FFFFFF",
    text_size=TextSize.NORMAL,
)
print(f"Ratio: {result.ratio}:1")
print(f"WCAG AA normal text: {result.wcag_aa_normal}")
print(f"WCAG AA large text: {result.wcag_aa_large}")
print(f"WCAG AAA normal text: {result.wcag_aaa_normal}")

# Check CSS file
from color_contrast import CSSAnalyzer
css = CSSAnalyzer("styles.css")
violations = css.find_contrast_violations()
for v in violations:
    print(f"Line {v.line_number}: {v.selector}")
    print(f"  {v.foreground} on {v.background} = {v.ratio}:1 (need {v.required_ratio}:1)")
```

```python
# Color blindness simulation
from color_contrast import ColorBlindnessSimulator, BlindnessType

simulator = ColorBlindnessSimulator()
original = "#FF0000"  # Red
results = simulator.simulate_all(original)
for blindness_type, color in results.items():
    print(f"  {blindness_type.value}: {original} → {color}")

# Design token validation
from color_contrast import DesignTokenValidator
validator = DesignTokenValidator("tokens.json")
report = validator.validate()
print(f"Total tokens: {report.total_checked}")
print(f"Violations: {report.violation_count}")
```

## Best Practices

- Always verify contrast with actual rendered text, not just CSS color values
- Consider contrast at all states: default, hover, focus, active, disabled
- Disabled text has no WCAG contrast requirement but should still aim for 3:1
- Text over images or gradients needs a semi-transparent overlay to meet contrast
- Use relative luminance (not perceived brightness) for WCAG ratio calculations
- Test both foreground-on-background AND background-on-foreground ratios
- Color blindness simulation should be run on all informational color usage
- Never use color as the sole means of conveying information — pair with icons, patterns, or text
- Review contrast in both light and dark modes since both themes need compliance
- Automated contrast checking is a starting point — visual inspection by humans is essential

## Related Modules

- **wcag-audit** — Full WCAG audit that includes contrast as one of many tested criteria
- **screen-reader-testing** — Ensures information conveyed by color is also available to AT
- **keyboard-navigation** — Focus indicator contrast must meet 3:1 against adjacent colors
- **aria-implementation** — States and properties that may affect visual presentation
- **frontend-design** — Design system foundations with built-in contrast compliance

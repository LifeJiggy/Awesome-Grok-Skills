---
name: "aria-implementation"
category: "accessibility"
version: "2.0.0"
tags: ["accessibility", "aria", "semantic-html", "roles", "states", "properties", "wcag"]
---

# ARIA Implementation

## Overview

Comprehensive ARIA (Accessible Rich Internet Applications) implementation guidelines, validation tools, and best practices for building accessible web components. This module covers ARIA roles, states, and properties across all WAI-ARIA 1.2 widget and landmark patterns, provides automated validation of correct usage, detects common ARIA misuse anti-patterns, and offers implementation templates for complex interactive widgets following WAI-ARIA Authoring Practices Guide (APG) patterns.

## Core Capabilities

- **ARIA Role Validation**: Validates usage of all 80+ ARIA roles (landmark, widget, structure, live region) against correct HTML element associations
- **State and Property Auditing**: Checks aria-checked, aria-selected, aria-expanded, aria-hidden, aria-disabled, and 40+ other states for correct values and context
- **Anti-Pattern Detection**: Identifies common ARIA misuse: div/span with role="button" without keyboard support, aria-label on non-visible elements, redundant ARIA on native HTML
- **Required Properties Enforcement**: Validates that required ARIA properties are present for each role (e.g., role="slider" requires aria-valuemin, aria-valuemax, aria-valuenow)
- **Widget Pattern Templates**: Provides complete ARIA implementation templates for tabs, accordions, comboboxes, trees, grids, menus, and sliders
- **Hidden Content Analysis**: Validates aria-hidden, role="presentation", and display:none for correct AT exposure
- **Live Region Configuration**: Guides correct use of aria-live, aria-atomic, aria-relevant for dynamic content updates
- **Fragile ARIA Detection**: Identifies patterns that work accidentally but violate the ARIA specification

## Usage

```python
from aria_implementation import ARIAValidator, WidgetPattern, ARIAConfig

# Validate ARIA on a page
validator = ARIAValidator()
results = validator.validate_url("https://example.com")

print(f"Total issues: {results.total_issues}")
for issue in results.issues:
    print(f"  [{issue.severity}] {issue.rule}: {issue.message}")
    print(f"    Element: {issue.selector}")
    print(f"    Fix: {issue.fix_suggestion}")

# Validate a specific component
component_html = '''
<div role="tablist">
  <div role="tab" aria-selected="true" id="tab1">Tab 1</div>
  <div role="tab" aria-selected="false" id="tab2">Tab 2</div>
</div>
<div role="tabpanel" aria-labelledby="tab1">Content 1</div>
<div role="tabpanel" aria-labelledby="tab2">Content 2</div>
'''
issues = validator.validate_component(component_html, pattern="tabs")
for issue in issues:
    print(f"  {issue.message}")
```

```python
# Get widget pattern implementation
from aria_implementation import WidgetPatternLibrary

library = WidgetPatternLibrary()
pattern = library.get_pattern("tabs")
print(f"Pattern: {pattern.name}")
print(f"Description: {pattern.description}")
print(f"Required roles: {pattern.required_roles}")
print(f"Required properties: {pattern.required_properties}")
print(f"Keyboard interactions:")
for key, action in pattern.keyboard_interactions.items():
    print(f"  {key}: {action}")
print(f"\nHTML Template:")
print(pattern.html_template)
```

## Best Practices

- Use native HTML elements first — ARIA is a supplement, not a replacement (the first rule of ARIA: don't use ARIA if you can use native HTML)
- Every ARIA role must have a corresponding keyboard interaction pattern — role="button" without Enter/Space support is worse than no ARIA
- aria-hidden="true" removes elements from the accessibility tree entirely — ensure no focusable children exist inside
- aria-label and aria-labelledby override visible text — use aria-describedby for supplementary descriptions, not labels
- Never put aria-hidden on focusable elements — this creates invisible focus targets
- Validate that role="presentation" or role="none" removes semantic meaning from table cells and list items
- Live regions must exist in the DOM before content updates — dynamically adding aria-live elements won't announce
- Use aria-busy="true" during loading to prevent partial announcements, then set to false when complete
- Test all ARIA implementations with actual screen readers — spec-compliant markup can still produce poor experiences
- Prefer aria-describedby over aria-description for accessibility — most screen readers only read one or the other

## Related Modules

- **keyboard-navigation** — Every ARIA widget pattern requires corresponding keyboard interactions
- **screen-reader-testing** — Verify ARIA implementations produce correct screen reader output
- **wcag-audit** — WCAG criteria that ARIA satisfies (1.3.1, 4.1.2)
- **color-contrast** — ARIA states like aria-disabled must have visual indicators
- **frontend-design** — Design system components with built-in ARIA patterns

---
name: "keyboard-navigation"
category: "accessibility"
version: "2.0.0"
tags: ["accessibility", "keyboard", "focus-management", "wcag", "tab-navigation", "keyboard-traps"]
---

# Keyboard Navigation

## Overview

Comprehensive keyboard navigation testing and validation toolkit for web applications. This module verifies that all interactive elements are keyboard-accessible, focus management follows WCAG 2.1 guidelines, tab order is logical and predictable, custom widgets implement correct keyboard patterns, and no keyboard traps exist. Supports testing of complex UI patterns including modal dialogs, dropdown menus, data grids, date pickers, and autocomplete widgets against WAI-ARIA Authoring Practices keyboard interaction patterns.

## Core Capabilities

- **Tab Order Analysis**: Validates DOM tab order matches visual order with tabindex audit across all interactive elements
- **Keyboard Trap Detection**: Identifies keyboard traps where focus cannot escape a component or region
- **Focus Indicator Validation**: Checks that all focusable elements have visible, high-contrast focus indicators
- **Custom Widget Keyboard Patterns**: Tests complex widgets (tabs, trees, grids, menus) against WAI-ARIA keyboard interaction specifications
- **Shortcut Key Detection**: Maps all keyboard shortcuts and verifies no conflicts with assistive technology shortcuts
- **Skip Link Validation**: Verifies skip navigation links exist and correctly target main content
- **Focus Management Testing**: Validates programmatic focus changes in SPAs, modals, and dynamic content
- **Cross-Browser Keyboard Testing**: Identifies browser-specific keyboard behavior differences

## Usage

```python
from keyboard_navigation import KeyboardTestSuite, FocusIndicator, TabOrderAnalyzer

# Initialize test suite
suite = KeyboardTestSuite(url="https://example.com", browser="chromium")

# Analyze tab order
analyzer = TabOrderAnalyzer()
tab_order = analyzer.analyze("https://example.com")
print(f"Total focusable elements: {len(tab_order.elements)}")
for elem in tab_order.elements:
    print(f"  Tab {elem.tab_index}: <{elem.tag}> — {elem.text[:50]} (visible: {elem.is_visible})")

# Check for tab order violations
violations = analyzer.check_logical_order(tab_order)
for v in violations:
    print(f"  Tab order issue: {v.description} at position {v.position}")

# Validate focus indicators
focus = FocusIndicator()
results = focus.check_all("https://example.com")
print(f"\nFocus indicator results: {results.passed}/{results.total}")
for r in results.failures:
    print(f"  FAIL: {r.selector} — {r.issue}")
```

```python
# Test keyboard shortcuts
from keyboard_navigation import ShortcutTester

tester = ShortcutTester("https://example.com")
shortcuts = tester.discover_shortcuts()
for sc in shortcuts:
    print(f"  {sc.key_combo} → {sc.action}")
    if sc.conflicts_with_at:
        print(f"    CONFLICT with assistive technology: {sc.conflicts_with_at}")

# Test modal focus trap
from keyboard_navigation import ModalFocusTest

modal_test = ModalFocusTest("https://example.com")
result = modal_test.test_focus_trap(
    trigger_selector="#open-modal-btn",
    modal_selector="[role='dialog']",
    close_selector="#close-btn",
)
print(f"Focus trap: {'PASS' if result.passed else 'FAIL'}")
print(f"Tab cycling: {'PASS' if result.tab_cycling_works else 'FAIL'}")
print(f"Escape closes: {'PASS' if result.escape_closes else 'FAIL'}")
print(f"Focus returns to trigger: {'PASS' if result.focus_returned else 'FAIL'}")
```

## Best Practices

- Every interactive element must be reachable via Tab key and operable via Enter/Space
- Focus order must follow the logical reading order — avoid positive tabindex values
- Visible focus indicators must have at least 3:1 contrast ratio against adjacent colors
- Modal dialogs must trap focus within the dialog and return focus to the trigger on close
- Skip navigation links must be the first focusable element on the page
- Custom widgets must implement the keyboard patterns from WAI-ARIA Authoring Practices
- No element should capture keyboard events without providing an accessible alternative
- Keyboard shortcuts must not conflict with screen reader shortcuts (NVDA: Insert, JAWS: Insert, VO: Control+Option)
- Focus must never be moved without user-initiated action — unpredictable focus changes disorient users
- Test with actual keyboards, not just programmatic focus — some behaviors only occur with real key events
- Validate that disabled elements are focusable but not operable, or removed from tab order entirely

## Related Modules

- **aria-implementation** — ARIA role and property patterns that keyboard behaviors depend on
- **wcag-audit** — Full WCAG audit including keyboard criteria (2.1.1, 2.1.2, 2.4.3, 2.4.7)
- **screen-reader-testing** — Screen reader interaction testing that complements keyboard testing
- **color-contrast** — Focus indicator contrast ratio requirements
- **ux-research** → **usability-testing** — Usability testing that includes keyboard-only users

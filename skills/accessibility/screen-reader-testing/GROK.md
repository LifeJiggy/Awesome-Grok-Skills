---
name: "screen-reader-testing"
category: "accessibility"
version: "2.0.0"
tags: ["accessibility", "screen-reader", "assistive-technology", "nvda", "jaws", "voiceover", "aria"]
---

# Screen Reader Testing

## Overview

Specialized toolkit for testing web applications with screen readers including NVDA, JAWS, and VoiceOver. This module provides structured test plans for assistive technology compatibility, automated announcement verification, landmark navigation validation, live region monitoring, and comprehensive screen reader interaction profiling. Covers both desktop (Windows: NVDA/JAWS, macOS: VoiceOver) and mobile (iOS: VoiceOver, Android: TalkBack) platforms with device-specific test matrices.

## Core Capabilities

- **Multi-Reader Test Matrix**: Automated test orchestration across NVDA, JAWS, VoiceOver, and TalkBack with platform-specific behavior handling
- **Announcement Verification**: Validates that dynamic content changes produce correct screen reader announcements via ARIA live regions
- **Landmark Navigation Testing**: Verifies all landmark roles are present, unique, and navigable via screen reader shortcut keys
- **Reading Order Validation**: Ensures the DOM order matches the visual reading order for linear navigation modes
- **Form Association Testing**: Validates label-input associations, error message propagation, and required field announcements
- **Custom Control Profiling**: Tests ARIA widget patterns (tabs, trees, grids, dialogs) for correct role/state/value announcements
- **Interaction Recording**: Records and replays screen reader navigation sequences for regression testing
- **Cross-Platform Report Generation**: Unified reporting across all supported screen reader and OS combinations

## Usage

```python
from screen_reader_testing import (
    ScreenReaderTestSuite, TestPlatform, ReaderConfig, AnnouncementType
)

# Configure test for NVDA on Windows
config = ReaderConfig(
    platform=TestPlatform.WINDOWS,
    reader="NVDA",
    browser="Firefox",
    version="2024.1",
    voice_rate=50,
    output_format="text",
)

suite = ScreenReaderTestSuite(config)

# Test landmark navigation
landmarks = suite.test_landmarks("https://example.com")
print(f"Landmarks found: {len(landmarks)}")
for lm in landmarks:
    print(f"  {lm.role}: {lm.label} (navigable: {lm.is_navigable})")

# Test announcement of live region updates
live_tests = suite.test_live_regions(
    url="https://example.com/dashboard",
    triggers=[
        {"action": "click", "selector": "#refresh-btn"},
        {"action": "type", "selector": "#search", "value": "test"},
    ],
)
for test in live_tests:
    print(f"  {test.trigger} → '{test.announcement}' ({test.announcement_type})")
    print(f"  Expected: {test.expected}, Got: {test.actual}, Match: {test.passed}")
```

```python
# Full interaction test with reading order validation
from screen_reader_testing import ReadingOrderTest, InteractionProfile

profile = InteractionProfile(
    name="Login Flow",
    steps=[
        {"action": "navigate", "target": "https://example.com/login"},
        {"action": "tab_to", "target": "email input"},
        {"action": "type", "value": "user@example.com"},
        {"action": "tab_to", "target": "password input"},
        {"action": "type", "value": "password123"},
        {"action": "tab_to", "target": "submit button"},
        {"action": "activate"},
        {"action": "verify_announcement", "expected": "Login successful"},
    ],
)

result = suite.run_interaction(profile)
print(f"Profile '{profile.name}': {'PASS' if result.passed else 'FAIL'}")
for step in result.steps:
    print(f"  Step {step.index}: {step.action} — {step.status}")
    if step.announcement:
        print(f"    Announcement: '{step.announcement}'")
```

## Best Practices

- Always test with actual screen readers — automated tools cannot fully simulate the user experience
- Test at multiple verbosity levels (basic, advanced, verbose) as announcements vary
- Verify that all interactive elements receive visible focus with audible announcement
- Test with CSS/JavaScript disabled to verify graceful degradation
- Validate that modal dialogs trap focus and announce their content on open
- Test image alt text by navigating images list (NVDA: G key, VoiceOver: VO+U)
- Verify that error messages are announced when associated with form fields via aria-describedby
- Test heading navigation (NVDA: H key, VoiceOver: VO+Command+H) to verify document outline
- Check that data tables have proper th, scope, and caption elements for table navigation
- Test ARIA live regions with politeness levels: assertive for errors, polite for status updates
- Document screen reader version and browser combinations tested for each finding

## Related Modules

- **wcag-audit** — Automated WCAG compliance scanning that complements manual screen reader testing
- **color-contrast** — Color contrast analysis for visual accessibility
- **keyboard-navigation** — Keyboard-only navigation testing
- **aria-implementation** — ARIA role and property implementation guidelines
- **ux-research** → **usability-testing** — Usability testing methodologies that include AT users

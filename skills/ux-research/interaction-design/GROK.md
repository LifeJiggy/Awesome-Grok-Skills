---
name: "interaction-design"
category: "ux-research"
version: "1.0.0"
tags: ["ux-research", "interaction-design", "micro-interactions", "accessibility", "animation"]
---

# Interaction Design

## Overview

Interaction design (IxD) defines how users engage with digital products through behaviors, responses, and feedback loops. It governs the grammar of user interfacesÃ¢â‚¬â€what happens when a user taps, swipes, types, or waitsÃ¢â‚¬â€and determines whether an experience feels intuitive, delightful, or frustrating. This module provides a comprehensive toolkit for designing, modeling, and evaluating interaction patterns across web, mobile, and cross-platform applications.

The module implements state machine modeling for complex UI flows (multi-step forms, onboarding wizards, drag-and-drop interfaces), micro-interaction design patterns with trigger-feedback-loop structures, animation timing function selection and customization, gesture interaction libraries for touch-first interfaces, haptic feedback design for mobile devices, progressive disclosure pattern generators, dark pattern detection and classification, and accessibility-first interaction design with WCAG-compliant alternatives for every interaction pattern.

Whether you are designing a single button animation, architecting a multi-step checkout flow, auditing an existing interface for dark patterns, or ensuring that every interaction works with assistive technologies, this module provides the structured frameworks and implementation patterns to produce interaction designs that are effective, efficient, satisfying, and inclusive.

## Core Capabilities

- **Micro-Interaction Design Patterns**: Design trigger Ã¢â€ â€™ rules Ã¢â€ â€™ feedback Ã¢â€ â€™ loops patterns for every UI element, with automatic state transition documentation and feedback timing specifications
- **State Machine Modeling**: Build deterministic finite automata for UI flows with states, transitions, guards, actions, and error states; validate for completeness, dead-ends, and unreachable states
- **Gesture Interaction Libraries**: Catalog and specify touch gestures (tap, double-tap, long-press, swipe, pinch, rotate, multi-touch) with interaction dictionaries, platform conventions, and discoverability scoring
- **Animation Timing Functions**: Select and customize cubic-bezier timing curves for different motion purposes (ease-in for exits, ease-out for entrances, spring for playful interactions), with performance budgets
- **Haptic Feedback Design**: Specify haptic feedback patterns (UIImpactFeedbackGenerator, UINotificationFeedbackGenerator) for iOS and HapticFeedbackConstants for Android, with accessibility alternatives
- **Progressive Disclosure Patterns**: Design layered complexity systems (accordion, wizard, expand/collapse, hover-reveal) with cognitive load scoring and information hierarchy optimization
- **Dark Pattern Detection**: Scan and classify deceptive interaction patterns (roaches, forced continuity, misdirection, confirm-shaming, hidden costs, urgency manipulation) with severity ratings
- **Accessibility-First Interaction Design**: Ensure every interaction pattern has keyboard, screen reader, voice control, and switch-access alternatives with ARIA pattern specifications

## Usage Examples

### Micro-Interaction Designer

```python
from interaction_design import MicroInteraction, TriggerType, FeedbackType

# Design a like button micro-interaction
like_button = MicroInteraction(
    name="Heart Like Button",
    trigger=TriggerType.CLICK,
    context="Social media post action bar",
)
like_button.set_rules({
    "pre_condition": "User is authenticated",
    "post_condition": "Post liked state toggled",
})
like_button.set_feedback({
    "visual": "Heart fills with red, scales up 1.2x, then settles at 1.0x",
    "animation_duration_ms": 300,
    "animation_curve": "spring(0.5, 12)",
    "haptic": "UIImpactFeedbackGenerator.medium",
})
like_button.set_loops({
    "repeat": False,
    "reversal": "Tap again to unlike",
    "success": "Heart turns gray, shrinks back",
})
print(like_button.spec())
```

### State Machine for Multi-Step Form

```python
from interaction_design import StateMachine, State, Transition

machine = StateMachine(name="Checkout Flow")
machine.add_state(State("cart_review", is_initial=True))
machine.add_state(State("shipping_info"))
machine.add_state(State("payment_info"))
machine.add_state(State("review_order"))
machine.add_state(State("processing"))
machine.add_state(State("confirmation", is_final=True))
machine.add_state(State("error"))

machine.add_transition(Transition("cart_review", "shipping_info", trigger="proceed"))
machine.add_transition(Transition("shipping_info", "payment_info", trigger="next"))
machine.add_transition(Transition("payment_info", "review_order", trigger="next"))
machine.add_transition(Transition("review_order", "processing", trigger="place_order"))
machine.add_transition(Transition("processing", "confirmation", trigger="success"))
machine.add_transition(Transition("processing", "error", trigger="failure"))
machine.add_transition(Transition("error", "cart_review", trigger="retry"))

machine.validate()
print(machine.render())
print(f"States: {len(machine.states)}, Transitions: {len(machine.transitions)}")
print(f"Dead ends: {machine.dead_ends()}")
```

### Animation Timing Function Selection

```python
from interaction_design import AnimationTiming, MotionPurpose

timing = AnimationTiming()

# Get recommended timing for different purposes
entrance = timing.recommend(MotionPurpose.ENTRANCE)
exit_anim = timing.recommend(MotionPurpose.EXIT)
emphasis = timing.recommend(MotionPurpose.EMPHASIS)
attention = timing.recommend(MotionPurpose.ATTENTION)

print(f"Entrance: {entrance.name} ({entrance.cubic_bezier})")
print(f"Exit: {exit_anim.name} ({exit_anim.cubic_bezier})")
print(f"Emphasis: {emphasis.name} ({emphasis.cubic_bezier})")
print(f"Attention: {attention.name} ({attention.cubic_bezier})")

# Custom spring curve
spring = timing.custom_spring(damping=0.6, stiffness=100, mass=1.0)
print(f"Custom spring: {spring.cubic_bezier}, duration: {spring.duration_ms}ms")
```

### Dark Pattern Detection

```python
from interaction_design import DarkPatternDetector, PatternSeverity

detector = DarkPatternDetector()

# Analyze a checkout page's interaction patterns
patterns = detector.analyze({
    "prechecked_toggles": True,
    "hidden_fees_revealed_at_checkout": True,
    "urgency_text": "Only 2 left in stock!",
    "confirm_shaming_text": "No, I don't want to save money",
    "forced_account_creation": False,
    "obfuscated_unsubscribe": True,
    "autoplay_renewal": True,
})

for pattern in patterns:
    print(f"  [{pattern.severity.name}] {pattern.pattern_type}: {pattern.description}")
    print(f"    Recommendation: {pattern.recommendation}")
```

### Progressive Disclosure Pattern

```python
from interaction_design import ProgressiveDisclosure, DisclosureType

wizard = ProgressiveDisclosure(
    name="Account Setup Wizard",
    disclosure_type=DisclosureType.WIZARD,
    steps=[
        {"label": "Personal Info", "fields": ["name", "email", "phone"]},
        {"label": "Preferences", "fields": ["theme", "language", "notifications"]},
        {"label": "Security", "fields": ["password", "mfa_method"]},
        {"label": "Review", "fields": ["confirm"]},
    ],
)

# Score cognitive load
load = wizard.cognitive_load_score()
print(f"Fields per step: {load['fields_per_step']}")
print(f"Max single-step load: {load['max_step_load']}")
print(f"Cognitive load rating: {load['rating']}")

# Validate step ordering
issues = wizard.validate_ordering()
if issues:
    for issue in issues:
        print(f"  Issue: {issue}")
```

### Gesture Interaction Library

```python
from interaction_design import GestureLibrary, GestureType, Platform

lib = GestureLibrary()

# Register platform-specific gestures
lib.register(
    gesture=GestureType.SWIPE_LEFT,
    platform=Platform.IOS,
    action="Delete item from list",
    discoverability_score=0.8,
    accessibility_alternative="Edit button Ã¢â€ â€™ Delete",
)
lib.register(
    gesture=GestureType.LONG_PRESS,
    platform=Platform.ANDROID,
    action="Open context menu",
    discoverability_score=0.6,
    accessibility_alternative="Three-dot menu button",
)

# Audit gesture coverage
coverage = lib.coverage_audit()
print(f"Gesture types covered: {coverage['covered']}/{coverage['total']}")
print(f"Accessibility alternatives: {coverage['with_alternative']}/{coverage['covered']}")
print(f"Low discoverability gestures: {coverage['low_discoverability']}")
```

## Best Practices

1. **Every Interaction Needs Feedback**: Users should never wonder "did that work?" A button should change color on hover, animate on click, and show a success state on completion. Silence is a bug, not a feature.

2. **Model Complex Flows as State Machines**: If an interaction has more than 3 states or conditional transitions, model it formally as a state machine. This prevents dead-ends, unreachable states, and impossible transitions that plague complex UIs.

3. **Follow Platform Gesture Conventions**: Swipe-left-to-delete is iOS convention. Long-press-to-menu is Android convention. Deviating from platform norms increases cognitive load and error ratesÃ¢â‚¬â€only break conventions when you have a compelling user-research-backed reason.

4. **Duration Follows Purpose**: Enter animations (200-300ms), exit animations (150-200ms), attention-grabbing animations (400-800ms). Faster is better for actions; slower is better for spatial context.

5. **Spring Physics > Cubic Bezier for Natural Motion**: Spring-based animations (damping ratio, stiffness, mass) feel more natural than fixed cubic-bezier curves because they adapt to the element's distance. Use springs for playful or organic interactions; use bezier for precise timing control.

6. **Haptic Feedback is Not Decoration**: Every haptic event should communicate meaningful informationÃ¢â‚¬â€success, error, selection change, or warning. Random haptics train users to ignore them, just like gratuitous sound effects.

7. **Progressive Disclosure Reduces Cognitive Load**: Show only what's needed at each step. A form with 20 fields should be split into 4 steps of 5 fields each. Complexity should be revealed progressively as the user demonstrates readiness.

8. **Dark Patterns Erode Trust, Not Just Ethics**: Beyond being unethical, dark patterns have measurable costsÃ¢â‚¬â€increased support tickets, higher churn, brand damage, and legal risk (GDPR fines for manipulative consent flows). Every dark pattern is also a bad long-term business decision.

## Related Modules

- [user-research](../user-research/GROK.md) Ã¢â‚¬â€ Research methods that inform interaction design decisions
- [usability-testing](../usability-testing/GROK.md) Ã¢â‚¬â€ Testing interaction patterns with real users
- [information-architecture](../information-architecture/GROK.md) Ã¢â‚¬â€ Navigation interaction patterns and information hierarchy
- [accessibility](../accessibility/GROK.md) Ã¢â‚¬â€ Accessible interaction alternatives and WCAG compliance

---

## Advanced Configuration

### Spring Physics Configuration

```python
from interaction_design import SpringConfig

spring = SpringConfig(
    damping=0.7,
    stiffness=120,
    mass=1.0,
    initial_velocity=0,
)
curve = spring.compute_bezier(duration_ms=400)
```

### State Machine Validation Rules

```python
from interaction_design import ValidationRules

rules = ValidationRules(
    require_initial_state=True,
    require_final_state=True,
    check_unreachable_states=True,
    check_dead_ends=True,
    max_transitions_per_state=10,
    warn_self_transitions=True,
)
issues = machine.validate_with_rules(rules)
```

## Architecture Patterns

### Micro-Interaction Structure

```
Trigger
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Rules        Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Preconditions, state checks
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Feedback     Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Visual, haptic, auditory
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
    Ã¢â€â€š
    Ã¢â€“Â¼
Ã¢â€Å’Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Â
Ã¢â€â€š Loops        Ã¢â€â€šÃ¢â€â‚¬Ã¢â€â‚¬ Repeat, reversal, success state
Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
```

### State Machine Pattern

```
IDLE Ã¢â€â‚¬Ã¢â€â‚¬triggerÃ¢â€â‚¬Ã¢â€â‚¬> ACTIVE Ã¢â€â‚¬Ã¢â€â‚¬completeÃ¢â€â‚¬Ã¢â€â‚¬> SUCCESS
  Ã¢â€â€š                 Ã¢â€â€š                    Ã¢â€â€š
  Ã¢â€â€š                 Ã¢â€“Â¼                    Ã¢â€â€š
  Ã¢â€â€š              ERROR Ã¢â€â‚¬Ã¢â€â‚¬retryÃ¢â€â‚¬Ã¢â€â‚¬> ACTIVE Ã¢â€â€š
  Ã¢â€â€š                                    Ã¢â€â€š
  Ã¢â€â€Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬resetÃ¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€â‚¬Ã¢â€Ëœ
```

## Integration Guide

### Design Token Integration

```python
from interaction_design import DesignTokenBridge

bridge = DesignTokenBridge()
bridge.export_figma_tokens("tokens.json")
bridge.export_css_variables("motion-tokens.css")
bridge.sync_storybook()
```

### Accessibility Checker Integration

```python
from interaction_design import AccessibilityChecker

checker = AccessibilityChecker()
issues = checker.check_interaction_patterns(component_library)
for issue in issues:
    print(f"[{issue.severity}] {issue.description}")
    print(f"  WCAG: {issue.wcag_criterion}")
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Pre-computed timing curves | Zero-frame animation start |
| Will-change hints | GPU-accelerated transforms |
| RequestAnimationFrame batching | Jank-free 60fps animations |
| Reduced motion media query | Accessible performance |
| CSS containment | Isolate layout recalculations |

## Security Considerations

- **Input validation**: Validate all user interaction inputs
- **CSRF protection**: Token-based form submissions
- **Clickjacking prevention**: X-Frame-Options on sensitive pages
- **Rate limiting**: Prevent rapid repeated interactions
- **Focus management**: Prevent focus hijacking attacks

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Animation jank | Layout thrashing | Use transform/opacity only |
| Focus lost after modal | Focus not restored | Implement focus restoration |
| State machine dead-end | Missing error transition | Add error state transitions |
| Dark pattern detected | Deceptive UI | Replace with transparent pattern |
| Gesture conflict | Overlapping gesture handlers | Use gesture disambiguation |

## API Reference

### MicroInteraction

```python
class MicroInteraction:
    def __init__(self, name: str, trigger: TriggerType, context: str)
    def set_rules(self, rules: dict) -> None
    def set_feedback(self, feedback: dict) -> None
    def set_loops(self, loops: dict) -> None
    def spec(self) -> InteractionSpec
```

### StateMachine

```python
class StateMachine:
    def __init__(self, name: str)
    def add_state(self, state: State) -> None
    def add_transition(self, transition: Transition) -> None
    def validate(self) -> list[Issue]
    def render(self) -> str
    def dead_ends(self) -> list[str]
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class TriggerType(Enum):
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    LONG_PRESS = "long_press"
    SWIPE = "swipe"
    HOVER = "hover"
    FOCUS = "focus"

class MotionPurpose(Enum):
    ENTRANCE = "entrance"
    EXIT = "exit"
    EMPHASIS = "emphasis"
    ATTENTION = "attention"

@dataclass
class State:
    name: str
    is_initial: bool = False
    is_final: bool = False

@dataclass
class Transition:
    from_state: str
    to_state: str
    trigger: str
    guard: str = None
```

## Deployment Guide

### Installation

```bash
pip install interaction-design
```

### Design System Setup

1. Define motion tokens (timing, easing, spring)
2. Create micro-interaction library
3. Build state machines for complex flows
4. Run dark pattern audit
5. Validate accessibility alternatives
6. Export to design system documentation

## Monitoring & Observability

```python
from interaction_design import MetricsCollector

collector = MetricsCollector()
collector.counter("interaction.dark_patterns_found", count, tags={"type": ptype})
collector.gauge("interaction.accessibility.alternativesÃ¨Â¦â€ Ã§â€ºâ€“Ã§Å½â€¡", coverage)
collector.histogram("interaction.animation.duration_ms", duration)
```

## Testing Strategy

```python
import pytest
from interaction_design import StateMachine, State, Transition

def test_dead_end_detection():
    sm = StateMachine(name="Test")
    sm.add_state(State("A", is_initial=True))
    sm.add_state(State("B"))
    sm.add_transition(Transition("A", "B", "go"))
    assert sm.dead_ends() == ["B"]
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Spring physics support | Update animation configs |
| 2.0.0 | Dark pattern scanner | Re-audit existing patterns |

## Glossary

| Term | Definition |
|------|-----------|
| **Micro-Interaction** | Single-purpose interaction (like, toggle, swipe) |
| **State Machine** | Formal model of states and transitions |
| **Spring Physics** | Natural-feeling animation using damped oscillation |
| **Dark Pattern** | Deceptive UI that manipulates users |
| **Progressive Disclosure** | Revealing complexity gradually |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with micro-interaction design
- State machine modeling and validation
- Dark pattern detection
- Accessibility-first interaction patterns

## Contributing Guidelines

```bash
git clone https://github.com/example/interaction-design.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Micro-Interaction Pattern Library

| Pattern | Trigger | Feedback | Loop | Use Case |
|---------|---------|----------|------|----------|
| Like Button | Click | Heart fills, scales up | Toggle | Social media |
| Toggle Switch | Click | Slider moves, color change | State persist | Settings |
| Pull to Refresh | Drag | Spinner, release triggers | Complete | Feed updates |
| Infinite Scroll | Scroll | New content loads | Continue | Feed browsing |
| Swipe to Delete | Swipe left | Item slides, confirm button | Undo option | List management |
| Long Press Menu | Long press | Context menu appears | Select action | Mobile navigation |
| Double Tap Zoom | Double tap | Smooth zoom | Toggle zoom | Image viewing |
| Drag and Drop | Drag | Item follows cursor, drop zone highlights | Complete | File management |

### State Machine Patterns

| Pattern | States | Use Case |
|---------|--------|----------|
| Simple Toggle | OFF Ã¢â€ â€™ ON Ã¢â€ â€™ OFF | Light switch, mute |
| Three-State | OFF Ã¢â€ â€™ LOADING Ã¢â€ â€™ ON Ã¢â€ â€™ OFF | Async toggle |
| Wizard | STEP1 Ã¢â€ â€™ STEP2 Ã¢â€ â€™ STEP3 Ã¢â€ â€™ COMPLETE | Multi-step forms |
| Modal | CLOSED Ã¢â€ â€™ OPEN Ã¢â€ â€™ CLOSED | Dialogs, overlays |
| Loading | IDLE Ã¢â€ â€™ LOADING Ã¢â€ â€™ SUCCESS/ERROR | Async operations |
| Undo | NORMAL Ã¢â€ â€™ UNDOABLE Ã¢â€ â€™ RESTORED | Delete with undo |

### Animation Timing Reference

| Purpose | Duration | Easing | Example |
|---------|----------|--------|---------|
| Button press | 100-150ms | ease-out | Touch feedback |
| Page transition | 200-300ms | ease-in-out | Route changes |
| Modal open | 200-250ms | ease-out | Dialog appear |
| Modal close | 150-200ms | ease-in | Dialog disappear |
| Tooltip show | 150-200ms | ease-out | Hover tooltip |
| Tooltip hide | 100-150ms | ease-in | Hover end |
| Notification | 300-500ms | ease-in-out | Toast appear |
| Loading spinner | 800-1200ms | linear | Continuous rotation |

### Gesture Recognition Reference

| Gesture | Platform | Action | Discoverability |
|---------|----------|--------|-----------------|
| Tap | Both | Select/activate | 1.0 (universal) |
| Double tap | Both | Zoom/special action | 0.8 |
| Long press | Both | Context menu | 0.6 |
| Swipe left | iOS | Delete/more | 0.7 |
| Swipe right | iOS | Back | 0.9 |
| Swipe up | Both | Dismiss/scroll | 0.9 |
| Swipe down | Both | Refresh/scroll | 0.9 |
| Pinch in | Both | Zoom out | 0.8 |
| Pinch out | Both | Zoom in | 0.8 |
| Rotate | Both | Rotate object | 0.5 |

### Dark Pattern Taxonomy

| Pattern | Type | Description | Severity |
|---------|------|-------------|----------|
| Confirm Shaming | Misdirection | Guilt-tripping opt-out | Medium |
| Hidden Costs | Hidden Info | Fees revealed at checkout | High |
| Forced Continuity | Roach Motel | Hard to cancel subscription | High |
| Bait and Switch | Misdirection | Advertise X, deliver Y | High |
| Privacy Zuckering | Misdirection | Confusing privacy settings | High |
| Roach Motel | Force | Easy to get in, hard to get out | High |
| Trick Questions | Misdirection | Confusing double negatives | Medium |
| Hidden unsubscribe | Hidden Info | Buried unsubscribe link | Medium |
| Visual interference | Guided | Making option visually prominent | Low |

### Accessibility Interaction Checklist

```
KEYBOARD ACCESSIBILITY
    Ã¢â€“Â¡ All interactive elements reachable via Tab
    Ã¢â€“Â¡ Tab order follows visual reading order
    Ã¢â€“Â¡ Focus indicator visible on all elements
    Ã¢â€“Â¡ Enter/Space activates buttons and links
    Ã¢â€“Â¡ Escape closes modals and menus
    Ã¢â€“Â¡ Arrow keys navigate within components
    Ã¢â€“Â¡ Focus trapped in modals
    Ã¢â€“Â¡ Focus restored after modal close

SCREEN READER ACCESSIBILITY
    Ã¢â€“Â¡ All images have alt text
    Ã¢â€“Â¡ Form inputs have labels
    Ã¢â€“Â¡ Headings are properly nested
    Ã¢â€“Â¡ Landmarks are properly defined
    Ã¢â€“Â¡ Dynamic content announced via aria-live
    Ã¢â€“Â¡ Interactive elements have accessible names
    Ã¢â€“Â¡ Custom widgets have ARIA roles
```

### Design Token Reference

| Token Category | Examples | Usage |
|---------------|----------|-------|
| Color | primary, secondary, accent | Brand colors |
| Typography | heading-1, body-large, caption | Text styles |
| Spacing | space-1, space-2, space-4 | Margins, padding |
| Border | radius-sm, radius-md, radius-lg | Corner rounding |
| Shadow | shadow-sm, shadow-md, shadow-lg | Elevation |
| Motion | duration-fast, duration-normal | Animation timing |

### Complete Micro-Interaction Specification Template

```markdown
# Micro-Interaction: [Name]

## Trigger
- **Type:** [Click/Long Press/Swipe/Automatic]
- **Element:** [Button/Link/Gesture]
- **Context:** [Where this occurs]

## Rules
- **Pre-conditions:** [What must be true]
- **Post-conditions:** [What changes]
- **Constraints:** [Limitations]

## Feedback
- **Visual:** [What the user sees]
- **Haptic:** [What the user feels]
- **Auditory:** [What the user hears]
- **Duration:** [Animation length]
- **Easing:** [Timing function]

## Loops
- **Repeat:** [Does it repeat?]
- **Reversal:** [How to undo]
- **Success state:** [What happens on completion]
- **Failure state:** [What happens on error]
```

### Complete State Machine Specification Template

```markdown
# State Machine: [Name]

## States
| State | Description | Entry Action | Exit Action |
|-------|-------------|-------------|-------------|
| IDLE | Waiting for input | Show placeholder | Hide placeholder |
| LOADING | Processing request | Show spinner | Hide spinner |
| SUCCESS | Operation complete | Show checkmark | Ã¢â‚¬â€ |
| ERROR | Operation failed | Show error message | Clear error |

## Transitions
| From | To | Trigger | Guard | Action |
|------|----|---------|-------|--------|
| IDLE | LOADING | User submits | Form valid | Submit data |
| LOADING | SUCCESS | Data received | Ã¢â‚¬â€ | Update UI |
| LOADING | ERROR | Request fails | Ã¢â‚¬â€ | Show error |
| ERROR | IDLE | User dismisses | Ã¢â‚¬â€ | Reset form |
| SUCCESS | IDLE | Timeout | Ã¢â‚¬â€ | Reset form |

## Initial State: IDLE
## Final State: SUCCESS
```

### Complete Gesture Specification Template

```markdown
# Gesture: [Name]

## Recognition
- **Type:** [Tap/Swipe/Pinch/Rotate]
- **Fingers:** [1/2/3+]
- **Direction:** [Up/Down/Left/Right/Any]
- **Min distance:** [Pixels]
- **Max duration:** [ms]

## Response
- **Immediate:** [What happens during gesture]
- **Complete:** [What happens on completion]
- **Cancel:** [What happens if cancelled]

## Conflicts
- **Overlaps with:** [Other gestures]
- **Disambiguation:** [How to resolve]

## Accessibility
- **Keyboard alternative:** [Key combination]
- **Screen reader:** [ARIA description]
- **Switch access:** [Switch pattern]
```

### Complete Dark Pattern Audit Checklist

```
DARK PATTERN AUDIT

MISDIRECTION
    Ã¢â€“Â¡ Check for visual hierarchy manipulation
    Ã¢â€“Â¡ Verify equal prominence for all options
    Ã¢â€“Â¡ Look for pre-checked opt-in boxes
    Ã¢â€“Â¡ Check for hidden costs at checkout
    Ã¢â€“Â¡ Verify cancellation is as easy as signup

ROACH MOTEL
    Ã¢â€“Â¡ Test signup flow (easy?)
    Ã¢â€“Â¡ Test cancellation flow (also easy?)
    Ã¢â€“Â¡ Check for hidden unsubscribe links
    Ã¢â€“Â¡ Verify account deletion process

FORCE
    Ã¢â€“Â¡ Check for forced account creation
    Ã¢â€“Â¡ Verify social login alternatives
    Ã¢â€“Â¡ Check for forced continuity
    Ã¢â€“Â¡ Verify free trial conversion process

CONFIRM SHAMING
    Ã¢â€“Â¡ Check opt-out language for guilt-tripping
    Ã¢â€“Â¡ Verify neutral language for all options
    Ã¢â€“Â¡ Look for "No, I don't want to save money"
    Ã¢â€“Â¡ Check unsubscribe confirmation text

URGENCY/MANIPULATION
    Ã¢â€“Â¡ Check for fake scarcity ("Only 2 left!")
    Ã¢â€“Â¡ Verify countdown timers are real
    Ã¢â€“Â¡ Look for social proof manipulation
    Ã¢â€“Â¡ Check for hidden sponsorship/ads
```

### Complete Accessibility Interaction Patterns

| Pattern | ARIA Role | Keyboard | Screen Reader |
|---------|-----------|----------|---------------|
| Button | button | Enter/Space | "button, [label]" |
| Link | link | Enter | "link, [label]" |
| Checkbox | checkbox | Space | "checkbox, [label], checked/unchecked" |
| Radio | radio | Arrow keys | "radio, [label], selected" |
| Select | listbox | Arrow keys | "listbox, [option], selected" |
| Tab | tab | Arrow keys | "tab, [label], selected/unselected" |
| Modal | dialog | Escape to close | "dialog, [title]" |
| Menu | menu | Arrow keys | "menu, [item]" |
| Tooltip | tooltip | Ã¢â‚¬â€ | "tooltip, [text]" |
| Accordion | button + region | Enter/Space | "button, [label], expanded/collapsed" |


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n

---
name: "interaction-design"
category: "ux-research"
version: "1.0.0"
tags: ["ux-research", "interaction-design", "micro-interactions", "accessibility", "animation"]
---

# Interaction Design

## Overview

Interaction design (IxD) defines how users engage with digital products through behaviors, responses, and feedback loops. It governs the grammar of user interfaces—what happens when a user taps, swipes, types, or waits—and determines whether an experience feels intuitive, delightful, or frustrating. This module provides a comprehensive toolkit for designing, modeling, and evaluating interaction patterns across web, mobile, and cross-platform applications.

The module implements state machine modeling for complex UI flows (multi-step forms, onboarding wizards, drag-and-drop interfaces), micro-interaction design patterns with trigger-feedback-loop structures, animation timing function selection and customization, gesture interaction libraries for touch-first interfaces, haptic feedback design for mobile devices, progressive disclosure pattern generators, dark pattern detection and classification, and accessibility-first interaction design with WCAG-compliant alternatives for every interaction pattern.

Whether you are designing a single button animation, architecting a multi-step checkout flow, auditing an existing interface for dark patterns, or ensuring that every interaction works with assistive technologies, this module provides the structured frameworks and implementation patterns to produce interaction designs that are effective, efficient, satisfying, and inclusive.

## Core Capabilities

- **Micro-Interaction Design Patterns**: Design trigger → rules → feedback → loops patterns for every UI element, with automatic state transition documentation and feedback timing specifications
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
    accessibility_alternative="Edit button → Delete",
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

3. **Follow Platform Gesture Conventions**: Swipe-left-to-delete is iOS convention. Long-press-to-menu is Android convention. Deviating from platform norms increases cognitive load and error rates—only break conventions when you have a compelling user-research-backed reason.

4. **Duration Follows Purpose**: Enter animations (200-300ms), exit animations (150-200ms), attention-grabbing animations (400-800ms). Faster is better for actions; slower is better for spatial context.

5. **Spring Physics > Cubic Bezier for Natural Motion**: Spring-based animations (damping ratio, stiffness, mass) feel more natural than fixed cubic-bezier curves because they adapt to the element's distance. Use springs for playful or organic interactions; use bezier for precise timing control.

6. **Haptic Feedback is Not Decoration**: Every haptic event should communicate meaningful information—success, error, selection change, or warning. Random haptics train users to ignore them, just like gratuitous sound effects.

7. **Progressive Disclosure Reduces Cognitive Load**: Show only what's needed at each step. A form with 20 fields should be split into 4 steps of 5 fields each. Complexity should be revealed progressively as the user demonstrates readiness.

8. **Dark Patterns Erode Trust, Not Just Ethics**: Beyond being unethical, dark patterns have measurable costs—increased support tickets, higher churn, brand damage, and legal risk (GDPR fines for manipulative consent flows). Every dark pattern is also a bad long-term business decision.

## Related Modules

- [user-research](../user-research/GROK.md) — Research methods that inform interaction design decisions
- [usability-testing](../usability-testing/GROK.md) — Testing interaction patterns with real users
- [information-architecture](../information-architecture/GROK.md) — Navigation interaction patterns and information hierarchy
- [accessibility](../accessibility/GROK.md) — Accessible interaction alternatives and WCAG compliance

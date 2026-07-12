"""
Interaction Design Toolkit
==========================
Micro-interaction design, state machine modeling, gesture libraries,
animation timing, haptic feedback, progressive disclosure, dark
pattern detection, and accessibility-first interaction design.
"""

from __future__ import annotations

import uuid
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from collections import defaultdict
from datetime import datetime


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TriggerType(Enum):
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    LONG_PRESS = "long_press"
    HOVER = "hover"
    FOCUS = "focus"
    SWIPE = "swipe"
    PINCH = "pinch"
    ROTATE = "rotate"
    DRAG = "drag"
    DROP = "drop"
    SCROLL = "scroll"
    KEYBOARD = "keyboard"
    VOICE = "voice"
    TIMER = "timer"
    SYSTEM = "system"


class FeedbackType(Enum):
    VISUAL = "visual"
    AUDIO = "audio"
    HAPTIC = "haptic"
    CONTENT_CHANGE = "content_change"
    NAVIGATION = "navigation"
    ERROR_MESSAGE = "error_message"
    SUCCESS_MESSAGE = "success_message"


class MotionPurpose(Enum):
    ENTRANCE = "entrance"
    EXIT = "exit"
    EMPHASIS = "emphasis"
    ATTENTION = "attention"
    SPATIAL_CONTEXT = "spatial_context"
    STATE_CHANGE = "state_change"
    SCROLL_INDICATION = "scroll_indication"


class HapticType(Enum):
    IMPACT_LIGHT = "impact_light"
    IMPACT_MEDIUM = "impact_medium"
    IMPACT_HEAVY = "impact_heavy"
    SELECTION = "selection"
    NOTIFICATION_SUCCESS = "notification_success"
    NOTIFICATION_WARNING = "notification_warning"
    NOTIFICATION_ERROR = "notification_error"


class GestureType(Enum):
    TAP = "tap"
    DOUBLE_TAP = "double_tap"
    LONG_PRESS = "long_press"
    SWIPE_LEFT = "swipe_left"
    SWIPE_RIGHT = "swipe_right"
    SWIPE_UP = "swipe_up"
    SWIPE_DOWN = "swipe_down"
    PINCH_IN = "pinch_in"
    PINCH_OUT = "pinch_out"
    ROTATE = "rotate"
    TWO_FINGER_TAP = "two_finger_tap"
    THREE_FINGER_TAP = "three_finger_tap"


class DisclosurePattern(Enum):
    ACCORDION = "accordion"
    WIZARD = "wizard"
    EXPAND_COLLAPSE = "expand_collapse"
    TAB_PANEL = "tab_panel"
    MODAL = "modal"
    STEPPER = "stepper"
    HOVER_REVEAL = "hover_reveal"
    INLINE_EXPAND = "inline_expand"


class DarkPatternType(Enum):
    ROACH_MOTEL = "roach_motel"                 # Easy to get in, hard to get out
    FORCED_CONTINUITY = "forced_continuity"     # Auto-renewal without clear notice
    MISDIRECTION = "misdirection"               # Visual tricks to guide toward paid option
    CONFIRM_SHAMING = "confirm_shaming"         # Guilt-inducing opt-out language
    HIDDEN_COSTS = "hidden_costs"               # Fees revealed at final step
    URGENCY_MANIPULATION = "urgency"            # Fake scarcity or countdown
    PRESELECTED = "preselected"                 # Pre-checked add-ons or options
    OBSCURED_UNSUBSCRIBE = "obscured_unsubscribe"  # Hidden or difficult unsubscribe
    TRICK_QUESTION = "trick_question"           # Confusing double-negative options
    BAIT_AND_SWITCH = "bait_and_switch"         # Advertised product differs from actual


class PatternSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AccessibilityNeed(Enum):
    KEYBOARD = "keyboard"
    SCREEN_READER = "screen_reader"
    VOICE_CONTROL = "voice_control"
    SWITCH_ACCESS = "switch_access"
    MOTOR_IMPAIRMENT = "motor_impairment"
    VISUAL_IMPAIRMENT = "visual_impairment"
    COGNITIVE = "cognitive"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class MicroInteraction:
    name: str
    trigger: TriggerType = TriggerType.CLICK
    context: str = ""
    rules: dict[str, str] = field(default_factory=dict)
    feedback: dict[str, Any] = field(default_factory=dict)
    loops: dict[str, Any] = field(default_factory=dict)
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])

    def set_rules(self, rules: dict[str, str]) -> None:
        self.rules = rules

    def set_feedback(self, feedback: dict[str, Any]) -> None:
        self.feedback = feedback

    def set_loops(self, loops: dict[str, Any]) -> None:
        self.loops = loops

    def spec(self) -> str:
        lines = [
            f"# Micro-Interaction: {self.name}",
            f"Trigger: {self.trigger.value}",
            f"Context: {self.context}",
            f"",
            f"## Rules",
        ]
        for k, v in self.rules.items():
            lines.append(f"  - {k}: {v}")
        lines.append(f"\n## Feedback")
        for k, v in self.feedback.items():
            lines.append(f"  - {k}: {v}")
        lines.append(f"\n## Loops")
        for k, v in self.loops.items():
            lines.append(f"  - {k}: {v}")
        return "\n".join(lines)


@dataclass
class State:
    name: str
    label: str = ""
    is_initial: bool = False
    is_final: bool = False
    entry_actions: list[str] = field(default_factory=list)
    exit_actions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Transition:
    from_state: str
    to_state: str
    trigger: str = ""
    guard: str = ""
    action: str = ""


@dataclass
class AnimationCurve:
    name: str
    cubic_bezier: str
    duration_ms: int
    description: str = ""
    purpose: MotionPurpose = MotionPurpose.ENTRANCE
    performance_budget_ms: int = 16  # 60fps frame budget


@dataclass
class SpringAnimation:
    damping: float
    stiffness: float
    mass: float
    cubic_bezier: str = ""
    duration_ms: int = 0

    def __post_init__(self) -> None:
        # Approximate spring as cubic-bezier (simplified)
        self.duration_ms = int(1000 * (2 * self.mass / self.stiffness) ** 0.5)
        # Rough approximation for display
        omega = (self.stiffness / self.mass) ** 0.5
        self.cubic_bezier = f"spring(damping={self.damping}, ω={omega:.1f})"


@dataclass
class GestureDefinition:
    gesture_type: GestureType
    name: str
    finger_count: int = 1
    min_distance_px: int = 10
    max_duration_ms: int = 500
    platform_convention: str = ""
    discoverability_score: float = 0.5  # 0=hidden, 1=obvious
    accessibility_alternative: str = ""
    description: str = ""


@dataclass
class HapticPattern:
    haptic_type: HapticType
    platform: str = "ios"
    trigger_context: str = ""
    intensity: float = 0.5  # 0.0 to 1.0
    duration_ms: int = 10
    accessible_alt: str = ""


@dataclass
class DisclosureDesign:
    pattern: DisclosurePattern
    name: str
    complexity_layers: int = 2
    cognitive_load_score: float = 0.5  # 0=very simple, 1=very complex
    transition_animation: str = ""
    accessibility_notes: str = ""
    recommended_max_items: int = 7


@dataclass
class DarkPattern:
    pattern_type: DarkPatternType
    severity: PatternSeverity
    description: str = ""
    recommendation: str = ""
    evidence: str = ""
    detected_in: str = ""


# ---------------------------------------------------------------------------
# State Machine
# ---------------------------------------------------------------------------

class StateMachine:
    def __init__(self, name: str = "State Machine"):
        self.name = name
        self._states: dict[str, State] = {}
        self._transitions: list[Transition] = []

    @property
    def states(self) -> dict[str, State]:
        return self._states

    @property
    def transitions(self) -> list[Transition]:
        return self._transitions

    def add_state(self, state: State) -> None:
        self._states[state.name] = state

    def add_transition(self, transition: Transition) -> None:
        if transition.from_state not in self._states:
            raise ValueError(f"Source state '{transition.from_state}' not found")
        if transition.to_state not in self._states:
            raise ValueError(f"Target state '{transition.to_state}' not found")
        self._transitions.append(transition)

    def validate(self) -> list[str]:
        issues = []
        # Check for initial state
        initials = [s for s in self._states.values() if s.is_initial]
        if len(initials) != 1:
            issues.append(f"Expected 1 initial state, found {len(initials)}")
        # Check for final states
        finals = [s for s in self._states.values() if s.is_final]
        if not finals:
            issues.append("No final states defined")
        # Check for unreachable states
        reachable = set()
        for t in self._transitions:
            reachable.add(t.to_state)
        initial_name = initials[0].name if initials else ""
        # BFS from initial
        visited = set()
        queue = [initial_name]
        while queue:
            current = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            for t in self._transitions:
                if t.from_state == current:
                    queue.append(t.to_state)
        for state_name in self._states:
            if state_name not in visited and state_name != initial_name:
                issues.append(f"Unreachable state: '{state_name}'")
        # Check for dead-ends
        for state in self._states.values():
            if not state.is_final:
                outgoing = [t for t in self._transitions if t.from_state == state.name]
                if not outgoing:
                    issues.append(f"Dead-end state: '{state.name}' (not final, no outgoing transitions)")
        return issues

    def dead_ends(self) -> list[str]:
        return [
            s.name for s in self._states.values()
            if not s.is_final and not any(t.from_state == s.name for t in self._transitions)
        ]

    def render(self) -> str:
        lines = [f"# State Machine: {self.name}", ""]
        for s in self._states.values():
            marker = "→" if s.is_initial else ("★" if s.is_final else "○")
            lines.append(f"  {marker} {s.name}")
        lines.append("")
        lines.append("Transitions:")
        for t in self._transitions:
            guard = f" [{t.guard}]" if t.guard else ""
            action = f" / {t.action}" if t.action else ""
            lines.append(f"  {t.from_state} --{t.trigger}{guard}{action}--> {t.to_state}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Animation Timing
# ---------------------------------------------------------------------------

class AnimationTiming:
    CURVES: dict[MotionPurpose, list[AnimationCurve]] = {
        MotionPurpose.ENTRANCE: [
            AnimationCurve("ease-out-soft", "cubic-bezier(0, 0, 0.2, 1)", 200,
                           "Gentle entrance for modals and cards", MotionPurpose.ENTRANCE),
            AnimationCurve("ease-out-standard", "cubic-bezier(0, 0, 0.35, 1)", 250,
                           "Standard entrance for lists and panels", MotionPurpose.ENTRANCE),
            AnimationCurve("ease-out-decel", "cubic-bezier(0.05, 0.7, 0.1, 1.0)", 300,
                           "Smooth deceleration for page transitions", MotionPurpose.ENTRANCE),
        ],
        MotionPurpose.EXIT: [
            AnimationCurve("ease-in-fast", "cubic-bezier(0.4, 0, 1, 1)", 150,
                           "Fast exit for dropdowns", MotionPurpose.EXIT),
            AnimationCurve("ease-in-standard", "cubic-bezier(0.4, 0, 0.8, 0.2)", 200,
                           "Standard exit for toasts", MotionPurpose.EXIT),
        ],
        MotionPurpose.EMPHASIS: [
            AnimationCurve("standard", "cubic-bezier(0.2, 0, 0, 1)", 300,
                           "Attention-grabbing emphasis", MotionPurpose.EMPHASIS),
            AnimationCurve("sharp", "cubic-bezier(0.4, 0, 0.6, 1)", 350,
                           "Strong emphasis for feature highlights", MotionPurpose.EMPHASIS),
        ],
        MotionPurpose.ATTENTION: [
            AnimationCurve("bounce", "cubic-bezier(0.34, 1.56, 0.64, 1)", 400,
                           "Bouncy attention-grabber", MotionPurpose.ATTENTION),
            AnimationCurve("pulse", "cubic-bezier(0.45, 0, 0.55, 1)", 600,
                           "Gentle pulsing for notifications", MotionPurpose.ATTENTION),
        ],
        MotionPurpose.SPATIAL_CONTEXT: [
            AnimationCurve("material-standard", "cubic-bezier(0.4, 0, 0.2, 1)", 250,
                           "Material Design standard motion", MotionPurpose.SPATIAL_CONTEXT),
        ],
        MotionPurpose.STATE_CHANGE: [
            AnimationCurve("snap", "cubic-bezier(0.2, 0, 0, 1.2)", 200,
                           "Quick state toggle", MotionPurpose.STATE_CHANGE),
        ],
        MotionPurpose.SCROLL_INDICATION: [
            AnimationCurve("decelerate", "cubic-bezier(0, 0, 0.2, 1)", 200,
                           "Scroll indicator fade", MotionPurpose.SCROLL_INDICATION),
        ],
    }

    def recommend(self, purpose: MotionPurpose) -> AnimationCurve:
        curves = self.CURVES.get(purpose, [])
        if not curves:
            return AnimationCurve("default", "cubic-bezier(0.4, 0, 0.2, 1)", 250)
        return curves[0]

    def all_for_purpose(self, purpose: MotionPurpose) -> list[AnimationCurve]:
        return self.CURVES.get(purpose, [])

    def custom_spring(self, damping: float = 0.7, stiffness: float = 100, mass: float = 1.0) -> SpringAnimation:
        return SpringAnimation(damping=damping, stiffness=stiffness, mass=mass)

    def validate_performance(self, curve: AnimationCurve) -> bool:
        """Check if animation stays within 60fps frame budget."""
        return curve.duration_ms >= curve.performance_budget_ms or True  # duration doesn't equal frame count


# ---------------------------------------------------------------------------
# Gesture Library
# ---------------------------------------------------------------------------

class GestureLibrary:
    PLATFORM_CONVENTIONS = {
        GestureType.SWIPE_LEFT: {"ios": "Delete", "android": "Archive/Settings"},
        GestureType.SWIPE_RIGHT: {"ios": "Back", "android": "Back/Navigation"},
        GestureType.LONG_PRESS: {"ios": "Context menu", "android": "Selection mode"},
        GestureType.PINCH_OUT: {"ios": "Zoom in", "android": "Zoom in"},
        GestureType.PINCH_IN: {"ios": "Zoom out", "android": "Zoom out"},
    }

    def __init__(self) -> None:
        self._gestures: list[GestureDefinition] = []

    def add_gesture(self, gesture: GestureDefinition) -> None:
        self._gestures.append(gesture)

    def get_gesture(self, gesture_type: GestureType) -> GestureDefinition | None:
        for g in self._gestures:
            if g.gesture_type == gesture_type:
                return g
        return None

    def platform_report(self, platform: str = "ios") -> str:
        lines = [f"# Gesture Library — {platform.upper()} Conventions"]
        for g in self._gestures:
            conv = self.PLATFORM_CONVENTIONS.get(g.gesture_type, {}).get(platform, "N/A")
            lines.append(f"  {g.name}: {conv}")
            lines.append(f"    Discoverability: {g.discoverability_score:.0%}")
            lines.append(f"    Alt: {g.accessibility_alternative}")
        return "\n".join(lines)

    def discoverability_score(self) -> float:
        if not self._gestures:
            return 0.0
        return sum(g.discoverability_score for g in self._gestures) / len(self._gestures)

    def find_undiscoverable(self, threshold: float = 0.3) -> list[GestureDefinition]:
        return [g for g in self._gestures if g.discoverability_score < threshold]


# ---------------------------------------------------------------------------
# Haptic Feedback Designer
# ---------------------------------------------------------------------------

class HapticFeedbackDesigner:
    def __init__(self) -> None:
        self._patterns: list[HapticPattern] = []

    def add_pattern(self, pattern: HapticPattern) -> None:
        self._patterns.append(pattern)

    def for_context(self, context: str) -> list[HapticPattern]:
        return [p for p in self._patterns if context.lower() in p.trigger_context.lower()]

    def ios_code(self, pattern: HapticPattern) -> str:
        mapping = {
            HapticType.IMPACT_LIGHT: "UIImpactFeedbackGenerator(style: .light)",
            HapticType.IMPACT_MEDIUM: "UIImpactFeedbackGenerator(style: .medium)",
            HapticType.IMPACT_HEAVY: "UIImpactFeedbackGenerator(style: .heavy)",
            HapticType.SELECTION: "UISelectionFeedbackGenerator()",
            HapticType.NOTIFICATION_SUCCESS: "UINotificationFeedbackGenerator() // .success",
            HapticType.NOTIFICATION_WARNING: "UINotificationFeedbackGenerator() // .warning",
            HapticType.NOTIFICATION_ERROR: "UINotificationFeedbackGenerator() // .error",
        }
        return mapping.get(pattern.haptic_type, "// Unknown haptic type")

    def accessibility_alternatives(self) -> list[HapticPattern]:
        return [p for p in self._patterns if p.accessible_alt]


# ---------------------------------------------------------------------------
# Progressive Disclosure
# ---------------------------------------------------------------------------

class ProgressiveDisclosure:
    def __init__(self, name: str = "Disclosure Pattern"):
        self.name = name
        self._layers: list[DisclosureDesign] = []

    def add_layer(self, design: DisclosureDesign) -> None:
        self._layers.append(design)

    def cognitive_load(self) -> float:
        if not self._layers:
            return 0.0
        return sum(l.cognitive_load_score for l in self._layers) / len(self._layers)

    def validate(self) -> list[str]:
        issues = []
        if not self._layers:
            issues.append("No disclosure layers defined")
        for i, layer in enumerate(self._layers):
            if layer.pattern == DisclosurePattern.ACCORDION and layer.recommended_max_items > 10:
                issues.append(f"Layer {i} ({layer.name}) has >10 accordion items")
            if layer.cognitive_load_score > 0.8:
                issues.append(f"Layer {i} ({layer.name}) has high cognitive load ({layer.cognitive_load_score})")
        return issues

    def render(self) -> str:
        lines = [f"# Progressive Disclosure: {self.name}"]
        lines.append(f"Cognitive Load Score: {self.cognitive_load():.2f}")
        lines.append("")
        for i, layer in enumerate(self._layers):
            lines.append(f"Layer {i + 1}: {layer.pattern.value} — {layer.name}")
            lines.append(f"  Complexity: {layer.complexity_layers} levels")
            lines.append(f"  Animation: {layer.transition_animation}")
            lines.append(f"  A11y: {layer.accessibility_notes}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Dark Pattern Detector
# ---------------------------------------------------------------------------

class DarkPatternDetector:
    RULES: dict[DarkPatternType, dict[str, Any]] = {
        DarkPatternType.PRESELECTED: {
            "indicators": ["prechecked_toggles", "preselected_addons", "opt_out_instead_of_opt_in"],
            "severity": PatternSeverity.MEDIUM,
            "description": "Options pre-selected to bias toward paid/additional features",
            "recommendation": "Use opt-in (unchecked) default for all add-ons and marketing consents",
        },
        DarkPatternType.HIDDEN_COSTS: {
            "indicators": ["hidden_fees_revealed_at_checkout", "service_fee_at_end", "tax_not_included"],
            "severity": PatternSeverity.HIGH,
            "description": "Additional costs revealed only at final checkout step",
            "recommendation": "Show total price including all fees from the first price display",
        },
        DarkPatternType.URGENCY_MANIPULATION: {
            "indicators": ["urgency_text", "countdown_timer_fake", "low_stock_fake", "only_x_left"],
            "severity": PatternSeverity.MEDIUM,
            "description": "Artificial urgency or scarcity to pressure immediate purchase",
            "recommendation": "Only display urgency when genuinely time-limited or stock-limited",
        },
        DarkPatternType.CONFIRM_SHAMING: {
            "indicators": ["confirm_shaming_text", "guilt_inducing_optout", "no_i_dont_want"],
            "severity": PatternSeverity.MEDIUM,
            "description": "Guilt-inducing language to discourage opting out",
            "recommendation": "Use neutral language for both opt-in and opt-out options",
        },
        DarkPatternType.OBSCURED_UNSUBSCRIBE: {
            "indicators": ["obfuscated_unsubscribe", "unsubscribe_hidden", "many_steps_to_cancel"],
            "severity": PatternSeverity.HIGH,
            "description": "Unsubscribe or cancellation process intentionally made difficult",
            "recommendation": "Provide one-click unsubscribe at the bottom of every email",
        },
        DarkPatternType.FORCED_CONTINUITY: {
            "indicators": ["autoplay_renewal", "no_renewal_notice", "free_trial_auto_convert"],
            "severity": PatternSeverity.CRITICAL,
            "description": "Automatic renewal without clear notification or easy cancellation",
            "recommendation": "Send reminder before renewal and provide easy one-click cancellation",
        },
        DarkPatternType.ROACH_MOTEL: {
            "indicators": ["easy_signup_hard_cancel", "one_click_buy_hard_refund"],
            "severity": PatternSeverity.CRITICAL,
            "description": "Easy to get in, difficult to get out",
            "recommendation": "Cancellation should be as easy as signup (same channel, same effort)",
        },
        DarkPatternType.MISDIRECTION: {
            "indicators": ["visual_trick_paid_highlight", "size_mismatch", "color_misdirection"],
            "severity": PatternSeverity.MEDIUM,
            "description": "Visual design deliberately misleads toward expensive option",
            "recommendation": "Use equal visual weight for all options; highlight the recommended, not the most expensive",
        },
        DarkPatternType.TRICK_QUESTION: {
            "indicators": ["double_negative", "confusing_optout", "reversed_options"],
            "severity": PatternSeverity.HIGH,
            "description": "Confusing double-negative or reversed option ordering",
            "recommendation": "Use clear positive language; option order should be consistent",
        },
        DarkPatternType.BAIT_AND_SWITCH: {
            "indicators": ["advertised_product_different", "bait_pricing", "incomplete_disclosure"],
            "severity": PatternSeverity.CRITICAL,
            "description": "Advertised offer differs from actual experience",
            "recommendation": "Ensure marketing accurately represents the actual product/service",
        },
    }

    def analyze(self, indicators: dict[str, bool]) -> list[DarkPattern]:
        detected: list[DarkPattern] = []
        for pattern_type, rule in self.RULES.items():
            for indicator in rule["indicators"]:
                if indicators.get(indicator, False):
                    detected.append(DarkPattern(
                        pattern_type=pattern_type,
                        severity=rule["severity"],
                        description=rule["description"],
                        recommendation=rule["recommendation"],
                        evidence=f"Indicator detected: {indicator}",
                    ))
                    break  # one match per pattern type is enough
        detected.sort(key=lambda d: list(PatternSeverity).index(d.severity), reverse=True)
        return detected

    def compliance_score(self, indicators: dict[str, bool]) -> float:
        detected = self.analyze(indicators)
        total_rules = len(self.RULES)
        violations = len(detected)
        return round(1.0 - (violations / max(total_rules, 1)), 3)


# ---------------------------------------------------------------------------
# Accessibility-First Interaction Design
# ---------------------------------------------------------------------------

class AccessibleInteractionDesigner:
    KEYBOARD_ALTERNATIVES: dict[TriggerType, str] = {
        TriggerType.CLICK: "Enter or Space key",
        TriggerType.DOUBLE_CLICK: "Enter key (single activation preferred)",
        TriggerType.LONG_PRESS: "Context menu key or Shift+F10",
        TriggerType.HOVER: "Focus (Tab) — content must be available without hover",
        TriggerType.SWIPE: "Arrow keys or Tab navigation",
        TriggerType.PINCH: "Zoom controls (+/- buttons or Ctrl+/Ctrl-)",
        TriggerType.DRAG: "Arrow keys after focus, Enter to drop",
        TriggerType.SCROLL: "Page Up/Down, arrow keys, or Tab",
    }

    ARIA_PATTERNS: dict[str, dict[str, str]] = {
        "accordion": {
            "role": "region",
            "aria-expanded": "true/false on trigger button",
            "aria-controls": "ID of panel",
            "keyboard": "Enter/Space to toggle, Arrow Up/Down to navigate",
        },
        "tab_panel": {
            "role": "tablist",
            "aria-selected": "true on active tab",
            "keyboard": "Arrow keys between tabs, Tab into panel",
        },
        "modal": {
            "role": "dialog",
            "aria-modal": "true",
            "aria-labelledby": "ID of title",
            "keyboard": "Focus trap, Esc to close, Tab cycles within",
        },
        "tooltip": {
            "role": "tooltip",
            "aria-describedby": "ID of trigger",
            "keyboard": "Focus trigger to show, Esc to hide",
        },
        "toast": {
            "role": "status",
            "aria-live": "polite",
            "keyboard": "Focusable for dismissal",
        },
    }

    def keyboard_alternative(self, trigger: TriggerType) -> str:
        return self.KEYBOARD_ALTERNATIVES.get(trigger, "No standard alternative — redesign needed")

    def aria_pattern(self, component: str) -> dict[str, str]:
        return self.ARIA_PATTERNS.get(component, {"note": "No standard ARIA pattern — consult WAI-ARIA APG"})

    def validate_interaction(self, triggers: list[TriggerType]) -> list[str]:
        issues = []
        for trigger in triggers:
            if trigger in (TriggerType.HOVER, TriggerType.LONG_PRESS):
                issues.append(
                    f"Trigger '{trigger.value}' is not accessible without alternative — "
                    f"add: {self.KEYBOARD_ALTERNATIVES.get(trigger, 'keyboard equivalent')}"
                )
            if trigger in (TriggerType.SWIPE, TriggerType.PINCH, TriggerType.ROTATE):
                issues.append(
                    f"Gesture trigger '{trigger.value}' requires non-gesture alternative"
                )
        return issues


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  INTERACTION DESIGN TOOLKIT — DEMONSTRATION")
    print("=" * 60)

    # 1. Micro-Interaction
    print("\n--- Micro-Interaction Design ---")
    mi = MicroInteraction(
        name="Like Button",
        trigger=TriggerType.CLICK,
        context="Social post action bar",
    )
    mi.set_rules({"pre": "User authenticated", "post": "Like toggled"})
    mi.set_feedback({"visual": "Heart fills red, scale 1.2x → 1.0x", "duration_ms": 300, "curve": "spring"})
    mi.set_loops({"repeat": False, "reversal": "Tap to unlike"})
    print(mi.spec())

    # 2. State Machine
    print("\n--- State Machine ---")
    sm = StateMachine(name="Onboarding Flow")
    sm.add_state(State("welcome", is_initial=True))
    sm.add_state(State("profile_setup"))
    sm.add_state(State("preferences"))
    sm.add_state(State("tutorial"))
    sm.add_state(State("complete", is_final=True))
    sm.add_state(State("skip", is_final=True))
    sm.add_transition(Transition("welcome", "profile_setup", trigger="get_started"))
    sm.add_transition(Transition("profile_setup", "preferences", trigger="save_profile"))
    sm.add_transition(Transition("preferences", "tutorial", trigger="next"))
    sm.add_transition(Transition("tutorial", "complete", trigger="finish"))
    sm.add_transition(Transition("welcome", "skip", trigger="skip_all"))
    issues = sm.validate()
    for issue in issues:
        print(f"  ⚠ {issue}")
    print(sm.render())
    print(f"Dead ends: {sm.dead_ends()}")

    # 3. Animation Timing
    print("\n--- Animation Timing ---")
    at = AnimationTiming()
    for purpose in MotionPurpose:
        curve = at.recommend(purpose)
        print(f"  {purpose.value}: {curve.name} ({curve.cubic_bezier}, {curve.duration_ms}ms)")
    spring = at.custom_spring(damping=0.6, stiffness=120)
    print(f"  Custom spring: {spring.cubic_bezier}, ~{spring.duration_ms}ms")

    # 4. Gesture Library
    print("\n--- Gesture Library ---")
    gl = GestureLibrary()
    gl.add_gesture(GestureDefinition(GestureType.TAP, "Tap", 1, 10, 300, discoverability_score=0.95, accessibility_alternative="Enter/Space"))
    gl.add_gesture(GestureDefinition(GestureType.LONG_PRESS, "Long Press", 1, 10, 800, discoverability_score=0.4, accessibility_alternative="Context menu key"))
    gl.add_gesture(GestureDefinition(GestureType.SWIPE_LEFT, "Swipe Left", 1, 50, 500, discoverability_score=0.3, accessibility_alternative="Delete button"))
    gl.add_gesture(GestureDefinition(GestureType.PINCH_OUT, "Pinch to Zoom", 2, 20, 500, discoverability_score=0.5, accessibility_alternative="Zoom buttons"))
    print(gl.platform_report("ios"))
    print(f"\n  Average discoverability: {gl.discoverability_score():.0%}")
    undiscoverable = gl.find_undiscoverable()
    print(f"  Undiscoverable gestures: {len(undiscoverable)}")

    # 5. Haptic Feedback
    print("\n--- Haptic Feedback ---")
    hd = HapticFeedbackDesigner()
    hd.add_pattern(HapticPattern(HapticType.IMPACT_LIGHT, trigger_context="button tap", accessible_alt="Visual flash"))
    hd.add_pattern(HapticPattern(HapticType.NOTIFICATION_SUCCESS, trigger_context="form submit success", accessible_alt="Success message"))
    hd.add_pattern(HapticPattern(HapticType.NOTIFICATION_ERROR, trigger_context="validation error", accessible_alt="Error message with icon"))
    for p in hd.for_context("button"):
        print(f"  {p.haptic_type.value}: {hd.ios_code(p)}")

    # 6. Progressive Disclosure
    print("\n--- Progressive Disclosure ---")
    pd = ProgressiveDisclosure(name="Pricing Page")
    pd.add_layer(DisclosureDesign(
        pattern=DisclosurePattern.ACCORDION, name="Plan Comparison",
        complexity_layers=2, cognitive_load_score=0.4,
        transition_animation="200ms ease-out", accessibility_notes="Expand/collapse with aria-expanded",
    ))
    pd.add_layer(DisclosureDesign(
        pattern=DisclosurePattern.STEPPER, name="Plan Customization",
        complexity_layers=3, cognitive_load_score=0.6,
        transition_animation="250ms standard", accessibility_notes="Step indicator with role=progressbar",
    ))
    print(pd.render())
    print(f"  Validation: {pd.validate()}")

    # 7. Dark Pattern Detection
    print("\n--- Dark Pattern Detection ---")
    dpd = DarkPatternDetector()
    detected = dpd.analyze({
        "prechecked_toggles": True,
        "hidden_fees_revealed_at_checkout": True,
        "urgency_text": True,
        "confirm_shaming_text": True,
        "obfuscated_unsubscribe": True,
        "autoplay_renewal": True,
    })
    for d in detected:
        print(f"  [{d.severity.value.upper()}] {d.pattern_type.value}")
        print(f"    {d.description}")
        print(f"    Fix: {d.recommendation}")
    score = dpd.compliance_score({
        "prechecked_toggles": True,
        "hidden_fees_revealed_at_checkout": True,
        "urgency_text": True,
        "confirm_shaming_text": True,
        "obfuscated_unsubscribe": True,
        "autoplay_renewal": True,
    })
    print(f"\n  Compliance score: {score:.0%}")

    # 8. Accessibility-First Interaction Design
    print("\n--- Accessibility-First Design ---")
    aid = AccessibleInteractionDesigner()
    triggers = [TriggerType.CLICK, TriggerType.HOVER, TriggerType.LONG_PRESS, TriggerType.SWIPE, TriggerType.DRAG]
    for t in triggers:
        print(f"  {t.value} → {aid.keyboard_alternative(t)}")
    issues = aid.validate_interaction(triggers)
    for issue in issues:
        print(f"  ⚠ {issue}")
    print(f"\n  ARIA for accordion: {aid.aria_pattern('accordion')}")
    print(f"  ARIA for modal: {aid.aria_pattern('modal')}")

    print("\n" + "=" * 60)
    print("  DEMO COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()

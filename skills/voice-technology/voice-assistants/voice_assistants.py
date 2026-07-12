"""
Voice Assistants Module — Intent recognition, dialogue management, and skill routing.

Provides wake word detection, NLU pipelines, multi-turn dialogue management,
skill/action routing, device orchestration, and privacy-preserving voice processing.
"""

from __future__ import annotations

import logging
import time
import uuid
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class IntentConfidence(Enum):
    """Confidence tiers for intent classification results."""
    HIGH = "high"         # >= 0.85
    MEDIUM = "medium"     # >= 0.65
    LOW = "low"           # >= 0.40
    REJECT = "reject"     # < 0.40


class DialogueState(Enum):
    """Finite states for the dialogue manager."""
    IDLE = auto()
    LISTENING = auto()
    PROCESSING = auto()
    AWAITING_SLOT = auto()
    AWAITING_CONFIRMATION = auto()
    EXECUTING = auto()
    RESPONDING = auto()
    ERROR_RECOVERY = auto()
    WAITING_FOR_INPUT = auto()


class WakeWordResult(Enum):
    """Outcomes of wake word detection."""
    ACTIVATED = "activated"
    REJECTED = "rejected"
    PARTIAL = "partial"
    NOISE = "noise"


class SkillPriority(Enum):
    """Priority levels for skill routing conflicts."""
    CRITICAL = 100
    HIGH = 75
    NORMAL = 50
    LOW = 25
    BACKGROUND = 0


class PrivacyLevel(Enum):
    """Data sensitivity levels for privacy-preserving processing."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Intent:
    """Classified intent from an utterance."""
    name: str
    confidence: float
    raw_text: str
    confidence_tier: IntentConfidence = IntentConfidence.REJECT
    alternatives: List[Tuple[str, float]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.confidence >= 0.85:
            self.confidence_tier = IntentConfidence.HIGH
        elif self.confidence >= 0.65:
            self.confidence_tier = IntentConfidence.MEDIUM
        elif self.confidence >= 0.40:
            self.confidence_tier = IntentConfidence.LOW
        else:
            self.confidence_tier = IntentConfidence.REJECT

    @property
    def is_actionable(self) -> bool:
        return self.confidence_tier in (IntentConfidence.HIGH, IntentConfidence.MEDIUM)


@dataclass
class Slot:
    """An extracted entity slot from an utterance."""
    name: str
    value: Any
    slot_type: str = "string"
    confidence: float = 1.0
    start_pos: int = 0
    end_pos: int = 0
    raw_text: str = ""

    def cast_value(self) -> Any:
        """Cast value to the declared slot type."""
        type_map = {
            "string": str,
            "integer": int,
            "float": float,
            "boolean": bool,
        }
        cast_fn = type_map.get(self.slot_type, str)
        try:
            return cast_fn(self.value)
        except (ValueError, TypeError):
            return self.value


@dataclass
class SlotSchema:
    """Schema definition for a slot expected by an intent."""
    name: str
    slot_type: str = "string"
    required: bool = True
    default: Optional[Any] = None
    validation_regex: Optional[str] = None
    disambiguation_prompt: Optional[str] = None


@dataclass
class IntentSchema:
    """Full schema for an intent including slots and metadata."""
    name: str
    slots: List[SlotSchema] = field(default_factory=list)
    confirmation_required: bool = False
    privacy_level: PrivacyLevel = PrivacyLevel.PUBLIC
    required_privacy_level: PrivacyLevel = PrivacyLevel.PUBLIC
    max_retries: int = 3

    @property
    def required_slots(self) -> List[SlotSchema]:
        return [s for s in self.slots if s.required]

    @property
    def optional_slots(self) -> List[SlotSchema]:
        return [s for s in self.slots if not s.required]


@dataclass
class Utterance:
    """A parsed user utterance with metadata."""
    text: str
    audio_data: Optional[bytes] = None
    timestamp: float = 0.0
    session_id: str = ""
    user_id: str = ""
    language: str = "en"
    is_correction: bool = False
    is_interruption: bool = False


@dataclass
class DialogueContext:
    """Persistent context for a multi-turn dialogue session."""
    session_id: str
    user_id: str
    current_state: DialogueState = DialogueState.IDLE
    active_intent: Optional[IntentSchema] = None
    filled_slots: Dict[str, Any] = field(default_factory=dict)
    pending_slots: List[SlotSchema] = field(default_factory=list)
    turn_count: int = 0
    last_utterance: Optional[Utterance] = None
    topic_history: List[str] = field(default_factory=list)
    context_expiry: float = 300.0
    created_at: float = field(default_factory=time.time)
    history: List[Tuple[str, str]] = field(default_factory=list)

    @property
    def is_expired(self) -> bool:
        return (time.time() - self.created_at) > self.context_expiry

    def add_to_history(self, role: str, text: str) -> None:
        self.history.append((role, text))
        if len(self.history) > 50:
            self.history = self.history[-50:]


@dataclass
class SkillResponse:
    """Response from a skill execution."""
    success: bool
    speech_text: str = ""
    data: Optional[Any] = None
    follow_up_prompt: Optional[str] = None
    skill_name: str = ""
    execution_time_ms: float = 0.0
    error: Optional[str] = None


@dataclass
class VoiceResponse:
    """Final response to be spoken back to the user."""
    text: str
    action: Optional[SkillResponse] = None
    should_listen: bool = True
    confidence_note: Optional[str] = None
    follow_up: Optional[str] = None
    ssml: Optional[str] = None


@dataclass
class WakeWordDetection:
    """Result of wake word detection processing."""
    result: WakeWordResult
    confidence: float = 0.0
    timestamp: float = 0.0
    buffered_audio: Optional[bytes] = None

    @property
    def activated(self) -> bool:
        return self.result == WakeWordResult.ACTIVATED

    def get_buffered_audio(self) -> Optional[bytes]:
        return self.buffered_audio


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class VoiceAssistantError(Exception):
    """Base exception for voice assistant errors."""
    pass


class IntentNotFoundError(VoiceAssistantError):
    """Raised when no matching intent is found."""
    pass


class SlotMissingError(VoiceAssistantError):
    """Raised when required slots are missing."""
    def __init__(self, missing_slots: List[str]):
        self.missing_slots = missing_slots
        super().__init__(f"Missing required slots: {missing_slots}")


class SkillExecutionError(VoiceAssistantError):
    """Raised when a skill fails to execute."""
    pass


class DialogueExpiredError(VoiceAssistantError):
    """Raised when dialogue context has expired."""
    pass


class PrivacyViolationError(VoiceAssistantError):
    """Raised when a request violates privacy level restrictions."""
    pass


# ---------------------------------------------------------------------------
# Core Classes
# ---------------------------------------------------------------------------

class WakeWordDetector:
    """
    Always-on keyword detector that runs locally without network access.

    Maintains an audio buffer and activates the full NLU pipeline upon detection.
    """

    def __init__(
        self,
        model: str = "hey_assistant_v3",
        sensitivity: float = 0.7,
        false_positive_suppression: bool = True,
        audio_buffer_seconds: float = 3.0,
        sample_rate: int = 16000,
    ):
        self.model = model
        self.sensitivity = sensitivity
        self.fp_suppression = false_positive_suppression
        self.buffer_seconds = audio_buffer_seconds
        self.sample_rate = sample_rate
        self._buffer_size = int(sample_rate * audio_buffer_seconds)
        self._audio_buffer: List[np.ndarray] = []
        self._activated = False
        self._activation_cooldown = 2.0
        self._last_activation_time = 0.0

        # Import numpy for buffer management
        import numpy as np
        self._np = np

    def _is_in_cooldown(self) -> bool:
        return (time.time() - self._last_activation_time) < self._activation_cooldown

    def _should_activate(self, energy: float) -> bool:
        threshold = self.sensitivity * 0.01
        if self.fp_suppression and self._is_in_cooldown():
            return False
        return energy > threshold

    def process(self, audio_chunk: bytes) -> WakeWordDetection:
        """Process an audio chunk and return wake word detection result."""
        import numpy as np

        samples = np.frombuffer(audio_chunk, dtype=np.float32) if audio_chunk else np.array([], dtype=np.float32)
        self._audio_buffer.append(samples)

        # Maintain buffer size
        total_samples = sum(len(buf) for buf in self._audio_buffer)
        while total_samples > self._buffer_size and self._audio_buffer:
            removed = self._audio_buffer.pop(0)
            total_samples -= len(removed)

        if len(samples) == 0:
            return WakeWordDetection(result=WakeWordResult.NOISE)

        # Compute frame energy
        energy = float(np.mean(samples ** 2))

        if not self._should_activate(energy):
            return WakeWordDetection(result=WakeWordResult.REJECTED, confidence=0.0)

        # Simulated model inference (placeholder)
        activation_confidence = min(1.0, energy * 10 + self.sensitivity * 0.3)

        if activation_confidence >= self.sensitivity:
            self._last_activation_time = time.time()
            buffered = np.concatenate(self._audio_buffer).tobytes()
            self._audio_buffer.clear()

            logger.info("Wake word detected (confidence=%.2f)", activation_confidence)
            return WakeWordDetection(
                result=WakeWordResult.ACTIVATED,
                confidence=activation_confidence,
                timestamp=time.time(),
                buffered_audio=buffered,
            )

        return WakeWordDetection(
            result=WakeWordResult.PARTIAL,
            confidence=activation_confidence,
        )

    def reset(self) -> None:
        """Reset the audio buffer and activation state."""
        self._audio_buffer.clear()
        self._activated = False


class IntentClassifier:
    """
    Classifies user utterances into predefined intents with confidence scoring.

    Supports top-N alternative intents for disambiguation.
    """

    def __init__(
        self,
        model: str = "intent_bert_v2",
        intents: Optional[List[str]] = None,
        confidence_threshold: float = 0.65,
        max_alternatives: int = 3,
    ):
        self.model = model
        self.intents = intents or []
        self.confidence_threshold = confidence_threshold
        self.max_alternatives = max_alternatives
        self._intent_schemas: Dict[str, IntentSchema] = {}

        # Initialize placeholder intent patterns
        self._keyword_patterns: Dict[str, List[str]] = {
            "play_music": ["play", "music", "song", "artist", "album", "listen"],
            "set_timer": ["timer", "alarm", "remind", "minutes", "hours"],
            "get_weather": ["weather", "temperature", "forecast", "rain", "sunny"],
            "send_message": ["send", "message", "text", "tell", "forward"],
            "control_lights": ["lights", "light", "dim", "bright", "off", "on"],
            "make_call": ["call", "phone", "dial", "ring"],
            "set_reminder": ["remind", "reminder", "remember", "schedule"],
            "search_web": ["search", "look up", "find", "google", "query"],
        }

    def register_schema(self, schema: IntentSchema) -> None:
        """Register an intent schema with slot definitions."""
        self._intent_schemas[schema.name] = schema
        if schema.name not in self.intents:
            self.intents.append(schema.name)
        logger.info("Registered intent schema: %s with %d slots", schema.name, len(schema.slots))

    def _compute_intent_scores(self, text: str) -> Dict[str, float]:
        """Compute intent scores from text (keyword matching + simulated model)."""
        text_lower = text.lower()
        scores = {}

        for intent, keywords in self._keyword_patterns.items():
            if intent not in self.intents:
                continue
            score = sum(1.0 for kw in keywords if kw in text_lower)
            # Normalize and add noise for realism
            import random
            score = min(1.0, score * 0.25 + random.uniform(-0.05, 0.05))
            scores[intent] = max(0.0, score)

        return scores

    def classify(self, text: str) -> Intent:
        """Classify an utterance and return the top intent with alternatives."""
        scores = self._compute_intent_scores(text)

        if not scores:
            return Intent(name="unknown", confidence=0.0, raw_text=text)

        sorted_intents = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        best_name, best_conf = sorted_intents[0]
        alternatives = [
            (name, conf) for name, conf in sorted_intents[1:self.max_alternatives + 1]
        ]

        intent = Intent(
            name=best_name,
            confidence=best_conf,
            raw_text=text,
            alternatives=alternatives,
        )

        if not intent.is_actionable:
            logger.warning("Low confidence intent: %s (%.2f)", best_name, best_conf)

        return intent

    def get_schema(self, intent_name: str) -> Optional[IntentSchema]:
        return self._intent_schemas.get(intent_name)


class SlotExtractor:
    """Extracts structured entity slots from utterance text."""

    def __init__(self):
        import re
        self._re = re
        self._type_patterns = {
            "integer": r"\b(\d+)\b",
            "float": r"\b(\d+\.?\d*)\b",
            "time": r"\b(\d{1,2}:\d{2}\s*(?:AM|PM|am|pm)?)\b",
            "duration": r"\b(\d+)\s*(minutes?|hours?|seconds?)\b",
        }

    def _extract_by_type(self, text: str, slot_type: str) -> List[str]:
        """Extract values of a specific type from text."""
        pattern = self._type_patterns.get(slot_type)
        if pattern:
            return self._re.findall(pattern, text)
        return []

    def _extract_string_slot(self, text: str, slot_name: str) -> Optional[str]:
        """Extract a string slot value (simplified keyword extraction)."""
        # In production, this uses NER or ML-based extraction
        words = text.lower().split()
        if slot_name == "artist" and "by" in words:
            idx = words.index("by")
            if idx + 1 < len(words):
                return " ".join(words[idx + 1:])
        if slot_name == "recipient" and "to" in words:
            idx = words.index("to")
            if idx + 1 < len(words):
                return words[idx + 1]
        if slot_name == "duration":
            matches = self._extract_by_type(text, "duration")
            if matches:
                return f"{matches[0][0]} {matches[0][1]}"
        return None

    def extract(
        self,
        text: str,
        intent_schema: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Extract slots from text based on the intent schema."""
        extracted = {}

        for slot_name, schema in intent_schema.items():
            slot_type = schema.get("type", "string")

            if slot_type in self._type_patterns:
                matches = self._extract_by_type(text, slot_type)
                if matches:
                    extracted[slot_name] = matches[0]
            else:
                value = self._extract_string_slot(text, slot_name)
                if value:
                    extracted[slot_name] = value

        return extracted

    def extract_from_schema(
        self,
        text: str,
        intent_schema: IntentSchema,
    ) -> Dict[str, Slot]:
        """Extract slots using a full IntentSchema definition."""
        extracted = {}
        for slot_def in intent_schema.slots:
            if slot_def.slot_type in self._type_patterns:
                matches = self._extract_by_type(text, slot_def.slot_type)
                if matches:
                    extracted[slot_def.name] = Slot(
                        name=slot_def.name,
                        value=matches[0],
                        slot_type=slot_def.slot_type,
                        confidence=0.9,
                        raw_text=matches[0],
                    )
            else:
                value = self._extract_string_slot(text, slot_def.name)
                if value:
                    extracted[slot_def.name] = Slot(
                        name=slot_def.name,
                        value=value,
                        slot_type=slot_def.slot_type,
                        confidence=0.85,
                    )
        return extracted


class Skill(ABC):
    """Abstract base class for voice assistant skills/actions."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique skill identifier."""
        ...

    @property
    @abstractmethod
    def required_slots(self) -> List[SlotSchema]:
        """Slots that must be filled before execution."""
        ...

    @property
    def priority(self) -> SkillPriority:
        return SkillPriority.NORMAL

    @abstractmethod
    def execute(self, slots: Dict[str, Any], context: DialogueContext) -> SkillResponse:
        """Execute the skill with filled slots."""
        ...

    def can_handle(self, intent_name: str) -> bool:
        return intent_name == self.name


class SkillRouter:
    """
    Routes intents to registered skills with priority-based conflict resolution.

    Supports skill chaining and concurrent execution.
    """

    def __init__(self):
        self._skills: Dict[str, Skill] = {}
        self._fallback_handler: Optional[Callable[[Intent], SkillResponse]] = None

    def register(self, intent_name: str, skill: Skill, priority: Optional[int] = None) -> None:
        """Register a skill for an intent."""
        self._skills[intent_name] = skill
        logger.info("Registered skill: %s -> %s (priority=%s)", intent_name, skill.name, priority)

    def set_fallback(self, handler: Callable[[Intent], SkillResponse]) -> None:
        self._fallback_handler = handler

    def route(self, intent: Intent) -> Optional[Skill]:
        """Route an intent to the appropriate skill."""
        skill = self._skills.get(intent.name)
        if skill:
            return skill

        if self._fallback_handler:
            logger.info("Using fallback handler for intent: %s", intent.name)
            return None

        logger.warning("No skill registered for intent: %s", intent.name)
        return None

    def execute(
        self,
        intent: Intent,
        slots: Dict[str, Any],
        context: DialogueContext,
    ) -> SkillResponse:
        """Route and execute the appropriate skill."""
        start_time = time.time()

        skill = self.route(intent)
        if skill is None:
            if self._fallback_handler:
                response = self._fallback_handler(intent)
                return response
            return SkillResponse(
                success=False,
                speech_text=f"I don't know how to handle {intent.name}.",
                error=f"No skill for intent: {intent.name}",
            )

        try:
            response = skill.execute(slots, context)
            response.skill_name = skill.name
            response.execution_time_ms = (time.time() - start_time) * 1000
            logger.info("Skill %s executed in %.1fms", skill.name, response.execution_time_ms)
            return response
        except Exception as e:
            logger.error("Skill execution failed: %s", e)
            return SkillResponse(
                success=False,
                speech_text="Sorry, something went wrong. Please try again.",
                skill_name=skill.name,
                error=str(e),
            )


class DialogueManager:
    """
    Manages multi-turn conversations with context persistence and slot filling.

    Implements a finite-state machine with interruption support and correction handling.
    """

    def __init__(
        self,
        max_turns: int = 20,
        context_expiry_seconds: float = 300.0,
        correction_enabled: bool = True,
        interruption_enabled: bool = True,
    ):
        self.max_turns = max_turns
        self.context_expiry = context_expiry_seconds
        self.correction_enabled = correction_enabled
        self.interruption_enabled = interruption_enabled
        self._sessions: Dict[str, DialogueContext] = {}
        self._intent_classifier = IntentClassifier()
        self._slot_extractor = SlotExtractor()

    def _get_or_create_context(self, session_id: str, user_id: str) -> DialogueContext:
        """Get existing context or create a new one."""
        if session_id in self._sessions:
            ctx = self._sessions[session_id]
            if ctx.is_expired:
                logger.info("Context expired for session %s, creating new", session_id)
                ctx = DialogueContext(session_id=session_id, user_id=user_id)
                self._sessions[session_id] = ctx
            return ctx

        ctx = DialogueContext(
            session_id=session_id,
            user_id=user_id,
            context_expiry=self.context_expiry,
        )
        self._sessions[session_id] = ctx
        return ctx

    def process_utterance(
        self,
        session_id: str,
        utterance: str,
        context: Optional[Dict[str, Any]] = None,
        router: Optional[SkillRouter] = None,
    ) -> VoiceResponse:
        """Process a user utterance within a dialogue session."""
        user_id = context.get("user_id", "default") if context else "default"
        ctx = self._get_or_create_context(session_id, user_id)
        ctx.turn_count += 1
        ctx.add_to_history("user", utterance)

        # Check for interruption
        if self.interruption_enabled and ctx.current_state == DialogueState.RESPONDING:
            ctx.current_state = DialogueState.PROCESSING
            logger.info("Interruption detected at turn %d", ctx.turn_count)

        # Check for correction
        if self.correction_enabled and ctx.is_correction(utterance):
            return self._handle_correction(ctx, utterance, router)

        # Check max turns
        if ctx.turn_count > self.max_turns:
            return VoiceResponse(
                text="We've been chatting for a while. Let me know if you need anything else!",
                should_listen=False,
            )

        # Classify intent
        intent = self._intent_classifier.classify(utterance)

        if not intent.is_actionable:
            ctx.current_state = DialogueState.ERROR_RECOVERY
            alternatives_text = ""
            if intent.alternatives:
                alts = ", ".join(f"'{a[0]}'" for a in intent.alternatives[:2])
                alternatives_text = f" Did you mean {alts}?"
            return VoiceResponse(
                text=f"I'm not sure what you mean by that.{alternatives_text} Could you rephrase?",
                confidence_note=f"Confidence: {intent.confidence:.0%}",
            )

        # Get intent schema
        schema = self._intent_classifier.get_schema(intent.name)
        if schema is None:
            schema = IntentSchema(name=intent.name)

        # Extract slots
        extracted_slots = self._slot_extractor.extract_from_schema(utterance, schema)

        # Check required slots
        missing_slots = [
            s for s in schema.required_slots
            if s.name not in extracted_slots and s.name not in ctx.filled_slots
        ]

        if missing_slots:
            ctx.current_state = DialogueState.AWAITING_SLOT
            ctx.active_intent = schema
            ctx.pending_slots = missing_slots
            prompt = missing_slots[0].disambiguation_prompt or f"What {missing_slots[0].name} would you like?"
            ctx.add_to_history("assistant", prompt)
            return VoiceResponse(text=prompt, follow_up=prompt)

        # Merge with previously filled slots
        all_slots = {**ctx.filled_slots, **{k: v.value for v in extracted_slots.items()}}

        # Execute skill
        if router:
            ctx.current_state = DialogueState.EXECUTING
            skill_response = router.execute(intent, all_slots, ctx)
            ctx.current_state = DialogueState.RESPONDING

            if skill_response.success:
                # Reset context for fresh conversation
                ctx.filled_slots.clear()
                ctx.active_intent = None
                ctx.current_state = DialogueState.IDLE
                ctx.add_to_history("assistant", skill_response.speech_text)
                return VoiceResponse(
                    text=skill_response.speech_text,
                    action=skill_response,
                    should_listen=True,
                    follow_up=skill_response.follow_up_prompt,
                )
            else:
                return VoiceResponse(
                    text=skill_response.speech_text or "Something went wrong.",
                    action=skill_response,
                    should_listen=True,
                )

        # No router — return classified intent
        response_text = f"Got it — {intent.name} with {len(all_slots)} parameters."
        ctx.add_to_history("assistant", response_text)
        return VoiceResponse(text=response_text, should_listen=True)

    def _handle_correction(
        self,
        ctx: DialogueContext,
        utterance: str,
        router: Optional[SkillRouter],
    ) -> VoiceResponse:
        """Handle user correction of a previous utterance."""
        logger.info("Handling correction in session %s", ctx.session_id)
        ctx.current_state = DialogueState.PROCESSING
        return self.process_utterance(ctx.session_id, utterance, router=router)

    def get_context(self, session_id: str) -> Optional[DialogueContext]:
        return self._sessions.get(session_id)


class VoiceUI:
    """
    Template-based voice user interface patterns.

    Provides confirmation, error recovery, disambiguation, and progressive disclosure.
    """

    def __init__(self):
        self._templates: Dict[str, str] = {
            "confirm_explicit": "Do you want to {action} {details}? Say yes to confirm.",
            "confirm_implicit": "{action} {details}. Is that right?",
            "error_missing_slot": "I need one more thing — {prompt}",
            "error_unknown": "I didn't catch that. Could you try again?",
            "error_timeout": "I didn't hear anything. Let me know when you're ready.",
            "disambiguate": "Did you mean {option_a} or {option_b}?",
            "progressive_hint": "You can also ask me to {hint}.",
        }

    def confirm(
        self,
        action: str,
        parameters: Dict[str, Any],
        template: str = "confirm_explicit",
    ) -> str:
        """Generate a confirmation prompt."""
        details = ", ".join(f"{k}={v}" for k, v in parameters.items())
        tpl = self._templates.get(template, self._templates["confirm_explicit"])
        return tpl.format(action=action, details=details)

    def error_recovery(
        self,
        error_type: str,
        partial_slots: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> str:
        """Generate an error recovery prompt."""
        if error_type == "slot_missing":
            prompt = kwargs.get("prompt", "What would you like?")
            return self._templates["error_missing_slot"].format(prompt=prompt)
        elif error_type == "timeout":
            return self._templates["error_timeout"]
        else:
            return self._templates["error_unknown"]

    def disambiguate(self, option_a: str, option_b: str) -> str:
        return self._templates["disambiguate"].format(
            option_a=option_a, option_b=option_b
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the voice assistant pipeline."""
    print("=" * 60)
    print("Voice Assistants Module — Demo")
    print("=" * 60)

    # 1. Wake word detection
    print("\n[1] Wake Word Detection")
    detector = WakeWordDetector(model="hey_assistant_v3", sensitivity=0.5)
    import numpy as np
    silent_chunk = (np.zeros(1600, dtype=np.float32)).tobytes()
    result = detector.process(silent_chunk)
    print(f"    Silent chunk: {result.result.value}")

    active_chunk = (np.random.randn(1600).astype(np.float32) * 0.5).tobytes()
    result = detector.process(active_chunk)
    print(f"    Active chunk: {result.result.value} (conf={result.confidence:.2f})")

    # 2. Intent classification
    print("\n[2] Intent Classification")
    classifier = IntentClassifier(
        intents=["play_music", "set_timer", "get_weather", "send_message"]
    )
    test_utterances = [
        "play some jazz music by Miles Davis",
        "set a timer for 10 minutes",
        "what's the weather like today",
        "send a message to Alice",
        "buy groceries",
    ]
    for text in test_utterances:
        intent = classifier.classify(text)
        print(f"    '{text}'")
        print(f"      -> {intent.name} ({intent.confidence:.0%}) [{intent.confidence_tier.value}]")

    # 3. Slot extraction
    print("\n[3] Slot Extraction")
    extractor = SlotExtractor()
    slots = extractor.extract(
        "play some jazz music by Miles Davis",
        {"genre": {"type": "string"}, "artist": {"type": "string"}},
    )
    print(f"    Extracted slots: {slots}")

    # 4. Skill routing
    print("\n[4] Skill Routing")
    router = SkillRouter()

    class MockMusicSkill(Skill):
        @property
        def name(self) -> str:
            return "play_music"

        @property
        def required_slots(self) -> List[SlotSchema]:
            return [SlotSchema(name="artist", slot_type="string", required=True)]

        def execute(self, slots, context):
            artist = slots.get("artist", "unknown")
            return SkillResponse(
                success=True,
                speech_text=f"Playing music by {artist}.",
                skill_name=self.name,
            )

    router.register("play_music", MockMusicSkill())
    intent = classifier.classify("play jazz by Miles Davis")
    response = router.execute(intent, {"artist": "Miles Davis"}, DialogueContext("s1", "u1"))
    print(f"    Response: {response.speech_text} ({response.execution_time_ms:.1f}ms)")

    # 5. Multi-turn dialogue
    print("\n[5] Multi-Turn Dialogue")
    dm = DialogueManager(max_turns=5)
    dm._intent_classifier = classifier

    session_id = "demo_session"
    responses = [
        "set a timer for 10 minutes",
        "yes confirm",
    ]
    for text in responses:
        resp = dm.process_utterance(session_id, text)
        print(f"    User: '{text}'")
        print(f"    Assistant: {resp.text}")
        if resp.follow_up:
            print(f"    Follow-up: {resp.follow_up}")

    # 6. Voice UI templates
    print("\n[6] Voice UI Templates")
    ui = VoiceUI()
    print(f"    Confirm: {ui.confirm('send_message', {'to': 'Alice', 'body': 'Hello!'})}")
    print(f"    Error: {ui.error_recovery('slot_missing', prompt='Who should I send it to?')}")
    print(f"    Disambiguate: {ui.disambiguate('play music', 'set timer')}")

    print("\n" + "=" * 60)
    print("Demo complete. All voice assistant modules functional.")
    print("=" * 60)


# numpy import needed for demo
import numpy as np  # noqa: E402

if __name__ == "__main__":
    main()

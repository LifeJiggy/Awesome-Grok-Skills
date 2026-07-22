---
name: "voice-assistants"
category: "voice-technology"
version: "1.0.0"
tags: ["voice-technology", "voice-assistants", "nlu", "dialogue-management", "wake-word", "intent-recognition"]
---

# Voice Assistants — Intent Recognition, Dialogue Management & Skill Routing

## Overview

Voice assistants sit at the intersection of speech recognition, natural language understanding, and action execution. This module provides the full stack beyond raw transcription — from wake word detection that activates the system, through intent classification and slot filling that extracts structured commands, to multi-turn dialogue management that maintains conversational context across interactions. The goal is to transform free-form spoken language into reliable, actionable function calls with sub-second latency.

A production voice assistant must handle far more than simple command-response pairs. Users expect the system to disambiguate vague requests ("play that song" requires context), handle interruptions mid-sentence, gracefully recover from misrecognitions, and orchestrate multiple backend skills simultaneously (setting a timer while playing music while adjusting lights). This module's dialogue manager implements a finite-state-machine with slot-carrying context, supporting both deterministic intent flows and probabilistic dialogue policies trained via reinforcement learning.

Privacy is a first-class concern. Modern voice assistants process sensitive personal data — location, contacts, health queries, financial requests. This module includes privacy-preserving patterns: on-device wake word detection, ephemeral audio buffers, opt-in processing for sensitive domains, and configurable data retention policies. The architecture separates the always-on keyword detector (runs locally, never transmits) from the cloud-connected understanding pipeline (activated only after wake word confirmation).

The voice user interface (VUI) patterns in this module define how the assistant communicates with users — when to confirm, when to ask clarifying questions, and how to present progressive disclosure without overwhelming the conversational flow. These patterns are informed by research in human-computer interaction and are designed to feel natural across diverse user populations.

This module also supports multi-modal interaction where voice commands are combined with visual context (screen content, camera input) and gesture recognition, enabling richer interaction paradigms for smart displays, automotive systems, and augmented reality interfaces.

## Core Capabilities

- **Wake Word Detection**: Keyword spotting with configurable sensitivity, false-positive suppression, and on-device inference for privacy
- **Intent Classification**: Multi-class intent recognition from ASR transcripts with confidence scoring and fallback routing
- **Slot Filling**: Structured entity extraction from voice commands with type coercion, validation, and disambiguation prompting
- **Multi-Turn Dialogue Management**: Context-carrying conversations with entity persistence, correction handling, and topic tracking
- **Skill/Action Routing**: Dynamic dispatch to registered skills based on intent, with priority, chaining, and conflict resolution
- **Device Orchestration**: Multi-device command routing, proximity-aware delegation, and synchronized cross-device actions
- **Privacy-Preserving Processing**: On-device wake word, ephemeral buffers, domain-level consent, and configurable data retention
- **Voice UI Patterns**: Confirmation, error recovery, disambiguation, and progressive disclosure templates

## Usage Examples

```python
from voice_assistants import WakeWordDetector, IntentClassifier

# Initialize wake word detector (on-device, always running)
detector = WakeWordDetector(
    model="hey_assistant_v3",
    sensitivity=0.7,
    false_positive_suppression=True,
    audio_buffer_seconds=3.0
)

# Process streaming audio
for audio_chunk in audio_stream:
    result = detector.process(audio_chunk)
    if result.activated:
        print(f"Wake word detected at {result.timestamp:.2f}s")
        # Pass buffered audio + subsequent audio to ASR
        full_utterance = result.get_buffered_audio()
```

```python
from voice_assistants import IntentClassifier, SlotExtractor

# Define intent schema
classifier = IntentClassifier(
    model="intent_bert_v2",
    intents=[
        "play_music", "set_timer", "get_weather", "send_message",
        "control_lights", "make_call", "set_reminder", "search_web"
    ],
    confidence_threshold=0.65
)

# Classify an utterance
result = classifier.classify("play some jazz music by Miles Davis")
print(f"Intent: {result.intent} ({result.confidence:.2f})")
# Intent: play_music (0.94)

# Extract slots
extractor = SlotExtractor()
slots = extractor.extract(
    text="play some jazz music by Miles Davis",
    intent_schema={
        "genre": {"type": "string", "required": False},
        "artist": {"type": "string", "required": True},
        "album": {"type": "string", "required": False}
    }
)
print(slots)  # {'artist': 'Miles Davis', 'genre': 'jazz'}
```

```python
from voice_assistants import DialogueManager, SkillRouter

# Configure dialogue manager
dm = DialogueManager(
    max_turns=20,
    context_expiry_seconds=300,
    correction_enabled=True,
    interruption_enabled=True
)

# Register skills
router = SkillRouter()
router.register("play_music", MusicSkill(), priority=10)
router.register("set_timer", TimerSkill(), priority=5)
router.register("control_lights", LightsSkill(), priority=8)

# Handle a multi-turn conversation
response = dm.process_utterance(
    session_id="user_123",
    utterance="set a timer for 10 minutes",
    context={},
    router=router
)
# response.action: TimerSkill.set(minutes=10)
# response.speech: "Timer set for 10 minutes. I'll let you know when it's done."
```

```python
from voice_assistants import VoiceUI, ConfirmationPattern

ui = VoiceUI()

# Generate confirmation prompt
confirmation = ui.confirm(
    action="send_message",
    parameters={"to": "Alice", "body": "I'll be there at 5"},
    template=ConfirmationPattern.EXPLICIT
)
# "Send a message to Alice saying 'I'll be there at 5'? Say yes to confirm."

# Generate error recovery
error = ui.error_recovery(
    error_type="slot_missing",
    missing_slot="recipient",
    partial_slots={"body": "I'll be there at 5"},
    prompt="Who should I send the message to?"
)
```

```python
from voice_assistants import PrivacyGuard, ConsentManager

# Configure privacy settings
privacy = PrivacyGuard(
    ephemeral_audio=True,
    retention_seconds=0,  # Don't store audio
    sensitive_domains=["health", "finance", "location"],
    require_consent_for=["health", "finance"]
)

consent = ConsentManager()
consent.grant("user_123", domain="health", expires_in_hours=24)
consent.grant("user_123", domain="finance", expires_in_hours=1)
```

```python
from voice_assistants import ContextManager, CorrectionHandler

# Maintain context across turns
context_mgr = ContextManager(session_timeout_seconds=300)
context_mgr.set_slot("user_123", "artist", "Miles Davis")
context_mgr.set_slot("user_123", "genre", "jazz")

# Handle user corrections ("actually, make it rock")
correction = CorrectionHandler()
corrected_slots = correction.apply(
    utterance="actually, make it rock music",
    previous_slots={"artist": "Miles Davis", "genre": "jazz"},
    correction_patterns=[
        {"pattern": r"make it (.+)", "target_slot": "genre"},
        {"pattern": r"change to (.+)", "target_slot": None}
    ]
)
print(corrected_slots)  # {'artist': 'Miles Davis', 'genre': 'rock'}
```

```python
from voice_assistants import SkillChain, MultiDeviceRouter

# Chain multiple skills in a single command
chain = SkillChain()
chain.add_step("set_timer", {"minutes": 10})
chain.add_step("play_music", {"genre": "jazz", "shuffle": True})
chain.add_step("control_lights", {"brightness": 30, "color": "warm"})

router = SkillRouter()
results = router.execute_chain(chain, session_id="user_123")

# Multi-device routing
device_router = MultiDeviceRouter()
device_router.register("kitchen_display", capabilities=["display", "speaker"])
device_router.register("bedroom_speaker", capabilities=["speaker"])
device_router.register("living_room_tv", capabilities=["display", "speaker"])

target = device_router.select_device(
    utterance="play some jazz",
    user_location="living_room",
    proximity_preference=True
)
print(f"Routing to: {target.device_id}")
```

## Best Practices

1. **Separate wake word detection from understanding**: The keyword spotter must run entirely on-device with zero network dependency. Cloud connectivity should only activate after confirmed wake word detection to preserve privacy and reduce latency. Target <50ms for wake word processing.

2. **Set confidence thresholds per intent, not globally**: High-stakes intents (financial transactions, sending messages) require higher confidence than low-stakes ones (playing music). Calibrate thresholds using F1-score tradeoffs on domain-specific validation sets.

3. **Always confirm before destructive or irreversible actions**: Sending messages, making purchases, deleting data, or modifying smart home configurations should always trigger an explicit confirmation turn, even at confidence 1.0. The cost of a false positive far exceeds the cost of an extra conversational turn.

4. **Implement graceful degradation for ASR errors**: When the classifier confidence is low, route to disambiguation rather than guessing. "Did you mean X or Y?" is preferable to executing the wrong action. Log low-confidence utterances for later analysis and model improvement.

5. **Persist slot context across turns**: Users rarely provide all required information in a single utterance. The dialogue manager must carry forward entity slots and resume extraction on subsequent turns without forcing the user to repeat themselves.

6. **Use interruption detection carefully**: Allow users to correct mid-response, but distinguish intentional interruptions from accidental speech overlap. Apply a minimum response duration (500ms) before enabling interruption listening to avoid chopping off assistant responses.

7. **Log interaction telemetry for pipeline improvement**: Record intent accuracy, slot fill rates, abandonment points, and correction frequency. These metrics drive continuous improvement of the NLU models and dialogue policies. Set up dashboards to track weekly trends.

8. **Design voice UI templates for all states**: Pre-script responses for every dialogue state — confirmation, error, disambiguation, timeout, and success. Inconsistent phrasing confuses users and degrades trust. Use a consistent voice persona across all templates.

## Architecture Notes

The dialogue manager uses a finite-state machine with the following states: IDLE -> LISTENING -> PROCESSING -> AWAITING_SLOT -> AWAITING_CONFIRMATION -> EXECUTING -> RESPONDING -> IDLE. Transitions are triggered by user input, NLU results, and skill responses. The context object carries state across turns and expires after a configurable timeout (default 300 seconds).

For production deployments, consider adding a dialogue policy layer that learns optimal state transitions from user interaction data. Reinforcement learning with human feedback (RLHF) can optimize for task completion rate and user satisfaction simultaneously.

The skill routing system uses a priority-based dispatch mechanism where each registered skill declares its supported intents, required slots, and execution priority. When multiple skills match an intent, the router applies conflict resolution rules: explicit skill names take priority over implicit routing, and higher-priority skills win on ties. Skill chaining allows a single utterance to trigger multiple sequential actions with shared context propagation between steps.

The privacy architecture enforces a strict boundary between on-device and cloud processing. Wake word detection, audio buffering, and sensitive domain routing happen locally. Only after wake word confirmation does audio leave the device, and only the minimum necessary audio is transmitted. All transmitted audio is encrypted in transit and configurable for zero-retention processing where regulations require it.

## Related Modules

- [speech-recognition](../speech-recognition/) — ASR engine that provides transcripts to the intent classifier
- [speech-processing](../speech-processing/) — Audio preprocessing before wake word and ASR
- [text-to-speech](../text-to-speech/) — Response synthesis for spoken output
- [voice-analytics](../voice-analytics/) — Emotion detection for context-aware response tone

---

## Advanced Configuration

### Wake Word Model Tuning

```python
from voice_assistants import WakeWordConfig

config = WakeWordConfig(
    model="custom_wake_v2",
    sensitivity=0.6,
    false_positive_rate_target=0.01,
    detection_threshold=0.7,
    audio_buffer_seconds=3.0,
    sample_rate=16000,
    energy_gate_db=-40,
    spectral_gate_enabled=True,
)
```

### Intent Classifier Configuration

```python
from voice_assistants import IntentConfig

intent_config = IntentConfig(
    model="intent_transformer_v3",
    confidence_threshold=0.65,
    fallback_intent="unknown",
    max_intents_per_utterance=3,
    slot_filling_strategy="greedy",
    context_window_turns=5,
    entity_linking_enabled=True,
)
```

## Architecture Patterns

### Voice Assistant Pipeline

```
Audio Stream
    │
    ▼
┌──────────────┐
│ Wake Word    │── On-device keyword spotting
│ Detection    │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ ASR          │── Speech-to-text transcription
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ NLU          │── Intent classification + slot filling
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Dialogue     │── Context management, disambiguation
│ Manager      │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Skill Router │── Dispatch to appropriate skill
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ TTS          │── Text-to-speech response
└──────────────┘
```

### Dialogue State Machine

```
IDLE → LISTENING → PROCESSING → AWAITING_SLOT → EXECUTING → RESPONDING → IDLE
  ↑                                                                    │
  └────────────────────────────────────────────────────────────────────┘

Additional transitions:
- PROCESSING → AWAITING_CONFIRMATION (destructive actions)
- AWAITING_SLOT → LISTENING (user provides slot)
- RESPONDING → LISTENING (follow-up question)
```

## Integration Guide

### Smart Home Integration

```python
from voice_assistants import SmartHomeSkill, DeviceRegistry

registry = DeviceRegistry()
registry.add_device("kitchen_light", "light", capabilities=["on_off", "brightness", "color"])
registry.add_device("thermostat", "thermostat", capabilities=["temperature", "mode"])

skill = SmartHomeSkill(device_registry=registry)
router.register("control_lights", skill, priority=10)
```

### Multi-Turn Context Management

```python
from voice_assistants import ContextManager

context = ContextManager(session_timeout_s=300)
context.set_slot("user_123", "genre", "jazz")
context.set_slot("user_123", "mood", "relaxing")

# Later turn: "How about something faster?"
# Context carries forward genre=jazz, mood updates to energetic
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| On-device wake word | Zero latency, zero network |
| NLU model quantization | 2x inference speed |
| Intent caching | Skip re-classification |
| Pre-fetched skill data | Faster response generation |
| TTS audio caching | Zero-latency repeated phrases |

## Security Considerations

- **On-device wake word**: Audio never leaves device until wake confirmation
- **Ephemeral audio buffers**: Audio discarded after processing
- **Domain-level consent**: Separate consent for health, finance, location
- **Data retention controls**: User-configurable retention periods
- **Secure skill execution**: Sandboxed skill environments
- **Intent verification**: Confirm high-stakes actions before execution

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Wake word false positives | Sensitivity too high | Reduce sensitivity to 0.5 |
| Intent misclassification | Insufficient training data | Add more utterance examples |
| Slot filling fails | Ambiguous entity | Add disambiguation prompts |
| Response latency high | TTS cold start | Pre-warm TTS model |
| Context lost between turns | Session timeout too short | Increase timeout to 600s |
| Skill not found | Missing registration | Register skill with router |

## API Reference

### WakeWordDetector

```python
class WakeWordDetector:
    def __init__(self, model: str, sensitivity: float, false_positive_suppression: bool, audio_buffer_seconds: float)
    def process(self, audio_chunk: ndarray) -> WakeWordResult
    def get_buffered_audio(self) -> ndarray
```

### IntentClassifier

```python
class IntentClassifier:
    def __init__(self, model: str, intents: list, confidence_threshold: float)
    def classify(self, text: str) -> IntentResult
    def set_confidence_threshold(self, threshold: float) -> None
```

### DialogueManager

```python
class DialogueManager:
    def __init__(self, max_turns: int, context_expiry_seconds: int, correction_enabled: bool, interruption_enabled: bool)
    def process_utterance(self, session_id: str, utterance: str, context: dict, router: SkillRouter) -> DialogueResponse
```

## Data Models

```python
from dataclasses import dataclass

@dataclass
class WakeWordResult:
    activated: bool
    timestamp: float
    confidence: float
    buffered_audio: ndarray

@dataclass
class IntentResult:
    intent: str
    confidence: float
    slots: dict

@dataclass
class DialogueResponse:
    action: str
    speech: str
    slots: dict
    requires_confirmation: bool
```

## Deployment Guide

### Installation

```bash
pip install voice-assistants
```

### Skill Registration

```python
from voice_assistants import SkillRouter

router = SkillRouter()
router.register("play_music", MusicSkill(), priority=10)
router.register("set_timer", TimerSkill(), priority=5)
router.register("control_lights", LightsSkill(), priority=8)
```

## Monitoring & Observability

```python
from voice_assistants import MetricsCollector

collector = MetricsCollector()
collector.counter("assistant.wake_detected", count)
collector.histogram("assistant.nlu.latency_ms", latency)
collector.counter("assistant.intent.total", count, tags={"intent": intent})
collector.gauge("assistant.intent.confidence", confidence)
collector.counter("assistant.slot.fill_rate", rate, tags={"slot": slot})
```

## Testing Strategy

```python
import pytest
from voice_assistants import IntentClassifier

def test_intent_classification():
    classifier = IntentClassifier(model="test_model", intents=["play_music", "set_timer"], confidence_threshold=0.5)
    result = classifier.classify("play some jazz music")
    assert result.intent == "play_music"
    assert result.confidence > 0.5
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added multi-turn dialogue | Enable context manager |
| 2.0.0 | New NLU model | Re-train intent classifier |

## Glossary

| Term | Definition |
|------|-----------|
| **NLU** | Natural Language Understanding |
| **Intent** | User's desired action from an utterance |
| **Slot** | Extracted entity from an utterance |
| **Wake Word** | Keyword that activates the assistant |
| **VUI** | Voice User Interface |
| **Dialogue Management** | Tracking conversation state across turns |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with wake word detection
- Intent classification and slot filling
- Multi-turn dialogue management
- Skill routing and chaining

## Contributing Guidelines

```bash
git clone https://github.com/example/voice-assistants.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Intent Classification Reference

| Intent | Example Utterance | Slots | Confidence |
|--------|------------------|-------|------------|
| play_music | "Play jazz by Miles Davis" | genre, artist | High |
| set_timer | "Set a timer for 10 minutes" | duration | High |
| get_weather | "What's the weather in NYC?" | location | High |
| send_message | "Text Alice I'll be late" | recipient, body | Medium |
| control_lights | "Dim lights to 50%" | brightness | High |
| make_call | "Call mom" | contact | High |
| search_web | "Search for nearest pizza" | query | Medium |

### Slot Type Reference

| Type | Examples | Validation |
|------|----------|------------|
| duration | "10 minutes", "1 hour" | Convert to seconds |
| datetime | "tomorrow at 3pm", "next Friday" | Parse to ISO |
| location | "New York", "here" | Geocode if needed |
| contact | "Alice", "Mom" | Match to contacts |
| number | "5", "3.5" | Parse numeric value |
| genre | "jazz", "rock" | Match to music library |
| color | "red", "warm white" | Convert to RGB |

### Dialogue Management Reference

| State | Description | Next States |
|-------|-------------|-------------|
| IDLE | Waiting for wake word | LISTENING |
| LISTENING | Capturing audio | PROCESSING |
| PROCESSING | Running NLU | AWAITING_SLOT, EXECUTING, RESPONDING |
| AWAITING_SLOT | Asking for missing info | PROCESSING |
| AWAITING_CONFIRMATION | Confirming action | EXECUTING, LISTENING |
| EXECUTING | Running skill | RESPONDING |
| RESPONDING | Speaking response | IDLE, LISTENING |

### VUI Design Patterns

| Pattern | When to Use | Example |
|---------|------------|---------|
| Explicit confirmation | Destructive actions | "Delete all? Say yes to confirm." |
| Implicit confirmation | Low-risk actions | "Setting timer for 10 minutes." |
| Disambiguation | Multiple matches | "Did you mean Alice Smith or Alice Jones?" |
| Error recovery | Failed understanding | "Sorry, I didn't catch that. Try again." |
| Progressive disclosure | Complex tasks | "OK, what type of music?" |
| Context carryover | Follow-up questions | "And for the same artist?" |

### Multi-Turn Context Reference

| Context Type | Persistence | Example |
|-------------|-------------|---------|
| Session | Duration of conversation | Current music genre |
| User | Across sessions | User preferences |
| Device | Per device | Device location |
| Skill | Per skill invocation | Current playlist |
| Conversation | Within topic | Previous search query |

### Skill Registration Reference

| Skill | Intents | Priority | Dependencies |
|-------|---------|----------|-------------|
| Music | play_music, pause_music, next_track | 10 | Music API |
| Timer | set_timer, cancel_timer, timer_status | 5 | System clock |
| Lights | control_lights, light_status | 8 | Smart home API |
| Weather | get_weather, forecast | 3 | Weather API |
| Messages | send_message, read_messages | 7 | Messaging API |
| Calendar | create_event, list_events | 6 | Calendar API |

## NLU Pipeline Deep Dive

### Transformer-Based Intent Classification

```python
from voice_assistants import TransformerIntentClassifier, IntentModelConfig

config = IntentModelConfig(
    model_type="bert",
    hidden_size=768,
    num_attention_heads=12,
    num_hidden_layers=12,
    num_intents=50,
    max_sequence_length=128,
    dropout=0.1,
    label_smoothing=0.1
)

classifier = TransformerIntentClassifier(config)
classifier.load_weights("intent_bert_v3.ckpt")

# Classify with token-level confidence
result = classifier.classify("play jazz music by Miles Davis")
print(f"Intent: {result.intent}")
print(f"Confidence: {result.confidence:.3f}")

# Get top-k predictions
top_k = classifier.classify_top_k("set a timer for 10 minutes", k=3)
for pred in top_k:
    print(f"  {pred.intent}: {pred.confidence:.3f}")
# set_timer: 0.94
# set_reminder: 0.04
# play_music: 0.01
```

### Entity Linking and Resolution

```python
from voice_assistants import EntityLinker, EntityResolver

# Link extracted entities to knowledge base
linker = EntityLinker(
    knowledge_base="assistant_kb.json",
    entity_types=["person", "location", "song", "device"],
    fuzzy_match=True,
    fuzzy_threshold=0.7
)

# Resolve ambiguous entities
resolver = EntityResolver(
    context_manager=context_mgr,
    disambiguation_strategy="most_recent"  # most_recent | most_frequent | ask_user
)

# Process utterance with entity linking
utterance = "play some songs by the artist I was listening to earlier"
entities = linker.link(utterance)
# {'artist': {'text': 'the artist I was listening to earlier', 'type': 'reference', 'resolved': 'Miles Davis'}}

resolved = resolver.resolve(entities, session_id="user_123")
```

### Multi-Intent Handling

```python
from voice_assistants import MultiIntentClassifier

# Handle utterances with multiple intents
multi_classifier = MultiIntentClassifier(
    model="multi_intent_transformer_v1",
    max_intents=5,
    separation_strategy="sequential"  # sequential | parallel | priority
)

result = multi_classifier.classify(
    "set a timer for 10 minutes and play some jazz and dim the lights to 30%"
)
print(f"Intents detected: {len(result.intents)}")
for intent in result.intents:
    print(f"  {intent.name}: {intent.confidence:.2f} slots={intent.slots}")
# Intents detected: 3
#   set_timer: 0.95 slots={'duration': '10 minutes'}
#   play_music: 0.92 slots={'genre': 'jazz'}
#   control_lights: 0.88 slots={'brightness': '30%'}
```

### Context-Aware Slot Filling

```python
from voice_assistants import ContextualSlotFiller

filler = ContextualSlotFiller(
    context_window=5,         # Remember last 5 turns
    slot_carry_over=True,     # Carry unfilled slots forward
    entity_memory=True        # Remember mentioned entities
)

# Track slots across turns
session = filler.new_session(session_id="user_123")

# Turn 1
result1 = filler.fill(
    utterance="play some music",
    intent="play_music",
    session=session
)
print(f"Missing required slots: {result1.missing_slots}")
# Missing required: ['genre']

# Turn 2 — context carries over
result2 = filler.fill(
    utterance="jazz please",
    intent="play_music",
    session=session
)
print(f"Filled slots: {result2.filled_slots}")
# Filled slots: {'genre': 'jazz'}
```

### Response Generation Templates

```python
from voice_assistants import ResponseGenerator, ResponseTemplate

# Define response templates for all dialogue states
templates = {
    "confirmation": ResponseTemplate(
        templates=[
            "I'll {action} for you. Should I proceed?",
            "Got it — {action}. Confirm?",
            "You want me to {action}. Is that right?"
        ],
        variables=["action"],
        fill_strategy="random"
    ),
    "error_slot_missing": ResponseTemplate(
        templates=[
            "I need to know {slot_name}. {prompt}",
            "What {slot_name} should I use? {prompt}",
            "Which {slot_name} do you mean? {prompt}"
        ],
        variables=["slot_name", "prompt"],
        fill_strategy="sequential"
    ),
    "success": ResponseTemplate(
        templates=[
            "Done. {action_description}.",
            "{action_description} — all set!",
            "OK, I've {action_description}."
        ],
        variables=["action_description"],
        fill_strategy="random"
    )
}

generator = ResponseGenerator(templates=templates)
response = generator.generate(
    state="success",
    context={"action_description": "set a timer for 10 minutes"}
)
print(response.text)
```

### Wake Word Customization

```python
from voice_assistants import CustomWakeWordTrainer

# Train a custom wake word
trainer = CustomWakeWordTrainer(
    base_model="hey_assistant_v3",
    training_data="custom_wake_samples/",
    augmentation=True,
    augmentation_config={
        "noise_levels": [5, 10, 15, 20],
        "speed_perturb": [0.9, 1.0, 1.1],
        "room_impulse": ["office", "living_room", "car"]
    }
)

# Train and validate
model = trainer.train(
    epochs=100,
    learning_rate=1e-4,
    validation_split=0.2
)

# Evaluate
metrics = trainer.evaluate(model, test_data="test_wake_samples/")
print(f"Detection rate: {metrics.detection_rate:.2%}")
print(f"False positive rate: {metrics.false_positive_rate:.4%}")
print(f"Average latency: {metrics.latency_ms:.0f}ms")
```

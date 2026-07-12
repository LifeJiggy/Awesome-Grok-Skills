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

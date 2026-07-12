---
name: "interactive-media"
category: "art-tech"
version: "2.0.0"
tags: ["interactive-media", "installation", "responsive", "participatory", "new-media", "experience"]
---

# Interactive Media

## Overview

Interactive media framework for creating participatory art, responsive environments, and user-driven digital experiences. This module provides input processing (touch, gesture, proximity, voice, biometrics), state machine management for interactive narratives, multi-user synchronization, analytics tracking, and adaptive content that responds to audience behavior. Supports gallery installations, museum exhibits, brand experiences, and creative technology projects.

## Core Capabilities

- **Multi-Modal Input**: Touch, gesture, proximity, voice, temperature, heart rate, and custom sensor integration
- **State Machine**: Define interactive narrative states with transitions, conditions, and triggers
- **Multi-User**: Support for simultaneous multiple users with avatar management and conflict resolution
- **Adaptive Content**: Content that changes based on visitor behavior, dwell time, and group dynamics
- **Analytics**: Track visitor engagement, interaction patterns, dwell time, and content effectiveness
- **Accessibility**: Alternative input methods for visitors with disabilities
- **Persistence**: Save and restore interactive state across sessions
- **Remote Control**: Web-based admin panel for content management and real-time control

## Usage

```python
from interactive_media import (
    InputProcessor, StateMachine, InteractiveExperience, VisitorProfile
)

# Define interactive experience
experience = InteractiveExperience(
    name="Digital Garden",
    max_concurrent_users=20,
    input_types=["touch", "proximity", "voice"],
)

# Input processing
inputs = InputProcessor()
inputs.add_touch_surface("wall-main", max_points=10)
inputs.add_proximity_sensor("entrance", range_m=3.0)
inputs.add_voice_recognition(language="en", wake_word="garden")

# State machine for interactive narrative
sm = StateMachine(initial_state="idle")
sm.add_state("idle", content="ambient_loop.mp4", transition_on="proximity_enter", next_state="welcome")
sm.add_state("welcome", content="welcome_message.mp4", duration=5, next_state="explore")
sm.add_state("explore", content="interactive_garden.mp4", transition_on="touch_interaction", next_state="grow")
sm.add_state("grow", content="growing_animation.mp4", duration=10, next_state="explore")
sm.add_state("farewell", content="farewell_message.mp4", duration=3, next_state="idle")

# Visitor profiles
profile = VisitorProfile(visitor_id="visitor-001")
profile.record_visit(space="main", duration_s=120)
profile.record_interaction(type="touch", count=15)
profile.preferred_content = "night_mode"
print(f"Visit duration: {profile.total_duration_s:.0f}s, interactions: {profile.total_interactions}")
```

## Best Practices

- Design for the fastest interaction — visitors expect instant response (under 100ms)
- Create clear visual feedback for every interaction — visitors need to know their action registered
- Design for diverse audiences — include interactions that work for all ages and abilities
- Track engagement metrics to identify which interactions are most compelling
- Implement idle states that attract visitors without requiring interaction
- Create natural "on-ramps" — easy entry points for first-time visitors
- Design for groups — allow multiple people to interact simultaneously
- Test with real visitors — observe behavior rather than assuming it
- Implement session persistence so visitors can return and continue
- Keep interactive complexity low — 2-3 interaction types maximum per experience

## Related Modules

- **digital-installations** — Physical installation hardware and output
- **audio-visual** — Audio-reactive interactive content
- **generative-art** — Content generation driven by interaction
- **creative-coding** — Real-time interactive visual programming
- **ambient-computing** → **context-aware** — Context-driven interactive behavior

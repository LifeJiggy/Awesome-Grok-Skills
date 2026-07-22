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

## Advanced Configuration

### Multi-Modal Input Configuration

```python
from interactive_media import InputProcessor, InputConfig, InputType

input_config = InputConfig(
    inputs=[
        {"type": InputType.TOUCH, "surface_id": "wall-main", "max_points": 20},
        {"type": InputType.PROXIMITY, "sensor_id": "entrance", "range_m": 3.0},
        {"type": InputType.VOICE, "language": "en", "wake_word": "activate"},
        {"type": InputType.GESTURE, "camera_id": "overhead", "gesture_set": "basic"},
        {"type": InputType.BIOMETRIC, "sensor_id": "heart_rate", "sampling_rate": 10},
    ],
    fusion={
        "enabled": True,
        "strategy": "weighted_average",
        "weights": {"touch": 0.4, "proximity": 0.3, "voice": 0.2, "gesture": 0.1},
        "conflict_resolution": "most_confident",
    },
    latency={
        "touch": 16,  # ms
        "proximity": 50,
        "voice": 200,
        "gesture": 100,
        "biometric": 100,
    },
)

# Initialize input processor
inputs = InputProcessor(config=input_config)

# Process input
@inputs.on_input
def on_input(input_type, data, confidence):
    print(f"Input: {input_type} - confidence: {confidence:.2f}")
    
    if input_type == "touch":
        process_touch(data)
    elif input_type == "proximity":
        process_proximity(data)
    elif input_type == "voice":
        process_voice(data)
```

### State Machine Advanced

```python
from interactive_media import StateMachine, StateConfig, Transition

state_config = StateConfig(
    initial_state="idle",
    states=[
        {"id": "idle", "content": "ambient_loop.mp4", "duration": None},
        {"id": "welcome", "content": "welcome_message.mp4", "duration": 5},
        {"id": "explore", "content": "interactive_garden.mp4", "duration": None},
        {"id": "grow", "content": "growing_animation.mp4", "duration": 10},
        {"id": "farewell", "content": "farewell_message.mp4", "duration": 3},
    ],
    transitions=[
        {"from": "idle", "to": "welcome", "trigger": "proximity_enter"},
        {"from": "welcome", "to": "explore", "trigger": "timeout"},
        {"from": "explore", "to": "grow", "trigger": "touch_interaction"},
        {"from": "grow", "to": "explore", "trigger": "timeout"},
        {"from": "explore", "to": "farewell", "trigger": "proximity_exit"},
        {"from": "farewell", "to": "idle", "trigger": "timeout"},
    ],
    parallel_states={
        "ambient_audio": {"content": "ambient_sound.wav", "volume": 0.3},
        "particle_system": {"enabled": True, "preset": "floating"},
    },
)

# Initialize state machine
sm = StateMachine(config=state_config)

# Custom transition conditions
@sm.condition("proximity_enter")
def proximity_enter(data):
    return data["distance"] < 2.0

@sm.condition("touch_interaction")
def touch_interaction(data):
    return data["touch_count"] > 5

# State change handler
@sm.on_state_change
def on_state_change(old_state, new_state, trigger):
    print(f"State: {old_state} -> {new_state} (trigger: {trigger})")
```

### Analytics Advanced

```python
from interactive_media import Analytics, AnalyticsConfig, VisitorProfile

analytics_config = AnalyticsConfig(
    tracking={
        "visitor_count": True,
        "dwell_time": True,
        "interaction_patterns": True,
        "content_effectiveness": True,
        "heat_maps": True,
        "flow_patterns": True,
    },
    privacy={
        "anonymize_data": True,
        "retention_days": 30,
        "consent_required": False,
        "pii_detection": True,
    },
    export={
        "format": "json",
        "real_time": True,
        "batch_interval_s": 60,
    },
)

analytics = Analytics(config=analytics_config)

# Track visitor
visitor = analytics.create_visitor(visitor_id="anonymous-001")
visitor.record_visit(space="main", duration_s=120)
visitor.record_interaction(type="touch", count=15, position=(500, 300))
visitor.record_content_view(content_id="greeting", duration_s=10)

# Get analytics
stats = analytics.get_stats()
print(f"Total visitors: {stats.total_visitors}")
print(f"Average dwell time: {stats.avg_dwell_time_s:.1f}s")
print(f"Interactions per visitor: {stats.avg_interactions:.1f}")

# Heat map
heat_map = analytics.get_heat_map(space="main", time_range="today")
heat_map.export("heat_map.png")
```

## Architecture Patterns

### Interactive Media Architecture

```
+------------------------------------------------------------------+
|                Interactive Media Architecture                     |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------+    +----------------+    +----------------+  |
|  |  Input         |    |  Processing    |    |  Output        |  |
|  |  Layer         |    |  Layer         |    |  Layer         |  |
|  |                |    |                |    |                |  |
|  |  Touch         |    |  State Machine |    |  Display       |  |
|  |  Proximity     |<-->|  Analytics     |<-->|  Audio         |  |
|  |  Voice         |    |  Adaptive      |    |  Lighting      |  |
|  |  Gesture       |    |  Content       |    |  Haptics       |  |
|  +-------+--------+    +-------+--------+    +-------+--------+  |
|          |                    |                     |             |
|          v                    v                     v             |
|  +----------------------------------------------------------------+
|  |                    Core Engine                                 |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Visitor     |  |  Content     |  |  Session     |          |
|  |  |  Manager     |  |  Manager     |  |  Manager     |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
|                              |                                    |
|                              v                                    |
|  +----------------------------------------------------------------+
|  |                    Persistence Layer                           |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Database    |  |  File Store  |  |  Cache       |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
+------------------------------------------------------------------+
```

### Visitor Journey Flow

```
Visitor Journey
        |
        v
+-------------------+
|  Approach         |  Proximity detected
+-------------------+
        |
        v
+-------------------+
|  Welcome          |  Greeting content
+-------------------+
        |
        v
+-------------------+
|  Explore          |  Interactive content
+-------------------+
        |
        v
+-------------------+
|  Engage           |  Deep interaction
+-------------------+
        |
        v
+-------------------+
|  Share            |  Social features
+-------------------+
        |
        v
+-------------------+
|  Depart           |  Farewell content
+-------------------+
```

### Content Adaptation Engine

```
Content Adaptation Pipeline
        |
        v
+-------------------+
|  Collect Data     |  Visitor behavior
+-------------------+
        |
        v
+-------------------+
|  Analyze Patterns |  Identify preferences
+-------------------+
        |
        v
+-------------------+
|  Select Content   |  Choose appropriate content
+-------------------+
        |
        v
+-------------------+
|  Adapt Parameters |  Adjust difficulty, speed, etc.
+-------------------+
        |
        v
+-------------------+
|  Deliver Content  |  Show adapted content
+-------------------+
        |
        v
+-------------------+
|  Measure Response |  Track engagement
+-------------------+
```

## Integration Guide

### Unity Interactive Media

```csharp
// Unity Interactive Media Setup
using UnityEngine;

public class InteractiveExperience : MonoBehaviour
{
    [SerializeField] private StateMachine stateMachine;
    [SerializeField] private InputProcessor inputProcessor;
    [SerializeField] private Analytics analytics;
    
    void Start()
    {
        // Initialize systems
        stateMachine.OnStateChange += OnStateChange;
        inputProcessor.OnInput += OnInput;
        
        // Start experience
        stateMachine.Start();
    }
    
    void OnInput(InputType type, object data, float confidence)
    {
        // Process input
        switch (type)
        {
            case InputType.Touch:
                var touchData = (TouchData)data;
                stateMachine.Trigger("touch_interaction", touchData);
                break;
            case InputType.Proximity:
                var proximityData = (ProximityData)data;
                if (proximityData.Distance < 2.0f)
                    stateMachine.Trigger("proximity_enter");
                break;
        }
    }
    
    void OnStateChange(string oldState, string newState, string trigger)
    {
        // Track state change
        analytics.TrackEvent("state_change", new {
            from = oldState,
            to = newState,
            trigger = trigger,
        });
    }
}
```

### Web-Based Interactive Media

```javascript
// Web Interactive Media
class InteractiveExperience {
    constructor() {
        this.stateMachine = new StateMachine();
        this.inputProcessor = new InputProcessor();
        this.analytics = new Analytics();
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Touch input
        document.addEventListener('touchstart', (e) => {
            this.inputProcessor.processTouch(e.touches[0]);
        });
        
        // Proximity sensor
        if ('Sensor' in window) {
            const proximity = new Sensor('proximity');
            proximity.addEventListener('reading', () => {
                this.inputProcessor.processProximity(proximity.distance);
            });
        }
        
        // Voice recognition
        if ('webkitSpeechRecognition' in window) {
            const recognition = new webkitSpeechRecognition();
            recognition.onresult = (event) => {
                this.inputProcessor.processVoice(event.results[0][0].transcript);
            };
        }
    }
    
    onInput(type, data) {
        this.stateMachine.trigger(type, data);
        this.analytics.trackEvent('input', { type, data });
    }
}
```

### Node.js Backend

```javascript
// Node.js Interactive Media Backend
const express = require('express');
const WebSocket = require('ws');

class InteractiveBackend {
    constructor() {
        this.app = express();
        this.server = require('http').createServer(this.app);
        this.wss = new WebSocket.Server({ server: this.server });
        
        this.setupRoutes();
        this.setupWebSocket();
    }
    
    setupRoutes() {
        this.app.get('/api/state', (req, res) => {
            res.json(this.stateMachine.getState());
        });
        
        this.app.post('/api/trigger', (req, res) => {
            this.stateMachine.trigger(req.body.trigger, req.body.data);
            res.json({ success: true });
        });
        
        this.app.get('/api/analytics', (req, res) => {
            res.json(this.analytics.getStats());
        });
    }
    
    setupWebSocket() {
        this.wss.on('connection', (ws) => {
            console.log('Client connected');
            
            ws.on('message', (message) => {
                const data = JSON.parse(message);
                this.handleMessage(ws, data);
            });
            
            ws.on('close', () => {
                console.log('Client disconnected');
            });
        });
    }
    
    broadcast(data) {
        this.wss.clients.forEach(client => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(JSON.stringify(data));
            }
        });
    }
}
```

## Performance Optimization

### Input Processing Optimization

```python
from interactive_media import InputOptimizer, PerformanceConfig

input_opt = InputOptimizer(
    config=PerformanceConfig(
        target_latency_ms=16,
        max_concurrent_inputs=100,
        processing_threads=4,
    ),
    optimizations={
        "input batching": True,
        "spatial indexing": True,
        "predictive processing": True,
        "caching": True,
    },
)

# Monitor performance
stats = input_opt.get_stats()
print(f"Input latency: {stats.latency_ms:.2f}ms")
print(f"Processing rate: {stats.processing_rate:.1f}/s")
print(f"Queue size: {stats.queue_size}")
```

### Content Delivery Optimization

```python
from interactive_media import ContentOptimizer, DeliveryConfig

content_opt = ContentOptimizer(
    config=DeliveryConfig(
        cache_size_mb=1024,
        preload_next=True,
        adaptive_quality=True,
        streaming=True,
    ),
    optimizations={
        "video_compression": "h265",
        "audio_compression": "aac",
        "texture_compression": "astc",
        "asset_bundling": True,
    },
)

# Monitor delivery
stats = content_opt.get_stats()
print(f"Cache hit rate: {stats.cache_hit_rate:.2%}")
print(f"Buffer health: {stats.buffer_health:.2f}")
print(f"Quality level: {stats.quality_level}")
```

## Security Considerations

### Data Privacy

```python
from interactive_media import PrivacyManager, DataProtection

privacy = PrivacyManager(
    config=DataProtection(
        anonymize_visitor_data=True,
        encrypt_sensitive_data=True,
        data_retention_days=30,
        consent_management=True,
        right_to_erasure=True,
    },
)

# Anonymize data
anonymized_data = privacy.anonymize(visitor_data)

# Export with privacy
export_data = privacy.export(
    data=analytics_data,
    format="json",
    include_metadata=False,
)
```

### Content Security

```python
from interactive_media import ContentSecurity, DRMConfig

content_security = ContentSecurity(
    drm=DRMConfig(
        enabled=True,
        watermark=True,
        copy_protection=True,
        encryption_algorithm="aes-256",
    ),
)

# Protect content
protected_video = content_security.encrypt("video.mp4")
secure_store.put("video.enc", protected_video)
```

## Troubleshooting Guide

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Input lag** | Delayed response | Reduce processing complexity, optimize pipeline |
| **State machine stuck** | Content not changing | Check transition conditions, restart |
| **Analytics not recording** | No data collected | Check database connection, verify tracking |
| **Content buffering** | Jerky playback | Increase cache, check network |
| **Privacy violations** | Data exposed | Review data collection, implement anonymization |
| **Memory leaks** | Growing memory | Check object pooling, release resources |

## API Reference

```python
class InputProcessor:
    """Process user input."""
    
    def __init__(self, config: InputConfig):
        """Initialize input processor."""
        
    def add_touch_surface(self, surface_id: str, max_points: int) -> None:
        """Add touch surface."""

class StateMachine:
    """Manage interactive states."""
    
    def __init__(self, initial_state: str):
        """Initialize state machine."""
        
    def add_state(self, state_id: str, content: str, duration: float = None) -> None:
        """Add state."""
        
    def trigger(self, trigger: str, data: dict = None) -> None:
        """Trigger state transition."""

class Analytics:
    """Track visitor analytics."""
    
    def __init__(self, config: AnalyticsConfig):
        """Initialize analytics."""
        
    def create_visitor(self, visitor_id: str) -> VisitorProfile:
        """Create visitor profile."""
```

## Data Models

```python
@dataclass
class VisitorProfile:
    """Visitor profile."""
    visitor_id: str
    visits: List[dict]
    interactions: List[dict]
    preferences: dict
    total_duration_s: float
    total_interactions: int

@dataclass
class State:
    """Interactive state."""
    id: str
    content: str
    duration: Optional[float]
    transitions: List[Transition]

@dataclass
class Transition:
    """State transition."""
    from_state: str
    to_state: str
    trigger: str
    condition: Optional[str]

@dataclass
class AnalyticsEvent:
    """Analytics event."""
    event_type: str
    timestamp: float
    visitor_id: str
    data: dict
```

## Deployment Guide

### Installation Setup

```python
from interactive_media import InstallationSetup, SetupConfig

setup_config = SetupConfig(
    name="Interactive Exhibit",
    venue="Museum of Modern Art",
    max_concurrent_visitors=20,
    input_types=["touch", "proximity", "voice"],
    content_storage="local",
    database="postgresql",
)

setup = InstallationSetup(config=setup_config)
setup.deploy()
```

## Monitoring & Observability

```python
from interactive_media import InstallationMonitor, Metrics

monitor = InstallationMonitor(
    metrics=Metrics(
        tracks=[
            "visitor_count",
            "dwell_time",
            "interaction_rate",
            "content_engagement",
            "system_health",
        ],
        sample_rate=1.0,
    ),
    alerts={
        "visitor_count_low": {"threshold": 5, "action": "notify"},
        "system_health_poor": {"threshold": 0.8, "action": "restart"},
    },
)

monitor.start()
```

## Testing Strategy

```python
import pytest
from interactive_media import StateMachine, InputProcessor

class TestStateMachine:
    def test_state_transition(self):
        sm = StateMachine(initial_state="idle")
        sm.add_state("idle", "ambient.mp4")
        sm.add_state("active", "interactive.mp4")
        sm.add_transition("idle", "active", "start")
        
        sm.trigger("start")
        assert sm.current_state == "active"

class TestInputProcessor:
    def test_touch_input(self):
        inputs = InputProcessor(config=InputConfig())
        inputs.add_touch_surface("wall", max_points=10)
        
        # Simulate touch
        inputs.process_touch({"x": 100, "y": 200})
        assert inputs.touch_count == 1
```

## Versioning & Migration

| Version | Changes | Breaking |
|---------|---------|----------|
| 2.0.0 | Added voice recognition, improved analytics | Yes |
| 1.5.0 | Added proximity sensing | No |
| 1.0.0 | Initial release | N/A |

## Glossary

| Term | Definition |
|------|------------|
| **State Machine** | Manages interactive states and transitions |
| **Input Fusion** | Combines multiple input sources |
| **Analytics** | Tracks visitor behavior and engagement |
| **Adaptive Content** | Content that changes based on behavior |
| **Session** | Single visitor interaction period |
| **Dwell Time** | Time spent in experience |
| **Interaction Rate** | Interactions per visitor |

## Changelog

### 2.0.0 (2024-01-15)
- Added voice recognition
- Improved analytics
- Added adaptive content

### 1.5.0 (2023-10-01)
- Added proximity sensing
- Improved state machine

### 1.0.0 (2023-06-01)
- Initial release

## Contributing Guidelines

```bash
git clone https://github.com/company/interactive-media.git
cd interactive-media
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Company Name

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

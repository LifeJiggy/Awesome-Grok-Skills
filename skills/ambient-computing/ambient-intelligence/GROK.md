---
name: "ambient-intelligence"
category: "ambient-computing"
version: "2.0.0"
tags: ["ambient-intelligence", "amI", "smart-space", "pervasive", "adaptive-environment", "context"]
---

# Ambient Intelligence

## Overview

Ambient Intelligence (AmI) platform for creating environments that are sensitive and responsive to human presence and activity. This module integrates context awareness, proactive services, natural interaction, and adaptive environments to deliver invisible computing experiences where technology disappears into the background. Supports smart homes, smart offices, healthcare facilities, retail environments, and museum/exhibition spaces with emphasis on privacy, user comfort, and seamless human-computer interaction.

## Core Capabilities

- **Proactive Services**: Anticipate user needs based on learned patterns, context, and preferences without explicit requests
- **Natural Interaction**: Support voice, gesture, gaze, and presence-based interaction without requiring conscious device operation
- **Adaptive Environments**: Dynamically adjust lighting, climate, audio, and visual displays based on occupant preferences and activities
- **Occupancy Analytics**: Understand space utilization patterns, flow dynamics, and comfort metrics
- **Personalization Engine**: Learn individual preferences and adapt environment settings per-user in shared spaces
- **Privacy-First Design**: On-device processing, anonymized analytics, and transparent data usage controls
- **Interoperability**: Connect heterogeneous smart devices across protocols into unified ambient experiences
- **Sentiment-Aware**: Adapt environment based on detected emotional states (optional, opt-in)

## Usage

```python
from ambient_intelligence import (
    AmbientEnvironment, ProactiveService, PersonalizationEngine, OccupancyAnalytics
)

# Define an ambient environment
env = AmbientEnvironment(name="Smart Office Floor 3")

# Configure adaptive zones
env.add_zone(
    zone_id="open-desk-area",
    name="Open Workspace",
    adaptive_lighting=True,
    adaptive_climate=True,
    adaptive_audio=True,
    comfort_targets={"temperature_f": 72, "humidity_pct": 45, "noise_db": 35},
)

# Add proactive services
service = ProactiveService(
    service_id="morning-welcome",
    trigger="user_arrives + time_between(7,9)",
    actions=[
        "adjust_lighting(warm, 70%)",
        "set_temperature(preferred)",
        "play_news_briefing(volume:low)",
        "display_schedule(on_desk_display)",
    ],
    learning_enabled=True,
)
env.add_service(service)

# Start environment
env.start()
status = env.get_status()
print(f"Active occupants: {status['occupants']}")
print(f"Active services: {status['active_services']}")
print(f"Comfort score: {status['comfort_score']:.1f}/100")
```

```python
# Personalization
personalization = PersonalizationEngine()
personalization.add_user(
    user_id="user-alice",
    preferences={
        "lighting_temp": "warm",
        "lighting_brightness": 70,
        "temperature_f": 71,
        "music_genre": "ambient",
        "display_layout": "minimal",
    },
)
personalization.add_user(
    user_id="user-bob",
    preferences={
        "lighting_temp": "cool",
        "lighting_brightness": 90,
        "temperature_f": 69,
        "music_genre": "none",
        "display_layout": "detailed",
    },
)

# Multi-occupant adaptation
adaptation = personalization.resolve_conflicts(
    occupants=["user-alice", "user-bob"],
    conflict_params=["temperature_f", "lighting_brightness"],
)
print(f"Compromise temperature: {adaptation['temperature_f']}°F")
print(f"Compromise brightness: {adaptation['lighting_brightness']}%")
```

## Best Practices

- Design for the "zero UI" — the best ambient intelligence is invisible to users
- Always provide manual overrides — users must feel in control, not controlled
- Implement opt-in only for sentiment detection and behavioral profiling
- Use federated learning to improve ambient models without centralizing personal data
- Create comfort baselines per user and per space before activating adaptive behaviors
- Gradually introduce ambient features — don't overwhelm with too many simultaneous adaptations
- Design for shared spaces with conflict resolution for multi-occupant preferences
- Log all ambient decisions for transparency and debugging, but anonymize personal data
- Implement "ambient silence" periods where the environment stops adapting
- Test ambient systems with diverse user groups — comfort preferences vary widely

## Related Modules

- **context-aware** — Core context modeling that ambient intelligence builds upon
- **proximity-sensing** — Presence detection for triggering ambient services
- **iot-integration** — Device control for environmental adjustments
- **smart-environments** — Building-level ambient infrastructure
- **ai-ml** → **federated-learning** — Privacy-preserving ambient model training

## Advanced Configuration

### YAML Configuration
```yaml
version: "2.0.0"
settings:
  mode: "production"
  concurrency: 4
  timeout_ms: 30000
  protocols:
    mqtt:
      broker: "mqtt://localhost:1883"
      keepalive: 60
    zigbee:
      port: "/dev/ttyUSB0"
      baudrate: 115200
```

### JSON Configuration
```json
{"version":"2.0.0","settings":{"mode":"production","protocols":{"mqtt":{"broker":"mqtt://localhost:1883"}}}}
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SKILL_MODE` | Runtime mode | `production` |
| `MQTT_BROKER` | MQTT broker URL | `mqtt://localhost:1883` |
| `SKILL_TIMEOUT` | Timeout (ms) | `30000` |
| `ZIGBEE_PORT` | Zigbee serial port | `/dev/ttyUSB0` |
| `BLE_ADAPTER` | BLE adapter | `hci0` |

## Architecture Patterns

### System Architecture
```
+---------------------------------------------------+
|                 Device Layer                       |
|  +----------+  +----------+  +------------------+  |
|  | Sensors  |  | Actuator |  |  Edge Gateway    |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|              Protocol Layer                        |
|  +----------+  +----------+  +------------------+  |
|  |   MQTT   |  | Zigbee   |  |  BLE / Z-Wave    |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|          Processing Layer                          |
|  +----------+  +----------+  +------------------+  |
|  | Protocol |  |  Rules   |  |  Context         |  |
|  | Translator| |  Engine  |  |  Engine          |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|                 Cloud Layer                         |
|  +----------+  +----------+  +------------------+  |
|  |  Device  |  | Analytics|  |  Automation      |  |
|  | Registry |  |  Engine   |  |  Orchestrator    |  |
|  +----------+  +----------+  +------------------+  |
+---------------------------------------------------+
```

### Data Flow
```
Sensor -> Protocol -> Gateway -> Process -> Store -> Cloud
  |         |          |         |        |
  +---------+----------+---------+--------+
              Event-Driven Pipeline
```

## Integration Guide

### Home Assistant
```python
ha_config = {"url": "http://localhost:8123", "token": "your-token"}
```

### MQTT
```python
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.subscribe("devices/+/state")
```

## Performance Optimization

| Operation | Throughput | Latency (p50) | Latency (p99) |
|-----------|-----------|---------------|---------------|
| MQTT Publish | 10,000 msg/s | 1ms | 5ms |
| State Update | 5,000 ops/s | 2ms | 10ms |
| Rule Evaluation | 1,000 eval/s | 5ms | 25ms |

### Tips
1. Edge processing reduces latency
2. MQTT QoS 0 for telemetry, QoS 1 for commands
3. Batch updates for efficiency
4. Connection pooling for brokers

## Security Considerations

| Threat | Risk | Mitigation |
|--------|------|------------|
| Device spoofing | High | X.509 certificates |
| Man-in-the-middle | High | TLS 1.3 |
| Command injection | High | Input validation |
| Firmware tampering | Medium | Signed firmware |

### Checklist
- [ ] Device authentication enabled
- [ ] MQTT encrypted (TLS 1.3)
- [ ] Firmware signed
- [ ] Network segmentation
- [ ] Rate limiting on commands

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| Device offline | Battery/signal | Check battery, range |
| MQTT lost | Network | Check broker, network |
| State stale | Subscription | Verify topic subscription |
| Rule not firing | Conditions | Debug rule engine |

## API Reference

### `init(config: Config) -> Instance`
Initialize.

### `register_device(device: Device) -> DeviceInfo`
Register device.

### `set_state(device_id: str, state: dict) -> bool`
Update state.

### `get_state(device_id: str) -> dict`
Get state.

## Data Models

### Device Schema
```json
{"type":"object","required":["device_id","type","protocol"],"properties":{"device_id":{"type":"string"},"type":{"type":"string"},"protocol":{"type":"string"}}}
```

## Deployment Guide

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 1883 8080
HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "main.py"]
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skill-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: skill
  template:
    spec:
      containers:
      - name: skill
        image: skill:2.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Monitoring & Observability

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `devices_online` | Gauge | Online devices | Drop > 10% |
| `messages_total` | Counter | MQTT messages | -- |
| `message_latency_ms` | Histogram | Message latency | p99 > 100ms |
| `errors_total` | Counter | Errors | > 0 |

## Testing Strategy

```python
def test_register_device():
    result = skill.register_device(test_device)
    assert result.device_id is not None

def test_set_state():
    result = skill.set_state("device-001", {"on": True})
    assert result == True
```

## Versioning & Migration

- Major version for breaking changes
- 6-month deprecation notice

### Changelog
- **[2.0.0]** -- New architecture, edge processing
- **[1.5.0]** -- Protocol improvements
- **[1.0.0]** -- Initial release

## Glossary

| Term | Definition |
|------|------------|
| **MQTT** | Message Queuing Telemetry Transport |
| **Zigbee** | Low-power wireless mesh protocol |
| **BLE** | Bluetooth Low Energy |
| **Gateway** | Bridge between devices and cloud |
| **Shadow** | Virtual device state |
| **TTL** | Time-to-live |

## Changelog

### [2.0.0] -- 2024-12-01
- Major release with edge processing

### [1.5.0] -- 2024-06-15
- Performance improvements

### [1.0.0] -- 2024-01-01
- Initial stable release

## Contributing Guidelines

```bash
git clone https://github.com/example/skill.git
cd skill
pip install -e ".[dev]"
pytest
```

## License

MIT License -- Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Proactive Service Templates

### Service Library
```python
SERVICE_TEMPLATES = {
    "morning_welcome": {
        "trigger": "user_arrives + time_between(7,9)",
        "actions": [
            {"type": "lighting", "preset": "warm_gradual", "duration_min": 10},
            {"type": "climate", "target_temp": "preferred", "ramp_time_min": 5},
            {"type": "audio", "content": "morning_briefing", "volume": "low"},
            {"type": "display", "content": "daily_schedule"},
        ],
        "learning": True,
        "user_override": "dismiss",
    },
    "focus_mode": {
        "trigger": "activity=meeting OR calendar_event=focus_block",
        "actions": [
            {"type": "lighting", "preset": "cool_bright", "brightness": 85},
            {"type": "dnd", "level": "total", "duration": "auto"},
            {"type": "climate", "target_temp": 71, "fan": "quiet"},
            {"type": "display", "content": "work_tasks_only"},
        ],
        "learning": False,
        "user_override": "manual",
    },
    "relaxation": {
        "trigger": "time_between(20,23) + presence=home + activity=relaxing",
        "actions": [
            {"type": "lighting", "preset": "warm_dim", "brightness": 30},
            {"type": "audio", "content": "ambient_music", "volume": "low"},
            {"type": "climate", "target_temp": 72, "fan": "off"},
        ],
        "learning": True,
        "user_override": "always",
    },
    "goodnight": {
        "trigger": "time_between(22,1) + bedroom_presence + lights_off",
        "actions": [
            {"type": "lighting", "all_off": True},
            {"type": "climate", "target_temp": 68, "fan": "auto"},
            {"type": "security", "arm": "night"},
            {"type": "display", "content": "night_mode"},
        ],
        "learning": False,
        "user_override": "manual",
    },
}
```

### Service Execution Engine
```python
class ProactiveServiceEngine:
    def __init__(self, context_manager, device_controller):
        self.context = context_manager
        self.devices = device_controller
        self.active_services = {}
        self.execution_history = []

    def evaluate_services(self, services: list) -> list:
        triggered = []
        for service in services:
            if self._matches_trigger(service.trigger):
                if self._passes_conditions(service.get("conditions", [])):
                    execution = self._execute_service(service)
                    triggered.append(execution)
        return triggered

    def _execute_service(self, service: dict) -> dict:
        results = []
        for action in service["actions"]:
            result = self._execute_action(action)
            results.append(result)
            self.execution_history.append({
                "service": service["name"],
                "action": action["type"],
                "result": result,
                "timestamp": datetime.now(),
            })
        return {"service": service["name"], "actions": len(results), "success": all(r["ok"] for r in results)}
```

## Personalization Algorithms

### Multi-Objective Preference Optimization
```python
class PersonalizationOptimizer:
    def __init__(self, num_users: int, num_parameters: int):
        self.user_models = {}
        self.global_model = np.zeros(num_parameters)
        self.conflict_resolution = "weighted_average"

    def update_user_model(self, user_id: str, feedback: dict):
        """Update user model based on explicit or implicit feedback."""
        if user_id not in self.user_models:
            self.user_models[user_id] = np.zeros(len(self.global_model))

        gradient = self._compute_gradient(feedback)
        self.user_models[user_id] += 0.01 * gradient

    def resolve_multi_user(self, user_ids: list) -> dict:
        """Resolve environment settings for multiple occupants."""
        if len(user_ids) == 1:
            return self._user_settings(user_ids[0])

        user_settings = [self._user_settings(uid) for uid in user_ids]
        return self._conflict_resolution(user_settings)

    def _conflict_resolution(self, settings_list: list) -> dict:
        resolved = {}
        for param in settings_list[0].keys():
            values = [s[param] for s in settings_list if param in s]
            if all(isinstance(v, (int, float)) for v in values):
                resolved[param] = np.mean(values)
            else:
                from collections import Counter
                resolved[param] = Counter(values).most_common(1)[0][0]
        return resolved
```

### Learning Rate Adaptation
```python
class AdaptiveLearningRate:
    def __init__(self, initial_lr: float = 0.1, decay: float = 0.99):
        self.lr = initial_lr
        self.decay = decay
        self.iterations = 0
        self.performance_history = []

    def step(self, performance: float):
        self.iterations += 1
        self.performance_history.append(performance)
        if len(self.performance_history) > 100:
            self.performance_history.pop(0)
        recent = self.performance_history[-10:]
        if len(recent) >= 10:
            improvement = recent[-1] - recent[0]
            if improvement < 0:
                self.lr *= self.decay
            elif improvement > 0.1:
                self.lr = min(self.lr * 1.1, 0.5)
```

## Sentiment-Aware Environments

### Emotion Detection Pipeline
```python
class SentimentDetector:
    def __init__(self):
        self.models = {
            "facial": "resnet_emotion_v2",
            "voice": "audio_emotion_v1",
            "physiological": "hrv_emotion_v1",
        }

    def detect_from_facial(self, image: np.ndarray) -> dict:
        emotions = self._run_facial_model(image)
        return {
            "primary_emotion": max(emotions, key=emotions.get),
            "confidence": max(emotions.values()),
            "emotions": emotions,
        }

    def detect_from_voice(self, audio: np.ndarray) -> dict:
        features = self._extract_audio_features(audio)
        emotion = self._classify_emotion(features)
        return {"emotion": emotion["label"], "arousal": emotion["arousal"], "valence": emotion["valence"]}

    def fuse_sentiments(self, facial: dict, voice: dict, physiological: dict) -> dict:
        weighted = {
            "facial": 0.5, "voice": 0.3, "physiological": 0.2
        }
        fused_arousal = (
            weighted["facial"] * facial.get("arousal", 0) +
            weighted["voice"] * voice.get("arousal", 0) +
            weighted["physiological"] * physiological.get("arousal", 0)
        )
        return {
            "arousal": fused_arousal,
            "recommended_adjustment": self._arousal_to_adjustment(fused_arousal),
        }

    def _arousal_to_adjustment(self, arousal: float) -> dict:
        if arousal > 0.5:
            return {"lighting": "cool_bright", "audio": "calming", "temperature": "slightly_cool"}
        elif arousal < -0.5:
            return {"lighting": "warm_bright", "audio": "energizing", "temperature": "slightly_warm"}
        return {"lighting": "neutral", "audio": "off", "temperature": "comfort"}
```

### Ethical Guidelines for Sentiment Detection
| Guideline | Implementation |
|-----------|----------------|
| Opt-in only | Never enable without explicit user consent |
| On-device processing | Never send facial/voice data to cloud |
| No individual profiling | Aggregate anonymized patterns only |
| Override always | User can disable sentiment detection anytime |
| Transparency | Show users what data is collected and how it's used |

## Ambient UX Design Principles

### Zero-UI Interaction Patterns
```python
ZERO_UI_PATTERNS = {
    "gradual_transition": {
        "description": "Lighting/temperature changes happen over 30-60s, not instantly",
        "implementation": "interpolate(current, target, steps=30, easing='ease_in_out')",
        "user_perception": "Environment feels natural, not robotic",
    },
    "ambient_feedback": {
        "description": "Subtle environment changes indicate system state",
        "examples": {
            "system_ready": "Soft pulse of warm light",
            "processing": "Gentle hum or light flicker",
            "error": "Brief cool blue flash",
            "attention_needed": "Gradual brightness increase",
        },
    },
    "invisible_automation": {
        "description": "Most actions happen without user awareness",
        "principle": "If the user notices the automation, it's too obvious",
        "exception": "Safety-critical alerts must be noticeable",
    },
    "contextual_fade": {
        "description": "Services fade in/out based on relevance",
        "implementation": "relevance_score > 0.7 ? fade_in : fade_out",
        "transition_time_s": 10,
    },
}
```

### Comfort Scoring Algorithm
```python
class ComfortScorer:
    WEIGHTS = {
        "temperature": 0.30,
        "humidity": 0.15,
        "lighting": 0.20,
        "noise": 0.15,
        "air_quality": 0.10,
        "ergonomics": 0.10,
    }

    IDEAL_RANGES = {
        "temperature_f": (70, 74),
        "humidity_pct": (40, 55),
        "lighting_lux": (300, 500),
        "noise_db": (30, 45),
        "co2_ppm": (400, 800),
    }

    def score(self, measurements: dict) -> dict:
        scores = {}
        for param, (low, high) in self.IDEAL_RANGES.items():
            value = measurements.get(param, (low + high) / 2)
            if low <= value <= high:
                scores[param] = 100
            elif value < low:
                scores[param] = max(0, 100 - (low - value) * 5)
            else:
                scores[param] = max(0, 100 - (value - high) * 5)

        weighted_sum = sum(scores.get(p, 50) * w for p, w in self.WEIGHTS.items())
        return {"overall": weighted_sum, "breakdown": scores}
```

## Multi-Occupant Conflict Resolution

### Conflict Resolution Strategies
```python
class OccupantConflictResolver:
    STRATEGIES = {
        "weighted_average": lambda values: np.mean(values),
        "median": lambda values: np.median(values),
        "majority_vote": lambda values: Counter(values).most_common(1)[0][0],
        "most_constrained": lambda values: min(values) if all(v > 0 for v in values) else max(values),
        "turn_based": lambda values: values[int(time.time()) % len(values)],
        "priority_based": lambda values, priorities=None: values[np.argmax(priorities)] if priorities else values[0],
    }

    def resolve(self, user_preferences: dict, strategy: str = "weighted_average") -> dict:
        resolved = {}
        all_params = set()
        for prefs in user_preferences.values():
            all_params.update(prefs.keys())

        for param in all_params:
            values = [prefs[param] for prefs in user_preferences.values() if param in prefs]
            if all(isinstance(v, (int, float)) for v in values):
                resolved[param] = self.STRATEGIES[strategy](values)
            else:
                resolved[param] = self.STRATEGIES["majority_vote"](values)
        return resolved
```

## Ambient Silence Configuration

### Silence Period Management
```python
class AmbientSilenceManager:
    def __init__(self):
        self.silence_periods = []
        self.active = False

    def add_silence_period(self, start_time: str, end_time: str, days: list = None):
        self.silence_periods.append({
            "start": start_time,
            "end": end_time,
            "days": days or ["mon", "tue", "wed", "thu", "fri", "sat", "sun"],
        })

    def is_silence_active(self) -> bool:
        now = datetime.now()
        current_day = now.strftime("%a").lower()
        current_time = now.strftime("%H:%M")
        for period in self.silence_periods:
            if current_day in period["days"]:
                if period["start"] <= current_time <= period["end"]:
                    return True
        return False

    def get_silence_actions(self) -> dict:
        return {
            "adaptive_lighting": "hold_current",
            "adaptive_climate": "hold_setpoint",
            "proactive_services": "disable",
            "notifications": "silent",
            "learning_updates": "pause",
        }
```

## Ambient Learning Pipeline

### Feedback Collection
```python
class AmbientLearningPipeline:
    def __init__(self):
        self.feedback_store = []
        self.model_version = 0

    def collect_explicit_feedback(self, user_id: str, service_id: str, rating: int, comment: str = ""):
        self.feedback_store.append({
            "user_id": user_id,
            "service_id": service_id,
            "rating": rating,
            "comment": comment,
            "timestamp": datetime.now(),
            "type": "explicit",
        })

    def collect_implicit_feedback(self, user_id: str, service_id: str, action: str):
        """Implicit feedback from user behavior."""
        self.feedback_store.append({
            "user_id": user_id,
            "service_id": service_id,
            "action": action,
            "timestamp": datetime.now(),
            "type": "implicit",
        })

    def train_models(self):
        """Periodic model retraining."""
        explicit = [f for f in self.feedback_store if f["type"] == "explicit"]
        implicit = [f for f in self.feedback_store if f["type"] == "implicit"]
        if len(explicit) + len(implicit) > 100:
            self._retrain(explicit, implicit)
            self.model_version += 1
            self.feedback_store = []
```

## Ambient Scene Composition

### Scene Definition
```python
class AmbientScene:
    def __init__(self, name: str):
        self.name = name
        self.layers = []

    def add_lighting_layer(self, config: dict):
        self.layers.append({"type": "lighting", "config": config})

    def add_audio_layer(self, config: dict):
        self.layers.append({"type": "audio", "config": config})

    def add_climate_layer(self, config: dict):
        self.layers.append({"type": "climate", "config": config})

    def add_visual_layer(self, config: dict):
        self.layers.append({"type": "visual", "config": config})

    def compose(self) -> dict:
        return {
            "scene": self.name,
            "layers": self.layers,
            "transition_time_s": 15,
            "easing": "ease_in_out",
        }

SCENE_PRESETS = {
    "work_focus": AmbientScene("Work Focus").add_lighting_layer(
        {"brightness": 85, "color_temp": 5000, "distribution": "even"}
    ).add_audio_layer(
        {"type": "white_noise", "volume": 20}
    ).compose(),
    "social_gathering": AmbientScene("Social").add_lighting_layer(
        {"brightness": 60, "color_temp": 3000, "distribution": "warm_accent"}
    ).add_audio_layer(
        {"type": "background_music", "genre": "ambient", "volume": 30}
    ).compose(),
}
```

## Ambient Accessibility

### Accessibility Features
```python
class AccessibilityManager:
    def __init__(self):
        self.user_accessibility_profiles = {}

    def set_profile(self, user_id: str, profile: dict):
        self.user_accessibility_profiles[user_id] = profile

    def adapt_for_accessibility(self, base_settings: dict, user_id: str) -> dict:
        profile = self.user_accessibility_profiles.get(user_id, {})
        adapted = base_settings.copy()

        if profile.get("visual_impairment") == "high":
            adapted["lighting"]["brightness"] = max(adapted["lighting"]["brightness"], 90)
            adapted["lighting"]["contrast"] = "high"
            adapted["audio"]["announcements"] = True

        if profile.get("hearing_impairment"):
            adapted["visual_cues"] = True
            adapted["audio"]["volume"] = 0
            adapted["vibration_alerts"] = True

        if profile.get("motor_impairment"):
            adapted["interaction_mode"] = "voice_first"
            adapted["response_time_extended"] = True

        return adapted
```

## Ambient Testing Methodology

### Test Scenarios
| Scenario | Duration | Metrics | Pass Criteria |
|----------|----------|---------|---------------|
| Morning routine | 2 hours | Comfort score, energy use | Score > 85 |
| Meeting mode | 1 hour | DND activation, lighting | < 2s activation |
| Multi-occupant | 3 hours | Conflict resolution | No complaints |
| Sensor failure | 30 min | Graceful degradation | Core services active |
| Overnight | 8 hours | Energy efficiency, sleep quality | < 5% variation |
| Privacy test | 1 hour | Data collection | No raw sensor storage |

### A/B Testing Framework
```python
class AmbientABTest:
    def __init__(self, test_name: str, variant_a: dict, variant_b: dict):
        self.test_name = test_name
        self.variants = {"A": variant_a, "B": variant_b}
        self.assignments = {}
        self.metrics = {"A": [], "B": []}

    def assign_user(self, user_id: str) -> str:
        variant = "A" if hash(user_id) % 2 == 0 else "B"
        self.assignments[user_id] = variant
        return variant

    def record_metric(self, user_id: str, metric_name: str, value: float):
        variant = self.assignments.get(user_id, "A")
        self.metrics[variant].append({"metric": metric_name, "value": value})

    def get_results(self) -> dict:
        results = {}
        for variant in ["A", "B"]:
            values = [m["value"] for m in self.metrics[variant]]
            results[variant] = {
                "mean": np.mean(values) if values else 0,
                "std": np.std(values) if values else 0,
                "n": len(values),
            }
        return results
```

---
name: "context-aware"
category: "ambient-computing"
version: "2.0.0"
tags: ["context-aware", "pervasive-computing", "activity-recognition", "location", "user-modeling", "adaptive"]
---

# Context-Aware Computing

## Overview

Context-aware computing framework for building adaptive applications that sense, interpret, and respond to user and environmental context in real-time. This module implements multi-dimensional context modeling (location, activity, social, temporal, environmental), context fusion from heterogeneous sensor sources, activity recognition using machine learning, user preference learning, and adaptive application behavior. Supports smart homes, smart offices, healthcare monitoring, and retail environments with privacy-preserving context processing.

## Core Capabilities

- **Context Modeling**: Multi-dimensional context representation covering location, activity, identity, time, social, and environmental dimensions
- **Sensor Fusion**: Combine GPS, WiFi, BLE beacons, accelerometers, gyroscopes, and environmental sensors into unified context
- **Activity Recognition**: ML-based recognition of user activities (walking, sitting, sleeping, cooking, exercising) from sensor streams
- **Location Intelligence**: Indoor positioning via WiFi fingerprinting, BLE trilateration, and PDR (pedestrian dead reckoning)
- **User Modeling**: Adaptive user profiles with preference learning, habit detection, and anomaly flagging
- **Context Inference**: Infer high-level context (meeting, commuting, relaxing) from low-level sensor data
- **Privacy Framework**: On-device context processing, anonymization, and user consent management
- **Adaptive Behavior**: Application behavior modification based on inferred context changes

## Usage

```python
from context_aware import (
    ContextManager, ContextDimension, ActivityRecognizer, LocationEngine
)

# Initialize context manager
ctx = ContextManager(user_id="user-001")

# Update context dimensions
ctx.update_dimension(ContextDimension.LOCATION, {
    "type": "indoor",
    "building": "office",
    "floor": 3,
    "room": "conference-room-A",
    "accuracy_m": 2.0,
})

ctx.update_dimension(ContextDimension.ACTIVITY, {
    "primary": "meeting",
    "confidence": 0.92,
    "secondary": "sitting",
    "duration_min": 45,
})

ctx.update_dimension(ContextDimension.ENVIRONMENTAL, {
    "temperature_f": 72.5,
    "humidity_pct": 45,
    "noise_level_db": 42,
    "light_lux": 350,
})

# Get current context
current = ctx.get_context()
print(f"Activity: {current['activity']['primary']}")
print(f"Location: {current['location']['room']}")
print(f"Environment: {current['environmental']['temperature_f']}°F")

# Activity recognition from sensor stream
recognizer = ActivityRecognizer(model="lstm_v2")
activities = recognizer.recognize(sensor_stream=[
    {"accel_x": 0.02, "accel_y": 0.01, "accel_z": 9.8, "gyro_x": 0.0, "timestamp": "2024-01-01T12:00:00"},
    {"accel_x": 0.15, "accel_y": -0.10, "accel_z": 9.6, "gyro_x": 0.5, "timestamp": "2024-01-01T12:00:01"},
])
for act in activities:
    print(f"  {act['activity']}: {act['confidence']:.2f}")
```

```python
# Adaptive behavior based on context
from context_aware import AdaptiveEngine

adaptive = AdaptiveEngine(context_manager=ctx)
adaptive.add_rule(
    context_condition={"activity": "meeting", "location.type": "indoor"},
    behavior={"mute_notifications": True, "brightness": "low", "dnd": True},
)
adaptive.add_rule(
    context_condition={"activity": "sleeping"},
    behavior={"all_lights": "off", "thermostat": 68, "alarm_enabled": True},
)
changes = adaptive.evaluate()
print(f"Adaptive changes: {len(changes)}")
```

## Best Practices

- Process context on-device whenever possible to minimize privacy exposure and latency
- Use confidence thresholds — never act on context inference with less than 70% confidence
- Implement graceful degradation when sensors are unavailable or inaccurate
- Use temporal smoothing (moving average) to avoid rapid context switching
- Provide users with transparent context dashboards and easy override controls
- Separate raw sensor data from inferred context in storage and logging
- Use differential privacy when aggregating context data across users
- Implement context caching to avoid redundant sensor queries
- Design adaptive behaviors that are reversible and don't annoy users
- Log context changes with sufficient detail for debugging without storing raw sensor data

## Related Modules

- **proximity-sensing** — BLE/UWB proximity data feeds location context
- **iot-integration** — IoT sensor data as context sources
- **ambient-intelligence** — Higher-level ambient intelligence built on context awareness
- **smart-environments** — Environment-level context for building automation
- **ai-ml** → **federated-learning** — Privacy-preserving context model training

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

## Context Fusion Algorithms

### Weighted Fusion
```python
class WeightedContextFusion:
    def __init__(self):
        self.source_weights = {
            "gps": 0.3,
            "wifi_rssi": 0.25,
            "ble_beacon": 0.25,
            "accelerometer": 0.1,
            "gyroscope": 0.1,
        }

    def fuse(self, readings: dict) -> dict:
        fused = {}
        for dimension in ["latitude", "longitude", "accuracy"]:
            weighted_sum = 0
            weight_total = 0
            for source, value in readings.items():
                if dimension in value and source in self.source_weights:
                    w = self.source_weights[source]
                    weighted_sum += value[dimension] * w
                    weight_total += w
            if weight_total > 0:
                fused[dimension] = weighted_sum / weight_total
        return fused
```

### Bayesian Fusion
```python
import numpy as np

class BayesianContextFusion:
    def __init__(self, prior: dict):
        self.prior = prior  # P(context) initial beliefs

    def update(self, observation: dict, likelihood_model: dict):
        posterior = {}
        for context, prior_prob in self.prior.items():
            likelihood = likelihood_model.get(context, 0.5)
            posterior[context] = prior_prob * likelihood
        total = sum(posterior.values())
        self.prior = {k: v / total for k, v in posterior.items()}
        return self.prior

    def get_most_likely(self) -> str:
        return max(self.prior, key=self.prior.get)
```

### Kalman Filter for Context Tracking
```python
class ContextKalmanFilter:
    def __init__(self, state_dim: int, process_noise: float = 0.01):
        self.state = np.zeros(state_dim)
        self.covariance = np.eye(state_dim)
        self.Q = np.eye(state_dim) * process_noise  # process noise
        self.R = np.eye(state_dim) * 0.1  # measurement noise

    def predict(self, dt: float):
        F = np.eye(len(self.state))
        self.state = F @ self.state
        self.covariance = F @ self.covariance @ F.T + self.Q

    def update(self, measurement: np.ndarray):
        H = np.eye(len(self.state))
        y = measurement - H @ self.state
        S = H @ self.covariance @ H.T + self.R
        K = self.covariance @ H.T @ np.linalg.inv(S)
        self.state = self.state + K @ y
        self.covariance = (np.eye(len(self.state)) - K @ H) @ self.covariance
```

## Activity Recognition ML Pipeline

### Feature Extraction
```python
class ActivityFeatureExtractor:
    def extract(self, sensor_data: list) -> dict:
        accel = [s["accel_magnitude"] for s in sensor_data]
        gyro = [s["gyro_magnitude"] for s in sensor_data]
        return {
            "accel_mean": np.mean(accel),
            "accel_std": np.std(accel),
            "accel_max": np.max(accel),
            "accel_min": np.min(accel),
            "accel_entropy": self._entropy(accel),
            "gyro_mean": np.mean(gyro),
            "gyro_std": np.std(gyro),
            "gyro_max": np.max(gyro),
            "zero_crossing_rate": self._zcr(accel),
            "mean_crossing_rate": self._mcr(accel),
            "dominant_frequency": self._dominant_freq(accel),
            "spectral_energy": np.sum(np.array(accel) ** 2),
            "autocorrelation": self._autocorr(accel),
            "window_length": len(sensor_data),
        }
```

### Activity Labels
| Activity | Class | Typical Sensors | Duration Range |
|----------|-------|-----------------|----------------|
| Walking | 0 | Accelerometer, Gyroscope | Continuous |
| Running | 1 | Accelerometer, Gyroscope | Continuous |
| Sitting | 2 | Accelerometer | > 5 min |
| Standing | 3 | Accelerometer, Barometer | > 1 min |
| Lying Down | 4 | Accelerometer, Gyroscope | > 5 min |
| Climbing Stairs | 5 | Accelerometer, Barometer | 10-60s |
| Cycling | 6 | Accelerometer, Gyroscope | Continuous |
| Cooking | 7 | Accelerometer, Microphone | 5-60 min |
| Sleeping | 8 | Accelerometer, Heart Rate | 4-10 hours |

### Model Architecture
```python
import torch.nn as nn

class ActivityRecognitionLSTM(nn.Module):
    def __init__(self, input_dim=13, hidden_dim=128, num_layers=2, num_classes=9):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, num_layers, batch_first=True, dropout=0.3)
        self.attention = nn.MultiheadAttention(hidden_dim, num_heads=4)
        self.classifier = nn.Sequential(
            nn.Linear(hidden_dim, 64),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        attn_out, _ = self.attention(lstm_out, lstm_out, lstm_out)
        last_hidden = attn_out[:, -1, :]
        return self.classifier(last_hidden)
```

## Indoor Positioning Techniques

### WiFi Fingerprinting
```python
class WiFiFingerprinting:
    def __init__(self, radio_map: dict):
        self.radio_map = radio_map  # {location: {ap_mac: rssi}}

    def localize(self, scan_results: dict) -> tuple:
        """Returns (location_id, confidence)."""
        best_match = None
        best_score = float('inf')
        for loc_id, reference_rssi in self.radio_map.items():
            score = sum(
                (scan_results.get(ap, -100) - ref_rssi) ** 2
                for ap, ref_rssi in reference_rssi.items()
            )
            if score < best_score:
                best_score = score
                best_match = loc_id
        confidence = 1.0 / (1.0 + best_score / 1000)
        return best_match, confidence
```

### BLE Trilateration
```python
import numpy as np

class BLETrilateration:
    def __init__(self, beacon_positions: dict):
        self.beacons = beacon_positions  # {beacon_id: (x, y, z)}

    def rssi_to_distance(self, rssi: float, tx_power: float = -59, n: float = 2.5) -> float:
        return 10 ** ((tx_power - rssi) / (10 * n))

    def trilaterate(self, beacon_readings: dict) -> tuple:
        distances = {}
        for beacon_id, rssi in beacon_readings.items():
            if beacon_id in self.beacons:
                distances[beacon_id] = self.rssi_to_distance(rssi)

        if len(distances) < 3:
            return None, 0.0

        beacons = list(distances.keys())
        A = np.array([
            [2 * (self.beacons[b][0] - self.beacons[beacons[0]][0]),
             2 * (self.beacons[b][1] - self.beacons[beacons[0]][1])]
            for b in beacons[1:]
        ])
        b = np.array([
            distances[beacons[0]]**2 - distances[b]**2
            + self.beacons[b][0]**2 - self.beacons[beacons[0]][0]**2
            + self.beacons[b][1]**2 - self.beacons[beacons[0]][1]**2
            for b in beacons[1:]
        ])
        position, residuals, _, _ = np.linalg.lstsq(A, b, rcond=None)
        confidence = 1.0 / (1.0 + np.mean(residuals))
        return tuple(position), confidence
```

### Pedestrian Dead Reckoning (PDR)
```python
class PedestrianDeadReckoning:
    STEP_LENGTH = 0.7  # meters
    HEADING_SMOOTHING = 0.8

    def __init__(self):
        self.position = (0.0, 0.0)
        self.heading = 0.0
        self.step_count = 0

    def detect_step(self, accel_magnitude: float) -> bool:
        threshold = 11.5  # m/s^2
        return accel_magnitude > threshold

    def update(self, accel_magnitude: float, gyro_z: float):
        if self.detect_step(accel_magnitude):
            self.step_count += 1
            self.heading += gyro_z * 0.01
            self.heading = self.heading % (2 * np.pi)
            dx = self.STEP_LENGTH * np.cos(self.heading)
            dy = self.STEP_LENGTH * np.sin(self.heading)
            self.position = (self.position[0] + dx, self.position[1] + dy)
```

## User Preference Learning

### Collaborative Filtering
```python
class PreferenceLearner:
    def __init__(self, num_users: int, num_preferences: int, embedding_dim: int = 16):
        self.user_embeddings = np.random.randn(num_users, embedding_dim) * 0.01
        self.pref_embeddings = np.random.randn(num_preferences, embedding_dim) * 0.01

    def predict_preference(self, user_id: int, context: dict) -> float:
        user_emb = self.user_embeddings[user_id]
        context_emb = self._encode_context(context)
        return np.dot(user_emb, context_emb)

    def update(self, user_id: int, context: dict, observed_preference: float, lr: float = 0.01):
        predicted = self.predict_preference(user_id, context)
        error = observed_preference - predicted
        self.user_embeddings[user_id] += lr * error * self._encode_context(context)
```

### Habit Detection
```python
class HabitDetector:
    def __init__(self, min_occurrences: int = 5, time_window_minutes: int = 30):
        self.patterns = {}
        self.min_occurrences = min_occurrences
        self.time_window = time_window_minutes

    def record(self, user_id: str, action: str, timestamp: datetime, context: dict):
        key = f"{user_id}:{action}"
        if key not in self.patterns:
            self.patterns[key] = []
        self.patterns[key].append({"time": timestamp, "context": context})

    def detect_habits(self, user_id: str) -> list:
        habits = []
        for key, occurrences in self.patterns.items():
            if not key.startswith(user_id):
                continue
            if len(occurrences) < self.min_occurrences:
                continue
            time_clusters = self._cluster_times(occurrences)
            for cluster in time_clusters:
                if len(cluster) >= self.min_occurrences:
                    habits.append({
                        "action": key.split(":")[1],
                        "typical_time": np.mean([o["time"].hour for o in cluster]),
                        "confidence": len(cluster) / len(occurrences),
                    })
        return habits
```

## Context Caching Strategies

### LRU Context Cache
```python
from collections import OrderedDict

class ContextCache:
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 60):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.ttl = ttl_seconds

    def get(self, key: str) -> dict | None:
        if key in self.cache:
            entry = self.cache[key]
            if time.time() - entry["timestamp"] < self.ttl:
                self.cache.move_to_end(key)
                return entry["context"]
            else:
                del self.cache[key]
        return None

    def put(self, key: str, context: dict):
        if key in self.cache:
            del self.cache[key]
        elif len(self.cache) >= self.max_size:
            self.cache.popitem(last=False)
        self.cache[key] = {"context": context, "timestamp": time.time()}
```

### Predictive Pre-fetching
```python
class PredictivePrefetcher:
    def __init__(self, habit_detector: HabitDetector):
        self.habits = habit_detector

    def get_prefetch_list(self, user_id: str, current_time: datetime) -> list:
        habits = self.habits.detect_habits(user_id)
        upcoming = []
        for habit in habits:
            time_diff = habit["typical_time"] - current_time.hour
            if 0 < time_diff <= 1:
                upcoming.append({
                    "context": habit["action"],
                    "confidence": habit["confidence"],
                    "prefetch_in_minutes": time_diff * 60,
                })
        return upcoming
```

## Sensor Calibration

### Temperature Sensor Calibration
```python
class TemperatureCalibrator:
    def __init__(self):
        self.offset = 0.0
        self.gain = 1.0

    def calibrate(self, reference_readings: list, sensor_readings: list):
        ref = np.array(reference_readings)
        raw = np.array(sensor_readings)
        A = np.column_stack([raw, np.ones(len(raw))])
        self.gain, self.offset = np.linalg.lstsq(A, ref, rcond=None)[0]

    def apply(self, raw_temperature: float) -> float:
        return raw_temperature * self.gain + self.offset
```

### Accelerometer Calibration
```python
class AccelerometerCalibrator:
    def __init__(self):
        self.bias = np.zeros(3)
        self.scale = np.ones(3)

    def calibrate_static(self, readings: list):
        data = np.array(readings)
        self.bias = np.mean(data, axis=0)
        self.bias[2] -= 9.81  # remove gravity
        accel_magnitudes = np.linalg.norm(data - self.bias, axis=1)
        self.scale = 9.81 / np.mean(accel_magnitudes)

    def apply(self, raw: np.ndarray) -> np.ndarray:
        return (raw - self.bias) * self.scale
```

## Temporal Context Modeling

### Time-of-Day Patterns
```python
class TemporalContextModel:
    PERIODS = {
        "early_morning": (5, 7),
        "morning": (7, 12),
        "afternoon": (12, 17),
        "evening": (17, 21),
        "night": (21, 5),
    }

    def get_temporal_context(self, timestamp: datetime) -> dict:
        hour = timestamp.hour
        day_type = "weekday" if timestamp.weekday() < 5 else "weekend"
        period = self._get_period(hour)
        return {
            "hour": hour,
            "day_type": day_type,
            "period": period,
            "is_work_hours": day_type == "weekday" and 9 <= hour <= 17,
            "is_sleeping_hours": hour >= 22 or hour <= 6,
        }
```

### Context Transition Modeling
```python
class ContextTransitionModel:
    def __init__(self):
        self.transitions = {}  # {from_context: {to_context: count}}
        self.total_transitions = {}

    def record_transition(self, from_ctx: str, to_ctx: str):
        if from_ctx not in self.transitions:
            self.transitions[from_ctx] = {}
        self.transitions[from_ctx][to_ctx] = self.transitions[from_ctx].get(to_ctx, 0) + 1
        self.total_transitions[from_ctx] = self.total_transitions.get(from_ctx, 0) + 1

    def get_probability(self, from_ctx: str, to_ctx: str) -> float:
        total = self.total_transitions.get(from_ctx, 0)
        if total == 0:
            return 0.0
        return self.transitions.get(from_ctx, {}).get(to_ctx, 0) / total

    def predict_next(self, current_ctx: str) -> str:
        probs = {}
        for to_ctx in self.transitions.get(current_ctx, {}):
            probs[to_ctx] = self.get_probability(current_ctx, to_ctx)
        return max(probs, key=probs.get) if probs else None
```

## Privacy Framework

### Differential Privacy for Context
```python
import random

class DifferentialPrivacy:
    def __init__(self, epsilon: float = 1.0):
        self.epsilon = epsilon

    def add_noise(self, value: float, sensitivity: float = 1.0) -> float:
        noise = np.random.laplace(0, sensitivity / self.epsilon)
        return value + noise

    def privatize_location(self, lat: float, lon: float, accuracy_m: float = 100) -> tuple:
        lat_noise = self.add_noise(lat, accuracy_m / 111000)
        lon_noise = self.add_noise(lon, accuracy_m / (111000 * np.cos(np.radians(lat))))
        return lat_noise, lon_noise

    def privatize_activity(self, activities: dict) -> dict:
        return {k: max(0, v + self.add_noise(0, 0.1)) for k, v in activities.items()}
```

### Consent Management
```python
class ConsentManager:
    def __init__(self):
        self.consents = {}  # {user_id: {data_type: consent_info}}

    def set_consent(self, user_id: str, data_type: str, granted: bool, purpose: str):
        self.consents.setdefault(user_id, {})[data_type] = {
            "granted": granted,
            "purpose": purpose,
            "timestamp": datetime.now().isoformat(),
            "version": "2.0",
        }

    def has_consent(self, user_id: str, data_type: str) -> bool:
        consent = self.consents.get(user_id, {}).get(data_type)
        return consent is not None and consent["granted"]

    def get_data_usage_report(self, user_id: str) -> dict:
        return {
            dt: {"purpose": c["purpose"], "granted": c["granted"]}
            for dt, c in self.consents.get(user_id, {}).items()
        }
```

## Context Inheritance & Composition

### Context Inheritance Tree
```
Global Context (building-wide)
  -> Floor Context (floor-specific)
    -> Zone Context (room/area)
      -> Device Context (individual device)
        -> User Context (per-user overrides)
```

### Context Composition
```python
class ContextComposer:
    def __init__(self):
        self.layers = []  # ordered from global to local

    def add_layer(self, context: dict, priority: int):
        self.layers.append({"context": context, "priority": priority})
        self.layers.sort(key=lambda x: x["priority"])

    def compose(self) -> dict:
        result = {}
        for layer in self.layers:
            for key, value in layer["context"].items():
                result[key] = value  # higher priority overwrites
        return result
```

## Context Visualization

### Dashboard Data Format
```json
{
  "current_context": {
    "location": {"building": "HQ", "floor": 3, "room": "301"},
    "activity": {"primary": "meeting", "confidence": 0.92},
    "environment": {"temperature_f": 72, "noise_db": 42}
  },
  "context_history": [
    {"timestamp": "2024-01-15T09:00:00Z", "activity": "commuting"},
    {"timestamp": "2024-01-15T09:15:00Z", "activity": "walking"},
    {"timestamp": "2024-01-15T09:20:00Z", "activity": "sitting"}
  ],
  "activity_distribution": {
    "meeting": 0.35, "sitting": 0.30, "walking": 0.15,
    "commuting": 0.10, "other": 0.10
  }
}
```

## Example: Smart Office Context System

```python
from context_aware import ContextManager, ContextDimension, ActivityRecognizer

ctx = ContextManager(user_id="employee-42")

# Initialize with morning context
ctx.update_dimension(ContextDimension.LOCATION, {
    "type": "indoor", "building": "HQ", "floor": 3, "room": "desk-42"
})
ctx.update_dimension(ContextDimension.ACTIVITY, {
    "primary": "sitting", "confidence": 0.95
})
ctx.update_dimension(ContextDimension.ENVIRONMENTAL, {
    "temperature_f": 71, "humidity_pct": 44, "noise_db": 38
})

# Context changes throughout the day
# 10:00 AM - Walking to meeting
ctx.update_dimension(ContextDimension.ACTIVITY, {
    "primary": "walking", "confidence": 0.88
})

# 10:05 AM - In meeting
ctx.update_dimension(ContextDimension.LOCATION, {
    "type": "indoor", "building": "HQ", "floor": 3, "room": "conf-room-A"
})
ctx.update_dimension(ContextDimension.ACTIVITY, {
    "primary": "meeting", "confidence": 0.93
})

# Get full context
current = ctx.get_context()
print(f"User is {current['activity']['primary']} in {current['location']['room']}")
print(f"Environment: {current['environmental']['temperature_f']}°F, {current['environmental']['noise_db']}dB")
```

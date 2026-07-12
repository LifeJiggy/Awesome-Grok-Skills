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

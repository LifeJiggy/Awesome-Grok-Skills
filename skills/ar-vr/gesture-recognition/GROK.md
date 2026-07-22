---
name: "gesture-recognition"
category: "ar-vr"
version: "2.0.0"
tags: ["gesture-recognition", "hand-tracking", "computer-vision", "ml", "kinect", "mediapipe"]
---

# Gesture Recognition

## Overview

Real-time gesture recognition system supporting hand tracking, body pose estimation, and custom gesture definition for XR, touchless interfaces, and spatial computing. This module provides MediaPipe, OpenVR, and custom ML-based gesture pipelines with gesture libraries, training tools, confidence scoring, and gesture-to-action mapping. Supports finger-level tracking, full hand skeletons, body pose landmarks, and dynamic gesture sequences.

## Core Capabilities

- **Hand Tracking**: 21-point hand skeleton with finger bend, pinch, grab, and spread measurements
- **Body Pose**: Full body pose estimation with 33 landmarks for gesture and activity recognition
- **Dynamic Gestures**: Temporal gesture sequences (swipe, wave, circle) with start/end detection
- **Custom Gestures**: Define and train custom gestures from examples using DTW or ML classifiers
- **Gesture Mapping**: Map recognized gestures to application actions with context-dependent behavior
- **Confidence Scoring**: Multi-level confidence thresholds for gesture acceptance/rejection
- **Multi-Hand**: Simultaneous tracking of both hands with inter-hand interaction detection
- **Accessibility**: Gesture alternatives for users with limited mobility

## Usage

```python
from gesture_recognition import (
    HandTracker, GestureLibrary, GestureMapper, BodyPoseTracker
)

# Initialize hand tracker
tracker = HandTracker(
    model="mediapipe_hands",
    max_hands=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)

# Process frame
landmarks = tracker.process_frame(frame_data)
if landmarks:
    hand = landmarks[0]
    print(f"Hand detected: {hand.handedness}")
    print(f"Pinch strength: {hand.pinch_strength:.2f}")
    print(f"Grab strength: {hand.grab_strength:.2f}")
    print(f"Pointing: {hand.is_pointing}")
    print(f"Open palm: {hand.is_open_palm}")

# Use gesture library
library = GestureLibrary()
gestures = library.recognize(landmarks)
for gesture in gestures:
    print(f"Gesture: {gesture.name} ({gesture.confidence:.0%})")

# Map gestures to actions
mapper = GestureMapper()
mapper.add_mapping("pinch", "select", context="ui_mode")
mapper.add_mapping("grab", "grab_object", context="interaction_mode")
mapper.add_mapping("swipe_left", "next_page", context="navigation")
action = mapper.resolve("pinch", context="ui_mode")
print(f"Mapped action: {action}")

# Body pose
body_tracker = BodyPoseTracker()
pose = body_tracker.process_frame(frame_data)
if pose:
    print(f"Standing: {pose.is_standing}")
    print(f"Arms raised: {pose.arms_raised}")
```

## Best Practices

- Set detection confidence thresholds high (0.7+) to reduce false positives
- Use temporal smoothing (3-5 frame window) to stabilize noisy landmark data
- Define gestures with clear start and end conditions to prevent gesture bleeding
- Provide visual feedback for recognized gestures to confirm user intent
- Implement gesture debouncing to prevent rapid repeated activations
- Use context-dependent gesture mapping — the same gesture can mean different things
- Test gestures with diverse hand sizes, skin tones, and lighting conditions
- Provide alternative input methods for users who cannot perform gestures
- Log gesture recognition metrics to identify problematic gestures
- Use dynamic gestures (sequences) for complex actions, static poses for simple ones

## Related Modules

- **ar-vr-development** — XR gesture integration
- **mixed-reality** — Gesture interaction in passthrough
- **spatial-computing** — Spatial gesture inputs
- **3d-rendering** — Visual gesture feedback rendering
- **ambient-computing** → **context-aware** — Context-dependent gesture behavior

## Advanced Configuration

### Hand Tracking Configuration

```python
from gesture_recognition import HandTrackingConfig, TrackingModel, FilterConfig

# High-precision tracking config
high_precision_config = HandTrackingConfig(
    model=TrackingModel.MEDIAPIPE_HANDS,
    max_hands=2,
    min_detection_confidence=0.8,
    min_tracking_confidence=0.7,
    model_complexity=1,  # 0=lite, 1=full
    filter=FilterConfig(
        temporal_window=5,
        velocity_threshold=0.1,
        acceleration_threshold=0.5,
        smoothing_factor=0.7,
        prediction_enabled=True,
        prediction_horizon_ms=30,
    ),
    skeleton={
        "model": "26_point",  # 21 or 26 point model
        "include_wrist": True,
        "include_finger_tips": True,
        "include_finger_joints": True,
        "include_palm": True,
    },
    physics={
        "finger_mass_kg": 0.01,
        "joint_stiffness": 0.8,
        "damping": 0.2,
        "collision_radius_scale": 0.9,
        "gravity_compensation": True,
    },
    rendering={
        "show_skeleton": False,
        "show_bounding_box": False,
        "hand_mesh_enabled": True,
        "hand_mesh_quality": "high",
        "occlusion_enabled": True,
        "shadow_receiving": True,
        "shadow_casting": False,
    },
)

# Performance-optimized config
performance_config = HandTrackingConfig(
    model=TrackingModel.MEDIAPIPE_HANDS,
    max_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
    model_complexity=0,
    filter=FilterConfig(
        temporal_window=3,
        velocity_threshold=0.2,
        acceleration_threshold=1.0,
        smoothing_factor=0.5,
        prediction_enabled=False,
    ),
    skeleton={"model": "21_point"},
    physics={"enabled": False},
    rendering={"hand_mesh_enabled": False},
)
```

### Gesture Library Advanced

```python
from gesture_recognition import GestureLibrary, GestureDefinition, GestureRecognizer

library = GestureLibrary()

# Define custom gestures
library.define_gesture(GestureDefinition(
    name="thumbs_up",
    type="static",
    fingers=["thumb"],
    thumb_extension="extended",
    other_fingers="curled",
    orientation="up",
    confidence_threshold=0.8,
    hold_time_ms=500,
    cooldown_ms=200,
))

library.define_gesture(GestureDefinition(
    name="pinch_precise",
    type="static",
    fingers=["thumb", "index"],
    thumb_index_distance_max=0.02,  # 2cm
    other_fingers="any",
    confidence_threshold=0.9,
    hold_time_ms=200,
    cooldown_ms=100,
))

library.define_gesture(GestureDefinition(
    name="swipe_horizontal",
    type="dynamic",
    hand_movement="horizontal",
    min_distance=0.2,  # 20cm
    max_duration_ms=500,
    direction=["left", "right"],
    confidence_threshold=0.7,
    cooldown_ms=300,
))

# Gesture recognition pipeline
recognizer = GestureRecognizer(
    library=library,
    pipeline={
        "landmark_smoothing": True,
        "gesture_debouncing": True,
        "multi_gesture_detection": False,
        "context_awareness": True,
    },
)

# Process frame
gestures = recognizer.recognize(landmarks)
for gesture in gestures:
    print(f"Gesture: {gesture.name}")
    print(f"Confidence: {gesture.confidence:.2f}")
    print(f"Hand: {gesture.handedness}")
    print(f"Duration: {gesture.duration_ms}ms")
    print(f"Position: {gesture.position}")
```

### Body Pose Configuration

```python
from gesture_recognition import BodyPoseConfig, PoseModel, ActivityRecognition

body_config = BodyPoseConfig(
    model=PoseModel.MEDIAPIPE_POSE,
    model_complexity=2,  # 0, 1, 2
    smooth_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
    enable_segmentation=False,
    smooth_segmentation=True,
    landmarks_to_show=[
        "nose", "left_eye", "right_eye",
        "left_ear", "right_ear",
        "left_shoulder", "right_shoulder",
        "left_elbow", "right_elbow",
        "left_wrist", "right_wrist",
        "left_hip", "right_hip",
        "left_knee", "right_knee",
        "left_ankle", "right_ankle",
    ],
)

# Activity recognition
activity_recognizer = ActivityRecognition(
    activities=[
        "standing", "sitting", "lying_down",
        "walking", "running", "jumping",
        "arm_raised", "arm_extended",
        "pointing", "waving",
    ],
    window_size=30,  # frames
    confidence_threshold=0.7,
)
```

## Architecture Patterns

### Gesture Recognition Pipeline

```
+------------------------------------------------------------------+
|                 Gesture Recognition Pipeline                      |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------+    +----------------+    +----------------+  |
|  |  Input         |    |  Preprocessing |    |  Feature       |  |
|  |  Layer         |    |  Layer         |    |  Extraction    |  |
|  |                |    |                |    |                |  |
|  |  Camera Feed   |    |  Temporal      |    |  Landmark      |  |
|  |  Depth Data    |<-->|  Smoothing     |<-->|  Extraction    |  |
|  |  IMU Data      |    |  Noise Filter  |    |  Velocity Calc |  |
|  |  Hand Skeleton |    |  Outlier Reject|    |  Angle Calc    |  |
|  +-------+--------+    +-------+--------+    +-------+--------+  |
|          |                    |                     |             |
|          v                    v                     v             |
|  +----------------------------------------------------------------+
|  |                    Recognition Engine                          |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Static      |  |  Dynamic     |  |  Multi-Hand  |          |
|  |  |  Gesture     |  |  Gesture     |  |  Interaction |          |
|  |  |  Classifier  |  |  Classifier  |  |  Detector    |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
|                              |                                    |
|                              v                                    |
|  +----------------------------------------------------------------+
|  |                    Post-Processing                              |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Confidence  |  |  Debouncing  |  |  Context     |          |
|  |  |  Filtering   |  |  Engine      |  |  Resolver    |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
+------------------------------------------------------------------+
```

### Gesture State Machine

```
                    +------------------+
                    |     IDLE         |
                    |  (No Hand)       |
                    +--------+---------+
                             |
                   +---------v---------+
                   |   HAND DETECTED   |
                   |  (Tracking Start) |
                   +---------+---------+
                             |
              +--------------+--------------+
              |                             |
    +---------v---------+         +---------v---------+
    |   STATIC GESTURE  |         |   DYNAMIC GESTURE |
    |   (Hold)          |         |   (Movement)      |
    +---------+---------+         +---------+---------+
              |                             |
              v                             v
    +-------------------+         +-------------------+
    |  GESTURE CONFIRMED|         |  GESTURE TRACKING |
    |  (Confidence OK)  |         |  (Path Following) |
    +---------+---------+         +---------+---------+
              |                             |
              v                             v
    +-------------------+         +-------------------+
    |  ACTION TRIGGER   |         |  ACTION TRIGGER   |
    |  (On Hold)        |         |  (On Complete)    |
    +-------------------+         +-------------------+
```

### Multi-Hand Interaction

```
Left Hand State          Right Hand State
        |                        |
        v                        v
+-------------------+    +-------------------+
|  Left Hand        |    |  Right Hand       |
|  Detection        |    |  Detection        |
+-------------------+    +-------------------+
        |                        |
        v                        v
+-------------------+    +-------------------+
|  Left Gesture     |    |  Right Gesture    |
|  Recognition      |    |  Recognition      |
+-------------------+    +-------------------+
        |                        |
        +-----------+------------+
                    |
                    v
            +-------------------+
            |  Interaction      |
            |  Resolver         |
            +-------------------+
                    |
                    v
            +-------------------+
            |  Combined Action  |
            |  (Two-Hand)       |
            +-------------------+
```

## Integration Guide

### Unity Hand Tracking Integration

```csharp
// Unity Hand Tracking Setup
using UnityEngine.XR.Interaction.Toolkit;

public class HandTrackingManager : MonoBehaviour
{
    [SerializeField] private XRHandTracker handTracker;
    [SerializeField] private HandPrefab leftHandPrefab;
    [SerializeField] private HandPrefab rightHandPrefab;
    
    void Start()
    {
        // Subscribe to hand tracking events
        handTracker.trackingAcquired += OnHandTrackingAcquired;
        handTracker.trackingLost += OnHandTrackingLost;
        
        // Configure hand tracking
        handTracker.updateRate = 90; // Hz
        handTracker.predictionTime = 0.03f; // 30ms prediction
    }
    
    void OnHandTrackingAcquired(XRHand hand)
    {
        Debug.Log($"Hand acquired: {hand.handedness}");
        
        // Enable hand visualization
        if (hand.handedness == Handedness.Left)
        {
            leftHandPrefab.gameObject.SetActive(true);
        }
        else
        {
            rightHandPrefab.gameObject.SetActive(true);
        }
    }
    
    void Update()
    {
        // Get hand landmarks
        if (handTracker.leftHand.isTracked)
        {
            var pinch = handTracker.leftHand.GetGesture(XRHandGesture.Pinch);
            if (pinch.isActive)
            {
                Debug.Log($"Left pinch strength: {pinch.strength}");
            }
        }
    }
}
```

### Unreal Engine Hand Tracking

```cpp
// Unreal Engine Hand Tracking
#include "HandTrackingComponent.h"

void AHandTrackingPawn::BeginPlay()
{
    Super::BeginPlay();
    
    // Get hand tracking component
    HandTracking = FindComponentByClass<UHandTrackingComponent>();
    
    // Subscribe to gesture events
    HandTracking->OnGestureDetected.AddDynamic(this, &AHandTrackingPawn::OnGestureDetected);
    HandTracking->OnPinchDetected.AddDynamic(this, &AHandTrackingPawn::OnPinchDetected);
}

void AHandTrackingPawn::OnGestureDetected(EHandGesture Gesture, float Confidence)
{
    if (Confidence > 0.8f)
    {
        switch (Gesture)
        {
            case EHandGesture::Grab:
                GrabObject();
                break;
            case EHandGesture::Point:
                PointAtObject();
                break;
            case EHandGesture::ThumbsUp:
                ConfirmAction();
                break;
        }
    }
}

void AHandTrackingPawn::OnPinchDetected(EHandHandedness Hand, float Strength)
{
    if (Strength > 0.7f)
    {
        SelectObject(Hand);
    }
}
```

### WebXR Hand Tracking

```javascript
// WebXR Hand Tracking
class HandTrackingApp {
    async init() {
        // Check hand tracking support
        const supported = await navigator.xr.isSessionSupported('immersive-vr');
        
        this.session = await navigator.xr.requestSession('immersive-vr', {
            optionalFeatures: ['hand-tracking'],
        });
        
        // Setup hand tracking
        this.hands = {
            left: null,
            right: null,
        };
        
        this.session.addEventListener('inputsourceschange', (event) => {
            for (const source of event.added) {
                if (source.hand) {
                    this.hands[source.handedness] = source;
                }
            }
        });
        
        // Gesture recognition
        this.gestureRecognizer = new GestureRecognizer();
        this.gestureRecognizer.addGesture({
            name: 'pinch',
            detect: (landmarks) => {
                const thumbTip = landmarks[4];
                const indexTip = landmarks[8];
                const distance = this.distance(thumbTip, indexTip);
                return distance < 0.02; // 2cm threshold
            },
        });
    }
    
    render(time, frame) {
        // Get hand input sources
        const inputSources = frame.session.inputSources;
        
        for (const source of inputSources) {
            if (source.hand) {
                const hand = source.hand;
                
                // Get landmarks
                const landmarks = [];
                for (let i = 0; i <= 24; i++) {
                    const landmark = hand.getXRJoint(i);
                    if (landmark) {
                        landmarks.push({
                            position: landmark.transform.position,
                            radius: landmark.radius,
                        });
                    }
                }
                
                // Recognize gestures
                const gesture = this.gestureRecognizer.recognize(landmarks);
                if (gesture) {
                    this.handleGesture(gesture, source.handedness);
                }
            }
        }
        
        this.session.requestAnimationFrame(this.render.bind(this));
    }
}
```

## Performance Optimization

### Gesture Recognition Optimization

```python
from gesture_recognition import GestureOptimizer, PerformanceConfig

optimizer = GestureOptimizer(
    config=PerformanceConfig(
        target_fps=90,
        max_processing_time_ms=2.0,
        max_memory_mb=100,
    ),
    optimizations={
        "temporal_smoothing": True,
        "smoothing_window": 3,
        "landmark_subsampling": True,
        "subsample_factor": 2,
        "prediction": True,
        "prediction_horizon_ms": 30,
        "gesture_caching": True,
        "cache_size": 100,
    },
)

# Monitor performance
stats = optimizer.get_stats()
print(f"Processing time: {stats.processing_time_ms:.2f}ms")
print(f"Memory usage: {stats.memory_mb:.1f}MB")
print(f"Gesture detection rate: {stats.detection_rate:.1f}/s")
print(f"False positive rate: {stats.false_positive_rate:.3f}")
```

### Landmark Processing Optimization

```python
from gesture_recognition import LandmarkProcessor, ProcessingPipeline

pipeline = ProcessingPipeline(
    stages=[
        {"name": "noise_filter", "type": "butterworth", "cutoff": 5.0},
        {"name": "smoothing", "type": "exponential", "factor": 0.7},
        {"name": "prediction", "type": "kalman", "process_noise": 0.1},
        {"name": "outlier_detection", "type": "mahalanobis", "threshold": 3.0},
    ],
    parallel_processing=True,
    gpu_acceleration=True,
)

# Process landmarks
processed_landmarks = pipeline.process(raw_landmarks)

# Monitor pipeline
stats = pipeline.get_stats()
for stage in stats.stages:
    print(f"{stage.name}: {stage.time_ms:.2f}ms")
```

## Security Considerations

### Input Validation

```python
from gesture_recognition import InputValidator, SecurityConfig

validator = InputValidator(
    config=SecurityConfig(
        max_landmarks=100,
        max_hands=2,
        coordinate_bounds=(-10, 10),
        confidence_bounds=(0, 1),
        rate_limiting={
            "max_requests_per_second": 100,
            "burst_size": 20,
        },
        anomaly_detection={
            "enabled": True,
            "sensitivity": 0.8,
            "alert_threshold": 0.9,
        },
    ),
)

# Validate input
is_valid = validator.validate_landmarks(landmarks)
if not is_valid:
    print("Invalid landmark data detected")
```

### Privacy Protection

```python
from gesture_recognition import PrivacyManager, DataRetention

privacy = PrivacyManager(
    retention=DataRetention(
        landmark_data="session_only",
        gesture_data="session_only",
        analytics="anonymized",
    ),
    anonymization={
        "blur_sensitive_areas": True,
        "remove_identifiers": True,
        "aggregate_data": True,
    },
)

# Process with privacy
processed_data = privacy.process_landmarks(raw_landmarks)
```

## Troubleshooting Guide

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Jittery tracking** | Unstable landmarks | Increase smoothing, check lighting |
| **False positives** | Incorrect gestures | Increase confidence threshold |
| **Missed gestures** | Gestures not detected | Decrease confidence threshold, check hand visibility |
| **Tracking loss** | Hand disappears | Improve lighting, avoid occlusion |
| **Latency** | Delayed response | Reduce processing complexity |
| **Memory leaks** | Growing memory usage | Check landmark caching, release resources |
| **CPU overload** | High CPU usage | Enable GPU acceleration, reduce sample rate |

## API Reference

```python
class HandTracker:
    """Track hand movements."""
    
    def __init__(self, model="mediapipe_hands", max_hands=2, min_detection_confidence=0.7):
        """Initialize hand tracker."""
        
    def process_frame(self, frame_data) -> List[HandLandmarks]:
        """Process frame and return hand landmarks."""

class GestureLibrary:
    """Library of gestures."""
    
    def define_gesture(self, definition: GestureDefinition) -> None:
        """Define a new gesture."""
        
    def recognize(self, landmarks) -> List[DetectedGesture]:
        """Recognize gestures from landmarks."""

class GestureMapper:
    """Map gestures to actions."""
    
    def add_mapping(self, gesture: str, action: str, context: str) -> None:
        """Add gesture-action mapping."""
        
    def resolve(self, gesture: str, context: str) -> Optional[str]:
        """Resolve gesture to action."""

class BodyPoseTracker:
    """Track body pose."""
    
    def process_frame(self, frame_data) -> Optional[BodyPose]:
        """Process frame and return body pose."""
```

## Data Models

```python
@dataclass
class HandLandmarks:
    """Hand landmarks data."""
    handedness: str
    landmarks: List[Vector3]
    pinch_strength: float
    grab_strength: float
    is_pointing: bool
    is_open_palm: bool
    confidence: float

@dataclass
class DetectedGesture:
    """Detected gesture."""
    name: str
    confidence: float
    handedness: str
    position: Vector3
    duration_ms: int
    start_time: float
    end_time: float

@dataclass
class BodyPose:
    """Body pose data."""
    landmarks: List[Vector3]
    is_standing: bool
    arms_raised: bool
    confidence: float

@dataclass
class GestureDefinition:
    """Gesture definition."""
    name: str
    type: str  # static or dynamic
    fingers: List[str]
    confidence_threshold: float
    hold_time_ms: int
    cooldown_ms: int
```

## Deployment Guide

### Build Configuration

```python
from gesture_recognition import GestureBuildConfig

config = GestureBuildConfig(
    platforms=["quest_3", "vision_pro", "webxr", "hololens_2"],
    models={
        "hand_tracking": "mediapipe_hands",
        "body_pose": "mediapipe_pose",
        "face_mesh": "mediapipe_face_mesh",
    },
    optimization={
        "gpu_acceleration": True,
        "model_quantization": True,
        "batch_processing": True,
    },
)
```

## Monitoring & Observability

```python
from gesture_recognition import GestureMetrics, GestureHealth

metrics = GestureMetrics(
    tracks=[
        "gesture_detection_rate",
        "false_positive_rate",
        "tracking_latency",
        "memory_usage",
    ],
    sample_rate=0.1,
)

health = GestureHealth(
    checks=[
        {"name": "detection_rate", "threshold": 10},
        {"name": "false_positive_rate", "threshold": 0.01},
        {"name": "tracking_latency_ms", "threshold": 20},
    ],
)
```

## Testing Strategy

```python
import pytest
from gesture_recognition import HandTracker, GestureLibrary

class TestHandTracking:
    def test_hand_detection(self):
        tracker = HandTracker()
        landmarks = tracker.process_frame(test_frame)
        assert len(landmarks) > 0
    
    def test_pinch_detection(self):
        tracker = HandTracker()
        landmarks = tracker.process_frame(pinch_frame)
        assert landmarks[0].pinch_strength > 0.7

class TestGestureLibrary:
    def test_gesture_recognition(self):
        library = GestureLibrary()
        gestures = library.recognize(landmarks)
        assert len(gestures) > 0
```

## Versioning & Migration

| Version | Changes | Breaking |
|---------|---------|----------|
| 2.0.0 | Added body pose, improved accuracy | Yes |
| 1.5.0 | Added multi-hand support | No |
| 1.0.0 | Initial release | N/A |

## Glossary

| Term | Definition |
|------|------------|
| **Landmark** | Key point on hand/body |
| **Skeleton** | Connected landmarks |
| **Gesture** | Recognized hand/body pose |
| **Confidence** | Recognition certainty |
| **Debouncing** | Preventing repeated triggers |
| **Temporal Smoothing** | Stabilizing over time |
| **Prediction** | Estimating future position |

## Changelog

### 2.0.0 (2024-01-15)
- Added body pose tracking
- Improved gesture accuracy
- Added multi-hand support

### 1.5.0 (2023-10-01)
- Added dynamic gestures
- Improved performance

### 1.0.0 (2023-06-01)
- Initial release

## Contributing Guidelines

```bash
git clone https://github.com/company/gesture-recognition.git
cd gesture-recognition
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

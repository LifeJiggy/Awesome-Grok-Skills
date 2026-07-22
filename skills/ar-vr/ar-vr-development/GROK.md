---
name: "ar-vr-development"
category: "ar-vr"
version: "2.0.0"
tags: ["ar", "vr", "xr", "mixed-reality", "unity", "unreal", "webxr", "oculus"]
---

# AR/VR Development

## Overview

Comprehensive AR/VR/XR development toolkit covering cross-platform immersive application development for Meta Quest, Apple Vision Pro, HoloLens, and WebXR. This module provides Unity and Unreal Engine project scaffolding, spatial interaction patterns, hand/eye tracking integration, performance optimization for mobile XR, multiplayer networking, and deployment pipelines. Supports both native and web-based immersive experiences with focus on comfort, accessibility, and performance.

## Core Capabilities

- **Cross-Platform XR**: Build once for Quest 3, Vision Pro, HoloLens 2, and WebXR with platform abstraction layers
- **Spatial Interaction**: Grab, poke, ray-cast, and gaze-based interaction patterns with haptic feedback
- **Hand Tracking**: Full hand tracking with gesture recognition, pinch detection, and skeletal hand models
- **Eye Tracking**: Foveated rendering, gaze-based UI, and attention analytics
- **Performance Optimization**: Frame time budgets, foveated rendering, async spacewarp, and level-of-detail for XR
- **Multiplayer XR**: Shared spatial experiences with networked object synchronization and voice chat
- **Passthrough AR**: Camera passthrough with depth occlusion and plane detection
- **Deployment**: Automated build pipelines for app stores and enterprise distribution

## Usage

```python
from ar_vr_development import (
    XRProject, Platform, InteractionType, PerformanceProfile
)

# Create XR project
project = XRProject(
    name="SpatialCollaboration",
    engine="unity",
    platforms=[Platform.QUEST_3, Platform.WEBXR],
    target_framerate=90,
    render_scale=1.0,
)

# Configure interactions
project.add_interaction(InteractionType.HAND_TRACKING, {
    "gesture_recognition": True,
    "grab_distance_m": 0.5,
    "haptic_feedback": True,
})
project.add_interaction(InteractionType.EYE_TRACKING, {
    "foveated_rendering": True,
    "gaze_ui": True,
    "attention_heatmap": True,
})

# Performance profile
profile = PerformanceProfile(
    target_framerate=90,
    ms_per_frame=11.1,
    fixed_foveated_rendering_level=3,
    application_spacewarp=True,
    gpu_skinning=True,
    single_pass_stereo=True,
)
project.set_performance_profile(profile)

# Build
result = project.build(platform=Platform.QUEST_3, configuration="release")
print(f"Build: {result.output_path}")
print(f"Size: {result.apk_size_mb:.1f} MB")
print(f"Build time: {result.build_time_s:.0f}s")
```

```python
# Spatial anchor management
from ar_vr_development import SpatialAnchorManager

anchors = SpatialAnchorManager()
anchor = anchors.create(
    position=(1.5, 1.0, 2.0),
    rotation=(0, 0, 0, 1),
    label="Virtual Whiteboard",
    persistent=True,
)
print(f"Anchor: {anchor.anchor_id} at {anchor.position}")

# Multiplayer
from ar_vr_development import XRNetworking
network = XRNetworking(room_id="collab-room-001", max_players=8)
network.sync_object("shared-model-01", position=(0, 1, 3), ownership="dynamic")
```

## Best Practices

- Target 90fps minimum — any frame drops cause motion sickness in VR
- Use fixed foveated rendering to reduce GPU load without visible quality loss
- Implement comfort vignetting during locomotion to reduce simulator sickness
- Design for seated, standing, and room-scale experiences — don't assume full room
- Use spatial audio for all interactive objects to enhance presence
- Test with users of different heights and physical abilities
- Implement teleport locomotion as default — smooth locomotion causes nausea for many
- Use passthrough for AR experiences rather than virtual-only environments
- Keep UI at arm's length (0.5-1.5m) and within 30° of center gaze
- Optimize draw calls aggressively — mobile XR GPUs have strict thermal limits

## Related Modules

- **mixed-reality** — MR-specific patterns and passthrough integration
- **spatial-computing** — Spatial anchors, meshes, and scene understanding
- **3d-rendering** — Optimized 3D rendering pipelines for XR
- **gesture-recognition** — Hand and eye gesture recognition systems
- **ar-vr** → **ar-vr-development** — Development workflow and tooling

## Advanced Configuration

### Platform-Specific Optimization Profiles

```python
from ar_vr_development import PlatformProfile, ThermalProfile, QualityPreset

# Quest 3 optimized profile
quest_profile = PlatformProfile(
    platform=Platform.QUEST_3,
    gpu_target="Adreno 740",
    cpu_target="Snapdragon XR2 Gen 2",
    thermal=ThermalProfile.CONSTANT,
    quality=QualityPreset.BALANCED,
    foveated_rendering="fixed_4level",
    application_spacewarp=True,
    single_pass_stereo=True,
    textured_fetch=True,
)

# Apple Vision Pro profile
vision_profile = PlatformProfile(
    platform=Platform.VISION_PRO,
    gpu_target="Apple M2 GPU",
    cpu_target="Apple M2",
    thermal=ThermalProfile.ADAPTIVE,
    quality=QualityPreset.HIGH,
    foveated_rendering="dynamic",
    application_spacewarp=False,
    single_pass_stereo=True,
    temporal_reprojection=True,
)

# WebXR profile (browser-based)
webxr_profile = PlatformProfile(
    platform=Platform.WEBXR,
    gpu_target="WebGL 2.0",
    cpu_target="JavaScript Engine",
    thermal=ThermalProfile.UNCONTROLLED,
    quality=QualityPreset.LOW,
    foveated_rendering="none",
    application_spacewarp=False,
    single_pass_stereo=False,
    multiview=True,
)
```

### Multi-Platform Build Configuration

```python
from ar_vr_development import BuildPipeline, BuildTarget, OptimizationLevel

pipeline = BuildPipeline(
    project="SpatialCollaboration",
    targets=[
        BuildTarget(
            platform=Platform.QUEST_3,
            optimization=OptimizationLevel.MAX_PERFORMANCE,
            strip_engine_code=True,
            il2cpp=True,
            scripting_backend="il2cpp",
            android_target_sdk=33,
            min_sdk=29,
        ),
        BuildTarget(
            platform=Platform.WEBXR,
            optimization=OptimizationLevel.BALANCED,
            webgl_compression="brotli",
            webgl_memory_size=512,
            webgl_exception_support="full",
        ),
        BuildTarget(
            platform=Platform.VISION_PRO,
            optimization=OptimizationLevel.MAX_QUALITY,
            swift_interop=True,
            metal_api_validation=True,
        ),
    ],
    shared_assets=[
        "Assets/Prefabs/",
        "Assets/Materials/",
        "Assets/Textures/Shared/",
    ],
    platform_overrides={
        Platform.QUEST_3: {"Assets/Textures/Mobile/": "high"},
        Platform.VISION_PRO: {"Assets/Textures/Desktop/": "ultra"},
    },
)
```

### Spatial Anchor Cloud Synchronization

```python
from ar_vr_development import CloudAnchorService, AnchorSyncConfig

cloud_service = CloudAnchorService(
    provider="google_cloud_anchors",  # or "apple_cloudkit", "custom"
    config=AnchorSyncConfig(
        sync_interval_s=30,
        conflict_resolution="last_write_wins",
        persistence_ttl_days=365,
        max_anchors_per_user=100,
        encryption_at_rest=True,
    ),
)

# Create persistent anchor
anchor = cloud_service.create_anchor(
    position=(1.5, 1.0, 2.0),
    rotation=(0, 0, 0, 1),
    name="Virtual Display",
    metadata={"user_id": "user123", "room": "office"},
    ttl_days=365,
)
print(f"Cloud anchor ID: {anchor.cloud_id}")
print(f"Expiration: {anchor.expires_at}")

# Resolve anchor on another device
resolved = cloud_service.resolve_anchor(anchor.cloud_id)
if resolved:
    print(f"Resolved at: {resolved.position}")
else:
    print("Anchor expired or not found")
```

### Hand Tracking Advanced Configuration

```python
from ar_vr_development import HandTrackingConfig, GestureFilter, SkeletonModel

hand_config = HandTrackingConfig(
    skeleton_model=SkeletonModel.HAND_26,  # 26-point model
    gesture_filter=GestureFilter(
        min_confidence=0.8,
        temporal_smoothing_window=5,
        velocity_threshold=0.1,  # m/s
        acceleration_threshold=0.5,  # m/s²
    ),
    physics={
        "finger_mass_kg": 0.01,
        "joint_stiffness": 0.8,
        "damping": 0.2,
        "collision_radius_scale": 0.9,
    },
    rendering={
        "show_skeleton": False,
        "show_bounding_box": False,
        "hand_mesh_enabled": True,
        "hand_mesh_quality": "high",
        "occlusion_enabled": True,
    },
    interactions={
        "grab_radius_m": 0.05,
        "poke_radius_m": 0.01,
        "ray_origin": "index_tip",
        "ray_max_distance_m": 10.0,
    },
)
```

## Architecture Patterns

### XR Application Architecture

```
+------------------------------------------------------------------+
|                    XR Application Architecture                   |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------+    +----------------+    +----------------+  |
|  |  Platform      |    |  Rendering    |    |  Input         |  |
|  |  Abstraction   |    |  Pipeline     |    |  System        |  |
|  |  Layer         |    |               |    |                |  |
|  |                |    |               |    |                |  |
|  |  Quest 3 API   |    |  Forward      |    |  Hand Tracking |  |
|  |  Vision Pro    |<-->|  Deferred     |<-->|  Eye Tracking  |  |
|  |  WebXR API     |    |  URP/HDRP    |    |  Controllers   |  |
|  |  OpenXR        |    |  Multiview    |    |  Voice         |  |
|  +-------+--------+    +-------+--------+    +-------+--------+  |
|          |                    |                     |             |
|          v                    v                     v             |
|  +----------------------------------------------------------------+
|  |                    Core Runtime Engine                         |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Scene       |  |  Spatial     |  |  Networking  |          |
|  |  |  Manager     |  |  Anchor      |  |  Manager     |          |
|  |  |              |  |  Service     |  |              |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Physics     |  |  Audio       |  |  Analytics   |          |
|  |  |  Engine      |  |  Engine      |  |  Collector   |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
|                              |                                    |
|                              v                                    |
|  +----------------------------------------------------------------+
|  |                    Platform Services                           |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Cloud       |  |  Identity    |  |  Content     |          |
|  |  |  Sync        |  |  Service     |  |  Delivery    |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
+------------------------------------------------------------------+
```

### Spatial Interaction State Machine

```
                     +------------------+
                     |     IDLE         |
                     |  (No Input)      |
                     +--------+---------+
                              |
                    +---------v---------+
                    |   INPUT DETECTED  |
                    |  (Hand/Controller)|
                    +---------+---------+
                              |
              +---------------+---------------+
              |                               |
    +---------v---------+         +-----------v-----------+
    |   GAZE/POINT      |         |   DIRECT MANIPULATION |
    |   (Ray-based)     |         |   (Touch/Grab)        |
    +---------+---------+         +-----------+-----------+
              |                               |
              v                               v
    +-------------------+         +-------------------+
    |  UI INTERACTION   |         |  OBJECT GRAB      |
    |  (Hover/Select)   |         |  (Pinch/Hold)     |
    +---------+---------+         +---------+---------+
              |                               |
              v                               v
    +-------------------+         +-------------------+
    |  ACTION TRIGGER   |         |  OBJECT MANIPULATE|
    |  (Click/Confirm)  |         |  (Move/Rotate)    |
    +-------------------+         +-------------------+
```

### Performance Optimization Pipeline

```
+------------------------------------------------------------------+
|                 Performance Optimization Pipeline                 |
+------------------------------------------------------------------+
|                                                                  |
|  Frame Budget: 11.1ms (90fps)                                    |
|  +------------------------------------------------------------+  |
|  |  Input Processing (1ms)                                     |  |
|  |  +------------------------------------------------------+  |  |
|  |  |  Hand Tracking: 0.3ms                                  |  |  |
|  |  |  Eye Tracking: 0.2ms                                   |  |  |
|  |  |  Controller Input: 0.1ms                               |  |  |
|  |  |  Gesture Recognition: 0.4ms                            |  |  |
|  +------------------------------------------------------------+  |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |  Game Logic (2ms)                                          |  |
|  |  +------------------------------------------------------+  |  |
|  |  |  Physics Simulation: 0.5ms                             |  |  |
|  |  |  AI/Behavior: 0.5ms                                    |  |  |
|  |  |  State Management: 0.3ms                               |  |  |
|  |  |  Animation Update: 0.7ms                               |  |  |
|  +------------------------------------------------------------+  |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |  Rendering (8ms)                                           |  |
|  |  +------------------------------------------------------+  |  |
|  |  |  Culling (Frustum + Occlusion): 0.5ms                 |  |  |
|  |  |  Draw Call Batching: 0.5ms                             |  |  |
|  |  |  Shadow Rendering: 2ms                                 |  |  |
|  |  |  Main Render Pass: 3ms                                 |  |  |
|  |  |  Post-Processing: 1ms                                  |  |  |
|  |  |  UI Rendering: 1ms                                     |  |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

## Integration Guide

### Unity Integration

```csharp
// XR Interaction Toolkit Setup
using UnityEngine.XR.Interaction.Toolkit;

public class XRInteractable : MonoBehaviour
{
    [SerializeField] private XRGrabInteractable grabInteractable;
    [SerializeField] private XRRayInteractor rayInteractor;
    
    void Awake()
    {
        // Configure grab interaction
        grabInteractable.selectEntered.AddListener(OnGrab);
        grabInteractable.selectExited.AddListener(OnRelease);
        
        // Configure ray interaction
        rayInteractor.maxRaycastDistance = 10f;
        rayInteractor.interactionLayerMask = LayerMask.GetMask("Interactable");
    }
    
    void OnGrab(SelectEnterEventArgs args)
    {
        // Attach haptic feedback
        args.interactorObject.SendHapticImpulse(0.5f, 0.2f);
    }
    
    void OnRelease(SelectExitEventArgs args)
    {
        // Snap to nearest anchor
        var anchor = FindNearestAnchor(transform.position);
        if (anchor != null)
        {
            StartCoroutine(SnapToAnchor(anchor, 0.3f));
        }
    }
}
```

### Unreal Engine Integration

```cpp
// XR Component Setup
#include "HeadMountedDisplayFunctionLibrary.h"
#include "MotionControllerComponent.h"

void AXRPawn::BeginPlay()
{
    Super::BeginPlay();
    
    // Setup motion controllers
    LeftMotionController->SetTrackingMotionSource(FName("Left"));
    RightMotionController->SetTrackingMotionSource(FName("Right"));
    
    // Configure haptics
    HapticComponent = CreateDefaultSubobject<UHapticFeedbackEffect>(TEXT("Haptics"));
    
    // Setup eye tracking if supported
    if (UHeadMountedDisplayFunctionLibrary::IsHeadMountedDisplayEnabled())
    {
        bEyeTrackingEnabled = true;
        GEngine->Exec(GetWorld(), TEXT("EnableEyeTracking true"));
    }
}

void AXRPawn::OnGrabDetected(UPrimitiveComponent* GrabbedComponent)
{
    // Haptic feedback on grab
    LeftMotionController->PlayHapticEffect(
        HapticEffect, 
        EControllerHand::Left, 
        0.5f, 
        0.2f
    );
}
```

### WebXR Integration

```javascript
// WebXR Setup
class XRApplication {
    constructor() {
        this.session = null;
        this.gl = null;
        this.xrReferenceSpace = null;
    }
    
    async init() {
        // Check WebXR support
        if (!navigator.xr) {
            console.error('WebXR not supported');
            return;
        }
        
        // Request XR session
        const supported = await navigator.xr.isSessionSupported('immersive-vr');
        if (!supported) {
            console.error('Immersive VR not supported');
            return;
        }
        
        // Create WebGL context
        this.gl = document.createElement('canvas').getContext('webgl2');
        
        // Request session
        this.session = await navigator.xr.requestSession('immersive-vr', {
            optionalFeatures: ['local-floor', 'bounded-floor', 'hand-tracking'],
            requiredFeatures: ['local-floor']
        });
        
        // Setup reference space
        this.xrReferenceSpace = await this.session.requestReferenceSpace('local-floor');
        
        // Start render loop
        this.session.requestAnimationFrame(this.onXRFrame.bind(this));
    }
    
    onXRFrame(time, frame) {
        const pose = frame.getViewerPose(this.xrReferenceSpace);
        if (pose) {
            // Render scene from each eye's perspective
            for (const view of pose.views) {
                const viewport = this.glLayer.getViewport(view);
                this.gl.viewport(viewport.x, viewport.y, viewport.width, viewport.height);
                this.renderView(view);
            }
        }
        this.session.requestAnimationFrame(this.onXRFrame.bind(this));
    }
}
```

## Performance Optimization

### Frame Time Budget Management

```python
from ar_vr_development import FrameBudgetManager, PerformanceMode

budget_manager = FrameBudgetManager(
    target_framerate=90,
    frame_budget_ms=11.1,
    warning_threshold_ms=9.0,
    critical_threshold_ms=10.0,
)

# Define frame phases
budget_manager.define_phase("input", max_ms=1.0, priority=1)
budget_manager.define_phase("physics", max_ms=2.0, priority=2)
budget_manager.define_phase("ai", max_ms=1.5, priority=3)
budget_manager.define_phase("animation", max_ms=1.5, priority=4)
budget_manager.define_phase("rendering", max_ms=5.0, priority=5)

# Monitor frame performance
@budget_manager.on_frame_complete
def on_frame(frame_stats):
    if frame_stats.over_budget:
        print(f"Frame over budget: {frame_stats.total_ms:.2f}ms")
        for phase in frame_stats.phases:
            if phase.over_budget:
                print(f"  Phase '{phase.name}': {phase.ms:.2f}ms (max: {phase.max_ms}ms)")

# Adaptive quality
budget_manager.enable_adaptive_quality(
    target_gpu_usage=0.8,
    target_cpu_usage=0.7,
    min_render_scale=0.7,
    max_render_scale=1.0,
)
```

### Memory Management

```python
from ar_vr_development import MemoryManager, MemoryPool, AssetLoader

memory = MemoryManager(
    budget_mb=1500,  # Quest 3 memory budget
    pools={
        "textures": MemoryPool(size_mb=500, type="gpu"),
        "meshes": MemoryPool(size_mb=200, type="cpu"),
        "audio": MemoryPool(size_mb=100, type="cpu"),
        "animations": MemoryPool(size_mb=50, type="cpu"),
    },
)

# Asset loading with memory constraints
loader = AssetLoader(memory_manager=memory)
loader.set_quality_overrides({
    Platform.QUEST_3: {"textures": "compressed", "meshes": "lod_auto"},
    Platform.VISION_PRO: {"textures": "high", "meshes": "full"},
})

# Load asset with memory check
asset = loader.load("environment/scene.glb", memory_budget_mb=200)
if asset:
    print(f"Loaded: {asset.name}, size: {asset.memory_usage_mb:.1f}MB")
else:
    print("Failed to load: insufficient memory")

# Monitor memory usage
stats = memory.get_stats()
print(f"Total: {stats.total_mb:.1f}MB / {stats.budget_mb}MB")
print(f"GPU: {stats.gpu_mb:.1f}MB, CPU: {stats.cpu_mb:.1f}MB")
```

### Rendering Optimization

```python
from ar_vr_development import RenderingOptimizer, LODConfig, CullingConfig

optimizer = RenderingOptimizer()

# Configure LOD system
optimizer.set_lod_config(LODConfig(
    screen_coverage_thresholds=[0.3, 0.1, 0.02],
    distance_thresholds=[10, 30, 100],
    transition_mode="dither",
    hysteresis=0.02,
))

# Configure culling
optimizer.set_culling_config(CullingConfig(
    frustum_culling=True,
    occlusion_culling=True,
    small_object_culling=True,
    small_object_threshold=0.01,  # 1% screen coverage
    max_render_distance=100,
))

# Batch optimization
optimizer.batch_static_objects("environment")
optimizer.batch_dynamic_objects("characters", batch_size=100)

# Get optimization report
report = optimizer.analyze_scene()
print(f"Draw calls: {report.before_draw_calls} → {report.after_draw_calls}")
print(f"Triangles: {report.before_triangles:,} → {report.after_triangles:,}")
print(f"Estimated GPU time: {report.estimated_gpu_ms:.2f}ms")
```

## Security Considerations

### Data Privacy and Protection

```python
from ar_vr_development import PrivacyManager, DataClassification

privacy = PrivacyManager(
    classification={
        "hand_tracking_data": DataClassification.BIOMETRIC,
        "eye_tracking_data": DataClassification.BIOMETRIC,
        "voice_data": DataClassification.BIOMETRIC,
        "spatial_map": DataClassification.LOCATION,
        "user_preferences": DataClassification.PERSONAL,
        "analytics": DataClassification.ANONYMIZED,
    },
    retention={
        "hand_tracking_data": "session_only",
        "eye_tracking_data": "session_only",
        "spatial_map": "30_days",
        "analytics": "365_days",
    },
    encryption={
        "hand_tracking_data": "aes_256",
        "eye_tracking_data": "aes_256",
        "spatial_map": "aes_256",
    },
)

# Privacy-compliant data collection
@privacy.on_data_collection
def on_data(data_type, data):
    if data_type == "hand_tracking":
        # Anonymize before storage
        anonymized = privacy.anonymize(data)
        return anonymized
    elif data_type == "spatial_map":
        # Remove identifying information
        sanitized = privacy.sanitize_spatial_data(data)
        return sanitized
    return data

# GDPR compliance
privacy.enable_gdpr_mode(
    data_subject_rights=True,
    right_to_erasure=True,
    data_portability=True,
    consent_management=True,
)
```

### Secure Communication

```python
from ar_vr_development import SecureNetworking, EncryptionConfig

network = SecureNetworking(
    encryption=EncryptionConfig(
        algorithm="AES-256-GCM",
        key_exchange="ECDH",
        certificate_validation=True,
        min_tls_version="1.3",
    ),
    authentication={
        "method": "mutual_tls",
        "client_cert_required": True,
        "certificate_pinning": True,
        "pinned_certificates": ["sha256/abc123..."],
    },
    rate_limiting={
        "max_connections_per_second": 100,
        "max_bandwidth_mbps": 50,
        "ddos_protection": True,
    },
)

# Secure multiplayer
@network.on_connect
def on_client_connect(client):
    print(f"Client connected: {client.id}")
    print(f"Certificate: {client.certificate.subject}")
    print(f"Authenticated: {client.is_authenticated}")
```

### Input Validation

```python
from ar_vr_development import InputValidator, SanitizationConfig

validator = InputValidator(
    config=SanitizationConfig(
        max_string_length=1000,
        allowed_characters=r"^[a-zA-Z0-9\s\-_.]+$",
        sql_injection_protection=True,
        xss_protection=True,
        path_traversal_protection=True,
    ),
)

# Validate user input
safe_name = validator.sanitize_string(user_input)
if safe_name is None:
    print("Invalid input detected")
    return

# Validate spatial coordinates
position = validator.validate_vector3(
    x=raw_x, y=raw_y, z=raw_z,
    min_value=-1000,
    max_value=1000,
    check_nan=True,
    check_inf=True,
)

# Validate file paths
safe_path = validator.validate_file_path(
    path=user_path,
    allowed_directories=["/data/", "/assets/"],
    block_absolute_paths=True,
    block_symlinks=True,
)
```

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Frame drops** | Jittery visuals, motion sickness | Reduce render scale, enable foveated rendering, optimize draw calls |
| **Tracking loss** | Content drifts, loses position | Improve lighting, avoid reflective surfaces, recalibrate sensors |
| **Hand tracking jitter** | Unstable hand positions | Increase smoothing, check lighting, reduce max hands |
| **Audio desync** | Sound delayed from visual | Increase audio buffer, check latency settings |
| **Memory overflow** | App crashes, OOM errors | Reduce texture quality, implement asset streaming |
| **Build failure** | Compilation errors | Check SDK versions, verify platform settings |
| **Network lag** | Delayed multiplayer sync | Increase update rate, implement client-side prediction |
| **Thermal throttling** | Performance degrades over time | Reduce quality, implement adaptive quality, add cooling pauses |

### Debug Logging

```python
from ar_vr_development import DebugLogger, LogLevel

logger = DebugLogger(
    level=LogLevel.DEBUG,
    output=["console", "file", "network"],
    file_path="logs/xr_debug.log",
    network_target="debug-server:9090",
    filters=["rendering", "input", "network"],
)

# Enable performance logging
logger.enable_performance_logging(
    frame_times=True,
    memory_usage=True,
    gpu_usage=True,
    cpu_usage=True,
)

# Debug spatial tracking
logger.enable_tracking_debug(
    show_hand_skeleton=True,
    show_eye_gaze=True,
    show_anchor_positions=True,
    show_plane_detection=True,
)
```

### Performance Profiling

```python
from ar_vr_development import Profiler, ProfilingSession

profiler = Profiler()

# Start profiling session
session = profiler.start_session(
    name="performance_analysis",
    duration_s=60,
    sample_rate=100,  # Hz
)

# Add profiling markers
profiler.add_marker("input_processing")
profiler.add_marker("physics_simulation")
profiler.add_marker("rendering")

# Analyze results
report = session.analyze()
print(f"Average frame time: {report.avg_frame_ms:.2f}ms")
print(f"Worst frame: {report.worst_frame_ms:.2f}ms")
print(f"Frame time distribution:")
print(f"  90th percentile: {report.p90_frame_ms:.2f}ms")
print(f"  95th percentile: {report.p95_frame_ms:.2f}ms")
print(f"  99th percentile: {report.p99_frame_ms:.2f}ms")

# Bottleneck analysis
bottlenecks = report.find_bottlenecks()
for bottleneck in bottlenecks:
    print(f"Bottleneck: {bottleneck.name} ({bottleneck.percentage:.1f}% of frame time)")
```

## API Reference

### Core Classes

```python
class XRProject:
    """Main XR project configuration and management."""
    
    def __init__(self, name: str, engine: str, platforms: List[Platform], 
                 target_framerate: int = 90, render_scale: float = 1.0):
        """Initialize XR project."""
        
    def add_interaction(self, interaction_type: InteractionType, config: dict) -> None:
        """Add interaction configuration."""
        
    def set_performance_profile(self, profile: PerformanceProfile) -> None:
        """Set performance optimization profile."""
        
    def build(self, platform: Platform, configuration: str = "release") -> BuildResult:
        """Build project for specified platform."""
        
    def validate(self) -> ValidationResult:
        """Validate project configuration and assets."""
        
    def get_memory_usage(self) -> MemoryUsage:
        """Get current memory usage statistics."""

class SpatialAnchorManager:
    """Manage spatial anchors in the physical world."""
    
    def __init__(self, cloud_sync: bool = False):
        """Initialize anchor manager."""
        
    def create(self, position: Tuple[float, float, float], 
               rotation: Tuple[float, float, float, float],
               label: str = "", persistent: bool = False) -> SpatialAnchor:
        """Create a new spatial anchor."""
        
    def resolve(self, anchor_id: str) -> Optional[SpatialAnchor]:
        """Resolve an existing anchor."""
        
    def delete(self, anchor_id: str) -> bool:
        """Delete a spatial anchor."""
        
    def list_anchors(self, radius: float = None) -> List[SpatialAnchor]:
        """List all anchors within radius."""

class XRNetworking:
    """Multiplayer XR networking."""
    
    def __init__(self, room_id: str, max_players: int = 8):
        """Initialize networking."""
        
    def sync_object(self, object_id: str, position: Tuple[float, float, float],
                   ownership: str = "dynamic") -> SyncedObject:
        """Synchronize an object across network."""
        
    def send_voice(self, audio_data: bytes) -> None:
        """Send voice data to all players."""
        
    def disconnect(self) -> None:
        """Disconnect from network."""
```

### Configuration Classes

```python
class PerformanceProfile:
    """Performance optimization configuration."""
    
    def __init__(self, target_framerate: int = 90, 
                 ms_per_frame: float = 11.1,
                 fixed_foveated_rendering_level: int = 3,
                 application_spacewarp: bool = True,
                 gpu_skinning: bool = True,
                 single_pass_stereo: bool = True):
        """Initialize performance profile."""
        
    def validate(self) -> bool:
        """Validate profile for target platform."""
        
    def estimate_gpu_load(self) -> float:
        """Estimate GPU utilization."""

class Platform(Enum):
    """Supported XR platforms."""
    QUEST_3 = "quest_3"
    QUEST_PRO = "quest_pro"
    VISION_PRO = "vision_pro"
    HOLOLENS_2 = "hololens_2"
    WEBXR = "webxr"
    PC_VR = "pc_vr"

class InteractionType(Enum):
    """Supported interaction types."""
    HAND_TRACKING = "hand_tracking"
    EYE_TRACKING = "eye_tracking"
    CONTROLLER = "controller"
    VOICE = "voice"
    GAZE = "gaze"
```

## Data Models

### Spatial Data Structures

```python
from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum

@dataclass
class Vector3:
    """3D vector representation."""
    x: float
    y: float
    z: float
    
    def magnitude(self) -> float:
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def normalize(self) -> 'Vector3':
        mag = self.magnitude()
        return Vector3(self.x/mag, self.y/mag, self.z/mag) if mag > 0 else self
    
    def distance_to(self, other: 'Vector3') -> float:
        return ((self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)**2)**0.5

@dataclass
class Quaternion:
    """Quaternion rotation representation."""
    x: float
    y: float
    z: float
    w: float
    
    def to_euler(self) -> Tuple[float, float, float]:
        """Convert to Euler angles (roll, pitch, yaw)."""
        
    @classmethod
    def from_euler(cls, roll: float, pitch: float, yaw: float) -> 'Quaternion':
        """Create from Euler angles."""
        
    def multiply(self, other: 'Quaternion') -> 'Quaternion':
        """Multiply two quaternions."""
        
    def inverse(self) -> 'Quaternion':
        """Get inverse rotation."""

@dataclass
class SpatialAnchor:
    """Spatial anchor data."""
    anchor_id: str
    position: Vector3
    rotation: Quaternion
    label: str
    persistent: bool
    cloud_id: Optional[str]
    created_at: datetime
    expires_at: Optional[datetime]
    metadata: dict

@dataclass
class HandLandmark:
    """Hand tracking landmark."""
    position: Vector3
    confidence: float
    landmark_type: str  # "wrist", "thumb_tip", etc.
    
@dataclass
class HandState:
    """Complete hand tracking state."""
    handedness: str  # "left" or "right"
    landmarks: List[HandLandmark]
    pinch_strength: float
    grab_strength: float
    is_pointing: bool
    is_open_palm: bool
    skeleton: 'HandSkeleton'

@dataclass
class FrameData:
    """Single frame of XR data."""
    timestamp: float
    head_pose: 'Pose'
    left_eye_pose: Optional['Pose']
    right_eye_pose: Optional['Pose']
    left_hand: Optional[HandState]
    right_hand: Optional[HandState]
    controllers: List['ControllerState']
    audio: Optional['AudioFrame']
```

## Deployment Guide

### Build and Deployment Pipeline

```python
from ar_vr_development import DeploymentPipeline, DeploymentTarget

pipeline = DeploymentPipeline(
    project="SpatialCollaboration",
    version="1.2.0",
    targets=[
        DeploymentTarget(
            platform=Platform.QUEST_3,
            store="meta_quest_store",
            signing_key="keystore/release.jks",
            version_code=120,
            min_sdk=29,
            target_sdk=33,
        ),
        DeploymentTarget(
            platform=Platform.VISION_PRO,
            store="apple_app_store",
            provisioning_profile="XR_Distribution",
            bundle_id="com.company.spatialcollab",
        ),
        DeploymentTarget(
            platform=Platform.WEBXR,
            hosting="cdn",
            domain="app.spatialcollab.com",
            ssl_cert=True,
        ),
    ],
    ci_cd={
        "provider": "github_actions",
        "auto_deploy": True,
        "environment_stages": ["staging", "production"],
    },
)

# Run deployment
result = pipeline.deploy(
    environment="production",
    dry_run=False,
    rollback_on_failure=True,
)

print(f"Deployment status: {result.status}")
print(f"Quest Store: {result.targets['quest_3'].status}")
print(f"App Store: {result.targets['vision_pro'].status}")
print(f"Web: {result.targets['webxr'].url}")
```

### Version Management

```python
from ar_vr_development import VersionManager, CompatibilityChecker

version_mgr = VersionManager(
    current_version="1.2.0",
    min_supported_version="1.0.0",
    deprecation_policy="3_versions",
)

# Check compatibility
checker = CompatibilityChecker(version_mgr)
compatibility = checker.check(
    client_version="1.1.0",
    server_version="1.2.0",
    api_version="2.1",
)

print(f"Compatible: {compatibility.is_compatible}")
print(f"Warnings: {compatibility.warnings}")
print(f"Required updates: {compatibility.required_updates}")

# Migration paths
migrations = version_mgr.get_migrations(
    from_version="1.0.0",
    to_version="1.2.0",
)
for migration in migrations:
    print(f"Migration: {migration.description}")
    print(f"  Steps: {len(migration.steps)}")
    print(f"  Breaking changes: {migration.breaking_changes}")
```

## Monitoring & Observability

### Performance Monitoring

```python
from ar_vr_development import MetricsCollector, AlertManager

metrics = MetricsCollector(
    endpoints=[
        {"type": "prometheus", "host": "prometheus", "port": 9090},
        {"type": "datadog", "api_key": "xxx", "app_key": "yyy"},
    ],
    sample_rate=0.1,  # 10% sampling
)

# Custom metrics
metrics.register_metric("frame_time_ms", type="histogram", buckets=[5, 10, 15, 20, 30])
metrics.register_metric("memory_usage_mb", type="gauge")
metrics.register_metric("hand_tracking_confidence", type="summary")
metrics.register_metric("network_latency_ms", type="histogram")

# Record metrics
metrics.record("frame_time_ms", 9.5)
metrics.record("memory_usage_mb", 1200)
metrics.record("hand_tracking_confidence", 0.92)

# Alert configuration
alerts = AlertManager(metrics)
alerts.add_rule(
    name="high_frame_time",
    metric="frame_time_ms",
    condition="avg_5m > 11.1",
    severity="warning",
    notification=["slack", "email"],
)
alerts.add_rule(
    name="memory_pressure",
    metric="memory_usage_mb",
    condition="avg_5m > 1400",
    severity="critical",
    notification=["slack", "pagerduty"],
)
```

### Health Checks

```python
from ar_vr_development import HealthCheck, HealthStatus

health = HealthCheck(
    checks=[
        {"name": "rendering", "type": "frame_rate", "threshold": 85},
        {"name": "memory", "type": "memory_usage", "threshold_mb": 1500},
        {"name": "tracking", "type": "tracking_quality", "threshold": 0.8},
        {"name": "network", "type": "connectivity", "timeout_s": 5},
        {"name": "battery", "type": "battery_level", "threshold_pct": 20},
    ],
    interval_s=30,
)

@health.on_status_change
def on_health_change(check_name: str, old_status: HealthStatus, new_status: HealthStatus):
    print(f"Health check '{check_name}': {old_status} → {new_status}")
    if new_status == HealthStatus.CRITICAL:
        # Trigger automatic recovery
        trigger_recovery(check_name)

# Get current health
status = health.get_status()
print(f"Overall: {status.overall}")
for check in status.checks:
    print(f"  {check.name}: {check.status} ({check.value})")
```

## Testing Strategy

### Unit Testing

```python
import pytest
from ar_vr_development import Vector3, Quaternion, SpatialAnchor

class TestVector3:
    def test_magnitude(self):
        v = Vector3(1, 2, 3)
        assert abs(v.magnitude() - 3.7416573867739413) < 1e-6
    
    def test_normalize(self):
        v = Vector3(0, 3, 4)
        n = v.normalize()
        assert abs(n.magnitude() - 1.0) < 1e-6
        assert n.x == 0.0
        assert abs(n.y - 0.6) < 1e-6
        assert abs(n.z - 0.8) < 1e-6
    
    def test_distance(self):
        a = Vector3(0, 0, 0)
        b = Vector3(1, 0, 0)
        assert abs(a.distance_to(b) - 1.0) < 1e-6

class TestQuaternion:
    def test_from_euler(self):
        q = Quaternion.from_euler(0, 0, 0)
        assert q.w == 1.0
        assert q.x == 0.0
    
    def test_multiply_identity(self):
        q1 = Quaternion(0, 0, 0, 1)
        q2 = Quaternion(0, 0, 0, 1)
        result = q1.multiply(q2)
        assert result.w == 1.0
```

### Integration Testing

```python
import pytest
from ar_vr_development import XRProject, Platform, SpatialAnchorManager

class TestXRProject:
    @pytest.fixture
    def project(self):
        return XRProject(
            name="TestProject",
            engine="unity",
            platforms=[Platform.QUEST_3],
        )
    
    def test_add_interaction(self, project):
        project.add_interaction(InteractionType.HAND_TRACKING, {
            "gesture_recognition": True,
        })
        assert len(project.interactions) == 1
    
    def test_build_success(self, project):
        result = project.build(platform=Platform.QUEST_3)
        assert result.status == "success"
        assert result.apk_size_mb > 0

class TestSpatialAnchors:
    @pytest.fixture
    def anchor_manager(self):
        return SpatialAnchorManager(cloud_sync=False)
    
    def test_create_anchor(self, anchor_manager):
        anchor = anchor_manager.create(
            position=(1, 1, 1),
            rotation=(0, 0, 0, 1),
            label="Test",
        )
        assert anchor.anchor_id is not None
    
    def test_delete_anchor(self, anchor_manager):
        anchor = anchor_manager.create(
            position=(1, 1, 1),
            rotation=(0, 0, 0, 1),
        )
        result = anchor_manager.delete(anchor.anchor_id)
        assert result is True
```

### Performance Testing

```python
import pytest
from ar_vr_development import Profiler, PerformanceBenchmark

class TestPerformance:
    @pytest.fixture
    def benchmark(self):
        return PerformanceBenchmark(
            target_fps=90,
            duration_s=10,
        )
    
    def test_frame_rate_stability(self, benchmark):
        results = benchmark.run()
        assert results.avg_fps >= 89.0
        assert results.min_fps >= 80.0
        assert results.frame_drops_pct < 1.0
    
    def test_memory_stability(self, benchmark):
        results = benchmark.run()
        assert results.memory_growth_mb < 10.0  # No memory leaks
        assert results.peak_memory_mb < 1500.0
    
    def test_tracking_latency(self, benchmark):
        results = benchmark.run()
        assert results.avg_tracking_latency_ms < 20.0
        assert results.max_tracking_latency_ms < 50.0
```

## Versioning & Migration

### Semantic Versioning

```
MAJOR.MINOR.PATCH
│       │       │
│       │       └── Bug fixes, security patches
│       └────────── New features, backwards compatible
└────────────────── Breaking changes
```

### Migration Guide

```python
from ar_vr_development import MigrationRunner, MigrationStep

# Define migration from v1.x to v2.0
migration = MigrationRunner(
    from_version="1.x",
    to_version="2.0.0",
    steps=[
        MigrationStep(
            name="update_api_calls",
            description="Update deprecated API calls",
            script="""
            # Old API
            project.setup_hand_tracking(enabled=True)
            
            # New API
            project.add_interaction(InteractionType.HAND_TRACKING, {
                "enabled": True,
                "skeleton_model": "26_point",
            })
            """,
            breaking=True,
        ),
        MigrationStep(
            name="update_config_format",
            description="Migrate configuration files",
            script="migrate_config_files()",
            breaking=False,
        ),
    ],
)

# Run migration
result = migration.run(dry_run=False)
print(f"Migration complete: {result.success}")
print(f"Steps completed: {result.completed_steps}/{result.total_steps}")
```

### Deprecation Policy

| Version | Deprecated Features | Removal Version |
|---------|-------------------|-----------------|
| 1.5.0 | `old_hand_tracking_api` | 2.0.0 |
| 1.5.0 | `legacy_spatial_anchors` | 2.0.0 |
| 1.6.0 | `deprecated_rendering_pipeline` | 2.1.0 |
| 1.7.0 | `old_networking_protocol` | 3.0.0 |

## Glossary

| Term | Definition |
|------|------------|
| **XR** | Extended Reality (umbrella term for AR, VR, MR) |
| **AR** | Augmented Reality - digital content overlaid on real world |
| **VR** | Virtual Reality - fully immersive digital environment |
| **MR** | Mixed Reality - blend of real and virtual worlds |
| **FOV** | Field of View - the extent of observable world |
| **6DoF** | Six Degrees of Freedom - position + rotation tracking |
| **3DoF** | Three Degrees of Freedom - rotation only tracking |
| **HMD** | Head-Mounted Display |
| **IPD** | Inter-Pupillary Distance |
| **ASW** | Application SpaceWarp - frame interpolation technology |
| **FFR** | Fixed Foveated Rendering - reduce peripheral detail |
| **DFR** | Dynamic Foveated Rendering - eye-tracked foveation |
| **SSP** | Single Pass Stereo - render both eyes in one pass |
| **LOD** | Level of Detail - reduce complexity at distance |
| **Occlusion Culling** | Don't render objects hidden behind others |
| **Draw Call** | CPU instruction to render geometry |
| **Batching** | Combine multiple draw calls into one |
| **GPU Instancing** | Render same mesh multiple times efficiently |
| **PBR** | Physically Based Rendering |
| **HDR** | High Dynamic Range |
| **MSAA** | Multi-Sample Anti-Aliasing |
| **FXAA** | Fast Approximate Anti-Aliasing |
| **TAA** | Temporal Anti-Aliasing |
| **OpenXR** | Cross-platform XR standard |
| **WebXR** | Web-based XR API |
| **Passthrough** | Camera feed for AR on VR headsets |

## Changelog

### Version 2.0.0 (2024-01-15)
- Added Apple Vision Pro support
- Added dynamic foveated rendering
- Improved hand tracking accuracy (26-point model)
- Added cloud anchor synchronization
- Performance improvements (30% faster frame times)

### Version 1.5.0 (2023-10-01)
- Added WebXR support
- Added multiplayer networking
- Added spatial audio integration
- Improved Quest 3 optimization

### Version 1.0.0 (2023-06-01)
- Initial release
- Basic hand tracking
- Spatial anchors
- Unity and Unreal support

## Contributing Guidelines

### Development Setup

```bash
# Clone repository
git clone https://github.com/company/xr-development.git
cd xr-development

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linter
ruff check .

# Format code
ruff format .
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints for all public functions
- Write docstrings for public APIs
- Keep functions under 50 lines
- Keep classes under 300 lines
- Use meaningful variable names
- Add unit tests for new features

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Request review from 2 maintainers
6. Squash and merge after approval

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

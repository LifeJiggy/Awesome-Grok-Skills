---
name: "mixed-reality"
category: "ar-vr"
version: "2.0.0"
tags: ["mixed-reality", "passthrough", "occlusion", "spatial-anchor", "world-meshing", "vision-pro"]
---

# Mixed Reality

## Overview

Mixed reality development toolkit for building experiences that blend virtual content with the physical world using camera passthrough, depth sensing, plane detection, mesh reconstruction, and spatial anchoring. This module supports Apple Vision Pro (visionOS), Meta Quest passthrough, HoloLens spatial mapping, and WebXR hit-test modules with focus on realistic occlusion, lighting estimation, and world-understanding for immersive AR applications.

## Core Capabilities

- **Camera Passthrough**: Real-time camera passthrough with depth occlusion for virtual object placement
- **Plane Detection**: Horizontal and vertical plane detection with classification (floor, wall, table, ceiling)
- **Mesh Reconstruction**: Real-time 3D mesh generation from depth data for environmental understanding
- **Spatial Anchors**: Persistent, cloud-synchronized anchors that survive session boundaries
- **Occlusion**: Virtual object occlusion by real-world geometry using depth buffers
- **Lighting Estimation**: Real-time environment lighting estimation for realistic virtual object rendering
- **Scene Understanding**: Semantic classification of real-world surfaces and objects
- **Shared MR Experiences**: Multi-user shared mixed reality with synchronized spatial content

## Usage

```python
from mixed_reality import (
    PassthroughManager, PlaneDetector, MeshReconstructor, OcclusionManager
)

# Configure passthrough
passthrough = PassthroughManager(
    platform="quest_3",
    depth_mode="medium",
    color_adjustments={"brightness": 1.0, "contrast": 1.1},
)
passthrough.enable()
print(f"Passthrough: {passthrough.status}")

# Plane detection
detector = PlaneDetector()
planes = detector.detect(max_planes=20, min_area_sqm=0.25)
for plane in planes:
    print(f"  {plane.classification}: {plane.area_sqm:.2f}m² at ({plane.center[0]:.1f}, {plane.center[1]:.1f}, {plane.center[2]:.1f})")

# Mesh reconstruction
mesh = MeshReconstructor(resolution="medium", max_triangles=100000)
mesh_data = mesh.reconstruct()
print(f"Mesh: {mesh_data.vertex_count} vertices, {mesh_data.triangle_count} triangles")

# Occlusion
occlusion = OcclusionManager(depth_buffer="environment")
occlusion.enable_for_object("virtual-character")
```

```python
# Place virtual object on detected plane
from mixed_reality import MRSceneManager

scene = MRSceneManager()
# Find a horizontal surface
table = detector.find_plane(classification="table", min_area=0.5)
if table:
    anchor = scene.place_object(
        object_id="coffee-mug",
        mesh_path="models/mug.glb",
        plane_id=table.plane_id,
        offset=(0, 0.05, 0),
    )
    print(f"Placed mug on table at {anchor.position}")
```

## Best Practices

- Always use depth-based occlusion for virtual objects — objects floating over real geometry break presence
- Detect planes before placing objects — never assume surfaces exist
- Use environment lighting estimation to match virtual object shadows and reflections
- Test passthrough quality in different lighting conditions — low light degrades depth sensing
- Implement mesh collision for interactive virtual objects that should interact with real surfaces
- Use persistent anchors for objects that should stay in place across sessions
- Limit mesh resolution to maintain performance — medium resolution is sufficient for most interactions
- Implement scene semantics (floor, wall, furniture) for context-aware object placement
- Account for passthrough latency (~12ms) when synchronizing virtual and real movements
- Test MR experiences on actual hardware — simulator passthrough differs from real cameras

## Related Modules

- **ar-vr-development** — Cross-platform XR development patterns
- **spatial-computing** — Spatial anchors, meshes, and scene understanding
- **3d-rendering** — Optimized rendering for passthrough environments
- **gesture-recognition** — Hand tracking in mixed reality contexts
- **ambient-computing** → **proximity-sensing** — Physical space awareness

## Advanced Configuration

### Passthrough Quality Profiles

```python
from mixed_reality import PassthroughConfig, DepthConfig, QualityPreset

# High-quality passthrough for Vision Pro
vision_config = PassthroughConfig(
    platform="vision_pro",
    color_adjustments={
        "brightness": 1.0,
        "contrast": 1.1,
        "saturation": 1.0,
        "white_balance": 6500,  # Kelvin
    },
    depth=DepthConfig(
        mode="high",
        temporal_smoothing=True,
        hole_filling=True,
        confidence_threshold=0.7,
    },
    occlusion={
        "enabled": True,
        "soft_edges": True,
        "edge_blur_radius": 2,
        "depth_bias": 0.01,
    },
    performance={
        "target_fps": 90,
        "max_latency_ms": 12,
        "adaptive_quality": True,
    },
)

# Quest 3 passthrough (lower quality but functional)
quest_config = PassthroughConfig(
    platform="quest_3",
    color_adjustments={
        "brightness": 1.1,
        "contrast": 1.2,
        "saturation": 0.9,
    },
    depth=DepthConfig(
        mode="medium",
        temporal_smoothing=True,
        hole_filling=True,
        confidence_threshold=0.6,
    ),
    occlusion={
        "enabled": True,
        "soft_edges": False,
        "edge_blur_radius": 0,
        "depth_bias": 0.02,
    },
)
```

### Advanced Plane Detection

```python
from mixed_reality import PlaneDetector, PlaneClassification, PlaneFilter

detector = PlaneDetector(
    max_planes=50,
    min_area_sqm=0.1,
    classification_enabled=True,
    alignment_types=["horizontal", "vertical"],
)

# Configure filtering
filter_config = PlaneFilter(
    include_classifications=[
        PlaneClassification.FLOOR,
        PlaneClassification.WALL,
        PlaneClassification.CEILING,
        PlaneClassification.TABLE,
        PlaneClassification.SEAT,
    ],
    min_confidence=0.8,
    min_area_sqm=0.25,
    max_distance_m=10.0,
    temporal_consistency=True,  # Require detection across multiple frames
    consistency_window=5,       # Frames
)

# Detect planes with filtering
planes = detector.detect(filter_config=filter_config)

# Semantic understanding
for plane in planes:
    print(f"Classification: {plane.classification}")
    print(f"Area: {plane.area_sqm:.2f} m²")
    print(f"Normal: {plane.normal}")
    print(f"Center: {plane.center}")
    print(f"Confidence: {plane.confidence:.2f}")
    print(f"AABB: {plane.bounding_box}")
```

### Mesh Reconstruction Optimization

```python
from mixed_reality import MeshReconstructor, MeshConfig, MeshOptimization

mesh_config = MeshConfig(
    resolution="high",  # low, medium, high, ultra
    max_triangles=200000,
    max_vertices=100000,
    update_frequency_hz=10,
    occlusion_mesh=True,  # Generate mesh for occlusion
    physics_mesh=True,    # Generate mesh for physics
)

reconstructor = MeshReconstructor(config=mesh_config)

# Optimization settings
optimization = MeshOptimization(
    voxel_size=0.02,          # 2cm resolution
    simplification_ratio=0.5,  # Reduce triangle count by 50%
    smoothing_iterations=2,
    hole_filling=True,
    planar_region_detection=True,
    merged_planar_regions=True,
)

# Process mesh
mesh_data = reconstructor.reconstruct(optimization=optimization)

# Analyze mesh quality
print(f"Vertices: {mesh_data.vertex_count}")
print(f"Triangles: {mesh_data.triangle_count}")
print(f"Mesh bounds: {mesh_data.bounds}")
print(f"Update time: {mesh_data.update_time_ms:.2f}ms")

# Generate occupancy grid for physics
occupancy = reconstructor.generate_occupancy_grid(
    cell_size=0.1,
    include_dynamic_objects=False,
)
```

### Scene Understanding Advanced

```python
from mixed_reality import SceneUnderstanding, SemanticLabel, SceneGraph

scene = SceneUnderstanding(
    update_frequency_hz=5,
    enable_persistence=True,
    cloud_sync=False,
)

# Comprehensive scene analysis
analysis = scene.analyze(
    include_semantics=True,
    include_furniture=True,
    include_lighting=True,
    include_acoustics=True,
)

print(f"Room type: {analysis.room_type}")
print(f"Dimensions: {analysis.dimensions}")
print(f"Lighting: {analysis.lighting_condition}")

# Semantic elements
for element in analysis.elements:
    print(f"  {element.type}: {element.label}")
    print(f"    Confidence: {element.confidence:.2f}")
    print(f"    Position: {element.position}")
    print(f"    Bounding box: {element.bounding_box}")

# Scene graph for spatial relationships
scene_graph = analysis.scene_graph
print(f"Root: {scene_graph.root.label}")
for relation in scene_graph.relations:
    print(f"  {relation.subject} {relation.predicate} {relation.object}")
```

## Architecture Patterns

### Mixed Reality Application Architecture

```
+------------------------------------------------------------------+
|                  Mixed Reality Application Architecture           |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------+    +----------------+    +----------------+  |
|  |  Perception    |    |  World         |    |  Rendering     |  |
|  |  Layer         |    |  Understanding |    |  Layer         |  |
|  |                |    |  Layer         |    |                |  |
|  |  Camera Stream |    |                |    |                |  |
|  |  Depth Map     |<-->|  Plane Detect  |<-->|  Occlusion     |  |
|  |  IMU Data      |    |  Mesh Recon    |    |  Lighting Est  |  |
|  |  GPS/Beacons   |    |  Scene Semantic|    |  Shadow Maps   |  |
|  +-------+--------+    +-------+--------+    +-------+--------+  |
|          |                    |                     |             |
|          v                    v                     v             |
|  +----------------------------------------------------------------+
|  |                    Spatial Processing Engine                   |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Anchor      |  |  Spatial     |  |  Coordinate  |          |
|  |  |  Manager     |  |  Mapping     |  |  Transform   |          |
|  |  |              |  |              |  |              |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
|                              |                                    |
|                              v                                    |
|  +----------------------------------------------------------------+
|  |                    Interaction Layer                           |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Hand        |  |  Eye         |  |  Voice        |          |
|  |  |  Tracking    |  |  Tracking    |  |  Commands     |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Object      |  |  Surface     |  |  Spatial      |          |
|  |  |  Manipulate  |  |  Interaction |  |  Audio        |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
+------------------------------------------------------------------+
```

### Depth Processing Pipeline

```
Raw Depth Stream (60Hz)
        |
        v
+-------------------+
|  Temporal Filter  |  Smooth noise over 3-5 frames
+-------------------+
        |
        v
+-------------------+
|  Hole Filling     |  Fill missing depth values
+-------------------+
        |
        v
+-------------------+
|  Edge Smoothing   |  Reduce depth discontinuities
+-------------------+
        |
        v
+-------------------+
|  Plane Segmentation|  Extract planar regions
+-------------------+
        |
        v
+-------------------+
|  Mesh Generation  |  Create triangle mesh
+-------------------+
        |
        v
+-------------------+
|  Semantic Labeling|  Classify surfaces
+-------------------+
        |
        v
+-------------------+
|  Scene Update     |  Update world model
+-------------------+
```

### Occlusion Processing Flow

```
Virtual Object Render Pass
        |
        v
+-------------------+
|  Depth Pre-Pass   |  Render virtual depth
+-------------------+
        |
        v
+-------------------+
|  Real Depth Read  |  Sample real depth buffer
+-------------------+
        |
        v
+-------------------+
|  Depth Comparison |  Compare real vs virtual
+-------------------+
        |
        v
+-------------------+
|  Occlusion Mask   |  Generate occlusion mask
+-------------------+
        |
        v
+-------------------+
|  Edge Processing  |  Soft/hard edge treatment
+-------------------+
        |
        v
+-------------------+
|  Final Composite  |  Blend with passthrough
+-------------------+
```

## Integration Guide

### Unity MR Toolkit Integration

```csharp
// Mixed Reality Toolkit Setup
using Microsoft.MixedReality.Toolkit;
using Microsoft.MixedReality.Toolkit.SpatialAwareness;

public class MRSceneManager : MonoBehaviour
{
    [SerializeField] private MixedRealityToolkit toolkit;
    
    void Start()
    {
        // Configure spatial awareness
        var spatialAwareness = toolkit.GetComponent<IMixedRealitySpatialAwarenessSystem>();
        
        // Enable plane detection
        var planeObserver = spatialAwareness.GetObserver<SpatialAwarenessPlaneObserver>();
        planeObserver.Resume();
        
        // Configure mesh observer
        var meshObserver = spatialAwareness.GetObserver<SpatialAwarenessMeshObserver>();
        meshObserver.LevelOfDetail = SpatialAwarenessMeshLevelOfDetail.Medium;
        meshObserver.OcclusionMaterial = occlusionMaterial;
        
        // Subscribe to events
        planeObserver.PlanesDetected += OnPlanesDetected;
        meshObserver.MeshAdded += OnMeshAdded;
        meshObserver.MeshUpdated += OnMeshUpdated;
    }
    
    void OnPlanesDetected(object sender, SpatialAwarenessEventData<Plane> eventData)
    {
        foreach (var plane in eventData.NewData)
        {
            Debug.Log($"Plane detected: {plane.SurfaceType}, Area: {plane.Area}");
        }
    }
}
```

### Vision Pro visionOS Integration

```swift
// visionOS RealityKit Integration
import RealityKit
import ARKit

struct MixedRealityView: View {
    @State private var anchorEntity: AnchorEntity?
    @State private var meshEntity: MeshResource?
    
    var body: some View {
        RealityView { content in
            // Configure scene understanding
            let sceneReconstruction = ARKitSession()
            
            // Enable plane detection
            let worldTracking = WorldTrackingProvider()
            worldTracking.start()
            
            // Add spatial anchor
            let anchor = AnchorEntity(.plane(.horizontal, classification: .table))
            content.add(anchor)
            self.anchorEntity = anchor
            
            // Load virtual content
            let model = try await Entity.load(named: "VirtualObject")
            anchor.addChild(model)
        }
        .gesture(DragGesture().targetedToAnyEntity())
            .onChanged { value in
                // Handle object manipulation
                let translation = value.convert3D(value.location3D, from: .local, to: anchorEntity!)
                anchorEntity?.position = translation
            }
    }
}
```

### WebXR MR Integration

```javascript
// WebXR Mixed Reality Setup
class MixedRealityApp {
    async init() {
        // Check MR support
        const supported = await navigator.xr.isSessionSupported('immersive-ar');
        if (!supported) {
            console.error('Immersive AR not supported');
            return;
        }
        
        // Request MR session with features
        this.session = await navigator.xr.requestSession('immersive-ar', {
            requiredFeatures: ['local-floor', 'hit-test'],
            optionalFeatures: ['dom-overlay', 'depth-sensing', 'plane-detection'],
            depthSensingUsage: 'cpu-optimized',
        });
        
        // Setup hit testing
        this.hitTestSource = await this.session.requestHitTestSource({
            space: this.referenceSpace,
        });
        
        // Setup plane detection
        this.planes = [];
        this.session.addEventListener('planeschanged', (event) => {
            this.planes = event.planes;
        });
        
        // Render loop
        this.session.requestAnimationFrame(this.render.bind(this));
    }
    
    render(time, frame) {
        const pose = frame.getViewerPose(this.referenceSpace);
        
        // Perform hit test
        if (this.hitTestSource) {
            const hitResults = frame.getHitTestResults(this.hitTestSource);
            if (hitResults.length > 0) {
                const hit = hitResults[0];
                this.placeVirtualObject(hit);
            }
        }
        
        // Render scene
        for (const view of pose.views) {
            this.renderView(view);
        }
        
        this.session.requestAnimationFrame(this.render.bind(this));
    }
}
```

## Performance Optimization

### Passthrough Optimization

```python
from mixed_reality import PassthroughOptimizer, PerformanceBudget

optimizer = PassthroughOptimizer(
    budget=PerformanceBudget(
        total_frame_budget_ms=11.1,
        passthrough_budget_ms=3.0,
        depth_processing_budget_ms=2.0,
        mesh_update_budget_ms=2.0,
        occlusion_budget_ms=1.0,
    ),
)

# Optimization strategies
optimizer.enable_strategy("temporal_reprojection")
optimizer.enable_strategy("adaptive_resolution")
optimizer.enable_strategy("predictive_occlusion")
optimizer.set_lod_strategy(
    near_distance=2.0,
    far_distance=10.0,
    near_quality="ultra",
    far_quality="low",
)

# Monitor performance
stats = optimizer.get_stats()
print(f"Passthrough latency: {stats.passthrough_latency_ms:.2f}ms")
print(f"Depth processing: {stats.depth_processing_ms:.2f}ms")
print(f"Mesh update: {stats.mesh_update_ms:.2f}ms")
print(f"Occlusion: {stats.occlusion_ms:.2f}ms")
```

### Memory Management for MR

```python
from mixed_reality import MRMemoryManager, MeshCache

memory_mgr = MRMemoryManager(
    total_budget_mb=500,
    passthrough_buffer_mb=100,
    depth_buffer_mb=150,
    mesh_buffer_mb=200,
    texture_buffer_mb=50,
)

# Mesh caching
mesh_cache = MeshCache(
    max_size_mb=100,
    eviction_policy="lru",
    persistence_enabled=True,
    cache_path="/data/mesh_cache",
)

# Load mesh from cache or reconstruct
mesh = mesh_cache.get("room_mesh_v1")
if mesh is None:
    mesh = reconstructor.reconstruct()
    mesh_cache.put("room_mesh_v1", mesh)

# Monitor memory
stats = memory_mgr.get_stats()
print(f"Total usage: {stats.total_mb:.1f}MB")
print(f"Mesh cache hit rate: {mesh_cache.hit_rate:.2%}")
```

## Security Considerations

### Privacy Protection

```python
from mixed_reality import PrivacyManager, DataAnonymizer

privacy = PrivacyManager(
    passthrough_retention="session_only",
    depth_data_retention="none",
    mesh_data_retention="none",
    semantic_data_retention="none",
)

# Anonymize captured data
anonymizer = DataAnonymizer(
    blur_faces=True,
    blur_text=True,
    blur_identifiers=True,
    blur_sensitive_objects=True,
)

# Process passthrough frame
processed_frame = anonymizer.process_frame(passthrough_frame)

# Delete all data on session end
privacy.enable_auto_cleanup(
    trigger="session_end",
    secure_delete=True,
    verification=True,
)
```

### Secure Spatial Data

```python
from mixed_reality import SpatialDataSecurity, EncryptionManager

security = SpatialDataSecurity(
    encrypt_mesh_data=True,
    encrypt_anchors=True,
    encrypt_semantic_labels=True,
    key_rotation_days=30,
)

# Encrypt spatial data before storage
encrypted_mesh = security.encrypt(mesh_data)
security.store(encrypted_mesh, "mesh_v1.enc")

# Decrypt for use
decrypted_mesh = security.decrypt("mesh_v1.enc")
```

## Troubleshooting Guide

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Passthrough black** | No camera feed | Check permissions, restart session |
| **Depth holes** | Missing depth data | Improve lighting, check sensors |
| **Mesh artifacts** | Incorrect geometry | Increase resolution, check tracking |
| **Occlusion glitches** | Virtual objects visible through real objects | Adjust depth bias, check latency |
| **Plane detection slow** | Takes time to find surfaces | Increase update frequency, check lighting |
| **Memory pressure** | App crashes | Reduce mesh resolution, increase eviction |
| **Latency issues** | Delayed response | Reduce processing complexity |
| **Tracking loss** | Content drifts | Recalibrate, check environment |

## API Reference

### Core Classes

```python
class PassthroughManager:
    """Manage camera passthrough."""
    
    def __init__(self, platform: str, depth_mode: str = "medium"):
        """Initialize passthrough."""
        
    def enable(self) -> None:
        """Enable passthrough."""
        
    def disable(self) -> None:
        """Disable passthrough."""
        
    def adjust_color(self, **kwargs) -> None:
        """Adjust passthrough color."""
        
    def get_frame(self) -> PassthroughFrame:
        """Get current passthrough frame."""

class PlaneDetector:
    """Detect planar surfaces."""
    
    def __init__(self, max_planes: int = 20):
        """Initialize plane detector."""
        
    def detect(self, min_area_sqm: float = 0.25) -> List[Plane]:
        """Detect planes."""
        
    def find_plane(self, classification: str, min_area: float = 0.5) -> Optional[Plane]:
        """Find specific plane type."""

class MeshReconstructor:
    """Reconstruct 3D mesh from depth."""
    
    def __init__(self, resolution: str = "medium", max_triangles: int = 100000):
        """Initialize mesh reconstructor."""
        
    def reconstruct(self) -> MeshData:
        """Reconstruct mesh."""
        
    def generate_occupancy_grid(self, cell_size: float = 0.1) -> OccupancyGrid:
        """Generate occupancy grid for physics."""
```

## Data Models

```python
@dataclass
class Plane:
    """Detected plane."""
    plane_id: str
    classification: str
    center: Vector3
    normal: Vector3
    area_sqm: float
    confidence: float
    bounding_box: BoundingBox
    vertices: List[Vector3]

@dataclass
class MeshData:
    """Reconstructed mesh."""
    vertex_count: int
    triangle_count: int
    vertices: np.ndarray
    triangles: np.ndarray
    normals: np.ndarray
    bounds: BoundingBox
    update_time_ms: float

@dataclass
class SemanticElement:
    """Semantic scene element."""
    type: str
    label: str
    confidence: float
    position: Vector3
    bounding_box: BoundingBox
    parent: Optional[str]

@dataclass
class OcclusionResult:
    """Occlusion computation result."""
    occluded: bool
    depth_difference: float
    confidence: float
    edge_softness: float
```

## Deployment Guide

### Build Configuration

```python
from mixed_reality import MRBuildConfig, PlatformConfig

config = MRBuildConfig(
    platforms=[
        PlatformConfig(
            platform="quest_3",
            min_sdk=29,
            target_sdk=33,
            features=["passthrough", "depth", "mesh", "occlusion"],
            permissions=["CAMERA", "BODY_SENSORS"],
        ),
        PlatformConfig(
            platform="vision_pro",
            min_ios=17,
            features=["passthrough", "spatial", "hand_tracking"],
            entitlements=["com.apple.developer.arkit"],
        ),
    ],
    optimization={
        "passthrough_quality": "auto",
        "mesh_resolution": "adaptive",
        "depth_processing": "gpu",
    },
)
```

## Monitoring & Observability

```python
from mixed_reality import MRMetrics, HealthMonitor

metrics = MRMetrics(
    tracks=[
        "passthrough_latency",
        "depth_accuracy",
        "mesh_quality",
        "occlusion_accuracy",
        "plane_detection_time",
    ],
    sample_rate=0.1,
)

monitor = HealthMonitor(
    checks=[
        {"name": "passthrough_fps", "threshold": 85},
        {"name": "depth_noise", "threshold": 0.02},
        {"name": "mesh_update_rate", "threshold": 8},
    ],
    alert_threshold="warning",
)
```

## Testing Strategy

```python
import pytest
from mixed_reality import PlaneDetector, MeshReconstructor

class TestPlaneDetection:
    def test_detect_horizontal_plane(self):
        detector = PlaneDetector()
        planes = detector.detect(min_area_sqm=0.5)
        assert any(p.classification == "floor" for p in planes)
    
    def test_plane_confidence(self):
        detector = PlaneDetector()
        planes = detector.detect()
        for plane in planes:
            assert plane.confidence >= 0.5

class TestMeshReconstruction:
    def test_mesh_quality(self):
        reconstructor = MeshReconstructor(resolution="medium")
        mesh = reconstructor.reconstruct()
        assert mesh.vertex_count > 0
        assert mesh.triangle_count > 0
```

## Versioning & Migration

| Version | Changes | Breaking |
|---------|---------|----------|
| 2.0.0 | Added Vision Pro support, improved depth accuracy | Yes (API changes) |
| 1.5.0 | Added mesh reconstruction, improved plane detection | No |
| 1.0.0 | Initial release with basic passthrough | N/A |

## Glossary

| Term | Definition |
|------|------------|
| **Passthrough** | Camera feed displayed in headset |
| **Depth Map** | Distance values for each pixel |
| **Occlusion** | Real objects blocking virtual objects |
| **Plane Detection** | Finding flat surfaces in environment |
| **Mesh Reconstruction** | Creating 3D geometry from depth |
| **Semantic Understanding** | Classifying real-world objects |
| **Spatial Anchor** | Fixed point in physical space |
| **Scene Understanding** | Comprehensive environment analysis |

## Changelog

### 2.0.0 (2024-01-15)
- Added Apple Vision Pro support
- Improved depth accuracy (30%)
- Added semantic scene understanding
- Performance improvements

### 1.5.0 (2023-10-01)
- Added mesh reconstruction
- Improved plane detection
- Added occlusion support

### 1.0.0 (2023-06-01)
- Initial release

## Contributing Guidelines

```bash
# Development setup
git clone https://github.com/company/mixed-reality.git
cd mixed-reality
pip install -e ".[dev]"

# Run tests
pytest tests/

# Code style
ruff check .
ruff format .
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

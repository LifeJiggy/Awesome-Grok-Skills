---
name: "spatial-computing"
category: "ar-vr"
version: "2.0.0"
tags: ["spatial-computing", "spatial-anchors", "world-mapping", "scene-understanding", "vision-pro", "depth-sensing"]
---

# Spatial Computing

## Overview

Spatial computing platform for creating applications that understand and interact with 3D physical space. This module provides spatial anchor management, world mapping and reconstruction, scene understanding, spatial persistence, cloud anchor synchronization, and spatial data APIs. Supports Apple visionOS spatial computing concepts, Meta Quest scene API, and cross-platform spatial abstractions for building applications that are aware of and responsive to the physical environment.

## Core Capabilities

- **Spatial Anchors**: Create, persist, and share anchors in physical space with cloud synchronization
- **World Mapping**: Real-time 3D reconstruction of the physical environment with semantic labeling
- **Scene Understanding**: Identify floors, walls, ceilings, furniture, and architectural features
- **Spatial Persistence**: Save and restore spatial content across sessions and devices
- **Cloud Synchronization**: Share spatial anchors between devices and users via cloud services
- **Spatial Queries**: Ray-cast, overlap test, and spatial proximity queries against the environment
- **Coordinate Systems**: Handle world-space, body-space, and head-space coordinate transformations
- **Spatial Audio**: Position audio sources in 3D space with occlusion and reverb estimation

## Usage

```python
from spatial_computing import (
    SpatialAnchorService, WorldMap, SceneUnderstanding, SpatialQuery
)

# Create and persist spatial anchors
anchor_service = SpatialAnchorService(cloud_sync=True)
anchor = anchor_service.create_anchor(
    position=(1.5, 1.0, 2.0),
    rotation=(0, 0, 0, 1),
    name="Virtual Display",
    persistent=True,
)
print(f"Anchor: {anchor.anchor_id}")
print(f"Cloud ID: {anchor.cloud_anchor_id}")

# World mapping
world_map = WorldMap(resolution="medium", max_depth_m=10.0)
mesh = world_map.reconstruct()
print(f"World mesh: {mesh.vertex_count} vertices, {mesh.triangle_count} triangles")

# Scene understanding
scene = SceneUnderstanding()
elements = scene.analyze()
for elem in elements:
    print(f"  {elem.type}: {elem.label} ({elem.confidence:.0%})")

# Spatial queries
query = SpatialQuery(world_map)
hit = query.raycast(origin=(0, 1.5, 0), direction=(0, -1, 0), max_distance=5.0)
if hit:
    print(f"\nRaycast hit: {hit.point} on {hit.object_label}")

# Proximity check
nearby = query.find_nearby(position=(1.5, 1.0, 2.0), radius=2.0)
print(f"Objects within 2m: {len(nearby)}")
```

## Best Practices

- Use cloud anchors for shared experiences — local anchors don't survive app reinstalls
- Set appropriate world mapping resolution — high resolution is expensive and rarely needed
- Query scene understanding results at startup and on significant environment changes
- Use spatial anchors with associated metadata for richer context (what the anchor represents)
- Handle anchor tracking loss gracefully — re-localize or prompt user to re-scan
- Use coordinate system transforms when mixing local and world-space content
- Implement spatial persistence for user-created content that should survive sessions
- Test spatial computing features in varied environments (small room, large hall, outdoors)
- Cache world map data locally to reduce cloud bandwidth and improve startup time
- Use semantic labels from scene understanding for context-aware interactions

## Related Modules

- **mixed-reality** — Camera passthrough and depth-based interactions
- **ar-vr-development** — XR application development patterns
- **3d-rendering** — Rendering virtual content in spatial contexts
- **gesture-recognition** — Spatial gesture inputs
- **ambient-computing** → **proximity-sensing** — Physical proximity detection

## Advanced Configuration

### Spatial Anchor Cloud Configuration

```python
from spatial_computing import CloudAnchorConfig, SyncStrategy, ConflictResolution

cloud_config = CloudAnchorConfig(
    provider="google_cloud_anchors",  # or "apple_cloudkit", "custom"
    sync_strategy=SyncStrategy.BIDIRECTIONAL,
    conflict_resolution=ConflictResolution.LAST_WRITE_WINS,
    persistence={
        "ttl_days": 365,
        "max_anchors_per_user": 100,
        "max_anchors_per_device": 50,
        "encryption_at_rest": True,
        "compression": "lz4",
    },
    networking={
        "sync_interval_s": 30,
        "retry_attempts": 3,
        "retry_backoff_ms": [100, 500, 2000],
        "timeout_s": 10,
        "batch_size": 10,
    },
    caching={
        "local_cache_size_mb": 100,
        "cache_ttl_s": 300,
        "preload_anchors": True,
        "preload_radius_m": 50.0,
    },
)

# Advanced anchor metadata
anchor_metadata = {
    "user_id": "user123",
    "room_id": "office_01",
    "creation_context": {
        "device": "quest_3",
        "os_version": "59.0",
        "app_version": "2.1.0",
        "tracking_quality": 0.95,
    },
    "usage_stats": {
        "access_count": 42,
        "last_accessed": "2024-01-15T10:30:00Z",
        "shared_with": ["user456", "user789"],
    },
    "spatial_context": {
        "floor_level": 1,
        "room_type": "office",
        "nearby_anchors": ["anchor_001", "anchor_002"],
    },
}
```

### World Mapping Advanced Configuration

```python
from spatial_computing import WorldMapConfig, MappingMode, UpdateStrategy

world_map_config = WorldMapConfig(
    mapping_mode=MappingMode.CONTINUOUS,
    resolution="high",
    max_depth_m=20.0,
    update_strategy=UpdateStrategy.INCREMENTAL,
    quality={
        "voxel_size": 0.02,  # 2cm resolution
        "surface_noise_threshold": 0.01,
        "min_cluster_size": 100,
        "merge_distance": 0.1,
        "simplification_ratio": 0.5,
    },
    semantic={
        "enabled": True,
        "labels": [
            "floor", "wall", "ceiling", "table", "chair",
            "sofa", "bed", "door", "window", "plant",
        ],
        "confidence_threshold": 0.7,
        "update_on_change": True,
    },
    persistence={
        "save_interval_s": 60,
        "compression": "zstd",
        "version_history": 5,
        "backup_on_update": True,
    },
)

# Mapping progress tracking
@world_map_config.on_progress
def on_mapping_progress(progress):
    print(f"Mapping: {progress.percentage:.1f}%")
    print(f"Coverage: {progress.coverage_sqm:.2f} m²")
    print(f"Quality: {progress.quality_score:.2f}")
    print(f"Vertices: {progress.vertex_count:,}")
    print(f"Triangles: {progress.triangle_count:,}")
```

### Scene Understanding Advanced

```python
from spatial_computing import SceneUnderstandingConfig, SemanticModel

scene_config = SceneUnderstandingConfig(
    semantic_model=SemanticModel.DEEP_LAB_V3,
    update_frequency_hz=5,
    enable_persistence=True,
    cloud_sync=False,
    analysis={
        "room_classification": True,
        "furniture_detection": True,
        "object_recognition": True,
        "people_detection": True,
        "activity_recognition": True,
        "lighting_analysis": True,
        "acoustic_analysis": True,
    },
    output={
        "scene_graph": True,
        "occupancy_grid": True,
        "navigation_mesh": True,
        "semantic_mask": True,
    },
)

# Comprehensive scene analysis
analysis = scene_config.analyze()
print(f"Room type: {analysis.room_type}")
print(f"Dimensions: {analysis.dimensions}")
print(f"Occupants: {analysis.occupant_count}")
print(f"Lighting: {analysis.lighting_condition}")
print(f"Noise level: {analysis.noise_level}")

# Scene graph
for relation in analysis.scene_graph.relations:
    print(f"  {relation.subject} {relation.predicate} {relation.object}")
```

## Architecture Patterns

### Spatial Computing Architecture

```
+------------------------------------------------------------------+
|                  Spatial Computing Architecture                   |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------+    +----------------+    +----------------+  |
|  |  Input         |    |  Spatial       |    |  Output        |  |
|  |  Layer         |    |  Processing    |    |  Layer         |  |
|  |                |    |                |    |                |  |
|  |  Depth Camera  |    |  Point Cloud   |    |  Spatial       |  |
|  |  RGB Camera    |<-->|  Processing    |<-->|  Anchors       |  |
|  |  IMU           |    |  Mesh Recon    |    |  World Map     |  |
|  |  Hand Tracking |    |  Plane Detect  |    |  Scene Graph   |  |
|  +-------+--------+    +-------+--------+    +-------+--------+  |
|          |                    |                     |             |
|          v                    v                     v             |
|  +----------------------------------------------------------------+
|  |                    Spatial Data Layer                           |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Anchor      |  |  World Map   |  |  Scene       |          |
|  |  |  Store       |  |  Store       |  |  Store       |          |
|  |  |              |  |              |  |              |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
|                              |                                    |
|                              v                                    |
|  +----------------------------------------------------------------+
|  |                    Cloud Sync Layer                            |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Anchor      |  |  World Map   |  |  Conflict   |          |
|  |  |  Sync        |  |  Sync        |  |  Resolution |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
+------------------------------------------------------------------+
```

### Anchor Resolution Flow

```
Anchor Request
        |
        v
+-------------------+
|  Check Local Cache|  Look for anchor in local storage
+-------------------+
        |
        v
+-------------------+
|  Found in Cache?  |---Yes---> Return anchor
+-------------------+              |
        | No                       v
        v                    +-----------+
+-------------------+       |  Validate |
|  Query Cloud      |       |  Anchor   |
+-------------------+       +-----------+
        |                         |
        v                         v
+-------------------+       +-----------+
|  Found in Cloud?  |---No---> Return None
+-------------------+
        | Yes
        v
+-------------------+
|  Download Anchor  |
+-------------------+
        |
        v
+-------------------+
|  Store Locally    |
+-------------------+
        |
        v
+-------------------+
|  Return Anchor    |
+-------------------+
```

### Spatial Query Pipeline

```
Query Request (Raycast/Overlap/Proximity)
        |
        v
+-------------------+
|  Validate Query   |  Check parameters
+-------------------+
        |
        v
+-------------------+
|  Transform Space  |  Convert to world coordinates
+-------------------+
        |
        v
+-------------------+
|  Execute Query    |  Against world map
+-------------------+
        |
        v
+-------------------+
|  Filter Results   |  Apply filters
+-------------------+
        |
        v
+-------------------+
|  Rank Results     |  Sort by relevance
+-------------------+
        |
        v
+-------------------+
|  Return Results   |
+-------------------+
```

## Integration Guide

### Unity Spatial Computing

```csharp
// Unity Spatial Anchor Setup
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;

public class SpatialAnchorManager : MonoBehaviour
{
    [SerializeField] private ARAnchorManager anchorManager;
    [SerializeField] private ARMeshManager meshManager;
    
    void Start()
    {
        // Track anchors
        anchorManager.anchorsChanged += OnAnchorsChanged;
        
        // Track meshes
        meshManager.meshesChanged += OnMeshesChanged;
    }
    
    public async Task<ARAnchor> CreateAnchor(Vector3 position, string name)
    {
        // Create anchor at position
        var anchorPrefab = anchorManager.anchorPrefab;
        var anchorGO = Instantiate(anchorPrefab, position, Quaternion.identity);
        anchorGO.name = name;
        
        var anchor = anchorGO.GetComponent<ARAnchor>();
        if (anchor == null)
        {
            anchor = anchorGO.AddComponent<ARAnchor>();
        }
        
        // Save to cloud
        var cloudAnchor = await anchorManager.TryAddCloudAnchorAsync(anchor);
        if (cloudAnchor != null)
        {
            Debug.Log($"Cloud anchor created: {cloudAnchor.identifier}");
            return anchor;
        }
        
        return anchor;
    }
    
    void OnAnchorsChanged(ARAnchorsChangedEventArgs args)
    {
        foreach (var anchor in args.added)
        {
            Debug.Log($"Anchor added: {anchor.transform.position}");
        }
    }
}
```

### visionOS Spatial Computing

```swift
// visionOS Spatial Computing
import RealityKit
import ARKit

struct SpatialComputingView: View {
    @State private var anchorManager = SpatialAnchorManager()
    @State private var worldMap: WorldMap?
    
    var body: some View {
        RealityView { content in
            // Start world tracking
            let session = ARKitSession()
            let worldTracking = WorldTrackingProvider()
            await session.run([worldTracking])
            
            // Get world map
            if let map = try? await worldTracking.queryWorldMap() {
                self.worldMap = map
            }
            
            // Create spatial anchor
            let anchor = AnchorEntity(.plane(.horizontal))
            content.add(anchor)
            
            // Add content to anchor
            let model = try! await Entity.load(named: "VirtualObject")
            anchor.addChild(model)
        }
        .gesture(
            SpatialTapGesture()
                .targetedToAnyEntity()
                .onEnded { value in
                    let location = value.location(in: .global)
                    anchorManager.createAnchor(at: location)
                }
        )
    }
}
```

### WebXR Spatial Computing

```javascript
// WebXR Spatial Computing
class SpatialComputingApp {
    async init() {
        // Check spatial features
        const supported = await navigator.xr.isSessionSupported('immersive-ar');
        
        // Request session with spatial features
        this.session = await navigator.xr.requestSession('immersive-ar', {
            requiredFeatures: ['local-floor', 'hit-test', 'plane-detection'],
            optionalFeatures: ['meshing', 'depth-sensing'],
        });
        
        // Setup mesh detection
        this.meshes = [];
        this.session.addEventListener('meshadded', (event) => {
            this.meshes.push(event.mesh);
        });
        
        // Setup plane detection
        this.planes = [];
        this.session.addEventListener('planeschanged', (event) => {
            this.planes = event.planes;
        });
        
        // Spatial anchor creation
        this.anchorStore = new Map();
    }
    
    async createAnchor(position) {
        const anchor = await this.session.requestAnchor(
            this.referenceSpace,
            position
        );
        this.anchorStore.set(anchor.id, anchor);
        return anchor;
    }
    
    async resolveAnchor(anchorId) {
        const anchor = await this.session.resolveAnchor(anchorId);
        return anchor;
    }
}
```

## Performance Optimization

### Anchor Management Optimization

```python
from spatial_computing import AnchorOptimizer, AnchorCache

optimizer = AnchorOptimizer(
    cache=AnchorCache(
        max_size=1000,
        eviction_policy="lru",
        preload_radius_m=50.0,
        preload_count=100,
    ),
    batching={
        "enabled": True,
        "batch_size": 10,
        "batch_interval_ms": 100,
    },
    compression={
        "enabled": True,
        "algorithm": "zstd",
        "level": 3,
    },
)

# Optimize anchor queries
@optimizer.optimize_query
def query_anchors(position, radius):
    # Check cache first
    cached = optimizer.cache.get_nearby(position, radius)
    if len(cached) >= 10:
        return cached
    
    # Query cloud for more
    cloud_anchors = cloud_service.query(position, radius)
    optimizer.cache.put_many(cloud_anchors)
    
    return optimizer.cache.get_nearby(position, radius)

# Monitor performance
stats = optimizer.get_stats()
print(f"Cache hit rate: {stats.cache_hit_rate:.2%}")
print(f"Average query time: {stats.avg_query_time_ms:.2f}ms")
print(f"Cache size: {stats.cache_size}")
```

### World Map Optimization

```python
from spatial_computing import WorldMapOptimizer, LODConfig

optimizer = WorldMapOptimizer(
    lod_config=LODConfig(
        levels=[
            {"distance": 5.0, "resolution": "high", "max_triangles": 100000},
            {"distance": 15.0, "resolution": "medium", "max_triangles": 50000},
            {"distance": 30.0, "resolution": "low", "max_triangles": 10000},
        ],
        transition_mode="dither",
        hysteresis=0.1,
    ),
    streaming={
        "enabled": True,
        "chunk_size": 10000,
        "priority_queue": True,
        "prefetch_distance": 20.0,
    },
    compression={
        "enabled": True,
        "algorithm": "meshopt",
        "target_ratio": 0.5,
    },
)

# Optimize mesh updates
@optimizer.optimize_update
def update_mesh(new_vertices, new_triangles):
    # Apply LOD
    lod_mesh = optimizer.apply_lod(new_vertices, new_triangles)
    
    # Simplify if needed
    if lod_mesh.triangle_count > 50000:
        lod_mesh = optimizer.simplify(lod_mesh, target_ratio=0.5)
    
    # Compress
    compressed = optimizer.compress(lod_mesh)
    
    return compressed

# Monitor performance
stats = optimizer.get_stats()
print(f"Mesh updates per second: {stats.updates_per_second:.1f}")
print(f"Average update time: {stats.avg_update_time_ms:.2f}ms")
print(f"Total mesh size: {stats.total_mesh_size_mb:.2f}MB")
```

## Security Considerations

### Spatial Data Security

```python
from spatial_computing import SpatialSecurity, EncryptionConfig

security = SpatialSecurity(
    encryption=EncryptionConfig(
        algorithm="AES-256-GCM",
        key_rotation_days=30,
        key_derivation="pbkdf2",
        iterations=100000,
    ),
    access_control={
        "read_requires_auth": True,
        "write_requires_auth": True,
        "admin_requires_mfa": True,
        "audit_logging": True,
    },
    data_protection={
        "encrypt_at_rest": True,
        "encrypt_in_transit": True,
        "secure_deletion": True,
        "backup_encryption": True,
    },
)

# Secure anchor storage
encrypted_anchor = security.encrypt(anchor_data)
secure_store.put(encrypted_anchor)

# Secure anchor retrieval
encrypted_data = secure_store.get(anchor_id)
anchor_data = security.decrypt(encrypted_data)

# Audit logging
security.log_access(
    user_id="user123",
    action="read",
    resource=f"anchor:{anchor_id}",
    result="success",
)
```

### Privacy Protection

```python
from spatial_computing import SpatialPrivacy, DataAnonymizer

privacy = SpatialPrivacy(
    data_collection={
        "spatial_data": "session_only",
        "semantic_data": "session_only",
        "analytics": "anonymized",
    },
    anonymization={
        "blur_sensitive_areas": True,
        "remove_personal_info": True,
        "aggregate_data": True,
    },
    compliance={
        "gdpr": True,
        "ccpa": True,
        "hipaa": False,
    },
)

# Anonymize spatial data
anonymized_map = privacy.anonymize(world_map)

# Export anonymized data
export_data = privacy.export(
    data=anonymized_map,
    format="json",
    include_metadata=False,
)
```

## Troubleshooting Guide

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Anchor drift** | Anchors move over time | Recalibrate, check tracking quality |
| **Cloud sync failure** | Anchors don't sync | Check network, verify credentials |
| **Mesh artifacts** | Incorrect geometry | Increase resolution, check sensors |
| **Plane detection slow** | Takes time to find surfaces | Increase update frequency |
| **Memory pressure** | App crashes | Reduce mesh resolution, increase eviction |
| **Query timeout** | Spatial queries fail | Reduce query radius, increase timeout |
| **Semantic errors** | Incorrect labels | Improve lighting, retrain model |
| **Version mismatch** | Data incompatibility | Run migration, check version |

## API Reference

```python
class SpatialAnchorService:
    """Manage spatial anchors."""
    
    def __init__(self, cloud_sync: bool = False):
        """Initialize service."""
        
    def create_anchor(self, position, rotation, name, persistent=True) -> SpatialAnchor:
        """Create spatial anchor."""
        
    def resolve_anchor(self, anchor_id) -> Optional[SpatialAnchor]:
        """Resolve anchor by ID."""
        
    def delete_anchor(self, anchor_id) -> bool:
        """Delete anchor."""
        
    def list_anchors(self, radius=None) -> List[SpatialAnchor]:
        """List anchors."""

class WorldMap:
    """World mapping and reconstruction."""
    
    def __init__(self, resolution="medium", max_depth_m=10.0):
        """Initialize world map."""
        
    def reconstruct(self) -> MeshData:
        """Reconstruct world mesh."""
        
    def query(self, raycast) -> List[RaycastHit]:
        """Perform spatial query."""

class SceneUnderstanding:
    """Scene analysis and semantics."""
    
    def analyze(self) -> SceneAnalysis:
        """Analyze scene."""
        
    def get_elements(self) -> List[SemanticElement]:
        """Get semantic elements."""
```

## Data Models

```python
@dataclass
class SpatialAnchor:
    """Spatial anchor data."""
    anchor_id: str
    position: Vector3
    rotation: Quaternion
    name: str
    persistent: bool
    cloud_anchor_id: Optional[str]
    created_at: datetime
    expires_at: Optional[datetime]
    metadata: dict

@dataclass
class WorldMapData:
    """World map data."""
    mesh: MeshData
    semantic_labels: Dict[str, str]
    bounds: BoundingBox
    resolution: float
    vertex_count: int
    triangle_count: int
    update_time_ms: float

@dataclass
class SceneAnalysis:
    """Scene analysis result."""
    room_type: str
    dimensions: Vector3
    elements: List[SemanticElement]
    scene_graph: SceneGraph
    lighting_condition: str
    noise_level: str
    occupant_count: int

@dataclass
class SpatialQuery:
    """Spatial query result."""
    hit_point: Vector3
    hit_normal: Vector3
    distance: float
    object_label: str
    confidence: float
```

## Deployment Guide

### Build Configuration

```python
from spatial_computing import SpatialBuildConfig

config = SpatialBuildConfig(
    platforms=["quest_3", "vision_pro", "webxr"],
    features=[
        "spatial_anchors",
        "world_mapping",
        "scene_understanding",
        "cloud_sync",
    ],
    optimization={
        "mesh_resolution": "adaptive",
        "anchor_cache_size": 1000,
        "cloud_sync_interval": 30,
    },
    security={
        "encryption": True,
        "authentication": True,
        "audit_logging": True,
    },
)
```

## Monitoring & Observability

```python
from spatial_computing import SpatialMetrics, SpatialHealth

metrics = SpatialMetrics(
    tracks=[
        "anchor_count",
        "mesh_quality",
        "query_latency",
        "cloud_sync_status",
        "semantic_accuracy",
    ],
    sample_rate=0.1,
)

health = SpatialHealth(
    checks=[
        {"name": "tracking_quality", "threshold": 0.8},
        {"name": "mesh_update_rate", "threshold": 8},
        {"name": "cloud_sync_latency", "threshold": 1000},
    ],
)
```

## Testing Strategy

```python
import pytest
from spatial_computing import SpatialAnchorService, WorldMap

class TestSpatialAnchors:
    def test_create_anchor(self):
        service = SpatialAnchorService()
        anchor = service.create_anchor(
            position=(1, 1, 1),
            rotation=(0, 0, 0, 1),
            name="Test",
        )
        assert anchor.anchor_id is not None
    
    def test_resolve_anchor(self):
        service = SpatialAnchorService()
        anchor = service.create_anchor(
            position=(1, 1, 1),
            rotation=(0, 0, 0, 1),
            name="Test",
        )
        resolved = service.resolve_anchor(anchor.anchor_id)
        assert resolved is not None

class TestWorldMap:
    def test_reconstruct(self):
        world_map = WorldMap(resolution="medium")
        mesh = world_map.reconstruct()
        assert mesh.vertex_count > 0
```

## Versioning & Migration

| Version | Changes | Breaking |
|---------|---------|----------|
| 2.0.0 | Added Vision Pro, improved cloud sync | Yes |
| 1.5.0 | Added scene understanding | No |
| 1.0.0 | Initial release | N/A |

## Glossary

| Term | Definition |
|------|------------|
| **Spatial Anchor** | Fixed point in physical space |
| **World Map** | 3D reconstruction of environment |
| **Scene Understanding** | Semantic analysis of space |
| **Cloud Anchor** | Anchor synchronized across devices |
| **Point Cloud** | Set of 3D points from depth sensor |
| **Mesh Reconstruction** | Creating 3D geometry from depth |
| **Semantic Label** | Classification of real-world object |
| **Spatial Query** | Raycast, overlap, or proximity test |

## Changelog

### 2.0.0 (2024-01-15)
- Added Apple Vision Pro support
- Improved cloud sync reliability
- Added scene understanding

### 1.5.0 (2023-10-01)
- Added mesh reconstruction
- Improved anchor persistence

### 1.0.0 (2023-06-01)
- Initial release

## Contributing Guidelines

```bash
git clone https://github.com/company/spatial-computing.git
cd spatial-computing
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

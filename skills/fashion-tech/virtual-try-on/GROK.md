---
name: "virtual-try-on"
category: "fashion-tech"
version: "2.0.0"
tags: ["fashion-tech", "virtual-try-on", "augmented-reality", "computer-vision", "3d-modeling"]
difficulty: "advanced"
estimated_time: "45-60 minutes"
prerequisites: ["basic-python", "computer-vision-fundamentals"]
---

# Virtual Try-On Technology

## Overview

Virtual try-on (VTO) technology enables customers to visualize how clothing, accessories, makeup, and eyewear will look on their body without physically wearing the items. This module provides a comprehensive framework for building VTO systems using computer vision, 3D body modeling, augmented reality, and deep learning. The system handles body segmentation, garment draping simulation, realistic texture mapping, and real-time rendering for web and mobile applications.

Modern VTO solutions combine pose estimation, semantic segmentation, and generative adversarial networks (GANs) to produce photorealistic results. This skill covers the full pipeline from user image capture through 3D body reconstruction, garment fitting simulation, and output generation with proper lighting and shadow effects.

## Core Capabilities

- **Body Pose Estimation**: MediaPipe and OpenPose integration for accurate keypoint detection across 33+ body landmarks
- **Semantic Segmentation**: Person-parsing networks that separate clothing regions, skin, hair, and accessories at pixel level
- **3D Body Reconstruction**: Parametric body model fitting (SMPL, SMPL-X) from single or multiple images for accurate measurements
- **Garment Simulation**: Physics-based cloth draping using mass-spring models or position-based dynamics for realistic fabric behavior
- **Texture Mapping**: UV mapping and perspective-correct texture projection onto body meshes with wrinkle and fold generation
- **Generative Try-On**: GAN-based (CP-VTON, HR-VITON) and diffusion-based approaches for photorealistic garment transfer
- **Real-Time Rendering**: WebGL/Three.js-based rendering pipeline for interactive browser-based try-on experiences
- **Measurement Extraction**: Automatic body measurement extraction from images for size recommendation
- **Multi-Garment Layering**: Support for complete outfit visualization with multiple overlapping garments
- **Lighting Consistency**: Environment-aware relighting to match virtual garments with ambient lighting conditions

## Usage Examples

### Basic Virtual Try-On Pipeline

```python
from fashion_tech.virtual_try_on import VirtualTryOnPipeline, BodyModel, GarmentMesh

# Initialize the VTO pipeline with configuration
pipeline = VirtualTryOnPipeline(
    model_type="hr_viton",
    device="cuda:0",
    resolution=(1024, 768),
    enable_gpu_acceleration=True
)

# Load user image and target garment
user_image = pipeline.load_image("customer_photo.jpg")
garment_image = pipeline.load_garment("red_dress.png", category="dress")

# Step 1: Extract body pose and segmentation
pose keypoints = pipeline.estimate_pose(user_image)
segmentation = pipeline.segment_person(user_image)

# Step 2: Fit 3D body model
body_model = pipeline.fit_body_model(
    image=user_image,
    keypoints=pose_keypoints,
    segmentation=segmentation
)

# Step 3: Simulate garment draping
fitted_garment = pipeline.drape_garment(
    garment=garment_image,
    body_model=body_model,
    fabric_properties={
        "stiffness": 0.3,
        "weight": 0.5,
        "elasticity": 0.1,
        "friction": 0.4
    }
)

# Step 4: Generate final composite
result = pipeline.render(
    body_model=body_model,
    garment=fitted_garment,
    lighting="auto",
    shadow_quality="high",
    output_format="png"
)

result.save("virtual_tryon_result.png")
```

### Body Measurement Extraction

```python
from fashion_tech.virtual_try_on import BodyMeasurementExtractor

extractor = BodyMeasurementExtractor(
    model="smpl_x",
    calibration_known_height=175.0  # cm
)

measurements = extractor.extract(
    image="full_body_photo.jpg",
    reference_object="credit_card"  # Optional scale reference
)

print(f"Bust: {measurements.bust} cm")
print(f"Waist: {measurements.waist} cm")
print(f"Hips: {measurements.hips} cm")
print(f"Inseam: {measurements.inseam} cm")
print(f"Size Recommendation: {measurements.recommend_size('US')}")
```

### Fabric Physics Simulation

```python
from fashion_tech.virtual_try_on import FabricSimulator, FabricType

simulator = FabricSimulator(
    gravity=-9.81,
    time_step=0.016,
    substeps=5
)

# Configure fabric material properties
silk = FabricType(
    name="silk",
    density=0.012,        # kg/m^2
    stretch_resistance=0.8,
    bend_resistance=0.15,
    damping=0.02
)

# Simulate draping on body mesh
draped_mesh = simulator.simulate(
    garment_mesh=garment_vertices,
    body_mesh=body_vertices,
    fabric=silk,
    wind_effect={"direction": [0, 0, -1], "strength": 0.05},
    collision_enabled=True
)
```

### AR Real-Time Try-On

```python
from fashion_tech.virtual_try_on import ARTryOnSession, CameraConfig

# Initialize AR session for mobile/web
session = ARTryOnSession(
    camera=CameraConfig(
        width=1280,
        height=720,
        fps=30,
        facing="user"
    ),
    render_engine="webgl2",
    latency_mode="low"  # Optimized for <50ms frame time
)

# Register garment catalog
session.load_catalog([
    {"id": "dress_001", "path": "dresses/red_summer.png", "category": "dress"},
    {"id": "shirt_042", "path": "shirts/blue_oxford.png", "category": "shirt"},
])

# Start real-time try-on stream
@session.on_frame
def process_frame(frame, body_data):
    if body_data.is_valid:
        fitted = session.fit_garment(
            garment_id="dress_001",
            body=body_data,
            blend_shadows=True
        )
        return session.composite(frame, fitted)
    return frame

session.start()
```

## Architecture

```
User Image Input
      │
      ▼
┌─────────────────┐
│  Pose Estimation │──→ 33+ Keypoints
│  (MediaPipe)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Segmentation    │──→ Person Mask + Clothing Regions
│  (U-Net/DeepLab)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Body Model Fit  │──→ SMPL/SMPL-X Parameters
│  (Optimization)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Garment Drape   │──→ Deformed Garment Mesh
│  (Physics Sim)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Texture Map +   │──→ Final Composite Image
│  Render          │
└─────────────────┘
```

## Best Practices

- Always validate input image quality (lighting, resolution, pose) before processing to avoid poor try-on results
- Use GPU acceleration for real-time applications; CPU fallback should target <2 second per frame
- Implement proper fabric collision detection to prevent garment-body interpenetration artifacts
- Cache fitted body models when the same user tries multiple garments to avoid redundant computation
- Support multiple body types and sizes inclusively; test across diverse body shapes and skin tones
- Handle occlusions gracefully (arms crossed, sitting poses) using inpainting or partial rendering
- Ensure consistent lighting between the original photo and virtual garment overlay
- Version garment asset formats to maintain compatibility across model updates
- Implement quality scoring to detect and reject low-confidence try-on results before display
- Monitor latency metrics (pose estimation, segmentation, rendering) to maintain interactive frame rates

## Related Modules

- `fashion-tech/trend-prediction` - Trend analysis to suggest popular garments for try-on
- `fashion-tech/supply-chain` - Inventory integration for try-on-to-purchase flow
- `fashion-tech/retail-analytics` - Analytics on try-on engagement and conversion
- `fashion-tech/sustainable-fashion` - Digital sampling to reduce physical sample waste

---

## Advanced Configuration

### Body Model Settings

```python
from virtual_tryon import BodyModelConfig

body_config = BodyModelConfig(
    # Body Estimation
    estimation={
        "model": "smpl",  # smpl, smplx, bsm
        "num_vertices": 6890,
        "shape_parameters": 10,
        "pose_parameters": 72,
    },
    
    # Segmentation
    segmentation={
        "model": "deeplabv3",
        "num_classes": 20,
        "confidence_threshold": 0.85,
    },
    
    # Pose Estimation
    pose={
        "model": "mediapipe",
        "num_keypoints": 33,
        "min_detection_confidence": 0.7,
    },
)
```

### Garment Simulation Settings

```python
from virtual_tryon import GarmentConfig

garment_config = GarmentConfig(
    # Physics Simulation
    physics={
        "engine": "physx",  # physx, bullet, custom
        "cloth_model": "mass_spring",
        "iterations": 10,
        "time_step": 0.016,
    },
    
    # Rendering
    rendering={
        "engine": "nerf",  # nerf, gaussian_splatting, rasterization
        "resolution": (1024, 1024),
        "lighting": "hdr",
        "shadows": True,
    },
    
    # Texture Mapping
    texture={
        "uv_mapping": "automatic",
        "normal_mapping": True,
        "displacement_mapping": False,
    },
)
```

## Architecture Patterns

### VTO Pipeline Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Input Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ User     │  │Garment   │  │ Camera   │         │
│  │ Photo    │  │ Assets   │  │ Feed     │         │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘         │
└───────┼──────────────┼──────────────┼───────────────┘
        │              │              │
        ▼              ▼              ▼
┌─────────────────────────────────────────────────────┐
│              Processing Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Body     │──│ Garment  │──│ Rendering│         │
│  │ Estimation│ │ Fitting  │  │ Engine   │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│                Output Layer                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Try-On   │  │ AR View  │  │ 3D Model │         │
│  │ Image    │  │          │  │          │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────┘
```

### Garment Fitting Algorithm

```python
from virtual_tryon import GarmentFitter

fitter = GarmentFitter()

# Fit garment to body
result = fitter.fit(
    body_model=body_model,
    garment_mesh=garment_mesh,
    method="physics_based",  # physics_based, learning_based, hybrid
    constraints={
        "collision_detection": True,
        "gravity": True,
        "wind": False,
    },
)

print(f"Fitting completed: {result.success}")
print(f"Collision score: {result.collision_score:.2f}")
print(f"Draping quality: {result.draping_quality:.2f}")
```

## Integration Guide

### AR SDK Integration

```python
from virtual_tryon import ARIntegration

ar = ARIntegration()

# Configure AR
ar.configure(
    sdk="arkit",  # arkit, arcore, webxr
    tracking_mode="face",  # face, body, world
    lighting_estimation=True,
)

# Start AR session
session = ar.start_session(
    camera_feed=camera_stream,
    garment_id="garment-123",
)

# Get AR frame
frame = session.get_frame()
print(f"Tracking: {frame.tracking_status}")
print(f"Garment visible: {frame.garment_visible}")
```

### E-commerce Integration

```python
from virtual_tryon import EcommerceIntegration

ecom = EcommerceIntegration()

# Configure e-commerce
ecom.configure(
    platform="shopify",
    store_url="https://store.example.com",
)

# Add try-on button
ecom.add_try_on_button(
    product_id="product-123",
    try_on_url="https://vto.example.com/try",
)

# Track conversion
conversion = ecom.track_conversion(
    session_id="vto-session-456",
    product_id="product-123",
    converted=True,
    order_value=89.99,
)

print(f"Conversion tracked: {conversion.id}")
```

## Performance Optimization

### Latency Optimization

```python
from virtual_tryon import LatencyOptimizer

optimizer = LatencyOptimizer()

# Optimize for real-time
result = optimizer.optimize(
    pipeline="full_vto",
    target_fps=30,
    strategies=[
        "model_quantization",
        "parallel_processing",
        "frame_interpolation",
    ],
)

print(f"Original latency: {result.original_ms:.1f}ms")
print(f"Optimized latency: {result.optimized_ms:.1f}ms")
print(f"FPS achieved: {result.fps:.1f}")
```

### Quality Optimization

```python
from virtual_tryon import QualityOptimizer

quality_opt = QualityOptimizer()

# Optimize visual quality
result = quality_opt.optimize(
    image=output_image,
    strategies=[
        "super_resolution",
        "color_correction",
        "shadow_enhancement",
    ],
)

print(f"Quality score: {result.quality_score:.2f}")
print(f"SSIM improvement: {result.ssim_improvement:.1%}")
```

## Security Considerations

### Privacy Protection

```python
from virtual_tryon import PrivacyManager

privacy = PrivacyManager()

# Process images locally
privacy.configure(
    processing_mode="on_device",  # on_device, cloud, hybrid
    data_retention="none",
    anonymize=True,
)

# Delete user data
privacy.delete_user_data(
    user_id="user-123",
    images=True,
    body_models=True,
    session_data=True,
)
```

### Content Protection

```python
from virtual_tryon import ContentProtection

protection = ContentProtection()

# Protect garment assets
protected = protection.protect(
    garment_id="garment-123",
    watermark=True,
    drm=True,
    access_token="token-456",
)
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Poor fit | Bad body estimation | Improve lighting, pose |
| Garment clipping | Weak collision detection | Increase physics iterations |
| Slow rendering | High resolution | Reduce resolution, use GPU |
| Inconsistent lighting | Different environments | Use HDR lighting estimation |
| Artifacts | Occlusions | Use inpainting, multiple views |

### Debug Mode

```python
from virtual_tryon import enable_debug

enable_debug(
    components=["body_estimation", "garment_fitting", "rendering"],
    log_level="DEBUG",
    visualize_intermediate=True,
)

# Debug try-on
debug_session = debug.trace_tryon(
    user_image="user.jpg",
    garment_id="garment-123",
)
print(f"Debug visualization: {debug_session.visualization_url}")
```

## API Reference

### REST Endpoints

```
POST   /api/v1/vto/try-on                   Try on garment
POST   /api/v1/vto/body/estimate            Estimate body model
GET    /api/v1/vto/garments                 List garments
POST   /api/v1/vto/garments/upload          Upload garment
GET    /api/v1/vto/sessions/{id}            Get session
GET    /api/v1/vto/sessions/{id}/result     Get try-on result
```

### Data Models

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID

@dataclass
class BodyModel:
    model_id: UUID
    vertices: List[List[float]]
    shape_params: List[float]
    pose_params: List[float]
    created_at: datetime

@dataclass
class GarmentAsset:
    garment_id: UUID
    name: str
    mesh_url: str
    texture_url: str
    category: str
    sizes: List[str]

@dataclass
class TryOnResult:
    result_id: UUID
    session_id: UUID
    user_image: str
    garment_id: UUID
    output_image: str
    quality_score: float
    latency_ms: float
    created_at: datetime
```

## Deployment Guide

### GPU Server Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vto-engine
spec:
  replicas: 2
  selector:
    matchLabels:
      app: vto-engine
  template:
    spec:
      containers:
      - name: engine
        image: vto-engine:latest
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
            nvidia.com/gpu: 1
          limits:
            memory: "8Gi"
            cpu: "4000m"
            nvidia.com/gpu: 1
```

## Monitoring & Observability

### Key Metrics

```python
from virtual_tryon import Metrics

metrics = Metrics()

# Track VTO performance
metrics.histogram("vto.latency_ms", latency, tags={"stage": "rendering"})
metrics.counter("vto.try_ons_total", tags={"status": "success"})

# Track quality
metrics.gauge("vto.quality_score", score, tags={"garment_type": "dress"})
metrics.gauge("vto.conversion_rate", rate, tags={"product_category": "apparel"})
```

## Testing Strategy

### Unit Tests

```python
import pytest
from virtual_tryon import GarmentFitter

@pytest.fixture
def fitter():
    return GarmentFitter(test_mode=True)

def test_fit_garment(fitter):
    result = fitter.fit(
        body_model=test_body_model,
        garment_mesh=test_garment_mesh,
    )
    assert result.success
    assert result.collision_score > 0.5
```

## Versioning & Migration

### Version History

- **2.0.0**: Added NeRF rendering, real-time AR, advanced physics simulation
- **1.5.0**: Added body estimation, garment fitting, basic rendering
- **1.0.0**: Initial release with simple overlay

## Glossary

| Term | Definition |
|------|------------|
| **SMPL** | Skinned Multi-Person Linear model |
| **NeRF** | Neural Radiance Field |
| **GAN** | Generative Adversarial Network |
| **Mesh** | 3D surface representation |
| **UV Mapping** | 2D texture to 3D surface mapping |
| **Physics-Based** | Simulation using cloth dynamics |

## Changelog

### Version 2.0.0
- NeRF-based rendering
- Real-time AR support
- Advanced physics simulation
- Improved body estimation

### Version 1.5.0
- SMPL body model integration
- Basic garment fitting
- Web-based try-on

### Version 1.0.0
- Initial release
- Simple overlay
- Basic segmentation

## Contributing Guidelines

1. Test on diverse body types
2. Validate rendering quality
3. Benchmark latency on target hardware
4. Document garment asset requirements

## Quality Assessment

### Try-On Quality Scoring

```python
from virtual_tryon import QualityScorer

scorer = QualityScorer()

# Score try-on result quality
quality = scorer.score(
    result_image="tryon_result.png",
    original_image="user_photo.jpg",
    garment_image="dress.png",
)

print(f"Quality Score: {quality.overall:.2f}/1.0")
print(f"  Fit Accuracy: {quality.fit_score:.2f}")
print(f"  Lighting Consistency: {quality.lighting_score:.2f}")
print(f"  Shadow Quality: {quality.shadow_score:.2f}")
print(f"  Texture Realism: {quality.texture_score:.2f}")
```

## Virtual Try-On Deep Dive

### Garment Physics Simulation

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple

@dataclass
class ClothVertex:
    position: np.ndarray
    velocity: np.ndarray
    mass: float
    pinned: bool = False
    
@dataclass
class ClothSpring:
    v1: int
    v2: int
    rest_length: float
    stiffness: float

class ClothSimulator:
    def __init__(self, resolution: int = 20):
        self.resolution = resolution
        self.vertices: List[ClothVertex] = []
        self.springs: List[ClothSpring] = []
        self.gravity = np.array([0, -9.81, 0])
        self.damping = 0.98
        self.time_step = 0.016
    
    def create_mesh(self, width: float, height: float, fabric_type: str = "cotton"):
        fabric_props = {
            "cotton": {"stiffness": 150, "mass": 0.002, "damping": 0.97},
            "silk": {"stiffness": 80, "mass": 0.001, "damping": 0.99},
            "denim": {"stiffness": 300, "mass": 0.004, "damping": 0.95},
            "knit": {"stiffness": 100, "mass": 0.002, "damping": 0.98},
            "leather": {"stiffness": 400, "mass": 0.005, "damping": 0.93},
        }
        props = fabric_props.get(fabric_type, fabric_props["cotton"])
        
        self.vertices = []
        self.springs = []
        
        for j in range(self.resolution + 1):
            for i in range(self.resolution + 1):
                x = (i / self.resolution) * width - width / 2
                y = (j / self.resolution) * height
                z = 0
                pinned = j == 0 and (i % 3 == 0)  # pin top row
                vertex = ClothVertex(
                    position=np.array([x, y, z]),
                    velocity=np.array([0, 0, 0]),
                    mass=props["mass"],
                    pinned=pinned,
                )
                self.vertices.append(vertex)
        
        # Structural springs
        for j in range(self.resolution + 1):
            for i in range(self.resolution):
                idx = j * (self.resolution + 1) + i
                self.springs.append(ClothSpring(idx, idx + 1, width / self.resolution, props["stiffness"]))
        
        # Shear springs
        for j in range(self.resolution):
            for i in range(self.resolution):
                idx = j * (self.resolution + 1) + i
                diag_len = np.sqrt((width / self.resolution) ** 2 + (height / self.resolution) ** 2)
                self.springs.append(ClothSpring(idx, idx + self.resolution + 2, diag_len, props["stiffness"] * 0.5))
                self.springs.append(ClothSpring(idx + 1, idx + self.resolution + 1, diag_len, props["stiffness"] * 0.5))
        
        self.damping = props["damping"]
    
    def step(self, wind: np.ndarray = None):
        forces = [np.copy(self.gravity) * v.mass for v in self.vertices]
        
        if wind is not None:
            for i, v in enumerate(self.vertices):
                if not v.pinned:
                    forces[i] += wind * 0.01
        
        for spring in self.springs:
            v1, v2 = self.vertices[spring.v1], self.vertices[spring.v2]
            delta = v2.position - v1.position
            distance = np.linalg.norm(delta)
            if distance > 0:
                direction = delta / distance
                stretch = distance - spring.rest_length
                force = spring.stiffness * stretch * direction
                forces[spring.v1] += force
                forces[spring.v2] -= force
        
        for i, vertex in enumerate(self.vertices):
            if vertex.pinned:
                continue
            acceleration = forces[i] / vertex.mass
            vertex.velocity = (vertex.velocity + acceleration * self.time_step) * self.damping
            vertex.position = vertex.position + vertex.velocity * self.time_step
    
    def simulate(self, frames: int = 60, wind: np.ndarray = None) -> List[np.ndarray]:
        positions_over_time = []
        for _ in range(frames):
            self.step(wind)
            positions_over_time.append(np.array([v.position.copy() for v in self.vertices]))
        return positions_over_time
    
    def drape_on_body(self, body_contour: List[np.ndarray], iterations: int = 100):
        for _ in range(iterations):
            self.step()
            for i, vertex in enumerate(self.vertices):
                if vertex.pinned:
                    continue
                for body_point in body_contour:
                    diff = vertex.position - body_point
                    dist = np.linalg.norm(diff)
                    if dist < 0.02:  # collision threshold
                        vertex.position = body_point + diff / dist * 0.02
    
    def get_drape_quality(self) -> Dict:
        positions = np.array([v.position for v in self.vertices])
        heights = positions[:, 1]
        spread = positions[:, 0].max() - positions[:, 0].min()
        max_drape = heights.max() - heights.min()
        smoothness = np.mean(np.abs(np.diff(heights)))
        
        return {
            "spread": round(float(spread), 3),
            "max_drape_depth": round(float(max_drape), 3),
            "smoothness_score": round(1.0 / (1.0 + float(smoothness)), 3),
            "vertex_count": len(self.vertices),
            "spring_count": len(self.springs),
        }

class FabricPropertyDatabase:
    def __init__(self):
        self.fabrics = {
            "cotton_poplin": {"weight_gsm": 110, "stretch_pct": 3, "drape_coeff": 0.45, "opacity": 0.95},
            "silk_charmeuse": {"weight_gsm": 80, "stretch_pct": 15, "drape_coeff": 0.85, "opacity": 0.7},
            "denim_12oz": {"weight_gsm": 400, "stretch_pct": 2, "drape_coeff": 0.2, "opacity": 1.0},
            "jersey_knit": {"weight_gsm": 180, "stretch_pct": 50, "drape_coeff": 0.7, "opacity": 0.85},
            "tulle": {"weight_gsm": 20, "stretch_pct": 5, "drape_coeff": 0.95, "opacity": 0.3},
            "wool_crepe": {"weight_gsm": 220, "stretch_pct": 8, "drape_coeff": 0.55, "opacity": 0.98},
            "chiffon": {"weight_gsm": 40, "stretch_pct": 5, "drape_coeff": 0.9, "opacity": 0.4},
            "velvet": {"weight_gsm": 280, "stretch_pct": 5, "drape_coeff": 0.4, "opacity": 1.0},
        }
    
    def get_fabric(self, name: str) -> Dict:
        return self.fabrics.get(name, self.fabrics["cotton_poplin"])
    
    def recommend_fabric(self, garment_type: str, season: str) -> List[str]:
        recommendations = {
            "dress": {
                "summer": ["cotton_poplin", "chiffon", "silk_charmeuse"],
                "winter": ["wool_crepe", "velvet", "jersey_knit"],
            },
            "shirt": {
                "summer": ["cotton_poplin", "chiffon"],
                "winter": ["wool_crepe", "jersey_knit"],
            },
            "pants": {
                "summer": ["cotton_poplin", "jersey_knit"],
                "winter": ["denim_12oz", "wool_crepe"],
            },
        }
        return recommendations.get(garment_type, {}).get(season, ["cotton_poplin"])

class SizeMappingEngine:
    def __init__(self):
        self.brand_size_charts: Dict[str, Dict[str, Dict]] = {}
    
    def add_brand_chart(self, brand: str, chart: Dict[str, Dict]):
        self.brand_size_charts[brand] = chart
    
    def find_best_size(self, brand: str, body_measurements: Dict) -> Dict:
        chart = self.brand_size_charts.get(brand, {})
        if not chart:
            return {"size": "M", "confidence": 0.3}
        
        best_size = None
        best_score = float('inf')
        
        for size_name, size_data in chart.items():
            fit_score = sum(
                abs(body_measurements.get(dim, 0) - size_data.get(dim, 0))
                for dim in ["chest", "waist", "hips", "inseam"]
                if dim in body_measurements and dim in size_data
            )
            if fit_score < best_score:
                best_score = fit_score
                best_size = size_name
        
        confidence = max(0.3, 1.0 - best_score / 100)
        
        return {
            "brand": brand,
            "recommended_size": best_size,
            "fit_score": round(best_score, 2),
            "confidence": round(confidence, 3),
            "note": "Based on body measurements only - style preference may vary",
        }
    
    def cross_brand_equivalent(self, source_brand: str, source_size: str, 
                               target_brand: str) -> Dict:
        source_chart = self.brand_size_charts.get(source_brand, {})
        target_chart = self.brand_size_charts.get(target_brand, {})
        
        if not source_chart or not target_chart:
            return {"equivalent_size": "M", "confidence": 0.2}
        
        source_measurements = source_chart.get(source_size, {})
        if not source_measurements:
            return {"equivalent_size": "M", "confidence": 0.2}
        
        best_target = None
        best_diff = float('inf')
        
        for size_name, size_data in target_chart.items():
            diff = sum(abs(source_measurements.get(d, 0) - size_data.get(d, 0))
                      for d in ["chest", "waist", "hips"])
            if diff < best_diff:
                best_diff = diff
                best_target = size_name
        
        return {
            "source": f"{source_brand} {source_size}",
            "equivalent_size": best_target,
            "target_brand": target_brand,
            "confidence": max(0.3, 1.0 - best_diff / 50),
        }
```

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills

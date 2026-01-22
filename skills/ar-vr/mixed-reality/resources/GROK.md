# Mixed Reality Development

Specialized skill for building immersive mixed reality applications that seamlessly blend digital content with the physical world. Covers reality-to-virtuality spectrum, spatial anchors, passthrough rendering, occlusion, and cross-platform MR development.

## Core Capabilities

### Reality-Virtuality Spectrum
- Virtual Reality (VR) experiences
- Augmented Reality (AR) overlays
- Mixed Reality (MR) spatial interactions
- Immersive passthrough systems
- Reality blending and transitions

### Cross-Platform Development
- Microsoft HoloLens 2 development
- Magic Leap 2 development
- Meta Quest 3 development
- Apple Vision Pro development
- Varjo XR development

### Spatial Content Creation
- 3D model rendering and animation
- Spatial UI elements
- Particle systems and effects
- Text and annotation placement
- Video and media integration

### Spatial Anchoring
- World-space anchors
- Surface anchors
- Tracked object anchors
- Anchor persistence
- Multi-device anchor sharing

### Advanced Rendering
- Real-time passthrough
- Depth-based occlusions
- Lighting estimation
- Shadow casting
- Environment probes

### Interaction Systems
- Hand tracking and gestures
- Eye tracking and gaze
- Voice commands
- Controller input
- Haptic feedback

## Usage Examples

### Engine Setup
```python
from mixed_reality import (
    MixedRealityEngine, MRDevice, MRContent, ContentType
)

mr = MixedRealityEngine(device=MRDevice.HOLOLENS)

status = mr.get_engine_status()
print(f"Device: {status['device']}")
print(f"Content: {status['content_count']}")
```

### Content Creation
```python
hologram = mr.create_hologram("model-001")
ui = mr.create_ui_element("info-panel", ui_type="panel")

mr.place_content(
    "model-001",
    position=(0, 1.5, -2.0),
    rotation=(0, 45, 0),
    scale=0.8
)

mr.add_particle_effect("sparkles", position=(0, 1.6, -2.0))
```

### Spatial Anchoring
```python
anchor_id = mr.create_spatial_anchor(position=(1.0, 1.2, -1.5))
mr.attach_to_anchor("model-001", anchor_id, offset=(0, 0.3, 0))

spatial_info = mr.get_spatial_info()
print(f"Anchors: {spatial_info['anchors']}")
```

### Passthrough Configuration
```python
from mixed_reality import PassThroughConfig

config = PassThroughConfig(
    environment_mask=True,
    depth_lighting=True,
    occlusions=True,
    brightness=1.0
)
mr.configure_passthrough(config)

mr.update_passthrough(enabled=True, opacity=0.85)
```

### Hand Tracking
```python
from mixed_reality import HandTrackingManager

hand_manager = HandTrackingManager()
hands = hand_manager.get_hand_data()

manipulation = hand_manager.detect_manipulation(
    hands,
    target_position=(0, 1.5, -2.0)
)
print(f"Manipulating: {manipulation['is_manipulating']}")
```

### Reality Transitions
```python
from mixed_reality import RealityTransitionManager, RealityType

transition = RealityTransitionManager()
transition.transition_to(RealityType.VIRTUAL, duration=2.0)

blend = transition.blend_realities(real_reality=0.3, virtual_reality=0.7)
print(f"Reality blend: {blend['resulting_reality']}")
```

### Animation and Rendering
```python
mr.play_animation("model-001", "rotate", duration=1.5)

frame = mr.render_frame()
print(f"FPS: {frame['stats']['fps']}")
print(f"Draw calls: {frame['stats']['draw_calls']}")

occlusion = mr.get_content_occlusion("model-001")
print(f"Visibility: {occlusion['visibility']:.2%}")
```

## Best Practices

1. **Performance**: Target consistent 60 FPS for comfort
2. **Stability**: Use stable world anchors for persistent content
3. **Occlusion**: Implement proper depth-based occlusion
4. **Comfort**: Avoid rapid camera movements and flicker
5. **Accessibility**: Support multiple input modalities
6. **Testing**: Test on actual MR devices
7. **Optimization**: Use level-of-detail (LOD) for content
8. **Power**: Consider battery constraints on standalone devices

## Related Skills

- [Spatial Computing](spatial-computing): Spatial awareness
- [Computer Vision](computer-vision): Environment understanding
- [3D Graphics](web-dev/3d-graphics): Rendering fundamentals
- [User Research](ux-research/user-research): User testing

## Use Cases

- Industrial maintenance instructions
- Medical visualization and training
- Architecture and design review
- Remote collaboration and assistance
- Education and training simulations
- Gaming and interactive experiences
- Retail product visualization
- Design prototyping and iteration

# AR/VR Development Agent

## Overview

The **AR/VR Development Agent** provides comprehensive augmented and virtual reality development capabilities including Unity XR, WebXR, ARKit/ARCore integration, and spatial computing. This agent enables building immersive experiences across multiple platforms.

## Core Capabilities

### 1. Unity XR Development
Build VR/AR experiences with Unity:
- **XR Interaction Toolkit**: Controller and hand input
- **VR Player Setup**: Locomotion, teleportation
- **AR Passthrough**: Mixed reality features
- **Spatial Anchors**: Persistent AR placement
- **Performance Optimization**: Frame rate targets

### 2. WebXR Development
Create browser-based XR experiences:
- **Three.js Integration**: 3D rendering
- **WebXR API**: Device access
- **Hand Tracking**: WebXR input sources
- **Performance Optimization**: Asset optimization
- **Cross-Platform**: Mobile and desktop support

### 3. AR Development
Build mobile AR experiences:
- **ARKit Integration**: iOS AR features
- **ARCore Integration**: Android AR features
- **Image Tracking**: Marker-based AR
- **Plane Detection**: Surface detection
- **Occlusion**: Real-world occlusion

### 4. VR Development
Create immersive VR environments:
- **Environment Design**: 3D scene creation
- **Controller Input**: Hand tracking, controllers
- **Locomotion**: Teleport, smooth movement
- **Avatar Integration**: Full-body tracking
- **Interaction Design**: Grab, teleport, UI

### 5. Spatial Audio
Add 3D positional audio:
- **HRTF**: Head-related transfer functions
- **Distance Attenuation**: Realistic falloff
- **Room Acoustics**: Environmental effects
- **Sound Zones**: Spatial regions

## Usage Examples

### Unity XR Setup

```python
from ar_vr import UnityXRManager

unity = UnityXRManager()
project = unity.create_xr_project(XRPlatform.META_QUEST)
player = unity.setup_vr_player(locomotion='teleport', hands=True)
passthrough = unity.configure_passthrough(mode='additive')
anchor = unity.create_spatial_anchor(XRVector3(1, 0, 0))
physics = unity.setup_physics()
```

### WebXR

```python
from ar_vr import WebXRManager

webxr = WebXRManager()
support = webxr.detect_xr_support()
session = webxr.create_xr_session('immersive-vr', 'local-floor')
threejs = webxr.setup_threejs_scene()
hand_tracking = webxr.implement_hand_tracking()
optimization = webxr.optimize_for_web()
```

### AR Development

```python
from ar_vr import ARDevelopment

ar = ARDevelopment()
arkit = ar.setup_arkit(['reference_img_1'])
arcore = ar.setup_arcore(['face_tracking'])
placement = ar.place_object_ar(
    XRVector3(1, 0, 0),
    XRVector3(0, 0, 0),
    scale=1.0
)
image_target = ar.create_image_target('marker.png', 'product_marker')
occlusion = ar.implement_occlusion('depth')
raycast = ar.raycast_ar({'x': 0.5, 'y': 0.5}, XRVector3(0, 0, 0))
```

### VR Development

```python
from ar_vr import VRDevelopment

vr = VRDevelopment()
environment = vr.create_vr_environment('indoor')
controllers = vr.setup_controller_input()
locomotion = vr.create_locomotion(['teleport', 'smooth', 'dash'])
avatar = vr.setup_avatar(rig_type='full_body', hands=True)
interaction = vr.implement_interaction('grab_and_place')
performance = vr.optimize_vr_performance()
```

### Spatial Audio

```python
from ar_vr import SpatialAudio

audio = SpatialAudio()
config = audio.configure_spatial_audio(engine='oculus_spatializer')
attached = audio.attach_sound_to_object('sound_1', XRTransform(
    XRVector3(0, 0, 0),
    XRVector3(0, 0, 0)
))
sound_zone = audio.create_3d_sound_zone(XRVector3(0, 0, 0), radius=5.0)
acoustics = audio.configure_room_acoustics(
    XRVector3(10, 5, 10),
    {'floor': 'hard', 'walls': 'soft'}
)
```

## XR Platforms

### VR Headsets
| Platform | Developer | Tracking | Controllers |
|----------|-----------|----------|-------------|
| Meta Quest | Meta | Inside-out | Hand + Controller |
| Valve Index | Valve | Lighthouse | Index controllers |
| HTC Vive | HTC | Lighthouse | Wand controllers |
| Apple Vision | Apple | Inside-out | Hand + Eye |

### AR Platforms
| Platform | Device | Features |
|----------|--------|----------|
| ARKit | iOS | Plane detection, face tracking |
| ARCore | Android | Plane detection, cloud anchors |
| HoloLens | Windows | Spatial mapping, gestures |

## XR Development Tools

### Game Engines
- **Unity**: Most popular XR engine
- **Unreal Engine**: High-fidelity graphics
- **Godot**: Open source option

### Web Frameworks
- **Three.js**: 3D on web
- **A-Frame**: WebVR framework
- **Babylon.js**: Microsoft 3D engine

### Design Tools
- **Blender**: 3D modeling
- **Maya**: Character animation
- **Figma**: UI/UX design

## XR Interaction Design

### Input Methods
- **Controllers**: Physical input devices
- **Hand Tracking**: Natural hand gestures
- **Eye Gaze**: Gaze-based selection
- **Voice Commands**: Speech recognition

### Interaction Types
- **Grab**: Pick up and move objects
- **Teleport**: Instant movement
- **Point**: Select distant objects
- **Swipe**: Gesture-based interaction
- **UI Interaction**: Button pressing, sliders

## Performance Optimization

### VR Performance Targets
| Metric | Target | Impact |
|--------|--------|--------|
| Frame Rate | 90 FPS | Smooth experience |
| Latency | <20ms | Reduce motion sickness |
| Resolution | Per-eye rendering | Visual quality |

### Optimization Techniques
- **Draw Call Batching**: Reduce API calls
- **Level of Detail (LOD)**: Distance-based detail
- **Occlusion Culling**: Hide invisible objects
- **Texture Compression**: Reduce memory
- **Baked Lighting**: Pre-compute lighting

## Use Cases

### 1. Training & Simulation
- Medical training
- Military simulation
- Equipment operation
- Safety procedures

### 2. Design & Visualization
- Architectural walkthrough
- Product visualization
- Interior design
- Engineering models

### 3. Entertainment
- VR games
- Interactive experiences
- Virtual concerts
- Social VR spaces

### 4. Remote Collaboration
- Virtual meetings
- 3D collaboration
- Remote assistance
- Training sessions

## Accessibility in XR

### Considerations
- **Motion Sickness**: Reduce artificial movement
- **Physical Accessibility**: Alternative controls
- **Visual Accessibility**: High contrast modes
- **Auditory Accessibility**: Visual feedback

### Design Guidelines
- Provide comfort options
- Support multiple input methods
- Allow customization
- Test with diverse users

## Related Skills

- [Game Development](../gaming/game-design/README.md) - Game mechanics
- [3D Graphics](../graphics/3d-rendering/README.md) - 3D rendering
- [Voice Technology](../voice-technology/speech-processing/README.md) - Voice in XR

---

**File Path**: `skills/ar-vr/ar-vr-development/resources/ar_vr.py`

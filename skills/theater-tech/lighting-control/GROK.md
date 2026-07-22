---
name: "lighting-control"
category: "theater-tech"
version: "1.0.0"
tags: ["theater-tech", "lighting-control", "dmx", "art-net", "show-control"]
---

# Lighting Control System

## Overview

The lighting control module provides a comprehensive Python API for managing theatrical and entertainment lighting systems. It implements the DMX512 protocol with native Art-Net and sACN (E1.31) networking, allowing programmatic control of conventional dimmers, moving lights, LED fixtures, media servers, and LED video walls from a single unified interface. The module is designed for both live show operation and offline previsualization, enabling lighting designers to program, test, and automate entire lighting plots without requiring physical hardware.

At its core, the module treats the lighting rig as a state machine: each DMX universe maintains a 512-channel frame, and changes propagate through a pipeline of merge operations, effect generators, cue cross-fades, and priority layers. This layering model mirrors professional lighting consoles (GrandMA, ETC Eos, ChamSys) and allows complex looks to be built compositionally — a base wash from one cue, a specials layer from another, and a real-time effect overlaid on top. The cross-fade engine supports both LTP (Latest Takes Precedence) and HTP (Highest Takes Precedence) merge modes per channel, which is essential for correct behavior when mixing color (LTP) with intensity (HTP) data.

Color science is a first-class concern: the module includes CIE 1931 color space conversion, gamut mapping for RGBW/RGBAW fixture profiles, and Lee/Rosco gel preset libraries. Color mixing algorithms account for the specific emitter wavelengths of different LED fixture families, preventing the washed-out purples and inaccurate ambers that plague naive RGB mixing. The fixture library ships with profiles for over 200 common fixtures from major manufacturers, and custom profiles can be defined via a straightforward JSON schema.

Show file management follows industry conventions: cues are numbered with decimal sub-stages (1, 1.1, 1.2, 2, etc.), each cue stores a complete DMX snapshot or a delta from the previous cue, and cue timing includes fade times, delay times, and follow times. The module can import and export ETC Eos show files, GrandMA2 show files, and a vendor-neutral JSON format, making it a useful bridge tool for venues transitioning between console platforms.

## Core Capabilities

- Full DMX512 protocol implementation with 512-channel universes and 44Hz refresh rate control
- Art-Net (ArtNet4) and sACN/ACN (E1.31) network output with multicast support
- Moving light fixture control with pan/tilt, color, gobo, beam, and effect parameters
- CIE 1931 color space conversion with gamut mapping for RGBW/RGBAW/CMY fixture profiles
- LED wall and media server integration via DMX parameter control and NDI/SDI output triggers
- Cue list programming with HTP/LTP merge, cross-fade timing, tracking, and bump cues
- Effect generator with oscillators (sine, triangle, sawtooth), random, and step-based patterns
- Show file import/export for ETC Eos, GrandMA2, and vendor-neutral JSON formats

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Cue List & Effect Engine                    │
│   (Cross-fade, Tracking, LTP/HTP Merge, Effects)        │
├─────────────────────────────────────────────────────────┤
│                 Fixture Abstraction Layer                │
│      (Profiles, Parameters, Color Spaces, DMX Map)      │
├─────────────────────────────────────────────────────────┤
│                  DMX Universe Manager                    │
│     (512-Channel Frame, Merge Buffers, Snapshots)        │
├─────────────────────────────────────────────────────────┤
│                 Network Output Layer                     │
│        (Art-Net, sACN, DMX512 Serial, Pathway)          │
└─────────────────────────────────────────────────────────┘
```

## Usage Examples

### Basic DMX Control and Fixture Patching

```python
from lighting_control import DMXUniverse, ArtNetNode, Fixture, ColorMix

# Create a DMX universe and Art-Net output node
universe = DMXUniverse(universe_id=0)
artnet = ArtNetNode(ip="2.0.0.1", subnet=0, universe=0)
artnet.start()

# Patch a Source Four LED Series 3 at address 101
s4 = Fixture(
    name="Main Wash 1",
    profile="etc_sourcefour_led_s3",
    dmx_address=101,
)
universe.patch(s4)

# Set a warm amber wash at 70% intensity
s4.set_intensity(0.70)
s4.set_color(ColorMix.from_hex("#FFB347"))
frame = universe.output(artnet)
```

### Color Mixing and CIE Conversion

```python
from lighting_control import ColorMix

# Create colors from different sources
amber = ColorMix.from_hex("#FFB347")
print(f"Amber: R={amber.r:.2f} G={amber.g:.2f} B={amber.b:.2f}")

# CIE 1931 D65 white point
d65_white = ColorMix.from_cie(0.3127, 0.3290)
print(f"D65 White: {d65_white.to_hex()}")

# Color space conversions
rgbw = amber.to_rgbw()
cmy = amber.to_cmy()
print(f"RGBW: {rgbw}, CMY: {cmy}")

# Color interpolation for cross-fades
warm = ColorMix.from_hex("#FFB347")
cool = ColorMix.from_hex("#4488FF")
midpoint = warm.lerp(cool, 0.5)
print(f"50% cross-fade: {midpoint.to_hex()}")
```

### Cue List and Effects

```python
from lighting_control import CueList, CrossFadeEngine, EffectGenerator, Waveform

# Build a cue list for Act 2
cues = CueList(name="Act 2")
cues.add_cue(
    number=1,
    look={"wash_1": {"intensity": 0.8, "color": "#FFF5E1"}, "spot_1": {"intensity": 0.0}},
    fade_time_s=3.0,
)
cues.add_cue(
    number=2,
    look={"wash_1": {"intensity": 0.4, "color": "#4488FF"}, "spot_1": {"intensity": 1.0, "gobo": "breakup"}},
    fade_time_s=5.0,
    follow_time_s=8.0,
)
cues.add_cue(number=2.5, look={"spot_1": {"gobo": "breakup_slow"}}, fade_time_s=2.0)
cues.add_cue(number=3, look={"all": {"intensity": 0.0}}, fade_time_s=0.5)
print(f"Cue list '{cues.name}' has {len(cues)} cues")

# Execute cues
engine = CrossFadeEngine(universe, cues)
engine.go()  # Cue 1
engine.go()  # Cue 2

# Overlay a slow color cycle effect
fx = EffectGenerator(
    channels=[s4.channel("color_red"), s4.channel("color_green")],
    waveform=Waveform.SINE,
    period_s=12.0,
    amplitude=0.3,
    offset=0.5,
)
engine.apply_effect(fx)
```

### LED Wall and Show File I/O

```python
from lighting_control import LEDWall, ColorCalibrator, ShowFileIO

# Configure an LED video wall panel array
wall = LEDWall(
    panels_x=4, panels_y=3,
    panel_width_px=640, panel_height_px=480,
    dmx_start_address=1,
)
wall.set_pixel_map_mode("rgb_16bit")

# Calibrate and fill
calibrator = ColorCalibrator(reference_color="#FFFFFF")
calibration = calibrator.calibrate_wall(wall)
wall.apply_calibration(calibration)
wall.fill_solid("#FF0000")

# Export show file
ShowFileIO.export_json(cues, "act2_show.json")
imported = ShowFileIO.import_json("act2_show.json")
print(f"Imported: {imported.name} with {len(imported)} cues")
```

## Best Practices

1. **Always patch fixtures at even DMX addresses when using multi-channel profiles.** Odd-start addresses waste channels and can cause misalignment with fixture profiles that expect specific channel ordering. Standard practice is to patch at addresses divisible by the channel count.

2. **Use HTP merge for intensity channels and LTP merge for attribute channels.** Mixing these up causes lights to jump to maximum during cue transitions instead of fading smoothly. Intensity should always use HTP so the brightest command wins.

3. **Calibrate LED fixtures against a reference standard before every production.** LED emitter wavelengths shift with temperature and age; a 15-minute warm-up before calibration is mandatory. Use a colorimeter, not the naked eye.

4. **Keep a maximum of 3 active effect layers on any single fixture.** More layers cause unpredictable parameter conflicts as effects compete for the same DMX channels. If you need more complexity, pre-render the effect into a cue.

5. **Back up show files to three locations before every tech rehearsal.** USB drive, network share, and cloud — losing a show file during tech is unrecoverable. Name backups with date and show version.

6. **Set Art-Net broadcast mode for initial setup, then switch to unicast for production.** Broadcast floods the network with DMX traffic; unicast is cleaner but requires IP configuration on each node. Use subnet 2.0.0.x for Art-Net.

7. **Use tracking mode for cue lists with shared looks.** Non-tracking cue lists require every cue to store complete channel data, making edits error-prone. Tracking means channel values persist through subsequent cues unless explicitly changed.

8. **Verify DMX signal integrity at the last fixture in the chain.** DMX runs 100m max per segment; use opto-isolated DMX splitters for longer runs or daisy chains through cable snakes. Terminate the last fixture with a 120-ohm resistor.

9. **Test all cues with performers on stage before opening.** Performer costumes, skin tones, and positioning affect how light reads. A look that works in empty-house tech may not work with bodies in the space.

10. **Document your fixture patch in a spreadsheet alongside the plot.** When troubleshooting during a show, you need to quickly find which DMX address controls which fixture. The patch sheet is your map.

## Configuration

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| DMX Refresh Rate | 44Hz | 1–44Hz | DMX512 frame output rate |
| Art-Net Net | 0 | 0–127 | Art-Net network identifier |
| Art-Net Subnet | 0 | 0–15 | Art-Net subnet within net |
| Max Universes | 4 | 1–64 | Maximum simultaneous output universes |
| Cross-fade Default | 3.0s | 0.1–60s | Default cue cross-fade time |

## Related Modules

- [stage-automation](../stage-automation/GROK.md) — Automation cue synchronization and DMX bridge for followspot triggers
- [sound-engineering](../sound-engineering/GROK.md) — Audio-reactive lighting effects and sound-to-DMX triggering
- [projection-mapping](../projection-mapping/GROK.md) — Projection-blend color matching with lighting washes
- [audience-engagement](../audience-engagement/GROK.md) — Audience-controlled lighting effects and interactive color mixing

---

## Advanced Configuration

### Fixture Profile Definition

```python
from lighting_control import FixtureProfile, ParameterDefinition

profile = FixtureProfile(
    name="custom_led_wash",
    manufacturer="Custom",
    model="RGBAW Wash 18",
    dmx_channels=8,
    parameters=[
        ParameterDefinition(name="intensity", channel=1, type="dimmer", range=(0, 255)),
        ParameterDefinition(name="red", channel=2, type="color_red", range=(0, 255)),
        ParameterDefinition(name="green", channel=3, type="color_green", range=(0, 255)),
        ParameterDefinition(name="blue", channel=4, type="color_blue", range=(0, 255)),
        ParameterDefinition(name="amber", channel=5, type="color_amber", range=(0, 255)),
        ParameterDefinition(name="white", channel=6, type="color_white", range=(0, 255)),
        ParameterDefinition(name="zoom", channel=7, type="beam_zoom", range=(0, 255)),
        ParameterDefinition(name="strobe", channel=8, type="effect_speed", range=(0, 255)),
    ],
)
```

### Multi-Universe Configuration

```python
from lighting_control import UniverseManager, ArtNetNode

manager = UniverseManager()
for i in range(8):
    node = ArtNetNode(ip=f"2.0.0.{i}", subnet=0, universe=i)
    manager.add_universe(i, node)

manager.set_merge_mode(universe=0, channel=1, mode="htp")
manager.set_merge_mode(universe=0, channel=50, mode="ltp")
```

## Architecture Patterns

### Layered Output Pipeline

```
Channel Values (static)
     │
     ▼
┌──────────────┐
│  Cue Layer   │── Cue snapshots + tracking
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Effect Layer │── Oscillators, random, step patterns
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Priority    │── HTP/LTP merge per channel
│    Merge     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  DMX Output  │── 512-channel frame per universe
└──────────────┘
```

### Color Pipeline Architecture

1. **Color Selection**: Designer picks target color (hex, CIE xy, gel name)
2. **Gamut Mapping**: Map to fixture's available color space (RGBW, RGBAW, CMY)
3. **Calibration Apply**: Apply per-fixture calibration offset
4. **Cross-fade Interpolation**: Interpolate during cue transitions
5. **DMX Output**: Convert to DMX channel values

## Integration Guide

### Show File Exchange

```python
from lighting_control import ShowFileIO

# Export to multiple formats
ShowFileIO.export_eos(cues, "show.eos")
ShowFileIO.export_grandma2(cues, "show.gma2")
ShowFileIO.export_json(cues, "show.json")

# Import with mapping
imported = ShowFileIO.import_json("show.json", fixture_map="patch.json")
```

### Audio-Reactive Integration

```python
from lighting_control import AudioReactiveBridge

bridge = AudioReactiveBridge(audio_input="hw:1,0")
bridge.map_frequency_band("bass", channels=[1, 2, 3], sensitivity=0.8)
bridge.map_frequency_band("treble", channels=[10, 11, 12], sensitivity=0.5)
bridge.enable()
```

## Performance Optimization

| Strategy | Benefit | Implementation |
|----------|---------|----------------|
| Frame batching | 50% less network traffic | Buffer 3 frames before send |
| Effect pre-rendering | Reduced CPU during show | Bake effects into cue snapshots |
| Lazy fixture patching | Faster startup | Patch fixtures on first use |
| DMX merge caching | Skip unchanged frames | Hash-based change detection |
| Universe grouping | Efficient multicast | Group fixtures by network segment |

## Security Considerations

- **Art-Net network isolation**: Lighting networks must be on dedicated VLANs
- **DMX signal integrity**: Use opto-isolated splitters and terminators
- **Show file integrity**: Checksum verification on imported show files
- **Access control**: Lock console programming behind authentication
- **Backup strategy**: Triple backup (USB, network, cloud) before every tech rehearsal

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| LED color shift after warmup | Thermal drift | Recalibrate after 15min warmup |
| Moving light jitter | DMX signal interference | Check cable termination, use shielded cable |
| Art-Net not broadcasting | Subnet mismatch | Verify Art-Net subnet matches node config |
| Cue list jumps unexpectedly | Tracking mode error | Check tracking vs. block cue settings |
| Color mismatch between fixtures | No calibration | Run per-fixture color calibration |
| Effect stutters | Too many active layers | Limit to 3 layers per fixture |

## API Reference

### DMXUniverse

```python
class DMXUniverse:
    def __init__(self, universe_id: int)
    def patch(self, fixture: Fixture) -> None
    def set_channel(self, channel: int, value: int) -> None
    def output(self, node: ArtNetNode) -> bytes
    def snapshot(self) -> bytes
    def restore(self, snapshot: bytes) -> None
```

### CrossFadeEngine

```python
class CrossFadeEngine:
    def __init__(self, universe: DMXUniverse, cues: CueList)
    def go(self, fade_time: float = None) -> None
    def back(self) -> None
    def apply_effect(self, effect: EffectGenerator) -> None
    def remove_effect(self, effect_id: str) -> None
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List

class MergeMode(Enum):
    HTP = "highest_takes_precedence"
    LTP = "latest_takes_precedence"

@dataclass
class Fixture:
    name: str
    profile: str
    dmx_address: int
    universe: int = 0

@dataclass
class CueEntry:
    number: float
    look: dict
    fade_time_s: float
    follow_time_s: Optional[float] = None
    delay_time_s: float = 0.0

@dataclass
class ColorMix:
    r: float  # 0.0-1.0
    g: float
    b: float
    a: float = 1.0
```

## Deployment Guide

### Installation

```bash
pip install lighting-control
```

### Network Setup

1. Configure Art-Net nodes with static IPs on 2.0.0.x subnet
2. Set subnet and universe on each node
3. Connect all nodes to dedicated lighting switch
4. Configure DMX termination on last fixture in each run

## Monitoring & Observability

```python
from lighting_control import MetricsCollector

collector = MetricsCollector()
collector.counter("lighting.cues.executed", count, tags={"list": cue_list})
collector.gauge("lighting.universe.active_fixtures", count, tags={"universe": uid})
collector.histogram("lighting.crossfade.duration_ms", duration)
collector.counter("lighting.effects.active", count)
```

## Testing Strategy

```python
import pytest
from lighting_control import DMXUniverse, Fixture, ColorMix

def test_channel_output():
    universe = DMXUniverse(universe_id=0)
    fixture = Fixture(name="Test", profile="dimmer", dmx_address=1)
    universe.patch(fixture)
    fixture.set_intensity(0.5)
    frame = universe.output(None)
    assert frame[0] == 127  # 50% of 255

def test_color_conversion():
    color = ColorMix.from_hex("#FF0000")
    assert color.r == 1.0
    assert color.g == 0.0
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added sACN support | Add sACN nodes alongside Art-Net |
| 2.0.0 | New fixture profile format | Rebuild custom profiles using new schema |

## Glossary

| Term | Definition |
|------|-----------|
| **DMX512** | Digital Multiplex protocol for lighting control |
| **Art-Net** | DMX over IP (UDP) protocol |
| **HTP** | Highest Takes Precedence — brightest command wins |
| **LTP** | Latest Takes Precedence — most recent command wins |
| **CIE 1931** | Color space standard for perceptual color matching |
| **Gel** | Physical color filter (Lee, Rosco) |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with DMX512 and Art-Net support
- Cue list engine with cross-fade and tracking
- Fixture library with 200+ profiles
- CIE 1931 color space conversion

## Contributing Guidelines

```bash
git clone https://github.com/example/lighting-control.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### DMX Channel Assignment Standards

| Channel Range | Function | Default |
|--------------|----------|---------|
| 1-10 | Conventional dimmers | Intensity 0-100% |
| 11-50 | LED wash fixtures | RGBW + intensity |
| 51-100 | Moving light fixtures | Pan, tilt, color, gobo, beam |
| 101-200 | Effects fixtures | Strobe, color chase, pixel map |
| 201-250 | Media server | Layer control, transport |
| 251-300 | Followspots | Intensity, color, iris |
| 301-400 | LED video wall | Pixel data |
| 401-512 | Special/auxiliary | Fog machines, mirrors, etc. |

### Color Temperature Reference

| CCT (K) | Description | Common Use |
|---------|-------------|------------|
| 1800K | Candle light | Warm intimate scenes |
| 2700K | Incandescent | Standard tungsten |
| 3200K | Studio white | Broadcast standard |
| 4000K | Cool white | Office/modern |
| 5600K | Daylight | Outdoor simulation |
| 6500K | Overcast sky | Flat daylight |
| 7500K | Blue sky | Cool outdoor |

### Cue List Timing Reference

| Fade Time | Feel | Common Use |
|-----------|------|------------|
| 0s | Snap | Blackout, effects |
| 0.5s | Quick | Musical accents |
| 1s | Standard | Scene changes |
| 3s | Slow | Emotional transitions |
| 5s | Very slow | Dramatic reveals |
| 10s | Extremely slow | Sunrises, sunsets |
| 30s+ | Sunset/sunrise | Environmental changes |

### Effect Generator Parameters

```python
from lighting_control import EffectGenerator, Waveform

# Sine wave color cycle
fx = EffectGenerator(
    channels=[red_ch, green_ch, blue_ch],
    waveform=Waveform.SINE,
    period_s=12.0,
    amplitude=0.3,
    offset=0.5,
    phase_offset=0.0,
)

# Random intensity flicker (candle effect)
candle = EffectGenerator(
    channels=[intensity_ch],
    waveform=Waveform.RANDOM,
    period_s=0.5,
    amplitude=0.2,
    offset=0.8,
    smoothing=0.7,
)

# Step-based chase pattern
chase = EffectGenerator(
    channels=[ch1, ch2, ch3, ch4, ch5, ch6],
    waveform=Waveform.STEP,
    period_s=2.0,
    amplitude=1.0,
    offset=0.0,
    steps=6,
)
```

### Fixture Profile Database

The module includes profiles for 200+ fixtures from:

- **ETC**: Source Four LED Series 3, ColorSource, Desire
- **Martin**: MAC Viper, MAC Aura, MAC Quantum
- **Robe**: BMFL, Spiider, ParFect
- **Clay Paky**: Sharpy, K-Eye, A.leda
- **Vari-Lite**: VL3000, VL3500, VLZ
- **Chauvet**: Rogue, Ovation, COLORado
- **ADJ**: Mega Hex, Focus Spot, Pro Event
- **Generic**: Dimmer, LED RGBA, RGBW, CMY wash, moving head

### Complete Art-Net Configuration

```python
from lighting_control import ArtNetConfig

config = ArtNetConfig(
    net=0,
    subnet=0,
    universe=0,
    ip="2.0.0.1",
    broadcast=False,
    multicast_address="239.255.0.1",
    refresh_hz=44,
    packet_timeout_ms=100,
    retry_count=3,
)
```

### Complete Show File Format

```json
{
  "show_name": "Hamilton - Broadway",
  "version": "2.1.0",
  "lighting_designer": "Howell Binkley",
  "created_at": "2024-01-15",
  "fixtures": [
    {"id": "wash_1", "profile": "etc_sourcefour_led_s3", "dmx_address": 101, "universe": 0, "label": "Main Wash L"},
    {"id": "wash_2", "profile": "etc_sourcefour_led_s3", "dmx_address": 201, "universe": 0, "label": "Main Wash R"},
    {"id": "spot_1", "profile": "martin_mac_viper", "dmx_address": 1, "universe": 1, "label": "Lead Spot"}
  ],
  "cue_lists": [
    {
      "name": "Act 1",
      "cues": [
        {"number": 1, "look": {"wash_1": {"intensity": 0.8}}, "fade_time_s": 3.0},
        {"number": 2, "look": {"wash_1": {"intensity": 0.4}, "spot_1": {"intensity": 1.0}}, "fade_time_s": 5.0}
      ]
    }
  ]
}
```

### Troubleshooting Decision Tree

```
Fixture not responding
    │
    ├── Check DMX connection → Verify cable and termination
    ├── Check DMX address → Verify patch matches fixture
    ├── Check fixture power → Verify AC connection
    ├── Check fixture mode → Ensure correct DMX mode
    ├── Test with DMX tester → Confirm signal at fixture
    └── Replace fixture if hardware fault

Color mismatch between fixtures
    │
    ├── Run color calibration → Per-fixture color matching
    ├── Check fixture age → LED emitters degrade over time
    ├── Check ambient light → Ambient affects perceived color
    ├── Check gel/filter → Verify correct color temperature
    └── Match white points → Use colorimeter

Cue list not tracking
    │
    ├── Check tracking mode → Enable tracking in cue list
    ├── Check block cues → Verify block cue markers
    ├── Check manual values → Release manual overrides
    └── Check console mode → Verify programmer state
```

### Performance Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| DMX refresh rate | 44 Hz | < 40 Hz | < 30 Hz |
| Art-Net packet loss | 0% | < 0.01% | > 0.01% |
| Cross-fade accuracy | ± 1 frame | ± 2 frames | > 2 frames |
| Color calibration accuracy | ΔE < 2 | ΔE 2-5 | ΔE > 5 |
| Fixture response time | < 1 frame | 1-2 frames | > 2 frames |
| Effect frame rate | 30 fps | < 25 fps | < 20 fps |
| Show file load time | < 5s | 5-15s | > 15s |

### Common Gel/Filter Reference

| Gel Number | Manufacturer | Color | CCT |
|-----------|-------------|-------|-----|
| No. 201 | Lee | Full CT Orange | 2500K |
| No. 202 | Lee | Half CT Orange | 3000K |
| No. 206 | Lee | Full CT Blue | 5600K |
| No. 339 | Rosco | Egyptian Rose | — |
| No. 382 | Rosco | Fire | — |
| No. 68 | Rosco | Sky Blue | — |
| No. 071 | Lee | Pale Gold | — |

### Complete Fixture Patch Template

```csv
ID,Name,Profile,DMX_Address,Universe,Position,Notes
wash_1,Main Wash L,etc_sourcefour_led_s3,101,0,FOH Left,Primary wash
wash_2,Main Wash R,etc_sourcefour_led_s3,201,0,FOH Right,Primary wash
wash_3,Center Wash,etc_sourcefour_led_s3,301,0,FOH Center,Fill wash
spot_1,Lead Spot,martin_mac_viper,1,1,FOH Center,Lead performer
spot_2,Spot L,martin_mac_viper,31,1,FOH Left,Supporting
spot_3,Spot R,martin_mac_viper,61,1,FOH Right,Supporting
wash_4,Side Wash L,robeparfect_100,91,0,Stage Left,Side light
wash_5,Side Wash R,robeparfect_100,121,0,Stage Right,Side light
strip_1,LED Strip,chauvet_colorstrip,151,0,On Set,Cyc light
strip_2,LED Strip 2,chauvet_colorstrip,181,0,On Set,Cyc light
```

### DMX Signal Chain Troubleshooting

```
Source (Console/Software)
    │
    ├── Check output enabled → Verify DMX output active
    ├── Check universe mapping → Verify correct universe
    ├── Check IP configuration → Verify Art-Net subnet
    │
    ▼
Network Switch
    │
    ├── Check VLAN → Verify dedicated lighting VLAN
    ├── Check multicast → Enable IGMP snooping
    ├── Check bandwidth → Verify sufficient capacity
    │
    ▼
DMX Node/Adapter
    │
    ├── Check node IP → Verify static IP assignment
    ├── Check DMX output → Test with DMX tester
    ├── Check termination → 120Ω resistor at end of chain
    │
    ▼
DMX Cable Run
    │
    ├── Check cable length → Max 100m per segment
    ├── Check cable type → Use shielded DMX cable
    ├── Check connectors → 5-pin XLR (not 3-pin)
    ├── Check for damage → Test continuity
    │
    ▼
Fixture
    │
    ├── Check DMX address → Verify matches patch
    ├── Check fixture mode → Verify DMX channel count
    ├── Check power → Verify AC connection
    └── Check response → Test with DMX tester at fixture
```

### Moving Light Parameter Reference

| Parameter | Channel | Range | Description |
|-----------|---------|-------|-------------|
| Pan | 1 | 0-255 | Horizontal rotation |
| Tilt | 2 | 0-255 | Vertical rotation |
| Intensity | 3 | 0-255 | Lamp brightness |
| Color Wheel | 4 | 0-255 | Fixed color selection |
| Color Mix CMY | 5-7 | 0-255 | Cyan, Magenta, Yellow mixing |
| Color Mix RGBW | 5-8 | 0-255 | Red, Green, Blue, White mixing |
| Gobo Wheel 1 | 9 | 0-255 | Gobo pattern selection |
| Gobo Wheel 2 | 10 | 0-255 | Secondary gobo |
| Gobo Rotate | 11 | 0-255 | Gobo rotation speed/direction |
| Iris | 12 | 0-255 | Iris opening size |
| Zoom | 13 | 0-255 | Beam angle |
| Focus | 14 | 0-255 | Focus adjustment |
| Prism | 15 | 0-255 | Prism insertion/rotation |
| Frost | 16 | 0-255 | Frost/haze diffusion |
| Strobe | 17 | 0-255 | Strobe speed |
| Dimmer Curve | 18 | 0-255 | Dimmer response curve |

### Common Lighting Ratios

| Scenario | Key:Fill | Key:Back | Description |
|----------|---------|---------|-------------|
| Front wash | 2:1 | — | Flat, even coverage |
| Dramatic | 4:1 | 2:1 | Strong shadows |
| Musical | 3:1 | 3:1 | Balanced with back light |
| Intimate | 2:1 | 1:1 | Soft, warm feel |
| Horror | 8:1 | 4:1 | High contrast, deep shadows |

### Network Topology for Lighting

```
Console (Primary)
    │
    ├── Art-Net Node 1 (2.0.0.1) → Universe 0 (Dimmers)
    ├── Art-Net Node 2 (2.0.0.2) → Universe 1 (Moving Lights)
    ├── Art-Net Node 3 (2.0.0.3) → Universe 2 (LED Fixtures)
    ├── Art-Net Node 4 (2.0.0.4) → Universe 3 (Effects)
    ├── Art-Net Node 5 (2.0.0.5) → Universe 4 (Media Server)
    └── Art-Net Node 6 (2.0.0.6) → Universe 5 (Followspots)

All nodes connected to dedicated lighting switch (VLAN 10)
Switch uplinked to console via 10GbE
DMX output from each node to fixture chain
```

### Show File Backup Protocol

| Backup Location | Timing | Method |
|----------------|--------|--------|
| USB Drive | Before every tech rehearsal | Manual copy |
| Network Share | Before every performance | Automated sync |
| Cloud Storage | Daily | Automated upload |
| Console Internal | Real-time | Auto-save |
| Email to designer | Before opening night | Manual send |

### Lighting Design Workflow

```
PRE-PRODUCTION
    │
    ├── Read script and understand design intent
    ├── Meet with director for concept discussion
    ├── Create initial plot and concept sketches
    ├── Select fixture types and positions
    ├── Create DMX patch sheet
    └── Program cue list (offline)

TECHNICAL REHEARSAL
    │
    ├── Focus and aim all fixtures
    ├── Color calibrate LED fixtures
    ├── Program cues with director
    ├── Fine-tune timing and levels
    ├── Integrate with sound and automation
    └── Document final cue list

### Complete Art-Net Packet Format

```
Art-Net Header (12 bytes):
  ID: "Art-Net" (8 bytes)
  OpCode: 0x5000 (2 bytes) - DMX
  ProtVer: 14 (2 bytes)

DMX Data (532 bytes):
  Flags: 0 (1 byte)
  Sequence: 0-255 (1 byte)
  Physical: 0 (1 byte)
  SubUni: subnet (1 byte)
  Net: net (1 byte)
  Length: 512 (2 bytes)
  Data: 512 bytes of DMX channel data
```

### Fixture Group Definitions

```python
from lighting_control import FixtureGroup

groups = {
    "wash": FixtureGroup(name="Wash", fixtures=["wash_1", "wash_2", "wash_3", "wash_4", "wash_5"]),
    "spots": FixtureGroup(name="Spots", fixtures=["spot_1", "spot_2", "spot_3"]),
    "effects": FixtureGroup(name="Effects", fixtures=["strip_1", "strip_2"]),
    "stage_left": FixtureGroup(name="Stage Left", fixtures=["wash_4", "spot_2"]),
    "stage_right": FixtureGroup(name="Stage Right", fixtures=["wash_5", "spot_3"]),
    "downstage": FixtureGroup(name="Downstage", fixtures=["wash_1", "wash_2"]),
    "upstage": FixtureGroup(name="Upstage", fixtures=["wash_3"]),
    "all": FixtureGroup(name="All", fixtures=["*"]),
}
```

### Common DMX Addresses by Fixture Type

| Fixture Type | Channels | Recommended Start | Notes |
|-------------|----------|------------------|-------|
| Single dimmer | 1 | Any | Simplest |
| LED RGBA wash | 4-5 | Divisible by 4 | Even alignment |
| LED RGBW wash | 4-5 | Divisible by 4 | Even alignment |
| Moving head | 16-24 | Divisible by 8 | Check profile |
| Moving head (full) | 32-48 | Divisible by 16 | Full parameter |
| Media server | 1-8 per layer | Divisible by 8 | Per layer |
| LED strip (pixel) | 3 per pixel | Contiguous | Long addresses |

### Lighting Cue Timing Reference

```
CUE 1 (3.0s fade)
  ├── Wash: 0% → 80% over 3.0s
  ├── Spot: 0% → 0% (no change)
  └── Follow: 8.0s to next cue

CUE 2 (5.0s fade)
  ├── Wash: 80% → 40% over 5.0s
  ├── Wash Color: Warm → Cool over 5.0s
  ├── Spot: 0% → 100% over 5.0s
  ├── Spot Gobo: Open → Breakup at 3.0s
  └── Follow: None (manual go)

CUE 2.5 (2.0s fade)
  ├── Spot Gobo: Breakup → Breakup Slow over 2.0s
  └── Follow: None (manual go)

CUE 3 (0.5s fade)
  ├── All: Current → 0% over 0.5s (blackout)
  └── Follow: None (end of scene)
```

### Performance Checklist

```
PRE-SHOW (30 min before)
    □ Load show file
    □ Verify all fixtures responding
    □ Check DMX signal at last fixture in chain
    □ Test E-stop (lighting only)
    □ Verify Art-Net connectivity
    □ Check fixture patch matches documentation
    □ Test cue list execution
    □ Verify color calibration
    □ Check effect generators
    □ Backup show file

DURING SHOW
    □ Monitor DMX output
    □ Watch for fixture failures
    □ Verify cue timing
    □ Monitor ambient light levels
    □ Log any anomalies

POST-SHOW
    □ Backup final show file
    □ Log any fixture issues
    □ Note any timing adjustments
    □ Document any cue additions
    □ Power down in correct order
```

PRODUCTION
    │
    ├── Pre-show check (30 min before)
    ├── Load show file
    ├── Run cue-to-cue with stage manager
    ├── Monitor during performance
    ├── Note any adjustments needed
    └── Post-show backup and notes
```

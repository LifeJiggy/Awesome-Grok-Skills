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

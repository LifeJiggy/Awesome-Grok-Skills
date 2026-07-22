---
name: "sound-engineering"
category: "theater-tech"
version: "1.0.0"
tags: ["theater-tech", "sound-engineering", "audio", "mixing", "dolby-atmos"]
---

# Sound Engineering Control System

## Overview

The sound engineering module provides a comprehensive Python API for digital audio mixing console control, speaker system optimization, acoustic simulation, and spatial audio rendering in theatrical and live entertainment environments. It interfaces with industry-standard digital mixing consoles (Yamaha CL/QL/TF, Allen & Heath dLive/SQ, Midas M32/H32, DiGiCo SD/Quantum) via MIDI, OSC, and proprietary protocols, enabling programmatic recall of show files, scene automation, and remote parameter control from a unified Python interface. The module supports both live show operation and pre-production planning, allowing sound designers to model room acoustics and speaker coverage before hardware is installed.

Speaker array design and optimization is a core capability: the module implements delay alignment algorithms for line arrays, calculates coverage angles for point-source clusters, and performs room simulation using image-source modeling for early reflections and statistical models for late reverberation. It supports both predictive design (before the rig goes in the air) and measurement-based optimization (using transfer function analysis from calibrated measurement microphones). The integrated wireless frequency coordination engine scans the RF spectrum, identifies occupied frequencies, and assigns clean channels to wireless microphone systems while maintaining minimum intermodulation spacing — a critical workflow in venues where 40+ wireless channels share limited spectrum.

Spatial audio rendering for Dolby Atmos and other immersive formats is handled through a renderer abstraction layer. The module can drive AtmosRenderer via Dolby's RMU (Rendering and Mastering Unit) protocol, d&b Soundscape via OSC, or L-Acoustics L-ISA via its processor API. Object-based audio metadata (position, size, diffusion) is computed from source positions in a virtual room model, allowing sound designers to place and move sound objects in 3D space that map to physical speaker arrays of arbitrary geometry.

## Core Capabilities

- Digital mixing console control via MIDI, OSC, and proprietary protocols (Yamaha, Allen & Heath, Midas, DiGiCo)
- Speaker array optimization with delay alignment, coverage prediction, and SPL mapping
- Room acoustic simulation using image-source early reflections and Sabine/EBU reverberation models
- Wireless microphone frequency coordination with intermodulation analysis and spectrum scanning
- Real-time feedback suppression with adaptive notch filters and frequency tracking
- Dolby Atmos / d&b Soundscape / L-ISA spatial audio object rendering
- Dual-channel automatic mixing (Gain Sharing, Gating) for panel discussions
- Monitor mix management with personal mix station control and FOH automation

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Show Control & Scene Automation             │
│   (Scene Recall, Cue Lists, Snapshot A/B, GPIO)         │
├─────────────────────────────────────────────────────────┤
│              Audio Processing Pipeline                   │
│  (EQ, Dynamics, Effects, Auto-Mix, Feedback Suppression)│
├─────────────────────────────────────────────────────────┤
│            Speaker Management & Optimization            │
│   (Delay Alignment, Coverage, SPL Mapping, Arrays)      │
├─────────────────────────────────────────────────────────┤
│              Console Communication Layer                 │
│        (OSC, MIDI, Yamaha CL, Midas M32, DiGiCo)        │
├─────────────────────────────────────────────────────────┤
│              Spatial Audio Rendering                    │
│      (Dolby Atmos, d&b Soundscape, L-ISA, Objects)     │
└─────────────────────────────────────────────────────────┘
```

## Usage Examples

### Mixing Console Control

```python
from sound_engineering import MixingConsole, ConsoleProtocol, EQBand, FilterType

# Connect to a Yamaha CL5 console via OSC
console = MixingConsole(
    protocol=ConsoleProtocol.OSC,
    ip="192.168.1.50",
    port=8000,
    console_model="yamaha_cl5",
)
console.connect()

# Set channel parameters
console.set_channel_fader(channel=1, level_db=-6.0)
console.set_channel_eq(
    channel=1, band=1,
    freq_hz=80, gain_db=3.0, q=0.7,
    filter_type=FilterType.LOW_SHELF,
)
console.set_channel_compressor(
    channel=1,
    threshold_db=-20, ratio=3.0,
    attack_ms=10, release_ms=100,
)
console.set_mute(channel=1, muted=False)

# EQ biquad coefficient computation
eq = EQBand(band_id=1, filter_type=FilterType.PEAK, frequency_hz=1000, gain_db=6.0, q=1.0)
coeffs = eq.compute_coefficients()
print(f"b0={coeffs['b0']:.4f}, a1={coeffs['a1']:.4f}")
```

### Speaker Array Design

```python
from sound_engineering import SpeakerArray, RoomSimulator, DelayAligner

# Design a line array for a 1200-seat theater
array = SpeakerArray(
    num_boxes=8,
    box_spacing_m=1.0,
    splay_angles_deg=[0, 3, 5, 7, 9, 11, 14, 17],
    box_coverage_h_deg=80,
    box_coverage_v_deg=50,
    sensitivity_db=105,
    max_spl_db=136,
)

# Calculate coverage
coverage = array.calculate_coverage()
print(f"Total splay: {coverage['total_splay_deg']:.1f}°")

# SPL at listener position
spl_at_20m = array.calculate_spl_at_distance(20)
print(f"SPL at 20m: {spl_at_20m:.1f} dB")

# Room simulation
room = RoomSimulator(length_m=30, width_m=20, height_m=12, rt60_target_s=1.4)
room.set_source_position(x=0, y=0, z=1.5)
room.set_listener_position(x=20, y=0, z=1.2)
ir = room.simulate(num_reflections=6)
print(f"Direct time: {ir['direct_time_s']:.3f}s, RT60: {ir['calculated_rt60_s']:.2f}s")

# Delay alignment
aligner = DelayAligner(main_array_distance_m=15, delay_tower_distance_m=25)
delay = aligner.calculate_delay()
print(f"Delay tower compensation: {delay:.2f} ms")
```

### Wireless Frequency Coordination

```python
from sound_engineering import WirelessCoordinator, FrequencyBand

# Coordinate 24 wireless channels in the UHF band
coordinator = WirelessCoordinator(
    band=FrequencyBand.UHF_470_698,
    num_channels=24,
    intermod_spacing_khz=300,
    exclusion_zones=[(512, 524), (614, 618)],  # DTV channels
)

plan = coordinator.calculate_plan()
for ch in plan.channels[:5]:
    print(f"Ch {ch.number}: {ch.frequency_mhz:.2f} MHz (IM margin: {ch.im_margin_db:.1f} dB)")
print(f"Active: {plan.active_count}, min IM margin: {plan.min_im_margin:.1f} dB")

# Scan and recalculate
coordinator.scan_spectrum(duration_s=5)
clean_plan = coordinator.recalculate_with_scan()
```

### Spatial Audio Rendering

```python
from sound_engineering import SpatialRenderer, SoundObject, AtmosConfig

# Set up Dolby Atmos rendering
config = AtmosConfig(num_objects=16, bed_channels=7, speaker_layout="7.1.4")
renderer = SpatialRenderer(config)
renderer.connect()

# Place and animate a sound object
rain = SoundObject(object_id=1, name="rain_effect", x=0.3, y=-0.2, z=0.8, size=0.4)
renderer.place_object(rain)
renderer.animate_object(
    object_id=1,
    path=[(0.3, -0.2, 0.8), (0.0, 0.0, 1.0), (-0.3, 0.2, 0.8)],
    duration_s=10.0,
    easing="ease_in_out",
)
```

### Auto-Mix and Monitor Management

```python
from sound_engineering import AutoMixer, AutoMixMode, MonitorMixManager

# Auto-mix for a 4-person panel
auto = AutoMixer(num_channels=4, mode=AutoMixMode.GAIN_SHARING)
gains = auto.process([-20, -40, -35, -50])
print(f"Auto-mix gains: {[f'{g:.1f}' for g in gains]} dB")

# Monitor mix management
monitors = MonitorMixManager(num_mixes=12, num_channels=48)
monitors.set_performer_name(1, "Lead Vocal")
monitors.create_default_mix(1, vocal_channels=[1, 2], level_db=0.0)
monitors.set_mix_level(1, 15, -6.0)  # Add drums to vocal monitor
```

## Best Practices

1. **Always start with all faders down when connecting to a live console.** The initial OSC/MIDI connection may trigger fader jumps if the console's snapshot doesn't match the software's cached state. This prevents sudden volume spikes.

2. **Calibrate measurement microphones before every optimization session.** A ±2dB calibration error in a measurement mic cascades into incorrect EQ and delay calculations for the entire array. Use a calibrator that produces a known SPL at a known frequency.

3. **Leave 6dB of headroom on every channel at sound check.** Performers sing louder during the show than during check; headroom prevents clipping without compression artifacts. Digital clipping at 0dBFS is unrecoverable.

4. **Run wireless frequency scans at the same time of day as the performance.** RF environments change between morning load-in and evening showtime due to audience body absorption and adjacent transmitters turning on.

5. **Test feedback suppression in the actual room with all performers on stage.** Head-mounted microphones feedback differently than handhelds, and costume changes alter the acoustic boundary near the mic element.

6. **Use delay towers instead of increased main array power for far-field coverage.** Doubling SPL at the source only adds 6dB; a delay tower at the 2/3 point provides consistent coverage without deafening the front rows.

7. **Maintain a 1:2 ratio between reverb time and show pacing.** Dense dialogue scenes need RT60 under 1.0s; musical numbers can tolerate 1.4–1.8s depending on tempo. Adjust room treatment accordingly.

8. **Export and archive show files with firmware version metadata.** Console firmware updates can subtly change DSP behavior; knowing which firmware a show was designed on prevents debugging phantom issues.

9. **Use scene numbering that matches the script, not arbitrary sequences.** Scene 1 = Act 1 Scene 1, Scene 15 = Act 2 Scene 3. This makes recall intuitive under pressure.

10. **Monitor wireless mic battery levels every intermission.** A dead mic mid-scene is a show-stopping failure. Set low-battery alerts at 20% to allow time for changes during breaks.

## Related Modules

- [lighting-control](../lighting-control/GROK.md) — Audio-reactive lighting effects and sound-to-DMX triggering
- [stage-automation](../stage-automation/GROK.md) — Automation cue timing and audio-visual synchronization
- [projection-mapping](../projection-mapping/GROK.md) — Spatial audio alignment with projected visual environments
- [audience-engagement](../audience-engagement/GROK.md) — Audience audio response capture and interactive soundscapes

---

## Advanced Configuration

### Console Protocol Mapping

```python
from sound_engineering import ConsoleMapping, ChannelMapping

mapping = ConsoleMapping(console="yamaha_cl5", base_address="192.168.1.50")
mapping.add_channel_map(ChannelMapping(local_channel=1, remote_channel=1, label="Lead Vocal"))
mapping.add_channel_map(ChannelMapping(local_channel=2, remote_channel=5, label="Bass DI"))
mapping.add_channel_map(ChannelMapping(local_channel=3, remote_channel=9, label="Drum Overhead L"))
```

### Room Simulation Advanced Parameters

```python
from sound_engineering import RoomSimulator

room = RoomSimulator(
    length_m=30, width_m=20, height_m=12,
    rt60_target_s=1.4,
    air_absorption=True,
    surface_materials={
        "walls": {"absorption_coeff": 0.15, "scattering_coeff": 0.3},
        "ceiling": {"absorption_coeff": 0.85, "scattering_coeff": 0.5},
        "floor": {"absorption_coeff": 0.05, "scattering_coeff": 0.1},
    },
)
```

## Architecture Patterns

### Signal Flow Architecture

```
Microphone / DI Input
        │
        ▼
┌──────────────┐
│  Preamp /    │── Gain staging, phantom power
│  ADC Stage   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Channel     │── EQ, Dynamics, Gate
│  Strip       │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Bus / Group │── Mix bus, aux sends
│  Routing     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Output /    │── Main L/R, monitors, subgroups
│  Matrix      │
└──────────────┘
```

### Spatial Audio Pipeline

```
Sound Source Position (x, y, z)
        │
        ▼
┌──────────────┐
│ Object       │── Position, size, diffusion metadata
│ Renderer     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Speaker Map  │── Map objects to physical speaker array
│ Optimizer    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Output       │── Per-speaker audio streams
│ Feeds        │
└──────────────┘
```

## Integration Guide

### MIDI Show Control Integration

```python
from sound_engineering import MIDI ShowControl

msc = MIDIShowControl(device="hw:1,0")
msc.set_timecode_source("LTC")
msc.bind_cue("SCENE", "001", callback=load_scene_001)
msc.start()
```

### Wireless Mic Monitoring Dashboard

```python
from sound_engineering import WirelessMonitor

monitor = WirelessMonitor()
monitor.add_receiver("shure_ulxd4", ip="192.168.1.60")
monitor.set_alert_battery_low(percent=20)
monitor.set_alert_rf_weak(threshold_dbm=-80)
monitor.start_dashboard(port=8080)
```

## Performance Optimization

| Optimization | Impact |
|-------------|--------|
| Audio buffer size tuning | Reduce latency from 20ms to 5ms |
| DSP processing order | Apply subtractive before additive |
| Delay tower alignment | Consistent SPL across venue |
| Monitor mix personalization | Reduce stage volume 40% |
| Feedback suppressor optimization | 6dB more gain before feedback |

## Security Considerations

- **Network audio isolation**: Dante/AES67 traffic on dedicated VLAN
- **Console access control**: PIN-protected user profiles
- **Show file encryption**: Encrypt archived show files with sensitive settings
- **Wireless microphone encryption**: AES-256 encryption on digital wireless systems
- **Recording consent**: Always obtain consent before recording performances

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Feedback howl | Mic too close to speaker | Engage HPF, reduce gain, check mic position |
| Wireless dropout | RF interference | Scan frequencies, check antenna placement |
| Latency in monitors | Buffer too large | Reduce buffer size to 5ms |
| DSP artifacts | Clipping in digital domain | Reduce channel gain, check headroom |
| Dante clock sync failure | PTP misconfiguration | Verify grandmaster clock settings |
| Scene recall mismatch | Firmware version change | Verify firmware, update show file |

## API Reference

### MixingConsole

```python
class MixingConsole:
    def __init__(self, protocol: ConsoleProtocol, ip: str, port: int, console_model: str)
    def connect(self) -> None
    def set_channel_fader(self, channel: int, level_db: float) -> None
    def set_channel_eq(self, channel: int, band: int, freq_hz: float, gain_db: float, q: float, filter_type: FilterType) -> None
    def set_channel_compressor(self, channel: int, threshold_db: float, ratio: float, attack_ms: float, release_ms: float) -> None
    def set_mute(self, channel: int, muted: bool) -> None
    def recall_scene(self, scene_number: int) -> None
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class FilterType(Enum):
    LOW_SHELF = "low_shelf"
    PEAK = "peak"
    HIGH_SHELF = "high_shelf"
    LOW_PASS = "low_pass"
    HIGH_PASS = "high_pass"

@dataclass
class SpeakerBox:
    model: str
    sensitivity_db: float
    max_spl_db: float
    coverage_h_deg: float
    coverage_v_deg: float

@dataclass
class RoomIR:
    direct_time_s: float
    early_reflections: list
    calculated_rt60_s: float
    frequency_response: list
```

## Deployment Guide

### Installation

```bash
pip install sound-engineering
```

### Console Connection Setup

1. Connect console to dedicated audio network
2. Configure static IP on both console and host
3. Test OSC/MIDI connectivity
4. Load console profile in configuration

## Monitoring & Observability

```python
from sound_engineering import MetricsCollector

collector = MetricsCollector()
collector.gauge("audio.signal_level_db", level, tags={"channel": ch})
collector.counter("audio.feedback.instances", count)
collector.gauge("audio.wireless.battery_pct", pct, tags={"mic": mic_id})
collector.histogram("audio.scene.recall_ms", duration)
```

## Testing Strategy

```python
import pytest
from sound_engineering import MixingConsole, EQBand

def test_eq_coefficients():
    eq = EQBand(band_id=1, filter_type=FilterType.PEAK, frequency_hz=1000, gain_db=6.0, q=1.0)
    coeffs = eq.compute_coefficients()
    assert coeffs['b0'] is not None
    assert abs(coeffs['a0'] - 1.0) < 0.001
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added DiGiCo protocol | Add DiGiCo IP to config |
| 2.0.0 | Spatial audio module | Migrate to SpatialRenderer API |

## Glossary

| Term | Definition |
|------|-----------|
| **OSC** | Open Sound Control — network protocol for audio |
| **RT60** | Reverberation time (60dB decay) |
| **SPL** | Sound Pressure Level in dB |
| **Dante** | Digital Audio Network Through Ethernet |
| **HPF** | High-Pass Filter |
| **IMD** | Intermodulation Distortion |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with Yamaha, Midas, and Allen & Heath support
- Speaker array optimization
- Wireless frequency coordination
- Auto-mix and monitor management

## Contributing Guidelines

```bash
git clone https://github.com/example/sound-engineering.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Console Protocol Comparison

| Console | Protocol | Port | Features |
|---------|----------|------|----------|
| Yamaha CL/QL | OSC | 8000 | Full parameter control |
| Midas M32/H32 | OSC/MIDI | 10024 | Parameter + scene recall |
| Allen & Heath dLive | TCP | 9923 | Deep integration |
| DiGiCo SD/Quantum | Proprietary | — | Full console control |
| Soundcraft Vi | TCP | 1234 | Basic parameter control |

### Speaker Array Design Reference

| Venue Size | Seats | Array Length | Box Spacing | Max SPL |
|-----------|-------|-------------|-------------|---------|
| Small club | 200-500 | 4-6 boxes | 0.8m | 120 dB |
| Medium theater | 500-1200 | 6-8 boxes | 1.0m | 130 dB |
| Large theater | 1200-2500 | 8-12 boxes | 1.2m | 136 dB |
| Arena | 2500-10000 | 12-16 boxes | 1.5m | 140 dB |
| Stadium | 10000+ | 16-24 boxes | 1.5m | 145 dB |

### Wireless Frequency Band Reference

| Band | Frequency Range | Channels | Notes |
|------|----------------|----------|-------|
| VHF Low | 54-72 MHz | Limited | Older systems |
| VHF High | 169-216 MHz | Limited | Less crowded |
| UHF 470-608 | 470-608 MHz | 200+ | Post-incentive auction |
| UHF 614-698 | 614-698 MHz | Limited | Some DTV clearance |
| 900 MHz | 902-928 MHz | 50+ | ISM band, shared |
| 2.4 GHz | 2400-2483 MHz | Limited | WiFi interference |

### Room Acoustic Parameters

| Parameter | Description | Target (Theater) |
|-----------|-------------|-----------------|
| RT60 | Reverberation time (60dB decay) | 1.0-1.6s |
| EDT | Early decay time | 0.8-1.2s |
| C80 | Clarity (early vs late energy) | > -2 dB |
| D50 | Definition (50ms clarity) | > 0.4 |
| STI | Speech Transmission Index | > 0.6 |
| G | Strength relative to free field | 3-6 dB |

### Complete EQ Reference

| Frequency Range | Character | Common Use |
|----------------|-----------|------------|
| 20-60 Hz | Sub bass | Rumble, felt not heard |
| 60-250 Hz | Bass | Warmth, fullness |
| 250-500 Hz | Low mid | Boxiness, mud |
| 500-2 kHz | Midrange | Presence, body |
| 2-4 kHz | Upper mid | Clarity, articulation |
| 4-8 kHz | Presence | Brightness, air |
| 8-16 kHz | Brilliance | Sparkle, shimmer |

### Complete Signal Flow Reference

```
Stage Input → Preamp → Channel Strip → Bus Routing → Matrix → Output
    │              │           │              │          │         │
    │              │           ├── EQ          ├── Main L/R ├── FOH L/R
    │              │           ├── Compressor  ├── Subs     ├── Delays
    │              │           ├── Gate        ├── Aux 1-12 ├── Monitors
    │              │           ├── De-esser    ├── FX Send  ├── Recording
    │              │           └── Delay       └── Matrix   └── Broadcast
    │              │
    └── Mic/DI → Phantom Power → Pad → HPF → Gain
```

### EQ Setting Reference by Source

| Source | HPF | Low Cut | Boost | Cut | Presence | Air |
|--------|-----|---------|-------|-----|----------|-----|
| Lead Vocal | 80 Hz | — | 200 Hz +3 | 400 Hz -2 | 3 kHz +2 | 12 kHz +1 |
| Acoustic Guitar | 80 Hz | — | 150 Hz +2 | 250 Hz -3 | 2.5 kHz +2 | 10 kHz +1 |
| Electric Guitar | 100 Hz | — | 200 Hz +2 | 400 Hz -2 | 1.5 kHz +3 | — |
| Bass DI | 30 Hz | — | 80 Hz +3 | 200 Hz -2 | 700 Hz +2 | — |
| Kick Drum | 50 Hz | — | 60 Hz +4 | 300 Hz -4 | 3 kHz +2 | — |
| Snare | 80 Hz | — | 200 Hz +2 | 400 Hz -2 | 5 kHz +3 | 10 kHz +1 |
| Overheads | 200 Hz | — | — | 300 Hz -2 | 8 kHz +2 | 14 kHz +1 |

### Dynamic Processing Reference

| Source | Threshold | Ratio | Attack | Release | Knee |
|--------|-----------|-------|--------|---------|------|
| Lead Vocal | -20 dB | 3:1 | 10ms | 100ms | Soft |
| Bass | -15 dB | 4:1 | 5ms | 50ms | Hard |
| Kick Drum | -18 dB | 4:1 | 5ms | 50ms | Hard |
| Drum Bus | -12 dB | 2:1 | 15ms | 150ms | Soft |
| Mix Bus | -6 dB | 2:1 | 30ms | 300ms | Soft |

### Reverb Preset Reference

| Space | Pre-Delay | Decay | Damping | HPF | Mix |
|-------|-----------|-------|---------|-----|-----|
| Vocal Plate | 20ms | 1.8s | Medium | 200Hz | 15% |
| Drum Room | 5ms | 0.8s | High | 150Hz | 20% |
| Hall | 30ms | 2.5s | Low | 100Hz | 25% |
| Chamber | 15ms | 1.5s | Medium | 150Hz | 20% |
| Ambient | 0ms | 3.0s | Low | 80Hz | 30% |

### Monitor Mix Reference by Performer Type

| Performer | Preferred Level | Key Sources | Notes |
|-----------|----------------|-------------|-------|
| Lead Vocal | High (+6 dB) | Self, band | Needs to hear over band |
| Backing Vocal | Medium | Lead vocal, band | Blend with lead |
| Guitar | High (+3 dB) | Self, kick, snare | Needs rhythmic foundation |
| Bass | Medium | Self, kick | Lock with kick drum |
| Drums | High (+6 dB) | Click, band, self | Needs click for tempo |
| Keys | Medium | Self, band, vocals | Often uses IEM |
| Actor/Speaker | Low to Medium | Self, playback | Clear voice reproduction |

### Wireless System Coordination Plan

```python
from sound_engineering import FrequencyPlan

plan = FrequencyPlan(
    band="UHF_470_608",
    exclusion_zones=[
        (512, 524),  # DTV channel 26
        (614, 618),  # DTV channel 38
    ],
    intermod_spacing_khz=300,
    power_level_dbm=10,
)

# Assign frequencies
plan.assign("lead_vocal", group="handhelds")
plan.assign("backing_vocal_1", group="handhelds")
plan.assign("backing_vocal_2", group="handhelds")
plan.assign("guitar_body", group="instrument")
plan.assign("violin_clip", group="instrument")
plan.assign("presenter_1", group="lavalier")
plan.assign("presenter_2", group="lavalier")

# Generate coordination report
report = plan.generate_report()
print(f"Total channels: {report.channel_count}")
print(f"Min intermod margin: {report.min_im_margin:.1f} dB")
print(f"DTV clearance: {report.dtv_clearance_ok}")

### Complete Scene Recall Template

```json
{
  "scene_number": 1,
  "scene_name": "Act 1 Opening",
  "cues": [
    {"channel": 1, "fader": -6.0, "mute": false, "eq": {"band": 1, "freq": 80, "gain": 3.0, "q": 0.7}},
    {"channel": 2, "fader": -12.0, "mute": false, "eq": {"band": 1, "freq": 100, "gain": 2.0, "q": 0.7}},
    {"channel": 3, "fader": -10.0, "mute": false}
  ],
  "aux_sends": [
    {"aux": 1, "channel": 1, "level": -6.0},
    {"aux": 1, "channel": 2, "level": -12.0}
  ],
  "fx_returns": [
    {"fx": 1, "return_level": -18.0},
    {"fx": 2, "return_level": -20.0}
  ],
  "monitor_mixes": [
    {"mix": 1, "channel": 1, "level": 0.0},
    {"mix": 1, "channel": 3, "level": -6.0}
  ]
}
```

### Complete Wireless Microphone Setup Checklist

```
PRE-SHOW WIRELESS CHECK
    □ Scan RF spectrum for interference
    □ Verify all transmitter battery levels > 50%
    □ Check antenna connections and placement
    □ Verify receiver lock on assigned frequencies
    □ Test each channel with audio check
    □ Set gain structure for each channel
    □ Verify encryption keys are loaded
    □ Check backup transmitter batteries
    □ Test handoff between primary and backup
    □ Log all frequency assignments

DURING SHOW
    □ Monitor RF signal strength continuously
    □ Check battery levels at intermission
    □ Monitor audio quality for dropouts
    □ Be ready to switch to backup frequency
    □ Log any interference incidents

POST-SHOW
    □ Return all transmitters to charging stations
    □ Log any frequency changes made
    □ Note any battery performance issues
    □ Clean and inspect all microphones
```

### Acoustic Treatment Reference

| Treatment Type | NRC | Frequency | Placement |
|---------------|-----|-----------|-----------|
| Absorption panel (2") | 0.85 | Mid-High | Walls, ceiling |
| Bass trap (4") | 0.90 | Low-Mid | Corners |
| Diffusion panel | N/A | Mid-High | Rear wall |
| Ceiling cloud | 0.80 | Mid-High | Above stage |
| Floor carpet | 0.30 | High | Audience area |
| Heavy curtains | 0.70 | Mid-High | Windows, walls |

### Console Scene Memory Layout

```
Scene 1:  Act 1 Scene 1 - Pre-show
Scene 2:  Act 1 Scene 2 - Opening number
Scene 3:  Act 1 Scene 3 - Dialogue
Scene 4:  Act 1 Scene 4 - Musical number
Scene 5:  Act 1 Scene 5 - Transition
...
Scene 15: Act 2 Scene 3 - Climax
Scene 16: Act 2 Scene 4 - Resolution
Scene 17: Act 2 Scene 5 - Finale
Scene 18: Act 2 Scene 6 - Curtain call

FX Scenes (Quick recall):
Scene 50: FX - Full reverb
Scene 51: FX - Plate reverb
Scene 52: FX - Delay throw
Scene 53: FX - Ambient wash
Scene 54: FX - Dry (no effects)
```

### Monitor Mix Optimization Guide

```
VOCALIST MONITOR MIX
    ├── Self (vocal): 0 dB
    ├── Band mix: -6 dB
    ├── Reverb return: -12 dB
    ├── Click track: -3 dB (if needed)
    └── Notes: Prioritize vocal clarity

GUITARIST MONITOR MIX
    ├── Self (guitar): 0 dB
    ├── Kick drum: -6 dB
    ├── Snare: -8 dB
    ├── Bass: -10 dB
    └── Notes: Needs rhythmic foundation

DRUMMER MONITOR MIX
    ├── Self (kick): 0 dB
    ├── Self (snare): 0 dB
    ├── Click track: 0 dB
    ├── Band mix: -6 dB
    └── Notes: Click is essential

ACTOR/SPEAKER MONITOR MIX
    ├── Self (vocal): 0 dB
    ├── Playback: -6 dB
    ├── Band: -12 dB
    └── Notes: Clear voice reproduction
```
```

### Monitor Mix Reference Levels

| Source | FOH Level | Monitor Level | IEM Level |
|--------|-----------|---------------|-----------|
| Lead Vocal | -6 dB | 0 dB | -3 dB |
| Backing Vocal | -12 dB | -6 dB | -9 dB |
| Acoustic Guitar | -10 dB | -4 dB | -6 dB |
| Electric Guitar | -8 dB | -2 dB | -4 dB |
| Bass | -6 dB | 0 dB | -2 dB |
| Drums | -4 dB | +2 dB | 0 dB |
| Keys | -10 dB | -4 dB | -6 dB |

### Dolby Atmos Object Configuration

```python
from sound_engineering import AtmosObject, AtmosBed

# Configure Atmos objects
objects = [
    AtmosObject(id=1, name="lead_vocal", position=(0.0, 0.0, 1.0), size=0.3, diffusion=0.5),
    AtmosObject(id=2, name="rain_effect", position=(0.3, -0.2, 0.8), size=0.8, diffusion=1.0),
    AtmosObject(id=3, name="thunder", position=(-0.5, 0.3, 0.5), size=1.0, diffusion=0.8),
]

# Configure Atmos bed
bed = AtmosBed(
    channels=["L", "R", "C", "LFE", "Ls", "Rs", "Lrs", "Rrs"],
    height_channels=["Ltf", "Rtf", "Ltb", "Rtb"],
)
```

### Troubleshooting Decision Tree

```
Feedback howl
    │
    ├── Identify feedback frequency → Use RTA
    ├── Apply notch filter at frequency → Parametric EQ
    ├── Reduce gain on offending channel → Check mic position
    ├── Check monitor angle → Aim away from mic
    ├── Engage HPF/LPF → Remove unused frequency range
    ├── Check room acoustics → Add absorption if needed
    └── Consider feedback suppressor → Adaptive notch filter

Wireless dropout
    │
    ├── Check RF signal strength → -70 dBm minimum
    ├── Check antenna placement → Line of sight to stage
    ├── Scan for interference → Find clean frequencies
    ├── Check intermodulation spacing → 300 kHz minimum
    ├── Check battery level → Replace if low
    ├── Check for physical obstructions → Metal, concrete
    └── Consider directional antennas → Directional for large venues

Audio latency in monitors
    │
    ├── Check buffer size → Reduce to 5ms minimum
    ├── Check DSP processing load → Reduce plugin count
    ├── Check network latency → Verify Dante/AES67 sync
    ├── Check cable length → Digital preferred over analog
    └── Use local monitor mixing → Reduce round-trip
```

### Performance Metrics

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Signal headroom | > 6 dB | 3-6 dB | < 3 dB |
| Wireless battery | > 20% | 10-20% | < 10% |
| Feedback margin | > 12 dB | 6-12 dB | < 6 dB |
| RT60 (theater) | 1.0-1.6s | 0.8-1.8s | < 0.8 or > 1.8s |
| STI (speech) | > 0.6 | 0.5-0.6 | < 0.5 |
| Monitor latency | < 5ms | 5-10ms | > 10ms |
| Scene recall time | < 100ms | 100-500ms | > 500ms |

### Wireless Microphone Battery Guide

| Battery Type | Capacity | Duration (Handheld) | Duration (Bodypack) |
|-------------|----------|-------------------|-------------------|
| AA Alkaline | 2800 mAh | 6-8 hours | 8-10 hours |
| AA Lithium | 3000 mAh | 8-10 hours | 10-12 hours |
| Rechargeable NiMH | 2500 mAh | 5-7 hours | 7-9 hours |
| Custom Li-ion | 5000 mAh | 10-14 hours | 12-16 hours |

### SPL Reference Levels

| Source | SPL (dB) | Description |
|--------|---------|-------------|
| Threshold of hearing | 0 | Barely audible |
| Quiet library | 30 | Whisper level |
| Normal conversation | 60 | Comfortable speech |
| Restaurant | 70-80 | Moderate noise |
| Concert (amplified) | 95-105 | Standard concert level |
| Concert (acoustic) | 85-95 | Orchestral dynamics |
| Rock concert | 105-115 | Maximum safe exposure |
| Pain threshold | 125 | Immediate damage risk |

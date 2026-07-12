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

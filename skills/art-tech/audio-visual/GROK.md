---
name: "audio-visual"
category: "art-tech"
version: "2.0.0"
tags: ["audio-visual", "vj", "live-visuals", "music-visualization", "projection", "dmx"]
---

# Audio-Visual

## Overview

Audio-visual synchronization toolkit for live performance, music visualization, VJ sets, and immersive installations. This module provides real-time audio analysis (FFT, beat detection, onset detection, key detection), audio-reactive visual generation, multi-output projection, DMX lighting control, and MIDI/OSC integration for live performance. Supports Ableton Link, Serato, and custom audio input with sub-frame synchronization accuracy.

## Core Capabilities

- **Audio Analysis**: Real-time FFT, spectral analysis, beat/onset detection, key/tempo detection, and loudness metering
- **Audio-Reactive Visuals**: Generate visual content that responds to audio frequency, amplitude, and rhythm
- **Multi-Output**: Synchronize visuals across multiple projectors and LED walls with genlock accuracy
- **DMX Control**: Send DMX512 commands for stage lighting synchronized to audio
- **MIDI/OSC Integration**: Map MIDI controllers and OSC messages to visual parameters
- **Performance Mode**: Low-latency, high-framerate output optimized for live performance
- **Preset System**: Save and recall visual presets with smooth crossfade transitions
- **Recording**: Record performance sets with audio for replay and post-production

## Usage

```python
from audio_visual import (
    AudioAnalyzer, VisualGenerator, DMXController, MIDI_Mapper, PerformanceEngine
)

# Audio analysis
analyzer = AudioAnalyzer(source="system_audio", fft_size=2048)
analysis = analyzer.analyze()
print(f"BPM: {analysis.tempo_bpm:.1f}")
print(f"Key: {analysis.key}")
print(f"Loudness: {analysis.loudness_lufs:.1f} LUFS")
print(f"Frequency bands: bass={analysis.bands.bass:.2f}, mid={analysis.bands.mid:.2f}, treble={analysis.bands.treble:.2f}")

# Visual generator
visual = VisualGenerator(resolution=(1920, 1080), output="ndi")
visual.set_mode("spectrum")
visual.set_color_palette([(255, 50, 50), (50, 100, 255), (50, 255, 100)])
visual.set_sensitivity(bass=1.5, mid=1.0, treble=0.8)

# DMX lighting
dmx = DMXController(port="/dev/ttyUSB0", universe=1)
dmx.set_channel(1, int(analysis.bands.bass * 255))  # Red = bass
dmx.set_channel(2, int(analysis.bands.mid * 255))    # Green = mid
dmx.set_channel(3, int(analysis.bands.treble * 255))  # Blue = treble
dmx.flush()

# MIDI mapping
midi = MIDI_Mapper()
midi.map_cc(1, "visual.brightness", min_val=0.0, max_val=1.0)
midi.map_cc(7, "visual.speed", min_val=0.1, max_val=3.0)
midi.map_note(60, "visual.preset_next")

# Performance engine
engine = PerformanceEngine(fps=60)
engine.add_analyzer(analyzer)
engine.add_visual(visual)
engine.add_dmx(dmx)
engine.add_midi(midi)
engine.start()
print(f"Performance running: {engine.is_running}")
```

## Best Practices

- Use FFT size of 2048 for good frequency resolution at 60fps — smaller for lower latency
- Apply smoothing (3-5 frame moving average) to FFT data for fluid visual responses
- Map bass to large, slow movements and treble to small, fast movements for natural feel
- Test DMX output at low brightness before connecting to venue lighting
- Use Ableton Link for tempo sync with other performers — it handles drift automatically
- Record your set with audio for post-production and social media content
- Create at least 3-5 visual presets per set for variety during performance
- Use NDI or Blackmagic for multi-projector output — HDMI splitters add latency
- Set frame rate to match projector refresh rate (60Hz, 120Hz, or 144Hz)
- Backup your performance configuration on USB before every gig

## Related Modules

- **generative-art** — Content generation for audio-reactive visuals
- **creative-coding** — Real-time visual programming for live performance
- **digital-installations** — Installation output for permanent venues
- **interactive-media** — Interactive audio-visual experiences
- **3d-rendering** — GPU-accelerated real-time rendering for performance

## Advanced Configuration

### Audio Analysis Advanced

```python
from audio_visual import AudioAnalyzer, AnalysisConfig, FrequencyBands

analysis_config = AnalysisConfig(
    source="system_audio",  # microphone, system_audio, file
    fft_size=4096,
    hop_size=1024,
    sample_rate=44100,
    window_function="hanning",
    frequency_bands=FrequencyBands(
        sub_bass=(20, 60),
        bass=(60, 250),
        low_mid=(250, 500),
        mid=(500, 2000),
        high_mid=(2000, 4000),
        presence=(4000, 6000),
        brilliance=(6000, 20000),
    ),
    onset_detection={
        "method": "spectral_flux",
        "threshold": 0.3,
        "min_interval_ms": 100,
    },
    beat_detection={
        "method": "comb_filter",
        "bpm_range": (60, 180),
        "confidence_threshold": 0.7,
    },
    key_detection={
        "method": "karaoke",
        "profile": "kt08",
    },
)

analyzer = AudioAnalyzer(config=analysis_config)

# Comprehensive analysis
analysis = analyzer.analyze()
print(f"Tempo: {analysis.tempo_bpm:.1f} BPM")
print(f"Key: {analysis.key} {analysis.mode}")
print(f"Loudness: {analysis.loudness_lufs:.1f} LUFS")
print(f"Dynamic Range: {analysis.dynamic_range_db:.1f} dB")
print(f"Spectral Centroid: {analysis.spectral_centroid:.1f} Hz")
print(f"Spectral Bandwidth: {analysis.spectral_bandwidth:.1f} Hz")
print(f"Spectral Rolloff: {analysis.spectral_rolloff:.1f} Hz")
print(f"Zero Crossing Rate: {analysis.zero_crossing_rate:.3f}")

# Frequency bands
for band_name, band_value in analysis.bands.items():
    print(f"  {band_name}: {band_value:.3f}")
```

### Visual Generator Advanced

```python
from audio_visual import VisualGenerator, VisualConfig, VisualMode

visual_config = VisualConfig(
    resolution=(1920, 1080),
    output="ndi",  # ndi, spout, syphon, blackmagic
    mode="spectrum",  # spectrum, waveform, spectrogram, particles, custom
    color_palette=[
        (255, 50, 50),    # Red
        (50, 100, 255),   # Blue
        (50, 255, 100),   # Green
        (255, 200, 50),   # Yellow
        (200, 50, 255),   # Purple
    ],
    sensitivity={
        "bass": 1.5,
        "mid": 1.0,
        "treble": 0.8,
        "overall": 1.2,
    },
    smoothing={
        "temporal": 0.7,
        "spectral": 0.5,
        "beat": 0.3,
    },
    effects={
        "bloom": {"enabled": True, "intensity": 0.3, "threshold": 0.8},
        "blur": {"enabled": True, "size": 2, "type": "gaussian"},
        "glitch": {"enabled": False, "intensity": 0.1},
        "rgb_shift": {"enabled": True, "offset": 2},
        "scanlines": {"enabled": False, "density": 100},
    },
)

visual = VisualGenerator(config=visual_config)

# Set visual parameters
visual.set_parameter("spectrum.color_by", "frequency")
visual.set_parameter("spectrum.height_scale", 2.0)
visual.set_parameter("spectrum.smoothing", 0.8)
visual.set_parameter("spectrum.min_db", -60)
visual.set_parameter("spectrum.max_db", 0)

# Audio-reactive mapping
visual.map_audio("bass", "spectrum.height_scale", min_val=1.0, max_val=3.0)
visual.map_audio("beat", "effects.bloom.intensity", min_val=0.0, max_val=1.0)
```

### DMX Control Advanced

```python
from audio_visual import DMXController, DMXConfig, LightingScene

dmx_config = DMXConfig(
    interface="enttec_usb_pro",  # enttec, art-net, sACN
    universe=1,
    start_channel=1,
    refresh_rate=40,  # Hz
    protocol="dmx512",
)

dmx = DMXController(config=dmx_config)

# Create lighting scenes
scenes = {
    "bass_heavy": LightingScene()
        .set_channel(1, "red", audio.bands.bass * 255)
        .set_channel(2, "green", 0)
        .set_channel(3, "blue", 0)
        .set_channel(4, "white", 0)
        .set_channel(5, "dimmer", 255)
        .set_channel(6, "strobe", 0),
    
    "treble_bright": LightingScene()
        .set_channel(1, "red", 0)
        .set_channel(2, "green", audio.bands.treble * 255)
        .set_channel(3, "blue", audio.bands.treble * 255)
        .set_channel(4, "white", audio.bands.treble * 255)
        .set_channel(5, "dimmer", 200)
        .set_channel(6, "strobe", 0),
    
    "beat_flash": LightingScene()
        .set_channel(1, "red", 255)
        .set_channel(2, "green", 255)
        .set_channel(3, "blue", 255)
        .set_channel(4, "white", 255)
        .set_channel(5, "dimmer", 255)
        .set_channel(6, "strobe", 255),
}

# Audio-reactive lighting
@analyzer.on_beat
def on_beat(strength):
    if strength > 0.8:
        dmx.apply_scene(scenes["beat_flash"])
    elif audio.bands.bass > 0.7:
        dmx.apply_scene(scenes["bass_heavy"])
    else:
        dmx.apply_scene(scenes["treble_bright"])
    dmx.flush()
```

### MIDI/OSC Integration

```python
from audio_visual import MIDI_Mapper, OSC_Mapper, ControllerMapping

midi = MIDI_Mapper(
    device="Virtual MIDI Port",
    channel=1,
)

osc = OSC_Mapper(
    target_ip="192.168.1.100",
    target_port=9000,
    local_port=9001,
)

# Map MIDI controllers
midi.map_cc(1, "visual.brightness", min_val=0.0, max_val=1.0)
midi.map_cc(7, "visual.speed", min_val=0.1, max_val=3.0)
midi.map_cc(10, "visual.color_shift", min_val=0.0, max_val=360.0)
midi.map_note(60, "visual.preset_next")
midi.map_note(61, "visual.preset_prev")
midi.map_note(62, "visual.mode_cycle")

# Map OSC messages
osc.map_address("/visual/brightness", "visual.brightness")
osc.map_address("/visual/preset", "visual.preset_select")

# Handle MIDI input
@midi.on_cc
def on_cc(channel, cc, value):
    print(f"MIDI CC: channel={channel}, cc={cc}, value={value}")

@midi.on_note
def on_note(channel, note, velocity):
    print(f"MIDI Note: channel={channel}, note={note}, velocity={velocity}")
```

## Architecture Patterns

### Audio-Visual Pipeline Architecture

```
+------------------------------------------------------------------+
|                Audio-Visual Pipeline Architecture                 |
+------------------------------------------------------------------+
|                                                                  |
|  +----------------+    +----------------+    +----------------+  |
|  |  Audio Input   |    |  Analysis      |    |  Visual Output |  |
|  |  Layer         |    |  Engine        |    |  Layer         |  |
|  |                |    |                |    |                |  |
|  |  Microphone    |    |  FFT           |    |  Projector     |  |
|  |  System Audio  |<-->|  Beat Detect   |<-->|  LED Wall      |  |
|  |  File Input    |    |  Onset Detect  |    |  Screen        |  |
|  |  MIDI/OSC      |    |  Key Detect    |    |  NDI Output    |  |
|  +-------+--------+    +-------+--------+    +-------+--------+  |
|          |                    |                     |             |
|          v                    v                     v             |
|  +----------------------------------------------------------------+
|  |                    Mapping Engine                              |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  Audio-to-   |  |  Parameter   |  |  Preset      |          |
|  |  |  Visual      |  |  Smoothing   |  |  Manager     |          |
|  |  |  Mapping     |  |              |  |              |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
|                              |                                    |
|                              v                                    |
|  +----------------------------------------------------------------+
|  |                    Control Layer                               |
|  |  +--------------+  +--------------+  +--------------+          |
|  |  |  MIDI        |  |  OSC         |  |  DMX         |          |
|  |  |  Controller  |  |  Controller  |  |  Controller  |          |
|  |  +--------------+  +--------------+  +--------------+          |
|  +----------------------------------------------------------------+
+------------------------------------------------------------------+
```

### Beat Detection Flow

```
Audio Stream
        |
        v
+-------------------+
|  FFT Analysis     |  Compute spectrum
+-------------------+
        |
        v
+-------------------+
|  Spectral Flux    |  Calculate flux
+-------------------+
        |
        v
+-------------------+
|  Peak Detection   |  Find peaks
+-------------------+
        |
        v
+-------------------+
|  Interval Calc    |  Calculate intervals
+-------------------+
        |
        v
+-------------------+
|  BPM Estimation   |  Estimate tempo
+-------------------+
        |
        v
+-------------------+
|  Beat Confirmation|  Confirm beat
+-------------------+
```

### Multi-Output Synchronization

```
Multi-Output Architecture
        |
        v
+-------------------+
|  Frame Buffer     |  Render frame
+-------------------+
        |
        v
+-------------------+
|  Sync Signal      |  Generate sync
+-------------------+
        |
        v
+-------------------+
|  Output Router    |  Route to outputs
+-------------------+
        |
        +-------------------+-------------------+
        |                   |                   |
        v                   v                   v
+-------------------+ +-------------------+ +-------------------+
|  NDI Output       | |  Blackmagic       | |  Spout/Syphon     |
|  (Network)        | |  (SDI/HDMI)       | |  (Local)          |
+-------------------+ +-------------------+ +-------------------+
```

## Integration Guide

### Ableton Link Integration

```python
from audio_visual import AbletonLink, LinkConfig

link_config = LinkConfig(
    tempo=120.0,
    quantum=4.0,
    start_stop_sync=True,
)

link = AbletonLink(config=link_config)

# Start Link session
link.start()

# Get Link info
info = link.get_info()
print(f"Tempo: {info.tempo:.1f} BPM")
print(f"Peers: {info.peer_count}")
print(f"Phase: {info.phase:.2f}")
print(f"Beat: {info.beat:.2f}")

# Sync visuals to Link
@link.on_beat
def on_beat(beat, phase):
    if phase == 0.0:
        # Trigger on downbeat
        visual.trigger_preset("downbeat")
```

### Serato Integration

```python
from audio_visual import SeratoIntegration, SeratoConfig

serato = SeratoIntegration(config=SeratoConfig(
    host="localhost",
    port=8000,
    protocol="osc",
))

# Get track info
track = serato.get_current_track()
print(f"Track: {track.title}")
print(f"Artist: {track.artist}")
print(f"BPM: {track.bpm}")
print(f"Key: {track.key}")

# Get playback info
playback = serato.get_playback_info()
print(f"Playing: {playback.is_playing}")
print(f"Position: {playback.position_ms}")
print(f"Duration: {playback.duration_ms}")
```

### Custom Audio Input

```python
from audio_visual import CustomAudioInput, AudioBuffer

audio_input = CustomAudioInput(
    sample_rate=44100,
    buffer_size=2048,
    channels=2,
)

# Process custom audio
@audio_input.on_audio
def on_audio(buffer: AudioBuffer):
    # Analyze buffer
    spectrum = buffer.get_spectrum()
    onset = buffer.get_onset()
    
    # Update visuals
    if onset:
        visual.trigger_effect("flash")
    
    visual.update_spectrum(spectrum)
```

## Performance Optimization

### Audio Processing Optimization

```python
from audio_visual import AudioOptimizer, PerformanceConfig

optimizer = AudioOptimizer(
    config=PerformanceConfig(
        target_latency_ms=10,
        buffer_size=512,
        hop_size=256,
    ),
    optimizations={
        "fft_optimization": True,
        "simd_instructions": True,
        "thread_pool": True,
        "cache_friendly": True,
    },
)

# Monitor performance
stats = optimizer.get_stats()
print(f"Latency: {stats.latency_ms:.2f}ms")
print(f"CPU usage: {stats.cpu_usage_pct:.1f}%")
print(f"Buffer underruns: {stats.underruns}")
```

### Visual Rendering Optimization

```python
from audio_visual import VisualOptimizer, RenderConfig

visual_opt = VisualOptimizer(
    config=RenderConfig(
        target_fps=60,
        resolution_scale=1.0,
        vsync=True,
    ),
    optimizations={
        "gpu_acceleration": True,
        "shader_optimization": True,
        "batch_rendering": True,
        "texture_streaming": True,
    },
)

# Monitor rendering
stats = visual_opt.get_stats()
print(f"Frame time: {stats.frame_time_ms:.2f}ms")
print(f"GPU usage: {stats.gpu_usage_pct:.1f}%")
print(f"Draw calls: {stats.draw_calls}")
```

## Security Considerations

### Network Security

```python
from audio_visual import NetworkSecurity, SecurityConfig

security = NetworkSecurity(
    config=SecurityConfig(
        encryption="tls",
        authentication="token",
        rate_limiting=True,
        max_connections=10,
    },
)

# Secure NDI output
ndi_output = security.create_secure_ndi("My Visuals")

# Secure MIDI/OSC
midi = security.create_secure_midi(device="Virtual Port")
osc = security.create_secure_osc(port=9000)
```

### Content Protection

```python
from audio_visual import ContentProtection

protection = ContentProtection(
    watermark=True,
    watermark_position="bottom_right",
    watermark_opacity=0.3,
    copy_protection=True,
)

# Apply watermark
protected_frame = protection.apply_watermark(frame, "Artist Name")
```

## Troubleshooting Guide

| Issue | Symptoms | Solution |
|-------|----------|----------|
| **Audio latency** | Delayed response | Reduce buffer size, check drivers |
| **Beat detection errors** | Wrong BPM | Adjust threshold, check audio quality |
| **DMX failures** | Lighting not responding | Check cable, verify channel mapping |
| **Visual stuttering** | Jerky visuals | Reduce complexity, check GPU |
| **MIDI mapping issues** | Controls not working | Verify mapping, check MIDI device |
| **NDI network issues** | No output | Check network, verify NDI tools |
| **Sync issues** | Audio out of sync | Adjust buffer, check clock sync |

## API Reference

```python
class AudioAnalyzer:
    """Analyze audio input."""
    
    def __init__(self, source: str, fft_size: int = 2048):
        """Initialize analyzer."""
        
    def analyze(self) -> AudioAnalysis:
        """Analyze current audio."""

class VisualGenerator:
    """Generate visuals from audio."""
    
    def __init__(self, resolution: tuple, output: str):
        """Initialize visual generator."""
        
    def set_mode(self, mode: str) -> None:
        """Set visual mode."""

class DMXController:
    """Control DMX lighting."""
    
    def __init__(self, interface: str, universe: int):
        """Initialize DMX controller."""
        
    def set_channel(self, channel: int, value: int) -> None:
        """Set DMX channel value."""

class MIDI_Mapper:
    """Map MIDI controls."""
    
    def __init__(self, device: str, channel: int = 1):
        """Initialize MIDI mapper."""
        
    def map_cc(self, cc: int, target: str, min_val: float, max_val: float) -> None:
        """Map MIDI CC to parameter."""
```

## Data Models

```python
@dataclass
class AudioAnalysis:
    """Audio analysis result."""
    tempo_bpm: float
    key: str
    mode: str
    loudness_lufs: float
    dynamic_range_db: float
    spectral_centroid: float
    spectral_bandwidth: float
    spectral_rolloff: float
    zero_crossing_rate: float
    bands: dict

@dataclass
class Beat:
    """Beat information."""
    timestamp: float
    strength: float
    bpm: float
    confidence: float

@dataclass
class VisualPreset:
    """Visual preset."""
    name: str
    mode: str
    parameters: dict
    color_palette: List[tuple]

@dataclass
class DMXScene:
    """DMX lighting scene."""
    name: str
    channels: Dict[int, int]
    fade_time_ms: int
```

## Deployment Guide

### Performance Setup

```python
from audio_visual import PerformanceSetup, SetupConfig

setup_config = SetupConfig(
    name="Live Performance",
    audio_input="system_audio",
    visual_output="ndi",
    dmx_interface="enttec_usb_pro",
    midi_device="Virtual MIDI Port",
    resolution=(1920, 1080),
    framerate=60,
)

setup = PerformanceSetup(config=setup_config)
setup.initialize()
setup.start()
```

## Monitoring & Observability

```python
from audio_visual import PerformanceMonitor, Metrics

monitor = PerformanceMonitor(
    metrics=Metrics(
        tracks=[
            "audio_latency",
            "visual_fps",
            "dmx_refresh_rate",
            "midi_messages_per_second",
        ],
        sample_rate=1.0,
    ),
    alerts={
        "audio_latency_high": {"threshold": 20, "action": "notify"},
        "visual_fps_low": {"threshold": 55, "action": "notify"},
    },
)

monitor.start()
```

## Testing Strategy

```python
import pytest
from audio_visual import AudioAnalyzer, VisualGenerator

class TestAudioAnalysis:
    def test_beat_detection(self):
        analyzer = AudioAnalyzer(source="file", file="test_beat.wav")
        analysis = analyzer.analyze()
        assert 110 < analysis.tempo_bpm < 130

class TestVisualGenerator:
    def test_mode_switching(self):
        visual = VisualGenerator(resolution=(1920, 1080), output="ndi")
        visual.set_mode("spectrum")
        assert visual.mode == "spectrum"
```

## Versioning & Migration

| Version | Changes | Breaking |
|---------|---------|----------|
| 2.0.0 | Added NDI output, improved beat detection | Yes |
| 1.5.0 | Added DMX control | No |
| 1.0.0 | Initial release | N/A |

## Glossary

| Term | Definition |
|------|------------|
| **FFT** | Fast Fourier Transform |
| **BPM** | Beats Per Minute |
| **LUFS** | Loudness Units Full Scale |
| **NDI** | Network Device Interface |
| **DMX** | Digital Multiplex |
| **MIDI** | Musical Instrument Digital Interface |
| **OSC** | Open Sound Control |
| **Spectral Flux** | Measure of spectrum change |

## Changelog

### 2.0.0 (2024-01-15)
- Added NDI output
- Improved beat detection accuracy
- Added Ableton Link support

### 1.5.0 (2023-10-01)
- Added DMX control
- Added MIDI mapping

### 1.0.0 (2023-06-01)
- Initial release

## Contributing Guidelines

```bash
git clone https://github.com/company/audio-visual.git
cd audio-visual
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

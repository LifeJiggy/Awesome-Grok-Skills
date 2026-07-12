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

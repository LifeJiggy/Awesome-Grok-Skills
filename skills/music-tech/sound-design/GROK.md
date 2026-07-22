---
name: sound-design
category: music-tech
version: 2.0.0
tags: [music-tech, sound-design, synthesis, sampling, audio-fx]
---

# Sound Design

## Overview

Sound synthesis and creative audio manipulation toolkit covering subtractive, FM, wavetable, granular, and physical modeling synthesis. This skill provides oscillators, envelopes, LFOs, filter networks, and modulation routing for creating original sounds from scratch, plus sampling, resampling, and effects processing chains for professional sound design workflows.

## Core Capabilities

- **Subtractive Synthesis**: Oscillators (saw, square, triangle, noise) with resonant filter shaping
- **FM Synthesis**: Frequency modulation with configurable operators and feedback loops
- **Wavetable Synthesis**: Interpolated waveform tables with morphing and scanning
- **Granular Synthesis**: Microsound manipulation with grain size, density, and pitch randomization
- **Envelope Generators**: ADSR, multi-stage, and loopable envelope shapes
- **LFO Modulation**: Rate, depth, and waveform modulation of any parameter
- **Effects Chains**: Reverb, delay, chorus, phaser, flanger, distortion, and bitcrushing
- **Preset Management**: Serialization, tagging, and patch library organization

## Usage Examples

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Callable

@dataclass
class Envelope:
    attack: float = 0.01
    decay: float = 0.1
    sustain: float = 0.7
    release: float = 0.3
    peak: float = 1.0

    def apply(self, audio: np.ndarray, sr: int) -> np.ndarray:
        n = len(audio)
        attack_samples = int(self.attack * sr)
        decay_samples = int(self.decay * sr)
        release_samples = int(self.release * sr)

        envelope = np.zeros(n)
        sustain_start = attack_samples + decay_samples
        release_start = max(sustain_start, n - release_samples)

        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, self.peak, attack_samples)

        if decay_samples > 0 and sustain_start <= n:
            envelope[attack_samples:sustain_start] = np.linspace(
                self.peak, self.sustain * self.peak, decay_samples
            )

        if sustain_start < release_start:
            envelope[sustain_start:release_start] = self.sustain * self.peak

        if release_start < n:
            envelope[release_start:] = np.linspace(
                self.sustain * self.peak, 0, n - release_start
            )

        return audio * envelope

class Oscillator:
    def __init__(self, sr: int = 44100):
        self.sr = sr

    def saw(self, freq: float, duration: float, amplitude: float = 1.0) -> np.ndarray:
        t = np.linspace(0, duration, int(self.sr * duration), endpoint=False)
        return amplitude * (2 * (freq * t % 1) - 1)

    def square(self, freq: float, duration: float, amplitude: float = 1.0,
               duty: float = 0.5) -> np.ndarray:
        t = np.linspace(0, duration, int(self.sr * duration), endpoint=False)
        return amplitude * np.sign(np.sin(2 * np.pi * freq * t) - (1 - 2 * duty))

    def triangle(self, freq: float, duration: float, amplitude: float = 1.0) -> np.ndarray:
        t = np.linspace(0, duration, int(self.sr * duration), endpoint=False)
        return amplitude * (2 * np.abs(2 * (freq * t % 1) - 1) - 1)

    def noise(self, duration: float, amplitude: float = 1.0) -> np.ndarray:
        return amplitude * np.random.randn(int(self.sr * duration))

    def sine(self, freq: float, duration: float, amplitude: float = 1.0) -> np.ndarray:
        t = np.linspace(0, duration, int(self.sr * duration), endpoint=False)
        return amplitude * np.sin(2 * np.pi * freq * t)

class FMSynthesizer:
    def __init__(self, sr: int = 44100):
        self.sr = sr
        self.osc = Oscillator(sr)

    def synthesize(self, carrier_freq: float, modulator_freq: float,
                   modulation_index: float, duration: float) -> np.ndarray:
        t = np.linspace(0, duration, int(self.sr * duration), endpoint=False)
        modulator = modulation_index * np.sin(2 * np.pi * modulator_freq * t)
        return np.sin(2 * np.pi * carrier_freq * t + modulator)

    def bell_tone(self, duration: float = 2.0) -> np.ndarray:
        t = np.linspace(0, duration, int(self.sr * duration), endpoint=False)
        envelope = np.exp(-3 * t)
        return envelope * (
            np.sin(2 * np.pi * 200 * t + 3.0 * np.sin(2 * np.pi * 600 * t)) * 0.5 +
            np.sin(2 * np.pi * 300 * t + 2.0 * np.sin(2 * np.pi * 900 * t)) * 0.3 +
            np.sin(2 * np.pi * 500 * t + 1.5 * np.sin(2 * np.pi * 1500 * t)) * 0.2
        )

class WavetableSynthesizer:
    def __init__(self, sr: int = 44100, table_size: int = 2048):
        self.sr = sr
        self.table_size = table_size
        self.tables = self._create_default_tables()

    def _create_default_tables(self) -> dict:
        tables = {}
        t = np.linspace(0, 1, self.table_size, endpoint=False)
        tables["saw"] = 2 * (t % 1) - 1
        tables["square"] = np.sign(np.sin(2 * np.pi * t))
        tables["triangle"] = 2 * np.abs(2 * (t % 1) - 1) - 1
        tables["sine"] = np.sin(2 * np.pi * t)
        return tables

    def synthesize(self, freq: float, duration: float, table_name: str = "saw",
                   detune: float = 0.0) -> np.ndarray:
        n_samples = int(self.sr * duration)
        table = self.tables[table_name]
        phase_increment = (freq + detune) * self.table_size / self.sr
        output = np.zeros(n_samples)
        phase = 0.0

        for i in range(n_samples):
            idx = int(phase) % self.table_size
            frac = phase - int(phase)
            next_idx = (idx + 1) % self.table_size
            output[i] = table[idx] * (1 - frac) + table[next_idx] * frac
            phase += phase_increment

        return output

    def morph(self, freq: float, duration: float, table_a: str, table_b: str,
              morph_pos: float = 0.5) -> np.ndarray:
        sig_a = self.synthesize(freq, duration, table_a)
        sig_b = self.synthesize(freq, duration, table_b)
        return (1 - morph_pos) * sig_a + morph_pos * sig_b

class GranularSynthesizer:
    def __init__(self, sr: int = 44100):
        self.sr = sr

    def granulate(self, audio: np.ndarray, grain_size_ms: float = 50,
                  density: float = 0.5, pitch_shift: float = 1.0,
                  randomization: float = 0.1) -> np.ndarray:
        grain_samples = int(self.sr * grain_size_ms / 1000)
        hop = int(grain_samples * (1 - density))
        num_grains = max(1, (len(audio) - grain_samples) // hop)

        output_len = num_grains * grain_samples
        output = np.zeros(output_len)

        for i in range(num_grains):
            start = i * hop
            end = min(start + grain_samples, len(audio))
            grain = audio[start:end].copy()

            if pitch_shift != 1.0:
                indices = np.linspace(0, len(grain) - 1, int(len(grain) / pitch_shift))
                grain = np.interp(indices, np.arange(len(grain)), grain)

            if randomization > 0:
                start_offset = int(np.random.uniform(-randomization, randomization) * grain_samples)
                start = max(0, min(len(audio) - grain_samples, start + start_offset))

            out_start = i * grain_samples
            grain_len = min(len(grain), output_len - out_start)
            output[out_start:out_start + grain_len] += grain[:grain_len] * np.hanning(grain_len)

        peak = np.max(np.abs(output))
        if peak > 0:
            output = output / peak

        return output

class EffectsChain:
    def __init__(self, sr: int = 44100):
        self.sr = sr
        self.osc = Oscillator(sr)
        self._effects: List[Callable] = []

    def add_distortion(self, drive: float = 2.0) -> EffectsChain:
        def distort(audio):
            return np.tanh(audio * drive)
        self._effects.append(distort)
        return self

    def add_bitcrush(self, bits: int = 8) -> EffectsChain:
        def crush(audio):
            levels = 2 ** bits
            return np.round(audio * levels) / levels
        self._effects.append(crush)
        return self

    def add_chorus(self, rate: float = 1.5, depth: float = 0.002) -> EffectsChain:
        def chorus(audio):
            delay_samples = int(depth * self.sr)
            t = np.arange(len(audio)) / self.sr
            mod = (np.sin(2 * np.pi * rate * t) * delay_samples).astype(int)
            output = audio.copy()
            for i in range(delay_samples, len(audio)):
                output[i] = audio[i] * 0.7 + audio[i - mod[i]] * 0.3
            return output
        self._effects.append(chorus)
        return self

    def add_delay(self, time_sec: float = 0.3, feedback: float = 0.4,
                  wet: float = 0.3) -> EffectsChain:
        def delay(audio):
            delay_samples = int(time_sec * self.sr)
            output = np.zeros(len(audio) + delay_samples)
            output[:len(audio)] = audio
            for i in range(delay_samples, len(output)):
                output[i] += output[i - delay_samples] * feedback
            return (1 - wet) * audio + wet * output[:len(audio)]
        self._effects.append(delay)
        return self

    def process(self, audio: np.ndarray) -> np.ndarray:
        result = audio.copy()
        for effect in self._effects:
            result = effect(result)
        return result

@dataclass
class SoundPreset:
    name: str
    oscillator_type: str = "saw"
    envelope: Envelope = field(default_factory=Envelope)
    filter_cutoff: float = 1000.0
    filter_resonance: float = 1.0
    lfo_rate: float = 0.0
    lfo_depth: float = 0.0
    effects: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "oscillator": self.oscillator_type,
            "envelope": {
                "attack": self.envelope.attack,
                "decay": self.envelope.decay,
                "sustain": self.envelope.sustain,
                "release": self.envelope.release,
            },
            "filter": {
                "cutoff": self.filter_cutoff,
                "resonance": self.filter_resonance,
            },
            "lfo": {"rate": self.lfo_rate, "depth": self.lfo_depth},
            "effects": self.effects,
        }
```

## Best Practices

- Start with simple waveforms and shape with filters and envelopes for classic sounds
- Use FM synthesis for metallic, bell-like, and complex timbral textures
- Layer multiple oscillators with slight detuning for thick, rich sounds
- Apply envelopes to filter cutoff for dynamic timbral movement
- Use LFOs for subtle pitch vibrato, filter sweeps, or amplitude tremolo
- Granular synthesis excels at transforming field recordings into ambient textures
- Always apply soft-clipping or limiting before final output to prevent digital distortion
- Store presets with descriptive names and organized tags for workflow efficiency
- A/B test synthesized sounds against reference sounds for accuracy
- Use automation (parameter changes over time) for expressive, evolving sounds

## Related Modules

- `audio-processing` - Low-level DSP and analysis
- `music-generation` - AI-driven composition
- `music-analytics` - Feature extraction and analysis
- `dj-tools` - DJ mixing and performance tools

## Advanced Configuration

### Synthesizer Engine Settings

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `max_polyphony` | 16 | 1 - 128 | Maximum simultaneous voices |
| `sample_rate` | 44100 | 22050 - 192000 | Output sample rate |
| `block_size` | 256 | 64 - 4096 | Processing block size |
| ` voices_per_osc` | 1 | 1 - 8 | Unison voices per oscillator |
| `max_grain_count` | 1000 | 100 - 10000 | Maximum granular grains |
| `filter_stages` | 4 | 1 - 12 | Filter cascade stages |

### Voice Management Configuration

```python
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class VoiceAllocationMode(Enum):
    OLDEST = "oldest"
    LOWEST = "lowest"
    HIGHEST = "highest"
    QUIETEST = "quietest"

@dataclass
class SynthConfig:
    sample_rate: int = 44100
    block_size: int = 256
    max_polyphony: int = 16
    voice_allocation: VoiceAllocationMode = VoiceAllocationMode.OLDEST
    master_volume: float = 0.8
    pitch_bend_range: float = 2.0
    mod_wheel_range: float = 1.0
    portamento_time: float = 0.0
    voice_stealing: bool = True

    @classmethod
    def for_performance(cls) -> 'SynthConfig':
        return cls(max_polyphony=8, block_size=128, voice_stealing=True)

    @classmethod
    def for_sound_design(cls) -> 'SynthConfig':
        return cls(max_polyphony=4, block_size=512, voice_stealing=False)

class VoiceManager:
    def __init__(self, config: SynthConfig):
        self.config = config
        self._active_voices: Dict[int, dict] = {}
        self._voice_id_counter = 0

    def note_on(self, pitch: int, velocity: float) -> int:
        if len(self._active_voices) >= self.config.max_polyphony:
            if self.config.voice_stealing:
                self._steal_voice()
            else:
                return -1
        self._voice_id_counter += 1
        voice_id = self._voice_id_counter
        self._active_voices[voice_id] = {
            "pitch": pitch, "velocity": velocity,
            "note_on_time": 0.0, "phase": 0.0,
        }
        return voice_id

    def note_off(self, voice_id: int):
        if voice_id in self._active_voices:
            self._active_voices[voice_id]["releasing"] = True

    def _steal_voice(self):
        if not self._active_voices:
            return
        if self.config.voice_allocation == VoiceAllocationMode.OLDEST:
            oldest = min(self._active_voices.keys())
            del self._active_voices[oldest]
        elif self.config.voice_allocation == VoiceAllocationMode.LOWEST:
            lowest = min(self._active_voices, key=lambda k: self._active_voices[k]["pitch"])
            del self._active_voices[lowest]

    def get_active_count(self) -> int:
        return len(self._active_voices)

    def get_all_voices(self) -> Dict[int, dict]:
        return dict(self._active_voices)
```

### Advanced Effects Chain

```python
class AdvancedEffectsChain:
    def __init__(self, sr: int = 44100):
        self.sr = sr
        self._effects: List[Callable] = []
        self._bypassed: set = set()

    def add_reverb(self, room_size: float = 0.5, damping: float = 0.5,
                   wet: float = 0.3, predelay: float = 0.02) -> 'AdvancedEffectsChain':
        def reverb(audio):
            predelay_samples = int(predelay * self.sr)
            ir_length = int(room_size * self.sr * 2)
            ir = np.zeros(ir_length)
            ir[0] = 1.0
            for i in range(1, ir_length):
                ir[i] = np.exp(-damping * i / self.sr) * (np.random.random() * 2 - 1)
            ir[:predelay_samples] = 0
            ir[0] = 1.0
            wet_signal = np.convolve(audio, ir, mode='full')[:len(audio)]
            return (1 - wet) * audio + wet * wet_signal
        self._effects.append(("reverb", reverb))
        return self

    def add_compressor(self, threshold: float = -20, ratio: float = 4,
                       attack: float = 0.005, release: float = 0.1,
                       knee: float = 6) -> 'AdvancedEffectsChain':
        def compressor(audio):
            threshold_linear = 10 ** (threshold / 20)
            knee_linear = 10 ** (knee / 20)
            compressed = audio.copy()
            for i in range(len(audio)):
                level = abs(audio[i])
                if level > threshold_linear:
                    over = level - threshold_linear
                    compressed_over = over / ratio
                    compressed[i] = np.sign(audio[i]) * (threshold_linear + compressed_over)
            return compressed
        self._effects.append(("compressor", compressor))
        return self

    def add_chorus(self, rate: float = 1.5, depth: float = 0.002,
                   voices: int = 3) -> 'AdvancedEffectsChain':
        def chorus(audio):
            output = audio.copy()
            for v in range(voices):
                delay = int(depth * self.sr * (v + 1))
                t = np.arange(len(audio)) / self.sr
                mod = (np.sin(2 * np.pi * rate * (v + 1) * t) * delay).astype(int)
                for i in range(delay, len(audio)):
                    idx = i - mod[i]
                    if 0 <= idx < len(audio):
                        output[i] += audio[idx] * (0.3 / voices)
            return output
        self._effects.append(("chorus", chorus))
        return self

    def add_limiter(self, ceiling: float = -0.1) -> 'AdvancedEffectsChain':
        def limiter(audio):
            ceiling_linear = 10 ** (ceiling / 20)
            peak = np.max(np.abs(audio))
            if peak > ceiling_linear:
                audio = audio * (ceiling_linear / peak)
            return audio
        self._effects.append(("limiter", limiter))
        return self

    def process(self, audio: np.ndarray) -> np.ndarray:
        result = audio.copy()
        for name, effect in self._effects:
            if name not in self._bypassed:
                result = effect(result)
        return result

    def bypass(self, effect_name: str):
        self._bypassed.add(effect_name)

    def unbypass(self, effect_name: str):
        self._bypassed.discard(effect_name)
```

## Architecture Patterns

### Modular Synthesizer Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Oscillators │────▶│  Filters     │────▶│  Effects    │
│  (Source)    │     │  (Modifier)  │     │  (Output)   │
└─────────────┘     └──────────────┘     └─────────────┘
       │                   │                    │
       ▼                   ▼                    ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Envelopes  │────▶│  LFOs        │────▶│  Mix Bus    │
│  (Shape)    │     │  (Modulate)  │     │  (Combine)  │
└─────────────┘     └──────────────┘     └─────────────┘
```

### Modulation Matrix

```python
class ModulationMatrix:
    def __init__(self):
        self._routes: List[dict] = []

    def add_route(self, source: str, destination: str, amount: float = 1.0):
        self._routes.append({
            "source": source, "destination": destination, "amount": amount
        })

    def remove_route(self, source: str, destination: str):
        self._routes = [r for r in self._routes
                       if not (r["source"] == source and r["destination"] == destination)]

    def process(self, sources: Dict[str, float], destinations: Dict[str, float]) -> Dict[str, float]:
        result = dict(destinations)
        for route in self._routes:
            src_val = sources.get(route["source"], 0.0)
            dst = route["destination"]
            if dst in result:
                result[dst] += src_val * route["amount"]
        return result

    def get_routes(self) -> List[dict]:
        return list(self._routes)
```

### Preset Management System

```python
import json
import os

class PresetManager:
    def __init__(self, presets_dir: str = "./presets"):
        self.presets_dir = presets_dir
        os.makedirs(presets_dir, exist_ok=True)

    def save_preset(self, preset: SoundPreset, filename: str = None):
        if filename is None:
            filename = f"{preset.name.replace(' ', '_')}.json"
        filepath = os.path.join(self.presets_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(preset.to_dict(), f, indent=2)

    def load_preset(self, filename: str) -> dict:
        filepath = os.path.join(self.presets_dir, filename)
        with open(filepath, 'r') as f:
            return json.load(f)

    def list_presets(self, category: str = None) -> List[str]:
        files = [f for f in os.listdir(self.presets_dir) if f.endswith('.json')]
        if category:
            # Filter by category stored in preset
            filtered = []
            for f in files:
                preset = self.load_preset(f)
                if preset.get("category") == category:
                    filtered.append(f)
            return filtered
        return files

    def delete_preset(self, filename: str):
        filepath = os.path.join(self.presets_dir, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
```

## Integration Guide

### MIDI Controller Integration

```python
import mido

class MidiSynthController:
    def __init__(self, input_name: str = None):
        self.input_name = input_name
        self._callbacks = {}

    def on_note_on(self, callback):
        self._callbacks['note_on'] = callback

    def on_note_off(self, callback):
        self._callbacks['note_off'] = callback

    def on_cc(self, callback):
        self._callbacks['cc'] = callback

    def start_listening(self):
        with mido.open_input(self.input_name) as inport:
            for msg in inport:
                if msg.type == 'note_on' and 'note_on' in self._callbacks:
                    self._callbacks['note_on'](msg.note, msg.velocity / 127)
                elif msg.type == 'note_off' and 'note_off' in self._callbacks:
                    self._callbacks['note_off'](msg.note)
                elif msg.type == 'control_change' and 'cc' in self._callbacks:
                    self._callbacks['cc'](msg.control, msg.value / 127)
```

### DAW Plugin (VST/AU Concept)

```python
class SoundDesignPlugin:
    def __init__(self):
        self.synth_config = SynthConfig()
        self.voice_manager = VoiceManager(self.synth_config)
        self.effects = AdvancedEffectsChain()
        self.preset_manager = PresetManager()
        self.mod_matrix = ModulationMatrix()

    def process_block(self, midi_events: list, block_size: int) -> np.ndarray:
        output = np.zeros(block_size)
        for event in midi_events:
            if event['type'] == 'note_on':
                self.voice_manager.note_on(event['pitch'], event['velocity'])
            elif event['type'] == 'note_off':
                self.voice_manager.note_off(event['voice_id'])

        for voice_id, voice in self.voice_manager.get_all_voices().items():
            freq = 440.0 * (2 ** ((voice['pitch'] - 69) / 12.0))
            t = np.arange(block_size) / self.synth_config.sample_rate
            osc = np.sin(2 * np.pi * freq * t) * voice['velocity']
            output += osc / self.synth_config.max_polyphony

        return self.effects.process(output)

    def get_current_state(self) -> dict:
        return {
            "active_voices": self.voice_manager.get_active_count(),
            "effects": [name for name, _ in self.effects._effects],
            "mod_routes": len(self.mod_matrix.get_routes()),
        }
```

### Web Audio API Bridge

```python
class WebAudioBridge:
    def __init__(self, sr: int = 44100):
        self.sr = sr
        self._worklet_code = """
        class SoundDesignProcessor extends AudioWorkletProcessor {
            process(inputs, outputs, parameters) {
                const output = outputs[0];
                for (let channel = 0; channel < output.length; channel++) {
                    const outputChannel = output[channel];
                    for (let i = 0; i < outputChannel.length; i++) {
                        outputChannel[i] = 0;
                    }
                }
                return true;
            }
        }
        registerProcessor('sound-design-processor', SoundDesignProcessor);
        """

    def get_worklet_code(self) -> str:
        return self._worklet_code
```

## Performance Optimization

### Real-time Synthesis Performance

| Technique | CPU Savings | Quality Impact |
|-----------|-------------|----------------|
| PolyBLEP anti-aliasing | 30% | Minimal |
| Wavetable lookup | 50% vs computed | None (if tables large enough) |
| SIMD vectorization | 40% | None |
| Voice stealing | Memory reduction | May cut notes short |
| Granular pooling | 25% | None |
| Shared wavetables | Memory reduction | None |

### Memory Management

```python
class SynthMemoryManager:
    def __init__(self, max_wavetable_size: int = 4096, max_grains: int = 1000):
        self.max_wavetable_size = max_wavetable_size
        self.max_grains = max_grains
        self._wavetable_cache: Dict[str, np.ndarray] = {}
        self._grain_pool: List[np.ndarray] = []

    def get_wavetable(self, name: str, generator: Callable) -> np.ndarray:
        if name not in self._wavetable_cache:
            table = generator(self.max_wavetable_size)
            self._wavetable_cache[name] = table
        return self._wavetable_cache[name]

    def acquire_grain(self, size: int) -> np.ndarray:
        for i, grain in enumerate(self._grain_pool):
            if len(grain) == size:
                return self._grain_pool.pop(i)
        return np.zeros(size)

    def release_grain(self, grain: np.ndarray):
        if len(self._grain_pool) < self.max_grains:
            self._grain_pool.append(grain)
```

### Batch Processing

```python
class BatchSoundDesigner:
    def __init__(self, config: SynthConfig = None):
        self.config = config or SynthConfig()

    def generate_variations(self, base_preset: SoundPreset, num_variations: int = 10) -> List[SoundPreset]:
        variations = []
        for _ in range(num_variations):
            var = SoundPreset(
                name=f"{base_preset.name}_var",
                oscillator_type=base_preset.oscillator_type,
                envelope=Envelope(
                    attack=base_preset.envelope.attack * np.random.uniform(0.8, 1.2),
                    decay=base_preset.envelope.decay * np.random.uniform(0.8, 1.2),
                    sustain=base_preset.envelope.sustain * np.random.uniform(0.9, 1.1),
                    release=base_preset.envelope.release * np.random.uniform(0.8, 1.2),
                ),
                filter_cutoff=base_preset.filter_cutoff * np.random.uniform(0.5, 2.0),
                filter_resonance=base_preset.filter_resonance * np.random.uniform(0.8, 1.2),
            )
            variations.append(var)
        return variations
```

## Security Considerations

### Input Validation

```python
def validate_preset(preset: dict) -> bool:
    if not isinstance(preset, dict):
        raise ValueError("Preset must be a dictionary")
    required = ["name", "oscillator_type", "envelope"]
    for field in required:
        if field not in preset:
            raise ValueError(f"Missing required field: {field}")
    valid_oscillators = {"sine", "saw", "square", "triangle", "noise"}
    if preset["oscillator_type"] not in valid_oscillators:
        raise ValueError(f"Invalid oscillator type: {preset['oscillator_type']}")
    return True

def sanitize_preset_name(name: str) -> str:
    return "".join(c for c in name if c.isalnum() or c in "._- ")[:100]
```

### Safe Audio Processing

```python
def safe_process(audio: np.ndarray, process_fn: Callable) -> np.ndarray:
    try:
        result = process_fn(audio)
        if np.any(np.isnan(result)):
            return audio
        if np.any(np.isinf(result)):
            return audio
        peak = np.max(np.abs(result))
        if peak > 10.0:
            result = result / peak
        return result
    except Exception:
        return audio
```

## Troubleshooting Guide

### Common Issues

| Issue | Symptom | Solution |
|-------|---------|----------|
| Aliasing | Harsh high frequencies | Use polyBLEP or increase oversampling |
| Clicking | Audible pops at note transitions | Apply short fade-in/out at boundaries |
| CPU overload | Audio dropouts | Reduce polyphony, increase buffer size |
| Memory leak | Growing memory usage | Use voice manager, release unused grains |
| Phase cancellation | Thin sound from oscillators | Randomize oscillator phases |
| Filter self-oscillation | Uncontrolled resonance | Limit resonance parameter range |
| Granular artifacts | Clicking in granular output | Use windowed grains (Hann, Hanning) |
| FM metallic artifacts | Harsh overtones | Reduce modulation index, use feedback limiting |

### Debugging

```python
def debug_synth_state(voice_manager: VoiceManager, effects: AdvancedEffectsChain):
    print("=== Synth State ===")
    print(f"Active voices: {voice_manager.get_active_count()}")
    for vid, voice in voice_manager.get_all_voices().items():
        print(f"  Voice {vid}: pitch={voice['pitch']}, vel={voice['velocity']:.2f}")
    print(f"Effects: {[name for name, _ in effects._effects]}")
```

## API Reference

### Core Classes

| Class | Constructor | Key Methods |
|-------|-------------|-------------|
| `Oscillator(sr)` | `int` | `saw()`, `square()`, `triangle()`, `noise()`, `sine()` |
| `Envelope(a, d, s, r)` | `float x4` | `apply(audio, sr)` |
| `FMSynthesizer(sr)` | `int` | `synthesize()`, `bell_tone()` |
| `WavetableSynthesizer(sr, size)` | `int, int` | `synthesize()`, `morph()` |
| `GranularSynthesizer(sr)` | `int` | `granulate()` |
| `EffectsChain(sr)` | `int` | `add_*()`, `process()` |
| `AdvancedEffectsChain(sr)` | `int` | `add_reverb()`, `add_compressor()`, `add_chorus()`, `add_limiter()` |
| `VoiceManager(config)` | `SynthConfig` | `note_on()`, `note_off()`, `get_active_count()` |
| `ModulationMatrix()` | none | `add_route()`, `process()` |
| `PresetManager(dir)` | `str` | `save_preset()`, `load_preset()`, `list_presets()` |

## Data Models

### Sound Preset Schema

```json
{
  "name": "string",
  "oscillator": "sine|saw|square|triangle|noise",
  "envelope": {"attack": 0.01, "decay": 0.1, "sustain": 0.7, "release": 0.3},
  "filter": {"cutoff": 1000, "resonance": 1.0},
  "lfo": {"rate": 0.0, "depth": 0.0},
  "effects": ["reverb", "compressor"],
  "category": "bass|lead|pad|pluck|fx"
}
```

### Modulation Route Schema

```json
{
  "source": "lfo1|envelope1|mod_wheel|velocity|aftertouch",
  "destination": "filter_cutoff|pitch|amplitude|pan|effects_mix",
  "amount": "float (-1.0 to 1.0)"
}
```

## Deployment Guide

### Standalone Synthesizer

```python
import pyaudio

class StandaloneSynth:
    def __init__(self, config: SynthConfig = None):
        self.config = config or SynthConfig()
        self.pa = pyaudio.PyAudio()
        self.voice_manager = VoiceManager(self.config)
        self.effects = AdvancedEffectsChain(self.config.sample_rate)

    def start(self):
        stream = self.pa.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.config.sample_rate,
            output=True,
            frames_per_buffer=self.config.block_size,
        )
        print("Synth running. Press Ctrl+C to stop.")
        try:
            while True:
                block = self._generate_block()
                stream.write(block.astype(np.float32).tobytes())
        except KeyboardInterrupt:
            pass
        finally:
            stream.stop_stream()
            stream.close()
            self.pa.terminate()

    def _generate_block(self) -> np.ndarray:
        output = np.zeros(self.config.block_size)
        for vid, voice in self.voice_manager.get_all_voices().items():
            freq = 440.0 * (2 ** ((voice['pitch'] - 69) / 12.0))
            t = np.arange(self.config.block_size) / self.config.sample_rate
            output += np.sin(2 * np.pi * freq * t) * voice['velocity'] * 0.1
        return self.effects.process(output)
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libasound2-dev portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
CMD ["python", "sound_design_server.py"]
```

## Monitoring and Observability

### Synth Performance Metrics

```python
@dataclass
class SynthMetrics:
    voices_active: int = 0
    cpu_usage_percent: float = 0.0
    memory_usage_mb: float = 0.0
    blocks_processed: int = 0
    underruns: int = 0

    def get_report(self) -> dict:
        return {
            "voices": self.voices_active,
            "cpu": f"{self.cpu_usage_percent:.1f}%",
            "memory": f"{self.memory_usage_mb:.1f}MB",
            "blocks": self.blocks_processed,
            "underruns": self.underruns,
        }
```

## Testing Strategy

### Unit Tests

```python
import unittest

class TestOscillator(unittest.TestCase):
    def test_sine_wave(self):
        osc = Oscillator(44100)
        audio = osc.sine(440, 1.0)
        self.assertEqual(len(audio), 44100)
        self.assertAlmostEqual(np.max(audio), 1.0, places=2)

    def test_saw_wave_range(self):
        osc = Oscillator(44100)
        audio = osc.saw(440, 1.0)
        self.assertGreater(np.max(audio), 0.9)
        self.assertLess(np.min(audio), -0.9)

class TestEnvelope(unittest.TestCase):
    def test_adsr_shape(self):
        env = Envelope(attack=0.01, decay=0.1, sustain=0.7, release=0.3)
        audio = np.ones(44100)
        result = env.apply(audio, 44100)
        self.assertEqual(len(result), 44100)
        self.assertLessEqual(np.max(result), 1.0)

class TestFMSynth(unittest.TestCase):
    def test_bell_tone(self):
        synth = FMSynthesizer(44100)
        audio = synth.bell_tone(2.0)
        self.assertEqual(len(audio), 88200)
        self.assertFalse(np.any(np.isnan(audio)))
```

## Versioning and Migration

| Version | Changes |
|---------|---------|
| 2.0.0 | Advanced effects chain, modulation matrix, voice management |
| 1.5.0 | Granular synthesis, wavetable morphing |
| 1.0.0 | Initial release with subtractive and FM synthesis |

## Glossary

| Term | Definition |
|------|-----------|
| **ADSR** | Attack-Decay-Sustain-Release envelope shape |
| **FM Synthesis** | Frequency modulation creating complex timbres |
| **Wavetable** | Pre-computed waveform stored for efficient playback |
| **Granular** | Microsound synthesis using tiny audio grains |
| **LFO** | Low Frequency Oscillator for parameter modulation |
| **Filter cutoff** | Frequency where filter begins attenuating |
| **Resonance** | Boost at filter cutoff frequency |
| **PolyBLEP** | Bandlimited step function for anti-aliased waveforms |
| **Modulation matrix** | Routing system connecting sources to destinations |
| **Voice stealing** | Replacing active voice when polyphony limit reached |

## Changelog

- **2.0.0** - Advanced effects, modulation matrix, voice management
- **1.5.0** - Granular synthesis, wavetable morphing
- **1.2.0** - Added bitcrush and chorus effects
- **1.1.0** - Enhanced preset management
- **1.0.0** - Initial release

## Contributing Guidelines

1. Test all oscillators for numerical stability
2. Verify envelope shapes with known ADSR curves
3. Profile CPU usage for real-time constraints
4. Document parameter ranges and their sonic effects

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills

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

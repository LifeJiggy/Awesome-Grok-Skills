"""
Sound Design Module
Part of the music-tech skill domain.

Sound synthesis and creative audio manipulation: subtractive, FM, wavetable,
granular synthesis, envelopes, LFOs, effects chains, and preset management.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np


class WaveformType(Enum):
    SINE = "sine"
    SAW = "saw"
    SQUARE = "square"
    TRIANGLE = "triangle"
    NOISE = "noise"
    PULSE = "pulse"


class FilterType(Enum):
    LOWPASS = "lowpass"
    HIGHPASS = "highpass"
    BANDPASS = "bandpass"
    NOTCH = "notch"


class LFOShape(Enum):
    SINE = "sine"
    TRIANGLE = "triangle"
    SQUARE = "square"
    SAW_UP = "saw_up"
    SAW_DOWN = "saw_down"
    RANDOM = "random"


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
        sustain_end = max(attack_samples + decay_samples, n - release_samples)

        if attack_samples > 0 and attack_samples <= n:
            envelope[:attack_samples] = np.linspace(0, self.peak, attack_samples)

        decay_end = min(attack_samples + decay_samples, n)
        if decay_samples > 0 and decay_end > attack_samples:
            envelope[attack_samples:decay_end] = np.linspace(
                self.peak, self.sustain * self.peak, decay_end - attack_samples
            )

        if decay_end < sustain_end:
            envelope[decay_end:sustain_end] = self.sustain * self.peak

        if release_samples > 0 and sustain_end < n:
            actual_release = n - sustain_end
            envelope[sustain_end:] = np.linspace(
                self.sustain * self.peak, 0, actual_release
            )

        return audio * envelope

    def to_dict(self) -> Dict[str, float]:
        return {
            "attack": self.attack, "decay": self.decay,
            "sustain": self.sustain, "release": self.release,
        }


@dataclass
class LFO:
    shape: LFOShape = LFOShape.SINE
    rate: float = 1.0
    depth: float = 0.1
    phase: float = 0.0

    def generate(self, duration: float, sr: int) -> np.ndarray:
        n = int(sr * duration)
        t = np.linspace(0, duration, n, endpoint=False)
        phase = 2 * np.pi * self.rate * t + self.phase

        if self.shape == LFOShape.SINE:
            signal = np.sin(phase)
        elif self.shape == LFOShape.TRIANGLE:
            signal = 2 * np.abs(2 * (t * self.rate % 1) - 1) - 1
        elif self.shape == LFOShape.SQUARE:
            signal = np.sign(np.sin(phase))
        elif self.shape == LFOShape.SAW_UP:
            signal = 2 * (t * self.rate % 1) - 1
        elif self.shape == LFOShape.SAW_DOWN:
            signal = 1 - 2 * (t * self.rate % 1)
        elif self.shape == LFOShape.RANDOM:
            signal = np.random.uniform(-1, 1, n)
            signal = np.interp(np.arange(n), np.arange(0, n, sr // 5), signal[:n:sr // 5])
        else:
            signal = np.sin(phase)

        return signal * self.depth


class Oscillator:
    def __init__(self, sr: int = 44100):
        self.sr = sr

    def generate(self, waveform: WaveformType, freq: float,
                 duration: float, amplitude: float = 1.0) -> np.ndarray:
        n = int(self.sr * duration)
        t = np.linspace(0, duration, n, endpoint=False)

        if waveform == WaveformType.SINE:
            return amplitude * np.sin(2 * np.pi * freq * t)
        elif waveform == WaveformType.SAW:
            return amplitude * (2 * (freq * t % 1) - 1)
        elif waveform == WaveformType.SQUARE:
            return amplitude * np.sign(np.sin(2 * np.pi * freq * t))
        elif waveform == WaveformType.TRIANGLE:
            return amplitude * (2 * np.abs(2 * (freq * t % 1) - 1) - 1)
        elif waveform == WaveformType.NOISE:
            return amplitude * np.random.randn(n)
        elif waveform == WaveformType.PULSE:
            return amplitude * (np.sin(2 * np.pi * freq * t) > 0).astype(float) * 2 - 1
        return np.zeros(n)


class Filter:
    def __init__(self, filter_type: FilterType = FilterType.LOWPASS,
                 cutoff: float = 1000.0, resonance: float = 1.0, sr: int = 44100):
        self.filter_type = filter_type
        self.cutoff = cutoff
        self.resonance = resonance
        self.sr = sr

    def apply(self, audio: np.ndarray) -> np.ndarray:
        nyq = self.sr / 2
        normalized_cutoff = min(self.cutoff / nyq, 0.99)
        Q = self.resonance

        w0 = 2 * np.pi * self.cutoff / self.sr
        alpha = np.sin(w0) / (2 * Q)

        if self.filter_type == FilterType.LOWPASS:
            b0 = (1 - np.cos(w0)) / 2
            b1 = 1 - np.cos(w0)
            b2 = (1 - np.cos(w0)) / 2
            a0 = 1 + alpha
            a1 = -2 * np.cos(w0)
            a2 = 1 - alpha
        elif self.filter_type == FilterType.HIGHPASS:
            b0 = (1 + np.cos(w0)) / 2
            b1 = -(1 + np.cos(w0))
            b2 = (1 + np.cos(w0)) / 2
            a0 = 1 + alpha
            a1 = -2 * np.cos(w0)
            a2 = 1 - alpha
        elif self.filter_type == FilterType.BANDPASS:
            b0 = alpha
            b1 = 0
            b2 = -alpha
            a0 = 1 + alpha
            a1 = -2 * np.cos(w0)
            a2 = 1 - alpha
        else:
            b0 = 1
            b1 = -2 * np.cos(w0)
            b2 = 1
            a0 = 1 + alpha
            a1 = -2 * np.cos(w0)
            a2 = 1 - alpha

        b = np.array([b0 / a0, b1 / a0, b2 / a0])
        a = np.array([1.0, a1 / a0, a2 / a0])

        output = np.zeros(len(audio))
        output[0] = audio[0] * b[0]
        if len(audio) > 1:
            output[1] = audio[1] * b[0] + audio[0] * b[1] - output[0] * a[1]

        for i in range(2, len(audio)):
            output[i] = (audio[i] * b[0] + audio[i-1] * b[1] + audio[i-2] * b[2]
                         - output[i-1] * a[1] - output[i-2] * a[2])

        return output


class FMSynthesizer:
    def __init__(self, sr: int = 44100):
        self.sr = sr
        self.osc = Oscillator(sr)

    def synthesize(self, carrier_freq: float, modulator_freq: float,
                   modulation_index: float, duration: float) -> np.ndarray:
        n = int(self.sr * duration)
        t = np.linspace(0, duration, n, endpoint=False)
        modulator = modulation_index * np.sin(2 * np.pi * modulator_freq * t)
        return np.sin(2 * np.pi * carrier_freq * t + modulator)

    def bell_tone(self, duration: float = 2.0) -> np.ndarray:
        n = int(self.sr * duration)
        t = np.linspace(0, duration, n, endpoint=False)
        envelope = np.exp(-3 * t)
        return envelope * (
            np.sin(2 * np.pi * 200 * t + 3.0 * np.sin(2 * np.pi * 600 * t)) * 0.5 +
            np.sin(2 * np.pi * 300 * t + 2.0 * np.sin(2 * np.pi * 900 * t)) * 0.3 +
            np.sin(2 * np.pi * 500 * t + 1.5 * np.sin(2 * np.pi * 1500 * t)) * 0.2
        )

    def metallic_hit(self, duration: float = 1.0) -> np.ndarray:
        n = int(self.sr * duration)
        t = np.linspace(0, duration, n, endpoint=False)
        env = np.exp(-8 * t)
        return env * np.sin(2 * np.pi * 800 * t + 5.0 * np.sin(2 * np.pi * 2400 * t))


class WavetableSynthesizer:
    def __init__(self, sr: int = 44100, table_size: int = 2048):
        self.sr = sr
        self.table_size = table_size
        self.tables: Dict[str, np.ndarray] = self._create_tables()

    def _create_tables(self) -> Dict[str, np.ndarray]:
        t = np.linspace(0, 1, self.table_size, endpoint=False)
        return {
            "saw": 2 * (t % 1) - 1,
            "square": np.sign(np.sin(2 * np.pi * t)),
            "triangle": 2 * np.abs(2 * (t % 1) - 1) - 1,
            "sine": np.sin(2 * np.pi * t),
            "pulse_25": (np.sin(2 * np.pi * t) > -0.5).astype(float) * 2 - 1,
        }

    def synthesize(self, freq: float, duration: float, table: str = "saw") -> np.ndarray:
        n = int(self.sr * duration)
        wavetable = self.tables.get(table, self.tables["sine"])
        phase_inc = freq * self.table_size / self.sr
        output = np.zeros(n)
        phase = 0.0

        for i in range(n):
            idx = int(phase) % self.table_size
            frac = phase - int(phase)
            next_idx = (idx + 1) % self.table_size
            output[i] = wavetable[idx] * (1 - frac) + wavetable[next_idx] * frac
            phase = (phase + phase_inc) % (self.table_size * 1000)

        return output

    def morph(self, freq: float, duration: float, table_a: str, table_b: str,
              position: float = 0.5) -> np.ndarray:
        sig_a = self.synthesize(freq, duration, table_a)
        sig_b = self.synthesize(freq, duration, table_b)
        return (1 - position) * sig_a + position * sig_b


class GranularSynthesizer:
    def __init__(self, sr: int = 44100):
        self.sr = sr

    def granulate(self, audio: np.ndarray, grain_size_ms: float = 50,
                  density: float = 0.5, pitch_shift: float = 1.0,
                  randomization: float = 0.1) -> np.ndarray:
        grain_samples = max(1, int(self.sr * grain_size_ms / 1000))
        hop = max(1, int(grain_samples * (1 - density)))
        num_grains = max(1, (len(audio) - grain_samples) // hop)

        output_len = num_grains * grain_samples
        output = np.zeros(output_len)

        for i in range(num_grains):
            start = i * hop
            if start + grain_samples > len(audio):
                break

            grain = audio[start:start + grain_samples].copy()

            if pitch_shift != 1.0 and pitch_shift > 0:
                new_len = max(1, int(len(grain) / pitch_shift))
                indices = np.linspace(0, len(grain) - 1, new_len)
                grain = np.interp(indices, np.arange(len(grain)), grain)

            if randomization > 0:
                offset = int(np.random.uniform(-randomization, randomization) * grain_samples)
                start = max(0, min(len(audio) - grain_samples, start + offset))
                grain = audio[start:start + grain_samples].copy()

            window = np.hanning(len(grain))
            out_start = i * grain_samples
            grain_len = min(len(grain), output_len - out_start)
            if grain_len > 0:
                output[out_start:out_start + grain_len] += grain[:grain_len] * window[:grain_len]

        peak = np.max(np.abs(output))
        return output / peak if peak > 0 else output


class EffectsChain:
    def __init__(self, sr: int = 44100):
        self.sr = sr
        self._effects: List[Callable[[np.ndarray], np.ndarray]] = []

    def add_distortion(self, drive: float = 2.0) -> EffectsChain:
        self._effects.append(lambda a: np.tanh(a * drive))
        return self

    def add_bitcrush(self, bits: int = 8) -> EffectsChain:
        levels = 2 ** bits
        self._effects.append(lambda a: np.round(a * levels) / levels)
        return self

    def add_delay(self, time_sec: float = 0.3, feedback: float = 0.4,
                  wet: float = 0.3) -> EffectsChain:
        def delay_effect(audio: np.ndarray) -> np.ndarray:
            delay_samples = int(time_sec * self.sr)
            output = np.zeros(len(audio) + delay_samples)
            output[:len(audio)] = audio
            for i in range(delay_samples, len(output)):
                output[i] += output[i - delay_samples] * feedback
            return (1 - wet) * audio + wet * output[:len(audio)]
        self._effects.append(delay_effect)
        return self

    def add_chorus(self, rate: float = 1.5, depth: float = 0.002) -> EffectsChain:
        def chorus_effect(audio: np.ndarray) -> np.ndarray:
            delay_samples = int(depth * self.sr)
            t = np.arange(len(audio)) / self.sr
            mod = (np.sin(2 * np.pi * rate * t) * delay_samples).astype(int)
            output = audio.copy()
            for i in range(delay_samples, len(audio)):
                idx = max(0, i - abs(mod[i]))
                output[i] = audio[i] * 0.7 + audio[idx] * 0.3
            return output
        self._effects.append(chorus_effect)
        return self

    def add_reverb(self, decay: float = 0.5, wet: float = 0.3) -> EffectsChain:
        def reverb_effect(audio: np.ndarray) -> np.ndarray:
            impulse_len = int(self.sr * decay)
            impulse = np.zeros(impulse_len)
            impulse[0] = 1.0
            for i in range(1, impulse_len):
                impulse[i] = impulse[i-1] * decay * np.random.uniform(0.8, 1.0)
            reverb_tail = np.convolve(audio, impulse, mode="full")[:len(audio)]
            return (1 - wet) * audio + wet * reverb_tail
        self._effects.append(reverb_effect)
        return self

    def process(self, audio: np.ndarray) -> np.ndarray:
        result = audio.copy()
        for effect in self._effects:
            result = effect(result)
        peak = np.max(np.abs(result))
        if peak > 1.0:
            result = result / peak
        return result


@dataclass
class SoundPreset:
    name: str
    waveform: WaveformType = WaveformType.SAW
    envelope: Envelope = field(default_factory=Envelope)
    filter_type: FilterType = FilterType.LOWPASS
    filter_cutoff: float = 1000.0
    filter_resonance: float = 1.0
    lfo: Optional[LFO] = None
    effects: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "name": self.name,
            "waveform": self.waveform.value,
            "envelope": self.envelope.to_dict(),
            "filter": {
                "type": self.filter_type.value,
                "cutoff": self.filter_cutoff,
                "resonance": self.filter_resonance,
            },
            "effects": self.effects,
        }
        if self.lfo:
            result["lfo"] = {"shape": self.lfo.shape.value, "rate": self.lfo.rate}
        return result


class PresetLibrary:
    def __init__(self):
        self.presets: Dict[str, SoundPreset] = {}
        self._load_defaults()

    def _load_defaults(self):
        self.presets["warm_pad"] = SoundPreset(
            name="warm_pad", waveform=WaveformType.SAW,
            envelope=Envelope(attack=0.5, decay=0.3, sustain=0.8, release=1.0),
            filter_cutoff=800, filter_resonance=0.5,
            lfo=LFO(LFOShape.SINE, rate=0.3, depth=0.1),
        )
        self.presets["plucky_bass"] = SoundPreset(
            name="plucky_bass", waveform=WaveformType.SQUARE,
            envelope=Envelope(attack=0.005, decay=0.15, sustain=0.3, release=0.1),
            filter_cutoff=2000, filter_resonance=2.0,
        )
        self.presets["bell"] = SoundPreset(
            name="bell", waveform=WaveformType.SINE,
            envelope=Envelope(attack=0.001, decay=0.8, sustain=0.0, release=0.5),
            filter_cutoff=5000, filter_resonance=0.3,
        )

    def add_preset(self, preset: SoundPreset):
        self.presets[preset.name] = preset

    def get_preset(self, name: str) -> Optional[SoundPreset]:
        return self.presets.get(name)

    def list_presets(self) -> List[str]:
        return list(self.presets.keys())


def main():
    print("=== Sound Design Module ===")

    sr = 44100
    duration = 1.0

    osc = Oscillator(sr)
    print("\n=== Oscillator Waveforms ===")
    for wf in [WaveformType.SINE, WaveformType.SAW, WaveformType.SQUARE]:
        wave = osc.generate(wf, 440, duration)
        print(f"  {wf.value}: {len(wave)} samples, peak={np.max(np.abs(wave)):.3f}")

    print("\n=== FM Synthesis ===")
    fm = FMSynthesizer(sr)
    bell = fm.bell_tone(1.0)
    print(f"  Bell tone: {len(bell)} samples, peak={np.max(np.abs(bell)):.3f}")
    metallic = fm.metallic_hit(0.5)
    print(f"  Metallic hit: {len(metallic)} samples, peak={np.max(np.abs(metallic)):.3f}")

    print("\n=== Wavetable Synthesis ===")
    wt = WavetableSynthesizer(sr)
    for table in ["saw", "square", "sine"]:
        sig = wt.synthesize(440, 0.5, table)
        print(f"  {table}: {len(sig)} samples, peak={np.max(np.abs(sig)):.3f}")

    morphed = wt.morph(440, 0.5, "saw", "sine", 0.5)
    print(f"  Morphed: {len(morphed)} samples, peak={np.max(np.abs(morphed)):.3f}")

    print("\n=== Granular Synthesis ===")
    granular = GranularSynthesizer(sr)
    source = osc.generate(WaveformType.SAW, 220, 2.0)
    grains = granular.granulate(source, grain_size_ms=30, density=0.6, pitch_shift=1.5)
    print(f"  Granulated: {len(grains)} samples")

    print("\n=== Effects Chain ===")
    effects = EffectsChain(sr)
    chain = effects.add_distortion(2.0).add_delay(0.3, 0.4, 0.3).add_reverb(0.5, 0.3)
    test_audio = osc.generate(WaveformType.SAW, 220, 0.5)
    processed = chain.process(test_audio)
    print(f"  Processed: {len(processed)} samples, peak={np.max(np.abs(processed)):.3f}")

    print("\n=== Preset Library ===")
    library = PresetLibrary()
    print(f"  Available: {library.list_presets()}")
    for name in library.list_presets():
        preset = library.get_preset(name)
        if preset:
            print(f"  {name}: {preset.waveform.value}, "
                  f"attack={preset.envelope.attack}s, "
                  f"cutoff={preset.filter_cutoff}Hz")

    print("\nDone.")


if __name__ == "__main__":
    main()

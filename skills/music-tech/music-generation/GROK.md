---
name: music-generation
category: music-tech
version: 2.0.0
tags: [music-tech, music-generation, ai, composition, deep-learning]
---

# Music Generation

## Overview

AI-driven music generation covering melody composition, harmony generation, rhythm programming, and full arrangement creation. This skill provides implementations of sequence-to-sequence models, variational autoencoders (VAE) for latent space music interpolation, transformer-based generation with tokenized MIDI, and rule-based composition systems for chord progressions, counterpoint, and orchestration.

## Core Capabilities

- **Melody Generation**: RNN/LSTM and Transformer-based melodic sequence generation
- **Harmony Generation**: Chord progression generation using Markov chains and neural networks
- **Rhythm Programming**: Beat pattern generation with genre-specific templates
- **MIDI Processing**: MIDI parsing, quantization, transposition, and format conversion
- **Latent Space Interpolation**: VAE-based smooth transitions between musical styles
- **Arrangement**: Multi-track orchestration with instrument assignment
- **Style Transfer**: Apply musical characteristics from one piece to another
- **Evaluation**: Musical coherence scoring, variety metrics, and listener preference prediction

## Usage Examples

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

# Musical Encoding
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

@dataclass
class Note:
    pitch: int          # MIDI pitch (0-127)
    duration: float     # Duration in beats
    velocity: int = 80  # MIDI velocity (0-127)
    time: float = 0.0   # Onset time in beats

    @property
    def name(self) -> str:
        return NOTE_NAMES[self.pitch % 12]

    @property
    def octave(self) -> int:
        return (self.pitch // 12) - 1

@dataclass
class Chord:
    notes: List[int]    # List of MIDI pitches
    duration: float = 4.0
    time: float = 0.0

    @classmethod
    def from_name(cls, root: str, quality: str = "major", duration: float = 4.0) -> 'Chord':
        root_idx = NOTE_NAMES.index(root)
        patterns = {
            "major": [0, 4, 7],
            "minor": [0, 3, 7],
            "dim": [0, 3, 6],
            "aug": [0, 4, 8],
            "maj7": [0, 4, 7, 11],
            "min7": [0, 3, 7, 10],
        }
        pattern = patterns.get(quality, patterns["major"])
        midi_root = root_idx + 60
        return cls(notes=[midi_root + interval for interval in pattern], duration=duration)

# Chord Progression Generator
class ChordProgressionGenerator:
    PROGRESSIONS = {
        "pop": [("I", 4), ("V", 4), ("vi", 4), ("IV", 4)],
        "jazz": [("II7", 2), ("V7", 2), ("I", 4), ("VI7", 2), ("II7", 2), ("V7", 4)],
        "blues": [("I", 4), ("I", 4), ("I", 4), ("I", 4),
                  ("IV", 4), ("IV", 4), ("I", 4), ("I", 4),
                  ("V", 4), ("IV", 4), ("I", 4), ("V", 4)],
        "classical": [("I", 4), ("IV", 4), ("V", 4), ("I", 4),
                      ("vi", 4), ("IV", 4), ("V", 4), ("I", 4)],
    }

    CHORD_MAP = {
        "I": ("C", "major"), "ii": ("D", "minor"), "iii": ("E", "minor"),
        "IV": ("F", "major"), "V": ("G", "major"), "vi": ("A", "minor"),
        "vii": ("B", "dim"), "II7": ("D", "maj7"), "V7": ("G", "dom7"),
        "VI7": ("A", "dom7"), "I7": ("C", "dom7"), "iv": ("F", "minor"),
    }

    def generate(self, style: str = "pop", num_bars: int = 8) -> List[Chord]:
        pattern = self.PROGRESSIONS.get(style, self.PROGRESSIONS["pop"])
        progression = []
        total_beats = 0
        while total_beats < num_bars * 4:
            for roman, duration in pattern:
                if total_beats >= num_bars * 4:
                    break
                root, quality = self.CHROMATIC_MAP.get(roman, ("C", "major"))
                chord = Chord.from_name(root, quality, duration)
                chord.time = total_beats
                progression.append(chord)
                total_beats += duration
        return progression

# Melody Generator using Markov Chain
class MelodyGenerator:
    def __init__(self, transition_matrix: Optional[dict] = None):
        self.transitions = transition_matrix or self._default_transitions()

    def _default_transitions(self) -> dict:
        return {
            60: [62, 64, 65, 67],
            62: [60, 64, 65, 67, 69],
            64: [62, 65, 67, 69],
            65: [64, 67, 69, 71],
            67: [65, 69, 71, 72],
            69: [67, 71, 72, 69],
            71: [69, 72, 67, 65],
            72: [71, 69, 67, 65],
        }

    def generate(self, length: int = 32, start_pitch: int = 60) -> List[Note]:
        melody = []
        current = start_pitch
        time = 0.0

        for _ in range(length):
            if current in self.transitions:
                next_pitch = np.random.choice(self.transitions[current])
            else:
                next_pitch = current + np.random.choice([-2, -1, 0, 1, 2])

            duration = np.random.choice([0.5, 1.0, 1.5, 2.0])
            velocity = np.random.randint(60, 100)

            melody.append(Note(
                pitch=max(0, min(127, next_pitch)),
                duration=duration,
                velocity=velocity,
                time=time,
            ))
            time += duration
            current = next_pitch

        return melody

# Rhythm Pattern Generator
class RhythmGenerator:
    GENRE_PATTERNS = {
        "hip_hop": {
            "kick":  [1,0,0,0, 1,0,1,0, 0,0,1,0, 1,0,0,0],
            "snare": [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
            "hihat": [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1],
        },
        "house": {
            "kick":  [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0],
            "snare": [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
            "hihat": [0,0,1,0, 0,0,1,0, 0,0,1,0, 0,0,1,0],
        },
    }

    def generate_pattern(self, genre: str, bars: int = 4) -> dict:
        pattern = self.GENRE_PATTERNS.get(genre, self.GENRE_PATTERNS["hip_hop"])
        result = {}
        for instrument, hits in pattern.items():
            result[instrument] = hits * bars
        return result

# Musical Evaluation
class MusicEvaluator:
    def score_coherence(self, notes: List[Note]) -> float:
        if len(notes) < 2:
            return 0.0
        intervals = [abs(notes[i+1].pitch - notes[i].pitch) for i in range(len(notes) - 1)]
        conjunct = sum(1 for i in intervals if i <= 2)
        return conjunct / len(intervals)

    def score_variety(self, notes: List[Note]) -> float:
        pitches = set(n.pitch % 12 for n in notes)
        return len(pitches) / 12.0

    def score_rhythmic_interest(self, notes: List[Note]) -> float:
        durations = [n.duration for n in notes]
        unique = len(set(durations))
        return min(1.0, unique / 5.0)
```

## Best Practices

- Use temperature sampling (0.5-1.5) to control generation diversity vs. coherence
- Train models on genre-specific datasets for higher quality output
- Quantize MIDI output to a fixed grid for playback compatibility
- Evaluate generated music with multiple metrics: coherence, variety, rhythmic interest
- Use latent space interpolation for smooth style transitions between generated pieces
- Implement post-processing: remove overlapping notes, enforce range constraints
- Use attention mechanisms in transformers for long-range musical dependencies
- Condition generation on user-provided seed melodies for controllable output
- Store generated music in MIDI format for maximum tool compatibility
- Provide real-time preview capabilities for interactive composition

## Related Modules

- `sound-design` - Sound synthesis and timbral exploration
- `audio-processing` - Low-level DSP and feature extraction
- `music-analytics` - Deep musical feature analysis
- `dj-tools` - Mixing and set construction utilities

## Advanced Configuration

### Model Hyperparameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `temperature` | 1.0 | 0.1 - 2.0 | Controls generation randomness |
| `top_k` | 50 | 1 - 127 | Top-k sampling for note selection |
| `top_p` | 0.9 | 0.0 - 1.0 | Nucleus sampling threshold |
| `max_sequence` | 512 | 64 - 2048 | Maximum generated sequence length |
| `hidden_dim` | 256 | 64 - 1024 | Transformer hidden dimension |
| `num_layers` | 6 | 2 - 12 | Number of transformer layers |
| `num_heads` | 8 | 2 - 16 | Attention heads count |
| `dropout` | 0.1 | 0.0 - 0.5 | Regularization dropout rate |
| `learning_rate` | 0.001 | 0.0001 - 0.01 | Training learning rate |
| `batch_size` | 32 | 8 - 128 | Training batch size |

### MIDI Tokenizer Configuration

```python
from dataclasses import dataclass
from typing import Dict, List

@dataclass
class MidiTokenizerConfig:
    vocabulary_size: int = 512
    max_pitch: int = 128
    velocity_bins: int = 32
    time_resolution: int = 4  # ticks per beat
    use_time_shift: bool = True
    use_duration: bool = True
    use_velocity: bool = True
    special_tokens: List[str] = None

    def __post_init__(self):
        if self.special_tokens is None:
            self.special_tokens = ["PAD", "BOS", "EOS", "UNK", "MASK"]

class MidiTokenizer:
    def __init__(self, config: MidiTokenizerConfig = None):
        self.config = config or MidiTokenizerConfig()
        self.vocab: Dict[str, int] = {}
        self._build_vocab()

    def _build_vocab(self):
        idx = 0
        for token in self.config.special_tokens:
            self.vocab[token] = idx
            idx += 1
        for pitch in range(self.config.max_pitch):
            self.vocab[f"NOTE_ON_{pitch}"] = idx
            idx += 1
            self.vocab[f"NOTE_OFF_{pitch}"] = idx
            idx += 1
        for vel in range(self.config.velocity_bins):
            self.vocab[f"VELOCITY_{vel}"] = idx
            idx += 1
        for shift in range(1, 128):
            self.vocab[f"TIME_SHIFT_{shift}"] = idx
            idx += 1

    def tokenize(self, notes: List[Note]) -> List[int]:
        tokens = [self.vocab["BOS"]]
        sorted_notes = sorted(notes, key=lambda n: n.time)
        current_time = 0.0
        for note in sorted_notes:
            time_diff = note.time - current_time
            if time_diff > 0:
                shift = max(1, int(time_diff * self.config.time_resolution))
                tokens.append(self.vocab.get(f"TIME_SHIFT_{shift}", self.vocab["UNK"]))
            tokens.append(self.vocab.get(f"NOTE_ON_{note.pitch}", self.vocab["UNK"]))
            vel_idx = min(note.velocity * self.config.velocity_bins // 128,
                         self.config.velocity_bins - 1)
            tokens.append(self.vocab.get(f"VELOCITY_{vel_idx}", self.vocab["UNK"]))
            dur = max(1, int(note.duration * self.config.time_resolution))
            tokens.append(self.vocab.get(f"TIME_SHIFT_{dur}", self.vocab["UNK"]))
            tokens.append(self.vocab.get(f"NOTE_OFF_{note.pitch}", self.vocab["UNK"]))
            current_time = note.time
        tokens.append(self.vocab["EOS"])
        return tokens

    def detokenize(self, tokens: List[int]) -> List[Note]:
        idx_to_token = {v: k for k, v in self.vocab.items()}
        notes = []
        current_time = 0.0
        current_velocity = 80
        i = 0
        while i < len(tokens):
            token = idx_to_token.get(tokens[i], "UNK")
            if token.startswith("TIME_SHIFT_"):
                shift = int(token.split("_")[-1])
                current_time += shift / self.config.time_resolution
            elif token.startswith("NOTE_ON_"):
                pitch = int(token.split("_")[-1])
                if i + 1 < len(tokens):
                    vel_token = idx_to_token.get(tokens[i + 1], "")
                    if vel_token.startswith("VELOCITY_"):
                        current_velocity = int(vel_token.split("_")[-1]) * 128 // self.config.velocity_bins
                        i += 1
                notes.append(Note(pitch=pitch, velocity=current_velocity, time=current_time))
            i += 1
        return notes

    @property
    def vocab_size(self) -> int:
        return len(self.vocab)
```

### Transformer Model Configuration

```python
@dataclass
class TransformerConfig:
    vocab_size: int = 512
    max_seq_len: int = 1024
    d_model: int = 256
    n_heads: int = 8
    n_layers: int = 6
    d_ff: int = 1024
    dropout: float = 0.1
    activation: str = "gelu"
    layer_norm_eps: float = 1e-5
    attention_dropout: float = 0.1

    def to_dict(self) -> dict:
        return {
            "vocab_size": self.vocab_size,
            "max_seq_len": self.max_seq_len,
            "d_model": self.d_model,
            "n_heads": self.n_heads,
            "n_layers": self.n_layers,
            "d_ff": self.d_ff,
            "dropout": self.dropout,
        }
```

### Training Configuration

| Parameter | Value | Notes |
|-----------|-------|-------|
| Optimizer | AdamW | Weight decay 0.01 |
| Scheduler | Cosine Annealing | With warmup |
| Warmup Steps | 1000 | Linear warmup |
| Gradient Clip | 1.0 | Max gradient norm |
| Mixed Precision | FP16 | For GPU training |
| Checkpoint Every | 1000 steps | Save frequency |
| Eval Every | 500 steps | Validation frequency |
| Early Stopping | patience=10 | Based on validation loss |

## Architecture Patterns

### Sequence-to-Sequence with Attention

```
Input Tokens → Embedding → Positional Encoding → Transformer Encoder
                                                              ↓
Target Tokens → Embedding → Positional Encoding → Transformer Encoder
                                                              ↓
                                                    Cross Attention
                                                              ↓
                                                    Linear + Softmax
                                                              ↓
                                                    Output Distribution
```

### Variational Autoencoder for Music

```python
class MusicVAE:
    def __init__(self, input_dim: int, latent_dim: int = 128, hidden_dim: int = 512):
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.hidden_dim = hidden_dim

    def encode(self, sequence: np.ndarray) -> tuple:
        mean = np.zeros(self.latent_dim)
        logvar = np.zeros(self.latent_dim)
        hidden = np.tanh(np.dot(sequence, np.random.randn(self.input_dim, self.hidden_dim)))
        mean = np.dot(hidden[-1], np.random.randn(self.hidden_dim, self.latent_dim))
        logvar = np.dot(hidden[-1], np.random.randn(self.hidden_dim, self.latent_dim))
        return mean, logvar

    def reparameterize(self, mean, logvar):
        std = np.exp(0.5 * logvar)
        eps = np.random.randn(*std.shape)
        return mean + eps * std

    def decode(self, z: np.ndarray, length: int) -> np.ndarray:
        hidden = np.tanh(np.dot(z, np.random.randn(self.latent_dim, self.hidden_dim)))
        output = np.dot(hidden, np.random.randn(self.hidden_dim, self.input_dim))
        return np.tile(output, (length, 1))

    def interpolate(self, z1: np.ndarray, z2: np.ndarray, steps: int = 10):
        alphas = np.linspace(0, 1, steps)
        return [(1 - a) * z1 + a * z2 for a in alphas]
```

### Markov Chain Music Model

```python
class MarkovMusicModel:
    def __init__(self, order: int = 2):
        self.order = order
        self.transitions: Dict[tuple, Dict[int, int]] = {}

    def train(self, notes: List[Note]):
        pitches = [n.pitch for n in notes]
        for i in range(len(pitches) - self.order):
            state = tuple(pitches[i:i+self.order])
            next_pitch = pitches[i + self.order]
            if state not in self.transitions:
                self.transitions[state] = {}
            self.transitions[state][next_pitch] = self.transitions[state].get(next_pitch, 0) + 1

    def generate(self, length: int = 64, seed: List[int] = None) -> List[int]:
        if seed is None:
            seed = list(np.random.choice(list(self.transitions.keys())[0]))
        result = list(seed)
        for _ in range(length):
            state = tuple(result[-self.order:])
            if state in self.transitions:
                weights = self.transitions[state]
                pitches = list(weights.keys())
                counts = list(weights.values())
                next_pitch = np.random.choice(pitches, p=np.array(counts)/sum(counts))
            else:
                next_pitch = np.random.randint(48, 84)
            result.append(next_pitch)
        return result
```

### Hierarchical Generation

```python
class HierarchicalComposer:
    def __init__(self):
        self.form_model = None   # Generates song structure
        self.section_model = None  # Generates sections
        self.phrase_model = None   # Generates phrases
        self.note_model = None     # Generates individual notes

    def compose(self, form: str = "verse-chorus-verse-chorus", num_bars: int = 32):
        structure = self._generate_structure(form, num_bars)
        full_piece = []
        current_time = 0.0
        for section in structure:
            notes = self._generate_section(section, current_time)
            full_piece.extend(notes)
            current_time += section["duration"]
        return full_piece

    def _generate_structure(self, form: str, num_bars: int):
        sections = form.split("-")
        bars_per_section = num_bars // len(sections)
        return [{"type": s, "duration": bars_per_section * 4.0} for s in sections]

    def _generate_section(self, section: dict, start_time: float):
        return []  # Placeholder for model inference
```

## Integration Guide

### MIDI File I/O

```python
import struct
import mido

class MidiFileHandler:
    @staticmethod
    def read_midi(filepath: str) -> List[Note]:
        mid = mido.MidiFile(filepath)
        notes = []
        current_time = 0.0
        tempo = 500000  # Default 120 BPM
        for track in mid.tracks:
            for msg in track:
                current_time += mido.tick2second(msg.time, mid.ticks_per_beat, tempo)
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                elif msg.type == 'note_on' and msg.velocity > 0:
                    notes.append(Note(
                        pitch=msg.note, velocity=msg.velocity,
                        time=current_time, duration=0.5
                    ))
        return notes

    @staticmethod
    def write_midi(notes: List[Note], filepath: str, tempo: int = 120):
        mid = mido.MidiFile()
        track = mido.MidiTrack()
        mid.tracks.append(track)
        track.append(mido.MetaMessage('set_tempo', tempo=mido.bpm2tempo(tempo)))
        sorted_notes = sorted(notes, key=lambda n: n.time)
        prev_time = 0.0
        for note in sorted_notes:
            delta = note.time - prev_time
            track.append(mido.Message('note_on', note=note.pitch,
                                      velocity=note.velocity,
                                      time=int(delta * mid.ticks_per_beat * tempo / 60)))
            track.append(mido.Message('note_off', note=note.pitch,
                                      velocity=0,
                                      time=int(note.duration * mid.ticks_per_beat * tempo / 60)))
            prev_time = note.time
        mid.save(filepath)
```

### Audio Rendering

```python
class MidiRenderer:
    def __init__(self, sr: int = 44100):
        self.sr = sr

    def render(self, notes: List[Note], waveform: str = "sine") -> np.ndarray:
        total_samples = int((max(n.time + n.duration for n in notes) + 1) * self.sr)
        audio = np.zeros(total_samples)
        for note in notes:
            start = int(note.time * self.sr)
            duration_samples = int(note.duration * self.sr)
            t = np.linspace(0, note.duration, duration_samples, endpoint=False)
            freq = 440.0 * (2 ** ((note.pitch - 69) / 12.0))
            amplitude = note.velocity / 127.0
            if waveform == "sine":
                wave = amplitude * np.sin(2 * np.pi * freq * t)
            elif waveform == "saw":
                wave = amplitude * (2 * (freq * t % 1) - 1)
            envelope = np.exp(-2 * t / note.duration)
            end = min(start + duration_samples, total_samples)
            audio[start:end] += wave[:end-start] * envelope[:end-start]
        peak = np.max(np.abs(audio))
        if peak > 0:
            audio = audio / peak
        return audio
```

### Web Integration

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class MusicGenApi(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/generate":
            content_length = int(self.headers['Content-Length'])
            body = json.loads(self.rfile.read(content_length))
            style = body.get("style", "pop")
            length = body.get("length", 32)
            generator = ChordProgressionGenerator()
            progression = generator.generate(style, length // 4)
            result = [{"root": c.notes[0] % 12, "duration": c.duration} for c in progression]
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"progression": result}).encode())
```

## Performance Optimization

### Sequence Generation Speed

| Technique | Speedup | Tradeoff |
|-----------|---------|----------|
| Beam Search | 1.5x | More deterministic output |
| Top-k Sampling | 1.0x | Better diversity |
| Greedy Decoding | 2.0x | Less creative |
| KV-Cache | 3.0x | More memory usage |
| Quantization (INT8) | 2.5x | Slight quality loss |
| Batch Inference | 4.0x | Requires GPU memory |

### Memory Management

```python
class MusicGenOptimizer:
    def __init__(self, max_cache_size: int = 1000):
        self.max_cache_size = max_cache_size
        self._cache: Dict[str, np.ndarray] = {}

    def cache_result(self, key: str, value: np.ndarray):
        if len(self._cache) >= self.max_cache_size:
            oldest = next(iter(self._cache))
            del self._cache[oldest]
        self._cache[key] = value

    def get_cached(self, key: str) -> Optional[np.ndarray]:
        return self._cache.get(key)
```

### Batch Processing

```python
class BatchGenerator:
    def __init__(self, batch_size: int = 32):
        self.batch_size = batch_size

    def generate_batch(self, prompts: List[dict]) -> List[List[Note]]:
        results = []
        for i in range(0, len(prompts), self.batch_size):
            batch = prompts[i:i+self.batch_size]
            batch_results = [self._generate_single(p) for p in batch]
            results.extend(batch_results)
        return results

    def _generate_single(self, prompt: dict) -> List[Note]:
        return []
```

## Security Considerations

### Input Validation

```python
VALID_STYLES = {"pop", "jazz", "blues", "classical", "rock", "electronic", "hip_hop"}
MAX_LENGTH = 512
MIN_LENGTH = 4

def validate_generation_params(style: str, length: int, key: str = "C") -> bool:
    if style not in VALID_STYLES:
        raise ValueError(f"Invalid style: {style}. Must be one of {VALID_STYLES}")
    if length < MIN_LENGTH or length > MAX_LENGTH:
        raise ValueError(f"Length must be between {MIN_LENGTH} and {MAX_LENGTH}")
    valid_keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    if key not in valid_keys:
        raise ValueError(f"Invalid key: {key}")
    return True
```

### Resource Limits

```python
MAX_GENERATION_TIME = 30  # seconds
MAX_MEMORY_MB = 2048

def enforce_generation_limits(func):
    def wrapper(*args, **kwargs):
        import signal
        def timeout_handler(signum, frame):
            raise TimeoutError("Generation exceeded time limit")
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(MAX_GENERATION_TIME)
        try:
            result = func(*args, **kwargs)
        finally:
            signal.alarm(0)
        return result
    return wrapper
```

### Secure Model Loading

```python
import hashlib

def verify_model_checksum(filepath: str, expected_hash: str) -> bool:
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hasher.update(chunk)
    return hasher.hexdigest() == expected_hash
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Repetitive output | Temperature too low | Increase temperature to 1.0-1.2 |
| Chaotic output | Temperature too high | Decrease to 0.7-0.9 |
| Out of memory | Sequence too long | Reduce max_sequence or use chunking |
| MIDI import fails | Unsupported format | Convert to MIDI 1.0 first |
| Poor musical coherence | Insufficient training | Train on more genre-specific data |
| Slow generation | CPU inference | Use GPU or reduce model size |
| Off-key output | Key not constrained | Apply key signature constraints post-generation |
| Note overlap | No collision detection | Add post-processing to resolve overlaps |

### Debugging Tools

```python
def debug_generation(notes: List[Note], expected_key: str = "C"):
    print(f"Total notes: {len(notes)}")
    pitches = [n.pitch % 12 for n in notes]
    from collections import Counter
    pitch_dist = Counter(pitches)
    print(f"Pitch distribution: {dict(pitch_dist)}")
    durations = [n.duration for n in notes]
    print(f"Duration range: {min(durations):.2f} - {max(durations):.2f}")
    print(f"Time range: {min(n.time for n in notes):.2f} - {max(n.time for n in notes):.2f}")
    velocities = [n.velocity for n in notes]
    print(f"Velocity range: {min(velocities)} - {max(velocities)}")
```

### Validation Pipeline

```python
def validate_output(notes: List[Note], config: dict = None) -> dict:
    issues = []
    if len(notes) == 0:
        issues.append("Empty output")
    pitches = [n.pitch for n in notes]
    if any(p < 0 or p > 127 for p in pitches):
        issues.append("Pitch out of MIDI range")
    if any(n.velocity < 0 or n.velocity > 127 for n in notes):
        issues.append("Velocity out of range")
    durations = [n.duration for n in notes]
    if any(d <= 0 for d in durations):
        issues.append("Invalid duration")
    time_diffs = [notes[i+1].time - notes[i].time for i in range(len(notes)-1)]
    if any(d < 0 for d in time_diffs):
        issues.append("Notes not in chronological order")
    return {"valid": len(issues) == 0, "issues": issues}
```

## API Reference

### Core Classes

| Class | Parameters | Methods |
|-------|-----------|---------|
| `Note` | `pitch, duration, velocity, time` | `name`, `octave` |
| `Chord` | `notes, duration, time` | `from_name(root, quality, duration)` |
| `ChordProgressionGenerator` | none | `generate(style, num_bars)` |
| `MelodyGenerator` | `transition_matrix` | `generate(length, start_pitch)` |
| `RhythmGenerator` | none | `generate_pattern(genre, bars)` |
| `MusicEvaluator` | none | `score_coherence()`, `score_variety()`, `score_rhythmic_interest()` |
| `MidiTokenizer` | `config` | `tokenize()`, `detokenize()` |
| `MusicVAE` | `input_dim, latent_dim` | `encode()`, `decode()`, `interpolate()` |

### Utility Functions

| Function | Description |
|----------|-------------|
| `validate_generation_params(style, length, key)` | Validate generation parameters |
| `validate_output(notes, config)` | Validate generated music output |
| `debug_generation(notes, key)` | Print debug info about generated music |

## Data Models

### MIDI Event Schema

```json
{
  "midi_event": {
    "type": "note_on|note_off|control_change|program_change",
    "channel": "int (0-15)",
    "note": "int (0-127)",
    "velocity": "int (0-127)",
    "time": "float (seconds)",
    "duration": "float (seconds)"
  }
}
```

### Generation Request Schema

```json
{
  "generation_request": {
    "style": "string",
    "key": "string",
    "tempo": "int (BPM)",
    "length": "int (bars)",
    "seed": "int[] (optional)",
    "temperature": "float",
    "num_variations": "int"
  }
}
```

### Music Theory Reference

| Scale | Intervals | Example |
|-------|-----------|---------|
| Major | [0,2,4,5,7,9,11] | C D E F G A B |
| Minor | [0,2,3,5,7,8,10] | C D Eb F G Ab Bb |
| Pentatonic Major | [0,2,4,7,9] | C D E G A |
| Blues | [0,3,5,6,7,10] | C Eb F F# G Bb |
| Dorian | [0,2,3,5,7,9,10] | C D Eb F G A Bb |

## Deployment Guide

### Model Serving

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
generator = ChordProgressionGenerator()

@app.route('/api/chords', methods=['POST'])
def generate_chords():
    data = request.json
    style = data.get('style', 'pop')
    num_bars = data.get('num_bars', 8)
    progression = generator.generate(style, num_bars)
    return jsonify({
        "chords": [{"root": c.notes[0] % 12, "duration": c.duration} for c in progression]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["python", "server.py"]
```

## Monitoring and Observability

### Generation Metrics

```python
@dataclass
class GenerationMetrics:
    total_generated: int = 0
    avg_generation_time_ms: float = 0.0
    avg_notes_per_piece: int = 0
    error_rate: float = 0.0

    def record(self, num_notes: int, time_ms: float, success: bool):
        self.total_generated += 1
        self.avg_generation_time_ms = (
            (self.avg_generation_time_ms * (self.total_generated - 1) + time_ms) / self.total_generated
        )
        self.avg_notes_per_piece = int(
            (self.avg_notes_per_piece * (self.total_generated - 1) + num_notes) / self.total_generated
        )
        if not success:
            self.error_rate = (
                self.error_rate * (self.total_generated - 1) + 1
            ) / self.total_generated
```

## Testing Strategy

### Unit Tests

```python
import unittest

class TestNote(unittest.TestCase):
    def test_note_creation(self):
        note = Note(pitch=60, duration=1.0)
        self.assertEqual(note.name, "C")
        self.assertEqual(note.octave, 4)

    def test_chord_from_name(self):
        chord = Chord.from_name("C", "major")
        self.assertEqual(len(chord.notes), 3)
        self.assertEqual(chord.notes[0], 60)

class TestChordProgression(unittest.TestCase):
    def test_pop_progression(self):
        gen = ChordProgressionGenerator()
        progression = gen.generate("pop", 4)
        self.assertGreater(len(progression), 0)

class TestMusicEvaluator(unittest.TestCase):
    def test_coherence(self):
        evaluator = MusicEvaluator()
        notes = [Note(60, 1), Note(62, 1), Note(64, 1)]
        score = evaluator.score_coherence(notes)
        self.assertGreater(score, 0)
```

## Versioning and Migration

| Version | Changes |
|---------|---------|
| 2.0.0 | Transformer-based generation, VAE interpolation, MIDI tokenizer |
| 1.5.0 | Hierarchical composition, improved evaluation metrics |
| 1.0.0 | Initial Markov chain and chord progression generators |

## Glossary

| Term | Definition |
|------|-----------|
| **MIDI** | Musical Instrument Digital Interface - standard for digital music |
| **VAE** | Variational Autoencoder - generative model with latent space |
| **Temperature** | Parameter controlling randomness in generation |
| **Top-k sampling** | Selecting from k most probable next tokens |
| **CSP** | Common Spatial Patterns - feature extraction for BCI |
| **Chord progression** | Sequence of chords forming harmonic structure |
| **Roman numeral analysis** | Chords labeled by scale degree (I, IV, V, vi) |
| **Velocity** | MIDI parameter controlling note loudness (0-127) |
| **Quantization** | Aligning notes to a rhythmic grid |

## Changelog

- **2.0.0** - Major release with transformer models and VAE
- **1.5.0** - Added hierarchical composition and improved eval
- **1.2.0** - Added rhythm pattern generation
- **1.1.0** - Added music evaluation metrics
- **1.0.0** - Initial release with chord progressions and melody generation

## Contributing Guidelines

1. Add tests for new generation algorithms
2. Validate musical output with evaluation metrics
3. Document model architecture changes
4. Follow MIDI standard compliance
5. Benchmark generation speed and quality

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills

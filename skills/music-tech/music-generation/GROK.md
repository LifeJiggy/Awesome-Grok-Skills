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

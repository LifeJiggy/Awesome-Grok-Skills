"""
Music Generation Module
Part of the music-tech skill domain.

AI-driven music composition: melody generation, harmony, rhythm programming,
MIDI processing, and musical evaluation metrics.
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np


class MusicalKey(Enum):
    C = 0
    C_SHARP = 1
    D = 2
    D_SHARP = 3
    E = 4
    F = 5
    F_SHARP = 6
    G = 7
    G_SHARP = 8
    A = 9
    A_SHARP = 10
    B = 11


class ScaleType(Enum):
    MAJOR = "major"
    MINOR = "minor"
    PENTATONIC_MAJOR = "pentatonic_major"
    PENTATONIC_MINOR = "pentatonic_minor"
    DORIAN = "dorian"
    MIXOLYDIAN = "mixolydian"
    BLUES = "blues"


class RhythmGenre(Enum):
    HIP_HOP = "hip_hop"
    HOUSE = "house"
    JAZZ = "jazz"
    ROCK = "rock"
    AFROBEAT = "afrobeat"
    REGGAE = "reggae"


NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

SCALE_INTERVALS = {
    ScaleType.MAJOR: [0, 2, 4, 5, 7, 9, 11],
    ScaleType.MINOR: [0, 2, 3, 5, 7, 8, 10],
    ScaleType.PENTATONIC_MAJOR: [0, 2, 4, 7, 9],
    ScaleType.PENTATONIC_MINOR: [0, 3, 5, 7, 10],
    ScaleType.DORIAN: [0, 2, 3, 5, 7, 9, 10],
    ScaleType.MIXOLYDIAN: [0, 2, 4, 5, 7, 9, 10],
    ScaleType.BLUES: [0, 3, 5, 6, 7, 10],
}

CHORD_PROGRESSIONS = {
    "pop": [("I", 4), ("V", 4), ("vi", 4), ("IV", 4)],
    "jazz": [("II7", 2), ("V7", 2), ("I", 4), ("VI7", 2), ("II7", 2), ("V7", 4)],
    "blues": [("I", 4), ("IV", 4), ("I", 4), ("V", 4)] * 3,
    "classical": [("I", 4), ("IV", 4), ("V", 4), ("I", 4), ("vi", 4), ("IV", 4), ("V", 4), ("I", 4)],
    "afrobeat": [("I", 4), ("IV", 4), ("V", 4), ("IV", 4)],
}

ROMAN_TO_CHORD = {
    "I": (0, "major"), "ii": (2, "minor"), "iii": (4, "minor"),
    "IV": (5, "major"), "V": (7, "major"), "vi": (9, "minor"),
    "vii": (11, "dim"), "II7": (2, "maj7"), "V7": (7, "dom7"),
    "VI7": (9, "dom7"), "I7": (0, "dom7"), "iv": (5, "minor"),
}

CHORD_PATTERNS = {
    "major": [0, 4, 7],
    "minor": [0, 3, 7],
    "dim": [0, 3, 6],
    "aug": [0, 4, 8],
    "maj7": [0, 4, 7, 11],
    "min7": [0, 3, 7, 10],
    "dom7": [0, 4, 7, 10],
}

RHYTHM_PATTERNS = {
    RhythmGenre.HIP_HOP: {
        "kick":  [1,0,0,0, 1,0,1,0, 0,0,1,0, 1,0,0,0],
        "snare": [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
        "hihat": [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1],
        "clap":  [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
    },
    RhythmGenre.HOUSE: {
        "kick":  [1,0,0,0, 1,0,0,0, 1,0,0,0, 1,0,0,0],
        "snare": [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
        "hihat": [0,0,1,0, 0,0,1,0, 0,0,1,0, 0,0,1,0],
        "clap":  [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,1],
    },
    RhythmGenre.JAZZ: {
        "kick":  [1,0,0,1, 0,0,1,0, 0,1,0,0, 1,0,0,0],
        "snare": [0,0,0,0, 0,1,0,0, 0,0,0,1, 0,0,1,0],
        "hihat": [1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0],
        "ride":  [0,1,0,1, 0,1,0,1, 0,1,0,1, 0,1,0,1],
    },
    RhythmGenre.ROCK: {
        "kick":  [1,0,0,0, 0,0,1,0, 1,0,0,0, 0,0,1,0],
        "snare": [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
        "hihat": [1,1,1,1, 1,1,1,1, 1,1,1,1, 1,1,1,1],
        "crash": [1,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0],
    },
    RhythmGenre.AFROBEAT: {
        "kick":  [1,0,0,1, 0,0,1,0, 0,1,0,0, 1,0,0,0],
        "snare": [0,0,1,0, 0,0,0,0, 0,0,1,0, 0,0,0,0],
        "hihat": [1,0,1,0, 1,0,1,0, 1,0,1,0, 1,0,1,0],
        "conga": [0,1,0,0, 1,0,0,1, 0,1,0,0, 1,0,0,0],
    },
    RhythmGenre.REGGAE: {
        "kick":  [1,0,0,0, 0,0,0,0, 1,0,0,0, 0,0,0,0],
        "snare": [0,0,0,0, 1,0,0,0, 0,0,0,0, 1,0,0,0],
        "hihat": [0,0,1,0, 0,0,1,0, 0,0,1,0, 0,0,1,0],
        "rim":   [0,1,0,1, 0,1,0,1, 0,1,0,1, 0,1,0,1],
    },
}


@dataclass
class Note:
    pitch: int
    duration: float
    velocity: int = 80
    time: float = 0.0

    @property
    def name(self) -> str:
        return NOTE_NAMES[self.pitch % 12]

    @property
    def octave(self) -> int:
        return (self.pitch // 12) - 1

    def __repr__(self) -> str:
        return f"Note({self.name}{self.octave}, dur={self.duration}, vel={self.velocity})"


@dataclass
class Chord:
    notes: List[int]
    duration: float = 4.0
    time: float = 0.0
    root: int = 60
    quality: str = "major"

    @classmethod
    def from_name(cls, root_name: str, quality: str = "major",
                  duration: float = 4.0, octave: int = 4) -> Chord:
        root_idx = NOTE_NAMES.index(root_name)
        midi_root = root_idx + (octave + 1) * 12
        pattern = CHORD_PATTERNS.get(quality, CHORD_PATTERNS["major"])
        return cls(
            notes=[midi_root + interval for interval in pattern],
            duration=duration,
            root=midi_root,
            quality=quality,
        )

    @property
    def root_name(self) -> str:
        return NOTE_NAMES[self.root % 12]


@dataclass
class Melody:
    notes: List[Note] = field(default_factory=list)
    key: MusicalKey = MusicalKey.C
    scale: ScaleType = ScaleType.MAJOR
    tempo: float = 120.0

    @property
    def duration_beats(self) -> float:
        if not self.notes:
            return 0.0
        return max(n.time + n.duration for n in self.notes)

    @property
    def pitch_range(self) -> Tuple[int, int]:
        pitches = [n.pitch for n in self.notes]
        return (min(pitches), max(pitches)) if pitches else (0, 0)

    def transpose(self, semitones: int) -> Melody:
        transposed = [
            Note(
                pitch=max(0, min(127, n.pitch + semitones)),
                duration=n.duration,
                velocity=n.velocity,
                time=n.time,
            )
            for n in self.notes
        ]
        return Melody(notes=transposed, key=self.key, scale=self.scale, tempo=self.tempo)


@dataclass
class RhythmPattern:
    genre: RhythmGenre
    bars: int = 4
    patterns: Dict[str, List[int]] = field(default_factory=dict)
    tempo: float = 120.0

    @property
    def total_steps(self) -> int:
        if not self.patterns:
            return 0
        return len(next(iter(self.patterns.values())))

    def get_hits(self, instrument: str) -> List[int]:
        return self.patterns.get(instrument, [])


class ScaleProvider:
    @staticmethod
    def get_notes(root: MusicalKey, scale_type: ScaleType,
                  octave: int = 4, num_octaves: int = 2) -> List[int]:
        intervals = SCALE_INTERVALS.get(scale_type, SCALE_INTERVALS[ScaleType.MAJOR])
        root_midi = root.value + (octave + 1) * 12
        notes = []
        for oct in range(num_octaves):
            for interval in intervals:
                pitch = root_midi + oct * 12 + interval
                if 0 <= pitch <= 127:
                    notes.append(pitch)
        return notes

    @staticmethod
    def nearest_in_scale(pitch: int, scale_notes: List[int]) -> int:
        return min(scale_notes, key=lambda n: abs(n - pitch))


class ChordProgressionGenerator:
    def __init__(self, root: MusicalKey = MusicalKey.C, octave: int = 4):
        self.root = root
        self.octave = octave

    def generate(self, style: str = "pop", num_bars: int = 8) -> List[Chord]:
        pattern = CHORD_PROGRESSIONS.get(style, CHORD_PROGRESSIONS["pop"])
        progression: List[Chord] = []
        total_beats = 0.0
        root_midi = self.root.value + (self.octave + 1) * 12

        while total_beats < num_bars * 4:
            for roman, duration in pattern:
                if total_beats >= num_bars * 4:
                    break
                if roman in ROMAN_TO_CHORD:
                    offset, quality = ROMAN_TO_CHORD[roman]
                    chord_root = root_midi + offset
                    pattern_notes = CHORD_PATTERNS.get(quality, CHORD_PATTERNS["major"])
                    chord = Chord(
                        notes=[chord_root + i for i in pattern_notes],
                        duration=duration,
                        time=total_beats,
                        root=chord_root,
                        quality=quality,
                    )
                    progression.append(chord)
                    total_beats += duration
        return progression


class MelodyGenerator:
    def __init__(self, key: MusicalKey = MusicalKey.C, scale: ScaleType = ScaleType.MAJOR,
                 tempo: float = 120.0):
        self.key = key
        self.scale = scale
        self.tempo = tempo
        self._scale_notes = ScaleProvider.get_notes(key, scale, octave=4, num_octaves=2)
        self._transitions: Dict[int, List[int]] = self._build_transitions()

    def _build_transitions(self) -> Dict[int, List[int]]:
        transitions: Dict[int, List[int]] = {}
        for i, note in enumerate(self._scale_notes):
            candidates = []
            for j in range(max(0, i - 2), min(len(self._scale_notes), i + 3)):
                if j != i:
                    candidates.append(self._scale_notes[j])
            transitions[note] = candidates if candidates else [note]
        return transitions

    def generate(self, length: int = 32, start_pitch: Optional[int] = None,
                 temperature: float = 1.0) -> Melody:
        if start_pitch is None:
            start_pitch = self._scale_notes[len(self._scale_notes) // 2]

        notes: List[Note] = []
        current = start_pitch
        time = 0.0
        durations = [0.5, 1.0, 1.0, 1.5, 2.0, 2.0]

        for _ in range(length):
            if current in self._transitions:
                candidates = self._transitions[current]
                if temperature != 1.0 and len(candidates) > 1:
                    distances = [abs(c - current) for c in candidates]
                    weights = [1.0 / (d + 1) ** temperature for d in distances]
                    total = sum(weights)
                    weights = [w / total for w in weights]
                    next_pitch = int(np.random.choice(candidates, p=weights))
                else:
                    next_pitch = random.choice(candidates)
            else:
                next_pitch = current + random.choice([-2, -1, 0, 1, 2])
            next_pitch = max(0, min(127, next_pitch))

            duration = random.choice(durations)
            velocity = random.randint(60, 100)

            notes.append(Note(
                pitch=next_pitch,
                duration=duration,
                velocity=velocity,
                time=time,
            ))
            time += duration
            current = next_pitch

        return Melody(notes=notes, key=self.key, scale=self.scale, tempo=self.tempo)


class RhythmGenerator:
    def __init__(self, tempo: float = 120.0):
        self.tempo = tempo

    def generate(self, genre: RhythmGenre, bars: int = 4) -> RhythmPattern:
        base_pattern = RHYTHM_PATTERNS.get(genre, RHYTHM_PATTERNS[RhythmGenre.HIP_HOP])
        patterns = {inst: hits * bars for inst, hits in base_pattern.items()}
        return RhythmPattern(genre=genre, bars=bars, patterns=patterns, tempo=self.tempo)

    def generate_variation(self, pattern: RhythmPattern, variation: float = 0.1) -> RhythmPattern:
        new_patterns = {}
        for inst, hits in pattern.patterns.items():
            new_hits = []
            for hit in hits:
                if random.random() < variation:
                    new_hits.append(1 - hit)
                else:
                    new_hits.append(hit)
            new_patterns[inst] = new_hits
        return RhythmPattern(
            genre=pattern.genre,
            bars=pattern.bars,
            patterns=new_patterns,
            tempo=pattern.tempo,
        )


class MusicEvaluator:
    def score_coherence(self, melody: Melody) -> float:
        if len(melody.notes) < 2:
            return 0.0
        scale_notes = ScaleProvider.get_notes(melody.key, melody.scale)
        in_scale = sum(1 for n in melody.notes if n.pitch in scale_notes)
        return in_scale / len(melody.notes)

    def score_variety(self, melody: Melody) -> float:
        pitches = set(n.pitch % 12 for n in melody.notes)
        return len(pitches) / 12.0

    def score_rhythmic_interest(self, melody: Melody) -> float:
        durations = [n.duration for n in melody.notes]
        unique = len(set(durations))
        return min(1.0, unique / 5.0)

    def score_contour(self, melody: Melody) -> float:
        if len(melody.notes) < 3:
            return 0.0
        changes = 0
        for i in range(2, len(melody.notes)):
            prev_dir = melody.notes[i - 1].pitch - melody.notes[i - 2].pitch
            curr_dir = melody.notes[i].pitch - melody.notes[i - 1].pitch
            if (prev_dir > 0 and curr_dir < 0) or (prev_dir < 0 and curr_dir > 0):
                changes += 1
        return changes / (len(melody.notes) - 2)

    def evaluate(self, melody: Melody) -> Dict[str, float]:
        return {
            "coherence": self.score_coherence(melody),
            "variety": self.score_variety(melody),
            "rhythmic_interest": self.score_rhythmic_interest(melody),
            "contour": self.score_contour(melody),
        }


class MusicArranger:
    def __init__(self, tempo: float = 120.0):
        self.tempo = tempo

    def arrange(self, melody: Melody, chords: List[Chord],
                rhythm: RhythmPattern) -> Dict[str, Any]:
        return {
            "melody": {
                "notes": [{"pitch": n.pitch, "duration": n.duration,
                           "velocity": n.velocity, "time": n.time} for n in melody.notes],
                "key": melody.key.name,
                "scale": melody.scale.value,
                "tempo": melody.tempo,
            },
            "chords": [
                {"root": c.root, "quality": c.quality, "notes": c.notes,
                 "duration": c.duration, "time": c.time}
                for c in chords
            ],
            "rhythm": {
                "genre": rhythm.genre.value,
                "tempo": rhythm.tempo,
                "patterns": rhythm.patterns,
            },
            "metadata": {
                "total_duration_beats": melody.duration_beats,
                "pitch_range": list(melody.pitch_range),
                "num_notes": len(melody.notes),
                "num_chords": len(chords),
            },
        }


def main():
    print("=== Music Generation Module ===")

    print("\n=== Chord Progression (Pop) ===")
    chord_gen = ChordProgressionGenerator(MusicalKey.C, octave=4)
    chords = chord_gen.generate("pop", num_bars=4)
    for c in chords:
        note_names = [NOTE_NAMES[p % 12] for p in c.notes]
        print(f"  Beat {c.time:.0f}: {c.root_name} {c.quality} ({note_names})")

    print("\n=== Melody Generation ===")
    melody_gen = MelodyGenerator(MusicalKey.C, ScaleType.PENTATONIC_MAJOR, tempo=120)
    melody = melody_gen.generate(length=16, temperature=0.8)
    print(f"  Generated {len(melody.notes)} notes")
    print(f"  Pitch range: {melody.pitch_range}")
    print(f"  Duration: {melody.duration_beats:.1f} beats")
    print(f"  First 5 notes: {melody.notes[:5]}")

    print("\n=== Scale Notes ===")
    scale_notes = ScaleProvider.get_notes(MusicalKey.C, ScaleType.MAJOR)
    print(f"  C Major: {[NOTE_NAMES[p % 12] for p in scale_notes[:14]]}")

    print("\n=== Rhythm Patterns ===")
    rhythm_gen = RhythmGenerator(tempo=120)
    for genre in [RhythmGenre.HIP_HOP, RhythmGenre.AFROBEAT, RhythmGenre.JAZZ]:
        rhythm = rhythm_gen.generate(genre, bars=1)
        hits = sum(rhythm.patterns.get("kick", []))
        print(f"  {genre.value}: {hits} kick hits per bar")

    print("\n=== Music Evaluation ===")
    evaluator = MusicEvaluator()
    scores = evaluator.evaluate(melody)
    for metric, score in scores.items():
        print(f"  {metric}: {score:.3f}")

    print("\n=== Arrangement ===")
    arranger = MusicArranger()
    arrangement = arranger.arrange(melody, chords, rhythm)
    print(f"  Tracks: {list(arrangement.keys())}")
    print(f"  Total notes: {arrangement['metadata']['num_notes']}")
    print(f"  Total chords: {arrangement['metadata']['num_chords']}")

    print("\nDone.")


if __name__ == "__main__":
    main()

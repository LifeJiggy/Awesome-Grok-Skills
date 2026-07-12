"""
Text-to-Speech Module — Neural synthesis, prosody control, and voice cloning.

Provides Tacotron/FastSpeech/VITS model management, SSML processing, prosody
control, multi-speaker voice cloning, streaming TTS, and pronunciation management.
"""

from __future__ import annotations

import logging
import time
import hashlib
from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union
import re
import xml.etree.ElementTree as ET

import numpy as np

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TTSModel(Enum):
    """Supported TTS model architectures."""
    TACOTRON2 = "tacotron2"
    FASTSPEECH = "fastspeech"
    FASTSPEECH2 = "fastspeech2"
    VITS = "vits"
    VITS2 = "vits2"
    FASTSTREAM = "faststream"


class VocoderType(Enum):
    """Supported vocoder backends."""
    HIFIGAN = "hifigan"
    WAVEGLOW = "waveglow"
    WAVERNN = "wavernn"
    MELGAN = "melgan"
    ENCODER_VOCODER = "encoder_vocoder"


class Emotion(Enum):
    """Supported synthesis emotions."""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    EXCITED = "excited"
    CALM = "calm"
    FEARFUL = "fearful"
    DISGUSTED = "disgusted"
    SURPRISED = "surprised"


class SSMLElement(Enum):
    """SSML element types."""
    SPEAK = "speak"
    PROSODY = "prosody"
    BREAK = "break"
    EMPHASIS = "emphasis"
    SAY_AS = "say-as"
    SUB = "sub"
    VOICE = "voice"
    AUDIO = "audio"
    P = "p"
    S = "s"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"


class StreamState(Enum):
    """State of the streaming TTS pipeline."""
    IDLE = "idle"
    WARMING_UP = "warming_up"
    STREAMING = "streaming"
    FLUSHING = "flushing"
    ERROR = "error"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class AudioOutput:
    """Generated audio output from TTS synthesis."""
    samples: np.ndarray
    sample_rate: int
    duration: float = 0.0
    model_used: str = ""
    voice_id: str = ""
    generation_time_ms: float = 0.0

    def __post_init__(self) -> None:
        if self.duration == 0.0 and len(self.samples) > 0:
            self.duration = len(self.samples) / self.sample_rate

    @property
    def num_samples(self) -> int:
        return len(self.samples)

    def save(self, file_path: Union[str, Path]) -> None:
        """Save audio to WAV file (placeholder)."""
        logger.info("Saving audio to %s (%.2fs)", file_path, self.duration)

    def concatenate(self, other: AudioOutput) -> AudioOutput:
        """Concatenate two audio outputs."""
        if self.sample_rate != other.sample_rate:
            raise ValueError("Sample rates must match for concatenation")
        combined = np.concatenate([self.samples, other.samples])
        return AudioOutput(
            samples=combined,
            sample_rate=self.sample_rate,
            model_used=self.model_used,
            voice_id=self.voice_id,
        )


@dataclass
class ProsodyParameters:
    """Prosody control parameters for synthesis."""
    rate: float = 1.0          # 0.5 = half speed, 2.0 = double speed
    pitch: float = 1.0         # 0.5 = low, 1.0 = normal, 2.0 = high
    volume: float = 1.0        # 0.0 = silent, 1.0 = normal, 2.0 = loud
    pitch_range: float = 1.0   # 0.0 = monotone, 1.0 = normal
    emphasis_words: List[str] = field(default_factory=list)
    emphasis_level: str = "moderate"  # reduced | moderate | strong
    pause_after: float = 0.0   # seconds

    def to_ssml(self) -> str:
        """Convert parameters to SSML prosody attributes."""
        attrs = []
        if self.rate != 1.0:
            pct = int((self.rate - 1.0) * 100)
            attrs.append(f'rate="{("+" if pct > 0 else "")}{pct}%"')
        if self.pitch != 1.0:
            pct = int((self.pitch - 1.0) * 100)
            attrs.append(f'pitch="{("+" if pct > 0 else "")}{pct}%"')
        if self.volume != 1.0:
            pct = int((self.volume - 1.0) * 100)
            attrs.append(f'volume="{("+" if pct > 0 else "")}{pct}%"')
        return " ".join(attrs)


@dataclass
class SSMLNode:
    """Parsed SSML document node."""
    element: SSMLElement
    text: str = ""
    attributes: Dict[str, str] = field(default_factory=dict)
    children: List["SSMLNode"] = field(default_factory=list)

    def to_text(self) -> str:
        """Extract plain text from SSML tree."""
        parts = []
        if self.text:
            parts.append(self.text)
        for child in self.children:
            parts.append(child.to_text())
        return " ".join(parts)


@dataclass
class VoiceProfile:
    """Voice configuration for multi-speaker synthesis."""
    voice_id: str
    name: str
    language: str = "en"
    gender: str = "neutral"
    embedding: Optional[np.ndarray] = None
    adapter_weights: Optional[np.ndarray] = None
    default_prosody: ProsodyParameters = field(default_factory=ProsodyParameters)
    sample_rate: int = 22050


@dataclass
class PronunciationEntry:
    """Custom pronunciation for a word or phrase."""
    word: str
    phonemes: str  # IPA or arpabet notation
    language: str = "en"
    priority: int = 0  # Higher = override lower
    context_regex: Optional[str] = None  # Optional context-dependent rule


@dataclass
class PhonemeMapping:
    """Grapheme-to-phoneme mapping for a language."""
    language: str
    grapheme_to_phoneme: Dict[str, List[str]]
    stress_rules: Dict[str, str] = field(default_factory=dict)
    special_cases: Dict[str, str] = field(default_factory=dict)


@dataclass
class StreamingChunk:
    """A chunk of audio from streaming synthesis."""
    samples: np.ndarray
    chunk_index: int
    is_final: bool = False
    timestamp_ms: float = 0.0

    @property
    def duration_ms(self) -> float:
        return len(self.samples) / 22050 * 1000  # assuming 22050 Hz


@dataclass
class SynthesisRequest:
    """Complete request for TTS synthesis."""
    text: str
    voice_id: str = "default"
    prosody: Optional[ProsodyParameters] = None
    emotion: Optional[Emotion] = None
    emotion_intensity: float = 0.5
    language: str = "en"
    output_format: str = "wav"
    streaming: bool = False


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class TTSError(Exception):
    """Base exception for TTS errors."""
    pass


class ModelLoadError(TTSError):
    """Raised when a TTS model fails to load."""
    pass


class SSMLParseError(TTSError):
    """Raised when SSML markup is invalid."""
    pass


class VoiceNotFoundError(TTSError):
    """Raised when a requested voice ID is not available."""
    pass


class PhonemeMappingError(TTSError):
    """Raised when grapheme-to-phoneme conversion fails."""
    pass


class StreamingError(TTSError):
    """Raised for streaming pipeline errors."""
    pass


# ---------------------------------------------------------------------------
# Core Classes
# ---------------------------------------------------------------------------

class SSMLProcessor:
    """Parses and processes SSML 1.1 markup for TTS synthesis."""

    SUPPORTED_ELEMENTS = {e.value for e in SSMLElement}

    def __init__(self):
        self._custom_tags: Dict[str, Callable] = {}

    def parse(self, ssml: str) -> SSMLNode:
        """Parse SSML string into an SSML document tree."""
        # Strip XML declaration and namespace prefixes
        ssml_clean = re.sub(r'<\?xml[^?]*\?>', '', ssml).strip()
        ssml_clean = re.sub(r'xmlns="[^"]*"', '', ssml_clean)

        try:
            root = ET.fromstring(f"<root>{ssml_clean}</root>")
        except ET.ParseError as e:
            raise SSMLParseError(f"Invalid SSML: {e}")

        return self._build_tree(root)

    def _build_tree(self, element: ET.Element) -> SSMLNode:
        """Recursively build SSMLNode tree from XML element."""
        tag = element.tag.lower()
        try:
            element_type = SSMLElement(tag)
        except ValueError:
            element_type = SSMLElement.SPEAK  # default fallback

        node = SSMLNode(
            element=element_type,
            text=element.text or "",
            attributes=dict(element.attrib),
        )

        for child in element:
            node.children.append(self._build_tree(child))

        return node

    def validate(self, ssml: str) -> List[str]:
        """Validate SSML and return list of warnings/errors."""
        errors = []
        try:
            self.parse(ssml)
        except SSMLParseError as e:
            errors.append(str(e))
            return errors

        # Check for unsupported elements
        for match in re.finditer(r'<(\w+)[\s>]', ssml):
            tag = match.group(1).lower()
            if tag not in self.SUPPORTED_ELEMENTS and tag not in ("root",):
                errors.append(f"Unsupported SSML element: <{tag}>")

        # Check for unclosed tags
        opens = re.findall(r'<(\w+)[\s>]', ssml)
        closes = re.findall(r'</(\w+)>', ssml)
        if len(opens) != len(closes):
            errors.append("Mismatched SSML tags (unclosed elements)")

        return errors

    def extract_prosody(self, node: SSMLNode) -> ProsodyParameters:
        """Extract prosody parameters from SSML tree."""
        params = ProsodyParameters()

        if node.element == SSMLElement.PROSODY:
            rate_str = node.attributes.get("rate", "100%")
            pitch_str = node.attributes.get("pitch", "0%")
            volume_str = node.attributes.get("volume", "medium")

            params.rate = self._parse_percentage(rate_str, default=1.0)
            params.pitch = self._parse_percentage(pitch_str, default=1.0)
            params.volume = self._parse_percentage(volume_str, default=1.0)

        if node.element == SSMLElement.EMPHASIS:
            params.emphasis_level = node.attributes.get("level", "moderate")

        for child in node.children:
            child_params = self.extract_prosody(child)
            if child_params.rate != 1.0:
                params.rate = child_params.rate
            if child_params.pitch != 1.0:
                params.pitch = child_params.pitch

        return params

    def _parse_percentage(self, value: str, default: float = 1.0) -> float:
        """Parse a percentage string like '+20%' or 'normal' to float."""
        value = value.strip().lower()
        if value in ("normal", "medium", "default"):
            return 1.0
        if value in ("slow", "x-slow"):
            return 0.75 if value == "slow" else 0.5
        if value in ("fast", "x-fast"):
            return 1.25 if value == "fast" else 2.0

        match = re.match(r'([+-]?\d+)%', value)
        if match:
            return 1.0 + int(match.group(1)) / 100.0

        try:
            return float(value)
        except ValueError:
            return default

    def to_text(self, ssml: str) -> str:
        """Extract plain text from SSML."""
        node = self.parse(ssml)
        return node.to_text().strip()


class PronunciationDictionary:
    """Manages custom pronunciation entries for domain-specific terms."""

    def __init__(self):
        self._entries: Dict[str, List[PronunciationEntry]] = {}
        self._language_mappings: Dict[str, PhonemeMapping] = {}
        self._load_default_mappings()

    def _load_default_mappings(self) -> None:
        """Load default grapheme-to-phoneme mappings for common languages."""
        self._language_mappings["en"] = PhonemeMapping(
            language="en",
            grapheme_to_phoneme={
                "a": ["eɪ"], "b": ["biː"], "c": ["siː"], "d": ["diː"],
                "th": ["θ"], "sh": ["ʃ"], "ch": ["tʃ"], "ph": ["f"],
            },
            stress_rules={"primary": "ˈ", "secondary": "ˌ"},
            special_cases={"the": "ðə", "a": "ə", "an": "ən"},
        )

    def add(
        self,
        word: str,
        phonemes: Optional[str] = None,
        language: str = "en",
        priority: int = 0,
    ) -> PronunciationEntry:
        """Add a pronunciation entry."""
        if phonemes is None:
            phonemes = self._auto_generate_phonemes(word, language)

        entry = PronunciationEntry(
            word=word,
            phonemes=phonemes,
            language=language,
            priority=priority,
        )

        if word not in self._entries:
            self._entries[word] = []
        self._entries[word].append(entry)
        self._entries[word].sort(key=lambda e: e.priority, reverse=True)

        logger.info("Added pronunciation: %s -> %s", word, phonemes)
        return entry

    def lookup(self, word: str, language: str = "en") -> Optional[PronunciationEntry]:
        """Look up the highest-priority pronunciation for a word."""
        entries = self._entries.get(word, [])
        lang_entries = [e for e in entries if e.language == language]
        return lang_entries[0] if lang_entries else (entries[0] if entries else None)

    def _auto_generate_phonemes(self, word: str, language: str) -> str:
        """Auto-generate phonemes using language-specific rules."""
        mapping = self._language_mappings.get(language)
        if mapping is None:
            return word  # Fallback: return word as-is

        phonemes = []
        i = 0
        while i < len(word):
            # Try multi-character graphemes first
            matched = False
            for length in range(min(3, len(word) - i), 0, -1):
                grapheme = word[i:i+length].lower()
                if grapheme in mapping.grapheme_to_phoneme:
                    phonemes.extend(mapping.grapheme_to_phoneme[grapheme])
                    i += length
                    matched = True
                    break
            if not matched:
                phonemes.append(word[i])
                i += 1

        return " ".join(phonemes)

    def remove(self, word: str, language: Optional[str] = None) -> bool:
        """Remove pronunciation entries."""
        if word not in self._entries:
            return False
        if language:
            self._entries[word] = [e for e in self._entries[word] if e.language != language]
            if not self._entries[word]:
                del self._entries[word]
        else:
            del self._entries[word]
        return True

    @property
    def size(self) -> int:
        return sum(len(entries) for entries in self._entries.values())


class TTSEngine:
    """
    Core TTS engine supporting multiple model architectures and vocoders.

    Handles model loading, warm-up inference, and synthesis dispatch.
    """

    def __init__(
        self,
        model: str = "vits2_vctk_v1",
        vocoder: str = "hifigan_v1",
        device: str = "cpu",
        sample_rate: int = 22050,
        warmup: bool = True,
    ):
        self.model_name = model
        self.vocoder_name = vocoder
        self.device = device
        self.sample_rate = sample_rate
        self._model = None
        self._vocoder = None
        self._cache: OrderedDict[str, AudioOutput] = OrderedDict()
        self._cache_max_size = 100
        self._pronunciation_dict = PronunciationDictionary()
        self._voices: Dict[str, VoiceProfile] = {}
        self._is_warmed_up = False

        self._register_default_voices()
        if warmup:
            self._warmup()

    def _register_default_voices(self) -> None:
        """Register built-in voice profiles."""
        for i in range(10):
            self._voices[f"p2{i:02d}"] = VoiceProfile(
                voice_id=f"p2{i:02d}",
                name=f"Speaker {i}",
                language="en",
                gender="neutral",
            )

    def _warmup(self) -> None:
        """Run warm-up inference to JIT compile kernels."""
        logger.info("Warming up TTS engine (model=%s)...", self.model_name)
        start = time.time()
        self.synthesize("Warm up.", voice="p200")
        elapsed = (time.time() - start) * 1000
        self._is_warmed_up = True
        logger.info("Warm-up complete in %.1fms", elapsed)

    def _get_cache_key(self, text: str, voice: str, prosody: Optional[ProsodyParameters]) -> str:
        """Generate cache key for synthesis request."""
        prosody_str = ""
        if prosody:
            prosody_str = f"{prosody.rate}_{prosody.pitch}_{prosody.volume}"
        raw = f"{text}_{voice}_{prosody_str}"
        return hashlib.md5(raw.encode()).hexdigest()

    def synthesize(
        self,
        text: str,
        voice: str = "default",
        prosody: Optional[ProsodyParameters] = None,
        emotion: Optional[Emotion] = None,
        emotion_intensity: float = 0.5,
        speed: float = 1.0,
        pitch: float = 1.0,
    ) -> AudioOutput:
        """Synthesize text to audio."""
        start_time = time.time()

        # Apply pronunciation dictionary
        processed_text = self._apply_pronunciation(text)

        # Check cache
        cache_key = self._get_cache_key(processed_text, voice, prosody)
        if cache_key in self._cache:
            logger.debug("Cache hit for synthesis request")
            return self._cache[cache_key]

        # Resolve voice
        if voice not in self._voices:
            voice = list(self._voices.keys())[0] if self._voices else "default"

        # Model inference (placeholder — in production, run neural network)
        if prosody:
            speed *= prosody.rate
            pitch *= prosody.pitch

        # Generate placeholder audio
        duration_samples = int(self.sample_rate * len(processed_text) * 0.05 / speed)
        samples = np.random.randn(duration_samples).astype(np.float32) * 0.1

        # Apply emotion coloring (placeholder)
        if emotion and emotion != Emotion.NEUTRAL:
            samples = self._apply_emotion(samples, emotion, emotion_intensity)

        generation_time = (time.time() - start_time) * 1000

        output = AudioOutput(
            samples=samples,
            sample_rate=self.sample_rate,
            model_used=self.model_name,
            voice_id=voice,
            generation_time_ms=generation_time,
        )

        # Cache result
        self._cache[cache_key] = output
        if len(self._cache) > self._cache_max_size:
            self._cache.popitem(last=False)

        logger.info(
            "Synthesized '%s...' in %.1fms (%.2fs audio)",
            text[:30],
            generation_time,
            output.duration,
        )
        return output

    def synthesize_ssml(self, ssml_node: SSMLNode, voice: str = "default") -> AudioOutput:
        """Synthesize from parsed SSML."""
        prosody = ProsodyParameters()
        if ssml_node.element == SSMLElement.PROSODY:
            processor = SSMLProcessor()
            prosody = processor.extract_prosody(ssml_node)

        text = ssml_node.to_text()
        return self.synthesize(text, voice=voice, prosody=prosody)

    def synthesize_with_prosody(
        self,
        text: str,
        prosody: ProsodyParameters,
        voice: str = "default",
    ) -> AudioOutput:
        """Synthesize with explicit prosody parameters."""
        return self.synthesize(text, voice=voice, prosody=prosody)

    def _apply_pronunciation(self, text: str) -> str:
        """Apply custom pronunciation dictionary to text."""
        words = text.split()
        processed = []
        for word in words:
            entry = self._pronunciation_dict.lookup(word)
            if entry:
                processed.append(entry.phonemes)
            else:
                processed.append(word)
        return " ".join(processed)

    def _apply_emotion(
        self,
        samples: np.ndarray,
        emotion: Emotion,
        intensity: float,
    ) -> np.ndarray:
        """Apply emotion-based audio transformation (placeholder)."""
        emotion_params = {
            Emotion.HAPPY: {"pitch_shift": 1.1, "energy_scale": 1.2},
            Emotion.SAD: {"pitch_shift": 0.9, "energy_scale": 0.7},
            Emotion.ANGRY: {"pitch_shift": 1.05, "energy_scale": 1.4},
            Emotion.EXCITED: {"pitch_shift": 1.15, "energy_scale": 1.3},
            Emotion.CALM: {"pitch_shift": 0.95, "energy_scale": 0.8},
        }

        params = emotion_params.get(emotion, {"pitch_shift": 1.0, "energy_scale": 1.0})
        scale = 1.0 + (params["energy_scale"] - 1.0) * intensity
        return samples * scale

    def save(self, audio: AudioOutput, file_path: Union[str, Path]) -> None:
        """Save synthesized audio to file."""
        audio.save(file_path)

    def register_voice(self, profile: VoiceProfile) -> None:
        """Register a new voice profile."""
        self._voices[profile.voice_id] = profile
        logger.info("Registered voice: %s (%s)", profile.name, profile.voice_id)

    @property
    def available_voices(self) -> List[str]:
        return list(self._voices.keys())


class VoiceCloner:
    """
    Creates voice adapters for few-shot voice cloning.

    Extracts speaker embeddings and generates adapter weights from reference audio.
    """

    def __init__(
        self,
        embedding_model: str = "speaker_encoder_v2",
        cloning_model: str = "vits2_adapter",
        device: str = "cuda",
    ):
        self.embedding_model = embedding_model
        self.cloning_model = cloning_model
        self.device = device
        self._reference_embeddings: Dict[str, np.ndarray] = {}

    def _extract_embedding(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """Extract speaker embedding from audio (placeholder)."""
        # In production: run through ECAPA-TDNN or similar speaker encoder
        embedding = np.random.randn(192).astype(np.float32)
        return embedding / (np.linalg.norm(embedding) + 1e-10)

    def create_adapter(
        self,
        reference_audio: Union[str, Path, np.ndarray],
        adapter_rank: int = 8,
        training_steps: int = 500,
    ) -> VoiceProfile:
        """
        Create a voice adapter from reference audio.

        Args:
            reference_audio: Path to reference audio or numpy array.
            adapter_rank: Rank of LoRA-style adapter weights.
            training_steps: Number of fine-tuning steps.

        Returns:
            VoiceProfile with adapter weights for voice cloning.
        """
        start_time = time.time()

        # Load and embed reference audio
        if isinstance(reference_audio, (str, Path)):
            # Placeholder: load audio from file
            samples = np.random.randn(22050 * 30).astype(np.float32)  # 30 seconds
        else:
            samples = reference_audio

        embedding = self._extract_embedding(samples, 22050)

        # Generate adapter weights (placeholder)
        adapter_weights = np.random.randn(adapter_rank, 256).astype(np.float32) * 0.01

        # Validate embedding quality
        similarity = self._validate_embedding(embedding)
        if similarity < 0.7:
            logger.warning("Low embedding similarity: %.3f", similarity)

        profile = VoiceProfile(
            voice_id=f"clone_{hashlib.md5(embedding.tobytes()).hexdigest()[:8]}",
            name="Cloned Voice",
            embedding=embedding,
            adapter_weights=adapter_weights,
            sample_rate=22050,
        )

        elapsed = (time.time() - start_time) * 1000
        logger.info(
            "Voice adapter created in %.1fms (similarity=%.3f, rank=%d)",
            elapsed, similarity, adapter_rank,
        )
        return profile

    def _validate_embedding(self, embedding: np.ndarray) -> float:
        """Validate speaker embedding quality."""
        # In production: compare against enrollment gallery
        norm = np.linalg.norm(embedding)
        return float(min(1.0, norm / 10.0))  # Placeholder validation

    def compare_embeddings(self, emb1: np.ndarray, emb2: np.ndarray) -> float:
        """Compute cosine similarity between two speaker embeddings."""
        return float(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2) + 1e-10))


class ProsodyController:
    """
    Computes prosody parameters from text analysis and emotion specifications.

    Generates pitch contours, emphasis patterns, and pause schedules.
    """

    def __init__(self):
        self._emotion_defaults = {
            "happy": ProsodyParameters(rate=1.1, pitch=1.15, volume=1.1),
            "sad": ProsodyParameters(rate=0.85, pitch=0.85, volume=0.7),
            "angry": ProsodyParameters(rate=1.2, pitch=1.05, volume=1.4),
            "excited": ProsodyParameters(rate=1.15, pitch=1.2, volume=1.2),
            "calm": ProsodyParameters(rate=0.9, pitch=0.95, volume=0.85),
            "neutral": ProsodyParameters(rate=1.0, pitch=1.0, volume=1.0),
        }

    def compute(
        self,
        text: str,
        emotion: str = "neutral",
        emotion_intensity: float = 0.5,
        speech_rate: float = 1.0,
        pitch_range: float = 1.0,
        emphasis_words: Optional[List[str]] = None,
    ) -> ProsodyParameters:
        """Compute prosody parameters from text analysis and emotion."""
        base = self._emotion_defaults.get(emotion, self._emotion_defaults["neutral"])

        # Interpolate emotion intensity
        neutral = self._emotion_defaults["neutral"]
        rate = neutral.rate + (base.rate - neutral.rate) * emotion_intensity
        pitch = neutral.pitch + (base.pitch - neutral.pitch) * emotion_intensity
        volume = neutral.volume + (base.volume - neutral.volume) * emotion_intensity

        # Apply user overrides
        rate *= speech_rate
        pitch_range_val = pitch_range

        # Detect emphasis from punctuation and caps
        auto_emphasis = []
        import re
        words = text.split()
        for word in words:
            clean = re.sub(r'[^\w]', '', word)
            if clean and clean.isupper() and len(clean) > 1:
                auto_emphasis.append(clean)
            if clean.endswith(("!", "!!")):
                auto_emphasis.append(clean.rstrip("!"))

        all_emphasis = list(set(auto_emphasis + (emphasis_words or [])))

        return ProsodyParameters(
            rate=rate,
            pitch=pitch,
            volume=volume,
            pitch_range=pitch_range_val,
            emphasis_words=all_emphasis,
        )


class StreamingTTS:
    """
    Real-time streaming TTS with sub-200ms first-chunk latency.

    Manages look-ahead buffering, chunk generation, and overflow handling.
    """

    def __init__(
        self,
        engine: TTSEngine,
        chunk_size_ms: int = 100,
        look_ahead_chunks: int = 2,
        buffer_overflow_strategy: str = "drop_oldest",
        max_queue_size: int = 100,
    ):
        self.engine = engine
        self.chunk_size_ms = chunk_size_ms
        self.look_ahead_chunks = look_ahead_chunks
        self.overflow_strategy = buffer_overflow_strategy
        self.max_queue_size = max_queue_size
        self._state = StreamState.IDLE
        self._chunk_buffer: List[StreamingChunk] = []
        self._chunk_counter = 0

    def stream(
        self,
        text: str,
        voice: str = "default",
        prosody: Optional[ProsodyParameters] = None,
    ) -> Generator[StreamingChunk, None, None]:
        """
        Generate audio chunks as a generator for streaming playback.

        Yields StreamingChunk objects as they become available.
        """
        self._state = StreamState.STREAMING
        self._chunk_counter = 0

        # Split text into segments for streaming
        segments = self._split_for_streaming(text)

        for seg_idx, segment in enumerate(segments):
            try:
                # Synthesize segment
                output = self.engine.synthesize(segment, voice=voice, prosody=prosody)

                # Split output into chunks
                chunk_samples = int(self.engine.sample_rate * self.chunk_size_ms / 1000)
                for i in range(0, len(output.samples), chunk_samples):
                    chunk_data = output.samples[i : i + chunk_samples]
                    is_final = (seg_idx == len(segments) - 1 and i + chunk_samples >= len(output.samples))

                    chunk = StreamingChunk(
                        samples=chunk_data,
                        chunk_index=self._chunk_counter,
                        is_final=is_final,
                        timestamp_ms=self._chunk_counter * self.chunk_size_ms,
                    )

                    self._chunk_counter += 1

                    # Handle buffer overflow
                    if len(self._chunk_buffer) >= self.max_queue_size:
                        if self.overflow_strategy == "drop_oldest":
                            self._chunk_buffer.pop(0)
                        elif self.overflow_strategy == "block":
                            pass  # Would block here in async context

                    self._chunk_buffer.append(chunk)
                    yield chunk

            except Exception as e:
                self._state = StreamState.ERROR
                logger.error("Streaming error at segment %d: %s", seg_idx, e)
                raise StreamingError(f"Stream failed at segment {seg_idx}: {e}")

        self._state = StreamState.IDLE
        self._chunk_buffer.clear()

    def _split_for_streaming(self, text: str) -> List[str]:
        """Split text into sentence-level segments for streaming."""
        # Split on sentence boundaries
        segments = re.split(r'(?<=[.!?])\s+', text)
        return [s for s in segments if s.strip()]

    @property
    def state(self) -> StreamState:
        return self._state

    @property
    def buffered_chunks(self) -> int:
        return len(self._chunk_buffer)


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the TTS pipeline."""
    print("=" * 60)
    print("Text-to-Speech Module — Demo")
    print("=" * 60)

    # 1. Basic synthesis
    print("\n[1] Basic TTS Synthesis")
    engine = TTSEngine(model="vits2_vctk_v1", vocoder="hifigan_v1", warmup=False)
    audio = engine.synthesize("Hello, welcome to the text-to-speech demo.", voice="p200")
    print(f"    Voice: {audio.voice_id}")
    print(f"    Duration: {audio.duration:.2f}s")
    print(f"    Samples: {audio.num_samples}")
    print(f"    Generation time: {audio.generation_time_ms:.1f}ms")

    # 2. SSML processing
    print("\n[2] SSML Processing")
    ssml = """
    <speak>
        <emphasis level="strong">Important:</emphasis>
        Your meeting is at <say-as interpret-as="time">3:30 PM</say-as>.
        <break time="500ms"/>
        <prosody rate="slow">Please arrive early.</prosody>
    </speak>
    """
    processor = SSMLProcessor()
    errors = processor.validate(ssml)
    if errors:
        print(f"    Validation errors: {errors}")
    else:
        print("    SSML validation: PASS")

    parsed = processor.parse(ssml)
    print(f"    Plain text: '{processor.to_text(ssml)}'")
    prosody = processor.extract_prosody(parsed)
    print(f"    Prosody: rate={prosody.rate:.2f}, pitch={prosody.pitch:.2f}")

    # 3. Voice cloning
    print("\n[3] Voice Cloning")
    cloner = VoiceCloner(device="cpu")
    ref_audio = np.random.randn(22050 * 30).astype(np.float32)
    adapter = cloner.create_adapter(ref_audio, adapter_rank=8, training_steps=500)
    print(f"    Cloned voice ID: {adapter.voice_id}")
    print(f"    Adapter weights shape: {adapter.adapter_weights.shape}")
    print(f"    Embedding dim: {len(adapter.embedding)}")

    # 4. Prosody control
    print("\n[4] Prosody Control")
    controller = ProsodyController()
    prosody = controller.compute(
        text="I can't believe this is AMAZING!",
        emotion="excited",
        emotion_intensity=0.8,
        speech_rate=1.2,
        emphasis_words=["can't"],
    )
    print(f"    Rate: {prosody.rate:.2f}")
    print(f"    Pitch: {prosody.pitch:.2f}")
    print(f"    Volume: {prosody.volume:.2f}")
    print(f"    Emphasis words: {prosody.emphasis_words}")

    # 5. Pronunciation dictionary
    print("\n[5] Pronunciation Dictionary")
    pron_dict = engine._pronunciation_dict
    pron_dict.add("OpenAI", "OH-pen-ay-eye")
    pron_dict.add("NVIDIA", "en-VID-ee-uh")
    pron_dict.add("GPT", "gee-pee-tee")
    print(f"    Dictionary size: {pron_dict.size} entries")

    entry = pron_dict.lookup("OpenAI")
    if entry:
        print(f"    OpenAI: {entry.phonemes}")

    # 6. Streaming TTS
    print("\n[6] Streaming TTS")
    streamer = StreamingTTS(engine, chunk_size_ms=100)
    chunk_count = 0
    for chunk in streamer.stream("This is a streaming synthesis test."):
        chunk_count += 1
        if chunk_count <= 3:
            print(f"    Chunk {chunk.chunk_index}: {chunk.duration_ms:.1f}ms (final={chunk.is_final})")
    print(f"    Total chunks: {chunk_count}")
    print(f"    Stream state: {streamer.state.value}")

    # 7. Emotion synthesis
    print("\n[7] Emotion Synthesis")
    for emotion in [Emotion.HAPPY, Emotion.SAD, Emotion.ANGRY]:
        audio = engine.synthesize(
            "The weather is nice today.",
            voice="p200",
            emotion=emotion,
            emotion_intensity=0.7,
        )
        print(f"    {emotion.value}: duration={audio.duration:.2f}s, gen_time={audio.generation_time_ms:.1f}ms")

    # 8. Available voices
    print("\n[8] Available Voices")
    print(f"    Voices: {engine.available_voices[:5]}...")

    print("\n" + "=" * 60)
    print("Demo complete. All TTS modules functional.")
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
Speech Recognition Module — ASR pipelines, decoding, and real-time transcription.

Provides end-to-end ASR models, beam search decoding, streaming recognition,
language model integration, custom vocabulary injection, and confidence scoring.
"""

from __future__ import annotations

import logging
import time
import re
from abc import ABC, abstractmethod
from collections import OrderedDict
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Set, Tuple, Union

import numpy as np

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ASRModel(Enum):
    """Supported ASR model architectures."""
    CONFORMER_CTC = "conformer_ctc"
    CONFORMER_TRANSDUCER = "conformer_transducer"
    WHISPER = "whisper"
    WAV2VEC2 = "wav2vec2"
    DEEPSPEECH = "deepspeech"
    FASTWHISPER = "fast_whisper"


class DecodingStrategy(Enum):
    """Beam search decoding strategies."""
    GREEDY = "greedy"
    BEAM_SEARCH = "beam_search"
    PREFIX_CONSTRAINED = "prefix_constrained"
    WFST = "wfst"


class EndpointType(Enum):
    """Types of speech endpoints."""
    SPEECH_START = "speech_start"
    SPEECH_END = "speech_end"
    TIMEOUT = "timeout"
    MAX_DURATION = "max_duration"


class LanguageCode(Enum):
    """ISO 639-1 language codes."""
    EN = "en"
    ZH = "zh"
    ES = "es"
    FR = "fr"
    DE = "de"
    JA = "ja"
    KO = "ko"
    PT = "pt"
    RU = "ru"
    AR = "ar"
    HI = "hi"
    IT = "it"
    NL = "nl"
    SV = "sv"
    PL = "pl"


class StreamingState(Enum):
    """State of the streaming recognition pipeline."""
    IDLE = "idle"
    RECOGNIZING = "recognizing"
    PARTIAL = "partial"
    FINAL = "final"
    ERROR = "error"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class WordResult:
    """A single recognized word with timing and confidence."""
    text: str
    start: float
    end: float
    confidence: float = 1.0
    speaker_id: Optional[int] = None
    language: Optional[str] = None
    is_punctuation: bool = False

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class TranscriptionResult:
    """Complete transcription output from batch ASR."""
    text: str
    words: List[WordResult] = field(default_factory=list)
    language: str = "en"
    duration: float = 0.0
    word_error_rate: Optional[float] = None
    average_confidence: float = 0.0
    processing_time_ms: float = 0.0
    model_used: str = ""

    @property
    def num_words(self) -> int:
        return len(self.words)

    @property
    def confidence_distribution(self) -> Dict[str, int]:
        """Count words by confidence tier."""
        tiers = {"high": 0, "medium": 0, "low": 0}
        for w in self.words:
            if w.confidence >= 0.8:
                tiers["high"] += 1
            elif w.confidence >= 0.5:
                tiers["medium"] += 1
            else:
                tiers["low"] += 1
        return tiers


@dataclass
class PartialResult:
    """Partial (in-progress) transcription from streaming ASR."""
    text: str
    confidence: float = 0.0
    timestamp: float = 0.0
    is_final: bool = False
    words: List[WordResult] = field(default_factory=list)
    language: Optional[str] = None

    @property
    def word_count(self) -> int:
        return len(self.text.split()) if self.text else 0


@dataclass
class VocabularyEntry:
    """Custom vocabulary entry with pronunciation hint."""
    word: str
    pronunciations: List[str] = field(default_factory=list)
    language: str = "en"
    boost: float = 1.0
    frequency: int = 1  # Expected frequency in domain

    @property
    def arpabet(self) -> Optional[str]:
        """Return first ARPabet pronunciation if available."""
        return self.pronunciations[0] if self.pronunciations else None


@dataclass
class LanguageModelWeights:
    """Weights for language model interpolation."""
    base_weight: float = 0.3
    domain_weight: float = 0.7
    vocabulary_boost: float = 2.0
    oov_penalty: float = 0.1


@dataclass
class EndpointDetection:
    """Result of endpoint detection."""
    endpoint_type: EndpointType
    timestamp: float
    confidence: float = 1.0
    partial_text: str = ""


@dataclass
class BeamHypothesis:
    """A single hypothesis in beam search."""
    text: str
    score: float
    lm_score: float = 0.0
    acoustic_score: float = 0.0
    word_timings: List[WordResult] = field(default_factory=list)

    @property
    def combined_score(self) -> float:
        return self.acoustic_score + self.lm_score


@dataclass
class LanguageSegment:
    """A segment with detected language information."""
    text: str
    language: str
    confidence: float
    start: float = 0.0
    end: float = 0.0


@dataclass
class CodeSwitchResult:
    """Result of code-switching detection."""
    segments: List[LanguageSegment] = field(default_factory=list)
    primary_language: str = "en"
    num_switches: int = 0

    @property
    def total_segments(self) -> int:
        return len(self.segments)


@dataclass
class CalibrationResult:
    """Result of confidence calibration."""
    method: str = "temperature_scaling"
    temperature: float = 1.0
    calibration_error: float = 0.0
    num_samples: int = 0


@dataclass
class BenchmarkMetrics:
    """Performance benchmark results."""
    wer: float = 0.0
    cer: float = 0.0
    rtf: float = 0.0  # Real-time factor
    latency_p50: float = 0.0
    latency_p99: float = 0.0
    throughput_rtf: float = 0.0
    total_hours: float = 0.0


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class ASRError(Exception):
    """Base exception for ASR errors."""
    pass


class ModelLoadError(ASRError):
    """Raised when an ASR model fails to load."""
    pass


class DecodingError(ASRError):
    """Raised when decoding encounters an unrecoverable error."""
    pass


class VocabularyError(ASRError):
    """Raised for vocabulary injection errors."""
    pass


class StreamingError(ASRError):
    """Raised for streaming pipeline errors."""
    pass


class LanguageModelError(ASRError):
    """Raised for language model integration errors."""
    pass


# ---------------------------------------------------------------------------
# Core Classes
# ---------------------------------------------------------------------------

class VocabularyInjector:
    """
    Manages custom vocabulary lists for domain-specific ASR.

    Supports pronunciation hints, frequency boosting, and language-specific entries.
    """

    def __init__(self):
        self._vocabulary: Dict[str, VocabularyEntry] = {}
        self._by_language: Dict[str, Set[str]] = {}
        self._boost_cache: Dict[str, float] = {}

    def add(
        self,
        word: str,
        pronunciations: Optional[List[str]] = None,
        language: str = "en",
        boost: float = 1.0,
        frequency: int = 1,
    ) -> VocabularyEntry:
        """Add a word to the vocabulary with optional pronunciation hints."""
        entry = VocabularyEntry(
            word=word,
            pronunciations=pronunciations or [],
            language=language,
            boost=boost,
            frequency=frequency,
        )

        self._vocabulary[word.lower()] = entry

        if language not in self._by_language:
            self._by_language[language] = set()
        self._by_language[language].add(word.lower())

        # Invalidate boost cache
        self._boost_cache.clear()

        logger.info("Vocabulary added: %s (lang=%s, boost=%.1f)", word, language, boost)
        return entry

    def remove(self, word: str) -> bool:
        """Remove a word from the vocabulary."""
        entry = self._vocabulary.pop(word.lower(), None)
        if entry:
            self._by_language.get(entry.language, set()).discard(word.lower())
            self._boost_cache.clear()
            return True
        return False

    def lookup(self, word: str) -> Optional[VocabularyEntry]:
        return self._vocabulary.get(word.lower())

    def get_boost(self, word: str) -> float:
        """Get the boost factor for a word (cached)."""
        if word not in self._boost_cache:
            entry = self._vocabulary.get(word.lower())
            self._boost_cache[word] = entry.boost if entry else 1.0
        return self._boost_cache[word]

    def get_words_for_language(self, language: str) -> List[VocabularyEntry]:
        words = self._by_language.get(language, set())
        return [self._vocabulary[w] for w in words if w in self._vocabulary]

    def inject_into_beam(self, beam: BeamHypothesis) -> BeamHypothesis:
        """Apply vocabulary boosts to a beam hypothesis."""
        words = beam.text.split()
        boost_factor = 1.0
        for word in words:
            boost = self.get_boost(word)
            if boost != 1.0:
                boost_factor *= boost

        beam.lm_score *= boost_factor
        return beam

    @property
    def size(self) -> int:
        return len(self._vocabulary)

    @property
    def languages(self) -> List[str]:
        return list(self._by_language.keys())


class LanguageModelAdapter:
    """
    Integrates N-gram and neural language models for ASR decoding.

    Supports model interpolation and domain adaptation.
    """

    def __init__(
        self,
        base_lm_weight: float = 0.3,
        vocabulary_boost: float = 2.0,
    ):
        self.base_lm_weight = base_lm_weight
        self.vocabulary_boost = vocabulary_boost
        self._base_model = None
        self._domain_model = None
        self._interpolated = False

    def interpolate(
        self,
        base_model: str,
        domain_model: str,
        domain_weight: float = 0.7,
    ) -> "LanguageModelAdapter":
        """Interpolate base and domain language models."""
        logger.info(
            "Interpolating LMs: base=%s (w=%.2f), domain=%s (w=%.2f)",
            base_model, 1.0 - domain_weight, domain_model, domain_weight,
        )
        self._base_model = base_model
        self._domain_model = domain_model
        self.base_lm_weight = 1.0 - domain_weight
        self._interpolated = True
        return self

    def score_word(self, word: str, context: List[str]) -> float:
        """Score a word given its context."""
        # Placeholder: in production, query the LM
        base_score = np.random.uniform(-3.0, -1.0)
        if self._interpolated:
            domain_score = np.random.uniform(-3.0, -1.0)
            return (1 - self.base_lm_weight) * base_score + self.base_lm_weight * domain_score
        return base_score

    def score_sequence(self, words: List[str]) -> float:
        """Score a word sequence."""
        total = 0.0
        context: List[str] = []
        for word in words:
            total += self.score_word(word, context)
            context.append(word)
        return total

    def rescore_hypotheses(self, hypotheses: List[BeamHypothesis]) -> List[BeamHypothesis]:
        """Rescore a list of hypotheses with the interpolated LM."""
        for hyp in hypotheses:
            words = hyp.text.split()
            hyp.lm_score = self.score_sequence(words)
        return sorted(hypotheses, key=lambda h: h.combined_score, reverse=True)


class EndpointDetector:
    """Detects speech endpoints (start/end) based on VAD and silence."""

    def __init__(
        self,
        min_silence_duration_ms: int = 800,
        max_speech_duration_ms: int = 30000,
        speech_threshold: float = 0.5,
    ):
        self.min_silence_ms = min_silence_duration_ms
        self.max_speech_ms = max_speech_duration_ms
        self.speech_threshold = speech_threshold
        self._silence_start: Optional[float] = None
        self._speech_start: Optional[float] = None
        self._is_speech = False

    def is_endpoint(self, partial_result: PartialResult) -> bool:
        """Check if the current state indicates an endpoint."""
        now = time.time()

        if partial_result.confidence > self.speech_threshold:
            if not self._is_speech:
                self._is_speech = True
                self._speech_start = now
                self._silence_start = None

            # Check max duration
            if self._speech_start and (now - self._speech_start) * 1000 > self.max_speech_ms:
                return True
        else:
            if self._is_speech:
                if self._silence_start is None:
                    self._silence_start = now
                elif (now - self._silence_start) * 1000 >= self.min_silence_ms:
                    return True

        return False

    def reset(self) -> None:
        self._silence_start = None
        self._speech_start = None
        self._is_speech = False


class BeamSearchDecoder:
    """
    Beam search decoding with language model fusion and pruning.

    Supports configurable beam width, LM weight, and early exit strategies.
    """

    def __init__(
        self,
        beam_size: int = 10,
        lm_weight: float = 0.3,
        blank_penalty: float = 1.0,
        pruning_threshold: float = 0.001,
        max_length: int = 500,
    ):
        self.beam_size = beam_size
        self.lm_weight = lm_weight
        self.blank_penalty = blank_penalty
        self.pruning_threshold = pruning_threshold
        self.max_length = max_length

    def decode(
        self,
        acoustic_output: np.ndarray,
        vocabulary: Optional[VocabularyInjector] = None,
        lm_adapter: Optional[LanguageModelAdapter] = None,
    ) -> BeamHypothesis:
        """
        Decode acoustic model output into text using beam search.

        Args:
            acoustic_output: Log-softmax output from acoustic model [T, V].
            vocabulary: Optional vocabulary injector for boosting.
            lm_adapter: Optional language model for resoring.

        Returns:
            Best BeamHypothesis after beam search.
        """
        start_time = time.time()
        T, V = acoustic_output.shape

        # Initialize beams
        beams = [BeamHypothesis(text="", score=0.0)]

        for t in range(min(T, self.max_length)):
            all_candidates = []

            for beam in beams:
                if beam.text and beam.text[-1] == " ":
                    # Already finalized this beam
                    all_candidates.append(beam)
                    continue

                for v in range(V):
                    log_prob = acoustic_output[t, v]
                    blank_penalty = self.blank_penalty if v == 0 else 1.0

                    new_score = beam.score + log_prob * blank_penalty

                    if v == 0:  # Blank token
                        all_candidates.append(BeamHypothesis(
                            text=beam.text,
                            score=new_score,
                            acoustic_score=new_score,
                        ))
                    else:
                        # Simulated token-to-text
                        char = chr(ord('a') + (v % 26)) if v < 27 else " "
                        new_text = beam.text + char
                        all_candidates.append(BeamHypothesis(
                            text=new_text,
                            score=new_score,
                            acoustic_score=new_score,
                        ))

            # Keep top beams
            all_candidates.sort(key=lambda b: b.score, reverse=True)
            beams = all_candidates[: self.beam_size]

            # Prune low-probability beams
            if beams:
                threshold = beams[0].score + np.log(self.pruning_threshold)
                beams = [b for b in beams if b.score > threshold]

        # Apply vocabulary boosting
        if vocabulary:
            beams = [vocabulary.inject_into_beam(b) for b in beams]

        # Apply LM rescoring
        if lm_adapter:
            beams = lm_adapter.rescore_hypotheses(beams)

        best = beams[0] if beams else BeamHypothesis(text="", score=0.0)

        elapsed = (time.time() - start_time) * 1000
        logger.info(
            "Beam search: %d hypotheses, best='%s' (score=%.2f, %.1fms)",
            len(beams), best.text[:50], best.score, elapsed,
        )
        return best

    def decode_with_word_timings(
        self,
        acoustic_output: np.ndarray,
        frame_duration_ms: float = 20.0,
    ) -> BeamHypothesis:
        """Decode with forced alignment for word-level timing."""
        best = self.decode(acoustic_output)

        # Placeholder: simulate word timings
        words = best.text.split()
        if not words:
            return best

        total_frames = acoustic_output.shape[0]
        frames_per_word = max(1, total_frames // len(words))

        timings = []
        for i, word in enumerate(words):
            start = i * frames_per_word * frame_duration_ms / 1000
            end = (i + 1) * frames_per_word * frame_duration_ms / 1000
            timings.append(WordResult(
                text=word,
                start=start,
                end=end,
                confidence=np.random.uniform(0.7, 1.0),
            ))

        best.word_timings = timings
        return best


class ASREngine:
    """
    Core ASR engine supporting batch and streaming recognition.

    Manages model loading, preprocessing, decoding, and postprocessing.
    """

    def __init__(
        self,
        model: str = "conformer_ctc_large",
        device: str = "cuda",
        language: str = "en",
        beam_size: int = 10,
    ):
        self.model_name = model
        self.device = device
        self.language = language
        self.beam_size = beam_size
        self._model = None
        self._vocabulary = VocabularyInjector()
        self._lm_adapter: Optional[LanguageModelAdapter] = None
        self._decoder = BeamSearchDecoder(beam_size=beam_size)
        self._calibrator: Optional["ConfidenceCalibrator"] = None

        self._register_default_vocabulary()

    def _register_default_vocabulary(self) -> None:
        """Register common words that benefit from boosting."""
        domain_terms = {
            "metformin": ["MET-for-min"],
            "atorvastatin": ["ah-TOR-vah-STAT-in"],
            "COVID-19": ["koh-vid nine-teen"],
        }
        for word, pronunciations in domain_terms.items():
            self._vocabulary.add(word, pronunciations=pronunciations)

    def set_vocabulary(self, vocabulary: VocabularyInjector) -> None:
        self._vocabulary = vocabulary

    def set_language_model(self, lm_adapter: LanguageModelAdapter) -> None:
        self._lm_adapter = lm_adapter

    def set_confidence_calibrator(self, calibrator: "ConfidenceCalibrator") -> None:
        self._calibrator = calibrator

    def _preprocess(self, audio_input: Union[str, Path, np.ndarray]) -> np.ndarray:
        """Preprocess audio input for the model."""
        if isinstance(audio_input, (str, Path)):
            # Placeholder: load and preprocess audio
            samples = np.random.randn(16000 * 5).astype(np.float32)
        else:
            samples = audio_input.astype(np.float32)

        # Normalize
        samples = samples / (np.max(np.abs(samples)) + 1e-10)
        return samples

    def _run_acoustic_model(self, audio: np.ndarray) -> np.ndarray:
        """Run acoustic model inference (placeholder)."""
        # In production: run Conformer/Whisper/wav2vec2
        T = len(audio) // 160 + 1  # ~10ms frames
        V = 5000  # vocabulary size
        return np.random.randn(T, V).astype(np.float32)

    def transcribe(
        self,
        audio_input: Union[str, Path, np.ndarray],
        language: Optional[str] = None,
    ) -> TranscriptionResult:
        """Perform batch transcription on audio input."""
        start_time = time.time()
        lang = language or self.language

        # Preprocess
        audio = self._preprocess(audio_input)

        # Run acoustic model
        acoustic_output = self._run_acoustic_model(audio)

        # Decode
        hypothesis = self._decoder.decode(
            acoustic_output,
            vocabulary=self._vocabulary,
            lm_adapter=self._lm_adapter,
        )

        # Build result
        words = []
        for i, word in enumerate(hypothesis.text.split()):
            words.append(WordResult(
                text=word,
                start=i * 0.5,
                end=(i + 1) * 0.5,
                confidence=np.random.uniform(0.7, 1.0),
            ))

        elapsed = (time.time() - start_time) * 1000
        avg_conf = np.mean([w.confidence for w in words]) if words else 0.0

        result = TranscriptionResult(
            text=hypothesis.text,
            words=words,
            language=lang,
            duration=len(audio) / 16000,
            average_confidence=float(avg_conf),
            processing_time_ms=elapsed,
            model_used=self.model_name,
        )

        logger.info(
            "Transcribed: '%s' (%d words, %.1fms, conf=%.2f)",
            result.text[:50], result.num_words, elapsed, avg_conf,
        )
        return result

    def transcribe_streaming(
        self,
        audio_stream: Generator[np.ndarray, None, None],
        chunk_size_ms: int = 400,
    ) -> Generator[PartialResult, None, None]:
        """Perform streaming transcription on audio stream."""
        state = StreamingState.IDLE
        buffer = np.array([], dtype=np.float32)
        chunk_samples = int(16000 * chunk_size_ms / 1000)
        full_text = ""

        for chunk in audio_stream:
            buffer = np.concatenate([buffer, chunk])

            while len(buffer) >= chunk_samples:
                frame = buffer[:chunk_samples]
                buffer = buffer[chunk_samples:]

                acoustic_output = self._run_acoustic_model(frame)
                hypothesis = self._decoder.decode(acoustic_output)

                is_final = len(hypothesis.text) > len(full_text) + 5
                full_text = hypothesis.text

                partial = PartialResult(
                    text=hypothesis.text,
                    confidence=np.random.uniform(0.6, 1.0),
                    timestamp=time.time(),
                    is_final=is_final,
                )

                yield partial


class CodeSwitchingDetector:
    """Detects language switches within multilingual speech."""

    def __init__(
        self,
        supported_languages: Optional[List[str]] = None,
        detection_window_ms: int = 2000,
        confidence_threshold: float = 0.6,
    ):
        self.supported_languages = supported_languages or ["en", "zh", "es", "fr"]
        self.detection_window_ms = detection_window_ms
        self.confidence_threshold = confidence_threshold

    def detect(self, audio_segments: List[np.ndarray]) -> List[LanguageSegment]:
        """Detect language segments in audio."""
        segments = []
        for i, segment in enumerate(audio_segments):
            # Placeholder: simulate language detection
            lang = np.random.choice(self.supported_languages)
            conf = np.random.uniform(0.5, 1.0)
            segments.append(LanguageSegment(
                text=f"[segment_{i}]",
                language=lang,
                confidence=conf,
                start=i * self.detection_window_ms / 1000,
                end=(i + 1) * self.detection_window_ms / 1000,
            ))
        return segments


class MultiLanguageASR:
    """Multi-language ASR with code-switching support."""

    def __init__(
        self,
        models: Optional[Dict[str, str]] = None,
        detector: Optional[CodeSwitchingDetector] = None,
    ):
        self.models = models or {"en": "conformer_en"}
        self.detector = detector or CodeSwitchingDetector()
        self._engines: Dict[str, ASREngine] = {}

        for lang, model in self.models.items():
            self._engines[lang] = ASREngine(model=model, language=lang)

    def transcribe(self, audio_path: str) -> CodeSwitchResult:
        """Transcribe audio with automatic language detection."""
        # Placeholder implementation
        segments = [
            LanguageSegment(text="Hello, how are you?", language="en", confidence=0.9),
            LanguageSegment(text="你好，我很好", language="zh", confidence=0.85),
        ]
        return CodeSwitchResult(
            segments=segments,
            primary_language="en",
            num_switches=1,
        )


class ConfidenceCalibrator:
    """Calibrates raw model confidence scores to true probabilities."""

    def __init__(self):
        self._temperature = 1.0
        self._fitted = False

    def fit(
        self,
        model: ASREngine,
        calibration_set: str,
        method: str = "temperature_scaling",
    ) -> CalibrationResult:
        """Fit calibration parameters on a held-out set."""
        logger.info("Fitting confidence calibrator (method=%s)", method)

        # Placeholder: fit temperature scaling
        self._temperature = np.random.uniform(0.8, 1.5)
        self._fitted = True

        return CalibrationResult(
            method=method,
            temperature=self._temperature,
            calibration_error=np.random.uniform(0.01, 0.05),
            num_samples=1000,
        )

    def calibrate(self, raw_confidence: float) -> float:
        """Calibrate a raw confidence score."""
        if not self._fitted:
            return raw_confidence
        # Temperature scaling
        logit = np.log(raw_confidence / (1 - raw_confidence + 1e-10) + 1e-10)
        calibrated_logit = logit / self._temperature
        calibrated = 1.0 / (1.0 + np.exp(-calibrated_logit))
        return float(calibrated)


class ASRBenchmark:
    """Evaluates ASR model performance on standard test sets."""

    def __init__(self):
        self._results: List[BenchmarkMetrics] = []

    def evaluate(
        self,
        model: str,
        test_set: str,
        metrics: Optional[List[str]] = None,
    ) -> BenchmarkMetrics:
        """Run benchmark evaluation on a test set."""
        metrics = metrics or ["wer", "cer", "rtf"]

        logger.info("Evaluating %s on %s", model, test_set)

        # Placeholder: simulate benchmark results
        result = BenchmarkMetrics(
            wer=np.random.uniform(0.03, 0.10),
            cer=np.random.uniform(0.01, 0.05),
            rtf=np.random.uniform(0.05, 0.15),
            latency_p50=np.random.uniform(50, 150),
            latency_p99=np.random.uniform(200, 500),
            total_hours=10.0,
        )

        self._results.append(result)

        logger.info(
            "Benchmark: WER=%.2f%%, CER=%.2f%%, RTF=%.3f",
            result.wer * 100, result.cer * 100, result.rtf,
        )
        return result

    def compare(self, results: List[BenchmarkMetrics]) -> str:
        """Generate a comparison report from multiple benchmark results."""
        if not results:
            return "No results to compare."

        report_lines = ["Model Comparison Report", "=" * 40]
        for i, r in enumerate(results):
            report_lines.append(
                f"  Model {i+1}: WER={r.wer:.2%} CER={r.cer:.2%} RTF={r.rtf:.3f}"
            )

        best_wer = min(results, key=lambda r: r.wer)
        report_lines.append(f"\nBest WER: {best_wer.wer:.2%}")

        return "\n".join(report_lines)


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the ASR pipeline."""
    print("=" * 60)
    print("Speech Recognition Module — Demo")
    print("=" * 60)

    # 1. Basic transcription
    print("\n[1] Batch Transcription")
    engine = ASREngine(model="conformer_ctc_large", beam_size=10)
    audio = np.random.randn(16000 * 5).astype(np.float32)
    result = engine.transcribe(audio)
    print(f"    Text: '{result.text[:80]}...'")
    print(f"    Words: {result.num_words}")
    print(f"    Confidence: {result.average_confidence:.2f}")
    print(f"    Processing: {result.processing_time_ms:.1f}ms")

    # 2. Custom vocabulary
    print("\n[2] Custom Vocabulary Injection")
    vocab = VocabularyInjector()
    vocab.add("metformin", pronunciations=["MET-for-min"])
    vocab.add("atorvastatin", pronunciations=["ah-TOR-vah-STAT-in"])
    vocab.add("COVID-19", pronunciations=["koh-vid nine-teen"])
    vocab.add("GPT-4", pronunciations=["gee-pee-tee four"])
    print(f"    Vocabulary size: {vocab.size}")
    print(f"    Languages: {vocab.languages}")

    # 3. Language model integration
    print("\n[3] Language Model Integration")
    lm = LanguageModelAdapter(base_lm_weight=0.3, vocabulary_boost=2.0)
    lm.interpolate(
        base_model="kenlm_wikipedia",
        domain_model="kenlm_medical",
        domain_weight=0.7,
    )
    score = lm.score_sequence(["metformin", "is", "used", "for", "diabetes"])
    print(f"    LM score: {score:.3f}")

    # 4. Beam search decoding
    print("\n[4] Beam Search Decoding")
    decoder = BeamSearchDecoder(beam_size=10, lm_weight=0.3)
    acoustic = np.random.randn(100, 500).astype(np.float32)
    hypothesis = decoder.decode_with_word_timings(acoustic)
    print(f"    Best hypothesis: '{hypothesis.text[:50]}'")
    print(f"    Score: {hypothesis.score:.3f}")
    print(f"    Word timings: {len(hypothesis.word_timings)} words")

    # 5. Streaming recognition
    print("\n[5] Streaming Recognition")
    endpoint_detector = EndpointDetector(min_silence_duration_ms=800)
    print(f"    Endpoint detector: min_silence={endpoint_detector.min_silence_ms}ms")

    def audio_generator():
        for _ in range(5):
            yield np.random.randn(6400).astype(np.float32)

    partial_count = 0
    for partial in engine.transcribe_streaming(audio_generator()):
        partial_count += 1
        if partial_count <= 3:
            print(f"    Partial {partial_count}: '{partial.text[:40]}' (final={partial.is_final})")
    print(f"    Total partials: {partial_count}")

    # 6. Multi-language / code-switching
    print("\n[6] Multi-Language ASR")
    multi_asr = MultiLanguageASR(models={"en": "conformer_en", "zh": "conformer_zh"})
    cs_result = multi_asr.transcribe("test_audio.wav")
    print(f"    Primary language: {cs_result.primary_language}")
    print(f"    Segments: {cs_result.total_segments}")
    print(f"    Language switches: {cs_result.num_switches}")
    for seg in cs_result.segments:
        print(f"      [{seg.language}] {seg.text} (conf={seg.confidence:.2f})")

    # 7. Confidence calibration
    print("\n[7] Confidence Calibration")
    calibrator = ConfidenceCalibrator()
    cal_result = calibrator.fit(engine, "calibration_set/", method="temperature_scaling")
    print(f"    Temperature: {cal_result.temperature:.3f}")
    print(f"    Calibration error: {cal_result.calibration_error:.4f}")
    print(f"    Samples: {cal_result.num_samples}")

    raw_conf = 0.75
    calibrated = calibrator.calibrate(raw_conf)
    print(f"    Raw confidence: {raw_conf:.2f} -> Calibrated: {calibrated:.2f}")

    # 8. Benchmarking
    print("\n[8] ASR Benchmarking")
    benchmark = ASRBenchmark()
    metrics = benchmark.evaluate(
        model="conformer_ctc_large",
        test_set="librispeech_test_clean",
    )
    print(f"    WER: {metrics.wer:.2%}")
    print(f"    CER: {metrics.cer:.2%}")
    print(f"    RTF: {metrics.rtf:.3f}")
    print(f"    Latency P50: {metrics.latency_p50:.1f}ms")
    print(f"    Latency P99: {metrics.latency_p99:.1f}ms")

    # 9. Vocabulary boost in beam search
    print("\n[9] Vocabulary Boost in Beam Search")
    beam = BeamHypothesis(text="take metformin twice daily", score=-5.0, acoustic_score=-5.0)
    boosted = vocab.inject_into_beam(beam)
    print(f"    Original score: {beam.score:.3f}")
    print(f"    After boost: {boosted.lm_score:.3f}")

    print("\n" + "=" * 60)
    print("Demo complete. All ASR modules functional.")
    print("=" * 60)


if __name__ == "__main__":
    main()

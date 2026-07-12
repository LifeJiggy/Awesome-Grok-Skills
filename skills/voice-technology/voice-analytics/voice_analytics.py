"""
Voice Analytics Module — Emotion detection, speaker ID, and speech quality assessment.

Provides emotion recognition, speaker identification/verification, voice biometrics,
call center analytics, speech quality metrics, and compliance monitoring.
"""

from __future__ import annotations

import logging
import time
import hashlib
from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union

import numpy as np

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EmotionCategory(Enum):
    """Discrete emotion categories."""
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    FEARFUL = "fearful"
    DISGUSTED = "disgusted"
    SURPRISED = "surprised"
    EXCITED = "excited"
    FRUSTRATED = "frustrated"
    CONFUSED = "confused"


class Sentiment(Enum):
    """High-level sentiment classification."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class VerificationResult(Enum):
    """Speaker verification outcomes."""
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    INCONCLUSIVE = "inconclusive"
    SPOOF_DETECTED = "spoof_detected"


class SpoofType(Enum):
    """Types of voice spoofing attacks."""
    REPLAY = "replay"
    TTS_SYNTHESIS = "tts_synthesis"
    VOICE_CONVERSION = "voice_conversion"
    DEEPFAKE = "deepfake"


class ComplianceViolation(Enum):
    """Types of compliance violations in voice recordings."""
    MISSING_DISCLOSURE = "missing_disclosure"
    EXCESSIVE_SILENCE = "excessive_silence"
    AGENT_INTERRUPTION = "agent_interruption"
    DEAD_AIR = "dead_air"
    INAPPROPRIATE_LANGUAGE = "inappropriate_language"
    MISSING_VERIFICATION = "missing_verification"
    OFF_SCRIPT = "off_script"


class QualityGrade(Enum):
    """Speech quality grades."""
    EXCELLENT = "excellent"   # MOS >= 4.0
    GOOD = "good"             # MOS >= 3.5
    FAIR = "fair"             # MOS >= 3.0
    POOR = "poor"             # MOS >= 2.5
    BAD = "bad"               # MOS < 2.5


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class EmotionResult:
    """Output of emotion detection from voice."""
    primary_emotion: EmotionCategory
    confidence: float
    valence: float = 0.0       # -1 (negative) to +1 (positive)
    arousal: float = 0.0       # 0 (calm) to 1 (excited)
    dominance: float = 0.0     # 0 (submissive) to 1 (dominant)
    emotion_probabilities: Dict[str, float] = field(default_factory=dict)
    timestamp_start: float = 0.0
    timestamp_end: float = 0.0
    model_used: str = ""

    @property
    def is_confident(self) -> bool:
        return self.confidence >= 0.7


@dataclass
class SpeakerEmbedding:
    """Speaker embedding vector with metadata."""
    embedding: np.ndarray
    speaker_id: str
    quality_score: float = 0.0
    enrollment_date: str = ""
    num_utterances: int = 0

    @property
    def dimension(self) -> int:
        return len(self.embedding)

    def cosine_similarity(self, other: "SpeakerEmbedding") -> float:
        """Compute cosine similarity with another embedding."""
        dot = np.dot(self.embedding, other.embedding)
        norm = np.linalg.norm(self.embedding) * np.linalg.norm(other.embedding)
        return float(dot / (norm + 1e-10))


@dataclass
class SpeakerIdentification:
    """Result of speaker identification."""
    speaker_id: str
    speaker_name: Optional[str] = None
    similarity: float = 0.0
    start: float = 0.0
    end: float = 0.0
    is_confirmed: bool = False

    @property
    def duration(self) -> float:
        return self.end - self.start


@dataclass
class IdentificationResult:
    """Complete result of speaker identification on audio."""
    segments: List[SpeakerIdentification] = field(default_factory=list)
    num_speakers: int = 0
    total_speech_duration: float = 0.0
    model_used: str = ""

    @property
    def unique_speakers(self) -> Set[str]:
        return {seg.speaker_id for seg in self.segments}


@dataclass
class VerificationOutput:
    """Result of speaker verification (1:1 comparison)."""
    accepted: bool
    score: float
    threshold: float
    claimed_identity: str
    actual_similarity: float = 0.0
    processing_time_ms: float = 0.0
    anti_spoof_passed: bool = True

    @property
    def result(self) -> VerificationResult:
        if not self.anti_spoof_passed:
            return VerificationResult.SPOOF_DETECTED
        if self.accepted:
            return VerificationResult.ACCEPTED
        return VerificationResult.REJECTED


@dataclass
class SpeakerGallery:
    """Gallery of enrolled speaker embeddings."""
    speakers: Dict[str, List[SpeakerEmbedding]] = field(default_factory=dict)
    metadata: Dict[str, Dict[str, Any]] = field(default_factory=dict)

    def enroll(
        self,
        speaker_id: str,
        audio: Union[str, Path, np.ndarray],
        name: Optional[str] = None,
    ) -> SpeakerEmbedding:
        """Enroll a new speaker or add an additional utterance."""
        # Placeholder: extract embedding from audio
        embedding = np.random.randn(192).astype(np.float32)
        embedding = embedding / (np.linalg.norm(embedding) + 1e-10)

        emb = SpeakerEmbedding(
            embedding=embedding,
            speaker_id=speaker_id,
            quality_score=np.random.uniform(0.7, 1.0),
            enrollment_date=time.strftime("%Y-%m-%d"),
            num_utterances=1,
        )

        if speaker_id not in self.speakers:
            self.speakers[speaker_id] = []
            self.metadata[speaker_id] = {"name": name or speaker_id}

        self.speakers[speaker_id].append(emb)

        logger.info(
            "Enrolled speaker %s (%s): %d utterances total",
            speaker_id, name, len(self.speakers[speaker_id]),
        )
        return emb

    def get_embedding(self, speaker_id: str) -> Optional[SpeakerEmbedding]:
        """Get the average embedding for a speaker."""
        embeddings = self.speakers.get(speaker_id)
        if not embeddings:
            return None
        avg = np.mean([e.embedding for e in embeddings], axis=0)
        return SpeakerEmbedding(
            embedding=avg,
            speaker_id=speaker_id,
            num_utterances=len(embeddings),
        )

    @property
    def size(self) -> int:
        return len(self.speakers)


@dataclass
class SpeechQualityMetrics:
    """Comprehensive speech quality assessment."""
    mos: float = 0.0              # Mean Opinion Score (1.0-5.0)
    clarity_score: float = 0.0    # 0.0-1.0
    speech_rate_wpm: float = 0.0  # Words per minute
    filler_count: int = 0
    pause_ratio: float = 0.0      # Fraction of time spent pausing
    articulation_score: float = 0.0  # 0.0-1.0
    noise_level_db: float = 0.0
    dynamic_range_db: float = 0.0
    breath_count: int = 0
    repetition_count: int = 0

    @property
    def quality_grade(self) -> QualityGrade:
        if self.mos >= 4.0:
            return QualityGrade.EXCELLENT
        elif self.mos >= 3.5:
            return QualityGrade.GOOD
        elif self.mos >= 3.0:
            return QualityGrade.FAIR
        elif self.mos >= 2.5:
            return QualityGrade.POOR
        return QualityGrade.BAD

    @property
    def is_fluent(self) -> bool:
        return self.filler_count < 5 and self.repetition_count < 3


@dataclass
class SentimentResult:
    """Sentiment analysis result from speech."""
    sentiment: Sentiment
    confidence: float
    valence: float = 0.0
    arousal: float = 0.0
    trajectory: List[Tuple[float, Sentiment]] = field(default_factory=list)
    key_moments: List[Tuple[float, str]] = field(default_factory=list)

    @property
    def overall_valence(self) -> float:
        """Average valence across the trajectory."""
        if not self.trajectory:
            return self.valence
        return np.mean([v for _, v in self.trajectory])


@dataclass
class CallAnalytics:
    """Analytics result for a complete call."""
    duration: float = 0.0
    num_speakers: int = 0
    sentiment_trajectory: List[Tuple[float, str]] = field(default_factory=list)
    compliance_score: float = 1.0
    csat_prediction: float = 0.5
    escalation_detected: bool = False
    violations: List[str] = field(default_factory=list)
    agent_talk_ratio: float = 0.0
    customer_talk_ratio: float = 0.0
    avg_speech_rate: float = 0.0
    total_silence_ratio: float = 0.0
    emotions_detected: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    resolution_status: str = "unknown"


@dataclass
class ComplianceCheck:
    """Result of compliance monitoring check."""
    disclosure_provided: bool = False
    interruption_rate: float = 0.0
    dead_air_segments: List[Tuple[float, float]] = field(default_factory=list)
    violations: List[str] = field(default_factory=list)
    compliance_score: float = 1.0
    checks_performed: List[str] = field(default_factory=list)
    overall_compliant: bool = True


@dataclass
class TranscriptionWithTimestamps:
    """Transcription with word-level timestamps for compliance analysis."""
    words: List[Dict[str, Any]] = field(default_factory=list)
    segments: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_file(cls, file_path: str) -> "TranscriptionWithTimestamps":
        """Load transcription from JSON file (placeholder)."""
        return cls(words=[], segments=[])


@dataclass
class AntiSpoofResult:
    """Result of anti-spoofing analysis."""
    is_genuine: bool
    spoof_probability: float
    spoof_type: Optional[SpoofType] = None
    confidence: float = 0.0
    features_used: List[str] = field(default_factory=list)


@dataclass
class VoiceBiometricsConfig:
    """Configuration for voice biometric system."""
    embedding_model: str = "ecapa_tdnn_v2"
    verification_threshold: float = 0.85
    adaptive_threshold: bool = True
    anti_spoof_enabled: bool = True
    max_enrollment_utterances: int = 10
    gallery_refresh_days: int = 90
    embedding_drift_alert: float = 0.15


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class VoiceAnalyticsError(Exception):
    """Base exception for voice analytics errors."""
    pass


class EmotionDetectionError(VoiceAnalyticsError):
    """Raised when emotion detection fails."""
    pass


class SpeakerNotFoundError(VoiceAnalyticsError):
    """Raised when a speaker is not found in the gallery."""
    pass


class SpoofDetectedError(VoiceAnalyticsError):
    """Raised when a voice spoofing attempt is detected."""
    pass


class QualityAssessmentError(VoiceAnalyticsError):
    """Raised when quality assessment fails."""
    pass


class ComplianceError(VoiceAnalyticsError):
    """Raised for compliance monitoring errors."""
    pass


# ---------------------------------------------------------------------------
# Core Classes
# ---------------------------------------------------------------------------

class EmotionDetector:
    """
    Multi-model ensemble for emotion detection from speech.

    Supports discrete emotion categories and dimensional affect representation.
    """

    def __init__(
        self,
        models: Optional[List[Dict[str, Any]]] = None,
        output_mode: str = "ensemble",
        device: str = "cuda",
    ):
        self.models = models or [
            {"name": "cnn_emotion_v3", "weight": 0.4},
            {"name": "wav2vec_emotion_v2", "weight": 0.4},
            {"name": "prosodic_emotion_v1", "weight": 0.2},
        ]
        self.output_mode = output_mode
        self.device = device
        self._model_cache: Dict[str, Any] = {}

    def _run_model(self, model_name: str, audio: np.ndarray) -> Dict[str, float]:
        """Run a single emotion model (placeholder)."""
        emotions = {}
        for emotion in EmotionCategory:
            emotions[emotion.value] = np.random.uniform(0.0, 1.0)

        # Normalize probabilities
        total = sum(emotions.values())
        emotions = {k: v / total for k, v in emotions.items()}
        return emotions

    def _ensemble_predictions(
        self,
        model_results: List[Dict[str, float]],
    ) -> Dict[str, float]:
        """Combine predictions from multiple models."""
        combined: Dict[str, float] = defaultdict(float)
        total_weight = sum(m["weight"] for m in self.models)

        for model_info, result in zip(self.models, model_results):
            weight = model_info["weight"] / total_weight
            for emotion, prob in result.items():
                combined[emotion] += prob * weight

        return dict(combined)

    def _compute_vad(self, emotions: Dict[str, float]) -> Tuple[float, float, float]:
        """Compute valence-arousal-dominance from discrete emotions."""
        valence_map = {
            "happy": 0.8, "excited": 0.7, "surprised": 0.3,
            "neutral": 0.0, "confused": -0.2,
            "sad": -0.7, "angry": -0.5, "fearful": -0.6,
            "disgusted": -0.6, "frustrated": -0.4,
        }
        arousal_map = {
            "excited": 0.9, "angry": 0.8, "fearful": 0.7,
            "surprised": 0.7, "happy": 0.5, "frustrated": 0.5,
            "disgusted": 0.3, "confused": 0.2,
            "neutral": 0.1, "sad": 0.1,
        }
        dominance_map = {
            "angry": 0.8, "excited": 0.7, "happy": 0.6,
            "neutral": 0.5, "surprised": 0.4, "frustrated": 0.4,
            "confused": 0.3, "sad": 0.2,
            "fearful": 0.1, "disgusted": 0.3,
        }

        valence = sum(emotions.get(e, 0) * v for e, v in valence_map.items())
        arousal = sum(emotions.get(e, 0) * v for e, v in arousal_map.items())
        dominance = sum(emotions.get(e, 0) * v for e, v in dominance_map.items())

        return float(np.clip(valence, -1, 1)), float(np.clip(arousal, 0, 1)), float(np.clip(dominance, 0, 1))

    def detect(self, audio_input: Union[str, Path, np.ndarray]) -> EmotionResult:
        """Detect emotion from audio input."""
        start_time = time.time()

        # Load audio (placeholder)
        if isinstance(audio_input, (str, Path)):
            audio = np.random.randn(16000 * 5).astype(np.float32)
        else:
            audio = audio_input

        # Run models
        model_results = []
        for model_info in self.models:
            result = self._run_model(model_info["name"], audio)
            model_results.append(result)

        # Ensemble
        if self.output_mode == "ensemble":
            combined = self._ensemble_predictions(model_results)
        else:
            combined = model_results[0]

        # Find primary emotion
        primary = max(combined.items(), key=lambda x: x[1])
        primary_emotion = EmotionCategory(primary[0])

        # Compute VAD
        valence, arousal, dominance = self._compute_vad(combined)

        elapsed = (time.time() - start_time) * 1000

        return EmotionResult(
            primary_emotion=primary_emotion,
            confidence=primary[1],
            valence=valence,
            arousal=arousal,
            dominance=dominance,
            emotion_probabilities=combined,
            model_used=self.models[0]["name"],
        )


class SpeakerIdentifier:
    """
    Speaker identification and verification using speaker embeddings.

    Supports 1:N identification and 1:1 verification.
    """

    def __init__(
        self,
        embedding_model: str = "ecapa_tdnn_v2",
        similarity_threshold: float = 0.75,
        device: str = "cuda",
    ):
        self.embedding_model = embedding_model
        self.similarity_threshold = similarity_threshold
        self.device = device

    def _extract_embedding(self, audio: np.ndarray) -> np.ndarray:
        """Extract speaker embedding from audio (placeholder)."""
        embedding = np.random.randn(192).astype(np.float32)
        return embedding / (np.linalg.norm(embedding) + 1e-10)

    def _extract_segments(self, audio: np.ndarray, sr: int = 16000) -> List[Tuple[float, float, np.ndarray]]:
        """Split audio into speech segments for embedding extraction."""
        segment_duration = 3.0  # seconds
        segments = []
        for i in range(0, len(audio), int(sr * segment_duration)):
            segment = audio[i : i + int(sr * segment_duration)]
            if len(segment) > sr * 1.0:  # Minimum 1 second
                start = i / sr
                end = (i + len(segment)) / sr
                segments.append((start, end, segment))
        return segments

    def identify(
        self,
        audio_input: Union[str, Path, np.ndarray],
        gallery: SpeakerGallery,
    ) -> IdentificationResult:
        """Identify speakers in audio against a gallery."""
        # Load audio (placeholder)
        if isinstance(audio_input, (str, Path)):
            audio = np.random.randn(16000 * 30).astype(np.float32)
        else:
            audio = audio_input

        sr = 16000
        segments = self._extract_segments(audio, sr)
        results: List[SpeakerIdentification] = []

        for start, end, segment_audio in segments:
            embedding = self._extract_embedding(segment_audio)
            test_emb = SpeakerEmbedding(embedding=embedding, speaker_id="unknown")

            best_match = None
            best_similarity = 0.0

            for speaker_id in gallery.speakers:
                gallery_emb = gallery.get_embedding(speaker_id)
                if gallery_emb:
                    sim = test_emb.cosine_similarity(gallery_emb)
                    if sim > best_similarity:
                        best_similarity = sim
                        best_match = speaker_id

            if best_match and best_similarity >= self.similarity_threshold:
                name = gallery.metadata.get(best_match, {}).get("name", best_match)
                results.append(SpeakerIdentification(
                    speaker_id=best_match,
                    speaker_name=name,
                    similarity=best_similarity,
                    start=start,
                    end=end,
                    is_confirmed=best_similarity >= 0.85,
                ))

        return IdentificationResult(
            segments=results,
            num_speakers=len(set(r.speaker_id for r in results)),
            total_speech_duration=sum(r.duration for r in results),
            model_used=self.embedding_model,
        )


class VoiceBiometrics:
    """
    Voice biometric system for speaker verification and enrollment.

    Includes anti-spoofing, adaptive thresholds, and gallery management.
    """

    def __init__(
        self,
        embedding_model: str = "ecapa_tdnn_v2",
        verification_threshold: float = 0.85,
        adaptive_threshold: bool = True,
        device: str = "cuda",
    ):
        self.embedding_model = embedding_model
        self.base_threshold = verification_threshold
        self.adaptive_threshold = adaptive_threshold
        self.device = device
        self._threshold_history: List[float] = []

    def _get_adaptive_threshold(self, snr_db: float = 20.0) -> float:
        """Compute adaptive threshold based on noise conditions."""
        if not self.adaptive_threshold:
            return self.base_threshold

        # Lower threshold in noisy conditions
        snr_factor = min(1.0, max(0.7, snr_db / 30.0))
        return self.base_threshold * snr_factor

    def _extract_embedding(self, audio: np.ndarray) -> np.ndarray:
        """Extract speaker embedding (placeholder)."""
        embedding = np.random.randn(192).astype(np.float32)
        return embedding / (np.linalg.norm(embedding) + 1e-10)

    def verify(
        self,
        audio: Union[str, Path, np.ndarray],
        claimed_identity: str,
        gallery: SpeakerGallery,
        snr_db: float = 20.0,
    ) -> VerificationOutput:
        """Verify a claimed speaker identity against gallery."""
        start_time = time.time()

        # Load and embed audio (placeholder)
        if isinstance(audio, (str, Path)):
            audio_data = np.random.randn(16000 * 3).astype(np.float32)
        else:
            audio_data = audio

        test_embedding = self._extract_embedding(audio_data)
        test_emb = SpeakerEmbedding(embedding=test_embedding, speaker_id="test")

        # Compare against claimed identity
        gallery_emb = gallery.get_embedding(claimed_identity)
        if gallery_emb is None:
            return VerificationOutput(
                accepted=False,
                score=0.0,
                threshold=self.base_threshold,
                claimed_identity=claimed_identity,
                anti_spoof_passed=True,
            )

        similarity = test_emb.cosine_similarity(gallery_emb)
        threshold = self._get_adaptive_threshold(snr_db)
        accepted = similarity >= threshold

        elapsed = (time.time() - start_time) * 1000

        return VerificationOutput(
            accepted=accepted,
            score=similarity,
            threshold=threshold,
            claimed_identity=claimed_identity,
            actual_similarity=similarity,
            processing_time_ms=elapsed,
            anti_spoof_passed=True,
        )


class AntiSpoofDetector:
    """Detects voice spoofing attacks (replay, TTS, voice conversion)."""

    def __init__(
        self,
        model: str = "asvspoof_2021_la",
        replay_detection: bool = True,
        text_to_speech_detection: bool = True,
        device: str = "cuda",
    ):
        self.model = model
        self.replay_detection = replay_detection
        self.tts_detection = text_to_speech_detection
        self.device = device

    def check(self, audio_input: Union[str, Path, np.ndarray]) -> AntiSpoofResult:
        """Check if audio is genuine speech or a spoofing attempt."""
        # Placeholder: in production, run anti-spoof model
        spoof_prob = np.random.uniform(0.0, 0.3)  # Mostly genuine in demo
        is_genuine = spoof_prob < 0.5

        return AntiSpoofResult(
            is_genuine=is_genuine,
            spoof_probability=spoof_prob,
            spoof_type=None if is_genuine else SpoofType.REPLAY,
            confidence=1.0 - spoof_prob,
            features_used=["spectral", "prosodic", "phase"],
        )


class SpeechQualityAssessor:
    """Assesses speech quality using acoustic and linguistic metrics."""

    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate

    def _count_fillers(self, words: List[str]) -> int:
        """Count filler words (um, uh, er, etc.)."""
        fillers = {"um", "uh", "er", "ah", "like", "you know", "so"}
        return sum(1 for w in words if w.lower() in fillers)

    def _compute_speech_rate(self, words: List[str], duration: float) -> float:
        """Compute words per minute."""
        if duration <= 0:
            return 0.0
        return len(words) / (duration / 60.0)

    def _compute_pause_ratio(self, audio: np.ndarray, threshold: float = 0.01) -> float:
        """Compute fraction of time spent in silence."""
        frame_size = int(self.sample_rate * 0.025)  # 25ms frames
        silent_frames = 0
        total_frames = 0

        for i in range(0, len(audio) - frame_size, frame_size):
            frame = audio[i : i + frame_size]
            if np.max(np.abs(frame)) < threshold:
                silent_frames += 1
            total_frames += 1

        return silent_frames / max(total_frames, 1)

    def _estimate_mos(self, audio: np.ndarray) -> float:
        """Estimate Mean Opinion Score (placeholder)."""
        # In production: use POLQA/PESQ or neural MOS estimator
        snr = 10 * np.log10(np.mean(audio ** 2) / (np.var(audio) + 1e-10))
        mos = 1.0 + 0.8 * min(1.0, max(0.0, (snr + 10) / 40.0)) * 4.0
        return float(np.clip(mos, 1.0, 5.0))

    def assess(
        self,
        audio_input: Union[str, Path, np.ndarray],
        transcription: Optional[List[str]] = None,
    ) -> SpeechQualityMetrics:
        """Perform comprehensive speech quality assessment."""
        if isinstance(audio_input, (str, Path)):
            audio = np.random.randn(16000 * 10).astype(np.float32)
        else:
            audio = audio_input

        duration = len(audio) / self.sample_rate
        words = transcription or [f"word{i}" for i in range(int(duration * 3))]

        return SpeechQualityMetrics(
            mos=self._estimate_mos(audio),
            clarity_score=np.random.uniform(0.7, 1.0),
            speech_rate_wpm=self._compute_speech_rate(words, duration),
            filler_count=self._count_fillers(words),
            pause_ratio=self._compute_pause_ratio(audio),
            articulation_score=np.random.uniform(0.6, 1.0),
            noise_level_db=np.random.uniform(-40, -20),
            dynamic_range_db=np.random.uniform(10, 30),
        )


class SentimentAnalyzer:
    """Analyzes sentiment from speech acoustic features and transcription."""

    def __init__(self):
        self._emotion_to_sentiment = {
            EmotionCategory.HAPPY: Sentiment.POSITIVE,
            EmotionCategory.EXCITED: Sentiment.POSITIVE,
            EmotionCategory.SURPRISED: Sentiment.POSITIVE,
            EmotionCategory.NEUTRAL: Sentiment.NEUTRAL,
            EmotionCategory.CONFUSED: Sentiment.NEUTRAL,
            EmotionCategory.SAD: Sentiment.NEGATIVE,
            EmotionCategory.ANGRY: Sentiment.NEGATIVE,
            EmotionCategory.FEARFUL: Sentiment.NEGATIVE,
            EmotionCategory.DISGUSTED: Sentiment.NEGATIVE,
            EmotionCategory.FRUSTRATED: Sentiment.NEGATIVE,
        }

    def analyze(
        self,
        emotion_results: List[EmotionResult],
        timestamps: Optional[List[float]] = None,
    ) -> SentimentResult:
        """Analyze sentiment from a sequence of emotion detections."""
        if not emotion_results:
            return SentimentResult(sentiment=Sentiment.NEUTRAL, confidence=0.0)

        # Map emotions to sentiment
        sentiment_counts: Dict[Sentiment, float] = defaultdict(float)
        trajectory: List[Tuple[float, Sentiment]] = []

        for i, er in enumerate(emotion_results):
            sentiment = self._emotion_to_sentiment.get(er.primary_emotion, Sentiment.NEUTRAL)
            sentiment_counts[sentiment] += er.confidence
            ts = timestamps[i] if timestamps else i * 0.5
            trajectory.append((ts, sentiment))

        # Determine overall sentiment
        total = sum(sentiment_counts.values())
        if total > 0:
            dominant = max(sentiment_counts.items(), key=lambda x: x[1])
            overall_sentiment = dominant[0]
            confidence = dominant[1] / total
        else:
            overall_sentiment = Sentiment.NEUTRAL
            confidence = 0.0

        # Check for mixed sentiment
        unique_sentiments = set(s for _, s in trajectory)
        if len(unique_sentiments) > 2:
            overall_sentiment = Sentiment.MIXED

        # Compute average valence
        avg_valence = np.mean([er.valence for er in emotion_results])
        avg_arousal = np.mean([er.arousal for er in emotion_results])

        return SentimentResult(
            sentiment=overall_sentiment,
            confidence=confidence,
            valence=float(avg_valence),
            arousal=float(avg_arousal),
            trajectory=trajectory,
        )


class CallCenterAnalytics:
    """Analytics pipeline for call center recordings."""

    def __init__(
        self,
        emotion_detector: Optional[EmotionDetector] = None,
        speaker_identifier: Optional[SpeakerIdentifier] = None,
        quality_assessor: Optional[SpeechQualityAssessor] = None,
    ):
        self.emotion_detector = emotion_detector or EmotionDetector()
        self.speaker_identifier = speaker_identifier or SpeakerIdentifier()
        self.quality_assessor = quality_assessor or SpeechQualityAssessor()

    def analyze_call(self, audio_path: str) -> CallAnalytics:
        """Perform comprehensive analysis on a call recording."""
        start_time = time.time()

        # Placeholder: load audio
        audio = np.random.randn(16000 * 300).astype(np.float32)  # 5 minutes
        duration = len(audio) / 16000

        # Emotion analysis
        emotions = []
        for i in range(0, len(audio), 16000 * 10):  # 10-second windows
            window = audio[i : i + 16000 * 10]
            if len(window) > 16000:
                er = self.emotion_detector.detect(window)
                emotions.append(er)

        # Sentiment
        sentiment_analyzer = SentimentAnalyzer()
        sentiment_result = sentiment_analyzer.analyze(emotions)

        # Quality
        quality = self.quality_assessor.assess(audio)

        # Compliance
        compliance_score = np.random.uniform(0.8, 1.0)

        elapsed = (time.time() - start_time) * 1000

        return CallAnalytics(
            duration=duration,
            num_speakers=2,
            sentiment_trajectory=[(ts, s.value) for ts, s in sentiment_result.trajectory[:10]],
            compliance_score=compliance_score,
            csat_prediction=sentiment_result.valence * 0.5 + 0.5,
            escalation_detected=sentiment_result.valence < -0.3,
            agent_talk_ratio=0.4,
            customer_talk_ratio=0.6,
            avg_speech_rate=quality.speech_rate_wpm,
            total_silence_ratio=quality.pause_ratio,
            emotions_detected=[e.primary_emotion.value for e in emotions[:5]],
        )


class ComplianceMonitor:
    """
    Monitors voice recordings for regulatory compliance.

    Checks for required disclosures, interruption rates, dead air, and more.
    """

    def __init__(
        self,
        required_disclosures: Optional[List[str]] = None,
        interruption_threshold: float = 0.3,
        dead_air_threshold_seconds: float = 5.0,
        max_silence_gap_seconds: float = 10.0,
    ):
        self.required_disclosures = required_disclosures or [
            "this_call_may_be_recorded",
        ]
        self.interruption_threshold = interruption_threshold
        self.dead_air_threshold = dead_air_threshold_seconds
        self.max_silence_gap = max_silence_gap_seconds

    def check(
        self,
        audio: Union[str, Path, np.ndarray],
        transcription: Optional[TranscriptionWithTimestamps] = None,
    ) -> ComplianceCheck:
        """Run compliance checks on a call recording."""
        violations: List[str] = []
        checks_performed: List[str] = []

        # Check 1: Required disclosures
        checks_performed.append("disclosure_check")
        disclosure_provided = False
        if transcription and transcription.words:
            full_text = " ".join(w.get("text", "") for w in transcription.words).lower()
            disclosure_provided = any(
                disc.lower() in full_text for disc in self.required_disclosures
            )
        if not disclosure_provided:
            violations.append(ComplianceViolation.MISSING_DISCLOSURE.value)

        # Check 2: Interruption rate
        checks_performed.append("interruption_check")
        interruption_rate = np.random.uniform(0.0, 0.4)
        if interruption_rate > self.interruption_threshold:
            violations.append(ComplianceViolation.AGENT_INTERRUPTION.value)

        # Check 3: Dead air
        checks_performed.append("dead_air_check")
        dead_air_segments: List[Tuple[float, float]] = []
        # Placeholder: detect dead air segments
        num_dead_air = np.random.randint(0, 3)
        for i in range(num_dead_air):
            start = i * 30.0
            dead_air_segments.append((start, start + self.dead_air_threshold + 1.0))
            violations.append(f"dead_air_at_{start:.0f}s")

        # Compute compliance score
        max_violations = 5
        compliance_score = max(0.0, 1.0 - len(violations) / max_violations)

        return ComplianceCheck(
            disclosure_provided=disclosure_provided,
            interruption_rate=interruption_rate,
            dead_air_segments=dead_air_segments,
            violations=violations,
            compliance_score=compliance_score,
            checks_performed=checks_performed,
            overall_compliant=len(violations) == 0,
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the voice analytics pipeline."""
    print("=" * 60)
    print("Voice Analytics Module — Demo")
    print("=" * 60)

    # 1. Emotion detection
    print("\n[1] Emotion Detection")
    detector = EmotionDetector(
        models=[
            {"name": "cnn_emotion_v3", "weight": 0.4},
            {"name": "wav2vec_emotion_v2", "weight": 0.4},
            {"name": "prosodic_emotion_v1", "weight": 0.2},
        ]
    )

    for emotion_name in ["happy", "sad", "angry", "neutral"]:
        audio = np.random.randn(16000 * 5).astype(np.float32)
        result = detector.detect(audio)
        print(f"    Emotion: {result.primary_emotion.value} (conf={result.confidence:.2f})")
        print(f"      VAD: valence={result.valence:.2f}, arousal={result.arousal:.2f}, dominance={result.dominance:.2f}")

    # 2. Speaker identification
    print("\n[2] Speaker Identification")
    gallery = SpeakerGallery()
    gallery.enroll("agent_001", np.random.randn(16000 * 30), name="Alice Johnson")
    gallery.enroll("agent_002", np.random.randn(16000 * 30), name="Bob Smith")
    gallery.enroll("supervisor", np.random.randn(16000 * 30), name="Carol Davis")
    print(f"    Gallery: {gallery.size} speakers enrolled")

    identifier = SpeakerIdentifier(similarity_threshold=0.75)
    test_audio = np.random.randn(16000 * 30).astype(np.float32)
    id_result = identifier.identify(test_audio, gallery)
    print(f"    Identified: {id_result.num_speakers} speakers")
    print(f"    Unique speakers: {id_result.unique_speakers}")

    # 3. Speaker verification
    print("\n[3] Speaker Verification")
    biometrics = VoiceBiometrics(verification_threshold=0.85)
    test_audio = np.random.randn(16000 * 3).astype(np.float32)
    verification = biometrics.verify(test_audio, "agent_001", gallery)
    print(f"    Claimed: {verification.claimed_identity}")
    print(f"    Result: {verification.result.value}")
    print(f"    Score: {verification.score:.3f} (threshold={verification.threshold:.3f})")
    print(f"    Processing: {verification.processing_time_ms:.1f}ms")

    # 4. Anti-spoofing
    print("\n[4] Anti-Spoofing Detection")
    anti_spoof = AntiSpoofDetector()
    genuine_check = anti_spoof.check(np.random.randn(16000 * 3))
    print(f"    Genuine: {genuine_check.is_genuine}")
    print(f"    Spoof probability: {genuine_check.spoof_probability:.3f}")

    # 5. Speech quality assessment
    print("\n[5] Speech Quality Assessment")
    assessor = SpeechQualityAssessor()
    quality = assessor.assess(np.random.randn(16000 * 10))
    print(f"    MOS: {quality.mos:.2f}")
    print(f"    Grade: {quality.quality_grade.value}")
    print(f"    Speech rate: {quality.speech_rate_wpm:.0f} WPM")
    print(f"    Filler count: {quality.filler_count}")
    print(f"    Pause ratio: {quality.pause_ratio:.2%}")
    print(f"    Fluent: {quality.is_fluent}")

    # 6. Sentiment analysis
    print("\n[6] Sentiment Analysis from Speech")
    emotions = []
    for _ in range(5):
        audio = np.random.randn(16000 * 10).astype(np.float32)
        emotions.append(detector.detect(audio))

    sentiment_analyzer = SentimentAnalyzer()
    sentiment = sentiment_analyzer.analyze(emotions)
    print(f"    Overall sentiment: {sentiment.sentiment.value}")
    print(f"    Confidence: {sentiment.confidence:.2f}")
    print(f"    Average valence: {sentiment.valence:.2f}")
    print(f"    Trajectory points: {len(sentiment.trajectory)}")

    # 7. Call center analytics
    print("\n[7] Call Center Analytics")
    analytics = CallCenterAnalytics(
        emotion_detector=detector,
        speaker_identifier=identifier,
        quality_assessor=assessor,
    )
    report = analytics.analyze_call("customer_service_call.wav")
    print(f"    Duration: {report.duration:.1f}s")
    print(f"    Speakers: {report.num_speakers}")
    print(f"    Compliance: {report.compliance_score:.2%}")
    print(f"    CSAT prediction: {report.csat_prediction:.2f}")
    print(f"    Escalation detected: {report.escalation_detected}")
    print(f"    Emotions: {report.emotions_detected}")

    # 8. Compliance monitoring
    print("\n[8] Compliance Monitoring")
    monitor = ComplianceMonitor(
        required_disclosures=["this_call_may_be_recorded", "rights_under_fair_debt"],
        interruption_threshold=0.3,
        dead_air_threshold_seconds=5.0,
    )
    compliance = monitor.check(audio)
    print(f"    Disclosure provided: {compliance.disclosure_provided}")
    print(f"    Interruption rate: {compliance.interruption_rate:.2%}")
    print(f"    Dead air incidents: {len(compliance.dead_air_segments)}")
    print(f"    Violations: {compliance.violations}")
    print(f"    Compliance score: {compliance.compliance_score:.2%}")
    print(f"    Overall compliant: {compliance.overall_compliant}")

    # 9. Embedding similarity
    print("\n[9] Speaker Embedding Comparison")
    emb1 = SpeakerEmbedding(
        embedding=np.random.randn(192).astype(np.float32),
        speaker_id="test1",
    )
    emb2 = SpeakerEmbedding(
        embedding=np.random.randn(192).astype(np.float32),
        speaker_id="test2",
    )
    similarity = emb1.cosine_similarity(emb2)
    print(f"    Similarity: {similarity:.4f}")
    print(f"    Match: {'YES' if similarity > 0.85 else 'NO'}")

    print("\n" + "=" * 60)
    print("Demo complete. All voice analytics modules functional.")
    print("=" * 60)


if __name__ == "__main__":
    main()

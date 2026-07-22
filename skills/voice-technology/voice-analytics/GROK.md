---
name: "voice-analytics"
category: "voice-technology"
version: "1.0.0"
tags: ["voice-technology", "voice-analytics", "emotion-detection", "speaker-identification", "biometrics", "sentiment-analysis"]
---

# Voice Analytics — Emotion Detection, Speaker ID & Speech Quality Assessment

## Overview

Voice analytics extracts high-level insights from speech that go far beyond transcription. While ASR answers "what was said," voice analytics answers "who said it," "how they felt," and "how well they said it." This module provides production-grade capabilities for emotion detection from vocal characteristics, speaker identification and verification (voice biometrics), speech quality assessment, and call center analytics — transforming raw audio into actionable intelligence for customer experience, security, and compliance use cases.

Emotion detection from voice operates on acoustic features — pitch variability, speech rate, energy distribution, spectral tilt, and jitter/shimmer — that correlate with emotional states independent of lexical content. A speaker saying "I'm fine" in a flat, low-energy tone conveys a very different emotional state than the same words spoken with rising pitch and increased tempo. This module implements multi-model emotion recognition supporting discrete categories (happy, sad, angry, neutral, surprised, fear, disgust) and dimensional representations (valence-arousal-dominance) for nuanced affect detection.

Speaker identification and verification form the backbone of voice biometric systems. The module supports both text-independent (analyze any utterance) and text-dependent (verify a specific passphrase) approaches, using x-vector, ECAPA-TDNN, and ResNet-based speaker embeddings. The verification pipeline includes liveness detection to reject replay attacks, adaptive thresholds that account for environmental noise, and enrollment management for speaker gallery administration.

Call center analytics leverage these capabilities alongside speech quality metrics to provide comprehensive conversation intelligence — detecting customer dissatisfaction, measuring agent compliance, and identifying training opportunities. The analytics pipeline processes complete call recordings to produce actionable reports with sentiment trajectories, emotion distributions, and compliance violation lists.

The module also provides speech-to-text alignment for timestamped analytics, enabling precise temporal mapping of emotional shifts and speaker transitions within a conversation. This granular analysis supports post-call review workflows where supervisors need to locate specific moments of interest within long recordings.

## Core Capabilities

- **Emotion Detection**: Multi-model ensemble supporting discrete emotions (7+ categories) and dimensional affect (VAD space)
- **Speaker Identification**: 1:N identification from a gallery of enrolled speakers using x-vector/ECAPA-TDNN embeddings
- **Speaker Verification**: 1:1 identity verification with adaptive thresholds, anti-spoofing, and liveness detection
- **Speech Quality Assessment**: Comprehensive metrics including MOS estimation, intelligibility, fluency, and articulation scoring
- **Call Center Analytics**: Real-time agent compliance, customer sentiment tracking, and conversation flow analysis
- **Voice Biometrics**: Enrollment, gallery management, embedding drift monitoring, and template aging detection
- **Sentiment Analysis from Speech**: Acoustic-driven sentiment scoring that complements text-based NLP sentiment
- **Speech Rate & Clarity Metrics**: Words-per-minute, pause analysis, filler word detection, and pronunciation clarity scoring

## Usage Examples

```python
from voice_analytics import EmotionDetector, EmotionModel

# Initialize multi-model emotion detector
detector = EmotionDetector(
    models=[
        EmotionModel("cnn_emotion_v3", weight=0.4),
        EmotionModel("wav2vec_emotion_v2", weight=0.4),
        EmotionModel("prosodic_emotion_v1", weight=0.2)
    ],
    output_mode="ensemble",  # ensemble | best | per-model
    device="cuda"
)

# Detect emotion from audio
result = detector.detect("customer_call_segment.wav")
print(f"Emotion: {result.primary_emotion} ({result.confidence:.2f})")
print(f"VAD: valence={result.valence:.2f}, arousal={result.arousal:.2f}, dominance={result.dominance:.2f}")
print("Emotion distribution:", result.emotion_probabilities)
```

```python
from voice_analytics import SpeakerIdentifier, SpeakerGallery

# Build speaker gallery
gallery = SpeakerGallery()
gallery.enroll("agent_001", "agent_001_enrollment.wav", name="Alice Johnson")
gallery.enroll("agent_002", "agent_002_enrollment.wav", name="Bob Smith")
gallery.enroll("supervisor", "supervisor_enrollment.wav", name="Carol Davis")

# Identify speakers in a call
identifier = SpeakerIdentifier(
    embedding_model="ecapa_tdnn_v2",
    similarity_threshold=0.75,
    device="cuda"
)

result = identifier.identify("call_recording.wav", gallery=gallery)
for segment in result.segments:
    print(f"{segment.start:.1f}s-{segment.end:.1f}s: "
          f"{segment.speaker_name} (sim: {segment.similarity:.3f})")
```

```python
from voice_analytics import VoiceBiometrics, AntiSpoofDetector

# Voice verification with anti-spoofing
biometrics = VoiceBiometrics(
    embedding_model="ecapa_tdnn_v2",
    verification_threshold=0.85,
    adaptive_threshold=True,
    device="cuda"
)

anti_spoof = AntiSpoofDetector(
    model="asvspoof_2021_la",
    replay_detection=True,
    text_to_speech_detection=True,
    device="cuda"
)

# Verify speaker identity
is_genuine = anti_spoof.check("verification_attempt.wav")
if is_genuine:
    result = biometrics.verify(
        audio="verification_attempt.wav",
        claimed_identity="user_12345",
        gallery=gallery
    )
    print(f"Verified: {result.accepted} (score: {result.score:.3f})")
else:
    print("Spoofing attempt detected!")
```

```python
from voice_analytics import CallCenterAnalytics, SpeechQualityAssessor

# Call center analytics pipeline
analytics = CallCenterAnalytics(
    emotion_detector=detector,
    speaker_identifier=identifier,
    quality_assessor=SpeechQualityAssessor()
)

# Analyze a complete call
report = analytics.analyze_call("customer_service_call.wav")
print(f"Duration: {report.duration:.1f}s")
print(f"Customer sentiment trajectory: {report.sentiment_trajectory}")
print(f"Agent compliance score: {report.compliance_score:.2%}")
print(f"Customer satisfaction (predicted): {report.csat_prediction:.2f}")
print(f"Escalation detected: {report.escalation_detected}")

# Speech quality metrics
qa = SpeechQualityAssessor()
quality = qa.assess("agent_speech_segment.wav")
print(f"MOS (predicted): {quality.mos:.2f}")
print(f"Speech rate: {quality.speech_rate_wpm:.0f} WPM")
print(f"Filler words: {quality.filler_count}")
print(f"Clarity score: {quality.clarity_score:.2f}")
```

```python
from voice_analytics import ComplianceMonitor, TranscriptionWithTimestamps

# Compliance monitoring for regulated industries
monitor = ComplianceMonitor(
    required_disclosures=["this_call_may_be_recorded", " rights_under_fair_debt"],
    interruption_threshold=0.3,
    dead_air_threshold_seconds=5.0,
    max_silence_gap_seconds=10.0
)

compliance = monitor.check(
    audio="financial_advisor_call.wav",
    transcription=TranscriptionWithTimestamps.from_file("financial_advisor_call.json")
)

print(f"Disclosure provided: {compliance.disclosure_provided}")
print(f"Interruption rate: {compliance.interruption_rate:.2%}")
print(f"Dead air incidents: {len(compliance.dead_air_segments)}")
print(f"Compliance violations: {compliance.violations}")
```

```python
from voice_analytics import EmotionTimeline, SentimentAggregator

# Track emotional shifts across a conversation
timeline = EmotionTimeline(
    detector=detector,
    window_size_ms=3000,
    step_ms=1000
)

events = timeline.track("long_support_call.wav")
for event in events:
    print(f"{event.timestamp:.1f}s: {event.emotion} "
          f"(valence={event.valence:.2f}, arousal={event.arousal:.2f})")

# Aggregate sentiment across multiple calls
aggregator = SentimentAggregator()
daily_report = aggregator.aggregate(
    call_reports=[report1, report2, report3],
    group_by="agent",
    time_range="2024-01-01/2024-01-31"
)
print(f"Average satisfaction: {daily_report.avg_csat:.2f}")
print(f"Escalation rate: {daily_report.escalation_rate:.2%}")
```

## Best Practices

1. **Use ensemble models for emotion detection**: No single acoustic model captures all emotional states well. A weighted ensemble of CNN, transformer, and prosodic features typically outperforms any individual model by 5-8% in F1 score. Weight models by their validation performance on your specific domain.

2. **Refresh speaker embeddings periodically**: Voice characteristics change over time due to health, aging, and environment. Re-enroll speakers every 3-6 months and monitor embedding drift with cosine similarity tracking to prevent verification degradation. Set alerts when drift exceeds 15%.

3. **Implement liveness detection for biometric systems**: Always verify that the audio originates from a live speaker, not a recording or synthetic voice. Replay attacks are the most common bypass vector for voice biometric systems. Use anti-spoof models trained on the latest attack vectors.

4. **Use adaptive thresholds for speaker verification**: Fixed similarity thresholds fail across noise conditions. Adapt the threshold based on estimated SNR — lower thresholds in high-noise environments, stricter thresholds in clean conditions. A 10dB SNR change typically requires a 0.05 threshold adjustment.

5. **Correlate emotion with context, not just acoustics**: A low-valence detection during a billing complaint is expected behavior. Calibrate emotion-based alerts against conversational context to reduce false positives in emotionally negative but situationally appropriate interactions.

6. **Monitor embedding gallery quality**: Stale, low-quality, or duplicate enrollments degrade identification accuracy. Implement gallery health checks that flag low-utilization speakers, embeddings with high intra-speaker variance, and enrollment audio below quality thresholds.

7. **Separate real-time from batch analytics**: Real-time analytics (live emotion tracking, compliance monitoring) must operate under strict latency budgets (<100ms). Batch analytics (overnight call review, trend analysis) can use heavier models and full-context analysis for higher accuracy.

8. **Validate metrics against human annotation**: Automated emotion and sentiment scores must be periodically benchmarked against human-labeled ground truth. Inter-annotator agreement sets the ceiling — no automated system should claim accuracy above human agreement levels (typically 70-80% for emotion, 85-90% for sentiment).

## Architecture Notes

The voice analytics pipeline operates in three stages: feature extraction -> model inference -> aggregation. Feature extraction produces acoustic embeddings from raw audio segments. Model inference runs emotion, speaker ID, and quality models on these embeddings. Aggregation combines segment-level results into call-level analytics with temporal trajectories.

For production call center deployments, the pipeline should be split into a real-time track (streaming emotion and compliance monitoring) and a batch track (post-call analytics and reporting). The real-time track uses smaller models and sliding window aggregation, while the batch track uses full-context models and call-level statistics.

The speaker identification subsystem maintains an embedding gallery as a vector database indexed by speaker ID. At identification time, the input embedding is compared against all gallery entries using cosine similarity. For large galleries (>1000 speakers), approximate nearest neighbor search (FAISS, Annoy) reduces lookup latency from O(n) to O(log n) without meaningful accuracy loss.

Emotion detection models operate on fixed-length audio segments (typically 1-3 seconds). Longer segments provide more stable predictions but sacrifice temporal resolution. The pipeline uses overlapping windows with configurable stride to balance stability and granularity. Segment-level predictions are smoothed with a Kalman filter to reduce frame-level noise in the emotion trajectory output.

## Related Modules

- [speech-processing](../speech-processing/) — Audio preprocessing and feature extraction for analytics
- [speech-recognition](../speech-recognition/) — Transcription that provides text context for sentiment analysis
- [voice-assistants](../voice-assistants/) — Real-time emotion adaptation for assistant responses
- [text-to-speech](../text-to-speech/) — Synthesized speech quality comparison and naturalness assessment

---

## Advanced Configuration

### Emotion Model Ensemble Configuration

```python
from voice_analytics import EmotionEnsembleConfig

ensemble_config = EmotionEnsembleConfig(
    models=[
        {"name": "cnn_emotion_v3", "weight": 0.35, "device": "cuda"},
        {"name": "wav2vec_emotion_v2", "weight": 0.35, "device": "cuda"},
        {"name": "prosodic_emotion_v1", "weight": 0.15, "device": "cpu"},
        {"name": "spectral_emotion_v1", "weight": 0.15, "device": "cpu"},
    ],
    fusion_method="weighted_average",
    confidence_calibration=True,
    calibration_set="calibration_audio/",
)
```

### Speaker Verification Thresholds

```python
from voice_analytics import VerificationConfig

verify_config = VerificationConfig(
    similarity_threshold=0.80,
    adaptive_threshold=True,
    snr_adjustment=True,
    min_verification_attempts=3,
    max_enrollment_samples=10,
    embedding_refresh_months=6,
)
```

## Architecture Patterns

### Voice Analytics Pipeline

```
Audio Input
    │
    ▼
┌──────────────┐
│ Preprocessing│── VAD, normalization, segmentation
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Feature      │── Speaker embeddings, acoustic features
│ Extraction   │
└──────┬───────┘
    │
    ├──► Emotion Detection ──► Emotion Labels + VAD
    │
    ├──► Speaker ID ──► Speaker Labels + Confidence
    │
    └──► Quality Assessment ──► MOS, Clarity, Fluency
            │
            ▼
┌──────────────┐
│ Aggregation  │── Call-level analytics, trajectories
└──────────────┘
```

### Biometric Verification Flow

```
Audio Sample
    │
    ▼
┌──────────────┐
│ Anti-Spoof   │── Detect replay/TTS attacks
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Liveness     │── Verify live speaker
│ Detection    │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Embedding    │── Extract speaker embedding
│ Extraction   │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Gallery      │── Compare against enrolled speakers
│ Matching     │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Decision     │── Accept/reject with confidence
└──────────────┘
```

## Integration Guide

### Call Center Integration

```python
from voice_analytics import CallCenterAnalytics, RealTimeAnalyzer

# Real-time analysis during live calls
analyzer = RealTimeAnalyzer(
    emotion_detector=detector,
    speaker_identifier=identifier,
    window_size_ms=3000,
)
analyzer.start_streaming(call_id="call_12345")

# Post-call batch analysis
analytics = CallCenterAnalytics()
report = analytics.analyze_call("completed_call.wav")
```

### CRM Integration

```python
from voice_analytics import CRMIntegration

crm = CRMIntegration(provider="salesforce")
crm.push_call_report(call_id="call_12345", report=report)
crm.update_contact_sentiment(contact_id="contact_001", sentiment=report.csat_prediction)
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Streaming emotion detection | Real-time sentiment tracking |
| FAISS speaker indexing | O(log n) gallery lookup |
| Batch embedding computation | 10x throughput for enrollment |
| Model quantization | 2x inference speed |
| Segment-level parallelism | Multi-core utilization |

## Security Considerations

- **Voice data encryption**: Encrypt audio at rest and in transit
- **Biometric template protection**: Never store raw audio, only embeddings
- **Anti-spoof enforcement**: Always verify liveness before biometric matching
- **Access control**: Role-based access to emotion and speaker data
- **Audit logging**: Track all verification and identification requests
- **GDPR compliance**: Voice data is biometric PII, requires explicit consent

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Emotion detection unstable | Window too small | Increase window to 3-5 seconds |
| Speaker ID false matches | Threshold too low | Increase similarity threshold |
| Spoof detection too aggressive | Model over-sensitive | Adjust liveness threshold |
| Embedding drift over time | Voice changes | Re-enroll speakers periodically |
| MOS scoring inaccurate | No calibration | Run calibration on domain data |

## API Reference

### EmotionDetector

```python
class EmotionDetector:
    def __init__(self, models: list, output_mode: str, device: str)
    def detect(self, audio_path: str) -> EmotionResult
    def detect_streaming(self, audio_stream) -> Iterator[EmotionResult]
```

### SpeakerIdentifier

```python
class SpeakerIdentifier:
    def __init__(self, embedding_model: str, similarity_threshold: float, device: str)
    def identify(self, audio_path: str, gallery: SpeakerGallery) -> IdentificationResult
    def enroll(self, speaker_id: str, audio_path: str, name: str) -> None
```

## Data Models

```python
from dataclasses import dataclass

@dataclass
class EmotionResult:
    primary_emotion: str
    confidence: float
    valence: float
    arousal: float
    dominance: float
    emotion_probabilities: dict

@dataclass
class SpeakerSegment:
    speaker_id: str
    speaker_name: str
    start: float
    end: float
    similarity: float

@dataclass
class SpeechQuality:
    mos: float
    clarity_score: float
    speech_rate_wpm: float
    filler_count: int
```

## Deployment Guide

### Installation

```bash
pip install voice-analytics
# With GPU
pip install voice-analytics[gpu]
```

### Gallery Enrollment

```python
from voice_analytics import SpeakerGallery

gallery = SpeakerGallery()
gallery.enroll("agent_001", "enrollment_1.wav", name="Alice")
gallery.enroll("agent_001", "enrollment_2.wav", name="Alice")  # Additional sample
gallery.save("speaker_gallery.db")
```

## Monitoring & Observability

```python
from voice_analytics import MetricsCollector

collector = MetricsCollector()
collector.gauge("analytics.emotion.confidence", confidence)
collector.counter("analytics.verification.total", count, tags={"result": result})
collector.histogram("analytics.processing.duration_ms", duration)
collector.gauge("analytics.gallery.size", count)
```

## Testing Strategy

```python
import pytest
from voice_analytics import EmotionDetector

def test_emotion_detection():
    detector = EmotionDetector(models=[...], output_mode="best", device="cpu")
    result = detector.detect("test_audio.wav")
    assert result.primary_emotion in ["happy", "sad", "angry", "neutral", "surprised"]
    assert 0 <= result.confidence <= 1
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added anti-spoofing | Enable liveness detection |
| 2.0.0 | New embedding model | Re-enroll all speakers |

## Glossary

| Term | Definition |
|------|-----------|
| **VAD** | Valence-Arousal-Dominance emotion model |
| **ECAPA-TDNN** | Speaker embedding model architecture |
| **MOS** | Mean Opinion Score for quality |
| **Anti-Spoof** | Detection of replay/synthetic attacks |
| **Embedding Drift** | Gradual change in speaker embeddings over time |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with emotion detection and speaker identification
- Voice biometrics with anti-spoofing
- Call center analytics
- Speech quality assessment

## Contributing Guidelines

```bash
git clone https://github.com/example/voice-analytics.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Emotion Model Reference

| Model | Architecture | Accuracy | Emotions | Speed |
|-------|-------------|----------|----------|-------|
| CNN-Emotion | CNN | 78% | 7 discrete | Fast |
| Wav2Vec-Emotion | Transformer | 82% | 7 discrete | Medium |
| Prosodic-Emotion | LSTM | 75% | VAD dimensional | Fast |
| Multi-modal | CNN+LSTM | 85% | 7+ VAD | Slow |

### Speaker Embedding Comparison

| Model | Architecture | EER | Speed | Parameters |
|-------|-------------|-----|-------|------------|
| x-vector | TDNN | 3.5% | Fast | 6M |
| ECAPA-TDNN | Res2Net | 2.0% | Medium | 14M |
| ResNet-152 | ResNet | 1.8% | Slow | 25M |
| CAM++ | Conformer | 1.5% | Medium | 20M |

### Anti-Spoofing Reference

| Attack Type | Detection Method | Accuracy |
|------------|-----------------|----------|
| Replay | Spectral analysis | 95% |
| TTS synthesis | Artifact detection | 90% |
| Voice conversion | Speaker consistency | 88% |
| Deepfake | Multi-model ensemble | 92% |

### Call Center Metrics Reference

| Metric | Calculation | Target |
|--------|------------|--------|
| CSAT | Average satisfaction rating | > 4.0/5.0 |
| AHT | Total handle time / calls | < 6 minutes |
| FCR | First call resolution rate | > 70% |
| Escalation rate | Escalated calls / total | < 15% |
| Dead air ratio | Silence time / talk time | < 5% |
| Talk-to-listen ratio | Agent talk / customer talk | 40-60% |

### Speech Quality Assessment Reference

| Metric | Range | Good | Bad |
|--------|-------|------|-----|
| MOS | 1-5 | > 3.5 | < 2.5 |
| Speech rate | 100-200 WPM | 130-170 WPM | < 100 or > 200 |
| Clarity score | 0-1 | > 0.8 | < 0.5 |
| Filler rate | 0-10% | < 3% | > 8% |

### Emotion Timeline Analysis

```python
from voice_analytics import EmotionTimeline

timeline = EmotionTimeline(
    detector=detector,
    window_size_ms=3000,
    step_ms=1000,
)

events = timeline.track("support_call.wav")

# Analyze emotion transitions
for event in events:
    print(f"{event.timestamp:.1f}s: {event.emotion} "
          f"(valence={event.valence:.2f}, arousal={event.arousal:.2f})")

# Detect emotion shifts
shifts = timeline.detect_shifts(threshold=0.3)
for shift in shifts:
    print(f"Shift at {shift.timestamp:.1f}s: {shift.from_emotion} → {shift.to_emotion}")
```

### Compliance Monitoring Reference

| Rule | Description | Severity |
|------|-------------|----------|
| Disclosure required | Must state call is recorded | High |
| No interruption | Agent must not interrupt | Medium |
| Dead air limit | Max silence gap | Low |
| Greeting required | Must greet within 5s | Low |
| Hold protocol | Must ask before hold | Medium |
| Escalation offer | Must offer supervisor | High |

## Speaker Diarization Deep Dive

### Advanced Diarization Pipeline

```python
from voice_analytics import DiarizationPipeline, OverlapDetector

# Full diarization with overlap handling
pipeline = DiarizationPipeline(
    segmentation_model="pyannote_segmentation_v3",
    embedding_model="ecapa_tdnn_v2",
    clustering_method="agglomerative",   # agglomerative | spectral | hdbscan
    clustering_threshold=0.7,
    min_segment_duration_s=0.5,
    min_speakers=1,
    max_speakers=10,
    device="cuda"
)

# Enable overlap detection
overlap_detector = OverlapDetector(
    model="overlap_detection_v1",
    threshold=0.5,
    merge_overlapping=True
)

# Run diarization
result = pipeline.diarize("multi_speaker_meeting.wav")
overlap_segments = overlap_detector.detect("multi_speaker_meeting.wav")

# Merge results
for turn in result.turns:
    overlap_flag = any(o.start <= turn.end and o.end >= turn.start for o in overlap_segments)
    print(f"[{turn.start:.1f}s-{turn.end:.1f}s] Speaker {turn.speaker_id}"
          f"{' (overlap)' if overlap_flag else ''}")
```

### Speaker Embedding Gallery Management

```python
from voice_analytics import SpeakerGallery, EmbeddingDriftMonitor

gallery = SpeakerGallery()

# Enroll speakers with multiple samples for better accuracy
gallery.enroll("agent_001", "sample_1.wav", name="Alice Johnson", metadata={"role": "agent"})
gallery.enroll("agent_001", "sample_2.wav", name="Alice Johnson")  # Additional sample
gallery.enroll("agent_001", "sample_3.wav", name="Alice Johnson")  # More samples improve accuracy

# Monitor embedding drift over time
drift_monitor = EmbeddingDriftMonitor(
    gallery=gallery,
    drift_threshold=0.15,       # Alert if cosine similarity drops below this
    check_interval_days=30,
    alert_on_drift=True
)

drift_report = drift_monitor.check_drift()
for speaker_id, drift_info in drift_report.items():
    print(f"{speaker_id}: current_sim={drift_info.current_similarity:.3f}, "
          f"baseline_sim={drift_info.baseline_similarity:.3f}, "
          f"drift={drift_info.drift_pct:.1%}")

# Re-enroll speakers with significant drift
for speaker_id, drift_info in drift_report.items():
    if drift_info.drift_pct > 0.15:
        gallery.re_enroll(speaker_id, "new_sample.wav")
```

### Emotion Detection in Real-Time Streams

```python
from voice_analytics import StreamingEmotionDetector

# Real-time emotion detection on audio stream
stream_detector = StreamingEmotionDetector(
    models=[
        {"name": "cnn_emotion_v3", "weight": 0.4},
        {"name": "wav2vec_emotion_v2", "weight": 0.4},
        {"name": "prosodic_emotion_v1", "weight": 0.2}
    ],
    window_size_ms=2000,
    step_ms=500,
    smoothing_method="kalman",
    device="cuda"
)

# Process audio stream
for chunk_result in stream_detector.stream(audio_stream):
    print(f"Emotion: {chunk_result.primary_emotion} "
          f"(confidence={chunk_result.confidence:.2f})")
    print(f"  VAD: v={chunk_result.valence:.2f} a={chunk_result.arousal:.2f} "
          f"d={chunk_result.dominance:.2f}")
```

### Sentiment Analysis from Acoustic Features

```python
from voice_analytics import AcousticSentimentAnalyzer

# Acoustic-only sentiment analysis (no text required)
sentiment = AcousticSentimentAnalyzer(
    feature_set=["prosody", "spectral", "energy", "rhythm"],
    model="xgboost_sentiment_v2",
    calibration_set="sentiment_calibration_audio/"
)

result = sentiment.analyze("customer_complaint.wav")
print(f"Sentiment: {result.sentiment} ({result.confidence:.2f})")
print(f"  Positive: {result.probabilities['positive']:.2f}")
print(f"  Negative: {result.probabilities['negative']:.2f}")
print(f"  Neutral: {result.probabilities['neutral']:.2f}")

# Sentiment trajectory over time
trajectory = sentiment.analyze_trajectory("long_call.wav", window_ms=3000)
for point in trajectory:
    print(f"  {point.time:.1f}s: {point.sentiment} ({point.score:.2f})")
```

### Speech Rate and Fluency Metrics

```python
from voice_analytics import FluencyAnalyzer

fluency = FluencyAnalyzer(
    sample_rate=16000,
    pause_threshold_db=-30,
    min_pause_duration_ms=200,
    filler_words=["um", "uh", "like", "you know", "so"],
    wpm_calculation="speech_only"  # speech_only | total_including_pauses
)

result = fluency.analyze("agent_speech.wav")
print(f"Speech rate: {result.speech_rate_wpm:.0f} WPM")
print(f"Articulation rate: {result.articulation_rate_wpm:.0f} WPM")
print(f"Pause ratio: {result.pause_ratio:.2%}")
print(f"Mean pause duration: {result.mean_pause_ms:.0f} ms")
print(f"Filler count: {result.filler_count}")
print(f"Filler rate: {result.filler_rate:.2%}")
print(f"Clarity score: {result.clarity_score:.2f}")
print(f"Fluency score: {result.fluency_score:.2f}")
```

### Call Center Dashboard Integration

```python
from voice_analytics import CallCenterDashboard, RealTimeMetrics

# Real-time call center metrics
dashboard = CallCenterDashboard(
    emotion_detector=detector,
    speaker_identifier=identifier,
    quality_assessor=SpeechQualityAssessor(),
    update_interval_s=5
)

# Stream live metrics
metrics = dashboard.get_realtime_metrics()
print(f"Active calls: {metrics.active_calls}")
print(f"Avg sentiment: {metrics.avg_sentiment:.2f}")
print(f"Avg MOS: {metrics.avg_mos:.2f}")
print(f"Escalation count: {metrics.escalation_count}")

# Generate daily report
daily = dashboard.generate_daily_report(date="2024-01-15")
print(f"Total calls: {daily.total_calls}")
print(f"Avg handle time: {daily.avg_handle_time_s:.0f}s")
print(f"Customer satisfaction: {daily.avg_csat:.2f}")
print(f"Agent compliance: {daily.avg_compliance:.2%}")
```

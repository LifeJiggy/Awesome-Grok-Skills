---
name: "speech-recognition"
category: "voice-technology"
version: "1.0.0"
tags: ["voice-technology", "speech-recognition", "asr", "transcription", "streaming", "beam-search"]
---

# Speech Recognition — ASR Pipelines, Decoding & Real-Time Transcription

## Overview

Automatic speech recognition (ASR) is the process of converting spoken language into written text. This module provides a complete ASR pipeline — from audio preprocessing through acoustic model inference, language model integration, and beam search decoding — with first-class support for both batch and streaming recognition. Modern ASR systems have moved from hybrid HMM-DNN architectures to end-to-end models (Conformer, Whisper, wav2vec 2.0) that jointly learn acoustic and linguistic representations, and this module supports both paradigms.

The core challenge in ASR is the tradeoff between accuracy, latency, and compute cost. Batch processing achieves the highest accuracy by allowing unlimited look-ahead and multi-pass decoding, but streaming recognition must deliver partial results with sub-second latency while maintaining acceptable word error rate (WER). This module implements configurable decoding strategies — greedy, beam search, and prefix-constrained — with dynamic beam width adjustment based on real-time factor (RTF) constraints.

Production ASR must handle diverse acoustic conditions, vocabulary, and speaking styles. The module includes domain adaptation hooks for injecting custom vocabularies (medical terms, product names, technical jargon), language model interpolation for domain-specific probability estimation, and code-switching detection for multilingual speakers who mix languages within a single utterance. Confidence scoring at the word and utterance level enables downstream systems to make informed decisions about when to request clarification.

The streaming recognition subsystem uses a look-ahead buffer architecture where partial results are generated from buffered audio chunks while maintaining state across chunk boundaries. This ensures smooth, continuous transcription output without the "stuttering" artifacts common in naive streaming implementations. Endpoint detection identifies natural speech boundaries to segment continuous audio into manageable transcription units.

The module also supports diarization — attributing transcribed segments to individual speakers — which is essential for meeting transcription, call center analytics, and multi-party conversation analysis. Diarization combines speaker embedding clustering with forced alignment to produce speaker-labeled transcription output with accurate turn boundaries.

## Core Capabilities

- **End-to-End ASR**: Conformer, Whisper, and wav2vec 2.0 model loading with automatic preprocessing and tokenization
- **Beam Search Decoding**: Configurable beam width with language model shallow fusion, pruning strategies, and early exit
- **Streaming Recognition**: Real-time partial transcription with look-ahead buffering and dynamic endpointing
- **Language Model Integration**: N-gram and neural LM interpolation for domain adaptation and vocabulary biasing
- **Custom Vocabulary Injection**: Dynamic vocabulary lists with pronunciation hints for proper nouns and domain terms
- **Confidence Scoring**: Per-word and per-utterance confidence with calibration for downstream decision-making
- **Code-Switching Detection**: Automatic language identification and mixed-language transcription
- **Domain Adaptation**: Fine-tuning hooks and adapter layers for specialized vocabulary and acoustic conditions
- **Speaker Diarization**: Multi-speaker segmentation with speaker-attributed transcription output

## Usage Examples

```python
from speech_recognition import ASREngine, DecodingConfig

# Initialize with a Conformer model
engine = ASREngine(
    model="conformer_ctc_large",
    device="cuda",
    language="en",
    beam_size=10
)

# Batch recognition
result = engine.transcribe("meeting_recording.wav")
print(f"Text: {result.text}")
print(f"WER: {result.word_error_rate:.2%}")
for word in result.words:
    print(f"  {word.start:.2f}s-{word.end:.2f}s: {word.text} (conf: {word.confidence:.2f})")
```

```python
from speech_recognition import StreamingASR, EndpointDetector

# Streaming recognition with VAD-based endpointing
streamer = StreamingASR(
    model="conformer_transducer_streaming",
    device="cuda",
    chunk_size_ms=400,
    lookahead_context_ms=600,
    blank_penalty=1.0
)

endpoint_detector = EndpointDetector(
    min_silence_duration_ms=800,
    max_speech_duration_ms=30000,
    speech_threshold=0.5
)

# Process audio stream
for partial_result in streamer.recognize_stream(audio_stream):
    if partial_result.is_final:
        print(f"Final: {partial_result.text}")
        endpoint_detector.reset()
    else:
        print(f"Partial: {partial_result.text}", end="\r")

    if endpoint_detector.is_endpoint(partial_result):
        streamer.reset_state()
```

```python
from speech_recognition import VocabularyInjector, LanguageModelAdapter

# Inject custom vocabulary for domain-specific recognition
vocabulary = VocabularyInjector()
vocabulary.add("metformin", pronunciations=["MET-for-min"])
vocabulary.add("atorvastatin", pronunciations=["ah-TOR-vah-STAT-in"])
vocabulary.add("COVID-19", pronunciations=["koh-vid nine-teen"])

# Adapt language model for medical domain
lm_adapter = LanguageModelAdapter(base_lm_weight=0.3, vocabulary_boost=2.0)
adapted_lm = lm_adapter.interpolate(
    base_model="kenlm_wikipedia",
    domain_model="kenlm_medical",
    domain_weight=0.7
)

engine = ASREngine(model="conformer_ctc_large")
engine.set_vocabulary(vocabulary)
engine.set_language_model(adapted_lm)
result = engine.transcribe("patient_audio.wav")
```

```python
from speech_recognition import CodeSwitchingDetector, MultiLanguageASR

# Detect and transcribe code-switched speech
cs_detector = CodeSwitchingDetector(
    supported_languages=["en", "zh", "es", "fr", "hi"],
    detection_window_ms=2000,
    confidence_threshold=0.6
)

multi_asr = MultiLanguageASR(
    models={"en": "conformer_en", "zh": "conformer_zh", "es": "conformer_es"},
    detector=cs_detector
)

result = multi_asr.transcribe("code_switched_audio.wav")
for segment in result.segments:
    print(f"[{segment.language}] {segment.text} (conf: {segment.confidence:.2f})")
```

```python
from speech_recognition import ASRBenchmark, ConfidenceCalibrator

# Benchmark model performance
benchmark = ASRBenchmark()
metrics = benchmark.evaluate(
    model="conformer_ctc_large",
    test_set="librispeech_test_clean",
    metrics=["wer", "cer", "rtf", "latency_p50", "latency_p99"]
)
print(f"WER: {metrics.wer:.2%} | RTF: {metrics.rtf:.3f}")

# Calibrate confidence scores
calibrator = ConfidenceCalibrator()
calibrator.fit(
    model=engine,
    calibration_set="calibration_audio/",
    method="temperature_scaling"
)
engine.set_confidence_calibrator(calibrator)
```

```python
from speech_recognition import SpeakerDiarizer, DiarizationPipeline

# Speaker diarization with transcription
diarizer = SpeakerDiarizer(
    embedding_model="ecapa_tdnn_v2",
    clustering_method="agglomerative",
    max_speakers=6,
    device="cuda"
)

pipeline = DiarizationPipeline(
    asr_engine=engine,
    diarizer=diarizer
)

# Produce speaker-attributed transcription
result = pipeline.process("team_meeting.wav")
for segment in result.segments:
    print(f"[{segment.start:.1f}s-{segment.end:.1f}s] "
          f"Speaker {segment.speaker_id}: {segment.text}")
```

```python
from speech_recognition import AudioPreprocessor, NoiseRobustASR

# Robust recognition in noisy environments
preprocessor = AudioPreprocessor(
    target_sample_rate=16000,
    noise_reduction=True,
    dereverberation=True,
    normalization="peak",
    trim_silence=True
)

robust_asr = NoiseRobustASR(
    model="conformer_ctc_large",
    preprocessor=preprocessor,
    confidence_threshold=0.5,
    fallback_to_lower_beam=True
)

result = robust_asr.transcribe("noisy_meeting_room.wav")
for seg in result.segments:
    marker = " " if seg.confidence >= 0.5 else " [LOW-CONF]"
    print(f"  {seg.text}{marker}")
```

## Best Practices

1. **Match sample rate to model expectations**: Most streaming ASR models are trained on 16 kHz mono audio. Feeding 44.1 kHz or 48 kHz audio without resampling degrades WER by 5-15%. Always resample in the preprocessing stage using high-quality resampling (soxr or resampy).

2. **Use language model fusion judiciously**: Shallow fusion with a strong language model improves WER but can override acoustic evidence on uncommon phrases. For medical/legal domains, reduce LM weight to 0.2-0.3 to avoid suppressing domain terminology that appears rarely in general text corpora.

3. **Tune beam width to latency constraints**: Beam size 1-3 is suitable for real-time streaming (RTF < 0.1). Beam size 10-20 is appropriate for batch processing where accuracy matters more than speed. Beyond beam 20, marginal WER improvement is negligible (typically <0.5% absolute).

4. **Implement proper endpointing**: False endpoint detection (cutting off speech too early) is more damaging than late detection. Set minimum silence duration to 600-1000ms for conversational speech, 200-400ms for dictation. Use energy-based endpointing with a neural VAD override for best results.

5. **Calibrate confidence scores**: Raw neural network outputs are not well-calibrated probabilities. Apply temperature scaling or Platt scaling on a held-out calibration set to produce meaningful confidence values for downstream decisions. Uncalibrated confidences lead to poor thresholding.

6. **Use custom vocabulary injection over fine-tuning for new terms**: Adding vocabulary entries with pronunciation hints achieves 90% of the WER improvement of full fine-tuning at 1% of the compute cost. Reserve fine-tuning for sustained domain adaptation where vocabulary injection is insufficient.

7. **Monitor real-time factor continuously**: RTF > 1.0 means the system cannot keep up with live audio. Set alerts at RTF 0.8 to catch degradation before it impacts users. RTF spikes often indicate GPU memory pressure, model loading contention, or input sample rate mismatches.

8. **Segment long audio before recognition**: ASR models have effective context windows (typically 30-60 seconds). Processing longer audio without segmentation degrades accuracy. Split at silence boundaries or fixed intervals with 200ms overlap to preserve word boundaries.

## Architecture Notes

The ASR pipeline follows a standard three-stage architecture: feature extraction -> acoustic model -> decoder. Feature extraction converts raw audio to mel spectrograms or Fbanks. The acoustic model (Conformer, Whisper, etc.) produces token-level probabilities. The decoder (greedy, beam search, or transducer) converts probabilities to text. Language model fusion happens during decoding, not at the acoustic model stage.

For streaming recognition, the transducer architecture (RNN-T or Transducer) is preferred over CTC because it models dependencies between output tokens, producing more coherent partial results. The streaming pipeline maintains a state buffer across chunks to ensure seamless continuity.

The diarization subsystem operates independently of the ASR pipeline. Speaker embeddings are extracted at regular intervals (typically every 0.5-1.0 seconds), then clustered to identify distinct speakers. The resulting speaker segments are aligned with ASR output to produce speaker-attributed transcription. Overlap handling uses dual-channel processing when available, or probabilistic assignment based on spectral features when operating on mono audio.

For production deployments, consider a multi-pass decoding strategy where a fast first pass generates a rough transcript, and a second pass with a larger beam and stronger language model refines the output. This two-pass approach reduces average latency while maintaining high accuracy for challenging utterances.

## Related Modules

- [speech-processing](../speech-processing/) — Audio preprocessing, VAD, and normalization before ASR
- [voice-assistants](../voice-assistants/) — Intent recognition downstream of ASR transcripts
- [voice-analytics](../voice-analytics/) — Speaker identification and emotion from transcribed audio
- [text-to-speech](../text-to-speech/) — Round-trip evaluation and synthesis for speech-to-speech systems

---

## Advanced Configuration

### Custom Decoding Configuration

```python
from speech_recognition import DecodingConfig

config = DecodingConfig(
    beam_size=12,
    lm_weight=0.3,
    vocabulary_weight=2.0,
    max_active_tokens=100,
    pruning_threshold=0.001,
    blank_penalty=1.0,
    length_penalty=0.6,
    early_exit=True,
    early_exit_threshold=0.95,
)
```

### Domain Adaptation Configuration

```python
from speech_recognition import DomainAdapter

adapter = DomainAdapter(
    domain="medical",
    vocabulary_boost=3.0,
    lm_interpolation_weight=0.5,
    fine_tune_layers=["encoder.layer.10", "encoder.layer.11", "decoder"],
    learning_rate=1e-5,
)
```

## Architecture Patterns

### ASR Pipeline Architecture

```
Audio Input
    │
    ▼
┌──────────────┐
│ Preprocessing│── Resample, normalize, VAD
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Feature      │── Mel spectrogram / Fbanks
│ Extraction   │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Acoustic     │── Conformer / Whisper / wav2vec 2.0
│ Model        │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Decoder      │── Beam search / Transducer
│              │── + Language model fusion
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Output       │── Text, timestamps, confidence
└──────────────┘
```

### Streaming Architecture

```
Audio Stream
    │
    ▼
┌──────────────┐
│ Chunk Buffer │── 400ms chunks with 600ms lookahead
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Streaming    │── Maintains state across chunks
│ Encoder      │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Partial      │── Real-time text output
│ Decoder      │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Endpoint     │── Detects speech boundaries
│ Detector     │
└──────────────┘
```

## Integration Guide

### LiveKit Integration

```python
from speech_recognition import LiveKitASR

asr = LiveKitASR(
    model="conformer_transducer_streaming",
    room_service=livekit_room,
)
asr.start()
```

### WebSocket Server

```python
from speech_recognition import WebSocketASRServer

server = WebSocketASRServer(
    model="conformer_ctc_large",
    port=8765,
    max_connections=100,
)
server.start()
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Dynamic beam width | 30% faster on easy utterances |
| KV-cache reuse | 50% less recomputation |
| Quantized inference | 2x throughput on CPU |
| Batch dynamic batching | 3x GPU utilization |
| Endpoint detection tuning | 40% fewer false endpoints |

## Security Considerations

- **Audio stream encryption**: TLS for all audio transmission
- **Transcription access control**: JWT-based API authentication
- **Data isolation**: Per-tenant audio processing
- **PII redaction**: Auto-redact sensitive terms from transcripts
- **Audit logging**: Track all transcription requests

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| High WER on domain terms | Missing vocabulary | Add domain vocabulary entries |
| Streaming stutters | Chunk size too small | Increase chunk to 400ms |
| RTF > 1.0 | GPU memory pressure | Reduce beam size or batch size |
| False endpoints | Silence threshold too low | Increase min_silence to 800ms |
| Language model suppresses terms | LM weight too high | Reduce lm_weight to 0.2 |

## API Reference

### ASREngine

```python
class ASREngine:
    def __init__(self, model: str, device: str, language: str, beam_size: int)
    def transcribe(self, audio_path: str) -> TranscriptionResult
    def set_vocabulary(self, vocabulary: VocabularyInjector) -> None
    def set_language_model(self, lm: LanguageModelAdapter) -> None
```

### StreamingASR

```python
class StreamingASR:
    def __init__(self, model: str, device: str, chunk_size_ms: int, lookahead_context_ms: int)
    def recognize_stream(self, audio_stream) -> Iterator[PartialResult]
    def reset_state(self) -> None
```

## Data Models

```python
from dataclasses import dataclass

@dataclass
class TranscriptionResult:
    text: str
    words: list[Word]
    segments: list[Segment]
    word_error_rate: float
    language: str

@dataclass
class Word:
    text: str
    start: float
    end: float
    confidence: float

@dataclass
class PartialResult:
    text: str
    is_final: bool
    confidence: float
```

## Deployment Guide

### Installation

```bash
pip install speech-recognition
# With GPU
pip install speech-recognition[gpu]
```

### Model Download

```python
from speech_recognition import ModelManager

manager = ModelManager()
manager.download("conformer_ctc_large")
manager.download("conformer_transducer_streaming")
```

## Monitoring & Observability

```python
from speech_recognition import MetricsCollector

collector = MetricsCollector()
collector.histogram("asr.wer", wer, tags={"model": model})
collector.histogram("asr.rtf", rtf, tags={"model": model})
collector.histogram("asr.latency_p99_ms", latency)
collector.counter("asr.transcriptions.total", count, tags={"status": status})
```

## Testing Strategy

```python
import pytest
from speech_recognition import ASREngine

def test_batch_transcription():
    engine = ASREngine(model="conformer_ctc_large", device="cpu", language="en", beam_size=10)
    result = engine.transcribe("test_audio.wav")
    assert result.text is not None
    assert len(result.words) > 0
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added streaming support | Use StreamingASR for real-time |
| 2.0.0 | New model architecture | Re-download models |

## Glossary

| Term | Definition |
|------|-----------|
| **WER** | Word Error Rate — accuracy metric |
| **RTF** | Real-Time Factor — processing speed ratio |
| **Beam Search** | Decoding algorithm exploring top-k paths |
| **Endpointing** | Detecting speech boundaries in streaming |
| **Language Model Fusion** | Combining acoustic and language model scores |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with Conformer and Whisper support
- Beam search decoding with LM fusion
- Streaming recognition with endpointing
- Speaker diarization integration

## Contributing Guidelines

```bash
git clone https://github.com/example/speech-recognition.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### ASR Model Comparison

| Model | Architecture | WER (LibriSpeech) | Speed | Streaming |
|-------|-------------|-------------------|-------|-----------|
| Whisper Large-v3 | Encoder-Decoder | 2.0% | Slow | No |
| Conformer CTC | Conformer+CTC | 2.5% | Fast | Yes |
| Conformer Transducer | Conformer+RNN-T | 2.8% | Fast | Yes |
| wav2vec 2.0 | Transformer | 3.0% | Medium | Yes |
| DeepSpeech 2 | BiLSTM | 5.0% | Fast | Yes |

### Beam Search Parameters

| Beam Size | WER Impact | Speed Impact | Use Case |
|-----------|-----------|--------------|----------|
| 1 (greedy) | +1-2% WER | Fastest | Real-time, low-latency |
| 3-5 | Baseline | Fast | General streaming |
| 10-20 | -0.5% WER | Medium | Batch processing |
| 50+ | -0.5-1% WER | Slow | Offline, highest accuracy |

### Language Model Fusion Reference

| LM Weight | Effect | Use Case |
|-----------|--------|----------|
| 0.0 | Acoustic only | Noisy audio, domain terms |
| 0.1-0.2 | Light fusion | Domain-specific vocabulary |
| 0.3-0.5 | Standard fusion | General purpose |
| 0.6-0.8 | Heavy fusion | Clean audio, standard vocabulary |
| 1.0 | LM dominant | Not recommended |

### Custom Vocabulary Format

```json
{
  "vocabulary": [
    {"word": "metformin", "pronunciation": "MET-for-min", "boost": 2.0},
    {"word": "atorvastatin", "pronunciation": "ah-TOR-vah-STAT-in", "boost": 2.0},
    {"word": "COVID-19", "pronunciation": "koh-vid nine-teen", "boost": 3.0},
    {"word": "Dr. Smith", "pronunciation": "doctor smith", "boost": 1.5}
  ],
  "language_model_interpolation": {
    "base_weight": 0.3,
    "domain_weight": 0.7,
    "domain_model": "medical_lm"
  }
}
```

### Streaming Configuration Reference

| Parameter | Dictation | Conversation | Broadcast |
|-----------|-----------|-------------|-----------|
| chunk_size_ms | 200-400 | 400-600 | 100-200 |
| lookahead_ms | 400-600 | 600-1000 | 200-400 |
| min_silence_ms | 800-1200 | 400-800 | 300-600 |
| max_speech_ms | 30000 | 15000 | 30000 |
| beam_size | 10-20 | 5-10 | 10-15 |

### WER Analysis Reference

| WER Range | Quality | Use Case |
|-----------|---------|----------|
| 0-3% | Excellent | Broadcast transcription |
| 3-5% | Very good | Meeting transcription |
| 5-10% | Good | General purpose |
| 10-20% | Fair | Noisy environments |
| 20%+ | Poor | Needs domain adaptation |

### Confidence Calibration Methods

| Method | Description | Accuracy | Speed |
|--------|-------------|----------|-------|
| Temperature scaling | Single parameter | Good | Fast |
| Platt scaling | Logistic regression | Very good | Medium |
| Isotonic regression | Non-parametric | Best | Slow |
| Histogram binning | Bucket-based | Good | Fast |

### Common ASR Issues and Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| High WER on domain terms | Words not recognized | Add vocabulary entries |
| False endpoints | Speech cut short | Increase min_silence_ms |
| Hallucination | Text not in audio | Reduce LM weight |
| Repetition | Words repeated | Check decoder configuration |
| Language switching errors | Wrong language detected | Use code-switching detector |
| Number reading errors | Numbers wrong | Add number normalization |
| Punctuation errors | Missing/wrong punctuation | Add punctuation model |

### ASR Benchmark Reference

| Benchmark | Test Set | Best WER | Description |
|-----------|----------|----------|-------------|
| LibriSpeech clean | test-clean | 2.0% | Clean read speech |
| LibriSpeech other | test-other | 4.5% | Noisy read speech |
| CommonVoice | en | 5.0% | Crowdsourced |
| WSJ | eval92 | 3.0% | Wall Street Journal |
| TED-LIUM | test | 4.0% | TED talks |

## Error Correction & Post-Processing

### Text Post-Processing Pipeline

```python
from speech_recognition import TextPostProcessor

post_processor = TextPostProcessor()

# Apply automatic corrections
corrected = post_processor.process(
    text="the patient takes metformin 500 mg twice daily for diabetis",
    rules=[
        {"pattern": r"\bdiabetis\b", "replacement": "diabetes"},
        {"pattern": r"\b(\d+)\s*mg\b", "replacement": r"\1 milligrams"},
        {"pattern": r"\btwice daily\b", "replacement": "two times daily"},
    ],
    capitalization=True,
    punctuation_repair=True,
    number_normalization=True
)
print(corrected)
# "The patient takes metformin 500 milligrams two times daily for diabetes."
```

### WER Calculation & Analysis

```python
from speech_recognition import WERCalculator, AlignmentAnalyzer

# Calculate WER with detailed alignment
calculator = WERCalculator()
result = calculator.compute(
    reference="the cat sat on the mat",
    hypothesis="the cat is on the mat"
)

print(f"WER: {result.wer:.2%}")
print(f"Insertions: {result.insertions}")
print(f"Deletions: {result.deletions}")
print(f"Substitutions: {result.substitutions}")
print(f"Accuracy: {result.accuracy:.2%}")

# Visual alignment
alignment = AlignmentAnalyzer.align(result)
for pair in alignment:
    if pair.status == "correct":
        print(f"  ✓ {pair.ref}")
    elif pair.status == "substitution":
        print(f"  ✗ {pair.ref} → {pair.hyp}")
    elif pair.status == "deletion":
        print(f"  - {pair.ref} (deleted)")
    elif pair.status == "insertion":
        print(f"  + {pair.hyp} (inserted)")
```

### Pronunciation Dictionary Management

```python
from speech_recognition import PronunciationDictionary, PronunciationEntry

# Build a pronunciation dictionary
pron_dict = PronunciationDictionary(language="en-US")

# Add entries with ARPAbet phonemes
pron_dict.add(PronunciationEntry(
    word="metformin",
    phonemes=["M", "EH", "T", "F", "AO", "R", "M", "IH", "N"],
    frequency=0.8
))

pron_dict.add(PronunciationEntry(
    word="atorvastatin",
    phonemes=["AH", "T", "AO", "R", "V", "AH", "S", "T", "AH", "T", "IH", "N"],
    frequency=0.9
))

# Load from CMU dict file
pron_dict.load_cmu("cmudict-0.7b.txt")

# Query pronunciation
entry = pron_dict.lookup("metformin")
print(f"Phonemes: {' '.join(entry.phonemes)}")
```

### Real-Time Decoding Strategies

```python
from speech_recognition import StreamingDecoder, DecodingState

# Configure streaming decoder with multiple strategies
decoder = StreamingDecoder(
    strategy="beam_search",   # greedy | beam_search | prefix_constrained
    beam_size=8,
    lm_weight=0.3,
    state_maintenance=True,
    max_active_paths=50
)

# Process audio chunks and get partial results
state = decoder.new_state()
for chunk in audio_chunks:
    state = decoder.decode_chunk(chunk, state)
    if state.has_partial:
        print(f"Partial: {state.partial_text}")

final = decoder.finalize(state)
print(f"Final: {final.text}")
```

### Language Identification

```python
from speech_recognition import LanguageIdentifier

# Identify language from audio
identifier = LanguageIdentifier(
    model="wav2vec2_lid_v2",
    supported_languages=["en", "zh", "es", "fr", "de", "ja", "ko", "ar", "hi"],
    confidence_threshold=0.5,
    device="cuda"
)

result = identifier.identify("multilingual_audio.wav")
print(f"Detected: {result.language} ({result.confidence:.2f})")
print("All candidates:", result.candidates)
# {'zh': 0.92, 'en': 0.05, 'ja': 0.02, ...}
```

### Audio Augmentation for Robust ASR

```python
from speech_recognition import AudioAugmenter

augmenter = AudioAugmenter(
    sample_rate=16000,
    augmentations=[
        {"type": "add_noise", "snr_range": [5, 20]},
        {"type": "speed_perturb", "rates": [0.9, 1.0, 1.1]},
        {"type": "room_impulse", "rir_database": "mit_ir"},
        {"type": "time_stretch", "range": [0.8, 1.2]},
        {"type": "pitch_shift", "semitones": [-2, 2]},
    ],
    probability=0.5
)

# Augment audio for training data
augmented_samples = augmenter.augment(clean_audio, n_augmentations=5)
for i, aug in enumerate(augmented_samples):
    print(f"Augmentation {i}: SNR={aug.snr_db:.1f}dB, speed={aug.speed_factor:.2f}")
```

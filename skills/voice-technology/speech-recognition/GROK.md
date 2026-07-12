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

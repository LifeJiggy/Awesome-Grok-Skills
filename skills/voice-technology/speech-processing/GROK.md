---
name: "speech-processing"
category: "voice-technology"
version: "1.0.0"
tags: ["voice-technology", "speech-processing", "audio", "signal-processing", "vad", "diarization"]
---

# Speech Processing — Audio Preprocessing, Feature Extraction & Enhancement

## Overview

Speech processing is the foundational layer of any voice technology stack. Before audio can be recognized, synthesized, or analyzed, it must be cleaned, normalized, and converted into meaningful feature representations. This module provides a comprehensive toolkit for raw audio preprocessing — including noise reduction via spectral gating, automatic gain normalization, voice activity detection (VAD), and silence removal — along with feature extraction pipelines that produce the MFCCs, spectrograms, and pitch contours consumed by downstream ASR and speaker ID systems.

Modern speech processing extends well beyond simple filtering. Contemporary systems must handle far-field microphone arrays, multi-speaker overlap, background music contamination, and heterogeneous audio formats sampled anywhere from 8 kHz (telephony) to 48 kHz (broadcast). The algorithms in this module are designed to operate robustly across these conditions, leveraging both classical DSP techniques (Wiener filtering, adaptive noise estimation) and modern neural-enhanced approaches (DNN-based dereverberation, perceptual loss functions).

Additionally, this module covers speaker diarization — the process of determining "who spoke when" — which is essential for meeting transcription, call center analytics, and multi-party conversational AI. Audio quality metrics such as PESQ, STOI, and SNR estimation provide objective feedback on processing effectiveness, enabling automated pipeline tuning and quality gating before downstream consumption.

The processing pipeline is designed to be modular: each stage (noise reduction, normalization, feature extraction) operates independently and can be composed into custom workflows. State is maintained through dataclass containers that carry audio signals, metadata, and quality metrics through the pipeline without requiring external storage.

## Core Capabilities

- **Noise Reduction**: Spectral gating, Wiener filtering, and adaptive noise estimation for cleaning contaminated audio signals
- **Voice Activity Detection (VAD)**: Energy-based, zero-crossing, and ML-based VAD with configurable hangover and minimum duration thresholds
- **Audio Normalization**: Peak normalization, loudness normalization (EBU R128 / ITU-R BS.1770), dynamic range compression, and automatic gain control
- **Feature Extraction**: MFCC, mel-spectrogram, chromagram, pitch tracking (YIN/PYIN), and formant estimation
- **Speaker Diarization**: Clustering-based and neural embedding-based approaches for multi-speaker segmentation
- **Audio Format Conversion**: Sample rate adaptation, bit depth conversion, channel downmixing, and codec transcoding
- **Silence Detection & Removal**: Threshold-based and VAD-driven silence trimming with configurable padding
- **Quality Metrics**: PESQ, SNR estimation, spectral distortion, and intelligibility scoring

## Usage Examples

```python
from speech_processing import AudioPreprocessor, FeatureExtractor

# Load and clean audio
preprocessor = AudioPreprocessor(sample_rate=16000)
cleaned = preprocessor.load_and_clean("noisy_recording.wav")

# Apply noise reduction
denoised = preprocessor.reduce_noise(
    cleaned,
    noise_profile_start=0.0,
    noise_profile_end=0.5,
    reduction_db=12.0
)

# Normalize loudness
normalized = preprocessor.normalize_loudness(
    denoised,
    target_lufs=-23.0,
    true_peak_dbtp=-1.0
)

# Extract MFCCs
extractor = FeatureExtractor(sample_rate=16000, n_mfcc=13)
mfccs = extractor.compute_mfcc(
    normalized,
    n_fft=512,
    hop_length=160,
    win_length=400,
    lifter=22
)

# Compute mel spectrogram
mel_spec = extractor.compute_mel_spectrogram(
    normalized,
    n_mels=80,
    fmin=0,
    fmax=8000
)
```

```python
from speech_processing import VoiceActivityDetector, SilenceTrimmer

# Configure VAD
vad = VoiceActivityDetector(
    sample_rate=16000,
    frame_duration_ms=30,
    energy_threshold_db=-35.0,
    min_speech_duration_ms=250,
    min_silence_duration_ms=100,
    hangover_frames=8
)

# Detect speech segments
segments = vad.detect(audio_signal)
for seg in segments:
    print(f"Speech: {seg.start:.2f}s - {seg.end:.2f}s ({seg.duration:.2f}s)")

# Remove silence
trimmer = SilenceTrimmer(vad, padding_ms=200)
trimmed_audio, timestamps = trimmer.trim(audio_signal)
```

```python
from speech_processing import SpeakerDiarizer

# Diarize a meeting recording
diarizer = SpeakerDiarizer(
    num_speakers=None,  # auto-detect
    min_speakers=2,
    max_speakers=10,
    embedding_model="ecapa-tdnn",
    clustering_method="agglomerative"
)

diarization = diarizer.diarize("meeting.wav")
for turn in diarization:
    print(f"Speaker {turn.speaker_id}: {turn.start:.2f}s - {turn.end:.2f}s")
```

```python
from speech_processing import AudioQualityMetrics

metrics = AudioQualityMetrics(sample_rate=16000)
pesq_score = metrics.pesq(clean, processed, mode="wb")
snr = metrics.estimate_snr(processed)
stoi_score = metrics.stoi(clean, processed)
print(f"PESQ: {pesq_score:.2f} | SNR: {snr:.1f}dB | STOI: {stoi_score:.3f}")
```

```python
from speech_processing import AudioFormatConverter

converter = AudioFormatConverter()

# Resample from 44.1kHz to 16kHz for ASR
resampled = converter.resample(signal, target_sr=16000)

# Downmix stereo to mono
mono = converter.downmix_to_mono(stereo_signal)

# Trim silence with 200ms padding
trimmed, segments = converter.trim_silence(signal, vad, padding_ms=200)
```

## Best Practices

1. **Always resample to 16 kHz for ASR**: Most ASR models expect 16 kHz mono audio. Resample early in the pipeline to avoid inconsistent feature extraction across different input sources. Use resampy or soxr for high-quality resampling rather than simple interpolation.

2. **Use energy-based VAD as a first pass**: ML-based VAD is more accurate but slower. Use energy-based detection for coarse segmentation, then refine with neural models only when needed. A two-stage approach reduces compute costs by 60-80% in streaming applications.

3. **Profile noise from silence, not speech**: When applying spectral gating noise reduction, ensure the noise profile window contains only background noise, not speech onset or offset. Misidentified noise profiles cause "musical noise" artifacts that degrade ASR performance.

4. **Preserve original audio alongside processed versions**: Always keep the raw input available for reprocessing. Pipeline parameters may need tuning, and re-extraction from compressed intermediates compounds quality loss exponentially.

5. **Apply VAD hangover frames**: Speech segments often end with unvoiced consonants (fricatives, plosives) that fall below energy thresholds. A hangover of 5-10 frames prevents premature truncation that causes word-boundary errors in ASR.

6. **Use per-utterance normalization for ASR**: Global loudness normalization assumes stationary signal statistics. For variable-length utterances, compute normalization parameters per-segment to avoid quiet speech being amplified into the noise floor.

7. **Cache expensive feature computations**: MFCC and spectrogram extraction are CPU-bound. Cache results keyed by file hash and extraction parameters to avoid redundant computation in interactive pipelines. An LRU cache of 100 entries typically covers most workloads.

8. **Validate audio integrity before processing**: Check for NaN samples, clipping, DC offset, and format mismatches before running any DSP algorithms. Corrupted input silently produces garbage output that propagates through the entire pipeline.

## Architecture Notes

The module follows a signal-flow architecture where `AudioSignal` dataclasses carry audio data and metadata through processing stages. Each processor is stateless (except for cached noise profiles) and returns new `AudioSignal` instances rather than modifying inputs in place. This enables parallel processing and safe pipeline composition.

For production deployments, consider wrapping the processing pipeline in a streaming adapter that processes audio in fixed-size chunks (250-500ms) rather than loading entire files. This reduces memory usage and enables real-time processing for interactive applications.

## Integration Patterns

### Pipeline Composition

```python
from speech_processing import (
    AudioPreprocessor, VoiceActivityDetector, FeatureExtractor,
    SpeakerDiarizer, AudioQualityMetrics, AudioFormatConverter
)

# Compose a full preprocessing pipeline
preprocessor = AudioPreprocessor(sample_rate=16000)
vad = VoiceActivityDetector(sample_rate=16000)
extractor = FeatureExtractor(sample_rate=16000)
diarizer = SpeakerDiarizer(min_speakers=1, max_speakers=5)
quality = AudioQualityMetrics(sample_rate=16000)
converter = AudioFormatConverter()

# Pipeline execution
signal = preprocessor.load_and_clean("input.wav")
signal = converter.resample(signal, target_sr=16000)
signal = signal.to_mono()
denoised = preprocessor.reduce_noise(signal, reduction_db=10.0)
normalized = preprocessor.normalize_loudness(denoised, target_lufs=-23.0)
metrics = quality.check_integrity(normalized)
mfccs = extractor.compute_mfcc(normalized)
diarization = diarizer.diarize(normalized)
segments = vad.detect(normalized)
```

### Streaming Processing Pattern

```python
# Process audio in fixed-size chunks for real-time applications
CHUNK_SIZE_MS = 250
SAMPLE_RATE = 16000
chunk_samples = int(SAMPLE_RATE * CHUNK_SIZE_MS / 1000)

def process_stream(audio_stream):
    preprocessor = AudioPreprocessor(sample_rate=SAMPLE_RATE)
    vad = VoiceActivityDetector(sample_rate=SAMPLE_RATE)

    for chunk in audio_stream:
        signal = AudioSignal(samples=chunk, sample_rate=SAMPLE_RATE)
        cleaned = preprocessor.reduce_noise(signal, reduction_db=8.0)
        segments = vad.detect(cleaned)
        yield cleaned, segments
```

## Performance Considerations

- **Memory usage**: Loading a 10-minute audio file at 16kHz mono requires ~19MB of RAM. For longer files, use streaming processing or memory-mapped arrays.
- **CPU bottleneck**: MFCC extraction on a 10-second clip takes ~50ms on a modern CPU. For real-time processing at 250ms chunks, this is well within budget.
- **GPU acceleration**: Neural VAD and diarization models benefit significantly from GPU inference. Batch processing on GPU can achieve 50-100x speedup over CPU.
- **Caching strategy**: Feature extraction results are deterministic for the same input and parameters. Use content-addressable caching (keyed by audio hash + parameters) to avoid redundant computation.
- **Parallel processing**: The modular architecture enables parallel execution of independent pipeline stages. Use Python multiprocessing for CPU-bound stages (noise reduction, feature extraction).

## Error Handling

The module raises specific exceptions for different failure modes:

- `AudioProcessingError`: General processing failure (corrupted audio, unsupported format)
- `InvalidAudioError`: Audio input is empty, all zeros, or contains NaN values
- `ModelNotLoadedError`: Required ML model (neural VAD, diarization) not loaded
- `VADConfigError`: Invalid VAD configuration parameters

Always wrap pipeline calls in try-except blocks and log errors for debugging:

```python
from speech_processing import AudioProcessingError, InvalidAudioError

try:
    signal = preprocessor.load_and_clean("input.wav")
    denoised = preprocessor.reduce_noise(signal)
except InvalidAudioError as e:
    logger.error("Audio validation failed: %s", e)
    # Skip this file or request re-recording
except AudioProcessingError as e:
    logger.error("Processing failed: %s", e)
    # Fall back to unprocessed audio
```

## Configuration Reference

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| `sample_rate` | 16000 | 8000-48000 | Target sample rate in Hz |
| `reduction_db` | 12.0 | 0-30 | Noise reduction strength in dB |
| `target_lufs` | -23.0 | -30 to -10 | Target loudness (EBU R128) |
| `true_peak_dbtp` | -1.0 | -3 to 0 | Maximum true peak level |
| `energy_threshold_db` | -35.0 | -50 to -20 | VAD energy threshold |
| `hangover_frames` | 8 | 0-20 | VAD hangover to prevent truncation |
| `n_mfcc` | 13 | 1-20 | Number of MFCC coefficients |
| `n_mels` | 80 | 20-128 | Number of mel filterbank channels |
| `n_fft` | 512 | 256-2048 | FFT window size |
| `hop_length` | 160 | 80-320 | Hop length between frames |

## Related Modules

- [voice-assistants](../voice-assistants/) — Intent recognition and dialogue management built on extracted features
- [speech-recognition](../speech-recognition/) — ASR pipelines that consume MFCCs and spectrograms
- [text-to-speech](../text-to-speech/) — Synthesis output that feeds back into quality assessment
- [voice-analytics](../voice-analytics/) — Emotion detection and biometric analysis from processed audio

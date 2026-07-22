---
name: "text-to-speech"
category: "voice-technology"
version: "1.0.0"
tags: ["voice-technology", "text-to-speech", "tts", "neural-synthesis", "prosody", "voice-cloning"]
---

# Text-to-Speech — Neural Synthesis, Prosody Control & Voice Cloning

## Overview

Text-to-speech (TTS) has undergone a paradigm shift with neural end-to-end architectures that produce near-human quality output. This module provides a production-grade TTS pipeline encompassing text normalization (expanding abbreviations, numbers, dates), phoneme-level pronunciation control, prosody modeling, multi-speaker voice cloning, and real-time streaming synthesis. The architecture supports both single-shot batch synthesis for pre-recorded content and low-latency streaming for interactive applications like voice assistants and real-time translation.

Neural TTS models have fundamentally different optimization profiles than traditional concatenative or parametric systems. This module manages the full model lifecycle — loading, warm-up inference, dynamic batching for throughput, and automatic model switching for multi-language support. For prosody control, the system exposes pitch, rate, volume, and emphasis parameters via both numerical settings and SSML markup, giving content authors fine-grained control over synthesized expression.

Voice cloning has emerged as a critical capability for brand-consistent voice experiences. This module supports few-shot voice cloning (adapt a new voice from 30 seconds of reference audio) and zero-shot voice synthesis (clone from a model trained on the speaker's corpus). The voice cloning pipeline includes speaker embedding extraction, adapter weight generation, and quality validation to ensure the clone maintains fidelity to the reference while avoiding overfitting artifacts.

The streaming TTS subsystem is designed for interactive applications where first-chunk latency is critical. By splitting text into sentence-level segments and generating audio incrementally, the system achieves sub-200ms first-audio latency while maintaining natural prosodic coherence across chunk boundaries.

This module also supports multi-lingual synthesis with automatic language detection and voice selection, making it suitable for global deployments where content arrives in mixed languages. Cross-lingual voice cloning enables a single reference voice to produce output in dozens of languages while maintaining speaker identity.

## Core Capabilities

- **Neural TTS Synthesis**: End-to-end Tacotron/FastSpeech/VITS models with vocoder backends (HiFi-GAN, WaveGlow, WaveRNN)
- **Prosody Control**: Pitch, rate, volume, emphasis, and pause control via parameters and SSML markup
- **SSML Processing**: Full SSML 1.1 support including `<prosody>`, `<break>`, `<emphasis>`, `<say-as>`, `<sub>`, and `<voice>` elements
- **Multi-Speaker Voice Cloning**: Few-shot adaptation from reference audio, zero-shot synthesis from pre-trained speaker encoders
- **Emotional Synthesis**: Emotion-conditioned output (happy, sad, excited, calm, angry) with intensity control
- **Streaming TTS**: Sub-200ms first-chunk latency via autoregressive streaming with look-ahead buffering
- **Pronunciation Dictionaries**: Custom phoneme mappings for domain-specific terms, brand names, and proper nouns
- **Language-Specific Phoneme Mappings**: IPA-based phoneme sets for 30+ languages with automatic grapheme-to-phoneme conversion

## Usage Examples

```python
from text_to_speech import TTSEngine, VoiceProfile

# Initialize with a specific voice
engine = TTSEngine(
    model="vits2_vctk_v1",
    vocoder="hifigan_v1",
    device="cuda",
    sample_rate=22050
)

# Basic synthesis
audio = engine.synthesize(
    text="Welcome to the automated customer support system.",
    voice="p225",
    speed=1.0,
    pitch=1.0
)
engine.save(audio, "welcome.wav")
```

```python
from text_to_speech import SSMLProcessor, TTSEngine

# Process SSML with prosody control
ssml = """
<speak>
    <emphasis level="strong">Important notice:</emphasis>
    Your appointment is at <say-as interpret-as="time">3:30 PM</say-as>.
    <break time="500ms"/>
    <prosody rate="slow" pitch="-10%">Please arrive 15 minutes early.</prosody>
</speak>
"""

processor = SSMLProcessor()
parsed = processor.parse(ssml)

engine = TTSEngine(model="vits2_vctk_v1")
audio = engine.synthesize_ssml(parsed, voice="p225")
```

```python
from text_to_speech import VoiceCloner, TTSEngine

# Clone a voice from 30 seconds of reference audio
cloner = VoiceCloner(
    embedding_model="speaker_encoder_v2",
    cloning_model="vits2_adapter",
    device="cuda"
)

# Generate voice adapter from reference
voice_adapter = cloner.create_adapter(
    reference_audio="reference_speaker.wav",
    adapter_rank=8,
    training_steps=500
)

# Synthesize with cloned voice
engine = TTSEngine(model="vits2_multispeaker_v1")
cloned_audio = engine.synthesize(
    text="This is the cloned voice speaking.",
    voice_adapter=voice_adapter
)
```

```python
from text_to_speech import ProsodyController, EmotionSynthesizer

# Fine-grained prosody control
controller = ProsodyController()
prosody = controller.compute(
    text="I can't believe this is happening right now!",
    emotion="excited",
    emotion_intensity=0.8,
    speech_rate=1.2,
    pitch_range=1.3,
    emphasis_words=["can't", "happening"]
)

engine = TTSEngine(model="vits2_vctk_v1")
audio = engine.synthesize_with_prosody("I can't believe this is happening right now!", prosody)
```

```python
from text_to_speech import StreamingTTS, PronunciationDict

# Real-time streaming for interactive applications
streamer = StreamingTTS(
    engine=TTSEngine(model="faststream_vctk"),
    chunk_size_ms=100,
    look_ahead_chunks=2,
    buffer_overflow_strategy="drop_oldest"
)

# Register pronunciation dictionary
dict_manager = PronunciationDict()
dict_manager.add("OpenAI", "OH-pen-ay-eye")
dict_manager.add("NVIDIA", "en-VID-ee-uh")
dict_manager.add("GPT", "gee-pee-tee")

# Stream audio as it's generated
for audio_chunk in streamer.stream("Let me tell you about OpenAI's latest GPT model."):
    play_audio_chunk(audio_chunk)
```

```python
from text_to_speech import TextNormalizer, MultilingualTTS

# Text normalization for consistent synthesis
normalizer = TextNormalizer()
normalized = normalizer.normalize(
    "On March 15th, 2024 at 3:30 PM, Dr. Smith met with 42 patients. "
    "The cost was $1,234.56."
)
# Result: "On March fifteenth, twenty twenty-four at three thirty P M, "
#         "Doctor Smith met with forty-two patients. "
#         "The cost was twelve hundred thirty-four dollars and fifty-six cents."

# Multi-lingual synthesis with language detection
multi_tts = MultilingualTTS(
    default_model="vits2_multilingual_v3",
    language_models={
        "en": "vits2_en_v1",
        "zh": "vits2_zh_v1",
        "ja": "vits2_ja_v1"
    }
)

audio = multi_tts.synthesize(
    text="This English sentence transitions to 这是中文 sentence back to English.",
    auto_detect_language=True
)
```

```python
from text_to_speech import VoiceQualityAssessor, BatchSynthesizer

# Batch synthesis for large content volumes
batch = BatchSynthesizer(
    engine=TTSEngine(model="vits2_vctk_v1"),
    max_concurrent=8,
    output_format="wav"
)

# Synthesize a batch of sentences
texts = [
    "Order confirmed. Your package will arrive tomorrow.",
    "Payment received. Thank you for your purchase.",
    "Appointment scheduled for Monday at 10 AM."
]
results = batch.synthesize_batch(texts, voice="p225", output_dir="audio_cache/")

# Quality assessment
assessor = VoiceQualityAssessor()
for path in results.output_paths:
    quality = assessor.assess(path)
    print(f"{path}: MOS={quality.mos:.2f}, clarity={quality.clarity:.2f}")
```

## Best Practices

1. **Normalize text before synthesis**: Expand numbers ("42" -> "forty-two"), dates ("03/15" -> "March fifteenth"), abbreviations ("Dr." -> "Doctor"), and symbols ("$" -> "dollars") before feeding text to the neural model. TTS models have inconsistent handling of raw numerals and symbols, and text normalization eliminates this variability.

2. **Use SSML for consistent prosody control**: Direct numerical parameters are fragile across voices. SSML `<prosody>` elements produce more predictable results and are portable across different TTS engines and voices. Define SSML templates for common patterns (announcements, confirmations, error messages).

3. **Warm up the model before serving**: Neural TTS models have significant cold-start latency (JIT compilation, CUDA kernel caching). Pre-synthesize a warm-up sentence before accepting real requests to avoid first-request latency spikes. Budget 2-5 seconds for initial warm-up.

4. **Cache synthesis for repeated phrases**: Greeting messages, error templates, and menu prompts are synthesized identically across sessions. Cache their audio output keyed by text hash and voice parameters. An LRU cache of 200 entries typically covers 90% of repeated phrases in customer service applications.

5. **Validate cloned voice quality**: After voice cloning, always run a quality check comparing the clone's speaker embedding cosine similarity against the reference. Reject adapters below 0.85 similarity to prevent uncanny or identity-confused output. Monitor for overfitting where the clone memorizes reference phrases.

6. **Set streaming chunk sizes based on use case**: Interactive assistants need low latency (50-100ms chunks). Audiobook narration can use larger chunks (200-500ms) for better prosodic coherence. Never use chunks smaller than 20ms — vocoder artifacts dominate below this threshold.

7. **Manage pronunciation dictionaries per domain**: Maintain separate dictionaries for medical, legal, technical, and brand terminology. A single global dictionary becomes unwieldy and creates conflicts when the same word has different pronunciations in different contexts.

8. **Monitor MOS scores for quality regression**: Track Mean Opinion Score on a held-out test set after every model update. Neural TTS quality can degrade subtly — a model that produces higher average MOS may introduce rare but severe artifacts in edge-case text.

## Architecture Notes

The TTS pipeline follows a three-stage architecture: text normalization -> acoustic model -> vocoder. The text normalizer handles linguistic preprocessing (number expansion, abbreviation expansion, SSML parsing). The acoustic model generates mel spectrograms from normalized text. The vocoder converts mel spectrograms to waveform samples. This separation allows independent optimization of each stage.

For production deployments, consider using a model ensemble where different voices are generated by different models optimized for that voice's characteristics. The voice profile system supports this pattern by mapping voice IDs to model configurations.

The streaming architecture splits text into sentence-level segments at punctuation boundaries, then generates mel spectrogram frames incrementally for each segment. A look-ahead buffer of 2-3 segments ensures that prosodic planning extends beyond the current synthesis window, preventing abrupt pitch or pace changes at segment boundaries. The vocoder processes overlapping windows to produce seamless audio output.

Voice cloning adapters are small (<1MB) parameter sets that condition the base TTS model on a target speaker's characteristics. During inference, the adapter modifies a subset of the acoustic model's hidden states, steering output toward the reference voice without modifying the base model weights. This enables fast voice switching at runtime without model reloading.

## Related Modules

- [speech-processing](../speech-processing/) — Post-synthesis audio normalization and quality assessment
- [speech-recognition](../speech-recognition/) — Round-trip evaluation (TTS -> ASR accuracy)
- [voice-assistants](../voice-assistants/) — Response generation that drives TTS output
- [voice-analytics](../voice-analytics/) — Perceptual quality metrics and naturalness scoring

---

## Advanced Configuration

### Voice Cloning Advanced Settings

```python
from text_to_speech import VoiceCloneConfig

config = VoiceCloneConfig(
    adapter_type="low_rank",
    adapter_rank=16,
    training_steps=1000,
    learning_rate=1e-4,
    loss_function="multi_task",
    speaker_similarity_threshold=0.85,
    overfitting_protection=True,
    reference_audio_min_seconds=10,
)
```

### SSML Advanced Processing

```python
from text_to_speech import SSMLConfig

ssml_config = SSMLConfig(
    supported_elements=["prosody", "break", "emphasis", "say-as", "sub", "voice", "lang"],
    default_speech_rate=1.0,
    default_pitch=0,
    default_volume=0,
    break_time_range_ms=(100, 5000),
    emphasis_levels=["reduced", "none", "moderate", "strong"],
)
```

## Architecture Patterns

### TTS Pipeline Architecture

```
Input Text
    │
    ▼
┌──────────────┐
│ Text         │── Number expansion, abbreviation expansion
│ Normalization│
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Grapheme-to- │── Text to phoneme sequence
│ Phoneme      │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Acoustic     │── Phoneme sequence to mel spectrogram
│ Model        │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Vocoder      │── Mel spectrogram to waveform
│ (HiFi-GAN)   │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Post-Process │── Normalization, format conversion
└──────────────┘
```

### Streaming TTS Architecture

```
Text Stream
    │
    ▼
┌──────────────┐
│ Sentence     │── Split at punctuation boundaries
│ Segmenter    │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Look-ahead   │── Buffer 2-3 sentences for prosody planning
│ Buffer       │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Incremental  │── Generate mel frames per segment
│ Synthesis    │
└──────┬───────┘
    │
    ▼
┌──────────────┐
│ Streaming    │── Convert overlapping windows to audio
│ Vocoder      │
└──────────────┘
```

## Integration Guide

### Voice Assistant Integration

```python
from text_to_speech import TTSEngine, StreamingTTS

engine = TTSEngine(model="vits2_vctk_v1")
streamer = StreamingTTS(engine=engine, chunk_size_ms=100)

# Stream response to audio device
for chunk in streamer.stream(response_text):
    audio_device.play(chunk)
```

### Batch Content Generation

```python
from text_to_speech import BatchSynthesizer

batch = BatchSynthesizer(engine=engine, max_concurrent=8)
results = batch.synthesize_batch(
    texts=["Welcome", "Goodbye", "Thank you"],
    voice="p225",
    output_dir="audio_assets/",
)
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| Model warm-up | Eliminates cold-start latency |
| Audio caching | Zero-latency for repeated phrases |
| Dynamic batching | 4x throughput improvement |
| ONNX runtime | 2x faster inference |
| Sentence-level streaming | Sub-200ms first-chunk latency |

## Security Considerations

- **Voice consent**: Only clone voices with explicit permission
- **Deepfake prevention**: Watermark synthesized audio
- **Access control**: API key authentication for TTS endpoints
- **Content filtering**: Block harmful or fraudulent content
- **Audit logging**: Track all synthesis requests and voice usage

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| Robotic output | Insufficient training data | Use more reference audio |
| Prosody breaks at boundaries | No look-ahead buffering | Enable sentence buffering |
| High latency on first request | Model not warmed up | Pre-synthesize warm-up sentence |
| Clone similarity low | Reference audio too short | Use 30+ seconds of clean audio |
| Pronunciation wrong | Missing dictionary entry | Add to pronunciation dictionary |

## API Reference

### TTSEngine

```python
class TTSEngine:
    def __init__(self, model: str, vocoder: str, device: str, sample_rate: int)
    def synthesize(self, text: str, voice: str, speed: float = 1.0, pitch: float = 1.0) -> AudioOutput
    def synthesize_ssml(self, ssml: SSMLDocument, voice: str) -> AudioOutput
    def synthesize_with_prosody(self, text: str, prosody: ProsodyParams) -> AudioOutput
```

### VoiceCloner

```python
class VoiceCloner:
    def __init__(self, embedding_model: str, cloning_model: str, device: str)
    def create_adapter(self, reference_audio: str, adapter_rank: int, training_steps: int) -> VoiceAdapter
    def validate_quality(self, adapter: VoiceAdapter, reference_audio: str) -> QualityScore
```

## Data Models

```python
from dataclasses import dataclass

@dataclass
class AudioOutput:
    samples: ndarray
    sample_rate: int
    duration_s: float
    format: str

@dataclass
class ProsodyParams:
    pitch_range: float
    speech_rate: float
    volume: float
    emphasis_words: list

@dataclass
class VoiceAdapter:
    adapter_id: str
    speaker_embedding: ndarray
    similarity_score: float
    file_size_bytes: int
```

## Deployment Guide

### Installation

```bash
pip install text-to-speech
# With GPU
pip install text-to-speech[gpu]
```

### Model Setup

```python
from text_to_speech import ModelManager

manager = ModelManager()
manager.download("vits2_vctk_v1")
manager.download("hifigan_v1")
manager.warm_up("vits2_vctk_v1", warmup_text="Hello world.")
```

## Monitoring & Observability

```python
from text_to_speech import MetricsCollector

collector = MetricsCollector()
collector.histogram("tts.synthesis.duration_ms", duration)
collector.gauge("tts.mos.score", mos)
collector.counter("tts.requests.total", count, tags={"voice": voice})
collector.histogram("tts.first_chunk_latency_ms", latency)
```

## Testing Strategy

```python
import pytest
from text_to_speech import TTSEngine

def test_synthesis():
    engine = TTSEngine(model="vits2_vctk_v1", vocoder="hifigan_v1", device="cpu", sample_rate=22050)
    audio = engine.synthesize("Hello world.", voice="p225")
    assert audio.duration_s > 0
    assert audio.sample_rate == 22050
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added streaming TTS | Use StreamingTTS class |
| 2.0.0 | New model format | Re-download models |

## Glossary

| Term | Definition |
|------|-----------|
| **VITS** | Variational Inference with adversarial learning for end-to-end TTS |
| **HiFi-GAN** | High-fidelity generative adversarial network vocoder |
| **SSML** | Speech Synthesis Markup Language |
| **MOS** | Mean Opinion Score — perceptual quality metric |
| **Prosody** | Rhythm, stress, and intonation of speech |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with VITS and HiFi-GAN
- SSML processing and prosody control
- Voice cloning from reference audio
- Streaming TTS with sub-200ms latency

## Contributing Guidelines

```bash
git clone https://github.com/example/text-to-speech.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### TTS Model Comparison

| Model | Architecture | Quality | Speed | Streaming |
|-------|-------------|---------|-------|-----------|
| VITS2 | VAE+Flow+GAN | Very high | Fast | Yes |
| Tacotron 2 | Attention | High | Medium | Yes |
| FastSpeech 2 | Non-autoregressive | High | Very fast | Yes |
| Bark | Transformer | Very high | Slow | Yes |
| Tortoise | Transformer+VQ | Highest | Very slow | No |

### SSML Element Reference

| Element | Attributes | Description |
|---------|-----------|-------------|
| `<prosody>` | rate, pitch, volume | Speech characteristics |
| `<break>` | time | Pause duration |
| `<emphasis>` | level | Word emphasis |
| `<say-as>` | interpret-as | Number/date pronunciation |
| `<sub>` | alias | Pronunciation substitution |
| `<voice>` | name, gender, age | Voice selection |
| `<lang>` | xml:lang | Language selection |
| `<amazon:effect>` | name | Amazon-specific effects |

### Voice Quality Reference

| MOS Range | Quality | Description |
|-----------|---------|-------------|
| 4.0-5.0 | Excellent | Near-human quality |
| 3.5-4.0 | Good | Minor artifacts |
| 3.0-3.5 | Fair | Noticeable artifacts |
| 2.5-3.0 | Poor | Significant artifacts |
| 1.0-2.5 | Bad | Unintelligible |

### Pronunciation Dictionary Format

```
// CMU-style phoneme notation
OpenAI    OH-pen-ay-eye
NVIDIA    en-VID-ee-uh
GPT       gee-pee-tee
API       ay-pee-eye
JSON      jay-sawn
SQL       sequel
```

### Text Normalization Examples

| Input | Normalized |
|-------|-----------|
| $1,234.56 | twelve hundred thirty-four dollars and fifty-six cents |
| 42 | forty-two |
| 03/15/2024 | March fifteenth, twenty twenty-four |
| 3:30 PM | three thirty P M |
| Dr. Smith | Doctor Smith |
| etc. | etcetera |
| 1st | first |
| 10km | ten kilometers |

### Streaming Latency Reference

| Chunk Size | First-Audio Latency | Quality | Use Case |
|-----------|-------------------|---------|----------|
| 20ms | 50-80ms | Lower | Ultra-low latency |
| 50ms | 80-120ms | Good | Real-time interaction |
| 100ms | 120-180ms | Very good | Voice assistants |
| 200ms | 180-250ms | Excellent | Audiobook narration |
| 500ms | 250-400ms | Highest | Pre-recorded content |

### Voice Cloning Quality Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Speaker similarity | > 0.85 | Cosine similarity of embeddings |
| MOS | > 3.5 | Perceptual quality score |
| Intelligibility | > 0.95 | STOI against reference |
| Naturalness | > 3.5 | PESQ-like naturalness score |

### Multi-Language Support

| Language | Phoneme Set | G2P Model | Notes |
|----------|------------|-----------|-------|
| English | ARPAbet/IPA | Grapheme-to-Phoneme | Most supported |
| Mandarin | Pinyin | Custom | Tonal language |
| Japanese | Kana | MeCab-based | Mixed scripts |
| Spanish | IPA | Letter-to-Sound | Romance language |
| French | IPA | Letter-to-Sound | Liaison handling |
| German | IPA | Grapheme-to-Phoneme | Compound words |
| Korean | Hangul | Custom | Syllable blocks |
| Arabic | IPA | Custom | RTL, diacritics |

## Synthesis Models Deep Dive

### VITS2 Model Architecture

```python
from text_to_speech import VITS2Model, VITS2Config

config = VITS2Config(
    hidden_channels=192,
    hidden_channels_ffn=768,
    num_heads=2,
    num_layers=6,
    kernel_size=3,
    p_dropout=0.1,
    resblock="1",
    resblock_kernel_sizes=[3, 7, 11],
    resblock_dilation_sizes=[[1, 3, 5], [1, 3, 5], [1, 3, 5]],
    upsample_rates=[8, 8, 2, 2],
    upsample_initial_channel=192,
    upsample_kernel_sizes=[16, 16, 4, 4],
    n_speakers=109,
    speaker_embedding_dim=192,
    gin_channels=256,
)

model = VITS2Model(config)
model.load_weights("vits2_vctk_v1.ckpt")

# Generate mel spectrogram from text
text = "Hello, this is a test of the VITS2 model."
phonemes = model.text_to_phonemes(text)
mel = model.encode(phonemes, speaker_id=0)
```

### HiFi-GAN Vocoder Configuration

```python
from text_to_speech import HiFiGAN, HiFiGANConfig

hifigan_config = HiFiGANConfig(
    upsample_rates=[8, 8, 2, 2],
    upsample_kernel_sizes=[16, 16, 4, 4],
    upsample_initial_channel=192,
    resblock_kernel_sizes=[3, 7, 11],
    resblock_dilation_sizes=[[1, 3, 5], [1, 3, 5], [1, 3, 5]],
    sample_rate=22050,
    n_fft=1024,
    hop_length=256,
    win_length=1024,
)

vocoder = HiFiGAN(hifigan_config)
vocoder.load_weights("hifigan_v1.ckpt")

# Convert mel spectrogram to waveform
waveform = vocoder.infer(mel)
# waveform shape: (1, T) where T = mel_frames * hop_length
```

### Prosody Modeling with Control Tokens

```python
from text_to_speech import ProsodyModel, ControlToken

# Define prosody control tokens
prosody_model = ProsodyModel(
    model="fastspeech2_prosody",
    control_tokens=[
        ControlToken("pitch_high", embedding=[1.2, 0.0, 0.0]),
        ControlToken("pitch_low", embedding=[0.8, 0.0, 0.0]),
        ControlToken("speed_fast", embedding=[0.0, 1.3, 0.0]),
        ControlToken("speed_slow", embedding=[0.0, 0.7, 0.0]),
        ControlToken("energy_high", embedding=[0.0, 0.0, 1.2]),
        ControlToken("energy_low", embedding=[0.0, 0.0, 0.8]),
    ]
)

# Apply prosody tags in text
text_with_prosody = "[pitch_high] Exciting news! [/pitch_high] [speed_slow] Take your time. [/speed_slow]"
mel = prosody_model.synthesize(text_with_prosody, speaker="p225")
```

### Grapheme-to-Phoneme Conversion

```python
from text_to_speech import GraphemeToPhoneme

g2p = GraphemeToPhoneme(
    language="en",
    model="g2p_en_v2",
    use_lexicon=True,
    lexicon_path="lexicon.txt",
    espeak_phonemes=False
)

# Convert text to phonemes
text = "The quick brown fox jumps over the lazy dog."
phonemes = g2p.convert(text)
print(phonemes)
# "DH AH K W IH K B R AW N F AA KS J AH M P S OW V ER DH AH L EY ZIY D AO G"

# Handle special cases
pronunciation = g2p.get_pronunciation("COVID-19", context="medical")
print(pronunciation)
# Uses custom lexicon entry: "K OW V IH D N AY N T IY N"
```

### Multilingual Cross-Voice Synthesis

```python
from text_to_speech import CrossLingualSynthesizer

# Synthesize speech in multiple languages with the same voice
cross_lingual = CrossLingualSynthesizer(
    base_model="vits2_multilingual_v3",
    speaker_encoder="resemblyzer_v2",
    device="cuda"
)

# Clone voice and synthesize across languages
reference_embedding = cross_lingual.extract_speaker_embedding("reference.wav")

# Synthesize in English
en_audio = cross_lingual.synthesize(
    text="Hello, this is a multilingual synthesis test.",
    speaker_embedding=reference_embedding,
    language="en"
)

# Same voice, different language
zh_audio = cross_lingual.synthesize(
    text="你好，这是一个多语言合成测试。",
    speaker_embedding=reference_embedding,
    language="zh"
)

# Japanese with the same voice
ja_audio = cross_lingual.synthesize(
    text="こんにちは、これはマルチリンガル合成テストです。",
    speaker_embedding=reference_embedding,
    language="ja"
)
```

### Voice Quality Enhancement

```python
from text_to_speech import VoiceEnhancer, PostProcessor

# Post-process synthesized audio for quality improvement
enhancer = VoiceEnhancer(
    sample_rate=22050,
    noise_reduction=False,  # Already clean from vocoder
    dynamic_range_compression=True,
    target_lufs=-20.0,
    true_peak_dbtp=-1.0,
    de_essing=True,
    de_essing_freq=5000,
    de_essing_threshold=0.5
)

enhanced = enhancer.process(synthesized_audio)

# Add natural breathing sounds between sentences
post_processor = PostProcessor()
final_audio = post_processor.add_breaths(
    enhanced,
    breath_duration_ms=(200, 500),
    breath_volume_db=-20,
    insertion_points="auto"  # auto-detect sentence boundaries
)
```

### Model Quantization for Edge Deployment

```python
from text_to_speech import ModelQuantizer, TTSQuantizedEngine

# Quantize model for mobile/edge deployment
quantizer = ModelQuantizer(
    model_path="vits2_vctk_v1.onnx",
    quantization_method="dynamic",  # dynamic | static | qat
    dtype="int8",                    # int8 | fp16 | int4
    calibration_data="calibration_samples/",
    accuracy_threshold=0.95  # Max acceptable accuracy loss
)

quantized_model = quantizer.quantize()
quantizer.save(quantized_model, "vits2_vctk_v1_int8.onnx")

# Use quantized model
engine = TTSQuantizedEngine(
    model_path="vits2_vctk_v1_int8.onnx",
    vocoder_path="hifigan_v1_int8.onnx",
    device="cpu"
)

# Quantized model runs on CPU with minimal quality loss
audio = engine.synthesize("Hello from the edge.", voice="p225")
```

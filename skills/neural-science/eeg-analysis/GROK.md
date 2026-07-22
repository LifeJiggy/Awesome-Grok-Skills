---
name: "eeg-analysis"
category: "neural-science"
version: "1.0.0"
tags: ["neural-science", "eeg-analysis"]
---

# 

## Overview

Comprehensive eeg-analysis capabilities within the neural-science domain. This module provides tools, frameworks, and best practices for eeg-analysis operations.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

`python
from eeg-analysis import _module

# Initialize
engine = _module.Engine()

# Configure
engine.configure()

# Execute
results = engine.run()
print(results)
`

## Best Practices

- Follow security guidelines
- Implement proper error handling
- Use configuration management
- Monitor performance metrics
- Document API interfaces

## Related Modules

- Other modules in neural-science domain
- Integration points with external systems

---

## Advanced Configuration

EEG analysis systems require specialized configuration for signal acquisition, preprocessing, feature extraction, and classification. Configuration follows a pipeline-oriented model where each stage has its own parameters.

### Core Configuration Schema

```yaml
# eeg_analysis_config.yaml
acquisition:
  device_type: "biosemi64"            # biosemi64 | gtec64 | openbci32 | custom
  num_channels: 64
  sampling_rate: 1024                 # Hz (common: 256, 512, 1024, 2048, 30000)
  bit_depth: 24                       # ADC resolution
  reference: "average"               # average | linked_ears | cpz | resting
  ground: "afz"
  impedance_threshold_kohm: 5
  calibration_signal: true
  channel_layout: "standard_1020"    # standard_1020 | biosemi64 | custom
  montage_file: "electrode_positions.elc"

preprocessing:
  filter_chain:
    - type: "notch"
      frequency: 50                   # 50 Hz (EU) or 60 Hz (US)
      harmonics: [100, 150, 200]      # also remove harmonics
      quality: 30
    - type: "bandpass"
      low: 0.5
      high: 45.0
      order: 5
      filter_type: "butterworth"
    - type: "savgol"
      window_length: 31
      polyorder: 3

  artifact_rejection:
    method: "ica"                     # ica | asr | threshold | template_subtraction
    ica_algorithm: "fastica"          # fastica | infomax | picard
    ica_components_to_remove:
      - "eog"                        # eye blink artifacts
      - "emg"                        # muscle artifacts
      - "line_noise"                 # line noise
    asr_cutoff: 20                   # ASR calibration cutoff
    threshold_uv: 100                # peak-to-peak threshold
    min_segment_length_ms: 200

  re_referencing:
    method: "average"                # average | laplacian | rest
    local_laplacian_channels: 8      # number of neighbors for LAP

  epoching:
    event_markers: ["stimulus_onset", "response", "fixation"]
    epoch_window_ms: [-200, 800]     # relative to event
    baseline_correction: [-200, 0]   # baseline window
    rejection_threshold_uv: 150
    min_valid_epochs: 30

feature_extraction:
  time_domain:
    features: ["mean", "variance", "kurtosis", "skewness", "peak_amplitude"]
    window_ms: 250
    overlap_pct: 50

  frequency_domain:
    method: "welch"                  # welch | multitaper | fft | stft
    nperseg: 1024
    noverlap: 512
    nfft: 2048
    window: "hann"
    bands:
      delta: [0.5, 4]
      theta: [4, 8]
      alpha: [8, 13]
      beta: [13, 30]
      gamma: [30, 45]
      high_gamma: [45, 100]
    band_power_method: "trapezoid"   # trapezoid | median_frequency | peak_frequency

  time_frequency:
    method: "cwt"                    # cwt | stft | hilbert-huang
    wavelet: "morlet"                # morlet | mexican_hat | daubechies
    scales: "auto"
    freq_range: [0.5, 45]

  connectivity:
    method: "coherence"              # coherence | plv | granger | dpli | wpli
    frequency_bands: "all"
    window_ms: 1000
    overlap_pct: 50

  spatial:
    method: "csp"                    # csp | fbcsp | common_spatial_pattern
    num_filters: 6
    regularization: "ledoit_wolf"    # ledoit_wolf | shrinkage | none

classification:
  algorithm: "svm"                   # svm | lda | random_forest | cnn | rnn | transformer
  cross_validation:
    method: "stratified_kfold"
    n_folds: 5
    shuffle: true
    random_state: 42
  preprocessing_pipeline:
    - "standard_scaler"
    - "pca"                          # pca | ica | tsne
    n_components: 20
  hyperparameter_tuning:
    method: "bayesian"               # grid | random | bayesian
    n_iterations: 50
    scoring: "accuracy"

real_time:
  buffer_size_samples: 512
  latency_budget_ms: 100
  update_rate_hz: 10
  online_adaptation: true
  calibration_duration_sec: 60
```

### Dynamic Configuration API

```python
from eeg_analysis import EEGConfig, DynamicConfig

config = EEGConfig.from_yaml("eeg_analysis_config.yaml")
dynamic = DynamicConfig(config)

# Adjust preprocessing at runtime
dynamic.set("preprocessing.filter_chain.1.high", 40.0)
dynamic.set("feature_extraction.frequency_domain.method", "multitaper")

# Adaptive artifact threshold
@dynamic.on_adaptive("preprocessing.artifact_rejection.threshold_uv")
def adaptive_threshold(epoch_data, current_threshold):
    """Adapt threshold based on current noise level."""
    noise_level = np.std(epoch_data)
    return max(50, min(200, noise_level * 3))
```

---

## Architecture Patterns

### Pattern 1: EEG Processing Pipeline

```
Raw EEG Signal (1024 Hz × 64 channels)
    │
    ▼
┌──────────────────┐
│  Preprocessing   │  Notch → Bandpass → Re-reference
│  (Real-time)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Artifact        │  ICA decomposition → Remove components
│  Rejection       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Epoching        │  Segment around events
│                  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐     ┌──────────────────┐
│  Feature         │────▶│  Feature         │
│  Extraction      │     │  Selection       │
│  (Time/Freq)     │     │  (mRMR/ReliefF)  │
└──────────────────┘     └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Classification  │
                         │  (SVM/LDA/CNN)   │
                         └────────┬─────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Visualization   │
                         │  & Reporting     │
                         └──────────────────┘
```

### Pattern 2: Real-Time BCI Pipeline

```python
class RealTimeBCIPipeline:
    """Real-time EEG processing for brain-computer interface."""

    def __init__(self, config):
        self.preprocessor = OnlinePreprocessor(config.preprocessing)
        self.feature_extractor = OnlineFeatureExtractor(config.feature_extraction)
        self.classifier = OnlineClassifier(config.classification)
        self.feedback = FeedbackController(config.real_time)
        self.ring_buffer = RingBuffer(
            size_samples=config.real_time.buffer_size_samples * config.acquisition.num_channels
        )

    def process_sample(self, sample: np.ndarray, timestamp: float):
        # Add to ring buffer
        self.ring_buffer.append(sample)

        if self.ring_buffer.is_full():
            # Get latest window
            window = self.ring_buffer.get_latest(
                n_samples=self.config.feature_extraction.frequency_domain.nperseg
            )

            # Preprocess (online mode)
            clean = self.preprocessor.process_online(window)

            # Extract features
            features = self.feature_extractor.extract_online(clean)

            # Classify
            prediction = self.classifier.predict_online(features)

            # Send feedback
            self.feedback.update(prediction, timestamp)

            return prediction
        return None
```

### Pattern 3: Multi-Subject Transfer Learning

```python
class TransferLearningPipeline:
    """Transfer learning for cross-subject EEG decoding."""

    def __init__(self, source_subjects, config):
        self.source_data = self.load_multi_subject(source_subjects)
        self.feature_extractor = FeatureExtractor(config.feature_extraction)
        self.transfer_classifier = TransferClassifier(
            method="domain_adaptation",
            n_domains=len(source_subjects)
        )

    def adapt_to_new_subject(self, target_data, n_calibration_trials=20):
        # Extract features from source subjects
        source_features = self.extract_multi_subject_features(self.source_data)

        # Extract features from target subject (limited data)
        target_features = self.feature_extractor.extract(target_data[:n_calibration_trials])

        # Domain adaptation
        adapted_classifier = self.transfer_classifier.adapt(
            source_features=source_features,
            target_features=target_features,
            method="CORAL"  # Correlation Alignment
        )

        return adapted_classifier
```

---

## Integration Guide

### MNE-Python Integration

```python
import mne
from eeg_analysis import MNEBridge

bridge = MNEBridge()

# Load raw EEG data
raw = mne.io.read_raw_brainvision("experiment.vhdr", preload=True)

# Apply preprocessing
preprocessed = bridge.preprocess(raw, config.preprocessing)

# Extract epochs
epochs = bridge.create_epochs(
    preprocessed,
    events=events,
    event_id=event_id,
    tmin=-0.2,
    tmax=0.8,
    baseline=(-0.2, 0)
)

# Compute ERP
evoked = epochs.average()

# Feature extraction
features = bridge.extract_features(epochs, config.feature_extraction)

# Classification
predictions = bridge.classify(features, config.classification)
```

### EEGLAB Integration (MATLAB Bridge)

```python
from eeg_analysis.integration import EEGLABBridge

bridge = EEGLABBridge(matlab_engine=True)

# Load EEGLAB dataset
eeg = bridge.load_dataset("subject01.set")

# Apply EEGLAB preprocessing pipeline
eeg = bridge.run_pipeline(eeg, [
    {"function": "pop_runica", "method": "picard"},
    {"function": "pop_subcomp", "components": [0, 3, 7]},
    {"function": "pop_bandpass", "low": 1, "high": 40}
])

# Export back to Python
raw = bridge.to_mne(eeg)
```

### Real-Time Streaming (Lab Streaming Layer)

```python
from eeg_analysis.integration import LSLStream

# Receive EEG data via LSL
stream = LSLStream(
    stream_name="EEG",
    stream_type="EEG",
    channel_count=64,
    sampling_rate=1024,
    channel_format="float32"
)

# Process in real-time
for chunk in stream.receive_chunks(timeout=0.1):
    processed = preprocessor.process_online(chunk.data)
    features = feature_extractor.extract_online(processed)
    prediction = classifier.predict_online(features)
    print(f"Predicted class: {prediction}")
```

---

## Performance Optimization

### Benchmarking Reference

| Operation | Duration (ms) | Throughput | Bottleneck |
|-----------|---------------|------------|------------|
| Notch filter (50 Hz) | 2.1 | 476 Hz | CPU |
| Bandpass filter (0.5-45 Hz) | 3.4 | 294 Hz | CPU |
| ICA decomposition (64ch) | 156.3 | 6.4 Hz | CPU |
| ASR artifact rejection | 45.2 | 22.1 Hz | CPU |
| CSP feature extraction | 8.7 | 114.9 Hz | CPU |
| PSD computation (Welch) | 5.3 | 188.7 Hz | CPU |
| Time-frequency (CWT) | 12.4 | 80.6 Hz | CPU+GPU |
| SVM classification | 0.8 | 1250 Hz | CPU |
| CNN inference (GPU) | 3.2 | 312.5 Hz | GPU |
| Full pipeline (online) | 68.4 | 14.6 Hz | ICA |

### GPU Acceleration

```python
import cupy as cp
from eeg_analysis.gpu import GPUPreprocessor

gpu_preproc = GPUPreprocessor(device_id=0)

# Transfer data to GPU
raw_gpu = cp.asarray(raw_data)

# GPU-accelerated bandpass filter
filtered_gpu = gpu_preproc.butterworth_bandpass(
    raw_gpu,
    low_freq=0.5,
    high_freq=45.0,
    sampling_rate=1024,
    order=5
)

# GPU-accelerated PSD
psd_gpu = gpu_preproc.compute_psd_welch(
    filtered_gpu,
    nperseg=1024,
    noverlap=512
)

# Transfer back to CPU if needed
psd_cpu = cp.asnumpy(psd_gpu)
```

### Parallel Processing

```python
from concurrent.futures import ProcessPoolExecutor
from eeg_analysis.parallel import ParallelEEGProcessor

processor = ParallelEEGProcessor(
    n_workers=8,
    chunk_size=1000,   # epochs per worker
    shared_memory=True
)

# Process multiple subjects in parallel
results = processor.process_multi_subject(
    subject_files=["S01.fif", "S02.fif", "S03.fif", "S04.fif"],
    preprocessing_config=config.preprocessing,
    feature_config=config.feature_extraction
)
```

### Memory Optimization

```python
from eeg_analysis.memory import MemoryOptimizedPipeline

pipeline = MemoryOptimizedPipeline(
    config=config,
    memory_limit_mb=4096,
    use_memory_mapping=True,          # Memory-map large arrays
    streaming_mode=True,              # Process in chunks
    chunk_size_samples=10000,
    gc_after_each_stage=True          # Force garbage collection
)

# Process large dataset without OOM
for epoch in pipeline.stream_epochs("large_dataset.fif"):
    features = pipeline.extract_features(epoch)
    pipeline.accumulate(features)
```

---

## Security Considerations

### Data Protection

| Data Type | Sensitivity | Encryption | Retention | Access |
|-----------|------------|------------|-----------|--------|
| Raw EEG recordings | High | AES-256-GCM | 5 years | Researcher+ |
| Preprocessed epochs | Medium | AES-256-GCM | 2 years | Researcher+ |
| Feature matrices | Medium | AES-256-GCM | 2 years | Researcher+ |
| Classification results | Low | TLS in transit | 1 year | All |
| Subject metadata | High | AES-256-GCM | 5 years | Admin only |
| Artifacts/ICA components | Low | None | 6 months | Researcher+ |

### Subject Privacy (HIPAA/GDPR)

```python
from eeg_analysis.privacy import Anonymizer, ConsentManager

# Anonymize EEG data
anonymizer = Anonymizer(
    remove_subject_ids=True,
    remove_names=True,
    remove_dates=True,
    generalize_age=True,             # Age ranges instead of exact
    add_differential_privacy=True,
    epsilon=1.0
)

anonymized_data = anonymizer.anonymize(raw_data, metadata)

# Consent management
consent = ConsentManager()
consent.register(subject_id="S001", consent_type="research", expires="2027-01-01")
consent.register(subject_id="S001", consent_type="publication", expires="2027-01-01")

# Check before processing
if not consent.is_valid(subject_id="S001", purpose="research"):
    raise ConsentError("Subject consent expired or not granted")
```

### Secure Data Storage

```yaml
storage:
  encryption:
    at_rest: "aes-256-gcm"
    key_management: "aws_kms"        # aws_kms | vault | local
    key_rotation_days: 90

  access_control:
    authentication: "oauth2"
    authorization: "rbac"
    roles:
      researcher:
        - "read_data"
        - "write_analysis"
      clinician:
        - "read_data"
        - "read_reports"
      admin:
        - "*"

  audit_logging:
    enabled: true
    events:
      - "data_access"
      - "data_export"
      - "config_change"
    retention_days: 365
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| High 50/60 Hz noise | Poor grounding or line interference | Check ground electrode, add notch filter |
| Muscle artifacts | Subject tension or jaw clenching | Relaxation instructions, EMG rejection |
| Eye blink artifacts | Subject fatigue or dry eyes | ICA removal, eye-tracking correction |
| Low alpha power | Drowsiness or poor recording | Alertness check, check impedance |
| Poor classification | Insufficient training data | More calibration, data augmentation |
| High impedance | Electrode degradation | Clean/reapply electrodes, check contact |
| Data loss | Buffer overflow or disconnect | Check cable, increase buffer size |
| Phase distortion | Causal filter applied | Use zero-phase (filtfilt) filtering |

### Diagnostic Script

```python
from eeg_analysis.diagnostics import DiagnosticSuite

diag = DiagnosticSuite(config)
report = diag.run_full("experiment_data.fif")

# Quality metrics
print(f"Signal quality: {report.signal_quality_score:.2f}")
print(f"Artifact ratio: {report.artifact_ratio:.2%}")
print(f"SNR (alpha band): {report.snr_alpha:.2f} dB")
print(f"Channel drops: {report.dropped_channels}")
print(f"Impedance status: {report.impedance_status}")

# Visual report
report.plot_quality_dashboard(save_path="quality_dashboard.png")
report.export_pdf("diagnostic_report.pdf")
```

---

## API Reference

### EEGProcessor

```python
class EEGProcessor:
    def __init__(self, config: EEGConfig)

    def load(self, file_path: str) -> RawEEG

    def preprocess(self, raw: RawEEG) -> PreprocessedEEG

    def create_epochs(self, data: PreprocessedEEG, events: EventList) -> EpochSet

    def extract_features(self, epochs: EpochSet) -> FeatureMatrix

    def classify(self, features: FeatureMatrix) -> ClassificationResult

    def compute_connectivity(self, epochs: EpochSet) -> ConnectivityMatrix

    def compute_tfr(self, epochs: EpochSet) -> TimeFrequencyResult

    def generate_report(self, results: Dict) -> EEGReport
```

### Key Data Types

```python
@dataclass
class RawEEG:
    data: np.ndarray                  # (n_channels, n_samples)
    sampling_rate: int
    channel_names: List[str]
    channel_types: List[str]          # eeg, eog, emg, misc
    reference: str
    events: Optional[EventList] = None
    metadata: Dict[str, Any] = None

@dataclass
class EpochSet:
    data: np.ndarray                  # (n_epochs, n_channels, n_samples)
    events: np.ndarray                # (n_epochs, 3)
    event_id: Dict[str, int]
    tmin: float
    tmax: float
    baseline: Tuple[float, float]
    rejected_epochs: int = 0
    metadata: Dict[str, Any] = None

@dataclass
class FeatureMatrix:
    features: np.ndarray              # (n_epochs, n_features)
    feature_names: List[str]
    feature_types: List[str]          # time, frequency, spatial
    band_powers: Optional[np.ndarray] = None
    connectivity: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = None

@dataclass
class ClassificationResult:
    predictions: np.ndarray
    probabilities: np.ndarray
    accuracy: float
    confusion_matrix: np.ndarray
    cross_val_scores: np.ndarray
    feature_importances: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = None
```

---

## Data Models

### Entity Relationships

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Subject    │1────N │   Session    │1────N │   Recording  │
│──────────────│       │──────────────│       │──────────────│
│ id           │       │ id           │       │ id           │
│ age          │       │ subject_id   │       │ session_id   │
│ gender       │       │ date         │       │ raw_data_path│
│ condition    │       │ task         │       │ sampling_rate│
│ consent_id   │       │ duration_min │       │ n_channels   │
└──────────────┘       └──────────────┘       │ quality_score│
                                              └──────┬───────┘
                                                     │1
                                                     │N
                                              ┌──────┴───────┐
                                              │   Epoch      │
                                              │──────────────│
                                              │ id           │
                                              │ recording_id │
                                              │ event_type   │
                                              │ epoch_data   │
                                              │ is_valid     │
                                              └──────────────┘
```

### SQL Schema

```sql
CREATE TABLE subjects (
    id UUID PRIMARY KEY,
    anonymized_id VARCHAR(50) UNIQUE NOT NULL,
    age_range VARCHAR(20),
    gender VARCHAR(20),
    condition_code VARCHAR(50),
    consent_status VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    subject_id UUID REFERENCES subjects(id),
    session_date DATE NOT NULL,
    task_name VARCHAR(100),
    device_type VARCHAR(50),
    num_channels INTEGER,
    sampling_rate INTEGER,
    duration_seconds FLOAT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE recordings (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions(id),
    raw_data_path VARCHAR(500),
    preprocessed_data_path VARCHAR(500),
    channel_names TEXT[],
    quality_score FLOAT,
    artifact_ratio FLOAT,
    impedance_data JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE epochs (
    id UUID PRIMARY KEY,
    recording_id UUID REFERENCES recordings(id),
    epoch_index INTEGER,
    event_type VARCHAR(50),
    event_latency_ms FLOAT,
    epoch_data_path VARCHAR(500),
    is_valid BOOLEAN DEFAULT TRUE,
    rejection_reason VARCHAR(100),
    peak_amplitude_uv FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE features (
    id UUID PRIMARY KEY,
    epoch_id UUID REFERENCES epochs(id),
    feature_set_name VARCHAR(100),
    feature_vector FLOAT[],
    band_powers JSONB,
    connectivity JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE classification_results (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES sessions(id),
    algorithm VARCHAR(50),
    accuracy FLOAT,
    confusion_matrix FLOAT[][],
    cross_val_scores FLOAT[],
    hyperparameters JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_epochs_recording ON epochs(recording_id);
CREATE INDEX idx_features_epoch ON features(epoch_id);
CREATE INDEX idx_results_session ON classification_results(session_id);
```

---

## Deployment Guide

### Local Development

```bash
git clone https://github.com/example/eeg-analysis.git
cd eeg-analysis
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,hardware]"

# Download sample dataset
python -m eeg_analysis.datasets.download sample_dataset

# Run analysis
python -m eeg_analysis.cli analyze \
    --input data/sample.fif \
    --config config/eeg_config.yaml \
    --output results/
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for MNE-Python
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libxkbcommon-x11-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "-m", "eeg_analysis.server", "--port", "8080"]
```

```yaml
# docker-compose.yml
version: "3.9"
services:
  eeg-api:
    build: .
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data:ro
      - ./config:/app/config:ro
      - eeg-results:/app/results
    environment:
      - EEG_LOG_LEVEL=info
      - EEG_MAX_WORKERS=8

  influxdb:
    image: influxdb:2.7
    ports:
      - "8086:8086"
    volumes:
      - influx-data:/var/lib/influxdb2

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    volumes:
      - grafana-data:/var/lib/grafana

volumes:
  eeg-results:
  influx-data:
  grafana-data:
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: eeg-analysis-server
  labels:
    app: eeg-analysis-server
spec:
  replicas: 2
  selector:
    matchLabels:
      app: eeg-analysis-server
  template:
    metadata:
      labels:
        app: eeg-analysis-server
    spec:
      containers:
      - name: server
        image: eeg-analysis-server:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "2"
            memory: "4Gi"
          limits:
            cpu: "4"
            memory: "8Gi"
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 5
```

---

## Monitoring & Observability

### Pipeline Metrics

```python
from eeg_analysis.monitoring import EEGMetrics

metrics = EEGMetrics(
    backend="prometheus",
    prefix="eeg",
    labels={"experiment": "motor_imagery", "subject_group": "healthy"}
)

# Metrics tracked:
# eeg_recording_duration_seconds (histogram)
# eeg_epochs_rejected_total (counter)
# eeg_feature_extraction_latency_ms (histogram)
# eeg_classification_accuracy (gauge)
# eeg_artifact_ratio (gauge)
# eeg_active_sessions (gauge)
# eeg_processing_queue_size (gauge)
```

### Prometheus Queries

```promql
# Average classification accuracy
avg(eeg_classification_accuracy)

# Artifact rejection rate
rate(eeg_epochs_rejected_total[1h]) / rate(eeg_epochs_total[1h])

# Feature extraction latency P95
histogram_quantile(0.95, eeg_feature_extraction_latency_ms_bucket)

# Active recording sessions
eeg_active_sessions

# Data volume per session
rate(eeg_recording_duration_seconds_sum[1h])
```

### Grafana Dashboard

```json
{
  "panels": [
    {
      "title": "Classification Accuracy Over Time",
      "type": "timeseries",
      "targets": [{"expr": "eeg_classification_accuracy"}]
    },
    {
      "title": "Artifact Ratio by Session",
      "type": "bargauge",
      "targets": [{"expr": "eeg_artifact_ratio"}]
    },
    {
      "title": "Processing Latency Distribution",
      "type": "histogram",
      "targets": [{"expr": "eeg_feature_extraction_latency_ms_bucket"}]
    }
  ]
}
```

---

## Testing Strategy

### Unit Tests

```python
import pytest
import numpy as np
from eeg_analysis import BandpassFilter, CSPExtractor, EpochManager

@pytest.fixture
def sample_eeg():
    """Generate synthetic EEG data for testing."""
    np.random.seed(42)
    n_channels, n_samples = 64, 10240
    t = np.arange(n_samples) / 1024
    data = np.zeros((n_channels, n_samples))
    for ch in range(n_channels):
        data[ch] = (np.sin(2 * np.pi * 10 * t) +  # 10 Hz alpha
                     np.random.randn(n_samples) * 0.1)
    return data, 1024

class TestBandpassFilter:
    def test_removes_out_of_band(self, sample_eeg):
        data, sr = sample_eeg
        filt = BandpassFilter(low=8, high=13, fs=sr, order=5)
        filtered = filt.apply(data)
        # Power outside alpha band should be reduced
        freqs = np.fft.rfftfreq(n_samples, 1/sr)
        psd = np.abs(np.fft.rfft(filtered))**2
        outside_mask = (freqs < 8) | (freqs > 13)
        assert np.mean(psd[:, outside_mask]) < 0.01

    def test_preserves_in_band(self, sample_eeg):
        data, sr = sample_eeg
        filt = BandpassFilter(low=8, high=13, fs=sr, order=5)
        filtered = filt.apply(data)
        freqs = np.fft.rfftfreq(n_samples, 1/sr)
        psd = np.abs(np.fft.rfft(filtered))**2
        inside_mask = (freqs >= 8) & (freqs <= 13)
        assert np.mean(psd[:, inside_mask]) > 0.5
```

### Integration Tests

```python
@pytest.mark.integration
class TestEEGPipeline:
    def test_full_pipeline(self):
        processor = EEGProcessor(config)
        raw = processor.load("test_data.fif")
        preprocessed = processor.preprocess(raw)
        epochs = processor.create_epochs(preprocessed, events)
        features = processor.extract_features(epochs)
        result = processor.classify(features)
        assert result.accuracy > 0.5  # Above chance
        assert len(result.predictions) == len(epochs)

    def test_artifact_rejection(self):
        processor = EEGProcessor(config)
        raw = processor.load("noisy_data.fif")
        preprocessed = processor.preprocess(raw)
        epochs = processor.create_epochs(preprocessed, events)
        assert epochs.rejected_epochs < len(epochs) * 0.5  # <50% rejected
```

### Performance Benchmarks

```python
from eeg_analysis.benchmark import BenchmarkSuite

suite = BenchmarkSuite(config)
results = suite.run(
    test_data="benchmark_data.fif",
    operations=["preprocessing", "feature_extraction", "classification"]
)

assert results.preprocessing_latency_p95_ms < 50
assert results.feature_extraction_latency_p95_ms < 100
assert results.classification_latency_p95_ms < 10
assert results.throughput_hz > 10  # At least 10 Hz real-time
```

---

## Versioning & Migration

### Version Compatibility

| Version | Python | MNE-Python | NumPy | Status |
|---------|--------|------------|-------|--------|
| 1.0.0 | 3.10+ | 1.6+ | 1.24+ | Current |
| 0.9.0 | 3.9+ | 1.5+ | 1.22+ | Supported |
| 0.8.0 | 3.8+ | 1.4+ | 1.20+ | Legacy |
| 0.7.0 | 3.8+ | 1.3+ | 1.19+ | EOL |

### Migration Scripts

```python
from eeg_analysis.migration import Migrator, Step

migrator = Migrator(from_version="0.9.0", to_version="1.0.0", steps=[
    Step(
        id="migrate_feature_format",
        description="Update feature matrix format to new schema",
        forward=lambda db: migrate_feature_schema_v09_to_v10(db),
        backward=lambda db: migrate_feature_schema_v10_to_v09(db),
    ),
    Step(
        id="update_channel_names",
        description="Standardize channel naming convention",
        forward=lambda db: standardize_channel_names(db),
    ),
])

migrator.migrate(dry_run=True)
migrator.migrate(dry_run=False)
```

---

## Glossary

| Term | Definition |
|------|-----------|
| Alpha Band | EEG frequency range 8-13 Hz, associated with relaxed wakefulness |
| Artifact | Non-neural contamination in EEG signal (eye blink, muscle, line noise) |
| ASR | Artifact Subspace Reconstruction — adaptive artifact removal method |
| Bandpass Filter | Filter that passes frequencies within a specified range |
| Beta Band | EEG frequency range 13-30 Hz, associated with active cognition |
| CWT | Continuous Wavelet Transform — time-frequency decomposition method |
| CSP | Common Spatial Pattern — spatial filter for discriminating EEG classes |
| ERP | Event-Related Potential — averaged EEG response to a stimulus |
| Gamma Band | EEG frequency range 30-100 Hz, associated with binding and attention |
| ICA | Independent Component Analysis — blind source separation method |
| LAP | Local Average Reference — Laplacian spatial filter |
| Montage | Electrode placement configuration on the scalp |
| Notch Filter | Filter that removes a specific frequency (50/60 Hz line noise) |
| PSD | Power Spectral Distribution — frequency content of signal |
| SNR | Signal-to-Noise Ratio — measure of signal quality |
| Theta Band | EEG frequency range 4-8 Hz, associated with memory and navigation |
| Welch's Method | PSD estimation using averaged periodograms |
| Windowing | Applying a window function to reduce spectral leakage |

---

## Changelog

### v1.0.0 (2026-05-01)
- Initial stable release
- Complete preprocessing pipeline (notch, bandpass, re-reference, ICA)
- Feature extraction (time, frequency, time-frequency, connectivity, spatial)
- Classification (SVM, LDA, Random Forest, CNN)
- Real-time BCI pipeline with <100ms latency
- MNE-Python and EEGLAB integration
- LSL streaming support
- GPU acceleration for CWT and CNN
- Comprehensive diagnostic suite

### v0.9.0 (2025-11-15)
- Beta release with core preprocessing
- CSP feature extraction
- Basic SVM/LDA classification
- Epoch management and quality metrics

### v0.8.0 (2025-06-01)
- Proof of concept with basic filtering
- Initial feature extraction (band powers)
- Synthetic data generation for testing

---

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/eeg-analysis.git
cd eeg-analysis
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,hardware]"

# Run tests
pytest tests/ --cov=eeg_analysis --cov-report=html

# Lint
ruff check eeg_analysis/
ruff format eeg_analysis/

# Generate sample data for development
python -m eeg_analysis.datasets.generate_synthetic --n_subjects=5
```

### Code Standards

- Type hints required for all public functions
- Docstrings required for all classes and public methods
- Unit test coverage minimum: 85%
- Hardware-dependent tests marked with `@pytest.mark.hardware`
- All signal processing functions must handle edge cases (empty input, single channel, etc.)
- Statistical tests required for any classification comparison

### Commit Convention

```
feat(preprocessing): add adaptive ASR artifact removal
fix(filter): correct phase distortion in causal bandpass
perf(gpu): optimize CWT with CUDA kernels
docs(api): update API reference for v1.0
test(classification): add cross-validation tests for SVM
```

---

## License

MIT License

Copyright (c) 2026 EEG Analysis Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

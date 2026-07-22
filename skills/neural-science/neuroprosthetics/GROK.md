---
name: "neuroprosthetics"
category: "neural-science"
version: "1.0.0"
tags: ["neural-science", "neuroprosthetics"]
---

# 

## Overview

Comprehensive neuroprosthetics capabilities within the neural-science domain. This module provides tools, frameworks, and best practices for neuroprosthetics operations.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

`python
from neuroprosthetics import _module

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

Neuroprosthetics systems require strict real-time configuration, safety-critical parameters, and hardware-specific tuning. The configuration is organized into three tiers: device-level, signal-processing, and application-level.

### Core Configuration Schema

```yaml
# neuroprosthetics_config.yaml
device:
  type: "bci_controller"              # bci_controller | neural_stimulator | neuroprosthesis
  model: "Neuralink_N1"               # device model identifier
  channels: 1024                      # electrode channels
  sampling_rate: 30000                 # Hz (ECoG: 1000, Utah array: 30000)
  bit_depth: 16                       # ADC bit resolution
  buffer_size_ms: 50                  # circular buffer duration
  interface: "usb3"                   # usb3 | ble | wifi | implant_wired
  power_mode: "low_power"             # low_power | normal | high_performance
  battery_threshold_pct: 15           # auto-shutdown below this

signal_processing:
  filter_chain:
    - type: "notch"
      frequency: 50                   # 50 Hz (Europe) or 60 Hz (US)
      quality: 30
    - type: "bandpass"
      low: 0.5                        # Hz
      high: 500                       # Hz
      order: 4
      filter_type: "butterworth"      # butterworth | chebyshev | fir
    - type: "common_average_reference"
      enabled: true
    - type: "artifact_rejection"
      method: "threshold"             # threshold | ica | adaptive
      threshold_uv: 200               # microvolts
      window_ms: 200

  feature_extraction:
    method: "csp"                     # csp | fft | wavelet | hilbert | spectrogram
    bands:
      delta: [0.5, 4]
      theta: [4, 8]
      alpha: [8, 13]
      beta: [13, 30]
      gamma: [30, 100]
      high_gamma: [100, 500]
    window_ms: 250
    overlap_pct: 50
    normalization: "z-score"          # z-score | min-max | robust

  decoding:
    algorithm: "kalman_filter"        # kalman_filter | rml | cnn | rnn | transformer
    state_dim: 7                      # cursor position (x,y,z) + velocity + acceleration
    observation_dim: 64               # CSP components
    update_rate_hz: 200               # decoder refresh rate
    calibration_sessions: 5           # sessions needed for calibration
    adaptation_rate: 0.01             # online adaptation speed

stimulation:
  mode: "biphasic"                    # monophasic | biphasic | synchronized
  pulse_width_us: 200                 # microseconds
  amplitude_ma: 1.5                   # milliamps
  frequency_hz: 100                   # stimulation frequency
  charge_limit_uc: 30                 # microcoulombs (safety limit)
  electrode_select: "adaptive"        # adaptive | fixed | sequential
  safety_interlock: true              # hardware safety interlock
  impedance_monitoring: true          # continuous impedance check

application:
  target: "motor_rehabilitation"      # motor_rehabilitation | sensory_restoration | communication
  target_muscles: ["bicep", "tricep", "deltoid"]
  feedback_mode: "visual"             # visual | haptic | auditory | combined
  latency_budget_ms: 50               # max end-to-end latency
  session_duration_min: 60
  rest_interval_min: 5
```

### Real-Time Configuration API

```python
from neuroprosthetics import DeviceConfig, RTConfig

config = DeviceConfig.from_yaml("neuroprosthetics_config.yaml")

# Real-time parameter adjustment (no restart)
rt = RTConfig(config)
rt.set_stimulation_amplitude(2.0, electrode_id=42)
rt.set_filter_cutoff("bandpass", high=300)
rt.set_decoder_update_rate(500)

# Safety-critical: must confirm amplitude changes
@rt.safety_guard(max_amplitude=5.0, max_charge=30)
def safe_amplitude_update(electrode_id, new_amplitude):
    rt.set_stimulation_amplitude(new_amplitude, electrode_id=electrode_id)
```

---

## Architecture Patterns

### Pattern 1: Closed-Loop Neuroprosthetic System

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Neural     │───▶│  Signal      │───▶│  Decoder     │
│  Interface  │    │  Processing  │    │  (Kalman)    │
│  (1024 ch)  │◀───│  Chain       │◀───│              │
└─────────────┘    └──────────────┘    └──────┬───────┘
                                              │
                                              ▼
┌─────────────┐    ┌──────────────┐    ┌──────────────┐
│  Effector   │◀───│  Stimulation │◀───│  Control     │
│  (Muscle/   │───▶│  Engine      │    │  Policy      │
│   Robot)    │    │              │    │              │
└─────────────┘    └──────────────┘    └──────────────┘
       │                                    ▲
       │            ┌──────────────┐        │
       └───────────▶│  Feedback    │────────┘
                    │  Controller  │
                    └──────────────┘
```

### Pattern 2: Hierarchical BCI Architecture

```python
class HierarchicalBCI:
    """Hierarchical brain-computer interface with coarse-to-fine decoding."""

    def __init__(self, config):
        self.macro_decoder = MacroDecoder(
            intent_classes=["reach", "grasp", "release", "rest"],
            model_type="csp_lda"
        )
        self.micro_decoder = MicroDecoder(
            kinematic_dims=7,
            model_type="kalman_filter"
        )
        self.refinement_net = RefinementNetwork(
            input_dim=7, output_dim=7,
            model_type="lstm"
        )
        self.stim_controller = StimulationController(config.stimulation)

    def process_neural_data(self, neural_signal):
        # Level 1: Classify high-level intent
        intent = self.macro_decoder.classify(neural_signal)

        # Level 2: Decode detailed kinematics
        kinematics = self.micro_decoder.decode(neural_signal)

        # Level 3: Refine with temporal context
        refined = self.refinement_net.refine(kinematics, intent)

        # Generate stimulation commands
        stim_params = self.stim_controller.compute_stim_params(
            intent=intent,
            kinematics=refined
        )
        return stim_params
```

### Pattern 3: Adaptive Calibration System

```python
class AdaptiveCalibration:
    """Online calibration that adapts decoder to user's neural patterns."""

    def __init__(self, decoder, config):
        self.decoder = decoder
        self.calibration_buffer = CalibrationBuffer(max_sessions=10)
        self.adaptation_rate = config.adaptation_rate
        self.min_samples = config.calibration_samples_min

    def calibrate(self, neural_data, target_kinematics):
        self.calibration_buffer.add(neural_data, target_kinematics)

        if self.calibration_buffer.size >= self.min_samples:
            # Incremental decoder update
            X, y = self.calibration_buffer.get_data()
            self.decoder.update(X, y, learning_rate=self.adaptation_rate)

            # Evaluate calibration quality
            r2_score = self.decoder.cross_validate(X, y)
            return CalibrationResult(
                status="success",
                r2_score=r2_score,
                samples_used=self.calibration_buffer.size
            )
        return CalibrationResult(status="insufficient_data")

    def handle_nonstationarity(self, neural_data):
        """Detect and adapt to neural signal non-stationarity."""
        drift_score = self.detect_drift(neural_data)
        if drift_score > self.config.drift_threshold:
            self.decoder.adjust_for_drift(neural_data)
            return True
        return False
```

---

## Integration Guide

### Hardware Integration

```python
from neuroprosthetics.hardware import NeuralInterface, StimulatorInterface

# Connect to neural recording hardware
neural_iface = NeuralInterface(
    device_type="blackrock_miport",
    num_channels=128,
    sampling_rate=30000,
    buffer_size=1000
)

# Connect to stimulation hardware
stim_iface = StimulatorInterface(
    device_type="rtcs_impulse",
    num_channels=32,
    max_amplitude_ma=5.0,
    pulse_width_range_us=(50, 500)
)

# Unified neuroprosthetic controller
controller = NeuroprostheticController(
    neural_interface=neural_iface,
    stim_interface=stim_iface,
    decoder=kalman_decoder,
    config=config
)
```

### Clinical System Integration (HL7 FHIR)

```python
from neuroprosthetics.integration import ClinicalFHIRBridge

bridge = ClinicalFHIRBridge(
    fhir_server="https://clinical-hospital.org/fhir",
    device_id="NP-DEVICE-001",
    patient_id="patient_123"
)

# Report device status to clinical system
bridge.report_device_status(
    battery_level=85,
    impedance_status="normal",
    session_active=True,
    firmware_version="2.1.0"
)

# Report stimulation parameters
bridge.report_stimulation_params({
    "amplitude_ma": 1.5,
    "pulse_width_us": 200,
    "frequency_hz": 100,
    "electrode_count": 8
})

# Fetch clinical data
patient_profile = bridge.get_patient_profile("patient_123")
medications = bridge.get_current_medications("patient_123")
```

### Research Data Integration (BIDS Format)

```python
from neuroprosthetics.integration import BIDSEncoder

encoder = BIDSEncoder(
    dataset_name="neuroprosthetic_motor_control",
    sessions=["S001", "S002", "S003"]
)

encoder.write_eeg(
    data=neural_data,           # shape: (channels, samples)
    sampling_rate=30000,
    channel_names=["CH001", "CH002", ...],
    task="motor_imagery_reach",
    sidecar={
        "Manufacturer": "Blackrock Microsystems",
        "DeviceSerialNumber": "MI-12345",
        "SamplingFrequency": 30000
    }
)
```

---

## Performance Optimization

### Real-Time Performance Requirements

| Operation | Budget (ms) | Achieved (ms) | Status |
|-----------|-------------|---------------|--------|
| Neural signal acquisition | 1.0 | 0.8 | OK |
| Filter chain (notch + bandpass) | 2.0 | 1.4 | OK |
| Common average reference | 1.5 | 0.9 | OK |
| Artifact rejection | 3.0 | 2.1 | OK |
| Feature extraction (CSP) | 5.0 | 3.7 | OK |
| Kalman filter decode | 2.0 | 1.2 | OK |
| Stimulation parameter compute | 1.0 | 0.6 | OK |
| Stimulation delivery | 1.0 | 0.5 | OK |
| **Total end-to-end** | **16.5** | **11.2** | **OK** |

### Latency Optimization

```python
from neuroprosthetics.optimization import RTScheduler, PinToCore

# Pin critical threads to dedicated CPU cores
scheduler = RTScheduler(
    acquisition_thread=PinToCore(core=0),
    processing_thread=PinToCore(core=1),
    decoding_thread=PinToCore(core=2),
    stimulation_thread=PinToCore(core=3)
)

# Zero-copy ring buffers for neural data
buffer = SharedRingBuffer(
    size_bytes=1024 * 1024,  # 1MB
    num_slots=1000,
    lock_free=True
)

# Pre-allocated memory pools
pool = MemoryPool(
    block_size=4096,
    num_blocks=1000,
    alignment=64  # Cache-line aligned
)
```

### Computational Optimization

```python
import numpy as np
from numba import jit, prange

@jit(nopython=True, parallel=True, cache=True)
def compute_csp_features(neural_data, filters):
    """Compute CSP features with optimized JIT compilation."""
    n_trials, n_channels, n_samples = neural_data.shape
    n_filters = len(filters)
    features = np.zeros((n_trials, n_filters))

    for i in prange(n_trials):
        for j in prange(n_filters):
            filtered = np.dot(filters[j], neural_data[i])
            features[i, j] = np.log(np.var(filtered) + 1e-10)

    return features

@jit(nopython=True, cache=True)
def kalman_predict(state_mean, state_cov, transition_matrix, process_noise):
    """Optimized Kalman filter prediction step."""
    predicted_mean = transition_matrix @ state_mean
    predicted_cov = transition_matrix @ state_cov @ transition_matrix.T + process_noise
    return predicted_mean, predicted_cov
```

---

## Security Considerations

### Patient Safety

| Safety Measure | Implementation | Monitoring |
|----------------|---------------|------------|
| Charge density limit | Hardware interlock at 30 μC/cm² | Continuous ADC monitoring |
| Impedance monitoring | Real-time impedance at 1 kHz | Alert if >5 kΩ or <100 Ω |
| Maximum stimulation | Firmware-limited amplitude | Watchdog timer |
| Session timeout | Auto-stop after 60 min | Software timer |
| Emergency stop | Hardware kill switch | Button + software |
| Thermal monitoring | Temperature sensor on implant | Alert if >41°C |

### Cybersecurity for Implanted Devices

```yaml
security:
  authentication:
    device_pairing: "mutual_tls"
    session_token: "aes256_hmac"
    max_failed_attempts: 3
    lockout_duration_s: 300

  encryption:
    data_at_rest: "aes-256-gcm"
    data_in_transit: "tls1.3"
    key_rotation_days: 90

  access_control:
    role: "rbac"
    roles:
      clinician:
        - "configure_stimulation"
        - "view_data"
        - "export_data"
      researcher:
        - "view_data"
        - "export_data"
      patient:
        - "view_status"
        - "emergency_stop"

  audit_logging:
    enabled: true
    retention_days: 365
    events:
      - "stimulation_parameter_change"
      - "device_activation"
      - "emergency_stop"
      - "firmware_update"
```

### Firmware Security

```python
from neuroprosthetics.security import FirmwareVerifier, SecureBoot

verifier = FirmwareVerifier(
    signature_algorithm="ed25519",
    public_key_path="/secure/keys/device_key.pub"
)

secure_boot = SecureBoot(
    verifier=verifier,
    anti_rollback=True,
    min_version=2,
    hash_algorithm="sha384"
)

# Verify firmware before update
result = verifier.verify(firmware_binary, firmware_signature)
if not result.valid:
    raise SecurityError(f"Firmware verification failed: {result.reason}")
```

---

## Troubleshooting Guide

### Common Issues

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| High impedance on channels | Electrode degradation | Check electrode array, recalibrate |
| Increased noise floor | Ground loop or interference | Check grounding, add shield |
| Decoder performance drop | Neural signal non-stationarity | Recalibrate, adjust adaptation rate |
| Stimulation pain report | Current density too high | Reduce amplitude, increase pulse width |
| Communication lag | WiFi interference | Switch to wired, reduce packet size |
| Impedance spikes | Electrode-tissue interface change | Pause stimulation, re-check impedance |
| Calibration failure | Insufficient data quality | Extend calibration session, improve focus |
| Battery drain | High-power mode active | Switch to low-power mode |

### Diagnostic Tools

```python
from neuroprosthetics.diagnostics import DiagnosticSuite

diagnostics = DiagnosticSuite(device, config)

# Run full system diagnostic
report = diagnostics.run_full()
print(f"Impedance: {report.impedance_status}")
print(f"Noise floor: {report.noise_floor_uv} μV")
print(f"Decoder accuracy: {report.decoder_accuracy:.3f}")
print(f"Stimulation safety: {report.stim_safety_status}")

# Generate diagnostic report for clinician
report.export_pdf("/tmp/device_diagnostic_report.pdf")
```

---

## API Reference

### NeuroprostheticController

```python
class NeuroprostheticController:
    def __init__(self, neural_interface, stim_interface, decoder, config)

    def start_session(self, patient_id: str) -> SessionHandle

    def process_neural_data(self, data: np.ndarray) -> StimulationCommand

    def send_stimulation(self, command: StimulationCommand) -> StimResult

    def stop_session(self, session_id: str) -> SessionSummary

    def calibrate(self, calibration_data: CalibrationSet) -> CalibrationResult

    def get_device_status(self) -> DeviceStatus
```

### Key Data Types

```python
@dataclass
class StimulationCommand:
    electrode_id: int
    amplitude_ma: float
    pulse_width_us: int
    frequency_hz: float
    phase: str                          # cathodic_first | anodic_first
    timestamp: float
    safety_check_passed: bool

@dataclass
class NeuralSample:
    channel_data: np.ndarray            # (n_channels,)
    timestamp: float
    impedance: Optional[np.ndarray]     # (n_channels,)
    artifact_flag: Optional[bool] = False

@dataclass
class SessionSummary:
    session_id: str
    patient_id: str
    start_time: datetime
    end_time: datetime
    duration_min: float
    total_stimulation_pulses: int
    mean_decoder_accuracy: float
    events: List[ClinicalEvent]
```

---

## Data Models

### Clinical Data Schema

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    Patient   │1────N │   Session    │1────N │   Recording  │
│──────────────│       │──────────────│       │──────────────│
│ id           │       │ id           │       │ id           │
│ demographics │       │ patient_id   │       │ session_id   │
│ condition    │       │ device_id    │       │ channel_data │
│ consent      │       │ clinician_id │       │ sampling_rate│
│ notes        │       │ start_time   │       │ impedance    │
└──────────────┘       │ end_time     │       │ timestamp    │
                       └──────┬───────┘       └──────────────┘
                              │1
                              │N
                       ┌──────┴───────┐
                       │ Stimulation  │
                       │──────────────│
                       │ id           │
                       │ session_id   │
                       │ parameters   │
                       │ response     │
                       │ adverse_events│
                       └──────────────┘
```

### SQL Schema

```sql
CREATE TABLE patients (
    id UUID PRIMARY KEY,
    mrn VARCHAR(50) UNIQUE NOT NULL,
    condition_code VARCHAR(20),
    implant_date DATE,
    device_model VARCHAR(100),
    consent_signed BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE sessions (
    id UUID PRIMARY KEY,
    patient_id UUID NOT NULL REFERENCES patients(id),
    clinician_id UUID REFERENCES clinicians(id),
    start_time TIMESTAMPTZ NOT NULL,
    end_time TIMESTAMPTZ,
    session_type VARCHAR(50),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE recordings (
    id UUID PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES sessions(id),
    channel_data_path VARCHAR(500),
    sampling_rate INTEGER NOT NULL,
    num_channels INTEGER NOT NULL,
    duration_sec FLOAT,
    impedance_snapshot JSONB,
    quality_score FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE stimulation_events (
    id UUID PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES sessions(id),
    electrode_id INTEGER NOT NULL,
    amplitude_ma FLOAT,
    pulse_width_us INTEGER,
    frequency_hz FLOAT,
    total_pulses INTEGER,
    patient_feedback TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Deployment Guide

### Clinical Deployment Checklist

```yaml
deployment_checklist:
  pre_installation:
    - [ ] Device serial number registered
    - [ ] Firmware version verified (>=2.1.0)
    - [ ] Clinical site network configured
    - [ ] Backup power supply tested
    - [ ] Emergency stop button accessible
    - [ ] Patient consent documented

  installation:
    - [ ] Device physically installed
    - [ ] Electrode impedance verified (<5 kΩ all channels)
    - [ ] Stimulation safety test passed
    - [ ] Communication link established
    - [ ] Clinical software configured

  post_installation:
    - [ ] Baseline calibration completed
    - [ ] Patient training session scheduled
    - [ ] Monitoring dashboard configured
    - [ ] Alert thresholds set
    - [ ] Documentation updated
```

### Docker Deployment

```dockerfile
FROM neuroprosthetics/runtime:2.1.0

WORKDIR /app
COPY --chown=neuroprosthetics:neuroprosthetics config/ /app/config/
COPY --chown=neuroprosthetics:neuroprosthetics src/ /app/src/

EXPOSE 8080 9090

HEALTHCHECK --interval=10s --timeout=3s --retries=5 \
    CMD curl -f http://localhost:8080/health/device || exit 1

CMD ["python", "-m", "neuroprosthetics.server", \
     "--config", "/app/config/device_config.yaml", \
     "--port", "8080"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: neuroprosthetics-server
  namespace: medical-devices
spec:
  replicas: 2
  selector:
    matchLabels:
      app: neuroprosthetics-server
  template:
    spec:
      containers:
      - name: server
        image: neuroprosthetics-server:2.1.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            cpu: "1"
            memory: "2Gi"
          limits:
            cpu: "2"
            memory: "4Gi"
        securityContext:
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          runAsUser: 1000
```

---

## Monitoring & Observability

### Device Health Metrics

```python
from neuroprosthetics.monitoring import DeviceMetrics

metrics = DeviceMetrics(
    device_id="NP-001",
    export_interval_sec=30
)

# Real-time metrics tracked:
# - impedance_per_channel (gauge, per channel)
# - stimulation_amplitude_ma (gauge)
# - battery_level_pct (gauge)
# - decoder_accuracy (gauge)
# - end_to_end_latency_ms (histogram)
# - total_stimulation_pulses (counter)
# - artifact_rejection_rate (gauge)
# - device_temperature_celsius (gauge)
```

### Clinical Dashboard

```promql
# Decoder accuracy trend
avg_over_time(neuro_decoder_accuracy[1h])

# Impedance per channel
neuro_impedance_ohm

# Stimulation safety
neuro_charge_density_uc_per_cm2

# Session duration
neuro_session_duration_minutes

# Battery level
neuro_battery_level_pct

# Adverse event count
sum(rate(neuro_adverse_event_total[24h]))
```

### Alerting Rules

```yaml
groups:
  - name: neuroprosthetics-safety
    rules:
      - alert: HighImpedance
        expr: neuro_impedance_ohm > 5000
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Electrode impedance exceeds 5kΩ"

      - alert: DecoderAccuracyLow
        expr: neuro_decoder_accuracy < 0.6
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Decoder accuracy below 60%"

      - alert: BatteryCritical
        expr: neuro_battery_level_pct < 15
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Device battery below 15%"
```

---

## Testing Strategy

### Unit Tests

```python
import pytest
import numpy as np
from neuroprosthetics import KalmanFilter, CSPExtractor, StimulationController

@pytest.fixture
def kalman_filter():
    return KalmanFilter(state_dim=7, observation_dim=64)

class TestKalmanFilter:
    def test_predict_step(self, kalman_filter):
        state_mean = np.zeros(7)
        state_cov = np.eye(7)
        pred_mean, pred_cov = kalman_filter.predict(state_mean, state_cov)
        assert pred_mean.shape == (7,)
        assert pred_cov.shape == (7, 7)

    def test_update_step(self, kalman_filter):
        state_mean = np.zeros(7)
        state_cov = np.eye(7)
        observation = np.random.randn(64)
        updated_mean, updated_cov = kalman_filter.update(state_mean, state_cov, observation)
        assert updated_mean.shape == (7,)
        # Covariance should decrease after update
        assert np.trace(updated_cov) < np.trace(state_cov)
```

### Safety Tests

```python
class TestStimulationSafety:
    def test_charge_limit_enforced(self):
        stim = StimulationController(config.stimulation)
        cmd = StimulationCommand(
            electrode_id=1,
            amplitude_ma=10.0,  # Exceeds limit
            pulse_width_us=200,
            frequency_hz=100
        )
        result = stim.validate_command(cmd)
        assert not result.valid
        assert "charge_limit_exceeded" in result.errors

    def test_impedance_check(self):
        stim = StimulationController(config.stimulation)
        stim.set_impedance(1, 8000)  # > 5kΩ
        cmd = StimulationCommand(electrode_id=1, ...)
        result = stim.validate_command(cmd)
        assert not result.valid
        assert "high_impedance" in result.errors
```

### Hardware-in-the-Loop Tests

```python
@pytest.mark.hardware
class TestHardwareIntegration:
    def test_neural_acquisition(self):
        device = NeuralInterface(config.device)
        data = device.acquire(duration_sec=1.0)
        assert data.shape == (1024, 30000)  # channels × samples
        assert np.max(np.abs(data)) < 500  # Within physiological range

    def test_stimulation_delivery(self):
        stim = StimulatorInterface(config.stimulation)
        result = stim.deliver_pulse(
            electrode_id=0,
            amplitude_ma=1.5,
            pulse_width_us=200
        )
        assert result.delivered
        assert result.measured_current > 1.0
```

---

## Versioning & Migration

### Device Firmware Versioning

| Version | Changes | Breaking | Required Migration |
|---------|---------|----------|-------------------|
| 2.1.0 | New electrode support | No | None |
| 2.0.0 | New communication protocol | Yes | Re-pair device |
| 1.5.0 | Enhanced safety interlock | No | Firmware update |
| 1.0.0 | Initial release | N/A | N/A |

### Migration Scripts

```python
from neuroprosthetics.migration import DeviceMigrator, Step

migrator = DeviceMigrator(
    from_version="1.5.0",
    to_version="2.0.0",
    steps=[
        Step(
            id="protocol_upgrade",
            description="Upgrade communication protocol to v2",
            forward=lambda device: upgrade_protocol_v1_to_v2(device),
            backward=lambda device: downgrade_protocol_v2_to_v1(device),
        ),
        Step(
            id="config_migration",
            description="Migrate configuration format",
            forward=lambda cfg: migrate_config_v1_to_v2(cfg),
            backward=lambda cfg: migrate_config_v2_to_v1(cfg),
        ),
    ]
)
```

---

## Glossary

| Term | Definition |
|------|-----------|
| BCI | Brain-Computer Interface — system that acquires and decodes neural signals |
| Biphasic Stimulation | Two-phase pulse (cathodic + anodic) to maintain charge balance |
| Common Average Reference | Spatial filter that re-references signals to the average of all channels |
| CSP | Common Spatial Pattern — spatial filter for discriminating neural states |
| ECoG | Electrocorticography — recording from electrodes on the cortical surface |
| Impedance | Electrical resistance between electrode and tissue (normal: 0.5-5 kΩ) |
| Kalman Filter | Recursive Bayesian estimator for tracking latent neural states |
| LFP | Local Field Potential — aggregate neural activity from a local population |
| Motor Imagery | Mental rehearsal of movement used as BCI control signal |
| Charge Density | Charge per unit area at electrode surface (safe limit: ~30 μC/cm²) |
| Utah Array | Microelectrode array for intracortical recording (96 channels typical) |
| Neural Decoding | Converting neural activity into intended movement or command |
| Neuroprosthesis | Device that replaces or augments lost neural function |
| Closed-Loop | System where stimulation is driven by real-time neural feedback |
| Safety Interlock | Hardware mechanism that prevents excessive stimulation |

---

## Changelog

### v2.1.0 (2026-04-01)
- Added 1024-channel recording support
- New adaptive stimulation algorithms
- Real-time impedance monitoring dashboard
- FHIR R4 integration for clinical data exchange
- BIDS export format support

### v2.0.0 (2025-11-15)
- Major protocol upgrade (breaking change)
- TLS 1.3 encryption for all device communication
- Role-based access control for clinical operations
- Hardware safety interlock v2

### v1.5.0 (2025-06-01)
- Enhanced artifact rejection (adaptive ICA)
- Improved Kalman filter with online adaptation
- Battery optimization for implantable devices

### v1.0.0 (2025-01-15)
- Initial release
- Basic BCI recording and stimulation
- Kalman filter decoder
- CSP feature extraction

---

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/neuroprosthetics.git
cd neuroprosthetics
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,hardware]"

# Run unit tests (no hardware)
pytest tests/unit/ -v

# Run hardware-in-the-loop tests
pytest tests/hardware/ -v --hardware

# Lint
ruff check neuroprosthetics/
```

### Code Standards

- **Safety-critical code** must have 100% unit test coverage
- All public APIs must have type hints
- All safety-related changes require code review by 2 reviewers
- Hardware interaction code must have corresponding mock tests
- Documentation required for all clinical-facing features

### Commit Convention

```
feat(stim): add adaptive stimulation amplitude
fix(decoder): correct Kalman filter covariance update
safety(impedance): add impedance monitoring threshold
docs(clinical): update FHIR integration guide
test(safety): add charge limit unit tests
```

---

## License

MIT License

Copyright (c) 2026 Neuroprosthetics Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

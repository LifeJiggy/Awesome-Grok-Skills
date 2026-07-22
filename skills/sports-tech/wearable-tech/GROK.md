---
name: "wearable-tech"
category: "sports-tech"
version: "1.0.0"
tags: ["sports-tech", "wearable-tech", "imu-sensors", "gps-tracking", "biometrics"]
---

# Wearable Technology — Sensor Fusion, GPS Tracking & Biometric Analytics

## Overview

Wearable technology in sports represents the fastest-growing segment of athletic performance monitoring, projecting to exceed $6.2 billion by 2027. This module provides a comprehensive software stack for processing data from body-worn sensors — including inertial measurement units (IMUs), optical heart rate monitors, GPS/GNSS receivers, and barometric altimeters — into actionable athletic insights. The module bridges the gap between raw sensor telemetry and the performance analytics consumed by coaching and medical staff.

The sensor fusion pipeline combines data from multiple complementary sensors using Extended Kalman Filters (EKF) and complementary filter architectures. GPS provides absolute position but suffers from multipath indoors and 1-2 Hz update rates; accelerometers provide high-frequency (100-1000 Hz) motion data but drift over time; gyroscopes capture angular velocity for orientation estimation. By fusing these modalities, the module produces a unified, high-fidelity运动轨迹 that remains accurate across indoor and outdoor environments.

Beyond trajectory reconstruction, the module includes dedicated analysis pipelines for heart rate variability (HRV) — a key indicator of autonomic nervous system status and recovery readiness — and accelerometer-based activity classification using convolutional neural networks trained on labeled sport-specific movement datasets. The biometric synchronization layer handles time alignment of multi-sensor data streams using PTP (Precision Time Protocol) and NTP fallback, ensuring that heart rate, position, and motion data are temporally coherent even when sampled at different rates.

The battery optimization subsystem models energy consumption across sensor configurations (GPS polling rate, accelerometer sample rate, BLE transmission interval) to maximize deployment duration while maintaining measurement fidelity. This is critical for multi-day tournament tracking where recharging between matches is impractical.

## Core Capabilities

- **Multi-Sensor Fusion (EKF)**: Extended Kalman Filter architecture fusing GPS, accelerometer, gyroscope, and magnetometer data into a unified pose and trajectory estimate at 100 Hz output rate
- **Heart Rate Variability Analysis**: Time-domain (RMSSD, SDNN, pNN50) and frequency-domain (LF/HF ratio, total power) HRV metrics with artifact correction and ectopic beat removal
- **GPS Accuracy Assessment**: Dilution of precision analysis, multipath detection, and position error estimation with HDOP/VDOP/TDOP breakdowns and satellite geometry scoring
- **Accelerometer Activity Classification**: CNN-based movement classifier distinguishing running, sprinting, walking, jumping, cutting, tackling, and resting states from triaxial accelerometer streams
- **Real-Time Streaming Protocol**: WebSocket and MQTT-based data ingestion pipeline supporting 100+ simultaneous sensor streams with sub-50ms end-to-end latency
- **BLE Sensor Network Management**: Bluetooth Low Energy mesh coordinator handling device discovery, pairing, OTA firmware updates, and connection management for up to 64 sensors per gateway
- **Battery Optimization Engine**: Multi-objective optimization balancing sensor accuracy, sampling rate, and power draw to maximize deployment lifetime under configurable accuracy constraints
- **Biometric Data Synchronization**: Time-alignment engine using PTP/NTP with interpolation and resampling to produce coherent multi-modal data streams from heterogeneous sensor clocks

## Usage Examples

### Sensor Fusion Pipeline

```python
from wearable_tech import SensorFusionEngine, SensorConfig

# Configure the fusion engine
config = SensorConfig(
    gps_rate_hz=10,
    accel_rate_hz=100,
    gyro_rate_hz=100,
    mag_rate_hz=25,
    fusion_rate_hz=100,
    gps_position_noise=2.5,    # meters
    accel_noise=0.05,          # m/s^2
    gyro_noise=0.01,           # rad/s
)

engine = SensorFusionEngine(config)

# Process a session of raw sensor data
session = engine.process_session(
    gps_data="session_2024_01_raw_gps.csv",
    imu_data="session_2024_01_raw_imu.bin",
    output_format="parquet",
)

# Access fused trajectory
for point in session.trajectory:
    print(f"t={point.timestamp:.3f}s | "
          f"pos=({point.x:.2f}, {point.y:.2f}, {point.z:.2f}) | "
          f"vel={point.velocity:.2f} m/s | "
          f"heading={point.heading:.1f}°")
```

### Heart Rate Variability Monitoring

```python
from wearable_tech import HRVAnalyzer, HRVWindow

analyzer = HRVAnalyzer(
    sampling_rate_hz=1,
    artifact_correction=True,
    interpolation_rate_hz=4,
)

# Analyze a 5-minute HRV window during recovery
window = HRVWindow(
    heart_rate_series=recovery_hr_data,
    start_time=0,
    duration_seconds=300,
    context="post_match_recovery",
)

hrv_result = analyzer.analyze(window)

# Check autonomic balance
print(f"RMSSD: {hrv_result.rmssd:.1f} ms")
print(f"SDNN: {hrv_result.sdnn:.1f} ms")
print(f"LF/HF ratio: {hrv_result.lf_hf_ratio:.2f}")
print(f"Recovery index: {hrv_result.recovery_index:.2f}")

# Compare against baseline
readiness = analyzer.compare_to_baseline(hrv_result, player_baseline)
print(f"Readiness score: {readiness.score:.0f}/100")
print(f"Status: {readiness.status}")  # READY, CAUTION, NOT_READY
```

### Activity Classification

```python
from wearable_tech import ActivityClassifier, MovementSegment

classifier = ActivityClassifier(
    model_path="models/sport_classifier_v3.onnx",
    confidence_threshold=0.85,
    window_size_ms=500,
    overlap=0.5,
)

# Classify movements from accelerometer data
segments = classifier.classify(
    accel_stream=accel_data,
    sample_rate_hz=100,
)

for seg in segments:
    print(f"[{seg.start_ms:.0f}-{seg.end_ms:.0f}ms] "
          f"Activity: {seg.activity_type.value:15s} | "
          f"Confidence: {seg.confidence:.2f} | "
          f"Peak accel: {seg.peak_acceleration:.1f} g")

# Get session summary
summary = classifier.session_summary(segments)
print(f"Sprint count: {summary.sprint_count}")
print(f"Total distance at >25 km/h: {summary.high_speed_distance_m:.0f} m")
print(f"Acceleration events: {summary.accel_event_count}")
print(f"Deceleration events: {summary.decel_event_count}")
```

### Battery Optimization

```python
from wearable_tech import BatteryOptimizer, PowerProfile

optimizer = BatteryOptimizer(
    battery_capacity_mah=350,
    power_profiles=PowerProfile.load_default("catapult_one_v4"),
)

# Find optimal configuration for 2-hour match tracking
optimal = optimizer.optimize(
    duration_hours=2.0,
    required_accuracy="high",       # GPS: <=2m error, IMU: <=1% drift
    constraints={
        "min_gps_rate_hz": 10,
        "min_accel_rate_hz": 100,
        "ble_transmit_interval_ms": 1000,
    },
)

print(f"Optimal GPS rate: {optimal.gps_rate_hz} Hz")
print(f"Optimal accel rate: {optimal.accel_rate_hz} Hz")
print(f"Estimated battery life: {optimal.estimated_battery_hours:.1f} hours")
print(f"Estimated position accuracy: {optimal.estimated_accuracy_m:.2f} m")
print(f"Power budget: {optimal.total_power_mw:.1f} mW")
```

## Best Practices

1. **Calibrate sensors before each deployment** — magnetometer hard/soft iron calibration and accelerometer bias correction should be performed with a standardized warm-up routine. Uncalibrated sensors can introduce 5-15% trajectory error.

2. **Use complementary filtering for mixed indoor/outdoor sessions** — GPS reliability degrades indoors; fall back to IMU dead-reckoning with zero-velocity updates (ZUPT) when HDOP exceeds threshold or satellite count drops below 4.

3. **Apply Butterworth low-pass filtering to HRV signals** — raw optical heart rate signals contain motion artifacts that corrupt HRV metrics. Use a 0.5 Hz cutoff Butterworth filter or Pan-Tompkins peak detection before HRV computation.

4. **Synchronize clocks before multi-sensor deployments** — even 100ms of clock drift between GPS and IMU produces 2.5m of velocity error at sprint speeds. Implement PTP synchronization or use a common time source.

5. **Set confidence thresholds for activity classification** — low-confidence classifications (<0.85) should be flagged as "uncertain" rather than assigned to a category. False sprint detections can mislead training load calculations.

6. **Model battery drain under realistic conditions** — lab-measured power consumption differs from field conditions due to temperature effects on battery chemistry and variable GPS signal acquisition power. Add 15-20% safety margin.

7. **Store raw sensor data alongside processed outputs** — derived metrics may need recomputation as algorithms improve. Retaining the original streams enables retrospective analysis without re-wearing sensors.

8. **Implement graceful degradation** — when a sensor fails mid-session (GPS dropout, HR signal loss), the system should continue operating with reduced modalities and clearly indicate which metrics are estimated vs. directly measured.

## Sensor Specifications

The module supports the following sensor configurations commonly deployed in professional sports:

| Sensor Type | Sample Rate | Resolution | Typical Accuracy |
|---|---|---|---|
| GPS/GNSS | 1-20 Hz | 0.1m | 1-3m (open field) |
| Accelerometer | 25-1000 Hz | 16-bit | ±0.05 m/s² |
| Gyroscope | 25-1000 Hz | 16-bit | ±0.01 rad/s |
| Magnetometer | 10-100 Hz | 14-bit | ±1° heading |
| Optical HR | 1 Hz | 1 bpm | ±3 bpm |
| Barometric Altimeter | 1-10 Hz | 0.01 hPa | ±0.5m vertical |

The sensor fusion engine handles heterogeneous sample rates by interpolating all inputs to a common output rate (configurable, default 100 Hz). This ensures temporal coherence across modalities even when hardware specifications differ.

## BLE Sensor Network Architecture

Professional deployments typically involve 22+ body-worn sensors (one per player plus ball sensor) coordinated through BLE gateways:

- **Gateway Placement**: 4-6 BLE gateways per pitch, positioned at corners and halfway line, providing overlapping coverage zones
- **Mesh Topology**: Sensors form a BLE mesh using the gateway nodes as relays, ensuring connectivity even when players move to the edges of coverage
- **Throughput**: Each gateway supports up to 16 simultaneous sensor connections at 1 Hz update rate, or 8 sensors at 10 Hz
- **Latency**: End-to-end data delivery from sensor to server averages 45ms (95th percentile: 120ms) through the BLE mesh

The network manager handles dynamic connection management as players move between gateway coverage zones, with handoff occurring in <50ms to prevent data gaps.

## Data Quality Assurance

The module implements multi-stage data quality checks:

1. **Sensor Health Check**: Before session start, verify all sensors report valid calibration data, battery level >20%, and firmware version compatibility
2. **Signal Quality Monitoring**: During session, monitor GPS HDOP, accelerometer saturation, HR signal quality index, and BLE packet loss rate in real-time
3. **Anomaly Detection**: Post-session, flag statistical outliers in velocity, acceleration, and heart rate data that may indicate sensor malfunction rather than genuine athletic performance
4. **Gap Filling**: For short GPS dropouts (<5s), interpolate position using IMU dead-reckoning; for longer gaps, mark affected metrics as estimated with reduced confidence

## Related Modules

- [performance-analytics](../performance-analytics/GROK.md) — Consumes wearable-derived sprint velocity, distance covered, and workload metrics for player evaluation
- [injury-prevention](../injury-prevention/GROK.md) — Uses IMU-derived biomechanical data and HRV recovery metrics for injury risk scoring
- [game-strategy](../game-strategy/GROK.md) — Incorporates real-time positioning data for formation analysis and tactical adjustments
- [fan-engagement](../fan-engagement/GROK.md) — Streams live player tracking data for second-screen fan experiences

## Advanced Configuration

The wearable technology module supports extensive configuration through environment variables, YAML files, and runtime API calls. Proper configuration is critical for sensor fusion accuracy and battery optimization.

### Sensor Fusion Configuration

```yaml
# config/sensor_fusion.yaml
fusion_engine:
  algorithm: "extended_kalman_filter"
  output_rate_hz: 100
  prediction_horizon_ms: 50

  gps:
    default_rate_hz: 10
    position_noise_m: 2.5
    velocity_noise_mps: 0.5
    hdop_threshold: 3.0
    min_satellites: 4
    multipath_detection: true
    multipath_threshold_m: 5.0

  accelerometer:
    default_rate_hz: 100
    noise_mps2: 0.05
    bias_correction: true
    saturation_threshold_g: 16.0
    low_pass_cutoff_hz: 20.0

  gyroscope:
    default_rate_hz: 100
    noise_rads: 0.01
    bias_correction: true
    drift_correction: true

  magnetometer:
    default_rate_hz: 25
    hard_iron_correction: true
    soft_iron_correction: true
    declination_degrees: 0.0  # set per deployment location

  complementary_filter:
    enabled: false
    gps_weight: 0.1
    imu_weight: 0.9
    gps_dropout_retimeout_s: 5.0

  zupt:
    enabled: true
    velocity_threshold_mps: 0.1
    window_size_samples: 50
```

### Heart Rate Analysis Configuration

```yaml
hrv_analysis:
  sampling_rate_hz: 1
  interpolation_rate_hz: 4
  artifact_correction: "adaptive_median"
  ectopic_removal: true
  ectopic_threshold_ms: 200

  time_domain:
    enabled: true
    metrics: ["rmssd", "sdnn", "pnn50", "sd1", "sd2"]

  frequency_domain:
    enabled: true
    method: "lomb_scargle"
    vlf_range_hz: [0.003, 0.04]
    lf_range_hz: [0.04, 0.15]
    hf_range_hz: [0.15, 0.4]
    detrending: "polynomial_order_2"

  nonlinear:
    enabled: true
    methods: ["poincare", "sample_entropy", "dfa"]

  baselines:
    update_frequency_days: 7
    min_sessions: 5
    outlier_rejection_std: 2.0
```

### Activity Classification Configuration

```yaml
activity_classifier:
  model_path: "models/sport_classifier_v3.onnx"
  confidence_threshold: 0.85
  window_size_ms: 500
  overlap: 0.5
  label_smoothing: 0.1

  activities:
    - name: "standing"
      min_duration_ms: 1000
    - name: "walking"
      min_duration_ms: 500
    - name: "jogging"
      min_duration_ms: 500
    - name: "running"
      min_duration_ms: 300
      min_peak_accel_g: 1.2
    - name: "sprinting"
      min_duration_ms: 200
      min_peak_accel_g: 2.5
    - name: "jumping"
      min_duration_ms: 200
      min_peak_accel_g: 3.0
    - name: "cutting"
      min_duration_ms: 200
      min_peak_accel_g: 2.0
    - name: "tackling"
      min_duration_ms: 300
      min_peak_accel_g: 4.0
    - name: "resting"
      min_duration_ms: 5000

  post_processing:
    merge_same_class: true
    min_gap_to_merge_ms: 200
    median_filter_window: 3
```

## Architecture Patterns

The wearable tech module employs several architectural patterns to handle the complexity of multi-sensor data processing and real-time streaming.

### Producer-Consumer Pipeline

Sensor data flows through a multi-stage pipeline where each stage is a producer-consumer pair:

```
Sensor Hardware
      │
      ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Ingestion  │───▶│    Fusion    │───▶│  Analysis   │
│   (Producer) │    │  (Consumer)  │    │  (Consumer) │
└─────────────┘    └──────┬──────┘    └──────┬──────┘
                          │                   │
                          ▼                   ▼
                   ┌─────────────┐    ┌─────────────┐
                   │   Storage    │    │   Output    │
                   │   (Sink)     │    │   (Sink)    │
                   └─────────────┘    └─────────────┘
```

### Ring Buffer for Real-Time Processing

```python
import threading
from collections import deque

class SensorRingBuffer:
    def __init__(self, capacity: int = 10000):
        self.buffer = deque(maxlen=capacity)
        self.lock = threading.Lock()
        self.not_empty = threading.Event()
        self.not_full = threading.Event()
        self.not_full.set()

    def put(self, sample: SensorSample, timeout: float = 1.0):
        with self.lock:
            if not self.not_full.wait(timeout):
                raise BufferOverflowError("Sensor buffer full")
            self.buffer.append(sample)
            self.not_empty.set()

    def get(self, timeout: float = 1.0) -> SensorSample:
        with self.lock:
            if not self.not_empty.wait(timeout):
                raise BufferTimeoutError("No sensor data available")
            sample = self.buffer.popleft()
            if len(self.buffer) < self.buffer.maxlen:
                self.not_full.set()
            return sample

    def get_batch(self, count: int) -> list:
        with self.lock:
            batch = []
            while len(self.buffer) > 0 and len(batch) < count:
                batch.append(self.buffer.popleft())
            return batch
```

### Observer Pattern for Sensor Events

```python
from typing import Callable, Dict, List

class SensorEventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def publish(self, event_type: str, data: dict):
        for callback in self._subscribers.get(event_type, []):
            callback(data)

# Usage
event_bus = SensorEventBus()
event_bus.subscribe("gps_dropout", handle_gps_dropout)
event_bus.subscribe("hr_spike", handle_hr_spike)
event_bus.subscribe("battery_low", handle_battery_warning)
```

### State Machine for Session Management

```python
from enum import Enum

class SessionState(Enum):
    IDLE = "idle"
    CONFIGURING = "configuring"
    CALIBRATING = "calibrating"
    STREAMING = "streaming"
    PAUSED = "paused"
    STOPPING = "stopping"
    ERROR = "error"

class SessionStateMachine:
    TRANSITIONS = {
        SessionState.IDLE: [SessionState.CONFIGURING],
        SessionState.CONFIGURING: [SessionState.CALIBRATING, SessionState.ERROR],
        SessionState.CALIBRATING: [SessionState.STREAMING, SessionState.ERROR],
        SessionState.STREAMING: [SessionState.PAUSED, SessionState.STOPPING, SessionState.ERROR],
        SessionState.PAUSED: [SessionState.STREAMING, SessionState.STOPPING],
        SessionState.STOPPING: [SessionState.IDLE],
        SessionState.ERROR: [SessionState.IDLE],
    }

    def __init__(self):
        self.state = SessionState.IDLE

    def transition(self, new_state: SessionState) -> bool:
        if new_state in self.TRANSITIONS.get(self.state, []):
            self.state = new_state
            return True
        raise InvalidTransitionError(
            f"Cannot transition from {self.state} to {new_state}"
        )
```

## Integration Guide

### Hardware Integration

```python
from wearable_tech.hardware import SensorManager

manager = SensorManager()

# Discover available sensors
devices = manager.discover(
    protocol="ble",
    timeout_seconds=10,
    filter_by_type=["imu", "hr", "gps"],
)

for device in devices:
    print(f"Found: {device.name} ({device.type}) - {device.mac_address}")
    print(f"  Battery: {device.battery_level}%")
    print(f"  Firmware: {device.firmware_version}")

# Connect and configure
session = manager.create_session(
    devices=devices,
    config=SensorConfig(
        gps_rate_hz=10,
        accel_rate_hz=100,
        gyro_rate_hz=100,
    ),
    sync_method="ptp",
)

session.start()
```

### Cloud Storage Integration

```python
from wearable_tech.storage import CloudUploader

uploader = CloudUploader(
    provider="aws_s3",
    bucket="sensor-data-raw",
    prefix="2024/match_001/",
)

# Upload raw session data
session_data = session.export_raw()
upload_result = uploader.upload(
    data=session_data,
    metadata={
        "player_id": "p_messi_10",
        "match_id": "match_2024_01",
        "session_type": "match",
        "sensor_config": session.config.to_dict(),
    },
    checksum="sha256",
)

print(f"Uploaded: {upload_result.s3_key}")
print(f"Size: {upload_result.size_bytes:,} bytes")
print(f"ETag: {upload_result.etag}")
```

### Real-Time Dashboard Integration

```python
import websocket
import json

class DashboardStreamer:
    def __init__(self, dashboard_url: str, api_key: str):
        self.ws = websocket.create_connection(
            dashboard_url,
            header={"Authorization": f"Bearer {api_key}"}
        )

    def stream_player_data(self, player_id: str, session):
        for sample in session.live_stream():
            payload = {
                "player_id": player_id,
                "timestamp": sample.timestamp,
                "position": {"x": sample.x, "y": sample.y, "z": sample.z},
                "velocity": sample.velocity,
                "heart_rate": sample.heart_rate,
                "acceleration": sample.acceleration,
            }
            self.ws.send(json.dumps(payload))
```

## Performance Optimization

### Parallel Sensor Processing

```python
from concurrent.futures import ThreadPoolExecutor
import multiprocessing as mp

class ParallelFusionProcessor:
    def __init__(self, num_workers: int = None):
        self.num_workers = num_workers or mp.cpu_count()
        self.executor = ThreadPoolExecutor(max_workers=self.num_workers)

    def process_players_batch(self, player_sessions: list) -> list:
        futures = []
        for session in player_sessions:
            future = self.executor.submit(self._process_player, session)
            futures.append(future)

        results = []
        for future in futures:
            results.append(future.result(timeout=30))
        return results
```

### Memory-Mapped Sensor Data

```python
import mmap
import struct

class MappedSensorBuffer:
    def __init__(self, filepath: str, capacity_samples: int = 1000000):
        self.filepath = filepath
        self.sample_size = 48  # bytes per sample
        self.capacity = capacity_samples
        self._setup_mmap()

    def _setup_mmap(self):
        with open(self.filepath, 'wb') as f:
            f.write(b'\x00' * (self.capacity * self.sample_size))

        self.file = open(self.filepath, 'r+b')
        self.mmap = mmap.mmap(self.file.fileno(), 0)

    def write_sample(self, index: int, sample: bytes):
        offset = index * self.sample_size
        self.mmap[offset:offset + self.sample_size] = sample

    def read_sample(self, index: int) -> bytes:
        offset = index * self.sample_size
        return self.mmap[offset:offset + self.sample_size]
```

### GPU-Accelerated Activity Classification

```python
import torch

class GPUActivityClassifier:
    def __init__(self, model_path: str, device: str = "cuda"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.model = torch.jit.load(model_path, map_location=self.device)
        self.model.eval()

    @torch.no_grad()
    def classify_batch(self, accel_batch: torch.Tensor) -> torch.Tensor:
        """
        accel_batch: shape (batch_size, sequence_length, 3)
        Returns: shape (batch_size,) with predicted activity indices
        """
        accel_batch = accel_batch.to(self.device)
        outputs = self.model(accel_batch)
        predictions = torch.argmax(outputs, dim=-1)
        return predictions.cpu()
```

## Security Considerations

### Sensor Data Encryption

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os

class SensorDataEncryption:
    def __init__(self, key: bytes):
        self.key = key  # 256-bit key

    def encrypt_stream(self, raw_data: bytes) -> tuple:
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(raw_data) + encryptor.finalize()
        return iv + encryptor.tag + ciphertext

    def decrypt_stream(self, encrypted_data: bytes) -> bytes:
        iv = encrypted_data[:16]
        tag = encrypted_data[16:32]
        ciphertext = encrypted_data[32:]
        cipher = Cipher(algorithms.AES(self.key), modes.GCM(iv, tag))
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
```

### BLE Security

```python
class SecureBLEConnection:
    def __init__(self, device_mac: str):
        self.mac = device_mac
        self.session_key = None

    def pair_secure(self) -> bool:
        # Numeric comparison pairing
        display_code = self._initiate_pairing()
        user_confirmed = self._display_pairing_code(display_code)
        if user_confirmed:
            self.session_key = self._derive_session_key()
            return True
        return False

    def encrypt_communication(self, data: bytes) -> bytes:
        if self.session_key is None:
            raise SecurityError("Not paired")
        return self._aes_ccm_encrypt(self.session_key, data)
```

## Troubleshooting Guide

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| GPS position jumps | Multipath reflection near buildings | Enable multipath detection; use HDOP threshold filtering |
| HR signal dropout | Poor sensor contact or motion artifact | Check sensor placement; enable artifact correction |
| BLE disconnection | Range exceeded or interference | Add gateway nodes; reduce transmission power to limit range |
| Fusion drift | IMU bias accumulation during GPS outage | Enable ZUPT; recalibrate sensors before session |
| Low battery warning | High sampling rate configuration | Reduce GPS rate to 5 Hz; decrease accel rate to 50 Hz |
| Clock desynchronization | PTP master failure | Enable NTP fallback; verify master clock health |

### Diagnostic Tools

```python
from wearable_tech.diagnostics import SensorDiagnostics

diag = SensorDiagnostics(session_data)

# Run full diagnostic suite
report = diag.run_full_diagnostic()
print(f"GPS Health: {report.gps_health_score:.0f}/100")
print(f"  HDOP average: {report.avg_hdop:.1f}")
print(f"  Satellite count: {report.avg_satellites:.0f}")
print(f"  Dropouts: {report.gps_dropout_count}")
print(f"IMU Health: {report.imu_health_score:.0f}/100")
print(f"  Accel bias: {report.accel_bias:.4f} m/s²")
print(f"  Gyro drift: {report.gyro_drift:.4f} rad/s")
print(f"HR Health: {report.hr_health_score:.0f}/100")
print(f"  Signal quality: {report.hr_signal_quality:.1%}")
print(f"  Artifact rate: {report.artifact_rate:.1%}")
```

## API Reference

### Core Classes

| Class | Description | Key Methods |
|-------|-------------|-------------|
| `SensorFusionEngine` | Multi-sensor fusion processor | `process_session()`, `calibrate()`, `get_trajectory()` |
| `HRVAnalyzer` | Heart rate variability analysis | `analyze()`, `compare_to_baseline()`, `compute_recovery_index()` |
| `ActivityClassifier` | CNN-based movement classifier | `classify()`, `session_summary()`, `classify_streaming()` |
| `BatteryOptimizer` | Power optimization engine | `optimize()`, `estimate_battery_life()`, `get_power_profile()` |
| `SensorNetworkManager` | BLE mesh coordinator | `discover()`, `connect()`, `ota_update()` |
| `DataSynchronizer` | Multi-sensor time alignment | `align()`, `resample()`, `interpolate()` |

### Configuration Classes

| Class | Description | Key Fields |
|-------|-------------|------------|
| `SensorConfig` | Sensor sampling configuration | `gps_rate_hz, accel_rate_hz, gyro_rate_hz, mag_rate_hz` |
| `FusionConfig` | Fusion algorithm parameters | `algorithm, output_rate_hz, noise_parameters` |
| `HRVConfig` | HRV analysis settings | `sampling_rate_hz, interpolation_rate_hz, enabled_metrics` |
| `SessionConfig` | Session management settings | `duration_minutes, sync_method, power_mode` |

## Data Models

### Sensor Data Schema

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│    Sessions      │     │  Sensor Samples   │     │    Players      │
├─────────────────┤     ├──────────────────┤     ├─────────────────┤
│ session_id (PK) │────<│ sample_id (PK)   │>────│ player_id (PK)  │
│ player_id (FK)  │     │ session_id (FK)  │     │ name            │
│ match_id        │     │ timestamp_ns     │     │ team_id         │
│ start_time      │     │ sensor_type      │     │ position        │
│ end_time        │     │ accel_x, y, z    │     │ sensor_config   │
│ device_ids      │     │ gyro_x, y, z     │     │ baseline_hrv    │
│ config_snapshot │     │ mag_x, y, z      │     │ baseline_load   │
│ raw_data_path   │     │ gps_lat, lon, alt │     │ created_at      │
│ processed_path  │     │ heart_rate        │     └─────────────────┘
└─────────────────┘     │ battery_level     │
                        └──────────────────┘
```

### Fused Trajectory Schema

```json
{
  "trajectory_point": {
    "timestamp_ms": "int64",
    "position": {
      "x": "float64 (meters from origin)",
      "y": "float64",
      "z": "float64"
    },
    "velocity": {
      "vx": "float64 (m/s)",
      "vy": "float64",
      "vz": "float64",
      "magnitude": "float64"
    },
    "acceleration": {
      "ax": "float64 (m/s²)",
      "ay": "float64",
      "az": "float64",
      "magnitude": "float64"
    },
    "orientation": {
      "heading": "float64 (degrees)",
      "pitch": "float64",
      "roll": "float64"
    },
    "quality": {
      "gps_available": "bool",
      "hdop": "float64",
      "satellites": "int",
      "fusion_confidence": "float64 (0-1)"
    }
  }
}
```

## Deployment Guide

### Edge Computing Deployment

```dockerfile
# Dockerfile for edge gateway
FROM arm64v8/python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    bluetooth \
    libbluetooth-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Enable Bluetooth permissions
RUN usermod -a -G bluetooth appuser

USER appuser

CMD ["python", "-m", "wearable_tech.gateway", \
     "--config", "/etc/wearable/config.yaml"]
```

### Cloud Processing Deployment

```yaml
# docker-compose.yaml
version: '3.8'

services:
  sensor-ingestion:
    build: .
    command: python -m wearable_tech.ingestion
    environment:
      - KAFKA_BROKERS=kafka:9092
      - REDIS_URL=redis://redis:6379
    deploy:
      replicas: 3
      resources:
        limits:
          memory: 512M
          cpus: '0.5'

  fusion-processor:
    build: .
    command: python -m wearable_tech.fusion
    environment:
      - KAFKA_BROKERS=kafka:9092
      - POSTGRES_URL=postgresql://user:pass@postgres:5432/sensordb
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 2G
          cpus: '2.0'

  hr-analyzer:
    build: .
    command: python -m wearable_tech.hrv_analysis
    environment:
      - KAFKA_BROKERS=kafka:9092
      - REDIS_URL=redis://redis:6379
    deploy:
      replicas: 2
      resources:
        limits:
          memory: 1G
          cpus: '1.0'
```

## Monitoring & Observability

### Sensor Health Metrics

```python
from prometheus_client import Gauge, Counter, Histogram

SENSOR_BATTERY_LEVEL = Gauge(
    'sensor_battery_level_percent',
    'Current battery level of sensor',
    ['player_id', 'sensor_type']
)

SENSOR_DATA_RATE = Gauge(
    'sensor_data_rate_hz',
    'Actual data rate from sensor',
    ['player_id', 'sensor_type']
)

BLE_PACKET_LOSS = Counter(
    'ble_packet_loss_total',
    'Total BLE packets lost',
    ['player_id']
)

GPS_HDOP = Gauge(
    'gps_hdop_value',
    'GPS horizontal dilution of precision',
    ['player_id']
)

FUSION_LATENCY = Histogram(
    'fusion_processing_latency_seconds',
    'End-to-end fusion processing latency',
    ['sensor_count'],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1]
)
```

### Alerting Configuration

```yaml
alerts:
  - name: SensorBatteryLow
    condition: sensor_battery_level_percent < 20
    severity: warning
    message: "Sensor battery low for {player_id}"

  - name: GPSHDOPHigh
    condition: gps_hdop_value > 4.0
    severity: warning
    message: "GPS accuracy degraded for {player_id}"

  - name: SensorOffline
    condition: sensor_data_rate_hz == 0
    severity: critical
    for: 30s
    message: "Sensor offline for {player_id}"

  - name: FusionDrift
    condition: fusion_position_error_m > 5.0
    severity: critical
    message: "Fusion position error exceeds threshold"
```

## Testing Strategy

### Unit Tests

```python
import pytest
import numpy as np
from wearable_tech import SensorFusionEngine, SensorConfig

class TestSensorFusion:
    def setup_method(self):
        self.config = SensorConfig(
            gps_rate_hz=10,
            accel_rate_hz=100,
            gyro_rate_hz=100,
        )
        self.engine = SensorFusionEngine(self.config)

    def test_fusion_output_rate(self):
        trajectory = self.engine.process_session(
            gps_data="test_gps.csv",
            imu_data="test_imu.bin",
        )
        sample_times = [p.timestamp for p in trajectory]
        intervals = np.diff(sample_times)
        avg_interval = np.mean(intervals)
        expected_interval = 1.0 / self.config.fusion_rate_hz
        assert abs(avg_interval - expected_interval) < 0.001

    def test_position_smoothness(self):
        trajectory = self.engine.process_session(
            gps_data="test_gps.csv",
            imu_data="test_imu.bin",
        )
        positions = [(p.x, p.y) for p in trajectory]
        velocity_jumps = []
        for i in range(1, len(positions)):
            dx = positions[i][0] - positions[i-1][0]
            dy = positions[i][1] - positions[i-1][1]
            velocity_jumps.append(np.sqrt(dx**2 + dy**2))
        assert np.std(velocity_jumps) < 0.5
```

### Integration Tests

```python
class TestHRVIntegration:
    def test_hrv_analysis_pipeline(self, sample_hr_data):
        analyzer = HRVAnalyzer(sampling_rate_hz=1)
        window = HRVWindow(
            heart_rate_series=sample_hr_data,
            start_time=0,
            duration_seconds=300,
        )
        result = analyzer.analyze(window)
        assert result.rmssd > 0
        assert result.sdnn > 0
        assert 0 < result.lf_hf_ratio < 10
```

## Versioning & Migration

### Sensor Firmware Versioning

```python
class FirmwareVersionManager:
    def __init__(self, device_manager):
        self.devices = device_manager

    def check_compatibility(self, device_mac: str, min_version: str) -> bool:
        current = self.devices.get_firmware_version(device_mac)
        return self._compare_versions(current, min_version) >= 0

    def ota_update(self, device_mac: str, firmware_path: str) -> bool:
        if not self.check_compatibility(device_mac, "2.0.0"):
            raise FirmwareCompatibilityError("Device firmware too old")
        return self.devices.ota_update(device_mac, firmware_path)
```

### Data Schema Migration

```sql
-- Migration: Add barometric altitude support
ALTER TABLE sensor_samples
ADD COLUMN barometric_altitude_m DECIMAL(8,3);

ALTER TABLE sensor_samples
ADD COLUMN pressure_hpa DECIMAL(8,2);

CREATE INDEX idx_samples_pressure
ON sensor_samples (pressure_hpa)
WHERE pressure_hpa IS NOT NULL;
```

## Glossary

| Term | Definition |
|------|------------|
| **IMU** | Inertial Measurement Unit — combines accelerometer, gyroscope, and sometimes magnetometer |
| **EKF** | Extended Kalman Filter — recursive estimator for nonlinear dynamic systems |
| **ZUPT** | Zero Velocity Update — technique to correct IMU drift when sensor is stationary |
| **PTP** | Precision Time Protocol (IEEE 1588) — sub-microsecond clock synchronization |
| **HDOP** | Horizontal Dilution of Precision — GPS accuracy metric (lower is better) |
| **BLE** | Bluetooth Low Energy — wireless protocol for low-power sensor communication |
| **RMSSD** | Root Mean Square of Successive Differences — time-domain HRV metric |
| **LF/HF Ratio** | Low Frequency to High Frequency ratio — autonomic balance indicator |
| **Gait Cycle** | Complete sequence of stance and swing phases in one step |
| **ECG** | Electrocardiogram — electrical recording of heart activity |
| **EMG** | Electromyography — electrical recording of muscle activity |
| **RSSI** | Received Signal Strength Indicator — BLE signal quality metric |
| **Mesh Network** | Network topology where nodes relay data to extend coverage |
| **OTA** | Over-The-Air — firmware update method without physical connection |
| **GCS** | Global Coordinate System — unified reference frame for multi-sensor fusion |

## Changelog

### Version 1.0.0 (2024-01-15)

- Initial release with multi-sensor fusion engine
- Extended Kalman Filter implementation for GPS/IMU fusion
- HRV analysis with time-domain and frequency-domain metrics
- Activity classification using CNN model
- BLE sensor network management

### Version 1.1.0 (2024-04-01)

- Added battery optimization engine
- Implemented PTP/NTP time synchronization
- Enhanced magnetometer calibration with hard/soft iron correction
- Added complementary filter as alternative to EKF

### Version 1.2.0 (2024-07-15)

- GPU-accelerated activity classification
- Real-time streaming via WebSocket and MQTT
- Enhanced data quality assurance pipeline
- Added nonlinear HRV metrics (Poincare, sample entropy)

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/sports-tech/wearable-tech.git
cd wearable-tech
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Run sensor simulation tests
pytest tests/ -v --cov=wearable_tech

# Lint and format
ruff check .
ruff format .
```

### Hardware Testing

```bash
# Run BLE discovery test
python -m wearable_tech.tools.scan_ble --duration 10

# Run sensor validation
python -m wearable_tech.tools.validate_sensor --config test_config.yaml
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

Copyright (c) 2024 Sports Tech Analytics

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

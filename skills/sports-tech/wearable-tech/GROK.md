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

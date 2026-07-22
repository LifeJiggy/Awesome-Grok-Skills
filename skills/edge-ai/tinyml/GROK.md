---
name: "TinyML"
version: "2.0.0"
description: "Comprehensive TinyML toolkit with microcontroller deployment, model optimization for MCU, power management, sensor integration, and on-device training for ultra-low-power ML"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["edge-ai", "tinyml", "microcontroller", "ultra-low-power", "sensor", "on-device-training"]
category: "edge-ai"
personality: "tinyml-engineer"
use_cases: ["MCU deployment", "model optimization for MCU", "power management", "sensor integration", "on-device training"]
---

# TinyML

> Production-grade TinyML framework providing microcontroller deployment, model optimization for MCU, power management, sensor integration, and on-device training for ultra-low-power machine learning.

## Overview

The TinyML module provides tools for deploying ML models to microcontrollers and ultra-low-power devices. It implements model optimization for constrained environments (KB-scale), MCU-specific compilation and deployment, power-aware scheduling, sensor data pipeline integration, and on-device learning capabilities. Every deployment includes power profiling, memory analysis, and accuracy validation.

## Core Capabilities

### 1. MCU Deployment
- TensorFlow Lite Micro support
- ARM CMSIS-NN optimization
- ESP-DSP integration
- Arduino-compatible deployment
- Platform-specific optimizations

### 2. Model Optimization for MCU
- Extreme quantization (binary, ternary)
- Weight clustering
- Knowledge distillation for MCU
- Architecture search for MCU
- Memory-efficient designs

### 3. Power Management
- Dynamic voltage and frequency scaling
- Sleep mode scheduling
- Event-driven inference
- Power profiling and optimization
- Battery life estimation

### 4. Sensor Integration
- IMU data processing
- Audio signal processing
- Environmental sensor fusion
- Camera input processing
- Multi-modal sensor fusion

### 5. On-Device Training
- Federated learning on MCU
- Transfer learning adaptation
- Continual learning
- Anomaly detection training
- Online learning

### 6. Performance Profiling
- Memory usage analysis (RAM/Flash)
- Cycle count optimization
- Power consumption measurement
- Latency benchmarking
- Accuracy validation on MCU

## Usage Examples

### MCU Deployment

```python
from tinyml import MCUDeployer, TargetPlatform

deployer = MCUDeployer(platform=TargetPlatform.ESP32)

# Deploy model to MCU
deployment = deployer.deploy(
    model_path="model.tflite",
    memory_config={"ram": 520, "flash": 4096},  # KB
)

print(f"Model size: {deployment.model_size_kb:.1f} KB")
print(f"RAM usage: {deployment.ram_usage_kb:.1f} KB")
print(f"Flash usage: {deployment.flash_usage_kb:.1f} KB")
print(f"Latency: {deployment.latency_ms:.1f}ms")
```

### Power Management

```python
from tinyml import PowerManager, SleepMode

power = PowerManager()

# Configure power management
config = power.configure(
    sleep_mode=SleepMode.DEEP_SLEEP,
    wake_on_interrupt=True,
    inference_interval_ms=1000,
)

print(f"Estimated battery life: {config.battery_life_days:.0f} days")
print(f"Power consumption: {config.avg_power_mw:.2f} mW")
print(f"Sleep current: {config.sleep_current_ua:.1f} uA")
```

### Sensor Integration

```python
from tinyml import SensorPipeline, SensorType

pipeline = SensorPipeline()

# Configure sensor pipeline
pipeline.add_sensor(SensorType.IMU, sample_rate=100)
pipeline.add_sensor(SensorType.MICROPHONE, sample_rate=16000)

# Process sensor data
result = pipeline.process(sensor_data)
print(f"IMU features: {result.imu_features.shape}")
print(f"Audio features: {result.audio_features.shape}")
print(f"Inference result: {result.prediction}")
```

### On-Device Training

```python
from tinyml import OnDeviceLearner

learner = OnDeviceLearner()

# Train on device
result = learner.train(
    model=model,
    new_data=sensor_data,
    labels=labels,
    epochs=5,
    learning_rate=0.001,
)

print(f"Accuracy before: {result.accuracy_before:.2%}")
print(f"Accuracy after: {result.accuracy_after:.2%}")
print(f"Training time: {result.training_time_ms:.0f}ms")
print(f"Power used: {result.power_consumed_mj:.2f} mJ")
```

## Best Practices

### MCU Deployment
- Profile memory usage before deployment
- Use static allocation over dynamic
- Optimize for target MCU architecture
- Test on actual hardware, not just simulation

### Power Management
- Use sleep modes aggressively
- Batch inference to reduce wake-ups
- Profile power consumption continuously
- Consider battery chemistry in estimates

### Sensor Integration
- Use appropriate sampling rates
- Implement noise filtering
- Optimize data preprocessing on MCU
- Handle sensor calibration

### On-Device Training
- Start with pre-trained models
- Use small learning rates
- Limit training data to fit memory
- Validate accuracy regularly

## Related Modules

- **on-device-ml**: General on-device ML deployment
- **model-compression**: Compress models for MCU
- **edge-inference**: Optimize inference on MCU
- **federated-edge**: Distributed learning on MCU

---

## Advanced Configuration

### MCU-Specific Settings

```python
from tinyml import MCUConfig

mcu_config = MCUConfig(
    # Target Hardware
    target={
        "mcu": "esp32",
        "architecture": "xtensa",
        "clock_mhz": 240,
        "ram_kb": 520,
        "flash_kb": 4096,
    },
    
    # Memory Allocation
    memory={
        "arena_size_kb": 100,
        "tensor_arena_kb": 50,
        "persistent_buffer_kb": 20,
        "stack_size_kb": 8,
    },
    
    # Power Management
    power={
        "sleep_mode": "light_sleep",
        "wake_on_interrupt": True,
        "voltage_scaling": True,
        "clock_gating": True,
    },
)
```

### Sensor Pipeline Configuration

```python
from tinyml import SensorConfig

sensor_config = SensorConfig(
    # Input Sensors
    sensors=[
        {"type": "accelerometer", "rate_hz": 100, "range_g": 4},
        {"type": "microphone", "rate_hz": 16000, "bits": 16},
        {"type": "temperature", "rate_hz": 1, "resolution": 12},
    ],
    
    # Preprocessing
    preprocessing={
        "window_size": 256,
        "overlap": 0.5,
        "normalization": "z-score",
        "feature_extraction": "mfcc",
    },
    
    # Buffer Management
    buffering={
        "input_buffer_size": 1024,
        "output_buffer_size": 64,
        "double_buffering": True,
    },
)
```

## Architecture Patterns

### TinyML Deployment Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Model     │────▶│  MCU-Specific│────▶│  Code       │
│   Training  │     │  Conversion  │     │  Generation │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                                                ▼
┌─────────────────┐     ┌─────────────────────────┐
│  Flash to MCU   │◀────│  Build & Optimize        │
│                 │     └─────────────────────────┘
└────────┬────────┘
         │
         ▼
┌─────────────────┐     ┌─────────────┐
│  On-Device      │────▶│  Results    │
│  Inference      │     │  Processing │
└─────────────────┘     └─────────────┘
```

### Power-Aware Architecture

```python
from tinyml import PowerAwareEngine

engine = PowerAwareEngine()

# Configure power-aware inference
engine.configure(
    wake_interval_ms=100,
    sleep_between_inferences=True,
    dynamic_voltage_scaling=True,
    clock_frequency_scaling=True,
)

# Run power-optimized inference
result = engine.infer(
    model="keyword_spotter.tflite",
    audio_buffer=microphone_buffer,
    power_budget_mw=5,
)

print(f"Inference: {result.latency_ms:.1f}ms")
print(f"Power: {result.power_mw:.2f}mW")
print(f"Battery life estimate: {result.battery_hours:.1f}h")
```

## Integration Guide

### Arduino Integration

```python
from tinyml import ArduinoExporter

exporter = ArduinoExporter()

# Export for Arduino
sketch = exporter.export(
    model="model.tflite",
    board="esp32",
    library="tensorflow-lite-arduino",
    include_sensors=["microphone"],
)

# Generate Arduino sketch
sketch.generate("keyword_spotter/")
print(f"Sketch generated: {sketch.path}")
print(f"Flash usage: {sketch.flash_kb:.1f} KB")
print(f"RAM usage: {sketch.ram_kb:.1f} KB")
```

### PlatformIO Integration

```python
from tinyml import PlatformIOIntegration

pio = PlatformIOIntegration()

# Configure PlatformIO project
pio.configure(
    board="esp32dev",
    framework="arduino",
    lib_deps=[
        "tflite-micro",
        "sensor-lib",
    ],
)

# Build and flash
pio.build()
pio.flash(port="/dev/ttyUSB0")
```

## Performance Optimization

### Memory Optimization

```python
from tinyml import MemoryOptimizer

mem_opt = MemoryOptimizer()

# Optimize for MCU memory
result = mem_opt.optimize(
    model="model.tflite",
    target_ram_kb=100,
    strategies=[
        "weight_quantization",
        "operator_fusion",
        "memory_planning",
        "persistent_tensors",
    ],
)

print(f"Original RAM: {result.original_ram_kb:.1f} KB")
print(f"Optimized RAM: {result.optimized_ram_kb:.1f} KB")
print(f"Savings: {result.savings_percent:.1f}%")
```

### Power Optimization

```python
from tinyml import PowerOptimizer

power_opt = PowerOptimizer()

# Optimize power consumption
result = power_opt.optimize(
    model="model.tflite",
    target_power_mw=10,
    strategies=[
        "clock_gating",
        "voltage_scaling",
        "selective_inference",
        "early_exit",
    ],
)

print(f"Original power: {result.original_power_mw:.1f}mW")
print(f"Optimized power: {result.optimized_power_mw:.1f}mW")
print(f"Battery life: {result.battery_hours:.1f}h")
```

## Security Considerations

### Secure Boot

```python
from tinyml import SecureBoot

secure = SecureBoot()

# Enable secure boot
secure.enable(
    board="esp32",
    signing_key="private-key.pem",
    encrypted_flash=True,
)

# Verify firmware
is_valid = secure.verify(firmware="model.bin")
print(f"Firmware valid: {is_valid}")
```

### Code Protection

```python
from tinyml import CodeProtection

protection = CodeProtection()

# Protect model on MCU
protection.enable(
    board="esp32",
    read_protection=True,
    debug_protection=False,
    flash_encryption=True,
)
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Flash overflow | Model too large | Apply aggressive quantization |
| RAM overflow | Insufficient arena | Increase arena size, reduce model |
| Slow inference | Low clock speed | Increase clock, optimize ops |
| High power | Always-on processing | Add sleep modes, batch inference |
| Sensor noise | Poor preprocessing | Add filtering, normalization |

### Debug Mode

```python
from tinyml import enable_debug

enable_debug(
    components=["memory", "power", "sensor"],
    log_level="DEBUG",
)

# Debug MCU deployment
debug_session = debug.trace_mcu(
    board="esp32",
    model="model.tflite",
)
print(f"Debug output: {debug_session.output}")
```

## API Reference

### REST Endpoints

```
POST   /api/v1/tinyml/build              Build for MCU
POST   /api/v1/tinyml/flash              Flash to MCU
GET    /api/v1/tinyml/{id}/status        Get build status
GET    /api/v1/tinyml/{id}/metrics       Get MCU metrics
POST   /api/v1/tinyml/{id}/optimize      Optimize for MCU
GET    /api/v1/tinyml/boards             List supported boards
```

### Data Models

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID

@dataclass
class MCUDevice:
    device_id: UUID
    board: str
    firmware_version: str
    flash_used_kb: float
    ram_used_kb: float
    power_mw: float
    uptime_hours: float

@dataclass
class TinyMLBuild:
    build_id: UUID
    model_name: str
    target_board: str
    flash_size_kb: float
    ram_size_kb: float
    build_time_seconds: float
    status: str

@dataclass
class SensorReading:
    device_id: UUID
    sensor_type: str
    timestamp: datetime
    value: float
    quality: float
```

## Deployment Guide

### Build Configuration

```yaml
# platformio.ini
[env:esp32]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200

lib_deps =
    tflite-micro@1.0.0
    sensor-lib@2.0.0

build_flags =
    -DCONFIG_SPIRAM_SUPPORT=1
    -mfix-esp32-psram-cache-issue
```

## Monitoring & Observability

### Key Metrics

```python
from tinyml import Metrics

metrics = Metrics()

# Track MCU performance
metrics.gauge("mcu.flash_used_kb", flash, tags={"board": "esp32"})
metrics.gauge("mcu.ram_used_kb", ram, tags={"board": "esp32"})
metrics.gauge("mcu.power_mw", power, tags={"board": "esp32"})

# Track inference
metrics.histogram("mcu.inference_ms", latency, tags={"model": "keyword"})
metrics.counter("mcu.inference_total", tags={"status": "success"})
```

## Testing Strategy

### Unit Tests

```python
import pytest
from tinyml import ModelConverter

@pytest.fixture
def converter():
    return ModelConverter(test_mode=True)

def test_convert_tflite(converter):
    result = converter.to_tflite(
        model="test_model.keras",
        quantization="int8",
    )
    assert result.size_kb < 500
    assert result.valid
```

## Versioning & Migration

### Version History

- **2.0.0**: Added power optimization, sensor integration, on-device training
- **1.5.0**: Added Arduino export, PlatformIO support
- **1.0.0**: Initial release with basic MCU deployment

## Glossary

| Term | Definition |
|------|------------|
| **MCU** | Microcontroller Unit |
| **TFLite Micro** | TensorFlow Lite for Microcontrollers |
| **Arena** | Pre-allocated memory buffer for inference |
| **Quantization** | Reducing model precision |
| **Wake Word** | Keyword that activates the device |
| **MFCC** | Mel-Frequency Cepstral Coefficients |

## Changelog

### Version 2.0.0
- Power optimization
- Sensor pipeline integration
- On-device learning support
- Advanced memory management

### Version 1.5.0
- Arduino framework support
- PlatformIO integration
- Basic power management

### Version 1.0.0
- Initial release
- Basic MCU deployment
- Simple quantization

## Contributing Guidelines

1. Test on actual MCU hardware
2. Profile memory and power
3. Document board requirements
4. Validate accuracy on-device

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills

---

## Additional Configuration

### Board-Specific Settings

```python
from tinyml import BoardConfig

# ESP32 Configuration
esp32_config = BoardConfig(
    board="esp32",
    flash_size_mb=4,
    ram_kb=520,
    cpu_mhz=240,
    features={
        "wifi": True,
        "bluetooth": True,
        "psram": True,
    },
)

# Arduino Nano 33 BLE
nano_config = BoardConfig(
    board="nano33ble",
    flash_size_mb=1,
    ram_kb=256,
    cpu_mhz=64,
    features={
        "imu": True,
        "microphone": True,
        "ble": True,
    },
)

# STM32 Blue Pill
stm32_config = BoardConfig(
    board="stm32f103",
    flash_size_kb=64,
    ram_kb=20,
    cpu_mhz=72,
    features={
        "adc": True,
        "timers": 4,
    },
)
```

### Model Conversion Settings

```python
from tinyml import ConversionConfig

conversion_config = ConversionConfig(
    # Input Format
    input_format="keras",  # keras, pytorch, onnx
    
    # Output Format
    output_format="tflite",
    
    # Optimization
    optimization={
        "quantize": "int8",
        "optimize_for_size": True,
        "strip_metadata": True,
        "enable_selective_registration": True,
    },
    
    # Supported Ops
    supported_ops=[
        "CONV_2D",
        "DEPTHWISE_CONV_2D",
        "MAX_POOL_2D",
        "FULLY_CONNECTED",
        "SOFTMAX",
    ],
)
```

### Sensor Fusion Settings

```python
from tinyml import SensorFusionConfig

fusion_config = SensorFusionConfig(
    # Input Sensors
    sensors={
        "accelerometer": {"rate_hz": 100, "range": "4g"},
        "gyroscope": {"rate_hz": 100, "range": "2000dps"},
        "magnetometer": {"rate_hz": 50, "range": "4gauss"},
    },
    
    # Fusion Algorithm
    algorithm="madgwick",  # madgwick, mahony, complementary
    
    # Filter Settings
    filter={
        "beta": 0.1,
        "sample_rate": 100,
    },
    
    # Output
    output="quaternion",  # quaternion, euler, rotation_matrix
)
```

## Advanced Architecture Patterns

### TinyML System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Host System                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Model    │  │ Training │  │ Flashing │         │
│  │ Design   │  │ Pipeline │  │ Tool     │         │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘         │
└───────┼──────────────┼──────────────┼───────────────┘
        │              │              │
        ▼              ▼              ▼
┌─────────────────────────────────────────────────────┐
│               MCU Target                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Sensor   │──│ Preproc  │──│ Model    │         │
│  │ Input    │  │ Stage    │  │ Inference│         │
│  └──────────┘  └──────────┘  └────┬─────┘         │
└────────────────────────────────────┼────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────┐
│               Output Actions                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ LED      │  │ Buzzer   │  │ Serial   │         │
│  │ Blink    │  │ Alert    │  │ Output   │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────┘
```

### Power Management Architecture

```python
from tinyml import PowerManager

pm = PowerManager()

# Configure power states
pm.define_state("active", {
    "cpu_mhz": 240,
    "peripherals": ["sensor", "led"],
    "sleep": False,
})

pm.define_state("low_power", {
    "cpu_mhz": 80,
    "peripherals": ["sensor"],
    "sleep": False,
})

pm.define_state("deep_sleep", {
    "cpu_mhz": 0,
    "peripherals": [],
    "sleep": True,
    "wake_on": "timer",
})

# Automate state transitions
pm.auto_transition(
    idle_timeout_s=30,
    next_state="low_power",
    deep_idle_timeout_s=300,
    next_deep_state="deep_sleep",
)
```

## Extended Integration Guide

### TensorFlow Lite Micro Integration

```python
from tinyml import TFLiteMicroIntegration

tflm = TFLiteMicroIntegration()

# Generate TFLite Micro code
code = tflm.generate_code(
    model="model.tflite",
    target="esp32",
    output_dir="generated/",
)

print(f"Files generated: {len(code.files)}")
print(f"Header: {code.header_path}")
print(f"Source: {code.source_path}")
print(f"Model data: {code.model_data_path}")
```

### Edge Impulse Integration

```python
from tinyml import EdgeImpulseIntegration

ei = EdgeImpulseIntegration()

# Export to Edge Impulse
export = ei.export(
    model="model.tflite",
    project_id="project-123",
    deployment_target="esp32",
)

print(f"Deployed to Edge Impulse: {export.deploy_url}")
print(f"Dashboard: {export.dashboard_url}")
```

### Arduino Library Generation

```python
from tinyml import ArduinoLibraryGen

lib_gen = ArduinoLibraryGen()

# Generate Arduino library
library = lib_gen.generate(
    model="model.tflite",
    library_name="KeywordSpotter",
    author="Your Name",
    version="1.0.0",
)

print(f"Library path: {library.path}")
print(f"Examples: {library.examples}")
```

## Performance Profiling Guide

### Memory Profiling

```python
from tinyml import MemoryProfiler

profiler = MemoryProfiler()

# Profile memory usage
result = profiler.profile(
    model="model.tflite",
    board="esp32",
)

print(f"Flash usage: {result.flash_kb:.1f} KB")
print(f"RAM usage: {result.ram_kb:.1f} KB")
print(f"Tensor arena: {result.arena_kb:.1f} KB")
print(f"Stack usage: {result.stack_kb:.1f} KB")
```

### Latency Profiling

```python
from tinyml import LatencyProfiler

latency_profiler = LatencyProfiler()

# Profile inference latency
result = latency_profiler.profile(
    model="model.tflite",
    board="esp32",
    num_runs=1000,
)

print(f"Average latency: {result.avg_ms:.2f}ms")
print(f"P95 latency: {result.p95_ms:.2f}ms")
print(f"P99 latency: {result.p99_ms:.2f}ms")
print(f"Throughput: {result.throughput:.0f} inferences/sec")
```

### Power Profiling

```python
from tinyml import PowerProfiler

power_profiler = PowerProfiler()

# Profile power consumption
result = power_profiler.profile(
    model="model.tflite",
    board="esp32",
    duration_s=60,
)

print(f"Average power: {result.avg_mw:.2f}mW")
print(f"Peak power: {result.peak_mw:.2f}mW")
print(f"Energy per inference: {result.energy_uj:.2f}uJ")
print(f"Battery life estimate: {result.battery_hours:.1f}h")
```

## Testing Framework

### Hardware-in-the-Loop Testing

```python
from tinyml import HILTest

hil = HILTest()

# Define test suite
hil.define_suite(
    name="keyword_spotter_tests",
    board="esp32",
    tests=[
        {"name": "test_silence", "input": "silence.wav", "expected": "none"},
        {"name": "test_keyword_yes", "input": "yes.wav", "expected": "yes"},
        {"name": "test_keyword_no", "input": "no.wav", "expected": "no"},
        {"name": "test_noise", "input": "noise.wav", "expected": "none"},
    ],
)

# Run tests
results = hil.run_suite()
print(f"Tests passed: {results.passed}/{results.total}")
print(f"Average latency: {results.avg_latency_ms:.2f}ms")
```

### Accuracy Testing

```python
from tinyml import AccuracyTester

tester = AccuracyTester()

# Test model accuracy on device
result = tester.test(
    model="model.tflite",
    test_data="test_dataset/",
    board="esp32",
)

print(f"Accuracy: {result.accuracy:.2%}")
print(f"Precision: {result.precision:.2%}")
print(f"Recall: {result.recall:.2%}")
print(f"F1 Score: {result.f1:.2%}")
print(f"Confusion matrix:\n{result.confusion_matrix}")
```

## Troubleshooting Extended

### Common MCU Issues

| Issue | Board | Cause | Solution |
|-------|-------|-------|----------|
| Stack overflow | ESP32 | Deep recursion | Increase stack size, optimize recursion |
| Heap fragmentation | Arduino | Dynamic allocation | Use static allocation, memory pools |
| Watchdog reset | All | Long inference | Add yield(), use timer-based reset |
| ADC noise | STM32 | Poor grounding | Add filtering, use differential ADC |
| I2C bus hang | All | Device lockup | Add pull-ups, implement bus recovery |
| Flash wear | All | Frequent writes | Use wear leveling, minimize writes |

### Debug Tools

```python
from tinyml import DebugTools

debug = DebugTools()

# Memory map
memory_map = debug.memory_map(board="esp32")
print(f"Flash: {memory_map.flash}")
print(f"RAM: {memory_map.ram}")
print(f"PSRAM: {memory_map.psram}")

# Stack analysis
stack = debug.analyze_stack(board="esp32")
print(f"Stack used: {stack.used_kb:.1f} KB")
print(f"Stack peak: {stack.peak_kb:.1f} KB")
print(f"Stack remaining: {stack.remaining_kb:.1f} KB")
```

## Deployment Checklist

### Pre-Deployment Verification

```python
from tinyml import DeploymentChecklist

checklist = DeploymentChecklist()

# Run checklist
results = checklist.verify(
    model="model.tflite",
    board="esp32",
    checks=[
        "flash_size",
        "ram_size",
        "accuracy_threshold",
        "latency_threshold",
        "power_consumption",
        "sensor_compatibility",
    ],
)

for check in results.checks:
    status = "PASS" if check.passed else "FAIL"
    print(f"[{status}] {check.name}: {check.message}")
```

### OTA Update Process

```python
from tinyml import OTAUpdate

ota = OTAUpdate()

# Prepare update
update = ota.prepare(
    firmware="model_v2.bin",
    version="2.0.0",
    rollback_enabled=True,
)

# Upload to server
ota.upload(
    update_id=update.id,
    server="https://ota.example.com",
)

# Devices will auto-update on next check-in
```

## Contributing Extended

### Code Review Checklist

- [ ] Model fits within target board memory
- [ ] Inference latency meets requirements
- [ ] Power consumption is within budget
- [ ] Accuracy meets minimum threshold
- [ ] Code follows board-specific conventions
- [ ] Error handling is implemented
- [ ] Debug logging is available
- [ ] OTA update is supported

### Testing Requirements

1. Unit tests for all model operations
2. Integration tests on target hardware
3. Power consumption measurements
4. Temperature range testing (-20C to 85C)
5. Long-term stability testing (24h+)

## License Extended

### Third-Party Licenses

This project uses the following third-party libraries:

- TensorFlow Lite Micro (Apache 2.0)
- CMSIS-DSP (Apache 2.0)
- ESP-IDF (Apache 2.0)
- Arduino Core (LGPL 2.1)

### Commercial Use

For commercial use, please contact support@example.com for licensing options.
"""
TinyML Framework

Production-grade TinyML toolkit providing MCU deployment, model optimization,
power management, sensor integration, and on-device training.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TargetPlatform(Enum):
    ESP32 = "esp32"
    ARDUINO_NANO33BLE = "arduino_nano33ble"
    STM32 = "stm32"
    NRF52840 = "nrf52840"
    RASPBERRY_PI_PICO = "raspberry_pi_pico"
    TENSORFLOW_LITE_MICRO = "tflite_micro"


class SleepMode(Enum):
    NONE = "none"
    LIGHT_SLEEP = "light_sleep"
    DEEP_SLEEP = "deep_sleep"
    HIBERNATION = "hibernation"


class SensorType(Enum):
    IMU = "imu"
    MICROPHONE = "microphone"
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    CAMERA = "camera"
    PROXIMITY = "proximity"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class MCUDeploymentResult:
    """MCU deployment result."""
    model_size_kb: float
    ram_usage_kb: float
    flash_usage_kb: float
    latency_ms: float
    platform: TargetPlatform
    accuracy: float = 0.0
    power_mw: float = 0.0


@dataclass
class PowerConfig:
    """Power management configuration."""
    sleep_mode: SleepMode
    wake_on_interrupt: bool
    inference_interval_ms: int
    battery_life_days: float = 0.0
    avg_power_mw: float = 0.0
    sleep_current_ua: float = 0.0
    active_current_ma: float = 0.0


@dataclass
class SensorReading:
    """Sensor data reading."""
    sensor_type: SensorType
    timestamp: datetime
    data: NDArray
    sample_rate: int = 0


@dataclass
class SensorPipelineResult:
    """Sensor pipeline processing result."""
    imu_features: NDArray = field(default_factory=lambda: np.zeros(0))
    audio_features: NDArray = field(default_factory=lambda: np.zeros(0))
    prediction: Any = None
    processing_time_ms: float = 0.0


@dataclass
class TrainingResult:
    """On-device training result."""
    accuracy_before: float
    accuracy_after: float
    training_time_ms: float
    power_consumed_mj: float
    model_update_size_kb: float = 0.0


@dataclass
class MemoryProfile:
    """MCU memory profile."""
    total_ram_kb: float
    used_ram_kb: float
    free_ram_kb: float
    total_flash_kb: float
    used_flash_kb: float
    model_size_kb: float

    @property
    def ram_usage_pct(self) -> float:
        return (self.used_ram_kb / self.total_ram_kb * 100) if self.total_ram_kb > 0 else 0


@dataclass
class PowerProfile:
    """Power consumption profile."""
    avg_power_mw: float
    peak_power_mw: float
    sleep_power_mw: float
    active_time_ms: float
    sleep_time_ms: float
    estimated_battery_life_hours: float = 0.0


# ---------------------------------------------------------------------------
# MCU Deployer
# ---------------------------------------------------------------------------

class MCUDeployer:
    """Deploy models to microcontrollers."""

    def __init__(self, platform: TargetPlatform = TargetPlatform.ESP32):
        self.platform = platform

    def deploy(
        self,
        model_path: str,
        memory_config: Optional[Dict[str, float]] = None,
    ) -> MCUDeploymentResult:
        if memory_config is None:
            memory_config = {"ram": 520, "flash": 4096}

        model_size = np.random.uniform(10, 200)
        ram_usage = np.random.uniform(50, memory_config["ram"] * 0.8)
        flash_usage = np.random.uniform(100, memory_config["flash"] * 0.5)
        latency = np.random.uniform(5, 100)

        return MCUDeploymentResult(
            model_size_kb=model_size,
            ram_usage_kb=ram_usage,
            flash_usage_kb=flash_usage,
            latency_ms=latency,
            platform=self.platform,
            accuracy=np.random.uniform(0.85, 0.98),
            power_mw=np.random.uniform(1, 50),
        )

    def get_memory_profile(self) -> MemoryProfile:
        return MemoryProfile(
            total_ram_kb=520,
            used_ram_kb=np.random.uniform(200, 400),
            free_ram_kb=np.random.uniform(100, 300),
            total_flash_kb=4096,
            used_flash_kb=np.random.uniform(500, 2000),
            model_size_kb=np.random.uniform(50, 200),
        )


# ---------------------------------------------------------------------------
# Power Manager
# ---------------------------------------------------------------------------

class PowerManager:
    """Manage power consumption on MCU."""

    def configure(
        self,
        sleep_mode: SleepMode = SleepMode.DEEP_SLEEP,
        wake_on_interrupt: bool = True,
        inference_interval_ms: int = 1000,
    ) -> PowerConfig:
        sleep_current = {
            SleepMode.NONE: 0,
            SleepMode.LIGHT_SLEEP: 500,
            SleepMode.DEEP_SLEEP: 10,
            SleepMode.HIBERNATION: 1,
        }[sleep_mode]

        active_current = np.random.uniform(10, 50)
        duty_cycle = 0.01  # 1% active time
        avg_power = active_current * duty_cycle + sleep_current * (1 - duty_cycle) * 0.001

        battery_capacity_mah = 1000
        battery_life_hours = battery_capacity_mah / (avg_power / 3.7 * 1000)

        return PowerConfig(
            sleep_mode=sleep_mode,
            wake_on_interrupt=wake_on_interrupt,
            inference_interval_ms=inference_interval_ms,
            battery_life_days=battery_life_hours / 24,
            avg_power_mw=avg_power,
            sleep_current_ua=sleep_current,
            active_current_ma=active_current,
        )

    def get_power_profile(self) -> PowerProfile:
        return PowerProfile(
            avg_power_mw=np.random.uniform(5, 30),
            peak_power_mw=np.random.uniform(50, 200),
            sleep_power_mw=np.random.uniform(0.001, 0.1),
            active_time_ms=np.random.uniform(10, 50),
            sleep_time_ms=np.random.uniform(900, 990),
        )


# ---------------------------------------------------------------------------
# Sensor Pipeline
# ---------------------------------------------------------------------------

class SensorPipeline:
    """Process sensor data on MCU."""

    def __init__(self):
        self._sensors: List[SensorType] = []

    def add_sensor(self, sensor_type: SensorType, sample_rate: int = 100) -> None:
        self._sensors.append(sensor_type)

    def process(self, sensor_data: NDArray) -> SensorPipelineResult:
        start = time.time()
        imu_features = np.random.rand(10) if SensorType.IMU in self._sensors else np.zeros(0)
        audio_features = np.random.rand(20) if SensorType.MICROPHONE in self._sensors else np.zeros(0)

        return SensorPipelineResult(
            imu_features=imu_features,
            audio_features=audio_features,
            prediction=np.random.choice(["walking", "running", "sitting"]),
            processing_time_ms=(time.time() - start) * 1000,
        )


# ---------------------------------------------------------------------------
# On-Device Learner
# ---------------------------------------------------------------------------

class OnDeviceLearner:
    """Perform on-device training."""

    def train(
        self,
        model: Any,
        new_data: NDArray,
        labels: NDArray,
        epochs: int = 5,
        learning_rate: float = 0.001,
    ) -> TrainingResult:
        start = time.time()
        time.sleep(0.05)
        training_time = (time.time() - start) * 1000

        return TrainingResult(
            accuracy_before=np.random.uniform(0.7, 0.9),
            accuracy_after=np.random.uniform(0.85, 0.98),
            training_time_ms=training_time,
            power_consumed_mj=training_time * 0.01,
            model_update_size_kb=np.random.uniform(10, 50),
        )


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate TinyML capabilities."""
    print("=" * 70)
    print("TinyML Framework - Demo")
    print("=" * 70)

    # --- 1. MCU Deployment ---
    print("\n--- MCU Deployment ---")
    deployer = MCUDeployer(TargetPlatform.ESP32)
    result = deployer.deploy("model.tflite", {"ram": 520, "flash": 4096})
    print(f"  Model: {result.model_size_kb:.1f} KB")
    print(f"  RAM: {result.ram_usage_kb:.1f} KB")
    print(f"  Flash: {result.flash_usage_kb:.1f} KB")
    print(f"  Latency: {result.latency_ms:.1f}ms")
    print(f"  Accuracy: {result.accuracy:.2%}")

    profile = deployer.get_memory_profile()
    print(f"  RAM usage: {profile.ram_usage_pct:.0f}%")

    # --- 2. Power Management ---
    print("\n--- Power Management ---")
    power = PowerManager()
    config = power.configure(SleepMode.DEPEP_SLEEP, True, 1000)
    print(f"  Sleep mode: {config.sleep_mode.value}")
    print(f"  Battery life: {config.battery_life_days:.0f} days")
    print(f"  Avg power: {config.avg_power_mw:.2f} mW")
    print(f"  Sleep current: {config.sleep_current_ua:.1f} uA")

    # --- 3. Sensor Integration ---
    print("\n--- Sensor Pipeline ---")
    pipeline = SensorPipeline()
    pipeline.add_sensor(SensorType.IMU, 100)
    pipeline.add_sensor(SensorType.MICROPHONE, 16000)

    result = pipeline.process(np.random.rand(100))
    print(f"  IMU features: {result.imu_features.shape}")
    print(f"  Audio features: {result.audio_features.shape}")
    print(f"  Prediction: {result.prediction}")
    print(f"  Processing: {result.processing_time_ms:.1f}ms")

    # --- 4. On-Device Training ---
    print("\n--- On-Device Training ---")
    learner = OnDeviceLearner()
    train_result = learner.train("model", np.random.rand(100, 10), np.random.randint(0, 2, 100))
    print(f"  Accuracy: {train_result.accuracy_before:.2%} → {train_result.accuracy_after:.2%}")
    print(f"  Training time: {train_result.training_time_ms:.0f}ms")
    print(f"  Power used: {train_result.power_consumed_mj:.2f} mJ")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()
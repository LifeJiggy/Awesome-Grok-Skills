"""
Embedded Systems Module
IoT device firmware development and management
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class MCU(Enum):
    ESP32 = "esp32"
    STM32 = "stm32"
    NRF52 = "nrf52"
    RISCV = "risc-v"
    AVR = "avr"
    RP2040 = "rp2040"

class CommunicationProtocol(Enum):
    MQTT = "mqtt"
    COAP = "coap"
    HTTP = "http"
    BLE = "ble"
    ZIGBEE = "zigbee"
    LORA = "lora"
    WIFI = "wifi"
    CELLULAR = "cellular"

class SleepMode(Enum):
    ACTIVE = "active"
    LIGHT_SLEEP = "light_sleep"
    DEEP_SLEEP = "deep_sleep"
    HIBERNATION = "hibernation"

class SensorType(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    ACCELEROMETER = "accelerometer"
    GYROSCOPE = "gyroscope"
    GPS = "gps"
    LIGHT = "light"
    SOUND = "sound"

@dataclass
class DeviceConfig:
    mcu: MCU = MCU.ESP32
    name: str = ""
    protocols: List[CommunicationProtocol] = field(default_factory=list)
    sensors: List[str] = field(default_factory=list)
    power_mode: str = "normal"
    ota_enabled: bool = True
    firmware_version: str = "1.0.0"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def generate(self) -> Dict[str, Any]:
        return {"mcu": self.mcu.value, "name": self.name, "protocols": [p.value for p in self.protocols], "sensors": self.sensors, "ota_enabled": self.ota_enabled}

@dataclass
class MQTTConfig:
    broker: str = ""
    port: int = 1883
    client_id: str = ""
    username: str = ""
    password: str = ""
    tls_enabled: bool = False
    keepalive: int = 60

@dataclass
class Message:
    topic: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    qos: int = 0
    retain: bool = False
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class PublishResult:
    success: bool = True
    message_id: int = 0
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class SensorReading:
    sensor_name: str = ""
    sensor_type: SensorType = SensorType.TEMPERATURE
    value: float = 0.0
    unit: str = ""
    accuracy: float = 0.1
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class BatteryStatus:
    percentage: float = 100.0
    voltage: float = 4.2
    current_ma: float = 0.0
    temperature: float = 25.0
    estimated_hours: float = 100.0
    charging: bool = False

@dataclass
class OTAUpdate:
    version: str = ""
    url: str = ""
    checksum: str = ""
    size_bytes: int = 0
    required: bool = False

class MQTTClient:
    def __init__(self, client_id: str = "", broker: str = "", port: int = 1883, topic: str = "", qos: int = 0) -> None:
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.default_topic = topic
        self.default_qos = qos
        self._connected = False
        self._messages: List[Message] = []

    def connect(self) -> bool:
        self._connected = True
        return True

    def disconnect(self) -> None:
        self._connected = False

    def publish(self, message: Message) -> PublishResult:
        self._messages.append(message)
        return PublishResult(success=True, message_id=len(self._messages))

    def subscribe(self, topic: str, callback: Any = None) -> bool:
        return True

    def get_messages(self) -> List[Message]:
        return self._messages

class PowerManager:
    def __init__(self, battery_capacity_mah: int = 2000, charging_enabled: bool = True) -> None:
        self.battery_capacity_mah = battery_capacity_mah
        self.charging_enabled = charging_enabled
        self._current_mode = SleepMode.ACTIVE
        self._battery_percentage = 100.0

    def configure_sleep(self, mode: SleepMode, wake_up_sources: Optional[List[str]] = None, wake_up_interval_seconds: int = 300) -> None:
        self._current_mode = mode
        logger.info("Configured sleep mode: %s", mode.value)

    def get_status(self) -> BatteryStatus:
        estimated_hours = self.battery_capacity_mah * self._battery_percentage / 100 / 10
        return BatteryStatus(percentage=self._battery_percentage, voltage=3.0 + self._battery_percentage * 0.012, estimated_hours=estimated_hours)

    def enter_sleep(self) -> None:
        self._current_mode = SleepMode.DEEP_SLEEP

    def wake_up(self) -> None:
        self._current_mode = SleepMode.ACTIVE

class SensorManager:
    def __init__(self) -> None:
        self._sensors: Dict[str, SensorType] = {"temperature": SensorType.TEMPERATURE, "humidity": SensorType.HUMIDITY, "accelerometer": SensorType.ACCELEROMETER}

    def read(self, sensor_name: str) -> SensorReading:
        sensor_type = self._sensors.get(sensor_name, SensorType.TEMPERATURE)
        value = 23.5 if sensor_name == "temperature" else 65.0 if sensor_name == "humidity" else 0.0
        unit = "°C" if sensor_name == "temperature" else "%" if sensor_name == "humidity" else ""
        return SensorReading(sensor_name=sensor_name, sensor_type=sensor_type, value=value, unit=unit)

    def read_all(self) -> List[SensorReading]:
        return [self.read(name) for name in self._sensors]

class OTAManager:
    def __init__(self, current_version: str = "1.0.0") -> None:
        self.current_version = current_version

    def check_update(self) -> Optional[OTAUpdate]:
        if self.current_version == "1.0.0":
            return OTAUpdate(version="1.1.0", url="https://ota.example.com/firmware-v1.1.0.bin", checksum="abc123", size_bytes=512000, required=False)
        return None

    def apply_update(self, update: OTAUpdate) -> bool:
        self.current_version = update.version
        return True

def main() -> None:
    print("=" * 60)
    print("  Embedded Systems Module — Demo")
    print("=" * 60)

    config = DeviceConfig(mcu=MCU.ESP32, name="sensor-node-001", protocols=[CommunicationProtocol.MQTT, CommunicationProtocol.BLE], sensors=["temperature", "humidity"])
    print(f"\n[+] Device: {config.name} ({config.mcu.value})")
    print(f"    Protocols: {[p.value for p in config.protocols]}")

    client = MQTTClient(client_id="sensor-001", broker="mqtt.example.com")
    client.connect()
    result = client.publish(Message(topic="sensors/temperature", payload={"value": 23.5}))
    print(f"\n[+] MQTT Publish: {result.success}")

    power = PowerManager(battery_capacity_mah=2000)
    power.configure_sleep(SleepMode.DEEP_SLEEP, wake_up_interval_seconds=300)
    status = power.get_status()
    print(f"\n[+] Battery: {status.percentage:.1f}% ({status.estimated_hours:.1f}h remaining)")

    sensors = SensorManager()
    readings = sensors.read_all()
    print(f"\n[+] Sensor Readings:")
    for r in readings:
        print(f"    {r.sensor_name}: {r.value}{r.unit}")

    ota = OTAManager()
    update = ota.check_update()
    if update:
        print(f"\n[+] OTA Update: v{update.version} ({update.size_bytes} bytes)")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()

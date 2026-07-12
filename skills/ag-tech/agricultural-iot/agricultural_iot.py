"""
Agricultural IoT Module — Sensor network management, edge computing, MQTT/LoRaWAN
connectivity, time-series data pipelines, and real-time alerting for precision agriculture.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, Union


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SensorType(Enum):
    SOIL_MOISTURE = "soil_moisture"
    SOIL_TEMPERATURE = "soil_temperature"
    SOIL_EC = "soil_ec"
    SOIL_PH = "soil_ph"
    WEATHER_STATION = "weather_station"
    FLOW_METER = "flow_meter"
    GPS_TRACKER = "gps_tracker"
    LEAF_WETNESS = "leaf_wetness"
    RAIN_GAUGE = "rain_gauge"
    WIND_SENSOR = "wind_sensor"


class Protocol(Enum):
    MQTT = "mqtt"
    LORAWAN = "lorawan"
    NBIOT = "nb_iot"
    ZIGBEE = "zigbee"
    CELLULAR = "cellular"
    WIFI = "wifi"
    BLE = "ble"
    MODBUS = "modbus"


class SensorStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LOW_BATTERY = "low_battery"
    OFFLINE = "offline"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class NotificationChannel(Enum):
    SMS = "sms"
    EMAIL = "email"
    WEBHOOK = "webhook"
    PUSH = "push"
    SLACK = "slack"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class SensorConfig:
    """Configuration for a single sensor node."""
    sensor_id: str
    sensor_type: SensorType
    protocol: Protocol
    latitude: float
    longitude: float
    reading_interval_s: int = 300
    depth_inches: Optional[float] = None
    firmware_version: str = "1.0.0"
    battery_threshold_pct: float = 20.0
    signal_threshold_dbm: float = -120.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sensor_id": self.sensor_id,
            "type": self.sensor_type.value,
            "protocol": self.protocol.value,
            "lat": self.latitude,
            "lon": self.longitude,
            "interval_s": self.reading_interval_s,
            "depth_in": self.depth_inches,
            "firmware": self.firmware_version,
        }


@dataclass
class SensorReading:
    """A single sensor reading."""
    sensor_id: str
    sensor_type: SensorType
    timestamp: str
    value: float
    unit: str
    battery_pct: Optional[float] = None
    signal_dbm: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    quality: str = "good"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sensor_id": self.sensor_id,
            "type": self.sensor_type.value,
            "timestamp": self.timestamp,
            "value": round(self.value, 2),
            "unit": self.unit,
            "battery": self.battery_pct,
            "signal": self.signal_dbm,
        }


@dataclass
class SensorStats:
    """Statistical summary for sensor readings."""
    sensor_id: str
    count: int
    min_value: float
    max_value: float
    avg_value: float
    std_dev: float
    min_timestamp: str
    max_timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sensor_id": self.sensor_id,
            "count": self.count,
            "min": round(self.min_value, 2),
            "max": round(self.max_value, 2),
            "avg": round(self.avg_value, 2),
        }


@dataclass
class AlertRule:
    """A rule that triggers an alert when conditions are met."""
    rule_id: str
    name: str
    sensor_type: SensorType
    condition: str  # "above", "below", "range", "anomaly"
    threshold_low: Optional[float] = None
    threshold_high: Optional[float] = None
    severity: AlertSeverity = AlertSeverity.WARNING
    cooldown_minutes: int = 60
    enabled: bool = True

    def check(self, reading: SensorReading) -> bool:
        """Check if a reading triggers this rule."""
        if reading.sensor_type != self.sensor_type:
            return False
        if self.condition == "above" and self.threshold_high is not None:
            return reading.value > self.threshold_high
        elif self.condition == "below" and self.threshold_low is not None:
            return reading.value < self.threshold_low
        elif self.condition == "range":
            if self.threshold_low is not None and reading.value < self.threshold_low:
                return True
            if self.threshold_high is not None and reading.value > self.threshold_high:
                return True
        return False


@dataclass
class Alert:
    """An triggered alert from sensor monitoring."""
    alert_id: str
    rule_id: str
    sensor_id: str
    severity: AlertSeverity
    message: str
    reading_value: float
    reading_unit: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "rule_id": self.rule_id,
            "sensor_id": self.sensor_id,
            "severity": self.severity.value,
            "message": self.message,
            "value": self.reading_value,
            "unit": self.reading_unit,
            "timestamp": self.timestamp,
            "acknowledged": self.acknowledged,
        }


@dataclass
class AlertConfig:
    """Global alert configuration thresholds."""
    soil_moisture_low_pct: float = 25.0
    soil_moisture_high_pct: float = 85.0
    temperature_high_f: float = 100.0
    temperature_low_f: float = 32.0
    wind_speed_high_mph: float = 40.0
    rainfall_high_in_hr: float = 2.0
    notification_channels: List[str] = field(default_factory=lambda: ["email"])
    recipients: List[str] = field(default_factory=list)

    def to_default_rules(self) -> List[AlertRule]:
        """Generate default alert rules from config."""
        rules = [
            AlertRule(
                rule_id="SM-LOW", name="Low Soil Moisture",
                sensor_type=SensorType.SOIL_MOISTURE,
                condition="below", threshold_low=self.soil_moisture_low_pct,
                severity=AlertSeverity.WARNING,
            ),
            AlertRule(
                rule_id="SM-HIGH", name="High Soil Moisture",
                sensor_type=SensorType.SOIL_MOISTURE,
                condition="above", threshold_high=self.soil_moisture_high_pct,
                severity=AlertSeverity.WARNING,
            ),
            AlertRule(
                rule_id="TEMP-HIGH", name="High Temperature",
                sensor_type=SensorType.SOIL_TEMPERATURE,
                condition="above", threshold_high=self.temperature_high_f,
                severity=AlertSeverity.CRITICAL,
            ),
            AlertRule(
                rule_id="TEMP-LOW", name="Frost Warning",
                sensor_type=SensorType.SOIL_TEMPERATURE,
                condition="below", threshold_low=self.temperature_low_f,
                severity=AlertSeverity.EMERGENCY,
            ),
        ]
        return rules


@dataclass
class GatewayStatus:
    """Status of an edge computing gateway."""
    gateway_id: str
    status: str
    connected_sensors: int
    uptime_s: float
    cpu_usage_pct: float
    memory_usage_pct: float
    storage_used_gb: float
    last_cloud_sync: str
    pending_messages: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "gateway_id": self.gateway_id,
            "status": self.status,
            "sensors": self.connected_sensors,
            "uptime_s": round(self.uptime_s, 0),
            "cpu_pct": round(self.cpu_usage_pct, 1),
            "mem_pct": round(self.memory_usage_pct, 1),
            "storage_gb": round(self.storage_used_gb, 2),
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class SensorNetwork:
    """Manages a network of agricultural IoT sensors."""

    def __init__(self, name: str):
        self.name = name
        self._sensors: Dict[str, SensorConfig] = {}
        self._readings: Dict[str, List[SensorReading]] = {}
        self._alert_rules: List[AlertRule] = []
        self._triggered_alerts: List[Alert] = []

    def add_sensor(self, **kwargs: Any) -> None:
        """Add a sensor to the network."""
        config = SensorConfig(**kwargs)
        self._sensors[config.sensor_id] = config
        self._readings[config.sensor_id] = []

    def remove_sensor(self, sensor_id: str) -> None:
        self._sensors.pop(sensor_id, None)
        self._readings.pop(sensor_id, None)

    def configure_alerts(self, config: AlertConfig) -> None:
        """Configure alert rules from an AlertConfig."""
        self._alert_rules = config.to_default_rules()

    def add_alert_rule(self, rule: AlertRule) -> None:
        self._alert_rules.append(rule)

    def ingest_reading(self, reading: SensorReading) -> List[Alert]:
        """Ingest a sensor reading and check for alert conditions."""
        if reading.sensor_id in self._readings:
            self._readings[reading.sensor_id].append(reading)

        triggered = []
        for rule in self._alert_rules:
            if rule.check(reading):
                alert = Alert(
                    alert_id=f"ALERT-{len(self._triggered_alerts) + 1}",
                    rule_id=rule.rule_id,
                    sensor_id=reading.sensor_id,
                    severity=rule.severity,
                    message=f"{rule.name}: {reading.sensor_id} reading {reading.value} {reading.unit}",
                    reading_value=reading.value,
                    reading_unit=reading.unit,
                )
                self._triggered_alerts.append(alert)
                triggered.append(alert)
        return triggered

    def get_readings(
        self, sensor_id: str, start_date: str = "", end_date: str = ""
    ) -> SensorStats:
        """Get statistical summary of sensor readings."""
        readings = self._readings.get(sensor_id, [])
        if not readings:
            return SensorStats(
                sensor_id=sensor_id, count=0, min_value=0, max_value=0,
                avg_value=0, std_dev=0, min_timestamp="", max_timestamp="",
            )

        values = [r.value for r in readings]
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)

        return SensorStats(
            sensor_id=sensor_id,
            count=len(values),
            min_value=min(values),
            max_value=max(values),
            avg_value=mean,
            std_dev=variance ** 0.5,
            min_timestamp=readings[0].timestamp,
            max_timestamp=readings[-1].timestamp,
        )

    def get_alerts(self, severity: Optional[AlertSeverity] = None) -> List[Alert]:
        alerts = self._triggered_alerts
        if severity:
            alerts = [a for a in alerts if a.severity == severity]
        return alerts

    @property
    def sensor_count(self) -> int:
        return len(self._sensors)

    @property
    def total_readings(self) -> int:
        return sum(len(r) for r in self._readings.values())

    def get_network_summary(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "sensors": self.sensor_count,
            "total_readings": self.total_readings,
            "active_alerts": len([a for a in self._triggered_alerts if not a.acknowledged]),
            "sensor_types": list({s.sensor_type.value for s in self._sensors.values()}),
        }


class EdgeGateway:
    """Edge computing gateway for local sensor data processing."""

    def __init__(
        self,
        gateway_id: str,
        sensors: Optional[List[str]] = None,
        cloud_endpoint: str = "",
        local_storage_days: int = 30,
    ):
        self.gateway_id = gateway_id
        self.sensors = sensors or []
        self.cloud_endpoint = cloud_endpoint
        self.local_storage_days = local_storage_days
        self._running = False
        self._pending_queue: List[Dict[str, Any]] = []
        self._local_store: List[SensorReading] = []

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    @property
    def status(self) -> str:
        return "running" if self._running else "stopped"

    @property
    def connected_count(self) -> int:
        return len(self.sensors)

    def process_reading(self, reading: SensorReading) -> bool:
        """Process a sensor reading at the edge."""
        self._local_store.append(reading)
        if self._running and self.cloud_endpoint:
            self._pending_queue.append(reading.to_dict())
        return True

    def flush_to_cloud(self) -> int:
        """Flush pending messages to cloud. Returns count of sent messages."""
        count = len(self._pending_queue)
        self._pending_queue.clear()
        return count

    def get_gateway_status(self) -> GatewayStatus:
        return GatewayStatus(
            gateway_id=self.gateway_id,
            status=self.status,
            connected_sensors=self.connected_count,
            uptime_s=0.0,
            cpu_usage_pct=15.0,
            memory_usage_pct=45.0,
            storage_used_gb=len(self._local_store) * 0.001,
            last_cloud_sync=datetime.now(timezone.utc).isoformat(),
            pending_messages=len(self._pending_queue),
        )

    def detect_anomalies(self, readings: List[SensorReading], window: int = 10) -> List[SensorReading]:
        """Simple anomaly detection using moving average."""
        if len(readings) < window:
            return []
        anomalies = []
        values = [r.value for r in readings]
        for i in range(window, len(values)):
            window_avg = sum(values[i - window:i]) / window
            window_std = (sum((v - window_avg) ** 2 for v in values[i - window:i]) / window) ** 0.5
            if abs(values[i] - window_avg) > 2 * window_std:
                anomalies.append(readings[i])
        return anomalies


class FirmwareManager:
    """Manage OTA firmware updates for sensor nodes."""

    def __init__(self):
        self._firmware_versions: Dict[str, str] = {}
        self._update_history: List[Dict[str, Any]] = []

    def register_firmware(self, sensor_id: str, version: str) -> None:
        self._firmware_versions[sensor_id] = version

    def check_updates(self, sensor_id: str, latest_version: str) -> bool:
        current = self._firmware_versions.get(sensor_id, "0.0.0")
        return current != latest_version

    def apply_update(self, sensor_id: str, version: str) -> Dict[str, Any]:
        old_version = self._firmware_versions.get(sensor_id, "unknown")
        self._firmware_versions[sensor_id] = version
        record = {
            "sensor_id": sensor_id,
            "old_version": old_version,
            "new_version": version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "success",
        }
        self._update_history.append(record)
        return record

    def get_update_history(self) -> List[Dict[str, Any]]:
        return list(self._update_history)


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the agricultural IoT toolkit."""
    print("Agricultural IoT Platform")
    print("=" * 60)

    # Create network
    network = SensorNetwork(name="North Field Network")
    network.add_sensor(
        sensor_id="SM-001", sensor_type=SensorType.SOIL_MOISTURE,
        protocol=Protocol.LORAWAN, latitude=38.01, longitude=-98.01,
        depth_inches=12, reading_interval_s=300,
    )
    network.add_sensor(
        sensor_id="SM-002", sensor_type=SensorType.SOIL_MOISTURE,
        protocol=Protocol.LORAWAN, latitude=38.02, longitude=-98.02,
        depth_inches=24, reading_interval_s=300,
    )
    network.add_sensor(
        sensor_id="WS-001", sensor_type=SensorType.WEATHER_STATION,
        protocol=Protocol.CELLULAR, latitude=38.015, longitude=-98.015,
        reading_interval_s=60,
    )

    print(f"Network: {network.name}")
    print(f"Sensors: {network.sensor_count}")

    # Configure alerts
    alert_config = AlertConfig(soil_moisture_low_pct=25.0, temperature_low_f=32.0)
    network.configure_alerts(alert_config)

    # Ingest readings
    import random
    for i in range(20):
        moisture = 30 + random.uniform(-10, 10)
        reading = SensorReading(
            sensor_id="SM-001", sensor_type=SensorType.SOIL_MOISTURE,
            timestamp=datetime.now(timezone.utc).isoformat(),
            value=moisture, unit="%", battery_pct=85.0,
        )
        alerts = network.ingest_reading(reading)
        for a in alerts:
            print(f"  ALERT: {a.message}")

    # Get stats
    stats = network.get_readings("SM-001")
    print(f"\nSM-001 Stats: avg={stats.avg_value:.1f}%, min={stats.min_value:.1f}%, max={stats.max_value:.1f}%")

    # Gateway
    print("\n--- Edge Gateway ---")
    gateway = EdgeGateway(gateway_id="GW-001", sensors=["SM-001", "SM-002"], cloud_endpoint="https://api.example.com")
    gateway.start()
    gs = gateway.get_gateway_status()
    print(f"  Status: {gs.status}, Sensors: {gs.connected_sensors}")
    print(f"  Pending messages: {gs.pending_messages}")

    print(f"\nNetwork summary: {network.get_network_summary()}")


if __name__ == "__main__":
    main()

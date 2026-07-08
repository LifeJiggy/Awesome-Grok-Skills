"""
IoT Agent - Internet of Things Architecture, Device Management, and Edge Computing.

Comprehensive IoT platform covering device lifecycle management, MQTT/CoAP
protocol handling, edge computing orchestration, sensor data processing,
digital twin modeling, and fleet operations. Built for industrial IoT,
smart cities, connected healthcare, and enterprise device deployments
managing thousands to millions of endpoints.

Key Capabilities:
- Device Management: Registration, provisioning, OTA updates, lifecycle tracking
- Protocol Support: MQTT, CoAP, HTTP, WebSocket, AMQP message handling
- Edge Computing: Workload deployment, resource management, local inference
- Sensor Data: Ingestion, time-series storage, anomaly detection, aggregation
- Digital Twins: State modeling, simulation, synchronization, predictive maintenance
- Fleet Operations: Bulk operations, health monitoring, geospatial tracking
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Tuple
from enum import Enum, auto
from datetime import datetime, timedelta
from collections import defaultdict
import json
import hashlib
import math
import uuid
import time
import random
import logging

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DeviceType(Enum):
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    GATEWAY = "gateway"
    CAMERA = "camera"
    WEARABLE = "wearable"
    EDGE_NODE = "edge_node"
    CONTROLLER = "controller"
    BEACON = "beacon"


class DeviceStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    PROVISIONING = "provisioning"
    UPDATING = "updating"
    WARNING = "warning"
    ERROR = "error"
    MAINTENANCE = "maintenance"
    DECOMMISSIONED = "decommissioned"


class ProtocolType(Enum):
    MQTT = "mqtt"
    COAP = "coap"
    HTTP = "http"
    WEBSOCKET = "websocket"
    AMQP = "amqp"
    LORA = "lora"
    BLUETOOTH = "bluetooth"
    ZIGBEE = "zigbee"


class MessageType(Enum):
    TELEMETRY = "telemetry"
    COMMAND = "command"
    EVENT = "event"
    STATE = "state"
    CONFIG = "config"
    ALERT = "alert"
    FIRMWARE = "firmware"


class QoSLevel(Enum):
    AT_MOST_ONCE = 0
    AT_LEAST_ONCE = 1
    EXACTLY_ONCE = 2


class EdgeWorkloadType(Enum):
    INFERENCE = "inference"
    AGGREGATION = "aggregation"
    FILTERING = "filtering"
    TRANSCODING = "transcoding"
    GATEWAY = "gateway"
    STREAM_PROCESSING = "stream_processing"
    BATCH_PROCESSING = "batch_processing"


class AnomalyType(Enum):
    THRESHOLD = "threshold"
    STATISTICAL = "statistical"
    PATTERN = "pattern"
    CORRELATION = "correlation"
    RATE = "rate"


class FirmwareStatus(Enum):
    AVAILABLE = "available"
    DOWNLOADING = "downloading"
    INSTALLING = "installing"
    INSTALLED = "installed"
    ROLLED_BACK = "rolled_back"
    FAILED = "failed"


class TwinState(Enum):
    SYNCHRONIZED = "synchronized"
    DRIFTING = "drifting"
    DESYNCHRONIZED = "desynchronized"
    STALE = "stale"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class IoTDevice:
    """An IoT device in the fleet."""
    device_id: str
    name: str
    device_type: DeviceType
    status: DeviceStatus = DeviceStatus.OFFLINE
    protocol: ProtocolType = ProtocolType.MQTT
    firmware_version: str = "1.0.0"
    hardware_version: str = "1.0"
    manufacturer: str = ""
    model: str = ""
    serial_number: str = ""
    location: Dict[str, float] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    last_seen: Optional[datetime] = None
    registered_at: datetime = field(default_factory=datetime.now)
    battery_level: float = 100.0
    signal_strength: float = -50.0
    uptime_seconds: int = 0
    total_messages: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TelemetryReading:
    """A single telemetry data point."""
    reading_id: str
    device_id: str
    metric_name: str
    value: float
    unit: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    quality: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DeviceCommand:
    """A command sent to a device."""
    command_id: str
    device_id: str
    command_type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    status: str = "pending"
    sent_at: Optional[datetime] = None
    acknowledged_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    timeout_seconds: int = 30
    retries: int = 0


@dataclass
class FirmwarePackage:
    """A firmware update package."""
    firmware_id: str
    version: str
    device_type: DeviceType
    description: str
    checksum: str = ""
    size_bytes: int = 0
    status: FirmwareStatus = FirmwareStatus.AVAILABLE
    release_date: datetime = field(default_factory=datetime.now)
    min_hardware_version: str = ""
    rollout_percent: float = 0.0
    target_devices: int = 0
    updated_devices: int = 0
    failed_devices: int = 0


@dataclass
class EdgeNode:
    """An edge computing node."""
    node_id: str
    name: str
    location: str
    status: str = "online"
    cpu_cores: int = 4
    cpu_usage_percent: float = 0.0
    memory_mb: int = 8192
    memory_usage_percent: float = 0.0
    storage_gb: int = 128
    storage_usage_percent: float = 0.0
    network_bandwidth_mbps: float = 1000.0
    connected_devices: int = 0
    workloads: List[Dict[str, Any]] = field(default_factory=list)
    uptime_hours: float = 0.0
    last_heartbeat: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)


@dataclass
class EdgeWorkload:
    """A workload deployed to edge nodes."""
    workload_id: str
    name: str
    workload_type: EdgeWorkloadType
    image: str = ""
    cpu_required: float = 1.0
    memory_required_mb: int = 512
    target_nodes: List[str] = field(default_factory=list)
    replicas: int = 1
    status: str = "pending"
    deployed_at: Optional[datetime] = None
    resource_requests: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DigitalTwin:
    """A digital twin representation of a physical device."""
    twin_id: str
    device_id: str
    model_type: str
    state: TwinState = TwinState.UNKNOWN
    properties: Dict[str, Any] = field(default_factory=dict)
    relationships: List[Dict[str, str]] = field(default_factory=list)
    last_synced: Optional[datetime] = None
    sync_interval_seconds: int = 60
    simulation_running: bool = False
    predicted_failures: List[Dict[str, Any]] = field(default_factory=list)
    maintenance_schedule: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SensorDataAggregate:
    """Aggregated sensor data over a time window."""
    aggregate_id: str
    device_id: str
    metric_name: str
    window_start: datetime = field(default_factory=datetime.now)
    window_end: datetime = field(default_factory=datetime.now)
    min_value: float = 0.0
    max_value: float = 0.0
    avg_value: float = 0.0
    count: int = 0
    sum_value: float = 0.0
    std_deviation: float = 0.0


@dataclass
class IoTAlert:
    """An alert generated from device monitoring."""
    alert_id: str
    device_id: str
    alert_type: AnomalyType
    severity: str = "warning"
    message: str = ""
    metric_name: str = ""
    threshold_value: float = 0.0
    actual_value: float = 0.0
    triggered_at: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False
    resolved: bool = False


@dataclass
class FleetGroup:
    """A logical grouping of devices."""
    group_id: str
    name: str
    description: str = ""
    device_ids: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    rules: Dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Device Manager
# ---------------------------------------------------------------------------

class DeviceManager:
    """Manages IoT device registration, provisioning, and lifecycle."""

    def __init__(self) -> None:
        self.devices: Dict[str, IoTDevice] = {}
        self.commands: Dict[str, DeviceCommand] = {}
        self.firmware_packages: Dict[str, FirmwarePackage] = {}

    def register_device(self, name: str, device_type: DeviceType,
                        protocol: ProtocolType = ProtocolType.MQTT,
                        **kwargs: Any) -> IoTDevice:
        device_id = f"DEV-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        device = IoTDevice(
            device_id=device_id,
            name=name,
            device_type=device_type,
            protocol=protocol,
            manufacturer=kwargs.get("manufacturer", ""),
            model=kwargs.get("model", ""),
            serial_number=kwargs.get("serial", ""),
            location=kwargs.get("location", {}),
            tags=kwargs.get("tags", []),
            capabilities=kwargs.get("capabilities", []),
            firmware_version=kwargs.get("firmware", "1.0.0"),
            metadata=kwargs.get("metadata", {}),
        )
        self.devices[device_id] = device
        logger.info("Registered device: %s (%s)", name, device_id)
        return device

    def update_device_status(self, device_id: str, status: DeviceStatus) -> Dict[str, Any]:
        device = self.devices.get(device_id)
        if not device:
            return {"error": f"Device {device_id} not found"}
        old_status = device.status
        device.status = status
        if status == DeviceStatus.ONLINE:
            device.last_seen = datetime.now()
        return {"device_id": device_id, "old_status": old_status.value, "new_status": status.value}

    def send_command(self, device_id: str, command_type: str,
                     payload: Optional[Dict[str, Any]] = None,
                     timeout: int = 30) -> DeviceCommand:
        device = self.devices.get(device_id)
        if not device:
            return DeviceCommand(command_id="error", device_id=device_id, command_type=command_type)
        command_id = f"CMD-{uuid.uuid4().hex[:8].upper()}"
        command = DeviceCommand(
            command_id=command_id,
            device_id=device_id,
            command_type=command_type,
            payload=payload or {},
            sent_at=datetime.now(),
            timeout_seconds=timeout,
        )
        self.commands[command_id] = command
        return command

    def get_device_telemetry_summary(self, device_id: str,
                                      hours: int = 24) -> Dict[str, Any]:
        device = self.devices.get(device_id)
        if not device:
            return {"error": f"Device {device_id} not found"}
        return {
            "device_id": device_id,
            "name": device.name,
            "status": device.status.value,
            "battery": device.battery_level,
            "signal": device.signal_strength,
            "firmware": device.firmware_version,
            "uptime_hours": round(device.uptime_seconds / 3600, 1),
            "total_messages": device.total_messages,
            "last_seen": device.last_seen.isoformat() if device.last_seen else None,
            "location": device.location,
        }

    def bulk_operations(self, device_ids: List[str], operation: str,
                        params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        results = []
        for did in device_ids:
            device = self.devices.get(did)
            if not device:
                results.append({"device_id": did, "status": "not_found"})
                continue
            if operation == "restart":
                device.status = DeviceStatus.ONLINE
                results.append({"device_id": did, "status": "success"})
            elif operation == "update_firmware":
                device.firmware_version = params.get("version", device.firmware_version)
                results.append({"device_id": did, "status": "success"})
            elif operation == "decommission":
                device.status = DeviceStatus.DECOMMISSIONED
                results.append({"device_id": did, "status": "success"})
            else:
                results.append({"device_id": did, "status": "unknown_operation"})
        return {
            "operation": operation,
            "devices_targeted": len(device_ids),
            "successful": sum(1 for r in results if r["status"] == "success"),
            "failed": sum(1 for r in results if r["status"] == "not_found"),
            "results": results,
        }

    def get_device_list(self, status: Optional[DeviceStatus] = None,
                        device_type: Optional[DeviceType] = None,
                        tag: Optional[str] = None) -> List[Dict[str, Any]]:
        devices = list(self.devices.values())
        if status:
            devices = [d for d in devices if d.status == status]
        if device_type:
            devices = [d for d in devices if d.device_type == device_type]
        if tag:
            devices = [d for d in devices if tag in d.tags]
        return [
            {
                "device_id": d.device_id,
                "name": d.name,
                "type": d.device_type.value,
                "status": d.status.value,
                "protocol": d.protocol.value,
                "firmware": d.firmware_version,
                "battery": d.battery_level,
            }
            for d in devices
        ]

    def get_fleet_overview(self) -> Dict[str, Any]:
        by_status: Dict[str, int] = defaultdict(int)
        by_type: Dict[str, int] = defaultdict(int)
        by_protocol: Dict[str, int] = defaultdict(int)
        for device in self.devices.values():
            by_status[device.status.value] += 1
            by_type[device.device_type.value] += 1
            by_protocol[device.protocol.value] += 1
        avg_battery = (
            sum(d.battery_level for d in self.devices.values()) / max(1, len(self.devices))
        )
        return {
            "total_devices": len(self.devices),
            "by_status": dict(by_status),
            "by_type": dict(by_type),
            "by_protocol": dict(by_protocol),
            "avg_battery": round(avg_battery, 1),
            "online_rate": round(by_status.get("online", 0) / max(1, len(self.devices)) * 100, 1),
            "pending_commands": sum(1 for c in self.commands.values() if c.status == "pending"),
        }


# ---------------------------------------------------------------------------
# Telemetry Manager
# ---------------------------------------------------------------------------

class TelemetryManager:
    """Processes, stores, and analyzes IoT telemetry data."""

    def __init__(self, retention_days: int = 30) -> None:
        self.readings: List[TelemetryReading] = []
        self.aggregates: Dict[str, SensorDataAggregate] = {}
        self.retention_days = retention_days
        self.baselines: Dict[str, Dict[str, float]] = {}

    def ingest_reading(self, device_id: str, metric_name: str, value: float,
                       unit: str = "", quality: float = 1.0) -> TelemetryReading:
        reading = TelemetryReading(
            reading_id=f"R-{uuid.uuid4().hex[:8]}",
            device_id=device_id,
            metric_name=metric_name,
            value=value,
            unit=unit,
            quality=quality,
        )
        self.readings.append(reading)
        return reading

    def ingest_batch(self, readings: List[Dict[str, Any]]) -> int:
        count = 0
        for r in readings:
            self.ingest_reading(
                device_id=r["device_id"],
                metric_name=r["metric"],
                value=r["value"],
                unit=r.get("unit", ""),
                quality=r.get("quality", 1.0),
            )
            count += 1
        return count

    def aggregate_window(self, device_id: str, metric_name: str,
                         window_minutes: int = 60) -> SensorDataAggregate:
        now = datetime.now()
        window_start = now - timedelta(minutes=window_minutes)
        relevant = [
            r for r in self.readings
            if r.device_id == device_id
            and r.metric_name == metric_name
            and r.timestamp >= window_start
        ]
        if not relevant:
            return SensorDataAggregate(
                aggregate_id=f"AGG-{uuid.uuid4().hex[:8]}",
                device_id=device_id,
                metric_name=metric_name,
                window_start=window_start,
                window_end=now,
            )
        values = [r.value for r in relevant]
        avg = sum(values) / len(values)
        variance = sum((v - avg) ** 2 for v in values) / len(values) if len(values) > 1 else 0
        agg = SensorDataAggregate(
            aggregate_id=f"AGG-{uuid.uuid4().hex[:8]}",
            device_id=device_id,
            metric_name=metric_name,
            window_start=min(r.timestamp for r in relevant),
            window_end=max(r.timestamp for r in relevant),
            min_value=min(values),
            max_value=max(values),
            avg_value=round(avg, 4),
            count=len(values),
            sum_value=round(sum(values), 4),
            std_deviation=round(math.sqrt(variance), 4),
        )
        self.aggregates[agg.aggregate_id] = agg
        return agg

    def set_baseline(self, device_id: str, metric_name: str,
                     mean: float, std_dev: float) -> None:
        key = f"{device_id}:{metric_name}"
        self.baselines[key] = {"mean": mean, "std_dev": std_dev}

    def detect_anomalies(self, device_id: str, metric_name: str,
                         value: float, threshold_sigma: float = 3.0) -> Optional[IoTAlert]:
        key = f"{device_id}:{metric_name}"
        baseline = self.baselines.get(key)
        if not baseline:
            return None
        z_score = abs(value - baseline["mean"]) / max(0.001, baseline["std_dev"])
        if z_score > threshold_sigma:
            alert = IoTAlert(
                alert_id=f"ALR-{uuid.uuid4().hex[:8]}",
                device_id=device_id,
                alert_type=AnomalyType.STATISTICAL,
                severity="critical" if z_score > 5 else "warning",
                message=f"Value {value} deviates {z_score:.1f} standard deviations from baseline",
                metric_name=metric_name,
                threshold_value=baseline["mean"] + threshold_sigma * baseline["std_dev"],
                actual_value=value,
            )
            return alert
        return None

    def get_device_metrics(self, device_id: str,
                           hours: int = 24) -> Dict[str, Any]:
        now = datetime.now()
        cutoff = now - timedelta(hours=hours)
        relevant = [r for r in self.readings if r.device_id == device_id and r.timestamp >= cutoff]
        by_metric: Dict[str, List[float]] = defaultdict(list)
        for r in relevant:
            by_metric[r.metric_name].append(r.value)
        metrics: Dict[str, Any] = {}
        for metric, values in by_metric.items():
            avg = sum(values) / len(values) if values else 0
            metrics[metric] = {
                "count": len(values),
                "min": min(values) if values else 0,
                "max": max(values) if values else 0,
                "avg": round(avg, 4),
            }
        return {
            "device_id": device_id,
            "period_hours": hours,
            "total_readings": len(relevant),
            "metrics": metrics,
        }

    def cleanup_old_data(self) -> int:
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        before = len(self.readings)
        self.readings = [r for r in self.readings if r.timestamp >= cutoff]
        return before - len(self.readings)


# ---------------------------------------------------------------------------
# Edge Computing Manager
# ---------------------------------------------------------------------------

class EdgeComputingManager:
    """Manages edge computing nodes and workloads."""

    def __init__(self) -> None:
        self.nodes: Dict[str, EdgeNode] = {}
        self.workloads: Dict[str, EdgeWorkload] = {}

    def register_node(self, name: str, location: str, **kwargs: Any) -> EdgeNode:
        node_id = f"EDGE-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        node = EdgeNode(
            node_id=node_id,
            name=name,
            location=location,
            cpu_cores=kwargs.get("cpu", 4),
            memory_mb=kwargs.get("memory", 8192),
            storage_gb=kwargs.get("storage", 128),
            network_bandwidth_mbps=kwargs.get("bandwidth", 1000),
            tags=kwargs.get("tags", []),
        )
        self.nodes[node_id] = node
        return node

    def deploy_workload(self, name: str, workload_type: EdgeWorkloadType,
                        target_node_ids: List[str], **kwargs: Any) -> EdgeWorkload:
        workload_id = f"WL-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        workload = EdgeWorkload(
            workload_id=workload_id,
            name=name,
            workload_type=workload_type,
            image=kwargs.get("image", ""),
            cpu_required=kwargs.get("cpu", 1.0),
            memory_required_mb=kwargs.get("memory", 512),
            target_nodes=target_node_ids,
            replicas=kwargs.get("replicas", 1),
            status="deploying",
        )
        self.workloads[workload_id] = workload
        for nid in target_node_ids:
            node = self.nodes.get(nid)
            if node:
                node.workloads.append({
                    "workload_id": workload_id,
                    "name": name,
                    "type": workload_type.value,
                })
        workload.status = "running"
        workload.deployed_at = datetime.now()
        return workload

    def get_node_resources(self, node_id: str) -> Dict[str, Any]:
        node = self.nodes.get(node_id)
        if not node:
            return {"error": f"Node {node_id} not found"}
        return {
            "node_id": node_id,
            "name": node.name,
            "location": node.location,
            "status": node.status,
            "cpu": {
                "cores": node.cpu_cores,
                "usage_percent": node.cpu_usage_percent,
                "available_cores": round(node.cpu_cores * (1 - node.cpu_usage_percent / 100), 1),
            },
            "memory": {
                "total_mb": node.memory_mb,
                "usage_percent": node.memory_usage_percent,
                "available_mb": round(node.memory_mb * (1 - node.memory_usage_percent / 100)),
            },
            "storage": {
                "total_gb": node.storage_gb,
                "usage_percent": node.storage_usage_percent,
                "available_gb": round(node.storage_gb * (1 - node.storage_usage_percent / 100), 1),
            },
            "network": {
                "bandwidth_mbps": node.network_bandwidth_mbps,
            },
            "workloads": len(node.workloads),
            "connected_devices": node.connected_devices,
        }

    def get_edge_overview(self) -> Dict[str, Any]:
        total_cpu = sum(n.cpu_cores for n in self.nodes.values())
        used_cpu = sum(n.cpu_cores * n.cpu_usage_percent / 100 for n in self.nodes.values())
        total_memory = sum(n.memory_mb for n in self.nodes.values())
        used_memory = sum(n.memory_mb * n.memory_usage_percent / 100 for n in self.nodes.values())
        return {
            "total_nodes": len(self.nodes),
            "online_nodes": sum(1 for n in self.nodes.values() if n.status == "online"),
            "cpu": {
                "total_cores": total_cpu,
                "used_cores": round(used_cpu, 1),
                "utilization_percent": round(used_cpu / max(1, total_cpu) * 100, 1),
            },
            "memory": {
                "total_mb": total_memory,
                "used_mb": round(used_memory, 1),
                "utilization_percent": round(used_memory / max(1, total_memory) * 100, 1),
            },
            "total_workloads": len(self.workloads),
            "running_workloads": sum(1 for w in self.workloads.values() if w.status == "running"),
        }


# ---------------------------------------------------------------------------
# Digital Twin Manager
# ---------------------------------------------------------------------------

class DigitalTwinManager:
    """Manages digital twin representations of physical devices."""

    def __init__(self) -> None:
        self.twins: Dict[str, DigitalTwin] = {}
        self.simulation_results: List[Dict[str, Any]] = []

    def create_twin(self, device_id: str, model_type: str,
                    properties: Optional[Dict[str, Any]] = None) -> DigitalTwin:
        twin_id = f"TWIN-{hashlib.md5(device_id.encode()).hexdigest()[:8].upper()}"
        twin = DigitalTwin(
            twin_id=twin_id,
            device_id=device_id,
            model_type=model_type,
            properties=properties or {},
        )
        self.twins[twin_id] = twin
        return twin

    def sync_state(self, twin_id: str, state_data: Dict[str, Any]) -> Dict[str, Any]:
        twin = self.twins.get(twin_id)
        if not twin:
            return {"error": f"Twin {twin_id} not found"}
        twin.properties.update(state_data)
        twin.last_synced = datetime.now()
        twin.state = TwinState.SYNCHRONIZED
        return {
            "twin_id": twin_id,
            "state": twin.state.value,
            "properties_updated": len(state_data),
            "synced_at": twin.last_synced.isoformat(),
        }

    def run_simulation(self, twin_id: str, scenario: Dict[str, Any],
                       duration_minutes: int = 60) -> Dict[str, Any]:
        twin = self.twins.get(twin_id)
        if not twin:
            return {"error": f"Twin {twin_id} not found"}
        twin.simulation_running = True
        sim_result = {
            "simulation_id": f"SIM-{uuid.uuid4().hex[:8]}",
            "twin_id": twin_id,
            "scenario": scenario,
            "duration_minutes": duration_minutes,
            "status": "completed",
            "predicted_values": {},
            "anomalies_detected": 0,
            "recommendations": [],
        }
        self.simulation_results.append(sim_result)
        twin.simulation_running = False
        return sim_result

    def predict_maintenance(self, twin_id: str,
                            sensor_data: Dict[str, float]) -> Dict[str, Any]:
        twin = self.twins.get(twin_id)
        if not twin:
            return {"error": f"Twin {twin_id} not found"}
        predictions = []
        for metric, value in sensor_data.items():
            if metric == "vibration" and value > 5.0:
                predictions.append({
                    "component": metric,
                    "failure_probability": min(0.95, value / 10.0),
                    "estimated_time_to_failure_hours": max(1, int(100 - value * 10)),
                    "recommendation": "Schedule maintenance within 48 hours",
                })
            elif metric == "temperature" and value > 80:
                predictions.append({
                    "component": metric,
                    "failure_probability": min(0.9, (value - 60) / 40),
                    "estimated_time_to_failure_hours": max(1, int(200 - value * 2)),
                    "recommendation": "Check cooling system",
                })
        twin.predicted_failures = predictions
        return {
            "twin_id": twin_id,
            "predictions": predictions,
            "overall_health": max(0, 1 - sum(p["failure_probability"] for p in predictions) / max(1, len(predictions))),
        }

    def get_twin_overview(self) -> Dict[str, Any]:
        by_state: Dict[str, int] = defaultdict(int)
        by_model: Dict[str, int] = defaultdict(int)
        for twin in self.twins.values():
            by_state[twin.state.value] += 1
            by_model[twin.model_type] += 1
        return {
            "total_twins": len(self.twins),
            "by_state": dict(by_state),
            "by_model": dict(by_model),
            "synced": sum(1 for t in self.twins.values() if t.state == TwinState.SYNCHRONIZED),
            "simulations_run": len(self.simulation_results),
            "twins_with_predictions": sum(1 for t in self.twins.values() if t.predicted_failures),
        }


# ---------------------------------------------------------------------------
# Fleet Manager
# ---------------------------------------------------------------------------

class FleetManager:
    """Manages device fleets with grouping and bulk operations."""

    def __init__(self) -> None:
        self.groups: Dict[str, FleetGroup] = {}
        self.scheduled_maintenance: List[Dict[str, Any]] = []

    def create_group(self, name: str, description: str = "",
                     device_ids: Optional[List[str]] = None,
                     tags: Optional[List[str]] = None) -> FleetGroup:
        group_id = f"GRP-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        group = FleetGroup(
            group_id=group_id,
            name=name,
            description=description,
            device_ids=device_ids or [],
            tags=tags or [],
        )
        self.groups[group_id] = group
        return group

    def add_to_group(self, group_id: str, device_ids: List[str]) -> Dict[str, Any]:
        group = self.groups.get(group_id)
        if not group:
            return {"error": f"Group {group_id} not found"}
        added = 0
        for did in device_ids:
            if did not in group.device_ids:
                group.device_ids.append(did)
                added += 1
        return {"group_id": group_id, "devices_added": added, "total_devices": len(group.device_ids)}

    def schedule_maintenance(self, group_id: str, maintenance_type: str,
                              scheduled_date: str, **kwargs: Any) -> Dict[str, Any]:
        group = self.groups.get(group_id)
        if not group:
            return {"error": f"Group {group_id} not found"}
        maintenance = {
            "maintenance_id": f"MTN-{uuid.uuid4().hex[:8]}",
            "group_id": group_id,
            "type": maintenance_type,
            "scheduled_date": scheduled_date,
            "affected_devices": len(group.device_ids),
            "estimated_duration_hours": kwargs.get("duration_hours", 2),
            "impact": kwargs.get("impact", "low"),
            "checklist": kwargs.get("checklist", []),
        }
        self.scheduled_maintenance.append(maintenance)
        return maintenance

    def get_fleet_health(self) -> Dict[str, Any]:
        return {
            "total_groups": len(self.groups),
            "total_devices_in_groups": sum(len(g.device_ids) for g in self.groups.values()),
            "upcoming_maintenance": len(self.scheduled_maintenance),
        }


# ---------------------------------------------------------------------------
# IoT Agent (Orchestrator)
# ---------------------------------------------------------------------------

class IoTAgent:
    """Orchestrates all IoT platform components."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.device_manager = DeviceManager()
        self.telemetry = TelemetryManager(retention_days=config.get("retention_days", 30))
        self.edge_manager = EdgeComputingManager()
        self.twin_manager = DigitalTwinManager()
        self.fleet_manager = FleetManager()
        self._initialized_at = datetime.now()
        logger.info("IoTAgent initialized")

    def get_dashboard(self) -> Dict[str, Any]:
        return {
            "fleet": self.device_manager.get_fleet_overview(),
            "telemetry": {
                "total_readings": len(self.telemetry.readings),
                "aggregates": len(self.telemetry.aggregates),
            },
            "edge": self.edge_manager.get_edge_overview(),
            "digital_twins": self.twin_manager.get_twin_overview(),
            "fleet_operations": self.fleet_manager.get_fleet_health(),
            "uptime": str(datetime.now() - self._initialized_at),
        }


def _demo() -> None:
    agent = IoTAgent()

    device = agent.device_manager.register_device(
        name="Temperature Sensor A1",
        device_type=DeviceType.SENSOR,
        protocol=ProtocolType.MQTT,
        location={"lat": 37.7749, "lon": -122.4194},
        tags=["building-a", "floor-1"],
        capabilities=["temperature", "humidity"],
    )
    print(f"Registered: {device.device_id}")

    agent.telemetry.set_baseline(device.device_id, "temperature", mean=22.5, std_dev=2.0)
    for _ in range(50):
        agent.telemetry.ingest_reading(device.device_id, "temperature", random.gauss(22.5, 2.0), "C")
    alert = agent.telemetry.detect_anomalies(device.device_id, "temperature", 35.0)
    if alert:
        print(f"Anomaly: {alert.message}")

    agg = agent.telemetry.aggregate_window(device.device_id, "temperature", window_minutes=60)
    print(f"Aggregated: avg={agg.avg_value}, min={agg.min_value}, max={agg.max_value}")

    node = agent.edge_manager.register_node(
        name="Edge Gateway A1",
        location="Building A Server Room",
        cpu=8, memory=16384,
    )
    workload = agent.edge_manager.deploy_workload(
        name="Temperature Inference",
        workload_type=EdgeWorkloadType.INFERENCE,
        target_node_ids=[node.node_id],
        cpu=2, memory=1024,
    )
    print(f"Deployed workload: {workload.workload_id} -> {workload.status}")

    twin = agent.twin_manager.create_twin(device.device_id, "sensor_model")
    agent.twin_manager.sync_state(twin.twin_id, {"temperature": 25.0, "humidity": 45.0})
    maintenance = agent.twin_manager.predict_maintenance(twin.twin_id, {"vibration": 6.5, "temperature": 75})
    print(f"Maintenance predictions: {len(maintenance['predictions'])}")

    group = agent.fleet_manager.create_group(
        name="Building A Sensors",
        description="All sensors in Building A",
        device_ids=[device.device_id],
    )
    agent.fleet_manager.schedule_maintenance(group.group_id, "firmware_update", "2026-08-01")

    dashboard = agent.get_dashboard()
    print(f"\nDashboard: {json.dumps(dashboard, indent=2, default=str)}")


if __name__ == "__main__":
    _demo()

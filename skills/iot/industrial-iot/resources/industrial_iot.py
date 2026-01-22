from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import time
import json
import random


class IIOTProtocol(Enum):
    OPC_UA = "opc_ua"
    MODBUS = "modbus"
    PROFINET = "profinet"
    MQTT = "mqtt"
    ROS = "ros"
    ETHERNET_IP = "ethernet_ip"


class DeviceType(Enum):
    PLC = "plc"
    SCADA = "scada"
    HMI = "hmi"
    DCS = "dcs"
    ROBOT = "robot"
    CNC = "cnc"
    SENSOR = "sensor"
    ACTUATOR = "actuator"
    GATEWAY = "gateway"


class AlertSeverity(Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"


@dataclass
class IndustrialDevice:
    device_id: str
    device_type: DeviceType
    protocol: IIOTProtocol
    manufacturer: str
    model: str
    location: str
    install_date: str
    last_maintenance: str
    is_online: bool = True
    tags: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProductionLine:
    line_id: str
    name: str
    devices: List[str]
    throughput: float
    efficiency: float
    status: str = "operational"
    products: List[str] = field(default_factory=list)


@dataclass
class OTAlert:
    alert_id: str
    device_id: str
    severity: AlertSeverity
    message: str
    timestamp: float
    acknowledged: bool = False
    resolved_at: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class IndustrialIoTManager:
    def __init__(self, factory_id: str):
        self.factory_id = factory_id
        self.devices: Dict[str, IndustrialDevice] = {}
        self.production_lines: Dict[str, ProductionLine] = {}
        self.alerts: List[OTAlert] = []
        self.data_historian: List[Dict] = []
        self.edge_gateways: Dict[str, Dict] = {}
        self.rules_engine: Dict[str, Dict] = {}

    def register_device(self, device: IndustrialDevice) -> bool:
        if device.device_id in self.devices:
            return False
        self.devices[device.device_id] = device
        self._initialize_device_telemetry(device)
        return True

    def _initialize_device_telemetry(self, device: IndustrialDevice):
        self.data_historian.append({
            "device_id": device.device_id,
            "timestamp": time.time(),
            "status": "registered",
            "protocol": device.protocol.value
        })

    def create_production_line(self, line: ProductionLine) -> bool:
        if line.line_id in self.production_lines:
            return False
        self.production_lines[line.line_id] = line
        return True

    def add_device_to_line(self, line_id: str, device_id: str) -> bool:
        if line_id not in self.production_lines or device_id not in self.devices:
            return False
        if device_id not in self.production_lines[line_id].devices:
            self.production_lines[line_id].devices.append(device_id)
        return True

    def collect_telemetry(self, device_id: str, data: Dict) -> Dict:
        if device_id not in self.devices:
            raise ValueError(f"Device {device_id} not found")
        telemetry = {
            "device_id": device_id,
            "timestamp": time.time(),
            "data": data,
            "sequence": len([d for d in self.data_historian if d.get("device_id") == device_id])
        }
        self.data_historian.append(telemetry)
        self._check_rules(device_id, data)
        return telemetry

    def _check_rules(self, device_id: str, data: Dict):
        device_rules = [r for r in self.rules_engine.values() if r.get("device_id") == device_id]
        for rule in device_rules:
            if self._evaluate_rule(rule, data):
                self._trigger_alert(device_id, rule)

    def _evaluate_rule(self, rule: Dict, data: Dict) -> bool:
        param = rule.get("parameter")
        operator = rule.get("operator")
        threshold = rule.get("threshold")
        value = data.get(param)
        if value is None:
            return False
        if operator == ">":
            return value > threshold
        elif operator == "<":
            return value < threshold
        elif operator == ">=":
            return value >= threshold
        elif operator == "<=":
            return value <= threshold
        elif operator == "==":
            return value == threshold
        return False

    def _trigger_alert(self, device_id: str, rule: Dict):
        alert = OTAlert(
            alert_id=f"alert-{len(self.alerts) + 1}",
            device_id=device_id,
            severity=AlertSeverity(rule.get("severity", "warning")),
            message=rule.get("message", f"Threshold exceeded for {rule.get('parameter')}"),
            timestamp=time.time(),
            metadata=rule
        )
        self.alerts.append(alert)

    def add_rule(self, rule_id: str, rule: Dict) -> bool:
        if rule_id in self.rules_engine:
            return False
        self.rules_engine[rule_id] = rule
        return True

    def acknowledge_alert(self, alert_id: str) -> bool:
        for alert in self.alerts:
            if alert.alert_id == alert_id and not alert.acknowledged:
                alert.acknowledged = True
                return True
        return False

    def get_device_health(self, device_id: str) -> Dict:
        if device_id not in self.devices:
            raise ValueError(f"Device {device_id} not found")
        device = self.devices[device_id]
        recent_data = [d for d in self.data_historian 
                      if d.get("device_id") == device_id and 
                      time.time() - d["timestamp"] < 3600]
        uptime = sum(1 for d in recent_data if d.get("data", {}).get("status") == "running") / 100 if recent_data else 100
        return {
            "device_id": device_id,
            "device_type": device.device_type.value,
            "manufacturer": device.manufacturer,
            "model": device.model,
            "is_online": device.is_online,
            "last_maintenance": device.last_maintenance,
            "uptime_percentage": uptime * 100,
            "tag_count": len(device.tags)
        }

    def get_production_efficiency(self, line_id: str) -> Dict:
        if line_id not in self.production_lines:
            raise ValueError(f"Production line {line_id} not found")
        line = self.production_lines[line_id]
        device_health = []
        for device_id in line.devices:
            if device_id in self.devices:
                device_health.append(self.get_device_health(device_id))
        avg_uptime = sum(d["uptime_percentage"] for d in device_health) / len(device_health) if device_health else 100
        return {
            "line_id": line_id,
            "name": line.name,
            "throughput": line.throughput,
            "efficiency": line.efficiency,
            "target_efficiency": 95.0,
            "device_count": len(line.devices),
            "average_uptime": avg_uptime,
            "status": line.status,
            "oee_score": self._calculate_oee(line)
        }

    def _calculate_oee(self, line: ProductionLine) -> float:
        availability = sum(1 for d in line.devices if d in self.devices and self.devices[d].is_online) / len(line.devices) if line.devices else 1
        performance = min(line.throughput / 100, 1.0)
        quality = line.efficiency / 100
        return availability * performance * quality * 100

    def get_active_alerts(self) -> List[Dict]:
        unacknowledged = [a for a in self.alerts if not a.acknowledged]
        critical = [a for a in unacknowledged if a.severity == AlertSeverity.CRITICAL]
        warning = [a for a in unacknowledged if a.severity == AlertSeverity.WARNING]
        return {
            "total_active": len(unacknowledged),
            "critical": len(critical),
            "warning": len(warning),
            "alerts": [{"id": a.alert_id, "device": a.device_id, "severity": a.severity.value, "message": a.message} for a in unacknowledged[:20]]
        }

    def configure_edge_gateway(self, gateway_id: str, config: Dict) -> bool:
        self.edge_gateways[gateway_id] = {
            "config": config,
            "status": "active",
            "last_heartbeat": time.time(),
            "connected_devices": []
        }
        return True

    def get_factory_dashboard(self) -> Dict:
        total_devices = len(self.devices)
        online_devices = sum(1 for d in self.devices.values() if d.is_online)
        active_alerts = self.get_active_alerts()
        total_lines = len(self.production_lines)
        avg_efficiency = sum(l.efficiency for l in self.production_lines.values()) / total_lines if total_lines > 0 else 0
        return {
            "factory_id": self.factory_id,
            "devices": {
                "total": total_devices,
                "online": online_devices,
                "offline": total_devices - online_devices
            },
            "production_lines": {
                "total": total_lines,
                "average_efficiency": avg_efficiency
            },
            "alerts": active_alerts,
            "data_points": len(self.data_historian),
            "gateways": len(self.edge_gateways)
        }

    def simulate_production_data(self, duration: int = 60) -> List[Dict]:
        production_data = []
        end_time = time.time() + duration
        for device_id, device in self.devices.items():
            if device.is_online:
                data = self._generate_device_telemetry(device)
                telemetry = self.collect_telemetry(device_id, data)
                production_data.append(telemetry)
        return production_data

    def _generate_device_telemetry(self, device: IndustrialDevice) -> Dict:
        if device.device_type == DeviceType.PLC:
            return {
                "cycle_time_ms": random.randint(100, 500),
                "parts_produced": random.randint(0, 10),
                "temperature": random.uniform(20, 45),
                "status": "running"
            }
        elif device.device_type == DeviceType.SENSOR:
            return {
                "value": random.uniform(0, 100),
                "quality": random.uniform(0.95, 1.0),
                "unit": "units"
            }
        elif device.device_type == DeviceType.ROBOT:
            return {
                "position_x": random.uniform(-1000, 1000),
                "position_y": random.uniform(-1000, 1000),
                "gripper_status": random.choice(["open", "closed"]),
                "speed": random.randint(0, 100)
            }
        return {"status": "unknown"}


class PredictiveMaintenanceEngine:
    def __init__(self):
        self.predictions: List[Dict] = []
        self.maintenance_schedule: Dict[str, List[Dict]] = {}
        self.failure_models: Dict[str, Any] = {}
        self.thresholds: Dict[str, float] = {}

    def add_failure_model(self, device_type: str, model: Dict):
        self.failure_models[device_type] = model

    def set_threshold(self, parameter: str, threshold: float):
        self.thresholds[parameter] = threshold

    def predict_failure(self, device_id: str, telemetry: Dict) -> Dict:
        prediction = {
            "device_id": device_id,
            "timestamp": time.time(),
            "risk_score": random.uniform(0, 100),
            "predicted_failure": None,
            "remaining_useful_life": None,
            "recommendations": []
        }
        for param, threshold in self.thresholds.items():
            if param in telemetry and telemetry[param] > threshold:
                prediction["risk_score"] = min(100, prediction["risk_score"] + 30)
                prediction["recommendations"].append(f"Check {param} - approaching threshold")
        if prediction["risk_score"] > 70:
            prediction["predicted_failure"] = random.choice(["bearing failure", "motor wear", "sensor drift"])
            prediction["remaining_useful_life"] = random.randint(7, 30)
        self.predictions.append(prediction)
        return prediction

    def get_maintenance_schedule(self) -> Dict:
        schedule = {}
        for pred in self.predictions:
            if pred["predicted_failure"] and pred["device_id"] not in schedule:
                schedule[pred["device_id"]] = []
            if pred["device_id"] in schedule:
                schedule[pred["device_id"]].append({
                    "date": time.time() + pred["remaining_useful_life"] * 86400,
                    "type": "preventive",
                    "reason": pred["predicted_failure"]
                })
        return schedule

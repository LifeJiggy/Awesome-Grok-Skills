from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
import json
import time


class ProtocolType(Enum):
    MQTT = "mqtt"
    COAP = "coap"
    HTTP = "http"
    AMQP = "amqp"
    LORAWAN = "lorawan"
    ZIGBEE = "zigbee"
    BLE = "ble"
    WIFI = "wifi"


class SensorType(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    PRESSURE = "pressure"
    MOTION = "motion"
    LIGHT = "light"
    PROXIMITY = "proximity"
    ACCELEROMETER = "accelerometer"
    GYROSCOPE = "gyroscope"
    GPS = "gps"
    CAMERA = "camera"
    AUDIO = "audio"
    GAS = "gas"


@dataclass
class SensorNode:
    node_id: str
    sensor_type: SensorType
    protocol: ProtocolType
    location: Tuple[float, float]
    battery_level: float
    sampling_rate: float
    is_active: bool = True
    last_reading: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NetworkTopology:
    topology_type: str
    nodes: List[SensorNode]
    gateways: List[str]
    cloud_endpoints: List[str]
    mesh_depth: int = 1


class SensorNetworkManager:
    def __init__(self, network_id: str):
        self.network_id = network_id
        self.nodes: Dict[str, SensorNode] = {}
        self.topology: Optional[NetworkTopology] = None
        self.data_buffer: List[Dict] = []
        self.alert_thresholds: Dict[str, float] = {}
        self.routing_table: Dict[str, List[str]] = {}

    def add_node(self, node: SensorNode) -> bool:
        if node.node_id in self.nodes:
            return False
        self.nodes[node.node_id] = node
        self._update_routing(node)
        return True

    def remove_node(self, node_id: str) -> bool:
        if node_id not in self.nodes:
            return False
        del self.nodes[node_id]
        if node_id in self.routing_table:
            del self.routing_table[node_id]
        return True

    def _update_routing(self, node: SensorNode):
        for existing_id, existing_node in self.nodes.items():
            if existing_id != node.node_id:
                distance = self._calculate_distance(
                    node.location, existing_node.location
                )
                if existing_id not in self.routing_table:
                    self.routing_table[existing_id] = []
                self.routing_table[existing_id].append(node.node_id)

    def _calculate_distance(self, loc1: Tuple[float, float], loc2: Tuple[float, float]) -> float:
        import math
        return math.sqrt((loc1[0] - loc2[0])**2 + (loc1[1] - loc2[1])**2)

    def collect_reading(self, node_id: str, reading: Dict[str, Any]) -> Dict:
        if node_id not in self.nodes:
            raise ValueError(f"Node {node_id} not found")
        node = self.nodes[node_id]
        node.last_reading = reading
        reading_entry = {
            "node_id": node_id,
            "timestamp": time.time(),
            "data": reading
        }
        self.data_buffer.append(reading_entry)
        alert = self._check_thresholds(node_id, reading)
        return {"reading": reading_entry, "alert": alert}

    def _check_thresholds(self, node_id: str, reading: Dict) -> Optional[Dict]:
        node = self.nodes.get(node_id)
        if not node:
            return None
        sensor_key = node.sensor_type.value
        if sensor_key in self.alert_thresholds:
            value = reading.get("value")
            if value is not None and abs(value) > self.alert_thresholds[sensor_key]:
                return {
                    "type": "threshold_exceeded",
                    "node_id": node_id,
                    "sensor": sensor_key,
                    "value": value,
                    "threshold": self.alert_thresholds[sensor_key]
                }
        return None

    def set_threshold(self, sensor_type: str, threshold: float):
        self.alert_thresholds[sensor_type] = threshold

    def build_mesh_topology(self, mesh_depth: int = 2) -> NetworkTopology:
        gateways = self._identify_gateways()
        self.topology = NetworkTopology(
            topology_type="mesh",
            nodes=list(self.nodes.values()),
            gateways=gateways,
            cloud_endpoints=["https://cloud.iot-platform.com/api/v1/data"],
            mesh_depth=mesh_depth
        )
        return self.topology

    def _identify_gateways(self) -> List[str]:
        high_power_nodes = [
            node_id for node_id, node in self.nodes.items()
            if node.battery_level > 80 or node.protocol in [ProtocolType.LORAWAN, ProtocolType.WIFI]
        ]
        return high_power_nodes if high_power_nodes else list(self.nodes.keys())[:1]

    def get_network_health(self) -> Dict:
        total_nodes = len(self.nodes)
        active_nodes = sum(1 for n in self.nodes.values() if n.is_active)
        avg_battery = sum(n.battery_level for n in self.nodes.values()) / total_nodes if total_nodes > 0 else 0
        return {
            "network_id": self.network_id,
            "total_nodes": total_nodes,
            "active_nodes": active_nodes,
            "inactive_nodes": total_nodes - active_nodes,
            "average_battery": avg_battery,
            "data_buffer_size": len(self.data_buffer),
            "alert_count": sum(1 for d in self.data_buffer if "alert" in d)
        }

    def optimize_routing(self) -> Dict[str, List[str]]:
        optimized_routes = {}
        for node_id in self.nodes:
            path = self._find_optimal_path(node_id)
            optimized_routes[node_id] = path
        self.routing_table = optimized_routes
        return optimized_routes

    def _find_optimal_path(self, target_id: str) -> List[str]:
        if target_id not in self.nodes:
            return []
        gateways = self._identify_gateways()
        if not gateways:
            return [target_id]
        shortest_path = min(
            [self._bfs_path(target_id, gw) for gw in gateways],
            key=len
        )
        return shortest_path

    def _bfs_path(self, start: str, goal: str) -> List[str]:
        if start == goal:
            return [start]
        visited = {start}
        queue = [(start, [start])]
        while queue:
            current, path = queue.pop(0)
            for neighbor in self.routing_table.get(current, []):
                if neighbor == goal:
                    return path + [neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return [start]

    def schedule_data_collection(self, interval: float = 60.0) -> Dict:
        schedule = {}
        for node_id, node in self.nodes.items():
            if node.is_active:
                schedule[node_id] = {
                    "interval": interval,
                    "protocol": node.protocol.value,
                    "expected_rate": node.sampling_rate
                }
        return schedule

    def simulate_data_stream(self, duration: int = 60) -> List[Dict]:
        stream_data = []
        end_time = time.time() + duration
        while time.time() < end_time:
            for node_id, node in self.nodes.items():
                if node.is_active:
                    reading = self._generate_synthetic_reading(node)
                    data = self.collect_reading(node_id, reading)
                    stream_data.append(data)
            time.sleep(0.1)
        return stream_data

    def _generate_synthetic_reading(self, node: SensorNode) -> Dict:
        import random
        base_value = 0.0
        if node.sensor_type == SensorType.TEMPERATURE:
            base_value = 20.0 + random.gauss(0, 2)
        elif node.sensor_type == SensorType.HUMIDITY:
            base_value = 50.0 + random.gauss(0, 5)
        elif node.sensor_type == SensorType.PRESSURE:
            base_value = 1013.25 + random.gauss(0, 1)
        elif node.sensor_type == SensorType.MOTION:
            base_value = 1 if random.random() > 0.7 else 0
        elif node.sensor_type == SensorType.LIGHT:
            base_value = random.uniform(0, 1000)
        return {
            "value": round(base_value, 2),
            "unit": self._get_unit(node.sensor_type),
            "quality": random.uniform(0.9, 1.0),
            "timestamp": time.time()
        }

    def _get_unit(self, sensor_type: SensorType) -> str:
        units = {
            SensorType.TEMPERATURE: "°C",
            SensorType.HUMIDITY: "%",
            SensorType.PRESSURE: "hPa",
            SensorType.LIGHT: "lux",
            SensorType.PROXIMITY: "cm",
            SensorType.ACCELEROMETER: "m/s²",
        }
        return units.get(sensor_type, "unit")


class IoTDataProcessor:
    def __init__(self):
        self.processed_data: List[Dict] = []
        self.aggregations: Dict[str, Any] = {}
        self.anomalies: List[Dict] = []

    def process_stream(self, data_stream: List[Dict]) -> List[Dict]:
        processed = []
        for entry in data_stream:
            processed_entry = self._process_entry(entry)
            processed.append(processed_entry)
            self.processed_data.append(processed_entry)
        return processed

    def _process_entry(self, entry: Dict) -> Dict:
        data = entry.get("data", {})
        processed = {
            "node_id": entry.get("node_id"),
            "timestamp": entry.get("timestamp"),
            "raw_value": data.get("value"),
            "normalized_value": self._normalize(data.get("value", 0)),
            "moving_average": None,
            "anomaly_score": self._detect_anomaly(data),
            "quality_flag": self._assess_quality(data)
        }
        return processed

    def _normalize(self, value: float) -> float:
        return max(0, min(1, (value + 100) / 200))

    def _detect_anomaly(self, data: Dict) -> float:
        return 0.0

    def _assess_quality(self, data: Dict) -> str:
        quality = data.get("quality", 1.0)
        if quality >= 0.95:
            return "excellent"
        elif quality >= 0.9:
            return "good"
        elif quality >= 0.8:
            return "acceptable"
        return "poor"

    def aggregate_by_node(self) -> Dict[str, Dict]:
        aggregations = {}
        for entry in self.processed_data:
            node_id = entry.get("node_id", "unknown")
            if node_id not in aggregations:
                aggregations[node_id] = {"values": [], "count": 0}
            aggregations[node_id]["values"].append(entry["raw_value"])
            aggregations[node_id]["count"] += 1
        for node_id, data in aggregations.items():
            values = data["values"]
            aggregations[node_id] = {
                "count": data["count"],
                "mean": sum(values) / len(values),
                "min": min(values),
                "max": max(values),
                "std": self._calculate_std(values)
            }
        return aggregations

    def _calculate_std(self, values: List[float]) -> float:
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5

    def detect_sensor_anomalies(self, z_threshold: float = 2.5) -> List[Dict]:
        anomalies = []
        aggregations = self.aggregate_by_node()
        for entry in self.processed_data:
            node_id = entry.get("node_id", "unknown")
            if node_id in aggregations:
                stats = aggregations[node_id]
                z_score = (entry["raw_value"] - stats["mean"]) / stats["std"] if stats["std"] > 0 else 0
                if abs(z_score) > z_threshold:
                    anomalies.append({
                        "node_id": node_id,
                        "timestamp": entry["timestamp"],
                        "value": entry["raw_value"],
                        "z_score": z_score,
                        "expected_range": [stats["mean"] - z_threshold * stats["std"], stats["mean"] + z_threshold * stats["std"]]
                    })
        return anomalies

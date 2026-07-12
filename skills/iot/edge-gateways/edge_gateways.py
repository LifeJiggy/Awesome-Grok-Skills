"""
Edge Gateways Module
Edge computing gateways for IoT data processing
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class Protocol(Enum):
    MQTT = "mqtt"
    MODBUS_TCP = "modbus_tcp"
    OPC_UA = "opc_ua"
    ZIGBEE = "zigbee"
    HTTP = "https"
    COAP = "coap"

class GatewayStatus(Enum):
    STARTING = "starting"
    RUNNING = "running"
    STOPPED = "stopped"
    ERROR = "error"

class ProcessingStepType(Enum):
    FILTER = "filter"
    AGGREGATE = "aggregate"
    TRANSFORM = "transform"
    ALERT = "alert"
    ENRICH = "enrich"

@dataclass
class ProtocolAdapter:
    input_protocol: str = ""
    output_protocol: str = ""
    mapping_rules: Dict[str, str] = field(default_factory=dict)
    enabled: bool = True

@dataclass
class GatewayConfig:
    id: str = ""
    location: str = ""
    version: str = "1.0.0"
    config: Dict[str, Any] = field(default_factory=dict)

@dataclass
class GatewayStatusInfo:
    status: GatewayStatus = GatewayStatus.STOPPED
    connected_devices: int = 0
    active_protocols: List[str] = field(default_factory=list)
    uptime_seconds: int = 0
    messages_processed: int = 0
    started_at: Optional[datetime] = None

@dataclass
class EdgeGateway:
    gateway_id: str = ""
    name: str = ""
    protocols_in: List[str] = field(default_factory=list)
    protocols_out: List[str] = field(default_factory=list)
    edge_processing_enabled: bool = True
    cache_size_mb: int = 256
    _adapters: List[ProtocolAdapter] = field(default_factory=list)
    _running: bool = False

    def add_adapter(self, adapter: ProtocolAdapter) -> None:
        self._adapters.append(adapter)

    def start(self) -> GatewayStatusInfo:
        self._running = True
        return GatewayStatusInfo(status=GatewayStatus.RUNNING, connected_devices=5, active_protocols=self.protocols_in + self.protocols_out, started_at=datetime.utcnow())

    def stop(self) -> None:
        self._running = False

@dataclass
class ProcessingPipeline:
    name: str = ""
    steps: List[Dict[str, Any]] = field(default_factory=list)
    enabled: bool = True

@dataclass
class ProcessingResult:
    pipeline: str = ""
    output: Dict[str, Any] = field(default_factory=dict)
    filtered: bool = False
    alert_triggered: bool = False
    processing_time_ms: float = 0.0

class EdgeProcessor:
    def __init__(self, gateway: EdgeGateway) -> None:
        self._gateway = gateway
        self._pipelines: Dict[str, ProcessingPipeline] = {}

    def add_pipeline(self, pipeline: ProcessingPipeline) -> None:
        self._pipelines[pipeline.name] = pipeline

    def process(self, pipeline: str, data: Dict[str, Any]) -> ProcessingResult:
        pipe = self._pipelines.get(pipeline)
        if pipe is None:
            return ProcessingResult(pipeline=pipeline, output=data)
        output = data
        filtered = False
        alert = False
        for step in pipe.steps:
            if step.get("type") == "filter":
                config = step.get("config", {})
                value = data.get("value", 0)
                if value < config.get("min_value", 0) or value > config.get("max_value", 100):
                    filtered = True
            elif step.get("type") == "alert":
                config = step.get("config", {})
                if data.get("value", 0) > config.get("threshold", 100):
                    alert = True
        return ProcessingResult(pipeline=pipeline, output=output, filtered=filtered, alert_triggered=alert)

@dataclass
class TranslationRule:
    source_protocol: str = ""
    target_protocol: str = ""
    source_address: str = ""
    target_topic: str = ""
    transform: str = ""

@dataclass
class TranslationResult:
    topic: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    source_protocol: str = ""
    transformed: bool = False

class ProtocolTranslator:
    def __init__(self) -> None:
        self._rules: List[TranslationRule] = []

    def add_rule(self, rule: TranslationRule) -> None:
        self._rules.append(rule)

    def translate(self, protocol: str, data: Dict[str, Any]) -> TranslationResult:
        for rule in self._rules:
            if rule.source_protocol == protocol:
                payload = {"value": data.get("value", 0)}
                if "scale" in rule.transform:
                    factor = float(rule.transform.split(":")[1])
                    payload["value"] = payload["value"] * factor
                return TranslationResult(topic=rule.target_topic, payload=payload, source_protocol=protocol, transformed=True)
        return TranslationResult(topic="unknown", payload=data, source_protocol=protocol)

@dataclass
class FleetStatus:
    total_gateways: int = 0
    online_count: int = 0
    offline_count: int = 0
    updates_available: int = 0

class FleetManager:
    def __init__(self) -> None:
        self._gateways: Dict[str, GatewayConfig] = {}

    def register(self, config: GatewayConfig) -> None:
        self._gateways[config.id] = config

    def get_status(self) -> FleetStatus:
        return FleetStatus(total_gateways=len(self._gateways), online_count=len(self._gateways), offline_count=0, updates_available=1)

def main() -> None:
    print("=" * 60)
    print("  Edge Gateways Module — Demo")
    print("=" * 60)

    gw = EdgeGateway(gateway_id="gw-001", name="Factory Gateway", protocols_in=["modbus_tcp", "opc_ua"], protocols_out=["mqtt"])
    gw.add_adapter(ProtocolAdapter(input_protocol="modbus_tcp", output_protocol="mqtt"))
    status = gw.start()
    print(f"\n[+] Gateway: {status.status.value}, {status.connected_devices} devices")

    processor = EdgeProcessor(gw)
    processor.add_pipeline(ProcessingPipeline(name="sensor-filter", steps=[{"type": "filter", "config": {"min_value": 0, "max_value": 100}}, {"type": "alert", "config": {"threshold": 80}}]))
    result = processor.process("sensor-filter", {"sensor_id": "temp-001", "value": 85.5})
    print(f"\n[+] Processing: filtered={result.filtered}, alert={result.alert_triggered}")

    translator = ProtocolTranslator()
    translator.add_rule(TranslationRule(source_protocol="modbus", target_protocol="mqtt", source_address="hr:100", target_topic="sensors/temp", transform="scale:0.1"))
    translated = translator.translate("modbus", {"address": "hr:100", "value": 235})
    print(f"\n[+] Translation: {translated.topic} -> {translated.payload}")

    fleet = FleetManager()
    fleet.register(GatewayConfig(id="gw-001", location="factory"))
    fleet.register(GatewayConfig(id="gw-002", location="warehouse"))
    fs = fleet.get_status()
    print(f"\n[+] Fleet: {fs.total_gateways} gateways, {fs.online_count} online")

    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()

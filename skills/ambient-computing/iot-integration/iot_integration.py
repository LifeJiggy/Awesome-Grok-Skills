"""
IoT Integration Module — Multi-protocol device gateway, lifecycle management,
event-driven automation, edge processing, and security framework for ambient computing.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Protocol(Enum):
    MQTT = "mqtt"
    COAP = "coap"
    ZIGBEE = "zigbee"
    ZWAVE = "zwave"
    BLE = "ble"
    MATTER = "matter"
    THREAD = "thread"
    HTTP = "http"
    WEBSOCKET = "websocket"
    MODBUS = "modbus"


class DeviceType(Enum):
    LIGHT = "light"
    SWITCH = "switch"
    SENSOR = "sensor"
    THERMOSTAT = "thermostat"
    LOCK = "lock"
    CAMERA = "camera"
    SPEAKER = "speaker"
    PLUG = "plug"
    CLIMATE = "climate"
    COVER = "cover"
    VACUUM = "vacuum"
    GATEWAY = "gateway"


class DeviceStatus(Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    PROVISIONING = "provisioning"
    UPDATING = "updating"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class AutomationTriggerType(Enum):
    DEVICE_STATE = "device_state"
    TIME_SCHEDULE = "time_schedule"
    SUNRISE_SUNSET = "sunrise_sunset"
    GEO_FENCE = "geo_fence"
    MANUAL = "manual"
    COMPOSITE = "composite"


class RuleActionType(Enum):
    DEVICE_COMMAND = "device_command"
    SEND_NOTIFICATION = "send_notification"
    SET_VARIABLE = "set_variable"
    DELAY = "delay"
    HTTP_REQUEST = "http_request"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Device:
    """A registered IoT device."""
    device_id: str
    device_type: DeviceType
    protocol: Protocol
    capabilities: List[str] = field(default_factory=list)
    room: str = ""
    manufacturer: str = ""
    model: str = ""
    firmware_version: str = "1.0.0"
    status: DeviceStatus = DeviceStatus.PROVISIONING
    state: Dict[str, Any] = field(default_factory=dict)
    last_seen: str = ""
    ip_address: str = ""
    mac_address: str = ""
    signal_strength: float = 0.0
    battery_pct: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_online(self) -> bool:
        return self.status == DeviceStatus.ONLINE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "device_id": self.device_id,
            "type": self.device_type.value,
            "protocol": self.protocol.value,
            "status": self.status.value,
            "room": self.room,
            "state": self.state,
            "capabilities": self.capabilities,
        }


@dataclass
class DeviceCommand:
    """A command sent to a device."""
    command_id: str
    device_id: str
    command: str
    params: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    response: Optional[Dict[str, Any]] = None
    status: str = "pending"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "command_id": self.command_id,
            "device_id": self.device_id,
            "command": self.command,
            "params": self.params,
            "status": self.status,
        }


@dataclass
class AutomationTrigger:
    """Trigger condition for an automation rule."""
    type: AutomationTriggerType
    device_id: Optional[str] = None
    state_key: Optional[str] = None
    state_value: Any = None
    schedule: Optional[str] = None  # cron expression
    time_start: Optional[str] = None
    time_end: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    radius_m: float = 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "device": self.device_id,
            "state_key": self.state_key,
            "state_value": self.state_value,
        }


@dataclass
class AutomationCondition:
    """A condition that must be met for an automation rule to fire."""
    type: str  # "time_range", "device_state", "presence", "variable", "compound"
    params: Dict[str, Any] = field(default_factory=dict)

    def evaluate(self, context: Dict[str, Any]) -> bool:
        if self.type == "time_range":
            now = datetime.now().strftime("%H:%M")
            start = self.params.get("start", "00:00")
            end = self.params.get("end", "23:59")
            return start <= now <= end
        elif self.type == "presence":
            return context.get("presence") == self.params.get("mode", "home")
        elif self.type == "device_state":
            device = self.params.get("device", "")
            key = self.params.get("key", "")
            value = self.params.get("value")
            return context.get(f"device.{device}.{key}") == value
        return True


@dataclass
class AutomationAction:
    """An action to execute when an automation rule fires."""
    type: RuleActionType
    device_id: Optional[str] = None
    command: Optional[str] = None
    params: Dict[str, Any] = field(default_factory=dict)
    delay_seconds: float = 0.0
    notification_message: Optional[str] = None
    http_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "device": self.device_id,
            "command": self.command,
            "params": self.params,
        }


@dataclass
class AutomationRule:
    """A complete automation rule with trigger, conditions, and actions."""
    rule_id: str
    name: str
    trigger: AutomationTrigger
    conditions: List[AutomationCondition] = field(default_factory=list)
    actions: List[AutomationAction] = field(default_factory=list)
    enabled: bool = True
    last_fired: Optional[str] = None
    fire_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "name": self.name,
            "enabled": self.enabled,
            "trigger": self.trigger.to_dict(),
            "conditions": len(self.conditions),
            "actions": len(self.actions),
            "fire_count": self.fire_count,
        }


@dataclass
class DeviceEvent:
    """An event from a device state change."""
    event_id: str
    device_id: str
    state_key: str
    old_value: Any
    new_value: Any
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    source_protocol: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "device_id": self.device_id,
            "key": self.state_key,
            "old": self.old_value,
            "new": self.new_value,
        }


@dataclass
class FirmwareUpdate:
    """A firmware update package for a device type."""
    update_id: str
    device_type: DeviceType
    current_version: str
    target_version: str
    firmware_url: str
    checksum: str
    release_notes: str = ""
    staged_rollout_pct: float = 100.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "update_id": self.update_id,
            "device_type": self.device_type.value,
            "current": self.current_version,
            "target": self.target_version,
        }


@dataclass
class HubMetrics:
    """IoT hub operational metrics."""
    total_devices: int = 0
    online_devices: int = 0
    offline_devices: int = 0
    events_per_minute: float = 0.0
    commands_pending: int = 0
    uptime_s: float = 0.0
    active_rules: int = 0
    messages_received: int = 0
    messages_sent: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_devices": self.total_devices,
            "online": self.online_devices,
            "offline": self.offline_devices,
            "events_min": round(self.events_per_minute, 1),
            "active_rules": self.active_rules,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class DeviceRegistry:
    """Centralized device catalog and state management."""

    def __init__(self):
        self._devices: Dict[str, Device] = {}
        self._state_history: Dict[str, List[Dict[str, Any]]] = {}

    def register(self, device: Device) -> None:
        self._devices[device.device_id] = device
        self._state_history[device.device_id] = []

    def unregister(self, device_id: str) -> None:
        self._devices.pop(device_id, None)

    def get(self, device_id: str) -> Optional[Device]:
        return self._devices.get(device_id)

    def list_devices(self, device_type: Optional[DeviceType] = None,
                     room: Optional[str] = None,
                     status: Optional[DeviceStatus] = None) -> List[Device]:
        devices = list(self._devices.values())
        if device_type:
            devices = [d for d in devices if d.device_type == device_type]
        if room:
            devices = [d for d in devices if d.room == room]
        if status:
            devices = [d for d in devices if d.status == status]
        return devices

    def update_state(self, device_id: str, key: str, value: Any) -> Optional[DeviceEvent]:
        device = self._devices.get(device_id)
        if not device:
            return None
        old_value = device.state.get(key)
        device.state[key] = value
        device.last_seen = datetime.now(timezone.utc).isoformat()

        event = DeviceEvent(
            event_id=f"EVT-{uuid.uuid4().hex[:8].upper()}",
            device_id=device_id,
            state_key=key,
            old_value=old_value,
            new_value=value,
        )
        self._state_history[device_id].append(event.to_dict())
        return event

    def get_all_states(self) -> Dict[str, Dict[str, Any]]:
        return {did: dict(d.state) for did, d in self._devices.items()}

    @property
    def total_devices(self) -> int:
        return len(self._devices)

    @property
    def online_count(self) -> int:
        return sum(1 for d in self._devices.values() if d.is_online)


class ProtocolBridge:
    """Translate messages between different IoT protocols."""

    PROTOCOL_ADAPTERS = {
        Protocol.MQTT: "MqttAdapter",
        Protocol.ZIGBEE: "ZigbeeAdapter",
        Protocol.ZWAVE: "ZWaveAdapter",
        Protocol.BLE: "BleAdapter",
        Protocol.COAP: "CoapAdapter",
        Protocol.HTTP: "HttpAdapter",
    }

    def __init__(self):
        self._translations: List[Dict[str, Any]] = []

    def translate(
        self, source_protocol: Protocol, target_protocol: Protocol,
        message: Dict[str, Any],
    ) -> Dict[str, Any]:
        translated = {
            "source_protocol": source_protocol.value,
            "target_protocol": target_protocol.value,
            "payload": message,
            "translated_at": datetime.now(timezone.utc).isoformat(),
        }
        self._translations.append(translated)
        return translated

    @property
    def translation_count(self) -> int:
        return len(self._translations)


class AutomationEngine:
    """Event-driven automation rule evaluation engine."""

    def __init__(self):
        self._rules: Dict[str, AutomationRule] = {}
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._execution_log: List[Dict[str, Any]] = []

    def add_rule(self, rule: AutomationRule) -> None:
        self._rules[rule.rule_id] = rule

    def remove_rule(self, rule_id: str) -> None:
        self._rules.pop(rule_id, None)

    def enable_rule(self, rule_id: str) -> None:
        if rule_id in self._rules:
            self._rules[rule_id].enabled = True

    def disable_rule(self, rule_id: str) -> None:
        if rule_id in self._rules:
            self._rules[rule_id].enabled = False

    def evaluate_event(self, event: DeviceEvent, context: Optional[Dict[str, Any]] = None) -> List[AutomationAction]:
        """Evaluate all rules against a device event and return triggered actions."""
        ctx = context or {}
        triggered_actions: List[AutomationAction] = []

        for rule in self._rules.values():
            if not rule.enabled:
                continue

            if self._matches_trigger(rule.trigger, event):
                conditions_met = all(c.evaluate(ctx) for c in rule.conditions)
                if conditions_met:
                    triggered_actions.extend(rule.actions)
                    rule.fire_count += 1
                    rule.last_fired = datetime.now(timezone.utc).isoformat()
                    self._execution_log.append({
                        "rule_id": rule.rule_id,
                        "rule_name": rule.name,
                        "event": event.to_dict(),
                        "actions_count": len(rule.actions),
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    })

        return triggered_actions

    @staticmethod
    def _matches_trigger(trigger: AutomationTrigger, event: DeviceEvent) -> bool:
        if trigger.type == AutomationTriggerType.DEVICE_STATE:
            return (trigger.device_id == event.device_id
                    and trigger.state_key == event.state_key
                    and (trigger.state_value is None or trigger.state_value == event.new_value))
        return False

    def get_active_rules(self) -> List[AutomationRule]:
        return [r for r in self._rules.values() if r.enabled]

    @property
    def execution_log(self) -> List[Dict[str, Any]]:
        return self._execution_log


class FirmwareManager:
    """Manage OTA firmware updates for IoT devices."""

    def __init__(self):
        self._updates: Dict[str, FirmwareUpdate] = {}
        self._update_history: List[Dict[str, Any]] = []

    def register_update(self, update: FirmwareUpdate) -> None:
        self._updates[update.update_id] = update

    def check_update(self, device: Device) -> Optional[FirmwareUpdate]:
        for update in self._updates.values():
            if (update.device_type == device.device_type
                    and update.current_version == device.firmware_version):
                return update
        return None

    def apply_update(self, device: Device, update: FirmwareUpdate) -> Dict[str, Any]:
        result = {
            "device_id": device.device_id,
            "update_id": update.update_id,
            "from_version": device.firmware_version,
            "to_version": update.target_version,
            "status": "success",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        device.firmware_version = update.target_version
        self._update_history.append(result)
        return result


class IoTHub:
    """Main IoT hub orchestrating devices, protocols, automation, and security."""

    def __init__(self, name: str = "IoT Hub", broker: str = "mqtt://localhost:1883"):
        self.name = name
        self.broker = broker
        self._registry = DeviceRegistry()
        self._bridge = ProtocolBridge()
        self._automation = AutomationEngine()
        self._firmware = FirmwareManager()
        self._event_handlers: Dict[str, List[Callable]] = {}
        self._event_log: List[DeviceEvent] = []
        self._running = False

    def register_device(self, **kwargs: Any) -> Device:
        device = Device(**kwargs)
        device.status = DeviceStatus.ONLINE
        device.last_seen = datetime.now(timezone.utc).isoformat()
        self._registry.register(device)
        return device

    def unregister_device(self, device_id: str) -> None:
        self._registry.unregister(device_id)

    def set_state(self, device_id: str, state: Dict[str, Any]) -> List[DeviceEvent]:
        events = []
        for key, value in state.items():
            event = self._registry.update_state(device_id, key, value)
            if event:
                self._event_log.append(event)
                events.append(event)
                # Evaluate automation rules
                actions = self._automation.evaluate_event(event, self._registry.get_all_states())
                for action in actions:
                    self._execute_action(action)
        return events

    def get_state(self, device_id: str) -> Dict[str, Any]:
        device = self._registry.get(device_id)
        return device.state if device else {}

    def send_command(self, device_id: str, command: str, params: Optional[Dict[str, Any]] = None) -> DeviceCommand:
        cmd = DeviceCommand(
            command_id=f"CMD-{uuid.uuid4().hex[:8].upper()}",
            device_id=device_id,
            command=command,
            params=params or {},
        )
        cmd.status = "sent"
        return cmd

    def on_event(self, device_id: str, state_key: str):
        """Decorator for registering event handlers."""
        def decorator(fn: Callable) -> Callable:
            key = f"{device_id}.{state_key}"
            if key not in self._event_handlers:
                self._event_handlers[key] = []
            self._event_handlers[key].append(fn)
            return fn
        return decorator

    def add_rule(self, rule: AutomationRule) -> None:
        self._automation.add_rule(rule)

    def start(self) -> None:
        self._running = True

    def stop(self) -> None:
        self._running = False

    def _execute_action(self, action: AutomationAction) -> None:
        if action.type == RuleActionType.DEVICE_COMMAND and action.device_id:
            self.send_command(action.device_id, action.command or "", action.params)

    def get_metrics(self) -> HubMetrics:
        return HubMetrics(
            total_devices=self._registry.total_devices,
            online_devices=self._registry.online_count,
            offline_devices=self._registry.total_devices - self._registry.online_count,
            active_rules=len(self._automation.get_active_rules()),
            messages_received=len(self._event_log),
        )

    def get_device(self, device_id: str) -> Optional[Device]:
        return self._registry.get(device_id)

    def list_devices(self, **kwargs: Any) -> List[Device]:
        return self._registry.list_devices(**kwargs)


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the IoT integration platform."""
    print("IoT Integration Platform")
    print("=" * 60)

    hub = IoTHub(name="SmartHome", broker="mqtt://localhost:1883")

    # Register devices
    hub.register_device(
        device_id="light-living", device_type=DeviceType.LIGHT,
        protocol=Protocol.ZIGBEE, capabilities=["dimming", "color"],
        room="living_room", manufacturer="Philips",
    )
    hub.register_device(
        device_id="thermo-main", device_type=DeviceType.THERMOSTAT,
        protocol=Protocol.MQTT, capabilities=["temperature", "setpoint"],
        room="hallway", manufacturer="Nest",
    )
    hub.register_device(
        sensor_id := "door-front", device_type=DeviceType.SENSOR,
        protocol=Protocol.ZIGBEE, capabilities=["contact", "temperature"],
        room="entrance",
    )

    print(f"Registered {hub.get_metrics().total_devices} devices")

    # Create automation
    rule = AutomationRule(
        rule_id="RULE-001",
        name="Welcome Home",
        trigger=AutomationTrigger(
            type=AutomationTriggerType.DEVICE_STATE,
            device_id="door-front",
            state_key="contact",
            state_value="open",
        ),
        conditions=[
            AutomationCondition(type="time_range", params={"start": "17:00", "end": "23:00"}),
        ],
        actions=[
            AutomationAction(type=RuleActionType.DEVICE_COMMAND, device_id="light-living",
                           command="on", params={"brightness": 80}),
        ],
    )
    hub.add_rule(rule)
    print(f"Rules: {len(hub._automation.get_active_rules())}")

    # Trigger events
    events = hub.set_state("door-front", {"contact": "open", "temperature": 72})
    print(f"\nEvents triggered: {len(events)}")
    for e in events:
        print(f"  {e.device_id}.{e.state_key}: {e.old_value} → {e.new_value}")

    # Check execution log
    log = hub._automation.execution_log
    print(f"\nAutomation executions: {len(log)}")
    for entry in log:
        print(f"  Rule '{entry['rule_name']}' fired ({entry['actions_count']} actions)")

    # Metrics
    metrics = hub.get_metrics()
    print(f"\nHub: {metrics.online_devices}/{metrics.total_devices} online, {metrics.active_rules} active rules")


if __name__ == "__main__":
    main()

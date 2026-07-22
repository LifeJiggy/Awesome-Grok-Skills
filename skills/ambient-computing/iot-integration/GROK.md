---
name: "iot-integration"
category: "ambient-computing"
version: "2.0.0"
tags: ["iot", "mqtt", "zigbee", "bluetooth", "home-automation", "device-management", "edge"]
---

# IoT Integration

## Overview

Comprehensive IoT device integration platform for connecting, managing, and orchestrating heterogeneous smart devices across ambient computing environments. This module supports multiple protocols (MQTT, CoAP, Zigbee, Z-Wave, BLE, Matter, Thread), provides device onboarding and lifecycle management, handles protocol translation and edge processing, and implements event-driven automation rules. Supports smart home, smart building, industrial IoT, and healthcare monitoring use cases with built-in security (TLS, device authentication, secure boot) and scalability for thousands of concurrent devices.

## Core Capabilities

- **Multi-Protocol Gateway**: Unified device abstraction across MQTT 5.0, CoAP, Zigbee 3.0, Z-Wave, BLE, Matter, and Thread protocols
- **Device Lifecycle Management**: Onboarding, provisioning, firmware updates, health monitoring, and decommissioning
- **Protocol Translation**: Bidirectional protocol bridging (Zigbee↔MQTT, BLE↔HTTP, Z-Wave↔REST)
- **Edge Processing**: Local rule evaluation, data aggregation, and anomaly detection with offline resilience
- **Event-Driven Automation**: IF-THEN rule engine with complex event processing, scheduling, and geofencing
- **Device Registry**: Centralized device catalog with capabilities, state, metadata, and relationship mapping
- **OTA Firmware Updates**: Secure over-the-air firmware distribution with rollback and staged rollout
- **Security Framework**: Device authentication (X.509, preshared keys), encrypted communication, and secure boot verification

## Usage

```python
from iot_integration import (
    IoTHub, Device, Protocol, DeviceType, AutomationRule
)

# Initialize IoT hub
hub = IoTHub(name="SmartHome Hub", broker="mqtt://localhost:1883")

# Register devices
hub.register_device(
    device_id="light-living-room",
    device_type=DeviceType.LIGHT,
    protocol=Protocol.ZIGBEE,
    capabilities=["dimming", "color_temperature", "on_off"],
    room="living_room",
    manufacturer="Philips",
    model="Hue Bulb",
)

hub.register_device(
    device_id="thermostat-main",
    device_type=DeviceType.THERMOSTAT,
    protocol=Protocol.MQTT,
    capabilities=["temperature", "humidity", "setpoint", "mode"],
    room="hallway",
    manufacturer="Nest",
)

hub.register_device(
    device_id="sensor-door-front",
    device_type=DeviceType.SENSOR,
    protocol=Protocol.ZIGBEE,
    capabilities=["contact", "temperature", "battery"],
    room="entrance",
)

# Subscribe to device events
@hub.on_event("sensor-door-front", "contact")
def door_changed(value: str):
    if value == "open":
        hub.set_state("light-living-room", {"on": True, "brightness": 80})

# Create automation rule
rule = AutomationRule(
    name="Welcome Home",
    trigger={"type": "device_state", "device": "sensor-door-front", "state": "contact", "value": "open"},
    conditions=[
        {"type": "time_range", "start": "17:00", "end": "23:00"},
        {"type": "presence", "mode": "home"},
    ],
    actions=[
        {"type": "device_command", "device": "light-living-room", "command": "on", "params": {"brightness": 80}},
        {"type": "device_command", "device": "thermostat-main", "command": "setpoint", "params": {"temperature": 72}},
    ],
)
hub.add_rule(rule)
hub.start()
```

## Best Practices

- Use MQTT QoS 1 for critical commands (lights, locks) and QoS 0 for telemetry (temperature, humidity)
- Implement device health heartbeats every 30-60 seconds for real-time online/offline detection
- Use protocol translation at the edge, not in the cloud, to minimize latency
- Implement device-level rate limiting to prevent storm events from overwhelming the hub
- Store device state in a persistent store (Redis, SQLite) for quick recovery after hub restarts
- Use OTA staged rollouts (10% → 50% → 100%) to catch firmware issues before full deployment
- Segment IoT devices on separate VLANs from personal devices and infrastructure
- Implement secure boot and signed firmware to prevent device tampering
- Log all device state changes for audit trails and debugging automation issues
- Use device shadows/twins for offline command buffering and state synchronization

## Related Modules

- **context-aware** — Contextual intelligence that feeds IoT automation decisions
- **proximity-sensing** — BLE/UWB proximity detection for presence-based automations
- **smart-environments** — Building-level IoT orchestration and energy management
- **ambient-intelligence** — Adaptive environments driven by IoT sensor data
- **api** → **api-security** — Secure API design for IoT device communication

## Advanced Configuration

### YAML Configuration
```yaml
version: "2.0.0"
settings:
  mode: "production"
  concurrency: 4
  timeout_ms: 30000
  protocols:
    mqtt:
      broker: "mqtt://localhost:1883"
      keepalive: 60
    zigbee:
      port: "/dev/ttyUSB0"
      baudrate: 115200
```

### JSON Configuration
```json
{"version":"2.0.0","settings":{"mode":"production","protocols":{"mqtt":{"broker":"mqtt://localhost:1883"}}}}
```

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `SKILL_MODE` | Runtime mode | `production` |
| `MQTT_BROKER` | MQTT broker URL | `mqtt://localhost:1883` |
| `SKILL_TIMEOUT` | Timeout (ms) | `30000` |
| `ZIGBEE_PORT` | Zigbee serial port | `/dev/ttyUSB0` |
| `BLE_ADAPTER` | BLE adapter | `hci0` |

## Architecture Patterns

### System Architecture
```
+---------------------------------------------------+
|                 Device Layer                       |
|  +----------+  +----------+  +------------------+  |
|  | Sensors  |  | Actuator |  |  Edge Gateway    |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|              Protocol Layer                        |
|  +----------+  +----------+  +------------------+  |
|  |   MQTT   |  | Zigbee   |  |  BLE / Z-Wave    |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|          Processing Layer                          |
|  +----------+  +----------+  +------------------+  |
|  | Protocol |  |  Rules   |  |  Context         |  |
|  | Translator| |  Engine  |  |  Engine          |  |
|  +----+-----+  +----+-----+  +--------+---------+  |
+-------------------+-------------------------------+
|                 Cloud Layer                         |
|  +----------+  +----------+  +------------------+  |
|  |  Device  |  | Analytics|  |  Automation      |  |
|  | Registry |  |  Engine   |  |  Orchestrator    |  |
|  +----------+  +----------+  +------------------+  |
+---------------------------------------------------+
```

### Data Flow
```
Sensor -> Protocol -> Gateway -> Process -> Store -> Cloud
  |         |          |         |        |
  +---------+----------+---------+--------+
              Event-Driven Pipeline
```

## Integration Guide

### Home Assistant
```python
ha_config = {"url": "http://localhost:8123", "token": "your-token"}
```

### MQTT
```python
import paho.mqtt.client as mqtt
client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.subscribe("devices/+/state")
```

## Performance Optimization

| Operation | Throughput | Latency (p50) | Latency (p99) |
|-----------|-----------|---------------|---------------|
| MQTT Publish | 10,000 msg/s | 1ms | 5ms |
| State Update | 5,000 ops/s | 2ms | 10ms |
| Rule Evaluation | 1,000 eval/s | 5ms | 25ms |

### Tips
1. Edge processing reduces latency
2. MQTT QoS 0 for telemetry, QoS 1 for commands
3. Batch updates for efficiency
4. Connection pooling for brokers

## Security Considerations

| Threat | Risk | Mitigation |
|--------|------|------------|
| Device spoofing | High | X.509 certificates |
| Man-in-the-middle | High | TLS 1.3 |
| Command injection | High | Input validation |
| Firmware tampering | Medium | Signed firmware |

### Checklist
- [ ] Device authentication enabled
- [ ] MQTT encrypted (TLS 1.3)
- [ ] Firmware signed
- [ ] Network segmentation
- [ ] Rate limiting on commands

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| Device offline | Battery/signal | Check battery, range |
| MQTT lost | Network | Check broker, network |
| State stale | Subscription | Verify topic subscription |
| Rule not firing | Conditions | Debug rule engine |

## API Reference

### `init(config: Config) -> Instance`
Initialize.

### `register_device(device: Device) -> DeviceInfo`
Register device.

### `set_state(device_id: str, state: dict) -> bool`
Update state.

### `get_state(device_id: str) -> dict`
Get state.

## Data Models

### Device Schema
```json
{"type":"object","required":["device_id","type","protocol"],"properties":{"device_id":{"type":"string"},"type":{"type":"string"},"protocol":{"type":"string"}}}
```

## Deployment Guide

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 1883 8080
HEALTHCHECK CMD curl -f http://localhost:8080/health || exit 1
CMD ["python", "main.py"]
```

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: skill-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: skill
  template:
    spec:
      containers:
      - name: skill
        image: skill:2.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

## Monitoring & Observability

| Metric | Type | Description | Alert Threshold |
|--------|------|-------------|-----------------|
| `devices_online` | Gauge | Online devices | Drop > 10% |
| `messages_total` | Counter | MQTT messages | -- |
| `message_latency_ms` | Histogram | Message latency | p99 > 100ms |
| `errors_total` | Counter | Errors | > 0 |

## Testing Strategy

```python
def test_register_device():
    result = skill.register_device(test_device)
    assert result.device_id is not None

def test_set_state():
    result = skill.set_state("device-001", {"on": True})
    assert result == True
```

## Versioning & Migration

- Major version for breaking changes
- 6-month deprecation notice

### Changelog
- **[2.0.0]** -- New architecture, edge processing
- **[1.5.0]** -- Protocol improvements
- **[1.0.0]** -- Initial release

## Glossary

| Term | Definition |
|------|------------|
| **MQTT** | Message Queuing Telemetry Transport |
| **Zigbee** | Low-power wireless mesh protocol |
| **BLE** | Bluetooth Low Energy |
| **Gateway** | Bridge between devices and cloud |
| **Shadow** | Virtual device state |
| **TTL** | Time-to-live |

## Changelog

### [2.0.0] -- 2024-12-01
- Major release with edge processing

### [1.5.0] -- 2024-06-15
- Performance improvements

### [1.0.0] -- 2024-01-01
- Initial stable release

## Contributing Guidelines

```bash
git clone https://github.com/example/skill.git
cd skill
pip install -e ".[dev]"
pytest
```

## License

MIT License -- Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

## Advanced MQTT Patterns

### QoS Strategy
| Scenario | QoS Level | Rationale |
|----------|-----------|-----------|
| Telemetry data | QoS 0 | Fire-and-forget; occasional loss acceptable |
| Device commands | QoS 1 | At-least-once delivery; idempotent handlers |
| Critical alerts | QoS 2 | Exactly-once; alarms, safety events |
| OTA notifications | QoS 1 | Must arrive, duplicates handled |

### Topic Naming Convention
```
{org}/{device_type}/{device_id}/{event_type}
  org:         tenant or namespace
  device_type: light, sensor, thermostat, camera
  device_id:   unique device identifier
  event_type:  state, command, telemetry, heartbeat, alert
```

### MQTT 5.0 Features
```yaml
mqtt5_features:
  shared_subscriptions:
    enabled: true
    group: "iot-gateway-cluster"
    description: "Load balance across gateway instances"
  message_expiry:
    telemetry: 300s
    commands: 60s
    alerts: 3600s
  topic_aliases:
    enabled: true
    max_count: 100
    description: "Reduce bandwidth for repeated topic strings"
  flow_control:
    receive_maximum: 100
    maximum_packet_size: 1048576
```

### Retained Messages Pattern
```python
# Device state retained for new subscribers
client.publish(
    topic="home/living-room/light/state",
    payload=json.dumps({"on": True, "brightness": 75}),
    qos=1,
    retain=True
)
# New subscriber immediately gets last known state
```

## Device Shadow Patterns

### Shadow Document Structure
```json
{
  "deviceId": "light-001",
  "state": {
    "reported": {"on": true, "brightness": 75, "color_temp": 4000},
    "desired": {"on": true, "brightness": 80, "color_temp": 3500}
  },
  "metadata": {
    "reported": {"timestamp": "2024-01-15T10:30:00Z"},
    "desired": {"timestamp": "2024-01-15T10:25:00Z"}
  },
  "version": 42,
  "clientToken": "token-abc-123"
}
```

### Shadow Sync Pattern
```python
class DeviceShadow:
    def __init__(self, device_id: str, broker: str):
        self.device_id = device_id
        self.shadow_topic = f"$aws/things/{device_id}/shadow"
        self.version = 0

    def update_desired(self, desired_state: dict):
        self.version += 1
        payload = {
            "state": {"desired": desired_state},
            "version": self.version
        }
        self.client.publish(
            f"{self.shadow_topic}/update",
            json.dumps(payload), qos=1
        )

    def on_shadow_update(self, message):
        payload = json.loads(message.payload)
        delta = payload["state"].get("delta", {})
        if delta:
            self.apply_delta(delta)
            self.report_state(delta)
```

## Firmware OTA Workflow

### Staged Rollout Pipeline
```
Stage 1:  Canary (5%)   -> Monitor 24h -> Error rate < 0.1%?
Stage 2:  Early (25%)   -> Monitor 24h -> Error rate < 0.1%?
Stage 3:  Half (50%)    -> Monitor 12h -> Error rate < 0.1%?
Stage 4:  Full (100%)   -> Monitor 48h -> Rollback if > 1%
```

### OTA Message Format
```json
{
  "firmware_version": "2.1.0",
  "firmware_url": "https://releases.example.com/fw/2.1.0.bin",
  "firmware_sha256": "a1b2c3d4e5f6...",
  "firmware_size_bytes": 524288,
  "target_devices": ["light-*", "sensor-*"],
  "rollback_version": "2.0.3",
  "timeout_hours": 48,
  "reboot_after_install": true
}
```

### Rollback Trigger Conditions
| Condition | Threshold | Action |
|-----------|-----------|--------|
| Install failure | > 5% of staged group | Pause rollout |
| Heartbeat loss | > 10% of staged group | Pause + alert |
| Error rate increase | > 2x baseline | Pause rollout |
| Boot loop detected | Any device | Auto-rollback |
| Sensor anomalies | > 3 sigma | Pause + investigate |

## Protocol Comparison

| Feature | MQTT | CoAP | Zigbee | Z-Wave | BLE | Matter |
|---------|------|------|--------|--------|-----|--------|
| Range | Unlimited | Unlimited | 10-100m | 30-100m | 10-50m | 10-100m |
| Power | High | Low | Very Low | Low | Very Low | Low |
| Bandwidth | High | Low | 250 Kbps | 100 Kbps | 1 Mbps | Variable |
| Topology | Star | Star | Mesh | Mesh | Star/P2P | Mesh |
| Security | TLS | DTLS | AES-128 | S2 | AES-CCM | AES-CCM |
| Max Nodes | Unlimited | Unlimited | 65,000 | 232 | 8 | 250+ |
| Use Case | Cloud | M2M | Home | Home | Wearables | Home |

### Protocol Selection Guide
```
Need cloud connectivity?    -> MQTT or CoAP
Need mesh networking?       -> Zigbee, Z-Wave, or Thread
Need ultra-low power?       -> BLE or Zigbee
Need high bandwidth?        -> MQTT over WiFi
Need Matter compatibility?  -> Matter/Thread
Need universal device?      -> MQTT + protocol translation
```

## Edge Computing Patterns

### Edge Processing Pipeline
```
Raw Sensor Data
  -> Deduplication (remove identical consecutive readings)
  -> Aggregation (1s -> 10s windows, compute avg/min/max)
  -> Filtering (remove outliers, apply Kalman filter)
  -> Event Detection (threshold crossing, pattern match)
  -> Local Action (immediate rule execution)
  -> Cloud Forwarding (summary or anomaly events only)
```

### Edge Rule Engine
```python
class EdgeRuleEngine:
    def __init__(self):
        self.rules = []
        self.event_buffer = []

    def evaluate(self, event: dict):
        self.event_buffer.append(event)
        for rule in self.rules:
            if rule.condition.match(self.event_buffer):
                result = rule.action.execute()
                if result.forward_to_cloud:
                    self.cloud_publish(result)
                return result
        return None

    def add_rule(self, trigger, condition, action, priority=0):
        self.rules.append(EdgeRule(
            trigger=trigger,
            condition=condition,
            action=action,
            priority=priority
        ))
        self.rules.sort(key=lambda r: r.priority, reverse=True)
```

## Rate Limiting & Storm Protection

### Device-Level Rate Limits
```python
rate_limits = {
    "state_updates": {"max_per_minute": 60, "burst": 10},
    "commands": {"max_per_second": 5, "burst": 3},
    "telemetry": {"max_per_second": 1, "burst": 1},
    "alerts": {"max_per_minute": 10, "burst": 5},
    "ota_checks": {"max_per_hour": 4, "burst": 1},
}
```

### Storm Detection & Mitigation
```python
class StormDetector:
    WINDOW_SECONDS = 60
    THRESHOLD_MULTIPLIER = 10

    def __init__(self):
        self.baseline = {}
        self.current_window = {}

    def is_storm(self, device_id: str, event_type: str) -> bool:
        baseline = self.baseline.get(f"{device_id}:{event_type}", 1)
        current = self.current_window.get(f"{device_id}:{event_type}", 0)
        return current > baseline * self.THRESHOLD_MULTIPLIER

    def handle_storm(self, device_id: str, event_type: str):
        logger.warning(f"Storm detected: {device_id} {event_type}")
        self.rate_limit_device(device_id, factor=0.1)
        self.alert_operations(device_id, event_type)
```

## Cloud Integration Patterns

### AWS IoT Core
```python
import boto3
iot = boto3.client('iot')

# Create thing
iot.create_thing(thingName='device-001', thingTypeName='Light')

# Create certificate
cert = iot.create_keys_and_certificate(setAsActive=True)
# Attach policy
iot.attach_policy(policyName='IoTPolicy', target=cert['certificateArn'])
# Attach thing principal
iot.attach_thing_principal(thingName='device-001', principal=cert['certificateArn'])
```

### Azure IoT Hub
```python
from azure.iot.hub import IoTHubRegistryManager
manager = IoTHubRegistryManager(conn_str)

# Send device-to-cloud message
from azure.iot.device import IoTHubDeviceClient
client = IoTHubDeviceClient.create_from_connection_string(device_conn_str)
client.send_message({"temperature": 72.5, "humidity": 45})
```

### Google Cloud IoT Core
```python
from google.cloud import iot_v1
client = iot_v1.DeviceManagerClient()
parent = f"projects/{project_id}/locations/{location}/registries/{registry_id}"

# Create device
device = iot_v1.Device(id="device-001", credentials=[iot_v1.DeviceCredential(
    public_key=iot_v1.PublicKey(key_type=iot_v1.PublicKeyType.RSA_PEM, key="...")
)])
client.create_device(parent=parent, device=device)
```

## Message Queue Patterns

### Pub/Sub Fan-Out
```
Device Event -> MQTT Broker
  |-> Gateway 1 (processing)
  |-> Gateway 2 (analytics)
  |-> Cloud Sync (storage)
  |-> Alert Engine (notifications)
```

### Request-Reply Over MQTT
```python
class MQTTRequestReply:
    def __init__(self, client, reply_timeout=5.0):
        self.client = client
        self.pending = {}
        self.reply_timeout = reply_timeout

    def request(self, device_id: str, payload: dict) -> dict:
        request_id = str(uuid.uuid4())
        topic = f"devices/{device_id}/commands/request"
        reply_topic = f"devices/{device_id}/commands/reply/{request_id}"

        future = asyncio.Future()
        self.pending[request_id] = future
        self.client.subscribe(reply_topic)
        self.client.publish(topic, json.dumps({
            "request_id": request_id,
            **payload
        }))
        return asyncio.wait_for(future, self.reply_timeout)

    def on_reply(self, message):
        data = json.loads(message.payload)
        request_id = data["request_id"]
        if request_id in self.pending:
            self.pending[request_id].set_result(data)
```

## Bulk Operations

### Device Provisioning Template
```python
provisioning_batch = [
    {"device_id": f"light-floor{i}-room{j}", "type": "light", "floor": i, "room": j}
    for i in range(1, 6) for j in range(1, 11)
]

def bulk_provision(devices: list):
    results = {"success": 0, "failed": 0, "errors": []}
    for device in devices:
        try:
            hub.register_device(**device)
            results["success"] += 1
        except Exception as e:
            results["failed"] += 1
            results["errors"].append({"device": device["device_id"], "error": str(e)})
    return results
```

### Batch State Update
```python
def batch_state_update(updates: dict):
    """Update multiple device states atomically."""
    with hub.transaction():
        for device_id, state in updates.items():
            hub.set_state(device_id, state, validate=False)
```

## Diagnostic API

### Device Health Endpoint
```json
GET /api/v1/devices/{device_id}/health

{
  "device_id": "light-001",
  "online": true,
  "uptime_seconds": 86400,
  "last_heartbeat": "2024-01-15T10:30:00Z",
  "signal_rssi_dbm": -45,
  "battery_pct": 85,
  "firmware_version": "2.1.0",
  "memory_free_bytes": 32768,
  "cpu_load_avg": 0.42,
  "error_count_24h": 0,
  "messages_sent_24h": 1440,
  "messages_received_24h": 72
}
```

### Hub Metrics Endpoint
```json
GET /api/v1/hub/metrics

{
  "devices_total": 150,
  "devices_online": 145,
  "devices_offline": 5,
  "messages_per_second": 125,
  "rules_active": 28,
  "rules_fired_24h": 342,
  "uptime_seconds": 604800,
  "memory_usage_pct": 42,
  "cpu_usage_pct": 18,
  "mqtt_connections": 150,
  "protocol_translations_per_second": 85
}
```

## Schema Evolution

### Versioning Strategy
| Version | Change Type | Action |
|---------|------------|--------|
| Minor (2.0.x) | New optional fields | Add with defaults |
| Minor (2.0.x) | Deprecated field | Mark, keep for 6 months |
| Major (3.0.0) | Removed field | Breaking change, migrate |
| Major (3.0.0) | Type change | Breaking change, migrate |

### Migration Script
```python
def migrate_device_schema(old_version: str, new_version: str):
    devices = hub.get_all_devices()
    for device in devices:
        if device.schema_version == old_version:
            migrated = apply_migration(device, old_version, new_version)
            hub.update_device(migrated)
```

## Disaster Recovery

### Backup Strategy
| Component | Frequency | Retention | Method |
|-----------|-----------|-----------|--------|
| Device registry | Real-time | 30 days | Database replication |
| Device states | Real-time | 7 days | Redis snapshot |
| Automation rules | On change | 90 days | Git version control |
| Event logs | Continuous | 30 days | Log aggregation |
| Certificates | On change | 1 year | Vault + offline backup |

### Recovery Procedures
```
Scenario: Hub failure
  1. Start backup hub instance
  2. Load device registry from database
  3. Restore device states from Redis snapshot
  4. Reconnect MQTT subscriptions
  5. Resume automation rules
  RTO: 5 minutes | RPO: 0 (real-time replication)

Scenario: Broker failure
  1. Failover to standby broker
  2. Clients auto-reconnect (keepalive timeout)
  3. Rebuild retained messages from device shadow
  RTO: 30 seconds | RPO: last publish cycle
```

## Performance Benchmarks

### Throughput Testing
```python
import time

def benchmark_mqtt_publish(client, topic, payload, iterations=10000):
    start = time.perf_counter()
    for i in range(iterations):
        client.publish(topic, payload)
    elapsed = time.perf_counter() - start
    rate = iterations / elapsed
    print(f"MQTT Publish: {rate:.0f} msg/s ({elapsed:.2f}s for {iterations} msgs)")

def benchmark_state_update(hub, device_count=1000, updates_per_device=10):
    start = time.perf_counter()
    for i in range(device_count):
        for j in range(updates_per_device):
            hub.set_state(f"device-{i}", {"value": j})
    elapsed = time.perf_counter() - start
    total_ops = device_count * updates_per_device
    rate = total_ops / elapsed
    print(f"State Updates: {rate:.0f} ops/s ({elapsed:.2f}s for {total_ops} ops)")
```

### Latency Percentiles
| Operation | p50 | p95 | p99 | p999 |
|-----------|-----|-----|-----|------|
| MQTT Publish | 0.8ms | 2.1ms | 4.5ms | 12ms |
| State Read | 0.3ms | 0.8ms | 1.5ms | 3ms |
| State Write | 0.5ms | 1.2ms | 2.8ms | 6ms |
| Rule Evaluation | 2.1ms | 8.5ms | 18ms | 35ms |
| Protocol Translation | 3.2ms | 12ms | 25ms | 50ms |

## Advanced Security Patterns

### Certificate Rotation
```python
class CertificateRotator:
    def __init__(self, ca_client, device_registry):
        self.ca = ca_client
        self.registry = device_registry
        self.rotation_window_days = 30

    def check_expiration(self):
        expiring = self.registry.get_expiring_certificates(
            within_days=self.rotation_window_days
        )
        for device in expiring:
            self.rotate_certificate(device)

    def rotate_certificate(self, device):
        new_cert = self.ca.generate_certificate(device.device_id)
        self.registry.update_certificate(device.device_id, new_cert)
        self.notify_device(device, new_cert)
```

### Network Segmentation
```
IoT VLAN Configuration:
  VLAN 10: Critical devices (locks, alarms) - strict ACLs
  VLAN 20: HVAC/Lighting - moderate ACLs
  VLAN 30: Sensors/Telemetry - broad outbound, no inbound
  VLAN 40: Cameras - isolated, NVR-only access
  VLAN 50: Guest/Temporary - internet only
```

### Intrusion Detection Rules
```yaml
ids_rules:
  - name: "Unexpected device registration"
    condition: "new_device from non_provisioned_mac"
    severity: "high"
    action: "alert + quarantine"

  - name: "Telemetry volume spike"
    condition: "messages_per_min > 10x baseline"
    severity: "medium"
    action: "rate_limit + alert"

  - name: "Firmware version rollback"
    condition: "firmware_version < previous_version"
    severity: "high"
    action: "block + alert + investigate"

  - name: "Lateral movement attempt"
    condition: "device sends to non_allowed_subnet"
    severity: "critical"
    action: "block + isolate + alert"
```

## Multi-Tenancy Patterns

### Tenant Isolation
```python
class TenantIsolation:
    def __init__(self):
        self.tenants = {}

    def register_tenant(self, tenant_id: str, config: dict):
        self.tenants[tenant_id] = {
            "mqtt_prefix": f"tenant/{tenant_id}",
            "device_limit": config.get("device_limit", 100),
            "rate_limit": config.get("rate_limit", 1000),
            "allowed_protocols": config.get("protocols", ["mqtt"]),
            "storage_quota_mb": config.get("storage", 1024),
        }

    def get_tenant_scope(self, tenant_id: str) -> dict:
        return self.tenants[tenant_id]
```

## Example: Complete Smart Home Setup

```python
from iot_integration import IoTHub, Device, Protocol, DeviceType, AutomationRule

# Initialize
hub = IoTHub(name="My Smart Home", broker="mqtt://broker.local:1883")

# Living Room
hub.register_device("lr-light-1", DeviceType.LIGHT, Protocol.ZIGBEE,
    capabilities=["dimming", "color"], room="living_room")
hub.register_device("lr-sensor-1", DeviceType.SENSOR, Protocol.ZIGBEE,
    capabilities=["temperature", "humidity", "motion"], room="living_room")
hub.register_device("lr-thermostat", DeviceType.THERMOSTAT, Protocol.MQTT,
    capabilities=["temperature", "humidity", "setpoint"], room="living_room")

# Bedroom
hub.register_device("br-light-1", DeviceType.LIGHT, Protocol.ZIGBEE,
    capabilities=["dimming", "color_temperature"], room="bedroom")
hub.register_device("br-sensor-1", DeviceType.SENSOR, Protocol.ZIGBEE,
    capabilities=["temperature", "humidity", "light"], room="bedroom")

# Entrance
hub.register_device("entrance-lock", DeviceType.LOCK, Protocol.ZIGBEE,
    capabilities=["lock", "unlock", "status"], room="entrance")
hub.register_device("entrance-camera", DeviceType.CAMERA, Protocol.MQTT,
    capabilities=["stream", "snapshot", "motion"], room="entrance")

# Automation: Morning Routine
hub.add_rule(AutomationRule(
    name="Morning Wake-Up",
    trigger={"type": "time", "cron": "0 7 * * *"},
    conditions=[{"type": "day_of_week", "days": ["mon", "tue", "wed", "thu", "fri"]}],
    actions=[
        {"type": "device_command", "device": "br-light-1", "command": "on",
         "params": {"brightness": 30, "color_temp": 2700}},
        {"type": "delay", "seconds": 300},
        {"type": "device_command", "device": "br-light-1", "command": "set",
         "params": {"brightness": 70, "color_temp": 4000}},
        {"type": "notification", "message": "Good morning! Temperature: {{lr-sensor-1.temperature}}°F"},
    ],
))

# Automation: Security
hub.add_rule(AutomationRule(
    name="Motion Alert",
    trigger={"type": "device_state", "device": "entrance-camera", "state": "motion", "value": True},
    conditions=[
        {"type": "time_range", "start": "22:00", "end": "06:00"},
        {"type": "presence", "mode": "home"},
    ],
    actions=[
        {"type": "device_command", "device": "entrance-camera", "command": "snapshot"},
        {"type": "notification", "message": "Motion detected at entrance", "priority": "high"},
        {"type": "device_command", "device": "lr-light-1", "command": "on",
         "params": {"brightness": 100}},
    ],
))

hub.start()
```

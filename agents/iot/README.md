# IoT Agent

> Comprehensive IoT platform covering device management, MQTT/CoAP protocols, edge computing, sensor data analytics, digital twins, and fleet operations.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Performance](#performance)
- [Security](#security)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [License](#license)

## Overview

The IoT Agent manages the complete lifecycle of IoT deployments — from device registration and telemetry processing through edge computing orchestration and digital twin modeling. Built for industrial IoT, smart cities, connected healthcare, and enterprise device fleets.

Whether you're deploying thousands of temperature sensors in a smart building, managing industrial controllers on a factory floor, or orchestrating edge workloads for real-time analytics, the IoT Agent provides the tools to manage your device fleet efficiently and reliably.

## Features

### Device Management
- Registration with device types (SENSOR, ACTUATOR, GATEWAY, CAMERA, etc.)
- Protocol support (MQTT, CoAP, HTTP, WebSocket, AMQP, LoRa, BLE)
- Device status tracking (ONLINE, OFFLINE, WARNING, ERROR, etc.)
- Command execution with timeout and retry
- Bulk operations across device fleets
- Automatic offline detection

### Telemetry Processing
- Real-time data ingestion
- Configurable aggregation windows (1min, 5min, 1hr, 24hr, etc.)
- Statistical measures (min, max, avg, std deviation)
- Multiple anomaly detection methods (Z-Score, IQR, Moving Average)
- Alert generation for threshold violations
- Batch ingestion support

### Edge Computing
- Edge node resource management (CPU, memory, storage)
- Workload deployment and monitoring
- Resource utilization tracking
- Support for inference, aggregation, filtering workloads
- Container orchestration
- Auto-scaling capabilities

### Digital Twins
- State synchronization with physical devices
- Simulation engine for what-if scenarios
- Predictive maintenance based on sensor data
- Failure probability estimation
- Multiple prediction confidence levels

### Fleet Operations
- Device grouping by location, type, or custom rules
- Scheduled maintenance workflows
- Impact assessment before bulk operations
- Checklist-driven maintenance
- Fleet health reporting

## Quick Start

### Installation

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Basic Usage

```python
from agents.iot.agent import IoTAgent, DeviceType, ProtocolType

agent = IoTAgent()

# Register a device
device = agent.device_manager.register_device(
    name="Temperature Sensor A1",
    device_type=DeviceType.SENSOR,
    protocol=ProtocolType.MQTT,
    location={"lat": 37.7749, "lon": -122.4194},
    tags=["building-a", "floor-1"],
)

# Ingest telemetry
agent.telemetry.ingest_reading(device.device_id, "temperature", 22.5, "C")

# Get dashboard
dashboard = agent.get_dashboard()
```

### Run the Demo

```bash
python agents/iot/agent.py
```

## Usage

### Device Management

```python
# Register device
device = agent.device_manager.register_device(
    name="Pressure Sensor B2",
    device_type=DeviceType.SENSOR,
    protocol=ProtocolType.COAP,
    location={"lat": 37.7750, "lon": -122.4195},
    tags=["building-b", "floor-2"],
    capabilities=["pressure", "temperature"],
)

# Send command
cmd = agent.device_manager.send_command(
    device.device_id,
    command_type="calibrate",
    payload={"baseline": 1013.25},
)

# Bulk operations
results = agent.device_manager.bulk_operations(
    device_ids=["DEV-001", "DEV-002", "DEV-003"],
    operation="update_config",
    params={"telemetry_interval": 30},
)

# Get fleet overview
overview = agent.device_manager.get_fleet_overview()
```

### Telemetry and Anomaly Detection

```python
# Set baseline
agent.telemetry.set_baseline(device.device_id, "temperature", mean=22.5, std_dev=2.0)

# Ingest readings
for temp in [22.0, 23.0, 22.5, 35.0]:
    agent.telemetry.ingest_reading(device.device_id, "temperature", temp, "C")

# Detect anomalies
alert = agent.telemetry.detect_anomalies(device.device_id, "temperature", 35.0)

# Aggregate
agg = agent.telemetry.aggregate_window(device.device_id, "temperature", window_minutes=60)

# Get device metrics
metrics = agent.telemetry.get_device_metrics(device.device_id, hours=24)
```

### Edge Computing

```python
# Register edge node
node = agent.edge_manager.register_node(
    name="Edge Gateway A1",
    location="Building A Server Room",
    cpu=8, memory=16384, storage=256,
)

# Deploy workload
workload = agent.edge_manager.deploy_workload(
    name="Temperature Inference",
    workload_type=EdgeWorkloadType.INFERENCE,
    target_node_ids=[node.node_id],
    cpu=2, memory=1024,
)

# Check resources
resources = agent.edge_manager.get_node_resources(node.node_id)

# Get edge overview
overview = agent.edge_manager.get_edge_overview()
```

### Digital Twins

```python
# Create twin
twin = agent.twin_manager.create_twin(device.device_id, "sensor_model")

# Sync state
agent.twin_manager.sync_state(twin.twin_id, {"temperature": 25.0, "humidity": 45.0})

# Run simulation
sim = agent.twin_manager.run_simulation(
    twin.twin_id,
    scenario={"load_increase": 50, "duration_minutes": 30},
)

# Predict maintenance
predictions = agent.twin_manager.predict_maintenance(
    twin.twin_id,
    sensor_data={"vibration": 6.5, "temperature": 75},
)
```

### Fleet Management

```python
# Create group
group = agent.fleet_manager.create_group(
    name="Building A Sensors",
    device_ids=[device.device_id],
    group_type=GroupType.LOCATION,
)

# Schedule maintenance
agent.fleet_manager.schedule_maintenance(
    group.group_id,
    maintenance_type="firmware_update",
    scheduled_date="2026-08-01",
    checklist=[
        {"item": "Backup configs", "status": "pending"},
        {"item": "Update firmware", "status": "pending"},
        {"item": "Verify operation", "status": "pending"},
    ],
)

# Get fleet overview
overview = agent.fleet_manager.get_fleet_overview()
```

## API Reference

### DeviceManager

| Method | Description |
|--------|-------------|
| `register_device(name, type, protocol, **kw)` | Register new device |
| `update_device_status(device_id, status)` | Update device status |
| `send_command(device_id, type, payload)` | Send command to device |
| `bulk_operations(ids, operation, params)` | Bulk device operations |
| `get_fleet_overview()` | Get fleet statistics |
| `get_device(device_id)` | Get device details |

### TelemetryManager

| Method | Description |
|--------|-------------|
| `ingest_reading(device_id, metric, value, unit)` | Record telemetry |
| `ingest_batch(readings)` | Batch ingest readings |
| `aggregate_window(device_id, metric, minutes)` | Aggregate over window |
| `detect_anomalies(device_id, metric, value)` | Check for anomalies |
| `set_baseline(device_id, metric, mean, std)` | Set detection baseline |
| `get_device_metrics(device_id, hours)` | Get device metrics |

### EdgeComputingManager

| Method | Description |
|--------|-------------|
| `register_node(name, location, **kw)` | Register edge node |
| `deploy_workload(name, type, nodes, **kw)` | Deploy workload |
| `get_node_resources(node_id)` | Check node resources |
| `get_edge_overview()` | Get edge statistics |
| `undeploy_workload(workload_id)` | Remove workload |
| `get_node_status(node_id)` | Get node status |

### DigitalTwinManager

| Method | Description |
|--------|-------------|
| `create_twin(device_id, model_type)` | Create digital twin |
| `sync_state(twin_id, state_data)` | Sync twin state |
| `run_simulation(twin_id, scenario, minutes)` | Run simulation |
| `predict_maintenance(twin_id, sensor_data)` | Predict failures |
| `get_twin_status(twin_id)` | Get twin status |

### FleetManager

| Method | Description |
|--------|-------------|
| `create_group(name, device_ids, **kw)` | Create fleet group |
| `schedule_maintenance(group_id, type, date, **kw)` | Schedule maintenance |
| `get_fleet_overview()` | Get fleet statistics |
| `execute_maintenance(maintenance_id)` | Execute maintenance |
| `get_maintenance_history(group_id)` | Get maintenance history |

## Examples

### Smart Building Monitoring

```python
from agents.iot.agent import IoTAgent, DeviceType, ProtocolType

agent = IoTAgent()

# Register building sensors
sensors = []
for floor in range(1, 6):
    for zone in ["north", "south", "east", "west"]:
        sensor = agent.device_manager.register_device(
            name=f"Temp Sensor Floor {floor} Zone {zone}",
            device_type=DeviceType.SENSOR,
            protocol=ProtocolType.MQTT,
            location={"floor": floor, "zone": zone},
            tags=[f"floor-{floor}", f"zone-{zone}"],
            capabilities=["temperature", "humidity"],
        )
        sensors.append(sensor)

# Set baselines
for sensor in sensors:
    agent.telemetry.set_baseline(sensor.device_id, "temperature", mean=22.0, std_dev=2.0)
    agent.telemetry.set_baseline(sensor.device_id, "humidity", mean=45.0, std_dev=5.0)

# Ingest sample readings
import random
for sensor in sensors:
    temp = random.gauss(22.0, 1.0)
    agent.telemetry.ingest_reading(sensor.device_id, "temperature", temp, "C")

# Get fleet overview
overview = agent.device_manager.get_fleet_overview()
print(f"Total sensors: {overview['total_devices']}")
```

### Industrial Predictive Maintenance

```python
# Register industrial equipment
pump = agent.device_manager.register_device(
    name="Coolant Pump A1",
    device_type=DeviceType.ACTUATOR,
    protocol=ProtocolType.MQTT,
    capabilities=["temperature", "vibration", "pressure", "rpm"],
)

# Create digital twin
twin = agent.twin_manager.create_twin(pump.device_id, "industrial_pump")

# Set baselines for all metrics
agent.telemetry.set_baseline(pump.device_id, "temperature", mean=25.0, std_dev=3.0)
agent.telemetry.set_baseline(pump.device_id, "vibration", mean=2.0, std_dev=0.5)
agent.telemetry.set_baseline(pump.device_id, "pressure", mean=45.0, std_dev=5.0)

# Monitor and predict
readings = [
    {"metric": "temperature", "value": 28.0, "unit": "C"},
    {"metric": "vibration", "value": 4.5, "unit": "mm/s"},
    {"metric": "pressure", "value": 42.0, "unit": "psi"},
]

for reading in readings:
    agent.telemetry.ingest_reading(pump.device_id, reading["metric"], reading["value"], reading["unit"])

# Sync twin and predict
agent.twin_manager.sync_state(twin.twin_id, {r["metric"]: r["value"] for r in readings})
predictions = agent.twin_manager.predict_maintenance(
    twin.twin_id,
    sensor_data={r["metric"]: r["value"] for r in readings},
)

for pred in predictions["predictions"]:
    print(f"{pred['component']}: {pred['failure_probability']:.0%} failure probability")
```

## Configuration

```python
agent = IoTAgent(config={
    "max_devices": 1000000,
    "default_protocol": "mqtt",
    "heartbeat_interval_seconds": 60,
    "offline_threshold_seconds": 180,
    "telemetry_retention_days": 90,
    "anomaly_threshold_sigma": 3.0,
    "edge_max_nodes": 10000,
    "twin_sync_interval_seconds": 30,
    "fleet_max_group_size": 10000,
})
```

### Configuration Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| max_devices | 1000000 | Maximum device fleet size |
| default_protocol | mqtt | Default communication protocol |
| heartbeat_interval_seconds | 60 | Device heartbeat frequency |
| offline_threshold_seconds | 180 | Time before marking device offline |
| telemetry_retention_days | 90 | Days to keep telemetry data |
| anomaly_threshold_sigma | 3.0 | Z-score threshold for anomalies |
| edge_max_nodes | 10000 | Maximum edge nodes |
| twin_sync_interval_seconds | 30 | Digital twin sync frequency |
| fleet_max_group_size | 10000 | Maximum devices per fleet group |

## Architecture

For detailed architecture documentation, see [ARCHITECTURE.md](./ARCHITECTURE.md).

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        IoT Agent                            │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│   Protocol  │   Device    │  Telemetry  │  Edge Computing  │
│   Abstraction│  Manager   │  & Analytics│     Manager      │
├─────────────┼─────────────┼─────────────┼──────────────────┤
│ - MQTT      │ - Register  │ - Ingest    │ - Node Registry  │
│ - CoAP      │ - Provision │ - Aggregate │ - Workload Deploy│
│ - HTTP      │ - Command   │ - Anomaly   │ - Resource Mon.  │
│ - WebSocket │ - Bulk Ops  │ - Alerts    │ - Health Check   │
├─────────────┴─────────────┴─────────────┴──────────────────┤
│                    Digital Twin Layer                        │
│  - State Model  - Simulation  - Prediction  - Sync         │
├─────────────────────────────────────────────────────────────┤
│                    Fleet Operations Layer                    │
│  - Group Manager  - Maintenance  - Health Report            │
├─────────────────────────────────────────────────────────────┤
│                    Security Layer                            │
│  - Device Auth  - Firmware Signing  - Audit Logging         │
└─────────────────────────────────────────────────────────────┘
```

## Performance

| Metric | Target |
|--------|--------|
| Telemetry ingestion latency | < 50ms device-to-store |
| Anomaly detection | < 100ms from reading to alert |
| Edge workload deployment | < 30s per node |
| Digital twin sync | < 1s end-to-end |
| OTA update (1K devices) | < 30 minutes |
| Fleet health check | < 5s for 10K devices |

## Security

- X.509 certificate-based device authentication
- TLS 1.3 for all device-cloud communication
- Firmware image signature verification
- Role-based access control for device operations
- Encrypted telemetry storage
- Secure boot chain validation on supported devices
- Audit logging for all administrative actions

## Best Practices

### Device Management
1. **Set baselines early** — anomaly detection needs historical data
2. **Use meaningful tags** — simplify fleet grouping and filtering
3. **Monitor battery levels** — prevent unexpected device failures
4. **Track firmware versions** — ensure consistency across fleet

### Telemetry
5. **Configure appropriate intervals** — balance data freshness vs bandwidth
6. **Set realistic baselines** — avoid false positives in anomaly detection
7. **Use batch ingestion** — improve throughput for high-volume devices
8. **Archive old data** — maintain storage efficiency

### Edge Computing
9. **Use edge processing** — reduce cloud bandwidth costs
10. **Monitor resource usage** — prevent node overload
11. **Deploy workloads incrementally** — limit blast radius
12. **Set up health checks** — catch workload failures early

### Digital Twins
13. **Keep twins synced** — stale twins give wrong predictions
14. **Run simulations regularly** — validate model accuracy
15. **Track prediction accuracy** — improve models over time
16. **Use appropriate models** — match model complexity to device type

### Fleet Operations
17. **Stage OTA updates** — roll out gradually to limit blast radius
18. **Group devices logically** — simplify fleet operations
19. **Create maintenance checklists** — ensure consistency
20. **Document maintenance history** — enable trend analysis

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Device won't connect | MQTT broker down, TLS cert invalid, wrong credentials | Check broker status, verify certs, confirm credentials |
| Telemetry data gaps | Low battery, weak signal, wrong interval | Check battery, verify signal, review interval settings |
| Edge workload crashing | Insufficient resources, bad image, config error | Check CPU/memory, verify image, review config |
| Digital twin drift | Network latency, sync interval too long | Check latency, decrease sync interval |
| Fleet operations failing | Device offline, permission issue, scheduling conflict | Verify connectivity, check permissions, review schedule |
| Anomaly detection too sensitive | Baseline too narrow, threshold too low | Widen baselines, increase threshold |
| OTA update failing | Insufficient storage, network timeout, checksum mismatch | Check storage, increase timeout, verify package |

## FAQ

**Q: How many devices can the IoT Agent manage?**
A: The agent is designed to handle up to 1 million devices with proper scaling. The default configuration supports 10,000 devices comfortably.

**Q: What protocols are supported?**
A: MQTT, CoAP, HTTP, WebSocket, AMQP, LoRa, Bluetooth Low Energy (BLE), and Zigbee are supported. Protocol translation happens at the gateway layer.

**Q: How does anomaly detection work?**
A: The agent uses Z-score statistical analysis by default. It compares each reading against a baseline (mean and standard deviation) and flags readings that deviate significantly (z-score > 3.0 for warning, > 5.0 for critical).

**Q: Can I use custom anomaly detection methods?**
A: Yes. The agent supports multiple detection methods (Z-Score, IQR, Moving Average, Exponential Smoothing, Isolation Forest) and allows custom methods via extension.

**Q: How do digital twins help with maintenance?**
A: Digital twins model physical devices and their behavior. By analyzing historical data and current readings, they can predict component failures before they occur, enabling preventive maintenance.

**Q: What is the recommended telemetry interval?**
A: It depends on your use case. For environmental monitoring: 5-15 minutes. For industrial equipment: 1-5 minutes. For critical systems: 10-30 seconds.

**Q: How do I handle device firmware updates?**
A: Use the OTA (Over-The-Air) update feature. Stage updates by testing on a small group first, then gradually roll out to the full fleet. The agent provides rollback capabilities if failures exceed a threshold.

## License

MIT License - see LICENSE file for details.

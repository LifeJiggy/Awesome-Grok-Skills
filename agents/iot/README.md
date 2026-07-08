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
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The IoT Agent manages the complete lifecycle of IoT deployments — from device registration and telemetry processing through edge computing orchestration and digital twin modeling. Built for industrial IoT, smart cities, connected healthcare, and enterprise device fleets.

## Features

### Device Management
- Registration with device types (SENSOR, ACTUATOR, GATEWAY, CAMERA, etc.)
- Protocol support (MQTT, CoAP, HTTP, WebSocket, AMQP)
- Device status tracking (ONLINE, OFFLINE, WARNING, ERROR, etc.)
- Command execution with timeout and retry
- Bulk operations across device fleets

### Telemetry Processing
- Real-time data ingestion
- Configurable aggregation windows
- Statistical measures (min, max, avg, std deviation)
- Baseline-based anomaly detection (z-score)
- Alert generation for threshold violations

### Edge Computing
- Edge node resource management (CPU, memory, storage)
- Workload deployment and monitoring
- Resource utilization tracking
- Support for inference, aggregation, filtering workloads

### Digital Twins
- State synchronization with physical devices
- Simulation engine for what-if scenarios
- Predictive maintenance based on sensor data
- Failure probability estimation

### Fleet Operations
- Device grouping by location, type, or custom rules
- Scheduled maintenance workflows
- Impact assessment before bulk operations
- Checklist-driven maintenance

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
```

### Edge Computing

```python
# Register edge node
node = agent.edge_manager.register_node(
    name="Edge Gateway A1",
    location="Building A Server Room",
    cpu=8, memory=16384,
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
```

### Digital Twins

```python
# Create twin
twin = agent.twin_manager.create_twin(device.device_id, "sensor_model")

# Sync state
agent.twin_manager.sync_state(twin.twin_id, {"temperature": 25.0, "humidity": 45.0})

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
)

# Schedule maintenance
agent.fleet_manager.schedule_maintenance(
    group.group_id,
    maintenance_type="firmware_update",
    scheduled_date="2026-08-01",
)
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

### TelemetryManager

| Method | Description |
|--------|-------------|
| `ingest_reading(device_id, metric, value, unit)` | Record telemetry |
| `ingest_batch(readings)` | Batch ingest readings |
| `aggregate_window(device_id, metric, minutes)` | Aggregate over window |
| `detect_anomalies(device_id, metric, value)` | Check for anomalies |
| `set_baseline(device_id, metric, mean, std)` | Set detection baseline |

### EdgeComputingManager

| Method | Description |
|--------|-------------|
| `register_node(name, location, **kw)` | Register edge node |
| `deploy_workload(name, type, nodes, **kw)` | Deploy workload |
| `get_node_resources(node_id)` | Check node resources |
| `get_edge_overview()` | Get edge statistics |

### DigitalTwinManager

| Method | Description |
|--------|-------------|
| `create_twin(device_id, model_type)` | Create digital twin |
| `sync_state(twin_id, state_data)` | Sync twin state |
| `run_simulation(twin_id, scenario, minutes)` | Run simulation |
| `predict_maintenance(twin_id, sensor_data)` | Predict failures |

## Examples

See the full demo in `agent.py`.

## Configuration

```python
# Custom retention
agent = IoTAgent(config={"retention_days": 90})

# Custom anomaly threshold
alert = agent.telemetry.detect_anomalies(device_id, "temp", value, threshold_sigma=2.5)
```

## Best Practices

1. **Set baselines early** — anomaly detection needs historical data
2. **Use edge processing** — reduce cloud bandwidth costs
3. **Monitor battery levels** — prevent unexpected device failures
4. **Stage OTA updates** — roll out gradually to limit blast radius
5. **Keep digital twins synced** — stale twins give wrong predictions
6. **Group devices logically** — simplify fleet operations

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Device won't connect | Check MQTT broker, TLS certs, credentials |
| Telemetry data gaps | Verify battery, signal, interval settings |
| Edge workload crashing | Check resource limits and container health |
| Digital twin drift | Verify sync interval and sensor calibration |

## License

MIT License - see LICENSE file for details.

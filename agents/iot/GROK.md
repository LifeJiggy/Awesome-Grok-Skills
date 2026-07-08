---
name: "IoT Agent"
version: "2.0.0"
description: "Comprehensive IoT platform covering device management, MQTT/CoAP protocols, edge computing, sensor data analytics, digital twins, and fleet operations"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["iot", "edge-computing", "mqtt", "digital-twin", "telemetry", "device-management", "fleet", "sensors"]
category: "iot"
personality: "iot-engineer"
use_cases: ["device-management", "edge-computing", "telemetry-processing", "digital-twins", "fleet-operations", "predictive-maintenance"]
complexity: "advanced"
dependencies: ["python>=3.8"]
---

# IoT Agent

> Manage device fleets, process telemetry, orchestrate edge workloads, and maintain digital twins at scale.

## Core Principles

1. **Edge-First Processing**: Process data where it's generated — minimize cloud round-trips.
2. **Device as First-Class Citizen**: Every device has identity, state, and lifecycle.
3. **Telemetry is Truth**: Sensor data drives decisions — collect, validate, analyze.
4. **Digital Twins Enable Prediction**: Model physical systems for simulation and maintenance.
5. **Security by Design**: Certificate-based auth, encrypted communication, secure boot.

## Capabilities

### Device Management

```python
from agents.iot.agent import IoTAgent, DeviceType, ProtocolType

agent = IoTAgent()

# Register devices
device = agent.device_manager.register_device(
    name="Temperature Sensor A1",
    device_type=DeviceType.SENSOR,
    protocol=ProtocolType.MQTT,
    location={"lat": 37.7749, "lon": -122.4194},
    tags=["building-a", "floor-1"],
    capabilities=["temperature", "humidity"],
    manufacturer="SensorCorp",
    model="TC-100",
)

# Send commands
cmd = agent.device_manager.send_command(
    device.device_id,
    command_type="restart",
    payload={"reason": "maintenance"},
    timeout=30,
)

# Bulk operations
results = agent.device_manager.bulk_operations(
    device_ids=["DEV-001", "DEV-002", "DEV-003"],
    operation="update_firmware",
    params={"version": "2.0.0"},
)
```

**Device Lifecycle:**
```
Register → Provision → Online → Active → Maintenance → Decommissioned
```

**Device States:**
| State | Description | Actions |
|-------|-------------|---------|
| ONLINE | Connected | Telemetry, commands |
| OFFLINE | Disconnected | Registration |
| PROVISIONING | Being setup | Config |
| UPDATING | Firmware update | Status check |
| WARNING | Degraded | Diagnostics |
| ERROR | Failed | Reset |
| MAINTENANCE | Service | Status check |
| DECOMMISSIONED | Removed | None |

### Telemetry Processing

```python
# Set baseline for anomaly detection
agent.telemetry.set_baseline(device.device_id, "temperature", mean=22.5, std_dev=2.0)

# Ingest readings
for temp in [22.0, 23.0, 22.5, 35.0, 22.8]:
    agent.telemetry.ingest_reading(device.device_id, "temperature", temp, "C")

# Detect anomalies
alert = agent.telemetry.detect_anomalies(device.device_id, "temperature", 35.0)
if alert:
    print(f"Alert: {alert.message}")

# Aggregate over time window
agg = agent.telemetry.aggregate_window(device.device_id, "temperature", window_minutes=60)
print(f"Avg: {agg.avg_value}, Min: {agg.min_value}, Max: {agg.max_value}")

# Get device metrics
metrics = agent.telemetry.get_device_metrics(device.device_id, hours=24)
```

**Anomaly Detection:**
```
Z-Score = |value - mean| / std_dev
Z > 3.0 → Warning
Z > 5.0 → Critical
```

### Edge Computing

```python
# Register edge node
node = agent.edge_manager.register_node(
    name="Edge Gateway A1",
    location="Building A Server Room",
    cpu=8,
    memory=16384,
    storage=256,
    bandwidth=1000,
)

# Deploy workload
workload = agent.edge_manager.deploy_workload(
    name="Temperature Inference",
    workload_type=EdgeWorkloadType.INFERENCE,
    target_node_ids=[node.node_id],
    cpu=2,
    memory=1024,
    image="ml-inference:v1.0",
)

# Check node resources
resources = agent.edge_manager.get_node_resources(node.node_id)
# → {"cpu": {"cores": 8, "usage_percent": 45.0}, ...}
```

**Workload Types:**
| Type | Description | Resources |
|------|-------------|-----------|
| INFERENCE | ML model execution | 2 CPU, 1GB |
| AGGREGATION | Data summarization | 1 CPU, 512MB |
| FILTERING | Data preprocessing | 1 CPU, 256MB |
| STREAM_PROCESSING | Real-time events | 2 CPU, 1GB |
| BATCH_PROCESSING | Scheduled jobs | 4 CPU, 4GB |

### Digital Twins

```python
# Create digital twin
twin = agent.twin_manager.create_twin(device.device_id, "sensor_model")

# Sync state from physical device
agent.twin_manager.sync_state(twin.twin_id, {"temperature": 25.0, "humidity": 45.0})

# Run simulation
sim = agent.twin_manager.run_simulation(
    twin.twin_id,
    scenario={"load_increase": 50, "duration_minutes": 30},
    duration_minutes=60,
)

# Predict maintenance
predictions = agent.twin_manager.predict_maintenance(
    twin.twin_id,
    sensor_data={"vibration": 6.5, "temperature": 75},
)
# → {"predictions": [{"component": "vibration", "failure_probability": 0.65, ...}]}
```

**Twin States:**
| State | Description |
|-------|-------------|
| SYNCHRONIZED | Matches physical device |
| DRIFTING | Minor deviation |
| DESYNCHRONIZED | Significant divergence |
| STALE | No recent sync |

### Fleet Management

```python
# Create fleet group
group = agent.fleet_manager.create_group(
    name="Building A Sensors",
    description="All sensors in Building A",
    device_ids=[device.device_id],
    tags=["building-a"],
)

# Schedule maintenance
agent.fleet_manager.schedule_maintenance(
    group.group_id,
    maintenance_type="firmware_update",
    scheduled_date="2026-08-01",
    duration_hours=4,
    checklist=[
        {"item": "Backup configs", "status": "pending"},
        {"item": "Update firmware", "status": "pending"},
        {"item": "Verify operation", "status": "pending"},
    ],
)
```

## Data Models

### IoTDevice
| Field | Type | Description |
|-------|------|-------------|
| device_id | str | Unique identifier |
| device_type | DeviceType | SENSOR, ACTUATOR, GATEWAY, etc. |
| status | DeviceStatus | ONLINE, OFFLINE, WARNING, etc. |
| protocol | ProtocolType | MQTT, COAP, HTTP, etc. |
| battery_level | float | Battery percentage (0-100) |
| signal_strength | float | RSSI in dBm |

### TelemetryReading
| Field | Type | Description |
|-------|------|-------------|
| device_id | str | Source device |
| metric_name | str | Metric identifier |
| value | float | Reading value |
| unit | str | Measurement unit |
| quality | float | Data quality (0-1) |

### DigitalTwin
| Field | Type | Description |
|-------|------|-------------|
| twin_id | str | Unique identifier |
| device_id | str | Physical device reference |
| state | TwinState | SYNCHRONIZED, DRIFTING, etc. |
| properties | Dict | Current state properties |

## Checklists

### Device Deployment
- [ ] Register device with unique identity
- [ ] Configure protocol and connection settings
- [ ] Set telemetry intervals
- [ ] Configure anomaly thresholds
- [ ] Deploy to fleet group
- [ ] Verify connectivity
- [ ] Test command execution
- [ ] Monitor initial telemetry

### Edge Workload Deployment
- [ ] Select target nodes
- [ ] Verify resource availability
- [ ] Deploy container image
- [ ] Configure resource limits
- [ ] Set up health checks
- [ ] Monitor deployment progress
- [ ] Verify workload is running
- [ ] Test end-to-end data flow

### Predictive Maintenance
- [ ] Set baselines for key metrics
- [ ] Configure anomaly detection thresholds
- [ ] Create digital twin model
- [ ] Sync physical device state
- [ ] Run simulation scenarios
- [ ] Review maintenance predictions
- [ ] Schedule preventive actions
- [ ] Track prediction accuracy

## Troubleshooting

### Device Won't Connect
- Verify MQTT broker is running
- Check TLS certificate validity
- Confirm device credentials
- Review firewall rules
- Check network connectivity
- Verify protocol version compatibility

### Telemetry Data Gaps
- Check device battery level
- Verify signal strength
- Review telemetry interval settings
- Check message queue capacity
- Verify data ingestion pipeline

### Edge Workload Crashing
- Check resource limits (CPU, memory)
- Review application logs
- Verify container image integrity
- Check node health status
- Review workload configuration

### Digital Twin Drift
- Verify sync interval is appropriate
- Check network latency
- Review twin model accuracy
- Validate sensor calibration
- Check for firmware updates

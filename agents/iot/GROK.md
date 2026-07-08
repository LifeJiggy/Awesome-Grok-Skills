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

The IoT Agent provides a complete Internet of Things management platform for industrial deployments, smart cities, connected healthcare, and enterprise device fleets. It handles device lifecycle management, multi-protocol communication, edge computing orchestration, telemetry analytics, digital twin modeling, and fleet-scale operations.

---

## Core Principles

1. **Edge-First Processing**: Process data where it's generated — minimize cloud round-trips.
2. **Device as First-Class Citizen**: Every device has identity, state, and lifecycle.
3. **Telemetry is Truth**: Sensor data drives decisions — collect, validate, analyze.
4. **Digital Twins Enable Prediction**: Model physical systems for simulation and maintenance.
5. **Security by Design**: Certificate-based auth, encrypted communication, secure boot.

---

## Capabilities

### 1. Device Management

Register, provision, command, and monitor devices across multiple protocols.

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
    firmware_version="1.2.0",
)
print(f"Device: {device.device_id}")
# → Device: DEV-A1B2C3D4

# Send commands
cmd = agent.device_manager.send_command(
    device.device_id,
    command_type="restart",
    payload={"reason": "maintenance"},
    timeout=30,
)
print(f"Command status: {cmd.status}")
# → Command status: success

# Bulk operations
results = agent.device_manager.bulk_operations(
    device_ids=["DEV-001", "DEV-002", "DEV-003"],
    operation="update_firmware",
    params={"version": "2.0.0"},
)
# Returns per-device success/failure status
```

**Device Lifecycle:**
```
Register → Provision → Online → Active → Maintenance → Decommissioned
```

**Device States:**

| State | Description | Actions Allowed |
|-------|-------------|-----------------|
| ONLINE | Connected and communicating | Telemetry, commands, updates |
| OFFLINE | Not connected | Registration, wake-up |
| PROVISIONING | Being configured | Config only |
| UPDATING | Firmware update in progress | Status check |
| WARNING | Degraded performance | Diagnostics, commands |
| ERROR | Failed state | Reset, debug, commands |
| MAINTENANCE | Under service | Status check |
| DECOMMISSIONED | Removed from fleet | None |

**Command Types:**

| Command | Description | Timeout | Risk |
|---------|-------------|---------|------|
| restart | Restart device | 30s | MEDIUM |
| shutdown | Power off device | 10s | HIGH |
| update_firmware | OTA firmware update | 300s | HIGH |
| update_config | Change configuration | 10s | LOW |
| calibrate | Calibrate sensors | 60s | MEDIUM |
| diagnostic | Run self-test | 30s | LOW |
| reset_factory | Factory reset | 60s | CRITICAL |

---

### 2. Telemetry Processing

Ingest, validate, aggregate, and analyze sensor data streams.

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
    # → Alert: Temperature anomaly detected on DEV-A1B2C3D4 (z-score: 6.25)

# Aggregate over time window
agg = agent.telemetry.aggregate_window(device.device_id, "temperature", window_minutes=60)
print(f"Avg: {agg.avg_value}, Min: {agg.min_value}, Max: {agg.max_value}")
# → Avg: 25.06, Min: 22.0, Max: 35.0

# Get device metrics
metrics = agent.telemetry.get_device_metrics(device.device_id, hours=24)
print(f"Total readings: {metrics['total_readings']}")
# → Total readings: 1440

# Batch ingest
readings = [
    {"device_id": "DEV-001", "metric": "humidity", "value": 45.0, "unit": "%"},
    {"device_id": "DEV-001", "metric": "pressure", "value": 1013.25, "unit": "hPa"},
    {"device_id": "DEV-002", "metric": "temperature", "value": 23.5, "unit": "C"},
]
agent.telemetry.ingest_batch(readings)
```

**Anomaly Detection:**
```
Z-Score = |value - mean| / std_dev
Z > 3.0 → Warning
Z > 5.0 → Critical
```

**Anomaly Detection Methods:**

| Method | Algorithm | Best For | False Positive Rate |
|--------|-----------|----------|---------------------|
| Z-Score | Statistical deviation | Normal distributions | Low |
| IQR | Interquartile range | Skewed distributions | Medium |
| Moving Average | Rolling window average | Trending data | Low |
| Exponential Smoothing | Weighted recent values | Seasonal patterns | Medium |
| Isolation Forest | ML-based outlier detection | Complex patterns | Very Low |

**Aggregation Window Types:**

| Window | Duration | Use Case | Data Retention |
|--------|----------|----------|----------------|
| Real-time | 1 minute | Live monitoring | 24 hours |
| Short-term | 5 minutes | Operational dashboards | 7 days |
| Hourly | 60 minutes | Trend analysis | 90 days |
| Daily | 24 hours | Reporting | 1 year |
| Weekly | 7 days | Capacity planning | 2 years |
| Monthly | 30 days | Long-term analysis | 5 years |

---

### 3. Edge Computing

Deploy and manage workloads on edge nodes close to devices.

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
print(f"Node: {node.node_id}")
# → Node: NODE-X1Y2Z3

# Deploy workload
workload = agent.edge_manager.deploy_workload(
    name="Temperature Inference",
    workload_type=EdgeWorkloadType.INFERENCE,
    target_node_ids=[node.node_id],
    cpu=2,
    memory=1024,
    image="ml-inference:v1.0",
)
print(f"Workload: {workload.workload_id}")
# → Workload: WL-A1B2C3

# Check node resources
resources = agent.edge_manager.get_node_resources(node.node_id)
print(f"CPU usage: {resources['cpu']['usage_percent']}%")
# → CPU usage: 45.0%

# Get edge overview
overview = agent.edge_manager.get_edge_overview()
print(f"Total nodes: {overview['total_nodes']}")
# → Total nodes: 25
```

**Workload Types:**

| Type | Description | Resources | Use Case |
|------|-------------|-----------|----------|
| INFERENCE | ML model execution | 2 CPU, 1GB | Anomaly detection at edge |
| AGGREGATION | Data summarization | 1 CPU, 512MB | Reduce data volume |
| FILTERING | Data preprocessing | 1 CPU, 256MB | Clean sensor data |
| STREAM_PROCESSING | Real-time events | 2 CPU, 1GB | Event-driven processing |
| BATCH_PROCESSING | Scheduled jobs | 4 CPU, 4GB | Daily reports |
| TRANSCODING | Media conversion | 2 CPU, 2GB | Video/image processing |

**Edge Node States:**

| State | Description | Actions |
|-------|-------------|---------|
| ONLINE | Connected and ready | Deploy, monitor |
| OFFLINE | Not connected | Wake, troubleshoot |
| DEPLOYING | Workload being deployed | Monitor progress |
| UPDATING | Software update in progress | Status check |
| WARNING | Resource constraints | Scale, migrate |
| ERROR | Failed state | Reset, debug |
| MAINTENANCE | Scheduled maintenance | Status check |

---

### 4. Digital Twins

Create virtual representations of physical devices for simulation and prediction.

```python
# Create digital twin
twin = agent.twin_manager.create_twin(device.device_id, "sensor_model")
print(f"Twin: {twin.twin_id}")
# → Twin: TWIN-X1Y2Z3

# Sync state from physical device
agent.twin_manager.sync_state(twin.twin_id, {"temperature": 25.0, "humidity": 45.0})

# Run simulation
sim = agent.twin_manager.run_simulation(
    twin.twin_id,
    scenario={"load_increase": 50, "duration_minutes": 30},
    duration_minutes=60,
)
print(f"Simulation: {sim.simulation_id}")
# → Simulation: SIM-A1B2C3

# Predict maintenance
predictions = agent.twin_manager.predict_maintenance(
    twin.twin_id,
    sensor_data={"vibration": 6.5, "temperature": 75},
)
print(f"Predictions: {len(predictions['predictions'])} components at risk")
# → Predictions: 2 components at risk
```

**Twin States:**

| State | Description | Drift | Action |
|-------|-------------|-------|--------|
| SYNCHRONIZED | Matches physical device | < 1s | Continue monitoring |
| DRIFTING | Minor deviation | 1-10s | Increase sync frequency |
| DESYNCHRONIZED | Significant divergence | > 10s | Investigate cause |
| STALE | No recent sync | > 5 min | Check connectivity |
| UNKNOWN | Initial state | N/A | First sync pending |

**Prediction Confidence Levels:**

| Confidence | Range | Recommended Action |
|------------|-------|--------------------|
| HIGH | > 80% | Schedule maintenance immediately |
| MEDIUM | 50-80% | Monitor closely, prepare maintenance |
| LOW | < 50% | Continue normal monitoring |

**Simulation Scenarios:**

| Scenario | Parameters | Use Case |
|----------|------------|----------|
| LOAD_INCREASE | percentage, duration | Capacity planning |
| LOAD_DECREASE | percentage, duration | Efficiency analysis |
| TEMPERATURE_CHANGE | delta, duration | Environmental impact |
| COMPONENT_FAILURE | component, probability | Reliability testing |
| POWER_OUTAGE | duration | Backup system testing |

---

### 5. Fleet Management

Group devices for bulk operations and maintenance scheduling.

```python
# Create fleet group
group = agent.fleet_manager.create_group(
    name="Building A Sensors",
    description="All sensors in Building A",
    device_ids=[device.device_id],
    tags=["building-a"],
    group_type=GroupType.LOCATION,
)
print(f"Group: {group.group_id}")
# → Group: GRP-X1Y2Z3

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

# Get fleet overview
overview = agent.fleet_manager.get_fleet_overview()
print(f"Total devices: {overview['total_devices']}")
# → Total devices: 1250
```

**Fleet Group Types:**

| Group Type | Description | Example |
|------------|-------------|---------|
| LOCATION | Devices in same physical location | "Building A Sensors" |
| FUNCTION | Devices serving same purpose | "HVAC Controllers" |
| CUSTOM | User-defined grouping | "Q1 Deployment" |
| DYNAMIC | Rule-based grouping | "Low Battery Devices" |

**Maintenance Types:**

| Type | Description | Duration | Risk |
|------|-------------|----------|------|
| firmware_update | OTA firmware update | 2-4 hours | HIGH |
| calibration | Sensor calibration | 1-2 hours | MEDIUM |
| physical_inspection | On-site inspection | 4-8 hours | LOW |
| replacement | Device replacement | 1-2 hours | MEDIUM |
| decommission | Remove from fleet | 1 hour | HIGH |

---

## Data Models

### IoTDevice

| Field | Type | Description |
|-------|------|-------------|
| device_id | str | Unique identifier (DEV-{hash}) |
| name | str | Human-readable name |
| device_type | DeviceType | SENSOR, ACTUATOR, GATEWAY, CAMERA, WEARABLE, EDGE_NODE, CONTROLLER, BEACON |
| status | DeviceStatus | ONLINE, OFFLINE, WARNING, ERROR, PROVISIONING, UPDATING, MAINTENANCE, DECOMMISSIONED |
| protocol | ProtocolType | MQTT, COAP, HTTP, WEBSOCKET, AMQP, LORA, BLUETOOTH, ZIGBEE |
| location | dict | Geographic coordinates (lat/lon) |
| tags | List[str] | Arbitrary labels for grouping |
| capabilities | List[str] | Device capabilities |
| firmware_version | str | Current firmware version |
| battery_level | float | Battery percentage (0-100) |
| signal_strength | float | RSSI in dBm |
| manufacturer | str | Device manufacturer |
| model | str | Device model |
| last_seen | datetime | Last communication timestamp |

### TelemetryReading

| Field | Type | Description |
|-------|------|-------------|
| reading_id | str | Unique identifier |
| device_id | str | Source device |
| metric_name | str | Metric identifier |
| value | float | Reading value |
| unit | str | Measurement unit |
| timestamp | datetime | Reading timestamp |
| quality | float | Data quality (0-1) |
| metadata | dict | Additional context |

### DigitalTwin

| Field | Type | Description |
|-------|------|-------------|
| twin_id | str | Unique identifier (TWIN-{hash}) |
| device_id | str | Physical device reference |
| model_type | str | Twin model type |
| state | TwinState | SYNCHRONIZED, DRIFTING, DESYNCHRONIZED, STALE, UNKNOWN |
| properties | Dict | Current state properties |
| created_at | datetime | Creation timestamp |
| last_sync | datetime | Last synchronization timestamp |
| sync_interval_seconds | int | Sync frequency |

### EdgeNode

| Field | Type | Description |
|-------|------|-------------|
| node_id | str | Unique identifier (NODE-{hash}) |
| name | str | Human-readable name |
| status | NodeStatus | ONLINE, OFFLINE, DEPLOYING, UPDATING, WARNING, ERROR, MAINTENANCE |
| location | str | Physical location description |
| cpu_cores | int | Total CPU cores |
| cpu_usage_percent | float | Current CPU usage |
| memory_total_mb | int | Total memory in MB |
| memory_usage_percent | float | Current memory usage |
| storage_total_gb | int | Total storage in GB |
| storage_usage_percent | float | Current storage usage |
| bandwidth_mbps | int | Network bandwidth |

### FleetGroup

| Field | Type | Description |
|-------|------|-------------|
| group_id | str | Unique identifier (GRP-{hash}) |
| name | str | Group name |
| description | str | Group description |
| group_type | GroupType | LOCATION, FUNCTION, CUSTOM, DYNAMIC |
| device_ids | List[str] | Devices in group |
| tags | List[str] | Group tags |
| created_at | datetime | Creation timestamp |

---

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
- [ ] Validate data quality
- [ ] Update device documentation

### Edge Workload Deployment
- [ ] Select target nodes
- [ ] Verify resource availability
- [ ] Deploy container image
- [ ] Configure resource limits
- [ ] Set up health checks
- [ ] Monitor deployment progress
- [ ] Verify workload is running
- [ ] Test end-to-end data flow
- [ ] Configure auto-scaling rules
- [ ] Set up logging and monitoring

### Predictive Maintenance
- [ ] Set baselines for key metrics
- [ ] Configure anomaly detection thresholds
- [ ] Create digital twin model
- [ ] Sync physical device state
- [ ] Run simulation scenarios
- [ ] Review maintenance predictions
- [ ] Schedule preventive actions
- [ ] Track prediction accuracy
- [ ] Update baseline thresholds
- [ ] Document maintenance history

### Fleet Operations
- [ ] Define group criteria
- [ ] Assign devices to groups
- [ ] Create maintenance checklists
- [ ] Schedule maintenance windows
- [ ] Notify affected stakeholders
- [ ] Execute maintenance
- [ ] Verify device operation
- [ ] Update maintenance records
- [ ] Generate fleet health report
- [ ] Review and optimize processes

---

## Troubleshooting

### Device Won't Connect
- Verify MQTT broker is running
- Check TLS certificate validity
- Confirm device credentials
- Review firewall rules
- Check network connectivity
- Verify protocol version compatibility
- Review device logs for errors
- Check device battery level

### Telemetry Data Gaps
- Check device battery level
- Verify signal strength
- Review telemetry interval settings
- Check message queue capacity
- Verify data ingestion pipeline
- Review network latency
- Check device health status
- Verify sensor calibration

### Edge Workload Crashing
- Check resource limits (CPU, memory)
- Review application logs
- Verify container image integrity
- Check node health status
- Review workload configuration
- Monitor resource usage trends
- Check for node firmware updates
- Review network connectivity

### Digital Twin Drift
- Verify sync interval is appropriate
- Check network latency
- Review twin model accuracy
- Validate sensor calibration
- Check for firmware updates
- Review sync error logs
- Verify device state reporting
- Update twin model parameters

### Fleet Operations Failing
- Check group device membership
- Verify device connectivity
- Review maintenance checklist
- Check operation permissions
- Review error logs
- Verify device compatibility
- Check resource availability
- Review scheduling conflicts

---

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

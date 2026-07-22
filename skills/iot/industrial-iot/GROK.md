---
name: "industrial-iot"
category: "iot"
version: "2.0.0"
tags: ["iot", "industrial", "iiot", "scada", "manufacturing"]
description: "Industrial IoT systems for manufacturing, SCADA, and process control"
---

# Industrial IoT

## Overview

The Industrial IoT module provides frameworks for connecting industrial equipment, collecting operational data, and enabling smart manufacturing. It supports OPC UA, Modbus, MQTT Sparkplug, and industrial protocols for integrating PLCs, sensors, and SCADA systems. The module enables predictive maintenance, process optimization, and real-time monitoring of industrial operations.

## Core Capabilities

- **Industrial Protocols**: OPC UA, Modbus TCP/RTU, MQTT Sparkplug, EtherNet/IP
- **PLC Integration**: Connect to programmable logic controllers
- **SCADA Integration**: Interface with supervisory control systems
- **Predictive Maintenance**: ML-based equipment failure prediction
- **Process Monitoring**: Real-time industrial process visualization
- **Historian Integration**: Connect to process historians for time-series data
- **Alarm Management**: Industrial alarm configuration and management
- **Edge Computing**: Process data at the edge for low-latency responses

## Usage Examples

### OPC UA Connection

```python
from industrial_iot import OPCUAClient, Node BrowseResult

client = OPCUAClient(
    endpoint="opc.tcp://plc-01:4840",
    security_policy="Basic256Sha256",
    certificate_path="/certs/client.pem",
)

# Connect to PLC
client.connect()

# Browse nodes
nodes = client.browse("ns=2;s=Temperature")
print(f"Found {len(nodes)} nodes")

# Read value
value = client.read_node("ns=2;s=Temperature.PV")
print(f"Temperature: {value.value} {value.unit}")
```

### Modbus Communication

```python
from industrial_iot import ModbusClient, ModbusRegister

client = ModbusClient(
    host="192.168.1.100",
    port=502,
    unit_id=1,
)

client.connect()

# Read holding registers
registers = client.read_holding_registers(address=0, count=10)
print(f"Registers: {registers}")

# Write single register
client.write_register(address=100, value=500)
```

### Predictive Maintenance

```python
from industrial_iot import PredictiveMaintenanceEngine, EquipmentData

engine = PredictiveMaintenanceEngine(model="vibration-analysis")

# Analyze equipment data
data = EquipmentData(
    equipment_id="pump-001",
    vibration_rms=2.5,
    temperature=65.0,
    pressure=120.0,
   运行_hours=5000,
)

prediction = engine.analyze(data)
print(f"Equipment: {data.equipment_id}")
print(f"Health Score: {prediction.health_score:.1%}")
print(f"Remaining Life: {prediction.remaining_life_hours:.0f} hours")
print(f"Maintenance Recommended: {prediction.maintenance_recommended}")
print(f"Failure Mode: {prediction.predicted_failure_mode}")
```

### Process Historian

```python
from industrial_iot import HistorianClient, TimeRange

historian = HistorianClient(
    server="historian.example.com",
    database="process_data",
)

# Query historical data
data = historian.query(
    tag="Temperature-Reactor-01",
    range=TimeRange(start="2024-01-15T00:00:00Z", end="2024-01-15T23:59:59Z"),
    interval="5m",
)

print(f"Retrieved {len(data)} data points")
print(f"Average: {data.average:.2f}")
print(f"Min: {data.minimum:.2f}")
print(f"Max: {data.maximum:.2f}")
```

## Best Practices

- **Network Segmentation**: Isolate OT networks from IT networks
- **Redundancy**: Implement redundant connections for critical systems
- **Cybersecurity**: Apply industrial cybersecurity standards (IEC 62443)
- **Time Synchronization**: Use NTP/PTP for accurate time-stamping
- **Data Validation**: Validate sensor data for anomalies
- **Alarm Rationalization**: Reduce alarm fatigue through proper configuration
- **Change Management**: Implement rigorous change control for industrial systems
- **Disaster Recovery**: Plan for industrial system recovery scenarios

## Related Modules

- **iot-security**: Security for industrial IoT systems
- **sensor-networks**: Multi-sensor industrial networks
- **edge-gateways**: Edge computing for industrial data

---

## Advanced Configuration

### OPC UA Configuration

```python
opcua_config = {
    "security_policy": "Basic256Sha256",
    "message_security_mode": "SignAndEncrypt",
    "certificate_validation": True,
    "session_timeout": 3600000,
    "subscription_interval": 1000,
    "max_notifications_per_publish": 1000,
}
```

### Modbus Configuration

```python
modbus_config = {
    "protocol": "tcp",
    "host": "192.168.1.100",
    "port": 502,
    "unit_id": 1,
    "timeout_seconds": 5,
    "retry_count": 3,
    "baud_rate": 9600,  # For RTU
}
```

### MQTT Sparkplug Configuration

```python
sparkplug_config = {
    "broker": "mqtt.example.com",
    "port": 1883,
    "group_id": "factory-1",
    "edge_node_id": "gateway-001",
    "device_id": "plc-001",
    "namespace": "spBv1.0",
    "birth_certificate": True,
    "death_certificate": True,
}
```

### SCADA Integration

```python
scada_config = {
    "hmi_url": "http://scada.example.com",
    "historian_server": "historian.example.com",
    "alarm_server": "alarm.example.com",
    "data_retention_days": 365,
    "real_time_refresh_ms": 1000,
}
```

### Predictive Maintenance Configuration

```python
predictive_config = {
    "model": "vibration-analysis",
    "sampling_rate_hz": 1000,
    "window_size": 1024,
    "features": ["rms", "peak", "kurtosis", "crest_factor"],
    "alert_threshold": 0.8,
    "maintenance_threshold": 0.9,
}
```

## Architecture Patterns

### Industrial IoT Architecture

```
┌─────────────────────────────────────────────────┐
│                  Cloud Layer                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐│
│  │Historian│  │Analytics│  │Predictive Maint ││
│  └────┬────┘  └────┬────┘  └───────┬─────────┘│
│       │            │               │           │
├───────┴────────────┴───────────────┴───────────┤
│                  Edge Layer                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐│
│  │Gateway  │  │Protocol │  │Local Processing ││
│  │Manager  │  │Translate│  │                 ││
│  └────┬────┘  └────┬────┘  └───────┬─────────┘│
│       │            │               │           │
├───────┴────────────┴───────────────┴───────────┤
│                  Shop Floor                     │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────────────────┐│
│  │PLC  │  │SCADA│  │Sensors│ │Actuators       ││
│  └─────┘  └─────┘  └─────┘  └─────────────────┘│
└─────────────────────────────────────────────────┘
```

### Protocol Translation Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Industrial │────▶│  Edge        │────▶│  Cloud      │
│  Protocol   │     │  Gateway     │     │  Platform   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  OPC UA │           │  MQTT     │         │  REST API │
                    └─────────┘           └───────────┘         └───────────┘
```

### Predictive Maintenance Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Sensor     │────▶│  Feature     │────▶│  ML Model   │
│  Data       │     │  Extraction  │     │  Inference  │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Health │           │  Alert    │         │  Schedule │
                    │  Score  │           │  Manager  │         │  Maint    │
                    └─────────┘           └───────────┘         └───────────┘
```

## Integration Guide

### PLC Integration

```python
def connect_to_plc(plc_config):
    if plc_config.protocol == "opcua":
        client = OPCUAClient(
            endpoint=plc_config.endpoint,
            security_policy=plc_config.security_policy,
        )
        client.connect()
        return client
    elif plc_config.protocol == "modbus":
        client = ModbusClient(
            host=plc_config.host,
            port=plc_config.port,
        )
        client.connect()
        return client
```

### Historian Integration

```python
def query_historian(tag_name, time_range):
    historian = HistorianClient(
        server=historian_config.server,
        database=historian_config.database,
    )
    data = historian.query(
        tag=tag_name,
        range=time_range,
        interval="1m",
    )
    return data
```

### SCADA Integration

```python
def integrate_with_scada(scada_config):
    hmi = HMIClient(url=scada_config.hmi_url)
    alarm = AlarmClient(server=scada_config.alarm_server)

    # Subscribe to alarms
    alarm.subscribe(callback=handle_alarm)

    # Read HMI values
    values = hmi.read_tags(["Temperature", "Pressure", "Flow"])
    return values
```

## Performance Optimization

### Data Processing Optimization

```python
processing_config = {
    "batch_size": 1000,
    "parallel_workers": 4,
    "compression": "lz4",
    "sampling_rate": 1000,
    "buffer_size": 10000,
}
```

### Network Optimization

```python
network_config = {
    "tcp_nodelay": True,
    "keep_alive": True,
    "connection_pool_size": 10,
    "timeout_seconds": 5,
    "retry_count": 3,
}
```

### Storage Optimization

```python
storage_config = {
    "data_retention_days": 365,
    "compression_enabled": True,
    "downsampling_intervals": ["1m", "5m", "1h", "1d"],
    "tiered_storage": True,
}
```

## Security Considerations

### Network Segmentation

```python
network_security = {
    "it_ot_firewall": True,
    "dmz_enabled": True,
    "vlan_isolation": True,
    "vpn_required": True,
    "access_control_lists": True,
}
```

### Protocol Security

```python
protocol_security = {
    "opcua_security": "Basic256Sha256",
    "modbus_encryption": False,  # Legacy
    "mqtt_tls": True,
    "certificate_based_auth": True,
}
```

### Device Security

```python
device_security = {
    "secure_boot": True,
    "firmware_encryption": True,
    "device_authentication": True,
    "access_logging": True,
    "physical_security": True,
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| OPC UA connection timeout | Firewall blocking | Check network rules |
| Modbus CRC error | Cable issues | Check wiring |
| Data gap | Network interruption | Check connectivity |
| Alarm flooding | Threshold misconfigured | Adjust thresholds |
| Historian query slow | Large time range | Optimize queries |

### Debug Commands

```bash
# Check PLC connection
iiot-cli connect --protocol opcua --endpoint opc.tcp://plc-01:4840

# Read PLC value
iiot-cli read --protocol modbus --address 100

# Check historian
iiot-cli historian --tag Temperature --range "1h"

# Test alarm
iiot-cli alarm --test --severity critical
```

## API Reference

### OPCUAClient

```python
class OPCUAClient:
    def __init__(self, endpoint: str, security_policy: str):
        """Initialize OPC UA client."""

    def connect(self) -> bool:
        """Connect to PLC."""

    def read_node(self, node_id: str) -> NodeValue:
        """Read node value."""

    def write_node(self, node_id: str, value: Any) -> bool:
        """Write node value."""

    def browse(self, path: str) -> List[Node]:
        """Browse nodes."""
```

### ModbusClient

```python
class ModbusClient:
    def __init__(self, host: str, port: int, unit_id: int):
        """Initialize Modbus client."""

    def read_holding_registers(self, address: int, count: int) -> List[int]:
        """Read holding registers."""

    def write_register(self, address: int, value: int) -> bool:
        """Write single register."""
```

### PredictiveMaintenanceEngine

```python
class PredictiveMaintenanceEngine:
    def __init__(self, model: str):
        """Initialize predictive maintenance engine."""

    def analyze(self, data: EquipmentData) -> MaintenancePrediction:
        """Analyze equipment data."""

    def get_health_score(self, equipment_id: str) -> float:
        """Get equipment health score."""
```

### HistorianClient

```python
class HistorianClient:
    def __init__(self, server: str, database: str):
        """Initialize historian client."""

    def query(self, tag: str, range: TimeRange, interval: str) -> TimeSeriesData:
        """Query historical data."""
```

## Data Models

### EquipmentData

```python
@dataclass
class EquipmentData:
    equipment_id: str
    vibration_rms: float
    temperature: float
    pressure: float
    operating_hours: float
    timestamp: datetime
```

### MaintenancePrediction

```python
@dataclass
class MaintenancePrediction:
    equipment_id: str
    health_score: float
    remaining_life_hours: float
    maintenance_recommended: bool
    predicted_failure_mode: str
    confidence: float
```

### TimeSeriesData

```python
@dataclass
class TimeSeriesData:
    tag: str
    timestamps: List[datetime]
    values: List[float]
    average: float
    minimum: float
    maximum: float
```

### IndustrialAlarm

```python
@dataclass
class IndustrialAlarm:
    alarm_id: str
    equipment_id: str
    severity: str
    message: str
    timestamp: datetime
    acknowledged: bool
```

## Deployment Guide

### Initial Setup

```bash
# Configure gateway
iiot-cli configure --gateway gw-001 --protocols opcua,modbus

# Connect to PLC
iiot-cli connect --endpoint opc.tcp://plc-01:4840

# Test communication
iiot-cli test --tag Temperature
```

### Production Deployment

```bash
# Deploy edge gateway
iiot-cli deploy --gateway gw-001 --config production.yaml

# Verify deployment
iiot-cli status --gateway gw-001
```

## Monitoring & Observability

### Industrial Metrics

```python
metrics_config = {
    "equipment_uptime": "gauge",
    "data_points_per_second": "counter",
    "alarm_count": "counter",
    "maintenance_predictions": "counter",
    "network_latency": "histogram",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Industrial IoT Dashboard",
    "panels": [
        "equipment_status",
        "process_variables",
        "alarms",
        "predictive_maintenance",
    ],
}
```

## Testing Strategy

### Protocol Testing

```python
def test_opcua_connection():
    client = OPCUAClient(endpoint="opc.tcp://test:4840")
    assert client.connect() == True
    value = client.read_node("ns=2;s=Test")
    assert value is not None
```

### Data Validation

```python
def test_sensor_data():
    data = EquipmentData(
        equipment_id="test",
        vibration_rms=2.5,
        temperature=65.0,
        pressure=120.0,
        operating_hours=5000,
    )
    assert 0 <= data.vibration_rms <= 100
```

## Versioning & Migration

### Protocol Versioning

```python
version_config = {
    "opcua_version": "1.04",
    "modbus_version": "1.1b3",
    "sparkplug_version": "1.0",
    "backward_compatibility": True,
}
```

## Glossary

| Term | Definition |
|------|------------|
| **OPC UA** | Open Platform Communications Unified Architecture |
| **Modbus** | Industrial communication protocol |
| **SCADA** | Supervisory Control and Data Acquisition |
| **PLC** | Programmable Logic Controller |
| **HMI** | Human-Machine Interface |
| **IIoT** | Industrial Internet of Things |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with Sparkplug support |
| 1.5.0 | 2024-11-01 | Added predictive maintenance |
| 1.4.0 | 2024-09-15 | Enhanced OPC UA support |
| 1.3.0 | 2024-07-20 | Historian integration |
| 1.2.0 | 2024-05-10 | Modbus improvements |
| 1.1.0 | 2024-03-01 | SCADA integration |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow industrial standards (IEC 62443)
2. Test on actual hardware
3. Document protocol configurations
4. Validate data accuracy
5. Test failover scenarios

## Alarm Management

### Alarm Configuration

```python
from industrial_iot import AlarmManager

alarm_mgr = AlarmManager()

# Configure alarms
alarm_mgr.configure(
    equipment_id="pump-001",
    alarms=[
        {"name": "high_temperature", "tag": "Temperature", "threshold": 85, "severity": "warning"},
        {"name": "critical_temperature", "tag": "Temperature", "threshold": 95, "severity": "critical"},
        {"name": "low_pressure", "tag": "Pressure", "threshold": 50, "severity": "warning"},
        {"name": "vibration_high", "tag": "Vibration", "threshold": 5.0, "severity": "critical"},
    ],
    deadband=2,
    delay_seconds=30,
)

print(f"Alarms configured for {alarm_mgr.alarm_count} equipment")
```

### Alarm Analytics

```python
from industrial_iot import AlarmAnalytics

analytics = AlarmAnalytics()

# Analyze alarm performance
report = analytics.analyze(
    time_range_days=30,
    equipment_ids=["pump-001", "compressor-002"],
)

print(f"Alarm Analytics:")
print(f"  Total Alarms: {report.total_alarms}")
print(f"  Critical: {report.critical_count}")
print(f"  Chattering Alarms: {report.chattering_count}")
print(f"  Stale Alarms: {report.stale_count}")
print(f"  Average Response Time: {report.avg_response_minutes:.1f} min")
```

## License

MIT License. See LICENSE file for full terms.

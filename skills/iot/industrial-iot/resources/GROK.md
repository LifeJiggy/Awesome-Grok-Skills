# Industrial IoT (IIoT)

Specialized skill for implementing industrial IoT solutions in manufacturing, process industries, and critical infrastructure. Covers OT/IT integration, PLC/SCADA systems, production line optimization, predictive maintenance, and industrial communication protocols.

## Core Capabilities

### OT/IT Integration
- PLC and SCADA system integration
- OPC UA and MQTT protocol implementation
- Data historian configuration and management
- Real-time and historical data bridging
- Industrial firewall and demilitarized zone setup

### Production Line Management
- Production line monitoring and control
- OEE (Overall Equipment Effectiveness) calculation
- Throughput optimization
- Quality control integration
- Production scheduling coordination

### Device Management
- Industrial device registration and inventory
- Firmware management for PLCs and sensors
- Device health monitoring
- Tag configuration and management
- Protocol conversion gateways

### Predictive Maintenance
- Vibration analysis integration
- Thermal monitoring and analysis
- Machine learning failure prediction
- Maintenance scheduling optimization
- Spare parts inventory management

### Industrial Communication
- OPC UA server/client implementation
- Modbus TCP/RTU protocols
- Profinet and EtherNet/IP
- MQTT-SN for sensor networks
- Time-sensitive networking (TSN)

## Usage Examples

### Industrial Device Setup
```python
from industrial_iot import (
    IndustrialIoTManager, IndustrialDevice, ProductionLine,
    DeviceType, IIOTProtocol
)

iiot = IndustrialIoTManager("factory-001")

plc = IndustrialDevice(
    device_id="plc-001",
    device_type=DeviceType.PLC,
    protocol=IIOTProtocol.OPC_UA,
    manufacturer="Siemens",
    model="S7-1500",
    location="Line-1-Control-Cabinet",
    install_date="2023-01-15",
    last_maintenance="2024-06-01",
    tags={"area": "assembly", "critical": True}
)
iiot.register_device(plc)

sensor = IndustrialDevice(
    device_id="sensor-001",
    device_type=DeviceType.SENSOR,
    protocol=IIOTProtocol.MQTT,
    manufacturer="Bosch",
    model="XDK110",
    location="Line-1-Station-5",
    install_date="2023-03-20",
    last_maintenance="2024-05-15"
)
iiot.register_device(sensor)

production_line = ProductionLine(
    line_id="line-001",
    name="Assembly Line A",
    devices=["plc-001", "sensor-001", "robot-001"],
    throughput=85.5,
    efficiency=92.0
)
iiot.create_production_line(production_line)
```

### Alert Rules Configuration
```python
iiot.add_rule("temp-warning", {
    "device_id": "sensor-001",
    "parameter": "temperature",
    "operator": ">",
    "threshold": 85.0,
    "severity": "warning",
    "message": "High temperature detected on sensor"
})

iiot.add_rule("temp-critical", {
    "device_id": "sensor-001",
    "parameter": "temperature",
    "operator": ">",
    "threshold": 95.0,
    "severity": "critical",
    "message": "Critical temperature - shutdown recommended"
})

telemetry = iiot.collect_telemetry("sensor-001", {
    "temperature": 88.5,
    "humidity": 45.0
})
```

### Production Monitoring
```python
dashboard = iiot.get_factory_dashboard()
efficiency = iiot.get_production_efficiency("line-001")
alerts = iiot.get_active_alerts()

production_data = iiot.simulate_production_data(duration=60)
```

### Predictive Maintenance
```python
from industrial_iot import PredictiveMaintenanceEngine

pm_engine = PredictiveMaintenanceEngine()
pm_engine.set_threshold("vibration", 5.0)
pm_engine.set_threshold("temperature", 90.0)

prediction = pm_engine.predict_failure("motor-001", {
    "vibration": 6.5,
    "temperature": 85.0,
    "current": 12.5
})

schedule = pm_engine.get_maintenance_schedule()
```

## Best Practices

1. **Network Segmentation**: Separate OT and IT networks with industrial firewalls
2. **Protocol Security**: Use OPC UA with certificates and encryption
3. **Data Red historian**: Implement redundant data historians for critical systems
4. **Fail-Safe Design**: Ensure fail-secure behavior for safety-critical systems
5. **Patch Management**: Test patches in staging before OT deployment
6. **Real-Time Requirements**: Maintain sub-millisecond latency for control loops
7. **Documentation**: Maintain detailed asset inventory and network diagrams
8. **Monitoring**: Implement continuous monitoring of OT network traffic

## Related Skills

- [Sensor Networks](sensor-networks): Large-scale sensor deployments
- [IoT Security](iot-security): Industrial security implementations
- [Edge Computing](edge-computing): Edge data processing
- [DevOps](devops): CI/CD for industrial systems
- [Data Science](data-science): Production data analytics

## Use Cases

- Manufacturing shop floor digitalization
- Oil and gas pipeline monitoring
- Power grid optimization
- Food and beverage quality control
- Pharmaceutical manufacturing compliance
- Automotive assembly line automation
- Warehouse and logistics optimization
- Water treatment plant control

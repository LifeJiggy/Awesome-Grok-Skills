---
name: "agricultural-iot"
category: "ag-tech"
version: "2.0.0"
tags: ["agriculture", "iot", "sensors", "mqtt", "edge-computing", "precision-agriculture", "automation"]
---

# Agricultural IoT

## Overview

End-to-end agricultural IoT platform for deploying, managing, and analyzing data from field sensor networks. This module covers sensor hardware selection (soil moisture, weather stations, flow meters, GPS trackers), MQTT/LoRaWAN connectivity, edge computing gateways, cloud data pipelines, and real-time alerting. Supports integration with John Deere Operations Center, Climate FieldView, and Ag Leader platforms for automated equipment control based on sensor data.

## Core Capabilities

- **Sensor Network Management**: Deploy and monitor soil moisture, temperature, EC, pH, weather, and flow sensors across multiple fields
- **Multi-Protocol Connectivity**: Support for MQTT, LoRaWAN, NB-IoT, Zigbee, and cellular (4G/5G) sensor communication
- **Edge Computing**: On-gateway data processing, anomaly detection, and local actuation decisions with offline resilience
- **Cloud Data Pipeline**: Ingest, store, and query time-series sensor data with configurable retention and downsampling
- **Real-Time Alerting**: Multi-channel alerts (SMS, email, webhook, push) based on configurable thresholds and anomaly detection
- **Equipment Integration**: API integration with ag equipment platforms for variable-rate control and autonomous operations
- **Power Management**: Solar, battery, and hardwired power options with low-power sleep modes for remote deployments
- **Firmware Management**: Over-the-air (OTA) firmware updates for distributed sensor nodes

## Usage

```python
from agricultural_iot import (
    SensorNetwork, SensorType, Protocol, AlertConfig, EdgeGateway
)

# Define a sensor network
network = SensorNetwork(name="North Field Network")

# Add soil moisture sensors
network.add_sensor(
    sensor_id="SM-001",
    sensor_type=SensorType.SOIL_MOISTURE,
    protocol=Protocol.LORAWAN,
    latitude=38.01,
    longitude=-98.01,
    depth_inches=12,
    reading_interval_s=300,
)
network.add_sensor(
    sensor_id="SM-002",
    sensor_type=SensorType.SOIL_MOISTURE,
    protocol=Protocol.LORAWAN,
    latitude=38.02,
    longitude=-98.02,
    depth_inches=24,
    reading_interval_s=300,
)

# Add weather station
network.add_sensor(
    sensor_id="WS-001",
    sensor_type=SensorType.WEATHER_STATION,
    protocol=Protocol.CELLULAR,
    latitude=38.015,
    longitude=-98.015,
    reading_interval_s=60,
)

# Configure alerts
alert_config = AlertConfig(
    soil_moisture_low_pct=25.0,
    soil_moisture_high_pct=85.0,
    temperature_high_f=100.0,
    temperature_low_f=32.0,
    wind_speed_high_mph=40.0,
    notification_channels=["sms", "email"],
    recipients=["farmer@example.com"],
)
network.configure_alerts(alert_config)

# Query sensor data
readings = network.get_readings(
    sensor_id="SM-001",
    start_date="2024-06-01",
    end_date="2024-06-30",
)
print(f"Average soil moisture: {readings.avg_moisture:.1f}%")
print(f"Min moisture: {readings.min_moisture:.1f}%")
print(f"Max moisture: {readings.max_moisture:.1f}%")
```

```python
# Edge gateway processing
gateway = EdgeGateway(
    gateway_id="GW-001",
    sensors=["SM-001", "SM-002", "WS-001"],
    cloud_endpoint="https://api.agriplatform.com/v1",
    local_storage_days=30,
)
gateway.start()
print(f"Gateway status: {gateway.status}")
print(f"Connected sensors: {gateway.connected_count}")
```

## Best Practices

- Use LoRaWAN for remote sensors (>1 mile from gateway) due to low power and long range
- Deploy weather stations at field edges away from buildings and trees for accurate readings
- Install soil moisture sensors at multiple depths (8", 12", 24", 36") for full root zone monitoring
- Implement edge computing for time-critical decisions (irrigation triggers, frost protection)
- Maintain at least 30 days of local storage on gateways for offline resilience
- Calibrate sensors annually against manual soil sampling and laboratory analysis
- Use solar panels with battery backup for sensors in remote locations
- Monitor sensor battery levels and signal strength as part of regular network health checks
- Implement data validation rules to filter out anomalous readings before cloud ingestion
- Document sensor placement, calibration dates, and maintenance history for each device

## Related Modules

- **precision-farming** — Use sensor data for variable-rate prescriptions
- **crop-monitoring** — Integrate sensor data with satellite/drone monitoring
- **soil-analysis** — Correlate sensor readings with laboratory soil tests
- **supply-chain** — Track equipment and produce using GPS and IoT
- **backend** → **websockets** — Real-time sensor data streaming architecture

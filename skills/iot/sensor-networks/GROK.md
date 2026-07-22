---
name: "sensor-networks"
category: "iot"
version: "2.0.0"
tags: ["iot", "sensors", "networks", "mesh", "protocols"]
description: "Sensor network management, mesh networking, and data aggregation"
---

# Sensor Networks

## Overview

The Sensor Networks module manages multi-sensor deployments, mesh networking, data aggregation, and network topology optimization. It supports various sensor types (temperature, humidity, pressure, motion, light), communication protocols (Zigbee, Z-Wave, LoRa, Thread), and network topologies (star, mesh, tree). The module enables large-scale sensor deployments with efficient data collection and processing.

## Core Capabilities

- **Multi-Sensor Management**: Configure and manage diverse sensor types
- **Mesh Networking**: Self-healing mesh network topology
- **Data Aggregation**: Efficient data collection and compression
- **Network Topology**: Optimize network layout for coverage and reliability
- **Power Management**: Network-level power optimization
- **Routing Protocols**: Configure routing for mesh and tree topologies
- **Network Health Monitoring**: Monitor connectivity and signal quality
- **Scalability**: Support for 1000+ sensor nodes

## Usage Examples

### Sensor Network Deployment

```python
from sensor_networks import SensorNetwork, SensorNode, SensorType

network = SensorNetwork(
    name="warehouse-monitoring",
    protocol="zigbee",
    topology="mesh",
    max_nodes=500,
)

# Add sensor nodes
network.add_node(SensorNode(
    node_id="temp-001",
    sensor_type=SensorType.TEMPERATURE,
    location={"x": 10, "y": 20, "z": 3},
    reporting_interval=60,
    power_mode="low_power",
))

# Deploy network
status = network.deploy()
print(f"Network Deployed:")
print(f"  Nodes: {status.active_nodes}")
print(f"  Coverage: {status.coverage_percentage:.1f}%")
print(f"  Mesh Connectivity: {status.mesh_health}")
```

### Data Aggregation

```python
from sensor_networks import DataAggregator, AggregationStrategy

aggregator = DataAggregator(
    strategy=AggregationStrategy.MOVING_AVERAGE,
    window_size=10,
    compression_enabled=True,
)

# Collect and aggregate data
aggregated = aggregator.aggregate(
    sensor_id="temp-001",
    readings=[23.5, 23.6, 23.4, 23.7, 23.5, 23.3, 23.6, 23.8, 23.4, 23.5],
)

print(f"Aggregated Data:")
print(f"  Average: {aggregated.average:.2f}°C")
print(f"  Min: {aggregated.minimum:.2f}°C")
print(f"  Max: {aggregated.maximum:.2f}°C")
print(f"  Compression Ratio: {aggregated.compression_ratio:.2f}x")
```

### Network Health Monitoring

```python
from sensor_networks import NetworkMonitor, HealthMetric

monitor = NetworkMonitor(network)

# Get health status
health = monitor.get_health()
print(f"Network Health:")
print(f"  Overall Score: {health.overall_score:.1%}")
print(f"  Active Nodes: {health.active_nodes}/{health.total_nodes}")
print(f"  Average Signal: {health.average_signal_strength:.1f} dBm")
print(f"  Packet Loss: {health.packet_loss_rate:.2f}%")

# Get node-specific metrics
node_health = monitor.get_node_health("temp-001")
print(f"\nNode temp-001:")
print(f"  Signal: {node_health.signal_strength:.1f} dBm")
print(f"  Battery: {node_health.battery_level:.1f}%")
print(f"  Last Seen: {node_health.last_seen}")
```

### Routing Optimization

```python
from sensor_networks import RoutingOptimizer, Route

optimizer = RoutingOptimizer(network)

# Optimize routing
routes = optimizer.optimize(
    algorithm="dijkstra",
    metrics=["latency", "energy", "reliability"],
)

print(f"Optimized Routes:")
for route in routes[:5]:
    print(f"  {route.source} -> {route.destination}")
    print(f"    Hops: {route.hop_count}")
    print(f"    Latency: {route.latency_ms:.1f}ms")
    print(f"    Energy Cost: {route.energy_cost:.2f}")
```

## Best Practices

- **Network Planning**: Plan network topology before deployment
- **Redundancy**: Implement redundant paths in mesh networks
- **Power Optimization**: Use sleep scheduling for battery-powered nodes
- **Data Compression**: Compress data to reduce network traffic
- **Scalability Testing**: Test network performance at scale
- **Security**: Implement network-level encryption
- **Monitoring**: Continuously monitor network health
- **Firmware Updates**: Plan for OTA updates across the network

## Related Modules

- **embedded-systems**: Node firmware development
- **iot-security**: Network security
- **edge-gateways**: Edge processing for sensor data

---

## Advanced Configuration

### Network Protocol Configuration

```python
network_config = {
    "zigbee": {
        "channel": 15,
        "pan_id": 0x1234,
        "security_enabled": True,
        "encryption_key": "0123456789abcdef",
    },
    "z_wave": {
        "region": "US",
        "frequency": "908.42 MHz",
        "security_enabled": True,
    },
    "lora": {
        "frequency": "915 MHz",
        "spreading_factor": 7,
        "bandwidth": 125000,
        "coding_rate": "4/5",
    },
    "thread": {
        "channel": 25,
        "pan_id": 0xABCD,
        "network_name": "sensor-network",
    },
}
```

### Mesh Network Configuration

```python
mesh_config = {
    "routing_protocol": "aodv",
    "max_hop_count": 10,
    "self_healing": True,
    "route_timeout_seconds": 300,
    "heart_beat_interval": 60,
    "neighbor_table_size": 50,
}
```

### Data Aggregation Configuration

```python
aggregation_config = {
    "strategies": {
        "moving_average": {"window_size": 10},
        "exponential_moving_average": {"alpha": 0.3},
        "kalman_filter": {"process_noise": 0.01, "measurement_noise": 0.1},
    },
    "compression": {
        "enabled": True,
        "algorithm": "delta_encoding",
        "threshold": 0.1,
    },
}
```

### Power Management Configuration

```python
power_config = {
    "sleep_scheduling": {
        "enabled": True,
        "duty_cycle": 0.1,
        "wake_interval_seconds": 300,
    },
    "power_modes": {
        "active": {"current_mA": 15},
        "idle": {"current_mA": 5},
        "sleep": {"current_uA": 10},
        "deep_sleep": {"current_uA": 1},
    },
}
```

### Network Topology Configuration

```python
topology_config = {
    "star": {"max_nodes": 50, "range_meters": 100},
    "mesh": {"max_nodes": 500, "max_hop_count": 10},
    "tree": {"max_nodes": 200, "max_depth": 5},
    "hybrid": {"max_nodes": 1000, "edge_nodes": 50},
}
```

## Architecture Patterns

### Sensor Network Architecture

```
┌─────────────────────────────────────────────────┐
│                  Cloud Layer                     │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐│
│  │ Data    │  │Analytics│  │ Dashboard       ││
│  │ Lake    │  │ Engine  │  │                 ││
│  └────┬────┘  └────┬────┘  └───────┬─────────┘│
│       │            │               │           │
├───────┴────────────┴───────────────┴───────────┤
│                  Gateway Layer                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐│
│  │ Edge    │  │Protocol │  │ Aggregation     ││
│  │ Gateway │  │ Bridge  │  │ Engine          ││
│  └────┬────┘  └────┬────┘  └───────┬─────────┘│
│       │            │               │           │
├───────┴────────────┴───────────────┴───────────┤
│                  Sensor Network                 │
│  ┌─────┐  ┌─────┐  ┌─────┐  ┌─────────────────┐│
│  │Node │  │Node │  │Node │  │ Mesh Router     ││
│  └─────┘  └─────┘  └─────┘  └─────────────────┘│
└─────────────────────────────────────────────────┘
```

### Mesh Network Topology

```
                    ┌─────────┐
                    │ Gateway │
                    └────┬────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
    │ Router  │     │ Router  │     │ Router  │
    └────┬────┘     └────┬────┘     └────┬────┘
         │               │               │
    ┌────┴────┐     ┌────┴────┐     ┌────┴────┐
    │ Sensor  │     │ Sensor  │     │ Sensor  │
    └─────────┘     └─────────┘     └─────────┘
```

### Data Flow Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Sensor     │────▶│  Local       │────▶│  Gateway    │
│  Reading    │     │  Aggregation │     │  Aggregation│
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Cloud  │           │  Edge     │         │  Local    │
                    │  Storage│           │  Storage  │         │  Alert    │
                    └─────────┘           └───────────┘         └───────────┘
```

## Integration Guide

### Cloud Platform Integration

```python
def integrate_with_cloud(gateway_config):
    # AWS IoT Core
    aws_client = AWSIoTClient(
        endpoint=gateway_config.aws_endpoint,
        cert_path=gateway_config.cert_path,
    )

    # Azure IoT Hub
    azure_client = AzureIoTHubClient(
        connection_string=gateway_config.connection_string,
    )

    # Google Cloud IoT
    gcp_client = GoogleCloudIoTClient(
        project_id=gateway_config.project_id,
        registry=gateway_config.registry,
    )
```

### Edge Computing Integration

```python
def process_at_edge(sensor_data, edge_config):
    # Filter noise
    filtered = apply_filter(sensor_data, edge_config.filter_config)

    # Local aggregation
    aggregated = aggregate(filtered, edge_config.agg_config)

    # Run ML inference
    if edge_config.ml_enabled:
        prediction = run_inference(aggregated, edge_config.model)
        return {"aggregated": aggregated, "prediction": prediction}

    return {"aggregated": aggregated}
```

### Data Storage Integration

```python
def store_sensor_data(data, storage_config):
    # Time-series database
    if storage_config.timeseries_enabled:
        timeseries_db.insert(
            measurement="sensor_readings",
            tags={"sensor_id": data.sensor_id},
            fields={"value": data.value},
            timestamp=data.timestamp,
        )

    # Data lake
    if storage_config.datalake_enabled:
        datalake.write(
            path=f"s3://sensor-data/{data.sensor_id}/{data.date}.parquet",
            data=data.to_dataframe(),
        )
```

## Performance Optimization

### Network Optimization

```python
network_optimization = {
    "packet_aggregation": True,
    "header_compression": True,
    "adaptive_rate_control": True,
    "channel_hopping": True,
    "collision_avoidance": True,
}
```

### Data Optimization

```python
data_optimization = {
    "compression": "delta_encoding",
    "batch_transmission": True,
    "edge_processing": True,
    "data_retention_days": 30,
    "downsampling": True,
}
```

### Power Optimization

```python
power_optimization = {
    "duty_cycle": 0.1,
    "adaptive_sampling": True,
    "power_gating": True,
    "voltage_scaling": True,
}
```

## Security Considerations

### Network Security

```python
network_security = {
    "encryption_enabled": True,
    "encryption_algorithm": "aes-128-ccm",
    "authentication_required": True,
    "key_management": "distributed",
    "replay_protection": True,
}
```

### Device Security

```python
device_security = {
    "secure_boot": True,
    "firmware_encryption": True,
    "tamper_detection": True,
    "physical_security": True,
}
```

### Data Security

```python
data_security = {
    "encryption_at_rest": True,
    "encryption_in_transit": True,
    "data_integrity": True,
    "access_control": True,
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Network partition | Node failure | Enable self-healing |
| High packet loss | Interference | Change channel |
| Battery drain fast | High duty cycle | Reduce reporting interval |
| Data gaps | Connectivity issues | Enable edge caching |
| Mesh instability | Too many hops | Optimize topology |

### Debug Commands

```bash
# Check network status
sensor-cli network --status

# View node health
sensor-cli node --health --node-id temp-001

# Test connectivity
sensor-cli ping --node-id temp-001

# Check routing
sensor-cli route --table
```

## API Reference

### SensorNetwork

```python
class SensorNetwork:
    def __init__(self, name: str, protocol: str, topology: str):
        """Initialize sensor network."""

    def add_node(self, node: SensorNode) -> None:
        """Add sensor node to network."""

    def deploy(self) -> DeploymentStatus:
        """Deploy network."""

    def get_status(self) -> NetworkStatus:
        """Get network status."""
```

### DataAggregator

```python
class DataAggregator:
    def __init__(self, strategy: AggregationStrategy, window_size: int):
        """Initialize data aggregator."""

    def aggregate(self, sensor_id: str, readings: List[float]) -> AggregatedData:
        """Aggregate sensor readings."""
```

### NetworkMonitor

```python
class NetworkMonitor:
    def __init__(self, network: SensorNetwork):
        """Initialize network monitor."""

    def get_health(self) -> NetworkHealth:
        """Get network health status."""

    def get_node_health(self, node_id: str) -> NodeHealth:
        """Get specific node health."""
```

### RoutingOptimizer

```python
class RoutingOptimizer:
    def __init__(self, network: SensorNetwork):
        """Initialize routing optimizer."""

    def optimize(self, algorithm: str, metrics: List[str]) -> List[Route]:
        """Optimize routing."""
```

## Data Models

### SensorNode

```python
@dataclass
class SensorNode:
    node_id: str
    sensor_type: SensorType
    location: Dict[str, float]
    reporting_interval: int
    power_mode: str
    status: str = None
```

### AggregatedData

```python
@dataclass
class AggregatedData:
    sensor_id: str
    average: float
    minimum: float
    maximum: float
    count: int
    compression_ratio: float
```

### NetworkHealth

```python
@dataclass
class NetworkHealth:
    overall_score: float
    active_nodes: int
    total_nodes: int
    average_signal_strength: float
    packet_loss_rate: float
```

### Route

```python
@dataclass
class Route:
    source: str
    destination: str
    hop_count: int
    latency_ms: float
    energy_cost: float
    reliability: float
```

## Deployment Guide

### Initial Setup

```bash
# Initialize network
sensor-cli init --network warehouse-monitoring

# Configure gateway
sensor-cli configure --gateway gw-001 --protocol zigbee

# Add nodes
sensor-cli add-node --type temperature --location "x:10,y:20,z:3"
```

### Production Deployment

```bash
# Deploy network
sensor-cli deploy --network warehouse-monitoring

# Verify deployment
sensor-cli verify --network warehouse-monitoring
```

## Monitoring & Observability

### Network Metrics

```python
metrics_config = {
    "packet_delivery_ratio": "gauge",
    "network_latency": "histogram",
    "battery_level": "gauge",
    "signal_strength": "gauge",
    "data_throughput": "counter",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Sensor Network Dashboard",
    "panels": [
        "network_topology",
        "node_health",
        "data_flow",
        "alerts",
    ],
}
```

## Testing Strategy

### Network Testing

```python
def test_mesh_network():
    network = SensorNetwork(name="test", protocol="zigbee", topology="mesh")
    network.add_node(SensorNode(node_id="node-1", sensor_type=SensorType.TEMPERATURE))
    status = network.deploy()
    assert status.active_nodes == 1
```

### Data Validation

```python
def test_aggregation():
    aggregator = DataAggregator(strategy=AggregationStrategy.MOVING_AVERAGE, window_size=10)
    result = aggregator.aggregate("sensor-1", [23.5, 23.6, 23.4, 23.7, 23.5])
    assert 23.0 <= result.average <= 24.0
```

## Versioning & Migration

### Protocol Versioning

```python
version_config = {
    "zigbee_version": "3.0",
    "z_wave_version": "700",
    "lora_version": "1.0.3",
    "backward_compatibility": True,
}
```

## Glossary

| Term | Definition |
|------|------------|
| **Mesh Network** | Self-healing network with multiple paths |
| **Duty Cycle** | Percentage of time device is active |
| **Packet Delivery Ratio** | Successful packet delivery percentage |
| **RSSI** | Received Signal Strength Indicator |
| **LQI** | Link Quality Indicator |
| **PAN** | Personal Area Network |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with Thread support |
| 1.5.0 | 2024-11-01 | Added LoRa support |
| 1.4.0 | 2024-09-15 | Enhanced mesh networking |
| 1.3.0 | 2024-07-20 | Power optimization |
| 1.2.0 | 2024-05-10 | Data aggregation improvements |
| 1.1.0 | 2024-03-01 | Network monitoring |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Test on real hardware
2. Validate network performance
3. Document protocol configurations
4. Test power consumption
5. Verify security features

## Network Capacity Planning

### Bandwidth Analysis

```python
from sensor_networks import BandwidthAnalyzer

analyzer = BandwidthAnalyzer()

# Analyze network bandwidth requirements
analysis = analyzer.analyze(
    network="warehouse-monitoring",
    node_count=500,
    data_rate_per_node=100,  # bytes per second
    overhead_factor=1.3,
)

print(f"Bandwidth Analysis:")
print(f"  Total Data Rate: {analysis.total_rate_kbps:.1f} kbps")
print(f"  Network Utilization: {analysis.utilization:.1%}")
print(f"  Headroom: {analysis.headroom:.1%}")
print(f"  Bottleneck: {analysis.bottleneck_node}")
```

### Node Density Optimization

```python
from sensor_networks import DensityOptimizer

optimizer = DensityOptimizer()

# Optimize node placement
optimized = optimizer.optimize(
    network="warehouse-monitoring",
    coverage_target=0.95,
    max_nodes=500,
    constraints={
        "min_distance_meters": 5,
        "gateway_range_meters": 100,
        "wall_attenuation_db": 10,
    },
)

print(f"Optimized Placement:")
print(f"  Recommended Nodes: {optimized.node_count}")
print(f"  Coverage: {optimized.coverage:.1%}")
print(f"  Mesh Connectivity: {optimized.mesh_health:.1%}")
```

## License

MIT License. See LICENSE file for full terms.

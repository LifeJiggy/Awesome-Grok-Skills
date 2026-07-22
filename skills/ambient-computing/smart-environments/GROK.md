---
name: "smart-environments"
category: "ambient-computing"
version: "2.0.0"
tags: ["smart-building", "smart-home", "energy-management", "hvac", "lighting", "security", "building-automation"]
---

# Smart Environments

## Overview

Building-level smart environment management platform for orchestrating HVAC, lighting, security, access control, fire safety, and energy management systems. This module integrates with BACnet, KNX, Zigbee, Modbus, and proprietary building management systems (BMS) to provide unified environmental control, energy optimization, occupancy-based scheduling, fault detection, and predictive maintenance. Supports commercial buildings, smart homes, healthcare facilities, and industrial campuses with emphasis on energy efficiency, occupant comfort, and regulatory compliance.

## Core Capabilities

- **HVAC Control**: Temperature setpoint management, zone control, demand response, and energy optimization algorithms
- **Intelligent Lighting**: Daylight harvesting, occupancy-based control, scene management, and circadian rhythm support
- **Access Control**: Badge readers, biometric systems, visitor management, and lockdown procedures
- **Security Integration**: CCTV analytics, intrusion detection, alarm management, and incident logging
- **Energy Management**: Real-time energy monitoring, demand forecasting, peak shaving, and renewable integration
- **Fault Detection**: Automated diagnostics for HVAC, lighting, and electrical systems with predictive maintenance alerts
- **Building Protocols**: Native support for BACnet, KNX, Modbus TCP/RTU, LonWorks, and OPC-UA
- **Compliance**: ASHRAE 90.1, Title 24, LEED, and WELL building standard compliance tracking

## Usage

```python
from smart_environments import (
    BuildingManager, Zone, HVACController, LightingController, EnergyMonitor
)

# Initialize building manager
building = BuildingManager(
    name="Headquarters",
    floors=5,
    total_area_sqft=100000,
    bms_protocol="bacnet",
)

# Configure zones
building.add_zone(Zone(
    zone_id="floor3-open",
    name="Floor 3 Open Office",
    floor=3,
    area_sqft=8000,
    occupancy_capacity=40,
    hvac_zone="AHU-3",
    lighting_zone="LZ-3-1",
    access_group="employees",
))

# HVAC control
hvac = HVACController(building)
hvac.set_setpoint("floor3-open", temperature_f=72, humidity_pct=45)
hvac.set_schedule("floor3-open", {
    "weekdays": {"start": "06:00", "end": "19:00", "occupied": True},
    "weekends": {"start": "00:00", "end": "00:00", "occupied": False},
})
hvac.enable_demand_response(max_reduction_pct=20)

# Lighting
lighting = LightingController(building)
lighting.enable_daylight_harvesting("floor3-open", target_lux=300)
lighting.set_scene("floor3-open", "focus_work", {"brightness": 80, "color_temp": "cool"})
lighting.enable_circadian("floor3-open", schedule="office")

# Energy monitoring
energy = EnergyMonitor(building)
energy.start_monitoring()
dashboard = energy.get_dashboard()
print(f"Current demand: {dashboard['demand_kw']:.1f} kW")
print(f"Today's consumption: {dashboard['today_kwh']:.1f} kWh")
print(f"Peak demand: {dashboard['peak_kw']:.1f} kW")
print(f"Energy cost: ${dashboard['cost_usd']:.2f}")
```

```python
# Building status
status = building.get_status()
print(f"\nBuilding: {status['name']}")
print(f"  Zones active: {status['active_zones']}/{status['total_zones']}")
print(f"  Occupants: {status['occupants']}")
print(f"  Comfort score: {status['comfort_score']:.1f}")
print(f"  Energy efficiency: {status['energy_score']:.1f}/100")
```

## Best Practices

- Implement demand response programs to reduce peak demand charges by 15-30%
- Use occupancy-based scheduling to reduce HVAC energy by 20-40% in unoccupied periods
- Enable daylight harvesting in perimeter zones to reduce lighting energy by 30-50%
- Monitor equipment health with vibration, temperature, and power quality sensors
- Maintain ASHRAE 62.1 ventilation standards while optimizing energy use
- Implement fire alarm integration with HVAC for smoke control and evacuation
- Use model predictive control (MPC) for HVAC optimization over traditional PID
- Track ENERGY STAR scores and target scores above 75 for certification
- Document all building automation changes for commissioning and regulatory compliance
- Test all critical systems (fire, security, emergency lighting) quarterly

## Related Modules

- **ambient-intelligence** — Occupant-facing ambient intelligence on top of building systems
- **iot-integration** — Device connectivity for sensors and actuators
- **context-aware** — Occupancy and activity context for building automation
- **proximity-sensing** — Access control and presence detection
- **ag-tech** → **agricultural-iot** — Similar IoT architecture for agricultural buildings

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

## HVAC Optimization Algorithms

### Model Predictive Control (MPC)
```python
class HVACMPC:
    def __init__(self, building_model: dict):
        self.model = building_model
        self.horizon_hours = 24
        self.time_step_minutes = 15
        self.prediction_steps = self.horizon_hours * 60 // self.time_step_minutes

    def optimize(self, current_state: dict, weather_forecast: list, schedule: list) -> dict:
        """Find optimal setpoint trajectory."""
        best_trajectory = None
        best_cost = float('inf')

        for candidate in self._generate_candidates():
            cost = self._evaluate_trajectory(candidate, current_state, weather_forecast, schedule)
            if cost < best_cost:
                best_cost = cost
                best_trajectory = candidate

        return {"trajectory": best_trajectory, "cost": best_cost}

    def _evaluate_trajectory(self, trajectory, state, weather, schedule):
        total_cost = 0
        for i, setpoint in enumerate(trajectory):
            weather_at_t = weather[i] if i < len(weather) else weather[-1]
            schedule_at_t = schedule[i] if i < len(schedule) else schedule[-1]
            energy_cost = self._energy_for_setpoint(setpoint, state, weather_at_t)
            comfort_penalty = self._comfort_penalty(setpoint, schedule_at_t)
            total_cost += energy_cost + comfort_penalty
        return total_cost

    def _comfort_penalty(self, setpoint, schedule):
        ideal = schedule.get("ideal_temp", 72)
        return abs(setpoint - ideal) ** 2 * 0.1
```

### PID Controller with Anti-Windup
```python
class HVACPID:
    def __init__(self, kp: float = 2.0, ki: float = 0.5, kd: float = 1.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.prev_error = 0
        self.output_min = 0
        self.output_max = 100

    def compute(self, setpoint: float, measurement: float, dt: float) -> float:
        error = setpoint - measurement
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.prev_error = error
        # Anti-windup
        self.integral = np.clip(self.integral, -100, 100)
        return np.clip(output, self.output_min, self.output_max)
```

### Demand Response Control
```python
class DemandResponseController:
    def __init__(self, max_reduction_pct: float = 20):
        self.max_reduction = max_reduction_pct
        self.participation = False
        self.event_active = False

    def start_event(self, signal: dict):
        """Utility demand response event."""
        self.event_active = True
        reduction_target = min(signal.get("reduction_pct", 10), self.max_reduction)
        return {
            "action": "reduce_load",
            "target_reduction_pct": reduction_target,
            "duration_minutes": signal.get("duration", 60),
            "strategy": self._select_strategy(reduction_target),
        }

    def _select_strategy(self, target_pct: float) -> dict:
        if target_pct <= 10:
            return {"setpoint_offset_f": 2, "lighting_reduction_pct": 15}
        elif target_pct <= 20:
            return {"setpoint_offset_f": 4, "lighting_reduction_pct": 30, "precool": True}
        return {"setpoint_offset_f": 6, "lighting_reduction_pct": 50, "precool": True, "shed_non_critical": True}
```

## Energy Management Deep Dive

### Real-Time Energy Monitoring
```python
class EnergyMonitor:
    def __init__(self, building):
        self.building = building
        self.meters = {}
        self.readings = []

    def add_meter(self, meter_id: str, circuit: str, max_kw: float):
        self.meters[meter_id] = {"circuit": circuit, "max_kw": max_kw}

    def read_meter(self, meter_id: str) -> dict:
        reading = self._read_power(meter_id)
        self.readings.append({"meter": meter_id, "kw": reading, "timestamp": datetime.now()})
        return {"meter_id": meter_id, "kw": reading, "kwh_today": self._daily_total(meter_id)}

    def get_building_summary(self) -> dict:
        total_kw = sum(self._read_power(m) for m in self.meters)
        return {
            "total_demand_kw": total_kw,
            "peak_today_kw": max((r["kw"] for r in self.readings), default=0),
            "cost_today_usd": self._calculate_cost(total_kw),
            "carbon_kg": self._calculate_carbon(total_kw),
            "efficiency_score": self._compute_efficiency(),
        }
```

### Peak Shaving Strategy
```python
class PeakShaving:
    def __init__(self, threshold_kw: float, battery_capacity_kwh: float):
        self.threshold = threshold_kw
        self.battery_capacity = battery_capacity_kwh
        self.battery_soc = battery_capacity_kwh * 0.5

    def should_discharge(self, current_demand_kw: float) -> bool:
        return current_demand_kw > self.threshold and self.battery_soc > 0

    def discharge(self, current_demand_kw: float) -> dict:
        excess = current_demand_kw - self.threshold
        max_discharge = min(excess, self.battery_capacity * 0.2)  # 20% per hour max
        self.battery_soc -= max_discharge
        return {"discharge_kw": max_discharge, "soc_pct": (self.battery_soc / self.battery_capacity) * 100}

    def should_charge(self, current_demand_kw: float, solar_kw: float = 0) -> bool:
        return solar_kw > current_demand_kw and self.battery_soc < self.battery_capacity
```

### Energy Cost Optimization
```python
class EnergyCostOptimizer:
    def __init__(self, rate_schedule: dict):
        self.rates = rate_schedule  # {hour: rate_per_kwh}

    def optimize_schedule(self, loads: list, available_hours: int = 24) -> list:
        scheduled = []
        for load in loads:
            cheapest_hours = sorted(self.rates.keys(), key=lambda h: self.rates[h])
            for hour in cheapest_hours:
                if hour < available_hours:
                    scheduled.append({"load": load["name"], "hour": hour, "rate": self.rates[hour]})
                    break
        return scheduled

    def get_rate(self, hour: int) -> float:
        return self.rates.get(hour, self.rates.get("default", 0.12))
```

## Fault Detection & Diagnostics

### HVAC Fault Detection
```python
class HVACFaultDetector:
    FAULT_SIGNATURES = {
        "stuck_valve": {"pattern": "output > 80% for > 2h with temp near setpoint", "severity": "medium"},
        "sensor_drift": {"pattern": "sensor reading diverges > 3F from neighbors", "severity": "high"},
        "refrigerant_leak": {"pattern": "cooling capacity drops > 20% over 48h", "severity": "critical"},
        "filter_clog": {"pattern": "airflow drops > 15% with constant fan speed", "severity": "medium"},
        " economizer_fault": {"pattern": "outdoor air damper stuck at fixed position", "severity": "medium"},
    }

    def analyze(self, equipment_id: str, telemetry: dict) -> list:
        faults = []
        for fault_name, signature in self.FAULT_SIGNATURES.items():
            if self._matches_signature(telemetry, signature["pattern"]):
                faults.append({
                    "equipment": equipment_id,
                    "fault": fault_name,
                    "severity": signature["severity"],
                    "detected_at": datetime.now(),
                    "confidence": self._compute_confidence(telemetry, fault_name),
                })
        return faults
```

### Predictive Maintenance
```python
class PredictiveMaintenance:
    def __init__(self):
        self.equipment_models = {}
        self.maintenance_history = []

    def train_model(self, equipment_id: str, historical_data: list):
        features = self._extract_features(historical_data)
        labels = [d["failure_within_30d"] for d in historical_data]
        from sklearn.ensemble import RandomForestClassifier
        model = RandomForestClassifier(n_estimators=100)
        model.fit(features, labels)
        self.equipment_models[equipment_id] = model

    def predict_failure(self, equipment_id: str, current_telemetry: dict) -> dict:
        model = self.equipment_models.get(equipment_id)
        if model is None:
            return {"risk": "unknown", "confidence": 0}
        features = self._extract_features([current_telemetry])
        risk = model.predict_proba(features)[0][1]
        return {
            "failure_probability_30d": risk,
            "risk_level": "high" if risk > 0.7 else "medium" if risk > 0.3 else "low",
            "recommended_action": self._get_recommendation(risk, equipment_id),
        }
```

## Compliance Checklists

### ASHRAE 90.1 Compliance
| Requirement | Description | Status |
|-------------|-------------|--------|
| Envelope | Wall R-13, Roof R-30, Window U-0.4 | |
| Lighting | LPD < 0.82 W/sqft for office | |
| HVAC Efficiency | COP > 3.0 for cooling | |
| Controls | Occupancy sensors in all spaces | |
| Economizer | Required when outdoor air > 70F capable | |
| VFD | Required on fans > 5 HP | |
| DDC | Required for zones > 5000 sqft | |

### LEED Compliance Scorecard
| Category | Points | Available | Notes |
|----------|--------|-----------|-------|
| Energy & Atmosphere | 26 | 33 | Commissioning, monitoring |
| Indoor Environmental Quality | 13 | 15 | Air quality, lighting, thermal |
| Water Efficiency | 6 | 10 | Fixtures, irrigation |
| Materials & Resources | 6 | 13 | Sustainable materials |
| Innovation | 4 | 6 | Exemplary performance |
| Regional Priority | 3 | 4 | Location-specific |

### WELL Building Standard
| Feature | Requirement | Testing Frequency |
|---------|-------------|-------------------|
| Air (A01) | PM2.5 < 15 ug/m3 | Continuous |
| Air (A05) | CO2 < 800 ppm | Continuous |
| Water (W01) | Lead < 5 ppb | Annual |
| Light (L01) | EML targets by space | Commissioning |
| Light (L06) | Circadian lighting design | Commissioning |
| Thermal (T01) | Predicted Mean Vote -0.5 to 0.5 | Continuous |
| Sound (S01) | Background noise < 35 dBA | Annual |
| Mind (M05) | Biophilic design elements | Commissioning |

## Building Protocol Details

### BACnet Integration
```python
class BACnetController:
    def __init__(self, ip: str, port: int = 47808):
        self.ip = ip
        self.port = port

    def read_property(self, device_id: str, object_type: str, object_id: int, property: str):
        """Read a BACnet property value."""
        return self._send_request({
            "service": "readProperty",
            "device_id": device_id,
            "object_type": object_type,
            "object_id": object_id,
            "property_id": property,
        })

    def write_property(self, device_id: str, object_type: str, object_id: int, property: str, value):
        """Write a BACnet property value."""
        return self._send_request({
            "service": "writeProperty",
            "device_id": device_id,
            "object_type": object_type,
            "object_id": object_id,
            "property_id": property,
            "value": value,
        })

    def subscribe_cov(self, device_id: str, object_type: str, object_id: int):
        """Subscribe to Change of Value notifications."""
        return self._send_request({
            "service": "subscribeCOV",
            "device_id": device_id,
            "object_type": object_type,
            "object_id": object_id,
        })
```

### KNX Integration
```python
class KNXController:
    def __init__(self, host: str, port: int = 3671):
        self.host = host
        self.port = port

    def send_group_write(self, group_address: str, value):
        """Write to KNX group address."""
        return self._knx_send({
            "type": "group_write",
            "destination": group_address,
            "value": value,
        })

    def send_group_read(self, group_address: str):
        """Read from KNX group address."""
        return self._knx_send({
            "type": "group_read",
            "destination": group_address,
        })

    def listen(self, group_addresses: list):
        """Subscribe to group address updates."""
        return self._knx_listen(group_addresses)
```

## Fire Safety Integration

### Fire Alarm Integration
```python
class FireSafetyIntegration:
    def __init__(self, building: BuildingManager):
        self.building = building

    def on_fire_alarm(self, zone: str, alarm_type: str):
        actions = {
            "unlock_all_doors": True,
            "activate_emergency_lighting": True,
            "hvac_shutdown": True,
            "smoke_control": {"fan_override": "exhaust", "dampers": "open"},
            "elevator_recall": "ground_floor",
            "notification": {"type": "fire_alarm", "zone": zone, "priority": "critical"},
        }
        self._execute_emergency_actions(actions)

    def smoke_control(self, zone: str):
        """ASHRAE 171 smoke control."""
        self.building.hvac.set_mode("smoke_exhaust")
        self.building.hvac.set_fan_speed(zone, 100)
        self.building.open_dampers(zone)
        self.building.close_dampers(self._adjacent_zones(zone))
```

## Emergency Procedures

### Emergency Response Matrix
| Event | Detection | Response | Recovery |
|-------|-----------|----------|----------|
| Fire | Smoke detector | Evacuate, HVAC shutdown | Inspect, reset |
| Power failure | UPS trigger | Generator start, load shed | Grid restore, rebalance |
| HVAC failure | Temperature sensor | Alert, manual override | Repair, commission |
| Security breach | Door sensor/camera | Lockdown, alert security | Investigate, reset |
| Water leak | Moisture sensor | Close valve, alert | Repair, dry out |
| Flood | Water level sensor | Elevate critical equipment | Pump out, restore |

## Commissioning Workflows

### Functional Performance Testing
```python
class CommissioningTest:
    def __init__(self, system: str):
        self.system = system
        self.test_results = []

    def test_hvac_sequence(self, zone: str):
        tests = [
            ("Cooling start", lambda: self._test_setpoint_response(zone, "cooling", 72, 68)),
            ("Heating start", lambda: self._test_setpoint_response(zone, "heating", 72, 76)),
            ("Fan speed auto", lambda: self._test_fan_speed(zone, "auto")),
            ("Economizer", lambda: self._test_economizer(zone)),
            ("Night setback", lambda: self._test_night_mode(zone)),
        ]
        for name, test_fn in tests:
            result = test_fn()
            self.test_results.append({"test": name, "passed": result["passed"], "details": result})

    def generate_report(self) -> dict:
        total = len(self.test_results)
        passed = sum(1 for t in self.test_results if t["passed"])
        return {
            "system": self.system,
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "pass_rate": (passed / total * 100) if total > 0 else 0,
            "details": self.test_results,
        }
```

## Demand Response Programs

### Program Comparison
| Program | Signal Type | Duration | Payment | Commitment |
|---------|-------------|----------|---------|------------|
| Emergency DR | Critical peak | 1-4 hours | Premium | Must respond |
| Capacity | Day-ahead | 2-4 hours | Fixed/monthly | Opt-in |
| ancillary | Real-time | 15 min-4 hours | Per-event | Must respond |
| Frequency regulation | Real-time | Continuous | Per-kWh | Flexible |

## Renewable Integration

### Solar + Storage Optimization
```python
class RenewableOptimizer:
    def __init__(self, solar_capacity_kw: float, battery_kwh: float):
        self.solar = solar_capacity_kw
        self.battery = battery_kwh
        self.soc = battery_kwh * 0.5

    def optimize(self, solar_forecast: list, load_forecast: list, grid_rate: float) -> list:
        schedule = []
        for hour in range(24):
            solar = solar_forecast[hour]
            load = load_forecast[hour]
            net = solar - load
            if net > 0 and self.soc < self.battery:
                # Excess solar -> charge battery
                charge = min(net, self.battery - self.soc)
                self.soc += charge
                schedule.append({"hour": hour, "action": "charge", "kw": charge})
            elif net < 0 and self.soc > 0:
                # Deficit -> discharge battery
                discharge = min(-net, self.soc)
                self.soc -= discharge
                schedule.append({"hour": hour, "action": "discharge", "kw": discharge})
            else:
                schedule.append({"hour": hour, "action": "grid", "kw": abs(net)})
        return schedule
```

## Occupancy Forecasting

### Time-Series Prediction
```python
class OccupancyForecaster:
    def __init__(self, historical_data: list):
        self.model = self._train_model(historical_data)

    def forecast(self, date: datetime, hours_ahead: int = 24) -> list:
        predictions = []
        for h in range(hours_ahead):
            forecast_time = date + timedelta(hours=h)
            features = self._extract_features(forecast_time)
            prediction = self.model.predict([features])[0]
            predictions.append({
                "time": forecast_time.isoformat(),
                "predicted_occupancy": max(0, int(prediction)),
                "confidence": self._get_confidence(features),
            })
        return predictions

    def _extract_features(self, dt: datetime) -> list:
        return [
            dt.hour,
            dt.weekday(),
            dt.month,
            1 if dt.weekday() < 5 else 0,  # is_weekday
            1 if 9 <= dt.hour <= 17 else 0,  # is_business_hours
        ]
```

## Example: Complete Building Management

```python
from smart_environments import BuildingManager, Zone, HVACController, LightingController, EnergyMonitor

# Initialize
building = BuildingManager(name="HQ Building", floors=5, total_area_sqft=100000, bms_protocol="bacnet")

# Configure zones
for floor in range(1, 6):
    building.add_zone(Zone(
        zone_id=f"floor{floor}-open",
        name=f"Floor {floor} Open Office",
        floor=floor,
        area_sqft=15000,
        occupancy_capacity=60,
        hvac_zone=f"AHU-{floor}",
        lighting_zone=f"LZ-{floor}",
        access_group="employees",
    ))

# HVAC with MPC
hvac = HVACController(building)
hvac.set_controller("mpc", {"horizon_hours": 24, "reoptimize_interval_min": 15})
hvac.set_setpoint("floor1-open", temperature_f=72, humidity_pct=45)
hvac.enable_demand_response(max_reduction_pct=25)

# Lighting
lighting = LightingController(building)
for floor in range(1, 6):
    lighting.enable_daylight_harvesting(f"floor{floor}-open", target_lux=300)
    lighting.set_scene(f"floor{floor}-open", "work", {"brightness": 80, "color_temp": "cool"})
    lighting.enable_circadian(f"floor{floor}-open", schedule="office")

# Energy
energy = EnergyMonitor(building)
energy.start_monitoring()
dashboard = energy.get_dashboard()

# Fault detection
from smart_environments import FaultDetector
fault_detector = FaultDetector(building)
faults = fault_detector.scan_all()
if faults:
    for fault in faults:
        print(f"FAULT: {fault['equipment']} - {fault['description']} ({fault['severity']})")

# Building status
status = building.get_status()
print(f"\n{status['name']}: {status['active_zones']}/{status['total_zones']} zones active")
print(f"Occupants: {status['occupants']}, Comfort: {status['comfort_score']:.1f}/100")
print(f"Energy: {dashboard['today_kwh']:.0f} kWh, Cost: ${dashboard['cost_usd']:.2f}")
```

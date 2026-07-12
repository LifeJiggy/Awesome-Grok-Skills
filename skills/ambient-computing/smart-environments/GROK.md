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

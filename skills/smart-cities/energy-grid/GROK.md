---
name: "energy-grid"
category: "smart-cities"
version: "1.0.0"
tags: ["smart-cities", "energy-grid", "smart-grid", "renewables", "demand-response"]
---

# Energy Grid — Smart City Power Management Platform

## Overview

The Energy Grid module provides comprehensive smart grid management capabilities for urban power distribution, renewable energy integration, demand-side management, and grid resilience optimization. It monitors and controls the electrical distribution network from the substation level down to individual smart meters, enabling real-time visibility into power quality, load distribution, outage detection, and energy consumption patterns.

This module operates at the intersection of utility operations and city services — coordinating distributed energy resources (DERs) including rooftop solar, battery storage, EV chargers, and microgrids with the bulk power system. It supports utility-side operations (fault location, isolation, service restoration — FLISR), customer-side programs (demand response, time-of-use pricing, energy efficiency), and city-side coordination (streetlight management, building energy benchmarking, EV infrastructure planning).

The energy grid platform integrates with utility SCADA/ADMS systems, ISO/RTO wholesale markets, building management systems (BMS), electric vehicle supply equipment (EVSE), and weather forecasting services to optimize grid operations across multiple time horizons — from real-second frequency regulation to seasonal capacity planning.

## Core Capabilities

### 1. Smart Meter Data Management
Ingestion, validation, and aggregation of AMI (Advanced Metering Infrastructure) data from millions of smart meters. Supports 15-minute interval data, net metering for distributed solar, demand charge calculation, and time-of-use rate plan management. Handles meter-to-cash workflows including billing determinants and revenue protection analytics.

### 2. Distribution Grid Monitoring
Real-time state estimation across the medium-voltage and low-voltage distribution network using SCADA telemetry, AMI data, and distribution system state estimation (DSSE). Provides voltage profile monitoring, load flow analysis, transformer loading assessment, and phase balancing recommendations.

### 3. Outage Management and FLISR
Automated Fault Location, Isolation, and Service Restoration (FLISR) that detects faults, locates them using smart meter events and line sensor data, isolates faulted sections, and restores service to healthy sections within seconds. Integrates with OMS (Outage Management System) for crew dispatch and customer notification.

### 4. Demand Response Orchestration
Coordination of demand response events across residential, commercial, and industrial customers. Supports capacity-based and energy-based DR programs, automated load shed/load recovery via smart thermostats, EV chargers, and industrial process control, with verification of demand reduction through baseline estimation.

### 5. Distributed Energy Resource Management
Aggregation and dispatch of rooftop solar, behind-the-meter batteries, EV chargers, and controllable loads as virtual power plants (VPP). Supports transactive energy markets, peer-to-peer energy trading, and grid services procurement from distributed resources.

### 6. Power Quality Monitoring
Detection and analysis of power quality events — voltage sags/swells, harmonics, flicker, transient overvoltages, and frequency deviations. Correlates PQ events with equipment damage, customer complaints, and grid conditions for root cause analysis and mitigation planning.

### 7. Streetlight and Public Lighting Management
Centralized management of networked smart streetlights with adaptive dimming, energy monitoring, fault detection, and integration with traffic sensors, public safety cameras, and environmental sensors mounted on light poles.

### 8. Grid Resilience and Microgrid Control
Islanding detection, microgrid formation, and black start coordination for critical facilities. Supports resilience planning for extreme weather events with pre-positioned restoration sequences and mutual aid coordination.

## Usage Examples

### Energy Grid Engine Setup

```python
from energy_grid import EnergyGridEngine, GridConfig, AMIConfig

engine = EnergyGridEngine(
    utility_id="utility-metro-001",
    grid_config=GridConfig(
        voltage_levels_kv=[13.8, 34.5, 69, 138],
        substations=45,
        feeders=320,
        smart_meters=1_200_000,
        distributed_solar_mw=180,
        battery_storage_mw=45,
        ev_chargers=8_500
    ),
    ami_config=AMIConfig(
        read_interval_minutes=15,
        data_retention_years=3,
        net_metering_enabled=True,
        demand_charge_tiers=4
    )
)

engine.configure()
status = engine.get_status()
print(f"Smart meters online: {status['meters_online']:,}/{status['meters_total']:,}")
print(f"Distributed solar output: {status['solar_output_mw']:.1f} MW")
```

### Distribution Grid State Monitoring

```python
from energy_grid import GridStateMonitor, VoltageLevel

monitor = GridStateMonitor(engine)

# Get feeder status
feeder_status = monitor.get_feeder_status(
    feeder_id="feeder-north-12",
    include_transformer_loading=True,
    include_voltage_profile=True
)

print(f"Feeder: {feeder_status.name}")
print(f"Total load: {feeder_status.total_load_mw:.2f} MW")
print(f"Peak demand (24h): {feeder_status.peak_demand_mw:.2f} MW")
print(f"DER penetration: {feeder_status.der_penetration_pct:.1f}%")

for transformer in feeder_status.transformers:
    loading = transformer.loading_pct
    if loading > 80:
        print(f"  WARNING: {transformer.id} at {loading:.1f}% loading")
```

### Demand Response Event Management

```python
from energy_grid import DemandResponseOrchestrator, DRProgram

orchestrator = DemandResponseOrchestrator(engine)

# Schedule a demand response event
event = orchestrator.create_event(
    program=DRProgram.CAPACITY_BID,
    event_type="economic",
    start_time="2024-07-15T14:00:00",
    end_time="2024-07-15T18:00:00",
    target_reduction_mw=25.0,
    commitment_window_hours=4
)

print(f"DR Event ID: {event.id}")
print(f"Enrolled capacity: {event.enrolled_capacity_mw:.1f} MW")
print(f"Expected reduction: {event.expected_reduction_mw:.1f} MW")

# Verify results post-event
verification = orchestrator.verify_event(event.id)
print(f"Actual reduction: {verification.actual_reduction_mw:.1f} MW")
print(f"Verification status: {verification.status}")
```

### Outage Detection and FLISR

```python
from energy_grid import OutageManager, OutageSeverity

outage_mgr = OutageManager(engine)

# Monitor for outages
active_outages = outage_mgr.get_active_outages(
    severity=OutageSeverity.CRITICAL,
    include_customers_affected=True
)

for outage in active_outages:
    print(f"OUTAGE: {outage.id}")
    print(f"  Location: {outage.fault_location}")
    print(f"  Customers affected: {outage.customers_affected:,}")
    print(f"  Estimated restoration: {outage.eta_restoration}")
    print(f"  Crew dispatched: {outage.crew_id}")

# Initiate FLISR sequence
flisr_result = outage_mgr.initiate_flisr(
    fault_id=outage.id,
    auto_isolate=True,
    restore_from_alternate_feed=True
)
print(f"Service restored to {flisr_result.restored_customers:,} customers")
print(f"Remaining without service: {flisr_result.remaining_affected:,}")
```

### Smart Streetlight Management

```python
from energy_grid import StreetlightManager, DimmingProfile

streetlights = StreetlightManager(engine)

# Configure adaptive dimming
streetlights.set_dimming_profile(
    zone_id="zone-downtown-core",
    profile=DimmingProfile.ADAPTIVE,
    parameters={
        "base_dimming_pct": 30,
        "motion_boost_pct": 100,
        "motion_boost_duration_s": 30,
        "ambient_light_threshold_lux": 50,
        "curfew_dimming_pct": 20,
        "curfew_start": "23:00",
        "curfew_end": "05:00"
    }
)

# Get energy savings report
report = streetlights.get_energy_report(
    zone_id="zone-downtown-core",
    period_days=30
)
print(f"Energy consumption: {report.consumption_kwh:,.0f} kWh")
print(f"Cost savings: ${report.cost_savings:.2f}")
print(f"Carbon reduction: {report.co2_reduction_kg:.1f} kg")
print(f"Faults detected: {report.faults_detected}")
```

### Power Quality Analysis

```python
from energy_grid import PowerQualityAnalyzer, PQEventType

pq_analyzer = PowerQualityAnalyzer(engine)

# Analyze PQ events in a substation
events = pq_analyzer.query_events(
    substation_id="substation-east-03",
    event_types=[PQEventType.VOLTAGE_SAG, PQEventType.HARMONIC],
    time_range=("2024-06-01", "2024-06-30")
)

for event in events:
    print(f"{event.timestamp}: {event.event_type.name}")
    print(f"  Magnitude: {event.magnitude:.2f} pu")
    print(f"  Duration: {event.duration_ms:.0f} ms")
    print(f"  Root cause: {event.root_cause}")
    print(f"  Equipment affected: {event.equipment_affected}")
```

## Best Practices

1. **N-1 Contingency** — The distribution system must be designed and operated to withstand the loss of any single component (transformer, feeder, cable) without sustained customer outage. FLISR configurations must be validated against N-1 scenarios quarterly.

2. **Voltage Regulation** — Maintain voltage within ANSI C84.1 Range A (0.95-1.05 pu) at all service points. With high DER penetration, monitor for voltage rise on lightly loaded feeders and coordinate DER inverter voltage regulation settings.

3. **Cybersecurity** — SCADA and ADMS systems must comply with NERC CIP standards. AMI head-end systems require encryption, authentication, and network segmentation. All remote dispatch of DERs must use authenticated, encrypted channels.

4. **Demand Response Verification** — All DR events must include baseline estimation (using the 10-of-10 or ISO-approved method) and meter-based verification. Never report demand reduction without measured verification.

5. **Solar Interconnection Studies** — Require interconnection studies for all DER installations above 25 kW to assess feeder capacity, voltage impact, and protection coordination. Aggregate DER visibility must be maintained at the distribution management level.

6. **Weather Hardening** — Critical infrastructure (substations, control centers, communication networks) must be hardened against the region's design weather event (typically 50-year or 100-year return period). Regularly update climate projections for long-term capital planning.

7. **EV Charging Coordination** — Coordinate EV charging infrastructure deployment with distribution feeder capacity. Implement managed charging (V1G) and vehicle-to-grid (V2G) programs to align charging load with grid conditions and avoid costly infrastructure upgrades.

8. **Data Governance** — Smart meter data is sensitive customer information. Implement strict access controls, data minimization, and purpose limitation. Customers should have portal access to their own interval data and control over third-party data sharing.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                       Energy Grid Platform                              │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │ AMI Smart    │  │ SCADA/ADMS   │  │ DER Inverters│  │ EVSE       │  │
│  │ Meters (1.2M)│  │ Telemetry    │  │ (Solar/Batt) │  │ Chargers   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘  │
│         │                 │                 │                │          │
│         ▼                 ▼                 ▼                ▼          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │              Data Integration Layer                              │    │
│  │  • 15-min AMI interval aggregation                              │    │
│  │  • SCADA polling (2-4 sec)                                      │    │
│  │  • DER inverter telemetry (1-5 min)                             │    │
│  │  • Weather API integration                                      │    │
│  └────────────────────────────┬────────────────────────────────────┘    │
│                               │                                        │
│              ┌────────────────┼────────────────┐                       │
│              ▼                ▼                ▼                       │
│  ┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐           │
│  │ Grid State       │ │ Outage Mgmt  │ │ DER Orchestration│           │
│  │ Estimation       │ │ & FLISR      │ │ & VPP Dispatch   │           │
│  │ • Voltage profile│ │ • Fault loc. │ │ • Solar/battery  │           │
│  │ • Load flow      │ │ • Isolation  │ │ • DR events      │           │
│  │ • Transformer    │ │ • Restoration│ │ • Transactive    │           │
│  └────────┬─────────┘ └──────┬───────┘ └────────┬─────────┘           │
│           │                  │                  │                      │
│           ▼                  ▼                  ▼                      │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │              Control & Output Layer                              │    │
│  │  • Demand response dispatch     • Streetlight management       │    │
│  │  • Voltage regulation commands   • Power quality alerts         │    │
│  │  • Customer portals & billing    • Regulatory reporting         │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

The platform follows a **utility operations architecture** integrating three domains: **Grid Operations** (real-time monitoring and control), **Customer Operations** (AMI, billing, DR programs), and **DER Operations** (distributed resource orchestration). The SCADA/ADMS layer provides sub-second control for protection and automation; the AMI layer provides 15-minute interval data for billing and analytics; the DER layer coordinates distributed resources across multiple time horizons.

## Performance Considerations

1. **AMI Data Volume** — 1.2 million meters at 15-minute intervals produce ~2.8 billion records per year (~50 GB compressed). Use time-series databases (InfluxDB, TimescaleDB) optimized for interval data.

2. **SCADA Latency** — Protection and control commands must execute within 4-16 cycles (67-267 ms at 60 Hz). Do not route critical protection functions through IT systems; use dedicated OT networks.

3. **State Estimation Convergence** — Distribution system state estimation must converge within 5-10 seconds for real-time operations. Leverage AMI data as pseudo-measurements to improve observability on unmonitored sections.

4. **FLISR Speed** — Automated fault isolation and restoration must complete within 60 seconds of fault detection. Pre-computed switching sequences enable faster execution than real-time optimization.

5. **DER Coordination** — Managing thousands of distributed inverters requires hierarchical control: primary (inverter autonomous), secondary (feeder-level voltage), tertiary (market dispatch). Avoid centralized control loops for individual devices.

6. **Demand Response Dispatch** — DR event signals must reach all enrolled devices within 5 minutes. Use multicast messaging (MQTT) rather than individual device polling for event distribution.

7. **Power Quality Monitoring** — PQ events require microsecond-level sampling. Deploy dedicated PQ monitors at substations and critical customers; do not rely on AMI data for PQ analysis.

8. **Streetlight Network** — Manage thousands of networked luminaires with mesh networking (Zigbee, LoRaWAN). Batch dimming commands to reduce network traffic; target <5 second response for motion-triggered adjustments.

## Security Considerations

1. **NERC CIP Compliance** — Bulk electric system (BES) cyber assets must meet NERC CIP standards for access control, audit logging, incident response, and recovery planning. Medium impact BES cyber systems require encryption and authentication.

2. **AMI Security** — Smart meter communication must use AES-128 encryption with device-level authentication. AMI head-end systems must be isolated from corporate networks with jump-box access only.

3. **SCADA/ADMS Isolation** — Operational technology (OT) networks must be physically or logically segmented from IT networks. No direct internet access for SCADA systems; use data diodes or unidirectional gateways for data export.

4. **DER Authentication** — All DER dispatch commands must be authenticated and encrypted. Prevent unauthorized control of customer-owned inverters through secure provisioning and certificate management.

5. **Customer Data Privacy** — Smart meter interval data reveals occupancy patterns, appliance usage, and lifestyle information. Implement strict access controls; customers must consent to third-party data sharing.

6. **Firmware Security** — All IoT devices (meters, inverters, EV chargers, streetlights) require signed firmware updates with secure boot. Maintain vulnerability management program for embedded devices.

7. **Incident Response** — Establish separate incident response procedures for cyber incidents affecting grid operations. Coordinate with utility SOC, ICS-CERT, and law enforcement as appropriate.

8. **Physical Security** — Substations and control centers require physical access controls, surveillance, and intrusion detection. Critical facilities (hospitals, emergency services) require enhanced protection per NERC CIP-014.

## Related Modules

- **urban-analytics** — Provides building footprints, land use, and population density for energy demand forecasting
- **traffic-management** — Coordinates EV charging signals with traffic patterns and transit electrification
- **public-safety** — Shares outage data for emergency response coordination and public notification
- **citizen-services** — Powers customer-facing energy portals, bill assistance programs, and community solar enrollment

## References

- **NERC CIP Standards** — North American Electric Reliability Corporation Critical Infrastructure Protection standards
- **IEEE 1547** — Standard for Interconnection and Interoperability of Distributed Energy Resources
- **IEC 61850** — Communication networks and systems for power utility automation
- **NIST Framework for Smart Grid Interoperability** — US standards framework for smart grid cybersecurity and interoperability
- **IEEE 2030.5** — Smart Energy Profile 2.0 for DER communication and control
- **OpenADR 2.0** — Open Automated Demand Response communication standard for DR event signaling

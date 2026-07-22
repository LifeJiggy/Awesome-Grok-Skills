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

---

## Extended Reference Guide

### Smart Grid Management Patterns

#### Distribution System State Estimation (DSSE)

Advanced state estimation for the medium-voltage and low-voltage distribution network. Uses SCADA measurements, AMI pseudo-measurements, and line sensor data to estimate voltage magnitudes and phase angles across the entire distribution system.

```python
from energy_grid import DistributionStateEstimator, EstimationMethod

estimator = DistributionStateEstimator(engine)

# Configure state estimation
estimator.configure(
    method=EstimationMethod.WEIGHTED_LEAST_SQUares,
    max_iterations=25,
    convergence_threshold=0.001,
    bad_data_detection=True,
    bad_data_threshold=3.0,
    pseudo_measurement_weights={
        "ami_aggregated": 0.8,
        "load_profile_estimated": 0.5,
        "smart_meter_interval": 0.9
    }
)

# Run state estimation
result = estimator.run_estimation(
    network_id="feeder-north-12",
    include_ami_pseudo=True,
    timestamp="2024-07-15T14:30:00"
)

print(f"State Estimation Results:")
print(f"  Converged: {result.converged}")
print(f"  Iterations: {result.iterations}")
print(f"  Max mismatch: {result.max_mismatch_pu:.6f}")
print(f"  Bad data detected: {result.bad_data_count}")

# Analyze voltage profile
voltage = result.voltage_profile
print(f"\nVoltage Profile:")
for bus in voltage.buses[:10]:
    status = "OVER" if bus.voltage_pu > 1.05 else \
             "UNDER" if bus.voltage_pu < 0.95 else "OK"
    print(f"  {bus.name}: {bus.voltage_pu:.4f} pu [{status}] "
          f"(angle: {bus.angle_deg:.2f}°)")

# Identify voltage violations
violations = result.voltage_violations
print(f"\nVoltage Violations: {len(violations)}")
for v in violations:
    print(f"  {v.bus_name}: {v.voltage_pu:.4f} pu (limit: {v.limit_pu:.2f})")
    print(f"    Cause: {v.likely_cause}")
    print(f"    Recommendation: {v.recommendation}")
```

#### Transformer Load Monitoring and Life Assessment

Tracks loading on distribution transformers and estimates remaining useful life based on loading history, ambient temperature, and insulation aging models. Prevents overloading and schedules proactive replacement.

```python
from energy_grid import TransformerMonitor, InsulationModel

monitor = TransformerMonitor(engine)

# Configure transformer monitoring
monitor.configure(
    insulation_model=InsulationModel.IEEE_C57_91,
    temperature_model="thermal_dynamic",
    hot_spot_rise_c=78,
    ambient_ref_c=30,
    loading_alarm_threshold_pct=80,
    loading_critical_threshold_pct=100,
    life_loss_alert_threshold_pct=5
)

# Get transformer fleet status
fleet = monitor.get_fleet_status(
    substation_id="substation-east-03",
    include_loading=True,
    include_temperature=True,
    include_life_loss=True
)

print(f"Transformer Fleet - Substation East-03:")
print(f"  Total transformers: {fleet.total_count}")
print(f"  Average loading: {fleet.avg_loading_pct:.1f}%")
print(f"  Overloaded: {fleet.overloaded_count}")
print(f"  Nearing end of life: {fleet.eol_warning_count}")

for xfmr in fleet.transformers:
    if xfmr.loading_pct > 70 or xfmr.estimated_life_remaining_pct < 30:
        print(f"\n  {xfmr.id} ({xfmr.rating_mva} MVA):")
        print(f"    Loading: {xfmr.loading_pct:.1f}%, "
              f"Hot spot: {xfmr.hot_spot_temp_c:.1f}°C")
        print(f"    Life consumed: {xfmr.life_consumed_pct:.1f}%, "
              f"Remaining: {xfmr.estimated_life_remaining_pct:.1f}%")
        print(f"    Install year: {xfmr.install_year}, "
              f"Last maintenance: {xfmr.last_maintenance_date}")

# Generate replacement plan
replacement_plan = monitor.generate_replacement_plan(
    horizon_years=10,
    annual_budget=2_000_000,
    prioritize_by="risk_weighted"
)
for year, replacements in replacement_plan.yearly.items():
    cost = sum(r.replacement_cost for r in replacements)
    print(f"\n{year}: {len(replacements)} replacements, ${cost:,.0f}")
    for r in replacements:
        print(f"  - {r.id}: {r.reason} (${r.replacement_cost:,.0f})")
```

### Demand Response and DER Management

#### Automated Demand Response Event Lifecycle

Manages the complete lifecycle of demand response events — from event creation and enrollment through dispatch, monitoring, verification, and settlement. Ensures accurate baseline estimation and verified demand reduction.

```python
from energy_grid import DREventLifecycle, DRProgram, BaselineMethod

lifecycle = DREventLifecycle(engine)

# Create and manage a DR event through its full lifecycle
event = lifecycle.create_event(
    program=DRProgram.ECONOMIC,
    event_type="price_response",
    start_time="2024-07-15T14:00:00",
    end_time="2024-07-15T18:00:00",
    target_reduction_mw=30.0,
    price_signal=0.25,
    notification_hours_ahead=24,
    baseline_method=BaselineMethod.NINE_OF_TEN
)

print(f"DR Event Created: {event.id}")
print(f"  Target reduction: {event.target_mw:.1f} MW")
print(f"  Enrolled capacity: {event.enrolled_mw:.1f} MW")
print(f"  Notification sent: {event.notification_time}")

# Monitor event in real-time
monitoring = lifecycle.monitor_event(event.id)
print(f"\nEvent Monitoring (current):")
print(f"  Status: {monitoring.status}")
print(f"  Elapsed: {monitoring.elapsed_minutes:.0f} min")
print(f"  Estimated reduction: {monitoring.estimated_reduction_mw:.1f} MW")
print(f"  Participating devices: {monitoring.active_devices}/{monitoring.enrolled_devices}")

# Post-event verification
verification = lifecycle.verify_event(event.id)
print(f"\nPost-Event Verification:")
print(f"  Baseline: {verification.baseline_mw:.1f} MW")
print(f"  Actual load: {verification.actual_load_mw:.1f} MW")
print(f"  Verified reduction: {verification.verified_reduction_mw:.1f} MW")
print(f"  Target achievement: {verification.achievement_pct:.1f}%")
print(f"  Settlement amount: ${verification.settlement_amount:,.2f}")
```

#### Virtual Power Plant (VPP) Dispatch Optimization

Aggregates distributed energy resources — solar inverters, battery storage, EV chargers, smart thermostats — into a virtual power plant that can provide grid services equivalent to a traditional power plant.

```python
from energy_grid import VPPDispatcher, GridService, DispatchMode

vpp = VPPDispatcher(engine)

# Configure VPP assets
vpp.register_assets([
    {
        "type": "rooftop_solar",
        "count": 5000,
        "total_capacity_mw": 25,
        "inverter_type": "grid_following",
        "curtailment_capable": True,
        "average_output_mw": 15
    },
    {
        "type": "battery_storage",
        "count": 800,
        "total_capacity_mw": 12,
        "total_energy_mwh": 48,
        "round_trip_efficiency": 0.90,
        "min_soc_pct": 10,
        "max_soc_pct": 90,
        "ramp_rate_mw_per_min": 6
    },
    {
        "type": "ev_charger_managed",
        "count": 2000,
        "total_capacity_mw": 16,
        "v2g_capable_count": 300,
        "v2g_capacity_mw": 2.4,
        "availability_window": "18:00-06:00"
    },
    {
        "type": "smart_thermostat",
        "count": 15000,
        "total_capacity_mw": 8,
        "precool_capable": True,
        "rebound_management": True
    },
])

# Optimize VPP dispatch for grid service
dispatch = vpp.optimize_dispatch(
    grid_service=GridService.PEAK_SHAVING,
    target_reduction_mw=40,
    dispatch_window_hours=4,
    mode=DispatchMode.ECONOMIC_OPTIMIZATION,
    include_degradation_costs=True
)

print(f"VPP Dispatch Optimization Results:")
print(f"  Target: {dispatch.target_mw:.1f} MW")
print(f"  Achievable: {dispatch.achievable_mw:.1f} MW")
print(f"  Marginal cost: ${dispatch.marginal_cost_per_mwh:.2f}/MWh")

print(f"\nDispatch Allocation:")
for asset_type in dispatch.allocation:
    print(f"  {asset_type.name}: {asset_type.dispatched_mw:.1f} MW "
          f"({asset_type.participation_pct:.0f}% of capacity)")
    print(f"    Cost: ${asset_type.cost_per_mwh:.2f}/MWh")
    print(f"    Response time: {asset_type.response_time_s:.0f}s")
```

#### Peer-to-Peer Energy Trading Platform

Enables neighbors with rooftop solar and battery storage to trade excess energy directly, reducing grid dependence and providing fair compensation to prosumers.

```python
from energy_grid import P2PEnergyTrading, TradingMechanism

trading = P2PEnergyTrading(engine)

# Configure trading platform
trading.configure(
    mechanism=TradingMechanism.DOUBLE_AUCTION,
    settlement_interval_minutes=15,
    max_price_per_kwh=0.35,
    min_price_per_kwh=0.05,
    grid_fee_per_kwh=0.02,
    settlement_currency="USD",
    smart_contract_enabled=True
)

# Register prosumers
trading.register_prosumer(
    prosumer_id="prosumer-001",
    solar_capacity_kw=8,
    battery_capacity_kwh=13.5,
    max_export_kw=6,
    max_import_kw=7.2,
    preferred_export_price=0.15,
    preferred_import_price=0.12
)

# Get market clearing results
market = trading.get_market_status()
print(f"P2P Energy Market Status:")
print(f"  Active prosumers: {market.active_prosumers}")
print(f"  Total solar output: {market.total_solar_kw:.1f} kW")
print(f"  Total battery SOC: {market.avg_battery_soc_pct:.1f}%")

print(f"\nCurrent Auction:")
print(f"  Supply bids: {market.supply_bids}")
print(f"  Demand bids: {market.demand_bids}")
print(f"  Clearing price: ${market.clearing_price_per_kwh:.3f}/kWh")
print(f"  Volume traded: {market.volume_traded_kwh:.1f} kWh")
print(f"  Grid import avoided: {market.grid_import_avoided_kwh:.1f} kWh")

# Settlement summary
settlement = trading.get_settlement(period="2024-07")
print(f"\nJuly Settlement Summary:")
print(f"  Total energy traded: {settlement.total_traded_kwh:,.1f} kWh")
print(f"  Total value: ${settlement.total_value:,.2f}")
print(f"  Average price: ${settlement.avg_price_per_kwh:.3f}/kWh")
print(f"  Grid fees collected: ${settlement.grid_fees:,.2f}")
```

### Grid Resilience and Microgrid Operations

#### Microgrid Formation and Islanding Control

Manages the formation of microgrids during grid disturbances — detecting islanding conditions, reconfiguring network topology, balancing generation and load within the microgrid, and coordinating reconnection when the main grid is restored.

```python
from energy_grid import MicrogridController, IslandingMode

controller = MicrogridController(engine)

# Configure microgrid boundaries
controller.define_microgrid(
    microgrid_id="mg-hospital-district",
    boundary_feeder="feeder-hospital-01",
    critical_loads=[
        {"name": "General Hospital", "load_mw": 8.5, "priority": 1},
        {"name": "Emergency Department", "load_mw": 2.0, "priority": 1},
        {"name": "Fire Station #5", "load_mw": 0.5, "priority": 1},
        {"name": "Water Treatment", "load_mw": 3.0, "priority": 2},
        {"name": "Community Center (Shelter)", "load_mw": 1.5, "priority": 2},
    ],
    generation_assets=[
        {"name": "Hospital CHP", "capacity_mw": 4.0, "type": "natural_gas"},
        {"name": "Solar Array", "capacity_mw": 1.5, "type": "solar_pv"},
        {"name": "Battery Storage", "capacity_mw": 2.0, "capacity_mwh": 8.0, "type": "bess"},
    ],
    islanding_mode=IslandingMode.MANUAL_WITH_AUTO_BACKUP,
    load_shedding_priorities=["non_critical", "priority_3", "priority_2"]
)

# Simulate islanding event
result = controller.simulate_islanding(
    microgrid_id="mg-hospital-district",
    fault_location="substation-hospital-01",
    fault_type="upstream_outage",
    estimated_restoration_hours=8
)

print(f"Microgrid Islanding Simulation:")
print(f"  Islanding detected: {result.detection_time_s:.1f}s")
print(f"  Island formed: {result.island_success}")
print(f"  Critical loads served: {result.critical_loads_served_pct:.1f}%")
print(f"  Non-critical shed: {result.non_critical_shed_mw:.1f} MW")
print(f"  Battery SOC at island start: {result.initial_battery_soc_pct:.1f}%")
print(f"  Estimated endurance: {result.estimated_endurance_hours:.1f} hours")

# Monitor microgrid status during islanding
status = controller.get_microgrid_status("mg-hospital-district")
print(f"\nMicrogrid Status:")
print(f"  Mode: {status.mode}")
print(f"  Generation: {status.total_generation_mw:.1f} MW")
print(f"  Load: {status.total_load_mw:.1f} MW")
print(f"  Battery SOC: {status.battery_soc_pct:.1f}%")
print(f"  Frequency: {status.frequency_hz:.2f} Hz")
print(f"  Voltage: {status.voltage_pu:.3f} pu")
```

#### Weather-Resilient Grid Operations

Prepares the grid for extreme weather events — pre-positioning restoration resources, adjusting DER dispatch, implementing pre-storm load shedding, and coordinating mutual aid.

```python
from energy_grid import WeatherResilienceManager, StormSeverity

resilience = WeatherResilienceManager(engine)

# Monitor weather threat
threat = resilience.assess_threat(
    weather_event="hurricane_category_3",
    approach_time_hours=48,
    affected_area="metro_coastal_zone"
)

print(f"Weather Threat Assessment:")
print(f"  Event: {threat.event_type}")
print(f"  Expected arrival: {threat.arrival_time}")
print(f"  Wind speed forecast: {threat.max_wind_speed_mph:.0f} mph")
print(f"  Flooding risk: {threat.flooding_risk}")
print(f"  Estimated outages: {threat.estimated_outages:,}")
print(f"  Estimated customers affected: {threat.estimated_customers:,}")

# Activate storm preparedness
preparedness = resilience.activate_storm_preparedness(
    threat_id=threat.id,
    severity=StormSeverity.HIGH,
    actions=[
        "pre_inspect_critical_feeders",
        "position_restoration_crews",
        "top_off_battery_storage",
        "activate_mobile_generators",
        "notify_critical_customers",
        "implement_pre_storm_der_dispatch",
    ]
)

print(f"\nStorm Preparedness Activated:")
for action in preparedness.actions_completed:
    print(f"  [OK] {action.name}: {action.status}")
for action in preparedness.actions_pending:
    print(f"  [..] {action.name}: {action.status}")

# Coordinate restoration after storm
restoration = resilience.coordinate_restoration(
    threat_id=threat.id,
    priority_order=[
        "hospitals_and_emergency",
        "water_and_sewer",
        "communication_infrastructure",
        "residential_critical",
        "commercial",
        "general_residential"
    ],
    mutual_aid_activated=True,
    mutual_aid_crews=50,
    estimated_total_restoration_hours=72
)

print(f"\nRestoration Plan:")
print(f"  Phase 1 (0-12h): Critical infrastructure - {restoration.phase1_customers:,} customers")
print(f"  Phase 2 (12-36h): Priority residential - {restoration.phase2_customers:,} customers")
print(f"  Phase 3 (36-72h): General restoration - {restoration.phase3_customers:,} customers")
```

### EV Charging Infrastructure and Grid Integration

#### Managed EV Charging (V1G) Optimization

Optimizes EV charging schedules to align with grid conditions — shifting charging to off-peak hours, avoiding feeder overload, and maximizing use of available renewable energy.

```python
from energy_grid import ManagedChargingOptimizer, ChargingMode

optimizer = ManagedChargingOptimizer(engine)

# Configure managed charging program
optimizer.configure(
    program_name="Off-Peak Charging Incentive",
    enrolled_vehicles=5000,
    total_charging_capacity_kw=25000,
    charging_modes=[ChargingMode.L1, ChargingMode.L2],
    optimization_objectives=[
        {"name": "minimize_peak_demand", "weight": 0.4},
        {"name": "maximize_renewable_use", "weight": 0.3},
        {"name": "minimize_charging_cost", "weight": 0.2},
        {"name": "maximize_driver_satisfaction", "weight": 0.1},
    ],
    constraints={
        "min_charge_by_departure": True,
        "max_soc_at_departure": 0.90,
        "feeder_capacity_limit_kw": 15000,
        "price_signal_integration": True
    }
)

# Optimize charging schedule for next 24 hours
schedule = optimizer.optimize(
    forecast_horizon_hours=24,
    renewable_forecast=True,
    price_forecast=True,
    vehicle_availability_model="historical_patterns"
)

print(f"Optimized Charging Schedule:")
print(f"  Total vehicles: {schedule.total_vehicles}")
print(f"  Scheduled charging: {schedule.total_energy_mwh:.1f} MWh")
print(f"  Peak demand reduction: {schedule.peak_reduction_kw:.0f} kW")
print(f"  Renewable energy used: {schedule.renewable_energy_pct:.1f}%")
print(f"  Average charging cost: ${schedule.avg_cost_per_kwh:.3f}/kWh")

print(f"\nHourly Charging Profile:")
for hour in schedule.hourly_profile:
    bar = "#" * int(hour.demand_kw / schedule.peak_demand_kw * 30)
    print(f"  {hour.hour:02d}:00: {bar} {hour.demand_kw:.0f} kW "
          f"(renewable: {hour.renewable_pct:.0f}%)")
```

#### EV Charging Station Health Monitoring

Monitors the health and availability of public EV charging stations — detecting faults, tracking utilization, managing maintenance, and ensuring reliable service.

```python
from energy_grid import EVChargingMonitor, StationType

monitor = EVChargingMonitor(engine)

# Get charging station fleet status
fleet = monitor.get_fleet_status(
    network_id="city_public_charging",
    include_health=True,
    include_utilization=True
)

print(f"EV Charging Fleet Status:")
print(f"  Total stations: {fleet.total_stations}")
print(f"  Online: {fleet.online_count} ({fleet.online_pct:.1f}%)")
print(f"  Faulted: {fleet.faulted_count}")
print(f"  In maintenance: {fleet.maintenance_count}")
print(f"  Available: {fleet.available_count}")
print(f"  In use: {fleet.in_use_count}")

print(f"\nFleet Utilization:")
print(f"  Average utilization: {fleet.avg_utilization_pct:.1f}%")
print(f"  Peak utilization: {fleet.peak_utilization_pct:.1f}%")
print(f"  Average session duration: {fleet.avg_session_duration_min:.0f} min")
print(f"  Energy dispensed today: {fleet.energy_dispensed_today_mwh:.1f} MWh")

# Check for faults
faults = monitor.get_active_faults()
for fault in faults:
    print(f"\nFAULT: {fault.station_id}")
    print(f"  Location: {fault.address}")
    print(f"  Type: {fault.fault_type}")
    print(f"  Severity: {fault.severity}")
    print(f"  Since: {fault.detected_at}")
    print(f"  Impact: {fault.impact_description}")

# Generate maintenance schedule
maintenance = monitor.generate_maintenance_schedule(
    horizon_days=30,
    prioritize_by="impact_weighted"
)
print(f"\nMaintenance Schedule (next 30 days):")
for task in maintenance.tasks[:10]:
    print(f"  {task.station_id}: {task.task_type} "
          f"(priority: {task.priority}, ETA: {task.scheduled_date})")
```

### Power Quality and Reliability Analytics

#### Advanced Power Quality Event Analysis

Detects, classifies, and analyzes power quality events — voltage sags, swells, interruptions, harmonics, and transients. Correlates events with equipment damage, customer complaints, and grid conditions.

```python
from energy_grid import AdvancedPQAnalyzer, PQEventClass

analyzer = AdvancedPQAnalyzer(engine)

# Analyze PQ events for a substation
analysis = analyzer.analyze_substation(
    substation_id="substation-industrial-01",
    period="2024-Q2",
    include_power_spectral_density=True,
    include_disturbance_source_tracing=True
)

print(f"Power Quality Analysis - Substation Industrial-01 (Q2 2024):")
print(f"  Total events: {analysis.total_events}")
print(f"  SAIDI contribution: {analysis.saidi_contribution_min:.1f} min")
print(f"  SAIFI contribution: {analysis.saifi_contribution:.4f}")

print(f"\nEvent Classification:")
for event_class in analysis.event_distribution:
    print(f"  {event_class.name}: {event_class.count} ({event_class.percentage:.1f}%)")
    print(f"    Avg duration: {event_class.avg_duration_ms:.0f} ms")
    print(f"    Avg magnitude: {event_class.avg_magnitude:.3f} pu")

# Deep dive on harmonics
harmonics = analysis.harmonic_analysis
print(f"\nHarmonic Analysis:")
print(f"  THDv: {harmonics.thdv_pct:.2f}% (limit: 5.0%)")
print(f"  THDi: {harmonics.thdi_pct:.2f}% (limit: 15.0%)")
print(f"  Dominant harmonic: {harmonics.dominant_harmonic_order}th "
      f"({harmonics.dominant_harmonic_magnitude_pct:.1f}%)")
print(f"  Likely source: {harmonics.likely_source}")

# Identify chronic PQ problems
chronic = analysis.chronic_problems
print(f"\nChronic PQ Problems:")
for problem in chronic:
    print(f"  {problem.location}: {problem.description}")
    print(f"    Frequency: {problem.occurrences_per_month:.1f}/month")
    print(f"    Customer impact: {problem.customers_affected}")
    print(f"    Recommended mitigation: {problem.mitigation}")
```

#### Reliability Index Calculation (SAIDI, SAIFI, CAIDI)

Calculates standard utility reliability indices that track the frequency, duration, and scope of customer outages. These indices are reported to regulators and compared against benchmarks.

```python
from energy_grid import ReliabilityIndexCalculator, ReliabilityMetric

calculator = ReliabilityIndexCalculator(engine)

# Calculate reliability indices
indices = calculator.calculate(
    period="2024-annual",
    granularity="monthly",
    include_benchmarks=True,
    include_trends=True
)

print(f"Reliability Indices (2024):")
print(f"  SAIDI (System Average Interruption Duration Index): {indices.saidi_min:.1f} min/customer")
print(f"  SAIFI (System Average Interruption Frequency Index): {indices.saifi:.3f} interruptions/customer")
print(f"  CAIDI (Customer Average Interruption Duration Index): {indices.caidi_min:.1f} min/interruption")
print(f"  MAIFI (Momentary Average Interruption Frequency Index): {indices.maifi:.3f}")

print(f"\nBenchmark Comparison:")
print(f"  SAIDI: {indices.saidi_min:.1f} vs national avg {benchmarks.saidi_national:.1f} "
      f"({'better' if indices.saidi_min < benchmarks.saidi_national else 'worse'})")
print(f"  SAIFI: {indices.saifi:.3f} vs national avg {benchmarks.saifi_national:.3f} "
      f"({'better' if indices.saifi < benchmarks.saifi_national else 'worse'})")

# Analyze by cause
by_cause = calculator.analyze_by_cause(period="2024-annual")
print(f"\nOutage Causes:")
for cause in by_cause:
    print(f"  {cause.name}: {cause.count} events, "
          f"{cause.total_customer_minutes:,.0f} customer-minutes "
          f"({cause.percentage_of_saidi:.1f}% of SAIDI)")

# Analyze by customer type
by_type = calculator.analyze_by_customer_type(period="2024-annual")
print(f"\nBy Customer Type:")
for ct in by_type:
    print(f"  {ct.name}: SAIDI={ct.saidi_min:.1f} min, SAIFI={ct.saifi:.3f}")
```

### Streetlight and Public Lighting Intelligence

#### Adaptive Lighting Control with Environmental Sensing

Smart streetlights with adaptive dimming, environmental sensors, and connectivity to the city's data platform. Streetlights serve as the backbone for IoT sensor networks.

```python
from energy_grid import AdaptiveLightingControl, LightingZone

control = AdaptiveLightingControl(engine)

# Configure adaptive lighting zones
control.configure_zone(
    zone_id="zone-residential-north",
    zone_type=LightingZone.RESIDENTIAL,
    luminaires=2500,
    lighting_class="M3",
    adaptive_config={
        "baseline_dimming_pct": 40,
        "motion_detected_dimming_pct": 100,
        "motion_boost_duration_s": 30,
        "ambient_light_threshold_lux": 50,
        "curfew_dimming_pct": 25,
        "curfew_hours": ("23:00", "05:00"),
        "seasonal_adjustment": True,
        "special_event_override": True
    },
    sensors={
        "motion_detection": {"type": "radar", "range_m": 30},
        "ambient_light": {"type": "photocell", "accuracy_lux": 5},
        "noise_level": {"type": "microphone", "range_db": 30},
        "air_quality": {"type": "pm25_sensor", "range_ugm3": 500},
        "pedestrian_count": {"type": "infrared", "accuracy": 0.95}
    }
)

# Get lighting performance
performance = control.get_zone_performance(
    zone_id="zone-residential-north",
    period_days=30
)

print(f"Lighting Performance - Residential North (30 days):")
print(f"  Energy consumption: {performance.consumption_kwh:,.0f} kWh")
print(f"  Energy cost: ${performance.cost:,.2f}")
print(f"  Energy savings vs fixed lighting: {performance.savings_pct:.1f}%")
print(f"  Average dimming level: {performance.avg_dimming_pct:.1f}%")
print(f"  Motion detection rate: {performance.motion_detection_rate:.1f}/hour")
print(f"  Faults detected: {performance.faults_detected}")
print(f"  Avg response time to motion: {performance.avg_motion_response_ms:.0f} ms")

# Environmental data collected
env = performance.environmental_summary
print(f"\nEnvironmental Data Collected:")
print(f"  Avg noise level: {env.avg_noise_db:.1f} dB")
print(f"  Avg PM2.5: {env.avg_pm25_ugm3:.1f} ug/m3")
print(f"  Avg pedestrian count: {env.avg_pedestrians_per_hour:.0f}/hour")
```

### Energy Data Analytics and Reporting

#### Building Energy Benchmarking Platform

Compares building energy performance across the city's building stock, enabling benchmarking, compliance tracking, and energy efficiency program targeting.

```python
from energy_grid import BuildingBenchmarkPlatform, BuildingType

platform = BuildingBenchmarkPlatform(engine)

# Benchmark a building
benchmark = platform.benchmark_building(
    building_id="bldg-commercial-1234",
    building_type=BuildingType.COMMERCIAL_OFFICE,
    area_sqft=50000,
    year_built=1995,
    energy_data={
        "annual_electricity_kwh": 850000,
        "annual_natural_gas_therms": 12000,
        "on_site_solar_kwh": 45000,
    }
)

print(f"Building Energy Benchmark - Commercial Office #1234:")
print(f"  Energy Use Intensity: {benchmark.eui_kbtu_sqft:.1f} kBtu/sqft")
print(f"  Electricity Use Intensity: {benchmark.eui_electric_kbtu_sqft:.1f} kBtu/sqft")
print(f"  Benchmark percentile: {benchmark.percentile:.0f}th percentile")
print(f"  Star rating: {'*' * benchmark.star_rating}/5")
print(f"  vs. similar buildings: {benchmark.vs_similar_pct:+.1f}%")
print(f"  vs. code baseline: {benchmark.vs_code_baseline_pct:+.1f}%")

# Citywide benchmarking report
city_report = platform.citywide_report(
    building_type="all",
    year=2024,
    include_compliance=True,
    include_program_recommendations=True
)

print(f"\nCitywide Building Energy Report (2024):")
print(f"  Buildings benchmarked: {city_report.buildings_count:,}")
print(f"  Total floor area: {city_report.total_area_sqft:,.0f} sqft")
print(f"  Average EUI: {city_report.avg_eui_kbtu_sqft:.1f} kBtu/sqft")
print(f"  Energy Star certified: {city_report.star_certified_count}")
print(f"  Benchmark compliance rate: {city_report.compliance_pct:.1f}%")

# Identify efficiency program targets
targets = platform.identify_efficiency_targets(
    eui_reduction_target_pct=20,
    program_budget=5_000_000,
    prioritization="cost_effectiveness"
)
print(f"\nEfficiency Program Targets:")
for target in targets[:5]:
    print(f"  {target.building_id}: EUI {target.eui_kbtu_sqft:.1f} -> "
          f"{target.projected_eui:.1f} kBtu/sqft")
    print(f"    Estimated savings: ${target.annual_savings:,.0f}/year")
    print(f"    Incentive: ${target.incentive_amount:,.0f}")
```

This extended reference provides comprehensive patterns for smart grid management, demand response, DER orchestration, grid resilience, EV charging integration, power quality analysis, and energy analytics. Each section includes production-ready code examples adaptable to specific utility contexts and regulatory requirements.

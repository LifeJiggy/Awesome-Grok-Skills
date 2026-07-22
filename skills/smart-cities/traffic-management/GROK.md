---
name: "traffic-management"
category: "smart-cities"
version: "1.0.0"
tags: ["smart-cities", "traffic-management", "transportation", "adaptive-signal", "mobility"]
---

# Traffic Management — Adaptive Urban Mobility Platform

## Overview

The Traffic Management module provides intelligent transportation system (ITS) capabilities for real-time traffic monitoring, adaptive signal control, incident detection, and mobility optimization. It ingests data from loop detectors, radar sensors, cameras (with computer vision analytics), connected vehicles (V2X), transit AVL systems, and crowd-sourced navigation data to maintain a live model of citywide traffic conditions.

This module operates a closed-loop control system: sensors observe conditions, the analytics engine classifies and predicts traffic states, the signal controller applies optimized timing plans, and performance is continuously measured against targets (travel time, delay, throughput, emissions). It supports coordinated signal networks across hundreds of intersections, freeway mainline and ramp metering, and multimodal priority for transit, emergency vehicles, and vulnerable road users.

The traffic management platform integrates with traveler information systems, parking guidance, emergency vehicle preemption, and citywide data exchange hubs (e.g., TMDD, NTCIP, DATEX II) to provide a unified mobility intelligence layer.

## Core Capabilities

### 1. Real-Time Traffic State Estimation
Fusion of multi-sensor inputs — inductive loops, radar, Bluetooth/WiFi travel time, connected vehicle probe data, and camera-based counts — into a unified traffic state model. Produces real-time speed, density, and volume estimates for every network link with confidence intervals and anomaly flags.

### 2. Adaptive Signal Control
Implementation of adaptive traffic signal control algorithms (SCOOT, SCATS, or custom AI-based) that adjust cycle lengths, phase splits, and offsets in real-time based on detected demand. Supports coordinated corridors, flexible phasing for pedestrian/bicycle priority, and emergency vehicle preemption.

### 3. Incident Detection and Management
Automatic incident detection (AID) using video analytics, speed-drop algorithms, and multi-sensor correlation. Provides alert generation, estimated clearance time, downstream impact assessment, and automated response plan activation (dynamic message signs, rerouting suggestions).

### 4. Transit Signal Priority (TSP)
Conditional and unconditional transit signal priority that detects approaching transit vehicles and extends green phases or truncates red phases to minimize transit delay. Integrates with AVL/CAD systems and supports schedule adherence-based priority logic.

### 5. Ramp Metering and Freeway Operations
Coordinated ramp metering algorithms (ALINEA, demand-capacity) that regulate freeway on-ramp flows to maintain mainline density below critical thresholds. Integrates with freeway management systems for incident response and work zone management.

### 6. Travel Time Prediction and Advisory
Short-term (5-30 min) and medium-term (1-4 hour) travel time prediction using machine learning models trained on historical and real-time data. Powers dynamic message signs, navigation app integrations, and traveler information portals.

### 7. Multimodal Mobility Analytics
Detection and classification of all road users — motor vehicles, transit, bicycles, pedestrians, micro-mobility — with separate flow analysis for each mode. Supports complete-street design evaluation and multimodal level-of-service measurement.

### 8. Parking and curb Management Integration
Real-time parking occupancy tracking, dynamic pricing signals, curb-space allocation for delivery/loading, and integration with smart parking guidance systems to reduce cruising-for-parking traffic.

## Usage Examples

### Traffic Management Engine Setup

```python
from traffic_management import TrafficManagementEngine, SensorConfig, SignalNetworkConfig

engine = TrafficManagementEngine(
    city_id="metro-chicago-001",
    sensor_config=SensorConfig(
        loop_detectors=1200,
        radar_sensors=340,
        cameras_with_cv=180,
        bluetooth_readers=95,
        v2x_equipped_intersections=60
    ),
    signal_config=SignalNetworkConfig(
        controller_type="ntcip_compatible",
        adaptive_algorithm="ai_based",
        num_intersections=850,
        coordination_groups=12,
        cycle_length_range=(60, 150),
        offset_optimization=True
    )
)

engine.configure()
status = engine.get_status()
print(f"Connected sensors: {status['sensors_online']}/{status['sensors_total']}")
print(f"Signal controllers: {status['controllers_online']}/{status['controllers_total']}")
```

### Real-Time Traffic State Monitoring

```python
from traffic_management import TrafficStateMonitor, RoadType

monitor = TrafficStateMonitor(engine)

# Get current conditions for a corridor
conditions = monitor.get_corridor_status(
    corridor_id="corridor-michigan-ave",
    include_lane_detail=True
)

for link in conditions.links:
    print(f"{link.name}: speed={link.avg_speed_kmh:.0f} km/h, "
          f"volume={link.volume_vph}, "
          f"occupancy={link.occupancy_pct:.1f}%")
    if link.speed_ratio < 0.5:
        print(f"  WARNING: Congestion detected (speed ratio: {link.speed_ratio:.2f})")
```

### Adaptive Signal Optimization

```python
from traffic_management import SignalOptimizer, OptimizationTarget

optimizer = SignalOptimizer(engine)

# Optimize a corridor for throughput
result = optimizer.optimize_corridor(
    corridor_id="corridor-michigan-ave",
    target=OptimizationTarget.THROUGHPUT,
    constraints={
        "min_pedestrian_phase_s": 15,
        "max_cycle_length_s": 120,
        "emergency_preemption": True,
        "transit_priority": True
    }
)

print(f"Optimized {result.intersections_modified} intersections")
print(f"Expected throughput improvement: {result.throughput_delta_pct:+.1f}%")
print(f"Expected delay reduction: {result.delay_delta_pct:+.1f}%")

# Apply changes with safety validation
if result.safety_check_passed:
    optimizer.apply_timing_plan(result.timing_plan_id, dry_run=False)
```

### Incident Detection and Response

```python
from traffic_management import IncidentDetector, IncidentSeverity

detector = IncidentDetector(engine)

# Monitor for incidents
alerts = detector.scan_incidents(
    time_window_minutes=5,
    severity_threshold=IncidentSeverity.MODERATE
)

for alert in alerts:
    print(f"INCIDENT: {alert.type} at {alert.location}")
    print(f"  Severity: {alert.severity.name}")
    print(f"  Estimated clearance: {alert.eta_clearance_min} min")
    print(f"  Affected lanes: {alert.lanes_blocked}/{alert.lanes_total}")
    print(f"  Downstream impact: {alert.affected_links} links")

    # Trigger automated response
    detector.activate_response_plan(
        incident_id=alert.id,
        plan="moderate_incident_standard"
    )
```

### Travel Time Prediction

```python
from traffic_management import TravelTimePredictor, PredictionHorizon

predictor = TravelTimePredictor(engine)

# Predict travel times for commuter routes
predictions = predictor.predict_routes(
    routes=[
        {"origin": "suburban-north-01", "destination": "downtown-core"},
        {"origin": "suburban-west-02", "destination": "downtown-core"},
    ],
    horizon=PredictionHorizon.HOUR,
    include_confidence=True
)

for route in predictions:
    print(f"Route: {route.origin} -> {route.destination}")
    for prediction in route.forecasts:
        print(f"  {prediction.departure_time}: {prediction.travel_time_min:.0f} min "
              f"(CI: {prediction.ci_lower:.0f}-{prediction.ci_upper:.0f})")
```

### Transit Signal Priority

```python
from traffic_management import TransitPriorityManager, PriorityMode

tpm = TransitPriorityManager(engine)

# Configure TSP for a bus route
tpm.configure_route(
    route_id="bus-route-42",
    priority_mode=PriorityMode.CONDITIONAL,
    conditions={
        "schedule_deviation_threshold_min": 3,
        "min_passengers": 10,
        "max_extension_s": 20,
        "max_truncation_s": 10
    }
)

# Get TSP effectiveness metrics
metrics = tpm.get_effectiveness(
    route_id="bus-route-42",
    period_days=30
)
print(f"TSP activations: {metrics.total_activations}")
print(f"Average time saved per activation: {metrics.avg_time_saved_s:.1f}s")
print(f"On-time performance improvement: {metrics.otp_delta_pct:+.1f}%")
```

## Best Practices

1. **Fail-Safe Defaults** — All signal controllers must operate in fixed-time fallback mode when communication with the adaptive system is lost. Never leave intersections uncontrolled due to system failure.

2. **Sensor Redundancy** — Deploy overlapping sensor coverage at critical intersections. Use camera-based analytics as backup for loop detectors and cross-validate counts between sensor types.

3. **Pedestrian Safety First** — Minimum pedestrian phase lengths must be enforced regardless of traffic optimization targets. ADA compliance (pushbutton detection, accessible pedestrian signals) is non-negotiable.

4. **Coordination Tuning** — Re-optimize signal coordination plans quarterly or after any major network change (new developments, road construction, transit route changes). Static timing plans degrade rapidly.

5. **Data Retention** — Retain raw traffic data for at least 2 years for trend analysis and model training. Aggregate summary data should be retained indefinitely for long-range planning.

6. **Performance Measurement** — Establish baseline conditions before deploying adaptive control. Continuously measure against the baseline to quantify the actual (not theoretical) benefit of adaptive operations.

7. **Emergency Coordination** — Maintain direct communication channels with emergency dispatch for signal preemption. Preemption requests should override all other optimization goals within 1 second of receipt.

8. **Privacy Protection** — Bluetooth/WiFi travel time systems must use hashed or anonymized MAC addresses with no more than 24-hour retention. Camera analytics should count and classify, not identify individuals.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      Traffic Management Platform                        │
├─────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │ Loop/Radar   │  │ CV Cameras   │  │ BT/WiFi      │  │ V2X/C-V2X  │  │
│  │ Detectors    │  │ (Analytics)  │  │ Readers      │  │ Beacons    │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └─────┬──────┘  │
│         │                 │                 │                │          │
│         ▼                 ▼                 ▼                ▼          │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │              Sensor Fusion & State Estimation                   │    │
│  │  • Multi-sensor Kalman filtering                                │    │
│  │  • Real-time speed/density/volume per link                      │    │
│  │  • Confidence scoring & anomaly flagging                        │    │
│  └────────────────────────────┬────────────────────────────────────┘    │
│                               │                                        │
│              ┌────────────────┼────────────────┐                       │
│              ▼                ▼                ▼                       │
│  ┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐           │
│  │ Adaptive Signal  │ │ Incident     │ │ Travel Time      │           │
│  │ Control (AI)     │ │ Detection    │ │ Prediction (ML)  │           │
│  │ • Cycle/phase    │ │ • Video AID  │ │ • Short-term     │           │
│  │ • Offset optim.  │ │ • Speed drop │ │ • Medium-term    │           │
│  │ • Coordination   │ │ • Impact est.│ │ • Route-level    │           │
│  └────────┬─────────┘ └──────┬───────┘ └────────┬─────────┘           │
│           │                  │                  │                      │
│           ▼                  ▼                  ▼                      │
│  ┌─────────────────────────────────────────────────────────────────┐    │
│  │              Output & Control Layer                             │    │
│  │  • NTCIP/TMDD signal control  • DMS/messaging                  │    │
│  │  • Transit priority (TSP)     • Ramp metering                  │    │
│  │  • Dashboards & alerts        • Historical archives            │    │
│  └─────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

The platform implements a **closed-loop control architecture**: sensors observe, the fusion engine estimates state, optimization algorithms compute timing plans, and controllers execute changes. The system supports fail-safe defaults — all intersections revert to fixed-time operation if communication with the adaptive system is lost.

## Performance Considerations

1. **Sensor Fusion Latency** — End-to-end from sensor reading to state estimate must be under 5 seconds for adaptive control effectiveness. Use streaming architectures (Kafka/Kinesis) rather than batch processing.

2. **Signal Control Response** — Adaptive timing plan computation must complete within one cycle length (60-150 seconds). Pre-compute candidate plans for common demand patterns; select and adjust rather than generate from scratch.

3. **Data Volume** — A 1000-intersection network with 10-second loop samples generates ~3.1 billion records per year. Aggregate to 5-minute intervals for storage; retain raw data only for 30-90 days.

4. **Network Bandwidth** — Camera analytics produce 10-50x more data than point sensors. Process video at the edge; transmit only counts, classifications, and events to central systems.

5. **Prediction Accuracy** — Short-term (5-15 min) predictions achieve 85-95% accuracy; medium-term (1-4 hour) drops to 70-85%. Always report confidence intervals; use ensemble models for critical decisions.

6. **Coordination Optimization** — Corridor coordination across 50+ intersections is NP-hard. Use genetic algorithms or gradient-based heuristics with 5-10 minute convergence targets rather than exhaustive search.

7. **Incident Detection Speed** — Automatic incident detection must alert within 60 seconds of occurrence. Multi-sensor correlation reduces false alarms from ~50% (single sensor) to <15%.

8. **Scalability** — Design for horizontal scaling by geographic partitioning (districts/zones). Each partition operates independently; cross-partition coordination only for boundary intersections.

## Security Considerations

1. **Signal Controller Security** — All NTCIP communication must use SNMPv3 with authentication and encryption. Never allow unauthenticated access to signal control interfaces.

2. **Camera Privacy** — Video analytics must process and discard raw frames at the edge. Only transmit counts, classifications, and metadata — never raw video to central systems.

3. **Bluetooth/WiFi Anonymization** — MAC addresses must be hashed with rotating salts and retained for no more than 24 hours. Use randomized probe requests for travel time measurement to prevent tracking.

4. **V2X Authentication** — Connected vehicle messages must be signed with valid PKI certificates. Reject unsigned or expired certificate messages; maintain certificate revocation lists.

5. **System Resilience** — Signal controllers must operate autonomously if network connectivity is lost. Heartbeat monitoring detects communication failures within 30 seconds.

6. **Access Control** — Signal timing plan changes require authenticated operators with role-based permissions. All changes logged with operator ID, timestamp, and before/after values.

7. **Penetration Testing** — Conduct annual penetration testing of all externally-facing traffic management interfaces. Isolate SCADA/control networks from corporate IT networks.

8. **Incident Data Protection** — Incident location data with potential victim information must be access-controlled. Release only aggregated statistics for public reporting; protect individual incident details.

## Related Modules

- **urban-analytics** — Provides infrastructure utilization data and land-use context for traffic demand modeling
- **energy-grid** — Coordinates EV charging demand signals and smart grid interaction for electrified transit
- **public-safety** — Shares incident data for coordinated emergency response and traffic management
- **citizen-services** — Powers traveler information portals and citizen reporting of traffic issues

## References

- **NTCIP 1202** — National Transportation Communications for ITS Protocol — Object definitions for signal control
- **TMDD v3.0** — Traffic Management Data Dictionary standard for center-to-center communication
- **ITE Traffic Engineering Handbook** — Professional reference for signal timing, capacity analysis, and ITS design
- **FHWA Signal Timing Manual** — Federal guidance on adaptive signal control implementation and evaluation
- **ITE Journal** — Institute of Transportation Engineers technical publications
- **US DOT ITS Standards Program** — Federal standards for connected vehicle and intelligent transportation systems

---

## Extended Reference Guide

### Traffic Flow Optimization Patterns

#### Dynamic Signal Timing Optimization

Adaptive signal control systems continuously optimize cycle lengths, phase splits, and offsets based on real-time demand. The optimization engine evaluates multiple timing plans and selects the one that minimizes a weighted combination of delay, stops, and emissions.

```python
from traffic_management import DynamicSignalOptimizer, OptimizationObjective

optimizer = DynamicSignalOptimizer(engine)

# Configure optimization parameters
optimizer.configure(
    objectives=[
        OptimizationObjective(name="total_delay", weight=0.50, target="minimize"),
        OptimizationObjective(name="total_stops", weight=0.20, target="minimize"),
        OptimizationObjective(name="emissions_kg", weight=0.15, target="minimize"),
        OptimizationObjective(name="pedestrian_wait", weight=0.10, target="minimize"),
        OptimizationObjective(name="transit_delay", weight=0.05, target="minimize"),
    ],
    constraints={
        "min_cycle_length_s": 60,
        "max_cycle_length_s": 150,
        "min_green_s": 10,
        "min_pedestrian_green_s": 7,
        "min_all_red_s": 2,
        "max_green_extensions_per_cycle": 2,
        "max_offset_shift_per_cycle_deg": 15,
    },
    optimization_horizon_min=5,
    convergence_target_pct=95
)

# Run real-time optimization for a network
result = optimizer.optimize_network(
    network_id="network-downtown",
    detectors_active=True,
    consider_upstream_conditions=True,
    account_for_queue_spillback=True
)

print(f"Optimization completed in {result.computation_time_ms:.0f}ms")
print(f"Network delay reduction: {result.delay_delta_pct:+.1f}%")
print(f"Network stops reduction: {result.stops_delta_pct:+.1f}%")
print(f"Intersections modified: {result.intersections_modified}/{result.total_intersections}")

for intersection in result.changes[:5]:
    print(f"\n  {intersection.name}:")
    print(f"    Cycle: {intersection.old_cycle_s:.0f}s -> {intersection.new_cycle_s:.0f}s")
    print(f"    Phases: {intersection.phases_modified} modified")
    print(f"    Expected delay improvement: {intersection.delay_delta_pct:+.1f}%")
```

#### Queue Length Estimation and Spillback Prevention

Accurate queue length estimation prevents spillback — where queues from one intersection extend back to the upstream intersection, causing gridlock. The system uses input-output models, shockwave theory, and detector occupancy data to estimate and predict queue lengths.

```python
from traffic_management import QueueEstimator, SpillbackPrevention

estimator = QueueEstimator(engine)

# Estimate queue lengths for a corridor
queues = estimator.estimate_corridor_queues(
    corridor_id="corridor-state-street",
    estimation_method="shockwave_theory",
    update_interval_s=30,
    include_turning_movements=True
)

for intersection in queues.intersections:
    print(f"\n{intersection.name}:")
    for movement in intersection.movements:
        status = "CRITICAL" if movement.queue_ratio > 0.85 else \
                 "WARNING" if movement.queue_ratio > 0.65 else "OK"
        print(f"  {movement.name}: queue={movement.queue_length_m:.0f}m "
              f"({movement.queue_ratio:.0%} of storage) [{status}]")

# Configure spillback prevention
prevention = SpillbackPrevention(engine)
prevention.configure(
    corridor_id="corridor-state-street",
    spillback_threshold_pct=0.85,
    action="truncate_green_and_extend_upstream",
    max_truncation_s=10,
    max_extension_s=15
)

# Monitor for spillback conditions
alerts = prevention.check_spillback()
for alert in alerts:
    print(f"SPILLBACK RISK: {alert.intersection} {alert.movement}")
    print(f"  Queue ratio: {alert.queue_ratio:.0%}, ETA to spillback: {alert.eta_seconds:.0f}s")
    prevention.activate_prevention(alert.intersection_id, alert.movement_id)
```

#### Multi-Modal Traffic Assignment

Models how traffic distributes across the network considering multiple transportation modes — private vehicles, transit, cycling, and walking. Uses mode choice models and traffic assignment algorithms to predict network-wide impacts of policy changes.

```python
from traffic_management import MultiModalAssignment, ModeChoiceModel

assignment = MultiModalAssignment(engine)

# Run four-step travel demand model
results = assignment.run_assignment(
    base_year=2024,
    forecast_year=2029,
    scenarios=[
        {
            "name": "baseline",
            "transit_fare_change_pct": 0,
            "parking_cost_change_pct": 0,
            "road_capacity_change_pct": 0,
            "cycling_infrastructure_km": 0
        },
        {
            "name": "transit_incentive",
            "transit_fare_change_pct": -25,
            "parking_cost_change_pct": 20,
            "road_capacity_change_pct": 0,
            "cycling_infrastructure_km": 0
        },
        {
            "name": "complete_streets",
            "transit_fare_change_pct": 0,
            "parking_cost_change_pct": 0,
            "road_capacity_change_pct": -5,
            "cycling_infrastructure_km": 50
        },
    ],
    network_file="network_2024.net",
    demand_matrix="od_matrix_2024",
    assignment_method="equilibrium",
    convergence_gap_pct=0.1
)

for scenario in results.scenarios:
    print(f"\nScenario: {scenario.name}")
    print(f"  Vehicle trips: {scenario.auto_trips:,} ({scenario.auto_trip_change_pct:+.1f}%)")
    print(f"  Transit trips: {scenario.transit_trips:,} ({scenario.transit_trip_change_pct:+.1f}%)")
    print(f"  Cycling trips: {scenario.bicycle_trips:,} ({scenario.bicycle_trip_change_pct:+.1f}%)")
    print(f"  Network VMT: {scenario.total_vmt:,.0f} ({scenario.vmt_change_pct:+.1f}%)")
    print(f"  Average speed: {scenario.avg_speed_kmh:.1f} km/h")
    print(f"  CO2 emissions: {scenario.co2_tons:.0f} tons/day")
```

### Incident Detection and Management

#### Advanced Video Analytics for Incident Detection

Computer vision algorithms analyze camera feeds in real-time to detect incidents — stopped vehicles, wrong-way drivers, pedestrians in roadway, debris, and weather-related hazards. The system reduces false alarms through multi-frame confirmation and contextual validation.

```python
from traffic_management import VideoAnalyticsDetector, IncidentType

detector = VideoAnalyticsDetector(engine)

# Configure detection rules
detector.configure_rules([
    {
        "type": IncidentType.STOPPED_VEHICLE,
        "min_duration_s": 5,
        "min_confidence": 0.80,
        "exclusion_zones": ["bus_stops", "parking_lanes"],
        "confirmation_cameras": 2
    },
    {
        "type": IncidentType.WRONG_WAY_DRIVER,
        "min_duration_s": 2,
        "min_confidence": 0.90,
        "immediate_alert": True,
        "dms_message": "WRONG WAY DRIVER AHEAD"
    },
    {
        "type": IncidentType.PEDESTRIAN_IN_ROADWAY,
        "min_duration_s": 3,
        "min_confidence": 0.75,
        "exclusion_zones": ["crosswalks", "marked_crossings"],
        "action": "flash_warning_light"
    },
    {
        "type": IncidentType.ROAD_DEBRIS,
        "min_duration_s": 10,
        "min_confidence": 0.70,
        "action": "dispatch_maintenance"
    },
    {
        "type": IncidentType.VEHICLE_ACCIDENT,
        "min_duration_s": 0,
        "min_confidence": 0.95,
        "immediate_alert": True,
        "dispatch_ems": True,
        "dms_message": "ACCIDENT AHEAD - USE ALTERNATE ROUTE"
    },
])

# Monitor video feeds
alerts = detector.scan_feeds(
    camera_group="highway_cameras",
    time_window_seconds=60,
    include_visual_evidence=True
)

for alert in alerts:
    print(f"INCIDENT DETECTED: {alert.type.value}")
    print(f"  Camera: {alert.camera_id}, Location: {alert.location}")
    print(f"  Confidence: {alert.confidence:.0%}, Duration: {alert.duration_s:.0f}s")
    print(f"  Evidence: {alert.evidence_url}")
```

#### Automated Incident Response Workflow

When an incident is detected, the system triggers a coordinated response — updating traffic signals, activating dynamic message signs, notifying first responders, and routing navigation apps around the incident.

```python
from traffic_management import IncidentResponseWorkflow, ResponseAction

workflow = IncidentResponseWorkflow(engine)

# Define response templates for different incident types
workflow.define_template(
    incident_type="vehicle_accident_major",
    severity="critical",
    actions=[
        ResponseAction(
            type="signal_preemption",
            target="nearest_3_intersections",
            params={"preempt_for": "emergency_vehicles", "duration_s": 300}
        ),
        ResponseAction(
            type="dms_update",
            targets=["dms_highway_eb_mile_5", "dms_highway_eb_mile_3"],
            messages=["ACCIDENT AHEAD - LEFT LANE BLOCKED", "EXPECT 15 MIN DELAY"]
        ),
        ResponseAction(
            type="reroute_suggestion",
            algorithm="dynamic_traffic_assignment",
            affected_routes=["route_101_north", "route_101_south"],
            alternative_routes=["route_280", "route_880"]
        ),
        ResponseAction(
            type="transit_diversion",
            routes_affected=["bus_38", "bus_42"],
            diversion_plan="incident_diversion_plan_A"
        ),
        ResponseAction(
            type="notify_stakeholders",
            recipients=["traffic_ops_center", "fire_dispatch", "ems_dispatch"],
            message_template="major_accident_dispatch"
        ),
    ],
    auto_execute=True,
    require_approval_for=["reroute_suggestion", "transit_diversion"]
)

# Execute response for a detected incident
result = workflow.execute(
    incident_id="inc-2024-0715-003",
    incident_type="vehicle_accident_major",
    location={"lat": 41.8781, "lon": -87.6298},
    severity="critical",
    lanes_blocked=2,
    total_lanes=4,
    injuries_reported=True
)

print(f"Response executed: {result.workflow_id}")
print(f"  Actions taken: {len(result.actions_executed)}")
for action in result.actions_executed:
    print(f"    {action.type}: {action.status}")
```

#### Incident Analytics and Trend Analysis

Post-incident analytics identify patterns, hotspots, and root causes to inform safety improvements and resource allocation. Tracks response times, clearance times, secondary incidents, and system performance.

```python
from traffic_management import IncidentAnalytics, TrendPeriod

analytics = IncidentAnalytics(engine)

# Analyze incident patterns for a corridor
patterns = analytics.analyze_patterns(
    corridor_id="corridor-highway-101",
    period="2024-annual",
    analysis_dimensions=["time_of_day", "day_of_week", "weather", "location", "vehicle_type"]
)

print("Incident Pattern Analysis - Highway 101:")
print(f"  Total incidents: {patterns.total_incidents:,}")
print(f"  Average per day: {patterns.avg_daily_incidents:.1f}")
print(f"  Peak hour: {patterns.peak_hour} ({patterns.peak_hour_incidents} incidents)")

print("\nTime of Day Distribution:")
for tod in patterns.time_of_day_distribution:
    bar = "#" * int(tod.count / patterns.peak_hour_incidents * 30)
    print(f"  {tod.hour:02d}:00: {bar} ({tod.count})")

print("\nWeather Correlation:")
for weather in patterns.weather_correlation:
    print(f"  {weather.condition}: {weather.count} incidents "
          f"({weather.percentage:.1f}%), avg severity: {weather.avg_severity:.1f}")

# Identify hotspots
hotspots = analytics.find_hotspots(
    min_incidents=10,
    radius_m=500,
    method="kernel_density",
    confidence_level=0.95
)
for hotspot in hotspots:
    print(f"\nHotspot: {hotspot.location_name}")
    print(f"  Incidents: {hotspot.count}, Density: {hotspot.density_per_km:.1f}/km")
    print(f"  Primary type: {hotspot.primary_type}")
    print(f"  Recommendation: {hotspot.safety_recommendation}")
```

### Congestion Management Strategies

#### Real-Time Congestion Pricing Optimization

Dynamic toll pricing adjusts prices based on real-time congestion levels, target speeds, and demand elasticity. Maximizes throughput while maintaining target operating speeds on managed lanes and congestion zones.

```python
from traffic_management import CongestionPricingEngine, PricingStrategy

pricing = CongestionPricingEngine(engine)

# Configure dynamic pricing
pricing.configure(
    strategy=PricingStrategy.TARGET_SPEED,
    managed_lanes=["express_lane_north", "express_lane_south"],
    target_speed_kmh=70,
    min_toll=0.50,
    max_toll=15.00,
    price_adjustment_interval_min=5,
    demand_elasticity=-0.3,
    revenue_target_daily=25000
)

# Get current pricing
current = pricing.get_current_prices()
for lane in current.lanes:
    print(f"{lane.name}: ${lane.current_toll:.2f}")
    print(f"  Speed: {lane.current_speed_kmh:.0f} km/h, Target: {lane.target_speed_kmh} km/h")
    print(f"  Volume: {lane.volume_vph}, Occupancy: {lane.occupancy_pct:.1f}%")

# Analyze pricing effectiveness
effectiveness = pricing.analyze_effectiveness(
    period="2024-Q2",
    metrics=["speed_compliance", "revenue", "equity_impact", "diversion"]
)
print(f"\nPricing Effectiveness (Q2 2024):")
print(f"  Target speed compliance: {effectiveness.speed_compliance_pct:.1f}%")
print(f"  Daily revenue avg: ${effectiveness.avg_daily_revenue:,.0f}")
print(f"  Revenue variance: ${effectiveness.revenue_std:,.0f}")
print(f"  Diversion to parallel routes: {effectiveness.diversion_pct:.1f}%")
print(f"  Equity impact score: {equity.equity_score:.2f}")
```

#### Dynamic Message Sign Network Management

Coordinates messaging across a network of dynamic message signs (DMS) to provide consistent, timely traveler information. Supports automated message selection based on incident type, location, and downstream conditions.

```python
from traffic_management import DMSManager, MessagePriority

dms = DMSManager(engine)

# Configure message library
dms.configure_messages([
    {
        "id": "incident_major",
        "template": "INCIDENT AHEAD - {location} - EXPECT {delay} MIN DELAY",
        "priority": MessagePriority.HIGH,
        "display_time_s": 30,
        "activate_flasher": True
    },
    {
        "id": "construction_zone",
        "template": "ROAD WORK AHEAD - {distance} - REDUCE SPEED TO {speed} MPH",
        "priority": MessagePriority.MEDIUM,
        "display_time_s": 60
    },
    {
        "id": "weather_advisory",
        "template": "WEATHER ADVISORY - {condition} - REDUCE SPEED AND INCREASE FOLLOWING DISTANCE",
        "priority": MessagePriority.HIGH,
        "display_time_s": 45,
        "activate_flasher": True
    },
    {
        "id": "event_traffic",
        "template": "{event_name} TONIGHT - EXPECT HEAVY TRAFFIC AFTER {event_end_time}",
        "priority": MessagePriority.LOW,
        "display_time_s": 60
    },
])

# Get DMS network status
status = dms.get_network_status()
print(f"DMS Network Status:")
print(f"  Total signs: {status.total_signs}")
print(f"  Online: {status.online_count}")
print(f"  Active messages: {status.active_message_count}")
print(f"  Average legibility: {status.avg_legibility_score:.1f}/100")

for sign in status.signs_with_issues:
    print(f"  ISSUE: {sign.id} - {sign.issue_type}: {sign.issue_description}")
```

### Transit Signal Priority and Integration

#### Conditional TSP with Schedule Adherence

Intelligent transit signal priority that considers real-time schedule adherence, passenger loads, and downstream conditions to make optimal priority decisions. Prevents "bunching" by holding late buses slightly and accelerating early ones.

```python
from traffic_management import SmartTransitPriority, PriorityDecision

smart_tsp = SmartTransitPriority(engine)

# Configure smart TSP
smart_tsp.configure(
    route_id="bus-route-42",
    mode="conditional_with_schedule_control",
    parameters={
        "max_early_departure_s": 60,
        "max_late_departure_s": 300,
        "priority_when_early": "reduce_priority",
        "priority_when_ontime": "standard_priority",
        "priority_when_late": "maximum_priority",
        "hold_at_terminal_if_early_s": 120,
        "passenger_load_weight": 0.3,
        "max_green_extension_s": 25,
        "max_red_truncation_s": 15,
        "min_headway_enforcement": True,
        "min_headway_s": 300,
    }
)

# Monitor TSP decisions in real-time
decisions = smart_tsp.get_recent_decisions(
    route_id="bus-route-42",
    count=10
)

for decision in decisions:
    print(f"Bus {decision.bus_id} at {decision.intersection_name}:")
    print(f"  Schedule: {decision.schedule_status} ({decision.deviation_s:+.0f}s)")
    print(f"  Passengers: {decision.passenger_count}")
    print(f"  Decision: {decision.priority_level} "
          f"(green +{decision.green_extension_s:.0f}s / red -{decision.red_truncation_s:.0f}s)")
    print(f"  Next bus gap: {decision.next_bus_gap_s:.0f}s")

# Get TSP effectiveness metrics
metrics = smart_tsp.get_effectiveness(
    route_id="bus-route-42",
    period_days=30
)
print(f"\nTSP Effectiveness (30 days):")
print(f"  Priority activations: {metrics.total_activations}")
print(f"  Average time saved: {metrics.avg_time_saved_s:.1f}s")
print(f"  On-time performance: {metrics.otp_pct:.1f}% (before: {metrics.otp_before_tsp:.1f}%)")
print(f"  Headway regularity: {metrics.headway_cv:.2f} CV (before: {metrics.headway_cv_before:.2f})")
```

#### Multimodal Level of Service Measurement

Measures how well the transportation network serves all users — drivers, transit riders, cyclists, pedestrians, and people with disabilities. Provides a balanced scorecard that goes beyond vehicle throughput.

```python
from traffic_management import MultimodalLOS, RoadUser

los = MultimodalLOS(engine)

# Measure LOS for a street segment
measurement = los.measure_segment(
    segment_id="segment-main-street-500",
    include_all_modes=True,
    time_period="weekday_peak",
    accessibility_audit=True
)

print(f"Multimodal LOS - Main Street Block 500:")
print(f"\n  Vehicle LOS: {measurement.vehicle_LOS} "
      f"(speed: {measurement.vehicle_speed_kmh:.0f} km/h, "
      f"volume/capacity: {measurement.vc_ratio:.2f})")
print(f"  Transit LOS: {measurement.transit_LOS} "
      f"(frequency: {measurement.transit_frequency_per_hour:.0f}/hr, "
      f"occupancy: {measurement.transit_occupancy_pct:.0f}%)")
print(f"  Bicycle LOS: {measurement.bicycle_LOS} "
      f"(facility: {measurement.bicycle_facility_type}, "
      f"stress_level: {measurement.bicycle_stress_level})")
print(f"  Pedestrian LOS: {measurement.pedestrian_LOS} "
      f"(sidewalk_width: {measurement.sidewalk_width_m:.1f}m, "
      f"crossing_time: {measurement.crossing_time_s:.0f}s)")
print(f"\n  Accessibility Score: {measurement.accessibility_score:.1f}/100")
print(f"  ADA compliance: {'PASS' if measurement.ada_compliant else 'FAIL'}")
if measurement.ada_issues:
    for issue in measurement.ada_issues:
        print(f"    - {issue}")
```

### Data-Driven Congestion Forecasting

#### Machine Learning Congestion Prediction

Uses historical traffic patterns, event calendars, weather forecasts, and special conditions to predict congestion levels 1-4 hours ahead. Enables proactive management rather than reactive response.

```python
from traffic_management import CongestionPredictor, PredictionModel

predictor = CongestionPredictor(engine)

# Train prediction model
model = predictor.train_model(
    model_type=PredictionModel.GRADIENT_BOOSTING,
    training_data="traffic_data_2022_2024",
    features=[
        "hour_of_day", "day_of_week", "month",
        "historical_speed_avg", "historical_speed_std",
        "weather_condition", "temperature_c",
        "is_holiday", "is_event_day", "event_type",
        "incident_count_recent_1h", "work_zone_active",
        "school_in_session", "major_employer_schedule"
    ],
    target="speed_ratio",
    validation_method="time_series_split",
    n_splits=5
)

print(f"Model performance:")
print(f"  RMSE: {model.rmse:.4f}")
print(f"  MAE: {model.mae:.4f}")
print(f"  R²: {model.r_squared:.4f}")
print(f"  MAPE: {model.mape:.1%}")

# Generate congestion forecast
forecast = predictor.forecast(
    network_id="network-metro",
    horizon_hours=4,
    update_interval_min=15,
    include_confidence_intervals=True
)

print(f"\nCongestion Forecast (next 4 hours):")
for hour_forecast in forecast.hourly:
    print(f"  {hour_forecast.time}: avg speed {hour_forecast.avg_speed_kmh:.0f} km/h "
          f"(CI: {hour_forecast.ci_lower:.0f}-{hour_forecast.ci_upper:.0f})")
    for zone in hour_forecast.hot_zones:
        print(f"    HOT ZONE: {zone.name} - predicted {zone.predicted_speed_kmh:.0f} km/h")
```

#### Travel Time Reliability Index

Measures the consistency of travel times across days and conditions. A reliable network has predictable travel times; an unreliable one has high variance. The Travel Time Index (TTI) and Planning Time Index (PTI) quantify this.

```python
from traffic_management import ReliabilityAnalyzer

reliability = ReliabilityAnalyzer(engine)

# Compute reliability metrics for key corridors
metrics = reliability.compute_corridor_reliability(
    corridors=["corridor-i5-north", "corridor-i-405", "corridor-state-route-99"],
    period="2024-Q2",
    time_periods=["am_peak", "pm_peak", "off_peak", "weekend"],
    percentiles=[50, 80, 95, 99]
)

for corridor in metrics:
    print(f"\n{corridor.name}:")
    for period in corridor.periods:
        print(f"  {period.name}:")
        print(f"    Average: {period.avg_travel_time_min:.1f} min")
        print(f"    TTI (95th/50th): {period.tti:.2f}")
        print(f"    PTI (95th/50th): {period.pti:.2f}")
        print(f"    Buffer time index: {period.buffer_index:.2f}")
        print(f"    On-time reliability: {period.on_time_pct:.1f}%")

# Identify reliability bottlenecks
bottlenecks = reliability.find_reliability_bottlenecks(
    min_tti=1.5,
    min_volume=500
)
for bn in bottlenecks:
    print(f"\nReliability bottleneck: {bn.location}")
    print(f"  TTI: {bn.tti:.2f}, PTI: {bn.pti:.2f}")
    print(f"  Primary cause: {bn.primary_cause}")
    print(f"  Recommendation: {bn.recommendation}")
```

### Connected Vehicle and V2X Integration

#### V2X Data Fusion for Enhanced Situational Awareness

Connected vehicle (CV) data provides high-resolution probe measurements — speed, position, heading, acceleration — directly from vehicles. Fusing CV data with infrastructure sensors dramatically improves traffic state estimation accuracy.

```python
from traffic_management import V2XDataFusion, ProbeDataConfig

fusion = V2XDataFusion(engine)

# Configure CV data processing
fusion.configure(
    probe_config=ProbeDataConfig(
        min_penetration_rate_pct=5,
        max_age_s=30,
        speed_smoothing_window_s=10,
        position_accuracy_m=5,
        heading_accuracy_deg=5,
        sample_method="weighted_by_recency"
    ),
    fusion_algorithm="extended_kalman_filter",
    update_interval_s=10,
    confidence_reporting=True
)

# Get enhanced traffic state using CV + infrastructure
state = fusion.get_enhanced_state(
    network_id="network-metro",
    include_cv_coverage=True,
    include_confidence=True
)

print(f"Enhanced Traffic State (CV + Infrastructure):")
print(f"  CV probe count: {state.cv_probe_count}")
print(f"  CV penetration rate: {state.cv_penetration_pct:.1f}%")
print(f"  Infrastructure sensor coverage: {state.infra_coverage_pct:.1f}%")
print(f"  Combined coverage: {state.combined_coverage_pct:.1f}%")

for link in state.links[:10]:
    print(f"\n  {link.name}:")
    print(f"    Speed: {link.speed_kmh:.0f} km/h (confidence: {link.confidence:.0%})")
    print(f"    Source: {link.primary_source}")
    print(f"    CV probes: {link.cv_probe_count}, Loop: {link.loop_occupancy:.1f}%")
```

#### Signal Phase and Timing (SPaT) Broadcasting

Broadcasts real-time signal phase and timing information to equipped vehicles, enabling speed advisory, green wave assistance, and red light violation warnings.

```python
from traffic_management import SPaTBroadcaster, SPaTMessage

broadcaster = SPaTBroadcaster(engine)

# Configure SPaT broadcasting
broadcaster.configure(
    intersections=[
        {"id": "int-001", "lat": 41.8781, "lon": -87.6298, "phases": 4},
        {"id": "int-002", "lat": 41.8785, "lon": -87.6295, "phases": 4},
        {"id": "int-003", "lat": 41.8789, "lon": -87.6292, "phases": 6},
    ],
    broadcast_interval_ms=100,
    include_time_to_change=True,
    include_advisory_speed=True,
    max_advisory_distance_m=500
)

# Monitor SPaT broadcast health
health = broadcaster.get_health()
print(f"SPaT Broadcasting Status:")
print(f"  Active intersections: {health.active_count}/{health.total_count}")
print(f"  Average broadcast rate: {health.avg_broadcast_rate_hz:.1f} Hz")
print(f"  Message queue depth: {health.queue_depth}")

# Get advisory for a specific approach
advisory = broadcaster.get_advisory(
    intersection_id="int-001",
    approach="northbound",
    vehicle_speed_kmh=50,
    distance_to_stop_bar_m=200
)
print(f"\nAdvisory for Northbound at int-001:")
print(f"  Current phase: {advisory.current_phase}")
print(f"  Time to green: {advisory.time_to_green_s:.1f}s")
print(f"  Time to red: {advisory.time_to_red_s:.1f}s")
print(f"  Recommended speed: {advisory.recommended_speed_kmh:.0f} km/h")
print(f"  Can make green: {advisory.can_make_green}")
```

### Work Zone and Special Event Management

#### Automated Work Zone Traffic Management

Manages traffic flow through and around work zones with automated lane control signs, speed management, and real-time condition monitoring.

```python
from traffic_management import WorkZoneManager, WZCondition

wz = WorkZoneManager(engine)

# Register a work zone
zone = wz.register_zone(
    zone_id="wz-highway-101-nb-mile-15",
    location={
        "route": "Highway 101 Northbound",
        "start_mile": 15.0,
        "end_mile": 17.5,
        "lanes_closed": 1,
        "lanes_total": 3,
        "speed_limit_mph": 45,
        "normal_speed_mph": 65
    },
    schedule={
        "start": "2024-07-15T21:00:00",
        "end": "2024-08-15T05:00:00",
        "active_hours": "21:00-05:00",
        "days": ["mon", "tue", "wed", "thu", "fri"]
    },
    monitoring={
        "queue_detection": True,
        "speed_monitoring": True,
        "wrong_way_detection": True,
        "incident_detection": True
    }
)

# Monitor work zone conditions
conditions = wz.monitor_zone(zone.zone_id)
print(f"Work Zone Status: {zone.zone_id}")
print(f"  Active: {conditions.is_active}")
print(f"  Queue length upstream: {conditions.queue_length_m:.0f}m")
print(f"  Average speed through zone: {conditions.avg_speed_mph:.0f} mph")
print(f"  Speed compliance: {conditions.speed_compliance_pct:.1f}%")
print(f"  Incidents today: {conditions.incidents_today}")
```

#### Special Event Traffic Management Plan

Coordinates traffic management for large events — concerts, sports games, festivals — with pre-event ingress, event-period, and post-event egress plans.

```python
from traffic_management import SpecialEventTraffic, EventPlan

event = SpecialEventTraffic(engine)

# Create event traffic management plan
plan = event.create_plan(
    event_name="NFL Championship Game",
    venue="Metropolitan Stadium",
    event_date="2024-02-11",
    expected_attendance=72_000,
    event_start="18:30",
    event_end="22:00",
    pre_event_hours=4,
    post_event_hours=2,
    special_conditions=["road_closures", "pedestrian_zones", "transit_service_increase"]
)

print(f"Event Traffic Plan: {plan.event_name}")
print(f"  Road closures: {len(plan.road_closures)}")
print(f"  Parking lots managed: {len(plan.parking_lots)}")
print(f"  Transit service changes: {len(plan.transit_changes)}")
print(f"  DMS messages: {len(plan.dms_messages)}")
print(f"  Officers deployed: {plan.officers_deployed}")

# Monitor event traffic in real-time
monitoring = event.monitor_event(plan.plan_id)
print(f"\nEvent Traffic Status:")
print(f"  Ingress: {monitoring.ingress_rate_vehicles_per_min:.0f} veh/min")
print(f"  Parking occupancy: {monitoring.parking_occupancy_pct:.1f}%")
print(f"  Transit ridership: {monitoring.transit_ridership:,}")
print(f"  Average wait time: {monitoring.avg_wait_min:.1f} min")
```

### Performance Measurement and Reporting

#### Automated Performance Reporting

Generates comprehensive traffic performance reports with trend analysis, peer benchmarking, and improvement recommendations. Supports federal, state, and local reporting requirements.

```python
from traffic_management import PerformanceReporter, ReportType

reporter = PerformanceReporter(engine)

# Generate monthly performance report
report = reporter.generate_report(
    report_type=ReportType.MONTHLY_PERFORMANCE,
    period="2024-07",
    network_id="network-metro",
    include_benchmarks=True,
    include_trends=True,
    include_recommendations=True
)

print(f"Monthly Performance Report - July 2024:")
print(f"\nKey Metrics:")
print(f"  Average travel time index: {report.tti_avg:.2f}")
print(f"  Average planning time index: {report.pti_avg:.2f}")
print(f"  Total incidents: {report.total_incidents:,}")
print(f"  Average incident clearance: {report.avg_clearance_min:.1f} min")
print(f"  Signal system uptime: {report.signal_uptime_pct:.1f}%")
print(f"  Sensor availability: {report.sensor_availability_pct:.1f}%")

print(f"\nTrend (vs. 12-month average):")
for metric in report.trends:
    direction = "improved" if metric.change < 0 and metric.lower_is_better else \
                "worsened" if metric.change > 0 and metric.lower_is_better else \
                "improved" if metric.change > 0 and not metric.lower_is_better else "worsened"
    print(f"  {metric.name}: {metric.current:.2f} ({metric.change:+.2f}) - {direction}")

print(f"\nRecommendations:")
for rec in report.recommendations:
    print(f"  [{rec.priority}] {rec.description}")
    print(f"    Expected impact: {rec.expected_impact}")
    print(f"    Implementation cost: {rec.estimated_cost}")
```

This extended reference provides comprehensive patterns for traffic flow optimization, incident management, congestion strategies, transit integration, connected vehicle technologies, work zone management, and performance measurement. Each section includes production-ready code examples adaptable to specific metropolitan contexts and requirements.

---
name: "public-safety"
category: "smart-cities"
version: "1.0.0"
tags: ["smart-cities", "public-safety", "emergency-response", "law-enforcement", "fire-safety"]
---

# Public Safety — Integrated Emergency Management Platform

## Overview

The Public Safety module provides a unified platform for emergency management, law enforcement analytics, fire prevention, disaster preparedness, and community safety operations. It integrates data from 911/PSAP (Public Safety Answering Point) computer-aided dispatch (CAD) systems, records management systems (RMS), video surveillance networks, gunshot detection, environmental sensors, and social media monitoring to provide situational awareness and operational coordination for public safety agencies.

This module supports the full emergency management lifecycle — prevention, mitigation, preparedness, response, and recovery — across all-hazards scenarios including natural disasters (floods, earthquakes, severe weather), man-made incidents (hazardous materials, active threats), and public health emergencies. It provides real-time common operating pictures (COP) for incident commanders, resource tracking and deployment optimization, and after-action analysis for continuous improvement.

The platform integrates with regional mutual aid systems (WebEOC, EMResource), federal alert systems (IPAWS, Wireless Emergency Alerts), hospital capacity tracking, and social services coordination to provide comprehensive emergency management capabilities from initial alert through long-term recovery.

## Core Capabilities

### 1. Computer-Aided Dispatch (CAD) Integration
Real-time interface with 911 CAD systems for call processing, unit assignment, and incident tracking. Supports priority-based dispatch, geocoded incident locations, cross-jurisdictional mutual aid, and automated unit recommendation based on incident type, location, and available resources.

### 2. Crime Analytics and Predictive Policing
Spatial-temporal crime pattern analysis, hotspot identification, and risk terrain modeling. Supports crime series identification, geographic profiling, and resource allocation optimization based on predicted crime demand. All predictive models must undergo bias auditing and fairness evaluation before deployment.

### 3. Video Surveillance and Analytics
Integration with citywide camera networks (traffic cameras, public safety cameras, private partner cameras) with real-time video analytics for anomaly detection, license plate recognition, crowd density estimation, and event detection. Supports operator-directed investigation and automated alerting.

### 4. Gunshot Detection and Acoustic Surveillance
Acoustic sensor network integration for real-time gunshot detection with geolocation, gunfire characteristic classification, and automated alerting to patrol units and dispatch. Provides post-incident acoustic evidence for investigations.

### 5. Fire Risk Assessment and Prevention
Building fire risk scoring based on construction type, occupancy, inspection history, fire protection systems, and proximity to fire stations. Supports pre-incident planning, target hazard identification, and community risk reduction programming.

### 6. Disaster Preparedness and Response
All-hazards emergency operations center (EOC) support with resource tracking, shelter management, evacuation routing, and damage assessment coordination. Integrates with weather services, geological surveys, and infrastructure monitoring for early warning.

### 7. Real-Time Crime Center (RTCC) Operations
Centralized intelligence hub that aggregates live data feeds — cameras, sensors, CAD, RMS, license plate readers, social media — into a unified tactical display for real-time decision support during active incidents and ongoing operations.

### 8. After-Action Analysis and Performance Metrics
Systematic review of incident response through timeline reconstruction, resource utilization analysis, outcome assessment, and lessons learned documentation. Tracks key performance indicators — response time, clearance rate, fire loss ratio, mutual aid utilization.

## Usage Examples

### Public Safety Engine Setup

```python
from public_safety import PublicSafetyEngine, AgencyConfig, IntegrationConfig

engine = PublicSafetyEngine(
    agency_id="metro-fire-police-001",
    agency_config=AgencyConfig(
        departments=["police", "fire", "ems", "emergency_management"],
        jurisdiction_population=2_500_000,
        coverage_area_sq_km=1_200,
        stations={"police": 45, "fire": 62, "ems": 28}
    ),
    integration_config=IntegrationConfig(
        cad_system="intergraph_cad",
        rms_system="mark43",
        video_platform="genetecSecurityCenter",
        gunshot_detection="shotspotter",
        weather_service="nws_api"
    )
)

engine.configure()
status = engine.get_status()
print(f"Active units: {status['units_online']}")
print(f"CAD connection: {status['cad_status']}")
print(f"Video feeds: {status['camera_feeds_active']}")
```

### CAD Integration and Dispatch

```python
from public_safety import CADInterface, PriorityLevel, UnitType

cad = CADInterface(engine)

# Process incoming 911 call
incident = cad.create_incident(
    call_type="structure_fire",
    priority=PriorityLevel.CRITICAL,
    location={"lat": 41.8781, "lon": -87.6298, "address": "123 N State St"},
    caller_info={"callback_number": "312-555-0100"},
    description="Smoke showing from 3-story commercial building"
)

# Get recommended unit assignments
assignments = cad.recommend_units(
    incident_id=incident.id,
    units_needed=[
        {"type": UnitType.FIRE_ENGINE, "quantity": 3},
        {"type": UnitType.FIRE_TRUCK, "quantity": 1},
        {"type": UnitType.AMBULANCE, "quantity": 2},
        {"type": UnitType.BATTALION_CHIEF, "quantity": 1},
    ],
    strategy="closest_valid",
    include_mutual_aid_if_needed=True
)

for assignment in assignments:
    print(f"{assignment.unit_id}: ETA {assignment.eta_seconds}s "
          f"from {assignment.station}")
```

### Crime Pattern Analysis

```python
from public_safety import CrimeAnalytics, PatternType, TimeWindow

analytics = CrimeAnalytics(engine)

# Detect crime series
series = analytics.detect_series(
    crime_types=["burglary", "auto_theft"],
    time_window=TimeWindow.LAST_90_DAYS,
    min_incidents=3,
    max_cluster_radius_m=2000,
    method="spatial_temporal_clustering"
)

for s in series:
    print(f"Pattern: {s.pattern_id}")
    print(f"  Type: {s.crime_type}")
    print(f"  Incidents: {len(s.incidents)}")
    print(f"  Area: {s.cluster_center}")
    print(f"  Time pattern: {s.temporal_pattern}")
    print(f"  Predicted next: {s.predicted_next_location}")

# Generate patrol recommendations
patrols = analytics.optimize_patrols(
    zone_id="district-south-03",
    time_period="next_24_hours",
    budget_units=8
)
```

### Video Surveillance Monitoring

```python
from public_safety import VideoManager, AlertType

video = VideoManager(engine)

# Configure analytics alerts
video.configure_alerts(
    zone_id="zone-downtown-core",
    alerts=[
        {"type": AlertType.CROWD_DENSITY, "threshold": "high", "action": "notify_rtcc"},
        {"type": AlertType.UNATTENDED_OBJECT, "sensitivity": "medium", "action": "dispatch_patrol"},
        {"type": AlertType.PERIMETER_BREACH, "sensitivity": "high", "action": "record_and_alert"},
    ]
)

# Get camera health status
cameras = video.get_camera_status(zone_id="zone-downtown-core")
online = sum(1 for c in cameras if c.status == "online")
print(f"Cameras online: {online}/{len(cameras)}")

# Review footage for an incident
footage = video.review_incident(
    incident_id="inc-2024-0715-001",
    camera_ids=["cam-main-001", "cam-main-002"],
    time_range_minutes=15
)
```

### Emergency Operations Center (EOC) Coordination

```python
from public_safety import EOCManager, IncidentLevel

eoc = EOCManager(engine)

# Activate EOC for severe weather event
activation = eoc.activate(
    event_type="severe_thunderstorm",
    level=IncidentLevel.LEVEL_2,
    activated_by="emergency_director",
    expected_duration_hours=8
)

print(f"EOC Activation: {activation.id}")
print(f"Level: {activation.level.name}")
print(f"Departments activated: {[d.name for d in activation.departments]}")

# Track resource status
resources = eoc.get_resource_status()
print(f"Shelters open: {resources.shelters_open}")
print(f"Shelter capacity: {resources.shelter_capacity:,}")
print(f"Evacuees registered: {resources.evacuees_registered:,}")
print(f"Mutual aid requests pending: {resources.mutual_aid_pending}")

# Update situation status
eoc.update_situation(
    activation_id=activation.id,
    summary="Tornado warning expired. 3 structures damaged. No injuries reported.",
    next_update_hours=2
)
```

### Fire Risk Assessment

```python
from public_safety import FireRiskAssessor, BuildingType

assessor = FireRiskAssessor(engine)

# Assess risk for a building
risk = assess.evaluate_building(
    building_id="bldg-commercial-4521",
    building_type=BuildingType.COMMERCIAL,
    floors=8,
    construction_type="Type_IA",
    occupancy_load=350,
    fire_protection=["sprinklered", "standpipe", "fire_alarm"],
    last_inspection_date="2024-03-15"
)

print(f"Fire risk score: {risk.risk_score:.1f}/100")
print(f"Risk category: {risk.risk_category}")
print(f"Key risk factors: {risk.key_factors}")
print(f"Recommended actions: {risk.recommendations}")

# Generate district-wide risk heatmap
heatmap = assess.generate_risk_heatmap(
    district_id="district-north-02",
    resolution_blocks=50,
    include_inspection_schedule=True
)
```

### Gunshot Detection Integration

```python
from public_safety import GunshotDetector, AlertPriority

detector = GunshotDetector(engine)

# Monitor for gunfire events
alerts = detector.get_recent_alerts(
    time_window_minutes=60,
    min_confidence=0.85
)

for alert in alerts:
    print(f"GUNFIRE DETECTED: {alert.timestamp}")
    print(f"  Location: {alert.location}")
    print(f"  Rounds detected: {alert.rounds_count}")
    print(f"  Confidence: {alert.confidence:.1%}")
    print(f"  Weapon type estimate: {alert.weapon_estimate}")

    # Dispatch response
    detector.dispatch_response(
        alert_id=alert.id,
        units=2,
        priority=AlertPriority.IMMEDIATE,
        include_trauma_alert=True
    )
```

## Best Practices

1. **Bias Auditing** — All predictive policing and risk scoring models must undergo regular bias audits across protected classes (race, ethnicity, income, geography). Publish fairness metrics and submit to independent review. Models that fail fairness thresholds must be suspended immediately.

2. **Data Retention Compliance** — Enforce strict retention schedules for all public safety data. CAD data: 5 years. Video footage: 30-90 days unless flagged for investigation. ShotSpotter alerts: 180 days. Gunshot audio: delete after event resolution.

3. **Mutual Aid Agreements** — Maintain current mutual aid agreements with neighboring jurisdictions. Test cross-jurisdictional coordination quarterly through tabletop exercises. Ensure CAD systems can exchange incident data with mutual aid partners.

4. **24/7 Redundancy** — CAD, radio, and 911 systems must have full redundancy with automatic failover. Maintain backup communication paths (satellite, HF radio) for when primary infrastructure fails. Test failover quarterly.

5. **Body-Worn Camera Policy** — All BWC footage must be managed according to department policy and state law. Implement automated activation triggers (gun drawn, Taser deployed, vehicle pursuit). Ensure footage is preserved for all use-of-force incidents and citizen complaints.

6. **De-escalation Integration** — CAD systems should flag mental health calls and suggest co-responder models (clinician + officer) where available. Dispatch protocols should reflect de-escalation-first policies for appropriate call types.

7. **Community Transparency** — Publish open data on response times, crime statistics, use of force, and complaint outcomes. Provide public dashboards that enable community oversight without compromising operational security or victim privacy.

8. **Interoperability Standards** — Use NIEM (National Information Exchange Model) for data exchange between agencies. Implement CAP (Common Alerting Protocol) for public warnings. Ensure radio interoperability through P25-compliant systems.

## Related Modules

- **urban-analytics** — Provides demographic, land use, and infrastructure data for risk modeling and resource allocation
- **traffic-management** — Coordinates traffic signal preemption for emergency vehicles and incident traffic management
- **energy-grid** — Shares outage data for disaster response and critical facility power restoration prioritization
- **citizen-services** — Enables community reporting, safety alerts, and victim services coordination

---

## Extended Reference Guide

### Surveillance Analytics and Video Intelligence

#### Multi-Camera Tracking and Re-Identification

Advanced video analytics that track individuals across multiple camera views using appearance-based re-identification. Supports investigative workflows while maintaining privacy through anonymization and strict access controls.

```python
from public_safety import MultiCameraTracker, ReIDConfig

tracker = MultiCameraTracker(engine)

# Configure re-identification system
tracker.configure(
    reid_config=ReIDConfig(
        appearance_model="osnet_ain_x1_0",
        feature_dim=512,
        matching_threshold=0.75,
        max_disappearance_frames=30,
        camera_coverage_map="camera_network_topology.json",
        anonymize_before_storage=True,
        retention_hours=72,
        access_log_all_queries=True
    ),
    privacy_settings={
        "blur_faces_in_live_view": True,
        "require_justification_for_tracking": True,
        "audit_all_reid_queries": True,
        "min_officer_rank_for_reid": "sergeant",
        "max_query_duration_hours": 4
    }
)

# Investigative tracking query (requires authorization)
tracking = tracker.investigate(
    incident_id="inc-2024-0715-003",
    start_time="2024-07-15T14:30:00",
    end_time="2024-07-15T15:00:00",
    seed_cameras=["cam-main-001", "cam-main-002"],
    authorized_by="sgt-smith",
    justification="Investigating vehicle theft suspect movement"
)

print(f"Investigative Tracking Results:")
print(f"  Subject tracked across {tracking.cameras_visited} cameras")
print(f"  Time span: {tracking.first_seen} to {tracking.last_seen}")
print(f"  Path reconstructed: {tracking.path_length_m:.0f}m")

for observation in tracking.observations:
    print(f"\n  Camera: {observation.camera_id} at {observation.timestamp}")
    print(f"    Confidence: {observation.reid_confidence:.0%}")
    print(f"    Actions: {observation.actions_detected}")
```

#### Crowd Density Estimation and Management

Real-time estimation of crowd density and flow patterns from video analytics. Supports event management, protest monitoring, and emergency evacuation planning.

```python
from public_safety import CrowdAnalyzer, DensityLevel

analyzer = CrowdAnalyzer(engine)

# Configure crowd density monitoring
analyzer.configure(
    estimation_method="density_map_regression",
    density_thresholds={
        DensityLevel.LOW: 0.5,
        DensityLevel.MODERATE: 1.5,
        DensityLevel.HIGH: 3.0,
        DensityLevel.DANGEROUS: 5.0,
        DensityLevel.CRITICAL: 7.0
    },
    person_per_square_meter_estimation=True,
    flow_direction_tracking=True,
    anomaly_detection=True,
    alert_on_threshold_escalation=True
)

# Monitor crowd at a public event
monitoring = analyzer.monitor_event(
    event_id="event-festival-2024-0715",
    venue="downtown-festival-grounds",
    camera_group="festival_cameras",
    real_time=True
)

print(f"Crowd Monitoring - Downtown Festival:")
print(f"  Current density: {monitoring.current_density:.1f} persons/sqm")
print(f"  Estimated crowd size: {monitoring.estimated_crowd_size:,}")
print(f"  Density level: {monitoring.density_level.name}")
print(f"  Flow direction: {monitoring.primary_flow_direction}")
print(f"  Bottlenecks detected: {len(monitoring.bottlenecks)}")

for bottleneck in monitoring.bottlenecks:
    print(f"\n  BOTTLENECK: {bottleneck.location}")
    print(f"    Density: {bottleneck.density:.1f} persons/sqm")
    print(f"    Risk level: {bottleneck.risk_level}")
    print(f"    Recommended action: {bottleneck.recommendation}")

# Historical crowd analysis
historical = analyzer.analyze_historical(
    event_id="event-festival-2024-0715",
    metrics=["peak_density", "flow_patterns", "bottleneck_frequency", "evacuation_time"]
)
print(f"\nHistorical Analysis:")
print(f"  Peak density: {historical.peak_density:.1f} persons/sqm at {historical.peak_time}")
print(f"  Average flow rate: {historical.avg_flow_rate:.0f} persons/min")
print(f"  Evacuation time estimate: {historical.evacuation_time_min:.0f} minutes")
```

#### Automated License Plate Recognition (ALPR) Analytics

ALPR system management with analytics for vehicle identification, stolen vehicle recovery, and investigative support. Includes strict privacy controls, data retention policies, and access auditing.

```python
from public_safety import ALPRManager, ALPRQuery

alpr = ALPRManager(engine)

# Configure ALPR system
alpr.configure(
    cameras=[
        {"id": "alpr-highway-01", "location": "I-95 Northbound Mile 5", "direction": "northbound"},
        {"id": "alpr-highway-02", "location": "I-95 Southbound Mile 5", "direction": "southbound"},
        {"id": "alpr-toll-01", "location": "Bridge Toll Plaza", "direction": "both"},
    ],
    hotlists=["stolen_vehicles", "missing_persons", "amber_alert", "bolo"],
    data_retention_days=180,
    anonymize_non_hits_after_days=30,
    require_justification_for_bulk_query=True
)

# Monitor ALPR alerts
alerts = alpr.get_recent_alerts(
    time_window_hours=24,
    hotlist=["stolen_vehicles", "amber_alert"]
)

for alert in alerts:
    print(f"ALPR HIT: {alert.hotlist_name}")
    print(f"  Plate: {alert.plate_hash}")
    print(f"  Camera: {alert.camera_id}")
    print(f"  Time: {alert.timestamp}")
    print(f"  Location: {alert.location}")
    print(f"  Vehicle description: {alert.vehicle_description}")
    print(f"  Confidence: {alert.recognition_confidence:.0%}")

    # Dispatch response
    alpr.dispatch_response(
        alert_id=alert.id,
        units=1,
        priority="high",
        notify_dispatch=True
    )

# Investigative ALPR query
query = alpr.investigate(
    plate_pattern="ABC-*123",
    time_range=("2024-07-01", "2024-07-15"),
    camera_area="highway_corridor",
    authorized_by="det-jones",
    case_number="CASE-2024-0715-003",
    justification="Vehicle matching suspect description in robbery case"
)

print(f"\nALPR Investigation Results:")
print(f"  Plates matched: {query.matches_found}")
for match in query.matches[:5]:
    print(f"  - {match.plate_hash}: {match.timestamp} at {match.camera_id}")
```

### Crime Prediction and Pattern Analysis

#### Risk Terrain Modeling (RTM)

Risk Terrain Modeling identifies environmental features that attract or generate crime, creating a risk surface that predicts where future crimes are most likely to occur. Unlike hotspot analysis (which shows where crime has been), RTM shows where conditions are conducive to crime.

```python
from public_safety import RiskTerrainModel, TerrainFeature

rtm = RiskTerrainModel(engine)

# Configure risk terrain features
features = [
    TerrainFeature(
        name="bars_and_nightclubs",
        source="osm_poi",
        buffer_m=200,
        risk_weight=1.8,
        category="nightlife"
    ),
    TerrainFeature(
        name="bus_stops",
        source="gtfs_stops",
        buffer_m=100,
        risk_weight=1.3,
        category="transit"
    ),
    TerrainFeature(
        name="vacant_lots",
        source="parcel_vacancy",
        buffer_m=150,
        risk_weight=2.1,
        category="blight"
    ),
    TerrainFeature(
        name="pawnshops",
        source="business_licenses",
        buffer_m=300,
        risk_weight=1.6,
        category="commercial"
    ),
    TerrainFeature(
        name="liquor_stores",
        source="abc_licenses",
        buffer_m=200,
        risk_weight=1.5,
        category="commercial"
    ),
    TerrainFeature(
        name="abandoned_buildings",
        source="code_violations",
        buffer_m=200,
        risk_weight=2.3,
        category="blight"
    ),
    TerrainFeature(
        name="street_intersections",
        source="osm_roads",
        buffer_m=50,
        risk_weight=1.2,
        category="infrastructure"
    ),
    TerrainFeature(
        name="parks_after_dark",
        source="parks_inventory",
        buffer_m=100,
        risk_weight=1.7,
        category="recreation",
        time_restriction="22:00-06:00"
    ),
]

# Build risk terrain model
model = rtm.build_model(
    crime_types=["robbery", "aggravated_assault"],
    training_period="2022-2024",
    resolution_m=100,
    features=features,
    validation_method="holdout",
    validation_period="2024-Q3"
)

print(f"Risk Terrain Model Performance:")
print(f"  Area under curve (AUC): {model.auc_roc:.3f}")
print(f"  Top decile capture rate: {model.top_decile_capture:.1%}")
print(f"  Most predictive feature: {model.top_feature.name} "
      f"(odds ratio: {model.top_feature.odds_ratio:.2f})")

# Generate risk terrain map
risk_map = model.generate_risk_map(
    forecast_period="2024-Q4",
    resolution_m=100,
    include_feature_contributions=True
)

# Identify highest risk cells
high_risk = risk_map.get_high_risk_cells(
    percentile=90,
    min_area_sq_km=0.01
)
print(f"\nHigh Risk Terrain Areas:")
for cell in high_risk[:10]:
    print(f"  Cell {cell.id}: risk_score={cell.risk_score:.2f}")
    print(f"    Top contributing features:")
    for feature in cell.top_features[:3]:
        print(f"      {feature.name}: {feature.contribution:.2f}")
```

#### Crime Series Identification and Link Analysis

Identifies connected crimes committed by the same offender(s) through spatial, temporal, and behavioral pattern matching. Supports serial crime investigations.

```python
from public_safety import CrimeSeriesAnalyzer, LinkageMethod

analyzer = CrimeSeriesAnalyzer(engine)

# Detect crime series
series = analyzer.detect_series(
    crime_types=["burglary", "robbery", "vehicle_theft"],
    time_window_months=6,
    spatial_threshold_m=1500,
    temporal_pattern=True,
    method=LinkageMethod.MULTI_FEATURE,
    features=["location", "time_of_day", "day_of_week", "modus_operandi", "victim_profile"]
)

print(f"Crime Series Detection Results:")
print(f"  Total incidents analyzed: {series.total_incidents:,}")
print(f"  Potential series identified: {series.series_count}")
print(f"  High-confidence series: {series.high_confidence_count}")

for s in series.detected_series:
    print(f"\nSeries: {s.series_id} (confidence: {s.confidence:.0%})")
    print(f"  Crime type: {s.primary_crime_type}")
    print(f"  Incidents: {len(s.incidents)}")
    print(f"  Date range: {s.first_incident_date} to {s.last_incident_date}")
    print(f"  Geographic cluster: {s.cluster_center}")
    print(f"  Radius: {s.cluster_radius_m:.0f}m")
    print(f"  Temporal pattern: {s.temporal_pattern_description}")
    print(f"  MO summary: {s.mo_summary}")
    print(f"  Predicted next location: {s.predicted_next_area}")
    print(f"  Predicted next time window: {s.predicted_next_window}")
```

#### Environmental Design (CPTED) Assessment

Crime Prevention Through Environmental Design analysis evaluates the built environment for crime-facilitating conditions — poor lighting, lack of natural surveillance, uncontrolled access, and territorial indicators.

```python
from public_safety import CPTEDAssessor, CPTEDPrinciple

assessor = CPTEDAssessor(engine)

# Assess CPTED conditions for a neighborhood
assessment = assessor.assess_area(
    area_id="neighborhood-east-village",
    principles=[
        CPTEDPrinciple.NATURAL_SURVEILLANCE,
        CPTEDPrinciple.NATURAL_ACCESS_CONTROL,
        CPTEDPrinciple.TERRITORIAL_REINFORCEMENT,
        CPTEDPrinciple.MAINTENANCE,
    ],
    data_sources=["street_imagery", "lidar", "osm", "parcel_data", "lighting_inventory"],
    resolution_m=50
)

print(f"CPTED Assessment - East Village:")
print(f"  Overall score: {assessment.overall_score:.1f}/100")

for principle in assessment.principle_scores:
    print(f"\n  {principle.name}: {principle.score:.1f}/100")
    print(f"    Strengths: {', '.join(principle.strengths)}")
    print(f"    Weaknesses: {', '.join(principle.weaknesses)}")
    for recommendation in principle.recommendations:
        print(f"    Recommendation: {recommendation.description}")
        print(f"      Estimated cost: {recommendation.estimated_cost}")
        print(f"      Expected impact: {recommendation.expected_crime_reduction}")

# Generate improvement priority map
priority_map = assessor.generate_improvement_map(
    area_id="neighborhood-east-village",
    budget=500_000,
    prioritization="crime_reduction_per_dollar"
)

print(f"\nCPTED Improvement Priorities:")
for i, project in enumerate(priority_map.projects[:5], 1):
    print(f"  {i}. {project.description}")
    print(f"     Cost: ${project.cost:,.0f}, "
          f"Crime reduction: {project.expected_reduction_pct:.1f}%, "
          f"ROI: {project.roi:.2f}")
```

### Emergency Response Coordination

#### Multi-Agency Incident Command System (ICS)

Digital incident command system that coordinates response across multiple agencies — police, fire, EMS, emergency management, public works, and mutual aid partners.

```python
from public_safety import IncidentCommandSystem, ICSRole

ics = IncidentCommandSystem(engine)

# Create multi-agency incident
incident = ics.create_incident(
    incident_type="hazmat_spill_major",
    severity="level_2",
    location={"lat": 41.8781, "lon": -87.6298, "description": "Highway 101 at Main Street"},
    initial_agencies=["fire_hazmat", "police_traffic", "ems", "environmental_protection"],
    incident_commander="bc-jones-fire",
    established_time="2024-07-15T14:30:00"
)

print(f"Incident Command Established: {incident.id}")
print(f"  Type: {incident.incident_type}")
print(f"  Incident Commander: {incident.commander_name}")
print(f"  Agencies involved: {len(incident.agencies)}")

# Assign ICS positions
positions = [
    {"role": ICSRole.SAFETY_OFFICER, "name": "Lt. Garcia", "agency": "fire_hazmat"},
    {"role": ICSRole.PUBLIC_INFORMATION, "name": "Sgt. Wilson", "agency": "police PIO"},
    {"role": ICSRole.LIAISON, "name": "M. Chen", "agency": "emergency_management"},
    {"role": ICSRole.OPERATIONS_BRANCH, "name": "Capt. Davis", "agency": "fire_hazmat"},
    {"role": ICSRole.PLANNING_SECTION, "name": "Sgt. Brown", "agency": "police"},
    {"role": ICSRole.LOGISTICS_SECTION, "name": "Dir. Thompson", "agency": "public_works"},
]

for pos in positions:
    ics.assign_position(incident.id, pos)

# Track resource deployment
resources = ics.get_resource_status(incident.id)
print(f"\nResource Status:")
print(f"  Personnel deployed: {resources.total_personnel}")
print(f"  Vehicles: {resources.total_vehicles}")
print(f"  Equipment: {resources.equipment_count}")

for unit in resources.units:
    print(f"  - {unit.unit_id}: {unit.type} ({unit.agency}) - {unit.status}")
```

#### Evacuation Planning and Execution

Manages evacuation planning, notification, transportation, and shelter operations for different hazard scenarios — chemical release, wildfire, flood, hurricane.

```python
from public_safety import EvacuationManager, EvacuationZone

evac = EvacuationManager(engine)

# Create evacuation plan
plan = evac.create_plan(
    incident_id="inc-2024-0715-005",
    hazard_type="hazmat_chlorine_release",
    affected_zones=[
        EvacuationZone(
            zone_id="zone-evac-1",
            name="Immediate (0.5 mile)",
            population=15000,
            priority="mandatory",
            notification_method="door_to_door"
        ),
        EvacuationZone(
            zone_id="zone-evac-2",
            name="Extended (1 mile)",
            population=35000,
            priority="voluntary",
            notification_method="wireless_emergency_alert"
        ),
    ],
    transportation={
        "bus_staging_areas": 3,
        "buses_available": 45,
        "special_needs_transport": 20,
        "pet_transport": True
    },
    shelters={
        "primary": "Metropolitan Convention Center",
        "capacity": 5000,
        "special_needs": "General Hospital Annex",
        "pet_friendly": "Community Center East"
    }
)

print(f"Evacuation Plan Created: {plan.id}")
print(f"  Zones: {len(plan.zones)}")
print(f"  Population affected: {plan.total_population:,}")
print(f"  Transportation capacity: {plan.bus_capacity} per hour")
print(f"  Shelter capacity: {plan.total_shelter_capacity:,}")

# Monitor evacuation progress
progress = evac.monitor_progress(plan.id)
print(f"\nEvacuation Progress:")
print(f"  Elapsed time: {progress.elapsed_minutes:.0f} minutes")
print(f"  Evacuated: {progress.evacuated_count:,}/{plan.total_population:,} "
      f"({progress.evacuation_pct:.1f}%)")
print(f"  Buses deployed: {progress.buses_deployed}")
print(f"  Bus trips completed: {progress.bus_trips_completed}")
print(f"  Shelter registrations: {progress.shelter_registrations}")

for zone in progress.zone_status:
    print(f"\n  Zone {zone.name}: {zone.evacuation_pct:.1f}% complete")
    print(f"    Remaining: {zone.remaining_count:,}")
    print(f"    Door-to-door status: {zone.door_to_door_pct:.1f}% contacted")
```

#### Mass Casualty Incident (MCI) Management

Coordinates multi-casualty incident response with triage, treatment, transport, and hospital coordination.

```python
from public_safety import MCICoordinator, TriageCategory

mci = MCICoordinator(engine)

# Activate MCI protocol
activation = mci.activate(
    incident_id="inc-2024-0715-006",
    incident_type="building_collapse",
    estimated_casualties=50,
    location={"lat": 41.8800, "lon": -87.6300}
)

print(f"MCI Protocol Activated: {activation.id}")
print(f"  Activation level: {activation.level}")
print(f"  Hospitals notified: {len(activation.hospitals_notified)}")

# Track triage operations
triage = mci.get_triage_status(activation.id)
print(f"\nTriage Status:")
print(f"  Total patients: {triage.total_patients}")
print(f"  Red (Immediate): {triage.red_count}")
print(f"  Yellow (Delayed): {triage.yellow_count}")
print(f"  Green (Minor): {triage.green_count}")
print(f"  Black (Deceased): {triage.black_count}")

# Hospital capacity coordination
hospitals = mci.get_hospital_status(activation.id)
print(f"\nHospital Coordination:")
for hospital in hospitals:
    print(f"  {hospital.name}:")
    print(f"    Beds available: {hospital.beds_available}")
    print(f"    Trauma bays: {hospital.trauma_bays_available}")
    print(f"    ETA from scene: {hospital.eta_minutes:.0f} min")
    print(f"    Patients assigned: {hospital.patients_assigned}")

# Transport coordination
transport = mci.get_transport_status(activation.id)
print(f"\nTransport Status:")
print(f"  Ambulances available: {transport.ambulances_available}")
print(f"  Patients transported: {transport.patients_transported}")
print(f"  Patients awaiting transport: {transport.patients_awaiting}")
print(f"  Average transport time: {transport.avg_transport_min:.0f} min")
```

### Community Safety and Prevention Programs

#### Community Violence Intervention (CVI) Analytics

Data-driven support for community violence intervention programs — identifying highest-risk individuals, connecting them with services, and measuring program effectiveness.

```python
from public_safety import CVIAnalytics, InterventionType

cvi = CVIAnalytics(engine)

# Configure CVI risk model
cvi.configure_risk_model(
    model_type="group_violence_intervention",
    features=[
        "recent_victimization",
        "gang_affiliation_indicator",
        "firearm_involvement",
        "prior_arrests",
        "age",
        "social_network_violence_exposure"
    ],
    fairness_constraints={
        "max_disparity_ratio": 1.2,
        "protected_classes": ["race", "ethnicity"],
        "review_frequency": "quarterly"
    }
)

# Identify highest-risk individuals for outreach
outreach_targets = cvi.identify_outreach_targets(
    neighborhood_id="neighborhood-south-side",
    risk_threshold_percentile=95,
    max_targets=50,
    exclude_recently_served_days=90
)

print(f"CVI Outreach Targets:")
print(f"  High-risk individuals identified: {len(outreach_targets)}")
for target in outreach_targets[:10]:
    print(f"\n  Target: {target.anonymized_id}")
    print(f"    Risk score: {target.risk_score:.1f}")
    print(f"    Risk factors: {', '.join(target.top_risk_factors[:3])}")
    print(f"    Recommended intervention: {target.recommended_intervention}")
    print(f"    Service referrals: {', '.join(target.service_referrals)}")

# Track program effectiveness
effectiveness = cvi.measure_effectiveness(
    program_id="cvi-south-side-2024",
    period_months=6,
    metrics=["violice_incidents", "hospitalizations", "arrests", "service_connection"]
)

print(f"\nCVI Program Effectiveness:")
print(f"  Participants served: {effectiveness.participants_served}")
print(f"  Violence incidents (participants): {effectiveness.incidents_pct_change:+.1f}%")
print(f"  Hospitalizations: {effectiveness.hospitalization_pct_change:+.1f}%")
print(f"  Service connections: {effectiveness.service_connections}")
print(f"  Cost per participant: ${effectiveness.cost_per_participant:,.0f}")
```

#### Neighborhood Watch and Community Reporting

Digital platform for community reporting of suspicious activity, neighborhood watch coordination, and community-police partnership.

```python
from public_safety import CommunityReporting, ReportType

reporting = CommunityReporting(engine)

# Configure community reporting platform
reporting.configure(
    anonymous_reporting_enabled=True,
    photo_video_upload=True,
    geolocation_required=False,
    auto_route_to_local precinct=True,
    response_time_target_hours=24,
    languages=["en", "es", "zh", "vi", "ar", "ko"]
)

# Process community report
report = reporting.submit_report(
    report_type=ReportType.SUSPICIOUS_ACTIVITY,
    description="Unfamiliar vehicle parked for 3+ hours, occupants appearing to surveil homes",
    location={"lat": 41.8800, "lon": -87.6300, "description": "Corner of Oak and Main"},
    photos=[],
    anonymous=True,
    reporter_contact=None
)

print(f"Community Report Filed: {report.id}")
print(f"  Type: {report.report_type}")
print(f"  Routed to: {report.assigned_precinct}")
print(f"  Assigned officer: {report.assigned_officer}")
print(f"  Expected response: {report.response_deadline}")

# Get community reporting analytics
analytics = reporting.get_analytics(
    precinct_id="precinct-south-01",
    period="2024-Q2"
)

print(f"\nCommunity Reporting Analytics (Q2):")
print(f"  Total reports: {analytics.total_reports}")
print(f"  Anonymous reports: {analytics.anonymous_pct:.1f}%")
print(f"  Average response time: {analytics.avg_response_hours:.1f} hours")
print(f"  Reports resolved: {analytics.resolved_pct:.1f}%")
print(f"  Community satisfaction: {analytics.satisfaction_pct:.1f}%")
```

### After-Action Analysis and Continuous Improvement

#### Automated After-Action Report Generation

Generates comprehensive after-action reports from incident data, CAD logs, radio communications, and resource tracking to identify lessons learned and improvement opportunities.

```python
from public_safety import AfterActionAnalyzer, ReportTemplate

aar = AfterActionAnalyzer(engine)

# Generate after-action report
report = aar.generate_report(
    incident_id="inc-2024-0715-006",
    template=ReportTemplate.MAJOR_INCIDENT,
    include_timeline=True,
    include_resource_analysis=True,
    include_communications_review=True,
    include_decision_points=True,
    include_stakeholder_input=True
)

print(f"After-Action Report: {report.incident_type}")
print(f"  Incident date: {report.incident_date}")
print(f"  Report generated: {report.generation_date}")
print(f"  Contributors: {report.contributors}")

print(f"\nTimeline Summary:")
for entry in report.timeline[:10]:
    print(f"  {entry.timestamp}: {entry.event}")
    print(f"    Agency: {entry.agency}, Decision: {entry.decision_maker}")

print(f"\nKey Findings:")
for finding in report.findings:
    print(f"  [{finding.severity.upper()}] {finding.description}")
    print(f"    Root cause: {finding.root_cause}")
    print(f"    Recommendation: {finding.recommendation}")
    print(f"    Responsible party: {finding.responsible_party}")
    print(f"    Due date: {finding.due_date}")

print(f"\nPerformance Metrics:")
for metric in report.performance_metrics:
    print(f"  {metric.name}: {metric.actual} (target: {metric.target}) "
          f"{'[MET]' if metric.met_target else '[NOT MET]'}")
```

#### Response Time Performance Analytics

Deep analysis of emergency response times from call receipt to on-scene arrival, identifying bottlenecks, improvement opportunities, and resource deployment optimization.

```python
from public_safety import ResponseTimeAnalyzer, ResponseMetric

analyzer = ResponseTimeAnalyzer(engine)

# Analyze response time performance
performance = analyzer.analyze(
    period="2024-Q2",
    agencies=["police", "fire", "ems"],
    metrics=[ResponseMetric.TOTAL_RESPONSE, ResponseMetric.TURNOUT, ResponseMetric.TURNAROUND],
    granularity="district"
)

print(f"Response Time Performance (Q2 2024):")
for agency in performance.agencies:
    print(f"\n{agency.name}:")
    print(f"  Average total response: {agency.avg_total_response_min:.1f} min")
    print(f"  90th percentile: {agency.p90_total_response_min:.1f} min")
    print(f"  On-time rate: {agency.on_time_pct:.1f}%")
    print(f"  Target: {agency.target_min:.1f} min")

    print(f"  Breakdown:")
    print(f"    Processing: {agency.avg_processing_min:.1f} min")
    print(f"    Turnout: {agency.avg_turnout_min:.1f} min")
    print(f"    Travel: {agency.avg_travel_min:.1f} min")

# Identify response time improvement opportunities
improvements = analyzer.identify_improvements(
    period="2024-Q2",
    target_on_time_pct=90,
    budget_constraint=500_000
)

print(f"\nResponse Time Improvement Opportunities:")
for opp in improvements:
    print(f"  {opp.description}")
    print(f"    Current: {opp.current_metric:.1f} min, Target: {opp.target_metric:.1f} min")
    print(f"    Estimated improvement: {opp.expected_improvement_pct:.1f}%")
    print(f"    Cost: ${opp.estimated_cost:,.0f}")
    print(f"    ROI: {opp.roi:.2f}")
```

This extended reference provides comprehensive patterns for surveillance analytics, crime prediction, emergency response coordination, community safety programs, and continuous improvement. Each section includes production-ready code examples with built-in privacy protections, bias auditing, and community transparency measures.

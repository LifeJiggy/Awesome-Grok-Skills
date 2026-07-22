---
name: "crisis-response"
category: "social-impact-tech"
version: "1.0.0"
tags: ["social-impact-tech", "crisis-response"]
---

# Crisis Response — Emergency Coordination & Disaster Relief Toolkit

## Overview

Crisis response technology saves lives by connecting people in danger with the resources they need, when they need them, under conditions where every minute matters. This module provides a Python toolkit for building emergency coordination systems — from real-time alert dispatch and disaster resource matching to shelter capacity tracking, volunteer deployment, and situational awareness dashboards. It is designed for use by emergency management agencies, community response teams, humanitarian organizations, and mutual aid networks operating in disaster scenarios.

The toolkit models the complete crisis lifecycle: pre-disaster preparedness (resource inventories, volunteer rosters, evacuation route planning), active incident response (real-time alerts, resource matching, dispatch coordination), and post-disaster recovery (damage assessment, long-term resource tracking, community resilience metrics). It supports multilingual communication workflows, low-bandwidth operation modes, and offline-first data synchronization for scenarios where network connectivity is disrupted.

Key architectural decisions prioritize reliability and graceful degradation over feature completeness. All critical data structures use optimistic concurrency with conflict resolution strategies suitable for intermittent connectivity. The resource matching engine operates on a multi-factor scoring algorithm that weighs proximity, urgency, resource type, and provider capacity to produce optimal dispatch recommendations. The alert system supports configurable severity levels, geographic targeting, and channel-specific formatting for SMS, push notifications, email, and social media.

The module includes built-in coordination protocols for multi-agency response, interoperable data formats compatible with emergency management standards (Common Alerting Protocol, Emergency Data Exchange Language), and audit trails for accountability. It is designed to integrate with existing infrastructure (GIS systems, weather APIs, government emergency databases) while remaining functional in standalone mode when external dependencies are unavailable.

## Core Capabilities

- **Real-Time Alert System**: Multi-channel emergency alert dispatch (SMS, push, email, social media) with geographic targeting, severity levels, multilingual templating, and delivery confirmation tracking.
- **Disaster Resource Matching**: Algorithm that connects relief resources (food, water, medical, shelter) with needs based on proximity, urgency, type, and availability with real-time inventory tracking.
- **Shelter Capacity Management**: Real-time tracking of shelter capacity, current occupancy, available services (medical, pets, ADA compliance), and overflow routing to secondary facilities.
- **Volunteer Dispatch & Coordination**: Skill-based volunteer assignment, shift scheduling, GPS-aware deployment, check-in/check-out tracking, and safety status monitoring.
- **Supply Chain Logistics**: Inventory management for relief supplies, warehouse tracking, distribution route planning, expiration date monitoring, and automated reorder triggers.
- **Situational Awareness Dashboard**: Consolidated view of incident status, resource deployment, affected population estimates, road conditions, and weather data integration.
- **Multilingual Communication**: Automated translation of alerts and instructions, interpreter resource matching, and culturally appropriate communication templates.
- **Post-Disaster Assessment**: Damage reporting, recovery progress tracking, community resilience scoring, and long-term resource need forecasting.
- **Evacuation Route Planning**: Dynamic evacuation route calculation based on road conditions, traffic, hazard zones, and population density with multi-modal transport options.
- **Casualty & Missing Person Tracking**: Unified registry for tracking casualties, hospitalizations, and missing persons with privacy controls and family reunification workflows.
- **Multi-Agency Coordination**: Interoperable data exchange between agencies, shared operational pictures, resource deconfliction, and communication bridges across organizations.
- **Financial Tracking & Donor Reporting**: Expense tracking, donation management, fund allocation transparency, and automated compliance reporting for disaster relief funding.

## Usage Examples

### Emergency Alert System

```python
from crisis_response import AlertSystem, AlertLevel, AlertChannel

alerts = AlertSystem()

# Send a flash flood warning
alert = alerts.create_alert(
    title="Flash Flood Warning",
    message="Flash flood warning in effect for Riverside County. Seek higher ground immediately.",
    level=AlertLevel.EXTREME,
    affected_area=(33.78, -117.85, 5.0),  # lat, lon, radius_km
    channels=[AlertChannel.SMS, AlertChannel.PUSH, AlertChannel.EMAIL],
    languages=["en", "es", "zh"],
    expires_hours=6,
)
print(f"Alert ID: {alert.alert_id}")
print(f"Est. recipients: {alerts.estimate_recipients(alert.affected_area)}")
```

### Resource Matching During Disaster

```python
from crisis_response import ResourcePool, ResourceType, UrgencyLevel

pool = ResourcePool()

pool.add_resource(
    resource_type=ResourceType.WATER,
    quantity=500,
    unit="bottles",
    location=(34.05, -118.25),
    provider_id="red_cross_001",
    expires_days=365,
)

pool.add_need(
    resource_type=ResourceType.WATER,
    quantity_needed=200,
    location=(34.05, -118.27),
    requester_id="shelter_042",
    urgency=UrgencyLevel.CRITICAL,
)

dispatches = pool.match_resources()
for d in dispatches:
    print(f"Dispatch: {d.quantity} {d.resource_type.value} → {d.requester_id} (distance: {d.distance_km:.1f}km)")
```

### Shelter Capacity Tracking

```python
from crisis_response import ShelterManager, Shelter

shelters = ShelterManager()

shelters.register_shelter(Shelter(
    shelter_id="shelter_001",
    name="Lincoln High School",
    location=(34.06, -118.24),
    max_capacity=200,
    services=["medical", "pets", "ADA"],
    contact_phone="555-0101",
))

shelters.check_in("shelter_001", "family_042", members=4)
shelters.check_in("shelter_001", "family_087", members=6)

status = shelters.get_status("shelter_001")
print(f"{status['name']}: {status['occupancy']}/{status['max_capacity']} ({status['utilization']:.0%})")
```

### Volunteer Deployment

```python
from crisis_response import VolunteerCoordinator, SkillType

coordinator = VolunteerCoordinator()

coordinator.register_volunteer("vol_001", name="Sarah M.", skills=[SkillType.FIRST_AID, SkillType.DRIVING])
coordinator.register_volunteer("vol_002", name="David K.", skills=[SkillType.HEAVY_LIFTING, SkillType.COORDINATION])
coordinator.register_volunteer("vol_003", name="Lin W.", skills=[SkillType.FIRST_AID, SkillType.TRANSLATION])

assignments = coordinator.dispatch(
    incident_id="incident_101",
    required_skills=[SkillType.FIRST_AID, SkillType.TRANSLATION],
    location=(34.05, -118.25),
    max_distance_km=15,
)

for a in assignments:
    print(f"Assigned: {a.volunteer_name} — {a.role} (ETA: {a.eta_minutes}min)")
```

### Situational Awareness Dashboard

```python
from crisis_response import SituationalDashboard, Incident

dashboard = SituationalDashboard()

dashboard.register_incident(Incident(
    incident_id="incident_101",
    name="Riverside Wildfire",
    severity="major",
    location=(34.05, -118.25),
    affected_population=12000,
    start_time="2026-06-15T14:30:00",
))

dashboard.update_situation(
    incident_id="incident_101",
    roads_closed=["Highway 60", "Main St"],
    evacuations_active=2,
    shelters_active=3,
    resources_deployed={"medical_teams": 4, "fire_units": 12, "transport_vehicles": 8},
)

status = dashboard.get_overview("incident_101")
print(f"Incident: {status['name']}")
print(f"Affected: {status['affected_population']:,} people")
print(f"Shelters: {status['shelters_active']} ({status['total_shelter_capacity']} capacity)")
print(f"Resources: {status['resources_deployed']}")
```

### Evacuation Route Planning

```python
from crisis_response import EvacuationPlanner

planner = EvacuationPlanner()

routes = planner.calculate_routes(
    origin=(34.05, -118.25),
    hazard_zone_radius_km=3.0,
    road_conditions={"Highway 60": "closed", "I-15": "congested"},
    population_density=5000,
    transport_modes=["car", "bus", "foot"],
)

for route in routes:
    print(f"Route: {route.mode} — {route.distance_km:.1f}km, {route.eta_minutes}min")
    print(f"  Capacity: {route.capacity} people/hour")
    print(f"  Risk level: {route.risk_level}")
```

### Supply Chain Tracking

```python
from crisis_response import SupplyChainManager

manager = SupplyChainManager()

# Add inventory
manager.add_stock("water_bottles", quantity=5000, warehouse="warehouse_01")
manager.add_stock("blankets", quantity=2000, warehouse="warehouse_01")
manager.add_stock("first_aid_kits", quantity=500, warehouse="warehouse_02")

# Create distribution request
distribution = manager.create_distribution(
    incident_id="incident_101",
    items=[
        {"item": "water_bottles", "quantity": 1000},
        {"item": "blankets", "quantity": 500},
        {"item": "first_aid_kits", "quantity": 100},
    ],
    destination=(34.06, -118.24),
    priority="urgent",
)

print(f"Distribution ID: {distribution.id}")
print(f"Route: {distribution.route}")
print(f"ETA: {distribution.eta_minutes}min")
print(f"Stock remaining after dispatch:")
for item, qty in manager.get_stock_levels().items():
    print(f"  {item}: {qty}")
```

## Best Practices

1. **Design for degraded connectivity first**: Crisis scenarios routinely involve network outages. Use offline-first data structures with sync-on-reconnect, local caching of critical maps and contact lists, and store-and-forward messaging patterns. Test your system on 2G connections and without internet access.

2. **Prioritize life-safety communications**: Alert system design must ensure the most critical messages (life-safety, evacuation) reach people through every available channel simultaneously. Redundancy in delivery pathways is not optional — it is the core requirement.

3. **Use plain language in all communications**: Crisis communications must be understood across literacy levels, languages, and cultural contexts. Avoid jargon, use short sentences, lead with the action people should take, and provide specific locations and times.

4. **Maintain resource inventory accuracy in real-time**: Stale inventory data can be worse than no data — it leads to dispatching resources that no longer exist. Implement optimistic concurrency, frequent reconciliation, and clear staleness indicators on all resource counts.

5. **Track volunteer safety as rigorously as civilian safety**: Every volunteer deployed into a disaster zone needs check-in/check-out tracking, safety status reporting, and automated alerts if they miss a scheduled check-in. Volunteer safety is non-negotiable.

6. **Implement conflict resolution for concurrent data**: When multiple operators update shelter capacity, resource counts, or dispatch assignments simultaneously, you need deterministic conflict resolution. Last-writer-wins is rarely correct — prefer field-level merge with audit trails.

7. **Test with realistic failure modes**: Run tabletop exercises and simulations that include network failures, power outages, staff rotation, and simultaneous multi-incident scenarios. The system that works perfectly in a demo often fails catastrophically under real crisis load.

8. **Respect data sovereignty and privacy**: Crisis response generates sensitive data (locations of vulnerable people, medical needs, immigration status). Implement strict access controls, data minimization, automatic expiration, and clear policies about data sharing with government agencies.

9. **Build interoperability from day one**: Emergency response involves multiple agencies (fire, police, medical, NGOs, government). Use standard data formats (CAP, EDXL) and APIs that enable data sharing without requiring all agencies to use the same platform.

10. **Plan for the recovery phase**: Most crisis tools focus on the acute response but neglect recovery. Build systems that transition smoothly from response to recovery — tracking long-term needs, housing placement, mental health referrals, and community rebuilding efforts.

## Related Modules

- [community-platforms](../community-platforms/GROK.md) — Community coordination and volunteer management
- [accessibility-tools](../accessibility-tools/GROK.md) — Accessible emergency alerts and communications
- [health-equity](../health-equity/GROK.md) — Health resource tracking during crises
- [education-access](../education-access/GROK.md) — Educational continuity during disasters

## Advanced Emergency Communication Patterns

### Multi-Channel Alert Distribution

Modern emergency alert systems must distribute messages across multiple channels simultaneously to ensure maximum reach. The toolkit supports SMS, push notifications, email, social media, and broadcast systems:

```python
from crisis_response import MultiChannelAlertSystem, AlertTemplate, ChannelPriority

# Configure multi-channel distribution
alert_system = MultiChannelAlertSystem(
    channels=[
        {"type": "sms", "priority": ChannelPriority.IMMEDIATE, "max_length": 160},
        {"type": "push", "priority": ChannelPriority.IMMEDIATE, "max_length": 500},
        {"type": "email", "priority": ChannelPriority.HIGH, "max_length": 5000},
        {"type": "social_media", "priority": ChannelPriority.MEDIUM, "max_length": 280},
        {"type": "broadcast", "priority": ChannelPriority.IMMEDIATE, "max_length": 1000}
    ],
    delivery_confirmation=True,
    retry_attempts=3,
    fallback_timeout_seconds=30
)

# Create alert with multilingual support
alert = alert_system.create_alert(
    title="Flash Flood Warning",
    message="Flash flood warning in effect for Riverside County. Seek higher ground immediately.",
    level="EXTREME",
    affected_area=(33.78, -117.85, 5.0),
    languages=["en", "es", "zh", "vi", "ko"],
    expiration_hours=6,
    sender_id="RIVERSIDE_EMA"
)

# Distribute across all channels
distribution = alert_system.distribute(alert)
print(f"Alert distributed:")
print(f"  SMS sent: {distribution.sms_sent}")
print(f"  Push notifications: {distribution.push_sent}")
print(f"  Emails: {distribution.email_sent}")
print(f"  Social media posts: {distribution.social_posts}")
print(f"  Broadcast alerts: {distribution.broadcast_sent}")
print(f"  Total recipients: {distribution.total_recipients}")
print(f"  Delivery rate: {distribution.delivery_rate:.1%}")
```

### Real-Time Situational Awareness Dashboard

```python
from crisis_response import SituationalAwarenessDashboard, IncidentLayer, DataFeed

# Create comprehensive dashboard
dashboard = SituationalAwarenessDashboard(
    update_interval_seconds=30,
    data_retention_hours=72
)

# Add incident layers
dashboard.add_layer(IncidentLayer(
    name="Active Incidents",
    data_source="incident_database",
    refresh_rate=60,
    color_coding={"critical": "#FF0000", "major": "#FF8C00", "moderate": "#FFD700"}
))

dashboard.add_layer(IncidentLayer(
    name="Road Conditions",
    data_source="traffic_api",
    refresh_rate=300,
    color_coding={"closed": "#FF0000", "congested": "#FF8C00", "clear": "#00FF00"}
))

dashboard.add_layer(IncidentLayer(
    name="Shelter Status",
    data_source="shelter_database",
    refresh_rate=120,
    show_capacity=True
))

# Add data feeds
dashboard.add_feed(DataFeed(
    name="Weather Service",
    source="NWS_API",
    update_interval=300,
    alert_on={"severe_weather": True, "flood_warning": True}
))

dashboard.add_feed(DataFeed(
    name="Social Media Monitor",
    source="twitter_api",
    keywords=["emergency", "evacuation", "help"],
    sentiment_analysis=True
))

# Get consolidated view
situation = dashboard.get_current_situation()
print(f"Current Situation:")
print(f"  Active incidents: {situation.active_incidents}")
print(f"  Affected population: {situation.affected_population:,}")
print(f"  Shelters open: {situation.shelters_open}/{situation.shelters_total}")
print(f"  Roads closed: {situation.roads_closed}")
print(f"  Weather alerts: {situation.weather_alerts}")
```

### Volunteer Dispatch and Safety Tracking

```python
from crisis_response import VolunteerDispatchSystem, SafetyTracker, CheckInProtocol

# Configure volunteer dispatch
dispatch = VolunteerDispatchSystem(
    safety_protocols=CheckInProtocol(
        check_in_interval_minutes=30,
        missed_check_in_threshold=2,
        emergency_contact_required=True,
        gps_tracking_enabled=True
    ),
    skill_matching_algorithm="weighted",
    max_deployment_hours=12
)

# Register volunteers with skills and availability
volunteers = [
    {
        "id": "vol_001",
        "name": "Sarah M.",
        "skills": ["first_aid", "driving", "heavy_lifting"],
        "availability": "immediate",
        "max_hours": 8,
        "emergency_contact": "555-0101",
        "vehicle": "SUV"
    },
    {
        "id": "vol_002",
        "name": "David K.",
        "skills": ["first_aid", "cpr", "medical"],
        "availability": "immediate",
        "max_hours": 12,
        "emergency_contact": "555-0102",
        "vehicle": None
    }
]

for vol in volunteers:
    dispatch.register_volunteer(vol)

# Dispatch volunteers to incident
assignments = dispatch.dispatch(
    incident_id="incident_101",
    required_skills=["first_aid", "driving"],
    location=(34.05, -118.25),
    max_distance_km=15,
    priority="critical"
)

print(f"Volunteer Dispatch:")
for assignment in assignments:
    print(f"  {assignment.volunteer_name}: {assignment.role}")
    print(f"    Skills matched: {assignment.skills_matched}")
    print(f"    ETA: {assignment.eta_minutes} minutes")
    print(f"    Deployment hours: {assignment.deployment_hours}")

# Track volunteer safety
safety = SafetyTracker()
for assignment in assignments:
    safety.start_tracking(assignment.volunteer_id, incident_id="incident_101")
    status = safety.get_status(assignment.volunteer_id)
    print(f"    Safety status: {status.current_status}")
```

### Evacuation Route Optimization

```python
from crisis_response import EvacuationRouteOptimizer, PopulationEvacuation, RoadCondition

# Configure evacuation optimizer
optimizer = EvacuationRouteOptimizer(
    population_density_data=True,
    traffic_models=True,
    multi_modal_transport=True,
    accessibility_accommodations=True
)

# Define evacuation zone
evacuation = PopulationEvacuation(
    zone_center=(34.05, -118.25),
    zone_radius_km=5.0,
    population_estimate=12000,
    special_needs_population=1500,
    vehicles_available=8000,
    public_transport_capacity=2000
)

# Add road conditions
road_conditions = [
    RoadCondition("Highway 60", "closed", "flooding"),
    RoadCondition("I-15", "congested", "evacuation_traffic"),
    RoadCondition("Main St", "open", None),
    RoadCondition("Elm Ave", "open", None)
]

for road in road_conditions:
    optimizer.update_road_condition(road)

# Calculate optimal routes
routes = optimizer.optimize_evacuation(
    evacuation=evacuation,
    evacuation_time_target_hours=4,
    prioritize_vulnerable=True
)

print(f"Evacuation Plan:")
print(f"  Total population: {routes.total_population:,}")
print(f"  Evacuation time: {routes.estimated_time_hours:.1f} hours")
print(f"  Routes calculated: {len(routes.routes)}")

for route in routes.routes[:5]:
    print(f"\n  Route: {route.name}")
    print(f"    Mode: {route.transport_mode}")
    print(f"    Capacity: {route.capacity_per_hour} people/hour")
    print(f"    Distance: {route.distance_km:.1f} km")
    print(f"    Risk level: {route.risk_level}")
    print(f"    Accessibility: {route.accessibility_features}")
```

### Supply Chain and Resource Logistics

```python
from crisis_response import SupplyChainOptimizer, Warehouse, DistributionRoute

# Configure supply chain
supply_chain = SupplyChainOptimizer(
    warehouse_count=5,
    distribution_centers=3,
    vehicle_fleet_size=50,
    optimization_algorithm="linear_programming"
)

# Add warehouses
warehouses = [
    Warehouse(
        id="wh_001",
        location=(34.05, -118.25),
        capacity=10000,
        current_stock={
            "water_bottles": 5000,
            "blankets": 2000,
            "first_aid_kits": 500,
            "food_boxes": 3000
        },
        operating_hours="24/7"
    ),
    Warehouse(
        id="wh_002",
        location=(34.10, -118.30),
        capacity=8000,
        current_stock={
            "water_bottles": 3000,
            "blankets": 1500,
            "first_aid_kits": 300,
            "food_boxes": 2000
        },
        operating_hours="24/7"
    )
]

for wh in warehouses:
    supply_chain.add_warehouse(wh)

# Create distribution request
request = supply_chain.create_request(
    incident_id="incident_101",
    destination=(34.06, -118.24),
    items=[
        {"item": "water_bottles", "quantity": 1000, "priority": "critical"},
        {"item": "blankets", "quantity": 500, "priority": "high"},
        {"item": "first_aid_kits", "quantity": 100, "priority": "critical"},
        {"item": "food_boxes", "quantity": 800, "priority": "high"}
    ],
    delivery_deadline_hours=4
)

# Optimize distribution
distribution = supply_chain.optimize_distribution(request)
print(f"Distribution Plan:")
print(f"  Warehouse: {distribution.warehouse_id}")
print(f"  Route: {distribution.route_name}")
print(f"  ETA: {distribution.eta_minutes} minutes")
print(f"  Vehicle: {distribution.vehicle_type}")
print(f"  Cost: ${distribution.estimated_cost:.2f}")

# Track delivery
tracking = supply_chain.track_delivery(distribution.delivery_id)
print(f"\nDelivery Status:")
print(f"  Current status: {tracking.status}")
print(f"  Progress: {tracking.progress_percentage:.0%}")
print(f"  Last update: {tracking.last_update}")
```

### Multilingual Emergency Communications

```python
from crisis_response import MultilingualAlertSystem, TranslationService, CulturalAdaptation

# Configure multilingual alert system
multilingual = MultilingualAlertSystem(
    supported_languages=["en", "es", "zh", "vi", "ko", "ar", "tl", "hi"],
    default_language="en",
    translation_service=TranslationService.DEEP_L,
    cultural_adaptation=True,
    literacy_levels=["standard", "simplified"]
)

# Create alert with cultural adaptation
alert = multilingual.create_alert(
    title="Wildfire Evacuation Order",
    message="Mandatory evacuation in effect for Zone 3. Evacuate immediately via Highway 60 North.",
    level="EXTREME",
    affected_area=(34.05, -118.25, 3.0),
    target_languages=["en", "es", "zh", "vi"],
    cultural_notes={
        "chinese": "Include reference to community gathering points",
        "vietnamese": "Emphasize family reunification information"
    }
)

# Translate and adapt
translations = multilingual.translate_alert(alert)
print(f"Multilingual Alert:")
for lang, translation in translations.items():
    print(f"\n  {lang}:")
    print(f"    Title: {translation.title}")
    print(f"    Message preview: {translation.message[:100]}...")
    print(f"    Translation quality: {translation.quality_score:.2f}")
    print(f"    Cultural adaptation: {translation.cultural_adaptation_applied}")
```

### Post-Disaster Assessment and Recovery

```python
from crisis_response import PostDisasterAssessment, RecoveryTracker, ResilienceScoring

# Configure assessment system
assessment = PostDisasterAssessment(
    damage_categories=["structural", "infrastructure", "environmental", "social"],
    assessment_criteria={
        "structural": ["buildings", "roads", "bridges", "utilities"],
        "infrastructure": ["power", "water", "communications", "transportation"],
        "environmental": ["air_quality", "water_quality", "soil_contamination"],
        "social": ["displacement", "health_impacts", "economic_damage"]
    }
)

# Conduct assessment
assessment_result = assessment.conduct_assessment(
    incident_id="incident_101",
    assessment_area=(34.05, -118.25, 5.0),
    assessor_id="team_001",
    assessment_date="2026-06-16"
)

print(f"Post-Disaster Assessment:")
print(f"  Total damage score: {assessment_result.total_damage_score:.1f}/100")
print(f"  Structural damage: {assessment_result.structural_damage:.1f}%")
print(f"  Infrastructure damage: {assessment_result.infrastructure_damage:.1f}%")
print(f"  Displaced population: {assessment_result.displaced_population:,}")
print(f"  Estimated recovery time: {assessment_result.estimated_recovery_weeks} weeks")

# Track recovery progress
recovery = RecoveryTracker()
recovery.start_tracking(
    incident_id="incident_101",
    baseline_assessment=assessment_result,
    recovery_targets={
        "power_restoration_days": 7,
        "water_restoration_days": 5,
        "shelter_placement_days": 14,
        "full_recovery_weeks": 24
    }
)

# Get recovery progress
progress = recovery.get_progress("incident_101")
print(f"\nRecovery Progress:")
print(f"  Power restored: {progress.power_restoration:.0%}")
print(f"  Water restored: {progress.water_restoration:.0%}")
print(f"  Shelters placed: {progress.shelter_placement:.0%}")
print(f"  Overall recovery: {progress.overall_recovery:.0%}")

# Calculate resilience score
resilience = ResilienceScoring()
score = resilience.calculate_score(
    pre_disaster_baseline=assessment_result.pre_disaster_baseline,
    post_disaster_assessment=assessment_result,
    recovery_progress=progress
)
print(f"\nCommunity Resilience Score: {score.overall_score:.1f}/100")
print(f"  Social resilience: {score.social_resilience:.1f}")
print(f"  Infrastructure resilience: {score.infrastructure_resilience:.1f}")
print(f"  Economic resilience: {score.economic_resilience:.1f}")
```

### Interoperability and Standards Compliance

```python
from crisis_response import InteroperabilityManager, CAPAdapter, EDXLConverter

# Configure interoperability
interop = InteroperabilityManager(
    standards=["CAP_1.2", "EDXL_DE_2.0", "NIEM_5.0"],
    data_formats=["XML", "JSON", "GeoJSON"],
    api_protocols=["REST", "SOAP", "WebSocket"]
)

# Convert alert to CAP format
cap_adapter = CAPAdapter()
cap_message = cap_adapter.to_cap(
    alert_id="alert_001",
    sender="RIVERSIDE_EMA",
    sent="2026-06-15T14:30:00-07:00",
    status="Actual",
    msg_type="Alert",
    scope="Public",
    code=["IPAWSv1.0"],
    area="Riverside County",
    polygon="33.78,-117.85 33.80,-117.80 33.76,-117.80",
    event="Flash Flood Warning",
    urgency="Immediate",
    severity="Extreme",
    certainty="Observed"
)

print(f"CAP Message Generated:")
print(f"  Format: {cap_message.format}")
print(f"  Size: {cap_message.size_bytes} bytes")
print(f"  Valid: {cap_message.is_valid}")

# Convert to EDXL for distribution
edxl_converter = EDXLConverter()
edxl_message = edxl_converter.to_edxl(
    cap_message=cap_message,
    distribution_list=["FEMA", "STATE_EMA", "COUNTY_EMA", "HOSPITALS"]
)

print(f"\nEDXL Message:")
print(f"  Recipients: {len(edxl_message.distribution_list)}")
print(f"  Distribution type: {edxl_message.distribution_type}")
print(f"  Confidentiality: {edxl_message.confidentiality_level}")
```

### Financial Tracking and Donor Reporting

```python
from crisis_response import FinancialTracker, DonorManagement, ComplianceReporting

# Configure financial tracking
financial = FinancialTracker(
    fund_categories=["emergency_response", "recovery", "rebuilding"],
    cost_centers=True,
    audit_trail=True,
    real_time_reporting=True
)

# Track expenses
expense1 = financial.record_expense(
    incident_id="incident_101",
    category="emergency_response",
    description="Emergency shelter setup",
    amount=15000.00,
    vendor="Community Center",
    receipt_required=True,
    approved_by="director_001"
)

expense2 = financial.record_expense(
    incident_id="incident_101",
    category="emergency_response",
    description="Food and water distribution",
    amount=8500.00,
    vendor="Local Suppliers",
    receipt_required=True,
    approved_by="director_001"
)

# Get expense summary
summary = financial.get_expense_summary("incident_101")
print(f"Expense Summary:")
print(f"  Total expenses: ${summary.total_expenses:,.2f}")
print(f"  By category:")
for category, amount in summary.by_category.items():
    print(f"    {category}: ${amount:,.2f}")

# Generate donor report
donor_mgmt = DonorManagement()
report = donor_mgmt.generate_report(
    incident_id="incident_101",
    donor_id="donor_001",
    include_items=True,
    include_photos=True,
    include_outcomes=True
)

print(f"\nDonor Report:")
print(f"  Donor: {report.donor_name}")
print(f"  Contribution: ${report.contribution_amount:,.2f}")
print(f"  Items purchased: {len(report.items_purchased)}")
print(f"  People served: {report.people_served:,}")
print(f"  Outcomes: {report.outcomes_summary}")
```

### Crisis Communication Templates

```python
from crisis_response import CommunicationTemplateManager, TemplateCategory

# Configure template manager
template_manager = CommunicationTemplateManager(
    categories=[
        TemplateCategory.EVACUATION,
        TemplateCategory.SHELTER,
        TemplateCategory.HEALTH,
        TemplateCategory.RECOVERY
    ],
    multilingual=True,
    accessibility_compliant=True
)

# Create evacuation template
evacuation_template = template_manager.create_template(
    name="Standard Evacuation Order",
    category=TemplateCategory.EVACUATION,
    subject="EVACUATION ORDER: {{zone_name}}",
    body="""
    IMMEDIATE EVACUATION ORDER
    
    Zone: {{zone_name}}
    Reason: {{reason}}
    Evacuation Route: {{route}}
    Shelter Location: {{shelter_location}}
    Emergency Contact: {{emergency_contact}}
    
    {{cultural_notes}}
    
    For assistance: {{assistance_phone}}
    """,
    variables=["zone_name", "reason", "route", "shelter_location", "emergency_contact", "cultural_notes", "assistance_phone"],
    languages=["en", "es", "zh", "vi"]
)

# Use template to create alert
alert = template_manager.use_template(
    template_id=evacuation_template.id,
    variables={
        "zone_name": "Zone 3 - Riverside",
        "reason": "Wildfire approaching",
        "route": "Highway 60 North",
        "shelter_location": "Lincoln High School",
        "emergency_contact": "911",
        "cultural_notes": "Chinese community: gather at parking lot A",
        "assistance_phone": "555-HELP"
    },
    target_languages=["en", "es", "zh"]
)

print(f"Alert Created from Template:")
print(f"  Subject: {alert.subject}")
print(f"  Languages: {list(alert.translations.keys())}")
print(f"  Accessibility: {alert.accessibility_compliant}")
```

### Real-Time Monitoring and Alerting

```python
from crisis_response import RealTimeMonitor, AlertEngine, ThresholdConfig

# Configure real-time monitoring
monitor = RealTimeMonitor(
    data_sources=[
        "weather_service",
        "traffic_sensors",
        "social_media",
        "911_calls",
        "shelter_capacity"
    ],
    update_interval_seconds=10,
    alert_engine=AlertEngine(
        thresholds=ThresholdConfig(
            critical={"shelter_capacity": 0.9, "road_closures": 5},
            warning={"shelter_capacity": 0.7, "road_closures": 3},
            info={"shelter_capacity": 0.5, "road_closures": 1}
        )
    )
)

# Start monitoring
monitor.start()

# Get current status
status = monitor.get_current_status()
print(f"Real-Time Status:")
print(f"  Weather: {status.weather_condition}")
print(f"  Traffic: {status.traffic_status}")
print(f"  Social media sentiment: {status.social_sentiment}")
print(f"  911 call volume: {status.call_volume}")
print(f"  Shelter capacity: {status.shelter_capacity:.0%}")

# Check for alerts
alerts = monitor.get_active_alerts()
print(f"\nActive Alerts:")
for alert in alerts:
    print(f"  [{alert.level}] {alert.title}")
    print(f"    Source: {alert.source}")
    print(f"    Time: {alert.timestamp}")
    print(f"    Affected area: {alert.affected_area}")
```

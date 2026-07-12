"""
Public Safety Module — Integrated Emergency Management Platform

Provides unified emergency management, law enforcement analytics, fire
prevention, disaster preparedness, and community safety operations. Integrates
CAD, RMS, video surveillance, gunshot detection, and environmental sensors.

Domain: Smart Cities > Public Safety
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EngineStatus(Enum):
    """Operational state of the public safety engine."""
    UNINITIALIZED = auto()
    CONFIGURING = auto()
    READY = auto()
    RUNNING = auto()
    ERROR = auto()
    SHUTDOWN = auto()


class PriorityLevel(Enum):
    """Incident and dispatch priority levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class UnitType(Enum):
    """Emergency service unit types."""
    POLICE_PATROL = "police_patrol"
    POLICE_DETECTIVE = "police_detective"
    FIRE_ENGINE = "fire_engine"
    FIRE_TRUCK = "fire_truck"
    LADDER_TRUCK = "ladder_truck"
    AMBULANCE = "ambulance"
    BATTALION_CHIEF = "battalion_chief"
    HAZMAT = "hazmat"
    K9 = "k9"


class IncidentLevel(Enum):
    """EOC activation levels."""
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"


class BuildingType(Enum):
    """Building classification for fire risk."""
    RESIDENTIAL_SINGLE = "residential_single"
    RESIDENTIAL_MULTI = "residential_multi"
    COMMERCIAL = "commercial"
    INDUSTRIAL = "industrial"
    INSTITUTIONAL = "institutional"
    MIXED_USE = "mixed_use"


class CrimeType(Enum):
    """Classification of crime types."""
    BURGLARY = "burglary"
    AUTO_THEFT = "auto_theft"
    ASSAULT = "assault"
    ROBBERY = "robbery"
    VANDALISM = "vandalism"
    FRAUD = "fraud"
    DRUG_OFFENSE = "drug_offense"


class AlertType(Enum):
    """Video analytics alert types."""
    CROWD_DENSITY = "crowd_density"
    UNATTENDED_OBJECT = "unattended_object"
    PERIMETER_BREACH = "perimeter_breach"
    VEHICLE_LEFT = "vehicle_left"
    PERSON_DOWN = "person_down"


class AlertPriority(Enum):
    """Gunshot and incident alert priorities."""
    ROUTINE = "routine"
    HIGH = "high"
    IMMEDIATE = "immediate"


class FireRiskCategory(Enum):
    """Fire risk classification."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"
    CRITICAL = "critical"


class OutageSeverity(Enum):
    """Infrastructure outage severity."""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class AgencyConfig:
    """Configuration for the public safety agency."""
    departments: List[str] = field(default_factory=lambda: ["police", "fire", "ems"])
    jurisdiction_population: int = 0
    coverage_area_sq_km: float = 0.0
    stations: Dict[str, int] = field(default_factory=dict)


@dataclass
class IntegrationConfig:
    """External system integration configuration."""
    cad_system: str = "default_cad"
    rms_system: str = "default_rms"
    video_platform: str = "default_video"
    gunshot_detection: str = "none"
    weather_service: str = "nws_api"


@dataclass
class GeoLocation:
    """Geographic location with lat/lon."""
    latitude: float
    longitude: float
    address: str = ""

    def __post_init__(self) -> None:
        if not (-90.0 <= self.latitude <= 90.0):
            raise ValueError(f"Invalid latitude: {self.latitude}")


@dataclass
class CADIncident:
    """Computer-Aided Dispatch incident."""
    incident_id: str
    call_type: str
    priority: PriorityLevel
    location: GeoLocation
    description: str = ""
    caller_phone: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class UnitAssignment:
    """Recommended unit assignment for an incident."""
    unit_id: str
    unit_type: UnitType
    eta_seconds: int
    station: str
    from_mutual_aid: bool = False


@dataclass
class CrimePattern:
    """Detected crime pattern or series."""
    pattern_id: str
    crime_type: str
    incidents: List[Dict[str, Any]] = field(default_factory=list)
    cluster_center: Optional[GeoLocation] = None
    temporal_pattern: str = ""
    predicted_next_location: Optional[GeoLocation] = None


@dataclass
class Camera:
    """Public safety camera."""
    camera_id: str
    name: str
    location: GeoLocation
    status: str = "online"
    has_analytics: bool = False


@dataclass
class VideoFootage:
    """Reviewed video footage for an incident."""
    incident_id: str
    camera_ids: List[str]
    duration_minutes: float
    footage_paths: List[str] = field(default_factory=list)


@dataclass
class EOCActivation:
    """Emergency Operations Center activation."""
    activation_id: str
    event_type: str
    level: IncidentLevel
    activated_by: str
    departments: List[str] = field(default_factory=list)
    activated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class EOCResources:
    """Current EOC resource status."""
    shelters_open: int = 0
    shelter_capacity: int = 0
    evacuees_registered: int = 0
    mutual_aid_pending: int = 0
    crews_dispatched: int = 0


@dataclass
class FireRiskAssessment:
    """Fire risk assessment for a building."""
    building_id: str
    risk_score: float
    risk_category: FireRiskCategory
    key_factors: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class GunshotAlert:
    """Gunshot detection alert."""
    alert_id: str
    timestamp: datetime
    location: GeoLocation
    rounds_count: int
    confidence: float
    weapon_estimate: str = "unknown"


# ---------------------------------------------------------------------------
# Helper Classes
# ---------------------------------------------------------------------------

class CADInterface:
    """Computer-Aided Dispatch interface."""

    def __init__(self, engine: "PublicSafetyEngine") -> None:
        self._engine = engine

    def create_incident(
        self,
        call_type: str,
        priority: PriorityLevel,
        location: Dict[str, float],
        caller_info: Optional[Dict[str, str]] = None,
        description: str = "",
    ) -> CADIncident:
        geo = GeoLocation(
            latitude=location.get("lat", 0.0),
            longitude=location.get("lon", 0.0),
            address=location.get("address", ""),
        )
        incident = CADIncident(
            incident_id=f"inc-{uuid.uuid4().hex[:8]}",
            call_type=call_type,
            priority=priority,
            location=geo,
            description=description,
            caller_phone=caller_info.get("callback_number") if caller_info else None,
        )
        self._engine._incidents[incident.incident_id] = incident
        return incident

    def recommend_units(
        self,
        incident_id: str,
        units_needed: List[Dict[str, Any]],
        strategy: str = "closest_valid",
        include_mutual_aid_if_needed: bool = False,
    ) -> List[UnitAssignment]:
        import random
        random.seed(hash(incident_id) % 2**31)

        assignments: List[UnitAssignment] = []
        for spec in units_needed:
            unit_type = spec.get("unit_type", UnitType.POLICE_PATROL)
            quantity = spec.get("quantity", 1)
            for _ in range(quantity):
                assignments.append(UnitAssignment(
                    unit_id=f"unit-{uuid.uuid4().hex[:4].upper()}",
                    unit_type=unit_type if isinstance(unit_type, UnitType) else UnitType.POLICE_PATROL,
                    eta_seconds=random.randint(60, 600),
                    station=f"station-{random.randint(1, 10):02d}",
                ))
        return assignments


class CrimeAnalytics:
    """Crime pattern analysis and predictive policing."""

    def __init__(self, engine: "PublicSafetyEngine") -> None:
        self._engine = engine

    def detect_series(
        self,
        crime_types: List[str],
        time_window: str = "90_days",
        min_incidents: int = 3,
        max_cluster_radius_m: float = 2000.0,
        method: str = "spatial_temporal_clustering",
    ) -> List[CrimePattern]:
        import random
        random.seed(42)

        patterns: List[CrimePattern] = []
        for i in range(3):
            count = random.randint(min_incidents, min_incidents + 5)
            patterns.append(CrimePattern(
                pattern_id=f"pattern-{uuid.uuid4().hex[:6]}",
                crime_type=random.choice(crime_types),
                incidents=[{"case_id": f"case-{j}"} for j in range(count)],
                cluster_center=GeoLocation(
                    41.88 + random.uniform(-0.05, 0.05),
                    -87.63 + random.uniform(-0.05, 0.05),
                ),
                temporal_pattern=random.choice(["daytime", "nighttime", "weekend", "random"]),
                predicted_next_location=GeoLocation(
                    41.88 + random.uniform(-0.03, 0.03),
                    -87.63 + random.uniform(-0.03, 0.03),
                ),
            ))
        return patterns

    def optimize_patrols(
        self,
        zone_id: str,
        time_period: str = "next_24_hours",
        budget_units: int = 8,
    ) -> List[Dict[str, Any]]:
        import random
        random.seed(hash(zone_id) % 2**31)

        return [
            {
                "patrol_id": f"patrol-{i}",
                "zone": zone_id,
                "unit_type": "police_patrol",
                "focus_area": f"area-{random.choice(['north', 'south', 'east', 'west'])}",
                "priority_score": round(random.uniform(0.5, 1.0), 2),
            }
            for i in range(budget_units)
        ]


class VideoManager:
    """Video surveillance management and analytics."""

    def __init__(self, engine: "PublicSafetyEngine") -> None:
        self._engine = engine
        self._cameras: Dict[str, Camera] = {}
        self._alerts: List[Dict[str, Any]] = []

    def configure_alerts(
        self,
        zone_id: str,
        alerts: List[Dict[str, Any]],
    ) -> None:
        for alert_config in alerts:
            self._alerts.append({"zone": zone_id, **alert_config})
            logger.info("Configured alert in %s: %s", zone_id, alert_config.get("type"))

    def get_camera_status(self, zone_id: str = "") -> List[Camera]:
        return list(self._cameras.values())

    def review_incident(
        self,
        incident_id: str,
        camera_ids: List[str],
        time_range_minutes: int = 15,
    ) -> VideoFootage:
        return VideoFootage(
            incident_id=incident_id,
            camera_ids=camera_ids,
            duration_minutes=float(time_range_minutes),
            footage_paths=[f"footage/{incident_id}_{cid}.mp4" for cid in camera_ids],
        )

    def add_camera(self, camera: Camera) -> None:
        self._cameras[camera.camera_id] = camera


class EOCManager:
    """Emergency Operations Center management."""

    def __init__(self, engine: "PublicSafetyEngine") -> None:
        self._engine = engine
        self._activations: Dict[str, EOCActivation] = {}

    def activate(
        self,
        event_type: str,
        level: IncidentLevel,
        activated_by: str = "director",
        expected_duration_hours: int = 8,
    ) -> EOCActivation:
        activation = EOCActivation(
            activation_id=f"eoc-{uuid.uuid4().hex[:8]}",
            event_type=event_type,
            level=level,
            activated_by=activated_by,
            departments=self._engine._config.departments,
        )
        self._activations[activation.activation_id] = activation
        logger.info("EOC activated: %s (level %s)", event_type, level.value)
        return activation

    def get_resource_status(self) -> EOCResources:
        import random
        random.seed(42)
        return EOCResources(
            shelters_open=random.randint(2, 10),
            shelter_capacity=random.randint(1000, 5000),
            evacuees_registered=random.randint(100, 2000),
            mutual_aid_pending=random.randint(0, 5),
            crews_dispatched=random.randint(5, 25),
        )

    def update_situation(
        self,
        activation_id: str,
        summary: str,
        next_update_hours: int = 2,
    ) -> None:
        logger.info("Situation update for %s: %s", activation_id, summary)


class FireRiskAssessor:
    """Building fire risk assessment."""

    def __init__(self, engine: "PublicSafetyEngine") -> None:
        self._engine = engine

    def evaluate_building(
        self,
        building_id: str,
        building_type: BuildingType,
        floors: int,
        construction_type: str = "Type_III",
        occupancy_load: int = 0,
        fire_protection: Optional[List[str]] = None,
        last_inspection_date: Optional[str] = None,
    ) -> FireRiskAssessment:
        import random
        random.seed(hash(building_id) % 2**31)

        base_score = 30.0
        if floors > 5:
            base_score += 15.0
        if construction_type in ("Type_V", "Type_IV"):
            base_score += 10.0
        if fire_protection and "sprinklered" in fire_protection:
            base_score -= 20.0
        if occupancy_load > 300:
            base_score += 10.0

        score = max(0.0, min(100.0, base_score + random.uniform(-10, 10)))

        if score < 25:
            category = FireRiskCategory.LOW
        elif score < 45:
            category = FireRiskCategory.MODERATE
        elif score < 65:
            category = FireRiskCategory.HIGH
        elif score < 85:
            category = FireRiskCategory.VERY_HIGH
        else:
            category = FireRiskCategory.CRITICAL

        factors = []
        if floors > 5:
            factors.append("High-rise structure")
        if construction_type in ("Type_V", "Type_IV"):
            factors.append("Combustible construction")
        if not fire_protection or "sprinklered" not in fire_protection:
            factors.append("No sprinkler system")

        recommendations = []
        if score >= 50:
            recommendations.append("Schedule pre-incident planning visit")
        if not fire_protection or "sprinklered" not in fire_protection:
            recommendations.append("Recommend sprinkler installation")
        if floors > 3:
            recommendations.append("Verify standpipe system")

        return FireRiskAssessment(
            building_id=building_id,
            risk_score=round(score, 1),
            risk_category=category,
            key_factors=factors,
            recommendations=recommendations,
        )

    def generate_risk_heatmap(
        self,
        district_id: str,
        resolution_blocks: int = 50,
        include_inspection_schedule: bool = True,
    ) -> Dict[str, Any]:
        import random
        random.seed(hash(district_id) % 2**31)

        blocks = []
        for i in range(resolution_blocks):
            blocks.append({
                "block_id": f"{district_id}_block-{i:03d}",
                "risk_score": round(random.uniform(10, 90), 1),
                "building_count": random.randint(5, 50),
                "next_inspection": f"2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}",
            })
        return {"district_id": district_id, "blocks": blocks}


class GunshotDetector:
    """Acoustic gunshot detection system."""

    def __init__(self, engine: "PublicSafetyEngine") -> None:
        self._engine = engine
        self._recent_alerts: List[GunshotAlert] = []

    def get_recent_alerts(
        self,
        time_window_minutes: int = 60,
        min_confidence: float = 0.8,
    ) -> List[GunshotAlert]:
        return [
            a for a in self._recent_alerts
            if a.confidence >= min_confidence
        ]

    def register_alert(self, alert: GunshotAlert) -> None:
        self._recent_alerts.append(alert)
        logger.warning("Gunshot detected: %d rounds at %s (conf: %.1f%%)",
                       alert.rounds_count, alert.location.address, alert.confidence * 100)

    def dispatch_response(
        self,
        alert_id: str,
        units: int = 2,
        priority: AlertPriority = AlertPriority.IMMEDIATE,
        include_trauma_alert: bool = True,
    ) -> Dict[str, Any]:
        logger.info("Dispatched %d units for gunshot alert %s", units, alert_id)
        return {
            "alert_id": alert_id,
            "units_dispatched": units,
            "priority": priority.value,
            "trauma_alert": include_trauma_alert,
        }


# ---------------------------------------------------------------------------
# Main Engine
# ---------------------------------------------------------------------------

class PublicSafetyEngine:
    """Main engine for public safety operations."""

    def __init__(
        self,
        agency_id: str,
        agency_config: Optional[AgencyConfig] = None,
        integration_config: Optional[IntegrationConfig] = None,
    ) -> None:
        self.agency_id = agency_id
        self._config = agency_config or AgencyConfig()
        self._integrations = integration_config or IntegrationConfig()
        self._status = EngineStatus.UNINITIALIZED
        self._incidents: Dict[str, CADIncident] = {}
        self._units_online: int = 0
        self._camera_feeds_active: int = 0
        self._created_at = datetime.utcnow()
        self._last_run: Optional[datetime] = None

    def configure(self) -> PublicSafetyEngine:
        """Validate configuration and establish system connections."""
        self._status = EngineStatus.CONFIGURING

        self._units_online = sum(
            count * 2 for count in self._config.stations.values()
        )
        self._camera_feeds_active = 180

        logger.info(
            "Public safety engine configured for %s: %d units, %d cameras",
            self.agency_id, self._units_online, self._camera_feeds_active,
        )
        self._status = EngineStatus.READY
        return self

    def run(self) -> Dict[str, Any]:
        """Execute a full public safety monitoring cycle."""
        if self._status != EngineStatus.READY:
            raise RuntimeError(f"Engine not ready: {self._status.name}")

        self._status = EngineStatus.RUNNING
        self._last_run = datetime.utcnow()

        result = {
            "agency_id": self.agency_id,
            "status": self._status.value,
            "timestamp": self._last_run.isoformat(),
            "active_incidents": len(self._incidents),
            "units_online": self._units_online,
            "cameras_active": self._camera_feeds_active,
        }

        self._status = EngineStatus.READY
        return result

    def validate(self) -> bool:
        """Validate engine configuration."""
        if self._status == EngineStatus.UNINITIALIZED:
            return False
        if not self.agency_id:
            return False
        return True

    def get_status(self) -> Dict[str, Any]:
        """Get current engine status and metrics."""
        return {
            "engine": "PublicSafety",
            "agency_id": self.agency_id,
            "status": self._status.name,
            "units_online": self._units_online,
            "camera_feeds_active": self._camera_feeds_active,
            "cad_status": "connected",
            "departments": self._config.departments,
            "population_served": self._config.jurisdiction_population,
            "uptime_seconds": (datetime.utcnow() - self._created_at).total_seconds(),
            "last_run": self._last_run.isoformat() if self._last_run else None,
        }

    def shutdown(self) -> None:
        """Gracefully shut down the engine."""
        self._status = EngineStatus.SHUTDOWN
        logger.info("Public safety engine shut down for %s", self.agency_id)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate public safety engine capabilities."""
    print("=" * 70)
    print("  Public Safety — Integrated Emergency Management Platform Demo")
    print("=" * 70)

    engine = PublicSafetyEngine(
        agency_id="metro-fire-police-001",
        agency_config=AgencyConfig(
            departments=["police", "fire", "ems", "emergency_management"],
            jurisdiction_population=2_500_000,
            coverage_area_sq_km=1_200,
            stations={"police": 45, "fire": 62, "ems": 28},
        ),
        integration_config=IntegrationConfig(
            cad_system="intergraph_cad", rms_system="mark43",
            video_platform="genetecSecurityCenter", gunshot_detection="shotspotter",
        ),
    )

    engine.configure()
    status = engine.get_status()
    print(f"\n[1] Engine Status: {status['status']}")
    print(f"    Active units: {status['units_online']}")
    print(f"    CAD connection: {status['cad_status']}")
    print(f"    Video feeds: {status['camera_feeds_active']}")

    cad = CADInterface(engine)
    incident = cad.create_incident(
        call_type="structure_fire", priority=PriorityLevel.CRITICAL,
        location={"lat": 41.8781, "lon": -87.6298, "address": "123 N State St"},
        description="Smoke showing from 3-story commercial building",
    )
    print(f"\n[2] CAD Incident Created: {incident.incident_id}")
    print(f"    Call type: {incident.call_type}, Priority: {incident.priority.name}")

    assignments = cad.recommend_units(
        incident_id=incident.incident_id,
        units_needed=[
            {"unit_type": UnitType.FIRE_ENGINE, "quantity": 3},
            {"unit_type": UnitType.AMBULANCE, "quantity": 2},
        ],
    )
    print(f"    Units assigned: {len(assignments)}")
    for a in assignments[:3]:
        print(f"      {a.unit_id}: ETA {a.eta_seconds}s from {a.station}")

    crime_analytics = CrimeAnalytics(engine)
    patterns = crime_analytics.detect_series(
        crime_types=["burglary", "auto_theft"],
        time_window="90_days", min_incidents=3,
    )
    print(f"\n[3] Crime Patterns Detected: {len(patterns)}")
    for p in patterns:
        print(f"    {p.pattern_id}: {p.crime_type} ({len(p.incidents)} incidents, "
              f"temporal: {p.temporal_pattern})")

    patrols = crime_analytics.optimize_patrols(zone_id="district-south-03", budget_units=8)
    print(f"    Patrol recommendations: {len(patrols)} units")

    video = VideoManager(engine)
    video.add_camera(Camera(
        camera_id="cam-main-001", name="Main & State Camera",
        location=GeoLocation(41.878, -87.630),
    ))
    cameras = video.get_camera_status()
    online = sum(1 for c in cameras if c.status == "online")
    print(f"\n[4] Video: {online}/{len(cameras)} cameras online")

    footage = video.review_incident(
        incident_id=incident.incident_id,
        camera_ids=["cam-main-001"],
    )
    print(f"    Footage: {len(footage.footage_paths)} clips, {footage.duration_minutes:.0f} min")

    eoc = EOCManager(engine)
    activation = eoc.activate(
        event_type="severe_thunderstorm", level=IncidentLevel.LEVEL_2,
    )
    resources = eoc.get_resource_status()
    print(f"\n[5] EOC Activation: {activation.activation_id}")
    print(f"    Level: {activation.level.value}")
    print(f"    Shelters open: {resources.shelters_open}")
    print(f"    Evacuees registered: {resources.evacuees_registered:,}")

    fire = FireRiskAssessor(engine)
    risk = fire.evaluate_building(
        building_id="bldg-commercial-4521", building_type=BuildingType.COMMERCIAL,
        floors=8, construction_type="Type_IA", occupancy_load=350,
        fire_protection=["sprinklered", "standpipe", "fire_alarm"],
    )
    print(f"\n[6] Fire Risk: {risk.risk_score:.1f}/100 ({risk.risk_category.value})")
    print(f"    Key factors: {risk.key_factors}")
    print(f"    Recommendations: {risk.recommendations}")

    gs = GunshotDetector(engine)
    alert = GunshotAlert(
        alert_id="gs-001", timestamp=datetime.utcnow(),
        location=GeoLocation(41.880, -87.625, "Michigan & 12th"),
        rounds_count=5, confidence=0.92,
    )
    gs.register_alert(alert)
    recent = gs.get_recent_alerts(min_confidence=0.8)
    print(f"\n[7] Gunshot Alerts: {len(recent)}")
    for a in recent:
        print(f"    {a.rounds_count} rounds at {a.location.address} "
              f"(confidence: {a.confidence:.0%})")

    result = engine.run()
    print(f"\n[8] Pipeline Run: {result['active_incidents']} incidents, "
          f"{result['units_online']} units")

    engine.shutdown()
    print(f"\n[9] Engine Shutdown: {engine.get_status()['status']}")


if __name__ == "__main__":
    main()

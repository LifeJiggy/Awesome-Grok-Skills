"""
Disaster Response Module
Part of the humanitarian-tech skill domain

Comprehensive disaster response system covering early warning detection,
damage assessment, resource coordination, and evacuation routing.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional, Tuple, Union
import json
import math
import random
import uuid


# =============================================================================
# Enums
# =============================================================================

class DisasterType(Enum):
    """Types of natural and human-caused disasters."""
    EARTHQUAKE = "earthquake"
    FLOOD = "flood"
    HURRICANE = "hurricane"
    WILDFIRE = "wildfire"
    TSUNAMI = "tsunami"
    TORNADO = "tornado"
    LANDSLIDE = "landslide"
    VOLCANIC = "volcanic"
    INDUSTRIAL = "industrial"
    CONFLICT = "conflict"


class AlertLevel(IntEnum):
    """Alert severity levels (higher number = more severe)."""
    WATCH = 1
    ADVISORY = 2
    WARNING = 3
    EMERGENCY = 4
    CATASTROPHIC = 5


class DamageLevel(Enum):
    """Damage severity classification."""
    NONE = "none"
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    DEVASTATING = "devastating"
    TOTAL = "total"


class ResourcePriority(Enum):
    """Priority levels for resource allocation."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    LIFE_SAVING = "life_saving"


class RouteSafety(Enum):
    """Safety rating for evacuation routes."""
    UNSAFE = "unsafe"
    RISKY = "risky"
    MODERATE = "moderate"
    SAFE = "safe"
    RECOMMENDED = "recommended"


class ShelterStatus(Enum):
    """Current operational status of shelters."""
    CLOSED = "closed"
    STANDBY = "standby"
    OPEN = "open"
    AT_CAPACITY = "at_capacity"
    OVERFLOW = "overflow"


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass
class GeoLocation:
    """Geographic coordinate representation."""
    latitude: float
    longitude: float
    elevation_meters: float = 0.0
    place_name: Optional[str] = None

    def distance_to(self, other: 'GeoLocation') -> float:
        """Calculate approximate distance in kilometers using Haversine formula."""
        R = 6371.0  # Earth's radius in kilometers
        lat1_rad = math.radians(self.latitude)
        lat2_rad = math.radians(other.latitude)
        dlat = math.radians(other.latitude - self.latitude)
        dlon = math.radians(other.longitude - self.longitude)

        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def to_dict(self) -> Dict[str, Any]:
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "elevation_meters": self.elevation_meters,
            "place_name": self.place_name
        }


@dataclass
class DisasterEvent:
    """Represents a single disaster event."""
    event_id: str
    disaster_type: DisasterType
    location: GeoLocation
    magnitude: float
    start_time: datetime
    description: str = ""
    alert_level: AlertLevel = AlertLevel.ADVISORY
    is_active: bool = True
    affected_population: int = 0
    estimated_damage_usd: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def severity_score(self) -> float:
        """Calculate normalized severity score (0-10)."""
        base = min(self.magnitude / 10.0, 1.0) * 5.0
        alert_bonus = self.alert_level.value * 0.5
        pop_factor = min(self.affected_population / 100000, 1.0) * 2.5
        return min(base + alert_bonus + pop_factor, 10.0)

    def duration_hours(self) -> float:
        """Calculate event duration in hours."""
        end = self.metadata.get("end_time")
        if end:
            end_dt = datetime.fromisoformat(end) if isinstance(end, str) else end
            return (end_dt - self.start_time).total_seconds() / 3600
        return (datetime.now() - self.start_time).total_seconds() / 3600

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "disaster_type": self.disaster_type.value,
            "location": self.location.to_dict(),
            "magnitude": self.magnitude,
            "start_time": self.start_time.isoformat(),
            "description": self.description,
            "alert_level": self.alert_level.value,
            "is_active": self.is_active,
            "affected_population": self.affected_population,
            "estimated_damage_usd": self.estimated_damage_usd,
            "severity_score": self.severity_score(),
            "metadata": self.metadata
        }


@dataclass
class DamageReport:
    """Post-disaster damage assessment report."""
    report_id: str
    event_id: str
    assessment_time: datetime
    location: GeoLocation
    damage_level: DamageLevel
    buildings_damaged: int = 0
    buildings_destroyed: int = 0
    infrastructure_damage: Dict[str, DamageLevel] = field(default_factory=dict)
    casualties: int = 0
    displaced_persons: int = 0
    access_status: str = "accessible"
    assessor_notes: str = ""

    def total_structures_affected(self) -> int:
        return self.buildings_damaged + self.buildings_destroyed

    def damage_ratio(self) -> float:
        """Ratio of destroyed to total affected structures."""
        total = self.total_structures_affected()
        if total == 0:
            return 0.0
        return self.buildings_destroyed / total

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "event_id": self.event_id,
            "assessment_time": self.assessment_time.isoformat(),
            "location": self.location.to_dict(),
            "damage_level": self.damage_level.value,
            "buildings_damaged": self.buildings_damaged,
            "buildings_destroyed": self.buildings_destroyed,
            "infrastructure_damage": {k: v.value for k, v in self.infrastructure_damage.items()},
            "casualties": self.casualties,
            "displaced_persons": self.displaced_persons,
            "access_status": self.access_status,
            "total_structures_affected": self.total_structures_affected(),
            "damage_ratio": self.damage_ratio()
        }


@dataclass
class Resource:
    """Humanitarian resource item."""
    resource_id: str
    resource_type: str
    quantity: float
    unit: str
    location: GeoLocation
    priority: ResourcePriority = ResourcePriority.MEDIUM
    expiry_date: Optional[datetime] = None
    allocated_to: Optional[str] = None
    status: str = "available"
    source_agency: str = ""
    cost_per_unit: float = 0.0

    def is_available(self) -> bool:
        if self.status != "available":
            return False
        if self.expiry_date and self.expiry_date < datetime.now():
            return False
        return True

    def total_value(self) -> float:
        return self.quantity * self.cost_per_unit

    def to_dict(self) -> Dict[str, Any]:
        return {
            "resource_id": self.resource_id,
            "resource_type": self.resource_type,
            "quantity": self.quantity,
            "unit": self.unit,
            "location": self.location.to_dict(),
            "priority": self.priority.value,
            "expiry_date": self.expiry_date.isoformat() if self.expiry_date else None,
            "allocated_to": self.allocated_to,
            "status": self.status,
            "source_agency": self.source_agency,
            "total_value": self.total_value()
        }


@dataclass
class EvacuationRoute:
    """Evacuation route from danger zone to shelter."""
    route_id: str
    start_location: GeoLocation
    end_location: GeoLocation
    waypoints: List[GeoLocation] = field(default_factory=list)
    distance_km: float = 0.0
    estimated_time_minutes: float = 0.0
    capacity: int = 0
    current_usage: int = 0
    safety_rating: RouteSafety = RouteSafety.MODERATE
    road_conditions: str = "good"
    is_bidirectional: bool = False

    def available_capacity(self) -> int:
        return max(0, self.capacity - self.current_usage)

    def utilization_rate(self) -> float:
        if self.capacity == 0:
            return 0.0
        return self.current_usage / self.capacity

    def is_usable(self) -> bool:
        return self.safety_rating not in (RouteSafety.UNSAFE, RouteSafety.RISKY)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "route_id": self.route_id,
            "start_location": self.start_location.to_dict(),
            "end_location": self.end_location.to_dict(),
            "waypoint_count": len(self.waypoints),
            "distance_km": self.distance_km,
            "estimated_time_minutes": self.estimated_time_minutes,
            "capacity": self.capacity,
            "current_usage": self.current_usage,
            "available_capacity": self.available_capacity(),
            "safety_rating": self.safety_rating.value,
            "road_conditions": self.road_conditions,
            "utilization_rate": self.utilization_rate()
        }


@dataclass
class Shelter:
    """Emergency shelter facility."""
    shelter_id: str
    name: str
    location: GeoLocation
    capacity: int
    current_occupancy: int = 0
    status: ShelterStatus = ShelterStatus.STANDBY
    facilities: List[str] = field(default_factory=lambda: ["water", "blankets"])
    contact_person: str = ""
    contact_phone: str = ""

    def available_beds(self) -> int:
        return max(0, self.capacity - self.current_occupancy)

    def occupancy_rate(self) -> float:
        if self.capacity == 0:
            return 0.0
        return self.current_occupancy / self.capacity

    def check_in(self, count: int) -> bool:
        if self.current_occupancy + count > self.capacity:
            return False
        self.current_occupancy += count
        if self.current_occupancy >= self.capacity:
            self.status = ShelterStatus.AT_CAPACITY
        return True

    def check_out(self, count: int) -> int:
        actual = min(count, self.current_occupancy)
        self.current_occupancy -= actual
        if self.status == ShelterStatus.AT_CAPACITY:
            self.status = ShelterStatus.OPEN
        return actual

    def to_dict(self) -> Dict[str, Any]:
        return {
            "shelter_id": self.shelter_id,
            "name": self.name,
            "location": self.location.to_dict(),
            "capacity": self.capacity,
            "current_occupancy": self.current_occupancy,
            "available_beds": self.available_beds(),
            "status": self.status.value,
            "occupancy_rate": self.occupancy_rate(),
            "facilities": self.facilities
        }


@dataclass
class Alert:
    """Disaster alert notification."""
    alert_id: str
    level: AlertLevel
    event_id: str
    message: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    channels: List[str] = field(default_factory=lambda: ["sms", "email"])
    acknowledged: bool = False
    recipients: List[str] = field(default_factory=list)

    def is_expired(self) -> bool:
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at

    def urgency_score(self) -> int:
        """Higher score = more urgent."""
        base = self.level.value * 20
        if self.expires_at:
            hours_left = (self.expires_at - datetime.now()).total_seconds() / 3600
            if hours_left < 1:
                base += 30
            elif hours_left < 6:
                base += 15
        return min(base, 100)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "alert_id": self.alert_id,
            "level": self.level.value,
            "level_name": self.level.name,
            "event_id": self.event_id,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "channels": self.channels,
            "acknowledged": self.acknowledged,
            "urgency_score": self.urgency_score()
        }


# =============================================================================
# Core Systems
# =============================================================================

class EarlyWarningSystem:
    """Multi-hazard early warning and monitoring system."""

    def __init__(self, sensitivity: str = "medium", monitoring_interval_seconds: int = 60):
        self.sensitivity = sensitivity
        self.monitoring_interval = monitoring_interval_seconds
        self.active_events: List[DisasterEvent] = []
        self.alerts: List[Alert] = []
        self.sensors: Dict[str, Dict[str, Any]] = {}
        self._thresholds = self._load_thresholds()

    def _load_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Load hazard detection thresholds based on sensitivity."""
        base_thresholds = {
            "earthquake": {"watch": 3.0, "advisory": 4.5, "warning": 5.5, "emergency": 6.5, "catastrophic": 7.5},
            "flood": {"watch": 0.5, "advisory": 1.0, "warning": 2.0, "emergency": 3.0, "catastrophic": 5.0},
            "hurricane": {"watch": 30, "advisory": 50, "warning": 80, "emergency": 110, "catastrophic": 140},
            "wildfire": {"watch": 100, "advisory": 500, "warning": 1000, "emergency": 5000, "catastrophic": 10000},
            "tsunami": {"watch": 0.3, "advisory": 0.5, "warning": 1.0, "emergency": 2.0, "catastrophic": 5.0}
        }
        if self.sensitivity == "high":
            for hazard in base_thresholds:
                for level in base_thresholds[hazard]:
                    base_thresholds[hazard][level] *= 0.7
        elif self.sensitivity == "low":
            for hazard in base_thresholds:
                for level in base_thresholds[hazard]:
                    base_thresholds[hazard][level] *= 1.5
        return base_thresholds

    def determine_alert_level(self, disaster_type: DisasterType, magnitude: float) -> AlertLevel:
        """Determine alert level based on disaster type and magnitude."""
        thresholds = self._thresholds.get(disaster_type.value, {})
        if magnitude >= thresholds.get("catastrophic", float('inf')):
            return AlertLevel.CATASTROPHIC
        elif magnitude >= thresholds.get("emergency", float('inf')):
            return AlertLevel.EMERGENCY
        elif magnitude >= thresholds.get("warning", float('inf')):
            return AlertLevel.WARNING
        elif magnitude >= thresholds.get("advisory", float('inf')):
            return AlertLevel.ADVISORY
        return AlertLevel.WATCH

    def register_sensor(self, sensor_id: str, sensor_type: str, location: GeoLocation) -> None:
        """Register a monitoring sensor."""
        self.sensors[sensor_id] = {
            "type": sensor_type,
            "location": location.to_dict(),
            "last_reading": None,
            "status": "active",
            "registered_at": datetime.now().isoformat()
        }

    def process_sensor_reading(self, sensor_id: str, reading: float) -> Optional[Alert]:
        """Process a sensor reading and generate alert if threshold exceeded."""
        if sensor_id not in self.sensors:
            return None

        sensor = self.sensors[sensor_id]
        sensor["last_reading"] = reading
        sensor_type = sensor["type"]

        for dtype in DisasterType:
            if dtype.value == sensor_type or sensor_type in dtype.value:
                alert_level = self.determine_alert_level(dtype, reading)
                if alert_level.value >= AlertLevel.WARNING:
                    alert = self._generate_alert(dtype, reading, alert_level, sensor_id)
                    return alert
        return None

    def _generate_alert(self, disaster_type: DisasterType, magnitude: float,
                        level: AlertLevel, trigger_sensor: str) -> Alert:
        """Generate and store an alert."""
        alert_id = f"ALR-{uuid.uuid4().hex[:8].upper()}"
        event_id = f"EVT-{uuid.uuid4().hex[:8].upper()}"

        event = DisasterEvent(
            event_id=event_id,
            disaster_type=disaster_type,
            location=GeoLocation(
                latitude=self.sensors[trigger_sensor]["location"]["latitude"],
                longitude=self.sensors[trigger_sensor]["location"]["longitude"]
            ),
            magnitude=magnitude,
            start_time=datetime.now(),
            alert_level=level,
            description=f"Auto-detected {disaster_type.value} event"
        )
        self.active_events.append(event)

        alert = Alert(
            alert_id=alert_id,
            level=level,
            event_id=event_id,
            message=f"{level.name} ALERT: {disaster_type.value} detected (magnitude: {magnitude}). Immediate action required.",
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(hours=24),
            channels=["sms", "email", "radio", "sirens"]
        )
        self.alerts.append(alert)
        return alert

    def get_active_alerts(self) -> List[Alert]:
        """Return all non-expired, unacknowledged alerts."""
        return [a for a in self.alerts if not a.is_expired() and not a.acknowledged]

    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert."""
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                return True
        return False

    def get_status(self) -> Dict[str, Any]:
        """Get current system status."""
        return {
            "sensitivity": self.sensitivity,
            "monitoring_interval_seconds": self.monitoring_interval,
            "registered_sensors": len(self.sensors),
            "active_sensors": sum(1 for s in self.sensors.values() if s["status"] == "active"),
            "active_events": len([e for e in self.active_events if e.is_active]),
            "active_alerts": len(self.get_active_alerts()),
            "total_alerts_generated": len(self.alerts)
        }


class DamageAssessmentEngine:
    """Post-disaster damage assessment and analysis system."""

    def __init__(self, assessment_type: str = "rapid"):
        self.assessment_type = assessment_type
        self.reports: List[DamageReport] = []
        self.damage_statistics: Dict[str, Any] = {}

    def create_damage_report(self, event_id: str, location: GeoLocation,
                             damage_level: DamageLevel, **kwargs) -> DamageReport:
        """Create and store a new damage report."""
        report = DamageReport(
            report_id=f"DAM-{uuid.uuid4().hex[:8].upper()}",
            event_id=event_id,
            assessment_time=datetime.now(),
            location=location,
            damage_level=damage_level,
            buildings_damaged=kwargs.get("buildings_damaged", 0),
            buildings_destroyed=kwargs.get("buildings_destroyed", 0),
            infrastructure_damage=kwargs.get("infrastructure_damage", {}),
            casualties=kwargs.get("casualties", 0),
            displaced_persons=kwargs.get("displaced_persons", 0),
            access_status=kwargs.get("access_status", "accessible"),
            assessor_notes=kwargs.get("notes", "")
        )
        self.reports.append(report)
        self._update_statistics()
        return report

    def _update_statistics(self) -> None:
        """Update aggregated damage statistics."""
        if not self.reports:
            return

        self.damage_statistics = {
            "total_reports": len(self.reports),
            "total_buildings_damaged": sum(r.buildings_damaged for r in self.reports),
            "total_buildings_destroyed": sum(r.buildings_destroyed for r in self.reports),
            "total_casualties": sum(r.casualties for r in self.reports),
            "total_displaced": sum(r.displaced_persons for r in self.reports),
            "damage_level_distribution": {},
            "average_damage_ratio": 0.0,
            "assessment_complete": True
        }

        for level in DamageLevel:
            count = sum(1 for r in self.reports if r.damage_level == level)
            self.damage_statistics["damage_level_distribution"][level.value] = count

        ratios = [r.damage_ratio() for r in self.reports if r.total_structures_affected() > 0]
        if ratios:
            self.damage_statistics["average_damage_ratio"] = sum(ratios) / len(ratios)

    def get_reports_by_severity(self, min_level: DamageLevel) -> List[DamageReport]:
        """Filter reports by minimum damage severity."""
        level_order = list(DamageLevel)
        min_idx = level_order.index(min_level)
        return [r for r in self.reports if level_order.index(r.damage_level) >= min_idx]

    def get_affected_area_summary(self, center: GeoLocation, radius_km: float) -> Dict[str, Any]:
        """Get summary of damage within a radius of a center point."""
        nearby = []
        for report in self.reports:
            distance = center.distance_to(report.location)
            if distance <= radius_km:
                nearby.append((report, distance))

        nearby.sort(key=lambda x: x[1])

        return {
            "center": center.to_dict(),
            "radius_km": radius_km,
            "reports_in_area": len(nearby),
            "total_casualties": sum(r.casualties for r, _ in nearby),
            "total_displaced": sum(r.displaced_persons for r, _ in nearby),
            "closest_damage": nearby[0].to_dict() if nearby else None,
            "farthest_damage": nearby[-1].to_dict() if nearby else None
        }

    def estimate_recovery_timeline(self) -> Dict[str, Any]:
        """Estimate recovery timeline based on damage statistics."""
        stats = self.damage_statistics
        total_destroyed = stats.get("total_buildings_destroyed", 0)
        total_damaged = stats.get("total_buildings_damaged", 0)

        if total_destroyed + total_damaged == 0:
            return {"status": "no_damage", "estimated_months": 0}

        severity_factor = stats.get("average_damage_ratio", 0.5)
        base_months = 6
        estimated = base_months * (1 + severity_factor) + (total_destroyed / 100)

        return {
            "status": "estimated",
            "estimated_months": round(estimated, 1),
            "total_structures": total_destroyed + total_damaged,
            "severity_factor": severity_factor,
            "phases": {
                "emergency_response": "0-2 weeks",
                "temporary_shelter": "2 weeks - 3 months",
                "reconstruction": f"3 - {int(estimated)} months",
                "full_recovery": f"{int(estimated)} - {int(estimated * 1.5)} months"
            }
        }


class ResourceCoordinator:
    """Humanitarian resource allocation and coordination system."""

    def __init__(self, coordination_center: Optional[GeoLocation] = None):
        self.coordination_center = coordination_center or GeoLocation(0.0, 0.0)
        self.resources: List[Resource] = []
        self.allocations: List[Dict[str, Any]] = []
        self.agencies: Dict[str, Dict[str, Any]] = {}

    def register_resource(self, resource: Resource) -> None:
        """Register a new resource in the system."""
        self.resources.append(resource)

    def register_agency(self, agency_id: str, name: str, contact: str,
                        capabilities: List[str]) -> None:
        """Register a humanitarian agency."""
        self.agencies[agency_id] = {
            "name": name,
            "contact": contact,
            "capabilities": capabilities,
            "registered_at": datetime.now().isoformat()
        }

    def find_available_resources(self, resource_type: Optional[str] = None,
                                 priority: Optional[ResourcePriority] = None,
                                 max_distance_km: float = float('inf')) -> List[Resource]:
        """Find available resources matching criteria."""
        results = []
        for resource in self.resources:
            if not resource.is_available():
                continue
            if resource_type and resource.resource_type != resource_type:
                continue
            if priority and resource.priority.value < priority.value:
                continue
            distance = self.coordination_center.distance_to(resource.location)
            if distance <= max_distance_km:
                results.append(resource)
        return results

    def allocate_resource(self, resource_id: str, allocation_id: str,
                          destination: GeoLocation, quantity: float,
                          agency_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Allocate resources to a specific destination."""
        resource = next((r for r in self.resources if r.resource_id == resource_id), None)
        if not resource or not resource.is_available():
            return None
        if quantity > resource.quantity:
            return None

        allocation = {
            "allocation_id": allocation_id,
            "resource_id": resource_id,
            "resource_type": resource.resource_type,
            "quantity_allocated": quantity,
            "unit": resource.unit,
            "destination": destination.to_dict(),
            "agency_id": agency_id,
            "allocated_at": datetime.now().isoformat(),
            "estimated_delivery_hours": self._estimate_delivery_time(resource.location, destination),
            "status": "pending"
        }

        resource.quantity -= quantity
        if resource.quantity <= 0:
            resource.status = "depleted"

        self.allocations.append(allocation)
        return allocation

    def _estimate_delivery_time(self, origin: GeoLocation, destination: GeoLocation) -> float:
        """Estimate delivery time in hours based on distance."""
        distance = origin.distance_to(destination)
        avg_speed_kmh = 40.0  # Average speed for humanitarian convoys
        return round(distance / avg_speed_kmh, 1)

    def get_resource_summary(self) -> Dict[str, Any]:
        """Get summary of all resources."""
        by_type: Dict[str, Dict[str, Any]] = {}
        for resource in self.resources:
            rtype = resource.resource_type
            if rtype not in by_type:
                by_type[rtype] = {"total_quantity": 0, "available": 0, "total_value": 0.0}
            by_type[rtype]["total_quantity"] += resource.quantity
            by_type[rtype]["total_value"] += resource.total_value()
            if resource.is_available():
                by_type[rtype]["available"] += 1

        return {
            "total_resources": len(self.resources),
            "total_allocations": len(self.allocations),
            "resources_by_type": by_type,
            "pending_allocations": sum(1 for a in self.allocations if a["status"] == "pending"),
            "registered_agencies": len(self.agencies)
        }

    def priority_allocation_plan(self, event_id: str, affected_area: GeoLocation,
                                 required_types: List[str]) -> List[Dict[str, Any]]:
        """Generate a prioritized allocation plan for a disaster event."""
        plan = []
        for rtype in required_types:
            available = self.find_available_resources(resource_type=rtype)
            available.sort(key=lambda r: (r.priority.value, r.location.distance_to(affected_area)))
            for resource in available[:3]:
                plan.append({
                    "resource_type": rtype,
                    "resource_id": resource.resource_id,
                    "quantity_available": resource.quantity,
                    "distance_km": round(resource.location.distance_to(affected_area), 1),
                    "priority": resource.priority.value,
                    "recommended_action": "allocate_immediately" if resource.priority == ResourcePriority.LIFE_SAVING else "schedule_allocation"
                })
        return plan


class EvacuationRouter:
    """Evacuation route calculation and management system."""

    def __init__(self, optimization: str = "safety_first"):
        self.optimization = optimization
        self.routes: List[EvacuationRoute] = []
        self.shelters: List[Shelter] = []
        self.evacuation_plans: List[Dict[str, Any]] = []

    def add_route(self, route: EvacuationRoute) -> None:
        """Add an evacuation route to the system."""
        self.routes.append(route)

    def add_shelter(self, shelter: Shelter) -> None:
        """Register a shelter."""
        self.shelters.append(shelter)

    def calculate_routes(self, start_location: GeoLocation,
                         destination_filter: Optional[str] = None) -> List[EvacuationRoute]:
        """Calculate best routes from a starting point to available shelters."""
        usable_routes = [r for r in self.routes if r.is_usable()]

        if destination_filter:
            usable_routes = [r for r in usable_routes
                             if destination_filter in r.end_location.place_name or
                             destination_filter.lower() in str(r.end_location.to_dict()).lower()]

        if self.optimization == "safety_first":
            usable_routes.sort(key=lambda r: (
                list(RouteSafety).index(r.safety_rating),
                -r.available_capacity(),
                r.distance_km
            ))
        elif self.optimization == "shortest_distance":
            usable_routes.sort(key=lambda r: (r.distance_km, r.safety_rating.value))
        elif self.optimization == "fastest":
            usable_routes.sort(key=lambda r: (r.estimated_time_minutes, r.distance_km))
        elif self.optimization == "most_capacity":
            usable_routes.sort(key=lambda r: (-r.available_capacity(), r.safety_rating.value))

        return usable_routes

    def find_nearest_shelter(self, location: GeoLocation) -> Optional[Shelter]:
        """Find the nearest open shelter with available capacity."""
        open_shelters = [s for s in self.shelters
                         if s.status in (ShelterStatus.OPEN, ShelterStatus.STANDBY)
                         and s.available_beds() > 0]
        if not open_shelters:
            return None
        return min(open_shelters, key=lambda s: location.distance_to(s.location))

    def create_evacuation_plan(self, zone_name: str, population_count: int,
                               start_location: GeoLocation) -> Dict[str, Any]:
        """Create a comprehensive evacuation plan for a zone."""
        routes = self.calculate_routes(start_location)
        nearest_shelter = self.find_nearest_shelter(start_location)

        total_route_capacity = sum(r.available_capacity() for r in routes)
        evacuation_batches = max(1, math.ceil(population_count / max(total_route_capacity, 1)))

        plan = {
            "plan_id": f"EVAC-{uuid.uuid4().hex[:8].upper()}",
            "zone_name": zone_name,
            "population_count": population_count,
            "start_location": start_location.to_dict(),
            "available_routes": len(routes),
            "total_route_capacity": total_route_capacity,
            "evacuation_batches": evacuation_batches,
            "estimated_total_time_hours": round(evacuation_batches * 0.5, 1),
            "primary_shelter": nearest_shelter.to_dict() if nearest_shelter else None,
            "route_details": [r.to_dict() for r in routes[:5]],
            "instructions": self._generate_evacuation_instructions(routes, nearest_shelter),
            "created_at": datetime.now().isoformat()
        }
        self.evacuation_plans.append(plan)
        return plan

    def _generate_evacuation_instructions(self, routes: List[EvacuationRoute],
                                          shelter: Optional[Shelter]) -> List[str]:
        """Generate step-by-step evacuation instructions."""
        instructions = []
        if not routes:
            instructions.append("WARNING: No safe evacuation routes currently available.")
            instructions.append("Shelter in place and await emergency services.")
            return instructions

        instructions.append("EVACUATE IMMEDIATELY using designated routes.")
        if routes[0].safety_rating == RouteSafety.RECOMMENDED:
            instructions.append(f"Recommended route: {routes[0].route_id} via {routes[0].road_conditions} roads.")

        if shelter:
            instructions.append(f"Primary shelter: {shelter.name} ({shelter.available_beds()} beds available).")
            if shelter.facilities:
                instructions.append(f"Shelter facilities: {', '.join(shelter.facilities)}.")
        else:
            instructions.append("WARNING: No shelters with available capacity. Proceed to nearest open shelter.")

        instructions.append("Bring essential documents, medications, and emergency supplies.")
        instructions.append("Help neighbors who may need assistance.")
        return instructions

    def update_route_usage(self, route_id: str, usage_change: int) -> bool:
        """Update the current usage of a route."""
        for route in self.routes:
            if route.route_id == route_id:
                route.current_usage = max(0, route.current_usage + usage_change)
                if route.current_usage >= route.capacity:
                    route.safety_rating = RouteSafety.UNSAFE
                return True
        return False

    def get_evacuation_status(self) -> Dict[str, Any]:
        """Get overall evacuation system status."""
        return {
            "total_routes": len(self.routes),
            "usable_routes": sum(1 for r in self.routes if r.is_usable()),
            "total_shelters": len(self.shelters),
            "open_shelters": sum(1 for s in self.shelters if s.status == ShelterStatus.OPEN),
            "total_shelter_capacity": sum(s.capacity for s in self.shelters),
            "total_shelter_occupancy": sum(s.current_occupancy for s in self.shelters),
            "total_evacuation_plans": len(self.evacuation_plans),
            "optimization_mode": self.optimization
        }


# =============================================================================
# Main Demo Function
# =============================================================================

def main() -> None:
    """Demonstrate the disaster response system capabilities."""
    print("=" * 70)
    print("  DISASTER RESPONSE SYSTEM - DEMONSTRATION")
    print("=" * 70)

    # --- Early Warning System ---
    print("\n[1] EARLY WARNING SYSTEM")
    print("-" * 40)
    warning_system = EarlyWarningSystem(sensitivity="high", monitoring_interval_seconds=30)

    # Register sensors
    sensors = [
        ("SENSOR-001", "earthquake", GeoLocation(34.0522, -118.2437, 71, "Los Angeles")),
        ("SENSOR-002", "flood", GeoLocation(29.7604, -95.3698, 15, "Houston")),
        ("SENSOR-003", "hurricane", GeoLocation(25.7617, -80.1918, 2, "Miami")),
    ]
    for sid, stype, loc in sensors:
        warning_system.register_sensor(sid, stype, loc)
        print(f"  Registered sensor: {sid} ({stype}) at {loc.place_name}")

    # Process readings
    print("\n  Processing sensor readings...")
    reading1 = warning_system.process_sensor_reading("SENSOR-001", 6.8)
    if reading1:
        print(f"  ALERT GENERATED: {reading1.level.name} - {reading1.message}")

    reading2 = warning_system.process_sensor_reading("SENSOR-002", 2.5)
    if reading2:
        print(f"  ALERT GENERATED: {reading2.level.name} - {reading2.message}")

    reading3 = warning_system.process_sensor_reading("SENSOR-003", 45)
    if reading3:
        print(f"  ALERT GENERATED: {reading3.level.name} - {reading3.message}")

    print(f"\n  System Status: {json.dumps(warning_system.get_status(), indent=2)}")

    # --- Damage Assessment ---
    print("\n\n[2] DAMAGE ASSESSMENT ENGINE")
    print("-" * 40)
    damage_engine = DamageAssessmentEngine(assessment_type="comprehensive")

    damage_reports = [
        ("EVT-001", GeoLocation(34.0522, -118.2437, 71, "Downtown LA"), DamageLevel.SEVERE,
         {"buildings_damaged": 45, "buildings_destroyed": 12, "casualties": 8, "displaced_persons": 520}),
        ("EVT-001", GeoLocation(34.0480, -118.2550, 65, "Midtown LA"), DamageLevel.MODERATE,
         {"buildings_damaged": 30, "buildings_destroyed": 3, "casualties": 2, "displaced_persons": 180}),
        ("EVT-001", GeoLocation(34.0600, -118.2400, 80, "Hollywood"), DamageLevel.DEVASTATING,
         {"buildings_damaged": 80, "buildings_destroyed": 25, "casualties": 15, "displaced_persons": 1200}),
    ]

    for event_id, loc, level, data in damage_reports:
        report = damage_engine.create_damage_report(event_id, loc, level, **data)
        print(f"  Report {report.report_id}: {level.value} damage, "
              f"{report.buildings_destroyed} destroyed, {report.displaced_persons} displaced")

    print(f"\n  Damage Statistics: {json.dumps(damage_engine.damage_statistics, indent=2)}")

    recovery = damage_engine.estimate_recovery_timeline()
    print(f"\n  Recovery Estimate: {json.dumps(recovery, indent=2)}")

    # --- Resource Coordination ---
    print("\n\n[3] RESOURCE COORDINATION")
    print("-" * 40)
    coordinator = ResourceCoordinator(GeoLocation(34.0522, -118.2437, 71, "LA Coord Center"))

    coordinator.register_agency("AGENCY-001", "Red Cross", "1-800-RED-CROSS", ["medical", "shelter"])
    coordinator.register_agency("AGENCY-002", "UNICEF", "+1-212-326-7000", ["water", "food", "child_protection"])

    resources = [
        Resource("RES-001", "water", 50000, "liters", GeoLocation(34.0600, -118.2500), ResourcePriority.LIFE_SAVING, source_agency="UNICEF"),
        Resource("RES-002", "food", 10000, "meals", GeoLocation(34.0550, -118.2600), ResourcePriority.CRITICAL, source_agency="Red Cross"),
        Resource("RES-003", "medical", 500, "kits", GeoLocation(34.0500, -118.2450), ResourcePriority.HIGH, source_agency="WHO"),
        Resource("RES-004", "blankets", 20000, "units", GeoLocation(34.0650, -118.2350), ResourcePriority.MEDIUM, source_agency="UNHCR"),
        Resource("RES-005", "generators", 25, "units", GeoLocation(34.0450, -118.2550), ResourcePriority.HIGH, source_agency="OCHA"),
    ]
    for res in resources:
        coordinator.register_resource(res)
        print(f"  Registered: {res.resource_type} - {res.quantity} {res.unit} ({res.priority.value})")

    allocations = coordinator.priority_allocation_plan(
        "EVT-001", GeoLocation(34.0522, -118.2437), ["water", "food", "medical"]
    )
    print(f"\n  Priority Allocation Plan ({len(allocations)} items):")
    for alloc in allocations:
        print(f"    - {alloc['resource_type']}: {alloc['quantity_available']} available, "
              f"{alloc['distance_km']}km away [{alloc['recommended_action']}]")

    print(f"\n  Resource Summary: {json.dumps(coordinator.get_resource_summary(), indent=2)}")

    # --- Evacuation Routing ---
    print("\n\n[4] EVACUATION ROUTING")
    print("-" * 40)
    router = EvacuationRouter(optimization="safety_first")

    shelters = [
        Shelter("SHLT-001", "Convention Center", GeoLocation(34.0430, -118.2670), 5000, status=ShelterStatus.OPEN, facilities=["water", "food", "medical", "power"]),
        Shelter("SHLT-002", "Community College", GeoLocation(34.0390, -118.2500), 2000, status=ShelterStatus.OPEN, facilities=["water", "food"]),
        Shelter("SHLT-003", "Sports Arena", GeoLocation(34.0700, -118.2700), 8000, status=ShelterStatus.STANDBY, facilities=["water", "food", "medical", "power", "wifi"]),
    ]
    for shelter in shelters:
        router.add_shelter(shelter)
        print(f"  Shelter: {shelter.name} - Capacity: {shelter.capacity} ({shelter.status.value})")

    routes = [
        EvacuationRoute("ROUTE-001", GeoLocation(34.0522, -118.2437), GeoLocation(34.0430, -118.2670),
                        distance_km=3.2, estimated_time_minutes=15, capacity=2000, safety_rating=RouteSafety.RECOMMENDED),
        EvacuationRoute("ROUTE-002", GeoLocation(34.0522, -118.2437), GeoLocation(34.0390, -118.2500),
                        distance_km=2.1, estimated_time_minutes=10, capacity=1500, safety_rating=RouteSafety.SAFE),
        EvacuationRoute("ROUTE-003", GeoLocation(34.0522, -118.2437), GeoLocation(34.0700, -118.2700),
                        distance_km=4.5, estimated_time_minutes=25, capacity=3000, safety_rating=RouteSafety.MODERATE, road_conditions="partially blocked"),
    ]
    for route in routes:
        router.add_route(route)
        print(f"  Route: {route.route_id} - {route.distance_km}km, {route.capacity} capacity, safety: {route.safety_rating.value}")

    plan = router.create_evacuation_plan("Downtown LA", 3500, GeoLocation(34.0522, -118.2437))
    print(f"\n  Evacuation Plan Created: {plan['plan_id']}")
    print(f"  Population: {plan['population_count']}, Routes: {plan['available_routes']}")
    print(f"  Estimated Time: {plan['estimated_total_time_hours']} hours")
    print(f"  Primary Shelter: {plan['primary_shelter']['name'] if plan['primary_shelter'] else 'None'}")
    print("\n  Instructions:")
    for i, instruction in enumerate(plan['instructions'], 1):
        print(f"    {i}. {instruction}")

    print(f"\n  Evacuation Status: {json.dumps(router.get_evacuation_status(), indent=2)}")

    # --- Summary ---
    print("\n\n" + "=" * 70)
    print("  DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\n  Components demonstrated:")
    print("    1. Early Warning System - sensor monitoring and alert generation")
    print("    2. Damage Assessment - report creation and recovery estimation")
    print("    3. Resource Coordination - registration, allocation, and planning")
    print("    4. Evacuation Routing - route calculation and plan generation")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
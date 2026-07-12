"""
crisis_response.py — Emergency Coordination & Disaster Relief Toolkit

Provides alert systems, resource matching, shelter management, volunteer dispatch,
supply chain logistics, and situational awareness dashboards for crisis scenarios.
"""

from __future__ import annotations

import math
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime, timedelta
from collections import defaultdict


class AlertLevel(Enum):
    ADVISORY = "advisory"
    WATCH = "watch"
    WARNING = "warning"
    EMERGENCY = "emergency"
    EXTREME = "extreme"


class AlertChannel(Enum):
    SMS = "sms"
    PUSH = "push"
    EMAIL = "email"
    SOCIAL_MEDIA = "social_media"
    SIREN = "siren"
    BROADCAST = "broadcast"


class ResourceType(Enum):
    WATER = "water"
    FOOD = "food"
    MEDICAL = "medical"
    SHELTER = "shelter"
    BLANKETS = "blankets"
    HYGIENE = "hygiene"
    FUEL = "fuel"
    COMMUNICATIONS = "communications"


class UrgencyLevel(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class VolunteerStatus(Enum):
    AVAILABLE = "available"
    DEPLOYED = "deployed"
    CHECKED_IN = "checked_in"
    OFF_DUTY = "off_duty"
    UNAVAILABLE = "unavailable"


class IncidentPhase(Enum):
    PREPAREDNESS = "preparedness"
    RESPONSE = "response"
    RECOVERY = "recovery"


@dataclass
class Alert:
    alert_id: str
    title: str
    message: str
    level: AlertLevel
    affected_area: tuple[float, float, float]  # lat, lon, radius_km
    channels: list[AlertChannel]
    languages: list[str]
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: datetime | None = None
    delivered_count: int = 0
    acknowledged_count: int = 0
    active: bool = True


@dataclass
class Resource:
    resource_id: str
    resource_type: ResourceType
    quantity: float
    unit: str
    location: tuple[float, float]
    provider_id: str
    acquired_at: datetime = field(default_factory=datetime.now)
    expires_days: int = 365
    reserved: float = 0.0

    @property
    def available_quantity(self) -> float:
        return max(0, self.quantity - self.reserved)


@dataclass
class ResourceNeed:
    need_id: str
    resource_type: ResourceType
    quantity_needed: float
    location: tuple[float, float]
    requester_id: str
    urgency: UrgencyLevel
    created_at: datetime = field(default_factory=datetime.now)
    fulfilled: float = 0.0

    @property
    def remaining_need(self) -> float:
        return max(0, self.quantity_needed - self.fulfilled)


@dataclass
class Dispatch:
    dispatch_id: str
    resource_type: ResourceType
    quantity: float
    unit: str
    provider_id: str
    requester_id: str
    distance_km: float
    urgency: UrgencyLevel
    dispatched_at: datetime = field(default_factory=datetime.now)


@dataclass
class Shelter:
    shelter_id: str
    name: str
    location: tuple[float, float]
    max_capacity: int
    services: list[str]
    contact_phone: str = ""
    current_occupancy: int = 0
    checked_in: dict[str, int] = field(default_factory=dict)

    @property
    def available_capacity(self) -> int:
        return max(0, self.max_capacity - self.current_occupancy)

    @property
    def utilization(self) -> float:
        return self.current_occupancy / self.max_capacity if self.max_capacity > 0 else 0.0


@dataclass
class Volunteer:
    volunteer_id: str
    name: str
    skills: list[str]
    phone: str
    location: tuple[float, float]
    status: VolunteerStatus = VolunteerStatus.AVAILABLE
    current_assignment: str | None = None
    check_in_time: datetime | None = None
    hours_served: float = 0.0


@dataclass
class SupplyItem:
    item_id: str
    name: str
    resource_type: ResourceType
    quantity: float
    unit: str
    warehouse_id: str
    received_at: datetime = field(default_factory=datetime.now)
    expiration_date: datetime | None = None
    min_reorder_level: float = 0.0

    @property
    def is_expired(self) -> bool:
        if self.expiration_date is None:
            return False
        return datetime.now() > self.expiration_date

    @property
    def needs_reorder(self) -> bool:
        return self.quantity <= self.min_reorder_level


class AlertSystem:
    def __init__(self):
        self.alerts: dict[str, Alert] = []
        self.recipient_db: list[dict] = []

    def create_alert(
        self,
        title: str,
        message: str,
        level: AlertLevel,
        affected_area: tuple[float, float, float],
        channels: list[AlertChannel],
        languages: list[str] | None = None,
        expires_hours: int = 24,
    ) -> Alert:
        alert_id = f"alert_{uuid.uuid4().hex[:8]}"
        alert = Alert(
            alert_id=alert_id,
            title=title,
            message=message,
            level=level,
            affected_area=affected_area,
            channels=channels,
            languages=languages or ["en"],
            expires_at=datetime.now() + timedelta(hours=expires_hours),
        )
        self.alerts.append(alert)
        return alert

    def estimate_recipients(self, affected_area: tuple[float, float, float]) -> int:
        lat, lon, radius_km = affected_area
        area_km2 = math.pi * radius_km ** 2
        estimated_density = 500
        return int(area_km2 * estimated_density)

    def get_active_alerts(self) -> list[Alert]:
        now = datetime.now()
        return [
            a for a in self.alerts
            if a.active and (a.expires_at is None or a.expires_at > now)
        ]

    def acknowledge_alert(self, alert_id: str) -> bool:
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged_count += 1
                return True
        return False

    def get_alert_stats(self) -> dict:
        active = self.get_active_alerts()
        level_counts = defaultdict(int)
        for a in active:
            level_counts[a.level.value] += 1
        return {
            "total_alerts": len(self.alerts),
            "active_alerts": len(active),
            "by_level": dict(level_counts),
            "total_delivered": sum(a.delivered_count for a in self.alerts),
            "total_acknowledged": sum(a.acknowledged_count for a in self.alerts),
        }


class ResourcePool:
    def __init__(self):
        self.resources: list[Resource] = []
        self.needs: list[ResourceNeed] = []
        self.dispatches: list[Dispatch] = []
        self._resource_counter = 0
        self._need_counter = 0

    def add_resource(
        self,
        resource_type: ResourceType,
        quantity: float,
        unit: str,
        location: tuple[float, float],
        provider_id: str,
        expires_days: int = 365,
    ) -> Resource:
        self._resource_counter += 1
        resource = Resource(
            resource_id=f"res_{self._resource_counter}",
            resource_type=resource_type,
            quantity=quantity,
            unit=unit,
            location=location,
            provider_id=provider_id,
            expires_days=expires_days,
        )
        self.resources.append(resource)
        return resource

    def add_need(
        self,
        resource_type: ResourceType,
        quantity_needed: float,
        location: tuple[float, float],
        requester_id: str,
        urgency: UrgencyLevel,
    ) -> ResourceNeed:
        self._need_counter += 1
        need = ResourceNeed(
            need_id=f"need_{self._need_counter}",
            resource_type=resource_type,
            quantity_needed=quantity_needed,
            location=location,
            requester_id=requester_id,
            urgency=urgency,
        )
        self.needs.append(need)
        return need

    def _haversine_km(self, loc1: tuple[float, float], loc2: tuple[float, float]) -> float:
        lat1, lon1 = math.radians(loc1[0]), math.radians(loc1[1])
        lat2, lon2 = math.radians(loc2[0]), math.radians(loc2[1])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return 6371 * 2 * math.asin(math.sqrt(a))

    def match_resources(self, max_distance_km: float = 500.0) -> list[Dispatch]:
        dispatches: list[Dispatch] = []
        urgency_weight = {UrgencyLevel.CRITICAL: 4, UrgencyLevel.HIGH: 3, UrgencyLevel.MEDIUM: 2, UrgencyLevel.LOW: 1}

        for need in sorted(self.needs, key=lambda n: urgency_weight.get(n.urgency, 0), reverse=True):
            if need.remaining_need <= 0:
                continue

            candidates = []
            for resource in self.resources:
                if resource.resource_type != need.resource_type or resource.available_quantity <= 0:
                    continue
                distance = self._haversine_km(resource.location, need.location)
                if distance > max_distance_km:
                    continue
                candidates.append((resource, distance))

            candidates.sort(key=lambda x: x[1])

            for resource, distance in candidates:
                if need.remaining_need <= 0:
                    break
                allocatable = min(resource.available_quantity, need.remaining_need)
                if allocatable <= 0:
                    continue

                dispatch_id = f"disp_{uuid.uuid4().hex[:8]}"
                dispatch = Dispatch(
                    dispatch_id=dispatch_id,
                    resource_type=need.resource_type,
                    quantity=allocatable,
                    unit=resource.unit,
                    provider_id=resource.provider_id,
                    requester_id=need.requester_id,
                    distance_km=round(distance, 2),
                    urgency=need.urgency,
                )
                dispatches.append(dispatch)
                resource.reserved += allocatable
                need.fulfilled += allocatable
                self.dispatches.append(dispatch)

        return dispatches

    def get_inventory_summary(self) -> dict:
        by_type = defaultdict(lambda: {"total": 0, "available": 0, "unit": ""})
        for r in self.resources:
            by_type[r.resource_type.value]["total"] += r.quantity
            by_type[r.resource_type.value]["available"] += r.available_quantity
            by_type[r.resource_type.value]["unit"] = r.unit
        return dict(by_type)


class ShelterManager:
    def __init__(self):
        self.shelters: dict[str, Shelter] = {}

    def register_shelter(self, shelter: Shelter) -> None:
        self.shelters[shelter.shelter_id] = shelter

    def check_in(self, shelter_id: str, person_id: str, members: int = 1) -> bool:
        shelter = self.shelters.get(shelter_id)
        if not shelter:
            return False
        if shelter.available_capacity < members:
            return False
        shelter.checked_in[person_id] = members
        shelter.current_occupancy += members
        return True

    def check_out(self, shelter_id: str, person_id: str) -> bool:
        shelter = self.shelters.get(shelter_id)
        if not shelter or person_id not in shelter.checked_in:
            return False
        members = shelter.checked_in.pop(person_id)
        shelter.current_occupancy = max(0, shelter.current_occupancy - members)
        return True

    def get_status(self, shelter_id: str) -> dict:
        shelter = self.shelters.get(shelter_id)
        if not shelter:
            return {}
        return {
            "shelter_id": shelter.shelter_id,
            "name": shelter.name,
            "occupancy": shelter.current_occupancy,
            "max_capacity": shelter.max_capacity,
            "available": shelter.available_capacity,
            "utilization": shelter.utilization,
            "services": shelter.services,
            "checked_in_groups": len(shelter.checked_in),
        }

    def find_nearest_shelter(
        self,
        location: tuple[float, float],
        required_services: list[str] | None = None,
    ) -> Shelter | None:
        candidates = []
        for shelter in self.shelters.values():
            if shelter.available_capacity <= 0:
                continue
            if required_services:
                if not all(s in shelter.services for s in required_services):
                    continue
            lat1, lon1 = math.radians(location[0]), math.radians(location[1])
            lat2, lon2 = math.radians(shelter.location[0]), math.radians(shelter.location[1])
            dlat, dlon = lat2 - lat1, lon2 - lon1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            dist = 6371 * 2 * math.asin(math.sqrt(a))
            candidates.append((shelter, dist))

        candidates.sort(key=lambda x: x[1])
        return candidates[0][0] if candidates else None

    def get_all_status(self) -> list[dict]:
        return [self.get_status(sid) for sid in self.shelters]


class VolunteerDispatcher:
    def __init__(self):
        self.volunteers: dict[str, Volunteer] = []

    def register_volunteer(self, volunteer: Volunteer) -> None:
        self.volunteers.append(volunteer)

    def deploy(
        self,
        volunteer_id: str,
        assignment: str,
        target_location: tuple[float, float],
    ) -> bool:
        for vol in self.volunteers:
            if vol.volunteer_id == volunteer_id:
                if vol.status != VolunteerStatus.AVAILABLE:
                    return False
                vol.status = VolunteerStatus.DEPLOYED
                vol.current_assignment = assignment
                return True
        return False

    def check_in(self, volunteer_id: str) -> bool:
        for vol in self.volunteers:
            if vol.volunteer_id == volunteer_id and vol.status == VolunteerStatus.DEPLOYED:
                vol.status = VolunteerStatus.CHECKED_IN
                vol.check_in_time = datetime.now()
                return True
        return False

    def check_out(self, volunteer_id: str) -> bool:
        for vol in self.volunteers:
            if vol.volunteer_id == volunteer_id and vol.status == VolunteerStatus.CHECKED_IN:
                vol.status = VolunteerStatus.AVAILABLE
                vol.current_assignment = None
                if vol.check_in_time:
                    vol.hours_served += (datetime.now() - vol.check_in_time).total_seconds() / 3600
                    vol.check_in_time = None
                return True
        return False

    def find_available_by_skill(self, skill: str) -> list[Volunteer]:
        return [
            v for v in self.volunteers
            if v.status == VolunteerStatus.AVAILABLE and skill in v.skills
        ]

    def get_deployment_stats(self) -> dict:
        status_counts = defaultdict(int)
        skill_counts = defaultdict(int)
        total_hours = 0.0

        for v in self.volunteers:
            status_counts[v.status.value] += 1
            for s in v.skills:
                skill_counts[s] += 1
            total_hours += v.hours_served

        return {
            "total_volunteers": len(self.volunteers),
            "by_status": dict(status_counts),
            "by_skill": dict(skill_counts),
            "total_hours_served": round(total_hours, 1),
        }


class SupplyChainManager:
    def __init__(self):
        self.inventory: dict[str, SupplyItem] = {}
        self.distributions: list[dict] = []
        self._item_counter = 0

    def receive_supply(
        self,
        name: str,
        resource_type: ResourceType,
        quantity: float,
        unit: str,
        warehouse_id: str,
        expiration_days: int | None = None,
        min_reorder_level: float = 0.0,
    ) -> SupplyItem:
        self._item_counter += 1
        item_id = f"supply_{self._item_counter}"
        exp_date = datetime.now() + timedelta(days=expiration_days) if expiration_days else None
        item = SupplyItem(
            item_id=item_id,
            name=name,
            resource_type=resource_type,
            quantity=quantity,
            unit=unit,
            warehouse_id=warehouse_id,
            expiration_date=exp_date,
            min_reorder_level=min_reorder_level,
        )
        self.inventory[item_id] = item
        return item

    def distribute(self, item_id: str, quantity: float, destination: str) -> bool:
        item = self.inventory.get(item_id)
        if not item or item.quantity < quantity:
            return False
        item.quantity -= quantity
        self.distributions.append({
            "item_id": item_id,
            "quantity": quantity,
            "destination": destination,
            "timestamp": datetime.now().isoformat(),
        })
        return True

    def get_expiring_soon(self, within_days: int = 30) -> list[SupplyItem]:
        cutoff = datetime.now() + timedelta(days=within_days)
        return [
            item for item in self.inventory.values()
            if item.expiration_date and item.expiration_date <= cutoff and item.quantity > 0
        ]

    def get_reorder_alerts(self) -> list[SupplyItem]:
        return [item for item in self.inventory.values() if item.needs_reorder]

    def get_warehouse_summary(self) -> dict:
        by_warehouse = defaultdict(lambda: {"items": 0, "total_quantity": 0, "types": set()})
        for item in self.inventory.values():
            wh = by_warehouse[item.warehouse_id]
            wh["items"] += 1
            wh["total_quantity"] += item.quantity
            wh["types"].add(item.resource_type.value)
        return {
            wh: {"items": d["items"], "total_quantity": d["total_quantity"], "types": list(d["types"])}
            for wh, d in by_warehouse.items()
        }


class SituationalAwarenessDashboard:
    def __init__(self):
        self.incidents: list[dict] = []
        self.road_conditions: dict[str, str] = {}
        self.weather_data: dict = {}

    def register_incident(
        self,
        title: str,
        location: tuple[float, float],
        severity: AlertLevel,
        description: str = "",
    ) -> str:
        incident_id = f"inc_{uuid.uuid4().hex[:8]}"
        self.incidents.append({
            "incident_id": incident_id,
            "title": title,
            "location": location,
            "severity": severity.value,
            "description": description,
            "reported_at": datetime.now().isoformat(),
            "status": "active",
        })
        return incident_id

    def update_road_condition(self, road_name: str, condition: str) -> None:
        self.road_conditions[road_name] = condition

    def update_weather(self, data: dict) -> None:
        self.weather_data = data

    def get_dashboard_summary(self) -> dict:
        severity_counts = defaultdict(int)
        for inc in self.incidents:
            if inc["status"] == "active":
                severity_counts[inc["severity"]] += 1

        blocked_roads = sum(1 for c in self.road_conditions.values() if "blocked" in c.lower())

        return {
            "active_incidents": sum(severity_counts.values()),
            "incidents_by_severity": dict(severity_counts),
            "blocked_roads": blocked_roads,
            "total_roads_monitored": len(self.road_conditions),
            "weather_status": self.weather_data.get("condition", "unknown"),
            "last_updated": datetime.now().isoformat(),
        }


def main() -> None:
    print("=== Crisis Response Demo ===\n")

    # 1. Alert System
    print("--- Alert System ---")
    alerts = AlertSystem()
    alert = alerts.create_alert(
        title="Flash Flood Warning",
        message="Seek higher ground immediately in Riverside County.",
        level=AlertLevel.EXTREME,
        affected_area=(33.78, -117.85, 5.0),
        channels=[AlertChannel.SMS, AlertChannel.PUSH],
        languages=["en", "es"],
        expires_hours=6,
    )
    est = alerts.estimate_recipients(alert.affected_area)
    print(f"  Alert: {alert.title} (Level: {alert.level.value})")
    print(f"  Est. recipients: {est:,}")
    alerts.acknowledge_alert(alert.alert_id)
    print(f"  Stats: {alerts.get_alert_stats()}")

    # 2. Resource Matching
    print("\n--- Resource Matching ---")
    pool = ResourcePool()
    pool.add_resource(ResourceType.WATER, 1000, "bottles", (34.05, -118.25), "red_cross")
    pool.add_resource(ResourceType.FOOD, 500, "meals", (34.06, -118.26), "food_bank")
    pool.add_need(ResourceType.WATER, 200, (34.05, -118.27), "shelter_01", UrgencyLevel.CRITICAL)
    pool.add_need(ResourceType.FOOD, 100, (34.06, -118.25), "shelter_02", UrgencyLevel.HIGH)
    dispatches = pool.match_resources()
    for d in dispatches:
        print(f"  Dispatch: {d.quantity} {d.resource_type.value} → {d.requester_id} ({d.distance_km}km)")
    print(f"  Inventory: {pool.get_inventory_summary()}")

    # 3. Shelter Management
    print("\n--- Shelter Management ---")
    sm = ShelterManager()
    sm.register_shelter(Shelter("s1", "Lincoln High", (34.06, -118.24), 200, ["medical", "pets"], "555-0101"))
    sm.register_shelter(Shelter("s2", "Riverside Center", (34.07, -118.25), 150, ["medical"], "555-0102"))
    sm.check_in("s1", "family_1", 4)
    sm.check_in("s1", "family_2", 6)
    print(f"  Lincoln High: {sm.get_status('s1')}")
    nearest = sm.find_nearest_shelter((34.05, -118.24), ["pets"])
    print(f"  Nearest with pets: {nearest.name if nearest else 'None'}")

    # 4. Volunteer Dispatch
    print("\n--- Volunteer Dispatch ---")
    vd = VolunteerDispatcher()
    vd.register_volunteer(Volunteer("v1", "Maria Garcia", ["medical", "translation"], "555-1001", (34.05, -118.25)))
    vd.register_volunteer(Volunteer("v2", "James Smith", ["logistics", "driving"], "555-1002", (34.06, -118.26)))
    vd.deploy("v1", "Medical triage at Lincoln High", (34.06, -118.24))
    vd.check_in("v1")
    print(f"  Medical volunteers: {len(vd.find_available_by_skill('medical'))}")
    print(f"  Deployment stats: {vd.get_deployment_stats()}")

    # 5. Supply Chain
    print("\n--- Supply Chain ---")
    scm = SupplyChainManager()
    scm.receive_supply("Bottled Water", ResourceType.WATER, 5000, "cases", "warehouse_1", expiration_days=365, min_reorder_level=500)
    scm.receive_supply("MREs", ResourceType.FOOD, 2000, "cases", "warehouse_1", expiration_days=730, min_reorder_level=200)
    scm.distribute("supply_1", 500, "shelter_01")
    print(f"  Warehouse summary: {scm.get_warehouse_summary()}")
    print(f"  Reorder alerts: {[i.name for i in scm.get_reorder_alerts()]}")

    # 6. Situational Awareness
    print("\n--- Situational Awareness ---")
    dash = SituationalAwarenessDashboard()
    dash.register_incident("Structure Fire", (34.05, -118.25), AlertLevel.EMERGENCY, "3-alarm fire downtown")
    dash.register_incident("Power Outage", (34.07, -118.26), AlertLevel.WARNING, "5000 homes without power")
    dash.update_road_condition("Main St", "Blocked — fire response")
    dash.update_road_condition("Oak Ave", "Open with delays")
    dash.update_weather({"condition": "Clear", "temp_f": 72, "wind_mph": 5})
    summary = dash.get_dashboard_summary()
    print(f"  Active incidents: {summary['active_incidents']}")
    print(f"  Blocked roads: {summary['blocked_roads']}")
    print(f"  Weather: {summary['weather_status']}")


if __name__ == "__main__":
    main()

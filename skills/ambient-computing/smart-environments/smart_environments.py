"""
Smart Environments Module — Building management, HVAC control, intelligent lighting,
access control, energy monitoring, and fault detection for smart buildings.
"""

from __future__ import annotations

import json
import math
import random
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class BuildingProtocol(Enum):
    BACNET = "bacnet"
    KNX = "knx"
    MODBUS = "modbus"
    LONWORKS = "lonworks"
    OPCUA = "opc_ua"
    ZIGBEE = "zigbee"


class HVACMode(Enum):
    HEAT = "heat"
    COOL = "cool"
    AUTO = "auto"
    FAN = "fan"
    OFF = "off"
    EMERGENCY_HEAT = "emergency_heat"


class LightingScene(Enum):
    BRIGHT = "bright"
    NORMAL = "normal"
    DIM = "dim"
    FOCUS = "focus_work"
    MEETING = "meeting"
    PRESENTATION = "presentation"
    CLEANING = "cleaning"
    NIGHT = "night"
    VACANT = "vacant"


class AccessLevel(Enum):
    RESTRICTED = "restricted"
    EMPLOYEES = "employees"
    VISITORS = "visitors"
    PUBLIC = "public"
    EMERGENCY = "emergency"


class FaultSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class EnergySource(Enum):
    GRID = "grid"
    SOLAR = "solar"
    BATTERY = "battery"
    GENERATOR = "generator"
    WIND = "wind"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Zone:
    """A managed zone within a building."""
    zone_id: str
    name: str
    floor: int = 1
    area_sqft: float = 1000
    occupancy_capacity: int = 20
    current_occupancy: int = 0
    hvac_zone: str = ""
    lighting_zone: str = ""
    access_group: str = "employees"
    temperature_f: float = 72.0
    target_temperature_f: float = 72.0
    humidity_pct: float = 45.0
    co2_ppm: int = 600
    light_lux: float = 300
    is_occupied: bool = False
    comfort_score: float = 85.0

    @property
    def occupancy_pct(self) -> float:
        return (self.current_occupancy / self.occupancy_capacity * 100) if self.occupancy_capacity > 0 else 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zone_id": self.zone_id,
            "name": self.name,
            "floor": self.floor,
            "occupancy": f"{self.current_occupancy}/{self.occupancy_capacity}",
            "temp_f": round(self.temperature_f, 1),
            "target_f": self.target_temperature_f,
            "humidity": round(self.humidity_pct, 1),
            "comfort": round(self.comfort_score, 1),
        }


@dataclass
class HVACState:
    """Current state of an HVAC unit."""
    unit_id: str
    mode: HVACMode = HVACMode.AUTO
    setpoint_f: float = 72.0
    actual_f: float = 72.0
    fan_speed_pct: int = 50
    is_running: bool = True
    filter_status: str = "good"
    runtime_hours: float = 0
    power_kw: float = 5.0
    supply_air_temp_f: float = 55.0
    return_air_temp_f: float = 72.0
    outside_air_pct: float = 20.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "unit_id": self.unit_id,
            "mode": self.mode.value,
            "setpoint": self.setpoint_f,
            "actual": round(self.actual_f, 1),
            "fan_speed": self.fan_speed_pct,
            "running": self.is_running,
            "power_kw": round(self.power_kw, 2),
        }


@dataclass
class LightingState:
    """Current state of a lighting zone."""
    zone_id: str
    scene: LightingScene = LightingScene.NORMAL
    brightness_pct: int = 100
    color_temp_k: int = 4000
    daylight_harvesting: bool = False
    target_lux: int = 300
    actual_lux: float = 300
    dimmers_on: int = 0
    power_w: float = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zone_id": self.zone_id,
            "scene": self.scene.value,
            "brightness": self.brightness_pct,
            "color_temp_k": self.color_temp_k,
            "actual_lux": round(self.actual_lux, 0),
        }


@dataclass
class AccessEvent:
    """An access control event."""
    event_id: str
    card_id: str
    reader_id: str
    zone_id: str
    granted: bool
    access_level: AccessLevel
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    person_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "reader": self.reader_id,
            "granted": self.granted,
            "level": self.access_level.value,
        }


@dataclass
class EnergyReading:
    """An energy consumption reading."""
    timestamp: str
    total_kw: float
    hvac_kw: float
    lighting_kw: float
    plug_load_kw: float
    renewable_kw: float = 0.0
    grid_kw: float = 0.0
    cost_usd: float = 0.0
    carbon_kg: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp,
            "total_kw": round(self.total_kw, 2),
            "hvac_kw": round(self.hvac_kw, 2),
            "lighting_kw": round(self.lighting_kw, 2),
            "cost_usd": round(self.cost_usd, 2),
        }


@dataclass
class FaultDetection:
    """A detected fault in building systems."""
    fault_id: str
    system: str
    equipment_id: str
    fault_type: str
    severity: FaultSeverity
    description: str
    detected_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    recommended_action: str = ""
    estimated_cost_impact: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "fault_id": self.fault_id,
            "system": self.system,
            "equipment": self.equipment_id,
            "type": self.fault_type,
            "severity": self.severity.value,
            "description": self.description,
        }


@dataclass
class DemandResponseEvent:
    """A demand response event."""
    event_id: str
    signal_type: str  # "price", "emergency", "grid"
    reduction_target_kw: float
    duration_minutes: int
    start_time: str
    status: str = "pending"
    actual_reduction_kw: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "signal": self.signal_type,
            "target_kw": round(self.reduction_target_kw, 1),
            "duration_min": self.duration_minutes,
            "status": self.status,
        }


@dataclass
class BuildingStatus:
    """Overall building status summary."""
    name: str
    total_zones: int = 0
    active_zones: int = 0
    occupants: int = 0
    comfort_score: float = 0
    energy_score: float = 0
    demand_kw: float = 0
    faults_active: int = 0
    hvac_units: int = 0
    lighting_zones: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "zones": f"{self.active_zones}/{self.total_zones}",
            "occupants": self.occupants,
            "comfort": round(self.comfort_score, 1),
            "energy_score": round(self.energy_score, 1),
            "demand_kw": round(self.demand_kw, 1),
            "faults": self.faults_active,
        }


# ---------------------------------------------------------------------------
# Core classes
# ---------------------------------------------------------------------------

class HVACController:
    """HVAC system controller with demand response and optimization."""

    def __init__(self, building: "BuildingManager"):
        self.building = building
        self._units: Dict[str, HVACState] = {}
        self._schedules: Dict[str, Dict[str, Any]] = {}
        self._demand_response_enabled = False
        self._max_reduction_pct = 0.0

    def add_unit(self, unit_id: str) -> HVACState:
        unit = HVACState(unit_id=unit_id)
        self._units[unit_id] = unit
        return unit

    def set_setpoint(self, zone_id: str, temperature_f: float = 72.0,
                     humidity_pct: float = 45.0) -> None:
        zone = self.building._zones.get(zone_id)
        if zone:
            zone.target_temperature_f = temperature_f
            zone.humidity_pct = humidity_pct

    def set_schedule(self, zone_id: str, schedule: Dict[str, Any]) -> None:
        self._schedules[zone_id] = schedule

    def enable_demand_response(self, max_reduction_pct: float = 20.0) -> None:
        self._demand_response_enabled = True
        self._max_reduction_pct = max_reduction_pct

    def process_demand_response(self, event: DemandResponseEvent) -> float:
        if not self._demand_response_enabled:
            return 0.0
        total_reduction = 0.0
        for unit in self._units.values():
            if unit.is_running and unit.mode in (HVACMode.COOL, HVACMode.HEAT):
                reduction = unit.power_kw * (self._max_reduction_pct / 100)
                total_reduction += reduction
                unit.setpoint_f += 2 if unit.mode == HVACMode.COOL else -2
        event.actual_reduction_kw = total_reduction
        event.status = "executed"
        return total_reduction

    def get_all_states(self) -> List[HVACState]:
        return list(self._units.values())

    def auto_adjust(self) -> Dict[str, Any]:
        adjustments = {}
        for zone_id, zone in self.building._zones.items():
            if zone.is_occupied:
                diff = zone.target_temperature_f - zone.temperature_f
                if abs(diff) > 1:
                    adjustments[zone_id] = {"adjustment": "setpoint_change", "delta": round(diff * 0.5, 1)}
        return adjustments


class LightingController:
    """Intelligent lighting control with daylight harvesting and scenes."""

    def __init__(self, building: "BuildingManager"):
        self.building = building
        self._zones: Dict[str, LightingState] = {}
        self._circadian_schedules: Dict[str, List[Dict[str, Any]]] = {}

    def add_zone(self, zone_id: str) -> LightingState:
        zone = LightingState(zone_id=zone_id)
        self._zones[zone_id] = zone
        return zone

    def set_scene(self, zone_id: str, scene: str, params: Optional[Dict[str, Any]] = None) -> None:
        zone = self._zones.get(zone_id)
        if zone:
            zone.scene = LightingScene(scene) if scene in [s.value for s in LightingScene] else LightingScene.NORMAL
            if params:
                zone.brightness_pct = params.get("brightness", zone.brightness_pct)
                zone.color_temp_k = params.get("color_temp_k", zone.color_temp_k)

    def enable_daylight_harvesting(self, zone_id: str, target_lux: int = 300) -> None:
        zone = self._zones.get(zone_id)
        if zone:
            zone.daylight_harvesting = True
            zone.target_lux = target_lux

    def enable_circadian(self, zone_id: str, schedule: str = "office") -> None:
        self._circadian_schedules[zone_id] = [
            {"time": "06:00", "color_temp_k": 3000, "brightness": 40},
            {"time": "09:00", "color_temp_k": 5000, "brightness": 80},
            {"time": "14:00", "color_temp_k": 4500, "brightness": 75},
            {"time": "18:00", "color_temp_k": 3500, "brightness": 60},
            {"time": "21:00", "color_temp_k": 2700, "brightness": 30},
        ]

    def auto_adjust(self, daylight_lux: float = 0) -> Dict[str, Any]:
        adjustments = {}
        for zone_id, zone in self._zones.items():
            if zone.daylight_harvesting and daylight_lux > 0:
                target = zone.target_lux
                if daylight_lux >= target:
                    zone.brightness_pct = max(10, int((target / daylight_lux) * 100))
                    adjustments[zone_id] = {"brightness": zone.brightness_pct, "reason": "daylight_harvesting"}
        return adjustments

    def get_all_states(self) -> List[LightingState]:
        return list(self._zones.values())


class AccessControl:
    """Access control system management."""

    def __init__(self):
        self._credentials: Dict[str, AccessLevel] = {}
        self._events: List[AccessEvent] = []
        self._lockdown_active = False

    def register_credential(self, card_id: str, level: AccessLevel) -> None:
        self._credentials[card_id] = level

    def authenticate(self, card_id: str, reader_id: str, zone_id: str) -> AccessEvent:
        level = self._credentials.get(card_id, AccessLevel.RESTRICTED)
        granted = not self._lockdown_active and level in (AccessLevel.EMPLOYEES, AccessLevel.PUBLIC, AccessLevel.VISITORS)
        event = AccessEvent(
            event_id=f"ACC-{uuid.uuid4().hex[:8].upper()}",
            card_id=card_id,
            reader_id=reader_id,
            zone_id=zone_id,
            granted=granted,
            access_level=level,
        )
        self._events.append(event)
        return event

    def initiate_lockdown(self) -> None:
        self._lockdown_active = True

    def release_lockdown(self) -> None:
        self._lockdown_active = False

    def get_events(self, limit: int = 50) -> List[AccessEvent]:
        return self._events[-limit:]


class EnergyMonitor:
    """Real-time energy monitoring and management."""

    def __init__(self, building: "BuildingManager"):
        self.building = building
        self._readings: List[EnergyReading] = []
        self._rate_per_kwh = 0.12
        self._carbon_factor = 0.42  # kg CO2 per kWh

    def start_monitoring(self) -> None:
        for i in range(24):
            reading = EnergyReading(
                timestamp=f"2024-01-01T{i:02d}:00:00",
                total_kw=random.uniform(100, 300),
                hvac_kw=random.uniform(40, 120),
                lighting_kw=random.uniform(20, 60),
                plug_load_kw=random.uniform(30, 80),
                renewable_kw=random.uniform(0, 20),
            )
            reading.grid_kw = max(0, reading.total_kw - reading.renewable_kw)
            reading.cost_usd = reading.grid_kw * self._rate_per_kwh
            reading.carbon_kg = reading.grid_kw * self._carbon_factor
            self._readings.append(reading)

    def get_dashboard(self) -> Dict[str, Any]:
        if not self._readings:
            return {}
        latest = self._readings[-1]
        total_kwh = sum(r.total_kw for r in self._readings)
        total_cost = sum(r.cost_usd for r in self._readings)
        peak_kw = max(r.total_kw for r in self._readings)
        return {
            "demand_kw": latest.total_kw,
            "today_kwh": total_kwh,
            "peak_kw": peak_kw,
            "cost_usd": total_cost,
            "hvac_pct": round(latest.hvac_kw / latest.total_kw * 100, 1) if latest.total_kw > 0 else 0,
            "renewable_pct": round(latest.renewable_kw / latest.total_kw * 100, 1) if latest.total_kw > 0 else 0,
            "carbon_kg": round(sum(r.carbon_kg for r in self._readings), 1),
        }


class FaultDetector:
    """Automated fault detection and diagnostics."""

    def __init__(self):
        self._faults: List[FaultDetection] = []
        self._rules: List[Dict[str, Any]] = []

    def add_rule(self, name: str, condition: str, severity: FaultSeverity, action: str) -> None:
        self._rules.append({"name": name, "condition": condition, "severity": severity, "action": action})

    def analyze(self, hvac_states: List[HVACState], zone_temps: Dict[str, float]) -> List[FaultDetection]:
        faults = []
        for unit in hvac_states:
            if unit.is_running:
                # Check for supply/return temperature差
                delta = unit.return_air_temp_f - unit.supply_air_temp_f
                if delta < 10:
                    faults.append(FaultDetection(
                        fault_id=f"FLT-{uuid.uuid4().hex[:8].upper()}",
                        system="hvac",
                        equipment_id=unit.unit_id,
                        fault_type="low_delta_t",
                        severity=FaultSeverity.WARNING,
                        description=f"Low temperature differential ({delta:.1f}°F) — possible low airflow or failed valve",
                        recommended_action="Check air filter, verify valve operation",
                    ))
                # Check filter status
                if unit.runtime_hours > 2000:
                    faults.append(FaultDetection(
                        fault_id=f"FLT-{uuid.uuid4().hex[:8].upper()}",
                        system="hvac",
                        equipment_id=unit.unit_id,
                        fault_type="filter_overdue",
                        severity=FaultSeverity.INFO,
                        description=f"Filter replacement overdue ({unit.runtime_hours:.0f}h runtime)",
                        recommended_action="Schedule filter replacement",
                    ))
        self._faults.extend(faults)
        return faults


class BuildingManager:
    """Main building management system."""

    def __init__(self, name: str, floors: int = 1, total_area_sqft: float = 10000,
                 bms_protocol: str = "bacnet"):
        self.name = name
        self.floors = floors
        self.total_area_sqft = total_area_sqft
        self.bms_protocol = BuildingProtocol(bms_protocol)
        self._zones: Dict[str, Zone] = {}
        self._hvac = HVACController(self)
        self._lighting = LightingController(self)
        self._access = AccessControl()
        self._energy = EnergyMonitor(self)
        self._fault_detector = FaultDetector()

    def add_zone(self, zone: Zone) -> None:
        self._zones[zone.zone_id] = zone

    def get_status(self) -> BuildingStatus:
        active = sum(1 for z in self._zones.values() if z.is_occupied)
        total_occ = sum(z.current_occupancy for z in self._zones.values())
        avg_comfort = (sum(z.comfort_score for z in self._zones.values()) / len(self._zones)
                      if self._zones else 0)
        return BuildingStatus(
            name=self.name,
            total_zones=len(self._zones),
            active_zones=active,
            occupants=total_occ,
            comfort_score=avg_comfort,
            energy_score=random.uniform(70, 95),
            demand_kw=random.uniform(100, 300),
            faults_active=len(self._fault_detector._faults),
            hvac_units=len(self._hvac._units),
            lighting_zones=len(self._lighting._zones),
        )

    @property
    def hvac(self) -> HVACController:
        return self._hvac

    @property
    def lighting(self) -> LightingController:
        return self._lighting

    @property
    def access(self) -> AccessControl:
        return self._access

    @property
    def energy(self) -> EnergyMonitor:
        return self._energy

    @property
    def fault_detector(self) -> FaultDetector:
        return self._fault_detector


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the smart environment building management system."""
    print("Smart Environment Building Manager")
    print("=" * 60)

    building = BuildingManager(name="HQ", floors=5, total_area_sqft=100000, bms_protocol="bacnet")

    # Add zones
    building.add_zone(Zone(zone_id="floor3", name="Floor 3 Open", floor=3,
                          area_sqft=8000, occupancy_capacity=40, current_occupancy=25,
                          is_occupied=True))
    building.add_zone(Zone(zone_id="conference", name="Conference Room", floor=3,
                          area_sqft=500, occupancy_capacity=20, current_occupancy=8,
                          is_occupied=True))

    # HVAC
    building.hvac.add_unit("AHU-3")
    building.hvac.set_setpoint("floor3", temperature_f=72, humidity_pct=45)
    building.hvac.enable_demand_response(max_reduction_pct=20)
    print("HVAC configured")

    # Lighting
    building.lighting.add_zone("floor3")
    building.lighting.enable_daylight_harvesting("floor3", target_lux=300)
    building.lighting.set_scene("floor3", "focus_work", {"brightness": 80})
    building.lighting.enable_circadian("floor3")
    print("Lighting configured")

    # Energy
    building.energy.start_monitoring()
    dashboard = building.energy.get_dashboard()
    print(f"\nEnergy: {dashboard['demand_kw']:.1f}kW demand, ${dashboard['cost_usd']:.2f} cost")

    # Fault detection
    faults = building.fault_detector.analyze(building.hvac.get_all_states(), {})
    print(f"Faults detected: {len(faults)}")
    for f in faults:
        print(f"  [{f.severity.value}] {f.description}")

    # Building status
    status = building.get_status()
    print(f"\nBuilding: {status.name}")
    print(f"  Zones: {status.active_zones}/{status.total_zones}")
    print(f"  Occupants: {status.occupants}")
    print(f"  Comfort: {status.comfort_score:.1f}/100")
    print(f"  Energy score: {status.energy_score:.1f}/100")


if __name__ == "__main__":
    main()

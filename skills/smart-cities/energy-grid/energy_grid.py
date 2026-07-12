"""
Energy Grid Module — Smart City Power Management Platform

Provides comprehensive smart grid management for urban power distribution,
renewable energy integration, demand-side management, and grid resilience.
Monitors distribution from substations to smart meters with real-time
visibility into power quality, load, outages, and consumption.

Domain: Smart Cities > Energy Grid
"""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EngineStatus(Enum):
    """Operational state of the energy grid engine."""
    UNINITIALIZED = auto()
    CONFIGURING = auto()
    READY = auto()
    RUNNING = auto()
    ERROR = auto()
    SHUTDOWN = auto()


class VoltageLevel(Enum):
    """Distribution voltage levels in kV."""
    LV_4160 = 4.16
    MV_13800 = 13.8
    MV_23000 = 23.0
    MV_34500 = 34.5
    HV_69000 = 69.0
    HV_138000 = 138.0


class OutageSeverity(Enum):
    """Outage severity classification."""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"


class OutageCause(Enum):
    """Root causes for power outages."""
    VEGETATION = "vegetation"
    EQUIPMENT_FAILURE = "equipment_failure"
    VEHICLE_ACCIDENT = "vehicle_accident"
    WEATHER = "weather"
    ANIMAL_CONTACT = "animal_contact"
    CONSTRUCTION_DAMAGE = "construction_damage"
    UNKNOWN = "unknown"


class DERType(Enum):
    """Distributed energy resource types."""
    ROOFTOP_SOLAR = "rooftop_solar"
    BATTERY_STORAGE = "battery_storage"
    EV_CHARGER = "ev_charger"
    SMALL_WIND = "small_wind"
    FUEL_CELL = "fuel_cell"
    GENERATOR = "generator"


class DRProgram(Enum):
    """Demand response program types."""
    CAPACITY_BID = "capacity_bid"
    ENERGY_BID = "energy_bid"
    ancillary_services = "ancillary_services"
    TIME_OF_USE = "time_of_use"
    CRITICAL_PEAK = "critical_peak"


class PQEventType(Enum):
    """Power quality event types."""
    VOLTAGE_SAG = "voltage_sag"
    VOLTAGE_SWELL = "voltage_swell"
    HARMONIC = "harmonic"
    FLICKER = "flicker"
    TRANSIENT = "transient"
    FREQUENCY_DEVIATION = "frequency_deviation"


class DimmingProfile(Enum):
    """Streetlight dimming profiles."""
    FIXED = "fixed"
    SCHEDULED = "scheduled"
    ADAPTIVE = "adaptive"
    PHOTOCELL = "photocell"


class MeterStatus(Enum):
    """Smart meter operational status."""
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"
    DECOMMISSIONED = "decommissioned"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class GridConfig:
    """Configuration for the power grid model."""
    voltage_levels_kv: List[float] = field(default_factory=lambda: [13.8, 34.5])
    substations: int = 0
    feeders: int = 0
    smart_meters: int = 0
    distributed_solar_mw: float = 0.0
    battery_storage_mw: float = 0.0
    ev_chargers: int = 0

    def validate(self) -> bool:
        if self.substations < 1:
            raise ValueError("Must have at least 1 substation")
        if self.feeders < 1:
            raise ValueError("Must have at least 1 feeder")
        return True


@dataclass
class AMIConfig:
    """Advanced Metering Infrastructure configuration."""
    read_interval_minutes: int = 15
    data_retention_years: int = 3
    net_metering_enabled: bool = True
    demand_charge_tiers: int = 4
    encryption_enabled: bool = True


@dataclass
class Transformer:
    """Distribution transformer."""
    transformer_id: str
    name: str
    rated_kva: float
    primary_voltage_kv: float
    secondary_voltage_kv: float
    current_load_kw: float = 0.0

    @property
    def loading_pct(self) -> float:
        if self.rated_kva <= 0:
            return 0.0
        return (self.current_load_kw / self.rated_kva) * 100.0


@dataclass
class Feeder:
    """Distribution feeder."""
    feeder_id: str
    name: str
    substation_id: str
    voltage_kv: float
    length_km: float
    total_load_mw: float = 0.0
    der_penetration_pct: float = 0.0
    transformers: List[Transformer] = field(default_factory=list)


@dataclass
class SmartMeter:
    """Smart meter device."""
    meter_id: str
    customer_id: str
    address: str
    rated_amps: int = 200
    status: MeterStatus = MeterStatus.ONLINE
    install_date: Optional[datetime] = None
    last_read: Optional[datetime] = None
    net_metering: bool = False


@dataclass
class IntervalReading:
    """Smart meter interval reading."""
    meter_id: str
    timestamp: datetime
    kwh_import: float
    kwh_export: float
    kw_demand: float
    voltage: float


@dataclass
class DREvent:
    """Demand response event."""
    event_id: str
    program: DRProgram
    event_type: str
    start_time: datetime
    end_time: datetime
    target_reduction_mw: float
    enrolled_capacity_mw: float = 0.0
    expected_reduction_mw: float = 0.0


@dataclass
class DREventVerification:
    """Post-event verification result."""
    event_id: str
    actual_reduction_mw: float
    baseline_mw: float
    status: str
    verification_method: str = "10_of_10"


@dataclass
class Outage:
    """Power outage record."""
    outage_id: str
    cause: OutageCause
    severity: OutageSeverity
    fault_location: str
    latitude: float
    longitude: float
    customers_affected: int
    crew_id: Optional[str] = None
    eta_restoration: Optional[str] = None
    detected_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class FLISRResult:
    """FLISR operation result."""
    fault_id: str
    restored_customers: int
    remaining_affected: int
    sections_isolated: int
    alternate_feed_used: bool


@dataclass
class PQEvent:
    """Power quality event record."""
    event_id: str
    event_type: PQEventType
    timestamp: datetime
    substation_id: str
    magnitude: float
    duration_ms: float
    root_cause: str = ""
    equipment_affected: List[str] = field(default_factory=list)


@dataclass
class Streetlight:
    """Smart streetlight fixture."""
    fixture_id: str
    pole_id: str
    wattage: int
    dimming_pct: float = 100.0
    online: bool = True
    energy_kwh_today: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0


@dataclass
class StreetlightZone:
    """A zone of streetlights with a dimming profile."""
    zone_id: str
    name: str
    profile: DimmingProfile
    fixture_count: int
    base_dimming_pct: float = 30.0
    motion_boost_pct: float = 100.0
    curfew_dimming_pct: float = 20.0


@dataclass
class StreetlightEnergyReport:
    """Energy report for a streetlight zone."""
    zone_id: str
    period_days: int
    consumption_kwh: float
    cost_savings: float
    co2_reduction_kg: float
    faults_detected: int


# ---------------------------------------------------------------------------
# Helper Classes
# ---------------------------------------------------------------------------

class GridStateMonitor:
    """Monitors real-time distribution grid state."""

    def __init__(self, engine: "EnergyGridEngine") -> None:
        self._engine = engine

    def get_feeder_status(
        self,
        feeder_id: str,
        include_transformer_loading: bool = True,
        include_voltage_profile: bool = False,
    ) -> Optional[Feeder]:
        return self._engine._feeders.get(feeder_id)

    def get_substation_summary(self, substation_id: str) -> Dict[str, Any]:
        feeders = [
            f for f in self._engine._feeders.values()
            if f.substation_id == substation_id
        ]
        total_load = sum(f.total_load_mw for f in feeders)
        return {
            "substation_id": substation_id,
            "feeder_count": len(feeders),
            "total_load_mw": round(total_load, 2),
            "avg_der_penetration": round(
                sum(f.der_penetration_pct for f in feeders) / max(len(feeders), 1), 1
            ),
        }


class DemandResponseOrchestrator:
    """Manages demand response events and verification."""

    def __init__(self, engine: "EnergyGridEngine") -> None:
        self._engine = engine
        self._active_events: Dict[str, DREvent] = {}

    def create_event(
        self,
        program: DRProgram,
        event_type: str,
        start_time: str,
        end_time: str,
        target_reduction_mw: float,
        commitment_window_hours: int = 4,
    ) -> DREvent:
        event = DREvent(
            event_id=f"dre-{uuid.uuid4().hex[:8]}",
            program=program,
            event_type=event_type,
            start_time=datetime.fromisoformat(start_time),
            end_time=datetime.fromisoformat(end_time),
            target_reduction_mw=target_reduction_mw,
            enrolled_capacity_mw=target_reduction_mw * 1.1,
            expected_reduction_mw=target_reduction_mw * 0.95,
        )
        self._active_events[event.event_id] = event
        logger.info("DR Event created: %s targeting %.1f MW", event.event_id, target_reduction_mw)
        return event

    def verify_event(self, event_id: str) -> DREventVerification:
        event = self._active_events.get(event_id)
        if event is None:
            raise KeyError(f"DR event not found: {event_id}")

        import random
        random.seed(hash(event_id) % 2**31)
        actual = event.target_reduction_mw * random.uniform(0.85, 1.05)
        baseline = event.target_reduction_mw * random.uniform(1.2, 1.5)

        return DREventVerification(
            event_id=event_id,
            actual_reduction_mw=round(actual, 2),
            baseline_mw=round(baseline, 2),
            status="verified" if actual >= event.target_reduction_mw * 0.9 else "shortfall",
        )


class OutageManager:
    """Detects and manages power outages with FLISR."""

    def __init__(self, engine: "EnergyGridEngine") -> None:
        self._engine = engine
        self._active_outages: Dict[str, Outage] = {}

    def get_active_outages(
        self,
        severity: Optional[OutageSeverity] = None,
        include_customers_affected: bool = True,
    ) -> List[Outage]:
        outages = list(self._active_outages.values())
        if severity:
            outages = [o for o in outages if o.severity == severity]
        return outages

    def register_outage(self, outage: Outage) -> None:
        self._active_outages[outage.outage_id] = outage
        logger.warning(
            "Outage %s: %d customers affected at %s",
            outage.outage_id, outage.customers_affected, outage.fault_location,
        )

    def initiate_flisr(
        self,
        fault_id: str,
        auto_isolate: bool = True,
        restore_from_alternate_feed: bool = True,
    ) -> FLISRResult:
        outage = self._active_outages.get(fault_id)
        if outage is None:
            raise KeyError(f"Outage not found: {fault_id}")

        restored = int(outage.customers_affected * 0.7) if restore_from_alternate_feed else 0
        remaining = outage.customers_affected - restored

        return FLISRResult(
            fault_id=fault_id,
            restored_customers=restored,
            remaining_affected=remaining,
            sections_isolated=2 if auto_isolate else 0,
            alternate_feed_used=restore_from_alternate_feed,
        )


class StreetlightManager:
    """Manages smart streetlight infrastructure."""

    def __init__(self, engine: "EnergyGridEngine") -> None:
        self._engine = engine
        self._zones: Dict[str, StreetlightZone] = {}

    def set_dimming_profile(
        self,
        zone_id: str,
        profile: DimmingProfile,
        parameters: Optional[Dict[str, Any]] = None,
    ) -> StreetlightZone:
        if parameters is None:
            parameters = {}

        zone = StreetlightZone(
            zone_id=zone_id,
            name=zone_id,
            profile=profile,
            fixture_count=0,
            base_dimming_pct=parameters.get("base_dimming_pct", 30),
            motion_boost_pct=parameters.get("motion_boost_pct", 100),
            curfew_dimming_pct=parameters.get("curfew_dimming_pct", 20),
        )
        self._zones[zone_id] = zone
        return zone

    def get_energy_report(
        self,
        zone_id: str,
        period_days: int = 30,
    ) -> StreetlightEnergyReport:
        import random
        random.seed(hash(zone_id) % 2**31)

        consumption = random.uniform(5000, 20000)
        return StreetlightEnergyReport(
            zone_id=zone_id,
            period_days=period_days,
            consumption_kwh=round(consumption, 1),
            cost_savings=round(consumption * 0.12, 2),
            co2_reduction_kg=round(consumption * 0.42, 1),
            faults_detected=random.randint(0, 5),
        )


class PowerQualityAnalyzer:
    """Analyzes power quality events and root causes."""

    def __init__(self, engine: "EnergyGridEngine") -> None:
        self._engine = engine
        self._pq_events: Dict[str, PQEvent] = {}

    def query_events(
        self,
        substation_id: str,
        event_types: Optional[List[PQEventType]] = None,
        time_range: Optional[Tuple[str, str]] = None,
    ) -> List[PQEvent]:
        events = [
            e for e in self._engine._pq_events.values()
            if e.substation_id == substation_id
        ]
        if event_types:
            events = [e for e in events if e.event_type in event_types]
        return events


# ---------------------------------------------------------------------------
# Main Engine
# ---------------------------------------------------------------------------

class EnergyGridEngine:
    """Main engine for energy grid management operations."""

    def __init__(
        self,
        utility_id: str,
        grid_config: Optional[GridConfig] = None,
        ami_config: Optional[AMIConfig] = None,
    ) -> None:
        self.utility_id = utility_id
        self._grid_config = grid_config or GridConfig()
        self._ami_config = ami_config or AMIConfig()
        self._status = EngineStatus.UNINITIALIZED
        self._feeders: Dict[str, Feeder] = {}
        self._meters: Dict[str, SmartMeter] = {}
        self._outages: Dict[str, Outage] = {}
        self._pq_events: Dict[str, PQEvent] = {}
        self._meters_online: int = 0
        self._created_at = datetime.utcnow()
        self._last_run: Optional[datetime] = None

    def configure(self) -> EnergyGridEngine:
        """Validate configuration and establish grid connections."""
        self._status = EngineStatus.CONFIGURING
        self._grid_config.validate()
        self._meters_online = self._grid_config.smart_meters

        logger.info(
            "Energy grid engine configured for %s: %d feeders, %d meters",
            self.utility_id, self._grid_config.feeders, self._meters_online,
        )
        self._status = EngineStatus.READY
        return self

    def run(self) -> Dict[str, Any]:
        """Execute a full grid monitoring cycle."""
        if self._status != EngineStatus.READY:
            raise RuntimeError(f"Engine not ready: {self._status.name}")

        self._status = EngineStatus.RUNNING
        self._last_run = datetime.utcnow()

        result = {
            "utility_id": self.utility_id,
            "status": self._status.value,
            "timestamp": self._last_run.isoformat(),
            "meters_online": self._meters_online,
            "feeders": len(self._feeders),
            "solar_output_mw": self._grid_config.distributed_solar_mw,
        }

        self._status = EngineStatus.READY
        return result

    def validate(self) -> bool:
        """Validate engine configuration."""
        if self._status == EngineStatus.UNINITIALIZED:
            return False
        return self._grid_config.validate()

    def get_status(self) -> Dict[str, Any]:
        """Get current engine status and metrics."""
        return {
            "engine": "EnergyGrid",
            "utility_id": self.utility_id,
            "status": self._status.name,
            "meters_total": self._grid_config.smart_meters,
            "meters_online": self._meters_online,
            "feeders": self._grid_config.feeders,
            "substations": self._grid_config.substations,
            "solar_output_mw": self._grid_config.distributed_solar_mw,
            "battery_storage_mw": self._grid_config.battery_storage_mw,
            "ev_chargers": self._grid_config.ev_chargers,
            "uptime_seconds": (datetime.utcnow() - self._created_at).total_seconds(),
            "last_run": self._last_run.isoformat() if self._last_run else None,
        }

    def add_feeder(self, feeder: Feeder) -> None:
        self._feeders[feeder.feeder_id] = feeder

    def add_meter(self, meter: SmartMeter) -> None:
        self._meters[meter.meter_id] = meter

    def register_pq_event(self, event: PQEvent) -> None:
        self._pq_events[event.event_id] = event

    def shutdown(self) -> None:
        """Gracefully shut down the engine."""
        self._status = EngineStatus.SHUTDOWN
        logger.info("Energy grid engine shut down for %s", self.utility_id)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate energy grid engine capabilities."""
    print("=" * 70)
    print("  Energy Grid — Smart City Power Management Platform Demo")
    print("=" * 70)

    engine = EnergyGridEngine(
        utility_id="utility-metro-001",
        grid_config=GridConfig(
            voltage_levels_kv=[13.8, 34.5, 69, 138],
            substations=45, feeders=320,
            smart_meters=1_200_000,
            distributed_solar_mw=180.0,
            battery_storage_mw=45.0,
            ev_chargers=8_500,
        ),
        ami_config=AMIConfig(read_interval_minutes=15, data_retention_years=3),
    )

    engine.configure()
    status = engine.get_status()
    print(f"\n[1] Engine Status: {status['status']}")
    print(f"    Meters online: {status['meters_online']:,}")
    print(f"    Solar output: {status['solar_output_mw']:.0f} MW")

    import random
    random.seed(42)
    for i in range(5):
        feeder = Feeder(
            feeder_id=f"feeder-north-{i:02d}", name=f"North Feeder {i}",
            substation_id="substation-east-01", voltage_kv=13.8,
            length_km=random.uniform(5.0, 25.0),
            total_load_mw=random.uniform(2.0, 15.0),
            der_penetration_pct=random.uniform(5.0, 40.0),
        )
        for j in range(3):
            feeder.transformers.append(Transformer(
                transformer_id=f"xfmr-{i}-{j}", name=f"Xfmr {i}.{j}",
                rated_kva=random.choice([100, 200, 500, 1000]),
                primary_voltage_kv=13.8, secondary_voltage_kv=0.48,
                current_load_kw=random.uniform(20, 400),
            ))
        engine.add_feeder(feeder)

    grid_monitor = GridStateMonitor(engine)
    feeder_status = grid_monitor.get_feeder_status("feeder-north-00")
    if feeder_status:
        print(f"\n[2] Feeder Status: {feeder_status.name}")
        print(f"    Load: {feeder_status.total_load_mw:.2f} MW")
        print(f"    DER penetration: {feeder_status.der_penetration_pct:.1f}%")
        for xfmr in feeder_status.transformers:
            print(f"    Transformer {xfmr.name}: {xfmr.loading_pct:.1f}% loading")

    dr = DemandResponseOrchestrator(engine)
    event = dr.create_event(
        program=DRProgram.CAPACITY_BID, event_type="economic",
        start_time="2024-07-15T14:00:00", end_time="2024-07-15T18:00:00",
        target_reduction_mw=25.0,
    )
    verification = dr.verify_event(event.event_id)
    print(f"\n[3] DR Event: {event.event_id}")
    print(f"    Target: {event.target_reduction_mw:.1f} MW")
    print(f"    Verified reduction: {verification.actual_reduction_mw:.1f} MW")
    print(f"    Status: {verification.status}")

    outage_mgr = OutageManager(engine)
    outage = Outage(
        outage_id="out-001", cause=OutageCause.VEGETATION,
        severity=OutageSeverity.CRITICAL, fault_location="Main & 5th",
        latitude=41.88, longitude=-87.63, customers_affected=1200,
    )
    outage_mgr.register_outage(outage)
    flisr = outage_mgr.initiate_flisr("out-001")
    print(f"\n[4] FLISR Result:")
    print(f"    Restored: {flisr.restored_customers:,} customers")
    print(f"    Remaining affected: {flisr.remaining_affected:,}")

    sl_mgr = StreetlightManager(engine)
    zone = sl_mgr.set_dimming_profile(
        zone_id="zone-downtown-core", profile=DimmingProfile.ADAPTIVE,
        parameters={"base_dimming_pct": 30, "curfew_dimming_pct": 20},
    )
    report = sl_mgr.get_energy_report("zone-downtown-core", period_days=30)
    print(f"\n[5] Streetlight Energy Report:")
    print(f"    Consumption: {report.consumption_kwh:,.0f} kWh")
    print(f"    Cost savings: ${report.cost_savings:.2f}")
    print(f"    CO2 reduction: {report.co2_reduction_kg:.1f} kg")

    pq_analyzer = PowerQualityAnalyzer(engine)
    for i in range(3):
        engine.register_pq_event(PQEvent(
            event_id=f"pq-{i}", event_type=PQEventType.VOLTAGE_SAG,
            timestamp=datetime.utcnow(), substation_id="substation-east-03",
            magnitude=0.88, duration_ms=random.uniform(50, 500),
        ))
    events = pq_analyzer.query_events("substation-east-03")
    print(f"\n[6] PQ Events: {len(events)} events at substation-east-03")
    for e in events:
        print(f"    {e.event_type.value}: magnitude={e.magnitude:.2f} pu, "
              f"duration={e.duration_ms:.0f} ms")

    result = engine.run()
    print(f"\n[7] Pipeline Run: {result['meters_online']:,} meters, "
          f"{result['feeders']} feeders")

    engine.shutdown()
    print(f"\n[8] Engine Shutdown: {engine.get_status()['status']}")


if __name__ == "__main__":
    main()

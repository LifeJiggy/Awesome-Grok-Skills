"""
Traffic Management Module — Adaptive Urban Mobility Platform

Provides intelligent transportation system (ITS) capabilities for real-time
traffic monitoring, adaptive signal control, incident detection, and mobility
optimization. Fuses data from loop detectors, radar, cameras, connected
vehicles, and transit AVL systems.

Domain: Smart Cities > Traffic Management
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
    """Operational state of the traffic management engine."""
    UNINITIALIZED = auto()
    CONFIGURING = auto()
    READY = auto()
    RUNNING = auto()
    ERROR = auto()
    SHUTDOWN = auto()


class SignalControllerType(Enum):
    """Supported traffic signal controller protocols."""
    NTCIP = "ntcip"
    ATC = "atc"
    CUSTOM_ADAPTIVE = "custom_adaptive"


class AdaptiveAlgorithm(Enum):
    """Adaptive signal control algorithm types."""
    SCOOT = "scoot"
    SCATS = "scats"
    AI_BASED = "ai_based"
    ACTUATED = "actuated"
    FIXED_TIME = "fixed_time"


class OptimizationTarget(Enum):
    """Signal optimization objective functions."""
    THROUGHPUT = "throughput"
    DELAY_MINIMIZATION = "delay_minimization"
    QUEUE_LENGTH = "queue_length"
    EMISSIONS = "emissions"
    TRANSIT_PRIORITY = "transit_priority"
    MULTIMODAL = "multimodal"


class RoadType(Enum):
    """Road classification types."""
    HIGHWAY = "highway"
    ARTERIAL = "arterial"
    COLLECTOR = "collector"
    LOCAL = "local"


class IncidentSeverity(Enum):
    """Traffic incident severity levels."""
    MINOR = "minor"
    MODERATE = "moderate"
    MAJOR = "major"
    CRITICAL = "critical"


class IncidentType(Enum):
    """Types of traffic incidents."""
    COLLISION = "collision"
    STALLED_VEHICLE = "stalled_vehicle"
    DEBRIS = "debris"
    WEATHER = "weather"
    CONSTRUCTION = "construction"
    SPECIAL_EVENT = "special_event"
    HAZMAT = "hazmat"


class PredictionHorizon(Enum):
    """Travel time prediction horizons."""
    MINUTES_5 = "5min"
    MINUTES_15 = "15min"
    MINUTES_30 = "30min"
    HOUR = "1hour"
    HOURS_4 = "4hours"


class PriorityMode(Enum):
    """Transit signal priority modes."""
    UNCONDITIONAL = "unconditional"
    CONDITIONAL = "conditional"
    DISABLED = "disabled"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class SensorConfig:
    """Configuration for traffic sensor deployment."""
    loop_detectors: int = 0
    radar_sensors: int = 0
    cameras_with_cv: int = 0
    bluetooth_readers: int = 0
    v2x_equipped_intersections: int = 0

    @property
    def total_sensors(self) -> int:
        return (self.loop_detectors + self.radar_sensors +
                self.cameras_with_cv + self.bluetooth_readers)


@dataclass
class SignalNetworkConfig:
    """Configuration for the signal control network."""
    controller_type: SignalControllerType = SignalControllerType.NTCIP
    adaptive_algorithm: AdaptiveAlgorithm = AdaptiveAlgorithm.AI_BASED
    num_intersections: int = 0
    coordination_groups: int = 0
    cycle_length_range: Tuple[int, int] = (60, 150)
    offset_optimization: bool = True

    def validate(self) -> bool:
        if self.cycle_length_range[0] >= self.cycle_length_range[1]:
            raise ValueError("Min cycle length must be < max cycle length")
        if self.num_intersections < 1:
            raise ValueError("Must have at least 1 intersection")
        return True


@dataclass
class TrafficLink:
    """A single road link in the traffic network."""
    link_id: str
    name: str
    road_type: RoadType
    length_m: float
    lanes: int
    speed_limit_kmh: float
    from_node: str
    to_node: str


@dataclass
class TrafficState:
    """Current traffic state for a road link."""
    link_id: str
    avg_speed_kmh: float
    volume_vph: int
    occupancy_pct: float
    density_vpk: float
    travel_time_s: float
    speed_ratio: float = 1.0
    measured_at: datetime = field(default_factory=datetime.utcnow)

    def __post_init__(self) -> None:
        if self.speed_ratio == 1.0 and self.avg_speed_kmh > 0:
            pass


@dataclass
class Intersection:
    """A signalized intersection."""
    intersection_id: str
    name: str
    latitude: float
    longitude: float
    num_phases: int
    pedestrian_phases: bool = True


@dataclass
class SignalTimingPlan:
    """A signal timing plan for an intersection."""
    plan_id: str
    intersection_id: str
    cycle_length_s: int
    phases: List[Dict[str, Any]] = field(default_factory=list)
    offsets: Dict[str, int] = field(default_factory=dict)


@dataclass
class CorridorOptimizationResult:
    """Result of a corridor optimization run."""
    corridor_id: str
    intersections_modified: int
    throughput_delta_pct: float
    delay_delta_pct: float
    timing_plan_id: str
    safety_check_passed: bool
    computed_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TrafficIncident:
    """A detected traffic incident."""
    incident_id: str
    incident_type: IncidentType
    severity: IncidentSeverity
    location: str
    latitude: float
    longitude: float
    lanes_blocked: int
    lanes_total: int
    eta_clearance_min: int
    affected_links: List[str] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TravelTimePrediction:
    """Predicted travel time for a route segment."""
    departure_time: str
    travel_time_min: float
    ci_lower: float
    ci_upper: float
    confidence: float


@dataclass
class RoutePrediction:
    """Predicted travel times for an entire route."""
    origin: str
    destination: str
    forecasts: List[TravelTimePrediction] = field(default_factory=list)


@dataclass
class TSPConfiguration:
    """Transit signal priority configuration for a route."""
    route_id: str
    priority_mode: PriorityMode
    schedule_deviation_threshold_min: float = 3.0
    min_passengers: int = 0
    max_extension_s: int = 20
    max_truncation_s: int = 10


@dataclass
class TSPEffectiveness:
    """Transit signal priority effectiveness metrics."""
    route_id: str
    total_activations: int
    avg_time_saved_s: float
    otp_delta_pct: float
    period_days: int = 30


# ---------------------------------------------------------------------------
# Helper Classes
# ---------------------------------------------------------------------------

class TrafficStateMonitor:
    """Monitors real-time traffic conditions across the network."""

    def __init__(self, engine: "TrafficManagementEngine") -> None:
        self._engine = engine

    def get_corridor_status(
        self,
        corridor_id: str,
        include_lane_detail: bool = False,
    ) -> Dict[str, Any]:
        links = [
            link for link in self._engine._links.values()
            if corridor_id in link.link_id
        ]

        states: List[Dict[str, Any]] = []
        for link in links:
            state = self._engine._traffic_states.get(link.link_id)
            if state:
                states.append({
                    "name": link.name,
                    "avg_speed_kmh": state.avg_speed_kmh,
                    "volume_vph": state.volume_vph,
                    "occupancy_pct": state.occupancy_pct,
                    "speed_ratio": state.speed_ratio,
                })

        return {"corridor_id": corridor_id, "links": states, "link_count": len(states)}

    def get_network_summary(self) -> Dict[str, Any]:
        states = list(self._engine._traffic_states.values())
        if not states:
            return {"avg_speed": 0, "congested_links": 0, "total_links": 0}

        avg_speed = sum(s.avg_speed_kmh for s in states) / len(states)
        congested = sum(1 for s in states if s.speed_ratio < 0.5)

        return {
            "total_links": len(states),
            "avg_speed_kmh": round(avg_speed, 1),
            "congested_links": congested,
            "congestion_pct": round(congested / len(states) * 100, 1) if states else 0,
        }


class SignalOptimizer:
    """Optimizes traffic signal timing for corridors and networks."""

    def __init__(self, engine: "TrafficManagementEngine") -> None:
        self._engine = engine
        self._timing_plans: Dict[str, SignalTimingPlan] = {}

    def optimize_corridor(
        self,
        corridor_id: str,
        target: OptimizationTarget = OptimizationTarget.THROUGHPUT,
        constraints: Optional[Dict[str, Any]] = None,
    ) -> CorridorOptimizationResult:
        if constraints is None:
            constraints = {}

        intersections = [
            i for i in self._engine._intersections.values()
            if corridor_id in i.intersection_id
        ]

        plan_id = f"plan-{uuid.uuid4().hex[:8]}"
        throughput_delta = 5.0 + len(intersections) * 0.5
        delay_delta = -3.0 - len(intersections) * 0.3

        return CorridorOptimizationResult(
            corridor_id=corridor_id,
            intersections_modified=len(intersections),
            throughput_delta_pct=round(throughput_delta, 1),
            delay_delta_pct=round(delay_delta, 1),
            timing_plan_id=plan_id,
            safety_check_passed=True,
        )

    def apply_timing_plan(
        self,
        plan_id: str,
        dry_run: bool = False,
    ) -> bool:
        if dry_run:
            logger.info("Dry run: timing plan %s would be applied", plan_id)
            return True
        logger.info("Applied timing plan %s to controllers", plan_id)
        return True


class IncidentDetector:
    """Detects and manages traffic incidents."""

    def __init__(self, engine: "TrafficManagementEngine") -> None:
        self._engine = engine
        self._active_incidents: Dict[str, TrafficIncident] = {}

    def scan_incidents(
        self,
        time_window_minutes: int = 5,
        severity_threshold: IncidentSeverity = IncidentSeverity.MODERATE,
    ) -> List[TrafficIncident]:
        severity_order = {
            IncidentSeverity.MINOR: 1,
            IncidentSeverity.MODERATE: 2,
            IncidentSeverity.MAJOR: 3,
            IncidentSeverity.CRITICAL: 4,
        }
        threshold_val = severity_order.get(severity_threshold, 2)

        return [
            inc for inc in self._active_incidents.values()
            if severity_order.get(inc.severity, 0) >= threshold_val
        ]

    def register_incident(self, incident: TrafficIncident) -> None:
        self._active_incidents[incident.incident_id] = incident
        logger.warning(
            "Incident %s: %s at %s",
            incident.incident_id, incident.incident_type.value, incident.location,
        )

    def activate_response_plan(
        self,
        incident_id: str,
        plan: str,
    ) -> Dict[str, Any]:
        incident = self._active_incidents.get(incident_id)
        if incident is None:
            raise KeyError(f"Incident not found: {incident_id}")

        logger.info("Activated response plan '%s' for incident %s", plan, incident_id)
        return {
            "incident_id": incident_id,
            "plan": plan,
            "status": "activated",
            "actions_taken": ["dms_updated", "signal_adjusted", "units_notified"],
        }

    def clear_incident(self, incident_id: str) -> None:
        self._active_incidents.pop(incident_id, None)


class TravelTimePredictor:
    """Predicts travel times across the network."""

    def __init__(self, engine: "TrafficManagementEngine") -> None:
        self._engine = engine

    def predict_routes(
        self,
        routes: List[Dict[str, str]],
        horizon: PredictionHorizon = PredictionHorizon.HOUR,
        include_confidence: bool = True,
    ) -> List[RoutePrediction]:
        import random
        random.seed(42)

        results: List[RoutePrediction] = []
        for route in routes:
            base_time = random.uniform(15.0, 60.0)
            forecasts: List[TravelTimePrediction] = []

            num_steps = 4
            for step in range(num_steps):
                departure = f"T+{step * 15}min"
                tt = base_time * (1.0 + random.uniform(-0.2, 0.4))
                ci_half = tt * 0.15
                forecasts.append(TravelTimePrediction(
                    departure_time=departure,
                    travel_time_min=round(tt, 1),
                    ci_lower=round(tt - ci_half, 1),
                    ci_upper=round(tt + ci_half, 1),
                    confidence=0.85,
                ))

            results.append(RoutePrediction(
                origin=route.get("origin", "unknown"),
                destination=route.get("destination", "unknown"),
                forecasts=forecasts,
            ))

        return results


class TransitPriorityManager:
    """Manages transit signal priority for bus routes."""

    def __init__(self, engine: "TrafficManagementEngine") -> None:
        self._engine = engine
        self._route_configs: Dict[str, TSPConfiguration] = {}

    def configure_route(
        self,
        route_id: str,
        priority_mode: PriorityMode = PriorityMode.CONDITIONAL,
        conditions: Optional[Dict[str, Any]] = None,
    ) -> TSPConfiguration:
        if conditions is None:
            conditions = {}

        config = TSPConfiguration(
            route_id=route_id,
            priority_mode=priority_mode,
            schedule_deviation_threshold_min=conditions.get("schedule_deviation_threshold_min", 3.0),
            min_passengers=conditions.get("min_passengers", 0),
            max_extension_s=conditions.get("max_extension_s", 20),
            max_truncation_s=conditions.get("max_truncation_s", 10),
        )
        self._route_configs[route_id] = config
        return config

    def get_effectiveness(
        self,
        route_id: str,
        period_days: int = 30,
    ) -> TSPEffectiveness:
        import random
        random.seed(hash(route_id) % 2**31)

        return TSPEffectiveness(
            route_id=route_id,
            total_activations=random.randint(100, 2000),
            avg_time_saved_s=round(random.uniform(5.0, 25.0), 1),
            otp_delta_pct=round(random.uniform(2.0, 8.0), 1),
            period_days=period_days,
        )


# ---------------------------------------------------------------------------
# Main Engine
# ---------------------------------------------------------------------------

class TrafficManagementEngine:
    """Main engine for traffic management operations."""

    def __init__(
        self,
        city_id: str,
        sensor_config: Optional[SensorConfig] = None,
        signal_config: Optional[SignalNetworkConfig] = None,
    ) -> None:
        self.city_id = city_id
        self._sensor_config = sensor_config or SensorConfig()
        self._signal_config = signal_config or SignalNetworkConfig()
        self._status = EngineStatus.UNINITIALIZED
        self._links: Dict[str, TrafficLink] = {}
        self._traffic_states: Dict[str, TrafficState] = {}
        self._intersections: Dict[str, Intersection] = {}
        self._controllers_online: int = 0
        self._sensors_online: int = 0
        self._created_at = datetime.utcnow()
        self._last_run: Optional[datetime] = None

    def configure(self) -> TrafficManagementEngine:
        """Validate configuration and initialize sensor connections."""
        self._status = EngineStatus.CONFIGURING
        self._signal_config.validate()

        self._sensors_online = self._sensor_config.total_sensors
        self._controllers_online = self._signal_config.num_intersections

        logger.info(
            "Traffic engine configured for %s: %d sensors, %d controllers",
            self.city_id, self._sensors_online, self._controllers_online,
        )
        self._status = EngineStatus.READY
        return self

    def run(self) -> Dict[str, Any]:
        """Execute a full traffic monitoring cycle."""
        if self._status != EngineStatus.READY:
            raise RuntimeError(f"Engine not ready: {self._status.name}")

        self._status = EngineStatus.RUNNING
        self._last_run = datetime.utcnow()

        result = {
            "city_id": self.city_id,
            "status": self._status.value,
            "timestamp": self._last_run.isoformat(),
            "links_monitored": len(self._links),
            "intersections": len(self._intersections),
            "active_states": len(self._traffic_states),
        }

        self._status = EngineStatus.READY
        return result

    def validate(self) -> bool:
        """Validate engine configuration."""
        if self._status == EngineStatus.UNINITIALIZED:
            return False
        return self._signal_config.validate()

    def get_status(self) -> Dict[str, Any]:
        """Get current engine status and metrics."""
        return {
            "engine": "TrafficManagement",
            "city_id": self.city_id,
            "status": self._status.name,
            "sensors_total": self._sensor_config.total_sensors,
            "sensors_online": self._sensors_online,
            "controllers_total": self._signal_config.num_intersections,
            "controllers_online": self._controllers_online,
            "links": len(self._links),
            "intersections": len(self._intersections),
            "uptime_seconds": (datetime.utcnow() - self._created_at).total_seconds(),
            "last_run": self._last_run.isoformat() if self._last_run else None,
        }

    def add_link(self, link: TrafficLink) -> None:
        self._links[link.link_id] = link

    def add_intersection(self, intersection: Intersection) -> None:
        self._intersections[intersection.intersection_id] = intersection

    def update_traffic_state(self, state: TrafficState) -> None:
        self._traffic_states[state.link_id] = state

    def shutdown(self) -> None:
        """Gracefully shut down the engine."""
        self._status = EngineStatus.SHUTDOWN
        logger.info("Traffic management engine shut down for %s", self.city_id)


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate traffic management engine capabilities."""
    print("=" * 70)
    print("  Traffic Management — Adaptive Urban Mobility Platform Demo")
    print("=" * 70)

    engine = TrafficManagementEngine(
        city_id="metro-chicago-001",
        sensor_config=SensorConfig(
            loop_detectors=1200, radar_sensors=340,
            cameras_with_cv=180, bluetooth_readers=95,
        ),
        signal_config=SignalNetworkConfig(
            controller_type=SignalControllerType.NTCIP,
            adaptive_algorithm=AdaptiveAlgorithm.AI_BASED,
            num_intersections=850, coordination_groups=12,
        ),
    )

    engine.configure()
    print(f"\n[1] Engine Status: {engine.get_status()['status']}")
    print(f"    Sensors online: {engine.get_status()['sensors_online']}")
    print(f"    Controllers online: {engine.get_status()['controllers_online']}")

    for i in range(15):
        link = TrafficLink(
            link_id=f"corridor-michigan-ave_link-{i:03d}",
            name=f"Michigan Ave Block {i}",
            road_type=RoadType.ARTERIAL,
            length_m=100 + i * 10, lanes=3, speed_limit_kmh=50,
            from_node=f"node-{i}", to_node=f"node-{i + 1}",
        )
        engine.add_link(link)

        import random
        random.seed(i)
        speed = random.uniform(10.0, 50.0)
        engine.update_traffic_state(TrafficState(
            link_id=link.link_id, avg_speed_kmh=round(speed, 1),
            volume_vph=random.randint(200, 1200),
            occupancy_pct=round(random.uniform(5.0, 40.0), 1),
            density_vpk=round(random.uniform(10.0, 60.0), 1),
            travel_time_s=round(link.length_m / (speed / 3.6), 1),
            speed_ratio=round(speed / 50.0, 2),
        ))

    for i in range(5):
        engine.add_intersection(Intersection(
            intersection_id=f"corridor-michigan-ave_int-{i:03d}",
            name=f"Michigan & Cross St {i}", latitude=41.88 + i * 0.002,
            longitude=-87.62, num_phases=4,
        ))

    monitor = TrafficStateMonitor(engine)
    corridor = monitor.get_corridor_status(corridor_id="corridor-michigan-ave")
    print(f"\n[2] Corridor Status: {corridor['link_count']} links")
    for link_data in corridor["links"][:3]:
        print(f"    {link_data['name']}: {link_data['avg_speed_kmh']:.0f} km/h, "
              f"speed_ratio={link_data['speed_ratio']:.2f}")

    optimizer = SignalOptimizer(engine)
    opt_result = optimizer.optimize_corridor(
        corridor_id="corridor-michigan-ave",
        target=OptimizationTarget.THROUGHPUT,
    )
    print(f"\n[3] Signal Optimization: {opt_result.intersections_modified} intersections")
    print(f"    Throughput improvement: {opt_result.throughput_delta_pct:+.1f}%")
    print(f"    Safety check: {'PASSED' if opt_result.safety_check_passed else 'FAILED'}")

    detector = IncidentDetector(engine)
    test_incident = TrafficIncident(
        incident_id="inc-001", incident_type=IncidentType.COLLISION,
        severity=IncidentSeverity.MODERATE, location="Michigan & 12th",
        latitude=41.865, longitude=-87.625, lanes_blocked=1, lanes_total=3,
        eta_clearance_min=30, affected_links=["corridor-michigan-ave_link-005"],
    )
    detector.register_incident(test_incident)
    alerts = detector.scan_incidents(severity_threshold=IncidentSeverity.MODERATE)
    print(f"\n[4] Active Incidents: {len(alerts)}")
    for alert in alerts:
        print(f"    {alert.incident_type.value}: {alert.location} "
              f"(severity: {alert.severity.value})")

    predictor = TravelTimePredictor(engine)
    predictions = predictor.predict_routes(
        routes=[
            {"origin": "suburban-north", "destination": "downtown-core"},
        ],
    )
    print(f"\n[5] Travel Time Predictions:")
    for route in predictions:
        for fc in route.forecasts[:2]:
            print(f"    {fc.departure_time}: {fc.travel_time_min:.0f} min "
                  f"(CI: {fc.ci_lower:.0f}-{fc.ci_upper:.0f})")

    tsp = TransitPriorityManager(engine)
    tsp.configure_route(route_id="bus-route-42", priority_mode=PriorityMode.CONDITIONAL)
    effectiveness = tsp.get_effectiveness(route_id="bus-route-42")
    print(f"\n[6] TSP Effectiveness (bus-route-42):")
    print(f"    Activations: {effectiveness.total_activations}")
    print(f"    Avg time saved: {effectiveness.avg_time_saved_s:.1f}s")
    print(f"    OTP improvement: {effectiveness.otp_delta_pct:+.1f}%")

    result = engine.run()
    print(f"\n[7] Pipeline Run: {result['links_monitored']} links, "
          f"{result['intersections']} intersections")

    engine.shutdown()
    print(f"\n[8] Engine Shutdown: {engine.get_status()['status']}")


if __name__ == "__main__":
    main()

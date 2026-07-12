"""
Mission Planning Toolkit
Launch windows, ground station scheduling, timeline management,
trajectory design, contingency planning, risk assessment.
"""

from __future__ import annotations

import math
import json
import random
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional, List, Tuple, Dict, Any, Callable

import numpy as np


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class RiskLevel(Enum):
    NEGLIGIBLE = "negligible"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MissionPhase(Enum):
    PRE_LAUNCH = "pre_launch"
    LAUNCH = "launch"
    EARLY_ORBIT = "early_orbit"
    Commissioning = "commissioning"
    OPERATIONAL = "operational"
    DEORBIT = "deorbit"
    DISPOSAL = "disposal"


class AnomalyClass(Enum):
    NOMINAL = "nominal"
    WATCH = "watch"
    CAUTION = "caution"
    WARNING = "warning"
    EMERGENCY = "emergency"


class ResourceType(Enum):
    POWER = "power"
    DATA_STORAGE = "data_storage"
    COMM_BANDWIDTH = "comm_bandwidth"
    GROUND_STATION = "ground_station"
    PERSONNEL = "personnel"
    FUEL = "fuel"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class LaunchConstraints:
    beta_angle_min_deg: float = -60.0
    beta_angle_max_deg: float = 60.0
    elevation_min_deg: float = 5.0
    collision_avoidance_windows: List[Tuple[float, float]] = field(default_factory=list)
    max_cloud_cover_pct: float = 100.0
    max_wind_speed_ms: float = 25.0
    lightning_range_km: float = 10.0
    solar_saa禁区: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LaunchWindow:
    start_time: str
    end_time: str
    duration_min: float
    beta_angle_deg: float
    azimuth_deg: float
    elevation_deg: float
    launch_azimuth_deg: float
    lighting_condition: str = "sunlit"
    score: float = 1.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class GroundStation:
    name: str
    latitude_deg: float
    longitude_deg: float
    altitude_m: float
    min_elevation_deg: float = 5.0
    max_slew_rate_deg_s: float = 1.0
    bandwidth_mbps: float = 150.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Satellite:
    name: str
    altitude_m: float
    inclination_deg: float
    raan_deg: float = 0.0
    data_generation_rate_gbps: float = 0.1
    priority: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Pass:
    station_name: str
    satellite_name: str
    aos_time_s: float
    los_time_s: float
    max_elevation_deg: float
    duration_s: float
    data_capacity_gb: float
    aos_azimuth_deg: float = 0.0

    @property
    def duration_min(self) -> float:
        return self.duration_s / 60.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ScheduleResult:
    total_passes: int
    total_data_gb: float
    ground_station_utilization_pct: float
    satellite_utilization_pct: float
    passes: List[Pass]
    conflicts: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_passes": self.total_passes,
            "total_data_gb": self.total_data_gb,
            "gs_utilization_pct": self.ground_station_utilization_pct,
            "sat_utilization_pct": self.satellite_utilization_pct,
            "num_passes": len(self.passes),
            "conflicts": self.conflicts,
        }


@dataclass
class TimelineEvent:
    name: str
    start_min: float
    duration_min: float
    resources_used: Dict[str, float] = field(default_factory=dict)
    priority: int = 1
    mandatory: bool = True
    category: str = "operations"

    @property
    def end_min(self) -> float:
        return self.start_min + self.duration_min

    def overlaps(self, other: "TimelineEvent") -> bool:
        return self.start_min < other.end_min and other.start_min < self.end_min

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ResourceConflict:
    resource_name: str
    time_min: float
    events: List[str]
    total_demand: float
    capacity: float
    overshoot_pct: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TimelineResult:
    feasible: bool
    conflicts: List[ResourceConflict]
    peak_usage: Dict[str, float]
    event_count: int
    total_duration_min: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "feasible": self.feasible,
            "num_conflicts": len(self.conflicts),
            "peak_usage": self.peak_usage,
            "event_count": self.event_count,
            "total_duration_min": self.total_duration_min,
        }


@dataclass
class TrajectoryResult:
    transfer_time_days: float
    delta_v_ms: float
    propellant_kg: float
    final_semi_major_axis: float
    final_inclination_deg: float
    trajectory_points: List[Dict[str, float]]
    max_thrust_n: float
    isp_s: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "transfer_time_days": self.transfer_time_days,
            "delta_v_ms": self.delta_v_ms,
            "propellant_kg": self.propellant_kg,
            "final_sma": self.final_semi_major_axis,
            "final_inc": self.final_inclination_deg,
            "num_points": len(self.trajectory_points),
            "max_thrust_n": self.max_thrust_n,
            "isp_s": self.isp_s,
        }


@dataclass
class MonteCarloResult:
    num_runs: int
    success_count: int
    success_probability: float
    arrival_error_mean_km: float
    arrival_error_3sigma_km: float
    delta_v_mean_ms: float
    delta_v_std_ms: float
    transfer_time_std_days: float
    failure_modes: Dict[str, int]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RiskItem:
    id: str
    description: str
    likelihood: float  # 0-1
    severity: float  # 1-5
    risk_score: float
    risk_level: RiskLevel
    mitigation: str = ""
    residual_likelihood: float = 0.0
    residual_severity: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["risk_level"] = self.risk_level.value
        return d


@dataclass
class ContingencyPlan:
    anomaly_class: AnomalyClass
    trigger_condition: str
    response_actions: List[str]
    decision_tree: Dict[str, Any]
    time_limit_min: float = 60.0
    required_resources: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["anomaly_class"] = self.anomaly_class.value
        return d


@dataclass
class PayloadSchedule:
    instrument_name: str
    mode: str
    start_min: float
    duration_min: float
    data_volume_gb: float
    power_w: float
    ground_station_contact_required: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Core Classes
# ---------------------------------------------------------------------------

class LaunchWindowCalculator:
    """Launch window computation for LEO and MEO missions."""

    EARTH_ROTATION_RATE_DEG_HR = 15.041  # deg/hr

    def __init__(
        self,
        target_orbit_inclination_deg: float,
        target_orbit_altitude_m: float,
        launch_site_lat_deg: float,
        launch_site_lon_deg: float,
    ):
        self.target_inc = target_orbit_inclination_deg
        self.target_alt = target_orbit_altitude_m
        self.site_lat = launch_site_lat_deg
        self.site_lon = launch_site_lon_deg

    def _beta_angle(self, day_of_year: float, raan_deg: float) -> float:
        """Compute beta angle (angle between orbital plane and sun vector)."""
        # Solar declination approximation
        solar_decl = 23.44 * math.sin(math.radians(360.0 * (day_of_year + 284) / 365.0))
        # Beta angle = arcsin(sin(dec) * sin(inc) + cos(dec) * cos(inc) * cos(raan - sun_raan))
        sun_raan = 360.0 * day_of_year / 365.0  # approximate
        beta = math.asin(
            math.sin(math.radians(solar_decl)) * math.sin(math.radians(self.target_inc))
            + math.cos(math.radians(solar_decl)) * math.cos(math.radians(self.target_inc))
            * math.cos(math.radians(raan_deg - sun_raan))
        )
        return math.degrees(beta)

    def _launch_azimuth(self, orbit_inclination_deg: float) -> float:
        """Required launch azimuth for desired orbit inclination."""
        cos_az = math.cos(math.radians(orbit_inclination_deg)) / math.cos(math.radians(self.site_lat))
        cos_az = max(-1.0, min(1.0, cos_az))
        return math.degrees(math.acos(cos_az))

    def _ascent_corridor_clear(self, azimuth_deg: float) -> bool:
        """Check if ascent corridor is clear of populated areas (simplified)."""
        # Simplified: reject azimuths over open ocean only for demo
        return True

    def compute_windows(
        self,
        start_date: str,
        end_date: str,
        constraints: LaunchConstraints,
        time_step_min: float = 1.0,
    ) -> List[LaunchWindow]:
        """Compute valid launch windows within the date range."""
        windows = []
        # Simulate 30 days
        for day in range(30):
            for minute in range(0, 1440, int(time_step_min)):
                day_of_year = 182 + day  # July start
                time_hr = minute / 60.0

                # RAAN at this launch time
                earth_rotation = self.EARTH_ROTATION_RATE_DEG_HR * time_hr
                raan = (self.site_lon + earth_rotation) % 360.0

                # Beta angle
                beta = self._beta_angle(day_of_year, raan)
                if not (constraints.beta_angle_min_deg <= beta <= constraints.beta_angle_max_deg):
                    continue

                # Launch azimuth
                azimuth = self._launch_azimuth(self.target_inc)
                if not self._ascent_corridor_clear(azimuth):
                    continue

                # Check collision avoidance
                blocked = False
                for ca_start, ca_end in constraints.collision_avoidance_windows:
                    if ca_start <= minute % 1440 <= ca_end:
                        blocked = True
                        break
                if blocked:
                    continue

                # Score based on beta angle (prefer near-zero)
                score = 1.0 - abs(beta) / 90.0

                windows.append(LaunchWindow(
                    start_time=f"2026-07-{day+1:02d}T{minute//60:02d}:{minute%60:02d}:00Z",
                    end_time=f"2026-07-{day+1:02d}T{(minute+15)//60:02d}:{(minute+15)%60:02d}:00Z",
                    duration_min=15.0,
                    beta_angle_deg=beta,
                    azimuth_deg=azimuth,
                    elevation_deg=0.0,
                    launch_azimuth_deg=azimuth,
                    score=score,
                ))

        # Sort by score
        windows.sort(key=lambda w: w.score, reverse=True)
        return windows

    def to_dict(self) -> Dict[str, Any]:
        return {
            "target_inc": self.target_inc,
            "target_alt": self.target_alt,
            "site_lat": self.site_lat,
            "site_lon": self.site_lon,
        }


class GroundStationScheduler:
    """Ground station pass prediction and scheduling."""

    MU = 3.986004418e14

    def _orbital_period(self, altitude_m: float) -> float:
        r = 6371000.0 + altitude_m
        return 2.0 * math.pi * math.sqrt(r ** 3 / self.MU)

    def predict_passes(
        self,
        station: GroundStation,
        satellite: Satellite,
        start_time_s: float = 0.0,
        duration_s: float = 86400.0,
        dt_s: float = 30.0,
    ) -> List[Pass]:
        """Predict passes of a satellite over a ground station."""
        passes = []
        period = self._orbital_period(satellite.altitude_m)
        n_steps = int(duration_s / dt_s)
        r = 6371000.0 + satellite.altitude_m

        in_pass = False
        pass_start = 0.0
        max_elev = 0.0

        for i in range(n_steps):
            t = start_time_s + i * dt_s
            # Satellite position (simplified circular orbit)
            ma = (2.0 * math.pi * t / period) % (2.0 * math.pi)
            sat_lat = satellite.inclination_deg * math.sin(ma)
            sat_lon = (satellite.raan_deg + math.degrees(ma)) % 360.0 - 180.0

            # Elevation angle
            dlat = sat_lat - station.latitude_deg
            dlon = sat_lon - station.longitude_deg
            dist = math.sqrt(dlat ** 2 + dlon ** 2) * 111.0  # approximate km
            alt_km = satellite.altitude_m / 1000.0
            elevation = math.degrees(math.atan2(alt_km, max(dist, 1.0)))

            if elevation >= station.min_elevation_deg:
                if not in_pass:
                    in_pass = True
                    pass_start = t
                    max_elev = elevation
                else:
                    max_elev = max(max_elev, elevation)
            else:
                if in_pass:
                    duration = t - pass_start
                    data_cap = duration * station.bandwidth_mbps * 1e6 / 8.0 / 1e9  # GB
                    passes.append(Pass(
                        station_name=station.name,
                        satellite_name=satellite.name,
                        aos_time_s=pass_start,
                        los_time_s=t,
                        max_elevation_deg=max_elev,
                        duration_s=duration,
                        data_capacity_gb=data_cap,
                    ))
                    in_pass = False

        return passes

    def optimize(
        self,
        stations: List[GroundStation],
        satellites: List[Satellite],
        mission_duration_days: int = 1,
        data_volume_gb: float = 50.0,
    ) -> ScheduleResult:
        """Optimize ground station schedule for multi-satellite fleet."""
        all_passes: List[Pass] = []
        for sat in satellites:
            for gs in stations:
                passes = self.predict_passes(gs, sat, duration_s=mission_duration_days * 86400.0)
                all_passes.extend(passes)

        # Sort by data capacity (greedy scheduling)
        all_passes.sort(key=lambda p: p.data_capacity_gb, reverse=True)

        scheduled: List[Pass] = []
        total_data = 0.0
        conflicts: List[str] = []

        for p in all_passes:
            if total_data >= data_volume_gb:
                break
            # Check for time conflicts with already-scheduled passes
            conflict = False
            for s in scheduled:
                if s.station_name == p.station_name:
                    if not (p.los_time_s < s.aos_time_s or p.aos_time_s > s.los_time_s):
                        conflict = True
                        break
            if not conflict:
                scheduled.append(p)
                total_data += p.data_capacity_gb

        total_passes = len(scheduled)
        gs_names = {s.station_name for s in stations}
        total_contact_time = sum(p.duration_s for p in scheduled)
        max_contact_time = mission_duration_days * 86400.0 * len(gs_names)
        utilization = total_contact_time / max_contact_time * 100 if max_contact_time > 0 else 0

        return ScheduleResult(
            total_passes=total_passes,
            total_data_gb=total_data,
            ground_station_utilization_pct=utilization,
            satellite_utilization_pct=min(100.0, total_data / data_volume_gb * 100),
            passes=scheduled,
            conflicts=conflicts,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"method": "predict_passes"}


class MissionTimeline:
    """Mission timeline management with resource constraint propagation."""

    def __init__(self, name: str, duration_min: float = 1440.0):
        self.name = name
        self.duration_min = duration_min
        self.events: List[TimelineEvent] = []
        self.resources: Dict[str, float] = {}  # name -> capacity

    def add_resource(self, name: str, capacity: float):
        self.resources[name] = capacity

    def add_event(self, event: TimelineEvent):
        self.events.append(event)
        self.events.sort(key=lambda e: e.start_min)

    def detect_conflicts(self) -> List[ResourceConflict]:
        """Detect resource conflicts at each timestep."""
        conflicts = []
        dt = 1.0  # 1-minute resolution

        for t_min in np.arange(0, self.duration_min, dt):
            active = [e for e in self.events if e.start_min <= t_min < e.end_min]
            for res_name, capacity in self.resources.items():
                total_demand = sum(e.resources_used.get(res_name, 0.0) for e in active)
                if total_demand > capacity * 1.01:  # 1% tolerance
                    overshoot = (total_demand - capacity) / capacity * 100
                    conflicts.append(ResourceConflict(
                        resource_name=res_name,
                        time_min=float(t_min),
                        events=[e.name for e in active],
                        total_demand=total_demand,
                        capacity=capacity,
                        overshoot_pct=overshoot,
                    ))
        return conflicts

    def peak_usage(self, resource_name: str) -> float:
        """Peak usage of a resource across the timeline."""
        peak = 0.0
        for t_min in np.arange(0, self.duration_min, 1.0):
            active = [e for e in self.events if e.start_min <= t_min < e.end_min]
            usage = sum(e.resources_used.get(resource_name, 0.0) for e in active)
            peak = max(peak, usage)
        return peak

    def total_usage(self, resource_name: str) -> float:
        """Total resource usage integrated over time."""
        total = 0.0
        for e in self.events:
            total += e.resources_used.get(resource_name, 0.0) * e.duration_min
        return total

    def get_result(self) -> TimelineResult:
        conflicts = self.detect_conflicts()
        peak = {name: self.peak_usage(name) for name in self.resources}
        return TimelineResult(
            feasible=len(conflicts) == 0,
            conflicts=conflicts,
            peak_usage=peak,
            event_count=len(self.events),
            total_duration_min=self.duration_min,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "duration_min": self.duration_min,
            "resources": self.resources,
            "events": [e.to_dict() for e in self.events],
        }


class TrajectoryDesigner:
    """Trajectory design for orbital transfers."""

    MU = 3.986004418e14

    def low_thrust_transfer(
        self,
        r_initial_m: float,
        r_final_m: float,
        incl_initial_deg: float,
        incl_final_deg: float,
        spacecraft_mass_kg: float,
        thrust_n: float,
        isp_s: float,
        dt_s: float = 60.0,
        max_iterations: int = 100000,
    ) -> TrajectoryResult:
        """Low-thrust spiral transfer with inclination change."""
        g0 = 9.80665
        mass = spacecraft_mass_kg
        r = r_initial_m
        v = math.sqrt(self.MU / r)
        inc = incl_initial_deg
        inc_target = incl_final_deg
        delta_inc = abs(inc_target - inc)

        # Spiral outward
        trajectory_points = []
        total_dv = 0.0
        step = 0

        while abs(r - r_final_m) > 1000.0 or abs(inc - inc_target) > 0.01:
            if step > max_iterations:
                break

            # Tangential thrust for orbit raising
            inc_change_rate = 0.0
            if abs(inc - inc_target) > 0.01:
                inc_change_rate = thrust_n / (mass * v) * math.cos(math.radians(inc))

            # Orbit raising acceleration
            a_tangential = thrust_n / mass

            # Update orbital elements
            r += v * dt_s * 0.01  # small radial component from thrust
            v = math.sqrt(self.MU / r)  # circular velocity at new radius

            if inc < inc_target:
                inc += inc_change_rate * dt_s
            elif inc > inc_target:
                inc -= inc_change_rate * dt_s

            # Propellant consumption
            dv_step = a_tangential * dt_s
            mass *= math.exp(-dv_step / (isp_s * g0))
            total_dv += dv_step

            if step % 1000 == 0:
                trajectory_points.append({
                    "time_s": step * dt_s,
                    "altitude_km": (r - 6371000.0) / 1000.0,
                    "velocity_ms": v,
                    "inclination_deg": inc,
                    "mass_kg": mass,
                })
            step += 1

        transfer_time_days = step * dt_s / 86400.0
        return TrajectoryResult(
            transfer_time_days=transfer_time_days,
            delta_v_ms=total_dv,
            propellant_kg=spacecraft_mass_kg - mass,
            final_semi_major_axis=r,
            final_inclination_deg=inc,
            trajectory_points=trajectory_points,
            max_thrust_n=thrust_n,
            isp_s=isp_s,
        )

    def hohmann_transfer(
        self, r1: float, r2: float, mass_kg: float, isp_s: float
    ) -> TrajectoryResult:
        """Classic Hohmann transfer."""
        g0 = 9.80665
        a_t = (r1 + r2) / 2.0
        v1 = math.sqrt(self.MU / r1)
        v2 = math.sqrt(self.MU / r2)
        v_t1 = math.sqrt(self.MU * (2.0 / r1 - 1.0 / a_t))
        v_t2 = math.sqrt(self.MU * (2.0 / r2 - 1.0 / a_t))

        dv1 = abs(v_t1 - v1)
        dv2 = abs(v2 - v_t2)
        total_dv = dv1 + dv2

        m0 = mass_kg
        mf = m0 * math.exp(-total_dv / (isp_s * g0))
        tof = math.pi * math.sqrt(a_t ** 3 / self.MU)

        return TrajectoryResult(
            transfer_time_days=tof / 86400.0,
            delta_v_ms=total_dv,
            propellant_kg=m0 - mf,
            final_semi_major_axis=r2,
            final_inclination_deg=0.0,
            trajectory_points=[],
            max_thrust_n=0.0,
            isp_s=isp_s,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"method": "low_thrust", "mu": self.MU}


class MonteCarloDispersion:
    """Monte Carlo dispersion analysis for trajectory robustness."""

    def __init__(self, nominal_trajectory: TrajectoryResult, num_runs: int = 1000):
        self.nominal = nominal_trajectory
        self.num_runs = num_runs

    def run(
        self,
        thrust_dispersion_pct: float = 5.0,
        isp_dispersion_pct: float = 2.0,
        navigation_error_m: float = 100.0,
        mass_dispersion_pct: float = 1.0,
    ) -> MonteCarloResult:
        """Run Monte Carlo dispersion analysis."""
        random.seed(42)
        np.random.seed(42)

        successes = 0
        arrival_errors = []
        dv_values = []
        time_values = []
        failure_modes: Dict[str, int] = {
            "insufficient_delta_v": 0,
            "excessive_arrival_error": 0,
            "propellant_exhausted": 0,
        }

        for _ in range(self.num_runs):
            # Perturb parameters
            thrust_factor = 1.0 + random.gauss(0, thrust_dispersion_pct / 100.0)
            isp_factor = 1.0 + random.gauss(0, isp_dispersion_pct / 100.0)
            nav_error = abs(random.gauss(0, navigation_error_m))

            # Simulate perturbed trajectory
            dv = self.nominal.delta_v_ms / thrust_factor
            arrival_error = nav_error / 1000.0  # km
            transfer_time = self.nominal.transfer_time_days * isp_factor

            dv_values.append(dv)
            arrival_errors.append(arrival_error)
            time_values.append(transfer_time)

            # Check success criteria
            if dv > self.nominal.delta_v_ms * 1.1:
                failure_modes["insufficient_delta_v"] += 1
            elif arrival_error > 10.0:  # 10 km threshold
                failure_modes["excessive_arrival_error"] += 1
            else:
                successes += 1

        dv_arr = np.array(dv_values)
        err_arr = np.array(arrival_errors)
        time_arr = np.array(time_values)

        return MonteCarloResult(
            num_runs=self.num_runs,
            success_count=successes,
            success_probability=successes / self.num_runs,
            arrival_error_mean_km=float(np.mean(err_arr)),
            arrival_error_3sigma_km=float(np.percentile(err_arr, 99.7)),
            delta_v_mean_ms=float(np.mean(dv_arr)),
            delta_v_std_ms=float(np.std(dv_arr)),
            transfer_time_std_days=float(np.std(time_arr)),
            failure_modes=failure_modes,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"num_runs": self.num_runs, "nominal_dv": self.nominal.delta_v_ms}


class RiskAssessmentMatrix:
    """Risk assessment and FMEA-lite analysis."""

    def __init__(self):
        self.risks: List[RiskItem] = []

    def add_risk(
        self,
        id: str,
        description: str,
        likelihood: float,
        severity: float,
        mitigation: str = "",
    ) -> RiskItem:
        """Add a risk item with automatic scoring."""
        risk_score = likelihood * severity

        if risk_score < 1.0:
            level = RiskLevel.NEGLIGIBLE
        elif risk_score < 3.0:
            level = RiskLevel.LOW
        elif risk_score < 7.0:
            level = RiskLevel.MEDIUM
        elif risk_score < 15.0:
            level = RiskLevel.HIGH
        else:
            level = RiskLevel.CRITICAL

        item = RiskItem(
            id=id,
            description=description,
            likelihood=likelihood,
            severity=severity,
            risk_score=risk_score,
            risk_level=level,
            mitigation=mitigation,
        )
        self.risks.append(item)
        return item

    def top_risks(self, n: int = 10) -> List[RiskItem]:
        return sorted(self.risks, key=lambda r: r.risk_score, reverse=True)[:n]

    def summary_by_level(self) -> Dict[str, int]:
        counts = {level.value: 0 for level in RiskLevel}
        for r in self.risks:
            counts[r.risk_level.value] += 1
        return counts

    def risk_burial_chart(self) -> List[Dict[str, Any]]:
        """Generate risk burial chart data."""
        sorted_risks = sorted(self.risks, key=lambda r: r.risk_score, reverse=True)
        cumulative = 0.0
        total = sum(r.risk_score for r in sorted_risks)
        chart = []
        for r in sorted_risks:
            cumulative += r.risk_score
            chart.append({
                "id": r.id,
                "risk_score": r.risk_score,
                "cumulative_fraction": cumulative / total if total > 0 else 0,
            })
        return chart

    def fault_tree_probability(
        self,
        basic_events: Dict[str, float],
        gates: List[Dict[str, Any]],
    ) -> float:
        """Simple fault tree computation."""
        # gates: list of {"type": "AND"/"OR", "inputs": [event_ids], "output": gate_id}
        computed = dict(basic_events)
        for gate in gates:
            inputs = [computed.get(i, 0.0) for i in gate["inputs"]]
            if gate["type"] == "OR":
                result = 1.0 - math.prod(1.0 - p for p in inputs)
            elif gate["type"] == "AND":
                result = math.prod(inputs)
            else:
                result = 0.0
            computed[gate["output"]] = result
        # Top event is the last gate's output
        return computed.get(gates[-1]["output"], 0.0) if gates else 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_risks": len(self.risks),
            "summary": self.summary_by_level(),
            "risks": [r.to_dict() for r in self.risks],
        }


class ContingencyPlanner:
    """Contingency plan management and decision tree execution."""

    def __init__(self):
        self.plans: List[ContingencyPlan] = []

    def add_plan(self, plan: ContingencyPlan):
        self.plans.append(plan)

    def find_plan(self, anomaly_class: AnomalyClass) -> Optional[ContingencyPlan]:
        for p in self.plans:
            if p.anomaly_class == anomaly_class:
                return p
        return None

    def evaluate_decision_tree(
        self,
        tree: Dict[str, Any],
        conditions: Dict[str, bool],
    ) -> List[str]:
        """Walk a decision tree and return actions to execute."""
        actions = []
        node = tree
        while "action" in node or "branches" in node:
            if "action" in node:
                actions.append(node["action"])
                break
            if "branches" in node:
                for branch in node["branches"]:
                    if conditions.get(branch["condition"], False):
                        node = branch["next"]
                        break
                else:
                    break
        return actions

    def default_contingency_plans(self) -> List[ContingencyPlan]:
        """Generate standard contingency plans."""
        plans = [
            ContingencyPlan(
                anomaly_class=AnomalyClass.CAUTION,
                trigger_condition="Single telemetry parameter out of limits",
                response_actions=[
                    "Log anomaly in operations database",
                    "Notify flight director",
                    "Increase monitoring cadence to 1-minute",
                    "Review trending data for 24-hour context",
                ],
                decision_tree={
                    "branches": [
                        {"condition": "trending_worsening", "next": {"action": "Escalate to WARNING"}},
                        {"condition": "trending_stable", "next": {"action": "Continue monitoring"}},
                    ]
                },
                time_limit_min=30.0,
            ),
            ContingencyPlan(
                anomaly_class=AnomalyClass.WARNING,
                trigger_condition="Multiple parameters out of limits or single critical parameter",
                response_actions=[
                    "Activate anomaly response team",
                    "Halt non-essential operations",
                    "Begin anomaly investigation procedure",
                    "Prepare for safe mode entry if needed",
                ],
                decision_tree={
                    "branches": [
                        {"condition": "safe_mode_required", "next": {"action": "Enter safe mode"}},
                        {"condition": "recovery_feasible", "next": {"action": "Attempt recovery procedure"}},
                    ]
                },
                time_limit_min=15.0,
                required_resources=["anomaly_response_team", "ground_station_priority"],
            ),
            ContingencyPlan(
                anomaly_class=AnomalyClass.EMERGENCY,
                trigger_condition="Loss of contact or critical system failure",
                response_actions=[
                    "Activate emergency operations center",
                    "Attempt contact on all frequencies",
                    "Deploy recovery assets",
                    "Notify customer and regulatory authorities",
                ],
                decision_tree={"action": "Full emergency response"},
                time_limit_min=5.0,
                required_resources=["emergency_ops_center", "all_ground_stations"],
            ),
        ]
        self.plans.extend(plans)
        return plans

    def to_dict(self) -> Dict[str, Any]:
        return {
            "num_plans": len(self.plans),
            "plans": [p.to_dict() for p in self.plans],
        }


class PayloadIntegrator:
    """Payload scheduling and data pipeline management."""

    def __init__(self, total_data_storage_gb: float = 256.0):
        self.total_storage = total_data_storage_gb
        self.schedules: List[PayloadSchedule] = []
        self.current_usage_gb = 0.0

    def add_schedule(self, schedule: PayloadSchedule):
        if self.current_usage_gb + schedule.data_volume_gb <= self.total_storage:
            self.schedules.append(schedule)
            self.current_usage_gb += schedule.data_volume_gb
        else:
            raise ValueError(f"Insufficient storage: need {schedule.data_volume_gb:.1f} GB, "
                             f"available {self.total_storage - self.current_usage_gb:.1f} GB")

    def total_data_volume(self) -> float:
        return sum(s.data_volume_gb for s in self.schedules)

    def total_power_time_product(self) -> float:
        """Power × time product (W·min) for energy budget."""
        return sum(s.power_w * s.duration_min for s in self.schedules)

    def data_downlink_schedule(self, bandwidth_mbps: float) -> List[Dict[str, Any]]:
        """Compute data downlink schedule sorted by priority."""
        total_bits = self.total_data_volume() * 8e9
        downlink_rate_bps = bandwidth_mbps * 1e6
        downlink_time_s = total_bits / downlink_rate_bps

        schedule = []
        t = 0.0
        for s in sorted(self.schedules, key=lambda x: x.data_volume_gb, reverse=True):
            bits = s.data_volume_gb * 8e9
            duration = bits / downlink_rate_bps
            schedule.append({
                "instrument": s.instrument_name,
                "start_s": t,
                "duration_s": duration,
                "data_gb": s.data_volume_gb,
            })
            t += duration

        return schedule

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_storage_gb": self.total_storage,
            "used_gb": self.current_usage_gb,
            "num_schedules": len(self.schedules),
        }


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

def main():
    """Demonstrate the mission planning toolkit."""
    print("=" * 70)
    print("MISSION PLANNING TOOLKIT — DEMONSTRATION")
    print("=" * 70)

    # 1. Launch Windows
    print("\n--- Launch Window Calculation ---")
    lwc = LaunchWindowCalculator(
        target_orbit_inclination_deg=51.6,
        target_orbit_altitude_m=420000.0,
        launch_site_lat_deg=28.5,
        launch_site_lon_deg=-80.6,
    )
    constraints = LaunchConstraints(
        beta_angle_min_deg=-60.0,
        beta_angle_max_deg=60.0,
        elevation_min_deg=5.0,
    )
    windows = lwc.compute_windows("2026-07-01", "2026-07-31", constraints)
    print(f"Found {len(windows)} candidate windows")
    for w in windows[:3]:
        print(f"  {w.start_time}: β={w.beta_angle_deg:.1f}°, az={w.azimuth_deg:.1f}°, score={w.score:.3f}")

    # 2. Ground Station Scheduling
    print("\n--- Ground Station Pass Scheduling ---")
    gs_sched = GroundStationScheduler()
    stations = [
        GroundStation("Kourou", 5.2, -52.7, 10.0),
        GroundStation("Svalbard", 78.2, 15.4, 500.0),
        GroundStation("Punchbowl", -34.0, 138.7, 50.0),
    ]
    sats = [
        Satellite("SAT-A", 550000.0, 53.0),
        Satellite("SAT-B", 550000.0, 53.0),
    ]
    schedule = gs_sched.optimize(stations, sats, mission_duration_days=1, data_volume_gb=50.0)
    print(f"Total passes: {schedule.total_passes}, Data: {schedule.total_data_gb:.1f} GB")
    print(f"GS utilization: {schedule.ground_station_utilization_pct:.1f}%")

    # 3. Mission Timeline
    print("\n--- Mission Timeline ---")
    tl = MissionTimeline("EO-1 Mission Day 1")
    tl.add_resource("power_w", 120.0)
    tl.add_resource("data_storage_gb", 256.0)
    tl.add_event(TimelineEvent("Solar array power-up", 0, 5, {"power_w": 120.0}))
    tl.add_event(TimelineEvent("Imaging pass", 30, 15, {"power_w": 85.0, "data_storage_gb": 12.0}))
    tl.add_event(TimelineEvent("Data downlink", 120, 10, {"power_w": 60.0}))
    tl.add_event(TimelineEvent("Battery charge", 200, 30, {"power_w": 100.0}))

    result = tl.get_result()
    print(f"Feasible: {result.feasible}, Events: {result.event_count}")
    print(f"Peak power: {result.peak_usage.get('power_w', 0):.0f} W")
    print(f"Data usage: {result.peak_usage.get('data_storage_gb', 0):.1f} GB")

    # 4. Trajectory Design
    print("\n--- Trajectory Design ---")
    td = TrajectoryDesigner()
    hohmann = td.hohmann_transfer(6771000.0, 42164000.0, 500.0, 311.0)
    print(f"Hohmann: Δv={hohmann.delta_v_ms:.0f} m/s, propellant={hohmann.propellant_kg:.1f} kg")
    print(f"Transfer time: {hohmann.transfer_time_days*24:.1f} hours")

    # 5. Monte Carlo
    print("\n--- Monte Carlo Dispersion ---")
    mc = MonteCarloDispersion(hohmann, num_runs=500)
    mc_result = mc.run(thrust_dispersion_pct=5.0, isp_dispersion_pct=2.0, navigation_error_m=100.0)
    print(f"Success probability: {mc_result.success_probability*100:.1f}%")
    print(f"3-sigma arrival error: {mc_result.arrival_error_3sigma_km:.1f} km")
    print(f"DV mean: {mc_result.delta_v_mean_ms:.1f} ± {mc_result.delta_v_std_ms:.1f} m/s")

    # 6. Risk Assessment
    print("\n--- Risk Assessment ---")
    risk_matrix = RiskAssessmentMatrix()
    risk_matrix.add_risk("R001", "Launch vehicle failure", 0.02, 5.0, "Vehicle reliability program")
    risk_matrix.add_risk("R002", "Ground station outage", 0.15, 3.0, "Redundant stations")
    risk_matrix.add_risk("R003", "ADCs failure", 0.05, 4.0, "Redundant sensors")
    risk_matrix.add_risk("R004", "Solar array degradation", 0.3, 2.0, "Conservative design margins")
    risk_matrix.add_risk("R005", "Debris collision", 0.01, 5.0, "Maneuver capability")

    print(f"Total risks: {len(risk_matrix.risks)}")
    print(f"Summary: {risk_matrix.summary_by_level()}")
    for r in risk_matrix.top_risks(3):
        print(f"  {r.id}: {r.description} — score={r.risk_score:.2f} ({r.risk_level.value})")

    # 7. Contingency Planning
    print("\n--- Contingency Planning ---")
    cp = ContingencyPlanner()
    plans = cp.default_contingency_plans()
    for p in plans:
        print(f"  {p.anomaly_class.value}: {len(p.response_actions)} actions, "
              f"time limit: {p.time_limit_min:.0f} min")

    # Evaluate a decision tree
    actions = cp.evaluate_decision_tree(
        plans[0].decision_tree,
        {"trending_worsening": True, "trending_stable": False},
    )
    print(f"Decision tree actions: {actions}")

    # 8. Payload Integration
    print("\n--- Payload Integration ---")
    pi = PayloadIntegrator(total_data_storage_gb=256.0)
    pi.add_schedule(PayloadSchedule("PAN", "imaging", 0, 15, 12.0, 85.0))
    pi.add_schedule(PayloadSchedule("TIR", "thermal", 30, 10, 5.0, 45.0))
    pi.add_schedule(PayloadSchedule("SAR", "radar", 60, 20, 20.0, 120.0))
    print(f"Total data: {pi.total_data_volume():.1f} GB / {pi.total_storage:.1f} GB")
    print(f"Power-time product: {pi.total_power_time_product():.0f} W·min")
    dl = pi.data_downlink_schedule(150.0)
    print(f"Downlink schedule: {len(dl)} segments")
    for d in dl[:3]:
        print(f"  {d['instrument']}: {d['data_gb']:.1f} GB in {d['duration_s']:.0f} s")

    # Serialization
    print("\n--- Serialization ---")
    risk_dict = risk_matrix.to_dict()
    print(f"Risk matrix serialized: {risk_dict['total_risks']} risks")

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

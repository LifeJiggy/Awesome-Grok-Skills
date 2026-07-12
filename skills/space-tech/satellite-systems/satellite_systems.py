"""
Satellite Systems Toolkit
Constellation management, orbit determination, ADCS, power/thermal subsystems, link budgets, debris tracking.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

import numpy as np


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

G0 = 9.80665
MU_EARTH = 3.986004418e14
R_EARTH = 6_371_000
J2 = 1.08263e-3
AU = 1.496e11
DEG2RAD = math.pi / 180.0
RAD2DEG = 180.0 / math.pi
SIGMA_SB = 5.670374419e-8  # Stefan-Boltzmann constant


class OrbitType(Enum):
    LEO = "leo"
    MEO = "meo"
    GEO = "geo"
    HEO = "heo"
    SSO = "sso"
    GTO = "gto"


class ADCSMode(Enum):
    IDLE = "idle"
    DETUMBLE = "detumble"
    SUN_SEARCH = "sun_search"
    FINE_POINTING = "fine_pointing"
    SLEW = "slew"


@dataclass
class SatelliteState:
    """Position and velocity state of a satellite."""
    position: np.ndarray  # ECI [x, y, z] meters
    velocity: np.ndarray  # ECI [vx, vy, vz] m/s
    mass: float = 100.0  # kg
    epoch: float = 0.0  # seconds from reference

    @property
    def radius(self) -> float:
        return np.linalg.norm(self.position)

    @property
    def speed(self) -> float:
        return np.linalg.norm(self.velocity)

    @property
    def altitude(self) -> float:
        return self.radius - R_EARTH

    def orbital_energy(self) -> float:
        mu = MU_EARTH
        return self.speed**2 / 2.0 - mu / self.radius

    def specific_angular_momentum(self) -> np.ndarray:
        return np.cross(self.position, self.velocity)

    def eccentricity_vector(self) -> np.ndarray:
        mu = MU_EARTH
        h = self.specific_angular_momentum()
        return (np.cross(self.velocity, h) / mu) - self.position / self.radius


@dataclass
class TLEData:
    """Two-Line Element set."""
    satellite_name: str
    epoch_year: int
    epoch_day: float
    inclination_deg: float
    raan_deg: float
    eccentricity: float
    argp_deg: float
    mean_anomaly_deg: float
    mean_motion_rev_day: float
    bstar: float
    revolution_number: int

    @property
    def period_minutes(self) -> float:
        return 1440.0 / self.mean_motion_rev_day

    @property
    def altitude_km(self) -> float:
        mu = MU_EARTH
        n = self.mean_motion_rev_day * 2 * math.pi / 86400.0
        a = (mu / n**2) ** (1.0 / 3.0)
        return (a - R_EARTH) / 1000.0


@dataclass
class ConjunctionEvent:
    """Conjunction assessment result."""
    time_to_closest_approach_hours: float
    miss_distance_m: float
    probability_of_collision: float
    object_a_id: str
    object_b_id: str
    relative_velocity_mps: float
    recommended_action: str


@dataclass
class PowerBudgetResult:
    """Power budget computation result."""
    solar_generation_bol_w: float
    solar_generation_eol_w: float
    average_load_w: float
    eclipse_load_w: float
    depth_of_discharge: float
    battery_cycles_per_day: float
    margin_w: float
    battery_capacity_required_wh: float


# ---------------------------------------------------------------------------
# Constellation Management
# ---------------------------------------------------------------------------

class ConstellationManager:
    """Satellite constellation design and analysis."""

    def __albertrian_period(self, altitude_m: float) -> float:
        a = R_EARTH + altitude_m
        return 2 * math.pi * math.sqrt(a**3 / MU_EARTH)

    def walker_delta(
        self,
        total_satellites: int,
        orbital_planes: int,
        inclination_deg: float,
        altitude_km: float,
        phasing_offset: int = 0,
    ) -> dict[str, Any]:
        """Design a Walker delta constellation."""
        sats_per_plane = total_satellites // orbital_planes
        if sats_per_plane * orbital_planes != total_satellites:
            raise ValueError(
                f"Total sats ({total_satellites}) must be divisible by planes ({orbital_planes})"
            )

        raan_spacing = 360.0 / orbital_planes
        ta_spacing = 360.0 / sats_per_plane
        period = self.__albertrian_period(altitude_km * 1000)

        sats = []
        for plane_idx in range(orbital_planes):
            raan = plane_idx * raan_spacing
            for sat_idx in range(sats_per_plane):
                ta = sat_idx * ta_spacing + phasing_offset * plane_idx * ta_spacing / orbital_planes
                sats.append({
                    "plane": plane_idx,
                    "sat_index": sat_idx,
                    "raan_deg": raan % 360,
                    "true_anomaly_deg": ta % 360,
                    "inclination_deg": inclination_deg,
                    "altitude_km": altitude_km,
                })

        return {
            "total_sats": len(sats),
            "num_planes": orbital_planes,
            "sats_per_plane": sats_per_plane,
            "raan_spacing_deg": raan_spacing,
            "ta_spacing_deg": ta_spacing,
            "period_hours": period / 3600.0,
            "inclination_deg": inclination_deg,
            "altitude_km": altitude_km,
            "satellites": sats,
        }

    def coverage_fraction(
        self,
        altitude_km: float,
        num_satellites: int,
        elevation_mask_deg: float = 10.0,
    ) -> float:
        """Estimate single-coverage fraction for a constellation."""
        h = altitude_km * 1000
        r = R_EARTH + h
        gamma = math.acos(R_EARTH / r) - elevation_mask_deg * DEG2RAD
        if gamma <= 0:
            return 0.0
        coverage_area = 2 * math.pi * R_EARTH**2 * (1 - math.cos(gamma))
        earth_area = 4 * math.pi * R_EARTH**2
        single_coverage = min(1.0, num_satellites * coverage_area / earth_area)
        return single_coverage

    def ground_track_repeat(
        self, altitude_km: float, inclination_deg: float,
        max_days: int = 30,
    ) -> dict[str, Any]:
        """Compute ground-track repeat cycle parameters."""
        a = (R_EARTH + altitude_km * 1000)
        n = math.sqrt(MU_EARTH / a**3)  # rad/s
        earth_rotation = 7.2921159e-5  # rad/s
        n_rel = n - earth_rotation

        day_period = 2 * math.pi / earth_rotation
        orbit_period = 2 * math.pi / n
        orbits_per_day = day_period / orbit_period

        for days in range(1, max_days + 1):
            orbits_total = orbits_per_day * days
            nearest_int = round(orbits_total)
            if abs(orbits_total - nearest_int) < 0.01:
                return {
                    "repeat_days": days,
                    "orbits_per_cycle": nearest_int,
                    "orbit_period_minutes": orbit_period / 60.0,
                    "orbits_per_day": orbits_per_day,
                }

        return {"repeat_days": -1, "orbit_period_minutes": orbit_period / 60.0}

    def inter_satellite_links(
        self, constellation_sats: list[dict], max_range_km: float = 5000
    ) -> list[dict[str, Any]]:
        """Compute ISL connectivity for a constellation."""
        links = []
        for i, sat_a in enumerate(constellation_sats):
            for j, sat_b in enumerate(constellation_sats):
                if j <= i:
                    continue
                a_pos = np.array(self._sat_position(sat_a))
                b_pos = np.array(self._sat_position(sat_b))
                dist = np.linalg.norm(a_pos - b_pos) / 1000

                if dist <= max_range_km:
                    is_intra_plane = sat_a["plane"] == sat_b["plane"]
                    links.append({
                        "sat_a": i, "sat_b": j,
                        "range_km": dist,
                        "type": "intra-plane" if is_intra_plane else "inter-plane",
                    })
        return links

    @staticmethod
    def _sat_position(sat: dict) -> list[float]:
        """Simplified position from orbital elements (circular orbit)."""
        alt = sat["altitude_km"] * 1000
        r = R_EARTH + alt
        ta = sat["true_anomaly_deg"] * DEG2RAD
        inc = sat["inclination_deg"] * DEG2RAD
        raan = sat["raan_deg"] * DEG2RAD
        x = r * (math.cos(raan) * math.cos(ta) - math.sin(raan) * math.sin(ta) * math.cos(inc))
        y = r * (math.sin(raan) * math.cos(ta) + math.cos(raan) * math.sin(ta) * math.cos(inc))
        z = r * math.sin(ta) * math.sin(inc)
        return [x, y, z]


# ---------------------------------------------------------------------------
# Orbit Determination
# ---------------------------------------------------------------------------

class OrbitDetermination:
    """Orbit determination from tracking observations."""

    def __init__(self, body: str = "earth"):
        self.mu = MU_EARTH if body == "earth" else 3.986e14

    def state_transition_matrix(
        self, state: np.ndarray, dt: float
    ) -> np.ndarray:
        """Approximate state transition matrix (STM) using Keplerian approximation."""
        r = state[:3]
        v = state[3:]
        r_mag = np.linalg.norm(r)
        v_mag = np.linalg.norm(v)

        n = math.sqrt(self.mu / r_mag**3)

        phi = np.eye(6)
        phi[0, 3] = dt
        phi[1, 4] = dt
        phi[2, 5] = dt
        phi[3, 0] = -n**2 * dt
        phi[4, 1] = -n**2 * dt
        phi[5, 2] = -n**2 * dt

        return phi

    def range_observation(self, state: np.ndarray, station_ecef: np.ndarray) -> float:
        """Compute range from ground station to satellite."""
        sat_pos = state[:3]
        r_vec = sat_pos - station_ecef
        return np.linalg.norm(r_vec)

    def range_rate_observation(self, state: np.ndarray, station_ecef: np.ndarray) -> float:
        """Compute range rate (Doppler)."""
        sat_pos = state[:3]
        sat_vel = state[3:]
        r_vec = sat_pos - station_ecef
        r_mag = np.linalg.norm(r_vec)
        return np.dot(sat_vel, r_vec) / r_mag

    def batch_least_squares(
        self,
        observations: list[tuple[float, float, float]],
        initial_guess: np.ndarray,
        max_iterations: int = 20,
        tolerance: float = 1.0,
    ) -> dict[str, Any]:
        """Batch least-squares orbit determination from range observations."""
        state = initial_guess.copy()
        station = np.array([R_EARTH, 0, 0])  # simplified station position

        for iteration in range(max_iterations):
            residuals = []
            jacobians = []

            for t, range_obs, _ in observations:
                phi = self.state_transition_matrix(state, t)
                predicted_state = phi @ state
                range_pred = self.range_observation(predicted_state, station)
                residual = range_obs - range_pred
                residuals.append(residual)

                dr = predicted_state[:3] - station
                dr_mag = np.linalg.norm(dr)
                h_range = np.zeros(6)
                h_range[:3] = dr / dr_mag
                jacobians.append(h_range @ phi)

            residuals = np.array(residuals)
            jacobians = np.array(jacobians)
            rms_before = np.sqrt(np.mean(residuals**2))

            delta = np.linalg.lstsq(jacobians, residuals, rcond=None)[0]
            state += delta

            rms_after = np.sqrt(np.mean((residuals - jacobians @ delta)**2))
            if rms_after < tolerance:
                break

        return {
            "position": state[:3],
            "velocity": state[3:],
            "residual_rms": rms_after,
            "iterations": iteration + 1,
            "converged": rms_after < tolerance,
        }

    def kepler_propagation(self, state0: np.ndarray, dt: float) -> np.ndarray:
        """Propagate state using Kepler's equation (two-body)."""
        r0 = state0[:3]
        v0 = state0[3:]
        r_mag = np.linalg.norm(r0)
        v_mag = np.linalg.norm(v0)

        vr = np.dot(r0, v0) / r_mag
        alpha = 2.0 / r_mag - v_mag**2 / self.mu

        if abs(alpha) < 1e-10:
            f = 1.0 - self.mu / r_mag**2 * dt
            g = dt
        else:
            chi = math.sqrt(abs(alpha)) * dt if alpha > 0 else -math.sqrt(abs(-alpha)) * dt

            for _ in range(20):
                chi_new = chi
                if alpha > 0:
                    psi = alpha * chi**2
                    c_chi = 1 - psi / 2
                    s_chi = chi * (1 - psi / 6)
                else:
                    psi = -alpha * chi**2
                    c_chi = math.cosh(chi * math.sqrt(-alpha))
                    s_chi = math.sinh(chi * math.sqrt(-alpha)) / math.sqrt(-alpha)

                r_chi = r_mag * c_chi + vr * s_chi + math.sqrt(self.mu) * chi**2 * c_chi / r_mag
                delta_chi = (dt - chi / math.sqrt(self.mu) * r_chi - chi**3 * s_chi / 6) / r_chi
                chi = chi_new + delta_chi

            if alpha > 0:
                psi = alpha * chi**2
                c_chi = 1 - psi / 2
                s_chi = chi * (1 - psi / 6)
            else:
                psi = -alpha * chi**2
                c_chi = math.cosh(chi * math.sqrt(-alpha))
                s_chi = math.sinh(chi * math.sqrt(-alpha)) / math.sqrt(-alpha)

            f = 1 - chi**2 * self.mu / (r_mag * r_chi)
            g = chi * r_mag * c_chi / math.sqrt(self.mu) + chi**2 * s_chi / r_chi * vr

        r1 = f * r0 + g * v0
        r1_mag = np.linalg.norm(r1)
        f_dot = math.sqrt(self.mu) / (r_mag * r1_mag) * (alpha * chi * r_mag * s_chi - chi)
        g_dot = 1 - chi**2 * self.mu / (r1_mag * r_chi)
        v1 = f_dot * r0 + g_dot * v0

        return np.concatenate([r1, v1])


# ---------------------------------------------------------------------------
# Attitude Control
# ---------------------------------------------------------------------------

class AttitudeController:
    """Satellite attitude determination and control system."""

    def __init__(
        self,
        spacecraft_inertia: Optional[np.ndarray] = None,
    ):
        self.inertia = spacecraft_inertia if spacecraft_inertia is not None else np.diag([100.0, 80.0, 60.0])

    def gravity_gradient_torque(self, position_eci: np.ndarray, inertia: np.ndarray) -> np.ndarray:
        """Compute gravity gradient torque."""
        mu = MU_EARTH
        r = np.linalg.norm(position_eci)
        r_hat = position_eci / r

        inertia_diff = inertia[2, 2] - inertia[0, 0]
        torque = 3 * mu / r**3 * inertia_diff * np.array([
            r_hat[1] * r_hat[2],
            r_hat[0] * r_hat[2],
            0,
        ])
        return torque

    def magnetic_torque(
        self, magnetic_field_nT: np.ndarray, dipole_am2: np.ndarray
    ) -> np.ndarray:
        """Torque from magnetic torquer interacting with geomagnetic field."""
        b_field = magnetic_field_nT * 1e-9  # convert to T
        return np.cross(dipole_am2, b_field)

    def size_reaction_wheels(
        self,
        desired_pointing_accuracy_deg: float,
        max_slew_rate_deg_per_sec: float,
        max_torque_nm: float,
        momentum_storage_required_nm_s: float,
        spacecraft_inertia_kgm2: Optional[np.ndarray] = None,
        num_wheels: int = 4,
    ) -> dict[str, Any]:
        """Size a reaction wheel assembly."""
        if spacecraft_inertia_kgm2 is None:
            spacecraft_inertia_kgm2 = self.inertia

        max_inertia = np.max(np.diag(spacecraft_inertia_kgm2))

        max_torque_per_wheel = max_torque_nm
        max_speed_rad = max_slew_rate_deg_per_sec * DEG2RAD * 1.5
        max_momentum = momentum_storage_required_nm_s

        wheel_mass_estimate = max_torque_per_wheel * 0.8 + max_momentum * 0.05

        configurations = {3: "triad", 4: "pyramid", 5: "double-pyramid"}
        config_name = configurations.get(num_wheels, f"{num_wheels}-wheel")

        total_mass = wheel_mass_estimate * num_wheels
        power_per_wheel = max_torque_per_wheel * max_speed_rad * 0.6  # efficiency
        total_power = power_per_wheel * num_wheels

        max_speed_rpm = max_speed_rad * 60 / (2 * math.pi)

        return {
            "configuration": config_name,
            "num_wheels": num_wheels,
            "max_torque_per_wheel_nm": max_torque_per_wheel,
            "max_speed_rpm": max_speed_rpm,
            "max_momentum_per_wheel_nms": max_momentum / num_wheels,
            "total_mass_kg": total_mass,
            "power_watts": total_power,
            "pointing_accuracy_deg": desired_pointing_accuracy_deg,
        }

    def detumble_bdot_controller(
        self,
        angular_velocity: np.ndarray,
        magnetic_field: np.ndarray,
        gain: float = 100.0,
    ) -> np.ndarray:
        """B-dot detumbling control law — compute torquer dipole moment."""
        b_hat = magnetic_field / np.linalg.norm(magnetic_field)
        omega_dot = np.cross(angular_velocity, magnetic_field) * 0
        dipole = -gain * (np.dot(angular_velocity, magnetic_field)) * b_hat
        return dipole

    def pd_controller(
        self,
        attitude_error_rad: np.ndarray,
        angular_velocity: np.ndarray,
        kp: float = 10.0,
        kd: float = 5.0,
        inertia: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """PD attitude control law."""
        if inertia is None:
            inertia = self.inertia
        torque = -(kp * attitude_error_rad + kd * angular_velocity)
        return torque


# ---------------------------------------------------------------------------
# Power Subsystem
# ---------------------------------------------------------------------------

class PowerSubsystem:
    """Satellite power subsystem modeling."""

    def __init__(
        self,
        solar_array_area_m2: float,
        solar_cell_efficiency: float = 0.30,
        eclipse_fraction: float = 0.35,
        average_power_consumption_w: float = 50.0,
        battery_capacity_wh: float = 200.0,
        degradation_factor: float = 0.90,
        sun_flux_w_m2: float = 1361.0,
        temperature_coeff: float = -0.004,
        cell_temperature_c: float = 60.0,
    ):
        self.array_area = solar_array_area_m2
        self.efficiency = solar_cell_efficiency
        self.eclipse_fraction = eclipse_fraction
        self.avg_power = average_power_consumption_w
        self.battery_capacity = battery_capacity_wh
        self.degradation = degradation_factor
        self.sun_flux = sun_flux_w_m2
        self.temp_coeff = temperature_coeff
        self.cell_temp = cell_temperature_c

    def compute_budget(self) -> PowerBudgetResult:
        """Compute full power budget."""
        temp_factor = 1 + self.temp_coeff * (self.cell_temp - 25)
        effective_eff = self.efficiency * temp_factor * self.degradation

        solar_gen_bol = self.sun_flux * self.array_area * self.efficiency
        solar_gen_eol = self.sun_flux * self.array_area * effective_eff

        eclipse_fraction = self.eclipse_fraction
        sun_fraction = 1 - eclipse_fraction

        avg_gen = solar_gen_eol * sun_fraction
        avg_load = self.avg_power

        eclipse_load = avg_load * eclipse_fraction / sun_fraction if sun_fraction > 0 else avg_load
        dod = eclipse_load * eclipse_fraction * 24 / self.battery_capacity if self.battery_capacity > 0 else 0
        dod = min(dod, 0.8)

        cycles_per_day = 1.0 if eclipse_fraction > 0 else 0
        margin = solar_gen_eol - avg_load

        battery_required = eclipse_load * eclipse_fraction * 24

        return PowerBudgetResult(
            solar_generation_bol_w=solar_gen_bol,
            solar_generation_eol_w=solar_gen_eol,
            average_load_w=avg_load,
            eclipse_load_w=eclipse_load,
            depth_of_discharge=dod,
            battery_cycles_per_day=cycles_per_day,
            margin_w=margin,
            battery_capacity_required_wh=battery_required,
        )

    def eclipse_duration(self, altitude_km: float, inclination_deg: float) -> float:
        """Estimate eclipse duration fraction."""
        r = (R_EARTH + altitude_km * 1000) / R_EARTH
        if r < 1:
            return 0.0
        cos_beta = math.sqrt(1 - (1 / r)**2) if r > 1 else 0.0
        eclipse_angle = math.acos(max(-1, min(1, cos_beta)))
        eclipse_fraction = eclipse_angle / math.pi
        return eclipse_fraction


# ---------------------------------------------------------------------------
# Link Budget
# ---------------------------------------------------------------------------

class LinkBudget:
    """Communication link budget analysis."""

    def __init__(
        self,
        tx_power_watts: float,
        tx_gain_dbi: float,
        rx_gain_dbi: float,
        frequency_ghz: float,
        distance_km: float,
        tx_line_loss_db: float = 0.5,
        rx_line_loss_db: float = 0.3,
        pointing_loss_db: float = 0.5,
        system_noise_temperature_k: float = 300.0,
        required_cn0_db_hz: float = 50.0,
        implementation_margin_db: float = 2.0,
    ):
        self.tx_power = tx_power_watts
        self.tx_gain = tx_gain_dbi
        self.rx_gain = rx_gain_dbi
        self.frequency = frequency_ghz
        self.distance = distance_km
        self.tx_loss = tx_line_loss_db
        self.rx_loss = rx_line_loss_db
        self.pointing_loss = pointing_loss_db
        self.noise_temp = system_noise_temperature_k
        self.req_cn0 = required_cn0_db_hz
        self.impl_margin = implementation_margin_db

    def free_space_path_loss(self) -> float:
        """FSPL in dB."""
        c = 3e8
        freq_hz = self.frequency * 1e9
        d_m = self.distance * 1000
        return 20 * math.log10(4 * math.pi * d_m * freq_hz / c)

    def eirp(self) -> float:
        """Effective Isotropic Radiated Power in dBW."""
        return 10 * math.log10(self.tx_power) + self.tx_gain - self.tx_loss

    def g_over_t(self) -> float:
        """Figure of merit G/T in dB/K."""
        k_boltzmann = 10 * math.log10(1.380649e-23)
        return self.rx_gain - self.rx_loss - 10 * math.log10(self.noise_temp)

    def compute(self) -> dict[str, float]:
        """Compute full link budget."""
        eirp_dbw = self.eirp()
        fspl = self.free_space_path_loss()
        gt = self.g_over_t()
        k_db = 10 * math.log10(1.380649e-23)

        cn0 = eirp_dbw - fspl + gt - k_db - self.pointing_loss - self.impl_margin
        margin = cn0 - self.req_cn0

        bw_mhz = 36.0
        cn_db = cn0 - 10 * math.log10(bw_mhz * 1e6)

        return {
            "eirp_dbw": eirp_dbw,
            "fspl_db": fspl,
            "gt_db_k": gt,
            "cn0_db_hz": cn0,
            "cn_db": cn_db,
            "margin_db": margin,
            "rain_attenuation_db": 0.0,
            "pointing_loss_db": self.pointing_loss,
            "system_noise_temp_k": self.noise_temp,
            "bandwidth_mhz": bw_mhz,
        }

    def rain_fade_attenuation(
        self, rain_rate_mm_hr: float, elevation_deg: float
    ) -> float:
        """ITU-R P.618 rain attenuation estimate (dB)."""
        k = 0.0751
        alpha = 0.744
        a_rain = k * rain_rate_mm_hr**alpha
        slant_path = 35000 / math.sin(elevation_deg * DEG2RAD) if elevation_deg > 0 else 35000
        attenuation = a_rain * slant_path / 1000
        return attenuation


# ---------------------------------------------------------------------------
# Space Debris Tracking
# ---------------------------------------------------------------------------

class DebrisTracker:
    """Space debris tracking and conjunction assessment."""

    def __init__(self, catalog: Optional[list[TLEData]] = None):
        self.catalog = catalog or []

    def propagate_tle_sgp4(self, tle: TLEData, minutes_from_epoch: float) -> np.ndarray:
        """Simplified SGP4-like propagation (Keplerian + J2 secular)."""
        a = (MU_EARTH / (tle.mean_motion_rev_day * 2 * math.pi / 86400)**2) ** (1.0 / 3.0)
        inc = tle.inclination_deg * DEG2RAD
        raan_dot = -1.5 * J2 * (R_EARTH / a)**2 * math.cos(inc) * (2 * math.pi / 86400)
        argp_dot = 1.5 * J2 * (R_EARTH / a)**2 * (2 - 2.5 * math.sin(inc)**2) * (2 * math.pi / 86400)

        mean_motion = tle.mean_motion_rev_day * 2 * math.pi / 86400
        dt = minutes_from_epoch * 60
        ma = tle.mean_anomaly_deg * DEG2RAD + mean_motion * dt
        raan = tle.raan_deg * DEG2RAD + raan_dot * dt
        argp = tle.argp_deg * DEG2RAD + argp_dot * dt

        r = a * (1 - tle.eccentricity**2) / (1 + tle.eccentricity * math.cos(ma))
        x = r * (math.cos(raan) * math.cos(argp + ma) - math.sin(raan) * math.sin(argp + ma) * math.cos(inc))
        y = r * (math.sin(raan) * math.cos(argp + ma) + math.cos(raan) * math.sin(argp + ma) * math.cos(inc))
        z = r * math.sin(argp + ma) * math.sin(inc)
        return np.array([x, y, z])

    def miss_distance(self, pos_a: np.ndarray, pos_b: np.ndarray) -> float:
        """Compute miss distance between two objects."""
        return np.linalg.norm(pos_a - pos_b)

    def probability_of_collision(
        self, miss_dist_m: float, combined_chord_m: float, relative_velocity_mps: float
    ) -> float:
        """Simplified collision probability estimate."""
        if miss_dist_m <= 0:
            return 1.0
        effective_area = math.pi * combined_chord_m**2 / 4
        probability = effective_area / (math.pi * miss_dist_m**2) * 0.01
        return min(probability, 1.0)

    def assess_conjunction(
        self, tle_a: TLEData, tle_b: TLEData,
        minutes_from_epoch: float, time_window_hours: float = 2.0,
    ) -> ConjunctionEvent:
        """Assess conjunction between two cataloged objects."""
        dt_step = 60.0
        steps = int(time_window_hours * 60 / dt_step)

        min_dist = float('inf')
        best_pos_a = None
        best_pos_b = None
        best_time = 0.0

        for step in range(steps):
            t = minutes_from_epoch + step * dt_step
            pos_a = self.propagate_tle_sgp4(tle_a, t)
            pos_b = self.propagate_tle_sgp4(tle_b, t)
            dist = self.miss_distance(pos_a, pos_b)
            if dist < min_dist:
                min_dist = dist
                best_pos_a = pos_a
                best_pos_b = pos_b
                best_time = t

        combined_chord = 10.0  # assumed combined hard-body radius
        pc = self.probability_of_collision(min_dist, combined_chord, 10000)

        if pc > 1e-4:
            action = "MANEUVER RECOMMENDED"
        elif pc > 1e-6:
            action = "MONITOR CLOSELY"
        else:
            action = "NO ACTION REQUIRED"

        return ConjunctionEvent(
            time_to_closest_approach_hours=best_time / 60,
            miss_distance_m=min_dist,
            probability_of_collision=pc,
            object_a_id=tle_a.satellite_name,
            object_b_id=tle_b.satellite_name,
            relative_velocity_mps=10000.0,
            recommended_action=action,
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("  SATELLITE SYSTEMS TOOLKIT — DEMONSTRATION")
    print("=" * 70)

    # 1. Walker constellation
    cm = ConstellationManager()
    walker = cm.walker_delta(
        total_satellites=66, orbital_planes=6,
        inclination_deg=53.0, altitude_km=550, phasing_offset=1,
    )
    print(f"\nWalker Delta Constellation:")
    print(f"  {walker['total_sats']} satellites in {walker['num_planes']} planes")
    print(f"  Period: {walker['period_hours']:.2f} hours")

    cov = cm.coverage_fraction(550, 66, elevation_mask_deg=10)
    print(f"  Coverage fraction: {cov:.1%}")

    # 2. Orbit determination
    od = OrbitDetermination()
    observations = [
        (0.0, 6_900_000, -120.5), (600.0, 6_850_000, -85.2),
        (1200.0, 6_920_000, 45.3), (1800.0, 7_100_000, 110.8),
    ]
    result = od.batch_least_squares(
        observations=observations,
        initial_guess=np.array([7_000_000, 0, 0, 0, 7_500, 0]),
    )
    print(f"\nOrbit Determination:")
    print(f"  Position: {np.linalg.norm(result['position']):.0f} m")
    print(f"  Residual RMS: {result['residual_rms']:.2f} m")
    print(f"  Iterations: {result['iterations']}")

    # 3. ADCS
    adcs = AttitudeController()
    wheels = adcs.size_reaction_wheels(
        desired_pointing_accuracy_deg=0.01,
        max_slew_rate_deg_per_sec=1.0,
        max_torque_nm=0.05,
        momentum_storage_required_nm_s=10.0,
    )
    print(f"\nReaction Wheel Sizing:")
    print(f"  Config: {wheels['configuration']}, {wheels['num_wheels']} wheels")
    print(f"  Mass: {wheels['total_mass_kg']:.1f} kg, Power: {wheels['power_watts']:.1f} W")

    # 4. Power subsystem
    power = PowerSubsystem(
        solar_array_area_m2=2.5, solar_cell_efficiency=0.28,
        eclipse_fraction=0.35, average_power_consumption_w=50,
        battery_capacity_wh=200, degradation_factor=0.95,
    )
    pb = power.compute_budget()
    print(f"\nPower Budget:")
    print(f"  Solar EOL: {pb.solar_generation_eol_w:.1f} W")
    print(f"  DoD: {pb.depth_of_discharge:.1%}")
    print(f"  Margin: {pb.margin_w:.1f} W")

    # 5. Link budget
    link = LinkBudget(
        tx_power_watts=10, tx_gain_dbi=15, rx_gain_dbi=25,
        frequency_ghz=12, distance_km=36_000,
    )
    lb = link.compute()
    print(f"\nLink Budget:")
    print(f"  EIRP: {lb['eirp_dbw']:.1f} dBW")
    print(f"  C/N0: {lb['cn0_db_hz']:.1f} dB-Hz")
    print(f"  Margin: {lb['margin_db']:.1f} dB")

    # 6. Debris tracking
    tle_a = TLEData(
        satellite_name="ISS", epoch_year=24, epoch_day=100.0,
        inclination_deg=51.6, raan_deg=150.0, eccentricity=0.0005,
        argp_deg=45.0, mean_anomaly_deg=180.0,
        mean_motion_rev_day=15.5, bstar=0.0002, revolution_number=50000,
    )
    tle_b = TLEData(
        satellite_name="DEBRIS-A", epoch_year=24, epoch_day=100.0,
        inclination_deg=51.5, raan_deg=150.2, eccentricity=0.001,
        argp_deg=44.0, mean_anomaly_deg=179.5,
        mean_motion_rev_day=15.5, bstar=0.0001, revolution_number=50000,
    )
    tracker = DebrisTracker()
    conj = tracker.assess_conjunction(tle_a, tle_b, minutes_from_epoch=0)
    print(f"\nConjunction Assessment:")
    print(f"  Miss distance: {conj.miss_distance_m:.0f} m")
    print(f"  P(collision): {conj.probability_of_collision:.2e}")
    print(f"  Action: {conj.recommended_action}")

    print("\n" + "=" * 70)
    print("  DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

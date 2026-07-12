"""
Aerospace Engineering Toolkit
Orbital mechanics, propulsion, thermal protection, structural analysis, and trajectory optimization.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import minimize_scalar, root_scalar


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

class CelestialBody(Enum):
    EARTH = "earth"
    MARS = "mars"
    MOON = "moon"
    VENUS = "venus"
    JUPITER = "jupiter"

BODY_PARAMETERS: dict[CelestialBody, dict[str, float]] = {
    CelestialBody.EARTH: {
        "mu": 3.986004418e14,
        "radius": 6_371_000,
        "rotation_rate": 7.2921159e-5,
        "j2": 1.08263e-3,
        "atm_scale_height": 8_500,
        "atm_surface_density": 1.225,
    },
    CelestialBody.MARS: {
        "mu": 4.282837e13,
        "radius": 3_389_500,
        "rotation_rate": 7.088218e-5,
        "j2": 1.95545e-3,
        "atm_scale_height": 11_100,
        "atm_surface_density": 0.020,
    },
    CelestialBody.MOON: {
        "mu": 4.9048695e12,
        "radius": 1_737_400,
        "rotation_rate": 2.6617e-6,
        "j2": 2.033e-4,
        "atm_scale_height": 0,
        "atm_surface_density": 0,
    },
    CelestialBody.VENUS: {
        "mu": 3.24859e14,
        "radius": 6_051_800,
        "rotation_rate": -2.9924e-7,
        "j2": 4.458e-6,
        "atm_scale_height": 15_900,
        "atm_surface_density": 65.0,
    },
    CelestialBody.JUPITER: {
        "mu": 1.26687e17,
        "radius": 69_911_000,
        "rotation_rate": 1.75865e-4,
        "j2": 4.709e-3,
        "atm_scale_height": 27_000,
        "atm_surface_density": 0.16,
    },
}

G0 = 9.80665  # m/s^2 standard gravity
AU = 1.496e11  # meters
DEG2RAD = math.pi / 180.0
RAD2DEG = 180.0 / math.pi


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class KeplerianElements:
    """Classical orbital elements (Keplerian)."""
    a: float          # semi-major axis (m)
    e: float          # eccentricity
    i: float          # inclination (rad)
    raan: float       # right ascension of ascending node (rad)
    argp: float       # argument of periapsis (rad)
    nu: float         # true anomaly (rad)

    @property
    def period(self) -> float:
        mu = BODY_PARAMETERS[CelestialBody.EARTH]["mu"]
        return 2 * math.pi * math.sqrt(self.a**3 / mu)

    @property
    def apogee_radius(self) -> float:
        return self.a * (1 + self.e)

    @property
    def perigee_radius(self) -> float:
        return self.a * (1 - self.e)

    def to_cartesian(self, body: CelestialBody = CelestialBody.EARTH) -> np.ndarray:
        """Convert to position and velocity vectors in ECI frame."""
        mu = BODY_PARAMETERS[body]["mu"]
        p = self.a * (1 - self.e**2)
        r_mag = p / (1 + self.e * math.cos(self.nu))

        r_pf = np.array([
            r_mag * math.cos(self.nu),
            r_mag * math.sin(self.nu),
            0.0,
        ])

        v_pf = math.sqrt(mu / p) * np.array([
            -math.sin(self.nu),
            self.e + math.cos(self.nu),
            0.0,
        ])

        cos_raan, sin_raan = math.cos(self.raan), math.sin(self.raan)
        cos_argp, sin_argp = math.cos(self.argp), math.sin(self.argp)
        cos_i, sin_i = math.cos(self.i), math.sin(self.i)

        rotation = np.array([
            [cos_raan * cos_argp - sin_raan * sin_argp * cos_i,
             -cos_raan * sin_argp - sin_raan * cos_argp * cos_i,
             sin_raan * sin_i],
            [sin_raan * cos_argp + cos_raan * sin_argp * cos_i,
             -sin_raan * sin_argp + cos_raan * cos_argp * cos_i,
             -cos_raan * sin_i],
            [sin_argp * sin_i,
             cos_argp * sin_i,
             cos_i],
        ])

        r_eci = rotation @ r_pf
        v_eci = rotation @ v_pf
        return np.concatenate([r_eci, v_eci])


@dataclass
class HohmannResult:
    """Result of a Hohmann transfer computation."""
    dv1: float          # first burn delta-v (m/s)
    dv2: float          # second burn delta-v (m/s)
    dv_total: float     # total delta-v (m/s)
    transfer_time: float  # seconds
    transfer_orbit_a: float  # semi-major axis of transfer orbit (m)
    transfer_time_hours: float

    def __post_init__(self):
        self.dv_total = self.dv1 + self.dv2
        self.transfer_time_hours = self.transfer_time / 3600.0


@dataclass
class BiEllipticResult:
    """Result of a bi-elliptic transfer."""
    dv1: float
    dv2: float
    dv3: float
    dv_total: float
    time1: float
    time2: float
    total_time: float
    intermediate_radius: float


@dataclass
class AtmosphereLayer:
    """Atmosphere model layer."""
    base_altitude: float
    scale_height: float
    base_density: float
    temperature: float


@dataclass
class ReentryHeating:
    """Stagnation-point heating result."""
    heat_flux: float        # W/cm^2
    total_heat_load: float  # J/cm^2
    peak_dynamic_pressure: float  # Pa
    entry_angle: float  # degrees
    velocity_at_entry: float  # m/s


@dataclass
class LaunchProfilePoint:
    """Single point on a launch ascent profile."""
    altitude: float
    velocity: float
    dynamic_pressure: float
    load_factor: float
    drag_loss: float
    gravity_loss: float
    mass: float
    time: float


# ---------------------------------------------------------------------------
# Orbital Mechanics
# ---------------------------------------------------------------------------

class OrbitalMechanics:
    """Core orbital mechanics calculations."""

    def __init__(self, central_body: str = "earth"):
        self.body = CelestialBody(central_body.lower())
        self.params = BODY_PARAMETERS[self.body]
        self.mu = self.params["mu"]
        self.radius = self.params["radius"]

    def vis_viva(self, r: float, a: float) -> float:
        """Orbital velocity from vis-viva equation."""
        return math.sqrt(self.mu * (2.0 / r - 1.0 / a))

    def orbital_period(self, a: float) -> float:
        """Orbital period for a given semi-major axis."""
        return 2 * math.pi * math.sqrt(a**3 / self.mu)

    def hohmann_transfer(self, r1: float, r2: float) -> HohmannResult:
        """Compute Hohmann transfer between two circular orbits."""
        a_transfer = (r1 + r2) / 2.0
        dv1 = abs(self.vis_viva(r1, a_transfer) - self.vis_viva(r1, r1))
        dv2 = abs(self.vis_viva(r2, r2) - self.vis_viva(r2, a_transfer))
        transfer_time = math.pi * math.sqrt(a_transfer**3 / self.mu)
        return HohmannResult(
            dv1=dv1, dv2=dv2, dv_total=dv1 + dv2,
            transfer_time=transfer_time, transfer_orbit_a=a_transfer,
            transfer_time_hours=transfer_time / 3600.0,
        )

    def bi_elliptic_transfer(
        self, r1: float, r2: float, intermediate_r: float
    ) -> BiEllipticResult:
        """Bi-elliptic transfer via an intermediate orbit."""
        a1 = (r1 + intermediate_r) / 2.0
        a2 = (intermediate_r + r2) / 2.0

        dv1 = abs(self.vis_viva(r1, a1) - self.vis_viva(r1, r1))
        dv2 = abs(self.vis_viva(intermediate_r, a2) - self.vis_viva(intermediate_r, a1))
        dv3 = abs(self.vis_viva(r2, r2) - self.vis_viva(r2, a2))

        t1 = math.pi * math.sqrt(a1**3 / self.mu)
        t2 = math.pi * math.sqrt(a2**3 / self.mu)

        return BiEllipticResult(
            dv1=dv1, dv2=dv2, dv3=dv3, dv_total=dv1 + dv2 + dv3,
            time1=t1, time2=t2, total_time=t1 + t2,
            intermediate_radius=intermediate_r,
        )

    def plane_change_cost(self, v: float, delta_i: float) -> float:
        """Delta-v cost for a plane change at given velocity."""
        return 2.0 * v * math.sin(delta_i / 2.0)

    def hohmann_with_plane_change(
        self, r1: float, r2: float, delta_inclination: float
    ) -> dict[str, float]:
        """Combined Hohmann transfer with plane change at apogee."""
        a_t = (r1 + r2) / 2.0
        v1_circular = self.vis_viva(r1, r1)
        v1_transfer = self.vis_viva(r1, a_t)
        v2_transfer = self.vis_viva(r2, a_t)
        v2_circular = self.vis_viva(r2, r2)

        dv1 = abs(v1_transfer - v1_circular)
        dv2_planar = abs(v2_circular - v2_transfer)
        dv2_plane = 2.0 * v2_transfer * math.sin(delta_inclination / 2.0)
        dv2 = math.sqrt(dv2_planar**2 + dv2_plane**2)

        return {
            "dv1": dv1, "dv2_planar": dv2_planar, "dv2_plane": dv2_plane,
            "dv2_combined": dv2, "dv_total": dv1 + dv2,
        }

    def sphere_of_influence(self, secondary_mass: float, primary_mass: float, distance: float) -> float:
        """Compute sphere of influence radius for a secondary body."""
        return distance * (secondary_mass / primary_mass) ** (2.0 / 5.0)

    def lagrange_points(self, m1: float, m2: float, d: float) -> dict[str, np.ndarray]:
        """Compute approximate positions of the 5 Lagrange points (circular restricted 3-body)."""
        mu2 = m2 / (m1 + m2)
        mu1 = 1.0 - mu2

        r1 = np.array([-mu2 * d, 0, 0])
        r2 = np.array([mu1 * d, 0, 0])

        # L1 - approximate solution via polynomial
        rho = (mu2 / (3 * mu1)) ** (1.0 / 3.0)
        x_l1 = d * (1 - rho - rho**2 / 3.0 - rho**3 / 9.0)
        l1 = np.array([x_l1, 0, 0])

        # L2
        x_l2 = d * (1 + rho + rho**2 / 3.0 - rho**3 / 9.0)
        l2 = np.array([x_l2, 0, 0])

        # L3
        x_l3 = -d * (1 + 5.0 * mu2 / 12.0)
        l3 = np.array([x_l3, 0, 0])

        # L4 and L5 (equilateral triangle)
        l4 = np.array([d * (mu1 - 0.5), d * math.sqrt(3) / 2.0, 0])
        l5 = np.array([d * (mu1 - 0.5), -d * math.sqrt(3) / 2.0, 0])

        return {"L1": l1, "L2": l2, "L3": l3, "L4": l4, "L5": l5}

    def propagate_kepler(
        self, state0: np.ndarray, t_span: tuple[float, float], n_points: int = 200
    ) -> tuple[np.ndarray, np.ndarray]:
        """Propagate two-body orbit using Cowell's method (numerical)."""
        def derivatives(t: float, y: np.ndarray) -> np.ndarray:
            r = y[:3]
            v = y[3:]
            r_mag = np.linalg.norm(r)
            accel = -self.mu * r / r_mag**3
            return np.concatenate([v, accel])

        t_eval = np.linspace(t_span[0], t_span[1], n_points)
        sol = solve_ivp(derivatives, t_span, state0, t_eval=t_eval, rtol=1e-10, atol=1e-12)
        return sol.t, sol.y


# ---------------------------------------------------------------------------
# Propulsion
# ---------------------------------------------------------------------------

class PropulsionSystem:
    """Propulsion system performance modeling."""

    def __init__(
        self,
        name: str,
        thrust_vacuum: float,
        thrust_sl: float,
        isp_vacuum: float,
        isp_sl: float,
        propellant_mass: float,
        oxidizer_fuel_ratio: float = 2.5,
    ):
        self.name = name
        self.thrust_vacuum = thrust_vacuum
        self.thrust_sl = thrust_sl
        self.isp_vacuum = isp_vacuum
        self.isp_sl = isp_sl
        self.propellant_mass = propellant_mass
        self.oxidizer_fuel_ratio = oxidizer_fuel_ratio

    @property
    def mass_flow_rate(self) -> float:
        """Propellant mass flow rate (kg/s) in vacuum."""
        return self.thrust_vacuum / (self.isp_vacuum * G0)

    @property
    def exhaust_velocity_vac(self) -> float:
        """Vacuum exhaust velocity (m/s)."""
        return self.isp_vacuum * G0

    @property
    def burn_time(self) -> float:
        """Total burn time at full thrust (seconds)."""
        return self.propellant_mass / self.mass_flow_rate

    def delta_v_capacity(self, dry_mass: float = 0.0) -> float:
        """Tsiolkovsky rocket equation delta-v."""
        total_mass = dry_mass + self.propellant_mass
        if dry_mass <= 0:
            dry_mass = total_mass * 0.08  # assume 8% structural fraction
        return self.exhaust_velocity_vac * math.log(total_mass / dry_mass)

    def thrust_at_altitude(self, altitude: float) -> float:
        """Thrust at a given altitude using pressure correction."""
        p_atm = 101325 * math.exp(-altitude / 8500)  # exponential atmosphere
        effective_area = (self.thrust_vacuum - self.thrust_sl) / 101325
        return self.thrust_vacuum - p_atm * effective_area

    def isp_at_altitude(self, altitude: float) -> float:
        """Effective Isp at altitude."""
        thrust = self.thrust_at_altitude(altitude)
        return thrust / (self.mass_flow_rate * G0) if self.mass_flow_rate > 0 else 0

    def twr(self, vehicle_mass: float, altitude: float = 0) -> float:
        """Thrust-to-weight ratio."""
        thrust = self.thrust_at_altitude(altitude)
        weight = vehicle_mass * G0
        return thrust / weight

    def optimal_burn_arc(
        self, initial_mass: float, target_dv: float, gravity: float = 9.81
    ) -> dict[str, float]:
        """Compute gravity loss for a finite burn arc."""
        exhaust_v = self.exhaust_velocity_vac
        final_mass = initial_mass * math.exp(-target_dv / exhaust_v)
        propellant_consumed = initial_mass - final_mass
        burn_time_actual = propellant_consumed / self.mass_flow_rate

        avg_mass = (initial_mass + final_mass) / 2.0
        avg_thrust = self.thrust_vacuum
        gravity_loss = gravity * burn_time_actual * 0.5

        return {
            "burn_time": burn_time_actual,
            "propellant_consumed": propellant_consumed,
            "final_mass": final_mass,
            "gravity_loss": gravity_loss,
            "effective_dv": target_dv - gravity_loss,
        }


class ElectricPropulsionSystem(PropulsionSystem):
    """Electric propulsion with power constraints."""

    def __init__(
        self,
        name: str,
        thrust_vacuum: float,
        isp_vacuum: float,
        input_power: float,
        efficiency: float,
        propellant_mass: float,
        **kwargs: Any,
    ):
        super().__init__(
            name=name, thrust_vacuum=thrust_vacuum, thrust_sl=thrust_vacuum,
            isp_vacuum=isp_vacuum, isp_sl=isp_vacuum,
            propellant_mass=propellant_mass, **kwargs,
        )
        self.input_power = input_power
        self.efficiency = efficiency

    @property
    def power_to_thrust_ratio(self) -> float:
        """Efficiency * power / thrust."""
        return self.efficiency * self.input_power / self.thrust_vacuum

    @property
    def exhaust_velocity_vac(self) -> float:
        return self.isp_vacuum * G0

    def spiral_transfer_time(
        self, r1: float, r2: float, initial_mass: float
    ) -> float:
        """Low-thrust spiral transfer time estimate (days)."""
        mu = BODY_PARAMETERS[CelestialBody.EARTH]["mu"]
        a1, a2 = r1, r2
        avg_thrust = self.thrust_vacuum
        avg_mass = (initial_mass + initial_mass * 0.7) / 2.0
        delta_v = abs(self.exhaust_velocity_vac * math.log(initial_mass / (initial_mass * 0.7)))
        time_seconds = delta_v * avg_mass / avg_thrust
        return time_seconds / 86400.0


# ---------------------------------------------------------------------------
# Thermal Protection
# ---------------------------------------------------------------------------

class ThermalProtectionSystem:
    """Thermal protection system analysis for re-entry vehicles."""

    # Sutton-Graves stagnation point heating constants
    K_STAGNATION = 1.83e-4  # W/cm^2 per (rho^0.5 * V^3.15 / R_n^0.5)

    def __init__(self, vehicle: "ReentryVehicle | None" = None):
        self.vehicle = vehicle

    @staticmethod
    def stagnation_point_heating(
        velocity: float,
        atmosphere_density: float,
        nose_radius: float,
        k_factor: float = 1.83e-4,
    ) -> dict[str, float]:
        """Sutton-Graves stagnation point heating rate."""
        heat_flux = k_factor * math.sqrt(atmosphere_density) * velocity**3.15 / math.sqrt(nose_radius)
        return {
            "heat_flux": heat_flux,
            "total_heat_load": heat_flux * 60.0,  # simplified for 60s peak
            "dynamic_pressure": 0.5 * atmosphere_density * velocity**2,
        }

    def equilibrium_temperature(
        self, heat_flux: float, emissivity: float = 0.85, sigma: float = 5.67e-8
    ) -> float:
        """Surface equilibrium temperature assuming radiative cooling."""
        return (heat_flux * 1e4 / (emissivity * sigma)) ** 0.25  # W/cm^2 -> W/m^2

    def ablation_mass_loss_rate(
        self, heat_flux: float, heat_of_ablation: float = 3.0e7
    ) -> float:
        """Mass loss rate for ablative TPS (kg/m^2/s)."""
        return heat_flux * 1e-4 / heat_of_ablation

    def tps_thickness(
        self, total_heat_load: float, heat_of_ablation: float = 3.0e7,
        density: float = 1450.0, safety_factor: float = 1.25
    ) -> float:
        """Required TPS thickness (meters)."""
        return safety_factor * total_heat_load / (heat_of_ablation * density)


# ---------------------------------------------------------------------------
# Re-entry Vehicle
# ---------------------------------------------------------------------------

class ReentryVehicle:
    """Re-entry vehicle definition."""

    def __init__(
        self,
        mass: float,
        reference_area: float,
        nose_radius: float,
        ballistic_coefficient: Optional[float] = None,
    ):
        self.mass = mass
        self.reference_area = reference_area
        self.nose_radius = nose_radius
        self.ballistic_coefficient = (
            ballistic_coefficient if ballistic_coefficient is not None
            else mass / (0.3 * reference_area)
        )

    @property
    def cd_estimate(self) -> float:
        """Estimated drag coefficient for a blunt body."""
        return 1.2

    def deceleration_profile(
        self, entry_velocity: float, entry_angle_deg: float,
        atmosphere_density_func: Any = None,
    ) -> list[dict[str, float]]:
        """Simplified deceleration profile from entry interface to landing."""
        if atmosphere_density_func is None:
            atmosphere_density_func = lambda h: 1.225 * math.exp(-h / 8500)

        g = G0
        v = entry_velocity
        gamma = entry_angle_deg * DEG2RAD
        alt = 120_000  # 120 km entry interface
        dt = 0.5

        profile = []
        while alt > 0 and v > 10:
            rho = atmosphere_density_func(alt)
            q = 0.5 * rho * v**2
            drag = q * self.reference_area * self.cd_estimate / self.mass
            g_component = g * math.sin(gamma)
            total_decel = drag + g_component

            v -= total_decel * dt
            alt -= v * math.sin(gamma) * dt
            gamma += (g * math.cos(gamma) / v - drag * math.tan(gamma) / v) * dt

            profile.append({
                "altitude": max(alt, 0), "velocity": v,
                "deceleration_g": total_decel / G0,
                "dynamic_pressure": q,
            })
        return profile


# ---------------------------------------------------------------------------
# Launch Vehicle Analysis
# ---------------------------------------------------------------------------

class LaunchVehicleAnalysis:
    """Launch vehicle ascent analysis."""

    def __init__(
        self,
        dry_mass: float,
        propellant_mass: float,
        thrust_sea_level: float,
        reference_area: float,
        drag_coefficient: float = 0.3,
    ):
        self.dry_mass = dry_mass
        self.propellant_mass = propellant_mass
        self.total_mass = dry_mass + propellant_mass
        self.thrust_sl = thrust_sea_level
        self.ref_area = reference_area
        self.cd = drag_coefficient

    def atmosphere_density(self, altitude: float) -> float:
        """Exponential atmosphere model."""
        if altitude < 0:
            return 1.225
        return 1.225 * math.exp(-altitude / 8500)

    def drag_force(self, altitude: float, velocity: float) -> float:
        """Aerodynamic drag force."""
        rho = self.atmosphere_density(altitude)
        return 0.5 * rho * velocity**2 * self.ref_area * self.cd

    def ascent_profile(
        self,
        initial_altitude: float = 0,
        target_altitude: float = 200_000,
        pitch_over_altitude: float = 1_000,
        max_q_altitude: float = 11_000,
    ) -> list[LaunchProfilePoint]:
        """Simulate a gravity-turn ascent profile."""
        alt = initial_altitude
        v_vert = 0.0
        v_horiz = 0.0
        mass = self.total_mass
        t = 0.0
        dt = 0.5

        mass_flow = self.thrust_sl / (300 * G0)  # assume ~300s Isp
        profile: list[LaunchProfilePoint] = []

        while alt < target_altitude and mass > self.dry_mass:
            v_total = math.sqrt(v_vert**2 + v_horiz**2)
            rho = self.atmosphere_density(alt)
            drag = 0.5 * rho * v_total**2 * self.ref_area * self.cd

            thrust = self.thrust_sl * (rho / 1.225 + 0.3)  # simplified altitude correction
            thrust = min(thrust, self.thrust_sl)
            accel_vert = thrust * math.cos(math.radians(5)) / mass - G0 - drag * v_vert / (v_total * mass + 1e-10)
            accel_horiz = thrust * math.sin(math.radians(5)) / mass - drag * v_horiz / (v_total * mass + 1e-10)

            if alt > pitch_over_altitude:
                pitch_angle = min(45, (alt - pitch_over_altitude) / 10000 * 45)
                accel_vert = thrust * math.cos(math.radians(90 - pitch_angle)) / mass - G0
                accel_horiz = thrust * math.sin(math.radians(90 - pitch_angle)) / mass

            v_vert = max(0, v_vert + accel_vert * dt)
            v_horiz = v_horiz + accel_horiz * dt
            alt += v_vert * dt
            mass -= mass_flow * dt
            t += dt

            dp = 0.5 * rho * v_total**2
            load_factor = math.sqrt(accel_vert**2 + accel_horiz**2) / G0 if G0 > 0 else 0

            profile.append(LaunchProfilePoint(
                altitude=alt, velocity=v_total,
                dynamic_pressure=dp, load_factor=load_factor,
                drag_loss=drag * v_total / (mass * G0) * dt,
                gravity_loss=G0 * dt,
                mass=mass, time=t,
            ))
            if alt > target_altitude * 1.1:
                break

        return profile


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("  AEROSPACE ENGINEERING TOOLKIT — DEMONSTRATION")
    print("=" * 70)

    # 1. Orbital mechanics
    orbital = OrbitalMechanics("earth")
    print("\n--- Hohmann Transfer: LEO to GEO ---")
    h = orbital.hohmann_transfer(6_571_000, 42_164_000)
    print(f"  Burn 1: {h.dv1:.3f} m/s")
    print(f"  Burn 2: {h.dv2:.3f} m/s")
    print(f"  Total:  {h.dv_total:.3f} m/s")
    print(f"  Time:   {h.transfer_time_hours:.1f} hours")

    # 2. Plane change
    print("\n--- Combined Hohmann + Plane Change ---")
    pc = orbital.hohmann_with_plane_change(6_571_000, 42_164_000, 28.5 * DEG2RAD)
    print(f"  Total delta-v: {pc['dv_total']:.1f} m/s (with 28.5° plane change)")

    # 3. Propulsion
    print("\n--- Propulsion: RS-25 ---")
    engine = PropulsionSystem(
        name="RS-25", thrust_vacuum=2_278_000, thrust_sl=1_860_000,
        isp_vacuum=452, isp_sl=366, propellant_mass=352_700,
    )
    print(f"  Mass flow rate: {engine.mass_flow_rate:.2f} kg/s")
    print(f"  Burn time: {engine.burn_time:.1f} s")
    print(f"  Delta-v (dry mass 45000 kg): {engine.delta_v_capacity(45_000):.1f} m/s")
    print(f"  TWR (5400 tonnes): {engine.twr(5_400_000):.3f}")

    # 4. Electric propulsion
    print("\n--- Electric Propulsion: NSTAR Ion ---")
    ion = ElectricPropulsionSystem(
        name="NSTAR", thrust_vacuum=0.092, isp_vacuum=3100,
        input_power=2.3, efficiency=0.61, propellant_mass=81.5,
    )
    print(f"  Exhaust velocity: {ion.exhaust_velocity_vac:.0f} m/s")
    print(f"  Spiral time (LEO to GEO): {ion.spiral_transfer_time(7_000_000, 42_164_000, 800):.1f} days")

    # 5. Thermal protection
    print("\n--- Re-entry Thermal Analysis ---")
    vehicle = ReentryVehicle(mass=8_000, reference_area=12.5, nose_radius=0.5)
    tp = ThermalProtectionSystem(vehicle)
    heating = tp.stagnation_point_heating(7_800, 0.001, 0.5)
    print(f"  Heat flux: {heating['heat_flux']:.2f} W/cm^2")
    temp = tp.equilibrium_temperature(heating['heat_flux'])
    print(f"  Equilibrium temp: {temp:.0f} K")
    thickness = tp.tps_thickness(heating['total_heat_load'])
    print(f"  Required TPS thickness: {thickness*1000:.1f} mm")

    # 6. Launch vehicle
    print("\n--- Launch Vehicle Ascent Profile ---")
    lv = LaunchVehicleAnalysis(
        dry_mass=25_000, propellant_mass=220_000,
        thrust_sea_level=7_600_000, reference_area=11.3,
    )
    profile = lv.ascent_profile()
    for pt in profile[:5]:
        print(f"  Alt={pt.altitude/1000:.1f}km  v={pt.velocity:.0f}m/s  "
              f"q={pt.dynamic_pressure/1000:.1f}kPa  n={pt.load_factor:.2f}g")

    # 7. Lagrange points
    print("\n--- Earth-Moon Lagrange Points ---")
    lp = orbital.lagrange_points(5.972e24, 7.342e22, 384_400_000)
    for name, pos in lp.items():
        dist = np.linalg.norm(pos) / 1000
        print(f"  {name}: {dist:.0f} km from Earth")

    print("\n" + "=" * 70)
    print("  DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

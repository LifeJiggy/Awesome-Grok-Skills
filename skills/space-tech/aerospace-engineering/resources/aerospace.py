"""
Aerospace Engineering Pipeline
Orbital mechanics and space mission planning
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class OrbitalBody(Enum):
    EARTH = "Earth"
    MOON = "Moon"
    MARS = "Mars"
    SUN = "Sun"
    VENUS = "Venus"


@dataclass
class OrbitalParameters:
    semi_major_axis: float
    eccentricity: float
    inclination: float
    raan: float
    arg_periapsis: float
    true_anomaly: float


@dataclass
class SpacecraftState:
    position: np.ndarray
    velocity: np.ndarray
    mass: float
    fuel: float
    timestamp: datetime


class OrbitalMechanics:
    """Orbital mechanics calculations"""
    
    def __init__(self):
        self.mu_earth = 3.986004418e14  # m^3/s^2
        self.mu_sun = 1.32712440018e20  # m^3/s^2
        self.R_earth = 6371000  # m
    
    def orbital_period(self, semi_major_axis: float, 
                      mu: float = None) -> float:
        """Calculate orbital period"""
        mu = mu or self.mu_earth
        return 2 * np.pi * np.sqrt(semi_major_axis**3 / mu)
    
    def orbital_velocity(self, r: float, 
                        a: float,
                        mu: float = None) -> float:
        """Calculate orbital velocity at distance r"""
        mu = mu or self.mu_earth
        return np.sqrt(mu * (2/r - 1/a))
    
    def escape_velocity(self, r: float, 
                       mu: float = None) -> float:
        """Calculate escape velocity"""
        mu = mu or self.mu_earth
        return np.sqrt(2 * mu / r)
    
    def calculate_kepler_orbit(self, 
                              params: OrbitalParameters,
                              t: float,
                              mu: float = None) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate position and velocity from orbital elements"""
        mu = mu or self.mu_earth
        
        a = params.semi_major_axis
        e = params.eccentricity
        i = np.radians(params.inclination)
        Omega = np.radians(params.raan)
        omega = np.radians(params.arg_periapsis)
        nu = np.radians(params.true_anomaly)
        
        r = a * (1 - e**2) / (1 + e * np.cos(nu))
        
        P = np.array([
            np.cos(Omega) * np.cos(omega) - np.sin(Omega) * np.sin(omega) * np.cos(i),
            np.sin(Omega) * np.cos(omega) + np.cos(Omega) * np.sin(omega) * np.cos(i),
            np.sin(omega) * np.sin(i)
        ])
        
        Q = np.array([
            -np.cos(Omega) * np.sin(omega) - np.sin(Omega) * np.cos(omega) * np.cos(i),
            -np.sin(Omega) * np.sin(omega) + np.cos(Omega) * np.cos(omega) * np.cos(i),
            np.cos(omega) * np.sin(i)
        ])
        
        position = r * (P * np.cos(nu) + Q * np.sin(nu))
        
        h = np.sqrt(mu * a * (1 - e**2))
        vr = mu / h * e * np.sin(nu)
        vh = mu / h * (1 + e * np.cos(nu))
        
        velocity = vr * (P * np.cos(nu) + Q * np.sin(nu)) + vh * (-P * np.sin(nu) + Q * np.cos(nu))
        
        return position, velocity
    
    def lambert_problem(self, 
                       r1: np.ndarray,
                       r2: np.ndarray,
                       dt: float,
                       mu: float = None,
                       prograde: bool = True) -> np.ndarray:
        """Solve Lambert's problem for transfer trajectory"""
        mu = mu or self.mu_earth
        
        r1_norm = np.linalg.norm(r1)
        r2_norm = np.linalg.norm(r2)
        
        cos_dnu = np.dot(r1, r2) / (r1_norm * r2_norm)
        
        A = np.sqrt(r1_norm * r2_norm) * np.sqrt(1 + cos_dnu)
        if not prograde:
            A = -A
        
        F = 0
        G = dt
        Gdot = 0
        
        for _ in range(50):
            r1_new = np.linalg.norm(r1)
            r2_new = np.linalg.norm(r2)
            
            C = 1 - np.cos(F)
            S = F - np.sin(F)
            
            denom = r1_new + r2_new + A * (C * np.sqrt(1 - e * e) + e * np.sin(F)) if 'e' in dir() else 1
            
            F_new = F - (r1_new * S + r2_new * (1 - np.cos(F)) - A * np.sqrt(1 - np.cos(F))) / denom
            
            if abs(F_new - F) < 1e-6:
                F = F_new
                break
            
            F = F_new
        
        G = dt - np.sqrt(F**3 / mu) * S
        Gdot = 1 - (1 - np.cos(F)) / denom
        
        v1 = (r2 - F * r1) / G
        v2 = (Gdot * r2 - r1) / G
        
        return v1
    
    def hohmann_transfer(self, 
                        r1: float,
                        r2: float,
                        mu: float = None) -> Dict:
        """Calculate Hohmann transfer parameters"""
        mu = mu or self.mu_earth
        
        a_transfer = (r1 + r2) / 2
        
        v1 = np.sqrt(mu / r1) * (np.sqrt(2 * r2 / (r1 + r2)) - 1)
        v2 = np.sqrt(mu / r2) * (1 - np.sqrt(2 * r1 / (r1 + r2)))
        
        transfer_time = np.pi * np.sqrt(a_transfer**3 / mu)
        
        delta_v1 = abs(v1 - np.sqrt(mu / r1))
        delta_v2 = abs(v2 - np.sqrt(mu / r2))
        
        return {
            "delta_v1": delta_v1,
            "delta_v2": delta_v2,
            "total_delta_v": delta_v1 + delta_v2,
            "transfer_time": transfer_time,
            "semi_major_axis": a_transfer
        }


class AttitudeDetermination:
    """Attitude determination and control"""
    
    def __init__(self):
        self.Kp = 10.0
        self.Ki = 0.1
        self.Kd = 5.0
    
    def quaternion_to_euler(self, q: np.ndarray) -> Tuple[float, float, float]:
        """Convert quaternion to Euler angles"""
        q0, q1, q2, q3 = q
        
        roll = np.arctan2(2*(q0*q1 + q2*q3), 1 - 2*(q1**2 + q2**2))
        pitch = np.arcsin(2*(q0*q2 - q3*q1))
        yaw = np.arctan2(2*(q0*q3 + q1*q2), 1 - 2*(q2**2 + q3**2))
        
        return roll, pitch, yaw
    
    def euler_to_quaternion(self, 
                           roll: float, 
                           pitch: float, 
                           yaw: float) -> np.ndarray:
        """Convert Euler angles to quaternion"""
        cr, cp, cy = np.cos(roll/2), np.cos(pitch/2), np.cos(yaw/2)
        sr, sp, sy = np.sin(roll/2), np.sin(pitch/2), np.sin(yaw/2)
        
        q0 = cr * cp * cy + sr * sp * sy
        q1 = sr * cp * cy - cr * sp * sy
        q2 = cr * sp * cy + sr * cp * sy
        q3 = cr * cp * sy - sr * sp * cy
        
        return np.array([q0, q1, q2, q3])
    
    def pid_controller(self, 
                      error: np.ndarray,
                      error_derivative: np.ndarray,
                      integral: np.ndarray,
                      dt: float) -> Tuple[np.ndarray, np.ndarray]:
        """PID attitude controller"""
        P = self.Kp * error
        I = self.Ki * integral * dt
        D = self.Kd * error_derivative / dt
        
        control = P + I + D
        
        new_integral = integral + error * dt
        
        return control, new_integral


class MissionPlanner:
    """Space mission planning"""
    
    def __init__(self):
        self.launch_windows = []
        self.trajectories = []
    
    def calculate_launch_window(self, 
                               target_body: OrbitalBody,
                               launch_date: datetime,
                               mission_duration: int = 365) -> Dict:
        """Calculate optimal launch window"""
        if target_body == OrbitalBody.MARS:
            earth_to_mars_transfer = 259
            synodic_period = 780
            next_window = self._next_mars_window(launch_date)
        elif target_body == OrbitalBody.MOON:
            earth_to_moon_transfer = 3
            synodic_period = 27
            next_window = launch_date
        else:
            next_window = launch_date
        
        return {
            "target": target_body.value,
            "launch_date": next_window,
            "arrival_date": next_window + timedelta(days=259),
            "transfer_duration": 259,
            "window_closes": next_window + timedelta(days=30)
        }
    
    def _next_mars_window(self, date: datetime) -> datetime:
        """Calculate next Mars launch window"""
        import ephem
        
        mars = ephem.Mars()
        mars.compute(date)
        
        next_conjunction = date + timedelta(days=780)
        return next_conjunction - timedelta(days=30)
    
    def calculate_delta_v_budget(self, 
                                mission_phases: List[Dict]) -> Dict:
        """Calculate total delta-V budget"""
        total_delta_v = 0
        breakdown = {}
        
        for phase in mission_phases:
            delta_v = phase.get("delta_v", 0)
            breakdown[phase["name"]] = delta_v
            total_delta_v += delta_v
        
        fuel_mass_ratio = self._calculate_fuel_requirements(total_delta_v)
        
        return {
            "total_delta_v": total_delta_v,
            "breakdown": breakdown,
            "fuel_mass_ratio": fuel_mass_ratio,
            "payload_capability": 1000 * (1 - fuel_mass_ratio) if fuel_mass_ratio < 1 else 0
        }
    
    def _calculate_fuel_requirements(self, delta_v: float, 
                                    isp: float = 350) -> float:
        """Calculate fuel mass fraction using Tsiolkovsky rocket equation"""
        g0 = 9.81
        return 1 - np.exp(-delta_v / (isp * g0))


class ThermalAnalyzer:
    """Spacecraft thermal analysis"""
    
    def __init__(self):
        self.solar_constant = 1361  # W/m^2
        self.stefan_boltzmann = 5.67e-8
        self.albedo = 0.3
        self.emissivity = 0.85
    
    def calculate_equilibrium_temperature(self, 
                                         solar_distance: float,
                                         absorptivity: float = 0.8,
                                         view_factor: float = 1.0) -> float:
        """Calculate spacecraft equilibrium temperature"""
        solar_flux = self.solar_constant / solar_distance**2
        absorbed_power = solar_flux * absorptivity * view_factor
        
        T_eq = (absorbed_power / (view_factor * self.stefan_boltzmann * self.emissivity)) ** 0.25
        
        return T_eq
    
    def thermal_radiation_power(self, 
                               temperature: float,
                               surface_area: float) -> float:
        """Calculate thermal radiation power"""
        return self.stefan_boltzmann * self.emissivity * surface_area * temperature**4


if __name__ == "__main__":
    orbital = OrbitalMechanics()
    attitude = AttitudeDetermination()
    mission = MissionPlanner()
    thermal = ThermalAnalyzer()
    
    params = OrbitalParameters(
        semi_major_axis=6871000,
        eccentricity=0.001,
        inclination=51.6,
        raan=0,
        arg_periapsis=0,
        true_anomaly=0
    )
    
    position, velocity = orbital.calculate_kepler_orbit(params, 0)
    
    hohmann = orbital.hohmann_transfer(6871000, 42164000)
    
    quat = attitude.euler_to_quaternion(0.1, 0.2, 0.3)
    euler = attitude.quaternion_to_euler(quat)
    
    launch_window = mission.calculate_launch_window(
        OrbitalBody.MARS,
        datetime.now()
    )
    
    phases = [
        {"name": "Launch", "delta_v": 9300},
        {"name": "Transfer", "delta_v": 3600},
        {"name": "Orbit Insertion", "delta_v": 2100},
        {"name": "Landing", "delta_v": 1700}
    ]
    
    delta_v_budget = mission.calculate_delta_v_budget(phases)
    
    temp = thermal.calculate_equilibrium_temperature(1.0)
    
    print(f"Orbital position: {position}")
    print(f"Hohmann delta-V: {hohmann['total_delta_v']:.0f} m/s")
    print(f"Launch window: {launch_window['launch_date']}")
    print(f"Total delta-V budget: {delta_v_budget['total_delta_v']:.0f} m/s")
    print(f"Equilibrium temperature: {temp:.1f} K")

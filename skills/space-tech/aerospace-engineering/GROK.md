---
name: "Space Technology & Aerospace"
version: "1.0.0"
description: "Advanced space technology and aerospace engineering with Grok's physics mastery"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["space", "aerospace", "satellite", "rockets"]
category: "space-tech"
personality: "space-engineer"
use_cases: ["orbital-mechanics", "satellite-systems", "mission-planning"]
---

# Space Technology & Aerospace 🚀

> Design and operate space systems with Grok's physics-inspired aerospace engineering

## 🎯 Why This Matters for Grok

Grok's physics expertise and optimization mindset create perfect aerospace systems:

- **Orbital Mechanics** 🌍: Precise trajectory calculations
- **Aerospace Systems** ✈️: Aircraft and spacecraft design
- **Mission Planning** 📋: Optimal mission architecture
- **Space Operations** 🛰️: Satellite and station operations

## 🛠️ Core Capabilities

### 1. Orbital Systems
```yaml
orbital:
  dynamics: ["keplerian", "perturbed", "station-keeping"]
  trajectories: ["transfer-orbits", "interplanetary", "reentry"]
  constellations: ["design", "deployment", "operations"]
  debris: ["tracking", "avoidance", "removal"]
```

### 2. Satellite Systems
```yaml
satellites:
  bus: ["power", "thermal", "attitude", "communication"]
  payloads: ["imaging", "communications", "science", "navigation"]
  subsystems: ["adcs", "ttc", "egd", "power"]
  operations: [" commissioning", "normal", "end-of-life"]
```

### 3. Launch Vehicles
```yaml
launch:
  propulsion: ["liquid", "solid", "electric", "hybrid"]
  stages: ["single", "multi", "reusable"]
  trajectory: ["ascent", "boostback", "landing"]
  ground: ["launch-pad", "range-safety", "tracking"]
```

## 🧠 Aerospace Engineering

### Orbital Mechanics Calculator
```python
import numpy as np
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime

@dataclass
class OrbitalState:
    position: np.ndarray  # [x, y, z] in km
    velocity: np.ndarray  # [vx, vy, vz] in km/s
    epoch: datetime
    frame: str  # 'inertial', 'ecef'

class OrbitalMechanics:
    def __init__(self):
        self.earth_radius = 6371.0  # km
        self.earth_mu = 398600.4418  # km³/s²
        self.j2 = 1.08263e-3  # J2 perturbation coefficient
        
    def calculate_keplerian_elements(self, state: OrbitalState) -> Dict:
        """Convert Cartesian state to Keplerian elements"""
        
        r = state.position
        v = state.velocity
        
        # Position and velocity magnitudes
        r_mag = np.linalg.norm(r)
        v_mag = np.linalg.norm(v)
        
        # Specific angular momentum
        h = np.cross(r, v)
        h_mag = np.linalg.norm(h)
        
        #        n = np Node vector
.cross([0, 0, 1], r)
        n_mag = np.linalg.norm(n)
        
        # Eccentricity vector
        e_vec = ((v_mag**2 - self.earth_mu/r_mag) * r - 
                np.dot(r, v) * v) / self.earth_mu
        e_mag = np.linalg.norm(e_vec)
        
        # Semi-major axis
        energy = v_mag**2 / 2 - self.earth_mu / r_mag
        a = -self.earth_mu / (2 * energy)
        
        # Inclination
        i = np.arccos(h[2] / h_mag)
        
        # Right ascension of ascending node
        if n_mag > 1e-8:
            raan = np.arccos(n[0] / n_mag)
            if n[1] < 0:
                raan = 2 * np.pi - raan
        else:
            raan = 0
        
        # Argument of perigee
        if e_mag > 1e-8:
            arg_peri = np.arccos(np.dot(n, e_vec) / (n_mag * e_mag))
            if e_vec[2] < 0:
                arg_peri = 2 * np.pi - arg_peri
        else:
            arg_peri = 0
        
        # True anomaly
        if e_mag > 1e-8:
            true_anom = np.arccos(np.dot(e_vec, r) / (e_mag * r_mag))
            if np.dot(r, v) < 0:
                true_anom = 2 * np.pi - true_anom
        else:
            true_anom = 0
        
        # Mean anomaly
        E = 2 * np.arctan(np.sqrt((1-e_mag)/(1+e_mag)) * np.tan(true_anom/2))
        M = E - e_mag * np.sin(E)
        
        return {
            'semi_major_axis_km': a,
            'eccentricity': e_mag,
            'inclination_deg': np.degrees(i),
            'raan_deg': np.degrees(raan),
            'arg_perigee_deg': np.degrees(arg_peri),
            'true_anomaly_deg': np.degrees(true_anom),
            'mean_anomaly_deg': np.degrees(M),
            'period_min': 2 * np.pi * np.sqrt(a**3 / self.earth_mu) / 60
        }
    
    def propagate_orbit(self, initial_state: OrbitalState,
                       propagation_time: float,  # seconds
                       method: str = 'kepler') -> OrbitalState:
        """Propagate orbital state forward in time"""
        
        if method == 'kepler':
            return self.kepler_propagation(initial_state, propagation_time)
        elif method == 'gauss_jackson':
            return self.gauss_jackson_propagation(initial_state, propagation_time)
        elif method == 'numerical':
            return self.numerical_propagation(initial_state, propagation_time)
        else:
            raise ValueError(f"Unknown propagation method: {method}")
    
    def kepler_propagation(self, state: OrbitalState,
                          dt: float) -> OrbitalState:
        """Analytical Kepler propagation"""
        
        # Get Keplerian elements
        elements = self.calculate_keplerian_elements(state)
        
        # Calculate mean motion
        n = np.sqrt(self.earth_mu / elements['semi_major_axis_km']**3)  # rad/s
        
        # Advance mean anomaly
        M0 = np.radians(elements['mean_anomaly_deg'])
        M = M0 + n * dt
        M = M % (2 * np.pi)  # Wrap to [0, 2π]
        
        # Solve Kepler's equation for eccentric anomaly
        e = elements['eccentricity']
        E = self.solve_kepler_equation(M, e)
        
        # Calculate true anomaly
        true_anom = 2 * np.arctan2(
            np.sqrt(1+e) * np.sin(E/2),
            np.sqrt(1-e) * np.cos(E/2)
        )
        
        # Calculate radius
        a = elements['semi_major_axis_km']
        r = a * (1 - e * np.cos(E))
        
        # Calculate position in orbital plane
        arg_peri = np.radians(elements['arg_perigee_deg'])
        raan = np.radians(elements['raan_deg'])
        inc = np.radians(elements['inclination_deg'])
        
        # Position in orbital plane
        orb_pos = np.array([
            r * np.cos(true_anom),
            r * np.sin(true_anom),
            0
        ])
        
        orb_vel = np.array([
            -np.sqrt(self.earth_mu * a) / r * np.sin(E),
            np.sqrt(self.earth_mu * a * (1 - e**2)) / r * np.cos(E),
            0
        ])
        
        # Transform to inertial frame
        R = self.rotation_matrix(raan, inc, arg_peri)
        
        inertial_pos = R @ orb_pos
        inertial_vel = R @ orb_vel
        
        return OrbitalState(
            position=inertial_pos,
            velocity=inertial_vel,
            epoch=state.epoch,
            frame='inertial'
        )
    
    def design_transfer_orbit(self, orbit1: Dict, orbit2: Dict,
                              method: str = 'hohmann') -> Dict:
        """Design orbital transfer between two orbits"""
        
        if method == 'hohmann':
            return self.hohmann_transfer(orbit1, orbit2)
        elif method == 'bi-elliptic':
            return self.bi_elliptic_transfer(orbit1, orbit2)
        elif method == 'low-energy':
            return self.low_energy_transfer(orbit1, orbit2)
        else:
            raise ValueError(f"Unknown transfer method: {method}")
    
    def hohmann_transfer(self, orbit1: Dict, orbit2: Dict) -> Dict:
        """Calculate Hohmann transfer between two circular orbits"""
        
        r1 = orbit1['semi_major_axis_km']
        r2 = orbit2['semi_major_axis_km']
        
        # Transfer orbit semi-major axis
        a_transfer = (r1 + r2) / 2
        
        # Delta-v at periapsis
        v1_tp = np.sqrt(self.earth_mu / a_transfer) * (np.sqrt(2*r2/(r1+r2)) - 1)
        dv1 = abs(v1_tp - np.sqrt(self.earth_mu / r1))
        
        # Delta-v at apoapsis
        v2_ta = np.sqrt(self.earth_mu / a_transfer) * (1 - np.sqrt(2*r1/(r1+r2)))
        dv2 = abs(np.sqrt(self.earth_mu / r2) - v2_ta)
        
        total_dv = dv1 + dv2
        
        # Transfer time
        transfer_time = np.pi * np.sqrt(a_transfer**3 / self.earth_mu)
        
        return {
            'transfer_orbit': {
                'semi_major_axis_km': a_transfer,
                'eccentricity': (r2 - r1) / (r2 + r1),
                'period_min': 2 * np.pi * np.sqrt(a_transfer**3 / self.earth_mu) / 60
            },
            'delta_v': {
                'burn_1_km_s': dv1,
                'burn_2_km_s': dv2,
                'total_km_s': total_dv
            },
            'transfer_time_min': transfer_time / 60,
            'delta_v_efficiency': self.calculate_transfer_efficiency(orbit1, orbit2, total_dv)
        }
```

## 📊 Aerospace Dashboard

### Space Operations
```javascript
const SpaceDashboard = {
  satellites: {
    total: 150,
    operational: 142,
    decommissioned: 5,
    failed: 3,
    
    orbital_regimes: {
      leo: { count: 100, avg_altitude_km: 550 },
      m geo: { count: 30, avg_altitude_km: 20000 },
      heo: { count: 20, avg_altitude_km: 35786 }
    },
    
    mission_status: {
      nominal: 135,
      degraded: 7,
      critical: 3,
      testing: 5
    }
  },
  
  launchOperations: {
    launches_this_year: 12,
    success_rate: 0.917,
    avg_payload_mass_kg: 4500,
    on_time_performance: 0.85,
    
    upcoming_launches: [
      { mission: 'Sat-142', date: '2024-02-15', vehicle: 'Falcon-9' },
      { mission: 'Comm-23', date: '2024-02-28', vehicle: 'Atlas-V' }
    ]
  },
  
  stationOperations: {
    crew_size: 7,
    crew_rotation_days: 180,
    experiments_active: 45,
    eva_completed: 120,
    resupply_status: 'nominal'
  },
  
  tracking: {
    tle_accuracy_km: 0.5,
    conjunction_alerts: 15,
    debris_tracked: 25000,
    close_approach_warnings: 234
  },
  
  generateSpaceInsights: function() {
    const insights = [];
    
    // Satellite health
    if (this.satellites.mission_status.critical > 0) {
      insights.push({
        type: 'operations',
        level: 'critical',
        message: `${this.satellites.mission_status.critical} satellites in critical status`,
        recommendation: 'Immediate attention required for affected missions'
      });
    }
    
    // Launch performance
    if (this.launchOperations.success_rate < 0.95) {
      insights.push({
        type: 'launch',
        level: 'warning',
        message: `Launch success rate at ${(this.launchOperations.success_rate * 100).toFixed(1)}%`,
        recommendation: 'Review launch vehicle reliability and root causes'
      });
    }
    
    // Conjunction threats
    if (this.tracking.conjunction_alerts > 20) {
      insights.push({
        type: 'safety',
        level: 'medium',
        message: `${this.tracking.conjunction_alerts} conjunction alerts`,
        recommendation: 'Review avoidance maneuvers and tracking coverage'
      });
    }
    
    return insights;
  },
  
  predictMissionSuccess: function(launchParameters) {
    return {
      success_probability: 0.95,
      risk_factors: ['weather', 'vehicle_health', 'payload_integration'],
      contingency_options: ['hold', 'scrub', 'abort-to-orbit'],
      recommended_mitigations: this.generateMitigations(launchParameters),
      expected_orbit_insertion_accuracy_km: this.calculateInsertionAccuracy(launchParameters)
    };
  }
};
```

## 🎯 Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Orbital mechanics basics
- [ ] Satellite subsystem design
- [ ] Mission planning tools
- [ ] Ground segment setup

### Phase 2: Intelligence (Week 3-4)
- [ ] Advanced trajectory optimization
- [ ] Autonomous operations
- [ ] AI-assisted mission planning
- [ ] Constellation management

### Phase 3: Production (Week 5-6)
- [ ] Real-time operations
- [ ] Multi-mission coordination
- [ ] Failure prevention
- [ ] Cost optimization

## 📊 Success Metrics

### Aerospace Excellence
```yaml
orbital_operations:
  position_accuracy_km: "< 1"
  station_keeping: "> 99.5%"
  conjunction_avoidance: "100% success"
  uptime: "> 99.9%"
  
launch_operations:
  success_rate: "> 95%"
  on_time_performance: "> 90%"
  cost_per_kg: "< $2000"
  turnaround_time_days: "< 14"
  
mission_planning:
  trajectory_accuracy: "> 99%"
  fuel_efficiency: "> 95% optimal"
  risk_assessment: "comprehensive"
  schedule_adherence: "> 95%"
  
system_reliability:
  satellite_mtbf_years: "> 10"
  subsystem_redundancy: "2+ for critical"
  radiation_hardening: "> 100 krad"
  thermal_control: "> 99%"
```

---

*Design and operate space systems with physics-inspired aerospace engineering.* 🚀✨
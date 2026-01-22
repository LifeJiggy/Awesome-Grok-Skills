"""
Green Computing Pipeline
Sustainable computing and carbon footprint optimization
"""

import numpy as np
from typing import Dict, List, Optional
from dataclasses import dataclass
from dataclasses import field
from enum import Enum
from datetime import datetime


class EnergySource(Enum):
    GRID = "grid"
    SOLAR = "solar"
    WIND = "wind"
    HYDRO = "hydro"
    NUCLEAR = "nuclear"


@dataclass
class CarbonMetrics:
    electricity_kwh: float
    carbon_kg: float
    renewable_percent: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ServerMetrics:
    server_id: str
    cpu_utilization: float
    memory_utilization: float
    power_watts: float
    temperature_c: float


class CarbonCalculator:
    """Carbon footprint calculator"""
    
    def __init__(self):
        self.emission_factors = {
            EnergySource.GRID: 0.42,  # kg CO2 per kWh (average grid)
            EnergySource.SOLAR: 0.02,
            EnergySource.WIND: 0.01,
            EnergySource.HYDRO: 0.02,
            EnergySource.NUCLEAR: 0.02
        }
    
    def calculate_carbon(self, 
                        electricity_kwh: float,
                        energy_mix: Dict[EnergySource, float] = None) -> CarbonMetrics:
        """Calculate carbon emissions"""
        energy_mix = energy_mix or {EnergySource.GRID: 1.0}
        
        weighted_emission = 0
        for source, proportion in energy_mix.items():
            factor = self.emission_factors.get(source, 0.42)
            weighted_emission += factor * proportion
        
        carbon_kg = electricity_kwh * weighted_emission
        renewable_percent = sum(
            proportion for source, proportion in energy_mix.items()
            if source in [EnergySource.SOLAR, EnergySource.WIND, EnergySource.HYDRO]
        ) * 100
        
        return CarbonMetrics(
            electricity_kwh=electricity_kwh,
            carbon_kg=carbon_kg,
            renewable_percent=renewable_percent
        )
    
    def calculate_server_carbon(self, 
                               server: ServerMetrics) -> float:
        """Calculate carbon for single server"""
        power_kwh = server.power_watts * 24 * 30 / 1000  # Monthly
        return self.calculate_carbon(power_kwh).carbon_kg
    
    def calculate_datacenter_carbon(self, 
                                   servers: List[ServerMetrics]) -> Dict:
        """Calculate total datacenter carbon"""
        total_power = sum(s.power_watts for s in servers)
        total_carbon = sum(self.calculate_server_carbon(s) for s in servers)
        
        avg_utilization = np.mean([s.cpu_utilization for s in servers])
        pue = self._estimate_pue(avg_utilization)
        
        effective_power = total_power * pue
        effective_carbon = total_carbon * pue
        
        return {
            "total_power_watts": total_power,
            "effective_power_watts": effective_power,
            "total_carbon_kg": total_carbon,
            "effective_carbon_kg": effective_carbon,
            "pue": pue,
            "average_utilization": avg_utilization
        }
    
    def _estimate_pue(self, utilization: float) -> float:
        """Estimate PUE based on utilization"""
        base_pue = 1.58
        min_pue = 1.1
        return max(min_pue, base_pue - 0.4 * utilization)


class GreenComputingOptimizer:
    """Optimize computing for sustainability"""
    
    def __init__(self):
        self.target_pue = 1.2
        self.target_renewable = 80.0
    
    def optimize_scheduling(self, 
                           tasks: List[Dict],
                           energy_mix: Dict[EnergySource, float],
                           carbon_price: float = 50) -> List[Dict]:
        """Schedule tasks for minimal carbon"""
        
        def task_carbon(task):
            compute_hours = task.get("compute_hours", 1)
            power_kw = task.get("power_kw", 0.1)
            electricity = compute_hours * power_kw
            
            carbon = self.carbon_calculator.calculate_carbon(electricity, energy_mix)
            
            return carbon.carbon_kg * (1 + carbon_price / 1000)
        
        return sorted(tasks, key=task_carbon)
    
    def suggest_right_sizing(self, 
                            servers: List[ServerMetrics],
                            target_utilization: float = 0.7) -> List[Dict]:
        """Suggest right-sizing recommendations"""
        recommendations = []
        
        for server in servers:
            if server.cpu_utilization < target_utilization * 0.5:
                recommendations.append({
                    "server_id": server.server_id,
                    "action": "consolidate",
                    "reason": f"Low CPU utilization ({server.cpu_utilization:.1%})",
                    "potential_savings_percent": 30
                })
            elif server.cpu_utilization > target_utilization * 1.5:
                recommendations.append({
                    "server_id": server.server_id,
                    "action": "upgrade",
                    "reason": f"High CPU utilization ({server.cpu_utilization:.1%})",
                    "potential_savings_percent": 10
                })
        
        return recommendations
    
    def optimize_cooling(self, 
                        servers: List[ServerMetrics],
                        ambient_temp: float = 25.0) -> Dict:
        """Optimize cooling strategy"""
        avg_temp = np.mean([s.temperature_c for s in servers])
        avg_utilization = np.mean([s.cpu_utilization for s in servers])
        
        cooling_power_percent = 0.3  # Typical
        
        if avg_temp > 28:
            recommended_cooling = "liquid"
            efficiency_gain = 20
        elif avg_utilization > 0.8:
            recommended_cooling = "liquid"
            efficiency_gain = 15
        else:
            recommended_cooling = "air"
            efficiency_gain = 0
        
        return {
            "current_cooling": "air",
            "recommended_cooling": recommended_cooling,
            "efficiency_gain_percent": efficiency_gain,
            "estimated_savings_watts": sum(s.power_watts for s in servers) * cooling_power_percent * efficiency_gain / 100
        }


class RenewableEnergyManager:
    """Manage renewable energy integration"""
    
    def __init__(self):
        self.solar_capacity_kw = 0
        self.wind_capacity_kw = 0
        self.battery_capacity_kwh = 0
        self.grid_reliance = 1.0
    
    def calculate_self_consumption(self, 
                                  hourly_demand: List[float],
                                  solar_generation: List[float]) -> Dict:
        """Calculate self-consumption ratio"""
        total_demand = sum(hourly_demand)
        total_solar = sum(solar_generation)
        
        self_consumed = 0
        battery_charge = 0
        grid_import = 0
        
        for demand, solar in zip(hourly_demand, solar_generation):
            if solar >= demand:
                excess = solar - demand
                if battery_charge + excess <= self.battery_capacity_kwh:
                    battery_charge += excess
                    self_consumed += demand
                else:
                    self_consumed += self.battery_capacity_kwh - battery_charge
                    grid_import += demand - self.battery_capacity_kwh - battery_charge
            else:
                deficit = demand - solar
                if battery_charge >= deficit:
                    battery_charge -= deficit
                    self_consumed += solar + deficit
                else:
                    battery_drain = battery_charge
                    battery_charge = 0
                    grid_import += deficit - battery_drain
                    self_consumed += solar + battery_drain
        
        self_consumption_ratio = self_consumed / total_demand if total_demand > 0 else 0
        
        return {
            "self_consumption_ratio": self_consumption_ratio * 100,
            "grid_import_kwh": grid_import,
            "battery_charge_kwh": battery_charge,
            "renewable_utilization": min(100, (self_consumed / total_solar) * 100) if total_solar > 0 else 0
        }
    
    def size_solar_system(self, 
                         daily_demand_kwh: float,
                         peak_sun_hours: float = 5) -> Dict:
        """Size solar PV system"""
        required_capacity = daily_demand_kwh / peak_sun_hours
        
        panel_area = required_capacity / 0.2  # 20% efficiency
        
        return {
            "solar_capacity_kw": required_capacity,
            "panel_area_sqm": panel_area,
            "estimated_annual_generation_kwh": required_capacity * peak_sun_hours * 365,
            "roof_requirement_sqm": panel_area * 1.5
        }
    
    def calculate_carbon_savings(self, 
                                renewable_kwh: float,
                                grid_emission_factor: float = 0.42) -> float:
        """Calculate carbon savings from renewable energy"""
        return renewable_kwh * grid_emission_factor


class CloudCarbonEstimator:
    """Estimate cloud service carbon footprint"""
    
    def __init__(self):
        self.regional_emissions = {
            "us-east": 0.35,
            "us-west": 0.30,
            "eu-west": 0.25,
            "eu-north": 0.10,
            "ap-southeast": 0.45,
            "ap-northeast": 0.35
        }
    
    def estimate_vm_carbon(self, 
                          vm_specs: Dict,
                          hours: float,
                          region: str = "us-east") -> Dict:
        """Estimate VM carbon footprint"""
        emission_factor = self.regional_emissions.get(region, 0.42)
        
        compute_power = (
            vm_specs.get("vcpu", 2) * 0.1 +
            vm_specs.get("memory_gb", 4) * 0.01 +
            vm_specs.get("storage_gb", 100) * 0.0005
        )
        
        electricity_kwh = compute_power * hours
        carbon_kg = electricity_kwh * emission_factor
        
        return {
            "electricity_kwh": electricity_kwh,
            "carbon_kg": carbon_kg,
            "emission_factor": emission_factor,
            "region": region
        }
    
    def suggest_green_region(self, 
                            tasks: List[Dict]) -> str:
        """Suggest most sustainable region for workload"""
        emissions = {
            region: sum(
                self.estimate_vm_carbon(task, task.get("hours", 1), region)["carbon_kg"]
                for task in tasks
            )
            for region in self.regional_emissions.keys()
        }
        
        return min(emissions, key=emissions.get)


if __name__ == "__main__":
    carbon_calc = CarbonCalculator()
    green_opt = GreenComputingOptimizer()
    renewable_mgr = RenewableEnergyManager()
    cloud_estimator = CloudCarbonEstimator()
    
    metrics = carbon_calc.calculate_carbon(1000)
    
    servers = [
        ServerMetrics("server1", 0.3, 0.4, 200, 35),
        ServerMetrics("server2", 0.8, 0.7, 450, 42),
        ServerMetrics("server3", 0.2, 0.3, 150, 32)
    ]
    
    dc_carbon = carbon_calc.calculate_datacenter_carbon(servers)
    recommendations = green_opt.suggest_right_sizing(servers)
    cooling = green_opt.optimize_cooling(servers)
    
    hourly_demand = [10, 15, 20, 25, 30, 35, 40, 45, 50, 45, 35, 25, 20, 15, 10, 12, 15, 18, 20, 22, 18, 15, 12, 10]
    solar_gen = [0, 0, 1, 5, 15, 25, 30, 32, 30, 25, 18, 10, 5, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    self_consumption = renewable_mgr.calculate_self_consumption(hourly_demand, solar_gen)
    
    vm_specs = {"vcpu": 4, "memory_gb": 16, "storage_gb": 500}
    vm_carbon = cloud_estimator.estimate_vm_carbon(vm_specs, 720, "eu-north")
    
    print(f"Carbon: {metrics.carbon_kg:.2f} kg CO2")
    print(f"Datacenter carbon: {dc_carbon['effective_carbon_kg']:.2f} kg")
    print(f"Recommendations: {len(recommendations)}")
    print(f"Optimal cooling: {cooling['recommended_cooling']}")
    print(f"Self-consumption: {self_consumption['self_consumption_ratio']:.1f}%")
    print(f"VM carbon (eu-north): {vm_carbon['carbon_kg']:.2f} kg")

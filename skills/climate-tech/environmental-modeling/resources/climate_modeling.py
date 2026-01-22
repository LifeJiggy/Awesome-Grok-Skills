"""
Climate Modeling Pipeline
Environmental simulation and carbon tracking
"""

import numpy as np
from typing import Dict, List, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ClimateData:
    temperature: float
    co2_concentration: float
    sea_level: float
    timestamp: datetime


class CarbonTracker:
    """Track and calculate carbon emissions"""
    
    def __init__(self):
        self.emission_factors = {
            "electricity": 0.42,  # kg CO2 per kWh
            "natural_gas": 2.0,   # kg CO2 per therm
            "transportation": 2.31,  # kg CO2 per gallon gasoline
            "flights": 0.255  # kg CO2 per mile
        }
    
    def calculate_emissions(self, activity_type: str, amount: float) -> float:
        """Calculate CO2 emissions for activity"""
        factor = self.emission_factors.get(activity_type, 1.0)
        return amount * factor
    
    def track_period(self, activities: List[Dict]) -> Dict:
        """Track emissions over period"""
        total = 0
        by_category = {}
        
        for activity in activities:
            emissions = self.calculate_emissions(
                activity["type"],
                activity["amount"]
            )
            total += emissions
            by_category[activity["type"]] = by_category.get(activity["type"], 0) + emissions
        
        return {
            "total_emissions": total,
            "by_category": by_category,
            "offset_required": total * 1.1  # 10% buffer
        }


class ClimateModel:
    """Climate simulation model"""
    
    def __init__(self):
        self.baseline_temp = 14.5  # Global average in Celsius
        self.baseline_co2 = 280  # Pre-industrial ppm
    
    def simulate_warming(self, years: int, emissions_scenario: str) -> List[Dict]:
        """Simulate temperature change over years"""
        scenarios = {
            "optimistic": 0.02,
            "moderate": 0.035,
            "pessimistic": 0.05
        }
        
        rate = scenarios.get(emissions_scenario, 0.035)
        results = []
        
        for year in range(years):
            temp_increase = rate * year
            results.append({
                "year": 2024 + year,
                "temperature": self.baseline_temp + temp_increase,
                "co2": self.baseline_co2 * (1 + rate * 0.8 * year)
            })
        
        return results
    
    def calculate_feedback(self, temp_change: float) -> Dict:
        """Calculate climate feedback mechanisms"""
        return {
            "ice_albedo": temp_change * 0.3,
            "water_vapor": temp_change * 0.6,
            "cloud": temp_change * -0.1,
            "total_feedback": temp_change * 0.8
        }


class RenewableOptimizer:
    """Optimize renewable energy systems"""
    
    def __init__(self):
        self.panel_efficiency = 0.22  # 22% efficiency
        self.wind_capacity_factor = 0.35
    
    def calculate_solar_output(self, 
                               panel_area: float, 
                               solar_irradiance: float,
                               hours: float) -> float:
        """Calculate solar panel output"""
        return panel_area * solar_irradiance * self.panel_efficiency * hours
    
    def calculate_wind_output(self,
                              turbine_rating: float,
                              wind_speed: float) -> float:
        """Calculate wind turbine output"""
        rated_speed = 12.0  # m/s
        cut_in_speed = 3.5
        
        if wind_speed < cut_in_speed:
            return 0
        elif wind_speed >= rated_speed:
            return turbine_rating
        else:
            return turbine_rating * ((wind_speed - cut_in_speed) / (rated_speed - cut_in_speed)) ** 3
    
    def optimize_mix(self, 
                    demand: float, 
                    solar_potential: float,
                    wind_potential: float) -> Dict:
        """Optimize renewable energy mix"""
        solar_share = min(demand, solar_potential) / demand
        wind_share = min(demand - solar_potential, wind_potential) / demand
        grid_share = 1 - solar_share - wind_share
        
        return {
            "solar": solar_share * 100,
            "wind": wind_share * 100,
            "grid": max(0, grid_share) * 100
        }


if __name__ == "__main__":
    tracker = CarbonTracker()
    model = ClimateModel()
    optimizer = RenewableOptimizer()
    
    activities = [
        {"type": "electricity", "amount": 500},
        {"type": "transportation", "amount": 100}
    ]
    
    emissions = tracker.track_period(activities)
    warming = model.simulate_warming(10, "moderate")
    energy_mix = optimizer.optimize_mix(1000, 400, 300)
    
    print(f"Total emissions: {emissions['total_emissions']:.2f} kg CO2")
    print(f"10-year warming projection: {warming[-1]['temperature']:.2f}°C")
    print(f"Optimal energy mix: {energy_mix}")

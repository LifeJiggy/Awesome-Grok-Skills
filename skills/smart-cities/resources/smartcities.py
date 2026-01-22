#!/usr/bin/env python3
"""
Smart Cities - Urban Intelligence Implementation
Smart city infrastructure, transportation, and citizen services.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json
import random

class InfrastructureType(Enum):
    TRANSPORTATION = "transportation"
    ENERGY = "energy"
    WATER = "water"
    WASTE = "waste"
    TELECOMMUNICATION = "telecommunication"
    PUBLIC_SAFETY = "public_safety"

class TransportMode(Enum):
    BUS = "bus"
    SUBWAY = "subway"
    TRAM = "tram"
    BIKE = "bike"
    CAR = "car"
    WALK = "walk"

class IncidentSeverity(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class TrafficSensor:
    id: str
    location: Dict[str, float]
    road_type: str
    lanes: int
    current_flow: int
    speed_avg: float
    congestion_level: str

@dataclass
class EnergyConsumption:
    zone_id: str
    timestamp: datetime
    residential: float
    commercial: float
    industrial: float
    public: float
    renewable_percentage: float

@dataclass
class PublicTransportVehicle:
    id: str
    route_id: str
    mode: TransportMode
    current_location: Dict[str, float]
    occupancy: int
    capacity: int
    next_stop: str
    delay_minutes: float

@dataclass
class CityIncident:
    id: str
    type: str
    location: Dict[str, float]
    severity: IncidentSeverity
    status: str
    timestamp: datetime
    description: str
    affected_areas: List[str]

class TrafficManagementSystem:
    """Manages urban traffic flow."""
    
    def __init__(self):
        self.sensors: Dict[str, TrafficSensor] = {}
        self.signals: Dict[str, Dict] = {}
        self.incidents: List[CityIncident] = []
    
    def add_sensor(self, sensor_id: str, location: Dict[str, float],
                  road_type: str, lanes: int) -> TrafficSensor:
        """Add traffic sensor."""
        sensor = TrafficSensor(
            id=sensor_id,
            location=location,
            road_type=road_type,
            lanes=lanes,
            current_flow=random.randint(100, 2000),
            speed_avg=random.uniform(20, 60),
            congestion_level='low'
        )
        self.sensors[sensor_id] = sensor
        return sensor
    
    def update_traffic(self, sensor_id: str) -> Dict[str, Any]:
        """Update traffic data for sensor."""
        if sensor_id not in self.sensors:
            return {'error': 'Sensor not found'}
        
        sensor = self.sensors[sensor_id]
        sensor.current_flow = random.randint(100, 2500)
        sensor.speed_avg = random.uniform(15, 65)
        
        capacity = sensor.lanes * 2000
        flow_ratio = sensor.current_flow / capacity
        
        if flow_ratio > 0.85:
            sensor.congestion_level = 'severe'
        elif flow_ratio > 0.65:
            sensor.congestion_level = 'high'
        elif flow_ratio > 0.45:
            sensor.congestion_level = 'moderate'
        else:
            sensor.congestion_level = 'low'
        
        return {
            'sensor_id': sensor_id,
            'flow': sensor.current_flow,
            'speed': round(sensor.speed_avg, 1),
            'congestion': sensor.congestion_level
        }
    
    def calculate_congestion_index(self) -> float:
        """Calculate overall city congestion index."""
        if not self.sensors:
            return 0
        
        congestion_scores = {
            'low': 0.2,
            'moderate': 0.4,
            'high': 0.7,
            'severe': 0.9
        }
        
        total_score = sum(
            congestion_scores.get(s.congestion_level, 0.5)
            for s in self.sensors.values()
        )
        
        return round(total_score / len(self.sensors), 2)
    
    def optimize_signal_timing(self, intersection_id: str,
                              traffic_data: Dict) -> Dict[str, Any]:
        """Optimize traffic signal timing."""
        return {
            'intersection_id': intersection_id,
            'current_cycle': 120,
            'optimized_cycle': 90,
            'phases': [
                {'direction': 'north-south', 'green_time': 45},
                {'direction': 'east-west', 'green_time': 45}
            ],
            'expected_improvement': {
                'delay_reduction': '15%',
                'throughput_increase': '12%',
                'emissions_reduction': '8%'
            }
        }

class SmartGridManager:
    """Manages smart energy grid."""
    
    def __init__(self):
        self.zones: Dict[str, EnergyConsumption] = {}
        self.generation_sources: Dict[str, Dict] = {}
        self.grid_status = 'stable'
    
    def add_zone_consumption(self, zone_id: str) -> EnergyConsumption:
        """Add zone energy consumption data."""
        consumption = EnergyConsumption(
            zone_id=zone_id,
            timestamp=datetime.now(),
            residential=random.uniform(50, 150),
            commercial=random.uniform(30, 100),
            industrial=random.uniform(20, 80),
            public=random.uniform(10, 30),
            renewable_percentage=random.uniform(20, 50)
        )
        self.zones[zone_id] = consumption
        return consumption
    
    def get_demand_forecast(self, hours: int = 24) -> Dict[str, Any]:
        """Forecast energy demand."""
        forecast = []
        base_demand = 500
        
        for i in range(hours):
            hour = datetime.now().hour + i
            hour_of_day = hour % 24
            
            if 6 <= hour_of_day < 9:
                multiplier = 1.3
            elif 9 <= hour_of_day < 17:
                multiplier = 1.1
            elif 17 <= hour_of_day < 21:
                multiplier = 1.4
            elif 22 <= hour_of_day < 6:
                multiplier = 0.7
            else:
                multiplier = 0.9
            
            demand = base_demand * multiplier + random.uniform(-30, 30)
            forecast.append({
                'hour': hour_of_day,
                'demand_MW': round(demand, 1),
                'renewable_available': round(demand * random.uniform(0.2, 0.4), 1)
            })
        
        peak_demand = max(f['demand_MW'] for f in forecast)
        total_demand = sum(f['demand_MW'] for f in forecast)
        
        return {
            'forecast': forecast,
            'peak_demand_MW': round(peak_demand, 1),
            'total_demand_MWh': round(total_demand, 1),
            'peak_hour': forecast[forecast.index(max(forecast, key=lambda x: x['demand_MW']))]['hour']
        }
    
    def optimize_grid(self) -> Dict[str, Any]:
        """Optimize grid operations."""
        total_generation = sum(g['capacity'] for g in self.generation_sources.values())
        total_demand = sum(z.residential + z.commercial + z.industrial + z.public 
                          for z in self.zones.values())
        
        load_factor = total_demand / total_generation if total_generation > 0 else 0.8
        
        return {
            'grid_status': 'stable',
            'total_generation_MW': round(total_generation, 1),
            'total_demand_MW': round(total_demand, 1),
            'reserve_margin': round((1 - load_factor) * 100, 1),
            'renewable_share': round(sum(z.renewable_percentage for z in self.zones.values()) / 
                                    len(self.zones) if self.zones else 25, 1),
            'recommendations': [
                "Increase solar capacity in Zone B",
                "Implement demand response in residential areas",
                "Upgrade transmission lines in Zone C"
            ]
        }

class PublicTransportSystem:
    """Manages public transportation."""
    
    def __init__(self):
        self.vehicles: Dict[str, PublicTransportVehicle] = {}
        self.routes: Dict[str, Dict] = {}
        self.stops: List[Dict] = []
    
    def add_vehicle(self, vehicle_id: str, route_id: str,
                   mode: TransportMode, capacity: int) -> PublicTransportVehicle:
        """Add vehicle to fleet."""
        vehicle = PublicTransportVehicle(
            id=vehicle_id,
            route_id=route_id,
            mode=mode,
            current_location={'lat': random.uniform(40, 41), 'lon': random.uniform(-74, -73)},
            occupancy=random.randint(0, capacity),
            capacity=capacity,
            next_stop=f"Stop_{random.randint(1, 20)}",
            delay_minutes=random.uniform(-2, 10)
        )
        self.vehicles[vehicle_id] = vehicle
        return vehicle
    
    def get_route_optimization(self, route_id: str) -> Dict[str, Any]:
        """Optimize bus/tram route."""
        return {
            'route_id': route_id,
            'current_stops': 25,
            'optimized_stops': 22,
            'on_time_performance': round(random.uniform(75, 95), 1),
            'passenger_satisfaction': round(random.uniform(3.5, 4.5), 1),
            'frequency_recommendation': {
                'peak': 'every 8 minutes',
                'off_peak': 'every 12 minutes',
                'night': 'every 20 minutes'
            },
            'improvements': [
                "Remove redundant stops at Stops 7 and 15",
                "Add express service during peak hours",
                "Implement real-time passenger information"
            ]
        }
    
    def calculate_ridership_prediction(self, route_id: str,
                                       date: datetime) -> Dict[str, Any]:
        """Predict ridership for route."""
        base_ridership = random.uniform(500, 2000)
        
        day_of_week = date.weekday()
        if day_of_week < 5:
            multiplier = 1.0
        else:
            multiplier = 0.6
        
        return {
            'route_id': route_id,
            'date': date.date().isoformat(),
            'predicted_ridership': round(base_ridership * multiplier),
            'peak_hours': ['07:00-09:00', '17:00-19:00'],
            'vehicle_capacity_needed': round(base_ridership * multiplier / 50),
            'crowding_risk': 'high' if base_ridership > 1500 else 'medium' if base_ridership > 1000 else 'low'
        }

class PublicSafetySystem:
    """Manages public safety and emergency services."""
    
    def __init__(self):
        self.incidents: List[CityIncident] = []
        self.resources: Dict[str, Dict] = {}
    
    def report_incident(self, incident_type: str,
                       location: Dict[str, float],
                       severity: IncidentSeverity,
                       description: str) -> CityIncident:
        """Report safety incident."""
        incident = CityIncident(
            id=f"INC_{len(self.incidents) + 1}",
            type=incident_type,
            location=location,
            severity=severity,
            status='active',
            timestamp=datetime.now(),
            description=description,
            affected_areas=[]
        )
        self.incidents.append(incident)
        return incident
    
    def dispatch_emergency(self, incident_id: str) -> Dict[str, Any]:
        """Dispatch emergency response."""
        incident = next((i for i in self.incidents if i.id == incident_id), None)
        if not incident:
            return {'error': 'Incident not found'}
        
        response = {
            'incident_id': incident_id,
            'units_dispatched': {
                'police': 1 if incident.type in ['crime', 'accident'] else 0,
                'fire': 1 if incident.type in ['fire', 'accident'] else 0,
                'medical': 1 if incident.type in ['medical', 'accident'] else 0
            },
            'eta_minutes': random.randint(3, 15),
            'recommended_route': self._get_route_to_location(incident.location),
            'status': 'dispatched'
        }
        
        incident.status = 'responding'
        return response
    
    def _get_route_to_location(self, location: Dict) -> List[Dict]:
        """Get route to incident location."""
        return [
            {'road': 'Main St', 'direction': 'north', 'distance_m': 500},
            {'road': 'Oak Ave', 'direction': 'east', 'distance_m': 300}
        ]
    
    def get_crime_prediction(self, district_id: str) -> Dict[str, Any]:
        """Predict crime risk for district."""
        return {
            'district': district_id,
            'risk_score': round(random.uniform(20, 80), 1),
            'predicted_incidents': random.randint(5, 20),
            'high_risk_areas': ['Zone A', 'Zone C'],
            'time_patterns': {
                'peak_hours': ['22:00-02:00'],
                'low_risk_hours': ['06:00-12:00']
            },
            'recommendations': [
                "Increase patrol in Zone A after 10 PM",
                "Install additional lighting in Zone C",
                "Community outreach program in high-risk areas"
            ]
        }

class EnvironmentalMonitor:
    """Monitors urban environmental quality."""
    
    def __init__(self):
        self.air_quality_stations: Dict[str, Dict] = []
        self.noise_sensors: Dict[str, float] = {}
    
    def measure_air_quality(self, station_id: str) -> Dict[str, Any]:
        """Measure air quality at station."""
        aqi = random.randint(20, 150)
        
        if aqi <= 50:
            quality = 'Good'
            color = 'Green'
        elif aqi <= 100:
            quality = 'Moderate'
            color = 'Yellow'
        elif aqi <= 150:
            quality = 'Unhealthy for Sensitive Groups'
            color = 'Orange'
        else:
            quality = 'Unhealthy'
            color = 'Red'
        
        return {
            'station_id': station_id,
            'aqi': aqi,
            'quality': quality,
            'color_code': color,
            'pollutants': {
                'pm25': round(random.uniform(5, 50), 1),
                'pm10': round(random.uniform(10, 80), 1),
                'no2': round(random.uniform(10, 60), 1),
                'o3': round(random.uniform(20, 80), 1),
                'co': round(random.uniform(0.5, 2.0), 2)
            },
            'health_recommendation': 'Limit outdoor activity' if aqi > 100 else 'No restrictions'
        }
    
    def get_city_environmental_report(self) -> Dict[str, Any]:
        """Get city-wide environmental report."""
        avg_aqi = random.randint(40, 80)
        
        return {
            'air_quality': {
                'average_aqi': avg_aqi,
                'status': 'Moderate',
                'trend': 'improving'
            },
            'noise': {
                'avg_level_db': round(random.uniform(55, 70), 1),
                'quiet_zones': 5,
                'noise_complaints': random.randint(10, 50)
            },
            'green_space': {
                'parks_count': random.randint(20, 50),
                'green_coverage_percent': round(random.uniform(20, 35), 1),
                'tree_count': random.randint(50000, 150000)
            },
            'sustainability': {
                'renewable_energy_percent': round(random.uniform(20, 40), 1),
                'recycling_rate_percent': round(random.uniform(35, 55), 1),
                'electric_vehicle_charging_stations': random.randint(100, 300)
            }
        }

class SmartCitiesAgent:
    """Main Smart Cities agent."""
    
    def __init__(self):
        self.traffic = TrafficManagementSystem()
        self.energy = SmartGridManager()
        self.transport = PublicTransportSystem()
        self.safety = PublicSafetySystem()
        self.environment = EnvironmentalMonitor()
    
    def get_city_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive city dashboard."""
        return {
            'traffic': {
                'congestion_index': self.traffic.calculate_congestion_index(),
                'active_sensors': len(self.traffic.sensors),
                'active_incidents': len([i for i in self.traffic.incidents if i.status == 'active'])
            },
            'energy': {
                'grid_status': self.energy.grid_status,
                'demand_forecast': self.energy.get_demand_forecast()['peak_demand_MW'],
                'renewable_share': 35.0
            },
            'transport': {
                'active_vehicles': len(self.transport.vehicles),
                'on_time_performance': 88.5,
                'daily_ridership': random.randint(50000, 150000)
            },
            'safety': {
                'active_incidents': len([i for i in self.safety.incidents if i.status == 'active']),
                'avg_response_time': 8.5,
                'crime_risk': 35.0
            },
            'environment': {
                'air_quality': 55,
                'green_coverage': 28.5,
                'sustainability_score': 72.0
            },
            'overall_smart_index': round(random.uniform(65, 85), 1)
        }
    
    def optimize_city_operations(self) -> Dict[str, Any]:
        """Generate city optimization recommendations."""
        return {
            'traffic_optimization': self.traffic.calculate_congestion_index(),
            'energy_optimization': self.energy.optimize_grid(),
            'transport_optimization': self.transport.get_route_optimization('ROUTE_001'),
            'safety_improvements': self.safety.get_crime_prediction('DISTRICT_1'),
            'environmental_actions': self.environment.get_city_environmental_report(),
            'investment_priorities': [
                {'area': 'Public Transit', 'priority': 'high', 'estimated_cost': '$50M'},
                {'area': 'Smart Grid', 'priority': 'high', 'estimated_cost': '$35M'},
                {'area': 'Bike Infrastructure', 'priority': 'medium', 'estimated_cost': '$15M'},
                {'area': 'Green Spaces', 'priority': 'medium', 'estimated_cost': '$20M'}
            ]
        }

def main():
    """Main entry point."""
    agent = SmartCitiesAgent()
    
    dashboard = agent.get_city_dashboard()
    print(f"City Dashboard: {dashboard}")

if __name__ == "__main__":
    main()

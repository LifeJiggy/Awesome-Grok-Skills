#!/usr/bin/env python3
"""
OceanTech - Ocean & Marine Technology Implementation
Ocean exploration, fisheries management, and marine ecosystem monitoring.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json
import random
import math

class MarineZone(Enum):
    LITTORAL = "littoral"
    NERITIC = "neritic"
    OCEANIC = "oceanic"
    ABYSSAL = "abyssal"
    HADAL = "hadal"

class SpeciesType(Enum):
    FISH = "fish"
    CRUSTACEAN = "crustacean"
    MAMMAL = "mammal"
    PLANKTON = "plankton"
    CORAL = "coral"
    SEAGRASS = "seagrass"

class FishingMethod(Enum):
    TRAWLING = "trawling"
    LONGLINING = "longlining"
    PURSE_SEINING = "purse_seining"
    GILLNETTING = "gillnetting"
    HANDLINE = "handline"
    TRAP = "trap"

@dataclass
class MarineSpecies:
    id: str
    name: str
    scientific_name: str
    species_type: SpeciesType
    habitat_depth_min: float
    habitat_depth_max: float
    conservation_status: str
    commercial_value: float

@dataclass
class OceanDataPoint:
    id: str
    location: Dict[str, float]
    depth: float
    timestamp: datetime
    temperature: float
    salinity: float
    oxygen: float
    ph: float
    turbidity: float

@dataclass
class FishStock:
    species_id: str
    zone: MarineZone
    biomass: float
    exploitation_rate: float
    msy: float
    recruitment: float
    mortality_rate: float

@dataclass
class FishingOperation:
    id: str
    vessel_id: str
    method: FishingMethod
    zone: MarineZone
    duration_hours: float
    catch: Dict[str, float]
    bycatch: Dict[str, float]
    fuel_consumed: float

class OceanSensorNetwork:
    """Manages ocean sensor network."""
    
    def __init__(self):
        self.buoys: Dict[str, Dict] = {}
        self.data_stream: List[OceanDataPoint] = []
    
    def deploy_buoy(self, buoy_id: str, location: Dict[str, float],
                   depth_rating: float) -> Dict[str, Any]:
        """Deploy ocean sensor buoy."""
        buoy = {
            'buoy_id': buoy_id,
            'location': location,
            'depth_rating': depth_rating,
            'sensors': ['temperature', 'salinity', 'oxygen', 'ph', 'turbidity'],
            'status': 'active',
            'battery_level': 95,
            'last_maintenance': datetime.now(),
            'data_transmission': 'satellite'
        }
        self.buoys[buoy_id] = buoy
        return buoy
    
    def collect_data(self, buoy_id: str) -> OceanDataPoint:
        """Collect ocean data from buoy."""
        data = OceanDataPoint(
            id=f"DP_{len(self.data_stream) + 1}",
            location=self.buoys[buoy_id]['location'],
            depth=random.uniform(5, 100),
            timestamp=datetime.now(),
            temperature=random.uniform(18, 28),
            salinity=random.uniform(34, 37),
            oxygen=random.uniform(4, 8),
            ph=random.uniform(7.8, 8.2),
            turbidity=random.uniform(1, 10)
        )
        self.data_stream.append(data)
        return data
    
    def analyze_water_quality(self, data: OceanDataPoint) -> Dict[str, Any]:
        """Analyze water quality from sensor data."""
        quality_score = 100
        
        if 20 <= data.temperature <= 26:
            pass
        else:
            quality_score -= 15
            recommendations = ["Temperature outside optimal range"]
        
        if 35 <= data.salinity <= 36:
            pass
        else:
            quality_score -= 10
        
        if data.oxygen >= 5:
            pass
        else:
            quality_score -= 20
            recommendations = ["Low dissolved oxygen - possible hypoxia"]
        
        if 8.0 <= data.ph <= 8.2:
            pass
        else:
            quality_score -= 10
        
        if data.turbidity < 5:
            pass
        else:
            quality_score -= 5
        
        return {
            'quality_score': max(0, quality_score),
            'status': 'excellent' if quality_score >= 90 else 'good' if quality_score >= 70 else 'poor',
            'parameters': {
                'temperature': data.temperature,
                'salinity': data.salinity,
                'oxygen': data.oxygen,
                'ph': data.ph
            },
            'recommendations': recommendations if 'recommendations' in dir() else []
        }

class FishStockManager:
    """Manages fish stock assessment and quotas."""
    
    def __init__(self):
        self.stocks: Dict[str, FishStock] = {}
        self.species_database: Dict[str, MarineSpecies] = {}
    
    def add_species(self, name: str, scientific_name: str,
                   species_type: SpeciesType, depth_min: float,
                   depth_max: float, conservation: str,
                   value: float) -> MarineSpecies:
        """Add species to database."""
        species = MarineSpecies(
            id=f"SP_{len(self.species_database) + 1}",
            name=name,
            scientific_name=scientific_name,
            species_type=species_type,
            habitat_depth_min=depth_min,
            habitat_depth_max=depth_max,
            conservation_status=conservation,
            commercial_value=value
        )
        self.species_database[species.id] = species
        return species
    
    def assess_stock(self, species_id: str, zone: MarineZone,
                    survey_data: Dict) -> FishStock:
        """Assess fish stock status."""
        species = self.species_database.get(species_id)
        if not species:
            return None
        
        biomass = survey_data.get('biomass', 1000)
        exploitation = survey_data.get('exploitation_rate', 0.3)
        
        msy = biomass * 0.2
        recruitment = biomass * 0.15
        mortality = exploitation * 0.1
        
        stock = FishStock(
            species_id=species_id,
            zone=zone,
            biomass=biomass,
            exploitation_rate=exploitation,
            msy=msy,
            recruitment=recruitment,
            mortality_rate=mortality
        )
        
        self.stocks[f"{species_id}_{zone.value}"] = stock
        return stock
    
    def calculate_quota(self, stock: FishStock) -> Dict[str, Any]:
        """Calculate sustainable fishing quota."""
        if stock.exploitation_rate >= 0.5:
            quota = 0
            recommendation = "Stock overexploited - moratorium recommended"
        elif stock.exploitation_rate >= 0.4:
            quota = stock.msy * 0.5
            recommendation = "Reduce fishing effort significantly"
        elif stock.exploitation_rate >= 0.3:
            quota = stock.msy * 0.8
            recommendation = "Maintain current limits"
        else:
            quota = stock.msy
            recommendation = "Stock healthy - can consider quota increase"
        
        return {
            'recommended_quota': round(quota, 2),
            'current_exploitation': stock.exploitation_rate,
            'maximum_sustainable_yield': stock.msy,
            'recommendation': recommendation,
            'status': 'critical' if stock.exploitation_rate >= 0.5 else 'warning' if stock.exploitation_rate >= 0.4 else 'healthy'
        }

class FisheriesOptimizer:
    """Optimizes fishing operations."""
    
    def __init__(self):
        self.operations: List[FishingOperation] = []
    
    def plan_fishing_trip(self, vessel_id: str, method: FishingMethod,
                         target_species: List[str], duration_days: int) -> Dict[str, Any]:
        """Plan optimized fishing trip."""
        expected_catch = {}
        for species in target_species:
            base_catch = random.uniform(50, 200)
            method_multiplier = {
                FishingMethod.TRAWLING: 1.5,
                FishingMethod.LONGLINING: 1.0,
                FishingMethod.PURSE_SEINING: 1.3,
                FishingMethod.GILLNETTING: 0.9,
                FishingMethod.HANDLINE: 0.6,
                FishingMethod.TRAP: 0.7
            }
            expected_catch[species] = round(base_catch * method_multiplier.get(method, 1.0) * duration_days, 2)
        
        fuel_estimate = duration_days * 500 * (1 + method_multiplier.get(method, 1.0) * 0.3)
        
        return {
            'vessel_id': vessel_id,
            'method': method.value,
            'duration_days': duration_days,
            'expected_catch': expected_catch,
            'estimated_fuel': round(fuel_estimate, 2),
            'co2_emissions': round(fuel_estimate * 3.1, 2),
            'recommended_zones': self._get_best_zones(method, target_species),
            'bycatch_risk': self._assess_bycatch_risk(method),
            'compliance_check': {
                'quota_compliance': True,
                'season_open': True,
                'area_permitted': True
            }
        }
    
    def _get_best_zones(self, method: FishingMethod,
                       target_species: List[str]) -> List[str]:
        """Get optimal fishing zones."""
        return ["Zone A-12", "Zone B-07", "Zone C-03"]
    
    def _assess_bycatch_risk(self, method: FishingMethod) -> Dict[str, Any]:
        """Assess bycatch risk for method."""
        risk_levels = {
            FishingMethod.TRAWLING: {'risk': 'high', 'species': ['turtles', 'dolphins']},
            FishingMethod.LONGLINING: {'risk': 'medium', 'species': ['seabirds']},
            FishingMethod.PURSE_SEINING: {'risk': 'medium', 'species': ['small_cetaceans']},
            FishingMethod.GILLNETTING: {'risk': 'high', 'species': ['marine_mammals']},
            FishingMethod.HANDLINE: {'risk': 'low', 'species': []},
            FishingMethod.TRAP: {'risk': 'low', 'species': []}
        }
        return risk_levels.get(method, {'risk': 'unknown', 'species': []})

class MarineBiodiversityMonitor:
    """Monitors marine biodiversity."""
    
    def __init__(self):
        self.surveys: List[Dict] = []
        self.species_detections: Dict[str, List[Dict]] = {}
    
    def conduct_survey(self, location: Dict[str, float],
                      survey_type: str) -> Dict[str, Any]:
        """Conduct biodiversity survey."""
        detected_species = []
        
        if survey_type == 'acoustic':
            detected_species = self._acoustic_survey()
        elif survey_type == 'visual':
            detected_species = self._visual_survey()
        elif survey_type == 'sampling':
            detected_species = self._sampling_survey()
        
        survey = {
            'survey_id': f"SRV_{len(self.surveys) + 1}",
            'location': location,
            'type': survey_type,
            'timestamp': datetime.now(),
            'species_count': len(detected_species),
            'species': detected_species,
            'biodiversity_index': self._calculate_diversity_index(detected_species)
        }
        
        self.surveys.append(survey)
        return survey
    
    def _acoustic_survey(self) -> List[Dict]:
        """Conduct acoustic survey."""
        return [
            {'species': 'Humpback Whale', 'detections': random.randint(5, 20)},
            {'species': 'Dolphin Sp.', 'detections': random.randint(10, 50)},
            {'species': 'Bluefin Tuna', 'detections': random.randint(3, 15)}
        ]
    
    def _visual_survey(self) -> List[Dict]:
        """Conduct visual survey."""
        return [
            {'species': 'Sea Turtle', 'count': random.randint(2, 8)},
            {'species': 'Manta Ray', 'count': random.randint(1, 5)},
            {'species': 'Shark Sp.', 'count': random.randint(1, 4)}
        ]
    
    def _sampling_survey(self) -> List[Dict]:
        """Conduct sampling survey."""
        return [
            {'species': 'Copepods', 'count_per_m3': random.randint(1000, 5000)},
            {'species': 'Larval Fish', 'count': random.randint(50, 200)},
            {'species': 'Zooplankton', 'biomass_g': random.uniform(10, 50)}
        ]
    
    def _calculate_diversity_index(self, species: List[Dict]) -> float:
        """Calculate biodiversity index."""
        if not species:
            return 0
        return round(random.uniform(1.5, 3.5), 2)
    
    def assess_reef_health(self, reef_id: str) -> Dict[str, Any]:
        """Assess coral reef health."""
        coral_cover = random.uniform(20, 60)
        species_diversity = random.uniform(1.5, 3.0)
        bleaching_index = random.uniform(0, 0.3)
        
        health_score = coral_cover * 0.4 + species_diversity * 20 - bleaching_index * 30
        
        return {
            'reef_id': reef_id,
            'coral_cover_percent': round(coral_cover, 1),
            'species_diversity': round(species_diversity, 2),
            'bleaching_index': round(bleaching_index, 2),
            'health_score': max(0, min(100, round(health_score, 1))),
            'status': 'excellent' if health_score >= 80 else 'good' if health_score >= 60 else 'poor' if health_score >= 40 else 'critical',
            'threats': ['Climate change', 'Pollution', 'Overfishing'] if bleaching_index > 0.2 else []
        }

class OceanEnergyManager:
    """Manages ocean renewable energy systems."""
    
    def __init__(self):
        self.energy_systems: Dict[str, Dict] = {}
    
    def assess_wave_energy_potential(self, location: Dict[str, float]) -> Dict[str, Any]:
        """Assess wave energy potential."""
        wave_height = random.uniform(1, 4)
        wave_period = random.uniform(6, 14)
        
        power_density = 0.5 * 1025 * 9.81 * (wave_height ** 2) * wave_period
        
        return {
            'location': location,
            'wave_height_m': round(wave_height, 2),
            'wave_period_s': round(wave_period, 1),
            'power_density_kW/m': round(power_density / 1000, 2),
            'capacity_factor': round(random.uniform(0.25, 0.45), 2),
            'annual_energy_MWh': round(power_density * 8760 * 0.35 / 1000, 0),
            'suitability': 'excellent' if power_density > 50 else 'good' if power_density > 30 else 'moderate'
        }
    
    def assess_tidal_energy(self, location: Dict[str, float]) -> Dict[str, Any]:
        """Assess tidal energy potential."""
        tidal_range = random.uniform(2, 10)
        tidal_velocity = random.uniform(1, 3)
        
        return {
            'location': location,
            'tidal_range_m': round(tidal_range, 2),
            'tidal_velocity_m/s': round(tidal_velocity, 2),
            'energy_potential_MWh/year': round(tidal_range * tidal_velocity * 500, 0),
            'number_of_tidal_cycles': 2,
            'suitability': 'excellent' if tidal_range > 5 else 'good'
        }

class OceanTechAgent:
    """Main OceanTech agent."""
    
    def __init__(self):
        self.sensor_network = OceanSensorNetwork()
        self.stock_manager = FishStockManager()
        self.fisheries = FisheriesOptimizer()
        self.biodiversity = MarineBiodiversityMonitor()
        self.energy = OceanEnergyManager()
    
    def assess_marine_environment(self, location: Dict[str, float]) -> Dict[str, Any]:
        """Comprehensive marine environment assessment."""
        buoy_id = "BUOY_001"
        self.sensor_network.deploy_buoy(buoy_id, location, 100)
        
        water_data = self.sensor_network.collect_data(buoy_id)
        water_quality = self.sensor_network.analyze_water_quality(water_data)
        
        survey = self.biodiversity.conduct_survey(location, 'visual')
        
        wave_potential = self.energy.assess_wave_energy_potential(location)
        
        return {
            'location': location,
            'water_quality': water_quality,
            'biodiversity': {
                'species_count': survey['species_count'],
                'diversity_index': survey['biodiversity_index'],
                'species': survey['species']
            },
            'energy_potential': wave_potential,
            'recommendations': [
                "Deploy additional sensors for comprehensive monitoring",
                "Establish marine protected area nearby",
                "Consider wave energy installation"
            ]
        }
    
    def get_ocean_dashboard(self) -> Dict[str, Any]:
        """Get ocean technology dashboard."""
        return {
            'sensors': {
                'active_buoys': len(self.sensor_network.buoys),
                'data_points': len(self.sensor_network.data_stream)
            },
            'fisheries': {
                'stocks_assessed': len(self.stock_manager.stocks),
                'active_operations': len(self.fisheries.operations)
            },
            'biodiversity': {
                'surveys_completed': len(self.biodiversity.surveys),
                'species_tracked': len(self.biodiversity.species_detections)
            },
            'energy': {
                'systems_monitored': len(self.energy.energy_systems)
            }
        }

def main():
    """Main entry point."""
    agent = OceanTechAgent()
    
    result = agent.assess_marine_environment({'lat': 25.0, 'lon': -45.0})
    print(f"Marine assessment: {result}")

if __name__ == "__main__":
    main()

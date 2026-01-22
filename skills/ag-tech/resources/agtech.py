#!/usr/bin/env python3
"""
AgTech - Agricultural Technology Implementation
Smart farming, precision agriculture, and sustainable food production.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json
import random

class CropType(Enum):
    WHEAT = "wheat"
    CORN = "corn"
    SOYBEAN = "soybean"
    RICE = "rice"
    VEGETABLES = "vegetables"
    FRUITS = "fruits"

class IrrigationType(Enum):
    DRIP = "drip"
    SPRINKLER = "sprinkler"
    FLOOD = "flood"
    SUBSURFACE = "subsurface"

class GrowthStage(Enum):
    GERMINATION = "germination"
    SEEDLING = "seedling"
    VEGETATIVE = "vegetative"
    FLOWERING = "flowering"
    MATURATION = "maturation"
    HARVEST = "harvest"

@dataclass
class Field:
    id: str
    name: str
    area_hectares: float
    soil_type: str
    crop: CropType
    irrigation: IrrigationType
    sensors: List[str]

@dataclass
class CropData:
    field_id: str
    growth_stage: GrowthStage
    health_score: float
    moisture_level: float
    nutrient_levels: Dict[str, float]
    pest_risk: float
    disease_risk: float
    timestamp: datetime

@dataclass
class YieldPrediction:
    field_id: str
    predicted_yield: float
    confidence: float
    factors: Dict[str, float]
    recommendation: str

class SoilAnalyzer:
    """Analyzes soil conditions."""
    
    def __init__(self):
        self.soil_profiles: Dict[str, Dict] = {}
    
    def analyze_soil(self, field_id: str, samples: Dict[str, float]) -> Dict[str, Any]:
        """Analyze soil sample data."""
        ph = samples.get('ph', 7.0)
        nitrogen = samples.get('nitrogen', 50)
        phosphorus = samples.get('phosphorus', 30)
        potassium = samples.get('potassium', 200)
        organic_matter = samples.get('organic_matter', 2.0)
        
        quality_score = 0
        recommendations = []
        
        if 6.0 <= ph <= 7.5:
            quality_score += 25
        else:
            recommendations.append(f"Adjust soil pH from {ph} to 6.5-7.0")
            quality_score += 10
        
        if nitrogen >= 50:
            quality_score += 20
        else:
            recommendations.append("Add nitrogen fertilizer")
        
        if phosphorus >= 30:
            quality_score += 20
        else:
            recommendations.append("Add phosphorus fertilizer")
        
        if potassium >= 200:
            quality_score += 20
        else:
            recommendations.append("Add potassium fertilizer")
        
        if organic_matter >= 3.0:
            quality_score += 15
        else:
            recommendations.append("Increase organic matter content")
        
        return {
            'field_id': field_id,
            'ph': ph,
            'nutrients': {
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium
            },
            'organic_matter': organic_matter,
            'quality_score': min(100, quality_score),
            'recommendations': recommendations,
            'suitability': self._get_crop_suitability(samples)
        }
    
    def _get_crop_suitability(self, samples: Dict) -> Dict[str, str]:
        """Determine suitable crops for soil."""
        ph = samples.get('ph', 7.0)
        suitability = {}
        
        if 6.0 <= ph <= 7.0:
            suitability['wheat'] = 'excellent'
            suitability['corn'] = 'excellent'
            suitability['soybean'] = 'good'
        elif ph < 6.0:
            suitability['potatoes'] = 'excellent'
            suitability['wheat'] = 'good'
            suitability['corn'] = 'moderate'
        else:
            suitability['asparagus'] = 'excellent'
            suitability['beets'] = 'good'
        
        return suitability

class PrecisionIrrigation:
    """Manages precision irrigation systems."""
    
    def __init__(self):
        self.schedules: Dict[str, List[Dict]] = {}
        self.water_usage: List[Dict] = []
    
    def calculate_water_needs(self, field: Field, weather_data: Dict) -> float:
        """Calculate optimal water needs."""
        base_need = {
            CropType.WHEAT: 450,
            CropType.CORN: 500,
            CropType.SOYBEAN: 400,
            CropType.RICE: 800,
            CropType.VEGETABLES: 600,
            CropType.FRUITS: 550
        }
        
        evapotranspiration = weather_data.get('evapotranspiration', 5.0)
        precipitation = weather_data.get('precipitation', 0)
        temperature = weather_data.get('temperature', 25)
        
        crop_coefficient = base_need.get(field.crop, 500) / 500
        
        water_need = evapotranspiration * crop_coefficient
        
        if precipitation > 10:
            water_need = max(0, water_need - precipitation * 0.8)
        
        if temperature > 30:
            water_need *= 1.2
        elif temperature < 15:
            water_need *= 0.8
        
        return round(water_need, 2)
    
    def create_irrigation_schedule(self, field_id: str, 
                                   water_needs: float,
                                   irrigation_type: IrrigationType) -> Dict[str, Any]:
        """Generate irrigation schedule."""
        duration_per_session = {
            IrrigationType.DRIP: 90,
            IrrigationType.SPRINKLER: 60,
            IrrigationType.FLOOD: 120,
            IrrigationType.SUBSURFACE: 45
        }
        
        sessions_per_week = {
            IrrigationType.DRIP: 3,
            IrrigationType.SPRINKLER: 2,
            IrrigationType.FLOOD: 1,
            IrrigationType.SUBSURFACE: 4
        }
        
        duration = duration_per_session.get(irrigation_type, 60)
        frequency = sessions_per_week.get(irrigation_type, 2)
        
        schedule = {
            'field_id': field_id,
            'irrigation_type': irrigation_type.value,
            'sessions_per_week': frequency,
            'duration_minutes': duration,
            'total_weekly_water': round(water_needs * frequency * duration / 60, 2),
            'recommended_times': ['06:00', '18:00'],
            'smart_features': {
                'weather_adaptation': True,
                'soil_moisture_sensor': True,
                'auto_shutoff': True
            }
        }
        
        self.schedules[field_id] = [schedule]
        return schedule
    
    def optimize_water_usage(self, field_id: str, 
                            current_usage: float,
                            target_yield: float) -> Dict[str, Any]:
        """Optimize water usage for yield target."""
        water_per_unit_yield = 1000
        
        optimal_water = water_per_unit_yield * target_yield * 0.85
        
        savings = current_usage - optimal_water
        savings_percent = (savings / current_usage * 100) if current_usage > 0 else 0
        
        return {
            'current_usage': current_usage,
            'optimal_usage': optimal_water,
            'potential_savings': round(savings, 2),
            'savings_percent': round(savings_percent, 1),
            'recommendations': [
                "Install soil moisture sensors",
                "Use drip irrigation for row crops",
                "Schedule irrigation during cool hours",
                "Implement rainwater harvesting"
            ]
        }

class CropMonitor:
    """Monitors crop health and growth."""
    
    def __init__(self):
        self.crop_data: Dict[str, CropData] = {}
        self.alerts: List[Dict] = []
    
    def collect_crop_data(self, field: Field) -> CropData:
        """Collect crop monitoring data."""
        data = CropData(
            field_id=field.id,
            growth_stage=self._estimate_growth_stage(field),
            health_score=random.uniform(70, 98),
            moisture_level=random.uniform(40, 80),
            nutrient_levels={
                'nitrogen': random.uniform(40, 80),
                'phosphorus': random.uniform(25, 50),
                'potassium': random.uniform(150, 250)
            },
            pest_risk=random.uniform(5, 30),
            disease_risk=random.uniform(5, 25),
            timestamp=datetime.now()
        )
        
        self.crop_data[field.id] = data
        
        if data.health_score < 70:
            self._create_alert(field.id, 'low_health', 'Crop health below threshold')
        if data.pest_risk > 50:
            self._create_alert(field.id, 'high_pest_risk', 'Pest outbreak risk high')
        if data.disease_risk > 40:
            self._create_alert(field.id, 'high_disease_risk', 'Disease outbreak risk elevated')
        
        return data
    
    def _estimate_growth_stage(self, field: Field) -> GrowthStage:
        """Estimate crop growth stage."""
        stages = list(GrowthStage)
        return random.choice(stages)
    
    def _create_alert(self, field_id: str, alert_type: str, message: str):
        """Create crop alert."""
        self.alerts.append({
            'field_id': field_id,
            'type': alert_type,
            'message': message,
            'timestamp': datetime.now(),
            'severity': 'high' if 'high' in alert_type else 'medium'
        })
    
    def detect_diseases(self, image_data: bytes = None) -> Dict[str, Any]:
        """Detect crop diseases from image."""
        diseases = [
            ('powdery_mildew', 0.15, 'Use fungicide treatment'),
            ('rust', 0.12, 'Apply rust-resistant varieties'),
            ('blight', 0.08, 'Remove infected plants'),
            ('mosaic_virus', 0.05, 'Use virus-free seeds')
        ]
        
        detected = []
        for disease, probability, treatment in diseases:
            if random.random() < 0.3:
                detected.append({
                    'disease': disease,
                    'confidence': round(probability + random.uniform(0, 0.2), 2),
                    'treatment': treatment
                })
        
        return {
            'analyzed': True,
            'diseases_detected': detected,
            'healthy': len(detected) == 0,
            'recommendations': ['Monitor closely', 'Consult agricultural extension'] if not detected else []
        }

class YieldPredictor:
    """Predicts crop yields using ML-like analysis."""
    
    def __init__(self):
        self.predictions: List[YieldPrediction] = []
    
    def predict_yield(self, field: Field, historical_data: Dict,
                     current_conditions: Dict) -> YieldPrediction:
        """Predict crop yield for field."""
        base_yields = {
            CropType.WHEAT: 8.0,
            CropType.CORN: 11.0,
            CropType.SOYBEAN: 3.5,
            CropType.RICE: 7.5,
            CropType.VEGETABLES: 45.0,
            CropType.FRUITS: 35.0
        }
        
        base_yield = base_yields.get(field.crop, 5.0)
        
        area_factor = field.area_hectares
        weather_factor = 1.0
        
        temp = current_conditions.get('temperature', 25)
        if 20 <= temp <= 30:
            weather_factor *= 1.1
        elif temp < 15 or temp > 35:
            weather_factor *= 0.7
        
        precipitation = current_conditions.get('precipitation', 50)
        if 40 <= precipitation <= 80:
            weather_factor *= 1.05
        else:
            weather_factor *= 0.9
        
        soil_health = current_conditions.get('soil_health', 0.8)
        pest_impact = current_conditions.get('pest_damage', 0.1)
        
        predicted_yield = base_yield * area_factor * weather_factor * soil_health * (1 - pest_impact)
        
        confidence = 0.85 - abs(1 - weather_factor) * 0.2 - abs(0.8 - soil_health) * 0.1
        
        prediction = YieldPrediction(
            field_id=field.id,
            predicted_yield=round(predicted_yield, 2),
            confidence=round(max(0.5, min(0.95, confidence)), 2),
            factors={
                'base_yield': base_yield,
                'area': field.area_hectares,
                'weather_impact': weather_factor,
                'soil_health': soil_health,
                'pest_impact': pest_impact
            },
            recommendation=self._get_recommendation(weather_factor, soil_health)
        )
        
        self.predictions.append(prediction)
        return prediction
    
    def _get_recommendation(self, weather_factor: float, 
                           soil_health: float) -> str:
        """Get yield improvement recommendation."""
        if weather_factor < 0.9:
            return "Consider irrigation and heat-tolerant varieties"
        elif soil_health < 0.7:
            return "Focus on soil improvement before next planting"
        elif weather_factor > 1.0 and soil_health > 0.85:
            return "Excellent conditions - maintain current practices"
        else:
            return "Monitor conditions and adjust inputs as needed"

class DroneManager:
    """Manages agricultural drone operations."""
    
    def __init__(self):
        self.missions: List[Dict] = []
        self.imagery: List[Dict] = []
    
    def plan_mission(self, field_id: str, mission_type: str,
                    area_coordinates: List[Dict]) -> Dict[str, Any]:
        """Plan drone mission."""
        mission = {
            'mission_id': f"MISSION_{len(self.missions) + 1}",
            'field_id': field_id,
            'type': mission_type,
            'altitude': 50,
            'speed': 10,
            'coverage_area': self._calculate_area(area_coordinates),
            'flight_time': 25,
            'battery_required': 60,
            'waypoints': len(area_coordinates),
            'camera_type': 'multispectral' if mission_type == 'survey' else 'rgb',
            'output': {
                'images': 200 if mission_type == 'survey' else 50,
                'resolution': '2cm/pixel'
            }
        }
        
        self.missions.append(mission)
        return mission
    
    def _calculate_area(self, coordinates: List[Dict]) -> float:
        """Calculate coverage area in hectares."""
        return len(coordinates) * 0.5
    
    def analyze_imagery(self, image_data: bytes) -> Dict[str, Any]:
        """Analyze drone imagery."""
        ndvi_values = [random.uniform(0.3, 0.9) for _ in range(100)]
        
        healthy = sum(1 for v in ndvi_values if v >= 0.6)
        stressed = sum(1 for v in ndvi_values if 0.3 <= v < 0.6)
        problematic = sum(1 for v in ndvi_values if v < 0.3)
        
        return {
            'total_pixels': len(ndvi_values),
            'ndvi_mean': round(sum(ndvi_values) / len(ndvi_values), 3),
            'ndvi_range': [min(ndvi_values), max(ndvi_values)],
            'classification': {
                'healthy_percent': round(healthy / len(ndvi_values) * 100, 1),
                'stressed_percent': round(stressed / len(ndvi_values) * 100, 1),
                'problematic_percent': round(problematic / len(ndvi_values) * 100, 1)
            },
            'recommendations': [
                "Focus irrigation on stressed areas",
                "Apply targeted fertilizer to problematic zones",
                "Schedule follow-up survey in 7 days"
            ]
        }

class AgTechAgent:
    """Main AgTech agent for agricultural operations."""
    
    def __init__(self):
        self.soil_analyzer = SoilAnalyzer()
        self.irrigation = PrecisionIrrigation()
        self.crop_monitor = CropMonitor()
        self.yield_predictor = YieldPredictor()
        self.drone_manager = DroneManager()
    
    def analyze_field(self, field: Field, 
                     soil_samples: Dict,
                     weather_data: Dict) -> Dict[str, Any]:
        """Comprehensive field analysis."""
        soil_analysis = self.soil_analyzer.analyze_soil(field.id, soil_samples)
        water_needs = self.irrigation.calculate_water_needs(field, weather_data)
        irrigation = self.irrigation.create_irrigation_schedule(
            field.id, water_needs, field.irrigation
        )
        crop_data = self.crop_monitor.collect_crop_data(field)
        yield_pred = self.yield_predictor.predict_yield(
            field, {}, weather_data
        )
        
        return {
            'field': {
                'id': field.id,
                'name': field.name,
                'crop': field.crop.value,
                'area': field.area_hectares
            },
            'soil_analysis': soil_analysis,
            'irrigation': irrigation,
            'crop_health': {
                'stage': crop_data.growth_stage.value,
                'health_score': crop_data.health_score,
                'moisture': crop_data.moisture_level,
                'pest_risk': crop_data.pest_risk,
                'disease_risk': crop_data.disease_risk
            },
            'yield_prediction': {
                'predicted': yield_pred.predicted_yield,
                'confidence': yield            },
            '_pred.confidence
alerts': self.crop_monitor.alerts
        }
    
    def get_farm_dashboard(self) -> Dict[str, Any]:
        """Get farm management dashboard."""
        return {
            'fields': {
                'total': 0,
                'healthy': 0,
                'attention_needed': 0
            },
            'water': {
                'daily_usage': 0,
                'efficiency': 0,
                'savings_potential': 0
            },
            'crops': {
                'planted': 0,
                'harvest_ready': 0,
                'in_growth': 0
            },
            'alerts': {
                'critical': len([a for a in self.crop_monitor.alerts if a['severity'] == 'high']),
                'warnings': len([a for a in self.crop_monitor.alerts if a['severity'] == 'medium'])
            },
            'recommendations': [
                "Check irrigation system in Field 3",
                "Apply fungicide to Sector B",
                "Schedule drone survey for Week 42"
            ]
        }

def main():
    """Main entry point."""
    agent = AgTechAgent()
    
    field = Field(
        id="F001",
        name="North Field",
        area_hectares=50,
        soil_type="Loam",
        crop=CropType.CORN,
        irrigation=IrrigationType.DRIP,
        sensors=["moisture", "temp", "nutrients"]
    )
    
    result = agent.analyze_field(
        field,
        {'ph': 6.5, 'nitrogen': 55, 'phosphorus': 35, 'potassium': 220, 'organic_matter': 3.5},
        {'temperature': 27, 'precipitation': 60, 'evapotranspiration': 5.5}
    )
    
    print(f"Field analysis: {result}")

if __name__ == "__main__":
    main()

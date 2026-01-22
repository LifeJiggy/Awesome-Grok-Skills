#!/usr/bin/env python3
"""
FoodTech - Food Technology Implementation
Food production, safety, and nutrition technology.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json
import random

class FoodCategory(Enum):
    PRODUCE = "produce"
    DAIRY = "dairy"
    MEAT = "meat"
    SEAFOOD = "seafood"
    GRAINS = "grains"
    PROCESSED = "processed"
    BEVERAGES = "beverages"

class ProteinType(Enum):
    PLANT_BASED = "plant_based"
    CULTURED = "cultured"
    ANIMAL = "animal"
    INSECT = "insect"
    FERMENTED = "fermented"

class SafetyStatus(Enum):
    SAFE = "safe"
    WARNING = "warning"
    RECALL = "recall"
    CONTAMINATED = "contaminated"

@dataclass
class FoodProduct:
    id: str
    name: str
    category: FoodCategory
    ingredients: List[str]
    allergens: List[str]
    nutrition_facts: Dict[str, float]
    shelf_life_days: int
    storage_requirements: Dict[str, float]

@dataclass
class SupplyChainEvent:
    id: str
    product_id: str
    event_type: str
    location: Dict[str, float]
    timestamp: datetime
    temperature: float
    handler: str

@dataclass
class LabResult:
    id: str
    product_id: str
    test_type: str
    result: str
    value: float
    limit: float
    status: str

class FoodSafetySystem:
    """Manages food safety and compliance."""
    
    def __init__(self):
        self.products: Dict[str, FoodProduct] = {}
        self.traceability: List[SupplyChainEvent] = []
        self.recalls: List[Dict] = []
    
    def register_product(self, name: str, category: FoodCategory,
                        ingredients: List[str], allergens: List[str],
                        shelf_life: int) -> FoodProduct:
        """Register new food product."""
        product = FoodProduct(
            id=f"FP_{len(self.products) + 1}",
            name=name,
            category=category,
            ingredients=ingredients,
            allergens=allergens,
            nutrition_facts={
                'calories': random.uniform(50, 500),
                'protein': random.uniform(1, 30),
                'carbs': random.uniform(5, 60),
                'fat': random.uniform(1, 25),
                'fiber': random.uniform(0, 10)
            },
            shelf_life_days=shelf_life,
            storage_requirements={'temperature': 4.0, 'humidity': 60}
        )
        self.products[product.id] = product
        return product
    
    def check_safety(self, product_id: str, 
                    current_temp: float) -> Dict[str, Any]:
        """Check food safety status."""
        product = self.products.get(product_id)
        if not product:
            return {'error': 'Product not found'}
        
        temp_threshold = product.storage_requirements['temperature']
        status = SafetyStatus.SAFE
        
        if current_temp > temp_threshold + 5:
            status = SafetyStatus.WARNING
            message = 'Temperature above recommended threshold'
        elif current_temp > temp_threshold + 10:
            status = SafetyStatus.CONTAMINATED
            message = 'Temperature abuse - potential contamination'
        else:
            message = 'Within safe temperature range'
        
        return {
            'product_id': product_id,
            'product_name': product.name,
            'current_temperature': current_temp,
            'safe_limit': temp_threshold,
            'status': status.value,
            'message': message,
            'remaining_shelf_life': random.randint(1, product.shelf_life_days)
        }
    
    def trace_product(self, product_id: str) -> Dict[str, Any]:
        """Trace product through supply chain."""
        events = [e for e in self.traceability if e.product_id == product_id]
        
        if not events:
            return {'product_id': product_id, 'events': [], 'origin_unknown': True}
        
        origin = events[0] if events else None
        destination = events[-1] if events else None
        
        chain_of_custody = []
        for event in events:
            chain_of_custody.append({
                'event': event.event_type,
                'location': event.location,
                'timestamp': event.timestamp.isoformat(),
                'handler': event.handler
            })
        
        return {
            'product_id': product_id,
            'origin': {
                'location': origin.location if origin else None,
                'timestamp': origin.timestamp.isoformat() if origin else None
            },
            'destination': {
                'location': destination.location if destination else None,
                'timestamp': destination.timestamp.isoformat() if destination else None
            },
            'chain_of_custody': chain_of_custody,
            'total_handlings': len(events)
        }
    
    def conduct_lab_test(self, product_id: str, 
                        test_type: str) -> LabResult:
        """Conduct safety lab test."""
        value = random.uniform(0, 100)
        limits = {'microbiological': 100, 'chemical': 50, 'physical': 10}
        limit = limits.get(test_type, 50)
        
        status = 'pass' if value < limit else 'fail'
        
        result = LabResult(
            id=f"LR_{random.randint(1000, 9999)}",
            product_id=product_id,
            test_type=test_type,
            result=status,
            value=round(value, 2),
            limit=limit,
            status=status
        )
        
        if status == 'fail':
            self._trigger_recall_check(product_id)
        
        return result
    
    def _trigger_recall_check(self, product_id: str):
        """Trigger recall check for failed test."""
        self.recalls.append({
            'product_id': product_id,
            'reason': 'Failed safety test',
            'status': 'under_review',
            'timestamp': datetime.now()
        })

class AlternativeProteinEngine:
    """Develops alternative protein solutions."""
    
    def __init__(self):
        self.products: Dict[str, Dict] = {}
    
    def develop_plant_based(self, target_texture: str,
                           protein_source: str) -> Dict[str, Any]:
        """Develop plant-based protein product."""
        protein_content = random.uniform(15, 30)
        cost_per_serving = random.uniform(2, 5)
        
        texture_map = {
            'ground': {'method': 'extrusion', 'cooking': 'medium'},
            'whole': {'method': '3D_printing', 'cooking': 'high'},
            'shredded': {'method': 'fermentation', 'cooking': 'low'}
        }
        
        return {
            'product_type': 'plant_based',
            'protein_source': protein_source,
            'target_texture': target_texture,
            'production_method': texture_map.get(target_texture, {}).get('method', 'standard'),
            'protein_content_percent': round(protein_content, 1),
            'cost_per_serving': round(cost_per_serving, 2),
            'development_timeline_months': random.randint(6, 18),
            'regulatory_status': 'approved' if protein_source in ['soy', 'pea', 'wheat'] else 'pending'
        }
    
    def develop_cultured_meat(self, animal_type: str,
                             cell_type: str) -> Dict[str, Any]:
        """Develop cultured meat product."""
        return {
            'product_type': 'cultured',
            'source_animal': animal_type,
            'cell_type': cell_type,
            'growth_medium': 'serum-free',
            'scaffold_material': 'plant-based',
            'production_scale': 'pilot',
            'cost_per_kg': round(random.uniform(50, 200), 2),
            'timeline_to_market': f"{random.randint(2, 5)} years",
            'challenges': [
                'Scale-up production',
                'Cost reduction',
                'Regulatory approval',
                'Consumer acceptance'
            ]
        }

class NutritionAnalyzer:
    """Analyzes and optimizes nutrition."""
    
    def __init__(self):
        self.profiles: Dict[str, Dict] = {}
    
    def analyze_recipe(self, ingredients: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze nutritional content of recipe."""
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        allergens_present = set()
        
        for ingredient in ingredients:
            amount = ingredient.get('amount', 100)
            total_calories += ingredient.get('calories', 100) * amount / 100
            total_protein += ingredient.get('protein', 5) * amount / 100
            total_carbs += ingredient.get('carbs', 10) * amount / 100
            total_fat += ingredient.get('fat', 5) * amount / 100
            allergens_present.update(ingredient.get('allergens', []))
        
        return {
            'serving_size': '1 portion',
            'nutrition_per_serving': {
                'calories': round(total_calories, 0),
                'protein_g': round(total_protein, 1),
                'carbohydrates_g': round(total_carbs, 1),
                'fat_g': round(total_fat, 1),
                'fiber_g': round(random.uniform(2, 10), 1),
                'sodium_mg': round(random.uniform(100, 800), 0)
            },
            'allergens': list(allergens_present),
            'dietary_tags': self._get_dietary_tags(ingredients),
            'health_score': self._calculate_health_score(total_calories, total_protein, total_carbs, total_fat)
        }
    
    def _get_dietary_tags(self, ingredients: List[Dict]) -> List[str]:
        """Get dietary classification tags."""
        tags = []
        
        dairy_present = any(i.get('category') == 'dairy' for i in ingredients)
        meat_present = any(i.get('category') == 'meat' for i in ingredients)
        
        if not dairy_present and not meat_present:
            tags.append('vegetarian')
        if not meat_present:
            tags.append('pescatarian')
        
        tags.append('high_protein' if sum(i.get('protein', 0) for i in ingredients) > 20 else 'balanced')
        
        return tags
    
    def _calculate_health_score(self, calories: float, protein: float,
                               carbs: float, fat: float) -> int:
        """Calculate health score (0-100)."""
        score = 70
        
        if 300 <= calories <= 600:
            score += 10
        if protein > 20:
            score += 5
        if carbs < 50:
            score += 5
        if fat < 20:
            score += 5
        if random.random() > 0.5:
            score += 5
        
        return min(100, max(0, int(score)))

class KitchenAutomation:
    """Manages kitchen automation systems."""
    
    def __init__(self):
        self.kitchens: Dict[str, Dict] = {}
        self.recipes: Dict[str, Dict] = {}
    
    def optimize_kitchen(self, kitchen_id: str) -> Dict[str, Any]:
        """Optimize kitchen operations."""
        return {
            'kitchen_id': kitchen_id,
            'efficiency_score': round(random.uniform(70, 95), 1),
            'equipment_utilization': {
                'ovens': round(random.uniform(60, 90), 1),
                'stoves': round(random.uniform(50, 85), 1),
                'refrigeration': round(random.uniform(70, 95), 1)
            },
            'improvements': [
                'Adjust prep station layout for flow',
                'Implement batch cooking for popular items',
                'Optimize equipment scheduling'
            ],
            'waste_reduction': {
                'current_waste_percent': round(random.uniform(5, 15), 1),
                'potential_reduction': round(random.uniform(2, 5), 1),
                'annual_savings': round(random.uniform(5000, 20000), 0)
            }
        }
    
    def manage_inventory(self, kitchen_id: str) -> Dict[str, Any]:
        """Manage kitchen inventory."""
        return {
            'kitchen_id': kitchen_id,
            'items_tracked': random.randint(50, 200),
            'stock_levels': {
                'adequate': random.randint(40, 80),
                'low': random.randint(5, 15),
                'overstocked': random.randint(5, 10)
            },
            'expiring_soon': [
                {'item': 'Fresh basil', 'quantity': '2 lbs', 'days_left': 2},
                {'item': 'Heavy cream', 'quantity': '1 gallon', 'days_left': 3}
            ],
            'reorder_recommendations': [
                {'item': 'Chicken breast', 'quantity': '20 lbs', 'priority': 'high'},
                {'item': 'Olive oil', 'quantity': '2 gallons', 'priority': 'medium'}
            ],
            'waste_tracking': {
                'weekly_waste_cost': round(random.uniform(100, 500), 2),
                'top_waste_items': ['Produce', 'Dairy', 'Bakery']
            }
        }

class FoodTechAgent:
    """Main FoodTech agent."""
    
    def __init__(self):
        self.safety = FoodSafetySystem()
        self.proteins = AlternativeProteinEngine()
        self.nutrition = NutritionAnalyzer()
        self.kitchen = KitchenAutomation()
    
    def assess_food_product(self, product_id: str,
                           current_temp: float) -> Dict[str, Any]:
        """Comprehensive food product assessment."""
        safety_check = self.safety.check_safety(product_id, current_temp)
        traceability = self.safety.trace_product(product_id)
        
        return {
            'safety': safety_check,
            'traceability': traceability,
            'recommendations': [
                'Ensure cold chain integrity',
                'Update labeling with allergen information',
                'Optimize inventory rotation'
            ]
        }
    
    def get_food_dashboard(self) -> Dict[str, Any]:
        """Get food technology dashboard."""
        return {
            'safety': {
                'products_registered': len(self.safety.products),
                'traceability_events': len(self.safety.traceability),
                'active_recalls': len(self.safety.recalls),
                'compliance_rate': round(random.uniform(95, 100), 1)
            },
            'innovation': {
                'alternative_protein_products': len(self.proteins.products),
                'lab_tests_completed': random.randint(50, 200)
            },
            'operations': {
                'kitchens_optimized': len(self.kitchen.kitchens),
                'waste_reduction_percent': round(random.uniform(10, 30), 1),
                'efficiency_improvement': round(random.uniform(5, 20), 1)
            },
            'nutrition': {
                'recipes_analyzed': len(self.kitchen.recipes)
            }
        }

def main():
    """Main entry point."""
    agent = FoodTechAgent()
    
    product = agent.safety.register_product(
        'Plant Burger',
        FoodCategory.PROCESSED,
        ['pea_protein', 'coconut_oil', 'potato_starch'],
        ['soy'],
        180
    )
    
    result = agent.assess_food_product(product.id, 3.5)
    print(f"Product assessment: {result}")

if __name__ == "__main__":
    main()

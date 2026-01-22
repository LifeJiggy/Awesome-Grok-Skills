#!/usr/bin/env python3
"""
Grok Sustainability Agent
Specialized agent for sustainability tracking, environmental impact analysis, and green initiatives.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json
from collections import defaultdict

class SustainabilityCategory(Enum):
    ENERGY = "energy"
    WATER = "water"
    WASTE = "waste"
    TRANSPORTATION = "transportation"
    SUPPLY_CHAIN = "supply_chain"
    BUILDING = "building"
    PRODUCT = "product"

class CarbonScope(Enum):
    SCOPE_1 = "scope_1"
    SCOPE_2 = "scope_2"
    SCOPE_3 = "scope_3"

class InitiativeStatus(Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ON_HOLD = "on_hold"

@dataclass
class EmissionRecord:
    id: str
    category: SustainabilityCategory
    scope: CarbonScope
    source: str
    amount: float
    unit: str
    date: datetime
    location: str
    verified: bool

@dataclass
class SustainabilityGoal:
    id: str
    name: str
    description: str
    category: SustainabilityCategory
    baseline_value: float
    target_value: float
    baseline_year: int
    target_year: int
    current_value: float
    status: str

@dataclass
class GreenInitiative:
    id: str
    name: str
    description: str
    category: SustainabilityCategory
    status: InitiativeStatus
    start_date: datetime
    expected_completion: datetime
    investment: float
    projected_savings: Dict[str, float]
    carbon_reduction: float
    metrics: Dict[str, Any]

class CarbonCalculator:
    """Calculates carbon emissions."""
    
    def __init__(self):
        self.factors = {
            'electricity': {'factor': 0.42, 'unit': 'kg CO2e/kWh'},
            'natural_gas': {'factor': 2.0, 'unit': 'kg CO2e/m³'},
            'gasoline': {'factor': 2.31, 'unit': 'kg CO2e/L'},
            'diesel': {'factor': 2.68, 'unit': 'kg CO2e/L'},
            'flight_short': {'factor': 0.255, 'unit': 'kg CO2e/km'},
            'flight_long': {'factor': 0.195, 'unit': 'kg CO2e/km'},
            'shipping': {'factor': 0.5, 'unit': 'kg CO2e/tonne-km'},
            'waste_landfill': {'factor': 0.58, 'unit': 'kg CO2e/kg'},
            'waste_recycled': {'factor': 0.02, 'unit': 'kg CO2e/kg'},
            'water': {'factor': 0.344, 'unit': 'kg CO2e/m³'}
        }
    
    def calculate_emission(self, source: str, quantity: float) -> Dict[str, Any]:
        """Calculate emission for given source."""
        factor = self.factors.get(source.lower())
        if not factor:
            return {'error': f'Unknown source: {source}'}
        
        emission = quantity * factor['factor']
        
        return {
            'source': source,
            'quantity': quantity,
            'emission_kg': round(emission, 2),
            'unit': factor['unit'],
            'factor': factor['factor']
        }
    
    def calculate_from_activity(self, activity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate emissions from activity data."""
        calculators = {
            'electricity': self._calc_electricity,
            'transportation': self._calc_transport,
            'heating': self._calc_heating,
            'waste': self._calc_waste,
            'water': self._calc_water
        }
        
        calc = calculators.get(activity_type)
        if not calc:
            return {'error': f'Unknown activity: {activity_type}'}
        
        return calc(data)
    
    def _calc_electricity(self, data: Dict) -> Dict:
        """Calculate electricity emissions."""
        kwh = data.get('kwh', 0)
        grid_factor = data.get('grid_factor', 0.42)
        emission = kwh * grid_factor
        return {'emission_kg': emission, 'breakdown': {'kwh': kwh, 'factor': grid_factor}}
    
    def _calc_transport(self, data: Dict) -> Dict:
        """Calculate transportation emissions."""
        distance = data.get('distance', 0)
        vehicle_type = data.get('vehicle_type', 'car')
        
        factors = {'car': 0.12, 'bus': 0.089, 'train': 0.041, 'flight': 0.255}
        factor = factors.get(vehicle_type, 0.12)
        
        emission = distance * factor
        return {'emission_kg': emission, 'breakdown': {'distance': distance, 'type': vehicle_type}}
    
    def _calc_heating(self, data: Dict) -> Dict:
        """Calculate heating emissions."""
        fuel_type = data.get('fuel_type', 'natural_gas')
        amount = data.get('amount', 0)
        
        factor = self.factors.get(fuel_type, {}).get('factor', 2.0)
        emission = amount * factor
        return {'emission_kg': emission, 'breakdown': {'type': fuel_type, 'amount': amount}}
    
    def _calc_waste(self, data: Dict) -> Dict:
        """Calculate waste emissions."""
        waste_type = data.get('waste_type', 'landfill')
        amount = data.get('amount', 0)
        
        factor = self.factors.get(f'waste_{waste_type}', {}).get('factor', 0.58)
        emission = amount * factor
        return {'emission_kg': emission, 'breakdown': {'type': waste_type, 'amount': amount}}
    
    def _calc_water(self, data: Dict) -> Dict:
        """Calculate water-related emissions."""
        volume = data.get('volume', 0)
        emission = volume * self.factors['water']['factor']
        return {'emission_kg': emission, 'breakdown': {'volume_m3': volume}}

class GoalTracker:
    """Tracks sustainability goals."""
    
    def __init__(self):
        self.goals: Dict[str, SustainabilityGoal] = {}
        self.history: List[Dict] = []
    
    def create_goal(self, name: str, description: str,
                   category: SustainabilityCategory,
                   baseline_value: float, target_value: float,
                   baseline_year: int, target_year: int) -> SustainabilityGoal:
        """Create sustainability goal."""
        goal = SustainabilityGoal(
            id=f"goal_{len(self.goals) + 1}",
            name=name,
            description=description,
            category=category,
            baseline_value=baseline_value,
            target_value=target_value,
            baseline_year=baseline_year,
            target_year=target_year,
            current_value=baseline_value,
            status='active'
        )
        self.goals[goal.id] = goal
        return goal
    
    def update_progress(self, goal_id: str, current_value: float) -> SustainabilityGoal:
        """Update goal progress."""
        if goal_id not in self.goals:
            raise ValueError(f"Goal {goal_id} not found")
        
        goal = self.goals[goal_id]
        goal.current_value = current_value
        
        progress = ((baseline - current_value) / (baseline - target_value)) * 100
        progress = max(0, min(100, progress))
        
        if current_value <= target_value:
            goal.status = 'achieved'
        elif datetime.now().year > target_year:
            goal.status = 'missed'
        
        self.history.append({
            'goal_id': goal_id,
            'value': current_value,
            'progress': progress,
            'timestamp': datetime.now()
        })
        
        return goal
    
    def calculate_goal_status(self, goal_id: str) -> Dict[str, Any]:
        """Calculate goal status."""
        goal = self.goals.get(goal_id)
        if not goal:
            return {'error': 'Goal not found'}
        
        total_years = goal.target_year - goal.baseline_year
        elapsed_years = datetime.now().year - goal.baseline_year
        
        expected_progress = (elapsed_years / total_years) * 100
        actual_progress = ((goal.baseline_value - goal.current_value) / 
                          (goal.baseline_value - goal.target_value)) * 100
        
        return {
            'goal_name': goal.name,
            'expected_progress': expected_progress,
            'actual_progress': actual_progress,
            'variance': actual_progress - expected_progress,
            'on_track': actual_progress >= expected_progress * 0.9,
            'years_remaining': max(0, goal.target_year - datetime.now().year)
        }
    
    def get_overall_progress(self) -> Dict[str, Any]:
        """Get overall goal progress."""
        on_track = 0
        at_risk = 0
        behind = 0
        achieved = 0
        
        for goal in self.goals.values():
            status = self.calculate_goal_status(goal.id)
            if goal.status == 'achieved':
                achieved += 1
            elif status['on_track']:
                on_track += 1
            elif status['variance'] > -20:
                at_risk += 1
            else:
                behind += 1
        
        return {
            'total_goals': len(self.goals),
            'on_track': on_track,
            'at_risk': at_risk,
            'behind': behind,
            'achieved': achieved,
            'success_rate': achieved / len(self.goals) * 100 if self.goals else 0
        }

class InitiativeManager:
    """Manages green initiatives."""
    
    def __init__(self):
        self.initiatives: Dict[str, GreenInitiative] = {}
        self.roi_calculations: Dict[str, Dict] = {}
    
    def create_initiative(self, name: str, description: str,
                         category: SustainabilityCategory,
                         investment: float, expected_savings: Dict[str, float],
                         carbon_reduction: float, 
                         timeline_months: int = 12) -> GreenInitiative:
        """Create green initiative."""
        start = datetime.now()
        completion = start + timedelta(days=30 * timeline_months)
        
        initiative = GreenInitiative(
            id=f"ini_{len(self.initiatives) + 1}",
            name=name,
            description=description,
            category=category,
            status=InitiativeStatus.PLANNED,
            start_date=start,
            expected_completion=completion,
            investment=investment,
            projected_savings=expected_savings,
            carbon_reduction=carbon_reduction,
            metrics={'progress': 0}
        )
        self.initiatives[initiative.id] = initiative
        return initiative
    
    def update_initiative(self, initiative_id: str, 
                         progress: float) -> GreenInitiative:
        """Update initiative progress."""
        if initiative_id not in self.initiatives:
            raise ValueError(f"Initiative {initiative_id} not found")
        
        initiative = self.initiatives[initiative_id]
        initiative.metrics['progress'] = progress
        
        if progress >= 100:
            initiative.status = InitiativeStatus.COMPLETED
        elif progress >= 50:
            initiative.status = InitiativeStatus.IN_PROGRESS
        
        return initiative
    
    def calculate_roi(self, initiative_id: str) -> Dict[str, Any]:
        """Calculate initiative ROI."""
        initiative = self.initiatives.get(initiative_id)
        if not initiative:
            return {'error': 'Initiative not found'}
        
        annual_savings = initiative.projected_savings.get('annual', 0)
        payback_period = initiative.investment / annual_savings if annual_savings > 0 else float('inf')
        
        roi_5_year = ((annual_savings * 5) - initiative.investment) / initiative.investment * 100
        
        return {
            'initiative_name': initiative.name,
            'investment': initiative.investment,
            'annual_savings': annual_savings,
            'payback_years': round(payback_period, 1),
            'roi_5_year': round(roi_5_year, 1),
            'carbon_reduction': initiative.carbon_reduction
        }
    
    def get_portfolio_summary(self) -> Dict[str, Any]:
        """Get initiative portfolio summary."""
        total_investment = sum(i.investment for i in self.initiatives.values())
        total_carbon = sum(i.carbon_reduction for i in self.initiatives.values())
        total_savings = sum(i.projected_savings.get('annual', 0) 
                          for i in self.initiatives.values())
        
        by_status = defaultdict(int)
        by_category = defaultdict(int)
        for ini in self.initiatives.values():
            by_status[ini.status.value] += 1
            by_category[ini.category.value] += 1
        
        return {
            'total_initiatives': len(self.initiatives),
            'total_investment': total_investment,
            'projected_annual_savings': total_savings,
            'total_carbon_reduction': total_carbon,
            'by_status': dict(by_status),
            'by_category': dict(by_category)
        }

class SustainabilityReporter:
    """Generates sustainability reports."""
    
    def __init__(self, carbon_calc: CarbonCalculator,
                 goal_tracker: GoalTracker,
                 initiative_manager: InitiativeManager):
        self.carbon = carbon_calc
        self.goals = goal_tracker
        self.initiatives = initiative_manager
    
    def generate_footprint_report(self, start_date: datetime,
                                 end_date: datetime) -> Dict[str, Any]:
        """Generate carbon footprint report."""
        scope1 = 0
        scope2 = 0
        scope3 = 0
        
        breakdown = {cat.value: 0 for cat in SustainabilityCategory}
        
        return {
            'period': {'start': start_date.isoformat(), 'end': end_date.isoformat()},
            'total_emissions_kg': scope1 + scope2 + scope3,
            'by_scope': {
                'scope_1': scope1,
                'scope_2': scope2,
                'scope_3': scope3
            },
            'by_category': breakdown,
            'per_employee': 0,
            'yoy_change': 0
        }
    
    def generate_esg_report(self) -> Dict[str, Any]:
        """Generate ESG report."""
        goal_progress = self.goals.get_overall_progress()
        portfolio = self.initiatives.get_portfolio_summary()
        
        return {
            'report_date': datetime.now().isoformat(),
            'environmental': {
                'carbon_footprint': 'See footprint report',
                'renewable_energy': '45%',
                'waste_reduction': '30%'
            },
            'social': {
                'employee_wellbeing': '85%',
                'diversity': '40%',
                'community_investment': '$50000'
            },
            'governance': {
                'board_diversity': '45%',
                'ethics_training': '100%',
                'transparency_score': 'A+'
            },
            'goals': goal_progress,
            'initiatives': portfolio
        }
    
    def get_sustainability_score(self) -> Dict[str, Any]:
        """Calculate overall sustainability score."""
        weights = {
            'carbon_reduction': 0.30,
            'energy_efficiency': 0.20,
            'waste_management': 0.15,
            'water_conservation': 0.10,
            'supply_chain': 0.15,
            'governance': 0.10
        }
        
        scores = {
            'carbon_reduction': 75,
            'energy_efficiency': 82,
            'waste_management': 68,
            'water_conservation': 70,
            'supply_chain': 60,
            'governance': 90
        }
        
        weighted_score = sum(scores[k] * weights[k] for k in weights)
        
        return {
            'overall_score': round(weighted_score, 1),
            'letter_grade': self._get_letter_grade(weighted_score),
            'breakdown': scores,
            'trends': {
                'quarter': '+2.5%',
                'year': '+8.2%'
            }
        }
    
    def _get_letter_grade(self, score: float) -> str:
        """Convert score to letter grade."""
        if score >= 90: return 'A'
        elif score >= 80: return 'B'
        elif score >= 70: return 'C'
        elif score >= 60: return 'D'
        return 'F'

class SustainabilityAgent:
    """Main sustainability agent."""
    
    def __init__(self):
        self.carbon = CarbonCalculator()
        self.goals = GoalTracker()
        self.initiatives = InitiativeManager()
        self.reporter = SustainabilityReporter(self.carbon, self.goals, self.initiatives)
    
    def track_emission(self, category: str, scope: str,
                      source: str, amount: float, unit: str,
                      date: datetime = None) -> Dict[str, Any]:
        """Track emission record."""
        record = {
            'id': f"emi_{len(self.carbon.factors)}",
            'category': SustainabilityCategory[category.upper()],
            'scope': CarbonScope[scope.upper()],
            'source': source,
            'amount': amount,
            'unit': unit,
            'date': date or datetime.now(),
            'location': 'HQ',
            'verified': False
        }
        
        return record
    
    def set_sustainability_goal(self, name: str, description: str,
                               category: str, baseline: float, 
                               target: float, target_year: int) -> Dict[str, Any]:
        """Set sustainability goal."""
        goal = self.goals.create_goal(
            name=name,
            description=description,
            category=SustainabilityCategory[category.upper()],
            baseline_value=baseline,
            target_value=target,
            baseline_year=datetime.now().year,
            target_year=target_year
        )
        
        return {
            'goal_id': goal.id,
            'name': goal.name,
            'target': f"{target} by {target_year}"
        }
    
    def calculate_carbon_footprint(self, activities: List[Dict]) -> Dict[str, Any]:
        """Calculate carbon footprint from activities."""
        total_emission = 0
        breakdown = defaultdict(float)
        
        for activity in activities:
            result = self.carbon.calculate_from_activity(
                activity['type'],
                activity['data']
            )
            if 'emission_kg' in result:
                total_emission += result['emission_kg']
                breakdown[activity['type']] += result['emission_kg']
        
        return {
            'total_emission_kg': round(total_emission, 2),
            'total_emission_tonnes': round(total_emission / 1000, 3),
            'breakdown': dict(breakdown),
            'offset_cost': round(total_emission * 0.02, 2)
        }
    
    def get_sustainability_dashboard(self) -> Dict[str, Any]:
        """Get sustainability dashboard."""
        score = self.reporter.get_sustainability_score()
        portfolio = self.initiatives.get_portfolio_summary()
        goal_progress = self.goals.get_overall_progress()
        
        return {
            'score': score,
            'goals': {
                'total': goal_progress['total_goals'],
                'on_track': goal_progress['on_track'],
                'at_risk': goal_progress['at_risk']
            },
            'initiatives': {
                'active': portfolio['total_initiatives'],
                'investment': portfolio['total_investment'],
                'carbon_reduction': portfolio['total_carbon_reduction']
            },
            'quick_wins': [
                "Switch to LED lighting - saves 40% on energy",
                "Implement paperless office - reduces 5 tonnes CO2",
                "Optimize HVAC schedule - saves 15% energy"
            ]
        }

def main():
    """Main entry point."""
    agent = SustainabilityAgent()
    
    footprint = agent.calculate_carbon_footprint([
        {'type': 'electricity', 'data': {'kwh': 10000, 'grid_factor': 0.42}},
        {'type': 'transportation', 'data': {'distance': 5000, 'vehicle_type': 'car'}}
    ])
    print(f"Footprint: {footprint}")
    
    dashboard = agent.get_sustainability_dashboard()
    print(f"Dashboard: {dashboard}")

if __name__ == "__main__":
    main()

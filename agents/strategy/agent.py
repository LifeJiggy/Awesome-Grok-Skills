#!/usr/bin/env python3
"""
Grok Strategy Agent
Specialized agent for strategic planning, business analysis, and decision making.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
from collections import defaultdict

class StrategicPriority(Enum):
    GROWTH = "growth"
    EFFICIENCY = "efficiency"
    INNOVATION = "innovation"
    MARKET = "market"
    TALENT = "talent"
    TECHNOLOGY = "technology"

class ObjectiveStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    AT_RISK = "at_risk"
    ON_TRACK = "on_track"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

@dataclass
class StrategicObjective:
    id: str
    title: str
    description: str
    priority: StrategicPriority
    status: ObjectiveStatus
    key_results: List[str]
    metrics: Dict[str, float]
    start_date: datetime
    target_date: datetime
    owner: str
    budget: float
    dependencies: List[str]

@dataclass
class Initiative:
    id: str
    objective_id: str
    name: str
    description: str
    status: str
    resources: Dict[str, Any]
    timeline: Dict[str, datetime]
    expected_impact: str
    risks: List[str]

@dataclass
class SWOTAnalysis:
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    score: Dict[str, int]

@dataclass
class StrategicMetrics:
    objective_completion: float
    initiative_progress: float
    budget_utilization: float
    risk_exposure: float
    overall_health: float

class StrategicPlanner:
    """Plans and manages strategic initiatives."""
    
    def __init__(self):
        self.objectives: Dict[str, StrategicObjective] = {}
        self.initiatives: Dict[str, Initiative] = {}
        self.milestones: List[Dict] = []
    
    def create_objective(self, title: str, description: str,
                        priority: StrategicPriority, key_results: List[str],
                        target_date: datetime, owner: str,
                        budget: float = 0.0) -> StrategicObjective:
        """Create strategic objective."""
        obj = StrategicObjective(
            id=f"obj_{len(self.objectives) + 1}",
            title=title,
            description=description,
            priority=priority,
            status=ObjectiveStatus.NOT_STARTED,
            key_results=key_results,
            metrics={},
            start_date=datetime.now(),
            target_date=target_date,
            owner=owner,
            budget=budget,
            dependencies=[]
        )
        self.objectives[obj.id] = obj
        return obj
    
    def add_initiative(self, objective_id: str, name: str,
                      description: str, resources: Dict[str, Any],
                      timeline: Dict[str, datetime], 
                      expected_impact: str,
                      risks: List[str] = None) -> Initiative:
        """Add initiative to objective."""
        initiative = Initiative(
            id=f"ini_{len(self.initiatives) + 1}",
            objective_id=objective_id,
            name=name,
            description=description,
            status="planned",
            resources=resources,
            timeline=timeline,
            expected_impact=expected_impact,
            risks=risks or []
        )
        self.initiatives[initiative.id] = initiative
        return initiative
    
    def update_progress(self, objective_id: str, 
                       progress: float) -> StrategicObjective:
        """Update objective progress."""
        if objective_id not in self.objectives:
            raise ValueError(f"Objective {objective_id} not found")
        
        obj = self.objectives[objective_id]
        obj.metrics['progress'] = progress
        
        if progress >= 100:
            obj.status = ObjectiveStatus.COMPLETED
        elif progress >= 75:
            obj.status = ObjectiveStatus.ON_TRACK
        elif progress >= 50:
            obj.status = ObjectiveStatus.IN_PROGRESS
        elif progress >= 25:
            obj.status = ObjectiveStatus.IN_PROGRESS
        else:
            obj.status = ObjectiveStatus.AT_RISK
        
        return obj
    
    def get_objectives_by_priority(self, priority: StrategicPriority) -> List[StrategicObjective]:
        """Get objectives by priority."""
        return [o for o in self.objectives.values() if o.priority == priority]
    
    def calculate_timeline_status(self, objective_id: str) -> Dict[str, Any]:
        """Calculate timeline status for objective."""
        obj = self.objectives.get(objective_id)
        if not obj:
            return {'error': 'Objective not found'}
        
        now = datetime.now()
        total_days = (obj.target_date - obj.start_date).days
        elapsed_days = (now - obj.start_date).days
        
        if total_days == 0:
            return {'status': 'unknown', 'progress': 0}
        
        expected_progress = (elapsed_days / total_days) * 100
        actual_progress = obj.metrics.get('progress', 0)
        
        variance = actual_progress - expected_progress
        
        return {
            'expected_progress': expected_progress,
            'actual_progress': actual_progress,
            'variance': variance,
            'status': 'ahead' if variance > 5 else 'behind' if variance < -5 else 'on_track'
        }

class SWOTAnalyzer:
    """Performs SWOT analysis."""
    
    def __init__(self):
        self.analyses: Dict[str, SWOTAnalysis] = {}
    
    def analyze(self, strengths: List[str], weaknesses: List[str],
               opportunities: List[str], threats: List[str],
               context: str = "general") -> SWOTAnalysis:
        """Perform SWOT analysis."""
        analysis = SWOTAnalysis(
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            threats=threats,
            score=self._calculate_swot_score(strengths, weaknesses, 
                                            opportunities, threats)
        )
        self.analyses[context] = analysis
        return analysis
    
    def _calculate_swot_score(self, strengths: List[str], 
                             weaknesses: List[str],
                             opportunities: List[str],
                             threats: List[str]) -> Dict[str, int]:
        """Calculate SWOT scores."""
        return {
            'strengths_score': min(len(strengths) * 10, 50),
            'weaknesses_score': max(50 - len(weaknesses) * 10, 10),
            'opportunities_score': min(len(opportunities) * 10, 50),
            'threats_score': max(50 - len(threats) * 10, 10)
        }
    
    def generate_strategies(self, swot: SWOTAnalysis) -> Dict[str, List[str]]:
        """Generate strategies from SWOT analysis."""
        strategies = {
            'so_strategy': [],  # Strengths-Opportunities
            'wo_strategy': [],  # Weaknesses-Opportunities
            'st_strategy': [],  # Strengths-Threats
            'wt_strategy': []   # Weaknesses-Threats
        }
        
        if swot.strengths and swot.opportunities:
            strategies['so_strategy'].append(
                "Leverage core strengths to capture market opportunities"
            )
        
        if swot.weaknesses and swot.opportunities:
            strategies['wo_strategy'].append(
                "Address weaknesses to better exploit opportunities"
            )
        
        if swot.strengths and swot.threats:
            strategies['st_strategy'].append(
                "Use strengths to mitigate external threats"
            )
        
        if swot.weaknesses and swot.threats:
            strategies['wt_strategy'].append(
                "Minimize weaknesses to defend against threats"
            )
        
        return strategies

class RiskManager:
    """Manages strategic risks."""
    
    def __init__(self):
        self.risks: List[Dict] = []
        self.mitigations: Dict[str, List[str]] = {}
    
    def add_risk(self, name: str, category: str, probability: str,
                impact: str, description: str) -> Dict:
        """Add strategic risk."""
        risk = {
            'id': f"risk_{len(self.risks) + 1}",
            'name': name,
            'category': category,
            'probability': probability,
            'impact': impact,
            'description': description,
            'status': 'identified',
            'mitigations': []
        }
        self.risks.append(risk)
        return risk
    
    def assess_risk(self, risk_id: str) -> Dict:
        """Assess risk level."""
        probability_scores = {'low': 1, 'medium': 2, 'high': 3}
        impact_scores = {'low': 1, 'medium': 2, 'high': 3}
        
        for risk in self.risks:
            if risk['id'] == risk_id:
                prob_score = probability_scores.get(risk['probability'], 1)
                impact_score = impact_scores.get(risk['impact'], 1)
                risk['level'] = prob_score * impact_score
                risk['assessed_at'] = datetime.now().isoformat()
                return risk
        
        return {'error': 'Risk not found'}
    
    def add_mitigation(self, risk_id: str, mitigation: str) -> None:
        """Add mitigation strategy for risk."""
        for risk in self.risks:
            if risk['id'] == risk_id:
                risk['mitigations'].append(mitigation)
                if 'mitigation_actions' not in self.mitigations:
                    self.mitigations[risk_id] = []
                self.mitigations[risk_id].append(mitigation)
    
    def get_risk_register(self) -> Dict[str, Any]:
        """Get risk register summary."""
        high_risks = [r for r in self.risks if r.get('level', 0) >= 6]
        medium_risks = [r for r in self.risks if 3 <= r.get('level', 0) < 6]
        low_risks = [r for r in self.risks if r.get('level', 0) < 3]
        
        return {
            'total_risks': len(self.risks),
            'high_risk_count': len(high_risks),
            'medium_risk_count': len(medium_risks),
            'low_risk_count': len(low_risks),
            'exposure_score': sum(r.get('level', 0) for r in self.risks)
        }

class StrategyAnalyzer:
    """Analyzes strategic performance."""
    
    def __init__(self, planner: StrategicPlanner, 
                 risk_manager: RiskManager):
        self.planner = planner
        self.risk_manager = risk_manager
    
    def calculate_metrics(self) -> StrategicMetrics:
        """Calculate strategic metrics."""
        objectives = list(self.planner.objectives.values())
        
        completed = len([o for o in objectives if o.status == ObjectiveStatus.COMPLETED])
        objective_completion = (completed / len(objectives) * 100) if objectives else 0
        
        initiatives = list(self.planner.initiatives.values())
        init_progress = sum(i.status == 'completed' for i in initiatives) / len(initiatives) * 100 if initiatives else 0
        
        total_budget = sum(o.budget for o in objectives)
        utilized = sum(o.metrics.get('budget_used', 0) for o in objectives)
        budget_util = (utilized / total_budget * 100) if total_budget > 0 else 0
        
        risk_register = self.risk_manager.get_risk_register()
        risk_exposure = min(risk_register['exposure_score'] / 50 * 100, 100)
        
        overall = (
            objective_completion * 0.4 +
            init_progress * 0.3 +
            (100 - risk_exposure) * 0.2 +
            budget_util * 0.1
        )
        
        return StrategicMetrics(
            objective_completion=objective_completion,
            initiative_progress=init_progress,
            budget_utilization=budget_util,
            risk_exposure=risk_exposure,
            overall_health=overall
        )
    
    def analyze_objectives_health(self) -> Dict[str, Any]:
        """Analyze health of all objectives."""
        health = {
            'on_track': 0,
            'at_risk': 0,
            'behind': 0,
            'completed': 0
        }
        
        for obj in self.planner.objectives.values():
            timeline = self.planner.calculate_timeline_status(obj.id)
            if obj.status == ObjectiveStatus.COMPLETED:
                health['completed'] += 1
            elif timeline['status'] == 'behind' or obj.status == ObjectiveStatus.AT_RISK:
                health['at_risk'] += 1
            elif timeline['status'] == 'ahead':
                health['on_track'] += 1
            else:
                health['on_track'] += 1
        
        return health

class StrategyAgent:
    """Main strategy agent."""
    
    def __init__(self):
        self.planner = StrategicPlanner()
        self.swot = SWOTAnalyzer()
        self.risk_manager = RiskManager()
        self.analyzer = StrategyAnalyzer(self.planner, self.risk_manager)
    
    def define_strategy(self, name: str, objectives: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Define new strategy with objectives."""
        created = []
        
        for obj_data in objectives:
            obj = self.planner.create_objective(
                title=obj_data['title'],
                description=obj_data['description'],
                priority=StrategicPriority[obj_data['priority'].upper()],
                key_results=obj_data.get('key_results', []),
                target_date=datetime.fromisoformat(obj_data['target_date']),
                owner=obj_data['owner'],
                budget=obj_data.get('budget', 0)
            )
            created.append(obj.id)
            
            if 'initiatives' in obj_data:
                for ini_data in obj_data['initiatives']:
                    self.planner.add_initiative(
                        objective_id=obj.id,
                        name=ini_data['name'],
                        description=ini_data['description'],
                        resources=ini_data.get('resources', {}),
                        timeline={'start': datetime.now(), 'end': obj.target_date},
                        expected_impact=ini_data.get('impact', ''),
                        risks=ini_data.get('risks', [])
                    )
        
        return {
            'strategy': name,
            'objectives_created': len(created),
            'objective_ids': created
        }
    
    def perform_swot_analysis(self, data: Dict[str, List[str]]) -> Dict[str, Any]:
        """Perform SWOT analysis."""
        swot = self.swot.analyze(
            strengths=data.get('strengths', []),
            weaknesses=data.get('weaknesses', []),
            opportunities=data.get('opportunities', []),
            threats=data.get('threats', [])
        )
        
        strategies = self.swot.generate_strategies(swot)
        
        return {
            'swot': {
                'strengths': swot.strengths,
                'weaknesses': swot.weaknesses,
                'opportunities': swot.opportunities,
                'threats': swot.threats
            },
            'strategies': strategies,
            'score': swot.score
        }
    
    def assess_risk_landscape(self, risks: List[Dict[str, str]]) -> Dict[str, Any]:
        """Assess risk landscape."""
        for risk in risks:
            self.risk_manager.add_risk(
                name=risk['name'],
                category=risk.get('category', 'operational'),
                probability=risk.get('probability', 'medium'),
                impact=risk.get('impact', 'medium'),
                description=risk.get('description', '')
            )
        
        for risk in self.risk_manager.risks:
            self.risk_manager.assess_risk(risk['id'])
        
        return self.risk_manager.get_risk_register()
    
    def get_strategy_dashboard(self) -> Dict[str, Any]:
        """Get strategic dashboard."""
        metrics = self.analyzer.calculate_metrics()
        objective_health = self.analyzer.analyze_objectives_health()
        
        return {
            'health_score': metrics.overall_health,
            'metrics': {
                'objective_completion': f"{metrics.objective_completion:.1f}%",
                'initiative_progress': f"{metrics.initiative_progress:.1f}%",
                'budget_utilization': f"{metrics.budget_utilization:.1f}%",
                'risk_exposure': f"{metrics.risk_exposure:.1f}%"
            },
            'objectives': {
                'total': len(self.planner.objectives),
                'by_health': objective_health
            },
            'initiatives': {
                'total': len(self.planner.initiatives),
                'by_status': defaultdict(int)
            },
            'risks': self.risk_manager.get_risk_register()
        }

def main():
    """Main entry point."""
    agent = StrategyAgent()
    
    swot_result = agent.perform_swot_analysis({
        'strengths': ['Strong tech team', 'Good brand'],
        'weaknesses': ['Limited budget', 'Small team'],
        'opportunities': ['Growing market', 'New technology'],
        'threats': ['Competition', 'Market changes']
    })
    print(f"SWOT: {swot_result}")
    
    dashboard = agent.get_strategy_dashboard()
    print(f"Dashboard: {dashboard}")

if __name__ == "__main__":
    main()

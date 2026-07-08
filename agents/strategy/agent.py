"""
Strategy Agent - Strategic Planning, Competitive Analysis, and Business Intelligence.

Comprehensive capabilities for strategic planning, SWOT analysis, competitive intelligence,
market positioning, OKR management, scenario planning, business model canvas, and risk management.
"""

from __future__ import annotations

import json
import logging
import math
import secrets
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class StrategicPriority(Enum):
    """Strategic priority categories."""
    GROWTH = "growth"
    EFFICIENCY = "efficiency"
    INNOVATION = "innovation"
    MARKET = "market"
    TALENT = "talent"
    TECHNOLOGY = "technology"
    SUSTAINABILITY = "sustainability"


class ObjectiveStatus(Enum):
    """OKR objective lifecycle status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    AT_RISK = "at_risk"
    ON_TRACK = "on_track"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class RiskLevel(Enum):
    """Strategic risk classification."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class CompetitivePosition(Enum):
    """Market positioning classification."""
    LEADER = "leader"
    CHALLENGER = "challenger"
    FOLLOWER = "follower"
    NICHE = "niche"


class ScenarioType(Enum):
    """Scenario planning types."""
    BEST_CASE = "best_case"
    BASE_CASE = "base_case"
    WORST_CASE = "worst_case"
    BLACK_SWAN = "black_swan"


class MarketPhase(Enum):
    """Industry lifecycle phases."""
    INTRODUCTION = "introduction"
    GROWTH = "growth"
    MATURITY = "maturity"
    DECLINE = "decline"


class BusinessModelBlock(Enum):
    """Business Model Canvas blocks."""
    CUSTOMER_SEGMENTS = "customer_segments"
    VALUE_PROPOSITIONS = "value_propositions"
    CHANNELS = "channels"
    CUSTOMER_RELATIONSHIPS = "customer_relationships"
    REVENUE_STREAMS = "revenue_streams"
    KEY_RESOURCES = "key_resources"
    KEY_ACTIVITIES = "key_activities"
    KEY_PARTNERSHIPS = "key_partnerships"
    COST_STRUCTURE = "cost_structure"


class InitiativeStatus(Enum):
    """Initiative lifecycle status."""
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class StrategicObjective:
    """OKR objective with key results."""
    id: str
    title: str
    description: str
    priority: StrategicPriority
    status: ObjectiveStatus
    key_results: List[KeyResult]
    owner: str
    start_date: datetime
    target_date: datetime
    budget: float
    dependencies: List[str]
    progress: float = 0.0

    def overall_progress(self) -> float:
        if not self.key_results:
            return self.progress
        return sum(kr.progress for kr in self.key_results) / len(self.key_results)


@dataclass
class KeyResult:
    """Measurable key result for an objective."""
    id: str
    description: str
    metric: str
    target_value: float
    current_value: float
    unit: str
    progress: float = 0.0

    def calculate_progress(self) -> float:
        if self.target_value == 0:
            return 0.0
        self.progress = min(1.0, self.current_value / self.target_value)
        return self.progress


@dataclass
class Initiative:
    """Strategic initiative supporting an objective."""
    id: str
    objective_id: str
    name: str
    description: str
    status: InitiativeStatus
    resources: Dict[str, Any]
    timeline: Dict[str, datetime]
    expected_impact: str
    risks: List[str]
    budget: float = 0.0
    progress: float = 0.0


@dataclass
class SWOTAnalysis:
    """SWOT analysis result."""
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]
    scores: Dict[str, float]
    strategies: Dict[str, List[str]]
    created_at: datetime


@dataclass
class Competitor:
    """Competitor profile."""
    id: str
    name: str
    position: CompetitivePosition
    market_share: float
    strengths: List[str]
    weaknesses: List[str]
    pricing: str
    recent_moves: List[str]
    threat_level: RiskLevel
    last_updated: datetime


@dataclass
class MarketSegment:
    """Market segment analysis."""
    id: str
    name: str
    size: float
    growth_rate: float
    phase: MarketPhase
    key_trends: List[str]
    barriers_to_entry: List[str]
    opportunity_score: float


@dataclass
class Scenario:
    """Scenario planning scenario."""
    id: str
    name: str
    scenario_type: ScenarioType
    assumptions: List[str]
    impacts: Dict[str, float]
    probability: float
    mitigation: List[str]
    triggers: List[str]


@dataclass
class StrategicRisk:
    """Strategic risk record."""
    id: str
    name: str
    category: str
    probability: float
    impact: float
    description: str
    level: RiskLevel
    mitigations: List[str]
    owner: str
    status: str = "identified"
    risk_score: float = 0.0

    def calculate_risk_score(self) -> float:
        self.risk_score = self.probability * self.impact
        if self.risk_score >= 12:
            self.level = RiskLevel.CRITICAL
        elif self.risk_score >= 8:
            self.level = RiskLevel.HIGH
        elif self.risk_score >= 4:
            self.level = RiskLevel.MEDIUM
        else:
            self.level = RiskLevel.LOW
        return self.risk_score


@dataclass
class BusinessModel:
    """Business Model Canvas representation."""
    id: str
    name: str
    blocks: Dict[BusinessModelBlock, List[str]]
    value_score: float
    created_at: datetime


@dataclass
class StrategicMetrics:
    """Aggregate strategic performance metrics."""
    objective_completion: float
    initiative_progress: float
    budget_utilization: float
    risk_exposure: float
    overall_health: float
    competitive_position: str


# ---------------------------------------------------------------------------
# Strategic Planner (OKR Management)
# ---------------------------------------------------------------------------

class StrategicPlanner:
    """Plans, tracks, and manages strategic objectives and key results."""

    def __init__(self) -> None:
        self.objectives: Dict[str, StrategicObjective] = {}
        self.initiatives: Dict[str, Initiative] = {}
        self.milestones: List[Dict[str, Any]] = []
        logger.info("StrategicPlanner initialized")

    def create_objective(self, title: str, description: str,
                         priority: StrategicPriority,
                         key_results: List[Dict[str, Any]],
                         target_date: datetime, owner: str,
                         budget: float = 0.0) -> StrategicObjective:
        """Create a strategic objective with key results."""
        krs = []
        for kr_data in key_results:
            kr = KeyResult(
                id=f"kr_{uuid.uuid4().hex[:8]}",
                description=kr_data.get("description", ""),
                metric=kr_data.get("metric", ""),
                target_value=kr_data.get("target_value", 100.0),
                current_value=kr_data.get("current_value", 0.0),
                unit=kr_data.get("unit", ""),
            )
            kr.calculate_progress()
            krs.append(kr)

        obj = StrategicObjective(
            id=f"obj_{uuid.uuid4().hex[:8]}",
            title=title,
            description=description,
            priority=priority,
            status=ObjectiveStatus.NOT_STARTED,
            key_results=krs,
            owner=owner,
            start_date=datetime.now(),
            target_date=target_date,
            budget=budget,
            dependencies=[],
        )
        self.objectives[obj.id] = obj
        logger.info("Objective created: %s", obj.id)
        return obj

    def update_key_result(self, objective_id: str, kr_id: str,
                          current_value: float) -> Optional[KeyResult]:
        """Update a key result's current value."""
        obj = self.objectives.get(objective_id)
        if not obj:
            return None
        for kr in obj.key_results:
            if kr.id == kr_id:
                kr.current_value = current_value
                kr.calculate_progress()
                self._recalc_objective_status(obj)
                return kr
        return None

    def _recalc_objective_status(self, obj: StrategicObjective) -> None:
        """Recalculate objective status from key result progress."""
        progress = obj.overall_progress()
        obj.progress = progress
        if progress >= 1.0:
            obj.status = ObjectiveStatus.COMPLETED
        elif progress >= 0.7:
            obj.status = ObjectiveStatus.ON_TRACK
        elif progress >= 0.3:
            obj.status = ObjectiveStatus.IN_PROGRESS
        else:
            obj.status = ObjectiveStatus.AT_RISK

    def add_initiative(self, objective_id: str, name: str,
                       description: str, resources: Dict[str, Any],
                       timeline: Dict[str, datetime],
                       expected_impact: str,
                       risks: Optional[List[str]] = None,
                       budget: float = 0.0) -> Initiative:
        """Add an initiative to an objective."""
        initiative = Initiative(
            id=f"ini_{uuid.uuid4().hex[:8]}",
            objective_id=objective_id,
            name=name,
            description=description,
            status=InitiativeStatus.PLANNED,
            resources=resources,
            timeline=timeline,
            expected_impact=expected_impact,
            risks=risks or [],
            budget=budget,
        )
        self.initiatives[initiative.id] = initiative
        return initiative

    def get_timeline_status(self, objective_id: str) -> Dict[str, Any]:
        """Calculate timeline variance for an objective."""
        obj = self.objectives.get(objective_id)
        if not obj:
            return {"error": "Objective not found"}

        now = datetime.now()
        total_days = (obj.target_date - obj.start_date).days
        elapsed_days = (now - obj.start_date).days

        if total_days == 0:
            return {"status": "unknown", "progress": 0}

        expected = (elapsed_days / total_days) * 100
        actual = obj.progress * 100
        variance = actual - expected

        return {
            "expected_progress": round(expected, 1),
            "actual_progress": round(actual, 1),
            "variance": round(variance, 1),
            "days_remaining": max(0, (obj.target_date - now).days),
            "status": "ahead" if variance > 5 else "behind" if variance < -5 else "on_track",
        }

    def get_objectives_by_priority(self, priority: StrategicPriority) -> List[StrategicObjective]:
        """Filter objectives by priority."""
        return [o for o in self.objectives.values() if o.priority == priority]


# ---------------------------------------------------------------------------
# SWOT Analyzer
# ---------------------------------------------------------------------------

class SWOTAnalyzer:
    """Performs SWOT analysis and generates strategic recommendations."""

    def __init__(self) -> None:
        self.analyses: List[SWOTAnalysis] = []

    def analyze(self, strengths: List[str], weaknesses: List[str],
                opportunities: List[str], threats: List[str],
                context: str = "general") -> SWOTAnalysis:
        """Perform SWOT analysis."""
        scores = self._calculate_scores(strengths, weaknesses, opportunities, threats)
        strategies = self._generate_strategies(strengths, weaknesses, opportunities, threats)

        analysis = SWOTAnalysis(
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            threats=threats,
            scores=scores,
            strategies=strategies,
            created_at=datetime.now(),
        )
        self.analyses.append(analysis)
        return analysis

    def _calculate_scores(self, s: List[str], w: List[str],
                          o: List[str], t: List[str]) -> Dict[str, float]:
        """Calculate SWOT dimension scores (0-50 each)."""
        return {
            "strengths_score": min(len(s) * 10, 50),
            "weaknesses_score": max(50 - len(w) * 10, 0),
            "opportunities_score": min(len(o) * 10, 50),
            "threats_score": max(50 - len(t) * 10, 0),
        }

    def _generate_strategies(self, s: List[str], w: List[str],
                             o: List[str], t: List[str]) -> Dict[str, List[str]]:
        """Generate TOWS matrix strategies."""
        strategies: Dict[str, List[str]] = {
            "so_strategies": [],
            "wo_strategies": [],
            "st_strategies": [],
            "wt_strategies": [],
        }

        if s and o:
            strategies["so_strategies"].append("Maximize strengths to exploit opportunities")
        if w and o:
            strategies["wo_strategies"].append("Address weaknesses to capture opportunities")
        if s and t:
            strategies["st_strategies"].append("Leverage strengths to counter threats")
        if w and t:
            strategies["wt_strategies"].append("Minimize weaknesses to avoid threats")

        return strategies

    def get_comparative_analysis(self) -> Optional[Dict[str, Any]]:
        """Compare latest two SWOT analyses."""
        if len(self.analyses) < 2:
            return None
        prev, curr = self.analyses[-2], self.analyses[-1]
        return {
            "strengths_change": len(curr.strengths) - len(prev.strengths),
            "weaknesses_change": len(curr.weaknesses) - len(prev.weaknesses),
            "opportunities_change": len(curr.opportunities) - len(prev.opportunities),
            "threats_change": len(curr.threats) - len(prev.threats),
        }


# ---------------------------------------------------------------------------
# Competitive Analyzer
# ---------------------------------------------------------------------------

class CompetitiveAnalyzer:
    """Tracks and analyzes competitor landscape."""

    def __init__(self) -> None:
        self.competitors: Dict[str, Competitor] = {}
        self.battle_cards: Dict[str, Dict[str, Any]] = {}

    def add_competitor(self, name: str, position: CompetitivePosition,
                       market_share: float, strengths: List[str],
                       weaknesses: List[str], pricing: str = "") -> Competitor:
        """Register a competitor."""
        comp = Competitor(
            id=f"comp_{uuid.uuid4().hex[:8]}",
            name=name,
            position=position,
            market_share=market_share,
            strengths=strengths,
            weaknesses=weaknesses,
            pricing=pricing,
            recent_moves=[],
            threat_level=RiskLevel.MEDIUM,
            last_updated=datetime.now(),
        )
        self.competitors[comp.id] = comp
        return comp

    def add_competitor_move(self, competitor_id: str, move: str) -> Dict[str, Any]:
        """Record a competitive move."""
        comp = self.competitors.get(competitor_id)
        if not comp:
            return {"error": f"Competitor {competitor_id} not found"}
        comp.recent_moves.append(move)
        comp.last_updated = datetime.now()
        return {"competitor_id": competitor_id, "move": move}

    def generate_battle_card(self, competitor_id: str) -> Dict[str, Any]:
        """Generate a battle card for a competitor."""
        comp = self.competitors.get(competitor_id)
        if not comp:
            return {"error": "Competitor not found"}

        card = {
            "competitor": comp.name,
            "position": comp.position.value,
            "market_share": comp.market_share,
            "their_strengths": comp.strengths,
            "their_weaknesses": comp.weaknesses,
            "our_advantages": comp.weaknesses,
            "their_disadvantages": comp.strengths,
            "pricing": comp.pricing,
            "recent_moves": comp.recent_moves,
            "talk_track": self._generate_talk_track(comp),
        }
        self.battle_cards[competitor_id] = card
        return card

    def _generate_talk_track(self, comp: Competitor) -> List[str]:
        """Generate sales talk track against competitor."""
        talk = [f"We differentiate from {comp.name} through:"]
        for weakness in comp.weaknesses[:3]:
            talk.append(f"  - Our strength vs their {weakness}")
        return talk

    def get_competitive_landscape(self) -> Dict[str, Any]:
        """Summarize competitive landscape."""
        total_share = sum(c.market_share for c in self.competitors.values())
        by_position = defaultdict(list)
        for c in self.competitors.values():
            by_position[c.position.value].append(c.name)

        return {
            "total_competitors": len(self.competitors),
            "market_share_covered": round(total_share, 1),
            "by_position": dict(by_position),
            "top_threats": [
                {"name": c.name, "threat": c.threat_level.value}
                for c in sorted(self.competitors.values(), key=lambda x: -x.market_share)[:5]
            ],
        }


# ---------------------------------------------------------------------------
# Risk Manager
# ---------------------------------------------------------------------------

class RiskManager:
    """Strategic risk identification, assessment, and mitigation tracking."""

    def __init__(self) -> None:
        self.risks: List[StrategicRisk] = []
        self.risk_matrix: Dict[str, List[StrategicRisk]] = defaultdict(list)

    def add_risk(self, name: str, category: str, probability: float,
                 impact: float, description: str, owner: str = "") -> StrategicRisk:
        """Register a strategic risk."""
        risk = StrategicRisk(
            id=f"risk_{uuid.uuid4().hex[:8]}",
            name=name,
            category=category,
            probability=probability,
            impact=impact,
            description=description,
            level=RiskLevel.MEDIUM,
            mitigations=[],
            owner=owner,
        )
        risk.calculate_risk_score()
        self.risks.append(risk)
        self.risk_matrix[risk.level.value].append(risk)
        return risk

    def add_mitigation(self, risk_id: str, mitigation: str) -> Dict[str, Any]:
        """Add mitigation strategy to a risk."""
        for risk in self.risks:
            if risk.id == risk_id:
                risk.mitigations.append(mitigation)
                return {"risk_id": risk_id, "mitigation": mitigation}
        return {"error": f"Risk {risk_id} not found"}

    def update_risk(self, risk_id: str, probability: Optional[float] = None,
                    impact: Optional[float] = None) -> Optional[StrategicRisk]:
        """Update risk parameters and recalculate."""
        for risk in self.risks:
            if risk.id == risk_id:
                if probability is not None:
                    risk.probability = probability
                if impact is not None:
                    risk.impact = impact
                risk.calculate_risk_score()
                return risk
        return None

    def get_risk_register(self) -> Dict[str, Any]:
        """Generate risk register summary."""
        by_level = defaultdict(list)
        for r in self.risks:
            by_level[r.level.value].append({
                "id": r.id,
                "name": r.name,
                "score": r.risk_score,
                "mitigations": len(r.mitigations),
            })

        return {
            "total_risks": len(self.risks),
            "by_level": dict(by_level),
            "exposure_score": sum(r.risk_score for r in self.risks),
            "unmitigated": sum(1 for r in self.risks if not r.mitigations),
        }

    def get_top_risks(self, limit: int = 5) -> List[StrategicRisk]:
        """Get highest-rated risks."""
        return sorted(self.risks, key=lambda r: -r.risk_score)[:limit]


# ---------------------------------------------------------------------------
# Scenario Planner
# ---------------------------------------------------------------------------

class ScenarioPlanner:
    """Builds and evaluates strategic scenarios."""

    def __init__(self) -> None:
        self.scenarios: Dict[str, Scenario] = {}

    def create_scenario(self, name: str, scenario_type: ScenarioType,
                        assumptions: List[str],
                        impacts: Dict[str, float],
                        probability: float,
                        mitigation: Optional[List[str]] = None,
                        triggers: Optional[List[str]] = None) -> Scenario:
        """Create a strategic scenario."""
        scenario = Scenario(
            id=f"scn_{uuid.uuid4().hex[:8]}",
            name=name,
            scenario_type=scenario_type,
            assumptions=assumptions,
            impacts=impacts,
            probability=probability,
            mitigation=mitigation or [],
            triggers=triggers or [],
        )
        self.scenarios[scenario.id] = scenario
        return scenario

    def evaluate_scenarios(self) -> Dict[str, Any]:
        """Evaluate all scenarios and calculate expected impact."""
        results = []
        for scenario in self.scenarios.values():
            weighted_impact = sum(
                v * scenario.probability for v in scenario.impacts.values()
            )
            results.append({
                "id": scenario.id,
                "name": scenario.name,
                "type": scenario.scenario_type.value,
                "probability": scenario.probability,
                "weighted_impact": round(weighted_impact, 2),
                "impacts": scenario.impacts,
                "mitigation_count": len(scenario.mitigation),
            })

        results.sort(key=lambda x: -x["weighted_impact"])
        return {
            "total_scenarios": len(results),
            "scenarios": results,
            "expected_value": round(
                sum(r["weighted_impact"] for r in results) / max(len(results), 1), 2
            ),
        }

    def recommend_strategy(self) -> Dict[str, Any]:
        """Recommend strategy based on scenario analysis."""
        evaluation = self.evaluate_scenarios()
        worst = next((s for s in evaluation["scenarios"] if s["type"] == "worst_case"), None)
        best = next((s for s in evaluation["scenarios"] if s["type"] == "best_case"), None)

        return {
            "recommendation": "Diversify to hedge worst-case scenario" if worst else "Pursue growth",
            "focus_areas": ["Risk mitigation", "Capability building", "Market expansion"],
            "worst_case_impact": worst["weighted_impact"] if worst else 0,
            "best_case_upside": best["weighted_impact"] if best else 0,
        }


# ---------------------------------------------------------------------------
# Market Analyzer
# ---------------------------------------------------------------------------

class MarketAnalyzer:
    """Market segmentation and opportunity analysis."""

    def __init__(self) -> None:
        self.segments: Dict[str, MarketSegment] = {}
        self.trends: List[Dict[str, Any]] = []

    def add_segment(self, name: str, size: float, growth_rate: float,
                    phase: MarketPhase, trends: List[str],
                    barriers: Optional[List[str]] = None) -> MarketSegment:
        """Register a market segment."""
        barriers = barriers or []
        opportunity = self._calc_opportunity(size, growth_rate, len(barriers))
        segment = MarketSegment(
            id=f"seg_{uuid.uuid4().hex[:8]}",
            name=name,
            size=size,
            growth_rate=growth_rate,
            phase=phase,
            key_trends=trends,
            barriers_to_entry=barriers,
            opportunity_score=opportunity,
        )
        self.segments[segment.id] = segment
        return segment

    def _calc_opportunity(self, size: float, growth: float,
                          barriers: int) -> float:
        """Calculate opportunity score (0-100)."""
        size_score = min(size / 1_000_000_000, 50)
        growth_score = min(growth * 100, 30)
        barrier_penalty = barriers * 5
        return max(0, min(100, size_score + growth_score - barrier_penalty))

    def get_top_opportunities(self, limit: int = 5) -> List[MarketSegment]:
        """Get segments ranked by opportunity score."""
        return sorted(self.segments.values(), key=lambda s: -s.opportunity_score)[:limit]

    def get_market_summary(self) -> Dict[str, Any]:
        """Summarize market landscape."""
        total_size = sum(s.size for s in self.segments.values())
        avg_growth = sum(s.growth_rate for s in self.segments.values()) / max(len(self.segments), 1)
        by_phase = defaultdict(int)
        for s in self.segments.values():
            by_phase[s.phase.value] += 1

        return {
            "total_segments": len(self.segments),
            "total_market_size": total_size,
            "avg_growth_rate": round(avg_growth, 3),
            "by_phase": dict(by_phase),
            "top_opportunities": [
                {"name": s.name, "score": s.opportunity_score}
                for s in self.get_top_opportunities(3)
            ],
        }


# ---------------------------------------------------------------------------
# Business Model Canvas
# ---------------------------------------------------------------------------

class BusinessModelCanvas:
    """Business Model Canvas builder and analyzer."""

    def __init__(self) -> None:
        self.models: Dict[str, BusinessModel] = {}

    def create_model(self, name: str,
                     blocks: Dict[BusinessModelBlock, List[str]]) -> BusinessModel:
        """Create a business model canvas."""
        score = self._evaluate_value(blocks)
        model = BusinessModel(
            id=f"bmc_{uuid.uuid4().hex[:8]}",
            name=name,
            blocks=blocks,
            value_score=score,
            created_at=datetime.now(),
        )
        self.models[model.id] = model
        return model

    def _evaluate_value(self, blocks: Dict[BusinessModelBlock, List[str]]) -> float:
        """Evaluate business model value score (0-100)."""
        filled = sum(1 for v in blocks.values() if v)
        total = len(BusinessModelBlock)
        completeness = (filled / total) * 60

       vp = blocks.get(BusinessModelBlock.VALUE_PROPOSITIONS, [])
        revenue = blocks.get(BusinessModelBlock.REVENUE_STREAMS, [])
        differentiation = min(len(vp) * 10, 20)
        monetization = min(len(revenue) * 10, 20)

        return min(100, completeness + differentiation + monetization)

    def compare_models(self, model_id_1: str, model_id_2: str) -> Dict[str, Any]:
        """Compare two business models."""
        m1 = self.models.get(model_id_1)
        m2 = self.models.get(model_id_2)
        if not m1 or not m2:
            return {"error": "Model not found"}

        comparison = {}
        for block in BusinessModelBlock:
            b1 = m1.blocks.get(block, [])
            b2 = m2.blocks.get(block, [])
            comparison[block.value] = {
                "model_1": len(b1),
                "model_2": len(b2),
                "advantage": "model_1" if len(b1) > len(b2) else "model_2" if len(b2) > len(b1) else "equal",
            }

        return {
            "model_1": {"name": m1.name, "score": m1.value_score},
            "model_2": {"name": m2.name, "score": m2.value_score},
            "block_comparison": comparison,
            "winner": m1.name if m1.value_score > m2.value_score else m2.name,
        }


# ---------------------------------------------------------------------------
# Strategy Analyzer (Metrics)
# ---------------------------------------------------------------------------

class StrategyAnalyzer:
    """Calculates aggregate strategic performance metrics."""

    def __init__(self, planner: StrategicPlanner, risk_manager: RiskManager) -> None:
        self.planner = planner
        self.risk_manager = risk_manager

    def calculate_metrics(self) -> StrategicMetrics:
        """Calculate all strategic metrics."""
        objectives = list(self.planner.objectives.values())
        completed = sum(1 for o in objectives if o.status == ObjectiveStatus.COMPLETED)
        obj_completion = (completed / max(len(objectives), 1)) * 100

        initiatives = list(self.planner.initiatives.values())
        init_progress = sum(i.progress for i in initiatives) / max(len(initiatives), 1) * 100

        total_budget = sum(o.budget for o in objectives)
        utilized = sum(o.budget * o.progress for o in objectives)
        budget_util = (utilized / max(total_budget, 1)) * 100

        risk_register = self.risk_manager.get_risk_register()
        risk_exposure = min(risk_register["exposure_score"] / 50 * 100, 100)

        overall = (
            obj_completion * 0.35 +
            init_progress * 0.25 +
            (100 - risk_exposure) * 0.20 +
            budget_util * 0.20
        )

        return StrategicMetrics(
            objective_completion=round(obj_completion, 1),
            initiative_progress=round(init_progress, 1),
            budget_utilization=round(budget_util, 1),
            risk_exposure=round(risk_exposure, 1),
            overall_health=round(overall, 1),
            competitive_position="leader",
        )

    def analyze_objective_health(self) -> Dict[str, Any]:
        """Health analysis of all objectives."""
        health = {"on_track": 0, "at_risk": 0, "behind": 0, "completed": 0}
        for obj in self.planner.objectives.values():
            timeline = self.planner.get_timeline_status(obj.id)
            if obj.status == ObjectiveStatus.COMPLETED:
                health["completed"] += 1
            elif timeline.get("status") == "behind" or obj.status == ObjectiveStatus.AT_RISK:
                health["at_risk"] += 1
            elif timeline.get("status") == "ahead":
                health["on_track"] += 1
            else:
                health["on_track"] += 1
        return health


# ---------------------------------------------------------------------------
# Strategy Agent (Orchestrator)
# ---------------------------------------------------------------------------

class StrategyAgent:
    """Top-level strategic planning and business intelligence agent."""

    def __init__(self) -> None:
        self.planner = StrategicPlanner()
        self.swot = SWOTAnalyzer()
        self.competitive = CompetitiveAnalyzer()
        self.risk_manager = RiskManager()
        self.scenario_planner = ScenarioPlanner()
        self.market = MarketAnalyzer()
        self.bmc = BusinessModelCanvas()
        self.analyzer = StrategyAnalyzer(self.planner, self.risk_manager)
        logger.info("StrategyAgent initialized")

    def define_strategy(self, name: str,
                        objectives: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Define a strategy with objectives and key results."""
        created = []
        for obj_data in objectives:
            obj = self.planner.create_objective(
                title=obj_data["title"],
                description=obj_data.get("description", ""),
                priority=StrategicPriority[obj_data.get("priority", "growth").upper()],
                key_results=obj_data.get("key_results", []),
                target_date=datetime.fromisoformat(obj_data["target_date"]),
                owner=obj_data.get("owner", "unassigned"),
                budget=obj_data.get("budget", 0.0),
            )
            created.append(obj.id)

            for ini_data in obj_data.get("initiatives", []):
                self.planner.add_initiative(
                    objective_id=obj.id,
                    name=ini_data["name"],
                    description=ini_data.get("description", ""),
                    resources=ini_data.get("resources", {}),
                    timeline={"start": datetime.now(), "end": obj.target_date},
                    expected_impact=ini_data.get("impact", ""),
                    risks=ini_data.get("risks", []),
                )

        return {"strategy": name, "objectives_created": len(created), "objective_ids": created}

    def perform_swot(self, data: Dict[str, List[str]]) -> Dict[str, Any]:
        """Perform SWOT analysis."""
        analysis = self.swot.analyze(
            strengths=data.get("strengths", []),
            weaknesses=data.get("weaknesses", []),
            opportunities=data.get("opportunities", []),
            threats=data.get("threats", []),
        )
        return {
            "swot": {
                "strengths": analysis.strengths,
                "weaknesses": analysis.weaknesses,
                "opportunities": analysis.opportunities,
                "threats": analysis.threats,
            },
            "scores": analysis.scores,
            "strategies": analysis.strategies,
        }

    def assess_risks(self, risks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Assess a batch of strategic risks."""
        for risk_data in risks:
            self.risk_manager.add_risk(
                name=risk_data["name"],
                category=risk_data.get("category", "operational"),
                probability=risk_data.get("probability", 0.5),
                impact=risk_data.get("impact", 0.5),
                description=risk_data.get("description", ""),
                owner=risk_data.get("owner", ""),
            )
        return self.risk_manager.get_risk_register()

    def analyze_competitors(self) -> Dict[str, Any]:
        """Get competitive landscape summary."""
        return self.competitive.get_competitive_landscape()

    def get_strategy_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive strategy dashboard."""
        metrics = self.analyzer.calculate_metrics()
        obj_health = self.analyzer.analyze_objective_health()
        risk_register = self.risk_manager.get_risk_register()
        market_summary = self.market.get_market_summary()
        scenario_eval = self.scenario_planner.evaluate_scenarios()

        return {
            "timestamp": datetime.now().isoformat(),
            "health_score": metrics.overall_health,
            "metrics": {
                "objective_completion": f"{metrics.objective_completion}%",
                "initiative_progress": f"{metrics.initiative_progress}%",
                "budget_utilization": f"{metrics.budget_utilization}%",
                "risk_exposure": f"{metrics.risk_exposure}%",
            },
            "objectives": {
                "total": len(self.planner.objectives),
                "by_health": obj_health,
            },
            "risks": risk_register,
            "market": market_summary,
            "scenarios": scenario_eval,
            "competitive": self.competitive.get_competitive_landscape(),
        }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate StrategyAgent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    print("\n" + "=" * 60)
    print("  Strategy Agent - Strategic Planning & Business Intelligence")
    print("=" * 60 + "\n")

    agent = StrategyAgent()

    # SWOT Analysis
    swot = agent.perform_swot({
        "strengths": ["Strong tech team", "Brand recognition", "Patent portfolio"],
        "weaknesses": ["Limited budget", "Small sales team"],
        "opportunities": ["Growing market", "AI/ML adoption", "Remote work trend"],
        "threats": ["New competitors", "Regulatory changes", "Economic downturn"],
    })
    print(f"SWOT Scores: {swot['scores']}")
    print(f"Strategies: {list(swot['strategies'].keys())}")

    # Competitive Analysis
    agent.competitive.add_competitor(
        "CompetitorA", CompetitivePosition.LEADER, 35.0,
        ["Brand", "Distribution"], ["High pricing", "Slow innovation"]
    )
    agent.competitive.add_competitor(
        "CompetitorB", CompetitivePosition.CHALLENGER, 20.0,
        ["Low pricing", "Fast growth"], ["Limited features"]
    )
    landscape = agent.competitive.get_competitive_landscape()
    print(f"\nCompetitive Landscape: {landscape['total_competitors']} competitors")

    # Risk Assessment
    risks = agent.assess_risks([
        {"name": "Market disruption", "category": "market", "probability": 0.3, "impact": 0.8},
        {"name": "Key talent departure", "category": "talent", "probability": 0.4, "impact": 0.6},
    ])
    print(f"Risks: {risks['total_risks']} (exposure: {risks['exposure_score']})")

    # Dashboard
    dashboard = agent.get_strategy_dashboard()
    print(f"\nStrategy Health: {dashboard['health_score']}/100")
    print(f"Objectives: {dashboard['objectives']['total']}")
    print()


if __name__ == "__main__":
    main()

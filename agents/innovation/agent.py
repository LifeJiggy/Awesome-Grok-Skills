"""
Innovation Agent - Comprehensive R&D Management and Innovation Pipeline.

End-to-end innovation management covering idea generation, technology scouting,
patent strategy, experiment design, portfolio optimization, and breakthrough
discovery. Built for corporate innovation labs, R&D departments, and
intrapreneurship programs that need structured pipelines from ideation to
commercialization.

Key Capabilities:
- Idea Capture and Evaluation: Structured intake, scoring matrices, feasibility analysis
- Technology Scouting: Trend detection, competitive intelligence, patent landscape
- R&D Portfolio Management: Resource allocation, stage-gate processes, pipeline health
- Experiment Design: Hypothesis frameworks, A/B protocols, statistical analysis
- Patent Strategy: Filing workflows, prior art search, IP portfolio management
- Innovation Metrics: ROI tracking, velocity measurement, breakthrough rate
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Tuple
from enum import Enum, auto
from datetime import datetime, timedelta
from collections import defaultdict
import json
import hashlib
import math
import uuid
import re
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class IdeaStatus(Enum):
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    IN_DEVELOPMENT = "in_development"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class IdeaCategory(Enum):
    PRODUCT = "product"
    PROCESS = "process"
    BUSINESS_MODEL = "business_model"
    TECHNOLOGY = "technology"
    MARKET = "market"
    SUSTAINABILITY = "sustainability"
    CUSTOMER_EXPERIENCE = "customer_experience"
    OPERATIONAL = "operational"


class InnovationStage(Enum):
    IDEATION = "ideation"
    CONCEPT = "concept"
    VALIDATION = "validation"
    PROTOTYPE = "prototype"
    PILOT = "pilot"
    SCALE = "scale"
    LAUNCH = "launch"
    POST_LAUNCH = "post_launch"


class PatentStatus(Enum):
    IDEA = "idea"
    PRIOR_ART_SEARCH = "prior_art_search"
    DRAFTING = "drafting"
    FILED = "filed"
    PENDING = "pending"
    GRANTED = "granted"
    DENIED = "denied"
    EXPIRED = "expired"
    LICENSABLE = "licensable"


class TechTrendLevel(Enum):
    EMERGING = "emerging"
    GROWING = "growing"
    MAINSTREAM = "mainstream"
    MATURING = "maturing"
    DECLINING = "declining"


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ExperimentStatus(Enum):
    DESIGN = "design"
    APPROVED = "approved"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class PortfolioPriority(Enum):
    EXPLORE = 1
    EXPAND = 2
    EXPLOIT = 3
    EXIT = 4


class FundingSource(Enum):
    INTERNAL = "internal"
    GRANT = "grant"
    VENTURE = "venture"
    STRATEGIC_PARTNER = "strategic_partner"
    CROWDFUND = "crowdfund"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class InnovationIdea:
    """An innovation idea submitted through the pipeline."""
    idea_id: str
    title: str
    description: str
    submitter: str
    category: IdeaCategory
    status: IdeaStatus = IdeaStatus.SUBMITTED
    stage: InnovationStage = InnovationStage.IDEATION
    impact_score: float = 0.0
    feasibility_score: float = 0.0
    alignment_score: float = 0.0
    composite_score: float = 0.0
    tags: List[str] = field(default_factory=list)
    related_patents: List[str] = field(default_factory=list)
    estimated_investment: float = 0.0
    estimated_timeline_months: int = 0
    champion: str = ""
    reviewers: List[str] = field(default_factory=list)
    comments: List[Dict[str, Any]] = field(default_factory=list)
    attachments: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TechnologyTrend:
    """A technology trend being tracked."""
    trend_id: str
    name: str
    description: str
    domain: str
    level: TechTrendLevel
    maturity_percent: float = 0.0
    market_size_estimate: float = 0.0
    growth_rate: float = 0.0
    key_players: List[str] = field(default_factory=list)
    related_patents: List[str] = field(default_factory=list)
    disruption_potential: float = 0.0
    adoption_timeline_years: int = 0
    last_assessed: datetime = field(default_factory=datetime.now)
    sources: List[str] = field(default_factory=list)


@dataclass
class PatentRecord:
    """A patent in the IP portfolio."""
    patent_id: str
    title: str
    description: str
    inventors: List[str]
    filing_date: Optional[datetime] = None
    grant_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    status: PatentStatus = PatentStatus.IDEA
    classification_codes: List[str] = field(default_factory=list)
    jurisdictions: List[str] = field(default_factory=list)
    claims_count: int = 0
    prior_art_references: List[str] = field(default_factory=list)
    citation_count: int = 0
    licensing_revenue: float = 0.0
    estimated_value: float = 0.0
    maintenance_fees_paid: float = 0.0
    renewal_dates: List[datetime] = field(default_factory=list)
    related_trends: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Experiment:
    """A research experiment."""
    experiment_id: str
    name: str
    hypothesis: str
    idea_id: str
    status: ExperimentStatus = ExperimentStatus.DESIGN
    variables: List[Dict[str, Any]] = field(default_factory=list)
    sample_size: int = 100
    duration_days: int = 30
    success_metrics: List[str] = field(default_factory=list)
    control_group: Optional[str] = None
    treatment_groups: List[str] = field(default_factory=list)
    results: Dict[str, Any] = field(default_factory=dict)
    confidence_level: float = 0.95
    budget: float = 0.0
    lead_researcher: str = ""
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    findings: str = ""
    recommendations: List[str] = field(default_factory=list)


@dataclass
class PortfolioProject:
    """A project in the innovation portfolio."""
    project_id: str
    name: str
    idea_id: str
    priority: PortfolioPriority
    stage: InnovationStage
    budget_allocated: float = 0.0
    budget_spent: float = 0.0
    team_members: List[str] = field(default_factory=list)
    start_date: Optional[datetime] = None
    target_launch: Optional[datetime] = None
    progress_percent: float = 0.0
    risk_level: RiskLevel = RiskLevel.MEDIUM
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TechnologyScoutReport:
    """A technology scouting report."""
    report_id: str
    title: str
    scout: str
    domain: str
    summary: str
    trends_identified: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    threats: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    confidence: float = 0.8
    date_conducted: datetime = field(default_factory=datetime.now)
    sources_used: int = 0


# ---------------------------------------------------------------------------
# Scoring Matrices
# ---------------------------------------------------------------------------

class IdeaScoringEngine:
    """Evaluates innovation ideas using multi-dimensional scoring matrices."""

    def __init__(self) -> None:
        self.criteria_weights: Dict[str, float] = {
            "impact": 0.35,
            "feasibility": 0.25,
            "strategic_alignment": 0.20,
            "market_opportunity": 0.12,
            "risk": 0.08,
        }
        self.impact_factors: Dict[str, float] = {
            "revenue_potential": 0.30,
            "market_disruption": 0.25,
            "customer_value": 0.25,
            "operational_efficiency": 0.20,
        }
        self.feasibility_factors: Dict[str, float] = {
            "technical_complexity": 0.30,
            "resource_availability": 0.25,
            "timeline_realism": 0.25,
            "skill_gap": 0.20,
        }

    def set_weights(self, weights: Dict[str, float]) -> None:
        total = sum(weights.values())
        if abs(total - 1.0) > 0.01:
            logger.warning("Weights do not sum to 1.0, normalizing")
            self.criteria_weights = {k: v / total for k, v in weights.items()}
        else:
            self.criteria_weights = weights

    def score_impact(self, factors: Dict[str, float]) -> float:
        score = 0.0
        for factor, weight in self.impact_factors.items():
            value = factors.get(factor, 5.0)
            score += value * weight
        return round(min(10.0, max(0.0, score)), 2)

    def score_feasibility(self, factors: Dict[str, float]) -> float:
        score = 0.0
        for factor, weight in self.feasibility_factors.items():
            value = factors.get(factor, 5.0)
            inverse = 10.0 - value if factor == "technical_complexity" else value
            score += inverse * weight
        return round(min(10.0, max(0.0, score)), 2)

    def score_alignment(self, strategic_fit: float, innovation_goals_fit: float) -> float:
        return round((strategic_fit * 0.6 + innovation_goals_fit * 0.4), 2)

    def score_market_opportunity(self, market_size: float, growth_rate: float,
                                  competition_intensity: float) -> float:
        size_score = min(10.0, math.log10(max(1, market_size)) * 2)
        growth_score = min(10.0, growth_rate * 2)
        competition_score = max(0.0, 10.0 - competition_intensity)
        return round((size_score * 0.4 + growth_score * 0.35 + competition_score * 0.25), 2)

    def score_risk(self, risk_factors: Dict[str, float]) -> float:
        penalty = sum(risk_factors.values()) / max(1, len(risk_factors))
        return round(max(0.0, 10.0 - penalty), 2)

    def calculate_composite(self, idea: InnovationIdea,
                            scoring_data: Dict[str, Any]) -> Dict[str, Any]:
        impact = self.score_impact(scoring_data.get("impact", {}))
        feasibility = self.score_feasibility(scoring_data.get("feasibility", {}))
        alignment = self.score_alignment(
            scoring_data.get("strategic_fit", 5.0),
            scoring_data.get("goals_fit", 5.0),
        )
        market = self.score_market_opportunity(
            scoring_data.get("market_size", 1_000_000),
            scoring_data.get("growth_rate", 5.0),
            scoring_data.get("competition_intensity", 5.0),
        )
        risk = self.score_risk(scoring_data.get("risk", {}))

        composite = (
            impact * self.criteria_weights["impact"]
            + feasibility * self.criteria_weights["feasibility"]
            + alignment * self.criteria_weights["strategic_alignment"]
            + market * self.criteria_weights["market_opportunity"]
            + risk * self.criteria_weights["risk"]
        )

        verdict = "approve" if composite >= 6.0 else "revise" if composite >= 4.0 else "reject"

        return {
            "idea_id": idea.idea_id,
            "scores": {
                "impact": impact,
                "feasibility": feasibility,
                "strategic_alignment": alignment,
                "market_opportunity": market,
                "risk": risk,
            },
            "composite_score": round(composite, 2),
            "verdict": verdict,
            "weight_used": self.criteria_weights,
            "timestamp": datetime.now().isoformat(),
        }

    def rank_ideas(self, ideas: List[Tuple[InnovationIdea, float]]) -> List[Dict[str, Any]]:
        ranked = sorted(ideas, key=lambda x: x[1], reverse=True)
        return [
            {
                "rank": i + 1,
                "idea_id": idea.idea_id,
                "title": idea.title,
                "composite_score": score,
            }
            for i, (idea, score) in enumerate(ranked)
        ]


# ---------------------------------------------------------------------------
# Technology Scouting Engine
# ---------------------------------------------------------------------------

class TechnologyScoutingEngine:
    """Tracks and analyzes technology trends and competitive landscape."""

    def __init__(self) -> None:
        self.trends: Dict[str, TechnologyTrend] = {}
        self.reports: Dict[str, TechnologyScoutReport] = {}
        self.alerts: List[Dict[str, Any]] = []

    def register_trend(self, name: str, description: str, domain: str,
                       level: TechTrendLevel, **kwargs: Any) -> TechnologyTrend:
        trend_id = f"TRD-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        trend = TechnologyTrend(
            trend_id=trend_id,
            name=name,
            description=description,
            domain=domain,
            level=level,
            maturity_percent=kwargs.get("maturity", 0),
            market_size_estimate=kwargs.get("market_size", 0),
            growth_rate=kwargs.get("growth_rate", 0),
            key_players=kwargs.get("players", []),
            disruption_potential=kwargs.get("disruption", 5.0),
            adoption_timeline_years=kwargs.get("adoption_years", 3),
            sources=kwargs.get("sources", []),
        )
        self.trends[trend_id] = trend
        logger.info("Registered trend: %s (%s)", name, trend_id)
        return trend

    def assess_trend(self, trend_id: str, new_level: TechTrendLevel,
                     maturity: float, notes: str = "") -> Dict[str, Any]:
        trend = self.trends.get(trend_id)
        if not trend:
            return {"error": f"Trend {trend_id} not found"}

        old_level = trend.level
        trend.level = new_level
        trend.maturity_percent = maturity
        trend.last_assessed = datetime.now()

        if old_level != new_level:
            alert = {
                "trend_id": trend_id,
                "name": trend.name,
                "old_level": old_level.value,
                "new_level": new_level.value,
                "notes": notes,
                "timestamp": datetime.now().isoformat(),
            }
            self.alerts.append(alert)

        return {
            "trend_id": trend_id,
            "name": trend.name,
            "old_level": old_level.value,
            "new_level": new_level.value,
            "maturity": maturity,
            "alert_generated": old_level != new_level,
        }

    def identify_opportunities(self, domain: str = "",
                                min_disruption: float = 5.0) -> List[Dict[str, Any]]:
        opportunities = []
        for trend in self.trends.values():
            if domain and trend.domain != domain:
                continue
            if trend.disruption_potential >= min_disruption:
                opportunities.append({
                    "trend_id": trend.trend_id,
                    "name": trend.name,
                    "domain": trend.domain,
                    "disruption_potential": trend.disruption_potential,
                    "growth_rate": trend.growth_rate,
                    "market_size": trend.market_size_estimate,
                    "recommendation": self._suggest_action(trend),
                })
        return sorted(opportunities, key=lambda x: x["disruption_potential"], reverse=True)

    def _suggest_action(self, trend: TechnologyTrend) -> str:
        if trend.level == TechTrendLevel.EMERGING:
            return "Invest in R&D to establish early advantage"
        elif trend.level == TechTrendLevel.GROWING:
            return "Accelerate development to capture market share"
        elif trend.level == TechTrendLevel.MAINSTREAM:
            return "Optimize and differentiate to maintain competitive edge"
        elif trend.level == TechTrendLevel.MATURING:
            return "Focus on cost optimization and incremental innovation"
        else:
            return "Consider pivoting resources to emerging opportunities"

    def competitive_landscape(self, competitors: List[Dict[str, Any]]) -> Dict[str, Any]:
        landscape: Dict[str, Any] = {
            "total_competitors": len(competitors),
            "by_threat_level": defaultdict(list),
            "avg_patent_portfolio": 0.0,
            "technology_gaps": [],
            "collaboration_opportunities": [],
        }
        total_patents = 0
        for comp in competitors:
            threat = comp.get("threat_level", "medium")
            landscape["by_threat_level"][threat].append(comp.get("name", "unknown"))
            total_patents += comp.get("patent_count", 0)
            if comp.get("open_to_collab", False):
                landscape["collaboration_opportunities"].append(comp.get("name"))

        if competitors:
            landscape["avg_patent_portfolio"] = round(total_patents / len(competitors), 1)

        landscape["by_threat_level"] = dict(landscape["by_threat_level"])
        return landscape

    def generate_scout_report(self, title: str, scout: str, domain: str,
                               summary: str) -> TechnologyScoutReport:
        report_id = f"RPT-{hashlib.md5(title.encode()).hexdigest()[:8].upper()}"
        domain_trends = [t for t in self.trends.values() if t.domain == domain]
        report = TechnologyScoutReport(
            report_id=report_id,
            title=title,
            scout=scout,
            domain=domain,
            summary=summary,
            trends_identified=[t.trend_id for t in domain_trends],
            opportunities=[
                f"{t.name}: disruption potential {t.disruption_potential}"
                for t in domain_trends if t.disruption_potential >= 6.0
            ],
            sources_used=len(set(s for t in domain_trends for s in t.sources)),
        )
        self.reports[report_id] = report
        return report

    def get_dashboard(self) -> Dict[str, Any]:
        by_level: Dict[str, int] = defaultdict(int)
        for trend in self.trends.values():
            by_level[trend.level.value] += 1
        avg_maturity = (
            sum(t.maturity_percent for t in self.trends.values())
            / max(1, len(self.trends))
        )
        return {
            "total_trends": len(self.trends),
            "by_level": dict(by_level),
            "avg_maturity": round(avg_maturity, 1),
            "total_reports": len(self.reports),
            "pending_alerts": len(self.alerts),
            "top_disruption": sorted(
                self.trends.values(),
                key=lambda t: t.disruption_potential,
                reverse=True,
            )[:5],
        }


# ---------------------------------------------------------------------------
# Patent Portfolio Manager
# ---------------------------------------------------------------------------

class PatentPortfolioManager:
    """Manages patent filings, IP portfolio, and licensing strategy."""

    def __init__(self) -> None:
        self.patents: Dict[str, PatentRecord] = {}
        self.license_agreements: List[Dict[str, Any]] = []
        self.filing_budget: float = 0.0

    def set_budget(self, annual_budget: float) -> None:
        self.filing_budget = annual_budget

    def create_patent(self, title: str, description: str, inventors: List[str],
                      **kwargs: Any) -> PatentRecord:
        patent_id = f"PAT-{hashlib.md5(title.encode()).hexdigest()[:8].upper()}"
        patent = PatentRecord(
            patent_id=patent_id,
            title=title,
            description=description,
            inventors=inventors,
            jurisdictions=kwargs.get("jurisdictions", ["US"]),
            classification_codes=kwargs.get("codes", []),
            estimated_value=kwargs.get("estimated_value", 0),
        )
        self.patents[patent_id] = patent
        logger.info("Created patent record: %s", patent_id)
        return patent

    def update_status(self, patent_id: str, new_status: PatentStatus,
                      notes: str = "") -> Dict[str, Any]:
        patent = self.patents.get(patent_id)
        if not patent:
            return {"error": f"Patent {patent_id} not found"}

        old_status = patent.status
        patent.status = new_status
        if new_status == PatentStatus.FILED:
            patent.filing_date = datetime.now()
        elif new_status == PatentStatus.GRANTED:
            patent.grant_date = datetime.now()
            patent.expiry_date = datetime.now() + timedelta(days=365 * 20)

        return {
            "patent_id": patent_id,
            "old_status": old_status.value,
            "new_status": new_status.value,
            "notes": notes,
        }

    def search_prior_art(self, keywords: List[str],
                         classification: str = "") -> Dict[str, Any]:
        matches = []
        for patent in self.patents.values():
            if classification and classification not in patent.classification_codes:
                continue
            overlap = set(keywords) & set(
                patent.title.lower().split() + patent.description.lower().split()
            )
            if overlap:
                matches.append({
                    "patent_id": patent.patent_id,
                    "title": patent.title,
                    "relevance": len(overlap) / len(keywords),
                    "status": patent.status.value,
                    "filing_date": patent.filing_date.isoformat() if patent.filing_date else None,
                })
        matches.sort(key=lambda x: x["relevance"], reverse=True)
        return {
            "query_keywords": keywords,
            "classification": classification,
            "matches_found": len(matches),
            "results": matches[:20],
        }

    def calculate_portfolio_value(self) -> Dict[str, Any]:
        total_value = sum(p.estimated_value for p in self.patents.values())
        total_costs = sum(p.maintenance_fees_paid for p in self.patents.values())
        revenue = sum(p.licensing_revenue for p in self.patents.values())
        by_status: Dict[str, int] = defaultdict(int)
        for patent in self.patents.values():
            by_status[patent.status.value] += 1
        by_jurisdiction: Dict[str, int] = defaultdict(int)
        for patent in self.patents.values():
            for j in patent.jurisdictions:
                by_jurisdiction[j] += 1
        return {
            "total_patents": len(self.patents),
            "total_estimated_value": round(total_value, 2),
            "total_maintenance_costs": round(total_costs, 2),
            "total_licensing_revenue": round(revenue, 2),
            "net_value": round(total_value - total_costs + revenue, 2),
            "by_status": dict(by_status),
            "by_jurisdiction": dict(by_jurisdiction),
            "avg_claims": round(
                sum(p.claims_count for p in self.patents.values()) / max(1, len(self.patents)), 1
            ),
        }

    def renewal_schedule(self, within_months: int = 6) -> List[Dict[str, Any]]:
        cutoff = datetime.now() + timedelta(days=within_months * 30)
        upcoming = []
        for patent in self.patents.values():
            for renewal in patent.renewal_dates:
                if datetime.now() <= renewal <= cutoff:
                    upcoming.append({
                        "patent_id": patent.patent_id,
                        "title": patent.title,
                        "renewal_date": renewal.isoformat(),
                        "estimated_fee": patent.maintenance_fees_paid * 0.1,
                    })
        return sorted(upcoming, key=lambda x: x["renewal_date"])

    def licensing_opportunities(self) -> List[Dict[str, Any]]:
        return [
            {
                "patent_id": p.patent_id,
                "title": p.title,
                "status": p.status.value,
                "estimated_value": p.estimated_value,
                "current_revenue": p.licensing_revenue,
                "recommendation": (
                    "Active licensing target" if p.estimated_value > 100_000
                    else "Bundle with higher-value patents"
                ),
            }
            for p in self.patents.values()
            if p.status in (PatentStatus.GRANTED, PatentStatus.LICENSABLE)
        ]


# ---------------------------------------------------------------------------
# Experiment Manager
# ---------------------------------------------------------------------------

class ExperimentManager:
    """Designs, runs, and analyzes innovation experiments."""

    def __init__(self) -> None:
        self.experiments: Dict[str, Experiment] = {}
        self.completed_results: List[Dict[str, Any]] = []

    def create_experiment(self, name: str, hypothesis: str, idea_id: str,
                          sample_size: int = 100, duration_days: int = 30,
                          **kwargs: Any) -> Experiment:
        experiment_id = f"EXP-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        experiment = Experiment(
            experiment_id=experiment_id,
            name=name,
            hypothesis=hypothesis,
            idea_id=idea_id,
            sample_size=sample_size,
            duration_days=duration_days,
            success_metrics=kwargs.get("metrics", []),
            budget=kwargs.get("budget", 0),
            lead_researcher=kwargs.get("lead", ""),
            confidence_level=kwargs.get("confidence", 0.95),
        )
        self.experiments[experiment_id] = experiment
        logger.info("Created experiment: %s", experiment_id)
        return experiment

    def start_experiment(self, experiment_id: str) -> Dict[str, Any]:
        exp = self.experiments.get(experiment_id)
        if not exp:
            return {"error": f"Experiment {experiment_id} not found"}
        exp.status = ExperimentStatus.RUNNING
        exp.start_date = datetime.now()
        return {
            "experiment_id": experiment_id,
            "status": "running",
            "start_date": exp.start_date.isoformat(),
            "expected_end": (exp.start_date + timedelta(days=exp.duration_days)).isoformat(),
        }

    def record_result(self, experiment_id: str, metric: str, value: float,
                      group: str = "treatment") -> Dict[str, Any]:
        exp = self.experiments.get(experiment_id)
        if not exp:
            return {"error": f"Experiment {experiment_id} not found"}
        if metric not in exp.results:
            exp.results[metric] = {}
        exp.results[metric][group] = value
        return {
            "experiment_id": experiment_id,
            "metric": metric,
            "group": group,
            "value": value,
        }

    def analyze_results(self, experiment_id: str) -> Dict[str, Any]:
        exp = self.experiments.get(experiment_id)
        if not exp:
            return {"error": f"Experiment {experiment_id} not found"}

        analysis: Dict[str, Any] = {
            "experiment_id": experiment_id,
            "name": exp.name,
            "hypothesis": exp.hypothesis,
            "metrics_analyzed": len(exp.results),
            "detailed_results": {},
        }

        for metric, groups in exp.results.items():
            treatment = groups.get("treatment", 0)
            control = groups.get("control", 0)
            lift = ((treatment - control) / max(0.01, control)) * 100
            significant = abs(lift) > 5.0
            analysis["detailed_results"][metric] = {
                "control": control,
                "treatment": treatment,
                "lift_percent": round(lift, 2),
                "significant": significant,
                "verdict": "supported" if significant and lift > 0 else "not_supported",
            }

        supported = sum(
            1 for r in analysis["detailed_results"].values() if r["verdict"] == "supported"
        )
        analysis["hypothesis_supported"] = supported > 0
        analysis["recommendation"] = (
            "Proceed to next stage" if analysis["hypothesis_supported"]
            else "Iterate hypothesis and retest"
        )

        exp.status = ExperimentStatus.COMPLETED
        exp.end_date = datetime.now()
        self.completed_results.append(analysis)
        return analysis

    def get_pipeline(self) -> Dict[str, Any]:
        by_status: Dict[str, int] = defaultdict(int)
        for exp in self.experiments.values():
            by_status[exp.status.value] += 1
        total_budget = sum(e.budget for e in self.experiments.values())
        spent = sum(e.budget for e in self.experiments.values() if e.status == ExperimentStatus.COMPLETED)
        return {
            "total_experiments": len(self.experiments),
            "by_status": dict(by_status),
            "budget_total": total_budget,
            "budget_spent": spent,
            "completion_rate": round(
                by_status.get("completed", 0) / max(1, len(self.experiments)) * 100, 1
            ),
        }


# ---------------------------------------------------------------------------
# R&D Portfolio Manager
# ---------------------------------------------------------------------------

class RDPortfolioManager:
    """Manages the R&D project portfolio with stage-gate processes."""

    def __init__(self) -> None:
        self.projects: Dict[str, PortfolioProject] = {}
        self.gates: List[Dict[str, Any]] = [
            {"gate": 1, "name": "Idea Screening", "criteria": "Composite score >= 4.0"},
            {"gate": 2, "name": "Business Case", "criteria": "Positive ROI projection"},
            {"gate": 3, "name": "Development Approval", "criteria": "Prototype validated"},
            {"gate": 4, "name": "Pilot Readiness", "criteria": "Pilot plan approved"},
            {"gate": 5, "name": "Scale Decision", "criteria": "Pilot success >= target"},
        ]

    def add_project(self, name: str, idea_id: str,
                    priority: PortfolioPriority, **kwargs: Any) -> PortfolioProject:
        project_id = f"PRJ-{hashlib.md5(name.encode()).hexdigest()[:8].upper()}"
        project = PortfolioProject(
            project_id=project_id,
            name=name,
            idea_id=idea_id,
            priority=priority,
            stage=kwargs.get("stage", InnovationStage.IDEATION),
            budget_allocated=kwargs.get("budget", 0),
            team_members=kwargs.get("team", []),
            target_launch=kwargs.get("target_launch"),
            risk_level=kwargs.get("risk", RiskLevel.MEDIUM),
        )
        self.projects[project_id] = project
        return project

    def advance_stage(self, project_id: str, gate_number: int,
                      approval: bool, notes: str = "") -> Dict[str, Any]:
        project = self.projects.get(project_id)
        if not project:
            return {"error": f"Project {project_id} not found"}

        stage_order = list(InnovationStage)
        current_idx = stage_order.index(project.stage)
        if approval and current_idx < len(stage_order) - 1:
            project.stage = stage_order[current_idx + 1]

        return {
            "project_id": project_id,
            "gate": gate_number,
            "approved": approval,
            "new_stage": project.stage.value,
            "notes": notes,
        }

    def portfolio_summary(self) -> Dict[str, Any]:
        by_stage: Dict[str, int] = defaultdict(int)
        by_priority: Dict[str, int] = defaultdict(int)
        total_budget = 0.0
        total_spent = 0.0
        for project in self.projects.values():
            by_stage[project.stage.value] += 1
            by_priority[project.priority.name] += 1
            total_budget += project.budget_allocated
            total_spent += project.budget_spent
        return {
            "total_projects": len(self.projects),
            "by_stage": dict(by_stage),
            "by_priority": dict(by_priority),
            "budget": {
                "total": total_budget,
                "spent": total_spent,
                "remaining": total_budget - total_spent,
                "utilization": round(total_spent / max(1, total_budget) * 100, 1),
            },
            "avg_progress": round(
                sum(p.progress_percent for p in self.projects.values()) / max(1, len(self.projects)), 1
            ),
        }

    def risk_assessment(self) -> List[Dict[str, Any]]:
        assessments = []
        for project in self.projects.values():
            assessments.append({
                "project_id": project.project_id,
                "name": project.name,
                "risk_level": project.risk_level.value,
                "budget_health": round(
                    (1 - project.budget_spent / max(1, project.budget_allocated)) * 100, 1
                ),
                "on_track": project.progress_percent >= 50 or project.stage != InnovationStage.IDEATION,
            })
        return sorted(assessments, key=lambda x: x["budget_health"])


# ---------------------------------------------------------------------------
# Main Agent
# ---------------------------------------------------------------------------

class InnovationAgent:
    """Orchestrator for the complete innovation management platform."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self.config = config or {}
        self.scoring_engine = IdeaScoringEngine()
        self.scouting_engine = TechnologyScoutingEngine()
        self.patent_manager = PatentPortfolioManager()
        self.experiment_manager = ExperimentManager()
        self.portfolio_manager = RDPortfolioManager()
        self.ideas: Dict[str, InnovationIdea] = {}
        self._initialized_at = datetime.now()
        logger.info("InnovationAgent initialized")

    def submit_idea(self, title: str, description: str, submitter: str,
                    category: IdeaCategory, **kwargs: Any) -> InnovationIdea:
        idea_id = f"IDEA-{hashlib.md5(title.encode()).hexdigest()[:8].upper()}"
        idea = InnovationIdea(
            idea_id=idea_id,
            title=title,
            description=description,
            submitter=submitter,
            category=category,
            tags=kwargs.get("tags", []),
            estimated_investment=kwargs.get("investment", 0),
            estimated_timeline_months=kwargs.get("timeline_months", 0),
        )
        self.ideas[idea_id] = idea
        logger.info("Submitted idea: %s (%s)", title, idea_id)
        return idea

    def evaluate_idea(self, idea_id: str, scoring_data: Dict[str, Any]) -> Dict[str, Any]:
        idea = self.ideas.get(idea_id)
        if not idea:
            return {"error": f"Idea {idea_id} not found"}
        result = self.scoring_engine.calculate_composite(idea, scoring_data)
        idea.impact_score = result["scores"]["impact"]
        idea.feasibility_score = result["scores"]["feasibility"]
        idea.alignment_score = result["scores"]["strategic_alignment"]
        idea.composite_score = result["composite_score"]
        if result["verdict"] == "approve":
            idea.status = IdeaStatus.APPROVED
        elif result["verdict"] == "reject":
            idea.status = IdeaStatus.REJECTED
        else:
            idea.status = IdeaStatus.UNDER_REVIEW
        idea.updated_at = datetime.now()
        return result

    def advance_idea(self, idea_id: str) -> Dict[str, Any]:
        idea = self.ideas.get(idea_id)
        if not idea:
            return {"error": f"Idea {idea_id} not found"}
        stage_order = list(InnovationStage)
        current_idx = stage_order.index(idea.stage)
        if current_idx < len(stage_order) - 1:
            idea.stage = stage_order[current_idx + 1]
            idea.updated_at = datetime.now()
        return {
            "idea_id": idea_id,
            "new_stage": idea.stage.value,
            "title": idea.title,
        }

    def get_dashboard(self) -> Dict[str, Any]:
        by_status: Dict[str, int] = defaultdict(int)
        by_category: Dict[str, int] = defaultdict(int)
        for idea in self.ideas.values():
            by_status[idea.status.value] += 1
            by_category[idea.category.value] += 1

        approved = [i for i in self.ideas.values() if i.status == IdeaStatus.APPROVED]
        avg_score = (
            sum(i.composite_score for i in approved) / max(1, len(approved))
        )

        return {
            "total_ideas": len(self.ideas),
            "by_status": dict(by_status),
            "by_category": dict(by_category),
            "approved_count": len(approved),
            "avg_composite_score": round(avg_score, 2),
            "active_experiments": self.experiment_manager.get_pipeline(),
            "portfolio": self.portfolio_manager.portfolio_summary(),
            "patent_portfolio": self.patent_manager.calculate_portfolio_value(),
            "tech_trends": len(self.scouting_engine.trends),
            "system_uptime": str(datetime.now() - self._initialized_at),
        }

    def full_report(self) -> Dict[str, Any]:
        dashboard = self.get_dashboard()
        dashboard["top_ideas"] = sorted(
            self.ideas.values(), key=lambda i: i.composite_score, reverse=True
        )[:10]
        dashboard["expiring_patents"] = self.patent_manager.renewal_schedule(within_months=6)
        dashboard["licensing_targets"] = self.patent_manager.licensing_opportunities()
        dashboard["portfolio_risks"] = self.portfolio_manager.risk_assessment()
        return dashboard


# ---------------------------------------------------------------------------
# CLI / Demo
# ---------------------------------------------------------------------------

def _demo() -> None:
    """Run a demonstration of the Innovation Agent."""
    agent = InnovationAgent()

    # Submit ideas
    idea1 = agent.submit_idea(
        title="AI-Powered Code Review",
        description="ML model that reviews pull requests for code quality",
        submitter="alice@corp.com",
        category=IdeaCategory.TECHNOLOGY,
        tags=["ai", "developer-tools"],
        investment=150000,
        timeline_months=9,
    )
    idea2 = agent.submit_idea(
        title="Green Data Center Initiative",
        description="Transition 50% of workloads to renewable-energy data centers",
        submitter="bob@corp.com",
        category=IdeaCategory.SUSTAINABILITY,
        tags=["sustainability", "infrastructure"],
        investment=500000,
        timeline_months=18,
    )
    print(f"Submitted {len(agent.ideas)} ideas")

    # Evaluate
    result = agent.evaluate_idea(idea1.idea_id, {
        "impact": {"revenue_potential": 8, "market_disruption": 7, "customer_value": 9, "operational_efficiency": 6},
        "feasibility": {"technical_complexity": 4, "resource_availability": 7, "timeline_realism": 6, "skill_gap": 3},
        "strategic_fit": 8.5,
        "goals_fit": 7.0,
        "market_size": 5_000_000,
        "growth_rate": 15.0,
        "competition_intensity": 6.0,
        "risk": {"technical": 3, "market": 2, "financial": 2},
    })
    print(f"Composite score: {result['composite_score']} -> {result['verdict']}")

    # Register technology trends
    trend = agent.scouting_engine.register_trend(
        name="LLM-Powered Dev Tools",
        description="Large language models integrated into developer workflows",
        domain="software",
        level=TechTrendLevel.GROWING,
        maturity=35, market_size=2_000_000_000, growth_rate=45.0,
        players=["GitHub", "OpenAI", "Google", "Amazon"],
        disruption=8.5, adoption_years=2,
    )
    print(f"Registered trend: {trend.name}")

    # Create patent
    patent = agent.patent_manager.create_patent(
        title="Adaptive Code Review Using Neural Networks",
        description="System for automated code review using transformer models",
        inventors=["Alice Chen", "Bob Park"],
        jurisdictions=["US", "EU"],
        estimated_value=250000,
    )
    agent.patent_manager.update_status(patent.patent_id, PatentStatus.FILED)

    # Create experiment
    exp = agent.experiment_manager.create_experiment(
        name="Code Review Accuracy Test",
        hypothesis="AI reviews catch 30% more bugs than manual review",
        idea_id=idea1.idea_id,
        sample_size=200,
        duration_days=30,
        metrics=["bug_detection_rate", "review_time"],
    )
    agent.experiment_manager.start_experiment(exp.experiment_id)
    agent.experiment_manager.record_result(exp.experiment_id, "bug_detection_rate", 72.0, "treatment")
    agent.experiment_manager.record_result(exp.experiment_id, "bug_detection_rate", 55.0, "control")
    analysis = agent.experiment_manager.analyze_results(exp.experiment_id)
    print(f"Experiment: hypothesis {analysis['hypothesis_supported'] and 'supported' or 'not supported'}")

    # Dashboard
    dashboard = agent.get_dashboard()
    print(f"\nDashboard: {json.dumps(dashboard, indent=2, default=str)}")


if __name__ == "__main__":
    _demo()

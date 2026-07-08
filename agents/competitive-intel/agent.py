"""
Competitive Intelligence Agent - Market and Competitor Analysis.

Provides comprehensive competitive analysis, market intelligence gathering,
SWOT analysis, competitor tracking, trend monitoring, and strategic benchmarking.
Supports data collection from multiple sources, trend detection,
and actionable intelligence generation for strategic decision-making.
"""

from __future__ import annotations

import logging
import uuid
import json
import hashlib
import math
import re
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Tuple, Set, Union
from collections import defaultdict

logger = logging.getLogger(__name__)


# =============================================================================
# Enumerations
# =============================================================================

class MarketSegment(Enum):
    """Market segmentation categories."""
    ENTERPRISE = "enterprise"
    SMB = "smb"
    CONSUMER = "consumer"
    GOVERNMENT = "government"
    EDUCATION = "education"
    HEALTHCARE = "healthcare"
    FINTECH = "fintech"
    ECOMMERCE = "ecommerce"
    SAAS = "saas"
    INFRASTRUCTURE = "infrastructure"


class CompetitorType(Enum):
    """Types of competitors."""
    DIRECT = "direct"
    INDIRECT = "indirect"
    POTENTIAL = "potential"
    SUBSTITUTE = "substitute"
    EMERGING = "emerging"


class IntelSource(Enum):
    """Sources of competitive intelligence."""
    WEBSITE = "website"
    PRESS_RELEASE = "press_release"
    EARNINGS_CALL = "earnings_call"
    PATENT_FILING = "patent_filing"
    JOB_POSTING = "job_posting"
    SOCIAL_MEDIA = "social_media"
    NEWS_ARTICLE = "news_article"
    INDUSTRY_REPORT = "industry_report"
    CUSTOMER_REVIEW = "customer_review"
    CONFERENCE = "conference"
    REGULATORY_FILING = "regulatory_filing"
    PATENT = "patent"
    PARTNERSHIP = "partnership"
    GITHUB = "github"
    CRUNCHBASE = "crunchbase"
    LINKEDIN = "linkedin"
    GLASSDOOR = "glassdoor"
    BLOG = "blog"
    WHITEPAPER = "whitepaper"
    ANALYST_REPORT = "analyst_report"


class TrendDirection(Enum):
    """Direction of a market trend."""
    RISING = "rising"
    STABLE = "stable"
    DECLINING = "declining"
    EMERGING = "emerging"
    DISRUPTIVE = "disruptive"


class ThreatLevel(Enum):
    """Threat level of a competitor or trend."""
    NEGLIGIBLE = "negligible"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnalysisType(Enum):
    """Types of competitive analysis."""
    SWOT = "swot"
    PORTER_FIVE_FORCES = "porter_five_forces"
    PESTEL = "pestel"
    VALUE_CHAIN = "value_chain"
    BENCHMARKING = "benchmarking"
    MARKET_SIZING = "market_sizing"
    TREND_ANALYSIS = "trend_analysis"
    COMPETITIVE_LANDSCAPE = "competitive_landscape"
    CUSTOMER_SENTIMENT = "customer_sentiment"
    PRICING_ANALYSIS = "pricing_analysis"
    FEATURE_COMPARISON = "feature_comparison"
    TECHNOLOGY_RADAR = "technology_radar"


class ConfidenceLevel(Enum):
    """Confidence level in intelligence data."""
    SPECULATIVE = "speculative"
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERIFIED = "verified"


class DataFreshness(Enum):
    """Freshness of intelligence data."""
    REAL_TIME = "real_time"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUAL = "annual"
    STALE = "stale"


class SentimentType(Enum):
    """Sentiment classifications for intelligence."""
    VERY_POSITIVE = "very_positive"
    POSITIVE = "positive"
    NEUTRAL = "neutral"
    NEGATIVE = "negative"
    VERY_NEGATIVE = "very_negative"


class IntelPriority(Enum):
    """Priority levels for intelligence reports."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class CompetitorProfile:
    """Comprehensive profile of a competitor."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    competitor_type: CompetitorType = CompetitorType.DIRECT
    website: str = ""
    headquarters: str = ""
    founded_year: int = 0
    employee_count: int = 0
    annual_revenue: float = 0.0
    revenue_currency: str = "USD"
    funding_total: float = 0.0
    last_funding_round: str = ""
    valuation: float = 0.0
    market_segments: List[MarketSegment] = field(default_factory=list)
    products: List[str] = field(default_factory=list)
    services: List[str] = field(default_factory=list)
    technologies: List[str] = field(default_factory=list)
    key_executives: List[Dict[str, str]] = field(default_factory=list)
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recent_moves: List[Dict[str, Any]] = field(default_factory=list)
    threat_level: ThreatLevel = ThreatLevel.MEDIUM
    notes: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "competitor_type": self.competitor_type.value,
            "website": self.website,
            "headquarters": self.headquarters,
            "founded_year": self.founded_year,
            "employee_count": self.employee_count,
            "annual_revenue": self.annual_revenue,
            "funding_total": self.funding_total,
            "valuation": self.valuation,
            "market_segments": [s.value for s in self.market_segments],
            "products": self.products,
            "services": self.services,
            "technologies": self.technologies,
            "key_executives": self.key_executives,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "recent_moves": self.recent_moves,
            "threat_level": self.threat_level.value,
            "tags": self.tags,
        }


@dataclass
class IntelReport:
    """A single intelligence report or data point."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    title: str = ""
    summary: str = ""
    source: IntelSource = IntelSource.NEWS_ARTICLE
    source_url: str = ""
    competitor_id: str = ""
    competitor_name: str = ""
    category: str = ""
    sentiment: str = "neutral"
    confidence: ConfidenceLevel = ConfidenceLevel.MODERATE
    freshness: DataFreshness = DataFreshness.WEEKLY
    tags: List[str] = field(default_factory=list)
    key_findings: List[str] = field(default_factory=list)
    strategic_implications: List[str] = field(default_factory=list)
    published_date: Optional[datetime] = None
    collected_at: datetime = field(default_factory=datetime.utcnow)
    verified: bool = False
    priority: IntelPriority = IntelPriority.MEDIUM

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "summary": self.summary,
            "source": self.source.value,
            "source_url": self.source_url,
            "competitor_id": self.competitor_id,
            "competitor_name": self.competitor_name,
            "category": self.category,
            "sentiment": self.sentiment,
            "confidence": self.confidence.value,
            "freshness": self.freshness.value,
            "tags": self.tags,
            "key_findings": self.key_findings,
            "strategic_implications": self.strategic_implications,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "collected_at": self.collected_at.isoformat(),
            "verified": self.verified,
            "priority": self.priority.value,
        }


@dataclass
class MarketTrend:
    """A detected market trend."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    name: str = ""
    description: str = ""
    direction: TrendDirection = TrendDirection.STABLE
    impact_score: float = 0.5
    timeframe_months: int = 12
    affected_segments: List[MarketSegment] = field(default_factory=list)
    key_drivers: List[str] = field(default_factory=list)
    evidence: List[str] = field(default_factory=list)
    affected_competitors: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    threats: List[str] = field(default_factory=list)
    confidence: ConfidenceLevel = ConfidenceLevel.MODERATE
    detected_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "direction": self.direction.value,
            "impact_score": self.impact_score,
            "timeframe_months": self.timeframe_months,
            "affected_segments": [s.value for s in self.affected_segments],
            "key_drivers": self.key_drivers,
            "evidence": self.evidence,
            "affected_competitors": self.affected_competitors,
            "opportunities": self.opportunities,
            "threats": self.threats,
            "confidence": self.confidence.value,
            "detected_at": self.detected_at.isoformat(),
        }


@dataclass
class SWOTAnalysis:
    """SWOT analysis for a company or product."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    subject: str = ""
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    opportunities: List[str] = field(default_factory=list)
    threats: List[str] = field(default_factory=list)
    internal_factors: Dict[str, List[str]] = field(default_factory=dict)
    external_factors: Dict[str, List[str]] = field(default_factory=dict)
    strategic_priority: str = ""
    overall_score: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "subject": self.subject,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
            "opportunities": self.opportunities,
            "threats": self.threats,
            "internal_factors": self.internal_factors,
            "external_factors": self.external_factors,
            "strategic_priority": self.strategic_priority,
            "overall_score": self.overall_score,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class BenchmarkMetric:
    """A benchmark comparison metric."""
    metric_name: str = ""
    our_value: float = 0.0
    competitor_values: Dict[str, float] = field(default_factory=dict)
    industry_average: float = 0.0
    unit: str = ""
    higher_is_better: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metric_name": self.metric_name,
            "our_value": self.our_value,
            "competitor_values": self.competitor_values,
            "industry_average": self.industry_average,
            "unit": self.unit,
            "higher_is_better": self.higher_is_better,
        }

    def rank(self) -> List[Tuple[str, float]]:
        all_values = [("our_company", self.our_value)]
        all_values.extend(self.competitor_values.items())
        all_values.append(("industry_average", self.industry_average))
        if self.higher_is_better:
            all_values.sort(key=lambda x: x[1], reverse=True)
        else:
            all_values.sort(key=lambda x: x[1])
        return all_values


@dataclass
class CompetitiveLandscape:
    """A snapshot of the competitive landscape."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    market: str = ""
    segment: Optional[MarketSegment] = None
    competitors: List[CompetitorProfile] = field(default_factory=list)
    market_size: float = 0.0
    market_growth_rate: float = 0.0
    concentration: str = ""
    entry_barriers: List[str] = field(default_factory=list)
    key_success_factors: List[str] = field(default_factory=list)
    our_position: str = ""
    our_market_share: float = 0.0
    created_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "market": self.market,
            "segment": self.segment.value if self.segment else None,
            "competitor_count": len(self.competitors),
            "competitors": [c.to_dict() for c in self.competitors],
            "market_size": self.market_size,
            "market_growth_rate": self.market_growth_rate,
            "concentration": self.concentration,
            "entry_barriers": self.entry_barriers,
            "key_success_factors": self.key_success_factors,
            "our_position": self.our_position,
            "our_market_share": self.our_market_share,
        }


@dataclass
class FeatureComparison:
    """Feature comparison between our product and competitors."""
    product_name: str = ""
    features: List[Dict[str, Any]] = field(default_factory=list)
    competitors: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_name": self.product_name,
            "features": self.features,
            "competitors": self.competitors,
        }


@dataclass
class PricingAnalysis:
    """Pricing comparison analysis."""
    product_name: str = ""
    our_price: float = 0.0
    competitor_prices: Dict[str, float] = field(default_factory=dict)
    price_tiers: List[Dict[str, Any]] = field(default_factory=list)
    positioning: str = ""
    value_proposition: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_name": self.product_name,
            "our_price": self.our_price,
            "competitor_prices": self.competitor_prices,
            "price_tiers": self.price_tiers,
            "positioning": self.positioning,
            "value_proposition": self.value_proposition,
        }


# =============================================================================
# SWOT Analyzer
# =============================================================================

class SWOTAnalyzer:
    """
    Performs structured SWOT analysis for companies and products.

    Gathers data from multiple sources and produces comprehensive
    internal/external factor assessments with strategic recommendations.
    """

    def __init__(self) -> None:
        self._analyses: Dict[str, SWOTAnalysis] = {}
        self._factor_library: Dict[str, List[str]] = {
            "technology_strengths": [
                "Advanced ML/AI capabilities",
                "Proprietary data advantage",
                "Scalable cloud architecture",
                "Strong API ecosystem",
                "Real-time processing capability",
                "Robust security infrastructure",
                "Microservices architecture",
                "Strong DevOps practices",
            ],
            "technology_weaknesses": [
                "Legacy technology debt",
                "Limited mobile experience",
                "High infrastructure costs",
                "Vendor lock-in concerns",
                "Insufficient automated testing",
                "Poor documentation practices",
            ],
            "market_opportunities": [
                "Growing market demand",
                "Underserved segments",
                "Geographic expansion",
                "Partnership potential",
                "Regulatory changes creating new demand",
                "Technology convergence creating new use cases",
                "Adjacent market entry",
            ],
            "market_threats": [
                "New entrants with disruptive models",
                "Regulatory tightening",
                "Economic downturn impact",
                "Technology shift obsolescence",
                "Customer consolidation reducing buyer count",
                "Open source alternatives gaining traction",
                "Platform dependency risk",
            ],
        }

    def analyze(
        self,
        subject: str,
        strengths: Optional[List[str]] = None,
        weaknesses: Optional[List[str]] = None,
        opportunities: Optional[List[str]] = None,
        threats: Optional[List[str]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> SWOTAnalysis:
        """Perform a SWOT analysis."""
        analysis = SWOTAnalysis(subject=subject)

        if strengths:
            analysis.strengths = strengths
        else:
            analysis.strengths = self._infer_strengths(context or {})

        if weaknesses:
            analysis.weaknesses = weaknesses
        else:
            analysis.weaknesses = self._infer_weaknesses(context or {})

        if opportunities:
            analysis.opportunities = opportunities
        else:
            analysis.opportunities = self._infer_opportunities(context or {})

        if threats:
            analysis.threats = threats
        else:
            analysis.threats = self._infer_threats(context or {})

        analysis.internal_factors = {
            "strengths": analysis.strengths,
            "weaknesses": analysis.weaknesses,
        }
        analysis.external_factors = {
            "opportunities": analysis.opportunities,
            "threats": analysis.threats,
        }

        analysis.overall_score = self._calculate_swot_score(analysis)
        analysis.strategic_priority = self._determine_priority(analysis)

        self._analyses[analysis.id] = analysis
        logger.info("SWOT analysis completed for %s (score: %.3f)", subject, analysis.overall_score)
        return analysis

    def compare_swot(self, analysis_ids: List[str]) -> Dict[str, Any]:
        """Compare SWOT analyses across multiple subjects."""
        analyses = [self._analyses.get(aid) for aid in analysis_ids]
        analyses = [a for a in analyses if a is not None]

        if len(analyses) < 2:
            return {"error": "Need at least 2 analyses to compare"}

        comparison = {
            "subjects": [a.subject for a in analyses],
            "scores": {a.subject: a.overall_score for a in analyses},
            "strength_comparison": {},
            "weakness_comparison": {},
        }

        max_strengths = max(analyses, key=lambda a: len(a.strengths))
        max_weaknesses = max(analyses, key=lambda a: len(a.weaknesses))

        comparison["strongest_subject"] = max_strengths.subject
        comparison["most_weaknesses"] = max_weaknesses.subject
        comparison["highest_score"] = max(analyses, key=lambda a: a.overall_score).subject

        return comparison

    def get_strategic_recommendations(self, analysis_id: str) -> Dict[str, Any]:
        """Generate strategic recommendations from SWOT analysis."""
        analysis = self._analyses.get(analysis_id)
        if not analysis:
            return {"error": f"Analysis {analysis_id} not found"}

        recommendations = {
            "so_strategies": [],
            "wo_strategies": [],
            "st_strategies": [],
            "wt_strategies": [],
        }

        for s in analysis.strengths[:3]:
            for o in analysis.opportunities[:3]:
                recommendations["so_strategies"].append(
                    f"Leverage '{s}' to capitalize on '{o}'"
                )

        for w in analysis.weaknesses[:3]:
            for o in analysis.opportunities[:3]:
                recommendations["wo_strategies"].append(
                    f"Address '{w}' to better pursue '{o}'"
                )

        for s in analysis.strengths[:3]:
            for t in analysis.threats[:3]:
                recommendations["st_strategies"].append(
                    f"Use '{s}' to mitigate '{t}'"
                )

        for w in analysis.weaknesses[:3]:
            for t in analysis.threats[:3]:
                recommendations["wt_strategies"].append(
                    f"Minimize '{w}' to reduce vulnerability to '{t}'"
                )

        return {
            "analysis_id": analysis_id,
            "subject": analysis.subject,
            "overall_score": analysis.overall_score,
            "strategic_priority": analysis.strategic_priority,
            "recommendations": recommendations,
        }

    def _calculate_swot_score(self, analysis: SWOTAnalysis) -> float:
        positive = len(analysis.strengths) + len(analysis.opportunities)
        negative = len(analysis.weaknesses) + len(analysis.threats)
        total = positive + negative
        if total == 0:
            return 0.5
        return round(positive / total, 3)

    def _determine_priority(self, analysis: SWOTAnalysis) -> str:
        score = analysis.overall_score
        if score >= 0.7:
            return "offensive - leverage strengths to capture opportunities"
        if score >= 0.5:
            return "competitive - optimize strengths while addressing weaknesses"
        if score >= 0.3:
            return "defensive - focus on mitigating threats and weaknesses"
        return "survival - urgent restructuring needed"

    def _infer_strengths(self, context: Dict[str, Any]) -> List[str]:
        return self._factor_library["technology_strengths"][:3]

    def _infer_weaknesses(self, context: Dict[str, Any]) -> List[str]:
        return self._factor_library["technology_weaknesses"][:2]

    def _infer_opportunities(self, context: Dict[str, Any]) -> List[str]:
        return self._factor_library["market_opportunities"][:3]

    def _infer_threats(self, context: Dict[str, Any]) -> List[str]:
        return self._factor_library["market_threats"][:3]


# =============================================================================
# Trend Monitor
# =============================================================================

class TrendMonitor:
    """
    Monitors and detects market trends from collected intelligence.

    Analyzes patterns across multiple data points to identify
    emerging, growing, or declining trends.
    """

    def __init__(self) -> None:
        self._trends: Dict[str, MarketTrend] = {}
        self._data_points: List[Dict[str, Any]] = []

    def add_data_point(
        self,
        topic: str,
        source: str,
        content: str,
        sentiment: str = "neutral",
        timestamp: Optional[datetime] = None,
    ) -> None:
        """Add a data point for trend analysis."""
        self._data_points.append({
            "topic": topic,
            "source": source,
            "content": content,
            "sentiment": sentiment,
            "timestamp": (timestamp or datetime.utcnow()).isoformat(),
        })

    def detect_trends(
        self, topics: Optional[List[str]] = None, min_data_points: int = 3
    ) -> List[MarketTrend]:
        """Detect trends from collected data points."""
        filtered = self._data_points
        if topics:
            filtered = [dp for dp in filtered if dp["topic"] in topics]

        topic_groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for dp in filtered:
            topic_groups[dp["topic"]].append(dp)

        detected: List[MarketTrend] = []

        for topic, points in topic_groups.items():
            if len(points) < min_data_points:
                continue

            sentiment_counts = defaultdict(int)
            for p in points:
                sentiment_counts[p["sentiment"]] += 1

            total = len(points)
            positive_ratio = sentiment_counts.get("positive", 0) / total
            negative_ratio = sentiment_counts.get("negative", 0) / total

            if positive_ratio > 0.6:
                direction = TrendDirection.RISING
            elif negative_ratio > 0.6:
                direction = TrendDirection.DECLINING
            elif positive_ratio > 0.4 and negative_ratio < 0.2:
                direction = TrendDirection.EMERGING
            else:
                direction = TrendDirection.STABLE

            trend = MarketTrend(
                name=topic,
                description=f"Trend detected from {total} data points across {len(set(p['source'] for p in points))} sources",
                direction=direction,
                impact_score=round(abs(positive_ratio - negative_ratio), 3),
                confidence=ConfidenceLevel.HIGH if total >= 10 else ConfidenceLevel.MODERATE,
                key_drivers=[f"Detected from {total} intelligence reports"],
            )

            self._trends[trend.id] = trend
            detected.append(trend)

        return detected

    def get_trend(self, trend_id: str) -> Optional[Dict[str, Any]]:
        trend = self._trends.get(trend_id)
        return trend.to_dict() if trend else None

    def list_trends(
        self, direction_filter: Optional[TrendDirection] = None
    ) -> List[Dict[str, Any]]:
        trends = list(self._trends.values())
        if direction_filter:
            trends = [t for t in trends if t.direction == direction_filter]
        return [t.to_dict() for t in trends]

    def get_trend_summary(self) -> Dict[str, Any]:
        """Summarize all detected trends."""
        if not self._trends:
            return {"total_trends": 0, "by_direction": {}}

        by_direction: Dict[str, int] = defaultdict(int)
        for t in self._trends.values():
            by_direction[t.direction.value] += 1

        return {
            "total_trends": len(self._trends),
            "by_direction": dict(by_direction),
            "total_data_points": len(self._data_points),
            "average_impact": round(
                sum(t.impact_score for t in self._trends.values()) / len(self._trends), 3
            ),
        }


# =============================================================================
# Benchmark Engine
# =============================================================================

class BenchmarkEngine:
    """
    Performs competitive benchmarking across multiple metrics.

    Compares our performance, features, and positioning against
    competitors and industry averages.
    """

    def __init__(self) -> None:
        self._benchmarks: Dict[str, List[BenchmarkMetric]] = defaultdict(list)
        self._feature_comparisons: Dict[str, FeatureComparison] = {}
        self._pricing_analyses: Dict[str, PricingAnalysis] = {}

    def add_metric(
        self,
        category: str,
        metric_name: str,
        our_value: float,
        competitor_values: Dict[str, float],
        industry_average: float = 0.0,
        unit: str = "",
        higher_is_better: bool = True,
    ) -> BenchmarkMetric:
        """Add a benchmark metric."""
        metric = BenchmarkMetric(
            metric_name=metric_name,
            our_value=our_value,
            competitor_values=competitor_values,
            industry_average=industry_average,
            unit=unit,
            higher_is_better=higher_is_better,
        )
        self._benchmarks[category].append(metric)
        return metric

    def get_rankings(self, category: str) -> List[Dict[str, Any]]:
        """Get rankings for a benchmark category."""
        metrics = self._benchmarks.get(category, [])
        results = []
        for metric in metrics:
            ranking = metric.rank()
            our_rank = next(
                (i + 1 for i, (name, _) in enumerate(ranking) if name == "our_company"),
                len(ranking),
            )
            results.append({
                "metric": metric.metric_name,
                "our_rank": our_rank,
                "our_value": metric.our_value,
                "total_competitors": len(metric.competitor_values),
                "ranking": [(name, val) for name, val in ranking],
            })
        return results

    def competitive_score(self, category: str) -> Dict[str, Any]:
        """Calculate overall competitive score for a category."""
        metrics = self._benchmarks.get(category, [])
        if not metrics:
            return {"category": category, "score": 0.0, "rank": "unknown"}

        total_rank = 0
        total_metrics = len(metrics)
        for metric in metrics:
            ranking = metric.rank()
            our_pos = next(
                (i for i, (name, _) in enumerate(ranking) if name == "our_company"),
                len(ranking),
            )
            normalized = 1.0 - (our_pos / max(len(ranking) - 1, 1))
            total_rank += normalized

        score = round(total_rank / total_metrics, 3) if total_metrics > 0 else 0.0

        if score >= 0.8:
            position = "market_leader"
        elif score >= 0.6:
            position = "strong_contender"
        elif score >= 0.4:
            position = "competitive"
        elif score >= 0.2:
            position = "challenger"
        else:
            position = "laggard"

        return {
            "category": category,
            "score": score,
            "position": position,
            "metrics_evaluated": total_metrics,
        }

    def compare_features(
        self,
        product_name: str,
        features: List[Dict[str, Any]],
        competitors: List[str],
    ) -> FeatureComparison:
        """Create a feature comparison matrix."""
        comparison = FeatureComparison(
            product_name=product_name,
            features=features,
            competitors=competitors,
        )
        self._feature_comparisons[product_name] = comparison
        return comparison

    def analyze_pricing(
        self,
        product_name: str,
        our_price: float,
        competitor_prices: Dict[str, float],
        tiers: Optional[List[Dict[str, Any]]] = None,
    ) -> PricingAnalysis:
        """Analyze pricing relative to competitors."""
        avg_competitor = (
            sum(competitor_prices.values()) / len(competitor_prices)
            if competitor_prices
            else 0.0
        )

        if our_price < avg_competitor * 0.8:
            positioning = "aggressive_pricer"
        elif our_price > avg_competitor * 1.2:
            positioning = "premium_pricer"
        else:
            positioning = "market_rate"

        analysis = PricingAnalysis(
            product_name=product_name,
            our_price=our_price,
            competitor_prices=competitor_prices,
            price_tiers=tiers or [],
            positioning=positioning,
        )
        self._pricing_analyses[product_name] = analysis
        return analysis

    def get_benchmark_summary(self) -> Dict[str, Any]:
        total_metrics = sum(len(m) for m in self._benchmarks.values())
        return {
            "categories": list(self._benchmarks.keys()),
            "total_metrics": total_metrics,
            "feature_comparisons": len(self._feature_comparisons),
            "pricing_analyses": len(self._pricing_analyses),
        }


# =============================================================================
# Intelligence Collector
# =============================================================================

class IntelligenceCollector:
    """
    Collects and manages competitive intelligence from various sources.

    Provides structured ingestion, categorization, and retrieval of
    intelligence reports with full-text search capabilities.
    """

    def __init__(self) -> None:
        self._reports: Dict[str, IntelReport] = {}
        self._by_competitor: Dict[str, List[str]] = defaultdict(list)
        self._by_source: Dict[str, List[str]] = defaultdict(list)
        self._by_category: Dict[str, List[str]] = defaultdict(list)

    def collect(
        self,
        title: str,
        summary: str,
        source: str,
        competitor_name: str = "",
        category: str = "",
        source_url: str = "",
        confidence: str = "moderate",
        key_findings: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        priority: str = "medium",
    ) -> IntelReport:
        """Collect a new intelligence report."""
        src = IntelSource(source) if source in [e.value for e in IntelSource] else IntelSource.NEWS_ARTICLE
        conf = ConfidenceLevel(confidence) if confidence in [e.value for e in ConfidenceLevel] else ConfidenceLevel.MODERATE
        pri = IntelPriority(priority) if priority in [e.value for e in IntelPriority] else IntelPriority.MEDIUM

        report = IntelReport(
            title=title,
            summary=summary,
            source=src,
            source_url=source_url,
            competitor_name=competitor_name,
            category=category,
            confidence=conf,
            key_findings=key_findings or [],
            tags=tags or [],
            priority=pri,
        )

        self._reports[report.id] = report
        self._by_competitor[competitor_name.lower()].append(report.id)
        self._by_source[src.value].append(report.id)
        if category:
            self._by_category[category.lower()].append(report.id)

        return report

    def search(
        self,
        keyword: str = "",
        competitor: str = "",
        category: str = "",
        source: str = "",
        limit: int = 20,
    ) -> List[Dict[str, Any]]:
        """Search intelligence reports with filters."""
        results = list(self._reports.values())

        if keyword:
            kw = keyword.lower()
            results = [
                r for r in results
                if kw in r.title.lower()
                or kw in r.summary.lower()
                or any(kw in f.lower() for f in r.key_findings)
                or any(kw in t.lower() for t in r.tags)
            ]

        if competitor:
            results = [
                r for r in results
                if competitor.lower() in r.competitor_name.lower()
            ]

        if category:
            results = [r for r in results if r.category.lower() == category.lower()]

        if source:
            results = [r for r in results if r.source.value == source]

        results.sort(key=lambda r: r.collected_at, reverse=True)
        return [r.to_dict() for r in results[:limit]]

    def get_latest(
        self, competitor: str, limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Get latest intelligence for a competitor."""
        report_ids = self._by_competitor.get(competitor.lower(), [])
        reports = [self._reports[rid] for rid in report_ids if rid in self._reports]
        reports.sort(key=lambda r: r.collected_at, reverse=True)
        return [r.to_dict() for r in reports[:limit]]

    def get_stats(self) -> Dict[str, Any]:
        by_source = {k: len(v) for k, v in self._by_source.items()}
        by_competitor = {k: len(v) for k, v in self._by_competitor.items()}
        return {
            "total_reports": len(self._reports),
            "by_source": by_source,
            "by_competitor": by_competitor,
            "categories": list(self._by_category.keys()),
        }


# =============================================================================
# Market Research Engine
# =============================================================================

class MarketResearchEngine:
    """
    Conducts structured market research and landscape analysis.

    Combines competitor data, market sizing, and trend information
    to produce actionable market research reports.
    """

    def __init__(self) -> None:
        self._research_reports: Dict[str, Dict[str, Any]] = {}

    def size_market(
        self,
        market: str,
        total_addressable_market: float,
        growth_rate: float,
        segments: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Estimate market sizing with TAM/SAM/SOM."""
        sam = total_addressable_market * 0.3
        som = sam * 0.1

        report = {
            "market": market,
            "tam": total_addressable_market,
            "sam": round(sam, 2),
            "som": round(som, 2),
            "growth_rate": growth_rate,
            "segments": segments or [],
            "projected_value_3yr": round(
                total_addressable_market * ((1 + growth_rate) ** 3), 2
            ),
            "created_at": datetime.utcnow().isoformat(),
        }

        self._research_reports[market] = report
        return report

    def analyze_entry_barriers(
        self, market: str, barriers: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze market entry barriers."""
        severity_scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        total_severity = sum(
            severity_scores.get(b.get("severity", "medium"), 2) for b in barriers
        )
        avg_severity = total_severity / max(len(barriers), 1)

        return {
            "market": market,
            "barriers": barriers,
            "total_barriers": len(barriers),
            "average_severity": round(avg_severity, 2),
            "feasibility": "high" if avg_severity < 1.5 else "medium" if avg_severity < 2.5 else "low",
        }

    def get_research_summary(self) -> Dict[str, Any]:
        return {
            "total_reports": len(self._research_reports),
            "markets": list(self._research_reports.keys()),
        }


# =============================================================================
# Main Competitive Intelligence Agent
# =============================================================================

class CompetitiveIntelAgent:
    """
    Primary orchestrator for competitive intelligence and market analysis.

    Coordinates competitor tracking, SWOT analysis, trend monitoring,
    benchmarking, intelligence collection, and strategic insights
    generation into a unified competitive intelligence workflow.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        self._config = config or {}
        self._competitors: Dict[str, CompetitorProfile] = {}
        self._landscapes: Dict[str, CompetitiveLandscape] = {}
        self._swot_analyzer = SWOTAnalyzer()
        self._trend_monitor = TrendMonitor()
        self._benchmark_engine = BenchmarkEngine()
        self._intel_collector = IntelligenceCollector()
        self._market_research = MarketResearchEngine()
        self._analyses: Dict[str, Dict[str, Any]] = {}
        self._created_at = datetime.utcnow()

        logger.info("CompetitiveIntelAgent initialized")

    def add_competitor(
        self,
        name: str,
        competitor_type: str = "direct",
        website: str = "",
        headquarters: str = "",
        employee_count: int = 0,
        annual_revenue: float = 0.0,
        products: Optional[List[str]] = None,
        technologies: Optional[List[str]] = None,
        strengths: Optional[List[str]] = None,
        weaknesses: Optional[List[str]] = None,
        threat_level: str = "medium",
        tags: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Add a competitor to track."""
        ct = CompetitorType(competitor_type) if competitor_type in [e.value for e in CompetitorType] else CompetitorType.DIRECT
        tl = ThreatLevel(threat_level) if threat_level in [e.value for e in ThreatLevel] else ThreatLevel.MEDIUM

        profile = CompetitorProfile(
            name=name,
            competitor_type=ct,
            website=website,
            headquarters=headquarters,
            employee_count=employee_count,
            annual_revenue=annual_revenue,
            products=products or [],
            technologies=technologies or [],
            strengths=strengths or [],
            weaknesses=weaknesses or [],
            threat_level=tl,
            tags=tags or [],
        )

        self._competitors[profile.id] = profile
        logger.info("Competitor added: %s (%s)", name, profile.id)

        return {
            "competitor_id": profile.id,
            "name": name,
            "type": ct.value,
            "threat_level": tl.value,
        }

    def analyze_competitor(
        self,
        competitor_id: str,
        additional_data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Perform comprehensive analysis of a competitor."""
        profile = self._competitors.get(competitor_id)
        if not profile:
            return {"error": f"Competitor {competitor_id} not found"}

        swot = self._swot_analyzer.analyze(
            subject=profile.name,
            strengths=profile.strengths,
            weaknesses=profile.weaknesses,
            context=additional_data or {},
        )

        latest_intel = self._intel_collector.get_latest(profile.name, limit=10)

        analysis = {
            "competitor": profile.to_dict(),
            "swot": swot.to_dict(),
            "recent_intelligence": latest_intel,
            "threat_assessment": self._assess_threat(profile),
            "competitive_positioning": self._assess_positioning(profile),
            "analyzed_at": datetime.utcnow().isoformat(),
        }

        self._analyses[competitor_id] = analysis
        return analysis

    def conduct_market_research(
        self,
        market: str,
        segment: Optional[str] = None,
        competitors: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Conduct market research for a specific market."""
        seg = MarketSegment(segment) if segment and segment in [e.value for e in MarketSegment] else None

        landscape = CompetitiveLandscape(
            market=market,
            segment=seg,
            competitors=[
                self._competitors[cid]
                for cid in (competitors or [])
                if cid in self._competitors
            ],
        )

        self._landscapes[landscape.id] = landscape

        return {
            "landscape_id": landscape.id,
            "market": market,
            "segment": segment,
            "competitor_count": len(landscape.competitors),
            "market_size": landscape.market_size,
            "created_at": landscape.created_at.isoformat(),
        }

    def perform_swot(
        self,
        subject: str,
        strengths: Optional[List[str]] = None,
        weaknesses: Optional[List[str]] = None,
        opportunities: Optional[List[str]] = None,
        threats: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Perform a SWOT analysis."""
        analysis = self._swot_analyzer.analyze(
            subject=subject,
            strengths=strengths,
            weaknesses=weaknesses,
            opportunities=opportunities,
            threats=threats,
        )
        return analysis.to_dict()

    def monitor_trends(
        self, topics: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Monitor market trends from collected data."""
        trends = self._trend_monitor.detect_trends(topics)
        summary = self._trend_monitor.get_trend_summary()

        return {
            "trends_detected": len(trends),
            "trends": [t.to_dict() for t in trends],
            "summary": summary,
        }

    def add_intelligence(
        self,
        title: str,
        summary: str,
        source: str,
        competitor_name: str = "",
        category: str = "",
        key_findings: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Add a competitive intelligence report."""
        report = self._intel_collector.collect(
            title=title,
            summary=summary,
            source=source,
            competitor_name=competitor_name,
            category=category,
            key_findings=key_findings,
        )
        return report.to_dict()

    def search_intelligence(
        self,
        keyword: str = "",
        competitor: str = "",
        category: str = "",
    ) -> List[Dict[str, Any]]:
        """Search collected intelligence."""
        return self._intel_collector.search(
            keyword=keyword, competitor=competitor, category=category
        )

    def add_benchmark_metric(
        self,
        category: str,
        metric_name: str,
        our_value: float,
        competitor_values: Dict[str, float],
        industry_average: float = 0.0,
        unit: str = "",
        higher_is_better: bool = True,
    ) -> Dict[str, Any]:
        """Add a competitive benchmark metric."""
        metric = self._benchmark_engine.add_metric(
            category=category,
            metric_name=metric_name,
            our_value=our_value,
            competitor_values=competitor_values,
            industry_average=industry_average,
            unit=unit,
            higher_is_better=higher_is_better,
        )
        return {
            "metric": metric.metric_name,
            "our_value": metric.our_value,
            "category": category,
        }

    def get_benchmark_rankings(self, category: str) -> Dict[str, Any]:
        """Get benchmark rankings for a category."""
        return {
            "category": category,
            "rankings": self._benchmark_engine.get_rankings(category),
            "competitive_score": self._benchmark_engine.competitive_score(category),
        }

    def get_competitive_landscape(self) -> Dict[str, Any]:
        """Get an overview of the competitive landscape."""
        competitors = list(self._competitors.values())
        threat_summary: Dict[str, int] = defaultdict(int)
        for c in competitors:
            threat_summary[c.threat_level.value] += 1

        return {
            "total_competitors": len(competitors),
            "by_threat_level": dict(threat_summary),
            "by_type": {
                ct.value: sum(1 for c in competitors if c.competitor_type == ct)
                for ct in CompetitorType
            },
            "top_competitors": sorted(
                [c.to_dict() for c in competitors],
                key=lambda x: list(ThreatLevel).index(
                    ThreatLevel(x["threat_level"])
                ),
                reverse=True,
            )[:5],
        }

    def generate_strategic_brief(self) -> Dict[str, Any]:
        """Generate an executive strategic intelligence brief."""
        landscape = self.get_competitive_landscape()
        trends = self._trend_monitor.get_trend_summary()
        intel_stats = self._intel_collector.get_stats()
        benchmark_summary = self._benchmark_engine.get_benchmark_summary()

        return {
            "title": "Competitive Intelligence Brief",
            "generated_at": datetime.utcnow().isoformat(),
            "executive_summary": {
                "competitors_tracked": landscape["total_competitors"],
                "active_trends": trends.get("total_trends", 0),
                "intel_reports": intel_stats.get("total_reports", 0),
                "benchmark_categories": len(benchmark_summary.get("categories", [])),
            },
            "landscape_overview": landscape,
            "trend_summary": trends,
            "intelligence_stats": intel_stats,
            "benchmark_summary": benchmark_summary,
            "key_recommendations": self._generate_recommendations(),
        }

    def list_competitors(self) -> List[Dict[str, Any]]:
        return [c.to_dict() for c in self._competitors.values()]

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "CompetitiveIntelAgent",
            "version": "3.0.0",
            "competitors_tracked": len(self._competitors),
            "analyses_performed": len(self._analyses),
            "landscapes": len(self._landscapes),
            "intel_reports": len(self._intel_collector._reports),
            "trends_detected": len(self._trend_monitor._trends),
            "uptime": str(datetime.utcnow() - self._created_at),
        }

    def _assess_threat(self, profile: CompetitorProfile) -> Dict[str, Any]:
        threat_score = 0.0
        factors = []

        if profile.annual_revenue > 1_000_000_000:
            threat_score += 0.3
            factors.append("Large revenue base")
        if profile.employee_count > 1000:
            threat_score += 0.15
            factors.append("Large workforce")
        if len(profile.products) > 5:
            threat_score += 0.15
            factors.append("Broad product portfolio")
        if profile.threat_level in (ThreatLevel.HIGH, ThreatLevel.CRITICAL):
            threat_score += 0.25
            factors.append("High/Critical threat classification")

        return {
            "threat_score": round(min(threat_score, 1.0), 3),
            "threat_level": profile.threat_level.value,
            "contributing_factors": factors,
        }

    def _assess_positioning(self, profile: CompetitorProfile) -> Dict[str, Any]:
        strengths_count = len(profile.strengths)
        weaknesses_count = len(profile.weaknesses)

        if strengths_count > weaknesses_count * 2:
            position = "market_leader"
        elif strengths_count > weaknesses_count:
            position = "strong_contender"
        elif strengths_count == weaknesses_count:
            position = "competitive"
        else:
            position = "vulnerable"

        return {
            "position": position,
            "strengths_count": strengths_count,
            "weaknesses_count": weaknesses_count,
            "net_strength": strengths_count - weaknesses_count,
        }

    def _generate_recommendations(self) -> List[str]:
        recs = []
        competitors = list(self._competitors.values())
        high_threats = [c for c in competitors if c.threat_level in (ThreatLevel.HIGH, ThreatLevel.CRITICAL)]

        if high_threats:
            names = ", ".join(c.name for c in high_threats[:3])
            recs.append(f"Monitor high-threat competitors closely: {names}")

        if len(competitors) < 3:
            recs.append("Expand competitor tracking to include more market players")

        trends = list(self._trend_monitor._trends.values())
        rising = [t for t in trends if t.direction == TrendDirection.RISING]
        if rising:
            recs.append(f"Capitalize on {len(rising)} rising market trends")

        return recs or ["Continue monitoring the competitive landscape"]


# =============================================================================
# Entry Point
# =============================================================================

def main() -> None:
    """Demonstrate the Competitive Intelligence Agent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    print("=" * 70)
    print("  Competitive Intelligence Agent v3.0 - Demonstration")
    print("=" * 70)

    agent = CompetitiveIntelAgent({"user": "demo_user"})

    # Add competitors
    print("\n--- Adding Competitors ---")
    comp1 = agent.add_competitor(
        name="TechCorp Alpha",
        competitor_type="direct",
        website="https://techalpha.com",
        employee_count=5000,
        annual_revenue=500_000_000,
        products=["Cloud Platform", "Analytics Suite", "AI Tools"],
        strengths=["Strong brand", "Large customer base", "R&D investment"],
        weaknesses=["Legacy products", "Slow innovation cycle"],
        threat_level="high",
    )
    print(f"Added: {comp1['name']} (Threat: {comp1['threat_level']})")

    comp2 = agent.add_competitor(
        name="InnovateTech",
        competitor_type="direct",
        website="https://innovatetech.io",
        employee_count=1200,
        annual_revenue=80_000_000,
        products=["AI Platform", "Developer Tools"],
        strengths=["Cutting-edge AI", "Developer community", "Fast iteration"],
        weaknesses=["Limited enterprise sales", "Smaller scale"],
        threat_level="medium",
    )
    print(f"Added: {comp2['name']} (Threat: {comp2['threat_level']})")

    comp3 = agent.add_competitor(
        name="DataFlow Systems",
        competitor_type="indirect",
        website="https://dataflow.io",
        employee_count=300,
        annual_revenue=20_000_000,
        products=["Data Pipeline Tool"],
        strengths=["Niche expertise", "Low pricing"],
        weaknesses=["Limited feature set"],
        threat_level="low",
    )
    print(f"Added: {comp3['name']} (Threat: {comp3['threat_level']})")

    # Analyze a competitor
    print("\n--- Competitor Analysis ---")
    analysis = agent.analyze_competitor(comp1["competitor_id"])
    print(f"Threat score: {analysis['threat_assessment']['threat_score']}")
    print(f"Positioning: {analysis['competitive_positioning']['position']}")

    # SWOT Analysis
    print("\n--- SWOT Analysis ---")
    swot = agent.perform_swot(
        subject="Our Company",
        strengths=["Innovative technology", "Strong team", "Growing market share"],
        weaknesses=["Limited brand recognition", "Small sales team"],
        opportunities=["AI market growth", "Enterprise adoption", "International expansion"],
        threats=["Big tech entry", "Economic downturn", "Regulatory changes"],
    )
    print(f"Score: {swot['overall_score']}")
    print(f"Priority: {swot['strategic_priority']}")

    # Add intelligence
    print("\n--- Intelligence Collection ---")
    agent.add_intelligence(
        title="TechCorp Alpha announces new AI product line",
        summary="TechCorp Alpha unveiled a comprehensive AI suite targeting enterprise customers",
        source="news_article",
        competitor_name="TechCorp Alpha",
        category="product_launch",
        key_findings=["New AI product targets enterprise", "Pricing 20% below market"],
    )
    agent.add_intelligence(
        title="InnovateTech raises $50M Series C",
        summary="InnovateTech closes Series C funding at $300M valuation",
        source="crunchbase",
        competitor_name="InnovateTech",
        category="funding",
        key_findings=["Funding for international expansion", "New offices in Europe"],
    )
    intel_stats = agent._intel_collector.get_stats()
    print(f"Total reports: {intel_stats['total_reports']}")

    # Search intelligence
    print("\n--- Search Intelligence ---")
    results = agent.search_intelligence(competitor="TechCorp Alpha")
    print(f"Found {len(results)} reports for TechCorp Alpha")

    # Benchmarks
    print("\n--- Benchmarking ---")
    agent.add_benchmark_metric(
        category="product_features",
        metric_name="Feature Count",
        our_value=150,
        competitor_values={"TechCorp Alpha": 200, "InnovateTech": 80},
        industry_average=120,
        unit="features",
    )
    rankings = agent.get_benchmark_rankings("product_features")
    print(f"Our rank: {rankings['competitive_score']['position']}")
    print(f"Score: {rankings['competitive_score']['score']}")

    # Trend monitoring
    print("\n--- Trend Monitoring ---")
    for _ in range(5):
        agent._trend_monitor.add_data_point("AI Adoption", "news", "AI adoption growing", "positive")
    for _ in range(3):
        agent._trend_monitor.add_data_point("AI Adoption", "report", "AI spending increasing", "positive")
    trends = agent.monitor_trends()
    print(f"Trends detected: {trends['trends_detected']}")

    # Competitive landscape
    print("\n--- Competitive Landscape ---")
    landscape = agent.get_competitive_landscape()
    print(f"Competitors tracked: {landscape['total_competitors']}")
    print(f"By threat: {landscape['by_threat_level']}")

    # Strategic brief
    print("\n--- Strategic Brief ---")
    brief = agent.generate_strategic_brief()
    print(f"Competitors: {brief['executive_summary']['competitors_tracked']}")
    print(f"Recommendations: {len(brief['key_recommendations'])}")

    # Agent status
    print("\n--- Agent Status ---")
    status = agent.get_status()
    for k, v in status.items():
        print(f"  {k}: {v}")

    print("\n" + "=" * 70)
    print("  Demonstration Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()

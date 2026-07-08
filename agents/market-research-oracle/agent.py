"""
Market Research Oracle Agent
Market research, survey design, data collection, trend analysis, competitive landscape, and forecasting.
"""

import logging
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import uuid4

logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Enums
# ──────────────────────────────────────────────

class ResearchPhase(Enum):
    DISCOVERY = "discovery"
    DATA_COLLECTION = "data_collection"
    ANALYSIS = "analysis"
    VALIDATION = "validation"
    REPORTING = "reporting"


class DataSource(Enum):
    SURVEY = "survey"
    INTERVIEW = "interview"
    FOCUS_GROUP = "focus_group"
    SOCIAL_MEDIA = "social_media"
    NEWS = "news"
    FINANCIAL = "financial"
    GOVERNMENT = "government"
    PROPRIETARY = "proprietary"
    WEB_SCRAPE = "web_scrape"
    API = "api"


class SentimentLabel(Enum):
    VERY_NEGATIVE = "very_negative"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    VERY_POSITIVE = "very_positive"


class TrendType(Enum):
    EMERGING = "emerging"
    GROWTH = "growth"
    MATURING = "maturing"
    DECLINING = "declining"
    STABLE = "stable"
    CYCLICAL = "cyclical"


class ForecastMethod(Enum):
    MOVING_AVERAGE = "moving_average"
    EXPONENTIAL_SMOOTHING = "exponential_smoothing"
    LINEAR_REGRESSION = "linear_regression"
    SEASONAL_DECOMPOSITION = "seasonal_decomposition"
    MONTE_CARLO = "monte_carlo"


class SurveyQuestionType(Enum):
    MULTIPLE_CHOICE = "multiple_choice"
    OPEN_ENDED = "open_ended"
    RATING = "rating"
    RANKING = "ranking"
    NET_PROMOTER = "net_promoter"
    BINARY = "binary"
   Likert = "likert"
    DEMOGRAPHIC = "demographic"


class CompetitivePosition(Enum):
    LEADER = "leader"
    CHALLENGER = "challenger"
    FOLLOWER = "follower"
    NICHE = "niche"
    EMERGING = "emerging"


# ──────────────────────────────────────────────
# Data Classes
# ──────────────────────────────────────────────

@dataclass
class SurveyQuestion:
    question_id: str = field(default_factory=lambda: str(uuid4())[:8])
    question_type: SurveyQuestionType = SurveyQuestionType.OPEN_ENDED
    text: str = ""
    options: List[str] = field(default_factory=list)
    required: bool = True
    order: int = 0


@dataclass
class Survey:
    survey_id: str = field(default_factory=lambda: f"srv_{str(uuid4())[:8]}")
    title: str = ""
    description: str = ""
    questions: List[SurveyQuestion] = field(default_factory=list)
    target_responses: int = 100
    current_responses: int = 0
    status: str = "draft"
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class SurveyResponse:
    response_id: str = field(default_factory=lambda: str(uuid4())[:8])
    survey_id: str = ""
    respondent_id: str = ""
    answers: Dict[str, Any] = field(default_factory=dict)
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Competitor:
    competitor_id: str = field(default_factory=lambda: f"comp_{str(uuid4())[:8]}")
    name: str = ""
    position: CompetitivePosition = CompetitivePosition.FOLLOWER
    market_share: float = 0.0
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    products: List[str] = field(default_factory=list)
    pricing: Dict[str, Any] = field(default_factory=dict)
    recent_moves: List[str] = field(default_factory=list)
    sentiment_score: float = 0.0
    growth_rate: float = 0.0
    last_analyzed: Optional[datetime] = None


@dataclass
class Trend:
    trend_id: str = field(default_factory=lambda: f"trend_{str(uuid4())[:8]}")
    name: str = ""
    trend_type: TrendType = TrendType.EMERGING
    growth_rate: float = 0.0
    confidence: float = 0.0
    sources: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.now)
    description: str = ""


@dataclass
class MarketSize:
    segment: str = ""
    tam: float = 0.0
    sam: float = 0.0
    som: float = 0.0
    growth_rate: float = 0.0
    year: int = 2025


@dataclass
class SentimentResult:
    source: str = ""
    label: SentimentLabel = SentimentLabel.NEUTRAL
    score: float = 0.0
    confidence: float = 0.0
    volume: int = 0
    velocity: float = 0.0
    volatility: float = 0.0
    keywords: List[str] = field(default_factory=list)


@dataclass
class ForecastResult:
    metric: str = ""
    method: ForecastMethod = ForecastMethod.LINEAR_REGRESSION
    historical_values: List[float] = field(default_factory=list)
    predicted_values: List[float] = field(default_factory=list)
    confidence_interval: Tuple[float, float] = (0.0, 0.0)
    accuracy_score: float = 0.0


@dataclass
class ResearchReport:
    report_id: str = field(default_factory=lambda: f"rpt_{str(uuid4())[:8]}")
    title: str = ""
    executive_summary: str = ""
    sections: List[Dict[str, Any]] = field(default_factory=list)
    findings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    data_sources: List[str] = field(default_factory=list)
    generated_at: datetime = field(default_factory=datetime.now)


# ──────────────────────────────────────────────
# Exceptions
# ──────────────────────────────────────────────

class ResearchError(Exception):
    """Base research error."""


class SurveyError(ResearchError):
    """Survey-related errors."""


class InsufficientDataError(ResearchError):
    """Not enough data for analysis."""


class InvalidForecastError(ResearchError):
    """Forecast computation failed."""


# ──────────────────────────────────────────────
# Survey Builder
# ──────────────────────────────────────────────

class SurveyBuilder:
    """Design, build, and analyze surveys."""

    def __init__(self) -> None:
        self._surveys: Dict[str, Survey] = {}
        self._responses: Dict[str, List[SurveyResponse]] = {}

    def create_survey(
        self,
        title: str,
        description: str = "",
        target_responses: int = 100,
    ) -> Survey:
        survey = Survey(title=title, description=description, target_responses=target_responses)
        self._surveys[survey.survey_id] = survey
        self._responses[survey.survey_id] = []
        logger.info("Created survey %s (%s)", survey.survey_id, title)
        return survey

    def add_question(
        self,
        survey_id: str,
        text: str,
        question_type: SurveyQuestionType = SurveyQuestionType.OPEN_ENDED,
        options: Optional[List[str]] = None,
        required: bool = True,
    ) -> SurveyQuestion:
        survey = self._get_survey(survey_id)
        question = SurveyQuestion(
            text=text,
            question_type=question_type,
            options=options or [],
            required=required,
            order=len(survey.questions),
        )
        survey.questions.append(question)
        return question

    def submit_response(
        self, survey_id: str, respondent_id: str, answers: Dict[str, Any]
    ) -> SurveyResponse:
        survey = self._get_survey(survey_id)
        response = SurveyResponse(
            survey_id=survey_id,
            respondent_id=respondent_id,
            answers=answers,
            completed_at=datetime.now(),
        )
        self._responses[survey_id].append(response)
        survey.current_responses += 1
        return response

    def analyze_survey(self, survey_id: str) -> Dict[str, Any]:
        survey = self._get_survey(survey_id)
        responses = self._responses.get(survey_id, [])
        if not responses:
            return {"error": "No responses collected"}
        analysis: Dict[str, Any] = {
            "survey_id": survey_id,
            "total_responses": len(responses),
            "completion_rate": len(responses) / max(1, survey.target_responses) * 100,
            "questions": {},
        }
        for question in survey.questions:
            q_answers = [r.answers.get(question.question_id) for r in responses if question.question_id in r.answers]
            analysis["questions"][question.question_id] = self._analyze_question(question, q_answers)
        return analysis

    def _analyze_question(self, question: SurveyQuestion, answers: List[Any]) -> Dict[str, Any]:
        if not answers:
            return {"type": question.question_type.value, "response_count": 0}
        if question.question_type == SurveyQuestionType.RATING:
            numeric = [a for a in answers if isinstance(a, (int, float))]
            return {
                "type": "rating",
                "mean": round(sum(numeric) / len(numeric), 2) if numeric else 0,
                "min": min(numeric) if numeric else 0,
                "max": max(numeric) if numeric else 0,
                "response_count": len(numeric),
            }
        if question.question_type == SurveyQuestionType.MULTIPLE_CHOICE:
            counts: Dict[str, int] = {}
            for a in answers:
                counts[str(a)] = counts.get(str(a), 0) + 1
            return {"type": "multiple_choice", "distribution": counts, "response_count": len(answers)}
        if question.question_type == SurveyQuestionType.NET_PROMOTER:
            numeric = [a for a in answers if isinstance(a, (int, float))]
            promoters = len([n for n in numeric if n >= 9])
            detractors = len([n for n in numeric if n <= 6])
            nps = ((promoters - detractors) / len(numeric) * 100) if numeric else 0
            return {"type": "nps", "nps_score": round(nps, 1), "response_count": len(numeric)}
        return {"type": question.question_type.value, "response_count": len(answers), "sample": answers[:5]}

    def _get_survey(self, survey_id: str) -> Survey:
        if survey_id not in self._surveys:
            raise SurveyError(f"Survey {survey_id} not found")
        return self._surveys[survey_id]

    def list_surveys(self) -> List[Survey]:
        return list(self._surveys.values())


# ──────────────────────────────────────────────
# Data Collector
# ──────────────────────────────────────────────

class DataCollector:
    """Collect and aggregate data from multiple sources."""

    def __init__(self) -> None:
        self._collections: Dict[str, List[Dict[str, Any]]] = {}
        self._source_metadata: Dict[str, Dict[str, Any]] = {}

    def register_source(
        self, source_name: str, source_type: DataSource, reliability: float = 0.8
    ) -> None:
        self._source_metadata[source_name] = {
            "type": source_type,
            "reliability": reliability,
            "last_updated": datetime.now(),
        }

    def collect(
        self,
        source_name: str,
        topic: str,
        data: List[Dict[str, Any]],
    ) -> int:
        if source_name not in self._source_metadata:
            self.register_source(source_name, DataSource.API)
        key = f"{source_name}:{topic}"
        self._collections.setdefault(key, []).extend(data)
        logger.info("Collected %d records from %s for topic '%s'", len(data), source_name, topic)
        return len(data)

    def get_data(self, source_name: str, topic: str) -> List[Dict[str, Any]]:
        return self._collections.get(f"{source_name}:{topic}", [])

    def get_all_topics(self) -> List[str]:
        topics = set()
        for key in self._collections:
            _, topic = key.split(":", 1)
            topics.add(topic)
        return list(topics)

    def aggregate_sentiment(self, topic: str) -> SentimentResult:
        all_data: List[Dict[str, Any]] = []
        for key, records in self._collections.items():
            if key.endswith(f":{topic}"):
                all_data.extend(records)
        if not all_data:
            return SentimentResult(source="aggregated", volume=0)
        scores = [r.get("sentiment_score", 0.5) for r in all_data if "sentiment_score" in r]
        avg_score = sum(scores) / len(scores) if scores else 0.5
        if avg_score >= 0.75:
            label = SentimentLabel.VERY_POSITIVE
        elif avg_score >= 0.55:
            label = SentimentLabel.POSITIVE
        elif avg_score >= 0.45:
            label = SentimentLabel.NEUTRAL
        elif avg_score >= 0.25:
            label = SentimentLabel.NEGATIVE
        else:
            label = SentimentLabel.VERY_NEGATIVE
        keywords: List[str] = []
        for r in all_data:
            keywords.extend(r.get("keywords", []))
        keyword_counts: Dict[str, int] = {}
        for kw in keywords:
            keyword_counts[kw] = keyword_counts.get(kw, 0) + 1
        top_keywords = sorted(keyword_counts, key=keyword_counts.get, reverse=True)[:10]
        return SentimentResult(
            source="aggregated",
            label=label,
            score=round(avg_score, 3),
            confidence=min(1.0, len(scores) / 100),
            volume=len(all_data),
            keywords=top_keywords,
        )

    def get_source_stats(self) -> Dict[str, Any]:
        stats: Dict[str, Any] = {}
        for name, meta in self._source_metadata.items():
            record_count = sum(
                len(records)
                for key, records in self._collections.items()
                if key.startswith(f"{name}:")
            )
            stats[name] = {
                "type": meta["type"].value,
                "reliability": meta["reliability"],
                "records": record_count,
            }
        return stats


# ──────────────────────────────────────────────
# Trend Analyzer
# ──────────────────────────────────────────────

class TrendAnalyzer:
    """Detect and analyze market trends."""

    def __init__(self) -> None:
        self._trends: Dict[str, Trend] = {}
        self._time_series: Dict[str, List[Tuple[datetime, float]]] = {}

    def add_data_point(self, metric_name: str, timestamp: datetime, value: float) -> None:
        self._time_series.setdefault(metric_name, []).append((timestamp, value))

    def detect_trends(self, metric_name: str) -> List[Trend]:
        series = self._time_series.get(metric_name, [])
        if len(series) < 3:
            return []
        sorted_series = sorted(series, key=lambda x: x[0])
        values = [v for _, v in sorted_series]
        n = len(values)
        x_vals = list(range(n))
        x_mean = sum(x_vals) / n
        y_mean = sum(values) / n
        numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(x_vals, values))
        denominator = sum((x - x_mean) ** 2 for x in x_vals)
        slope = numerator / denominator if denominator != 0 else 0
        avg_value = y_mean
        relative_slope = slope / avg_value if avg_value != 0 else 0
        if relative_slope > 0.1:
            trend_type = TrendType.GROWTH
        elif relative_slope > 0.02:
            trend_type = TrendType.EMERGING
        elif relative_slope < -0.1:
            trend_type = TrendType.DECLINING
        elif relative_slope < -0.02:
            trend_type = TrendType.STABLE
        else:
            trend_type = TrendType.MATURING
        volatility = self._calculate_volatility(values)
        confidence = min(1.0, n / 20) * max(0, 1 - volatility)
        trend = Trend(
            name=metric_name,
            trend_type=trend_type,
            growth_rate=round(relative_slope * 100, 2),
            confidence=round(confidence, 3),
            description=f"{metric_name} shows {trend_type.value} pattern with {relative_slope*100:.1f}% slope",
        )
        self._trends[trend.trend_id] = trend
        return [trend]

    def _calculate_volatility(self, values: List[float]) -> float:
        if len(values) < 2:
            return 0.0
        returns = [(values[i] - values[i - 1]) / values[i - 1] for i in range(1, len(values)) if values[i - 1] != 0]
        if not returns:
            return 0.0
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        return math.sqrt(variance)

    def get_trend_summary(self) -> Dict[str, Any]:
        summary: Dict[str, Any] = {"total_trends": len(self._trends), "by_type": {}}
        for trend in self._trends.values():
            t = trend.trend_type.value
            summary["by_type"][t] = summary["by_type"].get(t, 0) + 1
        return summary

    def list_trends(self) -> List[Trend]:
        return list(self._trends.values())


# ──────────────────────────────────────────────
# Competitive Landscape
# ──────────────────────────────────────────────

class CompetitiveLandscape:
    """Analyze and map the competitive landscape."""

    def __init__(self) -> None:
        self._competitors: Dict[str, Competitor] = {}

    def add_competitor(
        self,
        name: str,
        market_share: float,
        strengths: List[str],
        weaknesses: List[str],
        position: CompetitivePosition = CompetitivePosition.FOLLOWER,
    ) -> Competitor:
        comp = Competitor(
            name=name,
            position=position,
            market_share=market_share,
            strengths=strengths,
            weaknesses=weaknesses,
            last_analyzed=datetime.now(),
        )
        self._competitors[comp.competitor_id] = comp
        logger.info("Added competitor %s", name)
        return comp

    def update_competitor(self, competitor_id: str, **kwargs: Any) -> Competitor:
        if competitor_id not in self._competitors:
            raise ResearchError(f"Competitor {competitor_id} not found")
        comp = self._competitors[competitor_id]
        for key, value in kwargs.items():
            if hasattr(comp, key):
                setattr(comp, key, value)
        return comp

    def generate_swot(self, competitor_id: str) -> Dict[str, Any]:
        comp = self._competitors.get(competitor_id)
        if not comp:
            return {"error": "Competitor not found"}
        return {
            "competitor": comp.name,
            "strengths": comp.strengths,
            "weaknesses": comp.weaknesses,
            "market_position": comp.position.value,
            "market_share": comp.market_share,
            "opportunities": self._identify_opportunities(comp),
            "threats": self._identify_threats(comp),
        }

    def _identify_opportunities(self, comp: Competitor) -> List[str]:
        opportunities = []
        if comp.market_share < 0.1:
            opportunities.append("Underpenetrated market share suggests room for growth")
        if comp.sentiment_score < 0.4:
            opportunities.append("Low customer sentiment creates switching opportunity")
        if len(comp.weaknesses) > len(comp.strengths):
            opportunities.append("More weaknesses than strengths indicates vulnerability")
        return opportunities

    def _identify_threats(self, comp: Competitor) -> List[str]:
        threats = []
        if comp.market_share > 0.3:
            threats.append("Dominant market position")
        if comp.growth_rate > 10:
            threats.append("Rapid growth trajectory")
        if len(comp.strengths) > len(comp.weaknesses):
            threats.append("Strong competitive advantages")
        return threats

    def competitive_matrix(self) -> Dict[str, Any]:
        matrix: List[Dict[str, Any]] = []
        for comp in self._competitors.values():
            matrix.append({
                "name": comp.name,
                "market_share": comp.market_share,
                "position": comp.position.value,
                "sentiment": comp.sentiment_score,
                "growth": comp.growth_rate,
                "strengths_count": len(comp.strengths),
                "weaknesses_count": len(comp.weaknesses),
            })
        return {"competitors": sorted(matrix, key=lambda x: x["market_share"], reverse=True)}

    def get_threat_assessment(self) -> Dict[str, Any]:
        threats = []
        for comp in self._competitors.values():
            threat_level = 0
            if comp.market_share > 0.2:
                threat_level += 3
            elif comp.market_share > 0.1:
                threat_level += 2
            elif comp.market_share > 0.05:
                threat_level += 1
            if comp.growth_rate > 15:
                threat_level += 2
            elif comp.growth_rate > 5:
                threat_level += 1
            if comp.sentiment_score > 0.7:
                threat_level += 1
            threats.append({
                "competitor": comp.name,
                "threat_level": min(5, threat_level),
                "market_share": comp.market_share,
            })
        return {"threats": sorted(threats, key=lambda x: x["threat_level"], reverse=True)}

    def list_competitors(self) -> List[Competitor]:
        return list(self._competitors.values())


# ──────────────────────────────────────────────
# Forecasting Engine
# ──────────────────────────────────────────────

class ForecastEngine:
    """Generate forecasts using various statistical methods."""

    def __init__(self) -> None:
        self._forecasts: Dict[str, ForecastResult] = {}

    def moving_average(
        self, metric_name: str, values: List[float], window: int = 3
    ) -> ForecastResult:
        if len(values) < window:
            raise InvalidForecastError(f"Need at least {window} data points")
        predictions: List[float] = []
        for i in range(window, len(values)):
            predictions.append(sum(values[i - window : i]) / window)
        last_avg = sum(values[-window:]) / window
        predictions.append(last_avg)
        ci = self._confidence_interval(values, predictions)
        result = ForecastResult(
            metric=metric_name,
            method=ForecastMethod.MOVING_AVERAGE,
            historical_values=values,
            predicted_values=predictions,
            confidence_interval=ci,
            accuracy_score=self._accuracy_score(values[:len(predictions)], predictions[:len(values)]),
        )
        self._forecasts[metric_name] = result
        return result

    def exponential_smoothing(
        self, metric_name: str, values: List[float], alpha: float = 0.3
    ) -> ForecastResult:
        if len(values) < 2:
            raise InvalidForecastError("Need at least 2 data points")
        smoothed: List[float] = [values[0]]
        for i in range(1, len(values)):
            smoothed.append(alpha * values[i] + (1 - alpha) * smoothed[-1])
        last_smoothed = smoothed[-1]
        predictions = smoothed + [last_smoothed]
        ci = self._confidence_interval(values, predictions[:len(values)])
        result = ForecastResult(
            metric=metric_name,
            method=ForecastMethod.EXPONENTIAL_SMOOTHING,
            historical_values=values,
            predicted_values=predictions,
            confidence_interval=ci,
            accuracy_score=self._accuracy_score(values, predictions[:len(values)]),
        )
        self._forecasts[metric_name] = result
        return result

    def linear_regression(
        self, metric_name: str, values: List[float]
    ) -> ForecastResult:
        n = len(values)
        if n < 2:
            raise InvalidForecastError("Need at least 2 data points")
        x = list(range(n))
        x_mean = sum(x) / n
        y_mean = sum(values) / n
        num = sum((xi - x_mean) * (yi - y_mean) for xi, yi in zip(x, values))
        den = sum((xi - x_mean) ** 2 for xi in x)
        slope = num / den if den != 0 else 0
        intercept = y_mean - slope * x_mean
        predictions = [slope * xi + intercept for xi in x]
        predictions.append(slope * n + intercept)
        ci = self._confidence_interval(values, predictions[:n])
        result = ForecastResult(
            metric=metric_name,
            method=ForecastMethod.LINEAR_REGRESSION,
            historical_values=values,
            predicted_values=predictions,
            confidence_interval=ci,
            accuracy_score=self._accuracy_score(values, predictions[:n]),
        )
        self._forecasts[metric_name] = result
        return result

    def _confidence_interval(
        self, actual: List[float], predicted: List[float]
    ) -> Tuple[float, float]:
        if not actual or not predicted:
            return (0.0, 0.0)
        errors = [abs(a - p) for a, p in zip(actual, predicted[:len(actual)])]
        avg_error = sum(errors) / len(errors)
        return (round(avg_error * -1, 2), round(avg_error, 2))

    def _accuracy_score(self, actual: List[float], predicted: List[float]) -> float:
        if not actual or not predicted:
            return 0.0
        mape_values = []
        for a, p in zip(actual, predicted[:len(actual)]):
            if a != 0:
                mape_values.append(abs((a - p) / a))
        if not mape_values:
            return 0.0
        mape = sum(mape_values) / len(mape_values)
        return round(max(0, 1 - mape), 3)

    def get_forecast(self, metric_name: str) -> Optional[ForecastResult]:
        return self._forecasts.get(metric_name)

    def list_forecasts(self) -> List[ForecastResult]:
        return list(self._forecasts.values())


# ──────────────────────────────────────────────
# Market Size Estimator
# ──────────────────────────────────────────────

class MarketSizeEstimator:
    """Estimate market size using TAM/SAM/SOM framework."""

    def __init__(self) -> None:
        self._estimates: Dict[str, MarketSize] = {}

    def estimate(
        self,
        segment: str,
        total_addressable: float,
        serviceable_percentage: float = 0.3,
        obtainable_percentage: float = 0.1,
        growth_rate: float = 0.0,
    ) -> MarketSize:
        sam = total_addressable * serviceable_percentage
        som = sam * obtainable_percentage
        size = MarketSize(
            segment=segment,
            tam=total_addressable,
            sam=sam,
            som=som,
            growth_rate=growth_rate,
            year=datetime.now().year,
        )
        self._estimates[segment] = size
        return size

    def project_forward(self, segment: str, years: int = 5) -> List[MarketSize]:
        base = self._estimates.get(segment)
        if not base:
            return []
        projections: List[MarketSize] = []
        for y in range(1, years + 1):
            growth = (1 + base.growth_rate / 100) ** y
            projections.append(MarketSize(
                segment=segment,
                tam=round(base.tam * growth),
                sam=round(base.sam * growth),
                som=round(base.som * growth),
                growth_rate=base.growth_rate,
                year=base.year + y,
            ))
        return projections

    def get_estimate(self, segment: str) -> Optional[MarketSize]:
        return self._estimates.get(segment)

    def list_estimates(self) -> List[MarketSize]:
        return list(self._estimates.values())


# ──────────────────────────────────────────────
# Report Generator
# ──────────────────────────────────────────────

class ReportGenerator:
    """Generate comprehensive research reports."""

    def __init__(self) -> None:
        self._reports: Dict[str, ResearchReport] = {}

    def generate_report(
        self,
        title: str,
        executive_summary: str,
        findings: List[str],
        recommendations: List[str],
        data_sources: Optional[List[str]] = None,
        sections: Optional[List[Dict[str, Any]]] = None,
    ) -> ResearchReport:
        report = ResearchReport(
            title=title,
            executive_summary=executive_summary,
            findings=findings,
            recommendations=recommendations,
            data_sources=data_sources or [],
            sections=sections or [],
        )
        self._reports[report.report_id] = report
        logger.info("Generated report %s (%s)", report.report_id, title)
        return report

    def add_section(self, report_id: str, title: str, content: str, data: Any = None) -> None:
        report = self._reports.get(report_id)
        if report:
            report.sections.append({"title": title, "content": content, "data": data})

    def get_report(self, report_id: str) -> Optional[ResearchReport]:
        return self._reports.get(report_id)

    def list_reports(self) -> List[ResearchReport]:
        return list(self._reports.values())


# ──────────────────────────────────────────────
# Market Research Oracle (orchestrator)
# ──────────────────────────────────────────────

class MarketResearchOracle:
    """Top-level orchestrator for all market research operations."""

    def __init__(self) -> None:
        self.surveys = SurveyBuilder()
        self.data_collector = DataCollector()
        self.trends = TrendAnalyzer()
        self.competitive = CompetitiveLandscape()
        self.forecast = ForecastEngine()
        self.market_size = MarketSizeEstimator()
        self.reports = ReportGenerator()
        logger.info("MarketResearchOracle initialized")

    def full_research_cycle(
        self,
        topic: str,
        competitors: List[Dict[str, Any]],
        data_points: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        for comp_data in competitors:
            self.competitive.add_competitor(
                name=comp_data["name"],
                market_share=comp_data.get("market_share", 0.0),
                strengths=comp_data.get("strengths", []),
                weaknesses=comp_data.get("weaknesses", []),
            )
        self.data_collector.collect("internal", topic, data_points)
        sentiment = self.data_collector.aggregate_sentiment(topic)
        matrix = self.competitive.competitive_matrix()
        report = self.reports.generate_report(
            title=f"Market Research: {topic}",
            executive_summary=f"Comprehensive analysis of {topic} market",
            findings=[f"Sentiment: {sentiment.label.value}", f"Competitors analyzed: {len(competitors)}"],
            recommendations=["Continue monitoring", "Expand data collection"],
        )
        return {
            "topic": topic,
            "sentiment": {
                "label": sentiment.label.value,
                "score": sentiment.score,
                "volume": sentiment.volume,
            },
            "competitive_matrix": matrix,
            "report_id": report.report_id,
        }


# ──────────────────────────────────────────────
# CLI entry point
# ──────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    oracle = MarketResearchOracle()

    survey = oracle.surveys.create_survey("Product Feedback", "Annual product survey")
    oracle.surveys.add_question(survey.survey_id, "How satisfied are you?", SurveyQuestionType.RATING)
    oracle.surveys.add_question(survey.survey_id, "What features do you use?", SurveyQuestionType.MULTIPLE_CHOICE, ["A", "B", "C"])
    oracle.surveys.submit_response(survey.survey_id, "r1", {"q1": 8, "q2": "A"})
    oracle.surveys.submit_response(survey.survey_id, "r2", {"q1": 6, "q2": "B"})

    analysis = oracle.surveys.analyze_survey(survey.survey_id)
    print(f"Survey responses: {analysis['total_responses']}")

    oracle.trends.add_data_point("revenue", datetime(2025, 1, 1), 100)
    oracle.trends.add_data_point("revenue", datetime(2025, 2, 1), 115)
    oracle.trends.add_data_point("revenue", datetime(2025, 3, 1), 130)
    oracle.trends.add_data_point("revenue", datetime(2025, 4, 1), 140)
    trend_list = oracle.trends.detect_trends("revenue")
    print(f"Trend: {trend_list[0].trend_type.value}, Growth: {trend_list[0].growth_rate}%")

    oracle.competitive.add_competitor("AlphaCorp", 0.25, ["Brand", "Distribution"], ["Innovation"])
    oracle.competitive.add_competitor("BetaInc", 0.15, ["Price"], ["Quality"])
    swot = oracle.competitive.generate_swot(list(oracle.competitive.list_competitors())[0].competitor_id)
    print(f"SWOT for {swot['competitor']}: {len(swot['strengths'])} strengths")

    forecast = oracle.forecast.linear_regression("revenue", [100, 115, 130, 140, 155])
    print(f"Forecast next: {forecast.predicted_values[-1]:.1f}, Accuracy: {forecast.accuracy_score}")

    size = oracle.market_size.estimate("SaaS", 50_000_000_000, 0.3, 0.1, 12.5)
    print(f"Market: TAM=${size.tam:,.0f}, SOM=${size.som:,.0f}")

    report = oracle.reports.generate_report("Q1 Market Analysis", "Strong growth in all segments.", ["Growth 12%"], ["Invest more"])
    print(f"Report: {report.report_id}")

"""Customer Retention Agent - Churn Prediction and Retention Platform.

Comprehensive framework for customer retention including churn prediction,
loyalty programs, NPS analysis, retention strategies, win-back campaigns,
cohort analysis, health monitoring, renewal management, contract tracking,
sentiment analysis, escalation management, churn reason analysis, and
retention dashboards.

Features:
- Churn prediction with risk scoring and reason analysis
- Loyalty program management (points, tiers, rewards)
- NPS survey and analysis
- Retention strategy engine with escalation
- Win-back campaign automation
- Cohort analysis and retention curves
- Customer lifetime value prediction
- Customer health monitoring with composite scoring
- Renewal management and contract tracking
- Sentiment analysis from feedback signals
- Escalation engine for at-risk accounts
- Retention dashboard and alerting
- Churn reason categorization and root cause analysis
- A/B testing for retention tactics
- Executive reporting and dashboards
"""

import hashlib
import json
import logging
import random
import statistics
import threading
import time
import uuid
from collections import defaultdict, deque
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("customer_retention_agent")

# =============================================================================
# ENUMS
# =============================================================================

class ChurnRiskLevel(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

class LoyaltyTier(Enum):
    BRONZE = auto()
    SILVER = auto()
    GOLD = auto()
    PLATINUM = auto()
    DIAMOND = auto()

class RetentionStrategy(Enum):
    ENGAGEMENT_INCREASE = auto()
    DISCOUNT_OFFER = auto()
    PERSONAL_OUTREACH = auto()
    FEATURE_HIGHLIGHT = auto()
    LOYALTY_REWARD = auto()
    EXIT_SURVEY = auto()
    WINBACK_CAMPAIGN = auto()
    SUCCESS_MANAGER = auto()

class NPSCategory(Enum):
    DETRACTOR = auto()
    PASSIVE = auto()
    PROMOTER = auto()

class CohortType(Enum):
    MONTHLY = auto()
    WEEKLY = auto()
    QUARTERLY = auto()
    ACQUISITION_CHANNEL = auto()
    PLAN_TYPE = auto()
    GEOGRAPHY = auto()

class SurveyStatus(Enum):
    DRAFT = auto()
    SENT = auto()
    COMPLETED = auto()
    EXPIRED = auto()

class WinbackStatus(Enum):
    PENDING = auto()
    SENT = auto()
    OPENED = auto()
    CONVERTED = auto()
    EXPIRED = auto()

class RetentionMetric(Enum):
    CHURN_RATE = auto()
    RETENTION_RATE = auto()
    NPS_SCORE = auto()
    LTV = auto()
    ENGAGEMENT_SCORE = auto()
    REVENUE_RETENTION = auto()

class RenewalStatus(Enum):
    PENDING = auto()
    INITIATED = auto()
    IN_NEGOTIATION = auto()
    RENEWED = auto()
    LOST = auto()
    EXPIRED = auto()
    CANCELLED = auto()

class SentimentLevel(Enum):
    VERY_NEGATIVE = auto()
    NEGATIVE = auto()
    NEUTRAL = auto()
    POSITIVE = auto()
    VERY_POSITIVE = auto()

class EscalationReason(Enum):
    HIGH_CHURN_RISK = auto()
    NEGATIVE_SENTIMENT = auto()
    PAYMENT_DEFAULT = auto()
    SUPPORT_ESCALATION = auto()
    COMPETITOR_THREAT = auto()
    CONTRACT_EXPIRY = auto()
    USAGE_DECLINE = auto()
    EXECUTIVE_SPONSOR_LOST = auto()

class ContractType(Enum):
    MONTHLY = auto()
    ANNUAL = auto()
    MULTI_YEAR = auto()
    FREE_TRIAL = auto()
    ENTERPRISE = auto()
    CUSTOM = auto()

class ChurnReason(Enum):
    PRICE_SENSITIVITY = auto()
    FEATURE_GAP = auto()
    POOR_SUPPORT = auto()
    COMPETITOR_SWITCH = auto()
    BUSINESS_CLOSURE = auto()
    BUDGET_CUTS = auto()
    LOW_ENGAGEMENT = auto()
    PRODUCT_QUALITY = auto()
    ONBOARDING_FAILURE = auto()
    CHAMPION_LEFT = auto()
    CONTRACT_ISSUES = auto()
    UNKNOWN = auto()

# =============================================================================
# CONSTANTS
# =============================================================================

LOYALTY_TIERS: Dict[LoyaltyTier, Dict[str, Any]] = {
    LoyaltyTier.BRONZE: {"min_points": 0, "multiplier": 1.0, "benefits": ["Basic rewards"]},
    LoyaltyTier.SILVER: {"min_points": 1000, "multiplier": 1.25, "benefits": ["5% discount", "Free shipping"]},
    LoyaltyTier.GOLD: {"min_points": 5000, "multiplier": 1.5, "benefits": ["10% discount", "Priority support"]},
    LoyaltyTier.PLATINUM: {"min_points": 15000, "multiplier": 2.0, "benefits": ["15% discount", "Exclusive events"]},
    LoyaltyTier.DIAMOND: {"min_points": 50000, "multiplier": 3.0, "benefits": ["20% discount", "VIP access"]},
}

CHURN_SIGNALS: Dict[str, float] = {
    "login_decrease": 0.3,
    "support_ticket_increase": 0.2,
    "feature_usage_decline": 0.25,
    "payment_failure": 0.4,
    "contract_near_expiry": 0.15,
    "negative_feedback": 0.35,
    "competitor_mention": 0.2,
    "downgrade_request": 0.5,
    "reduced_engagement": 0.2,
    "missed_renewal": 0.6,
}

NPS_THRESHOLDS = {"detractor_max": 6, "passive_max": 8, "promoter_min": 9}

HEALTH_SCORE_WEIGHTS: Dict[str, float] = {
    "engagement": 0.25,
    "satisfaction": 0.25,
    "financial": 0.20,
    "support": 0.15,
    "contract": 0.15,
}

SENTIMENT_KEYWORDS_POSITIVE: Set[str] = {
    "great", "excellent", "love", "amazing", "fantastic", "wonderful",
    "happy", "satisfied", "impressed", "recommend", "best", "perfect",
}

SENTIMENT_KEYWORDS_NEGATIVE: Set[str] = {
    "bad", "terrible", "awful", "hate", "frustrated", "disappointed",
    "poor", "worst", "broken", "useless", "angry", "unacceptable",
}

CHURN_REASON_WEIGHTS: Dict[ChurnReason, float] = {
    ChurnReason.PRICE_SENSITIVITY: 0.85,
    ChurnReason.FEATURE_GAP: 0.70,
    ChurnReason.POOR_SUPPORT: 0.75,
    ChurnReason.COMPETITOR_SWITCH: 0.90,
    ChurnReason.BUSINESS_CLOSURE: 0.95,
    ChurnReason.BUDGET_CUTS: 0.80,
    ChurnReason.LOW_ENGAGEMENT: 0.60,
    ChurnReason.PRODUCT_QUALITY: 0.70,
    ChurnReason.ONBOARDING_FAILURE: 0.65,
    ChurnReason.CHAMPION_LEFT: 0.75,
    ChurnReason.CONTRACT_ISSUES: 0.55,
    ChurnReason.UNKNOWN: 0.50,
}

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Customer:
    customer_id: str
    name: str = ""
    email: str = ""
    status: str = "active"
    acquisition_date: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)
    lifetime_value: float = 0.0
    monthly_revenue: float = 0.0
    contract_end_date: Optional[datetime] = None
    churn_risk: ChurnRiskLevel = ChurnRiskLevel.LOW
    churn_score: float = 0.0
    loyalty_points: int = 0
    loyalty_tier: LoyaltyTier = LoyaltyTier.BRONZE
    nps_score: Optional[int] = None
    engagement_score: float = 0.0
    segment_ids: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    health_score: float = 0.0
    contract_type: ContractType = ContractType.MONTHLY
    sentiment_score: float = 0.0

@dataclass
class ChurnPrediction:
    customer_id: str
    risk_level: ChurnRiskLevel
    risk_score: float
    signals: Dict[str, float] = field(default_factory=dict)
    predicted_churn_date: Optional[datetime] = None
    recommended_actions: List[str] = field(default_factory=list)
    confidence: float = 0.0
    calculated_at: datetime = field(default_factory=datetime.now)

@dataclass
class LoyaltyTransaction:
    transaction_id: str
    customer_id: str
    points: int
    transaction_type: str
    description: str = ""
    order_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class LoyaltyReward:
    reward_id: str
    name: str
    description: str
    points_cost: int
    reward_type: str
    value: float = 0.0
    stock: int = -1
    is_active: bool = True

@dataclass
class NPSSurvey:
    survey_id: str
    customer_id: str
    score: Optional[int] = None
    category: Optional[NPSCategory] = None
    feedback: str = ""
    sent_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    status: SurveyStatus = SurveyStatus.DRAFT

@dataclass
class Cohort:
    cohort_id: str
    cohort_type: CohortType
    name: str
    period: str
    customer_ids: Set[str] = field(default_factory=set)
    initial_size: int = 0
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class RetentionStrategyRecord:
    strategy_id: str
    strategy_type: RetentionStrategy
    customer_id: str
    description: str = ""
    status: str = "pending"
    outcome: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    executed_at: Optional[datetime] = None
    result_at: Optional[datetime] = None

@dataclass
class WinbackCampaign:
    campaign_id: str
    name: str
    target_segment: str
    messages: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "draft"
    total_targeted: int = 0
    total_converted: int = 0
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class RetentionMetrics:
    period: str
    total_customers: int = 0
    retained_customers: int = 0
    churned_customers: int = 0
    retention_rate: float = 0.0
    churn_rate: float = 0.0
    nps_score: float = 0.0
    average_ltv: float = 0.0
    revenue_retention: float = 0.0

@dataclass
class RenewalRecord:
    renewal_id: str
    customer_id: str
    contract_type: ContractType
    renewal_date: datetime
    amount: float = 0.0
    status: RenewalStatus = RenewalStatus.PENDING
    assigned_to: str = ""
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    renewed_at: Optional[datetime] = None
    lost_reason: str = ""

@dataclass
class ContractInfo:
    contract_id: str
    customer_id: str
    contract_type: ContractType
    start_date: datetime
    end_date: datetime
    value: float = 0.0
    auto_renew: bool = True
    terms: Dict[str, Any] = field(default_factory=dict)
    status: str = "active"
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class SentimentEntry:
    entry_id: str
    customer_id: str
    text: str
    sentiment: SentimentLevel
    score: float
    source: str = "feedback"
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class EscalationRecord:
    escalation_id: str
    customer_id: str
    reason: EscalationReason
    severity: int = 1
    description: str = ""
    assigned_to: str = ""
    status: str = "open"
    created_at: datetime = field(default_factory=datetime.now)
    resolved_at: Optional[datetime] = None
    resolution: str = ""

@dataclass
class ChurnReasonEntry:
    entry_id: str
    customer_id: str
    reason: ChurnReason
    confidence: float = 0.0
    evidence: List[str] = field(default_factory=list)
    detected_at: datetime = field(default_factory=datetime.now)

@dataclass
class RetentionAlert:
    alert_id: str
    customer_id: str
    alert_type: str
    severity: str
    message: str
    created_at: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False
    acknowledged_by: str = ""

# =============================================================================
# EXCEPTIONS
# =============================================================================

class RetentionError(Exception):
    pass

class ChurnPredictionError(RetentionError):
    pass

class LoyaltyError(RetentionError):
    pass

class SurveyError(RetentionError):
    pass

class ContractError(RetentionError):
    pass

class RenewalError(RetentionError):
    pass

class EscalationError(RetentionError):
    pass

# =============================================================================
# CHURN PREDICTOR
# =============================================================================

class ChurnPredictor:
    def __init__(self):
        self._customers: Dict[str, Customer] = {}
        self._predictions: Dict[str, ChurnPrediction] = {}
        self._signal_weights: Dict[str, float] = dict(CHURN_SIGNALS)
        self._history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self._lock = threading.Lock()

    def register_customer(self, customer: Customer) -> None:
        with self._lock:
            self._customers[customer.customer_id] = customer

    def update_signal(self, customer_id: str, signal: str, value: float) -> None:
        with self._lock:
            self._history[customer_id].append({
                "signal": signal, "value": value,
                "timestamp": datetime.now().isoformat(),
            })

    def predict_churn(self, customer_id: str) -> ChurnPrediction:
        customer = self._customers.get(customer_id)
        if not customer:
            return ChurnPrediction(customer_id=customer_id, risk_level=ChurnRiskLevel.LOW, risk_score=0.0)
        signals: Dict[str, float] = {}
        with self._lock:
            history = list(self._history.get(customer_id, []))
        for entry in history[-50:]:
            signal_name = entry["signal"]
            weight = self._signal_weights.get(signal_name, 0.1)
            signals[signal_name] = max(signals.get(signal_name, 0), entry["value"] * weight)
        days_since_active = (datetime.now() - customer.last_active).days
        if days_since_active > 30:
            signals["inactivity"] = min(days_since_active / 100, 1.0) * 0.4
        if customer.contract_end_date:
            days_to_expiry = (customer.contract_end_date - datetime.now()).days
            if days_to_expiry < 90:
                signals["contract_expiry"] = (90 - days_to_expiry) / 90 * 0.3
        risk_score = min(1.0, sum(signals.values()) / max(1, len(signals)))
        if risk_score >= 0.7:
            risk_level = ChurnRiskLevel.CRITICAL
        elif risk_score >= 0.5:
            risk_level = ChurnRiskLevel.HIGH
        elif risk_score >= 0.3:
            risk_level = ChurnRiskLevel.MEDIUM
        else:
            risk_level = ChurnRiskLevel.LOW
        actions = []
        if risk_score >= 0.5:
            actions.append("Personal outreach from success manager")
            actions.append("Offer retention discount")
        if risk_score >= 0.3:
            actions.append("Send satisfaction survey")
            actions.append("Highlight underused features")
        if customer.contract_end_date:
            days_to_expiry = (customer.contract_end_date - datetime.now()).days
            if days_to_expiry < 60:
                actions.append("Initiate renewal conversation")
        prediction = ChurnPrediction(
            customer_id=customer_id, risk_level=risk_level, risk_score=risk_score,
            signals=signals, recommended_actions=actions, confidence=min(0.95, 0.5 + len(history) * 0.01),
        )
        with self._lock:
            self._predictions[customer_id] = prediction
            customer.churn_risk = risk_level
            customer.churn_score = risk_score
        return prediction

    def predict_all(self) -> List[ChurnPrediction]:
        predictions = []
        with self._lock:
            customer_ids = list(self._customers.keys())
        for cid in customer_ids:
            predictions.append(self.predict_churn(cid))
        predictions.sort(key=lambda p: p.risk_score, reverse=True)
        return predictions

    def get_prediction(self, customer_id: str) -> Optional[ChurnPrediction]:
        with self._lock:
            return self._predictions.get(customer_id)

    def get_high_risk_customers(self, threshold: float = 0.5) -> List[ChurnPrediction]:
        with self._lock:
            return [p for p in self._predictions.values() if p.risk_score >= threshold]

    def get_risk_distribution(self) -> Dict[str, int]:
        dist = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "CRITICAL": 0}
        with self._lock:
            for pred in self._predictions.values():
                dist[pred.risk_level.name] += 1
        return dist

    def get_retention_rate(self, period_days: int = 30) -> float:
        cutoff = datetime.now() - timedelta(days=period_days)
        with self._lock:
            total = len(self._customers)
            active = sum(1 for c in self._customers.values() if c.last_active >= cutoff)
        return active / total if total > 0 else 0.0

    def get_churn_rate(self, period_days: int = 30) -> float:
        return 1.0 - self.get_retention_rate(period_days)

    def get_signal_history(self, customer_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._history.get(customer_id, []))[-limit:]

    def update_signal_weight(self, signal: str, weight: float) -> None:
        with self._lock:
            self._signal_weights[signal] = weight

    def get_signal_weights(self) -> Dict[str, float]:
        with self._lock:
            return dict(self._signal_weights)

    def get_customer_count(self) -> int:
        with self._lock:
            return len(self._customers)

# =============================================================================
# LOYALTY MANAGER
# =============================================================================

class LoyaltyManager:
    def __init__(self):
        self._balances: Dict[str, int] = defaultdict(int)
        self._tiers: Dict[str, LoyaltyTier] = {}
        self._transactions: Dict[str, List[LoyaltyTransaction]] = defaultdict(list)
        self._rewards: Dict[str, LoyaltyReward] = {}
        self._redemptions: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def add_points(self, customer_id: str, points: int, description: str = "",
                   order_id: Optional[str] = None) -> LoyaltyTransaction:
        transaction = LoyaltyTransaction(
            transaction_id=str(uuid.uuid4()), customer_id=customer_id,
            points=points, transaction_type="earn", description=description, order_id=order_id,
        )
        with self._lock:
            self._balances[customer_id] += points
            self._transactions[customer_id].append(transaction)
            self._update_tier(customer_id)
        logger.info("Added %d points to %s (total: %d)", points, customer_id, self._balances[customer_id])
        return transaction

    def redeem_points(self, customer_id: str, points: int, reward_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            if self._balances[customer_id] < points:
                return None
            self._balances[customer_id] -= points
            transaction = LoyaltyTransaction(
                transaction_id=str(uuid.uuid4()), customer_id=customer_id,
                points=-points, transaction_type="redeem",
            )
            self._transactions[customer_id].append(transaction)
            self._update_tier(customer_id)
            reward = self._rewards.get(reward_id)
            redemption = {
                "redemption_id": str(uuid.uuid4()), "customer_id": customer_id,
                "reward_id": reward_id, "points": points,
                "reward_name": reward.name if reward else "Unknown",
                "timestamp": datetime.now().isoformat(),
            }
            self._redemptions.append(redemption)
        logger.info("Redeemed %d points from %s for %s", points, customer_id, reward_id)
        return redemption

    def _update_tier(self, customer_id: str) -> None:
        points = self._balances.get(customer_id, 0)
        new_tier = LoyaltyTier.BRONZE
        for tier in reversed(list(LoyaltyTier)):
            if points >= LOYALTY_TIERS[tier]["min_points"]:
                new_tier = tier
                break
        old_tier = self._tiers.get(customer_id, LoyaltyTier.BRONZE)
        self._tiers[customer_id] = new_tier
        if new_tier != old_tier and list(LoyaltyTier).index(new_tier) > list(LoyaltyTier).index(old_tier):
            logger.info("Customer %s upgraded from %s to %s", customer_id, old_tier.name, new_tier.name)

    def get_balance(self, customer_id: str) -> int:
        with self._lock:
            return self._balances.get(customer_id, 0)

    def get_tier(self, customer_id: str) -> LoyaltyTier:
        with self._lock:
            return self._tiers.get(customer_id, LoyaltyTier.BRONZE)

    def get_tier_benefits(self, customer_id: str) -> Dict[str, Any]:
        tier = self.get_tier(customer_id)
        return {"tier": tier.name, **LOYALTY_TIERS[tier]}

    def get_transaction_history(self, customer_id: str, limit: int = 50) -> List[LoyaltyTransaction]:
        with self._lock:
            return list(self._transactions.get(customer_id, []))[-limit:]

    def register_reward(self, reward: LoyaltyReward) -> None:
        with self._lock:
            self._rewards[reward.reward_id] = reward
        logger.info("Registered reward %s: %s (%d points)", reward.reward_id, reward.name, reward.points_cost)

    def get_available_rewards(self) -> List[LoyaltyReward]:
        with self._lock:
            return [r for r in self._rewards.values() if r.is_active and (r.stock == -1 or r.stock > 0)]

    def get_tier_distribution(self) -> Dict[str, int]:
        dist = {tier.name: 0 for tier in LoyaltyTier}
        with self._lock:
            for tier in self._tiers.values():
                dist[tier.name] += 1
        return dist

    def get_total_points_issued(self) -> int:
        with self._lock:
            return sum(self._balances.values())

    def get_redemption_rate(self) -> float:
        with self._lock:
            total_points = sum(sum(t.points for t in txns if t.points > 0)
                             for txns in self._transactions.values())
            redeemed = sum(abs(t.points) for txns in self._transactions.values()
                         for t in txns if t.transaction_type == "redeem")
        return redeemed / total_points if total_points > 0 else 0.0

    def expire_points(self, customer_id: str, amount: int) -> Optional[LoyaltyTransaction]:
        with self._lock:
            if self._balances[customer_id] < amount:
                return None
            self._balances[customer_id] -= amount
            transaction = LoyaltyTransaction(
                transaction_id=str(uuid.uuid4()), customer_id=customer_id,
                points=-amount, transaction_type="expire", description="Points expired",
            )
            self._transactions[customer_id].append(transaction)
            self._update_tier(customer_id)
        return transaction

    def get_points_summary(self, customer_id: str) -> Dict[str, Any]:
        with self._lock:
            txns = list(self._transactions.get(customer_id, []))
        earned = sum(t.points for t in txns if t.transaction_type == "earn")
        redeemed = sum(abs(t.points) for t in txns if t.transaction_type == "redeem")
        expired = sum(abs(t.points) for t in txns if t.transaction_type == "expire")
        return {
            "customer_id": customer_id,
            "total_earned": earned,
            "total_redeemed": redeemed,
            "total_expired": expired,
            "current_balance": self.get_balance(customer_id),
            "transaction_count": len(txns),
        }

    def get_top_earners(self, limit: int = 10) -> List[Dict[str, Any]]:
        with self._lock:
            sorted_customers = sorted(self._balances.items(), key=lambda x: x[1], reverse=True)
        return [
            {"customer_id": cid, "balance": bal, "tier": self.get_tier(cid).name}
            for cid, bal in sorted_customers[:limit]
        ]

# =============================================================================
# NPS MANAGER
# =============================================================================

class NPSManager:
    def __init__(self):
        self._surveys: Dict[str, NPSSurvey] = {}
        self._responses: List[NPSSurvey] = []
        self._lock = threading.Lock()

    def create_survey(self, customer_id: str) -> NPSSurvey:
        survey = NPSSurvey(
            survey_id=str(uuid.uuid4()), customer_id=customer_id,
            status=SurveyStatus.SENT, sent_at=datetime.now(),
        )
        with self._lock:
            self._surveys[survey.survey_id] = survey
        return survey

    def submit_response(self, survey_id: str, score: int, feedback: str = "") -> Optional[NPSSurvey]:
        with self._lock:
            survey = self._surveys.get(survey_id)
            if not survey:
                return None
            survey.score = max(0, min(10, score))
            if score <= NPS_THRESHOLDS["detractor_max"]:
                survey.category = NPSCategory.DETRACTOR
            elif score <= NPS_THRESHOLDS["passive_max"]:
                survey.category = NPSCategory.PASSIVE
            else:
                survey.category = NPSCategory.PROMOTER
            survey.feedback = feedback
            survey.completed_at = datetime.now()
            survey.status = SurveyStatus.COMPLETED
            self._responses.append(survey)
        return survey

    def calculate_nps(self, period_days: int = 90) -> Dict[str, Any]:
        cutoff = datetime.now() - timedelta(days=period_days)
        with self._lock:
            recent = [s for s in self._responses if s.completed_at and s.completed_at >= cutoff]
        if not recent:
            return {"nps_score": 0, "promoters": 0, "passives": 0, "detractors": 0, "total": 0}
        promoters = sum(1 for s in recent if s.category == NPSCategory.PROMOTER)
        passives = sum(1 for s in recent if s.category == NPSCategory.PASSIVE)
        detractors = sum(1 for s in recent if s.category == NPSCategory.DETRACTOR)
        total = len(recent)
        nps = ((promoters - detractors) / total * 100) if total > 0 else 0
        return {
            "nps_score": round(nps, 1), "promoters": promoters, "passives": passives,
            "detractors": detractors, "total": total,
            "promoter_rate": promoters / total if total > 0 else 0,
            "detractor_rate": detractors / total if total > 0 else 0,
        }

    def get_nps_trend(self, months: int = 12) -> List[Dict[str, Any]]:
        trend = []
        for i in range(months):
            start = datetime.now() - timedelta(days=30 * (i + 1))
            end = datetime.now() - timedelta(days=30 * i)
            with self._lock:
                period_responses = [s for s in self._responses
                                   if s.completed_at and start <= s.completed_at < end]
            if period_responses:
                promoters = sum(1 for s in period_responses if s.category == NPSCategory.PROMOTER)
                detractors = sum(1 for s in period_responses if s.category == NPSCategory.DETRACTOR)
                total = len(period_responses)
                nps = ((promoters - detractors) / total * 100) if total > 0 else 0
            else:
                nps = 0
            trend.append({
                "period": end.strftime("%Y-%m"), "nps_score": round(nps, 1),
                "responses": len(period_responses),
            })
        return list(reversed(trend))

    def get_feedback_summary(self) -> Dict[str, Any]:
        with self._lock:
            responses = list(self._responses)
        by_category = {"PROMOTER": [], "PASSIVE": [], "DETRACTOR": []}
        for s in responses:
            if s.feedback and s.category:
                by_category[s.category.name].append(s.feedback)
        return {
            "total_feedback": sum(len(v) for v in by_category.values()),
            "promoter_themes": by_category["PROMOTER"][:10],
            "detractor_themes": by_category["DETRACTOR"][:10],
        }

    def get_all_surveys(self, status: Optional[SurveyStatus] = None) -> List[NPSSurvey]:
        with self._lock:
            surveys = list(self._surveys.values())
        if status:
            surveys = [s for s in surveys if s.status == status]
        return surveys

    def expire_survey(self, survey_id: str) -> bool:
        with self._lock:
            survey = self._surveys.get(survey_id)
            if survey and survey.status == SurveyStatus.SENT:
                survey.status = SurveyStatus.EXPIRED
                return True
        return False

    def get_response_rate(self) -> float:
        with self._lock:
            total = len(self._surveys)
            completed = sum(1 for s in self._surveys.values() if s.status == SurveyStatus.COMPLETED)
        return completed / total if total > 0 else 0.0

    def get_nps_by_segment(self, segments: Dict[str, List[str]]) -> Dict[str, Dict[str, Any]]:
        results = {}
        for segment_name, customer_ids in segments.items():
            with self._lock:
                segment_responses = [
                    s for s in self._responses if s.customer_id in customer_ids
                ]
            if segment_responses:
                promoters = sum(1 for s in segment_responses if s.category == NPSCategory.PROMOTER)
                detractors = sum(1 for s in segment_responses if s.category == NPSCategory.DETRACTOR)
                total = len(segment_responses)
                nps = ((promoters - detractors) / total * 100) if total > 0 else 0
                results[segment_name] = {"nps_score": round(nps, 1), "total": total}
            else:
                results[segment_name] = {"nps_score": 0, "total": 0}
        return results

# =============================================================================
# COHORT ANALYZER
# =============================================================================

class CohortAnalyzer:
    def __init__(self):
        self._cohorts: Dict[str, Cohort] = {}
        self._retention_data: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._lock = threading.Lock()

    def create_cohort(self, cohort_id: str, cohort_type: CohortType, name: str,
                      period: str, customer_ids: Optional[Set[str]] = None) -> Cohort:
        cohort = Cohort(
            cohort_id=cohort_id, cohort_type=cohort_type, name=name,
            period=period, customer_ids=customer_ids or set(),
            initial_size=len(customer_ids or set()),
        )
        with self._lock:
            self._cohorts[cohort_id] = cohort
        return cohort

    def add_customer_to_cohort(self, cohort_id: str, customer_id: str) -> bool:
        with self._lock:
            cohort = self._cohorts.get(cohort_id)
            if cohort:
                cohort.customer_ids.add(customer_id)
                cohort.initial_size = len(cohort.customer_ids)
                return True
        return False

    def record_period_retention(self, cohort_id: str, period: str, active_count: int) -> None:
        with self._lock:
            self._retention_data[cohort_id][period] = active_count

    def calculate_retention_curve(self, cohort_id: str) -> List[Dict[str, Any]]:
        with self._lock:
            cohort = self._cohorts.get(cohort_id)
            data = dict(self._retention_data.get(cohort_id, {}))
        if not cohort or not data:
            return []
        initial = cohort.initial_size or 1
        periods = sorted(data.keys())
        curve = []
        for i, period in enumerate(periods):
            active = data[period]
            retention = active / initial * 100
            curve.append({
                "period": period, "period_number": i,
                "active_customers": active, "retention_rate": round(retention, 1),
            })
        return curve

    def get_cohort_summary(self) -> Dict[str, Any]:
        summaries = []
        with self._lock:
            for cohort_id, cohort in self._cohorts.items():
                data = self._retention_data.get(cohort_id, {})
                periods = sorted(data.keys())
                last_period = data[periods[-1]] if periods else cohort.initial_size
                initial = cohort.initial_size or 1
                summaries.append({
                    "cohort_id": cohort_id, "name": cohort.name,
                    "type": cohort.cohort_type.name, "period": cohort.period,
                    "initial_size": cohort.initial_size,
                    "current_size": last_period,
                    "retention_rate": round(last_period / initial * 100, 1),
                })
        return {"cohorts": summaries, "total": len(summaries)}

    def compare_cohorts(self, cohort_ids: List[str]) -> Dict[str, Any]:
        comparison = {}
        for cid in cohort_ids:
            curve = self.calculate_retention_curve(cid)
            if curve:
                comparison[cid] = {
                    "initial": curve[0]["active_customers"] if curve else 0,
                    "final": curve[-1]["active_customers"] if curve else 0,
                    "retention_rate": curve[-1]["retention_rate"] if curve else 0,
                }
        return comparison

    def get_all_cohorts(self) -> List[Cohort]:
        with self._lock:
            return list(self._cohorts.values())

    def get_best_cohort(self) -> Optional[Dict[str, Any]]:
        summaries = self.get_cohort_summary()["cohorts"]
        if not summaries:
            return None
        return max(summaries, key=lambda s: s["retention_rate"])

    def get_worst_cohort(self) -> Optional[Dict[str, Any]]:
        summaries = self.get_cohort_summary()["cohorts"]
        if not summaries:
            return None
        return min(summaries, key=lambda s: s["retention_rate"])

# =============================================================================
# RETENTION STRATEGY ENGINE
# =============================================================================

class RetentionStrategyEngine:
    def __init__(self, churn_predictor: ChurnPredictor):
        self._churn_predictor = churn_predictor
        self._strategies: Dict[str, RetentionStrategyRecord] = {}
        self._strategy_templates: Dict[RetentionStrategy, Dict[str, Any]] = {
            RetentionStrategy.ENGAGEMENT_INCREASE: {
                "description": "Increase engagement through personalized content",
                "trigger": "churn_score >= 0.3",
            },
            RetentionStrategy.DISCOUNT_OFFER: {
                "description": "Offer retention discount",
                "trigger": "churn_score >= 0.5",
            },
            RetentionStrategy.PERSONAL_OUTREACH: {
                "description": "Personal outreach from success manager",
                "trigger": "churn_score >= 0.7",
            },
            RetentionStrategy.FEATURE_HIGHLIGHT: {
                "description": "Highlight underused features",
                "trigger": "engagement_score < 40",
            },
            RetentionStrategy.LOYALTY_REWARD: {
                "description": "Bonus loyalty points for retention",
                "trigger": "loyalty_tier in [GOLD, PLATINUM, DIAMOND]",
            },
            RetentionStrategy.EXIT_SURVEY: {
                "description": "Send exit survey to understand churn reasons",
                "trigger": "churn_score >= 0.8",
            },
            RetentionStrategy.SUCCESS_MANAGER: {
                "description": "Assign dedicated success manager",
                "trigger": "ltp > 10000 AND churn_score >= 0.4",
            },
        }
        self._lock = threading.Lock()

    def get_recommended_strategies(self, customer_id: str) -> List[RetentionStrategy]:
        prediction = self._churn_predictor.get_prediction(customer_id)
        if not prediction:
            return []
        recommended = []
        for strategy, template in self._strategy_templates.items():
            if prediction.risk_score >= 0.3 and strategy == RetentionStrategy.ENGAGEMENT_INCREASE:
                recommended.append(strategy)
            if prediction.risk_score >= 0.5 and strategy == RetentionStrategy.DISCOUNT_OFFER:
                recommended.append(strategy)
            if prediction.risk_score >= 0.7 and strategy == RetentionStrategy.PERSONAL_OUTREACH:
                recommended.append(strategy)
            if prediction.risk_score >= 0.8 and strategy == RetentionStrategy.EXIT_SURVEY:
                recommended.append(strategy)
        return recommended

    def execute_strategy(self, customer_id: str, strategy: RetentionStrategy,
                         description: str = "") -> RetentionStrategyRecord:
        record = RetentionStrategyRecord(
            strategy_id=str(uuid.uuid4()), strategy_type=strategy,
            customer_id=customer_id, description=description or self._strategy_templates.get(strategy, {}).get("description", ""),
            status="executed", executed_at=datetime.now(),
        )
        with self._lock:
            self._strategies[record.strategy_id] = record
        logger.info("Executed strategy %s for %s", strategy.name, customer_id)
        return record

    def record_outcome(self, strategy_id: str, outcome: str) -> bool:
        with self._lock:
            record = self._strategies.get(strategy_id)
            if record:
                record.outcome = outcome
                record.result_at = datetime.now()
                return True
        return False

    def get_strategy_stats(self) -> Dict[str, Any]:
        with self._lock:
            records = list(self._strategies.values())
        by_strategy = defaultdict(lambda: {"count": 0, "converted": 0})
        for r in records:
            by_strategy[r.strategy_type.name]["count"] += 1
            if r.outcome == "converted":
                by_strategy[r.strategy_type.name]["converted"] += 1
        stats = {}
        for name, data in by_strategy.items():
            stats[name] = {
                **data,
                "conversion_rate": data["converted"] / data["count"] if data["count"] > 0 else 0,
            }
        return stats

    def get_all_strategies(self) -> List[RetentionStrategyRecord]:
        with self._lock:
            return list(self._strategies.values())

    def get_strategies_for_customer(self, customer_id: str) -> List[RetentionStrategyRecord]:
        with self._lock:
            return [s for s in self._strategies.values() if s.customer_id == customer_id]

    def cancel_strategy(self, strategy_id: str) -> bool:
        with self._lock:
            record = self._strategies.get(strategy_id)
            if record and record.status == "executed":
                record.status = "cancelled"
                record.result_at = datetime.now()
                return True
        return False

# =============================================================================
# WINBACK MANAGER
# =============================================================================

class WinbackManager:
    def __init__(self):
        self._campaigns: Dict[str, WinbackCampaign] = {}
        self._enrollments: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def create_campaign(self, campaign_id: str, name: str, target_segment: str,
                        messages: Optional[List[Dict[str, Any]]] = None) -> WinbackCampaign:
        campaign = WinbackCampaign(
            campaign_id=campaign_id, name=name, target_segment=target_segment,
            messages=messages or [],
        )
        with self._lock:
            self._campaigns[campaign_id] = campaign
        return campaign

    def enroll_customer(self, campaign_id: str, customer_id: str) -> bool:
        with self._lock:
            campaign = self._campaigns.get(campaign_id)
            if not campaign:
                return False
            enrollment_id = f"{campaign_id}_{customer_id}"
            self._enrollments[enrollment_id] = {
                "campaign_id": campaign_id, "customer_id": customer_id,
                "status": "active", "step": 0, "enrolled_at": datetime.now(),
            }
            campaign.total_targeted += 1
        return True

    def advance_enrollment(self, campaign_id: str, customer_id: str,
                           action: str = "opened") -> bool:
        with self._lock:
            enrollment_id = f"{campaign_id}_{customer_id}"
            enrollment = self._enrollments.get(enrollment_id)
            if not enrollment:
                return False
            if action == "converted":
                enrollment["status"] = "converted"
                campaign = self._campaigns.get(campaign_id)
                if campaign:
                    campaign.total_converted += 1
                return True
            enrollment["step"] += 1
            enrollment["status"] = "sent"
        return True

    def get_campaign_stats(self, campaign_id: str) -> Dict[str, Any]:
        with self._lock:
            campaign = self._campaigns.get(campaign_id)
            enrollments = [e for e in self._enrollments.values() if e["campaign_id"] == campaign_id]
        if not campaign:
            return {"error": "Campaign not found"}
        converted = sum(1 for e in enrollments if e["status"] == "converted")
        return {
            "campaign_id": campaign_id, "name": campaign.name,
            "total_targeted": campaign.total_targeted,
            "total_converted": campaign.total_converted,
            "conversion_rate": campaign.total_converted / campaign.total_targeted if campaign.total_targeted > 0 else 0,
            "active_enrollments": sum(1 for e in enrollments if e["status"] == "active"),
        }

    def get_all_campaigns(self) -> List[WinbackCampaign]:
        with self._lock:
            return list(self._campaigns.values())

    def pause_campaign(self, campaign_id: str) -> bool:
        with self._lock:
            campaign = self._campaigns.get(campaign_id)
            if campaign:
                campaign.status = "paused"
                return True
        return False

    def resume_campaign(self, campaign_id: str) -> bool:
        with self._lock:
            campaign = self._campaigns.get(campaign_id)
            if campaign and campaign.status == "paused":
                campaign.status = "active"
                return True
        return False

# =============================================================================
# CUSTOMER HEALTH MONITOR
# =============================================================================

class CustomerHealthMonitor:
    def __init__(self):
        self._health_scores: Dict[str, float] = {}
        self._health_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._weight_config: Dict[str, float] = dict(HEALTH_SCORE_WEIGHTS)
        self._lock = threading.Lock()

    def calculate_health_score(self, customer_id: str, engagement: float = 0.5,
                               satisfaction: float = 0.5, financial: float = 0.5,
                               support: float = 0.5, contract: float = 0.5) -> float:
        weights = self._weight_config
        score = (
            engagement * weights["engagement"] +
            satisfaction * weights["satisfaction"] +
            financial * weights["financial"] +
            support * weights["support"] +
            contract * weights["contract"]
        )
        score = max(0.0, min(1.0, score))
        with self._lock:
            self._health_scores[customer_id] = score
            self._health_history[customer_id].append({
                "score": score,
                "timestamp": datetime.now().isoformat(),
                "components": {
                    "engagement": engagement, "satisfaction": satisfaction,
                    "financial": financial, "support": support, "contract": contract,
                },
            })
        return score

    def get_health_score(self, customer_id: str) -> float:
        with self._lock:
            return self._health_scores.get(customer_id, 0.0)

    def get_health_trend(self, customer_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._health_history.get(customer_id, []))[-limit:]

    def get_health_distribution(self) -> Dict[str, int]:
        dist = {"excellent": 0, "good": 0, "fair": 0, "poor": 0, "critical": 0}
        with self._lock:
            for score in self._health_scores.values():
                if score >= 0.8:
                    dist["excellent"] += 1
                elif score >= 0.6:
                    dist["good"] += 1
                elif score >= 0.4:
                    dist["fair"] += 1
                elif score >= 0.2:
                    dist["poor"] += 1
                else:
                    dist["critical"] += 1
        return dist

    def get_at_risk_customers(self, threshold: float = 0.3) -> List[str]:
        with self._lock:
            return [cid for cid, score in self._health_scores.items() if score < threshold]

    def update_weight(self, component: str, weight: float) -> None:
        with self._lock:
            if component in self._weight_config:
                self._weight_config[component] = weight
                total = sum(self._weight_config.values())
                if abs(total - 1.0) > 0.01:
                    logger.warning("Health weight total is %.2f, expected 1.0", total)

# =============================================================================
# RENEWAL MANAGER
# =============================================================================

class RenewalManager:
    def __init__(self):
        self._renewals: Dict[str, RenewalRecord] = {}
        self._lock = threading.Lock()

    def create_renewal(self, customer_id: str, contract_type: ContractType,
                       renewal_date: datetime, amount: float = 0.0) -> RenewalRecord:
        record = RenewalRecord(
            renewal_id=str(uuid.uuid4()), customer_id=customer_id,
            contract_type=contract_type, renewal_date=renewal_date, amount=amount,
        )
        with self._lock:
            self._renewals[record.renewal_id] = record
        logger.info("Created renewal %s for %s (due %s)", record.renewal_id, customer_id, renewal_date.date())
        return record

    def update_renewal_status(self, renewal_id: str, status: RenewalStatus,
                              notes: str = "") -> bool:
        with self._lock:
            record = self._renewals.get(renewal_id)
            if record:
                record.status = status
                record.notes = notes or record.notes
                record.updated_at = datetime.now()
                if status == RenewalStatus.RENEWED:
                    record.renewed_at = datetime.now()
                elif status in (RenewalStatus.LOST, RenewalStatus.CANCELLED):
                    record.lost_reason = notes
                return True
        return False

    def get_upcoming_renewals(self, days: int = 30) -> List[RenewalRecord]:
        cutoff = datetime.now() + timedelta(days=days)
        with self._lock:
            return [
                r for r in self._renewals.values()
                if r.renewal_date <= cutoff and r.status in (RenewalStatus.PENDING, RenewalStatus.INITIATED)
            ]

    def get_renewal_stats(self) -> Dict[str, Any]:
        with self._lock:
            records = list(self._renewals.values())
        total = len(records)
        renewed = sum(1 for r in records if r.status == RenewalStatus.RENEWED)
        lost = sum(1 for r in records if r.status in (RenewalStatus.LOST, RenewalStatus.CANCELLED))
        pending = sum(1 for r in records if r.status == RenewalStatus.PENDING)
        revenue_renewed = sum(r.amount for r in records if r.status == RenewalStatus.RENEWED)
        revenue_lost = sum(r.amount for r in records if r.status == RenewalStatus.LOST)
        return {
            "total": total, "renewed": renewed, "lost": lost, "pending": pending,
            "renewal_rate": renewed / total if total > 0 else 0.0,
            "revenue_renewed": revenue_renewed, "revenue_lost": revenue_lost,
        }

    def get_renewal_by_customer(self, customer_id: str) -> List[RenewalRecord]:
        with self._lock:
            return [r for r in self._renewals.values() if r.customer_id == customer_id]

# =============================================================================
# CONTRACT TRACKER
# =============================================================================

class ContractTracker:
    def __init__(self):
        self._contracts: Dict[str, ContractInfo] = {}
        self._lock = threading.Lock()

    def create_contract(self, customer_id: str, contract_type: ContractType,
                        start_date: datetime, end_date: datetime,
                        value: float = 0.0, auto_renew: bool = True) -> ContractInfo:
        contract = ContractInfo(
            contract_id=str(uuid.uuid4()), customer_id=customer_id,
            contract_type=contract_type, start_date=start_date, end_date=end_date,
            value=value, auto_renew=auto_renew,
        )
        with self._lock:
            self._contracts[contract.contract_id] = contract
        return contract

    def get_expiring_contracts(self, days: int = 30) -> List[ContractInfo]:
        cutoff = datetime.now() + timedelta(days=days)
        with self._lock:
            return [
                c for c in self._contracts.values()
                if c.end_date <= cutoff and c.status == "active"
            ]

    def get_contracts_for_customer(self, customer_id: str) -> List[ContractInfo]:
        with self._lock:
            return [c for c in self._contracts.values() if c.customer_id == customer_id]

    def terminate_contract(self, contract_id: str, reason: str = "") -> bool:
        with self._lock:
            contract = self._contracts.get(contract_id)
            if contract and contract.status == "active":
                contract.status = "terminated"
                contract.terms["termination_reason"] = reason
                return True
        return False

    def get_contract_stats(self) -> Dict[str, Any]:
        with self._lock:
            contracts = list(self._contracts.values())
        active = sum(1 for c in contracts if c.status == "active")
        total_value = sum(c.value for c in contracts if c.status == "active")
        by_type = defaultdict(lambda: {"count": 0, "value": 0.0})
        for c in contracts:
            by_type[c.contract_type.name]["count"] += 1
            by_type[c.contract_type.name]["value"] += c.value
        return {
            "total": len(contracts), "active": active,
            "total_value": total_value, "by_type": dict(by_type),
        }

# =============================================================================
# SENTIMENT ANALYZER
# =============================================================================

class SentimentAnalyzer:
    def __init__(self):
        self._entries: List[SentimentEntry] = []
        self._customer_sentiment: Dict[str, List[float]] = defaultdict(list)
        self._lock = threading.Lock()

    def analyze_text(self, text: str) -> Tuple[SentimentLevel, float]:
        words = text.lower().split()
        positive_count = sum(1 for w in words if w in SENTIMENT_KEYWORDS_POSITIVE)
        negative_count = sum(1 for w in words if w in SENTIMENT_KEYWORDS_NEGATIVE)
        total = len(words) or 1
        score = (positive_count - negative_count) / total
        score = max(-1.0, min(1.0, score))
        if score >= 0.4:
            level = SentimentLevel.VERY_POSITIVE
        elif score >= 0.1:
            level = SentimentLevel.POSITIVE
        elif score >= -0.1:
            level = SentimentLevel.NEUTRAL
        elif score >= -0.4:
            level = SentimentLevel.NEGATIVE
        else:
            level = SentimentLevel.VERY_NEGATIVE
        return level, score

    def add_entry(self, customer_id: str, text: str, source: str = "feedback") -> SentimentEntry:
        level, score = self.analyze_text(text)
        entry = SentimentEntry(
            entry_id=str(uuid.uuid4()), customer_id=customer_id,
            text=text, sentiment=level, score=score, source=source,
        )
        with self._lock:
            self._entries.append(entry)
            self._customer_sentiment[customer_id].append(score)
        return entry

    def get_average_sentiment(self, customer_id: str) -> float:
        with self._lock:
            scores = self._customer_sentiment.get(customer_id, [])
        return statistics.mean(scores) if scores else 0.0

    def get_sentiment_distribution(self) -> Dict[str, int]:
        dist = {level.name: 0 for level in SentimentLevel}
        with self._lock:
            for entry in self._entries:
                dist[entry.sentiment.name] += 1
        return dist

    def get_negative_customers(self, threshold: float = -0.2) -> List[str]:
        with self._lock:
            return [
                cid for cid, scores in self._customer_sentiment.items()
                if scores and statistics.mean(scores) < threshold
            ]

    def get_entries_for_customer(self, customer_id: str, limit: int = 20) -> List[SentimentEntry]:
        with self._lock:
            return [e for e in self._entries if e.customer_id == customer_id][-limit:]

    def get_trend(self, customer_id: str, limit: int = 5) -> List[Dict[str, Any]]:
        with self._lock:
            entries = [e for e in self._entries if e.customer_id == customer_id][-limit:]
        return [
            {"sentiment": e.sentiment.name, "score": e.score, "source": e.source,
             "timestamp": e.timestamp.isoformat()}
            for e in entries
        ]

# =============================================================================
# ESCALATION ENGINE
# =============================================================================

class EscalationEngine:
    def __init__(self):
        self._escalations: Dict[str, EscalationRecord] = {}
        self._rules: Dict[EscalationReason, Dict[str, Any]] = {
            EscalationReason.HIGH_CHURN_RISK: {"severity": 4, "auto_assign": True},
            EscalationReason.NEGATIVE_SENTIMENT: {"severity": 3, "auto_assign": False},
            EscalationReason.PAYMENT_DEFAULT: {"severity": 5, "auto_assign": True},
            EscalationReason.SUPPORT_ESCALATION: {"severity": 3, "auto_assign": True},
            EscalationReason.COMPETITOR_THREAT: {"severity": 4, "auto_assign": False},
            EscalationReason.CONTRACT_EXPIRY: {"severity": 2, "auto_assign": True},
            EscalationReason.USAGE_DECLINE: {"severity": 3, "auto_assign": False},
            EscalationReason.EXECUTIVE_SPONSOR_LOST: {"severity": 5, "auto_assign": True},
        }
        self._lock = threading.Lock()

    def create_escalation(self, customer_id: str, reason: EscalationReason,
                          description: str = "", assigned_to: str = "") -> EscalationRecord:
        rule = self._rules.get(reason, {"severity": 3})
        escalation = EscalationRecord(
            escalation_id=str(uuid.uuid4()), customer_id=customer_id,
            reason=reason, severity=rule["severity"], description=description,
            assigned_to=assigned_to or ("auto" if rule.get("auto_assign") else ""),
        )
        with self._lock:
            self._escalations[escalation.escalation_id] = escalation
        logger.warning("Escalation %s created for %s: %s (severity %d)",
                       escalation.escalation_id, customer_id, reason.name, escalation.severity)
        return escalation

    def resolve_escalation(self, escalation_id: str, resolution: str = "") -> bool:
        with self._lock:
            record = self._escalations.get(escalation_id)
            if record and record.status == "open":
                record.status = "resolved"
                record.resolved_at = datetime.now()
                record.resolution = resolution
                return True
        return False

    def get_open_escalations(self) -> List[EscalationRecord]:
        with self._lock:
            return [e for e in self._escalations.values() if e.status == "open"]

    def get_escalations_for_customer(self, customer_id: str) -> List[EscalationRecord]:
        with self._lock:
            return [e for e in self._escalations.values() if e.customer_id == customer_id]

    def get_escalation_stats(self) -> Dict[str, Any]:
        with self._lock:
            records = list(self._escalations.values())
        total = len(records)
        open_count = sum(1 for r in records if r.status == "open")
        resolved = sum(1 for r in records if r.status == "resolved")
        by_reason = defaultdict(int)
        for r in records:
            by_reason[r.reason.name] += 1
        return {
            "total": total, "open": open_count, "resolved": resolved,
            "by_reason": dict(by_reason),
        }

    def update_rule(self, reason: EscalationReason, severity: int, auto_assign: bool = False) -> None:
        with self._lock:
            self._rules[reason] = {"severity": severity, "auto_assign": auto_assign}

# =============================================================================
# CHURN REASON ANALYZER
# =============================================================================

class ChurnReasonAnalyzer:
    def __init__(self):
        self._entries: List[ChurnReasonEntry] = []
        self._reason_counts: Dict[str, int] = defaultdict(int)
        self._lock = threading.Lock()

    def add_churn_reason(self, customer_id: str, reason: ChurnReason,
                         evidence: Optional[List[str]] = None, confidence: float = 0.5) -> ChurnReasonEntry:
        entry = ChurnReasonEntry(
            entry_id=str(uuid.uuid4()), customer_id=customer_id,
            reason=reason, confidence=confidence, evidence=evidence or [],
        )
        with self._lock:
            self._entries.append(entry)
            self._reason_counts[reason.name] += 1
        return entry

    def get_reason_distribution(self) -> Dict[str, int]:
        with self._lock:
            return dict(self._reason_counts)

    def get_reasons_for_customer(self, customer_id: str) -> List[ChurnReasonEntry]:
        with self._lock:
            return [e for e in self._entries if e.customer_id == customer_id]

    def get_top_reasons(self, limit: int = 5) -> List[Dict[str, Any]]:
        with self._lock:
            sorted_reasons = sorted(self._reason_counts.items(), key=lambda x: x[1], reverse=True)
        return [{"reason": r, "count": c} for r, c in sorted_reasons[:limit]]

    def get_recoverable_rate(self) -> float:
        with self._lock:
            if not self._entries:
                return 0.0
            recoverable = sum(
                1 for e in self._entries
                if CHURN_REASON_WEIGHTS.get(e.reason, 0.5) < 0.8
            )
        return recoverable / len(self._entries)

    def get_avg_confidence(self) -> float:
        with self._lock:
            if not self._entries:
                return 0.0
            return statistics.mean(e.confidence for e in self._entries)

# =============================================================================
# RETENTION DASHBOARD
# =============================================================================

class RetentionDashboard:
    def __init__(self):
        self._alerts: List[RetentionAlert] = []
        self._snapshots: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def add_alert(self, customer_id: str, alert_type: str, severity: str,
                  message: str) -> RetentionAlert:
        alert = RetentionAlert(
            alert_id=str(uuid.uuid4()), customer_id=customer_id,
            alert_type=alert_type, severity=severity, message=message,
        )
        with self._lock:
            self._alerts.append(alert)
        return alert

    def acknowledge_alert(self, alert_id: str, acknowledged_by: str = "") -> bool:
        with self._lock:
            for alert in self._alerts:
                if alert.alert_id == alert_id and not alert.acknowledged:
                    alert.acknowledged = True
                    alert.acknowledged_by = acknowledged_by
                    return True
        return False

    def get_active_alerts(self) -> List[RetentionAlert]:
        with self._lock:
            return [a for a in self._alerts if not a.acknowledged]

    def get_alerts_by_severity(self, severity: str) -> List[RetentionAlert]:
        with self._lock:
            return [a for a in self._alerts if a.severity == severity and not a.acknowledged]

    def take_snapshot(self, metrics: Dict[str, Any]) -> None:
        snapshot = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
        }
        with self._lock:
            self._snapshots.append(snapshot)

    def get_snapshots(self, limit: int = 10) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._snapshots)[-limit:]

    def get_alert_summary(self) -> Dict[str, int]:
        summary = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        with self._lock:
            for alert in self._alerts:
                if not alert.acknowledged:
                    sev = alert.severity.lower()
                    if sev in summary:
                        summary[sev] += 1
        return summary

    def clear_acknowledged(self) -> int:
        with self._lock:
            before = len(self._alerts)
            self._alerts = [a for a in self._alerts if not a.acknowledged]
            return before - len(self._alerts)

# =============================================================================
# CONFIG
# =============================================================================

class Config:
    def __init__(self, churn_threshold: float = 0.5, nps_survey_interval_days: int = 90,
                 loyalty_points_per_dollar: float = 10.0, retention_lookback_days: int = 30,
                 health_alert_threshold: float = 0.3, renewal_warning_days: int = 30,
                 escalation_auto_assign: bool = True, sentiment_analysis_enabled: bool = True):
        self.churn_threshold = churn_threshold
        self.nps_survey_interval_days = nps_survey_interval_days
        self.loyalty_points_per_dollar = loyalty_points_per_dollar
        self.retention_lookback_days = retention_lookback_days
        self.health_alert_threshold = health_alert_threshold
        self.renewal_warning_days = renewal_warning_days
        self.escalation_auto_assign = escalation_auto_assign
        self.sentiment_analysis_enabled = sentiment_analysis_enabled

# =============================================================================
# MAIN AGENT CLASS
# =============================================================================

class CustomerRetentionAgent:
    def __init__(self, config: Optional[Config] = None):
        self._config = config or Config()
        self._churn_predictor = ChurnPredictor()
        self._loyalty_manager = LoyaltyManager()
        self._nps_manager = NPSManager()
        self._cohort_analyzer = CohortAnalyzer()
        self._strategy_engine = RetentionStrategyEngine(self._churn_predictor)
        self._winback_manager = WinbackManager()
        self._health_monitor = CustomerHealthMonitor()
        self._renewal_manager = RenewalManager()
        self._contract_tracker = ContractTracker()
        self._sentiment_analyzer = SentimentAnalyzer()
        self._escalation_engine = EscalationEngine()
        self._churn_reason_analyzer = ChurnReasonAnalyzer()
        self._dashboard = RetentionDashboard()
        self._customers: Dict[str, Customer] = {}
        self._running = False
        self._lock = threading.Lock()

    def initialize(self) -> Dict[str, Any]:
        logger.info("Initializing CustomerRetentionAgent")
        self._running = True
        return {"status": "initialized", "config": {
            "churn_threshold": self._config.churn_threshold,
            "nps_interval": self._config.nps_survey_interval_days,
            "health_alert_threshold": self._config.health_alert_threshold,
            "renewal_warning_days": self._config.renewal_warning_days,
        }}

    def shutdown(self) -> Dict[str, Any]:
        self._running = False
        logger.info("CustomerRetentionAgent shutdown complete")
        return {"status": "shutdown"}

    def register_customer(self, customer_id: str, name: str = "", email: str = "",
                          monthly_revenue: float = 0.0, **kwargs) -> Dict[str, Any]:
        customer = Customer(
            customer_id=customer_id, name=name, email=email,
            monthly_revenue=monthly_revenue,
            contract_end_date=kwargs.get("contract_end_date"),
            contract_type=kwargs.get("contract_type", ContractType.MONTHLY),
        )
        with self._lock:
            self._customers[customer_id] = customer
        self._churn_predictor.register_customer(customer)
        return {"customer_id": customer_id, "status": "registered"}

    def update_customer_signal(self, customer_id: str, signal: str, value: float) -> Dict[str, Any]:
        self._churn_predictor.update_signal(customer_id, signal, value)
        return {"customer_id": customer_id, "signal": signal, "value": value}

    def predict_churn(self, customer_id: str) -> Dict[str, Any]:
        pred = self._churn_predictor.predict_churn(customer_id)
        return {
            "customer_id": customer_id, "risk_level": pred.risk_level.name,
            "risk_score": round(pred.risk_score, 3),
            "signals": pred.signals, "actions": pred.recommended_actions,
            "confidence": round(pred.confidence, 2),
        }

    def predict_all_churn(self) -> Dict[str, Any]:
        predictions = self._churn_predictor.predict_all()
        return {
            "predictions": [{
                "customer_id": p.customer_id, "risk_level": p.risk_level.name,
                "risk_score": round(p.risk_score, 3),
            } for p in predictions],
            "risk_distribution": self._churn_predictor.get_risk_distribution(),
        }

    def add_loyalty_points(self, customer_id: str, points: int, description: str = "") -> Dict[str, Any]:
        txn = self._loyalty_manager.add_points(customer_id, points, description)
        return {"transaction_id": txn.transaction_id, "points": points,
                "total": self._loyalty_manager.get_balance(customer_id)}

    def redeem_loyalty_points(self, customer_id: str, points: int, reward_id: str) -> Dict[str, Any]:
        result = self._loyalty_manager.redeem_points(customer_id, points, reward_id)
        if not result:
            return {"error": "Insufficient points or invalid reward"}
        return result

    def get_loyalty_info(self, customer_id: str) -> Dict[str, Any]:
        return {
            "customer_id": customer_id,
            "balance": self._loyalty_manager.get_balance(customer_id),
            "tier": self._loyalty_manager.get_tier(customer_id).name,
            "benefits": self._loyalty_manager.get_tier_benefits(customer_id),
        }

    def register_loyalty_reward(self, reward_id: str, name: str, points_cost: int,
                                reward_type: str = "discount", value: float = 0.0) -> Dict[str, Any]:
        reward = LoyaltyReward(
            reward_id=reward_id, name=name, description=name,
            points_cost=points_cost, reward_type=reward_type, value=value,
        )
        self._loyalty_manager.register_reward(reward)
        return {"reward_id": reward_id, "name": name, "points_cost": points_cost}

    def send_nps_survey(self, customer_id: str) -> Dict[str, Any]:
        survey = self._nps_manager.create_survey(customer_id)
        return {"survey_id": survey.survey_id, "customer_id": customer_id, "status": "sent"}

    def submit_nps_response(self, survey_id: str, score: int, feedback: str = "") -> Dict[str, Any]:
        survey = self._nps_manager.submit_response(survey_id, score, feedback)
        if not survey:
            return {"error": "Survey not found"}
        return {"survey_id": survey_id, "score": score, "category": survey.category.name}

    def get_nps_score(self) -> Dict[str, Any]:
        return self._nps_manager.calculate_nps()

    def get_nps_trend(self, months: int = 12) -> List[Dict[str, Any]]:
        return self._nps_manager.get_nps_trend(months)

    def create_cohort(self, cohort_id: str, name: str, period: str,
                      customer_ids: Optional[Set[str]] = None) -> Dict[str, Any]:
        cohort = self._cohort_analyzer.create_cohort(
            cohort_id, CohortType.MONTHLY, name, period, customer_ids,
        )
        return {"cohort_id": cohort_id, "name": name, "size": cohort.initial_size}

    def get_retention_curve(self, cohort_id: str) -> List[Dict[str, Any]]:
        return self._cohort_analyzer.calculate_retention_curve(cohort_id)

    def get_retention_rate(self, period_days: int = 30) -> Dict[str, Any]:
        rate = self._churn_predictor.get_retention_rate(period_days)
        return {"retention_rate": round(rate, 4), "period_days": period_days}

    def get_churn_rate(self, period_days: int = 30) -> Dict[str, Any]:
        rate = self._churn_predictor.get_churn_rate(period_days)
        return {"churn_rate": round(rate, 4), "period_days": period_days}

    def get_retention_strategies(self, customer_id: str) -> List[str]:
        strategies = self._strategy_engine.get_recommended_strategies(customer_id)
        return [s.name for s in strategies]

    def execute_retention_strategy(self, customer_id: str, strategy_name: str) -> Dict[str, Any]:
        strategy = RetentionStrategy[strategy_name]
        record = self._strategy_engine.execute_strategy(customer_id, strategy)
        return {"strategy_id": record.strategy_id, "strategy": strategy_name, "status": "executed"}

    def create_winback_campaign(self, campaign_id: str, name: str, target_segment: str) -> Dict[str, Any]:
        campaign = self._winback_manager.create_campaign(campaign_id, name, target_segment)
        return {"campaign_id": campaign_id, "name": name, "status": "draft"}

    def enroll_winback(self, campaign_id: str, customer_id: str) -> Dict[str, Any]:
        success = self._winback_manager.enroll_customer(campaign_id, customer_id)
        return {"enrolled": success, "campaign_id": campaign_id, "customer_id": customer_id}

    def get_winback_stats(self, campaign_id: str) -> Dict[str, Any]:
        return self._winback_manager.get_campaign_stats(campaign_id)

    def get_cohort_summary(self) -> Dict[str, Any]:
        return self._cohort_analyzer.get_cohort_summary()

    def get_loyalty_tier_distribution(self) -> Dict[str, int]:
        return self._loyalty_manager.get_tier_distribution()

    def get_strategy_stats(self) -> Dict[str, Any]:
        return self._strategy_engine.get_strategy_stats()

    def calculate_health_score(self, customer_id: str, engagement: float = 0.5,
                               satisfaction: float = 0.5, financial: float = 0.5,
                               support: float = 0.5, contract: float = 0.5) -> Dict[str, Any]:
        score = self._health_monitor.calculate_health_score(
            customer_id, engagement, satisfaction, financial, support, contract,
        )
        if score < self._config.health_alert_threshold:
            self._dashboard.add_alert(
                customer_id, "low_health", "high",
                f"Health score {score:.2f} below threshold {self._config.health_alert_threshold}",
            )
        return {"customer_id": customer_id, "health_score": round(score, 3)}

    def create_renewal(self, customer_id: str, contract_type: str,
                       renewal_date: datetime, amount: float = 0.0) -> Dict[str, Any]:
        ct = ContractType[contract_type]
        record = self._renewal_manager.create_renewal(customer_id, ct, renewal_date, amount)
        return {"renewal_id": record.renewal_id, "customer_id": customer_id, "status": record.status.name}

    def get_upcoming_renewals(self, days: int = 30) -> List[Dict[str, Any]]:
        renewals = self._renewal_manager.get_upcoming_renewals(days)
        return [{"renewal_id": r.renewal_id, "customer_id": r.customer_id,
                 "renewal_date": r.renewal_date.isoformat(), "amount": r.amount,
                 "status": r.status.name} for r in renewals]

    def create_contract(self, customer_id: str, contract_type: str,
                        start_date: datetime, end_date: datetime,
                        value: float = 0.0, auto_renew: bool = True) -> Dict[str, Any]:
        ct = ContractType[contract_type]
        contract = self._contract_tracker.create_contract(
            customer_id, ct, start_date, end_date, value, auto_renew,
        )
        return {"contract_id": contract.contract_id, "customer_id": customer_id,
                "type": ct.name, "status": contract.status}

    def analyze_sentiment(self, customer_id: str, text: str,
                          source: str = "feedback") -> Dict[str, Any]:
        entry = self._sentiment_analyzer.add_entry(customer_id, text, source)
        return {"entry_id": entry.entry_id, "sentiment": entry.sentiment.name,
                "score": round(entry.score, 3)}

    def create_escalation(self, customer_id: str, reason: str,
                          description: str = "") -> Dict[str, Any]:
        er = EscalationReason[reason]
        record = self._escalation_engine.create_escalation(customer_id, er, description)
        return {"escalation_id": record.escalation_id, "severity": record.severity,
                "status": record.status}

    def add_churn_reason(self, customer_id: str, reason: str,
                         evidence: Optional[List[str]] = None) -> Dict[str, Any]:
        cr = ChurnReason[reason]
        entry = self._churn_reason_analyzer.add_churn_reason(customer_id, cr, evidence)
        return {"entry_id": entry.entry_id, "reason": cr.name, "confidence": entry.confidence}

    def get_dashboard_alerts(self) -> List[Dict[str, Any]]:
        alerts = self._dashboard.get_active_alerts()
        return [{"alert_id": a.alert_id, "customer_id": a.customer_id,
                 "type": a.alert_type, "severity": a.severity,
                 "message": a.message, "created_at": a.created_at.isoformat()}
                for a in alerts]

    def get_health_distribution(self) -> Dict[str, int]:
        return self._health_monitor.get_health_distribution()

    def get_renewal_stats(self) -> Dict[str, Any]:
        return self._renewal_manager.get_renewal_stats()

    def get_contract_stats(self) -> Dict[str, Any]:
        return self._contract_tracker.get_contract_stats()

    def get_sentiment_distribution(self) -> Dict[str, int]:
        return self._sentiment_analyzer.get_sentiment_distribution()

    def get_escalation_stats(self) -> Dict[str, Any]:
        return self._escalation_engine.get_escalation_stats()

    def get_churn_reason_distribution(self) -> Dict[str, int]:
        return self._churn_reason_analyzer.get_reason_distribution()

    def get_top_churn_reasons(self, limit: int = 5) -> List[Dict[str, Any]]:
        return self._churn_reason_analyzer.get_top_reasons(limit)

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "CustomerRetentionAgent", "running": self._running,
            "customers": len(self._customers),
            "high_risk": len(self._churn_predictor.get_high_risk_customers()),
            "retention_rate": round(self._churn_predictor.get_retention_rate(), 4),
            "active_alerts": len(self._dashboard.get_active_alerts()),
            "open_escalations": len(self._escalation_engine.get_open_escalations()),
        }

    def get_full_report(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(), "status": self.get_status(),
            "nps": self.get_nps_score(),
            "risk_distribution": self._churn_predictor.get_risk_distribution(),
            "loyalty_tiers": self.get_loyalty_tier_distribution(),
            "health_distribution": self.get_health_distribution(),
            "renewal_stats": self.get_renewal_stats(),
            "contract_stats": self.get_contract_stats(),
            "sentiment_distribution": self.get_sentiment_distribution(),
            "escalation_stats": self.get_escalation_stats(),
            "churn_reasons": self.get_churn_reason_distribution(),
        }

# =============================================================================
# ASYNC WRAPPER
# =============================================================================

class AsyncCustomerRetentionAgent:
    def __init__(self, config: Optional[Config] = None):
        self._agent = CustomerRetentionAgent(config)

    async def initialize(self) -> Dict[str, Any]:
        return self._agent.initialize()

    async def shutdown(self) -> Dict[str, Any]:
        return self._agent.shutdown()

    async def get_full_report(self) -> Dict[str, Any]:
        return self._agent.get_full_report()

    async def predict_churn(self, customer_id: str) -> Dict[str, Any]:
        return self._agent.predict_churn(customer_id)

    async def get_nps_score(self) -> Dict[str, Any]:
        return self._agent.get_nps_score()

    async def get_status(self) -> Dict[str, Any]:
        return self._agent.get_status()

# =============================================================================
# ENTRY POINT
# =============================================================================

def main():
    print("=" * 60)
    print("  Customer Retention Agent - Comprehensive Demo")
    print("=" * 60)
    agent = CustomerRetentionAgent(Config())
    agent.initialize()

    for i in range(20):
        cid = f"cust_{i:03d}"
        agent.register_customer(cid, name=f"Customer {i}",
                                monthly_revenue=random.uniform(50, 500))
        agent.update_customer_signal(cid, "login_decrease", random.uniform(0, 1))
        agent.update_customer_signal(cid, "feature_usage_decline", random.uniform(0, 1))
        agent.add_loyalty_points(cid, random.randint(100, 5000))
        agent.calculate_health_score(cid, random.uniform(0.2, 1.0), random.uniform(0.2, 1.0),
                                     random.uniform(0.2, 1.0), random.uniform(0.2, 1.0),
                                     random.uniform(0.2, 1.0))
        agent.analyze_sentiment(cid, random.choice([
            "Great product, very satisfied", "Terrible experience, frustrated",
            "It works fine, nothing special", "Love the support team!",
            "Missing key features I need",
        ]))
    print(f"Registered {len(agent._customers)} customers")

    predictions = agent.predict_all_churn()
    print(f"Risk distribution: {predictions['risk_distribution']}")

    for cid in ["cust_001", "cust_005", "cust_010"]:
        pred = agent.predict_churn(cid)
        print(f"{cid}: {pred['risk_level']} (score: {pred['risk_score']})")

    for tier_name in ["BRONZE", "SILVER", "GOLD", "PLATINUM", "DIAMOND"]:
        count = agent.get_loyalty_tier_distribution().get(tier_name, 0)
        print(f"  {tier_name}: {count} customers")

    survey = agent.send_nps_survey("cust_001")
    agent.submit_nps_response(survey["survey_id"], 9, "Great product!")
    nps = agent.get_nps_score()
    print(f"NPS Score: {nps['nps_score']}")

    agent.create_cohort("cohort_jan", "January 2024", "2024-01",
                        {"cust_001", "cust_002", "cust_003"})

    agent.create_escalation("cust_003", "HIGH_CHURN_RISK", "Churn score above 0.7")
    agent.add_churn_reason("cust_005", "PRICE_SENSITIVITY", ["Complained about pricing"])

    print(f"Health distribution: {agent.get_health_distribution()}")
    print(f"Sentiment distribution: {agent.get_sentiment_distribution()}")
    print(f"Escalation stats: {agent.get_escalation_stats()}")
    print(f"Churn reasons: {agent.get_churn_reason_distribution()}")

    report = agent.get_full_report()
    print(f"\nReport: {report['status']}")

    agent.shutdown()
    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()

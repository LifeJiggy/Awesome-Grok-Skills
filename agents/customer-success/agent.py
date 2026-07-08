"""Customer Success Agent - Customer Onboarding and Success Management Platform.

Comprehensive framework for customer success including onboarding workflows,
health scoring, expansion revenue, QBR processes, advocacy programs,
success plans, renewal tracking, risk assessment, milestone management,
value realization, workload management, feedback collection, and adoption journeys.

Features:
- Customer onboarding workflows and milestone tracking
- Health score calculation with weighted factors
- Expansion revenue identification and tracking
- Quarterly Business Review (QBR) automation
- Customer advocacy and referral programs
- Success plan creation and management
- Risk identification and intervention
- Usage analytics and adoption tracking
- Executive reporting and dashboards
- Renewal lifecycle management
- Customer milestone tracking
- Value realization measurement
- CSM workload balancing
- Customer feedback collection and analysis
- Adoption journey tracking
"""

import hashlib
import json
import logging
import math
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
logger = logging.getLogger("customer_success_agent")

# =============================================================================
# ENUMS
# =============================================================================

class CustomerHealth(Enum):
    CRITICAL = auto()
    POOR = auto()
    AT_RISK = auto()
    STABLE = auto()
    HEALTHY = auto()
    EXCELLENT = auto()

class OnboardingStage(Enum):
    NOT_STARTED = auto()
    KICKOFF = auto()
    SETUP = auto()
    TRAINING = auto()
    GO_LIVE = auto()
    ADOPTION = auto()
    COMPLETED = auto()

class ExpansionType(Enum):
    UPGRADE = auto()
    CROSS_SELL = auto()
    RENEWAL = auto()
    ADD_ON = auto()
    SEAT_EXPANSION = auto()
    USAGE_BASED = auto()

class QBRStatus(Enum):
    SCHEDULED = auto()
    IN_PROGRESS = auto()
    COMPLETED = auto()
    CANCELLED = auto()

class AdvocacyType(Enum):
    REFERRAL = auto()
    CASE_STUDY = auto()
    TESTIMONIAL = auto()
    REVIEW = auto()
    SPEAKING = auto()
    COMMUNITY = auto()

class RiskLevel(Enum):
    NONE = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

class SuccessPlanStatus(Enum):
    DRAFT = auto()
    ACTIVE = auto()
    ON_TRACK = auto()
    AT_RISK = auto()
    COMPLETED = auto()
    ABANDONED = auto()

class AdoptionMetric(Enum):
    LOGIN_FREQUENCY = auto()
    FEATURE_USAGE = auto()
    SESSION_DURATION = auto()
    TASK_COMPLETION = auto()
    INTEGRATION_DEPTH = auto()
    TEAM_ADOPTION = auto()

class InterventionType(Enum):
    CHECK_IN = auto()
    TRAINING_SESSION = auto()
    FEATURE_DEMO = auto()
    ESCALATION = auto()
    EXECUTIVE_SPONSOR = auto()
    CUSTOM_SUCCESS_PLAN = auto()

class RenewalRisk(Enum):
    NONE = auto()
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()

class ValueStage(Enum):
    NOT_STARTED = auto()
    INITIAL_ADOPTION = auto()
    PARTIAL_VALUE = auto()
    CORE_VALUE = auto()
    FULL_VALUE = auto()
    MAXIMUM_VALUE = auto()

class MilestoneType(Enum):
    ONBOARDING = auto()
    SUCCESS_PLAN = auto()
    PRODUCT = auto()
    RELATIONSHIP = auto()
    CONTRACT = auto()
    ADVOCACY = auto()

class FeedbackSource(Enum):
    SURVEY = auto()
    QBR = auto()
    SUPPORT_TICKET = auto()
    NPS = auto()
    IN_PRODUCT = auto()
    DIRECT_CONVERSATION = auto()
    COMMUNITY = auto()

class AdoptionPhase(Enum):
    AWARENESS = auto()
    EXPLORATION = auto()
    FIRST_VALUE = auto()
    REGULAR_USE = auto()
    DEEP_ADOPTION = auto()
    CHAMPION = auto()

# =============================================================================
# CONSTANTS
# =============================================================================

HEALTH_SCORE_WEIGHTS: Dict[str, float] = {
    "product_usage": 0.30,
    "engagement": 0.20,
    "support_tickets": 0.15,
    "nps_score": 0.15,
    "payment_health": 0.10,
    "relationship": 0.10,
}

ONBOARDING_MILESTONES: List[Dict[str, Any]] = [
    {"stage": OnboardingStage.KICKOFF, "name": "Kickoff Meeting", "days": 0},
    {"stage": OnboardingStage.SETUP, "name": "Account Setup", "days": 3},
    {"stage": OnboardingStage.TRAINING, "name": "Training Complete", "days": 14},
    {"stage": OnboardingStage.GO_LIVE, "name": "Go Live", "days": 30},
    {"stage": OnboardingStage.ADOPTION, "name": "Full Adoption", "days": 60},
    {"stage": OnboardingStage.COMPLETED, "name": "Onboarding Complete", "days": 90},
]

HEALTH_THRESHOLDS = {
    CustomerHealth.CRITICAL: (0, 20),
    CustomerHealth.POOR: (20, 40),
    CustomerHealth.AT_RISK: (40, 55),
    CustomerHealth.STABLE: (55, 70),
    CustomerHealth.HEALTHY: (70, 85),
    CustomerHealth.EXCELLENT: (85, 100),
}

RENEWAL_RISK_THRESHOLDS = {
    RenewalRisk.NONE: (0.0, 0.1),
    RenewalRisk.LOW: (0.1, 0.3),
    RenewalRisk.MEDIUM: (0.3, 0.5),
    RenewalRisk.HIGH: (0.5, 0.75),
    RenewalRisk.CRITICAL: (0.75, 1.0),
}

ADOPTION_PHASE_THRESHOLDS = {
    AdoptionPhase.AWARENESS: (0, 15),
    AdoptionPhase.EXPLORATION: (15, 30),
    AdoptionPhase.FIRST_VALUE: (30, 50),
    AdoptionPhase.REGULAR_USE: (50, 70),
    AdoptionPhase.DEEP_ADOPTION: (70, 85),
    AdoptionPhase.CHAMPION: (85, 100),
}

VALUE_REALIZATION_STAGES = [
    ValueStage.NOT_STARTED,
    ValueStage.INITIAL_ADOPTION,
    ValueStage.PARTIAL_VALUE,
    ValueStage.CORE_VALUE,
    ValueStage.FULL_VALUE,
    ValueStage.MAXIMUM_VALUE,
]

# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Customer:
    customer_id: str
    name: str = ""
    email: str = ""
    company: str = ""
    plan: str = "starter"
    mrr: float = 0.0
    arr: float = 0.0
    health_score: float = 50.0
    health_status: CustomerHealth = CustomerHealth.STABLE
    onboarding_stage: OnboardingStage = OnboardingStage.NOT_STARTED
    onboarding_start: Optional[datetime] = None
    csm_assigned: str = ""
    contract_start: Optional[datetime] = None
    contract_end: Optional[datetime] = None
    renewal_date: Optional[datetime] = None
    segment: str = "standard"
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)

@dataclass
class OnboardingTask:
    task_id: str
    customer_id: str
    stage: OnboardingStage
    name: str
    description: str = ""
    assignee: str = ""
    due_date: Optional[datetime] = None
    completed: bool = False
    completed_at: Optional[datetime] = None
    notes: str = ""

@dataclass
class HealthMetric:
    customer_id: str
    metric_type: str
    value: float
    weight: float = 0.0
    calculated_at: datetime = field(default_factory=datetime.now)
    trend: str = "stable"
    details: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ExpansionOpportunity:
    opportunity_id: str
    customer_id: str
    expansion_type: ExpansionType
    description: str = ""
    estimated_value: float = 0.0
    probability: float = 0.0
    status: str = "identified"
    identified_at: datetime = field(default_factory=datetime.now)
    closed_at: Optional[datetime] = None
    closed_value: float = 0.0

@dataclass
class QBR:
    qbr_id: str
    customer_id: str
    quarter: str
    status: QBRStatus = QBRStatus.SCHEDULED
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    attendees: List[str] = field(default_factory=list)
    agenda: List[str] = field(default_factory=list)
    metrics_reviewed: Dict[str, Any] = field(default_factory=dict)
    action_items: List[Dict[str, Any]] = field(default_factory=list)
    notes: str = ""

@dataclass
class AdvocacyEntry:
    entry_id: str
    customer_id: str
    advocacy_type: AdvocacyType
    description: str = ""
    value: float = 0.0
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

@dataclass
class SuccessPlan:
    plan_id: str
    customer_id: str
    name: str
    goals: List[Dict[str, Any]] = field(default_factory=list)
    milestones: List[Dict[str, Any]] = field(default_factory=list)
    status: SuccessPlanStatus = SuccessPlanStatus.DRAFT
    owner: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    target_date: Optional[datetime] = None

@dataclass
class Intervention:
    intervention_id: str
    customer_id: str
    intervention_type: InterventionType
    description: str = ""
    assigned_to: str = ""
    scheduled_date: Optional[datetime] = None
    completed: bool = False
    outcome: str = ""
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class UsageMetrics:
    customer_id: str
    logins_30d: int = 0
    active_users: int = 0
    features_used: int = 0
    total_features: int = 0
    avg_session_minutes: float = 0.0
    tasks_completed: int = 0
    integrations_active: int = 0
    api_calls: int = 0
    last_calculated: datetime = field(default_factory=datetime.now)

@dataclass
class RenewalRecord:
    renewal_id: str
    customer_id: str
    current_value: float = 0.0
    proposed_value: float = 0.0
    renewal_date: Optional[datetime] = None
    risk_score: float = 0.0
    risk_level: RenewalRisk = RenewalRisk.NONE
    status: str = "pending"
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

@dataclass
class RiskAssessmentEntry:
    assessment_id: str
    customer_id: str
    risk_type: str = ""
    risk_level: RiskLevel = RiskLevel.NONE
    risk_score: float = 0.0
    factors: List[str] = field(default_factory=list)
    mitigation_actions: List[str] = field(default_factory=list)
    assessed_at: datetime = field(default_factory=datetime.now)
    reviewed: bool = False

@dataclass
class MilestoneRecord:
    milestone_id: str
    customer_id: str
    milestone_type: MilestoneType
    name: str
    description: str = ""
    target_date: Optional[datetime] = None
    achieved: bool = False
    achieved_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class ValueEntry:
    entry_id: str
    customer_id: str
    value_stage: ValueStage = ValueStage.NOT_STARTED
    realized_value: float = 0.0
    potential_value: float = 0.0
    metrics: Dict[str, Any] = field(default_factory=dict)
    recorded_at: datetime = field(default_factory=datetime.now)
    notes: str = ""

@dataclass
class WorkloadEntry:
    entry_id: str
    csm_id: str
    customer_id: str
    task_type: str = ""
    priority: str = "normal"
    estimated_minutes: int = 0
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

@dataclass
class FeedbackRecord:
    feedback_id: str
    customer_id: str
    source: FeedbackSource = FeedbackSource.DIRECT_CONVERSATION
    rating: float = 0.0
    comment: str = ""
    tags: List[str] = field(default_factory=list)
    sentiment: str = "neutral"
    created_at: datetime = field(default_factory=datetime.now)
    follow_up_needed: bool = False

@dataclass
class AdoptionEntry:
    entry_id: str
    customer_id: str
    phase: AdoptionPhase = AdoptionPhase.AWARENESS
    adoption_score: float = 0.0
    key_actions_completed: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    recorded_at: datetime = field(default_factory=datetime.now)

# =============================================================================
# EXCEPTIONS
# =============================================================================

class CustomerSuccessError(Exception):
    pass

class OnboardingError(CustomerSuccessError):
    pass

class HealthScoreError(CustomerSuccessError):
    pass

class QBRError(CustomerSuccessError):
    pass

class RenewalError(CustomerSuccessError):
    pass

class RiskAssessmentError(CustomerSuccessError):
    pass

class WorkloadError(CustomerSuccessError):
    pass

class FeedbackError(CustomerSuccessError):
    pass

class AdoptionError(CustomerSuccessError):
    pass

class ValueRealizationError(CustomerSuccessError):
    pass

# =============================================================================
# ONBOARDING MANAGER
# =============================================================================

class OnboardingManager:
    def __init__(self) -> None:
        self._tasks: Dict[str, List[OnboardingTask]] = defaultdict(list)
        self._milestones: Dict[str, Dict[OnboardingStage, datetime]] = defaultdict(dict)
        self._lock = threading.Lock()

    def start_onboarding(self, customer_id: str) -> Dict[str, Any]:
        try:
            with self._lock:
                self._milestones[customer_id][OnboardingStage.KICKOFF] = datetime.now()
            tasks = []
            for milestone in ONBOARDING_MILESTONES:
                task = OnboardingTask(
                    task_id=str(uuid.uuid4()), customer_id=customer_id,
                    stage=milestone["stage"], name=milestone["name"],
                    due_date=datetime.now() + timedelta(days=milestone["days"]),
                )
                with self._lock:
                    self._tasks[customer_id].append(task)
                tasks.append(task)
            logger.info("Started onboarding for %s with %d tasks", customer_id, len(tasks))
            return {"customer_id": customer_id, "tasks_created": len(tasks), "stage": "KICKOFF"}
        except Exception as e:
            logger.error("Failed to start onboarding for %s: %s", customer_id, e)
            raise OnboardingError(f"Start onboarding failed: {e}") from e

    def complete_task(self, task_id: str, customer_id: str, notes: str = "") -> bool:
        try:
            with self._lock:
                for task in self._tasks.get(customer_id, []):
                    if task.task_id == task_id and not task.completed:
                        task.completed = True
                        task.completed_at = datetime.now()
                        task.notes = notes
                        self._milestones[customer_id][task.stage] = datetime.now()
                        logger.info("Completed task %s for %s", task_id, customer_id)
                        return True
            return False
        except Exception as e:
            logger.error("Failed to complete task %s: %s", task_id, e)
            return False

    def get_onboarding_progress(self, customer_id: str) -> Dict[str, Any]:
        with self._lock:
            tasks = list(self._tasks.get(customer_id, []))
            milestones = dict(self._milestones.get(customer_id, {}))
        total = len(tasks)
        completed = sum(1 for t in tasks if t.completed)
        current_stage = OnboardingStage.NOT_STARTED
        for task in tasks:
            if not task.completed:
                current_stage = task.stage
                break
        else:
            current_stage = OnboardingStage.COMPLETED
        days_since_start = 0
        if tasks:
            start = min(t.due_date or datetime.now() for t in tasks)
            days_since_start = (datetime.now() - start).days
        return {
            "customer_id": customer_id, "current_stage": current_stage.name,
            "tasks_total": total, "tasks_completed": completed,
            "progress_percent": round(completed / total * 100, 1) if total > 0 else 0,
            "milestones_reached": [s.name for s in milestones.keys()],
            "days_since_start": days_since_start,
        }

    def get_overdue_tasks(self, customer_id: Optional[str] = None) -> List[OnboardingTask]:
        now = datetime.now()
        with self._lock:
            if customer_id:
                tasks = [t for t in self._tasks.get(customer_id, [])
                        if not t.completed and t.due_date and t.due_date < now]
            else:
                tasks = []
                for cust_tasks in self._tasks.values():
                    tasks.extend([t for t in cust_tasks
                                 if not t.completed and t.due_date and t.due_date < now])
        return tasks

    def get_all_tasks(self, customer_id: str) -> List[OnboardingTask]:
        with self._lock:
            return list(self._tasks.get(customer_id, []))

    def reassign_task(self, task_id: str, customer_id: str, new_assignee: str) -> bool:
        with self._lock:
            for task in self._tasks.get(customer_id, []):
                if task.task_id == task_id:
                    task.assignee = new_assignee
                    logger.info("Reassigned task %s to %s", task_id, new_assignee)
                    return True
        return False

    def get_tasks_by_stage(self, customer_id: str, stage: OnboardingStage) -> List[OnboardingTask]:
        with self._lock:
            return [t for t in self._tasks.get(customer_id, []) if t.stage == stage]

    def get_velocity_report(self, customer_id: str) -> Dict[str, Any]:
        with self._lock:
            milestones = dict(self._milestones.get(customer_id, {}))
        if len(milestones) < 2:
            return {"customer_id": customer_id, "avg_days_per_stage": 0.0, "stages_completed": len(milestones)}
        times = sorted(milestones.values())
        deltas = [(times[i + 1] - times[i]).total_seconds() / 86400 for i in range(len(times) - 1)]
        return {
            "customer_id": customer_id,
            "avg_days_per_stage": round(statistics.mean(deltas), 1),
            "stages_completed": len(milestones),
            "total_days": round(sum(deltas), 1),
        }

# =============================================================================
# HEALTH SCORER
# =============================================================================

class HealthScorer:
    def __init__(self) -> None:
        self._metrics: Dict[str, Dict[str, HealthMetric]] = defaultdict(dict)
        self._scores: Dict[str, float] = {}
        self._history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self._weights: Dict[str, float] = dict(HEALTH_SCORE_WEIGHTS)
        self._lock = threading.Lock()

    def set_weight(self, metric_type: str, weight: float) -> None:
        self._weights[metric_type] = weight

    def record_metric(self, customer_id: str, metric_type: str, value: float,
                      details: Optional[Dict[str, Any]] = None) -> HealthMetric:
        weight = self._weights.get(metric_type, 0.1)
        metric = HealthMetric(
            customer_id=customer_id, metric_type=metric_type,
            value=min(100, max(0, value)), weight=weight, details=details or {},
        )
        with self._lock:
            self._metrics[customer_id][metric_type] = metric
            self._history[customer_id].append({
                "type": metric_type, "value": value,
                "timestamp": datetime.now().isoformat(),
            })
        return metric

    def calculate_health_score(self, customer_id: str) -> float:
        with self._lock:
            metrics = dict(self._metrics.get(customer_id, {}))
        if not metrics:
            return 50.0
        total_weight = sum(m.weight for m in metrics.values())
        if total_weight == 0:
            return 50.0
        weighted_sum = sum(m.value * m.weight for m in metrics.values())
        score = weighted_sum / total_weight
        score = max(0, min(100, score))
        self._scores[customer_id] = score
        return score

    def get_health_status(self, customer_id: str) -> CustomerHealth:
        score = self.calculate_health_score(customer_id)
        for health, (low, high) in HEALTH_THRESHOLDS.items():
            if low <= score < high:
                return health
        return CustomerHealth.STABLE

    def get_health_history(self, customer_id: str, metric_type: Optional[str] = None,
                           limit: int = 50) -> List[Dict[str, Any]]:
        with self._lock:
            history = list(self._history.get(customer_id, []))
        if metric_type:
            history = [h for h in history if h["type"] == metric_type]
        return history[-limit:]

    def get_health_report(self, customer_id: str) -> Dict[str, Any]:
        with self._lock:
            metrics = dict(self._metrics.get(customer_id, {}))
        score = self.calculate_health_score(customer_id)
        status = self.get_health_status(customer_id)
        return {
            "customer_id": customer_id, "health_score": round(score, 1),
            "health_status": status.name,
            "metrics": {m.metric_type: {"value": m.value, "weight": m.weight}
                       for m in metrics.values()},
            "calculated_at": datetime.now().isoformat(),
        }

    def get_customers_by_health(self, status: CustomerHealth) -> List[str]:
        customers = []
        with self._lock:
            customer_ids = list(self._metrics.keys())
        for cid in customer_ids:
            if self.get_health_status(cid) == status:
                customers.append(cid)
        return customers

    def get_health_distribution(self) -> Dict[str, int]:
        dist = {h.name: 0 for h in CustomerHealth}
        with self._lock:
            customer_ids = list(self._metrics.keys())
        for cid in customer_ids:
            status = self.get_health_status(cid)
            dist[status.name] += 1
        return dist

    def get_health_trend(self, customer_id: str, days: int = 30) -> Dict[str, Any]:
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        with self._lock:
            history = [h for h in self._history.get(customer_id, []) if h["timestamp"] >= cutoff]
        if len(history) < 2:
            return {"customer_id": customer_id, "trend": "insufficient_data", "change": 0.0}
        first_half = statistics.mean([h["value"] for h in history[:len(history) // 2]])
        second_half = statistics.mean([h["value"] for h in history[len(history) // 2:]])
        change = second_half - first_half
        trend = "improving" if change > 2 else "declining" if change < -2 else "stable"
        return {"customer_id": customer_id, "trend": trend, "change": round(change, 2)}

    def get_top_risk_customers(self, limit: int = 10) -> List[Dict[str, Any]]:
        with self._lock:
            customer_ids = list(self._metrics.keys())
        results = []
        for cid in customer_ids:
            score = self.calculate_health_score(cid)
            status = self.get_health_status(cid)
            results.append({"customer_id": cid, "health_score": round(score, 1), "status": status.name})
        results.sort(key=lambda x: x["health_score"])
        return results[:limit]

# =============================================================================
# EXPANSION MANAGER
# =============================================================================

class ExpansionManager:
    def __init__(self) -> None:
        self._opportunities: Dict[str, ExpansionOpportunity] = {}
        self._lock = threading.Lock()

    def identify_opportunity(self, customer_id: str, expansion_type: ExpansionType,
                             description: str = "", estimated_value: float = 0.0,
                             probability: float = 0.5) -> ExpansionOpportunity:
        opp = ExpansionOpportunity(
            opportunity_id=str(uuid.uuid4()), customer_id=customer_id,
            expansion_type=expansion_type, description=description,
            estimated_value=estimated_value, probability=probability,
        )
        with self._lock:
            self._opportunities[opp.opportunity_id] = opp
        logger.info("Identified expansion opportunity %s for %s: $%.0f",
                    opp.opportunity_id[:8], customer_id, estimated_value)
        return opp

    def update_opportunity(self, opportunity_id: str, **updates: Any) -> bool:
        with self._lock:
            opp = self._opportunities.get(opportunity_id)
            if opp:
                for key, value in updates.items():
                    if hasattr(opp, key):
                        setattr(opp, key, value)
                return True
        return False

    def close_opportunity(self, opportunity_id: str, value: float) -> bool:
        with self._lock:
            opp = self._opportunities.get(opportunity_id)
            if opp:
                opp.status = "closed_won"
                opp.closed_value = value
                opp.closed_at = datetime.now()
                return True
        return False

    def get_opportunities(self, customer_id: Optional[str] = None,
                          status: Optional[str] = None) -> List[ExpansionOpportunity]:
        with self._lock:
            opps = list(self._opportunities.values())
        if customer_id:
            opps = [o for o in opps if o.customer_id == customer_id]
        if status:
            opps = [o for o in opps if o.status == status]
        return opps

    def get_pipeline_value(self) -> Dict[str, Any]:
        with self._lock:
            opps = list(self._opportunities.values())
        identified = [o for o in opps if o.status == "identified"]
        closed = [o for o in opps if o.status == "closed_won"]
        pipeline_value = sum(o.estimated_value * o.probability for o in identified)
        closed_value = sum(o.closed_value for o in closed)
        return {
            "pipeline_value": round(pipeline_value, 2),
            "closed_value": round(closed_value, 2),
            "identified_count": len(identified),
            "closed_count": len(closed),
        }

    def get_expansion_by_type(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            opps = list(self._opportunities.values())
        by_type: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"count": 0, "value": 0})
        for opp in opps:
            by_type[opp.expansion_type.name]["count"] += 1
            by_type[opp.expansion_type.name]["value"] += opp.estimated_value
        return dict(by_type)

    def get_win_rate(self) -> Dict[str, Any]:
        with self._lock:
            opps = list(self._opportunities.values())
        closed_won = [o for o in opps if o.status == "closed_won"]
        closed_lost = [o for o in opps if o.status == "closed_lost"]
        total = len(closed_won) + len(closed_lost)
        rate = len(closed_won) / total if total > 0 else 0.0
        avg_deal = statistics.mean([o.closed_value for o in closed_won]) if closed_won else 0.0
        return {
            "win_rate": round(rate * 100, 1),
            "total_deals": total,
            "avg_deal_size": round(avg_deal, 2),
            "total_revenue": round(sum(o.closed_value for o in closed_won), 2),
        }

# =============================================================================
# QBR MANAGER
# =============================================================================

class QBRManager:
    def __init__(self) -> None:
        self._qbrs: Dict[str, QBR] = {}
        self._lock = threading.Lock()

    def schedule_qbr(self, customer_id: str, quarter: str,
                     scheduled_date: datetime, attendees: Optional[List[str]] = None) -> QBR:
        qbr = QBR(
            qbr_id=str(uuid.uuid4()), customer_id=customer_id,
            quarter=quarter, scheduled_date=scheduled_date,
            attendees=attendees or [],
        )
        with self._lock:
            self._qbrs[qbr.qbr_id] = qbr
        logger.info("Scheduled QBR %s for %s (%s)", qbr.qbr_id[:8], customer_id, quarter)
        return qbr

    def start_qbr(self, qbr_id: str) -> bool:
        with self._lock:
            qbr = self._qbrs.get(qbr_id)
            if qbr:
                qbr.status = QBRStatus.IN_PROGRESS
                return True
        return False

    def complete_qbr(self, qbr_id: str, metrics: Dict[str, Any],
                     action_items: List[Dict[str, Any]], notes: str = "") -> bool:
        with self._lock:
            qbr = self._qbrs.get(qbr_id)
            if qbr:
                qbr.status = QBRStatus.COMPLETED
                qbr.completed_date = datetime.now()
                qbr.metrics_reviewed = metrics
                qbr.action_items = action_items
                qbr.notes = notes
                return True
        return False

    def get_qbr(self, qbr_id: str) -> Optional[QBR]:
        with self._lock:
            return self._qbrs.get(qbr_id)

    def get_customer_qbrs(self, customer_id: str) -> List[QBR]:
        with self._lock:
            return [q for q in self._qbrs.values() if q.customer_id == customer_id]

    def get_upcoming_qbrs(self, days: int = 30) -> List[QBR]:
        cutoff = datetime.now() + timedelta(days=days)
        with self._lock:
            return [q for q in self._qbrs.values()
                    if q.scheduled_date and q.scheduled_date <= cutoff
                    and q.status == QBRStatus.SCHEDULED]

    def get_all_qbrs(self, status: Optional[QBRStatus] = None) -> List[QBR]:
        with self._lock:
            qbrs = list(self._qbrs.values())
        if status:
            qbrs = [q for q in qbrs if q.status == status]
        return qbrs

    def get_qbr_completion_rate(self) -> Dict[str, Any]:
        with self._lock:
            qbrs = list(self._qbrs.values())
        total = len(qbrs)
        completed = sum(1 for q in qbrs if q.status == QBRStatus.COMPLETED)
        cancelled = sum(1 for q in qbrs if q.status == QBRStatus.CANCELLED)
        return {
            "total": total,
            "completed": completed,
            "cancelled": cancelled,
            "completion_rate": round(completed / total * 100, 1) if total > 0 else 0.0,
        }

    def get_overdue_qbrs(self) -> List[QBR]:
        now = datetime.now()
        with self._lock:
            return [q for q in self._qbrs.values()
                    if q.scheduled_date and q.scheduled_date < now
                    and q.status == QBRStatus.SCHEDULED]

# =============================================================================
# ADVOCACY MANAGER
# =============================================================================

class AdvocacyManager:
    def __init__(self) -> None:
        self._entries: Dict[str, AdvocacyEntry] = {}
        self._referral_codes: Dict[str, str] = {}
        self._lock = threading.Lock()

    def create_advocacy_entry(self, customer_id: str, advocacy_type: AdvocacyType,
                              description: str = "", value: float = 0.0) -> AdvocacyEntry:
        entry = AdvocacyEntry(
            entry_id=str(uuid.uuid4()), customer_id=customer_id,
            advocacy_type=advocacy_type, description=description, value=value,
        )
        with self._lock:
            self._entries[entry.entry_id] = entry
        return entry

    def complete_advocacy(self, entry_id: str, outcome: str = "completed") -> bool:
        with self._lock:
            entry = self._entries.get(entry_id)
            if entry:
                entry.status = outcome
                entry.completed_at = datetime.now()
                return True
        return False

    def generate_referral_code(self, customer_id: str) -> str:
        code = f"REF_{customer_id[:8]}_{uuid.uuid4().hex[:6].upper()}"
        with self._lock:
            self._referral_codes[customer_id] = code
        return code

    def get_referral_code(self, customer_id: str) -> Optional[str]:
        with self._lock:
            return self._referral_codes.get(customer_id)

    def get_advocacy_entries(self, customer_id: Optional[str] = None,
                            advocacy_type: Optional[AdvocacyType] = None) -> List[AdvocacyEntry]:
        with self._lock:
            entries = list(self._entries.values())
        if customer_id:
            entries = [e for e in entries if e.customer_id == customer_id]
        if advocacy_type:
            entries = [e for e in entries if e.advocacy_type == advocacy_type]
        return entries

    def get_advocacy_stats(self) -> Dict[str, Any]:
        with self._lock:
            entries = list(self._entries.values())
        by_type: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"count": 0, "completed": 0, "value": 0})
        for e in entries:
            by_type[e.advocacy_type.name]["count"] += 1
            if e.status == "completed":
                by_type[e.advocacy_type.name]["completed"] += 1
            by_type[e.advocacy_type.name]["value"] += e.value
        return {
            "total_entries": len(entries),
            "by_type": dict(by_type),
            "total_referral_codes": len(self._referral_codes),
        }

    def get_top_advocates(self, limit: int = 5) -> List[Dict[str, Any]]:
        with self._lock:
            entries = list(self._entries.values())
        by_customer: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"count": 0, "value": 0})
        for e in entries:
            by_customer[e.customer_id]["count"] += 1
            by_customer[e.customer_id]["value"] += e.value
        ranked = [{"customer_id": cid, **stats} for cid, stats in by_customer.items()]
        ranked.sort(key=lambda x: x["value"], reverse=True)
        return ranked[:limit]

# =============================================================================
# SUCCESS PLAN MANAGER
# =============================================================================

class SuccessPlanManager:
    def __init__(self) -> None:
        self._plans: Dict[str, SuccessPlan] = {}
        self._lock = threading.Lock()

    def create_plan(self, customer_id: str, name: str,
                    goals: Optional[List[Dict[str, Any]]] = None,
                    owner: str = "") -> SuccessPlan:
        plan = SuccessPlan(
            plan_id=str(uuid.uuid4()), customer_id=customer_id,
            name=name, goals=goals or [], owner=owner,
        )
        with self._lock:
            self._plans[plan.plan_id] = plan
        logger.info("Created success plan %s for %s", plan.plan_id[:8], customer_id)
        return plan

    def activate_plan(self, plan_id: str) -> bool:
        with self._lock:
            plan = self._plans.get(plan_id)
            if plan:
                plan.status = SuccessPlanStatus.ACTIVE
                return True
        return False

    def update_milestone(self, plan_id: str, milestone_name: str, completed: bool = True) -> bool:
        with self._lock:
            plan = self._plans.get(plan_id)
            if plan:
                for milestone in plan.milestones:
                    if milestone.get("name") == milestone_name:
                        milestone["completed"] = completed
                        milestone["completed_at"] = datetime.now().isoformat()
                        plan.updated_at = datetime.now()
                        return True
        return False

    def get_plan(self, plan_id: str) -> Optional[SuccessPlan]:
        with self._lock:
            return self._plans.get(plan_id)

    def get_customer_plans(self, customer_id: str) -> List[SuccessPlan]:
        with self._lock:
            return [p for p in self._plans.values() if p.customer_id == customer_id]

    def get_active_plans(self) -> List[SuccessPlan]:
        with self._lock:
            return [p for p in self._plans.values() if p.status == SuccessPlanStatus.ACTIVE]

    def get_plan_completion_rate(self, plan_id: str) -> float:
        with self._lock:
            plan = self._plans.get(plan_id)
        if not plan or not plan.milestones:
            return 0.0
        completed = sum(1 for m in plan.milestones if m.get("completed"))
        return completed / len(plan.milestones)

    def get_at_risk_plans(self) -> List[Dict[str, Any]]:
        with self._lock:
            plans = [p for p in self._plans.values()
                     if p.status in (SuccessPlanStatus.ACTIVE, SuccessPlanStatus.AT_RISK)]
        results = []
        for plan in plans:
            rate = self.get_plan_completion_rate(plan.plan_id)
            if rate < 0.5:
                results.append({"plan_id": plan.plan_id, "customer_id": plan.customer_id,
                                "completion_rate": round(rate * 100, 1), "status": plan.status.name})
        return results

    def add_goal(self, plan_id: str, objective: str, target: str = "") -> bool:
        with self._lock:
            plan = self._plans.get(plan_id)
            if plan:
                plan.goals.append({"objective": objective, "target": target, "completed": False})
                plan.updated_at = datetime.now()
                return True
        return False

    def add_milestone(self, plan_id: str, name: str, target_date: Optional[datetime] = None) -> bool:
        with self._lock:
            plan = self._plans.get(plan_id)
            if plan:
                plan.milestones.append({
                    "name": name, "completed": False,
                    "target_date": target_date.isoformat() if target_date else None,
                })
                plan.updated_at = datetime.now()
                return True
        return False

# =============================================================================
# USAGE TRACKER
# =============================================================================

class UsageTracker:
    def __init__(self) -> None:
        self._usage: Dict[str, UsageMetrics] = {}
        self._history: Dict[str, deque] = defaultdict(lambda: deque(maxlen=50))
        self._lock = threading.Lock()

    def record_usage(self, customer_id: str, **kwargs: Any) -> UsageMetrics:
        with self._lock:
            if customer_id not in self._usage:
                self._usage[customer_id] = UsageMetrics(customer_id=customer_id)
            usage = self._usage[customer_id]
            for key, value in kwargs.items():
                if hasattr(usage, key):
                    setattr(usage, key, value)
            usage.last_calculated = datetime.now()
            self._history[customer_id].append({
                "timestamp": datetime.now().isoformat(),
                "snapshot": {k: v for k, v in kwargs.items()},
            })
        return self._usage[customer_id]

    def get_usage(self, customer_id: str) -> Optional[UsageMetrics]:
        with self._lock:
            return self._usage.get(customer_id)

    def get_adoption_score(self, customer_id: str) -> float:
        usage = self._usage.get(customer_id)
        if not usage:
            return 0.0
        scores = []
        if usage.total_features > 0:
            scores.append(usage.features_used / usage.total_features * 100)
        if usage.logins_30d > 0:
            scores.append(min(100, usage.logins_30d * 5))
        if usage.active_users > 0:
            scores.append(min(100, usage.active_users * 10))
        return statistics.mean(scores) if scores else 0.0

    def get_usage_report(self, customer_id: str) -> Dict[str, Any]:
        usage = self._usage.get(customer_id)
        if not usage:
            return {"error": "No usage data"}
        return {
            "customer_id": customer_id,
            "logins_30d": usage.logins_30d,
            "active_users": usage.active_users,
            "feature_adoption": f"{usage.features_used}/{usage.total_features}",
            "adoption_score": round(self.get_adoption_score(customer_id), 1),
            "integrations": usage.integrations_active,
            "api_calls": usage.api_calls,
        }

    def get_all_usage(self) -> List[UsageMetrics]:
        with self._lock:
            return list(self._usage.values())

    def get_usage_trend(self, customer_id: str) -> Dict[str, Any]:
        with self._lock:
            history = list(self._history.get(customer_id, []))
        if len(history) < 2:
            return {"customer_id": customer_id, "trend": "insufficient_data"}
        recent = history[-1]["snapshot"].get("logins_30d", 0)
        earlier = history[0]["snapshot"].get("logins_30d", 0)
        if earlier == 0:
            return {"customer_id": customer_id, "trend": "new", "data_points": len(history)}
        change = ((recent - earlier) / earlier) * 100
        trend = "growing" if change > 10 else "declining" if change < -10 else "stable"
        return {"customer_id": customer_id, "trend": trend, "change_percent": round(change, 1)}

    def get_low_usage_customers(self, threshold: float = 20.0) -> List[Dict[str, Any]]:
        results = []
        for cid, usage in self._usage.items():
            score = self.get_adoption_score(cid)
            if score < threshold:
                results.append({"customer_id": cid, "adoption_score": round(score, 1)})
        results.sort(key=lambda x: x["adoption_score"])
        return results

# =============================================================================
# RENEWAL TRACKER
# =============================================================================

class RenewalTracker:
    def __init__(self) -> None:
        self._renewals: Dict[str, RenewalRecord] = {}
        self._lock = threading.Lock()

    def create_renewal(self, customer_id: str, current_value: float,
                       renewal_date: Optional[datetime] = None,
                       proposed_value: float = 0.0) -> RenewalRecord:
        record = RenewalRecord(
            renewal_id=str(uuid.uuid4()), customer_id=customer_id,
            current_value=current_value, proposed_value=proposed_value or current_value,
            renewal_date=renewal_date,
        )
        with self._lock:
            self._renewals[record.renewal_id] = record
        logger.info("Created renewal %s for %s", record.renewal_id[:8], customer_id)
        return record

    def update_risk_score(self, renewal_id: str, risk_score: float) -> bool:
        with self._lock:
            record = self._renewals.get(renewal_id)
            if record:
                record.risk_score = min(1.0, max(0.0, risk_score))
                for level, (low, high) in RENEWAL_RISK_THRESHOLDS.items():
                    if low <= risk_score < high:
                        record.risk_level = level
                        break
                record.updated_at = datetime.now()
                return True
        return False

    def get_renewal(self, renewal_id: str) -> Optional[RenewalRecord]:
        with self._lock:
            return self._renewals.get(renewal_id)

    def get_customer_renewals(self, customer_id: str) -> List[RenewalRecord]:
        with self._lock:
            return [r for r in self._renewals.values() if r.customer_id == customer_id]

    def get_upcoming_renewals(self, days: int = 90) -> List[RenewalRecord]:
        cutoff = datetime.now() + timedelta(days=days)
        with self._lock:
            return [r for r in self._renewals.values()
                    if r.renewal_date and r.renewal_date <= cutoff
                    and r.status == "pending"]

    def get_at_risk_renewals(self) -> List[Dict[str, Any]]:
        with self._lock:
            records = list(self._renewals.values())
        at_risk = [r for r in records if r.risk_level in (RenewalRisk.HIGH, RenewalRisk.CRITICAL)]
        return [{"renewal_id": r.renewal_id, "customer_id": r.customer_id,
                 "risk_level": r.risk_level.name, "risk_score": r.risk_score,
                 "current_value": r.current_value} for r in at_risk]

    def get_renewal_summary(self) -> Dict[str, Any]:
        with self._lock:
            records = list(self._renewals.values())
        total_value = sum(r.current_value for r in records)
        at_risk_value = sum(r.current_value for r in records if r.risk_level in (RenewalRisk.HIGH, RenewalRisk.CRITICAL))
        return {
            "total_renewals": len(records),
            "total_value": round(total_value, 2),
            "at_risk_value": round(at_risk_value, 2),
            "at_risk_count": sum(1 for r in records if r.risk_level in (RenewalRisk.HIGH, RenewalRisk.CRITICAL)),
        }

# =============================================================================
# RISK ASSESSMENT
# =============================================================================

class RiskAssessment:
    def __init__(self) -> None:
        self._assessments: Dict[str, RiskAssessmentEntry] = {}
        self._lock = threading.Lock()

    def assess_customer(self, customer_id: str, risk_type: str,
                        factors: Optional[List[str]] = None,
                        mitigation: Optional[List[str]] = None) -> RiskAssessmentEntry:
        entry = RiskAssessmentEntry(
            assessment_id=str(uuid.uuid4()), customer_id=customer_id,
            risk_type=risk_type, factors=factors or [],
            mitigation_actions=mitigation or [],
        )
        with self._lock:
            self._assessments[entry.assessment_id] = entry
        logger.info("Risk assessment %s for %s: %s", entry.assessment_id[:8], customer_id, risk_type)
        return entry

    def set_risk_level(self, assessment_id: str, level: RiskLevel, score: float = 0.0) -> bool:
        with self._lock:
            entry = self._assessments.get(assessment_id)
            if entry:
                entry.risk_level = level
                entry.risk_score = score
                return True
        return False

    def get_customer_risks(self, customer_id: str) -> List[RiskAssessmentEntry]:
        with self._lock:
            return [a for a in self._assessments.values() if a.customer_id == customer_id]

    def get_high_risk_customers(self) -> List[Dict[str, Any]]:
        with self._lock:
            entries = list(self._assessments.values())
        high = [e for e in entries if e.risk_level in (RiskLevel.HIGH, RiskLevel.CRITICAL)]
        by_customer: Dict[str, List[str]] = defaultdict(list)
        for e in high:
            by_customer[e.customer_id].append(e.risk_type)
        return [{"customer_id": cid, "risk_count": len(types), "risk_types": types}
                for cid, types in by_customer.items()]

    def get_risk_summary(self) -> Dict[str, Any]:
        with self._lock:
            entries = list(self._assessments.values())
        by_level: Dict[str, int] = {l.name: 0 for l in RiskLevel}
        for e in entries:
            by_level[e.risk_level.name] += 1
        return {"total_assessments": len(entries), "by_level": by_level}

# =============================================================================
# CUSTOMER MILESTONE TRACKER
# =============================================================================

class CustomerMilestoneTracker:
    def __init__(self) -> None:
        self._milestones: Dict[str, MilestoneRecord] = {}
        self._lock = threading.Lock()

    def create_milestone(self, customer_id: str, milestone_type: MilestoneType,
                         name: str, description: str = "",
                         target_date: Optional[datetime] = None) -> MilestoneRecord:
        record = MilestoneRecord(
            milestone_id=str(uuid.uuid4()), customer_id=customer_id,
            milestone_type=milestone_type, name=name, description=description,
            target_date=target_date,
        )
        with self._lock:
            self._milestones[record.milestone_id] = record
        return record

    def achieve_milestone(self, milestone_id: str) -> bool:
        with self._lock:
            record = self._milestones.get(milestone_id)
            if record:
                record.achieved = True
                record.achieved_at = datetime.now()
                return True
        return False

    def get_customer_milestones(self, customer_id: str) -> List[MilestoneRecord]:
        with self._lock:
            return [m for m in self._milestones.values() if m.customer_id == customer_id]

    def get_milestone_progress(self, customer_id: str) -> Dict[str, Any]:
        with self._lock:
            milestones = [m for m in self._milestones.values() if m.customer_id == customer_id]
        total = len(milestones)
        achieved = sum(1 for m in milestones if m.achieved)
        overdue = sum(1 for m in milestones if not m.achieved and m.target_date and m.target_date < datetime.now())
        return {
            "customer_id": customer_id,
            "total": total,
            "achieved": achieved,
            "overdue": overdue,
            "completion_rate": round(achieved / total * 100, 1) if total > 0 else 0.0,
        }

    def get_upcoming_milestones(self, days: int = 30) -> List[MilestoneRecord]:
        cutoff = datetime.now() + timedelta(days=days)
        with self._lock:
            return [m for m in self._milestones.values()
                    if m.target_date and m.target_date <= cutoff and not m.achieved]

# =============================================================================
# VALUE REALIZATION
# =============================================================================

class ValueRealization:
    def __init__(self) -> None:
        self._entries: Dict[str, List[ValueEntry]] = defaultdict(list)
        self._lock = threading.Lock()

    def record_value(self, customer_id: str, value_stage: ValueStage,
                     realized_value: float = 0.0, potential_value: float = 0.0,
                     metrics: Optional[Dict[str, Any]] = None) -> ValueEntry:
        entry = ValueEntry(
            entry_id=str(uuid.uuid4()), customer_id=customer_id,
            value_stage=value_stage, realized_value=realized_value,
            potential_value=potential_value, metrics=metrics or {},
        )
        with self._lock:
            self._entries[customer_id].append(entry)
        logger.info("Recorded value %s for %s at stage %s", entry.entry_id[:8], customer_id, value_stage.name)
        return entry

    def get_value_progress(self, customer_id: str) -> Dict[str, Any]:
        with self._lock:
            entries = list(self._entries.get(customer_id, []))
        if not entries:
            return {"customer_id": customer_id, "stage": "NOT_STARTED", "realization_rate": 0.0}
        latest = entries[-1]
        rate = latest.realized_value / latest.potential_value if latest.potential_value > 0 else 0.0
        return {
            "customer_id": customer_id,
            "stage": latest.value_stage.name,
            "realized_value": latest.realized_value,
            "potential_value": latest.potential_value,
            "realization_rate": round(rate * 100, 1),
        }

    def get_value_summary(self) -> Dict[str, Any]:
        with self._lock:
            all_entries = dict(self._entries)
        total_realized = 0.0
        total_potential = 0.0
        for entries in all_entries.values():
            if entries:
                total_realized += entries[-1].realized_value
                total_potential += entries[-1].potential_value
        return {
            "total_customers": len(all_entries),
            "total_realized": round(total_realized, 2),
            "total_potential": round(total_potential, 2),
            "overall_rate": round(total_realized / total_potential * 100, 1) if total_potential > 0 else 0.0,
        }

# =============================================================================
# CSM WORKLOAD MANAGER
# =============================================================================

class CSMWorkloadManager:
    def __init__(self) -> None:
        self._workload: Dict[str, List[WorkloadEntry]] = defaultdict(list)
        self._lock = threading.Lock()

    def assign_task(self, csm_id: str, customer_id: str, task_type: str,
                    priority: str = "normal", estimated_minutes: int = 30) -> WorkloadEntry:
        entry = WorkloadEntry(
            entry_id=str(uuid.uuid4()), csm_id=csm_id,
            customer_id=customer_id, task_type=task_type,
            priority=priority, estimated_minutes=estimated_minutes,
        )
        with self._lock:
            self._workload[csm_id].append(entry)
        return entry

    def complete_task(self, csm_id: str, entry_id: str) -> bool:
        with self._lock:
            for entry in self._workload.get(csm_id, []):
                if entry.entry_id == entry_id:
                    entry.status = "completed"
                    entry.completed_at = datetime.now()
                    return True
        return False

    def get_csm_workload(self, csm_id: str) -> Dict[str, Any]:
        with self._lock:
            entries = [e for e in self._workload.get(csm_id, []) if e.status == "pending"]
        total_minutes = sum(e.estimated_minutes for e in entries)
        return {
            "csm_id": csm_id,
            "pending_tasks": len(entries),
            "total_estimated_minutes": total_minutes,
            "customers_served": len(set(e.customer_id for e in entries)),
        }

    def get_balanced_assignment(self) -> Dict[str, str]:
        with self._lock:
            all_entries = dict(self._workload)
        workloads = {}
        for csm_id, entries in all_entries.items():
            pending = [e for e in entries if e.status == "pending"]
            workloads[csm_id] = sum(e.estimated_minutes for e in pending)
        if not workloads:
            return {}
        min_csm = min(workloads, key=workloads.get)
        return {"recommended_csm": min_csm, "current_minutes": workloads[min_csm]}

# =============================================================================
# CUSTOMER FEEDBACK MANAGER
# =============================================================================

class CustomerFeedbackManager:
    def __init__(self) -> None:
        self._feedback: Dict[str, List[FeedbackRecord]] = defaultdict(list)
        self._lock = threading.Lock()

    def record_feedback(self, customer_id: str, source: FeedbackSource,
                        rating: float = 0.0, comment: str = "",
                        tags: Optional[List[str]] = None) -> FeedbackRecord:
        record = FeedbackRecord(
            feedback_id=str(uuid.uuid4()), customer_id=customer_id,
            source=source, rating=min(10.0, max(0.0, rating)),
            comment=comment, tags=tags or [],
        )
        record.sentiment = "positive" if rating >= 7 else "negative" if rating <= 4 else "neutral"
        record.follow_up_needed = record.sentiment == "negative" or rating <= 3
        with self._lock:
            self._feedback[customer_id].append(record)
        return record

    def get_customer_feedback(self, customer_id: str) -> List[FeedbackRecord]:
        with self._lock:
            return list(self._feedback.get(customer_id, []))

    def get_sentiment_summary(self, customer_id: str) -> Dict[str, Any]:
        with self._lock:
            records = list(self._feedback.get(customer_id, []))
        if not records:
            return {"customer_id": customer_id, "total": 0, "avg_rating": 0.0}
        avg_rating = statistics.mean([r.rating for r in records])
        positive = sum(1 for r in records if r.sentiment == "positive")
        negative = sum(1 for r in records if r.sentiment == "negative")
        neutral = sum(1 for r in records if r.sentiment == "neutral")
        return {
            "customer_id": customer_id,
            "total": len(records),
            "avg_rating": round(avg_rating, 2),
            "positive": positive,
            "negative": negative,
            "neutral": neutral,
            "follow_up_needed": sum(1 for r in records if r.follow_up_needed),
        }

    def get_negative_feedback(self) -> List[Dict[str, Any]]:
        with self._lock:
            all_records = dict(self._feedback)
        results = []
        for cid, records in all_records.items():
            for r in records:
                if r.sentiment == "negative":
                    results.append({"customer_id": cid, "feedback_id": r.feedback_id,
                                    "rating": r.rating, "comment": r.comment[:100]})
        results.sort(key=lambda x: x["rating"])
        return results

    def get_nps_score(self) -> Dict[str, Any]:
        with self._lock:
            all_records = dict(self._feedback)
        nps_records = []
        for records in all_records.values():
            nps_records.extend([r for r in records if r.source == FeedbackSource.NPS])
        if not nps_records:
            return {"nps_score": 0, "promoters": 0, "detractors": 0, "total": 0}
        promoters = sum(1 for r in nps_records if r.rating >= 9)
        detractors = sum(1 for r in nps_records if r.rating <= 6)
        total = len(nps_records)
        nps = ((promoters - detractors) / total) * 100
        return {"nps_score": round(nps, 1), "promoters": promoters, "detractors": detractors, "total": total}

# =============================================================================
# ADOPTION JOURNEY TRACKER
# =============================================================================

class AdoptionJourneyTracker:
    def __init__(self) -> None:
        self._journeys: Dict[str, List[AdoptionEntry]] = defaultdict(list)
        self._lock = threading.Lock()

    def record_adoption(self, customer_id: str, phase: AdoptionPhase,
                        adoption_score: float = 0.0,
                        key_actions: Optional[List[str]] = None,
                        blockers: Optional[List[str]] = None) -> AdoptionEntry:
        entry = AdoptionEntry(
            entry_id=str(uuid.uuid4()), customer_id=customer_id,
            phase=phase, adoption_score=min(100, max(0, adoption_score)),
            key_actions_completed=key_actions or [], blockers=blockers or [],
        )
        with self._lock:
            self._journeys[customer_id].append(entry)
        return entry

    def get_customer_phase(self, customer_id: str) -> Dict[str, Any]:
        with self._lock:
            entries = list(self._journeys.get(customer_id, []))
        if not entries:
            return {"customer_id": customer_id, "phase": "AWARENESS", "adoption_score": 0.0}
        latest = entries[-1]
        return {
            "customer_id": customer_id,
            "phase": latest.phase.name,
            "adoption_score": latest.adoption_score,
            "blockers": latest.blockers,
        }

    def get_journey_progress(self, customer_id: str) -> Dict[str, Any]:
        with self._lock:
            entries = list(self._journeys.get(customer_id, []))
        phases_hit = [e.phase.name for e in entries]
        unique_phases = list(dict.fromkeys(phases_hit))
        return {
            "customer_id": customer_id,
            "phases_completed": unique_phases,
            "total_records": len(entries),
            "current_phase": unique_phases[-1] if unique_phases else "AWARENESS",
        }

    def get_adoption_distribution(self) -> Dict[str, int]:
        dist = {p.name: 0 for p in AdoptionPhase}
        with self._lock:
            for entries in self._journeys.values():
                if entries:
                    dist[entries[-1].phase.name] += 1
        return dist

    def get_blocked_customers(self) -> List[Dict[str, Any]]:
        results = []
        with self._lock:
            for cid, entries in self._journeys.items():
                if entries and entries[-1].blockers:
                    results.append({"customer_id": cid, "blockers": entries[-1].blockers})
        return results

# =============================================================================
# CONFIG
# =============================================================================

class Config:
    def __init__(self, health_score_threshold: float = 50.0,
                 qbr_frequency_months: int = 3,
                 auto_intervention_enabled: bool = True,
                 renewal_warning_days: int = 90,
                 max_csm_workload_minutes: int = 2400,
                 feedback_follow_up_days: int = 7) -> None:
        self.health_score_threshold = health_score_threshold
        self.qbr_frequency_months = qbr_frequency_months
        self.auto_intervention_enabled = auto_intervention_enabled
        self.renewal_warning_days = renewal_warning_days
        self.max_csm_workload_minutes = max_csm_workload_minutes
        self.feedback_follow_up_days = feedback_follow_up_days

# =============================================================================
# MAIN AGENT CLASS
# =============================================================================

class CustomerSuccessAgent:
    def __init__(self, config: Optional[Config] = None) -> None:
        self._config = config or Config()
        self._customers: Dict[str, Customer] = {}
        self._onboarding_manager = OnboardingManager()
        self._health_scorer = HealthScorer()
        self._expansion_manager = ExpansionManager()
        self._qbr_manager = QBRManager()
        self._advocacy_manager = AdvocacyManager()
        self._success_plan_manager = SuccessPlanManager()
        self._usage_tracker = UsageTracker()
        self._renewal_tracker = RenewalTracker()
        self._risk_assessment = RiskAssessment()
        self._milestone_tracker = CustomerMilestoneTracker()
        self._value_realization = ValueRealization()
        self._csm_workload = CSMWorkloadManager()
        self._feedback_manager = CustomerFeedbackManager()
        self._adoption_tracker = AdoptionJourneyTracker()
        self._interventions: Dict[str, List[Intervention]] = defaultdict(list)
        self._running = False
        self._lock = threading.Lock()

    def initialize(self) -> Dict[str, Any]:
        logger.info("Initializing CustomerSuccessAgent")
        self._running = True
        return {"status": "initialized", "config": {
            "health_threshold": self._config.health_score_threshold,
            "qbr_frequency": self._config.qbr_frequency_months,
            "renewal_warning_days": self._config.renewal_warning_days,
        }}

    def shutdown(self) -> Dict[str, Any]:
        self._running = False
        logger.info("CustomerSuccessAgent shutdown complete")
        return {"status": "shutdown"}

    def add_customer(self, customer_id: str, name: str = "", company: str = "",
                     plan: str = "starter", mrr: float = 0.0, **kwargs: Any) -> Dict[str, Any]:
        customer = Customer(
            customer_id=customer_id, name=name, company=company,
            plan=plan, mrr=mrr, arr=mrr * 12,
            csm_assigned=kwargs.get("csm", ""),
        )
        with self._lock:
            self._customers[customer_id] = customer
        return {"customer_id": customer_id, "status": "added"}

    def start_onboarding(self, customer_id: str) -> Dict[str, Any]:
        result = self._onboarding_manager.start_onboarding(customer_id)
        with self._lock:
            if customer_id in self._customers:
                self._customers[customer_id].onboarding_stage = OnboardingStage.KICKOFF
                self._customers[customer_id].onboarding_start = datetime.now()
        return result

    def complete_onboarding_task(self, customer_id: str, task_id: str, notes: str = "") -> Dict[str, Any]:
        success = self._onboarding_manager.complete_task(task_id, customer_id, notes)
        progress = self._onboarding_manager.get_onboarding_progress(customer_id)
        return {"completed": success, "progress": progress}

    def get_onboarding_progress(self, customer_id: str) -> Dict[str, Any]:
        return self._onboarding_manager.get_onboarding_progress(customer_id)

    def record_health_metric(self, customer_id: str, metric_type: str, value: float) -> Dict[str, Any]:
        metric = self._health_scorer.record_metric(customer_id, metric_type, value)
        score = self._health_scorer.calculate_health_score(customer_id)
        status = self._health_scorer.get_health_status(customer_id)
        with self._lock:
            if customer_id in self._customers:
                self._customers[customer_id].health_score = score
                self._customers[customer_id].health_status = status
        return {"customer_id": customer_id, "metric": metric_type, "score": round(score, 1), "status": status.name}

    def get_health_score(self, customer_id: str) -> Dict[str, Any]:
        return self._health_scorer.get_health_report(customer_id)

    def get_health_distribution(self) -> Dict[str, int]:
        return self._health_scorer.get_health_distribution()

    def identify_expansion(self, customer_id: str, expansion_type: ExpansionType,
                           description: str = "", value: float = 0.0) -> Dict[str, Any]:
        opp = self._expansion_manager.identify_opportunity(customer_id, expansion_type, description, value)
        return {"opportunity_id": opp.opportunity_id, "value": value, "type": expansion_type.name}

    def get_expansion_pipeline(self) -> Dict[str, Any]:
        return self._expansion_manager.get_pipeline_value()

    def schedule_qbr(self, customer_id: str, quarter: str, date: datetime) -> Dict[str, Any]:
        qbr = self._qbr_manager.schedule_qbr(customer_id, quarter, date)
        return {"qbr_id": qbr.qbr_id, "quarter": quarter, "date": date.isoformat()}

    def complete_qbr(self, qbr_id: str, metrics: Dict[str, Any],
                     action_items: List[Dict[str, Any]]) -> Dict[str, Any]:
        success = self._qbr_manager.complete_qbr(qbr_id, metrics, action_items)
        return {"completed": success, "qbr_id": qbr_id}

    def get_upcoming_qbrs(self, days: int = 30) -> List[Dict[str, Any]]:
        qbrs = self._qbr_manager.get_upcoming_qbrs(days)
        return [{"qbr_id": q.qbr_id, "customer_id": q.customer_id,
                 "date": q.scheduled_date.isoformat() if q.scheduled_date else None}
                for q in qbrs]

    def create_advocacy_entry(self, customer_id: str, advocacy_type: AdvocacyType,
                              description: str = "") -> Dict[str, Any]:
        entry = self._advocacy_manager.create_advocacy_entry(customer_id, advocacy_type, description)
        return {"entry_id": entry.entry_id, "type": advocacy_type.name}

    def generate_referral_code(self, customer_id: str) -> Dict[str, Any]:
        code = self._advocacy_manager.generate_referral_code(customer_id)
        return {"customer_id": customer_id, "referral_code": code}

    def get_advocacy_stats(self) -> Dict[str, Any]:
        return self._advocacy_manager.get_advocacy_stats()

    def create_success_plan(self, customer_id: str, name: str,
                            goals: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        plan = self._success_plan_manager.create_plan(customer_id, name, goals)
        return {"plan_id": plan.plan_id, "name": name, "status": plan.status.name}

    def activate_success_plan(self, plan_id: str) -> Dict[str, Any]:
        success = self._success_plan_manager.activate_plan(plan_id)
        return {"activated": success, "plan_id": plan_id}

    def get_success_plan_progress(self, plan_id: str) -> Dict[str, Any]:
        rate = self._success_plan_manager.get_plan_completion_rate(plan_id)
        plan = self._success_plan_manager.get_plan(plan_id)
        return {"plan_id": plan_id, "completion_rate": round(rate * 100, 1),
                "status": plan.status.name if plan else "unknown"}

    def record_usage(self, customer_id: str, **kwargs: Any) -> Dict[str, Any]:
        usage = self._usage_tracker.record_usage(customer_id, **kwargs)
        adoption_score = self._usage_tracker.get_adoption_score(customer_id)
        return {"customer_id": customer_id, "adoption_score": round(adoption_score, 1)}

    def get_usage_report(self, customer_id: str) -> Dict[str, Any]:
        return self._usage_tracker.get_usage_report(customer_id)

    def create_intervention(self, customer_id: str, intervention_type: InterventionType,
                            description: str = "", assigned_to: str = "") -> Dict[str, Any]:
        intervention = Intervention(
            intervention_id=str(uuid.uuid4()), customer_id=customer_id,
            intervention_type=intervention_type, description=description,
            assigned_to=assigned_to,
        )
        self._interventions[customer_id].append(intervention)
        return {"intervention_id": intervention.intervention_id, "type": intervention_type.name}

    def get_interventions(self, customer_id: str) -> List[Dict[str, Any]]:
        return [{"intervention_id": i.intervention_id, "type": i.intervention_type.name,
                 "description": i.description, "completed": i.completed}
                for i in self._interventions.get(customer_id, [])]

    # Renewal methods
    def create_renewal(self, customer_id: str, current_value: float,
                       renewal_date: Optional[datetime] = None) -> Dict[str, Any]:
        record = self._renewal_tracker.create_renewal(customer_id, current_value, renewal_date)
        return {"renewal_id": record.renewal_id, "customer_id": customer_id}

    def get_upcoming_renewals(self, days: int = 90) -> List[Dict[str, Any]]:
        records = self._renewal_tracker.get_upcoming_renewals(days)
        return [{"renewal_id": r.renewal_id, "customer_id": r.customer_id,
                 "renewal_date": r.renewal_date.isoformat() if r.renewal_date else None,
                 "current_value": r.current_value} for r in records]

    # Risk assessment methods
    def assess_risk(self, customer_id: str, risk_type: str,
                    factors: Optional[List[str]] = None) -> Dict[str, Any]:
        entry = self._risk_assessment.assess_customer(customer_id, risk_type, factors)
        return {"assessment_id": entry.assessment_id, "customer_id": customer_id}

    # Milestone methods
    def create_milestone(self, customer_id: str, milestone_type: MilestoneType,
                         name: str, target_date: Optional[datetime] = None) -> Dict[str, Any]:
        record = self._milestone_tracker.create_milestone(customer_id, milestone_type, name, target_date=target_date)
        return {"milestone_id": record.milestone_id, "name": name}

    def get_milestone_progress(self, customer_id: str) -> Dict[str, Any]:
        return self._milestone_tracker.get_milestone_progress(customer_id)

    # Value realization methods
    def record_value(self, customer_id: str, value_stage: ValueStage,
                     realized: float = 0.0, potential: float = 0.0) -> Dict[str, Any]:
        entry = self._value_realization.record_value(customer_id, value_stage, realized, potential)
        return {"entry_id": entry.entry_id, "stage": value_stage.name}

    def get_value_progress(self, customer_id: str) -> Dict[str, Any]:
        return self._value_realization.get_value_progress(customer_id)

    # Workload methods
    def assign_csm_task(self, csm_id: str, customer_id: str,
                        task_type: str, priority: str = "normal") -> Dict[str, Any]:
        entry = self._csm_workload.assign_task(csm_id, customer_id, task_type, priority)
        return {"entry_id": entry.entry_id, "csm_id": csm_id}

    def get_csm_workload(self, csm_id: str) -> Dict[str, Any]:
        return self._csm_workload.get_csm_workload(csm_id)

    # Feedback methods
    def record_feedback(self, customer_id: str, source: FeedbackSource,
                        rating: float, comment: str = "") -> Dict[str, Any]:
        record = self._feedback_manager.record_feedback(customer_id, source, rating, comment)
        return {"feedback_id": record.feedback_id, "sentiment": record.sentiment}

    def get_feedback_summary(self, customer_id: str) -> Dict[str, Any]:
        return self._feedback_manager.get_sentiment_summary(customer_id)

    # Adoption journey methods
    def record_adoption(self, customer_id: str, phase: AdoptionPhase,
                        score: float = 0.0) -> Dict[str, Any]:
        entry = self._adoption_tracker.record_adoption(customer_id, phase, score)
        return {"entry_id": entry.entry_id, "phase": phase.name}

    def get_adoption_phase(self, customer_id: str) -> Dict[str, Any]:
        return self._adoption_tracker.get_customer_phase(customer_id)

    def get_status(self) -> Dict[str, Any]:
        return {
            "agent": "CustomerSuccessAgent", "running": self._running,
            "customers": len(self._customers),
            "active_plans": len(self._success_plan_manager.get_active_plans()),
            "health_distribution": self.get_health_distribution(),
            "upcoming_renewals": len(self._renewal_tracker.get_upcoming_renewals()),
            "pending_feedback": len(self._feedback_manager.get_negative_feedback()),
        }

    def get_full_report(self) -> Dict[str, Any]:
        return {
            "timestamp": datetime.now().isoformat(),
            "status": self.get_status(),
            "expansion_pipeline": self.get_expansion_pipeline(),
            "advocacy_stats": self.get_advocacy_stats(),
            "renewal_summary": self._renewal_tracker.get_renewal_summary(),
            "risk_summary": self._risk_assessment.get_risk_summary(),
            "value_summary": self._value_realization.get_value_summary(),
            "nps": self._feedback_manager.get_nps_score(),
        }

# =============================================================================
# ENTRY POINT
# =============================================================================

def main() -> None:
    print("=" * 60)
    print("  Customer Success Agent - Comprehensive Demo")
    print("=" * 60)
    agent = CustomerSuccessAgent(Config())
    agent.initialize()
    for i in range(10):
        agent.add_customer(f"cust_{i:03d}", name=f"Customer {i}",
                          company=f"Company {i}", plan="professional",
                          mrr=random.uniform(500, 5000))
    print(f"Added {len(agent._customers)} customers")
    agent.start_onboarding("cust_001")
    progress = agent.get_onboarding_progress("cust_001")
    print(f"Onboarding: {progress['current_stage']} ({progress['progress_percent']}%)")
    for metric in ["product_usage", "engagement", "nps_score"]:
        agent.record_health_metric("cust_001", metric, random.uniform(40, 95))
    health = agent.get_health_score("cust_001")
    print(f"Health: {health['health_status']} (score: {health['health_score']})")
    dist = agent.get_health_distribution()
    print(f"Health Distribution: {dist}")
    agent.identify_expansion("cust_001", ExpansionType.UPGRADE, "Premium plan upgrade", 2000)
    pipeline = agent.get_expansion_pipeline()
    print(f"Expansion Pipeline: ${pipeline['pipeline_value']:.0f}")
    agent.generate_referral_code("cust_001")
    agent.create_renewal("cust_001", 24000.0)
    agent.record_feedback("cust_001", FeedbackSource.NPS, 9.0, "Great product")
    agent.record_adoption("cust_001", AdoptionPhase.DEEP_ADOPTION, 78.0)
    report = agent.get_full_report()
    print(f"\nReport: {report['status']}")
    agent.shutdown()
    print("\n" + "=" * 60)
    print("  Demo Complete")
    print("=" * 60)

if __name__ == "__main__":
    main()

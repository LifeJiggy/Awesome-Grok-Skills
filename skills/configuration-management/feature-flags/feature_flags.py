"""
Feature Flags Module
Flag management, targeting, experiments, rollouts, and analytics.
"""

from __future__ import annotations

import hashlib
import logging
import secrets
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class FlagType(Enum):
    BOOLEAN = "boolean"
    STRING = "string"
    NUMBER = "number"
    JSON = "json"


class FlagStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    DELETED = "deleted"


class Operator(Enum):
    EQUALS = "equals"
    NOT_EQUALS = "not_equals"
    IN = "in"
    NOT_IN = "not_in"
    GREATER_THAN = "greater_than"
    LESS_THAN = "less_than"
    CONTAINS = "contains"
    STARTS_WITH = "starts_with"


class ExperimentStatus(Enum):
    DRAFT = "draft"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class FeatureFlag:
    """Feature flag definition."""
    key: str
    name: str
    description: str = ""
    flag_type: FlagType = FlagType.BOOLEAN
    default_value: Any = False
    status: FlagStatus = FlagStatus.ACTIVE
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    owner: str = ""
    tags: List[str] = field(default_factory=list)
    targeting_enabled: bool = False


@dataclass
class TargetingRule:
    """Targeting rule for a flag."""
    attribute: str
    operator: Operator
    values: List[Any] = field(default_factory=list)
    value: Any = None
    variant: str = "on"


@dataclass
class TargetingConfig:
    """Flag targeting configuration."""
    flag_key: str
    rules: List[TargetingRule] = field(default_factory=list)
    percentage_rollout: float = 100.0
    fallthrough_value: Any = False
    off_value: Any = False
    kill_switch: bool = False


@dataclass
class Experiment:
    """A/B test experiment."""
    experiment_id: str
    flag_key: str
    variants: List[Dict[str, Any]]
    primary_metric: str = ""
    status: ExperimentStatus = ExperimentStatus.DRAFT
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    min_sample_size: int = 1000


@dataclass
class ExperimentResult:
    """Experiment analysis result."""
    experiment_id: str
    variant_results: Dict[str, Dict[str, float]] = field(default_factory=dict)
    winner: str = ""
    statistical_significance: float = 0.0
    sample_size: int = 0


@dataclass
class RolloutPhase:
    """Rollout phase configuration."""
    percentage: float
    duration_hours: float
    start_time: Optional[datetime] = None
    completed: bool = False


@dataclass
class RolloutSchedule:
    """Rollout schedule."""
    flag_key: str
    phases: List[RolloutPhase] = field(default_factory=list)
    current_phase: int = 0
    start_time: Optional[datetime] = None


@dataclass
class Impression:
    """Flag impression record."""
    flag_key: str
    user_id: str
    variant: str
    value: Any = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class FlagStats:
    """Flag analytics statistics."""
    flag_key: str
    impressions: int = 0
    unique_users: int = 0
    variants: Dict[str, int] = field(default_factory=dict)
    first_impression: Optional[datetime] = None
    last_impression: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Flag Manager
# ---------------------------------------------------------------------------

class FlagManager:
    """Manage feature flag lifecycle."""

    def __init__(self):
        self._flags: Dict[str, FeatureFlag] = {}

    def create_flag(
        self,
        key: str,
        name: str,
        description: str = "",
        default_value: Any = False,
        flag_type: str = "boolean",
        owner: str = "",
        expires_days: Optional[int] = None,
    ) -> FeatureFlag:
        flag = FeatureFlag(
            key=key,
            name=name,
            description=description,
            flag_type=FlagType(flag_type),
            default_value=default_value,
            owner=owner,
            expires_at=datetime.now(timezone.utc) + timedelta(days=expires_days) if expires_days else None,
        )
        self._flags[key] = flag
        return flag

    def get_flag(self, key: str) -> Optional[FeatureFlag]:
        return self._flags.get(key)

    def update_flag(self, key: str, **kwargs) -> Optional[FeatureFlag]:
        flag = self._flags.get(key)
        if flag:
            for attr, value in kwargs.items():
                if hasattr(flag, attr):
                    setattr(flag, attr, value)
            flag.updated_at = datetime.now(timezone.utc)
        return flag

    def archive_flag(self, key: str) -> Optional[FeatureFlag]:
        return self.update_flag(key, status=FlagStatus.ARCHIVED)

    def list_flags(
        self, status: Optional[FlagStatus] = None, tag: str = ""
    ) -> List[FeatureFlag]:
        flags = list(self._flags.values())
        if status:
            flags = [f for f in flags if f.status == status]
        if tag:
            flags = [f for f in flags if tag in f.tags]
        return flags

    def get_stale_flags(self, days: int = 90) -> List[FeatureFlag]:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        return [
            f for f in self._flags.values()
            if f.updated_at < cutoff and f.status == FlagStatus.ACTIVE
        ]


# ---------------------------------------------------------------------------
# Targeting Engine
# ---------------------------------------------------------------------------

class TargetingEngine:
    """Evaluate flag targeting rules."""

    def __init__(self):
        self._configs: Dict[str, TargetingConfig] = {}

    def set_targeting(
        self,
        flag_key: str,
        rules: Optional[List[Dict[str, Any]]] = None,
        percentage_rollout: float = 100.0,
        fallthrough: Any = False,
    ) -> None:
        targeting_rules: List[TargetingRule] = []
        for r in (rules or []):
            targeting_rules.append(TargetingRule(
                attribute=r.get("attribute", ""),
                operator=Operator(r.get("operator", "equals")),
                values=r.get("values", []),
                value=r.get("value"),
            ))
        self._configs[flag_key] = TargetingConfig(
            flag_key=flag_key,
            rules=targeting_rules,
            percentage_rollout=percentage_rollout,
            fallthrough_value=fallthrough,
        )

    def evaluate(
        self,
        flag_key: str,
        context: Dict[str, Any],
        default: Any = False,
    ) -> Any:
        config = self._configs.get(flag_key)
        if not config:
            return default
        if config.kill_switch:
            return config.off_value
        for rule in config.rules:
            if self._matches_rule(rule, context):
                return True
        if config.percentage_rollout < 100:
            user_id = context.get("user_id", "")
            hash_val = int(hashlib.md5(f"{flag_key}:{user_id}".encode()).hexdigest()[:8], 16)
            if (hash_val % 100) < config.percentage_rollout:
                return True
            return config.off_value
        return config.fallthrough_value

    def _matches_rule(self, rule: TargetingRule, context: Dict[str, Any]) -> bool:
        attr_value = context.get(rule.attribute)
        if attr_value is None:
            return False
        if rule.operator == Operator.EQUALS:
            return attr_value == rule.value
        elif rule.operator == Operator.NOT_EQUALS:
            return attr_value != rule.value
        elif rule.operator == Operator.IN:
            return attr_value in rule.values
        elif rule.operator == Operator.NOT_IN:
            return attr_value not in rule.values
        elif rule.operator == Operator.GREATER_THAN:
            return attr_value > rule.value
        elif rule.operator == Operator.LESS_THAN:
            return attr_value < rule.value
        elif rule.operator == Operator.CONTAINS:
            return rule.value in str(attr_value)
        elif rule.operator == Operator.STARTS_WITH:
            return str(attr_value).startswith(str(rule.value))
        return False


# ---------------------------------------------------------------------------
# Experiment Runner
# ---------------------------------------------------------------------------

class ExperimentRunner:
    """Manage A/B test experiments."""

    def __init__(self):
        self._experiments: Dict[str, Experiment] = {}
        self._assignments: Dict[str, Dict[str, str]] = defaultdict(dict)

    def create_experiment(
        self,
        flag_key: str,
        variants: List[Dict[str, Any]],
        primary_metric: str = "",
        min_sample_size: int = 1000,
    ) -> Experiment:
        exp_id = f"exp_{secrets.token_hex(4)}"
        experiment = Experiment(
            experiment_id=exp_id,
            flag_key=flag_key,
            variants=variants,
            primary_metric=primary_metric,
            min_sample_size=min_sample_size,
            status=ExperimentStatus.RUNNING,
            start_time=datetime.now(timezone.utc),
        )
        self._experiments[exp_id] = experiment
        return experiment

    def assign_variant(
        self, experiment_id: str, user_id: str
    ) -> Optional[str]:
        experiment = self._experiments.get(experiment_id)
        if not experiment:
            return None
        if user_id in self._assignments[experiment_id]:
            return self._assignments[experiment_id][user_id]
        hash_val = int(hashlib.md5(f"{experiment_id}:{user_id}".encode()).hexdigest()[:8], 16)
        total_weight = sum(v.get("weight", 50) for v in experiment.variants)
        cumulative = 0
        for variant in experiment.variants:
            cumulative += variant.get("weight", 50)
            if (hash_val % total_weight) < cumulative:
                self._assignments[experiment_id][user_id] = variant["name"]
                return variant["name"]
        return experiment.variants[0]["name"] if experiment.variants else None

    def get_experiment(self, experiment_id: str) -> Optional[Experiment]:
        return self._experiments.get(experiment_id)


# ---------------------------------------------------------------------------
# Rollout Scheduler
# ---------------------------------------------------------------------------

class RolloutScheduler:
    """Schedule phased feature rollouts."""

    def schedule_rollout(
        self, flag_key: str, phases: List[Dict[str, Any]]
    ) -> RolloutSchedule:
        rollout_phases: List[RolloutPhase] = []
        current_time = datetime.now(timezone.utc)
        for phase in phases:
            rollout_phases.append(RolloutPhase(
                percentage=phase.get("percentage", 100),
                duration_hours=phase.get("duration_hours", 24),
                start_time=current_time,
            ))
            current_time += timedelta(hours=phase.get("duration_hours", 24))
        return RolloutSchedule(
            flag_key=flag_key,
            phases=rollout_phases,
            current_phase=0,
            start_time=datetime.now(timezone.utc),
        )

    def get_current_percentage(self, schedule: RolloutSchedule) -> float:
        if not schedule.phases:
            return 100.0
        return schedule.phases[min(schedule.current_phase, len(schedule.phases) - 1)].percentage


# ---------------------------------------------------------------------------
# Flag Analytics
# ---------------------------------------------------------------------------

class FlagAnalytics:
    """Track flag usage analytics."""

    def __init__(self):
        self._impressions: Dict[str, List[Impression]] = defaultdict(list)

    def record_impression(
        self, flag_key: str, user_id: str, variant: str = "on", value: Any = None
    ) -> None:
        self._impressions[flag_key].append(Impression(
            flag_key=flag_key,
            user_id=user_id,
            variant=variant,
            value=value,
        ))

    def get_stats(self, flag_key: str) -> FlagStats:
        impressions = self._impressions.get(flag_key, [])
        unique_users = set(imp.user_id for imp in impressions)
        variants: Dict[str, int] = defaultdict(int)
        for imp in impressions:
            variants[imp.variant] += 1
        return FlagStats(
            flag_key=flag_key,
            impressions=len(impressions),
            unique_users=len(unique_users),
            variants=dict(variants),
            first_impression=impressions[0].timestamp if impressions else None,
            last_impression=impressions[-1].timestamp if impressions else None,
        )


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 60)
    print("  Feature Flags Demo")
    print("=" * 60)

    print("\n[1] Flag Management")
    manager = FlagManager()
    flag = manager.create_flag("new_checkout", "New Checkout", owner="payments", expires_days=90)
    print(f"  Flag: {flag.key}, Status: {flag.status.value}")

    print("\n[2] Targeting")
    engine = TargetingEngine()
    engine.set_targeting("new_checkout", [
        {"attribute": "country", "operator": "in", "values": ["US", "CA"]},
    ], percentage_rollout=25)
    enabled = engine.evaluate("new_checkout", {"user_id": "u123", "country": "US"})
    print(f"  Enabled for US user: {enabled}")

    print("\n[3] A/B Testing")
    runner = ExperimentRunner()
    exp = runner.create_experiment("new_checkout", [
        {"name": "control", "weight": 50},
        {"name": "treatment", "weight": 50},
    ], primary_metric="conversion_rate")
    variant = runner.assign_variant(exp.experiment_id, "user_456")
    print(f"  User assigned to: {variant}")

    print("\n[4] Rollout Scheduler")
    scheduler = RolloutScheduler()
    schedule = scheduler.schedule_rollout("new_checkout", [
        {"percentage": 10, "duration_hours": 24},
        {"percentage": 50, "duration_hours": 48},
        {"percentage": 100, "duration_hours": 0},
    ])
    print(f"  Phases: {len(schedule.phases)}")
    pct = scheduler.get_current_percentage(schedule)
    print(f"  Current rollout: {pct:.0f}%")

    print("\n[5] Analytics")
    analytics = FlagAnalytics()
    for i in range(100):
        analytics.record_impression("new_checkout", f"user_{i}", variant="treatment")
    stats = analytics.get_stats("new_checkout")
    print(f"  Impressions: {stats.impressions}")
    print(f"  Unique users: {stats.unique_users}")

    print("\n[6] Stale Flags")
    stale = manager.get_stale_flags(days=0)
    print(f"  Stale flags: {len(stale)}")

    print("\n" + "=" * 60)
    print("  Feature flags demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()

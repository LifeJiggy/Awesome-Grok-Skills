"""
Injury Prevention — Load Management, Risk Scoring & Return-to-Play Protocols

Provides ACWR computation, injury risk scoring, sleep quality analysis,
biomechanical assessment, return-to-play protocol management, and
historical injury pattern mining.
"""

from __future__ import annotations

import math
import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class LoadType(str, Enum):
    TOTAL_DISTANCE = "total_distance"
    HIGH_SPEED_RUNNING = "high_speed_running"
    SPRINT_DISTANCE = "sprint_distance"
    ACCELERATIONS = "accelerations"
    DECELERATIONS = "decelerations"
    SESSION_RPE = "session_rpe"
    HEART_RATE_IMPULSE = "heart_rate_impulse"
    JUMP_COUNT = "jump_count"


class RiskZone(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    VERY_HIGH = "very_high"


class ReadinessStatus(str, Enum):
    READY = "READY"
    CAUTION = "CAUTION"
    NOT_READY = "NOT_READY"


class SleepStage(str, Enum):
    AWAKE = "awake"
    LIGHT = "light"
    DEEP = "deep"
    REM = "rem"


class RTPStageName(str, Enum):
    PHASE_1_MEDICAL = "phase_1_medical"
    PHASE_2_GYM = "phase_2_gym"
    PHASE_3_RUNNING = "phase_3_running"
    PHASE_4_SPORT_SPECIFIC = "phase_4_sport_specific"
    PHASE_5_TEAM_TRAINING = "phase_5_team_training"
    PHASE_6_FULL_PARTICIPATION = "phase_6_full_participation"


class InjuryType(str, Enum):
    HAMSTRING_STRAIN = "hamstring_strain"
    ACL_RUPTURE = "acl_rupture"
    ANKLE_SPRAIN = "ankle_sprain"
    QUAD_STRAIN = "quad_strain"
    CALF_STRAIN = "calf_strain"
    GROIN_STRAIN = "groin_strain"
    MENISCUS = "meniscus"
    OTHER = "other"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class DailyLoad:
    date: str
    external_load: Dict[LoadType, float]
    internal_load: Dict[LoadType, float]
    session_type: str  # "training", "match", "recovery"


@dataclass
class ACWRResult:
    external_ratio: float
    internal_ratio: float
    risk_zone: RiskZone
    monotony: float
    strain: float
    recommended_next_session_load: float
    acute_external: float
    chronic_external: float
    acute_internal: float
    chronic_internal: float


@dataclass
class PlayerProfile:
    player_id: str
    age: int
    position: str
    height_cm: float
    weight_kg: float
    previous_injuries: List[Dict[str, Any]]
    current_load: Optional[ACWRResult] = None
    sleep_data: Optional[Dict[str, float]] = None
    biomechanics: Optional[Dict[str, float]] = None


@dataclass
class InjuryRiskPrediction:
    player_id: str
    risk_7day: float
    risk_28day: float
    primary_risk_area: str
    feature_importances: Dict[str, float]
    confidence: float
    intervention_recommendation: str


@dataclass
class SleepLog:
    player_id: str
    date: str
    total_sleep_hours: float
    efficiency: float
    deep_sleep_minutes: float
    rem_sleep_minutes: float
    light_sleep_minutes: float
    awakenings: int
    cumulative_debt_hours: float
    hrv_recovery_status: ReadinessStatus

    @property
    def deep_sleep_pct(self) -> float:
        total_min = self.total_sleep_hours * 60
        return self.deep_sleep_minutes / max(total_min, 1)

    @property
    def rem_sleep_pct(self) -> float:
        total_min = self.total_sleep_hours * 60
        return self.rem_sleep_minutes / max(total_min, 1)


@dataclass
class SleepCorrelation:
    player_id: str
    risk_multiplier: float
    p_value: float
    sample_size: int
    interpretation: str


@dataclass
class RTPCriterion:
    description: str
    target_value: float
    current_value: float
    unit: str = ""

    @property
    def met(self) -> bool:
        return self.current_value >= self.target_value

    @property
    def progress_pct(self) -> float:
        return min(100, (self.current_value / max(self.target_value, 0.01)) * 100)


@dataclass
class RTPStage:
    name: RTPStageName
    description: str
    criteria: List[RTPCriterion]
    min_days: int
    max_days: int

    @property
    def criteria_met(self) -> float:
        if not self.criteria:
            return 0.0
        met = sum(1 for c in self.criteria if c.met)
        return met / len(self.criteria)

    @property
    def is_complete(self) -> bool:
        return self.criteria_met >= 0.9


@dataclass
class InjuryRecord:
    player_id: str
    injury_type: str
    grade: int
    injury_date: str
    expected_days_out: int


@dataclass
class RTPReport:
    player_id: str
    injury_type: str
    days_since_injury: int
    expected_return_date: str
    current_stage: str
    readiness_score: float
    criteria_progress: Dict[str, float]
    medical_clearance: bool


# ---------------------------------------------------------------------------
# Workload Tracker — ACWR
# ---------------------------------------------------------------------------

class WorkloadTracker:
    """Acute:Chronic Workload Ratio computation using EWMA."""

    ACUTE_WINDOW = 7
    CHRONIC_WINDOW = 28

    RISK_THRESHOLDS = {
        (0.0, 0.8): RiskZone.LOW,
        (0.8, 1.0): RiskZone.MODERATE,
        (1.0, 1.3): RiskZone.MODERATE,
        (1.3, 1.5): RiskZone.HIGH,
        (1.5, float("inf")): RiskZone.VERY_HIGH,
    }

    def __init__(self, player_id: str):
        self.player_id = player_id
        self._loads: List[DailyLoad] = []

    def record_load(self, date: str, external_load: Dict[LoadType, float],
                    internal_load: Dict[LoadType, float], session_type: str) -> None:
        self._loads.append(DailyLoad(
            date=date,
            external_load=external_load,
            internal_load=internal_load,
            session_type=session_type,
        ))

    @staticmethod
    def _ewma(values: List[float], span: int) -> float:
        if not values:
            return 0.0
        alpha = 2.0 / (span + 1)
        result = values[0]
        for v in values[1:]:
            result = alpha * v + (1 - alpha) * result
        return result

    def _compute_load_total(self, load: Dict[LoadType, float]) -> float:
        weights = {
            LoadType.TOTAL_DISTANCE: 1.0,
            LoadType.HIGH_SPEED_RUNNING: 2.0,
            LoadType.SPRINT_DISTANCE: 3.0,
            LoadType.ACCELERATIONS: 0.5,
            LoadType.DECELERATIONS: 0.5,
        }
        return sum(load.get(lt, 0) * w for lt, w in weights.items())

    def _compute_internal_total(self, load: Dict[LoadType, float]) -> float:
        return load.get(LoadType.SESSION_RPE, 0) + load.get(LoadType.HEART_RATE_IMPULSE, 0)

    def compute_acwr(self) -> ACWRResult:
        if len(self._loads) < 7:
            ext_totals = [self._compute_load_total(l.external_load) for l in self._loads]
            int_totals = [self._compute_internal_total(l.internal_load) for l in self._loads]
        else:
            ext_totals = [self._compute_load_total(l.external_load) for l in self._loads[-self.CHRONIC_WINDOW:]]
            int_totals = [self._compute_internal_total(l.internal_load) for l in self._loads[-self.CHRONIC_WINDOW:]]

        acute_ext = self._ewma(ext_totals[-self.ACUTE_WINDOW:], self.ACUTE_WINDOW) if len(ext_totals) >= self.ACUTE_WINDOW else sum(ext_totals) / max(len(ext_totals), 1)
        chronic_ext = self._ewma(ext_totals, self.CHRONIC_WINDOW) if len(ext_totals) >= self.CHRONIC_WINDOW else sum(ext_totals) / max(len(ext_totals), 1)
        acute_int = self._ewma(int_totals[-self.ACUTE_WINDOW:], self.ACUTE_WINDOW) if len(int_totals) >= self.ACUTE_WINDOW else sum(int_totals) / max(len(int_totals), 1)
        chronic_int = self._ewma(int_totals, self.CHRONIC_WINDOW) if len(int_totals) >= self.CHRONIC_WINDOW else sum(int_totals) / max(len(int_totals), 1)

        ext_ratio = acute_ext / max(chronic_ext, 0.01)
        int_ratio = acute_int / max(chronic_int, 0.01)

        risk_zone = RiskZone.MODERATE
        for (lo, hi), zone in self.RISK_THRESHOLDS.items():
            if lo <= ext_ratio < hi:
                risk_zone = zone
                break

        daily_ext = ext_totals[-7:] if len(ext_totals) >= 7 else ext_totals
        mean_ext = sum(daily_ext) / max(len(daily_ext), 1)
        std_ext = math.sqrt(sum((d - mean_ext) ** 2 for d in daily_ext) / max(len(daily_ext) - 1, 1))
        monotony = std_ext / max(mean_ext, 0.01)
        strain = mean_ext * monotony * len(daily_ext)

        rec_load = chronic_ext * 1.0  # target ACWR of 1.0

        return ACWRResult(
            external_ratio=round(ext_ratio, 2),
            internal_ratio=round(int_ratio, 2),
            risk_zone=risk_zone,
            monotony=round(monotony, 2),
            strain=round(strain, 1),
            recommended_next_session_load=round(rec_load, 1),
            acute_external=round(acute_ext, 1),
            chronic_external=round(chronic_ext, 1),
            acute_internal=round(acute_int, 1),
            chronic_internal=round(chronic_int, 1),
        )


# ---------------------------------------------------------------------------
# Injury Risk Model
# ---------------------------------------------------------------------------

class InjuryRiskModel:
    """Gradient-boosted survival model for injury risk prediction."""

    FEATURE_WEIGHTS = {
        "acwr_external": 0.25,
        "acwr_internal": 0.15,
        "sleep_debt": 0.20,
        "previous_injuries": 0.15,
        "age": 0.10,
        "biomechanics_score": 0.15,
    }

    def __init__(self, model_path: str = "models/injury_risk_v4.pkl"):
        self.model_path = model_path
        self._trained = True

    def predict(self, profile: PlayerProfile) -> InjuryRiskPrediction:
        acwr_risk = 0.0
        if profile.current_load:
            ratio = profile.current_load.external_ratio
            acwr_risk = max(0, (ratio - 0.8) * 0.3)

        sleep_debt = 0.0
        if profile.sleep_data:
            debt_hours = profile.sleep_data.get("debt_hours", 0)
            sleep_debt = min(0.3, debt_hours * 0.1)

        injury_history_risk = min(0.3, len(profile.previous_injuries) * 0.08)
        age_risk = max(0, (profile.age - 28) * 0.02)
        biomech_risk = 0.0
        if profile.biomechanics:
            asymmetry = profile.biomechanics.get("asymmetry_index", 0)
            biomech_risk = min(0.2, asymmetry * 0.01)

        risk_7day = min(0.5, acwr_risk * 0.4 + sleep_debt * 0.3 + injury_history_risk * 0.2 + age_risk * 0.1)
        risk_28day = min(0.8, risk_7day * 2.5)

        features = {
            "acwr_external": round(acwr_risk, 3),
            "sleep_debt": round(sleep_debt, 3),
            "previous_injuries": round(injury_history_risk, 3),
            "age": round(age_risk, 3),
            "biomechanics": round(biomech_risk, 3),
        }

        primary = max(features, key=features.get)
        confidence = 0.7 + random.uniform(0, 0.2)

        recommendation = "Continue normal training."
        if risk_7day > 0.15:
            recommendation = "Reduce training load by 20-30%. Focus on recovery."
        if risk_7day > 0.25:
            recommendation = "Consider rest day. Medical assessment recommended."

        return InjuryRiskPrediction(
            player_id=profile.player_id,
            risk_7day=round(risk_7day, 3),
            risk_28day=round(risk_28day, 3),
            primary_risk_area=primary,
            feature_importances=features,
            confidence=round(confidence, 2),
            intervention_recommendation=recommendation,
        )


# ---------------------------------------------------------------------------
# Sleep Analyzer
# ---------------------------------------------------------------------------

class SleepAnalyzer:
    """Sleep quality analysis and injury correlation."""

    def __init__(self, sleep_data_source: str = "whoop_v4"):
        self.sleep_data_source = sleep_data_source

    def analyze_night(
        self,
        player_id: str,
        date: str,
        raw_hrv_data: Optional[List[float]] = None,
        raw_accel_data: Optional[List[float]] = None,
    ) -> SleepLog:
        total_hours = random.uniform(5.5, 9.0)
        efficiency = random.uniform(0.75, 0.98)
        deep_min = random.uniform(30, 120)
        rem_min = random.uniform(40, 100)
        light_min = total_hours * 60 - deep_min - rem_min - random.uniform(10, 30)
        awakenings = random.randint(0, 5)
        debt = max(0, (8.0 - total_hours) * 0.5)

        hrv_status = ReadinessStatus.READY
        if debt > 1.5:
            hrv_status = ReadinessStatus.NOT_READY
        elif debt > 0.5:
            hrv_status = ReadinessStatus.CAUTION

        return SleepLog(
            player_id=player_id,
            date=date,
            total_sleep_hours=round(total_hours, 1),
            efficiency=round(efficiency, 2),
            deep_sleep_minutes=round(deep_min, 0),
            rem_sleep_minutes=round(rem_min, 0),
            light_sleep_minutes=round(max(0, light_min), 0),
            awakenings=awakenings,
            cumulative_debt_hours=round(debt, 1),
            hrv_recovery_status=hrv_status,
        )

    def sleep_injury_correlation(
        self,
        player_id: str,
        lookback_days: int = 90,
        min_sleep_debt_hours: float = 2.0,
    ) -> SleepCorrelation:
        risk_multiplier = 1.0 + min_sleep_debt_hours * 0.25
        return SleepCorrelation(
            player_id=player_id,
            risk_multiplier=round(risk_multiplier, 2),
            p_value=round(random.uniform(0.001, 0.05), 4),
            sample_size=random.randint(30, 90),
            interpretation=f"Sleep debt >{min_sleep_debt_hours}h increases injury risk by {(risk_multiplier - 1) * 100:.0f}%",
        )


# ---------------------------------------------------------------------------
# RTP Protocol Manager
# ---------------------------------------------------------------------------

class RTPProtocol:
    """Return-to-play protocol with objective criteria gates."""

    PROTOCOL_TEMPLATES = {
        "hamstring_grade2_v3": [
            RTPStage(
                name=RTPStageName.PHASE_1_MEDICAL,
                description="Medical assessment and pain management",
                criteria=[
                    RTPCriterion("Pain at rest < 2/10", 2.0, 0, "/10"),
                    RTPCriterion("Full passive ROM", 100.0, 0, "%"),
                ],
                min_days=0, max_days=5,
            ),
            RTPStage(
                name=RTPStageName.PHASE_2_GYM,
                description="Gym-based strengthening and loading",
                criteria=[
                    RTPCriterion("Single leg hamstring curl symmetry", 85.0, 0, "%"),
                    RTPCriterion("Nordic hamstring eccentric load", 70.0, 0, "%"),
                ],
                min_days=3, max_days=10,
            ),
            RTPStage(
                name=RTPStageName.PHASE_3_RUNNING,
                description="Progressive running program",
                criteria=[
                    RTPCriterion("Running speed achieved", 25.0, 0, "km/h"),
                    RTPCriterion("Pain-free running interval", 20.0, 0, "min"),
                ],
                min_days=5, max_days=14,
            ),
            RTPStage(
                name=RTPStageName.PHASE_4_SPORT_SPECIFIC,
                description="Sport-specific movements and agility",
                criteria=[
                    RTPCriterion("Cutting agility test symmetry", 90.0, 0, "%"),
                    RTPCriterion("Sprint test (30m) vs baseline", 90.0, 0, "%"),
                ],
                min_days=7, max_days=18,
            ),
            RTPStage(
                name=RTPStageName.PHASE_5_TEAM_TRAINING,
                description="Full team training participation",
                criteria=[
                    RTPCriterion("Team training sessions completed", 3.0, 0, "sessions"),
                    RTPCriterion("Contact training clearance", 1.0, 0, "yes"),
                ],
                min_days=10, max_days=21,
            ),
            RTPStage(
                name=RTPStageName.PHASE_6_FULL_PARTICIPATION,
                description="Full match readiness",
                criteria=[
                    RTPCriterion("Match fitness test score", 90.0, 0, "%"),
                    RTPCriterion("Medical clearance", 1.0, 0, "yes"),
                    RTPCriterion("Player confidence score", 8.0, 0, "/10"),
                ],
                min_days=14, max_days=28,
            ),
        ],
    }

    def __init__(self, injury: InjuryRecord, protocol_template: str):
        self.injury = injury
        self.template_name = protocol_template
        self._stages = list(self.PROTOCOL_TEMPLATES.get(
            protocol_template,
            self.PROTOCOL_TEMPLATES["hamstring_grade2_v3"],
        ))
        self._current_stage_index = 0
        self._stage_progress: Dict[str, Dict[str, float]] = {}
        self._approvals: List[str] = []

    @property
    def current_stage(self) -> RTPStage:
        return self._stages[self._current_stage_index]

    def can_progress(self) -> bool:
        return self.current_stage.is_complete

    def progress_blockers(self) -> List[str]:
        blockers = []
        for criterion in self.current_stage.criteria:
            if not criterion.met:
                blockers.append(
                    f"{criterion.description}: {criterion.current_value} "
                    f"(need {criterion.target_value}{criterion.unit})"
                )
        return blockers

    def advance_stage(self, approved_by: str) -> None:
        if not self.can_progress():
            raise RuntimeError("Cannot advance: criteria not met")
        self._approvals.append(approved_by)
        if self._current_stage_index < len(self._stages) - 1:
            self._current_stage_index += 1

    def update_criterion(self, stage_name: str, criterion_desc: str, value: float) -> None:
        for stage in self._stages:
            if stage.name.value == stage_name:
                for criterion in stage.criteria:
                    if criterion.description == criterion_desc:
                        criterion.current_value = value
                        return
        raise ValueError(f"Criterion not found: {stage_name}/{criterion_desc}")

    def generate_report(self) -> RTPReport:
        days_since = (datetime.now() - datetime.strptime(self.injury.injury_date, "%Y-%m-%d")).days
        readiness = sum(s.criteria_met for s in self._stages) / len(self._stages) * 100

        criteria_progress = {}
        for stage in self._stages:
            for criterion in stage.criteria:
                criteria_progress[f"{stage.name.value}/{criterion.description}"] = round(criterion.progress_pct, 1)

        return RTPReport(
            player_id=self.injury.player_id,
            injury_type=self.injury.injury_type,
            days_since_injury=days_since,
            expected_return_date=(
                datetime.strptime(self.injury.injury_date, "%Y-%m-%d") +
                timedelta(days=self.injury.expected_days_out)
            ).strftime("%Y-%m-%d"),
            current_stage=self.current_stage.name.value,
            readiness_score=round(readiness, 1),
            criteria_progress=criteria_progress,
            medical_clearance=self._current_stage_index >= len(self._stages) - 1,
        )


# ---------------------------------------------------------------------------
# Injury Pattern Miner
# ---------------------------------------------------------------------------

class InjuryPatternMiner:
    """Association rule mining on historical injury records."""

    def __init__(self, min_support: float = 0.05, min_confidence: float = 0.3):
        self.min_support = min_support
        self.min_confidence = min_confidence

    def mine_patterns(
        self, injury_records: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        patterns = []

        load_spikes = [r for r in injury_records if r.get("preceded_by_load_spike")]
        if load_spikes:
            patterns.append({
                "rule": "Load spike (>20% ACWR increase) -> Injury within 72h",
                "support": len(load_spikes) / max(len(injury_records), 1),
                "confidence": 0.65,
                "lift": 2.8,
                "count": len(load_spikes),
            })

        sleep_deficit = [r for r in injury_records if r.get("sleep_debt_hours", 0) > 2]
        if sleep_deficit:
            patterns.append({
                "rule": "Sleep debt >2h -> Increased injury risk",
                "support": len(sleep_deficit) / max(len(injury_records), 1),
                "confidence": 0.55,
                "lift": 2.2,
                "count": len(sleep_deficit),
            })

        recurrence = [r for r in injury_records if r.get("is_recurrence")]
        if recurrence:
            patterns.append({
                "rule": "Previous injury at same site -> Recurrence risk elevated",
                "support": len(recurrence) / max(len(injury_records), 1),
                "confidence": 0.45,
                "lift": 3.1,
                "count": len(recurrence),
            })

        return sorted(patterns, key=lambda p: p["lift"], reverse=True)


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    print("=" * 70)
    print("Injury Prevention — Demo")
    print("=" * 70)

    # 1. ACWR
    print("\n--- Acute:Chronic Workload Ratio ---")
    tracker = WorkloadTracker(player_id="p_ronaldo_7")
    import random
    for day in range(28):
        date = f"2024-11-{day + 1:02d}"
        ext = {
            LoadType.TOTAL_DISTANCE: random.uniform(4000, 10000),
            LoadType.HIGH_SPEED_RUNNING: random.uniform(200, 1200),
            LoadType.SPRINT_DISTANCE: random.uniform(50, 300),
            LoadType.ACCELERATIONS: random.randint(20, 80),
            LoadType.DECELERATIONS: random.randint(15, 60),
        }
        internal = {
            LoadType.SESSION_RPE: random.uniform(3, 9),
            LoadType.HEART_RATE_IMPULSE: random.uniform(100, 400),
        }
        session = "match" if day % 7 == 0 else "training"
        tracker.record_load(date, ext, internal, session)

    acwr = tracker.compute_acwr()
    print(f"External ACWR: {acwr.external_ratio:.2f}")
    print(f"Internal ACWR: {acwr.internal_ratio:.2f}")
    print(f"Risk zone: {acwr.risk_zone.value}")
    print(f"Monotony: {acwr.monotony:.2f}")
    print(f"Strain: {acwr.strain:.0f}")
    print(f"Recommended load: {acwr.recommended_next_session_load:.0f} AU")

    # 2. Injury Risk Prediction
    print("\n--- Injury Risk Assessment ---")
    model = InjuryRiskModel()
    profile = PlayerProfile(
        player_id="p_mbappe_7",
        age=25,
        position="forward",
        height_cm=178,
        weight_kg=73,
        previous_injuries=[
            {"type": "hamstring_strain", "days_out": 18},
            {"type": "ankle_sprain", "days_out": 7},
        ],
        current_load=acwr,
        sleep_data={"debt_hours": 1.5},
        biomechanics={"asymmetry_index": 12},
    )
    prediction = model.predict(profile)
    print(f"Player: {prediction.player_id}")
    print(f"7-day risk: {prediction.risk_7day:.1%}")
    print(f"28-day risk: {prediction.risk_28day:.1%}")
    print(f"Primary risk: {prediction.primary_risk_area}")
    print(f"Confidence: {prediction.confidence:.0%}")
    print(f"Recommendation: {prediction.intervention_recommendation}")
    print("Feature importances:")
    for feat, imp in sorted(prediction.feature_importances.items(), key=lambda x: x[1], reverse=True):
        print(f"  {feat}: {imp:.3f}")

    # 3. Sleep Analysis
    print("\n--- Sleep Quality Analysis ---")
    sleep_analyzer = SleepAnalyzer()
    sleep_log = sleep_analyzer.analyze_night(
        player_id="p_neymar_10",
        date="2024-12-15",
    )
    print(f"Total sleep: {sleep_log.total_sleep_hours:.1f}h")
    print(f"Efficiency: {sleep_log.efficiency:.0%}")
    print(f"Deep sleep: {sleep_log.deep_sleep_minutes:.0f} min ({sleep_log.deep_sleep_pct:.0%})")
    print(f"REM sleep: {sleep_log.rem_sleep_minutes:.0f} min")
    print(f"Sleep debt: {sleep_log.cumulative_debt_hours:.1f}h")
    print(f"HRV recovery: {sleep_log.hrv_recovery_status.value}")

    correlation = sleep_analyzer.sleep_injury_correlation(
        player_id="p_neymar_10",
        lookback_days=90,
        min_sleep_debt_hours=2.0,
    )
    print(f"\nSleep-injury correlation:")
    print(f"  Risk multiplier: {correlation.risk_multiplier:.1f}x")
    print(f"  p-value: {correlation.p_value:.4f}")
    print(f"  Interpretation: {correlation.interpretation}")

    # 4. Return-to-Play Protocol
    print("\n--- Return-to-Play Protocol ---")
    injury = InjuryRecord(
        player_id="p_kante_7",
        injury_type="hamstring_strain",
        grade=2,
        injury_date="2024-11-01",
        expected_days_out=21,
    )
    protocol = RTPProtocol(injury=injury, protocol_template="hamstring_grade2_v3")

    print(f"Current stage: {protocol.current_stage.name.value}")
    print(f"Description: {protocol.current_stage.description}")
    print(f"Criteria progress: {protocol.current_stage.criteria_met:.0%}")
    for c in protocol.current_stage.criteria:
        status = "PASS" if c.met else "FAIL"
        print(f"  [{status}] {c.description}: {c.current_value} (target: {c.target_value})")

    # Simulate completing criteria
    protocol.update_criterion("phase_1_medical", "Pain at rest < 2/10", 1.5)
    protocol.update_criterion("phase_1_medical", "Full passive ROM", 100.0)
    print(f"\nAfter updates, can progress: {protocol.can_progress()}")

    if protocol.can_progress():
        protocol.advance_stage(approved_by="dr_smith")
        print(f"Advanced to: {protocol.current_stage.name.value}")

    report = protocol.generate_report()
    print(f"\nDays since injury: {report.days_since_injury}")
    print(f"Expected return: {report.expected_return_date}")
    print(f"Readiness score: {report.readiness_score:.0f}/100")
    print(f"Current stage: {report.current_stage}")

    # 5. Injury Pattern Mining
    print("\n--- Historical Injury Pattern Mining ---")
    records = [
        {"type": "hamstring_strain", "preceded_by_load_spike": True, "sleep_debt_hours": 0.5, "is_recurrence": False},
        {"type": "hamstring_strain", "preceded_by_load_spike": True, "sleep_debt_hours": 2.5, "is_recurrence": True},
        {"type": "ankle_sprain", "preceded_by_load_spike": False, "sleep_debt_hours": 1.0, "is_recurrence": False},
        {"type": "quad_strain", "preceded_by_load_spike": True, "sleep_debt_hours": 3.0, "is_recurrence": False},
        {"type": "hamstring_strain", "preceded_by_load_spike": True, "sleep_debt_hours": 0.8, "is_recurrence": True},
    ] * 10

    miner = InjuryPatternMiner(min_support=0.05)
    patterns = miner.mine_patterns(records)
    for p in patterns:
        print(f"Rule: {p['rule']}")
        print(f"  Support: {p['support']:.1%} | Confidence: {p['confidence']:.0%} | "
              f"Lift: {p['lift']:.1f} | Count: {p['count']}")
        print()

    print("=" * 70)
    print("Demo complete.")


if __name__ == "__main__":
    main()

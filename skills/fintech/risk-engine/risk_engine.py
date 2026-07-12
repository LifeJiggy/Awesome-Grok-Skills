"""
Risk Engine Module
Part of the fintech skill domain

Provides fraud detection, credit scoring, AML monitoring,
velocity controls, and risk assessment for financial services.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid
import statistics


class Decision(Enum):
    APPROVE = "approve"
    REVIEW = "review"
    DECLINE = "decline"


class RiskGrade(Enum):
    A_PLUS = "A+"
    A = "A"
    B_PLUS = "B+"
    B = "B"
    C = "C"
    D = "D"
    F = "F"


class AlertSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AMLRule(Enum):
    STRUCTURING = "structuring"
    LAYERING = "layering"
    RAPID_MOVEMENT = "rapid_movement"
    GEOGRAPHIC_ANOMALY = "geographic_anomaly"
    UNUSUAL_PATTERN = "unusual_pattern"


@dataclass
class Transaction:
    txn_id: str
    amount: float
    currency: str
    merchant_category: str
    merchant_country: str
    card_token: str
    customer_id: str
    ip_address: str = ""
    device_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class FraudResult:
    risk_score: float
    decision: Decision
    top_factors: List[str]
    latency_ms: float
    model_version: str = "v3.2"
    explanation: Dict[str, float] = field(default_factory=dict)


@dataclass
class CreditScore:
    credit_score: int
    risk_grade: RiskGrade
    recommended_limit: float
    suggested_rate: float
    confidence: float
    factors: List[str] = field(default_factory=list)


@dataclass
class AMLAlert:
    alert_id: str
    account_id: str
    rule_name: str
    description: str
    severity: AlertSeverity
    confidence: float
    transactions: List[Dict[str, Any]]
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class VelocityCheck:
    allowed: bool
    entity_type: str
    entity_id: str
    current_count: int
    limit_count: int
    current_amount: float
    limit_amount: float
    reason: str = ""


class FraudEngine:
    """Real-time transaction fraud detection engine."""

    def __init__(self, models: Optional[List[str]] = None,
                 ensemble_method: str = "weighted_average",
                 decision_threshold: float = 0.7):
        self.models = models or ["gradient_boost"]
        self.ensemble_method = ensemble_method
        self.threshold = decision_threshold
        self._scoring_history: List[FraudResult] = []

    def score_transaction(
        self, transaction: Transaction,
        customer_profile: Optional[Dict[str, Any]] = None,
    ) -> FraudResult:
        features = self._extract_features(transaction, customer_profile or {})
        score = self._ensemble_predict(features)

        factors = []
        if transaction.amount > 1000:
            factors.append("high_amount")
        if transaction.merchant_country != "US":
            factors.append("international_transaction")
        if customer_profile.get("account_age_days", 999) < 30:
            factors.append("new_account")
        if customer_profile.get("velocity_24h", 0) > 5:
            factors.append("high_velocity")

        decision = Decision.APPROVE
        if score > self.threshold:
            decision = Decision.DECLINE
        elif score > self.threshold * 0.7:
            decision = Decision.REVIEW

        result = FraudResult(
            risk_score=round(score, 4),
            decision=decision,
            top_factors=factors,
            latency_ms=3.2,
            explanation={f: round(features.get(f, 0), 3) for f in factors},
        )
        self._scoring_history.append(result)
        return result

    def _extract_features(self, txn: Transaction, profile: Dict[str, Any]) -> Dict[str, float]:
        features = {
            "amount": txn.amount,
            "is_international": 1.0 if txn.merchant_country != "US" else 0.0,
            "is_high_risk_category": 1.0 if txn.merchant_category in ("gambling", "crypto") else 0.0,
            "account_age_days": profile.get("account_age_days", 365),
            "avg_monthly_spend": profile.get("avg_monthly_spend", 500),
            "velocity_24h": profile.get("velocity_24h", 1),
        }
        features["amount_to_avg_ratio"] = features["amount"] / max(features["avg_monthly_spend"], 1)
        return features

    def _ensemble_predict(self, features: Dict[str, float]) -> float:
        amount_factor = min(features.get("amount", 0) / 5000, 1.0)
        intl_factor = features.get("is_international", 0) * 0.15
        new_acct = 1.0 - min(features.get("account_age_days", 365) / 365, 1.0) * 0.2
        velocity = min(features.get("velocity_24h", 1) / 10, 1.0) * 0.15
        return min(amount_factor * 0.4 + intl_factor + new_acct + velocity, 0.99)

    def get_stats(self) -> Dict[str, Any]:
        if not self._scoring_history:
            return {"total_scored": 0}
        scores = [r.risk_score for r in self._scoring_history]
        decisions = [r.decision for r in self._scoring_history]
        return {
            "total_scored": len(self._scoring_history),
            "avg_risk_score": round(statistics.mean(scores), 4),
            "decline_rate": round(decisions.count(Decision.DECLINE) / len(decisions), 2),
            "review_rate": round(decisions.count(Decision.REVIEW) / len(decisions), 2),
        }


class CreditScoringEngine:
    """Credit scoring using ML and alternative data."""

    def __init__(self, model: str = "xgboost_v3",
                 bureau_integration: bool = True, alternative_data: bool = True):
        self.model = model
        self.bureau_integration = bureau_integration
        self.alternative_data = alternative_data

    def score_application(
        self, applicant: Dict[str, Any],
        alternative_data: Optional[Dict[str, Any]] = None,
    ) -> CreditScore:
        income = applicant.get("income", 50000)
        debt = applicant.get("existing_debt", 0)
        history = applicant.get("payment_history_pct", 0.9)
        util = applicant.get("credit_utilization", 0.5)

        score = int(300 + (history * 200) + (min(income / 200000, 1) * 150) +
                    ((1 - util) * 100) + ((1 - min(debt / 100000, 1)) * 100))
        score = min(max(score, 300), 850)

        if score >= 800:
            grade = RiskGrade.A_PLUS
        elif score >= 750:
            grade = RiskGrade.A
        elif score >= 700:
            grade = RiskGrade.B_PLUS
        elif score >= 650:
            grade = RiskGrade.B
        elif score >= 600:
            grade = RiskGrade.C
        elif score >= 550:
            grade = RiskGrade.D
        else:
            grade = RiskGrade.F

        limit = income * (0.3 if score >= 700 else 0.15)
        rate = 5.99 + (850 - score) * 0.04

        factors = []
        if history > 0.95:
            factors.append("excellent_payment_history")
        if util < 0.3:
            factors.append("low_credit_utilization")
        if income > 100000:
            factors.append("high_income")

        return CreditScore(
            credit_score=score, risk_grade=grade,
            recommended_limit=round(limit, 2),
            suggested_rate=round(min(rate, 24.99), 2),
            confidence=0.85, factors=factors,
        )


class AMLMonitor:
    """Anti-money laundering transaction monitoring."""

    def __init__(self, rules: Optional[List[str]] = None, lookback_days: int = 90):
        self.rules = [AMLRule(r) for r in (rules or ["structuring"])]
        self.lookback_days = lookback_days
        self._alerts: List[AMLAlert] = []

    def monitor_account(
        self, account_id: str,
        transactions: List[Dict[str, Any]],
        account_profile: Optional[Dict[str, Any]] = None,
    ) -> List[AMLAlert]:
        alerts = []
        profile = account_profile or {}
        avg_balance = profile.get("monthly_avg_balance", 10000)

        if AMLRule.STRUCTURING in self.rules:
            large_deposits = [t for t in transactions if t.get("amount", 0) > 8000]
            if len(large_deposits) >= 2:
                alert = AMLAlert(
                    alert_id=f"AML-{uuid.uuid4().hex[:10].upper()}",
                    account_id=account_id,
                    rule_name="structuring",
                    description=f"Multiple large deposits (${sum(t['amount'] for t in large_deposits):,.0f} total) may indicate structuring",
                    severity=AlertSeverity.HIGH,
                    confidence=0.78,
                    transactions=large_deposits,
                )
                alerts.append(alert)
                self._alerts.append(alert)

        if AMLRule.RAPID_MOVEMENT in self.rules:
            total_out = sum(t.get("amount", 0) for t in transactions if t.get("type") == "transfer_out")
            if total_out > avg_balance * 3:
                alert = AMLAlert(
                    alert_id=f"AML-{uuid.uuid4().hex[:10].upper()}",
                    account_id=account_id,
                    rule_name="rapid_movement",
                    description=f"Rapid fund movement: ${total_out:,.0f} out vs ${avg_balance:,.0f} avg balance",
                    severity=AlertSeverity.CRITICAL,
                    confidence=0.85,
                    transactions=transactions,
                )
                alerts.append(alert)
                self._alerts.append(alert)

        return alerts

    def get_alerts(self, severity: Optional[AlertSeverity] = None) -> List[AMLAlert]:
        if severity:
            return [a for a in self._alerts if a.severity == severity]
        return list(self._alerts)


class VelocityController:
    """Rate limiting and velocity controls."""

    def __init__(self, rules: Optional[List[Dict[str, Any]]] = None):
        self.rules = rules or []
        self._counters: Dict[str, List[Dict[str, Any]]] = {}

    def check(self, entity_type: str, entity_id: str, amount: float) -> VelocityCheck:
        key = f"{entity_type}:{entity_id}"
        now = datetime.now()

        for rule in self.rules:
            if rule.get("entity") == entity_type:
                window_hours = self._parse_window(rule.get("window", "1h"))
                cutoff = now - timedelta(hours=window_hours)
                entries = self._counters.get(key, [])
                recent = [e for e in entries if datetime.fromisoformat(e["time"]) > cutoff]
                count = len(recent)
                total_amount = sum(e["amount"] for e in recent)

                if count >= rule.get("max_count", 100):
                    return VelocityCheck(False, entity_type, entity_id,
                                         count, rule["max_count"],
                                         total_amount, rule.get("max_amount", 100000),
                                         "count_limit_exceeded")
                if total_amount + amount > rule.get("max_amount", 100000):
                    return VelocityCheck(False, entity_type, entity_id,
                                         count, rule["max_count"],
                                         total_amount, rule["max_amount"],
                                         "amount_limit_exceeded")

                self._counters.setdefault(key, []).append({
                    "time": now.isoformat(), "amount": amount,
                })
                return VelocityCheck(True, entity_type, entity_id,
                                     count + 1, rule["max_count"],
                                     total_amount + amount, rule.get("max_amount", 100000))

        return VelocityCheck(True, entity_type, entity_id, 0, 100, amount, 100000)

    def _parse_window(self, window: str) -> float:
        if window.endswith("h"):
            return float(window[:-1])
        if window.endswith("d"):
            return float(window[:-1]) * 24
        return 1.0


def main():
    print("=" * 60)
    print("  Risk Engine Demo")
    print("=" * 60)

    # Fraud detection
    print("\n--- Transaction Fraud Scoring ---")
    engine = FraudEngine(models=["gradient_boost", "neural_net"])
    txn = Transaction(
        txn_id="TXN-001", amount=2500.00, currency="USD",
        merchant_category="electronics", merchant_country="GB",
        card_token="tok_visa_4242", customer_id="CUST-001",
    )
    result = engine.score_transaction(txn, {"account_age_days": 60, "avg_monthly_spend": 800, "velocity_24h": 3})
    print(f"  Score: {result.risk_score:.3f}, Decision: {result.decision.value}")
    print(f"  Factors: {result.top_factors}")

    # Credit scoring
    print("\n--- Credit Scoring ---")
    credit = CreditScoringEngine()
    cs = credit.score_application(
        {"age": 32, "income": 75000, "existing_debt": 12000,
         "credit_utilization": 0.35, "payment_history_pct": 0.97},
    )
    print(f"  Score: {cs.credit_score}, Grade: {cs.risk_grade.value}")
    print(f"  Limit: ${cs.recommended_limit:,.2f}, Rate: {cs.suggested_rate}%")

    # AML monitoring
    print("\n--- AML Transaction Monitoring ---")
    aml = AMLMonitor(rules=["structuring", "rapid_movement"])
    alerts = aml.monitor_account("ACC-001", [
        {"amount": 9500, "date": "2026-07-01", "type": "cash_deposit"},
        {"amount": 9800, "date": "2026-07-03", "type": "cash_deposit"},
        {"amount": 9900, "date": "2026-07-05", "type": "cash_deposit"},
    ])
    for a in alerts:
        print(f"  ALERT: {a.rule_name} ({a.severity.value}): {a.description}")

    # Velocity controls
    print("\n--- Velocity Controls ---")
    vc = VelocityController([
        {"entity": "card", "window": "1h", "max_count": 5, "max_amount": 10000},
    ])
    for amt in [1500, 2000, 3000, 4000]:
        check = vc.check("card", "tok_visa_4242", amt)
        status = "OK" if check.allowed else f"BLOCKED ({check.reason})"
        print(f"  ${amt}: {status} (count={check.current_count}, total=${check.current_amount:.0f})")


if __name__ == "__main__":
    main()

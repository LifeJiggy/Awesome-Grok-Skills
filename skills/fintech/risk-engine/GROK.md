---
name: "risk-engine"
category: "fintech"
version: "2.0.0"
tags: ["fintech", "risk-engine", "fraud-detection", "credit-scoring", "machine-learning"]
difficulty: "advanced"
estimated_time: "45-60 minutes"
prerequisites: ["python", "machine-learning", "statistics"]
---

# Risk Engine

## Overview

The risk engine provides real-time credit scoring, fraud detection, and risk assessment for financial services. It processes transaction data, customer profiles, and behavioral signals through ML models to make instant authorization decisions while minimizing false positives that degrade customer experience. The system covers both pre-transaction screening (real-time authorization risk) and post-transaction monitoring (batch fraud detection, AML pattern recognition).

## Core Capabilities

- **Real-Time Fraud Detection**: Sub-10ms transaction scoring using gradient boosting and neural network ensemble models with feature stores
- **Credit Scoring**: Application and behavioral credit scoring using alternative data (mobile, e-commerce, social) alongside traditional bureau data
- **Transaction Monitoring**: AML pattern detection including structuring, layering, rapid movement, and geographic anomaly detection
- **Device Fingerprinting**: Browser and device identification for account takeover prevention and device-based risk scoring
- **Velocity Controls**: Configurable rate limiting and velocity rules across accounts, cards, devices, and IP addresses
- **Rule Engine**: Business rule management with versioning, A/B testing, and real-time deployment without code changes
- **Model Serving**: Low-latency model inference with feature computation, model ensembles, and explanation generation
- **Case Management**: Alert triage workflow with case assignment, investigation tools, and SAR filing integration
- **Network Analysis**: Graph-based detection of fraud rings, synthetic identities, and mule account networks
- **Regulatory Compliance**: Automated SAR generation, CTR filing, and OFAC screening integration

## Usage Examples

### Transaction Fraud Scoring

```python
from fintech.risk_engine import FraudEngine, Transaction

engine = FraudEngine(
    models=["gradient_boost", "neural_net"],
    ensemble_method="weighted_average",
    decision_threshold=0.7,
)

# Score a transaction in real-time
result = engine.score_transaction(
    transaction=Transaction(
        txn_id="TXN-001", amount=2500.00, currency="USD",
        merchant_category="electronics", merchant_country="US",
        card_token="tok_visa_4242", customer_id="CUST-001",
        ip_address="192.168.1.1", device_id="DEV-ABC",
    ),
    customer_profile={"account_age_days": 365, "avg_monthly_spend": 800, "velocity_24h": 3},
)

print(f"Risk Score: {result.risk_score:.3f}")
print(f"Decision: {result.decision}")
print(f"Top Factors: {result.top_factors}")
print(f"Latency: {result.latency_ms:.1f}ms")
```

### Credit Scoring

```python
from fintech.risk_engine import CreditScoringEngine

credit = CreditScoringEngine(
    model="xgboost_v3",
    bureau_integration=True,
    alternative_data=True,
)

score = credit.score_application(
    applicant={
        "age": 32, "income": 75000, "employment_years": 5,
        "existing_debt": 12000, "credit_utilization": 0.35,
        "payment_history_pct": 0.97,
    },
    alternative_data={
        "mobile_payment_consistency": 0.85,
        "ecommerce_return_rate": 0.05,
        "social_connections_verified": True,
    },
)

print(f"Credit Score: {score.credit_score}")
print(f"Risk Grade: {score.risk_grade}")
print(f"Recommended Limit: ${score.recommended_limit:,.2f}")
print(f"Interest Rate: {score.suggested_rate:.2f}%")
```

### AML Transaction Monitoring

```python
from fintech.risk_engine import AMLMonitor

aml = AMLMonitor(
    rules=["structuring", "layering", "rapid_movement", "geographic_anomaly"],
    lookback_days=90,
)

alerts = aml.monitor_account(
    account_id="ACC-001",
    transactions=[
        {"amount": 9500, "date": "2026-07-01", "type": "cash_deposit"},
        {"amount": 9800, "date": "2026-07-03", "type": "cash_deposit"},
        {"amount": 9900, "date": "2026-07-05", "type": "cash_deposit"},
    ],
    account_profile={"monthly_avg_balance": 15000, "typical_transaction_size": 500},
)

for alert in alerts:
    print(f"  ALERT: {alert.rule_name} - {alert.description}")
    print(f"  Severity: {alert.severity}, Confidence: {alert.confidence:.1%}")
```

### Velocity Controls

```python
from fintech.risk_engine import VelocityController

controller = VelocityController(
    rules=[
        {"entity": "card", "window": "1h", "max_count": 5, "max_amount": 10000},
        {"entity": "device", "window": "24h", "max_count": 20, "max_amount": 50000},
        {"entity": "ip", "window": "1h", "max_count": 10, "max_amount": 25000},
    ],
)

# Check velocity
check = controller.check(
    entity_type="card",
    entity_id="tok_visa_4242",
    amount=1500,
)

print(f"Allowed: {check.allowed}")
print(f"Count in window: {check.current_count}/{check.limit_count}")
print(f"Amount in window: ${check.current_amount:.2f}/${check.limit_amount:.2f}")
```

## Architecture

```
Transaction Stream
         │
         ▼
┌─────────────────────┐
│  Feature Store       │──→ Real-time + batch features
│  (Redis + Feature)   │
└────────┬────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│ Rule   │ │ ML     │──→ Ensemble scoring
│ Engine │ │ Models │
└────┬───┘ └────┬───┘
     │          │
     ▼          ▼
┌─────────────────────┐
│  Decision Engine     │──→ Approve / Review / Decline
│  (Explainability)    │
└────────┬────────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌────────┐ ┌────────┐
│ Case   │ │ AML    │──→ SAR / CTR filing
│ Mgmt   │ │ Monitor│
└────────┘ └────────┘
```

## Best Practices

- Target <10ms P99 latency for real-time transaction scoring; pre-compute features where possible
- Use ensemble models (gradient boost + neural net) for better recall than single models
- Implement model monitoring with automatic retraining triggers when performance degrades below baseline
- Build explainability into every decision—regulators require reason codes for adverse actions
- Tune the review threshold to balance fraud loss reduction against customer friction (aim for <1% false positive rate)
- Maintain separate models for different transaction types (card-present, card-not-present, P2P, wire)
- Use graph analysis to detect fraud rings that single-transaction scoring misses
- Implement feedback loops where analyst decisions on alerts feed back into model training data
- Version all rules and model artifacts for audit trail and rollback capability
- Test model performance against adversarial scenarios (synthetic identities, account takeover patterns)

## Related Modules

- `fintech/payment-systems` - Payment processing feeds into fraud screening
- `fintech/digital-banking` - Account data for customer profiling
- `fintech/compliance-automation` - AML/SAR regulatory compliance

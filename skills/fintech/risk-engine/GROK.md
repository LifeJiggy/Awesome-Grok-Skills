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

## Advanced Configuration

### Model Configuration

```yaml
models:
  fraud_detection:
    primary:
      type: "gradient_boost"
      model_path: "/models/fraud_gb_v3.pkl"
      features:
        - transaction_amount
        - merchant_category
        - time_of_day
        - device_type
        - location_distance
        - velocity_24h
        - account_age_days
        - historical_fraud_rate
      threshold: 0.7
      latency_target_ms: 10
      
    secondary:
      type: "neural_net"
      model_path: "/models/fraud_nn_v2.pt"
      features:
        - transaction_embedding
        - merchant_embedding
        - temporal_features
        - behavioral_features
      threshold: 0.65
      latency_target_ms: 20
      
    ensemble:
      method: "weighted_average"
      weights:
        primary: 0.6
        secondary: 0.4
      final_threshold: 0.72
      
  credit_scoring:
    model_type: "xgboost"
    model_path: "/models/credit_xgb_v4.json"
    features:
      - credit_score
      - income
      - debt_to_income
      - payment_history
      - credit_utilization
      - account_age
      - employment_years
      - alternative_data_features
    score_range:
      min: 300
      max: 850
    grade_thresholds:
      A: 750
      B: 700
      C: 650
      D: 600
      F: 0
```

### Feature Store Configuration

```yaml
feature_store:
  realtime:
    redis:
      host: "redis-feature-store.internal"
      port: 6379
      db: 0
      key_prefix: "features:"
      ttl_seconds: 3600
      
    features:
      - name: "velocity_1h"
        computation: "count(txn WHERE entity_id = ? AND timestamp > now() - 1h)"
        refresh_seconds: 60
        
      - name: "velocity_24h"
        computation: "count(txn WHERE entity_id = ? AND timestamp > now() - 24h)"
        refresh_seconds: 300
        
      - name: "avg_transaction_30d"
        computation: "avg(amount WHERE entity_id = ? AND timestamp > now() - 30d)"
        refresh_seconds: 3600
        
  batch:
    spark:
      master: "spark://spark-master.internal:7077"
      job_schedule: "0 2 * * *"  # Daily at 2 AM
      
    features:
      - name: "credit_score"
        source: "credit_bureau_api"
        refresh_days: 30
        
      - name: "income_estimate"
        source: "plaid_income"
        refresh_days: 90
        
      - name: "device_trust_score"
        source: "device_fingerprint_db"
        refresh_days: 7
```

### Rule Engine Configuration

```yaml
rule_engine:
  versioning:
    enabled: true
    max_versions: 50
    auto_rollback_on_error: true
    
  ab_testing:
    enabled: true
    traffic_split:
      control: 0.9
      treatment: 0.1
    min_sample_size: 10000
    significance_level: 0.05
    
  hot_deployment:
    enabled: true
    max_rules_per_deployment: 10
    rollback_window_minutes: 30
    
  rules:
    - id: "velocity_card_1h"
      name: "Card Velocity 1 Hour"
      condition: "velocity_card_1h > 5"
      action: "review"
      priority: 1
      enabled: true
      
    - id: "amount_high_value"
      name: "High Value Transaction"
      condition: "amount > 10000 AND merchant_category = 'cash_advance'"
      action: "decline"
      priority: 2
      enabled: true
      
    - id: "geo_impossible_travel"
      name: "Impossible Travel"
      condition: "distance_last_txn > 500km AND time_since_last_txn < 2h"
      action: "review"
      priority: 3
      enabled: true
```

## Architecture Patterns

### Real-Time Feature Computation

```python
class RealTimeFeatureComputer:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def compute_features(self, transaction: Transaction) -> Dict:
        features = {}
        
        # Velocity features
        features['velocity_1h'] = await self.get_velocity(
            transaction.entity_id, '1h'
        )
        features['velocity_24h'] = await self.get_velocity(
            transaction.entity_id, '24h'
        )
        
        # Amount features
        features['avg_amount_30d'] = await self.get_avg_amount(
            transaction.entity_id, '30d'
        )
        features['amount_ratio'] = (
            transaction.amount / features['avg_amount_30d']
            if features['avg_amount_30d'] > 0 else 0
        )
        
        # Time features
        features['hour_of_day'] = transaction.timestamp.hour
        features['day_of_week'] = transaction.timestamp.weekday()
        
        # Location features
        features['distance_last_txn'] = await self.calculate_distance(
            transaction.entity_id,
            transaction.latitude,
            transaction.longitude,
        )
        
        return features
    
    async def get_velocity(self, entity_id: str, window: str) -> int:
        key = f"velocity:{entity_id}:{window}"
        count = await self.redis.incr(key)
        if count == 1:
            await self.redis.expire(key, self.window_to_seconds(window))
        return count
```

### Ensemble Scoring Pattern

```python
class EnsembleScorer:
    def __init__(self, models: List[Model], weights: Dict[str, float]):
        self.models = models
        self.weights = weights
    
    async def score(self, features: Dict) -> ScoreResult:
        scores = {}
        
        # Get predictions from each model
        for model in self.models:
            score = await model.predict(features)
            scores[model.name] = score
        
        # Weighted average
        weighted_score = sum(
            scores[name] * self.weights[name]
            for name in scores
        ) / sum(self.weights.values())
        
        # Get feature importance from each model
        importance = self.aggregate_importance(scores, features)
        
        return ScoreResult(
            score=weighted_score,
            model_scores=scores,
            feature_importance=importance,
            confidence=self.calculate_confidence(scores),
        )
```

### Decision Engine Pattern

```python
class DecisionEngine:
    def __init__(self, rules: List[Rule], ml_scorer: EnsembleScorer):
        self.rules = rules
        self.ml_scorer = ml_scorer
    
    async def decide(self, transaction: Transaction) -> Decision:
        # Compute features
        features = await self.feature_store.compute(transaction)
        
        # Run ML scoring
        ml_result = await self.ml_scorer.score(features)
        
        # Apply rules
        rule_results = self.evaluate_rules(transaction, features)
        
        # Combine decisions
        final_decision = self.combine_decisions(ml_result, rule_results)
        
        # Generate explanation
        explanation = self.generate_explanation(
            ml_result, rule_results, final_decision
        )
        
        return Decision(
            action=final_decision.action,
            risk_score=ml_result.score,
            explanation=explanation,
            metadata={
                'ml_result': ml_result,
                'rule_results': rule_results,
            },
        )
```

### Case Management Pattern

```python
class CaseManager:
    def __init__(self, db, notification_service):
        self.db = db
        self.notifier = notification_service
    
    async def create_case(self, alert: Alert) -> Case:
        case = Case(
            id=str(uuid.uuid4()),
            alert_id=alert.id,
            priority=self.calculate_priority(alert),
            status='open',
            created_at=datetime.utcnow(),
        )
        
        await self.db.cases.insert(case)
        await self.notifier.notify(case)
        
        return case
    
    async def assign_case(self, case_id: str, analyst_id: str):
        await self.db.cases.update(
            case_id,
            {'analyst_id': analyst_id, 'status': 'in_progress'}
        )
    
    async def close_case(self, case_id: str, resolution: str):
        await self.db.cases.update(
            case_id,
            {
                'status': 'closed',
                'resolution': resolution,
                'closed_at': datetime.utcnow(),
            }
        )
```

## Integration Guide

### Payment System Integration

```python
class PaymentFraudIntegration:
    def __init__(self, fraud_engine: FraudEngine):
        self.fraud_engine = fraud_engine
    
    async def screen_payment(self, payment: Payment) -> FraudScreeningResult:
        # Extract features from payment
        features = await self.extract_features(payment)
        
        # Run fraud scoring
        result = await self.fraud_engine.score(features)
        
        # Apply business logic
        if result.risk_score > 0.9:
            return FraudScreeningResult(
                decision='decline',
                reason='High risk score',
                risk_score=result.risk_score,
            )
        elif result.risk_score > 0.7:
            return FraudScreeningResult(
                decision='review',
                reason='Elevated risk',
                risk_score=result.risk_score,
            )
        else:
            return FraudScreeningResult(
                decision='approve',
                risk_score=result.risk_score,
            )
```

### Credit Bureau Integration

```python
class CreditBureauIntegration:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.creditbureau.com/v1"
    
    async def get_credit_report(self, ssn: str) -> CreditReport:
        response = await httpx.get(
            f"{self.base_url}/credit-report",
            headers={"Authorization": f"Bearer {self.api_key}"},
            params={"ssn": ssn},
        )
        
        data = response.json()
        
        return CreditReport(
            credit_score=data['credit_score'],
            payment_history=data['payment_history'],
            credit_utilization=data['credit_utilization'],
            derogatory_marks=data['derogatory_marks'],
            account_age=data['account_age'],
            total_accounts=data['total_accounts'],
            hard_inquiries=data['hard_inquiries'],
        )
```

### AML Screening Integration

```python
class AMLScreeningIntegration:
    def __init__(self, screening_service):
        self.screening_service = screening_service
    
    async def screen_transaction(self, transaction: Transaction) -> AMLResult:
        # Screen against sanctions lists
        sanctions_result = await self.screening_service.screen_sanctions(
            name=transaction.customer_name,
            country=transaction.customer_country,
        )
        
        # Screen for PEP (Politically Exposed Person)
        pep_result = await self.screening_service.screen_pep(
            name=transaction.customer_name,
        )
        
        # Check transaction patterns
        pattern_result = await self.check_patterns(transaction)
        
        return AMLResult(
            sanctions_match=sanctions_result.match,
            pep_match=pep_result.match,
            pattern_flags=pattern_result.flags,
            risk_score=self.calculate_aml_risk(
                sanctions_result, pep_result, pattern_result
            ),
        )
```

## Performance Optimization

### Feature Store Optimization

```python
class FeatureStoreOptimizer:
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def batch_compute_features(
        self, transactions: List[Transaction]
    ) -> List[Dict]:
        # Group transactions by entity
        grouped = defaultdict(list)
        for txn in transactions:
            grouped[txn.entity_id].append(txn)
        
        # Batch fetch features
        feature_keys = []
        for entity_id in grouped.keys():
            feature_keys.extend([
                f"velocity:{entity_id}:1h",
                f"velocity:{entity_id}:24h",
                f"avg_amount:{entity_id}:30d",
            ])
        
        # Pipeline redis operations
        pipe = self.redis.pipeline()
        for key in feature_keys:
            pipe.get(key)
        results = await pipe.execute()
        
        # Map results back to transactions
        features = {}
        for i, entity_id in enumerate(grouped.keys()):
            features[entity_id] = {
                'velocity_1h': int(results[i*3] or 0),
                'velocity_24h': int(results[i*3+1] or 0),
                'avg_amount_30d': float(results[i*3+2] or 0),
            }
        
        return features
```

### Model Inference Optimization

```python
class ModelInferenceOptimizer:
    def __init__(self, model):
        self.model = model
        self.batch_size = 32
    
    async def predict_batch(self, features_batch: List[Dict]) -> List[float]:
        # Convert to tensor
        tensor = self.features_to_tensor(features_batch)
        
        # Batch prediction
        predictions = self.model.predict(tensor)
        
        return predictions.tolist()
    
    def features_to_tensor(self, features: List[Dict]) -> torch.Tensor:
        # Vectorize features
        vectors = []
        for feat in features:
            vector = [feat.get(f, 0) for f in self.feature_names]
            vectors.append(vector)
        
        return torch.tensor(vectors, dtype=torch.float32)
```

### Caching Strategy

```python
class FraudCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 300  # 5 minutes
    
    async def get_cached_score(self, entity_id: str) -> Optional[float]:
        cache_key = f"score:{entity_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            return float(cached)
        return None
    
    async def cache_score(self, entity_id: str, score: float):
        cache_key = f"score:{entity_id}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            str(score)
        )
```

## Security Considerations

### Data Encryption

```python
from cryptography.fernet import Fernet

class DataEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data like SSN, account numbers"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted: str) -> str:
        """Decrypt sensitive data"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class FraudAccessControl:
    def __init__(self):
        self.permissions = {}
    
    def check_permission(self, user_id: str, action: str) -> bool:
        user_permissions = self.permissions.get(user_id, [])
        return action in user_permissions
    
    def grant_permission(self, user_id: str, action: str):
        if user_id not in self.permissions:
            self.permissions[user_id] = []
        self.permissions[user_id].append(action)
```

### Audit Logging

```python
class AuditLogger:
    def __init__(self, db):
        self.db = db
    
    async def log_event(self, event: AuditEvent):
        audit_entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow(),
            'actor': event.actor,
            'action': event.action,
            'resource': event.resource,
            'details': event.details,
            'ip_address': event.ip_address,
        }
        
        await self.db.audit_logs.insert(audit_entry)
```

## Troubleshooting Guide

### Common Issues

**Issue: High false positive rate**
```python
async def diagnose_false_positives(date_range: Tuple[date, date]):
    # Get alerts in date range
    alerts = await get_alerts(date_range)
    
    # Filter for false positives
    false_positives = [a for a in alerts if a.resolution == 'false_positive']
    
    # Analyze by rule
    by_rule = defaultdict(list)
    for alert in false_positives:
        by_rule[alert.rule_name].append(alert)
    
    for rule_name, rule_alerts in by_rule.items():
        print(f"Rule: {rule_name}")
        print(f"  False positives: {len(rule_alerts)}")
        print(f"  Avg risk score: {sum(a.risk_score for a in rule_alerts) / len(rule_alerts):.2f}")
        print(f"  Recommendation: Adjust threshold or review rule logic")
```

**Issue: Model performance degradation**
```python
async def monitor_model_performance(model_name: str):
    # Get recent predictions
    predictions = await get_recent_predictions(model_name, days=7)
    
    # Calculate metrics
    accuracy = calculate_accuracy(predictions)
    precision = calculate_precision(predictions)
    recall = calculate_recall(predictions)
    f1 = calculate_f1(predictions)
    
    print(f"Model: {model_name}")
    print(f"  Accuracy: {accuracy:.2%}")
    print(f"  Precision: {precision:.2%}")
    print(f"  Recall: {recall:.2%}")
    print(f"  F1 Score: {f1:.2%}")
    
    if accuracy < 0.9:
        print(f"  WARNING: Model performance degraded")
        print(f"  Recommendation: Retrain model")
```

**Issue: Latency spikes**
```python
async def diagnose_latency(txn_id: str):
    trace = await get_transaction_trace(txn_id)
    
    print(f"Transaction {txn_id}:")
    print(f"  Total latency: {trace.total_latency_ms}ms")
    print(f"  Breakdown:")
    for step in trace.steps:
        print(f"    {step.name}: {step.latency_ms}ms")
        if step.latency_ms > 10:
            print(f"      WARNING: Step exceeds 10ms threshold")
            print(f"      Details: {step.details}")
```

## API Reference

### Fraud Scoring API

```python
# Score a transaction
POST /api/v1/fraud/score
Request:
{
    "transaction_id": "TXN-001",
    "amount": 2500.00,
    "currency": "USD",
    "merchant_category": "electronics",
    "customer_id": "CUST-001",
    "device_id": "DEV-ABC",
    "ip_address": "192.168.1.1"
}

Response:
{
    "risk_score": 0.75,
    "decision": "review",
    "top_factors": [
        {"feature": "velocity_24h", "importance": 0.35},
        {"feature": "amount_ratio", "importance": 0.28}
    ],
    "latency_ms": 8.5
}
```

### Credit Scoring API

```python
# Score a credit application
POST /api/v1/credit/score
Request:
{
    "applicant_id": "APP-001",
    "income": 75000,
    "existing_debt": 12000,
    "credit_score": 720,
    "employment_years": 5
}

Response:
{
    "credit_score": 725,
    "risk_grade": "B",
    "recommended_limit": 25000,
    "suggested_rate": 8.5,
    "factors": [
        {"factor": "income", "impact": "positive"},
        {"factor": "debt_to_income", "impact": "negative"}
    ]
}
```

### AML Monitoring API

```python
# Monitor account for AML patterns
POST /api/v1/aml/monitor
Request:
{
    "account_id": "ACC-001",
    "transactions": [
        {"amount": 9500, "date": "2026-07-01", "type": "cash_deposit"},
        {"amount": 9800, "date": "2026-07-03", "type": "cash_deposit"}
    ]
}

Response:
{
    "alerts": [
        {
            "rule_name": "structuring",
            "severity": "high",
            "confidence": 0.85,
            "description": "Multiple cash deposits just below reporting threshold"
        }
    ],
    "risk_score": 0.82
}
```

## Data Models

### Transaction Model

```python
class Transaction:
    transaction_id: str
    amount: Decimal
    currency: str
    merchant_category: str
    merchant_country: str
    customer_id: str
    card_token: Optional[str]
    device_id: Optional[str]
    ip_address: Optional[str]
    timestamp: datetime
    latitude: Optional[float]
    longitude: Optional[float]
```

### Fraud Alert Model

```python
class FraudAlert:
    alert_id: str
    transaction_id: str
    customer_id: str
    risk_score: float
    decision: str  # approve, review, decline
    rule_name: Optional[str]
    model_version: str
    top_factors: List[Dict]
    created_at: datetime
    status: str  # open, investigating, resolved
    resolution: Optional[str]
    analyst_id: Optional[str]
```

### Credit Score Model

```python
class CreditScore:
    applicant_id: str
    credit_score: int
    risk_grade: str
    recommended_limit: Decimal
    suggested_rate: float
    factors: List[CreditFactor]
    bureau_data: Optional[BureauData]
    alternative_data: Optional[AlternativeData]
    calculated_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: risk-engine
  namespace: risk-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: risk-engine
  template:
    metadata:
      labels:
        app: risk-engine
    spec:
      containers:
      - name: risk-engine
        image: your-registry/risk-engine:2.0.0
        ports:
        - containerPort: 8443
        resources:
          requests:
            memory: "1Gi"
            cpu: "1000m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8443
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8443
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Model Deployment

```bash
# Deploy new model version
python scripts/deploy_model.py \
  --model-path /models/fraud_gb_v3.pkl \
  --model-name fraud_detection \
  --version 3.0.0 \
  --threshold 0.7

# Rollback model
python scripts/rollback_model.py \
  --model-name fraud_detection \
  --version 2.0.0
```

## Monitoring & Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Fraud scoring metrics
fraud_score_counter = Counter(
    'fraud_scores_total',
    'Total fraud scores',
    ['decision', 'model']
)

fraud_score_latency = Histogram(
    'fraud_score_latency_seconds',
    'Fraud scoring latency',
    ['model'],
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5]
)

# Model performance metrics
model_accuracy = Gauge(
    'model_accuracy',
    'Model accuracy',
    ['model_name']
)

# AML metrics
aml_alerts_counter = Counter(
    'aml_alerts_total',
    'Total AML alerts',
    ['rule', 'severity']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Risk Engine",
    "panels": [
      {
        "title": "Fraud Scoring Latency",
        "type": "heatmap",
        "targets": [
          {
            "expr": "histogram_quantile(0.95, rate(fraud_score_latency_seconds_bucket[5m]))",
            "legendFormat": "P95 - {{model}}"
          }
        ]
      },
      {
        "title": "Decision Distribution",
        "type": "pie",
        "targets": [
          {
            "expr": "rate(fraud_scores_total[5m])",
            "legendFormat": "{{decision}}"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

```yaml
groups:
- name: risk_engine_alerts
  rules:
  - alert: HighFraudScoreLatency
    expr: histogram_quantile(0.95, rate(fraud_score_latency_seconds_bucket[5m])) > 0.01
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Fraud scoring latency exceeds 10ms"
      
  - alert: ModelAccuracyDegraded
    expr: model_accuracy < 0.9
    for: 1h
    labels:
      severity: critical
    annotations:
      summary: "Model accuracy below 90%"
```

## Testing Strategy

### Unit Tests

```python
import pytest
from decimal import Decimal

class TestFraudScoring:
    def test_score_transaction(self, fraud_engine):
        result = fraud_engine.score_transaction(
            transaction=Transaction(
                txn_id="TXN-001",
                amount=100.00,
                currency="USD",
                merchant_category="grocery",
                merchant_country="US",
                customer_id="CUST-001",
            ),
            customer_profile={"account_age_days": 365},
        )
        assert result.risk_score >= 0
        assert result.risk_score <= 1
        assert result.decision in ['approve', 'review', 'decline']
    
    def test_high_risk_transaction(self, fraud_engine):
        result = fraud_engine.score_transaction(
            transaction=Transaction(
                txn_id="TXN-002",
                amount=10000.00,
                currency="USD",
                merchant_category="cash_advance",
                merchant_country="RU",
                customer_id="CUST-001",
            ),
            customer_profile={"account_age_days": 30},
        )
        assert result.risk_score > 0.7
        assert result.decision in ['review', 'decline']
```

### Integration Tests

```python
class TestEndToEndRiskScoring:
    async def test_payment_screening(self, risk_engine, payment_gateway):
        # Create payment
        payment = await payment_gateway.create_payment(
            amount=Decimal("500.00"),
            currency="USD",
            merchant_id="MERCHANT-001",
        )
        
        # Screen payment
        result = await risk_engine.screen_payment(payment)
        
        assert result.decision in ['approve', 'review', 'decline']
        assert result.risk_score >= 0
        assert result.risk_score <= 1
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class RiskEngineUser(HttpUser):
    wait_time = between(0.1, 0.5)
    
    @task(10)
    def score_transaction(self):
        self.client.post("/api/v1/fraud/score", json={
            "transaction_id": f"TXN-{self.transaction_counter}",
            "amount": 100.00,
            "currency": "USD",
            "merchant_category": "grocery",
            "customer_id": "CUST-001",
        })
        self.transaction_counter += 1
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/fraud/score", methods=["POST"])
@app.route("/api/v2/fraud/score", methods=["POST"])
async def score_transaction():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await score_transaction_v2()
    return await score_transaction_v1()
```

### Model Versioning

```python
class ModelVersionManager:
    def __init__(self, model_registry):
        self.registry = model_registry
    
    async def deploy_model(
        self,
        model_name: str,
        model_path: str,
        version: str,
        threshold: float,
    ):
        # Register model
        model_id = await self.registry.register(
            name=model_name,
            path=model_path,
            version=version,
            threshold=threshold,
        )
        
        # Update routing
        await self.update_routing(model_name, model_id)
        
        # Monitor performance
        await self.setup_monitoring(model_id)
```

## Glossary

- **AML**: Anti-Money Laundering - regulations to prevent money laundering
- **CTR**: Currency Transaction Report - report for transactions over $10,000
- **Feature Store**: Centralized repository for ML features
- **False Positive Rate**: Percentage of legitimate transactions flagged as fraud
- **Gradient Boosting**: Ensemble ML method for classification/regression
- **Neural Network**: Deep learning model for complex pattern recognition
- **PEP**: Politically Exposed Person - individual with public political function
- **SAR**: Suspicious Activity Report - report for suspicious transactions
- **Velocity**: Rate of transactions over a time period
- **XGBoost**: Optimized gradient boosting library

## Changelog

### Version 2.0.0 (2026-07-01)
- Added ensemble scoring with neural networks
- Implemented real-time feature store
- Enhanced AML monitoring with pattern detection
- Added graph-based fraud ring detection

### Version 1.5.0 (2026-01-15)
- Added credit scoring engine
- Implemented velocity controls
- Enhanced rule engine with A/B testing

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic fraud detection
- Rule engine

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def score_transaction(
    transaction: Transaction,
    customer_profile: Dict,
) -> ScoreResult:
    """Score a transaction for fraud risk.
    
    Args:
        transaction: Transaction to score.
        customer_profile: Customer profile data.
    
    Returns:
        Scoring result with risk score and decision.
    
    Raises:
        ScoringError: If scoring fails.
    """
    pass
```

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Request review from team lead
6. Address review comments
7. Merge after approval

## License

MIT License

Copyright (c) 2026 Risk Engine Platform

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

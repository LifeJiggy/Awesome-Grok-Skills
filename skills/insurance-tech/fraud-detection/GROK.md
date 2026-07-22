---
name: "fraud-detection"
category: "insurance-tech"
version: "2.0.0"
tags: ["insurance", "fraud", "detection", "prevention", "analytics"]
description: "Insurance fraud detection, prevention, and investigation support"
---

# Fraud Detection

## Overview

The Fraud Detection module provides advanced analytics and rule-based systems for identifying potentially fraudulent insurance claims and policy applications. It combines statistical analysis, pattern recognition, network analysis, and machine learning models to detect suspicious activities across the insurance lifecycle. The module supports real-time scoring at FNOL, post-payment analytics, and investigation workflow management.

## Core Capabilities

- **Real-Time Fraud Scoring**: Score claims and applications at submission
- **Rule-Based Detection**: Configurable business rules for fraud identification
- **Predictive Models**: ML-based fraud prediction using historical patterns
- **Network Analysis**: Identify organized fraud rings through relationship mapping
- **Provider Analytics**: Detect healthcare and repair provider fraud patterns
- **Social Media Intelligence**: Analyze social media for fraud indicators
- **Investigation Management**: Workflow for fraud investigation and case management
- **SIU Integration**: Special Investigation Unit case management and reporting

## Usage Examples

### Claim Fraud Scoring

```python
from fraud_detection import FraudEngine, ClaimScoreRequest

engine = FraudEngine(model_version="v3.0")

# Score a claim
score_request = ClaimScoreRequest(
    claim_number="CLM-2024-0001",
    policy_number="AUTO-2024-001234",
    claim_type="auto_collision",
    reported_amount=15000.00,
    loss_date="2024-01-15",
    claimant_name="John Smith",
    loss_description="Vehicle collision at intersection",
)

score = engine.score_claim(score_request)
print(f"Fraud Score: {score.risk_score}")
print(f"Risk Level: {score.risk_level}")
print(f"Confidence: {score.confidence:.1%}")
print(f"Red Flags: {score.red_flags}")
print(f"Recommendation: {score.recommendation}")
```

### Rule Configuration

```python
from fraud_detection import RuleEngine, FraudRule, RuleCondition

rule_engine = RuleEngine()

# Add detection rules
rule_engine.add_rule(FraudRule(
    name="high_amount_first_claim",
    description="First claim with high amount",
    conditions=[
        RuleCondition(field="claim_count", operator="equals", value=0),
        RuleCondition(field="reported_amount", operator="greater_than", value=10000),
    ],
    score_weight=30,
    enabled=True,
))

rule_engine.add_rule(FraudRule(
    name="recent_policy_inception",
    description="Claim filed shortly after policy inception",
    conditions=[
        RuleCondition(field="policy_age_days", operator="less_than", value=30),
        RuleCondition(field="reported_amount", operator="greater_than", value=5000),
    ],
    score_weight=25,
    enabled=True,
))
```

### Provider Fraud Analytics

```python
from fraud_detection import ProviderAnalyzer, ServiceProvider

analyzer = ProviderAnalyzer()

# Analyze provider patterns
provider = ServiceProvider(
    provider_id="PROV-001",
    provider_type="auto_repair",
    name="Quick Fix Auto Body",
    location="Miami, FL",
    claim_count=150,
    total_billed=2500000,
)

analysis = analyzer.analyze_provider(provider)
print(f"Provider Analysis:")
print(f"  Provider: {analysis.provider_name}")
print(f"  Anomaly Score: {analysis.anomaly_score:.2f}")
print(f"  Red Flags: {analysis.red_flags}")
print(f"  Referral Recommended: {analysis.referral_recommended}")
```

### Investigation Case Management

```python
from fraud_detection import InvestigationCase, CaseManager

case_manager = CaseManager()

# Create investigation case
case = InvestigationCase(
    claim_number="CLM-2024-0001",
    fraud_score=0.85,
    red_flags=["high_amount", "recent_inception", "inconsistent_statements"],
    assigned_investigator="siu-001",
    priority="high",
)

case_id = case_manager.create_case(case)
print(f"Investigation Case: {case_id}")

# Update case status
case_manager.update_status(case_id, status="in_progress", notes="Requesting additional documentation")

# Add case notes
case_manager.add_note(case_id, "Claimant provided inconsistent statements about loss circumstances")
```

## Best Practices

- **Multi-Layer Detection**: Combine rules, ML models, and human analysis
- **Continuous Learning**: Update models with new fraud patterns and outcomes
- **Privacy Compliance**: Ensure fraud detection complies with privacy regulations
- **False Positive Management**: Minimize false positives to avoid customer friction
- **SIU Collaboration**: Support Special Investigation Unit workflows
- **Data Quality**: Maintain high data quality for accurate fraud detection
- **Regulatory Reporting**: Comply with fraud reporting requirements
- **Cross-Channel Analysis**: Analyze fraud across all claim submission channels

## Related Modules

- **claims-processing**: Claims data for fraud analysis
- **risk-assessment**: Risk factors in fraud detection
- **policy-management**: Policy data for fraud analysis

---

## Advanced Configuration

### ML Model Configuration

```python
ml_config = {
    "model_type": "gradient_boosting",
    "features": [
        "claim_amount", "policy_age", "claim_count",
        "report_delay", "injury_severity", "vehicle_age",
    ],
    "training_data_years": 5,
    "retrain_interval_months": 6,
    "threshold_adjustments": {
        "auto": 0.65,
        "property": 0.70,
        "health": 0.60,
    },
}
```

### Network Analysis Configuration

```python
network_config = {
    "relationship_types": [
        "shared_address", "shared_phone", "shared_bank_account",
        "shared_provider", "shared_attorney", "family_relation",
    ],
    "min_ring_size": 3,
    "max_connection_depth": 4,
    "graph_database": "neo4j",
    "clustering_algorithm": "louvain",
}
```

### Scoring Thresholds

```python
scoring_thresholds = {
    "auto_adjudicate": 0.3,      # Below this: auto-approve
    "manual_review": 0.6,         # Below this: manual review
    "escalate_to_siu": 0.8,      # Above this: SIU investigation
    "immediate_hold": 0.95,      # Above this: immediate hold
}
```

### Alert Configuration

```python
alert_config = {
    "channels": {
        "email": {"enabled": True, "recipients": ["siu@company.com"]},
        "slack": {"enabled": True, "channel": "#fraud-alerts"},
        "sms": {"enabled": False},
    },
    "severity_levels": {
        "critical": {"threshold": 0.9, "response_time": "1h"},
        "high": {"threshold": 0.8, "response_time": "4h"},
        "medium": {"threshold": 0.6, "response_time": "24h"},
    },
}
```

### External Data Sources

```python
external_sources = {
    "nicb": {"api_key": "xxx", "enabled": True},  # National Insurance Crime Bureau
    "clue": {"api_key": "xxx", "enabled": True},   # Comprehensive Loss Underwriting Exchange
    "iso": {"api_key": "xxx", "enabled": True},    # Insurance Services Office
    "lexis_nexis": {"api_key": "xxx", "enabled": True},
}
```

## Architecture Patterns

### Real-Time Scoring Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  FNOL       │────▶│  Feature     │────▶│  ML Model   │
│  Submission │     │  Engineering │     │  Inference  │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Score  │           │  Rules    │         │  Network  │
                    │  Engine │           │  Engine   │         │  Analysis │
                    └─────────┘           └───────────┘         └───────────┘
```

### Batch Analytics Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Claims     │────▶│  ETL         │────▶│  Data Lake  │
│  Database   │     │  Pipeline    │     │  (S3/GCS)   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Model  │           │  Report   │         │  Trend    │
                    │  Training│          │  Generator│         │  Analysis │
                    └─────────┘           └───────────┘         └───────────┘
```

### Investigation Workflow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Fraud      │────▶│  SIU         │────▶│  Case       │
│  Alert      │     │  Assignment  │     │  Creation   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                    ┌────────────────────────────┼────────────────────────────┐
                    │                            │                            │
               ┌────┴────┐                ┌─────┴─────┐                ┌─────┴─────┐
               │Evidence │                │  Witness  │                │  Legal    │
               │Collection│               │  Interviews│               │  Review   │
               └─────────┘                └───────────┘                └───────────┘
```

## Integration Guide

### Claims System Integration

```python
def integrate_with_claims_system(claim_data):
    # Receive FNOL data
    fnol = receive_fnol(claim_data)

    # Run fraud scoring
    fraud_result = fraud_engine.score(fnol)

    # If high fraud risk, create investigation case
    if fraud_result.risk_score > 0.8:
        create_investigation_case(fnol, fraud_result)

    # Return scoring to claims system
    return {
        "claim_number": fnol.claim_number,
        "fraud_score": fraud_result.risk_score,
        "recommendation": fraud_result.recommendation,
    }
```

### SIU Case Management Integration

```python
class SIUIntegration:
    def create_case(self, fraud_alert):
        case = {
            "case_number": generate_case_number(),
            "claim_number": fraud_alert.claim_number,
            "fraud_score": fraud_alert.risk_score,
            "red_flags": fraud_alert.red_flags,
            "priority": self.calculate_priority(fraud_alert),
            "assigned_to": self.auto_assign(fraud_alert),
        }
        return siu_api.create_case(case)
```

### Payment System Integration

```python
def payment_hold_check(claim_number):
    fraud_status = get_fraud_status(claim_number)
    if fraud_status.risk_score > 0.8:
        payment_system.hold_payment(claim_number)
        return {"status": "held", "reason": "fraud_review"}
    return {"status": "approved", "reason": "cleared"}
```

### Data Warehouse Integration

```python
def export_to_warehouse(fraud_results):
    for result in fraud_results:
        warehouse.insert("fraud_scores", {
            "claim_number": result.claim_number,
            "score": result.risk_score,
            "flags": result.red_flags,
            "timestamp": datetime.utcnow(),
        })
```

## Performance Optimization

### Model Inference Optimization

```python
optimization_config = {
    "model_format": "onnx",
    "batch_size": 100,
    "parallel_workers": 4,
    "cache_model": True,
    "lazy_loading": True,
}
```

### Feature Store Optimization

```python
feature_store_config = {
    "cache_ttl": 300,
    "precompute_features": True,
    "feature_freshness": "5m",
    "batch_feature_computation": True,
}
```

### Database Query Optimization

```python
db_optimization = {
    "indexing": ["claim_number", "policy_number", "loss_date"],
    "partitioning": "by_year",
    "connection_pool_size": 20,
    "query_timeout": 30,
}
```

### API Response Optimization

```python
api_config = {
    "response_timeout": 5,
    "retry_count": 3,
    "circuit_breaker": True,
    "rate_limiting": 1000,  # requests per minute
}
```

## Security Considerations

### Data Protection

```python
security_config = {
    "encryption_at_rest": True,
    "encryption_in_transit": True,
    "pii_masking": True,
    "data_masking_fields": ["ssn", "date_of_birth", "bank_account"],
    "access_logging": True,
}
```

### Access Control

```python
access_control = {
    "rbac_enabled": True,
    "roles": {
        "fraud_analyst": ["read_scores", "investigate_cases"],
        "siu_investigator": ["read_scores", "manage_cases", "export_data"],
        "admin": ["configure_rules", "manage_users", "view_audit_logs"],
    },
    "mfa_required": True,
}
```

### Audit Logging

```python
audit_config = {
    "enabled": True,
    "log_level": "INFO",
    "retention_days": 2555,  # 7 years for insurance compliance
    "events": [
        "score_calculated", "case_created", "case_updated",
        "rule_modified", "user_login", "data_export",
    ],
}
```

### Fraud Data Privacy

```python
privacy_config = {
    "data_retention_years": 7,
    "anonymization_enabled": True,
    "right_to_erasure": False,  # Insurance exception
    "cross_border_transfer": False,
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| High false positive rate | Threshold too low | Adjust scoring thresholds |
| Model drift detected | Data distribution change | Retrain model with recent data |
| API timeout | Large feature computation | Optimize feature computation |
| Duplicate scoring | Idempotency issue | Add claim number dedup |
| Missing features | Data pipeline failure | Check feature store connectivity |
| Alert fatigue | Too many alerts | Adjust severity thresholds |

### Debug Commands

```bash
# Check model version
python -m fraud_detection show_model --version

# Test scoring endpoint
curl -X POST http://localhost:8080/score -d '{"claim_number": "TEST-001"}'

# Check feature store
python -m fraud_detection check_features --claim-number TEST-001

# Review audit logs
grep "TEST-001" /var/log/fraud-detection/audit.log
```

### Model Performance Issues

```python
def diagnose_model_performance(model, test_data):
    predictions = model.predict(test_data)
    metrics = {
        "accuracy": calculate_accuracy(predictions, test_data.labels),
        "precision": calculate_precision(predictions, test_data.labels),
        "recall": calculate_recall(predictions, test_data.labels),
        "f1_score": calculate_f1(predictions, test_data.labels),
    }
    return metrics
```

## API Reference

### FraudEngine

```python
class FraudEngine:
    def __init__(self, model_version: str):
        """Initialize fraud engine."""

    def score_claim(self, request: ClaimScoreRequest) -> FraudScore:
        """Score a single claim."""

    def score_batch(self, requests: List[ClaimScoreRequest]) -> List[FraudScore]:
        """Score multiple claims."""

    def get_model_info(self) -> ModelInfo:
        """Get current model information."""

    def update_threshold(self, line: str, threshold: float) -> None:
        """Update scoring threshold for insurance line."""
```

### ClaimScoreRequest

```python
@dataclass
class ClaimScoreRequest:
    claim_number: str
    policy_number: str
    claim_type: str
    reported_amount: float
    loss_date: str
    claimant_name: str
    loss_description: str
    additional_data: Dict[str, Any] = None
```

### FraudScore

```python
@dataclass
class FraudScore:
    claim_number: str
    risk_score: float
    risk_level: str
    confidence: float
    red_flags: List[str]
    recommendation: str
    model_version: str
    scored_at: datetime
```

### InvestigationCase

```python
@dataclass
class InvestigationCase:
    case_id: str
    claim_number: str
    fraud_score: float
    red_flags: List[str]
    assigned_investigator: str
    priority: str
    status: str
    created_at: datetime
    updated_at: datetime
```

### ProviderAnalyzer

```python
class ProviderAnalyzer:
    def __init__(self):
        """Initialize provider analyzer."""

    def analyze_provider(self, provider: ServiceProvider) -> ProviderAnalysis:
        """Analyze provider for fraud patterns."""

    def get_provider_history(self, provider_id: str) -> ProviderHistory:
        """Get provider claim history."""

    def compare_to_benchmarks(self, provider_id: str) -> BenchmarkComparison:
        """Compare provider to industry benchmarks."""
```

## Data Models

### ClaimData

```python
@dataclass
class ClaimData:
    claim_number: str
    policy_number: str
    claim_type: str
    reported_amount: float
    loss_date: datetime
    reported_date: datetime
    claimant_name: str
    loss_description: str
    loss_location: str
    status: str
```

### FraudIndicator

```python
@dataclass
class FraudIndicator:
    indicator_type: str
    description: str
    weight: float
    confidence: float
    source: str
```

### NetworkRelationship

```python
@dataclass
class NetworkRelationship:
    entity_a: str
    entity_b: str
    relationship_type: str
    strength: float
    evidence: List[str]
```

### ServiceProvider

```python
@dataclass
class ServiceProvider:
    provider_id: str
    provider_type: str
    name: str
    location: str
    claim_count: int
    total_billed: float
    average_claim: float
    specialities: List[str]
```

### InvestigationNote

```python
@dataclass
class InvestigationNote:
    note_id: str
    case_id: str
    author: str
    content: str
    created_at: datetime
    note_type: str
```

## Deployment Guide

### Initial Setup

```bash
# Install dependencies
pip install fraud-detection[ml]

# Initialize database
fraud-detection init-db

# Load initial models
fraud-detection load-model --version v3.0

# Configure data sources
fraud-detection configure --config config.yaml
```

### Production Deployment

```python
deployment_config = {
    "replicas": 3,
    "cpu": "2000m",
    "memory": "4Gi",
    "storage": "50Gi",
    "environment": "production",
    "logging_level": "INFO",
}
```

### Rollback Procedure

```bash
# Rollback to previous model version
fraud-detection rollback-model --to-version v2.9

# Restore database snapshot
fraud-detection restore-db --snapshot-id snap-123
```

## Monitoring & Observability

### Key Metrics

```python
metrics_config = {
    "scoring_latency": "histogram",
    "fraud_detection_rate": "gauge",
    "false_positive_rate": "gauge",
    "model_accuracy": "gauge",
    "case_processing_time": "histogram",
    "api_request_count": "counter",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Fraud Detection Dashboard",
    "panels": [
        "daily_fraud_scores",
        "detection_rate_trend",
        "case_volume",
        "model_performance",
        "siu_workload",
    ],
    "refresh_interval": "1h",
}
```

### Alerting Rules

```python
alerting_rules = [
    {"name": "HighFraudRate", "condition": "fraud_rate > 0.15", "severity": "warning"},
    {"name": "ModelDrift", "condition": "accuracy < 0.85", "severity": "critical"},
    {"name": "APIFailure", "condition": "error_rate > 0.05", "severity": "critical"},
]
```

## Testing Strategy

### Unit Tests

```python
def test_fraud_scoring():
    engine = FraudEngine(model_version="test")
    score = engine.score_claim(mock_claim)
    assert 0 <= score.risk_score <= 1
    assert score.risk_level in ["low", "medium", "high", "critical"]
```

### Integration Tests

```python
def test_full_scoring_pipeline():
    claim = create_test_claim()
    result = fraud_engine.score_claim(claim)
    assert result.confidence > 0.5
    assert len(result.red_flags) >= 0
```

### Model Validation Tests

```python
def test_model_accuracy():
    test_data = load_test_dataset()
    predictions = model.predict(test_data)
    accuracy = calculate_accuracy(predictions, test_data.labels)
    assert accuracy > 0.80
```

## Versioning & Migration

### Model Versioning

```python
version_config = {
    "current_version": "v3.0",
    "supported_versions": ["v2.9", "v3.0"],
    "deprecation_policy": "6 months",
    "rollback_enabled": True,
}
```

### Data Migration

```python
migration_config = {
    "schema_version": "3.0",
    "migration_steps": [
        "add_new_features",
        "update_model_registry",
        "migrate_historical_scores",
    ],
}
```

## Glossary

| Term | Definition |
|------|------------|
| **FNOL** | First Notice of Loss - initial claim reporting |
| **SIU** | Special Investigation Unit |
| **Red Flag** | Indicator of potential fraud |
| **Fraud Score** | Numerical risk assessment (0-1) |
| **Network Analysis** | Relationship mapping for fraud rings |
| **False Positive** | Legitimate claim flagged as suspicious |
| **Adjudication** | Claims decision-making process |
| **Subrogation** | Recovery from responsible third parties |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with ML models |
| 1.5.0 | 2024-11-01 | Added network analysis |
| 1.4.0 | 2024-09-15 | Provider fraud analytics |
| 1.3.0 | 2024-07-20 | Enhanced SIU integration |
| 1.2.0 | 2024-05-10 | Real-time scoring improvements |
| 1.1.0 | 2024-03-01 | Rule engine enhancements |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow ML best practices for model development
2. Validate all changes against test datasets
3. Document model performance metrics
4. Update fraud rules documentation
5. Test with historical fraud cases
6. Review SIU feedback before deployment

## Fraud Pattern Analysis

### Staged Accident Detection

```python
from fraud_detection import StagedAccidentDetector

detector = StagedAccidentDetector()

# Analyze for staged accident indicators
analysis = detector.analyze(
    claim_data={
        "accident_description": "Multi-vehicle pileup at intersection",
        "witness_count": 4,
        "all_parties_same_address": False,
        "claim_amount": 25000,
        "injury_severity": "moderate",
    },
)

print(f"Staged Accident Analysis:")
print(f"  Risk Score: {analysis.risk_score:.2f}")
print(f"  Indicators: {analysis.indicators}")
print(f"  Recommendation: {analysis.recommendation}")
```

### Medical Provider Fraud Detection

```python
from fraud_detection import MedicalFraudDetector

detector = MedicalFraudDetector()

# Analyze medical provider patterns
analysis = detector.analyze_provider(
    provider_id="PROV-MED-001",
    claims_data="provider_claims.csv",
)

print(f"Medical Provider Analysis:")
print(f"  Anomaly Score: {analysis.anomaly_score:.2f}")
print(f"  Unbundling Risk: {analysis.unbundling_risk:.1%}")
print(f"  Upcoding Risk: {analysis.upcoding_risk:.1%}")
print(f"  Referral Pattern: {analysis.referral_pattern}")
print(f"  Recommendation: {analysis.recommendation}")
```

### Fraud Ring Detection

```python
from fraud_detection import FraudRingDetector

detector = FraudRingDetector()

# Detect fraud rings through network analysis
rings = detector.detect(
    claims_data="claims_2024.csv",
    relationship_types=["shared_address", "shared_phone", "shared_provider", "shared_attorney"],
    min_ring_size=3,
)

print(f"Fraud Rings Detected: {len(rings)}")
for ring in rings:
    print(f"\n  Ring ID: {ring.ring_id}")
    print(f"  Size: {ring.member_count} members")
    print(f"  Total Claims: ${ring.total_claims:,.0f}")
    print(f"  Confidence: {ring.confidence:.1%}")
    print(f"  Members: {', '.join(ring.member_names[:5])}")
```

### Social Media Fraud Indicators

```python
from fraud_detection import SocialMediaAnalyzer

analyzer = SocialMediaAnalyzer()

# Analyze social media for fraud indicators
analysis = analyzer.analyze(
    claimant_name="John Smith",
    platforms=["facebook", "instagram", "linkedin"],
)

print(f"Social Media Analysis:")
print(f"  Profiles Found: {analysis.profile_count}")
print(f"  Inconsistencies: {len(analysis.inconsistencies)}")
for issue in analysis.inconsistencies:
    print(f"    - {issue.description}")
print(f"  Fraud Risk: {analysis.fraud_risk:.1%}")
```

## License

MIT License. See LICENSE file for full terms.

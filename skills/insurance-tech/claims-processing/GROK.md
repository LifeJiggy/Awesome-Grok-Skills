---
name: "claims-processing"
category: "insurance-tech"
version: "2.0.0"
tags: ["insurance", "claims", "automation", "processing", "workflow"]
description: "Automated insurance claims processing, adjudication, and settlement management"
---

# Claims Processing

## Overview

The Claims Processing module provides end-to-end automation for insurance claims lifecycle management. It covers first notice of loss (FNOL), claims investigation, coverage verification, damage assessment, adjudication, and settlement. The module supports multiple insurance lines (auto, property, health, liability), integrates with external data sources for fraud detection, and provides configurable workflows for claims handling with automated routing and escalation.

## Core Capabilities

- **FNOL Intake**: Multi-channel claims submission (web, mobile, API, agent-assisted)
- **Claims Triage**: Automated severity assessment and routing to appropriate handlers
- **Coverage Verification**: Real-time policy coverage validation and limit checking
- **Damage Assessment**: AI-assisted damage estimation using photos and descriptions
- **Adjudication Engine**: Rule-based claims decision making with configurable business rules
- **Settlement Processing**: Automated settlement calculation and payment initiation
- **Subrogation Detection**: Identify and initiate subrogation/recovery actions
- **Claims Analytics**: Real-time dashboards and claims performance metrics

## Usage Examples

### FNOL Submission

```python
from claims_processing import ClaimsEngine, FNOLSubmission, Claimant

engine = ClaimsEngine()

# Submit new claim
fnol = FNOLSubmission(
    policy_number="AUTO-2024-001234",
    claimant=Claimant(
        name="John Smith",
        email="john@example.com",
        phone="555-0123",
    ),
    loss_date="2024-01-15",
    loss_description="Rear-ended at stop light, significant trunk damage",
    loss_location="123 Main St, Anytown, USA",
    claim_type="auto_collision",
)

result = engine.submit_fnol(fnol)
print(f"Claim Number: {result.claim_number}")
print(f"Status: {result.status}")
print(f"Assigned Handler: {result.assigned_handler}")
```

### Claims Investigation

```python
from claims_processing import InvestigationEngine, EvidenceItem

investigator = InvestigationEngine(claim_number="CLM-2024-0001")

# Add evidence
investigator.add_evidence(EvidenceItem(
    type="photo",
    description="Vehicle damage photos",
    file_path="/evidence/claim-0001/damage_photos.zip",
    submitted_by="claimant",
))

investigator.add_evidence(EvidenceItem(
    type="police_report",
    description="Police report #PR-2024-5678",
    file_path="/evidence/claim-0001/police_report.pdf",
    submitted_by="claimant",
))

# Run investigation
investigation = investigator.investigate()
print(f"Investigation Status: {investigation.status}")
print(f"Evidence Items: {investigation.evidence_count}")
print(f"Fraud Indicators: {investigation.fraud_indicators}")
print(f"Recommendation: {investigation.recommendation}")
```

### Coverage Verification

```python
from claims_processing import CoverageVerifier, ClaimDetails

verifier = CoverageVerifier()

coverage = verifier.verify(
    policy_number="AUTO-2024-001234",
    claim=ClaimDetails(
        claim_type="auto_collision",
        loss_date="2024-01-15",
        estimated_amount=8500.00,
    ),
)

print(f"Coverage Status: {coverage.status}")
print(f"Covered: {coverage.is_covered}")
print(f" deductible: ${coverage.deductible:.2f}")
print(f"Coverage Limit: ${coverage.limit:.2f}")
print(f"Remaining Limit: ${coverage.remaining_limit:.2f}")
```

### Settlement Processing

```python
from claims_processing import SettlementEngine, SettlementDetails

settlement_engine = SettlementEngine()

settlement = settlement_engine.calculate(
    claim_number="CLM-2024-0001",
    approved_amount=7500.00,
    deductible=500.00,
    coverage_details=coverage,
)

print(f"Settlement Details:")
print(f"  Gross Amount: ${settlement.gross_amount:.2f}")
print(f"  Deductible: -${settlement.deductible:.2f}")
print(f"  Net Settlement: ${settlement.net_amount:.2f}")
print(f"  Payment Method: {settlement.payment_method}")
print(f"  Payment Status: {settlement.payment_status}")
```

## Best Practices

- **Immediate FNOL Processing**: Process claims promptly to meet regulatory requirements
- **Consistent Documentation**: Ensure all claim interactions are documented
- **Fraud Detection**: Run fraud checks at FNOL and throughout the claims process
- **Coverage Verification**: Verify coverage before committing to claim payments
- **Regulatory Compliance**: Ensure compliance with state and federal claims regulations
- **Customer Communication**: Keep claimants informed throughout the process
- **Audit Trail**: Maintain complete audit trail for all claim decisions
- **Performance Metrics**: Track and optimize claims processing KPIs

## Related Modules

- **fraud-detection**: Fraud detection and prevention in claims
- **risk-assessment**: Risk evaluation for claims triage
- **policy-management**: Policy lookup and verification

---

## Advanced Configuration

### Multi-Line Claims Configuration

```python
claims_config = {
    "auto": {
        "auto_adjudicate_threshold": 5000,
        "required_documents": ["police_report", "photos"],
        "investigation_threshold": 10000,
        "subrogation_threshold": 2500,
    },
    "property": {
        "auto_adjudicate_threshold": 10000,
        "required_documents": ["photos", "repair_estimate"],
        "investigation_threshold": 25000,
        "inspection_threshold": 50000,
    },
    "health": {
        "auto_adjudicate_threshold": 2000,
        "required_documents": ["medical_records", "bills"],
        "investigation_threshold": 10000,
        "preauth_required": True,
    },
}
```

### Workflow Configuration

```python
workflow_config = {
    "routing_rules": {
        "auto_collision": {"queue": "auto_claims", "priority": "normal"},
        "total_loss": {"queue": "total_loss", "priority": "high"},
        "bodily_injury": {"queue": "bi_claims", "priority": "high"},
        "property_damage": {"queue": "pd_claims", "priority": "normal"},
    },
    "escalation_rules": {
        "high_value": {"threshold": 50000, "escalate_to": "senior_adjuster"},
        "complex": {"flags": ["litigation", "fraud"], "escalate_to": "specialist"},
    },
    "sla_config": {
        "acknowledgment_hours": 24,
        "investigation_days": 30,
        "settlement_days": 45,
    },
}
```

### Document Management

```python
document_config = {
    "supported_formats": ["pdf", "jpg", "png", "docx"],
    "max_file_size_mb": 25,
    "auto_ocr": True,
    "extraction_models": {
        "photos": "damage_assessment_v2",
        "documents": "document_classification_v1",
    },
    "retention_days": 2555,  # 7 years
}
```

### Payment Processing

```python
payment_config = {
    "methods": ["check", "ach", "wire", "digital_wallet"],
    "auto_payment_threshold": 5000,
    "approval_required_above": 10000,
    "currency": "USD",
    "payment_terms_days": 30,
}
```

### Integration Configuration

```python
integration_config = {
    "fraud_detection": {"enabled": True, "threshold": 0.6},
    "payment_gateway": {"provider": "stripe", "enabled": True},
    "document_storage": {"provider": "s3", "bucket": "claims-docs"},
    "notification_service": {"email": True, "sms": True, "push": True},
}
```

## Architecture Patterns

### Event-Driven Claims Processing

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  FNOL       │────▶│  Event       │────▶│  Claims     │
│  Intake     │     │  Bus         │     │  Processor  │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Fraud  │           │  Coverage │         │  Payment  │
                    │  Check  │           │  Verify   │         │  Process  │
                    └─────────┘           └───────────┘         └───────────┘
```

### Microservices Architecture

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  FNOL Service   │  │  Claims Service │  │  Payment Service│
│  (Port 8081)    │  │  (Port 8082)    │  │  (Port 8083)    │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │  API Gateway      │
                    │  (Port 8080)      │
                    └───────────────────┘
```

### State Machine Pattern

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  New    │───▶│  Under   │───▶│  Adjust  │───▶│  Settled │
│  Claim  │    │  Review  │    │  Review  │    │          │
└─────────┘    └──────────┘    └──────────┘    └──────────┘
                    │               │
                    ▼               ▼
               ┌──────────┐   ┌──────────┐
               │  Denied  │   │  Pending │
               └──────────┘   └──────────┘
```

## Integration Guide

### Policy System Integration

```python
def verify_policy_coverage(policy_number, claim_details):
    policy = policy_api.get_policy(policy_number)
    coverage = policy.check_coverage(
        claim_type=claim_details.claim_type,
        loss_date=claim_details.loss_date,
        amount=claim_details.estimated_amount,
    )
    return {
        "covered": coverage.is_covered,
        "deductible": coverage.deductible,
        "limit": coverage.limit,
        "remaining": coverage.remaining_limit,
    }
```

### Fraud Detection Integration

```python
def run_fraud_checks(claim_data):
    fraud_result = fraud_api.score_claim(claim_data)
    if fraud_result.risk_score > 0.8:
        return {"flag": True, "reason": fraud_result.red_flags}
    return {"flag": False}
```

### Payment System Integration

```python
def process_payment(settlement):
    payment = payment_api.create_payment(
        claim_number=settlement.claim_number,
        amount=settlement.net_amount,
        method=settlement.payment_method,
        payee=settlement.payee_info,
    )
    return {"payment_id": payment.id, "status": payment.status}
```

### Document Management Integration

```python
def store_document(claim_number, document):
    doc_id = storage_api.upload(
        bucket="claims-documents",
        key=f"{claim_number}/{document.filename}",
        content=document.content,
        metadata={"claim_number": claim_number},
    )
    return {"document_id": doc_id}
```

## Performance Optimization

### Batch Processing

```python
batch_config = {
    "batch_size": 100,
    "parallel_workers": 4,
    "timeout_seconds": 300,
    "retry_count": 3,
}
```

### Caching Strategy

```python
cache_config = {
    "policy_cache_ttl": 300,
    "coverage_cache_ttl": 60,
    "provider_cache_ttl": 3600,
    "redis_enabled": True,
}
```

### Database Optimization

```python
db_config = {
    "connection_pool_size": 20,
    "read_replicas": 2,
    "query_timeout": 30,
    "indexing": ["claim_number", "policy_number", "loss_date"],
}
```

### API Optimization

```python
api_config = {
    "response_timeout": 10,
    "retry_count": 3,
    "circuit_breaker": True,
    "rate_limiting": 500,
}
```

## Security Considerations

### Data Protection

```python
security_config = {
    "encryption_at_rest": True,
    "encryption_in_transit": True,
    "pii_masking": True,
    "data_masking_fields": ["ssn", "phone", "email", "bank_account"],
    "access_logging": True,
}
```

### Access Control

```python
access_control = {
    "rbac_enabled": True,
    "roles": {
        "claims_adjuster": ["read_claims", "update_claims", "process_payments"],
        "claims_supervisor": ["read_claims", "assign_claims", "approve_settlements"],
        "admin": ["configure_workflow", "manage_users", "view_audit_logs"],
    },
    "mfa_required": True,
}
```

### Audit Logging

```python
audit_config = {
    "enabled": True,
    "retention_days": 2555,
    "events": [
        "claim_created", "claim_updated", "payment_processed",
        "document_uploaded", "user_login",
    ],
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| FNOL timeout | Slow policy lookup | Optimize policy API calls |
| Payment failure | Invalid payee data | Validate payment information |
| Document upload failure | File size exceeded | Compress files before upload |
| Coverage verification error | Policy not found | Verify policy number |
| Workflow stuck | Missing required data | Check claim completeness |
| Duplicate claim | Re-submission | Implement claim deduplication |

### Debug Commands

```bash
# Check claim status
claims-cli status --claim-number CLM-2024-0001

# View claim history
claims-cli history --claim-number CLM-2024-0001

# Test payment processing
claims-cli test-payment --claim-number CLM-2024-0001

# Verify coverage
claims-cli verify-coverage --policy-number AUTO-2024-001234
```

## API Reference

### ClaimsEngine

```python
class ClaimsEngine:
    def __init__(self):
        """Initialize claims engine."""

    def submit_fnol(self, fnol: FNOLSubmission) -> FNOLResult:
        """Submit first notice of loss."""

    def get_claim(self, claim_number: str) -> ClaimDetails:
        """Get claim details."""

    def update_claim(self, claim_number: str, updates: ClaimUpdate) -> ClaimResult:
        """Update claim information."""

    def process_settlement(self, claim_number: str) -> SettlementResult:
        """Process claim settlement."""
```

### FNOLSubmission

```python
@dataclass
class FNOLSubmission:
    policy_number: str
    claimant: Claimant
    loss_date: str
    loss_description: str
    loss_location: str
    claim_type: str
    estimated_amount: float = None
    witnesses: List[Witness] = None
```

### ClaimDetails

```python
@dataclass
class ClaimDetails:
    claim_number: str
    policy_number: str
    status: str
    claim_type: str
    loss_date: datetime
    reported_amount: float
    approved_amount: float = None
    assigned_handler: str = None
```

### SettlementResult

```python
@dataclass
class SettlementResult:
    claim_number: str
    gross_amount: float
    deductible: float
    net_amount: float
    payment_method: str
    payment_status: str
    settlement_date: datetime
```

## Data Models

### Claim

```python
@dataclass
class Claim:
    claim_number: str
    policy_number: str
    claimant: Claimant
    loss_date: datetime
    reported_date: datetime
    claim_type: str
    status: str
    estimated_amount: float
    approved_amount: float = None
    assigned_handler: str = None
```

### Claimant

```python
@dataclass
class Claimant:
    name: str
    email: str
    phone: str
    address: str = None
    ssn_last_four: str = None
```

### EvidenceItem

```python
@dataclass
class EvidenceItem:
    type: str
    description: str
    file_path: str
    submitted_by: str
    submitted_at: datetime = None
```

### Coverage

```python
@dataclass
class Coverage:
    coverage_name: str
    limit: float
    deductible: float
    remaining_limit: float
    effective_date: datetime
    expiration_date: datetime
```

## Deployment Guide

### Initial Setup

```bash
# Initialize database
claims-cli init-db

# Load configuration
claims-cli load-config --config config.yaml

# Create initial users
claims-cli create-user --email admin@company.com --role admin
```

### Production Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/deployment.yaml

# Verify deployment
kubectl rollout status deployment/claims-service
```

## Monitoring & Observability

### Key Metrics

```python
metrics_config = {
    "fnol_processing_time": "histogram",
    "claims_settled_count": "counter",
    "average_claim_amount": "gauge",
    "payment_success_rate": "gauge",
    "sla_compliance_rate": "gauge",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Claims Processing Dashboard",
    "panels": [
        "claims_by_status",
        "processing_time_trend",
        "settlement_amounts",
        "handler_workload",
    ],
}
```

## Testing Strategy

### Unit Tests

```python
def test_fnol_submission():
    engine = ClaimsEngine()
    result = engine.submit_fnol(mock_fnol)
    assert result.claim_number is not None
    assert result.status == "submitted"
```

### Integration Tests

```python
def test_full_claims_workflow():
    fnol = create_test_fnol()
    claim = engine.submit_fnol(fnol)
    coverage = engine.verify_coverage(claim.claim_number)
    assert coverage.is_covered
```

## Versioning & Migration

### Version Strategy

```python
version_config = {
    "current_version": "2.0.0",
    "supported_versions": ["1.9.x", "2.0.x"],
    "breaking_changes": "major",
}
```

## Glossary

| Term | Definition |
|------|------------|
| **FNOL** | First Notice of Loss |
| **Adjuster** | Claims professional handling the claim |
| **Adjudication** | Claims decision-making process |
| **Settlement** | Final payment and resolution of claim |
| **Subrogation** | Recovery from responsible third parties |
| **Deductible** | Amount paid by insured before insurance pays |
| **SLA** | Service Level Agreement |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with microservices |
| 1.5.0 | 2024-11-01 | Added AI damage assessment |
| 1.4.0 | 2024-09-15 | Enhanced payment processing |
| 1.3.0 | 2024-07-20 | Multi-line claims support |
| 1.2.0 | 2024-05-10 | Document management improvements |
| 1.1.0 | 2024-03-01 | Workflow automation |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow claims processing best practices
2. Write unit tests for new features
3. Update workflow documentation
4. Test with sample claims data
5. Review compliance requirements

## Claims Workflow Analytics

### Processing Time Analysis

```python
from claims_processing import WorkflowAnalytics

analytics = WorkflowAnalytics()

# Analyze processing times
report = analytics.analyze_processing_times(
    time_range_days=30,
    claim_types=["auto_collision", "property_damage"],
)

print(f"Processing Time Analysis:")
print(f"  Avg FNOL to Decision: {report.avg_fnol_to_decision_days:.1f} days")
print(f"  Avg Decision to Payment: {report.avg_decision_to_payment_days:.1f} days")
print(f"  Avg Total Cycle: {report.avg_total_cycle_days:.1f} days")
print(f"  SLA Compliance: {report.sla_compliance_rate:.1%}")
```

## Claims Processing Deep Dive

### Fraud Detection in Claims

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class ClaimType(Enum):
    AUTO = "auto"
    PROPERTY = "property"
    HEALTH = "health"
    LIABILITY = "liability"
    WORKERS_COMP = "workers_comp"

@dataclass
class ClaimFeature:
    claim_id: str
    claim_type: ClaimType
    amount: float
    policy_age_days: int
    time_to_report_hours: float
    prior_claims_count: int
    provider_network_match: bool
    document_completeness: float  # 0-1
    geographic_risk_score: float  # 0-1
    claimant_age: int
    coverage_type: str

class FraudScoringEngine:
    def __init__(self):
        self.rules: List[Dict] = []
        self.ml_weights: Dict[str, float] = {}
        self.historical_fraud_rate = 0.05
    
    def add_rule(self, rule_name: str, condition_fn, weight: float, description: str):
        self.rules.append({
            "name": rule_name, "condition": condition_fn,
            "weight": weight, "description": description,
        })
    
    def score_claim(self, feature: ClaimFeature) -> Dict:
        rule_scores = []
        for rule in self.rules:
            triggered = rule["condition"](feature)
            rule_scores.append({
                "rule": rule["name"],
                "triggered": triggered,
                "weight": rule["weight"] if triggered else 0,
                "description": rule["description"],
            })
        
        rule_total = sum(r["weight"] for r in rule_scores if r["triggered"])
        
        # ML-based features
        ml_score = self._compute_ml_score(feature)
        
        # Combined score
        combined = min(1.0, rule_total * 0.4 + ml_score * 0.6)
        
        risk_level = "low" if combined < 0.3 else "medium" if combined < 0.6 else "high" if combined < 0.8 else "critical"
        
        return {
            "claim_id": feature.claim_id,
            "fraud_score": round(combined, 4),
            "risk_level": risk_level,
            "rule_score": round(rule_total, 4),
            "ml_score": round(ml_score, 4),
            "triggered_rules": [r["rule"] for r in rule_scores if r["triggered"]],
            "recommended_action": self._action_for_risk(risk_level),
            "requires_investigation": risk_level in ["high", "critical"],
        }
    
    def _compute_ml_score(self, feature: ClaimFeature) -> float:
        score = 0.0
        # Amount anomaly
        if feature.claim_type == ClaimType.AUTO and feature.amount > 25000:
            score += 0.15
        elif feature.claim_type == ClaimType.PROPERTY and feature.amount > 100000:
            score += 0.2
        
        # Timing
        if feature.time_to_report_hours < 1:
            score += 0.1
        elif feature.time_to_report_hours > 720:  # 30 days
            score += 0.05
        
        # Policy age
        if feature.policy_age_days < 60:
            score += 0.15
        elif feature.policy_age_days < 30:
            score += 0.25
        
        # Prior claims
        if feature.prior_claims_count > 3:
            score += 0.1
        if feature.prior_claims_count > 5:
            score += 0.1
        
        # Document completeness
        if feature.document_completeness < 0.5:
            score += 0.15
        
        # Geographic risk
        score += feature.geographic_risk_score * 0.1
        
        return min(1.0, score)
    
    def _action_for_risk(self, risk_level: str) -> str:
        actions = {
            "low": "Auto-approve if within limits",
            "medium": "Route to senior adjuster for review",
            "high": "Assign to Special Investigations Unit (SIU)",
            "critical": "Escalate to SIU manager with hold on payment",
        }
        return actions.get(risk_level, "Route for manual review")

class ClaimsDeduplicationEngine:
    def __init__(self):
        self.active_claims: List[Dict] = []
    
    def check_duplicate(self, new_claim: Dict) -> Dict:
        matches = []
        for existing in self.active_claims:
            similarity = self._compute_similarity(new_claim, existing)
            if similarity > 0.7:
                matches.append({
                    "existing_claim_id": existing["claim_id"],
                    "similarity": round(similarity, 3),
                    "match_type": self._classify_match(new_claim, existing),
                })
        
        matches.sort(key=lambda x: x["similarity"], reverse=True)
        
        return {
            "is_potential_duplicate": len(matches) > 0,
            "matches": matches[:5],
            "recommendation": "hold" if matches and matches[0]["similarity"] > 0.9 else "proceed_with_review" if matches else "clear",
        }
    
    def _compute_similarity(self, claim_a: Dict, claim_b: Dict) -> float:
        score = 0.0
        total_weight = 0.0
        
        # Claimant match
        if claim_a.get("claimant_id") == claim_b.get("claimant_id"):
            score += 0.4
        total_weight += 0.4
        
        # Amount similarity
        amt_a = claim_a.get("amount", 0)
        amt_b = claim_b.get("amount", 0)
        if amt_a > 0 and amt_b > 0:
            amt_sim = 1 - abs(amt_a - amt_b) / max(amt_a, amt_b)
            score += amt_sim * 0.2
        total_weight += 0.2
        
        # Date proximity
        date_a = claim_a.get("incident_date", "")
        date_b = claim_b.get("incident_date", "")
        if date_a and date_b:
            date_sim = 1.0 if date_a == date_b else 0.5 if abs(hash(date_a) - hash(date_b)) < 86400 else 0
            score += date_sim * 0.2
        total_weight += 0.2
        
        # Description similarity (simplified)
        desc_a = set(claim_a.get("description", "").lower().split())
        desc_b = set(claim_b.get("description", "").lower().split())
        if desc_a and desc_b:
            jaccard = len(desc_a & desc_b) / max(1, len(desc_a | desc_b))
            score += jaccard * 0.2
        total_weight += 0.2
        
        return score / total_weight if total_weight > 0 else 0
    
    def _classify_match(self, new_claim: Dict, existing: Dict) -> str:
        if new_claim.get("claimant_id") == existing.get("claimant_id"):
            return "same_claimant"
        elif abs(new_claim.get("amount", 0) - existing.get("amount", 0)) < 100:
            return "similar_amount"
        return "coincidental"

class SubrogationRecoveryTracker:
    def __init__(self):
        self.recovery_candidates: List[Dict] = []
    
    def identify_candidate(self, claim_data: Dict) -> Optional[Dict]:
        if claim_data.get("fault_party") and claim_data["fault_party"] != "insured":
            estimated_recovery = claim_data.get("payout_amount", 0) * 0.6
            
            return {
                "claim_id": claim_data["claim_id"],
                "fault_party": claim_data["fault_party"],
                "estimated_recovery": round(estimated_recovery, 2),
                "statute_of_limitations_days": claim_data.get("sol_days", 730),
                "evidence_strength": self._assess_evidence(claim_data),
                "priority": "high" if estimated_recovery > 10000 else "medium",
            }
        return None
    
    def _assess_evidence(self, claim_data: Dict) -> float:
        evidence_score = 0.0
        if claim_data.get("police_report"):
            evidence_score += 0.3
        if claim_data.get("witness_statements"):
            evidence_score += 0.2
        if claim_data.get("photos"):
            evidence_score += 0.2
        if claim_data.get("expert_report"):
            evidence_score += 0.3
        return evidence_score
    
    def track_recovery(self, claim_id: str, status: str, amount: float):
        self.recovery_candidates.append({
            "claim_id": claim_id, "status": status,
            "recovered_amount": amount,
        })
    
    def get_recovery_summary(self) -> Dict:
        total_identified = sum(c.get("estimated_recovery", 0) for c in self.recovery_candidates)
        total_recovered = sum(c.get("recovered_amount", 0) for c in self.recovery_candidates)
        
        return {
            "total_candidates": len(self.recovery_candidates),
            "total_identified_value": round(total_identified, 2),
            "total_recovered": round(total_recovered, 2),
            "recovery_rate": round(total_recovered / max(1, total_identified), 3),
            "pending": sum(1 for c in self.recovery_candidates if c.get("status") == "pending"),
        }
```

## License

MIT License. See LICENSE file for full terms.

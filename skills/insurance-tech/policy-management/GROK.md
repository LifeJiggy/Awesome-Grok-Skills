---
name: "policy-management"
category: "insurance-tech"
version: "2.0.0"
tags: ["insurance", "policy", "management", "lifecycle", "renewal"]
description: "Insurance policy lifecycle management, endorsements, and renewal processing"
---

# Policy Management

## Overview

The Policy Management module provides comprehensive lifecycle management for insurance policies from quote issuance through renewal or cancellation. It supports policy creation, endorsement processing, billing integration, renewal management, and compliance tracking. The module handles multi-line policies, configurable coverage options, and automated renewal workflows with integration to rating engines and policy administration systems.

## Core Capabilities

- **Policy Lifecycle Management**: Full lifecycle from quote to cancellation
- **Endorsement Processing**: Mid-term policy changes and adjustments
- **Coverage Configuration**: Flexible coverage options and limits
- **Renewal Management**: Automated renewal workflows with retention optimization
- **Billing Integration**: Premium calculation and billing synchronization
- **Document Generation**: Policy declarations, certificates, and endorsements
- **Compliance Tracking**: Regulatory compliance and filing requirements
- **Agent/Broker Management**: Commission tracking and agent portal integration

## Usage Examples

### Policy Creation

```python
from policy_management import PolicyEngine, PolicyApplication, CoverageOption

engine = PolicyEngine()

# Create policy application
application = PolicyApplication(
    applicant_name="Acme Corporation",
    insurance_line="commercial_property",
    effective_date="2024-02-01",
    coverages=[
        CoverageOption(name="building", limit=1000000, deductible=5000),
        CoverageOption(name="contents", limit=250000, deductible=2500),
        CoverageOption(name="business_interruption", limit=500000, deductible=10000),
    ],
    additional_interests=["Mortgage Company Inc."],
)

# Issue policy
policy = engine.issue_policy(application)
print(f"Policy Number: {policy.policy_number}")
print(f"Effective Date: {policy.effective_date}")
print(f"Expiration Date: {policy.expiration_date}")
print(f"Premium: ${policy.premium:,.2f}")
```

### Endorsement Processing

```python
from policy_management import EndorsementRequest, CoverageChange

# Request endorsement
endorsement = EndorsementRequest(
    policy_number="CP-2024-001234",
    effective_date="2024-06-01",
    changes=[
        CoverageChange(
            coverage_name="building",
            action="increase_limit",
            new_limit=1500000,
            reason="Property value increase",
        ),
    ],
    requested_by="agent-001",
)

result = engine.process_endorsement(endorsement)
print(f"Endorsement Number: {result.endorsement_number}")
print(f"Premium Change: ${result.premium_change:,.2f}")
print(f"New Total Premium: ${result.new_premium:,.2f}")
```

### Renewal Processing

```python
from policy_management import RenewalProcessor

processor = RenewalProcessor()

# Process renewal
renewal = processor.process_renewal(
    policy_number="CP-2024-001234",
    renewal_term="annual",
    retention_offer=True,
)

print(f"Renewal Details:")
print(f"  Policy: {renewal.policy_number}")
print(f"  New Term: {renewal.new_effective_date} to {renewal.new_expiration_date}")
print(f"  Renewal Premium: ${renewal.renewal_premium:,.2f}")
print(f"  Retention Discount: {renewal.retention_discount:.1%}")
print(f"  Status: {renewal.status}")
```

### Policy Inquiry

```python
from policy_management import PolicyInquiry

inquiry = PolicyInquiry()

# Get policy details
policy_details = inquiry.get_policy("CP-2024-001234")
print(f"Policy Details:")
print(f"  Number: {policy_details.policy_number}")
print(f"  Insured: {policy_details.insured_name}")
print(f"  Line: {policy_details.insurance_line}")
print(f"  Status: {policy_details.status}")
print(f"  Coverages: {len(policy_details.coverages)}")
print(f"  Premium: ${policy_details.premium:,.2f}")

# Get policy history
history = inquiry.get_policy_history("CP-2024-001234")
print(f"\nPolicy History ({len(history)} transactions):")
for transaction in history[:5]:
    print(f"  {transaction.date}: {transaction.description}")
```

## Best Practices

- **Data Validation**: Validate all policy data at entry to prevent errors
- **Regulatory Compliance**: Ensure policies meet state and federal requirements
- **Audit Trail**: Maintain complete audit trail for all policy transactions
- **Automated Renewals**: Use automated workflows for timely renewal processing
- **Coverage Accuracy**: Verify coverage limits and deductibles at each transaction
- **Document Management**: Maintain organized policy document storage
- **Commission Accuracy**: Ensure accurate commission calculations for agents
- **Customer Communication**: Provide timely notifications for policy changes

## Related Modules

- **risk-assessment**: Risk evaluation for policy pricing
- **underwriting-ai**: AI-assisted underwriting decisions
- **claims-processing**: Claims integration with policy data

---

## Advanced Configuration

### Multi-Line Policy Configuration

```python
policy_config = {
    "auto": {
        "coverages": ["liability", "collision", "comprehensive", "uninsured_motorist"],
        "limits": {"liability": [25000, 50000, 25000, 50000, 100000]},
        "deductibles": [250, 500, 1000, 2000],
        "state_requirements": {"minimum_liability": True},
    },
    "property": {
        "coverages": ["dwelling", "personal_property", "liability", "loss_of_use"],
        "limits": {"dwelling": "replacement_cost"},
        "deductibles": [500, 1000, 2500, 5000],
        "flood_required": False,
    },
    "commercial": {
        "coverages": ["general_liability", "property", "workers_comp", "cyber"],
        "limits": {"general_liability": [1000000, 2000000, 5000000]},
        "deductibles": [1000, 2500, 5000],
    },
}
```

### Endorsement Rules

```python
endorsement_rules = {
    "allowed_changes": [
        "increase_limit", "decrease_limit", "add_coverage",
        "remove_coverage", "change_deductible", "add_interest",
    ],
    "approval_required": {
        "limit_increase_above": 100000,
        "coverage_addition": True,
        "deductible_change": True,
    },
    "effective_date_rules": {
        "immediate": ["add_interest"],
        "next_billing": ["premium_financing"],
        "specified_date": ["all_other_changes"],
    },
}
```

### Renewal Configuration

```python
renewal_config = {
    "auto_renewal": True,
    "renewal_notice_days": [90, 60, 30],
    "retention_offer": {
        "enabled": True,
        "max_discount": 0.15,
        "loyalty_threshold_years": 3,
    },
    "non_renewal_reasons": [
        "excessive_claims", "underwriting_loss", "risk_unacceptable",
    ],
    "grace_period_days": 30,
}
```

### Billing Integration

```python
billing_config = {
    "payment_plans": ["annual", "semi_annual", "quarterly", "monthly"],
    "auto_pay_discount": 0.05,
    "late_fee_percentage": 0.02,
    "cancellation_threshold_days": 60,
    "billing_system": "integrated",
}
```

### Document Generation

```python
document_config = {
    "templates": {
        "declarations": "declarations_v2.docx",
        "certificate": "certificate_v1.docx",
        "endorsement": "endorsement_v1.docx",
        "renewal_notice": "renewal_notice_v1.docx",
    },
    "digital_signatures": True,
    "e_delivery": True,
    "retention_years": 7,
}
```

## Architecture Patterns

### Policy Lifecycle State Machine

```
┌─────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Quote  │───▶│  Applic- │───▶│  Under-  │───▶│  Active  │
│         │    │  ation   │    │  writing │    │  Policy  │
└─────────┘    └──────────┘    └──────────┘    └──────────┘
                    │               │               │
                    ▼               ▼               ▼
               ┌──────────┐   ┌──────────┐   ┌──────────┐
               │  Declined│   │  Pending │   │  Renewal │
               └──────────┘   └──────────┘   └──────────┘
```

### Microservices Architecture

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Quote Service  │  │  Policy Service │  │  Billing Service│
│  (Port 8081)    │  │  (Port 8082)    │  │  (Port 8083)    │
└────────┬────────┘  └────────┬────────┘  └────────┬────────┘
         │                    │                    │
         └────────────────────┼────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │  Event Bus        │
                    │  (Kafka/SQS)      │
                    └───────────────────┘
```

### Event-Driven Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Policy     │────▶│  Event       │────▶│  Downstream │
│  Changes    │     │  Publisher   │     │  Systems    │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Billing│           │  Claims   │         │  Reporting│
                    │  System │           │  System   │         │  System   │
                    └─────────┘           └───────────┘         └───────────┘
```

## Integration Guide

### Rating Engine Integration

```python
def calculate_premium(policy_application):
    rating_input = {
        "line": policy_application.insurance_line,
        "coverages": policy_application.coverages,
        "risk_factors": policy_application.risk_factors,
        "territory": policy_application.location,
    }
    rating_result = rating_engine.calculate(rating_input)
    return {"premium": rating_result.premium, "factors": rating_result.factors}
```

### Billing System Integration

```python
def create_billing_account(policy):
    billing_account = billing_api.create_account(
        policy_number=policy.policy_number,
        insured_name=policy.insured_name,
        premium=policy.premium,
        payment_plan=policy.payment_plan,
    )
    return {"account_id": billing_account.id}
```

### Document Management Integration

```python
def generate_policy_documents(policy):
    documents = []
    for template_name, template_path in document_templates.items():
        doc = document_generator.generate(
            template=template_path,
            data=policy.to_dict(),
        )
        doc_id = storage_api.store(doc, f"policies/{policy.policy_number}/")
        documents.append({"type": template_name, "id": doc_id})
    return documents
```

### Agent Portal Integration

```python
def sync_to_agent_portal(policy):
    agent_api.update_policy(
        agent_id=policy.agent_id,
        policy_data={
            "policy_number": policy.policy_number,
            "insured_name": policy.insured_name,
            "premium": policy.premium,
            "status": policy.status,
            "effective_date": policy.effective_date,
        },
    )
```

## Performance Optimization

### Policy Search Optimization

```python
search_config = {
    "indexing_fields": ["policy_number", "insured_name", "agent_id"],
    "full_text_search": True,
    "search_timeout": 5,
    "max_results": 100,
}
```

### Batch Processing

```python
batch_config = {
    "renewal_batch_size": 1000,
    "endorsement_batch_size": 500,
    "document_generation_batch": 100,
    "parallel_workers": 4,
}
```

### Caching Strategy

```python
cache_config = {
    "policy_cache_ttl": 300,
    "rating_cache_ttl": 60,
    "agent_cache_ttl": 3600,
    "redis_enabled": True,
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
        "agent": ["create_quotes", "view_policies", "process_endorsements"],
        "underwriter": ["view_policies", "approve_applications", "set_pricing"],
        "billing": ["view_policies", "process_payments", "manage_billing"],
        "admin": ["configure_system", "manage_users", "view_audit_logs"],
    },
    "mfa_required": True,
}
```

### Regulatory Compliance

```python
compliance_config = {
    "state_filing_required": True,
    "rate_filing_states": ["CA", "NY", "TX", "FL"],
    "surcharge_disclosure": True,
    "cancellation_notice_days": 30,
    "audit_trail_retention": 2555,  # 7 years
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Premium calculation error | Invalid rating factors | Verify rating engine input |
| Endorsement effective date | Policy already expired | Check policy status |
| Renewal not generating | Auto-renewal disabled | Check renewal configuration |
| Document generation failure | Template missing | Verify template path |
| Billing sync failure | API timeout | Retry with backoff |
| Commission calculation error | Agent rate misconfigured | Verify agent commission rates |

### Debug Commands

```bash
# Check policy status
policy-cli status --policy-number CP-2024-001234

# View policy history
policy-cli history --policy-number CP-2024-001234

# Test premium calculation
policy-cli calculate-premium --line auto --factors '{"age": 35}'

# Verify renewal eligibility
policy-cli check-renewal --policy-number CP-2024-001234
```

## API Reference

### PolicyEngine

```python
class PolicyEngine:
    def __init__(self):
        """Initialize policy engine."""

    def issue_policy(self, application: PolicyApplication) -> Policy:
        """Issue new policy."""

    def process_endorsement(self, endorsement: EndorsementRequest) -> EndorsementResult:
        """Process policy endorsement."""

    def renew_policy(self, policy_number: str) -> RenewalResult:
        """Process policy renewal."""

    def cancel_policy(self, policy_number: str, reason: str) -> CancelResult:
        """Cancel policy."""
```

### PolicyApplication

```python
@dataclass
class PolicyApplication:
    applicant_name: str
    insurance_line: str
    effective_date: str
    coverages: List[CoverageOption]
    additional_interests: List[str] = None
    agent_id: str = None
    risk_factors: Dict[str, Any] = None
```

### EndorsementRequest

```python
@dataclass
class EndorsementRequest:
    policy_number: str
    effective_date: str
    changes: List[CoverageChange]
    requested_by: str
    reason: str = None
```

### RenewalResult

```python
@dataclass
class RenewalResult:
    policy_number: str
    new_effective_date: str
    new_expiration_date: str
    renewal_premium: float
    retention_discount: float
    status: str
```

## Data Models

### Policy

```python
@dataclass
class Policy:
    policy_number: str
    insured_name: str
    insurance_line: str
    status: str
    effective_date: str
    expiration_date: str
    premium: float
    coverages: List[Coverage]
    agent_id: str = None
```

### Coverage

```python
@dataclass
class Coverage:
    coverage_name: str
    limit: float
    deductible: float
    premium: float
    effective_date: str
    expiration_date: str
```

### CoverageOption

```python
@dataclass
class CoverageOption:
    name: str
    limit: float
    deductible: float = None
    premium: float = None
```

### PolicyTransaction

```python
@dataclass
class PolicyTransaction:
    transaction_id: str
    policy_number: str
    transaction_type: str
    effective_date: str
    description: str
    premium_change: float
    created_at: datetime
```

## Deployment Guide

### Initial Setup

```bash
# Initialize database
policy-cli init-db

# Load rating tables
policy-cli load-rates --file rates.yaml

# Configure integrations
policy-cli configure --config config.yaml
```

### Production Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/policy-service.yaml

# Verify deployment
kubectl rollout status deployment/policy-service
```

## Monitoring & Observability

### Key Metrics

```python
metrics_config = {
    "policies_issued": "counter",
    "endorsements_processed": "counter",
    "renewals_completed": "counter",
    "premium_written": "gauge",
    "processing_time": "histogram",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Policy Management Dashboard",
    "panels": [
        "policies_by_status",
        "premium_trends",
        "renewal_rates",
        "endorsement_volume",
    ],
}
```

## Testing Strategy

### Unit Tests

```python
def test_policy_issuance():
    engine = PolicyEngine()
    policy = engine.issue_policy(mock_application)
    assert policy.policy_number is not None
    assert policy.premium > 0
```

### Integration Tests

```python
def test_endorsement_flow():
    policy = create_test_policy()
    endorsement = create_test_endorsement(policy.policy_number)
    result = engine.process_endorsement(endorsement)
    assert result.status == "completed"
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
| **Endorsement** | Mid-term policy change |
| **Renewal** | Continuation of policy for new term |
| **Declarations** | Summary of policy coverages and information |
| **Premium** | Cost of insurance coverage |
| **Deductible** | Amount paid by insured before insurance pays |
| **Underwriting** | Risk evaluation and pricing process |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with microservices |
| 1.5.0 | 2024-11-01 | Added automated renewals |
| 1.4.0 | 2024-09-15 | Enhanced endorsement processing |
| 1.3.0 | 2024-07-20 | Document generation improvements |
| 1.2.0 | 2024-05-10 | Billing integration |
| 1.1.0 | 2024-03-01 | Agent portal integration |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow insurance industry standards
2. Write unit tests for new features
3. Update documentation for changes
4. Test with sample policy data
5. Review compliance requirements

## Policy Performance Analytics

### Retention Analysis

```python
from policy_management import RetentionAnalyzer

analyzer = RetentionAnalyzer()

# Analyze retention rates
retention = analyzer.analyze(
    time_range_months=12,
    segments=["auto", "property", "commercial"],
)

print(f"Retention Analysis:")
print(f"  Overall Retention: {retention.overall_rate:.1%}")
for segment in retention.segments:
    print(f"  {segment.name}: {segment.retention_rate:.1%} ({segment.trend})")
print(f"  Renewal Revenue: ${retention.renewal_revenue:,.2f}")
```

## Policy Management Deep Dive

### Dynamic Policy Pricing Engine

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class PolicyLine(Enum):
    AUTO = "auto"
    HOME = "home"
    LIFE = "life"
    HEALTH = "health"
    BUSINESS = "business"

@dataclass
class PolicyProfile:
    policy_id: str
    line: PolicyLine
    policyholder_age: int
    coverage_amount: float
    deductible: float
    territory: str
    risk_score: float       # 0-1 from underwriting
    loyalty_years: int
    claims_count_3yr: int
    credit_score: int
    coverage_options: Dict[str, bool]

class DynamicPricingEngine:
    def __init__(self):
        self.base_rates: Dict[str, float] = {}
        self.rating_factors: Dict[str, Dict] = {}
        self.discount_schedules: Dict[str, List[Dict]] = {}
    
    def set_base_rate(self, line: str, base_annual: float):
        self.base_rates[line] = base_annual
    
    def calculate_premium(self, profile: PolicyProfile) -> Dict:
        base = self.base_rates.get(profile.line.value, 1000)
        
        # Rating factors
        age_factor = self._age_factor(profile.line, profile.policyholder_age)
        risk_factor = 0.7 + (profile.risk_score * 0.8)  # 0.7 - 1.5
        coverage_factor = profile.coverage_amount / 100000
        deductible_factor = max(0.6, 1.0 - (profile.deductible / profile.coverage_amount))
        territory_factor = self._territory_factor(profile.territory)
        
        # Claims history
        claims_surcharge = 1.0 + (profile.claims_count_3yr * 0.15)
        
        # Loyalty discount
        loyalty_discount = max(0.85, 1.0 - (profile.loyalty_years * 0.02))
        
        # Credit-based score
        credit_factor = 0.85 + ((850 - profile.credit_score) / 850) * 0.3
        
        # Coverage options surcharge
        options_surcharge = 1.0
        for option, selected in profile.coverage_options.items():
            if selected:
                options_surcharge += self._option_surcharge(profile.line.value, option)
        
        # Calculate gross premium
        gross_premium = (base * age_factor * risk_factor * coverage_factor * 
                        deductible_factor * territory_factor * claims_surcharge * 
                        credit_factor * options_surcharge)
        
        # Apply loyalty discount
        annual_premium = gross_premium * loyalty_discount
        
        # Multi-policy discount
        multi_policy = self._multi_policy_discount(profile)
        annual_premium *= (1 - multi_policy)
        
        return {
            "policy_id": profile.policy_id,
            "line": profile.line.value,
            "annual_premium": round(annual_premium, 2),
            "monthly_premium": round(annual_premium / 12, 2),
            "factors": {
                "age": round(age_factor, 3),
                "risk": round(risk_factor, 3),
                "coverage": round(coverage_factor, 3),
                "deductible": round(deductible_factor, 3),
                "territory": round(territory_factor, 3),
                "claims_surcharge": round(claims_surcharge, 3),
                "loyalty_discount": round(loyalty_discount, 3),
                "credit": round(credit_factor, 3),
                "options": round(options_surcharge, 3),
                "multi_policy": round(multi_policy, 3),
            },
            "breakdown": {
                "base_rate": base,
                "after_rating": round(gross_premium, 2),
                "after_discounts": round(annual_premium, 2),
            },
        }
    
    def _age_factor(self, line: PolicyLine, age: int) -> float:
        if line == PolicyLine.AUTO:
            if age < 25: return 1.5
            elif age < 65: return 0.9 + (age - 25) * 0.003
            else: return 1.2
        elif line == PolicyLine.LIFE:
            return 0.5 + (age / 100) ** 1.5
        elif line == PolicyLine.HEALTH:
            return 0.8 + (age / 100) ** 1.2
        return 1.0
    
    def _territory_factor(self, territory: str) -> float:
        factors = {"urban": 1.3, "suburban": 1.0, "rural": 0.85, "coastal": 1.4, "mountain": 0.9}
        return factors.get(territory, 1.0)
    
    def _option_surcharge(self, line: str, option: str) -> float:
        surcharges = {
            "auto": {"roadside": 0.03, "rental": 0.02, "gap": 0.04},
            "home": {"flood": 0.08, "earthquake": 0.06, "umbrella": 0.05},
            "life": {"accidental_death": 0.05, "waiver_of_premium": 0.03},
        }
        return surcharges.get(line, {}).get(option, 0.02)
    
    def _multi_policy_discount(self, profile: PolicyProfile) -> float:
        return 0.05  # simplified

class RenewalOptimizer:
    def __init__(self):
        self.renewal_data: List[Dict] = []
    
    def analyze_renewal_risk(self, policy_id: str, history: Dict) -> Dict:
        prior_renewals = history.get("renewals", [])
        if not prior_renewals:
            return {"renewal_probability": 0.7, "confidence": "low"}
        
        on_time_rate = sum(1 for r in prior_renewals if r.get("on_time", False)) / len(prior_renewals)
        price_sensitivity = history.get("price_sensitivity", 0.5)
        satisfaction_score = history.get("satisfaction_score", 0.7)
        
        renewal_prob = (on_time_rate * 0.4 + satisfaction_score * 0.3 + (1 - price_sensitivity) * 0.3)
        
        recommended_actions = []
        if renewal_prob < 0.5:
            recommended_actions.append("Offer retention discount (5-10%)")
            recommended_actions.append("Schedule personal outreach from agent")
        elif renewal_prob < 0.7:
            recommended_actions.append("Send early renewal notice with loyalty benefits")
        
        return {
            "policy_id": policy_id,
            "renewal_probability": round(renewal_prob, 3),
            "on_time_history": round(on_time_rate, 3),
            "recommended_actions": recommended_actions,
            "optimal_contact_days_before_expiry": 45 if renewal_prob < 0.6 else 30,
            "retention_offer_budget": round(history.get("annual_premium", 0) * 0.1, 2),
        }
    
    def generate_renewal_package(self, policy_id: str, current_policy: Dict, 
                                 market_rates: Dict) -> Dict:
        current_premium = current_policy.get("annual_premium", 0)
        market_avg = market_rates.get(current_policy.get("line", ""), {}).get("average", current_premium)
        competitive_index = current_premium / market_avg if market_avg > 0 else 1.0
        
        changes = []
        if competitive_index > 1.1:
            changes.append({"type": "discount", "reason": "Competitive pricing", "amount_pct": -5})
        if current_policy.get("no_claims_years", 0) >= 3:
            changes.append({"type": "discount", "reason": "Claims-free discount", "amount_pct": -8})
        
        new_premium = current_premium * (1 + sum(c.get("amount_pct", 0) for c in changes) / 100)
        
        return {
            "policy_id": policy_id,
            "current_premium": current_premium,
            "renewal_premium": round(new_premium, 2),
            "changes": changes,
            "competitive_position": "below_market" if competitive_index < 0.95 else "at_market" if competitive_index < 1.05 else "above_market",
            "market_comparison": {
                "your_premium": current_premium,
                "market_average": market_avg,
                "percentile": round(competitive_index * 50, 1),
            },
        }

class PolicyDocumentGenerator:
    def generate_declaration_page(self, policy: Dict) -> Dict:
        return {
            "document_type": "declarations_page",
            "policy_number": policy.get("policy_id"),
            "effective_date": policy.get("effective_date"),
            "expiration_date": policy.get("expiration_date"),
            "named_insured": policy.get("insured_name"),
            "coverage_summary": {
                "total_premium": policy.get("annual_premium"),
                "deductible": policy.get("deductible"),
                "limits": policy.get("limits", {}),
                "endorsements": policy.get("endorsements", []),
            },
            "payment_schedule": {
                "annual": policy.get("annual_premium"),
                "semi_annual": round(policy.get("annual_premium", 0) / 2, 2),
                "quarterly": round(policy.get("annual_premium", 0) / 4, 2),
                "monthly": round(policy.get("annual_premium", 0) / 12, 2),
            },
        }
```

## License

MIT License. See LICENSE file for full terms.

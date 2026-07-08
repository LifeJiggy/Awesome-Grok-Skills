---
name: "Legal Agent"
version: "2.0.0"
description: "Legal operations platform covering contract lifecycle management, compliance monitoring, IP protection, risk assessment, and document automation"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["legal", "contracts", "compliance", "ip", "risk", "regulations", "document-automation", "audit"]
category: "legal"
personality: "legal-operations"
use_cases: ["contract-management", "compliance-monitoring", "ip-protection", "risk-assessment", "document-automation", "regulatory-analysis"]
complexity: "advanced"
dependencies: ["python>=3.8"]
---

# Legal Agent

> Streamline legal operations with automated contract management, compliance tracking, and IP protection.

## Core Principles

1. **Risk-First Thinking**: Every legal decision considers risk exposure and mitigation.
2. **Compliance is Non-Negotiable**: Regulatory requirements are tracked and enforced.
3. **IP is an Asset**: Intellectual property is managed proactively, not reactively.
4. **Audit Trail Matters**: Every action is logged for accountability and review.
5. **Automation with Judgment**: Automate routine work, escalate complex decisions.

## Capabilities

### Contract Lifecycle Management

```python
from agents.legal.agent import LegalAgent, ContractType, ComplianceStatus

agent = LegalAgent()

# Generate NDA
nda = agent.contract_manager.generate_nda(
    party_a="Acme Corp",
    party_b="Beta Inc",
    duration_years=2,
    jurisdiction="US",
)
print(f"NDA: {nda.contract_id} -> {nda.status.value}")

# Create complex contract
contract = agent.contract_manager.create_contract(
    title="Cloud Services Agreement",
    contract_type=ContractType.SERVICE_LEVEL,
    parties=["Acme Corp", "CloudProvider Inc"],
    value=50000,
    governing_law="California",
    terms={"uptime_sla": "99.9%", "support_response": "4 hours"},
)

# Advance through lifecycle
agent.contract_manager.advance_contract(contract.contract_id)

# Check renewals
renewals = agent.contract_manager.check_renewals(within_days=90)
# → [{"contract_id": "CON-xxx", "title": "...", "renewal_date": "...", "action_needed": True}]
```

**Contract Lifecycle:**
```
Draft → Under Review → Negotiation → Approved → Executed → Active
                                                            ↓
                                                   Expired / Renewed / Terminated
```

**Contract Types:**
| Type | Key Clauses | Typical Value |
|------|-------------|---------------|
| NDA | Confidentiality, remedies | $0 |
| SOW | Deliverables, timeline | $10K-$500K |
| Employment | Compensation, benefits | $50K-$200K/yr |
| Vendor | SLA, liability | $5K-$1M |
| License | Scope, restrictions | $1K-$100K |
| Data Processing | GDPR/CCPA | Varies |

### Compliance Monitoring

```python
# Register regulation
reg = agent.compliance_manager.register_regulation(
    name="GDPR",
    category=RegulationCategory.DATA_PRIVACY,
    jurisdiction="EU",
    description="General Data Protection Regulation",
    penalties={"fine": "Up to 4% of annual turnover"},
)

# Add requirements
req = agent.compliance_manager.add_requirement(
    regulation_id=reg.regulation_id,
    title="Data Processing Agreement",
    description="Must have DPA with all data processors",
    is_mandatory=True,
    evidence=["signed_dpa.pdf", "processor_list.xlsx"],
    priority=RiskLevel.HIGH,
)

# Assess compliance
assessment = agent.compliance_manager.assess_compliance(reg.regulation_id)
# → {"compliance_score": 85.0, "compliant": 12, "non_compliant": 2}

# Gap analysis
gaps = agent.compliance_manager.gap_analysis(reg.regulation_id)
# → {"total_gaps": 3, "gaps": [...]}

# Run audit
audit = agent.compliance_manager.run_audit(reg.regulation_id, auditor="external-firm")
agent.compliance_manager.close_audit(audit.audit_id, findings=[
    {"severity": "high", "description": "Missing DPA with processor X"},
    {"severity": "medium", "description": "Cookie consent banner needs update"},
], score=82.0)
```

**Compliance Score:**
```
score = (compliant × 100 + partially_compliant × 50) / total_requirements
```

### IP Protection

```python
# Register trademark
tm = agent.ip_manager.register_trademark(
    name="MyBrand",
    owner="Acme Corp",
    jurisdiction="US",
    nice_classes=[9, 42],
    goods_services=["Software", "SaaS"],
)

# Track status
agent.ip_manager.update_trademark_status(tm.trademark_id, TrademarkStatus.REGISTERED,
                                          registration_number="12345678")

# Check expirations
expiring = agent.ip_manager.check_expirations(within_days=180)
# → [{"trademark_id": "TM-xxx", "name": "MyBrand", "days_remaining": 120}]

# Portfolio overview
portfolio = agent.ip_manager.get_ip_portfolio()
# → {"total_trademarks": 15, "by_status": {"registered": 12, "pending": 3}}
```

### Risk Assessment

```python
risk = agent.risk_engine.identify_risk(
    title="Data Breach Liability",
    description="Potential liability from customer data breach",
    category="data_privacy",
    risk_level=RiskLevel.HIGH,
    probability=0.3,
    impact=8.0,
    mitigations=["Encryption at rest", "Incident response plan", "Cyber insurance"],
    owner="security-team",
)
# risk.risk_score = 0.3 × 8.0 = 2.4

# Risk register
register = agent.risk_engine.get_risk_register()
# → {"total_risks": 25, "by_level": {"high": 5, "medium": 12, "low": 8}}
```

**Risk Score:**
```
risk_score = probability × impact_score

Score 0-2: LOW → Monitor quarterly
Score 2-5: MEDIUM → Review monthly
Score 5-8: HIGH → Active mitigation
Score 8-10: CRITICAL → Immediate action
```

### Document Automation

```python
# Register template
template = agent.doc_engine.register_template(
    name="Privacy Policy",
    template_type="policy",
    content_template="This Privacy Policy describes how {company} collects and processes personal data of {audience}.",
    variables=["company", "audience"],
)

# Generate document
doc = agent.doc_engine.generate_document(
    template["template_id"],
    {"company": "Acme Corp", "audience": "users"},
    author="legal-team",
)

# Approve
agent.doc_engine.approve_document(doc.document_id, "legal-director")
```

### Clause Library

```python
# Add standard clauses
agent.contract_manager.add_clause(
    title="Limitation of Liability",
    category="liability",
    content="In no event shall either party's total liability exceed the fees paid in the preceding 12 months.",
    risk_level=RiskLevel.MEDIUM,
    jurisdiction="US",
)

# Search clauses
clauses = agent.contract_manager.search_clauses(
    category="liability",
    jurisdiction="US",
    max_risk=RiskLevel.MEDIUM,
)
```

## Data Models

### Contract
| Field | Type | Description |
|-------|------|-------------|
| contract_id | str | Unique identifier |
| contract_type | ContractType | NDA, SOW, EMPLOYMENT, etc. |
| status | ContractStatus | DRAFT → ACTIVE → EXPIRED |
| parties | List[str] | Contract parties |
| value | float | Contract value ($) |
| expiration_date | datetime | End date |

### ComplianceRegulation
| Field | Type | Description |
|-------|------|-------------|
| regulation_id | str | Unique identifier |
| category | RegulationCategory | DATA_PRIVACY, FINANCIAL, etc. |
| jurisdiction | str | Applicable jurisdiction |
| compliance_score | float | Current compliance score (0-100) |

### LegalRisk
| Field | Type | Description |
|-------|------|-------------|
| risk_id | str | Unique identifier |
| risk_level | RiskLevel | LOW, MEDIUM, HIGH, CRITICAL |
| probability | float | Likelihood (0-1) |
| impact_score | float | Impact severity (0-10) |
| risk_score | float | probability × impact |

## Checklists

### Contract Creation
- [ ] Identify contract type and parties
- [ ] Select appropriate template
- [ ] Customize terms and clauses
- [ ] Review for legal compliance
- [ ] Route for internal approval
- [ ] Send for counterparty review
- [ ] Track negotiation changes
- [ ] Execute and archive

### Compliance Setup
- [ ] Identify applicable regulations
- [ ] Map requirements to controls
- [ ] Assess current compliance state
- [ ] Identify gaps
- [ ] Create remediation plan
- [ ] Assign responsible parties
- [ ] Set audit schedule
- [ ] Configure monitoring

### IP Protection
- [ ] Search existing marks
- [ ] File application
- [ ] Track examination status
- [ ] Respond to office actions
- [ ] Register upon approval
- [ ] Set renewal reminders
- [ ] Monitor for infringement
- [ ] Maintain portfolio records

## Troubleshooting

### Contract Stuck in Review
- Check if all required reviewers have been added
- Verify approval workflow is correct
- Review for missing information
- Check for conflicting terms with existing contracts

### Compliance Score Not Improving
- Verify evidence has been uploaded
- Check requirement status updates
- Review gap remediation progress
- Ensure controls are properly mapped

### Risk Scores Seem Inaccurate
- Review probability and impact assessments
- Check if risk factors have changed
- Verify owner has updated status
- Consider external factors not yet captured

### Document Generation Failing
- Verify template variables are provided
- Check template syntax for errors
- Ensure all required fields are populated
- Review document approval workflow

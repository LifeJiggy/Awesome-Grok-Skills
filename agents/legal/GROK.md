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

The Legal Agent provides a complete legal operations platform for corporate legal departments, startups, and organizations navigating complex regulatory environments. It automates contract lifecycle management, compliance monitoring across multiple frameworks, intellectual property portfolio protection, legal risk assessment, and document generation.

---

## Core Principles

1. **Risk-First Thinking**: Every legal decision considers risk exposure and mitigation.
2. **Compliance is Non-Negotiable**: Regulatory requirements are tracked and enforced.
3. **IP is an Asset**: Intellectual property is managed proactively, not reactively.
4. **Audit Trail Matters**: Every action is logged for accountability and review.
5. **Automation with Judgment**: Automate routine work, escalate complex decisions.

---

## Capabilities

### 1. Contract Lifecycle Management

Generate, track, and manage contracts through their complete lifecycle.

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
# → NDA: CON-A1B2C3D4 -> draft

# Create complex contract
contract = agent.contract_manager.create_contract(
    title="Cloud Services Agreement",
    contract_type=ContractType.SERVICE_LEVEL,
    parties=["Acme Corp", "CloudProvider Inc"],
    value=50000,
    governing_law="California",
    terms={"uptime_sla": "99.9%", "support_response": "4 hours"},
)
print(f"Contract: {contract.contract_id}")
# → Contract: CON-E5F6G7H8

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
| Service Level | Uptime SLA, penalties | $10K-$500K |
| Partnership | Revenue share, IP | Varies |

**Contract States:**

| State | Description | Next States |
|-------|-------------|-------------|
| DRAFT | Initial creation | UNDER_REVIEW |
| UNDER_REVIEW | Legal review in progress | NEGOTIATION, DRAFT |
| NEGOTIATION | Counterparty review | APPROVED, UNDER_REVIEW |
| APPROVED | Ready for execution | EXECUTED |
| EXECUTED | Signed by all parties | ACTIVE |
| ACTIVE | In force | EXPIRED, RENEWED, TERMINATED |
| EXPIRED | Past end date | None |
| TERMINATED | Early termination | None |

---

### 2. Compliance Monitoring

Track and assess compliance across multiple regulatory frameworks.

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

**Compliance Levels:**

| Score | Level | Action |
|-------|-------|--------|
| 90-100 | EXCELLENT | Maintain current controls |
| 70-89 | GOOD | Address identified gaps |
| 50-69 | NEEDS IMPROVEMENT | Priority remediation |
| 0-49 | CRITICAL | Immediate action required |

**Supported Regulations:**

| Regulation | Jurisdiction | Category | Penalties |
|------------|--------------|----------|-----------|
| GDPR | EU | Data Privacy | Up to 4% turnover |
| CCPA | California | Data Privacy | $2,500-$7,500/violation |
| SOC2 | Global | Security | Loss of certification |
| HIPAA | US | Health | $100-$50,000/violation |
| PCI-DSS | Global | Financial | $5,000-$100,000/month |
| SOX | US | Financial | Fines + criminal |
| ISO 27001 | Global | Security | Loss of certification |

---

### 3. IP Protection

Manage trademarks, copyrights, and intellectual property portfolio.

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

**Trademark Lifecycle:**
```
APPLICATION → PENDING → REGISTERED → ACTIVE → EXPIRATION
                         │
                    OPPOSED → CANCELLED
```

**IP Asset Types:**

| Type | Protection | Duration | Renewal |
|------|------------|----------|---------|
| Trademark | Brand names, logos | 10 years | Every 10 years |
| Copyright | Creative works | Life + 70 years | Not renewable |
| Patent | Inventions | 20 years | Not renewable |
| Trade Secret | Confidential info | Indefinite | Ongoing |

**Portfolio Health Indicators:**

| Indicator | Healthy | Warning | Critical |
|-----------|---------|---------|----------|
| Expiring within 6 months | < 5% | 5-15% | > 15% |
| Pending applications | < 10% | 10-25% | > 25% |
| Jurisdiction coverage | > 90% | 70-90% | < 70% |

---

### 4. Risk Assessment

Identify, score, and track legal risks with probability-impact methodology.

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

**Risk Categories:**

| Category | Examples | Typical Impact |
|----------|----------|----------------|
| CONTRACTUAL | Breach, non-performance | Financial, operational |
| REGULATORY | Non-compliance, fines | Financial, reputational |
| LITIGATION | Lawsuits, claims | Financial, reputational |
| IP | Infringement, theft | Competitive, financial |
| OPERATIONAL | Process failures | Operational, financial |

**Risk Heat Map:**

```
Impact
  10 │ CRITICAL │ CRITICAL │ CRITICAL │ CRITICAL │ CRITICAL │
   8 │   HIGH   │ CRITICAL │ CRITICAL │ CRITICAL │ CRITICAL │
   6 │   HIGH   │   HIGH   │ CRITICAL │ CRITICAL │ CRITICAL │
   4 │  MEDIUM  │   HIGH   │   HIGH   │ CRITICAL │ CRITICAL │
   2 │   LOW    │  MEDIUM  │  MEDIUM  │   HIGH   │   HIGH   │
      0.0-0.2   0.2-0.4   0.4-0.6   0.6-0.8   0.8-1.0
                        Probability
```

---

### 5. Document Automation

Generate legal documents from templates with variable substitution and approval workflows.

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

**Document Types:**

| Type | Variables | Approval |
|------|-----------|----------|
| NDA | party_a, party_b, duration | Legal review |
| SOW | deliverables, timeline | Legal + Finance |
| Privacy Policy | company, audience | Legal + DPO |
| Terms of Service | company, service | Legal |
| Employment Agreement | employee, compensation | Legal + HR |
| Vendor Agreement | vendor, scope | Legal + Procurement |

**Document States:**

| State | Description |
|-------|-------------|
| DRAFT | Initial generation |
| UNDER_REVIEW | Review in progress |
| APPROVED | Ready for use |
| PUBLISHED | Active document |
| ARCHIVED | No longer active |

---

### 6. Clause Library

Manage standard and custom clauses with risk classification.

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

**Clause Risk Levels:**

| Risk | Description | Review Required |
|------|-------------|-----------------|
| LOW | Standard, pre-approved | Optional |
| MEDIUM | Acceptable with modifications | Recommended |
| HIGH | Requires legal review | Mandatory |
| CRITICAL | Non-standard, significant exposure | Executive approval |

---

## Data Models

### Contract

| Field | Type | Description |
|-------|------|-------------|
| contract_id | str | Unique identifier (CON-{hash}) |
| title | str | Contract title |
| contract_type | ContractType | NDA, SOW, EMPLOYMENT, etc. |
| status | ContractStatus | DRAFT → ACTIVE → EXPIRED |
| parties | List[str] | Contract parties |
| value | float | Contract value ($) |
| governing_law | str | Applicable jurisdiction |
| effective_date | datetime | Start date |
| expiration_date | datetime | End date |
| renewal_date | datetime | Renewal deadline |
| auto_renew | bool | Auto-renewal flag |

### ComplianceRegulation

| Field | Type | Description |
|-------|------|-------------|
| regulation_id | str | Unique identifier (REG-{hash}) |
| name | str | Regulation name |
| category | RegulationCategory | DATA_PRIVACY, FINANCIAL, etc. |
| jurisdiction | str | Applicable jurisdiction |
| compliance_score | float | Current score (0-100) |
| total_requirements | int | Number of requirements |
| compliant_count | int | Compliant requirements |

### ComplianceRequirement

| Field | Type | Description |
|-------|------|-------------|
| requirement_id | str | Unique identifier |
| regulation_id | str | Parent regulation |
| title | str | Requirement title |
| description | str | Detailed description |
| is_mandatory | bool | Mandatory requirement |
| status | ComplianceStatus | COMPLIANT, PARTIAL, NON_COMPLIANT |
| evidence | List[str] | Supporting documents |
| priority | RiskLevel | LOW, MEDIUM, HIGH, CRITICAL |

### Trademark

| Field | Type | Description |
|-------|------|-------------|
| trademark_id | str | Unique identifier (TM-{hash}) |
| name | str | Trademark name |
| owner | str | Owner entity |
| jurisdiction | str | Registration jurisdiction |
| status | TrademarkStatus | APPLICATION, PENDING, REGISTERED, ACTIVE, EXPIRED |
| nice_classes | List[int] | Nice classification codes |
| registration_number | str | Official registration number |
| filing_date | datetime | Application filing date |
| registration_date | datetime | Registration date |
| expiration_date | datetime | Expiration date |

### LegalRisk

| Field | Type | Description |
|-------|------|-------------|
| risk_id | str | Unique identifier (RISK-{hash}) |
| title | str | Risk title |
| description | str | Detailed description |
| category | str | Risk category |
| risk_level | RiskLevel | LOW, MEDIUM, HIGH, CRITICAL |
| probability | float | Likelihood (0-1) |
| impact_score | float | Impact severity (0-10) |
| risk_score | float | probability × impact |
| owner | str | Responsible party |
| mitigations | List[str] | Mitigation strategies |
| status | RiskStatus | OPEN, MITIGATED, ACCEPTED, CLOSED |

---

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
- [ ] Set renewal reminders
- [ ] Link to compliance requirements

### Compliance Setup
- [ ] Identify applicable regulations
- [ ] Map requirements to controls
- [ ] Assess current compliance state
- [ ] Identify gaps
- [ ] Create remediation plan
- [ ] Assign responsible parties
- [ ] Set audit schedule
- [ ] Configure monitoring
- [ ] Document evidence collection
- [ ] Establish reporting cadence

### IP Protection
- [ ] Search existing marks
- [ ] File application
- [ ] Track examination status
- [ ] Respond to office actions
- [ ] Register upon approval
- [ ] Set renewal reminders
- [ ] Monitor for infringement
- [ ] Maintain portfolio records
- [ ] Cover key jurisdictions
- [ ] Review portfolio annually

### Risk Assessment
- [ ] Identify risk sources
- [ ] Assess probability
- [ ] Evaluate impact
- [ ] Calculate risk score
- [ ] Assign owner
- [ ] Develop mitigation plan
- [ ] Set review schedule
- [ ] Track mitigation progress
- [ ] Escalate critical risks
- [ ] Document decisions

### Document Automation
- [ ] Define template variables
- [ ] Create document template
- [ ] Set approval workflow
- [ ] Test variable substitution
- [ ] Validate output format
- [ ] Configure version control
- [ ] Set access permissions
- [ ] Establish review cycle

---

## Troubleshooting

### Contract Stuck in Review
- Check if all required reviewers have been added
- Verify approval workflow is correct
- Review for missing information
- Check for conflicting terms with existing contracts
- Verify contract value threshold for approval level
- Check reviewer availability and workload

### Compliance Score Not Improving
- Verify evidence has been uploaded
- Check requirement status updates
- Review gap remediation progress
- Ensure controls are properly mapped
- Verify evidence meets requirement criteria
- Check for new requirements added

### Risk Scores Seem Inaccurate
- Review probability and impact assessments
- Check if risk factors have changed
- Verify owner has updated status
- Consider external factors not yet captured
- Review historical risk data
- Validate scoring methodology

### Document Generation Failing
- Verify template variables are provided
- Check template syntax for errors
- Ensure all required fields are populated
- Review document approval workflow
- Check template version compatibility
- Verify output format requirements

### IP Expiration Missed
- Check expiration warning settings
- Verify notification recipients
- Review monitoring schedule
- Check jurisdiction coverage
- Validate renewal calendar integration
- Audit reminder escalation process

---

## Configuration

```python
agent = LegalAgent(config={
    "default_jurisdiction": "US",
    "renewal_notice_days": 60,
    "auto_renew_default": False,
    "compliance_assessment_frequency": "quarterly",
    "risk_review_frequency": "monthly",
    "ip_expiration_warning_days": 180,
    "document_approval_timeout_days": 7,
    "audit_retention_years": 7,
})
```

### Configuration Reference

| Parameter | Default | Description |
|-----------|---------|-------------|
| default_jurisdiction | US | Default legal jurisdiction |
| renewal_notice_days | 60 | Days before renewal to alert |
| auto_renew_default | False | Default auto-renewal setting |
| compliance_assessment_frequency | quarterly | How often to assess compliance |
| risk_review_frequency | monthly | How often to review risks |
| ip_expiration_warning_days | 180 | Days before IP expiration to warn |
| document_approval_timeout_days | 7 | Days before approval timeout |
| audit_retention_years | 7 | Years to retain audit records |

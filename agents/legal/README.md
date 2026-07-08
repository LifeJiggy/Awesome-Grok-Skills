# Legal Agent

> Legal operations platform covering contract lifecycle management, compliance monitoring, IP protection, risk assessment, and document automation.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Security](#security)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)
- [License](#license)

## Overview

The Legal Agent automates and streamlines legal operations across contract management, compliance tracking, intellectual property protection, risk assessment, and document generation. Built for corporate legal departments, startups building legal infrastructure, and organizations navigating GDPR, CCPA, SOC2, HIPAA, and industry-specific regulations.

Whether you're managing a portfolio of vendor contracts, ensuring GDPR compliance, protecting your brand trademarks, assessing legal risks, or generating standard legal documents, the Legal Agent provides the tools to manage your legal operations efficiently and consistently.

## Features

### Contract Management
- Full lifecycle: Draft → Under Review → Negotiation → Approved → Executed → Active
- NDA generation with customizable terms
- Clause library with risk classification
- Renewal tracking with configurable notice periods
- Contract value and party management
- Multi-jurisdiction support

### Compliance Monitoring
- Multi-regulation tracking (GDPR, CCPA, SOC2, HIPAA, etc.)
- Requirement assessment (compliant, partial, non-compliant)
- Gap analysis with priority ranking
- Audit workflow management
- Compliance scoring and reporting

### IP Protection
- Trademark lifecycle management
- Portfolio value calculation
- Expiration monitoring (6-month warning)
- Jurisdiction tracking
- Prior art search

### Risk Assessment
- Risk identification and scoring (probability × impact)
- Risk levels: LOW, MEDIUM, HIGH, CRITICAL
- Mitigation strategy tracking
- Owner assignment
- Risk register with filtering

### Document Automation
- Template-based document generation
- Variable substitution
- Approval workflow
- Version tracking
- Document inventory

### Audit & Reporting
- Complete audit trail for all operations
- Compliance reports by regulation
- Risk reports with heat maps
- Dashboard with key metrics

## Quick Start

### Installation

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Basic Usage

```python
from agents.legal.agent import LegalAgent, ContractType, RegulationCategory

agent = LegalAgent()

# Generate NDA
nda = agent.contract_manager.generate_nda(
    party_a="Acme Corp",
    party_b="Beta Inc",
    duration_years=2,
)
print(f"NDA: {nda.contract_id} -> {nda.status.value}")

# Register regulation
reg = agent.compliance_manager.register_regulation(
    name="GDPR",
    category=RegulationCategory.DATA_PRIVACY,
    jurisdiction="EU",
)

# Get dashboard
dashboard = agent.get_dashboard()
```

### Run the Demo

```bash
python agents/legal/agent.py
```

## Usage

### Contract Lifecycle

```python
# Create contract
contract = agent.contract_manager.create_contract(
    title="Cloud Services Agreement",
    contract_type=ContractType.SERVICE_LEVEL,
    parties=["Acme Corp", "CloudProvider Inc"],
    value=50000,
    governing_law="California",
)

# Advance through stages
agent.contract_manager.advance_contract(contract.contract_id)

# Check renewals
renewals = agent.contract_manager.check_renewals(within_days=90)
```

### Compliance Assessment

```python
# Add requirements
req = agent.compliance_manager.add_requirement(
    regulation_id=reg.regulation_id,
    title="Data Processing Agreement",
    description="Must have DPA with all data processors",
    evidence=["signed_dpa.pdf"],
)

# Assess compliance
assessment = agent.compliance_manager.assess_compliance(reg.regulation_id)
print(f"Score: {assessment['compliance_score']}%")

# Gap analysis
gaps = agent.compliance_manager.gap_analysis(reg.regulation_id)
print(f"Gaps: {gaps['total_gaps']}")
```

### IP Protection

```python
tm = agent.ip_manager.register_trademark(
    name="MyBrand",
    owner="Acme Corp",
    jurisdiction="US",
    nice_classes=[9, 42],
)

# Check expirations
expiring = agent.ip_manager.check_expirations(within_days=180)

# Portfolio overview
portfolio = agent.ip_manager.get_ip_portfolio()
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
    mitigations=["Encryption", "Incident response plan", "Cyber insurance"],
)

# Risk register
register = agent.risk_engine.get_risk_register()
```

### Document Automation

```python
template = agent.doc_engine.register_template(
    name="Privacy Policy",
    template_type="policy",
    content_template="This Privacy Policy describes how {company} processes data.",
    variables=["company"],
)

doc = agent.doc_engine.generate_document(
    template["template_id"],
    {"company": "Acme Corp"},
    author="legal-team",
)
agent.doc_engine.approve_document(doc.document_id, "legal-director")
```

## API Reference

### ContractManager

| Method | Description |
|--------|-------------|
| `create_contract(title, type, parties, **kw)` | Create contract |
| `generate_nda(party_a, party_b, years)` | Generate NDA |
| `advance_contract(contract_id)` | Advance lifecycle |
| `check_renewals(within_days)` | Check upcoming renewals |
| `add_clause(title, category, content, ...)` | Add to clause library |
| `search_clauses(category, jurisdiction, ...)` | Search clause library |

### ComplianceManager

| Method | Description |
|--------|-------------|
| `register_regulation(name, category, jurisdiction)` | Register regulation |
| `add_requirement(reg_id, title, desc, **kw)` | Add requirement |
| `assess_compliance(reg_id)` | Assess compliance |
| `gap_analysis(reg_id)` | Identify gaps |
| `run_audit(reg_id, auditor)` | Start audit |
| `close_audit(audit_id, findings, score)` | Close audit |

### IPProtectionManager

| Method | Description |
|--------|-------------|
| `register_trademark(name, owner, jurisdiction)` | Register trademark |
| `update_trademark_status(tm_id, status)` | Update status |
| `check_expirations(within_days)` | Check expirations |
| `get_ip_portfolio()` | Get portfolio overview |

### LegalRiskEngine

| Method | Description |
|--------|-------------|
| `identify_risk(title, desc, category, level, ...)` | Identify risk |
| `update_risk(risk_id, **kwargs)` | Update risk |
| `get_risk_register()` | Get risk register |
| `get_risk_heat_map()` | Get risk heat map |

### DocumentAutomationEngine

| Method | Description |
|--------|-------------|
| `register_template(name, type, content, vars)` | Register template |
| `generate_document(template_id, vars, author)` | Generate document |
| `approve_document(doc_id, approver)` | Approve document |
| `get_document_inventory()` | Get all documents |

## Examples

### NDA Workflow

```python
from agents.legal.agent import LegalAgent

agent = LegalAgent()

# Generate mutual NDA
nda = agent.contract_manager.generate_nda(
    party_a="Acme Corp",
    party_b="Beta Inc",
    duration_years=2,
    jurisdiction="US",
    nda_type="mutual",
)
print(f"NDA: {nda.contract_id}")

# Advance through lifecycle
agent.contract_manager.advance_contract(nda.contract_id)  # → UNDER_REVIEW
agent.contract_manager.advance_contract(nda.contract_id)  # → NEGOTIATION
agent.contract_manager.advance_contract(nda.contract_id)  # → APPROVED
agent.contract_manager.advance_contract(nda.contract_id)  # → EXECUTED
agent.contract_manager.advance_contract(nda.contract_id)  # → ACTIVE

# Check renewals
renewals = agent.contract_manager.check_renewals(within_days=90)
```

### GDPR Compliance Setup

```python
# Register GDPR
gdpr = agent.compliance_manager.register_regulation(
    name="GDPR",
    category=RegulationCategory.DATA_PRIVACY,
    jurisdiction="EU",
    description="General Data Protection Regulation",
)

# Add key requirements
requirements = [
    ("Data Processing Agreement", "Must have DPA with all processors", True),
    ("Privacy Policy", "Public privacy policy required", True),
    ("Consent Management", "User consent for data processing", True),
    ("Breach Notification", "72-hour breach notification", True),
    ("Data Subject Rights", "Process for DSAR requests", True),
]

for title, desc, mandatory in requirements:
    agent.compliance_manager.add_requirement(
        regulation_id=gdpr.regulation_id,
        title=title,
        description=desc,
        is_mandatory=mandatory,
    )

# Assess compliance
assessment = agent.compliance_manager.assess_compliance(gdpr.regulation_id)
print(f"GDPR Score: {assessment['compliance_score']}%")

# Run gap analysis
gaps = agent.compliance_manager.gap_analysis(gdpr.regulation_id)
for gap in gaps["gaps"]:
    print(f"Gap: {gap['title']} (Priority: {gap['priority']})")
```

### Risk Assessment

```python
# Identify risks
risks = [
    {
        "title": "Data Breach Liability",
        "description": "Potential liability from customer data breach",
        "category": "data_privacy",
        "risk_level": RiskLevel.HIGH,
        "probability": 0.3,
        "impact": 8.0,
        "mitigations": ["Encryption", "Incident response plan", "Cyber insurance"],
    },
    {
        "title": "Contract Breach",
        "description": "Risk of non-performance under SLA",
        "category": "contractual",
        "risk_level": RiskLevel.MEDIUM,
        "probability": 0.2,
        "impact": 5.0,
        "mitigations": ["Performance monitoring", "Escalation procedures"],
    },
]

for risk_data in risks:
    risk = agent.risk_engine.identify_risk(**risk_data)
    print(f"Risk: {risk.title} (Score: {risk.risk_score})")

# Get risk register
register = agent.risk_engine.get_risk_register()
print(f"Total risks: {register['total_risks']}")
```

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

## Architecture

For detailed architecture documentation, see [ARCHITECTURE.md](./ARCHITECTURE.md).

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                       Legal Agent                           │
├─────────────┬─────────────┬─────────────┬──────────────────┤
│  Contract   │  Compliance │     IP      │     Risk         │
│  Management │  Management │  Protection │  Assessment      │
├─────────────┼─────────────┼─────────────┼──────────────────┤
│ - Lifecycle │ - Regulation│ - Trademark │ - Identification │
│ - Clauses   │ - Requiremt │ - Portfolio │ - Scoring        │
│ - Templates │ - Assessment│ - Expiration│ - Mitigation     │
│ - Renewals  │ - Gap Anlys │ - Prior Art │ - Register       │
├─────────────┴─────────────┴─────────────┴──────────────────┤
│                  Document Automation Layer                  │
│  - Templates  - Generation  - Approval  - Version Control  │
├─────────────────────────────────────────────────────────────┤
│                  Audit & Reporting Layer                    │
│  - Audit Trail  - Compliance Reports  - Risk Reports       │
└─────────────────────────────────────────────────────────────┘
```

## Security

- Confidentiality levels per contract (public, internal, confidential, restricted)
- Role-based access to legal documents and IP data
- Audit trail for all contract and compliance modifications
- Encrypted storage for sensitive legal documents
- Access logging for IP portfolio data
- Separation of duties for contract approval workflows

**Access Control:**

| Role | Contracts | Compliance | IP | Risk | Documents |
|------|-----------|------------|-----|------|-----------|
| Legal Admin | Full | Full | Full | Full | Full |
| Legal Counsel | Read/Write | Read/Write | Read | Read/Write | Read/Write |
| Paralegal | Read | Read | Read | Read | Read/Write |
| Business User | Read (own) | None | None | None | Read |
| Auditor | Read | Read | Read | Read | Read |

## Best Practices

### Contract Management
1. **Standardize contracts** — use templates and clause libraries
2. **Track renewals proactively** — don't let contracts auto-renew unknowingly
3. **Review high-risk clauses** — require legal review for critical terms
4. **Maintain version control** — track all contract modifications
5. **Link to compliance** — map contracts to regulatory requirements

### Compliance
6. **Assess compliance regularly** — regulations change frequently
7. **Document evidence** — maintain audit-ready documentation
8. **Prioritize gaps** — focus on mandatory requirements first
9. **Set review schedules** — quarterly assessments minimum
10. **Track remediation** — ensure gaps are addressed

### IP Protection
11. **Monitor expirations** — set 180-day warning alerts
12. **Cover key jurisdictions** — protect IP in operating markets
13. **Search before filing** — check for conflicts early
14. **Maintain portfolio records** — keep documentation current
15. **Review annually** — assess portfolio health

### Risk Assessment
16. **Score risks consistently** — use probability × impact framework
17. **Assign owners** — every risk needs a responsible party
18. **Track mitigations** — ensure actions are taken
19. **Escalate critical risks** — immediate attention for high scores
20. **Review regularly** — monthly risk register reviews

### Document Automation
21. **Use templates** — ensure consistency across documents
22. **Require approvals** — don't skip review steps
23. **Version control** — track document changes
24. **Test generation** — validate output before publishing
25. **Archive old versions** — maintain document history

## Troubleshooting

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Contract stuck in review | Missing reviewers, workflow issue | Check reviewer assignments, verify workflow |
| Compliance score not improving | Evidence not uploaded, status not updated | Upload evidence, update requirement status |
| Risk scores seem off | Outdated probability/impact, missing factors | Review assessments, update risk data |
| Document generation failing | Missing variables, template syntax error | Check variables, verify template format |
| IP expiration missed | Warning settings incorrect, notification failure | Check expiration warning days, verify alerts |
| Renewal alerts not received | Notice period too short, notification config | Increase notice days, check notification settings |
| Gap analysis incomplete | Requirements not fully mapped, evidence missing | Complete requirement mapping, upload evidence |
| Audit trail gaps | Operations not logged, retention too short | Verify logging, increase retention period |

## FAQ

**Q: How does the compliance scoring work?**
A: The score is calculated as `(compliant × 100 + partially_compliant × 50) / total_requirements`. A score of 100% means all requirements are fully compliant.

**Q: Can I customize the risk scoring formula?**
A: The default formula is `probability × impact_score`. You can customize the probability and impact scales, or implement alternative scoring methods.

**Q: How are contract renewals tracked?**
A: The system monitors active contracts and alerts you based on the configured notice period (default: 60 days). You can set custom notice periods per contract.

**Q: What happens when an IP asset expires?**
A: The system generates alerts at 180, 90, 60, and 30 days before expiration. You can customize the warning schedule.

**Q: Can I export compliance reports?**
A: Yes. The system generates compliance reports by regulation, including scores, gaps, and remediation status.

**Q: How do I handle multi-jurisdiction compliance?**
A: Register regulations by jurisdiction and link requirements to applicable contracts. The system tracks obligations across jurisdictions.

## License

MIT License - see LICENSE file for details.

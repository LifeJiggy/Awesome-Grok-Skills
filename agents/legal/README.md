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
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The Legal Agent automates and streamlines legal operations across contract management, compliance tracking, intellectual property protection, risk assessment, and document generation. Built for corporate legal departments, startups building legal infrastructure, and organizations navigating GDPR, CCPA, SOC2, HIPAA, and industry-specific regulations.

## Features

### Contract Management
- Full lifecycle: Draft → Under Review → Negotiation → Approved → Executed → Active
- NDA generation with customizable terms
- Clause library with risk classification
- Renewal tracking with configurable notice periods
- Contract value and party management

### Compliance Monitoring
- Multi-regulation tracking (GDPR, CCPA, SOC2, HIPAA, etc.)
- Requirement assessment (compliant, partial, non-compliant)
- Gap analysis with priority ranking
- Audit workflow management
- Compliance scoring

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

# Gap analysis
gaps = agent.compliance_manager.gap_analysis(reg.regulation_id)
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

### ComplianceManager

| Method | Description |
|--------|-------------|
| `register_regulation(name, category, jurisdiction)` | Register regulation |
| `add_requirement(reg_id, title, desc, **kw)` | Add requirement |
| `assess_compliance(reg_id)` | Assess compliance |
| `gap_analysis(reg_id)` | Identify gaps |
| `run_audit(reg_id, auditor)` | Start audit |

### IPProtectionManager

| Method | Description |
|--------|-------------|
| `register_trademark(name, owner, jurisdiction)` | Register trademark |
| `update_trademark_status(tm_id, status)` | Update status |
| `check_expirations(within_days)` | Check expirations |

### LegalRiskEngine

| Method | Description |
|--------|-------------|
| `identify_risk(title, desc, category, level, ...)` | Identify risk |
| `update_risk(risk_id, **kwargs)` | Update risk |
| `get_risk_register()` | Get risk register |

## Examples

See the full demo in `agent.py`.

## Configuration

```python
agent = LegalAgent(config={"default_jurisdiction": "US"})
```

## Best Practices

1. **Standardize contracts** — use templates and clause libraries
2. **Track renewals proactively** — don't let contracts auto-renew unknowingly
3. **Assess compliance regularly** — regulations change frequently
4. **Maintain IP portfolio** — monitor expirations and renewals
5. **Score risks consistently** — use probability × impact framework
6. **Audit trail everything** — legal actions need documentation

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Contract stuck in review | Check reviewer assignments and workflow |
| Compliance score not improving | Verify evidence uploads and status updates |
| Risk scores seem off | Review probability and impact assessments |
| Document generation failing | Check template variables and syntax |

## License

MIT License - see LICENSE file for details.

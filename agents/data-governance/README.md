# Data Governance Agent

> Comprehensive data governance — policies, quality, lineage, metadata, compliance, and stewardship.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.0.0-orange.svg)](CHANGELOG.md)

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Policy Management](#policy-management)
  - [Asset Management](#asset-management)
  - [Quality Management](#quality-management)
  - [Lineage Tracking](#lineage-tracking)
  - [Metadata Catalog](#metadata-catalog)
  - [Compliance Assessment](#compliance-assessment)
  - [Stewardship](#stewardship)
  - [Issue Management](#issue-management)
  - [Governance Scoring](#governance-scoring)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Data Governance Agent is a comprehensive system for managing enterprise data governance. It handles policy creation and enforcement, data quality profiling and monitoring, data lineage tracking, metadata catalog management, compliance assessment, and stewardship coordination.

Built for data teams, compliance officers, data stewards, and data architects who need a structured, auditable approach to enterprise data governance.

### What Makes This Agent Different

- **20 Policy Types**: Comprehensive policy coverage
- **10 Quality Dimensions**: Full quality profiling
- **15+ Quality Rule Types**: Flexible quality validation
- **18 Compliance Frameworks**: GDPR, SOC2, HIPAA, PCI, and more
- **Graph-based Lineage**: Impact analysis with upstream/downstream tracing
- **Business Glossary**: Centralized terminology management
- **Maturity Scoring**: Measure governance maturity across 6 dimensions
- **Audit Trail**: Every action logged for compliance

---

## Features

| Feature | Description |
|---------|-------------|
| Policy Management | Create, approve, enforce, and retire policies |
| Asset Registration | Register and catalog data assets |
| Quality Profiling | Profile quality across 10 dimensions |
| Quality Rules | 15+ rule types with thresholds and monitoring |
| Lineage Tracking | Graph-based lineage with impact analysis |
| Metadata Catalog | Centralized metadata with search and glossary |
| Compliance Assessment | 18 frameworks with scoring and findings |
| Stewardship | Assign stewards and track actions |
| Issue Management | Track and resolve governance issues |
| Governance Scoring | Maturity scoring across 6 dimensions |
| Export | JSON, CSV, Markdown, PDF formats |
| Audit Trail | Immutable operation logging |

---

## Quick Start

```python
from agents.data_governance.agent import DataGovernanceAgent, PolicyType, ComplianceFramework

# Initialize agent
agent = DataGovernanceAgent()

# Create policy
policy = agent.create_policy(name="Retention Policy", policy_type=PolicyType.DATA_RETENTION)
agent.approve_policy(policy.policy_id, "Data Governance Board")

# Register asset
asset = agent.register_asset(name="customers", classification=DataClassification.PII)

# Profile quality
profile = agent.profile_quality(asset.asset_id)
print(f"Quality: {profile.overall_score:.2%}")

# Calculate governance score
score = agent.calculate_governance_score()
print(f"Maturity: {score.maturity_level.value}")
```

### Run the Demo

```bash
python agents/data-governance/agent.py
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills

# No external dependencies required
# Python 3.10+ with standard library only
```

---

## Usage

### Policy Management

```python
from agents.data_governance.agent import DataGovernanceAgent, PolicyType, ComplianceFramework

agent = DataGovernanceAgent()

# Create policy
policy = agent.create_policy(
    name="Data Retention Policy",
    policy_type=PolicyType.DATA_RETENTION,
    description="Define retention periods for all data types",
    classification=DataClassification.INTERNAL,
    rules=[
        {"type": "retention_period", "data_type": "customer_data", "days": 2555},
        {"type": "retention_period", "data_type": "log_data", "days": 365},
    ],
    compliance_frameworks=[ComplianceFramework.GDPR, ComplianceFramework.SOC2],
)

# Approve policy
agent.approve_policy(policy.policy_id, "Data Governance Board")

# Check policies needing review
needs_review = agent.get_policies_needing_review()
```

### Asset Management

```python
# Register asset
asset = agent.register_asset(
    name="customers",
    asset_type=AssetType.TABLE,
    domain=DataDomain.CUSTOMER,
    classification=DataClassification.PII,
    owner="data-team",
    steward="john-doe",
    location="production.postgres.customers",
    tags=["customer", "pii", "production"],
)

# Search assets
results = agent.search_assets("customer")

# Filter by domain
customer_assets = agent.list_assets(domain=DataDomain.CUSTOMER)
```

### Quality Management

```python
# Create quality rule
rule = agent.create_quality_rule(
    name="Customer Email Not Null",
    rule_type=QualityRuleType.NOT_NULL,
    dimension=QualityDimension.COMPLETENESS,
    asset_id=asset.asset_id,
    column_name="email",
    threshold=0.99,
)

# Profile quality
profile = agent.profile_quality(asset.asset_id)
print(f"Quality: {profile.overall_score:.2%}")

# Run rules
results = agent.run_quality_rules(asset.asset_id)

# Get summary
summary = agent.get_quality_summary()
```

### Lineage Tracking

```python
# Track lineage
lineage = agent.track_lineage(
    source="raw_customers",
    target="cleaned_customers",
    change_type=ChangeType.TRANSFORMATION,
    description="ETL cleaning and deduplication",
)

# Impact analysis
impact = agent.impact_analysis("dim_customers")
print(f"Downstream: {impact['downstream_count']} assets")
print(f"Risk: {impact['risk_level']}")

# Trace dependencies
upstream = agent.trace_upstream("dim_customers")
downstream = agent.trace_downstream("dim_customers")
```

### Metadata Catalog

```python
# Create catalog
catalog = agent.create_catalog(name="Enterprise Data Catalog")

# Add metadata
agent.add_metadata(catalog.catalog_id, asset.asset_id, "description", "Master customer table")
agent.add_metadata(catalog.catalog_id, asset.asset_id, "sla", "99.9%", MetadataType.OPERATIONAL)

# Business glossary
agent.add_business_glossary(catalog.catalog_id, "Customer", "Any individual or organization that has purchased products or services")

# Search
results = agent.search_catalog(catalog.catalog_id, "customer")
```

### Compliance Assessment

```python
# Assess GDPR
assessment = agent.assess_compliance(
    framework=ComplianceFramework.GDPR,
    controls_assessed=50,
    controls_passed=45,
    controls_failed=5,
    findings=[
        {"control": "Art. 17 Right to Erasure", "status": "partial"},
    ],
    assessed_by="Compliance Officer",
)
print(f"GDPR: {assessment.status.value} (score: {assessment.score:.2%})")

# Get summary
summary = agent.get_compliance_summary()
```

### Stewardship

```python
steward = agent.assign_steward(
    name="John Doe",
    domain=DataDomain.CUSTOMER,
    assigned_assets=[asset.asset_id],
)
```

### Issue Management

```python
# Create issue
issue = agent.create_issue(
    title="Customer email validation failing",
    description="5% of records have invalid email formats",
    severity=IssueSeverity.HIGH,
    category="data_quality",
    asset_id=asset.asset_id,
    assigned_to="John Doe",
)

# Resolve
agent.resolve_issue(issue.issue_id, notes="Fixed validation regex")

# List open issues
open_issues = agent.list_issues(status=IssueStatus.OPEN)
```

### Governance Scoring

```python
score = agent.calculate_governance_score()
print(f"Overall Score: {score.overall_score:.2%}")
print(f"Maturity: {score.maturity_level.value}")
for dim, s in score.dimension_scores.items():
    print(f"  {dim}: {s:.2%}")
```

---

## API Reference

### DataGovernanceAgent

| Method | Description | Returns |
|--------|-------------|---------|
| `create_policy()` | Create governance policy | `DataPolicy` |
| `update_policy()` | Update policy | `DataPolicy` |
| `approve_policy()` | Approve policy | `DataPolicy` |
| `retire_policy()` | Retire policy | `DataPolicy` |
| `get_policy()` | Get policy by ID | `DataPolicy` |
| `list_policies()` | List all policies | `List[DataPolicy]` |
| `get_policies_needing_review()` | Get policies for review | `List[DataPolicy]` |
| `register_asset()` | Register data asset | `DataAsset` |
| `update_asset()` | Update asset | `DataAsset` |
| `get_asset()` | Get asset by ID | `DataAsset` |
| `list_assets()` | List all assets | `List[DataAsset]` |
| `search_assets()` | Search assets | `List[DataAsset]` |
| `delete_asset()` | Delete asset | `bool` |
| `create_quality_rule()` | Create quality rule | `QualityRule` |
| `profile_quality()` | Profile asset quality | `QualityProfile` |
| `run_quality_rules()` | Run quality rules | `Dict` |
| `get_quality_rules()` | Get quality rules | `List[QualityRule]` |
| `get_quality_summary()` | Get quality summary | `Dict` |
| `track_lineage()` | Track data lineage | `DataLineage` |
| `get_lineage()` | Get lineage by ID | `DataLineage` |
| `list_lineages()` | List all lineages | `List[DataLineage]` |
| `trace_upstream()` | Trace upstream deps | `List[Dict]` |
| `trace_downstream()` | Trace downstream | `List[Dict]` |
| `impact_analysis()` | Analyze impact | `Dict` |
| `create_catalog()` | Create metadata catalog | `MetadataCatalog` |
| `add_metadata()` | Add metadata entry | `MetadataEntry` |
| `search_catalog()` | Search catalog | `List[MetadataEntry]` |
| `get_catalog()` | Get catalog by ID | `MetadataCatalog` |
| `list_catalogs()` | List all catalogs | `List[MetadataCatalog]` |
| `add_business_glossary()` | Add glossary term | `None` |
| `get_business_glossary()` | Get glossary | `Dict` |
| `assess_compliance()` | Assess compliance | `ComplianceAssessment` |
| `get_assessment()` | Get assessment by ID | `ComplianceAssessment` |
| `list_assessments()` | List assessments | `List[ComplianceAssessment]` |
| `get_compliance_summary()` | Get compliance summary | `Dict` |
| `assign_steward()` | Assign data steward | `DataSteward` |
| `get_steward()` | Get steward by ID | `Optional[DataSteward]` |
| `list_stewards()` | List all stewards | `List[DataSteward]` |
| `create_issue()` | Create governance issue | `GovernanceIssue` |
| `resolve_issue()` | Resolve issue | `GovernanceIssue` |
| `get_issue()` | Get issue by ID | `GovernanceIssue` |
| `list_issues()` | List all issues | `List[GovernanceIssue]` |
| `calculate_governance_score()` | Calculate score | `GovernanceScore` |
| `get_status()` | Get agent status | `Dict` |
| `get_operation_log()` | Get operation log | `List[Dict]` |
| `clear_cache()` | Clear cache | `int` |
| `export_data()` | Export all data | `str` |

---

## Examples

### Example 1: Full Governance Setup

```python
agent = DataGovernanceAgent()

# Policies
agent.create_policy(name="Retention", policy_type=PolicyType.DATA_RETENTION, ...)
agent.create_policy(name="Access", policy_type=PolicyType.ACCESS_CONTROL, ...)

# Assets
agent.register_asset(name="customers", classification=DataClassification.PII, ...)
agent.register_asset(name="orders", classification=DataClassification.CONFIDENTIAL, ...)

# Quality
agent.create_quality_rule(name="Email Not Null", rule_type=QualityRuleType.NOT_NULL, ...)
agent.profile_quality(asset_id="asset-123")

# Lineage
agent.track_lineage(source="raw", target="cleaned", ...)

# Compliance
agent.assess_compliance(framework=ComplianceFramework.GDPR, ...)

# Score
score = agent.calculate_governance_score()
print(f"Maturity: {score.maturity_level.value}")
```

### Example 2: Quality Monitoring

```python
for asset in agent.list_assets():
    profile = agent.profile_quality(asset.asset_id)
    if profile.overall_score < 0.90:
        agent.create_issue(
            title=f"Low quality: {asset.name}",
            severity=IssueSeverity.HIGH,
            asset_id=asset.asset_id,
        )
```

### Example 3: Impact Analysis

```python
impact = agent.impact_analysis("dim_customers")
if impact["risk_level"] == "high":
    print(f"WARNING: {impact['downstream_count']} assets affected")
```

---

## Configuration

```python
from agents.data_governance.agent import Config, QualityConfig, ComplianceConfig

config = Config(
    agent_name="MyGovernanceAgent",
    default_classification=DataClassification.INTERNAL,
    default_retention_days=2555,
    quality=QualityConfig(
        default_quality_threshold=0.95,
        alert_threshold=0.90,
    ),
    compliance=ComplianceConfig(
        frameworks=[ComplianceFramework.GDPR, ComplianceFramework.SOC2],
        assessment_frequency_days=90,
    ),
)

agent = DataGovernanceAgent(config=config)
```

---

## Best Practices

### Policy Management

1. **Create policies for all governance areas** — don't leave gaps
2. **Review quarterly** — keep policies current
3. **Enforce consistently** — exceptions need formal process
4. **Document exceptions** — track and justify
5. **Communicate changes** — notify stakeholders

### Quality Management

1. **Profile new assets immediately** — baseline quality
2. **Set rules before production** — prevent issues
3. **Monitor continuously** — catch degradation
4. **Alert on thresholds** — 90% warning, 80% critical
5. **Remediate promptly** — address issues quickly

### Lineage Management

1. **Track all transformations** — no undocumented changes
2. **Impact analysis before changes** — assess downstream
3. **Cross-system tracking** — end-to-end lineage
4. **Historical tracking** — audit trail
5. **Visualize lineage** — make it accessible

### Compliance Management

1. **Assess regularly** — quarterly at minimum
2. **Collect evidence** — automated where possible
3. **Track findings** — remediation plans
4. **Report to leadership** — regular updates
5. **Update for new regulations** — stay current

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Low governance score | Missing ownership | Assign owners/stewards |
| Quality below threshold | Data issues | Create rules, remediate |
| Compliance non-compliant | Missing controls | Review findings, remediate |
| No lineage | Not tracked | Track all transformations |
| Missing metadata | Not cataloged | Add metadata entries |

---

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

---

## License

MIT License - see [LICENSE](../../LICENSE).

---

*Data Governance Agent v3.0.0 — Part of the Awesome Grok Skills collection.*

*Last updated: 2026-07-06*

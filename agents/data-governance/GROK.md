---
name: data-governance
version: 3.0.0
description: Comprehensive data governance agent — data policies, quality standards, lineage tracking, metadata management, compliance frameworks, stewardship coordination, and governance scoring for enterprise data management.
author: Awesome Grok Skills Team
tags:
  - data-governance
  - data-quality
  - data-lineage
  - metadata
  - compliance
  - gdpr
  - soc2
  - hipaa
  - data-policy
  - data-stewardship
category: Data & Analytics
personality: Methodical, audit-minded, detail-oriented, compliance-focused, driven by data quality and transparency
use_cases:
  - Creating and enforcing data policies
  - Profiling and monitoring data quality
  - Tracking data lineage across systems
  - Managing metadata catalogs
  - Assessing compliance with frameworks
  - Coordinating data stewardship
  - Calculating governance maturity scores
  - Managing governance issues
---

# Data Governance Agent

> THE definitive agent for enterprise data governance — policies, quality, lineage, metadata,
> compliance, stewardship, and governance scoring.
> Enterprise-grade, auditable, and deeply structured.

---

## Table of Contents

1. [Agent Identity](#agent-identity)
2. [Core Principles](#core-principles)
3. [Capabilities](#capabilities)
4. [Operational Guidelines](#operational-guidelines)
5. [Method Signatures](#method-signatures)
6. [Usage Patterns](#usage-patterns)
7. [Data Models](#data-models)
8. [Checklists](#checklists)
9. [Troubleshooting](#troubleshooting)

---

## Agent Identity

The Data Governance Agent manages the full data governance lifecycle — from policy creation and enforcement through data quality management, lineage tracking, metadata cataloging, compliance assessment, and stewardship coordination.

### What It Does

- Creates and manages data governance policies (20 types)
- Profiles data quality across 10 dimensions
- Tracks data lineage with impact analysis
- Maintains metadata catalogs with business glossary
- Assesses compliance across 18 frameworks
- Coordinates data stewardship activities
- Calculates governance maturity scores
- Manages governance issues and remediation

### What It Does NOT Do

- Does not directly query databases (manages governance metadata)
- Does not replace data quality tools (provides governance layer)
- Does not enforce technical controls (creates policy requirements)
- Does not replace compliance tools (provides assessment framework)

---

## Core Principles

### 1. Policy-First Governance
Every data decision should be governed by a documented policy. No exceptions without formal exception process.

### 2. Quality as a Requirement
Data quality is not optional. Every asset must meet minimum quality standards for its classification.

### 3. Lineage Transparency
Every data transformation must be documented. If you can't trace it, you can't trust it.

### 4. Metadata Completeness
Assets without metadata are invisible. Every asset must have owner, steward, classification, and description.

### 5. Compliance by Design
Compliance is built into processes, not bolted on. Frameworks guide architecture and operations.

### 6. Stewardship Accountability
Data stewards are accountable for their domains. Assign ownership, track actions, measure outcomes.

### 7. Continuous Improvement
Governance maturity is a journey. Measure, identify gaps, remediate, and repeat.

---

## Capabilities

### 1. Policy Management

Create, approve, and manage data governance policies.

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
agent.approve_policy(policy.policy_id, "Data Governance Board")
print(f"Policy: {policy.name} ({policy.status.value})")

# Check for policies needing review
needs_review = agent.get_policies_needing_review()
print(f"Policies needing review: {len(needs_review)}")
```

**Policy Types (20):**
- Data Retention, Classification, Access Control, Encryption
- Privacy, Sharing, Backup, Disposal
- Quality, Lineage, Master Data, Reference Data
- Sensitive Data, Cross-Border, Consent, Breach Notification
- Vendor, Audit, Training, Exception

### 2. Asset Management

Register and manage data assets in the governance catalog.

```python
# Register assets
customers = agent.register_asset(
    name="customers",
    asset_type=AssetType.TABLE,
    domain=DataDomain.CUSTOMER,
    classification=DataClassification.PII,
    owner="data-team",
    steward="john-doe",
    location="production.postgres.customers",
    tags=["customer", "pii", "production"],
)

orders = agent.register_asset(
    name="orders",
    asset_type=AssetType.TABLE,
    domain=DataDomain.SALES,
    classification=DataClassification.CONFIDENTIAL,
)

# Search assets
results = agent.search_assets("customer")
print(f"Found {len(results)} assets matching 'customer'")

# Filter by domain
customer_assets = agent.list_assets(domain=DataDomain.CUSTOMER)
```

**Asset Types (20):**
- Database, Table, View, File, API, Stream
- Report, Dashboard, Model, Dataset
- Schema, Column, Index, Stored Procedure
- ETL Job, Pipeline, Service, Queue, Cache, Lake

### 3. Quality Management

Profile data quality and manage quality rules.

```python
# Create quality rule
rule = agent.create_quality_rule(
    name="Customer Email Not Null",
    rule_type=QualityRuleType.NOT_NULL,
    dimension=QualityDimension.COMPLETENESS,
    asset_id=customers.asset_id,
    column_name="email",
    threshold=0.99,
)

# Profile quality
profile = agent.profile_quality(customers.asset_id)
print(f"Quality Score: {profile.overall_score:.2%}")
for dim, score in profile.dimension_scores.items():
    print(f"  {dim}: {score:.2%}")

# Run rules
results = agent.run_quality_rules(customers.asset_id)
print(f"Rules: {results['total_rules']}, Passed: {results['passed']}")

# Quality summary
summary = agent.get_quality_summary()
print(f"Average quality: {summary['average_quality_score']:.2%}")
```

**Quality Dimensions (10):**
- Accuracy, Completeness, Consistency, Timeliness
- Validity, Uniqueness, Integrity, Conformity
- Freshness, Reasonableness

**Quality Rule Types (15):**
- NOT_NULL, UNIQUE, RANGE, PATTERN, REFERENTIAL
- CUSTOM, FRESHNESS, VOLUME, SCHEMA, STATISTICAL
- BUSINESS_RULE, COMPARISON, AGGREGATE, COMPLETENESS, CONSISTENCY

### 4. Lineage Tracking

Track data flow and analyze impact of changes.

```python
# Track lineage
lineage1 = agent.track_lineage(
    source="raw_customers",
    target="cleaned_customers",
    change_type=ChangeType.TRANSFORMATION,
    description="ETL cleaning and deduplication",
)
lineage2 = agent.track_lineage(
    source="cleaned_customers",
    target="dim_customers",
    change_type=ChangeType.TRANSFORMATION,
)

# Impact analysis
impact = agent.impact_analysis("dim_customers")
print(f"Downstream: {impact['downstream_count']} assets")
print(f"Impact score: {impact['impact_score']:.2f}")
print(f"Risk: {impact['risk_level']}")

# Trace dependencies
upstream = agent.trace_upstream("dim_customers")
downstream = agent.trace_downstream("dim_customers")
```

### 5. Metadata Catalog

Manage metadata and business glossary.

```python
# Create catalog
catalog = agent.create_catalog(name="Enterprise Data Catalog")

# Add metadata
agent.add_metadata(catalog.catalog_id, customers.asset_id, "description", "Master customer table")
agent.add_metadata(catalog.catalog_id, customers.asset_id, "sla", "99.9%", MetadataType.OPERATIONAL)

# Business glossary
agent.add_business_glossary(catalog.catalog_id, "Customer", "Any individual or organization that has purchased products or services")
glossary = agent.get_business_glossary(catalog.catalog_id)

# Search
results = agent.search_catalog(catalog.catalog_id, "customer")
```

### 6. Compliance Assessment

Assess compliance across multiple frameworks.

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

# Compliance summary
summary = agent.get_compliance_summary()
print(f"Frameworks compliant: {summary['frameworks_compliant']}")
```

**Supported Frameworks (18):**
- GDPR, CCPA, HIPAA, SOX, SOC2, PCI DSS
- ISO 27001, ISO 27701, NIST CSF, FedRAMP
- COPPA, GLBA, FERPA, Basel III, MiFID II
- LGPD, PIPEDA, APPs

### 7. Stewardship

Coordinate data stewardship activities.

```python
# Assign steward
steward = agent.assign_steward(
    name="John Doe",
    domain=DataDomain.CUSTOMER,
    assigned_assets=[customers.asset_id],
)
print(f"Steward: {steward.name} ({steward.domain.value})")
```

### 8. Issue Management

Track and resolve governance issues.

```python
# Create issue
issue = agent.create_issue(
    title="Customer email validation failing",
    description="5% of records have invalid email formats",
    severity=IssueSeverity.HIGH,
    category="data_quality",
    asset_id=customers.asset_id,
    assigned_to="John Doe",
)

# Resolve
agent.resolve_issue(issue.issue_id, notes="Fixed validation regex")

# List open issues
open_issues = agent.list_issues(status=IssueStatus.OPEN)
```

### 9. Governance Scoring

Calculate overall governance maturity.

```python
score = agent.calculate_governance_score()
print(f"Overall Score: {score.overall_score:.2%}")
print(f"Maturity: {score.maturity_level.value}")
for dim, s in score.dimension_scores.items():
    print(f"  {dim}: {s:.2%}")
```

**Maturity Levels:**

| Level | Score | Description |
|-------|-------|-------------|
| Initial | <40% | Ad-hoc, no formal process |
| Developing | 40-59% | Some processes defined |
| Defined | 60-74% | Standardized processes |
| Managed | 75-89% | Measured and controlled |
| Optimized | ≥90% | Continuous improvement |

---

## Operational Guidelines

### Policy Management

1. **Create policies for all governance areas** — don't leave gaps
2. **Review policies quarterly** — keep them current
3. **Enforce consistently** — exceptions need formal process
4. **Document exceptions** — track and justify
5. **Communicate changes** — notify stakeholders

### Quality Management

1. **Profile new assets immediately** — baseline quality
2. **Set rules before production** — prevent issues
3. **Monitor continuously** — catch degradation early
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

## Method Signatures

### Policy Methods

```python
def create_policy(self, name: str, policy_type: PolicyType, ...) -> DataPolicy
def update_policy(self, policy_id: str, **kwargs) -> DataPolicy
def approve_policy(self, policy_id: str, approver: str) -> DataPolicy
def retire_policy(self, policy_id: str) -> DataPolicy
def get_policy(self, policy_id: str) -> DataPolicy
def list_policies(self, status: Optional[PolicyStatus] = None) -> List[DataPolicy]
def get_policies_needing_review(self) -> List[DataPolicy]
```

### Asset Methods

```python
def register_asset(self, name: str, ...) -> DataAsset
def update_asset(self, asset_id: str, **kwargs) -> DataAsset
def get_asset(self, asset_id: str) -> DataAsset
def list_assets(self, domain: Optional[DataDomain] = None, ...) -> List[DataAsset]
def search_assets(self, query: str) -> List[DataAsset]
def delete_asset(self, asset_id: str) -> bool
```

### Quality Methods

```python
def create_quality_rule(self, name: str, rule_type: QualityRuleType, ...) -> QualityRule
def profile_quality(self, asset_id: str) -> QualityProfile
def run_quality_rules(self, asset_id: str) -> Dict[str, Any]
def get_quality_rules(self, asset_id: Optional[str] = None) -> List[QualityRule]
def get_quality_summary(self) -> Dict[str, Any]
```

### Lineage Methods

```python
def track_lineage(self, source: str, target: str, ...) -> DataLineage
def get_lineage(self, lineage_id: str) -> DataLineage
def list_lineages(self) -> List[DataLineage]
def trace_upstream(self, asset_name: str) -> List[Dict]
def trace_downstream(self, asset_name: str) -> List[Dict]
def impact_analysis(self, asset_name: str) -> Dict[str, Any]
```

### Metadata Methods

```python
def create_catalog(self, name: str, description: str = "") -> MetadataCatalog
def add_metadata(self, catalog_id: str, asset_id: str, key: str, value: Any, ...) -> MetadataEntry
def search_catalog(self, catalog_id: str, query: str) -> List[MetadataEntry]
def get_catalog(self, catalog_id: str) -> MetadataCatalog
def list_catalogs(self) -> List[MetadataCatalog]
def add_business_glossary(self, catalog_id: str, term: str, definition: str) -> None
def get_business_glossary(self, catalog_id: str) -> Dict[str, str]
```

### Compliance Methods

```python
def assess_compliance(self, framework: ComplianceFramework, ...) -> ComplianceAssessment
def get_assessment(self, assessment_id: str) -> ComplianceAssessment
def list_assessments(self, framework: Optional[ComplianceFramework] = None) -> List[ComplianceAssessment]
def get_compliance_summary(self) -> Dict[str, Any]
```

### Stewardship & Issues

```python
def assign_steward(self, name: str, domain: DataDomain, ...) -> DataSteward
def get_steward(self, steward_id: str) -> Optional[DataSteward]
def list_stewards(self) -> List[DataSteward]
def create_issue(self, title: str, description: str, ...) -> GovernanceIssue
def resolve_issue(self, issue_id: str, notes: str = "") -> GovernanceIssue
def get_issue(self, issue_id: str) -> GovernanceIssue
def list_issues(self, status: Optional[IssueStatus] = None) -> List[GovernanceIssue]
```

### Governance & Status

```python
def calculate_governance_score(self) -> GovernanceScore
def get_status(self) -> Dict[str, Any]
def get_operation_log(self, limit: int = 50) -> List[Dict]
def clear_cache(self) -> int
def export_data(self, format: str = "json") -> str
```

---

## Usage Patterns

### Pattern 1: Full Governance Setup

```python
agent = DataGovernanceAgent()

# 1. Create policies
agent.create_policy(name="Retention Policy", policy_type=PolicyType.DATA_RETENTION, ...)
agent.create_policy(name="Access Policy", policy_type=PolicyType.ACCESS_CONTROL, ...)

# 2. Register assets
agent.register_asset(name="customers", classification=DataClassification.PII, ...)
agent.register_asset(name="orders", classification=DataClassification.CONFIDENTIAL, ...)

# 3. Create quality rules
agent.create_quality_rule(name="Email Not Null", rule_type=QualityRuleType.NOT_NULL, ...)

# 4. Profile quality
agent.profile_quality(asset_id="asset-123")

# 5. Track lineage
agent.track_lineage(source="raw", target="cleaned", ...)

# 6. Assess compliance
agent.assess_compliance(framework=ComplianceFramework.GDPR, ...)

# 7. Calculate score
score = agent.calculate_governance_score()
```

### Pattern 2: Quality Monitoring

```python
# Profile all assets
for asset in agent.list_assets():
    profile = agent.profile_quality(asset.asset_id)
    if profile.overall_score < 0.90:
        agent.create_issue(
            title=f"Low quality: {asset.name}",
            severity=IssueSeverity.HIGH,
            asset_id=asset.asset_id,
        )
```

### Pattern 3: Impact Analysis

```python
# Before changing an asset
impact = agent.impact_analysis("dim_customers")
if impact["risk_level"] == "high":
    print(f"WARNING: {impact['downstream_count']} assets affected")
    for downstream in impact["downstream_assets"]:
        print(f"  - {downstream}")
```

### Pattern 4: Compliance Audit

```python
# Assess all frameworks
for framework in ComplianceFramework:
    assessment = agent.assess_compliance(framework=framework, ...)
    if assessment.status == ComplianceStatus.NON_COMPLIANT:
        print(f"ALERT: {framework.value} non-compliant ({assessment.score:.0%})")
```

---

## Data Models

### DataAsset

| Field | Type | Description |
|-------|------|-------------|
| asset_id | str | Unique 12-char ID |
| name | str | Asset name |
| asset_type | AssetType | Type of asset |
| domain | DataDomain | Business domain |
| classification | DataClassification | Data sensitivity |
| owner | str | Asset owner |
| steward | str | Data steward |
| quality_score | float | Quality score 0-1 |
| freshness | DataFreshness | Data freshness |

### DataPolicy

| Field | Type | Description |
|-------|------|-------------|
| policy_id | str | Unique 12-char ID |
| name | str | Policy name |
| policy_type | PolicyType | Type of policy |
| status | PolicyStatus | Current status |
| classification | DataClassification | Applicable classification |
| compliance_frameworks | List[ComplianceFramework] | Frameworks |
| owner | str | Policy owner |

### QualityRule

| Field | Type | Description |
|-------|------|-------------|
| rule_id | str | Unique 8-char ID |
| rule_type | QualityRuleType | Type of rule |
| dimension | QualityDimension | Quality dimension |
| asset_id | str | Target asset |
| threshold | float | Pass threshold |
| pass_rate | float | Current pass rate |

### DataLineage

| Field | Type | Description |
|-------|------|-------------|
| lineage_id | str | Unique 8-char ID |
| source_asset | str | Source asset |
| target_asset | str | Target asset |
| nodes | List[LineageNode] | Lineage nodes |
| edges | List[Dict] | Connections |
| impact_score | float | Impact score 0-1 |

### ComplianceAssessment

| Field | Type | Description |
|-------|------|-------------|
| assessment_id | str | Unique ID |
| framework | ComplianceFramework | Framework |
| status | ComplianceStatus | Compliance status |
| score | float | Compliance score 0-1 |
| controls_passed | int | Controls passed |
| controls_failed | int | Controls failed |

---

## Checklists

### Policy Checklist

- [ ] Policy name and description defined
- [ ] Policy type selected
- [ ] Classification level set
- [ ] Rules documented
- [ ] Compliance frameworks identified
- [ ] Owner assigned
- [ ] Review frequency set
- [ ] Approval obtained
- [ ] Communication plan defined
- [ ] Exception process documented

### Quality Checklist

- [ ] Quality dimensions identified
- [ ] Rules created for each dimension
- [ ] Thresholds set appropriately
- [ ] Profiling schedule defined
- [ ] Alert thresholds configured
- [ ] Remediation process defined
- [ ] Steward assigned
- [ ] Dashboard created
- [ ] Historical tracking enabled
- [ ] Regular review scheduled

### Lineage Checklist

- [ ] Source systems documented
- [ ] Transformations tracked
- [ ] Dependencies mapped
- [ ] Impact analysis performed
- [ ] Cross-system lineage traced
- [ ] Visualizations created
- [ ] Historical changes tracked
- [ ] Change process defined
- [ ] Review cycle established
- [ ] Documentation maintained

### Compliance Checklist

- [ ] Frameworks selected
- [ ] Controls identified
- [ ] Assessment schedule set
- [ ] Evidence collection automated
- [ ] Findings documented
- [ ] Remediation plans created
- [ ] Reporting configured
- [ ] Training completed
- [ ] Audit trail maintained
- [ ] Regular review scheduled

---

## Troubleshooting

### Problem: Low governance score

**Symptoms:** `score.overall_score < 0.60`

**Diagnosis:**
```python
score = agent.calculate_governance_score()
for dim, s in score.dimension_scores.items():
    if s < 0.60:
        print(f"LOW: {dim}: {s:.2%}")
```

**Common Fixes:**
1. Assign owners/stewards to unowned assets
2. Create missing policies
3. Profile and remediate quality issues
4. Complete compliance assessments
5. Resolve open governance issues

### Problem: Quality score below threshold

**Symptoms:** `profile.overall_score < 0.90`

**Diagnosis:**
```python
profile = agent.profile_quality(asset_id)
for dim, score in profile.dimension_scores.items():
    if score < 0.90:
        print(f"LOW: {dim}: {score:.2%}")
```

**Common Fixes:**
1. Create rules for failing dimensions
2. Fix data issues at source
3. Add validation at ingestion
4. Schedule regular profiling
5. Assign steward for remediation

### Problem: Compliance non-compliant

**Symptoms:** `assessment.status == ComplianceStatus.NON_COMPLIANT`

**Solution:** Review findings, create remediation plan, assign owners, track to resolution.

### Problem: Missing lineage

**Symptoms:** Impact analysis shows no downstream

**Solution:** Track lineage for all transformations. Use `track_lineage()` for each ETL step.

### Problem: Steward not assigned

**Symptoms:** Assets without steward

**Solution:** Use `assign_steward()` for each domain. Assign to specific assets.

---

*Data Governance Agent v3.0.0 — Part of the Awesome Grok Skills collection.*
*Last updated: 2026-07-06*

# Business Analysis Agent

> Enterprise-grade business analysis framework covering the full BA lifecycle —
> requirements elicitation, stakeholder management, process modeling, gap analysis,
> SWOT intelligence, solution design, traceability, risk assessment, and handoff documentation.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [Example 1: Requirements Elicitation](#example-1-requirements-elicitation)
  - [Example 2: Stakeholder Mapping](#example-2-stakeholder-mapping)
  - [Example 3: Process Modeling](#example-3-process-modeling)
  - [Example 4: Gap Analysis & SWOT](#example-4-gap-analysis--swot)
  - [Example 5: Business Case with ROI](#example-5-business-case-with-roi)
  - [Example 6: User Stories & Traceability](#example-6-user-stories--traceability)
  - [Example 7: Risk Assessment](#example-7-risk-assessment)
  - [Example 8: Full Workflow](#example-8-full-workflow)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Walkthrough](#walkthrough)
- [Best Practices](#best-practices)
- [Troubleshooting FAQ](#troubleshooting-faq)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Business Analysis Agent is a Python-based system that provides structured
support for the complete business analysis discipline. It automates the creation
of standard BA artifacts while enforcing quality standards and best practices.

### What It Does

| Capability                   | Description                                      |
|-----------------------------|--------------------------------------------------|
| Requirements Elicitation    | 8 structured techniques with typed output        |
| Stakeholder Mapping         | RACI matrix + power/interest grid               |
| Process Modeling            | BPMN/UML with complexity scoring                |
| Gap Analysis                | 5-dimension gap identification                   |
| SWOT Analysis               | Weighted scoring with strategic implications     |
| Business Case               | NPV, IRR, ROI, payback period                   |
| User Stories                | INVEST-compliant with automatic scoring          |
| Traceability                | Forward and backward traceability matrices       |
| Solution Design             | Alternatives analysis with architecture spec     |
| Risk Assessment             | Probability × impact scoring with mitigations    |
| Change Impact               | Multi-dimensional impact assessment              |
| Handoff Documentation       | Complete BA-to-dev transfer package              |

### Who It's For

- **Senior Business Analysts** who need structured artifact generation
- **Product Owners** who want INVEST-compliant user stories
- **Project Managers** who need traceability and risk registers
- **Solution Architects** who want alternatives analysis for design decisions
- **Scrum Masters** who need structured sprint planning inputs

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        BUSINESS ANALYSIS AGENT                          │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │  Discovery    │  │  Analysis    │  │  Design      │  │  Delivery  │  │
│  │  Layer        │  │  Layer       │  │  Layer       │  │  Layer     │  │
│  │              │  │              │  │              │  │            │  │
│  │ • Elicit     │  │ • Gap        │  │ • Solution   │  │ • Handoff  │  │
│  │ • Stakeholder│  │ • SWOT       │  │ • Design     │  │ • Docs     │  │
│  │ • Process    │  │ • Risk       │  │ • Trace      │  │ • Transfer │  │
│  │ • Scope      │  │ • Impact     │  │ • Criteria   │  │ • Archive  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │                    Requirements Repository                         │  │
│  │  In-Memory Dict · SQLite · REST API (future)                      │  │
│  └────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

### Data Model

All artifacts are implemented as Python dataclasses with full type hints:

- **Requirement** — Core artifact with type, priority, status, acceptance criteria
- **StakeholderProfile** — RACI assignments and power/interest position
- **ProcessModel** — BPMN/UML activities, decisions, flows, complexity
- **GapAnalysisResult** — Dimension-specific gaps with root causes
- **SWOTAnalysis** — Weighted factors with strategic implications
- **BusinessCase** — Financial justification with NPV/IRR/ROI
- **UserStory** — INVEST-compliant stories with scoring
- **TraceabilityMatrix** — Forward/backward links with coverage
- **RiskAssessment** — Probability × impact with mitigations
- **ImpactAssessment** — Multi-dimensional change impact

---

## Installation

### From Source

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Direct Usage

No external dependencies required. The agent uses only Python standard library:

```bash
python agents/business-analysis/agent.py
```

### Optional Dependencies

```bash
# For diagram generation
pip install graphviz

# For DOCX export
pip install python-docx

# For PDF export
pip install weasyprint

# For persistent storage
pip install sqlite3  # included with Python

# For REST API (future)
pip install fastapi uvicorn
```

---

## Quick Start

### 1. Import the Agent

```python
from agents.business_analysis.agent import (
    BusinessAnalysisAgent,
    BAConfig,
    RequirementType,
    PriorityLevel,
    ModelingNotation,
    DocumentType,
)
```

### 2. Initialize with Configuration

```python
agent = BusinessAnalysisAgent(BAConfig(
    documentation_format=DocumentType.BRD,
    default_notation=ModelingNotation.BPMN,
    discount_rate=0.10,
    currency="USD",
))
```

### 3. Run the Full Workflow

```python
# Phase 1: Discovery
reqs = agent.gather_requirements("MY-PROJECT", method="workshop")
stakeholders = agent.create_stakeholder_map("MY-PROJECT")
process = agent.map_process("Customer Onboarding")

# Phase 2: Analysis
gaps = agent.conduct_gap_analysis(current, desired)
swot = agent.perform_swot_analysis("Our Platform", "Market expansion")
risks = agent.conduct_risk_assessment("MY-PROJECT")

# Phase 3: Design
stories = agent.create_user_stories("onboarding", ["new_user", "admin"])
design = agent.design_solution(reqs)
traceability = agent.build_traceability_matrix(reqs)

# Phase 4: Validation
validation = agent.validate_requirements(reqs)

# Phase 5: Handoff
handoff = agent.generate_handoff_document("MY-PROJECT")
```

---

## Usage Examples

### Example 1: Requirements Elicitation

```python
from agents.business_analysis.agent import BusinessAnalysisAgent, BAConfig

agent = BusinessAnalysisAgent()

# Gather requirements through a structured workshop
requirements = agent.gather_requirements(
    project_id="ECOM-2026",
    method="workshop"
)

# Examine collected requirements
for req in requirements:
    print(f"[{req.priority.name}] {req.title}")
    print(f"  Type: {req.type.value}")
    print(f"  Rationale: {req.rationale}")
    print(f"  Status: {req.status.value}")
    print()

# Output:
# [CRITICAL] User login with MFA
#   Type: functional
#   Rationale: Users must authenticate with MFA for security.
#   Status: draft
#
# [HIGH] Dashboard response < 2s
#   Type: non_functional
#   Rationale: Performance SLA for analytics dashboard.
#   Status: draft
# ...
```

### Example 2: Stakeholder Mapping

```python
# Build RACI matrix and engagement plan
stakeholder_map = agent.create_stakeholder_map("ECOM-2026")

# Print RACI matrix
print("RACI Matrix:")
for activity, assignments in stakeholder_map["raci_matrix"].items():
    print(f"\n  {activity}:")
    for name, role in assignments.items():
        print(f"    {name}: {role}")

# Print power/interest grid
print("\nPower/Interest Grid:")
for quadrant, members in stakeholder_map["power_interest_grid"].items():
    print(f"  {quadrant}: {', '.join(members) or '(empty)'}")

# Print engagement plan
print("\nEngagement Plan:")
for plan in stakeholder_map["engagement_plan"]:
    print(f"  {plan['stakeholder']}: {plan['frequency']} via {plan['channel']}")
```

### Example 3: Process Modeling

```python
from agents.business_analysis.agent import ModelingNotation

# Model a business process in BPMN notation
process = agent.map_process(
    process_name="Order Fulfillment",
    notation=ModelingNotation.BPMN
)

print(f"Process: {process.name}")
print(f"Complexity: {process.complexity.value}")
print(f"Activities: {len(process.activities)}")
print(f"Decisions: {len(process.decisions)}")
print(f"Swimlanes: {process.swimlanes}")
print(f"Cycle Time: {process.cycle_time_seconds:.0f} seconds")

print("\nInefficiencies:")
for ineff in process.inefficiencies:
    print(f"  - {ineff}")

print("\nBottlenecks:")
for bn in process.bottlenecks:
    print(f"  - {bn}")

# UML notation
process_uml = agent.map_process(
    process_name="Invoice Processing",
    notation=ModelingNotation.UML
)
print(f"\nUML Process: {process_uml.name}, Complexity: {process_uml.complexity.value}")
```

### Example 4: Gap Analysis & SWOT

```python
# Gap Analysis
current = {
    "process": "manual_spreadsheet_tracking",
    "technology": "on_prem_legacy",
    "people": "untrained_in_new_tools",
    "data": "siloed_excel_files",
    "governance": "undefined_policies",
}

desired = {
    "process": "automated_workflow_engine",
    "technology": "cloud_native_platform",
    "people": "certified_power_users",
    "data": "unified_data_warehouse",
    "governance": "documented_framework",
}

gaps = agent.conduct_gap_analysis(current, desired)
for gap in gaps:
    print(f"[{gap.gap_type.value.upper()}] {gap.description}")
    print(f"  Current:  {gap.current_state}")
    print(f"  Desired:  {gap.desired_state}")
    print(f"  Severity: {gap.severity.name}")
    print(f"  Root Cause: {gap.root_cause}")
    print(f"  Action: {gap.recommendation}")
    print()

# SWOT Analysis
swot = agent.perform_swot_analysis("E-Commerce Platform", "International expansion")

print("SWOT Weighted Scores:")
for category, score in swot.weighted_scores.items():
    bar = "█" * int(score / 5)
    print(f"  {category:15s}: {score:5.1f}% {bar}")

print("\nStrategic Implications:")
for imp in swot.strategic_implications:
    print(f"  → {imp}")
```

### Example 5: Business Case with ROI

```python
# Write a business case with custom costs and benefits
business_case = agent.write_business_case(
    problem="Customer onboarding takes 14 days; industry benchmark is 3 days",
    solution="Automated onboarding platform with identity verification API",
    costs={
        "development": 750000,
        "infrastructure": 150000,
        "training": 75000,
        "change_management": 50000,
        "contingency": 100000,
    },
    benefits={
        "revenue_increase": 1200000,
        "cost_savings": 450000,
        "efficiency_gains": 300000,
        "customer_satisfaction": 200000,
    }
)

print("Business Case Summary:")
print(f"  Problem:  {business_case.problem_statement[:60]}...")
print(f"  Solution: {business_case.proposed_solution[:60]}...")
print(f"  NPV:      ${business_case.npv:,.2f}")
print(f"  IRR:      {business_case.irr * 100:.1f}%")
print(f"  ROI:      {business_case.roi:.1f}%")
print(f"  Payback:  {business_case.payback_period_months:.0f} months")
print(f"  Confidence: {business_case.confidence_level}")
print(f"  Recommendation: {business_case.recommendation}")

print("\nAssumptions:")
for assumption in business_case.assumptions:
    print(f"  - {assumption}")
```

### Example 6: User Stories & Traceability

```python
# Create INVEST-compliant user stories
stories = agent.create_user_stories(
    feature="payment_processing",
    personas=["buyer", "seller", "admin"]
)

for story in stories:
    print(f"Story: {story.to_invest_text()}")
    print(f"  Points: {story.story_points}")
    print(f"  INVEST Score: {story.invest_score}/100")
    print(f"  Acceptance Criteria:")
    for ac in story.acceptance_criteria:
        print(f"    - {ac}")
    print()

# Build traceability matrix
matrix = agent.build_traceability_matrix()
print(f"Traceability Coverage: {matrix.coverage_percentage}%")
print(f"Gaps: {len(matrix.gaps)}")
for gap in matrix.gaps:
    print(f"  - {gap}")

# Generate acceptance criteria for a story
criteria = agent.create_acceptance_criteria(stories[0])
print(f"\nAcceptance Criteria for {stories[0].id}:")
for ac in criteria:
    print(f"  GIVEN: {ac.given}")
    print(f"  WHEN:  {ac.when}")
    print(f"  THEN:  {ac.then}")
    print()
```

### Example 7: Risk Assessment

```python
# Conduct risk assessment
risks = agent.conduct_risk_assessment("ECOM-2026")

print("Risk Register:")
print(f"{'ID':<12} {'Risk':<25} {'Level':<10} {'Score':<8} {'Mitigation'}")
print("-" * 90)
for risk in risks:
    print(
        f"{risk.id:<12} {risk.title:<25} {risk.risk_level.name:<10} "
        f"{risk.risk_score:<8.1f} {risk.mitigation_strategy[:40]}"
    )

# Assess impact of a change request
from agents.business_analysis.agent import ChangeRequest, ChangeType

cr = ChangeRequest(
    title="Add multi-currency support",
    description="Enable transactions in 15 currencies",
    change_type=ChangeType.TECHNOLOGICAL,
    affected_areas=["Payment Module", "Reporting", "API"],
)

impact = agent.assess_impact(cr)
print(f"\nImpact Assessment for: {cr.title}")
print(f"  Organizational: {impact.organizational_impact}")
print(f"  Technical:      {impact.technical_impact}")
print(f"  Cost:           ${impact.estimated_cost:,.0f}")
print(f"  Duration:       {impact.estimated_duration_weeks} weeks")
print(f"  Risk Level:     {impact.risk_level.name}")
print(f"  Recommendation: {impact.recommendation}")
```

### Example 8: Full Workflow

```python
from agents.business_analysis.agent import (
    BusinessAnalysisAgent, BAConfig, DocumentType, ModelingNotation
)

# Initialize
agent = BusinessAnalysisAgent(BAConfig(
    documentation_format=DocumentType.BRD,
    default_notation=ModelingNotation.BPMN,
))

PROJECT = "DIGITAL-TRANSFORM-2026"

# Phase 1: Discovery
reqs = agent.gather_requirements(PROJECT, "workshop")
agent.transition_phase(AnalysisPhase.ANALYSIS)
stakeholder_map = agent.create_stakeholder_map(PROJECT)
process = agent.map_process("Digital Customer Journey")

# Phase 2: Analysis
gaps = agent.conduct_gap_analysis(
    {"process": "paper_forms", "technology": "fax_based"},
    {"process": "digital_forms", "technology": "cloud_platform"}
)
swot = agent.perform_swot_analysis("Digital Platform", "Market disruption")
risks = agent.conduct_risk_assessment(PROJECT)

# Phase 3: Design
stories = agent.create_user_stories("digital_forms", ["customer", "agent", "manager"])
design = agent.design_solution(reqs)
data_flow = agent.model_data_flows("Customer Intake System")

# Phase 4: Validation
traceability = agent.build_traceability_matrix(reqs)
validation = agent.validate_requirements(reqs)

# Phase 5: Handoff
handoff = agent.generate_handoff_document(PROJECT)

# Export everything
export = agent.export_all()
print(f"Exported {len(export['requirements'])} requirements")
print(f"Exported {len(export['stakeholders'])} stakeholders")
print(f"Exported {len(export['processes'])} processes")
print(f"Exported {len(export['risks'])} risks")

# Status
print(agent.get_status())
```

---

## API Reference

### BusinessAnalysisAgent

#### Constructor

```python
BusinessAnalysisAgent(config: Optional[BAConfig] = None)
```

| Parameter | Type      | Default  | Description                   |
|-----------|-----------|----------|-------------------------------|
| config    | BAConfig  | None     | Agent configuration           |

#### Methods

| Method                        | Returns                | Description                          |
|-------------------------------|------------------------|--------------------------------------|
| `gather_requirements(pid, m)` | `List[Requirement]`    | Elicit requirements via technique    |
| `create_stakeholder_map(pid)` | `Dict[str, Any]`       | RACI + power/interest grid          |
| `map_process(name, notation)` | `ProcessModel`         | BPMN/UML process model              |
| `conduct_gap_analysis(c, d)`  | `List[GapAnalysisResult]` | Gap identification across 5 dims |
| `perform_swot_analysis(e, c)` | `SWOTAnalysis`         | Weighted SWOT with implications     |
| `write_business_case(p, s)`   | `BusinessCase`         | Financial justification with NPV    |
| `create_user_stories(f, p)`   | `List[UserStory]`      | INVEST-compliant stories            |
| `build_traceability_matrix()` | `TraceabilityMatrix`   | Forward/backward traceability       |
| `design_solution(reqs)`       | `SolutionDesign`       | Architecture with alternatives      |
| `assess_impact(cr)`           | `ImpactAssessment`     | Multi-dimensional impact            |
| `model_data_flows(sys)`       | `DataFlowModel`        | Data flow diagram generation        |
| `conduct_risk_assessment(pid)`| `List[RiskAssessment]` | Risk register with mitigations      |
| `validate_requirements(reqs)` | `Dict[str, Any]`       | Quality validation report           |
| `create_acceptance_criteria(s)`| `List[AcceptanceCriteria]` | Given/When/Then criteria      |
| `generate_handoff_document(p)`| `Dict[str, Any]`       | BA-to-dev handoff package           |
| `get_status()`                | `Dict[str, Any]`       | Current agent state                 |
| `transition_phase(phase)`     | `None`                 | Move to next analysis phase         |
| `export_all()`                | `Dict[str, Any]`       | Export all artifacts as dict        |

### Dataclasses

#### Requirement

```python
@dataclass
class Requirement:
    id: str                          # Auto-generated unique ID
    title: str                       # Short descriptive title
    description: str                 # Detailed description
    type: RequirementType            # FUNCTIONAL|NON_FUNCTIONAL|BUSINESS|TECHNICAL|TRANSITION|CONSTRAINT
    priority: PriorityLevel          # CRITICAL|HIGH|MEDIUM|LOW
    status: RequirementStatus        # DRAFT|REVIEWED|APPROVED|IMPLEMENTED|VERIFIED|REJECTED
    rationale: str                   # Business justification
    acceptance_criteria: List[str]   # Testable criteria
    dependencies: List[str]          # Linked requirement IDs
    stakeholder_ids: List[str]       # Related stakeholders
    tags: List[str]                  # Categorization tags
    created_at: str                  # ISO timestamp
    updated_at: str                  # ISO timestamp
    version: int                     # Version number
    estimated_effort: Optional[str]  # T-shirt size or hours
    source: str                      # Elicitation source
    notes: str                       # Additional notes
```

#### UserStory

```python
@dataclass
class UserStory:
    id: str
    title: str
    persona: str                     # Target user role
    action: str                      # What they want to do
    benefit: str                     # Why they want it
    story_text: str                  # Full "As a... I want... so that..." text
    priority: PriorityLevel
    story_points: int                # Estimated complexity (auto-calculated)
    invest_score: float              # 0-100 INVEST score
    acceptance_criteria: List[str]
    dependencies: List[str]
    epic_id: Optional[str]
    theme: str
    status: str
```

#### RiskAssessment

```python
@dataclass
class RiskAssessment:
    id: str
    title: str
    description: str
    probability: float               # 0.0 - 1.0
    impact: float                    # 0.0 - 1.0
    risk_level: RiskLevel            # NEGLIGIBLE|LOW|MEDIUM|HIGH|CRITICAL
    mitigation_strategy: str
    contingency_plan: str
    owner: str
    status: str
    category: str

    @property
    def risk_score(self) -> float:
        return probability * impact * 5
```

#### BusinessCase

```python
@dataclass
class BusinessCase:
    id: str
    problem_statement: str
    proposed_solution: str
    alternatives: List[Dict[str, Any]]
    costs: Dict[str, float]
    benefits: Dict[str, float]
    npv: float                       # Net Present Value
    irr: float                       # Internal Rate of Return
    roi: float                       # Return on Investment (%)
    payback_period_months: float
    risk_adjusted_roi: float
    strategic_alignment: List[str]
    assumptions: List[str]
    recommendation: str
    confidence_level: str
```

---

## Configuration

### BAConfig Options

```python
from agents.business_analysis.agent import BAConfig, DocumentType, ModelingNotation

config = BAConfig(
    # Document output format
    documentation_format=DocumentType.BRD,      # BRD|SRS|FRD|USP|NFR

    # Review cycles before approval
    review_cycles=2,

    # Default process modeling notation
    default_notation=ModelingNotation.BPMN,     # BPMN|UML|EPC|FLOWCHART

    # Risk escalation threshold (risk_score above this triggers escalation)
    risk_threshold=0.6,

    # INVEST criteria scoring weights (must sum to 1.0)
    invest_weights={
        "independent": 0.15,
        "negotiable": 0.10,
        "valuable": 0.20,
        "estimable": 0.15,
        "small": 0.20,
        "testable": 0.20,
    },

    # Engagement model
    stakeholder_engagement_model="agile",        # agile|waterfall|hybrid

    # Auto-generate Given/When/Then acceptance criteria
    auto_generate_acceptance_criteria=True,

    # Risk escalation threshold
    max_risk_score_before_escalation=3.5,

    # Financial settings
    currency="USD",
    discount_rate=0.10,                          # 10% for NPV calculation
)
```

### Environment Variables (Future)

```bash
export BA_DEFAULT_NOTATION=bpmn
export BA_DOCUMENT_FORMAT=brd
export BA_DISCOUNT_RATE=0.10
export BA_STORAGE_BACKEND=memory  # memory|sqlite|api
export BA_STORAGE_PATH=./ba_artifacts.db
```

---

## Walkthrough

### End-to-End: New Product Requirements Analysis

This walkthrough demonstrates analyzing requirements for a new customer portal.

**Step 1: Initialize the Agent**

```python
from agents.business_analysis.agent import BusinessAnalysisAgent, BAConfig

agent = BusinessAnalysisAgent(BAConfig(
    documentation_format=DocumentType.BRD,
    default_notation=ModelingNotation.BPMN,
))
```

**Step 2: Elicit Requirements**

```python
# Conduct a workshop with key stakeholders
reqs = agent.gather_requirements("PORTAL-2026", method="workshop")
print(f"Collected {len(reqs)} requirements from workshop")
```

**Step 3: Map Stakeholders**

```python
stakeholders = agent.create_stakeholder_map("PORTAL-2026")
print(f"Identified {stakeholders['stakeholder_count']} stakeholders")
for quadrant, members in stakeholders["power_interest_grid"].items():
    if members:
        print(f"  {quadrant}: {', '.join(members)}")
```

**Step 4: Model the Process**

```python
process = agent.map_process("Customer Portal Login", ModelingNotation.BPMN)
print(f"Process complexity: {process.complexity.value}")
print(f"Bottlenecks: {process.bottlenecks}")
```

**Step 5: Analyze Gaps**

```python
gaps = agent.conduct_gap_analysis(
    {"process": "paper_forms", "technology": "manual_lookup"},
    {"process": "digital_portal", "technology": "automated_search"}
)
for gap in gaps:
    print(f"[{gap.gap_type.value}] Severity: {gap.severity.name}")
    print(f"  Recommendation: {gap.recommendation}")
```

**Step 6: SWOT Analysis**

```python
swot = agent.perform_swot_analysis("Customer Portal", "Competitor launched similar")
for category, score in swot.weighted_scores.items():
    print(f"  {category}: {score}%")
```

**Step 7: Financial Justification**

```python
bc = agent.write_business_case(
    "Customer support handles 500 daily calls for account info",
    "Self-service portal reduces calls by 60%"
)
print(f"NPV: ${bc.npv:,.2f}")
print(f"ROI: {bc.roi:.1f}%")
print(f"Payback: {bc.payback_period_months:.0f} months")
```

**Step 8: User Stories**

```python
stories = agent.create_user_stories("self_service_portal", ["customer", "support_agent"])
for s in stories:
    print(f"{s.to_invest_text()}")
    print(f"  Points: {s.story_points} | INVEST: {s.invest_score}")
```

**Step 9: Risks**

```python
risks = agent.conduct_risk_assessment("PORTAL-2026")
for r in risks:
    print(f"[{r.risk_level.name}] {r.title}: {r.risk_score}")
```

**Step 10: Handoff**

```python
handoff = agent.generate_handoff_document("PORTAL-2026")
print(f"Handoff summary: {handoff['executive_summary']}")
print(f"Requirements: {handoff['requirements_summary']['total']}")
print(f"Risks: {len(handoff['risk_register'])}")
```

---

## Best Practices

### Requirements

1. **Use the SMART framework**: Specific, Measurable, Achievable, Relevant, Time-bound
2. **One requirement per card**: Each requirement should be independently verifiable
3. **Trace every link**: Business need → Requirement → Test → Acceptance
4. **Validate early**: Run `validate_requirements()` before handoff
5. **Version everything**: Requirements evolve — track version history

### Stakeholders

1. **Map before you start**: Know who's who before eliciting
2. **RACI every activity**: No activity without an Accountable party
3. **Tailor communication**: Executives get summaries, developers get details
4. **Manage expectations**: Use the engagement plan consistently
5. **Escalate conflicts**: When two stakeholders disagree, escalate to sponsor

### Process Modeling

1. **Choose the right notation**: BPMN for workflows, UML for system interactions
2. **Start simple**: Model the happy path first, then exceptions
3. **Score complexity**: Use the complexity formula to set expectations
4. **Identify bottlenecks**: Single-assignee steps are always bottlenecks
5. **Estimate cycle times**: Use the 5-minute/activity baseline

### Risk Management

1. **Quantify everything**: No risk without probability × impact
2. **Mitigate proactively**: Don't wait for risks to materialize
3. **Escalate high risks**: Use the escalation threshold in config
4. **Track status**: Risks change — review regularly
5. **Document contingency**: Have a Plan B for critical risks

### User Stories

1. **Follow INVEST**: Score every story; refines those below 60
2. **Right-size**: If story_points > 8, break it down
3. **Define personas**: Know who benefits and why
4. **Testable criteria**: Every story needs ≥ 2 Given/When/Then criteria
5. **Estimate honestly**: T-shirt sizing is a starting point, not a commitment

---

## Troubleshooting FAQ

### Q: Requirements seem too generic

**A:** Use a more specific elicitation method. `interview` and `focus_group` produce
more detailed requirements than `brainstorming`. Also check that the `rationale`
field contains a quantified business value.

### Q: INVEST scores are all low

**A:** The scoring algorithm penalizes:
- Missing personas (set `persona` field)
- Missing benefits (set `benefit` field)
- Too many dependencies (reduce `dependencies` list)
- Too many story points (break stories into smaller pieces)
- Missing acceptance criteria (add ≥ 2 criteria per story)

### Q: Gap analysis returns no gaps

**A:** The `current_state` and `desired_state` dicts must have different values
for at least one key. Check that the keys match between both dicts.

### Q: Business case shows negative NPV

**A:** Possible causes:
- Total costs exceed total benefits
- Discount rate is too high (default: 10%)
- Time horizon is too short (default: 5 years)
- Maintenance costs consume too much benefit (default: 20%)

### Q: Process complexity is always "simple"

**A:** The complexity formula is: `activities + (decisions × 2) + (swimlanes × 3)`.
Add more activities and swimlanes to increase complexity classification.

### Q: Risk scores seem too high or too low

**A:** Verify that `probability` and `impact` are in the 0.0-1.0 range.
The formula is: `probability × impact × 5`. Example: 0.7 × 0.8 × 5 = 2.8 (HIGH).

### Q: How do I persist artifacts across sessions?

**A:** Use `export_all()` to serialize, then save to JSON. Reload by reconstructing
dataclasses from the dict. For persistent storage, use the SQLite backend
(configure `BA_STORAGE_BACKEND=sqlite`).

### Q: Can I add custom risk templates?

**A:** Extend the `conduct_risk_assessment()` method by subclassing
`BusinessAnalysisAgent` and overriding the risk templates list.

---

## Contributing

### Development Setup

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install pytest
```

### Running Tests

```bash
pytest tests/ -v
```

### Code Style

- Type hints on all public methods
- Docstrings on all public classes and methods
- Dataclasses for all data structures
- Enums for all categorical values
- Logging at INFO level for operations, DEBUG for details

### Adding New Features

1. Define the data structure as a `@dataclass`
2. Add the corresponding method to `BusinessAnalysisAgent`
3. Add logging for the new operation
4. Update `get_status()` and `export_all()` if applicable
5. Add a usage example to this README
6. Update `ARCHITECTURE.md` with component documentation
7. Update `GROK.md` with capability documentation

---

## License

MIT License

Copyright (c) 2026 MiMo Team

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

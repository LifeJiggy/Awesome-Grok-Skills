---
name: "Sustainability Agent"
version: "2.0.0"
description: "Comprehensive sustainability management platform covering carbon tracking, ESG reporting, circular economy, green supply chain, and regulatory compliance"
author: "Awesome Grok Skills"
license: "MIT"
tags:
  - sustainability
  - esg
  - carbon-tracking
  - circular-economy
  - supply-chain
  - compliance
  - green-initiatives
  - environmental
  - climate
category: "sustainability"
personality: "sustainability-director"
use_cases:
  - "carbon footprint tracking"
  - "ESG scoring and reporting"
  - "sustainability goal management"
  - "green initiative planning"
  - "supply chain sustainability"
  - "circular economy tracking"
  - "resource usage monitoring"
  - "regulatory compliance"
  - "stakeholder reporting"
  - "UN SDG alignment"
---

# Sustainability Agent

> Comprehensive sustainability management platform for measuring, managing, and improving environmental and social impact.

## Agent Identity

You are the Sustainability Agent — a sustainability director capable of tracking carbon emissions, managing ESG performance, optimizing supply chains, and ensuring regulatory compliance. You combine environmental science expertise with business acumen to drive meaningful sustainability improvements.

### Core Principles

1. **Measure First**: You can't manage what you don't measure
2. **Science-Based**: Align targets with climate science (1.5°C pathway)
3. **Transparency**: Open and honest reporting to all stakeholders
4. **Continuous Improvement**: Always seek better sustainability outcomes
5. **Holistic View**: Consider environmental, social, and governance together

---

## Capabilities

### Carbon Footprint Tracking

```python
from agents.sustainability.agent import (
    SustainabilityAgent, SustainabilityCategory, CarbonScope
)

agent = SustainabilityAgent()

# Track Scope 1 (direct) emissions
agent.track_emission(
    SustainabilityCategory.ENERGY, CarbonScope.SCOPE_1,
    "Natural Gas", 5000, "m³", location="HQ"
)

# Track Scope 2 (indirect from purchased energy)
agent.track_emission(
    SustainabilityCategory.ENERGY, CarbonScope.SCOPE_2,
    "Electricity", 100000, "kWh", location="HQ"
)

# Calculate total footprint
footprint = agent.calculate_carbon_footprint([
    {"type": "electricity", "data": {"kwh": 100000, "region": "EU"}},
    {"type": "transportation", "data": {"distance_km": 50000, "mode": "car"}},
])
print(f"Total: {footprint['total_emission_tonnes']} tonnes CO2e")
```

### ESG Scoring

```python
from agents.sustainability.agent import ESGReporter

reporter = ESGReporter(agent.carbon, agent.goals, agent.initiatives, agent.supply_chain)
esg = reporter.calculate_esg_score()

print(f"Overall ESG Score: {esg.overall_score}")
print(f"Rating: {esg.rating.value}")
print(f"Environmental: {esg.environmental_score}")
print(f"Social: {esg.social_score}")
print(f"Governance: {esg.governance_score}")
```

### Sustainability Goals

```python
from agents.sustainability.agent import GoalPriority

# Create a goal
goal = agent.set_sustainability_goal(
    "Net Zero by 2030",
    "Achieve net-zero carbon emissions across all scopes",
    SustainabilityCategory.ENERGY,
    baseline=5000,
    target=0,
    target_year=2030,
    priority=GoalPriority.CRITICAL,
)

# Update progress
agent.goals.update_progress(goal["goal_id"], current_value=3500)

# Check status
status = agent.goals.calculate_goal_status(goal["goal_id"])
print(f"On track: {status['on_track']}")
```

### Green Initiatives

```python
# Create initiative
initiative = agent.initiatives.create_initiative(
    "Solar Panel Installation",
    "Install 500kW solar array on HQ roof",
    SustainabilityCategory.ENERGY,
    investment=150000,
    expected_savings={"annual": 25000},
    carbon_reduction=120,
    timeline_months=6,
)

# Calculate ROI
roi = agent.initiatives.calculate_roi(initiative.initiative_id)
print(f"Payback period: {roi['payback_years']} years")
print(f"5-year ROI: {roi['roi_5_year_pct']}%")
```

### Supply Chain Management

```python
from agents.sustainability.agent import SupplyChainTier

# Add supplier
supplier = agent.supply_chain.add_supplier(
    "Green Materials Co",
    SupplyChainTier.TIER_1,
    "Germany",
    "Raw Materials",
    sustainability_score=85,
    certifications=["ISO 14001", "FSC"],
    carbon_footprint=50,
)

# Calculate score
score = agent.supply_chain.calculate_supplier_score(supplier.supplier_id)
print(f"Sustainability score: {score['overall_score']}")
```

### Circular Economy

```python
# Add product
product = agent.circular_economy.add_product(
    "EcoWidget",
    "Consumer Electronics",
    {"aluminum": 40, "plastic": 30, "glass": 30},
    recyclable_pct=85,
    recycled_content_pct=25,
    carbon_footprint=12.5,
    design_for_disassembly=True,
    take_back_program=True,
)

# Check circularity
circularity = agent.circular_economy.calculate_circularity_score(product.product_id)
print(f"Circularity score: {circularity['circularity_score']}")
```

### Resource Tracking

```python
from agents.sustainability.agent import WaterSource, WasteType, EnergySource

# Track water usage
agent.resources.add_water_usage("HQ", WaterSource.MUNICIPAL, 500, datetime.now())

# Track waste
agent.resources.add_waste_record("HQ", WasteType.RECYCLABLE, 200, datetime.now(), recycled_pct=95)

# Track energy
agent.resources.add_energy_record("HQ", EnergySource.SOLAR, 5000, datetime.now(), renewable_pct=100)

# Get summaries
water = agent.resources.get_water_summary()
waste = agent.resources.get_waste_summary()
energy = agent.resources.get_energy_summary()
```

### Compliance Management

```python
from agents.sustainability.agent import ComplianceFramework

# Add requirement
agent.compliance.add_requirement(
    ComplianceFramework.EU_CSRD,
    "Annual sustainability reporting",
    due_date=datetime(2025, 12, 31),
)

# Get compliance summary
summary = agent.compliance.get_compliance_summary()
print(f"Compliance rate: {summary['compliance_rate_pct']}%")
```

### Dashboard & Reports

```python
# Get comprehensive dashboard
dashboard = agent.get_sustainability_dashboard()
print(dashboard)

# Generate annual report
report = agent.generate_annual_report()
print(report)
```

---

## Method Signatures

### CarbonCalculator

```python
def calculate_emission(source: str, quantity: float, region: str = "US_average") -> Dict[str, Any]
def calculate_from_activity(activity_type: str, data: Dict[str, Any]) -> Dict[str, Any]
def calculate_total_footprint(records: List[EmissionRecord]) -> Dict[str, Any]
```

### GoalTracker

```python
def create_goal(name: str, description: str, category: SustainabilityCategory,
                baseline_value: float, target_value: float, target_year: int,
                priority: GoalPriority = GoalPriority.MEDIUM, owner: str = "") -> SustainabilityGoal
def update_progress(goal_id: str, current_value: float) -> Optional[SustainabilityGoal]
def calculate_goal_status(goal_id: str) -> Dict[str, Any]
def get_overall_progress() -> Dict[str, Any]
```

### InitiativeManager

```python
def create_initiative(name: str, description: str, category: SustainabilityCategory,
                      investment: float, expected_savings: Dict[str, float],
                      carbon_reduction: float, timeline_months: int = 12,
                      owner: str = "") -> GreenInitiative
def update_initiative(initiative_id: str, progress: float,
                      status: Optional[InitiativeStatus] = None) -> Optional[GreenInitiative]
def calculate_roi(initiative_id: str) -> Dict[str, Any]
def get_portfolio_summary() -> Dict[str, Any]
```

### SupplyChainManager

```python
def add_supplier(name: str, tier: SupplyChainTier, location: str, category: str,
                 **kwargs: Any) -> Supplier
def calculate_supplier_score(supplier_id: str) -> Dict[str, Any]
def get_suppliers_by_tier(tier: SupplyChainTier) -> List[Supplier]
def get_supply_chain_summary() -> Dict[str, Any]
```

### CircularEconomyManager

```python
def add_product(name: str, category: str, material_composition: Dict[str, float],
                recyclable_pct: float, recycled_content_pct: float,
                carbon_footprint: float, **kwargs: Any) -> CircularProduct
def calculate_circularity_score(product_id: str) -> Dict[str, Any]
def get_portfolio_circularity() -> Dict[str, Any]
```

### ResourceUsageManager

```python
def add_water_usage(location: str, source: WaterSource, volume_m3: float,
                    date: datetime, **kwargs: Any) -> WaterUsage
def add_waste_record(location: str, waste_type: WasteType, weight_kg: float,
                     date: datetime, **kwargs: Any) -> WasteRecord
def add_energy_record(location: str, source: EnergySource, kwh: float,
                      date: datetime, **kwargs: Any) -> EnergyRecord
def get_water_summary(...) -> Dict[str, Any]
def get_waste_summary(...) -> Dict[str, Any]
def get_energy_summary(...) -> Dict[str, Any]
```

---

## Data Models

### EmissionRecord

```python
@dataclass
class EmissionRecord:
    record_id: str
    category: SustainabilityCategory
    scope: CarbonScope
    source: str
    amount: float
    unit: str
    date: datetime
    location: str
    verified: bool = False
    activity_data: Dict[str, Any] = field(default_factory=dict)
    reduction_offset: float = 0.0
    notes: str = ""

    @property
    def net_emission(self) -> float:
        return max(0, self.amount - self.reduction_offset)
```

### SustainabilityGoal

```python
@dataclass
class SustainabilityGoal:
    goal_id: str
    name: str
    description: str
    category: SustainabilityCategory
    baseline_value: float
    target_value: float
    baseline_year: int
    target_year: int
    current_value: float = 0.0
    status: str = "active"
    priority: GoalPriority = GoalPriority.MEDIUM

    @property
    def progress_pct(self) -> float
    @property
    def years_remaining(self) -> int
    @property
    def is_on_track(self) -> bool
```

### GreenInitiative

```python
@dataclass
class GreenInitiative:
    initiative_id: str
    name: str
    description: str
    category: SustainabilityCategory
    status: InitiativeStatus
    start_date: datetime
    expected_completion: datetime
    investment: float
    projected_savings: Dict[str, float]
    carbon_reduction: float
    metrics: Dict[str, Any] = field(default_factory=dict)

    @property
    def actual_completion_pct(self) -> float
    @property
    def is_overdue(self) -> bool
```

---

## Checklists

### Carbon Tracking

- [ ] All emission sources identified
- [ ] Emission factors validated for region
- [ ] Scope 1, 2, and 3 boundaries defined
- [ ] Data quality verified
- [ ] Third-party verification completed

### Goal Setting

- [ ] Baseline established with valid data
- [ ] Target aligned with science-based pathway
- [ ] Timeline realistic and measurable
- [ ] Owner assigned and accountable
- [ ] Milestones defined for progress tracking

### Supply Chain Assessment

- [ ] Supplier tiers mapped
- [ ] Sustainability criteria defined
- [ ] Audit schedule established
- [ ] Risk assessment completed
- [ ] Improvement plans in place

### Compliance

- [ ] Applicable frameworks identified
- [ ] Requirements documented
- [ ] Evidence collected and organized
- [ ] Submission deadlines tracked
- [ ] Follow-up actions assigned

---

## Troubleshooting

### Common Issues

**Emission calculations seem high**
- Verify emission factors are appropriate for your region
- Check if data includes all sources
- Ensure units are consistent

**Goal progress not updating**
- Confirm goal_id is correct
- Check that current_value is being passed
- Verify goal hasn't already been marked achieved

**Supplier scores are low**
- Request updated certifications
- Schedule audit to verify performance
- Work with supplier on improvement plan

**ESG score seems inconsistent**
- Check that all components are being calculated
- Verify scoring methodology matches your framework
- Review weight assignments

---

## Best Practices

1. **Regular Monitoring**: Track emissions monthly, not just annually
2. **Data Validation**: Verify emission factors and activity data
3. **Stakeholder Engagement**: Share progress transparently
4. **Continuous Improvement**: Update targets as you achieve goals
5. **Third-Party Verification**: Get independent assurance for credibility

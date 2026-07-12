---
name: workforce-planning
category: hr-tech
version: 1.0.0
tags:
  - workforce
  - planning
  - headcount
  - forecasting
  - skills-inventory
  - succession
  - capacity
  - hr-tech
difficulty: advanced
estimated_time: 50min
prerequisites:
  - python-3.11
  - pandas
  - numpy
  - scikit-learn
---

# Workforce Planning

## Purpose

Strategic workforce planning platform covering headcount forecasting, skills inventory management, succession pipeline planning, and capacity modeling. Provides data-driven workforce strategies aligned to business growth trajectories and operational requirements.

## Core Components

### 1. Headcount Forecasting

- **Growth Model**: Revenue-per-employee trending with department-specific multipliers
- **Attrition Adjustment**: Net headcount = openings + growth - attrition - internal mobility
- **Scenario Planning**: Best/base/worst case projections with adjustable growth assumptions
- **Budget Alignment**: Headcount plans tied to compensation budgets with cost-per-hire modeling

### 2. Skills Inventory

- **Skill Taxonomy**: Hierarchical skill graph with proficiency levels and recency weighting
- **Capacity Mapping**: Skills-to-projects allocation with utilization tracking
- **Supply-Demand Analysis**: Compare available skill supply against project/business demand
- **Gap Identification**: Time-bound skill shortage predictions based on project pipeline

### 3. Succession Pipeline Planning

- **Critical Role Identification**: Map roles by business impact, replacement difficulty, and vacancy risk
- **Pipeline Depth Scoring**: Count and readiness of potential successors per critical role
- **Development Timeline**: Projected readiness dates based on development plans and performance trajectory
- **Risk Matrix**: Combine succession readiness with attrition probability for comprehensive risk view

### 4. Capacity Planning

- **Utilization Modeling**: Target vs actual utilization with burnout risk thresholds
- **Project Allocation**: Optimal staffing recommendations balancing skill match and capacity
- **Bottleneck Detection**: Identify team/role constraints limiting delivery capacity
- **Demand Smoothing**: Forecast peak demand periods and recommend hiring/contractor timing

## Data Models

```
HeadcountPlan
  ├── plan_id: str
  ├── department: str
  ├── current_count: int
  ├── projected_count: Dict[int, int]
  ├── growth_assumptions: GrowthAssumptions
  ├── budget_impact: BudgetImpact
  └── scenarios: List[Scenario]

SkillsInventory
  ├── inventory_id: str
  ├── organization_id: str
  ├── skills: List[SkillAsset]
  ├── supply_demand: SupplyDemandReport
  └── gap_forecast: GapForecast

SuccessionPipeline
  ├── pipeline_id: str
  ├── critical_roles: List[CriticalRole]
  ├── health_score: float
  └── coverage_gaps: List[CoverageGap]

CapacityModel
  ├── model_id: str
  ├── team_capacities: List[TeamCapacity]
  ├── utilization_target: float
  ├── bottleneck_roles: List[str]
  └── demand_forecast: DemandForecast
```

## Implementation Patterns

### Headcount Projection
```python
class HeadcountForecaster:
    def project(self, current: int, growth_rate: float, attrition_rate: float, months: int) -> List[int]:
        projections = [current]
        for m in range(months):
            growth = current * growth_rate / 12
            attrition = current * attrition_rate / 12
            current = current + growth - attrition
            projections.append(round(current))
        return projections
```

### Capacity Utilization
```python
class CapacityPlanner:
    def optimize_allocation(self, projects, team, utilization_target):
        allocation = {}
        for project in sorted(projects, key=lambda p: p.priority, reverse=True):
            best_member = self.find_best_fit(project, team, allocation)
            allocation[project.project_id] = best_member.employee_id
        return allocation
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `attrition_rate_annual` | 0.15 | Assumed annual voluntary attrition rate |
| `utilization_target` | 0.80 | Target billable/utilization ratio |
| `burnout_threshold` | 0.90 | Utilization above which burnout risk is flagged |
| `succession_readiness_min` | 0.70 | Min readiness score for "ready now" classification |
| `forecast_horizon_months` | 24 | Default planning horizon |

## Integration Points

- **HRIS**: Workday, SAP SuccessFactors for current headcount and org data
- **Project Management**: Jira, Asana, Monday.com for project allocation and capacity
- **Finance**: Adaptive Insights, Anaplan for budget alignment
- **Recruiting**: ATS integration for pipeline and time-to-fill data
- **BI Tools**: Tableau, Power BI for executive dashboards

## Ethical Guidelines

1. Workforce plans must not be used to pre-emptively identify individuals for layoffs
2. Skills inventory data must be self-reported or verified with employee consent
3. Capacity utilization metrics must not be used for individual performance management
4. Succession planning data classified as confidential leadership information
5. All projections must include uncertainty ranges, not point estimates

## Testing Strategy

- **Forecasting**: Time-series accuracy validation with historical data
- **Skills Inventory**: Data completeness checks, taxonomy coverage validation
- **Succession**: Pipeline coverage calculation, readiness score calibration
- **Capacity**: Utilization calculation accuracy, bottleneck detection validation
- **Integration**: End-to-end planning cycle from demand to headcount recommendation

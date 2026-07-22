---
name: "policy-simulation"
category: "public-policy-tech"
version: "1.0.0"
tags: ["public-policy-tech", "policy-simulation"]
---

# Policy Simulation

## Overview

Comprehensive policy-simulation capabilities within the public-policy-tech domain. This module provides tools, frameworks, and best practices for policy-simulation operations.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

```python
from policy_simulation import _module

engine = _module.Engine()
engine.configure()
results = engine.run()
print(results)
```

## Best Practices

- Follow security guidelines
- Implement proper error handling
- Use configuration management
- Monitor performance metrics
- Document API interfaces

## Related Modules

- Other modules in public-policy-tech domain
- Integration points with external systems

## Advanced Configuration

### Simulation Models

- **Agent-Based Model (ABM)**: Simulates individual actors and their interactions. Useful for emergent behavior analysis.
- **System Dynamics (SD)**: Models feedback loops and stocks/flows. Good for macro-level policy analysis.
- **Microsimulation**: Individual-level simulation using survey data. Ideal for tax and transfer policy.
- **Computable General Equilibrium (CGE)**: Economy-wide models for trade and fiscal policy analysis.

### Simulation Configuration

```yaml
simulation:
  model_type: "agent_based"
  parameters:
    population_size: 100000
    time_horizon: "10y"
    time_step: "1month"
    stochastic_runs: 1000
  scenarios:
    - name: "baseline"
      description: "No policy change"
      parameters: {}
    - name: "carbon_tax"
      description: "$50/ton carbon tax"
      parameters:
        carbon_tax_rate: 50
        tax_implementation: "immediate"
    - name: "ubsidy"
      description: "Electric vehicle subsidy"
      parameters:
        ev_subsidy: 7500
        subsidy_duration: "5y"
  outputs:
    - name: "emissions_reduction"
      unit: "MT CO2e"
    - name: "gdp_impact"
      unit: "percentage"
    - name: "employment_effect"
      unit: "jobs"
```

### Scenario Design

```python
from policy_simulation import ScenarioDesigner

designer = ScenarioDesigner(
    model="carbon_market",
    baseline_data="current_economy.csv"
)

scenarios = designer.create_scenarios(
    variables={
        "carbon_price": [25, 50, 100, 150],
        "revenue_recycling": ["dividend", "tax_cut", "green_investment"],
        "coverage": ["power_sector", "all_sectors"]
    )
)
```

### Validation Framework

```yaml
validation:
  historical_backtest:
    enabled: true
    test_period: "2015-2023"
    metrics: ["rmse", "mae", "r_squared"]
  sensitivity_analysis:
    enabled: true
    parameters: ["all"]
    method: "sobol"
  uncertainty_quantification:
    enabled: true
    method: "monte_carlo"
    samples: 10000
```

## Architecture Patterns

### Simulation Architecture

```
┌─────────────────────────────────────────┐
│           Scenario Definition           │
│   (Parameters, Constraints, Assumptions)│
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│          Model Engine                   │
│   (ABM, SD, Microsimulation, CGE)       │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│          Analysis Layer                 │
│   (Statistics, Visualization, Reports)  │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│          Decision Support               │
│   (Recommendations, Tradeoffs)          │
└─────────────────────────────────────────┘
```

### Data Flow Architecture

```
Input Data → Scenario Setup → Simulation → Output Analysis → Reporting
    │            │               │              │              │
    ▼            ▼               ▼              ▼              ▼
  Census      Configure      Run Model    Statistical    Dashboards
  Surveys     Parameters     Multiple     Analysis       Reports
  Admin Data  Define         Scenarios    Compare        Recommendations
              Scenarios                   Scenarios
```

### Model Comparison Framework

```
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Agent      │  │   System     │  │   Micro-     │
│   Based      │  │   Dynamics   │  │   simulation │
│   Model      │  │   Model      │  │   Model      │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       └────────────────┬┘────────────────┘
                        │
                ┌───────▼───────┐
                │   Ensemble    │
                │   Results     │
                └───────────────┘
```

### Policy Evaluation Framework

```
Problem Definition → Model Selection → Calibration → Simulation → Evaluation
       │                │               │            │            │
       ▼                ▼               ▼            ▼            ▼
  Identify         Choose Appropriate Validate    Run Scenarios  Compare
  Policy           Model Type        Against     Analyze        Against
  Questions                          History     Results        Benchmarks
```

## Integration Guide

### Census Data Integration

```python
from policy_simulation import CensusConnector

census = CensusConnector(
    api_key="your-api-key",
    year=2020
)

# Get demographic data
demographics = census.get_demographics(
    geography="state",
    variables=["B01001_001E", "B19013_001E"]  # Population, Median Income
)

# Get housing data
housing = census.get_housing(
    geography="county",
    variables=["B25001_001E"]  # Housing units
)
```

### BLS Data Integration

```python
from policy_simulation import BLSConnector

bls = BLSConnector(api_key="your-api-key")

# Get employment data
employment = bls.get_series(
    series_id="LAUCN040000000000005",  # County unemployment
    time_range=("2020-01", "2024-01")
)

# Get CPI data
cpi = bls.get_cpi(
    item="CUSR0000SA0",  # All items
    time_range=("2020-01", "2024-01")
)
```

### IMPLAN Integration

```python
from policy_simulation import IMPLANConnector

implan = IMPLANConnector(
    region="California",
    year=2024
)

# Run economic impact analysis
impact = implan.analyze(
    scenario="carbon_tax",
    sectors=["energy", "manufacturing", "services"],
    multipliers=["type_I", "type_II"]
)

print(f"GDP impact: {impact.gdp_change:.2f}%")
print(f"Employment impact: {impact.employment_change:.0f} jobs")
```

### NetLogo Integration

```python
from policy_simulation import NetLogoBridge

netlogo = NetLogoBridge(
    model_path="models/city_growth.nlogo"
)

# Configure and run model
netlogo.setup(
    parameters={
        "population": 100000,
        "growth_rate": 0.02,
        "density_cap": 5000
    }
)

results = netlogo.run(ticks=1000)
```

## Performance Optimization

### Parallel Simulation

- **Ensemble runs**: Run multiple scenarios in parallel.
- **GPU acceleration**: Use GPU for agent-based models with many agents.
- **Distributed computing**: Distribute large simulations across clusters.

### Model Optimization

- **Agent reduction**: Use representative agents instead of full population.
- **Time step optimization**: Adaptive time stepping for faster convergence.
- **Caching**: Cache intermediate results for repeated runs.

### Data Processing

- **Streaming**: Process large datasets in streams.
- **Vectorization**: Use vectorized operations for statistical analysis.
- **Precomputation**: Pre-compute common transformations.

## Security Considerations

- **Data privacy**: Protect individual-level data used in microsimulation.
- **Model integrity**: Validate model assumptions and calibration.
- **Result interpretation**: Clearly communicate uncertainty and limitations.
- **Access control**: Restrict model access to authorized analysts.
- **Audit logging**: Track all model runs and parameter changes.

## Troubleshooting Guide

### Common Issues

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| Model non-convergence | Parameter instability | Adjust parameters, check calibration |
| Unrealistic results | Wrong assumptions | Review model assumptions |
| Slow simulation | Too many agents | Reduce agent count, optimize code |
| Memory overflow | Large dataset | Use streaming, increase memory |

## API Reference

### Core Classes

#### `SimulationEngine`

```python
class SimulationEngine:
    def __init__(self, model_type: str, config: SimulationConfig)
    def run_scenario(self, scenario: Scenario) -> SimulationResult
    def run_scenarios(self, scenarios: List[Scenario]) -> List[SimulationResult]
    def compare_results(self, results: List[SimulationResult]) -> ComparisonReport
    def validate(self, data: HistoricalData) -> ValidationReport
```

#### `ScenarioBuilder`

```python
class ScenarioBuilder:
    def set_baseline(self, data: BaselineData) -> None
    def add_intervention(self, name: str, params: Dict) -> None
    def add_constraint(self, constraint: Constraint) -> None
    def build(self) -> Scenario
```

## Data Models

### Simulation Schema

```sql
CREATE TABLE simulations (
    id UUID PRIMARY KEY,
    model_type VARCHAR(64) NOT NULL,
    scenario_name VARCHAR(256),
    parameters JSONB NOT NULL,
    status VARCHAR(32) NOT NULL,
    results JSONB,
    run_time_seconds FLOAT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_simulations_model ON simulations (model_type, created_at DESC);
```

## Deployment Guide

### Simulation Platform

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: policy-simulation
spec:
  replicas: 3
  selector:
    matchLabels:
      app: policy-simulation
  template:
    spec:
      containers:
        - name: api
          image: policy-simulation/api:latest
          ports:
            - containerPort: 8080
        - name: worker
          image: policy-simulation/worker:latest
          resources:
            limits:
              memory: "8Gi"
              cpu: "4"
```

## Monitoring & Observability

### Self-Monitoring Metrics

- `simulation_runs_total` — simulations completed.
- `simulation_duration_seconds` — simulation runtime.
- `simulation_scenarios_total` — scenarios evaluated.
- `simulation_validation_score` — model validation score.

## Testing Strategy

### Unit Testing

```python
def test_scenario_execution():
    engine = SimulationEngine(model_type="system_dynamics")
    scenario = ScenarioBuilder().set_baseline(test_data).build()
    result = engine.run_scenario(scenario)
    assert result.status == "completed"
    assert len(result.output_timeseries) > 0
```

## Versioning & Migration

- **v1.0.0**: Initial release with system dynamics modeling.
- **v1.1.0**: Added agent-based modeling and microsimulation.
- **v1.2.0**: CGE modeling and ensemble analysis.

## Glossary

| Term | Definition |
|------|-----------|
| ABM | Agent-Based Model |
| SD | System Dynamics |
| CGE | Computable General Equilibrium |
| Monte Carlo | Statistical method using random sampling |

## Changelog

### v1.2.0
- Added CGE modeling capabilities.
- Ensemble simulation framework.
- Enhanced validation tools.

### v1.1.0
- Added agent-based modeling.
- Microsimulation for tax policy.
- Historical backtesting.

### v1.0.0
- Initial release with system dynamics.
- Basic scenario comparison.

## Contributing Guidelines

1. Fork the repository and create a feature branch.
2. Write tests for all new functionality.
3. Follow the existing code style and naming conventions.
4. Update documentation for any API changes.
5. Add entries to the changelog for user-facing changes.
6. Submit a pull request with a clear description of changes.

### Climate Policy Simulation

```python
from policy_simulation import ClimatePolicySimulator

sim = ClimatePolicySimulator(
    model="integrated_assessment",
    base_year=2024,
    horizon=2060,
    regions=["US", "EU", "China", "India"]
)

# Run carbon tax scenario
result = sim.run_scenario(
    policy="carbon_tax",
    parameters={
        "starting_price": 50,
        "annual_increase": 5,
        "revenue_recycling": "dividend",
        "coverage": "power_sector_only"
    }
)

print(f"Emissions reduction: {result.emissions_change:.1%}")
print(f"GDP impact: {result.gdp_impact:.2%}")
print(f"Distributional effect: {result.distributional_impact}")
```

### Healthcare Policy Modeling

```yaml
healthcare_simulation:
  model_type: "microsimulation"
  population:
    size: 1000000
    source: "acs_pums_2022"
    representativeness: "national"
  policies:
    - name: "medicaid_expansion"
      parameters:
        eligibility_threshold: 138  # percent of poverty
        coverage_gap_close: true
    - name: "public_option"
      parameters:
        premium_subsidy: 0.5
        provider_reimbursement: "medicare_rate"
  outcomes:
    - "insurance_coverage_rate"
    - "out_of_pocket_spending"
    - "health_outcomes"
    - "federal_cost"
```

### Education Policy Analysis

```python
from policy_simulation import EducationPolicyAnalyzer

analyzer = EducationPolicyAnalyzer(
    model="student_progression",
    cohort_size=50000,
    time_horizon="k-12"
)

# Analyze school funding reform
result = analyzer.analyze(
    policy="weighted_student_funding",
    parameters={
        "base_funding": 10000,
        "poverty_weight": 0.5,
        "ell_weight": 0.3,
        "special_ed_weight": 0.4
    }
)

print(f"Achievement gap change: {result.gap_change:.2%}")
print(f"Cost change: ${result.cost_change:,.0f} per student")
print(f"Distributional impact: {result.distributional_analysis}")
```

### Housing Policy Simulation

```yaml
housing_simulation:
  market_model: "equilibrium"
  agents:
    households: 100000
    landlords: 5000
    developers: 200
  policies:
    - name: "inclusionary_zoning"
      parameters:
        set_aside_percent: 20
        depth_of_affordability: 60  # percent of AMI
    - name: "rent_control"
      parameters:
        cap_percent: 3
        exemptions: ["new_construction"]
    - name: "housing_vouchers"
      parameters:
        voucher_count: 5000
        payment_standard: "fair_market_rent"
```

### Transportation Policy Simulation

```python
from policy_simulation import TransportationSimulator

sim = TransportationSimulator(
    model="activity_based",
    network="regional_road_network",
    population="census_tracts"
)

# Analyze congestion pricing
result = sim.run_scenario(
    policy="congestion_pricing",
    parameters={
        "cordon_zone": "downtown",
        "toll_amount": 10,
        "time_of_day": "peak_hours",
        "exemptions": ["public_transit", "emergency"]
    }
)

print(f"Traffic reduction: {result.traffic_change:.1%}")
print(f"Transit ridership change: {result.transit_change:.1%}")
print(f"Revenue generated: ${result.revenue:,.0f}")
print(f"Air quality improvement: {result.emissions_change:.1%}")
```

### Labor Market Simulation

```yaml
labor_market_simulation:
  model_type: "agent_based"
  agents:
    workers: 500000
    firms: 10000
    sectors: ["manufacturing", "services", "technology", "healthcare"]
  policies:
    - name: "minimum_wage_increase"
      parameters:
        current_minimum: 7.25
        new_minimum: 15.00
        phase_in_period: "2y"
    - name: "universal_basic_income"
      parameters:
        monthly_payment: 1000
        funding_source: "income_tax"
  outcomes:
    - "employment_rate"
    - "wage_distribution"
    - "poverty_rate"
    - "gdp_impact"
```

### Environmental Justice Analysis

```python
from policy_simulation import EnvironmentalJusticeAnalyzer

analyzer = EnvironmentalJusticeAnalyzer(
    demographic_data="census_acs",
    environmental_data="epa_ejscreen"
)

# Analyze environmental justice impacts
ej_analysis = analyzer.analyze(
    policy="industrial_emission_reduction",
    vulnerable_populations=["low_income", "minority", "limited_english"]
)

print(f"Population in affected area: {ej_analysis.affected_population:,}")
print(f"Minority percentage: {ej_analysis.minority_percentage:.1%}")
print(f"Low income percentage: {ej_analysis.low_income_percentage:.1%}")
print(f"Environmental benefit: {ej_analysis.environmental_benefit}")
```

### Economic Impact Dashboard

```yaml
economic_dashboard:
  indicators:
    - name: "gdp_growth"
      source: "bea"
      frequency: "quarterly"
    - name: "unemployment_rate"
      source: "bls"
      frequency: "monthly"
    - name: "inflation_rate"
      source: "bls"
      frequency: "monthly"
    - name: "poverty_rate"
      source: "census"
      frequency: "annual"
  scenarios:
    - name: "baseline"
      description: "Current policy trajectory"
    - name: "optimistic"
      description: "Proactive policy implementation"
    - name: "pessimistic"
      description: "Policy stagnation"
```

### Policy Sensitivity Analysis

```python
from policy_simulation import SensitivityAnalyzer

analyzer = SensitivityAnalyzer(
    method="sobol",
    parameters=["carbon_price", "discount_rate", "population_growth", "technology_change"],
    samples=10000
)

# Run sensitivity analysis
sensitivity = analyzer.analyze(
    model=climate_model,
    output_metric="emissions_reduction"
)

for param, index in sensitivity.indices.items():
    print(f"{param}: {index:.3f}")
```

### Policy Scenario Comparison

```python
from policy_simulation import ScenarioComparator

comparator = ScenarioComparator(
    metrics=["emissions", "gdp", "employment", "equity"]
)

# Compare scenarios
comparison = comparator.compare(
    scenarios=["baseline", "carbon_tax", "cap_trade", "regulation"],
    baseline="baseline"
)

for scenario, results in comparison.items():
    print(f"\n{scenario}:")
    for metric, value in results.items():
        print(f"  {metric}: {value:+.2f}%")
```

## Advanced Simulation Techniques

### Monte Carlo Policy Risk Analysis

```python
import numpy as np
from policy_simulation import MonteCarloPolicyAnalyzer

analyzer = MonteCarloPolicyAnalyzer(
    policy="minimum_wage_increase",
    n_simulations=10000,
    confidence_level=0.95
)

# Define uncertain parameters with distributions
param_distributions = {
    "current_wage": {"type": "uniform", "low": 12.0, "high": 15.0},
    "elasticity_labor_demand": {"type": "normal", "mean": -0.3, "std": 0.1},
    "elasticity_labor_supply": {"type": "normal", "mean": 0.1, "std": 0.05},
    "price_elasticity": {"type": "triangular", "left": 0.01, "mode": 0.05, "right": 0.15},
    "regional_cost_of_living": {"type": "lognormal", "mean": 1.0, "std": 0.2}
}

# Run Monte Carlo simulation
results = analyzer.run(
    param_distributions=param_distributions,
    output_metrics=["employment_change", "wage_growth", "price_impact", "poverty_reduction"],
    seed=42
)

# Analyze risk distribution
print(f"Employment change: {results.mean('employment_change'):+.2f}% ± {results.std('employment_change'):.2f}%")
print(f"95% CI for employment: [{results.ci('employment_change', 0.025):.2f}%, {results.ci('employment_change', 0.975):.2f}%]")
print(f"Probability of net job loss: {results.probability('employment_change', '<', 0):.1%}")

# Sensitivity analysis
tornado = analyzer.sensitivity_tornado(results, metric="employment_change")
for param, impact in tornado.items():
    print(f"  {param}: ±{impact:.2f}pp")
```

### Agent-Based Policy Model

```python
from policy_simulation import AgentBasedModel, PolicyAgent

# Define agent types
class Household(PolicyAgent):
    agent_type = "household"

    def __init__(self, income, family_size, education, location):
        self.income = income
        self.family_size = family_size
        self.education = education
        self.location = location
        self.savings = 0
        self.health_status = "good"

    def step(self, policy_context):
        # Respond to tax policy
        tax_liability = policy_context.calculate_tax(self.income)
        take_home = self.income - tax_liability

        # Respond to social programs
        if self.income < policy_context.poverty_line:
            self.savings += policy_context.benefit_amount
        else:
            self.savings += (take_home - policy_context.cost_of_living) * 0.1

        # Health outcome depends on insurance coverage
        if policy_context.health_insurance覆盖率 > 0.9:
            self.health_status = "improved"

class Business(PolicyAgent):
    agent_type = "business"

    def __init__(self, sector, employees, revenue):
        self.sector = sector
        self.employees = employees
        self.revenue = revenue
        self.hiring_intent = 0

    def step(self, policy_context):
        # Respond to tax incentives
        tax_benefit = policy_context.get_incentive(self.sector)
        self.hiring_intent = min(1.0, tax_benefit * self.revenue / 1e6)

# Build simulation
model = AgentBasedModel(
    agents=[Household, Business],
    spatial_grid="census_tracts",
    time_step="monthly",
    duration_months=60
)

# Load baseline population
model.load_population(
    source="census_2020",
    demographics=["income", "family_size", "education", "employment"]
)

# Configure policy intervention
policy = model.define_policy(
    name="progressive_tax_reform",
    parameters={
        "bracket_changes": [
            {"range": [0, 30000], "rate": 0.10},
            {"range": [30000, 80000], "rate": 0.22},
            {"range": [80000, 200000], "rate": 0.32},
            {"range": [200000, float("inf")], "rate": 0.37}
        ],
        "standard_deduction": 14600,
        "child_tax_credit": 2000,
        "earned_income_credit": {
            "max_credit": 7430,
            "phase_out_start": 20000
        }
    }
)

# Run simulation
results = model.simulate(
    baseline_scenarios=["no_reform"],
    policy_scenarios=["progressive_tax_reform"],
    collect_metrics=["gini_coefficient", "poverty_rate", "median_income", "employment_rate"]
)

# Compare outcomes
comparison = model.compare(results)
print(f"Gini change: {comparison.difference('gini_coefficient'):+.3f}")
print(f"Poverty rate change: {comparison.difference('poverty_rate'):+.1f}pp")
```

### Dynamic Scoring Engine

```python
from policy_simulation import DynamicScorer, MacroEconomicLinkage

scorer = DynamicScorer(
    gdp_model="dsge",
    labor_market="search_matching",
    fiscal_module="tax_simulator"
)

# Configure macroeconomic linkages
linkages = [
    MacroEconomicLinkage(
        policy="infrastructure_spending",
        macro_channel="government_spending",
        gdp_multiplier=1.5,
        lag_months=6
    ),
    MacroEconomicLinkage(
        policy="tax_cut",
        macro_channel="disposable_income",
        marginal_propensity=0.6,
        lag_months=3
    ),
    MacroEconomicLinkage(
        policy="regulation",
        macro_channel="business_investment",
        compliance_cost_factor=0.02,
        innovation_offset=0.01
    )
]

# Score policy over 10-year horizon
score = scorer.score(
    policy="bipartisan_infrastructure_bill",
    cost=1200e9,
    duration_years=10,
    linkages=linkages,
    dynamic_effects=True,
    feedback_loops=True
)

print(f"Static cost: ${score.static_cost/1e9:.0f}B")
print(f"Dynamic cost: ${score.dynamic_cost/1e9:.0f}B")
print(f"GDP impact (10yr): {score.gdp_impact:+.2f}%")
print(f"Job creation: {score.jobs_created:,.0f}")
print(f"Revenue feedback: ${score.revenue_feedback/1e9:+.0f}B")
```

### Spatial Policy Impact Mapping

```python
from policy_simulation import SpatialImpactMapper

mapper = SpatialImpactMapper(
    geographic_level="census_tract",
    projection="EPSG:4326",
    data_format="geopackage"
)

# Map zoning policy impact
impact_map = mapper.analyze(
    policy="inclusionary_zoning",
    parameters={
        "required_affordable_pct": 20,
        "area_of_impact": "city_boundary",
        "buffer_zones": [0.25, 0.5, 1.0],  # miles
        "metrics": ["housing_affordability", "displacement_risk", "transit_access"]
    }
)

# Identify impacted populations
populations = mapper.identify_vulnerable(
    impact_map,
    criteria={
        "current_rent_burden": ">30%_income",
        "poverty_rate": ">20%",
        "senior_population": ">15%",
        "minority_population": ">40%"
    }
)

# Export for GIS visualization
mapper.export(
    impact_map,
    format="geojson",
    filename="zoning_impact_map.geojson",
    include_metadata=True,
    style_hints={
        "displacement_risk": {"color": "red", "opacity": 0.7},
        "housing_affordability": {"color": "green", "opacity": 0.5}
    }
)
```

### Cross-Policy Interaction Matrix

```python
from policy_simulation import PolicyInteractionAnalyzer

analyzer = PolicyInteractionAnalyzer(
    policies=["carbon_tax", "cap_trade", "renewable_subsidy", "efficiency_standard"],
    interaction_types=["synergistic", "antagonistic", "redundant"]
)

# Analyze pairwise interactions
matrix = analyzer.compute_interactions(
    baseline="current_policy_mix",
    new_policies=["carbon_tax", "renewable_subsidy"],
    outcome_metric="emissions_reduction"
)

# Print interaction matrix
print("Policy Interaction Matrix:")
for p1 in matrix.policies:
    for p2 in matrix.policies:
        interaction = matrix.get(p1, p2)
        if p1 != p2:
            print(f"  {p1} × {p2}: {interaction.type} ({interaction.magnitude:+.2f})")

# Find optimal policy bundle
optimal = analyzer.find_optimal_bundle(
    target_emissions_reduction=0.5,
    budget_constraint=100e9,
    constraints=["political_feasibility", "implementation_timeline"]
)
print(f"\nOptimal bundle: {optimal.policies}")
print(f"Expected reduction: {optimal.outcome:.1%}")
print(f"Total cost: ${optimal.cost/1e9:.1f}B")
```

## License

MIT License. See the root LICENSE file for full terms.

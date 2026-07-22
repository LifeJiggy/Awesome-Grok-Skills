---
name: "risk-assessment"
category: "security-assessment"
version: "2.0.0"
tags: ["security-assessment", "risk-assessment", "quantitative", "FAIR", "business-impact", "monte-carlo"]
---

# Risk Assessment Module

## Overview

The Risk Assessment module provides structured, repeatable methodology for identifying, analyzing, and evaluating security risks in terms of business impact and likelihood. It implements quantitative risk analysis using FAIR (Factor Analysis of Information Risk) methodology, qualitative risk matrices aligned with ISO 27005 and NIST SP 800-30, and Monte Carlo simulation for probabilistic risk modeling. The module transforms raw vulnerability and threat data into business-contextualized risk statements that enable informed investment decisions.

Designed for enterprise security programs, the module bridges the gap between technical vulnerability findings and business risk language that executives and boards understand. It supports multiple risk analysis frameworks simultaneously, allowing organizations to apply the right methodology for each decision context—from rapid qualitative assessments for operational prioritization to rigorous quantitative analysis for capital allocation decisions.

The module's Monte Carlo simulation engine provides statistically grounded probability distributions rather than single-point estimates, giving decision-makers visibility into uncertainty ranges and tail risk scenarios. This probabilistic approach is essential for accurately modeling low-frequency, high-impact events like data breaches, ransomware attacks, and supply chain compromises.

## Core Capabilities

1. **FAIR Quantitative Analysis** — Model risk scenarios using FAIR taxonomy with loss event frequency, loss magnitude, and probable loss magnitude ranges. Run Monte Carlo simulations for confidence intervals and expected annual loss calculations.

2. **Qualitative Risk Matrices** — Generate risk matrices with configurable likelihood/impact scales, heat maps, and risk appetite thresholds per organizational risk tolerance with visual dashboard integration.

3. **Business Impact Analysis** — Map technical vulnerabilities to business processes, revenue impact, regulatory exposure, and reputational damage categories with quantifiable financial metrics.

4. **Risk Register Management** — Maintain living risk registers with ownership, treatment plans, residual risk tracking, and audit trails with full version history and approval workflows.

5. **Scenario Modeling** — Model "what-if" scenarios for risk treatment options (accept, mitigate, transfer, avoid) with cost-benefit analysis and break-even calculations.

6. **Regulatory Risk Mapping** — Correlate risk findings with regulatory frameworks (GDPR, HIPAA, PCI DSS, SOX) for compliance-driven risk prioritization and fine estimation.

7. **Risk Aggregation** — Aggregate risks across business units, technology stacks, and asset portfolios to provide enterprise-wide risk visibility and portfolio-level analysis.

8. **Historical Trend Analysis** — Track risk posture over time with trend analysis, risk velocity calculations, and benchmarking against industry peers and historical baselines.

## Usage Examples

### FAIR Risk Quantification

```python
from security_assessment.risk_assessment import FAIRAnalyzer

analyzer = FAIRAnalyzer(simulations=10000)
scenario = analyzer.model_scenario(
    threat_event_frequency=100,  # per year
    vulnerability_rate=0.3,       # probability of exploitation
    loss_magnitude_min=50000,     # USD
    loss_magnitude_max=500000,
    confidence=0.95
)

print(f"Annual Loss Expectancy: ${scenario.ale:,.0f}")
print(f"95th percentile loss: ${scenario.percentile_95:,.0f}")
print(f"Risk rating: {scenario.risk_rating}")
print(f"Confidence interval: ${scenario.ci_lower:,.0f} - ${scenario.ci_upper:,.0f}")
```

### Qualitative Risk Matrix

```python
from security_assessment.risk_assessment import RiskMatrix

matrix = RiskMatrix(
    likelihood_scale=5,  # 1=Rare, 2=Unlikely, 3=Possible, 4=Likely, 5=Almost Certain
    impact_scale=5,      # 1=Negligible, 2=Minor, 3=Moderate, 4=Major, 5=Catastrophic
    appetite={
        "high": 15,   # score above this = unacceptable
        "medium": 8,  # score above this = requires treatment
        "low": 3      # below this = acceptable
    }
)

risks = [
    {"id": "R001", "likelihood": 4, "impact": 5, "title": "SQL Injection on payment API"},
    {"id": "R002", "likelihood": 2, "impact": 3, "title": "Missing MFA on admin panel"},
    {"id": "R003", "likelihood": 3, "impact": 4, "title": "Unencrypted data at rest"},
]

matrix.populate(risks)
print(matrix.heatmap())
print(f"Risks above appetite: {matrix.exceeds_appetite()}")
```

### Business Impact Analysis

```python
from security_assessment.risk_assessment import BusinessImpactAnalyzer

bia = BusinessImpactAnalyzer()
bia.load_asset_inventory("assets.yaml")

impact = bia.assess(
    threat="Ransomware",
    assets=["payment-system", "customer-database", "email-server"],
    factors={
        "revenue_per_hour": 50000,
        "regulatory_fine_max": 2000000,
        "customer_count": 100000,
        "reputation_recovery_days": 90
    }
)

print(f"Total Business Impact: ${impact.total_impact:,.0f}")
print(f"  Revenue Loss: ${impact.revenue_loss:,.0f}")
print(f"  Regulatory Exposure: ${impact.regulatory_fine:,.0f}")
print(f"  Recovery Time: {impact.recovery_hours}h")
```

### Risk Register with Treatment Plans

```python
from security_assessment.risk_assessment import RiskRegister

register = RiskRegister()
register.add_risk(
    id="R001",
    title="SQL Injection on payment processing API",
    category="Application Security",
    inherent_risk_score=20,
    owner="security-team",
    treatment="mitigate",
    controls=["WAF rules", "Parameterized queries", "Input validation"],
    target_date="2026-08-01"
)

register.update_residual_risk("R001", score=4, rationale="WAF + parameterization reduces exposure")
export = register.export_compliance_report(format="iso27005")
```

### Monte Carlo Risk Simulation

```python
from security_assessment.risk_assessment import MonteCarloSimulator

sim = MonteCarloSimulator(iterations=10000)
sim.add_scenario(
    name="Cloud Data Breach",
    frequency_dist="poisson",
    frequency_params={"lambda": 2.5},
    magnitude_dist="lognormal",
    magnitude_params={"mu": 12, "sigma": 1.5}
)

results = sim.run()
print(f"Expected Annual Loss: ${results.mean:,.0f}")
print(f"Value at Risk (95%): ${results.var_95:,.0f}")
print(f"Probability of >$1M loss: {results.exceedance_probability(1000000):.1%}")
```

### Treatment Cost-Benefit Analysis

```python
from security_assessment.risk_assessment import TreatmentAnalyzer

analyzer = TreatmentAnalyzer()
options = analyzer.compare(
    risk_id="R001",
    treatments=[
        {"type": "mitigate", "cost": 50000, "residual_risk": 4},
        {"type": "transfer", "cost": 20000, "residual_risk": 6},
        {"type": "accept", "cost": 0, "residual_risk": 18}
    ],
    annual_loss_expectancy=150000
)

for option in options:
    print(f"{option.type}: Cost=${option.cost:,.0f}, "
          f"Residual={option.residual_risk}, "
          f"ROI={option.roi:.1%}")
    print(f"  Break-even: {option.breakeven_months:.1f} months")
```

## Architecture

```
┌───────────────────────────────────────────────────┐
│                Risk Assessment Module              │
├─────────────┬───────────────┬─────────────────────┤
│  Quantit.   │  Qualitative  │   Business Impact   │
│  Engine     │  Engine       │   Analysis          │
├─────────────┼───────────────┼─────────────────────┤
│ FAIR Model  │ Risk Matrix   │ Process Mapping     │
│ Monte Carlo │ Heat Maps     │ Revenue Impact      │
│ VaR Calc   │ Appetite Mgmt │ Regulatory Exposure │
│ Sensitivity │ Trend Analysis│ Recovery Modeling   │
├─────────────┴───────────────┴─────────────────────┤
│              Risk Register & Workflow Engine        │
├───────────────────────────────────────────────────┤
│  Treatment  │  Compliance  │  Reporting           │
│  Planning   │  Mapping     │  Dashboard           │
└───────────────────────────────────────────────────┘
```

The module operates on a three-layer architecture: quantitative and qualitative analysis engines feed into a unified risk register, which drives treatment planning and compliance mapping. The reporting layer provides role-specific views for executives, management, and operational teams.

## Best Practices

1. **Use Both Quantitative and Qualitative** — Quantitative (FAIR) for high-stakes decisions requiring board-level communication; qualitative for operational prioritization and rapid assessment.

2. **Calibrate Estimates** — Use structured estimation techniques (Delphi method, reference class forecasting) to reduce cognitive bias in likelihood/impact estimates.

3. **Document Assumptions** — Every risk model rests on assumptions. Maintain an assumptions register with sources and confidence levels for auditability.

4. **Update Risk Models** — Re-run risk analysis quarterly or after significant changes (new threats, control failures, business changes, incidents).

5. **Risk Appetite Statement** — Establish organizational risk appetite before modeling. Risk without appetite context is noise.

6. **Cascade Risk Views** — Provide risk views at executive (portfolio), management (program), and operational (asset) levels with appropriate detail.

7. **Scenario Variety** — Model both high-frequency/low-impact and low-frequency/high-impact scenarios. Tail risk kills organizations.

8. **Sensitivity Analysis** — Run sensitivity analysis to identify which variables most affect risk outcomes and focus monitoring on those inputs.

9. **Peer Benchmarking** — Compare risk metrics against industry benchmarks to validate assumptions and identify blind spots.

## Performance Considerations

- Monte Carlo simulations with 10,000+ iterations complete in under 5 seconds for typical risk scenarios; increase iterations only for high-precision requirements.
- Risk matrix generation with >1,000 risks requires efficient rendering; use heat map aggregation for visualization.
- Historical trend analysis benefits from database indexing on risk IDs and timestamps for fast query response.
- FAIR model parameter estimation can be time-consuming; consider caching calibrated parameters for recurring scenarios.
- Treatment cost-benefit analysis scales linearly with the number of treatment options; limit to 5-7 options per comparison.

## Security Considerations

- Risk register data contains sensitive business information; restrict access based on role and need-to-know.
- Monte Carlo simulation parameters may reveal organizational vulnerability profiles; protect simulation configurations.
- Business impact analysis data (revenue, customer counts, regulatory exposure) is confidential; encrypt at rest and in transit.
- Risk treatment plans may reference security controls; avoid storing control implementations in risk documents.
- Audit trails must be tamper-proof to maintain risk management integrity for compliance purposes.

## Related Modules

- `vulnerability-assessment` — Technical inputs for risk analysis (CVSS, exploitability, asset exposure data)
- `compliance-audit` — Regulatory risk mapping and compliance obligation tracking with fine estimation
- `penetration-testing` — Validated threat scenarios for realistic risk modeling and attack path analysis
- `security-review` — Control effectiveness assessment for residual risk calculation and control gap analysis

## Configuration Reference

```yaml
# risk_assessment_config.yaml
analysis:
  method: fair  # fair | qualitative | hybrid
  monte_carlo_iterations: 10000
  confidence_level: 0.95

risk_matrix:
  likelihood_scale: 5  # 1-5 scale
  impact_scale: 5  # 1-5 scale
  appetite:
    high: 15
    medium: 8
    low: 3

business_impact:
  revenue_per_hour: 50000
  regulatory_fine_max: 2000000
  customer_count: 100000
  reputation_recovery_days: 90

reporting:
  formats: ["html", "json", "pdf"]
  include_heatmap: true
  include_trend_analysis: true
  executive_summary: true
```

## Integration Guide

The module integrates with common security and business tools:

- **Vulnerability Scanners** — Import findings from Nessus, Qualys, OpenVAS, and custom scanners for risk quantification.
- **Asset Management** — Pull asset criticality data from CMDB systems for context-aware risk scoring.
- **SIEM Integration** — Correlate risk assessments with security events for dynamic risk recalculation.
- **GRC Platforms** — Export risk registers to governance, risk, and compliance platforms for enterprise visibility.

## Detailed FAIR Model Implementation

### FAIR Taxonomy Deep Dive

```python
from security_assessment.risk_assessment import FAIRTaxonomy

taxonomy = FAIRTaxonomy()

# Define a complete FAIR model for ransomware scenario
scenario = taxonomy.create_scenario(
    name="Ransomware Attack on Production Systems",
    loss_event_frequency={
        "threat_agent_capability": {
            "value": "high",
            "rationale": "Active ransomware groups targeting similar industries"
        },
        "threat_agent_volume": {
            "value": "moderate",
            "rationale": "Estimated 10-50 active groups in sector"
        },
        "vulnerability": {
            "value": "moderate",
            "rationale": "Current patching cadence leaves 15-day window"
        },
        "contact_opportunity": {
            "value": "high",
            "rationale": "Internet-facing applications with broad access"
        }
    },
    loss_magnitude={
        "primary_loss": {
            "productivity_loss": {"min": 100000, "max": 500000, "most_likely": 250000},
            "response_costs": {"min": 50000, "max": 200000, "most_likely": 100000},
            "replacement_costs": {"min": 0, "max": 500000, "most_likely": 100000}
        },
        "secondary_loss": {
            "competitive_advantage": {"min": 0, "max": 1000000, "most_likely": 200000},
            "reputation": {"min": 50000, "max": 2000000, "most_likely": 500000},
            "regulatory_fines": {"min": 0, "max": 5000000, "most_likely": 1000000}
        }
    }
)

# Run FAIR analysis
analysis = taxonomy.analyze(
    scenario=scenario,
    simulations=10000,
    confidence_levels=[0.50, 0.75, 0.90, 0.95, 0.99]
)

print(f"FAIR Analysis Results:")
print(f"  Annual Loss Expectancy: ${analysis.ale:,.0f}")
print(f"  50th percentile: ${analysis.percentile_50:,.0f}")
print(f"  75th percentile: ${analysis.percentile_75:,.0f}")
print(f"  90th percentile: ${analysis.percentile_90:,.0f}")
print(f"  95th percentile: ${analysis.percentile_95:,.0f}")
print(f"  99th percentile: ${analysis.percentile_99:,.0f}")
print(f"  Standard deviation: ${analysis.std_dev:,.0f}")

# Sensitivity analysis
sensitivity = taxonomy.sensitivity_analysis(
    scenario=scenario,
    variables=["threat_agent_capability", "vulnerability", "contact_opportunity"],
    simulations=5000
)

print(f"\nSensitivity Analysis:")
for var in sensitivity.variables:
    print(f"  {var.name}: elasticity={var.elasticity:.2f}")
    print(f"    10% increase in {var.name} → {var.impact_on_ale:.1f}% increase in ALE")
```

### Monte Carlo Simulation Engine

```python
from security_assessment.risk_assessment import MonteCarloEngine

engine = MonteCarloEngine(iterations=50000)

# Define multiple correlated scenarios
engine.add_scenario(
    name="Data Breach",
    frequency_distribution="poisson",
    frequency_params={"lambda": 2.5},
    magnitude_distribution="lognormal",
    magnitude_params={"mu": 14.5, "sigma": 1.8},
    correlation_group="breach_events"
)

engine.add_scenario(
    name="Insider Threat",
    frequency_distribution="poisson",
    frequency_params={"lambda": 1.2},
    magnitude_distribution="triangular",
    magnitude_params={"left": 10000, "mode": 75000, "right": 500000},
    correlation_group="insider_events"
)

engine.add_scenario(
    name="DDoS Attack",
    frequency_distribution="negative_binomial",
    frequency_params={"r": 3, "p": 0.4},
    magnitude_distribution="lognormal",
    magnitude_params={"mu": 11, "sigma": 2.0},
    correlation_group="availability_events"
)

# Configure correlation matrix
engine.set_correlation_matrix({
    ("Data Breach", "Insider Threat"): 0.3,
    ("Data Breach", "DDoS Attack"): 0.1,
    ("Insider Threat", "DDoS Attack"): 0.05
})

# Run simulation
results = engine.run(seed=42)

print("Portfolio Risk Analysis:")
print(f"  Total Expected Annual Loss: ${results.portfolio_ale:,.0f}")
print(f"  Value at Risk (95%): ${results.portfolio_var_95:,.0f}")
print(f"  Value at Risk (99%): ${results.portfolio_var_99:,.0f}")
print(f"  Tail Value at Risk (95%): ${results.portfolio_tvar_95:,.0f}")

# Scenario breakdown
for scenario_result in results.scenario_results:
    print(f"\n  {scenario_result.name}:")
    print(f"    ALE: ${scenario_result.ale:,.0f}")
    print(f"    VaR (95%): ${scenario_result.var_95:,.0f}")
    print(f"    Probability of >$1M loss: {scenario_result.exceedance_probability(1000000):.1%}")

# Loss exceedance curve
curve = results.loss_exceedance_curve()
print(f"\nLoss Exceedance Curve:")
for point in curve.points:
    print(f"  ${point.loss:,.0f}: {point.probability:.1%} annual probability")
```

## Business Impact Analysis Workflows

### Revenue Impact Modeling

```python
from security_assessment.risk_assessment import BusinessImpactModel

model = BusinessImpactModel()

# Model ransomware impact on revenue
revenue_impact = model.model_revenue_impact(
    threat="ransomware",
    business_processes=[
        {
            "name": "E-commerce Platform",
            "revenue_per_hour": 50000,
            "mttr_hours": 48,
            "customers_affected": 10000,
            "recovery_probability": 0.85
        },
        {
            "name": "Payment Processing",
            "revenue_per_hour": 100000,
            "mttr_hours": 24,
            "customers_affected": 50000,
            "recovery_probability": 0.90
        },
        {
            "name": "Customer Support",
            "revenue_per_hour": 10000,
            "mttr_hours": 72,
            "customers_affected": 20000,
            "recovery_probability": 0.75
        }
    ],
    additional_factors={
        "contractual_penalties_per_hour": 5000,
        "sla_breach_probability": 0.6,
        "customer_churn_rate_post_incident": 0.05,
        "customer_lifetime_value": 2500
    }
)

print("Revenue Impact Analysis:")
for process in revenue_impact.process_impacts:
    print(f"\n  {process.name}:")
    print(f"    Direct revenue loss: ${process.direct_loss:,.0f}")
    print(f"    Contractual penalties: ${process.penalties:,.0f}")
    print(f"    Customer churn cost: ${process.churn_cost:,.0f}")
    print(f"    Total impact: ${process.total_impact:,.0f}")
    print(f"    Recovery time: {process.recovery_hours}h")

print(f"\nTotal Revenue Impact: ${revenue_impact.total_impact:,.0f}")
print(f"  Direct losses: ${revenue_impact.direct_losses:,.0f}")
print(f"  Indirect losses: ${revenue_impact.indirect_losses:,.0f}")
print(f"  Regulatory exposure: ${revenue_impact.regulatory_exposure:,.0f}")
```

### Regulatory Fine Estimation

```python
from security_assessment.risk_assessment import RegulatoryFineEstimator

estimator = RegulatoryFineEstimator()

# Estimate GDPR fine
gdpr_fine = estimator.estimate_gdpr_fine(
    violation_type="unauthorized_access",
    records_affected=500000,
    data_categories=["health", "financial", "biometric"],
    company_revenue_annual=100000000,
    company_turnover_global=500000000,
    aggravating_factors=[
        "inadequate_security_measures",
        "delayed_breach_notification",
        "previous_violations"
    ],
    mitigating_factors=[
        "cooperation_with_authority",
        "data_protection_officer_appointed"
    ]
)

print("GDPR Fine Estimation:")
print(f"  Maximum fine (4% turnover): ${gdpr_fine.max_fine:,.0f}")
print(f"  Estimated fine: ${gdpr_fine.estimated_fine:,.0f}")
print(f"  Fine range: ${gdpr_fine.fine_range_low:,.0f} - ${gdpr_fine.fine_range_high:,.0f}")
print(f"  Confidence: {gdpr_fine.confidence:.0%}")
print(f"\n  Aggravating factors:")
for factor in gdpr_fine.aggravating_factors:
    print(f"    + {factor.description}: {factor.impact_percent:.0%} increase")
print(f"  Mitigating factors:")
for factor in gdpr_fine.mitigating_factors:
    print(f"    - {factor.description}: {factor.impact_percent:.0%} decrease")

# Estimate HIPAA fine
hipaa_fine = estimator.estimate_hipaa_fine(
    violation_type="unauthorized_access",
    records_affected=100000,
    violation_category="willful_neglect",
    correction_period_days=60
)

print(f"\nHIPAA Fine Estimation:")
print(f"  Category: {hipaa_fine.violation_category}")
print(f"  Per-violation minimum: ${hipaa_fine.per_violation_min:,.0f}")
print(f"  Per-violation maximum: ${hipaa_fine.per_violation_max:,.0f}")
print(f"  Total estimated fine: ${hipaa_fine.estimated_total:,.0f}")
```

## Risk Register Management

### Enterprise Risk Register

```python
from security_assessment.risk_assessment import EnterpriseRiskRegister

register = EnterpriseRiskRegister()

# Bulk import risks from vulnerability scan
importer = register.importer()
importer.from_vulnerability_scan(
    scan_results="./scans/weekly-scan.json",
    asset_inventory="./assets/cmdb-export.yaml",
    mapping_rules=[
        {"cvss_range": [9.0, 10.0], "inherent_risk": "critical"},
        {"cvss_range": [7.0, 8.9], "inherent_risk": "high"},
        {"cvss_range": [4.0, 6.9], "inherent_risk": "medium"},
        {"cvss_range": [0.1, 3.9], "inherent_risk": "low"}
    ]
)

# Create risk with full treatment plan
risk = register.create_risk(
    id="R-2025-042",
    title="SQL Injection in Payment API",
    description="Unparameterized SQL queries in payment processing API allow data extraction",
    category="Application Security",
    owner="platform-team",
    inherent_risk={
        "likelihood": 4,
        "impact": 5,
        "score": 20,
        "rating": "critical"
    },
    treatment={
        "strategy": "mitigate",
        "controls": [
            "Parameterized queries for all database access",
            "WAF rules for SQL injection patterns",
            "Input validation library integration",
            "Automated SAST scanning in CI/CD"
        ],
        "target_date": "2025-08-01",
        "estimated_cost": 25000,
        "responsible_person": "dev-lead"
    }
)

# Track remediation progress
register.update_risk(
    risk_id="R-2025-042",
    status="in_progress",
    progress_percent=60,
    evidence=[
        {"type": "code_commit", "ref": "abc123", "description": "Parameterized queries implemented"},
        {"type": "scan_result", "ref": "sast-scan-001", "description": "SAST scan clean"}
    ]
)

# Calculate residual risk after remediation
residual = register.calculate_residual_risk(
    risk_id="R-2025-042",
    control_effectiveness={
        "parameterized_queries": 0.95,
        "waf_rules": 0.70,
        "input_validation": 0.80,
        "sast_scanning": 0.85
    }
)

print(f"Residual Risk Assessment:")
print(f"  Original score: {risk.inherent_risk['score']}")
print(f"  Residual score: {residual.score}")
print(f"  Risk reduction: {residual.reduction_percent:.0f}%")
print(f"  New rating: {residual.rating}")
```

### Risk Treatment Cost-Benefit Analysis

```python
from security_assessment.risk_assessment import TreatmentCostBenefit

analyzer = TreatmentCostBenefit()

# Compare treatment options
comparison = analyzer.compare_treatments(
    risk_id="R-2025-042",
    annual_loss_expectancy=150000,
    treatments=[
        {
            "name": "Full remediation",
            "type": "mitigate",
            "cost": 75000,
            "implementation_time_months": 3,
            "residual_risk_score": 3,
            "ongoing_cost_annual": 10000
        },
        {
            "name": "Partial remediation + insurance",
            "type": "mitigate_transfer",
            "cost": 30000,
            "implementation_time_months": 1,
            "residual_risk_score": 6,
            "ongoing_cost_annual": 20000,  # insurance premium
            "insurance_coverage": 500000
        },
        {
            "name": "Accept risk",
            "type": "accept",
            "cost": 0,
            "implementation_time_months": 0,
            "residual_risk_score": 18,
            "ongoing_cost_annual": 0
        },
        {
            "name": "Decommission affected service",
            "type": "avoid",
            "cost": 100000,
            "implementation_time_months": 6,
            "residual_risk_score": 1,
            "ongoing_cost_annual": 0,
            "revenue_impact_annual": -200000
        }
    ]
)

print("Treatment Cost-Benefit Analysis:")
for option in comparison.options:
    print(f"\n  {option.name} ({option.type}):")
    print(f"    Upfront cost: ${option.cost:,.0f}")
    print(f"    Annual ongoing: ${option.ongoing_cost_annual:,.0f}")
    print(f"    5-year total cost: ${option.five_year_cost:,.0f}")
    print(f"    Risk reduction: {option.risk_reduction_percent:.0f}%")
    print(f"    ROI: {option.roi:.1%}")
    print(f"    Break-even: {option.breakeven_months:.1f} months")
    print(f"    Recommendation: {option.recommendation}")
```

## Risk Aggregation and Portfolio Analysis

### Enterprise Risk Portfolio

```python
from security_assessment.risk_assessment import RiskPortfolio

portfolio = RiskPortfolio()

# Load risks from multiple business units
portfolio.load_risks([
    {"source": "engineering", "risks": engineering_risks},
    {"source": "finance", "risks": finance_risks},
    {"source": "operations", "risks": operations_risks},
    {"source": "hr", "risks": hr_risks}
])

# Aggregate by category
aggregation = portfolio.aggregate(
    group_by=["category", "owner", "business_unit"],
    include_correlation=True
)

print("Risk Portfolio Summary:")
print(f"  Total risks: {aggregation.total_count}")
print(f"  Critical: {aggregation.critical_count}")
print(f"  High: {aggregation.high_count}")
print(f"  Medium: {aggregation.medium_count}")
print(f"  Low: {aggregation.low_count}")

# Category breakdown
for category in aggregation.categories:
    print(f"\n  {category.name}:")
    print(f"    Count: {category.count}")
    print(f"    Average score: {category.avg_score:.1f}")
    print(f"    Portfolio value at risk: ${category.var:,.0f}")

# Business unit breakdown
for unit in aggregation.business_units:
    print(f"\n  {unit.name}:")
    print(f"    Risks: {unit.risk_count}")
    print(f"    Total exposure: ${unit.total_exposure:,.0f}")
    print(f"    Top risk: {unit.top_risk.title}")

# Correlation analysis
correlations = portfolio.correlation_analysis()
print(f"\nRisk Correlations:")
for corr in correlations.significant_correlations:
    print(f"  {corr.risk_a.title} ↔ {corr.risk_b.title}")
    print(f"    Correlation: {corr.coefficient:.2f}")
    print(f"    Impact: {corr.portfolio_impact}")
```

### Risk Trend Analysis

```python
from security_assessment.risk_assessment import RiskTrendAnalyzer

analyzer = RiskTrendAnalyzer(data_store=historical_store)

# Analyze trends over time
trends = analyzer.analyze_trends(
    time_range="24_months",
    metrics=["total_risks", "critical_risks", "avg_risk_score", 
             "remediation_rate", "risk_velocity"]
)

print("Risk Trend Analysis:")
for metric in trends.metrics:
    print(f"\n  {metric.name}:")
    print(f"    Current value: {metric.current_value}")
    print(f"    Previous period: {metric.previous_value}")
    print(f"    Change: {metric.change_percent:+.1f}%")
    print(f"    Trend: {metric.trend_direction}")
    print(f"    12-month forecast: {metric.forecast_value}")

# Benchmark against industry
benchmark = analyzer.benchmark(
    industry="technology",
    company_size="enterprise",
    metrics=["risk_density", "mttr", "risk_velocity"]
)

print("\nIndustry Benchmarking:")
for metric in benchmark.metrics:
    print(f"  {metric.name}:")
    print(f"    Our value: {metric.our_value}")
    print(f"    Industry median: {metric.industry_median}")
    print(f"    Industry 75th percentile: {metric.industry_p75}")
    print(f"    Percentile rank: {metric.percentile_rank:.0f}th")
```

## Database Schema for Risk Data

```sql
-- Risk register schema
CREATE TABLE risks (
    id SERIAL PRIMARY KEY,
    risk_number VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    subcategory VARCHAR(100),
    owner VARCHAR(100),
    business_unit VARCHAR(100),
    
    -- Inherent risk
    inherent_likelihood INTEGER CHECK (inherent_likelihood BETWEEN 1 AND 5),
    inherent_impact INTEGER CHECK (inherent_impact BETWEEN 1 AND 5),
    inherent_score INTEGER,
    inherent_rating VARCHAR(20),
    
    -- Residual risk
    residual_likelihood INTEGER CHECK (residual_likelihood BETWEEN 1 AND 5),
    residual_impact INTEGER CHECK (residual_impact BETWEEN 1 AND 5),
    residual_score INTEGER,
    residual_rating VARCHAR(20),
    
    -- Treatment
    treatment_strategy VARCHAR(50), -- accept, mitigate, transfer, avoid
    treatment_status VARCHAR(50),
    target_date DATE,
    
    -- FAIR analysis
    fair_ale DECIMAL(12, 2),
    fair_var_95 DECIMAL(12, 2),
    fair_ci_lower DECIMAL(12, 2),
    fair_ci_upper DECIMAL(12, 2),
    
    -- Metadata
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'open'
);

-- Risk treatment plans
CREATE TABLE risk_treatments (
    id SERIAL PRIMARY KEY,
    risk_id INTEGER REFERENCES risks(id),
    strategy VARCHAR(50) NOT NULL,
    description TEXT,
    controls JSONB,
    cost_estimate DECIMAL(12, 2),
    cost_actual DECIMAL(12, 2),
    implementation_timeline INTERVAL,
    owner VARCHAR(100),
    status VARCHAR(50) DEFAULT 'planned',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    evidence JSONB
);

-- Risk assessments (periodic)
CREATE TABLE risk_assessments (
    id SERIAL PRIMARY KEY,
    risk_id INTEGER REFERENCES risks(id),
    assessment_date DATE NOT NULL,
    assessor VARCHAR(100),
    methodology VARCHAR(50), -- fair, qualitative, hybrid
    likelihood INTEGER CHECK (likelihood BETWEEN 1 AND 5),
    impact INTEGER CHECK (impact BETWEEN 1 AND 5),
    score INTEGER,
    rating VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Business impact data
CREATE TABLE business_impacts (
    id SERIAL PRIMARY KEY,
    risk_id INTEGER REFERENCES risks(id),
    process_name VARCHAR(100),
    revenue_per_hour DECIMAL(12, 2),
    downtime_hours DECIMAL(8, 2),
    direct_loss DECIMAL(12, 2),
    indirect_loss DECIMAL(12, 2),
    regulatory_fine DECIMAL(12, 2),
    reputation_cost DECIMAL(12, 2),
    total_impact DECIMAL(12, 2),
    assessment_date DATE
);

-- Monte Carlo simulation results
CREATE TABLE mc_simulations (
    id SERIAL PRIMARY KEY,
    risk_id INTEGER REFERENCES risks(id),
    simulation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    iterations INTEGER,
    mean_loss DECIMAL(12, 2),
    std_dev DECIMAL(12, 2),
    percentile_50 DECIMAL(12, 2),
    percentile_75 DECIMAL(12, 2),
    percentile_90 DECIMAL(12, 2),
    percentile_95 DECIMAL(12, 2),
    percentile_99 DECIMAL(12, 2),
    var_95 DECIMAL(12, 2),
    tvar_95 DECIMAL(12, 2),
    parameters JSONB
);

-- Risk register snapshots
CREATE TABLE risk_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_date DATE NOT NULL,
    total_risks INTEGER,
    critical_count INTEGER,
    high_count INTEGER,
    medium_count INTEGER,
    low_count INTEGER,
    avg_risk_score DECIMAL(5, 2),
    total_exposure DECIMAL(15, 2),
    risk_velocity DECIMAL(8, 2),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_risks_status ON risks(status);
CREATE INDEX idx_risks_owner ON risks(owner);
CREATE INDEX idx_risks_category ON risks(category);
CREATE INDEX idx_risks_score ON risks(inherent_score);
CREATE INDEX idx_treatments_risk ON risk_treatments(risk_id);
CREATE INDEX idx_assessments_risk ON risk_assessments(risk_id);
CREATE INDEX idx_assessments_date ON risk_assessments(assessment_date);
CREATE INDEX idx_simulations_risk ON mc_simulations(risk_id);
CREATE INDEX idx_snapshots_date ON risk_snapshots(snapshot_date);
```

## Risk Dashboard Configuration

```json
{
  "dashboard": {
    "title": "Enterprise Risk Dashboard",
    "refresh_interval": "5m",
    "panels": [
      {
        "title": "Risk Portfolio Overview",
        "type": "stat_row",
        "metrics": [
          {"name": "Total Risks", "query": "count(risks{status='open'})"},
          {"name": "Critical Risks", "query": "count(risks{rating='critical'})"},
          {"name": "Average Score", "query": "avg(risks{status='open'}.score)"},
          {"name": "Total Exposure", "query": "sum(risks{status='open'}.fair_ale)"}
        ]
      },
      {
        "title": "Risk Heat Map",
        "type": "heatmap",
        "x_axis": "likelihood",
        "y_axis": "impact",
        "color_scale": ["green", "yellow", "orange", "red"],
        "data_source": "risks"
      },
      {
        "title": "Risk Trend",
        "type": "line_chart",
        "metrics": [
          {"name": "Critical", "query": "risk_snapshot{rating='critical'}"},
          {"name": "High", "query": "risk_snapshot{rating='high'}"},
          {"name": "Medium", "query": "risk_snapshot{rating='medium'}"}
        ],
        "time_range": "12_months"
      },
      {
        "title": "Remediation Progress",
        "type": "progress_bar",
        "segments": [
          {"label": "Completed", "query": "count(risks{status='resolved'})"},
          {"label": "In Progress", "query": "count(risks{status='in_progress'})"},
          {"label": "Not Started", "query": "count(risks{status='open'})"}
        ]
      },
      {
        "title": "Top Risks by ALE",
        "type": "table",
        "columns": ["Risk ID", "Title", "Rating", "ALE", "Owner", "Days Open"],
        "sort_by": "ALE",
        "sort_order": "desc",
        "limit": 10
      }
    ]
  }
}
```

## References

- FAIR — Factor Analysis of Information Risk (OpenFAIR)
- ISO 27005:2022 — Information Security Risk Management
- NIST SP 800-30 Rev 1 — Guide for Conducting Risk Assessments
- NIST Cybersecurity Framework 2.0 — Risk Assessment Function
- COSO ERM Framework — Enterprise Risk Management
- Monte Carlo Methods in Financial Engineering — Paul Glasserman
- The FAIR Model — RiskLens / FAIR Institute
- ISO 31000:2018 — Risk Management Guidelines

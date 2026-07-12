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

## References

- FAIR — Factor Analysis of Information Risk (OpenFAIR)
- ISO 27005:2022 — Information Security Risk Management
- NIST SP 800-30 Rev 1 — Guide for Conducting Risk Assessments
- NIST Cybersecurity Framework 2.0 — Risk Assessment Function
- COSO ERM Framework — Enterprise Risk Management
- Monte Carlo Methods in Financial Engineering — Paul Glasserman
- The FAIR Model — RiskLens / FAIR Institute
- ISO 31000:2018 — Risk Management Guidelines

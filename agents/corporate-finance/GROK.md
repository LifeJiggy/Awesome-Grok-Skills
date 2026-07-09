---
name: Corporate Finance Agent
version: 2.0.0
description: >
  Financial modeling, valuation, budgeting, forecasting, M&A analysis,
  capital structure optimization, cost reduction, and risk management
  for enterprise financial operations.
author: Awesome Grok Skills
tags:
  - corporate-finance
  - financial-modeling
  - budgeting
  - forecasting
  - valuation
  - capital-structure
  - cost-optimization
  - risk-management
  - monte-carlo
  - scenario-analysis
category: finance
personality:
  - analytical
  - precise
  - strategic
  - risk-aware
  - data-driven
use_cases:
  - Departmental budget creation and tracking
  - Revenue and expense forecasting
  - Financial statement analysis
  - Cost optimization and reduction
  - Capital allocation and ROI analysis
  - Scenario and sensitivity analysis
  - Monte Carlo simulation
  - Executive financial reporting
  - Variance analysis
  - Working capital management
---

# Corporate Finance Agent

## Agent Identity

You are the **Corporate Finance Agent**, an expert in financial planning, analysis, and management. You combine quantitative rigor with strategic insight to drive better financial decisions. You understand that every number tells a story and that good financial management is the backbone of business success.

**Core Mission:** Transform financial data into actionable insights that optimize performance, reduce costs, and maximize shareholder value.

**Operating Mode:** Always present findings with context. Numbers without interpretation are noise; recommendations without data are guesses. Provide both, always.

## Core Principles

1. **Accuracy First** — Financial data must be precise and verifiable. Double-check calculations, validate inputs, and flag anomalies.

2. **Data-Driven Decisions** — Every recommendation must be supported by numbers. Intuition has its place, but data drives the final call.

3. **Risk Awareness** — Consider downside scenarios alongside base cases. Optimism without risk analysis is recklessness.

4. **Transparency** — All assumptions and methodologies must be documented. Stakeholders should be able to trace any figure back to its source.

5. **Actionable Insights** — Analysis without action is academic. Always recommend concrete next steps with timelines.

6. **Conservative Estimates** — When uncertain, err on the side of caution. Over-delivering beats missing targets.

7. **Materiality Focus** — Focus on what matters most. Small variances don't warrant investigation; material ones do.

## Capabilities

### Budget Management

```python
agent = CorporateFinanceAgent()

# Create budget
budget = agent.create_budget(
    department="engineering",
    year=2024,
    amount=1_200_000.0,
    category="operating",
    owner="CTO",
)

# Update spend
status = agent._budget_manager.update_budget_spend(
    budget.budget_id,
    spent=750_000,
    committed=150_000,
)

# Analyze budgets
analysis = agent._budget_manager.analyze_budgets("engineering")
print(f"Total budget: ${analysis['total_amount']:,.2f}")
print(f"Percent spent: {analysis['percent_spent']}%")
print(f"Variance: ${analysis['variance']:,.2f}")
```

### Forecasting

```python
historical = {
    "Jan": 850_000, "Feb": 920_000, "Mar": 980_000,
    "Apr": 1_050_000, "May": 1_100_000, "Jun": 1_150_000,
}

# Forecast with exponential smoothing
forecast = agent.forecast(historical, periods=3, method="exponential_smoothing")
print(f"Forecast: {forecast.values}")
print(f"Confidence intervals: {forecast.confidence_intervals}")
print(f"Accuracy (MAPE): {forecast.accuracy}%")

# Scenario analysis
scenarios = agent.run_scenario_analysis(list(historical.values()), periods=3)
print(f"Bullish: {scenarios['scenarios']['bullish']}")
print(f"Bearish: {scenarios['scenarios']['bearish']}")
```

### Financial Analysis

```python
statements = {
    "revenue": 5_000_000,
    "gross_profit": 3_000_000,
    "ebitda": 1_500_000,
    "net_income": 800_000,
    "total_assets": 10_000_000,
    "total_equity": 6_000_000,
    "total_liabilities": 4_000_000,
    "current_assets": 3_000_000,
    "current_liabilities": 2_000_000,
}

analysis = agent.analyze_financials(statements)
print(f"Health score: {analysis['health_score']}")
print(f"Gross Margin: {analysis['ratios']['gross_margin']:.1%}")
print(f"ROE: {analysis['ratios']['roe']:.1%}")
print(f"Current Ratio: {analysis['ratios']['current_ratio']:.2f}")
for rec in analysis["recommendations"]:
    print(f"  - {rec}")
```

### Cost Optimization

```python
optimization = agent.optimize_costs(
    area="cloud_hosting",
    current_spend=250_000.0,
)

print(f"Current spend: ${optimization.current_spend:,.2f}")
print(f"Optimized spend: ${optimization.optimized_spend:,.2f}")
print(f"Savings: ${optimization.savings:,.2f} ({optimization.savings_percentage}%)")
print(f"Timeline: {optimization.timeline}")
print(f"Risk: {optimization.risk}")
```

### Capital Allocation

```python
allocation = agent.allocate_capital(
    department="R&D",
    total_budget=500_000.0,
    initiatives=["AI Platform", "Data Pipeline", "Security Hardening"],
)

print(f"Expected ROI: {allocation.expected_roi:.0%}")
print(f"Allocations: {allocation.allocations}")

# Reallocate
result = agent.reallocate_capital(allocation.allocation_id, "Marketing", 100_000)
print(f"Reallocation: {result['status']}")
```

## Method Signatures

### CorporateFinanceAgent

```python
def create_budget(
    self,
    department: str,
    year: int,
    amount: float,
    category: str = "operating",
    period: str = "annual",
    owner: str = "",
) -> Budget:
    """Create a departmental budget.

    Args:
        department: Department name (e.g., "engineering", "marketing").
        year: Fiscal year.
        amount: Budget amount in USD.
        category: Budget category (operating, capital, R&D, marketing).
        period: Budget period (annual, quarterly, monthly).
        owner: Budget owner name or title.

    Returns:
        Budget object with budget_id, status, and created_at.
    """

def forecast(
    self,
    historical: Dict[str, float],
    periods: int = 4,
    method: Optional[str] = None,
) -> ForecastResult:
    """Forecast future values using historical data.

    Args:
        historical: Dict of period labels to values (e.g., {"Jan": 1000}).
        periods: Number of periods to forecast.
        method: Forecasting method (linear_regression, moving_average,
                exponential_smoothing, monte_carlo). Auto-selected if None.

    Returns:
        ForecastResult with values, confidence_intervals, accuracy, method.
    """

def analyze_financials(
    self,
    statements: Dict,
) -> Dict[str, Any]:
    """Analyze financial statements and return ratios and recommendations.

    Args:
        statements: Dict with keys: revenue, gross_profit, ebitda, net_income,
                   total_assets, total_equity, total_liabilities,
                   current_assets, current_liabilities.

    Returns:
        Dict with ratios, health_score, and recommendations.
    """

def optimize_costs(
    self,
    area: str,
    current_spend: float,
    approach: str = "standard",
) -> CostOptimization:
    """Identify cost reduction opportunities.

    Args:
        area: Cost area to optimize (e.g., "cloud_hosting", "office_space").
        current_spend: Current annual spend in USD.
        approach: Optimization approach (standard, aggressive, conservative).

    Returns:
        CostOptimization with savings, timeline, risk, and opportunities.
    """

def run_scenario_analysis(
    self,
    base_values: List[float],
    periods: int = 4,
) -> Dict[str, Any]:
    """Run scenario analysis with bullish, base, and bearish projections.

    Args:
        base_values: Historical values to project from.
        periods: Number of periods to project.

    Returns:
        Dict with scenarios (bullish, base, bearish) and multipliers.
    """

def allocate_capital(
    self,
    department: str,
    total_budget: float,
    initiatives: List[str],
) -> CapitalAllocation:
    """Allocate capital across initiatives with ROI tracking.

    Args:
        department: Target department.
        total_budget: Total capital to allocate.
        initiatives: List of initiative names.

    Returns:
        CapitalAllocation with allocations dict and expected_roi.
    """

def reallocate_capital(
    self,
    allocation_id: str,
    new_department: str,
    amount: float,
) -> Dict[str, Any]:
    """Reallocate capital between departments.

    Args:
        allocation_id: ID of the source allocation.
        new_department: Department to receive funds.
        amount: Amount to reallocate.

    Returns:
        Dict with status, source_remaining, and destination_added.
    """

def get_status(self) -> Dict[str, Any]:
    """Get agent status and health information.

    Returns:
        Dict with version, component status, and data counts.
    """

def export_report(self, format: str = "json") -> Dict[str, Any]:
    """Export comprehensive financial report.

    Args:
        format: Export format (json, csv, dict).

    Returns:
        Dict with budget summary, forecasts, analysis, and recommendations.
    """
```

## Financial Ratios

| Ratio | Formula | Target | Warning |
|-------|---------|--------|---------|
| Gross Margin | Gross Profit / Revenue | > 40% | < 30% |
| Operating Margin | EBITDA / Revenue | > 20% | < 10% |
| Net Margin | Net Income / Revenue | > 10% | < 5% |
| ROE | Net Income / Equity | > 15% | < 8% |
| ROA | Net Income / Assets | > 8% | < 4% |
| Current Ratio | Current Assets / Current Liabilities | > 1.5 | < 1.0 |
| Debt-to-Equity | Liabilities / Equity | < 0.5 | > 1.0 |
| Asset Turnover | Revenue / Assets | > 0.5 | < 0.3 |

## Forecasting Methods

| Method | Best For | Pros | Cons |
|--------|----------|------|------|
| Linear Regression | Steady trends | Simple, interpretable | Assumes linearity |
| Moving Average | Stable data | Smooths noise | Lags trends |
| Exponential Smoothing | Recent trends | Responsive | Requires alpha tuning |
| Monte Carlo | Uncertainty | Quantifies risk | Computationally expensive |
| Scenario Analysis | Planning | Conservative + optimistic | Subjective assumptions |

## Checklists

### Budget Planning Checklist

- [ ] Department budgets aligned with strategic goals
- [ ] Historical spend data reviewed (12+ months)
- [ ] Variances from prior year explained
- [ ] Contingency reserves allocated (5-10%)
- [ ] Approval workflow defined
- [ ] Monitoring cadence established (monthly)
- [ ] KPIs and thresholds documented
- [ ] Cross-department dependencies mapped

### Financial Analysis Checklist

- [ ] Income statement reviewed
- [ ] Balance sheet analyzed
- [ ] Cash flow statement examined
- [ ] Key ratios calculated and benchmarked
- [ ] Trends identified (3+ periods)
- [ ] Recommendations documented with priority
- [ ] Risk factors assessed
- [ ] Action items assigned with owners

### Cost Optimization Checklist

- [ ] Cost categories defined (fixed vs variable)
- [ ] Current benchmarks established
- [ ] Quick wins identified (low effort, high impact)
- [ ] Savings estimates validated
- [ ] Implementation timeline defined
- [ ] Risk assessment completed
- [ ] Stakeholder buy-in obtained
- [ ] Tracking mechanism in place

## Troubleshooting

| Problem | Diagnosis | Solution |
|---------|-----------|----------|
| Forecast inaccurate | Method mismatch with data pattern | Try different forecasting method, check data quality |
| Budget variance high | Unexpected spend or revenue change | Investigate root cause, adjust budget if justified |
| Health score low | Poor ratios across multiple dimensions | Address weakest ratio first, prioritize by impact |
| Cost savings unrealistic | Over-optimistic assumptions | Validate with department owners, use conservative estimates |
| Capital ROI uncertain | Insufficient historical data | Gather more historical ROI data, use peer benchmarks |
| Monte Carlo results unstable | Too few simulations | Increase simulation count to 5000+ |
| Ratios show NaN | Division by zero in input data | Validate financial data for completeness and positivity |
| Forecast lags actuals | Moving average window too large | Reduce window size or switch to exponential smoothing |

## Configuration

```python
from agents.corporate_finance.agent import CorporateFinanceAgent, Config

config = Config(
    currency="USD",
    forecast_method="exponential_smoothing",
    budget_cycle="annual",
    scenario_bull_multiplier=1.2,
    scenario_bear_multiplier=0.8,
    monte_carlo_simulations=1000,
    confidence_level=0.95,
    default_tax_rate=0.21,
)
agent = CorporateFinanceAgent(config)
```

### Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `currency` | `"USD"` | Currency for all calculations |
| `forecast_method` | `"exponential_smoothing"` | Default forecasting method |
| `budget_cycle` | `"annual"` | Default budget period |
| `scenario_bull_multiplier` | `1.2` | Bullish scenario growth factor |
| `scenario_bear_multiplier` | `0.8` | Bearish scenario decline factor |
| `monte_carlo_simulations` | `1000` | Number of Monte Carlo simulations |
| `confidence_level` | `0.95` | Confidence interval level (95%) |
| `default_tax_rate` | `0.21` | Default corporate tax rate |

## Examples

### Full Financial Planning Workflow

```python
from agents.corporate_finance.agent import CorporateFinanceAgent

agent = CorporateFinanceAgent()

# 1. Create departmental budgets
eng_budget = agent.create_budget("engineering", 2024, 1_200_000, "operating", owner="CTO")
mkt_budget = agent.create_budget("marketing", 2024, 800_000, "operating", owner="CMO")

# 2. Track spending
agent._budget_manager.update_budget_spend(eng_budget.budget_id, spent=300_000, committed=50_000)
agent._budget_manager.update_budget_spend(mkt_budget.budget_id, spent=200_000, committed=30_000)

# 3. Forecast revenue
historical = {"Q1": 1_200_000, "Q2": 1_350_000, "Q3": 1_500_000}
forecast = agent.forecast(historical, periods=4, method="exponential_smoothing")

# 4. Analyze financials
analysis = agent.analyze_financials({
    "revenue": 5_000_000, "gross_profit": 3_000_000,
    "net_income": 800_000, "total_assets": 10_000_000,
    "total_equity": 6_000_000, "total_liabilities": 4_000_000,
    "current_assets": 3_000_000, "current_liabilities": 2_000_000,
})

# 5. Optimize costs
cost_opt = agent.optimize_costs("cloud_hosting", 250_000)

# 6. Allocate capital
allocation = agent.allocate_capital("R&D", 500_000, ["AI Platform", "Data Pipeline"])

# 7. Generate report
report = agent.export_report("json")
```

## Best Practices

1. **Review Budgets Monthly** — Track spend vs. forecast regularly to catch variances early
2. **Multiple Forecast Methods** — Compare methods for best accuracy; use ensemble approaches
3. **Stress Test Assumptions** — Use scenario analysis for risk management and planning
4. **Document Assumptions** — Record all forecasting assumptions for audit trail
5. **Act on Variances** — Investigate and address budget variances promptly; don't let them compound
6. **Optimize Continuously** — Regular cost optimization reviews; target 5-15% annual savings
7. **Align Capital to Strategy** — Ensure allocations support strategic goals, not just departmental requests
8. **Monitor Key Ratios** — Track financial ratios quarterly; address trends before they become problems
9. **Use Conservative Estimates** — When uncertain, err on the side of caution in forecasts
10. **Maintain Audit Trail** — Log all financial decisions with rationale and timestamps

## Security Considerations

- Financial data is sensitive; implement access controls
- All calculations logged for audit trail
- Budget approvals require proper authorization
- Financial reports restricted to authorized personnel
- Data encryption at rest for financial records
- Regular backup of financial data
- Compliance with financial regulations (SOX, GAAP, IFRS)
- Segregation of duties for financial operations

---

*Corporate Finance Agent v2.0 — Part of the Awesome Grok Skills collection.*
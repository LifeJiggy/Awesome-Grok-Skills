# Corporate Finance Agent

Financial modeling, valuation, budgeting, forecasting, M&A analysis, capital structure optimization, cost reduction, and risk management for enterprise financial operations.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Budget Management](#budget-management)
  - [Forecasting](#forecasting)
  - [Financial Analysis](#financial-analysis)
  - [Cost Optimization](#cost-optimization)
  - [Capital Allocation](#capital-allocation)
  - [Scenario Analysis](#scenario-analysis)
- [API Reference](#api-reference)
- [Financial Ratios](#financial-ratios)
- [Forecasting Methods](#forecasting-methods)
- [Data Models](#data-models)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Corporate Finance Agent is a Python-based system for managing corporate finance functions including budgeting, forecasting, financial analysis, cost optimization, and capital allocation. It provides audit-ready reporting, scenario analysis, Monte Carlo simulation, and executive-level dashboards.

**Key Capabilities:**
- Departmental budget creation and tracking with variance analysis
- Multiple forecasting methods (linear, moving average, exponential smoothing, Monte Carlo)
- Financial ratio analysis and health scoring with industry benchmarks
- Cost optimization with savings estimation and risk assessment
- Capital allocation with ROI tracking and reallocation support
- Scenario analysis (bullish, base, bearish) for strategic planning
- Comprehensive reporting for executive decision-making

**Ideal For:**
- CFOs and finance teams managing departmental budgets
- Financial analysts building forecasts and models
- Operations managers identifying cost reduction opportunities
- Strategic planners evaluating capital allocation options

## Features

| Feature | Description |
|---------|-------------|
| Budget Management | Create, track, and analyze departmental budgets with variance analysis |
| Forecasting | Multiple methods with confidence intervals and accuracy metrics |
| Financial Analysis | Ratio calculation, trend analysis, health scoring, benchmarks |
| Cost Optimization | Identify savings, analyze fixed/variable mix, risk assessment |
| Capital Allocation | Distribute capital, track ROI, reallocate between departments |
| Scenario Analysis | Bullish, base, bearish projections with multipliers |
| Monte Carlo | Simulation-based uncertainty quantification with configurable iterations |
| Reporting | Executive-level reports with recommendations and action items |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Corporate Finance Agent                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Budget   │  │Forecasting│  │Financial │  │  Cost    │   │
│  │ Manager  │  │  Engine   │  │ Analyzer │  │Optimizer │   │
│  │          │  │           │  │          │  │          │   │
│  │• Create  │  │• Linear   │  │• Ratios  │  │• Identify│   │
│  │• Track   │  │• Moving   │  │• Trends  │  │• Estimate│   │
│  │• Variance│  │• Exp.     │  │• Health  │  │• Risk    │   │
│  │          │  │• Monte    │  │• Recs    │  │          │   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │             │             │             │           │
│  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐  ┌────┴─────┐   │
│  │ Capital  │  │Financial │  │ Report   │  │ Scenario │   │
│  │Allocator │  │ Storage  │  │Generator │  │ Analyzer │   │
│  │          │  │          │  │          │  │          │   │
│  │• ROI     │  │• JSON    │  │• Exec    │  │• Bull    │   │
│  │• Realloc │  │• Audit   │  │• Summary │  │• Base    │   │
│  │• Portfolio│ │• Export  │  │• Detail  │  │• Bear    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                   Data Layer                         │   │
│  │  Budgets │ Forecasts │ Statements │ Allocations      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Basic Usage

```python
from agents.corporate_finance.agent import CorporateFinanceAgent

agent = CorporateFinanceAgent()

# Create budget
budget = agent.create_budget(
    department="engineering",
    year=2024,
    amount=1_200_000.0,
    category="operating",
    owner="CTO",
)

# Forecast
historical = {"Jan": 850_000, "Feb": 920_000, "Mar": 980_000}
forecast = agent.forecast(historical, periods=3)
print(f"Forecast: {forecast.values}")
print(f"Accuracy: {forecast.accuracy}%")

# Analyze financials
analysis = agent.analyze_financials({
    "revenue": 5_000_000,
    "gross_profit": 3_000_000,
    "net_income": 800_000,
    "total_assets": 10_000_000,
    "total_equity": 6_000_000,
    "total_liabilities": 4_000_000,
    "current_assets": 3_000_000,
    "current_liabilities": 2_000_000,
})
print(f"Health Score: {analysis['health_score']}")
```

### Command Line

```bash
python agents/corporate-finance/agent.py
```

## Usage

### Budget Management

```python
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

# Get budget status
status = agent._budget_manager.get_budget_status(budget.budget_id)
print(f"Percent spent: {status['percent_spent']}%")
print(f"Variance: ${status['variance']:,.2f}")
print(f"Status: {status['status']}")

# Analyze all budgets
analysis = agent._budget_manager.analyze_budgets()
print(f"Total budget: ${analysis['total_amount']:,.2f}")
print(f"Total spent: ${analysis['total_spent']:,.2f}")
```

### Forecasting

```python
historical = {
    "Jan": 850_000, "Feb": 920_000, "Mar": 980_000,
    "Apr": 1_050_000, "May": 1_100_000, "Jun": 1_150_000,
}

# Exponential smoothing (recommended for recent trends)
forecast = agent.forecast(historical, periods=3, method="exponential_smoothing")
print(f"Values: {forecast.values}")
print(f"Confidence: {forecast.confidence_intervals}")
print(f"Accuracy (MAPE): {forecast.accuracy}%")

# Linear regression (best for steady trends)
forecast_lr = agent.forecast(historical, periods=3, method="linear_regression")

# Monte Carlo (best for uncertainty)
forecast_mc = agent.forecast(historical, periods=3, method="monte_carlo")
print(f"Mean: {forecast_mc.mean}")
print(f"Std Dev: {forecast_mc.std_dev}")
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
print(f"Health Score: {analysis['health_score']}")
print(f"Gross Margin: {analysis['ratios']['gross_margin']:.1%}")
print(f"ROE: {analysis['ratios']['roe']:.1%}")
print(f"Current Ratio: {analysis['ratios']['current_ratio']:.2f}")
print(f"D/E Ratio: {analysis['ratios']['debt_to_equity']:.2f}")

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
print(f"Savings: ${optimization.savings:,.2f}")
print(f"Savings %: {optimization.savings_percentage}%")
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
for name, amount in allocation.allocations.items():
    print(f"  {name}: ${amount:,.2f}")

# Reallocate
result = agent.reallocate_capital(allocation.allocation_id, "Marketing", 100_000)
print(f"Status: {result['status']}")
print(f"R&D remaining: ${result['source_remaining']:,.2f}")
```

### Scenario Analysis

```python
base_values = [850_000, 920_000, 980_000, 1_050_000]
scenarios = agent.run_scenario_analysis(base_values, periods=3)

print(f"Bullish (+20%): {scenarios['scenarios']['bullish']}")
print(f"Base (flat):    {scenarios['scenarios']['base']}")
print(f"Bearish (-20%): {scenarios['scenarios']['bearish']}")
```

## API Reference

### CorporateFinanceAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `create_budget()` | department, year, amount, category, period, owner | Budget object |
| `forecast()` | historical, periods, method | ForecastResult object |
| `analyze_financials()` | statements | Analysis dict with ratios and recommendations |
| `optimize_costs()` | area, current_spend, approach | CostOptimization object |
| `run_scenario_analysis()` | base_values, periods | Scenario dict |
| `allocate_capital()` | department, total_budget, initiatives | CapitalAllocation object |
| `reallocate_capital()` | allocation_id, new_department, amount | Reallocation dict |
| `get_status()` | — | Agent status dict |
| `export_report()` | format | Financial report dict |

## Financial Ratios

| Ratio | Formula | Healthy Range | Warning |
|-------|---------|---------------|---------|
| Gross Margin | Gross Profit / Revenue | > 40% | < 30% |
| Operating Margin | EBITDA / Revenue | > 20% | < 10% |
| Net Margin | Net Income / Revenue | > 10% | < 5% |
| ROE | Net Income / Equity | > 15% | < 8% |
| ROA | Net Income / Assets | > 8% | < 4% |
| Current Ratio | Current Assets / Current Liabilities | > 1.5 | < 1.0 |
| Debt-to-Equity | Liabilities / Equity | < 0.5 | > 1.0 |
| Asset Turnover | Revenue / Assets | > 0.5 | < 0.3 |

## Forecasting Methods

| Method | Best For | Alpha/Window | Key Metric |
|--------|----------|--------------|------------|
| Linear Regression | Steady growth trends | N/A | R-squared |
| Moving Average | Stable data, noise reduction | window=3 | MAPE |
| Exponential Smoothing | Recent trend emphasis | alpha=0.3 | MAPE |
| Monte Carlo | Uncertainty quantification | simulations=1000 | Confidence interval |

## Data Models

### Budget
Departmental budget with spent, committed, forecast, variance tracking, and status management.

### ForecastResult
Forecast values with confidence intervals, accuracy (MAPE), method metadata, and trend data.

### CostOptimization
Cost reduction analysis with savings estimates, timeline, risk level, and implementation opportunities.

### CapitalAllocation
Capital distribution across departments and initiatives with ROI tracking and reallocation support.

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

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Forecast inaccurate | Try different method, verify data quality, check for outliers |
| Budget variance high | Investigate root cause, adjust if justified, document rationale |
| Health score low | Address weakest financial ratio first, prioritize by impact |
| Cost savings unrealistic | Validate with department owners, use conservative estimates |
| Capital ROI uncertain | Gather more historical ROI data, use industry benchmarks |
| Monte Carlo unstable | Increase simulation count to 5000+, verify input distributions |
| Ratios show NaN | Check for zero/negative values in financial data |
| Report incomplete | Verify all required financial fields are populated |

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams and component details
- `GROK.md` — Agent instructions, identity, and API reference
- `README.md` — This file

## Contributing

1. Add new forecasting methods (ARIMA, Prophet, neural networks)
2. Enhance financial ratio calculations (DuPont analysis, Altman Z-score)
3. Add new cost optimization strategies with industry benchmarks
4. Improve scenario analysis models with sensitivity tables
5. Add multi-entity consolidation support
6. Update documentation for API changes

## License

Part of the Awesome Grok Skills collection. See project root for license details.

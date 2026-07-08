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
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Corporate Finance Agent is a Python-based system for managing corporate finance functions including budgeting, forecasting, financial analysis, cost optimization, and capital allocation. It provides audit-ready reporting and scenario analysis.

**Key Capabilities:**
- Departmental budget creation and tracking
- Multiple forecasting methods (linear, moving average, exponential smoothing, Monte Carlo)
- Financial ratio analysis and health scoring
- Cost optimization with savings estimation
- Capital allocation with ROI tracking
- Scenario analysis (bullish, base, bearish)

## Features

| Feature | Description |
|---------|-------------|
| Budget Management | Create, track, and analyze departmental budgets |
| Forecasting | Multiple methods with confidence intervals |
| Financial Analysis | Ratio calculation, trend analysis, health scoring |
| Cost Optimization | Identify savings, analyze fixed/variable mix |
| Capital Allocation | Distribute capital, track ROI, reallocate |
| Scenario Analysis | Bullish, base, bearish projections |
| Monte Carlo | Simulation-based uncertainty quantification |

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Corporate Finance Agent                      │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │ Budget   │ │Forecasting│ │Financial │ │  Cost    │     │
│  │ Manager  │ │  Engine   │ │ Analyzer │ │Optimizer │     │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
│       │            │            │            │             │
│  ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐ ┌────┴─────┐     │
│  │ Capital  │ │Financial │ │ Report   │ │ Scenario │     │
│  │Allocator │ │ Storage  │ │Generator │ │ Analyzer │     │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘     │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

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
```

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

# Analyze all budgets
analysis = agent._budget_manager.analyze_budgets()
print(f"Total budget: ${analysis['total_amount']:,.2f}")
```

### Forecasting

```python
historical = {
    "Jan": 850_000, "Feb": 920_000, "Mar": 980_000,
    "Apr": 1_050_000, "May": 1_100_000, "Jun": 1_150_000,
}

# Exponential smoothing
forecast = agent.forecast(historical, periods=3, method="exponential_smoothing")
print(f"Values: {forecast.values}")
print(f"Confidence: {forecast.confidence_intervals}")
print(f"Accuracy: {forecast.accuracy}%")

# Linear regression
forecast_lr = agent.forecast(historical, periods=3, method="linear_regression")
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
print(f"Ratios: {analysis['ratios']}")
for rec in analysis["recommendations"]:
    print(f"  - {rec}")
```

### Cost Optimization

```python
optimization = agent.optimize_costs(
    area="cloud_hosting",
    current_spend=250_000.0,
)

print(f"Savings: ${optimization.savings:,.2f}")
print(f"Percentage: {optimization.savings_percentage}%")
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

# Reallocate
result = agent.reallocate_capital(allocation.allocation_id, "Marketing", 100_000)
```

### Scenario Analysis

```python
base_values = [850_000, 920_000, 980_000, 1_050_000]
scenarios = agent.run_scenario_analysis(base_values, periods=3)

print(f"Bullish: {scenarios['scenarios']['bullish']}")
print(f"Base: {scenarios['scenarios']['base']}")
print(f"Bearish: {scenarios['scenarios']['bearish']}")
```

## API Reference

### CorporateFinanceAgent

| Method | Parameters | Returns |
|--------|-----------|---------|
| `create_budget()` | department, year, amount, category, period, owner | Budget object |
| `forecast()` | historical, periods, method | ForecastResult object |
| `analyze_financials()` | statements | Analysis dict |
| `optimize_costs()` | area, current_spend, approach | CostOptimization object |
| `run_scenario_analysis()` | base_values, periods | Scenario dict |
| `allocate_capital()` | department, total_budget, initiatives | CapitalAllocation object |
| `reallocate_capital()` | allocation_id, new_department, amount | Reallocation dict |
| `get_status()` | — | Agent status dict |
| `export_report()` | format | Financial report dict |

## Financial Ratios

| Ratio | Formula | Healthy Range |
|-------|---------|---------------|
| Gross Margin | Gross Profit / Revenue | > 40% |
| Operating Margin | EBITDA / Revenue | > 20% |
| Net Margin | Net Income / Revenue | > 10% |
| ROE | Net Income / Equity | > 15% |
| ROA | Net Income / Assets | > 8% |
| Current Ratio | Current Assets / Current Liabilities | > 1.5 |
| Debt-to-Equity | Liabilities / Equity | < 0.5 |
| Asset Turnover | Revenue / Assets | > 0.5 |

## Forecasting Methods

| Method | Best For | Alpha/Window |
|--------|----------|--------------|
| Linear Regression | Steady growth trends | N/A |
| Moving Average | Stable data, noise reduction | window=3 |
| Exponential Smoothing | Recent trend emphasis | alpha=0.3 |
| Monte Carlo | Uncertainty quantification | simulations=1000 |

## Data Models

### Budget
Departmental budget with spent, committed, forecast, and variance tracking.

### ForecastResult
Forecast values with confidence intervals, accuracy, and method metadata.

### CostOptimization
Cost reduction analysis with savings, timeline, and risk assessment.

### CapitalAllocation
Capital distribution across departments and initiatives with ROI tracking.

## Configuration

```python
from agents.corporate_finance.agent import Config

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

## Best Practices

1. **Review Budgets Monthly** — Track spend vs. forecast regularly
2. **Multiple Forecast Methods** — Compare methods for best accuracy
3. **Stress Test Assumptions** — Use scenario analysis for risk management
4. **Document Assumptions** — Record all forecasting assumptions
5. **Act on Variances** — Investigate and address budget variances promptly
6. **Optimize Continuously** — Regular cost optimization reviews
7. **Align Capital to Strategy** — Ensure allocations support strategic goals

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Forecast inaccurate | Try different method, verify data quality |
| Budget variance high | Investigate root cause, adjust if justified |
| Health score low | Address weakest financial ratio first |
| Cost savings unrealistic | Validate with department owners |
| Capital ROI uncertain | Gather more historical ROI data |

## Files

- `agent.py` — Main implementation (~900 lines)
- `ARCHITECTURE.md` — System architecture with diagrams
- `GROK.md` — Agent instructions and identity
- `README.md` — This file

## Contributing

1. Add new forecasting methods
2. Enhance financial ratio calculations
3. Add new cost optimization strategies
4. Improve scenario analysis models
5. Update documentation for API changes

## License

Part of the Awesome Grok Skills collection. See project root for license details.

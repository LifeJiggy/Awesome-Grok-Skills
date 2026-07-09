# Real Estate Agent

> Property analysis, valuation, investment modeling, and portfolio management platform.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The Real Estate Agent is a comprehensive real estate analysis platform that provides property valuation using multiple methods (comparable sales, income approach, cost approach), market analysis and trend forecasting, investment ROI and cash flow analysis, mortgage calculation with amortization schedules, rental income optimization, portfolio management and rebalancing, due diligence checklist automation, tax impact analysis, property risk assessment, and multi-property comparison.

### Design Principles

- **Multi-Method Valuation**: Cross-validate property values using multiple approaches
- **Data-Driven Decisions**: Every recommendation backed by quantitative analysis
- **Risk-Aware**: Every investment includes risk assessment
- **Full Lifecycle**: From market research through due diligence to portfolio management

---

## Features

| Feature | Description |
|---------|-------------|
| **Property Valuation** | Comparable sales, income approach, cost approach, auto-valuation |
| **Market Analysis** | Health scoring, trend analysis, market comparison, hotspot detection |
| **Investment Analysis** | Buy-and-hold, flip, rental, BRRRR strategy modeling |
| **Mortgage Calculator** | Payment calculation, amortization, rate comparison |
| **Rental Analysis** | Rental yield, rent optimization, expense breakdown |
| **Portfolio Management** | Property tracking, allocation analysis, rebalancing |
| **Due Diligence** | Phase-based checklists with progress tracking |
| **Tax Analysis** | Property tax, depreciation, tax strategies |
| **Risk Assessment** | Multi-category risk scoring and mitigation |
| **Property Comparison** | Side-by-side comparison with weighted scoring |

---

## Quick Start

### Installation

```bash
# No external dependencies required
python agents/real-estate/agent.py
```

### Basic Usage

```python
from agents.real_estate.agent import RealEstateAgent

# Initialize the agent
agent = RealEstateAgent()

# Run the agent
result = agent.run()
print(result)
```

### First Property Valuation

```python
from agents.real_estate.agent import PropertyValuationEngine, Property, PropertyType, ListingStatus, PropertyCondition

engine = PropertyValuationEngine()

prop = Property(
    property_id="P001",
    address="123 Main St",
    city="Austin",
    state="TX",
    zip_code="78701",
    property_type=PropertyType.SINGLE_FAMILY,
    listing_status=ListingStatus.ACTIVE,
    condition=PropertyCondition.GOOD,
    price=450000,
    bedrooms=3,
    bathrooms=2.0,
    sqft=2000,
    lot_size_sqft=8000,
    year_built=2005,
    garage_spaces=2,
    stories=2,
    hoa_monthly=0,
    features=[],
    photos=[],
    mls_number="MLS123"
)
engine.register_property(prop)
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Real Estate Agent (Orchestrator)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │ PropertyValuation │  │  MarketAnalyzer   │  │Investment     │  │
│  │    Engine         │  │                   │  │Analyzer       │  │
│  └──────────────────┘  └──────────────────┘  └───────────────┘  │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │MortgageCalculator │  │  RentalAnalyzer   │  │Portfolio      │  │
│  │                   │  │                   │  │Manager        │  │
│  └──────────────────┘  └──────────────────┘  └───────────────┘  │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐  │
│  │DueDiligence       │  │   TaxAnalyzer     │  │RiskAssessor   │  │
│  │    Manager        │  │                   │  │               │  │
│  └──────────────────┘  └──────────────────┘  └───────────────┘  │
│                                                                   │
│  ┌───────────────────────────────────────────────────────────┐   │
│  │            PropertyComparisonEngine                        │   │
│  └───────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system architecture.

---

## Usage

### Property Valuation

```python
from agents.real_estate.agent import PropertyValuationEngine

engine = PropertyValuationEngine()
engine.register_property(prop)
engine.add_comparable("P001", comp)

# Comparable sales valuation
val = engine.comparable_sales_valuation("P001")

# Income approach
val = engine.income_approach_valuation("P001", annual_rental_income=33600, cap_rate=0.055)

# Cost approach
val = engine.cost_approach_valuation("P001", land_value=150000, replacement_cost_per_sqft=200, depreciation_pct=0.15)

# Auto valuation
val = engine.auto_valuation("P001")
```

### Market Analysis

```python
from agents.real_estate.agent import MarketAnalyzer, MarketData, MarketCycle

analyzer = MarketAnalyzer()
analyzer.register_market(market_data)

health = analyzer.market_health("M001")
comparison = analyzer.compare_markets(["M001", "M002"])
hotspots = analyzer.investment_hotspots()
trends = analyzer.trend_analysis("M001", months=12)
```

### Investment Analysis

```python
from agents.real_estate.agent import InvestmentAnalyzer, InvestmentStrategy

analyzer = InvestmentAnalyzer()

# Buy and hold
analysis = analyzer.analyze_property(
    property_id="P001",
    purchase_price=450000,
    down_payment_pct=20,
    interest_rate=6.5,
    loan_term_years=30,
    monthly_rental_income=2800,
    monthly_expenses=600,
    strategy=InvestmentStrategy.BUY_AND_HOLD
)

# Flip analysis
flip = analyzer.flip_analysis(
    purchase_price=350000,
    renovation_cost=50000,
    holding_months=6,
    after_repair_value=480000
)

# Cash flow projection
projections = analyzer.cash_flow_projection(
    monthly_rental=2800,
    monthly_expenses=600,
    mortgage_payment=2200,
    years=10
)
```

### Mortgage Calculator

```python
from agents.real_estate.agent import MortgageCalculator

mortgage = MortgageCalculator()
calc = mortgage.calculate(
    home_price=450000,
    down_payment_pct=20,
    interest_rate=6.5,
    loan_term_years=30,
    property_tax_annual=5400,
    insurance_annual=1800
)

# Compare rates
comparison = mortgage.compare_rates(
    loan_amount=360000,
    rates=[5.5, 6.0, 6.5, 7.0],
    term_years=30
)
```

---

## API Reference

| Class | Description |
|-------|-------------|
| `PropertyValuationEngine` | Multi-method property valuation |
| `MarketAnalyzer` | Market health, trends, and comparison |
| `InvestmentAnalyzer` | ROI, cash flow, and strategy analysis |
| `MortgageCalculator` | Payment and amortization calculations |
| `RentalAnalyzer` | Rental income and optimization |
| `PortfolioManager` | Portfolio tracking and rebalancing |
| `DueDiligenceManager` | Due diligence checklists and progress |
| `TaxAnalyzer` | Tax impact analysis |
| `RiskAssessor` | Property risk assessment |
| `PropertyComparisonEngine` | Multi-property comparison |

### Enums

| Enum | Values |
|------|--------|
| `PropertyType` | SINGLE_FAMILY, CONDO, TOWNHOUSE, MULTI_FAMILY, APARTMENT, LAND, COMMERCIAL, INDUSTRIAL, MIXED_USE |
| `ListingStatus` | ACTIVE, PENDING, SOLD, OFF_MARKET, EXPIRED, WITHDRAWN |
| `PropertyCondition` | EXCELLENT, GOOD, FAIR, POOR, NEEDS_RENOVATION |
| `MarketCycle` | RECOVERY, EXPANSION, HYPER_SUPPLY, RECESSION |
| `InvestmentStrategy` | BUY_AND_HOLD, FLIPPING, RENTAL_INCOME, BRRRR, WHOLESALE, SHORT_TERM_RENTAL, COMMERCIAL_LEASE, DEVELOPMENT |
| `DueDiligencePhase` | INITIAL, UNDER_CONTRACT, INSPECTION, APPRAISAL, FINANCING, CLOSING, POST_CLOSING |
| `RiskCategory` | MARKET, LIQUIDITY, CREDIT, OPERATIONAL, LEGAL, ENVIRONMENTAL, NATURAL_DISASTER, REGULATORY |

---

## Examples

### Complete Investment Analysis

```python
from agents.real_estate.agent import RealEstateAgent

agent = RealEstateAgent()

# Register property
agent.valuation.register_property(prop)
agent.valuation.add_comparable("P001", comp)

# Multi-method valuation
comp_val = agent.valuation.comparable_sales_valuation("P001")
income_val = agent.valuation.income_approach_valuation("P001", annual_rental_income=33600, cap_rate=0.055)
cost_val = agent.valuation.cost_approach_valuation("P001", land_value=150000, replacement_cost_per_sqft=200, depreciation_pct=0.15)

# Investment analysis
analysis = agent.investment.analyze_property(
    property_id="P001",
    purchase_price=450000,
    down_payment_pct=20,
    interest_rate=6.5,
    loan_term_years=30,
    monthly_rental_income=2800,
    monthly_expenses=600
)

# Risk assessment
risks = agent.risks.assess_property_risks("P001", PropertyType.SINGLE_FAMILY, 2005)

# Tax analysis
tax = agent.tax.analyze_tax_impact("P001", 450000, 33600, 12000)
```

---

## Configuration

```python
from agents.real_estate.agent import RealEstateConfig

config = RealEstateConfig(
    default_currency="USD",
    default_mortgage_rate=6.5,
    default_loan_term=30,
    default_down_payment_pct=20.0,
    default_vacancy_rate=0.05,
    default_maintenance_rate=0.01,
    default_management_fee_rate=0.08,
    default_insurance_rate=0.005,
    comparable_search_radius_miles=5.0,
    max_comparables=10,
    min_comparables=3,
    appreciation_rate_default=0.03,
    discount_rate_default=0.08,
    holding_cost_monthly_rate=0.005,
)
```

| Setting | Default | Description |
|---------|---------|-------------|
| `default_currency` | "USD" | Currency for calculations |
| `default_mortgage_rate` | 6.5 | Default interest rate (%) |
| `default_loan_term` | 30 | Default loan term (years) |
| `default_down_payment_pct` | 20.0 | Default down payment (%) |
| `default_vacancy_rate` | 0.05 | Default vacancy rate |
| `default_maintenance_rate` | 0.01 | Default maintenance rate |
| `default_management_fee_rate` | 0.08 | Default management fee |
| `default_insurance_rate` | 0.005 | Default insurance rate |
| `comparable_search_radius_miles` | 5.0 | Max radius for comps |
| `min_comparables` | 3 | Minimum comps for valuation |
| `appreciation_rate_default` | 0.03 | Default annual appreciation |

---

## Best Practices

### Valuation
1. Always use multiple valuation methods and cross-validate
2. Select comparables within 1 mile and 6 months
3. Adjust for size, condition, age, and location differences
4. Document all assumptions and adjustments

### Investment Analysis
1. Include all expenses (tax, insurance, maintenance, management, vacancy)
2. Stress-test with different rent growth and expense scenarios
3. Consider both cash flow and appreciation in ROI calculations
4. Account for closing costs in both purchase and sale

### Market Analysis
1. Track multiple indicators (price, rent, vacancy, DOM, inventory)
2. Understand the current market cycle position
3. Compare multiple markets before investing
4. Monitor population and employment growth trends

### Due Diligence
1. Never skip inspections — they save money long-term
2. Complete all items before removing contingencies
3. Document everything for legal protection
4. Use the checklist to ensure nothing is missed

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Valuation needs 3+ comparables | Add more comparable sales data |
| Negative cash flow | Increase rent or reduce expenses |
| Flip shows negative profit | Renovation cost too high or ARV too low |
| Portfolio shows over-allocation | Follow rebalance suggestions |
| Risk score is "high" | Address highest-impact risks first |

---

## Files

| File | Description |
|------|-------------|
| `agent.py` | Full implementation (all classes and logic) |
| `GROK.md` | Agent identity, capabilities, and code examples |
| `ARCHITECTURE.md` | System architecture with diagrams |
| `README.md` | This file — overview and quick start |

---

## License

MIT License — see [LICENSE](../../LICENSE) for details.

---

*Analyze, invest, and manage real estate with confidence and precision.*

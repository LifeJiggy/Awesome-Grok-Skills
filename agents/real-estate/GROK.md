---
name: "Real Estate Agent"
version: "2.0.0"
description: "Property analysis, valuation, investment analysis, and transaction assistance platform"
author: "Awesome Grok Skills"
license: "MIT"
tags:
  - real-estate
  - property-valuation
  - investment-analysis
  - mortgage
  - market-analysis
  - portfolio-management
  - due-diligence
  - rental-analysis
  - tax-analysis
  - risk-assessment
category: "real-estate"
personality: "property-consultant"
use_cases:
  - "property valuation using comparable sales, income, and cost approaches"
  - "market analysis and trend forecasting"
  - "investment ROI and cash flow analysis"
  - "mortgage calculation and amortization schedules"
  - "rental income optimization"
  - "portfolio management and rebalancing"
  - "due diligence checklist automation"
  - "tax impact analysis for real estate investments"
  - "property risk assessment"
  - "multi-property comparison and ranking"
---

# Real Estate Agent

> Real estate analysis platform with multi-method property valuation, market intelligence, investment modeling, and portfolio management.

## Agent Identity

You are the Real Estate Agent — a senior real estate analyst and investment consultant capable of valuing properties using multiple approaches, analyzing market conditions, modeling investment returns, calculating mortgages and amortization schedules, optimizing rental income, managing investment portfolios, automating due diligence, analyzing tax implications, assessing property risks, and comparing properties side-by-side. You combine deep market knowledge with quantitative analysis.

### Core Principles

1. **Multi-Method Valuation**: Cross-validate using comparable sales, income, and cost approaches
2. **Data-Driven Decisions**: Every recommendation backed by quantitative analysis
3. **Risk-Aware**: Every investment analysis includes risk assessment
4. **Full Lifecycle**: From market research through due diligence to portfolio management
5. **Transparency**: All assumptions and calculations visible and auditable
6. **Actionable Insights**: Provide clear recommendations, not just data
7. **Market Awareness**: Account for market cycles and economic conditions

---

## Capabilities

### Property Valuation

```python
from agents.real_estate.agent import PropertyValuationEngine, Property, PropertyType, ListingStatus, PropertyCondition
from agents.real_estate.agent import ComparableSale, PropertyType

engine = PropertyValuationEngine()

# Register a property
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
    features=["granite countertops", "hardwood floors"],
    photos=[],
    mls_number="MLS12345"
)
engine.register_property(prop)

# Add comparable sales
comp = ComparableSale(
    comp_id="C001",
    address="125 Main St",
    property_type=PropertyType.SINGLE_FAMILY,
    sold_price=460000,
    sold_date=datetime(2024, 1, 15),
    sqft=2100,
    bedrooms=3,
    bathrooms=2.0,
    lot_size_sqft=8500,
    year_built=2004,
    condition=PropertyCondition.GOOD,
    distance_miles=0.2,
    adjustments={}
)
engine.add_comparable("P001", comp)

# Get valuation
valuation = engine.comparable_sales_valuation("P001")
print(f"Estimated Value: ${valuation.estimated_value:,.2f}")
print(f"Confidence: {valuation.confidence:.1%}")
print(f"Range: ${valuation.value_range[0]:,.2f} - ${valuation.value_range[1]:,.2f}")
```

### Market Analysis

```python
from agents.real_estate.agent import MarketAnalyzer, MarketData, MarketCycle

market_analyzer = MarketAnalyzer()

market = MarketData(
    market_id="M001",
    name="Austin, TX",
    median_price=425000,
    avg_price_per_sqft=285,
    median_rent=2200,
    vacancy_rate=0.04,
    cap_rate=0.055,
    days_on_market=25,
    inventory_months=2.5,
    price_change_yoy=8.5,
    rent_change_yoy=5.2,
    population_growth=0.035,
    employment_growth=0.04,
    median_household_income=85000,
    market_cycle=MarketCycle.EXPANSION,
    last_updated=datetime.utcnow()
)
market_analyzer.register_market(market)

# Get market health
health = market_analyzer.market_health("M001")
print(f"Health Score: {health['health_score']}")
print(f"Recommendation: {health['recommendation']}")

# Compare markets
comparison = market_analyzer.compare_markets(["M001", "M002"])

# Get investment hotspots
hotspots = market_analyzer.investment_hotspots()
```

### Investment Analysis

```python
from agents.real_estate.agent import InvestmentAnalyzer, InvestmentStrategy

analyzer = InvestmentAnalyzer()

# Analyze a buy-and-hold investment
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

print(f"Monthly Cash Flow: ${analysis.cash_flow_monthly:,.2f}")
print(f"Cap Rate: {analysis.cap_rate:.2f}%")
print(f"Cash-on-Cash Return: {analysis.cash_on_cash_return:.2f}%")
print(f"Break-Even: {analysis.break_even_years:.1f} years")
print(f"5-Year ROI: {analysis.roi_5yr:.2f}%")

# Analyze a flip
flip = analyzer.flip_analysis(
    purchase_price=350000,
    renovation_cost=50000,
    holding_months=6,
    after_repair_value=480000
)
print(f"Flip Profit: ${flip['profit']:,.2f}")
print(f"Flip ROI: {flip['roi_pct']:.2f}%")

# Cash flow projection
projections = analyzer.cash_flow_projection(
    monthly_rental=2800,
    monthly_expenses=600,
    mortgage_payment=2200,
    years=10
)
```

### Mortgage Calculation

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

print(f"Monthly Payment: ${calc.total_monthly:,.2f}")
print(f"Principal & Interest: ${calc.principal_interest:,.2f}")
print(f"Total Interest: ${calc.total_interest:,.2f}")
print(f"Total Cost: ${calc.total_cost:,.2f}")

# Compare rates
rates_comparison = mortgage.compare_rates(
    loan_amount=360000,
    rates=[5.5, 6.0, 6.5, 7.0],
    term_years=30
)
```

### Rental Analysis

```python
from agents.real_estate.agent import RentalAnalyzer

rental = RentalAnalyzer()

analysis = rental.analyze_rental(
    property_id="P001",
    monthly_rent=2800,
    property_tax_annual=5400,
    insurance_annual=1800,
    hoa_monthly=0,
    maintenance_annual=4500,
    management_fee_pct=0.08
)

print(f"Net Operating Income: ${analysis.net_operating_income:,.2f}")
print(f"Gross Yield: {analysis.gross_yield:.2f}%")
print(f"Net Yield: {analysis.net_yield:.2f}%")

# Optimize rent
optimization = rental.rent_optimization(
    current_rent=2800,
    market_avg=2600,
    occupancy_rate=0.95
)
print(f"Recommended Rent: ${optimization['recommended']['new_rent']:,.2f}")
```

### Portfolio Management

```python
from agents.real_estate.agent import PortfolioManager, PortfolioProperty, InvestmentStrategy

portfolio = PortfolioManager()

pp = PortfolioProperty(
    portfolio_property_id="PP001",
    property_id="P001",
    acquisition_price=450000,
    acquisition_date=datetime(2022, 1, 1),
    current_value=485000,
    monthly_income=2800,
    monthly_expenses=600,
    equity=135000,
    strategy=InvestmentStrategy.BUY_AND_HOLD
)
portfolio.add_property(pp)

summary = portfolio.portfolio_summary()
allocation = portfolio.allocation_by_type()
rebalance = portfolio.rebalance_suggestions()
performance = portfolio.performance_history()
```

### Due Diligence

```python
from agents.real_estate.agent import DueDiligenceManager, DueDiligencePhase

dd = DueDiligenceManager()

checklist = dd.create_checklist("P001", DueDiligencePhase.INSPECTION)
progress = dd.checklist_progress(checklist)
print(f"Progress: {progress['progress_pct']}%")

# Complete items
dd.complete_item(checklist, checklist.items[0].item_id, notes="Completed by inspector")
```

### Tax Analysis

```python
from agents.real_estate.agent import TaxAnalyzer

tax = TaxAnalyzer()

analysis = tax.analyze_tax_impact(
    property_id="P001",
    purchase_price=450000,
    annual_rental_income=33600,
    annual_expenses=12000
)

print(f"Annual Property Tax: ${analysis.annual_property_tax:,.2f}")
print(f"Depreciation Deduction: ${analysis.depreciation_deduction:,.2f}")
print(f"Net Tax Impact: ${analysis.net_tax_impact:,.2f}")
print(f"Tax Strategies: {analysis.tax_strategies}")
```

### Risk Assessment

```python
from agents.real_estate.agent import RiskAssessor, PropertyType

assessor = RiskAssessor()

risks = assessor.assess_property_risks(
    property_id="P001",
    property_type=PropertyType.SINGLE_FAMILY,
    year_built=2005,
    location_risk_factors=["flood zone nearby"]
)

summary = assessor.risk_summary(risks)
print(f"Overall Rating: {summary['overall_rating']}")
```

### Property Comparison

```python
from agents.real_estate.agent import PropertyComparisonEngine

comparator = PropertyComparisonEngine()

result = comparator.compare(
    properties=[prop1, prop2, prop3],
    weights={"price": 0.25, "sqft": 0.15, "condition": 0.15, "location": 0.20, "value_per_sqft": 0.15, "features": 0.10}
)

print(f"Winner: {result['winner']}")
for p in result['comparison']:
    print(f"  {p['address']}: Score {p['score']:.1f}")
```

---

## Data Models

### Property

| Field | Type | Description |
|-------|------|-------------|
| `property_id` | str | Unique identifier |
| `address` | str | Full address |
| `city` | str | City name |
| `state` | str | State code |
| `zip_code` | str | ZIP code |
| `property_type` | PropertyType | Single family, condo, etc. |
| `listing_status` | ListingStatus | Active, pending, sold |
| `condition` | PropertyCondition | Excellent, good, fair, poor |
| `price` | float | Listed price |
| `bedrooms` | int | Number of bedrooms |
| `bathrooms` | float | Number of bathrooms |
| `sqft` | int | Square footage |
| `year_built` | int | Year constructed |
| `hoa_monthly` | float | Monthly HOA fee |

### InvestmentAnalysis

| Field | Type | Description |
|-------|------|-------------|
| `analysis_id` | str | Unique identifier |
| `property_id` | str | Property being analyzed |
| `strategy` | InvestmentStrategy | Buy-and-hold, flip, etc. |
| `purchase_price` | float | Purchase price |
| `down_payment` | float | Down payment amount |
| `loan_amount` | float | Loan amount |
| `cash_flow_monthly` | float | Monthly cash flow |
| `cap_rate` | float | Capitalization rate (%) |
| `cash_on_cash_return` | float | Cash-on-cash return (%) |
| `break_even_years` | float | Years to break even |

---

## Checklists

### Investment Analysis

- [ ] Market research completed
- [ ] Property valuation performed (multi-method)
- [ ] Rental income estimated
- [ ] Expenses itemized (tax, insurance, maintenance, management)
- [ ] Mortgage calculated with amortization
- [ ] Cash flow projected over holding period
- [ ] Cap rate and cash-on-cash computed
- [ ] Risk assessment completed
- [ ] Tax implications analyzed
- [ ] Exit strategy defined

### Due Diligence

- [ ] Property disclosure reviewed
- [ ] Title search completed
- [ ] Zoning verified
- [ ] HOA documents reviewed
- [ ] General inspection completed
- [ ] Termite inspection completed
- [ ] Roof inspection completed
- [ ] HVAC inspection completed
- [ ] Plumbing inspection completed
- [ ] Electrical inspection completed
- [ ] Foundation inspection completed
- [ ] Appraisal ordered and reviewed
- [ ] Loan application submitted
- [ ] Insurance bound
- [ ] Final walkthrough completed

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Valuation fails | Insufficient comparables | Add more comps or use income approach |
| Negative cash flow | High expenses or low rent | Reduce expenses or increase rent |
| High risk score | Multiple risk factors | Address highest-impact risks first |
| Portfolio imbalance | Over-allocation to one strategy | Follow rebalance suggestions |
| Low health score | Poor market indicators | Consider different markets |

---

## Expected Outcomes

| Metric | Target | Description |
|--------|--------|-------------|
| Valuation Accuracy | Within 10% | Compared to actual sale price |
| Investment Return | > 8% CoC | Cash-on-cash return target |
| Portfolio Diversification | No strategy > 40% | Risk mitigation |
| Due Diligence Coverage | 100% | All items completed |
| Risk Mitigation | All high risks addressed | Active mitigation plans |

---

*Analyze properties, model investments, manage portfolios with confidence.*
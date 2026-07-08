# Real Estate Agent Architecture

> Comprehensive architecture for the Real Estate Agent — property valuation, market analysis, investment analysis, portfolio management, and due diligence.

---

## Table of Contents

1. [Overview](#overview)
2. [System Components](#system-components)
3. [Data Flow](#data-flow)
4. [Key Components](#key-components)
5. [Component Details](#component-details)
6. [Design Patterns](#design-patterns)
7. [Tech Stack](#tech-stack)
8. [Configuration](#configuration)
9. [Performance](#performance)
10. [Security](#security)
11. [Scalability](#scalability)
12. [Extension Points](#extension-points)
13. [Monitoring & Observability](#monitoring--observability)
14. [Glossary](#glossary)
15. [Appendix: Design Decisions](#appendix-design-decisions)

---

## Overview

The Real Estate Agent is a comprehensive real estate analysis platform integrating property valuation, market analysis, investment analysis, mortgage calculation, rental optimization, portfolio management, due diligence automation, tax analysis, risk assessment, and property comparison into a unified system.

### Design Principles

- **Multi-Method Valuation**: Cross-validate using comparable sales, income, and cost approaches.
- **Data-Driven Decisions**: Every recommendation backed by quantitative analysis.
- **Risk-Aware**: Every investment analysis includes risk assessment.
- **Full Lifecycle**: From market research through due diligence to portfolio management.
- **Extensibility**: Plugin architecture for custom valuation models and integrations.

---

## System Components

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        Real Estate Agent (Orchestrator)                         │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐  │
│  │PropertyValuation  │  │  MarketAnalyzer   │  │   InvestmentAnalyzer        │  │
│  │    Engine         │  │                   │  │                              │  │
│  │                   │  │ • Market health   │  │ • Buy & hold analysis        │  │
│  │ • Comparable sales│  │ • Compare markets │  │ • Flip analysis              │  │
│  │ • Income approach │  │ • Neighborhoods   │  │ • Cash flow projection       │  │
│  │ • Cost approach   │  │ • Trend analysis  │  │ • ROI calculation            │  │
│  │ • Auto valuation  │  │ • Hotspot detect  │  │ • Break-even analysis        │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────────┘  │
│                                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐  │
│  │MortgageCalculator │  │  RentalAnalyzer   │  │    PortfolioManager         │  │
│  │                   │  │                   │  │                              │  │
│  │ • Payment calc    │  │ • Rental analysis │  │ • Property tracking          │  │
│  │ • Amortization    │  │ • Rent optimize   │  │ • Allocation by strategy     │  │
│  │ • Rate compare    │  │ • Yield analysis  │  │ • Performance history        │  │
│  │ • Total cost      │  │ • Expense breakdown│ │ • Rebalance suggestions      │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────────┘  │
│                                                                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────────┐  │
│  │DueDiligence       │  │   TaxAnalyzer     │  │    RiskAssessor             │  │
│  │    Manager        │  │                   │  │                             │  │
│  │ • Checklists      │  │ • Property tax    │  │ • Property risk assessment  │  │
│  │ • Phase tracking  │  │ • Depreciation    │  │ • Risk scoring              │  │
│  │ • Item completion │  │ • Tax strategies  │  │ • Mitigation suggestions    │  │
│  │ • Progress        │  │ • Net tax impact  │  │ • Risk summary              │  │
│  └──────────────────┘  └──────────────────┘  └──────────────────────────────┘  │
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐   │
│  │                  PropertyComparisonEngine                                │   │
│  │  • Side-by-side  • Weighted scoring  • Ranking  • Winner selection      │   │
│  └──────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
                    ┌──────────────────────────┐
                    │     Property Data         │
                    │     Market Data           │
                    │     Financial Data        │
                    └────────────┬─────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
    ┌─────────▼─────────┐ ┌─────▼──────┐ ┌────────▼────────┐
    │PropertyValuation   │ │MarketAnalyzer│ │InvestmentAnalyzer│
    │(Register →         │ │(Register →  │ │(Analyze →        │
    │ Comparable →       │ │ Health →    │ │ Cash flow →      │
    │ Adjust →           │ │ Compare →   │ │ ROI →            │
    │ Estimate)          │ │ Forecast)   │ │ Recommend)       │
    └─────────┬─────────┘ └─────┬──────┘ └────────┬────────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
    ┌─────────▼─────────┐ ┌─────▼──────┐ ┌────────▼────────┐
    │MortgageCalculator  │ │RentalAnalyzer│ │PropertyComparison│
    │(Calculate →        │ │(Analyze →   │ │(Compare →        │
    │ Amortize →         │ │ Optimize →  │ │ Score →          │
    │ Compare)           │ │ Yield)      │ │ Rank)            │
    └─────────┬─────────┘ └─────┬──────┘ └────────┬────────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
    ┌─────────▼─────────┐ ┌─────▼──────┐ ┌────────▼────────┐
    │DueDiligenceManager │ │ TaxAnalyzer │ │  RiskAssessor    │
    │(Create → Complete →│ │(Analyze →  │ │(Assess → Score →│
    │ Progress →         │ │ Deduct →   │ │ Mitigate)       │
    │ Verify)            │ │ Strategy)  │ │                 │
    └─────────┬─────────┘ └─────┬──────┘ └────────┬────────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │   PortfolioManager        │
                    │  (Add → Track →           │
                    │   Allocate → Rebalance)   │
                    └──────────────────────────┘
```

### Property Valuation Flow

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐
│  Register    │────▶│   Add Comps  │────▶│  Comparable   │
│  Property    │     │   (3-10)     │     │  Sales Method │
└─────────────┘     └──────────────┘     └───────┬──────┘
                                                  │
                    ┌──────────────┐              │
                    │  Income      │──────────────┤
                    │  Approach    │              │
                    └──────────────┘              │
                                                  ▼
                    ┌──────────────┐     ┌──────────────┐
                    │  Cost        │────▶│  Weighted    │
                    │  Approach    │     │  Valuation   │
                    └──────────────┘     └───────┬──────┘
                                                  │
                                                  ▼
                                         ┌──────────────┐
                                         │  Valuation   │
                                         │  Result      │
                                         └──────────────┘
```

### Investment Analysis Flow

```
Purchase Price + Financing → Mortgage Payment
         │
         ▼
Rental Income - Expenses - Mortgage → Cash Flow
         │
         ├──→ Cap Rate = NOI / Purchase Price
         ├──→ Cash-on-Cash = Annual CF / Cash Invested
         ├──→ ROI = (Appreciation + CF) / Investment
         └──→ Break-Even = Cash Invested / Annual CF
```

### Due Diligence Phase Flow

```
INITIAL ──→ UNDER_CONTRACT ──→ INSPECTION ──→ APPRAISAL
    │              │                │              │
    ▼              ▼                ▼              ▼
Disclosure    Purchase       Home inspect    Ordered
Zoning        Inspection     Termite         appraisal
HOA review    Financing      Roof/HVAC       Review
              contingencies  Foundation
                    │
                    ▼
              FINANCING ──→ CLOSING ──→ POST_CLOSING
                  │            │              │
                  ▼            ▼              ▼
              Loan app     Final walk    Record deed
              Income ver   Title ins     Transfer util
              Credit check Wire transfer Insurance
```

---

## Key Components

### 1. PropertyValuationEngine

Multi-method property valuation.

**Comparable Sales Method:**
```
Adjusted Price = Comp Price + Σ Adjustments

Adjustments:
  sqft_diff × $150/sqft
  bed_diff × $10,000/bedroom
  bath_diff × $7,500/bathroom
  year_diff × $500/year
```

**Income Approach:**
```
Value = Effective Gross Income / Cap Rate
EGI = Annual Rent × (1 - Vacancy Rate)
```

**Cost Approach:**
```
Value = Land Value + Replacement Cost - Depreciation
Depreciation = Replacement Cost × Depreciation %
```

### 2. MarketAnalyzer

Market health assessment and trend analysis.

**Health Score Formula:**
```
Base: 50
+ min(price_change_yoy × 5, 15)    if positive
+ 10 if vacancy < 5%
+ 10 if DOM < 30
+ 10 if population_growth > 2%
- deductions for negative indicators
```

**Market Cycle Recognition:**
```
Recovery → Expansion → Hyper Supply → Recovery
Low prices    Rising      Oversupply    Bottom
High return   Momentum    Risk          Opportunity
```

### 3. InvestmentAnalyzer

Comprehensive investment analysis.

**Cash Flow:**
```
Monthly CF = Rental Income - Expenses - Mortgage Payment
```

**Cap Rate:**
```
Cap Rate = (Annual Rental - Annual Expenses) / Purchase Price × 100
```

**Cash-on-Cash Return:**
```
CoC = (Annual CF / Total Cash Invested) × 100
Total Cash = Down Payment + Closing Costs + Repairs
```

**Break-Even:**
```
Break-Even Years = Total Cash / Annual Cash Flow
```

**Flip Analysis:**
```
Profit = ARV - Purchase - Renovation - Holding - Closing Costs
ROI = Profit / Total Investment × 100
```

### 4. MortgageCalculator

Mortgage payment and amortization calculation.

**Monthly Payment (P&I):**
```
M = P × [r(1+r)^n] / [(1+r)^n - 1]
Where: P = loan amount, r = monthly rate, n = total payments
```

**Amortization:**
```
Month 1: Interest = Balance × Rate, Principal = Payment - Interest
Month 2: New Balance = Balance - Principal
... repeat until Balance = 0
```

### 5. RentalAnalyzer

Rental income optimization.

**Revenue Optimization:**
```
For each rent scenario:
  New Occupancy = max(0.5, current_occupancy - rent_change × 0.02)
  Revenue = New Rent × New Occupancy
Choose rent that maximizes revenue
```

### 6. PortfolioManager

Investment portfolio tracking and rebalancing.

**Portfolio Metrics:**
```
Total Value = Σ Current Values
Total Equity = Σ (Current Value - Loan Balance)
Portfolio ROI = Total Equity / Total Investment × 100
Avg Cap Rate = mean(Net Income / Current Value) × 100
```

### 7. DueDiligenceManager

Standardized checklists for each due diligence phase.

**Checklist Coverage:**
- Initial: 4 items (disclosure, title, zoning, HOA)
- Under Contract: 4 items (agreement, earnest money, contingencies)
- Inspection: 8 items (general, termite, roof, HVAC, plumbing, electrical, foundation, sewer)
- Appraisal: 2 items (ordered, reviewed)
- Financing: 4 items (application, income, credit, insurance)
- Closing: 4 items (walkthrough, title, disclosure, wire)
- Post-Closing: 4 items (deed, utilities, insurance, management)

### 8. TaxAnalyzer

Tax impact analysis for real estate investments.

**Depreciation:**
```
Annual Depreciation = (Purchase Price × 0.8) / 27.5 years
```

**Net Tax Impact:**
```
Net = -Property Tax + Tax Benefit from Loss
Tax Benefit = max(0, -Taxable Income) × Marginal Rate
```

### 9. RiskAssessor

Property risk assessment with scoring.

**Risk Score:**
```
Risk Score = Probability × Impact
Rating: < 0.2 = Low, 0.2-0.4 = Medium, > 0.4 = High
```

### 10. PropertyComparisonEngine

Multi-criteria property comparison.

**Scoring Weights:**
```
Price: 25%
Sqft: 15%
Condition: 15%
Location: 20%
Value/Sqft: 15%
Features: 10%
```

---

## Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **Strategy** | Multiple valuation methods | PropertyValuationEngine |
| **Factory** | Mortgage calculation creation | MortgageCalculator |
| **Composite** | Portfolio of properties | PortfolioManager |
| **Template Method** | Due diligence checklists | DueDiligenceManager |
| **Observer** | Market trend monitoring | MarketAnalyzer |
| **Chain of Responsibility** | Risk assessment pipeline | RiskAssessor |
| **Facade** | RealEstateAgent orchestrator | Orchestrator |

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Data Structures | dataclasses, Enum, Dict, List |
| Statistics | statistics, math |
| Date/Time | datetime, timedelta |
| ID Generation | uuid4 |
| Logging | Python logging module |
| Optional | SQLite, pandas, matplotlib |

---

## Configuration

```python
RealEstateConfig(
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

---

## Performance

| Metric | Target | Notes |
|--------|--------|-------|
| Property registration | < 2ms | Dict insertion |
| Comparable valuation | < 10ms | For 10 comps |
| Income valuation | < 2ms | Simple division |
| Mortgage calculation | < 5ms | Including amortization (360 months) |
| Market health score | < 5ms | Arithmetic |
| Investment analysis | < 10ms | Multiple calculations |
| Portfolio summary | < 5ms | Aggregate over properties |
| Risk assessment | < 5ms | 3-5 risk items |
| Property comparison | < 10ms | For 5 properties |
| Full status | < 20ms | All components |

---

## Security

- **Input Validation**: All public methods validate inputs.
- **Financial Precision**: Round to 2 decimal places for currency.
- **No External Calls**: All computation local.
- **Audit Trail**: Valuation history maintained per property.
- **Data Isolation**: Each property and portfolio independent.

---

## Scalability

| Dimension | Strategy |
|-----------|----------|
| Property volume | Indexed by ID, city, type |
| Comparable data | Shuffled by distance and recency |
| Market data | Indexed by market ID |
| Portfolio size | Aggregate calculations scale O(n) |
| Amortization | O(n) for n months; bounded by loan term |
| Time series | Rolling windows for trend analysis |

---

## Extension Points

1. **Custom Valuation Models**: Machine learning, hedonic pricing.
2. **MLS Integration**: Pull comps from MLS data feeds.
3. **Geolocation APIs**: Latitude/longitude enrichment.
4. **Custom Market Indicators**: Additional economic indicators.
5. **Portfolio Analytics**: Advanced portfolio theory, Sharpe ratio.
6. **Document Generation**: PDF reports, offering letters.

---

## Monitoring & Observability

| Signal | Method |
|--------|--------|
| Properties tracked | `len(valuation.properties)` |
| Markets monitored | `len(market.markets)` |
| Portfolio value | `portfolio.portfolio_summary()["total_value"]` |
| Valuation accuracy | Compare estimates vs. actual sales |
| Market health | `market.market_health(id)["health_score"]` |
| Investment returns | `portfolio.performance_history()` |

---

## Glossary

| Term | Definition |
|------|-----------|
| Cap Rate | Capitalization Rate = NOI / Value |
| NOI | Net Operating Income |
| CoC | Cash-on-Cash Return |
| ARV | After Repair Value |
| DOM | Days on Market |
| TAM | Total Addressable Market |
| SAM | Serviceable Addressable Market |
| DSCR | Debt Service Coverage Ratio |
| LTV | Loan-to-Value Ratio |
| BRRRR | Buy, Rehab, Rent, Refinance, Repeat |
| 1031 Exchange | Tax-deferred property exchange |

---

## Appendix: Design Decisions

| Decision | Rationale |
|----------|-----------|
| Three valuation methods | Cross-validation increases accuracy |
| Adjustments based on sqft/bed/bath | Most impactful differentiators |
| Cap rate for income approach | Industry standard metric |
| 27.5-year depreciation | IRS residential rental standard |
| Risk score = P × I | Standard risk assessment formula |
| 3σ control limits | Industry standard for SPC |
| In-memory storage | Simplicity; persistence optional |
| Portfolio by strategy | Enables rebalancing recommendations |

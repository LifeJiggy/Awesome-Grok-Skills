---
name: business-development
version: 2.0.0
description: >
  Autonomous B2B partnership discovery, deal pipeline management, revenue modeling,
  market intelligence, competitive analysis, negotiation strategy, growth planning,
  channel partner design, due diligence tracking, and performance analytics.
author: MiMoCode
tags:
  - business-development
  - partnerships
  - revenue-modeling
  - market-analysis
  - deal-pipeline
  - growth-strategy
  - competitive-analysis
  - negotiation
  - channel-partners
  - due-diligence
  - sales-forecasting
  - value-proposition
  - market-entry
  - outreach
  - conversion-funnel
  - quarterly-review
  - b2b-saas
  - ansoff-matrix
  - npv-irr
  - swot-analysis
category: business-operations
personality: strategic, analytical, collaborative, data-driven, decisive
use_cases:
  - Partner discovery and evaluation
  - Deal pipeline management and forecasting
  - Revenue modeling with NPV/IRR analysis
  - Market sizing and TAM/SAM/SOM analysis
  - Competitive landscape assessment
  - Negotiation strategy optimization
  - Growth strategy planning (Ansoff matrix)
  - Channel partner program design
  - Due diligence execution
  - Quarterly business reviews
  - Sales forecasting with scenario planning
  - Value proposition development
  - Market entry strategy planning
  - Outreach campaign design and analysis
  - Conversion funnel bottleneck identification
  - BANT lead qualification
  - Pricing model design
  - Expansion roadmap planning
  - Partnership agreement structuring
---

# Business Development Agent — Agent Identity & Capabilities

## Table of Contents

1. [Agent Identity & Purpose](#1-agent-identity--purpose)
2. [Core Principles](#2-core-principles)
3. [Detailed Capabilities](#3-detailed-capabilities)
4. [Operational Guidelines](#4-operational-guidelines)
5. [Method Signatures & Usage Patterns](#5-method-signatures--usage-patterns)
6. [Data Models Reference](#6-data-models-reference)
7. [Checklists](#7-checklists)
8. [Troubleshooting Guide](#8-troubleshooting-guide)

---

## 1. Agent Identity & Purpose

### Who This Agent Is

The Business Development Agent is a strategic automation engine designed to replace
manual, spreadsheet-driven B2B business development processes with structured,
data-driven decision frameworks. It serves as the central nervous system for all
partnership, pipeline, revenue, market, and growth activities.

### Mission Statement

To accelerate B2B revenue growth by automating the identification, evaluation,
structuring, negotiation, and management of business partnerships and market
opportunities — while maintaining full transparency in every scoring and
recommendation algorithm.

### Target Users

| User Role | Primary Use Cases |
|-----------|------------------|
| VP Business Development | Pipeline health, partner scorecards, quarterly reviews |
| Head of Partnerships | Partner discovery, evaluation, deal structuring |
| Revenue Operations | Revenue modeling, sales forecasting, funnel analysis |
| Product Marketing | Value proposition canvas, competitive analysis |
| Strategy Lead | Market analysis, growth strategy, market entry planning |
| Deal Desk | Negotiation strategy, due diligence, contract structuring |

### System Boundaries

- **In scope**: Partner discovery, deal management, revenue modeling, market intelligence, competitive analysis, negotiation, growth strategy, channel design, due diligence, performance analytics, outreach, funnel analysis
- **Out of scope**: CRM data storage, contract execution, legal document generation, accounting, HR functions, direct email sending, calendar scheduling
- **State**: In-memory (no persistence layer — serialize outputs for external storage)
- **Dependencies**: Python 3.11+ stdlib only (zero external packages)

---

## 2. Core Principles

### Principle 1: Data Over Intuition

Every recommendation is backed by weighted scoring, not gut feel. Composite scores
combine multiple dimensions with explicit weights so the reasoning is transparent
and auditable. When a partner is recommended, you can trace the recommendation to
its five component scores and their published weights.

```
composite = synergy(0.30) + strategic(0.25) + cultural(0.15) + reach(0.15) + capability(0.15)
```

### Principle 2: Structured Pipelines

Deals move through defined stages with gate criteria. Nothing progresses without
meeting the requirements of the previous stage. This prevents pipeline pollution
and ensures forecasting accuracy. The pipeline health metric continuously monitors
for stagnation and decline.

```
IDENTIFICATION(5%) → QUALIFICATION(15%) → PROPOSAL(35%) → NEGOTIATION(60%) → CLOSING(85%) → POST_CLOSE(100%)
```

### Principle 3: Multi-Scenario Thinking

Revenue forecasts always present conservative, base, and optimistic scenarios.
Decision-makers get a range, not a single number. NPV and IRR ground the analysis
in financial reality. Payback period provides operational context.

### Principle 4: Market-First Strategy

Growth strategies are derived from market analysis, not internal desire. The Ansoff
matrix provides a rigorous framework for choosing between penetration, development,
product, and diversification strategies. Strategy selection is automatic based on
the company's current product and market portfolio.

### Principle 5: Transparent Scoring

Every score — partner composite, market attractiveness, pipeline health, negotiation
ZOPA, value proposition fit — uses published weights and formulas. No black boxes.
Stakeholders can trace any recommendation to its inputs and verify the math.

### Principle 6: Actionable Outputs

Every method returns structured data that maps directly to next steps. A partner
evaluation produces a scorecard with a recommendation. A due diligence report
identifies high-risk areas and proposes mitigation. A negotiation strategy includes
concessions and leverage points ready for execution.

### Principle 7: Risk Awareness

Competitive threats are scored and classified (CRITICAL/HIGH/MODERATE/LOW). Pipeline
health is continuously monitored. Negotiation strategies include walk-away points.
Growth plans include risk registers with mitigation strategies. Due diligence
identifies high-risk areas before commitment.

### Principle 8: Full Lifecycle Coverage

From initial partner identification through post-close maintenance and expansion,
the agent covers every phase. No hand-offs between disconnected tools. The same
agent that discovers a partner evaluates them, structures the deal, models the
revenue impact, and tracks the relationship through quarterly reviews.

### Principle 9: Composable Architecture

Each component — discovery, pipeline, revenue, market, competitive, negotiation,
growth, channel, due diligence, analytics — works independently or as part of an
orchestrated workflow. Call one method or chain them together. The agent doesn't
force a specific workflow.

### Principle 10: Auditability

All actions are logged with timestamps and context via `_event_log`. The event log
provides a complete audit trail for compliance and retrospective analysis. Every
significant state change is recorded.

---

## 3. Detailed Capabilities

### 3.1 Partner Discovery Engine

**Purpose**: Find, score, and rank potential partners matching specific criteria.

**How it works**:
1. Parse criteria (industry, revenue, capabilities, geography, synergy focus)
2. Generate candidates from market data (simulated — integrate with real sources)
3. Score each candidate across 5 dimensions with explicit weights
4. Rank by composite score and assign recommendation (PURSUE / EVALUATE / MONITOR)

**Method**: `find_partners(criteria, market)`

```python
candidates = agent.find_partners(
    criteria={
        "industry": "Cloud Infrastructure",     # Target industry
        "min_revenue": 100_000,                 # Minimum partner revenue
        "capabilities": ["hosting", "security"], # Required capabilities
        "synergy_focus": "revenue",             # Revenue vs tech synergy
        "max_results": 10,                      # Max candidates to return
    },
    market=MarketSegment.ENTERPRISE,           # Target market
)
# Returns: list of dicts with scores and recommendations
```

**Scoring Weights**:
| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Synergy | 30% | Complementary capabilities and market access |
| Strategic Alignment | 25% | Shared vision, goals, and roadmap overlap |
| Cultural Fit | 15% | Working style, values, communication compatibility |
| Market Reach | 15% | Access to target customer segments and geographies |
| Capability Match | 15% | Technical and operational capability overlap |

**Recommendation Thresholds**:
- composite >= 0.70 → PURSUE (high-priority engagement)
- composite >= 0.50 → EVALUATE (worth deeper assessment)
- composite < 0.50 → MONITOR (track for future opportunities)

---

### 3.2 Partner Evaluation Scorecard

**Purpose**: Produce a multi-dimensional assessment of a specific partner candidate.

**Method**: `evaluate_partner(partner_data)`

```python
scorecard = agent.evaluate_partner({
    "name": "Partner Corp",
    "financial_health": 0.85,   # Revenue stability, growth, runway
    "market_reach": 0.72,       # Customer base, geo coverage
    "tech_capability": 0.90,    # Stack maturity, innovation capacity
    "cultural_fit": 0.78,       # Values alignment, working style
    "innovation": 0.82,         # R&D investment, patent activity
    "risk": 0.15,               # Risk level (0=low, 1=high)
})
# Returns: PartnerScorecard with overall_score and recommendation()
```

**Scorecard Dimensions**:
| Dimension | Weight | Ideal Score |
|-----------|--------|------------|
| Financial Stability | 20% | > 0.8 |
| Market Reach | 18% | > 0.7 |
| Technical Capability | 22% | > 0.8 |
| Cultural Alignment | 15% | > 0.7 |
| Innovation Potential | 15% | > 0.7 |
| Risk Level (inverse) | 10% | < 0.2 |

**Recommendation Logic**:
- overall_score >= 0.8 → PURSUE AGGRESSIVELY
- overall_score >= 0.6 → PURSUE WITH MODERATE INVESTMENT
- overall_score >= 0.4 → CONDITIONAL PURSUIT — ADDRESS GAPS
- overall_score < 0.4 → DO NOT PURSUE

---

### 3.3 Deal Pipeline Manager

**Purpose**: Structure deals, track stage progression, and generate weighted forecasts.

**Method**: `structure_deal(partner, type, value)` and `manage_pipeline(stage_filter)`

```python
# Structure a new deal
deal = agent.structure_deal(
    partner_name="TechVentures Inc.",
    partnership_type=PartnershipType.TECHNOLOGY,
    deal_value=250_000,
)
# Returns: Partnership with auto-generated ID, timestamps, default scores

# Analyze entire pipeline
analysis = agent.manage_pipeline()
# Returns: total_deals, weighted_value, health, per-stage breakdown

# Filter to specific stage
negotiating = agent.manage_pipeline(stage_filter=DealStage.NEGOTIATION)
```

**Stage Progression Weights**:
| Stage | Weight | Probability of Close |
|-------|--------|---------------------|
| Identification | 5% | Very early, low confidence |
| Qualification | 15% | BANT qualified |
| Proposal | 35% | Formal proposal submitted |
| Negotiation | 60% | Active term discussion |
| Closing | 85% | Contract in final review |
| Post-Close | 100% | Agreement signed |
| Maintenance | 100% | Active relationship |
| Expansion | 100% | Upsell/cross-sell active |

**Pipeline Health Assessment**:
```
inputs: avg_deal_age_days, win_rate, stuck_deal_ratio

if win_rate > 30% AND avg_age < 90d:   → HEALTHY
if avg_age > 120d:                       → STAGNANT
if win_rate < 10% AND avg_age > 150d:   → DECLINING
otherwise:                               → AT_RISK
```

---

### 3.4 Revenue Modeling Framework

**Purpose**: Build multi-scenario revenue projections with financial metrics.

**Method**: `model_revenue(scenario, timeline, mrr, assumptions)`

```python
forecast = agent.model_revenue(
    scenario="base",            # conservative, base, or aggressive
    timeline_months=36,         # Projection horizon
    initial_mrr=75_000,         # Starting MRR
    assumptions={                # Optional overrides
        "growth_rate": 0.06,
        "churn_rate": 0.02,
        "expansion_rate": 0.01,
    },
)
print(f"NPV: ${forecast.npv():,.0f}")        # Net Present Value
print(f"IRR: {forecast.irr():.1%}")          # Internal Rate of Return
print(f"Payback: {forecast.payback_months(500_000)} months")
```

**Monthly Revenue Formula**:
```
mrr[t] = mrr[t-1] × (1 + growth - churn + expansion) × seasonal[t%12]
```

**NPV Formula**:
```
NPV = Σ (mrr[t] / (1 + discount_rate)^(t/12))   for t = 0..months
```

**Scenario Presets**:
| Scenario | Growth | Churn | Expansion | Discount |
|----------|--------|-------|-----------|----------|
| Conservative | 3% | 3.0% | 0.5% | 12% |
| Base | 6% | 2.0% | 1.0% | 10% |
| Aggressive | 10% | 1.5% | 2.0% | 8% |

**Seasonal Factors**: `[0.85, 0.90, 1.00, 1.05, 1.10, 1.15, 1.10, 1.05, 1.00, 0.95, 0.90, 0.85]`

---

### 3.5 Market Intelligence Hub

**Purpose**: Analyze market attractiveness with TAM/SAM/SOM, SWOT, and Porter's Five Forces.

**Method**: `analyze_market(opportunity)`

```python
market = agent.analyze_market({
    "industry": "Enterprise AI Platform",
    "market_size": 45_000_000_000,      # TAM in USD
    "cagr": 0.22,                        # Compound annual growth rate
    "trends": ["AI adoption", "Data sovereignty"],
    "rivalry": 0.65,                     # Porter's force scores (0-1)
    "new_entrants": 0.55,
    "substitutes": 0.4,
    "supplier_power": 0.3,
    "buyer_power": 0.6,
    "strengths": ["Strong brand"],
    "weaknesses": ["Limited reach"],
    "opportunities": ["SMB gap"],
    "threats": ["Big tech entry"],
    "regulations": ["GDPR", "SOC 2"],
})
# Returns: MarketAnalysis with attractiveness_score()
```

**Attractiveness Formula**:
```
score = (trend_score × 0.25) + (cagr_score × 0.35) + (force_score × 0.25) - reg_penalty
```

---

### 3.6 Competitive Analysis Module

**Purpose**: Map competitor positioning, assess threats, and identify strategic implications.

**Method**: `evaluate_competitive_landscape(industry)`

```python
comp = agent.evaluate_competitive_landscape("Enterprise AI")
# Returns: positioning_map, strategic_implications, moat_assessment

for c in comp["positioning_map"]:
    print(f"{c['name']}: {c['positioning']} — {c['threat']}")
```

**Threat Classification**:
| Score | Classification |
|-------|---------------|
| >= 0.8 | CRITICAL |
| >= 0.6 | HIGH |
| >= 0.3 | MODERATE |
| < 0.3 | LOW |

**Positioning Categories**: LEADER, CHALLENGER, NICHE, EMERGING

---

### 3.7 Negotiation Strategy Engine

**Purpose**: Calculate ZOPA, anchor points, and concession strategies.

**Method**: `negotiate_deal(value, style, walk_away, target)`

```python
strategy = agent.negotiate_deal(
    deal_value=250_000,
    style=NegotiationStyle.COLLABORATIVE,
    walk_away=150_000,     # Default: 60% of deal value
    target=225_000,        # Default: 90% of deal value
)
print(f"ZOPA: ${strategy.zone_of_possible_agreement}")
print(f"Acceptance at $200K: {strategy.probability_of_acceptance(200_000):.0%}")
```

**ZOPA Calculation**:
```
ZOPA = [walk_away_point, deal_value × 1.05]
```

**Acceptance Probability**:
```
if offer in ZOPA:
    prob = 1 - |offer - midpoint| / (zopa_width / 2) × 0.3
else:
    prob = 0.05
```

**Style Presets**:
| Style | Concessions | Leverage |
|-------|------------|----------|
| Competitive | Minimal (5% max) | Market position, brand |
| Collaborative | Flexible (pricing, SLA, co-marketing) | Mutual benefit, shared customers |
| Compromise | Balanced (mid-range pricing) | Shared pressure |
| Accommodating | Generous | Relationship value |
| Avoiding | Deferred | Time sensitivity |

---

### 3.8 Growth Strategy Generator

**Purpose**: Generate Ansoff-matrix-based growth strategies.

**Method**: `develop_growth_strategy(company_profile)`

```python
plan = agent.develop_growth_strategy({
    "current_revenue": 3_000_000,
    "products": 1,
    "markets": 1,
    "risk_tolerance": "moderate",  # affects budget allocation
})
# Auto-selects strategy based on products × markets matrix
# Returns: objectives, initiatives, budget, KPIs, risks, milestones
```

**Strategy Selection Logic**:
| Products | Markets | Strategy |
|----------|---------|----------|
| <= 1 | <= 1 | MARKET_PENETRATION |
| <= 1 | > 1 | MARKET_DEVELOPMENT |
| > 1 | <= 1 | PRODUCT_DEVELOPMENT |
| > 1 | > 1 | DIVERSIFICATION |

**Budget Calculation**:
```
budget = current_revenue × (0.15 if aggressive else 0.10)
```

---

### 3.9 Value Proposition Canvas

**Purpose**: Build customer-segment-specific value propositions.

**Method**: `create_value_proposition(target_market, product_name)`

```python
vp = agent.create_value_proposition(
    target_market=MarketSegment.ENTERPRISE,
    product_name="CloudScale Platform",
)
print(f"Headline: {vp.headline}")
print(f"Fit score: {vp.score:.3f}")
print(f"Jobs: {len(vp.customer_jobs)}")
print(f"Pains: {len(vp.pains)}")
print(f"Gains: {len(vp.gains)}")
```

**Fit Score Formula**:
```
fit = (pain_coverage + gain_coverage) / 2
where:
  pain_coverage = len(pain_relievers) / max(len(pains), 1)
  gain_coverage = len(gain_creators) / max(len(gains), 1)
```

---

### 3.10 Sales Forecasting

**Purpose**: Generate multi-scenario sales forecasts with seasonal adjustments.

**Method**: `forecast_sales(product_line, period_months, base_mrr)`

```python
forecast = agent.forecast_sales(
    product_line="Core Platform",
    period_months=12,
    base_mrr=120_000,
)
# Generates: pessimistic (0.6x), base (1.0x), optimistic (1.5x)
print(f"Expected: ${forecast.expected_value():,.0f}")
```

---

### 3.11 Channel Partner Strategy

**Purpose**: Design optimal channel mix for target segments.

**Method**: `design_channel_strategy(product, market)`

```python
channel = agent.design_channel_strategy(
    product="CloudScale Platform",
    target_market=MarketSegment.ENTERPRISE,
)
print(f"Channels: {', '.join(channel.channels)}")
print(f"Est. deals: {channel.estimated_deals()}")
print(f"CPA: ${channel.cost_per_acquisition():,.0f}")
```

**Formulas**:
```
estimated_deals = reach × conversion_rate
CPA = investment / estimated_deals
```

---

### 3.12 Due Diligence Tracker

**Purpose**: Execute comprehensive due diligence checklists.

**Method**: `conduct_due_diligence(target)`

```python
report = agent.conduct_due_diligence({
    "name": "Target Corp",
    "type": "acquisition",
})
# Returns: 6 workstreams, 30+ items, risk assessment, recommendation
```

**Workstreams**: Financial, Legal, Technical, Market, Team, Operational

**Decision Logic**:
```
if high_risk_areas > 0:  → "PROCEED WITH CAUTION"
else:                    → "PROCEED"
```

---

### 3.13 Outreach Campaign Design

**Purpose**: Design outreach campaigns with projected funnel metrics.

**Method**: `create_outreach_campaign(name, channel, audience_size)`

```python
campaign = agent.create_outreach_campaign(
    name="Q1 Partner Outreach",
    channel="linkedin",       # email, linkedin, events
    audience_size=300,
)
print(f"Response rate: {campaign.response_rate():.1%}")
print(f"Meeting rate: {campaign.meeting_rate():.1%}")
print(f"Deal rate: {campaign.deal_rate():.1%}")
print(f"Cost per meeting: ${campaign.cost_per_meeting():,.0f}")
```

**Channel Benchmarks**:
| Channel | Response Rate | Meeting Rate | Deal Rate | Cost/Contact |
|---------|-------------|-------------|-----------|-------------|
| Email | 8% | 15% | 3% | $5 |
| LinkedIn | 12% | 20% | 5% | $15 |
| Events | 25% | 40% | 8% | $100 |

---

### 3.14 Conversion Funnel Analysis

**Purpose**: Analyze conversion funnels and identify bottlenecks.

**Method**: `analyze_conversion_funnel(funnel_data)`

```python
funnel = agent.analyze_conversion_funnel({
    "stages": ["Prospects", "Contacted", "Meeting", "Proposal", "Closed"],
    "counts": [1000, 800, 160, 45, 12],
})
print(f"Overall: {funnel.overall_conversion():.1%}")
print(f"Bottleneck: {funnel.bottleneck_stage()}")
# bottleneck_stage() returns the stage with lowest conversion rate
```

---

### 3.15 Quarterly Performance Review

**Purpose**: Generate BD performance dashboards with metric tracking.

**Method**: `generate_quarterly_review(quarter, year)`

```python
review = agent.generate_quarterly_review("Q1", 2026)
summary = review.summary()
# Returns: quarter, health, revenue, pipeline, deals, metric statuses
```

**Health Assessment**:
```
on_track_ratio = metrics_on_track / total_metrics
if ratio >= 0.8:  → STRONG
if ratio >= 0.5:  → MODERATE
else:             → WEAK
```

**Metric Status**:
```
attainment = value / target
if attainment >= 1.0:  → EXCEEDED
if attainment >= 0.9:  → ON_TRACK
if attainment >= 0.7:  → AT_RISK
else:                  → BEHIND
```

---

## 4. Operational Guidelines

### Method Selection Guide

| Situation | Method(s) | Expected Output |
|-----------|-----------|-----------------|
| Need new partners | `find_partners()` → `evaluate_partner()` | Ranked candidates + scorecards |
| Starting a new deal | `structure_deal()` | Partnership object with ID |
| Checking pipeline health | `manage_pipeline()` | Health status + weighted forecast |
| Modeling revenue | `model_revenue()` × 3 scenarios | NPV, IRR, payback |
| Entering new market | `analyze_market()` → `plan_market_entry()` | Market analysis + entry plan |
| Competitive pressure | `evaluate_competitive_landscape()` | Positioning map + implications |
| Preparing negotiation | `negotiate_deal()` | ZOPA + concessions + leverage |
| Building sales materials | `create_value_proposition()` | Canvas with fit score |
| Forecasting sales | `forecast_sales()` | 3-scenario forecast |
| Designing channels | `design_channel_strategy()` | Channel mix + CPA |
| Evaluating a target | `conduct_due_diligence()` | 30-item checklist + risk report |
| Planning outreach | `create_outreach_campaign()` | Funnel projections |
| Reviewing performance | `generate_quarterly_review()` | 6-metric dashboard |
| Optimizing conversion | `analyze_conversion_funnel()` | Rates + bottleneck |

### Workflow Patterns

**Pattern 1: Partner Onboarding Pipeline**
```
find_partners() → evaluate_partner() → structure_deal() → conduct_due_diligence()
```

**Pattern 2: Market Expansion**
```
analyze_market() → develop_growth_strategy() → plan_market_entry()
```

**Pattern 3: Revenue Planning**
```
model_revenue() × 3 scenarios → forecast_sales() → generate_quarterly_review()
```

**Pattern 4: Competitive Response**
```
evaluate_competitive_landscape() → create_value_proposition() → negotiate_deal()
```

**Pattern 5: Channel Launch**
```
design_channel_strategy() → create_outreach_campaign() → analyze_conversion_funnel()
```

---

## 5. Method Signatures & Usage Patterns

### Constructor

```python
BusinessDevelopmentAgent(
    company_name: str = "Acme Corp",
    industry: str = "SaaS"
)
```

### Partner Methods

```python
find_partners(
    criteria: dict[str, Any],      # industry, min_revenue, capabilities, etc.
    market: MarketSegment = MarketSegment.ENTERPRISE
) -> list[dict[str, Any]]

evaluate_partner(
    partner_data: dict[str, Any]   # name, financial_health, market_reach, etc.
) -> PartnerScorecard
```

### Pipeline Methods

```python
structure_deal(
    partner_name: str,
    partnership_type: PartnershipType,
    deal_value: float,
    **kwargs: Any                  # end_date, contact_person, notes, tags
) -> Partnership

manage_pipeline(
    stage_filter: Optional[DealStage] = None
) -> dict[str, Any]
```

### Revenue Methods

```python
model_revenue(
    scenario: str = "base",        # conservative, base, aggressive
    timeline_months: int = 36,
    initial_mrr: float = 50_000,
    assumptions: Optional[dict[str, Any]] = None
) -> RevenueForecast
```

### Market Methods

```python
analyze_market(
    opportunity: dict[str, Any]    # industry, market_size, cagr, trends, etc.
) -> MarketAnalysis

plan_market_entry(
    target_market: dict[str, Any]  # name, segment, timeline, budget
) -> dict[str, Any]
```

### Strategy Methods

```python
develop_growth_strategy(
    company_profile: Optional[dict[str, Any]] = None
) -> GrowthPlan

negotiate_deal(
    deal_value: float,
    style: NegotiationStyle = NegotiationStyle.COLLABORATIVE,
    walk_away: Optional[float] = None,
    target: Optional[float] = None
) -> NegotiationStrategy

create_value_proposition(
    target_market: MarketSegment = MarketSegment.ENTERPRISE,
    product_name: str = "Platform"
) -> ValueProposition
```

### Analytics Methods

```python
forecast_sales(
    product_line: str = "Core Platform",
    period_months: int = 12,
    base_mrr: float = 100_000
) -> SalesForecast

evaluate_competitive_landscape(
    industry: Optional[str] = None
) -> dict[str, Any]

design_channel_strategy(
    product: str = "Core Platform",
    target_market: MarketSegment = MarketSegment.ENTERPRISE
) -> ChannelStrategy

conduct_due_diligence(
    target: dict[str, Any]         # name, type, risk overrides
) -> dict[str, Any]

generate_quarterly_review(
    quarter: str = "Q1",
    year: int = 2026
) -> QuarterlyReview

create_outreach_campaign(
    name: str = "Outreach Campaign",
    channel: str = "email",
    audience_size: int = 500
) -> OutreachCampaign

analyze_conversion_funnel(
    funnel_data: Optional[dict[str, list[int]]] = None
) -> ConversionFunnel
```

---

## 6. Data Models Reference

### Partnership

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| partner_id | str | uuid[:8] | Unique identifier |
| name | str | "" | Partner name |
| partnership_type | PartnershipType | STRATEGIC | Type of partnership |
| stage | DealStage | IDENTIFICATION | Current pipeline stage |
| market_segment | MarketSegment | ENTERPRISE | Target market |
| geography | GeographyScope | NATIONAL | Geographic scope |
| annual_value | float | 0.0 | Estimated annual value |
| start_date | datetime | None | Partnership start |
| end_date | datetime | None | Partnership end |
| health_score | float | 0.5 | Relationship health [0-1] |
| synergy_score | float | 0.0 | Synergy assessment [0-1] |
| cultural_fit | float | 0.0 | Cultural alignment [0-1] |
| strategic_alignment | float | 0.0 | Strategic fit [0-1] |

**Computed Methods**: `composite_score()`, `is_high_value()`, `remaining_days()`

### RevenueForecast

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| model_id | str | uuid[:8] | Unique identifier |
| name | str | "" | Scenario name |
| monthly_revenue | list[float] | [] | Monthly projections |
| assumptions | dict | {} | Model parameters |
| discount_rate | float | 0.10 | For NPV calculation |
| projection_months | int | 36 | Forecast horizon |

**Computed Methods**: `npv()`, `irr()`, `payback_months()`

### MarketAnalysis

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| industry | str | "" | Industry name |
| market_size | float | 0.0 | TAM in USD |
| cagr | float | 0.0 | Compound annual growth rate |
| key_trends | list[str] | [] | Market trends |
| swot | dict | {} | SWOT analysis |
| porter_forces | dict | {} | Five Forces scores |
| regulatory_factors | list[str] | [] | Regulatory considerations |

**Computed Methods**: `industry_attractiveness()`

---

## 7. Checklists

### Partner Evaluation Checklist

- [ ] Financial health verified (revenue, growth, runway, liabilities)
- [ ] Market reach assessed (customer base, geo coverage, channel access)
- [ ] Technical capability evaluated (stack, innovation, scalability)
- [ ] Cultural alignment confirmed (values, working style, communication)
- [ ] Risk level categorized (financial, legal, operational, market)
- [ ] Composite score calculated with published weights
- [ ] Recommendation generated (PURSUE / EVALUATE / MONITOR)
- [ ] Scorecard documented and stakeholder-reviewed

### Due Diligence Checklist

- [ ] Financial review: 3yr statements, revenue composition, burn rate, liabilities
- [ ] Legal review: Corp structure, contracts, IP ownership, litigation, compliance
- [ ] Technical review: Stack assessment, security audit, scalability, tech debt
- [ ] Market review: Position, NPS, roadmap alignment, GTM capability, brand
- [ ] Team review: Key person dependency, org structure, culture, retention
- [ ] Operational review: BCP, vendor dependencies, QA, support, SLAs
- [ ] High-risk areas identified with mitigation plans
- [ ] Decision recommendation documented

### Deal Closing Checklist

- [ ] Partner evaluation scorecard complete (>= 0.6 composite)
- [ ] Pipeline stage advanced to CLOSING with gate criteria met
- [ ] Terms sheet reviewed and agreed by both parties
- [ ] Legal and compliance review cleared
- [ ] Revenue share / pricing structure confirmed
- [ ] Exclusivity terms defined (if applicable)
- [ ] Termination clause documented
- [ ] Renewal terms specified
- [ ] Compliance requirements listed
- [ ] Agreement summary generated
- [ ] Post-close milestones and KPIs defined
- [ ] Onboarding plan created

### Market Entry Checklist

- [ ] TAM/SAM/SOM analysis complete
- [ ] SWOT analysis documented
- [ ] Porter's Five Forces assessed
- [ ] Competitive landscape mapped
- [ ] Regulatory requirements identified
- [ ] Entry mode selected (direct, partner, acquisition)
- [ ] Budget allocated across phases
- [ ] Timeline with milestones defined
- [ ] Risk mitigation plan created
- [ ] Success metrics established

---

## 8. Troubleshooting Guide

### Issue: Partner candidates all score below threshold

**Symptoms**: `find_partners()` returns empty PURSUE list

**Root Causes**:
- Criteria too restrictive (high `min_revenue`, narrow capabilities)
- Market segment too specific for available candidates
- Synergy focus mismatch

**Solutions**:
1. Lower `min_revenue` threshold (try 50% of current value)
2. Broaden `capabilities` list (add 2-3 related capabilities)
3. Increase `max_results` to get more candidates for selection
4. Try different `synergy_focus` values (revenue vs technology)
5. Expand to adjacent market segments

### Issue: Pipeline always shows DECLINING health

**Symptoms**: `manage_pipeline()` returns `PipelineHealth.DECLINING`

**Root Causes**:
- All deals stuck in early stages (no progression)
- Deals have very old `start_date` values
- Win rate too low (too few deals reaching POST_CLOSE)

**Solutions**:
1. Move deals forward through stage gates (update `deal.stage`)
2. Archive stale deals (remove from active pipeline)
3. Run `negotiate_deal()` to unblock stalled negotiations
4. Add new deals to improve win rate statistics
5. Review stage gate criteria — are they too strict?

### Issue: Revenue model NPV is negative

**Symptoms**: `model_revenue().npv() < 0`

**Root Causes**:
- Initial MRR too low relative to discount rate
- Churn rate exceeding growth rate
- Short projection horizon
- High discount rate

**Solutions**:
1. Increase `initial_mrr` parameter
2. Increase `growth_rate` in assumptions
3. Decrease `churn_rate` in assumptions
4. Extend `timeline_months` to 36+
5. Lower `discount_rate` (or use aggressive scenario)
6. Add `expansion_rate` to assumptions

### Issue: Negotiation ZOPA has zero width

**Symptoms**: `negotiate_deal().zopa_width() == 0`

**Root Causes**:
- Walk-away point equals or exceeds target point
- Invalid input values (walk_away > target)

**Solutions**:
1. Ensure walk_away < target (default: 60% vs 90% of deal value)
2. Use default parameters (auto-calculated)
3. Set explicit walk_away and target with proper spacing

### Issue: Quarterly review shows WEAK health

**Symptoms**: `generate_quarterly_review().overall_health() == "WEAK"`

**Root Causes**:
- Random seed producing below-target metrics (expected behavior in demo)
- Targets too aggressive for generated values

**Solutions**:
1. This is expected — the demo generates randomized metrics
2. For production use, pass real data through `BusinessMetric` objects
3. Adjust targets to match realistic capacity

### Issue: Value proposition fit score is low

**Symptoms**: `create_value_proposition().score < 0.5`

**Root Causes**:
- Fewer pain relievers than pains (low pain coverage)
- Fewer gain creators than gains (low gain coverage)

**Solutions**:
1. Add more pain relievers to address each identified pain
2. Add more gain creators to support each identified gain
3. Reduce the number of pains/gains to focus on core ones
4. Use the segment-specific profiles (ENTERPRISE vs SMB)

### Issue: Conversion funnel bottleneck is unexpected

**Symptoms**: `analyze_conversion_funnel().bottleneck_stage()` shows unexpected stage

**Root Causes**:
- Data quality issues in stage counts
- Normal — the bottleneck is the stage with lowest conversion rate

**Solutions**:
1. Verify stage counts are accurate
2. Focus improvement efforts on the bottleneck stage
3. Re-run after making changes to verify improvement

---

*GROK.md v2.0.0 — Business Development Agent Identity Document*

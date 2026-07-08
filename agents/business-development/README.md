# Business Development Agent

A comprehensive B2B business development automation engine — partner discovery, deal pipeline management, revenue modeling, market intelligence, competitive analysis, negotiation strategy, growth planning, channel partner design, due diligence tracking, and performance analytics.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Usage Examples](#usage-examples)
6. [API Reference](#api-reference)
7. [Configuration](#configuration)
8. [Walkthroughs](#walkthroughs)
9. [Best Practices](#best-practices)
10. [Troubleshooting & FAQ](#troubleshooting--faq)
11. [Contributing](#contributing)
12. [License](#license)

---

## Overview

### What It Does

The Business Development Agent automates the full B2B business development lifecycle, from initial partner discovery through post-close relationship management. It replaces manual, error-prone spreadsheet workflows with structured, auditable, data-driven decision frameworks.

| Phase | Capability | Method | Key Output |
|-------|-----------|--------|------------|
| **Discover** | Find and score potential partners | `find_partners()` | Ranked candidate list with scores |
| **Evaluate** | Multi-dimensional partner assessment | `evaluate_partner()` | Scorecard with recommendation |
| **Structure** | Create deals with term sheets | `structure_deal()` | Partnership object with metadata |
| **Manage** | Track pipeline with weighted forecasting | `manage_pipeline()` | Health status + weighted value |
| **Model** | Revenue projections with NPV/IRR | `model_revenue()` | Financial metrics by scenario |
| **Analyze** | Market sizing (TAM/SAM/SOM) | `analyze_market()` | Attractiveness score + SWOT |
| **Strategize** | Ansoff matrix growth planning | `develop_growth_strategy()` | Strategy + objectives + budget |
| **Negotiate** | ZOPA calculation and style selection | `negotiate_deal()` | ZOPA + concessions + leverage |
| **Position** | Value proposition canvas | `create_value_proposition()` | Jobs/pains/gains + fit score |
| **Forecast** | Multi-scenario sales forecasting | `forecast_sales()` | 3-scenario projections |
| **Compete** | Landscape analysis and threat mapping | `evaluate_competitive_landscape()` | Positioning map + implications |
| **Enter** | Market entry strategy | `plan_market_entry()` | Phased plan with budget |
| **Channel** | Channel partner program design | `design_channel_strategy()` | Channel mix + CPA projection |
| **Diligence** | Due diligence checklist execution | `conduct_due_diligence()` | 30-item checklist + risk report |
| **Review** | Quarterly performance dashboard | `generate_quarterly_review()` | 6-metric dashboard |
| **Outreach** | Campaign design with funnel metrics | `create_outreach_campaign()` | Funnel projections + CPA |
| **Funnel** | Conversion analysis and bottleneck ID | `analyze_conversion_funnel()` | Rates + bottleneck stage |

### Key Features

- **16 enums** covering partnership types, deal stages, market segments, revenue models, competitor positioning, growth strategies, pipeline health, negotiation styles, geography scope, and value proposition types
- **20 dataclasses** with computed methods (composite scores, fit scores, attainment, ZOPA width, etc.)
- **17 agent methods** with full type hints, logging, and error handling
- **Financial modeling** including NPV, IRR, and payback period calculations
- **Scenario analysis** with conservative/base/optimistic projections
- **Zero dependencies** — runs on Python 3.11+ stdlib only
- **Comprehensive demo** with a realistic B2B SaaS scenario covering all capabilities

### Who It's For

| Role | Use Cases |
|------|-----------|
| VP Business Development | Pipeline health monitoring, partner scorecards, quarterly reviews |
| Head of Partnerships | Partner discovery, evaluation, deal structuring |
| Revenue Operations | Revenue modeling, sales forecasting, funnel analysis |
| Product Marketing | Value proposition canvas, competitive analysis |
| Strategy Lead | Market analysis, growth strategy, market entry planning |
| Deal Desk | Negotiation strategy, due diligence, contract structuring |

---

## Architecture

```
+-----------------------------------------------------------------------+
|                    BusinessDevelopmentAgent                            |
|  company_name · industry · _event_log                                 |
+-----------------------------------------------------------------------+
|                                                                       |
|  +------------------+  +------------------+  +------------------+     |
|  | Partner Discovery|  | Deal Pipeline    |  | Revenue Modeling |     |
|  | find_partners()  |  | structure_deal() |  | model_revenue()  |     |
|  | evaluate_partner |  | manage_pipeline()|  |                  |     |
|  +------------------+  +------------------+  +------------------+     |
|                                                                       |
|  +------------------+  +------------------+  +------------------+     |
|  | Market Intel     |  | Competitive      |  | Negotiation      |     |
|  | analyze_market() |  | evaluate_        |  | negotiate_deal() |     |
|  |                  |  |   competitive_   |  |                  |     |
|  |                  |  |   landscape()    |  |                  |     |
|  +------------------+  +------------------+  +------------------+     |
|                                                                       |
|  +------------------+  +------------------+  +------------------+     |
|  | Growth Strategy  |  | Channel Partner  |  | Due Diligence    |     |
|  | develop_growth_  |  | design_channel_  |  | conduct_due_     |     |
|  | strategy()       |  | strategy()       |  | diligence()      |     |
|  +------------------+  +------------------+  +------------------+     |
|                                                                       |
|  +------------------+  +------------------+  +------------------+     |
|  | Sales Forecast   |  | Outreach &       |  | Performance      |     |
|  | forecast_sales() |  | Funnel           |  | Quarterly Review |     |
|  |                  |  | create_outreach_ |  | generate_        |     |
|  |                  |  | campaign()       |  | quarterly_review |     |
|  +------------------+  +------------------+  +------------------+     |
+-----------------------------------------------------------------------+
```

**Data Flow:**

```
Discovery ──→ Evaluation ──→ Deal Structure ──→ Due Diligence ──→ Negotiation ──→ Closing
                                                                         │
Market Intel ──→ Growth Strategy ──→ Market Entry                      │
                                        │                              │
Competitive ──→ Value Proposition ──→ Channel Strategy ──→ Outreach   │
                                                                   │
Sales Forecast ──→ Revenue Model ──→ Quarterly Review ◄───────────┘
```

For the full architecture document, see [ARCHITECTURE.md](./ARCHITECTURE.md).

---

## Installation

### Prerequisites

- Python 3.11 or later
- No external dependencies (stdlib only)

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd Awesome-Grok-Skills/agents/business-development

# Verify Python version
python --version  # Should be 3.11+

# Run the full demo
python agent.py
```

### Verify Installation

```bash
python -c "
from agent import BusinessDevelopmentAgent, PartnershipType, DealStage
agent = BusinessDevelopmentAgent('TestCo', 'SaaS')
deal = agent.structure_deal('TestPartner', PartnershipType.STRATEGIC, 100000)
print(f'Deal created: {deal.partner_id} (\${deal.annual_value:,.0f})')
print('Installation successful.')
"
```

### Virtual Environment (Recommended)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

python agent.py
```

---

## Quick Start

```python
from agent import BusinessDevelopmentAgent, MarketSegment, PartnershipType

# Initialize the agent
agent = BusinessDevelopmentAgent(
    company_name="YourCompany",
    industry="Enterprise SaaS"
)

# 1. Find partners
candidates = agent.find_partners(
    criteria={"industry": "Cloud Infrastructure", "min_revenue": 500_000},
    market=MarketSegment.ENTERPRISE,
)
print(f"Found {len(candidates)} candidates")
# Example output: Found 7 candidates

# 2. Structure a deal with the top candidate
deal = agent.structure_deal(
    partner_name=candidates[0]["name"],
    partnership_type=PartnershipType.TECHNOLOGY,
    deal_value=200_000,
)
print(f"Deal {deal.partner_id}: ${deal.annual_value:,.0f}")

# 3. Check pipeline health
analysis = agent.manage_pipeline()
print(f"Pipeline: ${analysis['weighted_value']:,.0f} weighted value")
print(f"Health: {analysis['health']}")

# 4. Model revenue impact
rev = agent.model_revenue("base", timeline_months=24, initial_mrr=100_000)
print(f"NPV: ${rev.npv():,.0f} | IRR: {rev.irr():.1%}")

# 5. Generate quarterly review
review = agent.generate_quarterly_review("Q1", 2026)
print(f"Health: {review.overall_health()}")
print(f"Revenue: ${review.revenue_generated:,.0f}")
```

---

## Usage Examples

### Example 1: End-to-End Partner Onboarding

```python
from agent import BusinessDevelopmentAgent, PartnershipType, MarketSegment

agent = BusinessDevelopmentAgent("Acme Corp", "AI Platform")

# Step 1: Discover candidates
candidates = agent.find_partners(
    criteria={
        "industry": "Data Analytics",
        "min_revenue": 200_000,
        "capabilities": ["ML pipelines", "data visualization"],
    },
    market=MarketSegment.ENTERPRISE,
)
print(f"Discovered {len(candidates)} candidates")

# Step 2: Evaluate the top candidate
scorecard = agent.evaluate_partner({
    "name": candidates[0]["name"],
    "financial_health": 0.80,
    "market_reach": 0.70,
    "tech_capability": 0.85,
    "cultural_fit": 0.75,
    "innovation": 0.80,
    "risk": 0.20,
})
print(f"Score: {scorecard.overall_score:.3f} -> {scorecard.recommendation()}")

# Step 3: Structure the deal
if scorecard.overall_score >= 0.6:
    deal = agent.structure_deal(
        partner_name=candidates[0]["name"],
        partnership_type=PartnershipType.TECHNOLOGY,
        deal_value=180_000,
    )

    # Step 4: Negotiate
    neg = agent.negotiate_deal(180_000)
    print(f"ZOPA: ${neg.zone_of_possible_agreement[0]:,.0f} - "
          f"${neg.zone_of_possible_agreement[1]:,.0f}")

    # Step 5: Due diligence
    dd = agent.conduct_due_diligence({
        "name": candidates[0]["name"],
        "type": "strategic_partner",
    })
    print(f"DD: {dd['recommendation']} ({dd['total_items']} items)")

    # Step 6: Pipeline check
    analysis = agent.manage_pipeline()
    print(f"Pipeline: {analysis['total_deals']} deals, "
          f"${analysis['weighted_value']:,.0f} weighted")
```

### Example 2: Market Entry Planning

```python
from agent import BusinessDevelopmentAgent, MarketSegment

agent = BusinessDevelopmentAgent("SaaS Co", "Cloud Platform")

# Analyze target market
market = agent.analyze_market({
    "industry": "Enterprise AI Platform",
    "market_size": 45_000_000_000,
    "cagr": 0.22,
    "trends": ["AI adoption", "Data sovereignty", "Remote work"],
    "rivalry": 0.65,
    "new_entrants": 0.55,
})
print(f"Attractiveness: {market.industry_attractiveness():.3f}")
print(f"Strengths: {market.swot['strengths']}")
print(f"Threats: {market.swot['threats']}")

# Develop growth strategy
plan = agent.develop_growth_strategy({
    "current_revenue": 5_000_000,
    "products": 2,
    "markets": 1,
    "risk_tolerance": "aggressive",
})
print(f"Strategy: {plan.strategy.value}")
print(f"Budget: ${plan.budget:,.0f}")
for obj in plan.objectives:
    print(f"  -> {obj}")

# Plan market entry
entry = agent.plan_market_entry({
    "name": "EMEA",
    "segment": "enterprise",
    "timeline_months": 12,
    "budget": 1_000_000,
})
for phase in entry["phases"]:
    print(f"  {phase['phase']}: ${phase['budget_allocation']:,.0f}")
print(f"Risk mitigation: {len(entry['risk_mitigation'])} strategies")
```

### Example 3: Revenue Modeling & Forecasting

```python
from agent import BusinessDevelopmentAgent

agent = BusinessDevelopmentAgent("FinTech Inc", "Payments")

# Model revenue across scenarios
print("Revenue Projections (36 months):")
print("-" * 55)
for scenario in ["conservative", "base", "aggressive"]:
    rev = agent.model_revenue(
        scenario=scenario,
        timeline_months=36,
        initial_mrr=100_000,
    )
    print(
        f"  {scenario:>14s}: NPV=${rev.npv():>12,.0f}  "
        f"IRR={rev.irr():.1%}  "
        f"Payback={rev.payback_months(1_000_000) or 'N/A'}mo"
    )

# Sales forecast by product line
print("\nSales Forecast (12 months):")
forecast = agent.forecast_sales(
    product_line="Enterprise Suite",
    period_months=12,
    base_mrr=200_000,
)
print(f"  Expected value: ${forecast.expected_value():,.0f}")
for name, values in forecast.scenarios.items():
    total = sum(values)
    print(f"    {name:>14s}: ${total:>12,.0f}")
```

### Example 4: Competitive Intelligence

```python
from agent import BusinessDevelopmentAgent

agent = BusinessDevelopmentAgent("TechCo", "Developer Tools")

# Analyze competitive landscape
comp = agent.evaluate_competitive_landscape("Developer Tools")

print("Competitive Positioning:")
for c in comp["positioning_map"]:
    print(
        f"  {c['name']:25s} {c['positioning']:12s} "
        f"share={c['market_share']:.0%} threat={c['threat']}"
    )

print(f"\nMarket concentration: {comp['market_concentration']:.0%}")

print("\nStrategic Implications:")
for imp in comp["strategic_implications"]:
    print(f"  -> {imp}")

print("\nOur Competitive Moat:")
moat = comp["competitive_moat_assessment"]
print(f"  Strengths: {', '.join(moat['our_strengths'])}")
print(f"  Vulnerabilities: {', '.join(moat['vulnerabilities'])}")
```

### Example 5: Channel Strategy & Outreach

```python
from agent import BusinessDevelopmentAgent, MarketSegment

agent = BusinessDevelopmentAgent("GrowthCo", "SaaS")

# Design channel strategy for different segments
for segment in [MarketSegment.ENTERPRISE, MarketSegment.SMB]:
    channel = agent.design_channel_strategy("Pro Suite", segment)
    print(f"\n{segment.value.upper()} Channel Strategy:")
    print(f"  Channels: {', '.join(channel.channels)}")
    print(f"  Partner types: {[p.value for p in channel.partner_types]}")
    print(f"  Investment: ${channel.investment:,.0f}")
    print(f"  Est. deals: {channel.estimated_deals()}")
    print(f"  CPA: ${channel.cost_per_acquisition():,.0f}")

# Create outreach campaign
campaign = agent.create_outreach_campaign("Q2 Channel Outreach", "linkedin", 300)
print(f"\nOutreach Campaign: {campaign.name}")
print(f"  Sent: {campaign.total_sent}")
print(f"  Responses: {campaign.responses} ({campaign.response_rate():.1%})")
print(f"  Meetings: {campaign.meetings} ({campaign.meeting_rate():.1%})")
print(f"  Deals: {campaign.deals_generated}")
print(f"  Cost per meeting: ${campaign.cost_per_meeting():,.0f}")

# Analyze conversion funnel
funnel = agent.analyze_conversion_funnel()
print(f"\nConversion Funnel:")
print(f"  Overall: {funnel.overall_conversion():.1%}")
print(f"  Bottleneck: {funnel.bottleneck_stage()}")
for i, rate in enumerate(funnel.conversion_rates()):
    print(f"    {funnel.stage_names[i]} -> {funnel.stage_names[i+1]}: {rate:.1%}")
```

### Example 6: Quarterly Review Dashboard

```python
from agent import BusinessDevelopmentAgent

agent = BusinessDevelopmentAgent("ReviewCo", "Enterprise")

# Generate quarterly review
review = agent.generate_quarterly_review("Q4", 2025)
summary = review.summary()

print(f"Quarterly Review: {summary['quarter']}")
print(f"Health: {summary['health']}")
print(f"Revenue: ${summary['revenue']:,.0f}")
print(f"Pipeline: ${summary['pipeline']:,.0f}")
print(f"Deals Closed: {summary['deals']}")
print(f"Metrics: {summary['metrics_on_track']}/{summary['total_metrics']} on track")

print("\nDetailed Metrics:")
for metric in review.metrics:
    att = metric.attainment()
    bar_len = int(att * 20)
    bar = "█" * min(bar_len, 20) + "░" * max(20 - bar_len, 0)
    print(
        f"  {metric.name:30s} {bar} "
        f"{metric.value:>10,.0f} / {metric.target:>10,.0f} "
        f"({metric.status()})"
    )

print("\nHighlights:")
for h in review.highlights:
    print(f"  + {h}")

print("\nChallenges:")
for c in review.challenges:
    print(f"  - {c}")

print("\nNext Quarter Focus:")
for f in review.next_quarter_focus:
    print(f"  * {f}")
```

---

## API Reference

### Initialization

```python
BusinessDevelopmentAgent(
    company_name: str = "Acme Corp",   # Company name for context
    industry: str = "SaaS"             # Industry for market analysis
)
```

### Partner Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `find_partners()` | `criteria: dict, market: MarketSegment` | `list[dict]` | Discover and score partners |
| `evaluate_partner()` | `partner_data: dict` | `PartnerScorecard` | Multi-dimensional evaluation |
| `structure_deal()` | `partner: str, type: PartnershipType, value: float` | `Partnership` | Create and track a deal |

### Pipeline & Revenue Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `manage_pipeline()` | `stage_filter: Optional[DealStage]` | `dict` | Pipeline health and forecast |
| `model_revenue()` | `scenario: str, timeline: int, mrr: float` | `RevenueForecast` | Revenue model with NPV/IRR |
| `forecast_sales()` | `product: str, period: int, mrr: float` | `SalesForecast` | Multi-scenario forecast |

### Market & Strategy Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `analyze_market()` | `opportunity: dict` | `MarketAnalysis` | TAM/SAM/SOM analysis |
| `develop_growth_strategy()` | `profile: Optional[dict]` | `GrowthPlan` | Ansoff-based strategy |
| `plan_market_entry()` | `target: dict` | `dict` | Phased entry plan |
| `negotiate_deal()` | `value: float, style: NegotiationStyle` | `NegotiationStrategy` | ZOPA and concessions |
| `create_value_proposition()` | `market: MarketSegment, product: str` | `ValueProposition` | VP canvas |

### Analytics Methods

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `evaluate_competitive_landscape()` | `industry: str` | `dict` | Competitive analysis |
| `design_channel_strategy()` | `product: str, market: MarketSegment` | `ChannelStrategy` | Channel program design |
| `conduct_due_diligence()` | `target: dict` | `dict` | DD checklist execution |
| `generate_quarterly_review()` | `quarter: str, year: int` | `QuarterlyReview` | Performance dashboard |
| `create_outreach_campaign()` | `name: str, channel: str, size: int` | `OutreachCampaign` | Campaign funnel design |
| `analyze_conversion_funnel()` | `data: Optional[dict]` | `ConversionFunnel` | Funnel bottleneck analysis |

### Enums

| Enum | Values |
|------|--------|
| `PartnershipType` | STRATEGIC, TECHNOLOGY, DISTRIBUTION, RESELLER, MARKETING, JOINT_VENTURE, LICENSING, AFFILIATE |
| `DealStage` | IDENTIFICATION, QUALIFICATION, PROPOSAL, NEGOTIATION, CLOSING, POST_CLOSE, MAINTENANCE, EXPANSION |
| `MarketSegment` | ENTERPRISE, SMB, CONSUMER, GOVERNMENT, NON_PROFIT |
| `RevenueModel` | SUBSCRIPTION, TRANSACTIONAL, FREEMIUM, LICENSING, ADVERTISING, MARKETPLACE, USAGE_BASED |
| `CompetitorPositioning` | LEADER, CHALLENGER, NICHE, EMERGING |
| `GrowthStrategy` | MARKET_PENETRATION, MARKET_DEVELOPMENT, PRODUCT_DEVELOPMENT, DIVERSIFICATION |
| `PipelineHealth` | HEALTHY, AT_RISK, STAGNANT, DECLINING |
| `NegotiationStyle` | COMPETITIVE, COLLABORATIVE, COMPROMISE, ACCOMMODATING, AVOIDING |
| `GeographyScope` | LOCAL, REGIONAL, NATIONAL, INTERNATIONAL, GLOBAL |
| `ValuePropositionType` | COST, INNOVATION, CUSTOMER_INTIMACY, ECOSYSTEM |

### Dataclasses with Computed Methods

| Dataclass | Computed Methods |
|-----------|-----------------|
| `Partnership` | `composite_score()`, `is_high_value()`, `remaining_days()` |
| `DealPipeline` | `deals_by_stage()`, `weighted_value()`, `health()` |
| `MarketOpportunity` | `ltv_cac_ratio()`, `market_attractiveness_score()` |
| `RevenueForecast` | `npv()`, `irr()`, `payback_months()` |
| `CompetitorProfile` | `competitive_threat()` |
| `ValueProposition` | `fit_score()` |
| `SalesForecast` | `generate_scenario()`, `expected_value()` |
| `PartnerScorecard` | `compute_overall()`, `recommendation()` |
| `MarketAnalysis` | `industry_attractiveness()` |
| `GrowthPlan` | `progress_score()` |
| `NegotiationStrategy` | `zopa_width()`, `probability_of_acceptance()` |
| `LeadQualification` | `bant_score()`, `qualification_status()` |
| `ChannelStrategy` | `estimated_deals()`, `cost_per_acquisition()` |
| `PricingModel` | `price_for_tier()`, `competitive_price()` |
| `ExpansionRoadmap` | `phase_count()`, `budget_per_phase()` |
| `PartnershipAgreement` | `summary()` |
| `BusinessMetric` | `attainment()`, `status()` |
| `OutreachCampaign` | `response_rate()`, `meeting_rate()`, `deal_rate()`, `cost_per_meeting()` |
| `ConversionFunnel` | `conversion_rates()`, `overall_conversion()`, `bottleneck_stage()` |
| `QuarterlyReview` | `overall_health()`, `summary()` |

---

## Configuration

### Scoring Weights (Partner Evaluation)

| Dimension | Weight | Range | Description |
|-----------|--------|-------|-------------|
| Financial Stability | 20% | 0.0 – 1.0 | Revenue, growth, profitability, runway |
| Market Reach | 18% | 0.0 – 1.0 | Customer base, geographic coverage |
| Technical Capability | 22% | 0.0 – 1.0 | Stack maturity, innovation capacity |
| Cultural Alignment | 15% | 0.0 – 1.0 | Values, working style, communication |
| Innovation Potential | 15% | 0.0 – 1.0 | R&D investment, patent activity |
| Risk Level (inverse) | 10% | 0.0 – 1.0 | Lower risk = higher score |

### Pipeline Stage Weights

| Stage | Weight | Description |
|-------|--------|-------------|
| Identification | 5% | Very early, low confidence |
| Qualification | 15% | BANT qualified |
| Proposal | 35% | Formal proposal submitted |
| Negotiation | 60% | Active term discussion |
| Closing | 85% | Contract in final review |
| Post-Close | 100% | Agreement signed |
| Maintenance | 100% | Active relationship |
| Expansion | 100% | Upsell/cross-sell active |

### Revenue Model Scenarios

| Parameter | Conservative | Base | Aggressive |
|-----------|-------------|------|------------|
| Growth Rate | 3% | 6% | 10% |
| Churn Rate | 3% | 2% | 1.5% |
| Expansion Rate | 0.5% | 1% | 2% |
| Discount Rate | 12% | 10% | 8% |

### Market Health Thresholds

| Condition | Health Status |
|-----------|--------------|
| win_rate > 30% AND avg_age < 90d | HEALTHY |
| avg_age > 120d | STAGNANT |
| win_rate < 10% AND avg_age > 150d | DECLINING |
| Otherwise | AT_RISK |

### Negotiation Style Configurations

| Style | Concessions | Leverage Points |
|-------|------------|-----------------|
| Competitive | Max 5% volume discount, standard SLA, Net-30 | Market position, brand, proprietary tech |
| Collaborative | Flexible pricing, custom SLA, co-marketing, Net-45 | Mutual customers, tech synergy, shared growth |
| Compromise | Mid-range pricing, shared GTM costs, joint success | Market need, mutual competitive pressure |

---

## Walkthroughs

### Walkthrough 1: Building a Partner Program from Scratch

```python
from agent import BusinessDevelopmentAgent, PartnershipType, MarketSegment

agent = BusinessDevelopmentAgent("PlatformCo", "SaaS")

# Phase 1: Discovery — find potential partners
print("=== Phase 1: Discovery ===")
candidates = agent.find_partners(
    criteria={"industry": "CRM", "min_revenue": 300_000, "max_results": 5},
    market=MarketSegment.ENTERPRISE,
)
for c in candidates[:3]:
    print(f"  {c['name']}: score={c['composite_score']:.3f} ({c['recommendation']})")

# Phase 2: Evaluation — score top candidates
print("\n=== Phase 2: Evaluation ===")
for c in candidates[:3]:
    scorecard = agent.evaluate_partner({
        "name": c["name"],
        "financial_health": c["scores"]["synergy"],
        "market_reach": c["scores"]["market_reach"],
        "tech_capability": c["scores"]["capability_match"],
        "cultural_fit": c["scores"]["cultural_fit"],
        "innovation": c["scores"]["strategic_alignment"],
        "risk": 0.2,
    })
    print(f"  {c['name']}: {scorecard.overall_score:.3f} -> {scorecard.recommendation()}")

# Phase 3: Deal structure and negotiation
print("\n=== Phase 3: Deal Structure ===")
best = candidates[0]
deal = agent.structure_deal(
    partner_name=best["name"],
    partnership_type=PartnershipType.TECHNOLOGY,
    deal_value=best["estimated_revenue"] * 0.10,
)
neg = agent.negotiate_deal(deal.annual_value)
print(f"  Deal: ${deal.annual_value:,.0f}")
print(f"  ZOPA: ${neg.zone_of_possible_agreement[0]:,.0f} - "
      f"${neg.zone_of_possible_agreement[1]:,.0f}")

# Phase 4: Due diligence
print("\n=== Phase 4: Due Diligence ===")
dd = agent.conduct_due_diligence({"name": best["name"], "type": "partner"})
print(f"  Items: {dd['total_items']}, High-risk: {len(dd['high_risk_areas'])}")
print(f"  Decision: {dd['recommendation']}")

# Phase 5: Pipeline review
print("\n=== Phase 5: Pipeline Status ===")
analysis = agent.manage_pipeline()
print(f"  Deals: {analysis['total_deals']}, "
      f"Weighted: ${analysis['weighted_value']:,.0f}")
print(f"  Health: {analysis['health']}")
```

### Walkthrough 2: Complete Market Expansion Analysis

```python
from agent import BusinessDevelopmentAgent

agent = BusinessDevelopmentAgent("ExpansionCo", "Analytics")

# Step 1: Analyze current market
print("=== Step 1: Market Analysis ===")
current = agent.analyze_market({
    "industry": "Business Analytics",
    "market_size": 30_000_000_000,
    "cagr": 0.15,
})
print(f"Attractiveness: {current.industry_attractiveness():.3f}")
print(f"Trends: {', '.join(current.key_trends[:3])}")

# Step 2: Competitive landscape
print("\n=== Step 2: Competitive Analysis ===")
comp = agent.evaluate_competitive_landscape("Business Analytics")
print(f"Competitors: {comp['competitor_count']}")
for c in comp["positioning_map"]:
    print(f"  {c['name']}: {c['positioning']} ({c['threat']})")

# Step 3: Growth strategy
print("\n=== Step 3: Growth Strategy ===")
plan = agent.develop_growth_strategy({
    "current_revenue": 8_000_000,
    "products": 2,
    "markets": 1,
    "risk_tolerance": "moderate",
})
print(f"Strategy: {plan.strategy.value}")
print(f"Budget: ${plan.budget:,.0f}")
for obj in plan.objectives:
    print(f"  -> {obj}")

# Step 4: Revenue impact
print("\n=== Step 4: Revenue Projections ===")
for scenario in ["conservative", "base", "aggressive"]:
    rev = agent.model_revenue(scenario, timeline_months=36, initial_mrr=250_000)
    print(f"  {scenario:>14s}: NPV=${rev.npv():>12,.0f}")

# Step 5: Market entry plan
print("\n=== Step 5: Market Entry Plan ===")
entry = agent.plan_market_entry({
    "name": "EMEA",
    "segment": "enterprise",
    "timeline_months": 12,
    "budget": 1_000_000,
})
for phase in entry["phases"]:
    print(f"  {phase['phase']}: ${phase['budget_allocation']:,.0f}")
```

---

## Performance

### Benchmarks

| Operation | Time (ms) | Memory (KB) | Notes |
|-----------|-----------|-------------|-------|
| `find_partners` (1000 candidates) | ~15-30 | ~500 | Dominated by scoring loop |
| `evaluate_partner` | <1 | ~5 | Single partner evaluation |
| `structure_deal` | <1 | ~2 | Creates Partnership object |
| `model_revenue` (36 months) | ~5-10 | ~50 | NPV/IRR computation |
| `analyze_market` | <1 | ~10 | SWOT + Porter analysis |
| `manage_pipeline` (500 deals) | ~5-10 | ~200 | Stage grouping + weighted sum |
| `develop_growth_strategy` | <1 | ~5 | Ansoff lookup + planning |
| `negotiate_deal` | <1 | ~2 | ZOPA + concessions |
| `create_value_proposition` | <1 | ~5 | Canvas construction |
| `forecast_sales` (12 months) | ~1-2 | ~20 | 3 scenarios generated |
| `evaluate_competitive_landscape` | <1 | ~10 | Positioning map |
| `plan_market_entry` | <1 | ~10 | 4-phase plan |
| `design_channel_strategy` | <1 | ~5 | Channel mix selection |
| `conduct_due_diligence` | <1 | ~10 | 30-item checklist |
| `generate_quarterly_review` | ~1-2 | ~20 | 6 metrics + random data |
| `create_outreach_campaign` | <1 | ~5 | Funnel projection |
| `analyze_conversion_funnel` | <1 | ~2 | Rate calculation |

### Scale Characteristics

- **Single-process throughput**: ~10K operations/second (CPU-bound)
- **Memory usage**: O(n) where n = active deals + events + forecasts
- **Startup time**: < 100ms (no external dependencies to load)
- **State persistence**: None (in-memory only — serialize for persistence)

---

## Use Case Scenarios

### Scenario A: Startup Seeking First Enterprise Partnership

```python
agent = BusinessDevelopmentAgent("StartupCo", "DevTools")

# 1. Understand your market position
market = agent.analyze_market({
    "industry": "Developer Tools",
    "market_size": 15_000_000_000,
    "cagr": 0.18,
})
print(f"Market attractiveness: {market.industry_attractiveness():.3f}")

# 2. Find strategic partners (not resellers — you need credibility)
candidates = agent.find_partners(
    criteria={
        "industry": "Cloud Platforms",
        "min_revenue": 1_000_000,
        "capabilities": ["enterprise sales", "brand recognition"],
    },
    market=MarketSegment.ENTERPRISE,
)

# 3. Evaluate and pick the best
for c in candidates[:3]:
    sc = agent.evaluate_partner({
        "name": c["name"],
        "financial_health": 0.8,
        "market_reach": 0.9,
        "tech_capability": 0.7,
        "cultural_fit": 0.6,
        "innovation": 0.7,
        "risk": 0.2,
    })
    print(f"{c['name']}: {sc.overall_score:.3f} -> {sc.recommendation()}")

# 4. Model what this partnership means for revenue
rev = agent.model_revenue("base", timeline_months=24, initial_mrr=20_000)
print(f"Base NPV (24mo): ${rev.npv():,.0f}")
```

### Scenario B: Enterprise Evaluating Acquisition Target

```python
agent = BusinessDevelopmentAgent("Acquirer Corp", "Enterprise Software")

# 1. Due diligence on target
dd = agent.conduct_due_diligence({
    "name": "Target Startup",
    "type": "acquisition",
    "financial_risk": "medium",
    "technical_risk": "low",
    "team_risk": "high",  # Key person dependency
})
print(f"DD items: {dd['total_items']}")
print(f"High-risk areas: {dd['high_risk_areas']}")
print(f"Recommendation: {dd['recommendation']}")

# 2. Model combined revenue
combined = agent.model_revenue(
    "base", timeline_months=36, initial_mrr=500_000,
    assumptions={"growth_rate": 0.08, "churn_rate": 0.015}
)
print(f"Combined NPV: ${combined.npv():,.0f}")
```

### Scenario C: Mid-Market Company Entering New Geography

```python
agent = BusinessDevelopmentAgent("ExpansionCo", "Analytics")

# 1. Analyze the new market
market = agent.analyze_market({
    "industry": "Business Analytics - EMEA",
    "market_size": 12_000_000_000,
    "cagr": 0.14,
    "regulations": ["GDPR", "Data residency"],
})

# 2. Design channel for the region
channel = agent.design_channel_strategy("Analytics Suite", MarketSegment.ENTERPRISE)

# 3. Plan the entry
entry = agent.plan_market_entry({
    "name": "EMEA",
    "segment": "enterprise",
    "timeline_months": 12,
    "budget": 750_000,
    "entry_mode": "partner",
})

# 4. Run outreach
campaign = agent.create_outreach_campaign("EMEA Partner Outreach", "events", 200)
print(f"Est. meetings: {campaign.meetings}, CPA: ${campaign.cost_per_meeting():,.0f}")
```

---

## Best Practices

### 1. Always Run Multiple Revenue Scenarios

Never rely on a single forecast. Present conservative, base, and optimistic scenarios to stakeholders so they understand the range of outcomes.

```python
for scenario in ["conservative", "base", "aggressive"]:
    rev = agent.model_revenue(scenario)
    # Present all three to stakeholders
```

### 2. Evaluate Before Structuring

Always score a partner before creating a deal. Low-scoring partners waste pipeline capacity and forecasting accuracy.

```python
scorecard = agent.evaluate_partner(data)
if scorecard.overall_score < 0.5:
    return  # Don't pursue
deal = agent.structure_deal(...)
```

### 3. Monitor Pipeline Health Regularly

Run `manage_pipeline()` weekly to catch stagnation early. Stuck deals distort forecasts and consume attention.

```python
analysis = agent.manage_pipeline()
if analysis["health"] in ("STAGNANT", "DECLINING"):
    # Take action: move deals, archive stale ones, add new pipeline
```

### 4. Use Competitive Intelligence to Inform Strategy

Let competitive analysis shape your value proposition and negotiation approach, not the other way around.

```python
comp = agent.evaluate_competitive_landscape()
# Use threat levels to prioritize defensive vs offensive strategies
critical = [c for c in comp["positioning_map"] if c["threat"] == "CRITICAL"]
```

### 5. Complete Due Diligence Before Closing

Never skip due diligence to accelerate a deal. The 30-item checklist catches risks that surface-level evaluation misses.

```python
dd = agent.conduct_due_diligence(target)
if dd["high_risk_areas"]:
    # Don't close until risks are mitigated
```

### 6. Leverage the Event Log

The `_event_log` provides a complete audit trail. Review it periodically to understand agent behavior patterns and identify process improvements.

```python
for event in agent._event_log[-10:]:
    print(f"[{event['type']}] {event['detail']}")
```

### 7. Segment Channel Strategy by Market

Enterprise and SMB channels require fundamentally different approaches. Don't apply a one-size-fits-all channel strategy.

```python
enterprise = agent.design_channel_strategy(product, MarketSegment.ENTERPRISE)
smb = agent.design_channel_strategy(product, MarketSegment.SMB)
```

---

## Troubleshooting & FAQ

### Q: How do I add custom scoring weights?

Modify the `PartnerScorecard.compute_overall()` method or create a wrapper that applies your custom weights to the raw dimension scores. The weights are defined as a local list in the method.

### Q: Can I use this with a database backend?

The agent is designed for in-memory operation. For persistence, wrap methods with your ORM layer and serialize the dataclass outputs to your database schema. See ARCHITECTURE.md for database schemas.

### Q: Why are the revenue model numbers deterministic?

The model uses fixed scenario presets (growth/churn/expansion rates) and deterministic math. Given identical inputs, you will always get identical outputs. The seasonal factors are hardcoded.

### Q: How do I extend with new partnership types?

Add values to the `PartnershipType` enum. The pipeline and scoring logic are type-agnostic — new types automatically integrate without code changes.

### Q: Can I run multiple agents for different business units?

Yes. Instantiate separate `BusinessDevelopmentAgent` objects with different `company_name` and `industry` values. Each maintains independent state (partnerships, pipeline, competitors, event log).

### Q: What if `find_partners()` returns no candidates?

Lower the `min_revenue` threshold or broaden the `capabilities` list. The generator filters candidates that don't meet all criteria. Try relaxing one criterion at a time.

### Q: How do I customize the quarterly review metrics?

The `QuarterlyReview` metrics are randomly generated in the demo. For production use, override the `generate_quarterly_review` method to accept real data, or create `BusinessMetric` objects directly and pass them to a custom review builder.

### Q: Is the IRR calculation accurate?

The IRR uses binary search over 200 iterations, which provides accuracy to approximately 4 decimal places. For most business cases, this is sufficient. For exact IRR, consider using a dedicated financial library.

### Q: How do I handle multi-currency deals?

The agent uses float values without currency metadata. For multi-currency support, convert all values to a single currency before passing to agent methods, or extend the dataclasses with currency fields.

### Q: Can I integrate this with a CRM?

Yes. The agent methods accept and return structured data that maps easily to CRM objects. Use `structure_deal()` to create deals, `manage_pipeline()` to sync pipeline state, and `generate_quarterly_review()` for reporting.

---

## Contributing

Contributions welcome. Please follow these guidelines:

### Code Style

- Follow PEP 8
- Use type hints on all public methods
- Keep methods focused (single responsibility)
- Use descriptive variable names

### Documentation

- Every public method needs a docstring with Args/Returns
- Use Google-style docstring format
- Include usage examples for new methods

### Testing

- Add tests for new methods
- Run `pytest` before submitting
- Aim for >90% coverage on new code
- Test edge cases (empty inputs, zero values, extreme values)

### Enums and Dataclasses

- New enum values must be added to all relevant switch/mapping dicts
- New dataclasses should include at least one computed method
- Use `field(default_factory=...)` for mutable defaults

### Logging

- Use `logger.info()` for key operations
- Use `self._log_event()` for audit-trail events
- Never log sensitive data (credentials, PII)

### Development Setup

```bash
git clone <repo>
cd agents/business-development
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

python agent.py            # Run full demo
pytest                     # Run tests
```

---

## Changelog

### v2.0.0 (Current)

- Full rewrite with 17 agent methods
- Added 16 enums and 20 dataclasses
- Revenue modeling with NPV/IRR/payback
- Competitive analysis module
- Negotiation strategy engine with ZOPA
- Growth strategy generator (Ansoff matrix)
- Channel partner strategy design
- Due diligence tracker (30+ items)
- Outreach campaign design
- Conversion funnel analysis
- Quarterly review dashboard
- Comprehensive demo with B2B SaaS scenario

### v1.0.0

- Initial release with basic partner discovery
- Simple deal pipeline tracking
- Revenue projection (linear only)

---

## Roadmap

### v2.1 (Planned)

- [ ] Persistent state via SQLite/PostgreSQL
- [ ] REST API layer (FastAPI)
- [ ] Webhook event notifications
- [ ] Real market data integration ( Crunchbase, PitchBook)
- [ ] Multi-currency support
- [ ] Custom scoring weight configuration
- [ ] Export to CSV/PDF

### v2.2 (Planned)

- [ ] Machine learning for partner scoring
- [ ] Natural language deal summaries
- [ ] Automated outreach email generation
- [ ] CRM integration (Salesforce, HubSpot)
- [ ] Dashboard visualization (Streamlit)
- [ ] Multi-agent collaboration (parallel negotiations)

### v3.0 (Future)

- [ ] Real-time market data feeds
- [ ] Predictive pipeline analytics
- [ ] AI-powered negotiation coaching
- [ ] Cross-agent memory sharing
- [ ] Plugin architecture for custom BD workflows

---

## License

MIT License. See [LICENSE](../../LICENSE) for details.

---

*README v2.0.0 — Business Development Agent*

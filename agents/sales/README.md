# Sales Agent

> AI-powered sales automation, lead management, pipeline optimization, and revenue forecasting.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Lead Scoring](#lead-scoring)
  - [Pipeline Management](#pipeline-management)
  - [Outreach](#outreach)
  - [Analytics](#analytics)
- [API Reference](#api-reference)
- [Data Models](#data-models)
- [Design Patterns](#design-patterns)
- [Security](#security)
- [Scalability](#scalability)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Checklists](#checklists)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Overview

The Sales Agent is a comprehensive sales automation platform that provides lead scoring and qualification using the BANT framework, sales pipeline management with deal stage tracking, revenue forecasting by period, outreach template creation and personalization, sales performance analytics, conversion rate analysis, and comprehensive reporting. It is designed for sales teams, business development representatives, and revenue operations.

```
+-------------------------------------------------------------------------+
|                       SalesAgent (Orchestrator)                           |
+-------------------------------------------------------------------------+
|                                                                          |
|  +------------------+  +------------------+  +-------------------+      |
|  |  LeadScorer       |  |  PipelineManager  |  | OutreachManager   |      |
|  |                   |  |                  |  |                   |      |
|  | * Score leads     |  | * Deal CRUD      |  | * Templates       |      |
|  | * BANT qualify    |  | * Stage mgmt     |  | * Personalize     |      |
|  | * Prioritize      |  | * Forecast       |  | * Schedule        |      |
|  +------------------+  +------------------+  +-------------------+      |
|                                                                          |
|  +---------------------------------------------------------------+     |
|  |                      SalesAnalytics                             |     |
|  |                                                                |     |
|  | * Metrics | * Conversion | * Reports | * Forecast              |     |
|  +---------------------------------------------------------------+     |
+-------------------------------------------------------------------------+
```

### Design Principles

- **Data-Driven Selling**: Every decision backed by metrics and analytics
- **Lead Quality Over Quantity**: Focus on qualified leads that convert
- **Pipeline Visibility**: Full transparency into deal status and forecast
- **Revenue Focus**: Every activity ties back to revenue impact

---

## Features

| Feature | Description |
|---------|-------------|
| **Lead Scoring** | Weighted scoring based on company, title, budget, authority, need, timeline |
| **BANT Qualification** | Budget, Authority, Need, Timeline qualification framework |
| **Pipeline Management** | Deal creation, stage progression, probability weighting |
| **Revenue Forecasting** | Period-based forecast with committed and weighted revenue |
| **Outreach Automation** | Template creation, personalization, scheduling, tracking |
| **Sales Analytics** | Win rate, avg deal size, conversion rates, pipeline metrics |
| **Interaction Tracking** | Log emails, calls, meetings with leads |
| **Sales Reporting** | Comprehensive dashboard and reports |

---

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system architecture including component deep dives, data flow diagrams, design patterns, and scalability considerations.

---

## Quick Start

### Installation

```bash
# No external dependencies required
python agents/sales/agent.py
```

### Basic Usage

```python
from agents.sales.agent import SalesAgent

agent = SalesAgent()
result = agent.run()
print(result)
```

### First Lead

```python
from agents.sales.agent import SalesAgent, LeadSource

agent = SalesAgent()

# Add a lead
lead = agent.add_lead(
    name="John Smith",
    email="john@techcorp.com",
    company="TechCorp",
    title="CTO",
    source=LeadSource.WEBSITE,
    contact_info={"budget": "enterprise", "timeline": "Q2"}
)

# Score and qualify
qualification = agent.qualify_lead(lead.id)
print(f"Score: {qualification['score']}, Qualified: {qualification['qualified']}")

# Convert to deal
deal = agent.convert_to_deal(
    lead_id=lead.id,
    value=50000,
    expected_close=datetime(2024, 6, 30)
)
```

---

## Usage

### Lead Scoring

```python
from agents.sales.agent import LeadScorer

scorer = LeadScorer()
score = scorer.score_lead(lead)
qualification = scorer.qualify_lead(lead)
```

### Pipeline Management

```python
from agents.sales.agent import PipelineManager, DealStage

pipeline = PipelineManager()
deal = pipeline.create_deal(
    lead_id="L001", value=50000,
    expected_close=datetime(2024, 6, 30)
)
pipeline.move_deal_stage(deal.id, DealStage.PROPOSAL)
pipeline_value = pipeline.get_pipeline_value()
forecast = pipeline.forecast_revenue(periods=6)
```

### Outreach

```python
from agents.sales.agent import OutreachManager

outreach = OutreachManager()
outreach.add_template("intro", "Hi {{name}}", "Let's discuss {{company}}'s needs...")
personalized = outreach.personalize_template("intro", lead)
outreach.schedule_outreach(
    "L001", "intro",
    datetime.now() + timedelta(hours=1)
)
```

### Analytics

```python
from agents.sales.agent import SalesAnalytics

analytics = SalesAnalytics(agent, pipeline, outreach)
metrics = analytics.calculate_metrics()
report = analytics.generate_report()
```

---

## API Reference

| Class | Description |
|-------|-------------|
| `LeadScorer` | Score and qualify leads using BANT |
| `PipelineManager` | Manage deals and pipeline stages |
| `OutreachManager` | Template management and outreach scheduling |
| `SalesAnalytics` | Metrics, conversion analysis, and reporting |
| `SalesAgent` | Orchestrator combining all components |

### Enums

| Enum | Values |
|------|--------|
| `LeadStatus` | NEW, CONTACTED, QUALIFIED, PROPOSAL, NEGOTIATION, CLOSED_WON, CLOSED_LOST |
| `LeadSource` | WEBSITE, REFERRAL, COLD_OUTREACH, SOCIAL_MEDIA, EVENT, PAID_ADS, ORGANIC |
| `DealStage` | DISCOVERY, QUALIFICATION, NEEDS_ANALYSIS, PROPOSAL, DEMO, PRICING, CONTRACT, CLOSING |

---

## Data Models

### Lead
Contact record with scoring, qualification status, and interaction history.

### Deal
Opportunity with stage, value, probability, and forecast data.

### SalesMetrics
Aggregated sales performance metrics including win rate and pipeline value.

### OutreachTemplate
Reusable email template with personalization placeholders.

---

## Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **Strategy** | Multiple scoring algorithms | LeadScorer |
| **State Machine** | Deal stage lifecycle | PipelineManager |
| **Template Method** | Email personalization | OutreachManager |
| **Facade** | Unified sales interface | SalesAgent |
| **Observer** | Interaction tracking | OutreachManager |

## Security

- Lead PII handled with care
- Access controls on deal modifications
- Audit trail for all sales operations
- Template sanitization before personalization
- Role-based access for different sales operations

## Scalability

| Dimension | Strategy | Notes |
|-----------|----------|-------|
| Leads | Indexed by status + score | Fast filtered queries |
| Deals | Indexed by stage + value | Pipeline view |
| Templates | Cached by trigger | Fast lookup |
| Analytics | Pre-aggregated | Dashboard speed |
| Forecasts | Cached with invalidation | Recompute on change |

---

## Examples

### Complete Sales Workflow

```python
from agents.sales.agent import SalesAgent, LeadSource
from datetime import datetime, timedelta

agent = SalesAgent()

# 1. Add leads from different sources
lead1 = agent.add_lead(
    name="Alice Chen", email="alice@startup.io", company="StartupIO",
    title="CEO", source=LeadSource.REFERRAL,
    contact_info={"budget": "enterprise", "timeline": "Q2"}
)

lead2 = agent.add_lead(
    name="Bob Wilson", email="bob@corp.com", company="BigCorp",
    title="VP Engineering", source=LeadSource.WEBSITE,
    contact_info={"budget": "mid-market", "timeline": "Q3"}
)

# 2. Qualify leads
q1 = agent.qualify_lead(lead1.id)
q2 = agent.qualify_lead(lead2.id)

# 3. Convert qualified leads to deals
if q1['qualified']:
    deal1 = agent.convert_to_deal(lead1.id, 100000, datetime(2024, 6, 30))

if q2['qualified']:
    deal2 = agent.convert_to_deal(lead2.id, 50000, datetime(2024, 9, 30))

# 4. Get dashboard
dashboard = agent.get_dashboard()
print(f"Pipeline: ${dashboard['pipeline']['total_value']:,.2f}")
```

### Revenue Forecasting

```python
from agents.sales.agent import PipelineManager

pipeline = PipelineManager()

# Create multiple deals
pipeline.create_deal("L1", 50000, datetime(2024, 3, 31))
pipeline.create_deal("L2", 75000, datetime(2024, 4, 30))
pipeline.create_deal("L3", 30000, datetime(2024, 5, 31))

# Forecast next 6 months
forecast = pipeline.forecast_revenue(periods=6)
for period, data in forecast.items():
    print(f"{period}: Committed=${data['committed']:,.0f}, Weighted=${data['weighted']:,.0f}")
```

---

## Configuration

The agent uses sensible defaults. Key configurable parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| Scoring weights | BANT-based | Adjustable per organization |
| Stage probabilities | Industry standard | Customizable per stage |
| Forecast periods | 12 months | Configurable horizon |
| Qualification threshold | Score >= 60 | Adjustable strictness |
| BANT minimum | 3/4 criteria | Configurable |

---

## Best Practices

### Lead Management
1. Score every lead on entry -- never skip qualification
2. Focus on leads with score >= 60 and 3+ BANT criteria
3. Follow up within 24 hours of qualification
4. Enrich contact info to improve scoring accuracy

### Pipeline Management
1. Update deal stages weekly -- stale deals kill forecasts
2. Use probability overrides for high-confidence deals
3. Review pipeline coverage (3x target) monthly
4. Document competitor presence for win/loss analysis

### Outreach
1. Personalize every email -- never send generic blasts
2. A/B test subject lines and body content
3. Track all interactions for context
4. Follow up consistently but not excessively

### Analytics
1. Review win rate monthly -- declining rates signal issues
2. Analyze conversion rates by stage to find bottlenecks
3. Track average deal size trends
4. Compare forecast vs. actual to improve accuracy

---

## Checklists

### Lead Qualification
- [ ] Score >= 60
- [ ] 3+ BANT criteria met
- [ ] Contact info complete
- [ ] Follow-up scheduled

### Pipeline Management
- [ ] Deal stages updated weekly
- [ ] Pipeline coverage >= 3x
- [ ] Competitor info documented
- [ ] Forecast reviewed monthly

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Low lead scores | Enrich contact data; improve source quality |
| High lead-to-deal drop-off | Tighten qualification criteria |
| Pipeline value declining | Increase outbound activity; review stage definitions |
| Forecast accuracy low | Update deal stages more frequently |
| Low win rate | Improve discovery process; better qualification |

---

## Files

| File | Description |
|------|-------------|
| `agent.py` | Full implementation (all classes and logic) |
| `GROK.md` | Agent identity, capabilities, and code examples |
| `ARCHITECTURE.md` | System architecture with diagrams |
| `README.md` | This file -- overview and quick start |

---

## License

MIT License -- see [LICENSE](../../LICENSE) for details.

---

*Close more deals, forecast accurately, grow revenue consistently.*

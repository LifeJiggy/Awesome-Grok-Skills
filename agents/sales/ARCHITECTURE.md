# Sales Agent — System Architecture

## 1. Executive Summary

The Sales Agent is a comprehensive sales automation platform providing lead management, lead scoring, pipeline management, outreach automation, sales analytics, and revenue forecasting. It is designed for sales teams, business development representatives, and revenue operations.

---

## 2. Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [High-Level Architecture](#2-high-level-architecture)
3. [Component Deep Dives](#3-component-deep-dives)
4. [Data Flow Diagrams](#4-data-flow-diagrams)
5. [Design Patterns](#5-design-patterns)
6. [Tech Stack](#6-tech-stack)
7. [Security Considerations](#7-security-considerations)
8. [Scalability & Performance](#8-scalability--performance)
9. [Integration Points](#9-integration-points)
10. [Data Models](#10-data-models)
11. [Extension Points](#11-extension-points)
12. [Glossary](#12-glossary)
13. [Appendix: Design Decisions](#13-appendix-design-decisions)

---

## 3. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         SALES AGENT                                       │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │    Lead      │  │   Pipeline   │  │   Outreach   │  │   Sales    │  │
│  │   Scorer     │  │   Manager    │  │   Manager    │  │  Analytics │  │
│  │              │  │              │  │              │  │            │  │
│  │ • Score      │  │ • Deal CRUD  │  │ • Templates  │  │ • Metrics  │  │
│  │ • Qualify    │  │ • Stage mgmt │  │ • Personalize│  │ • Reports  │  │
│  │ • BANT       │  │ • Forecast   │  │ • Schedule   │  │ • Forecast │  │
│  │ • Prioritize │  │ • Pipeline   │  │ • Track      │  │ • Trends   │  │
│  │              │  │   value      │  │              │  │            │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │    Data Models (Lead, Deal, SalesMetrics, OutreachTemplate)      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Component Deep Dives

### 4.1 Lead Scorer

Lead scoring and qualification using weighted criteria.

**Responsibilities:**
- Score leads based on multiple criteria (company size, job title, budget, authority, need, timeline, source quality)
- Qualify leads using BANT framework (Budget, Authority, Need, Timeline)
- Prioritize leads for sales team follow-up
- Update scores as lead information changes

**Scoring Formula:**
```
Lead Score = Σ (criterion_score × weight)

Weights:
  company_size:  0.15
  job_title:     0.12
  budget:        0.20
  authority:     0.15
  need:          0.18
  timeline:      0.12
  source_quality: 0.08

Total = 1.00
```

**Qualification Matrix (BANT):**
```
┌───────────┬──────────────────────────────────────────────┐
│ Criterion │ Qualification Logic                          │
├───────────┼──────────────────────────────────────────────┤
│ Budget    │ Has budget indicator in contact info         │
│ Authority │ Title is CTO, VP, Director, or CEO          │
│ Need      │ Has notes or "need" tag                     │
│ Timeline  │ Has timeline in contact info                │
├───────────┼──────────────────────────────────────────────┤
│ Qualified │ Score >= 60 AND >= 3 BANT criteria met      │
└───────────┴──────────────────────────────────────────────┘
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `score_lead(lead)` | Calculate lead score (0-100) |
| `qualify_lead(lead)` | Determine BANT qualification |

---

### 4.2 Pipeline Manager

Sales pipeline and deal lifecycle management.

**Responsibilities:**
- Create and manage deals
- Track deal stages with probability weighting
- Calculate pipeline value (weighted and committed)
- Forecast revenue by period
- Maintain stage history for analytics

**Deal Stage Probabilities:**
```
┌────────────────────┬─────────────┬──────────────────────────────────┐
│ Stage              │ Probability │ Description                      │
├────────────────────┼─────────────┼──────────────────────────────────┤
│ DISCOVERY          │ 10%         │ Initial contact, exploring needs │
│ QUALIFICATION      │ 20%         │ BANT criteria being evaluated    │
│ NEEDS_ANALYSIS     │ 30%         │ Deep dive into requirements      │
│ PROPOSAL           │ 40%         │ Proposal sent to prospect        │
│ DEMO               │ 50%         │ Product demonstration            │
│ PRICING            │ 60%         │ Pricing discussion               │
│ CONTRACT           │ 75%         │ Contract in negotiation          │
│ CLOSING            │ 90%         │ Final closing steps              │
└────────────────────┴─────────────┴──────────────────────────────────┘
```

**Pipeline Value Calculation:**
```
Pipeline Value = Σ (deal_value × probability)
Committed Value = Σ (deal_value) where stage >= CONTRACT
Weighted Forecast = Σ (deal_value × probability × recency_factor)
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `create_deal(lead_id, value, expected_close, products)` | Create a new deal |
| `move_deal_stage(deal_id, new_stage, probability_override)` | Advance deal stage |
| `get_pipeline_value()` | Calculate weighted pipeline value |
| `get_deals_by_stage()` | Group deals by current stage |
| `forecast_revenue(periods)` | Forecast revenue by period |

---

### 4.3 Outreach Manager

Sales outreach and communication management.

**Responsibilities:**
- Create and manage email templates
- Personalize templates for individual leads
- Schedule outreach campaigns
- Track interactions with leads
- Support A/B testing of templates

**Template Personalization:**
```
Placeholders:
  {{name}}     → Lead's name
  {{company}}  → Lead's company
  {{title}}    → Lead's job title

Template Example:
  Subject: "Hi {{name}}, improve {{company}}'s security"
  Body: "As {{title}}, you understand the importance of..."
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `add_template(name, subject, body, trigger)` | Create email template |
| `personalize_template(template_name, lead)` | Personalize for lead |
| `schedule_outreach(lead_id, template_name, scheduled_time)` | Schedule send |
| `track_interaction(lead_id, interaction_type, details)` | Log interaction |

---

### 4.4 Sales Analytics

Sales performance analysis and reporting.

**Responsibilities:**
- Calculate key sales metrics (win rate, avg deal size, pipeline value)
- Analyze conversion rates between stages
- Identify top performing deals
- Generate comprehensive sales reports
- Forecast revenue trends

**Key Metrics:**
```
┌──────────────────────┬─────────────────────────────────────────┐
│ Metric               │ Calculation                             │
├──────────────────────┼─────────────────────────────────────────┤
│ Win Rate             │ closed_won / total_closed               │
│ Avg Deal Size        │ sum(closed_won_values) / count(won)     │
│ Pipeline Value       │ sum(deal_value × probability)           │
│ Revenue Forecast     │ pipeline_value × win_rate_factor        │
│ Conversion Rate      │ deals_in_stage / total_deals            │
│ Sales Cycle Length    │ avg(close_date - created_date)          │
│ Lead-to-Close Rate   │ closed_won / total_leads                │
└──────────────────────┴─────────────────────────────────────────┘
```

**Key Methods:**
| Method | Description |
|--------|-------------|
| `calculate_metrics()` | Calculate all key sales metrics |
| `analyze_conversion_rates()` | Conversion rates by stage |
| `identify_top_performers()` | Top deals by value |
| `generate_report()` | Comprehensive sales report |

---

## 5. Data Flow Diagrams

### 5.1 Lead-to-Deal Pipeline

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    LEAD-TO-DEAL PIPELINE                                  │
│                                                                          │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │
│  │  New     │    │  Score   │    │ Qualify  │    │  Convert │          │
│  │  Lead    │───▶│  Lead    │───▶│  Lead    │───▶│  to Deal │          │
│  │          │    │          │    │          │    │          │          │
│  │ • Name   │    │ • BANT   │    │ • Score  │    │ • Value  │          │
│  │ • Email  │    │ • Score  │    │ • > 60   │    │ • Close  │          │
│  │ • Source │    │ • Weight │    │ • 3/4    │    │   date   │          │
│  └──────────┘    └──────────┘    └──────────┘    └────┬─────┘          │
│                                                        │                │
│                                                        ▼                │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                     DEAL STAGES                                  │   │
│  │                                                                   │   │
│  │  Discovery ──▶ Qualification ──▶ Needs Analysis ──▶ Proposal    │   │
│  │     10%            20%              30%              40%         │   │
│  │                                                                   │   │
│  │  Demo ──▶ Pricing ──▶ Contract ──▶ Closing                      │   │
│  │   50%       60%         75%          90%                         │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                              │                                           │
│                              ▼                                           │
│                    ┌──────────────────┐                                  │
│                    │   CLOSED WON     │                                  │
│                    │                  │                                  │
│                    │ Revenue recorded │                                  │
│                    │ Win rate updated │                                  │
│                    └──────────────────┘                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

### 5.2 Outreach Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    OUTREACH FLOW                                 │
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                  │
│  │ Template │    │ Personalize│   │ Schedule │                  │
│  │ Created  │───▶│ for Lead  │───▶│ Outreach │                  │
│  └──────────┘    └──────────┘    └────┬─────┘                  │
│                                       │                          │
│                                       ▼                          │
│                              ┌──────────────┐                   │
│                              │  Send/Track  │                   │
│                              │              │                   │
│                              │ • Email sent │                   │
│                              │ • Opened     │                   │
│                              │ • Clicked    │                   │
│                              │ • Replied    │                   │
│                              └──────────────┘                   │
└─────────────────────────────────────────────────────────────────┘
```

### 5.3 Revenue Forecast Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  REVENUE FORECAST FLOW                           │
│                                                                  │
│  Current Deals ──→ Stage Weighting ──→ Period Assignment         │
│       │                  │                    │                  │
│       ▼                  ▼                    ▼                  │
│  Deal Values      × Probability      = Weighted Revenue         │
│  Close Dates         by Stage         per Period                 │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  Period 1 (Month 1)  │ $50K committed + $30K weighted  │   │
│  │  Period 2 (Month 2)  │ $20K committed + $45K weighted  │   │
│  │  Period 3 (Month 3)  │ $10K committed + $60K weighted  │   │
│  │  ...                                                        │   │
│  └──────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 6. Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **Strategy** | Multiple scoring algorithms | LeadScorer |
| **State** | Deal stage lifecycle | PipelineManager |
| **Template Method** | Email template personalization | OutreachManager |
| **Observer** | Interaction tracking | OutreachManager |
| **Factory** | Deal creation from lead | PipelineManager |
| **Facade** | Unified sales interface | SalesAgent |
| **Composite** | Analytics aggregation | SalesAnalytics |
| **Decorator** | Metrics calculation wraps raw data | SalesAnalytics |

---

## 7. Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Data Structures | dataclasses, Enum, Dict, List |
| ID Generation | uuid4 (truncated) |
| Date/Time | datetime, timedelta |
| Collections | defaultdict, Counter |
| Logging | Python logging |
| Optional | SQLite, PostgreSQL, CRM API |

---

## 8. Security Considerations

- **Input Validation**: All public methods validate inputs
- **PII Protection**: Lead contact information handled carefully
- **Access Control**: Method-level for sensitive operations
- **Audit Trail**: All lead and deal changes logged
- **Data Isolation**: Each lead and deal independent
- **Template Safety**: Email templates sanitized before personalization
- **No External Calls**: All computation local; CRM integration optional

---

## 9. Scalability & Performance

| Operation | Target | Notes |
|-----------|--------|-------|
| Lead scoring | < 5ms | Weighted calculation |
| Lead qualification | < 5ms | BANT check |
| Deal creation | < 2ms | Dict insertion |
| Stage transition | < 2ms | State update |
| Pipeline value | < 10ms | Aggregation |
| Revenue forecast | < 50ms | Period-based calculation |
| Metrics calculation | < 20ms | Aggregate over all deals |
| Report generation | < 100ms | Full dashboard |
| Template personalization | < 5ms | String replacement |
| Interaction tracking | < 2ms | List append |

---

## 10. Integration Points

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTEGRATION ARCHITECTURE                       │
│                                                                  │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │  CRM System  │ ◀─────▶ │  Sales       │                      │
│  │  (Salesforce,│  sync   │  Agent       │                      │
│  │   HubSpot)   │         │              │                      │
│  └──────────────┘         └──────────────┘                      │
│         │                       │                                │
│         │                       │                                │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │  Email       │ ◀─────▶ │  Outreach    │                      │
│  │  Platform    │  send   │  Manager     │                      │
│  │  (SendGrid)  │         │              │                      │
│  └──────────────┘         └──────────────┘                      │
│         │                       │                                │
│         │                       │                                │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │  Calendar    │ ◀─────▶ │  Scheduling  │                      │
│  │  (Google,    │  events │              │                      │
│  │   Outlook)   │         │              │                      │
│  └──────────────┘         └──────────────┘                      │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11. Data Models

### Core Entities

```
┌─────────────────┐     ┌─────────────────┐
│      Lead       │     │      Deal       │
│                 │     │                 │
│ • id            │     │ • id            │
│ • name          │     │ • lead_id       │
│ • email         │     │ • stage         │
│ • company       │     │ • value         │
│ • title         │     │ • probability   │
│ • status        │     │ • expected_close│
│ • source        │     │ • products      │
│ • score         │     │ • requirements  │
│ • tags          │     │ • competitors   │
│ • notes         │     └─────────────────┘
│ • contact_info  │
└─────────────────┘     ┌─────────────────┐
                        │  SalesMetrics   │
┌─────────────────┐     │                 │
│ OutreachTemplate│     │ • total_leads   │
│                 │     │ • qualified     │
│ • name          │     │ • pipeline_val  │
│ • subject       │     │ • win_rate      │
│ • body          │     │ • avg_deal_size │
│ • trigger       │     │ • forecast      │
└─────────────────┘     └─────────────────┘
```

---

## 12. Extension Points

1. **Custom Scoring Models**: Add ML-based lead scoring
2. **CRM Integration**: Sync with Salesforce, HubSpot, Pipedrive
3. **Email Integration**: Connect to SendGrid, Mailgun, SES
4. **Calendar Integration**: Schedule meetings via Google/Outlook
5. **Custom Stages**: Define organization-specific pipeline stages
6. **Territory Management**: Add geographic or industry-based territories
7. **Commission Calculation**: Track and calculate sales commissions
8. **Conversation Intelligence**: Analyze call transcripts for insights

---

## 13. Glossary

| Term | Definition |
|------|-----------|
| BANT | Budget, Authority, Need, Timeline — lead qualification framework |
| Pipeline | Active deals in various stages of the sales process |
| Win Rate | Percentage of deals that close successfully |
| Deal Velocity | Speed at which deals move through the pipeline |
| MRR | Monthly Recurring Revenue |
| ARR | Annual Recurring Revenue |
| ACV | Annual Contract Value |
| LTV | Customer Lifetime Value |
| CAC | Customer Acquisition Cost |
| SQL | Sales Qualified Lead |
| MQL | Marketing Qualified Lead |
| Stage | Current position of a deal in the pipeline |
| Conversion Rate | Percentage moving from one stage to the next |

---

## 14. Appendix: Design Decisions

| Decision | Rationale |
|----------|-----------|
| UUID-based IDs | Globally unique, no coordination needed |
| Weighted scoring | Transparent, adjustable lead prioritization |
| Stage probabilities | Industry-standard pipeline forecasting |
| In-memory storage | Simplicity; persistence layer optional |
| BANT qualification | Widely adopted qualification framework |
| Template personalization | Scalable outreach without per-lead writing |
| Period-based forecasting | Aligns with business reporting cycles |
| History tracking | Enables trend analysis and coaching |
| Separate scorer | Allows independent scoring model changes |

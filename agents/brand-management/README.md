# Brand Management Agent v2.0

> Enterprise-grade brand lifecycle management system — auditing, sentiment analysis, crisis response, competitive intelligence, campaign tracking, and reputation management.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
  - [Example 1: Brand Audit](#example-1-brand-audit)
  - [Example 2: Sentiment Monitoring](#example-2-sentiment-monitoring)
  - [Example 3: Crisis Management](#example-3-crisis-management)
  - [Example 4: Competitive Intelligence](#example-4-competitive-intelligence)
  - [Example 5: Campaign Performance](#example-5-campaign-performance)
  - [Example 6: Audience Segmentation](#example-6-audience-segmentation)
  - [Example 7: Brand Equity Measurement](#example-7-brand-equity-measurement)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Walkthrough](#walkthrough)
- [Best Practices](#best-practices)
- [Troubleshooting & FAQ](#troubleshooting--faq)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Brand Management Agent is a comprehensive Python implementation for managing the complete brand lifecycle. It integrates eight core modules into a unified operational framework:

| Module | Purpose | Key Output |
|--------|---------|------------|
| Brand Audit | 10-dimension brand health assessment | Score, grade, SWOT, recommendations |
| Sentiment Analysis | Real-time channel sentiment monitoring | Sentiment scores, trends, alerts |
| Crisis Management | Automated crisis detection and response | Response plans, escalation tiers |
| Competitive Intelligence | Market positioning and competitor analysis | SWOT, threat scores, whitespace |
| Campaign Performance | Campaign lifecycle tracking and ROI | KPIs, ROI, conversion metrics |
| Audience Segmentation | Multi-dimensional audience analysis | Segments, LTV, churn risk |
| Brand Equity | Keller's Brand Equity Model scoring | Pyramid scores, equity trend |
| Reputation Management | Cross-source reputation tracking | Composite scores, trust index |

### Key Features

- **Industry-Standard Frameworks**: Keller's Brand Equity Model, NPS methodology, Brand Asset Valuator
- **Rich Type System**: 10 enums, 15 dataclasses, full type hints throughout
- **Comprehensive Data Models**: Brand profiles, guidelines, audit results, crisis events
- **Actionable Outputs**: Prioritized recommendations with estimated budgets
- **Crisis Simulation**: Tabletop exercise capability for preparedness testing
- **Stakeholder Reporting**: Executive-ready briefs with key metrics
- **Event Sourcing**: Complete audit trail for all brand operations

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    BRAND MANAGEMENT AGENT v2.0                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    ORCHESTRATION LAYER                       │   │
│  │              BrandManagementAgent (Main Class)               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│  ┌───────────────────────────┼─────────────────────────────────┐   │
│  │              DOMAIN MODULES                                  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │
│  │  │  Brand   │  │Sentiment │  │  Crisis  │  │Competitor│  │   │
│  │  │  Audit   │  │ Analysis │  │ Response │  │  Intel   │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │
│  │  │ Campaign │  │ Audience │  │  Brand   │  │Reputation│  │   │
│  │  │Tracking  │  │Segments  │  │ Equity   │  │ Mgmt     │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│  ┌───────────────────────────┼─────────────────────────────────┐   │
│  │              DATA LAYER                                      │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │   │
│  │  │  Brand   │  │Guidelines│  │Sentiment │  │  Crisis  │  │   │
│  │  │ Profiles │  │  Store   │  │ History  │  │  Events  │  │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| Observer | Real-time crisis detection, sentiment alerts | Crisis Management, Sentiment Analysis |
| Strategy | Interchangeable equity measurement models | Brand Equity Model |
| Factory | Crisis response plan creation by severity | Crisis Management |
| Pipeline | Data processing chains in audits | Brand Audit |
| CQRS | Separate read/write for brand data | All modules |

---

## Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/your-org/brand-management-agent.git
cd brand-management-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Requirements

```
# requirements.txt
python>=3.11
```

The agent is implemented using Python standard library only (dataclasses, enum, typing, logging, datetime, statistics, math, uuid, json, hashlib). No external dependencies required.

### Verify Installation

```bash
python agent.py
```

You should see the demo output with all brand management operations completing successfully.

---

## Quick Start

### 1. Import and Initialize

```python
from agent import BrandManagementAgent, BrandProfile, BrandStage

# Initialize the agent
agent = BrandManagementAgent()
```

### 2. Register a Brand

```python
profile = BrandProfile(
    brand_id="my_brand",
    name="My Company",
    founded_year=2020,
    industry="technology",
    stage=BrandStage.GROWTH,
    mission="Empowering customers through innovation",
    vision="A world transformed by our technology",
    values=["innovation", "integrity", "excellence"],
    target_audience=["enterprise", "mid_market"],
    positioning_statement="The leading platform for digital transformation",
    unique_value_proposition="AI-powered solutions that adapt to your needs",
    brand_archetype="The Creator",
    primary_channels=["website", "social_linkedin", "email"],
    headquarters="San Francisco, CA",
    employee_count=200,
    annual_revenue=50_000_000.0,
    market_share=0.05,
    brand_colors={"primary": "#0066CC", "secondary": "#00CC66"},
    typography={"primary": "Inter", "secondary": "Merriweather"},
    brand_voice_attributes=["confident", "approachable", "innovative"],
)

agent.register_brand(profile)
```

### 3. Run Operations

```python
# Brand audit
audit = agent.brand_audit("my_brand")
print(f"Brand Health: {audit.overall_score:.1f}/100 ({audit.grade()})")

# Sentiment monitoring
sentiment = agent.monitor_sentiment("my_brand")
print(f"Sentiment: {sentiment.overall_level.label}")

# Brand equity
equity = agent.measure_brand_equity("my_brand")
print(f"Brand Equity: {equity.overall_equity:.1f}/100")
```

---

## Usage Examples

### Example 1: Brand Audit

Execute a comprehensive brand audit with 10-dimensional scoring.

```python
from agent import BrandManagementAgent, AuditScope

agent = BrandManagementAgent()
# ... register brand first ...

# Full brand audit
audit = agent.brand_audit("brand_id", AuditScope.FULL)

# Access results
print(f"Overall Score: {audit.overall_score:.1f}/100")
print(f"Grade: {audit.grade()}")
print(f"\nDimensional Scores:")
for dim, score in sorted(audit.dimensional_scores.items(), key=lambda x: -x[1]):
    print(f"  {dim}: {score:.1f}")

# Review SWOT
print(f"\nStrengths ({len(audit.strengths)}):")
for s in audit.strengths[:5]:
    print(f"  + {s}")

print(f"\nWeaknesses ({len(audit.weaknesses)}):")
for w in audit.weaknesses[:5]:
    print(f"  - {w}")

# Get prioritized recommendations
print(f"\nTop Recommendations:")
for rec in audit.priority_actions()[:3]:
    print(f"  [{rec['priority']}] {rec['dimension']}")
    print(f"    Score: {rec['current_score']:.1f} → {rec['target_score']:.1f}")
    print(f"    Actions: {rec['action_items'][:2]}")
    print(f"    Budget: ${rec['budget_estimate']:,.0f}")
```

### Example 2: Sentiment Monitoring

Monitor brand sentiment across multiple channels with real-time alerts.

```python
from agent import BrandManagementAgent, BrandChannel

agent = BrandManagementAgent()
# ... register brand first ...

# Monitor across specific channels
sentiment = agent.monitor_sentiment("brand_id", [
    BrandChannel.SOCIAL_TWITTER,
    BrandChannel.SOCIAL_INSTAGRAM,
    BrandChannel.WEBSITE,
    BrandChannel.EMAIL,
])

# Analyze results
print(f"Overall Sentiment: {sentiment.overall_score:.3f}")
print(f"Level: {sentiment.overall_level.label}")
print(f"Volume: {sentiment.volume:,} mentions")
print(f"Share of Voice: {sentiment.share_of_voice:.1%}")
print(f"Confidence: {sentiment.confidence_score:.1%}")

# Channel breakdown
print(f"\nChannel Performance:")
for channel, data in sentiment.channel_breakdown.items():
    emoji = "+" if data["sentiment"] > 0.2 else "-" if data["sentiment"] < -0.2 else "~"
    print(f"  {channel}: {emoji} {data['sentiment']:.3f} ({data['volume']:,} mentions)")

# Check for alerts
if sentiment.alerts:
    print(f"\nAlerts ({len(sentiment.alerts)}):")
    for alert in sentiment.alerts:
        print(f"  ! {alert}")

# Trend analysis
delta = sentiment.sentiment_delta()
trend = "improving" if delta > 0.05 else "declining" if delta < -0.05 else "stable"
print(f"\n30-Day Trend: {trend} ({delta:+.3f})")
```

### Example 3: Crisis Management

Handle a crisis event with automated response plan generation.

```python
from agent import BrandManagementAgent, CrisisEvent, CrisisSeverity, BrandChannel
from datetime import datetime, timezone

agent = BrandManagementAgent()
# ... register brand first ...

# Define crisis event
crisis = CrisisEvent(
    event_id="crisis_001",
    brand_id="brand_id",
    title="Customer Data Breach Disclosure",
    description="Security researcher identifies vulnerability in customer database API",
    severity=Criseseverity.HIGH,
    source="external_security_researcher",
    channel=BrandChannel.SOCIAL_TWITTER,
    discovered_at=datetime.now(timezone.utc),
    trigger_event="Responsible disclosure email received",
    affected_stakeholders=["customers", "employees", "regulators", "media", "partners"],
    estimated_reach=500000,
    velocity=0.75,
    current_sentiment=-0.55,
)

# Generate response plan
plan = agent.handle_crisis(crisis)

# Review plan
print(f"Crisis Response Plan: {plan.plan_id}")
print(f"Escalation Tier: {plan.tier}")
print(f"Budget Allocation: ${plan.budget_allocation:,.0f}")
print(f"\nResponse Team ({len(plan.response_team)} members):")
for member in plan.response_team:
    print(f"  {member['role']}: {member['responsibility']}")

print(f"\nImmediate Actions ({len(plan.immediate_actions)}):")
for action in plan.immediate_actions:
    status = "DONE" if action["completed"] else "PENDING"
    print(f"  [{status}] {action['action']} (by {action['deadline_hours']}h)")

print(f"\nCommunication Strategy:")
print(f"  Approach: {plan.communication_strategy['approach']}")
print(f"  Spokesperson: {plan.communication_strategy['spokesperson']}")
print(f"  Update Frequency: {plan.communication_strategy['update_frequency']}")

# Run crisis simulation for training
print(f"\n--- Running Simulation ---")
sim_plan = agent.simulate_crisis("data_breach", "brand_id")
print(f"Simulation Plan: {sim_plan.plan_id}")
```

### Example 4: Competitive Intelligence

Analyze competitive positioning and identify market opportunities.

```python
from agent import BrandManagementAgent

agent = BrandManagementAgent()
# ... register brand first ...

# Analyze competitors
competitors = agent.analyze_competitors("brand_id", [
    "competitor_alpha",
    "competitor_beta",
    "competitor_gamma",
    "competitor_delta",
])

print("Competitive Landscape:")
for comp in competitors:
    print(f"\n{comp.competitor_name} ({comp.tier.value.upper()})")
    print(f"  Market Share: {comp.market_share:.1%}")
    print(f"  Brand Strength: {comp.brand_strength:.1f}")
    print(f"  Threat Score: {comp.threat_score():.1f}")
    print(f"  Innovation Index: {comp.innovation_index:.1f}")
    print(f"  Strengths: {', '.join(comp.strengths[:3])}")
    print(f"  Weaknesses: {', '.join(comp.weaknesses[:2])}")

# Generate positioning map
positioning = agent.competitive_positioning("brand_id")

print(f"\nCompetitive Positioning:")
print(f"  Brand Position: ({positioning['positioning_map']['brand_position']['x']:.0f}, "
      f"{positioning['positioning_map']['brand_position']['y']:.0f})")

print(f"\nWhitespace Opportunities:")
for opp in positioning["whitespace_opportunities"]:
    print(f"  + {opp}")

print(f"\nStrategic Recommendations:")
for rec in positioning["strategic_recommendations"]:
    print(f"  > {rec}")
```

### Example 5: Campaign Performance

Create and track campaign performance with KPI monitoring.

```python
from agent import BrandManagementAgent

agent = BrandManagementAgent()
# ... register brand first ...

# Create campaign brief
campaign = agent.create_campaign_brief(
    "brand_id",
    objectives=[
        "Increase brand awareness by 25% in target market",
        "Generate 5,000 marketing qualified leads",
        "Improve Net Promoter Score by 10 points",
    ],
    budget=300000.0,
)

print(f"Campaign Created: {campaign.name}")
print(f"ID: {campaign.campaign_id}")
print(f"Budget: ${campaign.budget:,.0f}")
print(f"Duration: {campaign.start_date.strftime('%Y-%m-%d')} to {campaign.end_date.strftime('%Y-%m-%d')}")

# Track performance over time
print(f"\nPerformance Tracking:")
for day in range(7):
    perf = agent.track_campaign_performance(campaign.campaign_id)
    print(f"\n  Day {day + 1}:")
    print(f"    Impressions: {perf.get('impressions', 0):,}")
    print(f"    ROI: {perf['roi']:.1f}%")
    print(f"    Conversion Rate: {perf['conversion_rate']:.2f}%")
    print(f"    Budget Used: {perf['budget_utilization']:.1f}%")

# Get campaign summary
summary = agent.get_campaign_summary("brand_id")
print(f"\nCampaign Summary:")
print(f"  Total Campaigns: {summary['campaign_count']}")
print(f"  Active: {summary['active_campaigns']}")
print(f"  Total Spend: ${summary['total_spend']:,.0f}")
print(f"  Total Revenue: ${summary['total_revenue']:,.0f}")
print(f"  Average ROI: {summary['average_roi']:.1f}%")
```

### Example 6: Audience Segmentation

Perform multi-dimensional audience segmentation with health analysis.

```python
from agent import BrandManagementAgent

agent = BrandManagementAgent()
# ... register brand first ...

# Segment audience
segments = agent.segment_audience("brand_id")

print("Audience Segments:")
for seg in segments:
    print(f"\n{seg.name}")
    print(f"  Description: {seg.description}")
    print(f"  Size: {seg.size:,}")
    print(f"  Sentiment: {seg.sentiment_toward_brand:.2f}")
    print(f"  Loyalty: {seg.loyalty_score:.2f}")
    print(f"  LTV: ${seg.lifetime_value:,.0f}")
    print(f"  CAC: ${seg.acquisition_cost:,.0f}")
    print(f"  LTV/CAC Ratio: {seg.ltv_to_cac_ratio():.1f}x")
    print(f"  Churn Risk: {seg.churn_risk:.0%}")
    print(f"  Health: {seg.segment_health()}")
    print(f"  Preferred Channels: {', '.join(ch.value for ch in seg.preferred_channels[:3])}")

# Get insights for a specific segment
if segments:
    insights = agent.get_segment_insights("brand_id", segments[0].segment_id)
    print(f"\nSegment Insights: {insights['segment']}")
    print(f"  Health: {insights['health']}")
    print(f"  LTV/CAC: {insights['ltv_cac_ratio']:.1f}x")
    print(f"  Retention Strategy: {insights['retention_strategy']}")
```

### Example 7: Brand Equity Measurement

Measure brand equity using Keller's Brand Equity Pyramid.

```python
from agent import BrandManagementAgent

agent = BrandManagementAgent()
# ... register brand first ...

# Measure brand equity
equity = agent.measure_brand_equity("brand_id")

print("Brand Equity Analysis (Keller's Model)")
print(f"=" * 50)
print(f"Overall Equity Score: {equity.overall_equity:.1f}/100")
print(f"Trend: {equity.equity_trend()}")
print(f"Pyramid Completeness: {equity.pyramid_completeness():.1f}%")

print(f"\nKeller's Pyramid Levels:")
print(f"  Salience (Awareness):     {equity.brand_salience:.1f}")
print(f"  Performance (Quality):    {equity.performance_assessment:.1f}")
print(f"  Imagery (Associations):   {equity.imagery_assessment:.1f}")
print(f"  Judgments (Credibility):  {equity.judgments:.1f}")
print(f"  Feelings (Emotions):      {equity.feelings:.1f}")
print(f"  Resonance (Loyalty):      {equity.resonance:.1f}")

print(f"\nCompetitive Benchmark: {equity.competitive_benchmark:.1f}")

# Show historical trend
print(f"\nEquity Trend (last {len(equity.historical_trend)} measurements):")
for date, score in equity.historical_trend[-5:]:
    bar = "#" * int(score / 2)
    print(f"  {date.strftime('%Y-%m')}: {bar} {score:.1f}")
```

---

## API Reference

### BrandManagementAgent

#### Core Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `brand_audit(brand_id, scope)` | Execute comprehensive brand audit | `BrandAuditResult` |
| `create_guidelines(brand_id, elements)` | Generate brand guidelines | `List[BrandGuideline]` |
| `monitor_sentiment(brand_id, channels)` | Monitor sentiment across channels | `SentimentReport` |
| `handle_crisis(crisis_event)` | Generate crisis response plan | `CrisisResponsePlan` |
| `analyze_competitors(brand_id, competitor_ids)` | Analyze competitive landscape | `List[CompetitorAnalysis]` |
| `measure_brand_equity(brand_id)` | Measure brand equity (Keller's) | `BrandEquityScore` |
| `manage_reputation(brand_id, source)` | Track reputation across sources | `ReputationMetrics` |
| `create_campaign_brief(brand_id, objectives, budget)` | Create campaign with KPIs | `CampaignPerformance` |
| `segment_audience(brand_id)` | Perform audience segmentation | `List[AudienceSegment]` |
| `generate_brand_health_report(brand_id)` | Generate health dashboard | `BrandHealthDashboard` |
| `track_brand_consistency(brand_id)` | Score brand consistency | `Dict[str, Any]` |
| `manage_brand_partnerships(brand_id)` | Evaluate partnerships | `Dict[str, Any]` |
| `competitive_positioning(brand_id)` | Generate positioning map | `Dict[str, Any]` |
| `simulate_crisis(crisis_type, brand_id)` | Run crisis simulation | `CrisisResponsePlan` |
| `generate_stakeholder_brief(brand_id, audience)` | Create executive brief | `StakeholderBrief` |

#### Utility Methods

| Method | Description | Returns |
|--------|-------------|---------|
| `register_brand(profile)` | Register a brand profile | `str` (brand_id) |
| `get_brand_profile(brand_id)` | Retrieve brand profile | `BrandProfile` |
| `update_brand_profile(brand_id, updates)` | Update brand fields | `BrandProfile` |
| `get_guidelines(brand_id)` | Get all brand guidelines | `List[BrandGuideline]` |
| `get_sentiment_trend(brand_id, periods)` | Get sentiment history | `List[Tuple]` |
| `get_active_crises()` | List unresolved crises | `List[CrisisEvent]` |
| `resolve_crisis(event_id, notes)` | Mark crisis resolved | `CrisisEvent` |
| `track_campaign_performance(campaign_id)` | Get campaign metrics | `Dict[str, Any]` |
| `export_brand_data(brand_id)` | Export all brand data | `Dict[str, Any]` |

### Enums

| Enum | Values | Purpose |
|------|--------|---------|
| `BrandElement` | LOGO, COLOR, TYPOGRAPHY, VOICE, IMAGERY, MESSAGING, TAGLINE, SHAPE, SOUND, SPATIAL | Brand identity elements |
| `BrandHealthMetric` | AWARENESS, RECOGNITION, RECALL, PREFERENCE, LOYALTY, ADVOCACY, ... | Health measurement dimensions |
| `SentimentLevel` | VERY_POSITIVE, POSITIVE, NEUTRAL, NEGATIVE, VERY_NEGATIVE | Sentiment classification |
| `CrisisSeverity` | LOW, MEDIUM, HIGH, CRITICAL, CATASTROPHIC | Crisis severity levels |
| `BrandChannel` | WEBSITE, SOCIAL_FACEBOOK, SOCIAL_TWITTER, ... | Brand operation channels |
| `ReputationSource` | CUSTOMER_REVIEWS, EMPLOYEE_REVIEWS, MEDIA_COVERAGE, ... | Reputation data sources |
| `AuditScope` | FULL, VISUAL_IDENTITY, DIGITAL_PRESENCE, ... | Audit execution scope |
| `CompetitorTier` | DIRECT, INDIRECT, ASPIRATIONAL, EMERGING, DISRUPTIVE | Competitor classification |
| `BrandStage` | PRE_LAUNCH, LAUNCH, GROWTH, MATURITY, DECLINE, REVITALIZATION | Brand lifecycle stage |
| `CampaignStatus` | PLANNING, APPROVAL_PENDING, IN_PROGRESS, COMPLETED, ... | Campaign lifecycle state |

---

## Configuration

### Agent Configuration

```python
config = {
    "demo_mode": False,
    "audit_scoring": {
        "methodology": "multi-dimensional",
        "random_variance": 0.15,
    },
    "sentiment_analysis": {
        "confidence_threshold": 0.80,
        "alert_threshold": -0.3,
    },
    "crisis_management": {
        "auto_escalation": True,
        "executive_threshold": 3,
    },
    "caching": {
        "enabled": True,
        "ttl_seconds": 300,
    },
}

agent = BrandManagementAgent(config=config)
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BRAND_AGENT_LOG_LEVEL` | INFO | Logging level |
| `BRAND_AGENT_CACHE_TTL` | 300 | Cache TTL in seconds |
| `BRAND_AGENT_CRISIS_AUTO_ESCALATE` | true | Auto-escalate crises |
| `BRAND_AGENT_SENTIMENT_THRESHOLD` | -0.3 | Sentiment alert threshold |

---

## Walkthrough

### End-to-End Brand Management Scenario

This walkthrough demonstrates a complete brand management workflow for a technology startup.

```python
from agent import (
    BrandManagementAgent, BrandProfile, BrandStage,
    AuditScope, BrandElement, BrandChannel, CrisisSeverity,
    CrisisEvent, CampaignStatus,
)
from datetime import datetime, timezone

# 1. Initialize agent
agent = BrandManagementAgent()

# 2. Register the brand
brand = BrandProfile(
    brand_id="nova_tech",
    name="NovaTech Solutions",
    founded_year=2020,
    industry="technology",
    stage=BrandStage.GROWTH,
    mission="Empowering businesses through intelligent automation",
    vision="A world where technology amplifies human potential",
    values=["innovation", "integrity", "customer_success"],
    target_audience=["enterprise", "mid_market"],
    positioning_statement="The intelligent automation platform",
    unique_value_proposition="AI that adapts to your business",
    brand_archetype="The Creator",
    primary_channels=[
        BrandChannel.WEBSITE,
        BrandChannel.SOCIAL_LINKEDIN,
        BrandChannel.EMAIL,
    ],
    headquarters="San Francisco, CA",
    employee_count=150,
    annual_revenue=20_000_000.0,
    market_share=0.03,
    brand_colors={"primary": "#1A73E8", "secondary": "#34A853"},
    typography={"primary": "Inter", "secondary": "Merriweather"},
    brand_voice_attributes=["confident", "approachable", "clear"],
)
agent.register_brand(brand)

# 3. Run initial brand audit
audit = agent.brand_audit("nova_tech", AuditScope.FULL)
print(f"Initial Audit Score: {audit.overall_score:.1f} ({audit.grade()})")

# 4. Create brand guidelines
guidelines = agent.create_guidelines("nova_tech", [
    BrandElement.LOGO,
    BrandElement.COLOR,
    BrandElement.TYPOGRAPHY,
    BrandElement.VOICE,
])
print(f"Created {len(guidelines)} brand guidelines")

# 5. Monitor sentiment
sentiment = agent.monitor_sentiment("nova_tech")
print(f"Brand Sentiment: {sentiment.overall_level.label}")

# 6. Analyze competitors
competitors = agent.analyze_competitors("nova_tech", ["comp_a", "comp_b", "comp_c"])
print(f"Competitors analyzed: {len(competitors)}")

# 7. Measure brand equity
equity = agent.measure_brand_equity("nova_tech")
print(f"Brand Equity: {equity.overall_equity:.1f}/100")

# 8. Create campaign
campaign = agent.create_campaign_brief(
    "nova_tech",
    ["Increase awareness by 30%", "Generate 2000 MQLs"],
    budget=150000.0,
)
print(f"Campaign created: {campaign.name}")

# 9. Segment audience
segments = agent.segment_audience("nova_tech")
print(f"Audience segments: {len(segments)}")

# 10. Track brand consistency
consistency = agent.track_brand_consistency("nova_tech")
print(f"Brand consistency: {consistency['grade']}")

# 11. Generate stakeholder brief
brief = agent.generate_stakeholder_brief("nova_tech", "executive")
print(f"Executive brief: {brief.title}")

# 12. Handle potential crisis
crisis = CrisisEvent(
    event_id="crisis_test",
    brand_id="nova_tech",
    title="Social Media Backlash",
    description="Negative viral post about product pricing",
    severity=Criseseverity.MEDIUM,
    source="twitter_user",
    channel=BrandChannel.SOCIAL_TWITTER,
    discovered_at=datetime.now(timezone.utc),
    trigger_event="Viral tweet with 50K impressions",
    affected_stakeholders=["customers", "prospects"],
    estimated_reach=50000,
    velocity=0.5,
    current_sentiment=-0.35,
)
response_plan = agent.handle_crisis(crisis)
print(f"Crisis response plan: {response_plan.plan_id} (Tier {response_plan.tier})")

# 13. Export all data
export_data = agent.export_brand_data("nova_tech")
print(f"\nExported data summary:")
for key, value in export_data.items():
    if key != "brand_profile":
        print(f"  {key}: {value}")

print("\nWalkthrough complete!")
```

---

## Best Practices

### Brand Management

1. **Audit Regularly**: Run brand audits quarterly to track health trends
2. **Maintain Guidelines**: Keep brand guidelines current and enforce compliance
3. **Monitor Continuously**: Set up sentiment monitoring with appropriate alert thresholds
4. **Document Everything**: Use event logging for audit trails
5. **Measure Equity**: Track brand equity using established frameworks (Keller's Model)

### Crisis Management

1. **Prepare in Advance**: Run crisis simulations regularly
2. **Classify Quickly**: Accurate severity classification drives appropriate response
3. **Communicate Transparently**: Lead with empathy and accountability
4. **Monitor Velocity**: Track crisis speed to anticipate escalation
5. **Learn Post-Crisis**: Document lessons learned and update protocols

### Competitive Intelligence

1. **Classify Competitors**: Use tier system to prioritize analysis depth
2. **Track Moves**: Monitor competitor product launches, pricing, and positioning
3. **Find Whitespace**: Look for underserved market segments
4. **Benchmark Regularly**: Compare brand metrics against competitors
5. **Anticipate Threats**: Monitor emerging competitors and disruptors

### Campaign Management

1. **Set Clear KPIs**: Define measurable targets before launch
2. **Track Continuously**: Monitor performance daily during active campaigns
3. **Optimize in Flight**: Adjust strategy based on real-time data
4. **Calculate True ROI**: Include brand lift alongside direct conversions
5. **Document Learnings**: Capture insights for future campaigns

---

## Troubleshooting & FAQ

### Common Questions

**Q: How do I handle multiple brands?**
A: Register each brand separately with a unique `brand_id`. All operations accept `brand_id` as the first parameter, so you can manage multiple brands in a single agent instance.

**Q: Can I customize the audit scoring?**
A: Yes. The `_score_dimension` method can be overridden in a subclass to implement custom scoring logic. The `AuditScope` enum controls which dimensions are evaluated.

**Q: How do I integrate with external data sources?**
A: The agent accepts data through its public API methods. For sentiment monitoring, feed data through the `monitor_sentiment` method. For competitive intelligence, provide competitor IDs to `analyze_competitors`.

**Q: What happens during a crisis?**
A: The `handle_crisis` method generates a complete response plan including team assembly, communication strategy, stakeholder matrix, messaging framework, monitoring plan, and escalation triggers. The plan is tailored to the crisis severity level.

**Q: How accurate is the sentiment analysis?**
A: The agent provides confidence scores for all sentiment analyses. Use the `confidence_score` field to assess reliability. For critical decisions, validate automated sentiment with human review.

### Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Brand not found | Brand not registered | Call `register_brand()` first |
| Audit score seems random | Built-in variance for realism | Run multiple audits, average results |
| Crisis plan too aggressive | High severity classification | Review CrisisSeverity enum usage |
| Low equity scores | Brand is new/immature | Expected for early-stage brands |
| Guidelines expired | Review date passed | Call `create_guidelines()` to refresh |
| Campaign ROI negative | Spend exceeds revenue | Normal for awareness campaigns |

### Error Handling

```python
try:
    audit = agent.brand_audit("nonexistent_brand")
except ValueError as e:
    print(f"Error: {e}")  # Brand 'nonexistent_brand' not found

try:
    plan = agent.handle_crisis(crisis)
except Exception as e:
    print(f"Crisis handling failed: {e}")
```

---

## Contributing

### Development Setup

```bash
# Clone the repository
git clone https://github.com/your-org/brand-management-agent.git

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/

# Run type checking
mypy agent.py

# Run linter
ruff check agent.py
```

### Code Standards

- **Type Hints**: All public methods must have complete type annotations
- **Docstrings**: All public methods must have docstrings
- **Testing**: All new features must include tests
- **Logging**: Use the `logger` instance for all operational logging
- **Error Handling**: Use descriptive error messages

### Adding New Features

1. Define data models as dataclasses with type hints
2. Add enums for categorical data
3. Implement methods in `BrandManagementAgent`
4. Add logging for all significant operations
5. Write tests covering the new functionality
6. Update documentation

---

## License

MIT License

Copyright (c) 2026 MiMoCode Agent Framework

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

*Brand Management Agent v2.0.0 — Built with Python, powered by data.*

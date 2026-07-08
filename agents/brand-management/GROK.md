---
name: brand-management
version: 2.0.0
description: >
  Enterprise-grade brand lifecycle management agent implementing brand auditing,
  sentiment monitoring, crisis response, competitive intelligence, campaign tracking,
  audience segmentation, and reputation management using industry-standard frameworks
  (Keller's Brand Equity Model, Brand Asset Valuator, NPS methodology, and crisis
  communication best practices).
author: MiMoCode Agent Framework
tags:
  - brand-management
  - sentiment-analysis
  - crisis-management
  - competitive-intelligence
  - campaign-performance
  - reputation-management
  - brand-equity
  - audience-segmentation
  - brand-audit
  - brand-guidelines
category: Marketing & Brand Operations
personality:
  analytical: 0.9
  strategic: 0.85
  detail_oriented: 0.95
  proactive: 0.8
  authoritative: 0.85
use_cases:
  - Comprehensive brand audits and health assessments
  - Real-time sentiment monitoring across channels
  - Crisis detection, response planning, and execution
  - Competitive positioning and intelligence analysis
  - Campaign performance tracking and ROI measurement
  - Audience segmentation and persona development
  - Brand guideline creation and compliance monitoring
  - Reputation tracking and stakeholder reporting
  - Brand equity measurement using Keller's pyramid
  - Partnership evaluation and management
---

# Brand Management Agent v2.0

## Agent Identity

The Brand Management Agent is a comprehensive brand lifecycle management system designed for enterprise-grade brand operations. It combines analytical rigor with practical brand management workflows, implementing industry-standard frameworks for measurable, defensible brand decisions.

**Core Philosophy:** Every brand decision should be data-driven, every crisis should have a plan, and every touchpoint should be consistent with brand identity.

---

## 10 Core Principles

### 1. Data-Driven Brand Decisions
Every recommendation, strategy, and response must be grounded in measurable data. Gut feelings are hypotheses waiting to be validated.

### 2. Proactive Brand Governance
Don't wait for crises — monitor, predict, and prevent. Brand health degrades silently before it becomes visible.

### 3. Consistency Across Touchpoints
Brand identity must be maintained with precision across every channel, every interaction, every time. Inconsistency is brand erosion.

### 4. Stakeholder-Centric Communication
Every crisis response, campaign brief, and stakeholder report should be tailored to its audience. One size fits none.

### 5. Competitive Awareness
Know your competitive landscape intimately. Opportunities are found in the gaps competitors leave; threats emerge from moves they make.

### 6. Measurable Brand Equity
Brand value must be quantified. Use established frameworks (Keller's Model, NPS, Brand Asset Valuator) to create comparable, trackable metrics.

### 7. Rapid Crisis Response
Speed matters in crisis management. The first 4 hours determine the trajectory of brand perception during a crisis.

### 8. Audience Intelligence
Deeply understand your audience segments. Different segments require different messages, channels, and value propositions.

### 9. Continuous Improvement
Brand management is iterative. Measure, learn, optimize, repeat. Every campaign, crisis, and audit provides data for the next cycle.

### 10. Ethical Brand Stewardship
Build brands with integrity. Short-term gains from deceptive practices destroy long-term brand equity.

---

## Detailed Capabilities

### 1. Brand Audit Engine

Comprehensive brand audit scoring across 10 dimensions with automated SWOT analysis and prioritized recommendations.

```python
# Execute a full brand audit
audit = agent.brand_audit("brand_id", AuditScope.FULL)

# Key outputs
print(f"Overall Score: {audit.overall_score}/100 (Grade: {audit.grade()})")
print(f"Compliance: {audit.compliance_score}%")
print(f"Consistency: {audit.consistency_score}%")

# Access prioritized recommendations
for rec in audit.priority_actions()[:5]:
    print(f"[Priority {rec['priority']}] {rec['dimension']}")
    print(f"  Current: {rec['current_score']:.1f} -> Target: {rec['target_score']:.1f}")
    print(f"  Actions: {rec['action_items']}")
```

**Audit Dimensions:**
| Dimension | Weight | Description |
|-----------|--------|-------------|
| Visual Identity | 15% | Logo, color, typography compliance |
| Verbal Identity | 12% | Voice, messaging, tone consistency |
| Digital Presence | 13% | Website, social, app brand alignment |
| Customer Perception | 14% | How customers perceive the brand |
| Competitive Positioning | 12% | Market position vs competitors |
| Channel Consistency | 10% | Brand alignment across channels |
| Employee Alignment | 8% | Internal brand understanding |
| Market Performance | 8% | Business metrics tied to brand |
| Innovation | 5% | Brand perception as innovative |
| Cultural Relevance | 3% | Alignment with cultural trends |

### 2. Sentiment Monitoring

Real-time sentiment analysis across all brand channels with trend detection and alert generation.

```python
# Monitor sentiment across channels
sentiment = agent.monitor_sentiment("brand_id", [
    BrandChannel.SOCIAL_TWITTER,
    BrandChannel.SOCIAL_INSTAGRAM,
    BrandChannel.WEBSITE,
])

# Analyze results
print(f"Overall Sentiment: {sentiment.overall_score:.3f} ({sentiment.overall_level.label})")
print(f"Volume: {sentiment.volume:,} mentions")
print(f"Share of Voice: {sentiment.share_of_voice:.1%}")
print(f"Alerts: {sentiment.alert_count()}")

# Check trending
if sentiment.is_trending_positive():
    print("Sentiment is trending positive!")
elif sentiment.sentiment_delta() < -0.1:
    print("WARNING: Significant sentiment decline detected")
```

**Sentiment Classification:**
| Score Range | Level | Action |
|-------------|-------|--------|
| 0.6 to 1.0 | Very Positive | Amplify advocacy |
| 0.2 to 0.6 | Positive | Maintain momentum |
| -0.2 to 0.2 | Neutral | Increase engagement |
| -0.6 to -0.2 | Negative | Investigate causes |
| -1.0 to -0.6 | Very Negative | Activate crisis response |

### 3. Crisis Management System

Automated crisis detection, severity classification, and response plan generation with escalation tiers.

```python
# Handle a crisis event
crisis = CrisisEvent(
    event_id="crisis_001",
    brand_id="brand_id",
    title="Data Security Incident",
    description="Potential vulnerability disclosed",
    severity=CrisisSeverity.HIGH,
    source="security_researcher",
    channel=BrandChannel.SOCIAL_TWITTER,
    discovered_at=datetime.now(timezone.utc),
    trigger_event="Security disclosure email",
    affected_stakeholders=["customers", "employees", "regulators"],
    estimated_reach=250000,
    velocity=0.7,
    current_sentiment=-0.45,
)

plan = agent.handle_crisis(crisis)
print(f"Response Plan: {plan.plan_id}")
print(f"Escalation Tier: {plan.tier}")
print(f"Team Size: {len(plan.response_team)}")
print(f"Immediate Actions: {len(plan.immediate_actions)}")

# Run crisis simulation
sim_plan = agent.simulate_crisis("data_breach", "brand_id")
```

**Crisis Severity Tiers:**
| Severity | Response Time | Escalation | Executive | Legal |
|----------|--------------|------------|-----------|-------|
| LOW | 72 hours | Tier 1 | No | No |
| MEDIUM | 24 hours | Tier 2 | No | No |
| HIGH | 4 hours | Tier 3 | Yes | No |
| CRITICAL | 1 hour | Tier 4 | Yes | Yes |
| CATASTROPHIC | 15 minutes | Tier 5 | Yes | Yes |

### 4. Competitive Intelligence

Comprehensive competitive positioning analysis with SWOT, threat scoring, and whitespace identification.

```python
# Analyze competitors
analyses = agent.analyze_competitors("brand_id", [
    "competitor_alpha", "competitor_beta", "competitor_gamma"
])

for comp in analyses:
    print(f"{comp.competitor_name} ({comp.tier.value})")
    print(f"  Market Share: {comp.market_share:.1%}")
    print(f"  Threat Score: {comp.threat_score():.1f}")
    print(f"  Strengths: {', '.join(comp.strengths[:3])}")

# Generate positioning map
positioning = agent.competitive_positioning("brand_id")
for opp in positioning["whitespace_opportunities"]:
    print(f"  Opportunity: {opp}")
```

### 5. Brand Equity Measurement

Keller's Brand Equity Model implementation measuring all six pyramid levels.

```python
equity = agent.measure_brand_equity("brand_id")

print(f"Overall Equity: {equity.overall_equity:.1f}/100")
print(f"Trend: {equity.equity_trend()}")
print(f"Pyramid Completeness: {equity.pyramid_completeness():.1f}%")

# Keller's Pyramid Levels
print(f"Salience:     {equity.brand_salience:.1f}")
print(f"Performance:  {equity.performance_assessment:.1f}")
print(f"Imagery:      {equity.imagery_assessment:.1f}")
print(f"Judgments:    {equity.judgments:.1f}")
print(f"Feelings:     {equity.feelings:.1f}")
print(f"Resonance:    {equity.resonance:.1f}")
```

### 6. Campaign Performance Tracking

Full campaign lifecycle management with KPI tracking and ROI analysis.

```python
# Create campaign brief
campaign = agent.create_campaign_brief(
    "brand_id",
    ["Increase brand awareness by 25%", "Generate 5000 MQLs"],
    budget=250000.0,
)

# Track performance
perf = agent.track_campaign_performance(campaign.campaign_id)
print(f"ROI: {perf['roi']:.1f}%")
print(f"Conversion Rate: {perf['conversion_rate']:.2f}%")
print(f"Budget Utilization: {perf['budget_utilization']:.1f}%")

# KPI status
for kpi, status in perf["kpi_status"].items():
    print(f"  {kpi}: {status['progress']:.0f}% ({status['status']})")
```

### 7. Audience Segmentation

Multi-dimensional audience segmentation with health classification and LTV analysis.

```python
segments = agent.segment_audience("brand_id")

for seg in segments:
    print(f"{seg.name}:")
    print(f"  Size: {seg.size:,} | LTV: ${seg.lifetime_value:,.0f}")
    print(f"  Health: {seg.segment_health()}")
    print(f"  LTV/CAC Ratio: {seg.ltv_to_cac_ratio():.1f}x")
    print(f"  Churn Risk: {seg.churn_risk:.0%}")

# Get segment-specific insights
insights = agent.get_segment_insights("brand_id", segments[0].segment_id)
print(f"Retention Strategy: {insights['retention_strategy']}")
```

**Segment Health Classification:**
| Classification | Criteria | Strategy |
|----------------|----------|----------|
| Champion | loyalty > 0.8 | Loyalty rewards, referral programs |
| Advocate | sentiment > 0.6 | Amplification, UGC campaigns |
| Stable | default | Engagement, value delivery |
| At Risk | churn_risk > 0.7 | Re-engagement, win-back offers |

### 8. Brand Guidelines Engine

Automated brand guideline generation with compliance monitoring and accessibility validation.

```python
# Create comprehensive guidelines
guidelines = agent.create_guidelines("brand_id", [
    BrandElement.LOGO,
    BrandElement.COLOR,
    BrandElement.TYPOGRAPHY,
    BrandElement.VOICE,
    BrandElement.IMAGERY,
    BrandElement.MESSAGING,
])

for g in guidelines:
    print(f"{g.title}")
    print(f"  Rules: {len(g.rules)}")
    print(f"  Don'ts: {len(g.donts)}")
    print(f"  Expires in: {g.days_until_review()} days")
    print(f"  Accessibility: {g.accessibility_notes}")

# Check expiring guidelines
expiring = agent.get_expiring_guidelines("brand_id", within_days=30)
print(f"Guidelines expiring soon: {len(expiring)}")
```

### 9. Reputation Management

Cross-source reputation tracking with composite scoring and trend analysis.

```python
reputation = agent.manage_reputation("brand_id")

print(f"Overall Score: {reputation.overall_score:.1f}/100")
print(f"Trend: {reputation.trend_direction}")
print(f"Trust Index: {reputation.trust_index:.1f}")
print(f"Crisis Resilience: {reputation.crisis_resilience_score:.1f}")

# Source breakdown
for source, score in reputation.source_scores.items():
    print(f"  {source}: {score:.1f}")
```

### 10. Stakeholder Briefing

Executive-ready stakeholder reports with key metrics, highlights, and recommended actions.

```python
brief = agent.generate_stakeholder_brief("brand_id", "executive")

print(f"Brief: {brief.title}")
print(f"Key Metrics:")
for metric, value in brief.key_metrics.items():
    print(f"  {metric}: {value:.1f}")
print(f"Highlights:")
for h in brief.highlights:
    print(f"  + {h}")
print(f"Concerns:")
for c in brief.concerns:
    print(f"  - {c}")
```

---

## Operational Guidelines

### When to Use Each Capability

| Situation | Capability | Priority |
|-----------|-----------|----------|
| Starting brand management program | Brand Audit | High |
| Negative mentions spike | Sentiment Monitoring | Critical |
| Viral crisis emerging | Crisis Management | Critical |
| Quarterly business review | Stakeholder Brief | High |
| New product launch | Campaign Brief | High |
| Entering new market | Competitive Analysis | Medium |
| Optimizing marketing spend | Audience Segmentation | Medium |
| Brand refresh/rebrand | Brand Guidelines | High |
| Measuring brand ROI | Brand Equity | Medium |
| Partnership evaluation | Partnership Management | Medium |

### Method Signatures

```python
# Core Operations
brand_audit(brand_id: str, scope: AuditScope = AuditScope.FULL) -> BrandAuditResult
create_guidelines(brand_id: str, elements: List[BrandElement]) -> List[BrandGuideline]
monitor_sentiment(brand_id: str, channels: Optional[List[BrandChannel]] = None) -> SentimentReport
handle_crisis(crisis_event: CrisisEvent) -> CrisisResponsePlan
analyze_competitors(brand_id: str, competitor_ids: List[str]) -> List[CompetitorAnalysis]
measure_brand_equity(brand_id: str) -> BrandEquityScore
manage_reputation(brand_id: str, source: Optional[ReputationSource] = None) -> ReputationMetrics
create_campaign_brief(brand_id: str, objectives: List[str], budget: float = 100000.0) -> CampaignPerformance
segment_audience(brand_id: str) -> List[AudienceSegment]
generate_brand_health_report(brand_id: str) -> BrandHealthDashboard
track_brand_consistency(brand_id: str) -> Dict[str, Any]
manage_brand_partnerships(brand_id: str) -> Dict[str, Any]
competitive_positioning(brand_id: str) -> Dict[str, Any]
simulate_crisis(crisis_type: str, brand_id: Optional[str] = None) -> CrisisResponsePlan
generate_stakeholder_brief(brand_id: str, audience: str = "executive") -> StakeholderBrief

# Utility Operations
register_brand(profile: BrandProfile) -> str
get_brand_profile(brand_id: str) -> BrandProfile
update_brand_profile(brand_id: str, updates: Dict[str, Any]) -> BrandProfile
get_guidelines(brand_id: str) -> List[BrandGuideline]
get_sentiment_trend(brand_id: str, periods: int = 12) -> List[Tuple[datetime, float]]
get_active_crises() -> List[CrisisEvent]
resolve_crisis(event_id: str, resolution_notes: str = "") -> CrisisEvent
track_campaign_performance(campaign_id: str) -> Dict[str, Any]
get_campaign_summary(brand_id: str) -> Dict[str, Any]
get_segment_insights(brand_id: str, segment_id: str) -> Dict[str, Any]
export_brand_data(brand_id: str) -> Dict[str, Any]
get_event_log(brand_id: Optional[str] = None, event_type: Optional[str] = None, limit: int = 50) -> List[Dict[str, Any]]
```

---

## Data Models

### BrandProfile
| Field | Type | Description |
|-------|------|-------------|
| brand_id | str | Unique brand identifier |
| name | str | Brand name |
| founded_year | int | Year brand was founded |
| industry | str | Industry classification |
| stage | BrandStage | Current lifecycle stage |
| mission | str | Brand mission statement |
| vision | str | Brand vision statement |
| values | List[str] | Core brand values |
| target_audience | List[str] | Target audience segments |
| positioning_statement | str | Brand positioning |
| unique_value_proposition | str | UVP |
| brand_archetype | str | Brand personality archetype |
| primary_channels | List[BrandChannel] | Primary brand channels |
| brand_colors | Dict[str, str] | Brand color palette |
| typography | Dict[str, str] | Font specifications |
| brand_voice_attributes | List[str] | Voice characteristics |

### SentimentReport
| Field | Type | Description |
|-------|------|-------------|
| report_id | str | Unique report identifier |
| overall_score | float | Sentiment score (-1.0 to 1.0) |
| overall_level | SentimentLevel | Classified sentiment level |
| volume | int | Total mention volume |
| channel_breakdown | Dict | Per-channel sentiment data |
| trending_topics | List | Topics driving sentiment |
| sentiment_trend | List | Historical trend data |
| share_of_voice | float | Market share of voice |
| alerts | List | Active alerts |

### CrisisEvent
| Field | Type | Description |
|-------|------|-------------|
| event_id | str | Unique event identifier |
| severity | CrisisSeverity | Crisis severity level |
| source | str | Crisis source/trigger |
| estimated_reach | int | Estimated audience reach |
| velocity | float | Crisis velocity (0-1) |
| current_sentiment | float | Current sentiment impact |
| affected_stakeholders | List[str] | Stakeholder groups impacted |

### BrandEquityScore
| Field | Type | Description |
|-------|------|-------------|
| overall_equity | float | Combined equity score |
| brand_salience | float | Awareness and recognition |
| performance_assessment | float | Product/service quality perception |
| imagery_assessment | float | Brand image and associations |
| judgments | float | Customer quality/credibility judgments |
| feelings | float | Emotional brand connections |
| resonance | float | Customer-brand relationship depth |

### CompetitorAnalysis
| Field | Type | Description |
|-------|------|-------------|
| competitor_name | str | Competitor identifier |
| tier | CompetitorTier | Threat classification tier |
| market_share | float | Estimated market share |
| strengths | List[str] | Key competitive strengths |
| weaknesses | List[str] | Key competitive weaknesses |
| positioning | str | Competitive positioning statement |
| threat_score | float | Composite threat rating |

### CampaignPerformance
| Field | Type | Description |
|-------|------|-------------|
| campaign_id | str | Unique campaign identifier |
| campaign_name | str | Campaign name |
| status | CampaignStatus | Current campaign status |
| budget | float | Total campaign budget |
| spend | float | Amount spent to date |
| kpis | Dict[str, float] | Key performance indicators |
| roi | float | Return on investment percentage |
| conversion_rate | float | Conversion rate percentage |

### AudienceSegment
| Field | Type | Description |
|-------|------|-------------|
| segment_id | str | Unique segment identifier |
| name | str | Segment name |
| size | int | Number of people in segment |
| demographics | Dict[str, Any] | Demographic breakdown |
| behaviors | List[str] | Key behavioral patterns |
| loyalty_score | float | Segment loyalty (0-1) |
| churn_risk | float | Churn probability (0-1) |
| lifetime_value | float | Average LTV in USD |
| cac | float | Customer acquisition cost |

### ReputationMetrics
| Field | Type | Description |
|-------|------|-------------|
| overall_score | float | Composite reputation score (0-100) |
| trust_index | float | Trust measurement (0-100) |
| crisis_resilience_score | float | Recovery capability rating |
| trend_direction | str | Overall trend direction |
| source_scores | Dict[str, float] | Per-source reputation scores |

---

## Checklists

### Brand Audit Checklist
- [ ] Brand profile is complete and current
- [ ] All brand elements are defined
- [ ] Audit scope is clearly specified
- [ ] Benchmark data is available
- [ ] Historical audit data exists for comparison
- [ ] Stakeholder expectations are aligned
- [ ] Resource allocation is approved

### Crisis Response Checklist
- [ ] Crisis event is properly classified
- [ ] Response team is assembled
- [ ] Initial holding statement is prepared
- [ ] Stakeholder notifications are sent
- [ ] Monitoring is activated
- [ ] Legal review is initiated (if required)
- [ ] Executive briefing is conducted
- [ ] Communication channels are confirmed
- [ ] Escalation triggers are defined
- [ ] Post-crisis review is scheduled

### Campaign Launch Checklist
- [ ] Campaign brief is approved
- [ ] KPI targets are set
- [ ] Budget is allocated
- [ ] Creative assets are approved
- [ ] Channel strategy is confirmed
- [ ] Tracking is configured
- [ ] Team roles are assigned
- [ ] Timeline is finalized
- [ ] Risk mitigation plan is in place
- [ ] Post-campaign analysis plan is ready

### Brand Guideline Compliance Checklist
- [ ] All guidelines are current (not expired)
- [ ] Accessibility requirements are documented
- [ ] Cross-platform adaptations are specified
- [ ] Local variant rules are defined
- [ ] Approval workflow is established
- [ ] Training materials are available
- [ ] Monitoring tools are configured
- [ ] Violation remediation process is defined

### Competitive Intelligence Checklist
- [ ] Competitor landscape is mapped
- [ ] Market share data is current
- [ ] SWOT analysis completed for each competitor
- [ ] Threat scores are calculated
- [ ] Whitespace opportunities identified
- [ ] Positioning map generated
- [ ] Strategic implications documented
- [ ] Monitoring alerts configured

---

## Troubleshooting Guide

### Common Issues

**Issue: Audit scores seem inconsistent between runs**
- Cause: Random variation in simulated scoring
- Resolution: Run multiple audits and average results; compare relative rankings rather than absolute scores
- Prevention: Use fixed random seeds for reproducibility in testing

**Issue: Crisis response plan doesn't match severity**
- Cause: Severity classification may not account for all factors
- Resolution: Manually adjust severity based on reach, velocity, and stakeholder impact
- Prevention: Use the full CrisisEvent data model with all impact factors

**Issue: Sentiment scores don't match manual analysis**
- Cause: Automated sentiment analysis has inherent limitations
- Resolution: Use sentiment as a directional indicator, not absolute truth; validate with human review
- Prevention: Combine automated analysis with periodic manual audits

**Issue: Campaign ROI seems too high/low**
- Cause: Attribution model may not capture full impact
- Resolution: Use multi-touch attribution; consider brand lift beyond direct conversions
- Prevention: Define clear attribution rules before campaign launch

**Issue: Audience segments overlap significantly**
- Cause: Segmentation dimensions may not be sufficiently discriminative
- Resolution: Review segment criteria; consider behavioral data over demographics
- Prevention: Validate segments with statistical testing before deployment

**Issue: Brand guidelines are not being followed**
- Cause: Guidelines may not be accessible or enforceable
- Resolution: Implement automated compliance checking; integrate into design tools
- Prevention: Make guidelines part of the creation workflow, not a separate step

### Performance Optimization

| Symptom | Diagnosis | Solution |
|---------|-----------|----------|
| Slow audit execution | Large brand profile | Optimize data loading; cache common queries |
| High memory usage | Too many concurrent analyses | Limit parallel operations; use streaming |
| Stale sentiment data | Ingestion pipeline lag | Check queue depth; scale workers |
| Missing crisis alerts | Alert threshold too strict | Review and adjust detection thresholds |
| Low cache hit ratio | Cache TTL too short | Increase TTL; review access patterns |
| Duplicate brand entries | Registration race condition | Use idempotency keys on registration |
| Stale competitor data | No automatic refresh | Schedule periodic competitor re-analysis |

---

## Usage Patterns

### Pattern 1: Brand Health Monitoring Workflow
```python
# Daily brand health check
dashboard = agent.generate_brand_health_report("brand_id")
sentiment = agent.monitor_sentiment("brand_id")
reputation = agent.manage_reputation("brand_id")

# Generate executive summary
brief = agent.generate_stakeholder_brief("brand_id", "executive")
```

### Pattern 2: Crisis Response Workflow
```python
# Detect and respond to crisis
crisis = CrisisEvent(...)  # From detection system
plan = agent.handle_crisis(crisis)

# Monitor resolution
while not crisis.is_resolved:
    sentiment = agent.monitor_sentiment(crisis.brand_id)
    if sentiment.overall_score > -0.2:
        agent.resolve_crisis(crisis.event_id, "Sentiment normalized")
```

### Pattern 3: Competitive Strategy Development
```python
# Full competitive analysis
competitors = agent.analyze_competitors("brand_id", competitor_ids)
positioning = agent.competitive_positioning("brand_id")
equity = agent.measure_brand_equity("brand_id")

# Develop strategy
for opp in positioning["whitespace_opportunities"]:
    print(f"Pursue: {opp}")
```

### Pattern 4: Campaign Optimization Loop
```python
# Create and monitor campaign
campaign = agent.create_campaign_brief("brand_id", objectives, budget)

# Track and optimize
for _ in range(30):  # 30-day campaign
    perf = agent.track_campaign_performance(campaign.campaign_id)
    if perf["kpi_status"]["conversion_rate"]["status"] == "behind":
        # Adjust strategy
        pass
```

### Pattern 5: Brand Refresh Workflow
```python
# Assess current state
audit = agent.brand_audit("brand_id", AuditScope.FULL)
equity = agent.measure_brand_equity("brand_id")

# Create new guidelines
guidelines = agent.create_guidelines("brand_id", [
    BrandElement.LOGO, BrandElement.COLOR,
    BrandElement.TYPOGRAPHY, BrandElement.VOICE,
])

# Track consistency post-refresh
consistency = agent.track_brand_consistency("brand_id")
```

---

## Integration Patterns

### Social Media Integration
```python
# Configure social monitoring channels
agent.configure_social_integration("brand_id", {
    "twitter": {"api_key": "...", "track_keywords": ["@brand", "#brand"]},
    "instagram": {"api_key": "...", "track_hashtags": ["#brand"]},
    "linkedin": {"api_key": "...", "monitor_mentions": True},
})
```

### Analytics Platform Integration
```python
# Connect to analytics platforms
agent.connect_analytics("brand_id", {
    "google_analytics": {"property_id": "..."},
    "mixpanel": {"project_token": "..."},
    "segment": {"write_key": "..."},
})
```

### CRM Integration
```python
# Sync customer data from CRM
agent.sync_crm_data("brand_id", {
    "salesforce": {"instance_url": "...", "object_types": ["Account", "Contact"]},
    "hubspot": {"portal_id": "...", "properties": ["hs_lead_status"]},
})
```

---

## Advanced Configuration

### Custom Audit Dimensions
```python
# Define custom audit dimensions beyond the default 10
agent.add_custom_dimension("brand_id", {
    "name": "Sustainability",
    "weight": 0.10,
    "sub_dimensions": ["Environmental Impact", "Social Responsibility", "Governance"],
    "scoring_method": "survey",
})
```

### Sentiment Thresholds
```python
# Customize sentiment alert thresholds
agent.configure_sentiment_thresholds("brand_id", {
    "negative_alert": -0.3,
    "crisis_threshold": -0.6,
    "volume_spike_multiplier": 3.0,
    "velocity_alert": 0.7,
})
```

### Crisis Playbooks
```python
# Define custom crisis response playbooks
agent.create_crisis_playbook("brand_id", "product_recall", {
    "immediate": [
        "Issue holding statement within 1 hour",
        "Activate product safety team",
        "Notify regulatory bodies",
    ],
    "short_term": [
        "Launch dedicated recall page",
        "Begin customer outreach",
        "Prepare FAQ document",
    ],
    "long_term": [
        "Conduct root cause analysis",
        "Implement prevention measures",
        "Launch trust rebuilding campaign",
    ],
})
```

---

## Glossary

| Term | Definition |
|------|-----------|
| Brand Equity | The commercial value derived from consumer perception of the brand |
| Share of Voice | Brand's advertising percentage compared to total market advertising |
| NPS | Net Promoter Score — measures customer loyalty on a -100 to +100 scale |
| SOV | Share of Voice — brand visibility relative to competitors |
| SOV/SOM Ratio | Share of Voice to Share of Market ratio for growth prediction |
| Brand Archetype | Universal character type (Hero, Explorer, Sage, etc.) that defines brand personality |
| Crisis Velocity | Speed at which a crisis is spreading across channels |
| Resonance | Depth of customer-brand relationship in Keller's Model |
| Salience | Brand awareness and recall strength |
| LTV | Lifetime Value — total revenue expected from a customer relationship |

---

## Methodology Reference

### Keller's Brand Equity Pyramid (Detailed)

```
                    ┌─────────────────┐
                    │    RESONANCE    │  ← Relationship depth
                    │  (Loyalty,      │
                    │   Attachment,   │
                    │   Community,    │
                    │   Engagement)   │
                    ├─────────────────┤
                    │    JUDGMENTS    │  ← Quality, Credibility,
                    │  &   FEELINGS   │    Consideration, Superiority
                    ├─────────────────┤
                    │   PERFORMANCE   │  ← Primary characteristics,
                    │  &   IMAGERY    │    Reliability, Durability
                    ├─────────────────┤
                    │    SALIENCE     │  ← Brand awareness,
                    │                 │    Recall, Recognition
                    └─────────────────┘

Scoring: Each level contributes to the overall equity score.
Weight:  Salience=15%, Performance=20%, Imagery=20%,
         Judgments=20%, Feelings=10%, Resonance=15%
```

### Brand Asset Valuator (BAV) Model

```
Differentiation → Relevance → Esteem → Knowledge

  High Diff + High Rel = Strong brand potential
  High Esteem + High Knowledge = Strong brand equity
  Gap between Esteem and Knowledge = Awareness problem
```

### Crisis Communication Timeline

```
Hour 0-1:    Detection and initial assessment
Hour 1-4:    Holding statement and team assembly
Hour 4-12:   Detailed response preparation
Hour 12-24:  Full stakeholder communication
Day 2-7:     Active monitoring and adjustment
Day 7-30:    Recovery and reputation rebuilding
Day 30-90:   Post-crisis review and prevention
```

### Sentiment Analysis Methodology

```
Input: Raw text mentions
  │
  ├── Text Preprocessing
  │     ├── Tokenization
  │     ├── Stop word removal
  │     ├── Lemmatization
  │     └── Entity recognition
  │
  ├── Sentiment Classification
  │     ├── Lexicon-based scoring
  │     ├── Context-aware analysis
  │     ├── Sarcasm detection
  │     └── Aspect-based sentiment
  │
  └── Aggregation
        ├── Channel-level scores
        ├── Time-series trending
        ├── Volume weighting
        └── Alert generation
```

---

## Best Practices Guide

### Brand Audit Best Practices

1. **Establish baseline before measurement** — Without a baseline, scores are meaningless
2. **Include both internal and external perspectives** — Employee alignment matters as much as customer perception
3. **Benchmark against industry** — Raw scores need context; compare to industry averages
4. **Track longitudinal trends** — Single audit is a snapshot; trends reveal trajectory
5. **Involve cross-functional stakeholders** — Brand is everyone's responsibility

### Sentiment Monitoring Best Practices

1. **Set up keyword monitoring early** — Include brand name, product names, CEO name, common misspellings
2. **Monitor competitor sentiment too** — Competitive context makes your numbers meaningful
3. **Calibrate with manual review** — Automated sentiment needs human calibration quarterly
4. **Account for volume spikes** — A few negative mentions in high-volume periods may not be significant
5. **Track sentiment by segment** — Overall sentiment masks segment-specific issues

### Crisis Management Best Practices

1. **Prepare playbooks before crises happen** — In-crisis decision-making is suboptimal
2. **Designate a single spokesperson** — Multiple voices create confusion
3. **Respond with empathy first, facts second** — People want to know you care before they care what you know
4. **Over-communicate during crisis** — Silence is interpreted as guilt or indifference
5. **Document everything** — Post-crisis review requires detailed records

### Competitive Analysis Best Practices

1. **Analyze at least 3-5 competitors** — Too few misses landscape; too many dilutes focus
2. **Include indirect competitors** — The threat often comes from adjacent spaces
3. **Update quarterly at minimum** — Competitive landscape shifts rapidly
4. **Focus on customer perception, not just features** — Brands compete on meaning, not just functionality
5. **Identify whitespace opportunities** — The most valuable insights come from gaps

### Campaign Performance Best Practices

1. **Define KPIs before launch** — Retrospective KPI selection introduces bias
2. **Use control groups when possible** — Attribution requires comparison
3. **Track leading and lagging indicators** — Don't wait for end-of-campaign to optimize
4. **Account for brand lift beyond direct response** — Awareness campaigns don't generate immediate conversions
5. **Conduct post-mortem for every campaign** — Learning compounds over time

---

## Version History

### v2.0.0 (Current)
- Complete rewrite with full Python implementations
- Added Keller's Brand Equity Model scoring
- Crisis management with 5-tier severity system
- Competitive intelligence with threat scoring
- Audience segmentation with LTV analysis
- Campaign performance tracking with ROI
- Reputation management with composite scoring

### v1.5.0
- Added sentiment monitoring across channels
- Crisis simulation capabilities
- Stakeholder briefing generation

### v1.0.0
- Initial agent implementation
- Brand audit framework
- Basic competitive analysis

---

*Brand Management Agent v2.0.0 — Enterprise-grade brand lifecycle management*

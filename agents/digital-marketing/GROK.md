---
name: "Digital Marketing Agent"
version: "2.0.0"
description: "Full-stack digital marketing platform covering campaign management, multi-channel strategy, paid advertising, email marketing, social media, SEO/SEM, performance analytics, and multi-touch attribution modeling"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["marketing", "campaigns", "seo", "email", "social-media", "attribution", "analytics", "advertising", "paid-search", "digital-strategy"]
category: "business"
personality: "data-driven-strategist"
use_cases:
  - "multi-channel campaign management"
  - "budget allocation optimization"
  - "email marketing automation"
  - "social media scheduling and analytics"
  - "SEO keyword tracking and site auditing"
  - "multi-touch attribution analysis"
  - "performance dashboard generation"
  - "ROI reporting and recommendations"
---

# Digital Marketing Agent

> Comprehensive digital marketing orchestration — campaigns, channels, content, analytics, and attribution in one agent.

## Agent Identity

The Digital Marketing Agent is a data-driven strategist that manages the full
lifecycle of digital marketing operations. From campaign creation through
attribution analysis, it optimizes spend, tracks performance, and delivers
actionable recommendations across every marketing channel.

**Core Personality**: Analytical, objective, optimization-focused. Recommends
based on data, not intuition. Balances short-term conversion with long-term
brand building.

## Core Principles

1. **Data Over Intuition**: Every recommendation is backed by metrics.
2. **Full-Funnel Thinking**: Balance awareness, consideration, and conversion.
3. **Channel Synergy**: Optimize the portfolio, not individual channels.
4. **Attribution Integrity**: Use the right model for the right question.
5. **Continuous Optimization**: Test, measure, iterate, repeat.

## Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                     DigitalMarketingAgent                                  │
│                                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐  │
│  │  Campaign      │  │  Channel       │  │  Performance               │  │
│  │  Manager       │  │  Strategy      │  │  Analytics                 │  │
│  │  ├ Create      │  │  ├ Recommend   │  │  ├ Touchpoints             │  │
│  │  ├ Activate    │  │  ├ Allocate    │  │  ├ Dashboard               │  │
│  │  ├ Pause       │  │  ├ Optimize    │  │  ├ Trends                  │  │
│  │  └ Complete    │  │  └ Score       │  │  └ Alerts                  │  │
│  └────────────────┘  └────────────────┘  └────────────────────────────┘  │
│                                                                          │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────────────────┐  │
│  │  Attribution   │  │  Email         │  │  Social                    │  │
│  │  Engine        │  │  Marketing     │  │  Media                     │  │
│  │  ├ 8 models    │  │  ├ Campaigns   │  │  ├ 10 platforms            │  │
│  │  ├ Compare     │  │  ├ Events      │  │  ├ Engagement              │  │
│  │  ├ Channel     │  │  ├ Metrics     │  │  ├ Analytics               │  │
│  │  └ Customer    │  │  └ ROI         │  │  └ Scheduling              │  │
│  └────────────────┘  └────────────────┘  └────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐│
│  │  SEO Manager                                                         ││
│  │  ├ Keywords  │ Rankings  │ Audits  │ Scorecard  │ Recommendations   ││
│  └──────────────────────────────────────────────────────────────────────┘│
└──────────────────────────────────────────────────────────────────────────┘
```

## Capabilities

### 1. Campaign Lifecycle Management

```python
from agents.digital_marketing.agent import (
    DigitalMarketingAgent, ObjectiveType, ChannelType, CampaignStatus
)

agent = DigitalMarketingAgent()

# Create a full campaign with strategy
result = agent.create_full_campaign(
    name="Black Friday 2025",
    objective=ObjectiveType.CONVERSION,
    channels=[ChannelType.PAID_SEARCH, ChannelType.EMAIL, ChannelType.DISPLAY],
    budget=100000,
    audience=AudienceDefinition(
        segment=AudienceSegment.HIGH_VALUE,
        demographics={"age_range": "25-54", "income": "high"},
        interests=["technology", "fashion", "home_goods"],
        geo_targets=["US", "CA"],
    ),
)
# Returns: {"campaign": {...}, "strategy": {...}}
```

**Campaign States:**

```
  ┌────────┐     ┌──────────┐     ┌────────┐
  │ DRAFT  │────►│ SCHEDULED│────►│ ACTIVE │
  └────────┘     └──────────┘     └────────┘
                                      │
                              ┌───────┴───────┐
                              ▼               ▼
                        ┌────────┐      ┌──────────┐
                        │ PAUSED │      │COMPLETED │
                        └────────┘      └──────────┘
                                            │
                                            ▼
                                      ┌──────────┐
                                      │ ARCHIVED │
                                      └──────────┘
```

### 2. Multi-Channel Strategy

```python
engine = ChannelStrategyEngine()

strategy = engine.develop_strategy(
    objective=ObjectiveType.AWARENESS,
    total_budget=50000,
    target_audience=audience,
)

# Get channel recommendations with fit scores
recs = engine.get_channel_recommendations(
    objective=ObjectiveType.CONVERSION,
    audience=audience,
    budget=50000,
)
# Returns ranked channels with estimated CPC, CPM, daily clicks, fit_score
```

**Channels Supported:**

| Category | Channels |
|----------|---------|
| Paid | Paid Search, Paid Social, Display, Video, Native |
| Organic | Organic Search, Social Organic, Content |
| Direct | Email, SMS, Push Notification |
| Partnership | Affiliate, Influencer, Event, Direct Mail |

**Channel Fit Matrix:**

```
┌─────────────────┬────────────┬────────────┬────────────┬────────────┐
│  Channel        │ Awareness  │ Consider   │ Conversion │ Retention  │
├─────────────────┼────────────┼────────────┼────────────┼────────────┤
│  Paid Search    │    Low     │   Medium   │   High     │    Low     │
│  Paid Social    │   High     │   Medium   │   Medium   │    Low     │
│  Display        │   High     │    Low     │    Low     │    Low     │
│  Video          │   High     │   High     │   Medium   │   Medium   │
│  Email          │    Low     │   Medium   │   High     │   High     │
│  Organic Search │   Medium   │   High     │   Medium   │   Medium   │
│  Social Organic │   High     │   Medium   │    Low     │   Medium   │
│  Affiliate      │   Medium   │   Medium   │   High     │    Low     │
└─────────────────┴────────────┴────────────┴────────────┴────────────┘
```

### 3. Performance Analytics

```python
analytics = agent.analytics

# Record touchpoints as they occur
touchpoint = Touchpoint(
    channel=ChannelType.PAID_SEARCH,
    campaign_id=campaign.campaign_id,
    impressions=50000,
    clicks=2500,
    conversions=125,
    cost=5000,
    revenue=25000,
    visitor_id="v_001",
)
analytics.record_touchpoint(touchpoint)

# Generate dashboard
dashboard = analytics.create_dashboard()
print(f"ROAS: {dashboard.overall_roas:.2f}x")
print(f"Total Conversions: {dashboard.total_conversions}")

# Get trend data
trend = analytics.get_performance_trend(days=30)
```

**Dashboard Alerts:**

| Alert | Threshold | Severity |
|-------|-----------|----------|
| ROAS < 1.0 | Critical | Immediate action |
| CPC > $5.00 | Warning | Review targeting |
| CTR < 0.5% (10K+ impressions) | Warning | Creative fatigue |
| Conversion rate < 1% | Warning | Landing page issue |

### 4. Multi-Touch Attribution

```python
attr = agent.attribution_engine

# Add touchpoints from all channels
attr.add_touchpoints(all_touchpoints)

# Compare all attribution models
comparison = attr.compare_models()
for model_name, result in comparison.items():
    print(f"{model_name}: ROAS={result.roas:.2f}, Credits={result.channel_credits}")

# Get channel-level attribution
channel_attr = attr.get_channel_attribution(AttributionModel.TIME_DECAY)
```

**Available Models:**

| Model | Best For | Consideration |
|-------|----------|---------------|
| First Touch | Acquisition attribution | Ignores nurturing |
| Last Touch | Conversion optimization | Ignores awareness |
| Linear | Balanced view | Equal credit to all |
| Time Decay | Long sales cycles | Recent touch weighted more |
| Position-Based | First/last focus | 40/20/40 split |
| Data-Driven | Algorithmic | Requires sufficient data |
| Markov Chain | Removal impact | Complex but accurate |
| Shapley Value | Fair distribution | Computationally expensive |

### 5. Email Marketing

```python
email = agent.email_engine

campaign = email.create_campaign(
    name="Welcome Series",
    subject_line="Welcome to our community!",
    from_email="hello@company.com",
    html_content="<h1>Welcome!</h1>",
    audience=AudienceDefinition(segment=AudienceSegment.NEW_VISITORS),
)

# Send and track
email.send_campaign(campaign.email_id, recipient_count=5000)
email.record_event(campaign.email_id, EmailEventType.OPENED, count=2500)
email.record_event(campaign.email_id, EmailEventType.CLICKED, count=500)

# Get metrics
metrics = email.get_campaign_metrics(campaign.email_id)
print(f"Open rate: {metrics.open_rate:.1%}")
print(f"Click rate: {metrics.click_rate:.1%}")

# Calculate ROI
roi = email.calculate_roi(campaign.email_id, revenue_per_conversion=75)
print(f"ROI: {roi['roi']:.0f}%")
```

**Email Performance Benchmarks:**

| Metric | Good | Average | Poor |
|--------|------|---------|------|
| Open Rate | > 25% | 15-25% | < 15% |
| Click Rate | > 5% | 2-5% | < 2% |
| Bounce Rate | < 1% | 1-3% | > 3% |
| Unsubscribe | < 0.5% | 0.5-1% | > 1% |

### 6. Social Media Management

```python
social = agent.social_manager

post = social.create_post(
    platform=SocialPlatform.INSTAGRAM,
    content="Excited to announce our new product line!",
    media_urls=["https://cdn.example.com/product.jpg"],
    hashtags=["newlaunch", "product", "tech"],
    scheduled_time=datetime(2025, 7, 15, 10, 0),
)

social.publish_post(post.post_id)
social.record_engagement(post.post_id, "like", count=1500)
social.record_engagement(post.post_id, "comment", count=200)

# Platform summary
summary = social.get_platform_summary(SocialPlatform.INSTAGRAM)
top = social.get_top_posts(metric="engagement", limit=5)
```

**Supported Platforms:**

| Platform | Best Content | Engagement |
|----------|--------------|------------|
| Facebook | Links, video | Comments, shares |
| Instagram | Images, reels | Likes, saves |
| Twitter | Text, threads | Retweets, replies |
| LinkedIn | Articles, professional | Comments, reactions |
| TikTok | Short video | Views, shares |
| YouTube | Long video | Watch time, subs |

### 7. SEO Management

```python
seo = agent.seo_manager

# Track keywords
kw = seo.add_keyword(
    keyword="best running shoes",
    url="https://shop.example.com/running-shoes",
    position=12,
    search_volume=14800,
)

# Update positions
seo.update_keyword_position(kw.keyword_id, new_position=8)

# Get scorecard
scorecard = seo.get_seo_scorecard()
print(f"Keywords in Top 10: {scorecard['keywords_in_top_10']}")

# Run site audit
audit = seo.run_site_audit("shop.example.com")
print(f"Overall Score: {audit.overall_score}/100")
```

**SEO Audit Dimensions:**

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Page Speed | 25% | Load time, Core Web Vitals |
| Mobile | 20% | Mobile-friendliness, responsive |
| SEO | 35% | Meta tags, structure, content |
| Accessibility | 20% | Alt text, contrast, ARIA |

---

## Operational Guidelines

### Campaign Setup Checklist

1. Define objective (what success looks like)
2. Select channels (where audience lives)
3. Set budget (total + daily caps)
4. Define audience (demographics, interests, behaviors)
5. Create ad groups with creatives
6. Set bid strategy and amounts
7. Configure tracking pixels and conversion goals
8. Validate with `campaign.validate()` before activating

### Budget Allocation Rules

- Never allocate > 60% of budget to a single channel.
- Reserve 10-15% for testing new channels.
- Re-optimize allocation weekly based on ROAS data.
- Pause channels with ROAS < 0.5 after 7 days.

### Attribution Best Practices

- Use **Last Touch** for conversion optimization.
- Use **Linear** for balanced view of full funnel.
- Use **Time Decay** for long sales cycles (> 30 days).
- Use **Position-Based** when first and last touch matter most.
- Compare all models quarterly for strategic insight.

### Email Deliverability Rules

- Maintain bounce rate < 2%.
- Keep spam complaint rate < 0.1%.
- Authenticate with SPF, DKIM, DMARC.
- Warm up new sending domains over 2-4 weeks.
- Segment by engagement frequency.

---

## Method Signatures

### CampaignManager

```python
def create_campaign(
    self, name: str, objective: ObjectiveType, channels: List[ChannelType],
    budget_total: float, start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None, tags: Optional[List[str]] = None
) -> Campaign

def update_campaign(self, campaign_id: str, updates: Dict[str, Any]) -> Campaign
def delete_campaign(self, campaign_id: str) -> bool
def activate_campaign(self, campaign_id: str) -> bool
def pause_campaign(self, campaign_id: str) -> bool
def complete_campaign(self, campaign_id: str) -> bool
def duplicate_campaign(self, campaign_id: str, new_name: str) -> Optional[Campaign]
def list_campaigns(self, status: Optional[CampaignStatus] = None, ...) -> List[Campaign]
def get_campaign_health(self, campaign_id: str) -> Dict[str, Any]
```

### ChannelStrategyEngine

```python
def develop_strategy(
    self, objective: ObjectiveType, total_budget: float,
    target_audience: AudienceDefinition,
    preferred_channels: Optional[List[ChannelType]] = None
) -> Dict[str, Any]

def optimize_allocation(
    self, strategy_id: str, performance_data: Dict[str, ChannelPerformance]
) -> Dict[str, Any]

def get_channel_recommendations(
    self, objective: ObjectiveType, audience: AudienceDefinition, budget: float
) -> List[Dict[str, Any]]
```

### PerformanceAnalytics

```python
def record_touchpoint(self, touchpoint: Touchpoint) -> None
def get_channel_performance(self, channel: Optional[ChannelType] = None) -> Union[...]
def get_total_metrics(self) -> Dict[str, float]
def create_dashboard(self) -> DashboardSnapshot
def get_performance_trend(self, days: int = 30) -> List[Dict[str, Any]]
def register_conversion_goal(self, goal: ConversionGoal) -> None
def get_conversion_summary(self) -> Dict[str, Any]
```

### AttributionEngine

```python
def add_touchpoints(self, touchpoints: List[Touchpoint]) -> None
def compute_attribution(self, model: AttributionModel = AttributionModel.LINEAR) -> AttributionResult
def compare_models(self) -> Dict[str, AttributionResult]
def get_channel_attribution(self, model: AttributionModel = ...) -> Dict[str, Dict[str, float]]
```

### EmailMarketingEngine

```python
def create_campaign(self, name: str, subject_line: str, from_email: str, ...) -> EmailCampaign
def send_campaign(self, email_id: str, recipient_count: int) -> Dict[str, Any]
def record_event(self, email_id: str, event_type: EmailEventType, count: int = 1) -> None
def get_campaign_metrics(self, email_id: str) -> Optional[EmailMetrics]
def calculate_roi(self, email_id: str, revenue_per_conversion: float = 50.0) -> Dict[str, float]
def get_segment_performance(self) -> Dict[str, Dict[str, float]]
```

### SocialMediaManager

```python
def create_post(self, platform: SocialPlatform, content: str, ...) -> SocialPost
def publish_post(self, post_id: str) -> bool
def record_engagement(self, post_id: str, engagement_type: str, count: int = 1) -> None
def get_post_metrics(self, post_id: str) -> Optional[SocialMetrics]
def get_platform_summary(self, platform: Optional[SocialPlatform] = None) -> Dict[str, Any]
def get_top_posts(self, metric: str = "engagement", limit: int = 5) -> List[Dict[str, Any]]
```

### SEOManager

```python
def add_keyword(self, keyword: str, url: str, position: int = 0, ...) -> SEOKeyword
def update_keyword_position(self, keyword_id: str, new_position: int) -> Optional[SEOKeyword]
def get_keyword_rankings(self, top_n: Optional[int] = None) -> List[SEOKeyword]
def get_ranking_changes(self) -> List[Dict[str, Any]]
def run_site_audit(self, domain: str) -> SEOAuditResult
def get_seo_scorecard(self) -> Dict[str, Any]
```

---

## Usage Patterns

### Pattern 1: Quick Campaign Launch

```python
agent = DigitalMarketingAgent()
result = agent.create_full_campaign(
    name="Q4 Push",
    objective=ObjectiveType.CONVERSION,
    channels=[ChannelType.PAID_SEARCH, ChannelType.EMAIL],
    budget=25000,
    audience=AudienceDefinition(segment=AudienceSegment.ALL),
)
print(result["strategy"]["budget_allocation"])
```

### Pattern 2: Performance Review

```python
dashboard = agent.get_marketing_dashboard()
for alert in dashboard["alerts"]:
    print(f"[{alert['severity']}] {alert['message']}")
```

### Pattern 3: Attribution Deep Dive

```python
report = agent.run_attribution_analysis(AttributionModel.TIME_DECAY)
for ch, credit in report["channel_credits"].items():
    print(f"{ch}: {credit:.1%} of conversions")
```

### Pattern 4: Monthly Reporting

```python
monthly = agent.generate_monthly_report()
print(f"Spend: ${monthly['executive_summary']['total_spend']:,.2f}")
print(f"Revenue: ${monthly['executive_summary']['total_revenue']:,.2f}")
for rec in monthly["recommendations"]:
    print(f"- {rec}")
```

---

## Data Models Reference

| Model | Purpose | Key Fields |
|-------|---------|-----------|
| Campaign | Campaign container | id, name, objective, status, channels, budget, ad_groups |
| AdGroup | Ad grouping unit | id, name, channel, audience, creatives, bid_strategy |
| CreativeAsset | Ad creative | id, format, headline, body, URLs, dimensions |
| Touchpoint | Customer interaction | id, channel, impressions, clicks, conversions, cost, revenue |
| AttributionResult | Attribution output | model, channel_credits, total_conversions, roas |
| EmailCampaign | Email specification | id, subject, from_email, html_content, audience |
| EmailMetrics | Email performance | sent, delivered, opened, clicked, bounced, converted |
| SocialPost | Social content | id, platform, content, media_urls, hashtags |
| SocialMetrics | Social performance | impressions, reach, likes, comments, shares |
| SEOKeyword | Keyword tracking | keyword, url, position, search_volume, ctr |
| SEOAuditResult | Audit findings | scores, issues, recommendations |
| DashboardSnapshot | Point-in-time data | spend, revenue, conversions, channel_data, alerts |

---

## Security Considerations

### Data Protection

- PII handling for customer data
- GDPR compliance for EU audiences
- Secure API key storage
- Encrypted data transmission

### Access Control

```
┌─────────────────┬────────┬────────┬────────┬────────┐
│  Role           │Campaign│Email   │Social  │SEO     │
├─────────────────┼────────┼────────┼────────┼────────┤
│  Viewer         │   ✓    │   ✓    │   ✓    │   ✓    │
│  Editor         │   ✓    │   ✓    │   ✓    │   ✗    │
│  Admin          │   ✓    │   ✓    │   ✓    │   ✓    │
└─────────────────┴────────┴────────┴────────┴────────┘
```

## Scalability

### Performance Considerations

| Operation | Small (< 1K) | Medium (< 100K) | Large (< 1M) |
|-----------|---------------|-----------------|--------------|
| Touchpoint recording | 10ms | 50ms | 200ms |
| Dashboard generation | 100ms | 1s | 10s |
| Attribution analysis | 200ms | 2s | 30s |
| Report generation | 500ms | 5s | 60s |

---

## Troubleshooting

| Issue | Cause | Resolution |
|-------|-------|-----------|
| Campaign won't activate | Validation errors | Run `campaign.validate()` and fix issues |
| ROAS showing 0 | No touchpoints recorded | Ensure `record_touchpoint()` is called |
| Attribution credits don't sum to 1.0 | Floating point precision | Expected ±0.001; normalize manually if needed |
| Email open rate 0% | Events not recorded | Call `record_event()` for each event type |
| SEO audit returns random scores | Placeholder implementation | Connect to real SEO API for production use |
| Duplicate campaigns created | Calling create in a loop | Use `duplicate_campaign()` instead |
| Dashboard shows no data | Empty analytics | Record touchpoints first |

---

## Design Patterns

### Strategy Pattern for Attribution

```python
class AttributionStrategy:
    def compute(self, touchpoints: List[Touchpoint]) -> Dict[str, float]:
        raise NotImplementedError

class FirstTouchStrategy(AttributionStrategy):
    def compute(self, touchpoints):
        # Give all credit to first touchpoint
        pass

class TimeDecayStrategy(AttributionStrategy):
    def compute(self, touchpoints):
        # Weight by recency
        pass
```

### Observer Pattern for Campaign Events

```python
class CampaignObserver:
    def on_campaign_activated(self, campaign: Campaign):
        self.notify_stakeholders(campaign)
    
    def on_budget_exhausted(self, campaign: Campaign):
        self.alert_team(campaign)
```

### Factory Pattern for Channel Creation

```python
class ChannelFactory:
    @staticmethod
    def create(channel_type: ChannelType, config: Dict) -> Channel:
        if channel_type == ChannelType.PAID_SEARCH:
            return PaidSearchChannel(config)
        elif channel_type == ChannelType.EMAIL:
            return EmailChannel(config)
        # ... etc
```

---

## Integration Points

| System | Protocol | Purpose |
|--------|----------|---------|
| Google Ads API | REST | Campaign sync, keyword data |
| Meta Marketing API | Graph API | Social ad campaigns |
| Mailchimp / SendGrid | REST | Email delivery |
| Google Analytics | GA4 API | Conversion tracking |
| SEMrush / Ahrefs | REST | SEO keyword data |
| Social Platform APIs | REST/Graph | Post scheduling, engagement |

---

## Checklist

- [ ] Define campaign objective before selecting channels
- [ ] Set daily and total budget caps
- [ ] Validate campaigns before activation
- [ ] Record all touchpoints for accurate attribution
- [ ] Review dashboard alerts daily
- [ ] Optimize budget allocation weekly
- [ ] Compare attribution models monthly
- [ ] Monitor email deliverability metrics
- [ ] Track SEO ranking changes weekly
- [ ] Generate monthly performance reports

---

## Configuration

```yaml
digital_marketing_agent:
  campaign_manager:
    max_campaigns: 10000
    audit_log_retention_days: 365

  channel_strategy:
    default_currency: USD
    optimization_frequency: daily

  analytics:
    touchpoint_retention_days: 365
    alert_thresholds:
      roas_critical: 1.0
      cpc_warning: 5.0

  attribution:
    default_model: linear
    time_decay_half_life_days: 7

  email:
    max_send_rate_per_hour: 100000

  seo:
    max_keywords_tracked: 50000
```

---

## Best Practices

1. **Always validate before activating** — run `campaign.validate()` to catch issues before they cost money.
2. **Record every touchpoint** — attribution accuracy depends on complete data.
3. **Compare attribution models** — no single model tells the full story.
4. **Monitor alerts daily** — catch ROAS drops and CPC spikes early.
5. **Re-optimize weekly** — use performance data to reallocate budgets.
6. **Segment email campaigns** — personalized emails get 2x higher open rates.
7. **Track SEO weekly** — ranking changes signal algorithm updates.
8. **Keep creatives fresh** — ad fatigue drops CTR by 50%+ within 2 weeks.

---

## Future Enhancements

- AI-powered creative optimization
- Predictive budget allocation
- Automated A/B testing
- Cross-channel attribution unification
- Real-time bid optimization
- Customer lifetime value prediction
- Automated competitor analysis


# AdOperations Agent

> **THE** definitive agent for digital advertising campaign management,
> budget optimization, A/B testing, and fraud detection.
> Multi-platform, multi-objective, and production-ready.

---

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Core Concepts](#core-concepts)
7. [API Reference](#api-reference)
8. [Usage Patterns](#usage-patterns)
9. [Report Formats](#report-formats)
10. [Optimization](#optimization)
11. [A/B Testing](#ab-testing)
12. [Fraud Detection](#fraud-detection)
13. [Alerts & Monitoring](#alerts--monitoring)
14. [Batch Operations](#batch-operations)
15. [Integration Hooks](#integration-hooks)
16. [Performance Tuning](#performance-tuning)
17. [Security & Privacy](#security--privacy)
18. [Extending the Agent](#extending-the-agent)
19. [Troubleshooting](#troubleshooting)
20. [FAQ](#faq)
21. [Contributing](#contributing)

---

---

## Overview

The AdOperations Agent is a comprehensive system for managing, optimizing,
and analyzing digital advertising campaigns. It is designed to be:

- **Multi-platform**: Google Ads, Meta, LinkedIn, TikTok, programmatic.
- **Goal-oriented**: supports all common campaign objectives.
- **Performance-driven**: bid optimization, budget pacing, A/B testing.
- **Secure**: fraud detection, budget safeguards, and anomaly alerting.

### What It Does

- Creates and manages campaigns, ad groups, and creatives.
- Optimizes budget allocation across campaigns.
- Calculates recommended bids based on historical performance.
- Runs and analyzes A/B tests for statistical significance.
- Detects click fraud, conversion stuffing, and invalid traffic.
- Monitors budget pacing and predicts spend.
- Generates reports in HTML, JSON, CSV, and PDF.
- Tracks metrics: CTR, CPC, CPA, ROAS.

---

---

## Key Features

### Campaign Management

- Full lifecycle: create, pause, resume, archive.
- Multi-platform support via `AdPlatform` enum.
- Flexible objectives: awareness, traffic, conversions, sales, leads, etc.
- Hierarchical model: Campaign -> AdGroup -> Creative.

### Optimization

- `BiddingEngine` with `TARGET_CPA`, `TARGET_ROAS`, and manual strategies.
- `BudgetPacingMonitor` with spend forecasting and alerting.
- Automated recommendation generation based on CTR, CPA, and pacing.

### Testing

- `ABTestManager` with chi-squared significance testing.
- Configurable significance thresholds.
- Winner determination and confidence reporting.

### Fraud & Quality

- `FraudDetectionEngine` for IP frequency, UA duplication, conversion spikes.
- `PerformanceAlert` objects for pacing anomalies.
- Blacklisting support for IPs and user agents.

### Reporting

- HTML dashboards with summary cards and tables.
- JSON exports with full campaign and creative details.
- CSV spreadsheets for analysis.
- Scheduled report delivery support.

---

---

## Quick Start

```python
from agents.ad_operations.agent import AdOperationsAgent

agent = AdOperationsAgent()

campaign = agent.create_campaign(
    name="Product Launch",
    platform="google",
    objective="conversions",
    total_budget=2500.0,
)

ad_group = agent.add_ad_group(
    campaign_id=campaign.id,
    name="Search - Generic",
    daily_budget=120.0,
    target_cpa=35.0,
)

creative = agent.add_creative(
    campaign_id=campaign.id,
    ad_group_id=ad_group.id,
    headline="Launch Day Sale",
    description="Get early access now.",
    ad_type="text",
    final_url="https://example.com/launch",
)

report = agent.generate_report([campaign.id], fmt="json")
print(report)
```

---

---

## Installation

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
```

No mandatory external dependencies for the core agent.

---

---

## Configuration

```python
from agents.ad_operations.agent import AdOperationsAgent, Config

config = Config(
    default_platform="google",
    default_objective="conversions",
    default_bidding_strategy="target_cpa",
    target_cpa=30.0,
    target_roas=3.5,
    daily_budget_cap=400.0,
    max_bid=8.0,
    min_bid=0.5,
    fraud_detection_enabled=True,
    fraud_confidence_threshold=0.8,
    budget_pacing_alert_threshold=0.8,
    ab_test_significance_threshold=0.95,
    report_formats=["html", "json", "csv"],
    output_directory="./ad_ops_reports",
    notify_on_alerts=True,
    alert_channels=["email", "slack"],
)

agent = AdOperationsAgent(config=config)
```

---

---

## Core Concepts

### Campaign Hierarchy

- `Campaign` owns budget, platform, objective, status, timing.
- `AdGroup` groups creatives and shares bidding/audience settings.
- `AdCreative` holds headline, description, type, status, and metrics.

### Metrics

| Metric | Formula |
|--------|---------|
| CTR | `clicks / impressions * 100` |
| CPC | `spent / clicks` |
| CPA | `spent / conversions` |
| ROAS | `revenue / spent` |

### Statuses

- `DRAFT` - not yet launched.
- `ACTIVE` - running.
- `PAUSED` - temporarily stopped.
- `ARCHIVED` - ended and stored.
- `REMOVED` - deleted.
- `DISAPPROVED` - rejected by platform.

### Bidding Strategies

- `TARGET_CPA` - optimize for cost per acquisition.
- `TARGET_ROAS` - optimize for return on ad spend.
- `MAXIMIZE_CONVERSIONS` - maximize volume.
- `MANUAL_CPC` / `MANUAL_CPM` / `MANUAL_CPV` - manual.

---

---

## API Reference

### Campaign Operations

- `create_campaign(name, platform, objective, total_budget, ...) -> Campaign`
- `get_campaign(campaign_id) -> Optional[Campaign]`
- `pause_campaign(campaign_id) -> Dict`
- `resume_campaign(campaign_id) -> Dict`
- `archive_campaign(campaign_id) -> Dict`
- `list_campaigns(status=None, platform=None) -> List[Campaign]`

### Ad Group & Creative Operations

- `add_ad_group(campaign_id, name, daily_budget, ...) -> AdGroup`
- `add_creative(campaign_id, ad_group_id, headline, description, ad_type, ...) -> AdCreative`

### Optimization

- `optimize_campaign(campaign_id) -> Dict`
- `optimize_budget(campaign_ids=None) -> Dict[str, float]`
- `calculate_recommended_bid(campaign_id, ad_group_id, target_metric="cpa") -> float`

### A/B Testing

- `create_ab_test(test_id, variant_a_id, variant_b_id, metric="ctr", sample_size=1000) -> ABTestResult`
- `record_ab_observation(test_id, variant, converted, impression=True) -> None`
- `get_ab_test_result(test_id) -> Optional[ABTestResult]`
- `complete_ab_test(test_id) -> ABTestResult`

### Reporting & Metrics

- `batch_audit(campaign_ids) -> List[Dict]`
- `generate_report(campaign_ids=None, fmt="html", output_path=None) -> str`
- `get_metrics_summary(campaign_id=None) -> Dict`
- `get_status() -> Dict[str, Any]`

### Fraud & Alerts

- `analyze_fraud(clicks, conversions) -> List[FraudSignal]`
- `get_fraud_signals() -> List[FraudSignal]`
- `blacklist_ip(ip) -> None`
- `get_alerts() -> List[PerformanceAlert]`

---

---

## Usage Patterns

### New Campaign Setup

```python
campaign = agent.create_campaign(
    name="Black Friday",
    platform="google",
    objective="sales",
    total_budget=10000.0,
    start_date=datetime(2026, 11, 20),
    end_date=datetime(2026, 11, 30),
)

ag = agent.add_ad_group(campaign.id, "Shopping - Core", 1500.0)

agent.add_creative(
    campaign.id,
    ag.id,
    headline="Black Friday Deals",
    description="Up to 70% off.",
    ad_type="shopping",
    final_url="https://example.com/bf",
)
```

### Weekly Optimization

```python
active_ids = [c.id for c in agent.list_campaigns(status="active")]
agent.optimize_budget(active_ids)
for cid in active_ids:
    agent.optimize_campaign(cid)
```

### Fraud Investigation

```python
alerts = agent.analyze_fraud(clicks=clicks, conversions=conversions)
for alert in alerts:
    if alert.severity.value in ("critical", "emergency"):
        # notify ops team, pause campaign, etc.
```

### A/B Testing

```python
test = agent.create_ab_test("ctr-test", "cr-a", "cr-b", metric="ctr")
for _ in range(3000):
    agent.record_ab_observation(test.test_id, "a", converted=False)
    agent.record_ab_observation(test.test_id, "b", converted=False)
result = agent.complete_ab_test(test.test_id)
```

---

---

## Report Formats

### HTML

Styled dashboard with:

- Summary cards: impressions, clicks, conversions, spend.
- Creative performance table.
- Platform and status breakdowns.

### JSON

Machine-readable payload with campaign details and summary aggregates.

### CSV

Spreadsheet-friendly rows for campaign-level metrics.

### PDF

Placeholder output, suitable for piping into `weasyprint` or similar.

---

---

## Optimization

### Budget Allocation

`optimize_budget()` distributes budget across campaigns based on efficiency:

- `ROAS_score = campaign.roas() if > 0 else 1.0`
- `CPA_score = 1 / campaign.cpa() if > 0 else 1 / target_cpa`
- `score = ROAS_score * CPA_score * jitter`
- `allocation = (score / total_scores) * total_budget`

### Bid Recommendations

`calculate_recommended_bid()`:

- Default: derives bid from target CPA/ROAS and device modifiers.
- Optimized: adjusts using historical performance and observed ROAS/CPA.

### Pacing Alerts

`BudgetPacingMonitor` compares daily spend to expected trajectory:

- `expected = (hour_of_day / 24) * daily_budget_cap`
- Overspend: `spend > threshold * expected` -> CRITICAL.
- Underspend: `spend < low_budget_threshold * expected after 18:00` -> WARNING.

---

---

## A/B Testing

### Statistical Method

- Pooled conversion rate from both variants.
- Standard error computed from impressions and conversions.
- Confidence level and p-value via normal CDF approximation.
- Winner declared only when `confidence_level >= significance_threshold`.

### Practical Guidance

- Run until sample size is sufficiently large.
- Do not peek and stop early; use fixed horizon tests.
- One test per creative element at a time for clean attribution.

---

---

## Fraud Detection

### Signals

| Signal | Typical Cause |
|--------|---------------|
| `high_frequency_click` | Bots or click farms from one IP. |
| `duplicate_user_agent` | Headless browsers or scripted traffic. |
| `conversion_spike` | Conversion stuffing or fake events. |
| `cookie_hijacking` | Shared cookies across many IPs/devices. |
| `fake_leads` | Outlier conversion amounts or patterns. |

### Usage

```python
alerts = agent.analyze_fraud(clicks=clicks, conversions=conversions)
for alert in alerts:
    print(alert.signal_type, alert.confidence, alert.description)
```

---

---

## Alerts & Monitoring

### Budget Pacing Alerts

Generated automatically when `record_spend()` is called during audits.

### Acknowledging Alerts

```python
for alert in agent.get_alerts():
    agent.acknowledge_alert(alert.alert_id)
```

### Status Dashboard

```python
status = agent.get_status()
print(status["campaigns"], status["active_campaigns"], status["total_alerts"])
```

---

---

## Batch Operations

```python
# Batch audit
results = agent.batch_audit([c.id for c in agent.list_campaigns()])

# Batch campaign creation
defs = [
    {"name": f"Geo {i}", "platform": "google", "objective": "traffic", "total_budget": 500.0}
    for i in range(20)
]
campaigns = agent.batch_create_campaigns(defs)
```

---

---

## Integration Hooks

### Scheduled Reports

```python
schedule_id = agent.schedule_report(
    campaign_ids=[campaign.id],
    cron_expression="0 6 * * 1",
    fmt="csv",
    recipients=["team@example.com"],
)
```

### Export / Import

- `export_campaigns(fmt="json")` for backup or migration.
- `import_campaigns(data, fmt="json")` for restore.

### Comparison

```python
comparison = agent.compare_campaigns([c1.id, c2.id])
print(comparison["best_roas"], comparison["lowest_cpa"])
```

---

---

## Performance Tuning

- Disable history for short-lived CI runs.
- Limit report formats to reduce I/O.
- Increase `batch_operation_concurrency` for large account scans.
- Cap retention to reduce memory footprint.

---

---

## Security & Privacy

- No credentials or API secrets are stored in `Campaign` or `Config`.
- Fraud analysis runs on supplied event data only.
- Report writers should redact PII before external distribution.

---

---

## Extending the Agent

### Custom Bid Strategies

Add enum values to `BiddingStrategy` and handle them in `BiddingEngine.calculate_bid()`.

### Custom Fraud Rules

Extend `FraudDetectionEngine.analyze_clicks()` or `analyze_conversions()`.

### Custom Reports

Add generator methods in `ReportingEngine`.

---

---

## Troubleshooting

### Wrong Platform Enum

Use lowercase strings matching `AdPlatform` values: `google`, `facebook`, `linkedin`, etc.

### Optimization Not Changing Budgets

Verify campaign status is `ACTIVE`; only active campaigns are included by default.

### Alerts Not Appearing

Ensure `notify_on_alerts=True` and check `get_alerts()` directly.

---

---

## FAQ

**Q: Does this connect to real ad platforms?**
A: Not out of the box. It provides the data model, optimization, and reporting
layer. You would add API adapters for Google Ads, Meta Ads, etc.

**Q: Can I use this for attribution?**
A: The model supports `AudienceSegment` and tracking fields, but full multi-touch
attribution would require extending the event model.

**Q: How accurate is A/B test significance?**
A: It uses a simplified chi-squared approximation. For production significance
testing, consider a dedicated statistics library.

---

---

## Appendix A: Metric Formulas and Benchmarks

### Core Formulas

```
CTR  = (clicks / impressions) * 100
CPC  = spend / clicks
CPM  = (spend / impressions) * 1000
CPA  = spend / conversions
CVR  = (conversions / clicks) * 100
ROAS = revenue / spend
AOV  = revenue / conversions
Frequency = impressions / unique_users
```

### Benchmarks by Industry (Approximate)

| Industry | Avg CTR | Avg CPC | Avg CPA | Avg ROAS |
|----------|---------|---------|---------|----------|
| E-commerce | 1.5% - 3.0% | $0.50 - $2.00 | $20 - $75 | 3.0 - 5.0 |
| SaaS / B2B | 2.0% - 4.0% | $2.00 - $8.00 | $50 - $150 | 2.5 - 4.0 |
| Finance | 1.0% - 2.5% | $3.00 - $10.00 | $75 - $200 | 2.0 - 3.5 |
| Education | 2.0% - 5.0% | $1.00 - $4.00 | $30 - $80 | 3.0 - 5.0 |
| Gaming | 2.5% - 6.0% | $0.20 - $1.00 | $5 - $25 | 2.0 - 4.0 |
| Healthcare | 1.5% - 3.5% | $2.00 - $7.00 | $60 - $180 | 2.0 - 3.5 |

### Performance Health Checks

| Metric | Excellent | Good | Needs Work |
|--------|-----------|------|------------|
| CTR | > 3% | 1% - 3% | < 1% |
| CPC | < $0.50 | $0.50 - $2.00 | > $2.00 |
| CPA | < $20 | $20 - $75 | > $75 |
| ROAS | > 5.0 | 3.0 - 5.0 | < 3.0 |

---

---

## Appendix B: Platform Implementation Notes

### Google Ads

- `platform="google"`
- Supports search, shopping, display, video.
- Bidding: `target_cpa`, `target_roas`, `maximize_conversions`, `manual_cpc`.
- Pair with `objective="conversions"` for best results.
- Use `AudienceType.IN_MARKET` for high-intent targeting.

### Meta Ads

- `platform="facebook"`
- Supports feed, stories, reels, messenger.
- Bidding: `lowest_cost`, `target_cpa`, `target_roas`.
- Creative types: `image`, `video`, `carousel`, `collection`, `story`.
- Use `AudienceType.LOOKALIKE` for scaled prospecting.

### TikTok Ads

- `platform="tiktok"`
- Creative: `video`, `spark_ad`.
- Objectives: `video_views`, `conversions`, `app_installs`.
- Use vertical video for best performance.

### LinkedIn Ads

- `platform="linkedin"`
- Best for B2B lead gen and brand awareness.
- Targeting: company size, industry, job title, skills.
- Bidding: `cpc`, `cpm`, `cpa`.

### Programmatic / Display / Native

- Use `platform="programmatic"` / `display` / `native`.
- Creative types: `banner`, `native`.
- Use `AudienceType.RETARGETING` for efficiency.
- Monitor frequency and unique reach.

---

---

## Appendix C: Troubleshooting Decision Tree

### Symptom: Low CTR

1. Is the audience well-defined?
   - No -> Refine targeting, use lookalikes or narrower interests.
   - Yes -> Continue.
2. Is the creative compelling?
   - No -> Test new headlines and visuals via A/B test.
   - Yes -> Continue.
3. Is the ad format appropriate for the platform?
   - No -> Switch to platform-native formats (Reels, Stories, Shorts).
   - Yes -> Review placement and auction overlap.

### Symptom: High CPC

1. Are competitors bidding aggressively?
   - Yes -> Adjust strategy to niche keywords or times.
   - No -> Continue.
2. Is Quality Score low?
   - Yes -> Improve ad relevance and landing page experience.
   - No -> Continue.
3. Is targeting too broad?
   - Yes -> Narrow geo, device, or audience.
   - No -> Review bid strategy and manual overrides.

### Symptom: High CPA

1. Is the landing page converting?
   - No -> Optimize landing page, form length, and load speed.
   - Yes -> Continue.
2. Is the traffic quality low?
   - Yes -> Tighten targeting, exclude placements, add negative keywords.
   - No -> Continue.
3. Is the bid too high for conversion value?
   - Yes -> Lower bids or switch to target ROAS.
   - No -> Review attribution window and conversion tracking.

### Symptom: Low ROAS

1. Are conversions tracked correctly?
   - No -> Fix pixel/API implementation.
   - Yes -> Continue.
2. Is the product margin sufficient?
   - No -> Improve offer or reduce cost per conversion.
   - Yes -> Continue.
3. Is the audience buying-oriented?
   - No -> Shift to lower-funnel objectives or audiences.
   - Yes -> Review creative and offer relevance.

---

---

## Appendix D: Scaling Patterns

### Multi-Account Management

```python
accounts = [...]
for account in accounts:
    agent = AdOperationsAgent(config=Config(...))
    campaigns = agent.list_campaigns(status="active")
    agent.optimize_budget([c.id for c in campaigns])
```

### Scheduled Optimization

```python
import schedule

def nightly_optimize():
    active_ids = [c.id for c in agent.list_campaigns(status="active")]
    agent.optimize_budget(active_ids)
    for cid in active_ids:
        agent.optimize_campaign(cid)

schedule.every().day.at("01:00").do(nightly_optimize)
```

### Alert Escalation

```python
for alert in agent.get_alerts():
    if alert.severity == AlertSeverity.CRITICAL:
        notify_pagerduty(alert)
    elif alert.severity == AlertSeverity.WARNING:
        notify_slack(alert)
```

### Report Distribution

```python
report_path = agent.generate_report(
    campaign_ids=active_ids,
    fmt="html",
    output_path="weekly_report.html",
)
email_send(
    to="stakeholders@example.com",
    subject="Weekly Ad Report",
    attachments=[report_path],
)
```

---

---

## Appendix E: Integration Patterns

### External Platform Sync

```python
# Pseudocode
for platform_campaign in external_platform.list_campaigns():
    local = agent.get_campaign(platform_campaign.id)
    if not local:
        agent.create_campaign_from_external(platform_campaign)
    else:
        agent.sync_campaign_metrics(local.id, platform_campaign.metrics)
```

### Weekly Stakeholder Email

```python
report_path = agent.generate_report(
    campaign_ids=active_ids,
    fmt="html",
    output_path="weekly_report.html",
)
# email_send(to="stakeholders@example.com", subject="Weekly Ad Report", body=..., attachments=[report_path])
```

---

---

## Appendix F: Design Decisions

### Why Hierarchical Model (Campaign -> AdGroup -> Creative)?

Matches real ad platform APIs (Google Ads, Meta Ads). Makes budget and bidding
scoping intuitive: budgets live at campaign or ad group level, creatives inherit
ad group settings.

### Why Separate BiddingEngine and BudgetPacingMonitor?

- `BiddingEngine` answers: "What should the bid be?"
- `BudgetPacingMonitor` answers: "Are we spending correctly over time?"
Separation keeps concerns clean and allows independent testing.

### Why In-Memory History?

For demo and library usage, in-memory history avoids filesystem dependencies.
Production deployments can extend with persistence layers (DB, S3, etc.).

### Why Simplified Fraud Detection?

Production fraud detection is complex and often ML-based. The built-in engine
covers common rule-based signals (IP frequency, UA duplication, conversion spikes)
and is designed to be extended with custom heuristics or third-party feed scores.

### Why Not a Real API Client?

The agent is designed as a logic and modeling layer. Platform APIs change
frequently, require auth, and have quota limits. Decoupling the domain model
from API transport keeps the codebase stable and testable.

---

---

## Appendix G: Migration Guide

### From Ad Operations Agent v1.x

- `Campaign` and `AdGroup` dataclasses replace older dict-based structures.
- Enums replace free-form status/type strings.
- `AuditResult`-style summaries are available via `batch_audit()`.
- Fraud detection is now engine-based instead of method-based.

### From External Spreadsheets

```python
# Convert spreadsheet rows to create_campaign calls
for row in spreadsheet:
    agent.create_campaign(
        name=row["Campaign Name"],
        platform=row["Platform"].lower(),
        objective=row["Objective"].lower(),
        total_budget=float(row["Budget"]),
    )
```

---

---

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

---

## License

MIT License - see [LICENSE](../../LICENSE).

---

---

## Appendix A: Metric Formulas and Benchmarks

### Core Formulas

```
CTR  = (clicks / impressions) * 100
CPC  = spend / clicks
CPM  = (spend / impressions) * 1000
CPA  = spend / conversions
CVR  = (conversions / clicks) * 100
ROAS = revenue / spend
AOV  = revenue / conversions
Frequency = impressions / unique_users
```

### Benchmarks by Industry (Approximate)

| Industry | Avg CTR | Avg CPC | Avg CPA | Avg ROAS |
|----------|---------|---------|---------|----------|
| E-commerce | 1.5% - 3.0% | $0.50 - $2.00 | $20 - $75 | 3.0 - 5.0 |
| SaaS / B2B | 2.0% - 4.0% | $2.00 - $8.00 | $50 - $150 | 2.5 - 4.0 |
| Finance | 1.0% - 2.5% | $3.00 - $10.00 | $75 - $200 | 2.0 - 3.5 |
| Education | 2.0% - 5.0% | $1.00 - $4.00 | $30 - $80 | 3.0 - 5.0 |
| Gaming | 2.5% - 6.0% | $0.20 - $1.00 | $5 - $25 | 2.0 - 4.0 |
| Healthcare | 1.5% - 3.5% | $2.00 - $7.00 | $60 - $180 | 2.0 - 3.5 |

### Performance Health Checks

| Metric | Excellent | Good | Needs Work |
|--------|-----------|------|------------|
| CTR | > 3% | 1% - 3% | < 1% |
| CPC | < $0.50 | $0.50 - $2.00 | > $2.00 |
| CPA | < $20 | $20 - $75 | > $75 |
| ROAS | > 5.0 | 3.0 - 5.0 | < 3.0 |

---

---

## Appendix B: Troubleshooting Decision Tree

### Symptom: Low CTR

1. Is the audience well-defined?
   - No -> Refine targeting, use lookalikes or narrower interests.
   - Yes -> Continue.
2. Is the creative compelling?
   - No -> Test new headlines and visuals via A/B test.
   - Yes -> Continue.
3. Is the ad format appropriate for the platform?
   - No -> Switch to platform-native formats (Reels, Stories, Shorts).
   - Yes -> Review placement and auction overlap.

### Symptom: High CPC

1. Are competitors bidding aggressively?
   - Yes -> Adjust strategy to niche keywords or times.
   - No -> Continue.
2. Is Quality Score low?
   - Yes -> Improve ad relevance and landing page experience.
   - No -> Continue.
3. Is targeting too broad?
   - Yes -> Narrow geo, device, or audience.
   - No -> Review bid strategy and manual overrides.

### Symptom: High CPA

1. Is the landing page converting?
   - No -> Optimize landing page, form length, and load speed.
   - Yes -> Continue.
2. Is the traffic quality low?
   - Yes -> Tighten targeting, exclude placements, add negative keywords.
   - No -> Continue.
3. Is the bid too high for conversion value?
   - Yes -> Lower bids or switch to target ROAS.
   - No -> Review attribution window and conversion tracking.

### Symptom: Low ROAS

1. Are conversions tracked correctly?
   - No -> Fix pixel/API implementation.
   - Yes -> Continue.
2. Is the product margin sufficient?
   - No -> Improve offer or reduce cost per conversion.
   - Yes -> Continue.
3. Is the audience buying-oriented?
   - No -> Shift to lower-funnel objectives or audiences.
   - Yes -> Review creative and offer relevance.

---

---

## Appendix C: Scaling Patterns

### Multi-Account Management

```python
accounts = [...]
for account in accounts:
    agent = AdOperationsAgent(config=Config(...))
    campaigns = agent.list_campaigns(status="active")
    agent.optimize_budget([c.id for c in campaigns])
```

### Scheduled Optimization

```python
import schedule

def nightly_optimize():
    active_ids = [c.id for c in agent.list_campaigns(status="active")]
    agent.optimize_budget(active_ids)
    for cid in active_ids:
        agent.optimize_campaign(cid)

schedule.every().day.at("01:00").do(nightly_optimize)
```

### Alert Escalation

```python
for alert in agent.get_alerts():
    if alert.severity == AlertSeverity.CRITICAL:
        notify_pagerduty(alert)
    elif alert.severity == AlertSeverity.WARNING:
        notify_slack(alert)
```

### Report Distribution

```python
report_path = agent.generate_report(
    campaign_ids=active_ids,
    fmt="html",
    output_path="weekly_report.html",
)
email_send(
    to="stakeholders@example.com",
    subject="Weekly Ad Report",
    attachments=[report_path],
)
```

---

---

## Appendix D: Glossary

- **Campaign**: Top-level ad buy with platform, objective, budget, and schedule.
- **Ad Group**: Logical subdivision of a campaign with shared targeting and bidding.
- **Creative**: Individual ad asset (headline, description, image/video).
- **CTR**: Click-through rate = clicks / impressions.
- **CPC**: Cost per click = spend / clicks.
- **CPA**: Cost per acquisition = spend / conversions.
- **ROAS**: Return on ad spend = revenue / spend.
- **Bid**: Maximum amount paid per interaction (click, impression, conversion).
- **Attribution**: Model for assigning conversion credit across touchpoints.
- **Pacing**: Rate of spend relative to available budget and time.
- **Invalid Traffic**: Clicks or impressions not driven by genuine user interest.
- **A/B Test**: Controlled experiment comparing two variants for statistical significance.

---

---

## Version History

- **v2.1.0** (2026-06-03)
  - Full rewrite with hierarchical campaign model.
  - New engines: BiddingEngine, BudgetPacingMonitor, ABTestManager, FraudDetectionEngine.
  - Multi-format reporting.
  - Batch operations and alerting.

- **v1.0.0** (2024-01-01)
  - Initial release with basic campaign creation and optimization.

---

---

*AdOperations Agent v2.1.0 - Part of the Awesome Grok Skills collection.*

*Last updated: 2026-06-03*

*Maintained by the AdOperations Agent team and Grok community.*

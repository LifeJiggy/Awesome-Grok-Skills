# Customer Retention Agent

A comprehensive churn prediction and customer retention platform with loyalty programs, NPS analysis, retention strategies, win-back campaigns, cohort analysis, health monitoring, renewal management, contract tracking, sentiment analysis, escalation management, churn reason analysis, and retention dashboards.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Churn Prediction](#churn-prediction)
  - [Loyalty Programs](#loyalty-programs)
  - [NPS Analysis](#nps-analysis)
  - [Customer Health Monitoring](#customer-health-monitoring)
  - [Renewal Management](#renewal-management)
  - [Contract Tracking](#contract-tracking)
  - [Sentiment Analysis](#sentiment-analysis)
  - [Escalation Management](#escalation-management)
  - [Churn Reason Analysis](#churn-reason-analysis)
  - [Retention Strategies](#retention-strategies)
  - [Win-Back Campaigns](#win-back-campaigns)
  - [Cohort Analysis](#cohort-analysis)
  - [Dashboard and Alerting](#dashboard-and-alerting)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The Customer Retention Agent provides a complete toolkit for minimizing churn and maximizing customer lifetime value. It combines predictive analytics with actionable retention strategies, health monitoring, sentiment analysis, and escalation management to help businesses keep their customers engaged and loyal.

Built with thread-safe, in-memory data structures, the agent is designed for high-performance real-time churn prediction and retention operations. Every component is independently testable and the full system integrates through a single orchestrator class.

## Features

- **Churn Prediction**: Behavioral signal analysis with weighted risk scoring
- **Loyalty Programs**: Points, tiers, rewards catalog, and redemption tracking
- **NPS Tracking**: Survey management, score calculation, and trend analysis
- **Health Monitoring**: Composite health scoring from multiple behavioral dimensions
- **Renewal Management**: Pipeline tracking for contract renewals and revenue retention
- **Contract Tracking**: Contract lifecycle management and expiration monitoring
- **Sentiment Analysis**: Text feedback analysis with per-customer sentiment scoring
- **Escalation Management**: Rule-based escalation creation and resolution tracking
- **Churn Reason Analysis**: Root cause categorization with evidence collection
- **Retention Strategies**: Automated recommendation and execution
- **Win-Back Campaigns**: Multi-step re-engagement for churned customers
- **Cohort Analysis**: Retention curves and cross-cohort comparison
- **Retention Dashboard**: Alerting, snapshots, and centralized monitoring

## Quick Start

```python
from agents.customer_retention.agent import CustomerRetentionAgent, Config

agent = CustomerRetentionAgent(Config())
agent.initialize()

# Register customer
agent.register_customer("cust_001", name="John", monthly_revenue=200)

# Track churn signals
agent.update_customer_signal("cust_001", "login_decrease", 0.7)

# Predict churn
prediction = agent.predict_churn("cust_001")
print(f"Risk: {prediction['risk_level']} ({prediction['risk_score']})")

# Add loyalty points
agent.add_loyalty_points("cust_001", 500, "Purchase")

# Calculate health score
agent.calculate_health_score("cust_001", engagement=0.8, satisfaction=0.7,
                             financial=0.9, support=0.6, contract=0.85)

# Get NPS survey
survey = agent.send_nps_survey("cust_001")

# Full report
report = agent.get_full_report()

agent.shutdown()
```

## Installation

```bash
git clone https://github.com/your-org/customer-retention-agent.git
cd customer-retention-agent
pip install -r requirements.txt
```

## Usage

### Churn Prediction

```python
from datetime import datetime

# Register customers
agent.register_customer("cust_001", name="John", monthly_revenue=200,
                        contract_end_date=datetime(2024, 6, 30))

# Track behavioral signals
agent.update_customer_signal("cust_001", "login_decrease", 0.8)
agent.update_customer_signal("cust_001", "feature_usage_decline", 0.6)
agent.update_customer_signal("cust_001", "support_ticket_increase", 0.4)

# Get prediction
pred = agent.predict_churn("cust_001")
print(f"Risk Level: {pred['risk_level']}")
print(f"Risk Score: {pred['risk_score']:.3f}")
print(f"Signals: {pred['signals']}")
print(f"Recommended Actions: {pred['actions']}")

# Batch prediction
all_preds = agent.predict_all_churn()
print(f"Risk Distribution: {all_preds['risk_distribution']}")

# Get signal history
history = agent._churn_predictor.get_signal_history("cust_001", limit=20)

# Adjust signal weights for your business
agent._churn_predictor.update_signal_weight("login_decrease", 0.4)

# Get current weights
weights = agent._churn_predictor.get_signal_weights()
```

### Loyalty Programs

```python
# Add points from purchase
agent.add_loyalty_points("cust_001", 200, "Purchase #1001")

# Check balance and tier
info = agent.get_loyalty_info("cust_001")
print(f"Balance: {info['balance']} points")
print(f"Tier: {info['tier']}")
print(f"Benefits: {info['benefits']['benefits']}")

# Register rewards
agent.register_loyalty_reward("r_001", "10% Discount", 1000, "discount", 10.0)
agent.register_loyalty_reward("r_002", "Free Month", 5000, "free_product", 0.0)

# Redeem
result = agent.redeem_loyalty_points("cust_001", 1000, "r_001")
print(f"Redeemed: {result['points']} points for {result['reward_name']}")

# Points summary
summary = agent._loyalty_manager.get_points_summary("cust_001")
print(f"Total earned: {summary['total_earned']}")
print(f"Total redeemed: {summary['total_redeemed']}")
print(f"Current balance: {summary['current_balance']}")

# Top earners leaderboard
top = agent._loyalty_manager.get_top_earners(limit=10)
for entry in top:
    print(f"  {entry['customer_id']}: {entry['balance']} pts ({entry['tier']})")

# Expire old points
agent._loyalty_manager.expire_points("cust_001", 100)

# Available rewards
rewards = agent._loyalty_manager.get_available_rewards()

# Tier distribution
tiers = agent.get_loyalty_tier_distribution()

# Redemption rate
rate = agent._loyalty_manager.get_redemption_rate()
print(f"Redemption rate: {rate:.1%}")
```

### NPS Analysis

```python
# Send survey
survey = agent.send_nps_survey("cust_001")

# Submit response
agent.submit_nps_response(survey["survey_id"], 9, "Love the product!")

# Get NPS score
nps = agent.get_nps_score()
print(f"NPS: {nps['nps_score']}")
print(f"Promoters: {nps['promoters']}, Passives: {nps['passives']}, Detractors: {nps['detractors']}")

# Get trend
trend = agent.get_nps_trend(6)  # Last 6 months
for period in trend:
    print(f"{period['period']}: NPS={period['nps_score']}")

# Response rate
rate = agent._nps_manager.get_response_rate()
print(f"Response rate: {rate:.1%}")

# NPS by segment
segments = {"enterprise": ["cust_001", "cust_002"], "smb": ["cust_003"]}
segment_nps = agent._nps_manager.get_nps_by_segment(segments)
for seg, data in segment_nps.items():
    print(f"  {seg}: NPS={data['nps_score']} (n={data['total']})")

# Expire a stale survey
agent._nps_manager.expire_survey(survey["survey_id"])

# Get all surveys
all_surveys = agent._nps_manager.get_all_surveys()
```

### Customer Health Monitoring

```python
# Calculate health score (all components 0.0 - 1.0)
health = agent.calculate_health_score(
    "cust_001", engagement=0.8, satisfaction=0.7,
    financial=0.9, support=0.6, contract=0.85
)
print(f"Health Score: {health['health_score']:.3f}")

# Get health distribution
dist = agent.get_health_distribution()
print(f"Excellent: {dist['excellent']}, Good: {dist['good']}, Fair: {dist['fair']}")

# Get at-risk customers (low health scores)
at_risk = agent._health_monitor.get_at_risk_customers(threshold=0.3)
print(f"At-risk customers: {at_risk}")

# Health trend
trend = agent._health_monitor.get_health_trend("cust_001")
for entry in trend:
    print(f"  {entry['timestamp']}: score={entry['score']:.3f}")

# Current health score
score = agent._health_monitor.get_health_score("cust_001")

# Adjust weight configuration
agent._health_monitor.update_weight("engagement", 0.30)
```

### Renewal Management

```python
from datetime import datetime, timedelta

# Create renewal
renewal = agent.create_renewal(
    "cust_001", "ANNUAL",
    datetime.now() + timedelta(days=30), 12000.0
)
print(f"Renewal ID: {renewal['renewal_id']}")

# Get upcoming renewals
upcoming = agent.get_upcoming_renewals(days=30)
for r in upcoming:
    print(f"  {r['customer_id']}: due {r['renewal_date']}, ${r['amount']}")

# Get renewal stats
stats = agent.get_renewal_stats()
print(f"Renewal rate: {stats['renewal_rate']:.1%}")
print(f"Revenue renewed: ${stats['revenue_renewed']:,.2f}")
print(f"Revenue lost: ${stats['revenue_lost']:,.2f}")

# Get renewals for specific customer
cust_renewals = agent._renewal_manager.get_renewal_by_customer("cust_001")

# Update renewal status
agent._renewal_manager.update_renewal_status(
    renewal["renewal_id"], RenewalStatus.RENEWED, notes="Signed new 2-year contract"
)
```

### Contract Tracking

```python
# Create contract
contract = agent.create_contract(
    "cust_001", "ANNUAL",
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31),
    value=12000.0, auto_renew=True
)
print(f"Contract ID: {contract['contract_id']}")

# Get expiring contracts
expiring = agent._contract_tracker.get_expiring_contracts(days=30)
for c in expiring:
    print(f"  {c.customer_id}: expires {c.end_date.date()}")

# Get contracts for customer
cust_contracts = agent._contract_tracker.get_contracts_for_customer("cust_001")

# Terminate contract
agent._contract_tracker.terminate_contract(contract["contract_id"], reason="Customer requested cancellation")

# Contract stats
stats = agent.get_contract_stats()
print(f"Active contracts: {stats['active']}")
print(f"Total value: ${stats['total_value']:,.2f}")
for type_name, type_data in stats['by_type'].items():
    print(f"  {type_name}: {type_data['count']} contracts, ${type_data['value']:,.2f}")
```

### Sentiment Analysis

```python
# Analyze feedback text
result = agent.analyze_sentiment("cust_001", "Great product, very satisfied!")
print(f"Sentiment: {result['sentiment']}, Score: {result['score']:.3f}")

result = agent.analyze_sentiment("cust_001", "Terrible experience, very frustrated")
print(f"Sentiment: {result['sentiment']}, Score: {result['score']:.3f}")

# Get sentiment distribution
dist = agent.get_sentiment_distribution()
for level, count in dist.items():
    print(f"  {level}: {count}")

# Identify negative customers
negatives = agent._sentiment_analyzer.get_negative_customers(threshold=-0.2)
print(f"Negative customers: {negatives}")

# Sentiment trend
trend = agent._sentiment_analyzer.get_trend("cust_001")
for entry in trend:
    print(f"  {entry['sentiment']} ({entry['score']:.3f}) from {entry['source']}")

# Average sentiment
avg = agent._sentiment_analyzer.get_average_sentiment("cust_001")
print(f"Average sentiment: {avg:.3f}")
```

### Escalation Management

```python
# Create escalation
escalation = agent.create_escalation(
    "cust_001", "HIGH_CHURN_RISK",
    description="Churn score above 0.7, no response to outreach"
)
print(f"Escalation: {escalation['escalation_id']} (severity {escalation['severity']})")

# Get open escalations
open_esc = agent._escalation_engine.get_open_escalations()
for e in open_esc:
    print(f"  {e.customer_id}: {e.reason.name} (severity {e.severity})")

# Get escalation stats
stats = agent.get_escalation_stats()
print(f"Open: {stats['open']}, Resolved: {stats['resolved']}")
for reason, count in stats['by_reason'].items():
    print(f"  {reason}: {count}")

# Get escalations for customer
cust_esc = agent._escalation_engine.get_escalations_for_customer("cust_001")

# Resolve escalation
agent._escalation_engine.resolve_escalation(
    escalation["escalation_id"], resolution="Customer retained with 20% discount"
)

# Update escalation rule
agent._escalation_engine.update_rule(EscalationReason.HIGH_CHURN_RISK, severity=5, auto_assign=True)
```

### Churn Reason Analysis

```python
# Record churn reason with evidence
agent.add_churn_reason(
    "cust_001", "PRICE_SENSITIVITY",
    evidence=["Complained about pricing", "Compared to competitor X"]
)

# Get reason distribution
dist = agent.get_churn_reason_distribution()
for reason, count in sorted(dist.items(), key=lambda x: -x[1]):
    print(f"  {reason}: {count}")

# Top reasons
top = agent.get_top_churn_reasons(limit=5)
for item in top:
    print(f"  {item['reason']}: {item['count']} occurrences")

# Recoverable rate
recoverable = agent._churn_reason_analyzer.get_recoverable_rate()
print(f"Recoverable churn: {recoverable:.1%}")

# Average confidence
avg_conf = agent._churn_reason_analyzer.get_avg_confidence()
print(f"Average confidence: {avg_conf:.2f}")

# Reasons for specific customer
cust_reasons = agent._churn_reason_analyzer.get_reasons_for_customer("cust_001")
```

### Retention Strategies

```python
# Get recommendations
strategies = agent.get_retention_strategies("cust_001")
print(f"Recommended: {strategies}")

# Execute strategy
result = agent.execute_retention_strategy("cust_001", "DISCOUNT_OFFER")
print(f"Strategy executed: {result['strategy']}")

# View effectiveness
stats = agent.get_strategy_stats()
for strategy, data in stats.items():
    print(f"{strategy}: {data['count']} executed, {data['conversion_rate']:.1%} conversion")

# Get customer-specific strategies
cust_strategies = agent._strategy_engine.get_strategies_for_customer("cust_001")

# Cancel a strategy
agent._strategy_engine.cancel_strategy(result["strategy_id"])
```

### Win-Back Campaigns

```python
# Create campaign
agent.create_winback_campaign("wb_001", "Come Back Offer", "churned_30d")

# Enroll customers
agent.enroll_winback("wb_001", "cust_002")
agent.enroll_winback("wb_001", "cust_003")

# Track results
stats = agent.get_winback_stats("wb_001")
print(f"Targeted: {stats['total_targeted']}")
print(f"Converted: {stats['total_converted']}")
print(f"Rate: {stats['conversion_rate']:.1%}")

# Pause/resume campaigns
agent._winback_manager.pause_campaign("wb_001")
agent._winback_manager.resume_campaign("wb_001")

# Get all campaigns
campaigns = agent._winback_manager.get_all_campaigns()
```

### Cohort Analysis

```python
# Create cohort
agent.create_cohort("cohort_jan", "January 2024", "2024-01",
                    {"cust_001", "cust_002", "cust_003"})

# Get retention curve
curve = agent.get_retention_curve("cohort_jan")
for period in curve:
    print(f"Period {period['period_number']}: {period['retention_rate']}% retained")

# Compare cohorts
comparison = agent._cohort_analyzer.compare_cohorts(["cohort_jan", "cohort_feb"])

# Best/worst
best = agent._cohort_analyzer.get_best_cohort()
worst = agent._cohort_analyzer.get_worst_cohort()

# Summary
summary = agent.get_cohort_summary()
print(f"Total cohorts: {summary['total']}")
```

### Dashboard and Alerting

```python
# Get active alerts
alerts = agent.get_dashboard_alerts()
for a in alerts:
    print(f"  [{a['severity']}] {a['type']}: {a['message']}")

# Alert summary
summary = agent._dashboard.get_alert_summary()
print(f"Critical: {summary['critical']}, High: {summary['high']}")

# Take a metric snapshot
agent._dashboard.take_snapshot({
    "retention_rate": 0.85, "nps": 42,
    "health_avg": 0.72, "open_escalations": 3
})

# View snapshots
snapshots = agent._dashboard.get_snapshots(limit=5)

# Acknowledge alert
if alerts:
    agent._dashboard.acknowledge_alert(alerts[0]["alert_id"], acknowledged_by="admin")

# Clear acknowledged alerts
cleared = agent._dashboard.clear_acknowledged()
```

## API Reference

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `register_customer()` | id, name, email, revenue | Dict | Register customer |
| `update_customer_signal()` | id, signal, value | Dict | Track churn signal |
| `predict_churn()` | id | Dict | Predict churn risk |
| `predict_all_churn()` | - | Dict | Batch prediction |
| `add_loyalty_points()` | id, points, desc | Dict | Award points |
| `redeem_loyalty_points()` | id, points, reward_id | Dict | Redeem points |
| `get_loyalty_info()` | id | Dict | Get loyalty status |
| `send_nps_survey()` | id | Dict | Send NPS survey |
| `submit_nps_response()` | survey_id, score, feedback | Dict | Submit response |
| `get_nps_score()` | - | Dict | Get NPS score |
| `get_nps_trend()` | months | List | Get NPS trend |
| `calculate_health_score()` | id, engagement, satisfaction, financial, support, contract | Dict | Health score |
| `create_renewal()` | id, type, date, amount | Dict | Create renewal |
| `get_upcoming_renewals()` | days | List | Upcoming renewals |
| `create_contract()` | id, type, start, end, value, auto_renew | Dict | Create contract |
| `analyze_sentiment()` | id, text, source | Dict | Analyze sentiment |
| `create_escalation()` | id, reason, description | Dict | Create escalation |
| `add_churn_reason()` | id, reason, evidence | Dict | Record churn reason |
| `get_retention_strategies()` | id | List | Get recommendations |
| `execute_retention_strategy()` | id, strategy | Dict | Execute strategy |
| `create_winback_campaign()` | id, name, segment | Dict | Create campaign |
| `enroll_winback()` | campaign_id, customer_id | Dict | Enroll customer |
| `create_cohort()` | id, name, period, ids | Dict | Create cohort |
| `get_retention_curve()` | cohort_id | List | Get retention curve |
| `get_retention_rate()` | period_days | Dict | Get retention rate |
| `get_churn_rate()` | period_days | Dict | Get churn rate |
| `get_dashboard_alerts()` | - | List | Active alerts |
| `get_health_distribution()` | - | Dict | Health score distribution |
| `get_renewal_stats()` | - | Dict | Renewal metrics |
| `get_contract_stats()` | - | Dict | Contract metrics |
| `get_sentiment_distribution()` | - | Dict | Sentiment breakdown |
| `get_escalation_stats()` | - | Dict | Escalation metrics |
| `get_churn_reason_distribution()` | - | Dict | Churn reasons |
| `get_top_churn_reasons()` | limit | List | Top churn reasons |
| `get_status()` | - | Dict | Agent status |
| `get_full_report()` | - | Dict | Comprehensive report |
| `initialize()` | - | Dict | Initialize agent |
| `shutdown()` | - | Dict | Shutdown agent |

## Configuration

```yaml
agent:
  churn_threshold: 0.5
  nps_survey_interval_days: 90
  loyalty_points_per_dollar: 10.0
  retention_lookback_days: 30
  health_alert_threshold: 0.3
  renewal_warning_days: 30
  escalation_auto_assign: true
  sentiment_analysis_enabled: true

churn_signals:
  login_decrease: 0.3
  support_ticket_increase: 0.2
  feature_usage_decline: 0.25
  payment_failure: 0.4
  contract_near_expiry: 0.15
  negative_feedback: 0.35
  competitor_mention: 0.2
  downgrade_request: 0.5
  reduced_engagement: 0.2
  missed_renewal: 0.6

loyalty_tiers:
  bronze: { min_points: 0, multiplier: 1.0 }
  silver: { min_points: 1000, multiplier: 1.25 }
  gold: { min_points: 5000, multiplier: 1.5 }
  platinum: { min_points: 15000, multiplier: 2.0 }
  diamond: { min_points: 50000, multiplier: 3.0 }

health_weights:
  engagement: 0.25
  satisfaction: 0.25
  financial: 0.20
  support: 0.15
  contract: 0.15
```

## Best Practices

### Churn Prevention
1. Track signals daily for at-risk customers
2. Act within 48 hours of high-risk prediction
3. Combine multiple signals for accuracy
4. Track intervention outcomes
5. Build strategy playbooks
6. Review and adjust signal weights quarterly
7. Use batch predictions for weekly portfolio reviews
8. Correlate churn scores with actual churn events

### Loyalty Programs
1. Set achievable tier thresholds
2. Offer meaningful rewards at each tier
3. Communicate benefits clearly
4. Celebrate tier upgrades
5. Prevent point expiration frustration
6. Monitor redemption rates for program health
7. Run A/B tests on reward offerings
8. Track loyalty program ROI

### NPS Surveys
1. Survey at natural touchpoints
2. Follow up with detractors immediately
3. Amplify promoter feedback
4. Close the feedback loop
5. Segment NPS by customer type
6. Set response rate targets
7. Use NPS trend for quarterly business reviews

### Health Monitoring
1. Calculate health scores weekly
2. Set alert thresholds appropriate for your business
3. Investigate rapid health declines
4. Use health scores alongside churn predictions
5. Track component-level breakdowns
6. Adjust weights based on your customer base

### Renewal Management
1. Start renewal conversations 90 days before expiry
2. Track revenue retention, not just count
3. Escalate stalled renewals
4. Automate renewal reminders
5. Measure renewal rate by contract type

### Escalation Management
1. Define clear escalation triggers and severity levels
2. Ensure auto-assignment for critical cases
3. Track resolution times
4. Review escalation patterns monthly
5. Close the loop on every escalation

### Churn Root Cause Analysis
1. Record reasons for every churn event
2. Collect supporting evidence
3. Distinguish actionable vs non-actionable causes
4. Feed insights back to product and support teams
5. Track reason distribution trends over time

## Troubleshooting

**Churn scores seem inaccurate**
- Verify signal data quality and completeness
- Check signal weights for your business model
- Add more behavioral signals for better accuracy
- Review historical patterns and adjust thresholds
- Ensure sufficient signal history exists

**Low NPS response rate**
- Shorten survey to 1-2 questions
- Send at optimal touchpoints
- Offer incentive for completion
- Test different channels (email, in-app, SMS)

**Loyalty points not adding up**
- Check transaction records for gaps
- Verify tier multiplier calculations
- Review expiration logic
- Check for duplicate point awards

**Health scores not reflecting reality**
- Review weight configuration for your business
- Ensure all component metrics are collecting data
- Check for stale data in individual components
- Adjust thresholds based on your customer base

**Escalations not being created**
- Verify escalation reason names match enum values
- Check if rules are configured correctly
- Ensure customer exists before creating escalation
- Review auto-assignment settings

**Sentiment analysis seems off**
- Check keyword lists for domain-specific terms
- Add industry-specific positive/negative keywords
- Review score normalization
- Consider context beyond single words

**Renewals not appearing in pipeline**
- Verify renewal creation was successful
- Check date calculations for upcoming filter
- Confirm status is PENDING or INITIATED
- Review renewal_date vs current date

## Architecture Summary

The agent is built around 13 independent subsystems, each managed by a dedicated class with thread-safe state:

```
CustomerRetentionAgent (Orchestrator)
├── ChurnPredictor          - Signal-based churn scoring
├── LoyaltyManager          - Points, tiers, rewards
├── NPSManager              - Survey lifecycle and scoring
├── CohortAnalyzer          - Retention curves by cohort
├── RetentionStrategyEngine - Strategy recommendation and execution
├── WinbackManager          - Re-engagement campaigns
├── CustomerHealthMonitor   - Composite health scoring
├── RenewalManager          - Renewal pipeline tracking
├── ContractTracker         - Contract lifecycle management
├── SentimentAnalyzer       - Text sentiment analysis
├── EscalationEngine        - Account escalation management
├── ChurnReasonAnalyzer     - Churn root cause analysis
└── RetentionDashboard      - Centralized alerting and monitoring
```

Each subsystem uses `threading.Lock()` for thread safety and dictionary-based registries for O(1) lookups. The orchestrator delegates to subsystems and aggregates results into consistent dictionary responses.

## Thread Safety

All operations are thread-safe. Each manager acquires its own lock for both reads and writes, preventing race conditions without cross-manager contention.

```python
# Safe to call from multiple threads
import threading

def process_customer(agent, customer_id):
    agent.update_customer_signal(customer_id, "login_decrease", 0.5)
    pred = agent.predict_churn(customer_id)
    if pred["risk_level"] == "CRITICAL":
        agent.create_escalation(customer_id, "HIGH_CHURN_RISK")

threads = [
    threading.Thread(target=process_customer, args=(agent, f"cust_{i:03d}"))
    for i in range(100)
]
for t in threads:
    t.start()
for t in threads:
    t.join()
```

## Demo

Run the built-in demo to see all features in action:

```bash
python -m agents.customer_retention.agent
```

The demo registers 20 customers with random signals, runs churn predictions, manages loyalty points, sends NPS surveys, creates cohorts, generates escalations, analyzes sentiment, and produces a comprehensive report.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all existing tests pass
5. Update documentation (GROK.md, ARCHITECTURE.md, README.md)
6. Submit a pull request

## Support

- Check the Troubleshooting section above
- Review ARCHITECTURE.md for design details
- See GROK.md for operational guidelines and checklists

## Advanced Usage

### Custom Signal Weights

```python
# Customize churn signal weights for your business
agent._churn_predictor.update_signal_weight("missed_renewal", 0.8)
agent._churn_predictor.update_signal_weight("login_decrease", 0.4)

# Verify weights
weights = agent._churn_predictor.get_signal_weights()
```

### Health Score Tuning

```python
# Adjust health score weights for your business model
agent._health_monitor.update_weight("engagement", 0.35)
agent._health_monitor.update_weight("satisfaction", 0.20)
agent._health_monitor.update_weight("financial", 0.20)
agent._health_monitor.update_weight("support", 0.15)
agent._health_monitor.update_weight("contract", 0.10)
```

### Escalation Rule Customization

```python
from agents.customer_retention.agent import EscalationReason

# Make high churn risk more urgent
agent._escalation_engine.update_rule(
    EscalationReason.HIGH_CHURN_RISK, severity=5, auto_assign=True
)

# Make negative sentiment manual review
agent._escalation_engine.update_rule(
    EscalationReason.NEGATIVE_SENTIMENT, severity=2, auto_assign=False
)
```

### Batch Customer Processing

```python
# Register multiple customers
customers = [
    ("cust_001", "Acme Corp", 500),
    ("cust_002", "Beta Inc", 1200),
    ("cust_003", "Gamma LLC", 300),
]
for cid, name, rev in customers:
    agent.register_customer(cid, name=name, monthly_revenue=rev)

# Batch churn prediction
predictions = agent.predict_all_churn()
for pred in predictions["predictions"]:
    if pred["risk_level"] in ("HIGH", "CRITICAL"):
        print(f"ALERT: {pred['customer_id']} at {pred['risk_level']} risk")
```

### Exporting Data

```python
import json

# Export full report
report = agent.get_full_report()
with open("retention_report.json", "w") as f:
    json.dump(report, f, indent=2, default=str)

# Export churn predictions
predictions = agent.predict_all_churn()
with open("churn_predictions.json", "w") as f:
    json.dump(predictions, f, indent=2)
```

## Runtime Requirements

- Python 3.8+
- No external dependencies (uses only stdlib)
- Thread-safe for concurrent access
- In-memory storage (no database required)

## Data Storage

All data is stored in-memory using Python dictionaries. For persistence, implement a serialization layer that snapshots state to your preferred storage backend.

```python
# Example: serialize agent state
import pickle

# Save state
state = {
    "customers": agent._customers,
    "predictions": agent._churn_predictor._predictions,
    "loyalty_balances": dict(agent._loyalty_manager._balances),
}
with open("agent_state.pkl", "wb") as f:
    pickle.dump(state, f)

# Load state (requires custom deserialization logic)
```

## Performance Notes

- Churn prediction: ~25ms per customer
- Points operations: ~10ms each
- NPS calculation: ~50ms
- Health score: ~15ms per customer
- All operations are O(1) or O(n) where n is the operation size
- Thread contention is minimal due to per-manager locking

## Error Handling

The agent returns structured error dictionaries for expected failures:

```python
# Insufficient points
result = agent.redeem_loyalty_points("cust_001", 999999, "reward_001")
# Returns: {"error": "Insufficient points or invalid reward"}

# Survey not found
result = agent.submit_nps_response("nonexistent", 9)
# Returns: {"error": "Survey not found"}

# Campaign not found
result = agent.enroll_winback("nonexistent", "cust_001")
# Returns: {"enrolled": false, ...}
```

## Enum Values

```python
# ChurnRiskLevel
LOW, MEDIUM, HIGH, CRITICAL

# LoyaltyTier
BRONZE, SILVER, GOLD, PLATINUM, DIAMOND

# RetentionStrategy
ENGAGEMENT_INCREASE, DISCOUNT_OFFER, PERSONAL_OUTREACH, FEATURE_HIGHLIGHT,
LOYALTY_REWARD, EXIT_SURVEY, WINBACK_CAMPAIGN, SUCCESS_MANAGER

# RenewalStatus
PENDING, INITIATED, IN_NEGOTIATION, RENEWED, LOST, EXPIRED, CANCELLED

# SentimentLevel
VERY_NEGATIVE, NEGATIVE, NEUTRAL, POSITIVE, VERY_POSITIVE

# EscalationReason
HIGH_CHURN_RISK, NEGATIVE_SENTIMENT, PAYMENT_DEFAULT, SUPPORT_ESCALATION,
COMPETITOR_THREAT, CONTRACT_EXPIRY, USAGE_DECLINE, EXECUTIVE_SPONSOR_LOST

# ContractType
MONTHLY, ANNUAL, MULTI_YEAR, FREE_TRIAL, ENTERPRISE, CUSTOM

# ChurnReason
PRICE_SENSITIVITY, FEATURE_GAP, POOR_SUPPORT, COMPETITOR_SWITCH,
BUSINESS_CLOSURE, BUDGET_CUTS, LOW_ENGAGEMENT, PRODUCT_QUALITY,
ONBOARDING_FAILURE, CHAMPION_LEFT, CONTRACT_ISSUES, UNKNOWN
```

## Data Models

### Customer
Core entity representing a customer with all retention-relevant attributes.

### ChurnPrediction
Prediction result with risk level, score, signals, and recommended actions.

### RenewalRecord
Tracks a contract renewal through its lifecycle from pending to resolved.

### ContractInfo
Represents a contract with type, dates, value, and auto-renewal settings.

### SentimentEntry
A single sentiment analysis result from text feedback.

### EscalationRecord
An account escalation with reason, severity, and resolution tracking.

### ChurnReasonEntry
A recorded churn reason with confidence score and supporting evidence.

### RetentionAlert
An alert generated by the dashboard for conditions requiring attention.

## Lifecycle Methods

```python
# Initialize the agent (required before use)
status = agent.initialize()
# Returns: {"status": "initialized", "config": {...}}

# Shutdown the agent (cleanup)
status = agent.shutdown()
# Returns: {"status": "shutdown"}
```

## Batch Operations

```python
# Predict churn for all customers
all_predictions = agent.predict_all_churn()
# Returns sorted list and risk distribution

# Get loyalty tier distribution
tiers = agent.get_loyalty_tier_distribution()
# Returns count per tier

# Get strategy effectiveness stats
stats = agent.get_strategy_stats()
# Returns conversion rates per strategy type
```

## Report Generation

```python
# Comprehensive report with all metrics
report = agent.get_full_report()
# Includes: status, nps, risk_distribution, loyalty_tiers,
#           health_distribution, renewal_stats, contract_stats,
#           sentiment_distribution, escalation_stats, churn_reasons

# Status summary
status = agent.get_status()
# Returns: agent info, counts, rates, alert counts
```

## Changelog

### v2.0.0
- Added 7 new subsystems: Health Monitor, Renewal Manager, Contract Tracker, Sentiment Analyzer, Escalation Engine, Churn Reason Analyzer, Retention Dashboard
- Added 5 new enums: RenewalStatus, SentimentLevel, EscalationReason, ContractType, ChurnReason
- Added 6 new dataclasses: RenewalRecord, ContractInfo, SentimentEntry, EscalationRecord, ChurnReasonEntry, RetentionAlert
- Expanded Config with health, renewal, escalation, and sentiment options
- Added AsyncCustomerRetentionAgent with async methods
- Comprehensive documentation and troubleshooting

### v1.0.0
- Initial release with ChurnPredictor, LoyaltyManager, NPSManager
- CohortAnalyzer, RetentionStrategyEngine, WinbackManager
- Basic churn prediction with weighted signals
- Loyalty tier progression and rewards catalog
- NPS survey lifecycle and scoring
- Retention strategy recommendation and execution
- Win-back campaign management

## Glossary

| Term | Definition |
|------|-----------|
| Churn | Customer stopping use of product/service |
| NPS | Net Promoter Score (-100 to +100) |
| LTV | Lifetime Value - total revenue from customer |
| ARR | Annual Recurring Revenue |
| MRR | Monthly Recurring Revenue |
| Health Score | Composite metric of customer wellness (0-1) |
| Cohort | Group of customers sharing a characteristic |
| Escalation | Formal routing of at-risk account to management |
| Win-Back | Campaign to re-engage churned customers |
| Sentiment | Analysis of text feedback polarity |
| Churn Reason | Root cause category for customer departure |

## FAQ

**Q: Can I use this with a database backend?**
A: Yes. The agent is in-memory by default. Add a persistence layer by serializing state periodically to your database.

**Q: Is it thread-safe?**
A: Yes. Every manager uses its own `threading.Lock()` for all reads and writes.

**Q: What Python version is required?**
A: Python 3.8 or higher. No external dependencies.

**Q: Can I customize signal weights?**
A: Yes. Use `agent._churn_predictor.update_signal_weight(signal, weight)`.

**Q: How do I add custom churn reasons?**
A: Add new values to the `ChurnReason` enum and update `CHURN_REASON_WEIGHTS`.

**Q: Can I run multiple agent instances?**
A: Yes. Each instance is independent. Shard customers across instances for scale.

**Q: How do I integrate with my CRM?**
A: Use the public API methods to push/pull data. See the Integration Patterns section in GROK.md.

**Q: What happens if I call methods before initialize()?**
A: The agent will work but may not be fully configured. Always call `initialize()` first.

## Example: Complete Retention Workflow

```python
from agents.customer_retention.agent import CustomerRetentionAgent, Config
from datetime import datetime, timedelta

agent = CustomerRetentionAgent(Config())
agent.initialize()

# --- Setup Phase ---
# Register customers
for i in range(50):
    agent.register_customer(
        f"cust_{i:03d}",
        name=f"Customer {i}",
        monthly_revenue=100 + i * 20,
        contract_end_date=datetime.now() + timedelta(days=30 + i * 10)
    )

# Create loyalty rewards
agent.register_loyalty_reward("r_001", "10% Discount", 1000, "discount", 10.0)
agent.register_loyalty_reward("r_002", "Free Month", 5000, "free_product", 0.0)

# --- Monitoring Phase ---
# Track signals for each customer
for i in range(50):
    cid = f"cust_{i:03d}"
    agent.update_customer_signal(cid, "login_decrease", 0.3 + (i % 5) * 0.15)
    agent.update_customer_signal(cid, "feature_usage_decline", 0.2 + (i % 3) * 0.2)
    agent.add_loyalty_points(cid, 100 + i * 50)

# --- Analysis Phase ---
# Run churn predictions
predictions = agent.predict_all_churn()
print(f"Risk distribution: {predictions['risk_distribution']}")

# Calculate health scores
for i in range(50):
    cid = f"cust_{i:03d}"
    agent.calculate_health_score(
        cid,
        engagement=0.5 + (i % 4) * 0.15,
        satisfaction=0.6 + (i % 3) * 0.1,
        financial=0.7 + (i % 5) * 0.06,
        support=0.4 + (i % 6) * 0.1,
        contract=0.8 + (i % 2) * 0.1
    )

# Analyze sentiment
feedback_samples = [
    "Great product, love it!", "Terrible experience, very frustrated",
    "It works fine, nothing special", "Amazing support team!",
    "Missing key features I need", "Best tool we've ever used",
    "Waste of money, switching soon", "Pretty good overall"
]
for i in range(50):
    cid = f"cust_{i:03d}"
    text = feedback_samples[i % len(feedback_samples)]
    agent.analyze_sentiment(cid, text)

# --- Intervention Phase ---
# Identify at-risk customers and act
for pred in predictions["predictions"]:
    if pred["risk_level"] in ("HIGH", "CRITICAL"):
        cid = pred["customer_id"]
        
        # Get retention strategies
        strategies = agent.get_retention_strategies(cid)
        if strategies:
            agent.execute_retention_strategy(cid, strategies[0])
        
        # Create escalation for critical
        if pred["risk_level"] == "CRITICAL":
            agent.create_escalation(cid, "HIGH_CHURN_RISK",
                                    f"Score: {pred['risk_score']:.3f}")
        
        # Record churn reason
        agent.add_churn_reason(cid, "LOW_ENGAGEMENT",
                               evidence=[f"Risk score: {pred['risk_score']:.3f}"])

# --- Reporting Phase ---
report = agent.get_full_report()
print(f"\nRetention Rate: {report['status']['retention_rate']:.1%}")
print(f"NPS: {report['nps']['nps_score']}")
print(f"Health Distribution: {report['health_distribution']}")
print(f"Open Escalations: {report['status']['open_escalations']}")
print(f"Active Alerts: {report['status']['active_alerts']}")

agent.shutdown()
```

## License

MIT License. See LICENSE file for details.

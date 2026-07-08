# Affiliate Marketing Agent

> Partner management, commission tracking, fraud detection, and performance analytics for affiliate programs.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Reference](#api-reference)
7. [Examples](#examples)
8. [Configuration](#configuration)
9. [Best Practices](#best-practices)
10. [Troubleshooting](#troubleshooting)
11. [License](#license)

---

## Overview

The Affiliate Marketing Agent is a comprehensive system for managing affiliate programs. It handles the full lifecycle from partner recruitment through commission payout, with built-in fraud detection and performance analytics.

### What It Does

- **Partner Management**: Recruit, approve, tier, search, and manage affiliate partners
- **Commission Calculation**: Flexible rules (percentage, fixed, tiered, recurring, hybrid) with tier multipliers
- **Conversion Tracking**: Click, impression, and conversion event tracking with sub-ID support
- **Fraud Detection**: Multi-strategy engine detecting click fraud, bots, conversion stuffing, cookie hijacking
- **Attribution**: Five models (last click, first click, linear, time decay, position-based)
- **Payout Processing**: Multi-method payouts with balance tracking and reconciliation
- **Performance Reporting**: HTML, JSON, CSV, Markdown reports with scheduled delivery
- **Webhook Integration**: Event-driven notifications for all significant actions
- **Compliance**: GDPR, CCPA, FTC disclosure tracking built in

---

## Features

| Feature | Description |
|---------|-------------|
| Multi-Tier Partners | Bronze → Diamond with auto-upgrade and commission multipliers |
| Commission Rules | Percentage, fixed, tiered, recurring, hybrid with max caps |
| Fraud Detection | 10 fraud signal types with confidence scoring |
| Attribution Models | 5 models for conversion credit distribution |
| Creative Management | Asset lifecycle with CTR tracking and approval workflow |
| Payout Processing | PayPal, bank transfer, check, crypto, wire |
| Multi-Format Reports | HTML, JSON, CSV, Markdown with scheduling |
| Webhook Dispatch | Event-driven notifications with retry logic |
| Batch Operations | Import/export partners, batch commission calculations |
| Compliance | GDPR, CCPA, FTC disclosure enforcement |

---

## Quick Start

```python
from agents.affiliate_marketing.agent import AffiliateMarketingAgent

# Initialize agent
agent = AffiliateMarketingAgent()

# Recruit a partner
partner = agent.recruit_partner(
    name="Tech Blog",
    email="contact@techblog.com",
    website="https://techblog.com"
)

# Approve the partner
agent.approve_partner(partner.id)

# Track a click
agent.track_click(partner.id, "https://example.com/product")

# Track a conversion
result = agent.track_conversion(partner.id, "ORD-001", 99.99)
print(f"Commission: ${result['commission']:.2f}")

# Generate report
report = agent.generate_performance_report(fmt="markdown")
print(report)
```

### Run the Agent

```bash
python agents/affiliate-marketing/agent.py --create-partner
python agents/affiliate-marketing/agent.py --dashboard
python agents/affiliate-marketing/agent.py --report
python agents/affiliate-marketing/agent.py --fraud
```

---

## Installation

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
```

### Optional Dependencies

```bash
pip install requests aiohttp prometheus-client redis
```

---

## Usage

### Partner Lifecycle

```python
# Create partner
partner = agent.recruit_partner("Acme Corp", "acme@example.com")

# Check status
print(partner.status)  # PartnerStatus.PENDING

# Approve
agent.approve_partner(partner.id)
print(partner.status)  # PartnerStatus.ACTIVE

# Suspend (with reason)
agent.suspend_partner(partner.id, reason="Policy violation")

# Terminate
agent.terminate_partner(partner.id, reason="Fraud confirmed")
```

### Commission Configuration

```python
from agents.affiliate_marketing.agent import CommissionRule, CommissionType

# Percentage commission
rule = CommissionRule(
    rule_id="standard-15",
    name="Standard 15%",
    commission_type=CommissionType.PERCENTAGE,
    percentage_rate=0.15,
    min_sale_amount=25.0,
    max_commission=500.0,
)

# Tiered commission
tiered = CommissionRule(
    rule_id="volume-tiers",
    name="Volume Tiers",
    commission_type=CommissionType.TIERED,
    tiered_rates={"0": 0.10, "5000": 0.12, "25000": 0.15, "100000": 0.20},
)

agent.add_commission_rule(rule, partner_ids=[partner.id])
```

### Fraud Detection

```python
from agents.affiliate_marketing.agent import FraudDetectionEngine

engine = FraudDetectionEngine()

# Analyze for fraud
alerts = engine.analyze_clicks(click_events)
alerts += engine.analyze_conversions(conversion_events)

# Review and resolve
for alert in alerts:
    if alert.confidence > 0.9:
        print(f"HIGH CONFIDENCE: {alert.description}")
    engine.resolve_alert(alert.alert_id, notes="Investigated — legitimate")
```

### Reporting

```python
# HTML report
agent.generate_performance_report(fmt="html", output_path="report.html")

# JSON for API
data = agent.generate_performance_report(fmt="json")

# Markdown for docs
md = agent.generate_performance_report(fmt="markdown")

# CSV for spreadsheets
csv_data = agent.generate_performance_report(fmt="csv")

# Dashboard summary
summary = agent.get_dashboard_summary()
```

---

## API Reference

### AffiliateMarketingAgent

| Method | Description |
|--------|-------------|
| `recruit_partner(name, email, ...)` | Create new partner |
| `approve_partner(partner_id)` | Activate partner |
| `suspend_partner(partner_id, reason)` | Suspend partner |
| `terminate_partner(partner_id, reason)` | Terminate partner |
| `list_partners(status, tier, tag)` | Filter and list partners |
| `search_partners(query)` | Search partners by text |
| `get_top_partners(metric, limit)` | Top performers |
| `add_commission_rule(rule, partner_ids)` | Assign commission rules |
| `track_click(partner_id, url, ...)` | Track affiliate click |
| `track_conversion(partner_id, order_id, amount)` | Track sale conversion |
| `track_impression(partner_id, url)` | Track ad impression |
| `detect_fraud(clicks, conversions)` | Run fraud analysis |
| `get_fraud_alerts(resolved)` | Get fraud alerts |
| `resolve_fraud_alert(alert_id, notes)` | Resolve alert |
| `request_payout(partner_id, amount, method)` | Request payout |
| `process_payout(payout_id)` | Process payout |
| `generate_performance_report(...)` | Generate report |
| `get_dashboard_summary()` | Dashboard metrics |
| `register_webhook(url, events)` | Register webhook |
| `export_partners(fmt)` | Export partner data |
| `import_partners(data, fmt)` | Import partner data |

### Enums

| Enum | Values |
|------|--------|
| `PartnerTier` | BRONZE, SILVER, GOLD, PLATINUM, DIAMOND |
| `PartnerStatus` | PENDING, ACTIVE, SUSPENDED, TERMINATED, INACTIVE |
| `CommissionType` | PERCENTAGE, FIXED, TIERED, RECURRING, HYBRID |
| `FraudSignalType` | CLICK_FRAUD, CONVERSION_STUFFING, COOKIE_HIJACKING, FAKE_LEADS, SELF_REFERRAL, BOT_TRAFFIC, ... |
| `AttributionModel` | LAST_CLICK, FIRST_CLICK, LINEAR, TIME_DECAY, POSITION_BASED |
| `PayoutMethod` | PAYPAL, BANK_TRANSFER, CHECK, CRYPTO, WIRE |

---

## Examples

### Complete Affiliate Workflow

```python
from agents.affiliate_marketing.agent import AffiliateMarketingAgent, CommissionRule, CommissionType

agent = AffiliateMarketingAgent()

# 1. Set up commission structure
rule = CommissionRule(
    rule_id="standard",
    name="Standard 12%",
    commission_type=CommissionType.PERCENTAGE,
    percentage_rate=0.12,
)
agent.add_commission_rule(rule)

# 2. Recruit partner
partner = agent.recruit_partner(
    name="Review Site",
    email="reviews@example.com",
    website="https://reviews.example.com"
)
agent.approve_partner(partner.id)

# 3. Track activity
agent.track_click(partner.id, "https://shop.example.com/product")
agent.track_click(partner.id, "https://shop.example.com/product")
agent.track_impression(partner.id, "https://shop.example.com/banner")

# 4. Record conversion
result = agent.track_conversion(
    partner_id=partner.id,
    order_id="ORD-2026-0042",
    sale_amount=149.99,
    product_category="electronics"
)
print(f"Commission earned: ${result['commission']:.2f}")

# 5. Check dashboard
summary = agent.get_dashboard_summary()
print(f"Total sales: ${summary['total_sales']:,.2f}")

# 6. Generate monthly report
report = agent.generate_performance_report(period_days=30, fmt="html")
```

### Fraud Investigation Workflow

```python
# Generate test fraud data
import random
from datetime import datetime, timedelta

clicks = []
for i in range(200):
    clicks.append(TrackingEvent(
        event_id=f"click-{i}",
        partner_id="partner-001",
        event_type="click",
        timestamp=datetime.now() - timedelta(seconds=random.randint(1, 60)),
        ip_address="10.0.0.1",  # Same IP = suspicious
        user_agent="Bot/1.0",
        session_id="sess-1",
        cookie_id="cookie-1",
        url="https://example.com",
        referrer="",
        device_type="desktop",
        country="US",
    ))

# Detect fraud
alerts = agent.detect_fraud(clicks=clicks)
for alert in alerts:
    print(f"[{alert.severity.value}] {alert.signal_type.value}")
    print(f"  {alert.description}")
    print(f"  Confidence: {alert.confidence:.0%}")
```

---

## Configuration

```python
from agents.affiliate_marketing.agent import Config

config = Config(
    # Commission
    default_commission_rate=0.10,
    cookie_duration_days=30,
    attribution_model="last_click",

    # Fraud
    fraud_detection_enabled=True,
    fraud_confidence_threshold=0.8,

    # Partners
    auto_approve_partners=False,
    max_partners=10000,
    tier_upgrade_auto=True,

    # Payouts
    min_payout_threshold=50.0,
    payout_schedule="monthly",

    # Compliance
    gdpr_compliant=True,
    ccpa_compliant=True,
    ftc_disclosure_required=True,

    # Webhooks
    webhook_enabled=True,

    # Reporting
    report_formats=["html", "json", "csv"],
    output_directory="./reports",
)

agent = AffiliateMarketingAgent(config=config)
```

---

## Best Practices

1. **Start Conservative**: Use `auto_approve_partners=False` until you trust the recruitment process
2. **Layer Fraud Detection**: Enable all detection strategies, then whitelist known-good partners
3. **Set Max Commissions**: Always use `max_commission` caps to prevent runaway payouts
4. **Monitor Tier Upgrades**: Review auto-upgrades monthly to ensure fairness
5. **Audit Regularly**: Run `get_dashboard_summary()` weekly and investigate anomalies
6. **Use Webhooks**: Enable webhooks for real-time fraud alerts and payout notifications
7. **Compliance First**: Keep GDPR/CCPA/FTC enabled — regulations change fast
8. **Backup Data**: Export partner data regularly with `export_partners()`

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Partner can't track | Status not ACTIVE | Run `approve_partner(partner_id)` |
| Commission is $0 | No matching rules | Add rules or check `min_sale_amount` |
| Fraud alerts everywhere | Too sensitive | Lower threshold or whitelist partners |
| Payout fails | Insufficient balance | Check `total_commissions_earned - total_commissions_paid` |
| Report is empty | Wrong date range | Adjust `period_days` parameter |
| Tier not upgrading | Thresholds not met | Check partner's sales and conversion counts |
| Webhook not firing | Events not registered | Verify webhook events list includes the event type |

---

## Files

- `agent.py` — Full implementation with enums, dataclasses, engines, and CLI
- `ARCHITECTURE.md` — System architecture with ASCII diagrams
- `GROK.md` — Agent identity, capabilities, and usage patterns
- `README.md` — This file

---

## License

MIT License — see [LICENSE](../../LICENSE).

---

*Affiliate Marketing Agent v2.0 — Part of the Awesome Grok Skills collection.*

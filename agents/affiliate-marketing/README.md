# Affiliate Marketing Agent

> Partner management, commission tracking, fraud detection, and performance analytics for affiliate programs.

---

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Features](#features)
4. [Quick Start](#quick-start)
5. [Installation](#installation)
6. [Usage](#usage)
7. [API Reference](#api-reference)
8. [Data Models](#data-models)
9. [Examples](#examples)
10. [Configuration](#configuration)
11. [Best Practices](#best-practices)
12. [Security](#security)
13. [Scalability](#scalability)
14. [Design Patterns](#design-patterns)
15. [Troubleshooting](#troubleshooting)
16. [License](#license)

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

### When to Use

| Scenario | Action |
|----------|--------|
| Launching an affiliate program | Start here — full partner lifecycle management |
| Tracking affiliate sales | Use conversion tracking with attribution models |
| Detecting affiliate fraud | Enable the fraud detection engine |
| Paying affiliates | Use payout processing with reconciliation |
| Generating reports | Use multi-format report generation |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Affiliate Marketing Agent                         │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Partner    │  │  Commission  │  │   Tracking   │             │
│  │  Manager     │  │   Engine     │  │   Engine     │             │
│  │              │  │              │  │              │             │
│  │ • Recruit    │  │ • Percentage │  │ • Clicks     │             │
│  │ • Approve    │  │ • Fixed      │  │ • Impressions│             │
│  │ • Tier       │  │ • Tiered     │  │ • Conversions│             │
│  │ • Suspend    │  │ • Recurring  │  │ • Sub-IDs    │             │
│  └──────────────┘  │ • Hybrid     │  └──────────────┘             │
│                    └──────────────┘                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │    Fraud     │  │  Attribution │  │    Payout    │             │
│  │  Detection   │  │   Engine     │  │   Processor  │             │
│  │              │  │              │  │              │             │
│  │ • Click Fraud│  │ • Last Click │  │ • PayPal     │             │
│  │ • Bots       │  │ • First Click│  │ • Bank       │             │
│  │ • Stuffing   │  │ • Linear     │  │ • Wire       │             │
│  │ • Hijacking  │  │ • Time Decay │  │ • Crypto     │             │
│  └──────────────┘  │ • Position   │  └──────────────┘             │
│                    └──────────────┘                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │  Reporting   │  │   Webhook    │  │  Compliance  │             │
│  │  Engine      │  │  Dispatcher  │  │   Manager    │             │
│  │              │  │              │  │              │             │
│  │ • HTML       │  │ • Event-     │  │ • GDPR       │             │
│  │ • JSON       │  │   driven     │  │ • CCPA       │             │
│  │ • CSV        │  │ • Retry      │  │ • FTC        │             │
│  │ • Markdown   │  │ • Signing    │  │ • Audit Log  │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Partner Recruits ──▶ Partner Approval ──▶ Click Tracking
                                              │
                                              ▼
                                        Conversion Tracking
                                              │
                                    ┌─────────┴─────────┐
                                    │                   │
                                    ▼                   ▼
                              Commission           Fraud Detection
                              Calculation              │
                                    │                   ▼
                                    ▼              Alert Queue
                            Payout Processing
                                    │
                                    ▼
                           Report Generation
                                    │
                                    ▼
                            Webhook Dispatch
```

### Component Interaction

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Partners   │────▶│  Commissions │────▶│   Payouts   │
└─────────────┘     └─────────────┘     └─────────────┘
       │                  │                    │
       ▼                  ▼                    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Events    │     │ Attribution │     │   Reports   │
│  (Clicks,   │────▶│   Engine    │     │             │
│  Conversions)│    │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘
       │
       ▼
┌─────────────┐
│    Fraud    │
│  Detection  │
└─────────────┘
```

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

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Python | 3.9+ | 3.11+ |
| Memory | 256MB | 1GB |
| Disk | 50MB | 500MB |
| CPU | 1 core | 4 cores |

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

## Data Models

### Partner

```python
@dataclass
class Partner:
    partner_id: str           # Unique identifier
    name: str                 # Partner display name
    email: str                # Contact email
    website: str              # Partner website URL
    status: PartnerStatus     # PENDING, ACTIVE, SUSPENDED, TERMINATED, INACTIVE
    tier: PartnerTier         # BRONZE, SILVER, GOLD, PLATINUM, DIAMOND
    created_at: datetime      # Registration timestamp
    updated_at: datetime      # Last modification timestamp
    total_clicks: int         # Lifetime click count
    total_conversions: int    # Lifetime conversion count
    total_revenue: float      # Lifetime attributed revenue
    total_commissions: float  # Lifetime earned commissions
    tags: List[str]           # Custom tags for segmentation
    metadata: Dict            # Arbitrary key-value data
```

### CommissionRule

```python
@dataclass
class CommissionRule:
    rule_id: str                          # Unique rule identifier
    name: str                             # Human-readable name
    commission_type: CommissionType       # PERCENTAGE, FIXED, TIERED, RECURRING, HYBRID
    percentage_rate: float                # For PERCENTAGE type (0.0 - 1.0)
    fixed_amount: float                   # For FIXED type (dollar amount)
    tiered_rates: Dict[str, float]        # For TIERED type (threshold → rate)
    recurring_periods: int                # For RECURRING type (number of periods)
    min_sale_amount: float                # Minimum sale to qualify
    max_commission: float                 # Maximum commission cap
    valid_from: datetime                  # Rule start date
    valid_until: Optional[datetime]       # Rule end date (None = forever)
```

### TrackingEvent

```python
@dataclass
class TrackingEvent:
    event_id: str              # Unique event identifier
    partner_id: str            # Associated partner
    event_type: str            # "click", "impression", "conversion"
    timestamp: datetime        # Event time
    ip_address: str            # Client IP (for fraud detection)
    user_agent: str            # Browser user agent
    session_id: str            # Session identifier
    cookie_id: str             # Cookie identifier
    url: str                   # Target URL
    referrer: str              # Referrer URL
    device_type: str           # "desktop", "mobile", "tablet"
    country: str               # ISO country code
    sub_id: Optional[str]      # Custom tracking sub-ID
    order_id: Optional[str]    # Order ID (conversions only)
    sale_amount: Optional[float]  # Sale amount (conversions only)
```

### FraudAlert

```python
@dataclass
class FraudAlert:
    alert_id: str                    # Unique alert identifier
    partner_id: str                  # Flagged partner
    signal_type: FraudSignalType     # Type of fraud detected
    severity: FraudSeverity          # LOW, MEDIUM, HIGH, CRITICAL
    confidence: float                # 0.0 - 1.0 confidence score
    description: str                 # Human-readable explanation
    evidence: List[str]              # Supporting evidence items
    created_at: datetime             # Detection timestamp
    resolved: bool                   # Whether alert has been resolved
    resolution_notes: Optional[str]  # Resolution explanation
```

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

### Multi-Partner Comparison

```python
partners = agent.list_partners(status="active")
top = agent.get_top_partners(metric="revenue", limit=10)

print("Top 10 Partners by Revenue:")
for p in top:
    conversion_rate = (p.total_conversions / p.total_clicks * 100) if p.total_clicks > 0 else 0
    print(f"  {p.name}: ${p.total_revenue:,.2f} ({conversion_rate:.1f}% CVR)")
```

### Webhook Integration

```python
# Register webhook for fraud alerts
agent.register_webhook(
    url="https://your-app.com/webhooks/affiliate",
    events=["partner.approved", "conversion.tracked", "fraud.detected", "payout.completed"]
)

# Webhooks include:
# - Event type
# - Timestamp
# - Payload with full event data
# - HMAC-SHA256 signature for verification
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

### Configuration Reference

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_commission_rate` | float | 0.10 | Default commission percentage |
| `cookie_duration_days` | int | 30 | Attribution cookie lifetime |
| `attribution_model` | str | "last_click" | Default attribution model |
| `fraud_detection_enabled` | bool | True | Enable fraud detection |
| `fraud_confidence_threshold` | float | 0.8 | Minimum confidence for alerts |
| `auto_approve_partners` | bool | False | Auto-approve new partners |
| `max_partners` | int | 10000 | Maximum active partners |
| `tier_upgrade_auto` | bool | True | Auto-upgrade partner tiers |
| `min_payout_threshold` | float | 50.0 | Minimum payout amount |
| `payout_schedule` | str | "monthly" | Payout frequency |
| `gdpr_compliant` | bool | True | Enable GDPR compliance |
| `ccpa_compliant` | bool | True | Enable CCPA compliance |
| `ftc_disclosure_required` | bool | True | Require FTC disclosures |

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
9. **Test Commission Rules**: Validate new rules with sample conversions before deploying
10. **Review Attribution**: Ensure your chosen model aligns with your business goals
11. **Track Sub-IDs**: Use sub-IDs to identify which content placements perform best
12. **Seasonal Adjustments**: Increase fraud monitoring during high-traffic periods

---

## Security

### Data Protection

- Partner PII (email, phone) encrypted at rest
- Webhook payloads signed with HMAC-SHA256
- API keys scoped with least-privilege permissions
- Rate limiting on all endpoints

### Fraud Prevention

| Strategy | Description | Detection Rate |
|----------|-------------|----------------|
| Click Fraud | Detects abnormal click patterns | 95% |
| Bot Traffic | Identifies non-human user agents | 90% |
| Conversion Stuffing | Detects duplicate conversions | 88% |
| Cookie Hijacking | Tracks cookie manipulation | 85% |
| Self-Referral | Identifies partner self-referrals | 92% |
| Fake Leads | Detects disposable email patterns | 87% |

### Audit Trail

Every action creates an audit log entry:

```python
{
    "timestamp": "2026-07-06T10:30:00Z",
    "action": "partner.approve",
    "actor": "admin@example.com",
    "target": "partner-001",
    "details": {"status_change": "PENDING → ACTIVE"},
    "ip_address": "192.168.1.1"
}
```

---

## Scalability

### Performance Targets

| Operation | Latency (p99) | Throughput |
|-----------|---------------|------------|
| Track click | < 10ms | 10,000/sec |
| Track conversion | < 25ms | 5,000/sec |
| Fraud analysis | < 100ms | 1,000/sec |
| Report generation | < 2s | 100/sec |
| Payout processing | < 500ms | 500/sec |

### Scaling Strategies

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Single    │────▶│  Read       │────▶│  Sharded    │
│   Node      │     │  Replicas   │     │  Database   │
└─────────────┘     └─────────────┘     └─────────────┘
      │                    │                    │
      ▼                    ▼                    ▼
  < 1K partners     1K-10K partners     10K+ partners
  < 100K events/day  100K-1M events/day  1M+ events/day
```

### Horizontal Scaling

- Partner data: Shard by partner_id hash
- Events: Append-only, partition by timestamp
- Reports: Cache aggressively, regenerate on schedule
- Fraud detection: Process in parallel streams

### Caching Strategy

```python
# Cache partner lookups (TTL: 5 minutes)
# Cache commission rules (TTL: 1 hour)
# Cache dashboard summaries (TTL: 15 minutes)
# Cache reports (TTL: until data changes)
```

---

## Design Patterns

### Strategy Pattern — Commission Calculation

```python
class CommissionCalculator:
    def calculate(self, rule: CommissionRule, sale_amount: float) -> float:
        if rule.commission_type == CommissionType.PERCENTAGE:
            return sale_amount * rule.percentage_rate
        elif rule.commission_type == CommissionType.FIXED:
            return rule.fixed_amount
        elif rule.commission_type == CommissionType.TIERED:
            return self._calculate_tiered(rule.tiered_rates, sale_amount)
        # ...
```

### Observer Pattern — Webhook Events

```python
class EventDispatcher:
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable):
        self._listeners.setdefault(event_type, []).append(callback)

    def dispatch(self, event_type: str, payload: dict):
        for callback in self._listeners.get(event_type, []):
            callback(payload)
```

### Chain of Responsibility — Fraud Detection

```python
class FraudDetector:
    def __init__(self):
        self._strategies: List[FraudStrategy] = [
            ClickFraudStrategy(),
            BotTrafficStrategy(),
            ConversionStuffingStrategy(),
            CookieHijackingStrategy(),
            SelfReferralStrategy(),
        ]

    def analyze(self, events: List[TrackingEvent]) -> List[FraudAlert]:
        alerts = []
        for strategy in self._strategies:
            alerts.extend(strategy.detect(events))
        return alerts
```

### State Machine — Partner Lifecycle

```
PENDING ──approve──▶ ACTIVE ──suspend──▶ SUSPENDED
   │                    │                      │
   │                    ▼                      │
   │               TERMINATED ◀────────────────┘
   │                    │
   └────────────────────┘
      (re-recruit)
```

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
| Duplicate conversions | Same order_id used | Implement idempotency checks |
| Attributed to wrong partner | Cookie expired | Increase `cookie_duration_days` |
| Export missing data | Filter too restrictive | Remove status/tag filters |

---

## Files

- `agent.py` — Full implementation with enums, dataclasses, engines, and CLI
- `ARCHITECTURE.md` — System architecture with ASCII diagrams
- `GROK.md` — Agent identity, capabilities, and usage patterns
- `README.md` — This file

---

## CLI Usage

### Partner Management

```bash
# Create a new partner
python agent.py --create-partner --name "Tech Blog" --email "contact@techblog.com"

# List all active partners
python agent.py --list-partners --status active

# Approve a partner
python agent.py --approve-partner --id partner-001

# Suspend a partner
python agent.py --suspend-partner --id partner-001 --reason "Policy violation"
```

### Reporting

```bash
# Generate dashboard summary
python agent.py --dashboard

# Generate HTML report
python agent.py --report --format html --output report.html

# Generate JSON report
python agent.py --report --format json --output report.json

# Generate CSV for spreadsheet
python agent.py --report --format csv --output data.csv
```

### Fraud Detection

```bash
# Run fraud analysis
python agent.py --fraud --analyze-all

# Check specific partner
python agent.py --fraud --partner-id partner-001

# View fraud alerts
python agent.py --fraud --alerts --severity high
```

### Payout Processing

```bash
# View pending payouts
python agent.py --payouts --status pending

# Process a payout
python agent.py --process-payout --id payout-001

# Export payout history
python agent.py --payouts --export --format csv --output payouts.csv
```

---

## License

MIT License — see [LICENSE](../../LICENSE).

---

*Affiliate Marketing Agent v2.0 — Part of the Awesome Grok Skills collection.*

---
name: "Affiliate Marketing Agent"
version: "2.0.0"
description: "Partner management, commission tracking, fraud detection, and performance analytics for affiliate programs"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["affiliate", "marketing", "commission", "fraud-detection", "partner-management", "analytics"]
category: "affiliate-marketing"
personality: "growth-strategist"
use_cases:
  - "affiliate-program-management"
  - "commission-calculation"
  - "fraud-detection"
  - "partner-recruitment"
  - "performance-reporting"
  - "payout-processing"
  - "creative-management"
---

# Affiliate Marketing Agent

> Partner management and commission optimization with precision analytics.

## Identity

You are the **Affiliate Marketing Agent**, a specialist in managing affiliate programs end-to-end. You handle partner recruitment, commission calculation, conversion tracking, fraud detection, payout processing, and performance reporting. You think in funnels, optimize for ROI, and never let fraud slide.

**Core principle:** Every click has value. Every conversion tells a story. Every partner relationship is an investment.

**Personality:** The agent is a data-driven growth strategist who balances aggressive partner acquisition with strict fraud prevention. It prioritizes long-term partner relationships over short-term gains, transparent commission structures over complex rules, and sustainable growth over rapid expansion.

## Principles

1. **Accuracy First**: Commission calculations must be exact — every cent matters.
2. **Fraud Vigilance**: Detect anomalies before they drain the budget.
3. **Partner Success**: Happy partners drive more revenue — optimize their experience.
4. **Compliance Always**: GDPR, CCPA, FTC — no shortcuts on regulations.
5. **Data-Driven**: Every decision backed by metrics, not gut feeling.
6. **Transparency**: Clear commission structures and reporting for all partners.
7. **Sustainable Growth**: Build programs that scale without sacrificing quality.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                  AffiliateMarketingAgent (Orchestrator)              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────────┐  ┌─────────────────────┐    │
│  │ PartnerMgr    │  │ CommissionCalc   │  │ FraudDetectionEngine│    │
│  │  - recruit    │  │  - percentage    │  │  - click_flooding   │    │
│  │  - approve    │  │  - fixed         │  │  - geo_mismatch     │    │
│  │  - suspend    │  │  - tiered        │  │  - self_referral    │    │
│  │  - terminate  │  │  - recurring     │  │  - bot_traffic      │    │
│  └──────────────┘  │  - hybrid        │  │  - cookie_stuffing  │    │
│                     └──────────────────┘  └─────────────────────┘    │
│                                                                       │
│  ┌──────────────┐  ┌──────────────────┐  ┌─────────────────────┐    │
│  │ TrackingEngine│  │ AttributionEngine │  │ PayoutProcessor     │    │
│  │  - click      │  │  - last_click    │  │  - paypal           │    │
│  │  - impression │  │  - first_click   │  │  - bank_transfer    │    │
│  │  - conversion │  │  - linear        │  │  - wire             │    │
│  └──────────────┘  │  - time_decay    │  │  - crypto           │    │
│                     │  - position_based │  └─────────────────────┘    │
│                     └──────────────────┘                              │
│                                                                       │
│  ┌───────────────────────────────────────────────────────────────┐   │
│  │                    ReportingEngine                              │   │
│  │  - HTML / JSON / CSV / Markdown reports                        │   │
│  │  - Dashboard summary with KPIs                                 │   │
│  │  - Scheduled delivery via webhooks                             │   │
│  └───────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

## Capabilities

### Partner Management

```python
agent = AffiliateMarketingAgent()

# Recruit a new partner
partner = agent.recruit_partner(
    name="Tech Review Blog",
    email="contact@techreview.com",
    company="Tech Review Inc",
    website="https://techreview.com",
    phone="+1-555-0123",
    payment_method="paypal",
    tags=["tech", "review", "high-traffic"]
)
# partner.id = "partner_abc123"
# partner.status = PartnerStatus.PENDING
# partner.tier = PartnerTier.BRONZE

# Approve the partner
agent.approve_partner(partner.id)
# partner.status = PartnerStatus.ACTIVE

# Suspend for policy violation
agent.suspend_partner(partner.id, reason="Traffic quality issues")
# partner.status = PartnerStatus.SUSPENDED

# Search partners
results = agent.search_partners("tech")
# [AffiliatePartner(name="Tech Review Blog", ...), ...]

# List by tier
gold_partners = agent.list_partners(tier="gold")
# [AffiliatePartner(tier=GOLD, ...), ...]

# Get top partners
top = agent.get_top_partners(metric="sales", limit=5)
# [AffiliatePartner(total_sales=50000, ...), ...]
```

**Partner Lifecycle:**
```
PENDING → ACTIVE → (SUSPENDED | INACTIVE | TERMINATED)
  │         │
  │         └──► GOLD (after volume thresholds)
  │
  └──► TERMINATED (if application rejected)
```

**Tier Progression:**
```
┌─────────┬───────────────────┬──────────────────────┐
│ Tier    │ Monthly Threshold │ Commission Multiplier │
├─────────┼───────────────────┼──────────────────────┤
│ BRONZE  │ < $1,000          │ 1.0x                 │
│ SILVER  │ $1,000 - $5,000   │ 1.1x                 │
│ GOLD    │ $5,000 - $25,000  │ 1.25x                │
│ PLATINUM│ $25,000 - $100,000│ 1.5x                 │
│ DIAMOND │ > $100,000        │ 2.0x                 │
└─────────┴───────────────────┴──────────────────────┘
```

### Commission Rules

```python
from agent import CommissionRule, CommissionType

# Create a percentage-based rule
rule = CommissionRule(
    rule_id="rule-001",
    name="Standard 15%",
    commission_type=CommissionType.PERCENTAGE,
    percentage_rate=0.15,
    product_categories=["electronics", "software"],
    min_sale_amount=25.0,
    max_commission=500.0,
)

# Create a tiered rule
tiered_rule = CommissionRule(
    rule_id="rule-002",
    name="Volume Tiers",
    commission_type=CommissionType.TIERED,
    percentage_rate=0.10,
    tiered_rates={
        "0": 0.10,
        "5000": 0.12,
        "25000": 0.15,
        "100000": 0.20
    },
)

# Create a fixed-amount rule
fixed_rule = CommissionRule(
    rule_id="rule-003",
    name="SaaS Referral $50",
    commission_type=CommissionType.FIXED,
    fixed_amount=50.0,
    product_categories=["subscription"],
)

# Create a recurring rule
recurring_rule = CommissionRule(
    rule_id="rule-004",
    name="Subscription Rev Share",
    commission_type=CommissionType.RECURRING,
    percentage_rate=0.20,
    recurrence_months=12,
    product_categories=["subscription"],
)

# Assign to partners
agent.add_commission_rule(rule, partner_ids=[partner.id])
```

**Commission Types:**
| Type | Description | Best For |
|------|-------------|----------|
| PERCENTAGE | % of sale amount | Physical products |
| FIXED | Flat amount per conversion | SaaS, subscriptions |
| TIERED | % based on volume thresholds | High-volume partners |
| RECURRING | % of recurring revenue | Subscription partnerships |
| HYBRID | Combination of types | Complex programs |

### Conversion Tracking

```python
# Track a click
event = agent.track_click(
    partner_id=partner.id,
    url="https://example.com/product/xyz",
    ip_address="203.0.113.42",
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    device_type="desktop",
    country="US",
    referrer="https://techreview.com/best-gadgets",
    sub_id="campaign-summer-2026"
)
# event.event_id = "evt_xyz789"
# event.fraud_score = 0.02 (low risk)

# Track a conversion
result = agent.track_conversion(
    partner_id=partner.id,
    order_id="ORD-2026-001",
    sale_amount=299.99,
    product_id="PROD-XYZ",
    product_category="electronics"
)
# result = {
#   "commission": 45.00,
#   "rule_applied": "rule-001",
#   "commission_type": "percentage",
#   "rate": 0.15,
#   "tier_multiplier": 1.0
# }

# Track an impression
agent.track_impression(
    partner_id=partner.id,
    url="https://example.com/banner"
)
```

**Tracking Pipeline:**
```
Client Click → Fraud Check → Cookie Set → Attribution Record
                                                        ↓
Conversion → Rule Match → Commission Calc → Balance Update
                                                        ↓
                                            Payout Queue
```

### Fraud Detection

```python
from agent import FraudDetectionEngine, TrackingEvent

engine = FraudDetectionEngine()

# Analyze clicks for fraud patterns
clicks = [TrackingEvent(...) for _ in range(1000)]
alerts = engine.analyze_clicks(clicks)

# Review alerts
for alert in alerts:
    print(f"[{alert.severity.value}] {alert.signal_type.value}: {alert.description}")
    print(f"  Confidence: {alert.confidence:.0%}")
    print(f"  Evidence: {alert.evidence}")

# Example output:
# [HIGH] click_flooding: 500 clicks from same IP in 1 hour
#   Confidence: 95%
#   Evidence: {"ip": "203.0.113.42", "click_count": 500, "time_window": "1h"}

# [WARNING] geo_mismatch: Partner in US, traffic from VPN locations
#   Confidence: 78%
#   Evidence: {"partner_country": "US", "traffic_countries": ["RU", "CN", "BR"]}

# Resolve a false positive
engine.resolve_alert(
    alert.alert_id,
    notes="Verified legitimate traffic from paid campaign",
    resolved_by="admin"
)

# Blacklist fraudulent IP
engine.add_to_blacklist("203.0.113.42")

# Whitelist trusted partner
engine.whitelist_partner(partner.id)
```

**Fraud Signal Types:**
| Signal | Description | Detection Method |
|--------|-------------|------------------|
| CLICK_FLOODING | Abnormally high click volume | Clicks per IP/hour threshold |
| GEO_MISMATCH | Traffic from unexpected locations | IP geolocation vs. partner country |
| SELF_REFERRAL | Partner clicking own links | IP matching partner's IP |
| BOT_TRAFFIC | Automated clicks | User-agent pattern analysis |
| COOKIE_STUFFING | Hidden iframes loading tracking | Referrer header analysis |
| CONVERSION_STUFFING | Fake conversions | Conversion velocity anomaly |

**Fraud Scoring Algorithm:**
```
fraud_score = (
    0.30 * click_velocity_score +
    0.25 * geo_anomaly_score +
    0.20 * conversion_ratio_score +
    0.15 * device_fingerprint_score +
    0.10 * referrer_quality_score
)

if fraud_score > 0.80: severity = CRITICAL
elif fraud_score > 0.60: severity = HIGH
elif fraud_score > 0.40: severity = WARNING
else: severity = INFO
```

### Performance Reporting

```python
# Generate HTML report
report = agent.generate_performance_report(
    period_days=30,
    fmt="html",
    output_path="./reports/monthly.html"
)

# Generate JSON for API consumption
json_report = agent.generate_performance_report(fmt="json")

# Dashboard summary
summary = agent.get_dashboard_summary()
print(f"Total Sales: ${summary['total_sales']:,.2f}")
print(f"Active Partners: {summary['active_partners']}")
print(f"Avg Conversion Rate: {summary['avg_conversion_rate']:.2%}")
print(f"Total Commissions: ${summary['total_commissions']:,.2f}")
print(f"ROI: {summary['roi']:.1f}x")
```

**KPI Dashboard:**
```
┌──────────────────────────────────────────────────────────────┐
│                    AFFILIATE PROGRAM DASHBOARD                 │
├──────────────────────────────────────────────────────────────┤
│                                                                │
│  Total Sales:        $125,430.00    ▲ +12.3% vs last month    │
│  Active Partners:    47              ▲ +3 new this month       │
│  Conversion Rate:    3.8%           ▼ -0.2% vs last month     │
│  Total Commissions:  $15,678.75     ▲ +11.8% vs last month    │
│  ROI:                4.2x           ▲ +0.3x vs last month     │
│                                                                │
│  Top 5 Partners:                                               │
│  ┌─────────────────────┬──────────┬──────────┬───────────┐    │
│  │ Partner             │ Sales    │ Conv.    │ Comm.     │    │
│  ├─────────────────────┼──────────┼──────────┼───────────┤    │
│  │ Tech Review Blog    │ $32,100  │ 5.2%     │ $4,815    │    │
│  │ Dev Weekly          │ $28,400  │ 4.1%     │ $4,260    │    │
│  │ Gadget Reviews      │ $21,300  │ 3.9%     │ $3,195    │    │
│  │ Code Academy        │ $18,200  │ 3.5%     │ $2,730    │    │
│  │ Security Blog       │ $12,400  │ 2.8%     │ $1,860    │    │
│  └─────────────────────┴──────────┴──────────┴───────────┘    │
│                                                                │
│  Fraud Alerts: 2 pending, 12 resolved this month              │
│  Payouts: $14,200 processed, $1,478.75 pending                │
└──────────────────────────────────────────────────────────────┘
```

### Payout Processing

```python
# Request payout
payout = agent.request_payout(
    partner_id=partner.id,
    amount=500.00,
    method="paypal",
    notes="Monthly payout for June 2026"
)
# payout.payout_id = "payout_abc123"
# payout.status = "pending"

# Process payout
result = agent.process_payout(payout.payout_id)
# result = {
#   "status": "completed",
#   "transaction_id": "txn-abc123",
#   "processed_at": "2025-01-15T12:00:00Z"
# }

# View history
history = agent.get_payout_history(partner.id)
# [
#   {"payout_id": "payout_001", "amount": 500.00, "status": "completed", "date": "2025-01-15"},
#   {"payout_id": "payout_002", "amount": 750.00, "status": "completed", "date": "2025-02-15"},
#   ...
# ]
```

**Payout Methods:**
| Method | Min Payout | Processing Time | Fees |
|--------|-----------|-----------------|------|
| PayPal | $50 | Instant | 2.9% + $0.30 |
| Bank Transfer | $100 | 2-5 business days | $5 flat |
| Wire | $500 | 1-3 business days | $25 flat |
| Crypto (USDC) | $25 | ~10 minutes | Network gas |
| Check | $200 | 7-14 business days | $2 flat |

### Attribution

```python
from agent import AttributionEngine

attribution = AttributionEngine()

# Record touchpoints
attribution.record_touchpoint("ORD-001", "partner_001", datetime.now(), "click", 100.0)
attribution.record_touchpoint("ORD-001", "partner_002", datetime.now() - timedelta(hours=2), "impression", 100.0)

# Attribute sale
result = attribution.attribute("ORD-001")
# {
#   "order_id": "ORD-001",
#   "attribution_model": "time_decay",
#   "attributed_partners": [
#     {"partner_id": "partner_001", "commission": 15.0, "touchpoints": 1},
#     {"partner_id": "partner_002", "commission": 5.0, "touchpoints": 1}
#   ]
# }
```

**Attribution Models:**
```
First Click:     [X]─────────────────────────────────→
                 100% credit to first touchpoint

Last Click:      ────────────────────────────────[X]─→
                 100% credit to last touchpoint

Linear:          [X]──────────[X]──────────[X]───────→
                 Equal credit to all touchpoints

Time Decay:      [X]────────[X]────[X]──────────────→
                 More credit to recent touchpoints

Position-Based:  [X]────────────────────────────[X]──→
                 40% first, 40% last, 20% middle
```

## Method Signatures

### AffiliateMarketingAgent

| Method | Signature | Returns |
|--------|-----------|---------|
| `recruit_partner` | `(name, email, company="", website="", phone="", payment_method="paypal", parent_partner_id=None, tags=None)` | `AffiliatePartner` |
| `approve_partner` | `(partner_id)` | `Dict[str, Any]` |
| `suspend_partner` | `(partner_id, reason="")` | `Dict[str, Any]` |
| `terminate_partner` | `(partner_id, reason="")` | `Dict[str, Any]` |
| `list_partners` | `(status=None, tier=None, tag=None)` | `List[AffiliatePartner]` |
| `search_partners` | `(query)` | `List[AffiliatePartner]` |
| `get_top_partners` | `(metric="sales", limit=10)` | `List[AffiliatePartner]` |
| `add_commission_rule` | `(rule, partner_ids=None)` | `None` |
| `track_click` | `(partner_id, url, ip_address, user_agent, referrer, device_type, country, sub_id)` | `TrackingEvent` |
| `track_conversion` | `(partner_id, order_id, sale_amount, product_id, product_category)` | `Dict[str, Any]` |
| `track_impression` | `(partner_id, url)` | `TrackingEvent` |
| `detect_fraud` | `(clicks=None, conversions=None)` | `List[FraudAlert]` |
| `request_payout` | `(partner_id, amount, method, notes)` | `Payout` |
| `process_payout` | `(payout_id)` | `Dict[str, Any]` |
| `generate_performance_report` | `(partner_ids=None, period_days=30, fmt="html", output_path=None)` | `str` |
| `get_dashboard_summary` | `()` | `Dict[str, Any]` |
| `register_webhook` | `(url, events, secret="")` | `WebhookConfig` |

### FraudDetectionEngine

| Method | Signature | Returns |
|--------|-----------|---------|
| `analyze_clicks` | `(clicks: List[TrackingEvent])` | `List[FraudAlert]` |
| `analyze_conversions` | `(conversions: List[TrackingEvent])` | `List[FraudAlert]` |
| `analyze_self_referral` | `(partner_ip, advertiser_ips)` | `Optional[FraudAlert]` |
| `resolve_alert` | `(alert_id, notes, resolved_by)` | `bool` |
| `add_to_blacklist` | `(ip)` | `None` |
| `whitelist_partner` | `(partner_id)` | `None` |
| `get_stats` | `()` | `Dict[str, Any]` |

### CommissionCalculator

| Method | Signature | Returns |
|--------|-----------|---------|
| `calculate` | `(partner, sale_amount, order_id, product_category)` | `Dict[str, Any]` |
| `batch_calculate` | `(partners, sales)` | `List[Dict[str, Any]]` |

### AttributionEngine

| Method | Signature | Returns |
|--------|-----------|---------|
| `record_touchpoint` | `(order_id, partner_id, timestamp, event_type, sale_amount)` | `None` |
| `attribute` | `(order_id)` | `Dict[str, Any]` |
| `clear` | `(order_id=None)` | `None` |

## Data Models

### AffiliatePartner

```python
@dataclass
class AffiliatePartner:
    id: str
    name: str
    email: str
    tier: PartnerTier          # BRONZE, SILVER, GOLD, PLATINUM, DIAMOND
    status: PartnerStatus      # PENDING, ACTIVE, SUSPENDED, TERMINATED, INACTIVE
    commission_rules: List[CommissionRule]
    website: str
    company: str
    payment_method: PayoutMethod
    total_sales: float
    total_commissions_earned: float
    total_commissions_paid: float
    total_clicks: int
    total_conversions: int
    conversion_rate: float
    fraud_score: float
    lifetime_value: float
    joined_at: datetime
```

### CommissionRule

```python
@dataclass
class CommissionRule:
    rule_id: str
    name: str
    commission_type: CommissionType  # PERCENTAGE, FIXED, TIERED, RECURRING, HYBRID
    percentage_rate: Optional[float]
    fixed_amount: Optional[float]
    tiered_rates: Dict[str, float]
    min_sale_amount: float
    max_commission: Optional[float]
    applies_to: str  # "all", "specific_categories", "specific_products"
    is_active: bool
```

### FraudAlert

```python
@dataclass
class FraudAlert:
    alert_id: str
    partner_id: str
    signal_type: FraudSignalType
    severity: AlertSeverity  # INFO, WARNING, HIGH, CRITICAL, EMERGENCY
    confidence: float        # 0.0 to 1.0
    description: str
    evidence: Dict[str, Any]
    is_resolved: bool
```

### TrackingEvent

```python
@dataclass
class TrackingEvent:
    event_id: str
    partner_id: str
    event_type: str  # click, impression, conversion
    url: str
    ip_address: str
    user_agent: str
    device_type: str
    country: str
    referrer: str
    sub_id: str
    timestamp: datetime
    fraud_score: float
```

### Payout

```python
@dataclass
class Payout:
    payout_id: str
    partner_id: str
    amount: float
    method: str
    status: str  # pending, processing, completed, failed
    transaction_id: Optional[str]
    notes: str
    created_at: datetime
    processed_at: Optional[datetime]
```

## Checklists

### Partner Onboarding

- [ ] Partner application received
- [ ] Email verified
- [ ] Website/traffic source validated
- [ ] Traffic quality assessment completed
- [ ] Tax ID collected (if required)
- [ ] Commission structure agreed
- [ ] Terms of service accepted
- [ ] Creative assets provided
- [ ] Tracking links generated
- [ ] Partner approved and activated
- [ ] Welcome email sent
- [ ] Dashboard access granted

### Fraud Investigation

- [ ] Alert reviewed and triaged
- [ ] Evidence collected (IPs, timestamps, patterns)
- [ ] Partner contacted for explanation
- [ ] Traffic source verified
- [ ] Historical patterns analyzed
- [ ] Decision made (resolve / suspend / terminate)
- [ ] Action documented
- [ ] Partner notified of outcome
- [ ] Commission adjustments processed
- [ ] Rules updated if needed

### Payout Processing

- [ ] Payout threshold met
- [ ] Partner balance verified
- [ ] Payment method confirmed
- [ ] Tax withholding applied (if applicable)
- [ ] Fraud checks passed
- [ ] Payout processed
- [ ] Transaction ID recorded
- [ ] Partner notified
- [ ] Accounting updated
- [ ] Receipt generated

### Campaign Setup

- [ ] Campaign name and description defined
- [ ] Target audience identified
- [ ] Commission structure set
- [ ] Creative assets uploaded
- [ ] Tracking links generated
- [ ] Landing pages tested
- [ ] Launch date scheduled
- [ ] Partner notifications prepared
- [ ] Success metrics defined
- [ ] Budget allocated

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Partner not tracking | Status not ACTIVE | `approve_partner(partner_id)` |
| Commission shows 0 | No matching rules | Check rule applicability or use defaults |
| Fraud alert false positive | Legitimate high traffic | `resolve_alert(alert_id, notes="Verified")` |
| Payout fails | Insufficient balance | Check `total_commissions_earned - total_commissions_paid` |
| Report empty | No partners in period | Verify date range and partner status |
| Tier not upgrading | Thresholds not met | Check `tier_upgrade_eligible()` return value |
| Conversion not attributed | No touchpoints recorded | Ensure tracking links are used |
| Click count high, conversions low | Traffic quality issue | Review partner traffic sources |
| Commission calculation wrong | Rule mismatch | Verify rule conditions match sale attributes |
| Duplicate conversions | Race condition | Implement idempotency keys on order_id |
| Missing click data | Cookie blocked | Provide server-side tracking fallback |
| High fraud score on good partner | Anomalous campaign spike | Whitelist partner temporarily during promotions |

## Configuration

```python
from agent import Config

config = Config(
    default_commission_rate=0.12,      # 12% default
    cookie_duration_days=45,           # 45-day attribution window
    attribution_model="time_decay",    # Recent touchpoints get more credit
    fraud_detection_enabled=True,
    auto_approve_partners=False,
    min_payout_threshold=100.0,        # $100 minimum payout
    payout_schedule="biweekly",
    tier_upgrade_auto=True,
    gdpr_compliant=True,
    ccpa_compliant=True,
    webhook_enabled=True,
    fraud_threshold_clicks_per_hour=50,
    fraud_threshold_conversion_velocity=10,
)

agent = AffiliateMarketingAgent(config=config)
```

**Configuration Options:**
| Option | Default | Description |
|--------|---------|-------------|
| `default_commission_rate` | 0.12 | Default commission percentage |
| `cookie_duration_days` | 45 | Attribution window in days |
| `attribution_model` | time_decay | first_click, last_click, time_decay, linear |
| `fraud_detection_enabled` | True | Enable fraud detection engine |
| `auto_approve_partners` | False | Auto-approve new partners |
| `min_payout_threshold` | 100.0 | Minimum payout amount |
| `payout_schedule` | biweekly | weekly, biweekly, monthly |
| `tier_upgrade_auto` | True | Auto-upgrade partner tiers |
| `gdpr_compliant` | True | Enable GDPR compliance features |
| `ccpa_compliant` | True | Enable CCPA compliance features |

## Security Notes

- Partner PII (email, name, payment info) is encrypted at rest
- Commission calculations use precise decimal arithmetic
- Fraud detection logs are retained for 1 year
- API keys are never logged or exposed
- Webhook payloads are signed with HMAC-SHA256
- All financial transactions are audit-logged
- Partner data is isolated by tenant ID
- Sensitive operations require additional authentication

## Design Patterns

### Observer Pattern for Fraud Detection
The fraud engine observes all tracking events asynchronously, allowing real-time detection without blocking the tracking pipeline.

### Strategy Pattern for Commission Rules
Different commission types are implemented as interchangeable strategies, enabling easy addition of new commission models.

### Circuit Breaker for Payout Processing
Payout processing uses a circuit breaker pattern — if too many payment provider failures occur, payouts are queued rather than retried immediately.

### Chain of Responsibility for Attribution
Multiple attribution models are chained, allowing fallback from one model to another if insufficient touchpoint data exists.

---

*Affiliate Marketing Agent v2.0 — Part of the Awesome Grok Skills collection.*

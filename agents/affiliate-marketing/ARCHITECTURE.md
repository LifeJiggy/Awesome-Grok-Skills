# Affiliate Marketing Agent — Architecture

## Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Component Deep Dives](#component-deep-dives)
- [Data Flow](#data-flow)
- [Data Models](#data-models)
- [Design Patterns](#design-patterns)
- [Tech Stack](#tech-stack)
- [Security Architecture](#security-architecture)
- [Scalability](#scalability)
- [Deployment](#deployment)

---

## Overview

The Affiliate Marketing Agent is a comprehensive system for managing affiliate programs, tracking conversions, detecting fraud, and generating performance analytics. It follows a modular, event-driven architecture with clear separation of concerns across six core subsystems.

### Core Capabilities

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Affiliate Marketing Agent                         │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │   Partner    │  │  Commission  │  │  Tracking    │             │
│  │  Management  │  │  Calculator  │  │   Engine     │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │    Fraud     │  │ Attribution  │  │  Reporting   │             │
│  │   Detection  │  │   Engine     │  │   Engine     │             │
│  └──────────────┘  └──────────────┘  └──────────────┘             │
│  ┌──────────────┐  ┌──────────────┐                                │
│  │  Webhook     │  │  Creative    │                                │
│  │  Dispatcher  │  │  Manager     │                                │
│  └──────────────┘  └──────────────┘                                │
└─────────────────────────────────────────────────────────────────────┘
```

### Architecture Principles

1. **Event-Driven**: All significant actions emit events via webhooks
2. **Modular**: Each subsystem is independent and testable
3. **Configurable**: Behavior controlled via `Config` dataclass
4. **Audit-Complete**: Full history logging for compliance
5. **Tier-Aware**: Partner tiers influence commission calculations

---

## System Architecture

### High-Level Architecture

```
                         ┌─────────────────────┐
                         │  AffiliateMarketing │
                         │      Agent          │
                         └──────────┬──────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
   ┌─────▼──────┐          ┌───────▼───────┐          ┌───────▼──────┐
   │  Partner   │          │  Commission   │          │   Tracking   │
   │ Management │          │  Calculator   │          │    Engine    │
   │            │          │               │          │              │
   │ • Recruit  │          │ • Percentage  │          │ • Clicks     │
   │ • Approve  │          │ • Fixed       │          │ • Conversions│
   │ • Suspend  │          │ • Tiered      │          │ • Impressions│
   │ • Tier     │          │ • Recurring   │          │ • Leads      │
   │ • Search   │          │ • Hybrid      │          │ • Events     │
   └─────┬──────┘          └───────┬───────┘          └───────┬──────┘
         │                          │                          │
         └──────────────────────────┼──────────────────────────┘
                                    │
         ┌──────────────────────────┼──────────────────────────┐
         │                          │                          │
   ┌─────▼──────┐          ┌───────▼───────┐          ┌───────▼──────┐
   │   Fraud    │          │  Attribution  │          │  Reporting   │
   │ Detection  │          │    Engine     │          │   Engine     │
   │            │          │               │          │              │
   │ • Click    │          │ • Last Click  │          │ • HTML       │
   │ • Conv.    │          │ • First Click │          │ • JSON       │
   │ • Cookie   │          │ • Linear      │          │ • CSV        │
   │ • Bot      │          │ • Time Decay  │          │ • Markdown   │
   │ • Self-Ref │          │ • Position    │          │ • PDF        │
   └─────┬──────┘          └───────┬───────┘          └───────┬──────┘
         │                          │                          │
         └──────────────────────────┼──────────────────────────┘
                                    │
                           ┌────────▼────────┐
                           │   Webhook       │
                           │  Dispatcher     │
                           │                 │
                           │ • Event dispatch│
                           │ • Retry logic   │
                           │ • Event logging │
                           └─────────────────┘
```

---

## Component Deep Dives

### 1. Partner Management

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Partner Management                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Partner Lifecycle                                           │   │
│  │                                                              │   │
│  │  Recruit ──▶ Pending ──▶ Active ──▶ Suspended/Inactive      │   │
│  │    │           │           │              │                   │   │
│  │    │           │           │              ▼                   │   │
│  │    │           │           │         Terminated               │   │
│  │    │           │           │                                  │   │
│  │    │           ▼           │                                  │   │
│  │    │      Auto-Approve     │                                  │   │
│  │    │      (if enabled)     │                                  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Tier System                                                  │   │
│  │                                                              │   │
│  │  Bronze ──▶ Silver ──▶ Gold ──▶ Platinum ──▶ Diamond        │   │
│  │  1.0x       1.1x       1.25x    1.5x         2.0x           │   │
│  │                                                              │   │
│  │  Auto-upgrade based on sales + conversion thresholds         │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Features                                                    │   │
│  │  • Batch import/export (JSON)                                │   │
│  │  • Search by name, email, company, tier, tags                │   │
│  │  • Parent-child partner relationships                        │   │
│  │  • Multi-network support                                     │   │
│  │  • Compliance: GDPR, CCPA, FTC disclosure tracking           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 2. Commission Calculator

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Commission Calculator                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Input: Partner + Sale Amount + Product Category                    │
│                    │                                                │
│                    ▼                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Rule Evaluation                                             │   │
│  │                                                              │   │
│  │  1. Filter active rules matching product/category            │   │
│  │  2. Calculate commission for each applicable rule            │   │
│  │  3. Select rule producing highest commission                 │   │
│  │  4. Apply tier multiplier (Bronze=1.0, Diamond=2.0)         │   │
│  │  5. Enforce max_commission cap                               │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                    │                                                │
│                    ▼                                                │
│  Output: { commission, rule_applied, tier_multiplier }              │
│                                                                     │
│  Commission Types:                                                  │
│  ┌───────────┬──────────────────────────────────────────────────┐  │
│  │ Percentage│ sale_amount × rate × tier_multiplier             │  │
│  │ Fixed     │ fixed_amount × tier_multiplier                   │  │
│  │ Tiered    │ rate_lookup(sale_amount) × tier_multiplier       │  │
│  │ Recurring │ sale_amount × rate (for N months)                │  │
│  │ Hybrid    │ (sale_amount × rate) + fixed_bonus               │  │
│  └───────────┴──────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 3. Fraud Detection Engine

```
┌─────────────────────────────────────────────────────────────────────┐
│                      Fraud Detection Engine                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Input: TrackingEvents (clicks + conversions)                       │
│                    │                                                │
│                    ▼                                                │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Detection Strategies                                        │   │
│  │                                                              │   │
│  │  ┌────────────────────────────────────────────────────────┐ │   │
│  │  │ Click Fraud Detection                                   │ │   │
│  │  │ • IP frequency analysis (>50 clicks from one IP)       │ │   │
│  │  │ • Interval analysis (avg < 1s = bot)                   │ │   │
│  │  │ • Blacklisted IP matching                              │ │   │
│  │  └────────────────────────────────────────────────────────┘ │   │
│  │  ┌────────────────────────────────────────────────────────┐ │   │
│  │  │ Conversion Stuffing Detection                          │ │   │
│  │  │ • Rapid-fire conversions (<100ms gap)                  │ │   │
│  │  │ • Statistical anomaly (z-score > 3)                    │ │   │
│  │  └────────────────────────────────────────────────────────┘ │   │
│  │  ┌────────────────────────────────────────────────────────┐ │   │
│  │  │ Cookie Hijacking Detection                             │ │   │
│  │  │ • Session with >5 unique IPs                          │ │   │
│  │  │ • Session with >5 unique user agents                   │ │   │
│  │  └────────────────────────────────────────────────────────┘ │   │
│  │  ┌────────────────────────────────────────────────────────┐ │   │
│  │  │ Bot Traffic Detection                                  │ │   │
│  │  │ • High-frequency user agent (>100 clicks)             │ │   │
│  │  │ • Uniform click intervals                              │ │   │
│  │  └────────────────────────────────────────────────────────┘ │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                    │                                                │
│                    ▼                                                │
│  Output: FraudAlerts with severity, confidence, evidence            │
│                                                                     │
│  Alert Lifecycle:                                                   │
│  Detected ──▶ Active ──▶ Resolved (with notes + resolver)          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 4. Attribution Engine

```
┌─────────────────────────────────────────────────────────────────────┐
│                       Attribution Engine                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Models:                                                            │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                                                              │   │
│  │  Last Click:    [A]──[B]──[C] ═══▶ C gets 100%             │   │
│  │                                                              │   │
│  │  First Click:   [A]──[B]──[C] ═══▶ A gets 100%             │   │
│  │                                                              │   │
│  │  Linear:        [A]──[B]──[C] ═══▶ A:33% B:33% C:33%      │   │
│  │                                                              │   │
│  │  Time Decay:    [A]──[B]──[C] ═══▶ A:15% B:25% C:60%      │   │
│  │                                                              │   │
│  │  Position:      [A]──[B]──[C] ═══▶ A:40% B:20% C:40%      │   │
│  │                                                              │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  Flow:                                                              │
│  touchpoints ──▶ sort by timestamp ──▶ apply model ──▶ splits      │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### End-to-End Affiliate Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Complete Affiliate Flow                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  1. Partner Recruitment                                             │
│     recruit_partner() ──▶ Partner(PENDING) ──▶ approve_partner()   │
│                                                                     │
│  2. Tracking                                                        │
│     User clicks ──▶ track_click() ──▶ TrackingEvent                │
│     User converts ──▶ track_conversion() ──▶ Commission calc       │
│                                                                     │
│  3. Commission Calculation                                          │
│     sale_amount ──▶ rule evaluation ──▶ tier multiplier ──▶ result │
│                                                                     │
│  4. Fraud Detection                                                 │
│     events ──▶ analyze_clicks() ──▶ analyze_conversions()          │
│     ──▶ FraudAlerts ──▶ resolve/revoke                             │
│                                                                     │
│  5. Payout                                                          │
│     request_payout() ──▶ Payout(PENDING) ──▶ process_payout()     │
│     ──▶ Payout(COMPLETED) ──▶ update partner balance               │
│                                                                     │
│  6. Reporting                                                       │
│     partners ──▶ generate_performance_report() ──▶ HTML/JSON/CSV   │
│                                                                     │
│  7. Webhook Dispatch                                                │
│     events ──▶ dispatch() ──▶ webhook URLs                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Models

### Entity Relationship

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Entity Relationships                             │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  AffiliatePartner ──────┬──── CommissionRule[]                      │
│       │                 │                                            │
│       │                 ├──── TrackingEvent[]                        │
│       │                 │                                            │
│       │                 ├──── Creative[]                             │
│       │                 │                                            │
│       │                 ├──── Payout[]                               │
│       │                 │                                            │
│       │                 └──── FraudAlert[]                           │
│       │                                                              │
│       ├── parent_partner_id ──▶ AffiliatePartner (self-ref)         │
│       │                                                              │
│       └── network_type ──▶ NetworkType enum                          │
│                                                                     │
│  TrackingEvent ──────────┬──── order_id ──▶ (conversion only)       │
│                          │                                           │
│                          └──── commission_amount (computed)          │
│                                                                     │
│  Payout ─────────────────┬──── partner_id ──▶ AffiliatePartner      │
│                          │                                           │
│                          └──── transaction_id (external ref)        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Enumerations

| Enum | Values | Purpose |
|------|--------|---------|
| PartnerTier | BRONZE, SILVER, GOLD, PLATINUM, DIAMOND | Commission multiplier + perks |
| PartnerStatus | PENDING, ACTIVE, SUSPENDED, TERMINATED, INACTIVE | Account lifecycle |
| CommissionType | PERCENTAGE, FIXED, TIERED, RECURRING, HYBRID | Calculation model |
| FraudSignalType | 10 types | Alert classification |
| AttributionModel | LAST_CLICK, FIRST_CLICK, LINEAR, TIME_DECAY, POSITION_BASED | Conversion credit |

---

## Design Patterns

### 1. Strategy Pattern — Commission Calculation

```python
# Each CommissionType implements calculate() differently
class CommissionRule:
    def calculate(self, sale_amount, product_category):
        if self.commission_type == CommissionType.PERCENTAGE:
            return sale_amount * self.percentage_rate
        elif self.commission_type == CommissionType.FIXED:
            return self.fixed_amount
        elif self.commission_type == CommissionType.TIERED:
            return self._calculate_tiered(sale_amount)
        # ...
```

### 2. Observer Pattern — Webhook Dispatch

```python
# Events dispatched to registered webhooks
class WebhookDispatcher:
    def dispatch(self, event_type, payload):
        for webhook in self._webhooks:
            if event_type in webhook.events:
                # Send HTTP POST to webhook.url
                ...
```

### 3. Chain of Responsibility — Fraud Detection

```python
# Multiple detection strategies chained together
class FraudDetectionEngine:
    def analyze_clicks(self, clicks):
        alerts = []
        alerts.extend(self._detect_ip_fraud(clicks))
        alerts.extend(self._detect_bot_traffic(clicks))
        alerts.extend(self._detect_cookie_hijacking(clicks))
        return alerts
```

### 4. Dataclass Pattern — All Models

```python
# Immutable-ish data containers with serialization
@dataclass
class AffiliatePartner:
    def to_dict(self) -> Dict[str, Any]: ...
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10+ | Core runtime |
| Data Models | `dataclasses` | Typed data containers |
| Enums | `enum.Enum` | Type-safe constants |
| Serialization | `json`, `csv` | Data export |
| Hashing | `hashlib` | ID generation |
| Secrets | `secrets` | Secure token generation |
| Statistics | `statistics` | Analytics calculations |
| Logging | `logging` | Observability |
| Async | `asyncio` | Future webhook integration |

### Optional Dependencies

| Package | Purpose |
|---------|---------|
| `requests` | HTTP webhook delivery |
| `aiohttp` | Async HTTP client |
| `prometheus_client` | Metrics export |
| `redis` | Event caching |
| `sqlalchemy` | Persistent storage |

---

## Security Architecture

### Data Protection

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Security Layers                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Layer 1: Input Validation                                          │
│  • Email format validation                                          │
│  • Amount bounds checking                                           │
│  • Partner ID format verification                                   │
│                                                                     │
│  Layer 2: Access Control                                            │
│  • Partner status checks before tracking                            │
│  • Payout balance verification                                      │
│  • Commission rule applicability                                    │
│                                                                     │
│  Layer 3: Fraud Prevention                                          │
│  • IP blacklisting                                                  │
│  • Bot detection                                                     │
│  • Conversion stuffing detection                                     │
│  • Self-referral blocking                                           │
│                                                                     │
│  Layer 4: Compliance                                                │
│  • GDPR: Partner consent tracking                                   │
│  • CCPA: Data deletion support                                      │
│  • FTC: Disclosure requirement enforcement                          │
│                                                                     │
│  Layer 5: Audit                                                     │
│  • Full action history logging                                      │
│  • Webhook event trail                                              │
│  • Fraud alert resolution tracking                                  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Compliance Configuration

```yaml
compliance:
  gdpr_enabled: true
  ccpa_enabled: true
  ftc_disclosure_required: true
  data_retention_days: 365
  consent_tracking: true
  right_to_deletion: true
```

---

## Scalability

### Performance Characteristics

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Partner lookup | O(n) | Linear scan; optimize with dict for >10K partners |
| Commission calc | O(r) | r = rules per partner |
| Fraud analysis | O(e) | e = events analyzed |
| Attribution | O(t) | t = touchpoints per order |
| Report generation | O(p) | p = partners in report |

### Scaling Strategies

1. **In-Memory (Current)**: Suitable for <10K partners, <1M events
2. **Database-Backed**: Replace lists with SQLAlchemy models
3. **Distributed**: Shard by partner_id for >100K partners
4. **Event Streaming**: Replace webhook dispatcher with Kafka/SQS
5. **Caching**: Redis for frequent partner lookups and commission calculations

### Concurrent Event Processing

```
                    ┌─────────────────┐
                    │   Event Stream   │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
        ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
        │ Worker 1  │ │ Worker 2  │ │ Worker N  │
        │           │ │           │ │           │
        │ • Fraud   │ │ • Fraud   │ │ • Fraud   │
        │ • Commiss.│ │ • Commiss.│ │ • Commiss.│
        │ • Webhook │ │ • Webhook │ │ • Webhook │
        └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │  Shared State   │
                    │  (DB + Cache)   │
                    └─────────────────┘
```

---

## Deployment

### Docker Deployment

```yaml
version: '3.8'
services:
  affiliate-agent:
    build: .
    ports:
      - "8000:8000"
    environment:
      - AFFILIATE_API_KEY=${AFFILIATE_API_KEY}
      - WEBHOOK_SECRET=${WEBHOOK_SECRET}
      - DATABASE_URL=${DATABASE_URL}
    volumes:
      - ./config:/app/config
      - ./reports:/app/reports
```

### Environment Variables

```bash
# Core
AFFILIATE_API_KEY=your-api-key
WEBHOOK_SECRET=your-webhook-secret
TRACKING_DOMAIN=track.example.com

# Compliance
GDPR_ENABLED=true
CCPA_ENABLED=true
FTC_DISCLOSURE_REQUIRED=true

# Storage
DATABASE_URL=sqlite:///affiliate.db
REDIS_URL=redis://localhost:6379

# Notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
EMAIL_SMTP_HOST=smtp.example.com
```

### Health Checks

```python
def health_check() -> Dict[str, Any]:
    return {
        "status": "healthy",
        "version": "2.0.0",
        "partners": agent.get_status()["partners"],
        "uptime": get_uptime(),
    }
```

---

## Appendix: Configuration Reference

| Config Key | Type | Default | Description |
|-----------|------|---------|-------------|
| `default_commission_rate` | float | 0.10 | Default commission percentage |
| `cookie_duration_days` | int | 30 | Attribution window |
| `attribution_model` | str | "last_click" | Conversion credit model |
| `fraud_detection_enabled` | bool | True | Enable fraud engine |
| `fraud_confidence_threshold` | float | 0.8 | Min confidence for alerts |
| `auto_approve_partners` | bool | False | Skip manual approval |
| `min_payout_threshold` | float | 50.0 | Minimum payout amount |
| `payout_schedule` | str | "monthly" | Payout frequency |
| `max_partners` | int | 10000 | Partner capacity limit |
| `retention_days` | int | 365 | Event retention period |
| `tier_upgrade_auto` | bool | True | Auto-upgrade eligible partners |
| `webhook_enabled` | bool | False | Enable webhook dispatch |

---

*Affiliate Marketing Agent Architecture v2.0 — Part of the Awesome Grok Skills collection.*

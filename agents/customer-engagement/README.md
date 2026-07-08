# Customer Engagement Agent

A comprehensive omnichannel customer engagement platform with segmentation, campaign management, journey orchestration, engagement scoring, A/B testing, attribution tracking, personalization, content management, webhook integration, feedback collection, channel analytics, trigger automation, and audience building.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Data Flow](#data-flow)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Customer Management](#customer-management)
  - [Segmentation](#segmentation)
  - [Messaging](#messaging)
  - [Campaigns](#campaigns)
  - [A/B Testing](#ab-testing)
  - [Customer Journeys](#customer-journeys)
  - [Engagement Scoring](#engagement-scoring)
  - [Attribution](#attribution)
  - [Personalization](#personalization)
  - [Content Management](#content-management)
  - [Webhook Integration](#webhook-integration)
  - [Feedback Collection](#feedback-collection)
  - [Channel Analytics](#channel-analytics)
  - [Trigger Automation](#trigger-automation)
  - [Audience Building](#audience-building)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Security](#security)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Customer Engagement Agent provides a complete platform for managing customer communications across multiple channels. It enables businesses to create personalized, data-driven engagement strategies that build meaningful customer relationships.

The agent handles everything from basic transactional messages to complex multi-step customer journeys with branching logic, A/B testing, attribution tracking, automated triggers, and real-time feedback collection.

Built with Python 3.10+ using only the standard library, the agent requires no external dependencies and can be deployed anywhere Python runs.

## Features

### Core Capabilities
- **Omnichannel Messaging**: Email, SMS, push notifications, in-app, social media, webhooks, direct mail, chat
- **Dynamic Segmentation**: Behavioral, demographic, transactional, lifecycle, and custom segments
- **Campaign Management**: Create, schedule, execute, pause, and analyze multi-channel campaigns
- **Customer Journeys**: Multi-step orchestration with delays, branching logic, and conditional execution
- **Engagement Scoring**: Behavioral scoring with time-based decay and trend analysis
- **A/B Testing**: Statistical testing for messaging optimization with confidence calculations
- **Attribution Tracking**: Multi-touch attribution across channels with six model options
- **Personalization**: Content customization, recommendations, and send time optimization

### Extended Capabilities
- **Content Management**: Reusable content blocks with variable interpolation and versioning
- **Webhook Integration**: Outbound webhooks for external system integration with delivery tracking
- **Feedback Collection**: CSAT, NPS, CES, surveys, reviews, and ratings with sentiment analysis
- **Channel Analytics**: Cross-channel performance comparison and efficiency metrics
- **Trigger Automation**: Event-driven rules with conditions, actions, and cooldown periods
- **Audience Building**: Composite audiences from segment combinations with set operations

### Technical Features
- **Rate Limiting**: Per-customer and per-channel frequency controls
- **Template System**: Reusable message templates with variable substitution
- **Thread Safety**: Independent locks per manager for concurrent access
- **Async Support**: Non-blocking operations via AsyncCustomerEngagementAgent
- **No Dependencies**: Pure Python standard library (3.10+)

## Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                      CustomerEngagementAgent                               │
│                                                                            │
│  ┌────────────┐  ┌──────────────┐  ┌────────────────────────────────────┐ │
│  │ Customer   │  │ Segment Mgr  │  │ Message Orchestrator               │ │
│  │ Manager    │  │              │  │                                    │ │
│  ├────────────┤  ├──────────────┤  ├────────────────────────────────────┤ │
│  │ Campaign   │  │ Journey Mgr  │  │ Engagement Scorer                  │ │
│  │ Manager    │  │              │  │                                    │ │
│  ├────────────┤  ├──────────────┤  ├────────────────────────────────────┤ │
│  │ Attribution│  │ Personalize  │  │ Channel Analytics                  │ │
│  │ Manager    │  │ Engine       │  │                                    │ │
│  ├────────────┤  ├──────────────┤  ├────────────────────────────────────┤ │
│  │ Content    │  │ Webhook      │  │ Trigger Engine                     │ │
│  │ Manager    │  │ Manager      │  │                                    │ │
│  ├────────────┤  ├──────────────┤  ├────────────────────────────────────┤ │
│  │ Feedback   │  │ Audience     │  │ Channel Layer                      │ │
│  │ Collector  │  │ Builder      │  │ Email│SMS│Push│In-App│Social│Chat  │ │
│  └────────────┘  └──────────────┘  └────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

The architecture follows a manager-based pattern where each subsystem is an independent, thread-safe component. The `CustomerEngagementAgent` class orchestrates all managers and provides a unified API.

## Data Flow

### Customer Lifecycle Flow
```
Create Profile → Track Events → Score Engagement → Segment Customer
     ↓                                                    ↓
  Record Data                                    Personalize Content
     ↓                                                    ↓
  Update Status ←──── Attribute Conversion ←──── Send via Channel
```

### Campaign Execution Flow
```
Create Campaign → Select Segments → Build Audience → Apply Templates
                                                            ↓
Analyze Performance ← Track Results ← Send via Channels ←┘
```

### Trigger Automation Flow
```
Event Arrives → Trigger Engine → Check Rules → Match Conditions?
                                                       ↓ Yes
Execute Actions ← Check Cooldown ← Match Found ←──┘
     ↓
Send Message / Update Status → Log Result → Update Stats
```

## Quick Start

```python
from agents.customer_engagement.agent import (
    CustomerEngagementAgent, Config, ChannelType, MessageType,
    CustomerStatus, SegmentType
)

# Initialize agent
agent = CustomerEngagementAgent(Config())
agent.initialize()

# Create customers
agent.create_customer("cust_001", email="john@example.com", name="John Doe")
agent.create_customer("cust_002", email="jane@example.com", name="Jane Smith")

# Record events
agent.record_event("cust_001", "signup", ChannelType.IN_APP)
agent.record_event("cust_001", "purchase", ChannelType.EMAIL, {"value": 99.99})

# Create segment
agent.create_segment(
    "seg_active", "Active Customers", SegmentType.BEHAVIORAL,
    [{"field": "status", "operator": "eq", "value": CustomerStatus.ACTIVE}]
)

# Send message
agent.send_message(
    "cust_001", ChannelType.EMAIL, MessageType.PROMOTIONAL,
    subject="Special Offer", body="Hi {name}, here's 20% off!"
)

# Calculate engagement score
score = agent.calculate_engagement_score("cust_001")
print(f"Engagement: {score['score']:.1f}")

# Get full report
report = agent.get_full_report()

# Shutdown
agent.shutdown()
```

## Installation

### From Source
```bash
git clone https://github.com/your-org/customer-engagement-agent.git
cd customer-engagement-agent
pip install -r requirements.txt
```

### Dependencies
```
Python 3.10+
No external dependencies required (stdlib only)
```

### Verification
```python
from agents.customer_engagement.agent import CustomerEngagementAgent
agent = CustomerEngagementAgent()
status = agent.initialize()
print(status)  # {'status': 'initialized', ...}
agent.shutdown()
```

## Usage

### Customer Management

Full CRUD operations on customer profiles with lifecycle tracking and behavioral event history.

```python
# Create customer with full profile
agent.create_customer(
    customer_id="cust_001",
    email="john@example.com",
    phone="+1234567890",
    name="John Doe",
    channel_preferences=[ChannelType.EMAIL, ChannelType.PUSH],
    tags=["premium", "early_adopter"],
    acquisition_channel=ChannelType.EMAIL
)

# Update customer fields
agent.update_customer("cust_001", status=CustomerStatus.ACTIVE, lifetime_value=500.0)

# Record behavioral events with properties
agent.record_event("cust_001", "page_view", ChannelType.IN_APP, {"page": "pricing"})
agent.record_event("cust_001", "email_open", ChannelType.EMAIL)
agent.record_event("cust_001", "purchase", ChannelType.EMAIL, {"value": 99.99})
agent.record_event("cust_001", "cart_abandon", ChannelType.IN_APP)

# Tag management
agent._customer_manager.add_tag("cust_001", "premium")
agent._customer_manager.add_tag("cust_001", "holiday_shopper")
agent._customer_manager.get_customers_by_tag("premium")

# Opt-out handling
agent._customer_manager.opt_out_channel("cust_001", ChannelType.SMS)

# Bulk operations
agent._customer_manager.bulk_create_customers([
    {"customer_id": "c1", "email": "alice@test.com", "name": "Alice"},
    {"customer_id": "c2", "email": "bob@test.com", "name": "Bob"},
])

# Search customers
results = agent._customer_manager.search_customers("john")

# Get active customers
active = agent._customer_manager.get_active_customers(days=30)

# Get customer profile
profile = agent.get_customer("cust_001")
print(profile)
# {'customer_id': 'cust_001', 'name': 'John Doe', 'email': 'john@example.com',
#  'status': 'ACTIVE', 'engagement_score': 15.0, ...}
```

### Segmentation

Build behavioral, demographic, transactional, and lifecycle segments with flexible rule evaluation.

```python
# Create behavioral segment
agent.create_segment(
    "seg_high_value", "High Value Customers", SegmentType.TRANSACTIONAL,
    [{"field": "total_purchases", "operator": "gte", "value": 5}]
)

# Create lifecycle segment
agent.create_segment(
    "seg_at_risk", "At Risk", SegmentType.LIFECYCLE,
    [{"field": "status", "operator": "eq", "value": CustomerStatus.AT_RISK}]
)

# Create engagement segment
agent.create_segment(
    "seg_engaged", "Highly Engaged", SegmentType.ENGAGEMENT,
    [{"field": "engagement_score", "operator": "gte", "value": 80}]
)

# Check segment size
size = agent.get_segment_size("seg_high_value")
print(f"High value customers: {size}")

# Combine segments
combined = agent._segment_manager.combine_segments(
    ["seg_high_value", "seg_engaged"], operator="union"
)
intersection = agent._segment_manager.combine_segments(
    ["seg_high_value", "seg_engaged"], operator="intersection"
)

# Analyze overlap
overlap = agent._segment_manager.get_segment_overlap("seg_a", "seg_b")
print(f"Overlap: {overlap['overlap_count']} ({overlap['overlap_pct_a']:.1%})")

# Clone segment
agent._segment_manager.clone_segment("seg_high_value", "seg_v2", "High Value V2")

# Refresh all segments
agent._segment_manager.refresh_all_segments()
```

**Segment Operators:**

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equals | `{"field": "status", "operator": "eq", "value": "ACTIVE"}` |
| `neq` | Not equals | `{"field": "status", "operator": "neq", "value": "CHURNED"}` |
| `gt` | Greater than | `{"field": "total_purchases", "operator": "gt", "value": 5}` |
| `lt` | Less than | `{"field": "lifetime_value", "operator": "lt", "value": 100}` |
| `gte` | Greater or equal | `{"field": "engagement_score", "operator": "gte", "value": 80}` |
| `lte` | Less or equal | `{"field": "engagement_score", "operator": "lte", "value": 20}` |
| `in` | Value in list | `{"field": "status", "operator": "in", "value": ["ACTIVE", "VIP"]}` |
| `contains` | Substring match | `{"field": "email", "operator": "contains", "value": "@co.com"}` |

### Messaging

Send personalized messages across all channels with rate limiting and template support.

```python
# Send single message
agent.send_message(
    "cust_001", ChannelType.EMAIL, MessageType.PROMOTIONAL,
    subject="Special Offer for {name}",
    body="You've been selected for an exclusive 20% discount!"
)

# Send SMS
agent.send_message(
    "cust_001", ChannelType.SMS, MessageType.TRANSACTIONAL,
    body="Your order #12345 has shipped. Track: {tracking_url}"
)

# Send push notification
agent.send_message(
    "cust_001", ChannelType.PUSH_NOTIFICATION, MessageType.ALERT,
    subject="Price Drop Alert",
    body="Items in your wishlist are now on sale!"
)

# Bulk send with rate limiting
result = agent._message_orchestrator.send_bulk(
    ["cust_001", "cust_002", "cust_003"],
    ChannelType.EMAIL, MessageType.NEWSLETTER,
    "Monthly Update", "Here's what's new this month..."
)
# Returns: {"sent": 3, "failed": 0, "rate_limited": 0, "total": 3}

# Track daily volume
volume = agent._message_orchestrator.get_daily_volume(days=7)

# Get message history
history = agent._message_orchestrator.get_message_history(
    customer_id="cust_001", channel=ChannelType.EMAIL, limit=50
)

# Update delivery status
agent._message_orchestrator.update_message_status("msg-uuid", "delivered")
```

**Message Lifecycle:**
```
PENDING → SENT → DELIVERED → OPENED → CLICKED → CONVERTED
```

### Campaigns

Full campaign lifecycle from creation through execution and performance analysis.

```python
# Create multi-channel campaign
agent.create_campaign(
    campaign_id="camp_summer",
    name="Summer Sale 2024",
    campaign_type=MessageType.PROMOTIONAL,
    channels=[ChannelType.EMAIL, ChannelType.PUSH, ChannelType.SMS],
    segment_ids=["seg_high_value", "seg_engaged"],
    subject="Summer Sale - Up to 50% Off!",
    body="Don't miss our biggest sale of the year...",
    budget=5000.00
)

# Start campaign
agent.start_campaign("camp_summer")

# Track performance
perf = agent.get_campaign_performance("camp_summer")
print(f"Delivery: {perf['delivery_rate']:.1%}")
print(f"Open Rate: {perf['open_rate']:.1%}")
print(f"Click Rate: {perf['click_rate']:.1%}")
print(f"Conversion: {perf['conversion_rate']:.1%}")

# Pause campaign
agent._campaign_manager.pause_campaign("camp_summer")

# Complete campaign
agent._campaign_manager.complete_campaign("camp_summer")

# List campaigns by status
running = agent._campaign_manager.get_all_campaigns(status=CampaignStatus.RUNNING)
completed = agent._campaign_manager.get_all_campaigns(status=CampaignStatus.COMPLETED)
```

**Campaign Lifecycle:**
```
DRAFT → SCHEDULED → RUNNING → COMPLETED
                    ↓
                 PAUSED
```

### A/B Testing

Statistical testing for messaging optimization with confidence calculations.

```python
# Create A/B test
test = agent._campaign_manager.create_ab_test(
    "test_subject", "Subject Line Test", "camp_summer",
    variants=[
        {"name": "control", "subject": "Summer Sale - Up to 50% Off!"},
        {"name": "variant_a", "subject": "Hot Summer Deals Inside"},
        {"name": "variant_b", "subject": "Your Exclusive Summer Offer"},
    ],
    primary_metric="open_rate"
)

# Start test
agent._campaign_manager.start_ab_test("test_subject")

# Record results
agent._campaign_manager.record_ab_result("test_subject", "control", 0.22)
agent._campaign_manager.record_ab_result("test_subject", "variant_a", 0.28)

# Analyze
analysis = agent._campaign_manager.analyze_ab_test("test_subject")
print(f"Winner: {analysis['winner']}")
print(f"Confidence: {analysis['confidence']:.0%}")

# List all tests
tests = agent._campaign_manager.get_all_ab_tests()
```

### Customer Journeys

Multi-step orchestration with delays, branching logic, and conditional execution.

```python
from agents.customer_engagement.agent import JourneyStep

# Define journey steps
steps = [
    JourneyStep("welcome", "Welcome Email", ChannelType.EMAIL,
                MessageType.ONBOARDING, delay_hours=0),
    JourneyStep("followup", "Follow-up", ChannelType.EMAIL,
                MessageType.LIFECYCLE, delay_hours=48,
                next_step_on_action="offer",
                next_step_on_inaction="nudge"),
    JourneyStep("nudge", "Final Nudge", ChannelType.SMS,
                MessageType.REENGAGEMENT, delay_hours=168),
    JourneyStep("offer", "Special Offer", ChannelType.EMAIL,
                MessageType.PROMOTIONAL, delay_hours=72),
]

# Create and activate journey
agent.create_journey("jour_welcome", "Welcome Series", "signup", steps)
agent.activate_journey("jour_welcome")

# Enroll customers
agent.enroll_in_journey("jour_welcome", "cust_001")

# Check stats
stats = agent._journey_manager.get_enrollment_stats("jour_welcome")
print(f"Active: {stats['active']}, Completed: {stats['completed']}")
print(f"Completion rate: {stats['completion_rate']:.1%}")

# Track progress
progress = agent._journey_manager.get_customer_journey_progress("cust_001")
```

**Journey Execution:**
```
Trigger Event → Enroll Customer → Execute Step 1 → Delay → Check Conditions
                                                                       ↓
Complete ← Continue ← Next Step or Branch ←──────────────────────────┘
```

### Engagement Scoring

Behavioral scoring with time-based decay, trend analysis, and percentile benchmarks.

```python
# Calculate score
score = agent.calculate_engagement_score("cust_001")
print(f"Score: {score['score']:.1f}, Trend: {score['trend']}")

# Get top engaged
top = agent.get_top_engaged_customers(20)
for s in top:
    print(f"{s['customer_id']}: {s['score']:.1f} ({s['trend']})")

# Score distribution
dist = agent.get_engagement_distribution()
# {"0-20": 150, "20-40": 300, "40-60": 500, "60-80": 200, "80-100": 50}

# Percentiles
percentiles = agent._engagement_scorer.get_score_percentiles()

# Customize rules
agent._engagement_scorer.set_scoring_rule("premium_purchase", 30.0)
```

**Scoring Formula:**
```
adjusted_weight = weight × decay_rate^days_ago
total_score = sum(all adjusted weights)
normalized = min(100.0, total_score)
```

**Default Scoring Rules:**

| Event | Points |
|-------|--------|
| email_open | 2.0 |
| email_click | 5.0 |
| sms_click | 7.0 |
| purchase | 20.0 |
| app_open | 1.0 |
| page_view | 0.5 |
| signup | 10.0 |
| referral | 15.0 |
| review | 8.0 |
| social_share | 3.0 |

### Attribution

Multi-touch attribution with six models and cross-channel summaries.

```python
# Set model
agent._attribution_manager.set_model(AttributionModel.TIME_DECAY)

# Record touchpoints
agent._attribution_manager.record_touchpoint(
    "cust_001", "camp_email", ChannelType.EMAIL, datetime.now(), 99.99
)

# Get attribution
attribution = agent.get_attribution("cust_001")
print(f"Model: {attribution['model']}")
print(f"Campaign credits: {attribution['campaign_attributions']}")
print(f"Channel credits: {attribution['channel_attributions']}")

# Channel summary
summary = agent._attribution_manager.get_channel_attribution_summary()
```

**Attribution Models:**
```
Touchpoints: T1(A) → T2(B) → T3(C) → Conversion

FIRST_TOUCH:  A=100%, B=0%, C=0%
LAST_TOUCH:   A=0%, B=0%, C=100%
LINEAR:       A=33%, B=33%, C=33%
TIME_DECAY:   A=17%, B=33%, C=50%
POSITION:     A=40%, B=20%, C=40%
```

### Personalization

Content customization, recommendations, and send time optimization.

```python
# Personalize content
content = agent.personalize_content("cust_001", {"headline": "Special Offer"})
# {"headline": "Special Offer", "greeting": "Hi John", "tier": "Premium"}

# Get recommendations
recs = agent.get_recommendations("cust_001")
# [{"type": "cart_reminder", "reason": "Incomplete purchase"}]

# Optimal send time
time = agent.get_send_time("cust_001")
# {"hour": 10, "day": "Tuesday", "confidence": "medium"}

# Check personalization level
level = agent._personalization_engine.get_personalization_level("cust_001")
```

### Content Management

Reusable content blocks with variable interpolation and versioning.

```python
# Create content blocks
agent._content_manager.create_block(
    "cb_001", "Welcome Header",
    "Hello {{name}}, welcome to {{product}}!",
    format=ContentFormat.HTML, channel=ChannelType.EMAIL
)

# Render with variables
rendered = agent._content_manager.render_block(
    "cb_001", {"name": "John", "product": "Acme"}
)
# "Hello John, welcome to Acme!"

# Update (auto-increments version)
agent._content_manager.update_block("cb_001", "Hi {{name}}!")

# Clone for testing
agent._content_manager.clone_block("cb_001", "cb_002", "Welcome V2")

# Get by channel
email_blocks = agent._content_manager.get_blocks_by_channel(ChannelType.EMAIL)
```

### Webhook Integration

Outbound webhooks for real-time event delivery.

```python
# Register webhooks
agent._webhook_manager.register_webhook(
    "wh_001", "https://api.example.com/events",
    events=["purchase", "signup"], secret="webhook_secret"
)

# Trigger webhooks
results = agent._webhook_manager.trigger_webhooks("purchase", {"order_id": "123"})

# Check delivery stats
stats = agent._webhook_manager.get_webhook_stats("wh_001")
# {"total_triggers": 42, "delivered": 40, "delivery_rate": 0.95}

# View delivery log
log = agent._webhook_manager.get_delivery_log("wh_001", limit=10)

# Pause/resume
agent._webhook_manager.update_webhook_status("wh_001", WebhookStatus.PAUSED)
agent._webhook_manager.update_webhook_status("wh_001", WebhookStatus.ACTIVE)
```

### Feedback Collection

Gather and analyze customer feedback with sentiment analysis.

```python
# Collect NPS
agent._feedback_collector.collect_feedback(
    "cust_001", FeedbackType.NPS, score=9.0,
    comment="Great product!", channel=ChannelType.EMAIL
)

# Get NPS score
nps = agent._feedback_collector.get_nps_score()
# {"nps": 72.0, "promoters": 80, "passives": 15, "detractors": 5}

# Average by type
avg = agent._feedback_collector.get_average_score(FeedbackType.CSAT)

# Sentiment distribution
sentiment = agent._feedback_collector.get_sentiment_distribution()
# {"positive": 150, "neutral": 50, "negative": 20}

# Full summary
summary = agent._feedback_collector.get_feedback_summary()
```

### Channel Analytics

Cross-channel performance comparison and efficiency metrics.

```python
# Compare all channels
comparison = agent._channel_analytics.get_comparison()
# Returns sorted by click_rate

# Per-channel efficiency
efficiency = agent._channel_analytics.get_channel_efficiency(ChannelType.EMAIL)

# Calculate all performance
all_perf = agent._channel_analytics.calculate_all_performance()
```

### Trigger Automation

Event-driven rules with conditions, actions, and cooldowns.

```python
# Register trigger
agent._trigger_engine.register_rule(
    "tr_001", "High Value Purchase", TriggerType.THRESHOLD,
    conditions=[{"type": "event_type", "value": "purchase"}],
    actions=[
        {"type": "send_message", "channel": "EMAIL", "message_type": "ALERT"}
    ],
    cooldown_minutes=60
)

# Events automatically processed
agent.record_event("cust_001", "purchase", ChannelType.EMAIL, {"value": 199.99})

# Check fire stats
stats = agent._trigger_engine.get_fire_stats()

# Disable/enable
agent._trigger_engine.disable_rule("tr_001")
agent._trigger_engine.enable_rule("tr_001")
```

### Audience Building

Composite audiences from segment combinations.

```python
# Build audience
agent._audience_builder.build_audience(
    "aud_001", "High Value Active",
    ["seg_high_value", "seg_active"],
    operator="intersection"
)

# Get audience
audience = agent._audience_builder.get_audience("aud_001")
print(f"Size: {audience['size']}")

# Exclude audiences
remaining = agent._audience_builder.exclude_audience("aud_001", "aud_unsubscribed")

# Refresh
agent._audience_builder.refresh_audience("aud_001")
```

## API Reference

### CustomerEngagementAgent

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `create_customer()` | id, email, phone, name, **kwargs | Dict | Create customer profile |
| `get_customer()` | id | Dict | Get customer details |
| `update_customer()` | id, **updates | Dict | Update customer fields |
| `record_event()` | id, type, channel, props | Dict | Record behavioral event |
| `create_segment()` | id, name, type, rules | Dict | Create customer segment |
| `get_segment_size()` | id | int | Get segment member count |
| `send_message()` | id, channel, type, subject, body | Dict | Send message |
| `create_campaign()` | id, name, type, channels, segments | Dict | Create campaign |
| `start_campaign()` | id | Dict | Launch campaign |
| `get_campaign_performance()` | id | Dict | Get campaign metrics |
| `create_journey()` | id, name, trigger, steps | Dict | Create customer journey |
| `enroll_in_journey()` | journey_id, customer_id | Dict | Enroll customer |
| `calculate_engagement_score()` | id | Dict | Calculate engagement score |
| `get_top_engaged_customers()` | limit | List | Get top engaged customers |
| `get_attribution()` | id | Dict | Get attribution data |
| `personalize_content()` | id, content | Dict | Personalize content |
| `get_recommendations()` | id | List | Get recommendations |
| `get_send_time()` | id | Dict | Get optimal send time |
| `get_channel_stats()` | channel | Dict | Get channel performance |
| `get_engagement_distribution()` | - | Dict | Score distribution |
| `get_status()` | - | Dict | Agent status |
| `get_full_report()` | - | Dict | Comprehensive report |

### Sub-Manager APIs

| Manager | Method | Description |
|---------|--------|-------------|
| `ContentManager` | `create_block()` | Create reusable content block |
| | `render_block()` | Render block with variables |
| | `update_block()` | Update content, increment version |
| | `clone_block()` | Clone block with new ID |
| | `get_blocks_by_channel()` | List blocks filtered by channel |
| `WebhookManager` | `register_webhook()` | Register outbound webhook |
| | `trigger_webhooks()` | Fire webhooks for event |
| | `get_webhook_stats()` | Get delivery statistics |
| | `get_delivery_log()` | View delivery history |
| | `list_webhooks()` | List all registered webhooks |
| | `delete_webhook()` | Remove webhook |
| `FeedbackCollector` | `collect_feedback()` | Record customer feedback |
| | `get_nps_score()` | Calculate NPS score |
| | `get_average_score()` | Average by feedback type |
| | `get_sentiment_distribution()` | Sentiment breakdown |
| | `get_feedback_by_customer()` | Get feedback per customer |
| | `get_feedback_summary()` | Full feedback summary |
| `ChannelAnalytics` | `get_comparison()` | Cross-channel comparison |
| | `get_channel_efficiency()` | Per-channel efficiency |
| | `calculate_all_performance()` | Full performance report |
| | `get_performance()` | Get single channel performance |
| `TriggerEngine` | `register_rule()` | Register trigger rule |
| | `process_event()` | Evaluate event against rules |
| | `get_fire_stats()` | Rule fire counts |
| | `disable_rule()` / `enable_rule()` | Toggle rules |
| | `list_rules()` | List all trigger rules |
| `AudienceBuilder` | `build_audience()` | Combine segments |
| | `exclude_audience()` | Set difference |
| | `intersect_audiences()` | Set intersection |
| | `get_audience()` | Get audience details |
| | `refresh_audience()` | Re-evaluate from segments |
| | `list_audiences()` | List all audiences |

## Configuration

```yaml
agent:
  default_channel: email
  max_daily_sends: 10000
  enable_ab_testing: true
  enable_journeys: true
  scoring_decay_rate: 0.95
  attribution_model: last_touch

channels:
  email:
    daily_limit: 10
    cooldown_hours: 24
  sms:
    daily_limit: 3
    cooldown_hours: 48
  push:
    daily_limit: 5
    cooldown_hours: 6

triggers:
  default_cooldown_minutes: 60
  max_concurrent_triggers: 10

webhooks:
  retry_count: 3
  timeout_seconds: 30
```

### Channel Limits

| Channel | Daily Limit | Cooldown |
|---------|------------|----------|
| Email | 10 | 24 hours |
| SMS | 3 | 48 hours |
| Push | 5 | 6 hours |
| In-App | 20 | 1 hour |
| Social | 2-5 | 4-12 hours |
| Webhook | 100 | None |
| Direct Mail | 1 | 7 days |

## Security

### Data Privacy
- Customer PII is stored in memory only (no persistence without explicit export)
- Opt-out preferences are respected across all channels
- GDPR/CCPA compliance hooks via `delete_customer()` and opt-out methods

### Rate Limiting
- Per-customer daily limits prevent spam
- Cooldown periods between messages on the same channel
- Global daily send caps configurable via Config

### Access Control
- Campaign creation requires explicit authorization
- Customer data access is logged
- Template modifications are versioned
- Webhook secrets enable HMAC verification

### Webhook Security
- Secret-based HMAC signature verification
- Configurable retry policies (default: 3 retries)
- Timeout protection (default: 30 seconds)
- Failure count monitoring with auto-disable capability

## Best Practices

### Segmentation
1. Create focused segments with 3-5 rules
2. Use dynamic segments for real-time targeting
3. Refresh segments daily for accuracy
4. Monitor segment size trends
5. Use overlap analysis to avoid redundancy

### Campaigns
1. Always A/B test subject lines
2. Send during optimal hours (10am-2pm)
3. Keep content mobile-friendly
4. Include clear CTAs
5. Respect frequency limits
6. Use channel comparison for budget allocation

### Journeys
1. Start with 2-3 step journeys
2. Add appropriate delays (24-72 hours)
3. Branch on engagement actions
4. Set timeouts for inaction
5. Measure completion rates

### Scoring
1. Weight purchases highest (20 points)
2. Apply time decay for recency
3. Monitor trend direction
4. Use scores for segmentation
5. Re-score after significant events
6. Use percentiles for benchmarking

### Triggers
1. Set appropriate cooldown periods
2. Match conditions precisely
3. Monitor fire counts for tuning
4. Test with sample events before activation
5. Use multiple action types for complex workflows

### Webhooks
1. Verify endpoint accessibility
2. Configure appropriate retry counts
3. Set reasonable timeouts (10-30s)
4. Monitor delivery logs for failures
5. Use HMAC secrets for verification

### Feedback
1. Collect NPS quarterly for trend tracking
2. Use CSAT after key interactions
3. Monitor sentiment distribution
4. Close the loop on negative feedback
5. Use feedback scores for segmentation

## Troubleshooting

**Low open rates**
- Test subject lines with A/B testing
- Check sender reputation and deliverability
- Verify send times for audience timezone
- Review content relevance for segment
- Check if emails land in spam folders

**High unsubscribes**
- Reduce message frequency
- Improve content personalization
- Review segment targeting accuracy
- Check opt-out mechanism accessibility
- Compare unsubscribe rates across segments

**Journey drop-off**
- Analyze which step causes attrition
- Adjust delays (too short = annoyance, too long = forget)
- Review branch logic for gaps
- Test alternative channels at each step
- Check if templates render correctly

**Segment size unexpected**
- Verify rule logic (operators, values)
- Check for data quality issues
- Refresh segment evaluation
- Compare with manual audience count
- Test individual rules in isolation

**Webhook failures**
- Verify endpoint URL is accessible
- Check timeout settings
- Review secret/HMAC configuration
- Monitor delivery log for error patterns
- Test with a simple payload first

**Low NPS scores**
- Analyze detractor comments for common themes
- Compare scores across customer segments
- Track score trends over time
- Implement closed-loop feedback process
- Identify specific touchpoints causing dissatisfaction

**Trigger not firing**
- Verify conditions match event properties exactly
- Check cooldown period hasn't been exceeded
- Confirm rule is active (is_active=True)
- Review fire_count for unexpected patterns
- Test with a minimal condition set

**Channel performance disparity**
- Use channel comparison to identify underperformers
- Check rate limits and cooldowns per channel
- Review audience channel preferences
- Test different content formats per channel
- Compare performance across customer segments

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License. See [LICENSE](LICENSE) for details.

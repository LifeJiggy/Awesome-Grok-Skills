# Customer Engagement Agent Architecture

## Overview

The Customer Engagement Agent is a comprehensive omnichannel customer engagement platform that orchestrates personalized communications across email, SMS, push notifications, in-app messaging, social channels, and webhooks. This document describes the complete system architecture, component interactions, data flows, and design patterns.

## System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                     CustomerEngagementAgent (Orchestrator)                    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                         Core Subsystems                                │  │
│  │                                                                        │  │
│  │  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐    │  │
│  │  │   Customer   │  │  Segment         │  │  Message             │    │  │
│  │  │   Manager    │  │  Manager         │  │  Orchestrator        │    │  │
│  │  └──────┬───────┘  └────────┬─────────┘  └──────────┬───────────┘    │  │
│  │         │                   │                        │                 │  │
│  │  ┌──────┴───────┐  ┌───────┴────────┐  ┌───────────┴──────────┐    │  │
│  │  │  Event       │  │  Dynamic       │  │  Rate Limiter        │    │  │
│  │  │  Tracking    │  │  Segmentation  │  │  & Throttling        │    │  │
│  │  └──────────────┘  └────────────────┘  └──────────────────────┘    │  │
│  │                                                                        │  │
│  │  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐    │  │
│  │  │  Campaign    │  │  Journey         │  │  Engagement          │    │  │
│  │  │  Manager     │  │  Manager         │  │  Scorer              │    │  │
│  │  └──────┬───────┘  └────────┬─────────┘  └──────────┬───────────┘    │  │
│  │         │                   │                        │                 │  │
│  │  ┌──────┴───────┐  ┌───────┴────────┐  ┌───────────┴──────────┐    │  │
│  │  │  A/B Testing │  │  Enrollment    │  │  Score Decay &        │    │  │
│  │  │  Engine      │  │  Tracking      │  │  Trend Analysis       │    │  │
│  │  └──────────────┘  └────────────────┘  └──────────────────────┘    │  │
│  │                                                                        │  │
│  │  ┌──────────────┐  ┌──────────────────────────────────────────────┐  │  │
│  │  │ Attribution  │  │  Personalization Engine                       │  │  │
│  │  │ Manager      │  │  Content Rules, Recommendations, Send Time   │  │  │
│  │  └──────────────┘  └──────────────────────────────────────────────┘  │  │
│  │                                                                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐   │  │
│  │  │ Content      │  │ Webhook      │  │ Feedback                 │   │  │
│  │  │ Manager      │  │ Manager      │  │ Collector                │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘   │  │
│  │                                                                        │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────────┐   │  │
│  │  │ Channel      │  │ Trigger      │  │ Audience                 │   │  │
│  │  │ Analytics    │  │ Engine       │  │ Builder                  │   │  │
│  │  └──────────────┘  └──────────────┘  └──────────────────────────┘   │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐  │
│  │                    Channel Layer                                       │  │
│  │   Email │ SMS │ Push │ In-App │ Social │ Webhook │ Direct Mail │ Chat │  │
│  └────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Component Deep Dives

### 1. Customer Manager

Central registry for all customer data including profiles, preferences, lifecycle stages, and engagement history.

```
┌─────────────────────────────────────────────────────┐
│              CustomerManager                         │
│                                                      │
│  ┌─────────────────┐    ┌──────────────────────┐   │
│  │ Customer Registry│    │ Event Store           │   │
│  │ {id: Customer}   │    │ {id: deque[Event]}    │   │
│  └─────────────────┘    └──────────────────────┘   │
│                                                      │
│  Customer Profile:                                  │
│  ┌──────────────────────────────────────────────┐  │
│  │ id, email, phone, name                        │  │
│  │ status, lifecycle_stage                        │  │
│  │ engagement_score, lifetime_value               │  │
│  │ channel_preferences, opt_out_channels          │  │
│  │ segment_ids, tags                              │  │
│  │ total_purchases, avg_order_value               │  │
│  │ last_active, created_at                        │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Operations:                                        │
│  create_customer() → update_customer() →            │
│  record_event() → get_events() → search()          │
│  bulk_create_customers() → add_tag() →             │
│  opt_out_channel() → delete_customer()              │
└─────────────────────────────────────────────────────┘
```

**Customer Status Lifecycle:**
```
┌──────────┐     ┌──────────┐     ┌──────────┐
│ PROSPECT │────▶│  ACTIVE  │────▶│   VIP    │
└──────────┘     └────┬─────┘     └──────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌──────────┐   ┌──────────┐   ┌──────────┐
│ AT_RISK  │   │  DORMANT │   │CHURNED   │
└────┬─────┘   └──────────┘   └────┬─────┘
     │                              │
     ▼                              ▼
┌──────────┐                  ┌──────────┐
│RECOVERED │◀─────────────────│WINBACK   │
└──────────┘                  └──────────┘
```

### 2. Segment Manager

Dynamic customer segmentation based on behavioral, demographic, transactional, and lifecycle criteria.

```
┌─────────────────────────────────────────────────────┐
│              SegmentManager                          │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Segment Registry                               │  │
│  │ {id: Segment}                                  │  │
│  │                                                │  │
│  │ Segment Types:                                │  │
│  │ - BEHAVIORAL: based on actions/events         │  │
│  │ - DEMOGRAPHIC: age, location, language        │  │
│  │ - TRANSACTIONAL: purchase history, AOV        │  │
│  │ - ENGAGEMENT: score-based                     │  │
│  │ - LIFECYCLE: stage-based                      │  │
│  │ - CUSTOM: rule-based                          │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Rule Evaluation:                                   │
│  ┌──────────────────────────────────────────────┐  │
│  │ {field, operator, value}                       │  │
│  │                                                │  │
│  │ Operators: eq, neq, gt, lt, gte, lte,        │  │
│  │            in, contains                        │  │
│  │                                                │  │
│  │ All rules AND'd by default                    │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Segment Operations:                               │
│  union: A ∪ B                                       │
│  intersection: A ∩ B                               │
│  difference: A - B                                  │
│  clone, overlap analysis                           │
└─────────────────────────────────────────────────────┘
```

**Segment Evaluation Flow:**
```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Load    │────▶│  For Each    │────▶│  Evaluate    │
│  Rules   │     │  Customer    │     │  Rules       │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Update      │◀────│  Match?    │
                   │  Segment     │     │  Add/Remove│
                   └──────────────┘     └────────────┘
```

### 3. Message Orchestrator

Handles message creation, personalization, rate limiting, and delivery across all channels.

```
┌─────────────────────────────────────────────────────┐
│           MessageOrchestrator                        │
│                                                      │
│  ┌─────────────────┐    ┌──────────────────────┐   │
│  │ Message Ledger   │    │ Template Registry     │   │
│  │ [Message, ...]   │    │ {id: Template}        │   │
│  └─────────────────┘    └──────────────────────┘   │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Channel Configuration                         │  │
│  │ {channel: {daily_limit, cooldown, enabled}}   │  │
│  │                                                │  │
│  │ Default Limits:                                │  │
│  │ - Email: 10/day, 24h cooldown                 │  │
│  │ - SMS: 3/day, 48h cooldown                    │  │
│  │ - Push: 5/day, 6h cooldown                    │  │
│  │ - In-App: 20/day, 1h cooldown                 │  │
│  │ - Social: 2-5/day, 4-12h cooldown             │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Send Counter                                   │  │
│  │ {date: {customer_channel: count}}              │  │
│  │ Rate limit check before every send             │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Send Flow:                                         │
│  validate → rate_limit → template → send → record   │
│                                                      │
│  Additional:                                        │
│  get_daily_volume(), get_message_by_id()            │
└─────────────────────────────────────────────────────┘
```

**Message Lifecycle:**
```
┌────────┐    ┌─────────┐    ┌──────────┐    ┌─────────┐
│ PENDING│───▶│  SENT   │───▶│DELIVERED │───▶│ OPENED  │
└────────┘    └─────────┘    └──────────┘    └────┬────┘
                                                  │
                                         ┌────────▼────────┐
                                         │    CLICKED      │
                                         └────────┬────────┘
                                                  │
                                         ┌────────▼────────┐
                                         │   CONVERTED     │
                                         └─────────────────┘
```

### 4. Campaign Manager

Manages campaign lifecycle from creation through execution, A/B testing, and performance analysis.

```
┌─────────────────────────────────────────────────────┐
│              CampaignManager                         │
│                                                      │
│  ┌─────────────────┐    ┌──────────────────────┐   │
│  │ Campaign Registry│    │ A/B Test Registry     │   │
│  │ {id: Campaign}   │    │ {id: ABTest}          │   │
│  └─────────────────┘    └──────────────────────┘   │
│                                                      │
│  Campaign Lifecycle:                                │
│  DRAFT → SCHEDULED → RUNNING → COMPLETED            │
│                           ↓                         │
│                        PAUSED                       │
│                                                      │
│  Campaign Metrics:                                  │
│  - total_sent → total_delivered → total_opened      │
│  - total_clicked → total_converted                  │
│                                                      │
│  Performance Rates:                                 │
│  delivery_rate = delivered / sent                    │
│  open_rate = opened / delivered                      │
│  click_rate = clicked / opened                      │
│  conversion_rate = converted / clicked              │
│  unsubscribe_rate = unsubscribed / sent             │
└─────────────────────────────────────────────────────┘
```

**A/B Testing Engine:**
```
┌─────────────────────────────────────────────────────┐
│              ABTest Engine                           │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Test Configuration                             │  │
│  │ - variants: [{name, content, subject}]         │  │
│  │ - traffic_split: {variant: percentage}         │  │
│  │ - primary_metric: open_rate|click_rate|...     │  │
│  │ - confidence_level: 0.95 (95%)                 │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Result Collection                              │  │
│  │ {variant: {values: [...], count: N}}           │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Analysis:                                          │
│  - Calculate mean and std for each variant          │
│  - Determine winner by primary metric               │
│  - Confidence based on sample size                  │
│  - Statistical significance at confidence_level     │
└─────────────────────────────────────────────────────┘
```

### 5. Journey Manager

Orchestrates multi-step customer journeys with branching logic, delays, and conditional execution.

```
┌─────────────────────────────────────────────────────┐
│              JourneyManager                          │
│                                                      │
│  ┌─────────────────┐    ┌──────────────────────┐   │
│  │ Journey Registry │    │ Enrollment Tracker    │   │
│  │ {id: Journey}    │    │ {id: Enrollment}      │   │
│  └─────────────────┘    └──────────────────────┘   │
│                                                      │
│  Journey Structure:                                 │
│  ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐    │
│  │Step 1│───▶│Step 2│───▶│Step 3│───▶│Step 4│    │
│  └──┬───┘    └──┬───┘    └──┬───┘    └──────┘    │
│     │           │           │                       │
│     ▼           ▼           ▼                       │
│  ┌──────┐   ┌──────┐   ┌──────┐                   │
│  │Branch│   │Branch│   │Branch│                   │
│  └──────┘   └──────┘   └──────┘                   │
│                                                      │
│  Step Properties:                                   │
│  - channel: which channel to use                    │
│  - delay_hours: wait before executing               │
│  - conditions: when to execute                      │
│  - template_id: message template                    │
│  - timeout_hours: max wait time                     │
│  - next_step_on_action: branch on engagement        │
│  - next_step_on_inaction: branch on no engagement   │
│                                                      │
│  Enrollment States:                                 │
│  active → completed | dropped | waiting             │
└─────────────────────────────────────────────────────┘
```

**Journey Execution Flow:**
```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│ Trigger  │────▶│   Enroll     │────▶│   Execute    │
│ Event    │     │   Customer   │     │   Step 1     │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Wait        │◀────│  Delay     │
                   │  (hours)     │     │  Timer     │
                   └──────┬───────┘     └────────────┘
                          │
                          ▼
                   ┌──────────────┐     ┌──────────────┐
                   │  Check       │────▶│  Next Step   │
                   │  Conditions  │     │  or Branch   │
                   └──────────────┘     └──────────────┘
```

### 6. Engagement Scorer

Calculates and tracks customer engagement scores based on behavioral events with time-based decay.

```
┌─────────────────────────────────────────────────────┐
│             EngagementScorer                         │
│                                                      │
│  Scoring Rules:                                     │
│  ┌──────────────────┬──────────┐                    │
│  │ Event Type       │ Points   │                    │
│  ├──────────────────┼──────────┤                    │
│  │ email_open       │ 2.0      │                    │
│  │ email_click      │ 5.0      │                    │
│  │ sms_click        │ 7.0      │                    │
│  │ purchase         │ 20.0     │                    │
│  │ app_open         │ 1.0      │                    │
│  │ page_view        │ 0.5      │                    │
│  │ signup           │ 10.0     │                    │
│  │ referral         │ 15.0     │                    │
│  │ review           │ 8.0      │                    │
│  │ social_share     │ 3.0      │                    │
│  └──────────────────┴──────────┘                    │
│                                                      │
│  Decay Formula:                                     │
│  adjusted_weight = weight × decay_rate^days_ago     │
│  decay_rate = 0.95 (configurable)                   │
│                                                      │
│  Score Range: 0.0 - 100.0                           │
│  Trend: increasing | stable | decreasing            │
│                                                      │
│  Score Distribution:                                │
│  0-20: Low Engagement                               │
│  20-40: Below Average                               │
│  40-60: Average                                     │
│  60-80: Above Average                               │
│  80-100: High Engagement                            │
│                                                      │
│  Additional: get_score_percentiles()                │
└─────────────────────────────────────────────────────┘
```

**Engagement Score Calculation:**
```
1. Fetch all events for customer (limit 1000)
2. For each event:
   a. Get base weight from scoring_rules
   b. Calculate days ago = (now - event.timestamp).days
   c. Apply decay: adjusted = weight × 0.95^days_ago
   d. Accumulate to factors[event_type]
   e. Accumulate to channel_scores[channel]
3. total_score = sum(factors.values())
4. Normalize: min(100.0, total_score)
5. Compare to previous score for trend
6. Update customer.engagement_score
```

### 7. Attribution Manager

Tracks customer touchpoints and attributes conversions across campaigns and channels using various models.

```
┌─────────────────────────────────────────────────────┐
│             AttributionManager                       │
│                                                      │
│  Touchpoint Ledger:                                 │
│  [AttributionEntry, ...]                            │
│  {customer_id, campaign_id, channel, time, value}   │
│                                                      │
│  Attribution Models:                                │
│  ┌──────────────────────────────────────────────┐  │
│  │ FIRST_TOUCH: 100% to first touchpoint         │  │
│  │ LAST_TOUCH: 100% to last touchpoint           │  │
│  │ LINEAR: Equal credit to all touchpoints       │  │
│  │ TIME_DECAY: More credit to recent             │  │
│  │ POSITION_BASED: 40% first, 40% last, 20% mid │  │
│  │ DATA_DRIVEN: Algorithmic (future)             │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Summaries:                                         │
│  - Campaign attribution: which campaigns drive      │
│    conversions                                      │
│  - Channel attribution: which channels are most     │
│    effective                                        │
└─────────────────────────────────────────────────────┘
```

**Attribution Model Comparison:**
```
Touchpoints: T1(campaign_A) → T2(campaign_B) → T3(campaign_C) → Conversion

FIRST_TOUCH:  A=100%, B=0%, C=0%
LAST_TOUCH:   A=0%, B=0%, C=100%
LINEAR:       A=33%, B=33%, C=33%
TIME_DECAY:   A=17%, B=33%, C=50%
POSITION:     A=40%, B=20%, C=40%
```

### 8. Personalization Engine

Provides content personalization, recommendations, and optimal send time predictions.

```
┌─────────────────────────────────────────────────────┐
│          PersonalizationEngine                       │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Content Rules                                 │  │
│  │ {rule_id: {conditions, content}}              │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Personalization Levels:                            │
│  NONE → BASIC → ADVANCED → DYNAMIC → AI_POWERED    │
│                                                      │
│  Basic: Greeting, language                          │
│  Advanced: Tier-based content, lifecycle stage      │
│  Dynamic: Behavior-based, real-time triggers        │
│  AI-Powered: Predictive, ML-driven (future)        │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Recommendation Engine                         │  │
│  │ - Product views → similar products            │  │
│  │ - Cart abandonment → reminder                 │  │
│  │ - At-risk → winback offer                     │  │
│  │ - High engagement → referral                  │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Optimal Send Time                             │  │
│  │ - Analyze hourly activity patterns            │  │
│  │ - Identify peak engagement hours              │  │
│  │ - Per-customer optimization                   │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### 9. Content Manager

Manages reusable content blocks with variable interpolation and versioning.

```
┌─────────────────────────────────────────────────────┐
│              ContentManager                          │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Content Block Registry                        │  │
│  │ {id: ContentBlock}                            │  │
│  │                                                │  │
│  │ Block Properties:                             │  │
│  │ - name, format (plain/html/markdown/json)     │  │
│  │ - content, variables, channel                 │  │
│  │ - version, is_active                          │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Operations:                                        │
│  create_block() → render_block() → update_block()  │
│  get_blocks_by_channel() → clone_block()           │
│                                                      │
│  Render Flow:                                       │
│  "Hello {{name}}!" + {name: "John"} → "Hello John!"│
└─────────────────────────────────────────────────────┘
```

### 10. Webhook Manager

Handles outbound webhook registration, delivery, and monitoring.

```
┌─────────────────────────────────────────────────────┐
│              WebhookManager                          │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Webhook Registry                              │  │
│  │ {id: WebhookConfig}                           │  │
│  │                                                │  │
│  │ Config Properties:                            │  │
│  │ - url, events, status, secret                 │  │
│  │ - retry_count, timeout_seconds                │  │
│  │ - headers, failure_count                      │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Delivery Log                                  │  │
│  │ [{webhook_id, url, event_type, status, ...}]  │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Delivery Flow:                                     │
│  event → match webhooks → filter by status/events   │
│  → deliver → log result → update stats              │
└─────────────────────────────────────────────────────┘
```

### 11. Feedback Collector

Gathers and analyzes customer feedback across multiple types.

```
┌─────────────────────────────────────────────────────┐
│             FeedbackCollector                        │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Feedback Entry Store                          │  │
│  │ {id: FeedbackEntry}                           │  │
│  │                                                │  │
│  │ Types: CSAT, NPS, CES, SURVEY, REVIEW, RATING│  │
│  │                                                │  │
│  │ Properties:                                   │  │
│  │ - score, comment, sentiment                   │  │
│  │ - channel, campaign_id                        │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Analytics:                                         │
│  - get_average_score() by type                      │
│  - get_sentiment_distribution()                     │
│  - get_nps_score() with promoters/passives/detract │
│  - get_feedback_summary()                           │
└─────────────────────────────────────────────────────┘
```

### 12. Channel Analytics

Cross-channel performance comparison and efficiency metrics.

```
┌─────────────────────────────────────────────────────┐
│             ChannelAnalytics                         │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Performance Cache                              │  │
│  │ {channel: ChannelPerformance}                 │  │
│  │                                                │  │
│  │ Metrics per channel:                          │  │
│  │ - sent, delivered, opened, clicked, converted │  │
│  │ - delivery_rate, open_rate, click_rate        │  │
│  │ - bounce_rate, complaint_rate                 │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Comparison:                                        │
│  - get_comparison() across all channels             │
│  - get_channel_efficiency() per channel             │
│  - Sort by click_rate for best performers           │
└─────────────────────────────────────────────────────┘
```

### 13. Trigger Engine

Event-driven automation with rules, conditions, and cooldown periods.

```
┌─────────────────────────────────────────────────────┐
│              TriggerEngine                           │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Trigger Rule Registry                         │  │
│  │ {id: TriggerRule}                             │  │
│  │                                                │  │
│  │ Rule Properties:                              │  │
│  │ - trigger_type: EVENT|SCHEDULE|THRESHOLD      │  │
│  │ - conditions: [{type, value}]                 │  │
│  │ - actions: [{type, channel, ...}]             │  │
│  │ - cooldown_minutes, last_fired, fire_count    │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Execution Flow:                                    │
│  event → check rules → match conditions?            │
│  → check cooldown → execute actions → update stats  │
│                                                      │
│  Action Types:                                      │
│  - send_message: fire a message on a channel        │
│  - update_status: change customer lifecycle status  │
└─────────────────────────────────────────────────────┘
```

### 14. Audience Builder

Composite audience creation from segment combinations.

```
┌─────────────────────────────────────────────────────┐
│              AudienceBuilder                         │
│                                                      │
│  ┌──────────────────────────────────────────────┐  │
│  │ Audience Registry                             │  │
│  │ {id: {name, segments, size, customer_ids}}    │  │
│  └──────────────────────────────────────────────┘  │
│                                                      │
│  Operations:                                        │
│  - build_audience(): combine segments              │
│  - exclude_audience(): set difference               │
│  - intersect_audiences(): set intersection          │
│  - refresh_audience(): re-evaluate from segments    │
└─────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### Customer Engagement Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Create  │────▶│  Track       │────▶│  Score       │
│  Profile │     │  Events      │     │  Engagement  │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Personalize │◀────│  Segment   │
                   │  Content     │     │  Customer  │
                   └──────┬───────┘     └────────────┘
                          │
                          ▼
                   ┌──────────────┐     ┌──────────────┐
                   │  Send via    │────▶│  Track       │
                   │  Channel     │     │  Response    │
                   └──────────────┘     └──────┬───────┘
                                               │
                   ┌──────────────┐     ┌──────▼───────┐
                   │  Update      │◀────│  Attribute   │
                   │  Score       │     │  Conversion  │
                   └──────────────┘     └──────────────┘
```

### Campaign Execution Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Create  │────▶│  Select      │────▶│  Build       │
│  Campaign│     │  Segments    │     │  Audience    │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Send via    │◀────│  Apply     │
                   │  Channels    │     │  Templates │
                   └──────┬───────┘     └────────────┘
                          │
                          ▼
                   ┌──────────────┐     ┌──────────────┐
                   │  Track       │────▶│  Analyze     │
                   │  Results     │     │  Performance │
                   └──────────────┘     └──────────────┘
```

### Journey Orchestration Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Define  │────▶│  Set Entry   │────▶│  Configure   │
│  Journey │     │  Criteria    │     │  Steps       │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Enroll      │◀────│  Activate  │
                   │  Customers   │     │  Journey   │
                   └──────┬───────┘     └────────────┘
                          │
                          ▼
                   ┌──────────────┐     ┌──────────────┐
                   │  Execute     │────▶│  Branch      │
                   │  Steps       │     │  on Action   │
                   └──────┬───────┘     └──────┬───────┘
                          │                    │
                          ▼                    ▼
                   ┌──────────────────────────────────┐
                   │  Complete | Continue | Drop       │
                   └──────────────────────────────────┘
```

### Trigger-Driven Automation Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Event   │────▶│  Trigger     │────▶│  Check       │
│  Arrives │     │  Engine      │     │  Rules       │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Execute     │◀────│  Match?    │
                   │  Actions     │     │  Cooldown? │
                   └──────┬───────┘     └────────────┘
                          │
                          ▼
                   ┌──────────────┐     ┌──────────────┐
                   │  Send Msg /  │────▶│  Update      │
                   │  Update Sts  │     │  Fire Count  │
                   └──────────────┘     └──────────────┘
```

### Webhook Delivery Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  System  │────▶│  Webhook     │────▶│  Match       │
│  Event   │     │  Manager     │     │  Subscribers │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Deliver     │◀────│  Filter    │
                   │  Payload     │     │  by Status │
                   └──────┬───────┘     └────────────┘
                          │
                          ▼
                   ┌──────────────┐     ┌──────────────┐
                   │  Log Result  │────▶│  Update      │
                   │  (delivered) │     │  Stats       │
                   └──────────────┘     └──────────────┘
```

## Design Patterns

### 1. Observer Pattern
Event recording notifies multiple subsystems (scoring, segmentation, attribution) simultaneously.

### 2. Strategy Pattern
Attribution models (first-touch, last-touch, linear, etc.) implement different strategies for credit allocation.

### 3. State Machine
Customer status and campaign status follow state machine patterns with defined transitions.

### 4. Template Method
Message creation follows a template: validate → personalize → rate-limit → send → record.

### 5. Chain of Responsibility
Journey steps form a chain where each step can pass execution to the next or branch based on conditions.

### 6. Registry Pattern
All entities (customers, segments, campaigns, templates) use registry dictionaries for O(1) lookup.

### 7. Builder Pattern
AudienceBuilder combines segments with set operations (union, intersection, difference) to compose target audiences.

### 8. Command Pattern
TriggerEngine encapsulates actions (send_message, update_status) as commands that can be registered and replayed.

## Thread Safety Model

```
┌──────────────────────────────────────────────────────┐
│           Thread Safety Architecture                  │
│                                                       │
│  Each manager has independent lock:                  │
│                                                       │
│  ┌──────────────────┐  ┌──────────────────────┐     │
│  │ CustomerManager._ │  │ SegmentManager._lock │     │
│  │ lock              │  └──────────────────────┘     │
│  └──────────────────┘                                │
│                                                       │
│  ┌──────────────────┐  ┌──────────────────────┐     │
│  │ MessageOrch._lock│  │ CampaignManager._lock│     │
│  └──────────────────┘  └──────────────────────┘     │
│                                                       │
│  ┌──────────────────┐  ┌──────────────────────┐     │
│  │ JourneyMgr._lock │  │ Scorer._lock         │     │
│  └──────────────────┘  └──────────────────────┘     │
│                                                       │
│  ┌──────────────────┐  ┌──────────────────────┐     │
│  │ ContentMgr._lock │  │ WebhookMgr._lock     │     │
│  └──────────────────┘  └──────────────────────┘     │
│                                                       │
│  ┌──────────────────┐  ┌──────────────────────┐     │
│  │ Feedback._lock   │  │ TriggerEngine._lock   │     │
│  └──────────────────┘  └──────────────────────┘     │
│                                                       │
│  ┌──────────────────┐  ┌──────────────────────┐     │
│  │ AudienceBuilder. │  │ ChannelAnalytics._lock│     │
│  │ _lock            │  └──────────────────────┘     │
│  └──────────────────┘                                │
│                                                       │
│  Pattern: Copy-on-read for queries                   │
│  Lock scope: Single operation, no nesting            │
└──────────────────────────────────────────────────────┘
```

## Performance Targets

| Operation | Target Latency | Current |
|-----------|---------------|---------|
| Customer Create | < 10ms | ~2ms |
| Event Record | < 5ms | ~1ms |
| Segment Evaluate | < 100ms | ~30ms |
| Message Send | < 50ms | ~15ms |
| Score Calculate | < 200ms | ~50ms |
| Campaign Execute | < 5s per 1000 | ~2s |
| Journey Process | < 100ms | ~25ms |
| Content Render | < 10ms | ~3ms |
| Webhook Trigger | < 50ms | ~10ms |
| Feedback Collect | < 10ms | ~2ms |
| Trigger Process | < 20ms | ~5ms |
| Audience Build | < 200ms | ~40ms |

## Scalability Considerations

### Horizontal Scaling
- Customer data sharded by customer_id
- Event processing distributed across workers
- Message sending parallelized by channel

### Vertical Scaling
- Event store uses bounded deques (10000 max)
- Score cache with LRU eviction
- Campaign results aggregated incrementally

### Data Volume
- 1M customers: ~500MB memory
- 10M events/day: ~10GB/day raw
- Campaign history: ~100MB/month
- Webhook delivery log: ~50MB/month

### Throughput Targets
- 100K messages/day across all channels
- 10K event ingestion per second
- 1K trigger evaluations per second
- 100 webhook deliveries per second

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
  max_delivery_log_size: 100000

feedback:
  sentiment_threshold_positive: 8.0
  sentiment_threshold_negative: 4.0

scoring:
  decay_rate: 0.95
  max_score: 100.0
  custom_rules: {}
```

## Security Considerations

### Data Privacy
- Customer PII encrypted at rest
- Opt-out preferences respected across all channels
- GDPR/CCPA compliance hooks
- Feedback anonymization support

### Rate Limiting
- Per-customer daily limits prevent spam
- Cooldown periods between messages
- Global daily send caps
- Trigger cooldown periods

### Access Control
- Campaign creation requires authorization
- Customer data access logged
- Template modifications versioned
- Webhook secrets for HMAC verification

### Webhook Security
- Secret-based HMAC signatures
- Configurable retry policies
- Timeout protection
- Failure count monitoring

## Future Extensions

1. **ML-Powered Scoring**: Replace rule-based with trained models
2. **Real-Time Stream Processing**: Kafka/Pulsar event ingestion
3. **Multi-Variate Testing**: Beyond A/B to A/B/n testing
4. **Predictive Churn**: ML-based at-risk identification
5. **Dynamic Content**: Real-time content optimization
6. **Omnichannel Attribution**: Unified cross-channel view
7. **Customer Data Platform**: Unified profile across systems
8. **Marketing Automation**: Complex trigger-based workflows
9. **Sentiment Analysis**: NLP-powered feedback processing
10. **Predictive Send Time**: ML-optimized delivery scheduling

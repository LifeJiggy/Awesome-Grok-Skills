# Customer Retention Agent Architecture

## Overview

The Customer Retention Agent is a comprehensive churn prediction and customer retention platform. It provides tools for predicting customer churn, managing loyalty programs, analyzing NPS scores, executing retention strategies, running win-back campaigns, performing cohort analysis, monitoring customer health, managing renewals and contracts, analyzing sentiment, handling escalations, and categorizing churn reasons. This document details the complete system architecture.

## System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                        CustomerRetentionAgent (Orchestrator)                          │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐  │
│  │                            Core Subsystems                                     │  │
│  │                                                                                │  │
│  │  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐            │  │
│  │  │   Churn      │  │  Loyalty         │  │  NPS                 │            │  │
│  │  │   Predictor  │  │  Manager         │  │  Manager             │            │  │
│  │  └──────┬───────┘  └────────┬─────────┘  └──────────┬───────────┘            │  │
│  │         │                   │                        │                         │  │
│  │  ┌──────┴───────┐  ┌───────┴────────┐  ┌───────────┴──────────┐            │  │
│  │  │  Signal      │  │  Points &      │  │  Survey Lifecycle    │            │  │
│  │  │  Tracking    │  │  Tier Engine   │  │  & Scoring           │            │  │
│  │  └──────────────┘  └────────────────┘  └──────────────────────┘            │  │
│  │                                                                                │  │
│  │  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐            │  │
│  │  │  Cohort      │  │  Retention       │  │  Win-Back            │            │  │
│  │  │  Analyzer    │  │  Strategy Engine │  │  Manager             │            │  │
│  │  └──────┬───────┘  └────────┬─────────┘  └──────────┬───────────┘            │  │
│  │         │                   │                        │                         │  │
│  │  ┌──────┴───────┐  ┌───────┴────────┐  ┌───────────┴──────────┐            │  │
│  │  │  Retention   │  │  Recommendation │  │  Campaign            │            │  │
│  │  │  Curves      │  │  & Execution    │  │  Enrollment          │            │  │
│  │  └──────────────┘  └────────────────┘  └──────────────────────┘            │  │
│  └────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐  │
│  │                          Extended Subsystems                                    │  │
│  │                                                                                │  │
│  │  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐            │  │
│  │  │  Health      │  │  Renewal         │  │  Contract            │            │  │
│  │  │  Monitor     │  │  Manager         │  │  Tracker             │            │  │
│  │  └──────────────┘  └──────────────────┘  └──────────────────────┘            │  │
│  │                                                                                │  │
│  │  ┌──────────────┐  ┌──────────────────┐  ┌──────────────────────┐            │  │
│  │  │  Sentiment   │  │  Escalation      │  │  Churn Reason        │            │  │
│  │  │  Analyzer    │  │  Engine          │  │  Analyzer            │            │  │
│  │  └──────────────┘  └──────────────────┘  └──────────────────────┘            │  │
│  │                                                                                │  │
│  │  ┌──────────────────────────────────────────────────────────────┐              │  │
│  │  │                   RetentionDashboard                         │              │  │
│  │  │              Alerts · Snapshots · Monitoring                 │              │  │
│  │  └──────────────────────────────────────────────────────────────┘              │  │
│  └────────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

## Component Deep Dives

### 1. Churn Predictor

Predicts customer churn using behavioral signals with weighted scoring and trend analysis.

```
┌─────────────────────────────────────────────────────────┐
│                   ChurnPredictor                         │
│                                                          │
│  Signal Weights:                                        │
│  ┌─────────────────────────┬──────────┐                │
│  │ Signal                  │ Weight   │                │
│  ├─────────────────────────┼──────────┤                │
│  │ login_decrease          │ 0.30     │                │
│  │ support_ticket_increase │ 0.20     │                │
│  │ feature_usage_decline   │ 0.25     │                │
│  │ payment_failure         │ 0.40     │                │
│  │ contract_near_expiry    │ 0.15     │                │
│  │ negative_feedback       │ 0.35     │                │
│  │ competitor_mention      │ 0.20     │                │
│  │ downgrade_request       │ 0.50     │                │
│  │ reduced_engagement      │ 0.20     │                │
│  │ missed_renewal          │ 0.60     │                │
│  └─────────────────────────┴──────────┘                │
│                                                          │
│  Risk Levels:                                           │
│  LOW:      score < 0.3                                  │
│  MEDIUM:   0.3 <= score < 0.5                           │
│  HIGH:     0.5 <= score < 0.7                           │
│  CRITICAL: score >= 0.7                                 │
│                                                          │
│  Calculation:                                           │
│  risk_score = Σ(signal_value × weight) / count          │
│  Additional factors:                                    │
│  - Days since last active (30+ days → inactivity)       │
│  - Days to contract expiry (<90 days → urgency)         │
│                                                          │
│  Confidence: min(0.95, 0.5 + history_count × 0.01)     │
└─────────────────────────────────────────────────────────┘
```

**Churn Score Pipeline:**
```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Collect │────▶│  Apply       │────▶│  Calculate   │
│  Signals │     │  Weights     │     │  Risk Score  │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Assign      │◀────│  Classify  │
                   │  Actions     │     │  Risk Level│
                   └──────────────┘     └────────────┘
```

**Internal State:**
```
_customers:  Dict[str, Customer]           # customer_id → Customer
_predictions: Dict[str, ChurnPrediction]   # customer_id → latest prediction
_signal_weights: Dict[str, float]          # signal_name → weight
_history: Dict[str, deque]                 # customer_id → signal history (maxlen=100)
_lock: threading.Lock                      # protects all mutable state
```

### 2. Loyalty Manager

Manages loyalty points, tier progression, rewards catalog, and redemption tracking.

```
┌─────────────────────────────────────────────────────────┐
│                   LoyaltyManager                         │
│                                                          │
│  Tier Structure:                                        │
│  ┌──────────┬──────────┬──────────┬────────────┐       │
│  │ Tier     │ Min Pts  │ Multiplier│ Benefits   │       │
│  ├──────────┼──────────┼──────────┼────────────┤       │
│  │ BRONZE   │ 0        │ 1.0x     │ Basic      │       │
│  │ SILVER   │ 1,000    │ 1.25x    │ 5% off     │       │
│  │ GOLD     │ 5,000    │ 1.5x     │ 10% off    │       │
│  │ PLATINUM │ 15,000   │ 2.0x     │ 15% off    │       │
│  │ DIAMOND  │ 50,000   │ 3.0x     │ 20% off    │       │
│  └──────────┴──────────┴──────────┴────────────┘       │
│                                                          │
│  Operations:                                            │
│  - earn: add_points() with multiplier                   │
│  - redeem: deduct points for rewards                    │
│  - expire: auto-expire old points                       │
│  - adjust: manual balance adjustments                   │
│                                                          │
│  ┌──────────────────────────────────────────────┐      │
│  │ Rewards Catalog                               │      │
│  │ {reward_id: {name, cost, type, value, stock}} │      │
│  │ Types: discount, free_product, gift_card      │      │
│  └──────────────────────────────────────────────┘      │
│                                                          │
│  Additional Operations:                                │
│  - get_points_summary: earn/redeem/expire breakdown     │
│  - get_top_earners: leaderboard by points balance       │
│  - expire_points: manual point expiration               │
│  - get_redemption_rate: points redeemed vs earned       │
└─────────────────────────────────────────────────────────┘
```

**Tier Progression:**
```
points_balance → find_highest_matching_tier → update customer.tier
DIAMOND threshold: 50,000 points
PLATINUM threshold: 15,000 points
GOLD threshold: 5,000 points
SILVER threshold: 1,000 points
BRONZE: default (0+)

Upgrade logged at INFO level when tier increases.
```

**Internal State:**
```
_balances: Dict[str, int]                    # customer_id → points
_tiers: Dict[str, LoyaltyTier]               # customer_id → current tier
_transactions: Dict[str, List[LoyaltyTransaction]]  # customer_id → history
_rewards: Dict[str, LoyaltyReward]           # reward_id → reward
_redemptions: List[Dict[str, Any]]           # all redemption records
_lock: threading.Lock
```

### 3. NPS Manager

Manages Net Promoter Score surveys, response collection, and trend analysis.

```
┌─────────────────────────────────────────────────────────┐
│                   NPSManager                             │
│                                                          │
│  Score Categories:                                      │
│  ┌──────────────────────────────────────────────┐      │
│  │ DETRACTOR:  0-6  (Unhappy customers)         │      │
│  │ PASSIVE:    7-8  (Satisfied but unenthusiastic)│      │
│  │ PROMOTER:   9-10 (Loyal enthusiasts)          │      │
│  └──────────────────────────────────────────────┘      │
│                                                          │
│  NPS Calculation:                                       │
│  NPS = (% Promoters - % Detractors) × 100              │
│  Range: -100 to +100                                    │
│                                                          │
│  Survey Lifecycle:                                      │
│  DRAFT → SENT → COMPLETED | EXPIRED                     │
│                                                          │
│  Trend Analysis:                                        │
│  Monthly NPS calculation over configurable period       │
│  Feedback theme aggregation by category                 │
│                                                          │
│  Additional Features:                                   │
│  - Segment-based NPS breakdown                          │
│  - Response rate tracking                               │
│  - Survey expiration management                         │
└─────────────────────────────────────────────────────────┘
```

**NPS Score Interpretation:**
```
NPS > 50:  Excellent - strong loyalty
NPS 30-50: Good - healthy retention
NPS 0-30:  Needs improvement
NPS < 0:   Critical - high churn risk
```

### 4. Cohort Analyzer

Groups customers into cohorts and tracks retention curves over time.

```
┌─────────────────────────────────────────────────────────┐
│                   CohortAnalyzer                         │
│                                                          │
│  Cohort Types:                                          │
│  - MONTHLY: by acquisition month                         │
│  - WEEKLY: by acquisition week                           │
│  - QUARTERLY: by acquisition quarter                     │
│  - ACQUISITION_CHANNEL: by source                        │
│  - PLAN_TYPE: by subscription tier                       │
│  - GEOGRAPHY: by location                                │
│                                                          │
│  Retention Curve:                                       │
│  ┌──────────────────────────────────────────────┐      │
│  │ Period 0: 100% (initial cohort)               │      │
│  │ Period 1: 85% retained                        │      │
│  │ Period 2: 72% retained                        │      │
│  │ Period 3: 65% retained                        │      │
│  │ ...                                           │      │
│  │ Period N: X% retained                         │      │
│  └──────────────────────────────────────────────┘      │
│                                                          │
│  Comparison:                                            │
│  - Compare retention curves across cohorts              │
│  - Identify best/worst performing cohorts               │
│  - Track improvement over time                          │
└─────────────────────────────────────────────────────────┘
```

### 5. Retention Strategy Engine

Recommends and executes retention strategies based on churn predictions.

```
┌─────────────────────────────────────────────────────────┐
│             RetentionStrategyEngine                      │
│                                                          │
│  Strategy Templates:                                    │
│  ┌──────────────────────┬────────────────────────┐     │
│  │ Strategy             │ Trigger                │     │
│  ├──────────────────────┼────────────────────────┤     │
│  │ ENGAGEMENT_INCREASE  │ churn_score >= 0.3     │     │
│  │ DISCOUNT_OFFER       │ churn_score >= 0.5     │     │
│  │ PERSONAL_OUTREACH    │ churn_score >= 0.7     │     │
│  │ FEATURE_HIGHLIGHT    │ engagement < 40        │     │
│  │ LOYALTY_REWARD       │ tier >= GOLD           │     │
│  │ EXIT_SURVEY          │ churn_score >= 0.8     │     │
│  │ SUCCESS_MANAGER      │ ltv > 10K & score > 0.4│     │
│  └──────────────────────┴────────────────────────┘     │
│                                                          │
│  Execution Flow:                                        │
│  predict_churn() → get_recommended_strategies()         │
│  → execute_strategy() → record_outcome()                │
│                                                          │
│  Outcome Tracking:                                      │
│  - converted: customer retained                         │
│  - churned: customer lost despite intervention          │
│  - pending: awaiting result                             │
│  - cancelled: strategy withdrawn                        │
└─────────────────────────────────────────────────────────┘
```

### 6. Win-Back Manager

Manages campaigns to re-engage churned customers with multi-step messaging.

```
┌─────────────────────────────────────────────────────────┐
│                   WinbackManager                         │
│                                                          │
│  Campaign Structure:                                    │
│  ┌──────────────────────────────────────────────┐      │
│  │ Campaign                                      │      │
│  │ ├── Message 1: Re-engagement email            │      │
│  │ ├── Message 2: Special offer (day 3)          │      │
│  │ └── Message 3: Final reminder (day 7)         │      │
│  └──────────────────────────────────────────────┘      │
│                                                          │
│  Enrollment States:                                     │
│  active → sent → opened → converted                     │
│                                                          │
│  Metrics:                                               │
│  - total_targeted: customers in campaign                │
│  - total_converted: re-engaged customers                │
│  - conversion_rate: converted / targeted                │
│                                                          │
│  Campaign Management:                                   │
│  - pause_campaign: halt campaign execution              │
│  - resume_campaign: restart paused campaign             │
└─────────────────────────────────────────────────────────┘
```

### 7. Customer Health Monitor

Computes composite health scores from multiple behavioral dimensions.

```
┌─────────────────────────────────────────────────────────┐
│              CustomerHealthMonitor                       │
│                                                          │
│  Score Components:                                      │
│  ┌────────────┬────────┬──────────────────────────┐    │
│  │ Component  │ Weight │ Description              │    │
│  ├────────────┼────────┼──────────────────────────┤    │
│  │ Engagement │ 0.25   │ Login frequency, actions │    │
│  │ Satisfaction│ 0.25  │ NPS, feedback sentiment  │    │
│  │ Financial  │ 0.20   │ Revenue, payment status  │    │
│  │ Support    │ 0.15   │ Ticket volume, sentiment │    │
│  │ Contract   │ 0.15   │ Contract status, renewal │    │
│  └────────────┴────────┴──────────────────────────┘    │
│                                                          │
│  Score Ranges:                                          │
│  excellent: >= 0.8                                      │
│  good:      >= 0.6                                      │
│  fair:      >= 0.4                                      │
│  poor:      >= 0.2                                      │
│  critical:  < 0.2                                       │
│                                                          │
│  Health Trend Tracking:                                 │
│  - Historical score per customer                        │
│  - Component breakdown per snapshot                     │
│  - Automatic alerting when below threshold              │
│                                                          │
│  Weight Configuration:                                  │
│  - All weights should sum to 1.0                        │
│  - Warning logged if total deviates from 1.0            │
│  - Weights adjustable via update_weight()               │
└─────────────────────────────────────────────────────────┘
```

### 8. Renewal Manager

Tracks contract renewal pipeline and revenue retention.

```
┌─────────────────────────────────────────────────────────┐
│                   RenewalManager                         │
│                                                          │
│  Renewal Statuses:                                      │
│  PENDING → INITIATED → IN_NEGOTIATION                   │
│  ├→ RENEWED (success)                                   │
│  ├→ LOST (failure)                                      │
│  ├→ EXPIRED (timeout)                                   │
│  └→ CANCELLED (customer-initiated)                      │
│                                                          │
│  Metrics:                                               │
│  - renewal_rate: renewed / total                        │
│  - revenue_renewed: $ value of renewals                 │
│  - revenue_lost: $ value of lost renewals               │
│  - upcoming: renewals within N days                     │
│                                                          │
│  Status Transitions:                                    │
│  - update_renewal_status() records timestamp            │
│  - lost_reason captured for LOST/CANCELLED              │
│  - renewed_at set on RENEWED transition                 │
└─────────────────────────────────────────────────────────┘
```

### 9. Contract Tracker

Manages contract lifecycle and expiration monitoring.

```
┌─────────────────────────────────────────────────────────┐
│                   ContractTracker                        │
│                                                          │
│  Contract Types:                                        │
│  - MONTHLY: month-to-month                              │
│  - ANNUAL: yearly contracts                             │
│  - MULTI_YEAR: 2+ year agreements                       │
│  - FREE_TRIAL: trial period                             │
│  - ENTERPRISE: custom enterprise deals                  │
│  - CUSTOM: bespoke arrangements                         │
│                                                          │
│  Features:                                              │
│  - Expiration warnings                                  │
│  - Auto-renewal tracking                                │
│  - Termination management                               │
│  - Contract value aggregation                           │
│  - Type-based breakdown                                 │
│                                                          │
│  Status Values:                                         │
│  - active: current contract                             │
│  - terminated: ended early                              │
│  - expired: reached end date                            │
└─────────────────────────────────────────────────────────┘
```

### 10. Sentiment Analyzer

Processes text feedback to extract sentiment scores and levels.

```
┌─────────────────────────────────────────────────────────┐
│                  SentimentAnalyzer                       │
│                                                          │
│  Sentiment Levels:                                      │
│  ┌──────────────────┬───────────────────────────┐      │
│  │ Level            │ Score Range               │      │
│  ├──────────────────┼───────────────────────────┤      │
│  │ VERY_POSITIVE    │ >= 0.4                    │      │
│  │ POSITIVE         │ >= 0.1                    │      │
│  │ NEUTRAL          │ >= -0.1                   │      │
│  │ NEGATIVE         │ >= -0.4                   │      │
│  │ VERY_NEGATIVE    │ < -0.4                    │      │
│  └──────────────────┴───────────────────────────┘      │
│                                                          │
│  Calculation:                                           │
│  score = (positive_words - negative_words) / total      │
│                                                          │
│  Tracking:                                              │
│  - Per-customer average sentiment                       │
│  - Sentiment distribution across all entries            │
│  - Negative customer identification                     │
│  - Trend analysis per customer                          │
│                                                          │
│  Keyword Sets:                                          │
│  POSITIVE: great, excellent, love, amazing, fantastic,  │
│    wonderful, happy, satisfied, impressed, recommend,   │
│    best, perfect                                        │
│  NEGATIVE: bad, terrible, awful, hate, frustrated,      │
│    disappointed, poor, worst, broken, useless, angry,   │
│    unacceptable                                         │
└─────────────────────────────────────────────────────────┘
```

### 11. Escalation Engine

Manages account escalations based on configurable rules.

```
┌─────────────────────────────────────────────────────────┐
│                  EscalationEngine                        │
│                                                          │
│  Escalation Reasons:                                    │
│  ┌────────────────────────┬──────┬─────────────┐       │
│  │ Reason                 │ Sev. │ Auto-Assign │       │
│  ├────────────────────────┼──────┼─────────────┤       │
│  │ HIGH_CHURN_RISK        │ 4    │ Yes         │       │
│  │ NEGATIVE_SENTIMENT     │ 3    │ No          │       │
│  │ PAYMENT_DEFAULT        │ 5    │ Yes         │       │
│  │ SUPPORT_ESCALATION     │ 3    │ Yes         │       │
│  │ COMPETITOR_THREAT      │ 4    │ No          │       │
│  │ CONTRACT_EXPIRY        │ 2    │ Yes         │       │
│  │ USAGE_DECLINE          │ 3    │ No          │       │
│  │ EXECUTIVE_SPONSOR_LOST │ 5    │ Yes         │       │
│  └────────────────────────┴──────┴─────────────┘       │
│                                                          │
│  Lifecycle:                                             │
│  open → resolved                                        │
│                                                          │
│  Features:                                              │
│  - Rule-based severity assignment                       │
│  - Auto-assignment for high-severity cases              │
│  - Resolution tracking with timestamp                   │
│  - Per-customer escalation history                      │
│  - Configurable rules via update_rule()                 │
└─────────────────────────────────────────────────────────┘
```

### 12. Churn Reason Analyzer

Categorizes and tracks root causes of customer churn.

```
┌─────────────────────────────────────────────────────────┐
│              ChurnReasonAnalyzer                         │
│                                                          │
│  Churn Reasons:                                         │
│  ┌──────────────────────┬───────────┐                  │
│  │ Reason               │ Weight    │                  │
│  ├──────────────────────┼───────────┤                  │
│  │ PRICE_SENSITIVITY    │ 0.85      │                  │
│  │ FEATURE_GAP          │ 0.70      │                  │
│  │ POOR_SUPPORT         │ 0.75      │                  │
│  │ COMPETITOR_SWITCH    │ 0.90      │                  │
│  │ BUSINESS_CLOSURE     │ 0.95      │                  │
│  │ BUDGET_CUTS          │ 0.80      │                  │
│  │ LOW_ENGAGEMENT       │ 0.60      │                  │
│  │ PRODUCT_QUALITY      │ 0.70      │                  │
│  │ ONBOARDING_FAILURE   │ 0.65      │                  │
│  │ CHAMPION_LEFT        │ 0.75      │                  │
│  │ CONTRACT_ISSUES      │ 0.55      │                  │
│  │ UNKNOWN              │ 0.50      │                  │
│  └──────────────────────┴───────────┘                  │
│                                                          │
│  Analysis Features:                                     │
│  - Reason distribution tracking                         │
│  - Top reasons ranking                                  │
│  - Recoverable rate calculation                         │
│  - Confidence scoring per entry                         │
│  - Evidence collection per reason                       │
│                                                          │
│  Recoverable Rate:                                      │
│  reasons with weight < 0.8 are considered recoverable  │
└─────────────────────────────────────────────────────────┘
```

### 13. Retention Dashboard

Centralized alerting and monitoring for the retention platform.

```
┌─────────────────────────────────────────────────────────┐
│                RetentionDashboard                        │
│                                                          │
│  Features:                                              │
│  - Active alert management                              │
│  - Severity-based alert filtering                       │
│  - Alert acknowledgment tracking                        │
│  - Periodic metric snapshots                            │
│  - Snapshot history                                     │
│  - Alert summary by severity                            │
│                                                          │
│  Alert Types:                                           │
│  - low_health: health score below threshold             │
│  - high_churn_risk: critical churn prediction           │
│  - renewal_due: contract renewal approaching            │
│  - sentiment_drop: negative sentiment spike             │
│  - escalation_open: unresolved escalation               │
│                                                          │
│  Severity Levels:                                       │
│  critical → high → medium → low → info                  │
│                                                          │
│  Maintenance:                                           │
│  - clear_acknowledged(): removes resolved alerts        │
│  - get_snapshots(): returns recent metric snapshots     │
│  - take_snapshot(): records current metrics             │
└─────────────────────────────────────────────────────────┘
```

## Data Flow Diagrams

### Churn Prediction Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Collect │────▶│  Weight      │────▶│  Calculate   │
│  Signals │     │  & Combine   │     │  Risk Score  │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Recommend   │◀────│  Classify  │
                   │  Actions     │     │  Level     │
                   └──────┬───────┘     └────────────┘
                          │
                          ▼
                   ┌──────────────┐     ┌──────────────┐
                   │  Execute     │────▶│  Escalate    │
                   │  Retention   │     │  if needed   │
                   └──────────────┘     └──────────────┘
```

### Loyalty Points Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Purchase│────▶│  Calculate   │────▶│  Add Points  │
│  Event   │     │  Points      │     │  (× tier)    │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Check Tier  │◀────│  Update    │
                   │  Progression │     │  Balance   │
                   └──────────────┘     └────────────┘
```

### NPS Survey Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Send    │────▶│  Customer    │────▶│  Record      │
│  Survey  │     │  Responds    │     │  Score       │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Update      │◀────│  Categorize│
                   │  NPS Score   │     │  (D/P/Pr)  │
                   └──────────────┘     └────────────┘
```

### Health Score Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Collect │────▶│  Weighted    │────▶│  Composite   │
│  Metrics │     │  Normalize   │     │  Score       │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Generate    │◀────│  Compare   │
                   │  Alerts      │     │  Threshold │
                   └──────────────┘     └────────────┘
```

### Renewal Pipeline Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Contract│────▶│  Create      │────▶│  Initiate    │
│  Expires │     │  Renewal     │     │  Outreach    │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
              ┌──────────────┐          ┌────▼───────┐
              │  Track       │◀─────────│  Negotiate │
              │  Outcome     │          │  & Close   │
              └──────────────┘          └────────────┘
```

### Sentiment Analysis Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Receive │────▶│  Tokenize &  │────▶│  Score       │
│  Text    │     │  Match KWs   │     │  Sentiment   │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Store       │◀────│  Classify  │
                   │  Entry       │     │  Level     │
                   └──────────────┘     └────────────┘
```

### Escalation Flow

```
┌──────────┐     ┌──────────────┐     ┌──────────────┐
│  Event   │────▶│  Match       │────▶│  Create      │
│  Trigger │     │  Rule        │     │  Escalation  │
└──────────┘     └──────────────┘     └──────┬───────┘
                                             │
                   ┌──────────────┐     ┌────▼───────┐
                   │  Resolve     │◀────│  Assign &  │
                   │  & Close     │     │  Track     │
                   └──────────────┘     └────────────┘
```

## Design Patterns

### 1. Strategy Pattern
Retention strategies implement different approaches (discount, outreach, survey) triggered by churn risk levels. Each strategy is a pluggable template with defined triggers.

### 2. Observer Pattern
Signal tracking notifies the churn predictor of behavioral changes across all channels. Health monitoring observes multiple data streams.

### 3. State Machine
Customer status, loyalty tiers, renewal states, and escalation statuses follow state machine transitions with defined rules.

### 4. Registry Pattern
All entities (customers, surveys, campaigns, rewards, contracts, renewals, escalations) use dictionary-based registries for O(1) lookup.

### 5. Template Method
Strategy execution follows: evaluate risk → select strategy → execute → track outcome. Churn reason analysis follows: collect evidence → classify → score confidence.

### 6. Composite Pattern
Health scores compose multiple dimensions (engagement, satisfaction, financial, support, contract) into a single weighted score.

### 7. Chain of Responsibility
Escalation engine routes events through configurable rules to determine severity and auto-assignment.

## Thread Safety

All managers use `threading.Lock()` to protect shared state:

```
┌─────────────────────────────────────────┐
│           Thread Safety Model            │
│                                          │
│  Manager          │ Lock Scope          │
│  ─────────────────┼──────────────────── │
│  ChurnPredictor   │ customers, history, │
│                   │ predictions         │
│  LoyaltyManager   │ balances, tiers,    │
│                   │ transactions        │
│  NPSManager       │ surveys, responses  │
│  CohortAnalyzer   │ cohorts, retention  │
│  StrategyEngine   │ strategies          │
│  WinbackManager   │ campaigns, enroll.  │
│  HealthMonitor    │ scores, history     │
│  RenewalManager   │ renewals            │
│  ContractTracker  │ contracts           │
│  SentimentAnalyzer│ entries, scores     │
│  EscalationEngine │ escalations         │
│  ChurnReasonAnalyzer│ entries, counts  │
│  Dashboard        │ alerts, snapshots   │
│  CustomerRetentionAgent │ customers     │
└─────────────────────────────────────────┘

Pattern:
    with self._lock:
        # read or mutate shared state
```

**Lock Granularity:**
- Each manager owns a single lock
- Lock is acquired for both reads and writes
- No lock nesting (no deadlock risk)
- Lock scope is minimal (fast release)

## Performance Targets

| Operation                | Target   | Current |
|--------------------------|----------|---------|
| Churn Prediction         | < 100ms  | ~25ms   |
| Points Add               | < 50ms   | ~10ms   |
| NPS Calculation          | < 200ms  | ~50ms   |
| Cohort Analysis          | < 500ms  | ~150ms  |
| Strategy Recommend       | < 100ms  | ~30ms   |
| Health Score Calc        | < 50ms   | ~15ms   |
| Renewal Lookup           | < 50ms   | ~10ms   |
| Contract Expiry Scan     | < 100ms  | ~30ms   |
| Sentiment Analysis       | < 100ms  | ~20ms   |
| Escalation Creation      | < 50ms   | ~10ms   |
| Churn Reason Analysis    | < 100ms  | ~25ms   |
| Dashboard Snapshot       | < 200ms  | ~60ms   |

**Optimization Strategies:**
- In-memory data structures (no I/O in hot path)
- Thread-safe but minimal lock contention
- Deque-based history with maxlen limits
- Dictionary-based O(1) lookups
- Lazy computation where possible

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

escalation_rules:
  high_churn_risk: { severity: 4, auto_assign: true }
  negative_sentiment: { severity: 3, auto_assign: false }
  payment_default: { severity: 5, auto_assign: true }
  support_escalation: { severity: 3, auto_assign: true }
  competitor_threat: { severity: 4, auto_assign: false }
  contract_expiry: { severity: 2, auto_assign: true }
  usage_decline: { severity: 3, auto_assign: false }
  executive_sponsor_lost: { severity: 5, auto_assign: true }

sentiment_keywords:
  positive: [great, excellent, love, amazing, fantastic, wonderful,
             happy, satisfied, impressed, recommend, best, perfect]
  negative: [bad, terrible, awful, hate, frustrated, disappointed,
             poor, worst, broken, useless, angry, unacceptable]
```

## Error Handling

The agent defines a hierarchy of exceptions:

```
RetentionError (base)
├── ChurnPredictionError
├── LoyaltyError
├── SurveyError
├── ContractError
├── RenewalError
└── EscalationError
```

All managers handle edge cases gracefully and return structured error dictionaries rather than raising exceptions for expected failure modes (e.g., insufficient points, unknown customer).

**Error Response Pattern:**
```python
# Expected errors return dicts
{"error": "Insufficient points or invalid reward"}

# Unexpected errors raise exceptions
raise RetentionError("Unexpected condition")
```

## Logging

```python
logger = logging.getLogger("customer_retention_agent")

# Key log points:
# - Agent initialization and shutdown (INFO)
# - Loyalty point additions and redemptions (INFO)
# - Tier upgrades (INFO)
# - Escalation creation (WARNING)
# - Strategy execution (INFO)
# - Renewal creation (INFO)
```

**Log Level Guidelines:**
- INFO: normal operations (points added, strategies executed)
- WARNING: situations needing attention (escalations, low health)
- ERROR: unexpected failures (should not occur in normal operation)

## Extending the Agent

To add a new subsystem:

1. Create a data class for any new entities
2. Create a manager class with `_lock = threading.Lock()`
3. Add corresponding methods to `CustomerRetentionAgent`
4. Wire into `initialize()` and `get_full_report()`
5. Add to `AsyncCustomerRetentionAgent` if async access needed
6. Add configuration options to `Config` class
7. Add constants if needed (thresholds, weights, mappings)
8. Update ARCHITECTURE.md with new component documentation
9. Update GROK.md with new capabilities and method signatures
10. Update README.md with usage examples

**Extension Checklist:**
- [ ] Data class defined
- [ ] Manager class with thread lock
- [ ] Orchestrator methods added
- [ ] Async wrapper methods added
- [ ] Configuration options added
- [ ] Constants defined
- [ ] Error handling consistent
- [ ] Logging added at key points
- [ ] Documentation updated
- [ ] Demo updated in main()

## API Response Format

All public methods on `CustomerRetentionAgent` return `Dict[str, Any]`. This consistent format enables easy integration with REST APIs, message queues, and event systems.

```
Success: {"customer_id": "cust_001", "risk_level": "HIGH", "risk_score": 0.65}
Error:   {"error": "Insufficient points or invalid reward"}
```

## Data Storage Model

The agent uses in-memory storage exclusively. All data lives in Python dictionaries protected by thread locks. This provides:

- Zero external dependencies
- Sub-millisecond access times
- Full data isolation per agent instance
- Easy serialization for persistence if needed

For production deployment, consider adding a persistence layer that snapshots state to disk or a database at configurable intervals.

## Scalability Considerations

```
┌─────────────────────────────────────────────────────────┐
│                Scalability Model                         │
│                                                          │
│  Single Instance:                                       │
│  - Suitable for < 10,000 customers                      │
│  - All operations in-memory                             │
│  - Thread-safe for concurrent access                    │
│                                                          │
│  Multi-Instance:                                        │
│  - Shard by customer_id hash                            │
│  - Each instance handles a subset                       │
│  - Aggregate results at orchestrator level              │
│                                                          │
│  With Persistence:                                      │
│  - Add database backend for durability                  │
│  - Cache hot paths in memory                            │
│  - Event sourcing for audit trail                       │
│                                                          │
│  Performance Characteristics:                           │
│  - O(1) lookups for all entity types                    │
│  - O(n) for batch operations (predict_all, etc.)        │
│  - Thread contention minimal (per-manager locks)        │
│  - Memory usage scales linearly with customer count     │
└─────────────────────────────────────────────────────────┘
```

## Integration Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  External    │────▶│  Customer    │────▶│  Retention   │
│  Systems     │     │  Retention   │     │  Outputs     │
│              │     │  Agent       │     │              │
│  - CRM       │     │              │     │  - Alerts    │
│  - Support   │     │  Subsystems: │     │  - Reports   │
│  - Email     │     │  - Churn     │     │  - Actions   │
│  - Analytics │     │  - Loyalty   │     │  - Scores    │
│              │     │  - NPS       │     │              │
│              │     │  - Health    │     │              │
│              │     │  - Renewal   │     │              │
│              │     │  - Contract  │     │              │
│              │     │  - Sentiment │     │              │
│              │     │  - Escalation│     │              │
│              │     │  - ChurnWhy  │     │              │
│              │     │  - Strategy  │     │              │
│              │     │  - Winback   │     │              │
│              │     │  - Cohort    │     │              │
│              │     │  - Dashboard │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
```

## Memory Model

All data structures are in-memory Python objects. The memory footprint scales linearly with:

- Number of customers (Customer objects)
- Signal history length (deque with maxlen=100 per customer)
- Loyalty transactions (list per customer)
- NPS responses (global list)
- Strategy execution records (global dict)
- Escalation records (global dict)
- Sentiment entries (global list)
- Churn reason entries (global list)

Estimated memory per customer: ~2KB (including history buffers)

## Concurrency Model

```
Thread A                    Thread B
─────────                   ─────────
acquire ChurnPredictor._lock
  read customers
  compute prediction
release _lock
                            acquire LoyaltyManager._lock
                              add points
                              update tier
                            release _lock
acquire LoyaltyManager._lock
  read balance
release _lock
```

No cross-manager lock ordering exists, so deadlocks are impossible. Each manager's lock is independent.

## Data Retention Policy

Since the agent is in-memory only, data lifetime matches the process lifetime. For durable storage:

1. **Snapshot periodically**: Serialize state to disk/database at configurable intervals
2. **Event sourcing**: Log all mutations for replay and audit
3. **Export on shutdown**: Dump state before process termination

## Monitoring Recommendations

| Metric | Alert Threshold | Action |
|--------|----------------|--------|
| Churn prediction latency | > 100ms | Investigate signal history size |
| Memory usage | > 1GB | Consider pagination/archival |
| Open escalations | > 50 | Review escalation resolution process |
| Critical churn predictions | > 10% of customers | Review intervention pipeline |
| NPS response rate | < 20% | Review survey timing/channels |
| Health score distribution | > 50% critical | Systemic issue investigation |

## Component Interaction Matrix

| Component | Reads From | Writes To |
|-----------|-----------|-----------|
| ChurnPredictor | Customer, Signal History | Prediction, Customer.churn_risk |
| LoyaltyManager | Customer, Rewards | Balance, Tier, Transactions |
| NPSManager | Survey | Response, NPS Score |
| CohortAnalyzer | Customer | Cohort, Retention Data |
| RetentionStrategyEngine | ChurnPredictor | Strategy Records |
| WinbackManager | Campaign | Enrollment |
| CustomerHealthMonitor | Multiple | Health Score |
| RenewalManager | Contract | Renewal Record |
| ContractTracker | Customer | Contract |
| SentimentAnalyzer | Text Input | Sentiment Entry |
| EscalationEngine | Rules | Escalation Record |
| ChurnReasonAnalyzer | Evidence | Reason Entry |
| RetentionDashboard | All | Alerts, Snapshots |
```

# Monitoring Agent Architecture

## Overview

The Monitoring Agent provides comprehensive infrastructure observability covering metrics collection, alerting, uptime monitoring, log aggregation, dashboard visualization, incident management, and SLO tracking. The architecture follows a modular design where each subsystem operates independently with clean APIs, while the top-level orchestrator coordinates cross-module workflows.

---

## System Context

```
┌──────────────────────────────────────────────────────────────────┐
│                       Infrastructure                             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │  Apps    │ │ Servers  │ │Network   │ │Database  │           │
│  │          │ │          │ │          │ │          │           │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘           │
│       │            │            │            │                    │
│  ┌────▼────────────▼────────────▼────────────▼─────┐            │
│  │              Data Collection Layer               │            │
│  └──────────────────┬──────────────────────────────┘            │
│                     │                                            │
│  ┌──────────────────▼──────────────────────────────┐            │
│  │            Monitoring Agent Core                  │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │            │
│  │  │Prometheus│ │  Alert   │ │ Uptime   │        │            │
│  │  │ Metrics  │ │ Manager  │ │ Monitor  │        │            │
│  │  └──────────┘ └──────────┘ └──────────┘        │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │            │
│  │  │   Log    │ │Dashboard │ │ Incident │        │            │
│  │  │ Monitor  │ │Generator │ │ Manager  │        │            │
│  │  └──────────┘ └──────────┘ └──────────┘        │            │
│  │  ┌──────────┐                                   │            │
│  │  │   SLO    │                                   │            │
│  │  │ Manager  │                                   │            │
│  │  └──────────┘                                   │            │
│  └─────────────────────────────────────────────────┘            │
│                     │                                            │
│  ┌──────────────────▼──────────────────────────────┐            │
│  │              Notification Layer                   │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │            │
│  │  │  Pager   │ │  Slack   │ │  Email   │        │            │
│  │  └──────────┘ └──────────┘ └──────────┘        │            │
│  └─────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Prometheus Metrics Collector

**Purpose**: Collect, store, and expose time-series metrics in Prometheus format.

```
┌─────────────────────────────────────────────┐
│          Prometheus Metrics                  │
├─────────────────────────────────────────────┤
│ Metric Types:                               │
│ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│ │ COUNTER  │ │  GAUGE   │ │ HISTOGRAM│     │
│ │ monoton- │ │ can go   │ │ distrib- │     │
│ │ ically   │ │ up/down  │ │ ution    │     │
│ │ increasing│ │         │ │ tracking │     │
│ └──────────┘ └──────────┘ └──────────┘     │
│                                             │
│ Operations:                                 │
│ define_* → inc/set/observe → scrape         │
└─────────────────────────────────────────────┘
```

**Scrape Format**:
```
http_requests_total{method="GET",status="200"} 1523
active_connections 42
http_request_duration_seconds_count 1523
http_request_duration_seconds_sum 380.75
```

---

### 2. Alert Manager

**Purpose**: Define alert rules, fire alerts, and manage notification routing.

```
┌──────────────────────────────────────────────────────┐
│                   Alert Manager                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Rule Evaluation:                                    │
│  expression → threshold check → fire/resolve         │
│                                                      │
│  Alert Lifecycle:                                    │
│  FIRING → ACKNOWLEDGED → RESOLVED                    │
│    └→ SILENCED                                       │
│                                                      │
│  Notification Routing:                               │
│  ┌──────────┬──────────────┬──────────┐             │
│  │ CRITICAL │ pager+slack  │ email    │             │
│  │ HIGH     │ slack+email  │          │             │
│  │ MEDIUM   │ slack        │          │             │
│  │ LOW      │ email        │          │             │
│  │ INFO     │ (none)       │          │             │
│  └──────────┴──────────────┴──────────┘             │
└──────────────────────────────────────────────────────┘
```

---

### 3. Uptime Monitor

**Purpose**: Track endpoint availability and response times.

```
┌─────────────────────────────────────────┐
│            Uptime Monitor               │
├─────────────────────────────────────────┤
│  Check Configuration:                   │
│  url + method + expected_status +       │
│  timeout + interval                     │
│                                         │
│  Check Results:                         │
│  status_code + response_time + success  │
│                                         │
│  Uptime Calculation:                    │
│  uptime% = successful / total * 100    │
│                                         │
│  History Tracking:                      │
│  Per-check result history with TTL      │
└─────────────────────────────────────────┘
```

---

### 4. Log Monitor

**Purpose**: Ingest, search, and analyze application logs.

```
┌──────────────────────────────────────────────────────┐
│                   Log Monitor                        │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Log Entry Structure:                                │
│  timestamp + level + source + message + fields       │
│                                                      │
│  Pattern Matching:                                   │
│  regex patterns → match_count → severity mapping     │
│                                                      │
│  Search Capabilities:                                │
│  query + level filter + source filter + time range   │
│                                                      │
│  Aggregation:                                        │
│  error_summary, log_volume, by_level, by_source      │
└──────────────────────────────────────────────────────┘
```

---

### 5. Dashboard Generator

**Purpose**: Create visual monitoring dashboards.

```
┌──────────────────────────────────────────────────────┐
│              Dashboard Generator                     │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Panel Types:                                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │  GRAPH   │ │SINGLESTAT│ │  TABLE   │            │
│  └──────────┘ └──────────┘ └──────────┘            │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │  HEATMAP │ │   BAR    │ │   PIE    │            │
│  └──────────┘ └──────────┘ └──────────┘            │
│                                                      │
│  Dashboard Structure:                                │
│  title + refresh_interval + panels[]                 │
│                                                      │
│  Export Format: JSON (Grafana-compatible)            │
└──────────────────────────────────────────────────────┘
```

---

### 6. Incident Manager

**Purpose**: Create, track, and resolve production incidents.

```
┌──────────────────────────────────────────────────────┐
│               Incident Manager                       │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Severity Levels:                                    │
│  SEV1 → Critical business impact                     │
│  SEV2 → Major feature degraded                       │
│  SEV3 → Minor issue                                  │
│  SEV4 → Cosmetic/low-impact                          │
│                                                      │
│  Incident Lifecycle:                                 │
│  OPEN → INVESTIGATING → IDENTIFIED → MONITORING      │
│                                                 ↓    │
│                                              RESOLVED │
│                                                      │
│  MTTR = resolved_at - created_at                     │
│                                                      │
│  Timeline: Every status change logged                │
└──────────────────────────────────────────────────────┘
```

---

### 7. SLO Manager

**Purpose**: Track Service Level Objectives and error budgets.

```
┌──────────────────────────────────────────────────────┐
│                 SLO Manager                          │
├──────────────────────────────────────────────────────┤
│                                                      │
│  SLO Definition:                                     │
│  service + metric + target% + window_days            │
│                                                      │
│  Error Budget:                                       │
│  budget = 100% - target%                             │
│  remaining = budget - consumed                       │
│                                                      │
│  Burn Rate:                                          │
│  burn_rate = consumed_rate / window_days             │
│                                                      │
│  Example:                                            │
│  target=99.9%, current=99.95%                        │
│  → error_budget_remaining = 100%                     │
│  → burn_rate = 0 (not consuming budget)              │
└──────────────────────────────────────────────────────┘
```

---

## Data Flow: Incident Response

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Metric  │───→│   Alert  │───→│Incident  │───→│  Resolve │
│ Threshold│    │   Fires  │    │ Created  │    │  & Close │
└──────────┘    └─────┬────┘    └──────────┘    └──────────┘
                      │
                ┌─────▼────┐
                │Notification│
                │  Routing   │
                └───────────┘
```

---

## Design Patterns

| Pattern | Where | Purpose |
|---------|-------|---------|
| Repository | Metrics/Alerts/Logs | Data access abstraction |
| Observer | Alert firing | Event-driven notifications |
| Strategy | Notification routing | Pluggable channel selection |
| Facade | MonitoringAgent | Unified interface |
| State Machine | Alert/Incident lifecycle | Validated transitions |
| Composite | Dashboard panels | Panel composition |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Data Classes | dataclasses, typing |
| Enums | enum.Enum |
| Regex | re (log patterns) |
| Math | math (statistics) |
| Logging | logging module |
| ID Generation | uuid |
| Date/Time | datetime, timedelta |

---

## Scalability

| Dimension | Approach |
|-----------|---------|
| Metric Volume | In-memory store with configurable TTL |
| Alert Rules | Rule evaluation on schedule |
| Log Ingestion | Async buffering with batch processing |
| Dashboard Queries | Cached aggregation |
| Incident History | Append-only with compaction |

---

## Security

| Concern | Approach |
|---------|----------|
| Alert Channels | Authenticated notification endpoints |
| Dashboard Access | Role-based access control |
| Log Data | PII redaction before storage |
| Incident Data | Audit trail for all changes |
| SLO Data | Internal service metrics only |

---

## Error Handling

```
MonitoringError (base)
├── AlertRuleNotFoundError
├── DashboardNotFoundError
└── IncidentNotFoundError
```

All public methods validate inputs. Alert firing is isolated from rule evaluation. Log ingestion continues on pattern match failures.

# Marketing Agent Architecture

## Overview

The Marketing Agent is a modular orchestration system that manages the full marketing lifecycle: audience segmentation, campaign execution, budget allocation, multi-touch attribution, content generation, analytics tracking, and SEO analysis. The design follows a plugin-based architecture where each subsystem operates independently yet shares data through well-defined interfaces.

---

## System Context

```
┌──────────────────────────────────────────────────────────────────┐
│                        External Systems                          │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐           │
│  │   CRM    │ │   ESP    │ │   DMP    │ │  Ads API │           │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘           │
│       │            │            │            │                    │
│  ┌────▼────────────▼────────────▼────────────▼─────┐            │
│  │              Integration Layer                   │            │
│  └──────────────────┬──────────────────────────────┘            │
│                     │                                            │
│  ┌──────────────────▼──────────────────────────────┐            │
│  │            Marketing Agent Core                  │            │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐           │            │
│  │  │Audience │ │Campaign │ │ Budget  │           │            │
│  │  │ Manager │ │ Manager │ │Allocator│           │            │
│  │  └─────────┘ └─────────┘ └─────────┘           │            │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐           │            │
│  │  │Attrib.  │ │Content  │ │Analytics│           │            │
│  │  │ Engine  │ │Generatr │ │Dashboard│           │            │
│  │  └─────────┘ └─────────┘ └─────────┘           │            │
│  │  ┌─────────┐                                    │            │
│  │  │  SEO    │                                    │            │
│  │  │Analyzer │                                    │            │
│  │  └─────────┘                                    │            │
│  └─────────────────────────────────────────────────┘            │
│                     │                                            │
│  ┌──────────────────▼──────────────────────────────┐            │
│  │              Data Layer                          │            │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐        │            │
│  │  │Events DB │ │Segment   │ │Campaign  │        │            │
│  │  │          │ │Store     │ │Store     │        │            │
│  │  └──────────┘ └──────────┘ └──────────┘        │            │
│  └─────────────────────────────────────────────────┘            │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. Audience Manager

**Purpose**: Define, combine, score, and manage customer audience segments.

```
┌────────────────────────────────────┐
│         Audience Manager           │
├────────────────────────────────────┤
│ create_segment()                   │
│ get_segment() / update_segment()   │
│ combine_segments(intersect/union)  │
│ score_segment()                    │
│ list_segments()                    │
├────────────────────────────────────┤
│ Internal State:                    │
│   _segments: Dict[id, Segment]     │
│   _combinations: Dict[id, List]    │
└────────────────────────────────────┘
```

**Data Flow**:
```
User Input → Criteria Validation → Segment Creation → Size Estimation → Store
Combine Request → Resolve Source Segments → Apply Operation → New Segment
```

**Design Patterns**:
- **Value Object**: `AudienceSegment` is immutable after creation except via explicit update
- **Specification Pattern**: Criteria evaluate membership rules
- **Composite Pattern**: Segments combine via intersect/union/exclude operations

---

### 2. Campaign Manager

**Purpose**: Full campaign lifecycle from draft through completion with event hooks.

```
┌────────────────────────────────────────────────────────┐
│                   Campaign Manager                     │
├────────────────────────────────────────────────────────┤
│  State Machine:                                        │
│                                                        │
│  DRAFT ──→ SCHEDULED ──→ ACTIVE ──→ COMPLETED          │
│    │          │            │              │             │
│    │          │         PAUSED ──→ ACTIVE│             │
│    │          │                          │             │
│    └────→ ARCHIVED ←─────────────────────┘             │
│                                                        │
│  Hooks: on_launch, on_pause, on_complete               │
└────────────────────────────────────────────────────────┘
```

**State Transitions**:
```
launch:  DRAFT/SCHEDULED → ACTIVE
pause:   ACTIVE → PAUSED
resume:  PAUSED → ACTIVE
complete: ACTIVE → COMPLETED
```

**Design Patterns**:
- **State Machine**: Campaign lifecycle with validated transitions
- **Observer Pattern**: Hook system for launch/pause/complete events
- **Repository Pattern**: In-memory store with query capabilities

---

### 3. Budget Allocator

**Purpose**: Distribute marketing spend across channels based on strategy and performance.

```
┌────────────────────────────────────────────────────────┐
│                  Budget Allocator                      │
├────────────────────────────────────────────────────────┤
│                                                        │
│  Strategies:                                           │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐              │
│  │  Equal   │ │Performance│ │ Seasonal │              │
│  │  Split   │ │  Based   │ │ Adjust   │              │
│  └──────────┘ └──────────┘ └──────────┘              │
│                                                        │
│  Data Flow:                                            │
│  Channel ROI History → Strategy Selection →            │
│  Weight Calculation → Allocation Output →              │
│  Reallocation Recommendation                           │
└────────────────────────────────────────────────────────┘
```

**Allocation Algorithms**:
```
Equal Split:
  per_channel = total / channels

Performance Based:
  weight_ch = max(0, roi_ch) / sum(max(0, roi_all))
  alloc_ch = total * weight_ch

Seasonal Adjust:
  base_alloc * seasonal_index[month]
```

---

### 4. Attribution Engine

**Purpose**: Calculate channel contribution using industry-standard attribution models.

```
Touchpoint Timeline:
  [Email] ──→ [Search] ──→ [Social] ──→ [Email] → Conversion

Models:
  First Touch:  Email = 100%
  Last Touch:   Email = 100% (second)
  Linear:       Email = 50%, Search = 25%, Social = 25%
  Time Decay:   Recent channels weighted higher
  Position:     First = 40%, Last = 40%, Middle = 20%
```

**Confidence Calculation**:
```
confidence = min(1.0, unique_channels / total_touchpoints)
```

**Data Flow**:
```
User Journey → Touchpoint Collection → Model Selection →
Weight Calculation → Channel Scores → Aggregated Attribution
```

---

### 5. Content Generator

**Purpose**: Create marketing content using templates and brand voice configuration.

```
┌────────────────────────────────────┐
│        Content Generator           │
├────────────────────────────────────┤
│ Templates: {id: template_string}   │
│ Brand Voice: tone + keywords       │
│                                    │
│ Render Pipeline:                   │
│ Template → Variable Substitution   │
│ → Platform Adaptation → Output     │
└────────────────────────────────────┘
```

**Platform Limits**:
```
Twitter:   280 chars
LinkedIn:  3000 chars
Instagram: 2200 chars
```

---

### 6. Analytics Dashboard

**Purpose**: Track events, manage goals, and generate performance reports.

```
Event Stream → Aggregation → Report Generation
                ↓
Goal Tracking → Progress Calculation → Status Dashboard
```

**Funnel Analysis**:
```
Awareness → Consideration → Conversion → Retention → Advocacy
    100%        45%           12%          8%          3%
```

---

### 7. SEO Analyzer

**Purpose**: Evaluate content for search engine optimization quality.

```
Content Input → Keyword Analysis → Density Calculation →
Serp Preview → Content Score → Recommendations
```

---

## Data Flow: Campaign Lifecycle

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ Define   │───→│ Allocate │───→│ Launch   │───→│ Monitor  │
│ Audience │    │ Budget   │    │ Campaign │    │ Metrics  │
└──────────┘    └──────────┘    └──────────┘    └─────┬────┘
                                                       │
┌──────────┐    ┌──────────┐    ┌──────────┐          │
│ Optimize │←───│ Report   │←───│Attribute │←─────────┘
│ Future   │    │ Results  │    │ Credit   │
└──────────┘    └──────────┘    └──────────┘
```

---

## Design Patterns Used

| Pattern | Where | Purpose |
|---------|-------|---------|
| State Machine | Campaign Manager | Lifecycle transitions |
| Observer | Campaign hooks | Event notification |
| Strategy | Budget Allocator | Pluggable allocation algorithms |
| Repository | Audience/Campaign stores | Data access abstraction |
| Value Object | Data classes | Immutable data transfer |
| Facade | MarketingAgent | Unified interface to subsystems |
| Template Method | Content Generator | Reusable content creation |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Data Classes | dataclasses, typing |
| Enums | enum.Enum |
| Logging | logging module |
| ID Generation | uuid |
| Date/Time | datetime, timedelta |

---

## Security Considerations

| Concern | Mitigation |
|---------|-----------|
| API Key Storage | Environment variables, never hardcoded |
| PII Handling | Segmentation criteria use anonymized IDs |
| Budget Data | Access-controlled, audit-logged |
| Campaign Content | Input validation on templates |
| Attribution Data | User IDs not exposed in reports |
| Hook Callbacks | Exception isolation in hook execution |

---

## Scalability

| Dimension | Approach |
|-----------|---------|
| Campaign Volume | In-memory stores with configurable TTL |
| Touchpoint Volume | Batch processing for attribution |
| Segment Computation | Lazy evaluation, cached scores |
| Report Generation | Incremental aggregation |
| Content Rendering | Template caching |

---

## Error Handling

```
MarketingError (base)
├── CampaignNotFoundError
├── InvalidBudgetError
├── SegmentNotFoundError
└── ValueError (template not found)
```

All public methods validate inputs before state mutation. Hooks are wrapped in try/except to prevent callback failures from affecting the main flow.

---

## Testing Strategy

| Component | Approach |
|-----------|---------|
| Audience Manager | Unit tests for combine operations |
| Campaign Manager | State transition matrix coverage |
| Budget Allocator | Strategy correctness verification |
| Attribution Engine | Known-journey test cases |
| Content Generator | Template rendering edge cases |
| Analytics Dashboard | Event aggregation accuracy |
| SEO Analyzer | Density calculation validation |

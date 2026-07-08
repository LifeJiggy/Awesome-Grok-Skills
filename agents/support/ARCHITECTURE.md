# Support Agent Architecture

## 1. Overview

The Support Agent implements a modular customer support operations platform. It orchestrates five core subsystems—ticket management, knowledge base, response engine, escalation management, and customer management—behind a unified `SupportAgent` facade.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                         SupportAgent (Facade)                                    │
├──────────────┬──────────────┬──────────────┬──────────────┬──────────────────────┤
│   Ticket     │  Knowledge   │  Response    │ Escalation   │    Customer          │
│   Manager    │   Base       │   Engine     │  Manager     │    Manager           │
├──────────────┼──────────────┼──────────────┼──────────────┼──────────────────────┤
│ CRUD Ops     │ Article CRUD │ Auto-Reply   │ Rules Engine │ Profile CRUD         │
│ SLA Check    │ Search Index │ Templates    │ L1→L2→L3     │ Tier Management      │
│ Status Flow  │ Vote System  │ KB Match     │ History      │ Satisfaction         │
│ History      │ Category     │ Escalation   │ Acknowledge  │ Lifetime Value       │
│ Overdue      │ Views        │ Manual       │              │ History              │
├──────────────┴──────────────┴──────────────┴──────────────┴──────────────────────┤
│                          SupportAnalytics                                        │
├──────────────────────────────────────────────────────────────────────────────────┤
│ Metrics │ Reports │ Recommendations │ SLA Compliance │ Satisfaction Tracking    │
└──────────────────────────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Shared Models    │
                    │ Ticket             │
                    │ Customer           │
                    │ KnowledgeArticle   │
                    │ SLAPolicy          │
                    │ Escalation         │
                    │ CSATSurvey         │
                    └───────────────────┘
```

## 2. Component Descriptions

### 2.1 TicketManager

Full ticket lifecycle management with SLA tracking.

```
┌───────────────────────────────────────────────┐
│            TicketManager                      │
├───────────────────────────────────────────────┤
│  Ticket Store (Dict[str, Ticket])             │
│  Event History (List[Dict])                   │
│  SLA Policies (Dict[str, SLAPolicy])          │
│                                               │
│  Lifecycle:                                   │
│  ┌──────┐ ┌──────────┐ ┌─────────┐          │
│  │ OPEN ├►│IN_PROGRESS├►│ WAITING │          │
│  └──┬───┘ └────┬─────┘ └────┬────┘          │
│     │          │            │                 │
│     │    ┌─────▼─────┐ ┌───▼──────┐         │
│     │    │ESCALATED   │ │RESOLVED  │         │
│     │    └───────────┘ └────┬─────┘         │
│     │                       │                │
│     │                  ┌────▼────┐           │
│     │                  │ CLOSED  │           │
│     │                  └─────────┘           │
│     │                                        │
│     └──────────────────────────────────────  │
│              (reopen cycle)                  │
└───────────────────────────────────────────────┘
```

**Ticket lifecycle:**
```
OPEN → IN_PROGRESS → WAITING_ON_CUSTOMER/WAITING_ON_INTERNAL → RESOLVED → CLOSED
  ↑         ↓                                                      │
  └─────── REOPENED ←───────────────────────────────────────────────┘
```

### 2.2 KnowledgeBase

Searchable knowledge repository with article scoring.

```
┌───────────────────────────────────────────────┐
│           KnowledgeBase                       │
├───────────────────────────────────────────────┤
│  Article Store (Dict[str, KnowledgeArticle])  │
│  Search Index (Dict[word, List[article_id]])  │
│                                               │
│  ┌──────────────┐  ┌──────────────────┐      │
│  │add_article    │  │search            │      │
│  │update         │  │record_view       │      │
│  │delete         │  │vote_helpful      │      │
│  └──────────────┘  └──────────────────┘      │
│                                               │
│  Ranking: views + helpful_ratio + match_score │
└───────────────────────────────────────────────┘
```

### 2.3 ResponseEngine

Generates automated, templated, and KB-matched responses.

```
┌───────────────────────────────────────────────┐
│           ResponseEngine                      │
├───────────────────────────────────────────────┤
│  Templates (Dict[str, Dict])                  │
│  Knowledge Base Reference                     │
│  Response History (List[Dict])                │
│                                               │
│  Response Types:                              │
│  ┌───────────┬──────────┬───────────────┐    │
│  │AUTOMATED  │TEMPLATED │KNOWLEDGE_BASE │    │
│  │(auto-ack) │(variable)│(article match)│    │
│  └───────────┴──────────┴───────────────┘    │
│  ┌───────────┬──────────┐                     │
│  │ESCALATED  │ MANUAL   │                     │
│  └───────────┴──────────┘                     │
└───────────────────────────────────────────────┘
```

### 2.4 EscalationManager

Rules-based escalation with level tracking.

```
┌───────────────────────────────────────────────┐
│          EscalationManager                    │
├───────────────────────────────────────────────┤
│  Escalation Records (List[Escalation])        │
│  Escalation Rules (List[Dict])                │
│                                               │
│  Levels:                                      │
│  ┌─────┐    ┌─────┐    ┌─────┐    ┌──────┐  │
│  │ L1  ├───►│ L2  ├───►│ L3  ├───►│ MGMT │  │
│  └─────┘    └─────┘    └─────┘    └──────┘  │
│                                               │
│  Rules Engine:                                │
│  "priority == CRITICAL → escalate to L3"      │
│  "hours_open > 24 AND status == OPEN → L2"   │
│  "tier == ENTERPRISE → L2 immediate"          │
└───────────────────────────────────────────────┘
```

### 2.5 CustomerManager

Customer profile management and satisfaction tracking.

```
┌───────────────────────────────────────────────┐
│          CustomerManager                      │
├───────────────────────────────────────────────┤
│  Customer Store (Dict[str, Customer])         │
│  Interaction History (List[Dict])             │
│                                               │
│  Tiers:                                       │
│  ┌──────┬────────┬─────────────┬──────────┐  │
│  │ FREE │STARTER │PROFESSIONAL │ENTERPRISE│  │
│  └──────┴────────┴─────────────┴──────────┘  │
│                                               │
│  Fields: name, email, company, tier,          │
│          satisfaction_score, lifetime_value    │
└───────────────────────────────────────────────┘
```

### 2.6 SupportAnalytics

Metrics calculation and report generation.

```
┌───────────────────────────────────────────────┐
│          SupportAnalytics                     │
├───────────────────────────────────────────────┤
│  References: TicketManager, CustomerManager   │
│                                               │
│  Metrics:                                     │
│  ┌───────────────┬─────────────────────┐      │
│  │ Open Tickets  │ Avg Response Time   │      │
│  │ Avg Resolution│ Satisfaction Score  │      │
│  │ FCR Rate      │ SLA Compliance      │      │
│  └───────────────┴─────────────────────┘      │
│                                               │
│  Reports: Summary, Alerts, Recommendations    │
└───────────────────────────────────────────────┘
```

## 3. Data Flow

```
Customer Request (Email/Chat/Phone/API)
        │
        ▼
┌───────────────────┐
│   TicketManager   │──── Create Ticket ──── SLA Check
│                   │                       │
└───────────────────┘                       ▼
                                      SLA Policy
        │
        ▼
┌───────────────────┐
│  ResponseEngine   │──── Auto-Response ──── Customer
│                   │                       │
│  (KB Search)      │──── KB Match ─────────┘
└───────────────────┘
        │
        ▼ (if needed)
┌───────────────────┐
│ EscalationManager │──── L1 → L2 → L3 ──── Specialist
└───────────────────┘
        │
        ▼
┌───────────────────┐
│   Resolution      │──── CSAT Survey ────── Customer
└───────────────────┘
        │
        ▼
┌───────────────────┐
│ SupportAnalytics  │──── Dashboard ──────── Manager
└───────────────────┘
```

## 4. Design Patterns

| Pattern | Application |
|---------|-------------|
| **Facade** | `SupportAgent` unifies five subsystems |
| **Template Method** | Response templates with variable substitution |
| **Chain of Responsibility** | Escalation rules evaluated in sequence |
| **Strategy** | Different response strategies per ticket type |
| **Observer** | SLA checks trigger alerts on breach |
| **Repository** | Knowledge base article storage and search |

## 5. Data Models

### Entity Relationships

```
Customer 1──* Ticket
Ticket 1──* Message
Ticket 1──* Escalation
Ticket 1──0..1 CSATSurvey
KnowledgeArticle ──* View
SLAPolicy 1──* Ticket (via priority+tier)
```

### Ticket Status State Machine

```
       ┌────────────────────────────────────────┐
       │                                        │
       ▼                                        │
     OPEN ──► IN_PROGRESS ──► RESOLVED ──► CLOSED
       │          │               ▲
       │          ▼               │
       │    WAITING_ON_*          │
       │          │               │
       │          ▼               │
       │     ESCALATED            │
       │          │               │
       └──────────┴───────────────┘
                    (reopen)
```

## 6. Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Type System | dataclasses, Enum, typing |
| Logging | Python logging |
| Text Search | Regex-based indexing |
| IDs | uuid4 |
| Date/Time | datetime, timedelta |

## 7. SLA Configuration

| Priority | Tier | First Response | Resolution |
|----------|------|----------------|------------|
| CRITICAL | ANY | 1 hour | 4 hours |
| HIGH | ENTERPRISE | 2 hours | 8 hours |
| HIGH | OTHER | 4 hours | 24 hours |
| MEDIUM | ANY | 8 hours | 48 hours |
| LOW | ANY | 24 hours | 72 hours |

## 8. Scalability

| Dimension | Strategy |
|-----------|----------|
| Ticket Volume | In-memory dict; migrate to DB |
| KB Article Count | Inverted index for search |
| Agent Count | Assign agent_id to tickets |
| Multi-channel | ChannelType enum tracks source |
| Multi-tenant | Add tenant_id to all models |

## 9. Extension Points

1. **New Channel**: Add to `ChannelType` enum and intake handler
2. **Custom Escalation Rules**: Add to `EscalationManager.escalation_rules`
3. **AI Response**: Integrate LLM for auto-response generation
4. **Webhook Integration**: Add ticket event webhooks
5. **Custom Metrics**: Extend `SupportMetrics` with domain KPIs
6. **Chat Widget**: Add real-time chat channel support

## 10. Performance Characteristics

| Metric | Target |
|--------|--------|
| Ticket creation | < 20ms |
| KB search (1K articles) | < 50ms |
| Response generation | < 30ms |
| SLA check (1K tickets) | < 100ms |
| Dashboard generation | < 200ms |
| Memory per 10K tickets | < 50MB |

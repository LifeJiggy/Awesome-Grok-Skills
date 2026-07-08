# Support Agent

Customer support operations platform with ticket management, knowledge bases, SLA tracking, escalation workflows, and satisfaction metrics.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Ticket Management](#ticket-management)
  - [Knowledge Base](#knowledge-base)
  - [Response Engine](#response-engine)
  - [SLA Tracking](#sla-tracking)
  - [Escalation Workflows](#escalation-workflows)
  - [Customer Management](#customer-management)
  - [Analytics and Reporting](#analytics-and-reporting)
  - [Dashboard](#dashboard)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The Support Agent provides end-to-end customer support operations. It manages tickets from intake through resolution, maintains a searchable knowledge base, generates automated and templated responses, enforces SLA policies, handles multi-level escalation, and produces comprehensive analytics.

## Features

| Feature | Description |
|---------|-------------|
| **Ticket Lifecycle** | Full CRUD with status transitions, SLA tracking, and history |
| **Knowledge Base** | Searchable articles with helpfulness voting and view tracking |
| **Response Engine** | Automated, templated, KB-matched, and manual response types |
| **SLA Enforcement** | Per-priority/per-tier response and resolution deadlines |
| **Escalation Workflows** | Rules-based escalation with L1-L3 levels and acknowledgment |
| **Customer Profiles** | Tier management, satisfaction tracking, lifetime value |
| **Satisfaction Surveys** | CSAT and NPS collection with rolling averages |
| **Analytics** | FCR rate, SLA compliance, response times, recommendations |

## Architecture

```
SupportAgent (Facade)
├── TicketManager (CRUD, SLA, Status Flow, History)
├── KnowledgeBase (Articles, Search Index, Voting)
├── ResponseEngine (Auto, Template, KB Match, Escalation)
├── EscalationManager (Rules, Levels, Acknowledgment)
├── CustomerManager (Profiles, Tiers, Satisfaction)
└── SupportAnalytics (Metrics, Reports, Recommendations)
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for full details.

## Quick Start

```python
from agents.support.agent import SupportAgent

agent = SupportAgent()

# Handle a ticket
result = agent.handle_incoming_ticket(
    subject="Login issue",
    description="Cannot login after password reset",
    category="technical",
    priority="2",
    customer_email="user@example.com",
)

# Check dashboard
dashboard = agent.get_support_dashboard()
print(f"Open: {dashboard['queue']['open']}")
```

Run directly:

```bash
python agents/support/agent.py
```

## Usage

### Ticket Management

```python
from agents.support.agent import TicketManager, TicketCategory, TicketPriority, TicketStatus

tm = TicketManager()

# Create
ticket = tm.create_ticket(
    subject="Cannot access billing",
    description="Getting 403 on billing page",
    category=TicketCategory.BILLING,
    priority=TicketPriority.HIGH,
    customer_id="CUST-001",
)

# Assign
tm.assign_ticket(ticket.id, "agent_001")

# Add messages
tm.add_message(ticket.id, "agent", "I'll look into this.")
tm.add_message(ticket.id, "customer", "Thanks!")

# Status transitions
tm.update_status(ticket.id, TicketStatus.IN_PROGRESS)
tm.resolve_ticket(ticket.id, "Fixed permission issue")
tm.close_ticket(ticket.id)

# SLA check
alerts = tm.check_sla()

# Overdue tickets
overdue = tm.get_overdue(hours=24)
```

### Knowledge Base

```python
from agents.support.agent import KnowledgeBase, TicketCategory

kb = KnowledgeBase()

# Add articles
kb.add_article(
    title="How to Reset Password",
    content="Go to Settings > Security > Change Password...",
    category=TicketCategory.ACCOUNT,
    tags=["password", "reset"],
)

# Search
results = kb.search("password reset login")

# Helpful votes
kb.vote_helpful(article.id, helpful=True)

# Top articles
top = kb.get_top_articles(5)
```

### Response Engine

```python
from agents.support.agent import ResponseEngine, ResponseType

engine = ResponseEngine(kb)

# Auto response
response = engine.generate_response(ticket.id, ResponseType.AUTOMATED)

# Template
engine.add_template("followup", "Hi {{name}}, following up...")
response = engine.generate_response(
    ticket.id, ResponseType.TEMPLATED,
    template_name="followup",
    variables={"name": "John"}
)

# KB match
response = engine.generate_response(ticket.id, ResponseType.KNOWLEDGE_BASE)
```

### SLA Tracking

SLA policies are automatically applied based on ticket priority and customer tier:

```python
# Check SLA compliance
alerts = tm.check_sla()
# [{"ticket_id": "TKT-001", "status": "at_risk", "hours_remaining": 1.5}]

# Get overdue
overdue = tm.get_overdue(hours=24)
```

| Priority | First Response | Resolution |
|----------|---------------|------------|
| CRITICAL | 1 hour | 4 hours |
| HIGH | 4 hours | 24 hours |
| MEDIUM | 8 hours | 48 hours |
| LOW | 24 hours | 72 hours |

### Escalation Workflows

```python
from agents.support.agent import EscalationManager, EscalationLevel

em = EscalationManager()

# Manual escalation
esc = em.escalate_ticket(
    ticket_id="TKT-001",
    from_level=EscalationLevel.L1,
    to_level=EscalationLevel.L3,
    reason="Complex SSO integration issue",
)

# Acknowledge
em.acknowledge_escalation(esc.id, notes="Investigating SAML config")

# Auto-check rules
rule = em.check_escalation_rules(ticket)
```

**Escalation levels:**
```
L1 (Tier 1) → L2 (Tier 2) → L3 (Engineering) → Management
```

### Customer Management

```python
from agents.support.agent import CustomerManager, CustomerTier

cm = CustomerManager()

# Add customer
customer = cm.add_customer(
    name="John Doe",
    email="john@acme.com",
    company="Acme Corp",
    tier=CustomerTier.ENTERPRISE,
)

# Satisfaction
from agents.support.agent import SatisfactionRating
cm.update_satisfaction(customer.id, SatisfactionRating.SATISFIED)

# History
history = cm.get_customer_history(customer.id)
```

### Analytics and Reporting

```python
from agents.support.agent import SupportAnalytics

analytics = SupportAnalytics(tm, cm)

# Metrics
metrics = analytics.calculate_metrics()
# SupportMetrics(open_tickets=15, avg_first_response_hours=2.3, ...)

# Report
report = analytics.generate_report()
# {"period": {...}, "summary": {...}, "alerts": {...}, "recommendations": [...]}
```

### Dashboard

```python
dashboard = agent.get_support_dashboard()
# {
#   "queue": {"open": 15, "critical": 2, "overdue": 3},
#   "metrics": {"avg_first_response_hours": 2.3, "satisfaction": 4.2},
#   "sla_alerts": [...],
#   "knowledge_base": {"total_articles": 150},
#   "escalations": {"total": 8, "unacknowledged": 1},
#   "recommendations": [...]
# }
```

## API Reference

### SupportAgent

| Method | Returns |
|--------|---------|
| `handle_incoming_ticket(subject, desc, category, priority, email, **kw)` | Dict |
| `generate_auto_response(ticket_id)` | Dict |
| `escalate_ticket(ticket_id, reason, escalate_to?)` | Dict |
| `resolve_ticket(ticket_id, notes?)` | Dict |
| `submit_satisfaction(ticket_id, rating, feedback?, nps?)` | Dict |
| `search_knowledge_base(query)` | List[Dict] |
| `get_support_dashboard()` | Dict |

### TicketManager

| Method | Returns |
|--------|---------|
| `create_ticket(subject, desc, category, priority, customer_id, ...)` | Ticket |
| `assign_ticket(ticket_id, assignee_id)` | Ticket |
| `update_status(ticket_id, status, note?)` | Ticket |
| `add_message(ticket_id, role, content, agent_id?)` | Dict |
| `resolve_ticket(ticket_id, notes?)` | Ticket |
| `close_ticket(ticket_id)` | Ticket |
| `reopen_ticket(ticket_id, reason)` | Ticket |
| `check_sla()` | List[Dict] |
| `get_overdue(hours?)` | List[Ticket] |

### KnowledgeBase

| Method | Returns |
|--------|---------|
| `add_article(title, content, category, tags, author?)` | KnowledgeArticle |
| `search(query, limit?)` | List[KnowledgeArticle] |
| `record_view(article_id)` | None |
| `vote_helpful(article_id, helpful)` | None |
| `get_top_articles(limit?)` | List[KnowledgeArticle] |

### EscalationManager

| Method | Returns |
|--------|---------|
| `escalate_ticket(ticket_id, from_level, to_level, reason, ...)` | Escalation |
| `acknowledge_escalation(escalation_id, notes?)` | Dict |
| `check_escalation_rules(ticket)` | Optional[Dict] |
| `get_escalation_history(ticket_id?)` | List[Escalation] |

### CustomerManager

| Method | Returns |
|--------|---------|
| `add_customer(name, email, company?, tier?)` | Customer |
| `get_by_email(email)` | Optional[Customer] |
| `get_by_id(customer_id)` | Optional[Customer] |
| `update_satisfaction(customer_id, rating)` | None |
| `get_customer_history(customer_id)` | Dict |

### SupportAnalytics

| Method | Returns |
|--------|---------|
| `calculate_metrics()` | SupportMetrics |
| `generate_report(start_date?, end_date?)` | Dict |

## Configuration

```python
import logging
logging.basicConfig(level=logging.INFO)

# Custom SLA policies
from agents.support.agent import SLAPolicy, TicketPriority, CustomerTier
agent.tickets.sla_policies = {
    "CRITICAL_DEFAULT": SLAPolicy(
        id="sla_crit", name="Critical SLA",
        priority=TicketPriority.CRITICAL, tier=CustomerTier.FREE,
        first_response_hours=1, resolution_hours=4,
        business_hours_only=False, description="Critical support",
    ),
}

# Custom escalation rules
agent.escalation.escalation_rules.append({
    "condition": "category == SECURITY",
    "action": "escalate_to_l3",
    "immediate": True,
})
```

## Examples

See `main()` in `agent.py` for a complete working example demonstrating:
- Knowledge base article creation
- Ticket intake and handling
- KB search
- Escalation
- Dashboard generation

## Best Practices

1. **Search KB first** - Don't write new answers for existing questions
2. **Use templates** - Consistency saves time
3. **Set SLA policies** - Default policies may not fit your needs
4. **Track satisfaction** - CSAT is your quality signal
5. **Review escalations** - Recurring escalations indicate training gaps
6. **Update KB regularly** - Outdated articles erode trust
7. **Close resolved tickets** - Open-but-resolved skews metrics

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Ticket not found | Check ID format: TKT-XXXXXXXX |
| KB search empty | Add articles with relevant tags |
| SLA always ON_TRACK | Configure SLAPolicy for each priority |
| Escalation not firing | Verify rule conditions match ticket state |
| Metrics show 0 | Need tickets with messages and resolution times |
| Customer duplicate | add_customer deduplicates by email |
| Response template missing | Add template with ResponseEngine.add_template() |

## Files

| File | Description |
|------|-------------|
| `agent.py` | Full implementation with all subsystems |
| `ARCHITECTURE.md` | System architecture and design patterns |
| `GROK.md` | Agent identity, capabilities, and API docs |
| `README.md` | This file |

## License

MIT License - See [LICENSE](../../LICENSE) for details.

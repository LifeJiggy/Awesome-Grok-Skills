---
name: "Support Agent"
version: "2.0.0"
description: "Customer support operations - ticket management, knowledge bases, SLA tracking, escalation workflows, satisfaction metrics"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["support", "tickets", "knowledge-base", "sla", "escalation", "satisfaction"]
category: "support"
personality: "support-specialist"
use_cases:
  - "ticket-management"
  - "knowledge-base"
  - "sla-tracking"
  - "escalation-workflows"
  - "customer-satisfaction"
  - "support-analytics"
---

# Support Agent

> Customer support operations with ticket management, knowledge bases, SLA tracking, escalation workflows, and satisfaction metrics.

## Identity

The Support Agent is a full-lifecycle customer support operations platform. It manages tickets from creation through resolution with SLA tracking, provides a searchable knowledge base with helpfulness scoring, generates automated and templated responses, handles multi-level escalation workflows, and calculates comprehensive support metrics.

**Core principle:** Every ticket has a deadline. Every customer has a history. Every resolution should teach.

## Principles

1. **First Response Fast** - Acknowledge within SLA, even with "we're looking into it"
2. **Resolve at Lowest Level** - L1 should handle 70%+ of tickets
3. **Knowledge Before Response** - Search KB before writing new answers
4. **Escalate with Context** - Never escalate empty-handed
5. **Measure Everything** - Response time, resolution time, satisfaction
6. **Close the Loop** - Follow up after resolution

## Capabilities

### 1. Ticket Management

```python
from agents.support.agent import TicketManager, TicketCategory, TicketPriority, TicketStatus

tm = TicketManager()

# Create ticket
ticket = tm.create_ticket(
    subject="Cannot login",
    description="Getting 403 error after password reset",
    category=TicketCategory.TECHNICAL,
    priority=TicketPriority.HIGH,
    customer_id="CUST-001",
)
# ticket.id = "TKT-A1B2C3D4"

# Assign to agent
tm.assign_ticket(ticket.id, "agent_001")

# Add messages
tm.add_message(ticket.id, "agent", "Can you try clearing your browser cache?")
tm.add_message(ticket.id, "customer", "That worked! Thank you.")

# Resolve
tm.resolve_ticket(ticket.id, "Browser cache was stale")

# Reopen if needed
tm.reopen_ticket(ticket.id, "Issue returned after restart")
```

**Ticket lifecycle:**
```
OPEN → IN_PROGRESS → WAITING → RESOLVED → CLOSED
                 ↕              ↑
              ESCALATED ────────┘
```

### 2. Knowledge Base

```python
from agents.support.agent import KnowledgeBase, TicketCategory

kb = KnowledgeBase()

# Add articles
article = kb.add_article(
    title="How to Reset Password",
    content="Go to Settings > Security > Change Password...",
    category=TicketCategory.ACCOUNT,
    tags=["password", "reset", "security"],
)

# Search
results = kb.search("password reset login")
# [KnowledgeArticle(title="How to Reset Password", helpful_ratio=0.85)]

# Track helpfulness
kb.vote_helpful(article.id, helpful=True)
kb.record_view(article.id)

# Get top articles
top = kb.get_top_articles(limit=5)
```

### 3. Response Engine

```python
from agents.support.agent import ResponseEngine, ResponseType

engine = ResponseEngine(kb)

# Automated response
response = engine.generate_response(ticket.id, ResponseType.AUTOMATED)
# {"type": "automated", "content": "Thank you for contacting support..."}

# Templated response
engine.add_template("followup", "Hi {{name}}, following up on ticket {{ticket_id}}...")
response = engine.generate_response(
    ticket.id, ResponseType.TEMPLATED,
    template_name="followup",
    variables={"name": "John", "ticket_id": ticket.id}
)

# KB-matched response
response = engine.generate_response(ticket.id, ResponseType.KNOWLEDGE_BASE)
```

### 4. SLA Tracking

```python
from agents.support.agent import SLAPolicy, TicketPriority, CustomerTier

# SLA policies are checked automatically
alerts = tm.check_sla()
# [{"ticket_id": "TKT-001", "status": "at_risk", "hours_remaining": 1.5}]

# Check overdue tickets
overdue = tm.get_overdue(hours=24)
```

**SLA defaults:**
| Priority | First Response | Resolution |
|----------|---------------|------------|
| CRITICAL | 1 hour | 4 hours |
| HIGH | 4 hours | 24 hours |
| MEDIUM | 8 hours | 48 hours |
| LOW | 24 hours | 72 hours |

### 5. Escalation Workflows

```python
from agents.support.agent import EscalationManager, EscalationLevel

em = EscalationManager()

# Manual escalation
esc = em.escalate_ticket(
    ticket_id="TKT-001",
    from_level=EscalationLevel.L1,
    to_level=EscalationLevel.L3,
    reason="Complex auth issue with SSO integration",
)
# esc.id = "ESC-A1B2C3D4"

# Acknowledge
em.acknowledge_escalation(esc.id, notes="Looking into SAML config")

# Auto-check rules
rule = em.check_escalation_rules(ticket)
# {"condition": "priority == CRITICAL", "action": "escalate_to_l3"}
```

**Escalation levels:**
```
L1 (Tier 1) → L2 (Tier 2) → L3 (Engineering) → Management → Executive
```

### 6. Customer Management

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

# Update satisfaction
from agents.support.agent import SatisfactionRating
cm.update_satisfaction(customer.id, SatisfactionRating.SATISFIED)

# Get history
history = cm.get_customer_history(customer.id)
```

### 7. Support Analytics

```python
from agents.support.agent import SupportAnalytics

analytics = SupportAnalytics(tm, cm)

# Calculate metrics
metrics = analytics.calculate_metrics()
# SupportMetrics(
#   open_tickets=15,
#   avg_first_response_hours=2.3,
#   avg_resolution_hours=18.5,
#   satisfaction_score=4.2,
#   sla_compliance_rate=0.94,
# )

# Generate report
report = analytics.generate_report()
# {"period": {...}, "summary": {...}, "alerts": {...}, "recommendations": [...]}
```

### 8. Unified Dashboard

```python
agent = SupportAgent()
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

## Method Signatures

```python
class SupportAgent:
    def handle_incoming_ticket(self, subject, description, category, priority, customer_email, **kwargs) -> Dict
    def generate_auto_response(self, ticket_id) -> Dict
    def escalate_ticket(self, ticket_id, reason, escalate_to?) -> Dict
    def resolve_ticket(self, ticket_id, resolution_notes?) -> Dict
    def submit_satisfaction(self, ticket_id, rating, feedback?, nps_score?) -> Dict
    def search_knowledge_base(self, query) -> List[Dict]
    def get_support_dashboard(self) -> Dict

class TicketManager:
    def create_ticket(self, subject, description, category, priority, customer_id, channel?, tags?, metadata?) -> Ticket
    def assign_ticket(self, ticket_id, assignee_id) -> Ticket
    def update_status(self, ticket_id, new_status, note?) -> Ticket
    def add_message(self, ticket_id, role, content, agent_id?) -> Dict
    def resolve_ticket(self, ticket_id, resolution_notes?) -> Ticket
    def close_ticket(self, ticket_id) -> Ticket
    def reopen_ticket(self, ticket_id, reason) -> Ticket
    def check_sla(self) -> List[Dict]
    def get_overdue(self, hours?) -> List[Ticket]

class KnowledgeBase:
    def add_article(self, title, content, category, tags, author?) -> KnowledgeArticle
    def search(self, query, limit?) -> List[KnowledgeArticle]
    def record_view(self, article_id) -> None
    def vote_helpful(self, article_id, helpful) -> None
    def get_top_articles(self, limit?) -> List[KnowledgeArticle]
```

## Data Models

### Ticket
| Field | Type | Description |
|-------|------|-------------|
| id | str | Format: TKT-XXXXXXXX |
| priority | TicketPriority | CRITICAL=1, HIGH=2, MEDIUM=3, LOW=4 |
| status | TicketStatus | Lifecycle state |
| sla_deadline | Optional[datetime] | First response deadline |
| sla_status | SLAStatus | ON_TRACK, AT_RISK, BREACHED |
| satisfaction_rating | Optional[SatisfactionRating] | 1-5 scale |

### KnowledgeArticle
| Field | Type | Description |
|-------|------|-------------|
| id | str | Format: KB-XXXXXXXX |
| views | int | View count |
| helpful_votes | int | Upvotes |
| not_helpful_votes | int | Downvotes |
| helpful_ratio | float | helpful / total |

### Customer
| Field | Type | Description |
|-------|------|-------------|
| id | str | Format: CUST-XXXXXXXX |
| tier | CustomerTier | FREE, STARTER, PROFESSIONAL, ENTERPRISE |
| satisfaction_score | float | Rolling average 1-5 |
| lifetime_value | float | Revenue contribution |

## Checklist

### Ticket Creation
- [ ] Subject is concise and descriptive
- [ ] Category is correctly classified
- [ ] Priority matches urgency
- [ ] SLA deadline is calculated

### Response
- [ ] Search KB first
- [ ] Use template when available
- [ ] Personalize automated responses
- [ ] Set expectations for follow-up

### Resolution
- [ ] Root cause is documented
- [ ] Resolution notes are clear
- [ ] Customer is notified
- [ ] CSAT survey is sent

### Escalation
- [ ] Context is included
- [ ] Correct level is targeted
- [ ] Customer is informed
- [ ] SLA is updated

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Ticket not found | Check ID format: TKT-XXXXXXXX |
| KB search returns nothing | Add articles with relevant tags |
| SLA always ON_TRACK | Ensure SLAPolicy is configured for priority |
| Escalation not triggering | Check rule conditions match ticket properties |
| Metrics show 0 | Tickets need messages and resolution times |
| Customer not found | Use add_customer() - it deduplicates by email |

## Security Notes

- Customer PII (email, name) is stored as-is; encrypt at rest
- Ticket messages may contain sensitive data; access-control
- KB articles are visible to all agents; restrict sensitive topics
- Satisfaction data is used for performance; handle confidentially
- Escalation notes may contain internal assessments

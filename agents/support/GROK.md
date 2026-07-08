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
  - "customer-success"
---

# Support Agent

> Customer support operations with ticket management, knowledge bases, SLA tracking, escalation workflows, and satisfaction metrics.

## Identity

The Support Agent is a full-lifecycle customer support operations platform. It manages tickets from creation through resolution with SLA tracking, provides a searchable knowledge base with helpfulness scoring, generates automated and templated responses, handles multi-level escalation workflows, and calculates comprehensive support metrics.

**Core principle:** Every ticket has a deadline. Every customer has a history. Every resolution should teach.

**Personality:** The agent is an empathetic, efficient support specialist who prioritizes first-contact resolution while maintaining service quality. It balances speed with thoroughness, automation with personal touch, and metrics with customer experience.

## Principles

1. **First Response Fast** - Acknowledge within SLA, even with "we're looking into it"
2. **Resolve at Lowest Level** - L1 should handle 70%+ of tickets
3. **Knowledge Before Response** - Search KB before writing new answers
4. **Escalate with Context** - Never escalate empty-handed
5. **Measure Everything** - Response time, resolution time, satisfaction
6. **Close the Loop** - Follow up after resolution
7. **Proactive Support** - Identify issues before customers report them
8. **Continuous Improvement** - Learn from every ticket

## Capabilities

### 1. Ticket Management

```python
from agents.support.agent import TicketManager, TicketCategory, TicketPriority, TicketStatus

tm = TicketManager()

# Create ticket
ticket = tm.create_ticket(
    subject="Cannot login after password reset",
    description="Getting 403 error after resetting password. Tried clearing cache but still not working.",
    category=TicketCategory.TECHNICAL,
    priority=TicketPriority.HIGH,
    customer_id="CUST-001",
    channel="email",
    tags=["login", "password", "403-error"]
)
# ticket.id = "TKT-A1B2C3D4"
# ticket.sla_deadline = datetime + 4 hours (HIGH priority)

# Assign to agent
tm.assign_ticket(ticket.id, "agent_001")

# Add messages
tm.add_message(ticket.id, "agent", "Can you try clearing your browser cache and cookies?")
tm.add_message(ticket.id, "customer", "Tried that, still getting 403")
tm.add_message(ticket.id, "agent", "I see the issue - your account needs re-verification. Let me fix that.")
tm.add_message(ticket.id, "customer", "That worked! Thank you!")

# Resolve
tm.resolve_ticket(ticket.id, "Account required re-verification after password reset")

# Reopen if needed
tm.reopen_ticket(ticket.id, "Issue returned after computer restart")
```

**Ticket lifecycle:**
```
OPEN → IN_PROGRESS → WAITING → RESOLVED → CLOSED
                 ↕              ↑
              ESCALATED ────────┘
```

**Ticket Priority SLAs:**
| Priority | First Response | Resolution | Example |
|----------|---------------|------------|---------|
| CRITICAL | 1 hour | 4 hours | Production down, data loss |
| HIGH | 4 hours | 24 hours | Major feature broken |
| MEDIUM | 8 hours | 48 hours | Workaround available |
| LOW | 24 hours | 72 hours | Minor issue, cosmetic |

### 2. Knowledge Base

```python
from agents.support.agent import KnowledgeBase, TicketCategory

kb = KnowledgeBase()

# Add articles
article = kb.add_article(
    title="How to Reset Password",
    content="1. Go to Settings > Security\n2. Click 'Change Password'\n3. Enter current password\n4. Enter new password twice\n5. Click Save",
    category=TicketCategory.ACCOUNT,
    tags=["password", "reset", "security", "login"],
    author="support-team"
)
# article.id = "KB-A1B2C3D4"

# Search
results = kb.search("password reset login")
# [
#   KnowledgeArticle(
#     title="How to Reset Password",
#     helpful_ratio=0.85,
#     views=1250,
#     score=92.5
#   ),
#   KnowledgeArticle(
#     title="Troubleshooting Login Issues",
#     helpful_ratio=0.72,
#     views=890,
#     score=78.3
#   )
# ]

# Track helpfulness
kb.vote_helpful(article.id, helpful=True)
kb.vote_helpful(article.id, helpful=True)
kb.vote_helpful(article.id, helpful=False)
# article.helpful_ratio = 0.67

# Record view
kb.record_view(article.id)

# Get top articles
top = kb.get_top_articles(limit=5)
# [
#   {"title": "How to Reset Password", "views": 1250, "helpful_ratio": 0.85},
#   ...
# ]

# Get by category
account_articles = kb.get_by_category(TicketCategory.ACCOUNT)
```

**KB Search Scoring:**
| Factor | Weight | Description |
|--------|--------|-------------|
| Word Match | 50% | Exact and partial word matches |
| Tag Match | 30% | Matching tags boost relevance |
| Helpful Ratio | 15% | Higher helpfulness = higher rank |
| Views | 5% | Popularity signal |

### 3. Response Engine

```python
from agents.support.agent import ResponseEngine, ResponseType

engine = ResponseEngine(kb)

# Automated response
response = engine.generate_response(ticket.id, ResponseType.AUTOMATED)
# {
#   "type": "automated",
#   "content": "Thank you for contacting support. Your ticket TKT-A1B2C3D4 has been created. We'll respond within 4 hours.",
#   "confidence": 0.95
# }

# Templated response
engine.add_template(
    "followup",
    "Hi {{name}},\n\nFollowing up on your ticket {{ticket_id}}.\n\n{{message}}\n\nBest,\nSupport Team"
)
response = engine.generate_response(
    ticket.id, ResponseType.TEMPLATED,
    template_name="followup",
    variables={
        "name": "John",
        "ticket_id": ticket.id,
        "message": "We've resolved your issue. Please let us know if you need anything else."
    }
)

# KB-matched response
response = engine.generate_response(ticket.id, ResponseType.KNOWLEDGE_BASE)
# {
#   "type": "knowledge_base",
#   "articles": [
#     {"title": "How to Reset Password", "relevance": 0.92},
#     {"title": "Troubleshooting Login Issues", "relevance": 0.78}
#   ],
#   "suggested_response": "Based on your issue, here are some relevant articles..."
# }
```

**Response Types:**
| Type | When to Use | Automation Level |
|------|-------------|------------------|
| AUTOMATED | Ticket creation, status updates | Fully automated |
| TEMPLATED | Common issues, follow-ups | Semi-automated |
| KNOWLEDGE_BASE | How-to questions | Suggested content |
| ESCALATED | Complex issues, SLA risk | Queue for human |
| MANUAL | Unique issues, sensitive cases | Full human |

### 4. SLA Tracking

```python
from agents.support.agent import SLAPolicy, TicketPriority, CustomerTier

# SLA policies are checked automatically
alerts = tm.check_sla()
# [
#   {
#     "ticket_id": "TKT-001",
#     "status": "at_risk",
#     "hours_remaining": 1.5,
#     "sla_type": "first_response",
#     "priority": "high"
#   },
#   {
#     "ticket_id": "TKT-002",
#     "status": "breached",
#     "hours_overdue": 2.0,
#     "sla_type": "resolution",
#     "priority": "critical"
#   }
# ]

# Check overdue tickets
overdue = tm.get_overdue(hours=24)
# [Ticket(id="TKT-003", subject="...", status="open", hours_open=26)]

# Get SLA compliance report
sla_report = tm.get_sla_report()
# {
#   "total_tickets": 150,
#   "within_sla": 142,
#   "breached": 8,
#   "compliance_rate": 0.947,
#   "by_priority": {
#     "critical": {"total": 5, "within_sla": 5, "rate": 1.0},
#     "high": {"total": 25, "within_sla": 23, "rate": 0.92},
#     "medium": {"total": 80, "within_sla": 76, "rate": 0.95},
#     "low": {"total": 40, "within_sla": 38, "rate": 0.95}
#   }
# }
```

### 5. Escalation Workflows

```python
from agents.support.agent import EscalationManager, EscalationLevel

em = EscalationManager()

# Manual escalation
esc = em.escalate_ticket(
    ticket_id="TKT-001",
    from_level=EscalationLevel.L1,
    to_level=EscalationLevel.L3,
    reason="Complex SSO integration issue requires engineering expertise",
    notes="Customer uses Okta SAML, getting certificate validation error"
)
# esc.id = "ESC-A1B2C3D4"

# Acknowledge
em.acknowledge_escalation(esc.id, notes="Investigating SAML certificate chain")

# Auto-check rules
rule = em.check_escalation_rules(ticket)
# {
#   "should_escalate": True,
#   "reason": "priority == CRITICAL",
#   "target_level": "L3"
# }

# Get escalation history
history = em.get_escalation_history(ticket.id)
# [
#   {
#     "id": "ESC-001",
#     "from_level": "L1",
#     "to_level": "L2",
#     "reason": "Customer frustrated, needs specialist",
#     "timestamp": "2025-01-15T10:30:00Z"
#   },
#   {
#     "id": "ESC-002",
#     "from_level": "L2",
#     "to_level": "L3",
#     "reason": "Engineering issue",
#     "timestamp": "2025-01-15T11:00:00Z"
#   }
# ]
```

**Escalation Levels:**
```
L1 (Tier 1) → L2 (Tier 2) → L3 (Engineering) → Management → Executive

Escalation Triggers:
- Critical priority → Immediate L3
- Enterprise customer → L2 immediate
- SLA breach → Escalate one level
- Customer satisfaction < 2 → Management
- Repeated issue (3+ tickets) → L2
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
    tier=CustomerTier.ENTERPRISE
)
# customer.id = "CUST-A1B2C3D4"
# customer.satisfaction_score = 0.0 (no data yet)

# Update satisfaction
from agents.support.agent import SatisfactionRating
cm.update_satisfaction(customer.id, SatisfactionRating.SATISFIED)
cm.update_satisfaction(customer.id, SatisfactionRating.VERY_SATISFIED)
# customer.satisfaction_score = 4.5

# Get history
history = cm.get_customer_history(customer.id)
# {
#   "customer_id": "CUST-A1B2C3D4",
#   "total_tickets": 12,
#   "avg_resolution_hours": 18.5,
#   "satisfaction_trend": [4.0, 4.5, 4.5],
#   "common_categories": ["technical", "billing"],
#   "lifetime_value": 125000.0
# }

# Get customer summary
summary = cm.get_customer_summary()
# {
#   "total_customers": 500,
#   "by_tier": {"enterprise": 50, "professional": 150, "starter": 300},
#   "avg_satisfaction": 4.2,
#   "at_risk_count": 12
# }
```

**Customer Tiers:**
| Tier | SLA Response | SLA Resolution | Support Level |
|------|--------------|----------------|---------------|
| FREE | 48 hours | 7 days | Email only |
| STARTER | 24 hours | 3 days | Email |
| PROFESSIONAL | 8 hours | 1 day | Email + Chat |
| ENTERPRISE | 4 hours | 8 hours | Priority + Phone |
| PLATINUM | 1 hour | 4 hours | 24/7 + Dedicated CSM |

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
#   first_contact_resolution=0.72,
#   tickets_per_agent=12.5
# )

# Generate report
report = analytics.generate_report()
# {
#   "period": {"start": "2025-01-01", "end": "2025-01-31"},
#   "summary": {
#     "total_tickets": 450,
#     "resolved": 420,
#     "open": 30,
#     "avg_first_response_hours": 2.3,
#     "avg_resolution_hours": 18.5,
#     "satisfaction_score": 4.2
#   },
#   "alerts": [
#     {"type": "sla_breach", "count": 8, "priority": "high"},
#     {"type": "at_risk_customers", "count": 12, "priority": "medium"}
#   ],
#   "recommendations": [
#     "Increase L1 training on password reset issues",
#     "Add KB article for common 403 errors",
#     "Review escalation rules for enterprise tickets"
#   ]
# }
```

### 8. Unified Dashboard

```python
agent = SupportAgent()
dashboard = agent.get_support_dashboard()
# {
#   "queue": {
#     "open": 15,
#     "critical": 2,
#     "overdue": 3,
#     "avg_wait_hours": 4.5
#   },
#   "metrics": {
#     "avg_first_response_hours": 2.3,
#     "avg_resolution_hours": 18.5,
#     "satisfaction": 4.2,
#     "sla_compliance": 0.94
#   },
#   "sla_alerts": [
#     {"ticket_id": "TKT-001", "status": "at_risk", "hours_remaining": 1.5}
#   ],
#   "knowledge_base": {
#     "total_articles": 150,
#     "top_searches": ["password reset", "login issues", "billing"],
#     "unanswered_queries": 5
#   },
#   "escalations": {
#     "total": 8,
#     "unacknowledged": 1,
#     "avg_resolution_hours": 6.2
#   },
#   "recommendations": [
#     "Add KB article for top unanswered query",
#     "Review escalation rules for L1 tickets"
#   ]
# }
```

## Method Signatures

```python
class SupportAgent:
    def handle_incoming_ticket(self, subject: str, description: str, category: TicketCategory, priority: TicketPriority, customer_email: str, **kwargs) -> Dict
    def generate_auto_response(self, ticket_id: str) -> Dict
    def escalate_ticket(self, ticket_id: str, reason: str, escalate_to: Optional[EscalationLevel] = None) -> Dict
    def resolve_ticket(self, ticket_id: str, resolution_notes: Optional[str] = None) -> Dict
    def submit_satisfaction(self, ticket_id: str, rating: SatisfactionRating, feedback: Optional[str] = None, nps_score: Optional[int] = None) -> Dict
    def search_knowledge_base(self, query: str) -> List[Dict]
    def get_support_dashboard(self) -> Dict

class TicketManager:
    def create_ticket(self, subject: str, description: str, category: TicketCategory, priority: TicketPriority, customer_id: str, channel: Optional[str] = None, tags: Optional[List[str]] = None, metadata: Optional[Dict] = None) -> Ticket
    def assign_ticket(self, ticket_id: str, assignee_id: str) -> Ticket
    def update_status(self, ticket_id: str, new_status: TicketStatus, note: Optional[str] = None) -> Ticket
    def add_message(self, ticket_id: str, role: str, content: str, agent_id: Optional[str] = None) -> Dict
    def resolve_ticket(self, ticket_id: str, resolution_notes: Optional[str] = None) -> Ticket
    def close_ticket(self, ticket_id: str) -> Ticket
    def reopen_ticket(self, ticket_id: str, reason: str) -> Ticket
    def check_sla(self) -> List[Dict]
    def get_overdue(self, hours: int = 24) -> List[Ticket]
    def get_sla_report(self) -> Dict

class KnowledgeBase:
    def add_article(self, title: str, content: str, category: TicketCategory, tags: List[str], author: Optional[str] = None) -> KnowledgeArticle
    def search(self, query: str, limit: int = 10) -> List[KnowledgeArticle]
    def record_view(self, article_id: str) -> None
    def vote_helpful(self, article_id: str, helpful: bool) -> None
    def get_top_articles(self, limit: int = 10) -> List[KnowledgeArticle]
    def get_by_category(self, category: TicketCategory) -> List[KnowledgeArticle]
    def update_article(self, article_id: str, content: Optional[str] = None, tags: Optional[List[str]] = None) -> KnowledgeArticle
    def delete_article(self, article_id: str) -> bool

class ResponseEngine:
    def generate_response(self, ticket_id: str, response_type: ResponseType, template_name: Optional[str] = None, variables: Optional[Dict] = None) -> Dict
    def add_template(self, name: str, template: str) -> None
    def get_response_history(self, ticket_id: str) -> List[Dict]

class EscalationManager:
    def escalate_ticket(self, ticket_id: str, from_level: EscalationLevel, to_level: EscalationLevel, reason: str, notes: Optional[str] = None) -> Escalation
    def acknowledge_escalation(self, escalation_id: str, notes: str) -> Dict
    def check_escalation_rules(self, ticket: Ticket) -> Dict
    def get_escalation_history(self, ticket_id: str) -> List[Dict]

class CustomerManager:
    def add_customer(self, name: str, email: str, company: str, tier: CustomerTier) -> Customer
    def update_satisfaction(self, customer_id: str, rating: SatisfactionRating) -> Dict
    def get_customer_history(self, customer_id: str) -> Dict
    def get_customer_summary(self) -> Dict

class SupportAnalytics:
    def calculate_metrics(self) -> SupportMetrics
    def generate_report(self) -> Dict
```

## Data Models

### Ticket
| Field | Type | Description |
|-------|------|-------------|
| id | str | Format: TKT-XXXXXXXX |
| subject | str | Ticket title |
| description | str | Detailed description |
| category | TicketCategory | TECHNICAL, BILLING, ACCOUNT, FEATURE_REQUEST, BUG_REPORT |
| priority | TicketPriority | CRITICAL=1, HIGH=2, MEDIUM=3, LOW=4 |
| status | TicketStatus | OPEN, IN_PROGRESS, WAITING_ON_CUSTOMER, WAITING_ON_INTERNAL, RESOLVED, CLOSED, ESCALATED |
| customer_id | str | Customer reference |
| assignee_id | Optional[str] | Assigned agent |
| channel | str | email, chat, phone, api, social |
| tags | List[str] | Classification tags |
| messages | List[Dict] | Conversation history |
| sla_deadline | Optional[datetime] | First response deadline |
| sla_status | SLAStatus | ON_TRACK, AT_RISK, BREACHED |
| satisfaction_rating | Optional[SatisfactionRating] | 1-5 scale |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |
| resolved_at | Optional[datetime] | Resolution timestamp |

### KnowledgeArticle
| Field | Type | Description |
|-------|------|-------------|
| id | str | Format: KB-XXXXXXXX |
| title | str | Article title |
| content | str | Article content |
| category | TicketCategory | Category classification |
| tags | List[str] | Searchable tags |
| author | str | Article author |
| views | int | View count |
| helpful_votes | int | Upvotes |
| not_helpful_votes | int | Downvotes |
| helpful_ratio | float | helpful / (helpful + not_helpful) |
| created_at | datetime | Creation timestamp |
| updated_at | datetime | Last update timestamp |

### Customer
| Field | Type | Description |
|-------|------|-------------|
| id | str | Format: CUST-XXXXXXXX |
| name | str | Customer name |
| email | str | Customer email |
| company | str | Company name |
| tier | CustomerTier | FREE, STARTER, PROFESSIONAL, ENTERPRISE, PLATINUM |
| satisfaction_score | float | Rolling average 1-5 |
| lifetime_value | float | Revenue contribution |
| total_tickets | int | Total tickets submitted |
| avg_resolution_hours | float | Average resolution time |

### Escalation
| Field | Type | Description |
|-------|------|-------------|
| id | str | Format: ESC-XXXXXXXX |
| ticket_id | str | Associated ticket |
| from_level | EscalationLevel | Previous level |
| to_level | EscalationLevel | New level |
| reason | str | Escalation reason |
| notes | str | Additional context |
| acknowledged | bool | Whether acknowledged |
| acknowledged_at | Optional[datetime] | Acknowledgment timestamp |
| timestamp | datetime | Escalation timestamp |

## Checklist

### Ticket Creation
- [ ] Subject is concise and descriptive
- [ ] Category is correctly classified
- [ ] Priority matches urgency
- [ ] SLA deadline is calculated
- [ ] Customer is identified
- [ ] Channel is recorded

### Response
- [ ] Search KB first
- [ ] Use template when available
- [ ] Personalize automated responses
- [ ] Set expectations for follow-up
- [ ] Document actions taken

### Resolution
- [ ] Root cause is documented
- [ ] Resolution notes are clear
- [ ] Customer is notified
- [ ] CSAT survey is sent
- [ ] KB updated if needed

### Escalation
- [ ] Context is included
- [ ] Correct level is targeted
- [ ] Customer is informed
- [ ] SLA is updated
- [ ] Handoff notes are complete

### Knowledge Base
- [ ] Article is searchable
- [ ] Content is accurate
- [ ] Tags are relevant
- [ ] Category is correct

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Ticket not found | Check ID format: TKT-XXXXXXXX |
| KB search returns nothing | Add articles with relevant tags |
| SLA always ON_TRACK | Ensure SLAPolicy is configured for priority |
| Escalation not triggering | Check rule conditions match ticket properties |
| Metrics show 0 | Tickets need messages and resolution times |
| Customer not found | Use add_customer() - it deduplicates by email |
| Response template not found | Check template name matches exactly |
| SLA breach not detected | Verify SLA policy exists for priority+tier combo |
| Satisfaction score = 0 | Submit satisfaction survey via submit_satisfaction() |
| KB helpful_ratio = 0 | Vote helpful/not_helpful via vote_helpful() |

## Security Notes

- Customer PII (email, name) is stored as-is; encrypt at rest
- Ticket messages may contain sensitive data; access-control
- KB articles are visible to all agents; restrict sensitive topics
- Satisfaction data is used for performance; handle confidentially
- Escalation notes may contain internal assessments
- Customer tier should not be disclosed to other customers
- Agent IDs should be validated before assignment
- Resolution notes may be shared with customers; avoid internal jargon

## Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| Ticket creation | < 20ms | In-memory storage |
| KB search (1K articles) | < 50ms | Inverted index |
| Response generation | < 30ms | Template caching |
| SLA check (1K tickets) | < 100ms | Batch evaluation |
| Dashboard generation | < 200ms | Cached aggregations |

---

*Support Agent v2.0 — Part of the Awesome Grok Skills collection.*

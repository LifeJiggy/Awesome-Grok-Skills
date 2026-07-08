"""
Support Agent - Customer Support Operations and Service Excellence.

Comprehensive capabilities for ticket management, knowledge bases, SLA tracking,
escalation workflows, customer satisfaction metrics, and multi-channel support.
"""

from __future__ import annotations

import json
import logging
import re
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class TicketStatus(Enum):
    """Ticket lifecycle status."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING_ON_CUSTOMER = "waiting_on_customer"
    WAITING_ON_INTERNAL = "waiting_on_internal"
    ESCALATED = "escalated"
    RESOLVED = "resolved"
    CLOSED = "closed"
    REOPENED = "reopened"


class TicketPriority(Enum):
    """Ticket priority levels."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TicketCategory(Enum):
    """Ticket classification categories."""
    BUG = "bug"
    FEATURE_REQUEST = "feature_request"
    QUESTION = "question"
    ACCOUNT = "account"
    BILLING = "billing"
    TECHNICAL = "technical"
    SECURITY = "security"
    ONBOARDING = "onboarding"
    INTEGRATION = "integration"
    GENERAL = "general"


class ResponseType(Enum):
    """Types of support responses."""
    AUTOMATED = "automated"
    TEMPLATED = "templated"
    KNOWLEDGE_BASE = "knowledge_base"
    ESCALATED = "escalated"
    MANUAL = "manual"


class CustomerTier(Enum):
    """Customer subscription tiers."""
    FREE = "free"
    STARTER = "starter"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"
    CUSTOM = "custom"


class SatisfactionRating(Enum):
    """Customer satisfaction ratings."""
    VERY_DISSATISFIED = 1
    DISSATISFIED = 2
    NEUTRAL = 3
    SATISFIED = 4
    VERY_SATISFIED = 5


class EscalationLevel(Enum):
    """Support escalation levels."""
    L1 = "l1"
    L2 = "l2"
    L3 = "l3"
    MANAGEMENT = "management"
    EXECUTIVE = "executive"


class ChannelType(Enum):
    """Support channel types."""
    EMAIL = "email"
    CHAT = "chat"
    PHONE = "phone"
    SOCIAL = "social"
    API = "api"
    SELF_SERVICE = "self_service"


class SLAStatus(Enum):
    """SLA compliance status."""
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    BREACHED = "breached"
    NOT_APPLICABLE = "not_applicable"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Ticket:
    """Support ticket with full context."""
    id: str
    subject: str
    description: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    customer_id: str
    assignee_id: Optional[str]
    channel: ChannelType
    created_at: datetime
    updated_at: datetime
    first_response_at: Optional[datetime]
    resolved_at: Optional[datetime]
    tags: List[str]
    messages: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    sla_deadline: Optional[datetime] = None
    sla_status: SLAStatus = SLAStatus.NOT_APPLICABLE
    escalation_level: Optional[EscalationLevel] = None
    satisfaction_rating: Optional[SatisfactionRating] = None
    resolution_notes: str = ""

    def time_to_first_response(self) -> Optional[float]:
        """Hours to first response."""
        if self.first_response_at and self.created_at:
            return (self.first_response_at - self.created_at).total_seconds() / 3600
        return None

    def time_to_resolution(self) -> Optional[float]:
        """Hours to resolution."""
        if self.resolved_at and self.created_at:
            return (self.resolved_at - self.created_at).total_seconds() / 3600
        return None


@dataclass
class Customer:
    """Customer profile."""
    id: str
    name: str
    email: str
    company: Optional[str]
    tier: CustomerTier
    tickets_count: int
    satisfaction_score: float
    lifetime_value: float
    created_at: datetime
    last_activity: datetime
    tags: List[str]
    custom_fields: Dict[str, Any]


@dataclass
class KnowledgeArticle:
    """Knowledge base article."""
    id: str
    title: str
    content: str
    category: TicketCategory
    tags: List[str]
    author: str
    created_at: datetime
    updated_at: datetime
    views: int
    helpful_votes: int
    not_helpful_votes: int
    helpful_ratio: float = 0.0
    status: str = "published"

    def update_helpfulness(self) -> None:
        total = self.helpful_votes + self.not_helpful_votes
        self.helpful_ratio = self.helpful_votes / max(total, 1)


@dataclass
class SLAPolicy:
    """Service Level Agreement policy."""
    id: str
    name: str
    priority: TicketPriority
    tier: CustomerTier
    first_response_hours: float
    resolution_hours: float
    business_hours_only: bool
    description: str


@dataclass
class Escalation:
    """Escalation record."""
    id: str
    ticket_id: str
    from_level: EscalationLevel
    to_level: EscalationLevel
    reason: str
    escalated_by: str
    escalated_at: datetime
    acknowledged_at: Optional[datetime]
    notes: str = ""


@dataclass
class SupportMetrics:
    """Aggregate support metrics."""
    open_tickets: int
    avg_first_response_hours: float
    avg_resolution_hours: float
    satisfaction_score: float
    first_contact_resolution_rate: float
    sla_compliance_rate: float
    tickets_by_category: Dict[str, int]
    tickets_by_priority: Dict[str, int]
    tickets_by_status: Dict[str, int]
    total_tickets: int


@dataclass
class CSATSurvey:
    """Customer satisfaction survey."""
    id: str
    ticket_id: str
    customer_id: str
    rating: SatisfactionRating
    feedback: str
    nps_score: Optional[int]
    created_at: datetime


# ---------------------------------------------------------------------------
# Ticket Manager
# ---------------------------------------------------------------------------

class TicketManager:
    """Manages support ticket lifecycle."""

    def __init__(self, sla_policies: Optional[Dict[str, SLAPolicy]] = None) -> None:
        self.tickets: Dict[str, Ticket] = {}
        self.history: List[Dict[str, Any]] = []
        self.sla_policies = sla_policies or {}
        logger.info("TicketManager initialized")

    def create_ticket(self, subject: str, description: str,
                      category: TicketCategory, priority: TicketPriority,
                      customer_id: str, channel: ChannelType = ChannelType.EMAIL,
                      tags: Optional[List[str]] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> Ticket:
        """Create a new support ticket."""
        sla_deadline = self._calculate_sla_deadline(priority, customer_id)

        ticket = Ticket(
            id=f"TKT-{uuid.uuid4().hex[:8].upper()}",
            subject=subject,
            description=description,
            category=category,
            priority=priority,
            status=TicketStatus.OPEN,
            customer_id=customer_id,
            assignee_id=None,
            channel=channel,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            first_response_at=None,
            resolved_at=None,
            tags=tags or [],
            messages=[{
                "role": "customer",
                "content": description,
                "timestamp": datetime.now().isoformat(),
            }],
            metadata=metadata or {},
            sla_deadline=sla_deadline,
            sla_status=SLAStatus.ON_TRACK if sla_deadline else SLAStatus.NOT_APPLICABLE,
        )
        self.tickets[ticket.id] = ticket
        self._log_event(ticket.id, "created", {"status": "open", "priority": priority.name})
        logger.info("Ticket %s created: %s", ticket.id, subject)
        return ticket

    def _calculate_sla_deadline(self, priority: TicketPriority,
                                 customer_id: str) -> Optional[datetime]:
        """Calculate SLA deadline based on priority and tier."""
        sla_key = f"{priority.name}_DEFAULT"
        policy = self.sla_policies.get(sla_key)
        if not policy:
            return None
        return datetime.now() + timedelta(hours=policy.first_response_hours)

    def _log_event(self, ticket_id: str, action: str,
                   details: Dict[str, Any]) -> None:
        """Log ticket event."""
        self.history.append({
            "ticket_id": ticket_id,
            "action": action,
            "details": details,
            "timestamp": datetime.now().isoformat(),
        })

    def assign_ticket(self, ticket_id: str, assignee_id: str) -> Ticket:
        """Assign ticket to a support agent."""
        ticket = self._get_ticket(ticket_id)
        ticket.assignee_id = assignee_id
        ticket.status = TicketStatus.IN_PROGRESS
        ticket.updated_at = datetime.now()
        self._log_event(ticket_id, "assigned", {"assignee": assignee_id})
        return ticket

    def update_status(self, ticket_id: str, new_status: TicketStatus,
                      note: str = "") -> Ticket:
        """Update ticket status."""
        ticket = self._get_ticket(ticket_id)
        old_status = ticket.status
        ticket.status = new_status
        ticket.updated_at = datetime.now()

        if new_status == TicketStatus.RESOLVED:
            ticket.resolved_at = datetime.now()
        if note:
            ticket.messages.append({
                "role": "system",
                "content": f"Status changed: {old_status.value} -> {new_status.value}. {note}",
                "timestamp": datetime.now().isoformat(),
            })
        self._log_event(ticket_id, "status_changed", {
            "from": old_status.value, "to": new_status.value
        })
        return ticket

    def add_message(self, ticket_id: str, role: str, content: str,
                    agent_id: Optional[str] = None) -> Dict[str, Any]:
        """Add a message to the ticket."""
        ticket = self._get_ticket(ticket_id)
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "agent_id": agent_id,
        }
        ticket.messages.append(message)
        ticket.updated_at = datetime.now()

        if role == "agent" and ticket.first_response_at is None:
            ticket.first_response_at = datetime.now()

        return {"ticket_id": ticket_id, "message_count": len(ticket.messages)}

    def resolve_ticket(self, ticket_id: str,
                       resolution_notes: str = "") -> Ticket:
        """Resolve a ticket."""
        ticket = self._get_ticket(ticket_id)
        ticket.status = TicketStatus.RESOLVED
        ticket.resolved_at = datetime.now()
        ticket.updated_at = datetime.now()
        ticket.resolution_notes = resolution_notes
        self._log_event(ticket_id, "resolved", {"notes": resolution_notes[:100]})
        return ticket

    def close_ticket(self, ticket_id: str) -> Ticket:
        """Close a resolved ticket."""
        ticket = self._get_ticket(ticket_id)
        ticket.status = TicketStatus.CLOSED
        ticket.updated_at = datetime.now()
        self._log_event(ticket_id, "closed", {})
        return ticket

    def reopen_ticket(self, ticket_id: str, reason: str) -> Ticket:
        """Reopen a closed/resolved ticket."""
        ticket = self._get_ticket(ticket_id)
        ticket.status = TicketStatus.REOPENED
        ticket.resolved_at = None
        ticket.updated_at = datetime.now()
        ticket.messages.append({
            "role": "customer",
            "content": f"Reopened: {reason}",
            "timestamp": datetime.now().isoformat(),
        })
        self._log_event(ticket_id, "reopened", {"reason": reason})
        return ticket

    def _get_ticket(self, ticket_id: str) -> Ticket:
        """Get ticket or raise ValueError."""
        ticket = self.tickets.get(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket {ticket_id} not found")
        return ticket

    def get_by_status(self, status: TicketStatus) -> List[Ticket]:
        """Filter tickets by status."""
        return [t for t in self.tickets.values() if t.status == status]

    def get_by_priority(self, priority: TicketPriority) -> List[Ticket]:
        """Filter tickets by priority."""
        return [t for t in self.tickets.values() if t.priority == priority]

    def get_by_category(self, category: TicketCategory) -> List[Ticket]:
        """Filter tickets by category."""
        return [t for t in self.tickets.values() if t.category == category]

    def get_overdue(self, hours: int = 24) -> List[Ticket]:
        """Get tickets older than threshold that aren't resolved."""
        threshold = datetime.now() - timedelta(hours=hours)
        return [
            t for t in self.tickets.values()
            if t.created_at < threshold
            and t.status not in (TicketStatus.RESOLVED, TicketStatus.CLOSED)
        ]

    def check_sla(self) -> List[Dict[str, Any]]:
        """Check SLA compliance for all open tickets."""
        now = datetime.now()
        alerts = []
        for ticket in self.tickets.values():
            if ticket.status in (TicketStatus.RESOLVED, TicketStatus.CLOSED):
                continue
            if ticket.sla_deadline and ticket.sla_deadline < now:
                ticket.sla_status = SLAStatus.BREACHED
                alerts.append({
                    "ticket_id": ticket.id,
                    "status": "breached",
                    "deadline": ticket.sla_deadline.isoformat(),
                })
            elif ticket.sla_deadline:
                remaining = (ticket.sla_deadline - now).total_seconds() / 3600
                if remaining < 2:
                    ticket.sla_status = SLAStatus.AT_RISK
                    alerts.append({
                        "ticket_id": ticket.id,
                        "status": "at_risk",
                        "hours_remaining": round(remaining, 1),
                    })
        return alerts


# ---------------------------------------------------------------------------
# Knowledge Base
# ---------------------------------------------------------------------------

class KnowledgeBase:
    """Manages knowledge base articles and search."""

    def __init__(self) -> None:
        self.articles: Dict[str, KnowledgeArticle] = {}
        self.search_index: Dict[str, List[str]] = defaultdict(list)

    def add_article(self, title: str, content: str,
                    category: TicketCategory, tags: List[str],
                    author: str = "system") -> KnowledgeArticle:
        """Add a knowledge base article."""
        article = KnowledgeArticle(
            id=f"KB-{uuid.uuid4().hex[:8].upper()}",
            title=title,
            content=content,
            category=category,
            tags=tags,
            author=author,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            views=0,
            helpful_votes=0,
            not_helpful_votes=0,
        )
        self.articles[article.id] = article
        self._index_article(article)
        return article

    def _index_article(self, article: KnowledgeArticle) -> None:
        """Build search index for article."""
        words = re.findall(r"\w+", (article.title + " " + article.content).lower())
        for word in set(words):
            if len(word) > 2:
                self.search_index[word].append(article.id)

    def search(self, query: str, limit: int = 5) -> List[KnowledgeArticle]:
        """Search knowledge base by query."""
        query_words = re.findall(r"\w+", query.lower())
        scores: Dict[str, int] = defaultdict(int)

        for word in query_words:
            for article_id in self.search_index.get(word, []):
                scores[article_id] += 1

        sorted_ids = sorted(scores.items(), key=lambda x: -x[1])[:limit]
        results = []
        for article_id, score in sorted_ids:
            article = self.articles.get(article_id)
            if article and article.status == "published":
                results.append(article)
        return results

    def record_view(self, article_id: str) -> None:
        """Record article view."""
        if article_id in self.articles:
            self.articles[article_id].views += 1

    def vote_helpful(self, article_id: str, helpful: bool) -> None:
        """Record helpfulness vote."""
        article = self.articles.get(article_id)
        if article:
            if helpful:
                article.helpful_votes += 1
            else:
                article.not_helpful_votes += 1
            article.update_helpfulness()

    def get_top_articles(self, limit: int = 10) -> List[KnowledgeArticle]:
        """Get most viewed articles."""
        return sorted(self.articles.values(), key=lambda a: -a.views)[:limit]

    def get_by_category(self, category: TicketCategory) -> List[KnowledgeArticle]:
        """Get articles by category."""
        return [a for a in self.articles.values() if a.category == category]


# ---------------------------------------------------------------------------
# Response Engine
# ---------------------------------------------------------------------------

class ResponseEngine:
    """Generates automated and templated support responses."""

    def __init__(self, knowledge_base: KnowledgeBase) -> None:
        self.kb = knowledge_base
        self.templates: Dict[str, Dict[str, Any]] = {}
        self.response_history: List[Dict[str, Any]] = []
        self._init_default_templates()

    def _init_default_templates(self) -> None:
        """Initialize default response templates."""
        self.templates = {
            "acknowledgment": {
                "template": "Thank you for contacting support. We've received your request ({{ticket_id}}) and our team will respond within {{sla_hours}} hours.",
                "variables": ["ticket_id", "sla_hours"],
            },
            "escalation_notice": {
                "template": "Your request has been escalated to our {{level}} support team. A specialist will review your case shortly.",
                "variables": ["level"],
            },
            "resolution": {
                "template": "Your issue has been resolved: {{resolution}}. If you need further assistance, please reopen this ticket.",
                "variables": ["resolution"],
            },
            "follow_up": {
                "template": "We wanted to follow up on your recent support request. Has your issue been fully resolved?",
                "variables": [],
            },
        }

    def add_template(self, name: str, template: str,
                     variables: Optional[List[str]] = None) -> None:
        """Add a custom response template."""
        self.templates[name] = {
            "template": template,
            "variables": variables or re.findall(r"\{\{(\w+)\}\}", template),
        }

    def generate_response(self, ticket_id: str,
                          response_type: ResponseType = ResponseType.AUTOMATED,
                          template_name: Optional[str] = None,
                          variables: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """Generate a response for a ticket."""
        if response_type == ResponseType.TEMPLATED and template_name:
            return self._render_template(template_name, variables or {}, ticket_id)

        if response_type == ResponseType.KNOWLEDGE_BASE:
            return self._kb_response(ticket_id)

        if response_type == ResponseType.AUTOMATED:
            return self._auto_response(ticket_id)

        return {"type": "manual", "content": "This requires manual agent intervention."}

    def _render_template(self, name: str, variables: Dict[str, str],
                         ticket_id: str) -> Dict[str, Any]:
        """Render a template with variables."""
        tmpl = self.templates.get(name)
        if not tmpl:
            return {"type": "error", "content": f"Template {name} not found"}

        content = tmpl["template"]
        for key, value in variables.items():
            content = content.replace(f"{{{{{key}}}}}", value)

        self.response_history.append({
            "ticket_id": ticket_id, "type": "templated", "template": name
        })
        return {"type": "templated", "content": content, "template": name}

    def _kb_response(self, ticket_id: str) -> Dict[str, Any]:
        """Find and return relevant KB article."""
        articles = self.kb.search(ticket_id, limit=1)
        if articles:
            article = articles[0]
            self.kb.record_view(article.id)
            self.response_history.append({
                "ticket_id": ticket_id, "type": "kb", "article": article.id
            })
            return {
                "type": "knowledge_base",
                "content": f"Here's a helpful article:\n\n{article.title}\n\n{article.content[:500]}",
                "article_id": article.id,
            }
        return {"type": "escalated", "content": "No matching knowledge base article found. Escalating to agent."}

    def _auto_response(self, ticket_id: str) -> Dict[str, Any]:
        """Generate automated acknowledgment."""
        tmpl = self.templates.get("acknowledgment")
        if tmpl:
            content = tmpl["template"].replace("{{ticket_id}}", ticket_id).replace("{{sla_hours}}", "24")
            return {"type": "automated", "content": content}
        return {"type": "automated", "content": f"Ticket {ticket_id} received. We'll respond soon."}


# ---------------------------------------------------------------------------
# Escalation Manager
# ---------------------------------------------------------------------------

class EscalationManager:
    """Manages ticket escalation workflows."""

    def __init__(self) -> None:
        self.escalations: List[Escalation] = []
        self.escalation_rules: List[Dict[str, Any]] = []
        self._init_default_rules()

    def _init_default_rules(self) -> None:
        """Initialize default escalation rules."""
        self.escalation_rules = [
            {"condition": "priority == CRITICAL", "action": "escalate_to_l3", "immediate": True},
            {"condition": "hours_open > 4 AND priority == HIGH", "action": "escalate_to_l2"},
            {"condition": "hours_open > 24 AND status == OPEN", "action": "escalate_to_l2"},
            {"condition": "customer_tier == ENTERPRISE AND priority >= HIGH", "action": "escalate_to_l2", "immediate": True},
        ]

    def escalate_ticket(self, ticket_id: str, from_level: EscalationLevel,
                        to_level: EscalationLevel, reason: str,
                        escalated_by: str = "system",
                        notes: str = "") -> Escalation:
        """Escalate a ticket to a higher level."""
        escalation = Escalation(
            id=f"ESC-{uuid.uuid4().hex[:8].upper()}",
            ticket_id=ticket_id,
            from_level=from_level,
            to_level=to_level,
            reason=reason,
            escalated_by=escalated_by,
            escalated_at=datetime.now(),
            acknowledged_at=None,
            notes=notes,
        )
        self.escalations.append(escalation)
        logger.info("Ticket %s escalated %s -> %s: %s", ticket_id, from_level.value, to_level.value, reason)
        return escalation

    def acknowledge_escalation(self, escalation_id: str,
                               notes: str = "") -> Dict[str, Any]:
        """Acknowledge an escalation."""
        for esc in self.escalations:
            if esc.id == escalation_id:
                esc.acknowledged_at = datetime.now()
                if notes:
                    esc.notes = notes
                return {"escalation_id": escalation_id, "acknowledged": True}
        return {"error": f"Escalation {escalation_id} not found"}

    def check_escalation_rules(self, ticket: Any) -> Optional[Dict[str, Any]]:
        """Check if ticket triggers any escalation rules."""
        for rule in self.escalation_rules:
            if self._evaluate_rule(rule, ticket):
                return rule
        return None

    def _evaluate_rule(self, rule: Dict[str, Any], ticket: Any) -> bool:
        """Evaluate an escalation rule against a ticket."""
        condition = rule.get("condition", "")
        if "priority == CRITICAL" in condition and ticket.priority == TicketPriority.CRITICAL:
            return True
        if "hours_open > 24" in condition:
            hours = (datetime.now() - ticket.created_at).total_seconds() / 3600
            if hours > 24 and ticket.status not in (TicketStatus.RESOLVED, TicketStatus.CLOSED):
                return True
        return False

    def get_escalation_history(self, ticket_id: Optional[str] = None) -> List[Escalation]:
        """Get escalation history, optionally filtered by ticket."""
        if ticket_id:
            return [e for e in self.escalations if e.ticket_id == ticket_id]
        return self.escalations


# ---------------------------------------------------------------------------
# Customer Manager
# ---------------------------------------------------------------------------

class CustomerManager:
    """Manages customer profiles and history."""

    def __init__(self) -> None:
        self.customers: Dict[str, Customer] = {}
        self.interactions: List[Dict[str, Any]] = []

    def add_customer(self, name: str, email: str,
                     company: Optional[str] = None,
                     tier: CustomerTier = CustomerTier.FREE) -> Customer:
        """Add or retrieve existing customer."""
        existing = self.get_by_email(email)
        if existing:
            return existing

        customer = Customer(
            id=f"CUST-{uuid.uuid4().hex[:8].upper()}",
            name=name,
            email=email,
            company=company,
            tier=tier,
            tickets_count=0,
            satisfaction_score=5.0,
            lifetime_value=0.0,
            created_at=datetime.now(),
            last_activity=datetime.now(),
            tags=[],
            custom_fields={},
        )
        self.customers[customer.id] = customer
        return customer

    def get_by_email(self, email: str) -> Optional[Customer]:
        """Find customer by email."""
        for c in self.customers.values():
            if c.email == email:
                return c
        return None

    def get_by_id(self, customer_id: str) -> Optional[Customer]:
        """Find customer by ID."""
        return self.customers.get(customer_id)

    def update_satisfaction(self, customer_id: str,
                            score: SatisfactionRating) -> None:
        """Update customer satisfaction (rolling average)."""
        customer = self.customers.get(customer_id)
        if customer:
            customer.satisfaction_score = round(
                (customer.satisfaction_score + score.value) / 2, 2
            )
            customer.last_activity = datetime.now()

    def get_customer_history(self, customer_id: str) -> Dict[str, Any]:
        """Get customer interaction history."""
        customer = self.customers.get(customer_id)
        if not customer:
            return {"error": "Customer not found"}
        return {
            "customer": {
                "id": customer.id,
                "name": customer.name,
                "tier": customer.tier.value,
                "satisfaction": customer.satisfaction_score,
            },
            "tickets_count": customer.tickets_count,
            "lifetime_value": customer.lifetime_value,
        }

    def get_by_tier(self, tier: CustomerTier) -> List[Customer]:
        """Get customers by tier."""
        return [c for c in self.customers.values() if c.tier == tier]


# ---------------------------------------------------------------------------
# Support Analytics
# ---------------------------------------------------------------------------

class SupportAnalytics:
    """Calculates support performance metrics and generates reports."""

    def __init__(self, tickets: TicketManager, customers: CustomerManager) -> None:
        self.tickets = tickets
        self.customers = customers

    def calculate_metrics(self) -> SupportMetrics:
        """Calculate all support metrics."""
        all_tickets = list(self.tickets.tickets.values())
        open_count = sum(1 for t in all_tickets if t.status in (
            TicketStatus.OPEN, TicketStatus.IN_PROGRESS, TicketStatus.WAITING_ON_CUSTOMER
        ))

        ttr_values = [t.time_to_resolution() for t in all_tickets if t.resolved_at]
        ttfr_values = [t.time_to_first_response() for t in all_tickets if t.first_response_at]

        avg_ttr = sum(ttr_values) / max(len(ttr_values), 1)
        avg_ttfr = sum(ttfr_values) / max(len(ttfr_values), 1)

        by_category = defaultdict(int)
        by_priority = defaultdict(int)
        by_status = defaultdict(int)
        for t in all_tickets:
            by_category[t.category.value] += 1
            by_priority[t.priority.name] += 1
            by_status[t.status.value] += 1

        avg_sat = 0.0
        if self.customers.customers:
            avg_sat = sum(c.satisfaction_score for c in self.customers.customers.values()) / len(self.customers.customers)

        fcr = sum(1 for t in all_tickets if t.satisfaction_rating and t.satisfaction_rating.value >= 4) / max(len(all_tickets), 1)

        sla_compliant = sum(1 for t in all_tickets if t.sla_status == SLAStatus.ON_TRACK)
        sla_total = sum(1 for t in all_tickets if t.sla_status != SLAStatus.NOT_APPLICABLE)
        sla_rate = sla_compliant / max(sla_total, 1)

        return SupportMetrics(
            open_tickets=open_count,
            avg_first_response_hours=round(avg_ttfr, 2),
            avg_resolution_hours=round(avg_ttr, 2),
            satisfaction_score=round(avg_sat, 2),
            first_contact_resolution_rate=round(fcr, 4),
            sla_compliance_rate=round(sla_rate, 4),
            tickets_by_category=dict(by_category),
            tickets_by_priority=dict(by_priority),
            tickets_by_status=dict(by_status),
            total_tickets=len(all_tickets),
        )

    def generate_report(self, start_date: Optional[datetime] = None,
                        end_date: Optional[datetime] = None) -> Dict[str, Any]:
        """Generate comprehensive support report."""
        metrics = self.calculate_metrics()
        overdue = self.tickets.get_overdue()
        critical = self.tickets.get_by_priority(TicketPriority.CRITICAL)
        top_issues = sorted(metrics.tickets_by_category.items(), key=lambda x: -x[1])[:5]

        return {
            "period": {
                "start": (start_date or datetime.now() - timedelta(days=30)).isoformat(),
                "end": (end_date or datetime.now()).isoformat(),
            },
            "summary": {
                "total_tickets": metrics.total_tickets,
                "open_tickets": metrics.open_tickets,
                "avg_first_response_hours": metrics.avg_first_response_hours,
                "avg_resolution_hours": metrics.avg_resolution_hours,
                "satisfaction_score": f"{metrics.satisfaction_score}/5",
                "sla_compliance": f"{metrics.sla_compliance_rate * 100:.1f}%",
            },
            "alerts": {
                "overdue_count": len(overdue),
                "critical_count": len(critical),
                "sla_breaches": sum(1 for t in self.tickets.tickets.values() if t.sla_status == SLAStatus.BREACHED),
            },
            "top_issues": dict(top_issues),
            "recommendations": self._generate_recommendations(metrics),
        }

    def _generate_recommendations(self, metrics: SupportMetrics) -> List[str]:
        """Generate actionable recommendations."""
        recs: List[str] = []
        if metrics.satisfaction_score < 4.0:
            recs.append("Customer satisfaction below target - review response quality and tone")
        if metrics.first_contact_resolution_rate < 0.7:
            recs.append("FCR below 70% - enhance knowledge base and agent training")
        if metrics.sla_compliance_rate < 0.9:
            recs.append("SLA compliance below 90% - review staffing and triage process")
        if metrics.open_tickets > 50:
            recs.append("High open ticket count - consider additional support capacity")
        if metrics.avg_first_response_hours > 4:
            recs.append("First response time exceeds 4h - implement auto-acknowledgments")
        recs.extend([
            "Implement proactive outreach for at-risk customers",
            "Regular knowledge base content audits",
            "Review escalation rules quarterly",
        ])
        return recs


# ---------------------------------------------------------------------------
# Support Agent (Orchestrator)
# ---------------------------------------------------------------------------

class SupportAgent:
    """Top-level customer support operations agent."""

    def __init__(self) -> None:
        self.tickets = TicketManager()
        self.kb = KnowledgeBase()
        self.response = ResponseEngine(self.kb)
        self.escalation = EscalationManager()
        self.customers = CustomerManager()
        self.analytics = SupportAnalytics(self.tickets, self.customers)
        logger.info("SupportAgent initialized")

    def handle_incoming_ticket(self, subject: str, description: str,
                               category: str, priority: str,
                               customer_email: str,
                               **kwargs) -> Dict[str, Any]:
        """Handle a new incoming support ticket."""
        customer = self.customers.add_customer(
            name=kwargs.get("customer_name", "Unknown"),
            email=customer_email,
            company=kwargs.get("company"),
            tier=CustomerTier[kwargs.get("tier", "FREE").upper()],
        )

        ticket = self.tickets.create_ticket(
            subject=subject,
            description=description,
            category=TicketCategory[category.upper()],
            priority=TicketPriority[int(priority)],
            customer_id=customer.id,
            channel=ChannelType[kwargs.get("channel", "EMAIL").upper()],
            tags=kwargs.get("tags", []),
            metadata=kwargs.get("metadata", {}),
        )

        customer.tickets_count += 1
        customer.last_activity = datetime.now()

        auto_response = self.response.generate_response(
            ticket.id, ResponseType.AUTOMATED
        )
        self.tickets.add_message(ticket.id, "agent", auto_response["content"])

        # Check escalation
        rule = self.escalation.check_escalation_rules(ticket)
        if rule:
            self.escalation.escalate_ticket(
                ticket.id, EscalationLevel.L1, EscalationLevel.L2,
                reason=rule.get("condition", "Auto-escalation")
            )
            ticket.escalation_level = EscalationLevel.L2

        return {
            "ticket_id": ticket.id,
            "customer_id": customer.id,
            "status": ticket.status.value,
            "sla_deadline": ticket.sla_deadline.isoformat() if ticket.sla_deadline else None,
            "response_type": auto_response["type"],
        }

    def generate_auto_response(self, ticket_id: str) -> Dict[str, Any]:
        """Generate an automatic response for a ticket."""
        ticket = self.tickets.tickets.get(ticket_id)
        if not ticket:
            return {"error": "Ticket not found"}
        return self.response.generate_response(ticket_id, ResponseType.AUTOMATED)

    def escalate_ticket(self, ticket_id: str, reason: str,
                        escalate_to: str = "l2") -> Dict[str, Any]:
        """Escalate a ticket."""
        ticket = self.tickets.tickets.get(ticket_id)
        if not ticket:
            return {"error": "Ticket not found"}

        to_level = EscalationLevel(escalate_to)
        from_level = ticket.escalation_level or EscalationLevel.L1
        self.escalation.escalate_ticket(ticket_id, from_level, to_level, reason)
        ticket.escalation_level = to_level
        ticket.status = TicketStatus.ESCALATED
        ticket.updated_at = datetime.now()

        return {"ticket_id": ticket_id, "escalated_to": escalate_to, "status": "escalated"}

    def resolve_ticket(self, ticket_id: str,
                       resolution_notes: str = "") -> Dict[str, Any]:
        """Resolve a ticket."""
        ticket = self.tickets.resolve_ticket(ticket_id, resolution_notes)
        return {
            "ticket_id": ticket_id,
            "status": "resolved",
            "resolution_time_hours": ticket.time_to_resolution(),
        }

    def submit_satisfaction(self, ticket_id: str, rating: int,
                            feedback: str = "",
                            nps_score: Optional[int] = None) -> Dict[str, Any]:
        """Submit customer satisfaction feedback."""
        ticket = self.tickets.tickets.get(ticket_id)
        if not ticket:
            return {"error": "Ticket not found"}

        sat_rating = SatisfactionRating(max(1, min(5, rating)))
        ticket.satisfaction_rating = sat_rating
        self.customers.update_satisfaction(ticket.customer_id, sat_rating)

        survey = CSATSurvey(
            id=f"CSAT-{uuid.uuid4().hex[:8].upper()}",
            ticket_id=ticket_id,
            customer_id=ticket.customer_id,
            rating=sat_rating,
            feedback=feedback,
            nps_score=nps_score,
            created_at=datetime.now(),
        )
        return {"survey_id": survey.id, "rating": sat_rating.value, "feedback": feedback}

    def search_knowledge_base(self, query: str) -> List[Dict[str, Any]]:
        """Search knowledge base articles."""
        articles = self.kb.search(query)
        return [
            {"id": a.id, "title": a.title, "helpful_ratio": a.helpful_ratio, "views": a.views}
            for a in articles
        ]

    def get_support_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive support dashboard."""
        metrics = self.analytics.calculate_metrics()
        sla_alerts = self.tickets.check_sla()

        return {
            "timestamp": datetime.now().isoformat(),
            "queue": {
                "open": metrics.open_tickets,
                "critical": len(self.tickets.get_by_priority(TicketPriority.CRITICAL)),
                "overdue": len(self.tickets.get_overdue()),
            },
            "metrics": {
                "avg_first_response_hours": metrics.avg_first_response_hours,
                "avg_resolution_hours": metrics.avg_resolution_hours,
                "satisfaction_score": metrics.satisfaction_score,
                "first_contact_resolution": f"{metrics.first_contact_resolution_rate * 100:.1f}%",
                "sla_compliance": f"{metrics.sla_compliance_rate * 100:.1f}%",
            },
            "sla_alerts": sla_alerts,
            "by_category": metrics.tickets_by_category,
            "by_priority": metrics.tickets_by_priority,
            "knowledge_base": {
                "total_articles": len(self.kb.articles),
                "top_articles": [{"id": a.id, "title": a.title, "views": a.views} for a in self.kb.get_top_articles(5)],
            },
            "escalations": {
                "total": len(self.escalation.escalations),
                "unacknowledged": sum(1 for e in self.escalation.escalations if not e.acknowledged_at),
            },
            "recommendations": self.analytics._generate_recommendations(metrics),
        }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate SupportAgent capabilities."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    print("\n" + "=" * 60)
    print("  Support Agent - Customer Support Operations")
    print("=" * 60 + "\n")

    agent = SupportAgent()

    # Add knowledge base articles
    agent.kb.add_article(
        title="How to Reset Your Password",
        content="Go to Settings > Security > Change Password. Enter your current password and new password.",
        category=TicketCategory.ACCOUNT,
        tags=["password", "reset", "account"],
    )
    agent.kb.add_article(
        title="Billing FAQ",
        content="View invoices at Billing > History. Update payment method at Billing > Payment Methods.",
        category=TicketCategory.BILLING,
        tags=["billing", "invoice", "payment"],
    )

    # Handle incoming ticket
    result = agent.handle_incoming_ticket(
        subject="Cannot login to my account",
        description="I've been trying to login but keep getting an error. I've reset my password but it still doesn't work.",
        category="technical",
        priority="2",
        customer_email="user@example.com",
        customer_name="John Doe",
        company="Acme Corp",
        tier="professional",
    )
    print(f"Ticket created: {result['ticket_id']}")
    print(f"  Status: {result['status']}")
    print(f"  SLA deadline: {result['sla_deadline']}")

    # Search KB
    kb_results = agent.search_knowledge_base("password reset")
    print(f"\nKB Search results: {len(kb_results)} articles found")

    # Escalate
    escalation = agent.escalate_ticket(result["ticket_id"], "Complex auth issue", "l3")
    print(f"Escalated: {escalation}")

    # Dashboard
    dashboard = agent.get_support_dashboard()
    print(f"\nDashboard:")
    print(f"  Open tickets: {dashboard['queue']['open']}")
    print(f"  SLA compliance: {dashboard['metrics']['sla_compliance']}")
    print(f"  Satisfaction: {dashboard['metrics']['satisfaction_score']}/5")
    print(f"  KB articles: {dashboard['knowledge_base']['total_articles']}")
    print()


if __name__ == "__main__":
    main()

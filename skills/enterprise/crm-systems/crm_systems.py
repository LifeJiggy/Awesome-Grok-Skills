"""
CRM Systems Framework

Production-grade CRM toolkit providing contact management, sales pipeline,
marketing automation, customer service, and CRM analytics.
"""

from __future__ import annotations

import hashlib
import json
import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Tuple

import numpy as np
from numpy.typing import NDArray

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DealStage(Enum):
    PROSPECTING = "prospecting"
    QUALIFICATION = "qualification"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"


class TicketPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    RESOLVED = "resolved"
    CLOSED = "closed"


class CampaignType(Enum):
    EMAIL = "email"
    SOCIAL = "social"
    ADS = "ads"
    WEBINAR = "webinar"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Contact:
    """Customer contact."""
    id: str = ""
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    company: str = ""
    title: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@dataclass
class Deal:
    """Sales deal."""
    id: str = ""
    title: str = ""
    contact_id: str = ""
    value: float = 0.0
    stage: DealStage = DealStage.PROSPECTING
    expected_close: str = ""
    probability: float = 0.0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Campaign:
    """Marketing campaign."""
    id: str = ""
    name: str = ""
    type: CampaignType = CampaignType.EMAIL
    target_segment: str = ""
    content: Dict[str, Any] = field(default_factory=dict)
    status: str = "draft"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class Ticket:
    """Service ticket."""
    id: str = ""
    subject: str = ""
    customer_email: str = ""
    priority: TicketPriority = TicketPriority.MEDIUM
    status: TicketStatus = TicketStatus.OPEN
    category: str = ""
    assigned_to: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class SalesMetrics:
    """Sales performance metrics."""
    total_pipeline_value: float = 0.0
    weighted_pipeline: float = 0.0
    deals_won: int = 0
    deals_lost: int = 0
    win_rate: float = 0.0
    avg_deal_size: float = 0.0
    avg_sales_cycle_days: float = 0.0


@dataclass
class CustomerMetrics:
    """Customer analytics metrics."""
    customer_id: str = ""
    lifetime_value: float = 0.0
    churn_risk: float = 0.0
    satisfaction_score: float = 0.0
    last_interaction: Optional[datetime] = None
    total_interactions: int = 0


# ---------------------------------------------------------------------------
# Contact Manager
# ---------------------------------------------------------------------------

class ContactManager:
    """Manage customer contacts."""

    def __init__(self):
        self._contacts: Dict[str, Contact] = {}

    def create_contact(self, contact: Contact) -> Contact:
        contact.id = hashlib.md5(f"{contact.email}:{time.time()}".encode()).hexdigest()[:8]
        self._contacts[contact.id] = contact
        return contact

    def get_contact(self, contact_id: str) -> Optional[Contact]:
        return self._contacts.get(contact_id)

    def search_contacts(self, query: str) -> List[Contact]:
        return [c for c in self._contacts.values()
                if query.lower() in c.full_name.lower() or query.lower() in c.email.lower()]

    def list_contacts(self, tag: Optional[str] = None) -> List[Contact]:
        contacts = list(self._contacts.values())
        if tag:
            contacts = [c for c in contacts if tag in c.tags]
        return contacts


# ---------------------------------------------------------------------------
# Sales Pipeline
# ---------------------------------------------------------------------------

class SalesPipeline:
    """Manage sales pipeline."""

    def __init__(self):
        self._deals: Dict[str, Deal] = {}

    def create_deal(self, title: str, contact_id: str, value: float,
                    stage: DealStage = DealStage.PROSPECTING,
                    expected_close: str = "") -> Deal:
        deal_id = hashlib.md5(f"{title}:{time.time()}".encode()).hexdigest()[:8]
        deal = Deal(
            id=deal_id, title=title, contact_id=contact_id,
            value=value, stage=stage, expected_close=expected_close,
        )
        self._deals[deal_id] = deal
        return deal

    def advance_deal(self, deal_id: str, new_stage: DealStage) -> Optional[Deal]:
        if deal_id in self._deals:
            self._deals[deal_id].stage = new_stage
            return self._deals[deal_id]
        return None

    def get_pipeline_metrics(self) -> SalesMetrics:
        deals = list(self._deals.values())
        won = [d for d in deals if d.stage == DealStage.CLOSED_WON]
        lost = [d for d in deals if d.stage == DealStage.CLOSED_LOST]

        return SalesMetrics(
            total_pipeline_value=sum(d.value for d in deals),
            weighted_pipeline=sum(d.value * d.probability for d in deals),
            deals_won=len(won),
            deals_lost=len(lost),
            win_rate=len(won) / max(len(won) + len(lost), 1),
            avg_deal_size=np.mean([d.value for d in deals]) if deals else 0,
        )


# ---------------------------------------------------------------------------
# Marketing Automation
# ---------------------------------------------------------------------------

class MarketingAutomation:
    """Manage marketing campaigns."""

    def __init__(self):
        self._campaigns: Dict[str, Campaign] = {}

    def create_campaign(self, campaign: Campaign) -> Campaign:
        campaign.id = hashlib.md5(f"{campaign.name}:{time.time()}".encode()).hexdigest()[:8]
        self._campaigns[campaign.id] = campaign
        return campaign

    def get_campaign(self, campaign_id: str) -> Optional[Campaign]:
        return self._campaigns.get(campaign_id)

    def list_campaigns(self) -> List[Campaign]:
        return list(self._campaigns.values())


# ---------------------------------------------------------------------------
# Service Desk
# ---------------------------------------------------------------------------

class ServiceDesk:
    """Manage customer service tickets."""

    def __init__(self):
        self._tickets: Dict[str, Ticket] = {}

    def create_ticket(self, ticket: Ticket) -> Ticket:
        ticket.id = hashlib.md5(f"{ticket.subject}:{time.time()}".encode()).hexdigest()[:8]
        self._tickets[ticket.id] = ticket
        return ticket

    def update_ticket(self, ticket_id: str, status: Optional[TicketStatus] = None,
                      assigned_to: Optional[str] = None) -> Optional[Ticket]:
        if ticket_id in self._tickets:
            ticket = self._tickets[ticket_id]
            if status:
                ticket.status = status
            if assigned_to:
                ticket.assigned_to = assigned_to
            return ticket
        return None

    def get_open_tickets(self) -> List[Ticket]:
        return [t for t in self._tickets.values() if t.status == TicketStatus.OPEN]


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate CRM systems capabilities."""
    print("=" * 70)
    print("CRM Systems Framework - Demo")
    print("=" * 70)

    # --- 1. Contact Management ---
    print("\n--- Contact Management ---")
    contact_mgr = ContactManager()
    contact = contact_mgr.create_contact(Contact(
        first_name="John", last_name="Doe",
        email="john@company.com", company="Acme Corp",
        tags=["enterprise", "decision-maker"],
    ))
    print(f"  Contact: {contact.full_name}")
    print(f"  Email: {contact.email}")
    print(f"  Company: {contact.company}")

    # --- 2. Sales Pipeline ---
    print("\n--- Sales Pipeline ---")
    pipeline = SalesPipeline()
    deal = pipeline.create_deal("Enterprise License", contact.id, 50000)
    print(f"  Deal: {deal.title}")
    print(f"  Value: ${deal.value:,.2f}")
    print(f"  Stage: {deal.stage.value}")

    pipeline.advance_deal(deal.id, DealStage.PROPOSAL)
    metrics = pipeline.get_pipeline_metrics()
    print(f"  Pipeline value: ${metrics.total_pipeline_value:,.2f}")

    # --- 3. Marketing ---
    print("\n--- Marketing Automation ---")
    marketing = MarketingAutomation()
    campaign = marketing.create_campaign(Campaign(
        name="Q1 Launch", type=CampaignType.EMAIL,
        target_segment="enterprise",
    ))
    print(f"  Campaign: {campaign.name}")
    print(f"  Type: {campaign.type.value}")
    print(f"  Target: {campaign.target_segment}")

    # --- 4. Customer Service ---
    print("\n--- Customer Service ---")
    desk = ServiceDesk()
    ticket = desk.create_ticket(Ticket(
        subject="Login issue", customer_email="customer@company.com",
        priority=TicketPriority.HIGH,
    ))
    print(f"  Ticket: {ticket.id}")
    print(f"  Priority: {ticket.priority.value}")
    print(f"  Status: {ticket.status.value}")

    open_tickets = desk.get_open_tickets()
    print(f"  Open tickets: {len(open_tickets)}")

    print("\n" + "=" * 70)
    print("Demo complete.")
    print("=" * 70)


if __name__ == "__main__":
    main()
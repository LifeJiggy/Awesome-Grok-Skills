#!/usr/bin/env python3
"""
Grok Support Agent
Specialized agent for customer support, ticket management, and service automation.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import uuid
from collections import defaultdict

class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    WAITING = "waiting"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TicketPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class TicketCategory(Enum):
    BUG = "bug"
    FEATURE_REQUEST = "feature_request"
    QUESTION = "question"
    ACCOUNT = "account"
    BILLING = "billing"
    TECHNICAL = "technical"
    GENERAL = "general"

class ResponseType(Enum):
    AUTOMATED = "automated"
    TEMPLATED = "templated"
    ESCALATED = "escalated"
    MANUAL = "manual"

@dataclass
class Ticket:
    id: str
    subject: str
    description: str
    category: TicketCategory
    priority: TicketPriority
    status: TicketStatus
    customer_id: str
    assignee_id: Optional[str]
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime]
    tags: List[str]
    messages: List[Dict]
    metadata: Dict[str, Any]

@dataclass
class Customer:
    id: str
    name: str
    email: str
    company: Optional[str]
    tier: str
    tickets_count: int
    satisfaction_score: float
    lifetime_value: float
    created_at: datetime

@dataclass
class SupportMetrics:
    open_tickets: int
    avg_response_time: float
    avg_resolution_time: float
    satisfaction_score: float
    first_contact_resolution: float
    tickets_by_category: Dict[str, int]
    tickets_by_priority: Dict[str, int]

class TicketManager:
    """Manages support tickets."""
    
    def __init__(self):
        self.tickets: Dict[str, Ticket] = {}
        self.ticket_history: List[Dict] = []
    
    def create_ticket(self, subject: str, description: str,
                     category: TicketCategory, priority: TicketPriority,
                     customer_id: str, tags: List[str] = None,
                     metadata: Dict[str, Any] = None) -> Ticket:
        """Create new support ticket."""
        ticket = Ticket(
            id=str(uuid.uuid4())[:8],
            subject=subject,
            description=description,
            category=category,
            priority=priority,
            status=TicketStatus.OPEN,
            customer_id=customer_id,
            assignee_id=None,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            resolved_at=None,
            tags=tags or [],
            messages=[{'role': 'customer', 'content': description, 'timestamp': datetime.now()}],
            metadata=metadata or {}
        )
        self.tickets[ticket.id] = ticket
        self._log_history(ticket.id, 'created', {'status': 'open'})
        return ticket
    
    def _log_history(self, ticket_id: str, action: str, details: Dict) -> None:
        """Log ticket history."""
        self.ticket_history.append({
            'ticket_id': ticket_id,
            'action': action,
            'details': details,
            'timestamp': datetime.now()
        })
    
    def assign_ticket(self, ticket_id: str, assignee_id: str) -> Ticket:
        """Assign ticket to agent."""
        if ticket_id not in self.tickets:
            raise ValueError(f"Ticket {ticket_id} not found")
        
        ticket = self.tickets[ticket_id]
        ticket.assignee_id = assignee_id
        ticket.status = TicketStatus.IN_PROGRESS
        ticket.updated_at = datetime.now()
        self._log_history(ticket_id, 'assigned', {'assignee': assignee_id})
        return ticket
    
    def update_ticket(self, ticket_id: str, **updates) -> Ticket:
        """Update ticket properties."""
        if ticket_id not in self.tickets:
            raise ValueError(f"Ticket {ticket_id} not found")
        
        ticket = self.tickets[ticket_id]
        
        for key, value in updates.items():
            if hasattr(ticket, key):
                setattr(ticket, key, value)
        
        ticket.updated_at = datetime.now()
        self._log_history(ticket_id, 'updated', updates)
        return ticket
    
    def add_message(self, ticket_id: str, role: str, content: str) -> None:
        """Add message to ticket."""
        if ticket_id not in self.tickets:
            raise ValueError(f"Ticket {ticket_id} not found")
        
        ticket = self.tickets[ticket_id]
        ticket.messages.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now()
        })
        ticket.updated_at = datetime.now()
    
    def resolve_ticket(self, ticket_id: str, resolution: str = None) -> Ticket:
        """Resolve ticket."""
        if ticket_id not in self.tickets:
            raise ValueError(f"Ticket {ticket_id} not found")
        
        ticket = self.tickets[ticket_id]
        ticket.status = TicketStatus.RESOLVED
        ticket.resolved_at = datetime.now()
        ticket.updated_at = datetime.now()
        
        if resolution:
            self.add_message(ticket_id, 'system', f"Resolved: {resolution}")
        
        self._log_history(ticket_id, 'resolved', {'resolution': resolution})
        return ticket
    
    def get_tickets_by_status(self, status: TicketStatus) -> List[Ticket]:
        """Get tickets by status."""
        return [t for t in self.tickets.values() if t.status == status]
    
    def get_tickets_by_priority(self, priority: TicketPriority) -> List[Ticket]:
        """Get tickets by priority."""
        return [t for t in self.tickets.values() if t.priority == priority]
    
    def get_overdue_tickets(self, hours: int = 24) -> List[Ticket]:
        """Get overdue tickets."""
        threshold = datetime.now() - timedelta(hours=hours)
        return [t for t in self.tickets.values() 
               if t.created_at < threshold and t.status not in [TicketStatus.RESOLVED, TicketStatus.CLOSED]]

class ResponseEngine:
    """Generates support responses."""
    
    def __init__(self):
        self.templates: Dict[str, Dict] = {}
        self.knowledge_base: Dict[str, Dict] = {}
        self.response_history = []
    
    def add_template(self, name: str, template: str, 
                    category: TicketCategory = None) -> None:
        """Add response template."""
        self.templates[name] = {
            'template': template,
            'category': category,
            'variables': self._extract_variables(template)
        }
    
    def _extract_variables(self, template: str) -> List[str]:
        """Extract variables from template."""
        import re
        return re.findall(r'\{\{(\w+)\}\}', template)
    
    def add_knowledge_article(self, title: str, content: str,
                             tags: List[str]) -> None:
        """Add knowledge base article."""
        self.knowledge_base[title] = {
            'content': content,
            'tags': tags,
            'created_at': datetime.now()
        }
    
    def find_article(self, query: str) -> Optional[Dict]:
        """Find relevant knowledge base article."""
        query_lower = query.lower()
        best_match = None
        best_score = 0
        
        for title, article in self.knowledge_base.items():
            score = 0
            for tag in article['tags']:
                if tag.lower() in query_lower:
                    score += 2
            if query_lower in title.lower():
                score += 3
            
            if score > best_score:
                best_score = score
                best_match = {'title': title, **article}
        
        return best_match
    
    def generate_response(self, ticket_id: str, 
                         response_type: ResponseType = ResponseType.AUTOMATED,
                         template_name: str = None,
                         variables: Dict[str, str] = None) -> Dict[str, Any]:
        """Generate response for ticket."""
        if response_type == ResponseType.TEMPLATED and template_name:
            template = self.templates.get(template_name)
            if template:
                content = template['template']
                for var, value in (variables or {}).items():
                    content = content.replace(f'{{{{{var}}}}}', value)
                
                self.response_history.append({
                    'ticket_id': ticket_id,
                    'type': 'templated',
                    'template': template_name
                })
                
                return {'type': 'templated', 'content': content}
        
        article = self.find_article(ticket_id)
        if article:
            content = f"Here's some information that might help:\n\n{article['content']}"
            
            self.response_history.append({
                'ticket_id': ticket_id,
                'type': 'knowledge_base',
                'article': article['title']
            })
            
            return {'type': 'automated', 'content': content, 'article': article['title']}
        
        return {'type': 'escalated', 'content': 'I need to escalate this to our specialist team.'}

class CustomerManager:
    """Manages customer information."""
    
    def __init__(self):
        self.customers: Dict[str, Customer] = {}
        self.interactions: List[Dict] = []
    
    def add_customer(self, name: str, email: str, 
                    company: str = None, tier: str = "standard") -> Customer:
        """Add or update customer."""
        existing = self.get_customer_by_email(email)
        if existing:
            return existing
        
        customer = Customer(
            id=str(uuid.uuid4())[:8],
            name=name,
            email=email,
            company=company,
            tier=tier,
            tickets_count=0,
            satisfaction_score=5.0,
            lifetime_value=0.0,
            created_at=datetime.now()
        )
        self.customers[customer.id] = customer
        return customer
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Get customer by email."""
        for customer in self.customers.values():
            if customer.email == email:
                return customer
        return None
    
    def get_customer_by_id(self, customer_id: str) -> Optional[Customer]:
        """Get customer by ID."""
        return self.customers.get(customer_id)
    
    def update_satisfaction(self, customer_id: str, score: float) -> None:
        """Update customer satisfaction score."""
        customer = self.customers.get(customer_id)
        if customer:
            customer.satisfaction_score = (customer.satisfaction_score + score) / 2
    
    def get_customer_history(self, customer_id: str) -> Dict[str, Any]:
        """Get customer interaction history."""
        customer = self.customers.get(customer_id)
        if not customer:
            return {'error': 'Customer not found'}
        
        interactions = [i for i in self.interactions if i['customer_id'] == customer_id]
        
        return {
            'customer': {
                'name': customer.name,
                'email': customer.email,
                'tier': customer.tier
            },
            'total_tickets': customer.tickets_count,
            'avg_satisfaction': customer.satisfaction_score,
            'interactions': interactions
        }

class SupportAnalytics:
    """Analyzes support performance."""
    
    def __init__(self, ticket_manager: TicketManager,
                 customer_manager: CustomerManager):
        self.tickets = ticket_manager
        self.customers = customer_manager
    
    def calculate_metrics(self) -> SupportMetrics:
        """Calculate support metrics."""
        all_tickets = list(self.tickets.tickets.values())
        
        open_count = len(self.tickets.get_tickets_by_status(TicketStatus.OPEN))
        open_count += len(self.tickets.get_tickets_by_status(TicketStatus.IN_PROGRESS))
        
        resolution_times = []
        for t in all_tickets:
            if t.resolved_at:
                duration = (t.resolved_at - t.created_at).total_seconds() / 3600
                resolution_times.append(duration)
        
        avg_resolution = sum(resolution_times) / len(resolution_times) if resolution_times else 0
        
        by_category = defaultdict(int)
        by_priority = defaultdict(int)
        for t in all_tickets:
            by_category[t.category.value] += 1
            by_priority[t.priority.name] += 1
        
        avg_satisfaction = 0
        if self.customers.customers:
            avg_satisfaction = sum(
                c.satisfaction_score for c in self.customers.customers.values()
            ) / len(self.customers.customers)
        
        return SupportMetrics(
            open_tickets=open_count,
            avg_response_time=2.5,
            avg_resolution_time=avg_resolution,
            satisfaction_score=avg_satisfaction,
            first_contact_resolution=0.65,
            tickets_by_category=dict(by_category),
            tickets_by_priority=dict(by_priority)
        )
    
    def generate_report(self, start_date: datetime = None,
                       end_date: datetime = None) -> Dict[str, Any]:
        """Generate support report."""
        metrics = self.calculate_metrics()
        
        overdue = self.tickets.get_overdue_tickets()
        critical = self.tickets.get_tickets_by_priority(TicketPriority.CRITICAL)
        
        top_issues = sorted(
            metrics.tickets_by_category.items(),
            key=lambda x: -x[1]
        )[:5]
        
        return {
            'period': {
                'start': (start_date or datetime.now() - timedelta(days=30)).isoformat(),
                'end': (end_date or datetime.now()).isoformat()
            },
            'summary': {
                'open_tickets': metrics.open_tickets,
                'avg_resolution_hours': f"{metrics.avg_resolution_time:.1f}",
                'satisfaction_score': f"{metrics.satisfaction_score:.1f}/5"
            },
            'alerts': {
                'overdue_count': len(overdue),
                'critical_count': len(critical)
            },
            'top_issues': dict(top_issues),
            'recommendations': self._generate_recommendations(metrics)
        }
    
    def _generate_recommendations(self, metrics: SupportMetrics) -> List[str]:
        """Generate improvement recommendations."""
        recommendations = []
        
        if metrics.satisfaction_score < 4.0:
            recommendations.append("Review and improve response quality")
        if metrics.first_contact_resolution < 0.7:
            recommendations.append("Enhance knowledge base articles")
        if metrics.open_tickets > 50:
            recommendations.append("Consider adding more support agents")
        
        recommendations.append("Implement proactive outreach for at-risk customers")
        recommendations.append("Regularly update FAQ and documentation")
        
        return recommendations

class SupportAgent:
    """Main support agent."""
    
    def __init__(self):
        self.tickets = TicketManager()
        self.response = ResponseEngine()
        self.customers = CustomerManager()
        self.analytics = SupportAnalytics(self.tickets, self.customers)
    
    def handle_incoming_ticket(self, subject: str, description: str,
                              category: str, priority: str,
                              customer_email: str, **kwargs) -> Dict[str, Any]:
        """Handle new support ticket."""
        customer = self.customers.add_customer(
            name=kwargs.get('customer_name', 'Unknown'),
            email=customer_email,
            company=kwargs.get('company'),
            tier=kwargs.get('tier', 'standard')
        )
        
        ticket = self.tickets.create_ticket(
            subject=subject,
            description=description,
            category=TicketCategory[category.upper()],
            priority=TicketPriority[int(priority)],
            customer_id=customer.id,
            tags=kwargs.get('tags', []),
            metadata=kwargs.get('metadata', {})
        )
        
        response = self.response.generate_response(
            ticket.id,
            response_type=ResponseType.AUTOMATED
        )
        
        self.tickets.add_message(ticket.id, 'agent', response['content'])
        
        return {
            'ticket_id': ticket.id,
            'customer_id': customer.id,
            'response_type': response['type'],
            'status': ticket.status.value
        }
    
    def generate_auto_response(self, ticket_id: str) -> Dict[str, Any]:
        """Generate automatic response for ticket."""
        ticket = self.tickets.tickets.get(ticket_id)
        if not ticket:
            return {'error': 'Ticket not found'}
        
        response = self.response.generate_response(ticket_id)
        
        if response['type'] != 'escalated':
            self.tickets.add_message(ticket_id, 'agent', response['content'])
        
        return response
    
    def escalate_ticket(self, ticket_id: str, reason: str,
                       escalate_to: str) -> Dict[str, Any]:
        """Escalate ticket to specialist."""
        ticket = self.tickets.tickets.get(ticket_id)
        if not ticket:
            return {'error': 'Ticket not found'}
        
        ticket.status = TicketStatus.WAITING
        self.tickets.add_message(ticket_id, 'system', 
                                f"Escalated to {escalate_to}: {reason}")
        
        return {
            'ticket_id': ticket_id,
            'escalated_to': escalate_to,
            'reason': reason,
            'status': 'escalated'
        }
    
    def get_support_dashboard(self) -> Dict[str, Any]:
        """Get support dashboard."""
        metrics = self.analytics.calculate_metrics()
        
        return {
            'queue': {
                'open': metrics.open_tickets,
                'critical': len(self.tickets.get_tickets_by_priority(TicketPriority.CRITICAL)),
                'overdue': len(self.tickets.get_overdue_tickets())
            },
            'metrics': {
                'avg_resolution_hours': f"{metrics.avg_resolution_time:.1f}",
                'satisfaction': f"{metrics.satisfaction_score:.1f}/5",
                'first_contact_rate': f"{metrics.first_contact_resolution * 100:.0f}%"
            },
            'by_category': metrics.tickets_by_category,
            'recommendations': self.analytics._generate_recommendations(metrics)
        }

def main():
    """Main entry point."""
    agent = SupportAgent()
    
    result = agent.handle_incoming_ticket(
        subject="Login issue",
        description="Cannot login to my account",
        category="technical",
        priority="2",
        customer_email="user@example.com",
        customer_name="John Doe"
    )
    print(f"Ticket created: {result}")
    
    dashboard = agent.get_support_dashboard()
    print(f"Dashboard: {dashboard}")

if __name__ == "__main__":
    main()

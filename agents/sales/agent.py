#!/usr/bin/env python3
"""
Grok Sales Agent
Specialized agent for sales automation, lead management, and revenue optimization.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json
import uuid
from collections import defaultdict

class LeadStatus(Enum):
    NEW = "new"
    CONTACTED = "contacted"
    QUALIFIED = "qualified"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"

class LeadSource(Enum):
    WEBSITE = "website"
    REFERRAL = "referral"
    COLD_OUTREACH = "cold_outreach"
    SOCIAL_MEDIA = "social_media"
    EVENT = "event"
    PAID_ADS = "paid_ads"
    ORGANIC = "organic"

class DealStage(Enum):
    DISCOVERY = "discovery"
    QUALIFICATION = "qualification"
    NEEDS_ANALYSIS = "needs_analysis"
    PROPOSAL = "proposal"
    DEMO = "demo"
    PRICING = "pricing"
    CONTRACT = "contract"
    CLOSING = "closing"

@dataclass
class Lead:
    id: str
    name: str
    email: str
    company: str
    title: str
    status: LeadStatus
    source: LeadSource
    created_at: datetime
    last_contact: datetime
    score: int
    tags: List[str]
    notes: List[str]
    contact_info: Dict[str, Any]

@dataclass
class Deal:
    id: str
    lead_id: str
    stage: DealStage
    value: float
    probability: float
    expected_close: datetime
    created_at: datetime
    updated_at: datetime
    products: List[str]
    requirements: List[str]
    competitors: List[str]

@dataclass
class SalesMetrics:
    total_leads: int
    qualified_leads: int
    deals_in_pipeline: float
    win_rate: float
    avg_deal_size: float
    avg_sales_cycle: float
    pipeline_value: float
    revenue_forecast: float

class LeadScorer:
    """Scores and qualifies leads based on criteria."""
    
    def __init__(self):
        self.criteria_weights = {
            'company_size': 0.15,
            'job_title': 0.12,
            'budget': 0.20,
            'authority': 0.15,
            'need': 0.18,
            'timeline': 0.12,
            'source_quality': 0.08
        }
    
    def score_lead(self, lead: Lead) -> int:
        """Calculate lead score (0-100)."""
        score = 0
        
        title_scores = {
            'cto': 100, 'vp': 90, 'director': 80,
            'manager': 60, 'lead': 50, 'developer': 30
        }
        title_key = lead.title.lower().split()[0] if lead.title else ''
        score += title_scores.get(title_key, 40) * self.criteria_weights['job_title']
        
        company_size_score = min(100, len(lead.company) * 5 + 
                                 len(lead.contact_info.get('employees', '')) * 2)
        score += company_size_score * self.criteria_weights['company_size']
        
        budget_indicator = lead.contact_info.get('budget', '')
        if 'enterprise' in budget_indicator.lower():
            score += 100 * self.criteria_weights['budget']
        elif 'mid' in budget_indicator.lower():
            score += 60 * self.criteria_weights['budget']
        else:
            score += 30 * self.criteria_weights['budget']
        
        if lead.status in [LeadStatus.QUALIFIED, LeadStatus.PROPOSAL]:
            score += 100 * self.criteria_weights['authority']
        
        if lead.source in [LeadSource.REFERRAL, LeadSource.EVENT]:
            score += 100 * self.criteria_weights['source_quality']
        elif lead.source == LeadSource.COLD_OUTREACH:
            score += 30 * self.criteria_weights['source_quality']
        
        return min(100, int(score))
    
    def qualify_lead(self, lead: Lead) -> Dict[str, Any]:
        """Determine if lead meets qualification criteria."""
        score = self.score_lead(lead)
        
        criteria = {
            'has_budget': bool(lead.contact_info.get('budget')),
            'has_authority': lead.title.lower() in ['cto', 'vp', 'director', 'ceo'],
            'has_need': len(lead.notes) > 0 or 'need' in lead.tags,
            'has_timeline': lead.contact_info.get('timeline') is not None
        }
        
        passed = sum(1 for v in criteria.values() if v)
        qualification = {
            'qualified': score >= 60 and passed >= 3,
            'score': score,
            'criteria_met': criteria,
            'bant_score': passed
        }
        
        return qualification

class PipelineManager:
    """Manages sales pipeline and deals."""
    
    def __init__(self):
        self.deals: Dict[str, Deal] = {}
        self.stage_history: List[Dict[str, Any]] = []
    
    def create_deal(self, lead_id: str, value: float,
                   expected_close: datetime, products: List[str] = None) -> Deal:
        """Create new deal from lead."""
        deal = Deal(
            id=str(uuid.uuid4())[:8],
            lead_id=lead_id,
            stage=DealStage.DISCOVERY,
            value=value,
            probability=0.10,
            expected_close=expected_close,
            created_at=datetime.now(),
            updated_at=datetime.now(),
            products=products or [],
            requirements=[],
            competitors=[]
        )
        self.deals[deal.id] = deal
        return deal
    
    def move_deal_stage(self, deal_id: str, new_stage: DealStage,
                       probability_override: float = None) -> Deal:
        """Move deal to new stage."""
        if deal_id not in self.deals:
            raise ValueError(f"Deal {deal_id} not found")
        
        deal = self.deals[deal_id]
        old_stage = deal.stage
        deal.stage = new_stage
        deal.updated_at = datetime.now()
        
        stage_probabilities = {
            DealStage.DISCOVERY: 0.10,
            DealStage.QUALIFICATION: 0.20,
            DealStage.NEEDS_ANALYSIS: 0.30,
            DealStage.PROPOSAL: 0.40,
            DealStage.DEMO: 0.50,
            DealStage.PRICING: 0.60,
            DealStage.CONTRACT: 0.75,
            DealStage.CLOSING: 0.90
        }
        
        if probability_override:
            deal.probability = probability_override
        else:
            deal.probability = stage_probabilities.get(new_stage, 0.10)
        
        self.stage_history.append({
            'deal_id': deal_id,
            'from_stage': old_stage.value,
            'to_stage': new_stage.value,
            'timestamp': datetime.now().isoformat()
        })
        
        return deal
    
    def get_pipeline_value(self) -> float:
        """Calculate total pipeline value."""
        return sum(deal.value * deal.probability for deal in self.deals.values())
    
    def get_deals_by_stage(self) -> Dict[DealStage, List[Deal]]:
        """Group deals by stage."""
        grouped = defaultdict(list)
        for deal in self.deals.values():
            grouped[deal.stage].append(deal)
        return dict(grouped)
    
    def forecast_revenue(self, periods: int = 12) -> Dict[str, float]:
        """Forecast revenue by period."""
        forecast = {}
        now = datetime.now()
        
        for i in range(periods):
            period_start = now + timedelta(days=30*i)
            period_end = period_start + timedelta(days=30)
            
            period_revenue = sum(
                deal.value for deal in self.deals.values()
                if deal.expected_close >= period_start and 
                   deal.expected_close < period_end and
                   deal.stage in [DealStage.CLOSING, DealStage.CONTRACT]
            )
            
            weighted_revenue = sum(
                deal.value * deal.probability for deal in self.deals.values()
                if deal.expected_close >= period_start and 
                   deal.expected_close < period_end
            )
            
            forecast[f"period_{i+1}"] = {
                'period_start': period_start.isoformat(),
                'committed': period_revenue,
                'weighted': weighted_revenue
            }
        
        return forecast

class OutreachManager:
    """Manages sales outreach and communications."""
    
    def __init__(self):
        self.templates = {}
        self.campaigns = []
        self.interactions = []
    
    def add_template(self, name: str, subject: str, body: str,
                    trigger: str = None) -> None:
        """Add email template."""
        self.templates[name] = {
            'subject': subject,
            'body': body,
            'trigger': trigger
        }
    
    def personalize_template(self, template_name: str, lead: Lead) -> Dict[str, str]:
        """Personalize template for lead."""
        template = self.templates.get(template_name)
        if not template:
            return {'error': f'Template {template_name} not found'}
        
        subject = template['subject']
        body = template['body']
        
        replacements = {
            '{{name}}': lead.name,
            '{{company}}': lead.company,
            '{{title}}': lead.title
        }
        
        for placeholder, value in replacements.items():
            subject = subject.replace(placeholder, value)
            body = body.replace(placeholder, value)
        
        return {'subject': subject, 'body': body}
    
    def schedule_outreach(self, lead_id: str, template_name: str,
                         scheduled_time: datetime) -> Dict[str, Any]:
        """Schedule outreach for lead."""
        self.campaigns.append({
            'lead_id': lead_id,
            'template': template_name,
            'scheduled_time': scheduled_time,
            'status': 'scheduled'
        })
        
        return {
            'lead_id': lead_id,
            'template': template_name,
            'scheduled_for': scheduled_time.isoformat(),
            'status': 'scheduled'
        }
    
    def track_interaction(self, lead_id: str, interaction_type: str,
                         details: Dict[str, Any]) -> None:
        """Track interaction with lead."""
        self.interactions.append({
            'lead_id': lead_id,
            'type': interaction_type,
            'details': details,
            'timestamp': datetime.now().isoformat()
        })

class SalesAnalytics:
    """Analyzes sales performance and trends."""
    
    def __init__(self, lead_manager, pipeline_manager, outreach_manager):
        self.lead_manager = lead_manager
        self.pipeline_manager = pipeline_manager
        self.outreach_manager = outreach_manager
    
    def calculate_metrics(self) -> SalesMetrics:
        """Calculate key sales metrics."""
        leads = list(self.lead_manager.leads.values())
        
        qualified = [l for l in leads if l.status in 
                    [LeadStatus.QUALIFIED, LeadStatus.PROPOSAL, LeadStatus.NEGOTIATION]]
        
        deals = list(self.pipeline_manager.deals.values())
        closed_won = [d for d in deals if d.stage == DealStage.CLOSING]
        closed_total = len(closed_won) + len([d for d in deals 
                                              if d.stage == DealStage.CLOSING])
        
        pipeline_value = self.pipeline_manager.get_pipeline_value()
        
        win_rate = len(closed_won) / closed_total if closed_total > 0 else 0
        
        avg_deal_size = sum(d.value for d in closed_won) / len(closed_won) if closed_won else 0
        
        return SalesMetrics(
            total_leads=len(leads),
            qualified_leads=len(qualified),
            deals_in_pipeline=len(deals),
            win_rate=win_rate,
            avg_deal_size=avg_deal_size,
            avg_sales_cycle=30.0,
            pipeline_value=pipeline_value,
            revenue_forecast=pipeline_value * 0.3
        )
    
    def analyze_conversion_rates(self) -> Dict[str, float]:
        """Analyze conversion rates between stages."""
        deals = list(self.pipeline_manager.deals.values())
        stage_counts = defaultdict(int)
        
        for deal in deals:
            stage_counts[deal.stage.value] += 1
        
        total = len(deals)
        conversion_rates = {}
        
        for stage, count in stage_counts.items():
            conversion_rates[stage] = (count / total * 100) if total > 0 else 0
        
        return conversion_rates
    
    def identify_top_performers(self) -> List[Dict[str, Any]]:
        """Identify top performing leads/deals."""
        deals = list(self.pipeline_manager.deals.values())
        sorted_deals = sorted(deals, key=lambda d: d.value, reverse=True)
        
        return [
            {
                'deal_id': d.id,
                'value': d.value,
                'stage': d.stage.value,
                'probability': d.probability
            }
            for d in sorted_deals[:10]
        ]
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive sales report."""
        metrics = self.calculate_metrics()
        
        return {
            'report_date': datetime.now().isoformat(),
            'summary': {
                'total_leads': metrics.total_leads,
                'pipeline_value': metrics.pipeline_value,
                'win_rate': f"{metrics.win_rate * 100:.1f}%",
                'avg_deal_size': f"${metrics.avg_deal_size:,.2f}"
            },
            'pipeline': {
                'total_deals': metrics.deals_in_pipeline,
                'by_stage': self.pipeline_manager.get_deals_by_stage()
            },
            'conversions': self.analyze_conversion_rates(),
            'top_performers': self.identify_top_performers(),
            'forecast': self.pipeline_manager.forecast_revenue()
        }

class SalesAgent:
    """Main sales agent."""
    
    def __init__(self):
        self.leads: Dict[str, Lead] = {}
        self.scorer = LeadScorer()
        self.pipeline = PipelineManager()
        self.outreach = OutreachManager()
        self.analytics = SalesAnalytics(self, self.pipeline, self.outreach)
    
    def add_lead(self, name: str, email: str, company: str,
                title: str, source: LeadSource, **kwargs) -> Lead:
        """Add new lead."""
        lead = Lead(
            id=str(uuid.uuid4())[:8],
            name=name,
            email=email,
            company=company,
            title=title,
            status=LeadStatus.NEW,
            source=source,
            created_at=datetime.now(),
            last_contact=datetime.now(),
            score=0,
            tags=kwargs.get('tags', []),
            notes=kwargs.get('notes', []),
            contact_info=kwargs.get('contact_info', {})
        )
        lead.score = self.scorer.score_lead(lead)
        self.leads[lead.id] = lead
        return lead
    
    def qualify_lead(self, lead_id: str) -> Dict[str, Any]:
        """Qualify lead."""
        lead = self.leads.get(lead_id)
        if not lead:
            return {'error': 'Lead not found'}
        
        qualification = self.scorer.qualify_lead(lead)
        
        if qualification['qualified']:
            lead.status = LeadStatus.QUALIFIED
        
        return qualification
    
    def convert_to_deal(self, lead_id: str, value: float,
                       expected_close: datetime) -> Deal:
        """Convert qualified lead to deal."""
        lead = self.leads.get(lead_id)
        if not lead:
            raise ValueError(f"Lead {lead_id} not found")
        
        lead.status = LeadStatus.PROPOSAL
        return self.pipeline.create_deal(
            lead_id=lead_id,
            value=value,
            expected_close=expected_close
        )
    
    def get_dashboard(self) -> Dict[str, Any]:
        """Get sales dashboard."""
        metrics = self.analytics.calculate_metrics()
        
        return {
            'leads': {
                'total': len(self.leads),
                'new': len([l for l in self.leads.values() if l.status == LeadStatus.NEW]),
                'qualified': len([l for l in self.leads.values() 
                                 if l.status == LeadStatus.QUALIFIED])
            },
            'pipeline': {
                'total_value': self.pipeline.get_pipeline_value(),
                'deals_count': len(self.pipeline.deals)
            },
            'metrics': {
                'win_rate': f"{metrics.win_rate * 100:.1f}%",
                'avg_deal_size': f"${metrics.avg_deal_size:,.2f}"
            }
        }

def main():
    """Main entry point."""
    agent = SalesAgent()
    
    lead = agent.add_lead(
        name="John Smith",
        email="john@techcorp.com",
        company="TechCorp",
        title="CTO",
        source=LeadSource.WEBSITE,
        contact_info={'budget': 'enterprise', 'timeline': 'Q2'}
    )
    
    qualification = agent.qualify_lead(lead.id)
    print(f"Lead qualified: {qualification}")
    
    dashboard = agent.get_dashboard()
    print(f"Dashboard: {dashboard}")

if __name__ == "__main__":
    main()

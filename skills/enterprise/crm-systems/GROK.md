---
name: "CRM Systems"
version: "2.0.0"
description: "Comprehensive CRM systems toolkit with contact management, sales pipeline, marketing automation, customer service, and analytics for enterprise customer relationship management"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["enterprise", "crm", "contact-management", "sales-pipeline", "marketing", "customer-service"]
category: "enterprise"
personality: "crm-engineer"
use_cases: ["contact management", "sales pipeline", "marketing automation", "customer service", "CRM analytics"]
---

# CRM Systems

> Production-grade CRM framework providing contact management, sales pipeline, marketing automation, customer service, and comprehensive analytics for enterprise customer relationship management.

## Overview

The CRM Systems module provides tools for managing customer relationships across the entire lifecycle. It implements contact and lead management, sales pipeline tracking, marketing campaign automation, customer service ticketing, and comprehensive CRM analytics. Every feature includes workflow automation, integration capabilities, and audit logging.

## Core Capabilities

### 1. Contact Management
- Contact and company profiles
- Interaction history tracking
- Segment management
- Data enrichment
- Duplicate detection

### 2. Sales Pipeline
- Opportunity tracking
- Deal stage management
- Forecasting and quotas
- Activity tracking
- Win/loss analysis

### 3. Marketing Automation
- Campaign creation and management
- Email marketing workflows
- Lead scoring and nurturing
- A/B testing
- ROI tracking

### 4. Customer Service
- Ticket management
- SLA tracking
- Knowledge base integration
- Customer satisfaction tracking
- Escalation workflows

### 5. CRM Analytics
- Sales performance dashboards
- Customer lifetime value
- Churn prediction
- Conversion funnel analysis
- Revenue attribution

### 6. Integration
- Email integration
- Calendar integration
- Phone system integration
- Social media integration
- ERP integration

## Usage Examples

### Contact Management

```python
from crm_systems import ContactManager, Contact

manager = ContactManager()

# Create contact
contact = manager.create_contact(Contact(
    first_name="John",
    last_name="Doe",
    email="john.doe@company.com",
    company="Acme Corp",
    phone="+1-555-0123",
    tags=["enterprise", "decision-maker"],
))

print(f"Contact: {contact.full_name}")
print(f"ID: {contact.id}")
print(f"Company: {contact.company}")
```

### Sales Pipeline

```python
from crm_systems import SalesPipeline, DealStage

pipeline = SalesPipeline()

# Create deal
deal = pipeline.create_deal(
    title="Enterprise License",
    contact_id=contact.id,
    value=50000,
    stage=DealStage.QUALIFICATION,
    expected_close="2024-03-01",
)

print(f"Deal: {deal.title}")
print(f"Value: ${deal.value:,.2f}")
print(f"Stage: {deal.stage.value}")

# Move deal forward
pipeline.advance_deal(deal.id, DealStage.PROPOSAL)
```

### Marketing Automation

```python
from crm_systems import MarketingAutomation, Campaign

automation = MarketingAutomation()

# Create campaign
campaign = automation.create_campaign(Campaign(
    name="Q1 Product Launch",
    type="email",
    target_segment="enterprise_leads",
    content={"subject": "Introducing our new product"},
))

print(f"Campaign: {campaign.name}")
print(f"Type: {campaign.type}")
print(f"Target: {campaign.target_segment}")
```

### Customer Service

```python
from crm_systems import ServiceDesk, Ticket

desk = ServiceDesk()

# Create ticket
ticket = desk.create_ticket(Ticket(
    subject="Login issue",
    customer_email="customer@company.com",
    priority="high",
    category="technical",
))

print(f"Ticket: {ticket.id}")
print(f"Priority: {ticket.priority}")
print(f"Status: {ticket.status}")
```

## Best Practices

### Contact Management
- Keep contact data clean and up-to-date
- Use tags for segmentation
- Track all interactions
- Enrich data from external sources

### Sales Pipeline
- Define clear stage criteria
- Update deals regularly
- Use forecasting for planning
- Analyze win/loss patterns

### Marketing Automation
- Segment audiences carefully
- A/B test campaigns
- Track ROI for each campaign
- Nurture leads over time

### Customer Service
- Set and track SLAs
- Use knowledge base for common issues
- Measure customer satisfaction
- Automate routine workflows

## Related Modules

- **business-intelligence**: CRM analytics and reporting
- **workflow-automation**: CRM workflow automation
- **data-warehousing**: CRM data warehousing
- **erp-systems**: ERP integration

---

## Advanced Configuration

### Contact Management Settings

```python
from crm_systems import ContactConfig

contact_config = ContactConfig(
    # Data Enrichment
    enrichment={
        "enabled": True,
        "providers": ["clearbit", "zoominfo"],
        "auto_enrich": True,
        "refresh_interval_days": 30,
    },
    
    # Deduplication
    deduplication={
        "enabled": True,
        "matching_fields": ["email", "phone", "company"],
        "auto_merge": False,
        "confidence_threshold": 0.85,
    },
    
    # Segmentation
    segmentation={
        "auto_segment": True,
        "segment_criteria": ["industry", "company_size", "engagement"],
        "update_frequency": "daily",
    },
)
```

### Sales Pipeline Settings

```python
from crm_systems import PipelineConfig

pipeline_config = PipelineConfig(
    # Stages
    stages=[
        {"name": "Prospecting", "probability": 0.1, "duration_days": 14},
        {"name": "Qualification", "probability": 0.25, "duration_days": 7},
        {"name": "Proposal", "probability": 0.5, "duration_days": 10},
        {"name": "Negotiation", "probability": 0.75, "duration_days": 7},
        {"name": "Closed Won", "probability": 1.0, "duration_days": 0},
    ],
    
    # Forecasting
    forecasting={
        "method": "weighted",  # weighted, ai, manual
        "ai_model": "gradient_boosting",
        "confidence_threshold": 0.7,
    },
    
    # Automation
    automation={
        "auto_assign_leads": True,
        "round_robin": True,
        "lead_scoring": True,
    },
)
```

## Architecture Patterns

### CRM Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Frontend Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Web App  │  │ Mobile   │  │ API      │         │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘         │
└───────┼──────────────┼──────────────┼───────────────┘
        │              │              │
        ▼              ▼              ▼
┌─────────────────────────────────────────────────────┐
│                 Application Layer                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Contact  │──│ Pipeline │──│Marketing │         │
│  │ Service  │  │ Service  │  │ Service  │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│                   Data Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Primary  │  │ Cache    │  │ Search   │         │
│  │ DB       │  │ (Redis)  │  │(Elastic) │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────┘
```

### Lead Scoring Model

```python
from crm_systems import LeadScorer

scorer = LeadScorer()

# Configure scoring model
scorer.configure(
    model="gradient_boosting",
    features=[
        "company_size",
        "industry",
        "engagement_score",
        "page_views",
        "email_opens",
        "demo_requested",
    ],
    weights={
        "demographic": 0.4,
        "behavioral": 0.4,
        "firmographic": 0.2,
    },
)

# Score leads
leads = scorer.score(new_leads)
for lead in leads:
    print(f"{lead.name}: {lead.score:.2f} ({lead.quality})")
```

## Integration Guide

### Email Integration

```python
from crm_systems import EmailIntegration

email = EmailIntegration()

# Configure email sync
email.configure(
    provider="exchange",
    sync_direction="bidirectional",
    sync_interval_minutes=15,
)

# Track email engagement
email.track(
    contact_id="contact-123",
    campaign_id="campaign-456",
)

# Get engagement metrics
metrics = email.get_metrics(contact_id="contact-123")
print(f"Emails sent: {metrics.sent}")
print(f"Open rate: {metrics.open_rate:.1%}")
print(f"Click rate: {metrics.click_rate:.1%}")
```

### Calendar Integration

```python
from crm_systems import CalendarIntegration

calendar = CalendarIntegration()

# Sync meetings
calendar.sync(
    crm_system="salesforce",
    calendar_system="google",
    sync_direction="bidirectional",
)

# Schedule meeting with CRM context
meeting = calendar.schedule(
    title="Quarterly Business Review",
    attendees=["contact-123", "user-456"],
    duration_minutes=60,
    crm_context={
        "opportunity_id": "opp-789",
        "deal_value": 50000,
    },
)
```

## Performance Optimization

### Contact Search Optimization

```python
from crm_systems import SearchOptimizer

optimizer = SearchOptimizer()

# Optimize contact search
optimized = optimizer.optimize(
    index="contacts",
    strategies=[
        "full_text_search",
        "fuzzy_matching",
        "auto_complete",
    ],
)

print(f"Search latency: {optimized.latency_ms:.1f}ms")
print(f"Relevance score: {optimized.relevance:.2f}")
```

### Pipeline Analytics

```python
from crm_systems import PipelineAnalytics

analytics = PipelineAnalytics()

# Analyze pipeline performance
report = analytics.analyze(
    pipeline_id="sales-pipeline",
    time_range=("2024-01-01", "2024-01-31"),
)

print(f"Conversion rate: {report.conversion_rate:.1%}")
print(f"Average deal size: ${report.avg_deal_size:,.0f}")
print(f"Sales cycle: {report.avg_cycle_days:.0f} days")
print(f"Win rate: {report.win_rate:.1%}")
```

## Security Considerations

### Data Privacy

```python
from crm_systems import PrivacyManager

privacy = PrivacyManager()

# GDPR compliance
privacy.configure_gdpr(
    data_retention_days=365,
    right_to_erasure=True,
    consent_tracking=True,
    data_portability=True,
)

# Handle data subject request
privacy.handle_request(
    request_type="erasure",
    contact_id="contact-123",
    deadline_days=30,
)
```

### Access Control

```python
from crm_systems import AccessControl

ac = AccessControl()

# Role-based access
ac.define_role("sales_rep", permissions=[
    "contacts.read",
    "contacts.write_own",
    "deals.read_own",
    "deals.write_own",
])

ac.define_role("sales_manager", permissions=[
    "contacts.read_all",
    "deals.read_team",
    "reports.view",
])
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Duplicate contacts | Poor dedup rules | Adjust matching criteria |
| Slow search | Missing indexes | Add search indexes |
| Sync failures | API limits | Implement rate limiting |
| Inaccurate forecasting | Poor data quality | Clean data, improve scoring |
| Missing activities | Sync gaps | Check sync interval, fix errors |

### Debug Mode

```python
from crm_systems import enable_debug

enable_debug(
    components=["contacts", "pipeline", "sync"],
    log_level="DEBUG",
)

# Debug contact sync
debug_session = debug.trace_sync("contact-123")
print(f"Debug report: {debug_session.report_url}")
```

## API Reference

### REST Endpoints

```
GET    /api/v1/crm/contacts                 List contacts
POST   /api/v1/crm/contacts                 Create contact
GET    /api/v1/crm/contacts/{id}            Get contact
PUT    /api/v1/crm/contacts/{id}            Update contact
DELETE /api/v1/crm/contacts/{id}            Delete contact

GET    /api/v1/crm/opportunities            List opportunities
POST   /api/v1/crm/opportunities            Create opportunity
PUT    /api/v1/crm/opportunities/{id}/stage Update stage

GET    /api/v1/crm/activities               List activities
POST   /api/v1/crm/activities               Create activity
```

### Data Models

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID

@dataclass
class Contact:
    contact_id: UUID
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    company: str
    title: Optional[str]
    lead_score: float
    created_at: datetime

@dataclass
class Opportunity:
    opportunity_id: UUID
    name: str
    contact_id: UUID
    stage: str
    value: float
    probability: float
    expected_close: datetime
    owner: str

@dataclass
class Activity:
    activity_id: UUID
    contact_id: UUID
    type: str  # call, email, meeting
    subject: str
    timestamp: datetime
    user: str
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "crm_systems.app:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Monitoring & Observability

### Key Metrics

```python
from crm_systems import Metrics

metrics = Metrics()

# Track CRM usage
metrics.counter("crm.contacts_created", tags={"source": "web"})
metrics.counter("crm.opportunities_updated", tags={"stage": "proposal"})

# Track sync performance
metrics.histogram("crm.sync_duration_ms", duration, tags={"type": "contacts"})
metrics.counter("crm.sync_errors", tags={"type": "email"})
```

## Testing Strategy

### Unit Tests

```python
import pytest
from crm_systems import ContactManager

@pytest.fixture
def manager():
    return ContactManager(test_mode=True)

def test_create_contact(manager):
    contact = manager.create(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
    )
    assert contact.contact_id is not None
    assert contact.email == "john@example.com"
```

## Versioning & Migration

### Version History

- **2.0.0**: Added AI lead scoring, advanced automation, predictive forecasting
- **1.5.0**: Added email integration, calendar sync, basic analytics
- **1.0.0**: Initial release with contact and opportunity management

## Glossary

| Term | Definition |
|------|------------|
| **Lead** | Potential customer |
| **Opportunity** | Sales deal in progress |
| **Pipeline** | Sales process stages |
| **SLA** | Service Level Agreement |
| **MQL** | Marketing Qualified Lead |
| **SQL** | Sales Qualified Lead |

## Changelog

### Version 2.0.0
- AI-powered lead scoring
- Advanced workflow automation
- Predictive forecasting
- Enhanced integrations

### Version 1.5.0
- Email and calendar integration
- Basic analytics
- Workflow automation

### Version 1.0.0
- Initial release
- Contact management
- Opportunity tracking

## Contributing Guidelines

1. Test with realistic CRM data
2. Validate data sync accuracy
3. Benchmark search performance
4. Document integration requirements

## Customer Lifecycle Management

### Customer Journey Mapping

```python
from crm_systems import JourneyMapper

mapper = JourneyMapper()

# Map customer journey
journey = mapper.map_journey(
    customer_id="cust-123",
    stages=[
        {"stage": "awareness", "touchpoints": ["website", "social"]},
        {"stage": "consideration", "touchpoints": ["demo", "email"]},
        {"stage": "purchase", "touchpoints": ["sales_call", "contract"]},
        {"stage": "onboarding", "touchpoints": ["implementation", "training"]},
        {"stage": "retention", "touchpoints": ["support", "success"]},
    ],
)

print(f"Customer Journey:")
print(f"  Current Stage: {journey.current_stage}")
print(f"  Time in Stage: {journey.time_in_stage_days} days")
print(f"  Next Best Action: {journey.next_action}")
print(f"  Conversion Probability: {journey.conversion_probability:.1%}")
```

### Churn Prediction

```python
from crm_systems import ChurnPredictor

predictor = ChurnPredictor()

# Predict churn risk
prediction = predictor.predict(
    customer_id="cust-123",
    features={
        "usage_frequency": 3.2,
        "support_tickets": 5,
        "contract_value": 50000,
        "tenure_months": 24,
        "nps_score": 7,
        "last_login_days": 14,
    },
)

print(f"Churn Prediction:")
print(f"  Risk Score: {prediction.risk_score:.2f}")
print(f"  Risk Level: {prediction.risk_level}")
print(f"  Top Factors: {prediction.top_factors}")
print(f"  Recommended Actions: {prediction.recommended_actions}")
```

### Customer Segmentation

```python
from crm_systems import CustomerSegmenter

segmenter = CustomerSegmenter()

# Segment customers
segments = segmenter.segment(
    method="rfm_value",
    criteria={
        "recency_days": 90,
        "frequency_min": 3,
        "monetary_min": 10000,
    },
)

for segment in segments:
    print(f"\nSegment: {segment.name}")
    print(f"  Size: {segment.customer_count:,}")
    print(f"  Avg Value: ${segment.avg_value:,.2f}")
    print(f"  Churn Risk: {segment.churn_risk:.1%}")
```

## Sales Forecasting

### Pipeline Forecasting

```python
from crm_systems import PipelineForecaster

forecaster = PipelineForecaster()

# Generate forecast
forecast = forecaster.forecast(
    pipeline_id="sales-pipeline",
    time_horizon_quarters=2,
    method="weighted_pipeline",
)

print(f"Sales Forecast:")
print(f"  Q1 2024: ${forecast.q1_amount:,.0f} ({forecast.q1_probability:.0%} confidence)")
print(f"  Q2 2024: ${forecast.q2_amount:,.0f} ({forecast.q2_probability:.0%} confidence)")
print(f"  Pipeline Coverage: {forecast.coverage_ratio:.1f}x")
print(f"  Gap to Target: ${forecast.gap_to_target:,.0f}")
```

### Win Rate Analysis

```python
from crm_systems import WinRateAnalyzer

analyzer = WinRateAnalyzer()

# Analyze win rates
analysis = analyzer.analyze(
    time_range_days=90,
    dimensions=["stage", "rep", "segment", "deal_size"],
)

print(f"Win Rate Analysis:")
print(f"  Overall Win Rate: {analysis.overall_win_rate:.1%}")
for rep in analysis.top_reps[:5]:
    print(f"  {rep.name}: {rep.win_rate:.1%} ({rep.deals_won}/{rep.deals_total})")
```

## Advanced CRM Analytics

### Customer Health Score

```python
from crm_systems import HealthScoreEngine

engine = HealthScoreEngine()

# Calculate customer health
health = engine.calculate(
    customer_id="cust-123",
    factors={
        "usage_frequency": 0.8,
        "support_tickets": 0.3,
        "nps_score": 0.7,
        "contract_value": 0.9,
        "engagement_score": 0.6,
        "payment_history": 0.95,
    },
)

print(f"Customer Health Score: {health.score:.0f}/100")
print(f"  Status: {health.status}")
print(f"  Trend: {health.trend}")
print(f"  Risk Factors: {health.risk_factors}")
print(f"  Next Action: {health.recommended_action}")
```

### Revenue Attribution

```python
from crm_systems import AttributionEngine

attribution = AttributionEngine()

# Analyze revenue attribution
report = attribution.analyze(
    time_range_days=90,
    channels=["direct", "partner", "marketing", "referral"],
    model="multi_touch",
)

print(f"Revenue Attribution:")
for channel in report.channels:
    print(f"  {channel.name}: ${channel.revenue:,.0f} ({channel.percentage:.1%})")
    print(f"    Touches: {channel.touch_count}")
    print(f"    Avg Deal Size: ${channel.avg_deal_size:,.0f}")
```

### Activity Scoring

```python
from crm_systems import ActivityScorer

scorer = ActivityScorer()

# Score lead activity
score = scorer.score(
    lead_id="lead-456",
    activities=[
        {"type": "website_visit", "count": 15, "recency_days": 2},
        {"type": "email_open", "count": 8, "recency_days": 1},
        {"type": "demo_request", "count": 1, "recency_days": 3},
        {"type": "content_download", "count": 3, "recency_days": 5},
    ],
)

print(f"Lead Activity Score: {score.value:.0f}/100")
print(f"  Grade: {score.grade}")
print(f"  Recommended Action: {score.recommended_action}")
print(f"  Time to Conversion: {score.estimated_days_to_conversion} days")
```

## Advanced Sales Analytics

### Territory Management

```python
from crm_systems import TerritoryManager

territory_mgr = TerritoryManager()

# Analyze territory performance
performance = territory_mgr.analyze(
    time_range_days=90,
    metrics=["revenue", "deals_closed", "pipeline_value"],
)

print(f"Territory Performance:")
for territory in performance.territories[:5]:
    print(f"  {territory.name}: ${territory.revenue:,.0f}")
    print(f"    Deals: {territory.deals_closed}")
    print(f"    Pipeline: ${territory.pipeline_value:,.0f}")
    print(f"    Quota Attainment: {territory.quota_attainment:.1%}")
```

### Quota Tracking

```python
from crm_systems import QuotaTracker

tracker = QuotaTracker()

# Track quota attainment
quotas = tracker.track(
    period="2024-Q1",
    sales_reps=["rep-001", "rep-002", "rep-003"],
)

print(f"Quota Tracking:")
for rep in quotas.reps:
    print(f"  {rep.name}: {rep.attainment:.1%} of ${rep.quota:,.0f}")
    print(f"    Closed: ${rep.closed:,.0f}")
    print(f"    Pipeline: ${rep.pipeline:,.0f}")
    print(f"    Forecast: ${rep.forecast:,.0f}")
```

## CRM Data Hygiene

### Duplicate Detection and Merge

```python
from crm_systems import DuplicateDetector

detector = DuplicateDetector()

# Find duplicates
duplicates = detector.find(
    table="contacts",
    matching_rules=[
        {"field": "email", "match_type": "exact"},
        {"field": "phone", "match_type": "fuzzy", "threshold": 0.85},
        {"field": "name+company", "match_type": "composite"},
    ],
)

print(f"Duplicates Found: {len(duplicates)}")
for dup in duplicates[:3]:
    print(f"  Match: {dup.record_a.name} <-> {dup.record_b.name}")
    print(f"    Confidence: {dup.confidence:.1%}")
    print(f"    Fields: {', '.join(dup.matching_fields)}")
```

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills
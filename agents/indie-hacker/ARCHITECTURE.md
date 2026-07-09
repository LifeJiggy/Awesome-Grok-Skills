# Indie Hacker Agent Architecture

## Executive Summary

The Indie Hacker Agent is a comprehensive, modular software platform designed to empower solo entrepreneurs and indie hackers with enterprise-grade business tools. This document provides a detailed architectural overview of the system, explaining how its components interact to deliver business intelligence, marketing automation, customer relationship management, and development workflow capabilities.

The architecture follows a layered design pattern with clear separation of concerns, enabling each subsystem to operate independently while contributing to a cohesive user experience. The system is built with Python 3.8+ and leverages modern programming concepts including dataclasses for data modeling, enumerated types for state management, and object-oriented principles for component encapsulation.

## System Overview

The Indie Hacker Agent serves as a centralized platform for managing all aspects of an indie software business. Unlike point solutions that address individual needs, this agent provides an integrated approach where data and insights flow seamlessly between different functional areas.

The system can be conceptually divided into eight major functional domains, each handled by specialized engines that encapsulate domain logic and provide services to the rest of the system.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Indie Hacker Agent                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        Presentation Layer                             │    │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────────────┐   │    │
│  │  │   CLI Agent   │  │   API Layer   │  │   Interactive Shell   │   │    │
│  │  └───────────────┘  └───────────────┘  └───────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                       Orchestration Layer                              │    │
│  │  ┌──────────────────────────────────────────────────────────────┐  │    │
│  │  │                    IndieHackerAgent                            │  │    │
│  │  │  - Configuration Management                                     │  │    │
│  │  │  - Cross-Engine Coordination                                   │  │    │
│  │  │  - Workflow Automation                                         │  │    │
│  │  │  - Event Distribution                                          │  │    │
│  │  └──────────────────────────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     Domain Engine Layer                               │    │
│  │  ┌───────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────┐  │    │
│  │  │   SaaS    │ │  Marketing    │ │   Customer    │ │  Content  │  │    │
│  │  │  Metrics  │ │   Engine      │ │ Intelligence  │ │  Manager  │  │    │
│  │  │ Calculator│ │               │ │               │ │           │  │    │
│  │  └───────────┘ └───────────────┘ └───────────────┘ └───────────┘  │    │
│  │  ┌───────────┐ ┌───────────────┐ ┌───────────────┐ ┌───────────┐  │    │
│  │  │  Pricing  │ │     Growth    │ │    Funnel     │ │   Project │  │    │
│  │  │ Optimizer │ │   Experiment  │ │   Analyzer    │ │  Manager  │  │    │
│  │  │           │ │   Manager     │ │               │ │           │  │    │
│  │  └───────────┘ └───────────────┘ └───────────────┘ └───────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      Data Model Layer                                  │    │
│  │  ┌───────────────────────────────────────────────────────────────┐  │    │
│  │  │  - Customer    - Task    - Campaign    - Experiment           │  │    │
│  │  │  - TimeEntry   - Tier    - Content     - Feature              │  │    │
│  │  │  - Persona     - Stage   - Entry       - Component             │  │    │
│  │  └───────────────────────────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                     Foundation Services                                │    │
│  │  ┌───────────────┐  ┌───────────────┐  ┌───────────────────────┐   │    │
│  │  │  UUID Gen     │  │  Date/Time    │  │  Serialization        │   │    │
│  │  └───────────────┘  └───────────────┘  └───────────────────────┘   │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### Presentation Layer

The **CLI Agent** provides the primary entry point for users. It handles argument parsing, command routing, and output formatting.

The **API Layer** provides programmatic access to all agent functionality. Functions return structured data consumed by other programs.

The **Interactive Shell** provides a REPL-like experience for exploring capabilities interactively.

### Orchestration Layer

The **IndieHackerAgent** class serves as the central orchestrator. It initializes all domain engines with sensible defaults and coordinates complex workflows.

**Initialization Flow:**
```
IndieHackerAgent(config)
  → SaaSMetricsCalculator()
  → MarketingAutomationEngine()
  → CustomerSegmenter()
  → ChurnPredictor()
  → ContentManager()
  → PricingOptimizer()
  → GrowthExperimentManager()
  → FunnelAnalyzer()
  → ProjectManager()
  → MVPTemplateEngine()
```

### Domain Engine Layer

#### SaaS Metrics Calculator

**Core Formulas:**
```
MRR = Σ (customers_per_tier × tier_price)
ARR = MRR × 12
LTV = (ARPU × Gross_Margin) / (Churn_Rate / 100)
CAC = Total_Sales_Marketing_Spend / New_Customers
LTV_CAC_Ratio = LTV / CAC
Payback_Months = CAC / (ARPU × Gross_Margin)
Quick_Ratio = (New_MRR + Expansion_MRR) / (Contraction_MRR + Churned_MRR)
```

**Growth Projection Model:**
```
For each month:
  new_mrr = current_mrr × (growth_rate / 100)
  churned_mrr = current_mrr × (churn_rate / 100)
  current_mrr = current_mrr + new_mrr - churned_mrr
```

#### Marketing Automation Engine

**Campaign Performance Estimation:**
```
estimated_opens = sent_count × open_rate
estimated_clicks = estimated_opens × click_rate
estimated_conversions = estimated_clicks × conversion_rate
revenue_generated = estimated_conversions × avg_revenue_per_conversion
```

**Automation Workflow Pattern:**
```
Trigger Event → Filter Conditions → Action Sequence → Follow-up Timing
     ↓
  user_signup → segment=new_users → send_welcome_email → wait(2 days)
                                                          ↓
                                              send_feature_highlight → ...
```

#### Customer Intelligence Layer

**Churn Risk Scoring:**
```
risk_score = Σ (factor_weight × factor_value)

Factors:
  health_score < 30      → +30 points
  engagement < 40        → +20 points
  days_inactive > 14     → +25 points
  support_tickets > 5    → +15 points

Risk Levels:
  score >= 70 → critical
  score >= 50 → high
  score >= 30 → medium
  score < 30  → low
```

**Customer Segmentation Dimensions:**
| Dimension | Criteria | Use Case |
|-----------|----------|----------|
| Behavior | health_score >= 70 | Active user targeting |
| Engagement | engagement_score >= 60 | Feature promotion |
| At-Risk | 30 <= health < 70 | Retention campaigns |
| Churned | churned_at != None | Win-back campaigns |
| Power User | engagement >= 80 | Upsell opportunities |
| Tier | plan == "pro" | Tier-specific messaging |
| Recency | last_active within N days | Re-engagement |

#### Content Management System

**SEO Scoring Algorithm:**
```
score = 0
score += min(30, keyword_count × 10)
score += min(20, word_count // 100)
score += 10 if published else 0
score += min(20, traffic // 100)
score += min(20, conversions × 2)
```

#### Pricing Optimizer

**Price Elasticity Model:**
```
demand_change = percent_price_change × elasticity × current_demand
elasticity = -1.2 (default, configurable)
new_demand = current_demand + demand_change
revenue_comparison = (new_price × new_demand) vs (current_price × current_demand)
```

**Psychological Pricing Points:**
```
charm_price = base × 0.95        (e.g., $29 → $27.55)
premium_price = base × 1.25      (e.g., $29 → $36.25)
enterprise_price = base × 5      (e.g., $29 → $145)
anchor_discount = base × 0.80    (e.g., $29 → $23.20)
```

#### Growth Experiment Manager

**Statistical Significance Test:**
```
pooled_rate = (control_rate + variant_rate) / 2
standard_error = sqrt(pooled_rate × (1 - pooled_rate) × 2 / sample_size)
z_score = |variant_rate - control_rate| / standard_error

Significance thresholds:
  90% confidence → z > 1.645
  95% confidence → z > 1.96
  99% confidence → z > 2.576
```

**Experiment Lifecycle:**
```
draft → running → completed
  ↓        ↓          ↓
  │     paused      winner determined
  │     failed      lift calculated
  └──── cancelled   significance assessed
```

#### Funnel Analyzer

**Conversion Rate Calculation:**
```
stage[i].conversion_rate = (stage[i].visitors / stage[i-1].visitors) × 100
stage[i].dropoff_rate = 100 - stage[i].conversion_rate
overall_conversion = (last_stage.visitors / first_stage.visitors) × 100
```

**Attribution Models:**
| Model | Description | Calculation |
|-------|-------------|-------------|
| First Touch | Credit to first interaction | 100% to first channel |
| Last Touch | Credit to last interaction | 100% to last channel |
| Linear | Equal credit to all touches | 1/N per channel |
| Time Decay | More credit to recent | Exponential decay |

#### Project Manager

**Task State Machine:**
```
backlog → todo → in_progress → review → done
                        ↓
                    blocked → (back to todo or in_progress)
```

**Time Tracking Integration:**
```
task.actual_hours = Σ time_entries.hours WHERE task_id = task.id
efficiency = actual_hours / estimated_hours × 100
```

#### MVP Template Engine

**Template Types and Tech Stacks:**
| Product Type | Frontend | Backend | Database | Hosting |
|-------------|----------|---------|----------|---------|
| SaaS (modern) | Next.js | Node.js + Prisma | PostgreSQL | Vercel + Railway |
| SaaS (minimal) | React + Vite | Supabase | PostgreSQL | Vercel |
| SaaS (Python) | React | FastAPI | PostgreSQL | Railway |
| API Service | N/A | FastAPI / Express | PostgreSQL | AWS Lambda |
| Mobile App | React Native | Firebase | Firestore | Firebase |
| Content Site | Next.js | Headless CMS | PostgreSQL | Vercel |
| Marketplace | Next.js | Node.js + Prisma | PostgreSQL | Railway |
| E-commerce | Next.js | Medusa / Saleor | PostgreSQL | Railway |

## Data Model Layer

### Core Data Structures

**Customer**: Business customer with subscription details, acquisition info, engagement history, and computed metrics.

**Task**: Unit of work with status workflow, priority, time estimates, and dependencies.

**TimeEntry**: Records time spent on a specific task with description, hours, date, and billable status.

**PricingTier**: Subscription level with price, features, limits, and popular flag.

**EmailCampaign**: Email marketing campaign with content, segment, and performance tracking.

**ContentPiece**: Marketing content with SEO metadata, keywords, and performance statistics.

**GrowthExperiment**: A/B test definition with hypothesis, variants, and results.

**FunnelStage**: Conversion funnel stage with visitor counts and computed rates.

### Data Relationships

```
Project 1──N Task
Task 1──N TimeEntry
Task N──N Task (dependencies)
Customer N──1 PricingTier
Customer 1──N EmailCampaign (via segment)
EmailCampaign N──1 Sequence
Funnel 1──N FunnelStage
GrowthExperiment 1──N ExperimentResult
ContentPiece N──N Keyword
```

## Foundation Services

**UUID Generation**: All entities receive unique identifiers using UUID v4.

**Date/Time Handling**: All temporal data uses the datetime module. ISO 8601 format.

**Serialization**: Dictionary-based APIs enable easy JSON serialization.

**Logging**: Structured logging throughout all engines for debugging and audit trails.

**Error Handling**: All errors returned as structured dictionaries with "error" key.

## Design Patterns

**Facade Pattern**: IndieHackerAgent presents simplified interface to complex engine interactions.

**Strategy Pattern**: Rate limiting, attribution modeling, and statistical analysis use swappable algorithms.

**Observer Pattern**: Event distribution enables cross-engine reactions without tight coupling.

**Factory Pattern**: Templates and configurations created through factory methods.

**Repository Pattern**: Engine classes maintain internal registries for data storage.

**State Machine**: Task and campaign statuses follow defined state transitions.

## Data Flow Examples

### Customer Health Update Flow
```
1. Customer data received
2. Segmenter updates segment assignments
3. Churn predictor recalculates risk score
4. If risk changes → event triggered
5. Marketing automation activated if needed
6. Customer record updated
7. Dashboard notified for display
```

### Campaign Execution Flow
```
1. Campaign parameters validated
2. Eligible recipients identified
3. Status updated to sending
4. Delivery statistics recorded
5. Open/click tracking enabled
6. Follow-up campaigns scheduled
7. Results aggregated for reporting
```

### Experiment Analysis Flow
```
1. Sample size threshold verified
2. Conversion rates calculated per variant
3. Statistical significance evaluated
4. Winner determined
5. Results stored, recommendations generated
6. Winning variant optionally applied
7. Reports updated
```

## Configuration Management

**Default Configuration**: All engines initialize with sensible defaults.

**Agent Configuration**: IndieHackerAgent accepts custom config overriding defaults.

**Per-Engine Configuration**: Individual engines configurable independently.

## Security Considerations

**Data Encapsulation**: Internal attributes use underscore prefixes.

**Input Validation**: All external inputs validated before use.

**Error Handling**: Structured error responses, no crashes.

**No External Dependencies**: Core system has minimal dependencies.

## Performance Characteristics

**Memory Efficiency**: Appropriate types, no unnecessary duplication.

**Computational Efficiency**: Optimized algorithms for projections and statistics.

**Initialization Time**: Fast initialization for automated workflows.

**Scalability**: Supports businesses from $0 to $10M+ revenue.

## Extension Points

**Custom Engines**: New domain engines via engine interface registration.

**Custom Templates**: MVP templates extended via template generator interface.

**Custom Integrations**: External systems via adapter patterns.

**Custom Reports**: Additional reporting via report generators.

## Deployment Considerations

**Local Development**: CLI interface for full local functionality.

**Automation Scripts**: Programmatic APIs for CI/CD pipelines.

**Server Deployment**: Long-running service for web access.

**Containerization**: Minimal dependencies for straightforward containerization.

## Future Evolution

**Data Persistence**: Persistence layers for historical data.

**Multi-Tenancy**: Multiple independent businesses from one instance.

**Team Collaboration**: Role-based access for small teams.

**Advanced Analytics**: Machine learning for predictive recommendations.

## Comparison with Alternatives

| Approach | Advantage | Trade-off |
|----------|-----------|-----------|
| vs. Microservices | Better performance, simpler deployment | Less independent scaling |
| vs. Monolith | Independent development and testing | More initial complexity |
| vs. Point Solutions | Integrated data flow between domains | Single codebase dependency |
| vs. Config-Based | Greater flexibility and type safety | Less non-developer accessibility |

---

## Data Flow Diagrams

### Revenue Calculation Flow

```
Customer Data ──► SaaS Metrics Calculator ──► Dashboard
      │                      │
      │              ┌───────┴───────┐
      │              │               │
      │         MRR Calc         LTV Calc
      │              │               │
      │         Tier × Count   ARPU / Churn
      │              │               │
      │              └───────┬───────┘
      │                      │
      │              ┌───────┴───────┐
      │              │               │
      │         ARR Calc        CAC Calc
      │              │               │
      │         MRR × 12      Spend / Customers
      │              │               │
      │              └───────┬───────┘
      │                      │
      │              ┌───────┴───────┐
      │              │               │
      │         Payback         Quick Ratio
      │         Calc             Calc
      │              │               │
      │         CAC / ARPU    (New + Exp) / (Contr + Churn)
      │              │               │
      └──────────────┴───────────────┘
                     │
              Full Status Report
```

### Experiment Lifecycle Flow

```
Create Experiment
       │
       ▼
  ┌─────────┐
  │  Draft  │
  └────┬────┘
       │ start_experiment()
       ▼
  ┌──────────┐
  │ Running  │◄─────────────────────┐
  └────┬─────┘                      │
       │ record_result()            │ pause_experiment()
       ▼                            │
  ┌──────────┐                      │
  │ Paused   │──────────────────────┘
  └────┬─────┘
       │ complete_experiment()
       ▼
  ┌───────────┐
  │ Completed │
  └────┬──────┘
       │
       ▼
  ┌───────────┐
  │  Results  │
  │  Analyzed │
  └───────────┘
```

---

## API Rate Limiting

### Rate Limit Configuration

```python
rate_limits = {
    "metrics.calculate_mrr": {
        "max_requests": 100,
        "window_seconds": 60,
        "strategy": "sliding_window",
    },
    "marketing.launch_campaign": {
        "max_requests": 10,
        "window_seconds": 3600,
        "strategy": "fixed_window",
    },
    "funnel.analyze_funnel": {
        "max_requests": 50,
        "window_seconds": 60,
        "strategy": "token_bucket",
    },
}
```

### Backoff Strategy

```
Attempt 1: Wait 1 second
Attempt 2: Wait 2 seconds
Attempt 3: Wait 4 seconds
Attempt 4: Wait 8 seconds
Attempt 5: Wait 16 seconds
Max Wait:  60 seconds

Rate Limit Headers:
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 45
  X-RateLimit-Reset: 1704067200
```

---

## Disaster Recovery

### Backup Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                  Backup Schedule                             │
├──────────────────┬──────────────┬───────────────────────────┤
│ Data Type        │ Frequency    │ Retention                 │
├──────────────────┼──────────────┼───────────────────────────┤
│ Customer Data    │ Hourly       │ 30 days                   │
│ Metrics Data     │ Daily        │ 90 days                   │
│ Campaign Data    │ Daily        │ 60 days                   │
│ Experiment Data  │ On completion│ Permanent                 │
│ Funnel Data      │ Daily        │ 90 days                   │
│ Content Data     │ Daily        │ 30 days                   │
│ Configuration    │ On change    │ Permanent                 │
└──────────────────┴──────────────┴───────────────────────────┘
```

### Recovery Procedures

```
RTO (Recovery Time Objective): 4 hours
RPO (Recovery Point Objective): 1 hour

Recovery Steps:
  1. Assess damage scope (< 15 min)
  2. Restore from latest backup (< 1 hour)
  3. Replay transaction logs (< 2 hours)
  4. Verify data integrity (< 30 min)
  5. Resume operations (< 15 min)
```

---

## Code Quality Standards

### Linting Rules

```python
# .flake8 configuration
[flake8]
max-line-length = 120
max-complexity = 10
max-args = 8
exclude = .git,__pycache__,build,dist
per-file-ignores =
    __init__.py:F401
    tests/*:S101
```

### Type Hints Enforcement

```python
# All public methods must have full type hints
def calculate_mrr(
    self,
    customers_by_tier: Dict[str, int],
    pricing: Dict[str, float],
) -> float:
    """Calculate Monthly Recurring Revenue."""
    pass

# Return types are mandatory
def get_customer_health(self, customer_id: str) -> Dict[str, Any]:
    """Get customer health score and breakdown."""
    pass
```

---

## Error Handling and Recovery

### Error Response Structure

```python
@dataclass
class ErrorResponse:
    error_code: str          # "VALIDATION_ERROR"
    error_type: str          # "ValidationError"
    message: str             # Human-readable description
    details: Dict[str, Any]  # Context-specific data
    timestamp: datetime      # When error occurred
    request_id: Optional[str]  # For correlation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": {
                "code": self.error_code,
                "type": self.error_type,
                "message": self.message,
                "details": self.details,
                "timestamp": self.timestamp.isoformat(),
                "request_id": self.request_id,
            }
        }
```

### Common Error Codes

| Error Code | Type | Description |
|------------|------|-------------|
| INVALID_EMAIL | ValidationError | Email format invalid |
| DUPLICATE_CUSTOMER | ValidationError | Customer already exists |
| NEGATIVE_MRR | ValidationError | MRR cannot be negative |
| INSUFFICIENT_DATA | ValidationError | Not enough data for calculation |
| EXPERIMENT_NOT_RUNNING | StateError | Experiment must be running to record result |
| TASK_DEPENDENCY_CYCLE | StateError | Circular dependency detected |
| FUNNEL_STAGE_MISSING | ValidationError | Funnel stages must be sequential |
| PRICE_INVALID | ValidationError | Price must be positive |

### Retry Strategy

```python
# Configure retry for transient failures
retry_config = {
    "max_retries": 3,
    "backoff_strategy": "exponential",
    "base_delay": 1.0,  # seconds
    "max_delay": 30.0,  # seconds
    "retryable_errors": [
        "ConnectionError",
        "TimeoutError",
        "RateLimitError",
    ],
}
```

---

## Security Best Practices

### Input Validation

```python
# Validate all external inputs
def validate_customer_input(data: Dict) -> Dict[str, str]:
    errors = {}

    if not data.get("email"):
        errors["email"] = "Email is required"
    elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', data["email"]):
        errors["email"] = "Invalid email format"

    if not data.get("name"):
        errors["name"] = "Name is required"
    elif len(data["name"]) > 100:
        errors["name"] = "Name too long (max 100 chars)"

    if data.get("plan") and data["plan"] not in ["starter", "pro", "enterprise"]:
        errors["plan"] = "Invalid plan"

    return errors
```

### Data Encryption

```python
# Encrypt sensitive data at rest
from cryptography.fernet import Fernet

class DataEncryptor:
    def __init__(self, key: bytes):
        self.cipher = Fernet(key)

    def encrypt(self, data: str) -> str:
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted: str) -> str:
        return self.cipher.decrypt(encrypted.encode()).decode()

# Usage
encryptor = DataEncryptor(settings.ENCRYPTION_KEY)
encrypted_email = encryptor.encrypt("user@example.com")
```

### API Security Headers

```python
# Security headers for API responses
security_headers = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "DENY",
    "X-XSS-Protection": "1; mode=block",
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
}
```

---

## Testing Strategy

### Unit Test Coverage

```python
# Test SaaS Metrics Calculator
class TestSaaSMetrics:
    def test_mrr_calculation(self):
        calc = SaaSMetricsCalculator()
        mrr = calc.calculate_mrr(
            customers_by_tier={"starter": 100, "pro": 50, "enterprise": 10},
            pricing={"starter": 29, "pro": 79, "enterprise": 199}
        )
        assert mrr == 8840.0

    def test_ltv_calculation(self):
        calc = SaaSMetricsCalculator()
        ltv = calc.calculate_ltv(arpu=88.4, gross_margin=0.8, churn_rate=5.0)
        assert ltv == 1414.4

    def test_quick_ratio(self):
        calc = SaaSMetricsCalculator()
        ratio = calc.quick_ratio(new_mrr=1000, expansion_mrr=500, contraction_mrr=200, churned_mrr=300)
        assert ratio == 3.0

# Test Marketing Engine
class TestMarketingEngine:
    def test_campaign_creation(self):
        engine = MarketingAutomationEngine()
        campaign = engine.create_campaign("Welcome", "Welcome to {product}!", "new_signups")
        assert campaign.name == "Welcome"
        assert campaign.status == "draft"

    def test_automation_workflow(self):
        engine = MarketingAutomationEngine()
        automation = engine.create_automation(
            name="Onboarding",
            trigger="user_signup",
            actions=["send_welcome", "wait_2_days", "send_features"],
        )
        assert len(automation.actions) == 3
```

### Integration Tests

```python
class TestIndieHackerIntegration:
    def test_full_customer_lifecycle(self):
        agent = IndieHackerAgent()

        # Create customer
        customer = agent.segmenter.add_customer(
            email="test@example.com",
            name="Test User",
            plan="starter",
        )

        # Track metrics
        agent.metrics.track_mrr_change(29.0, "new_subscription")

        # Create campaign
        campaign = agent.marketing_engine.create_campaign("Welcome", "Welcome!", "new_signups")

        # Analyze funnel
        funnel = agent.funnel.create_funnel("Signup", [
            {"name": "Landing", "visitors": 1000},
            {"name": "Signup", "visitors": 100},
        ])

        # Get status
        status = agent.full_status()
        assert status["customers"] >= 1
```

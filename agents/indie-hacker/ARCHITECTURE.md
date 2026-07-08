# Indie Hacker Agent Architecture

## Executive Summary

The Indie Hacker Agent is a comprehensive, modular software platform designed to empower solo entrepreneurs and indie hackers with enterprise-grade business tools. This document provides a detailed architectural overview of the system, explaining how its components interact to deliver business intelligence, marketing automation, customer relationship management, and development workflow capabilities.

The architecture follows a layered design pattern with clear separation of concerns, enabling each subsystem to operate independently while contributing to a cohesive user experience. The system is built with Python 3.8+ and leverages modern programming concepts including dataclasses for data modeling, enumerated types for state management, and object-oriented principles for component encapsulation.

This architecture document is intended for developers who need to understand the system's structure, maintainers who will extend the platform's capabilities, and technical stakeholders who require insight into the design decisions that shape the agent's functionality.

## System Overview

The Indie Hacker Agent serves as a centralized platform for managing all aspects of an indie software business. Unlike point solutions that address individual needs, this agent provides an integrated approach where data and insights flow seamlessly between different functional areas. When you record a task completion, it affects your project progress metrics. When a customer's health score changes, it triggers appropriate marketing automation workflows. This integration is achieved through a shared data model and well-defined interfaces between components.

The system can be conceptually divided into eight major functional domains, each handled by specialized engines that encapsulate domain logic and provide services to the rest of the system. These domains are business metrics and financial analysis, marketing automation, customer intelligence, content management, pricing optimization, growth experimentation, funnel analysis, and project management.

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

The presentation layer encompasses all interfaces through which users interact with the agent. While the current implementation focuses on a command-line interface and programmatic API, the architecture is designed to support additional presentation modes such as web dashboards, API endpoints, and integration with external tools.

The **CLI Agent** component provides the primary entry point for users. It handles argument parsing, command routing, and output formatting. The main function serves as the bootstrap mechanism that instantiates the agent and dispatches user commands to appropriate handlers. Output formatting is designed to be readable in terminal environments while remaining parseable by automation scripts.

The **API Layer** provides programmatic access to all agent functionality. Functions are designed to return structured data that can be consumed by other programs, integration tools, or custom user interfaces. All public methods return dictionaries with consistent key naming, enabling predictable access patterns.

The **Interactive Shell** provides a REPL-like experience for exploring the agent's capabilities interactively. It supports command history, tab completion, and contextual help.

### Orchestration Layer

The **IndieHackerAgent** class serves as the central orchestrator for all system components. This class is instantiated with optional configuration and initializes all domain engines with sensible defaults. The orchestrator maintains references to all engines and coordinates complex workflows that span multiple domains.

Key responsibilities of the orchestration layer include initialization of default configurations, cross-engine data flow management, workflow triggers and automation, event distribution when significant changes occur, and lifecycle management for projects and campaigns. The orchestrator implements the facade pattern, presenting a simplified interface to users while hiding the complexity of coordinating multiple specialized engines.

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

Each domain engine encapsulates all logic related to a specific business function. Engines are designed to be largely independent, enabling development and testing in isolation, while still participating in the broader system through well-defined interfaces.

#### SaaS Metrics Calculator

The **SaaSMetricsCalculator** engine handles all financial calculations relevant to subscription businesses. It maintains a history of metrics calculations for trend analysis and supports projection of future performance based on various scenarios.

The engine implements formulas from established SaaS finance practices:

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

The engine provides sophisticated projection capabilities through its project_growth method, which accepts current MRR, expected growth rate, expected churn rate, and a number of months to project.

#### Marketing Automation Engine

The **MarketingAutomationEngine** manages all email marketing and campaign automation functionality. It maintains registries of campaigns, sequences, automations, and triggers, enabling complex multi-step marketing workflows.

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

The **CustomerSegmenter**, **ChurnPredictor**, and related classes form the customer intelligence subsystem. These components work together to maintain a comprehensive view of each customer and provide actionable insights.

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

The **ContentManager** tracks all content marketing efforts including blog posts, landing pages, email copy, and social media content. It maintains metadata about each piece including keywords, word count, publication status, and performance metrics.

**SEO Scoring Algorithm:**
```
score = 0
score += min(30, keyword_count × 10)           # Keyword bonus
score += min(20, word_count // 100)             # Word count bonus
score += 10 if published else 0                 # Publication bonus
score += min(20, traffic // 100)                # Traffic bonus
score += min(20, conversions × 2)              # Conversion bonus
```

#### Pricing Optimizer

The **PricingOptimizer** manages pricing strategy including tier definitions, competitive analysis, and psychological pricing calculations.

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

The **GrowthExperimentManager** provides a structured framework for running A/B tests and growth experiments.

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

The **FunnelAnalyzer** tracks conversion funnels and provides detailed analysis of drop-off points.

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

The **ProjectManager** provides lightweight project and task management tailored for solo founders.

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

The **MVPTemplateEngine** generates appropriate development plans based on product type and requirements.

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

The data model layer defines all structures used throughout the system. These structures are implemented using Python dataclasses, which provide automatic initialization, representation, and comparison methods.

### Core Data Structures

**Customer**: Represents a business customer with their subscription details, acquisition information, engagement history, and computed metrics.

**Task**: Represents a unit of work within a project with status workflow, priority, time estimates, and dependencies.

**TimeEntry**: Records time spent on a specific task with description, hours, date, and billable status.

**PricingTier**: Defines a subscription level with price, features, limits, and popular flag.

**EmailCampaign**: Represents an email marketing campaign with content, segment, and performance tracking.

**ContentPiece**: Tracks marketing content with SEO metadata, keywords, and performance statistics.

**GrowthExperiment**: Captures A/B test definition with hypothesis, variants, and results.

**FunnelStage**: Defines a conversion funnel stage with visitor counts and computed rates.

**Feature**: Represents a product feature with priority, status, and acceptance criteria.

**UserPersona**: Customer persona with demographics, goals, pain points, and behaviors.

**MVPComponent**: Component of an MVP with technology suggestion and complexity estimate.

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

**UUID Generation**: All entities receive unique identifiers using UUID v4, ensuring global uniqueness.

**Date/Time Handling**: All temporal data uses the datetime module. Date formats follow ISO 8601 for consistency.

**Serialization**: Dictionary-based APIs enable easy JSON serialization. Consistent return structures across all methods.

**Logging**: Structured logging throughout all engines for debugging and audit trails.

**Error Handling**: All errors returned as structured dictionaries with "error" key, never raised as exceptions.

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

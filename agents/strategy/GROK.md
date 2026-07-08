---
name: "Strategy Agent"
version: "2.0.0"
description: "Strategic planning, competitive analysis, OKR management, risk assessment, scenario planning, business model canvas, and market intelligence"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["strategy", "planning", "competitive", "okr", "risk", "scenario", "bmc"]
category: "strategy"
personality: "strategist"
use_cases:
  - "strategic-planning"
  - "competitive-analysis"
  - "okr-management"
  - "risk-assessment"
  - "scenario-planning"
  - "market-analysis"
  - "business-model-canvas"
  - "swot-analysis"
  - "scenario-analysis"
---

# Strategy Agent

> Strategic planning, competitive intelligence, OKR management, risk assessment, scenario planning, and business model analysis.

## Identity

The Strategy Agent is a comprehensive business intelligence and strategic planning platform. It manages OKRs with key result tracking, performs SWOT analysis with TOWS strategy generation, tracks competitive landscape with battle cards, assesses strategic risks with mitigation tracking, builds and evaluates scenarios, analyzes market segments, and designs business model canvases.

**Core principle:** Strategy without measurement is just philosophy. Every objective has a key result. Every risk has a score. Every scenario has a probability.

**Personality:** The agent is a methodical, analytical strategist who balances rigorous data analysis with practical business insight. It prioritizes evidence over intuition, completeness over speed, and actionable recommendations over theoretical frameworks.

## Principles

1. **Measure What Matters** - OKRs with quantifiable key results
2. **Know Your Competition** - Battle cards, not assumptions
3. **Assess Risk Honestly** - Probability × Impact, not optimism
4. **Plan for Multiple Futures** - Best, base, and worst case scenarios
5. **Market-Driven Decisions** - Segment data guides resource allocation
6. **Business Model Clarity** - 9-block canvas forces completeness
7. **Execution Focus** - Strategy without execution is hallucination
8. **Continuous Learning** - Update strategies based on outcomes

## Capabilities

### 1. OKR Management (StrategicPlanner)

```python
from agents.strategy.agent import StrategicPlanner, StrategicPriority

planner = StrategicPlanner()

# Create objective with key results
obj = planner.create_objective(
    title="Achieve Product-Market Fit",
    description="Validate product-market fit in target segment",
    priority=StrategicPriority.GROWTH,
    key_results=[
        {
            "description": "Reach 10K MAU",
            "metric": "mau",
            "target_value": 10000,
            "current_value": 3500,
            "unit": "users"
        },
        {
            "description": "NPS > 50",
            "metric": "nps",
            "target_value": 50,
            "current_value": 32,
            "unit": "score"
        },
        {
            "description": "Retention > 40%",
            "metric": "retention",
            "target_value": 0.40,
            "current_value": 0.28,
            "unit": "rate"
        },
    ],
    target_date=datetime(2025, 6, 30),
    owner="product-team",
    budget=150000.0,
)
# obj.id = "obj_a1b2c3"
# obj.progress = 0.35 (avg of KR progress)

# Update key result
updated_kr = planner.update_key_result(
    obj.id,
    obj.key_results[0].id,
    current_value=5200
)
# updated_kr.progress = 0.52

# Add initiative
initiative = planner.add_initiative(
    objective_id=obj.id,
    name="User Research Sprint",
    description="Conduct 50 user interviews",
    linked_key_results=[obj.key_results[2].id]
)

# Get timeline status
timeline = planner.get_timeline_status(obj.id)
# {
#   "objective_id": "obj_a1b2c3",
#   "days_elapsed": 45,
#   "total_days": 180,
#   "expected_progress": 0.25,
#   "actual_progress": 0.35,
#   "status": "ahead",
#   "trend": "improving"
# }

# Get objectives by priority
growth_objs = planner.get_objectives_by_priority(StrategicPriority.GROWTH)
# [StrategicObjective(...), ...]

# Get full OKR summary
summary = planner.get_okr_summary()
# {
#   "total_objectives": 8,
#   "by_status": {"completed": 2, "on_track": 3, "in_progress": 2, "at_risk": 1},
#   "avg_progress": 0.62,
#   "budget_utilization": 0.45
# }
```

**Status Derivation:**
| Progress | Status | Color | Action |
|----------|--------|-------|--------|
| >= 100% | COMPLETED | Green | Celebrate, document learnings |
| >= 70% | ON_TRACK | Blue | Continue current trajectory |
| >= 30% | IN_PROGRESS | Yellow | Monitor and adjust |
| < 30% | AT_RISK | Red | Escalate and re-plan |

### 2. SWOT Analysis

```python
from agents.strategy.agent import SWOTAnalyzer

swot = SWOTAnalyzer()

# Perform SWOT analysis
analysis = swot.analyze(
    strengths=[
        "Strong engineering team",
        "Proprietary technology patent",
        "Established brand recognition"
    ],
    weaknesses=[
        "Limited marketing budget",
        "Small sales team",
        "No enterprise features"
    ],
    opportunities=[
        "Growing market (+15% CAGR)",
        "AI adoption accelerating",
        "Competitor weakness in support"
    ],
    threats=[
        "New well-funded competitors",
        "Regulatory changes pending",
        "Economic downturn risk"
    ],
    context="SaaS security startup entering enterprise market"
)
# {
#   "scores": {
#     "strengths_score": 30,
#     "weaknesses_score": 25,
#     "opportunities_score": 35,
#     "threats_score": 20
#   },
#   "overall_score": 5.0,
#   "strategies": {
#     "so_strategies": [
#       "Leverage engineering team to capture AI adoption opportunity",
#       "Use patent portfolio to differentiate against new competitors"
#     ],
#     "wo_strategies": [
#       "Address enterprise features gap to capture growing market",
#       "Build sales team to capitalize on competitor support weakness"
#     ],
#     "st_strategies": [
#       "Use brand recognition to maintain position against new entrants",
#       "Leverage technology patents to block competitor features"
#     ],
#     "wt_strategies": [
#       "Partner with established players to reduce market entry risk",
#       "Focus on SMB segment to avoid enterprise regulatory burden"
#     ]
#   },
#   "recommendations": [
#     "Prioritize enterprise feature development",
#     "Invest in sales team expansion",
#     "Monitor regulatory changes closely"
#   ]
# }

# Compare to previous analysis
comparison = swot.get_comparative_analysis()
# {
#   "current": {...},
#   "previous": {...},
#   "changes": {
#     "strengths": ["+1 new strength", "-0 removed"],
#     "threats": ["+1 new threat"]
#   }
# }
```

**TOWS Strategy Matrix:**
| | Opportunities | Threats |
|---|---|---|
| **Strengths** | SO: Leverage strengths to capture opportunities | ST: Use strengths to counter threats |
| **Weaknesses** | WO: Address weaknesses to exploit opportunities | WT: Minimize weaknesses to avoid threats |

### 3. Competitive Intelligence

```python
from agents.strategy.agent import CompetitiveAnalyzer, CompetitivePosition

comp = CompetitiveAnalyzer()

# Add competitor
competitor = comp.add_competitor(
    name="RivalCorp",
    position=CompetitivePosition.LEADER,
    market_share=35.0,
    strengths=["Brand recognition", "Distribution network", "Enterprise relationships"],
    weaknesses=["High pricing", "Slow innovation", "Poor support"],
    pricing="Premium",
    recent_moves=["Launched new product line", "Acquired smaller competitor"]
)
# competitor.id = "comp_xyz789"

# Track competitor move
comp.add_competitor_move(
    competitor.id,
    {
        "type": "product_launch",
        "description": "Enterprise Security Suite v2.0",
        "date": "2025-01-15",
        "impact": "high"
    }
)

# Generate battle card
card = comp.generate_battle_card(competitor.id)
# {
#   "competitor": "RivalCorp",
#   "position": "leader",
#   "market_share": 35.0,
#   "talk_track": [
#     "RivalCorp is the market leader but has known weaknesses",
#     "Their pricing is 30% higher than alternatives",
#     "Support response times average 48 hours vs our 4 hours"
#   ],
#   "differentiators": [
#     "We offer AI-powered automation they lack",
#     "Our pricing is transparent and predictable",
#     "24/7 support included in all plans"
#   ],
#   "objection_handling": {
#     "They're the market leader": "Market share doesn't equal fit. Our customers report 40% faster deployment.",
#     "They have more features": "Features without adoption are shelfware. Our UX scores 4.5/5 vs their 3.2/5."
#   },
#   "win_strategy": "Focus on TCO and time-to-value"
# }

# Get competitive landscape
landscape = comp.get_competitive_landscape()
# {
#   "total_competitors": 8,
#   "by_position": {"leader": 1, "challenger": 2, "follower": 4, "niche": 1},
#   "total_market_share": 100.0,
#   "our_position": "challenger",
#   "our_market_share": 15.0,
#   "biggest_threat": "RivalCorp",
#   "opportunity": "Niche player weakness in enterprise"
# }
```

**Competitive Positions:**
| Position | Description | Strategy |
|----------|-------------|----------|
| Leader | Highest market share, sets standards | Defend and expand |
| Challenger | Strong #2, actively gaining share | Attack weaknesses |
| Follower | Maintains position, imitates leaders | Selective differentiation |
| Niche | Focused on specific segment | Deepen specialization |

### 4. Risk Management

```python
from agents.strategy.agent import RiskManager

rm = RiskManager()

# Add risk
risk = rm.add_risk(
    name="Market disruption by new technology",
    category="market",
    probability=0.3,
    impact=0.8,
    description="AI-powered security tools could displace current offering",
    owner="strategy-team",
    triggers=["Competitor AI product launch", "VC funding for AI startups"]
)
# risk.risk_score = 2.4
# risk.level = RiskLevel.MEDIUM

# Add mitigation
rm.add_mitigation(risk.id, "Invest $2M in AI R&D over 18 months")
rm.add_mitigation(risk.id, "Partner with AI startups for integration")
rm.add_mitigation(risk.id, "Hire AI/ML engineering team")

# Update risk as situation changes
updated_risk = rm.update_risk(
    risk.id,
    probability=0.5,  # Increased due to market signals
    impact=0.8
)
# updated_risk.risk_score = 4.0
# updated_risk.level = RiskLevel.HIGH

# Get risk register
register = rm.get_risk_register()
# {
#   "total_risks": 12,
#   "by_level": {"critical": 1, "high": 3, "medium": 5, "low": 3},
#   "total_exposure": 24.5,
#   "top_risks": [...],
#   "mitigated_risks": 8
# }

# Get top risks
top = rm.get_top_risks(limit=5)
# [
#   {"name": "Market disruption", "score": 4.0, "level": "HIGH"},
#   {"name": "Key talent departure", "score": 3.5, "level": "MEDIUM"},
#   ...
# ]
```

**Risk Scoring:**
| Score | Level | Response Time |
|-------|-------|---------------|
| >= 12 | CRITICAL | 24 hours |
| >= 8 | HIGH | 1 week |
| >= 4 | MEDIUM | 1 month |
| < 4 | LOW | Quarterly review |

### 5. Scenario Planning

```python
from agents.strategy.agent import ScenarioPlanner, ScenarioType

sp = ScenarioPlanner()

# Create scenarios
sp.create_scenario(
    name="Aggressive Growth",
    scenario_type=ScenarioType.BEST_CASE,
    assumptions=["Market grows 25%", "No new competitors", "Successful product launch"],
    impacts={"revenue": 2.5, "market_share": 15.0, "employees": 50},
    probability=0.2,
    triggers=["Market expansion report", "Competitor exit"]
)

sp.create_scenario(
    name="Steady State",
    scenario_type=ScenarioType.BASE_CASE,
    assumptions=["Market grows 10%", "Minor competition", "Incremental improvements"],
    impacts={"revenue": 1.2, "market_share": 5.0, "employees": 20},
    probability=0.5,
    triggers=[]
)

sp.create_scenario(
    name="Market Contraction",
    scenario_type=ScenarioType.WORST_CASE,
    assumptions=["Recession", "Price pressure", "Major competitor entry"],
    impacts={"revenue": -0.5, "market_share": -5.0, "employees": -10},
    probability=0.3,
    mitigation=["Cost reduction plan", "Diversify revenue streams", "Focus on retention"]
)

# Evaluate scenarios
evaluation = sp.evaluate_scenarios()
# {
#   "total_scenarios": 3,
#   "expected_values": {
#     "revenue": 1.05,
#     "market_share": 4.0,
#     "employees": 12
#   },
#   "risk_adjusted_return": 0.85,
#   "scenario_distribution": {"best": 0.2, "base": 0.5, "worst": 0.3}
# }

# Get strategy recommendation
recommendation = sp.recommend_strategy()
# {
#   "recommended_approach": "balanced_growth",
#   "rationale": "Expected value positive but significant downside risk",
#   "actions": [
#     "Invest in growth but maintain cash reserves",
#     "Diversify revenue streams to reduce concentration risk",
#     "Build flexible cost structure for downside scenarios"
#   ],
#   "hedging_strategies": [
#     "Lock in long-term contracts with key customers",
#     "Maintain 6-month operating runway"
#   ]
# }
```

**Scenario Types:**
| Type | Description | Probability Range |
|------|-------------|-------------------|
| BEST_CASE | Optimistic outcome | 10-25% |
| BASE_CASE | Most likely outcome | 40-60% |
| WORST_CASE | Pessimistic outcome | 15-35% |

### 6. Market Analysis

```python
from agents.strategy.agent import MarketAnalyzer, MarketPhase

market = MarketAnalyzer()

# Add market segment
market.add_segment(
    name="Enterprise Security",
    size=50_000_000_000,  # $50B
    growth_rate=0.12,     # 12% CAGR
    phase=MarketPhase.GROWTH,
    trends=["Zero trust adoption", "Cloud migration", "AI-powered threats"],
    barriers=["High compliance requirements", "Long sales cycles", "Entrenched vendors"],
    competitors=["RivalCorp", "SecureInc", "CyberDefend"]
)
# segment.id = "seg_abc123"
# segment.opportunity_score = 78.5

# Add more segments
market.add_segment(
    name="SMB Security",
    size=10_000_000_000,  # $10B
    growth_rate=0.18,     # 18% CAGR
    phase=MarketPhase.GROWTH,
    trends=["DIY security", "Managed services", "Compliance pressure"],
    barriers=["Price sensitivity", "Limited budget", "Low awareness"]
)

# Get top opportunities
top = market.get_top_opportunities(limit=3)
# [
#   {
#     "name": "SMB Security",
#     "size": 10000000000,
#     "growth_rate": 0.18,
#     "opportunity_score": 82.3,
#     "phase": "growth"
#   },
#   {
#     "name": "Enterprise Security",
#     "size": 50000000000,
#     "growth_rate": 0.12,
#     "opportunity_score": 78.5,
#     "phase": "growth"
#   }
# ]

# Get market summary
summary = market.get_market_summary()
# {
#   "total_market_size": 60000000000,
#   "segments": 2,
#   "avg_growth_rate": 0.15,
#   "by_phase": {"growth": 2},
#   "top_opportunity": "SMB Security",
#   "recommendations": [
#     "SMB segment offers faster growth with lower barriers",
#     "Enterprise segment larger but more competitive"
#   ]
# }
```

**Market Phases:**
| Phase | Characteristics | Strategy |
|-------|-----------------|----------|
| Introduction | Low share, high investment, no profits | Educate and innovate |
| Growth | Rising share, growing demand, early profits | Invest and expand |
| Maturity | Stable share, price competition, peak profits | Defend and optimize |
| Decline | Falling share, decreasing demand | Harvest or divest |

### 7. Business Model Canvas

```python
from agents.strategy.agent import BusinessModelCanvas, BusinessModelBlock

bmc = BusinessModelCanvas()

# Create business model
model = bmc.create_model(
    name="SaaS Platform",
    blocks={
        BusinessModelBlock.CUSTOMER_SEGMENTS: [
            "Enterprise (1000+ employees)",
            "Mid-market (100-999 employees)",
            "SMB (10-99 employees)"
        ],
        BusinessModelBlock.VALUE_PROPOSITIONS: [
            "AI-powered security automation",
            "Real-time threat monitoring",
            "Compliance automation",
            "24/7 expert support"
        ],
        BusinessModelBlock.CHANNELS: [
            "Direct sales team",
            "Partner/reseller network",
            "Content marketing",
            "Product-led growth"
        ],
        BusinessModelBlock.CUSTOMER_RELATIONSHIPS: [
            "Self-service portal",
            "Dedicated customer success",
            "Community forums",
            "24/7 support"
        ],
        BusinessModelBlock.REVENUE_STREAMS: [
            "Monthly subscription (80%)",
            "Professional services (15%)",
            "Training and certification (5%)"
        ],
        BusinessModelBlock.KEY_RESOURCES: [
            "AI/ML platform",
            "Security research team",
            "Customer data",
            "Brand and reputation"
        ],
        BusinessModelBlock.KEY_ACTIVITIES: [
            "Product development",
            "Threat research",
            "Customer success",
            "Sales and marketing"
        ],
        BusinessModelBlock.KEY_PARTNERSHIPS: [
            "Cloud providers (AWS, Azure)",
            "Technology integrations",
            "Channel partners",
            "Compliance auditors"
        ],
        BusinessModelBlock.COST_STRUCTURE: [
            "R&D (40%)",
            "Sales and marketing (25%)",
            "Infrastructure (20%)",
            "G&A (15%)"
        ],
    }
)
# model.value_score = 78.5
# model.completeness = 0.95

# Compare models
comparison = bmc.compare_models(model.id, "competitor_model_id")
# {
#   "model_1": "SaaS Platform",
#   "model_2": "Competitor Model",
#   "value_score_diff": 12.5,
#   "strengths_over_competitor": [
#     "Stronger AI/ML capabilities",
#     "Better customer support offering"
#   ],
#   "weaknesses_vs_competitor": [
#     "Smaller partner network",
#     "Limited brand recognition"
#   ]
# }
```

**BMC Blocks:**
| Block | Description | Scoring |
|-------|-------------|---------|
| Customer Segments | Target customer groups | 0-15 |
| Value Propositions | Core value delivered | 0-20 |
| Channels | Distribution methods | 0-10 |
| Customer Relationships | Interaction types | 0-10 |
| Revenue Streams | Income sources | 0-15 |
| Key Resources | Critical assets | 0-10 |
| Key Activities | Essential operations | 0-10 |
| Key Partnerships | Strategic alliances | 0-5 |
| Cost Structure | Major cost drivers | 0-5 |

### 8. Unified Dashboard

```python
agent = StrategyAgent()
dashboard = agent.get_strategy_dashboard()
# {
#   "health_score": 72.5,
#   "metrics": {
#     "objective_completion": "45%",
#     "risk_exposure": "35%",
#     "market_opportunity": "78.5",
#     "competitive_position": "challenger"
#   },
#   "objectives": {
#     "total": 8,
#     "by_health": {
#       "completed": 2,
#       "on_track": 3,
#       "in_progress": 2,
#       "at_risk": 1
#     }
#   },
#   "risks": {
#     "total": 12,
#     "critical": 1,
#     "high": 3,
#     "exposure": 24.5
#   },
#   "market": {
#     "segments": 2,
#     "total_addressable": 60000000000,
#     "top_opportunity": "SMB Security"
#   },
#   "scenarios": {
#     "total": 3,
#     "expected_revenue": 1.05,
#     "risk_adjusted_return": 0.85
#   },
#   "competitive": {
#     "competitors": 8,
#     "our_share": 15.0,
#     "market_leader": "RivalCorp"
#   },
#   "recommendations": [
#     "Focus on SMB segment for faster growth",
#     "Address enterprise feature gap",
#     "Invest in AI capabilities"
#   ]
# }
```

## Method Signatures

```python
class StrategyAgent:
    def define_strategy(self, name: str, objectives: List[Dict]) -> Dict
    def perform_swot(self, data: Dict[str, List[str]]) -> Dict
    def assess_risks(self, risks: List[Dict]) -> Dict
    def analyze_competitors(self) -> Dict
    def get_strategy_dashboard(self) -> Dict

class StrategicPlanner:
    def create_objective(self, title: str, description: str, priority: StrategicPriority, key_results: List[Dict], target_date: datetime, owner: str, budget: Optional[float] = None) -> StrategicObjective
    def update_key_result(self, objective_id: str, kr_id: str, current_value: float) -> Optional[KeyResult]
    def add_initiative(self, objective_id: str, name: str, description: str = "", linked_key_results: Optional[List[str]] = None) -> Initiative
    def get_timeline_status(self, objective_id: str) -> Dict
    def get_objectives_by_priority(self, priority: StrategicPriority) -> List[StrategicObjective]
    def get_okr_summary(self) -> Dict

class SWOTAnalyzer:
    def analyze(self, strengths: List[str], weaknesses: List[str], opportunities: List[str], threats: List[str], context: Optional[str] = None) -> SWOTAnalysis
    def get_comparative_analysis(self) -> Optional[Dict]

class CompetitiveAnalyzer:
    def add_competitor(self, name: str, position: CompetitivePosition, market_share: float, strengths: List[str], weaknesses: List[str], pricing: Optional[str] = None) -> Competitor
    def add_competitor_move(self, competitor_id: str, move: Dict) -> Dict
    def generate_battle_card(self, competitor_id: str) -> Dict
    def get_competitive_landscape(self) -> Dict

class RiskManager:
    def add_risk(self, name: str, category: str, probability: float, impact: float, description: str, owner: Optional[str] = None) -> StrategicRisk
    def add_mitigation(self, risk_id: str, mitigation: str) -> Dict
    def update_risk(self, risk_id: str, probability: Optional[float] = None, impact: Optional[float] = None) -> Optional[StrategicRisk]
    def get_risk_register(self) -> Dict
    def get_top_risks(self, limit: int = 10) -> List[StrategicRisk]

class ScenarioPlanner:
    def create_scenario(self, name: str, scenario_type: ScenarioType, assumptions: List[str], impacts: Dict[str, float], probability: float, triggers: Optional[List[str]] = None, mitigation: Optional[List[str]] = None) -> Scenario
    def evaluate_scenarios(self) -> Dict
    def recommend_strategy(self) -> Dict

class MarketAnalyzer:
    def add_segment(self, name: str, size: float, growth_rate: float, phase: MarketPhase, trends: List[str], barriers: Optional[List[str]] = None, competitors: Optional[List[str]] = None) -> MarketSegment
    def get_top_opportunities(self, limit: int = 10) -> List[MarketSegment]
    def get_market_summary(self) -> Dict

class BusinessModelCanvas:
    def create_model(self, name: str, blocks: Dict[BusinessModelBlock, List[str]]) -> BusinessModel
    def compare_models(self, model_id_1: str, model_id_2: str) -> Dict
```

## Data Models

### StrategicObjective
| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique identifier (obj_XXXXXXXX) |
| title | str | Objective name |
| description | str | Detailed description |
| priority | StrategicPriority | GROWTH, EFFICIENCY, INNOVATION, MARKET, PRODUCT |
| status | ObjectiveStatus | NOT_STARTED, IN_PROGRESS, ON_TRACK, AT_RISK, COMPLETED |
| key_results | List[KeyResult] | Measurable outcomes |
| progress | float | 0.0-1.0 overall progress |
| owner | str | Responsible team/person |
| budget | Optional[float] | Allocated budget |
| target_date | datetime | Target completion date |

### KeyResult
| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique identifier |
| description | str | Measurable outcome |
| metric | str | Metric name |
| target_value | float | Target value |
| current_value | float | Current value |
| unit | str | Unit of measurement |
| progress | float | 0.0-1.0 (current/target) |

### StrategicRisk
| Field | Type | Description |
|-------|------|-------------|
| id | str | Risk identifier |
| name | str | Risk name |
| category | str | market, technology, operational, financial, regulatory |
| probability | float | 0.0-1.0 |
| impact | float | 0.0-1.0 |
| risk_score | float | probability × impact |
| level | RiskLevel | CRITICAL, HIGH, MEDIUM, LOW |
| description | str | Detailed description |
| owner | Optional[str] | Risk owner |
| mitigations | List[str] | Mitigation actions |

### Scenario
| Field | Type | Description |
|-------|------|-------------|
| id | str | Scenario identifier |
| name | str | Scenario name |
| scenario_type | ScenarioType | BEST_CASE, BASE_CASE, WORST_CASE |
| assumptions | List[str] | Underlying assumptions |
| impacts | Dict[str, float] | Impact per metric |
| probability | float | Likelihood of scenario |
| triggers | List[str] | Events that trigger this scenario |
| mitigation | List[str] | Mitigation actions |

### MarketSegment
| Field | Type | Description |
|-------|------|-------------|
| id | str | Segment identifier |
| name | str | Segment name |
| size | float | Total addressable market |
| growth_rate | float | Annual growth rate |
| phase | MarketPhase | INTRODUCTION, GROWTH, MATURITY, DECLINE |
| trends | List[str] | Market trends |
| barriers | List[str] | Entry barriers |
| opportunity_score | float | 0-100 |

### BusinessModel
| Field | Type | Description |
|-------|------|-------------|
| id | str | Model identifier |
| name | str | Model name |
| blocks | Dict[BusinessModelBlock, List[str]] | 9 BMC blocks |
| value_score | float | 0-100 |
| completeness | float | 0.0-1.0 |

## Checklist

### Strategic Planning
- [ ] Objectives have measurable key results
- [ ] Key results have clear target values
- [ ] Owner is assigned to each objective
- [ ] Timeline is realistic and challenging
- [ ] Budget is allocated and tracked
- [ ] Alignment with company strategy verified

### SWOT Analysis
- [ ] At least 3 items per dimension
- [ ] Items are specific and actionable
- [ ] TOWS strategies are generated
- [ ] Analysis is compared to previous
- [ ] External factors validated with data
- [ ] Internal factors honest and realistic

### Competitive Analysis
- [ ] Competitors have position classification
- [ ] Battle cards are generated
- [ ] Recent moves are tracked
- [ ] Threat levels are assessed
- [ ] Win/loss analysis incorporated
- [ ] Sales team feedback included

### Risk Management
- [ ] Probability and impact are estimated
- [ ] Risk scores are calculated
- [ ] Mitigations are documented
- [ ] Top risks are reviewed regularly
- [ ] Risk owners assigned
- [ ] Triggers and early warning signs defined

### Scenario Planning
- [ ] At least 3 scenarios created
- [ ] Probabilities sum to 1.0
- [ ] Impacts are realistic
- [ ] Weighted expected values calculated
- [ ] Strategy recommendations provided
- [ ] Hedging strategies identified

### Market Analysis
- [ ] Segments are clearly defined
- [ ] Size and growth data validated
- [ ] Phase assessment is accurate
- [ ] Barriers and trends documented
- [ ] Opportunity scores calculated

### Business Model Canvas
- [ ] All 9 blocks are filled
- [ ] Value proposition is clear
- [ ] Revenue streams are diversified
- [ ] Cost structure is realistic
- [ ] Model compared to alternatives

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Objective progress stuck | Update key result current values |
| SWOT scores seem wrong | Ensure at least 3 items per dimension |
| Risk score = 0 | Set probability and impact > 0 |
| Scenario evaluation empty | Create at least one scenario first |
| BMC score low | Fill all 9 blocks with content |
| Dashboard shows N/A | Initialize subsystems with data |
| Timeline shows wrong status | Check target_date and current progress |
| Battle card incomplete | Add strengths, weaknesses, and recent moves |
| Opportunity score = 0 | Add size, growth rate, and phase data |
| Competitive landscape empty | Add competitors with market share |

## Security Notes

- Strategic data is sensitive; restrict access
- Competitive intelligence should be ethically gathered
- Risk assessments may inform regulatory filings
- Scenario data should be version-controlled
- Business models may contain trade secrets
- Market data should be sourced and cited
- OKR progress should be auditable
- Battle cards should be reviewed before external use

## Performance Targets

| Operation | Target | Notes |
|-----------|--------|-------|
| SWOT analysis | < 10ms | Pre-built templates |
| Risk register generation | < 50ms | In-memory calculation |
| Scenario evaluation | < 100ms | Lazy evaluation |
| Dashboard generation | < 200ms | Cached aggregations |
| BMC comparison | < 30ms | Index-based lookup |

---

*Strategy Agent v2.0 — Part of the Awesome Grok Skills collection.*

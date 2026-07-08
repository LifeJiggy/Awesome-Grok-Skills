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
---

# Strategy Agent

> Strategic planning, competitive intelligence, OKR management, risk assessment, scenario planning, and business model analysis.

## Identity

The Strategy Agent is a comprehensive business intelligence and strategic planning platform. It manages OKRs with key result tracking, performs SWOT analysis with TOWS strategy generation, tracks competitive landscape with battle cards, assesses strategic risks with mitigation tracking, builds and evaluates scenarios, analyzes market segments, and designs business model canvases.

**Core principle:** Strategy without measurement is just philosophy. Every objective has a key result. Every risk has a score. Every scenario has a probability.

## Principles

1. **Measure What Matters** - OKRs with quantifiable key results
2. **Know Your Competition** - Battle cards, not assumptions
3. **Assess Risk Honestly** - Probability × Impact, not optimism
4. **Plan for Multiple Futures** - Best, base, and worst case scenarios
5. **Market-Driven Decisions** - Segment data guides resource allocation
6. **Business Model Clarity** - 9-block canvas forces completeness

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
        {"description": "Reach 10K MAU", "metric": "mau", "target_value": 10000, "current_value": 3500, "unit": "users"},
        {"description": "NPS > 50", "metric": "nps", "target_value": 50, "current_value": 32, "unit": "score"},
        {"description": "Retention > 40%", "metric": "retention", "target_value": 0.40, "current_value": 0.28, "unit": "rate"},
    ],
    target_date=datetime(2025, 6, 30),
    owner="product-team",
    budget=150000.0,
)

# Update key result
planner.update_key_result(obj.id, obj.key_results[0].id, current_value=5200)

# Get timeline status
timeline = planner.get_timeline_status(obj.id)
# {"expected_progress": 45.0, "actual_progress": 35.0, "status": "behind"}
```

### 2. SWOT Analysis

```python
from agents.strategy.agent import SWOTAnalyzer

swot = SWOTAnalyzer()
analysis = swot.analyze(
    strengths=["Strong team", "Patent portfolio", "Brand recognition"],
    weaknesses=["Limited budget", "Small team"],
    opportunities=["Growing market", "AI adoption"],
    threats=["New competitors", "Regulatory changes"],
)
# analysis.scores = {"strengths_score": 30, "weaknesses_score": 30, ...}
# analysis.strategies = {"so_strategies": [...], "wo_strategies": [...]}
```

### 3. Competitive Intelligence

```python
from agents.strategy.agent import CompetitiveAnalyzer, CompetitivePosition

comp = CompetitiveAnalyzer()
competitor = comp.add_competitor(
    name="RivalCorp",
    position=CompetitivePosition.LEADER,
    market_share=35.0,
    strengths=["Brand", "Distribution"],
    weaknesses=["High pricing", "Slow innovation"],
    pricing="Premium",
)

# Generate battle card
card = comp.generate_battle_card(competitor.id)
# {"talk_track": ["We differentiate from RivalCorp through:..."]}

# Landscape summary
landscape = comp.get_competitive_landscape()
```

### 4. Risk Management

```python
from agents.strategy.agent import RiskManager

rm = RiskManager()
risk = rm.add_risk(
    name="Market disruption",
    category="market",
    probability=0.3,
    impact=0.8,
    description="New technology could displace current offering",
    owner="strategy-team",
)
# risk.risk_score = 2.4, risk.level = RiskLevel.MEDIUM

rm.add_mitigation(risk.id, "Invest in R&D for next-gen technology")
register = rm.get_risk_register()
top_risks = rm.get_top_risks(limit=5)
```

### 5. Scenario Planning

```python
from agents.strategy.agent import ScenarioPlanner, ScenarioType

sp = ScenarioPlanner()
sp.create_scenario(
    name="Aggressive Growth",
    scenario_type=ScenarioType.BEST_CASE,
    assumptions=["Market grows 25%", "No new competitors"],
    impacts={"revenue": 2.5, "market_share": 15.0},
    probability=0.2,
    triggers=["Market expansion report"],
)

sp.create_scenario(
    name="Market Contraction",
    scenario_type=ScenarioType.WORST_CASE,
    assumptions=["Recession", "Price pressure"],
    impacts={"revenue": -0.5, "market_share": -5.0},
    probability=0.3,
    mitigation=["Cost reduction plan", "Diversify revenue"],
)

evaluation = sp.evaluate_scenarios()
recommendation = sp.recommend_strategy()
```

### 6. Market Analysis

```python
from agents.strategy.agent import MarketAnalyzer, MarketPhase

market = MarketAnalyzer()
market.add_segment(
    name="Enterprise Security",
    size=50_000_000_000,
    growth_rate=0.12,
    phase=MarketPhase.GROWTH,
    trends=["Zero trust adoption", "Cloud migration"],
    barriers=["High compliance requirements", "Long sales cycles"],
)

top = market.get_top_opportunities(limit=3)
summary = market.get_market_summary()
```

### 7. Business Model Canvas

```python
from agents.strategy.agent import BusinessModelCanvas, BusinessModelBlock

bmc = BusinessModelCanvas()
model = bmc.create_model(
    name="SaaS Platform",
    blocks={
        BusinessModelBlock.CUSTOMER_SEGMENTS: ["Enterprise", "SMB"],
        BusinessModelBlock.VALUE_PROPOSITIONS: ["AI-powered security", "Real-time monitoring"],
        BusinessModelBlock.CHANNELS: ["Direct sales", "Partner network"],
        BusinessModelBlock.CUSTOMER_RELATIONSHIPS: ["Self-service", "Dedicated support"],
        BusinessModelBlock.REVENUE_STREAMS: ["Subscription", "Professional services"],
        BusinessModelBlock.KEY_RESOURCES: ["AI platform", "Security team"],
        BusinessModelBlock.KEY_ACTIVITIES: ["Product development", "Threat research"],
        BusinessModelBlock.KEY_PARTNERSHIPS: ["Cloud providers", "Resellers"],
        BusinessModelBlock.COST_STRUCTURE: ["R&D", "Sales", "Infrastructure"],
    },
)
# model.value_score = 78.5
```

### 8. Unified Dashboard

```python
agent = StrategyAgent()
dashboard = agent.get_strategy_dashboard()
# {
#   "health_score": 72.5,
#   "metrics": {"objective_completion": "45%", "risk_exposure": "35%"},
#   "objectives": {"total": 5, "by_health": {...}},
#   "risks": {...},
#   "market": {...},
#   "scenarios": {...},
#   "competitive": {...},
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
    def create_objective(self, title, description, priority, key_results, target_date, owner, budget?) -> StrategicObjective
    def update_key_result(self, objective_id, kr_id, current_value) -> Optional[KeyResult]
    def add_initiative(self, objective_id, name, ...) -> Initiative
    def get_timeline_status(self, objective_id) -> Dict
    def get_objectives_by_priority(self, priority) -> List[StrategicObjective]

class SWOTAnalyzer:
    def analyze(self, strengths, weaknesses, opportunities, threats, context?) -> SWOTAnalysis
    def get_comparative_analysis(self) -> Optional[Dict]

class CompetitiveAnalyzer:
    def add_competitor(self, name, position, market_share, strengths, weaknesses, pricing?) -> Competitor
    def add_competitor_move(self, competitor_id, move) -> Dict
    def generate_battle_card(self, competitor_id) -> Dict
    def get_competitive_landscape(self) -> Dict

class RiskManager:
    def add_risk(self, name, category, probability, impact, description, owner?) -> StrategicRisk
    def add_mitigation(self, risk_id, mitigation) -> Dict
    def update_risk(self, risk_id, probability?, impact?) -> Optional[StrategicRisk]
    def get_risk_register(self) -> Dict
    def get_top_risks(self, limit?) -> List[StrategicRisk]
```

## Data Models

### StrategicObjective
| Field | Type | Description |
|-------|------|-------------|
| id | str | Unique identifier |
| title | str | Objective name |
| priority | StrategicPriority | GROWTH, EFFICIENCY, INNOVATION, etc. |
| status | ObjectiveStatus | NOT_STARTED → COMPLETED lifecycle |
| key_results | List[KeyResult] | Measurable outcomes |
| progress | float | 0.0 - 1.0 overall progress |

### StrategicRisk
| Field | Type | Description |
|-------|------|-------------|
| id | str | Risk identifier |
| probability | float | 0.0 - 1.0 |
| impact | float | 0.0 - 1.0 |
| risk_score | float | probability × impact |
| level | RiskLevel | CRITICAL, HIGH, MEDIUM, LOW |

### Scenario
| Field | Type | Description |
|-------|------|-------------|
| id | str | Scenario identifier |
| scenario_type | ScenarioType | BEST_CASE, BASE_CASE, WORST_CASE |
| probability | float | Likelihood of scenario |
| impacts | Dict[str, float] | Impact per metric |

## Checklist

### Strategic Planning
- [ ] Objectives have measurable key results
- [ ] Key results have clear target values
- [ ] Owner is assigned to each objective
- [ ] Timeline is realistic

### SWOT Analysis
- [ ] At least 3 items per dimension
- [ ] Items are specific and actionable
- [ ] TOWS strategies are generated
- [ ] Analysis is compared to previous

### Competitive Analysis
- [ ] Competitors have position classification
- [ ] Battle cards are generated
- [ ] Recent moves are tracked
- [ ] Threat levels are assessed

### Risk Management
- [ ] Probability and impact are estimated
- [ ] Risk scores are calculated
- [ ] Mitigations are documented
- [ ] Top risks are reviewed regularly

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Objective progress stuck | Update key result current values |
| SWOT scores seem wrong | Ensure at least 3 items per dimension |
| Risk score = 0 | Set probability and impact > 0 |
| Scenario evaluation empty | Create at least one scenario first |
| BMC score low | Fill all 9 blocks with content |
| Dashboard shows N/A | Initialize subsystems with data |

## Security Notes

- Strategic data is sensitive; restrict access
- Competitive intelligence should be ethically gathered
- Risk assessments may inform regulatory filings
- Scenario data should be version-controlled
- Business models may contain trade secrets

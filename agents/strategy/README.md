# Strategy Agent

Strategic planning, competitive intelligence, OKR management, risk assessment, scenario planning, market analysis, and business model canvas.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [OKR Management](#okr-management)
  - [SWOT Analysis](#swot-analysis)
  - [Competitive Intelligence](#competitive-intelligence)
  - [Risk Management](#risk-management)
  - [Scenario Planning](#scenario-planning)
  - [Market Analysis](#market-analysis)
  - [Business Model Canvas](#business-model-canvas)
  - [Dashboard](#dashboard)
- [API Reference](#api-reference)
- [Data Models](#data-models)
- [Design Patterns](#design-patterns)
- [Security](#security)
- [Scalability](#scalability)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Checklists](#checklists)
- [Troubleshooting](#troubleshooting)
- [Files](#files)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Strategy Agent provides a comprehensive strategic planning and business intelligence platform. It manages the full strategy lifecycle from market analysis and competitive intelligence through OKR tracking, risk management, and scenario planning.

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                         StrategyAgent (Facade)                                    │
├──────────────┬──────────────┬──────────────┬──────────────┬───────────────────────┤
│  Strategic   │    SWOT      │ Competitive  │    Risk      │    Scenario           │
│  Planner     │   Analyzer   │  Analyzer    │   Manager    │    Planner            │
├──────────────┼──────────────┼──────────────┼──────────────┼───────────────────────┤
│ Objectives   │ TOWS Matrix  │ Battle Cards │ Risk Matrix  │ Best/Base/Worst Case  │
│ Key Results  │ Scores       │ Market Share │ Mitigations  │ Weighted Impact       │
│ Initiatives  │ Strategies   │ Talk Tracks  │ Risk Scores  │ Recommendations       │
├──────────────┴──────────────┴──────────────┴──────────────┴───────────────────────┤
│                          Market Analyzer | Business Model Canvas                  │
└───────────────────────────────────────────────────────────────────────────────────┘
```

**Key Benefits:**
- Unified strategic planning across multiple domains
- Data-driven decision making with quantified metrics
- Automated competitive intelligence and battle cards
- Risk-adjusted scenario planning
- Business model evaluation and comparison

**Use Cases:**
- Quarterly strategic planning sessions
- OKR setting and tracking
- Competitive analysis and sales enablement
- Risk assessment and mitigation planning
- Market opportunity evaluation
- Business model design and iteration

## Features

| Feature | Description | Status |
|---------|-------------|--------|
| **OKR Management** | Objectives with key results, progress tracking, timeline analysis | Stable |
| **SWOT Analysis** | TOWS matrix strategy generation, comparative analysis | Stable |
| **Competitive Intelligence** | Battle cards, market share tracking, talk tracks | Stable |
| **Risk Management** | Probability x impact scoring, mitigation tracking, risk register | Stable |
| **Scenario Planning** | Best/base/worst case evaluation, weighted impact analysis | Stable |
| **Market Analysis** | Segment sizing, opportunity scoring, phase analysis | Stable |
| **Business Model Canvas** | 9-block BMC, value scoring, model comparison | Stable |
| **Unified Dashboard** | Aggregated strategic metrics and health scores | Stable |

## Architecture

### Component Interaction

```
                    ┌─────────────────┐
                    │  StrategyAgent  │
                    │    (Facade)     │
                    └────────┬────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
    ┌───────▼──────┐ ┌──────▼──────┐ ┌───────▼──────┐
    │  Strategic   │ │    SWOT     │ │ Competitive  │
    │  Planner     │ │  Analyzer   │ │  Analyzer    │
    └───────┬──────┘ └──────┬──────┘ └───────┬──────┘
            │                │                │
            └────────────────┼────────────────┘
                             │
            ┌────────────────┼────────────────┐
            │                │                │
    ┌───────▼──────┐ ┌──────▼──────┐ ┌───────▼──────┐
    │    Risk      │ │  Scenario   │ │   Market     │
    │   Manager    │ │   Planner   │ │  Analyzer    │
    └──────────────┘ └─────────────┘ └──────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for full technical details including data flow diagrams, design patterns, and scalability considerations.

## Quick Start

```python
from agents.strategy.agent import StrategyAgent

agent = StrategyAgent()

# SWOT Analysis
swot = agent.perform_swot({
    "strengths": ["Strong team", "Patent portfolio"],
    "weaknesses": ["Limited budget", "Small team"],
    "opportunities": ["Growing market", "AI adoption"],
    "threats": ["New competitors", "Regulatory changes"]
})

# Dashboard
dashboard = agent.get_strategy_dashboard()
print(f"Health: {dashboard['health_score']}/100")
print(f"Objectives: {dashboard['objectives']['total']}")
print(f"Risks: {dashboard['risks']['total']}")
```

Run the demo:

```bash
python agents/strategy/agent.py
```

## Installation

### Requirements

- Python 3.10+
- No external dependencies (standard library only)

### Setup

```bash
# Clone the repository
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills

# Install in development mode
pip install -e .
```

## Usage

### OKR Management

```python
from agents.strategy.agent import StrategicPlanner, StrategicPriority

planner = StrategicPlanner()

# Create objective with key results
obj = planner.create_objective(
    title="Achieve Product-Market Fit",
    description="Validate PMF in target segment",
    priority=StrategicPriority.GROWTH,
    key_results=[
        {"description": "Reach 10K MAU", "metric": "mau", "target_value": 10000, "current_value": 3500},
        {"description": "NPS > 50", "metric": "nps", "target_value": 50, "current_value": 32},
        {"description": "Retention > 40%", "metric": "retention", "target_value": 0.40, "current_value": 0.28},
    ],
    target_date=datetime(2025, 6, 30),
    owner="product-team",
    budget=150000.0,
)

# Update progress
planner.update_key_result(obj.id, obj.key_results[0].id, current_value=5200)

# Timeline analysis
timeline = planner.get_timeline_status(obj.id)
# {"expected_progress": 0.25, "actual_progress": 0.35, "status": "ahead"}

# Get OKR summary
summary = planner.get_okr_summary()
# {"total_objectives": 8, "avg_progress": 0.62, ...}
```

**OKR Best Practices:**
- Write measurable key results (numbers, not adjectives)
- Review OKRs weekly and update progress
- Target 70% completion for stretch goals
- Align OKRs across teams

### SWOT Analysis

```python
from agents.strategy.agent import SWOTAnalyzer

swot = SWOTAnalyzer()
analysis = swot.analyze(
    strengths=["Strong team", "Patents", "Brand"],
    weaknesses=["Limited budget", "Small team"],
    opportunities=["Growing market", "AI adoption"],
    threats=["Competition", "Regulation"],
)

print(f"SO Strategies: {analysis.strategies['so_strategies']}")
print(f"WT Strategies: {analysis.strategies['wt_strategies']}")
```

**TOWS Matrix:**
| | Opportunities | Threats |
|---|---|---|
| **Strengths** | SO: Leverage strengths | ST: Counter threats |
| **Weaknesses** | WO: Address weaknesses | WT: Minimize exposure |

### Competitive Intelligence

```python
from agents.strategy.agent import CompetitiveAnalyzer, CompetitivePosition

comp = CompetitiveAnalyzer()
competitor = comp.add_competitor(
    name="RivalCorp",
    position=CompetitivePosition.LEADER,
    market_share=35.0,
    strengths=["Brand", "Distribution"],
    weaknesses=["High pricing", "Slow innovation"],
)

# Battle card
card = comp.generate_battle_card(competitor.id)
print(f"Talk Track: {card['talk_track']}")

# Landscape
landscape = comp.get_competitive_landscape()
print(f"Competitors: {landscape['total_competitors']}")
```

### Risk Management

```python
from agents.strategy.agent import RiskManager

rm = RiskManager()
risk = rm.add_risk(
    name="Market disruption",
    category="market",
    probability=0.3,
    impact=0.8,
    description="New tech could displace offering",
)
rm.add_mitigation(risk.id, "Invest in R&D")

register = rm.get_risk_register()
top = rm.get_top_risks(5)
```

**Risk Scoring:**
| Score | Level | Response |
|-------|-------|----------|
| >= 12 | CRITICAL | 24 hours |
| >= 8 | HIGH | 1 week |
| >= 4 | MEDIUM | 1 month |
| < 4 | LOW | Quarterly |

### Scenario Planning

```python
from agents.strategy.agent import ScenarioPlanner, ScenarioType

sp = ScenarioPlanner()
sp.create_scenario("Growth", ScenarioType.BEST_CASE, ["Market +25%"], {"revenue": 2.5}, 0.2)
sp.create_scenario("Recession", ScenarioType.WORST_CASE, ["Downturn"], {"revenue": -0.5}, 0.3)

evaluation = sp.evaluate_scenarios()
recommendation = sp.recommend_strategy()
```

### Market Analysis

```python
from agents.strategy.agent import MarketAnalyzer, MarketPhase

market = MarketAnalyzer()
market.add_segment(
    name="Enterprise Security",
    size=50_000_000_000,
    growth_rate=0.12,
    phase=MarketPhase.GROWTH,
    trends=["Zero trust", "Cloud migration"],
    barriers=["Compliance", "Long sales cycles"],
)

top = market.get_top_opportunities(3)
summary = market.get_market_summary()
```

### Business Model Canvas

```python
from agents.strategy.agent import BusinessModelCanvas, BusinessModelBlock

bmc = BusinessModelCanvas()
model = bmc.create_model("SaaS Platform", {
    BusinessModelBlock.CUSTOMER_SEGMENTS: ["Enterprise", "SMB"],
    BusinessModelBlock.VALUE_PROPOSITIONS: ["AI security", "Real-time monitoring"],
    BusinessModelBlock.REVENUE_STREAMS: ["Subscription", "Services"],
    # ... all 9 blocks
})
print(f"Value Score: {model.value_score}")
```

### Dashboard

```python
dashboard = agent.get_strategy_dashboard()
# {
#   "health_score": 72.5,
#   "metrics": {...},
#   "objectives": {...},
#   "risks": {...},
#   "market": {...},
#   "scenarios": {...},
#   "competitive": {...},
# }
```

## API Reference

### StrategyAgent

| Method | Returns | Description |
|--------|---------|-------------|
| `define_strategy(name, objectives)` | Dict | Create strategy with objectives |
| `perform_swot(data)` | SWOTAnalysis | Run SWOT analysis |
| `assess_risks(risks)` | Dict | Create risk register |
| `analyze_competitors()` | Dict | Competitive landscape |
| `get_strategy_dashboard()` | Dict | Full dashboard |

### StrategicPlanner

| Method | Returns | Description |
|--------|---------|-------------|
| `create_objective(title, desc, priority, krs, date, owner, budget?)` | StrategicObjective | Create OKR |
| `update_key_result(obj_id, kr_id, value)` | Optional[KeyResult] | Update KR progress |
| `add_initiative(obj_id, name, ...)` | Initiative | Add supporting initiative |
| `get_timeline_status(obj_id)` | Dict | Timeline analysis |
| `get_objectives_by_priority(priority)` | List[StrategicObjective] | Filter by priority |
| `get_okr_summary()` | Dict | Overall OKR metrics |

### SWOTAnalyzer

| Method | Returns | Description |
|--------|---------|-------------|
| `analyze(s, w, o, t, context?)` | SWOTAnalysis | Run analysis |
| `get_comparative_analysis()` | Optional[Dict] | Compare to previous |

### CompetitiveAnalyzer

| Method | Returns | Description |
|--------|---------|-------------|
| `add_competitor(name, position, share, s, w, pricing?)` | Competitor | Add competitor |
| `add_competitor_move(id, move)` | Dict | Track competitor action |
| `generate_battle_card(id)` | Dict | Create battle card |
| `get_competitive_landscape()` | Dict | Market overview |

### RiskManager

| Method | Returns | Description |
|--------|---------|-------------|
| `add_risk(name, cat, prob, impact, desc, owner?)` | StrategicRisk | Add risk |
| `add_mitigation(risk_id, mitigation)` | Dict | Add mitigation |
| `update_risk(risk_id, prob?, impact?)` | Optional[StrategicRisk] | Update risk |
| `get_risk_register()` | Dict | Risk summary |
| `get_top_risks(limit?)` | List[StrategicRisk] | Top risks |

### ScenarioPlanner

| Method | Returns | Description |
|--------|---------|-------------|
| `create_scenario(name, type, assumptions, impacts, prob, ...)` | Scenario | Create scenario |
| `evaluate_scenarios()` | Dict | Weighted evaluation |
| `recommend_strategy()` | Dict | Strategy recommendation |

### MarketAnalyzer

| Method | Returns | Description |
|--------|---------|-------------|
| `add_segment(name, size, growth, phase, trends, barriers?)` | MarketSegment | Add segment |
| `get_top_opportunities(limit?)` | List[MarketSegment] | Top opportunities |
| `get_market_summary()` | Dict | Market overview |

### BusinessModelCanvas

| Method | Returns | Description |
|--------|---------|-------------|
| `create_model(name, blocks)` | BusinessModel | Create BMC |
| `compare_models(id1, id2)` | Dict | Compare models |

## Data Models

### StrategicObjective
OKR with title, key results, progress, owner, and timeline.

### SWOTAnalysis
Strengths, weaknesses, opportunities, threats with TOWS strategies.

### Competitor
Competitor record with market share, strengths, weaknesses, and moves.

### StrategicRisk
Risk with probability, impact, mitigations, and level classification.

### Scenario
Scenario with assumptions, impacts, probability, and weighted evaluation.

### MarketSegment
Market segment with size, growth rate, phase, and trends.

### BusinessModel
BMC with 9 blocks and calculated value score.

## Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **Facade** | Unified strategy interface | StrategyAgent |
| **Strategy** | Multiple OKR scoring methods | StrategicPlanner |
| **Observer** | Risk threshold alerts | RiskManager |
| **Builder** | Construct BMC models | BusinessModelCanvas |
| **Template Method** | SWOT analysis flow | SWOTAnalyzer |

## Security

- Strategic data access controls
- Audit trail for all strategic decisions
- Sensitive competitive intel protection
- Role-based access for different operations

## Scalability

| Dimension | Strategy | Notes |
|-----------|----------|-------|
| Objectives | Indexed by priority + status | Fast filtered queries |
| Risks | Indexed by level + category | Efficient triage |
| Competitors | Indexed by market share | Landscape view |
| Scenarios | Cached evaluation | Recompute on change |

## Configuration

```python
import logging
logging.basicConfig(level=logging.INFO)

# Custom risk scoring weights
# Override StrategicRisk.calculate_risk_score() for custom logic

# Custom opportunity scoring
# Override MarketAnalyzer._calc_opportunity() for custom weights

# Custom BMC scoring
# Override BusinessModelCanvas._calculate_value_score() for domain-specific scoring
```

## Examples

### Quarterly Strategic Review

```python
from agents.strategy.agent import StrategyAgent

agent = StrategyAgent()

# 1. Update OKRs
planner = agent.strategic_planner
for obj in planner.get_objectives_by_priority(StrategicPriority.GROWTH):
    print(f"{obj.title}: {obj.progress*100:.0f}%")

# 2. Review risks
rm = agent.risk_manager
top_risks = rm.get_top_risks(5)
for risk in top_risks:
    print(f"{risk.name}: {risk.level.value}")

# 3. Check competitive landscape
comp = agent.competitive_analyzer
landscape = comp.get_competitive_landscape()
print(f"Market position: {landscape['our_position']}")

# 4. Dashboard
dashboard = agent.get_strategy_dashboard()
print(f"Health Score: {dashboard['health_score']}")
```

### Battle Card Generation

```python
# Generate battle card for sales team
card = comp.generate_battle_card("comp_rivalcorp")

print("=== Battle Card: RivalCorp ===")
print(f"\nTalk Track:")
for point in card['talk_track']:
    print(f"  - {point}")

print(f"\nOur Differentiators:")
for diff in card['differentiators']:
    print(f"  - {diff}")

print(f"\nObjection Handling:")
for objection, response in card['objection_handling'].items():
    print(f"  Objection: {objection}")
    print(f"  Response: {response}")
```

## Best Practices

1. **Write measurable key results** - Numbers, not adjectives
2. **Review OKRs weekly** - Keep progress current
3. **Update competitive intel monthly** - Markets change fast
4. **Score risks honestly** - Optimism is not a strategy
5. **Plan multiple scenarios** - Never bet on one future
6. **Fill all BMC blocks** - Gaps reveal blind spots
7. **Use opportunity scores** - Data beats intuition
8. **Align OKRs across teams** - Strategy cascades top-down
9. **Document assumptions** - Especially for scenarios
10. **Review and adjust quarterly** - Strategy is iterative

## Checklists

### OKR Setting
- [ ] Objectives aligned with strategy
- [ ] Key results measurable (numbers)
- [ ] Owners assigned
- [ ] Timeline realistic
- [ ] Budget allocated (if needed)

### SWOT Analysis
- [ ] 3+ items per dimension
- [ ] TOWS strategies generated
- [ ] Action items created
- [ ] Review schedule set

### Risk Assessment
- [ ] All categories covered
- [ ] Probabilities realistic
- [ ] Impacts quantified
- [ ] Mitigations assigned
- [ ] Review cadence established

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Objective progress stuck | Update key result current values |
| SWOT scores seem off | Ensure 3+ items per dimension |
| Risk score = 0 | Set probability and impact > 0 |
| Scenario evaluation empty | Create scenarios first |
| BMC score low | Fill all 9 blocks with content |
| Dashboard shows N/A | Initialize subsystems with data |
| Timeline shows wrong status | Check target_date and progress |
| Battle card incomplete | Add strengths, weaknesses, recent moves |
| Opportunity score = 0 | Add size, growth, and phase data |
| Competitive landscape empty | Add competitors with market share |

## Files

| File | Description | Lines |
|------|-------------|-------|
| `agent.py` | Full implementation with all subsystems | ~2000+ |
| `ARCHITECTURE.md` | System architecture and design patterns | ~900 |
| `GROK.md` | Agent identity, capabilities, and API docs | ~900 |
| `README.md` | This file | ~900 |

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - See [LICENSE](../../LICENSE) for details.

## Support

- **Documentation**: See [ARCHITECTURE.md](ARCHITECTURE.md) and [GROK.md](GROK.md)
- **Issues**: GitHub Issues for bug reports and feature requests
- **Discussions**: GitHub Discussions for questions and community support

---

*Strategy Agent v2.0 -- Part of the Awesome Grok Skills collection.*

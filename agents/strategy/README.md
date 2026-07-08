# Strategy Agent

Strategic planning, competitive intelligence, OKR management, risk assessment, scenario planning, market analysis, and business model canvas.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
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
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The Strategy Agent provides a comprehensive strategic planning and business intelligence platform. It manages the full strategy lifecycle from market analysis and competitive intelligence through OKR tracking, risk management, and scenario planning.

## Features

| Feature | Description |
|---------|-------------|
| **OKR Management** | Objectives with key results, progress tracking, timeline analysis |
| **SWOT Analysis** | TOWS matrix strategy generation, comparative analysis |
| **Competitive Intelligence** | Battle cards, market share tracking, talk tracks |
| **Risk Management** | Probability × impact scoring, mitigation tracking, risk register |
| **Scenario Planning** | Best/base/worst case evaluation, weighted impact analysis |
| **Market Analysis** | Segment sizing, opportunity scoring, phase analysis |
| **Business Model Canvas** | 9-block BMC, value scoring, model comparison |
| **Unified Dashboard** | Aggregated strategic metrics and health scores |

## Architecture

```
StrategyAgent (Facade)
├── StrategicPlanner (OKRs, Key Results, Initiatives)
├── SWOTAnalyzer (TOWS Matrix, Comparative Analysis)
├── CompetitiveAnalyzer (Battle Cards, Landscape)
├── RiskManager (Scoring, Mitigations, Register)
├── ScenarioPlanner (Weighted Impact, Recommendations)
├── MarketAnalyzer (Segments, Opportunities, Phases)
├── BusinessModelCanvas (BMC Blocks, Value Scoring)
└── StrategyAnalyzer (Metrics Engine)
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for full details.

## Quick Start

```python
from agents.strategy.agent import StrategyAgent

agent = StrategyAgent()

# SWOT Analysis
swot = agent.perform_swot({
    "strengths": ["Strong team"],
    "weaknesses": ["Limited budget"],
    "opportunities": ["Growing market"],
    "threats": ["New competitors"],
})

# Dashboard
dashboard = agent.get_strategy_dashboard()
print(f"Health: {dashboard['health_score']}/100")
```

Run directly:

```bash
python agents/strategy/agent.py
```

## Usage

### OKR Management

```python
from agents.strategy.agent import StrategicPlanner, StrategicPriority

planner = StrategicPlanner()

# Create objective
obj = planner.create_objective(
    title="Achieve Product-Market Fit",
    description="Validate PMF in target segment",
    priority=StrategicPriority.GROWTH,
    key_results=[
        {"description": "Reach 10K MAU", "metric": "mau", "target_value": 10000, "current_value": 3500},
        {"description": "NPS > 50", "metric": "nps", "target_value": 50, "current_value": 32},
    ],
    target_date=datetime(2025, 6, 30),
    owner="product-team",
    budget=150000.0,
)

# Update progress
planner.update_key_result(obj.id, obj.key_results[0].id, current_value=5200)

# Timeline analysis
timeline = planner.get_timeline_status(obj.id)
```

### SWOT Analysis

```python
from agents.strategy.agent import SWOTAnalyzer

swot = SWOTAnalyzer()
analysis = swot.analyze(
    strengths=["Strong team", "Patents", "Brand"],
    weaknesses=["Limited budget"],
    opportunities=["Growing market", "AI adoption"],
    threats=["Competition", "Regulation"],
)
print(f"Strategies: {analysis.strategies}")
```

### Competitive Intelligence

```python
from agents.strategy.agent import CompetitiveAnalyzer, CompetitivePosition

comp = CompetitiveAnalyzer()
competitor = comp.add_competitor(
    name="RivalCorp",
    position=CompetitivePosition.LEADER,
    market_share=35.0,
    strengths=["Brand", "Distribution"],
    weaknesses=["High pricing"],
)

# Battle card
card = comp.generate_battle_card(competitor.id)

# Landscape
landscape = comp.get_competitive_landscape()
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

| Method | Returns |
|--------|---------|
| `define_strategy(name, objectives)` | Dict with created IDs |
| `perform_swot(data)` | SWOT analysis dict |
| `assess_risks(risks)` | Risk register |
| `analyze_competitors()` | Landscape summary |
| `get_strategy_dashboard()` | Full dashboard |

### StrategicPlanner

| Method | Returns |
|--------|---------|
| `create_objective(title, desc, priority, krs, date, owner, budget?)` | StrategicObjective |
| `update_key_result(obj_id, kr_id, value)` | Optional[KeyResult] |
| `add_initiative(obj_id, name, ...)` | Initiative |
| `get_timeline_status(obj_id)` | Dict |
| `get_objectives_by_priority(priority)` | List[StrategicObjective] |

### SWOTAnalyzer

| Method | Returns |
|--------|---------|
| `analyze(s, w, o, t, context?)` | SWOTAnalysis |
| `get_comparative_analysis()` | Optional[Dict] |

### CompetitiveAnalyzer

| Method | Returns |
|--------|---------|
| `add_competitor(name, position, share, s, w, pricing?)` | Competitor |
| `add_competitor_move(id, move)` | Dict |
| `generate_battle_card(id)` | Dict |
| `get_competitive_landscape()` | Dict |

### RiskManager

| Method | Returns |
|--------|---------|
| `add_risk(name, cat, prob, impact, desc, owner?)` | StrategicRisk |
| `add_mitigation(risk_id, mitigation)` | Dict |
| `update_risk(risk_id, prob?, impact?)` | Optional[StrategicRisk] |
| `get_risk_register()` | Dict |
| `get_top_risks(limit?)` | List[StrategicRisk] |

### ScenarioPlanner

| Method | Returns |
|--------|---------|
| `create_scenario(name, type, assumptions, impacts, prob, ...)` | Scenario |
| `evaluate_scenarios()` | Dict |
| `recommend_strategy()` | Dict |

### MarketAnalyzer

| Method | Returns |
|--------|---------|
| `add_segment(name, size, growth, phase, trends, barriers?)` | MarketSegment |
| `get_top_opportunities(limit?)` | List[MarketSegment] |
| `get_market_summary()` | Dict |

### BusinessModelCanvas

| Method | Returns |
|--------|---------|
| `create_model(name, blocks)` | BusinessModel |
| `compare_models(id1, id2)` | Dict |

## Configuration

```python
import logging
logging.basicConfig(level=logging.INFO)

# Custom risk scoring weights
# Override StrategicRisk.calculate_risk_score() for custom logic

# Custom opportunity scoring
# Override MarketAnalyzer._calc_opportunity() for custom weights
```

## Examples

See `main()` in `agent.py` for a complete working example demonstrating:
- SWOT analysis with strategy generation
- Competitive landscape assessment
- Risk evaluation with scoring
- Dashboard generation

## Best Practices

1. **Write measurable key results** - Numbers, not adjectives
2. **Review OKRs weekly** - Keep progress current
3. **Update competitive intel monthly** - Markets change fast
4. **Score risks honestly** - Optimism is not a strategy
5. **Plan multiple scenarios** - Never bet on one future
6. **Fill all BMC blocks** - Gaps reveal blind spots
7. **Use opportunity scores** - Data beats intuition

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Objective progress stuck | Update key result current values |
| SWOT scores seem off | Ensure 3+ items per dimension |
| Risk score = 0 | Set probability and impact > 0 |
| Scenario evaluation empty | Create scenarios first |
| BMC score low | Fill all 9 blocks with content |
| Dashboard shows N/A | Initialize subsystems with data |

## Files

| File | Description |
|------|-------------|
| `agent.py` | Full implementation with all subsystems |
| `ARCHITECTURE.md` | System architecture and design patterns |
| `GROK.md` | Agent identity, capabilities, and API docs |
| `README.md` | This file |

## License

MIT License - See [LICENSE](../../LICENSE) for details.

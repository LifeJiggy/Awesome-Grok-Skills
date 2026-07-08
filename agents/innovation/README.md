# Innovation Agent

> Comprehensive innovation management platform covering idea generation, technology scouting, patent strategy, experiment design, and R&D portfolio optimization.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

The Innovation Agent provides structured pipelines for managing the complete innovation lifecycle — from idea capture and evaluation through technology scouting, patent strategy, experiment design, and portfolio optimization. Built for corporate innovation labs, R&D departments, and intrapreneurship programs.

## Features

### Idea Management
- Multi-dimensional scoring with configurable weights
- Idea lifecycle tracking (SUBMITTED → COMPLETED)
- Category-based organization (PRODUCT, TECHNOLOGY, PROCESS, etc.)
- Composite scoring across impact, feasibility, alignment, market, and risk

### Technology Scouting
- Trend tracking with lifecycle levels (EMERGING → DECLINING)
- Disruption potential assessment
- Competitive landscape analysis
- Scout report generation
- Alert system for trend level changes

### Patent Portfolio Management
- Patent lifecycle tracking (IDEA → GRANTED)
- Prior art search across portfolio
- Jurisdiction and classification tracking
- Renewal scheduling
- Licensing opportunity identification

### Experiment Design
- Hypothesis-driven experiment framework
- Control vs. treatment analysis
- Statistical significance calculation
- Results documentation and recommendations

### R&D Portfolio
- Stage-gate process management
- Budget allocation and tracking
- Risk assessment per project
- Progress monitoring
- Cross-project dependencies

## Quick Start

### Installation

```bash
git clone https://github.com/your-org/awesome-grok-skills.git
cd awesome-grok-skills
pip install -e .
```

### Basic Usage

```python
from agents.innovation.agent import InnovationAgent, IdeaCategory, TechTrendLevel

agent = InnovationAgent()

# Submit an idea
idea = agent.submit_idea(
    title="AI-Powered Code Review",
    description="ML model for automated PR review",
    submitter="alice@corp.com",
    category=IdeaCategory.TECHNOLOGY,
)

# Evaluate it
result = agent.evaluate_idea(idea.idea_id, {
    "impact": {"revenue_potential": 8, "market_disruption": 7, "customer_value": 9, "operational_efficiency": 6},
    "feasibility": {"technical_complexity": 4, "resource_availability": 7, "timeline_realism": 6, "skill_gap": 3},
    "strategic_fit": 8.5, "goals_fit": 7.0,
    "market_size": 5_000_000, "growth_rate": 15.0, "competition_intensity": 6.0,
    "risk": {"technical": 3, "market": 2, "financial": 2},
})

print(f"Score: {result['composite_score']} -> {result['verdict']}")
```

### Run the Demo

```bash
python agents/innovation/agent.py
```

## Usage

### Technology Scouting

```python
trend = agent.scouting_engine.register_trend(
    name="LLM-Powered Dev Tools",
    description="Large language models in developer workflows",
    domain="software",
    level=TechTrendLevel.GROWING,
    disruption=8.5,
)

# Find opportunities
opps = agent.scouting_engine.identify_opportunities(domain="software", min_disruption=7.0)
```

### Patent Management

```python
patent = agent.patent_manager.create_patent(
    title="Adaptive Code Review Using Neural Networks",
    description="System for automated code review",
    inventors=["Alice Chen", "Bob Park"],
    jurisdictions=["US", "EU"],
    estimated_value=250000,
)

portfolio = agent.patent_manager.calculate_portfolio_value()
```

### Experiments

```python
exp = agent.experiment_manager.create_experiment(
    name="Code Review Accuracy Test",
    hypothesis="AI reviews catch 30% more bugs",
    idea_id=idea.idea_id,
    sample_size=200,
    metrics=["bug_detection_rate", "review_time"],
)

agent.experiment_manager.start_experiment(exp.experiment_id)
agent.experiment_manager.record_result(exp.experiment_id, "bug_detection_rate", 72.0, "treatment")
agent.experiment_manager.record_result(exp.experiment_id, "bug_detection_rate", 55.0, "control")

analysis = agent.experiment_manager.analyze_results(exp.experiment_id)
```

### Portfolio Management

```python
project = agent.portfolio_manager.add_project(
    name="AI Code Review MVP",
    idea_id=idea.idea_id,
    priority=PortfolioPriority.EXPLOIT,
    budget=200000,
)

summary = agent.portfolio_manager.portfolio_summary()
```

## API Reference

### InnovationAgent

| Method | Description |
|--------|-------------|
| `submit_idea(title, description, submitter, category, **kwargs)` | Submit a new idea |
| `evaluate_idea(idea_id, scoring_data)` | Score and evaluate an idea |
| `advance_idea(idea_id)` | Move idea to next stage |
| `get_dashboard()` | Get system-wide dashboard |
| `full_report()` | Get comprehensive report |

### IdeaScoringEngine

| Method | Description |
|--------|-------------|
| `set_weights(weights)` | Update scoring weights |
| `score_impact(factors)` | Score impact dimension |
| `score_feasibility(factors)` | Score feasibility dimension |
| `calculate_composite(idea, data)` | Calculate composite score |
| `rank_ideas(ideas)` | Rank ideas by score |

### TechnologyScoutingEngine

| Method | Description |
|--------|-------------|
| `register_trend(name, desc, domain, level, **kw)` | Register a new trend |
| `assess_trend(trend_id, new_level, maturity)` | Update trend assessment |
| `identify_opportunities(domain, min_disruption)` | Find opportunities |
| `generate_scout_report(title, scout, domain, summary)` | Create report |

### PatentPortfolioManager

| Method | Description |
|--------|-------------|
| `create_patent(title, desc, inventors, **kw)` | Create patent record |
| `update_status(patent_id, new_status)` | Update patent status |
| `search_prior_art(keywords, classification)` | Search for prior art |
| `calculate_portfolio_value()` | Get portfolio metrics |
| `renewal_schedule(within_months)` | Check upcoming renewals |

## Examples

See the full demo in `agent.py` or the [examples/](../examples/) directory.

## Configuration

```python
# Custom scoring weights
agent.scoring_engine.set_weights({
    "impact": 0.40,
    "feasibility": 0.20,
    "strategic_alignment": 0.25,
    "market_opportunity": 0.10,
    "risk": 0.05,
})

# Custom TM fuzzy threshold
agent = InnovationAgent(config={"fuzzy_threshold": 0.80})
```

## Best Practices

1. **Submit early, evaluate often** — capture ideas before they're forgotten
2. **Use consistent scoring criteria** — keep weights stable for comparability
3. **Track technology trends continuously** — don't wait for disruptions
4. **File patents early** — before public disclosure
5. **Design experiments with clear hypotheses** — avoid fishing expeditions
6. **Balance portfolio** — maintain explore/exploit mix

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Ideas score too low | Review scoring weights and criteria |
| Trend alerts not firing | Check trend registration and assessment interval |
| Experiment results inconclusive | Increase sample size or extend duration |
| Patent search returns nothing | Verify keywords and classification codes |

## License

MIT License - see LICENSE file for details.

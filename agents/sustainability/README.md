# Sustainability Agent

> Comprehensive sustainability management platform for measuring, managing, and improving environmental and social impact.

---

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

---

## Overview

The Sustainability Agent provides a complete toolkit for organizational sustainability management, covering:

- **Carbon Tracking**: Scope 1, 2, and 3 emissions calculation and monitoring
- **ESG Reporting**: Environmental, Social, and Governance scoring and reporting
- **Goal Management**: Science-based target setting and progress tracking
- **Green Initiatives**: Project planning, ROI calculation, and portfolio management
- **Supply Chain**: Supplier sustainability assessment and compliance tracking
- **Circular Economy**: Product lifecycle and recyclability tracking
- **Resource Usage**: Water, waste, and energy monitoring
- **Compliance**: Regulatory framework tracking (GRI, SASB, CDP, TCFD, EU CSRD)

---

## Features

### Carbon Management
- Activity-based emission calculations
- Regional grid emission factors for 10+ countries
- Scope 1, 2, and 3 categorization
- Emission verification tracking
- Carbon offset management

### ESG Analytics
- Automated ESG scoring (AAA to CCC rating)
- Stakeholder-specific reports
- Benchmark comparisons
- Trend analysis

### Goal Tracking
- Science-based target support
- Progress monitoring with variance analysis
- Milestone tracking
- On-track/at-risk/behind status

### Initiative Management
- ROI calculation
- Payback period analysis
- Portfolio summary
- Carbon reduction tracking

### Supply Chain
- Multi-tier supplier tracking
- Sustainability scoring model
- Audit scheduling
- Compliance monitoring

### Circular Economy
- Product recyclability assessment
- Recycled content tracking
- Circularity scoring
- End-of-life option tracking

---

## Quick Start

### Installation

```python
# No external dependencies required - pure Python implementation
from agents.sustainability.agent import SustainabilityAgent
```

### Basic Usage

```python
from agents.sustainability.agent import (
    SustainabilityAgent, SustainabilityCategory, CarbonScope
)

# Initialize agent
agent = SustainabilityAgent()

# Track an emission
agent.track_emission(
    SustainabilityCategory.ENERGY,
    CarbonScope.SCOPE_2,
    "Electricity",
    100000,
    "kWh",
    location="HQ"
)

# Calculate carbon footprint
footprint = agent.calculate_carbon_footprint([
    {"type": "electricity", "data": {"kwh": 100000}},
    {"type": "transportation", "data": {"distance_km": 5000, "mode": "car"}}
])
print(f"Total emissions: {footprint['total_emission_tonnes']} tonnes")
```

### Run the Demo

```bash
python agents/sustainability/agent.py
```

---

## Usage

### Carbon Tracking

```python
from agents.sustainability.agent import SustainabilityCategory, CarbonScope

# Track Scope 1 (direct) emissions
agent.track_emission(
    SustainabilityCategory.TRANSPORTATION, CarbonScope.SCOPE_1,
    "Company Vehicles", 5000, "L", location="HQ"
)

# Track Scope 3 (value chain) emissions
agent.track_emission(
    SustainabilityCategory.SUPPLY_CHAIN, CarbonScope.SCOPE_3,
    "Purchased Goods", 500000, "USD", location="Supply Chain"
)
```

### Goal Management

```python
from agents.sustainability.agent import GoalPriority

# Create a goal
goal = agent.set_sustainability_goal(
    "Reduce Energy Consumption",
    "Reduce total energy use by 30%",
    SustainabilityCategory.ENERGY,
    baseline=1000000,  # kWh
    target=700000,     # kWh
    target_year=2028,
    priority=GoalPriority.HIGH
)

# Update progress
agent.goals.update_progress(goal["goal_id"], current_value=850000)

# Check status
status = agent.goals.calculate_goal_status(goal["goal_id"])
print(f"Progress: {status['actual_progress']}%")
print(f"On track: {status['on_track']}")
```

### Initiative Management

```python
from agents.sustainability.agent import SustainabilityCategory

# Create initiative
initiative = agent.initiatives.create_initiative(
    "LED Lighting Retrofit",
    "Replace all fluorescent lights with LEDs",
    SustainabilityCategory.ENERGY,
    investment=25000,
    expected_savings={"annual": 8000},
    carbon_reduction=45,
    timeline_months=3
)

# Calculate ROI
roi = agent.initiatives.calculate_roi(initiative.initiative_id)
print(f"Payback: {roi['payback_years']} years")
print(f"ROI: {roi['roi_5_year_pct']}%")
```

### Supply Chain

```python
from agents.sustainability.agent import SupplyChainTier

# Add supplier
supplier = agent.supply_chain.add_supplier(
    "EcoMaterials Inc",
    SupplyChainTier.TIER_1,
    "USA",
    "Raw Materials",
    sustainability_score=82,
    certifications=["ISO 14001", "LEED"],
    carbon_footprint=75
)

# Get summary
summary = agent.supply_chain.get_supply_chain_summary()
print(f"Average score: {summary['average_sustainability_score']}")
```

### Dashboard

```python
# Get comprehensive dashboard
dashboard = agent.get_sustainability_dashboard()
print(f"ESG Score: {dashboard['esg_score']['overall']}")
print(f"Rating: {dashboard['esg_score']['rating']}")
```

---

## API Reference

### Main Classes

| Class | Description |
|-------|-------------|
| `SustainabilityAgent` | Main agent orchestrating all components |
| `CarbonCalculator` | Emission calculation engine |
| `GoalTracker` | Sustainability goal management |
| `InitiativeManager` | Green initiative tracking |
| `SupplyChainManager` | Supplier sustainability management |
| `CircularEconomyManager` | Product circularity tracking |
| `ResourceUsageManager` | Water, waste, and energy tracking |
| `ComplianceManager` | Regulatory compliance tracking |
| `ESGReporter` | ESG scoring and reporting |

### Key Enums

| Enum | Values |
|------|--------|
| `SustainabilityCategory` | ENERGY, WATER, WASTE, TRANSPORTATION, SUPPLY_CHAIN, BUILDING, PRODUCT, BIODIVERSITY, SOCIAL_IMPACT, GOVERNANCE |
| `CarbonScope` | SCOPE_1, SCOPE_2, SCOPE_3 |
| `GoalPriority` | CRITICAL, HIGH, MEDIUM, LOW |
| `ESGRating` | AAA, AA, A, BBB, BB, B, CCC |

### Key Data Classes

| Class | Purpose |
|-------|---------|
| `EmissionRecord` | Carbon emission tracking |
| `SustainabilityGoal` | Target/goal definition |
| `GreenInitiative` | Project/initiative tracking |
| `Supplier` | Supplier record |
| `CircularProduct` | Product circularity |
| `WaterUsage` | Water consumption |
| `WasteRecord` | Waste generation |
| `EnergyRecord` | Energy consumption |
| `ESGScore` | ESG scoring |
| `ComplianceRecord` | Compliance tracking |

---

## Examples

### Complete Workflow

```python
from agents.sustainability.agent import (
    SustainabilityAgent, SustainabilityCategory, CarbonScope,
    GoalPriority, SupplyChainTier, ComplianceFramework
)
from datetime import datetime

# Initialize
agent = SustainabilityAgent()

# 1. Track emissions
agent.track_emission(SustainabilityCategory.ENERGY, CarbonScope.SCOPE_1,
                     "Natural Gas", 3000, "m³", location="Factory")
agent.track_emission(SustainabilityCategory.ENERGY, CarbonScope.SCOPE_2,
                     "Electricity", 50000, "kWh", location="Office")

# 2. Set goal
goal = agent.set_sustainability_goal(
    "Net Zero by 2030", "Achieve net-zero emissions",
    SustainabilityCategory.ENERGY, 500, 0, 2030, GoalPriority.CRITICAL
)

# 3. Create initiative
ini = agent.initiatives.create_initiative(
    "Solar Installation", "Install rooftop solar",
    SustainabilityCategory.ENERGY, 200000,
    {"annual": 30000}, 180, 12
)

# 4. Add supplier
sup = agent.supply_chain.add_supplier(
    "Green Parts Co", SupplyChainTier.TIER_1, "Germany",
    "Components", certifications=["ISO 14001"]
)

# 5. Track resources
agent.resources.add_energy_record("HQ", "solar", 5000, datetime.now(), renewable_pct=100)
agent.resources.add_water_usage("HQ", "municipal", 300, datetime.now())

# 6. Add compliance
agent.compliance.add_requirement(ComplianceFramework.GRI, "Annual Report",
                                  due_date=datetime(2025, 12, 31))

# 7. Generate dashboard
dashboard = agent.get_sustainability_dashboard()
print(dashboard)
```

### Report Generation

```python
# Generate annual report
report = agent.generate_annual_report()
print(f"Total emissions: {report['carbon_footprint']['total_emission_tonnes']} tonnes")
print(f"ESG rating: {report['esg_score']['rating']}")
print(f"SDG alignment: {report['sdg_alignment']}")
```

---

## Configuration

The agent uses sensible defaults but can be configured:

```python
# Customize emission factors
agent.carbon.emission_factors["custom_source"] = {"factor": 1.5, "unit": "kg CO2e/unit"}

# Add regional grid factors
agent.carbon.grid_factors["MyRegion"] = 0.35

# Customize goal tracking
agent.goals.create_goal(
    name="Custom Goal",
    description="...",
    category=SustainabilityCategory.ENERGY,
    baseline_value=1000,
    target_value=500,
    target_year=2027,
    priority=GoalPriority.HIGH,
    owner="Sustainability Team"
)
```

---

## Best Practices

### Data Collection
1. **Consistency**: Use consistent units and time periods
2. **Granularity**: Collect data at the most granular level possible
3. **Verification**: Verify critical data points
4. **Documentation**: Document data sources and methodologies

### Goal Setting
1. **Science-Based**: Align with climate science (1.5°C pathway)
2. **Measurable**: Define clear, quantifiable targets
3. **Time-Bound**: Set realistic but ambitious timelines
4. **Accountable**: Assign ownership and responsibility

### Reporting
1. **Transparency**: Report both successes and challenges
2. **Comparability**: Use standardized frameworks (GRI, SASB)
3. **Materiality**: Focus on material topics
4. **Stakeholder-Specific**: Tailor reports to audience

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Emission calculations seem wrong | Verify emission factors and units |
| Goal progress not updating | Check goal_id and current_value |
| Supplier score is low | Request updated certifications |
| ESG score seems off | Verify all components are calculated |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## License

MIT License - See [LICENSE](../LICENSE) for details.

---

*Drive sustainability with data-driven insights and measurable impact.*

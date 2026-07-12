---
name: "circular-economy"
category: "sustainability"
version: "1.0.0"
tags: ["sustainability", "circular-economy", "material-flow", "recycling", "lifecycle"]
---

# Circular Economy

## Overview

The Circular Economy is an economic model that eliminates waste and promotes the continual use of resources through design, reuse, repair, remanufacturing, and recycling. Unlike the traditional linear economy (take-make-dispose), circularity keeps materials and products at their highest value for as long as possible. This module provides a comprehensive computational framework for Material Flow Analysis (MFA), product lifecycle tracking, waste stream optimization, recycling rate analytics, remanufacturing assessment, circular design scoring, industrial symbiosis matching, and Extended Producer Responsibility (EPR) tracking. It enables organizations to measure, manage, and optimize their transition from linear to circular operations.

Material Flow Analysis is the backbone of circular economy accounting: it tracks every kilogram of material as it enters a system (raw material extraction, imports), transforms through manufacturing and use phases, and exits as waste, emissions, or recycled output. This module implements both economy-wide MFA (Sankey-diagram-level flows across sectors) and product-level MFA (bill-of-materials decomposition for individual products). It includes time-series tracking to measure circularity progress over multi-year periods, hotspot identification to find where the largest material losses occur, and scenario modeling to evaluate the impact of design changes, new recycling technologies, or policy interventions.

The module addresses the practical challenges of circularity: how to score a product's circularity (Cradle-to-Cradle, Ellen MacArthur Foundation frameworks), how to identify industrial symbiosis opportunities (one company's waste stream as another's feedstock), how to manage Extended Producer Responsibility obligations across multiple jurisdictions, and how to optimize reverse logistics for product take-back programs. It provides tools for waste composition analysis, recyclability assessment, and the economic valuation of secondary materials. For manufacturing contexts, it includes remanufacturing feasibility scoring that evaluates whether a product can be economically restored to like-new condition versus being recycled for raw material recovery.

## Core Capabilities

- **Material Flow Analysis (MFA)**: Track material inputs, transformations, stocks, and outputs across product lifecycles or economy-wide systems with Sankey-diagram-ready data structures.
- **Product Lifecycle Tracking**: End-to-end tracking of materials from raw extraction through manufacturing, distribution, use, and end-of-life, with environmental impact scoring at each stage.
- **Waste Stream Optimization**: Analyze waste composition, identify diversion opportunities, optimize sorting efficiency, and model the impact of waste reduction interventions.
- **Recycling Rate Analytics**: Calculate and benchmark recycling rates (collection, sorting, reprocessing, market uptake), identify bottlenecks, and model circularity scenarios.
- **Remanufacturing Assessment**: Evaluate products for remanufacturing feasibility based on design features, material composition, damage assessment, and economic viability.
- **Circular Design Scoring**: Score products against circularity criteria (durability, reparability, recyclability, recycled content, toxic-free) using C2C and EMF frameworks.
- **Industrial Symbiosis Matching**: Identify and match waste streams between organizations as potential resource exchanges, with logistics and economic feasibility analysis.
- **EPR Tracking**: Manage Extended Producer Responsibility obligations across jurisdictions, including fee calculations, reporting, and compliance documentation.

## Architecture

The module is organized into four interconnected subsystems:

1. **Flow Tracking Subsystem**: MaterialFlowAnalyzer and LifecycleTracker capture material movements and environmental impacts. They produce Sankey-ready data structures and circularity metrics (MCI, recycling rate, material efficiency).
2. **Optimization Subsystem**: WasteOptimizer and SymbiosisMatcher identify improvement opportunities. WasteOptimizer maximizes diversion and revenue from waste streams. SymbiosisMatcher finds win-win resource exchanges between organizations.
3. **Assessment Subsystem**: RemanufacturingAssessor and CircularDesignScorer evaluate products and processes against circularity criteria. They produce scores, grades, and actionable recommendations.
4. **Compliance Subsystem**: EPRTracker manages regulatory obligations across jurisdictions. It calculates fees, tracks reporting deadlines, and maintains compliance documentation.

## Usage Examples

```python
from circular_economy import MaterialFlowAnalyzer, WasteOptimizer, CircularDesignScorer

# Material Flow Analysis for a manufacturing system
mfa = MaterialFlowAnalyzer(system="Widget Manufacturing")
mfa.add_input("steel", tonnes=500, source="primary_extraction", cost_per_tonne=800)
mfa.add_input("aluminum", tonnes=120, source="primary_extraction", cost_per_tonne=2200)
mfa.add_input("plastic", tonnes=80, source="recycled", cost_per_tonne=600)
mfa.add_process("stamping", input_materials=["steel"], output_materials=["steel_parts", "steel_scrap"])
mfa.add_process("assembly", input_materials=["steel_parts", "aluminum", "plastic"], output_materials=["widget"])
mfa.add_output("widget", tonnes=400, destination="market")
mfa.add_output("steel_scrap", tonnes=95, destination="recycler")
mfa.add_output("aluminum_scrap", tonnes=18, destination="recycler")

flow_report = mfa.analyze()
print(f"Input materials: {flow_report.total_input_tonnes:.0f} tonnes")
print(f"Product output: {flow_report.product_output_tonnes:.0f} tonnes")
print(f"Recycled material: {flow_report.recycled_output_tonnes:.0f} tonnes")
print(f"Circularity rate: {flow_report.circularity_rate:.1%}")

# Waste composition analysis
optimizer = WasteOptimizer(facility="Assembly Plant")
optimizer.add_waste_stream("steel_scrap", tonnes=95, recyclable=True, value_per_tonne=150)
optimizer.add_waste_stream("plastic_waste", tonnes=25, recyclable=True, value_per_tonne=80)
optimizer.add_waste_stream("mixed_metal", tonnes=12, recyclable=True, value_per_tonne=200)
optimizer.add_waste_stream("packaging", tonnes=15, recyclable=True, value_per_tonne=20)
optimizer.add_waste_stream("hazardous", tonnes=3, recyclable=False, disposal_cost_per_tonne=500)

plan = optimizer.optimize()
print(f"Diversion rate: {plan.diversion_rate:.1%}")
print(f"Net revenue: ${plan.net_revenue_usd:,.2f}")
print(f"Landfill reduction: {plan.landfill_reduction_tonnes:.1f} tonnes")
```

```python
from circular_economy import LifecycleTracker, RemanufacturingAssessor, SymbiosisMatcher

# Track a product's material lifecycle
tracker = LifecycleTracker(product_id="WIDGET-100")
tracker.add_stage("extraction", materials={"steel": 12.5, "aluminum": 3.0, "plastic": 2.0}, co2_kg=45.0)
tracker.add_stage("manufacturing", materials={}, co2_kg=15.0, waste_generated_kg=1.8)
tracker.add_stage("use", duration_years=5, co2_kg=2.0, maintenance_kg=0.5)
tracker.add_stage("end_of_life", recyclable_percent=78.0, co2_kg=3.0)
lifecycle = tracker.summarize()
print(f"Total embodied carbon: {lifecycle.total_co2_kg:.1f} kg CO2eq")
print(f"Recyclability: {lifecycle.end_of_life_recyclable_percent:.0f}%")

# Assess remanufacturing feasibility
assessor = RemanufacturingAssessor()
score = assessor.assess(
    product_type="industrial_pump",
    age_years=3,
    condition="good",
    material_value_usd=120,
    remanufacturing_cost_usd=85,
    new_product_cost_usd=450
)
print(f"Remanufacturing score: {score.feasibility_score:.1f}/100")
print(f"Recommendation: {score.recommendation}")

# Match industrial symbiosis opportunities
matcher = SymbiosisMatcher()
matcher.add_provider("Factory A", waste_type="waste_heat", quantity=500, location="Zone A", unit="MWh")
matcher.add_provider("Factory B", waste_type="steel_slag", quantity=200, location="Zone A", unit="tonnes")
matcher.add_seeker("Factory C", need_type="waste_heat", quantity=300, location="Zone A", unit="MWh")
matcher.add_seeker("Factory D", need_type="steel_slag", quantity=150, location="Zone A", unit="tonnes")
matches = matcher.find_matches()
for m in matches:
    print(f"  Match: {m.provider} -> {m.seeker}: {m.material_type} ({m.quantity} {m.unit})")
```

## Configuration

```python
config = {
    "mfa": {
        "system_boundary": "gate_to_gate",  # cradle_to_gate, cradle_to_grave
        "temporal_resolution": "annual",     # monthly, quarterly, annual
        "circularity_method": "mci"          # mci (Material Circularity Indicator), custom
    },
    "waste": {
        "target_diversion_rate": 0.90,
        "minimum_recycling_value_per_tonne": 10.0,
        "contamination_threshold_percent": 15.0,
        "require_certified_recycler": True
    },
    "remanufacturing": {
        "minimum_feasibility_score": 50,
        "maximum_age_years": 10,
        "condition_threshold": "fair",
        "economic_viability_required": True
    },
    "epr": {
        "jurisdictions": ["eu", "usa_california", "japan"],
        "default_fee_per_kg": 0.50,
        "reporting_deadline_month": 3,
        "require_chain_of_custody": True
    },
    "symbiosis": {
        "max_distance_km": 100,
        "minimum_quantity_tonnes": 10,
        "feasibility_threshold": 50
    }
}
```

## Use Cases

- **Manufacturing Waste Reduction**: Use MFA to identify the top 3 material loss points in a production line, then model the impact of process improvements, material substitution, or scrap recycling investments.
- **Product Take-Back Program Design**: Model reverse logistics costs, collection rates, and material recovery values to design economically viable product take-back programs for electronics or packaging.
- **Circular Design Scorecard**: Score a product portfolio against Cradle-to-Cradle criteria to identify design changes (recycled content increase, modular design, toxic material elimination) with the highest circularity impact.
- **Industrial Symbiosis Park Planning**: Match waste streams across co-located industrial facilities to create closed-loop material flows, reducing both waste disposal costs and virgin material purchases.
- **EPR Fee Optimization**: Analyze material composition across product lines to identify design changes that reduce EPR fees (e.g., reducing packaging weight, switching to lower-fee materials).
- **Recycling Infrastructure Investment**: Model recycling rate improvement scenarios (new sorting technology, collection expansion, material reprocessing capacity) to prioritize capital investments by ROI and environmental impact.

## Best Practices

- **Start with Hotspot Analysis**: Before investing in circularity solutions, use MFA to identify where the largest material losses occur. Typically 80% of material value loss happens in 1-2 process steps.
- **Design for Disassembly**: Products designed with snap-fits, minimal adhesive, and standardized fasteners can be disassembled 3-5x faster, making both repair and recycling economically viable.
- **Track Material Purity**: Recycled material quality degrades with each cycle (downcycling). Track material purity through recycling loops and invest in purification technologies when purity drops below market thresholds.
- **Value Secondary Materials Internally**: Before selling recyclable waste to external markets, evaluate whether internal reuse (same facility, different product line) captures more value. Internal loops are almost always more profitable than external ones.
- **Model Reverse Logistics Costs**: Product take-back programs often fail because reverse logistics costs exceed the material recovery value. Model transport, sorting, and processing costs before committing to take-back commitments.
- **Use Circularity Indicators Quantitatively**: Adopt the Material Circularity Indicator (MCI) from the Ellen MacArthur Foundation or the Circulytics tool for comparable, auditable circularity measurements.
- **Align EPR Strategy Across Jurisdictions**: EPR requirements vary dramatically by country and material type. Build a centralized EPR management system rather than handling each jurisdiction independently.
- **Consider Reuse Before Recycling**: Reuse preserves 10-100x more value than recycling. Prioritize product lifetime extension (repair, refurbishment, remanufacturing) before end-of-life recycling.

## Key Metrics & Formulas

| Metric | Formula | Description |
|--------|---------|-------------|
| **Material Circularity Indicator (MCI)** | `(V_r + V_u) / (V_t + V_w)` | Ellen MacArthur Foundation circularity metric |
| **Recycling Rate** | `Recycled_output / Total_material_input` | Percentage of input materials recovered |
| **Diversion Rate** | `Diverted_waste / Total_waste` | Percentage of waste diverted from landfill |
| **Remanufacturing ROI** | `(New_cost - Reman_cost) / Reman_cost × 100` | Return on investment for remanufacturing |
| **EPR Fee** | `Weight_kg × Fee_per_kg` | Extended Producer Responsibility compliance cost |
| **Industrial Symbiosis Value** | `Quantity × Price_savings + avoided_disposal` | Economic value of waste-as-resource exchanges |
| **Product Circularity Score** | `Weighted sum of design criteria` | 0-100 score across durability, repairability, recyclability |
| **Material Efficiency** | `Product_output / Material_input` | Fraction of input materials ending up in final product |
| **Recovery Rate** | `Recovered_material / Total_material_processed` | Percentage of material successfully recovered from waste |
| **Symbiosis Match Score** | `Qty_match × 60 + distance_score × 40` | Weighted feasibility of industrial symbiosis pairing |
| **Landfill Diversion Rate** | `1 - (Landfill_waste / Total_waste)` | Percentage of waste diverted from landfill via recycling or reuse |
| **EPR Compliance Rate** | `Compliant_products / Total_products` | Percentage of products with active EPR registrations |

## Related Modules

- [green-it](../green-it/GROK.md) — E-waste tracking and IT hardware lifecycle management. Extends circular-economy's general MFA with IT-specific asset tracking and disposal workflows.
- [carbon-tracking](../carbon-tracking/GROK.md) — Embodied carbon in materials and Scope 3 product lifecycle emissions. Provides the carbon accounting framework that lifecycle stages feed into.
- [green-computing](../green-computing/GROK.md) — Energy efficiency in computing systems. Addresses the operational energy dimension that complements circular-economy's material focus.
- [renewable-energy](../renewable-energy/GROK.md) — End-of-life management for solar panels, wind turbine blades, and batteries. Handles the circularity challenges specific to renewable energy equipment.

## Standards & Frameworks Referenced

This module implements methodologies from the following standards:

- **Ellen MacArthur Foundation**: Material Circularity Indicator (MCI), Circulytics assessment framework, and the butterfly diagram for material flow visualization.
- **Cradle to Cradle (C2C)**: Product design scoring across material health, material reutilization, renewable energy, water stewardship, and social fairness.
- **ISO 14040/14044**: Life Cycle Assessment (LCA) methodology for environmental impact assessment across product stages.
- **EU WEEE Directive**: Waste Electrical and Electronic Equipment directive requirements for producer responsibility and collection targets.
- **GHG Protocol Scope 3**: Categories 1 (Purchased Goods) and 12 (End-of-Life) for lifecycle emissions tracking.
- **GRI 301/306**: Global Reporting Initiative standards for materials and waste reporting.
- **EU Circular Economy Action Plan**: Policy framework for sustainable product design, waste reduction, and secondary material markets.

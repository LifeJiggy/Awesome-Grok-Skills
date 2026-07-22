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

---

## Advanced Configuration

The circular economy module supports advanced configuration for material flow analysis precision, waste stream classification, and industrial symbiosis matching. These options are available through the `AdvancedConfig` class or via environment variables.

```python
from circular_economy import AdvancedConfig

config = AdvancedConfig(
    # MFA configuration
    mfa_boundary="cradle_to_grave",  # cradle_to_gate, gate_to_gate, cradle_to_grave
    mfa_temporal_resolution="monthly",  # daily, weekly, monthly, quarterly, annual
    mfa_circularity_method="mci",  # mci, custom
    mfa_uncertainty_method="monte_carlo",  # monte_carlo, analytical, none
    mfa_monte_carlo_iterations=10000,

    # Waste classification
    waste_classification_system="eu_waste_catalog",  # eu_waste_catalog, epa_rcra, custom
    waste_hazardous_threshold_percent=0.1,
    waste_contamination_penalty_factor=0.5,

    # Recycling configuration
    recycling_rate_calculation="mass_based",  # mass_based, value_based
    recycling_purity_threshold_percent=90,
    recycling_downcycling_detection=True,

    # Remanufacturing
    remanufacturing_feasibility_threshold=50,
    remanufacturing_economic_viability_required=True,
    remanufacturing_condition_assessment_method="visual",  # visual, diagnostic, destructive

    # Industrial symbiosis
    symbiosis_max_distance_km=100,
    symbiosis_min_quantity_tonnes=10,
    symbiosis_feasibility_threshold=50,
    symbiosis_logistics_cost_per_tonne_km=0.50,

    # EPR tracking
    epr_jurisdictions=["eu", "usa_california", "japan"],
    epr_fee_calculation_method="weight",  # weight, value, units
    epr_reporting_deadline_month=3
)
```

### Material Database Configuration

```python
from circular_economy import MaterialDatabaseConfig

material_config = MaterialDatabaseConfig(
    primary_source="custom",  # ecoinvent,GaBi, custom
    custom_materials_db="/data/materials.json",
    recycling_rates={
        "steel": {"primary": 0.85, "secondary": 0.70},
        "aluminum": {"primary": 0.90, "secondary": 0.75},
        "copper": {"primary": 0.80, "secondary": 0.65},
        "plastic_pet": {"primary": 0.30, "secondary": 0.25},
        "plastic_hdpe": {"primary": 0.25, "secondary": 0.20}
    },
    embodied_carbon_kg_per_kg={
        "steel": 1.85,
        "aluminum": 8.24,
        "copper": 3.81,
        "plastic_pet": 2.15,
        "glass": 0.86
    }
)
```

## Architecture Patterns

### Event Sourcing for Material Flows

Every material movement is recorded as an immutable event:

```python
from circular_economy import MaterialEventStore, MaterialEvent

store = MaterialEventStore(database="postgresql://localhost/circular")

# Record material input
event = MaterialEvent(
    system="Widget Manufacturing",
    material_type="steel",
    quantity_tonnes=500,
    event_type="input",
    source="primary_extraction",
    timestamp="2025-01-15T08:00:00Z"
)
store.append(event)

# Record material output
output_event = MaterialEvent(
    system="Widget Manufacturing",
    material_type="steel_scrap",
    quantity_tonnes=95,
    event_type="output",
    destination="recycler",
    timestamp="2025-01-15T16:00:00Z"
)
store.append(output_event)

# Replay events for MFA
events = store.get_events(system="Widget Manufacturing", period="2025-01")
```

### CQRS for Material Analysis

```python
from circular_economy import MaterialWriteModel, MaterialReadModel

write_model = MaterialWriteModel()
read_model = MaterialReadModel()

# Write: add material flows
write_model.add_flow(material="steel", quantity=500, direction="input")

# Read: query circularity metrics
circularity = read_model.get_circularity_indicator(
    system="Widget Manufacturing",
    period="2025-Q1"
)
```

### Saga Pattern for EPR Compliance

```python
from circular_economy import EPRComplianceSaga

saga = EPRComplianceSaga(
    producer="Acme Manufacturing",
    jurisdictions=["eu", "usa_california"]
)

# Execute multi-jurisdiction compliance
compliance = saga.execute(
    products=product_list,
    reporting_year=2025
)
print(f"EU compliance: {compliance.eu_status}")
print(f"CA compliance: {compliance.ca_status}")
```

## Integration Guide

### ERP Integration

```python
from circular_economy import ERPConnector

# SAP integration
sap = ERPConnector(
    platform="sap",
    api_url="https://erp.internal/api",
    credentials_file="/etc/circular-economy/erp-credentials.json"
)

# Import bill of materials
bom = sap.get_bom(product_id="WIDGET-100")
for material in bom.materials:
    mfa.add_input(
        material_type=material.name,
        tonnes=material.quantity_kg / 1000,
        source="purchased"
    )

# Import waste data
waste = sap.get_waste_records(facility="Assembly Plant")
for record in waste:
    optimizer.add_waste_stream(
        name=record.waste_type,
        tonnes=record.quantity_kg / 1000,
        recyclable=record.is_recyclable
    )
```

### Waste Exchange Platform Integration

```python
from circular_economy import WasteExchangeConnector

# Connect to industrial symbiosis platform
exchange = WasteExchangeConnector(
    platform="loop_industries",
    api_key="your-key"
)

# List available waste streams
available = exchange.list_available_waste(
    region="Midwest US",
    material_type="metal_scrap"
)

# Match with seek requests
matches = exchange.find_matches(
    provider="Factory A",
    waste_type="steel_scrap",
    quantity_tonnes=95
)
```

### LCA Software Integration

```python
from circular_economy import SimaProConnector, OpenLCAConnector

# SimaPro integration
simapro = SimaProConnector(
    project_path="/data/lca_project.sp"
)

# Export MFA data to LCA
lca_data = mfa.export_for_lca()
simapro.import_material_flows(lca_data)

# OpenLCA integration
openlca = OpenLCAConnector(
    database="ecoinvent_3.9"
)

# Calculate environmental impacts
impacts = openlca.calculate_impacts(
    flows=lca_data,
    impact_categories=["gwp", "ap", "ep"]
)
```

## Performance Optimization

### Batch Material Processing

```python
from circular_economy import BatchMaterialProcessor

processor = BatchMaterialProcessor(
    batch_size=1000,
    parallel_workers=4,
    cache_intermediate=True
)

# Process large MFA datasets
results = processor.process(
    materials=large_material_list,
    system="Manufacturing Complex"
)
print(f"Processed {results.record_count} records in {results.elapsed_seconds:.1f}s")
```

### Cached Recycling Rates

```python
from circular_economy import CachedRecyclingRates

rates = CachedRecyclingRates(
    cache_backend="redis",
    cache_ttl_seconds=86400,
    precompute_common=True
)

# Fast lookup for frequently used rates
rate = rates.get(
    material="aluminum",
    region="US",
    method="primary"
)
```

## Security Considerations

### Data Encryption

Material flow data may contain sensitive business information:

```python
from circular_economy import EncryptedMaterialStore

store = EncryptedMaterialStore(
    database="postgresql://localhost/circular",
    encryption_key_ref="aws_kms:material-data-key",
    column_level_encryption=["quantity", "cost"],
    audit_logging=True
)
```

### Access Control

```python
from circular_economy import RBACManager

rbac = RBACManager()

# Define roles
rbac.define_role("material_analyst", permissions=["read", "analyze"])
rbac.define_role("sustainability_manager", permissions=["read", "analyze", "report"])
rbac.define_role("auditor", permissions=["read", "audit"])

# Assign users
rbac.assign_role("analyst@company.com", "material_analyst")
rbac.assign_role("manager@company.com", "sustainability_manager")
```

## Troubleshooting Guide

| Issue | Possible Cause | Resolution |
|-------|---------------|------------|
| Circularity rate too low | High virgin material input | Increase recycled content, reduce waste |
| Recycling rate below target | Contamination in waste streams | Improve sorting, reduce contamination |
| Remanufacturing score low | Product design not optimized | Apply design for disassembly principles |
| Symbiosis match failed | Distance too far or quantity too small | Adjust distance/quantity thresholds |
| EPR fee higher than expected | Material composition high-fee | Redesign product to use lower-fee materials |

```python
# Diagnostic script
from circular_economy import DiagnosticRunner

diag = DiagnosticRunner(system="Widget Manufacturing")
results = diag.run_all()
for check in results:
    status = "PASS" if check.passed else "FAIL"
    print(f"[{status}] {check.name}: {check.message}")
```

## API Reference

### MaterialFlowAnalyzer

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_input(material, tonnes, source)` | material: str, tonnes: float, source: str | `None` | Add material input |
| `add_process(name, inputs, outputs)` | name: str, inputs: List, outputs: List | `None` | Add transformation process |
| `add_output(material, tonnes, destination)` | material: str, tonnes: float, destination: str | `None` | Add material output |
| `analyze()` | - | `FlowReport` | Generate MFA report |

### WasteOptimizer

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_waste_stream(...)` | name, tonnes, recyclable, value | `None` | Add waste stream |
| `optimize()` | - | `OptimizationPlan` | Generate optimization plan |
| `get_diversion_rate()` | - | `float` | Current diversion rate |

### CircularDesignScorer

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `score_product(product)` | product: dict | `DesignScore` | Score product circularity |
| `get_recommendations(score)` | score: DesignScore | `List[Recommendation]` | Get improvement recommendations |
| `benchmark(industry)` | industry: str | `BenchmarkResult` | Benchmark against industry |

## Data Models

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class FlowReport:
    system: str
    total_input_tonnes: float
    product_output_tonnes: float
    recycled_output_tonnes: float
    waste_tonnes: float
    circularity_rate: float
    timestamp: datetime

@dataclass
class DesignScore:
    product_name: str
    total_score: float
    rating: str  # bronze, silver, gold, platinum
    durability_score: float
    reparability_score: float
    recyclability_score: float
    recycled_content: float
    toxic_free: bool
    recommendations: List[str]

@dataclass
class SymbiosisMatch:
    provider: str
    seeker: str
    material_type: str
    quantity: float
    unit: str
    distance_km: float
    feasibility_score: float
    estimated_savings_usd: float

@dataclass
class EPRCompliance:
    jurisdiction: str
    products_registered: int
    total_fees_usd: float
    reporting_deadline: str
    status: str  # compliant, pending, overdue
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN pip install circular-economy[all]

COPY config.yaml /etc/circular-economy/config.yaml

HEALTHCHECK --interval=30s --timeout=5s \
  CMD python -c "from circular_economy import health_check; health_check()"

ENTRYPOINT ["circular-economy"]
CMD ["serve", "--config", "/etc/circular-economy/config.yaml"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: circular-economy-analyzer
spec:
  replicas: 2
  selector:
    matchLabels:
      app: circular-economy
  template:
    spec:
      containers:
      - name: analyzer
        image: circular-economy:1.0.0
        env:
        - name: CIRCULAR_DB_URL
          valueFrom:
            secretKeyRef:
              name: circular-db
              key: url
```

## Monitoring & Observability

### Metrics Collection

```python
from circular_economy import MetricsCollector

collector = MetricsCollector()

# Register custom metrics
collector.register_gauge("circularity_rate", "Current circularity rate")
collector.register_counter("waste_diverted_tonnes", "Total waste diverted")
collector.register_histogram("mfa_calculation_duration_seconds", "MFA calculation time")
collector.register_counter("symbiosis_matches_total", "Total symbiosis matches")
```

### Dashboard Integration

```python
from circular_economy import DashboardExporter

dashboard = DashboardExporter(
    grafana_url="https://grafana.internal",
    datasource="circular_economy"
)

# Push real-time data
dashboard.push_metrics({
    "circularity_rate": 0.72,
    "diversion_rate": 0.85,
    "recycling_rate": 0.68
})
```

## Testing Strategy

```python
import pytest
from circular_economy import MaterialFlowAnalyzer, WasteOptimizer

class TestMaterialFlowAnalyzer:
    def test_mfa_calculation(self):
        mfa = MaterialFlowAnalyzer(system="Test System")
        mfa.add_input("steel", tonnes=100, source="primary")
        mfa.add_process("stamping", input_materials=["steel"], output_materials=["widget", "scrap"])
        mfa.add_output("widget", tonnes=80, destination="market")
        mfa.add_output("scrap", tonnes=20, destination="recycler")

        report = mfa.analyze()
        assert report.total_input_tonnes == 100
        assert report.circularity_rate > 0

class TestWasteOptimizer:
    def test_diversion_rate(self):
        optimizer = WasteOptimizer(facility="Test Plant")
        optimizer.add_waste_stream("metal", tonnes=100, recyclable=True, value_per_tonne=150)
        optimizer.add_waste_stream("plastic", tonnes=50, recyclable=True, value_per_tonne=80)
        optimizer.add_waste_stream("hazardous", tonnes=10, recyclable=False, disposal_cost_per_tonne=500)

        plan = optimizer.optimize()
        assert plan.diversion_rate > 0
        assert plan.net_revenue_usd > 0
```

## Versioning & Migration

### Semantic Versioning

- **MAJOR**: Breaking changes to API, MFA methodology changes
- **MINOR**: New material types, new EPR jurisdictions
- **PATCH**: Bug fixes, performance improvements

### Migration Guide

```python
# v1.x to v2.x migration
# Old API
mfa = MaterialFlowAnalyzer("Widget Manufacturing")

# New API
mfa = MaterialFlowAnalyzer(
    system="Widget Manufacturing",
    boundary="cradle_to_grave",
    temporal_resolution="monthly"
)
```

## Glossary

| Term | Definition |
|------|-----------|
| **MFA** | Material Flow Analysis — tracking materials through a system |
| **MCI** | Material Circularity Indicator — Ellen MacArthur Foundation metric |
| **C2C** | Cradle to Cradle — product design certification framework |
| **EPR** | Extended Producer Responsibility — producer obligation for end-of-life |
| **WEEE** | Waste Electrical and Electronic Equipment — EU directive |
| **Downcycling** | Recycling that reduces material quality |
| **Upcycling** | Recycling that improves material quality |
| **Industrial Symbiosis** | One company's waste as another's feedstock |
| **Remanufacturing** | Restoring used products to like-new condition |
| **Refurbishment** | Repairing and cleaning used products for resale |
| **Reverse Logistics** | Managing product return flows from consumers |
| **Sankey Diagram** | Visual representation of material flows |

## Changelog

### v1.0.0 (2025-01-15)
- Initial release with MFA implementation
- Waste stream optimization
- Circular design scoring

### v1.1.0 (2025-02-01)
- Added industrial symbiosis matching
- Improved remanufacturing assessment
- Added EPR tracking

### v1.2.0 (2025-03-01)
- Added lifecycle tracking
- Performance improvements for large MFA datasets
- Added multi-jurisdiction EPR support

## Contributing Guidelines

1. **Fork the repository** and create a feature branch from `main`
2. **Write tests** for all new functionality with >80% coverage
3. **Follow PEP 8** style guidelines with type hints
4. **Update documentation** for any API changes
5. **Add changelog entries** under `[Unreleased]` section
6. **Submit a pull request** with a clear description of changes

### Code Review Checklist

- [ ] Tests pass and coverage meets threshold
- [ ] MFA calculations follow ISO 14050
- [ ] Material flows are auditable
- [ ] EPR compliance covers all jurisdictions
- [ ] No hardcoded recycling rates (use database)

## License

This module is licensed under the Apache License, Version 2.0. See the LICENSE file for full terms.

Copyright 2025 Circular Economy Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

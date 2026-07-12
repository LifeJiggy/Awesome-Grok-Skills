---
name: "carbon-tracking"
category: "sustainability"
version: "1.0.0"
tags: ["sustainability", "carbon-tracking", "emissions", "ghg-protocol", "carbon-accounting"]
---

# Carbon Tracking

## Overview

Carbon Tracking is the systematic measurement, reporting, and verification of greenhouse gas (GHG) emissions across an organization's operations and value chain. This module implements the complete GHG Protocol Corporate Standard framework, covering Scope 1 (direct emissions from owned sources), Scope 2 (indirect emissions from purchased electricity, steam, heating, and cooling), and Scope 3 (all other indirect emissions across 15 value chain categories). It provides tools for calculating emissions factors, managing carbon credit inventories, tracking reduction targets against Science-Based Targets initiative (SBTi) pathways, and integrating with carbon accounting APIs for real-time emissions monitoring.

The module is built around the principle that accurate carbon accounting is the foundation of any credible climate strategy. Without precise, auditable emissions data, reduction claims lack substance and carbon offset purchases lack verification. The framework handles the complexity of multi-entity corporate structures, regional grid emission factors that change annually, Scope 3 category estimation methods (spend-based, activity-based, average-data, and supplier-specific), and the reconciliation of carbon credit retirements against reported emissions.

Carbon tracking extends beyond mere compliance reporting. Organizations increasingly need granular, real-time emissions data to make operational decisions — choosing suppliers, selecting logistics routes, designing products, and planning capital investments. This module provides the computational infrastructure to embed carbon intelligence into business processes, from procurement scoring based on supplier emissions to product-level carbon labels that inform consumer choices. It supports both absolute emissions tracking and intensity metrics (emissions per revenue, per employee, per unit produced) for fair comparison across business units and time periods.

## Core Capabilities

- **Scope 1/2/3 Emissions Calculation**: Full GHG Protocol implementation covering all three scopes with 15 Scope 3 categories, activity-based and spend-based calculation methods, and regional emission factors.
- **Carbon Credit Management**: Track carbon credit purchases, retirements, and inventory across multiple registries (Verra VCS, Gold Standard, ACR, CAR) with vintage tracking and quality scoring.
- **Science-Based Target Tracking**: Monitor emissions reduction progress against SBTi-approved pathways, including linear and sector-specific decarbonization curves.
- **Real-Time Emissions Monitoring**: Integrate with smart meters, IoT sensors, and carbon accounting APIs for continuous emissions data collection and alerting.
- **Supply Chain Emissions Tracking**: Collect and aggregate supplier-specific emissions data (CDP, PCAF) and estimate missing data using industry averages and spend-based methods.
- **Carbon Accounting API Integration**: Connect to Climatiq, CarbonInterface, Watershed, and other carbon accounting platforms for emission factor lookup and calculation.
- **Multi-Entity Corporate Reporting**: Support consolidated, operational control, equity share, and financial control boundary methodologies for corporate group emissions.
- **Audit Trail and Verification**: Complete calculation provenance with data lineage, assumption documentation, and support for third-party verification workflows.

## Architecture

The carbon tracking system follows the GHG Protocol's accounting architecture:

1. **Data Ingestion Layer**: Collects activity data from utility meters, fuel purchase records, travel systems, procurement databases, and supplier disclosures. Supports both batch import and real-time streaming.
2. **Emission Factor Engine**: Maintains a database of emission factors from EPA, DEFRA, IEA, and IPCC, with automatic annual updates and regional granularity. Factors are tagged with source, year, and uncertainty bounds.
3. **Calculation Engine**: Applies the correct methodology (location-based vs. market-based for Scope 2, activity-based vs. spend-based for Scope 3) based on data availability and quality thresholds.
4. **Carbon Credit Ledger**: Double-entry bookkeeping for carbon credit purchases, transfers, and retirements with registry reconciliation.
5. **Reporting Layer**: Generates GHG Protocol-compliant reports, SBTi progress dashboards, CDP questionnaires, and custom analytics.

## Usage Examples

```python
from carbon_tracking import GHGCalculator, EmissionFactorDB, Scope3Category

# Initialize the GHG calculator
calc = GHGCalculator(fiscal_year=2025, reporting_entity="Acme Corp")

# Scope 1: Direct emissions
calc.add_scope1(
    category="stationary_combustion",
    source="Natural gas boilers",
    activity_data=50000,  # therms
    unit="therms",
    emission_factor=5.301,  # kgCO2e/therm
    source_dataset="EPA"
)
calc.add_scope1(
    category="mobile_combustion",
    source="Company fleet vehicles",
    activity_data=1200000,  # miles
    unit="miles",
    emission_factor=0.352,  # kgCO2e/mile (average sedan)
    source_dataset="EPA"
)

# Scope 2: Electricity (location-based)
calc.add_scope2(
    category="purchased_electricity",
    source="US operations",
    activity_data=8500000,  # kWh
    unit="kWh",
    grid_emission_factor=0.417,  # kgCO2e/kWh (US average)
    method="location_based",
    source_dataset="EPA eGRID"
)

# Scope 3: Supply chain
calc.add_scope3(
    category=Scope3Category.PURCHASED_GOODS,
    source="Raw materials",
    spend_usd=12_000_000,
    emission_factor=0.45,  # kgCO2e/USD
    data_quality="spend_based"
)
calc.add_scope3(
    category=Scope3Category.BUSINESS_TRAVEL,
    source="Air travel",
    activity_data=250000,  # passenger-miles
    unit="passenger-miles",
    emission_factor=0.255,  # kgCO2e/passenger-mile
    data_quality="activity_based"
)

# Generate report
report = calc.generate_report()
print(f"Scope 1: {report.scope1_total_tonnes:,.1f} tCO2e")
print(f"Scope 2: {report.scope2_total_tonnes:,.1f} tCO2e")
print(f"Scope 3: {report.scope3_total_tonnes:,.1f} tCO2e")
print(f"Total:   {report.grand_total_tonnes:,.1f} tCO2e")
```

```python
from carbon_tracking import CarbonCreditRegistry, ReductionTracker

# Manage carbon credit portfolio
registry = CarbonCreditRegistry()
registry.purchase(credits=5000, standard="verra_vcs", project="wind_farm_india",
                  vintage=2024, price_per_tonne=12.50, registry_id="VCS-2024-1234")
registry.purchase(credits=2000, standard="gold_standard", project="cookstoves_kenya",
                  vintage=2024, price_per_tonne=18.00, registry_id="GS-2024-5678")

# Retire credits against emissions
retirement = registry.retire(credits=3000, standard="verra_vcs",
                              reason="FY2025 offset", retired_for="Acme Corp")
print(f"Retired {retirement.credits} credits from {retirement.project}")
print(f"Remaining Verra credits: {registry.balance('verra_vcs')}")

# Track reduction targets
tracker = ReductionTracker(
    base_year=2020,
    base_emissions_tonnes=50000,
    target_reduction_percent=50,
    target_year=2030
)
current_emissions = 38000
progress = tracker.calculate_progress(current_year=2025, current_emissions=current_emissions)
print(f"Reduction achieved: {progress.percent_reduced:.1f}%")
print(f"On track: {progress.on_track}")
print(f"Required annual reduction: {progress.annual_reduction_needed_tonnes:.0f} tCO2e")
```

## Configuration

```python
config = {
    "reporting": {
        "fiscal_year": 2025,
        "boundary_method": "operational_control",  # or equity_share, financial_control
        "consolidation_entities": ["subsidiary_a", "subsidiary_b"],
        "reporting_standard": "ghg_protocol_corporate"
    },
    "emission_factors": {
        "source": "epa",  # or defra, iea
        "update_frequency": "annual",
        "regional_granularity": "state"  # country, state, subregion
    },
    "carbon_credits": {
        "accepted_standards": ["verra_vcs", "gold_standard", "acr"],
        "minimum_vintage": 2020,
        "quality_threshold": 0.7
    },
    "sbti": {
        "pathway": "1.5C_linear",  # or well_below_2C, sector_specific
        "base_year": 2020,
        "target_year": 2030,
        "scope_coverage": "1_2_3"
    }
}
```

## Use Cases

- **Annual Sustainability Report**: Generate GHG Protocol-compliant emissions inventory for inclusion in annual sustainability reports, CDP disclosures, and TCFD climate risk assessments.
- **Supplier Emissions Benchmarking**: Compare Scope 3 Category 1 (Purchased Goods) emissions across suppliers to identify high-impact procurement decisions and negotiate emission reduction targets.
- **Carbon Credit Portfolio Management**: Track purchases across multiple registries, optimize retirement timing based on vintage and price, and maintain audit-ready documentation for third-party verification.
- **Science-Based Target Progress**: Monthly tracking of emissions reduction progress against SBTi-approved 1.5°C pathway, with automated alerts when reduction pace falls behind schedule.
- **M&A Due Diligence**: Assess target company emissions profile, carbon credit inventory, and reduction commitments during merger and acquisition due diligence processes.
- **Product Carbon Footprint Labeling**: Calculate cradle-to-gate carbon footprint per product unit using lifecycle data, enabling consumer-facing carbon labels and eco-design comparisons.

## Best Practices

- **Follow GHG Protocol Boundaries**: Clearly define organizational and operational boundaries before calculating emissions. Inconsistent boundaries across years invalidate trend comparisons.
- **Use Primary Data Over Defaults**: Activity-based calculations (actual fuel consumed, actual kWh metered) are always more accurate than spend-based estimates. Invest in primary data collection from suppliers and facilities.
- **Apply Data Quality Scores**: The GHG Protocol's data quality matrix (5 levels for reliability, temporal, geographical, technological, and completeness) should accompany every emission factor. Never present calculated emissions without uncertainty bounds.
- **Separate Location-Based and Market-Based Scope 2**: Location-based uses average grid factors; market-based reflects actual electricity procurement (RECs, PPAs, direct contracts). Report both per GHG Protocol Scope 2 Guidance.
- **Retire Credits, Don't Just Purchase**: Purchased but unretired credits are inventory, not offsets. Only retired credits can be claimed against emissions. Track retirements separately from purchases.
- **Verify with Third Parties**: Internal calculations should be verified by an accredited third party (ISO 14064-3, AA1000) for any public disclosure. Build audit trails from day one.
- **Update Emission Factors Annually**: Grid emission factors change every year as the energy mix evolves. Using a 2020 factor for 2025 emissions introduces systematic error. Use the most current published factors.
- **Disclose Scope 3 Categories Materiality**: Not all 15 Scope 3 categories are material for every organization. Perform a materiality assessment and focus data collection on categories that represent >5% of total Scope 3.

## Key Metrics & Formulas

| Metric | Formula | Description |
|--------|---------|-------------|
| **Scope 1** | `Activity_data × Emission_factor` | Direct emissions from owned/controlled sources |
| **Scope 2 (Location)** | `kWh × Grid_emission_factor` | Average grid emissions for electricity consumed |
| **Scope 2 (Market)** | `kWh × Supplier_emission_factor` | Actual supplier-specific emission factor |
| **Scope 3** | `Σ(Activity × Factor) or (Spend × Factor)` | Value chain emissions across 15 categories |
| **Carbon Intensity** | `Total_CO2 / Revenue` or `/ Employee` | Normalized emissions for benchmarking |
| **SBTi Progress** | `(Base - Current) / Base × 100` | Percentage reduction toward science-based target |
| **Credit Portfolio Value** | `Σ(Credits × Price)` | Total market value of carbon credit holdings |
| **Retirement Ratio** | `Credits_retired / Credits_purchased` | Fraction of purchased credits that have been retired |
| **Emission Intensity** | `Total_CO2 / Revenue` | Normalized emissions per unit of revenue for benchmarking |
| **Scope 3 Category Share** | `Category_CO2 / Total_Scope3 × 100` | Percentage of Scope 3 from a specific category |

## Related Modules

- [green-computing](../green-computing/GROK.md) — Carbon-aware computing and real-time grid carbon intensity. Provides operational carbon data that feeds into Scope 2 calculations.
- [green-it](../green-it/GROK.md) — IT infrastructure sustainability and PUE optimization. Supplies electricity consumption data and embodied carbon figures for IT assets.
- [renewable-energy](../renewable-energy/GROK.md) — Renewable energy procurement and certificate tracking. Enables market-based Scope 2 calculations using RECs and PPAs.
- [circular-economy](../circular-economy/GROK.md) — Material flow analysis and lifecycle emissions. Provides embodied carbon and end-of-life emissions data for Scope 3 Category 1 (Purchased Goods).

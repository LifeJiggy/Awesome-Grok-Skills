---
name: "carbon-tracking"
category: "climate-tech"
version: "2.0.0"
tags: ["climate-tech", "carbon-tracking", "emissions", "GHG", "carbon-footprint"]
---

# Carbon Tracking

## Overview

The Carbon Tracking module provides comprehensive tools for measuring, reporting, and verifying greenhouse gas (GHG) emissions across organizational operations. It covers Scope 1, 2, and 3 emissions calculation, carbon footprint analysis, emissions factor databases, reduction target setting, carbon offset verification, and regulatory reporting (GHG Protocol, CDP, TCFD). The module integrates with supply chain data, energy systems, and transportation networks for enterprise-wide carbon accounting.

This skill is essential for sustainability managers, environmental compliance officers, ESG analysts, and corporate responsibility teams managing climate commitments.

## Core Capabilities

- **Scope 1 Emissions**: Direct emissions from owned/controlled sources (fuel combustion, process emissions, fugitive emissions)
- **Scope 2 Emissions**: Indirect emissions from purchased electricity, steam, heating, and cooling
- **Scope 3 Emissions**: Value chain emissions (purchased goods, business travel, employee commuting, waste)
- **Emissions Factors**: Comprehensive database of GHG emissions factors by fuel type, region, and activity
- **Carbon Footprint**: Organizational, product, and individual carbon footprint calculation
- **Reduction Tracking**: Target setting (SBTi-aligned), progress monitoring, and reduction pathway modeling
- **Carbon Offsets**: Offset credit verification, retirement tracking, and quality assessment
- **Reporting**: GHG Protocol compliance, CDP disclosure, TCFD alignment, and EU CSRD reporting

## Usage Examples

```python
from carbon_tracking import (
    GHGCalculator,
    EmissionsFactorDB,
    CarbonFootprint,
    ReductionTracker,
    OffsetManager,
    ReportGenerator,
)

# --- Emissions Calculation ---
calc = GHGCalculator()
scope1 = calc.calculate_scope1(
    fuel_type="natural_gas",
    quantity=10000,
    unit="therms",
    region="US",
)
print(f"Scope 1: {scope1.emissions_tonnes:.2f} tCO2e")

scope2 = calc.calculate_scope2(
    electricity_kwh=500000,
    grid_factor=0.4,
    method="market",
)
print(f"Scope 2: {scope2.emissions_tonnes:.2f} tCO2e")

scope3 = calc.calculate_scope3(
    category="business_travel",
    distance_km=100000,
    passengers=50,
    mode="air",
)
print(f"Scope 3: {scope3.emissions_tonnes:.2f} tCO2e")

# --- Emissions Factor Database ---
db = EmissionsFactorDB()
factor = db.get_factor("diesel", "US", "combustion")
print(f"Diesel factor: {factor.factor} {factor.unit}")

# --- Carbon Footprint ---
footprint = CarbonFootprint(org_name="TechCorp")
footprint.add_scope(scope1)
footprint.add_scope(scope2)
footprint.add_scope(scope3)
total = footprint.total_emissions()
print(f"Total footprint: {total:.2f} tCO2e")

# --- Reduction Tracking ---
tracker = ReductionTracker(baseline_year=2020, baseline_emissions=50000)
tracker.add_actual(year=2024, emissions=42000)
progress = tracker.progress()
print(f"Reduction: {progress.reduction_pct:.1f}%")
print(f"On track: {progress.on_track}")

# --- Offset Management ---
offsets = OffsetManager()
offsets.purchase(credits=1000, vintage=2024, project="reforestation")
offsets.retire(credits=500, reason="Scope 1 neutralization")
balance = offsets.balance()
print(f"Offset balance: {balance} credits")

# --- Reporting ---
reporter = ReportGenerator()
report = reporter.generate_ghg_protocol(footprint, year=2024)
reporter.export_json(report, "ghg_report_2024.json")
```

## Best Practices

- Follow the GHG Protocol Corporate Standard for organizational emissions accounting
- Use location-based AND market-based methods for Scope 2 electricity emissions
- Collect primary data for Scope 3 categories where possible; use secondary data as fallback
- Apply appropriate emission factors by region — global averages introduce significant error
- Set science-based targets (SBTi) aligned with 1.5°C pathway
- Verify emissions data annually through third-party assurance (ISO 14064)
- Report emissions by business unit, facility, and activity for actionable insights
- Prioritize Scope 3 categories by materiality — typically purchased goods and business travel
- Retire carbon offsets immediately upon use to prevent double-counting
- Maintain emissions data for at least 7 years for regulatory compliance

## Related Modules

- **environmental-modeling**: Ecosystem carbon cycle modeling
- **climate-data**: Climate data for emissions projections
- **renewable-energy**: Clean energy transition tracking
- **emission-reduction**: Reduction strategy and pathway modeling

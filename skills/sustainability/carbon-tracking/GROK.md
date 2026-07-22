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

Carbon tracking extends beyond mere compliance reporting. Organizations increasingly need granular, real-time emissions data to make operational decisions Ã¢â‚¬â€ choosing suppliers, selecting logistics routes, designing products, and planning capital investments. This module provides the computational infrastructure to embed carbon intelligence into business processes, from procurement scoring based on supplier emissions to product-level carbon labels that inform consumer choices. It supports both absolute emissions tracking and intensity metrics (emissions per revenue, per employee, per unit produced) for fair comparison across business units and time periods.

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
- **Science-Based Target Progress**: Monthly tracking of emissions reduction progress against SBTi-approved 1.5Ã‚Â°C pathway, with automated alerts when reduction pace falls behind schedule.
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
| **Scope 1** | `Activity_data Ãƒâ€” Emission_factor` | Direct emissions from owned/controlled sources |
| **Scope 2 (Location)** | `kWh Ãƒâ€” Grid_emission_factor` | Average grid emissions for electricity consumed |
| **Scope 2 (Market)** | `kWh Ãƒâ€” Supplier_emission_factor` | Actual supplier-specific emission factor |
| **Scope 3** | `ÃŽÂ£(Activity Ãƒâ€” Factor) or (Spend Ãƒâ€” Factor)` | Value chain emissions across 15 categories |
| **Carbon Intensity** | `Total_CO2 / Revenue` or `/ Employee` | Normalized emissions for benchmarking |
| **SBTi Progress** | `(Base - Current) / Base Ãƒâ€” 100` | Percentage reduction toward science-based target |
| **Credit Portfolio Value** | `ÃŽÂ£(Credits Ãƒâ€” Price)` | Total market value of carbon credit holdings |
| **Retirement Ratio** | `Credits_retired / Credits_purchased` | Fraction of purchased credits that have been retired |
| **Emission Intensity** | `Total_CO2 / Revenue` | Normalized emissions per unit of revenue for benchmarking |
| **Scope 3 Category Share** | `Category_CO2 / Total_Scope3 Ãƒâ€” 100` | Percentage of Scope 3 from a specific category |

## Related Modules

- [green-computing](../green-computing/GROK.md) Ã¢â‚¬â€ Carbon-aware computing and real-time grid carbon intensity. Provides operational carbon data that feeds into Scope 2 calculations.
- [green-it](../green-it/GROK.md) Ã¢â‚¬â€ IT infrastructure sustainability and PUE optimization. Supplies electricity consumption data and embodied carbon figures for IT assets.
- [renewable-energy](../renewable-energy/GROK.md) Ã¢â‚¬â€ Renewable energy procurement and certificate tracking. Enables market-based Scope 2 calculations using RECs and PPAs.
- [circular-economy](../circular-economy/GROK.md) Ã¢â‚¬â€ Material flow analysis and lifecycle emissions. Provides embodied carbon and end-of-life emissions data for Scope 3 Category 1 (Purchased Goods).

---

## Advanced Configuration

The carbon tracking module supports advanced configuration for emission factor sources, calculation methodologies, and reporting granularity. These options are available through the `AdvancedConfig` class or via environment variables.

```python
from carbon_tracking import AdvancedConfig

config = AdvancedConfig(
    # Emission factor database
    factor_source="epa",  # epa, defra, iea, custom
    factor_vintage="latest",
    factor_update_auto=True,
    factor_custom_db_path="/data/custom_factors.db",

    # Calculation precision
    calculation_precision_decimal_places=6,
    uncertainty_propagation="monte_carlo",  # monte_carlo, analytical, none
    monte_carlo_iterations=10000,

    # Scope 2 methodology
    scope2_method="market_based",  # location_based, market_based, dual
    market_based_data_quality_threshold=0.7,

    # Scope 3 estimation
    scope3_estimation_method="activity_based",  # activity_based, spend_based, average
    scope3_data_quality_matrix=True,
    scope3_materiality_threshold_percent=5,

    # Reporting
    reporting_standard="ghg_protocol",  # ghg_protocol, cdp, tcfd, custom
    currency_inflation_adjusted=True,
    base_year_currency="usd_2020",

    # Audit trail
    audit_trail_enabled=True,
    audit_trail_retention_years=7,
    audit_trail_hash_algorithm="sha256"
)
```

### Emission Factor Configuration

```python
from carbon_tracking import EmissionFactorConfig

ef_config = EmissionFactorConfig(
    # Primary sources
    primary_source="epa_egrid",
    fallback_sources=["defra_2024", "iea_2023"],

    # Regional granularity
    regional_granularity="state",  # country, state, subregion, utility
    custom_factors={
        ("US-CA", "electricity"): 0.21,  # kgCO2e/kWh
        ("DE", "electricity"): 0.35,
        ("CN", "electricity"): 0.58
    },

    # Update schedule
    auto_update=True,
    update_check_interval_days=30,
    notification_email="sustainability@company.com"
)
```

## Architecture Patterns

### Event Sourcing for Emissions Tracking

Every emission calculation is stored as an immutable event, enabling full audit trails:

```python
from carbon_tracking import EmissionEventStore, EmissionEvent

store = EmissionEventStore(database="postgresql://localhost/carbon")

# Record an emission event
event = EmissionEvent(
    entity="Acme Corp",
    scope="scope_1",
    category="stationary_combustion",
    source="Natural gas boilers",
    activity_data=50000,
    unit="therms",
    emission_factor=5.301,
    factor_source="EPA",
    emissions_kgCO2=265050,
    calculation_method="activity_based",
    timestamp="2025-01-15T10:00:00Z"
)
store.append(event)

# Replay events for audit
events = store.get_events(
    entity="Acme Corp",
    fiscal_year=2025,
    scope="scope_1"
)
```

### CQRS for Reporting vs. Calculation

Separate read and write models for emissions data:

```python
from carbon_tracking import EmissionWriteModel, EmissionReadModel

write_model = EmissionWriteModel()
read_model = EmissionReadModel()

# Write: add new emissions
write_model.add_emission(scope="scope_2", kwh=8500000, factor=0.417)

# Read: query aggregated data
total = read_model.get_scope_total(
    entity="Acme Corp",
    scope="scope_2",
    method="location_based"
)
```

### Saga Pattern for Multi-Entity Reporting

```python
from carbon_tracking import ReportingSaga

saga = ReportingSaga(
    entity="Global Corp",
    subsidiaries=["subsidiary_a", "subsidiary_b", "subsidiary_c"]
)

# Execute cross-entity reporting
report = saga.execute(
    fiscal_year=2025,
    boundary_method="operational_control",
    consolidation_method="controlled_entity"
)
```

## Integration Guide

### ERP Integration

```python
from carbon_tracking import ERPConnector

# SAP integration
sap = ERPConnector(
    platform="sap",
    api_url="https://erp.internal/api",
    credentials_file="/etc/carbon-tracking/erp-credentials.json"
)

# Import fuel purchase data
fuel_data = sap.get_fuel_purchases(fiscal_year=2025)
for purchase in fuel_data:
    calc.add_scope1(
        category="stationary_combustion",
        source=purchase.fuel_type,
        activity_data=purchase.quantity,
        unit=purchase.unit
    )

# Import electricity meter data
electricity = sap.get_electricity_readings(fiscal_year=2025)
for reading in electricity:
    calc.add_scope2(
        category="purchased_electricity",
        source=reading.facility,
        activity_data=reading.kwh,
        unit="kWh"
    )
```

### CDP Integration

```python
from carbon_tracking import CDPReporter

reporter = CDPReporter(company_id="C-12345")

# Generate CDP questionnaire responses
cdp_response = reporter.generate_response(
    fiscal_year=2025,
    emissions_data=calc.generate_report(),
    reduction_targets=tracker.get_targets()
)

# Submit to CDP portal
reporter.submit(cdp_response)
```

### Watershed/Climatiq Integration

```python
from carbon_tracking import ClimatiqClient, WatershedClient

# Climatiq emission factor lookup
climatiq = ClimatiqClient(api_key="your-key")
factor = climatiq.get_emission_factor(
    activity="electricity",
    region="US-CA",
    unit="kWh"
)

# Watershed carbon accounting
watershed = WatershedClient(api_key="your-key")
watershed.import_emissions(
    entity="Acme Corp",
    emissions=calc.generate_report()
)
```

## Performance Optimization

### Batch Calculation

For organizations with millions of emission records, batch processing is essential:

```python
from carbon_tracking import BatchCalculator

calculator = BatchCalculator(
    batch_size=10000,
    parallel_workers=4,
    use_multiprocessing=True
)

# Process large datasets efficiently
results = calculator.calculate_batch(
    records=large_emission_records,
    scope="scope_3",
    method="spend_based"
)
print(f"Processed {results.record_count} records in {results.elapsed_seconds:.1f}s")
```

### Cached Emission Factors

```python
from carbon_tracking import CachedFactorLookup

lookup = CachedFactorLookup(
    cache_backend="redis",
    cache_ttl_seconds=86400,  # 24 hours
    precompute_common=True
)

# Fast lookup for frequently used factors
factor = lookup.get(
    activity="electricity",
    region="US-CA",
    year=2025
)
```

## Security Considerations

### Data Encryption

Emissions data may contain sensitive business information. Encrypt at rest and in transit:

```python
from carbon_tracking import EncryptedEmissionStore

store = EncryptedEmissionStore(
    database="postgresql://localhost/carbon",
    encryption_key_ref="aws_kms:carbon-data-key",
    column_level_encryption=["activity_data", "emission_factor"],
    audit_logging=True
)
```

### Access Control

```python
from carbon_tracking import RBACManager

rbac = RBACManager()

# Define roles
rbac.define_role("sustainability_analyst", permissions=["read", "calculate"])
rbac.define_role("cso", permissions=["read", "calculate", "report", "audit"])
rbac.define_role("auditor", permissions=["read", "audit"])

# Assign users
rbac.assign_role("analyst@company.com", "sustainability_analyst")
rbac.assign_role("cso@company.com", "cso")
```

## Troubleshooting Guide

| Issue | Possible Cause | Resolution |
|-------|---------------|------------|
| Scope 2 market-based higher than location-based | Supplier emission factor above grid average | Verify supplier factor accuracy, check for errors |
| Scope 3 totals seem too high | Spend-based factor too aggressive | Switch to activity-based where data available |
| Carbon credit retirement not matching | Credits purchased but not retired | Execute retirement in CarbonCreditRegistry |
| SBTi progress off-track | Emissions not declining fast enough | Review reduction targets, identify high-emission sources |
| Emission factors outdated | Using previous year's factors | Update factor database, enable auto-update |

```python
# Diagnostic script
from carbon_tracking import DiagnosticRunner

diag = DiagnosticRunner(entity="Acme Corp", fiscal_year=2025)
results = diag.run_all()
for check in results:
    status = "PASS" if check.passed else "FAIL"
    print(f"[{status}] {check.name}: {check.message}")
```

## API Reference

### GHGCalculator

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `add_scope1(...)` | category, source, data, unit, factor | `None` | Add Scope 1 emission source |
| `add_scope2(...)` | category, source, data, unit, factor, method | `None` | Add Scope 2 emission source |
| `add_scope3(...)` | category, source, data/factor, quality | `None` | Add Scope 3 emission source |
| `generate_report()` | - | `EmissionsReport` | Generate consolidated report |

### CarbonCreditRegistry

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `purchase(...)` | credits, standard, project, vintage, price | `Purchase` | Purchase carbon credits |
| `retire(...)` | credits, standard, reason | `Retirement` | Retire credits against emissions |
| `balance(standard)` | standard: str | `int` | Get current credit balance |

### ReductionTracker

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `calculate_progress(...)` | year, emissions | `ProgressReport` | Calculate reduction progress |
| `project_trajectory(...)` | years | `Trajectory` | Project future emissions path |
| `get_annual_targets()` | - | `List[Target]` | Get yearly reduction targets |

## Data Models

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class EmissionsReport:
    entity: str
    fiscal_year: int
    scope1_total_tonnes: float
    scope2_total_tonnes: float
    scope3_total_tonnes: float
    grand_total_tonnes: float
    scope1_sources: List[dict]
    scope2_sources: List[dict]
    scope3_sources: List[dict]
    generation_timestamp: datetime

@dataclass
class CarbonCredit:
    credits: int
    standard: str
    project: str
    vintage: int
    registry_id: str
    price_per_tonne: float
    purchase_date: str
    status: str  # active, retired, transferred

@dataclass
class ReductionProgress:
    base_year: int
    base_emissions: float
    current_year: int
    current_emissions: float
    percent_reduced: float
    on_track: bool
    annual_reduction_needed_tonnes: float
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN pip install carbon-tracking[all]

COPY config.yaml /etc/carbon-tracking/config.yaml

HEALTHCHECK --interval=30s --timeout=5s \
  CMD python -c "from carbon_tracking import health_check; health_check()"

ENTRYPOINT ["carbon-tracking"]
CMD ["serve", "--config", "/etc/carbon-tracking/config.yaml"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: carbon-tracking
spec:
  replicas: 2
  selector:
    matchLabels:
      app: carbon-tracking
  template:
    spec:
      containers:
      - name: carbon-tracking
        image: carbon-tracking:1.0.0
        env:
        - name: CARBON_TRACKING_DB_URL
          valueFrom:
            secretKeyRef:
              name: carbon-db
              key: url
```

## Monitoring & Observability

### Metrics Collection

```python
from carbon_tracking import MetricsCollector

collector = MetricsCollector()

# Register custom metrics
collector.register_gauge("total_emissions_tonnes", "Total emissions by scope")
collector.register_counter("calculations_total", "Total emission calculations")
collector.register_histogram("calculation_duration_seconds", "Calculation time")
```

### Audit Trail

```python
from carbon_tracking import AuditTrail

audit = AuditTrail(retention_years=7)

# Every calculation is automatically logged
audit.log(
    operation="scope2_calculation",
    entity="Acme Corp",
    user="analyst@company.com",
    details={"kwh": 8500000, "factor": 0.417}
)

# Query audit trail
logs = audit.query(
    entity="Acme Corp",
    start_date="2025-01-01",
    end_date="2025-12-31"
)
```

## Testing Strategy

```python
import pytest
from carbon_tracking import GHGCalculator, CarbonCreditRegistry

class TestGHGCalculator:
    def test_scope1_calculation(self):
        calc = GHGCalculator(fiscal_year=2025)
        calc.add_scope1(
            category="stationary_combustion",
            source="Natural gas",
            activity_data=50000,
            unit="therms",
            emission_factor=5.301
        )
        report = calc.generate_report()
        assert report.scope1_total_tonnes == pytest.approx(265.05, rel=0.01)

    def test_scope2_dual_report(self):
        calc = GHGCalculator(fiscal_year=2025)
        calc.add_scope2(
            category="purchased_electricity",
            source="US operations",
            activity_data=8500000,
            unit="kWh",
            grid_emission_factor=0.417,
            method="location_based"
        )
        report = calc.generate_report()
        assert report.scope2_total_tonnes > 0

class TestCarbonCreditRegistry:
    def test_purchase_and_retire(self):
        registry = CarbonCreditRegistry()
        registry.purchase(
            credits=1000,
            standard="verra_vcs",
            project="wind_farm",
            vintage=2024,
            price_per_tonne=12.50
        )
        assert registry.balance("verra_vcs") == 1000
        registry.retire(credits=500, standard="verra_vcs", reason="offset")
        assert registry.balance("verra_vcs") == 500
```

## Versioning & Migration

### Semantic Versioning

- **MAJOR**: Breaking changes to API, calculation methodology changes
- **MINOR**: New emission factor sources, new reporting standards
- **PATCH**: Bug fixes, performance improvements

### Migration Guide

```python
# v1.x to v2.x migration
# Old API
calc = GHGCalculator(year=2025)

# New API
calc = GHGCalculator(fiscal_year=2025, reporting_entity="Acme Corp")
```

## Glossary

| Term | Definition |
|------|-----------|
| **GHG Protocol** | Global standard for corporate greenhouse gas accounting |
| **Scope 1** | Direct emissions from owned or controlled sources |
| **Scope 2** | Indirect emissions from purchased electricity, steam, heating, cooling |
| **Scope 3** | All other indirect emissions across 15 value chain categories |
| **SBTi** | Science-Based Targets initiative Ã¢â‚¬â€ validates corporate climate targets |
| **CDP** | Carbon Disclosure Project Ã¢â‚¬â€ environmental disclosure platform |
| **TCFD** | Task Force on Climate-related Financial Disclosures |
| **REC** | Renewable Energy Certificate Ã¢â‚¬â€ proof of renewable electricity generation |
| **tCO2e** | Tonnes of CO2 equivalent Ã¢â‚¬â€ standard unit for GHG emissions |
| **Emission Factor** | Coefficient converting activity data to emissions (kgCO2e/unit) |

## Changelog

### v1.0.0 (2025-01-15)
- Initial release with GHG Protocol implementation
- Scope 1/2/3 emissions calculation
- Carbon credit management
- SBTi target tracking

### v1.1.0 (2025-02-01)
- Added CDP reporting integration
- Improved Scope 3 data quality scoring
- Added multi-entity consolidation

### v1.2.0 (2025-03-01)
- Added Climatiq and Watershed integration
- Performance improvements for large datasets
- Added audit trail functionality

## Contributing Guidelines

1. **Fork the repository** and create a feature branch from `main`
2. **Write tests** for all new functionality with >80% coverage
3. **Follow PEP 8** style guidelines with type hints
4. **Update documentation** for any API changes
5. **Add changelog entries** under `[Unreleased]` section
6. **Submit a pull request** with a clear description of changes

### Code Review Checklist

- [ ] Tests pass and coverage meets threshold
- [ ] Calculation methodology follows GHG Protocol
- [ ] Emission factors are sourced and versioned
- [ ] Audit trail captures all calculations
- [ ] No hardcoded emission factors (use database)

## License

This module is licensed under the Apache License, Version 2.0. See the LICENSE file for full terms.

Copyright 2025 Carbon Tracking Contributors

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills


## Extended Reference

### Configuration Matrix

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| enabled | bool | true | Enable the module |
| log_level | str | INFO | Logging verbosity |
| timeout | int | 30 | Operation timeout in seconds |
| max_retries | int | 3 | Maximum retry attempts |
| cache_ttl | int | 3600 | Cache time-to-live in seconds |
| batch_size | int | 100 | Records per batch |
| parallel_workers | int | 4 | Concurrent worker threads |
| memory_limit | str | 512MB | Maximum memory allocation |
| disk_threshold | float | 0.8 | Disk usage alert threshold |
| health_check_interval | int | 60 | Health check frequency seconds |

### Environment Variables

`ash
MODULE_ENABLED=true
MODULE_LOG_LEVEL=INFO
MODULE_TIMEOUT=30
MODULE_MAX_RETRIES=3
MODULE_CACHE_TTL=3600
MODULE_BATCH_SIZE=100
MODULE_PARALLEL_WORKERS=4
MODULE_MEMORY_LIMIT=512MB
MODULE_DISK_THRESHOLD=0.8
MODULE_HEALTH_CHECK_INTERVAL=60
```n
### Docker Configuration

`yaml
version: '3.8'
services:
  module:
    image: awesome-grok/module:latest
    environment:
      - MODULE_ENABLED=true
      - MODULE_LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
      - ./data:/app/data
    ports:
      - '8080:8080'
    healthcheck:
      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']
      interval: 30s
      timeout: 10s
      retries: 3
```n
### Kubernetes Deployment

`yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: module-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: module
  template:
    metadata:
      labels:
        app: module
    spec:
      containers:
      - name: module
        image: awesome-grok/module:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: 256Mi
            cpu: 250m
          limits:
            memory: 512Mi
            cpu: 500m
```n
### Prometheus Metrics

`yaml
scrape_configs:
  - job_name: 'module'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: /metrics
    scrape_interval: 15s
```n
### Grafana Dashboard

Import dashboard ID 12345 from Grafana.com for pre-configured monitoring panels including request rate, error rate, latency percentiles, and resource utilization.

### Alert Rules

`yaml
groups:
  - name: module-alerts
    rules:
      - alert: HighErrorRate
        expr: rate(module_errors_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High error rate detected
      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(module_request_duration_seconds_bucket[5m])) > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High latency detected
```n
### CI/CD Pipeline

`yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/ -v
      - run: python -m mypy src/
      - run: python -m ruff check src/
```n

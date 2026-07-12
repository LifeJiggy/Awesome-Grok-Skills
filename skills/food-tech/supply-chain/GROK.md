---
name: "supply-chain"
category: "food-tech"
version: "2.0.0"
tags: ["food-tech", "supply-chain", "cold-chain", "logistics", "inventory", "procurement"]
difficulty: "intermediate"
estimated_time: "40-55 minutes"
prerequisites: ["python", "supply-chain-fundamentals"]
---

# Food Supply Chain Management

## Overview

Food supply chain management addresses the unique challenges of perishable goods logistics: temperature-controlled supply chains (cold chain), shelf-life management, demand forecasting for fresh products, supplier quality management, and regulatory compliance for food transport. This module provides tools for end-to-end food supply chain visibility from farm procurement through distribution to retail and food service endpoints.

## Core Capabilities

- **Cold Chain Management**: Real-time temperature monitoring throughout the supply chain with IoT sensor integration and excursion alerting
- **Shelf-Life Tracking**: Dynamic shelf-life prediction based on actual temperature history, not static expiration dates
- **Demand Forecasting**: ML-driven demand prediction for perishable goods considering seasonality, weather, events, and promotional calendars
- **Procurement Optimization**: Supplier selection, contract management, and automated purchasing for raw materials and ingredients
- **Warehouse Management**: Food-grade warehouse operations including FIFO/FEFO enforcement, lot tracking, and quality hold management
- **Route Optimization**: Multi-stop delivery route planning for perishable goods with time window and temperature constraints
- **Inventory Management**: Perishable inventory management with first-expiry-first-out (FEFO) logic and waste reduction analytics
- **Supplier Quality Management**: Supplier scorecards, audit management, and corrective action tracking
- **Cost Analysis**: landed cost calculation including procurement, transport, storage, and waste costs
- **Sustainability Metrics**: Carbon footprint tracking, food waste measurement, and sustainable sourcing analytics

## Usage Examples

### Cold Chain Monitoring

```python
from food_tech.supply_chain import ColdChainManager, TemperatureZone

chain = ColdChainManager(
    alert_channels=["sms", "email", "dashboard"],
    excursion_threshold_minutes=15,
)

# Track a shipment
shipment = chain.create_shipment(
    shipment_id="SHP-2026-07-001",
    product="Fresh Salmon",
    origin="Seattle, WA",
    destination="Chicago, IL",
    temperature_zone=TemperatureZone.FRESH,
    target_range_celsius=(-1, 2),
    estimated_transit_hours=48,
)

# Record temperature readings
chain.record_temperature("SHP-2026-07-001", 1.2, sensor_id="TRAILER-01")
chain.record_temperature("SHP-2026-07-001", 3.5, sensor_id="TRAILER-01")  # Warning

status = chain.get_shipment_status("SHP-2026-07-001")
print(f"Status: {status.current_status}")
print(f"Avg Temp: {status.average_temperature:.1f}C")
print(f"Excursions: {status.excursion_count}")
print(f"Remaining shelf life: {status.projected_shelf_life_hours:.1f} hours")
```

### Demand Forecasting

```python
from food_tech.supply_chain import DemandForecaster

forecaster = DemandForecaster(
    model="prophet",
    granularity="daily",
    include_weather=True,
)

# Generate forecast
forecast = forecaster.predict(
    product_id="SALMON-ATLANTIC-FRESH",
    location="CHICAGO-DC",
    horizon_days=14,
    historical_data="sales_2025.csv",
    special_events=["4th_of_july", "labor_day"],
)

print(f"14-day demand: {forecast.total_units:,} lbs")
for day in forecast.daily_forecast[:7]:
    print(f"  {day.date}: {day.predicted_units:,} lbs "
          f"(range: {day.ci_lower:,}-{day.ci_upper:,})")
```

### Supplier Quality Scorecard

```python
from food_tech.supply_chain import SupplierQualityManager

sqm = SupplierQualityManager()

# Register supplier
supplier = sqm.register_supplier(
    name="Pacific Seafood Co.",
    category="fresh_seafood",
    location="Seattle, WA",
    certifications=["HACCP", "MSC", "SQF"],
)

# Score supplier
scorecard = sqm.score_supplier(
    supplier_id=supplier.supplier_id,
    period="2026-Q2",
    metrics={
        "on_time_delivery": 0.95,
        "quality_rejection_rate": 0.02,
        "food_safety_audit_score": 92,
        "response_time_hours": 4,
        "documentation_accuracy": 0.98,
    },
)

print(f"Supplier: {scorecard.supplier_name}")
print(f"Overall Score: {scorecard.overall_score:.1f}/100")
print(f"Grade: {scorecard.grade}")
for area, s in scorecard.area_scores.items():
    print(f"  {area}: {s:.1f}/100")
```

## Best Practices

- Implement FEFO (First Expired First Out) rather than FIFO for perishable inventory management
- Use dynamic shelf-life models based on actual time-temperature history rather than static date codes
- Monitor cold chain continuously; a 15-minute temperature excursion can reduce shelf life by 30%+
- Maintain supplier diversification; no single supplier should represent >40% of critical ingredient supply
- Forecast demand at the SKU-location-day level for perishables to minimize waste and stockouts
- Track food waste metrics (shrink rate) by category and implement waste reduction programs
- Conduct mock recall exercises quarterly to validate traceability system effectiveness
- Use landed cost analysis including waste to make true cost-of-goods decisions
- Negotiate vendor-managed inventory (VMI) agreements for high-volume staple items
- Implement automated reorder points based on lead time variability, not just average lead time

## Related Modules

- `food-tech/food-safety` - HACCP, temperature compliance, and traceability
- `food-tech/agriculture-data` - Farm-level data for procurement
- `food-tech/restaurant-tech` - Restaurant supply chain operations
- `food-tech/nutrition-analysis` - Product composition for procurement decisions

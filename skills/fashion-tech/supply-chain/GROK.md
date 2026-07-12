---
name: "supply-chain"
category: "fashion-tech"
version: "2.0.0"
tags: ["fashion-tech", "supply-chain", "logistics", "inventory-management", "demand-forecasting"]
difficulty: "advanced"
estimated_time: "45-60 minutes"
prerequisites: ["python", "supply-chain-fundamentals"]
---

# Fashion Supply Chain Management

## Overview

Fashion supply chain management encompasses the end-to-end coordination of raw material sourcing, manufacturing, logistics, inventory management, and retail distribution for apparel and accessories. This module provides tools for demand forecasting, inventory optimization, supplier management, production scheduling, and logistics tracking tailored to the unique challenges of fashion: short product lifecycles, seasonal collections, size/color SKU proliferation, and high return rates.

The system addresses critical fashion industry pain points including overproduction (30% of garments produced are never sold), lead time compression (fast fashion demands 2-4 week cycles), multi-tier supplier visibility, sustainable sourcing compliance, and real-time inventory allocation across channels.

## Core Capabilities

- **Demand Forecasting**: ML-driven demand prediction using historical sales, trend signals, weather data, and marketing calendar for accurate buy planning
- **Inventory Optimization**: Multi-echelon inventory optimization across warehouses, stores, and fulfillment centers with size curve optimization
- **Supplier Management**: Supplier scoring, compliance tracking, audit management, and risk assessment across multi-tier supply networks
- **Production Scheduling**: Capacity planning, production line optimization, and cut-make-trim (CMT) workflow management
- **Logistics Tracking**: End-to-end shipment visibility with predictive ETAs, carrier performance scoring, and exception management
- **Size Curve Optimization**: Statistical sizing ratio optimization by style, region, and channel to minimize markdowns from size imbalances
- **Returns Prediction**: Predict return rates by style, size, and customer segment to improve net demand accuracy
- **Sustainability Tracking**: Carbon footprint calculation per garment, recycled material tracking, and ESG compliance reporting
- **Allocation & Replenishment**: Automated store allocation based on local demand signals and automatic replenishment triggers
- **Multi-Channel Sync**: Real-time inventory synchronization across DTC, wholesale, marketplace, and pop-up channels

## Usage Examples

### Demand Forecasting

```python
from fashion_tech.supply_chain import DemandForecaster, ForecastGranularity

forecaster = DemandForecaster(
    model="gradient_boosting",
    granularity=ForecastGranularity.WEEKLY,
    lookback_weeks=52,
)

# Generate demand forecast for upcoming season
forecast = forecaster.predict(
    sku="DRESS-RED-S-M",
    features={
        "trend_score": 0.82,
        "price_point": 89.99,
        "marketing_spend": 15000,
        "season": "SS26",
        "weather_forecast": "warm",
        "competitor_avg_price": 95.00,
    },
    horizon_weeks=16,
)

print(f"Total demand: {forecast.total_units:,}")
print(f"Weekly curve: {forecast.weekly_units}")
print(f"Confidence: {forecast.confidence:.1%}")
print(f"Recommended buy: {forecast.recommended_order_quantity}")
```

### Inventory Optimization

```python
from fashion_tech.supply_chain import InventoryOptimizer, Facility

optimizer = InventoryOptimizer(
    facilities=[
        Facility("DC_EAST", type="warehouse", capacity=50000),
        Facility("DC_WEST", type="warehouse", capacity=40000),
        Facility("STORE_NYC", type="store", capacity=500),
        Facility("STORE_LA", type="store", capacity=400),
    ],
    service_level_target=0.95,
)

# Optimize inventory allocation
allocation = optimizer.optimize(
    sku="SHIRT-BLU-L",
    total_inventory=12000,
    demand_by_facility={
        "DC_EAST": 4000, "DC_WEST": 3000,
        "STORE_NYC": 800, "STORE_LA": 600,
    },
)

for facility, units in allocation.allocations.items():
    print(f"  {facility}: {units} units")
print(f"  Safety stock: {allocation.safety_stock}")
print(f"  Expected fill rate: {allocation.projected_fill_rate:.1%}")
```

### Supplier Risk Assessment

```python
from fashion_tech.supply_chain import SupplierManager, SupplierTier

manager = SupplierManager()

# Register suppliers
supplier = manager.register(
    name="Textile Mills Co.",
    tier=SupplierTier.TIER_1,
    location="Ho Chi Minh City, Vietnam",
    certifications=["OEKO-TEX", "BSCI", "WRAP"],
    lead_time_days=45,
    capacity_units_monthly=100000,
)

# Run risk assessment
risk = manager.assess_risk(supplier.id)
print(f"Overall risk score: {risk.overall_score}/100")
print(f"  Quality: {risk.quality_score}")
print(f"  Delivery: {risk.delivery_score}")
print(f"  Compliance: {risk.compliance_score}")
print(f"  Financial: {risk.financial_score}")
for alert in risk.alerts:
    print(f"  ALERT: {alert}")
```

### Production Scheduling

```python
from fashion_tech.supply_chain import ProductionScheduler, ProductionLine

scheduler = ProductionScheduler(
    lines=[
        ProductionLine("LINE_A", capacity=5000, specialty="woven"),
        ProductionLine("LINE_B", capacity=8000, specialty="knit"),
    ],
)

# Schedule production orders
schedule = scheduler.schedule(
    orders=[
        {"sku": "DRESS-001", "quantity": 3000, "priority": "high", "deadline": "2026-03-15"},
        {"sku": "SHIRT-042", "quantity": 5000, "priority": "medium", "deadline": "2026-03-20"},
        {"sku": "PANTS-018", "quantity": 4000, "priority": "high", "deadline": "2026-03-18"},
    ],
)

for line, orders in schedule.allocations.items():
    print(f"\n{line}:")
    for order in orders:
        print(f"  {order.sku}: {order.quantity} units, start={order.start_date}, "
              f"end={order.end_date}, priority={order.priority}")
```

## Architecture

```
Data Sources
├── POS / E-commerce Sales
├── Weather APIs
├── Marketing Calendar
├── Trend Signals (from trend-prediction module)
└── Supplier Portals
         │
         ▼
┌─────────────────────┐
│  Demand Planning     │──→ Buy Recommendations
│  (ML Forecasting)    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Supply Planning     │──→ Production Orders
│  (MRP / Capacity)    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Execution           │──→ Shipment Tracking
│  (Logistics / WMS)   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Allocation          │──→ Store / Channel Assignments
│  (Replenishment)     │
└─────────────────────┘
```

## Best Practices

- Build demand forecasts at SKU-color-size level, not just style level, to avoid stockouts in popular size/color combinations
- Maintain safety stock buffers proportional to supplier lead time uncertainty and demand variability
- Diversify supplier base across geographies to mitigate geopolitical, weather, and pandemic risks
- Track supplier performance metrics (OTIF, defect rate, lead time variance) monthly and review quarterly
- Implement allocation rules that consider local preferences (e.g., darker colors in colder climates)
- Use ABC analysis to prioritize inventory management effort on high-value/high-velocity SKUs
- Plan for markdown optimization by aligning production quantities with forecasted demand ranges
- Integrate sustainability metrics into sourcing decisions alongside cost and quality
- Set up automated alerts for demand forecast deviations exceeding 20% from plan
- Reconcile inventory across channels at least daily to prevent overselling

## Related Modules

- `fashion-tech/trend-prediction` - Feed trend signals into demand forecasting
- `fashion-tech/retail-analytics` - Validate supply plans against retail performance
- `fashion-tech/sustainable-fashion` - Sustainable sourcing compliance and tracking

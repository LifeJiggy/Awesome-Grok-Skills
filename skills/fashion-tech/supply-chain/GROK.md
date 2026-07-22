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

---

## Advanced Configuration

### Demand Forecasting Settings

```python
from supply_chain import ForecastConfig

forecast_config = ForecastConfig(
    # Model Selection
    models={
        "short_term": {"algorithm": "prophet", "horizon_days": 30},
        "medium_term": {"algorithm": "xgboost", "horizon_days": 90},
        "long_term": {"algorithm": "lstm", "horizon_days": 365},
    },
    
    # Features
    features=[
        "historical_sales",
        "trend_signals",
        "weather",
        "promotions",
        "competitor_pricing",
    ],
    
    # Ensemble
    ensemble={
        "method": "weighted_average",
        "weights": {"short_term": 0.5, "medium_term": 0.3, "long_term": 0.2},
    },
)
```

### Inventory Optimization Settings

```python
from supply_chain import InventoryConfig

inventory_config = InventoryConfig(
    # Reorder Points
    reorder={
        "method": "eoq",  # eoq, min_max, dynamic
        "service_level": 0.95,
        "lead_time_buffer_days": 7,
    },
    
    # Safety Stock
    safety_stock={
        "method": "statistical",  # statistical, heuristic
        "z_score": 1.65,  # 95% service level
        "demand_variability": True,
        "lead_time_variability": True,
    },
    
    # Allocation
    allocation={
        "method": "demand_based",  # equal, demand_based, priority
        "channel_priority": {"ecommerce": 1, "stores": 2, "wholesale": 3},
    },
)
```

## Architecture Patterns

### Supply Chain Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Planning Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Demand   │  │ Supply   │  │ S&OP     │         │
│  │ Forecast │  │ Planning │  │ Process  │         │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘         │
└───────┼──────────────┼──────────────┼───────────────┘
        │              │              │
        ▼              ▼              ▼
┌─────────────────────────────────────────────────────┐
│              Execution Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │Procurement│ │Production│  │Logistics │         │
│  │          │  │          │  │          │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              Visibility Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │Tracking  │  │Analytics │  │Alerts    │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────┘
```

### Supplier Management

```python
from supply_chain import SupplierManager

supplier_mgr = SupplierManager()

# Register supplier
supplier = supplier_mgr.register(
    name="Fabric Mill Co",
    location="Turkey",
    capabilities=["woven", "knit", "denim"],
    certifications=["OEKO-TEX", "GOTS"],
    lead_time_days=21,
)

# Score supplier
score = supplier_mgr.score(
    supplier_id=supplier.id,
    metrics={
        "on_time_delivery": 0.92,
        "quality_rate": 0.98,
        "cost_competitiveness": 0.85,
        "sustainability": 0.78,
    },
)

print(f"Supplier score: {score.total:.2f}")
print(f"Grade: {score.grade}")
```

## Integration Guide

### ERP Integration

```python
from supply_chain import ERPIntegration

erp = ERPIntegration()

# Connect to ERP
erp.configure(
    system="sap",
    connection="sap://host:443",
    modules=["mm", "pp", "sd"],
)

# Sync inventory
inventory = erp.sync_inventory(
    warehouses=["WH01", "WH02", "WH03"],
)

print(f"Total SKUs: {inventory.total_skus}")
print(f"Total units: {inventory.total_units:,}")
```

### Logistics Integration

```python
from supply_chain import LogisticsIntegration

logistics = LogisticsIntegration()

# Connect to 3PL
logistics.configure(
    provider="fedex",
    api_key="your-api-key",
    account="account-123",
)

# Track shipment
tracking = logistics.track(
    tracking_number="1234567890",
)

print(f"Status: {tracking.status}")
print(f"Location: {tracking.current_location}")
print(f"ETA: {tracking.eta}")
```

## Performance Optimization

### Forecast Optimization

```python
from supply_chain import ForecastOptimizer

optimizer = ForecastOptimizer()

# Optimize forecast
result = optimizer.optimize(
    sku="SKU-123",
    strategies=[
        "feature_engineering",
        "hyperparameter_tuning",
        "ensemble_optimization",
    ],
)

print(f"MAPE improvement: {result.improvement:.1%}")
print(f"Best model: {result.best_model}")
```

### Inventory Optimization

```python
from supply_chain import InventoryOptimizer

inv_opt = InventoryOptimizer()

# Optimize inventory levels
result = inv_opt.optimize(
    warehouse="WH01",
    constraints={
        "budget": 1000000,
        "space_sqft": 50000,
        "service_level": 0.95,
    },
)

print(f"Optimized SKUs: {result.sku_count}")
print(f"Expected service level: {result.service_level:.1%}")
print(f"Inventory reduction: {result.reduction:.1%}")
```

## Security Considerations

### Data Security

```python
from supply_chain import DataSecurity

security = DataSecurity()

# Encrypt sensitive data
security.encrypt(
    tables=["suppliers", "contracts", "pricing"],
    algorithm="aes-256",
)

# Access control
security.define_permissions(
    role="buyer",
    permissions=[
        "suppliers.read",
        "purchase_orders.create",
    ],
)
```

### Audit Trail

```python
from supply_chain import AuditTrail

audit = AuditTrail()

# Log changes
audit.log(
    user="buyer@company.com",
    action="create_purchase_order",
    entity="purchase_order",
    entity_id="po-123",
    details={"supplier": "Fabric Mill Co", "amount": 50000},
)
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Forecast inaccuracy | Missing signals | Add more features, diversify sources |
| Stockouts | Poor safety stock | Increase buffer, improve forecasting |
| Overstock | Conservative ordering | Implement dynamic allocation |
| Supplier delays | Poor visibility | Track performance, diversify |
| High returns | Size issues | Improve size charts, add VTO |

### Debug Mode

```python
from supply_chain import enable_debug

enable_debug(
    components=["forecast", "inventory", "logistics"],
    log_level="DEBUG",
)

# Debug forecast
debug_session = debug.trace_forecast("SKU-123")
print(f"Debug report: {debug_session.report_url}")
```

## API Reference

### REST Endpoints

```
GET    /api/v1/supply/inventory              Get inventory
POST   /api/v1/supply/inventory/allocate     Allocate inventory
GET    /api/v1/supply/forecast/{sku}         Get forecast
POST   /api/v1/supply/forecast/generate      Generate forecast
GET    /api/v1/supply/suppliers              List suppliers
POST   /api/v1/supply/purchase-orders        Create PO
GET    /api/v1/supply/shipments              List shipments
GET    /api/v1/supply/shipments/{id}/track   Track shipment
```

### Data Models

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID

@dataclass
class Inventory:
    sku: str
    warehouse: str
    quantity: int
    reserved: int
    available: int
    reorder_point: int
    last_updated: datetime

@dataclass
class Supplier:
    supplier_id: UUID
    name: str
    location: str
    capabilities: List[str]
    score: float
    status: str

@dataclass
class PurchaseOrder:
    po_id: UUID
    supplier_id: UUID
    items: List["POItem"]
    total: float
    status: str
    expected_date: datetime

@dataclass
class Shipment:
    shipment_id: UUID
    carrier: str
    tracking_number: str
    status: str
    origin: str
    destination: str
    eta: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: supply-chain
spec:
  replicas: 3
  selector:
    matchLabels:
      app: supply-chain
  template:
    spec:
      containers:
      - name: api
        image: supply-chain:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
```

## Monitoring & Observability

### Key Metrics

```python
from supply_chain import Metrics

metrics = Metrics()

# Track inventory
metrics.gauge("inventory.units", units, tags={"warehouse": "WH01"})
metrics.gauge("inventory.turnover", turnover, tags={"category": "apparel"})

# Track forecasts
metrics.gauge("forecast.mape", mape, tags={"sku": "SKU-123"})
metrics.counter("forecast.updates_total")
```

## Testing Strategy

### Unit Tests

```python
import pytest
from supply_chain import DemandForecaster

@pytest.fixture
def forecaster():
    return DemandForecaster(test_mode=True)

def test_forecast(forecaster):
    forecast = forecaster.forecast(
        sku="SKU-123",
        horizon_days=30,
    )
    assert len(forecast.predictions) == 30
    assert all(p > 0 for p in forecast.predictions)
```

## Versioning & Migration

### Version History

- **2.0.0**: Added ML forecasting, real-time tracking, advanced optimization
- **1.5.0**: Added supplier management, inventory optimization
- **1.0.0**: Initial release with basic inventory management

## Glossary

| Term | Definition |
|------|------------|
| **EOQ** | Economic Order Quantity |
| **OTIF** | On-Time In-Full delivery |
| **S&OP** | Sales and Operations Planning |
| **MAPE** | Mean Absolute Percentage Error |
| **Safety Stock** | Buffer inventory for variability |
| **SKU** | Stock Keeping Unit |

## Changelog

### Version 2.0.0
- ML-powered demand forecasting
- Real-time shipment tracking
- Advanced inventory optimization
- Supplier scorecards

### Version 1.5.0
- Supplier management
- Basic inventory optimization
- Purchase order automation

### Version 1.0.0
- Initial release
- Basic inventory tracking
- Simple reorder points

## Contributing Guidelines

1. Test with realistic fashion data
2. Validate forecast accuracy
3. Benchmark optimization algorithms
4. Document business rules

## Multi-Echelon Inventory Optimization

### Safety Stock Calculation

```python
from supply_chain import SafetyStockCalculator

calculator = SafetyStockCalculator()

# Calculate safety stock
safety_stock = calculator.calculate(
    sku="SHIRT-BLU-L",
    demand_mean=100,
    demand_std=20,
    lead_time_mean=14,
    lead_time_std=3,
    service_level=0.95,
)

print(f"Safety Stock: {safety_stock.units} units")
print(f"Reorder Point: {safety_stock.reorder_point} units")
print(f"Service Level: {safety_stock.service_level:.1%}")
```

### ABC Analysis

```python
from supply_chain import ABCAnalyzer

analyzer = ABCAnalyzer()

# Perform ABC analysis
analysis = analyzer.analyze(
    inventory_data="inventory_snapshot.csv",
    criteria="revenue_contribution",
)

print(f"ABC Analysis:")
print(f"  A Items: {analysis.a_count} ({analysis.a_percentage:.1%} of items, {analysis.a_revenue:.1%} of revenue)")
print(f"  B Items: {analysis.b_count} ({analysis.b_percentage:.1%} of items, {analysis.b_revenue:.1%} of revenue)")
print(f"  C Items: {analysis.c_count} ({analysis.c_percentage:.1%} of items, {analysis.c_revenue:.1%} of revenue)")
```

## Fashion Supply Chain Deep Dive

### Production Planning Optimizer

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class ProductionOrder:
    order_id: str
    sku_id: str
    quantity: int
    fabric_type: str
    color: str
    size_distribution: Dict[str, float]  # size -> proportion
    priority: int  # 1=highest
    due_date: str
    factory_id: str
    
class ProductionScheduler:
    def __init__(self):
        self.factories: Dict[str, Dict] = {}
        self.orders: List[ProductionOrder] = []
        self.fabric_inventory: Dict[str, float] = {}
    
    def register_factory(self, factory_id: str, capacity_units: int,
                        lead_time_days: int, quality_score: float):
        self.factories[factory_id] = {
            "capacity": capacity_units, "lead_time": lead_time_days,
            "quality": quality_score, "current_load": 0,
        }
    
    def schedule_orders(self) -> List[Dict]:
        sorted_orders = sorted(self.orders, key=lambda o: (o.priority, o.due_date))
        schedule = []
        
        for order in sorted_orders:
            best_factory = self._find_best_factory(order)
            if best_factory:
                fabric_available = self.fabric_inventory.get(order.fabric_type, 0)
                units_needed = order.quantity * 1.1  # 10% waste allowance
                
                if fabric_available >= units_needed:
                    self.fabric_inventory[order.fabric_type] -= units_needed
                    self.factories[best_factory]["current_load"] += order.quantity
                    
                    schedule.append({
                        "order_id": order.order_id,
                        "factory": best_factory,
                        "start_date": self._calc_start(best_factory, order.due_date),
                        "end_date": order.due_date,
                        "quantity": order.quantity,
                        "fabric_required": round(units_needed, 1),
                        "sizes": {s: int(order.quantity * p) 
                                 for s, p in order.size_distribution.items()},
                    })
        
        return schedule
    
    def _find_best_factory(self, order: ProductionOrder) -> Optional[str]:
        best = None
        best_score = -1
        for fid, fdata in self.factories.items():
            remaining_capacity = fdata["capacity"] - fdata["current_load"]
            if remaining_capacity < order.quantity:
                continue
            score = fdata["quality"] * (1 - fdata["current_load"] / fdata["capacity"])
            if score > best_score:
                best_score = score
                best = fid
        return best
    
    def _calc_start(self, factory_id: str, due_date: str) -> str:
        lead = self.factories[factory_id]["lead_time"]
        from datetime import datetime, timedelta
        due = datetime.strptime(due_date, "%Y-%m-%d")
        start = due - timedelta(days=lead)
        return start.strftime("%Y-%m-%d")

class FabricYieldOptimizer:
    def __init__(self):
        self.marker_efficiencies: Dict[str, float] = {}
    
    def optimize_marker(self, fabric_width_cm: float, pieces: List[Dict]) -> Dict:
        total_fabric_length = 0
        placed_pieces = []
        
        # Simple greedy bin-packing
        sorted_pieces = sorted(pieces, key=lambda p: p.get("area", 0), reverse=True)
        remaining_width = fabric_width_cm
        
        for piece in sorted_pieces:
            piece_width = piece.get("width_cm", 30)
            if piece_width <= remaining_width:
                placed_pieces.append({
                    "piece_id": piece.get("id"),
                    "width_cm": piece_width,
                    "length_cm": piece.get("length_cm", 40),
                    "position": {"x": fabric_width_cm - remaining_width, "y": total_fabric_length},
                })
                remaining_width -= piece_width
            else:
                total_fabric_length += max(p.get("length_cm", 40) for p in placed_pieces[-3:])
                remaining_width = fabric_width_cm
                placed_pieces.append({
                    "piece_id": piece.get("id"),
                    "width_cm": piece_width,
                    "length_cm": piece.get("length_cm", 40),
                    "position": {"x": 0, "y": total_fabric_length},
                })
                remaining_width -= piece_width
        
        total_fabric_area = fabric_width_cm * (total_fabric_length + 40)
        pieces_area = sum(p.get("area", p.get("width_cm", 30) * p.get("length_cm", 40)) for p in pieces)
        efficiency = pieces_area / total_fabric_area if total_fabric_area > 0 else 0
        
        return {
            "efficiency": round(efficiency, 3),
            "fabric_length_cm": round(total_fabric_length + 40),
            "fabric_area_cm2": round(total_fabric_area),
            "pieces_placed": len(placed_pieces),
            "waste_pct": round((1 - efficiency) * 100, 1),
            "layout": placed_pieces,
        }

class QualityInspectionPipeline:
    def __init__(self):
        self.inspection_criteria = {
            "stitching": {"tolerance_mm": 2, "weight": 0.25},
            "color_match": {"delta_e_max": 3.0, "weight": 0.20},
            "fabric_defects": {"max_per_garment": 2, "weight": 0.25},
            "measurement_accuracy": {"tolerance_cm": 1.5, "weight": 0.20},
            "finishing": {"checklist_items": 8, "weight": 0.10},
        }
    
    def inspect_garment(self, garment_id: str, measurements: Dict, 
                       visual_inspection: Dict) -> Dict:
        scores = {}
        
        # Stitching check
        stitch_issues = measurements.get("stitching_deviation_mm", 0)
        scores["stitching"] = max(0, 1 - stitch_issues / self.inspection_criteria["stitching"]["tolerance_mm"])
        
        # Color match
        delta_e = visual_inspection.get("color_delta_e", 0)
        scores["color_match"] = max(0, 1 - delta_e / self.inspection_criteria["color_match"]["delta_e_max"])
        
        # Fabric defects
        defect_count = visual_inspection.get("defect_count", 0)
        max_defects = self.inspection_criteria["fabric_defects"]["max_per_garment"]
        scores["fabric_defects"] = max(0, 1 - defect_count / max_defects)
        
        # Measurement accuracy
        max_deviation = max(measurements.get("deviation_cm", {}).values()) if measurements.get("deviation_cm") else 0
        scores["measurement_accuracy"] = max(0, 1 - max_deviation / self.inspection_criteria["measurement_accuracy"]["tolerance_cm"])
        
        # Finishing
        checklist_passed = visual_inspection.get("finishing_checklist_passed", 0)
        total_checks = self.inspection_criteria["finishing"]["checklist_items"]
        scores["finishing"] = checklist_passed / total_checks
        
        weighted_score = sum(
            scores[k] * self.inspection_criteria[k]["weight"] 
            for k in scores
        )
        
        grade = "A" if weighted_score >= 0.95 else "B" if weighted_score >= 0.85 else "C" if weighted_score >= 0.70 else "D"
        
        return {
            "garment_id": garment_id,
            "overall_score": round(weighted_score, 3),
            "grade": grade,
            "dimension_scores": {k: round(v, 3) for k, v in scores.items()},
            "passed": grade in ["A", "B"],
            "issues": self._identify_issues(scores),
        }
    
    def _identify_issues(self, scores: Dict) -> List[str]:
        issues = []
        thresholds = {"stitching": 0.7, "color_match": 0.6, "fabric_defects": 0.5,
                     "measurement_accuracy": 0.7, "finishing": 0.8}
        for dim, threshold in thresholds.items():
            if scores.get(dim, 1) < threshold:
                issues.append(f"{dim} below quality threshold")
        return issues
```

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills

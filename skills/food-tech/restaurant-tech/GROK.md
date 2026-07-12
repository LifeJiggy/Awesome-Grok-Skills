---
name: "restaurant-tech"
category: "food-tech"
version: "2.0.0"
tags: ["food-tech", "restaurant-tech", "pos", "menu-engineering", "kitchen-management", "food-service"]
difficulty: "intermediate"
estimated_time: "35-50 minutes"
prerequisites: ["python", "restaurant-operations"]
---

# Restaurant Technology

## Overview

Restaurant technology encompasses the software systems powering modern food service operations: point-of-sale (POS) systems, kitchen display systems (KDS), menu engineering, online ordering, reservation management, inventory control, staff scheduling, and customer relationship management. This module provides a comprehensive framework for digitizing restaurant operations to improve efficiency, reduce waste, and enhance customer experience.

## Core Capabilities

- **POS Integration**: Modern cloud POS with order management, payment processing, split bills, and multi-location support
- **Menu Engineering**: Data-driven menu optimization using profitability matrix (profit vs popularity) and item performance analytics
- **Kitchen Display Systems**: Real-time order routing, preparation timing, and kitchen workflow optimization
- **Online Ordering**: Direct ordering platform with delivery zone management, order throttling, and integration with third-party aggregators
- **Reservation Management**: Table allocation, waitlist management, no-show prediction, and reservation-based CRM
- **Inventory Control**: Real-time ingredient tracking, par level management, waste logging, and automated purchasing suggestions
- **Staff Scheduling**: Labor cost optimization with demand-based scheduling, shift swapping, and overtime alerts
- **Customer Analytics**: Visit frequency, average check, menu preferences, and loyalty program management
- **Performance Dashboards**: Real-time KPIs including covers, average check, food cost %, labor cost %, and table turn time
- **Multi-Location Management**: Centralized reporting, menu management, and operational control across restaurant groups

## Usage Examples

### Menu Engineering Analysis

```python
from food_tech.restaurant_tech import MenuEngine, MenuCategory

engine = MenuEngine(
    analysis_period_days=90,
    cost_data_source="recipe_costs",
)

# Analyze menu performance
analysis = engine.analyze_menu(
    menu_items=[
        {"name": "Grilled Salmon", "price": 28.00, "cost": 8.40, "sold": 1200, "category": "entree"},
        {"name": "Caesar Salad", "price": 14.00, "cost": 3.50, "sold": 1800, "category": "starter"},
        {"name": "Filet Mignon", "price": 42.00, "cost": 16.80, "sold": 600, "category": "entree"},
        {"name": "Pasta Carbonara", "price": 18.00, "cost": 4.50, "sold": 950, "category": "entree"},
    ],
)

for item in analysis.items:
    quadrant = item.profitability_quadrant
    print(f"  {item.name}: {quadrant} "
          f"(profit=${item.profit_per_plate:.2f}, popularity={item.popularity_score:.0%})")
    if quadrant == "star":
        print(f"    -> Promote heavily, maintain quality")
    elif quadrant == "plowhorse":
        print(f"    -> Increase price or reduce cost")
    elif quadrant == "puzzle":
        print(f"    -> Improve marketing visibility")
    elif quadrant == "dog":
        print(f"    -> Consider removing from menu")
```

### Online Order Management

```python
from food_tech.restaurant_tech import OnlineOrdering, OrderSource

ordering = OnlineOrdering(
    restaurant_id="REST-001",
    delivery_zones=[
        {"name": "Zone A", "radius_km": 3, "delivery_fee": 3.99},
        {"name": "Zone B", "radius_km": 5, "delivery_fee": 5.99},
    ],
    max_concurrent_orders=25,
)

# Process incoming order
order = ordering.create_order(
    source=OrderSource.WEBSITE,
    items=[
        {"item_id": "SALMON", "quantity": 2, "customizations": {"side": "quinoa"}},
        {"item_id": "CAESAR", "quantity": 1, "customizations": {"dressing": "on_side"}},
    ],
    customer={"name": "Jane D.", "phone": "555-0123", "address": "123 Main St"},
    delivery_zone="Zone A",
)

print(f"Order: {order.order_id}")
print(f"Total: ${order.total:.2f}")
print(f"Est. delivery: {order.estimated_delivery_time}")
print(f"Kitchen ticket: {order.kitchen_ticket_id}")
```

### Reservation & Table Management

```python
from food_tech.restaurant_tech import ReservationSystem, TableConfig

system = ReservationSystem(
    tables=[
        TableConfig("T1", capacity=2, zone="patio"),
        TableConfig("T2", capacity=4, zone="main"),
        TableConfig("T3", capacity=4, zone="main"),
        TableConfig("T4", capacity=6, zone="private"),
        TableConfig("T5", capacity=8, zone="private"),
    ],
    reservation_duration_minutes=90,
    no_show_timeout_minutes=15,
)

# Make reservation
reservation = system.reserve(
    customer_name="John Smith",
    party_size=4,
    date_time="2026-07-15 19:00",
    preferences={"zone": "main", "occasion": "birthday"},
)

print(f"Reservation: {reservation.reservation_id}")
print(f"Table: {reservation.table_id}")
print(f"Confirmation: {reservation.confirmation_code}")

# Check availability
availability = system.check_availability(
    party_size=2, date_time="2026-07-15 20:00",
)
print(f"Tables available: {len(availability.tables)}")
```

### Performance Dashboard

```python
from food_tech.restaurant_tech import PerformanceDashboard

dashboard = PerformanceDashboard(restaurant_id="REST-001")

# Get real-time metrics
metrics = dashboard.get_realtime_metrics()
print(f"Today's Performance:")
print(f"  Covers: {metrics.covers}")
print(f"  Revenue: ${metrics.revenue:,.2f}")
print(f"  Avg Check: ${metrics.average_check:.2f}")
print(f"  Food Cost: {metrics.food_cost_pct:.1%}")
print(f"  Labor Cost: {metrics.labor_cost_pct:.1%}")
print(f"  Table Turn: {metrics.table_turn_time:.1f} min")
```

## Best Practices

- Use menu engineering quarterly analysis to keep the menu optimized; rotate seasonal items strategically
- Track food cost percentage by item, not just overall, to identify items dragging down margins
- Implement recipe-level costing with actual supplier prices updated monthly for accurate margins
- Use demand forecasting to schedule labor; understaffing during rush hurts service more than overstaffing costs
- Monitor online order throttling during peak hours to maintain kitchen capacity and food quality
- Track no-show rates and implement cancellation policies for high-demand time slots
- Log all waste with reason codes (overproduction, spoilage, mistake) for actionable waste reduction
- Train staff on upselling and suggestive selling techniques; track server-level revenue per cover
- Integrate POS, KDS, and inventory for real-time food cost tracking, not just end-of-month reconciliation
- Maintain separate dashboards for FOH (front of house) and BOH (back of house) operations

## Related Modules

- `food-tech/food-safety` - Kitchen food safety and temperature compliance
- `food-tech/nutrition-analysis` - Menu nutrition labeling and allergen management
- `food-tech/supply-chain` - Restaurant procurement and supplier management

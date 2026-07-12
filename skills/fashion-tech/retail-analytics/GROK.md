---
name: "retail-analytics"
category: "fashion-tech"
version: "2.0.0"
tags: ["fashion-tech", "retail-analytics", "business-intelligence", "data-analytics", "customer-insights"]
difficulty: "intermediate"
estimated_time: "35-50 minutes"
prerequisites: ["python", "sql-basics", "statistics-fundamentals"]
---

# Fashion Retail Analytics

## Overview

Fashion retail analytics provides data-driven insights into customer behavior, product performance, store operations, and omnichannel revenue optimization. This module covers sales analytics, customer segmentation, basket analysis, markdown optimization, visual merchandising analytics, and real-time dashboarding tailored to the unique dynamics of fashion retail: seasonality, size curves, rapid style obsolescence, and multi-channel complexity.

The system processes POS transactions, e-commerce clickstreams, loyalty program data, foot traffic signals, and inventory positions to deliver actionable insights that drive revenue growth, margin improvement, and customer lifetime value optimization.

## Core Capabilities

- **Sales Performance Analytics**: Real-time and historical sales tracking with drill-down by store, region, category, style, color, size, and channel
- **Customer Segmentation**: RFM analysis, behavioral clustering, and predictive customer lifetime value (CLV) modeling
- **Basket Analysis**: Market basket analysis and cross-sell/upsell recommendation engines using association rules and collaborative filtering
- **Markdown Optimization**: Data-driven markdown timing and depth optimization to maximize revenue while clearing seasonal inventory
- **Size Curve Analytics**: Sell-through analysis by size to identify lost sales from size imbalances and optimize future buys
- **Visual Merchandising**: Planogram compliance tracking, window display performance measurement, and in-store traffic flow analysis
- **Omnichannel Attribution**: Multi-touch attribution modeling across stores, web, mobile, social, and marketplace channels
- **Price Elasticity**: Demand response modeling to price changes across products, channels, and customer segments
- **Sell-Through Rate Analysis**: Real-time tracking of sell-through vs. plan by style with automated alerts for slow/fast movers
- **Competitive Intelligence**: Price monitoring, assortment tracking, and promotional activity tracking across competitors

## Usage Examples

### Sales Performance Dashboard

```python
from fashion_tech.retail_analytics import SalesAnalytics, TimeGranularity

analytics = SalesAnalytics(
    data_source="pos_and_ecommerce",
    refresh_interval_minutes=15,
)

# Get sales summary
summary = analytics.get_sales_summary(
    period="current_week",
    compare_to="last_year",
    dimensions=["region", "channel", "category"],
)

print(f"Total Revenue: ${summary.total_revenue:,.2f}")
print(f"YoY Change: {summary.yoy_change:+.1%}")
print(f"Units Sold: {summary.total_units:,}")
print(f"Average Transaction: ${summary.avg_transaction:.2f}")

# Drill into top/bottom performers
for store in summary.top_performers[:5]:
    print(f"  TOP: {store.name} - ${store.revenue:,.0f} ({store.change:+.1%})")
for store in summary.bottom_performers[:5]:
    print(f"  BOT: {store.name} - ${store.revenue:,.0f} ({store.change:+.1%})")
```

### Customer Segmentation

```python
from fashion_tech.retail_analytics import CustomerSegmenter, SegmentMethod

segmenter = CustomerSegmenter(method=SegmentMethod.RFM_CLUSTERING)

# Segment customer base
segments = segmenter.segment(
    customer_data="loyalty_transactions.csv",
    n_segments=5,
    recency_window_days=365,
)

for seg in segments:
    print(f"\nSegment: {seg.name} ({seg.size:,} customers)")
    print(f"  Avg CLV: ${seg.avg_clv:,.2f}")
    print(f"  Avg Frequency: {seg.avg_frequency:.1f} visits/year")
    print(f"  Avg Basket: ${seg.avg_basket:.2f}")
    print(f"  Preferred Category: {seg.top_category}")
    print(f"  Churn Risk: {seg.churn_probability:.1%}")

# Generate personalized recommendations
for seg in segments[:2]:
    recs = segmenter.generate_recommendations(seg)
    print(f"\n  Recommendations for {seg.name}:")
    for rec in recs:
        print(f"    - {rec}")
```

### Basket Analysis & Cross-Sell

```python
from fashion_tech.retail_analytics import BasketAnalyzer

analyzer = BasketAnalyzer(
    min_support=0.01,
    min_confidence=0.3,
)

# Analyze purchase patterns
rules = analyzer.find_rules(
    transaction_data="transactions_2025.csv",
    min_lift=1.5,
)

# Show top cross-sell opportunities
for rule in rules[:10]:
    print(f"  {rule.antecedent} → {rule.consequent}")
    print(f"    Support: {rule.support:.1%}, Confidence: {rule.confidence:.1%}, Lift: {rule.lift:.2f}")
```

### Markdown Optimization

```python
from fashion_tech.retail_analytics import MarkdownOptimizer

optimizer = MarkdownOptimizer(
    objective="maximize_revenue",
    constraint="clear_90pct_by_week_12",
)

# Optimize markdown schedule for a style
plan = optimizer.optimize(
    style_id="DRESS-001",
    current_inventory=2500,
    weeks_remaining=12,
    cost_of_goods=25.00,
    original_retail=89.99,
    current_sell_through=0.35,
    demand_forecast=[120, 110, 95, 80, 65, 50, 35, 25, 15, 10, 5, 3],
)

print("Markdown Schedule:")
for week in plan.markdowns:
    print(f"  Week {week.week}: {week.discount_pct:.0f}% off → ${week.markdown_price:.2f}")
print(f"  Expected revenue: ${plan.total_revenue:,.2f}")
print(f"  Expected clearance: {plan.projected_clearance:.1%}")
```

### Sell-Through Analysis

```python
from fashion_tech.retail_analytics import SellThroughAnalyzer

analyzer = SellThroughAnalyzer()

# Analyze sell-through by size
analysis = analyzer.analyze(
    style_id="SHIRT-042",
    sales_data="pos_data.csv",
    inventory_data="inventory_snapshot.csv",
    weeks_on_floor=6,
)

for size in analysis.size_breakdown:
    status = "GOOD" if size.sell_through > 0.4 else "SLOW" if size.sell_through < 0.2 else "OK"
    print(f"  Size {size.label}: {size.sell_through:.1%} sell-through "
          f"({size.units_sold}/{size.units_received}) [{status}]")

print(f"\n  Overall: {analysis.total_sell_through:.1%}")
print(f"  Lost sales (sizes OOS): {analysis.lost_sales_units} units")
```

## Architecture

```
Data Sources
├── POS Terminals (transactions)
├── E-commerce Platform (clickstream, orders)
├── Loyalty / CRM System
├── Inventory Management System
├── Foot Traffic Sensors
└── Competitor Price Scrapers
         │
         ▼
┌─────────────────────┐
│  Data Warehouse      │──→ Star schema with fact/dim tables
│  (ETL / ELT)         │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Analytics Engine    │──→ Segmentation, basket, markdown models
│  (ML + Statistics)   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Visualization        │──→ Dashboards, alerts, reports
│  (BI Layer)           │
└─────────────────────┘
```

## Best Practices

- Track sell-through at SKU (style-color-size) level, not just style level, for actionable insights
- Compare performance against plan, not just prior year, to account for changed assortment and market conditions
- Use rolling 4-week averages to smooth weekly volatility in trend identification
- Segment markdown recommendations by channel since online and store demand patterns differ significantly
- Monitor size sell-through weekly and adjust replenishment to prevent size-specific stockouts
- Account for cannibalization when evaluating cross-sell recommendations
- Set up automated alerts for styles deviating >20% from sell-through plan
- Include promotional calendar context in all performance analysis to explain traffic/revenue spikes
- Use cohort analysis to measure true customer retention, not just aggregate repeat rates
- Validate analytics insights with store team feedback before implementing operational changes

## Related Modules

- `fashion-tech/trend-prediction` - Feed trend data into demand forecasting
- `fashion-tech/supply-chain` - Align inventory with sell-through insights
- `fashion-tech/sustainable-fashion` - Track circular program performance
- `fashion-tech/virtual-try-on` - Measure try-on impact on conversion

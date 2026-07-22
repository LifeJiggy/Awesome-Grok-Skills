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

---

## Advanced Configuration

### Analytics Settings

```python
from retail_analytics import AnalyticsConfig

analytics_config = AnalyticsConfig(
    # Data Sources
    sources={
        "pos": {"type": "database", "connection": "pos-db:5432"},
        "ecommerce": {"type": "api", "platform": "shopify"},
        "loyalty": {"type": "csv", "path": "/data/loyalty"},
        "foot_traffic": {"type": "sensor", "endpoint": "traffic-api"},
    },
    
    # Processing
    processing={
        "batch_schedule": "0 2 * * *",  # Daily at 2am
        "real_time_enabled": True,
        "window_size_hours": 24,
    },
    
    # Metrics
    metrics={
        "sell_through": True,
        "basket_analysis": True,
        "markdown_optimization": True,
        "customer_lifetime_value": True,
    },
)
```

### Dashboard Settings

```python
from retail_analytics import DashboardConfig

dashboard_config = DashboardConfig(
    # Refresh
    refresh={
        "auto_refresh": True,
        "interval_minutes": 15,
        "on_demand": True,
    },
    
    # Visualizations
    visualizations={
        "sales_heatmap": True,
        "trend_charts": True,
        "geo_analysis": True,
        "product_performance": True,
    },
    
    # Alerts
    alerts={
        "low_stock": {"threshold": 10, "notify": ["inventory_team"]},
        "sales_spike": {"threshold": 150, "notify": ["management"]},
        "markdown_needed": {"threshold": 0.3, "notify": ["merchandising"]},
    },
)
```

## Architecture Patterns

### Retail Analytics Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Data Sources                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ POS      │  │ E-commerce│  │ Loyalty  │         │
│  │ Systems  │  │ Platform │  │ Program  │         │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘         │
└───────┼──────────────┼──────────────┼───────────────┘
        │              │              │
        ▼              ▼              ▼
┌─────────────────────────────────────────────────────┐
│              Processing Layer                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ ETL      │──│ Analytics│──│ ML       │         │
│  │ Pipeline │  │ Engine   │  │ Models   │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────┬───────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────┐
│              Presentation Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │Dashboards│  │ Reports  │  │ Alerts   │         │
│  └──────────┘  └──────────┘  └──────────┘         │
└─────────────────────────────────────────────────────┘
```

### Customer Segmentation

```python
from retail_analytics import CustomerSegmentation

segmentation = CustomerSegmentation()

# Segment customers
segments = segmentation.segment(
    customers=customer_data,
    method="rfm",  # rfm, kmeans, dbscan
    features=["recency", "frequency", "monetary"],
    n_segments=5,
)

for segment in segments:
    print(f"{segment.name}: {segment.customer_count} customers")
    print(f"  Avg value: ${segment.avg_value:.2f}")
    print(f"  Churn risk: {segment.churn_risk:.1%}")
```

### Basket Analysis

```python
from retail_analytics import BasketAnalysis

basket = BasketAnalysis()

# Analyze baskets
rules = basket.analyze(
    transactions=transaction_data,
    min_support=0.01,
    min_confidence=0.5,
)

print(f"Rules found: {len(rules)}")
for rule in rules[:5]:
    print(f"  {rule.antecedent} → {rule.consequent}")
    print(f"    Support: {rule.support:.3f}, Confidence: {rule.confidence:.3f}")
```

## Integration Guide

### POS Integration

```python
from retail_analytics import POSIntegration

pos = POSIntegration()

# Connect to POS
pos.configure(
    system="square",
    api_key="your-api-key",
    store_id="store-123",
)

# Get transactions
transactions = pos.get_transactions(
    time_range_days=30,
    include_items=True,
)

print(f"Transactions: {len(transactions)}")
print(f"Revenue: ${transactions.total_revenue:,.2f}")
```

### E-commerce Integration

```python
from retail_analytics import EcommerceAnalytics

ecom = EcommerceAnalytics()

# Configure e-commerce
ecom.configure(
    platform="shopify",
    store_url="https://store.example.com",
    api_key="your-api-key",
)

# Get analytics
analytics = ecom.get_analytics(
    time_range_days=30,
    metrics=["visitors", "conversion", "revenue"],
)

print(f"Visitors: {analytics.visitors:,}")
print(f"Conversion: {analytics.conversion_rate:.2%}")
print(f"Revenue: ${analytics.revenue:,.2f}")
```

## Performance Optimization

### Query Optimization

```python
from retail_analytics import QueryOptimizer

optimizer = QueryOptimizer()

# Optimize queries
result = optimizer.optimize(
    queries=["sell_through", "basket_analysis", "customer_segment"],
    strategies=[
        "materialized_views",
        "partition_pruning",
        "caching",
    ],
)

print(f"Query time reduction: {result.improvement:.1%}")
print(f"Cache hit rate: {result.cache_hit_rate:.1%}")
```

### Dashboard Optimization

```python
from retail_analytics import DashboardOptimizer

dash_opt = DashboardOptimizer()

# Optimize dashboard
result = dash_opt.optimize(
    dashboard_id="sales_overview",
    strategies=[
        "data_aggregation",
        "lazy_loading",
        "result_caching",
    ],
)

print(f"Load time reduction: {result.improvement:.1%}")
print(f"Data points reduced: {result.data_reduction:.1%}")
```

## Security Considerations

### Data Security

```python
from retail_analytics import DataSecurity

security = DataSecurity()

# Encrypt sensitive data
security.encrypt(
    table="customers",
    columns=["email", "phone", "credit_card"],
    algorithm="aes-256",
)

# Mask PII
security.mask(
    table="transactions",
    columns=["customer_email"],
    mask_type="partial",
)
```

### Access Control

```python
from retail_analytics import AccessControl

ac = AccessControl()

# Role-based access
ac.define_role("analyst", permissions=[
    "reports.view",
    "dashboards.view",
    "data.export_limited",
])

ac.define_role("manager", permissions=[
    "reports.view",
    "reports.create",
    "dashboards.edit",
    "data.export_full",
])
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Slow queries | Missing indexes | Add indexes, use materialized views |
| Inaccurate metrics | Data quality issues | Validate data, fix ETL |
| Dashboard lag | Too much data | Aggregate, cache, paginate |
| Missing data | Sync failures | Check integrations, fix errors |
| Alert fatigue | Too many alerts | Tune thresholds, prioritize |

### Debug Mode

```python
from retail_analytics import enable_debug

enable_debug(
    components=["etl", "analytics", "dashboard"],
    log_level="DEBUG",
)

# Debug analytics
debug_session = debug.trace_analytics("sell_through")
print(f"Debug report: {debug_session.report_url}")
```

## API Reference

### REST Endpoints

```
GET    /api/v1/retail/sales                  Get sales data
GET    /api/v1/retail/products               List products
GET    /api/v1/retail/customers              List customers
GET    /api/v1/retail/analytics/sell-through Get sell-through
POST   /api/v1/retail/analytics/basket       Basket analysis
GET    /api/v1/retail/analytics/segments     Get segments
GET    /api/v1/retail/reports/{id}           Get report
```

### Data Models

```python
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime
from uuid import UUID

@dataclass
class Transaction:
    transaction_id: UUID
    store_id: UUID
    customer_id: Optional[UUID]
    items: List["TransactionItem"]
    total: float
    timestamp: datetime

@dataclass
class TransactionItem:
    product_id: UUID
    quantity: int
    price: float
    discount: float

@dataclass
class CustomerSegment:
    segment_id: UUID
    name: str
    customer_count: int
    avg_value: float
    churn_risk: float

@dataclass
class SellThrough:
    product_id: UUID
    store_id: UUID
    units_sold: int
    units_received: int
    sell_through_rate: float
    period: str
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: retail-analytics
spec:
  replicas: 3
  selector:
    matchLabels:
      app: retail-analytics
  template:
    spec:
      containers:
      - name: analytics
        image: retail-analytics:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: analytics-secrets
              key: database-url
```

## Monitoring & Observability

### Key Metrics

```python
from retail_analytics import Metrics

metrics = Metrics()

# Track analytics performance
metrics.histogram("analytics.query_ms", query_time, tags={"type": "sell_through"})
metrics.counter("analytics.reports_generated", tags={"type": "daily"})

# Track business metrics
metrics.gauge("retail.daily_revenue", revenue, tags={"store": "store-123"})
metrics.gauge("retail.conversion_rate", rate, tags={"channel": "ecommerce"})
```

## Testing Strategy

### Unit Tests

```python
import pytest
from retail_analytics import SellThroughAnalyzer

@pytest.fixture
def analyzer():
    return SellThroughAnalyzer(test_mode=True)

def test_calculate_sell_through(analyzer):
    result = analyzer.calculate(
        units_sold=100,
        units_received=150,
    )
    assert result == 0.6667
```

## Versioning & Migration

### Version History

- **2.0.0**: Added real-time analytics, ML-powered insights, advanced segmentation
- **1.5.0**: Added basket analysis, markdown optimization, dashboards
- **1.0.0**: Initial release with basic sales analytics

## Glossary

| Term | Definition |
|------|------------|
| **Sell-Through** | Units sold / Units received |
| **RFM** | Recency, Frequency, Monetary segmentation |
| **Basket Analysis** | Finding product associations |
| **Markdown** | Price reduction for clearance |
| **CLV** | Customer Lifetime Value |

## Changelog

### Version 2.0.0
- Real-time analytics
- ML-powered insights
- Advanced customer segmentation
- Predictive analytics

### Version 1.5.0
- Basket analysis
- Markdown optimization
- Dashboard builder

### Version 1.0.0
- Initial release
- Basic sales analytics
- Simple reporting

## Contributing Guidelines

1. Test with realistic retail data
2. Validate metric accuracy
3. Benchmark query performance
4. Document business logic

## Price Elasticity Analysis

### Demand Response Modeling

```python
from retail_analytics import PriceElasticityAnalyzer

analyzer = PriceElasticityAnalyzer()

# Analyze price elasticity
elasticity = analyzer.analyze(
    product_id="DRESS-001",
    price_changes=[
        {"date": "2024-01-01", "price": 89.99, "units_sold": 150},
        {"date": "2024-01-15", "price": 79.99, "units_sold": 220},
        {"date": "2024-02-01", "price": 99.99, "units_sold": 100},
    ],
)

print(f"Price Elasticity: {elasticity.coefficient:.2f}")
print(f"Elastic: {'Yes' if abs(elasticity.coefficient) > 1 else 'No'}")
print(f"Optimal Price: ${elasticity.optimal_price:.2f}")
```

## Fashion Retail Analytics Deep Dive

### Customer Lifetime Value for Fashion

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class FashionCLVModel:
    customer_id: str
    acquisition_cost: float
    purchases: List[Dict]  # [{amount, date, category, channel}]
    returns: List[Dict]
    tenure_months: int
    
    @property
    def gross_revenue(self) -> float:
        return sum(p.get("amount", 0) for p in self.purchases)
    
    @property
    def net_revenue(self) -> float:
        return_amounts = sum(r.get("refund_amount", 0) for r in self.returns)
        return self.gross_revenue - return_amounts
    
    @property
    def purchase_frequency(self) -> float:
        return len(self.purchases) / max(1, self.tenure_months)
    
    @property
    def avg_order_value(self) -> float:
        amounts = [p.get("amount", 0) for p in self.purchases]
        return np.mean(amounts) if amounts else 0
    
    @property
    def return_rate(self) -> float:
        return len(self.returns) / max(1, len(self.purchases))
    
    @property
    def category_breadth(self) -> float:
        categories = set(p.get("category", "") for p in self.purchases)
        return len(categories) / max(1, 10)  # normalized by typical categories

class CLVPredictor:
    def __init__(self):
        self.historical_clv: List[Dict] = []
    
    def predict_clv(self, customer: FashionCLVModel, months_ahead: int = 12) -> Dict:
        # BG/NBD-inspired simplified model
        recency = customer.tenure_months
        frequency = customer.purchase_frequency
        monetary = customer.avg_order_value
        
        # Survival probability
        churn_risk = max(0.1, 1.0 - frequency * 0.3 - (1 - customer.return_rate) * 0.2)
        survival_prob = (1 - churn_risk) ** months_ahead
        
        # Predicted purchases
        predicted_purchases = frequency * months_ahead * survival_prob
        predicted_revenue = predicted_purchases * monetary * (1 - customer.return_rate * 0.5)
        
        # Margin estimate (fashion average 50-60% gross margin)
        gross_margin = 0.55
        predicted_profit = predicted_revenue * gross_margin - customer.acquisition_cost * (1 - survival_prob)
        
        return {
            "customer_id": customer.customer_id,
            "current_clv": round(customer.net_revenue, 2),
            "predicted_clv_12m": round(predicted_revenue * gross_margin, 2),
            "survival_probability": round(survival_prob, 3),
            "predicted_purchases": round(predicted_purchases, 1),
            "predicted_profit": round(predicted_profit, 2),
            "clv_segment": self._segment(predicted_revenue * gross_margin),
            "retention_investment": round(predicted_profit * 0.15, 2),
        }
    
    def _segment(self, predicted_profit: float) -> str:
        if predicted_profit > 2000: return "VIP"
        elif predicted_profit > 500: return "Loyal"
        elif predicted_profit > 100: return "Regular"
        elif predicted_profit > 0: return "At-risk"
        return "Churned"

class FashionInventoryTurnoverAnalyzer:
    def analyze_turnover(self, inventory_data: List[Dict]) -> Dict:
        total_units = sum(i.get("units", 0) for i in inventory_data)
        total_sold = sum(i.get("sold_units", 0) for i in inventory_data)
        avg_inventory = total_units  # simplified
        cogs = sum(i.get("sold_units", 0) * i.get("cost", 0) for i in inventory_data)
        
        turnover_ratio = total_sold / max(1, avg_inventory)
        days_of_supply = 365 / max(1, turnover_ratio)
        
        category_turns = {}
        for item in inventory_data:
            cat = item.get("category", "unknown")
            if cat not in category_turns:
                category_turns[cat] = {"units": 0, "sold": 0}
            category_turns[cat]["units"] += item.get("units", 0)
            category_turns[cat]["sold"] += item.get("sold_units", 0)
        
        cat_analysis = {}
        for cat, data in category_turns.items():
            cat_turns = data["sold"] / max(1, data["units"])
            cat_analysis[cat] = {
                "turnover": round(cat_turns, 2),
                "days_of_supply": round(365 / max(1, cat_turns)),
                "sell_through": round(data["sold"] / max(1, data["units"]), 3),
                "status": "healthy" if 4 <= cat_turns <= 8 else "slow" if cat_turns < 4 else "fast",
            }
        
        return {
            "overall_turnover": round(turnover_ratio, 2),
            "overall_days_of_supply": round(days_of_supply),
            "cogs": round(cogs, 2),
            "category_analysis": cat_analysis,
            "slow_movers": [cat for cat, a in cat_analysis.items() if a["status"] == "slow"],
            "recommendations": self._recommendations(cat_analysis),
        }
    
    def _recommendations(self, analysis: Dict) -> List[str]:
        recs = []
        for cat, data in analysis.items():
            if data["status"] == "slow":
                recs.append(f"Mark down {cat} items - {data['days_of_supply']} days supply")
            elif data["status"] == "fast":
                recs.append(f"Reorder {cat} - high demand, {data['sell_through']:.0%} sell-through")
        return recs

class PriceOptimizationEngine:
    def optimize_prices(self, products: List[Dict], constraints: Dict) -> List[Dict]:
        optimized = []
        for product in products:
            current_price = product.get("price", 0)
            elasticity = product.get("price_elasticity", -1.5)
            margin = product.get("margin", 0.5)
            inventory_age_days = product.get("age_days", 0)
            
            # Dynamic pricing based on inventory age
            if inventory_age_days > 90:
                adjustment = -0.20  # aggressive markdown
            elif inventory_age_days > 60:
                adjustment = -0.10
            elif product.get("demand_trend") == "increasing":
                adjustment = 0.05
            else:
                adjustment = 0.0
            
            new_price = current_price * (1 + adjustment)
            new_price = max(constraints.get("min_margin_price", current_price * 0.5), new_price)
            new_price = min(constraints.get("max_price", current_price * 2), new_price)
            
            optimized.append({
                "product_id": product.get("id"),
                "current_price": current_price,
                "optimized_price": round(new_price, 2),
                "adjustment_pct": round(adjustment * 100, 1),
                "expected_volume_change": round(-elasticity * adjustment, 3),
                "reason": f"Inventory age: {inventory_age_days}d" if adjustment < 0 else "Demand increasing",
            })
        
        return optimized
```

## License

MIT License - Copyright (c) 2024 Awesome Grok Skills

---
name: "Business Intelligence (BI) Agent"
version: "2.0.0"
description: "Comprehensive BI reporting, analytics, dashboard design, KPI tracking, and self-service data exploration"
author: "Awesome Grok Skills"
license: "MIT"
tags:
  - bi
  - business-intelligence
  - reporting
  - analytics
  - dashboards
  - kpi
  - visualization
  - data-warehousing
  - etl
  - self-service-analytics
category: "analytics"
personality: "analytical-data-driven"
use_cases:
  - report-generation
  - dashboard-creation
  - kpi-tracking
  - data-visualization
  - ad-hoc-analysis
  - business-monitoring
  - performance-management
  - executive-reporting
  - operational-analytics
  - customer-analytics
---

# Business Intelligence (BI) Agent

> Transforming raw data into actionable business insights through advanced analytics, interactive dashboards, and intelligent reporting.

## Agent Identity

You are the Business Intelligence Agent — a senior analytics architect with deep expertise in data warehousing, ETL pipelines, dimensional modeling, and executive dashboard design. You think in metrics, reason in trends, and communicate through data stories.

### Core Personality Traits

- **Data-Driven**: Every recommendation is backed by quantifiable evidence
- **Methodical**: Systematic approach to data analysis and visualization
- **Insight-Focused**: Look beyond numbers to find actionable business insights
- **User-Centric**: Design reports and dashboards for the audience, not the data
- **Quality-Obsessed**: Ensure data accuracy, consistency, and completeness

## Core Principles

### 1. Data Integrity First
Every analysis begins with validating data quality. Never present insights from unverified or inconsistent data sources.

### 2. Context Over Numbers
Raw numbers mean nothing without context. Always compare to benchmarks, historical trends, or targets.

### 3. Audience-Appropriate Design
Executive dashboards differ from operational dashboards. Tailor complexity and detail to the viewer.

### 4. Actionable Insights
Reports should answer "so what?" and "now what?" — not just describe what happened.

### 5. Progressive Disclosure
Start with high-level summaries, enable drill-down to details. Don't overwhelm with everything at once.

## Capabilities

### Report Generation

Create, schedule, and distribute business reports across the organization.

```python
from agents.bi.agent import BIAgent, ReportType

agent = BIAgent()

# Create a weekly sales report
report_id = agent.report_manager.create_report(
    name="Weekly Sales Report",
    report_type=ReportType.OPERATIONAL,
    metrics=["revenue", "orders", "customers", "avg_order_value"],
    schedule="weekly",
    owner="VP Sales",
    delivery_channels=["email", "slack"]
)

# Generate the report
result = agent.report_manager.generate_report(
    report_id=report_id,
    date_range={"start": "2024-01-01", "end": "2024-01-21"}
)

# Access results
print(f"Revenue: {result['highlights'][0]['value']}")
print(f"Trend: {result['trends']['improving']}")
```

### Dashboard Design

Build interactive dashboards with configurable layouts, themes, and widgets.

```python
# Design executive dashboard
exec_dashboard = agent.dashboard_designer.design_executive_dashboard()

# Create custom dashboard
dashboard_id = agent.dashboard_designer.create_dashboard(
    name="Sales Performance",
    widgets=[
        {"type": "kpi_card", "title": "Revenue", "metric": "total_revenue"},
        {"type": "line_chart", "title": "Trend", "metric": "revenue_trend"},
        {"type": "bar_chart", "title": "By Region", "metric": "regional_sales"}
    ],
    layout="grid",
    theme="corporate"
)

# Analyze dashboard usage
usage = agent.dashboard_designer.analyze_dashboard_usage(dashboard_id)
print(f"Engagement score: {usage['engagement_score']}")
```

### KPI Tracking

Define, monitor, and alert on key performance indicators.

```python
# Define KPIs based on business goals
kpis = agent.kpi_analyzer.define_kpis(["growth", "efficiency", "satisfaction"])

# Track performance
performance = agent.kpi_analyzer.track_kpi_performance()

for kpi in performance['kpi_performance']:
    print(f"{kpi['kpi']}: {kpi['current']} ({kpi['status']})")

# Get industry benchmarks
benchmarks = agent.kpi_analyzer.get_kpi_benchmarks("Revenue Growth")
print(f"Industry average: {benchmarks['industry_avg']}%")
```

### Data Visualization

Suggest and configure optimal visualizations for different data types.

```python
# Get visualization recommendation
suggestion = agent.visualization.suggest_visualization(
    data_type="time_series",
    data_points=50,
    purpose="trend_analysis"
)
print(f"Recommended: {suggestion['primary']}")
print(f"Alternatives: {suggestion['alternatives']}")

# Create widget configuration
widget = agent.visualization.create_widget(
    widget_type=VisualizationType.LINE_CHART,
    title="Revenue Trend",
    data_source="sales_orders",
    dimensions=["order_date"],
    measures=["amount"]
)
```

### Self-Service Analytics

Enable business users to explore data and create ad-hoc analyses.

```python
# Explore available data
explorer = agent.self_service.get_data_explorer()
print(f"Available tables: {explorer['available_tables']}")
print(f"Features: {[f['feature'] for f in explorer['self_service_features']]}")

# Run ad-hoc analysis
analysis = agent.self_service.run_ad_hoc_analysis(
    question="What are our top performing products by region?",
    data_sources=["sales_orders", "products"]
)
print(f"Key findings: {analysis['results']['key_findings']}")
```

## Operational Guidelines

### Report Generation Workflow

1. **Validate Requirements**: Confirm metrics, dimensions, filters, and schedule
2. **Check Data Sources**: Ensure all required data is available and fresh
3. **Apply Templates**: Use standardized templates when available
4. **Generate Content**: Execute queries, calculate metrics, build narrative
5. **Quality Check**: Verify totals, trends, and calculations
6. **Distribute**: Send via configured channels with appropriate formatting

### Dashboard Design Principles

1. **Layout Hierarchy**: Most important metrics at top-left
2. **Widget Sizing**: KPI cards (1x1), charts (2x2 or 2x1), tables (full width)
3. **Color Consistency**: Use consistent colors across related widgets
4. **Interactive Elements**: Enable tooltips, filters, and drill-down
5. **Mobile Responsiveness**: Ensure readability on all screen sizes

### KPI Management Rules

1. **SMART Criteria**: Specific, Measurable, Achievable, Relevant, Time-bound
2. **Owner Assignment**: Every KPI must have a designated owner
3. **Threshold Setting**: Warning and critical thresholds required
4. **Regular Review**: KPIs reviewed quarterly for relevance
5. **Historical Context**: Always show trend, not just current value

## Method Signatures

### ReportManager

```python
def create_report(
    name: str,
    report_type: ReportType,
    metrics: List[str],
    schedule: str,
    owner: str = "",
    delivery_channels: Optional[List[str]] = None,
    filters: Optional[Dict[str, Any]] = None
) -> str

def generate_report(
    report_id: str,
    date_range: Dict[str, str]
) -> Dict

def get_report_dashboard() -> Dict

def clone_report(
    report_id: str,
    new_name: str
) -> Optional[str]

def archive_report(report_id: str) -> bool
```

### DashboardDesigner

```python
def create_dashboard(
    name: str,
    widgets: List[Dict],
    layout: DashboardLayout = DashboardLayout.GRID,
    theme: str = "default",
    owner: str = ""
) -> str

def design_executive_dashboard() -> Dict

def design_operational_dashboard() -> Dict

def analyze_dashboard_usage(dashboard_id: str) -> Dict

def clone_dashboard(
    dashboard_id: str,
    new_name: str
) -> Optional[str]
```

### KPIAnalyzer

```python
def define_kpis(business_goals: List[str]) -> Dict

def track_kpi_performance() -> Dict

def get_kpi_benchmarks(kpi_name: str) -> Dict[str, float]

def calculate_kpi_score(kpi_id: str) -> float
```

### DataVisualization

```python
def suggest_visualization(
    data_type: str,
    data_points: int,
    purpose: str
) -> Dict

def create_visualization_config(
    viz_type: VisualizationType,
    data_config: Dict
) -> Dict

def create_widget(
    widget_type: VisualizationType,
    title: str,
    data_source: str,
    dimensions: Optional[List[str]] = None,
    measures: Optional[List[str]] = None,
    position: Optional[Dict[str, int]] = None,
    size: Optional[Dict[str, int]] = None
) -> Widget

def generate_color_palette(
    num_colors: int,
    palette_type: str = "default"
) -> List[str]
```

### SelfServiceAnalytics

```python
def create_query(
    query_type: str,
    parameters: Dict
) -> Dict

def run_ad_hoc_analysis(
    question: str,
    data_sources: List[str]
) -> Dict

def get_data_explorer() -> Dict

def save_query(
    query_id: str,
    name: str,
    description: str = ""
) -> bool

def get_query_suggestions(partial_query: str) -> List[str]
```

## Usage Patterns

### Pattern 1: Executive Morning Briefing

```python
# Generate daily executive summary
report = agent.report_manager.generate_report(
    report_id="exec_daily",
    date_range={"start": "yesterday", "end": "today"}
)

# Check KPI health
kpi_status = agent.kpi_analyzer.track_kpi_performance()

# Create briefing
briefing = {
    "highlights": report["highlights"],
    "alerts": kpi_status["alerts"],
    "recommendations": kpi_status["recommendations"]
}
```

### Pattern 2: Ad-Hoc Analysis

```python
# Business user asks a question
analysis = agent.self_service.run_ad_hoc_analysis(
    question="Why did sales drop in the Southeast region last month?",
    data_sources=["sales_orders", "customers", "marketing_campaigns"]
)

# Get visualization suggestion
viz = agent.visualization.suggest_visualization(
    data_type="comparison",
    data_points=12,
    purpose="root_cause_analysis"
)
```

### Pattern 3: Dashboard Creation

```python
# Create department dashboard
dashboard_id = agent.dashboard_designer.create_dashboard(
    name="Marketing Performance",
    widgets=[
        {"type": "kpi_card", "title": "Leads", "metric": "leads_generated"},
        {"type": "kpi_card", "title": "CAC", "metric": "customer_acquisition_cost"},
        {"type": "funnel", "title": "Conversion Funnel"},
        {"type": "bar_chart", "title": "Channel Performance"},
        {"type": "line_chart", "title": "Trend Over Time"}
    ],
    layout="grid",
    theme="corporate",
    owner="CMO"
)
```

## Data Models

### Report

```python
@dataclass
class Report:
    report_id: str
    name: str
    report_type: ReportType
    schedule: str
    metrics: List[str]
    filters: Dict[str, Any]
    status: str
    owner: str
    created_at: str
    last_run: str
    next_run: str
    delivery_channels: List[str]
```

### KPI

```python
@dataclass
class KPI:
    kpi_id: str
    name: str
    definition: str
    formula: str
    target: float
    unit: str
    frequency: str
    owner: str
    data_source: str
    category: MetricCategory
    thresholds: Dict[str, float]
    current_value: float
    previous_value: float
    trend: str
    status: KPIStatus
```

### Dashboard

```python
@dataclass
class Dashboard:
    dashboard_id: str
    name: str
    layout: DashboardLayout
    widgets: List[Dict[str, Any]]
    filters: List[str]
    refresh_rate: str
    owner: str
    theme: str
    created_at: str
```

## Checklists

### Pre-Report Generation

- [ ] Data sources are accessible and fresh
- [ ] Required metrics are defined and calculable
- [ ] Date range is valid and complete
- [ ] Filters are correctly specified
- [ ] Distribution list is current
- [ ] Template exists or custom layout is defined

### Dashboard Review

- [ ] All widgets display correct data
- [ ] Filters work as expected
- [ ] Drill-down navigation functions
- [ ] Mobile responsiveness verified
- [ ] Load time acceptable (< 3 seconds)
- [ ] Colors are consistent and accessible

### KPI Validation

- [ ] KPI definition is clear and unambiguous
- [ ] Data source is reliable and timely
- [ ] Target is realistic and measurable
- [ ] Thresholds are appropriately set
- [ ] Owner is assigned and notified
- [ ] Historical trend is available

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Report generation fails | Data source unavailable | Check connectivity, verify credentials |
| Dashboard slow to load | Too many widgets or large data | Reduce widget count, add caching |
| KPI shows wrong value | Formula error or stale data | Verify formula, refresh data source |
| Visualization unclear | Wrong chart type selected | Use `suggest_visualization` for guidance |
| Alerts not firing | Threshold not set or misconfigured | Review threshold settings |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable detailed logging
agent = BIAgent()
agent.report_manager.create_report(...)  # Will log detailed execution info
```

### Performance Optimization

1. **Cache Frequently Accessed Data**: Use Redis for query results
2. **Schedule Heavy Reports**: Run complex reports during off-peak hours
3. **Aggregate Data**: Pre-aggregate historical data for faster queries
4. **Index Optimization**: Ensure database indexes align with query patterns
5. **Lazy Loading**: Load dashboard widgets on-demand

## Advanced Features

### Natural Language Queries

```python
# The self-service analytics engine supports natural language
analysis = agent.self_service.run_ad_hoc_analysis(
    question="Show me the top 5 customers by revenue this quarter",
    data_sources=["sales_orders", "customers"]
)
```

### Automated Insights

```python
# AI-powered insight generation
performance = agent.kpi_analyzer.track_kpi_performance()
# Automatically identifies anomalies, trends, and correlations
```

### Comparative Analysis

```python
# Compare performance across dimensions
analysis = agent.self_service.run_ad_hoc_analysis(
    question="Compare sales performance between North and South regions",
    data_sources=["sales_orders"]
)
```

## Integration Points

### Data Sources

- SQL Databases (PostgreSQL, MySQL, BigQuery, Snowflake)
- APIs (REST, GraphQL)
- File Systems (CSV, Excel, JSON)
- Streaming (Kafka, Kinesis)

### Distribution Channels

- Email (SMTP, SendGrid, SES)
- Slack / Microsoft Teams
- Webhooks
- PDF Export
- CSV / Excel Export

### Authentication

- OAuth 2.0 / OIDC
- API Keys
- JWT Tokens
- SAML 2.0

## Version History

| Version | Changes |
|---------|---------|
| 2.0.0 | Added self-service analytics, enhanced visualization engine |
| 1.5.0 | Added alert management, dashboard usage analytics |
| 1.0.0 | Initial release with report generation, dashboard design, KPI tracking |

## Advanced Analytics

### Predictive Analytics

```python
# Time series forecasting
forecast = agent.analytics.forecast_time_series(
    metric="revenue",
    periods=12,
    frequency="monthly",
    model="prophet",
    confidence_interval=0.95
)

print(f"Forecast: {forecast['values']}")
print(f"Confidence intervals: {forecast['confidence_intervals']}")
```

### Cohort Analysis

```python
# User cohort analysis
cohort = agent.analytics.analyze_cohort(
    cohort_type="acquisition",
    cohort_date="2024-01-01",
    period_type="monthly",
    metric="retention"
)

# Visualize cohort retention
for period, retention in cohort['retention_rates'].items():
    print(f"Month {period}: {retention:.1f}%")
```

### Funnel Analysis

```python
# Conversion funnel
funnel = agent.analytics.analyze_funnel(
    steps=["visit", "signup", "activation", "purchase", "retention"],
    date_range={"start": "2024-01-01", "end": "2024-01-31"}
)

for step in funnel['steps']:
    print(f"{step['name']}: {step['count']} ({step['conversion_rate']:.1f}%)")
```

### A/B Testing

```python
# Statistical significance test
result = agent.analytics.ab_test(
    metric="conversion_rate",
    control_group=control_data,
    treatment_group=treatment_data,
    significance_level=0.05
)

print(f"Control: {result['control_mean']:.3f}")
print(f"Treatment: {result['treatment_mean']:.3f}")
print(f"P-value: {result['p_value']:.4f}")
print(f"Statistically significant: {result['significant']}")
```

## Machine Learning Integration

### Anomaly Detection

```python
# Detect anomalies in metrics
anomalies = agent.ml.detect_anomalies(
    metric="daily_revenue",
    algorithm="isolation_forest",
    contamination=0.01,
    date_range={"start": "2024-01-01", "end": "2024-01-31"}
)

for anomaly in anomalies['detected']:
    print(f"Anomaly on {anomaly['date']}: {anomaly['value']} (expected: {anomaly['expected']})")
```

### Clustering

```python
# Customer segmentation
segments = agent.ml.cluster_customers(
    features=["recency", "frequency", "monetary"],
    algorithm="kmeans",
    n_clusters=4,
    normalize=True
)

for segment in segments['clusters']:
    print(f"Segment {segment['id']}: {segment['size']} customers")
    print(f"  Avg RFM: {segment['centroid']}")
```

### Recommendation Engine

```python
# Product recommendations
recommendations = agent.ml.recommend_products(
    user_id="user_123",
    algorithm="collaborative_filtering",
    n_recommendations=5,
    exclude_purchased=True
)

for rec in recommendations['products']:
    print(f"Product {rec['product_id']}: score {rec['score']:.3f}")
```

## Real-time Processing

### Stream Processing

```python
# Real-time event processing
stream_job = agent.stream.create_job(
    name="real-time-analytics",
    source="kafka://events",
    sink="redis://metrics",
    processing_logic="""
        SELECT 
            user_id,
            COUNT(*) as event_count,
            SUM(amount) as total_amount
        FROM events
        WHERE event_type = 'purchase'
        GROUP BY user_id, TUMBLE(window_size => INTERVAL '1' MINUTE)
    """
)

# Monitor stream
metrics = agent.stream.get_metrics(stream_job.job_id)
print(f"Throughput: {metrics['events_per_second']} events/sec")
print(f"Latency: {metrics['processing_latency_ms']} ms")
```

### Real-time Dashboards

```python
# WebSocket configuration for real-time updates
WEBSOCKET_CONFIG = {
    "endpoint": "wss://api.example.com/ws",
    "channels": [
        "dashboard:{dashboard_id}",
        "kpi:{kpi_id}",
        "alert:critical"
    ],
    "heartbeat_interval": 30,
    "reconnect_strategy": "exponential_backoff"
}
```

## Data Governance

### Data Quality Rules

```python
QUALITY_RULES = {
    "completeness": {
        "rule": "NOT NULL",
        "severity": "critical",
        "action": "reject_record"
    },
    "uniqueness": {
        "rule": "DISTINCT",
        "severity": "high",
        "action": "flag_duplicate"
    },
    "validity": {
        "rule": "REGEX",
        "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
        "severity": "medium",
        "action": "flag_invalid"
    },
    "timeliness": {
        "rule": "FRESHNESS",
        "max_delay_hours": 24,
        "severity": "high",
        "action": "alert_stale_data"
    }
}
```

### Data Catalog

```python
# Data catalog schema
DATA_CATALOG = {
    "databases": [
        {
            "name": "analytics",
            "tables": [
                {
                    "name": "fact_orders",
                    "description": "Daily aggregated order data",
                    "columns": [
                        {"name": "date", "type": "DATE", "description": "Order date"},
                        {"name": "revenue", "type": "DECIMAL(12,2)", "description": "Total revenue"},
                        {"name": "order_count", "type": "INTEGER", "description": "Number of orders"}
                    ],
                    "owner": "data-engineering",
                    "sla": "daily by 06:00 UTC"
                }
            ]
        }
    ]
}
```

## Performance Optimization

### Query Performance

```python
# Query optimization techniques
OPTIMIZATION_TECHNIQUES = {
    "materialized_views": {
        "description": "Pre-compute expensive aggregations",
        "refresh_schedule": "hourly",
        "examples": ["daily_revenue_summary", "customer_segment_counts"]
    },
    "partitioning": {
        "description": "Partition large tables by date",
        "strategy": "range partitioning on date column",
        "benefit": "Reduces scan volume for time-range queries"
    },
    "indexing": {
        "description": "Create indexes for frequent filters",
        "examples": ["CREATE INDEX idx_orders_date ON fact_orders(date)"]
    }
}
```

### Caching Layers

```python
# Multi-level caching
CACHE_HIERARCHY = {
    "L1": {
        "type": "in-memory",
        "size": "100MB",
        "ttl": 60,
        "strategy": "LRU"
    },
    "L2": {
        "type": "redis",
        "size": "1GB",
        "ttl": 300,
        "strategy": "write-through"
    },
    "L3": {
        "type": "cdn",
        "size": "unlimited",
        "ttl": 3600,
        "strategy": "cache-aside"
    }
}
```

## Integration Patterns

### Event-Driven Architecture

```python
# Event bus configuration
EVENT_CONFIG = {
    "event_bus": "bi-agent-events",
    "rules": [
        {
            "event_type": "report.generated",
            "targets": ["slack-notification", "email-delivery"]
        },
        {
            "event_type": "kpi.threshold_breached",
            "targets": ["pagerduty", "slack-alert"]
        },
        {
            "event_type": "dashboard.updated",
            "targets": ["websocket-broadcast"]
        }
    ]
}
```

### API Gateway Configuration

```python
API_CONFIG = {
    "rate_limiting": {
        "requests_per_minute": 1000,
        "burst_size": 100
    },
    "authentication": {
        "method": "JWT",
        "issuer": "https://auth.example.com",
        "audience": "bi-agent-api"
    },
    "caching": {
        "enabled": True,
        "ttl": 300,
        "endpoints": ["/api/kpis", "/api/dashboards"]
    }
}
```

## Scalability Patterns

### Horizontal Scaling

```python
SCALING_CONFIG = {
    "auto_scaling": {
        "min_instances": 2,
        "max_instances": 10,
        "scale_up_threshold": {
            "cpu_percent": 70,
            "memory_percent": 80,
            "request_latency_p95": 500
        },
        "scale_down_threshold": {
            "cpu_percent": 30,
            "memory_percent": 40,
            "request_latency_p95": 100
        },
        "cooldown_period": 300
    }
}
```

### Database Scaling

```python
DATABASE_SCALING = {
    "read_replicas": {
        "enabled": True,
        "count": 3,
        "strategy": "round_robin"
    },
    "connection_pooling": {
        "min_connections": 5,
        "max_connections": 20,
        "idle_timeout": 300
    },
    "query_timeout": 30,
    "slow_query_threshold": 1000
}
```

## Monitoring & Alerting

### Alert Rules

```python
ALERT_RULES = {
    "high_error_rate": {
        "metric": "error_rate",
        "threshold": 0.01,
        "duration": "5m",
        "severity": "critical",
        "channels": ["pagerduty", "slack"]
    },
    "slow_queries": {
        "metric": "query_duration_p95",
        "threshold": 5000,
        "duration": "10m",
        "severity": "warning",
        "channels": ["slack"]
    },
    "low_cache_hit_rate": {
        "metric": "cache_hit_rate",
        "threshold": 0.8,
        "duration": "15m",
        "severity": "warning",
        "channels": ["slack"]
    }
}
```

### SLA Monitoring

```python
SLA_TARGETS = {
    "availability": {
        "target": 0.999,
        "measurement_period": "30d",
        "error_budget": 43.2  # minutes per month
    },
    "performance": {
        "api_latency_p95": 200,
        "dashboard_load_time": 2000,
        "report_generation_time": 30000
    },
    "freshness": {
        "data_delay_max": 3600,
        "report_generation_max": 300
    }
}
```

## Security Hardening

### API Security

```python
SECURITY_MEASURES = {
    "authentication": {
        "method": "OAuth2 + JWT",
        "token_expiry": 900,
        "refresh_token_expiry": 86400
    },
    "authorization": {
        "model": "RBAC",
        "roles": ["viewer", "analyst", "manager", "admin"],
        "permissions": {
            "viewer": ["read"],
            "analyst": ["read", "write"],
            "manager": ["read", "write", "execute"],
            "admin": ["*"]
        }
    },
    "input_validation": {
        "max_request_size": "10MB",
        "allowed_content_types": ["application/json"],
        "sql_injection_protection": True,
        "xss_protection": True
    }
}
```

### Data Protection

```python
DATA_PROTECTION = {
    "encryption": {
        "at_rest": "AES-256",
        "in_transit": "TLS 1.3",
        "key_management": "AWS KMS"
    },
    "masking": {
        "pii_fields": ["email", "phone", "address"],
        "masking_strategy": "partial_mask",
        "environments": ["development", "staging"]
    },
    "retention": {
        "raw_data": "90 days",
        "processed_data": "365 days",
        "audit_logs": "7 years"
    }
}
```

## Deployment Strategies

### Blue-Green Deployment

```python
BLUE_GREEN_CONFIG = {
    "blue_environment": {
        "name": "production-blue",
        "traffic_weight": 100,
        "auto_scaling": {"min": 3, "max": 10}
    },
    "green_environment": {
        "name": "production-green",
        "traffic_weight": 0,
        "auto_scaling": {"min": 2, "max": 5}
    },
    "switch_strategy": "canary",
    "canary_percentage": 10,
    "canary_duration": 300
}
```

### Rolling Updates

```python
ROLLING_UPDATE_CONFIG = {
    "strategy": "rolling",
    "max_surge": "25%",
    "max_unavailable": "0",
    "progress_deadline": 600,
    "min_ready_seconds": 30
}
```

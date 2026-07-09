# Business Intelligence (BI) Agent

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/awesome-grok-skills/bi-agent)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-yellow.svg)](https://www.python.org/)

A comprehensive Business Intelligence agent that transforms raw data into actionable insights through advanced reporting, interactive dashboards, KPI tracking, and self-service analytics.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Report Generation](#report-generation)
  - [Dashboard Design](#dashboard-design)
  - [KPI Tracking](#kpi-tracking)
  - [Data Visualization](#data-visualization)
  - [Self-Service Analytics](#self-service-analytics)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The BI Agent is a modular, extensible business intelligence platform designed to meet the analytics needs of modern organizations. It provides:

- **Automated Report Generation**: Create, schedule, and distribute business reports
- **Interactive Dashboards**: Build visual dashboards with drag-and-drop widgets
- **KPI Monitoring**: Track key performance indicators with real-time alerts
- **Data Visualization**: Choose the right chart type for your data
- **Self-Service Analytics**: Enable business users to explore data independently

### Why Use This Agent?

| Traditional BI | BI Agent |
|---------------|----------|
| Complex setup | Modular, plug-and-play |
| Static reports | Dynamic, interactive dashboards |
| IT-dependent | Self-service for business users |
| Siloed data | Unified data catalog |
| Manual monitoring | Automated alerts and insights |

---

## Features

### Core Features

- **Report Engine**: Generate reports in PDF, Excel, HTML, and JSON formats
- **Dashboard Designer**: Create executive, operational, and analytical dashboards
- **KPI Tracker**: Monitor metrics with configurable thresholds and alerts
- **Visualization Engine**: Support for 15+ chart types with interactive features
- **Self-Service Analytics**: Natural language queries and ad-hoc analysis

### Advanced Features

- **Template Library**: Pre-built templates for common business reports
- **Theme System**: Customizable themes (default, dark, corporate)
- **Color Palettes**: Generate accessible color schemes for visualizations
- **Usage Analytics**: Track dashboard engagement and widget usage
- **Data Catalog**: Browse available data sources and schemas
- **Alert Management**: Multi-channel notifications (email, Slack, webhooks)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Business Intelligence Agent                   │
├─────────────────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │  Report    │  │ Dashboard │  │   KPI     │  │  Self-    │  │
│  │  Manager   │  │ Designer  │  │  Analyzer │  │  Service  │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  │
│  │  Viz      │  │  Alert    │  │  Data     │  │  Export   │  │
│  │  Engine   │  │  Manager  │  │  Catalog  │  │  Service  │  │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### Component Overview

| Component | Purpose | Key Classes |
|-----------|---------|-------------|
| Report Manager | Create and generate reports | `ReportManager`, `Report` |
| Dashboard Designer | Build interactive dashboards | `DashboardDesigner`, `Dashboard` |
| KPI Analyzer | Track performance metrics | `KPIAnalyzer`, `KPI` |
| Visualization Engine | Render charts and graphs | `DataVisualization`, `Widget` |
| Self-Service Analytics | Enable data exploration | `SelfServiceAnalytics` |

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/awesome-grok-skills/agents.git
cd agents

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from agents.bi.agent import BIAgent, ReportType

# Initialize the agent
agent = BIAgent()

# Create a report
report_id = agent.report_manager.create_report(
    name="Weekly Sales Report",
    report_type=ReportType.OPERATIONAL,
    metrics=["revenue", "orders", "customers"],
    schedule="weekly"
)

# Generate the report
result = agent.report_manager.generate_report(
    report_id=report_id,
    date_range={"start": "2024-01-01", "end": "2024-01-21"}
)

print(f"Revenue: {result['highlights'][0]['value']}")
```

### Run the Demo

```bash
python agents/bi/agent.py
```

---

## Usage

### Report Generation

Create and manage business reports with automated scheduling and distribution.

```python
# Create a report
report_id = agent.report_manager.create_report(
    name="Monthly Marketing Report",
    report_type=ReportType.MARKETING,
    metrics=["leads", "conversions", "cac", "roi"],
    schedule="monthly",
    owner="CMO",
    delivery_channels=["email", "slack"]
)

# Generate with date range
result = agent.report_manager.generate_report(
    report_id=report_id,
    date_range={"start": "2024-01-01", "end": "2024-01-31"}
)

# View report dashboard
dashboard = agent.report_manager.get_report_dashboard()
print(f"Total reports: {dashboard['total_reports']}")
```

**Report Types:**

| Type | Description | Typical Use |
|------|-------------|-------------|
| `OPERATIONAL` | Daily/weekly operational metrics | Team leads, managers |
| `TACTICAL` | Monthly/quarterly analysis | Directors, VPs |
| `STRATEGIC` | Long-term trend analysis | C-suite, board |
| `AD_HOC` | On-demand custom analysis | Analysts |
| `FINANCIAL` | Revenue, costs, profitability | Finance team |
| `MARKETING` | Campaign performance, ROI | Marketing team |

### Dashboard Design

Build interactive dashboards with configurable layouts and themes.

```python
# Design executive dashboard
exec_dash = agent.dashboard_designer.design_executive_dashboard()

# Create custom dashboard
dashboard_id = agent.dashboard_designer.create_dashboard(
    name="Sales Performance Dashboard",
    widgets=[
        {"type": "kpi_card", "title": "Revenue", "metric": "total_revenue"},
        {"type": "line_chart", "title": "Revenue Trend", "metric": "monthly_revenue"},
        {"type": "bar_chart", "title": "By Region", "metric": "regional_sales"},
        {"type": "table", "title": "Top Products", "columns": ["Product", "Revenue", "Units"]},
        {"type": "funnel", "title": "Sales Funnel", "stages": ["Visitors", "Leads", "Closed"]}
    ],
    layout="grid",
    theme="corporate",
    owner="VP Sales"
)

# Analyze usage
usage = agent.dashboard_designer.analyze_dashboard_usage(dashboard_id)
print(f"Engagement score: {usage['engagement_score']}")
```

**Layout Options:**

| Layout | Description | Best For |
|--------|-------------|----------|
| `GRID` | Aligned widget grid | Most dashboards |
| `EXECUTIVE` | High-level KPIs + charts | C-suite |
| `OPERATIONAL` | Real-time monitoring | Operations |
| `RESPONSIVE` | Adapts to screen size | Mobile access |

### KPI Tracking

Define and monitor key performance indicators with automated alerts.

```python
# Define KPIs based on business goals
kpis = agent.kpi_analyzer.define_kpis(["growth", "efficiency", "satisfaction"])

# Track performance
performance = agent.kpi_analyzer.track_kpi_performance()

for kpi in performance['kpi_performance']:
    print(f"{kpi['kpi']}: {kpi['current']} ({kpi['status']})")

# Get benchmarks
benchmarks = agent.kpi_analyzer.get_kpi_benchmarks("Revenue Growth")
print(f"Industry average: {benchmarks['industry_avg']}%")
print(f"Top quartile: {benchmarks['top_quartile']}%")
```

**KPI Statuses:**

| Status | Description | Action |
|--------|-------------|--------|
| `EXCEEDING` | Above target | Consider raising target |
| `ON_TRACK` | Within 90% of target | Continue monitoring |
| `AT_RISK` | 70-90% of target | Investigate causes |
| `FAILING` | Below 70% of target | Urgent intervention |

### Data Visualization

Get recommendations for the best visualization type for your data.

```python
# Get visualization suggestion
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

# Generate color palette
colors = agent.visualization.generate_color_palette(5, "pastel")
```

**Visualization Types:**

| Type | Best For | Data Requirements |
|------|----------|-------------------|
| Line Chart | Trends over time | Time series |
| Bar Chart | Comparisons | Categorical |
| Pie Chart | Proportions | Parts of whole |
| Scatter Plot | Correlations | Two variables |
| Heatmap | Patterns | Matrix data |
| Funnel | Conversion stages | Sequential |
| KPI Card | Single metrics | Single value |

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

for finding in analysis['results']['key_findings']:
    print(f"- {finding['finding']} (confidence: {finding['confidence']})")

# Get query suggestions
suggestions = agent.self_service.get_query_suggestions("revenue")
```

---

## API Reference

### BIAgent

```python
class BIAgent:
    """Main BI Agent orchestrating all capabilities."""
    
    report_manager: ReportManager
    dashboard_designer: DashboardDesigner
    kpi_analyzer: KPIAnalyzer
    visualization: DataVisualization
    self_service: SelfServiceAnalytics
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status summary."""
```

### ReportManager

```python
class ReportManager:
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
    
    def clone_report(report_id: str, new_name: str) -> Optional[str]
    
    def archive_report(report_id: str) -> bool
```

### DashboardDesigner

```python
class DashboardDesigner:
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
    
    def clone_dashboard(dashboard_id: str, new_name: str) -> Optional[str]
```

### KPIAnalyzer

```python
class KPIAnalyzer:
    def define_kpis(business_goals: List[str]) -> Dict
    
    def track_kpi_performance() -> Dict
    
    def get_kpi_benchmarks(kpi_name: str) -> Dict[str, float]
    
    def calculate_kpi_score(kpi_id: str) -> float
```

### DataVisualization

```python
class DataVisualization:
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
        measures: Optional[List[str]] = None
    ) -> Widget
    
    def generate_color_palette(
        num_colors: int,
        palette_type: str = "default"
    ) -> List[str]
```

---

## Examples

### Example 1: Executive Morning Briefing

```python
from agents.bi.agent import BIAgent

agent = BIAgent()

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

print("=== Executive Briefing ===")
for h in briefing["highlights"]:
    print(f"{h['metric']}: {h['value']} ({h['change']})")
```

### Example 2: Ad-Hoc Analysis

```python
from agents.bi.agent import BIAgent

agent = BIAgent()

# Business user asks a question
analysis = agent.self_service.run_ad_hoc_analysis(
    question="Why did sales drop in the Southeast region last month?",
    data_sources=["sales_orders", "customers", "marketing_campaigns"]
)

print("Key Findings:")
for finding in analysis['results']['key_findings']:
    print(f"- {finding['finding']}")

print("\nRecommendations:")
for rec in analysis['recommendations']:
    print(f"- {rec}")
```

### Example 3: Dashboard Creation

```python
from agents.bi.agent import BIAgent, VisualizationType

agent = BIAgent()

# Create marketing dashboard
dashboard_id = agent.dashboard_designer.create_dashboard(
    name="Marketing Performance",
    widgets=[
        {"type": "kpi_card", "title": "Leads Generated", "metric": "leads"},
        {"type": "kpi_card", "title": "Conversion Rate", "metric": "conversion"},
        {"type": "funnel", "title": "Lead Funnel"},
        {"type": "bar_chart", "title": "Channel Performance"},
        {"type": "line_chart", "title": "Trend Over Time"},
        {"type": "pie_chart", "title": "Traffic Sources"}
    ],
    layout="grid",
    theme="corporate",
    owner="CMO"
)

print(f"Dashboard created: {dashboard_id}")
```

---

## Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/bi

# Cache
REDIS_URL=redis://localhost:6379

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-password

# Slack
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/xxx
```

### Configuration File

```yaml
# config.yaml
bi_agent:
  database:
    url: postgresql://localhost:5432/bi
    pool_size: 10
  
  cache:
    backend: redis
    url: redis://localhost:6379
    ttl: 3600
  
  reports:
    default_format: pdf
    max_concurrent: 5
    timeout: 300
  
  dashboards:
    default_theme: corporate
    auto_refresh: true
    refresh_interval: 300
  
  alerts:
    channels:
      - email
      - slack
    throttle_minutes: 30
```

---

## Best Practices

### Report Design

1. **Start with the audience**: What decisions will this report inform?
2. **Lead with insights**: Put key findings at the top
3. **Use consistent formatting**: Same date format, number format, color scheme
4. **Include context**: Compare to targets, historical trends, benchmarks
5. **Make it actionable**: Every section should suggest an action

### Dashboard Design

1. **Layout hierarchy**: Most important metrics at top-left
2. **Limit widgets**: 6-10 widgets per dashboard maximum
3. **Use appropriate chart types**: Don't force data into wrong visualizations
4. **Enable interaction**: Tooltips, filters, drill-down
5. **Test on mobile**: Ensure readability on all devices

### KPI Management

1. **Limit quantity**: 5-7 KPIs per dashboard
2. **Assign owners**: Every KPI needs someone responsible
3. **Set thresholds**: Warning and critical levels
4. **Review regularly**: Quarterly relevance check
5. **Document definitions**: Clear formula and data source

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Report generation fails | Data source unavailable | Check connectivity, verify credentials |
| Dashboard slow to load | Too many widgets | Reduce count, add caching |
| KPI shows wrong value | Formula error | Verify formula, check data source |
| Alerts not firing | Threshold misconfigured | Review threshold settings |
| Visualization unclear | Wrong chart type | Use `suggest_visualization()` |

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = BIAgent()
# Detailed logs will be output
```

### Performance Tips

1. **Cache query results**: Use Redis for repeated queries
2. **Schedule heavy reports**: Run during off-peak hours
3. **Pre-aggregate data**: Summarize historical data
4. **Optimize queries**: Add database indexes
5. **Lazy load widgets**: Load dashboard widgets on-demand

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Run linter
ruff check agents/bi/

# Run type checker
mypy agents/bi/
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Support

- **Documentation**: [docs.example.com](https://docs.example.com)
- **Issues**: [GitHub Issues](https://github.com/awesome-grok-skills/agents/issues)
- **Discussions**: [GitHub Discussions](https://github.com/awesome-grok-skills/agents/discussions)

## Advanced Usage

### Custom Visualization Components

```python
# Create custom visualization
class HeatmapWidget(VisualizationWidget):
    def __init__(self, data, color_scale="viridis"):
        self.data = data
        self.color_scale = color_scale
    
    def render(self):
        return {
            "type": "heatmap",
            "data": self.data,
            "color_scale": self.color_scale,
            "interactive": True
        }

# Register custom widget
agent.visualization.register_widget("heatmap", HeatmapWidget)
```

### Advanced Query Builder

```python
# Complex query construction
query = (agent.query_builder
    .select("date", "revenue", "orders")
    .from_table("fact_orders")
    .where("date >= '2024-01-01'")
    .where("region = 'US'")
    .group_by("date")
    .having("SUM(revenue) > 10000")
    .order_by("revenue", descending=True)
    .limit(100)
    .build())

result = agent.query_executor.execute(query)
```

### Dashboard Templates

```python
# Create reusable dashboard template
template = agent.dashboard_designer.create_template(
    name="E-commerce Executive",
    description="Executive dashboard for e-commerce metrics",
    widgets=[
        {"type": "kpi_card", "title": "Daily Revenue", "metric": "daily_revenue"},
        {"type": "kpi_card", "title": "Conversion Rate", "metric": "conversion_rate"},
        {"type": "line_chart", "title": "Revenue Trend", "metric": "revenue_trend"},
        {"type": "bar_chart", "title": "Top Products", "metric": "product_performance"},
        {"type": "pie_chart", "title": "Traffic Sources", "metric": "traffic_sources"},
        {"type": "table", "title": "Recent Orders", "columns": ["Order ID", "Amount", "Status"]}
    ],
    layout="grid",
    theme="corporate"
)

# Apply template
dashboard_id = agent.dashboard_designer.create_from_template(
    template_id=template['template_id'],
    name="Q1 2024 Executive Dashboard",
    owner="CFO"
)
```

### Automated Insights

```python
# Generate automated insights
insights = agent.analytics.generate_insights(
    metrics=["revenue", "conversion_rate", "customer_acquisition_cost"],
    date_range={"start": "2024-01-01", "end": "2024-01-31"},
    insight_types=["trend", "anomaly", "correlation"]
)

for insight in insights['insights']:
    print(f"Insight: {insight['description']}")
    print(f"Confidence: {insight['confidence']:.2f}")
    print(f"Action: {insight['recommended_action']}")
```

## Performance Tuning

### Query Optimization

```python
# Analyze query performance
analysis = agent.performance.analyze_query(
    query="SELECT date, SUM(revenue) FROM fact_orders GROUP BY date",
    explain_plan=True
)

print(f"Execution time: {analysis['execution_time_ms']} ms")
print(f"Rows scanned: {analysis['rows_scanned']}")
print(f"Indexes used: {analysis['indexes_used']}")
print(f"Optimization suggestions: {analysis['suggestions']}")
```

### Caching Strategies

```python
# Configure caching
agent.performance.configure_cache(
    cache_type="redis",
    ttl=300,
    strategy="write-through",
    invalidation_rules=[
        {"event": "data_update", "pattern": "orders:*"},
        {"event": "schema_change", "pattern": "*"}
    ]
)

# Warm cache
agent.performance.warm_cache(
    queries=[
        "SELECT * FROM daily_revenue WHERE date = CURRENT_DATE",
        "SELECT * FROM top_products LIMIT 10"
    ]
)
```

### Connection Pooling

```python
# Configure connection pooling
agent.database.configure_pool(
    min_connections=5,
    max_connections=20,
    idle_timeout=300,
    connection_timeout=10,
    retry_attempts=3
)
```

## Security Considerations

### Role-Based Access Control

```python
# Define roles and permissions
roles = {
    "viewer": {
        "permissions": ["read:dashboards", "read:reports", "read:kpis"],
        "data_access": "own_department"
    },
    "analyst": {
        "permissions": ["read:*", "write:reports", "write:dashboards"],
        "data_access": "all_departments"
    },
    "manager": {
        "permissions": ["read:*", "write:*", "execute:*"],
        "data_access": "all_departments",
        "admin": ["manage_users", "configure_alerts"]
    }
}

# Apply role to user
agent.auth.assign_role(user_id="user_123", role="analyst")
```

### Data Masking

```python
# Configure data masking
agent.security.configure_masking(
    rules=[
        {"column": "email", "strategy": "partial", "pattern": "***@***.com"},
        {"column": "phone", "strategy": "hash", "algorithm": "sha256"},
        {"column": "ssn", "strategy": "redact", "replacement": "XXX-XX-XXXX"}
    ],
    environments=["development", "staging"]
)
```

### Audit Logging

```python
# Enable audit logging
agent.security.enable_audit_logging(
    events=[
        "user.login",
        "user.logout",
        "data.access",
        "data.modification",
        "report.generation",
        "dashboard.creation"
    ],
    retention_days=365,
    storage="s3://audit-logs-bucket"
)
```

## Integration Examples

### Slack Integration

```python
# Send report to Slack
agent.integration.slack.send_report(
    webhook_url="https://hooks.slack.com/services/xxx",
    report_id="report_123",
    channel="#analytics",
    message="Daily sales report ready"
)

# Send alert
agent.integration.slack.send_alert(
    webhook_url="https://hooks.slack.com/services/xxx",
    channel="#alerts",
    severity="critical",
    message="KPI threshold breached: Conversion rate dropped below 2%"
)
```

### Email Integration

```python
# Send report via email
agent.integration.email.send_report(
    to=["cfo@company.com", "analytics@company.com"],
    report_id="report_123",
    subject="Monthly Financial Report",
    body="Please find attached the monthly financial report.",
    attachments=["report.pdf", "data.xlsx"]
)
```

### Webhook Integration

```python
# Configure webhooks
agent.integration.webhooks.register(
    endpoint="https://api.company.com/webhooks/bi",
    events=["report.generated", "kpi.alert", "dashboard.updated"],
    secret="webhook_secret_key",
    retry_policy={"max_retries": 3, "backoff": "exponential"}
)
```

## Monitoring & Troubleshooting

### Health Check

```python
# Check system health
health = agent.monitoring.health_check()
print(f"Status: {health['status']}")
print(f"Components: {health['components']}")
print(f"Uptime: {health['uptime']}")

# Check specific component
db_health = agent.monitoring.check_component("database")
print(f"Database status: {db_health['status']}")
print(f"Connection pool: {db_health['connection_pool']}")
```

### Performance Monitoring

```python
# Monitor performance metrics
metrics = agent.monitoring.get_metrics(
    time_range="last_hour",
    metrics=["api_latency", "error_rate", "throughput", "cache_hit_rate"]
)

for metric, value in metrics.items():
    print(f"{metric}: {value}")
```

### Debug Mode

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable detailed tracing
agent.monitoring.enable_tracing(
    sample_rate=1.0,
    export_to="jaeger"
)
```

## Deployment Options

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bi-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bi-agent
  template:
    metadata:
      labels:
        app: bi-agent
    spec:
      containers:
        - name: bi-agent
          image: bi-agent:latest
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: bi-secrets
                  key: database-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
```

### Terraform Deployment

```hcl
resource "aws_ecs_service" "bi_agent" {
  name            = "bi-agent"
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.bi_agent.arn
  desired_count   = 3
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = aws_subnet.private[*].id
    security_groups = [aws_security_group.bi_agent.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.bi_agent.arn
    container_name   = "bi-agent"
    container_port   = 8000
  }
}
```

## Contributing Guidelines

### Development Workflow

```bash
# 1. Fork and clone
git clone https://github.com/your-org/awesome-grok-skills.git

# 2. Create feature branch
git checkout -b feature/amazing-feature

# 3. Install development dependencies
pip install -r requirements-dev.txt

# 4. Run tests
pytest tests/ -v

# 5. Run linter
ruff check agents/bi/

# 6. Run type checker
mypy agents/bi/

# 7. Commit changes
git commit -m 'Add amazing feature'

# 8. Push to branch
git push origin feature/amazing-feature

# 9. Create Pull Request
```

### Code Standards

```python
# Code style
- Follow PEP 8
- Use type hints
- Write docstrings for all public functions
- Keep functions under 50 lines
- Maximum line length: 88 characters

# Testing
- Write unit tests for all new features
- Maintain >90% test coverage
- Use pytest fixtures
- Mock external dependencies

# Documentation
- Update README.md for new features
- Add API documentation
- Include usage examples
```

# Analytics Agent

> **THE** definitive agent for data analytics, reporting, and insight generation.
> Transforms raw data into actionable wisdom with physics-inspired precision and meme-aware clarity.

---

## Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Core Concepts](#core-concepts)
7. [API Reference](#api-reference)
8. [Usage Patterns](#usage-patterns)
9. [Report Formats](#report-formats)
10. [Visualizations](#visualizations)
11. [Anomaly Detection](#anomaly-detection)
12. [Alerts & Monitoring](#alerts--monitoring)
13. [Batch Operations](#batch-operations)
14. [Integration Hooks](#integration-hooks)
15. [Performance Tuning](#performance-tuning)
16. [Security & Privacy](#security--privacy)
17. [Extending the Agent](#extending-the-agent)
18. [Troubleshooting](#troubleshooting)
19. [FAQ](#faq)
20. [Contributing](#contributing)

---

## Overview

The Analytics Agent is a comprehensive data analytics and reporting platform. It is designed to be:

- **Modular**: ingestion, processing, aggregation, visualization, and alerting as separate concerns.
- **Scalable**: supports batch and streaming analytics.
- **Observable**: tracks data freshness, pipeline health, and anomaly signals.
- **Extensible**: plugin system for custom data sources, metrics, and report formats.

### What It Does

- Ingests data from databases, APIs, and files.
- Cleans and validates data.
- Aggregates data by dimensions.
- Calculates KPIs from formulas.
- Generates reports in HTML, JSON, CSV, PDF.
- Creates chart configurations.
- Detects anomalies in metrics.
- Dispatches alerts via email, Slack, webhooks.

---

## Key Features

### Core Capabilities

| Capability | Description |
|------------|-------------|
| **Data Processing** | Ingest, clean, normalize, and validate data. |
| **Aggregation Engine** | Group-by operations with sum, avg, min, max, count. |
| **KPI Calculation** | Compute KPIs from configurable formulas. |
| **Report Generation** | HTML, JSON, CSV, PDF reports. |
| **Visualization** | Line, bar, pie, scatter, histogram, heatmap charts. |
| **Anomaly Detection** | Threshold and baseline-based anomaly checks. |
| **Alerting** | Email, Slack, webhook dispatch. |
| **Scheduled Reporting** | Cron-based report generation and distribution. |

---

## Installation

```bash
git clone https://github.com/LifeJiggy/Awesome-Grok-Skills.git
cd Awesome-Grok-Skills
```

Optional dependencies:
```bash
pip install pandas numpy  # data processing
pip install matplotlib seaborn  # visualization
pip install sqlalchemy  # database connectivity
pip install aiohttp  # async API calls
```

---

## Configuration

```python
from agents.analytics.agent import AnalyticsEngine, ReportGenerator, VisualizationGenerator, AnomalyDetector, AlertingEngine, Config

config = Config(
    # Reporting
    default_report_format="html",
    output_directory="./reports",
    max_report_rows=10000,

    # Anomaly detection
    anomaly_threshold=0.1,
    baseline_samples=30,

    # Alerting
    alert_channels=["email", "slack"],
    alert_on_anomaly=True,

    # Performance
    enable_cache=True,
    data_source_timeout=30,
    retention_days=90,
)
```

---

## Core Concepts

### Data Flow

```
Data Sources → AnalyticsEngine → Aggregations → KPIs
                                               ↓
                                        ReportGenerator → Reports
                                               ↓
                                    VisualizationGenerator → Charts
                                               ↓
                                         AnomalyDetector → Alerts
```

### Report Types

| Type | Frequency | Use Case |
|------|-----------|----------|
| `DAILY` | Every day | Operational dashboards |
| `WEEKLY` | Every week | Performance reviews |
| `MONTHLY` | Every month | Executive summaries |
| `QUARTERLY` | Every quarter | Strategic planning |
| `CUSTOM` | As needed | Ad-hoc analysis |

### Aggregation Functions

| Function | Description |
|----------|-------------|
| `sum` | Sum of values |
| `avg` | Average of values |
| `min` | Minimum value |
| `max` | Maximum value |
| `count` | Count of records |

---

## API Reference

### AnalyticsEngine

- `add_data_source(name, connection_str, source_type="database") -> None` - Add data source.
- `query(data_source, query, params=None) -> List[Dict]` - Execute query.
- `aggregate(data, group_by, aggregations) -> Dict` - Aggregate data.
- `calculate_kpis(data, kpi_definitions) -> Dict` - Calculate KPIs.
- `get_source_status(name) -> Dict` - Get source status.
- `clear_cache() -> None` - Clear query cache.

### ReportGenerator

- `create_report(name, report_type, metrics, filters=None) -> str` - Create report definition.
- `schedule_report(report_id, cron_expression, recipients) -> None` - Schedule report.
- `generate_report(report_id, data) -> Report` - Generate report.
- `export_report(report, fmt="json", path=None) -> str` - Export report to file.
- `get_scheduled_reports() -> List[Dict]` - List scheduled reports.

### VisualizationGenerator

- `generate_chart_config(chart_type, data, x_field, y_field, title=None, options=None) -> Dict` - Generate chart config.
- `generate_inline_html(chart_config) -> str` - Inline HTML preview.
- `export_to_image(chart_config, fmt="png", width=800, height=600) -> bytes` - Export to image.

### AnomalyDetector

- `set_threshold(metric, upper, lower=0) -> None` - Set anomaly threshold.
- `set_baseline(metric, mean, std, samples=30, z_threshold=3.0) -> None` - Set baseline.
- `check_anomaly(metric, value, recommendation=None) -> Dict` - Check if value is anomalous.
- `remove_metric(metric) -> None` - Remove threshold/baseline.

### AlertingEngine

- `add_rule(rule_name, condition, channel, severity="warning") -> None` - Add alert rule.
- `evaluate(result) -> List[Alert]` - Evaluate anomaly results.
- `acknowledge_alert(alert_id) -> bool` - Acknowledge alert.
- `get_alerts(status="open") -> List[Alert]` - Get alerts by status.
- `dispatch(alert) -> None` - Dispatch alert to channels.

### Enums and Data

- `ReportType`: daily, weekly, monthly, quarterly, custom.
- `DataSourceType`: database, file, api, stream.
- `AnomalySeverity`: normal, warning, critical, unknown.
- `Report`: report_id, name, report_type, metrics, filters, generated_at, data.
- `Alert`: alert_id, rule_name, severity, message, timestamp, payload, acknowledged.

---

## Usage Patterns

### Pattern 1: Daily Sales Report

```python
report_id = reporter.create_report(
    name="Daily Sales",
    report_type=ReportType.DAILY,
    metrics=["revenue", "orders", "customers"]
)

reporter.schedule_report(
    report_id=report_id,
    cron_expression="0 8 * * *",
    recipients=["team@example.com"]
)
```

### Pattern 2: Anomaly Monitoring

```python
detector.set_baseline("revenue", mean=5000, std=500, samples=30)
for daily_revenue in recent_revenues:
    result = detector.check_anomaly("revenue", daily_revenue)
    if result["is_anomaly"]:
        alerter.evaluate(result)
```

### Pattern 3: KPI Dashboard

```python
kpis = engine.calculate_kpis(data, {
    "total_revenue": {"formula": "sum(revenue)", "metrics": ["revenue"]},
    "conversion_rate": {"formula": "sum(conversions)/sum(clicks)*100", "metrics": ["conversions", "clicks"]}
})
display_dashboard(kpis)
```

### Pattern 4: Scheduled Weekly Report

```python
report_id = reporter.create_report(
    name="Weekly KPI Summary",
    report_type=ReportType.WEEKLY,
    metrics=["revenue", "orders", "customers"],
    filters={"date_range": "last_7_days"},
)
reporter.schedule_report(
    report_id=report_id,
    cron_expression="0 8 * * 1",
    recipients=["team@example.com"],
)
report = reporter.generate_report(report_id, latest_week_data)
reporter.export_report(report, fmt="html", path="./weekly_kpi.html")
```

### Pattern 5: Multi-Source Aggregation

```python
engine.add_data_source("db", "sales.db", source_type="database")
engine.add_data_source("file", "offline.csv", source_type="file")
db_rows = engine.query("db", "SELECT * FROM sales")
file_rows = engine.query("file", "SELECT * FROM data")
combined = list(db_rows) + list(file_rows)
aggregated = engine.aggregate(combined, "date", {"revenue": "sum", "orders": "count"})
```

### Pattern 6: Chart Preview Pipeline

```python
chart_cfg = visualizer.generate_chart_config(
    chart_type="bar",
    data=data,
    x_field="date",
    y_field="revenue",
    title="Daily Revenue",
    options={"stacked": False},
)
html = visualizer.generate_inline_html(chart_cfg)
```

---

## Report Formats

### HTML Report

- Summary cards for key metrics.
- Data tables with sorting.
- Embedded charts.
- Responsive layout via inline CSS.

### JSON Report

```json
{
  "report_id": "report_20240603_220000",
  "name": "Sales Summary",
  "generated_at": "2026-06-03T22:00:00",
  "summary": {"total_records": 1000},
  "details": [...]
}
```

### CSV Report

Spreadsheet-friendly rows with metrics as columns.

### PDF Report

Placeholder. In production, pipe JSON/CSV into a PDF renderer.

---

## Visualizations

### Supported Chart Types

| Type | Use Case |
|------|----------|
| `line` | Trends over time |
| `bar` | Comparisons across categories |
| `pie` | Proportions |
| `scatter` | Correlation analysis |
| `histogram` | Distribution analysis |
| `heatmap` | Matrix intensity |

### Chart Configuration

```python
chart = visualizer.generate_chart_config(
    chart_type="line",
    data=data,
    x_field="date",
    y_field="revenue",
    title="Daily Revenue"
)
# Returns config with type, data, axes, options
```

### Inline HTML Preview

```python
preview = visualizer.generate_inline_html(chart)
# Embed preview in a notebook, chat message, or email body.
```

### Export to Image

```python
image_bytes = visualizer.export_to_image(chart, fmt="png", width=1200, height=800)
with open("chart.png", "wb") as f:
    f.write(image_bytes)
```

---

## Anomaly Detection

### Detection Methods

| Method | Description |
|--------|-------------|
| `set_threshold` | Fixed upper/lower bounds. |
| `set_baseline` | Statistical baseline with z-score. |

### Severity Mapping

| Condition | Severity |
|-----------|----------|
| Value beyond threshold | critical |
| z-score > threshold * 1.5 | critical |
| z-score > threshold | warning |
| Normal | normal |

### Interpreting Results

```python
result = detector.check_anomaly("revenue", 5500)
if result["is_anomaly"]:
    print(f"Anomaly! Value: {result['value']}, Severity: {result['severity']}")
else:
    print("Normal")
```

### Example Baselines

```python
detector.set_baseline("cpu_usage", mean=45.0, std=10.0, samples=50)
detector.set_baseline("latency_ms", mean=120.0, std=25.0, samples=50)
```

---

## Alerts & Monitoring

### Alert Severity

- `critical` - Immediate action required.
- `warning` - Attention needed soon.
- `info` - Informational.

### Alert Lifecycle

```
created → evaluated → dispatched → acknowledged
```

### Acknowledging Alerts

```python
for alert in alerter.get_alerts(status="open"):
    alerter.acknowledge_alert(alert.alert_id)
```

### Custom Dispatch

Implement channel dispatch by wiring your webhook or mailer into alert handling. The current `AlertingEngine` logs dispatch calls and can be extended to call out to PagerDuty, Slack, or email services.

---

## Batch Operations

### Batch Report Generation

```python
report_ids = [reporter.create_report(f"Report {i}", ReportType.DAILY, ["revenue"]) for i in range(10)]
for rid in report_ids:
    report = reporter.generate_report(rid, data)
    reporter.export_report(report, fmt="csv", path=f"./reports/{rid}.csv")
```

### Batch Anomaly Checking

```python
metrics_to_check = ["revenue", "orders", "customers"]
for metric in metrics_to_check:
    for value in daily_values[metric]:
        detector.check_anomaly(metric, value)
```

---

## Integration Hooks

### Scheduled Reports

```python
reporter.schedule_report(
    report_id=report_id,
    cron_expression="0 6 * * 1",
    recipients=["team@example.com"]
)
```

### Alerting

```python
for alert in alerter.get_alerts():
    if alert.severity == "critical":
        send_slack_webhook(alert)
```

### Multi-Source Dashboard

```python
for database in databases:
    analytics.add_data_source(name=database["name"], connection_str=database["url"])
for report_id in report_ids:
    analytics.generate_report(...)
```

### Real-time Alerting

```python
for metric, value in live_stream():
    result = analytics.check_anomaly(metric, value)
    if result["is_anomaly"]:
        analytics.evaluate(result)
```

### CI/CD Reporting

```python
report = analytics.generate_report(report_id, latest_run_data())
analytics.export_report(report, fmt="html", path="latest.html")
```

### Anomaly Response Playbook

```python
alerts = analytics.alerter.get_alerts(status="open")
for alert in alerts:
    if alert.payload["severity"] == "critical":
        page_oncall(alert)
    elif alert.payload["severity"] == "warning":
        post_slack(alert)
```

### Batch Data Quality Checks

```python
for table in tables:
    data = analytics.query(source="warehouse", query=f"SELECT * FROM {table}")
    anomalies = [analytics.check_anomaly("row_count", len(data))]
```

---

## Performance Considerations

- Use `fmt="csv"` for large data exports.
- Enable caching for repeated queries.
- Limit `max_report_rows` to reduce serialization cost.
- Use batch operations for bulk processing.
- Keep `baseline_samples` just large enough for your seasonality.
- Avoid `max_report_rows` abuse; prefer filtering upstream.

---

## Security & Privacy

- No credentials stored in `Report` or `Config` by default.
- Data source connections should use environment-specific secrets.
- Reports may contain sensitive data; restrict export access.
- Follow organizational data classification policies.
- Log sensitive metric names with caution; avoid outputting raw payloads.

---

## Data Quality & Observability

### Source Status

```
get_source_status(name) -> {
    connection, type, schema, last_sync, status
}
```

### Cache Behavior

- `cache_enabled=True`: cached for `cache_ttl` seconds per source.
- `clear_cache()`: reset in-memory cache across all sources.
- Cache is best-effort; not a consistency mechanism.

### Alert Hygiene

- Tune thresholds and baselines against seasonality.
- Review alert noise and adjust `z_threshold`.
- Acknowledge alerts after resolution to keep queues clean.

---

## Extending the Agent

### Custom Aggregations

Add aggregation functions in `AnalyticsEngine.aggregate()`:

```python
def mode(values):
    from collections import Counter
    return Counter(values).most_common(1)[0][0]

aggregated = engine.aggregate(data, "category", {"category": "mode", "amount": "sum"})
```

### Custom KPIs

Define KPI formulas in `calculate_kpis()`:

```python
kpis = engine.calculate_kpis(data, {
    "profit_margin": {
        "formula": "(sum(revenue) - sum(cost)) / sum(revenue) * 100",
        "metrics": ["revenue", "cost"]
    }
})
```

### Custom Alert Channels

Add dispatch methods in `AlertingEngine`:

```python
class CustomAlertChannel:
    def send(self, alert):
        # Custom dispatch logic
        pass
```

---

## Troubleshooting

### Problem: Query returns empty results

- Verify `data_source` name is correct.
- Check connection string and permissions.
- Ensure query syntax matches source type.
- For files, confirm path and headers.

### Problem: Report generation slow

- Reduce `max_report_rows`.
- Enable caching.
- Use `fmt="csv"` for large exports.

### Problem: Alerts not firing

- Check `alert_channels` configuration.
- Verify `AnomalyDetector` thresholds are set.
- Ensure `evaluate()` is called after `check_anomaly()`.

### Problem: Anomaly detector over-flagging

- Review threshold values and baseline samples.
- Increase `z_threshold` to reduce sensitivity.
- Check for data quality issues in metric stream.

### Problem: Scheduled reports not running

- Verify cron syntax with `croniter` or similar.
- Check that report IDs remain valid.
- Ensure daemon process stays alive.

### Problem: CSV export malformed

- Check metric keys for special characters.
- Ensure values are scalar or stringifiable.
- Ensure no burst writes during export.

---

## FAQ

**Q: Does this connect to real databases?**
A: It provides the model. Connect to PostgreSQL, MySQL, etc., via `add_data_source()` with connection strings.

**Q: Can I use this for real-time analytics?**
A: The model supports batch and streaming patterns. Add a streaming data source (Kafka, Kinesis) via custom integration.

**Q: How accurate is anomaly detection?**
A: It uses simplified statistical methods. For production, consider dedicated libraries (Evidently, Arize).

**Q: Can I test with in-memory data?**
A: SQLite `:memory:` works as a data source for testing.

---

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md).

---

## License

MIT License - see [LICENSE](../../LICENSE).

---

## Appendix A: Metric Reference

### Classification Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| Accuracy | (TP + TN) / Total | Overall correctness |
| Precision | TP / (TP + FP) | False positive control |
| Recall | TP / (TP + FN) | False negative control |
| F1 | 2 * (P * R) / (P + R) | Harmonic mean |
| AUC | Area under ROC | Discriminative ability |
| LogLoss | -mean(y * log(p)) | Calibration quality |

### Regression Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| MAE | mean(|y - y_hat|) | Average absolute error |
| MSE | mean((y - y_hat)^2) | Average squared error |
| RMSE | sqrt(MSE) | Error in original units |
| MAPE | mean(|y - y_hat| / y) * 100 | Percentage error |
| R² | 1 - SS_res / SS_tot | Variance explained |

### Clustering Metrics

| Metric | Description |
|--------|-------------|
| Silhouette Score | Cluster cohesion and separation |
| Davies-Bouldin Index | Average similarity to closest cluster |
| Calinski-Harabasz Index | Ratio of between/within cluster variance |
| Adjusted Rand Index | Agreement with ground truth labels |

### Drift Metrics

| Metric | Formula | Description |
|--------|---------|-------------|
| PSI | sum((act% - exp%) * ln(act% / exp%)) | Population stability |
| KS Stat | max|F_ref(x) - F_curr(x)| | Distribution difference |
| JS Divergence | KL(P || M) + KL(Q || M) | Distribution similarity |
| Wasserstein | Earth mover's distance | Distribution distance |

---

## Appendix B: Troubleshooting

### Problem: Query returns empty results

- Verify `data_source` name is correct.
- Check connection string and permissions.
- Ensure query syntax is valid for the source type.

### Problem: Report generation slow

- Reduce `max_report_rows`.
- Enable `enable_cache` for repeated queries.
- Use `fmt="csv"` for large exports.

### Problem: Alerts not firing

- Check `alert_channels` configuration.
- Verify `AnomalyDetector` thresholds are set.
- Ensure `evaluate()` is called after `check_anomaly()`.

### Problem: Anomaly detector over-flagging

- Review threshold values and baseline samples.
- Increase `z_threshold` to reduce sensitivity.
- Check for data quality issues in metric stream.

### Problem: Scheduled reports not running

- Verify cron syntax with `croniter` or similar.
- Check that report IDs remain valid.
- Ensure daemon process stays alive.

---

## Appendix C: Design Decisions

### Why Separate ReportGenerator and VisualizationGenerator?

Reports contain data and metadata. Visualizations are chart-specific. Separation allows independent evolution and reuse of chart configs.

### Why In-Memory Data Sources?

For demo and library usage, in-memory storage avoids database dependencies. Production deployments can extend with persistent stores.

### Why Simplified Aggregation?

Production aggregation may use SQL engines or distributed compute. The built-in engine covers common group-by operations and is designed to be extended.

### Why Multiple Alert Channels?

Different teams prefer different communication paths. Decoupling alert evaluation from dispatch lets you route the same signal to email, Slack, PagerDuty, or webhooks.

---

## Appendix D: Integration Patterns

### Pattern: Multi-Source Dashboard

```python
for database in databases:
    analytics.add_data_source(name=database["name"], connection_str=database["url"])
for report_id in report_ids:
    analytics.generate_report(...)
```

### Pattern: Real-time Alerting

```python
for metric, value in live_stream():
    result = analytics.check_anomaly(metric, value)
    if result["is_anomaly"]:
        analytics.evaluate(result)
```

### Pattern: CI/CD Reporting

```python
report = analytics.generate_report(report_id, latest_run_data())
analytics.export_report(report, fmt="html", path="latest.html")
```

### Pattern: Anomaly Response Playbook

```python
alerts = analytics.alerter.get_alerts(status="open")
for alert in alerts:
    if alert.payload["severity"] == "critical":
        page_oncall(alert)
    elif alert.payload["severity"] == "warning":
        post_slack(alert)
```

### Pattern: Batch Data Quality Checks

```python
for table in tables:
    data = analytics.query(source="warehouse", query=f"SELECT * FROM {table}")
    anomalies = [analytics.check_anomaly("row_count", len(data))]
```

---

## Appendix E: Checklist

- [ ] Data source connection tested and authenticated
- [ ] Cache enabled for repeated queries
- [ ] Thresholds and baselines calibrated
- [ ] Alert channels configured
- [ ] Scheduled reports reviewed for seasonality
- [ ] Output directory exists and is writable
- [ ] PII handling reviewed before exporting reports

---

## Appendix F: Glossary

- **AnalyticsEngine**: Core engine for data sources, querying, aggregation, and KPI calculation.
- **ReportGenerator**: Creates, schedules, and exports analytics reports.
- **VisualizationGenerator**: Generates chart configurations and image exports.
- **AnomalyDetector**: Detects statistical anomalies in metrics.
- **AlertingEngine**: Evaluates anomalies and dispatches alerts.
- **Alert**: Structured anomaly notification payload.
- **KPI**: Key performance indicator computed from data.
- **Baseline**: Historical reference distribution for anomaly detection.
- **Pivot**: Cross-tab analysis for two-field grouping.

---

## Appendix G: Migration Guide

### From Analytics Agent v1.x

- `AnalyticsEngine` replaces older query/aggregate patterns.
- `ReportGenerator` replaces script-based report generation.
- `AnomalyDetector` replaces manual threshold checks.
- `AlertingEngine` replaces ad-hoc alerting.

### From External Spreadsheets

```python
# Convert spreadsheet rows to data source configs
for row in spreadsheet:
    analytics.add_data_source(
        name=row["Source Name"],
        connection_str=row["Connection"],
        source_type=row["Type"].lower(),
    )
```

---

## Appendix H: Compliance and Privacy

### GDPR / CCPA Considerations

- Do not store PII in `Report.data` if exported externally.
- Anonymize data before aggregation if required.
- Provide data retention and deletion workflows.

### Data Governance

- Track data source lineage.
- Maintain audit trails for report generation.
- Document data freshness and quality checks.

### Data Retention

- `retention_days` in `Config` limits history.
- Explicitly purge alert history and cached queries when no longer needed.

---

## Version History

- **v2.1.0** (2026-06-03)
  - Full rewrite with modular component architecture.
  - New components: AnalyticsEngine, ReportGenerator, VisualizationGenerator, AnomalyDetector, DataSourceManager, AlertingEngine.
  - Multi-format reporting and alerting.

- **v1.0.0** (2024-01-01)
  - Initial release with basic query and reporting.

---

---

## Appendix I: Metric Reference

### Descriptive Statistics

```
Mean = sum(x) / n
Median = middle value
Mode = most frequent value
Std Dev = sqrt(sum((x - mean)^2) / n)
Variance = std_dev^2
```

### Inferential Statistics

```
Z-score = (x - mean) / std_dev
P-value = P(observing result given null hypothesis)
Confidence Interval = mean ± z * (std_dev / sqrt(n))
```

### Correlation

```
Pearson r = cov(X, Y) / (std_X * std_Y)
Covariance = sum((x_i - mean_x) * (y_i - mean_y)) / n
```

### Regression

```
y = mx + b
m = (n*sum(xy) - sum(x)*sum(y)) / (n*sum(x^2) - sum(x)^2)
b = (sum(y) - m*sum(x)) / n
R² = 1 - SS_res / SS_tot
```

### Drift Metrics

```
PSI = sum((actual% - expected%) * ln(actual% / expected%))
KS Statistic = max|F_ref(x) - F_curr(x)|
Z-score = (value - baseline_mean) / baseline_std
```

---

---

## Appendix J: Reference Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        Analytics Agent                         │
├──────────────────────────────────────────────────────────────────┤
│  ┌───────────────┐  ┌───────────────┐  ┌─────────────────────┐  │
│  │ AnalyticsEngine│  │ ReportGenerator│  │ VisualizationGenerator│ │
│  └───────────────┘  └───────────────┘  └─────────────────────┘  │
│  ┌───────────────┐  ┌───────────────┐  ┌─────────────────────┐  │
│  │ AnomalyDetector│ │ DataSourceManager│ │ AlertingEngine     │  │
│  └───────────────┘  └───────────────┘  └─────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

### Data contracts

- Report payload: `Report` dataclass with report_id, name, type, metrics, filters, data.
- Anomaly result: Dict with metric, value, is_anomaly, severity, recommendation.
- Alert payload: `Alert` dataclass with alert_id, rule_name, severity, message, timestamp.

---

---

## Appendix K: Troubleshooting

### Symptom: Query returns empty results

1. Is the data source connected?
   - No -> Test connection with `get_source_status()`.
   - Yes -> Continue.
2. Is the query syntax valid?
   - No -> Review query and parameter placeholders.
   - Yes -> Continue.
3. Is the data present?
   - No -> Verify ingestion pipeline.
   - Yes -> Debug with smaller LIMIT.

### Symptom: Report generation slow

1. Is report very large?
   - Yes -> Use `fmt="csv"` or reduce `max_report_rows`.
   - No -> Continue.
2. Is caching enabled?
   - No -> Enable `enable_cache`.
   - Yes -> Continue.
3. Is data source slow?
   - Yes -> Add indexes or materialized views upstream.
   - No -> Profile Python serialization.

### Symptom: Alerts not firing

1. Are thresholds configured?
   - No -> Call `set_threshold()` or `set_baseline()`.
   - Yes -> Continue.
2. Is `evaluate()` called?
   - No -> Ensure alerting pipeline runs after `check_anomaly()`.
   - Yes -> Check channel configuration.

---

---

## Appendix L: Design Decisions

### Why AnalyticsAgent from multiple components?

Each component has a single responsibility:
- `AnalyticsEngine` handles data.
- `ReportGenerator` handles reports.
- `VisualizationGenerator` handles charts.
- `AnomalyDetector` handles detection.
- `AlertingEngine` handles notification.

### Why in-memory first?

For demo and library usage, in-memory storage avoids database dependencies.
Production deployments can extend with PostgreSQL, BigQuery, S3, Kafka.

### Why simplified aggregation?

Built-in engine covers common group-by operations. Production aggregation may
use DuckDB, Polars, Spark. The engine is designed to be extended.

### Why multiple alert channels?

Different teams prefer different communication paths. Decoupling evaluation from
dispatch lets you route the same signal to email, Slack, PagerDuty, or webhooks.

### Why Config dataclass?

Provides type safety, IDE support, and serialization. Makes defaults explicit.

---

---

## Appendix M: Migration Guide

### From Analytics Agent v1.x

- `AnalyticsEngine` replaces older query/aggregate patterns.
- `ReportGenerator` replaces script-based report generation.
- `AnomalyDetector` replaces manual threshold checks.
- `AlertingEngine` replaces ad-hoc alerting.

---

---

## Appendix N: Scaling Patterns

### Pattern: Multi-Source Dashboard

```python
for database in databases:
    analytics.add_data_source(name=database["name"], connection_str=database["url"])
for report_id in report_ids:
    analytics.generate_report(...)
```

### Pattern: Real-time Alerting

```python
for metric, value in live_stream():
    result = analytics.check_anomaly(metric, value)
    if result["is_anomaly"]:
        analytics.alerter.evaluate(result)
```

### Pattern: CI/CD Reporting

```python
report = analytics.generate_report(report_id, latest_run_data())
analytics.export_report(report, fmt="html", path="latest.html")
```

---

---

## Appendix O: Glossary

- **AnalyticsEngine**: Core engine for data sources, querying, aggregation, and KPI calculation.
- **ReportGenerator**: Creates, schedules, and exports analytics reports.
- **VisualizationGenerator**: Generates chart configurations and image exports.
- **AnomalyDetector**: Detects statistical anomalies in metrics.
- **AlertingEngine**: Evaluates anomalies and dispatches alerts.
- **Alert**: Structured anomaly notification payload.
- **KPI**: Key performance indicator computed from data.
- **Baseline**: Historical reference distribution for anomaly detection.
- **Pivot**: Cross-tab analysis for two-field grouping.
- **Cache**: In-memory query result cache with TTL.

---

---

## Appendix P: Version History

- **v2.1.0** (2026-06-03)
  - Full rewrite with modular component architecture.
  - New components: AnalyticsEngine, ReportGenerator, VisualizationGenerator, AnomalyDetector, DataSourceManager, AlertingEngine.
  - Multi-format reporting and alerting.

- **v1.0.0** (2024-01-01)
  - Initial release with basic query and reporting.

---

---

*Analytics Agent v2.1.0 - Part of the Awesome Grok Skills collection.*

*Last updated: 2026-06-03*

*Maintained by the Analytics Agent team and Grok community.*

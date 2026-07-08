# Data Quality Agent

Enterprise-grade data quality management — validation, profiling, cleansing, monitoring, anomaly detection, and composite quality scoring.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
  - [Dataset Registration](#dataset-registration)
  - [Profiling](#profiling)
  - [Validation](#validation)
  - [Anomaly Detection](#anomaly-detection)
  - [Cleansing Pipelines](#cleansing-pipelines)
  - [Monitoring](#monitoring)
  - [Quality Scoring](#quality-scoring)
  - [Reporting](#reporting)
- [API Reference](#api-reference)
  - [DataQualityAgent](#dataqualityagent)
  - [DataQualityConfig](#dataqualityconfig)
  - [Data Models](#data-models)
- [Examples](#examples)
- [Configuration](#configuration)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Data Quality Agent provides a comprehensive, modular system for ensuring data accuracy, completeness, consistency, timeliness, validity, and uniqueness across enterprise datasets. It profiles data statistically, enforces configurable validation rules, detects anomalies using multiple statistical methods, executes automated cleansing pipelines, monitors quality continuously with alerting, and produces scored reports.

**Key capabilities:**
- Statistical profiling of 6+ column types with 20+ metrics per column
- 6 validation rule types with severity classification
- 5 anomaly detection methods (Z-Score, IQR, MAD, EWM-STD, Percentile)
- 14 cleansing pipeline actions including PII protection
- 6 monitoring check types with history tracking
- Composite quality scoring with weighted dimension grading

---

## Features

| Feature | Description |
|---------|-------------|
| **Data Profiling** | Auto-detect column types, compute statistical distributions, identify patterns |
| **Validation Rules** | not_null, unique, regex, range, allowed_values, custom |
| **Anomaly Detection** | Z-Score, IQR, MAD, Exponentially Weighted Moving Std, Percentile |
| **Cleansing Pipelines** | Ordered step sequences: fill, trim, cast, deduplicate, mask PII |
| **Quality Monitoring** | Row counts, null percentages, freshness, schema matching |
| **Quality Scoring** | Weighted composite scores across 6 DAMA dimensions with letter grades |
| **PII Protection** | Pattern detection (email, phone, SSN, credit card), hashing, masking |
| **Comprehensive Reporting** | JSON export, summary text, per-dimension breakdowns |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    DATA QUALITY AGENT                     │
├─────────────────────────────────────────────────────────┤
│  Ingestion → Profiling → Validation → Anomaly Detection │
│       → Cleansing → Monitoring → Scoring → Reporting     │
└─────────────────────────────────────────────────────────┘
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full system architecture including component deep dives, data flow diagrams, design patterns, and scalability considerations.

---

## Quick Start

```python
from agents.data_quality.agent import (
    DataQualityAgent, DataQualityConfig, ValidationRule,
    QualityDimension, Severity, AnomalyMethod,
    CleansingStep, CleansingAction, MonitorCheck,
)

# Initialize
agent = DataQualityAgent()

# Register data
data = [
    {"id": 1, "name": "Alice", "email": "alice@example.com", "age": 30},
    {"id": 2, "name": "Bob", "email": None, "age": 25},
    {"id": 3, "name": "Charlie", "email": "invalid", "age": -5},
]
agent.register_dataset("users", data)

# Full assessment
report = agent.assess_quality("users")
print(f"Quality Score: {report.score.overall:.2%}")
print(f"Grade: {report.summary['quality_grade']}")
print(f"Issues Found: {report.summary['total_issues']}")
```

---

## Installation

### From Source

```bash
cd Awesome-Grok-Skills
pip install -e .
```

### Direct Usage

```bash
python agents/data-quality/agent.py
```

### Requirements

- Python 3.10+
- No external dependencies (uses only standard library)

---

## Usage

### Dataset Registration

```python
agent = DataQualityAgent()

# Register a dataset
result = agent.register_dataset("sales", sales_data)
print(f"Registered: {result['rows']} rows, {len(result['columns'])} columns")

# Retrieve a dataset
data = agent.get_dataset("sales")
```

### Profiling

```python
# Generate comprehensive profile
profile = agent.profile_dataset("sales")

# Dataset-level metrics
print(f"Rows: {profile.row_count}")
print(f"Columns: {profile.column_count}")
print(f"Completeness: {profile.overall_completeness:.2%}")
print(f"Duplicates: {profile.duplicate_rows}")

# Column-level metrics
for col in profile.columns:
    print(f"\n{col.column_name} ({col.profile_type.value}):")
    print(f"  Nulls: {col.null_percentage:.1f}%")
    print(f"  Distinct: {col.distinct_count}")
    if col.mean_value is not None:
        print(f"  Mean: {col.mean_value:.2f}")
    if col.top_values:
        print(f"  Top values: {list(col.top_values.items())[:3]}")
```

### Validation

```python
# Define rules
agent.add_rule(ValidationRule(
    name="email_required",
    dimension=QualityDimension.COMPLETENESS,
    severity=Severity.HIGH,
    column="email",
    rule_type="not_null",
))

agent.add_rule(ValidationRule(
    name="id_unique",
    dimension=QualityDimension.UNIQUENESS,
    severity=Severity.CRITICAL,
    column="id",
    rule_type="unique",
))

agent.add_rule(ValidationRule(
    name="age_range",
    dimension=QualityDimension.ACCURACY,
    severity=Severity.MEDIUM,
    column="age",
    rule_type="range",
    parameters={"min": 0, "max": 150},
))

# Run validation
issues = agent.validate_dataset("sales")

# Process issues
for issue in issues:
    if issue.severity in (Severity.CRITICAL, Severity.HIGH):
        print(f"[{issue.severity.value.upper()}] {issue.message}")
        print(f"  Affected rows: {issue.affected_rows}")
        print(f"  Sample values: {issue.sample_values[:3]}")
```

### Anomaly Detection

```python
# Z-Score (good for normal distributions)
anomaly = agent.detect_anomalies("sales", "revenue", AnomalyMethod.ZSCORE, threshold=3.0)
print(f"Anomalies: {anomaly.anomaly_count}")
print(f"Values: {anomaly.values[:5]}")

# IQR (good for skewed distributions)
anomaly = agent.detect_anomalies("sales", "revenue", AnomalyMethod.IQR, multiplier=1.5)

# MAD (robust against many outliers)
anomaly = agent.detect_anomalies("sales", "revenue", AnomalyMethod.MAD, threshold=3.5)

# EWM-STD (for time-series)
anomaly = agent.detect_anomalies("sales", "revenue", AnomalyMethod.EWM_STD, span=20)
```

### Cleansing Pipelines

```python
# Define pipeline steps
steps = [
    CleansingStep(action=CleansingAction.TRIM_WHITESPACE, column="name", order=1),
    CleansingStep(action=CleansingAction.LOWERCASE, column="email", order=2),
    CleansingStep(action=CleansingAction.FILL_MEDIAN, column="age", order=3),
    CleansingStep(action=CleansingAction.HASH_PII, column="ssn", order=4),
    CleansingStep(action=CleansingAction.DEDUPLICATE, order=5),
]

# Create and execute
agent.create_cleansing_pipeline("clean_sales", steps)
result = agent.run_cleansing_pipeline("sales", "clean_sales")

print(f"Rows: {result.rows_before} → {result.rows_after}")
print(f"Columns affected: {result.columns_affected}")
print(f"Steps executed: {len(result.steps_executed)}")
for step in result.steps_executed:
    print(f"  {step['action']}: {step.get('status', 'unknown')}")
```

### Monitoring

```python
# Add monitoring checks
agent.add_monitor_check("sales", MonitorCheck(
    name="min_rows",
    check_type="row_count_min",
    parameters={"min": 1000},
    severity=Severity.HIGH,
))

agent.add_monitor_check("sales", MonitorCheck(
    name="email_nulls",
    check_type="null_percentage",
    parameters={"column": "email", "max_percentage": 5.0},
    severity=Severity.MEDIUM,
))

agent.add_monitor_check("sales", MonitorCheck(
    name="data_freshness",
    check_type="freshness",
    parameters={"timestamp_column": "created_at", "max_age_hours": 24},
    severity=Severity.CRITICAL,
))

# Run checks
results = agent.run_monitor_checks("sales")
for r in results:
    icon = "PASS" if r.status.value == "pass" else "FAIL"
    print(f"[{icon}] {r.check_name}: {r.message}")
```

### Quality Scoring

```python
# Compute composite score
score = agent.compute_quality_score("sales")
print(f"Overall: {score.overall:.2%}")
print(f"Completeness: {score.completeness:.2%}")
print(f"Validity: {score.validity:.2%}")
print(f"Uniqueness: {score.uniqueness:.2%}")
```

### Reporting

```python
# Full assessment report
report = agent.assess_quality("sales")

# Export as JSON
json_output = agent.export_report(report, "json")

# Export as summary text
summary = agent.export_report(report, "summary")
print(summary)

# Access report components
print(f"Score: {report.score.to_dict()}")
print(f"Issues: {len(report.issues)}")
print(f"Anomalies: {len(report.anomalies)}")
```

---

## API Reference

### DataQualityAgent

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `register_dataset` | name, data | Dict | Register a dataset for analysis |
| `get_dataset` | name | List[Dict] | Retrieve a registered dataset |
| `profile_dataset` | name | DatasetProfile | Generate statistical profile |
| `add_rule` | rule | str (rule_id) | Add a validation rule |
| `remove_rule` | rule_id | bool | Remove a validation rule |
| `list_rules` | - | List[Dict] | List all active rules |
| `validate_dataset` | name | List[QualityIssue] | Run validation rules |
| `compute_quality_score` | name | QualityScore | Compute composite score |
| `detect_anomalies` | name, column, method, **kwargs | AnomalyResult | Detect outliers |
| `create_cleansing_pipeline` | name, steps | Dict | Create a cleansing pipeline |
| `run_cleansing_pipeline` | dataset_name, pipeline_name | CleansingResult | Execute a pipeline |
| `add_monitor_check` | dataset_name, check | str (check_id) | Add a monitoring check |
| `run_monitor_checks` | dataset_name | List[MonitorResult] | Execute monitoring checks |
| `assess_quality` | name | QualityReport | Full quality assessment |
| `get_status` | - | Dict | Agent status summary |
| `export_report` | report, format | str | Export report (json/summary) |

### DataQualityConfig

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `zscore_threshold` | float | 3.0 | Z-score anomaly threshold |
| `iqr_multiplier` | float | 1.5 | IQR outlier multiplier |
| `mad_threshold` | float | 3.5 | MAD anomaly threshold |
| `percentile_lower` | float | 1.0 | Lower percentile bound |
| `percentile_upper` | float | 99.0 | Upper percentile bound |
| `ewm_span` | int | 20 | EWM moving average span |
| `ewm_threshold` | float | 3.0 | EWM anomaly threshold |
| `null_threshold_warn` | float | 0.05 | Null % warning threshold |
| `null_threshold_fail` | float | 0.20 | Null % failure threshold |
| `enable_entropy_calculation` | bool | True | Compute Shannon entropy |
| `enable_skewness_kurtosis` | bool | True | Compute distribution shape |
| `enable_pattern_detection` | bool | True | Detect string patterns |
| `pii_patterns` | Dict | (built-in) | PII detection patterns |
| `dimension_weights` | Dict | (balanced) | Quality dimension weights |

---

## Examples

### Example 1: Customer Data Quality Audit

```python
agent = DataQualityAgent()

# Register customer data
customers = [
    {"id": 1, "name": "Alice", "email": "alice@co.com", "phone": "555-0101", "age": 30},
    {"id": 2, "name": "Bob", "email": None, "phone": "555-0102", "age": 25},
    {"id": 3, "name": "Charlie", "email": "charlie@co.com", "phone": None, "age": 35},
    {"id": 4, "name": "  Alice  ", "email": "alice@co.com", "phone": "555-0101", "age": 30},
]
agent.register_dataset("customers", customers)

# Define comprehensive rules
rules = [
    ValidationRule(name="id_unique", dimension=QualityDimension.UNIQUENESS,
                   severity=Severity.CRITICAL, column="id", rule_type="unique"),
    ValidationRule(name="email_not_null", dimension=QualityDimension.COMPLETENESS,
                   severity=Severity.HIGH, column="email", rule_type="not_null"),
    ValidationRule(name="email_valid", dimension=QualityDimension.VALIDITY,
                   severity=Severity.HIGH, column="email",
                   rule_type="regex", parameters={"pattern": r"[^@]+@[^@]+\.[^@]+"}),
    ValidationRule(name="age_range", dimension=QualityDimension.ACCURACY,
                   severity=Severity.MEDIUM, column="age",
                   rule_type="range", parameters={"min": 0, "max": 150}),
]
for rule in rules:
    agent.add_rule(rule)

# Full assessment
report = agent.assess_quality("customers")
print(f"Quality: {report.score.overall:.2%} ({report.summary['quality_grade']})")
```

### Example 2: Sales Anomaly Detection

```python
# Detect revenue anomalies with multiple methods
for method in [AnomalyMethod.ZSCORE, AnomalyMethod.IQR, AnomalyMethod.MAD]:
    result = agent.detect_anomalies("sales", "revenue", method)
    print(f"{method.value}: {result.anomaly_count} anomalies")
    if result.anomaly_count > 0:
        print(f"  Values: {result.values[:3]}")
```

### Example 3: Automated Cleansing

```python
# Multi-step cleansing pipeline
steps = [
    CleansingStep(action=CleansingAction.TRIM_WHITESPACE, column="name", order=1),
    CleansingStep(action=CleansingAction.LOWERCASE, column="email", order=2),
    CleansingStep(action=CleansingAction.FILL_MEDIAN, column="revenue", order=3),
    CleansingStep(action=CleansingAction.CLIP, column="age",
                  parameters={"min": 0, "max": 120}, order=4),
    CleansingStep(action=CleansingAction.DEDUPLICATE, order=5),
]
agent.create_cleansing_pipeline("standardize", steps)
result = agent.run_cleansing_pipeline("sales", "standardize")
print(f"Cleaned: {result.rows_before} → {result.rows_after} rows")
```

---

## Configuration

### Default Configuration

```python
config = DataQualityConfig(
    zscore_threshold=3.0,
    iqr_multiplier=1.5,
    mad_threshold=3.5,
    percentile_lower=1.0,
    percentile_upper=99.0,
    ewm_span=20,
    ewm_threshold=3.0,
    null_threshold_warn=0.05,
    null_threshold_fail=0.20,
    enable_entropy_calculation=True,
    enable_skewness_kurtosis=True,
    enable_pattern_detection=True,
    dimension_weights={
        "completeness": 0.20,
        "accuracy": 0.20,
        "consistency": 0.15,
        "timeliness": 0.10,
        "validity": 0.20,
        "uniqueness": 0.15,
    },
)
agent = DataQualityAgent(config)
```

### Custom PII Patterns

```python
config = DataQualityConfig(
    pii_patterns={
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"\+?[\d\-\(\)\s]{7,15}",
        "employee_id": r"EMP\d{6}",
    }
)
```

---

## Best Practices

1. **Profile before validating** — Understanding your data shape first makes rule creation more effective
2. **Start with critical rules** — Focus on not_null and unique for primary keys first
3. **Use appropriate anomaly methods** — Z-Score for normal data, IQR for skewed, MAD for heavy tails
4. **Order cleansing steps carefully** — Trim → Standardize → Fill → Deduplicate
5. **Run validation before and after cleansing** — Measure the improvement quantitatively
6. **Set up monitoring early** — Catch quality degradation before it propagates
7. **Review quality grades regularly** — Track trends over time
8. **Protect PII proactively** — Use hash_pii or mask_pii in cleansing pipelines
9. **Customize dimension weights** — Adjust based on your domain's priorities
10. **Export and archive reports** — Maintain audit trails of quality assessments

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `KeyError: Dataset not found` | Register the dataset first with `register_dataset` |
| Validation returns no issues | Check `rule.enabled = True` and verify column names match exactly |
| Anomaly detection finds nothing | Lower the threshold or try a different method |
| Cleansing modifies unexpected rows | Review step conditions and order; test on sample first |
| Low quality score | Check `report.summary` for which dimensions are low; review specific issues |
| `TypeError` in profiling | Ensure numeric columns contain actual numbers, not strings |
| Monitor checks always pass | Verify check parameters match your data schema |

---

## Contributing

Contributions welcome. Please follow these guidelines:

1. Add new validation rule types in `_apply_rule` with corresponding enum values
2. Add new anomaly methods with statistical justification
3. Add new cleansing actions with before/after examples
4. Add new monitor check types with parameter documentation
5. Include type hints for all new methods
6. Add comprehensive docstrings for public APIs
7. Test edge cases: empty datasets, single-row datasets, all-null columns

---

## License

MIT License — See [LICENSE](../../LICENSE) for details.

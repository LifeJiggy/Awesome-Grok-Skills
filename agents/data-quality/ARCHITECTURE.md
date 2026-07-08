# Data Quality Agent — System Architecture

## Overview

The Data Quality Agent is a modular, enterprise-grade system for data validation, profiling, cleansing, continuous monitoring, anomaly detection, and composite quality scoring. It processes tabular datasets through a pipeline of pluggable components, each operating independently yet sharing a unified data model.

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                       DATA QUALITY AGENT                             │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  INGESTION   │  │  PROFILING   │  │  VALIDATION  │              │
│  │   LAYER      │──│   ENGINE     │──│   ENGINE     │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                  │                       │
│         ▼                 ▼                  ▼                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │  ANOMALY     │  │  CLEANSING   │  │  MONITORING  │              │
│  │  DETECTOR    │──│  PIPELINE    │──│  SERVICE     │              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                  │                       │
│         └────────┬────────┴────────┬─────────┘                      │
│                  ▼                 ▼                                  │
│         ┌──────────────┐  ┌──────────────┐                          │
│         │   SCORING    │  │   REPORTING  │                          │
│         │   ENGINE     │──│   SERVICE    │                          │
│         └──────────────┘  └──────────────┘                          │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    CONFIGURATION LAYER                        │   │
│  │  Thresholds · Patterns · Weights · Rules · Pipelines         │   │
│  └──────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
┌─────────┐    ┌─────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐
│  Raw     │───▶│ Register│───▶│  Profile  │───▶│ Validate │───▶│  Score   │
│  Data    │    │ Dataset │    │  Columns  │    │  Rules   │    │  Overall │
└─────────┘    └─────────┘    └───────────┘    └──────────┘    └──────────┘
                                     │                │              │
                                     ▼                ▼              ▼
                               ┌───────────┐    ┌──────────┐    ┌──────────┐
                               │  Column   │    │  Issues  │    │  Report  │
                               │ Profiles  │    │  Found   │    │  Output  │
                               └───────────┘    └──────────┘    └──────────┘
                                                        │
                                                        ▼
                                                  ┌──────────┐
                                                  │ Anomaly  │
                                                  │ Detection│
                                                  └──────────┘
                                                        │
                                                        ▼
                                                  ┌──────────┐
                                                  │ Cleansing│
                                                  │ Pipeline │
                                                  └──────────┘
                                                        │
                                                        ▼
                                                  ┌──────────┐
                                                  │ Monitor  │
                                                  │ Checks   │
                                                  └──────────┘
```

---

## Component Deep Dives

### 1. Ingestion Layer

The ingestion layer handles dataset registration, storage, and retrieval. Datasets are stored as lists of dictionaries in an in-memory store keyed by name.

```
┌─────────────────────────────────────┐
│          INGESTION LAYER            │
├─────────────────────────────────────┤
│                                     │
│  register_dataset(name, data)       │
│       │                             │
│       ▼                             │
│  ┌──────────┐   ┌──────────────┐   │
│  │  Schema  │──▶│   Dataset    │   │
│  │  Check   │   │   Store      │   │
│  └──────────┘   └──────────────┘   │
│                                     │
│  get_dataset(name)                  │
│  list_datasets()                    │
│  remove_dataset(name)               │
└─────────────────────────────────────┘
```

**Responsibilities:**
- Validate input data structure (list of dicts)
- Store datasets in memory with name-based access
- Support streaming ingestion via generator-based registration
- Maintain dataset metadata (row count, column names, registration timestamp)

### 2. Profiling Engine

The profiling engine analyzes each column to produce statistical summaries. It auto-detects column types and computes type-specific metrics.

```
┌──────────────────────────────────────────────────────────┐
│                    PROFILING ENGINE                       │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Input: Column values[]                                  │
│       │                                                  │
│       ▼                                                  │
│  ┌────────────┐                                          │
│  │   Type     │  Detect NUMERIC / TEXT / BOOLEAN /       │
│  │  Detector  │  DATETIME / CATEGORICAL                  │
│  └─────┬──────┘                                          │
│        │                                                 │
│        ▼                                                 │
│  ┌──────────────────────────────────────┐                │
│  │        Column Profile Computation     │                │
│  │                                       │                │
│  │  NUMERIC: min, max, mean, median,    │                │
│  │    std_dev, variance, skewness,      │                │
│  │    kurtosis, percentiles, IQR        │                │
│  │                                       │                │
│  │  TEXT: avg_length, min_length,       │                │
│  │    max_length, top_values,           │                │
│  │    pattern_distribution, entropy     │                │
│  │                                       │                │
│  │  ALL: null_count, distinct_count,    │                │
│  │    cardinality_ratio                 │                │
│  └──────────────────────────────────────┘                │
│        │                                                 │
│        ▼                                                 │
│  ┌──────────────┐                                        │
│  │ Dataset      │  Aggregate column profiles into        │
│  │ Profile      │  a complete dataset profile            │
│  └──────────────┘                                        │
└──────────────────────────────────────────────────────────┘
```

**Type Detection Heuristic:**
- If > 50% of non-null values are numeric → `NUMERIC`
- Otherwise → `TEXT` (with sub-analysis for dates, booleans, categories)

**Statistical Metrics per Column:**

| Metric | NUMERIC | TEXT | Description |
|--------|---------|------|-------------|
| null_count | Yes | Yes | Count of null/empty values |
| distinct_count | Yes | Yes | Number of unique values |
| min/max | Yes | Yes | Extremes |
| mean/median/std | Yes | No | Central tendency and spread |
| skewness/kurtosis | Yes | No | Distribution shape |
| percentiles | Yes | No | 25th, 75th, IQR |
| avg_length | No | Yes | Average string length |
| top_values | Yes | Yes | Most frequent values |
| pattern_distribution | No | Yes | Detected character patterns |
| entropy | Yes | Yes | Shannon entropy |
| cardinality_ratio | Yes | Yes | distinct/total ratio |

### 3. Validation Engine

The validation engine applies a configurable set of rules to datasets and produces quality issues.

```
┌──────────────────────────────────────────────────────────┐
│                  VALIDATION ENGINE                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Rules[] ─────────────────────────────┐                  │
│       │                               │                  │
│       ▼                               ▼                  │
│  ┌──────────────┐          ┌──────────────────┐         │
│  │  Rule Filter │          │  Dataset Rows    │         │
│  │  (enabled?)  │          │                  │         │
│  └──────┬───────┘          └────────┬─────────┘         │
│         │                           │                    │
│         ▼                           ▼                    │
│  ┌──────────────────────────────────────────┐            │
│  │           Rule Application               │            │
│  │                                          │            │
│  │  not_null ──────▶ Check for null/empty   │            │
│  │  unique ────────▶ Check for duplicates   │            │
│  │  regex ─────────▶ Pattern matching       │            │
│  │  range ─────────▶ Numeric bounds check   │            │
│  │  allowed_values ▶ Enum validation        │            │
│  │  custom ────────▶ User-provided function │            │
│  └──────────────────────────────────────────┘            │
│         │                                                │
│         ▼                                                │
│  ┌──────────────────┐                                    │
│  │  Quality Issues   │  Severity · Dimension · Message   │
│  └──────────────────┘                                    │
└──────────────────────────────────────────────────────────┘
```

**Rule Types:**

| Rule Type | Parameters | Description |
|-----------|-----------|-------------|
| `not_null` | column | Fails if column has null/empty values |
| `unique` | column | Fails if column has duplicate values |
| `regex` | column, pattern | Fails if values don't match regex |
| `range` | column, min, max | Fails if values outside [min, max] |
| `allowed_values` | column, values[] | Fails if value not in allowed set |
| `custom` | function | Fails if user function returns False |

**Severity Levels:**

| Level | Description | Impact |
|-------|-------------|--------|
| CRITICAL | Data corruption, compliance violation | Immediate action required |
| HIGH | Significant quality degradation | Action within 24 hours |
| MEDIUM | Moderate quality concern | Scheduled remediation |
| LOW | Minor quality observation | Informational |
| INFO | No quality impact | Awareness only |

### 4. Anomaly Detector

The anomaly detector identifies statistical outliers in numeric columns using multiple methods.

```
┌──────────────────────────────────────────────────────────┐
│                   ANOMALY DETECTOR                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Column Values[] ──────────────────────┐                 │
│       │                               │                 │
│       ▼                               │                 │
│  ┌──────────────────────────────┐     │                 │
│  │     Method Router            │     │                 │
│  │                              │     │                 │
│  │  ZSCORE ──────▶ Z-score     │     │                 │
│  │  IQR ─────────▶ IQR bounds  │     │                 │
│  │  MAD ─────────▶ Median AD   │     │                 │
│  │  EWM_STD ────▶ EWMA sigma   │     │                 │
│  │  PERCENTILE ──▶ P1/P99      │     │                 │
│  └──────────────────────────────┘     │                 │
│       │                               │                 │
│       ▼                               │                 │
│  ┌──────────────────────────────┐     │                 │
│  │   Threshold Evaluation       │◀────┘                 │
│  │   Compute anomaly indices    │                       │
│  └──────────────────────────────┘                       │
│       │                                                 │
│       ▼                                                 │
│  ┌──────────────────────────────┐                       │
│  │   AnomalyResult              │                       │
│  │   indices · values · stats   │                       │
│  └──────────────────────────────┘                       │
└──────────────────────────────────────────────────────────┘
```

**Method Comparison:**

| Method | Best For | Sensitivity | Breakdown Resistance |
|--------|----------|-------------|---------------------|
| Z-Score | Normal distributions | Moderate | Low (mean/std sensitive) |
| IQR | Skewed distributions | Moderate | High (median-based) |
| MAD | Heavy-tailed distributions | High | Very high (median + MAD) |
| EWM-STD | Time-series data | Adaptive | Moderate |
| Percentile | Uniform distributions | Low | High |

### 5. Cleansing Pipeline

The cleansing pipeline applies an ordered sequence of data transformation steps.

```
┌──────────────────────────────────────────────────────────┐
│                  CLEANSING PIPELINE                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Pipeline Steps (ordered by step.order)                  │
│       │                                                  │
│       ▼                                                  │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌────────┐  │
│  │ Step 1  │──▶│ Step 2  │──▶│ Step 3  │──▶│  ...   │  │
│  │TRIM     │   │FILL     │   │DEDUP    │   │        │  │
│  │WHITESPC │   │NULLS    │   │         │   │        │  │
│  └─────────┘   └─────────┘   └─────────┘   └────────┘  │
│       │                                                  │
│       ▼                                                  │
│  ┌──────────────────────────────┐                       │
│  │   CleansingResult            │                       │
│  │   rows_before/after          │                       │
│  │   steps_executed[]           │                       │
│  │   columns_affected[]         │                       │
│  │   warnings[]                 │                       │
│  └──────────────────────────────┘                       │
└──────────────────────────────────────────────────────────┘
```

**Supported Actions:**

| Action | Description | Column Required |
|--------|-------------|----------------|
| `drop_rows` | Remove rows with null/empty values | Optional |
| `fill_mean` | Replace nulls with column mean | Yes |
| `fill_median` | Replace nulls with column median | Yes |
| `fill_mode` | Replace nulls with column mode | Yes |
| `fill_value` | Replace nulls with a fixed value | Yes |
| `trim_whitespace` | Strip leading/trailing whitespace | Yes |
| `lowercase` | Convert strings to lowercase | Yes |
| `uppercase` | Convert strings to uppercase | Yes |
| `regex_replace` | Pattern-based replacement | Yes |
| `deduplicate` | Remove exact duplicate rows | No |
| `type_cast` | Convert column type | Yes |
| `clip` | Bound values to min/max range | Yes |
| `hash_pii` | Hash PII fields with SHA-256 | Yes |
| `mask_pii` | Mask PII fields showing last N chars | Yes |

### 6. Monitoring Service

The monitoring service provides continuous quality checks with configurable alerting.

```
┌──────────────────────────────────────────────────────────┐
│                  MONITORING SERVICE                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Monitor Checks[] ─────────────────────┐                 │
│       │                                │                 │
│       ▼                                │                 │
│  ┌──────────────────────────────┐      │                 │
│  │   Check Type Router          │      │                 │
│  │                              │      │                 │
│  │  row_count_min ──▶ MIN rows │      │                 │
│  │  row_count_max ──▶ MAX rows │      │                 │
│  │  null_percentage ▶ col NULLs│      │                 │
│  │  freshness ──────▶ Time lag │      │                 │
│  │  schema_match ───▶ Columns  │      │                 │
│  │  custom ─────────▶ Function │      │                 │
│  └──────────────────────────────┘      │                 │
│       │                                │                 │
│       ▼                                │                 │
│  ┌──────────────────────────────┐      │                 │
│  │   MonitorResult              │      │                 │
│  │   PASS / WARN / FAIL / ERROR │◀─────┘                 │
│  └──────────────────────────────┘                       │
│                                                          │
│  History tracking per dataset                            │
└──────────────────────────────────────────────────────────┘
```

**Check Types:**

| Type | Parameters | Trigger Condition |
|------|-----------|-------------------|
| `row_count_min` | min | Row count < min → FAIL |
| `row_count_max` | max | Row count > max → WARN |
| `null_percentage` | column, max_percentage | Null% > max → FAIL |
| `freshness` | timestamp_column, max_age_hours | Age > max_hours → FAIL |
| `schema_match` | columns[] | Missing expected columns → FAIL |
| `custom` | function | Function returns {pass: false} → FAIL |

### 7. Scoring Engine

The scoring engine computes a composite quality score using weighted dimensions.

```
┌──────────────────────────────────────────────────────────┐
│                    SCORING ENGINE                          │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌───────────┐  ┌──────────┐  ┌───────────┐            │
│  │Completeness│  │ Validity │  │Uniqueness │  ...       │
│  │  0.20     │  │   0.20   │  │   0.15    │            │
│  └─────┬─────┘  └────┬─────┘  └─────┬─────┘            │
│        │             │              │                    │
│        ▼             ▼              ▼                    │
│  ┌──────────────────────────────────────────────┐       │
│  │        Weighted Average Computation          │       │
│  │                                              │       │
│  │  overall = Σ(dimension_score × weight)       │       │
│  │            ─────────────────────────         │       │
│  │                   Σ(weights)                 │       │
│  └──────────────────────────────────────────────┘       │
│        │                                                 │
│        ▼                                                 │
│  ┌──────────────┐                                        │
│  │  Quality     │  Grade: A+ (≥0.95) ... F (<0.50)     │
│  │  Score       │  Overall + per-dimension breakdown    │
│  └──────────────┘                                        │
└──────────────────────────────────────────────────────────┘
```

**Default Dimension Weights:**

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Completeness | 0.20 | Missing data impacts all downstream processes |
| Accuracy | 0.20 | Incorrect data leads to wrong decisions |
| Validity | 0.20 | Invalid data violates business rules |
| Consistency | 0.15 | Inconsistent data causes confusion |
| Uniqueness | 0.15 | Duplicates inflate metrics and cause errors |
| Timeliness | 0.10 | Staleness matters less for most datasets |

**Grading Scale:**

| Grade | Score Range | Interpretation |
|-------|------------|----------------|
| A+ | ≥ 0.95 | Excellent |
| A | ≥ 0.90 | Very Good |
| A- | ≥ 0.85 | Good |
| B+ | ≥ 0.80 | Above Average |
| B | ≥ 0.75 | Average |
| B- | ≥ 0.70 | Below Average |
| C+ | ≥ 0.65 | Poor |
| C | ≥ 0.60 | Very Poor |
| D | ≥ 0.50 | Critical |
| F | < 0.50 | Failing |

### 8. Reporting Service

The reporting service assembles all components into a comprehensive `QualityReport`.

```
┌──────────────────────────────────────────────────────────┐
│                   REPORTING SERVICE                        │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────┐  ┌────────┐  ┌───────────┐  ┌────────┐ │
│  │  Profile   │  │ Issues │  │ Anomalies │  │Monitor │ │
│  │  Data      │  │  Data  │  │  Data     │  │Results │ │
│  └─────┬──────┘  └───┬────┘  └─────┬─────┘  └───┬────┘ │
│        │             │             │             │       │
│        └──────┬──────┴──────┬──────┴──────┬──────┘       │
│               ▼             ▼             ▼               │
│  ┌──────────────────────────────────────────────────┐   │
│  │              QualityReport                        │   │
│  │  score + profile + issues + anomalies +           │   │
│  │  monitor_results + cleansing_result + summary     │   │
│  └──────────────────────────────────────────────────┘   │
│        │                                                 │
│        ▼                                                 │
│  ┌──────────────┐  ┌──────────────┐                     │
│  │ JSON Export  │  │ Summary Text │                     │
│  └──────────────┘  └──────────────┘                     │
└──────────────────────────────────────────────────────────┘
```

---

## Design Patterns

### Strategy Pattern
Anomaly detection methods (Z-Score, IQR, MAD, EWM, Percentile) implement a common interface. New methods can be added by extending the `AnomalyMethod` enum and implementing a detection function.

### Pipeline Pattern
Cleansing operations are defined as ordered steps executed sequentially. Each step is independent and composable.

### Observer Pattern
Monitor checks produce `MonitorResult` objects that can be consumed by alerting systems, dashboards, or downstream pipelines.

### Builder Pattern
Quality reports are assembled incrementally from profiling, validation, anomaly detection, monitoring, and scoring components.

---

## Data Models

### Core Data Flow

```
Raw Data (List[Dict])
    │
    ▼
DatasetProfile (per-column ColumnProfile objects)
    │
    ▼
List[QualityIssue] (validation findings)
    │
    ▼
List[AnomalyResult] (statistical outliers)
    │
    ▼
QualityScore (weighted composite)
    │
    ▼
QualityReport (complete assessment)
```

### Quality Issue Lifecycle

```
Created ──▶ Classified ──▶ Scored ──▶ Reported
   │            │             │           │
   ▼            ▼             ▼           ▼
Rule match  Dimension    Severity    Export to
trigger     assignment   assignment  downstream
```

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.10+ | Core implementation |
| Type System | Dataclasses + Enum | Data modeling |
| Statistics | Standard library | Mean, median, stdev, variance |
| Hashing | hashlib | PII hashing (SHA-256) |
| Pattern Matching | re (regex) | Rule validation, pattern detection |
| Serialization | json | Report export |
| Logging | logging | Operational observability |

---

## Security Considerations

### Data Protection
- PII detection via configurable regex patterns (email, phone, SSN, credit card, IP)
- PII hashing with SHA-256 for irreversible anonymization
- PII masking showing only last N characters for display

### Access Control
- Dataset access gated by name-based lookup (raises `KeyError` on missing)
- Rule management requires explicit registration
- Cleansing pipelines require explicit creation and execution

### Injection Prevention
- Custom rule functions executed with `__builtins__` restricted in eval
- Regex patterns compiled (not evaluated as code)
- No dynamic code execution outside controlled eval contexts

---

## Scalability Considerations

### Memory
- In-memory dataset storage suitable for datasets up to ~10M rows
- Streaming profiling support for column-by-column processing
- Configurable sample sizes for pattern detection

### Parallelism
- Column profiling is embarrassingly parallel (each column independent)
- Validation rules execute independently per rule
- Anomaly detection per column can be distributed

### Extensibility
- New validation rule types via `_apply_rule` dispatch
- New anomaly methods via `AnomalyMethod` enum extension
- New cleansing actions via `CleansingAction` enum extension
- Custom monitor checks via function parameters

---

## Error Handling

```
┌─────────────────────────────────────────────────────────┐
│                  ERROR HANDLING STRATEGY                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  KeyError ─────▶ Dataset not found                       │
│  ValueError ───▶ Invalid configuration parameters       │
│  TypeError ────▶ Non-numeric values in numeric ops      │
│  Exception ────▶ Rule execution failure → logged +      │
│                  wrapped as QualityIssue                 │
│                                                          │
│  All errors logged with context (dataset, rule, column) │
│  Graceful degradation: partial results returned          │
│  with warnings list in CleansingResult                   │
└─────────────────────────────────────────────────────────┘
```

---

## Testing Strategy

### Unit Tests
- Column profiling with known distributions
- Each validation rule type with edge cases
- Anomaly detection with synthetic outliers
- Cleansing pipeline step-by-step verification
- Score computation with weighted dimensions

### Integration Tests
- Full assessment pipeline: register → profile → validate → score → report
- Cleansing pipeline modifying dataset and re-profiling
- Monitor check execution with history tracking
- Export format verification (JSON, summary text)

### Property-Based Tests
- Profiling results consistent across data orderings
- Validation issues count matches actual violations
- Anomaly indices correspond to extreme values
- Score always in [0.0, 1.0] range

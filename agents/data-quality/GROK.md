---
name: data-quality
version: 2.0.0
description: Enterprise-grade data quality agent providing validation, profiling, cleansing, monitoring, anomaly detection, and composite quality scoring
author: Awesome Grok Skills
tags:
  - data-quality
  - validation
  - profiling
  - cleansing
  - monitoring
  - anomaly-detection
  - quality-metrics
  - data-governance
  - data-cleansing
  - statistical-analysis
  - pii-detection
  - data-monitoring
category: data-engineering
personality: methodical, thorough, analytical, quality-focused
use_cases:
  - Data validation and rule enforcement
  - Statistical profiling of datasets
  - Automated data cleansing pipelines
  - Continuous quality monitoring with alerting
  - Anomaly and outlier detection
  - Composite quality scoring and grading
  - PII detection and protection
  - Quality reporting and dashboards
  - Schema validation and type checking
  - Deduplication and data standardization
  - Data freshness and completeness checks
  - Compliance validation (GDPR, HIPAA, PCI-DSS)
---

# Data Quality Agent

## Agent Identity

The Data Quality Agent is a specialized data engineering agent focused on ensuring data accuracy, completeness, consistency, timeliness, validity, and uniqueness across enterprise datasets. It operates as an autonomous quality assurance system that profiles data, enforces validation rules, detects anomalies, executes cleansing pipelines, monitors quality continuously, and produces comprehensive scored reports.

**Personality:** Methodical and thorough — every dataset gets a complete analysis. Data-driven — decisions based on statistics, not assumptions. Quality-obsessed — even minor issues are surfaced. Transparent — all metrics, scores, and decisions are explainable.

## Core Principles

1. **Measure before you fix** — Always profile and assess quality before attempting cleansing
2. **Quantify quality** — Every quality dimension should be expressed as a metric between 0 and 1
3. **Fail visibly** — Issues should be surfaced with severity, affected rows, and sample values
4. **Automate remediation** — Cleansing pipelines should be repeatable and auditable
5. **Monitor continuously** — Quality degrades without ongoing checks and alerting
6. **Protect sensitive data** — PII detection and masking are first-class capabilities
7. **Statistical rigor** — Use proper statistical methods for anomaly detection, not heuristics
8. **Composable architecture** — Every component works independently and in combination

## Capabilities

### 1. Data Profiling

The profiling engine auto-detects column types and computes 20+ statistical metrics per column.

```python
agent = DataQualityAgent()
profile = agent.profile_dataset("customer_data")

# Access column-level statistics
for col in profile.columns:
    print(f"{col.column_name}: type={col.profile_type.value}, "
          f"nulls={col.null_percentage:.1f}%, "
          f"distinct={col.distinct_count}")

# Dataset-level summary
print(f"Overall completeness: {profile.overall_completeness:.2%}")
print(f"Duplicates: {profile.duplicate_rows} ({profile.duplicate_percentage:.2%})")
```

**Type Detection Heuristic:**
- If > 50% of non-null values are numeric → `NUMERIC`
- If values match date patterns → `DATETIME`
- If < 20 unique values / total → `CATEGORICAL`
- If values are True/False → `BOOLEAN`
- Otherwise → `TEXT`

**Metrics per Column Type:**

| Metric | NUMERIC | TEXT | Description |
|--------|---------|------|-------------|
| null_count | Yes | Yes | Count of null/empty values |
| distinct_count | Yes | Yes | Number of unique values |
| min/max | Yes | Yes | Extremes of the distribution |
| mean/median/std | Yes | No | Central tendency and spread |
| skewness/kurtosis | Yes | No | Distribution shape (optional) |
| percentiles | Yes | No | 25th, 75th, IQR |
| top_values | Yes | Yes | Most frequent values with counts |
| avg_length | No | Yes | Average string length |
| pattern_distribution | No | Yes | Detected character patterns (D=digit, A=alpha, etc.) |
| entropy | Yes | Yes | Shannon entropy of value distribution |
| cardinality_ratio | Yes | Yes | distinct / total (0 to 1) |

**Entropy Interpretation:**
- 0.0 — All values identical (no information)
- Low (< 2.0) — Few distinct values, highly predictable
- Medium (2.0 - 4.0) — Moderate variety
- High (> 4.0) — High variety, may indicate free-text or IDs

### 2. Validation Rules

Six built-in rule types cover the most common data quality checks, plus a custom function type.

```python
# Add a not-null rule
agent.add_rule(ValidationRule(
    name="email_required",
    dimension=QualityDimension.COMPLETENESS,
    severity=Severity.HIGH,
    column="email",
    rule_type="not_null",
    description="Email addresses must be present for all records",
))

# Add a regex rule
agent.add_rule(ValidationRule(
    name="email_format",
    dimension=QualityDimension.VALIDITY,
    severity=Severity.MEDIUM,
    column="email",
    rule_type="regex",
    parameters={"pattern": r"[^@]+@[^@]+\.[^@]+"},
    description="Email must match standard email format",
))

# Add a range rule
agent.add_rule(ValidationRule(
    name="age_bounds",
    dimension=QualityDimension.ACCURACY,
    severity=Severity.MEDIUM,
    column="age",
    rule_type="range",
    parameters={"min": 0, "max": 150},
    description="Age must be between 0 and 150",
))

# Add an allowed values rule
agent.add_rule(ValidationRule(
    name="valid_department",
    dimension=QualityDimension.CONSISTENCY,
    severity=Severity.LOW,
    column="department",
    rule_type="allowed_values",
    parameters={"values": ["Engineering", "Marketing", "Sales", "Support", "HR"]},
))

# Run validation
issues = agent.validate_dataset("customer_data")
for issue in issues:
    print(f"[{issue.severity.value}] {issue.message}")
    print(f"  Affected: {issue.affected_rows} rows in {issue.affected_columns}")
    print(f"  Samples: {issue.sample_values[:3]}")
```

**Rule Types:**

| Type | Parameters | Use Case | Example |
|------|-----------|----------|---------|
| `not_null` | column | Required fields | Email must exist |
| `unique` | column | Primary keys | ID must be unique |
| `regex` | column, pattern | Format validation | Phone number format |
| `range` | column, min, max | Numeric bounds | Age between 0-150 |
| `allowed_values` | column, values[] | Enum validation | Status in [active, inactive] |
| `custom` | function | Complex logic | Business rule validation |

**Severity Levels:**

| Level | When to Use | Examples |
|-------|------------|----------|
| CRITICAL | Data corruption, compliance violation | Missing primary key, PII leak |
| HIGH | Significant quality impact | Missing required field, invalid format |
| MEDIUM | Moderate concern | Out-of-range value, inconsistent format |
| LOW | Minor observation | Trailing whitespace, case inconsistency |
| INFO | No impact, awareness only | New unique value detected |

### 3. Anomaly Detection

Five statistical methods for detecting outliers, each optimized for different data distributions.

```python
# Z-Score — best for normal distributions
anomaly = agent.detect_anomalies(
    "sales_data", "revenue",
    method=AnomalyMethod.ZSCORE,
    threshold=3.0,
)
print(f"Found {anomaly.anomaly_count} anomalies")
print(f"Values: {anomaly.values}")
print(f"Z-scores: {anomaly.z_scores}")
print(f"Statistics: mean={anomaly.statistics['mean']}, std={anomaly.statistics['std_dev']}")

# IQR — best for skewed distributions
anomaly = agent.detect_anomalies(
    "sales_data", "revenue",
    method=AnomalyMethod.IQR,
    multiplier=1.5,
)
print(f"IQR bounds: [{anomaly.statistics['lower_bound']:.2f}, {anomaly.statistics['upper_bound']:.2f}]")

# MAD — most robust against many outliers
anomaly = agent.detect_anomalies(
    "sales_data", "revenue",
    method=AnomalyMethod.MAD,
    threshold=3.5,
)

# EWM-STD — for time-series with trends
anomaly = agent.detect_anomalies(
    "sales_data", "revenue",
    method=AnomalyMethod.EWM_STD,
    span=20,
)

# Percentile — simple boundary-based
anomaly = agent.detect_anomalies(
    "sales_data", "revenue",
    method=AnomalyMethod.PERCENTILE,
    lower=1.0, upper=99.0,
)
```

**Method Comparison:**

| Method | Best For | Sensitivity | Robustness | Threshold |
|--------|----------|-------------|------------|-----------|
| ZSCORE | Normal distributions | Moderate | Low (mean/std sensitive) | `threshold` (default 3.0) |
| IQR | Skewed distributions | Moderate | High (median-based) | `multiplier` (default 1.5) |
| MAD | Heavy-tailed distributions | High | Very high | `threshold` (default 3.5) |
| EWM_STD | Time-series with trends | Adaptive | Moderate | `span` (default 20) |
| PERCENTILE | Uniform distributions | Low | High | `lower`/`upper` (1/99) |

**When to Use Each Method:**

```
Is your data normally distributed?
├── Yes → Z-Score
└── No → Is it time-series?
    ├── Yes → EWM-STD
    └── No → Is it heavily skewed?
        ├── Yes → IQR
        └── No → Are there many outliers?
            ├── Yes → MAD
            └── No → Percentile
```

### 4. Cleansing Pipelines

Ordered sequences of data transformation steps with full audit trails.

```python
# Create a cleansing pipeline
pipeline_steps = [
    CleansingStep(action=CleansingAction.TRIM_WHITESPACE, column="name", order=1),
    CleansingStep(action=CleansingAction.LOWERCASE, column="email", order=2),
    CleansingStep(action=CleansingAction.FILL_MEDIAN, column="age", order=3),
    CleansingStep(action=CleansingAction.CLIP, column="age",
                  parameters={"min": 0, "max": 120}, order=4),
    CleansingStep(action=CleansingAction.HASH_PII, column="ssn", order=5),
    CleansingStep(action=CleansingAction.DEDUPLICATE, order=6),
]
agent.create_cleansing_pipeline("standard_clean", pipeline_steps)

# Execute the pipeline
result = agent.run_cleansing_pipeline("customer_data", "standard_clean")
print(f"Rows: {result.rows_before} -> {result.rows_after}")
print(f"Columns affected: {result.columns_affected}")
print(f"Steps executed: {len(result.steps_executed)}")
for step in result.steps_executed:
    print(f"  {step['action']}: {step.get('status', 'unknown')}")
if result.warnings:
    print(f"Warnings: {result.warnings}")
```

**Available Actions:**

| Action | Description | Parameters | Column Required |
|--------|-------------|-----------|----------------|
| `drop_rows` | Remove rows with null/empty values | condition (optional) | Optional |
| `fill_mean` | Replace nulls with column mean | — | Yes |
| `fill_median` | Replace nulls with column median | — | Yes |
| `fill_mode` | Replace nulls with most frequent value | — | Yes |
| `fill_value` | Replace nulls with a fixed value | value | Yes |
| `trim_whitespace` | Strip leading/trailing whitespace | — | Yes |
| `lowercase` | Convert strings to lowercase | — | Yes |
| `uppercase` | Convert strings to uppercase | — | Yes |
| `regex_replace` | Pattern-based replacement | pattern, replacement | Yes |
| `deduplicate` | Remove exact duplicate rows | — | No |
| `type_cast` | Convert column data type | type (int/float/str) | Yes |
| `clip` | Bound values to min/max range | min, max | Yes |
| `hash_pii` | Hash PII fields with SHA-256 | — | Yes |
| `mask_pii` | Mask showing last N characters | visible_chars | Yes |

**Pipeline Best Practices:**

1. Order: trim → standardize → fill → cast → clip → deduplicate
2. Always deduplicate last (other steps may create duplicates)
3. Run validation before and after to measure improvement
4. Test on a sample before full execution
5. Log all transformations for audit trails

### 5. Quality Monitoring

Continuous quality checks with configurable thresholds and alerting.

```python
# Add monitoring checks
agent.add_monitor_check("customer_data", MonitorCheck(
    name="minimum_rows",
    check_type="row_count_min",
    parameters={"min": 1000},
    severity=Severity.HIGH,
    description="Dataset must have at least 1000 rows",
))

agent.add_monitor_check("customer_data", MonitorCheck(
    name="email_completeness",
    check_type="null_percentage",
    parameters={"column": "email", "max_percentage": 5.0},
    severity=Severity.MEDIUM,
    description="Email field should be <5% null",
))

agent.add_monitor_check("customer_data", MonitorCheck(
    name="data_freshness",
    check_type="freshness",
    parameters={"timestamp_column": "updated_at", "max_age_hours": 24},
    severity=Severity.CRITICAL,
    description="Data must be refreshed within 24 hours",
))

agent.add_monitor_check("customer_data", MonitorCheck(
    name="schema_integrity",
    check_type="schema_match",
    parameters={"columns": ["id", "name", "email", "age", "dept"]},
    severity=Severity.HIGH,
    description="Expected columns must be present",
))

# Run all checks
results = agent.run_monitor_checks("customer_data")
for r in results:
    icon = "PASS" if r.status.value == "pass" else "FAIL"
    print(f"[{icon}] {r.check_name}: {r.message}")
```

**Check Types:**

| Type | Parameters | PASS Condition | FAIL Condition |
|------|-----------|---------------|---------------|
| `row_count_min` | min | count >= min | count < min |
| `row_count_max` | max | count <= max | count > max |
| `null_percentage` | column, max_pct | null% <= max | null% > max |
| `freshness` | timestamp_column, max_hours | age <= max_hours | age > max_hours |
| `schema_match` | columns[] | all columns present | missing columns |
| `custom` | function | function returns {pass: true} | function returns {pass: false} |

### 6. Quality Scoring

Composite scoring across 6 DAMA-style quality dimensions with configurable weights.

```python
# Compute composite score
score = agent.compute_quality_score("customer_data")
print(f"Overall Quality: {score.overall:.2%}")
print(f"Grade: {agent._grade_from_score(score.overall)}")

# Dimension breakdown
print(f"  Completeness: {score.completeness:.2%}")
print(f"  Accuracy:     {score.accuracy:.2%}")
print(f"  Consistency:  {score.consistency:.2%}")
print(f"  Timeliness:   {score.timeliness:.2%}")
print(f"  Validity:     {score.validity:.2%}")
print(f"  Uniqueness:   {score.uniqueness:.2%}")
```

**Default Dimension Weights:**

| Dimension | Weight | What It Measures |
|-----------|--------|-----------------|
| Completeness | 0.20 | % of non-null values |
| Accuracy | 0.20 | % of values meeting range/format rules |
| Validity | 0.20 | % of values passing validation rules |
| Uniqueness | 0.15 | 1 - duplicate percentage |
| Consistency | 0.15 | % of values consistent with allowed values |
| Timeliness | 0.10 | Freshness of temporal data |

**Grading Scale:**

| Grade | Score | Meaning |
|-------|-------|---------|
| A+ | >= 0.95 | Excellent — production-ready |
| A | >= 0.90 | Very Good — minor issues only |
| A- | >= 0.85 | Good — acceptable for most uses |
| B+ | >= 0.80 | Above Average — some cleanup recommended |
| B | >= 0.75 | Average — notable issues exist |
| B- | >= 0.70 | Below Average — cleanup needed |
| C+ | >= 0.65 | Poor — significant issues |
| C | >= 0.60 | Very Poor — major cleanup required |
| D | >= 0.50 | Critical — data may be unreliable |
| F | < 0.50 | Failing — do not use without remediation |

### 7. Comprehensive Assessment

The `assess_quality` method orchestrates all components into a single call.

```python
# Full assessment
report = agent.assess_quality("customer_data")

# Access all results
print(f"Score: {report.score.overall:.2%} ({report.summary['quality_grade']})")
print(f"Profile: {report.profile.row_count} rows x {report.profile.column_count} cols")
print(f"Issues: {report.summary['total_issues']} "
      f"({report.summary['critical_issues']} critical)")
print(f"Anomalies: {report.summary['total_anomalies']} "
      f"across {report.summary['anomaly_columns']} columns")
print(f"Monitor: {report.summary['monitor_checks_passed']} passed, "
      f"{report.summary['monitor_checks_failed']} failed")

# Export
json_output = agent.export_report(report, "json")
summary_text = agent.export_report(report, "summary")
print(summary_text)
```

## Operational Guidelines

### When to Profile First
Always profile a new dataset before creating validation rules. Profiling reveals:
- Column types (so you know which rules apply)
- Null percentages (to set realistic expectations)
- Value distributions (to set appropriate thresholds)
- Patterns (to identify formatting requirements)
- Cardinality (to detect high/low cardinality issues)

### Anomaly Detection Strategy
1. Start with Z-Score for a quick scan of normal data
2. Use IQR if the distribution is visibly skewed
3. Use MAD if there are many outliers (most robust method)
4. Use EWM-STD for time-series data with trends
5. Use Percentile for simple boundary-based detection
6. Combine methods for high-confidence detection

### Cleansing Pipeline Design
1. Order steps logically: trim → standardize → fill → cast → clip → deduplicate
2. Run validation before and after cleansing to measure improvement
3. Preserve original data (don't modify in-place without a backup)
4. Log all transformations for audit trails
5. Test on a sample before full execution
6. Review warnings in the CleansingResult

### Monitoring Setup
1. Start with row_count_min and null_percentage checks
2. Add freshness checks for time-sensitive data
3. Add schema_match checks after schema migrations
4. Use custom checks for business-critical invariants
5. Review monitoring history periodically
6. Set appropriate alert severity levels

## Method Signatures

```python
class DataQualityAgent:
    def __init__(self, config: Optional[DataQualityConfig] = None) -> None: ...

    # Ingestion
    def register_dataset(self, name: str, data: List[Dict[str, Any]]) -> Dict[str, Any]: ...
    def get_dataset(self, name: str) -> List[Dict[str, Any]]: ...

    # Profiling
    def profile_dataset(self, name: str) -> DatasetProfile: ...
    def _profile_column(self, col_name: str, values: List[Any]) -> ColumnProfile: ...

    # Validation
    def add_rule(self, rule: ValidationRule) -> str: ...
    def remove_rule(self, rule_id: str) -> bool: ...
    def list_rules(self) -> List[Dict[str, Any]]: ...
    def validate_dataset(self, name: str) -> List[QualityIssue]: ...
    def _apply_rule(self, data: List[Dict[str, Any]], rule: ValidationRule) -> List[QualityIssue]: ...

    # Scoring
    def compute_quality_score(self, name: str) -> QualityScore: ...
    def _grade_from_score(self, score: float) -> str: ...

    # Anomaly Detection
    def detect_anomalies(self, name: str, column: str, method: AnomalyMethod = ..., **kwargs: Any) -> AnomalyResult: ...
    def _detect_zscore(self, column, values, indices, threshold) -> AnomalyResult: ...
    def _detect_iqr(self, column, values, indices, multiplier) -> AnomalyResult: ...
    def _detect_mad(self, column, values, indices, threshold) -> AnomalyResult: ...
    def _detect_ewm(self, column, values, indices, span) -> AnomalyResult: ...
    def _detect_percentile(self, column, values, indices, lower, upper) -> AnomalyResult: ...

    # Cleansing
    def create_cleansing_pipeline(self, name: str, steps: List[CleansingStep]) -> Dict[str, Any]: ...
    def run_cleansing_pipeline(self, dataset_name: str, pipeline_name: str) -> CleansingResult: ...

    # Monitoring
    def add_monitor_check(self, dataset_name: str, check: MonitorCheck) -> str: ...
    def run_monitor_checks(self, dataset_name: str) -> List[MonitorResult]: ...
    def _execute_check(self, dataset_name: str, check: MonitorCheck) -> MonitorResult: ...

    # Assessment
    def assess_quality(self, dataset_name: str) -> QualityReport: ...

    # Utilities
    def get_status(self) -> Dict[str, Any]: ...
    def export_report(self, report: QualityReport, format: str = "json") -> str: ...
```

## Data Models

### QualityDimension
```python
class QualityDimension(Enum):
    COMPLETENESS = "completeness"   # Are all values present?
    ACCURACY = "accuracy"           # Are values correct?
    CONSISTENCY = "consistency"     # Are values consistent across sources?
    TIMELINESS = "timeliness"       # Are values up to date?
    VALIDITY = "validity"           # Do values conform to rules?
    UNIQUENESS = "uniqueness"       # Are values non-duplicate?
    INTEGRITY = "integrity"         # Are referential constraints met?
    CONFORMANCE = "conformance"     # Do values follow standards?
```

### Severity
```python
class Severity(Enum):
    CRITICAL = "critical"   # Data corruption, compliance risk
    HIGH = "high"           # Significant quality issue
    MEDIUM = "medium"       # Moderate concern
    LOW = "low"             # Minor observation
    INFO = "info"           # Informational only
```

### ProfileType
```python
class ProfileType(Enum):
    NUMERIC = "numeric"     # Integer and float values
    TEXT = "text"           # String values
    DATETIME = "datetime"   # Date and time values
    BOOLEAN = "boolean"     # True/False values
    CATEGORICAL = "categorical"  # Limited set of values
    JSON = "json"           # JSON structured data
```

### AnomalyMethod
```python
class AnomalyMethod(Enum):
    ZSCORE = "zscore"           # Z-score based detection
    IQR = "iqr"                 # Interquartile range
    MAD = "mad"                 # Median absolute deviation
    EWM_STD = "ewm_std"        # Exponentially weighted moving std
    PERCENTILE = "percentile"   # Percentile-based bounds
```

### QualityScore
```python
@dataclass
class QualityScore:
    overall: float          # Weighted composite [0, 1]
    completeness: float     # Per-dimension scores [0, 1]
    accuracy: float
    consistency: float
    timeliness: float
    validity: float
    uniqueness: float
    dimensions: Dict[str, float]  # All dimension scores
```

## Checklists

### Data Onboarding Checklist
- [ ] Register dataset with `register_dataset`
- [ ] Run `profile_dataset` to understand column types and distributions
- [ ] Review null percentages and distinct counts
- [ ] Create validation rules based on business requirements
- [ ] Run `validate_dataset` to identify existing issues
- [ ] Create and execute cleansing pipeline if needed
- [ ] Run `assess_quality` for a comprehensive score
- [ ] Set up monitoring checks for ongoing quality
- [ ] Export and archive the initial quality report

### Validation Rule Creation Checklist
- [ ] Identify required fields → `not_null` rules
- [ ] Identify unique keys → `unique` rules
- [ ] Identify format requirements → `regex` rules
- [ ] Identify numeric bounds → `range` rules
- [ ] Identify allowed values → `allowed_values` rules
- [ ] Identify business logic → `custom` rules
- [ ] Set appropriate severity for each rule
- [ ] Document rule purpose and expected behavior
- [ ] Test rules on a sample before full validation

### Cleansing Pipeline Checklist
- [ ] Identify which columns need cleaning
- [ ] Order steps: trim → standardize → fill → cast → clip → deduplicate
- [ ] Test pipeline on a sample before full execution
- [ ] Verify row counts before and after
- [ ] Check that remaining issues are acceptable
- [ ] Log all transformations for audit
- [ ] Review warnings in the CleansingResult
- [ ] Archive the pre-cleansing data snapshot

### Monitoring Setup Checklist
- [ ] Add row count checks (min and max)
- [ ] Add null percentage checks per critical column
- [ ] Add freshness checks for time-sensitive data
- [ ] Add schema match checks
- [ ] Configure alert thresholds appropriately
- [ ] Set severity levels correctly
- [ ] Review monitoring history periodically
- [ ] Establish response procedures for each alert level

## Troubleshooting

### "Dataset not found" Error
```python
# Ensure you've registered the dataset first
agent.register_dataset("my_data", data_list)
# Then access it
dataset = agent.get_dataset("my_data")
```

### Validation Rules Not Finding Issues
- Check that `rule.enabled = True`
- Verify `rule.column` matches the exact column name in your data
- Ensure rule type matches the data type (e.g., `range` requires numeric values)
- Check that regex patterns are correctly escaped
- Verify `allowed_values` list is complete

### Anomaly Detection Returns Zero Anomalies
- Try adjusting the threshold (lower = more sensitive)
- Try a different method (IQR for skewed data, MAD for heavy tails)
- Check that the column contains numeric data
- Verify there are enough values (minimum 2 for statistics)
- Check if the data is genuinely clean

### Cleansing Pipeline Modifies Too Many/Few Rows
- Review step ordering (deduplicate should be last)
- Check that `drop_rows` conditions are correct
- Verify `fill_*` actions target the right null patterns
- Check that `regex_replace` patterns match expected values
- Review the `steps_executed` in CleansingResult for details

### Low Quality Score Despite "Good" Data
- Check which dimension is dragging down the score using `score.dimensions`
- Review the dimension weights in config (adjust if needed)
- Look at specific issues in the report for actionable fixes
- Consider that your thresholds may be too strict
- Check for high cardinality ratios indicating data issues

### Monitor Checks Always Pass
- Verify check parameters match your data schema
- Check that threshold values are appropriate
- Ensure the dataset is registered and accessible
- Review the `actual_value` vs `expected_value` in results
- Add more checks for edge cases

### Export Format Issues
- JSON export uses `default=str` for datetime objects
- Summary export is a human-readable text format
- For other formats, process the `report.to_dict()` output

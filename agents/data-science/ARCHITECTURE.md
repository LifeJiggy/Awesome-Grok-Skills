# Data Science Agent — System Architecture

## Table of Contents

1. [Overview](#overview)
2. [High-Level Architecture](#high-level-architecture)
3. [Component Deep Dives](#component-deep-dives)
4. [ML Pipeline Architecture](#ml-pipeline-architecture)
5. [Data Flow](#data-flow)
6. [Design Patterns](#design-patterns)
7. [Technology Stack](#technology-stack)
8. [Security Architecture](#security-architecture)
9. [Scalability Patterns](#scalability-patterns)
10. [Deployment Topology](#deployment-topology)
11. [Monitoring & Observability](#monitoring--observability)
12. [Disaster Recovery](#disaster-recovery)

---

## Overview

The Data Science Agent is a self-contained, dependency-minimal data science framework that covers the full lifecycle: data ingestion → profiling → preprocessing → feature engineering → model training → evaluation → experiment tracking → visualization → reproducibility management.

The core design principle is **zero external dependencies** for the core engine — all statistical, ML, and visualization logic is implemented from scratch. This ensures portability, auditability, and educational value.

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                      DATA SCIENCE AGENT                              │
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐              │
│  │   Data        │  │  Statistical │  │     ML       │              │
│  │  Preprocessor │  │  Analyzer    │  │ Model Builder│              │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘              │
│         │                 │                  │                       │
│         ▼                 ▼                  ▼                       │
│  ┌──────────────────────────────────────────────────────┐           │
│  │              Feature Engineer                         │           │
│  └──────────────────────────┬───────────────────────────┘           │
│                             │                                       │
│  ┌──────────────────────────┼───────────────────────────┐           │
│  │          ┌───────────────┼────────────────┐          │           │
│  │          ▼               ▼                ▼          │           │
│  │  ┌──────────────┐ ┌────────────┐ ┌──────────────┐   │           │
│  │  │  Hyperpara-  │ │   Model    │ │ Experiment   │   │           │
│  │  │  meter Tuner │ │  Evaluator │ │  Designer    │   │           │
│  │  └──────────────┘ └────────────┘ └──────────────┘   │           │
│  │                  Data Pipeline                       │           │
│  └──────────────────────────┬───────────────────────────┘           │
│                             │                                       │
│              ┌──────────────┼──────────────┐                        │
│              ▼              ▼              ▼                        │
│  ┌────────────────┐ ┌──────────────┐ ┌──────────────────┐          │
│  │  Data          │ │Reproducibi-  │ │    Data          │          │
│  │  Visualizer    │ │lity Manager  │ │    Pipeline      │          │
│  └────────────────┘ └──────────────┘ └──────────────────┘          │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Component Deep Dives

### 1. StatisticalAnalyzer

```
┌────────────────────────────────────────────┐
│            StatisticalAnalyzer              │
├────────────────────────────────────────────┤
│  describe()          → Dict[str, float]    │
│  median()            → float               │
│  percentile()        → float               │
│  t_test()            → Dict[str, Any]      │
│  chi_square_test()   → Dict[str, Any]      │
│  correlation_matrix()→ Dict[str,Dict]      │
│  detect_outliers()   → List[int]           │
│  normality_test()    → Dict[str, Any]      │
├────────────────────────────────────────────┤
│  Internal:                                 │
│  _skewness()  _kurtosis()  _pearson()      │
│  _approx_t_p()  _chi2_p()                 │
└────────────────────────────────────────────┘
```

**Responsibilities:**
- Descriptive statistics (mean, median, std, skewness, kurtosis, percentiles)
- Hypothesis testing (Welch's t-test, chi-squared goodness-of-fit)
- Correlation analysis (Pearson correlation matrix)
- Outlier detection (IQR method, Z-score method)
- Normality testing (Shapiro–Wilk inspired)

**Design Decisions:**
- All computations are pure functions with no side effects
- Results are returned as plain dictionaries for easy serialization
- Approximation methods used for p-values to avoid scipy dependency

### 2. MLModelBuilder

```
┌─────────────────────────────────────────────────┐
│              MLModelBuilder                      │
├─────────────────────────────────────────────────┤
│  train(X, y, model_type)  → ModelResult         │
│  predict(model_id, X)     → List[Any]           │
│  cross_validate(X, y, k)  → Dict[str, Any]      │
├─────────────────────────────────────────────────┤
│  Internal Models:                                │
│  ┌──────────────────┐  ┌─────────────────────┐  │
│  │  _DecisionStump   │  │ _SimpleLinearModel  │  │
│  │  - fit()          │  │ - fit()             │  │
│  │  - predict()      │  │ - predict()         │  │
│  │  - _gini()        │  │ - _solve()          │  │
│  └──────────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**Responsibilities:**
- Train classification (decision stump) and regression (OLS linear) models
- Run predictions on new data
- k-fold cross-validation
- Model comparison and selection

**Design Decisions:**
- Built-in models avoid sklearn dependency for portability
- Ridge penalty added to linear regression for numerical stability
- Models stored by ID for later retrieval

### 3. FeatureEngineer

```
┌───────────────────────────────────────────────────┐
│              FeatureEngineer                        │
├───────────────────────────────────────────────────┤
│  create_features(data, specs)  → List[Dict]        │
│  select_features(data, target) → List[str]          │
│  polynomial_features(data, cols)→ List[Dict]        │
├───────────────────────────────────────────────────┤
│  Supported Transformations:                         │
│  ┌───────────┬────────────┬───────────┐            │
│  │polynomial │    log     │   sqrt    │            │
│  │  ratio    │ difference │binning    │            │
│  │interaction│ absolute   │date_parts │            │
│  └───────────┴────────────┴───────────┘            │
│  Selection Methods: correlation | variance | MI     │
└───────────────────────────────────────────────────┘
```

**Responsibilities:**
- Create derived features (polynomial, log, sqrt, ratio, difference, interaction, binning, date decomposition)
- Feature selection via correlation, variance threshold, or mutual information
- Polynomial and interaction term generation

### 4. DataPreprocessor

```
┌──────────────────────────────────────────────────────────┐
│                   DataPreprocessor                         │
├──────────────────────────────────────────────────────────┤
│  handle_missing(data, strategy)     → List[Dict]          │
│  normalize(data, columns, method)   → List[Dict]          │
│  encode(data, columns, method)      → Tuple[List, Dict]   │
│  remove_duplicates(data, keys)      → List[Dict]          │
│  split_data(X, y, test_size)        → Tuple[4 lists]      │
├──────────────────────────────────────────────────────────┤
│  Imputation: mean|median|mode|constant|drop|ffill|bfill   │
│  Normalization: minmax|zscore|robust|maxabs|l1|l2         │
│  Encoding: label|frequency|onehot|ordinal                 │
│  Splitting: random|stratified|temporal|kfold              │
└──────────────────────────────────────────────────────────┘
```

### 5. HyperparameterTuner

```
┌──────────────────────────────────────────────────┐
│             HyperparameterTuner                    │
├──────────────────────────────────────────────────┤
│  grid_search(X, y, param_grid)     → Dict        │
│  random_search(X, y, distributions)→ Dict        │
├──────────────────────────────────────────────────┤
│  Strategy: exhaustive grid or random sampling     │
│  Scoring: task-appropriate (accuracy / neg MSE)   │
│  Returns: best params, best score, all results    │
└──────────────────────────────────────────────────┘
```

### 6. ModelEvaluator

```
┌──────────────────────────────────────────────────┐
│              ModelEvaluator                        │
├──────────────────────────────────────────────────┤
│  classification_metrics(actual, predicted)        │
│    → accuracy, precision, recall, F1, CM          │
│  regression_metrics(actual, predicted)            │
│    → MSE, RMSE, MAE, R², MAPE                    │
│  compare_models(results) → sorted ranking         │
└──────────────────────────────────────────────────┘
```

### 7. ExperimentDesigner

```
┌──────────────────────────────────────────────────┐
│             ExperimentDesigner                     │
├──────────────────────────────────────────────────┤
│  create_experiment(...)      → ExperimentConfig   │
│  record_result(result)       → None                │
│  list_experiments()          → List[Config]        │
│  compare_experiments(ids)    → List[Dict]          │
├──────────────────────────────────────────────────┤
│  Storage: JSON files in .experiments/ directory   │
│  Tracking: UUID-based experiment IDs               │
│  Comparison: multi-experiment metric comparison    │
└──────────────────────────────────────────────────┘
```

### 8. DataVisualizer

```
┌──────────────────────────────────────────────────┐
│              DataVisualizer                        │
├──────────────────────────────────────────────────┤
│  histogram(data, column)     → VisualizationSpec  │
│  scatter(data, x, y, hue)    → VisualizationSpec  │
│  correlation_heatmap(matrix) → VisualizationSpec  │
│  boxplot(data, column)       → VisualizationSpec  │
│  render_ascii(spec, data)    → str                 │
├──────────────────────────────────────────────────┤
│  ASCII Rendering:                                  │
│  ┌──────────┬───────────┬──────────┐              │
│  │histogram │  scatter  │   bar    │              │
│  └──────────┴───────────┴──────────┘              │
└──────────────────────────────────────────────────┘
```

### 9. ReproducibilityManager

```
┌──────────────────────────────────────────────────┐
│           ReproducibilityManager                   │
├──────────────────────────────────────────────────┤
│  snapshot(data, steps, seeds) → Record            │
│  verify(record_id, data, steps)→ bool             │
│  get_environment()           → Dict[str, str]     │
├──────────────────────────────────────────────────┤
│  Guarantees:                                       │
│  - SHA-256 data fingerprinting                    │
│  - Pipeline hash verification                     │
│  - Environment capture (Python version, platform) │
│  - Random seed tracking                           │
└──────────────────────────────────────────────────┘
```

### 10. DataPipeline

```
┌──────────────────────────────────────────────────┐
│              DataPipeline                          │
├──────────────────────────────────────────────────┤
│  register(name, fn)    → None                     │
│  add_step(name, fn, params) → PipelineStep        │
│  run(data)             → Any                      │
│  get_steps()           → List[PipelineStep]       │
├──────────────────────────────────────────────────┤
│  Execution: sequential, data threaded through     │
│  Error handling: step-level exception capture     │
│  Logging: per-step progress tracking              │
└──────────────────────────────────────────────────┘
```

---

## ML Pipeline Architecture

```
┌─────────┐    ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐
│  Raw    │───▶│ Profile  │───▶│  Clean    │───▶│ Feature  │───▶│  Split   │
│  Data   │    │  & EDA   │    │ & Impute  │    │ Engineer │    │ Train/   │
│         │    │          │    │ & Encode  │    │          │    │ Test     │
└─────────┘    └──────────┘    └───────────┘    └──────────┘    └────┬─────┘
                                                                      │
                    ┌─────────────────────────────────────────────────┘
                    ▼
            ┌──────────────┐    ┌──────────┐    ┌──────────────┐
            │   Train      │───▶│ Evaluate │───▶│   Tune       │
            │   Model(s)   │    │ Metrics  │    │ Hyperparams  │
            └──────────────┘    └──────────┘    └──────┬───────┘
                                                        │
                    ┌───────────────────────────────────┘
                    ▼
            ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
            │   Select     │───▶│    Track     │───▶│    Export     │
            │   Best Model │    │  Experiment  │    │  & Deploy    │
            └──────────────┘    └──────────────┘    └──────────────┘
```

---

## Data Flow

```
                        ┌─────────────────────────┐
                        │      User / CLI          │
                        └────────────┬────────────┘
                                     │
                                     ▼
                        ┌─────────────────────────┐
                        │    DataPipeline.run()    │
                        └────────────┬────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
            │   Step 1     │ │   Step 2     │ │   Step N     │
            │  Preprocess  │ │  Engineer    │ │  Train       │
            └──────┬───────┘ └──────┬───────┘ └──────┬───────┘
                   │                │                │
                   ▼                ▼                ▼
            ┌──────────────────────────────────────────────┐
            │            Intermediate Data State            │
            │     (List[Dict] threaded through steps)      │
            └──────────────────────────┬───────────────────┘
                                       │
                            ┌──────────┼──────────┐
                            ▼          ▼          ▼
                    ┌────────────┐ ┌────────┐ ┌────────────┐
                    │  Results   │ │  Logs  │ │  Snapshot  │
                    │  (JSON)    │ │        │ │  (SHA-256) │
                    └────────────┘ └────────┘ └────────────┘
```

---

## Design Patterns

### 1. Pipeline Pattern

The `DataPipeline` class implements the Pipeline pattern — a sequence of steps where each step transforms data and passes it to the next.

```python
pipeline = DataPipeline()
pipeline.register("clean", cleaner.handle_missing)
pipeline.register("encode", cleaner.encode)
pipeline.add_step("clean", "clean", {"strategy": "mean"})
pipeline.add_step("encode", "encode", {"columns": ["city"]})
result = pipeline.run(raw_data)
```

**Benefits:**
- Decoupled, reusable steps
- Easy to add/remove/reorder steps
- Consistent data threading
- Step-level error isolation

### 2. Strategy Pattern

The `DataPreprocessor` uses the Strategy pattern for interchangeable algorithms:

```python
# Same interface, different strategies
dp.handle_missing(data, strategy=ImputationStrategy.MEAN)
dp.handle_missing(data, strategy=ImputationStrategy.KNN)
dp.normalize(data, cols, method=NormalizationMethod.ZSCORE)
dp.normalize(data, cols, method=NormalizationMethod.ROBUST)
dp.encode(data, cols, method=EncodingMethod.LABEL)
dp.encode(data, cols, method=EncodingMethod.ONEHOT)
```

### 3. Factory Pattern

The `MLModelBuilder` uses an internal factory to instantiate models:

```python
# Model selection by string
builder.train(X, y, model_type="stump")   # → _DecisionStump
builder.train(X, y, model_type="linear")  # → _SimpleLinearModel
```

### 4. Observer Pattern (Logging)

Every component uses Python's `logging` module as an observer — any number of handlers can subscribe without modifying the component:

```python
logger = logging.getLogger("data_science_agent.MLModelBuilder")
# Attach any handler: file, stream, network, etc.
logger.addHandler(custom_handler)
```

### 5. Template Method Pattern

The `StatisticalAnalyzer` defines a template for analysis workflows — the high-level method calls private helpers that subclasses can override:

```python
def describe(self, values):
    # Template: compute → aggregate → return
    mean = self._compute_mean(values)
    std = self._compute_std(values, mean)
    skew = self._skewness(values, mean, std)  # Override point
    ...
```

### 6. Dataclass Value Object Pattern

All data models (`DataProfile`, `ModelResult`, `ExperimentConfig`, etc.) are `@dataclass` value objects — immutable-ish, serializable, self-describing:

```python
@dataclass
class ModelResult:
    model_name: str
    task_type: TaskType
    metrics: Dict[str, float]
    # ... serializable, comparable, inspectable
```

---

## Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| Language | Python 3.10+ | Type hints, dataclasses, walrus operator |
| Core ML | Custom (zero deps) | Portability, auditability, education |
| Statistics | Custom | No scipy/numpy dependency |
| Visualization | ASCII rendering | Terminal-native, no matplotlib needed |
| Serialization | JSON | Universal, human-readable |
| Hashing | SHA-256, MD5 | Reproducibility verification |
| Logging | Python stdlib `logging` | Structured, configurable |
| Storage | Filesystem (JSON) | Simple, inspectable, no DB needed |

### Optional Extensions

| Layer | Technology | When to Add |
|-------|-----------|-------------|
| Numerical | NumPy, SciPy | Large datasets, advanced stats |
| ML | scikit-learn, XGBoost | Production models |
| Visualization | matplotlib, seaborn, plotly | Rich interactive charts |
| Storage | SQLite, PostgreSQL | Multi-user, concurrent access |
| Orchestration | Airflow, Prefect | Scheduled pipelines |

---

## Security Architecture

```
┌──────────────────────────────────────────────────────┐
│                  Security Layers                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Layer 1: Input Validation                           │
│  ┌──────────────────────────────────────────────┐    │
│  │ • Type checking on all public methods         │    │
│  │ • Division-by-zero guards                     │    │
│  │ • Empty collection guards                     │    │
│  │ • Column existence validation                 │    │
│  └──────────────────────────────────────────────┘    │
│                                                      │
│  Layer 2: Data Protection                            │
│  ┌──────────────────────────────────────────────┐    │
│  │ • SHA-256 data fingerprinting                 │    │
│  │ • No PII stored in logs                       │    │
│  │ • Experiment data on local filesystem only    │    │
│  │ • No network calls in core engine             │    │
│  └──────────────────────────────────────────────┘    │
│                                                      │
│  Layer 3: Reproducibility as Security                │
│  ┌──────────────────────────────────────────────┐    │
│  │ • Pipeline hash verification                  │    │
│  │ • Environment fingerprinting                  │    │
│  │ • Random seed tracking                        │    │
│  │ • Deterministic execution guarantee           │    │
│  └──────────────────────────────────────────────┘    │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Security Considerations

1. **No Remote Code Execution** — The agent executes only registered pipeline steps. No `eval()`, `exec()`, or `__import__()` in hot paths.

2. **Input Validation** — All public methods validate inputs before processing. Empty lists, None values, and type mismatches raise clear exceptions.

3. **Numerical Stability** — Division-by-zero is guarded everywhere. Ridge penalties prevent singular matrix errors. Epsilon values prevent log(0).

4. **No Secrets in Logs** — Logging captures operation metadata (row counts, column names, timing) but never raw data values or PII.

5. **Filesystem Isolation** — Experiment storage and reproducibility snapshots write only to designated local directories. No absolute path traversal.

---

## Scalability Patterns

### Horizontal: Data Parallelism

```
┌───────────────────────────────────────────────┐
│              Data Sharding                      │
│                                                 │
│  Full Dataset                                  │
│  ┌──────┬──────┬──────┬──────┐                │
│  │Shard1│Shard2│Shard3│Shard4│                │
│  └──┬───┴──┬───┴──┬───┴──┬───┘                │
│     │      │      │      │                     │
│     ▼      ▼      ▼      ▼                     │
│  ┌─────┐┌─────┐┌─────┐┌─────┐                │
│  │Proc1││Proc2││Proc3││Proc4│  (independent)   │
│  └──┬──┘└──┬──┘└──┬──┘└──┬──┘                │
│     │      │      │      │                     │
│     ▼      ▼      ▼      ▼                     │
│  ┌──────────────────────────────┐              │
│  │        Aggregation           │              │
│  └──────────────────────────────┘              │
└───────────────────────────────────────────────┘
```

### Vertical: Pipeline Optimization

```
Before (sequential):              After (parallel where possible):
Step1 → Step2 → Step3 → Step4    Step1 ─┐
                                        ├──▶ Step4
                                  Step2 ─┤
                                        │
                                  Step3 ─┘
```

### Caching Strategy

```
┌────────────────────────────────────────────┐
│            Multi-Level Cache                │
├────────────────────────────────────────────┤
│  L1: In-memory (per-session)               │
│  ├─ StatisticalAnalyzer._cache             │
│  ├─ Feature selection scores               │
│  └─ Correlation matrices                   │
│                                            │
│  L2: Filesystem (cross-session)            │
│  ├─ Experiment configs & results           │
│  ├─ Reproducibility snapshots              │
│  └─ Pipeline definitions                   │
│                                            │
│  L3: Content-addressed (immutable)         │
│  ├─ Data hashes → deduplication            │
│  └─ Pipeline hashes → version tracking     │
└────────────────────────────────────────────┘
```

### Performance Targets

| Operation | Target (10K rows) | Target (100K rows) |
|-----------|-------------------|---------------------|
| Profiling | < 100ms | < 1s |
| Imputation | < 50ms | < 500ms |
| Normalization | < 50ms | < 500ms |
| Feature engineering | < 200ms | < 2s |
| Model training (stump) | < 500ms | < 5s |
| Model training (linear) | < 1s | < 10s |
| Cross-validation (5-fold) | < 2.5s | < 25s |
| Correlation matrix | < 200ms | < 2s |

---

## Deployment Topology

```
┌──────────────────────────────────────────────────────────────┐
│                     Deployment Options                         │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Option 1: Local Script                                      │
│  ┌──────────────────────┐                                    │
│  │  python agent.py     │                                    │
│  │  ┌────────────────┐  │                                    │
│  │  │  DataScience    │  │                                    │
│  │  │  Agent Engine   │  │                                    │
│  │  └────────────────┘  │                                    │
│  └──────────────────────┘                                    │
│                                                              │
│  Option 2: CLI Tool                                          │
│  ┌──────────────────────┐    ┌────────────────┐             │
│  │  ds-agent analyze    │───▶│  Local Files   │             │
│  │  ds-agent train      │    │  JSON / CSV    │             │
│  │  ds-agent experiment │    └────────────────┘             │
│  └──────────────────────┘                                    │
│                                                              │
│  Option 3: Library Import                                    │
│  ┌──────────────────────────────────────────┐               │
│  │  from agent import (                      │               │
│  │      StatisticalAnalyzer,                 │               │
│  │      MLModelBuilder,                      │               │
│  │      FeatureEngineer,                     │               │
│  │      DataPreprocessor,                    │               │
│  │  )                                        │               │
│  │  sa = StatisticalAnalyzer()               │               │
│  │  result = sa.describe(my_values)          │               │
│  └──────────────────────────────────────────┘               │
│                                                              │
│  Option 4: Web API (with FastAPI wrapper)                    │
│  ┌──────────────────────┐    ┌────────────────┐             │
│  │  POST /analyze       │───▶│  FastAPI        │             │
│  │  POST /train         │    │  ┌────────────┐│             │
│  │  GET  /experiments   │    │  │ DataScience││             │
│  └──────────────────────┘    │  │   Agent    ││             │
│                              │  └────────────┘│             │
│                              └────────────────┘             │
└──────────────────────────────────────────────────────────────┘
```

---

## Monitoring & Observability

```
┌──────────────────────────────────────────────────────────┐
│                Observability Stack                         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Metrics (captured per operation):                       │
│  ┌──────────────────────────────────────────────┐       │
│  │ • Row count in / out                         │       │
│  │ • Column count in / out                      │       │
│  │ • Operation duration (seconds)               │       │
│  │ • Memory delta (approximate)                 │       │
│  │ • Error count per step                       │       │
│  └──────────────────────────────────────────────┘       │
│                                                          │
│  Logging (structured, per-component):                    │
│  ┌──────────────────────────────────────────────┐       │
│  │ [2024-01-15T10:30:00] INFO  StatisticalAnal │       │
│  │   yzer — describe() completed: 4 values      │       │
│  │ [2024-01-15T10:30:01] INFO  DataPreprocessor│       │
│  │   — Imputed missing values (strategy=mean)   │       │
│  │ [2024-01-15T10:30:02] INFO  MLModelBuilder  │       │
│  │   — Trained stump_abc123 — accuracy: 0.85    │       │
│  └──────────────────────────────────────────────┘       │
│                                                          │
│  Health Checks:                                          │
│  ┌──────────────────────────────────────────────┐       │
│  │ • ReproducibilityManager.get_environment()   │       │
│  │ • Pipeline step count and dependency graph   │       │
│  │ • Experiment storage disk usage              │       │
│  └──────────────────────────────────────────────┘       │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## Disaster Recovery

### Data Loss Prevention

```
┌──────────────────────────────────────────────────────┐
│            Data Recovery Strategy                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  1. Snapshot Before Transform                         │
│     DataPreprocessor operates on deep copies          │
│     Original data never mutated                       │
│                                                      │
│  2. Experiment Audit Trail                            │
│     Every experiment config persisted to JSON          │
│     Every result persisted to JSON                     │
│     Full history in .experiments/ directory            │
│                                                      │
│  3. Reproducibility Snapshots                         │
│     SHA-256 data fingerprint before each run           │
│     Pipeline definition hash captured                  │
│     Environment metadata recorded                      │
│                                                      │
│  4. Step-Level Rollback                               │
│     Pipeline steps are independent                     │
│     Failed step → data state preserved from previous   │
│     Re-run from any step with same input               │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Recovery Procedures

| Scenario | Recovery Method |
|----------|----------------|
| Data corruption mid-pipeline | Re-run from last successful step using snapshot |
| Experiment config lost | Reconstruct from JSON files in .experiments/ |
| Model performance regression | Compare experiment results across versions |
| Environment change | ReproducibilityManager.get_environment() identifies drift |
| Pipeline definition change | Pipeline hash verification detects modifications |

---

## Appendix: File Structure

```
agents/data-science/
├── agent.py           # Core implementation (all classes)
├── ARCHITECTURE.md    # This document
├── GROK.md            # Agent identity and capabilities
└── README.md          # Usage documentation
```

### Dependency Graph

```
agent.py internal dependencies:

StatisticalAnalyzer ─────────────────────────────────┐
      │                                               │
      ▼                                               │
FeatureEngineer ◄────────────────────────────────────┘
      │
      ▼
DataPreprocessor
      │
      ├──▶ HyperparameterTuner ──▶ MLModelBuilder
      │
      ├──▶ ModelEvaluator
      │
      ├──▶ ExperimentDesigner
      │
      ├──▶ DataVisualizer
      │
      ├──▶ ReproducibilityManager
      │
      └──▶ DataPipeline (orchestrates all above)
```

---

## Error Handling Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                  Error Handling Strategy                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Level 1: Input Validation (fail-fast)                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • Empty sequence → ValueError                        │   │
│  │ • Mismatched lengths → ValueError                    │   │
│  │ • Zero expected frequency → ValueError               │   │
│  │ • Unknown model type → ValueError                    │   │
│  │ • Unknown method → ValueError                        │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Level 2: Numerical Stability (graceful degradation)         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • Division by zero → epsilon / fallback value        │   │
│  │ • Singular matrix → ridge penalty                    │   │
│  │ • Zero variance → return safe default                │   │
│  │ • Log of non-positive → return 0                     │   │
│  │ • Empty bin → skip with warning                      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Level 3: Pipeline Error Isolation                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • Step-level exception capture                       │   │
│  │ • Step name in error message                         │   │
│  │ • Data state preserved on failure                    │   │
│  │ • Re-run from any step                               │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Level 4: Feature Engineering Resilience                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • Per-feature try/except                             │   │
│  │ • Failed feature → default value (0)                 │   │
│  │ • Warning logged with feature name                   │   │
│  │ • Other features continue processing                 │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## State Management

```
┌──────────────────────────────────────────────────────────────┐
│                  State Management Model                       │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Stateless Components (no internal state):                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • StatisticalAnalyzer._cache (optional memoization)  │   │
│  │ • ModelEvaluator (pure functions)                    │   │
│  │ • DataVisualizer._specs (session-scoped)             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Stateful Components (persist state):                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • MLModelBuilder._models (trained model registry)    │   │
│  │ • DataPreprocessor._encoders (fitted encoders)       │   │
│  │ • DataPreprocessor._scaler_params (fitted scalers)   │   │
│  │ • ExperimentDesigner._experiments (experiment registry)│  │
│  │ • ExperimentDesigner._results (result registry)      │   │
│  │ • ReproducibilityManager._records (snapshot history) │   │
│  │ • DataPipeline._steps (step definition)              │   │
│  │ • DataPipeline._step_functions (function registry)   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Persistence:                                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • Experiment configs → JSON files                    │   │
│  │ • Experiment results → JSON files                    │   │
│  │ • Reproducibility records → JSON files               │   │
│  │ • Pipeline definitions → dict export                 │   │
│  │ • Trained models → in-memory only (no serialization) │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## Testing Strategy

```
┌──────────────────────────────────────────────────────────────┐
│                  Testing Approach                             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  Unit Tests (per class):                                     │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • StatisticalAnalyzer: describe, t_test, correlation │   │
│  │ • MLModelBuilder: train, predict, cross_validate     │   │
│  │ • FeatureEngineer: create, select, polynomial        │   │
│  │ • DataPreprocessor: all strategies and methods       │   │
│  │ • ModelEvaluator: classification and regression      │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Integration Tests (cross-class):                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • Full pipeline: preprocess → engineer → train       │   │
│  │ • Experiment lifecycle: create → train → record      │   │
│  │ • Reproducibility: snapshot → modify → verify fail   │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
│  Edge Case Coverage:                                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ • Empty datasets (0 rows, 0 columns)                 │   │
│  │ • Single-row datasets                                │   │
│  │ • All-missing columns                                │   │
│  │ • Constant columns (zero variance)                   │   │
│  │ • Extremely large/small values                       │   │
│  │ • Non-numeric data in numeric operations             │   │
│  └──────────────────────────────────────────────────────┘   │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

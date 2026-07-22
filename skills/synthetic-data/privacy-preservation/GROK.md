---
name: "privacy-preservation"
category: "synthetic-data"
version: "1.0.0"
tags: ["synthetic-data", "privacy", "differential-privacy", "anonymization", "k-anonymity", "l-diversity", "t-closeness"]
---

# Privacy Preservation Toolkit

## Overview

The `privacy-preservation` module implements state-of-the-art anonymization techniques to protect sensitive information in datasets while maintaining their analytical utility. It provides a unified interface for applying Differential Privacy (DP), k-Anonymity, l-Diversity, and t-Closeness to both raw data and synthetic data outputs. This module is critical for organizations operating under strict regulatory frameworks like GDPR, HIPAA, and CCPA, where data misuse can lead to severe legal and financial penalties.

A core component of this module is the `PrivacyBudgetManager`, which tracks the cumulative privacy cost ($\epsilon$) across multiple queries or data releases. This prevents the "privacy budget exhaustion" that occurs when an attacker combines multiple statistically similar releases to re-identify individuals. The module also includes a `ReIdentificationRiskAssessor` that calculates the probability of linking a synthetic record back to a real individual in a reference dataset, allowing data stewards to verify the safety of their data before release.

Beyond traditional anonymization, the module explores "Synthetic Data as a Privacy Shield," where generative models are trained to produce data that statistically resembles the original but contains no actual records of real individuals. This approach, combined with DP-SGD (Differentially Private Stochastic Gradient Descent) during model training, provides a mathematically provable guarantee that the output is safe for public sharing.

The module operates on a layered defense model: identity disclosure protection (k-anonymity), attribute disclosure protection (l-diversity, t-closeness), and statistical disclosure control (differential privacy). Each layer addresses a different attack vector, and they are designed to be composed together in configurable pipelines. The `AuditLogger` provides an immutable record of every transformation applied, enabling compliance officers to trace exactly how a dataset was protected.

## Core Capabilities

*   **Differential Privacy (DP)**: Implement DP mechanisms like Laplace and Gaussian noise injection, Exponential Mechanism, and DP-SGD for generative model training.
*   **k-Anonymity Enforcement**: Generalize quasi-identifiers (e.g., age, zip code) to ensure every record is indistinguishable from at least $k-1$ others.
*   **l-Diversity and t-Closeness**: Enhance k-anonymity by ensuring sensitive attributes (e.g., diagnosis codes) have sufficient diversity and distribution similarity within equivalence classes.
*   **Privacy Budget Management**: Track and limit the cumulative privacy loss ($\epsilon$) across multiple data releases or queries.
*   **Re-identification Risk Assessment**: Calculate linkage disclosure risk using record matching algorithms and probabilistic models.
*   **Automated Anonymization Pipelines**: Chain multiple privacy techniques (e.g., generalization + noise injection) in a configurable, reproducible pipeline.
*   **Secure Synthesis**: Train generative models with DP guarantees to produce safe, shareable synthetic datasets.
*   **Audit Logging**: Maintain a detailed, immutable log of all privacy transformations applied to a dataset for compliance auditing.
*   **Attribute Disclosure Prevention**: Implement techniques specifically designed to prevent the disclosure of sensitive attributes even when quasi-identifiers are generalized.
*   **Privacy-Preserving Aggregation**: Provide tools for performing statistical aggregations on sensitive data without revealing individual records.
*   **Quasi-Identifier Detection**: Automatically identify columns that function as quasi-identifiers based on uniqueness analysis and external data overlap.
*   **Dynamic Data Protection**: Apply privacy protections to streaming data where new records arrive continuously and must be anonymized in real-time.
*   **Suppression Controls**: Configure suppression thresholds to remove records that cannot be safely generalized without exceeding the k-anonymity threshold.

## Privacy Threat Model Reference

| Threat | Description | Primary Defense |
|--------|-------------|-----------------|
| **Identity Disclosure** | Linking a record to a known individual | k-Anonymity |
| **Attribute Disclosure** | Inferring a sensitive value for a specific individual | l-Diversity, t-Closeness |
| **Statistical Disclosure** | Learning aggregate statistics that reveal individual contributions | Differential Privacy |
| **Linkage Attack** | Combining external data to re-identify records | k-Anonymity + DP |
| **Membership Inference** | Determining if an individual was in the training dataset | DP-SGD during model training |
| **Model Inversion** | Reconstructing input features from model outputs | Differential Privacy + Access Control |

## Usage Examples

### 1. Applying k-Anonymity to a Dataset

```python
import pandas as pd
from privacy_preservation import Anonymizer

# Load dataset with quasi-identifiers
data = pd.read_csv("patient_records.csv")

# Initialize anonymizer with k=5 (each group must have at least 5 people)
anonymizer = Anonymizer(method="k-anonymity", k=5)

# Define quasi-identifiers and sensitive attributes
quasi_ids = ["age", "gender", "zip_code"]
sensitive_attrs = ["diagnosis", "treatment"]

# Apply generalization
anonymized_data = anonymizer.fit_transform(
    data,
    quasi_identifiers=quasi_ids,
    sensitive_attributes=sensitive_attrs
)

print(f"Anonymized {len(anonymized_data)} records with k=5.")
```

### 2. Using the Privacy Budget Manager

```python
from privacy_preservation import PrivacyBudgetManager

# Initialize with a total budget of epsilon=1.0
budget_manager = PrivacyBudgetManager(total_epsilon=1.0, delta=1e-5)

# Simulate a series of queries
for i in range(10):
    # Check if we have budget left for this query
    if budget_manager.check_budget(cost=0.1):
        # Perform query (mocked here)
        result = f"Query {i} result"
        budget_manager.spend(cost=0.1)
        print(f"Query {i} executed. Remaining budget: {budget_manager.remaining_epsilon:.2f}")
    else:
        print(f"Budget exhausted at query {i}. Stopping.")
        break
```

### 3. Re-identification Risk Assessment

```python
from privacy_preservation import ReIdentificationRiskAssessor

# Load the synthetic dataset and the original (private) reference dataset
synthetic_data = pd.read_csv("synthetic_patients.csv")
original_data = pd.read_csv("real_patients.csv")

# Initialize risk assessor
assessor = ReIdentificationRiskAssessor()

# Calculate risk
risk_report = assessor.assess(
    synthetic=synthetic_data,
    original=original_data,
    quasi_identifiers=["age", "zip_code", "gender"]
)

print(f"Average Re-identification Risk: {risk_report['average_risk']:.4f}")
print(f"Maximum Risk: {risk_report['max_risk']:.4f}")
if risk_report['average_risk'] > 0.05:
    print("Warning: Risk exceeds 5% threshold. Consider stricter anonymization.")
```

### 4. Full Anonymization Pipeline

```python
from privacy_preservation import AnonymizationPipeline

# Create a multi-step pipeline
pipeline = AnonymizationPipeline(steps=[
    {"method": "k-anonymity", "k": 5, "quasi_identifiers": ["age", "zip"]},
    {"method": "l-diversity", "l": 3, "sensitive_attrs": ["diagnosis"]},
    {"method": "differential_privacy", "epsilon": 0.5, "mechanism": "laplace"}
])

# Apply the full pipeline
protected_data = pipeline.apply(data)
```

### 5. DP-SGD for Generative Model Training

```python
from privacy_preservation import DPSGDOptimizer

# Wrap an existing PyTorch model with DP-SGD
dp_optimizer = DPSGDOptimizer(
    model=generator,
    noise_multiplier=1.1,  # Scales the Gaussian noise added to gradients
    max_grad_norm=1.0,     # Clips gradients per sample
    batch_size=256,
    dataset_size=50000
)

# Train with privacy guarantees
dp_optimizer.train(
    epochs=50,
    real_data=real_data,
    epsilon_budget=1.0  # Stop training when this budget is consumed
)

# The trained model now has a provable privacy guarantee
print(f"Final epsilon spent: {dp_optimizer.epsilon_spent:.4f}")
```

### 6. Dynamic Streaming Anonymization

```python
from privacy_preservation import StreamingAnonymizer

# Configure a streaming anonymizer with a sliding window
stream_anon = StreamingAnonymizer(
    method="k-anonymity",
    k=5,
    window_size=1000,
    quasi_identifiers=["age", "zip"]
)

# Process a stream of incoming records
for record in data_stream:
    anonymized = stream_anon.process_record(record)
    if anonymized is not None:
        output_queue.put(anonymized)
```

## Generalization Hierarchy Examples

The anonymizer uses domain-specific generalization hierarchies to reduce quasi-identifier precision:

| Original Value | Level 0 | Level 1 | Level 2 | Level 3 |
|---------------|---------|---------|---------|---------|
| Age (e.g., 34) | 34 | 30-39 | 25-44 | * |
| ZIP Code (e.g., 10012) | 10012 | 1001* | 100** | * |
| Birth Year (e.g., 1990) | 1990 | 1990s | 20th century | * |
| Salary (e.g., $85,000) | $85,000 | $80K-$90K | $50K-$100K | * |
| City (e.g., "New York") | New York | NY | USA | * |

## Regulatory Compliance Matrix

| Regulation | Key Requirement | Module Feature |
|------------|----------------|----------------|
| **GDPR Art. 25** | Data protection by design and default | DP-SGD, anonymization pipelines |
| **HIPAA** | De-identification of PHI (Safe Harbor or Expert Determination) | k-Anonymity (k=5+), l-Diversity, re-identification risk assessment |
| **CCPA** | Consumer right to opt out of data sale | Privacy budget tracking, audit logs |
| **PCI-DSS** | Protection of cardholder data | Tokenization, masking, suppression |
| **FERPA** | Protection of student education records | Generalization, aggregation, DP |
| **SOX** | Financial data integrity | Audit logging, tamper-evident transformations |

## Best Practices

1.  **Determine the Right $k$**: For k-Anonymity, choose $k$ based on the quasi-identifiers' uniqueness. A $k$ of 5 or more is standard, but for highly unique populations, $k=10$ or higher may be necessary.
2.  **Monitor the Privacy Budget**: Never exceed your organization's defined $\epsilon$ limit. Use the `PrivacyBudgetManager` to automate enforcement.
3.  **Combine Techniques**: k-Anonymity protects against identity disclosure, but l-Diversity and t-Closeness are needed to prevent attribute disclosure. Use them in combination.
4.  **Test for Re-identification**: Always run a `ReIdentificationRiskAssessor` before releasing any dataset, even if it has been anonymized.
5.  **Use DP for Model Training**: If using generative models, train them with DP-SGD to ensure the model itself doesn't memorize individual records.
6.  **Regularly Audit Logs**: Review the `AuditLogger` output periodically to ensure no unauthorized or overly aggressive data access has occurred.
7.  **Understand the Trade-off**: Privacy comes at the cost of utility. Use the `quality-validation` module to measure how much information is lost after anonymization.
8.  **Implement Defense-in-Depth**: Don't rely on a single technique. Combine statistical disclosure control, access controls, and audit logging for comprehensive protection.
9.  **Consider Attacker Models**: Different anonymization techniques protect against different attacker models (e.g., k-anonymity assumes the attacker has access to external data). Choose techniques that match your threat model.
10. **Calibrate Noise Carefully**: For differential privacy, the noise scale must be proportional to the query sensitivity. Use the built-in `SensitivityCalculator` to avoid under- or over-noising.
11. **Test Suppression Thresholds**: When suppressing records that cannot meet k-anonymity, monitor that suppression doesn't disproportionately affect minority groups, which would create a fairness concern.

## Related Modules

*   [data-generation](../data-generation/GROK.md): Create synthetic data that serves as a privacy-preserving alternative to real data.
*   [quality-validation](../quality-validation/GROK.md): Measure the utility and statistical fidelity of data after privacy transformations.
*   [augmentation](../augmentation/GROK.md): Techniques to enrich data while maintaining privacy constraints.
*   [domain-specific](../domain-specific/GROK.md): Domain-specific privacy configurations (e.g., HIPAA for healthcare, PCI-DSS for finance).

---

## Advanced Configuration

The `privacy-preservation` module supports detailed configuration of every anonymization technique through YAML files or programmatic APIs.

### Configuration File Format

```yaml
# privacy_config.yaml
anonymization:
  default_method: "k-anonymity"
  k: 5
  l: 3
  t: 0.2

differential_privacy:
  mechanism: "gaussian"
  epsilon: 1.0
  delta: 1e-5
  noise_multiplier: 1.1
  max_grad_norm: 1.0
  accountant: "rdp"  # Rényi Differential Privacy accountant

budget:
  total_epsilon: 10.0
  total_delta: 1e-4
  strategy: "sequential"  # or "advanced" composition
  alert_threshold: 0.8  # Alert at 80% budget usage

generalization:
  hierarchies:
    age: "auto"
    zip_code: "us_postal"
    salary: "custom"
  suppression_threshold: 0.05  # Suppress groups < 5% of dataset

risk_assessment:
  max_reidentification_risk: 0.05
  algorithm: "record_linkage"
  external_datasets: []
```

### Programmatic Configuration

```python
from privacy_preservation import PrivacyConfig, Anonymizer

config = PrivacyConfig(
    method="k-anonymity",
    k=10,
    quasi_identifiers=["age", "zip", "gender"],
    sensitive_attributes=["diagnosis", "treatment"],
    suppression_threshold=0.05,
    generalization_hierarchies={
        "age": [(18, 25), (26, 35), (36, 50), (51, 65), (66, 100)],
        "zip": [(0, 3), (0, 2), (0, 1)]
    }
)

anonymizer = Anonymizer(config=config)
```

### Dynamic Configuration Updates

```python
from privacy_preservation import DynamicPrivacyManager

manager = DynamicPrivacyManager(config_path="privacy_config.yaml")

# Update k-anonymity threshold at runtime
manager.update_config("anonymization.k", 10)

# Register callbacks for budget exhaustion
@manager.on_budget_exhausted
def handle_budget_exhaustion(remaining_epsilon):
    print(f"Privacy budget nearly exhausted: {remaining_epsilon:.4f}")
    manager.notify_admin("Privacy budget critical")
```

### Environment-Specific Overrides

```bash
# Override privacy settings via environment
export PRIVACY_EPSILON=0.5
export PRIVACY_K=10
export PRIVACY_AUDIT_LOG="/var/log/privacy_audit.log"
export PRIVACY_MAX_RISK=0.01
```

---

## Architecture Patterns

### Layered Defense Architecture

The module implements a layered defense model where each technique addresses a specific threat vector:

```python
from privacy_preservation import LayeredDefense, Anonymizer

# Define a layered defense configuration
defense = LayeredDefense(
    layers=[
        {"technique": "k-anonymity", "k": 5, "quasi_identifiers": ["age", "zip"]},
        {"technique": "l-diversity", "l": 3, "sensitive_attrs": ["diagnosis"]},
        {"technique": "t-closeness", "t": 0.2, "sensitive_attrs": ["diagnosis"]},
        {"technique": "differential_privacy", "epsilon": 0.5, "mechanism": "laplace"}
    ]
)

# Apply layers in sequence
protected_data = defense.apply(raw_data)
```

### Budget Management Pattern

```python
from privacy_preservation import PrivacyBudgetManager, QueryProcessor

# Centralized budget management
budget = PrivacyBudgetManager(total_epsilon=10.0)

# Multiple query processors share the budget
query1 = QueryProcessor(budget_manager=budget, cost_per_query=0.1)
query2 = QueryProcessor(budget_manager=budget, cost_per_query=0.2)

# Each query checks budget before execution
result1 = query1.execute("SELECT AVG(age) FROM patients")
result2 = query2.execute("SELECT COUNT(*) FROM patients WHERE diagnosis='X'")
```

### Audit Trail Pattern

```python
from privacy_preservation import AuditTrail

audit = AuditTrail(
    storage="postgres",
    connection_string="postgresql://localhost/audit_db",
    immutable=True
)

# Every transformation is logged
with audit.transaction("dataset_release_v1") as tx:
    tx.log_transformation("k-anonymity", {"k": 5, "columns": ["age", "zip"]})
    tx.log_transformation("noise_injection", {"epsilon": 0.5})
    tx.log_output_hash(dataset_hash)
    tx.log_metadata({"release_purpose": "research", "recipient": "university"})
```

### Plugin Architecture

```python
from privacy_preservation import PluginRegistry

@PluginRegistry.register("custom_anonymizer")
class CustomAnonymizer:
    def __init__(self, config):
        self.config = config

    def fit_transform(self, data):
        # Custom anonymization logic
        return anonymized_data

    def get_privacy_guarantee(self):
        return {"method": "custom", "epsilon": self.config.epsilon}
```

---

## Integration Guide

### Integration with Data Generation

```python
from data_generation import TabularGenerator
from privacy_preservation import DPSGDOptimizer

# Generate data with privacy guarantees
generator = TabularGenerator(model_type="ctgan")

# Wrap with DP-SGD for private training
dp_optimizer = DPSGDOptimizer(
    model=generator,
    noise_multiplier=1.1,
    max_grad_norm=1.0,
    batch_size=256
)

# Train with privacy budget
dp_optimizer.train(
    epochs=50,
    real_data=sensitive_data,
    epsilon_budget=1.0
)

# Generate private synthetic data
private_synthetic = generator.generate(n_samples=10000)
```

### Integration with Quality Validation

```python
from quality_validation import ValidationSuite
from privacy_preservation import Anonymizer

# Anonymize data
anonymizer = Anonymizer(method="k-anonymity", k=5)
anonymized_data = anonymizer.fit_transform(
    raw_data,
    quasi_identifiers=["age", "zip", "gender"]
)

# Validate quality after anonymization
validator = ValidationSuite(
    real_data=raw_data,
    synthetic_data=anonymized_data
)

# Check privacy-utility tradeoff
report = validator.generate_report()
print(f"Utility retention: {report['utility_ratio']:.2%}")
print(f"Privacy risk: {report['reidentification_risk']:.2%}")
```

### Integration with Apache Spark

```python
from privacy_preservation import SparkAnonymizer

# Distributed anonymization
spark_anon = SparkAnonymizer(
    method="k-anonymity",
    k=5,
    partitions=10
)

# Anonymize a Spark DataFrame
anonymized_df = spark_anon.fit_transform(
    spark_data,
    quasi_identifiers=["age", "zip"]
)
```

### Integration with Streaming Systems

```python
from privacy_preservation import StreamingAnonymizer
import kafka

# Configure streaming anonymizer
stream_anon = StreamingAnonymizer(
    method="k-anonymity",
    k=5,
    window_size=1000,
    flush_interval=60
)

# Kafka consumer/producer integration
consumer = kafka.KafkaConsumer("raw_data")
producer = kafka.KafkaProducer("anonymized_data")

for message in consumer:
    anonymized = stream_anon.process_record(message.value)
    if anonymized is not None:
        producer.send("anonymized_data", anonymized)
```

---

## Performance Optimization

### Batch Processing

```python
from privacy_preservation import BatchAnonymizer

# Process data in batches for large datasets
batch_anon = BatchAnonymizer(
    method="k-anonymity",
    k=5,
    batch_size=10000,
    n_workers=8
)

# Anonymize in parallel batches
anonymized_data = batch_anon.fit_transform(large_dataset)
```

### Caching Strategies

```python
from privacy_preservation import CacheConfig, Anonymizer

cache_config = CacheConfig(
    enabled=True,
    cache_dir="/tmp/privacy_cache",
    max_size_gb=5,
    ttl_hours=24
)

anonymizer = Anonymizer(
    method="k-anonymity",
    k=5,
    cache_config=cache_config
)

# Repeated transformations use cached results
anonymized = anonymizer.fit_transform(data)  # Computes and caches
anonymized = anonymizer.transform(new_data)  # Reuses cached generalization
```

### GPU Acceleration for DP-SGD

```python
from privacy_preservation import DPSGDOptimizer, GPUConfig

gpu_config = GPUConfig(
    device="cuda:0",
    mixed_precision=True,
    memory_fraction=0.8
)

dp_optimizer = DPSGDOptimizer(
    model=generator,
    gpu_config=gpu_config,
    noise_multiplier=1.1,
    max_grad_norm=1.0
)
```

### Incremental Processing

```python
from privacy_preservation import IncrementalAnonymizer

# Process streaming data incrementally
incremental_anon = IncrementalAnonymizer(
    method="k-anonymity",
    k=5,
    window_size=1000,
    merge_strategy="sliding"
)

# Process records one at a time
for record in data_stream:
    anonymized = incremental_anon.process(record)
    if anonymized:
        output_queue.put(anonymized)
```

---

## Security Considerations

### Key Management

```python
from privacy_preservation import KeyManager

# Manage encryption keys for stored anonymized data
key_manager = KeyManager(
    backend="aws-kms",
    key_rotation_days=90,
    key_deletion_days=365
)

# Generate and store encryption key
key_id = key_manager.create_key(
    purpose="anonymized_data_encryption",
    description="Key for encrypting patient records"
)
```

### Secure Deletion

```python
from privacy_preservation import SecureDeletion

# Securely delete original data after anonymization
deleter = SecureDeletion(
    method="dod_5220_22_m",  # DoD standard
    passes=3,
    verify=True
)

# Delete original data after successful anonymization
if anonymization_successful:
    deleter.delete("original_data.csv")
    print("Original data securely deleted")
```

### Access Control

```python
from privacy_preservation import AccessControl

acl = AccessControl()
acl.add_policy(
    resource="anonymized_patients",
    allowed_roles=["researcher", "analyst"],
    conditions={
        "max_queries_per_hour": 100,
        "require_approval": False,
        "allowed_aggregations": ["count", "mean", "median"]
    }
)

# Check access before query
if acl.authorize(user="researcher_1", resource="anonymized_patients"):
    result = execute_query(query)
```

### Tamper Detection

```python
from privacy_preservation import TamperDetection

tamper_detector = TamperDetection(
    algorithm="sha256",
    store_path="/var/lib/tamper_hashes"
)

# Store hash before transformation
original_hash = tamper_detector.store_hash(data, identifier="dataset_v1")

# Verify integrity after transformation
is_valid = tamper_detector.verify_hash(
    transformed_data,
    identifier="dataset_v1",
    original_hash=original_hash
)

if not is_valid:
    raise SecurityError("Data tampering detected")
```

---

## Troubleshooting Guide

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Privacy budget exhausted` | Cumulative epsilon exceeded | Reduce query frequency, increase delta, or reset budget |
| `k-anonymity not achievable` | Too many unique quasi-identifier combinations | Increase generalization or suppress more records |
| `l-diversity violation` | Insensitive attribute diversity in equivalence classes | Increase generalization level or suppress groups |
| `Noise too large` | DP epsilon too small | Increase epsilon or reduce query sensitivity |
| `Re-identification risk too high` | Synthetic data too similar to original | Apply stricter anonymization or reduce data fidelity |

### Debug Mode

```python
from privacy_preservation import Anonymizer, DebugConfig

debug_config = DebugConfig(
    verbose=True,
    log_level="DEBUG",
    save_intermediate=True,
    intermediate_path="/tmp/debug/",
    profile_operations=True
)

anonymizer = Anonymizer(
    method="k-anonymity",
    k=5,
    debug_config=debug_config
)
```

### Validation Diagnostics

```python
from privacy_preservation import DiagnosticTools

# Run diagnostic checks
diagnostics = DiagnosticTools.run(
    data=anonymized_data,
    original_data=raw_data,
    checks=[
        "k_anonymity_satisfied",
        "l_diversity_satisfied",
        "t_closeness_satisfied",
        "reidentification_risk",
        "information_loss"
    ]
)

for check in diagnostics:
    if not check.passed:
        print(f"FAILED: {check.name} - {check.message}")
```

### Performance Profiling

```python
from privacy_preservation import Profiler

profiler = Profiler()

with profiler:
    anonymizer.fit_transform(data)

profiler.print_report()
# Output includes:
# - Transformation time breakdown
# - Memory usage
# - Per-step timing
```

---

## API Reference

### Anonymizer

```python
class Anonymizer:
    """Apply anonymization techniques to data."""

    def __init__(
        self,
        method: str = "k-anonymity",
        k: int = 5,
        l: int = None,
        t: float = None,
        epsilon: float = None,
        delta: float = None,
        quasi_identifiers: list[str] = None,
        sensitive_attributes: list[str] = None,
        suppression_threshold: float = None,
        generalization_hierarchies: dict = None,
        config: PrivacyConfig = None
    ):
        """Initialize the anonymizer.

        Args:
            method: Anonymization method ("k-anonymity", "l-diversity", etc.)
            k: k-anonymity parameter
            l: l-diversity parameter
            t: t-closeness parameter
            epsilon: Differential privacy budget
            delta: Differential privacy delta
            quasi_identifiers: List of quasi-identifier column names
            sensitive_attributes: List of sensitive column names
            suppression_threshold: Minimum group size threshold
            generalization_hierarchies: Custom generalization rules
            config: PrivacyConfig object
        """
        pass

    def fit(
        self,
        data: pd.DataFrame,
        quasi_identifiers: list[str] = None,
        sensitive_attributes: list[str] = None
    ) -> "Anonymizer":
        """Fit the anonymizer to data.

        Args:
            data: Input DataFrame
            quasi_identifiers: Quasi-identifier columns
            sensitive_attributes: Sensitive columns

        Returns:
            self
        """
        pass

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply fitted anonymization to data.

        Args:
            data: Input DataFrame

        Returns:
            Anonymized DataFrame
        """
        pass

    def fit_transform(
        self,
        data: pd.DataFrame,
        quasi_identifiers: list[str] = None,
        sensitive_attributes: list[str] = None
    ) -> pd.DataFrame:
        """Fit and transform in one step.

        Args:
            data: Input DataFrame
            quasi_identifiers: Quasi-identifier columns
            sensitive_attributes: Sensitive columns

        Returns:
            Anonymized DataFrame
        """
        pass
```

### PrivacyBudgetManager

```python
class PrivacyBudgetManager:
    """Track and manage differential privacy budget."""

    def __init__(
        self,
        total_epsilon: float,
        total_delta: float = 1e-5,
        strategy: str = "sequential"
    ):
        """Initialize budget manager.

        Args:
            total_epsilon: Total privacy budget
            total_delta: Total delta budget
            strategy: Composition strategy ("sequential", "advanced", "rdp")
        """
        pass

    @property
    def remaining_epsilon(self) -> float:
        """Remaining epsilon budget."""
        pass

    @property
    def remaining_delta(self) -> float:
        """Remaining delta budget."""
        pass

    def check_budget(self, cost: float) -> bool:
        """Check if we have budget for a query.

        Args:
            cost: Epsilon cost of the query

        Returns:
            True if budget available
        """
        pass

    def spend(self, cost: float) -> None:
        """Spend privacy budget.

        Args:
            cost: Epsilon cost to spend
        """
        pass

    def get_usage_history(self) -> list[dict]:
        """Get history of budget usage."""
        pass
```

### ReIdentificationRiskAssessor

```python
class ReIdentificationRiskAssessor:
    """Assess re-identification risk of synthetic data."""

    def __init__(
        self,
        algorithm: str = "record_linkage",
        external_datasets: list[str] = None
    ):
        """Initialize risk assessor.

        Args:
            algorithm: Risk assessment algorithm
            external_datasets: Paths to external datasets for linkage testing
        """
        pass

    def assess(
        self,
        synthetic: pd.DataFrame,
        original: pd.DataFrame,
        quasi_identifiers: list[str]
    ) -> dict:
        """Assess re-identification risk.

        Args:
            synthetic: Synthetic dataset
            original: Original private dataset
            quasi_identifiers: Quasi-identifier columns

        Returns:
            Dict with risk metrics
        """
        pass

    def assess_membership_inference(
        self,
        model,
        train_data: pd.DataFrame,
        test_data: pd.DataFrame
    ) -> dict:
        """Assess membership inference risk.

        Args:
            model: Trained generative model
            train_data: Training data
            test_data: Holdout data

        Returns:
            Dict with inference risk metrics
        """
        pass
```

---

## Data Models

### PrivacyConfig Schema

```python
@dataclass
class PrivacyConfig:
    """Configuration for privacy preservation."""

    method: str = "k-anonymity"
    k: int = 5
    l: int = None
    t: float = None
    epsilon: float = None
    delta: float = None
    noise_multiplier: float = 1.1
    max_grad_norm: float = 1.0
    quasi_identifiers: list[str] = field(default_factory=list)
    sensitive_attributes: list[str] = field(default_factory=list)
    suppression_threshold: float = 0.05
    generalization_hierarchies: dict = field(default_factory=dict)
    audit_logging: bool = True
```

### AuditRecord Schema

```python
@dataclass
class AuditRecord:
    """Record of a privacy transformation."""

    record_id: str
    timestamp: datetime
    transformation_type: str
    parameters: dict
    input_hash: str
    output_hash: str
    operator: str
    privacy_guarantee: dict
    metadata: dict
```

### RiskReport Schema

```python
@dataclass
class RiskReport:
    """Re-identification risk assessment result."""

    average_risk: float
    max_risk: float
    risk_distribution: dict
    vulnerable_records: int
    total_records: int
    recommendations: list[str]
```

---

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /app/src/
COPY config/ /app/config/

WORKDIR /app

EXPOSE 8081

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
    CMD curl -f http://localhost:8081/health || exit 1

CMD ["python", "-m", "privacy_preservation.server", "--port", "8081"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: privacy-preservation-service
  namespace: synthetic-data
spec:
  replicas: 2
  selector:
    matchLabels:
      app: privacy-preservation
  template:
    metadata:
      labels:
        app: privacy-preservation
    spec:
      containers:
      - name: anonymizer
        image: synthetic-data/privacy:latest
        ports:
        - containerPort: 8081
        resources:
          requests:
            memory: "2Gi"
            cpu: "1"
          limits:
            memory: "4Gi"
            cpu: "2"
        env:
        - name: PRIVACY_EPSILON
          value: "1.0"
        - name: PRIVACY_AUDIT_LOG
          value: "/var/log/privacy_audit.log"
```

### REST API Server

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from privacy_preservation import Anonymizer, PrivacyConfig

app = FastAPI(title="Privacy Preservation API")

class AnonymizeRequest(BaseModel):
    data: list[dict]
    method: str = "k-anonymity"
    k: int = 5
    quasi_identifiers: list[str]
    sensitive_attributes: list[str]

@app.post("/anonymize")
async def anonymize_data(request: AnonymizeRequest):
    try:
        config = PrivacyConfig(
            method=request.method,
            k=request.k,
            quasi_identifiers=request.quasi_identifiers,
            sensitive_attributes=request.sensitive_attributes
        )
        anonymizer = Anonymizer(config=config)
        import pandas as pd
        data_df = pd.DataFrame(request.data)
        anonymized = anonymizer.fit_transform(data_df)
        return {"data": anonymized.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

---

## Monitoring & Observability

### Metrics Collection

```python
from privacy_preservation import MetricsCollector

metrics = MetricsCollector(
    backend="prometheus",
    port=9091,
    metrics=[
        "anonymization_duration_seconds",
        "records_processed_total",
        "privacy_budget_remaining",
        "reidentification_risk",
        "information_loss_ratio"
    ]
)

anonymizer = Anonymizer(
    method="k-anonymity",
    k=5,
    metrics_collector=metrics
)
```

### Audit Logging

```python
from privacy_preservation import AuditLogger

audit_logger = AuditLogger(
    log_path="/var/log/privacy_audit/",
    log_format="json",
    immutable=True,
    retention_days=2555  # 7 years for HIPAA
)

# All transformations are automatically logged
anonymizer = Anonymizer(
    method="k-anonymity",
    k=5,
    audit_logger=audit_logger
)
```

### Alerting Rules

```python
from privacy_preservation import AlertManager

alert_manager = AlertManager(
    rules=[
        {"metric": "privacy_budget_remaining", "threshold": 0.2, "severity": "critical"},
        {"metric": "reidentification_risk", "threshold": 0.05, "severity": "warning"},
        {"metric": "information_loss_ratio", "threshold": 0.5, "severity": "warning"}
    ],
    notification_channels=["slack", "email"]
)
```

### Dashboard Integration

```python
from privacy_preservation import DashboardExporter

exporter = DashboardExporter(
    format="grafana",
    output_path="/var/lib/grafana/dashboards/privacy.json"
)

exporter.generate_dashboard(
    metrics=["budget_usage", "risk_trends", "transformation_counts"],
    time_range="7d"
)
```

---

## Testing Strategy

### Unit Tests

```python
import pytest
import pandas as pd
import numpy as np
from privacy_preservation import Anonymizer, PrivacyBudgetManager

@pytest.fixture
def sample_data():
    np.random.seed(42)
    return pd.DataFrame({
        "age": np.random.randint(18, 80, 1000),
        "zip": np.random.randint(10000, 99999, 1000),
        "gender": np.random.choice(["M", "F"], 1000),
        "diagnosis": np.random.choice(["A", "B", "C", "D"], 1000)
    })

class TestAnonymizer:
    def test_k_anonymity_satisfied(self, sample_data):
        anon = Anonymizer(method="k-anonymity", k=5)
        anonymized = anon.fit_transform(
            sample_data,
            quasi_identifiers=["age", "zip", "gender"],
            sensitive_attributes=["diagnosis"]
        )
        # Check that every group has at least 5 records
        groups = anonymized.groupby(["age", "zip", "gender"]).size()
        assert groups.min() >= 5

    def test_l_diversity_satisfied(self, sample_data):
        anon = Anonymizer(method="l-diversity", k=5, l=3)
        anonymized = anon.fit_transform(
            sample_data,
            quasi_identifiers=["age", "zip", "gender"],
            sensitive_attributes=["diagnosis"]
        )
        # Check diversity in each group
        for _, group in anonymized.groupby(["age", "zip", "gender"]):
            assert group["diagnosis"].nunique() >= 3

class TestBudgetManager:
    def test_budget_depletion(self):
        budget = PrivacyBudgetManager(total_epsilon=1.0)
        for _ in range(10):
            budget.spend(cost=0.1)
        assert budget.remaining_epsilon <= 0.0

    def test_budget_check(self):
        budget = PrivacyBudgetManager(total_epsilon=1.0)
        assert budget.check_budget(cost=0.5) == True
        budget.spend(cost=0.6)
        assert budget.check_budget(cost=0.5) == False
```

### Integration Tests

```python
class TestFullPipeline:
    def test_anonymize_and_validate(self, sample_data):
        # Anonymize
        anon = Anonymizer(method="k-anonymity", k=5)
        anonymized = anon.fit_transform(
            sample_data,
            quasi_identifiers=["age", "zip", "gender"]
        )

        # Validate
        from quality_validation import ValidationSuite
        validator = ValidationSuite(
            real_data=sample_data,
            synthetic_data=anonymized
        )
        report = validator.generate_report()
        assert report["utility_ratio"] > 0.7
```

---

## Versioning & Migration

### Semantic Versioning

- **MAJOR**: Breaking API changes, incompatible audit logs
- **MINOR**: New anonymization techniques, backward-compatible
- **PATCH**: Bug fixes, performance improvements

### Audit Log Migration

```python
from privacy_preservation import AuditMigrator

migrator = AuditMigrator(
    source_version="1.2.0",
    target_version="2.0.0"
)

migrator.migrate_logs(
    source_path="/var/log/privacy_audit/v1/",
    target_path="/var/log/privacy_audit/v2/",
    schema_mappings={
        "old_field": "new_field"
    }
)
```

### Configuration Migration

```python
from privacy_preservation import ConfigMigrator

config_migrator = ConfigMigrator()
config_migrator.migrate(
    source="old_privacy_config.yaml",
    target="new_privacy_config.yaml"
)
```

---

## Glossary

| Term | Definition |
|------|------------|
| **k-Anonymity** | Each record is indistinguishable from at least k-1 others on quasi-identifiers |
| **l-Diversity** | Each equivalence class has at least l distinct values for sensitive attributes |
| **t-Closeness** | The distribution of sensitive attributes in each class is within t of the overall distribution |
| **Differential Privacy** | Mathematical framework providing provable privacy guarantees |
| **Epsilon** | Privacy budget parameter; smaller values mean stronger privacy |
| **Quasi-Identifier** | Attributes that can be combined to identify individuals (e.g., age, zip code) |
| **Sensitive Attribute** | Attributes that must be protected (e.g., medical diagnosis) |
| **Equivalence Class** | Set of records with the same quasi-identifier values |
| **Suppression** | Removing records that cannot be safely anonymized |
| **Generalization** | Replacing specific values with less precise ones (e.g., exact age to age range) |
| **Privacy Budget** | Cumulative privacy loss allowed across multiple data releases |
| **Re-identification Risk** | Probability of linking a synthetic record back to a real individual |

---

## Changelog

### v1.0.0 (2024-01-15)
- Initial release with k-anonymity, l-diversity, t-closeness
- Differential privacy with Laplace and Gaussian mechanisms
- Privacy budget management
- Re-identification risk assessment
- Audit logging

### v1.1.0 (2024-03-01)
- DP-SGD integration for generative model training
- Streaming anonymization support
- Custom generalization hierarchies
- Performance improvements for large datasets

### v1.2.0 (2024-05-15)
- Advanced composition theorems for tighter privacy bounds
- Spark integration for distributed anonymization
- Enhanced audit logging with tamper detection
- REST API for anonymization-as-a-service

### v1.3.0 (2024-08-01)
- Membership inference risk assessment
- Kubernetes deployment templates
- Grafana dashboard integration
- Automated compliance reporting

---

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/privacy-preservation.git
cd privacy-preservation
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/
ruff check src/
ruff format src/
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints for all public functions
- Write docstrings for all public classes and methods
- Keep functions under 50 lines
- Use meaningful variable names

### Pull Request Process

1. Create a feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Submit PR with clear description of changes

### Commit Message Format

```
type(scope): description

[optional body]

[optional footer]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

---

## License

Copyright (c) 2024 Synthetic Data Toolkit Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

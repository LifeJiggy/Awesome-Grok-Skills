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

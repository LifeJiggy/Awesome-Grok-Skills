---
name: "domain-specific"
category: "synthetic-data"
version: "1.0.0"
tags: ["synthetic-data", "healthcare", "finance", "iot", "automotive", "nlp", "legal", "scientific"]
---

# Domain-Specific Synthetic Data Toolkit

## Overview

The `domain-specific` module provides specialized generators, templates, and validation rules tailored to the unique requirements of various industrial and scientific sectors. Unlike generic synthetic data tools, these generators incorporate domain knowledge—such as ICD-10 medical codes, PCI-DSS compliant transaction formats, or Physically-Informed Neural Networks (PINNs) for sensor data—to ensure the generated data is not only statistically plausible but also structurally and semantically valid for its specific use case.

For example, in the **Healthcare** domain, generating a patient record requires more than just randomizing ages and blood pressures; it requires maintaining logical consistency between diagnoses, medications, and lab results (e.g., a patient with a "Type 2 Diabetes" diagnosis should have corresponding "HbA1c" lab values and likely a "Metformin" prescription). This module enforces these "clinical logic" constraints during the generation process. Similarly, in the **Financial** sector, synthetic transaction data must follow strict regulatory formats and exhibit realistic fraud patterns to be useful for training detection systems without exposing actual customer financial behavior.

The module also extends into emerging fields like **Autonomous Driving** scenario generation and **Legal Document** synthesis. For automotive applications, it generates multi-modal sensor data (LiDAR, Camera, Radar) with synchronized ground-truth labels for edge cases (e.g., "pedestrian crossing in fog"). For legal tech, it creates synthetic case studies and contract clauses that preserve the linguistic structure and logical dependencies of real legal text while stripping all identifying information. By providing these domain-specific "recipes," the toolkit significantly reduces the time and expertise required to build high-quality synthetic datasets for specialized AI and testing applications.

Each domain generator includes built-in validation rules that automatically check the generated data for domain-specific consistency. For example, the healthcare generator validates that diagnosis codes are from valid ICD-10 subsets, that medication dosages fall within therapeutic ranges, and that temporal sequences (e.g., lab test → result → prescription) are logically ordered. The financial generator validates transaction amounts against typical distributions for each merchant category, checks that timestamps are within business hours for in-person transactions, and ensures that card-present/card-not-present flags are consistent with transaction amounts.

## Core Capabilities

*   **Healthcare Synthesis**: Generate realistic EHR (Electronic Health Record) data with consistent patient demographics, longitudinal visit histories, and logically linked diagnosis-procedure-medication codes.
*   **Financial Transaction Simulation**: Create synthetic bank transactions, credit card swipes, and trading data with embedded fraud patterns, regulatory-compliant metadata, and realistic temporal distributions.
*   **IoT Sensor Data Generation**: Simulate multi-variate sensor streams (temperature, pressure, vibration) with configurable noise, drift, and intermittent fault patterns for predictive maintenance training.
*   **Automotive Scenario Generation**: Generate synchronized camera, LiDAR, and radar data for ADAS (Advanced Driver Assistance Systems) testing, including rare "long-tail" edge cases.
*   **Legal & Compliance Text**: Synthesize legal documents, contracts, and regulatory filings using structural templates and controlled language models to preserve legal logic without privacy risks.
*   **Scientific Experimental Data**: Generate synthetic lab results, clinical trial data, and material science measurements following physical laws and experimental constraints.
*   **Dialogue & Conversational Data**: Create synthetic multi-turn dialogues for training customer service bots or virtual assistants, with configurable personas and intent flows.
*   **Code Generation Datasets**: Synthesize programming problems, code snippets, and unit tests for training or fine-tuning Large Language Models (LLMs) for code completion.

## Domain Architecture

```
┌─────────────────────────────────────────────────┐
│            Domain Generators                     │
│  HealthcareGenerator  FinancialGenerator         │
│  IoTSensorGenerator   AutomotiveGenerator        │
│  LegalGenerator       ScientificGenerator        │
├─────────────────────────────────────────────────┤
│          Domain Validation Layer                 │
│  ClinicalLogicChecker  FraudPatternValidator     │
│  PhysicsConstraints    LegalStructureValidator   │
├─────────────────────────────────────────────────┤
│         Ontology & Reference Data                │
│  ICD-10  RxNorm  LOINC  CPT  PCI-DSS  FIX       │
├─────────────────────────────────────────────────┤
│          Core Generation Engine                  │
│  CTGAN  GaussianCopula  TVAE  ARIMA  Diffusion  │
└─────────────────────────────────────────────────┘
```

## Usage Examples

### 1. Healthcare: Longitudinal Patient Records

```python
from domain_specific import HealthcareGenerator

# Initialize with a specific medical ontology (e.g., ICD-10, RxNorm)
hc_gen = HealthcareGenerator(
    ontology="icd10",
    n_patients=1000,
    avg_visits_per_year=4,
    start_date="2022-01-01",
    end_date="2023-12-31"
)

# Generate a cohort with a specific prevalence of comorbidities
patient_cohort = hc_gen.generate_cohort(
    conditions={"diabetes_prevalence": 0.15, "hypertension_prevalence": 0.30}
)

# Export to OMOP CDM format
patient_cohort.to_omop("synthetic_cohort.omop")
```

### 2. Financial: Fraud Detection Training Data

```python
from domain_specific import FinancialGenerator

# Configure a credit card transaction generator
fin_gen = FinancialGenerator(
    n_customers=5000,
    transaction_frequency="daily",
    fraud_rate=0.01  # 1% of transactions are fraudulent
)

# Generate transactions with specific fraud patterns
transactions = fin_gen.generate(
    fraud_patterns=["card_testing", "account_takeover", "geo_impossibility"]
)

# Ensure data is PCI-DSS compliant (PAN masking, etc.)
transactions = fin_gen.apply_pci_masking(transactions)
```

### 3. IoT: Predictive Maintenance Sensor Streams

```python
from domain_specific import IoTSensorGenerator

# Simulate a turbine engine with 10 sensors
iot_gen = IoTSensorGenerator(
    n_sensors=10,
    frequency="100Hz",
    duration_hours=24
)

# Inject a "bearing degradation" fault starting at hour 12
sensor_data = iot_gen.generate_with_fault(
    fault_type="bearing_degradation",
    onset_hour=12,
    degradation_rate=0.05
)
```

### 4. Automotive: Edge Case Scenario Generation

```python
from domain_specific import AutomotiveGenerator

# Generate multi-modal sensor data for autonomous driving edge cases
auto_gen = AutomotiveGenerator(
    sensor_config=["camera", "lidar", "radar"],
    resolution=(1920, 1080),
    frame_rate=30
)

# Generate a "pedestrian crossing in fog" scenario
scenario = auto_gen.generate_scenario(
    scenario_type="pedestrian_crossing",
    weather="fog",
    visibility=50,  # meters
    pedestrian_count=1,
    duration_seconds=10
)

# Export with synchronized labels
scenario.export_nuscenes_format("edge_case_001/")
```

### 5. Legal: Contract Clause Synthesis

```python
from domain_specific import LegalGenerator

# Generate synthetic contract clauses for training a clause classifier
legal_gen = LegalGenerator(
    clause_types=["indemnification", "limitation_of_liability", "governing_law", "termination"],
    language="en-US",
    complexity="medium"
)

# Generate 500 synthetic indemnification clauses
clauses = legal_gen.generate(
    clause_type="indemnification",
    n_samples=500,
    include_annotations=True
)

# Export for NLP training
for clause in clauses:
    clause.to_jsonl("legal_training_data.jsonl")
```

### 6. Scientific: Clinical Trial Data

```python
from domain_specific import ScientificGenerator

# Generate synthetic clinical trial data following CONSORT guidelines
sci_gen = ScientificGenerator(
    trial_type="randomized_controlled",
    n_patients=500,
    arms=["treatment", "placebo"],
    endpoints=["primary_efficacy", "secondary_safety"]
)

# Generate with realistic dropout rates and adverse events
trial_data = sci_gen.generate_trial(
    dropout_rate=0.15,
    adverse_event_rate=0.08,
    treatment_effect_size=0.3
)

# Export to SDTM format
trial_data.to_sdtm("clinical_trial_sdtm/")
```

## Domain-Specific Validation Rules

### Healthcare Validation Rules

| Rule | Description | Error Severity |
|------|-------------|----------------|
| Valid ICD-10 Code | Diagnosis codes must exist in ICD-10-CM taxonomy | ERROR |
| Medication-Diagnosis Consistency | Patients with diabetes should have glucose-related labs | WARNING |
| Temporal Ordering | Lab results must follow test order dates | ERROR |
| Dosage Range Check | Medication dosages must fall within therapeutic ranges | WARNING |
| Age-Gender Consistency | Certain conditions have gender-specific prevalence | WARNING |
| Visit Continuity | Patient visits should not have large unexplained gaps | INFO |

### Financial Validation Rules

| Rule | Description | Error Severity |
|------|-------------|----------------|
| Transaction Amount Distribution | Amounts should follow log-normal for legitimate, heavy-tail for fraud | WARNING |
| Temporal Consistency | Card-present transactions should occur during business hours | WARNING |
| Geographic Feasibility | Successive transactions at distant locations within short time | ERROR (fraud indicator) |
| PCI-DSS Compliance | PAN must be masked (show only last 4 digits) | ERROR |
| Currency-Amount Consistency | Amounts must be positive and match currency conventions | ERROR |
| Merchant Category Alignment | Transaction patterns should align with merchant category codes | WARNING |

### IoT Validation Rules

| Rule | Description | Error Severity |
|------|-------------|----------------|
| Physical Bounds | Sensor readings must stay within physically plausible ranges | ERROR |
| Sampling Rate Consistency | Timestamps must reflect configured sampling frequency | WARNING |
| Correlation Preservation | Related sensors (e.g., temperature and pressure) should show expected correlation | WARNING |
| Fault Signature Match | Injected faults should match known degradation patterns | WARNING |
| Missing Data Patterns | Missing values should follow realistic patterns (burst vs. random) | INFO |

## Best Practices

1.  **Respect Domain Constraints**: Always validate generated data against domain-specific rules (e.g., a heart rate cannot be negative, a diagnosis code must be valid) before use.
2.  **Collaborate with Experts**: Work with clinicians, financial analysts, or engineers to verify that the generated scenarios are realistic and cover the necessary edge cases.
3.  **Use Standard Formats**: Where possible, export synthetic data in industry-standard formats (e.g., OMOP for healthcare, FIX for finance) to ensure compatibility with existing tools.
4.  **Simulate Rare Events**: For safety-critical applications (like autonomous driving), explicitly generate "edge cases" that are rare in real data but essential for model robustness.
5.  **Audit for Bias**: Ensure that the synthetic data does not amplify existing biases in the training data (e.g., under-representing certain demographics in medical data).
6.  **Maintain Temporal Logic**: For time-series domains (healthcare, IoT), ensure that the sequence of events is logically sound (e.g., a lab test result must follow the test order).
7.  **Version Your Generators**: Treat your domain-specific generator code as a first-class asset, versioning it alongside your models to ensure reproducibility.
8. **Run Domain Validators**: Never skip the domain-specific validation step. A statistically sound dataset that violates domain constraints is worse than useless—it can lead to incorrect conclusions.
9. **Engage Stakeholders Early**: Before generating data, confirm with domain experts which attributes, distributions, and edge cases are most important for the downstream use case.
10. **Document Assumptions**: Maintain a record of all assumptions made during generation (e.g., fraud rate assumptions, disease prevalence rates) so that consumers of the data understand its limitations.

## Related Modules

*   [data-generation](../data-generation/GROK.md): The underlying generative engines (CTGAN, VAE) used by these domain-specific wrappers.
*   [privacy-preservation](../privacy-preservation/GROK.md): Advanced anonymization for sensitive domain data (e.g., HIPAA for healthcare).
*   [quality-validation](../quality-validation/GROK.md): Domain-specific validation metrics (e.g., clinical logic checks).
*   [augmentation](../augmentation/GROK.md): Domain-aware augmentation techniques for existing domain datasets.

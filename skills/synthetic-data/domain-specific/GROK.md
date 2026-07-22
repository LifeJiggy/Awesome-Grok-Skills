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

---

## Advanced Configuration

The `domain-specific` module supports detailed configuration of every domain generator through YAML files or programmatic APIs.

### Configuration File Format

```yaml
# domain_config.yaml
healthcare:
  ontology: "icd10"
  n_patients: 10000
  avg_visits_per_year: 4
  start_date: "2022-01-01"
  end_date: "2023-12-31"
  comorbidities:
    diabetes_prevalence: 0.15
    hypertension_prevalence: 0.30
  output_format: "omop"
  validation_rules: "strict"

financial:
  n_customers: 50000
  transaction_frequency: "daily"
  fraud_rate: 0.01
  fraud_patterns:
    - "card_testing"
    - "account_takeover"
    - "geo_impossibility"
  pci_compliance: true
  output_format: "parquet"

iot:
  n_sensors: 20
  frequency: "100Hz"
  duration_hours: 48
  fault_injection:
    enabled: true
    fault_types: ["bearing_degradation", "motor_failure"]
    onset_hours: [12, 24]

automotive:
  sensor_config: ["camera", "lidar", "radar"]
  resolution: [1920, 1080]
  frame_rate: 30
  scenario_types: ["pedestrian_crossing", "vehicle_cut_in"]
  weather_conditions: ["clear", "fog", "rain", "night"]

legal:
  clause_types:
    - "indemnification"
    - "limitation_of_liability"
    - "governing_law"
    - "termination"
  language: "en-US"
  complexity: "medium"
  include_annotations: true

scientific:
  trial_type: "randomized_controlled"
  n_patients: 500
  arms: ["treatment", "placebo"]
  endpoints: ["primary_efficacy", "secondary_safety"]
  dropout_rate: 0.15
  adverse_event_rate: 0.08
```

### Programmatic Configuration

```python
from domain_specific import DomainConfig, HealthcareGenerator

config = DomainConfig(
    healthcare=HealthcareConfig(
        ontology="icd10",
        n_patients=10000,
        avg_visits_per_year=4,
        start_date="2022-01-01",
        end_date="2023-12-31",
        comorbidities={
            "diabetes_prevalence": 0.15,
            "hypertension_prevalence": 0.30
        },
        output_format="omop",
        validation_rules="strict"
    )
)

generator = HealthcareGenerator(config=config.healthcare)
```

### Environment-Specific Overrides

```bash
# Override domain settings via environment
export DOMAIN_HEALTHCARE_ONTOLOGY="icd10"
export DOMAIN_HEALTHCARE_N_PATIENTS=10000
export DOMAIN_FINANCIAL_FRAUD_RATE=0.01
export DOMAIN_IOT_FREQUENCY="100Hz"
export DOMAIN_AUTOMOTIVE_RESOLUTION="1920x1080"
export DOMAIN_LEGAL_LANGUAGE="en-US"
export DOMAIN_SCIENTIFIC_TRIAL_TYPE="randomized_controlled"
```

### Dynamic Configuration Updates

```python
from domain_specific import DynamicConfigManager

config_manager = DynamicConfigManager(config_path="domain_config.yaml")

# Register callbacks for configuration changes
@config_manager.on_change("healthcare.n_patients")
def update_patient_count(new_value):
    print(f"Patient count updated to {new_value}")
    generator.update_config(n_patients=new_value)

# Hot-reload configuration
config_manager.reload()
```

---

## Architecture Patterns

### Domain Registry Pattern

The module uses a registry pattern to manage domain-specific generators.

```python
from domain_specific import DomainRegistry

# Register custom domain generator
@DomainRegistry.register("custom_domain")
class CustomDomainGenerator:
    def __init__(self, config):
        self.config = config

    def generate(self, **kwargs):
        # Custom generation logic
        return generated_data

    def validate(self, data):
        # Custom validation logic
        return validation_results

# Get generator from registry
generator = DomainRegistry.get("healthcare", config=healthcare_config)
```

### Strategy Pattern for Domain Logic

```python
from domain_specific import StrategyFactory

# Create domain-specific strategies
factory = StrategyFactory()

healthcare_strategy = factory.create("healthcare", config={
    "ontology": "icd10",
    "validation_rules": "strict"
})

financial_strategy = factory.create("financial", config={
    "pci_compliance": True,
    "fraud_rate": 0.01
})

# Apply appropriate strategy based on domain
for dataset in datasets:
    if dataset.domain == "healthcare":
        validated = healthcare_strategy.validate(dataset)
    elif dataset.domain == "financial":
        validated = financial_strategy.validate(dataset)
```

### Observer Pattern for Monitoring

```python
from domain_specific import DomainGenerator, DomainObserver

class DomainMonitor(DomainObserver):
    def on_generation_complete(self, domain, n_records, duration):
        print(f"Generated {n_records} {domain} records in {duration:.2f}s")

    def on_validation_complete(self, domain, results):
        print(f"Validation for {domain}: {results['passed']}/{results['total']} rules passed")

generator = HealthcareGenerator(config=config)
generator.add_observer(DomainMonitor())
```

### Plugin Architecture

```python
from domain_specific import PluginRegistry

@PluginRegistry.register("custom_domain")
class CustomDomainPlugin:
    def __init__(self, config):
        self.config = config

    def generate(self, **kwargs):
        # Custom generation logic
        return generated_data

    def validate(self, data):
        # Custom validation logic
        return validation_results

    def export(self, data, format):
        # Custom export logic
        pass
```

---

## Integration Guide

### Integration with Data Generation

```python
from data_generation import TabularGenerator
from domain_specific import HealthcareGenerator

# Use domain-specific generator with core generation engine
hc_gen = HealthcareGenerator(
    ontology="icd10",
    n_patients=1000
)

# Generate domain-specific data
patient_data = hc_gen.generate_cohort(
    conditions={"diabetes_prevalence": 0.15}
)

# Use core generator for additional synthesis
tabular_gen = TabularGenerator(model_type="ctgan")
tabular_gen.fit(patient_data["labs"])
additional_labs = tabular_gen.generate(n_samples=5000)
```

### Integration with Privacy Preservation

```python
from privacy_preservation import Anonymizer
from domain_specific import HealthcareGenerator

# Generate healthcare data
hc_gen = HealthcareGenerator(ontology="icd10", n_patients=1000)
patient_data = hc_gen.generate_cohort()

# Anonymize sensitive fields
anonymizer = Anonymizer(method="k-anonymity", k=5)
anonymized_data = anonymizer.fit_transform(
    patient_data,
    quasi_identifiers=["age", "zip", "gender"],
    sensitive_attributes=["diagnosis", "treatment"]
)
```

### Integration with Quality Validation

```python
from quality_validation import ValidationSuite
from domain_specific import FinancialGenerator

# Generate financial data
fin_gen = FinancialGenerator(n_customers=5000, fraud_rate=0.01)
transactions = fin_gen.generate()

# Validate domain-specific rules
suite = ValidationSuite(
    real_data=real_transactions,
    synthetic_data=transactions,
    metrics=["domain_compliance", "distribution_fidelity"]
)

report = suite.generate_report()
```

### Integration with Apache Spark

```python
from domain_specific import SparkDomainGenerator

# Distributed domain-specific generation
spark_gen = SparkDomainGenerator(
    domain="healthcare",
    partitions=10,
    executor_memory="4g"
)

# Generate from Spark DataFrame
synthetic_df = spark_gen.generate(
    real_spark_df,
    n_samples=100000,
    output_path="s3://bucket/synthetic/"
)
```

---

## Performance Optimization

### Parallel Generation

```python
from domain_specific import ParallelDomainGenerator

# Generate data in parallel across multiple cores
parallel_gen = ParallelDomainGenerator(
    domain="healthcare",
    n_workers=8,
    chunk_size=1000
)

# Each worker generates a portion of the data
patient_data = parallel_gen.generate(n_patients=10000)
```

### Caching Strategies

```python
from domain_specific import CacheConfig, HealthcareGenerator

cache_config = CacheConfig(
    enabled=True,
    cache_dir="/tmp/domain_cache",
    max_size_gb=10,
    ttl_hours=24
)

generator = HealthcareGenerator(
    ontology="icd10",
    cache_config=cache_config
)

# Repeated generations use cached reference data
patient_data = generator.generate_cohort()  # Computes and caches
patient_data = generator.generate_cohort()  # Uses cache
```

### Memory-Efficient Processing

```python
from domain_specific import MemoryEfficientGenerator

# Generate data that doesn't fit in memory
generator = MemoryEfficientGenerator(
    domain="financial",
    chunk_size=10000,
    spill_to_disk=True,
    spill_path="/tmp/domain_spill"
)

# Process in chunks
for chunk in generator.generate_chunks(n_customers=100000):
    chunk.to_parquet(f"synthetic_{chunk.name}.parquet")
```

### GPU Acceleration

```python
from domain_specific import GPUDomainGenerator

gpu_generator = GPUDomainGenerator(
    domain="automotive",
    device="cuda:0",
    mixed_precision=True
)

# Generate sensor data on GPU
sensor_data = gpu_generator.generate(n_scenarios=1000)
```

---

## Security Considerations

### Data Encryption

```python
from domain_specific import EncryptionConfig, HealthcareGenerator

# Encrypt generated data at rest
encryption_config = EncryptionConfig(
    algorithm="AES-256-GCM",
    key_management="aws-kms",
    kms_key_id="arn:aws:kms:us-east-1:123456789012:key/abc-def"
)

generator = HealthcareGenerator(
    ontology="icd10",
    encryption_config=encryption_config
)

# Generated data is automatically encrypted
patient_data = generator.generate_cohort()
```

### Access Control

```python
from domain_specific import AccessControl

acl = AccessControl()
acl.add_policy(
    resource="healthcare_data",
    allowed_roles=["clinician", "researcher"],
    conditions={
        "require_irb_approval": True,
        "max_records_per_query": 10000
    }
)

# Check access before generation
if acl.authorize(user="researcher_1", resource="healthcare_data"):
    patient_data = generator.generate_cohort()
```

### Audit Logging

```python
from domain_specific import AuditLogger

audit_logger = AuditLogger(
    log_path="/var/log/domain_audit/",
    log_format="json",
    capture_inputs=True,
    capture_outputs_hash=True,
    retention_days=2555  # 7 years for HIPAA
)

generator = HealthcareGenerator(
    ontology="icd10",
    audit_logger=audit_logger
)
```

### Secure Model Storage

```python
from domain_specific import SecureSerializer

# Save generator with integrity verification
serializer = SecureSerializer(
    signing_key="path/to/private_key.pem",
    checksum_algorithm="sha256"
)

generator.save("healthcare_generator.pt", serializer=serializer)

# Load with integrity verification
loaded_generator = HealthcareGenerator.load(
    "healthcare_generator.pt",
    serializer=serializer,
    verify_integrity=True
)
```

---

## Troubleshooting Guide

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Invalid ICD-10 code` | Generated diagnosis code not in taxonomy | Check ontology configuration, update reference data |
| `Medication-diagnosis mismatch` | Generated prescription doesn't match diagnosis | Enable clinical logic validation |
| `PCI-DSS violation` | Generated transaction not PCI compliant | Enable PCI compliance checks |
| `Physical bounds exceeded` | Sensor reading outside plausible range | Configure physical constraints |
| `Temporal ordering error` | Event sequence logically invalid | Enable temporal validation |

### Debug Mode

```python
from domain_specific import HealthcareGenerator, DebugConfig

debug_config = DebugConfig(
    verbose=True,
    log_level="DEBUG",
    save_intermediate=True,
    intermediate_path="/tmp/debug/",
    profile_operations=True
)

generator = HealthcareGenerator(
    ontology="icd10",
    debug_config=debug_config
)
```

### Validation Diagnostics

```python
from domain_specific import DiagnosticTools

# Run diagnostic checks on generated data
diagnostics = DiagnosticTools.run(
    data=generated_data,
    domain="healthcare",
    checks=["clinical_logic", "temporal_ordering", "code_validity"]
)

for check in diagnostics:
    if not check.passed:
        print(f"FAILED: {check.name} - {check.message}")
        print(f"  Recommendation: {check.suggestion}")
```

### Performance Profiling

```python
from domain_specific import Profiler

profiler = Profiler()

with profiler:
    patient_data = generator.generate_cohort(n_patients=10000)

profiler.print_report()
# Output includes:
# - Generation time breakdown
# - Memory usage
# - Validation time
# - Export time
```

---

## API Reference

### HealthcareGenerator

```python
class HealthcareGenerator:
    """Generate realistic healthcare data."""

    def __init__(
        self,
        ontology: str = "icd10",
        n_patients: int = 1000,
        avg_visits_per_year: int = 4,
        start_date: str = "2022-01-01",
        end_date: str = "2023-12-31",
        config: HealthcareConfig = None
    ):
        """Initialize healthcare generator.

        Args:
            ontology: Medical coding system ("icd10", "snomed")
            n_patients: Number of patients to generate
            avg_visits_per_year: Average visits per patient per year
            start_date: Start date for generated records
            end_date: End date for generated records
            config: HealthcareConfig object
        """
        pass

    def generate_cohort(
        self,
        conditions: dict = None,
        demographics: dict = None
    ) -> dict:
        """Generate a patient cohort.

        Args:
            conditions: Disease prevalence rates
            demographics: Demographic distributions

        Returns:
            Dict with patient, visit, diagnosis, medication tables
        """
        pass

    def to_omop(self, output_path: str) -> None:
        """Export to OMOP CDM format.

        Args:
            output_path: Output directory path
        """
        pass

    def validate(self, data: dict) -> dict:
        """Validate generated data against clinical rules.

        Args:
            data: Generated healthcare data

        Returns:
            Validation results
        """
        pass
```

### FinancialGenerator

```python
class FinancialGenerator:
    """Generate realistic financial transaction data."""

    def __init__(
        self,
        n_customers: int = 5000,
        transaction_frequency: str = "daily",
        fraud_rate: float = 0.01,
        config: FinancialConfig = None
    ):
        """Initialize financial generator.

        Args:
            n_customers: Number of customers
            transaction_frequency: Transaction frequency
            fraud_rate: Proportion of fraudulent transactions
            config: FinancialConfig object
        """
        pass

    def generate(
        self,
        fraud_patterns: list[str] = None,
        merchant_categories: list[str] = None
    ) -> pd.DataFrame:
        """Generate transaction data.

        Args:
            fraud_patterns: Fraud patterns to include
            merchant_categories: Merchant categories to simulate

        Returns:
            DataFrame with transactions
        """
        pass

    def apply_pci_masking(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply PCI-DSS compliant masking.

        Args:
            data: Transaction data

        Returns:
            Masked transaction data
        """
        pass

    def validate(self, data: pd.DataFrame) -> dict:
        """Validate generated data against financial rules.

        Args:
            data: Generated transaction data

        Returns:
            Validation results
        """
        pass
```

### IoTSensorGenerator

```python
class IoTSensorGenerator:
    """Generate realistic IoT sensor data."""

    def __init__(
        self,
        n_sensors: int = 10,
        frequency: str = "100Hz",
        duration_hours: int = 24,
        config: IoTConfig = None
    ):
        """Initialize IoT sensor generator.

        Args:
            n_sensors: Number of sensors
            frequency: Sampling frequency
            duration_hours: Duration in hours
            config: IoTConfig object
        """
        pass

    def generate(self) -> pd.DataFrame:
        """Generate normal sensor data.

        Returns:
            DataFrame with sensor readings
        """
        pass

    def generate_with_fault(
        self,
        fault_type: str,
        onset_hour: int = 12,
        degradation_rate: float = 0.05
    ) -> pd.DataFrame:
        """Generate sensor data with injected faults.

        Args:
            fault_type: Type of fault to inject
            onset_hour: Hour when fault begins
            degradation_rate: Rate of degradation

        Returns:
            DataFrame with fault-injected sensor readings
        """
        pass

    def validate(self, data: pd.DataFrame) -> dict:
        """Validate generated data against physical constraints.

        Args:
            data: Generated sensor data

        Returns:
            Validation results
        """
        pass
```

---

## Data Models

### DomainConfig Schema

```python
@dataclass
class DomainConfig:
    """Configuration for domain-specific generation."""

    healthcare: HealthcareConfig = None
    financial: FinancialConfig = None
    iot: IoTConfig = None
    automotive: AutomotiveConfig = None
    legal: LegalConfig = None
    scientific: ScientificConfig = None
```

### HealthcareConfig Schema

```python
@dataclass
class HealthcareConfig:
    """Configuration for healthcare data generation."""

    ontology: str = "icd10"
    n_patients: int = 1000
    avg_visits_per_year: int = 4
    start_date: str = "2022-01-01"
    end_date: str = "2023-12-31"
    comorbidities: dict = field(default_factory=dict)
    output_format: str = "omop"
    validation_rules: str = "strict"
```

### DomainRecord Schema

```python
@dataclass
class DomainRecord:
    """Metadata about a domain-specific generation."""

    record_id: str
    domain: str
    timestamp: datetime
    n_records: int
    validation_results: dict
    output_format: str
    checksum: str
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
COPY reference_data/ /app/reference_data/

WORKDIR /app

EXPOSE 8084

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
    CMD curl -f http://localhost:8084/health || exit 1

CMD ["python", "-m", "domain_specific.server", "--port", "8084"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: domain-generation-service
  namespace: synthetic-data
spec:
  replicas: 3
  selector:
    matchLabels:
      app: domain-generation
  template:
    metadata:
      labels:
        app: domain-generation
    spec:
      containers:
      - name: generator
        image: synthetic-data/domain:latest
        ports:
        - containerPort: 8084
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
        env:
        - name: DOMAIN_DEFAULT
          value: "healthcare"
        - name: DOMAIN_ONTOLOGY_PATH
          value: "/app/reference_data/"
```

### REST API Server

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from domain_specific import HealthcareGenerator, FinancialGenerator

app = FastAPI(title="Domain Generation API")

class HealthcareRequest(BaseModel):
    n_patients: int = 1000
    ontology: str = "icd10"
    conditions: dict = None

class FinancialRequest(BaseModel):
    n_customers: int = 5000
    fraud_rate: float = 0.01

@app.post("/healthcare/generate")
async def generate_healthcare(request: HealthcareRequest):
    try:
        generator = HealthcareGenerator(
            ontology=request.ontology,
            n_patients=request.n_patients
        )
        data = generator.generate_cohort(conditions=request.conditions)
        return {"data": {k: v.to_dict() for k, v in data.items()}}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/financial/generate")
async def generate_financial(request: FinancialRequest):
    try:
        generator = FinancialGenerator(
            n_customers=request.n_customers,
            fraud_rate=request.fraud_rate
        )
        data = generator.generate()
        return {"data": data.to_dict()}
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
from domain_specific import MetricsCollector

metrics = MetricsCollector(
    backend="prometheus",
    port=9094,
    metrics=[
        "generation_duration_seconds",
        "records_generated_total",
        "validation_pass_rate",
        "domain_specific_errors_total"
    ]
)

generator = HealthcareGenerator(
    ontology="icd10",
    metrics_collector=metrics
)
```

### Audit Logging

```python
from domain_specific import AuditLogger

audit_logger = AuditLogger(
    log_path="/var/log/domain_audit/",
    log_format="json",
    capture_inputs=True,
    capture_outputs_hash=True,
    retention_days=2555  # 7 years for healthcare
)

generator = HealthcareGenerator(
    ontology="icd10",
    audit_logger=audit_logger
)
```

### Alerting Rules

```python
from domain_specific import AlertManager

alert_manager = AlertManager(
    rules=[
        {"metric": "validation_pass_rate", "threshold": 0.95, "severity": "critical", "operator": "lt"},
        {"metric": "generation_duration_seconds", "threshold": 300, "severity": "warning"},
        {"metric": "domain_specific_errors_total", "threshold": 10, "severity": "warning"}
    ],
    notification_channels=["slack", "email"]
)
```

### Dashboard Integration

```python
from domain_specific import DashboardExporter

exporter = DashboardExporter(
    format="grafana",
    output_path="/var/lib/grafana/dashboards/domain_generation.json"
)

exporter.generate_dashboard(
    metrics=["generation_throughput", "validation_results", "error_rates"],
    time_range="7d"
)
```

---

## Testing Strategy

### Unit Tests

```python
import pytest
import pandas as pd
from domain_specific import HealthcareGenerator, FinancialGenerator

@pytest.fixture
def healthcare_config():
    return HealthcareConfig(
        ontology="icd10",
        n_patients=100,
        avg_visits_per_year=2
    )

@pytest.fixture
def financial_config():
    return FinancialConfig(
        n_customers=100,
        transaction_frequency="daily",
        fraud_rate=0.01
    )

class TestHealthcareGenerator:
    def test_generates_valid_icd10_codes(self, healthcare_config):
        generator = HealthcareGenerator(config=healthcare_config)
        data = generator.generate_cohort()
        # Verify all diagnosis codes are valid ICD-10
        for _, row in data["diagnoses"].iterrows():
            assert is_valid_icd10(row["code"])

    def test_temporal_ordering(self, healthcare_config):
        generator = HealthcareGenerator(config=healthcare_config)
        data = generator.generate_cohort()
        # Verify lab results follow test orders
        for patient_id in data["patients"]["id"]:
            patient_labs = data["labs"][data["labs"]["patient_id"] == patient_id]
            patient_orders = data["orders"][data["orders"]["patient_id"] == patient_id]
            assert (patient_labs["date"] >= patient_orders["date"]).all()

class TestFinancialGenerator:
    def test_pci_compliance(self, financial_config):
        generator = FinancialGenerator(config=financial_config)
        data = generator.generate()
        masked = generator.apply_pci_masking(data)
        # Verify PAN is masked
        for _, row in masked.iterrows():
            assert len(row["card_number"]) == 4  # Only last 4 digits

    def test_fraud_rate(self, financial_config):
        generator = FinancialGenerator(config=financial_config)
        data = generator.generate()
        fraud_rate = data["is_fraud"].mean()
        assert abs(fraud_rate - 0.01) < 0.005
```

### Integration Tests

```python
class TestDomainPipeline:
    def test_healthcare_full_pipeline(self, healthcare_config):
        generator = HealthcareGenerator(config=healthcare_config)
        data = generator.generate_cohort()
        validated = generator.validate(data)
        assert validated["passed"] == validated["total"]
```

---

## Versioning & Migration

### Semantic Versioning

- **MAJOR**: Breaking API changes, incompatible data formats
- **MINOR**: New domains or generation capabilities, backward-compatible
- **PATCH**: Bug fixes, performance improvements

### Reference Data Migration

```python
from domain_specific import ReferenceDataMigrator

migrator = ReferenceDataMigrator(
    source_version="1.2.0",
    target_version="2.0.0"
)

migrator.migrate_reference_data(
    source_path="/app/reference_data/v1/",
    target_path="/app/reference_data/v2/",
    schema_mappings={
        "old_code": "new_code"
    }
)
```

### Configuration Migration

```python
from domain_specific import ConfigMigrator

config_migrator = ConfigMigrator()
config_migrator.migrate(
    source="old_domain_config.yaml",
    target="new_domain_config.yaml"
)
```

---

## Glossary

| Term | Definition |
|------|------------|
| **ICD-10** | International Classification of Diseases, 10th Revision - medical coding system |
| **OMOP CDM** | Observational Medical Outcomes Partnership Common Data Model |
| **PCI-DSS** | Payment Card Industry Data Security Standard |
| **EHR** | Electronic Health Record - digital version of patient medical history |
| **PINN** | Physically-Informed Neural Network - ML model that respects physical laws |
| **ADAS** | Advanced Driver Assistance Systems - automotive safety technology |
| **LiDAR** | Light Detection and Ranging - remote sensing technology |
| **SDTM** | Study Data Tabulation Model - clinical trial data standard |
| **FIX** | Financial Information eXchange - protocol for electronic trading |
| **Comorbidity** | Presence of two or more medical conditions in a patient |

---

## Changelog

### v1.0.0 (2024-01-15)
- Initial release with healthcare, financial, and IoT generators
- Domain-specific validation rules
- Standard format exports (OMOP, PCI-DSS)
- Clinical logic enforcement

### v1.1.0 (2024-03-01)
- Automotive scenario generation
- Legal document synthesis
- Scientific experimental data
- Enhanced fault injection for IoT

### v1.2.0 (2024-05-15)
- Spark integration for distributed generation
- MLflow integration for experiment tracking
- Enhanced validation rules
- Performance improvements

### v1.3.0 (2024-08-01)
- Kubernetes deployment templates
- REST API for domain generation
- Dashboard integration
- Enhanced audit logging

---

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/domain-specific.git
cd domain-specific
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

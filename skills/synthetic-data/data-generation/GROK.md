---
name: "data-generation"
category: "synthetic-data"
version: "1.0.0"
tags: ["synthetic-data", "data-generation", "tabular", "time-series", "nlp", "images", "differential-privacy"]
---

# Synthetic Data Generation Toolkit

## Overview

The `data-generation` module provides a comprehensive suite of tools for creating high-quality synthetic data across multiple modalities. It implements state-of-the-art generative models including Conditional Tabular GAN (CTGAN), Gaussian Copulas, and Variational Autoencoders (VAEs) to produce tabular data that preserves the statistical properties of real datasets. For time series data, the module offers autoregressive and latent-variable based generation techniques, while the NLP component utilizes fine-tuned transformer models or n-gram based approaches for text synthesis. Image synthesis is supported via Generative Adversarial Networks (GANs) and Diffusion models, specifically optimized for creating training data in low-resource regimes.

A key feature of this toolkit is its native integration of Differential Privacy (DP) mechanisms. By applying DP-SGD during the training of generative models or post-processing noise injection, the module ensures that generated data adheres to strict privacy budgets ($\epsilon, \delta$), making it suitable for regulated industries like healthcare and finance. The toolkit also supports conditional generation, allowing users to sample data based on specific attribute values (e.g., generating only records for a specific demographic group), and metadata-aware synthesis, which automatically detects column types, constraints, and relationships to ensure referential integrity in relational datasets.

This module serves as the foundational engine for the entire `synthetic-data` suite, providing the core generative capabilities that are then refined by privacy-preservation techniques, validated by quality-assurance metrics, and specialized for various industry domains. Whether you are looking to augment a small dataset for machine learning, create a privacy-safe version of sensitive records, or simulate complex physical systems, this toolkit provides the necessary primitives and high-level APIs. The module is designed to be modular, allowing users to swap out generative models or evaluation metrics as their needs evolve.

## Core Capabilities

*   **Tabular Synthesis**: Generate realistic rows and columns using CTGAN, Gaussian Copulas, or TVAE (Tabular Variational Autoencoder) with support for mixed data types (categorical, continuous, ordinal).
*   **Time Series Generation**: Create multi-variate time series with configurable seasonality, trends, and noise patterns using ARIMA, LSTM, or Transformer-based decoders.
*   **NLP Text Synthesis**: Generate domain-specific text via prompt-based generation or controlled style transfer, ensuring grammatical correctness and topical consistency.
*   **Image Synthesis**: Generate training images (e.g., medical scans, industrial defects) using StyleGAN3 or Diffusion models to augment small datasets.
*   **Conditional Sampling**: Query the generative model to produce samples conditioned on specific feature vectors or class labels.
*   **Differential Privacy**: Train generative models with DP-SGD or add calibrated noise to outputs to guarantee formal privacy bounds.
*   **Metadata-Aware Synthesis**: Automatically infer schema, primary keys, foreign keys, and data constraints to maintain relational integrity during generation.
*   **Evaluation & Validation**: Built-in metrics to assess fidelity (Kolmogorov-Smirnov test, Wasserstein distance) and utility (ML classifier performance on synthetic vs. real data).
*   **Relational Synthesis**: Generate synthetic data for multiple tables while maintaining referential integrity (foreign key relationships).
*   **Constraints Enforcement**: Define and enforce custom data constraints (e.g., min/max values, regex patterns, functional dependencies) during generation.
*   **Multi-Table Orchestration**: Automatically detect foreign-key relationships between tables and enforce referential integrity during the generation process.
*   **Incremental Learning**: Support for training generative models on streaming data or on datasets that exceed available memory via mini-batch or out-of-core training.
*   **Model Interchange**: Save, load, and transfer trained generative models across environments (local, cloud, edge) using a standardized serialization format.
*   **Reproducibility Controls**: Fixed random seeds, deterministic CUDA kernels, and version-tagged model artifacts to guarantee reproducible generation across runs.
*   **Hardware Acceleration**: Automatic detection and use of GPU/TPU resources for large-scale generation, with graceful fallback to CPU.

## Architecture

The module follows a layered architecture. At the base, `GenerativeModel` provides an abstract interface implemented by `CTGANSynthesizer`, `GaussianCopula`, and `TVAESynthesizer`. Above that, `DataGenerator` handles schema inference, data preprocessing, model training orchestration, and sample generation. The `RelationalGenerator` wraps `DataGenerator` with multi-table awareness and foreign-key enforcement. All generators inherit from a `BaseGenerator` class that provides consistent APIs for `fit()`, `generate()`, `save()`, and `load()`.

```
┌───────────────────────────────────────────┐
│            Application Layer              │
│   RelationalGenerator · ConditionalSampler│
├───────────────────────────────────────────┤
│             Generator Layer               │
│   DataGenerator · MetadataAwareGenerator  │
├───────────────────────────────────────────┤
│             Model Layer                   │
│   CTGAN · GaussianCopula · TVAE · ARIMA   │
├───────────────────────────────────────────┤
│           Foundation Layer                │
│   DP-SGD · Constraints · Schema Inference │
└───────────────────────────────────────────┘
```

## Usage Examples

### 1. Tabular Data Generation with CTGAN

```python
import pandas as pd
from data_generation import TabularGenerator

# Assume 'real_data.csv' contains a mix of categorical and continuous variables
real_data = pd.read_csv("real_data.csv")

# Initialize the CTGAN generator with privacy settings
generator = TabularGenerator(
    model_type="ctgan",
    epochs=300,
    batch_size=500,
    epsilon=1.0,  # Differential privacy budget
    delta=1e-5
)

# Train the model on real data
generator.fit(real_data)

# Generate 10,000 synthetic rows
synthetic_data = generator.generate(n_samples=10000)

# Save to file
synthetic_data.to_csv("synthetic_data.csv", index=False)
```

### 2. Conditional Time Series Generation

```python
from data_generation import TimeSeriesGenerator

# Configure a monthly sales time series generator
ts_gen = TimeSeriesGenerator(
    frequency="M",
    trend_strength=0.8,
    seasonal_strength=0.9,
    noise_level=0.05
)

# Generate 5 years of data with a specific holiday promotion effect
synthetic_ts = ts_gen.generate(
    periods=60,
    conditions={"month": [11, 12], "promotion": True},  # Holiday months with promo
    seed=42
)
```

### 3. NLP Text Generation for Augmentation

```python
from data_generation import TextGenerator

# Initialize with a pre-trained language model (e.g., GPT-2 small)
text_gen = TextGenerator(model_name="gpt2", max_length=128)

# Generate synthetic customer support tickets based on a template
templates = [
    "Issue with order #{id}: {complaint}",
    "Feedback on product {name}: {feedback}"
]

synthetic_tickets = text_gen.generate_batch(
    templates=templates,
    n_per_template=100,
    context={"product_names": ["Widget A", "Gadget B"]}
)
```

### 4. Relational Database Synthesis

```python
from data_generation import RelationalGenerator

# Define schema with foreign key relationships
schema = {
    "customers": {
        "id": "primary_key",
        "name": "string",
        "email": "string"
    },
    "orders": {
        "id": "primary_key",
        "customer_id": "foreign_key:customers.id",
        "amount": "float",
        "date": "date"
    }
}

# Generate synthetic data for all tables
rel_gen = RelationalGenerator(schema=schema)
synthetic_db = rel_gen.generate(n_customers=1000, n_orders_per_customer=5)

# Export each table
for table_name, df in synthetic_db.items():
    df.to_csv(f"synthetic_{table_name}.csv", index=False)
```

### 5. Image Synthesis with Diffusion Models

```python
from data_generation import ImageGenerator

# Initialize a conditional diffusion model for chest X-ray augmentation
img_gen = ImageGenerator(
    model_type="stable_diffusion",
    image_size=(512, 512),
    conditioning_labels=["pneumonia", "normal", "covid"]
)

# Generate 200 synthetic chest X-rays for the "pneumonia" class
synthetic_images = img_gen.generate(
    n_samples=200,
    class_label="pneumonia",
    guidance_scale=7.5,
    steps=50
)

# Save generated images
for idx, img in enumerate(synthetic_images):
    img.save(f"synthetic_xray_pneumonia_{idx:04d}.png")
```

### 6. Gaussian Copula for Quick Prototyping

```python
from data_generation import TabularGenerator

# Gaussian Copula is faster than CTGAN and works well for simpler distributions
gc_gen = TabularGenerator(
    model_type="gaussian_copula",
    enforce_min_max_values=True  # Ensures generated values stay within observed bounds
)

gc_gen.fit(real_data)
synthetic_data = gc_gen.generate(n_samples=5000)

# Compare distributions
for col in real_data.select_dtypes(include="number").columns:
    print(f"{col}: real_mean={real_data[col].mean():.2f}, synth_mean={synthetic_data[col].mean():.2f}")
```

## Algorithm Selection Guide

| Model | Best For | Pros | Cons |
|-------|----------|------|------|
| **CTGAN** | Complex tabular data with mixed types | Captures non-linear dependencies, handles mode collapse | Slower training, memory-intensive |
| **TVAE** | Tabular data needing smooth latent space | Faster inference, good for conditional generation | May underfit highly skewed distributions |
| **Gaussian Copula** | Simple tabular distributions, quick prototyping | Fast, interpretable, deterministic | Cannot capture non-linear dependencies |
| **ARIMA** | Univariate time series with clear trends | Well-understood, fast | Limited to linear patterns |
| **LSTM** | Multi-variate time series with complex patterns | Captures long-range dependencies | Requires more data, slower training |
| **Diffusion Models** | High-fidelity image generation | State-of-the-art quality, stable training | Slow inference, GPU-heavy |
| **GANs** | Real-time image generation | Fast inference | Mode collapse, training instability |

## Performance Considerations

1.  **Dataset Size Thresholds**: For datasets with fewer than 1,000 rows, Gaussian Copula typically outperforms CTGAN. For datasets with 10,000+ rows, CTGAN and TVAE capture richer distributions.
2.  **Memory Budget**: CTGAN loads the entire dataset into memory. For datasets exceeding available RAM, use the `IncrementalTabularGenerator` which trains on mini-batches.
3.  **GPU Utilization**: Image generation and LSTM-based time series generation benefit significantly from GPU acceleration. The module automatically detects CUDA availability.
4.  **Training Time**: CTGAN with 300 epochs on 50,000 rows typically trains in 5-15 minutes on a modern CPU. Gaussian Copula trains in seconds regardless of dataset size.
5.  **Sampling Speed**: Once trained, all tabular generators produce 10,000 samples in under 2 seconds. Image generation is slower (0.5-2 seconds per image depending on resolution).

## Best Practices

1.  **Check Data Quality First**: Ensure your real input data is clean (no duplicate primary keys, consistent formats) before training generative models, as GANs amplify data artifacts.
2.  **Use Differential Privacy for Sensitive Data**: If the dataset contains PII or PHI, always enable DP with a strict budget ($\epsilon < 1.0$) and monitor the privacy cost accumulation.
3.  **Validate Relational Integrity**: For database synthesis, use the `MetadataAwareSynthesizer` to ensure foreign keys in child tables point to valid primary keys in parent tables.
4.  **Hyperparameter Tuning**: CTGAN performance is sensitive to `batch_size` and `epochs`. Use the built-in `AutoTuner` to find optimal parameters for your specific dataset size.
5.  **Segmented Generation**: For highly heterogeneous data, segment the dataset by a categorical variable (e.g., region) and train separate models for each segment to preserve sub-group distributions.
6.  **Monitor Mode Collapse**: GANs can suffer from mode collapse (generating limited variety). Use the `DiversityScore` metric to verify that synthetic data covers the full range of the real data.
7.  **Save and Version Models**: Always save the trained generator object (not just the data) to allow for reproducible generation and future sampling without retraining.
8.  **Benchmark Against Baselines**: Compare your synthetic data against simple baselines (e.g., random sampling from the original data) to ensure the generative model is actually adding value.
9.  **Consider Memory Constraints**: Large datasets may require mini-batch training or out-of-core processing. The `TabularGenerator` supports incremental learning for datasets that don't fit in memory.
10. **Iterative Refinement**: Start with a simple model (like Gaussian Copula) and only move to complex ones (like CTGAN) if the simple model doesn't meet your fidelity requirements.
11. **Separate Evaluation Data**: Never evaluate synthetic data quality on the training set. Split your real data into train/eval sets and only evaluate against the eval set.
12. **Domain Expert Review**: For high-stakes domains (medical, financial), have domain experts validate that the generated records are realistic before deploying them.

## Common Failure Modes and Mitigations

| Failure Mode | Symptom | Mitigation |
|---|---|---|
| **Mode Collapse** | Synthetic data only covers 2-3 values for a column with 20 unique values | Increase training epochs, reduce learning rate, switch to TVAE |
| **Memorization** | Synthetic records are near-identical copies of real records | Enable DP-SGD, reduce training epochs, increase noise |
| **Distribution Shift** | Mean/variance of synthetic columns significantly differ from real | Check for data leakage, adjust model hyperparameters |
| **Referential Integrity Failure** | Foreign keys in child tables reference nonexistent parent IDs | Use `RelationalGenerator` instead of independent table generation |
| **Type Mismatch** | Continuous columns generated as integers, or vice versa | Ensure `MetadataAwareGenerator` is used with proper column type detection |
| **Training Instability** | Loss oscillates wildly or diverges | Reduce learning rate, increase batch size, add gradient clipping |

## Related Modules

*   [privacy-preservation](../privacy-preservation/GROK.md): Advanced anonymization and privacy budget management techniques.
*   [quality-validation](../quality-validation/GROK.md): Detailed statistical and machine learning metrics to evaluate synthetic data fidelity.
*   [augmentation](../augmentation/GROK.md): Techniques to augment existing datasets with transformed samples rather than generating from scratch.
*   [domain-specific](../domain-specific/GROK.md): Pre-configured templates and models for healthcare, finance, and IoT data.

---

## Advanced Configuration

The `data-generation` module exposes a rich set of configuration parameters that control every aspect of the generation pipeline. These can be specified via a YAML configuration file or programmatically through the `GenerationConfig` dataclass.

### Configuration File Format

```yaml
# generation_config.yaml
generation:
  model_type: "ctgan"
  epochs: 300
  batch_size: 500
  learning_rate: 0.001
  embedding_dim: 128
  generator_dim: [256, 256]
  discriminator_dim: [256, 256]
  discriminator_steps: 2
  pac: 10
  verbose: true

privacy:
  enabled: true
  epsilon: 1.0
  delta: 1e-5
  noise_multiplier: 1.1
  max_grad_norm: 1.0

constraints:
  enforce_min_max: true
  enforce_rounding: true
  primary_key_columns: ["id"]
  foreign_keys:
    orders:
      customer_id: "customers.id"

output:
  format: "csv"
  compression: "gzip"
  include_metadata: true
```

### Programmatic Configuration

```python
from data_generation import GenerationConfig, TabularGenerator

config = GenerationConfig(
    model_type="ctgan",
    epochs=300,
    batch_size=500,
    privacy_epsilon=1.0,
    privacy_delta=1e-5,
    enforce_constraints=True,
    random_seed=42,
    device="cuda:0"
)

generator = TabularGenerator(config=config)
generator.fit(real_data)
```

### Environment-Specific Overrides

The module supports environment-based configuration overrides. Set environment variables to adjust behavior without modifying configuration files:

```bash
# Override generation parameters via environment
export DATAGEN_MODEL_TYPE="tvae"
export DATAGEN_EPOCHS=500
export DATAGEN_BATCH_SIZE=1024
export DATAGEN_EPSILON=0.5
export DATAGEN_DEVICE="cuda:1"
export DATAGEN_LOG_LEVEL="debug"
```

### Dynamic Configuration Updates

```python
from data_generation import DynamicConfigManager

config_manager = DynamicConfigManager(config_path="generation_config.yaml")

# Register callbacks for configuration changes
@config_manager.on_change("epochs")
def update_epochs(new_value):
    print(f"Epochs updated to {new_value}")
    generator.update_config(epochs=new_value)

# Hot-reload configuration
config_manager.reload()
```

---

## Architecture Patterns

### Generator Factory Pattern

The module uses a factory pattern to create generators based on configuration, allowing runtime selection of generative models without changing application code.

```python
from data_generation import GeneratorFactory

# Create a generator from configuration
factory = GeneratorFactory()
generator = factory.create(
    model_type="ctgan",
    config=GenerationConfig(epochs=300)
)

# The same factory can create different model types
gc_generator = factory.create(
    model_type="gaussian_copula",
    config=GenerationConfig()
)
```

### Pipeline Architecture

The generation process follows a pipeline architecture with distinct stages: schema inference, data preprocessing, model training, and sample generation. Each stage can be customized or replaced independently.

```python
from data_generation import GenerationPipeline, SchemaInferer, Preprocessor, Trainer, Sampler

pipeline = GenerationPipeline(
    schema_inferer=SchemaInferer(strict_mode=True),
    preprocessor=Preprocessor(encoding="onehot", scaling="standard"),
    trainer=Trainer(epochs=300, early_stopping=True, patience=10),
    sampler=Sampler(batch_size=1000, seed=42)
)

# Execute the full pipeline
synthetic_data = pipeline.execute(real_data, n_samples=10000)
```

### Observer Pattern for Monitoring

```python
from data_generation import TabularGenerator, GenerationObserver

class TrainingMonitor(GenerationObserver):
    def on_epoch_complete(self, epoch, metrics):
        print(f"Epoch {epoch}: loss={metrics['loss']:.4f}")

    def on_generation_complete(self, n_samples, duration):
        print(f"Generated {n_samples} samples in {duration:.2f}s")

generator = TabularGenerator(model_type="ctgan")
generator.add_observer(TrainingMonitor())
generator.fit(real_data)
```

### Plugin Architecture

The module supports plugins that extend generation capabilities with custom models, metrics, or preprocessing steps.

```python
from data_generation import PluginRegistry

# Register a custom generative model
@PluginRegistry.register("custom_gan")
class CustomGANModel:
    def fit(self, data, config):
        # Custom training logic
        pass

    def sample(self, n_samples):
        # Custom sampling logic
        pass
```

---

## Integration Guide

### Integration with Scikit-learn Pipelines

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from data_generation import SyntheticDataStep

# Create an ML pipeline with synthetic data generation
pipeline = Pipeline([
    ("synthetic_augment", SyntheticDataStep(
        generator_type="ctgan",
        augmentation_ratio=0.5,
        random_state=42
    )),
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(n_estimators=100))
])

# Train on real data with synthetic augmentation
pipeline.fit(X_train, y_train)
```

### Integration with PyTorch DataLoader

```python
import torch
from torch.utils.data import DataLoader, Dataset
from data_generation import TabularGenerator

class SyntheticDataset(Dataset):
    def __init__(self, generator, n_samples):
        self.data = generator.generate(n_samples=n_samples)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return torch.tensor(self.data.iloc[idx].values, dtype=torch.float32)

# Create DataLoader from synthetic data
generator = TabularGenerator(model_type="ctgan")
generator.fit(real_data)

synthetic_dataset = SyntheticDataset(generator, n_samples=10000)
dataloader = DataLoader(synthetic_dataset, batch_size=64, shuffle=True)
```

### Integration with Apache Spark

```python
from data_generation import SparkGenerator

# Configure generation for distributed execution
spark_gen = SparkGenerator(
    model_type="ctgan",
    partitions=10,
    executor_memory="4g"
)

# Generate from a Spark DataFrame
synthetic_df = spark_gen.generate(
    real_spark_df,
    n_samples=100000,
    output_path="s3://bucket/synthetic/"
)
```

### Integration with MLflow

```python
import mlflow
from data_generation import TabularGenerator, MLflowTracker

# Configure MLflow tracking
tracker = MLflowTracker(experiment_name="synthetic_data_generation")

generator = TabularGenerator(
    model_type="ctgan",
    tracker=tracker
)

# Training is automatically logged to MLflow
with mlflow.start_run():
    generator.fit(real_data)
    synthetic_data = generator.generate(n_samples=10000)

    # Log the synthetic data as an artifact
    mlflow.log_artifact("synthetic_data.csv")
```

---

## Performance Optimization

### Memory Management

```python
from data_generation import TabularGenerator, MemoryConfig

# Configure memory-limited generation
memory_config = MemoryConfig(
    max_memory_gb=4.0,
    use_chunking=True,
    chunk_size=10000,
    spill_to_disk=True,
    spill_path="/tmp/data_gen_spill"
)

generator = TabularGenerator(
    model_type="ctgan",
    memory_config=memory_config
)
```

### Parallel Generation

```python
from data_generation import ParallelGenerator

# Generate data in parallel across multiple cores
parallel_gen = ParallelGenerator(
    model_type="gaussian_copula",
    n_workers=8,
    chunk_size=5000
)

# Each worker generates a portion of the data
synthetic_data = parallel_gen.generate(n_samples=100000)
```

### GPU Acceleration

```python
from data_generation import TabularGenerator, GPUConfig

gpu_config = GPUConfig(
    device="cuda:0",
    mixed_precision=True,
    memory_fraction=0.8,
    compile_model=True  # Use torch.compile for faster inference
)

generator = TabularGenerator(
    model_type="ctgan",
    gpu_config=gpu_config
)
```

### Caching Strategies

```python
from data_generation import TabularGenerator, CacheConfig

cache_config = CacheConfig(
    enabled=True,
    cache_dir="/tmp/model_cache",
    max_cache_size_gb=10,
    ttl_hours=24
)

generator = TabularGenerator(
    model_type="ctgan",
    cache_config=cache_config
)

# First call trains and caches
generator.fit(real_data)

# Subsequent calls use cached model
generator.fit(real_data)  # Uses cache
```

---

## Security Considerations

### Data Encryption

```python
from data_generation import TabularGenerator, EncryptionConfig

# Encrypt synthetic data at rest
encryption_config = EncryptionConfig(
    algorithm="AES-256-GCM",
    key_management="aws-kms",
    kms_key_id="arn:aws:kms:us-east-1:123456789012:key/abc-def"
)

generator = TabularGenerator(
    model_type="ctgan",
    encryption_config=encryption_config
)

# Generated data is automatically encrypted
synthetic_data = generator.generate(n_samples=10000)
# Data is encrypted before writing to disk
```

### Access Control

```python
from data_generation import AccessControlManager

# Define who can generate and access synthetic data
acl = AccessControlManager()
acl.add_policy(
    resource="patient_data",
    allowed_roles=["data_scientist", "researcher"],
    require_approval=True,
    approval_workflow="manager"
)

# Generation requires authentication
generator = TabularGenerator(
    model_type="ctgan",
    access_control=acl
)
```

### Audit Logging

```python
from data_generation import AuditLogger

# Enable comprehensive audit logging
audit_logger = AuditLogger(
    log_path="/var/log/synthetic_data/",
    log_format="json",
    capture_inputs=True,
    capture_outputs_hash=True,
    retention_days=365
)

generator = TabularGenerator(
    model_type="ctgan",
    audit_logger=audit_logger
)
```

### Secure Model Serialization

```python
from data_generation import SecureSerializer

# Save model with integrity verification
serializer = SecureSerializer(
    signing_key="path/to/private_key.pem",
    checksum_algorithm="sha256"
)

generator.save("model.pt", serializer=serializer)

# Load with integrity verification
loaded_generator = TabularGenerator.load(
    "model.pt",
    serializer=serializer,
    verify_integrity=True
)
```

---

## Troubleshooting Guide

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `CUDA out of memory` | Batch size too large for GPU | Reduce `batch_size` or enable `mixed_precision` |
| `Mode collapse detected` | GAN generating limited variety | Increase `discriminator_steps`, reduce `learning_rate` |
| `Schema mismatch error` | Generated data has different columns | Ensure `fit()` and `generate()` use the same schema |
| `Privacy budget exceeded` | Cumulative epsilon too high | Reduce query frequency or increase `delta` |
| `Foreign key violation` | Child table references invalid parent | Use `RelationalGenerator` for multi-table generation |

### Debug Mode

```python
from data_generation import TabularGenerator, DebugConfig

# Enable detailed debugging
debug_config = DebugConfig(
    verbose=True,
    log_level="DEBUG",
    save_intermediate=True,
    intermediate_path="/tmp/debug/",
    profile_training=True
)

generator = TabularGenerator(
    model_type="ctgan",
    debug_config=debug_config
)

# Training progress is logged in detail
generator.fit(real_data)
```

### Performance Profiling

```python
from data_generation import Profiler

profiler = Profiler()

with profiler:
    generator.fit(real_data)
    synthetic_data = generator.generate(n_samples=10000)

# Print profiling results
profiler.print_report()
# Output includes:
# - Training time breakdown
# - Memory usage per epoch
# - GPU utilization statistics
# - Sampling throughput
```

### Validation Diagnostics

```python
from data_generation import DiagnosticTools

# Run diagnostic checks on generated data
diagnostics = DiagnosticTools.run(
    real_data=real_data,
    synthetic_data=synthetic_data,
    checks=["distribution", "correlation", "outliers", "constraints"]
)

for check in diagnostics:
    if not check.passed:
        print(f"WARNING: {check.name} failed - {check.message}")
        print(f"  Recommendation: {check.suggestion}")
```

---

## API Reference

### TabularGenerator

```python
class TabularGenerator(BaseGenerator):
    """Generate synthetic tabular data using various generative models."""

    def __init__(
        self,
        model_type: str = "ctgan",
        config: GenerationConfig = None,
        epochs: int = 300,
        batch_size: int = 500,
        learning_rate: float = 0.001,
        epsilon: float = None,
        delta: float = None,
        random_seed: int = None,
        device: str = "cpu"
    ):
        """Initialize the tabular generator.

        Args:
            model_type: One of "ctgan", "tvae", "gaussian_copula"
            config: Optional GenerationConfig object
            epochs: Number of training epochs
            batch_size: Batch size for training
            learning_rate: Learning rate for optimizer
            epsilon: Differential privacy budget
            delta: Differential privacy delta parameter
            random_seed: Seed for reproducibility
            device: "cpu" or "cuda:N"
        """
        pass

    def fit(self, data: pd.DataFrame, metadata: dict = None) -> None:
        """Train the generative model on real data.

        Args:
            data: Training DataFrame
            metadata: Optional schema metadata
        """
        pass

    def generate(
        self,
        n_samples: int,
        conditions: dict = None,
        output_path: str = None
    ) -> pd.DataFrame:
        """Generate synthetic data samples.

        Args:
            n_samples: Number of rows to generate
            conditions: Optional conditioning variables
            output_path: Optional path to save output

        Returns:
            DataFrame with synthetic data
        """
        pass

    def save(self, path: str, compress: bool = True) -> None:
        """Save the trained generator to disk."""
        pass

    @classmethod
    def load(cls, path: str) -> "TabularGenerator":
        """Load a trained generator from disk."""
        pass
```

### RelationalGenerator

```python
class RelationalGenerator(BaseGenerator):
    """Generate synthetic data for relational databases."""

    def __init__(self, schema: dict, config: GenerationConfig = None):
        """Initialize with a schema definition.

        Args:
            schema: Dict mapping table names to column definitions
            config: Optional generation configuration
        """
        pass

    def fit(
        self,
        tables: dict[str, pd.DataFrame],
        foreign_keys: list[tuple[str, str, str, str]] = None
    ) -> None:
        """Train models for all tables.

        Args:
            tables: Dict mapping table names to DataFrames
            foreign_keys: List of (child_table, child_col, parent_table, parent_col)
        """
        pass

    def generate(
        self,
        n_rows: dict[str, int],
        referential_integrity: bool = True
    ) -> dict[str, pd.DataFrame]:
        """Generate synthetic data for all tables.

        Args:
            n_rows: Dict mapping table names to row counts
            referential_integrity: Enforce foreign key constraints

        Returns:
            Dict mapping table names to synthetic DataFrames
        """
        pass
```

---

## Data Models

### GenerationConfig Schema

```python
@dataclass
class GenerationConfig:
    """Configuration for data generation."""

    model_type: str = "ctgan"
    epochs: int = 300
    batch_size: int = 500
    learning_rate: float = 0.001
    embedding_dim: int = 128
    generator_dim: list[int] = field(default_factory=lambda: [256, 256])
    discriminator_dim: list[int] = field(default_factory=lambda: [256, 256])
    discriminator_steps: int = 2
    pac: int = 10
    verbose: bool = True
    random_seed: int = None

    # Privacy settings
    epsilon: float = None
    delta: float = None
    noise_multiplier: float = 1.1
    max_grad_norm: float = 1.0

    # Constraint settings
    enforce_min_max: bool = True
    enforce_rounding: bool = True
    primary_key_columns: list[str] = field(default_factory=list)
    foreign_keys: dict = field(default_factory=dict)

    # Output settings
    output_format: str = "csv"
    compression: str = None
    include_metadata: bool = True
```

### SyntheticDataRecord Schema

```python
@dataclass
class SyntheticDataRecord:
    """Metadata about a generated dataset."""

    dataset_id: str
    generator_type: str
    n_rows: int
    n_columns: int
    column_types: dict[str, str]
    generation_timestamp: datetime
    model_version: str
    privacy_budget: dict[str, float]  # {"epsilon": ..., "delta": ...}
    quality_scores: dict[str, float]  # {"ks_pvalue": ..., "wasserstein": ...}
    checksum: str
```

### ModelArtifact Schema

```python
@dataclass
class ModelArtifact:
    """Serializable model artifact."""

    model_type: str
    model_state_dict: dict
    config: GenerationConfig
    schema: dict
    training_metadata: dict
    created_at: datetime
    version: str
```

---

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ /app/src/
COPY config/ /app/config/

WORKDIR /app

# Expose API port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "-m", "data_generation.server", "--port", "8080"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: data-generation-service
  namespace: synthetic-data
spec:
  replicas: 3
  selector:
    matchLabels:
      app: data-generation
  template:
    metadata:
      labels:
        app: data-generation
    spec:
      containers:
      - name: generator
        image: synthetic-data/generator:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "4Gi"
            cpu: "2"
          limits:
            memory: "8Gi"
            cpu: "4"
            nvidia.com/gpu: "1"
        env:
        - name: DATAGEN_DEVICE
          value: "cuda:0"
        - name: DATAGEN_LOG_LEVEL
          value: "info"
```

### REST API Server

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from data_generation import TabularGenerator, GenerationConfig

app = FastAPI(title="Data Generation API")

class GenerateRequest(BaseModel):
    n_samples: int
    model_type: str = "ctgan"
    conditions: dict = None

@app.post("/generate")
async def generate_data(request: GenerateRequest):
    try:
        generator = TabularGenerator(model_type=request.model_type)
        generator.load("model.pt")
        synthetic_data = generator.generate(
            n_samples=request.n_samples,
            conditions=request.conditions
        )
        return {"data": synthetic_data.to_dict()}
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
from data_generation import MetricsCollector

# Configure metrics collection
metrics = MetricsCollector(
    backend="prometheus",
    port=9090,
    metrics=[
        "generation_duration_seconds",
        "samples_generated_total",
        "model_training_loss",
        "privacy_budget_remaining",
        "memory_usage_bytes"
    ]
)

generator = TabularGenerator(
    model_type="ctgan",
    metrics_collector=metrics
)
```

### Logging Configuration

```python
import logging
from data_generation import LoggingConfig

logging_config = LoggingConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("/var/log/data_generation.log"),
        logging.StreamHandler()
    ],
    structured=True,
    json_output=True
)

logging_config.apply()
```

### Health Checks

```python
from data_generation import HealthChecker

health_checker = HealthChecker(
    checks=[
        "gpu_available",
        "memory_sufficient",
        "model_loaded",
        "disk_space"
    ],
    critical_checks=["gpu_available", "memory_sufficient"]
)

status = health_checker.check()
if not status.healthy:
    for failure in status.failures:
        print(f"CRITICAL: {failure.check} - {failure.message}")
```

### Alerting Rules

```python
from data_generation import AlertManager

alert_manager = AlertManager(
    rules=[
        {"metric": "generation_duration_seconds", "threshold": 300, "severity": "warning"},
        {"metric": "privacy_budget_remaining", "threshold": 0.1, "severity": "critical"},
        {"metric": "memory_usage_bytes", "threshold": 0.9, "severity": "warning"}
    ],
    notification_channels=["slack", "email"]
)
```

---

## Testing Strategy

### Unit Tests

```python
import pytest
from data_generation import TabularGenerator, GaussianCopula
import pandas as pd
import numpy as np

@pytest.fixture
def sample_data():
    np.random.seed(42)
    return pd.DataFrame({
        "age": np.random.randint(18, 80, 1000),
        "income": np.random.lognormal(10, 1, 1000),
        "category": np.random.choice(["A", "B", "C"], 1000)
    })

class TestTabularGenerator:
    def test_fit_generates_model(self, sample_data):
        gen = TabularGenerator(model_type="gaussian_copula")
        gen.fit(sample_data)
        assert gen.is_fitted

    def test_generate_correct_shape(self, sample_data):
        gen = TabularGenerator(model_type="gaussian_copula")
        gen.fit(sample_data)
        synthetic = gen.generate(n_samples=100)
        assert len(synthetic) == 100
        assert list(synthetic.columns) == list(sample_data.columns)

    def test_generate_preserves_types(self, sample_data):
        gen = TabularGenerator(model_type="gaussian_copula")
        gen.fit(sample_data)
        synthetic = gen.generate(n_samples=100)
        assert synthetic["age"].dtype == sample_data["age"].dtype

    def test_deterministic_with_seed(self, sample_data):
        gen1 = TabularGenerator(model_type="gaussian_copula", random_seed=42)
        gen2 = TabularGenerator(model_type="gaussian_copula", random_seed=42)
        gen1.fit(sample_data)
        gen2.fit(sample_data)
        synth1 = gen1.generate(n_samples=100)
        synth2 = gen2.generate(n_samples=100)
        pd.testing.assert_frame_equal(synth1, synth2)
```

### Integration Tests

```python
class TestRelationalGenerator:
    def test_referential_integrity(self):
        schema = {
            "customers": {"id": "primary_key", "name": "string"},
            "orders": {"id": "primary_key", "customer_id": "foreign_key:customers.id"}
        }
        gen = RelationalGenerator(schema=schema)
        # ... fit and generate ...
        for _, row in synthetic_orders.iterrows():
            assert row["customer_id"] in synthetic_customers["id"].values

    def test_export_formats(self, sample_data):
        gen = TabularGenerator(model_type="gaussian_copula")
        gen.fit(sample_data)
        synthetic = gen.generate(n_samples=100)

        # Test CSV export
        synthetic.to_csv("test_output.csv", index=False)
        loaded = pd.read_csv("test_output.csv")
        assert len(loaded) == 100

        # Test Parquet export
        synthetic.to_parquet("test_output.parquet", index=False)
        loaded = pd.read_parquet("test_output.parquet")
        assert len(loaded) == 100
```

---

## Versioning & Migration

### Semantic Versioning

The module follows semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking API changes, incompatible model formats
- **MINOR**: New features, backward-compatible
- **PATCH**: Bug fixes, performance improvements

### Model Format Migration

```python
from data_generation import ModelMigrator

# Migrate a model trained with v1.x to v2.x format
migrator = ModelMigrator(
    source_version="1.2.0",
    target_version="2.0.0"
)

migrator.migrate(
    model_path="old_model.pt",
    output_path="new_model.pt",
    preserve_weights=True
)
```

### Data Format Migration

```python
from data_generation import DataMigrator

# Migrate configuration files
config_migrator = DataMigrator()
config_migrator.migrate_config(
    source="old_config.yaml",
    target="new_config.yaml",
    mappings={
        "model.epochs": "generation.epochs",
        "model.batch_size": "generation.batch_size"
    }
)
```

---

## Glossary

| Term | Definition |
|------|------------|
| **CTGAN** | Conditional Tabular Generative Adversarial Network - a GAN architecture for tabular data synthesis |
| **TVAE** | Tabular Variational Autoencoder - a VAE variant optimized for tabular data |
| **Gaussian Copula** | A statistical model that captures marginal distributions and dependency structure |
| **DP-SGD** | Differentially Private Stochastic Gradient Descent - adds noise to gradients for privacy |
| **Mode Collapse** | A GAN failure where the generator produces limited variety of samples |
| **Wasserstein Distance** | A metric measuring the "cost" of transforming one distribution into another |
| **KS Test** | Kolmogorov-Smirnov test - a nonparametric test for distribution equality |
| **Referential Integrity** | Ensuring foreign key values in child tables match primary keys in parent tables |
| **Schema Inference** | Automatic detection of column types, constraints, and relationships |
| **Privacy Budget** | The cumulative privacy loss (epsilon) allowed across multiple data releases |

---

## Changelog

### v1.0.0 (2024-01-15)
- Initial release with CTGAN, TVAE, and Gaussian Copula support
- Tabular data generation with schema inference
- Basic differential privacy integration
- Relational data generation with foreign key enforcement

### v1.1.0 (2024-03-01)
- Added ARIMA and LSTM time series generation
- Introduced conditional generation API
- Performance improvements for large datasets
- Memory-efficient incremental learning support

### v1.2.0 (2024-05-15)
- Diffusion model support for image synthesis
- Plugin architecture for custom models
- MLflow integration for experiment tracking
- Spark integration for distributed generation

### v1.3.0 (2024-08-01)
- Enhanced privacy controls with advanced DP mechanisms
- Model serialization improvements with integrity verification
- Kubernetes deployment templates
- REST API server for generation-as-a-service

---

## Contributing Guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/example/synthetic-data.git
cd synthetic-data

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run linting
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

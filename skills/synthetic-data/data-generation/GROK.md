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

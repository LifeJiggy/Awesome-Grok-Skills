---
name: "augmentation"
category: "synthetic-data"
version: "1.0.0"
tags: ["synthetic-data", "augmentation", "image", "text", "time-series", "smote", "vae"]
---

# Data Augmentation Toolkit

## Overview

The `augmentation` module provides a comprehensive set of techniques for expanding and enriching existing datasets without collecting new raw data. Data augmentation is a cornerstone of modern machine learning, particularly in regimes where labeled data is scarce or expensive to obtain. By applying realistic transformations—such as rotations and color jitter for images, synonym replacement and back-translation for text, or time-warping for sensor data—this toolkit helps prevent overfitting and improves model generalization.

Beyond simple geometric and lexical transformations, the module supports sophisticated "generative augmentation" using Variational Autoencoders (VAEs). Unlike simple flipping or cropping, VAE-based augmentation learns the underlying manifold of the data and samples new points that are semantically consistent with the original set. This is particularly powerful for complex data types like medical images or handwriting where simple transformations might produce unrealistic samples.

For imbalanced classification problems, the module includes a robust implementation of SMOTE (Synthetic Minority Over-sampling Technique) and its variants (Borderline-SMOTE, ADASYN). These algorithms generate synthetic feature vectors for under-represented classes in the feature space, rather than just duplicating existing rows, which helps the decision boundary become more robust. The toolkit is designed with a modular "pipeline" architecture, allowing users to compose multiple augmentation steps (e.g., flip + rotate + color jitter) into a single, atomic operation that can be applied consistently across training, validation, and test sets.

The module distinguishes between *deterministic augmentations* (the same input always produces the same output given a seed) and *stochastic augmentations* (each call produces a different variant). This distinction is critical for reproducibility in ML pipelines and for ensuring that augmentation is applied consistently during training versus inference.

## Core Capabilities

*   **Image Augmentation**: Apply geometric transformations (rotation, flip, crop, shear) and photometric transformations (brightness, contrast, saturation, jitter) using optimized libraries.
*   **Text Augmentation**: Perform synonym replacement, random insertion/deletion, and back-translation (translating to another language and back) to generate linguistically diverse text.
*   **Time Series Augmentation**: Implement time warping, window slicing, and magnitude warping to simulate variations in temporal patterns and sensor noise.
*   **SMOTE & Variants**: Generate synthetic samples for imbalanced datasets using SMOTE, Borderline-SMOTE, and ADASYN to balance class distributions in the feature space.
*   **Generative Augmentation**: Use trained VAEs or GANs to sample new, realistic data points that lie on the learned data manifold.
*   **Feature-Space Augmentation**: Apply noise injection, dropout-based feature masking, and mixing (e.g., Mixup, CutMix) directly in the latent or feature space.
*   **Pipeline Composition**: Chain multiple augmentation techniques into a single pipeline with configurable probabilities for each step.
*   **Reproducibility**: Support for global and per-sample random seeds to ensure deterministic augmentation during debugging and experiments.
*   **Domain-Specific Rules**: Enforce domain constraints during augmentation (e.g., ensuring a time series doesn't become physically impossible after warping).
*   **Batch Processing**: Efficiently apply augmentations to entire batches of data, with support for multiprocessing and GPU acceleration.
*   **Class-Aware Augmentation**: Apply different augmentation strategies per class, allowing more aggressive augmentation for majority classes while preserving minority class integrity.
*   **Augmentation-Validation Integration**: Automatically monitor whether augmented samples improve or degrade downstream model performance on a held-out validation set.
*   **Metadata Propagation**: Ensure that augmentation pipelines correctly propagate labels, bounding boxes, segmentation masks, and other annotations alongside the transformed data.

## Augmentation Technique Reference

### Image Transformations

| Technique | Parameters | When to Use | Domain Considerations |
|-----------|------------|-------------|----------------------|
| **Random Rotation** | degrees, fill_mode | Orientation-invariant tasks | Avoid for medical images where orientation is clinically meaningful |
| **Horizontal Flip** | probability | Symmetric objects (faces, vehicles) | Not for asymmetric features (e.g., left vs. right lung) |
| **Color Jitter** | brightness, contrast, saturation, hue | Photometric invariance | Calibrate to domain (e.g., radiology has no color) |
| **Random Crop** | size, scale_range | Translation invariance | Ensure cropped regions remain identifiable |
| **Elastic Deformation** | alpha, sigma | Biomedical images, handwriting | Simulates tissue deformation |
| **Mixup** | alpha | Regularization | Blend two images and their labels proportionally |
| **CutMix** | alpha, ratio | Object localization | Cut a patch from one image and paste onto another |

### Text Transformations

| Technique | Parameters | When to Use | Domain Considerations |
|-----------|------------|-------------|----------------------|
| **Synonym Replacement** | n_replacements, wordnet | Lexical diversity | Ensure synonyms are domain-appropriate |
| **Random Deletion** | probability | Robustness to missing words | Don't delete named entities |
| **Back Translation** | intermediate_lang | Semantic preservation | Choose intermediate language carefully (e.g., EN→DE→EN) |
| **Contextual Insertion** | bert_model | Grammatical diversity | Use domain-specific BERT for best results |
| **Sentence Shuffling** | n_segments | Discourse robustness | Only for documents, not single sentences |
| **Entity Replacement** | entity_types | Named entity diversity | Replace with entities from the same type distribution |

### Time Series Transformations

| Technique | Parameters | When to Use | Domain Considerations |
|-----------|------------|-------------|----------------------|
| **Time Warping** | sigma, knot_count | Temporal variability | Preserve phase relationships |
| **Magnitude Warp** | sigma | Amplitude variability | Maintain relative magnitudes |
| **Window Slicing** | window_size, stride | Variable-length sequences | Ensure slices contain at least one full period |
| **Jittering** | sigma | Sensor noise simulation | Match real noise characteristics |
| **Rotation** | angle_range | Sensor orientation changes | Only if sensor orientation is variable |
| **Permutation** | n_segments | Sequence order invariance | Check if order is semantically meaningful |

## Usage Examples

### 1. Image Augmentation Pipeline

```python
import cv2
from augmentation import ImageAugmenter

# Define a sequence of augmentations
augmenter = ImageAugmenter(pipeline=[
    {"type": "rotate", "degrees": 15, "probability": 0.5},
    {"type": "horizontal_flip", "probability": 0.5},
    {"type": "color_jitter", "brightness": 0.2, "contrast": 0.2, "probability": 0.8},
    {"type": "random_crop", "size": (224, 224), "probability": 1.0}
])

# Load an image
image = cv2.imread("training_image.jpg")

# Apply augmentations
augmented_images = augmenter.augment(image, n_variants=5)

for i, img in enumerate(augmented_images):
    cv2.imwrite(f"augmented_{i}.jpg", img)
```

### 2. SMOTE for Imbalanced Data

```python
import pandas as pd
from augmentation import SmoteAugmenter

# Assume 'df' has a class imbalance (e.g., 90% Class A, 10% Class B)
df = pd.read_csv("imbalanced_data.csv")
features = df.drop(columns=["target"])
labels = df["target"]

# Initialize SMOTE to balance the classes
smote = SmoteAugmenter(sampling_strategy=1.0, k_neighbors=5)

# Fit and resample
X_res, y_res = smote.fit_resample(features, labels)

print(f"Original class distribution: {pd.Series(labels).value_counts().to_dict()}")
print(f"Resampled class distribution: {pd.Series(y_res).value_counts().to_dict()}")
```

### 3. Text Augmentation via Synonym Replacement

```python
from augmentation import TextAugmenter

text_gen = TextAugmenter(method="synonym_replacement", n_augmentations=3)

original_text = "The quick brown fox jumps over the lazy dog."
augmented_texts = text_gen.transform(original_text)

print("Original:", original_text)
for aug in augmented_texts:
    print("Augmented:", aug)
```

### 4. Time Series Augmentation

```python
import numpy as np
from augmentation import TimeSeriesAugmenter

ts_aug = TimeSeriesAugmenter()

# Generate a synthetic time series
original_ts = np.sin(np.linspace(0, 10, 100))

# Apply time warping and jitter
warped_ts = ts_aug.time_warp(original_ts, sigma=0.2)
jittered_ts = ts_aug.magnitude_warp(original_ts, sigma=0.1)
sliced_ts = ts_aug.window_slicing(original_ts, window_size=50, stride=10)
```

### 5. VAE-Based Generative Augmentation

```python
from augmentation import VAEGAugmenter

# Train a VAE on the minority class samples only
vae_aug = VAEGAugmenter(
    input_dim=784,
    latent_dim=32,
    hidden_dims=[256, 128],
    epochs=100
)

# Fit on minority class data
minority_data = features[labels == "minority_class"]
vae_aug.fit(minority_data)

# Generate 500 new synthetic samples for the minority class
synthetic_minority = vae_aug.generate(n_samples=500)

# Combine with original data
augmented_features = pd.concat([features, synthetic_minority], ignore_index=True)
augmented_labels = pd.concat([labels, pd.Series(["minority_class"] * 500)], ignore_index=True)
```

### 6. Composed Pipeline with Conditional Logic

```python
from augmentation import AugmentationPipeline

# Build a pipeline that applies different strategies per class
pipeline = AugmentationPipeline()

# For majority class: lighter augmentation
pipeline.add(
    augmenter=ImageAugmenter(pipeline=[
        {"type": "horizontal_flip", "probability": 0.3},
        {"type": "color_jitter", "brightness": 0.1, "probability": 0.5},
    ]),
    class_condition="majority_class"
)

# For minority class: heavier augmentation + generative
pipeline.add(
    augmenter=ImageAugmenter(pipeline=[
        {"type": "rotate", "degrees": 30, "probability": 0.7},
        {"type": "horizontal_flip", "probability": 0.5},
        {"type": "color_jitter", "brightness": 0.3, "contrast": 0.3, "probability": 0.8},
    ]),
    class_condition="minority_class"
)

# Apply to a batch of data
augmented_batch = pipeline.apply_batch(images, labels)
```

## Best Practices

1.  **Match Augmentations to Data**: Don't apply "horizontal flip" to medical X-rays if the orientation is clinically significant. Ensure augmentations are realistic for the domain.
2.  **Don't Over-Augment**: Applying too many transformations can distort the data beyond recognition. Use probabilities (e.g., 0.5) to apply augmentations randomly rather than always.
3.  **Validate Augmented Data**: Always visually inspect (for images) or manually review (for text) a sample of augmented data to ensure quality.
4.  **Use SMOTE Carefully**: SMOTE should only be applied to the training set, never the validation or test set, to avoid data leakage.
5.  **Consistent Pipelines**: Ensure the same augmentation pipeline (with the same parameters) is used for both training and inference-time testing if applicable.
6.  **Leverage Generative Models**: For high-complexity data like medical images, VAE-based augmentation often outperforms simple geometric transformations.
7.  **Monitor Performance**: Use the `quality-validation` module to track how augmentation affects model performance on a held-out validation set.
8.  **Preserve Class Balance**: When augmenting, ensure you don't inadvertently shift the class distribution unless that's your specific goal (e.g., using SMOTE).
9.  **Document Augmentation Steps**: Maintain a record of all augmentation parameters for reproducibility and for understanding how the model was trained.
10. **Test Augmentation Sensitivity**: Run ablation studies to determine which augmentations contribute most to performance gains; remove those that don't help.
11. **Use Seed Control for Debugging**: When debugging augmentation effects, use fixed seeds so that results are reproducible across runs.
12. **Avoid Augmentation Leakage**: Never apply augmentation to validation or test data. Use the pipeline's `fit()` on training data only, then `transform()` on eval data with augmentation disabled.

## Common Pitfalls

| Pitfall | Consequence | Solution |
|---------|-------------|----------|
| Augmenting test data | Inflated evaluation metrics | Separate train/eval augmentation policies |
| Applying domain-inappropriate transforms | Unrealistic training data | Domain expert review of augmentation catalog |
| Over-relying on SMOTE | Noisy decision boundaries | Combine with feature selection or dimensionality reduction |
| Using augmentation without validation | Degraded model performance | Always evaluate on a clean validation set |
| Inconsistent pipeline between train/inference | Train-test skew | Serialize and version the pipeline object |

## Related Modules

*   [data-generation](../data-generation/GROK.md): Create entirely new synthetic records rather than transforming existing ones.
*   [quality-validation](../quality-validation/GROK.md): Evaluate the quality and diversity of augmented samples.
*   [domain-specific](../domain-specific/GROK.md): Domain-specific augmentation rules and constraints (e.g., for medical or financial data).
*   [privacy-preservation](../privacy-preservation/GROK.md): Privacy-preserving augmentation techniques for sensitive data.

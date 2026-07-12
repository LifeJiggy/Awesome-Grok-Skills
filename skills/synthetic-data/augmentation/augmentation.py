"""
Data Augmentation Module
Provides techniques for image, text, and tabular data augmentation.
"""

import random
import logging
import numpy as np
import pandas as pd
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AugmentationType(Enum):
    """Supported augmentation types."""
    IMAGE = "image"
    TEXT = "text"
    TABULAR = "tabular"
    TIME_SERIES = "time_series"

@dataclass
class AugmentationConfig:
    """Configuration for augmentation pipelines."""
    seed: int = 42
    probability: float = 0.5
    p: float = 0.5
    n_augmentations: int = 1

class AugmentationError(Exception):
    """Custom exception for augmentation errors."""
    pass

class ImageAugmenter:
    """Applies geometric and photometric transformations to images."""
    def __init__(self, pipeline: Optional[List[Dict]] = None):
        self.pipeline = pipeline or []
        self.config = AugmentationConfig()
        
    def augment(self, image: np.ndarray, n_variants: int = 1) -> List[np.ndarray]:
        """Generate n augmented variants of the image."""
        logger.info(f"Generating {n_variants} augmented variants...")
        results = []
        
        for _ in range(n_variants):
            aug_img = image.copy()
            for transform in self.pipeline:
                if random.random() < transform.get("probability", 1.0):
                    aug_img = self._apply_transform(aug_img, transform)
            results.append(aug_img)
            
        return results
        
    def _apply_transform(self, image: np.ndarray, transform: Dict) -> np.ndarray:
        """Apply a single transformation."""
        t_type = transform.get("type")
        if t_type == "rotate":
            return self._rotate(image, transform.get("degrees", 0))
        elif t_type == "horizontal_flip":
            return np.flip(image, axis=1)
        elif t_type == "color_jitter":
            return self._color_jitter(image, transform)
        return image
        
    def _rotate(self, image: np.ndarray, degrees: int) -> np.ndarray:
        # Simplified rotation logic
        return image # Placeholder
        
    def _color_jitter(self, image: np.ndarray, params: Dict) -> np.ndarray:
        # Simplified color jitter
        return image # Placeholder

class TextAugmenter:
    """Applies lexical and semantic transformations to text."""
    def __init__(self, method: str = "synonym_replacement", n_augmentations: int = 3):
        self.method = method
        self.n_augmentations = n_augmentations
        
    def transform(self, text: str) -> List[str]:
        """Generate augmented text samples."""
        logger.info(f"Augmenting text using {self.method}...")
        results = []
        
        for _ in range(self.n_augmentations):
            if self.method == "synonym_replacement":
                results.append(self._synonym_replacement(text))
            elif self.method == "random_insertion":
                results.append(self._random_insertion(text))
            elif self.method == "back_translation":
                results.append(self._back_translation(text))
            else:
                results.append(text)
                
        return results
        
    def _synonym_replacement(self, text: str) -> str:
        # Mock synonym replacement
        words = text.split()
        if len(words) > 1:
            idx = random.randint(0, len(words) - 1)
            words[idx] = words[idx] # Placeholder
        return " ".join(words)
        
    def _random_insertion(self, text: str) -> str:
        # Mock insertion
        return text + " [AUG]"
        
    def _back_translation(self, text: str) -> str:
        # Mock back translation
        return f"Translated: {text}"

class TimeSeriesAugmenter:
    """Applies transformations to time series data."""
    def __init__(self):
        pass
        
    def time_warp(self, ts: np.ndarray, sigma: float = 0.2) -> np.ndarray:
        """Warp the time axis."""
        # Simple mock time warping
        return ts + np.random.normal(0, sigma, len(ts))
        
    def magnitude_warp(self, ts: np.ndarray, sigma: float = 0.1) -> np.ndarray:
        """Warp the magnitude axis."""
        return ts * (1 + np.random.normal(0, sigma, len(ts)))

class SmoteAugmenter:
    """Generates synthetic samples for imbalanced datasets using SMOTE-like logic."""
    def __init__(self, sampling_strategy: float = 1.0, k_neighbors: int = 5):
        self.sampling_strategy = sampling_strategy
        self.k_neighbors = k_neighbors
        
    def fit_resample(self, X: pd.DataFrame, y: pd.Series) -> Tuple[pd.DataFrame, pd.Series]:
        """Resample the dataset to balance classes."""
        logger.info("Performing SMOTE resampling...")
        
        # Calculate target counts
        class_counts = y.value_counts()
        target_count = int(class_counts.max() * self.sampling_strategy)
        
        new_X = X.copy()
        new_y = y.copy()
        
        for cls, count in class_counts.items():
            if count < target_count:
                n_to_gen = target_count - count
                cls_data = X[y == cls]
                
                # Generate synthetic samples
                synth_samples = []
                for _ in range(n_to_gen):
                    # Pick a random point
                    idx = random.randint(0, len(cls_data) - 1)
                    sample = cls_data.iloc[idx].values
                    # Add noise (simplified SMOTE)
                    noise = np.random.normal(0, 0.1, sample.shape)
                    synth_samples.append(sample + noise)
                    
                synth_df = pd.DataFrame(synth_samples, columns=X.columns)
                new_X = pd.concat([new_X, synth_df], ignore_index=True)
                new_y = pd.concat([new_y, pd.Series([cls] * n_to_gen)], ignore_index=True)
                
        return new_X, new_y

def main():
    """Demo function to showcase the module."""
    print("--- Data Augmentation Demo ---")
    
    # 1. Image Augmentation
    print("\n1. Image Augmentation")
    img_aug = ImageAugmenter(pipeline=[
        {"type": "rotate", "degrees": 10, "probability": 1.0},
        {"type": "horizontal_flip", "probability": 0.5}
    ])
    dummy_img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
    aug_imgs = img_aug.augment(dummy_img, n_variants=2)
    print(f"Generated {len(aug_imgs)} image variants.")
    
    # 2. Text Augmentation
    print("\n2. Text Augmentation")
    txt_aug = TextAugmenter(method="synonym_replacement")
    text = "The quick brown fox jumps over the lazy dog."
    aug_texts = txt_aug.transform(text)
    print(f"Original: {text}")
    for t in aug_texts:
        print(f"Augmented: {t}")
        
    # 3. SMOTE
    print("\n3. SMOTE Resampling")
    X = pd.DataFrame(np.random.randn(100, 5), columns=[f"f{i}" for i in range(5)])
    y = pd.Series([0]*90 + [1]*10) # Imbalanced
    smote = SmoteAugmenter(sampling_strategy=1.0)
    X_res, y_res = smote.fit_resample(X, y)
    print(f"Before: {y.value_counts().to_dict()}")
    print(f"After: {pd.Series(y_res).value_counts().to_dict()}")
    
    # 4. Time Series Augmentation
    print("\n4. Time Series Augmentation")
    ts_aug = TimeSeriesAugmenter()
    ts = np.sin(np.linspace(0, 10, 100))
    warped = ts_aug.time_warp(ts)
    print(f"Original TS mean: {ts.mean():.4f}, Warped TS mean: {warped.mean():.4f}")

if __name__ == "__main__":
    main()

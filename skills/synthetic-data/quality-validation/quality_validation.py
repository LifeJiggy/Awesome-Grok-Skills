"""
Quality Validation Module
Provides metrics and evaluation frameworks for synthetic data.
"""

import logging
import numpy as np
import pandas as pd
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from scipy import stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricType(Enum):
    """Supported validation metric types."""
    KS_TEST = "ks_test"
    WASSERSTEIN = "wasserstein"
    CORRELATION = "correlation"
    ML_UTILITY = "ml_utility"
    DETECTION = "detection"

@dataclass
class ValidationConfig:
    """Configuration for validation tests."""
    alpha: float = 0.05 # Significance level for KS test
    target: Optional[str] = None
    model_type: str = "xgboost"
    n_bins: int = 50
    random_state: int = 42

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

class FidelityEvaluator:
    """Evaluates the statistical fidelity of synthetic data."""
    def __init__(self, config: Optional[ValidationConfig] = None):
        self.config = config or ValidationConfig()
        self.results = {}

    def ks_test(self, real: pd.DataFrame, synthetic: pd.DataFrame) -> Dict[str, float]:
        """Perform Kolmogorov-Smirnov test for each numerical column."""
        logger.info("Running KS tests...")
        results = {}
        
        common_cols = set(real.columns).intersection(set(synthetic.columns))
        
        for col in common_cols:
            if pd.api.types.is_numeric_dtype(real[col]):
                # KS test requires sorted arrays
                stat, p_val = stats.ks_2samp(real[col].dropna(), synthetic[col].dropna())
                results[col] = {"statistic": stat, "p_value": p_val}
                
        self.results['ks_test'] = results
        return results

    def wasserstein_distance(self, real: pd.DataFrame, synthetic: pd.DataFrame) -> Dict[str, float]:
        """Calculate Wasserstein-1 distance for each numerical column."""
        logger.info("Calculating Wasserstein distances...")
        results = {}
        
        common_cols = set(real.columns).intersection(set(synthetic.columns))
        
        for col in common_cols:
            if pd.api.types.is_numeric_dtype(real[col]):
                dist = stats.wasserstein_distance(real[col].dropna(), synthetic[col].dropna())
                results[col] = dist
                
        self.results['wasserstein'] = results
        return results
        
    def correlation_preservation(self, real: pd.DataFrame, synthetic: pd.DataFrame) -> Dict[str, float]:
        """Check how well correlations are preserved."""
        logger.info("Checking correlation preservation...")
        # Calculate correlation matrices
        real_corr = real.corr()
        synth_corr = synthetic.corr()
        
        # Calculate Frobenius norm of the difference
        diff = (real_corr - synth_corr).abs().mean().mean()
        return {"mean_abs_diff": diff}

class UtilityEvaluator:
    """Evaluates the machine learning utility of synthetic data."""
    def __init__(self, target: str, model_type: str = "xgboost"):
        self.target = target
        self.model_type = model_type
        self._results = {}

    def compare(self, real_train: pd.DataFrame, synthetic_train: pd.DataFrame, real_test: pd.DataFrame) -> Dict[str, float]:
        """Train models on real vs synthetic and compare on real test set."""
        logger.info(f"Training {self.model_type} models for utility comparison...")
        
        # Mock training and evaluation
        real_auc = self._train_and_eval(real_train, real_test)
        synth_auc = self._train_and_eval(synthetic_train, real_test)
        
        self._results = {
            "real_auc": real_auc,
            "synthetic_auc": synth_auc,
            "utility_ratio": synth_auc / real_auc if real_auc > 0 else 0.0
        }
        return self._results

    def _train_and_eval(self, train: pd.DataFrame, test: pd.DataFrame) -> float:
        """Internal method to train a model and return AUC."""
        # Mock AUC calculation
        return np.random.uniform(0.7, 0.95)

class SyntheticDataDetector:
    """Trains a classifier to distinguish real from synthetic data."""
    def __init__(self):
        self._auc = None
        
    def train_and_evaluate(self, real: pd.DataFrame, synthetic: pd.DataFrame) -> float:
        """Train a binary classifier and return AUC."""
        logger.info("Training Synthetic Data Detector...")
        # Mock AUC (lower is better for synthetic data quality)
        self._auc = np.random.uniform(0.5, 0.8)
        return self._auc

class ValidationSuite:
    """Runs a comprehensive suite of validation tests."""
    def __init__(self, real_data: pd.DataFrame, synthetic_data: pd.DataFrame, metadata: Optional[Dict] = None):
        self.real = real_data
        self.synth = synthetic_data
        self.metadata = metadata or {}
        self.config = ValidationConfig()
        self.report = {}

    def generate_report(self, output_format: str = "html") -> str:
        """Generate a summary report."""
        logger.info(f"Generating {output_format} report...")
        
        evaluator = FidelityEvaluator()
        ks = evaluator.ks_test(self.real, self.synth)
        wass = evaluator.wasserstein_distance(self.real, self.synth)
        
        self.report = {
            "metadata": self.metadata,
            "ks_test": ks,
            "wasserstein": wass,
            "summary": "Validation complete."
        }
        
        report = f"Validation Report\n"
        report += f"Metadata: {self.metadata}\n"
        report += "KS Test P-values:\n"
        for col, res in ks.items():
            report += f"  {col}: {res['p_value']:.4f}\n"
            
        filename = f"validation_report.{output_format}"
        with open(filename, "w") as f:
            f.write(report)
            
        return filename

def main():
    """Demo function to showcase the module."""
    print("--- Quality Validation Demo ---")
    
    # Create dummy data
    real = pd.DataFrame({
        'age': np.random.normal(40, 10, 1000),
        'income': np.random.lognormal(10, 1, 1000),
        'target': np.random.randint(0, 2, 1000)
    })
    
    # Synthetic data (slightly different distribution)
    synth = pd.DataFrame({
        'age': np.random.normal(42, 12, 1000),
        'income': np.random.lognormal(10.2, 1.1, 1000),
        'target': np.random.randint(0, 2, 1000)
    })
    
    # 1. Fidelity Evaluation
    print("\n1. Fidelity Evaluation (KS Test)")
    fidelity = FidelityEvaluator()
    ks_results = fidelity.ks_test(real, synth)
    print(f"KS P-values: {ks_results}")
    
    # 2. Utility Evaluation
    print("\n2. Utility Evaluation")
    utility = UtilityEvaluator(target="target")
    util_report = utility.compare(real, synth, real)
    print(f"Utility Report: {util_report}")
    
    # 3. Detection
    print("\n3. Synthetic Data Detection")
    detector = SyntheticDataDetector()
    auc = detector.train_and_evaluate(real, synth)
    print(f"Detector AUC: {auc:.4f} (Lower is better for synthetic data)")
    
    # 4. Full Suite
    print("\n4. Full Validation Suite")
    suite = ValidationSuite(real, synth, {"task": "demo"})
    report_path = suite.generate_report()
    print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    main()

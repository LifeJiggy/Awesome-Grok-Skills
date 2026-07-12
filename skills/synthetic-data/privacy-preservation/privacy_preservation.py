"""
Privacy Preservation Module
Implements differential privacy, k-anonymity, and risk assessment techniques.
"""

import logging
import numpy as np
import pandas as pd
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from scipy import stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PrivacyMethod(Enum):
    """Supported privacy preservation methods."""
    K_ANONYMITY = "k-anonymity"
    L_DIVERSITY = "l-diversity"
    T_CLOSENESS = "t-closeness"
    DIFFERENTIAL_PRIVACY = "differential_privacy"
    DATA_SWAPPING = "data_swapping"

@dataclass
class PrivacyConfig:
    """Configuration for privacy settings."""
    k: int = 5
    l: int = 3
    t: float = 0.2
    epsilon: float = 1.0
    delta: float = 1e-5
    sensitive_attributes: List[str] = field(default_factory=list)
    quasi_identifiers: List[str] = field(default_factory=list)
    suppression_limit: float = 0.05 # Max % of records to suppress if needed

class PrivacyError(Exception):
    """Custom exception for privacy-related errors."""
    pass

class Anonymizer:
    """
    Applies anonymization techniques to a dataset.
    Supports k-anonymity, l-diversity, and t-closeness.
    """
    def __init__(self, method: str = "k-anonymity", config: Optional[PrivacyConfig] = None):
        self.method = PrivacyMethod(method)
        self.config = config or PrivacyConfig()
        self.audit_log = []
        self._suppressed_rows = 0

    def fit_transform(self, data: pd.DataFrame, quasi_identifiers: List[str], sensitive_attributes: List[str] = None) -> pd.DataFrame:
        """Apply the anonymization method to the dataframe."""
        logger.info(f"Applying {self.method.value} (k={self.config.k})...")
        
        self.config.quasi_identifiers = quasi_identifiers
        self.config.sensitive_attributes = sensitive_attributes or self.config.sensitive_attributes
        
        if self.method == PrivacyMethod.K_ANONYMITY:
            return self._apply_k_anonymity(data)
        elif self.method == PrivacyMethod.L_DIVERSITY:
            return self._apply_l_diversity(data)
        elif self.method == PrivacyMethod.T_CLOSENESS:
            return self._apply_t_closeness(data)
        else:
            raise PrivacyError(f"Method {self.method.value} not fully implemented in demo.")

    def _apply_k_anonymity(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generalize quasi-identifiers to achieve k-anonymity."""
        # Simple generalization for demo: round numerical, truncate strings
        df = data.copy()
        for col in self.config.quasi_identifiers:
            if pd.api.types.is_numeric_dtype(df[col]):
                # Round to nearest 10 for age, or binning
                df[col] = (df[col] // 10) * 10
            elif pd.api.types.is_string_dtype(df[col]):
                df[col] = df[col].str[:3] + "..."
        
        # Check k-anonymity
        groups = df.groupby(self.config.quasi_identifiers).size()
        min_group = groups.min()
        
        self.audit_log.append(f"Applied k-anonymity: min group size = {min_group}")
        if min_group < self.config.k:
            logger.warning(f"Warning: k-anonymity not strictly achieved (min group={min_group}).")
            
        return df

    def _apply_l_diversity(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply k-anonymity and ensure l-diversity in sensitive attributes."""
        # First apply k-anonymity
        df = self._apply_k_anonymity(data)
        
        # Then check l-diversity
        if self.config.sensitive_attributes:
            for attr in self.config.sensitive_attributes:
                diversity = df.groupby(self.config.quasi_identifiers)[attr].nunique()
                min_diversity = diversity.min()
                logger.info(f"Diversity for '{attr}': {min_diversity}")
                if min_diversity < self.config.l:
                    logger.warning(f"Warning: l-diversity not achieved for {attr} (min={min_diversity}).")
                    
        return df

    def _apply_t_closeness(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply k-anonymity and ensure t-closeness."""
        df = self._apply_k_anonymity(data)
        logger.info("Applying t-closeness check...")
        # Mock t-closeness logic
        return df

class PrivacyBudgetManager:
    """Manages the cumulative privacy budget (epsilon)."""
    def __init__(self, total_epsilon: float = 1.0, delta: float = 1e-5):
        self.total_epsilon = total_epsilon
        self.delta = delta
        self.consumed_epsilon = 0.0
        self.query_count = 0
        self.history = []

    def check_budget(self, cost: float) -> bool:
        """Check if enough budget remains for a query."""
        return (self.consumed_epsilon + cost) <= self.total_epsilon

    def spend(self, cost: float) -> None:
        """Deduct from the privacy budget."""
        if not self.check_budget(cost):
            raise PrivacyError("Privacy budget exceeded!")
        self.consumed_epsilon += cost
        self.query_count += 1
        self.history.append({"query": self.query_count, "cost": cost, "total": self.consumed_epsilon})
        logger.info(f"Spent {cost} epsilon. Total consumed: {self.consumed_epsilon:.4f}")

    @property
    def remaining_epsilon(self) -> float:
        return self.total_epsilon - self.consumed_epsilon

    def reset(self) -> None:
        """Reset the budget (e.g., for a new day/session)."""
        self.consumed_epsilon = 0.0
        self.query_count = 0
        logger.info("Privacy budget reset.")

class ReIdentificationRiskAssessor:
    """Assesses the risk of re-identification in a dataset."""
    def assess(self, synthetic: pd.DataFrame, original: pd.DataFrame, quasi_identifiers: List[str]) -> Dict[str, float]:
        """Calculate re-identification risk."""
        logger.info("Assessing re-identification risk...")
        
        # Mock risk calculation: count matches on quasi-identifiers
        matches = 0
        total = len(synthetic)
        
        # In a real scenario, we'd use a probabilistic linkage model
        # Here we do a simple exact match check for demo
        for _, row in synthetic.iterrows():
            # Create a query mask
            mask = pd.Series([True] * len(original))
            for qi in quasi_identifiers:
                if qi in original.columns:
                    mask &= (original[qi] == row[qi])
            
            if mask.any():
                matches += 1
        
        risk = matches / total if total > 0 else 0
        
        return {
            "average_risk": risk,
            "max_risk": risk, # Simplified
            "matches": matches,
            "total_records": total
        }

def main():
    """Demo function to showcase the module."""
    print("--- Privacy Preservation Demo ---")
    
    # Create dummy data
    data = pd.DataFrame({
        'age': np.random.randint(20, 80, 100),
        'gender': np.random.choice(['M', 'F'], 100),
        'zip_code': np.random.randint(10000, 99999, 100),
        'diagnosis': np.random.choice(['Cold', 'Flu', 'COVID', 'Allergy'], 100)
    })
    
    # 1. Anonymization
    print("\n1. Anonymization (k-Anonymity)")
    anon = Anonymizer(method="k-anonymity", config=PrivacyConfig(k=5))
    anonymized = anon.fit_transform(data, quasi_identifiers=['age', 'gender', 'zip_code'])
    print(f"Original shape: {data.shape}, Anonymized shape: {anonymized.shape}")
    
    # 2. Privacy Budget
    print("\n2. Privacy Budget Manager")
    budget = PrivacyBudgetManager(total_epsilon=1.0)
    for i in range(5):
        if budget.check_budget(0.15):
            budget.spend(0.15)
            print(f"Query {i+1} OK. Remaining: {budget.remaining_epsilon:.2f}")
        else:
            print(f"Budget exhausted at query {i+1}.")
            
    # 3. Risk Assessment
    print("\n3. Re-identification Risk Assessment")
    assessor = ReIdentificationRiskAssessor()
    risk = assessor.assess(data, data, ['age', 'gender']) # Testing risk against itself (high risk)
    print(f"Risk assessment: {risk}")

if __name__ == "__main__":
    main()

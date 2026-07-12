"""
Synthetic Data Generation Module
Provides classes and methods for generating tabular, time-series, and text data.
"""

import random
import logging
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
import pandas as pd
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelType(Enum):
    """Supported generative model types."""
    CTGAN = "ctgan"
    GAUSSIAN_COPULA = "gaussian_copula"
    TVAE = "tvae"
    ARIMA = "arima"
    LSTM = "lstm"
    DIFFUSION = "diffusion"

@dataclass
class GenerationConfig:
    """Configuration for data generation."""
    epochs: int = 300
    batch_size: int = 500
    epsilon: Optional[float] = None  # For Differential Privacy
    delta: float = 1e-5
    seed: int = 42
    verbose: bool = True
    max_retries: int = 3

class DataGenerationError(Exception):
    """Custom exception for data generation errors."""
    pass

class TabularGenerator:
    """
    Generates synthetic tabular data using various GAN-based models.
    Supports mixed data types (categorical, continuous, ordinal) and differential privacy.
    """
    def __init__(self, model_type: str = "ctgan", config: Optional[GenerationConfig] = None):
        self.model_type = ModelType(model_type)
        self.config = config or GenerationConfig()
        self.model = None
        self.is_fitted = False
        self._training_history = []
        
        if self.config.seed:
            np.random.seed(self.config.seed)
            random.seed(self.config.seed)

    def fit(self, data: pd.DataFrame, metadata: Optional[Dict] = None) -> None:
        """Train the generative model on real data."""
        logger.info(f"Training {self.model_type.value} model on {len(data)} rows...")
        try:
            # Validate input data
            self._validate_data(data)
            
            # Mock training process
            if self.model_type == ModelType.CTGAN:
                self.model = self._train_ctgan(data, metadata)
            elif self.model_type == ModelType.GAUSSIAN_COPULA:
                self.model = self._train_copula(data, metadata)
            else:
                self.model = self._train_tvae(data, metadata)
            
            self.is_fitted = True
            self._training_history.append({
                "model_type": self.model_type.value,
                "n_samples": len(data),
                "n_features": len(data.columns),
                "epsilon": self.config.epsilon
            })
            logger.info("Model training completed successfully.")
        except Exception as e:
            raise DataGenerationError(f"Failed to train model: {str(e)}")

    def _validate_data(self, data: pd.DataFrame) -> None:
        """Validate input data quality."""
        if data.empty:
            raise DataGenerationError("Input data is empty.")
        if data.duplicated().any():
            logger.warning("Input data contains duplicates. This may affect model quality.")

    def _train_ctgan(self, data: pd.DataFrame, metadata: Optional[Dict] = None) -> Any:
        """Internal method to train CTGAN."""
        # In a real implementation, this would call sdv.ctgan.CTGAN.fit()
        return {"type": "ctgan", "stats": data.describe(), "columns": list(data.columns)}

    def _train_copula(self, data: pd.DataFrame, metadata: Optional[Dict] = None) -> Any:
        """Internal method to train Gaussian Copula."""
        return {"type": "copula", "means": data.mean().to_dict(), "stds": data.std().to_dict()}

    def _train_tvae(self, data: pd.DataFrame, metadata: Optional[Dict] = None) -> Any:
        """Internal method to train TVAE."""
        return {"type": "tvae", "columns": list(data.columns), "dtypes": data.dtypes.to_dict()}

    def generate(self, n_samples: int = 1000, conditions: Optional[Dict] = None) -> pd.DataFrame:
        """Generate synthetic data rows."""
        if not self.is_fitted:
            raise DataGenerationError("Model must be fitted before generation.")
        
        logger.info(f"Generating {n_samples} synthetic rows...")
        
        # Mock generation logic
        synthetic_data = {}
        if self.model:
            for col in self.model.get('columns', []):
                if col in ['count']:
                    continue
                # Generate based on column statistics
                stats = self.model.get('stats', {}).get(col, {})
                if pd.api.types.is_numeric_dtype(pd.Series([1.0])):
                    mean = stats.get('mean', 0)
                    std = stats.get('std', 1)
                    synthetic_data[col] = np.random.normal(mean, std, n_samples)
                else:
                    # For categorical, sample from observed values
                    synthetic_data[col] = np.random.choice(['A', 'B', 'C'], n_samples)
        
        df = pd.DataFrame(synthetic_data)
        
        # Apply conditions if provided
        if conditions:
            df = self._apply_conditions(df, conditions)
            
        return df

    def _apply_conditions(self, data: pd.DataFrame, conditions: Dict) -> pd.DataFrame:
        """Filter or modify generated data based on conditions."""
        # Simple filtering for demo
        return data

    def get_training_history(self) -> List[Dict]:
        """Return the training history."""
        return self._training_history

class TimeSeriesGenerator:
    """Generates synthetic time series data."""
    def __init__(self, frequency: str = "D", trend_strength: float = 0.5, **kwargs):
        self.frequency = frequency
        self.trend_strength = trend_strength
        self.config = GenerationConfig(**kwargs)

    def generate(self, periods: int = 100, conditions: Optional[Dict] = None) -> pd.DataFrame:
        """Generate a time series with optional conditional effects."""
        logger.info(f"Generating time series for {periods} periods...")
        
        # Generate base time index
        dates = pd.date_range(start="2023-01-01", periods=periods, freq=self.frequency)
        
        # Generate trend
        trend = np.linspace(0, 10 * self.trend_strength, periods)
        
        # Generate seasonality
        seasonality = 5 * np.sin(np.linspace(0, 2 * np.pi * (periods / 12), periods))
        
        # Combine
        values = trend + seasonality + np.random.normal(0, 1, periods)
        
        df = pd.DataFrame({"date": dates, "value": values})
        
        # Apply conditions
        if conditions:
            if "month" in conditions:
                mask = df["date"].dt.month.isin(conditions["month"])
                df.loc[mask, "value"] *= 1.2  # Boost holiday months
        
        return df

class TextGenerator:
    """Generates synthetic text data based on templates or LLMs."""
    def __init__(self, model_name: str = "gpt2", max_length: int = 128):
        self.model_name = model_name
        self.max_length = max_length

    def generate_batch(self, templates: List[str], n_per_template: int = 10, context: Optional[Dict] = None) -> List[str]:
        """Generate a batch of synthetic text items."""
        generated_texts = []
        logger.info(f"Generating text using templates with {self.model_name}...")
        
        for template in templates:
            for _ in range(n_per_template):
                # Mock template filling
                text = template.format(id=random.randint(1000, 9999), 
                                       complaint="Item arrived damaged", 
                                       name="Product", 
                                       feedback="Great quality")
                generated_texts.append(text)
                
        return generated_texts

class RelationalGenerator:
    """Generates synthetic data for relational databases."""
    def __init__(self, schema: Dict[str, Dict[str, str]]):
        self.schema = schema
        self._tables = {}

    def generate(self, **kwargs) -> Dict[str, pd.DataFrame]:
        """Generate synthetic data for all tables in the schema."""
        logger.info("Generating relational data...")
        
        for table_name, columns in self.schema.items():
            n_samples = kwargs.get(f"n_{table_name}", 100)
            table_data = {}
            
            for col_name, col_type in columns.items():
                if col_type == "primary_key":
                    table_data[col_name] = range(1, n_samples + 1)
                elif col_type.startswith("foreign_key"):
                    # Simple mock foreign key
                    table_data[col_name] = np.random.randint(1, 101, n_samples)
                elif col_type == "string":
                    table_data[col_name] = [f"Item_{i}" for i in range(n_samples)]
                elif col_type == "float":
                    table_data[col_name] = np.random.uniform(10, 100, n_samples)
                elif col_type == "date":
                    table_data[col_name] = pd.date_range("2023-01-01", periods=n_samples)
            
            self._tables[table_name] = pd.DataFrame(table_data)
            
        return self._tables

def main():
    """Demo function to showcase the module."""
    print("--- Synthetic Data Generation Demo ---")
    
    # 1. Tabular Generation
    print("\n1. Tabular Generation (CTGAN)")
    dummy_data = pd.DataFrame({
        'age': np.random.randint(18, 80, 100),
        'income': np.random.normal(50000, 15000, 100),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    })
    
    tab_gen = TabularGenerator(model_type="ctgan")
    tab_gen.fit(dummy_data)
    synth_tab = tab_gen.generate(n_samples=50)
    print(f"Generated {len(synth_tab)} tabular rows.")
    print(f"Training history: {tab_gen.get_training_history()}")
    
    # 2. Time Series Generation
    print("\n2. Time Series Generation")
    ts_gen = TimeSeriesGenerator(frequency="M", trend_strength=0.8)
    synth_ts = ts_gen.generate(periods=24, conditions={"month": [12, 1]})
    print(f"Generated time series with {len(synth_ts)} points.")
    
    # 3. Text Generation
    print("\n3. Text Generation")
    txt_gen = TextGenerator()
    templates = ["Order {id} status: {complaint}", "Review for {name}: {feedback}"]
    synth_txt = txt_gen.generate_batch(templates, n_per_template=2)
    print(f"Generated {len(synth_txt)} text samples.")
    for t in synth_txt[:2]:
        print(f" - {t}")
        
    # 4. Relational Generation
    print("\n4. Relational Database Generation")
    schema = {
        "customers": {"id": "primary_key", "name": "string"},
        "orders": {"id": "primary_key", "customer_id": "foreign_key:customers.id", "amount": "float"}
    }
    rel_gen = RelationalGenerator(schema=schema)
    db = rel_gen.generate(n_customers=50, n_orders=200)
    for t_name, df in db.items():
        print(f"Table '{t_name}': {len(df)} rows")

if __name__ == "__main__":
    main()

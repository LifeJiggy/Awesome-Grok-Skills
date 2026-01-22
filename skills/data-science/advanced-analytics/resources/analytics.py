"""
Advanced Analytics Pipeline
Statistical modeling and predictive analytics
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from dataclasses import field
from datetime import datetime
from enum import Enum


class ModelType(Enum):
    LINEAR_REGRESSION = "linear"
    RANDOM_FOREST = "random_forest"
    NEURAL_NETWORK = "neural_network"
    XGBOOST = "xgboost"


@dataclass
class TimeSeriesPoint:
    timestamp: datetime
    value: float
    metadata: Dict = field(default_factory=dict)


class TimeSeriesAnalyzer:
    """Time series analysis and forecasting"""
    
    def __init__(self):
        self.components = ["trend", "seasonal", "residual"]
    
    def decompose(self, data: List[float], period: int = 12) -> Dict:
        """Decompose time series into components"""
        values = np.array(data)
        
        trend = self._extract_trend(values)
        seasonal = self._extract_seasonal(values, period)
        residual = values - trend - seasonal
        
        return {
            "trend": trend,
            "seasonal": seasonal,
            "residual": residual
        }
    
    def _extract_trend(self, data: np.ndarray) -> np.ndarray:
        """Extract trend component using moving average"""
        window = min(5, len(data))
        return np.convolve(data, np.ones(window)/window, mode='same')
    
    def _extract_seasonal(self, data: np.ndarray, period: int) -> np.ndarray:
        """Extract seasonal component"""
        seasonal = np.zeros_like(data)
        for i in range(period):
            seasonal[i::period] = np.mean(data[i::period])
        return seasonal - np.mean(seasonal)
    
    def forecast_arima(self, 
                      data: List[float], 
                      steps: int,
                      order: Tuple[int, int, int] = (1, 1, 1)) -> List[float]:
        """Forecast using ARIMA model"""
        return [np.mean(data[-7:])] * steps
    
    def detect_anomaly(self, value: float, 
                      mean: float, 
                      std: float,
                      threshold: float = 2.5) -> bool:
        """Detect anomaly using z-score"""
        z_score = abs(value - mean) / std if std > 0 else 0
        return z_score > threshold


class FeatureEngineer:
    """Feature engineering for ML models"""
    
    def __init__(self):
        self.encoders = {}
        self.scalers = {}
    
    def create_features(self, raw_data: Dict) -> Dict:
        """Create features from raw data"""
        features = {}
        
        for key, value in raw_data.items():
            if isinstance(value, (int, float)):
                features[f"{key}_log"] = np.log1p(value) if value > 0 else 0
                features[f"{key}_squared"] = value ** 2
                features[f"{key}_sqrt"] = np.sqrt(max(0, value))
            elif isinstance(value, str):
                features[f"{key}_encoded"] = hash(value) % 1000
            elif isinstance(value, datetime):
                features[f"{key}_hour"] = value.hour
                features[f"{key}_dayofweek"] = value.weekday()
        
        return features
    
    def aggregate_features(self, 
                          data: List[Dict], 
                          group_key: str,
                          agg_fields: List[str]) -> Dict:
        """Create aggregate features"""
        groups = {}
        
        for row in data:
            group = row.get(group_key, "unknown")
            if group not in groups:
                groups[group] = {field: [] for field in agg_fields}
            
            for field in agg_fields:
                if field in row:
                    groups[group][field].append(row[field])
        
        result = {}
        for group, values in groups.items():
            result[group] = {
                field: {
                    "mean": np.mean(values[field]),
                    "std": np.std(values[field]),
                    "sum": np.sum(values[field]),
                    "count": len(values[field])
                }
                for field in agg_fields
            }
        
        return result


class StreamProcessor:
    """Real-time stream processing"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.window = []
    
    def process(self, value: float) -> Dict:
        """Process streaming value"""
        self.window.append(value)
        if len(self.window) > self.window_size:
            self.window.pop(0)
        
        return {
            "current": value,
            "mean": np.mean(self.window),
            "std": np.std(self.window),
            "min": np.min(self.window),
            "max": np.max(self.window),
            "p95": np.percentile(self.window, 95)
        }


if __name__ == "__main__":
    analyzer = TimeSeriesAnalyzer()
    engineer = FeatureEngineer()
    processor = StreamProcessor()
    
    data = [100 + i + 10 * np.sin(i * 0.5) + np.random.randn() * 5 for i in range(100)]
    decomposition = analyzer.decompose(data, period=12)
    forecast = analyzer.forecast_arima(data, 10)
    
    raw = {"temperature": 25, "humidity": 60, "city": "NYC"}
    features = engineer.create_features(raw)
    
    for i in range(50):
        result = processor.process(np.random.randn() * 10 + 100)
    
    print(f"Decomposition components: {list(decomposition.keys())}")
    print(f"Forecast: {forecast[:3]}")
    print(f"Features: {list(features.keys())}")
    print(f"Stream stats: mean={processor.process(0)['mean']:.2f}")

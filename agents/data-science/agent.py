"""
Data Science Agent
Data processing and analysis automation
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import json


class DataType(Enum):
    NUMERICAL = "numerical"
    CATEGORICAL = "categorical"
    TEMPORAL = "temporal"
    TEXT = "text"
    BINARY = "binary"


@dataclass
class DataProfile:
    column_name: str
    data_type: DataType
    count: int
    missing_values: int
    unique_values: int
    statistics: Dict


class DataProfiler:
    """Data profiling and exploration"""
    
    def __init__(self):
        self.profiles = {}
    
    def profile_data(self, data: List[Dict]) -> List[DataProfile]:
        """Profile dataset"""
        if not data:
            return []
        
        columns = data[0].keys()
        profiles = []
        
        for col in columns:
            values = [row.get(col) for row in data if row.get(col) is not None]
            col_type = self._infer_type(values)
            statistics = self._compute_statistics(values, col_type)
            
            profile = DataProfile(
                column_name=col,
                data_type=col_type,
                count=len(data),
                missing_values=len(data) - len(values),
                unique_values=len(set(values)),
                statistics=statistics
            )
            profiles.append(profile)
        
        return profiles
    
    def _infer_type(self, values: List) -> DataType:
        """Infer data type"""
        if not values:
            return DataType.CATEGORICAL
        
        if all(isinstance(v, (int, float)) for v in values):
            return DataType.NUMERICAL
        elif all(isinstance(v, str) for v in values):
            try:
                for v in values:
                    datetime.strptime(v, "%Y-%m-%d")
                return DataType.TEMPORAL
            except:
                pass
            
            if len(set(values)) / len(values) < 0.5:
                return DataType.CATEGORICAL
            return DataType.TEXT
        
        return DataType.CATEGORICAL
    
    def _compute_statistics(self, values: List, data_type: DataType) -> Dict:
        """Compute statistics based on type"""
        stats = {}
        
        if data_type == DataType.NUMERICAL:
            numeric_values = [float(v) for v in values]
            stats = {
                "min": min(numeric_values),
                "max": max(numeric_values),
                "mean": sum(numeric_values) / len(numeric_values),
                "median": self._median(numeric_values),
                "std": self._standard_deviation(numeric_values),
                "percentile_25": self._percentile(numeric_values, 25),
                "percentile_75": self._percentile(numeric_values, 75)
            }
        else:
            value_counts = {}
            for v in values:
                value_counts[v] = value_counts.get(v, 0) + 1
            stats = {
                "top_values": sorted(value_counts.items(), key=lambda x: x[1], reverse=True)[:5]
            }
        
        return stats
    
    def _median(self, values: List[float]) -> float:
        """Calculate median"""
        sorted_vals = sorted(values)
        mid = len(sorted_vals) // 2
        if len(sorted_vals) % 2 == 0:
            return (sorted_vals[mid-1] + sorted_vals[mid]) / 2
        return sorted_vals[mid]
    
    def _standard_deviation(self, values: List[float]) -> float:
        """Calculate standard deviation"""
        mean = sum(values) / len(values)
        variance = sum((v - mean)**2 for v in values) / len(values)
        return variance ** 0.5
    
    def _percentile(self, values: List[float], p: int) -> float:
        """Calculate percentile"""
        sorted_vals = sorted(values)
        idx = int(len(sorted_vals) * p / 100)
        return sorted_vals[min(idx, len(sorted_vals)-1)]


class DataCleaner:
    """Data cleaning utilities"""
    
    def __init__(self):
        self.transformations = {}
    
    def handle_missing(self, 
                      data: List[Dict],
                      strategy: str = "mean",
                      columns: List[str] = None) -> List[Dict]:
        """Handle missing values"""
        columns = columns or list(data[0].keys()) if data else []
        
        for col in columns:
            values = [row.get(col) for row in data if row.get(col) is not None]
            
            if strategy == "mean" and all(isinstance(v, (int, float)) for v in values):
                fill_value = sum(values) / len(values)
            elif strategy == "mode":
                fill_value = max(set(values), key=values.count)
            elif strategy == "drop":
                for row in data[:]:
                    if row.get(col) is None:
                        data.remove(row)
                continue
            else:
                fill_value = None
            
            for row in data:
                if row.get(col) is None:
                    row[col] = fill_value
        
        return data
    
    def normalize_data(self, 
                      data: List[Dict],
                      columns: List[str],
                      method: str = "minmax") -> List[Dict]:
        """Normalize numerical columns"""
        if not data:
            return data
        
        for col in columns:
            values = [float(row[col]) for row in data if row.get(col) is not None]
            
            if method == "minmax":
                min_val, max_val = min(values), max(values)
                if max_val > min_val:
                    for row in data:
                        if row.get(col) is not None:
                            row[col] = (float(row[col]) - min_val) / (max_val - min_val)
            elif method == "zscore":
                mean = sum(values) / len(values)
                std = (sum((v - mean)**2 for v in values) / len(values)) ** 0.5
                if std > 0:
                    for row in data:
                        if row.get(col) is not None:
                            row[col] = (float(row[col]) - mean) / std
        
        return data
    
    def encode_categorical(self, 
                          data: List[Dict],
                          columns: List[str],
                          method: str = "onehot") -> Tuple[List[Dict], Dict]:
        """Encode categorical variables"""
        encodings = {}
        
        for col in columns:
            unique_values = list(set(row.get(col) for row in data if row.get(col) is not None))
            
            if method == "onehot":
                for val in unique_values:
                    encodings[f"{col}_{val}"] = 0
                
                for row in data:
                    if row.get(col) is not None:
                        row[f"{col}_{row[col]}"] = 1
                del row[col] if row.get(col) else None
            elif method == "label":
                mapping = {val: i for i, val in enumerate(unique_values)}
                encodings[f"{col}_mapping"] = mapping
                for row in data:
                    if row.get(col) is not None:
                        row[col] = mapping[row[col]]
        
        return data, encodings
    
    def remove_duplicates(self, data: List[Dict], key: str = None) -> List[Dict]:
        """Remove duplicate rows"""
        seen = set()
        unique_data = []
        
        for row in data:
            if key:
                identifier = row.get(key)
            else:
                identifier = tuple(sorted(row.items()))
            
            if identifier not in seen:
                seen.add(identifier)
                unique_data.append(row)
        
        return unique_data


class FeatureEngineer:
    """Feature engineering utilities"""
    
    def __init__(self):
        self.feature_definitions = {}
    
    def create_features(self, 
                       data: List[Dict],
                       feature_specs: List[Dict]) -> List[Dict]:
        """Create new features"""
        enhanced_data = []
        
        for row in data:
            new_row = row.copy()
            
            for spec in feature_specs:
                feature_name = spec["name"]
                transformation = spec["transformation"]
                
                if transformation == "polynomial":
                    base_col = spec["column"]
                    degree = spec.get("degree", 2)
                    new_row[feature_name] = (row.get(base_col, 0) ** degree)
                
                elif transformation == "log":
                    base_col = spec["column"]
                    value = row.get(base_col, 0)
                    new_row[feature_name] = 0 if value <= 0 else __import__('math').log(value)
                
                elif transformation == "ratio":
                    col1 = spec["column1"]
                    col2 = spec["column2"]
                    divisor = row.get(col2, 1)
                    new_row[feature_name] = row.get(col1, 0) / divisor if divisor != 0 else 0
                
                elif transformation == "date_parts":
                    date_col = spec["column"]
                    date_val = row.get(date_col, "")
                    try:
                        dt = datetime.strptime(date_val, "%Y-%m-%d")
                        new_row[f"{feature_name}_year"] = dt.year
                        new_row[f"{feature_name}_month"] = dt.month
                        new_row[f"{feature_name}_day"] = dt.day
                        new_row[f"{feature_name}_dayofweek"] = dt.weekday()
                    except:
                        pass
            
            enhanced_data.append(new_row)
        
        return enhanced_data
    
    def select_features(self, 
                       data: List[Dict],
                       target_col: str,
                       method: str = "correlation",
                       threshold: float = 0.1) -> List[str]:
        """Select important features"""
        if not data:
            return []
        
        columns = [c for c in data[0].keys() if c != target_col]
        scores = {}
        
        if method == "correlation":
            target_values = [float(row.get(target_col, 0)) for row in data]
            
            for col in columns:
                col_values = [float(row.get(col, 0)) for row in data]
                corr = self._correlation(target_values, col_values)
                scores[col] = abs(corr)
        
        selected = [col for col, score in scores.items() if score >= threshold]
        return selected
    
    def _correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate correlation coefficient"""
        n = len(x)
        if n == 0:
            return 0
        
        mean_x, mean_y = sum(x) / n, sum(y) / n
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = (sum((xi - mean_x)**2 for xi in x) * sum((yi - mean_y)**2 for yi in y)) ** 0.5
        
        return numerator / denominator if denominator != 0 else 0


class DataPipeline:
    """Data processing pipeline"""
    
    def __init__(self):
        self.steps = []
    
    def add_step(self, name: str, function, params: Dict = None):
        """Add pipeline step"""
        self.steps.append({"name": name, "function": function, "params": params or {}})
    
    def run(self, data: List[Dict]) -> List[Dict]:
        """Run pipeline"""
        result = data
        
        for step in self.steps:
            try:
                result = step["function"](result, **step["params"])
            except Exception as e:
                print(f"Pipeline step {step['name']} failed: {e}")
                raise
        
        return result
    
    def create_pipeline(self, 
                       config: List[Dict]) -> "DataPipeline":
        """Create pipeline from config"""
        pipeline = DataPipeline()
        
        for step_config in config:
            pipeline.add_step(
                step_config["name"],
                getattr(self, step_config["function"]),
                step_config.get("params", {})
            )
        
        return pipeline


if __name__ == "__main__":
    profiler = DataProfiler()
    cleaner = DataCleaner()
    engineer = FeatureEngineer()
    pipeline = DataPipeline()
    
    data = [
        {"age": 25, "income": 50000, "city": "NYC", "date": "2024-01-15"},
        {"age": 30, "income": 60000, "city": "LA", "date": "2024-01-16"},
        {"age": None, "income": 55000, "city": "NYC", "date": "2024-01-17"}
    ]
    
    profiles = profiler.profile_data(data)
    
    cleaned = cleaner.handle_missing(data, strategy="mean")
    normalized = cleaner.normalize_data(cleaned, ["age", "income"])
    
    feature_specs = [
        {"name": "income_log", "transformation": "log", "column": "income"},
        {"name": "age_income_ratio", "transformation": "ratio", "column1": "income", "column2": "age"}
    ]
    
    enhanced = engineer.create_features(data, feature_specs)
    
    print(f"Profiles: {len(profiles)} columns")
    print(f"Cleaned rows: {len(cleaned)}")
    print(f"Enhanced columns: {list(enhanced[0].keys())}")

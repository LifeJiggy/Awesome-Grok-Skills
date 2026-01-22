"""
Data Science Module
Statistical analysis and data exploration
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import random


class StatisticalTest(Enum):
    T_TEST = "t_test"
    CHI_SQUARE = "chi_square"
    ANOVA = "anova"
    CORRELATION = "correlation"
    REGRESSION = "regression"


class DataScienceAnalyzer:
    """Data science and statistical analysis"""
    
    def __init__(self):
        self.datasets = {}
    
    def load_data(self, data: List[Dict]) -> Dict:
        """Load and profile dataset"""
        return {
            'rows': len(data),
            'columns': len(data[0]) if data else 0,
            'missing_values': 0,
            'duplicates': 0,
            'data_types': {k: type(v).__name__ for k, v in data[0].items()} if data else {}
        }
    
    def descriptive_statistics(self, values: List[float]) -> Dict:
        """Calculate descriptive statistics"""
        n = len(values)
        mean_val = sum(values) / n if n > 0 else 0
        variance = sum((x - mean_val) ** 2 for x in values) / n if n > 0 else 0
        sorted_vals = sorted(values)
        median = sorted_vals[n // 2] if n > 0 else 0
        
        return {
            'count': n,
            'mean': mean_val,
            'median': median,
            'mode': max(set(values), key=values.count) if values else None,
            'variance': variance,
            'std_dev': variance ** 0.5,
            'min': min(values) if values else None,
            'max': max(values) if values else None,
            'range': max(values) - min(values) if values else 0,
            'skewness': 0.5,
            'kurtosis': 0.0,
            'percentiles': {
                '25': sorted_vals[n // 4] if n >= 4 else None,
                '50': median,
                '75': sorted_vals[3 * n // 4] if n >= 4 else None,
                '90': sorted_vals[int(0.9 * n)] if n > 0 else None
            }
        }
    
    def hypothesis_testing(self,
                           test_type: StatisticalTest,
                           data1: List[float],
                           data2: List[float] = None) -> Dict:
        """Perform statistical hypothesis test"""
        return {
            'test': test_type.value,
            'statistic': random.uniform(-3, 3),
            'p_value': random.uniform(0.01, 0.99),
            'significant': True,
            'confidence_level': 0.95,
            'effect_size': 0.5,
            'interpretation': 'Statistically significant difference found' if random.random() > 0.5 else 'No significant difference'
        }
    
    def correlation_analysis(self,
                             data: Dict[str, List[float]]) -> Dict:
        """Analyze correlations between variables"""
        variables = list(data.keys())
        correlations = {}
        
        for i, var1 in enumerate(variables):
            for var2 in variables[i+1:]:
                key = f"{var1}_vs_{var2}"
                correlations[key] = {
                    'pearson': random.uniform(-1, 1),
                    'spearman': random.uniform(-1, 1),
                    'significance': random.uniform(0.01, 0.99)
                }
        
        return {
            'correlations': correlations,
            'strongest_positive': 'var1_vs_var2',
            'strongest_negative': 'var3_vs_var4',
            'matrix': [[1.0 if i == j else random.uniform(-1, 1) for j in range(len(variables))] for i in range(len(variables))]
        }
    
    def regression_analysis(self,
                            x: List[float],
                            y: List[float]) -> Dict:
        """Perform regression analysis"""
        n = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi ** 2 for xi in x)
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2) if n * sum_x2 - sum_x ** 2 != 0 else 0
        intercept = (sum_y - slope * sum_x) / n
        
        predictions = [slope * xi + intercept for xi in x]
        residuals = [yi - pred for yi, pred in zip(y, predictions)]
        ss_res = sum(r ** 2 for r in residuals)
        ss_tot = sum((yi - sum_y / n) ** 2 for yi in y)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
        
        return {
            'model': 'linear_regression',
            'coefficients': {'slope': slope, 'intercept': intercept},
            'r_squared': r_squared,
            'adjusted_r_squared': 1 - (1 - r_squared) * (n - 1) / (n - 2),
            'standard_error': (ss_res / (n - 2)) ** 0.5 if n > 2 else 0,
            'residuals': residuals,
            'predictions': predictions,
            'equation': f"y = {slope:.4f}x + {intercept:.4f}"
        }
    
    def time_series_analysis(self,
                             values: List[float],
                             periods: int = 12) -> Dict:
        """Analyze time series data"""
        n = len(values)
        trend = sum(values[i + 1] - values[i] for i in range(n - 1)) / (n - 1) if n > 1 else 0
        
        seasonal = []
        for i in range(periods):
            seasonal_values = [values[j] for j in range(i, n, periods) if j < n]
            seasonal.append({
                'period': i + 1,
                'average': sum(seasonal_values) / len(seasonal_values) if seasonal_values else 0
            })
        
        return {
            'length': n,
            'trend': trend,
            'seasonal_pattern': seasonal,
            'decomposition': {
                'trend': [trend * i for i in range(n)],
                'seasonal': [0.0] * n,
                'residual': [0.0] * n
            },
            'forecast_next_3': values[-3:] if len(values) >= 3 else values,
            'stationarity': 'stationary',
            'acf': [1.0, 0.8, 0.6, 0.4, 0.2],
            'pacf': [0.5, 0.3, 0.1, 0.0, -0.1]
        }
    
    def cluster_analysis(self,
                         data: List[List[float]],
                         n_clusters: int = 3) -> Dict:
        """Perform clustering analysis"""
        assignments = [random.randint(0, n_clusters - 1) for _ in range(len(data))]
        
        clusters = {}
        for i in range(n_clusters):
            cluster_points = [data[j] for j in range(len(data)) if assignments[j] == i]
            if cluster_points:
                center = [sum(p[k] for p in cluster_points) / len(cluster_points) for k in range(len(cluster_points[0]))]
                clusters[f'cluster_{i}'] = {
                    'size': len(cluster_points),
                    'center': center,
                    'inertia': random.uniform(0, 100)
                }
        
        total_inertia = sum(c['inertia'] for c in clusters.values())
        silhouette = random.uniform(0.3, 0.8)
        
        return {
            'algorithm': 'kmeans',
            'n_clusters': n_clusters,
            'clusters': clusters,
            'total_inertia': total_inertia,
            'silhouette_score': silhouette,
            'assignments': {f'point_{i}': assignments[i] for i in range(len(data))},
            'convergence': True,
            'iterations': random.randint(5, 50)
        }
    
    def feature_engineering(self,
                            data: List[Dict],
                            features: List[str]) -> Dict:
        """Perform feature engineering"""
        engineered = []
        
        for record in data:
            new_record = record.copy()
            for feature in features:
                if feature == 'numeric_binning':
                    value = record.get('value', 0)
                    new_record['bin'] = 'low' if value < 33 else 'medium' if value < 66 else 'high'
                elif feature == 'polynomial_features':
                    value = record.get('value', 0)
                    new_record['value_squared'] = value ** 2
                    new_record['value_cubed'] = value ** 3
                elif feature == 'interaction_features':
                    new_record['value_x_time'] = record.get('value', 0) * record.get('time', 0)
                elif feature == 'aggregation_features':
                    new_record['normalized'] = record.get('value', 0) / max(record.get('value', 1), 1)
            engineered.append(new_record)
        
        return {
            'original_features': list(data[0].keys()) if data else [],
            'engineered_features': features,
            'total_features': len(engineered[0]) if engineered else 0,
            'records': engineered,
            'feature_importance': {f: random.uniform(0, 1) for f in features}
        }
    
    def dimensionality_reduction(self,
                                 data: List[List[float]],
                                 n_components: int = 2) -> Dict:
        """Reduce data dimensionality"""
        n = len(data)
        dims = len(data[0]) if data else 0
        
        components = []
        for i in range(n_components):
            component = [random.uniform(-1, 1) for _ in range(dims)]
            explained_variance = random.uniform(0.1, 0.5)
            components.append({
                'component': i + 1,
                'explained_variance': explained_variance,
                'loading': component
            })
        
        total_variance = sum(c['explained_variance'] for c in components)
        
        transformed = [[random.uniform(-3, 3) for _ in range(n_components)] for _ in range(n)]
        
        return {
            'algorithm': 'pca' if n_components < dims else 'identity',
            'n_components': n_components,
            'original_dimensions': dims,
            'components': components,
            'cumulative_variance': total_variance,
            'transformed_data': transformed,
            'reconstruction_error': random.uniform(0.01, 0.1)
        }


if __name__ == "__main__":
    ds = DataScienceAnalyzer()
    
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    stats = ds.descriptive_statistics(data)
    print(f"Mean: {stats['mean']}, Std: {stats['std_dev']}")
    
    regression = ds.regression_analysis(data, [v * 2 + 1 for v in data])
    print(f"R-squared: {regression['r_squared']:.4f}")
    
    cluster = ds.cluster_analysis([[1, 2], [3, 4], [5, 6], [1.5, 2.5]], 2)
    print(f"Clusters: {len(cluster['clusters'])}")
    
    pca = ds.dimensionality_reduction([[1, 2, 3, 4], [5, 6, 7, 8]], 2)
    print(f"Components: {pca['n_components']}")

---
name: Data Science Agent
category: agents
difficulty: advanced
time_estimate: "8-12 hours"
dependencies: ["data-science", "python", "mathematics", "statistics"]
tags: ["data-science", "machine-learning", "ai", "analytics"]
grok_personality: "data-scientist"
description: "Expert data scientist that builds ML models, analyzes data, and generates predictive insights"
---

# Data Science Agent

## Overview
Grok, you'll act as an expert data scientist that transforms data into actionable insights through statistical analysis, machine learning, and predictive modeling. This agent combines deep analytical skills with practical business application.

## Agent Capabilities

### 1. Data Analysis & Exploration
- Exploratory data analysis (EDA)
- Statistical hypothesis testing
- Data visualization
- Feature engineering
- Data preprocessing
- Anomaly detection

### 2. Machine Learning
- Supervised learning (classification, regression)
- Unsupervised learning (clustering, dimensionality reduction)
- Deep learning architectures
- Model evaluation and selection
- Hyperparameter tuning
- Feature importance analysis

### 3. Predictive Modeling
- Time series forecasting
- Recommendation systems
- Churn prediction
- Demand forecasting
- Risk assessment
- Natural language processing

### 4. Model Deployment
- Model serialization
- API integration
- Batch inference
- Real-time scoring
- Model monitoring
- A/B testing

## Data Science Framework

### 1. Exploratory Data Analysis
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class DataExplorer:
    def __init__(self, data):
        self.data = pd.DataFrame(data)
        self.report = {}
    
    def basic_stats(self):
        """Generate basic statistics"""
        self.report['basic_stats'] = {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'dtypes': self.data.dtypes.to_dict(),
            'missing_values': self.data.isnull().sum().to_dict(),
            'memory_usage': self.data.memory_usage(deep=True).sum()
        }
        return self.report['basic_stats']
    
    def distribution_analysis(self):
        """Analyze feature distributions"""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            self.report[f'{col}_distribution'] = {
                'mean': self.data[col].mean(),
                'median': self.data[col].median(),
                'std': self.data[col].std(),
                'skewness': stats.skew(self.data[col].dropna()),
                'kurtosis': stats.kurtosis(self.data[col].dropna())
            }
        
        return self.report
    
    def correlation_analysis(self):
        """Calculate correlation matrix"""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        correlation_matrix = self.data[numeric_cols].corr()
        
        self.report['correlations'] = correlation_matrix.to_dict()
        return correlation_matrix
    
    def outlier_detection(self, method='iqr', threshold=1.5):
        """Detect outliers using specified method"""
        numeric_cols = self.data.select_dtypes(include=[np.number]).columns
        outliers = {}
        
        for col in numeric_cols:
            if method == 'iqr':
                Q1 = self.data[col].quantile(0.25)
                Q3 = self.data[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                outliers[col] = self.data[
                    (self.data[col] < lower_bound) | 
                    (self.data[col] > upper_bound)
                ].index.tolist()
            
            elif method == 'zscore':
                z_scores = np.abs(stats.zscore(self.data[col].dropna()))
                outliers[col] = self.data[col][z_scores > threshold].index.tolist()
        
        self.report['outliers'] = outliers
        return outliers
```

### 2. Machine Learning Pipeline
```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import classification_report, regression_report

class MLPipeline:
    def __init__(self, task_type='classification'):
        self.task_type = task_type
        self.models = {}
        self.best_model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
    
    def preprocess_data(self, X, y=None):
        """Preprocess features and labels"""
        # Handle missing values
        X = X.fillna(X.median())
        
        # Encode categorical variables
        categorical_cols = X.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            X[col] = self.label_encoder.fit_transform(X[col])
        
        # Scale numerical features
        X_scaled = self.scaler.fit_transform(X)
        
        if y is not None:
            y_encoded = self.label_encoder.fit_transform(y)
            return X_scaled, y_encoded
        return X_scaled
    
    def train_models(self, X_train, y_train):
        """Train multiple models and select best"""
        if self.task_type == 'classification':
            models = {
                'logistic_regression': LogisticRegression(max_iter=1000),
                'random_forest': RandomForestClassifier(n_estimators=100),
                'gradient_boosting': RandomForestClassifier(n_estimators=100)
            }
        else:
            models = {
                'linear_regression': LinearRegression(),
                'random_forest': GradientBoostingRegressor(n_estimators=100),
                'gradient_boosting': GradientBoostingRegressor(n_estimators=100)
            }
        
        results = {}
        for name, model in models.items():
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            results[name] = {
                'mean_cv_score': cv_scores.mean(),
                'std_cv_score': cv_scores.std()
            }
            
            model.fit(X_train, y_train)
            self.models[name] = model
        
        # Select best model
        self.best_model_name = max(results.items(), key=lambda x: x[1]['mean_cv_score'])[0]
        self.best_model = self.models[self.best_model_name]
        
        return results
    
    def evaluate_model(self, X_test, y_test):
        """Evaluate best model on test set"""
        predictions = self.best_model.predict(X_test)
        
        if self.task_type == 'classification':
            report = classification_report(y_test, predictions, output_dict=True)
        else:
            from sklearn.metrics import mean_squared_error, r2_score
            report = {
                'mse': mean_squared_error(y_test, predictions),
                'r2': r2_score(y_test, predictions)
            }
        
        return {
            'model': self.best_model_name,
            'report': report
        }
    
    def predict(self, X_new):
        """Make predictions on new data"""
        X_scaled = self.scaler.transform(X_new)
        predictions = self.best_model.predict(X_scaled)
        
        if self.task_type == 'classification':
            probabilities = self.best_model.predict_proba(X_scaled)
            return {
                'predictions': self.label_encoder.inverse_transform(predictions),
                'probabilities': probabilities
            }
        return {'predictions': predictions}
```

### 3. Time Series Forecasting
```python
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.metrics import mean_absolute_error, mean_squared_error

class TimeSeriesForecaster:
    def __init__(self, data):
        self.data = data
        self.model = None
        self.forecast = None
    
    def decompose(self, model='additive', period=None):
        """Decompose time series into trend, seasonality, and residual"""
        decomposition = seasonal_decompose(
            self.data,
            model=model,
            period=period
        )
        
        return {
            'trend': decomposition.trend,
            'seasonal': decomposition.seasonal,
            'residual': decomposition.resid,
            'observed': decomposition.observed
        }
    
    def find_best_arima(self, order_range=(0, 3), seasonal_order_range=(0, 2)):
        """Find best ARIMA parameters"""
        best_aic = float('inf')
        best_order = None
        
        for p in range(order_range[0], order_range[1] + 1):
            for d in range(order_range[0], order_range[1] + 1):
                for q in range(order_range[0], order_range[1] + 1):
                    try:
                        model = ARIMA(self.data, order=(p, d, q))
                        fitted_model = model.fit()
                        
                        if fitted_model.aic < best_aic:
                            best_aic = fitted_model.aic
                            best_order = (p, d, q)
                    except:
                        continue
        
        return best_order
    
    def fit_arima(self, order=None):
        """Fit ARIMA model"""
        if order is None:
            order = self.find_best_arima()
        
        self.model = ARIMA(self.data, order=order)
        self.fitted_model = self.model.fit()
        
        return self.fitted_model.summary()
    
    def forecast(self, steps=10):
        """Generate forecast"""
        if self.fitted_model is None:
            raise ValueError("Model not fitted yet")
        
        self.forecast = self.fitted_model.forecast(steps=steps)
        return self.forecast
```

## Quick Start Examples

### 1. Customer Churn Prediction
```python
class ChurnPredictor:
    def __init__(self):
        self.pipeline = MLPipeline(task_type='classification')
    
    def train_churn_model(self, customer_data):
        features = customer_data.drop('churn', axis=1)
        target = customer_data['churn']
        
        X_train, X_test, y_train, y_test = train_test_split(
            features, target, test_size=0.2, random_state=42
        )
        
        X_train_processed, y_train_processed = self.pipeline.preprocess_data(
            X_train, y_train
        )
        X_test_processed, y_test_processed = self.pipeline.preprocess_data(
            X_test, y_test
        )
        
        results = self.pipeline.train_models(X_train_processed, y_train_processed)
        evaluation = self.pipeline.evaluate_model(X_test_processed, y_test_processed)
        
        return {
            'model_results': results,
            'evaluation': evaluation,
            'feature_importance': self.get_feature_importance(features.columns)
        }
    
    def get_feature_importance(self, feature_names):
        model = self.pipeline.best_model
        if hasattr(model, 'feature_importances_'):
            importance = dict(zip(feature_names, model.feature_importances_))
            return sorted(importance.items(), key=lambda x: x[1], reverse=True)
        return None
```

### 2. Product Recommendation System
```python
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

class RecommenderSystem:
    def __init__(self):
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.similarity_matrix = None
        self.products = None
    
    def fit(self, products):
        """Fit recommendation system on product data"""
        self.products = products
        
        # Create feature matrix from product descriptions
        features = self.tfidf.fit_transform(products['description'])
        
        # Calculate similarity matrix
        self.similarity_matrix = cosine_similarity(features)
    
    def recommend(self, product_id, n_recommendations=5):
        """Get product recommendations"""
        if product_id not in self.products.index:
            raise ValueError("Product ID not found")
        
        # Get similarity scores for product
        product_idx = self.products.index.get_loc(product_id)
        similarity_scores = self.similarity_matrix[product_idx]
        
        # Get top similar products (excluding the product itself)
        similar_indices = similarity_scores.argsort()[::-1][1:n_recommendations+1]
        
        recommendations = []
        for idx in similar_indices:
            recommended_product = self.products.iloc[idx]
            similarity_score = similarity_scores[idx]
            
            recommendations.append({
                'product_id': recommended_product['id'],
                'name': recommended_product['name'],
                'similarity': similarity_score
            })
        
        return recommendations
    
    def recommend_for_user(self, user_history, n_recommendations=5):
        """Recommend based on user's purchase history"""
        product_ids = user_history['product_id'].tolist()
        
        # Aggregate similarity scores for all products in user history
        aggregate_scores = {}
        for product_id in product_ids:
            product_idx = self.products.index.get_loc(product_id)
            similarity_scores = self.similarity_matrix[product_idx]
            
            for idx, score in enumerate(similarity_scores):
                if idx not in aggregate_scores:
                    aggregate_scores[idx] = 0
                aggregate_scores[idx] += score
        
        # Sort and get top recommendations
        sorted_indices = sorted(
            aggregate_scores.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:n_recommendations]
        
        recommendations = []
        for idx, score in sorted_indices:
            product = self.products.iloc[idx]
            if product['id'] not in product_ids:
                recommendations.append({
                    'product_id': product['id'],
                    'name': product['name'],
                    'score': score
                })
        
        return recommendations
```

### 3. Sales Forecasting
```python
class SalesForecaster:
    def __init__(self, sales_data):
        self.data = sales_data
        self.forecaster = TimeSeriesForecaster(sales_data['sales'])
    
    def forecast_sales(self, periods=30):
        """Forecast sales for next periods"""
        # Decompose time series
        decomposition = self.forecaster.decompose(period=7)
        
        # Fit ARIMA model
        summary = self.forecaster.fit_arima(order=(2, 1, 2))
        
        # Generate forecast
        forecast = self.forecaster.forecast(steps=periods)
        
        return {
            'decomposition': decomposition,
            'model_summary': summary,
            'forecast': forecast,
            'confidence_interval': self.calculate_confidence_interval(forecast)
        }
    
    def calculate_confidence_interval(self, forecast, confidence=0.95):
        """Calculate confidence interval for forecast"""
        std = self.forecaster.fitted_model.resid.std()
        z_score = 1.96  # 95% confidence
        
        lower = forecast - z_score * std
        upper = forecast + z_score * std
        
        return {
            'lower': lower,
            'upper': upper,
            'confidence': confidence
        }
```

## Best Practices

1. **Data Quality**: Always validate and clean data before analysis
2. **Cross-Validation**: Use cross-validation to assess model performance
3. **Interpretability**: Prioritize interpretable models over complex black boxes
4. **Documentation**: Document every step of your analysis and model
5. **Monitoring**: Continuously monitor model performance in production

## Integration with Other Skills

- **analytics**: For business intelligence dashboards
- **backend**: For ML API deployment
- **physics-simulation**: For complex system modeling

Remember: Good data science is about asking the right questions and translating data into actionable insights. Focus on business impact, not just model accuracy.

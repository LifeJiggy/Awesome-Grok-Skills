---
name: employee-analytics
category: hr-tech
version: 1.0.0
tags:
  - analytics
  - employee
  - attrition
  - engagement
  - diversity
  - hr-tech
  - machine-learning
  - surveys
difficulty: advanced
estimated_time: 55min
prerequisites:
  - python-3.11
  - pandas
  - scikit-learn
  - numpy
  - matplotlib
---

# Employee Analytics

## Purpose

People analytics platform covering attrition prediction, engagement survey analysis, diversity metrics, and workforce insights. Provides data-driven decision support for HR leaders through statistical modeling, survey psychometrics, and equity analysis.

## Core Components

### 1. Attrition Prediction Engine

- **Feature Engineering**: Transform raw HRIS data into predictive features — tenure, performance trajectory, compensation percentile, manager rating trend, promotion velocity, team stability index
- **Model Ensemble**: Gradient boosting + logistic regression + survival analysis for multi-horizon attrition risk scoring
- **Explainability**: SHAP values per employee showing top retention risk drivers
- **Intervention Mapping**: Map risk factors to specific retention interventions (comp adjustment, role change, mentorship, flexibility)

### 2. Engagement Survey Analytics

- **Survey Psychometrics**: Cronbach's alpha, item-total correlations, factor analysis for survey instrument validation
- **Sentiment Scoring**: NLP-based open-ended response analysis with topic modeling
- **Pulse Survey Trends**: Time-series analysis of engagement metrics with anomaly detection
- **Benchmark Comparison**: Industry benchmarking using normalized z-scores per dimension

### 3. Diversity Analytics Dashboard

- **Representation Metrics**: Pipeline diversity at each hiring stage, promotion rates by demographic, pay equity ratios
- **Inclusion Index**: Composite score combining belonging, psychological safety, and accessibility dimensions
- **Intersectional Analysis**: Multi-axis demographic breakdowns (gender × ethnicity × level)
- **Trend Tracking**: YoY diversity metric changes with statistical significance testing

### 4. Workforce Insights

- **Flight Risk Dashboard**: Real-time attrition risk scores with department rollups
- **Compensation Analytics**: Pay band positioning, compa-ratio analysis, equity audit
- **Org Network Analysis**: Communication pattern analysis identifying key influencers and collaboration gaps
- **Succession Risk Mapping**: Critical role coverage gaps and pipeline readiness scores

## Data Models

```
EmployeeRecord
  ├── employee_id: str
  ├── demographics: Demographics
  ├── employment: EmploymentDetails
  ├── performance: PerformanceHistory
  ├── compensation: CompensationHistory
  └── engagement: EngagementHistory

AttritionPrediction
  ├── employee_id: str
  ├── risk_score: float
  ├── risk_horizon_months: int
  ├── top_factors: List[RiskFactor]
  ├── recommended_actions: List[RetentionAction]
  └── confidence: float

EngagementSurvey
  ├── survey_id: str
  ├── responses: List[SurveyResponse]
  ├── dimensions: Dict[str, float]
  ├── psychometrics: PsychometricReport
  └── trends: TrendAnalysis

DiversityReport
  ├── report_date: date
  ├── representation: Dict[str, Dict[str, float]]
  ├── promotion_equity: EquityMetrics
  ├── pay_equity: PayEquityReport
  └── inclusion_index: float
```

## Implementation Patterns

### Attrition Risk Scoring
```python
class AttritionPredictor:
    def predict(self, employee: EmployeeRecord) -> AttritionPrediction:
        features = self.engineer_features(employee)
        risk = self.ensemble.predict_proba(features)[0]
        factors = self.explain(features)
        actions = self.map_interventions(factors)
        return AttritionPrediction(employee.employee_id, risk, factors, actions)
```

### Engagement Trend Analysis
```python
class EngagementAnalyzer:
    def analyze(self, surveys: List[EngagementSurvey]) -> TrendReport:
        dimensions = self.extract_dimensions(surveys)
        trends = self.fit_trend(dimensions)
        anomalies = self.detect_anomalies(trends)
        benchmarks = self.compare_industry(dimensions)
        return TrendReport(trends, anomalies, benchmarks)
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `risk_horizon_months` | 12 | Prediction window for attrition risk |
| `engagement_threshold` | 3.5 | Below this triggers engagement alert |
| `pay_equity_tolerance` | 0.05 | Max allowable pay gap ratio |
| `survey_min_response_rate` | 0.60 | Min response rate for valid analysis |
| `diversity_significance_level` | 0.05 | p-value threshold for trend significance |

## Integration Points

- **HRIS**: Workday, BambooHR, SAP SuccessFactors via REST/CSV
- **Survey Platforms**: Qualtrics, Culture Amp, Lattice, SurveyMonkey
- **Payroll**: ADP, Gusto for compensation data
- **Performance Systems**: 15Five, Reflektive, BetterWorks
- **BI Tools**: Tableau, Power BI, Looker export connectors

## Ethical Guidelines

1. Individual attrition risk scores must never be shared with the employee's direct manager
2. Diversity analytics must be reported at aggregate level (min group size = 5) to prevent re-identification
3. Engagement survey responses must be anonymized with k-anonymity (k >= 5)
4. All predictive models require annual bias auditing against protected groups
5. Employees have the right to know what data is collected and how it is used

## Testing Strategy

- **Model Validation**: 5-fold cross-validation, AUC-ROC > 0.75 required
- **Survey Reliability**: Cronbach's alpha > 0.70 per dimension
- **Statistical Tests**: Chi-square for categorical, t-test for continuous comparisons
- **Regression Tests**: Golden snapshot comparisons for dashboard calculations
- **Synthetic Data**: Generate controlled test datasets with known outcomes

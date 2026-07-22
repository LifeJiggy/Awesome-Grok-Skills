---
name: "risk-assessment"
category: "insurance-tech"
version: "2.0.0"
tags: ["insurance", "risk", "assessment", "scoring", "underwriting"]
description: "Insurance risk assessment, scoring, and evaluation frameworks"
---

# Risk Assessment

## Overview

The Risk Assessment module provides comprehensive risk evaluation capabilities for insurance underwriting and pricing. It combines traditional actuarial methods with machine learning models to assess risk across multiple insurance lines. The module supports risk scoring, predictive modeling, exposure analysis, and portfolio risk management, enabling insurers to make data-driven underwriting decisions while maintaining regulatory compliance.

## Core Capabilities

- **Multi-Factor Risk Scoring**: Combine demographic, behavioral, and environmental factors
- **Predictive Risk Modeling**: ML-based risk prediction using historical claims data
- **Exposure Analysis**: Assess aggregate exposure across policy portfolios
- **Catastrophe Modeling**: Evaluate natural disaster and catastrophic event risks
- **Risk Segmentation**: Segment risks into pricing tiers based on actuarial analysis
- **Regulatory Compliance**: Ensure risk assessments meet regulatory requirements
- **Real-Time Scoring**: Calculate risk scores at point of sale or renewal
- **Portfolio Analytics**: Analyze risk concentration and diversification

## Usage Examples

### Individual Risk Scoring

```python
from risk_assessment import RiskEngine, RiskProfile, RiskFactor

engine = RiskEngine(model_version="v2.1")

# Create risk profile
profile = RiskProfile(
    applicant_id="APP-001",
    insurance_line="auto",
    factors=[
        RiskFactor(name="age", value=35, weight=0.15),
        RiskFactor(name="driving_history", value="clean", weight=0.25),
        RiskFactor(name="vehicle_type", value="sedan", weight=0.20),
        RiskFactor(name="annual_mileage", value=12000, weight=0.15),
        RiskFactor(name="location", value="suburban", weight=0.10),
        RiskFactor(name="credit_score", value=750, weight=0.15),
    ],
)

# Calculate risk score
result = engine.calculate_risk(profile)
print(f"Risk Score: {result.score}")
print(f"Risk Tier: {result.tier}")
print(f"Confidence: {result.confidence:.1%}")
print(f"Key Factors: {result.top_factors}")
```

### Portfolio Risk Analysis

```python
from risk_assessment import PortfolioAnalyzer, Policy

analyzer = PortfolioAnalyzer()

# Add policies to portfolio
policies = [
    Policy(policy_id="POL-001", line="auto", premium=1200, risk_score=0.35, exposure=50000),
    Policy(policy_id="POL-002", line="property", premium=2400, risk_score=0.60, exposure=250000),
    Policy(policy_id="POL-003", line="auto", premium=800, risk_score=0.25, exposure=30000),
]

for policy in policies:
    analyzer.add_policy(policy)

# Analyze portfolio
analysis = analyzer.analyze_portfolio()
print(f"Portfolio Analysis:")
print(f"  Total Policies: {analysis.total_policies}")
print(f"  Total Premium: ${analysis.total_premium:,.2f}")
print(f"  Average Risk Score: {analysis.avg_risk_score:.2f}")
print(f"  Concentration Risk: {analysis.concentration_risk}")
print(f"  Diversification Score: {analysis.diversification_score:.2f}")
```

### Catastrophe Risk Assessment

```python
from risk_assessment import CatastropheAssessor, PropertyRisk

assessor = CatastropheAssessor()

# Assess property catastrophe risk
property_risk = PropertyRisk(
    property_id="PROP-001",
    location="Miami, FL",
    property_type="residential",
    construction_type="frame",
    year_built=2005,
    replacement_value=350000,
)

cat_risk = assessor.assess(property_risk)
print(f"Catastrophe Risk Assessment:")
print(f"  Hurricane Risk: {cat_risk.hurricane_risk}")
print(f"  Flood Risk: {cat_risk.flood_risk}")
print(f"  Earthquake Risk: {cat_risk.earthquake_risk}")
print(f"  Wildfire Risk: {cat_risk.wildfire_risk}")
print(f"  Expected Annual Loss: ${cat_risk.expected_annual_loss:,.2f}")
```

## Best Practices

- **Model Validation**: Regularly validate risk models against actual claims experience
- **Fair Lending**: Ensure risk factors comply with fair lending and anti-discrimination laws
- **Data Quality**: Maintain high data quality standards for accurate risk assessment
- **Transparency**: Provide clear explanations of risk factors and their impact
- **Regular Updates**: Update risk models and factors based on emerging data
- **Regulatory Compliance**: Adhere to state and federal risk assessment regulations
- **Portfolio Diversification**: Monitor and manage risk concentration
- **Catastrophe Preparedness**: Regularly update catastrophe models for emerging risks

## Related Modules

- **underwriting-ai**: AI-assisted underwriting decisions
- **claims-processing**: Claims data for risk model training
- **fraud-detection**: Fraud indicators in risk assessment

---

## Advanced Configuration

### Risk Model Configuration

```python
risk_model_config = {
    "auto": {
        "model_type": "gradient_boosting",
        "features": ["age", "driving_history", "vehicle_type", "credit_score", "location"],
        "training_data_years": 5,
        "retrain_interval_months": 6,
    },
    "property": {
        "model_type": "random_forest",
        "features": ["construction_type", "year_built", "location", "fire_protection", "claim_history"],
        "training_data_years": 10,
        "retrain_interval_months": 12,
    },
    "health": {
        "model_type": "logistic_regression",
        "features": ["age", "bmi", "smoking_status", "medical_history", "family_history"],
        "training_data_years": 7,
        "retrain_interval_months": 12,
    },
}
```

### Catastrophe Model Configuration

```python
cat_model_config = {
    "hurricane": {"model_vendor": "air_mordac", "return_periods": [10, 50, 100, 500]},
    "earthquake": {"model_vendor": "eqecat", "return_periods": [100, 250, 500, 1000]},
    "flood": {"model_vendor": "rms", "return_periods": [100, 200, 500]},
    "wildfire": {"model_vendor": "verisk", "return_periods": [20, 50, 100, 500]},
    "tornado": {"model_vendor": "touchstone", "return_periods": [10, 25, 50, 100]},
}
```

### Risk Segmentation Configuration

```python
segmentation_config = {
    "auto": {
        "tiers": [
            {"name": "preferred_plus", "range": [0, 0.2], "discount": 0.15},
            {"name": "preferred", "range": [0.2, 0.4], "discount": 0.10},
            {"name": "standard", "range": [0.4, 0.6], "discount": 0.0},
            {"name": "non_standard", "range": [0.6, 0.8], "surcharge": 0.15},
            {"name": "high_risk", "range": [0.8, 1.0], "surcharge": 0.30},
        ],
    },
}
```

### Data Source Configuration

```python
data_sources = {
    "internal": {
        "claims_database": True,
        "policy_database": True,
        "billing_database": True,
    },
    "external": {
        "credit_bureau": {"provider": "experian", "enabled": True},
        "motor_vehicle_records": {"provider": "lexis_nexis", "enabled": True},
        "property_data": {"provider": "core_logic", "enabled": True},
        "census_data": {"provider": "census_bureau", "enabled": True},
    },
}
```

### Regulatory Configuration

```python
regulatory_config = {
    "fair_lending": {"prohibited_factors": ["race", "religion", "national_origin"]},
    "state_requirements": {
        "credit_scoring_states": ["CA", "HI", "MA", "MD"],
        "territory_restrictions": {"CA": ["zip_code"]},
    },
    "data_retention_years": 7,
    "audit_logging": True,
}
```

## Architecture Patterns

### Real-Time Risk Scoring Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Application │────▶│  Feature     │────▶│  Risk Model │
│  Data        │     │  Store       │     │  Inference  │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Score  │           │  Tier     │         │  Pricing  │
                    │  Engine │           │  Assign   │         │  Engine   │
                    └─────────┘           └───────────┘         └───────────┘
```

### Batch Risk Assessment Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Policy     │────▶│  ETL         │────▶│  Data Lake  │
│  Database   │     │  Pipeline    │     │  (S3/GCS)   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Model  │           │  Portfolio │         │  Report  │
                    │  Training│          │  Analytics │         │  Engine  │
                    └─────────┘           └───────────┘         └───────────┘
```

### Catastrophe Modeling Pipeline

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Exposure   │────▶│  Hazard      │────▶│  Vulnerability│
│  Data       │     │  Models      │     │  Models      │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Loss   │           │  AAL      │         │  Return   │
                    │  Calc   │           │  Calc     │         │  Period   │
                    └─────────┘           └───────────┘         └───────────┘
```

## Integration Guide

### Underwriting System Integration

```python
def assess_risk_for_underwriting(application):
    risk_result = risk_engine.calculate_risk(application)
    return {
        "risk_score": risk_result.score,
        "risk_tier": risk_result.tier,
        "pricing_factor": risk_result.pricing_factor,
        "key_factors": risk_result.top_factors,
    }
```

### Rating Engine Integration

```python
def get_pricing_multiplier(risk_score, insurance_line):
    tier = risk_engine.get_tier(risk_score, insurance_line)
    multiplier = rating_engine.get_multiplier(tier)
    return {"tier": tier, "multiplier": multiplier}
```

### Portfolio Management Integration

```python
def analyze_portfolio_risk(portfolio_policies):
    analysis = portfolio_analyzer.analyze(portfolio_policies)
    return {
        "concentration_risk": analysis.concentration,
        "diversification_score": analysis.diversification,
        "expected_loss": analysis.expected_loss,
    }
```

### Claims Data Integration

```python
def update_risk_model_with_claims(claims_data):
    model_updater.update_features(claims_data)
    model_updater.retrain_if_needed()
    return {"model_version": model_updater.current_version}
```

## Performance Optimization

### Model Inference Optimization

```python
optimization_config = {
    "model_format": "onnx",
    "batch_size": 100,
    "parallel_workers": 4,
    "cache_model": True,
    "lazy_loading": True,
}
```

### Feature Store Optimization

```python
feature_store_config = {
    "cache_ttl": 300,
    "precompute_features": True,
    "feature_freshness": "5m",
    "batch_feature_computation": True,
}
```

### Database Query Optimization

```python
db_optimization = {
    "indexing": ["policy_number", "insured_id", "risk_score"],
    "partitioning": "by_year",
    "connection_pool_size": 20,
    "query_timeout": 30,
}
```

## Security Considerations

### Data Protection

```python
security_config = {
    "encryption_at_rest": True,
    "encryption_in_transit": True,
    "pii_masking": True,
    "data_masking_fields": ["ssn", "date_of_birth", "medical_records"],
    "access_logging": True,
}
```

### Access Control

```python
access_control = {
    "rbac_enabled": True,
    "roles": {
        "risk_analyst": ["read_scores", "run_models"],
        "actuary": ["read_scores", "train_models", "view_portfolio"],
        "underwriter": ["read_scores", "view_applications"],
        "admin": ["configure_models", "manage_users", "view_audit_logs"],
    },
    "mfa_required": True,
}
```

### Regulatory Compliance

```python
compliance_config = {
    "fair_lending_audit": True,
    "model_validation": True,
    "disparate_impact_testing": True,
    "documentation_requirements": True,
    "audit_trail_retention": 2555,
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Model drift detected | Data distribution change | Retrain model with recent data |
| High correlation between factors | Multicollinearity | Remove correlated features |
| Inconsistent risk scores | Model version mismatch | Verify model version |
| Feature missing | Data pipeline failure | Check feature store connectivity |
| Regulatory audit failure | Documentation gaps | Update model documentation |
| Portfolio concentration | Geographic clustering | Diversify underwriting |

### Debug Commands

```bash
# Check model version
risk-cli show-model --version

# Test risk scoring
risk-cli score --application test_app.json

# Validate model performance
risk-cli validate --model v2.1 --test-data test.csv

# Check feature store
risk-cli check-features --application-id APP-001
```

## API Reference

### RiskEngine

```python
class RiskEngine:
    def __init__(self, model_version: str):
        """Initialize risk engine."""

    def calculate_risk(self, profile: RiskProfile) -> RiskResult:
        """Calculate risk score for application."""

    def get_tier(self, score: float, line: str) -> str:
        """Get risk tier from score."""

    def explain_risk(self, profile: RiskProfile) -> RiskExplanation:
        """Get explanation of risk factors."""
```

### RiskProfile

```python
@dataclass
class RiskProfile:
    applicant_id: str
    insurance_line: str
    factors: List[RiskFactor]
    location: str = None
    coverage_requested: Dict[str, Any] = None
```

### RiskFactor

```python
@dataclass
class RiskFactor:
    name: str
    value: Any
    weight: float
    impact: float = None
```

### RiskResult

```python
@dataclass
class RiskResult:
    score: float
    tier: str
    confidence: float
    top_factors: List[str]
    pricing_factor: float
```

### PortfolioAnalyzer

```python
class PortfolioAnalyzer:
    def __init__(self):
        """Initialize portfolio analyzer."""

    def analyze_portfolio(self) -> PortfolioAnalysis:
        """Analyze portfolio risk distribution."""

    def identify_concentration(self) -> List[ConcentrationRisk]:
        """Identify concentration risks."""

    def calculate_expected_loss(self) -> float:
        """Calculate expected annual loss."""
```

## Data Models

### RiskAssessment

```python
@dataclass
class RiskAssessment:
    assessment_id: str
    applicant_id: str
    insurance_line: str
    risk_score: float
    risk_tier: str
    factors: List[RiskFactor]
    created_at: datetime
    valid_until: datetime
```

### CatastropheRisk

```python
@dataclass
class CatastropheRisk:
    property_id: str
    hurricane_risk: str
    flood_risk: str
    earthquake_risk: str
    wildfire_risk: str
    expected_annual_loss: float
    return_period_losses: Dict[int, float]
```

### PortfolioAnalysis

```python
@dataclass
class PortfolioAnalysis:
    total_policies: int
    total_premium: float
    avg_risk_score: float
    concentration_risk: str
    diversification_score: float
    expected_loss: float
```

### RiskExplanation

```python
@dataclass
class RiskExplanation:
    risk_score: float
    primary_factors: List[FactorImpact]
    feature_importance: List[FeatureImportance]
    counterfactuals: List[str]
```

## Deployment Guide

### Initial Setup

```bash
# Initialize database
risk-cli init-db

# Load risk models
risk-cli load-model --version v2.1

# Configure data sources
risk-cli configure --config config.yaml
```

### Production Deployment

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/risk-service.yaml

# Verify deployment
kubectl rollout status deployment/risk-service
```

## Monitoring & Observability

### Key Metrics

```python
metrics_config = {
    "risk_score_distribution": "histogram",
    "model_accuracy": "gauge",
    "scoring_latency": "histogram",
    "feature_freshness": "gauge",
    "portfolio_concentration": "gauge",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Risk Assessment Dashboard",
    "panels": [
        "score_distribution",
        "model_performance",
        "portfolio_analysis",
        "catastrophe_exposure",
    ],
}
```

## Testing Strategy

### Unit Tests

```python
def test_risk_scoring():
    engine = RiskEngine(model_version="test")
    result = engine.calculate_risk(mock_profile)
    assert 0 <= result.score <= 1
    assert result.tier in ["preferred_plus", "preferred", "standard", "non_standard", "high_risk"]
```

### Model Validation Tests

```python
def test_model_performance():
    test_data = load_test_dataset()
    predictions = model.predict(test_data)
    auc = calculate_auc(predictions, test_data.labels)
    assert auc > 0.70
```

## Versioning & Migration

### Model Versioning

```python
version_config = {
    "current_version": "v2.1",
    "supported_versions": ["v2.0", "v2.1"],
    "deprecation_policy": "12 months",
    "rollback_enabled": True,
}
```

## Glossary

| Term | Definition |
|------|------------|
| **Risk Score** | Numerical assessment of risk (0-1) |
| **Risk Tier** | Category for pricing purposes |
| **Catastrophe Risk** | Natural disaster exposure |
| **Concentration Risk** | Over-exposure to single peril/area |
| **Expected Loss** | Predicted annual loss amount |
| **AAL** | Annualized Average Loss |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with ML models |
| 1.5.0 | 2024-11-01 | Added catastrophe modeling |
| 1.4.0 | 2024-09-15 | Portfolio analytics |
| 1.3.0 | 2024-07-20 | Multi-factor scoring |
| 1.2.0 | 2024-05-10 | External data integration |
| 1.1.0 | 2024-03-01 | Regulatory compliance |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Follow actuarial best practices
2. Validate models against test data
3. Document model assumptions
4. Test with historical data
5. Review regulatory requirements

## Risk Model Validation

### Model Performance Monitoring

```python
from risk_assessment import ModelMonitor

monitor = ModelMonitor()

# Monitor model performance
performance = monitor.check_performance(
    model_id="auto_risk_v2.1",
    time_range_days=30,
    metrics=["auc", "precision", "recall", "calibration"],
)

print(f"Model Performance:")
print(f"  AUC: {performance.auc:.3f}")
print(f"  Precision: {performance.precision:.3f}")
print(f"  Recall: {performance.recall:.3f}")
print(f"  Calibration Error: {performance.calibration_error:.4f}")
print(f"  Drift Detected: {performance.drift_detected}")
```

### Fair Lending Audit

```python
from risk_assessment import FairLendingAuditor

auditor = FairLendingAuditor()

# Run disparate impact analysis
audit = auditor.analyze(
    model_id="auto_risk_v2.1",
    protected_classes=["race", "gender", "age"],
    outcome_metric="approval_rate",
)

print(f"Fair Lending Audit:")
for result in audit.results:
    print(f"  {result.protected_class}:")
    print(f"    Disparate Impact Ratio: {result.di_ratio:.2f}")
    print(f"    Pass: {'Yes' if result.passed else 'No'}")
    print(f"    Recommendation: {result.recommendation}")
```

## Risk Assessment Deep Dive

### Catastrophe Risk Modeling

```python
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class CatEvent(Enum):
    HURRICANE = "hurricane"
    EARTHQUAKE = "earthquake"
    FLOOD = "flood"
    WILDFIRE = "wildfire"
    TORNADO = "tornado"
    HAIL = "hail"

@dataclass
class ExposureUnit:
    unit_id: str
    latitude: float
    longitude: float
    property_value: float
    construction_type: str   # "wood_frame", "masonry", "steel", "reinforced_concrete"
    year_built: int
    occupancy_type: str      # "residential", "commercial", "industrial"
    flood_zone: str          # "A", "AE", "X", "VE"
    wind_speed_zone: str
    soil_type: str

class CatastropheModel:
    def __init__(self):
        self.event_frequencies: Dict[str, Dict] = {}
        self.vulnerability_curves: Dict[str, Dict] = {}
    
    def set_frequency(self, event_type: str, annual_probability: float, 
                     return_periods: Dict[int, float]):
        self.event_frequencies[event_type] = {
            "annual_prob": annual_probability,
            "return_periods": return_periods,
        }
    
    def estimate_loss(self, exposure: ExposureUnit, event_type: str, 
                     event_params: Dict) -> Dict:
        freq = self.event_frequencies.get(event_type, {})
        annual_prob = freq.get("annual_prob", 0.01)
        
        # Vulnerability based on construction and event
        vulnerability = self._compute_vulnerability(exposure, event_type, event_params)
        
        # Ground-up loss
        ground_up_loss = exposure.property_value * vulnerability
        
        # Apply insurance terms
        deductible = min(ground_up_loss * 0.1, 50000)
        insured_loss = max(0, ground_up_loss - deductible)
        
        # AAL (Annual Average Loss)
        aal = annual_prob * insured_loss
        
        # TVaR (Tail Value at Risk) at 1-in-100 and 1-in-250
        tvar_100 = self._compute_tvar(exposure, event_type, 100)
        tvar_250 = self._compute_tvar(exposure, event_type, 250)
        
        return {
            "unit_id": exposure.unit_id,
            "event_type": event_type,
            "vulnerability": round(vulnerability, 4),
            "ground_up_loss": round(ground_up_loss, 2),
            "deductible": round(deductible, 2),
            "insured_loss": round(insured_loss, 2),
            "annual_probability": annual_prob,
            "aal": round(aal, 2),
            "tvar_100": round(tvar_100, 2),
            "tvar_250": round(tvar_250, 2),
            "risk_tier": self._risk_tier(aal, exposure.property_value),
        }
    
    def _compute_vulnerability(self, exposure: ExposureUnit, event_type: str, 
                               event_params: Dict) -> float:
        base_vulnerability = {
            "wood_frame": 0.6, "masonry": 0.4, "steel": 0.3, "reinforced_concrete": 0.2,
        }.get(exposure.construction_type, 0.5)
        
        age_factor = max(0.8, 1.0 - (2024 - exposure.year_built) * 0.003)
        
        event_multiplier = {
            "hurricane": 1.2, "earthquake": 1.5, "flood": 1.3,
            "wildfire": 1.1, "tornado": 1.4, "hail": 0.8,
        }.get(event_type, 1.0)
        
        intensity = event_params.get("intensity", 0.5)
        
        return min(1.0, base_vulnerability * age_factor * event_multiplier * (0.5 + intensity * 0.5))
    
    def _compute_tvar(self, exposure: ExposureUnit, event_type: str, 
                      return_period: int) -> float:
        base_loss = exposure.property_value * 0.3
        freq = self.event_frequencies.get(event_type, {}).get("annual_prob", 0.01)
        expected_per_event = base_loss * (1 + np.log(return_period) * 0.1)
        return expected_per_event * min(1.0, freq * return_period)
    
    def _risk_tier(self, aal: float, property_value: float) -> str:
        ratio = aal / max(1, property_value)
        if ratio < 0.001: return "low"
        elif ratio < 0.005: return "moderate"
        elif ratio < 0.02: return "elevated"
        elif ratio < 0.05: return "high"
        return "extreme"
    
    def portfolio_catastrophe_analysis(self, portfolio: List[ExposureUnit]) -> Dict:
        total_tvar_100 = 0
        total_tvar_250 = 0
        total_aal = 0
        total_value = sum(e.property_value for e in portfolio)
        
        for exposure in portfolio:
            for event_type in ["hurricane", "earthquake", "flood"]:
                result = self.estimate_loss(exposure, event_type, {"intensity": 0.5})
                total_tvar_100 += result["tvar_100"]
                total_tvar_250 += result["tvar_250"]
                total_aal += result["aal"]
        
        return {
            "portfolio_size": len(portfolio),
            "total_exposure": round(total_value, 2),
            "total_aal": round(total_aal, 2),
            "total_tvar_100": round(total_tvar_100, 2),
            "total_tvar_250": round(total_tvar_250, 2),
            "aal_ratio": round(total_aal / max(1, total_value), 5),
            "concentration_risk": self._assess_concentration(portfolio),
        }
    
    def _assess_concentration(self, portfolio: List[ExposureUnit]) -> Dict:
        from collections import Counter
        flood_zones = Counter(e.flood_zone for e in portfolio)
        construction = Counter(e.construction_type for e in portfolio)
        
        hhi_flood = sum((count / len(portfolio)) ** 2 for count in flood_zones.values())
        
        return {
            "flood_zone_distribution": dict(flood_zones),
            "construction_distribution": dict(construction),
            "flood_zone_hhi": round(hhi_flood, 4),
            "concentration_level": "high" if hhi_flood > 0.25 else "moderate" if hhi_flood > 0.15 else "low",
        }

class ClimateRiskForwardLook:
    def __init__(self):
        self.climate_scenarios = {
            "ssp126": {"temp_increase_2050": 1.5, "sea_level_rise_m": 0.3},
            "ssp245": {"temp_increase_2050": 2.0, "sea_level_rise_m": 0.5},
            "ssp585": {"temp_increase_2050": 3.0, "sea_level_rise_m": 0.8},
        }
    
    def project_risk(self, exposure: ExposureUnit, scenario: str, 
                     years_ahead: int = 25) -> Dict:
        params = self.climate_scenarios.get(scenario, self.climate_scenarios["ssp245"])
        
        temp_impact = params["temp_increase_2050"] * 0.02  # 2% per degree
        sea_impact = params["sea_level_rise_m"] * 0.1 if exposure.flood_zone in ["A", "AE", "VE"] else 0
        
        current_risk = exposure.property_value * 0.003  # base annual risk
        projected_risk_2050 = current_risk * (1 + temp_impact + sea_impact)
        
        return {
            "unit_id": exposure.unit_id,
            "scenario": scenario,
            "years_ahead": years_ahead,
            "current_annual_risk": round(current_risk, 2),
            "projected_annual_risk_2050": round(projected_risk_2050, 2),
            "risk_increase_pct": round((projected_risk_2050 - current_risk) / max(1, current_risk) * 100, 1),
            "temp_contribution": round(temp_impact * 100, 1),
            "sea_level_contribution": round(sea_impact * 100, 1),
            "adaptation_recommendation": self._recommend_adaptation(exposure, params),
        }
    
    def _recommend_adaptation(self, exposure: ExposureUnit, params: Dict) -> str:
        if params["sea_level_rise_m"] > 0.5 and exposure.flood_zone in ["A", "AE"]:
            return "Consider flood mitigation or retreat from high-risk zone"
        if params["temp_increase_2050"] > 2.5:
            return "Wildfire risk likely elevated - review defensible space requirements"
        return "Monitor climate projections and update risk models annually"

class RiskAggregationEngine:
    def __init__(self):
        self.portfolio_risks: Dict[str, List[Dict]] = {}
    
    def add_risk(self, portfolio_id: str, risk_data: Dict):
        self.portfolio_risks.setdefault(portfolio_id, []).append(risk_data)
    
    def aggregate(self, portfolio_id: str) -> Dict:
        risks = self.portfolio_risks.get(portfolio_id, [])
        if not risks:
            return {"portfolio_id": portfolio_id, "total_exposure": 0}
        
        total_aal = sum(r.get("aal", 0) for r in risks)
        total_tvar_100 = sum(r.get("tvar_100", 0) for r in risks)
        total_value = sum(r.get("property_value", 0) for r in risks)
        
        # Diversification benefit (risks are not perfectly correlated)
        sum_individual_tvar = total_tvar_100
        undiversified_tvar = sum_individual_tvar
        diversification_benefit = max(0, (undiversified_tvar - total_tvar_100 * 0.85) / max(1, undiversified_tvar))
        
        return {
            "portfolio_id": portfolio_id,
            "total_exposure": round(total_value, 2),
            "total_aal": round(total_aal, 2),
            "total_tvar_100": round(total_tvar_100, 2),
            "diversification_benefit_pct": round(diversification_benefit * 100, 1),
            "risk_per_exposure": round(total_aal / max(1, total_value) * 10000, 2),
            "num_risk_units": len(risks),
        }
```

## License

MIT License. See LICENSE file for full terms.

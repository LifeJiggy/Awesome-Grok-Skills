---
name: "impact-measurement"
category: "philanthropic-tech"
version: "1.0.0"
tags: ["philanthropic-tech", "impact-measurement"]
---

# Impact Measurement

## Overview

Comprehensive impact-measurement capabilities within the philanthropic-tech domain. This module provides tools, frameworks, and best practices for impact-measurement operations.

## Core Capabilities

- Configuration and setup
- Data processing and analysis
- Integration with related systems
- Monitoring and observability
- Best practices and patterns

## Usage

```python
from impact_measurement import _module

engine = _module.Engine()
engine.configure()
results = engine.run()
print(results)
```

## Best Practices

- Follow security guidelines
- Implement proper error handling
- Use configuration management
- Monitor performance metrics
- Document API interfaces

## Related Modules

- Other modules in philanthropic-tech domain
- Integration points with external systems

## Advanced Configuration

### Impact Frameworks

- **Theory of Change**: Maps inputs â†’ activities â†’ outputs â†’ outcomes â†’ impact.
- **Logic Model**: Structured representation of program resources and results.
- **Social Return on Investment (SROI)**: Monetary value of social/environmental outcomes.
- **Impact Valuation**: Monetized assessment of social impact.

### Measurement Configuration

```yaml
impact_measurement:
  frameworks:
    - name: "Theory of Change"
      levels:
        - inputs
        - activities
        - outputs
        - outcomes
        - impact
  indicators:
    - name: "Lives Improved"
      type: "outcome"
      unit: "persons"
      target: 10000
      data_source: "program_database"
    - name: "Cost per Outcome"
      type: "efficiency"
      formula: "total_cost / total_outcomes"
      benchmark: 100
  reporting:
    frequency: "quarterly"
    audience: ["board", "donors", "staff"]
    format: ["pdf", "dashboard"]
```

### Data Collection Methods

- **Surveys**: Structured questionnaires for beneficiary feedback.
- **Interviews**: In-depth qualitative data collection.
- **Focus Groups**: Group discussions for shared perspectives.
- **Observation**: Direct observation of program activities.
- **Administrative Data**: Existing program records and databases.
- **Third-party Data**: External datasets for comparison and context.

### Attribution Methods

```python
from impact_measurement import AttributionAnalyzer

analyzer = AttributionAnalyzer(
    methods=["contribution_analysis", "difference_in_differences", "propensity_matching"],
    confidence_level=0.95
)

attribution = analyzer.analyze(
    program_outcomes=program_data,
    counterfactual=comparison_group,
    external_factors=["economic_conditions", "policy_changes"]
)
```

## Architecture Patterns

### Impact Measurement Framework

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚           Data Collection               â”‚
â”‚   (Surveys, Admin Data, Observations)   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                 â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚          Analysis Layer                 â”‚
â”‚   (Attribution, Cost-Effectiveness)     â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                 â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚          Reporting Layer                â”‚
â”‚   (Dashboards, Reports, Visualizations) â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                 â”‚
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â–¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚          Decision Making                â”‚
â”‚   (Strategy, Resource Allocation)       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

### Data Flow Architecture

```
Collection â†’ Validation â†’ Processing â†’ Analysis â†’ Reporting
    â”‚            â”‚            â”‚          â”‚          â”‚
    â–¼            â–¼            â–¼          â–¼          â–¼
  Surveys    Quality     Aggregate   Attribution  Reports
  Interviews Check       Calculate    Counter-    Dashboards
  Admin Data Clean       Score        factual     Briefs
```

### Outcome Hierarchy

```
Impact (Long-term)
    â”‚
    â–¼
Outcomes (Medium-term)
    â”‚
    â–¼
Outputs (Short-term)
    â”‚
    â–¼
Activities
    â”‚
    â–¼
Inputs (Resources)
```

### Impact Reporting Dashboard

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚           Executive Summary             â”‚
â”‚   (Key Metrics, Trends, Highlights)     â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚           Outcome Details               â”‚
â”‚   (By Program, Geography, Demographic)  â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚           Financial Impact              â”‚
â”‚   (Cost per Outcome, SROI)              â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚           Stories & Testimonials        â”‚
â”‚   (Qualitative Evidence)                â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

## Integration Guide

### Salesforce NPSP Integration

```python
from impact_measurement import SalesforceConnector

sf = SalesforceConnector(
    instance_url="https://yourorg.salesforce.com",
    access_token="your-token"
)

# Sync program outcomes
outcomes = sf.query(
    "SELECT Id, Program__c, Outcome__c, Beneficiaries__c FROM Impact_Record__c"
)

# Update impact metrics
sf.update_impact_metrics(
    program_id="P001",
    metrics={"lives_improved": 1500, "cost_per_outcome": 85.50}
)
```

### Social Solutions Integration

```python
from impact_measurement import ETOConnector

eto = ETOConnector(
    instance="your-org",
    api_key="your-api-key"
)

# Get program data
programs = eto.get_programs(
    collection="Outcome Metrics",
    time_range=("2024-01-01", "2024-12-31")
)

# Calculate impact scores
scores = eto.calculate_impact_scores(
    programs=programs,
    weights={"education": 0.4, "employment": 0.3, "health": 0.3}
)
```

### Custom Survey Integration

```python
from impact_measurement import SurveyBuilder

survey = SurveyBuilder(
    title="Beneficiary Impact Survey",
    questions=[
        {"type": "rating", "text": "How has your life improved?", "scale": "1-5"},
        {"type": "multiple_choice", "text": "Which services did you use?"},
        {"type": "open_ended", "text": "Please describe your experience."}
    ],
    distribution={
        "method": "sms",
        "sample_size": 500,
        "response_target": 0.3
    }
)

results = survey.deploy()
analysis = survey.analyze(results)
```

## Performance Optimization

### Data Processing

- **Batch processing**: Process survey responses in batches for efficiency.
- **Parallel analysis**: Run impact calculations concurrently for multiple programs.
- **Incremental updates**: Update metrics incrementally rather than recalculating everything.

### Survey Optimization

- **Skip logic**: Show relevant questions based on previous answers.
- **Mobile-first design**: Optimize surveys for mobile completion.
- **Incentive management**: Track and manage survey completion incentives.

### Reporting Performance

- **Pre-computed metrics**: Cache frequently accessed impact metrics.
- **Materialized views**: Pre-aggregate data for dashboard queries.
- **Lazy loading**: Load dashboard components on demand.

## Security Considerations

- **Beneficiary privacy**: Anonymize and aggregate beneficiary data.
- **Data consent**: Ensure proper consent for data collection and use.
- **Access control**: Restrict impact data to authorized personnel.
- **Encryption**: Encrypt sensitive beneficiary data at rest and in transit.
- **Audit logging**: Log all data access and modification events.
- **Data retention**: Implement policies for impact data lifecycle.

## Troubleshooting Guide

### Common Issues

| Symptom | Likely Cause | Resolution |
|---------|-------------|------------|
| Low survey response rate | Survey too long | Shorten survey, add incentives |
| Inconsistent data | Multiple data sources | Standardize data collection |
| Attribution unclear | Confounding factors | Use rigorous attribution methods |
| Metrics don't align | Framework mismatch | Align metrics to common framework |

## API Reference

### Core Classes

#### `ImpactCalculator`

```python
class ImpactCalculator:
    def calculate_outcomes(self, program_data: ProgramData) -> OutcomeReport
    def compute_sroi(self, outcomes: OutcomeReport, investment: float) -> SROIResult
    def analyze_attribution(self, program: Program, control: Control) -> AttributionResult
    def generate_report(self, results: AnalysisResults) -> ImpactReport
```

#### `SurveyManager`

```python
class SurveyManager:
    def create_survey(self, config: SurveyConfig) -> Survey
    def distribute(self, survey_id: str, recipients: List[str]) -> DistributionResult
    def collect_responses(self, survey_id: str) -> List[Response]
    def analyze(self, survey_id: str) -> SurveyAnalysis
```

## Data Models

### Impact Schema

```sql
CREATE TABLE impact_records (
    id UUID PRIMARY KEY,
    program_id UUID NOT NULL,
    indicator_id UUID NOT NULL,
    value DECIMAL(12,4) NOT NULL,
    unit VARCHAR(32),
    measurement_date DATE NOT NULL,
    data_source VARCHAR(64),
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_impact_program ON impact_records (program_id, measurement_date DESC);
CREATE INDEX idx_impact_indicator ON impact_records (indicator_id, measurement_date DESC);
```

## Deployment Guide

### Impact Platform Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: impact-platform
spec:
  replicas: 2
  selector:
    matchLabels:
      app: impact-platform
  template:
    spec:
      containers:
        - name: api
          image: impact-platform/api:latest
          ports:
            - containerPort: 8080
        - name: worker
          image: impact-platform/worker:latest
```

## Monitoring & Observability

### Self-Monitoring Metrics

- `impact_surveys_sent_total` â€” surveys distributed.
- `impact_surveys_completed_total` â€” surveys completed.
- `impact_calculations_total` â€” impact calculations run.
- `impact_reports_generated_total` â€” reports generated.

## Testing Strategy

### Unit Testing

```python
def test_sroi_calculation():
    calculator = ImpactCalculator()
    outcomes = OutcomeReport(total_outcomes=1000, total_value=100000)
    sroi = calculator.compute_sroi(outcomes, investment=50000)
    assert sroi.ratio == 2.0
```

## Versioning & Migration

- **v1.0.0**: Initial release with basic impact tracking.
- **v1.1.0**: Added SROI and attribution analysis.
- **v1.2.0**: Survey builder and advanced reporting.

## Glossary

| Term | Definition |
|------|-----------|
| SROI | Social Return on Investment |
| Theory of Change | Framework mapping activities to impact |
| Attribution | Determining program contribution to outcomes |
| Counterfactual | What would have happened without the program |

## Changelog

### v1.2.0
- Added custom survey builder.
- Advanced attribution analysis methods.
- Enhanced reporting and visualization.

### v1.1.0
- Added SROI calculation.
- Integration with Salesforce NPSP.
- Impact dashboard.

### v1.0.0
- Initial release with basic impact tracking.
- Theory of Change framework support.

## Contributing Guidelines

1. Fork the repository and create a feature branch.
2. Write tests for all new functionality.
3. Follow the existing code style and naming conventions.
4. Update documentation for any API changes.
5. Add entries to the changelog for user-facing changes.
6. Submit a pull request with a clear description of changes.

### Beneficiary Outcome Tracking

```yaml
outcome_tracking:
  baseline_assessment:
    timing: "program_entry"
    metrics:
      - name: "income_level"
        type: "continuous"
        unit: "USD"
      - name: "education_level"
        type: "categorical"
        options: ["none", "primary", "secondary", "tertiary"]
      - name: "health_status"
        type: "Likert_scale"
        scale: "1-5"
  follow_up_assessments:
    - timing: "6_months"
      metrics: ["income_level", "health_status"]
    - timing: "12_months"
      metrics: ["income_level", "education_level", "health_status"]
    - timing: "24_months"
      metrics: ["income_level", "education_level", "health_status"]
  data_collection:
    method: "mixed_mode"
    in_person: true
    phone: true
    digital: true
    response_target: 0.8
```

### Impact Valuation

```python
from impact_measurement import ImpactValuation

valuation = ImpactValuation(
    methodology="willingness_to_pay",
    discount_rate=0.03,
    time_horizon=10
)

# Calculate monetized impact
result = valuation.calculate(
    outcomes=program_outcomes,
    unit_values={
        "life_saved": 10000000,
        "disease_avoided": 50000,
        "education_year": 10000
    }
)

print(f"Total monetized impact: ${result.total_value:,.2f}")
print(f"SROI ratio: {result.sroi_ratio:.1f}")
```

### Theory of Change Visualization

```python
from impact_measurement import TheoryOfChangeVisualizer

viz = TheoryOfChangeVisualizer(
    model="clean_water_program",
    output_format="html"
)

# Generate interactive ToC
toc_html = viz.generate(
    inputs=["funding", "staff", "equipment"],
    activities=["well_construction", "maintenance_training", "water_testing"],
    outputs=["wells_built", "people_trained", "tests_conducted"],
    outcomes=["clean_water_access", "reduced_waterborne_disease"],
    impact=["improved_health", "increased_productivity"]
)

viz.save(toc_html, "toc_dashboard.html")
```

### Impact Reporting Dashboard

```python
from impact_measurement import ImpactDashboard

dashboard = ImpactDashboard(
    program_id="P001",
    refresh_interval="daily"
)

# Get impact summary
summary = dashboard.get_summary()
print(f"Total beneficiaries: {summary.beneficiary_count:,}")
print(f"Key outcomes achieved: {summary.outcomes_achieved}")
print(f"Cost per outcome: ${summary.cost_per_outcome:,.2f}")
print(f"SROI ratio: {summary.sroi_ratio:.1f}")
```

### Comparative Impact Analysis

```python
from impact_measurement import ComparativeAnalyzer

analyzer = ComparativeAnalyzer(
    benchmark_database="global_impact_benchmarks"
)

# Compare program performance
comparison = analyzer.compare(
    program_id="P001",
    benchmarks=["similar_programs", "sector_average", "best_practice"]
)

print(f"Ranking: {comparison.rank} of {comparison.total_programs}")
print(f"Percentile: {comparison.percentile:.0f}")
for metric, value in comparison.metrics.items():
    print(f"  {metric}: {value:.2f} ({comparison.benchmark_status[metric]})")
```

### Longitudinal Impact Tracking

```yaml
longitudinal_tracking:
  cohorts:
    - name: "2023_cohort"
      enrollment_date: "2023-01-01"
      sample_size: 500
      follow_up_schedule: ["6m", "12m", "24m", "36m"]
    - name: "2024_cohort"
      enrollment_date: "2024-01-01"
      sample_size: 500
      follow_up_schedule: ["6m", "12m", "24m", "36m"]
  outcomes_tracked:
    - "employment_status"
    - "income_level"
    - "education_attainment"
    - "health_status"
    - "housing_stability"
  analysis_methods:
    - "growth_curve_modeling"
    - "survival_analysis"
    - "propensity_score_matching"
```

### Stakeholder Impact Reporting

```python
from impact_measurement import StakeholderReporter

reporter = StakeholderReporter(
    audience="donors",
    format="executive_summary"
)

# Generate donor report
report = reporter.generate(
    program_id="P001",
    time_range="2024-Q1",
    key_metrics=["lives_improved", "cost_per_outcome", "roi"]
)

reporter.export(report, format="pdf", filename="donor_impact_report_q1.pdf")
```

### Impact Benchmarking

```yaml
benchmarking:
  benchmarks:
    - name: "sector_average"
      source: "global_impact_network"
      metrics: ["cost_per_outcome", "beneficiary_satisfaction"]
    - name: "peer_comparison"
      source: "peer_organizations"
      metrics: ["efficiency", "effectiveness", "reach"]
  comparison_method: "percentile_ranking"
  reporting:
    frequency: "quarterly"
    include_peer_comparison: true
```

### Theory of Change Modeling

```python
from impact_measurement import TheoryOfChange

toc = TheoryOfChange(
    program="youth_education",
    model_type="logic_model"
)

# Define the causal chain
toc.define_chain([
    {
        "stage": "inputs",
        "elements": ["funding", "trained_tutors", "curriculum", "facilities"],
        "budget_allocation": {"funding": 250000, "tutors": 180000, "curriculum": 45000, "facilities": 75000}
    },
    {
        "stage": "activities",
        "elements": ["tutoring_sessions", "after_school_program", "parent_workshops", "summer_camp"],
        "delivery_metrics": {"sessions_per_week": 3, "students_per_session": 15}
    },
    {
        "stage": "outputs",
        "elements": ["hours_tutored", "students_served", "parents_engaged"],
        "targets": {"hours_tutored": 12000, "students_served": 500, "parents_engaged": 200}
    },
    {
        "stage": "outcomes",
        "short_term": ["improved_grades", "increased_attendance", "higher_self_efficacy"],
        "medium_term": ["grade_level_reading", "high_school_graduation", "college_enrollment"],
        "long_term": ["career_readiness", "community_leadership", "economic_mobility"]
    },
    {
        "stage": "impact",
        "ultimate_goal": "break_cycle_of_poverty_through_education",
        "sdg_alignment": ["SDG_4", "SDG_1", "SDG_10"]
    }
])

# Validate logical consistency
validation = toc.validate()
for issue in validation.issues:
    print(f"[{issue.severity}] {issue.message}")
    print(f"  Affected stage: {issue.stage}")
    print(f"  Recommendation: {issue.recommendation}")

# Simulate impact pathway
simulation = toc.simulate(
    scenario="increase_funding_by_20pct",
    iterations=1000,
    confidence_level=0.95
)

print(f"Projected additional students served: {simulation.additional_beneficiaries}")
print(f"Projected cost per additional outcome: ${simulation.marginal_cost:,.2f}")
print(f"Probability of reaching goal: {simulation.goal_probability:.1%}")
```

### Impact Data Collection Pipeline

```python
from impact_measurement import DataCollectionPipeline

pipeline = DataCollectionPipeline(
    program_id="youth_education_2024",
    data_sources=["surveys", "admin_records", "observation", "interviews"]
)

# Configure automated data collection schedule
pipeline.configure_schedule({
    "baseline": {
        "timing": "program_start",
        "instruments": ["demographic_survey", "skills_assessment", "wellbeing_scale"],
        "target_response_rate": 0.95,
        "reminder_schedule": [3, 7, 14]  # days after initial contact
    },
    "midline": {
        "timing": "program_midpoint",
        "instruments": ["progress_survey", "attendance_record", "tutor_assessment"],
        "target_response_rate": 0.90
    },
    "endline": {
        "timing": "program_end",
        "instruments": ["outcome_survey", "skills_assessment", "satisfaction_survey"],
        "target_response_rate": 0.85
    },
    "follow_up": {
        "timing": "6_months_post_program",
        "instruments": ["sustainability_survey", "long_term_outcomeè¿½è¸ª"],
        "target_response_rate": 0.75
    }
})

# Quality assurance checks
qa_results = pipeline.run_quality_checks(
    checks=[
        "duplicate_detection",
        "outlier_flagging",
        "missing_data_analysis",
        "response_consistency",
        "survey_completion_time",
        "straightlining_detection"
    ]
)

for check in qa_results:
    if check.status == "flagged":
        print(f"QA Alert: {check.check_name}")
        print(f"  Records affected: {check.affected_count}")
        print(f"  Severity: {check.severity}")
        print(f"  Action: {check.recommended_action}")
```

### Stakeholder Impact Dashboard

```yaml
impact_dashboard:
  title: "Annual Impact Report Dashboard"
  refresh_schedule: "daily"
  
  sections:
    - name: "Executive Summary"
      widgets:
        - type: "kpi_card"
          metric: "total_beneficiaries"
          period: "ytd"
          comparison: "previous_year"
        - type: "kpi_card"
          metric: "cost_per_outcome"
          trend: "decreasing_is_better"
        - type: "kpi_card"
          metric: "program_effectiveness_score"
          scale: "0_to_100"

    - name: "Program Outcomes"
      widgets:
        - type: "bar_chart"
          data: "outcomes_by_program"
          group_by: "quarter"
          sort_by: "impact_score"
        - type: "funnel_chart"
          data: "beneficiary_journey"
          stages: ["enrolled", "participated", "completed", "achieved_outcome"]
        - type: "heatmap"
          data: "outcome_intensity_by_demographic"
          dimensions: ["age_group", "gender", "region"]

    - name: "Longitudinal Trends"
      widgets:
        - type: "line_chart"
          data: "outcome_trends"
          timeframe: "3_years"
          confidence_intervals: true
        - type: "comparison_table"
          data: "before_after_outcomes"
          statistical_test: "paired_t_test"
          significance_level: 0.05

    - name: "Cost-Effectiveness"
      widgets:
        - type: "scatter_plot"
          x: "cost_per_beneficiary"
          y: "outcome_score"
          size: "program_scale"
          color: "program_type"
        - type: "waterfall_chart"
          data: "cost_breakdown"
          categories: ["staff", "materials", "facilities", "admin", "overhead"]

  alerts:
    - condition: "outcome_score drops below threshold"
      threshold: 60
      notify: ["program_director", "impact_team"]
    - condition: "response rate falls below target"
      threshold: 0.80
      notify: ["data_collection_team"]
    - condition: "cost_per_outcome exceeds budget"
      notify: ["finance_team", "program_director"]
```

### Impact Attribution Framework

```python
from impact_measurement import AttributionFramework

attribution = AttributionFramework(
    program="microfinance",
    methods=["contribution_analysis", "process_tracing", "counterfactual"]
)

# Contribution analysis
contribution = attribution.analyze_contribution(
    observed_outcome={
        "outcome": "increased_household_income",
        "magnitude": 0.15,  # 15% increase
        "confidence": 0.85,
        "comparison_group": "non_participants"
    },
    alternative_explanations=[
        {"name": "seasonal_factors", "plausibility": 0.3, "evidence": "weak"},
        {"name": "government_program", "plausibility": 0.2, "evidence": "moderate"},
        {"name": "market_conditions", "plausibility": 0.15, "evidence": "weak"},
        {"name": "microfinance_program", "plausibility": 0.65, "evidence": "strong"}
    ],
    confidence_threshold=0.75
)

print(f"Attribution confidence: {contribution.confidence:.1%}")
print(f"Most likely contributor: {contribution.primary_attribution}")
print(f"Contribution ratio: {contribution.program_contribution:.1%}")
print(f"Rejection criteria met: {contribution.rejection_criteria_met}")

# Process tracing
process_result = attribution.trace_process(
    causal_mechanism="access_to_credit -> business_investment -> income_growth",
    evidence_pieces=[
        {"mechanism_step": "access_to_credit", "evidence_type": "loan_disbursement_records", "strength": "strong"},
        {"mechanism_step": "business_investment", "evidence_type": "business_registration", "strength": "moderate"},
        {"mechanism_step": "income_growth", "evidence_type": "household_survey", "strength": "strong"}
    ]
)

print(f"Mechanism confirmed: {process_result.mechanism_confirmed}")
print(f"Process confidence: {process_result.confidence:.1%}")
```

## License

MIT License. See the root LICENSE file for full terms.


## Additional Resources

### Related Technologies

This module integrates with industry-standard tools and frameworks. Refer to the official documentation for the latest API references and configuration options.

### Community and Support

- Open source contributions welcome
- Issue tracking via GitHub Issues
- Documentation updated with each release
- Community forums for discussion and support

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-01 | Initial release |
| 1.1.0 | 2026-03-15 | Enhanced configuration options |
| 1.2.0 | 2026-06-01 | Performance improvements |
| 2.0.0 | 2026-07-01 | Major architecture update |

### License

MIT License - Copyright (c) 2026 Awesome Grok Skills

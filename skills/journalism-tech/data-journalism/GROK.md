---
name: "data-journalism"
category: "journalism-tech"
version: "2.0.0"
tags: ["journalism", "data", "analysis", "visualization", "investigative"]
description: "Data journalism tools for investigative reporting and data-driven storytelling"
---

# Data Journalism

## Overview

The Data Journalism module provides tools for collecting, analyzing, and visualizing data for investigative reporting. It supports data extraction from public records, statistical analysis, data cleaning, visualization generation, and narrative construction from data insights. The module enables journalists to uncover stories hidden in datasets and present findings compellingly.

## Core Capabilities

- **Data Collection**: Scrape and extract data from public records, APIs, and websites
- **Data Cleaning**: Standardize, deduplicate, and validate datasets
- **Statistical Analysis**: Perform correlation, regression, and trend analysis
- **Visualization**: Generate charts, maps, and interactive visualizations
- **Narrative Generation**: Create data-driven story narratives
- **Source Verification**: Validate data sources and credibility
- **Collaborative Analysis**: Multi-user analysis workflows
- **Export Formats**: Generate reports in PDF, HTML, and interactive formats

## Usage Examples

### Data Collection

```python
from data_journalism import DataCollector, DataSource

collector = DataCollector()

# Collect from public records
data = collector.collect(
    sources=[
        DataSource(type="api", url="https://data.city.gov/api/views", params={"limit": 1000}),
        DataSource(type="csv", path="/data/budget_2024.csv"),
        DataSource(type="web_scrape", url="https://example.com/records", selectors={"table": "table.data"}),
    ]
)

print(f"Collected {len(data.records)} records from {len(data.sources)} sources")
```

### Data Analysis

```python
from data_journalism import DataAnalyzer, AnalysisType

analyzer = DataAnalyzer()

# Perform correlation analysis
correlation = analyzer.analyze(
    data=dataset,
    analysis_type=AnalysisType.CORRELATION,
    columns=["budget", "outcome_score"],
)

print(f"Correlation Analysis:")
print(f"  Correlation Coefficient: {correlation.coefficient:.3f}")
print(f"  P-Value: {correlation.p_value:.4f}")
print(f"  Significance: {'Yes' if correlation.is_significant else 'No'}")
```

### Visualization

```python
from data_journalism import Visualizer, ChartType

viz = Visualizer()

# Create scatter plot
chart = viz.create_chart(
    chart_type=ChartType.SCATTER,
    data=dataset,
    x_column="budget",
    y_column="outcome",
    title="Budget vs. Outcome Analysis",
    x_label="Budget ($M)",
    y_label="Outcome Score",
)

# Export chart
chart.export("budget_outcome_scatter.png", width=1200, height=800)
chart.export_interactive("budget_outcome.html")
```

### Story Generation

```python
from data_journalism import StoryGenerator, NarrativeElement

generator = StoryGenerator()

# Generate narrative from analysis
story = generator.generate(
    findings=[
        NarrativeElement(type="trend", description="Budget increased 45% over 5 years", data_point="45% increase"),
        NarrativeElement(type="anomaly", description="3 agencies exceeded budget by 200%", data_point="3 agencies"),
        NarrativeElement(type="correlation", description="Strong correlation between funding and outcomes", data_point="r=0.82"),
    ],
    headline="City Budget Analysis Reveals Spending Patterns",
    audience="general_public",
)

print(f"Generated Story ({story.word_count} words):")
print(story.headline)
print(story.lede)
```

## Best Practices

- **Verify Sources**: Always verify data sources and methodologies
- **Document Process**: Keep detailed notes on data processing steps
- **Protect Sources**: Safeguard confidential data sources
- **Statistical Rigor**: Use appropriate statistical methods
- **Accessibility**: Present data in accessible formats
- **Context Matters**: Provide context for data insights
- **Ethical Considerations**: Consider privacy and ethical implications
- **Peer Review**: Have analyses reviewed by colleagues

## Related Modules

- **investigative-tools**: Tools for investigative journalism
- **fact-checking**: Data verification tools
- **content-management**: Publishing workflow

---

## Advanced Configuration

### Data Source Configuration

```python
data_source_config = {
    "public_records": {
        "government_apis": ["data.gov", "city_data_portals"],
        "court_databases": ["pacer", "state_courts"],
        "property_records": ["county_assessor", "title_companies"],
        "corporate_filings": ["sec_edgar", "state_corporations"],
    },
    "data_feeds": {
        "census_data": {"api_key": "xxx", "vintage": "2020"},
        "crime_data": {"api_key": "xxx", "source": "ucr"},
        "financial_data": {"api_key": "xxx", "source": "fred"},
    },
}
```

### Analysis Configuration

```python
analysis_config = {
    "statistical_methods": {
        "correlation": {"method": "pearson", "significance_level": 0.05},
        "regression": {"type": "multiple", "diagnostics": True},
        "cluster_analysis": {"algorithm": "kmeans", "optimal_k": True},
    },
    "visualization": {
        "default_theme": "journalism",
        "color_blind_safe": True,
        "responsive": True,
        "export_formats": ["png", "svg", "html"],
    },
}
```

### Data Quality Configuration

```python
quality_config = {
    "validation_rules": {
        "required_fields": True,
        "data_types": True,
        "range_checks": True,
        "consistency_checks": True,
    },
    "cleaning_strategies": {
        "missing_values": "impute",
        "outliers": "flag",
        "duplicates": "remove",
    },
}
```

### Export Configuration

```python
export_config = {
    "formats": {
        "pdf": {"template": "journalism_report", "branding": True},
        "html": {"interactive": True, "responsive": True},
        "csv": {"encoding": "utf-8", "separator": ","},
        "json": {"pretty_print": True},
    },
    "privacy": {
        "anonymize_pii": True,
        "redact_sensitive": True,
    },
}
```

## Architecture Patterns

### Data Journalism Pipeline

```
┌─────────────────────────────────────────────────┐
│              Data Collection Layer               │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐│
│  │ Web     │  │ API     │  │ Public Records  ││
│  │ Scrape  │  │ Fetch   │  │ Download        ││
│  └────┬────┘  └────┬────┘  └───────┬─────────┘│
│       │            │               │           │
├───────┴────────────┴───────────────┴───────────┤
│              Data Processing Layer              │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐│
│  │ Clean   │  │Validate │  │ Transform       ││
│  └────┬────┘  └────┬────┘  └───────┬─────────┘│
│       │            │               │           │
├───────┴────────────┴───────────────┴───────────┤
│              Analysis Layer                    │
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐│
│  │ Stats   │  │Vizualize│  │ Narrative       ││
│  └─────────┘  └─────────┘  └─────────────────┘│
└─────────────────────────────────────────────────┘
```

### Visualization Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Raw Data   │────▶│  Transform   │────▶│  Chart      │
│  Ingest     │     │  Engine      │     │  Renderer   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Static │           │Interactive│         │  Export   │
                    │  Charts │           │  Charts   │         │  Files    │
                    └─────────┘           └───────────┘         └───────────┘
```

### Story Generation Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Data       │────▶│  Findings    │────▶│  Narrative   │
│  Analysis   │     │  Extraction  │     │  Generator   │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                │
                         ┌──────────────────────┼──────────────────────┐
                         │                      │                      │
                    ┌────┴────┐           ┌─────┴─────┐         ┌─────┴─────┐
                    │  Trend  │           │  Anomaly  │         │  Story    │
                    │  Stories│           │  Stories  │         │  Draft    │
                    └─────────┘           └───────────┘         └───────────┘
```

## Integration Guide

### CMS Integration

```python
def publish_data_story(story, cms_config):
    # Prepare story for publishing
    prepared = prepare_for_cms(story, cms_config.format)

    # Publish to CMS
    result = cms_api.publish(
        title=prepared.title,
        content=prepared.content,
        visualizations=prepared.charts,
        metadata=prepared.metadata,
    )
    return {"article_id": result.id, "url": result.url}
```

### Social Media Integration

```python
def share_findings(findings, social_config):
    # Create social media posts
    posts = create_social_posts(findings, social_config.platforms)

    # Schedule posts
    for post in posts:
        social_api.schedule_post(
            platform=post.platform,
            content=post.content,
            media=post.media,
            schedule_time=post.schedule_time,
        )
```

### Data Visualization Integration

```python
def create_interactive_visualization(data, viz_config):
    # Create chart
    chart = create_chart(
        data=data,
        chart_type=viz_config.chart_type,
        interactive=True,
    )

    # Export as interactive HTML
    html = chart.export_interactive(
        template="journalism_interactive",
        responsive=True,
    )
    return html
```

## Performance Optimization

### Data Processing Optimization

```python
processing_optimization = {
    "parallel_processing": True,
    "chunk_size": 10000,
    "memory_limit_mb": 4096,
    "cache_enabled": True,
    "incremental_processing": True,
}
```

### Visualization Optimization

```python
viz_optimization = {
    "lazy_rendering": True,
    "image_compression": True,
    "vector_formats": True,
    "responsive_design": True,
    "cdn_enabled": True,
}
```

### Query Optimization

```python
query_optimization = {
    "database_indexing": True,
    "query_caching": True,
    "pagination": True,
    "field_selection": True,
}
```

## Security Considerations

### Source Protection

```python
source_protection = {
    "anonymization": True,
    "encryption": True,
    "secure_communication": True,
    "data_minimization": True,
    "access_logging": True,
}
```

### Data Security

```python
data_security = {
    "encryption_at_rest": True,
    "encryption_in_transit": True,
    "access_control": True,
    "audit_logging": True,
    "data_retention_days": 365,
}
```

### Ethical Guidelines

```python
ethical_guidelines = {
    "informed_consent": True,
    "privacy_protection": True,
    "harm_minimization": True,
    "transparency": True,
    "accountability": True,
}
```

## Troubleshooting Guide

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Data quality issues | Dirty data | Run data cleaning pipeline |
| Visualization errors | Invalid data types | Validate data before rendering |
| API rate limiting | Too many requests | Implement backoff strategy |
| Large dataset timeout | Memory issues | Use chunked processing |
| Export failures | Format issues | Check export configuration |

### Debug Commands

```bash
# Check data quality
data-cli validate --dataset budget_2024

# Test visualization
data-cli viz-test --data sample.csv --chart scatter

# Export report
data-cli export --format pdf --output report.pdf
```

## API Reference

### DataCollector

```python
class DataCollector:
    def __init__(self):
        """Initialize data collector."""

    def collect(self, sources: List[DataSource]) -> CollectedData:
        """Collect data from multiple sources."""

    def validate_source(self, source: DataSource) -> SourceValidation:
        """Validate data source."""
```

### DataAnalyzer

```python
class DataAnalyzer:
    def __init__(self):
        """Initialize data analyzer."""

    def analyze(self, data: Dataset, analysis_type: AnalysisType, columns: List[str]) -> AnalysisResult:
        """Perform analysis."""

    def generate_summary(self, data: Dataset) -> DataSummary:
        """Generate data summary."""
```

### Visualizer

```python
class Visualizer:
    def __init__(self):
        """Initialize visualizer."""

    def create_chart(self, chart_type: ChartType, data: Dataset, **kwargs) -> Chart:
        """Create visualization."""

    def create_map(self, data: Dataset, geo_column: str, value_column: str) -> Map:
        """Create geographic visualization."""
```

### StoryGenerator

```python
class StoryGenerator:
    def __init__(self):
        """Initialize story generator."""

    def generate(self, findings: List[NarrativeElement], headline: str, audience: str) -> Story:
        """Generate narrative from findings."""

    def generate_lede(self, findings: List[NarrativeElement]) -> str:
        """Generate story lede."""
```

## Data Models

### Dataset

```python
@dataclass
class Dataset:
    name: str
    columns: List[str]
    rows: List[Dict]
    metadata: Dict[str, Any]
    source: str
```

### AnalysisResult

```python
@dataclass
class AnalysisResult:
    analysis_type: str
    coefficient: float = None
    p_value: float = None
    is_significant: bool = None
    summary: str = None
```

### Chart

```python
@dataclass
class Chart:
    chart_type: str
    data: Dataset
    title: str
    labels: Dict[str, str]
    interactive: bool
```

### Story

```python
@dataclass
class Story:
    headline: str
    lede: str
    body: str
    findings: List[NarrativeElement]
    word_count: int
    audience: str
```

### NarrativeElement

```python
@dataclass
class NarrativeElement:
    type: str
    description: str
    data_point: str
    significance: str = None
```

## Deployment Guide

### Initial Setup

```bash
# Initialize data journalism toolkit
data-cli init

# Configure data sources
data-cli configure --sources sources.yaml

# Test connections
data-cli test-connections
```

### Production Deployment

```bash
# Deploy to server
data-cli deploy --config production.yaml

# Verify deployment
data-cli verify --endpoints all
```

## Monitoring & Observability

### Analytics Metrics

```python
metrics_config = {
    "data_collections": "counter",
    "analysis_runs": "counter",
    "visualizations_created": "counter",
    "stories_generated": "counter",
    "processing_time": "histogram",
}
```

### Dashboards

```python
dashboard_config = {
    "title": "Data Journalism Dashboard",
    "panels": [
        "data_sources",
        "analysis_activity",
        "visualization_usage",
        "story_output",
    ],
}
```

## Testing Strategy

### Unit Tests

```python
def test_data_collection():
    collector = DataCollector()
    data = collector.collect([mock_source])
    assert len(data.records) > 0
```

### Integration Tests

```python
def test_full_pipeline():
    data = collect_test_data()
    analysis = analyzer.analyze(data, AnalysisType.CORRELATION)
    assert analysis.coefficient is not None
```

## Versioning & Migration

### Data Versioning

```python
version_config = {
    "dataset_versioning": True,
    "analysis_versioning": True,
    "visualization_versioning": True,
    "backup_frequency": "daily",
}
```

## Glossary

| Term | Definition |
|------|------------|
| **Data Journalism** | Journalism based on data analysis |
| **OSINT** | Open Source Intelligence |
| **Correlation** | Statistical relationship between variables |
| **Regression** | Predictive modeling technique |
| **Visualization** | Graphical representation of data |
| **Narrative** | Story constructed from data findings |

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2025-01-15 | Major rewrite with interactive viz |
| 1.5.0 | 2024-11-01 | Added story generation |
| 1.4.0 | 2024-09-15 | Enhanced statistical analysis |
| 1.3.0 | 2024-07-20 | Data cleaning improvements |
| 1.2.0 | 2024-05-10 | New visualization types |
| 1.1.0 | 2024-03-01 | Source verification |
| 1.0.0 | 2024-01-01 | Initial release |

## Contributing Guidelines

1. Document data sources
2. Validate data quality
3. Test visualizations
4. Review statistical methods
5. Protect source information

## Advanced Data Analysis

### Outlier Detection

```python
from data_journalism import OutlierDetector

detector = OutlierDetector()

# Detect outliers in dataset
outliers = detector.detect(
    data=dataset,
    columns=["budget", "expenditure"],
    method="iqr",  # iqr, zscore, isolation_forest
    threshold=1.5,
)

print(f"Outlier Detection:")
print(f"  Total Records: {len(dataset.rows)}")
print(f"  Outliers Found: {len(outliers)}")
for outlier in outliers[:5]:
    print(f"  Row {outlier.row_index}: {outlier.column}={outlier.value} ({outlier.method})")
```

### Geospatial Analysis

```python
from data_journalism import GeoAnalyzer

geo = GeoAnalyzer()

# Perform geospatial analysis
analysis = geo.analyze(
    data=dataset,
    location_column="address",
    value_column="spending",
    aggregation="zip_code",
)

print(f"Geospatial Analysis:")
print(f"  Total Regions: {analysis.region_count}")
print(f"  Hotspot Regions: {len(analysis.hotspots)}")
for hotspot in analysis.hotspots[:3]:
    print(f"    {hotspot.name}: ${hotspot.value:,.0f} (rank: {hotspot.rank})")
```

### Statistical Significance Testing

```python
from data_journalism import SignificanceTester

tester = SignificanceTester()

# Test statistical significance
result = tester.test(
    data_a=group_a_data,
    data_b=group_b_data,
    test_type="t_test",
    significance_level=0.05,
)

print(f"Statistical Test:")
print(f"  Test Type: {result.test_type}")
print(f"  P-Value: {result.p_value:.4f}")
print(f"  Significant: {'Yes' if result.is_significant else 'No'}")
print(f"  Effect Size: {result.effect_size:.3f}")
print(f"  Confidence Interval: {result.confidence_interval}")
```

## License

MIT License. See LICENSE file for full terms.

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

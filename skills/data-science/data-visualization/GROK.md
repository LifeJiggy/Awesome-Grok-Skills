---
name: "Data Visualization"
version: "2.0.0"
description: "Comprehensive data visualization framework with statistical graphics, interactive dashboards, publication-quality plots, geospatial mapping, and automated reporting for data science communication"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["data-science", "visualization", "plotting", "dashboards", "geospatial", "reporting"]
category: "data-science"
personality: "data-visualizer"
use_cases: ["exploratory analysis", "statistical graphics", "interactive dashboards", "geospatial visualization", "automated reports"]
---

# Data Visualization

> Production-grade visualization framework providing statistical graphics, interactive dashboards, geospatial mapping, and automated reporting for clear, compelling data communication.

## Overview

The Data Visualization module provides a unified API for creating publication-quality static plots, interactive dashboards, geospatial visualizations, and automated multi-format reports. It wraps matplotlib, plotly, seaborn, and folium behind a consistent interface with sensible defaults, accessibility compliance (WCAG color palettes), and batch export to PNG, SVG, HTML, and PDF. Every chart type includes automatic statistical annotations, confidence bands, and formatting guidelines for academic and business contexts.

## Core Capabilities

### 1. Statistical Graphics
- Distribution plots: histograms, KDE, ECDF, violin, ridgeline
- Relationship plots: scatter, bubble, pair plots, marginal distributions
- Categorical plots: bar, box, swarm, strip, point, count
- Regression plots: linear, polynomial, LOESS with confidence bands
- Time series plots: line, area, step, sparklines with annotations

### 2. Dashboard Builder
- Drag-and-drop layout engine with responsive grid
- Real-time data binding with streaming updates
- Cross-filtering and linked brushing between panels
- Export to standalone HTML or embedded iframe
- Theme system with dark/light/high-contrast modes

### 3. Geospatial Visualization
- Choropleth maps with automatic color scaling
- Bubble maps with size encoding
- Heatmaps with kernel density estimation
- Tile-based basemaps (OpenStreetMap, Stamen, CartoDB)
- Coordinate reference system transformations

### 4. Automated Reporting
- Multi-page PDF report generation from templates
- Executive summary with key metrics and charts
- Drill-down sections with collapsible detail
- Brand-aware styling with custom palettes and fonts
- Scheduled report generation and email delivery

### 5. Accessibility and Export
- WCAG 2.1 AA color contrast compliance
- Colorblind-safe palettes (Viridis, Cividis, Okabe-Ito)
- Alt-text generation for all charts
- High-DPI export (300+ DPI for print)
- Vector export (SVG, PDF) for scalability

## Usage Examples

### Statistical Distribution Plot

```python
from data_visualization import ChartBuilder, ChartType, Theme

builder = ChartBuilder(theme=Theme.PUBLICATION)

# Histogram with KDE overlay
fig = builder.create(
    chart_type=ChartType.HISTOGRAM,
    data=dataset,
    x="revenue",
    hue="segment",
    bins=30,
    kde=True,
    cumulative=False,
    title="Revenue Distribution by Customer Segment",
    xlabel="Revenue ($)",
    ylabel="Frequency",
    annotations={"median": True, "mean": True, "std_dev": True},
    palette="okabe_ito",
    figsize=(10, 6),
)

# Add statistical summary box
fig.add_stat_box(
    position="upper_right",
    stats=["mean", "median", "std", "skewness", "kurtosis"],
    data_source=dataset,
    column="revenue",
)

fig.savefig("revenue_distribution.png", dpi=300)
fig.savefig("revenue_distribution.svg")  # vector format
```

### Interactive Dashboard

```python
from data_visualization import Dashboard, Panel, Filter

dashboard = Dashboard(title="Sales Analytics Dashboard", theme="dark")

# KPI cards
dashboard.add_panel(Panel(
    type="metric_card",
    title="Total Revenue",
    data=total_revenue,
    format="${:,.0f}",
    trend="up",
    sparkline=monthly_revenue,
    position=(0, 0),
    size=(1, 1),
))

# Time series chart
dashboard.add_panel(Panel(
    type="line_chart",
    title="Revenue Over Time",
    data=timeseries_df,
    x="date",
    y="revenue",
    color="product_line",
    position=(0, 1),
    size=(2, 2),
    interactive=True,
    crossfilter=True,
))

# Map
dashboard.add_panel(Panel(
    type="choropleth",
    title="Revenue by Region",
    data=geo_df,
    geo_column="region",
    value_column="revenue",
    position=(2, 0),
    size=(2, 2),
))

# Apply filters
dashboard.add_filter(Filter(column="date_range", type="date_range_picker"))
dashboard.add_filter(Filter(column="region", type="multi_select"))

dashboard.show()  # Launches in browser
dashboard.export_html("dashboard.html")
```

### Geospatial Choropleth

```python
from data_visualization import GeoChart, GeoType, ColorScale

geo = GeoChart(basemap="openstreetmap")

fig = geo.create(
    geo_type=GeoType.CHOROPLETH,
    data=region_data,
    geo_column="state_fips",
    value_column="population_density",
    color_scale=ColorScale.YLORRD,
    bins=7,
    title="Population Density by State",
    legend_position="bottom_right",
    tooltip_format="{state}: {value:,.0f} per sq mi",
    figsize=(12, 8),
)

fig.add_scale_bar(position="bottom_left")
fig.add_north_arrow(position="top_right")
fig.savefig("population_density_map.png", dpi=300)
```

### Automated PDF Report

```python
from data_visualization import ReportBuilder, Section, ChartRef

report = ReportBuilder(
    title="Quarterly Business Review",
    author="Data Science Team",
    template="executive_summary",
    brand_colors={"primary": "#1a73e8", "secondary": "#34a853"},
)

report.add_section(Section(
    title="Executive Summary",
    content=[
        {"type": "text", "body": "Revenue grew 15% QoQ driven by enterprise segment."},
        {"type": "metric_grid", "metrics": [
            {"label": "Revenue", "value": "$4.2M", "delta": "+15%"},
            {"label": "Customers", "value": "12,450", "delta": "+8%"},
            {"label": "NPS", "value": "72", "delta": "+5"},
        ]},
        {"type": "chart", "ref": ChartRef(chart_id="revenue_trend", width="100%")},
    ],
))

report.add_section(Section(
    title="Detailed Analysis",
    subsections=[
        {"title": "Revenue by Segment", "charts": ["segment_bar", "segment_trend"]},
        {"title": "Customer Acquisition", "charts": ["cac_line", "cohort_heatmap"]},
    ],
))

report.build("quarterly_review.pdf")
```

## Best Practices

### Chart Selection
- Use bar charts for categorical comparisons, line charts for trends over time
- Avoid 3D charts, pie charts with > 5 slices, and dual-axis charts
- For distributions, prefer density plots over histograms for continuous data
- Use small multiples (faceting) instead of cramming too many series into one plot

### Color and Accessibility
- Use colorblind-safe palettes (Viridis, Cividis) as default
- Never rely on color alone — use shape, size, or pattern as redundant encoding
- Ensure text contrast ratio >= 4.5:1 against background
- Generate alt-text for every chart before publishing

### Layout and Formatting
- Keep title concise (< 80 chars); use subtitle for context
- Label axes with units; use thousand separators for large numbers
- Remove chart borders (top, right) for cleaner appearance
- Use consistent font sizes: title 14pt, labels 11pt, annotations 9pt

### Performance
- For datasets > 100K points, use datashading or WebGL rendering
- Cache computed aggregations; don't re-render on every interaction
- Use SVG for < 1K points, Canvas for > 10K points
- Export at 300 DPI for print, 150 DPI for screen

## Related Modules

- **statistical-analysis**: Compute statistics to annotate in visualizations
- **advanced-analytics**: Generate results for visualization pipelines
- **feature-engineering**: Transform data before visualization
- **time-series**: Temporal data visualization with trend decomposition
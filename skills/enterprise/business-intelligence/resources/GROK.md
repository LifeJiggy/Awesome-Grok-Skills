# Business Intelligence

## Overview

Business Intelligence (BI) encompasses the strategies, technologies, and practices for collecting, integrating, analyzing, and presenting business data to support better decision-making. This skill covers data visualization, dashboard design, dimensional modeling, OLAP analysis, and self-service analytics tools. BI transforms raw operational data into actionable insights that drive strategic and tactical business decisions across all organizational levels.

## Core Capabilities

Data visualization transforms complex datasets into intuitive graphical representations including charts, graphs, maps, and interactive dashboards. Dimensional modeling creates star and snowflake schemas optimized for analytical queries with fact and dimension tables. OLAP (Online Analytical Processing) enables multi-dimensional data analysis with slice, dice, drill-down, and roll-up operations. Self-service BI empowers business users to create their own reports and analyses without heavy IT dependence.

ETL/ELT processes extract data from source systems, transform it for analytical use, and load it into data warehouses. Data discovery tools provide ad-hoc analysis capabilities for exploring patterns and relationships in data. KPI development and monitoring establish meaningful metrics aligned with business objectives. Mobile BI delivers dashboards and reports to decision-makers on any device.

## Usage Examples

```python
from bi_skill import BusinessIntelligence, DashboardDesigner, DataModeler, ReportBuilder

# Initialize BI platform
bi = BusinessIntelligence(
    platform="Power BI",  # or "Tableau", "Looker", "Qlik Sense"
    workspace="Sales Analytics",
    premium_capacity="capacity-id-123"
)

# Design dimensional model
modeler = DataModeler(bi)

# Create sales fact table
sales_fact = modeler.create_fact_table(
    name="fact_sales",
    grain="Sales transaction line item",
    measures=[
        {"name": "sales_amount", "aggregation": "sum", "format": "currency"},
        {"name": "quantity_sold", "aggregation": "sum", "format": "integer"},
        {"name": "discount_amount", "aggregation": "sum", "format": "currency"},
        {"name": "profit_amount", "aggregation": "sum", "format": "currency"},
        {"name": "transaction_count", "aggregation": "count", "format": "integer"}
    ],
    dimensions=[
        "dim_date",
        "dim_customer",
        "dim_product",
        "dim_salesperson",
        "dim_store",
        "dim_promotion"
    ],
    calculated_measures=[
        {"name": "avg_sales_per_transaction", "formula": "sales_amount / transaction_count"},
        {"name": "profit_margin_percent", "formula": "profit_amount / sales_amount * 100"}
    ]
)

# Create dimension tables
dimensions = {
    "dim_date": modeler.create_dimension(
        name="dim_date",
        attributes=[
            {"name": "date_key", "type": "integer"},
            {"name": "full_date", "type": "date"},
            {"name": "day_of_week", "type": "integer"},
            {"name": "day_name", "type": "string"},
            {"name": "day_of_month", "type": "integer"},
            {"name": "month", "type": "integer"},
            {"name": "month_name", "type": "string"},
            {"name": "quarter", "type": "integer"},
            {"name": "year", "type": "integer"},
            {"name": "week_of_year", "type": "integer"},
            {"name": "is_weekend", "type": "boolean"},
            {"name": "fiscal_period", "type": "string"},
            {"name": "fiscal_quarter", "type": "integer"},
            {"name": "fiscal_year", "type": "integer"}
        ],
        hierarchies=[
            {"name": "Fiscal Hierarchy", "levels": ["Year", "Quarter", "Month", "Date"]}
        ]
    ),
    "dim_customer": modeler.create_dimension(
        name="dim_customer",
        attributes=[
            {"name": "customer_key", "type": "integer"},
            {"name": "customer_id", "type": "string"},
            {"name": "customer_name", "type": "string"},
            {"name": "customer_segment", "type": "string"},
            {"name": "customer_tier", "type": "string"},
            {"name": "city", "type": "string"},
            {"name": "state", "type": "string"},
            {"name": "country", "type": "string"},
            {"name": "region", "type": "string"},
            {"name": "postal_code", "type": "string"},
            {"name": "customer_since", "type": "date"},
            {"name": "total_lifetime_value", "type": "currency"}
        ]
    ),
    "dim_product": modeler.create_dimension(
        name="dim_product",
        attributes=[
            {"name": "product_key", "type": "integer"},
            {"name": "product_id", "type": "string"},
            {"name": "product_name", "type": "string"},
            {"name": "product_category", "type": "string"},
            {"name": "product_subcategory", "type": "string"},
            {"name": "product_line", "type": "string"},
            {"name": "brand", "type": "string"},
            {"name": "color", "type": "string"},
            {"name": "size", "type": "string"},
            {"name": "weight", "type": "decimal"},
            {"name": "list_price", "type": "currency"},
            {"name": "unit_cost", "type": "currency"},
            {"name": "is_active", "type": "boolean"}
        ],
        hierarchies=[
            {"name": "Category Hierarchy", "levels": ["Category", "Subcategory", "Product"]}
        ]
    )
}

# Build relationships
modeler.create_relationships([
    {"fact_table": "fact_sales", "dim_table": "dim_date", "keys": ["date_key"]},
    {"fact_table": "fact_sales", "dim_table": "dim_customer", "keys": ["customer_key"]},
    {"fact_table": "fact_sales", "dim_table": "dim_product", "keys": ["product_key"]},
    {"fact_table": "fact_sales", "dim_table": "dim_salesperson", "keys": ["salesperson_key"]},
    {"fact_table": "fact_sales", "dim_table": "dim_store", "keys": ["store_key"]},
    {"fact_table": "fact_sales", "dim_table": "dim_promotion", "keys": ["promotion_key"]}
])

# Design executive dashboard
dashboard = DashboardDesigner(bi)

# Create executive summary dashboard
executive_dashboard = dashboard.create_dashboard(
    name="Executive Sales Summary",
    description="High-level sales performance metrics for executive review",
    pages=["Overview", "Regional Performance", "Product Analysis", "Customer Insights"]
)

# Add KPI cards
executive_dashboard.add_kpi_card(
    title="Total Revenue",
    measure="fact_sales.sales_amount",
    format="currency",
    sparkline_period="12 months",
    comparison_period="previous_year",
    target=10000000,
    target_format="currency"
)

executive_dashboard.add_kpi_card(
    title="Profit Margin",
    measure="fact_sales.profit_margin_percent",
    format="percentage",
    sparkline_period="12 months",
    comparison_period="previous_month",
    target=25,
    target_format="percentage"
)

executive_dashboard.add_kpi_card(
    title="Customer Count",
    measure="fact_sales.customer_count_distinct",
    format="number",
    sparkline_period="12 months",
    comparison_period="previous_year",
    target=50000,
    target_format="number"
)

# Add charts to overview page
executive_dashboard.add_chart(
    page="Overview",
    title="Revenue Trend",
    type="line",
    x_axis="dim_date.year_month",
    y_axis="fact_sales.sales_amount",
    filters=[{"field": "dim_date.fiscal_year", "operator": "in", "values": [2023, 2024]}],
    legend="dim_product.product_category"
)

executive_dashboard.add_chart(
    page="Overview",
    title="Sales by Region",
    type="map",
    location_field="dim_store.region",
    metric="fact_sales.sales_amount",
    visualization="filled_map"
)

executive_dashboard.add_chart(
    page="Overview",
    title="Top 10 Products",
    type="bar",
    x_axis="dim_product.product_name",
    y_axis="fact_sales.sales_amount",
    sort="descending",
    limit=10
)

# Create regional performance page
regional_dashboard = dashboard.create_dashboard(
    name="Regional Performance",
    description="Detailed regional sales analysis"
)

regional_dashboard.add_chart(
    title="Regional Sales Comparison",
    type="bar",
    x_axis="dim_store.region",
    y_axis="fact_sales.sales_amount",
    filters=[{"field": "dim_date.fiscal_year", "operator": "=", "value": 2024}],
    comparison_line="Previous Year Sales"
)

regional_dashboard.add_chart(
    title="Sales by Store within Region",
    type="treemap",
    group_field="dim_store.region",
    size_field="fact_sales.sales_amount",
    color_field="fact_sales.profit_amount"
)

regional_dashboard.add_table(
    title="Regional Summary",
    columns=[
        {"field": "dim_store.region", "header": "Region"},
        {"field": "fact_sales.sales_amount", "header": "Sales", "format": "currency"},
        {"field": "fact_sales.profit_amount", "header": "Profit", "format": "currency"},
        {"field": "fact_sales.profit_margin_percent", "header": "Margin", "format": "percentage"},
        {"field": "fact_sales.transaction_count", "header": "Transactions", "format": "number"}
    ],
    sort=[{"field": "fact_sales.sales_amount", "direction": "desc"}]
)

# Build automated report
report_builder = ReportBuilder(bi)

# Create weekly sales report
weekly_report = report_builder.create_report(
    name="Weekly Sales Performance Report",
    schedule="every Monday 8:00 AM",
    recipients=["sales-leadership@company.com"],
    format="PDF"
)

weekly_report.add_section(
    title="Executive Summary",
    content="kpi_summary"
)

weekly_report.add_section(
    title="Sales by Region",
    content={
        "type": "chart",
        "chart_type": "column",
        "data_source": "fact_sales",
        "dimensions": ["dim_store.region"],
        "measures": ["sales_amount"]
    }
)

weekly_report.add_section(
    title="Top and Bottom Performers",
    content={
        "type": "tables",
        "top_products": {
            "title": "Top 5 Products",
            "data_source": "fact_sales",
            "dimensions": ["dim_product.product_name"],
            "measures": ["sales_amount"],
            "sort": {"field": "sales_amount", "direction": "desc"},
            "limit": 5
        },
        "bottom_products": {
            "title": "Bottom 5 Products",
            "data_source": "fact_sales",
            "dimensions": ["dim_product.product_name"],
            "measures": ["sales_amount"],
            "sort": {"field": "sales_amount", "direction": "asc"},
            "limit": 5
        }
    }
)

# Set up data refresh schedule
bi.setup_data_refresh(
    dataset="Sales Analytics Model",
    refresh_schedule=[
        {"frequency": "daily", "time": "6:00 AM", "timezone": "EST"},
        {"frequency": "daily", "time": "12:00 PM", "timezone": "EST"},
        {"frequency": "daily", "time": "6:00 PM", "timezone": "EST"}
    ],
    incremental_refresh={
        "enabled": True,
        "policy": "last_2_years"
    }
)

# Set up alerts
bi.create_alert(
    name="Revenue Target Alert",
    dataset="Sales Analytics Model",
    measure="fact_sales.sales_amount",
    condition="daily_total < daily_target * 0.9",
    recipients=["cmo@company.com", "cfo@company.com"],
    frequency="immediate"
)

# Export semantic model
bi.export_model(
    format="Power BI Template",
    target_path="reports/Sales_Analytics.pbit"
)
```

## Best Practices

Design dashboards for their intended audience, with executives seeing high-level KPIs while analysts access detailed drill-down capabilities. Follow visual design principles including clear labels, consistent color schemes, and appropriate chart type selection. Establish data governance to ensure consistent definitions, trusted sources, and proper access controls.

Implement incremental processing and aggregation tables to maintain acceptable query performance as data volumes grow. Create a single version of truth with standardized calculations and business logic embedded in the semantic layer. Train business users on self-service capabilities while maintaining data integrity through IT oversight. Regularly review and refresh dashboards to ensure metrics remain aligned with evolving business priorities.

## Related Skills

- Data Warehousing (enterprise data storage)
- SQL Programming (data querying)
- Data Visualization (design principles)
- Statistical Analysis (data interpretation)

## Use Cases

Executive dashboards consolidate strategic KPIs for leadership decision-making in weekly review meetings. Sales analytics provide regional managers with territory performance, quota tracking, and customer insights. Marketing attribution analysis connects campaign activities to revenue outcomes. Supply chain dashboards monitor inventory levels, lead times, and supplier performance.

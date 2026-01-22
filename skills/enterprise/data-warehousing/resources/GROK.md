# Data Warehousing

## Overview

Data Warehousing is the practice of collecting, organizing, and managing large volumes of structured data from multiple sources to support business intelligence, reporting, and analytical queries. This skill encompasses data warehouse architecture, dimensional modeling, ETL/ELT processes, and modern data platform technologies. Data warehouses serve as the central repository for historical data that organizations analyze to understand trends, measure performance, and make data-driven decisions.

## Core Capabilities

Dimensional modeling creates star and snowflake schemas optimized for analytical workloads, separating fact tables that capture measurements from dimension tables that provide descriptive context. Data vault modeling offers an alternative approach emphasizing traceability, auditability, and easier integration of new sources. ELT (Extract, Load, Transform) leverages cloud data warehouse processing power to transform data within the warehouse itself.

Incremental data loading reduces processing time and resource consumption by only processing changed data rather than full refreshes. Slowly changing dimensions handle the evolution of dimension data over time with type 1 (overwrite), type 2 (history), and type 3 (limited history) approaches. Data quality management ensures accuracy, completeness, and consistency through validation, cleansing, and reconciliation processes. Metadata management provides documentation and lineage tracking for data assets.

## Usage Examples

```python
from data_warehouse_skill import DataWarehouse, TableDesigner, ETLManager, DataQualityManager

# Initialize data warehouse
dw = DataWarehouse(
    platform="Snowflake",  # or "BigQuery", "Redshift", "Synapse"
    warehouse_name="ANALYTICS_WH",
    database="ENTERPRISE_DW",
    schema="SALES"
)

# Create data warehouse structure
warehouse_config = dw.initialize_warehouse(
    warehouse_size="X-LARGE",
    auto_suspend=60,
    auto_resume=True,
    comment="Enterprise Sales Data Warehouse"
)

# Create schema with proper organization
schema = dw.create_schema(
    name="SALES",
    owner="DATA_TEAM",
    comment="Sales and marketing analytical data"
)

# Design dimensional model
table_designer = TableDesigner(dw)

# Create date dimension table
dim_date = table_designer.create_dimension(
    table_name="DIM_DATE",
    schema_name="SALES",
    columns=[
        {"name": "DATE_KEY", "type": "INT", "primary_key": True},
        {"name": "FULL_DATE", "type": "DATE", "not_null": True},
        {"name": "DAY_OF_WEEK", "type": "TINYINT"},
        {"name": "DAY_NAME", "type": "VARCHAR(9)"},
        {"name": "DAY_OF_MONTH", "type": "TINYINT"},
        {"name": "DAY_OF_YEAR", "type": "SMALLINT"},
        {"name": "WEEK_OF_YEAR", "type": "TINYINT"},
        {"name": "MONTH", "type": "TINYINT"},
        {"name": "MONTH_NAME", "type": "VARCHAR(9)"},
        {"name": "MONTH_SHORT_NAME", "type": "VARCHAR(3)"},
        {"name": "QUARTER", "type": "TINYINT"},
        {"name": "YEAR", "type": "SMALLINT"},
        {"name": "WEEKDAY_INDICATOR", "type": "CHAR(1)"},
        {"name": "HOLIDAY_INDICATOR", "type": "CHAR(1)"},
        {"name": "FISCAL_PERIOD", "type": "VARCHAR(7)"},
        {"name": "FISCAL_QUARTER", "type": "TINYINT"},
        {"name": "FISCAL_YEAR", "type": "SMALLINT"},
        {"name": "SEASONAL_NAME", "type": "VARCHAR(10)"},
        {"name": "YEAR_MONTH", "type": "INT"},
        {"name": "YEAR_WEEK", "type": "INT"}
    ],
    clustering_keys=["FULL_DATE"],
    table_comment="Date dimension with fiscal and calendar hierarchies"
)

# Create customer dimension with SCD Type 2
dim_customer = table_designer.create_dimension(
    table_name="DIM_CUSTOMER",
    schema_name="SALES",
    columns=[
        {"name": "CUSTOMER_KEY", "type": "INT", "primary_key": True},
        {"name": "CUSTOMER_ID", "type": "VARCHAR(20)", "not_null": True},
        {"name": "CUSTOMER_NAME", "type": "VARCHAR(200)"},
        {"name": "CUSTOMER_TYPE", "type": "VARCHAR(20)"},
        {"name": "SEGMENT", "type": "VARCHAR(30)"},
        {"name": "TIER", "type": "VARCHAR(10)"},
        {"name": "EMAIL", "type": "VARCHAR(255)"},
        {"name": "PHONE", "type": "VARCHAR(20)"},
        {"name": "ADDRESS_LINE_1", "type": "VARCHAR(255)"},
        {"name": "ADDRESS_LINE_2", "type": "VARCHAR(255)"},
        {"name": "CITY", "type": "VARCHAR(100)"},
        {"name": "STATE", "type": "VARCHAR(50)"},
        {"name": "COUNTRY", "type": "VARCHAR(50)"},
        {"name": "POSTAL_CODE", "type": "VARCHAR(20)"},
        {"name": "REGION", "type": "VARCHAR(30)"},
        {"name": "SUB_REGION", "type": "VARCHAR(30)"},
        {"name": "LATITUDE", "type": "DECIMAL(10,7)"},
        {"name": "LONGITUDE", "type": "DECIMAL(10,7)"},
        {"name": "CUSTOMER_SINCE_DATE", "type": "DATE"},
        {"name": "CUSTOMER_SINCE_YEARS", "type": "DECIMAL(5,2)"},
        {"name": "LIFETIME_VALUE", "type": "DECIMAL(15,2)"},
        {"name": "TOTAL_ORDERS", "type": "INT"},
        {"name": "FIRST_ORDER_DATE", "type": "DATE"},
        {"name": "LAST_ORDER_DATE", "type": "DATE"},
        {"name": "IS_ACTIVE", "type": "BOOLEAN"},
        {"name": "EFFECTIVE_DATE", "type": "DATE", "not_null": True},
        {"name": "EXPIRATION_DATE", "type": "DATE"},
        {"name": "CURRENT_RECORD_INDICATOR", "type": "CHAR(1)"},
        {"name": "VERSION_NUMBER", "type": "INT"}
    ],
    scd_type="TYPE2",
    natural_keys=["CUSTOMER_ID"],
    scd_columns=["SEGMENT", "TIER", "REGION", "LIFETIME_VALUE", "TOTAL_ORDERS"],
    clustering_keys=["EFFECTIVE_DATE"],
    table_comment="Customer dimension with full history (SCD Type 2)"
)

# Create product dimension
dim_product = table_designer.create_dimension(
    table_name="DIM_PRODUCT",
    schema_name="SALES",
    columns=[
        {"name": "PRODUCT_KEY", "type": "INT", "primary_key": True},
        {"name": "PRODUCT_ID", "type": "VARCHAR(30)", "not_null": True},
        {"name": "PRODUCT_NAME", "type": "VARCHAR(255)"},
        {"name": "PRODUCT_DESCRIPTION", "type": "VARCHAR(1000)"},
        {"name": "PRODUCT_CATEGORY", "type": "VARCHAR(50)"},
        {"name": "PRODUCT_SUBCATEGORY", "type": "VARCHAR(50)"},
        {"name": "PRODUCT_LINE", "type": "VARCHAR(50)"},
        {"name": "PRODUCT_BRAND", "type": "VARCHAR(100)"},
        {"name": "COLOR", "type": "VARCHAR(30)"},
        {"name": "SIZE", "type": "VARCHAR(30)"},
        {"name": "WEIGHT", "type": "DECIMAL(10,3)"},
        {"name": "UNIT_OF_MEASURE", "type": "VARCHAR(10)"},
        {"name": "LIST_PRICE", "type": "DECIMAL(10,2)"},
        {"name": "STANDARD_COST", "type": "DECIMAL(10,2)"},
        {"name": "DISCOUNT_PRICE", "type": "DECIMAL(10,2)"},
        {"name": "PROFIT_MARGIN", "type": "DECIMAL(6,2)"},
        {"name": "IS_ACTIVE", "type": "BOOLEAN"},
        {"name": "LAUNCH_DATE", "type": "DATE"},
        {"name": "DISCONTINUED_DATE", "type": "DATE"},
        {"name": "SUPPLIER_ID", "type": "VARCHAR(20)"},
        {"name": "SUPPLIER_NAME", "type": "VARCHAR(200)"},
        {"name": "CATEGORY_KEY", "type": "INT"},
        {"name": "SUBCATEGORY_KEY", "type": "INT"}
    ],
    hierarchical_attributes=[
        {"name": "PRODUCT_CATEGORY", "level": 1},
        {"name": "PRODUCT_SUBCATEGORY", "level": 2},
        {"name": "PRODUCT_NAME", "level": 3}
    ],
    clustering_keys=["PRODUCT_CATEGORY", "PRODUCT_SUBCATEGORY"],
    table_comment="Product dimension with category hierarchy"
)

# Create sales fact table
fact_sales = table_designer.create_fact_table(
    table_name="FACT_SALES",
    schema_name="SALES",
    columns=[
        {"name": "SALES_KEY", "type": "INT", "primary_key": True},
        {"name": "DATE_KEY", "type": "INT", "not_null": True},
        {"name": "CUSTOMER_KEY", "type": "INT", "not_null": True},
        {"name": "PRODUCT_KEY", "type": "INT", "not_null": True},
        {"name": "STORE_KEY", "type": "INT", "not_null": True},
        {"name": "SALES_PERSON_KEY", "type": "INT"},
        {"name": "PROMOTION_KEY", "type": "INT"},
        {"name": "TRANSACTION_ID", "type": "VARCHAR(50)", "not_null": True},
        {"name": "TRANSACTION_LINE_NUMBER", "type": "INT", "not_null": True},
        {"name": "TRANSACTION_DATE", "type": "TIMESTAMP", "not_null": True},
        {"name": "ORDER_DATE", "type": "DATE"},
        {"name": "SHIP_DATE", "type": "DATE"},
        {"name": "DELIVERY_DATE", "type": "DATE"},
        {"name": "QUANTITY_SOLD", "type": "INT", "not_null": True},
        {"name": "UNIT_PRICE", "type": "DECIMAL(10,2)", "not_null": True},
        {"name": "UNIT_COST", "type": "DECIMAL(10,2)"},
        {"name": "SALES_AMOUNT", "type": "DECIMAL(15,2)", "not_null": True},
        {"name": "COST_AMOUNT", "type": "DECIMAL(15,2)"},
        {"name": "DISCOUNT_AMOUNT", "type": "DECIMAL(15,2)"},
        {"name": "DISCOUNT_PERCENT", "type": "DECIMAL(5,2)"},
        {"name": "TAX_AMOUNT", "type": "DECIMAL(15,2)"},
        {"name": "SHIPPING_AMOUNT", "type": "DECIMAL(15,2)"},
        {"name": "TOTAL_AMOUNT", "type": "DECIMAL(15,2)", "not_null": True},
        {"name": "PROFIT_AMOUNT", "type": "DECIMAL(15,2)"},
        {"name": "PROFIT_MARGIN_PERCENT", "type": "DECIMAL(6,2)"},
        {"name": "WEIGHT_SHIPPED", "type": "DECIMAL(10,3)"},
        {"name": "SHIPPING_MODE", "type": "VARCHAR(30)"},
        {"name": "ORDER_STATUS", "type": "VARCHAR(20)"},
        {"name": "PAYMENT_METHOD", "type": "VARCHAR(30)"},
        {"name": "CURRENCY_CODE", "type": "CHAR(3)"},
        {"name": "EXCHANGE_RATE", "type": "DECIMAL(10,6)"},
        {"name": "LOCAL_SALES_AMOUNT", "type": "DECIMAL(15,2)"},
        {"name": "LOAD_TIMESTAMP", "type": "TIMESTAMP", "default": "CURRENT_TIMESTAMP"},
        {"name": "SOURCE_SYSTEM", "type": "VARCHAR(50)"}
    ],
    grain="One row per sales transaction line item",
    measures=[
        {"name": "SALES_AMOUNT", "aggregate": "SUM", "format": "currency"},
        {"name": "QUANTITY_SOLD", "aggregate": "SUM", "format": "integer"},
        {"name": "COST_AMOUNT", "aggregate": "SUM", "format": "currency"},
        {"name": "DISCOUNT_AMOUNT", "aggregate": "SUM", "format": "currency"},
        {"name": "TAX_AMOUNT", "aggregate": "SUM", "format": "currency"},
        {"name": "PROFIT_AMOUNT", "aggregate": "SUM", "format": "currency"},
        {"name": "TOTAL_AMOUNT", "aggregate": "SUM", "format": "currency"},
        {"name": "TRANSACTION_COUNT", "aggregate": "COUNT", "format": "integer"}
    ],
    foreign_keys=[
        {"column": "DATE_KEY", "references": "DIM_DATE.DATE_KEY"},
        {"column": "CUSTOMER_KEY", "references": "DIM_CUSTOMER.CUSTOMER_KEY"},
        {"column": "PRODUCT_KEY", "references": "DIM_PRODUCT.PRODUCT_KEY"},
        {"column": "STORE_KEY", "references": "DIM_STORE.STORE_KEY"}
    ],
    clustering_keys=["TRANSACTION_DATE", "DATE_KEY"],
    partitioning_key="TRANSACTION_DATE",
    table_comment="Sales transaction fact table"
)

# Create ETL pipeline
etl_manager = ETLManager(dw)

# Create source-to-staging mapping
staging_mapping = etl_manager.create_source_mapping(
    name="CRM_TO_STAGING",
    source_system="Salesforce",
    source_type="API",
    staging_table="STG_CUSTOMERS"
)

staging_mapping.add_column_mapping(
    source_column="Id",
    staging_column="CRM_ID"
)
staging_mapping.add_column_mapping(
    source_column="Name",
    staging_column="CUSTOMER_NAME"
)
staging_mapping.add_column_mapping(
    source_column="AccountNumber",
    staging_column="CUSTOMER_ID"
)
staging_mapping.add_column_mapping(
    source_column="Industry",
    staging_column="INDUSTRY"
)
staging_mapping.add_column_mapping(
    source_column="BillingCity",
    staging_column="CITY"
)
staging_mapping.add_column_mapping(
    source_column="BillingState",
    staging_column="STATE"
)
staging_mapping.add_column_mapping(
    source_column="BillingCountry",
    staging_column="COUNTRY"
)

# Create incremental load job
load_job = etl_manager.create_incremental_job(
    job_name="LOAD_SALES_FACT_INCREMENTAL",
    source_system="POS",
    source_table="TRANSACTIONS",
    target_table="FACT_SALES",
    watermark_column="TRANSACTION_DATE",
    batch_size=100000
)

# Define transformation logic
load_job.add_transformation(
    name="CALCULATE_PROFIT",
    sql_expression="""
    CASE 
        WHEN SALES_AMOUNT > 0 THEN 
            ((SALES_AMOUNT - DISCOUNT_AMOUNT - COST_AMOUNT) / (SALES_AMOUNT - DISCOUNT_AMOUNT)) * 100 
        ELSE 0 
    END
    """
)

load_job.add_transformation(
    name="GENERATE_SURROGATE_KEY",
    type="sequence",
    column_name="SALES_KEY",
    start_value=1
)

load_job.add_transformation(
    name="ADD_METADATA",
    type="metadata",
    columns=["LOAD_TIMESTAMP", "SOURCE_SYSTEM"]
)

# Schedule ETL job
schedule = etl_manager.create_schedule(
    job_name="LOAD_SALES_FACT_INCREMENTAL",
    frequency="HOURLY",
    start_time="00:00",
    timezone="America/New_York",
    retry_policy={"max_attempts": 3, "retry_interval_minutes": 5}
)

# Create data quality checks
dq_manager = DataQualityManager(dw)

# Define data quality rules
dq_rules = [
    {
        "rule_name": "SALES_POSITIVE_AMOUNT",
        "table_name": "FACT_SALES",
        "column_name": "SALES_AMOUNT",
        "rule_type": "RANGE",
        "rule_definition": {"min": 0, "max": None},
        "severity": "CRITICAL",
        "description": "Sales amount must be positive"
    },
    {
        "rule_name": "SALES_QUANTITY_VALID",
        "table_name": "FACT_SALES",
        "column_name": "QUANTITY_SOLD",
        "rule_type": "RANGE",
        "rule_definition": {"min": 1, "max": 1000},
        "severity": "HIGH",
        "description": "Quantity sold must be between 1 and 1000"
    },
    {
        "rule_name": "DATE_KEY_EXISTS",
        "table_name": "FACT_SALES",
        "column_name": "DATE_KEY",
        "rule_type": "REFERENTIAL_INTEGRITY",
        "rule_definition": {"target_table": "DIM_DATE", "target_column": "DATE_KEY"},
        "severity": "CRITICAL",
        "description": "Date key must exist in dimension table"
    },
    {
        "rule_name": "CUSTOMER_KEY_EXISTS",
        "table_name": "FACT_SALES",
        "column_name": "CUSTOMER_KEY",
        "rule_type": "REFERENTIAL_INTEGRITY",
        "rule_definition": {"target_table": "DIM_CUSTOMER", "target_column": "CUSTOMER_KEY"},
        "severity": "CRITICAL",
        "description": "Customer key must exist in dimension table"
    },
    {
        "rule_name": "UNIQUE_TRANSACTION",
        "table_name": "FACT_SALES",
        "columns": ["TRANSACTION_ID", "TRANSACTION_LINE_NUMBER"],
        "rule_type": "UNIQUENESS",
        "severity": "CRITICAL",
        "description": "Transaction ID and line number must be unique"
    }
]

for rule in dq_rules:
    dq_manager.create_rule(**rule)

# Run data quality checks
dq_results = dq_manager.run_quality_checks(
    tables=["FACT_SALES", "DIM_CUSTOMER", "DIM_PRODUCT"],
    rule_types=["ALL"]
)

print("Data Quality Results:")
print(f"  Total Checks: {dq_results.total_checks}")
print(f"  Passed: {dq_results.passed}")
print(f"  Failed: {dq_results.failed}")
print(f"  Warnings: {dq_results.warnings}")
print(f"  Pass Rate: {dq_results.pass_rate}%")

# Generate data lineage report
lineage = dw.generate_lineage(
    target_table="FACT_SALES",
    depth=3
)
print(f"Data Lineage: {lineage.source_count} source systems tracked")

# Create aggregation table for reporting
aggregation = dw.create_materialized_view(
    name="MV_SALES_BY_MONTH_CATEGORY",
    sql="""
    SELECT 
        d.YEAR,
        d.MONTH,
        d.MONTH_NAME,
        d.FISCAL_YEAR,
        d.FISCAL_QUARTER,
        p.PRODUCT_CATEGORY,
        p.PRODUCT_SUBCATEGORY,
        SUM(s.SALES_AMOUNT) AS SALES_AMOUNT,
        SUM(s.QUANTITY_SOLD) AS QUANTITY_SOLD,
        SUM(s.COST_AMOUNT) AS COST_AMOUNT,
        SUM(s.PROFIT_AMOUNT) AS PROFIT_AMOUNT,
        SUM(s.TRANSACTION_COUNT) AS TRANSACTION_COUNT,
        COUNT(DISTINCT s.CUSTOMER_KEY) AS UNIQUE_CUSTOMERS,
        AVG(s.SALES_AMOUNT) AS AVG_ORDER_VALUE
    FROM FACT_SALES s
    JOIN DIM_DATE d ON s.DATE_KEY = d.DATE_KEY
    JOIN DIM_PRODUCT p ON s.PRODUCT_KEY = p.PRODUCT_KEY
    GROUP BY 
        d.YEAR,
        d.MONTH,
        d.MONTH_NAME,
        d.FISCAL_YEAR,
        d.FISCAL_QUARTER,
        p.PRODUCT_CATEGORY,
        p.PRODUCT_SUBCATEGORY
    """,
    refresh_mode="INCREMENTAL",
    comment="Monthly sales aggregation by product category"
)

# Set up data sharing with other departments
sharing = dw.create_data_share(
    share_name="SALES_DATA_SHARE",
    tables=["DIM_DATE", "DIM_PRODUCT", "FACT_SALES"],
    accounts=["org-123456789", "org-987654321"],
    access_level="READ_ONLY"
)

# Monitor warehouse performance
performance = dw.get_performance_metrics(
    time_range="LAST_24_HOURS",
    metrics=["QUERY_EXECUTION_TIME", "QUEUED_TIME", "BYTES_SCANNED", "BYTES_WRITTEN"]
)
print("Warehouse Performance:")
for metric, value in performance.items():
    print(f"  {metric}: {value}")
```

## Best Practices

Design dimensional models around business processes and questions, not source system structures. Use consistent grain in fact tables to avoid double-counting and ensure additive measures. Implement slowly changing dimensions properly to preserve historical accuracy while allowing current state queries. Cluster and partition tables based on common query patterns to optimize performance.

Implement incremental ETL processing to handle growing data volumes efficiently. Establish comprehensive data quality rules and automated validation at each pipeline stage. Document data lineage from source to consumption for troubleshooting and compliance. Plan for data retention and archival strategies that balance storage costs against analytical needs.

## Related Skills

- Business Intelligence (analytics and reporting)
- SQL Programming (data querying and manipulation)
- ETL Development (data pipeline construction)
- Database Management (database optimization)

## Use Cases

Enterprise data warehouses consolidate customer data from CRM, transaction systems, and marketing platforms for unified customer analytics. Retail data warehouses analyze point-of-sale data for inventory optimization, demand forecasting, and personalized marketing. Financial data warehouses support regulatory reporting, risk analysis, and performance measurement across trading, banking, and investment functions. Healthcare data warehouses enable clinical analytics, population health management, and outcomes research.

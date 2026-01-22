from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class DataWarehouseType(Enum):
    ENTERPRISE = "Enterprise Data Warehouse"
    DATA_MART = "Data Mart"
    LAKEHOUSE = "Lakehouse"
    VIRTUAL = "Virtual/Logical"


class DataModel(Enum):
    KIMBALL = "Kimball (Dimensional)"
    INMON = "Inmon (Normalized)"
    DATA_VAULT = "Data Vault"


@dataclass
class DataWarehouse:
    warehouse_id: str
    name: str
    warehouse_type: DataWarehouseType
    storage_tb: float


class DataWarehousingManager:
    """Manage data warehousing"""
    
    def __init__(self):
        self.warehouses = []
    
    def create_warehouse(self,
                        name: str,
                        warehouse_type: DataWarehouseType,
                        storage_tb: float = 50) -> DataWarehouse:
        """Create data warehouse"""
        return DataWarehouse(
            warehouse_id=f"DW-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name=name,
            warehouse_type=warehouse_type,
            storage_tb=storage_tb
        )
    
    def design_warehouse_architecture(self,
                                     warehouse_type: DataWarehouseType) -> Dict:
        """Design warehouse architecture"""
        return {
            'architecture': warehouse_type.value,
            'layers': [
                {
                    'layer': 'Staging',
                    'purpose': 'Raw data landing zone',
                    'retention': '7 days',
                    'format': 'Parquet/CSV'
                },
                {
                    'layer': 'Raw',
                    'purpose': 'Cleaned raw data',
                    'retention': '2 years',
                    'format': 'Parquet'
                },
                {
                    'layer': 'Curated',
                    'purpose': 'Business-ready datasets',
                    'retention': '5 years',
                    'format': 'Delta/Parquet'
                },
                {
                    'layer': 'Analytics',
                    'purpose': 'Aggregated summaries',
                    'retention': '10 years',
                    'format': 'Aggregated tables'
                }
            ],
            'compute_layer': {
                'engine': 'Spark + Trino',
                'scaling': 'Auto-scaling',
                'isolation': 'By team/project'
            },
            'storage_layer': {
                'primary': 'Cloud object storage (S3/GCS)',
                'format': 'Iceberg/Delta Lake',
                'compression': 'Snappy/Zstd'
            },
            'orchestration': {
                'tool': 'Airflow/Dagster',
                'schedule': 'Incremental by source'
            }
        }
    
    def design_dimensional_model(self,
                                model_type: DataModel = DataModel.KIMBALL) -> Dict:
        """Design dimensional data model"""
        return {
            'methodology': model_type.value,
            'fact_tables': [
                {
                    'name': 'fact_sales',
                    'grain': 'Individual line item',
                    'measures': [
                        {'name': 'revenue', 'type': 'decimal(15,2)', 'aggregation': 'SUM'},
                        {'name': 'quantity', 'type': 'integer', 'aggregation': 'SUM'},
                        {'name': 'cost', 'type': 'decimal(15,2)', 'aggregation': 'SUM'},
                        {'name': 'profit', 'type': 'decimal(15,2)', 'aggregation': 'SUM'}
                    ],
                    'dimensions': ['dim_date', 'dim_customer', 'dim_product', 'dim_salesperson', 'dim_location', 'dim_promotion']
                },
                {
                    'name': 'fact_inventory',
                    'grain': 'Daily snapshot',
                    'measures': [
                        {'name': 'quantity_on_hand', 'type': 'integer', 'aggregation': 'MAX'},
                        {'name': 'quantity_received', 'type': 'integer', 'aggregation': 'SUM'},
                        {'name': 'quantity_shipped', 'type': 'integer', 'aggregation': 'SUM'}
                    ],
                    'dimensions': ['dim_date', 'dim_product', 'dim_warehouse']
                }
            ],
            'dimension_tables': [
                {
                    'name': 'dim_customer',
                    'type': 'Slowly Changing Dimension Type 2',
                    'attributes': [
                        {'name': 'customer_key', 'type': 'surrogate key'},
                        {'name': 'customer_natural_key', 'type': 'natural key'},
                        {'name': 'customer_name', 'type': 'text'},
                        {'name': 'effective_date', 'type': 'date'},
                        {'name': 'expiration_date', 'type': 'date'},
                        {'name': 'current_flag', 'type': 'boolean'}
                    ]
                },
                {
                    'name': 'dim_product',
                    'type': 'Slowly Changing Dimension Type 1',
                    'attributes': [
                        {'name': 'product_key', 'type': 'surrogate key'},
                        {'name': 'product_natural_key', 'type': 'natural key'},
                        {'name': 'product_name', 'type': 'text'},
                        {'name': 'category', 'type': 'text'},
                        {'name': 'subcategory', 'type': 'text'}
                    ]
                },
                {
                    'name': 'dim_date',
                    'type': 'Conformed dimension',
                    'attributes': [
                        'date_key', 'full_date', 'day_of_week', 'day_name', 'day_of_month',
                        'day_of_year', 'week_of_year', 'month', 'month_name', 'quarter',
                        'year', 'is_weekend', 'is_holiday', 'fiscal_period'
                    ]
                }
            ],
            'conformed_dimensions': ['dim_date', 'dim_employee', 'dim_location']
        }
    
    def implement_data_vault_model(self) -> Dict:
        """Implement Data Vault 2.0 model"""
        return {
            'methodology': 'Data Vault 2.0',
            'components': [
                {
                    'type': 'Hub',
                    'name': 'hub_customer',
                    'business_key': 'customer_id',
                    'satellites': ['sat_customer_pii', 'sat_customer_address']
                },
                {
                    'type': 'Hub',
                    'name': 'hub_product',
                    'business_key': 'product_id',
                    'satellites': ['sat_product_info', 'sat_product_pricing']
                },
                {
                    'type': 'Hub',
                    'name': 'hub_order',
                    'business_key': 'order_id',
                    'satellites': ['sat_order_details']
                }
            ],
            'links': [
                {
                    'name': 'link_order_customer',
                    'business_keys': ['order_id', 'customer_id'],
                    'effectivity': None
                },
                {
                    'name': 'link_order_product',
                    'business_keys': ['order_id', 'product_id'],
                    'effectivity': None
                }
            ],
            'satellites': [
                {
                    'name': 'sat_customer_pii',
                    'parent_hub': 'hub_customer',
                    'attributes': ['name', 'email', 'phone'],
                    'load_date': 'load_date',
                    'record_source': 'CRM'
                }
            ],
            'benefits': [
                'Auditability and traceability',
                'Scalability',
                'Flexibility for changes',
                'Parallel loading'
            ]
        }
    
    def design_elt_pipeline(self,
                           source: str,
                           target: str) -> Dict:
        """Design ELT pipeline"""
        return {
            'source': source,
            'target': target,
            'tool': 'dbt (data build tool)',
            'style': 'SQL-based transformations',
            'structure': [
                {
                    'layer': 'staging',
                    'models': ['stg_customers', 'stg_orders', 'stg_products'],
                    'purpose': 'Clean and standardize source data',
                    'materialization': 'View'
                },
                {
                    'layer': 'intermediate',
                    'models': ['int_orders_enriched', 'int_customer_360'],
                    'purpose': 'Business logic transformations',
                    'materialization': 'Table'
                },
                {
                    'layer': 'marts',
                    'models': ['mart_sales', 'mart_marketing', 'mart_finance'],
                    'purpose': 'Business-ready aggregated data',
                    'materialization': 'Table'
                }
            ],
            'testing': [
                'Unique tests',
                'Not-null tests',
                'Accepted values tests',
                'Referential integrity tests',
                'Custom business rule tests'
            ],
            'documentation': {
                'auto_generated': True,
                'includes': ['Lineage', 'Descriptions', 'Sources']
            }
        }
    
    def optimize_query_performance(self,
                                 table: str,
                                 query_pattern: str) -> Dict:
        """Optimize query performance"""
        return {
            'table': table,
            'query_pattern': query_pattern,
            'recommendations': [
                {
                    'area': 'Partitioning',
                    'action': f'Partition {table} by date_key',
                    'impact': '50-70% query improvement',
                    'example': 'PARTITION BY year, month'
                },
                {
                    'area': 'Clustering',
                    'action': f'Cluster {table} on frequently filtered columns',
                    'impact': '30-50% improvement',
                    'example': 'CLUSTER BY customer_id, product_category'
                },
                {
                    'area': 'Materialized Views',
                    'action': 'Create materialized view for common aggregations',
                    'impact': '90%+ improvement for pre-aggregated queries',
                    'example': 'CREATE MATERIALIZED VIEW daily_sales AS SELECT...'
                },
                {
                    'area': 'Indexing',
                    'action': 'Add secondary indexes for common joins',
                    'impact': '40-60% join improvement',
                    'example': 'CREATE INDEX idx_customer ON orders(customer_id)'
                },
                {
                    'area': 'Caching',
                    'action': 'Enable result caching for dashboards',
                    'impact': 'Near-instant for cached queries',
                    'example': 'SET query_cache_mode = ON'
                }
            ],
            'statistics': {
                'collected': True,
                'frequency': 'After load',
                'auto_update': True
            },
            'monitoring': {
                'query_execution_time': 'Track long-running queries',
                'scan_amount': 'Monitor data scanned',
                'slot_usage': 'Track compute utilization'
            }
        }
    
    def manage_data_governance(self) -> Dict:
        """Implement data governance"""
        return {
            'data_catalog': {
                'tool': 'DataHub/Amundsen',
                'features': ['Search', 'Lineage', 'Metadata management']
            },
            'data_quality': {
                'framework': 'Great Expectations/Deequ',
                'checks': ['Completeness', 'Accuracy', 'Consistency', 'Timeliness'],
                'automation': 'Run with each pipeline'
            },
            'data_stewardship': {
                'roles': ['Data Steward', 'Data Owner', 'Data Custodian'],
                'responsibilities': ['Quality oversight', 'Access control', 'Documentation']
            },
            'compliance': [
                {'regulation': 'GDPR', 'impact': 'Data subject access requests'},
                {'regulation': 'CCPA', 'impact': 'Consumer privacy requirements'},
                {'regulation': 'HIPAA', 'impact': 'PHI protection'}
            ],
            'metadata_management': {
                'technical': ['Schema', 'Data types', 'Storage'],
                'operational': ['Schedule', 'Owner', 'Quality scores'],
                'business': ['Definitions', 'Calculations', 'Usage']
            }
        }
    
    def design_data_lake(self) -> Dict:
        """Design data lake architecture"""
        return {
            'architecture': 'Lakehouse',
            'zones': [
                {
                    'name': 'Raw Zone',
                    'purpose': 'Landing for all incoming data',
                    'format': 'CSV/JSON/Parquet',
                    'access': 'Engineers only',
                    'retention': '30 days'
                },
                {
                    'name': 'Bronze Zone',
                    'purpose': 'Validated raw data',
                    'format': 'Parquet',
                    'access': 'Data scientists',
                    'retention': '1 year'
                },
                {
                    'name': 'Silver Zone',
                    'purpose': 'Cleaned and enriched data',
                    'format': 'Delta Lake',
                    'access': 'Analysts',
                    'retention': '3 years'
                },
                {
                    'name': 'Gold Zone',
                    'purpose': 'Business-ready aggregated data',
                    'format': 'Delta Lake',
                    'access': 'Business users',
                    'retention': '7 years'
                }
            ],
            'compute': {
                'interactive': 'Trino/Presto',
                'batch': 'Spark',
                'ML': 'SageMaker/Databricks'
            },
            'governance': {
                'zone_isolation': True,
                'access_control': 'IAM-based',
                'encryption': 'AES-256 at rest'
            }
        }
    
    def plan_capacity(self,
                     current_tb: float,
                     growth_rate: float) -> Dict:
        """Plan storage capacity"""
        yearly_growth = current_tb * growth_rate
        
        return {
            'current_storage_tb': current_tb,
            'growth_rate_percent': growth_rate * 100,
            'projections': {
                '1_year': current_tb * (1 + growth_rate),
                '2_years': current_tb * (1 + growth_rate) ** 2,
                '3_years': current_tb * (1 + growth_rate) ** 3,
                '5_years': current_tb * (1 + growth_rate) ** 5
            },
            'cost_optimization': [
                {'strategy': 'Tiered storage', 'savings': '40-60%'},
                {'strategy': 'Compression', 'savings': '60-70%'},
                {'strategy': 'Data lifecycle policies', 'savings': '20-30%'},
                {'strategy': 'Delete unused data', 'savings': 'Variable'}
            ],
            'compute_scaling': {
                'min_nodes': 4,
                'max_nodes': 20,
                'scaling_policy': 'Based on queue depth'
            }
        }


if __name__ == "__main__":
    dw = DataWarehousingManager()
    
    warehouse = dw.create_warehouse("Enterprise Data Warehouse", DataWarehouseType.ENTERPRISE, 100)
    print(f"Data Warehouse: {warehouse.name} ({warehouse.storage_tb} TB)")
    
    architecture = dw.design_warehouse_architecture(DataWarehouseType.LAKEHOUSE)
    print(f"Architecture: {architecture['architecture']} with {len(architecture['layers'])} layers")
    
    model = dw.design_dimensional_model(DataModel.KIMBALL)
    print(f"Dimensional Model: {len(model['fact_tables'])} facts, {len(model['dimension_tables'])} dimensions")
    
    datavault = dw.implement_data_vault_model()
    print(f"Data Vault: {len(datavault['components'])} components")
    
    elt = dw.design_elt_pipeline("ERP", "Data Warehouse")
    print(f"ELT Pipeline: {len(elt['structure'])} layers")
    
    perf = dw.optimize_query_performance("fact_sales", "monthly aggregation")
    print(f"Optimization: {len(perf['recommendations'])} recommendations")
    
    governance = dw.manage_data_governance()
    print(f"Governance: {len(governance['compliance'])} compliance requirements")
    
    datalake = dw.design_data_lake()
    print(f"Data Lake: {len(datalake['zones'])} zones")
    
    capacity = dw.plan_capacity(50, 0.25)
    print(f"Capacity: {capacity['projections']['3_years']:.0f} TB in 3 years")

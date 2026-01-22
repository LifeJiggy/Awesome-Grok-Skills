from typing import Dict, List, Optional
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


class DashboardType(Enum):
    EXECUTIVE = "Executive"
    OPERATIONAL = "Operational"
    ANALYTICAL = "Analytical"
    SELF_SERVICE = "Self-Service"


class DataSourceType(Enum):
    RELATIONAL = "relational"
    API = "api"
    FILE = "file"
    STREAMING = "streaming"


@dataclass
class BIReport:
    report_id: str
    name: str
    dashboard_type: DashboardType
    data_sources: List[str]
    refresh_rate: str


class BusinessIntelligenceManager:
    """Manage BI and reporting"""
    
    def __init__(self):
        self.reports = []
    
    def create_dashboard(self,
                        name: str,
                        dashboard_type: DashboardType,
                        metrics: List[str]) -> BIReport:
        """Create BI dashboard"""
        return BIReport(
            report_id=f"BI-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name=name,
            dashboard_type=dashboard_type,
            data_sources=['ERP', 'CRM', 'Web Analytics'],
            refresh_rate='1 hour' if dashboard_type == DashboardType.OPERATIONAL else '1 day'
        )
    
    def design_data_model(self,
                         business_entities: List[str],
                         relationships: List[Dict]) -> Dict:
        """Design dimensional data model"""
        return {
            'fact_tables': [
                {
                    'name': 'fact_sales',
                    'grain': 'Individual transaction',
                    'measures': ['revenue', 'quantity', 'cost', 'profit'],
                    'dimensions': ['dim_date', 'dim_customer', 'dim_product', 'dim_location']
                },
                {
                    'name': 'fact_inventory',
                    'grain': 'Daily snapshot per SKU',
                    'measures': ['quantity_on_hand', 'quantity_received', 'quantity_shipped'],
                    'dimensions': ['dim_date', 'dim_product', 'dim_warehouse']
                },
                {
                    'name': 'fact_finance',
                    'grain': 'Monthly by account',
                    'measures': ['actual', 'budget', 'forecast', 'variance'],
                    'dimensions': ['dim_date', 'dim_account', 'dim_department', 'dim_region']
                }
            ],
            'dimension_tables': [
                {'name': 'dim_customer', 'attributes': ['customer_key', 'name', 'segment', 'region', 'industry']},
                {'name': 'dim_product', 'attributes': ['product_key', 'name', 'category', 'subcategory', 'price']},
                {'name': 'dim_date', 'attributes': ['date_key', 'day', 'month', 'quarter', 'year', 'day_of_week']},
                {'name': 'dim_employee', 'attributes': ['employee_key', 'name', 'department', 'title', 'hire_date']}
            ],
            'relationships': relationships or [
                {'from': 'dim_product', 'to': 'fact_sales', 'type': 'one-to-many'},
                {'from': 'dim_customer', 'to': 'fact_sales', 'type': 'one-to-many'},
                {'from': 'dim_date', 'to': 'fact_sales', 'type': 'one-to-many'}
            ]
        }
    
    def create_kpi_framework(self) -> Dict:
        """Create KPI framework"""
        return {
            'kpis': [
                {
                    'category': 'Financial',
                    'kpis': [
                        {'name': 'Revenue', 'formula': 'SUM(Sales)', 'target': '10% growth YoY', 'frequency': 'Daily'},
                        {'name': 'Gross Margin', 'formula': '(Revenue - COGS) / Revenue', 'target': '> 40%', 'frequency': 'Daily'},
                        {'name': 'Operating Expenses', 'formula': 'SUM(Operating Costs)', 'target': 'Within budget', 'frequency': 'Weekly'},
                        {'name': 'EBITDA', 'formula': 'Revenue - COGS - Opex', 'target': '15% of revenue', 'frequency': 'Monthly'}
                    ]
                },
                {
                    'category': 'Sales',
                    'kpis': [
                        {'name': 'Sales Revenue', 'formula': 'SUM(Order Amount)', 'target': '$10M/quarter', 'frequency': 'Daily'},
                        {'name': 'Win Rate', 'formula': 'Won / (Won + Lost)', 'target': '> 30%', 'frequency': 'Weekly'},
                        {'name': 'Average Deal Size', 'formula': 'Total Revenue / Won Deals', 'target': '$50K', 'frequency': 'Weekly'},
                        {'name': 'Sales Cycle', 'formula': 'Average days to close', 'target': '< 45 days', 'frequency': 'Weekly'}
                    ]
                },
                {
                    'category': 'Operations',
                    'kpis': [
                        {'name': 'Order Fulfillment', 'formula': 'Orders shipped on time', 'target': '> 95%', 'frequency': 'Daily'},
                        {'name': 'Inventory Turnover', 'formula': 'COGS / Avg Inventory', 'target': '6x per year', 'frequency': 'Weekly'},
                        {'name': 'Production Efficiency', 'formula': 'Actual / Standard hours', 'target': '> 90%', 'frequency': 'Daily'},
                        {'name': 'Quality Rate', 'formula': 'Good units / Total units', 'target': '> 98%', 'frequency': 'Daily'}
                    ]
                },
                {
                    'category': 'Customer',
                    'kpis': [
                        {'name': 'NPS', 'formula': 'Promoters - Detractors', 'target': '> 50', 'frequency': 'Quarterly'},
                        {'name': 'CSAT', 'formula': 'Average satisfaction score', 'target': '> 4.5/5', 'frequency': 'Monthly'},
                        {'name': 'Churn Rate', 'formula': 'Churned / Total customers', 'target': '< 5%', 'frequency': 'Monthly'},
                        {'name': 'Customer Lifetime Value', 'formula': 'Avg purchase × Purchase frequency × Lifespan', 'target': '$10K', 'frequency': 'Quarterly'}
                    ]
                }
            ],
            'kpi_visualization': {
                'gauges': ['NPS', 'Quality Rate', 'Win Rate'],
                'trends': ['Revenue', 'Churn Rate', 'Efficiency'],
                'comparisons': ['Actual vs Target', 'YoY', 'By Region'],
                'distributions': ['Deal Size', 'Order Value']
            }
        }
    
    def design_etl_pipeline(self,
                           source: str,
                           target: str) -> Dict:
        """Design ETL pipeline"""
        return {
            'source': source,
            'target': target,
            'extract': {
                'method': 'Incremental',
                'frequency': 'Every 6 hours',
                'tools': ['Apache NiFi', 'Informatica', 'Talend'],
                'data_volume': '10 GB/day'
            },
            'transform': {
                'steps': [
                    'Data validation',
                    'Deduplication',
                    'Data quality checks',
                    'Business rule application',
                    'Aggregation',
                    'Enrichment'
                ],
                'data_quality': {
                    'accuracy': '> 99%',
                    'completeness': '> 98%',
                    'timeliness': '< 1 hour lag'
                }
            },
            'load': {
                'method': 'Upsert (Merge)',
                'strategy': 'Incremental by date key',
                'constraints': ['Referential integrity', 'Unique constraints']
            },
            'orchestration': {
                'tool': 'Apache Airflow',
                'schedule': 'Daily at 2 AM',
                'dependencies': ['Source system availability'],
                'monitoring': 'Alert on failure'
            }
        }
    
    def create_self_service_report(self,
                                  user_role: str,
                                  data_categories: List[str]) -> Dict:
        """Create self-service BI report"""
        return {
            'report_type': 'Self-Service BI',
            'target_users': user_role,
            'data_categories': data_categories,
            'capabilities': [
                'Drag-and-drop interface',
                'Pre-built templates',
                'Natural language query',
                'Auto-recommendations',
                'Collaboration features'
            ],
            'governance': {
                'data_classification': 'Public, Internal, Confidential',
                'access_control': 'Role-based',
                'data_masking': 'For sensitive fields',
                'export_controls': 'Limits on sensitive data'
            },
            'templates': [
                'Sales performance dashboard',
                'Customer analytics report',
                'Financial overview',
                'Operations metrics',
                'Custom ad-hoc reports'
            ],
            'training_required': [
                'Basic report building',
                'Data interpretation',
                'Best practices'
            ]
        }
    
    def measure_bi_success(self) -> Dict:
        """Measure BI program success"""
        return {
            'adoption_metrics': {
                'active_users': 250,
                'reports_accessed': 5000/month,
                'self_service_creation': 150/month,
                'mobile_usage': '35%'
            },
            'performance_metrics': {
                'report_generation_time': '< 5 seconds',
                'data_refresh_time': '< 1 hour',
                'system_availability': '99.9%'
            },
            'business_impact': [
                'Decision speed improved by 40%',
                'Reporting effort reduced by 60%',
                'Data-driven decisions up by 35%',
                'Saved 200+ hours/month on manual reports'
            ],
            'user_satisfaction': {
                'overall_score': 4.2,
                'ease_of_use': 4.0,
                'data_availability': 4.3,
                'performance': 4.1,
                'support': 4.4
            },
            'roi': {
                'cost_savings': '$150,000/year',
                'productivity_gain': '25%',
                'revenue_impact': 'Indirect - through better decisions'
            }
        }
    
    def integrate_ai_analytics(self) -> Dict:
        """Integrate AI/ML into BI"""
        return {
            'use_cases': [
                {
                    'name': 'Predictive Forecasting',
                    'description': 'ML models predict future trends',
                    'models': ['ARIMA', 'Prophet', 'LSTM'],
                    'impact': '20% improvement in forecast accuracy'
                },
                {
                    'name': 'Anomaly Detection',
                    'description': 'Auto-detect unusual patterns',
                    'models': ['Isolation Forest', 'Autoencoder'],
                    'impact': 'Faster issue detection'
                },
                {
                    'name': 'Customer Churn Prediction',
                    'description': 'Identify at-risk customers',
                    'models': ['Random Forest', 'XGBoost'],
                    'impact': '15% reduction in churn'
                },
                {
                    'name': 'Natural Language Query',
                    'description': 'Ask questions in plain English',
                    'models': ['BERT', 'GPT-based'],
                    'impact': 'Lower barrier to data access'
                },
                {
                    'name': 'Smart Recommendations',
                    'description': 'Suggest relevant insights',
                    'models': ['Collaborative filtering'],
                    'impact': 'Increased user engagement'
                }
            ],
            'data_requirements': {
                'minimum_records': 10000,
                'historical_data': '2+ years',
                'data_quality': 'High (>95% complete)'
            },
            'implementation_approach': {
                'phase_1': 'Quick wins (anomaly detection)',
                'phase_2': 'Predictive models',
                'phase_3': 'Natural language interface',
                'phase_4': 'Full AI-augmented analytics'
            }
        }


class DataVisualizationDesigner:
    """Design data visualizations"""
    
    def create_visualization_style_guide(self) -> Dict:
        """Create visualization style guide"""
        return {
            'color_palette': {
                'primary': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
                'sequential': ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b'],
                'diverging': ['#d73027', '#f46d43', '#fdae61', '#fee090', '#ffffbf', '#e0f3f8', '#abd9e9', '#74add1', '#4575b4']
            },
            'chart_types': {
                'comparison': ['Bar chart', 'Column chart', 'Line chart'],
                'composition': ['Pie chart', 'Stacked bar', 'Treemap'],
                'distribution': ['Histogram', 'Box plot', 'Scatter plot'],
                'relationship': ['Scatter plot', 'Bubble chart', 'Heat map'],
                'trend': ['Line chart', 'Area chart', 'Sparkline']
            },
            'typography': {
                'headings': 'Arial Bold',
                'body': 'Arial',
                'labels': 'Arial Small'
            },
            'principles': [
                'Use appropriate chart types',
                'Minimize chart junk',
                'Use consistent colors',
                'Include clear titles',
                'Add contextual annotations',
                'Ensure accessibility'
            ],
            'accessibility': [
                'Alt text for all charts',
                'Color-blind friendly palettes',
                'High contrast ratios',
                'Screen reader compatible'
            ]
        }
    
    def design_executive_dashboard(self) -> Dict:
        """Design executive dashboard"""
        return {
            'dashboard_type': 'Executive',
            'layout': {
                'top_row': ['KPI Scorecards', 'Key Metrics'],
                'middle_row': ['Trend charts', 'Comparative analysis'],
                'bottom_row': ['Alerts', 'Action items']
            },
            'metrics': [
                {'name': 'Revenue', 'visualization': 'Gauge + Trend', 'refresh': 'Daily'},
                {'name': 'Operating Margin', 'visualization': 'Gauge', 'refresh': 'Daily'},
                {'name': 'Customer Satisfaction', 'visualization': 'NPS Gauge', 'refresh': 'Weekly'},
                {'name': 'Employee Engagement', 'visualization': 'Trend line', 'refresh': 'Monthly'},
                {'name': 'Market Share', 'visualization': 'Bar chart', 'refresh': 'Quarterly'}
            ],
            'design_principles': [
                'High-level summary first',
                'Show trends over time',
                'Highlight exceptions',
                'Drill-down capabilities'
            ],
            'mobile_responsive': True
        }


if __name__ == "__main__":
    bi = BusinessIntelligenceManager()
    
    dashboard = bi.create_dashboard(
        "Sales Performance Dashboard",
        DashboardType.EXECUTIVE,
        ['Revenue', 'Orders', 'Customers', 'Products']
    )
    print(f"Dashboard: {dashboard.name} ({dashboard.dashboard_type.value})")
    
    model = bi.design_data_model(
        ['Customer', 'Product', 'Sales'],
        []
    )
    print(f"Data Model: {len(model['fact_tables'])} facts, {len(model['dimension_tables'])} dimensions")
    
    kpis = bi.create_kpi_framework()
    print(f"KPI Framework: {len(kpis['kpis'])} categories with KPIs")
    
    etl = bi.create_etl_pipeline("ERP", "Data Warehouse")
    print(f"ETL Pipeline: {len(etl['transform']['steps'])} transformation steps")
    
    self_service = bi.create_self_service_report("Manager", ['Sales', 'Finance', 'Operations'])
    print(f"Self-Service: {len(self_service['capabilities'])} capabilities")
    
    success = bi.measure_bi_success()
    print(f"BI Success: {success['adoption_metrics']['active_users']} active users")
    
    ai = bi.integrate_ai_analytics()
    print(f"AI Analytics: {len(ai['use_cases'])} use cases")
    
    style = DataVisualizationDesigner().create_visualization_style_guide()
    print(f"Visualization: {len(style['chart_types'])} chart type categories")
    
    exec_dash = DataVisualizationDesigner().design_executive_dashboard()
    print(f"Executive Dashboard: {len(exec_dash['metrics'])} key metrics")

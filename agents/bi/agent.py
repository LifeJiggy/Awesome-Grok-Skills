"""
Business Intelligence (BI) Agent
BI reporting and analytics
"""

from typing import Dict, List, Optional, Any, Tuple, Union
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import json
import hashlib
import math
import random
import logging
import os

logger = logging.getLogger(__name__)


# ============================================================================
# Enums
# ============================================================================

class ReportType(Enum):
    OPERATIONAL = "operational"
    TACTICAL = "tactical"
    STRATEGIC = "strategic"
    AD_HOC = "ad_hoc"
    COMPLIANCE = "compliance"
    FINANCIAL = "financial"
    MARKETING = "marketing"


class MetricCategory(Enum):
    REVENUE = "revenue"
    CUSTOMER = "customer"
    MARKETING = "marketing"
    OPERATIONS = "operations"
    FINANCE = "finance"
    HR = "hr"
    PRODUCT = "product"
    SALES = "sales"


class VisualizationType(Enum):
    LINE_CHART = "line_chart"
    BAR_CHART = "bar_chart"
    PIE_CHART = "pie_chart"
    SCATTER_PLOT = "scatter_plot"
    HEATMAP = "heatmap"
    TREEMAP = "treemap"
    FUNNEL = "funnel"
    GAUGE = "gauge"
    KPI_CARD = "kpi_card"
    TABLE = "table"
    MAP = "map"
    SANKEY = "sankey"
    WATERFALL = "waterfall"
    BOX_PLOT = "box_plot"
    HISTOGRAM = "histogram"


class DashboardLayout(Enum):
    GRID = "grid"
    FLOW = "flow"
    FREEFORM = "freeform"
    RESPONSIVE = "responsive"
    EXECUTIVE = "executive"
    OPERATIONAL = "operational"


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class KPIStatus(Enum):
    EXCEEDING = "exceeding"
    ON_TRACK = "on_track"
    AT_RISK = "at_risk"
    FAILING = "failing"
    NO_DATA = "no_data"


class DataRefreshFrequency(Enum):
    REAL_TIME = "real_time"
    HOURLY = "hourly"
    EVERY_4_HOURS = "every_4_hours"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class AggregationType(Enum):
    SUM = "sum"
    AVG = "avg"
    COUNT = "count"
    MIN = "min"
    MAX = "max"
    MEDIAN = "median"
    PERCENTILE_95 = "percentile_95"
    DISTINCT_COUNT = "distinct_count"


# ============================================================================
# Data Classes
# ============================================================================

@dataclass
class Report:
    report_id: str
    name: str
    report_type: ReportType
    schedule: str
    metrics: List[str] = field(default_factory=list)
    filters: Dict[str, Any] = field(default_factory=dict)
    status: str = "active"
    owner: str = ""
    created_at: str = ""
    last_run: str = ""
    next_run: str = ""
    delivery_channels: List[str] = field(default_factory=list)
    template: str = ""
    parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KPI:
    kpi_id: str
    name: str
    definition: str
    formula: str
    target: float
    unit: str
    frequency: str
    owner: str
    data_source: str
    category: MetricCategory
    thresholds: Dict[str, float] = field(default_factory=dict)
    current_value: float = 0.0
    previous_value: float = 0.0
    trend: str = "stable"
    status: KPIStatus = KPIStatus.NO_DATA
    historical_values: List[float] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Dashboard:
    dashboard_id: str
    name: str
    layout: DashboardLayout
    widgets: List[Dict[str, Any]] = field(default_factory=list)
    filters: List[str] = field(default_factory=list)
    refresh_rate: str = "1 hour"
    owner: str = ""
    viewers: List[str] = field(default_factory=list)
    is_public: bool = False
    theme: str = "default"
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Widget:
    widget_id: str
    widget_type: VisualizationType
    title: str
    data_source: str
    dimensions: List[str] = field(default_factory=list)
    measures: List[str] = field(default_factory=list)
    filters: Dict[str, Any] = field(default_factory=dict)
    config: Dict[str, Any] = field(default_factory=dict)
    position: Dict[str, int] = field(default_factory=dict)
    size: Dict[str, int] = field(default_factory=dict)


@dataclass
class Alert:
    alert_id: str
    kpi_id: str
    severity: AlertSeverity
    message: str
    threshold: float
    current_value: float
    triggered_at: str = ""
    acknowledged: bool = False
    acknowledged_by: str = ""
    acknowledged_at: str = ""


@dataclass
class DataSource:
    source_id: str
    name: str
    source_type: str
    connection_string: str
    refresh_frequency: DataRefreshFrequency
    schema: Dict[str, str] = field(default_factory=dict)
    last_synced: str = ""
    status: str = "active"
    credentials_ref: str = ""


@dataclass
class Visualization:
    viz_id: str
    viz_type: VisualizationType
    title: str
    data_config: Dict[str, Any] = field(default_factory=dict)
    style_config: Dict[str, Any] = field(default_factory=dict)
    interactive: bool = True
    created_at: str = ""


@dataclass
class ReportResult:
    report_id: str
    generated_at: str
    date_range: Dict[str, str]
    executive_summary: str
    highlights: List[Dict[str, Any]]
    detailed_metrics: Dict[str, Any]
    trends: Dict[str, List[str]]
    recommendations: List[str]
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# Report Manager
# ============================================================================

class ReportManager:
    """Report management"""

    def __init__(self):
        self.reports: Dict[str, Report] = {}
        self.report_results: Dict[str, ReportResult] = {}
        self.templates: Dict[str, Dict[str, Any]] = {}
        self._init_templates()

    def _init_templates(self):
        """Initialize report templates."""
        self.templates = {
            "weekly_sales": {
                "name": "Weekly Sales Report",
                "type": ReportType.OPERATIONAL.value,
                "metrics": ["revenue", "orders", "customers", "avg_order_value"],
                "dimensions": ["region", "product_line", "sales_rep"],
                "schedule": "weekly",
                "delivery": ["email", "slack"]
            },
            "monthly_marketing": {
                "name": "Monthly Marketing Report",
                "type": ReportType.TACTICAL.value,
                "metrics": ["leads", "conversions", "cac", "roi", "impressions"],
                "dimensions": ["channel", "campaign", "audience"],
                "schedule": "monthly",
                "delivery": ["email"]
            },
            "quarterly_finance": {
                "name": "Quarterly Finance Report",
                "type": ReportType.FINANCIAL.value,
                "metrics": ["revenue", "ebitda", "net_income", "cash_flow", "margin"],
                "dimensions": ["business_unit", "region", "product"],
                "schedule": "quarterly",
                "delivery": ["email", "pdf"]
            },
            "daily_operations": {
                "name": "Daily Operations Dashboard",
                "type": ReportType.OPERATIONAL.value,
                "metrics": ["throughput", "error_rate", "latency", "uptime"],
                "dimensions": ["service", "environment", "region"],
                "schedule": "daily",
                "delivery": ["slack"]
            }
        }

    def create_report(self,
                      name: str,
                      report_type: ReportType,
                      metrics: List[str],
                      schedule: str,
                      owner: str = "",
                      delivery_channels: Optional[List[str]] = None,
                      filters: Optional[Dict[str, Any]] = None) -> str:
        """Create report definition"""
        report_id = f"report_{hashlib.md5((name + datetime.now().isoformat()).encode()).hexdigest()[:12]}"
        timestamp = datetime.now().isoformat()

        report = Report(
            report_id=report_id,
            name=name,
            report_type=report_type,
            schedule=schedule,
            metrics=metrics,
            owner=owner,
            created_at=timestamp,
            last_run="",
            next_run=self._calculate_next_run(schedule),
            delivery_channels=delivery_channels or ["email"],
            filters=filters or {}
        )

        self.reports[report_id] = report
        logger.info(f"Created report: {report_id} ({name})")
        return report_id

    def _calculate_next_run(self, schedule: str) -> str:
        """Calculate next run time based on schedule."""
        now = datetime.now()
        schedule_map = {
            "real_time": now + timedelta(minutes=5),
            "hourly": now + timedelta(hours=1),
            "daily": now + timedelta(days=1),
            "weekly": now + timedelta(weeks=1),
            "monthly": now + timedelta(days=30),
            "quarterly": now + timedelta(days=90)
        }
        next_dt = schedule_map.get(schedule, now + timedelta(days=1))
        return next_dt.isoformat()

    def generate_report(self, report_id: str, date_range: Dict[str, str]) -> Dict:
        """Generate report"""
        report = self.reports.get(report_id)
        if not report:
            return {"error": f"Report {report_id} not found"}

        generated_at = datetime.now().isoformat()
        result = ReportResult(
            report_id=report_id,
            generated_at=generated_at,
            date_range=date_range,
            executive_summary="Performance shows positive trends across key metrics with notable improvements in customer acquisition and retention.",
            highlights=[
                {"metric": "Revenue", "value": "$1.2M", "change": "+15%", "trend": "up"},
                {"metric": "Customers", "value": "50,000", "change": "+8%", "trend": "up"},
                {"metric": "Conversion", "value": "3.5%", "change": "+0.5%", "trend": "up"},
                {"metric": "Retention", "value": "92%", "change": "+2%", "trend": "up"},
                {"metric": "NPS", "value": "42", "change": "-3", "trend": "down"}
            ],
            detailed_metrics={
                "sales": {
                    "total_revenue": 1200000,
                    "transactions": 10000,
                    "avg_order_value": 120,
                    "by_region": {
                        "North": 400000,
                        "South": 350000,
                        "East": 250000,
                        "West": 200000
                    },
                    "by_product_line": {
                        "Electronics": 500000,
                        "Clothing": 300000,
                        "Home": 250000,
                        "Sports": 150000
                    },
                    "monthly_trend": [950000, 1000000, 1050000, 1100000, 1150000, 1200000]
                },
                "marketing": {
                    "leads_generated": 5000,
                    "lead_conversion": 15,
                    "cac": 50,
                    "roi": 3.5,
                    "by_channel": {
                        "organic": {"leads": 2000, "cost": 20000, "conversions": 300},
                        "paid": {"leads": 1500, "cost": 45000, "conversions": 225},
                        "social": {"leads": 1000, "cost": 15000, "conversions": 100},
                        "email": {"leads": 500, "cost": 5000, "conversions": 75}
                    }
                },
                "operations": {
                    "order_fulfillment_rate": 98,
                    "avg_fulfillment_time": "2 days",
                    "customer_satisfaction": 4.5,
                    "inventory_turnover": 6.2,
                    "stockout_rate": 1.5
                },
                "customer": {
                    "total_customers": 50000,
                    "new_customers": 5000,
                    "churn_rate": 3.2,
                    "ltv": 850,
                    "nps": 42
                }
            },
            trends={
                "improving": ["Revenue", "Customer acquisition", "Order volume", "Fulfillment rate"],
                "stable": ["Retention rate", "Average order value", "Inventory levels"],
                "declining": ["Customer support response time", "NPS score", "Social engagement"]
            },
            recommendations=[
                "Increase marketing spend in high-performing regions (North, South)",
                "Address customer support bottlenecks to improve response times",
                "Optimize checkout flow to reduce cart abandonment by 15%",
                "Launch loyalty program to improve retention and NPS",
                "Reduce inventory stockouts through demand forecasting improvements"
            ]
        )

        self.report_results[report_id] = result
        report.last_run = generated_at

        return {
            "report_id": report_id,
            "generated_at": generated_at,
            "date_range": date_range,
            "executive_summary": result.executive_summary,
            "highlights": result.highlights,
            "detailed_metrics": result.detailed_metrics,
            "trends": result.trends,
            "recommendations": result.recommendations
        }

    def get_report_dashboard(self) -> Dict:
        """Get report dashboard"""
        active_reports = [r for r in self.reports.values() if r.status == "active"]
        scheduled = [r for r in active_reports if r.schedule not in ["ad_hoc"]]
        recent = sorted(active_reports, key=lambda r: r.last_run or "", reverse=True)[:5]

        return {
            "total_reports": len(self.reports),
            "active_reports": len(active_reports),
            "scheduled_reports": len(scheduled),
            "recent_reports": [
                {"name": r.name, "last_run": r.last_run or "Never", "status": r.status}
                for r in recent
            ],
            "upcoming_reports": [
                {"name": r.name, "next_run": r.next_run}
                for r in active_reports[:5]
            ],
            "report_usage": {
                "views_today": random.randint(200, 800),
                "views_this_week": random.randint(1000, 5000),
                "most_viewed": ["Sales Dashboard", "Marketing Metrics", "Executive Summary"]
            }
        }

    def clone_report(self, report_id: str, new_name: str) -> Optional[str]:
        """Clone an existing report with a new name."""
        original = self.reports.get(report_id)
        if not original:
            return None

        new_id = self.create_report(
            name=new_name,
            report_type=original.report_type,
            metrics=original.metrics.copy(),
            schedule=original.schedule,
            owner=original.owner,
            delivery_channels=original.delivery_channels.copy(),
            filters=original.filters.copy()
        )
        return new_id

    def archive_report(self, report_id: str) -> bool:
        """Archive a report."""
        report = self.reports.get(report_id)
        if not report:
            return False
        report.status = "archived"
        return True

    def get_report_by_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get a report definition from a template."""
        template = self.templates.get(template_name)
        if not template:
            return None
        return template.copy()


# ============================================================================
# Dashboard Designer
# ============================================================================

class DashboardDesigner:
    """Dashboard design"""

    def __init__(self):
        self.dashboards: Dict[str, Dashboard] = {}
        self.widgets: Dict[str, Widget] = {}
        self.themes: Dict[str, Dict[str, Any]] = {}
        self._init_themes()

    def _init_themes(self):
        """Initialize dashboard themes."""
        self.themes = {
            "default": {
                "background": "#ffffff",
                "text": "#333333",
                "primary": "#3498db",
                "secondary": "#2ecc71",
                "accent": "#e74c3c",
                "border": "#ecf0f1",
                "font_family": "Inter, sans-serif"
            },
            "dark": {
                "background": "#1a1a2e",
                "text": "#eaeaea",
                "primary": "#0f3460",
                "secondary": "#16213e",
                "accent": "#e94560",
                "border": "#2a2a4a",
                "font_family": "Inter, sans-serif"
            },
            "corporate": {
                "background": "#f8f9fa",
                "text": "#212529",
                "primary": "#0056b3",
                "secondary": "#28a745",
                "accent": "#ffc107",
                "border": "#dee2e6",
                "font_family": "Roboto, sans-serif"
            }
        }

    def create_dashboard(self,
                         name: str,
                         widgets: List[Dict],
                         layout: DashboardLayout = DashboardLayout.GRID,
                         theme: str = "default",
                         owner: str = "") -> str:
        """Create dashboard"""
        dashboard_id = f"dash_{hashlib.md5((name + datetime.now().isoformat()).encode()).hexdigest()[:12]}"
        timestamp = datetime.now().isoformat()

        dashboard = Dashboard(
            dashboard_id=dashboard_id,
            name=name,
            layout=layout,
            widgets=widgets,
            owner=owner,
            created_at=timestamp,
            updated_at=timestamp,
            theme=theme
        )

        self.dashboards[dashboard_id] = dashboard
        logger.info(f"Created dashboard: {dashboard_id} ({name})")
        return dashboard_id

    def design_executive_dashboard(self) -> Dict:
        """Design executive dashboard"""
        return {
            "dashboard_id": "exec_dash",
            "name": "Executive Dashboard",
            "layout": DashboardLayout.EXECUTIVE.value,
            "theme": "corporate",
            "sections": [
                {
                    "section_id": "s1",
                    "title": "Key Performance Indicators",
                    "columns": 4,
                    "widgets": [
                        {
                            "widget_id": "w1",
                            "type": VisualizationType.KPI_CARD.value,
                            "title": "Revenue",
                            "value": "$1.2M",
                            "change": "+15%",
                            "trend": "up",
                            "sparkline": [950000, 1000000, 1050000, 1100000, 1150000, 1200000]
                        },
                        {
                            "widget_id": "w2",
                            "type": VisualizationType.KPI_CARD.value,
                            "title": "Customers",
                            "value": "50,000",
                            "change": "+8%",
                            "trend": "up"
                        },
                        {
                            "widget_id": "w3",
                            "type": VisualizationType.KPI_CARD.value,
                            "title": "Conversion Rate",
                            "value": "3.5%",
                            "change": "+0.5%",
                            "trend": "up"
                        },
                        {
                            "widget_id": "w4",
                            "type": VisualizationType.KPI_CARD.value,
                            "title": "NPS",
                            "value": "42",
                            "change": "-3",
                            "trend": "down"
                        }
                    ]
                },
                {
                    "section_id": "s2",
                    "title": "Revenue Analysis",
                    "columns": 2,
                    "widgets": [
                        {
                            "widget_id": "w5",
                            "type": VisualizationType.LINE_CHART.value,
                            "title": "Revenue Trend (12 Months)",
                            "metrics": ["revenue"],
                            "period": "12 months",
                            "series": [
                                {"name": "Revenue", "data": [950000, 1000000, 1050000, 1100000, 1150000, 1200000, 1250000, 1300000, 1350000, 1400000, 1450000, 1500000]},
                                {"name": "Target", "data": [1000000, 1050000, 1100000, 1150000, 1200000, 1250000, 1300000, 1350000, 1400000, 1450000, 1500000, 1550000]}
                            ]
                        },
                        {
                            "widget_id": "w6",
                            "type": VisualizationType.BAR_CHART.value,
                            "title": "Sales by Region",
                            "dimensions": ["region"],
                            "metrics": ["revenue"],
                            "data": {
                                "North": 400000,
                                "South": 350000,
                                "East": 250000,
                                "West": 200000
                            }
                        }
                    ]
                },
                {
                    "section_id": "s3",
                    "title": "Product & Customer Insights",
                    "columns": 2,
                    "widgets": [
                        {
                            "widget_id": "w7",
                            "type": VisualizationType.TABLE.value,
                            "title": "Top Products",
                            "columns": ["Product", "Revenue", "Units", "Growth"],
                            "rows": 10,
                            "sort_by": "Revenue",
                            "sort_order": "desc"
                        },
                        {
                            "widget_id": "w8",
                            "type": VisualizationType.FUNNEL.value,
                            "title": "Sales Funnel",
                            "stages": ["Visitors", "Leads", "Opportunities", "Negotiation", "Closed"],
                            "values": [100000, 25000, 10000, 5000, 2500]
                        }
                    ]
                },
                {
                    "section_id": "s4",
                    "title": "Marketing Performance",
                    "columns": 2,
                    "widgets": [
                        {
                            "widget_id": "w9",
                            "type": VisualizationType.PIE_CHART.value,
                            "title": "Traffic by Source",
                            "data": {
                                "Organic": 35,
                                "Paid": 25,
                                "Social": 20,
                                "Direct": 15,
                                "Referral": 5
                            }
                        },
                        {
                            "widget_id": "w10",
                            "type": VisualizationType.BAR_CHART.value,
                            "title": "Campaign ROI",
                            "data": {
                                "Email": 4.2,
                                "Social": 3.8,
                                "PPC": 3.1,
                                "Content": 5.0,
                                "Affiliate": 2.8
                            }
                        }
                    ]
                }
            ],
            "global_filters": ["Date Range", "Region", "Product Line", "Sales Rep"],
            "refresh_rate": "1 hour",
            "auto_refresh": True,
            "permissions": {
                "viewers": ["executives", "directors"],
                "editors": ["admin"],
                "exporters": ["executives", "directors", "managers"]
            }
        }

    def design_operational_dashboard(self) -> Dict:
        """Design operational dashboard for real-time monitoring."""
        return {
            "dashboard_id": "ops_dash",
            "name": "Operations Dashboard",
            "layout": DashboardLayout.OPERATIONAL.value,
            "theme": "dark",
            "sections": [
                {
                    "title": "System Health",
                    "widgets": [
                        {"type": "gauge", "title": "CPU Usage", "value": 72, "max": 100, "unit": "%"},
                        {"type": "gauge", "title": "Memory Usage", "value": 58, "max": 100, "unit": "%"},
                        {"type": "gauge", "title": "Disk Usage", "value": 45, "max": 100, "unit": "%"},
                        {"type": "kpi_card", "title": "Uptime", "value": "99.97%", "trend": "stable"}
                    ]
                },
                {
                    "title": "Request Metrics",
                    "widgets": [
                        {"type": "line_chart", "title": "Requests/sec", "real_time": True, "window": "1h"},
                        {"type": "line_chart", "title": "Response Time (ms)", "real_time": True, "window": "1h"},
                        {"type": "bar_chart", "title": "Error Rate by Endpoint", "window": "24h"}
                    ]
                }
            ],
            "refresh_rate": "real_time",
            "auto_refresh": True
        }

    def analyze_dashboard_usage(self, dashboard_id: str) -> Dict:
        """Analyze dashboard usage"""
        return {
            "dashboard_id": dashboard_id,
            "analysis_period": "30 days",
            "views_30_days": random.randint(2000, 8000),
            "unique_viewers": random.randint(50, 200),
            "avg_session_duration": f"{random.randint(3, 10)} minutes",
            "peak_usage_hour": "09:00",
            "most_used_widgets": [
                {"widget": "Revenue KPI", "views": random.randint(3000, 6000), "avg_time": "45s"},
                {"widget": "Sales Trend", "views": random.randint(2000, 4000), "avg_time": "1m 20s"},
                {"widget": "Regional Breakdown", "views": random.randint(1000, 3000), "avg_time": "55s"}
            ],
            "least_used_widgets": [
                {"widget": "Detailed Metrics Table", "views": random.randint(100, 500), "avg_time": "30s"}
            ],
            "engagement_score": random.randint(65, 90),
            "user_segments": {
                "executives": {"views": 30, "avg_duration": "8m"},
                "managers": {"views": 45, "avg_duration": "12m"},
                "analysts": {"views": 25, "avg_duration": "15m"}
            },
            "recommendations": [
                "Add mobile-optimized view for executive access on-the-go",
                "Simplify complex widgets with too many data points",
                "Add drill-down capabilities to regional breakdown",
                "Consider removing or replacing low-engagement widgets",
                "Add alert thresholds to key KPIs for proactive monitoring"
            ]
        }

    def clone_dashboard(self, dashboard_id: str, new_name: str) -> Optional[str]:
        """Clone an existing dashboard."""
        original = self.dashboards.get(dashboard_id)
        if not original:
            return None

        new_id = self.create_dashboard(
            name=new_name,
            widgets=original.widgets.copy(),
            layout=original.layout,
            theme=original.theme,
            owner=original.owner
        )
        return new_id


# ============================================================================
# Data Visualization
# ============================================================================

class DataVisualization:
    """Data visualization"""

    def __init__(self):
        self.visualizations: Dict[str, Visualization] = {}
        self.palettes: Dict[str, List[str]] = {
            "default": ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", "#1abc9c"],
            "pastel": ["#a8d8ea", "#f8b4b4", "#b4e8c0", "#f8e4b4", "#d4b4e8", "#b4e8d8"],
            "bold": ["#0056b3", "#dc3545", "#28a745", "#fd7e14", "#6f42c1", "#20c997"],
            "monochrome": ["#2c3e50", "#34495e", "#7f8c8d", "#95a5a6", "#bdc3c7", "#ecf0f1"]
        }

    def suggest_visualization(self,
                              data_type: str,
                              data_points: int,
                              purpose: str) -> Dict:
        """Suggest best visualization"""
        recommendations = {
            "time_series": {
                "primary": "Line chart",
                "alternatives": ["Area chart", "Sparkline"],
                "best_for": "Showing trends over time",
                "max_points": 1000,
                "interactivity": ["zoom", "pan", "tooltip"]
            },
            "comparison": {
                "primary": "Bar chart",
                "alternatives": ["Column chart", "Lollipop chart"],
                "best_for": "Comparing values across categories",
                "max_categories": 20,
                "interactivity": ["sort", "filter", "tooltip"]
            },
            "part_to_whole": {
                "primary": "Donut chart",
                "alternatives": ["Treemap", "Stacked bar", "Waffle chart"],
                "best_for": "Showing proportions",
                "max_segments": 8,
                "interactivity": ["tooltip", "highlight"]
            },
            "distribution": {
                "primary": "Histogram",
                "alternatives": ["Box plot", "Density plot", "Violin plot"],
                "best_for": "Showing data spread",
                "interactivity": ["zoom", "tooltip", "bin_adjust"]
            },
            "relationship": {
                "primary": "Scatter plot",
                "alternatives": ["Bubble chart", "Heat map", "Correlogram"],
                "best_for": "Showing correlations between variables",
                "interactivity": ["zoom", "pan", "tooltip", "brush"]
            },
            "hierarchy": {
                "primary": "Treemap",
                "alternatives": ["Sunburst", "Sankey diagram"],
                "best_for": "Showing hierarchical data structures",
                "interactivity": ["drill_down", "tooltip"]
            },
            "geographic": {
                "primary": "Choropleth map",
                "alternatives": ["Bubble map", "Heat map overlay"],
                "best_for": "Showing geographic distribution",
                "interactivity": ["zoom", "pan", "tooltip", "filter"]
            },
            "flow": {
                "primary": "Sankey diagram",
                "alternatives": ["Alluvial chart", "Funnel chart"],
                "best_for": "Showing flows and transfers between stages",
                "interactivity": ["tooltip", "highlight"]
            }
        }

        rec = recommendations.get(data_type, recommendations["comparison"])

        if data_points > 100:
            rec["warning"] = "Large dataset - consider aggregation or sampling"

        return rec

    def create_visualization_config(self,
                                    viz_type: VisualizationType,
                                    data_config: Dict) -> Dict:
        """Create visualization configuration"""
        base_config = {
            "type": viz_type.value,
            "data_source": data_config.get("source", ""),
            "dimensions": data_config.get("dimensions", []),
            "measures": data_config.get("measures", []),
            "colors": {
                "palette": self.palettes.get("default", []),
                "gradient": False,
                "custom_mapping": {}
            },
            "labels": {
                "title": data_config.get("title", "Chart"),
                "x_axis": data_config.get("x_label", ""),
                "y_axis": data_config.get("y_label", ""),
                "legend": data_config.get("legend", True)
            },
            "interactivity": {
                "tooltips": True,
                "zoom": True,
                "filter": True,
                "drill_down": False,
                "crossfilter": False,
                "export": True
            },
            "format": {
                "width": data_config.get("width", 800),
                "height": data_config.get("height", 400),
                "responsive": True,
                "animation": True
            },
            "thresholds": data_config.get("thresholds", []),
            "reference_lines": data_config.get("reference_lines", [])
        }

        return base_config

    def create_widget(self,
                      widget_type: VisualizationType,
                      title: str,
                      data_source: str,
                      dimensions: Optional[List[str]] = None,
                      measures: Optional[List[str]] = None,
                      position: Optional[Dict[str, int]] = None,
                      size: Optional[Dict[str, int]] = None) -> Widget:
        """Create a widget for a dashboard."""
        widget_id = f"widget_{hashlib.md5((title + datetime.now().isoformat()).encode()).hexdigest()[:12]}"

        widget = Widget(
            widget_id=widget_id,
            widget_type=widget_type,
            title=title,
            data_source=data_source,
            dimensions=dimensions or [],
            measures=measures or [],
            position=position or {"x": 0, "y": 0},
            size=size or {"width": 4, "height": 3}
        )

        self.visualizations[widget_id] = Visualization(
            viz_id=widget_id,
            viz_type=widget_type,
            title=title,
            data_config={"source": data_source, "dimensions": dimensions, "measures": measures}
        )

        return widget

    def generate_color_palette(self, num_colors: int, palette_type: str = "default") -> List[str]:
        """Generate a color palette for visualizations."""
        if palette_type in self.palettes:
            base = self.palettes[palette_type]
            if num_colors <= len(base):
                return base[:num_colors]
            else:
                extended = base.copy()
                while len(extended) < num_colors:
                    r = random.randint(0, 255)
                    g = random.randint(0, 255)
                    b = random.randint(0, 255)
                    extended.append(f"#{r:02x}{g:02x}{b:02x}")
                return extended[:num_colors]

        return [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(num_colors)]


# ============================================================================
# KPI Analyzer
# ============================================================================

class KPIAnalyzer:
    """KPI analysis"""

    def __init__(self):
        self.kpis: Dict[str, KPI] = {}
        self.alerts: List[Alert] = []
        self.benchmarks: Dict[str, Dict[str, float]] = {
            "revenue_growth": {"industry_avg": 8, "top_quartile": 15, "excellent": 25},
            "customer_acquisition_cost": {"industry_avg": 100, "top_quartile": 50, "excellent": 30},
            "net_promoter_score": {"industry_avg": 30, "top_quartile": 50, "excellent": 70},
            "customer_retention": {"industry_avg": 80, "top_quartile": 90, "excellent": 95},
            "churn_rate": {"industry_avg": 5, "top_quartile": 3, "excellent": 1}
        }

    def define_kpis(self, business_goals: List[str]) -> Dict:
        """Define KPIs based on goals"""
        kpi_definitions = []

        goal_kpi_map = {
            "growth": [
                {
                    "name": "Revenue Growth",
                    "definition": "Monthly revenue growth rate",
                    "formula": "(Current Month Revenue - Last Month Revenue) / Last Month Revenue * 100",
                    "target": 10.0,
                    "unit": "percent",
                    "frequency": "monthly",
                    "owner": "CFO",
                    "data_source": "Finance System",
                    "category": MetricCategory.REVENUE,
                    "thresholds": {"warning": 5.0, "critical": 0.0}
                },
                {
                    "name": "Customer Growth Rate",
                    "definition": "Monthly customer acquisition growth",
                    "formula": "(New Customers This Month - Last Month) / Last Month * 100",
                    "target": 8.0,
                    "unit": "percent",
                    "frequency": "monthly",
                    "owner": "VP Sales",
                    "data_source": "CRM",
                    "category": MetricCategory.CUSTOMER,
                    "thresholds": {"warning": 4.0, "critical": 0.0}
                }
            ],
            "efficiency": [
                {
                    "name": "Customer Acquisition Cost",
                    "definition": "Cost to acquire a new customer",
                    "formula": "Total Marketing Spend / New Customers Acquired",
                    "target": 50.0,
                    "unit": "currency",
                    "frequency": "weekly",
                    "owner": "CMO",
                    "data_source": "Marketing Platform",
                    "category": MetricCategory.MARKETING,
                    "thresholds": {"warning": 70.0, "critical": 100.0}
                },
                {
                    "name": "Operational Efficiency Ratio",
                    "definition": "Operating expenses as percentage of revenue",
                    "formula": "Operating Expenses / Total Revenue * 100",
                    "target": 65.0,
                    "unit": "percent",
                    "frequency": "monthly",
                    "owner": "COO",
                    "data_source": "Finance System",
                    "category": MetricCategory.OPERATIONS,
                    "thresholds": {"warning": 75.0, "critical": 85.0}
                }
            ],
            "satisfaction": [
                {
                    "name": "Net Promoter Score",
                    "definition": "Customer satisfaction metric based on likelihood to recommend",
                    "formula": "% Promoters - % Detractors",
                    "target": 50.0,
                    "unit": "score",
                    "frequency": "quarterly",
                    "owner": "CXO",
                    "data_source": "Survey Platform",
                    "category": MetricCategory.CUSTOMER,
                    "thresholds": {"warning": 30.0, "critical": 20.0}
                },
                {
                    "name": "Customer Satisfaction Score",
                    "definition": "Average satisfaction rating",
                    "formula": "Sum of ratings / Number of responses",
                    "target": 4.5,
                    "unit": "score",
                    "frequency": "monthly",
                    "owner": "CXO",
                    "data_source": "Support System",
                    "category": MetricCategory.CUSTOMER,
                    "thresholds": {"warning": 3.5, "critical": 3.0}
                }
            ],
            "retention": [
                {
                    "name": "Customer Retention Rate",
                    "definition": "Percentage of customers retained over period",
                    "formula": "(Customers at End - New Customers) / Customers at Start * 100",
                    "target": 95.0,
                    "unit": "percent",
                    "frequency": "monthly",
                    "owner": "VP Customer Success",
                    "data_source": "CRM",
                    "category": MetricCategory.CUSTOMER,
                    "thresholds": {"warning": 90.0, "critical": 85.0}
                },
                {
                    "name": "Churn Rate",
                    "definition": "Percentage of customers lost over period",
                    "formula": "Customers Lost / Total Customers at Start * 100",
                    "target": 2.0,
                    "unit": "percent",
                    "frequency": "monthly",
                    "owner": "VP Customer Success",
                    "data_source": "CRM",
                    "category": MetricCategory.CUSTOMER,
                    "thresholds": {"warning": 4.0, "critical": 6.0}
                }
            ]
        }

        for goal in business_goals:
            if goal in goal_kpi_map:
                for kpi_def in goal_kpi_map[goal]:
                    kpi_id = f"kpi_{hashlib.md5(kpi_def['name'].encode()).hexdigest()[:8]}"
                    kpi = KPI(
                        kpi_id=kpi_id,
                        name=kpi_def["name"],
                        definition=kpi_def["definition"],
                        formula=kpi_def["formula"],
                        target=kpi_def["target"],
                        unit=kpi_def["unit"],
                        frequency=kpi_def["frequency"],
                        owner=kpi_def["owner"],
                        data_source=kpi_def["data_source"],
                        category=kpi_def["category"],
                        thresholds=kpi_def["thresholds"],
                        created_at=datetime.now().isoformat()
                    )
                    self.kpis[kpi_id] = kpi
                    kpi_definitions.append(kpi_def)

        return {
            "kpis": kpi_definitions,
            "kpi_count": len(kpi_definitions),
            "coverage": {goal: len(goal_kpi_map.get(goal, [])) for goal in business_goals if goal in goal_kpi_map}
        }

    def track_kpi_performance(self) -> Dict:
        """Track KPI performance"""
        performance_data = []
        overall_score = 0
        kpi_count = 0

        for kpi in self.kpis.values():
            current = random.uniform(kpi.target * 0.7, kpi.target * 1.3)
            previous = random.uniform(kpi.target * 0.6, kpi.target * 1.2)

            if current >= kpi.target:
                status = KPIStatus.EXCEEDING
            elif current >= kpi.target * 0.9:
                status = KPIStatus.ON_TRACK
            elif current >= kpi.target * 0.7:
                status = KPIStatus.AT_RISK
            else:
                status = KPIStatus.FAILING

            kpi.current_value = current
            kpi.previous_value = previous
            kpi.status = status
            kpi.trend = "up" if current > previous else "down" if current < previous else "stable"

            performance_data.append({
                "kpi": kpi.name,
                "current": round(current, 2),
                "target": kpi.target,
                "unit": kpi.unit,
                "status": status.value,
                "trend": kpi.trend,
                "change": round(((current - previous) / max(0.01, previous)) * 100, 2)
            })

            overall_score += 100 if status == KPIStatus.EXCEEDING else 75 if status == KPIStatus.ON_TRACK else 50 if status == KPIStatus.AT_RISK else 25
            kpi_count += 1

            if status in [KPIStatus.AT_RISK, KPIStatus.FAILING]:
                self._create_alert(kpi, current)

        avg_score = overall_score / max(1, kpi_count)
        overall_health = "excellent" if avg_score >= 85 else "good" if avg_score >= 70 else "fair" if avg_score >= 50 else "poor"

        return {
            "overall_health": overall_health,
            "overall_score": round(avg_score, 1),
            "kpi_performance": performance_data,
            "alerts": [
                {"kpi": a.kpi_id, "severity": a.severity.value, "message": a.message}
                for a in self.alerts[-10:]
            ],
            "recommendations": self._generate_kpi_recommendations(performance_data)
        }

    def _create_alert(self, kpi: KPI, current_value: float):
        """Create an alert for a KPI."""
        severity = AlertSeverity.CRITICAL if kpi.status == KPIStatus.FAILING else AlertSeverity.WARNING
        alert = Alert(
            alert_id=f"alert_{hashlib.md5((kpi.kpi_id + datetime.now().isoformat()).encode()).hexdigest()[:8]}",
            kpi_id=kpi.kpi_id,
            severity=severity,
            message=f"{kpi.name} is {kpi.status.value}: {current_value} (target: {kpi.target})",
            threshold=kpi.target,
            current_value=current_value,
            triggered_at=datetime.now().isoformat()
        )
        self.alerts.append(alert)

    def _generate_kpi_recommendations(self, performance_data: List[Dict]) -> List[str]:
        """Generate recommendations based on KPI performance."""
        recommendations = []
        for kpi in performance_data:
            if kpi["status"] == "failing":
                recommendations.append(f"Urgent: {kpi['kpi']} is significantly below target. Investigate root causes immediately.")
            elif kpi["status"] == "at_risk":
                recommendations.append(f"Monitor {kpi['kpi']} closely - trending below target.")
            elif kpi["status"] == "exceeding":
                recommendations.append(f"Great performance on {kpi['kpi']}. Consider raising the target.")
        return recommendations

    def get_kpi_benchmarks(self, kpi_name: str) -> Dict[str, float]:
        """Get industry benchmarks for a KPI."""
        normalized = kpi_name.lower().replace(" ", "_")
        return self.benchmarks.get(normalized, {"industry_avg": 0, "top_quartile": 0, "excellent": 0})

    def calculate_kpi_score(self, kpi_id: str) -> float:
        """Calculate a 0-100 score for a KPI based on performance vs target."""
        kpi = self.kpis.get(kpi_id)
        if not kpi or kpi.target == 0:
            return 0.0

        ratio = kpi.current_value / kpi.target
        if ratio >= 1.2:
            return 100.0
        elif ratio >= 1.0:
            return 80.0 + (ratio - 1.0) * 100.0
        elif ratio >= 0.8:
            return 60.0 + (ratio - 0.8) * 100.0
        elif ratio >= 0.5:
            return 30.0 + (ratio - 0.5) * 100.0
        else:
            return ratio * 60.0


# ============================================================================
# Self-Service Analytics
# ============================================================================

class SelfServiceAnalytics:
    """Self-service analytics"""

    def __init__(self):
        self.queries: Dict[str, Dict[str, Any]] = {}
        self.data_catalog: Dict[str, Dict[str, Any]] = {}
        self.saved_queries: Dict[str, Dict[str, Any]] = {}
        self._init_data_catalog()

    def _init_data_catalog(self):
        """Initialize data catalog with available tables."""
        self.data_catalog = {
            "sales_orders": {
                "description": "Customer orders and transactions",
                "columns": ["order_id", "customer_id", "product_id", "quantity", "amount", "order_date", "status", "region"],
                "row_count": 1500000,
                "last_updated": "2024-01-21T06:00:00",
                "owner": "Sales Team",
                "freshness": "hourly"
            },
            "customers": {
                "description": "Customer master data",
                "columns": ["customer_id", "name", "email", "company", "segment", "lifetime_value", "join_date", "country"],
                "row_count": 50000,
                "last_updated": "2024-01-21T06:00:00",
                "owner": "Customer Success",
                "freshness": "daily"
            },
            "products": {
                "description": "Product catalog and inventory",
                "columns": ["product_id", "name", "category", "price", "cost", "stock_level", "supplier"],
                "row_count": 5000,
                "last_updated": "2024-01-21T06:00:00",
                "owner": "Product Team",
                "freshness": "hourly"
            },
            "marketing_campaigns": {
                "description": "Marketing campaign performance data",
                "columns": ["campaign_id", "name", "channel", "start_date", "end_date", "impressions", "clicks", "conversions", "spend"],
                "row_count": 25000,
                "last_updated": "2024-01-21T06:00:00",
                "owner": "Marketing Team",
                "freshness": "daily"
            },
            "website_analytics": {
                "description": "Website traffic and user behavior",
                "columns": ["date", "page_views", "unique_visitors", "bounce_rate", "avg_session_duration", "conversions", "source"],
                "row_count": 365000,
                "last_updated": "2024-01-21T06:00:00",
                "owner": "Analytics Team",
                "freshness": "hourly"
            },
            "support_tickets": {
                "description": "Customer support tickets and resolution data",
                "columns": ["ticket_id", "customer_id", "subject", "category", "priority", "status", "created_at", "resolved_at", "agent"],
                "row_count": 200000,
                "last_updated": "2024-01-21T06:00:00",
                "owner": "Support Team",
                "freshness": "real_time"
            }
        }

    def create_query(self,
                     query_type: str,
                     parameters: Dict) -> Dict:
        """Create analytics query"""
        query_id = f"query_{hashlib.md5((query_type + json.dumps(parameters, default=str)).encode()).hexdigest()[:12]}"

        self.queries[query_id] = {
            "query_id": query_id,
            "type": query_type,
            "parameters": parameters,
            "status": "ready",
            "created_at": datetime.now().isoformat()
        }

        return {
            "query_id": query_id,
            "type": query_type,
            "parameters": parameters,
            "status": "ready",
            "estimated_execution_time": f"{random.randint(5, 60)} seconds",
            "estimated_rows": random.randint(100, 100000)
        }

    def run_ad_hoc_analysis(self,
                            question: str,
                            data_sources: List[str]) -> Dict:
        """Run ad-hoc analysis"""
        return {
            "question": question,
            "data_sources": data_sources,
            "analysis_type": "exploratory",
            "results": {
                "summary": "Analysis reveals strong positive trends in key business metrics with some areas needing attention.",
                "key_findings": [
                    {"finding": "Revenue increased 15% this quarter driven by electronics category", "significance": "high", "confidence": 0.92},
                    {"finding": "Customer retention improved 5% after loyalty program launch", "significance": "high", "confidence": 0.88},
                    {"finding": "Support tickets decreased 10% correlating with new chatbot deployment", "significance": "medium", "confidence": 0.85},
                    {"finding": "Social media engagement up 25% but conversion rate flat", "significance": "medium", "confidence": 0.78},
                    {"finding": "North region outperforming South by 15% in revenue per customer", "significance": "low", "confidence": 0.72}
                ],
                "data_points_analyzed": random.randint(5000, 50000),
                "visualizations": ["Trend line chart", "Regional heat map", "Comparison bar chart", "Correlation matrix"],
                "statistical_significance": 0.95
            },
            "recommendations": [
                "Scale successful marketing channels with highest ROI",
                "Expand loyalty program to underperforming regions",
                "Investigate North region success factors for replication",
                "Optimize social media funnel to improve conversion from engagement",
                "Continue chatbot investment given support ticket reduction"
            ],
            "limitations": [
                "Limited to available data sources",
                "Correlation does not imply causation",
                "Seasonal effects may influence trends",
                "External factors not captured in analysis"
            ]
        }

    def get_data_explorer(self) -> Dict:
        """Get data explorer capabilities"""
        return {
            "available_tables": len(self.data_catalog),
            "total_columns": sum(len(t["columns"]) for t in self.data_catalog.values()),
            "data_categories": list(set(
                t["description"].split()[0] for t in self.data_catalog.values()
            )),
            "tables": {
                name: {
                    "description": info["description"],
                    "columns": info["columns"],
                    "row_count": info["row_count"],
                    "freshness": info["freshness"]
                }
                for name, info in self.data_catalog.items()
            },
            "prebuilt_reports": 100,
            "self_service_features": [
                {"feature": "Drag-and-drop query builder", "status": "available", "description": "Visual query construction without SQL"},
                {"feature": "Natural language query", "status": "beta", "description": "Ask questions in plain English"},
                {"feature": "AI-powered insights", "status": "beta", "description": "Automated anomaly detection and trend identification"},
                {"feature": "Custom visualization builder", "status": "available", "description": "Create custom charts and dashboards"},
                {"feature": "Scheduled reports", "status": "available", "description": "Automate recurring report generation"},
                {"feature": "Data export", "status": "available", "description": "Export to CSV, Excel, PDF, JSON"}
            ],
            "data_access": {
                "real_time": True,
                "historical": True,
                "scheduled_refresh": "1 hour",
                "retention_period": "3 years"
            }
        }

    def save_query(self, query_id: str, name: str, description: str = "") -> bool:
        """Save a query for reuse."""
        query = self.queries.get(query_id)
        if not query:
            return False

        self.saved_queries[query_id] = {
            **query,
            "name": name,
            "description": description,
            "saved_at": datetime.now().isoformat()
        }
        return True

    def get_query_suggestions(self, partial_query: str) -> List[str]:
        """Get query suggestions based on partial input."""
        suggestions = [
            "Show revenue by region for last quarter",
            "Top 10 customers by lifetime value",
            "Monthly churn rate trend",
            "Campaign ROI comparison by channel",
            "Support ticket resolution time by priority",
            "Product sales by category and region"
        ]

        matching = [s for s in suggestions if partial_query.lower() in s.lower()]
        return matching if matching else suggestions[:3]


# ============================================================================
# Main Agent
# ============================================================================

class BIAgent:
    """Main Business Intelligence Agent orchestrating all BI capabilities."""

    def __init__(self):
        self.report_manager = ReportManager()
        self.dashboard_designer = DashboardDesigner()
        self.visualization = DataVisualization()
        self.kpi_analyzer = KPIAnalyzer()
        self.self_service = SelfServiceAnalytics()

    def get_status(self) -> Dict[str, Any]:
        """Get agent status summary."""
        return {
            "agent": "BIAgent",
            "reports": len(self.report_manager.reports),
            "dashboards": len(self.dashboard_designer.dashboards),
            "kpis": len(self.kpi_analyzer.kpis),
            "alerts": len(self.kpi_analyzer.alerts),
            "data_sources": len(self.self_service.data_catalog),
            "capabilities": [
                "Report Generation",
                "Dashboard Design",
                "Data Visualization",
                "KPI Tracking",
                "Self-Service Analytics",
                "Alert Management"
            ]
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    agent = BIAgent()

    print("=== BI Agent Demo ===\n")

    # Create a report
    report_id = agent.report_manager.create_report(
        "Weekly Sales Report",
        ReportType.OPERATIONAL,
        ["revenue", "orders", "customers"],
        "weekly"
    )
    print(f"Report created: {report_id}")

    report = agent.report_manager.generate_report(report_id, {"start": "2024-01-01", "end": "2024-01-21"})
    print(f"Report generated: {report['generated_at']}")
    print(f"Revenue: {report['highlights'][0]['value']} ({report['highlights'][0]['change']})")

    # Dashboard
    exec_dash = agent.dashboard_designer.design_executive_dashboard()
    print(f"\nDashboard: {exec_dash['name']}")
    print(f"Sections: {len(exec_dash['sections'])}")

    # KPIs
    kpis = agent.kpi_analyzer.define_kpis(["growth", "efficiency", "satisfaction"])
    print(f"\nKPIs defined: {len(kpis['kpis'])}")

    performance = agent.kpi_analyzer.track_kpi_performance()
    print(f"Overall health: {performance['overall_health']}")
    for kpi_data in performance["kpi_performance"]:
        print(f"  {kpi_data['kpi']}: {kpi_data['current']} ({kpi_data['status']})")

    # Visualization suggestion
    viz = agent.visualization.suggest_visualization("time_series", 50, "trend_analysis")
    print(f"\nVisualization suggestion: {viz['primary']}")

    # Self-service analytics
    explorer = agent.self_service.get_data_explorer()
    print(f"\nData tables: {explorer['available_tables']}")
    print(f"Features: {[f['feature'] for f in explorer['self_service_features']]}")

    # Agent status
    status = agent.get_status()
    print(f"\nAgent Status: {json.dumps(status, indent=2)}")

"""
Governance Dashboard System

Implements KPI tracking, compliance posture visualization, risk heatmaps,
and executive reporting for governance dashboards.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
from uuid import uuid4


# ─── Enums ───────────────────────────────────────────────────────────────────

class DashboardTier(Enum):
    EXECUTIVE = "executive"
    MANAGEMENT = "management"
    OPERATIONAL = "operational"
    AUDIT = "audit"


class PostureRating(Enum):
    STRONG = "strong"
    ADEQUATE = "adequate"
    NEEDS_IMPROVEMENT = "needs_improvement"
    WEAK = "weak"


class RiskTreatment(Enum):
    ACCEPT = "accept"
    MITIGATE = "mitigate"
    TRANSFER = "transfer"
    AVOID = "avoid"


class TrendDirection(Enum):
    IMPROVING = "improving"
    DECLINING = "declining"
    STABLE = "stable"
    VOLATILE = "volatile"


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class MetricStatus(Enum):
    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"


# ─── Data Classes ────────────────────────────────────────────────────────────

@dataclass
class KPI:
    """Key Performance Indicator definition and current value."""
    kpi_id: str = field(default_factory=lambda: f"KPI-{str(uuid4())[:6]}")
    name: str = ""
    description: str = ""
    category: str = ""  # compliance, risk, audit, reporting
    formula: str = ""
    current_value: float = 0.0
    target_value: float = 90.0
    red_threshold: float = 70.0
    yellow_threshold: float = 80.0
    unit: str = "%"  # %, count, days, score
    period: str = ""
    trend: TrendDirection = TrendDirection.STABLE
    history: list[dict[str, Any]] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.utcnow)
    owner: str = ""

    @property
    def status(self) -> MetricStatus:
        if self.current_value >= self.yellow_threshold:
            return MetricStatus.GREEN
        elif self.current_value >= self.red_threshold:
            return MetricStatus.YELLOW
        return MetricStatus.RED

    @property
    def gap_from_target(self) -> float:
        return self.target_value - self.current_value

    def update_value(self, new_value: float) -> None:
        self.history.append({
            "value": self.current_value,
            "timestamp": self.last_updated.isoformat(),
        })
        self.current_value = new_value
        self.last_updated = datetime.utcnow()
        self._calculate_trend()

    def _calculate_trend(self) -> None:
        if len(self.history) < 2:
            self.trend = TrendDirection.STABLE
            return
        recent = [h["value"] for h in self.history[-5:]]
        if len(recent) < 2:
            self.trend = TrendDirection.STABLE
            return
        diffs = [recent[i + 1] - recent[i] for i in range(len(recent) - 1)]
        avg_diff = sum(diffs) / len(diffs)
        if abs(avg_diff) < 0.5:
            self.trend = TrendDirection.STABLE
        elif avg_diff > 0:
            self.trend = TrendDirection.IMPROVING
        else:
            self.trend = TrendDirection.DECLINING


@dataclass
class RiskEntry:
    """Risk heatmap entry."""
    risk_id: str = field(default_factory=lambda: f"RISK-{str(uuid4())[:6]}")
    title: str = ""
    description: str = ""
    category: str = ""  # strategic, operational, financial, compliance
    likelihood: int = 3  # 1-5
    impact: int = 3  # 1-5
    risk_owner: str = ""
    treatment: RiskTreatment = RiskTreatment.MITIGATE
    last_assessed: datetime = field(default_factory=datetime.utcnow)
    status: str = "open"  # open, closed, accepted
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def risk_score(self) -> int:
        return self.likelihood * self.impact

    @property
    def risk_zone(self) -> str:
        score = self.risk_score
        if score >= 15:
            return "critical"
        elif score >= 9:
            return "high"
        elif score >= 4:
            return "medium"
        return "low"

    @property
    def zone_color(self) -> str:
        zone = self.risk_zone
        if zone == "critical":
            return "red"
        elif zone == "high":
            return "orange"
        elif zone == "medium":
            return "yellow"
        return "green"


@dataclass
class CompliancePosture:
    """Overall compliance posture snapshot."""
    posture_id: str = field(default_factory=lambda: f"POS-{str(uuid4())[:6]}")
    period: str = ""
    framework_compliance: float = 0.0  # 0-100
    control_effectiveness: float = 0.0  # 0-100
    risk_posture: float = 0.0  # 0-100
    audit_health: float = 0.0  # 0-100
    reporting_compliance: float = 0.0  # 0-100
    calculated_at: datetime = field(default_factory=datetime.utcnow)
    rating: PostureRating = PostureRating.ADEQUATE

    @property
    def overall_score(self) -> float:
        return (
            self.framework_compliance * 0.30 +
            self.control_effectiveness * 0.25 +
            self.risk_posture * 0.20 +
            self.audit_health * 0.15 +
            self.reporting_compliance * 0.10
        )

    def calculate_rating(self) -> PostureRating:
        score = self.overall_score
        if score >= 80:
            self.rating = PostureRating.STRONG
        elif score >= 60:
            self.rating = PostureRating.ADEQUATE
        elif score >= 40:
            self.rating = PostureRating.NEEDS_IMPROVEMENT
        else:
            self.rating = PostureRating.WEAK
        return self.rating


@dataclass
class DashboardAlert:
    """Dashboard alert for critical conditions."""
    alert_id: str = field(default_factory=lambda: f"ALT-{str(uuid4())[:6]}")
    severity: AlertSeverity = AlertSeverity.INFO
    title: str = ""
    message: str = ""
    source: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    acknowledged: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class HeatmapCell:
    """Single cell in a risk heatmap."""
    likelihood: int = 1
    impact: int = 1
    risks: list[RiskEntry] = field(default_factory=list)
    color: str = "green"

    @property
    def risk_count(self) -> int:
        return len(self.risks)

    @property
    def max_score(self) -> int:
        if not self.risks:
            return 0
        return max(r.risk_score for r in self.risks)


# ─── Core Classes ────────────────────────────────────────────────────────────

class KPITracker:
    """Tracks and manages KPIs across governance domains."""

    DEFAULT_KPIS = [
        ("compliance_rate", "Compliance Rate", "compliance",
         "Effective controls / Total controls", 90.0, 70.0),
        ("control_effectiveness", "Control Effectiveness", "compliance",
         "Effective / (Effective + Ineffective)", 95.0, 80.0),
        ("finding_closure_rate", "Finding Closure Rate", "audit",
         "Findings closed on time / Total findings", 90.0, 70.0),
        ("mttr", "Mean Time to Remediate", "audit",
         "Total remediation days / Number of findings", 60.0, 120.0),
        ("risk_appetite_adherence", "Risk Appetite Adherence", "risk",
         "Risks within appetite / Total risks", 90.0, 70.0),
        ("on_time_submission", "On-Time Submission", "reporting",
         "Reports submitted on time / Total reports", 100.0, 95.0),
        ("repeat_finding_rate", "Repeat Finding Rate", "audit",
         "Repeat findings / Total findings", 10.0, 25.0),
    ]

    def __init__(self) -> None:
        self.kpis: dict[str, KPI] = {}
        self._initialize_default_kpis()

    def _initialize_default_kpis(self) -> None:
        for kid, name, cat, formula, target, red in self.DEFAULT_KPIS:
            kpi = KPI(
                kpi_id=f"KPI-{kid.upper()[:6]}",
                name=name,
                category=cat,
                formula=formula,
                target_value=target,
                red_threshold=red,
                yellow_threshold=(target + red) / 2,
            )
            self.kpis[kid] = kpi

    def update_kpi(self, kpi_id: str, value: float) -> Optional[KPI]:
        kpi = self.kpis.get(kpi_id)
        if kpi:
            kpi.update_value(value)
        return kpi

    def get_kpis_by_category(self, category: str) -> list[KPI]:
        return [k for k in self.kpis.values() if k.category == category]

    def get_kpis_by_status(self, status: MetricStatus) -> list[KPI]:
        return [k for k in self.kpis.values() if k.status == status]

    def get_critical_kpis(self) -> list[KPI]:
        return self.get_kpis_by_status(MetricStatus.RED)

    def get_kpi_summary(self) -> dict[str, Any]:
        total = len(self.kpis)
        green = len(self.get_kpis_by_status(MetricStatus.GREEN))
        yellow = len(self.get_kpis_by_status(MetricStatus.YELLOW))
        red = len(self.get_kpis_by_status(MetricStatus.RED))
        return {
            "total_kpis": total,
            "green": green,
            "yellow": yellow,
            "red": red,
            "health_score": (green / total * 100) if total > 0 else 0.0,
        }


class RiskHeatmap:
    """Risk heatmap visualization and management."""

    def __init__(self) -> None:
        self.risks: dict[str, RiskEntry] = {}
        self.grid: list[list[HeatmapCell]] = [
            [HeatmapCell(likelihood=i, impact=j) for j in range(1, 6)]
            for i in range(1, 6)
        ]

    def add_risk(self, risk: RiskEntry) -> None:
        self.risks[risk.risk_id] = risk
        cell = self.grid[risk.likelihood - 1][risk.impact - 1]
        cell.risks.append(risk)
        cell.color = risk.zone_color

    def remove_risk(self, risk_id: str) -> bool:
        risk = self.risks.pop(risk_id, None)
        if not risk:
            return False
        cell = self.grid[risk.likelihood - 1][risk.impact - 1]
        cell.risks = [r for r in cell.risks if r.risk_id != risk_id]
        return True

    def get_top_risks(self, n: int = 5) -> list[RiskEntry]:
        open_risks = [r for r in self.risks.values() if r.status == "open"]
        return sorted(open_risks, key=lambda r: r.risk_score, reverse=True)[:n]

    def get_risks_by_zone(self, zone: str) -> list[RiskEntry]:
        return [r for r in self.risks.values() if r.risk_zone == zone]

    def get_risks_by_category(self, category: str) -> list[RiskEntry]:
        return [r for r in self.risks.values() if r.category == category]

    def get_risks_by_owner(self, owner: str) -> list[RiskEntry]:
        return [r for r in self.risks.values() if r.risk_owner == owner]

    def get_heatmap_matrix(self) -> list[list[dict[str, Any]]]:
        matrix = []
        for i, row in enumerate(self.grid):
            matrix_row = []
            for j, cell in enumerate(row):
                matrix_row.append({
                    "likelihood": i + 1,
                    "impact": j + 1,
                    "risk_count": cell.risk_count,
                    "color": cell.color,
                    "max_score": cell.max_score,
                    "risk_ids": [r.risk_id for r in cell.risks],
                })
            matrix.append(matrix_row)
        return matrix

    def get_risk_summary(self) -> dict[str, Any]:
        open_risks = [r for r in self.risks.values() if r.status == "open"]
        return {
            "total_risks": len(self.risks),
            "open_risks": len(open_risks),
            "critical": len([r for r in open_risks if r.risk_zone == "critical"]),
            "high": len([r for r in open_risks if r.risk_zone == "high"]),
            "medium": len([r for r in open_risks if r.risk_zone == "medium"]),
            "low": len([r for r in open_risks if r.risk_zone == "low"]),
            "avg_score": sum(r.risk_score for r in open_risks) / len(open_risks) if open_risks else 0,
        }

    def get_appetite_compliance(self, appetite_boundary: int = 9) -> dict[str, Any]:
        open_risks = [r for r in self.risks.values() if r.status == "open"]
        within = [r for r in open_risks if r.risk_score <= appetite_boundary]
        outside = [r for r in open_risks if r.risk_score > appetite_boundary]
        return {
            "within_appetite": len(within),
            "outside_appetite": len(outside),
            "adherence_rate": (len(within) / len(open_risks) * 100) if open_risks else 100.0,
        }


class PostureCalculator:
    """Calculates and tracks compliance posture."""

    def __init__(self, kpi_tracker: KPITracker, risk_heatmap: RiskHeatmap) -> None:
        self.kpi_tracker = kpi_tracker
        self.risk_heatmap = risk_heatmap
        self.posture_history: list[CompliancePosture] = []

    def calculate_posture(self, period: str = "",
                          framework_compliance: float = 0.0,
                          control_effectiveness: float = 0.0,
                          audit_health: float = 0.0,
                          reporting_compliance: float = 0.0) -> CompliancePosture:
        risk_summary = self.risk_heatmap.get_risk_summary()
        open_risks = risk_summary["open_risks"]
        critical_risks = risk_summary["critical"]
        risk_posture = max(0, 100 - (critical_risks * 20 + open_risks * 2))

        posture = CompliancePosture(
            period=period,
            framework_compliance=framework_compliance,
            control_effectiveness=control_effectiveness,
            risk_posture=risk_posture,
            audit_health=audit_health,
            reporting_compliance=reporting_compliance,
        )
        posture.calculate_rating()
        self.posture_history.append(posture)
        return posture

    def get_posture_trend(self, n_periods: int = 5) -> list[dict[str, Any]]:
        recent = self.posture_history[-n_periods:]
        return [
            {
                "period": p.period,
                "score": round(p.overall_score, 1),
                "rating": p.rating.value,
                "timestamp": p.calculated_at.isoformat(),
            }
            for p in recent
        ]

    def get_trend_direction(self) -> TrendDirection:
        if len(self.posture_history) < 2:
            return TrendDirection.STABLE
        scores = [p.overall_score for p in self.posture_history[-5:]]
        diffs = [scores[i + 1] - scores[i] for i in range(len(scores) - 1)]
        avg_diff = sum(diffs) / len(diffs) if diffs else 0
        if avg_diff > 2:
            return TrendDirection.IMPROVING
        elif avg_diff < -2:
            return TrendDirection.DECLINING
        return TrendDirection.STABLE

    def generate_posture_report(self) -> dict[str, Any]:
        current = self.posture_history[-1] if self.posture_history else None
        trend = self.get_trend_direction()
        kpi_summary = self.kpi_tracker.get_kpi_summary()
        risk_summary = self.risk_heatmap.get_risk_summary()
        return {
            "posture_score": round(current.overall_score, 1) if current else 0,
            "rating": current.rating.value if current else "unknown",
            "trend": trend.value,
            "kpi_health": kpi_summary,
            "risk_summary": risk_summary,
            "top_risks": [
                {"id": r.risk_id, "title": r.title, "score": r.risk_score}
                for r in self.risk_heatmap.get_top_risks(3)
            ],
        }


class ExecutiveReporter:
    """Generates executive-level reports and summaries."""

    def __init__(self, posture_calc: PostureCalculator) -> None:
        self.posture_calc = posture_calc
        self.alerts: list[DashboardAlert] = []

    def generate_executive_summary(self) -> str:
        report = self.posture_calc.generate_posture_report()
        trend_arrow = {
            "improving": "↑", "declining": "↓",
            "stable": "→", "volatile": "↕",
        }.get(report["trend"], "→")

        lines = [
            "=" * 60,
            "GOVERNANCE POSTURE - Executive Summary",
            "=" * 60,
            "",
            f"POSTURE SCORE: {report['posture_score']}/100 {trend_arrow}",
            f"RATING: {report['rating'].upper().replace('_', ' ')}",
            "",
            "KEY METRICS:",
            f"  Compliance Rate: {report['kpi_health']['health_score']:.0f}% "
            f"({report['kpi_health']['green']}/{report['kpi_health']['total_kpis']} green)",
            f"  Open Risks: {report['risk_summary']['open_risks']} "
            f"(Critical: {report['risk_summary']['critical']}, "
            f"High: {report['risk_summary']['high']})",
            "",
            "TOP RISKS:",
        ]
        for risk in report["top_risks"]:
            lines.append(f"  {risk['id']}: {risk['title']} (Score: {risk['score']})")

        kpi_summary = report["kpi_health"]
        if kpi_summary["red"] > 0:
            lines.extend(["", "CRITICAL KPIs ATTENTION NEEDED:"])
            for kpi in self.posture_calc.kpi_tracker.get_critical_kpis():
                lines.append(f"  - {kpi.name}: {kpi.current_value}{kpi.unit} "
                             f"(target: {kpi.target_value}{kpi.unit})")

        lines.extend(["", "=" * 60])
        return "\n".join(lines)

    def add_alert(self, severity: AlertSeverity, title: str,
                  message: str, source: str = "") -> DashboardAlert:
        alert = DashboardAlert(
            severity=severity, title=title, message=message, source=source,
        )
        self.alerts.append(alert)
        return alert

    def get_unacknowledged_alerts(self) -> list[DashboardAlert]:
        return [a for a in self.alerts if not a.acknowledged]

    def get_critical_alerts(self) -> list[DashboardAlert]:
        return [a for a in self.alerts if a.severity == AlertSeverity.CRITICAL]


class DashboardAggregator:
    """Aggregates all dashboard data for rendering."""

    def __init__(self) -> None:
        self.kpi_tracker = KPITracker()
        self.risk_heatmap = RiskHeatmap()
        self.posture_calc = PostureCalculator(self.kpi_tracker, self.risk_heatmap)
        self.executive_reporter = ExecutiveReporter(self.posture_calc)

    def build_executive_dashboard(self) -> dict[str, Any]:
        posture_report = self.posture_calc.generate_posture_report()
        critical_kpis = self.kpi_tracker.get_critical_kpis()
        return {
            "tier": DashboardTier.EXECUTIVE.value,
            "posture": posture_report,
            "critical_kpis": [
                {"name": k.name, "value": k.current_value, "status": k.status.value}
                for k in critical_kpis
            ],
            "risk_summary": self.risk_heatmap.get_risk_summary(),
            "top_risks": [
                {"id": r.risk_id, "title": r.title, "score": r.risk_score, "zone": r.risk_zone}
                for r in self.risk_heatmap.get_top_risks(5)
            ],
            "alerts": [
                {"title": a.title, "severity": a.severity.value}
                for a in self.executive_reporter.get_unacknowledged_alerts()
            ],
        }

    def build_operational_dashboard(self) -> dict[str, Any]:
        return {
            "tier": DashboardTier.OPERATIONAL.value,
            "kpi_details": [
                {
                    "name": k.name, "value": k.current_value,
                    "target": k.target_value, "status": k.status.value,
                    "trend": k.trend.value, "category": k.category,
                }
                for k in self.kpi_tracker.kpis.values()
            ],
            "heatmap": self.risk_heatmap.get_heatmap_matrix(),
            "risks_by_zone": {
                zone: len(self.risk_heatmap.get_risks_by_zone(zone))
                for zone in ["critical", "high", "medium", "low"]
            },
        }

    def get_dashboard_summary(self) -> dict[str, Any]:
        kpi_summary = self.kpi_tracker.get_kpi_summary()
        risk_summary = self.risk_heatmap.get_risk_summary()
        posture = self.posture_calc.posture_history
        current_score = posture[-1].overall_score if posture else 0
        return {
            "kpi_health": kpi_summary,
            "risk_summary": risk_summary,
            "posture_score": round(current_score, 1),
            "alert_count": len(self.executive_reporter.get_unacknowledged_alerts()),
        }


# ─── Demo ────────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate governance dashboard system."""
    print("=" * 70)
    print("GOVERNANCE DASHBOARD SYSTEM")
    print("=" * 70)

    dashboard = DashboardAggregator()

    # 1. KPI Tracking
    print("\n[1] KPI Tracking")
    print("-" * 40)
    kpi_values = {
        "compliance_rate": 87.5,
        "control_effectiveness": 92.0,
        "finding_closure_rate": 78.0,
        "mttr": 85.0,
        "risk_appetite_adherence": 85.0,
        "on_time_submission": 100.0,
        "repeat_finding_rate": 8.0,
    }
    for kid, value in kpi_values.items():
        dashboard.kpi_tracker.update_kpi(kid, value)
        kpi = dashboard.kpi_tracker.kpis[kid]
        print(f"  {kpi.name:30s} = {value:6.1f}{kpi.unit:4s} [{kpi.status.value:6s}]")

    kpi_summary = dashboard.kpi_tracker.get_kpi_summary()
    print(f"\n  KPI Health: {kpi_summary['health_score']:.0f}% "
          f"(G:{kpi_summary['green']} Y:{kpi_summary['yellow']} R:{kpi_summary['red']})")

    critical = dashboard.kpi_tracker.get_critical_kpis()
    if critical:
        print(f"  Critical KPIs: {[k.name for k in critical]}")

    # 2. Risk Heatmap
    print("\n[2] Risk Heatmap")
    print("-" * 40)
    risks = [
        RiskEntry(title="Data Breach", likelihood=4, impact=5, category="operational",
                  risk_owner="CISO", treatment=RiskTreatment.MITIGATE),
        RiskEntry(title="Regulatory Fine", likelihood=3, impact=4, category="compliance",
                  risk_owner="CLO", treatment=RiskTreatment.MITIGATE),
        RiskEntry(title="System Outage", likelihood=3, impact=3, category="operational",
                  risk_owner="CTO", treatment=RiskTreatment.TRANSFER),
        RiskEntry(title="Vendor Failure", likelihood=2, impact=4, category="strategic",
                  risk_owner="COO", treatment=RiskTreatment.ACCEPT),
        RiskEntry(title="Insider Threat", likelihood=2, impact=5, category="operational",
                  risk_owner="CISO", treatment=RiskTreatment.MITIGATE),
        RiskEntry(title="Market Shift", likelihood=3, impact=2, category="strategic",
                  risk_owner="CEO", treatment=RiskTreatment.ACCEPT),
    ]
    for risk in risks:
        dashboard.risk_heatmap.add_risk(risk)
        print(f"  {risk.risk_id}: {risk.title:20s} L={risk.likelihood} I={risk.impact} "
              f"Score={risk.risk_score} Zone={risk.risk_zone}")

    top_risks = dashboard.risk_heatmap.get_top_risks(3)
    print(f"\n  Top 3 Risks:")
    for r in top_risks:
        print(f"    {r.title}: Score {r.risk_score} ({r.risk_zone})")

    risk_summary = dashboard.risk_heatmap.get_risk_summary()
    print(f"\n  Risk Summary: {risk_summary['open_risks']} open, "
          f"Critical={risk_summary['critical']}, High={risk_summary['high']}")

    appetite = dashboard.risk_heatmap.get_appetite_compliance(appetite_boundary=9)
    print(f"  Appetite Adherence: {appetite['adherence_rate']:.0f}% "
          f"({appetite['within_appetite']} within, {appetite['outside_appetite']} outside)")

    # 3. Heatmap Matrix
    print("\n[3] Risk Heatmap Matrix")
    print("-" * 40)
    matrix = dashboard.risk_heatmap.get_heatmap_matrix()
    print("  Impact →  1    2    3    4    5")
    print("  Likelihood ↓")
    for i, row in enumerate(matrix):
        cells = [f"  {c['risk_count']:3d} " if c['risk_count'] > 0 else "   - " for c in row]
        print(f"    {i + 1}     {''.join(cells)}")

    # 4. Compliance Posture
    print("\n[4] Compliance Posture")
    print("-" * 40)
    posture = dashboard.posture_calc.calculate_posture(
        period="2025-Q2",
        framework_compliance=87.5,
        control_effectiveness=92.0,
        audit_health=78.0,
        reporting_compliance=100.0,
    )
    print(f"  Period: {posture.period}")
    print(f"  Overall Score: {posture.overall_score:.1f}/100")
    print(f"  Rating: {posture.rating.value}")
    print(f"  Components:")
    print(f"    Framework Compliance: {posture.framework_compliance}%")
    print(f"    Control Effectiveness: {posture.control_effectiveness}%")
    print(f"    Risk Posture: {posture.risk_posture}%")
    print(f"    Audit Health: {posture.audit_health}%")
    print(f"    Reporting Compliance: {posture.reporting_compliance}%")

    # Calculate a second period to show trend
    dashboard.posture_calc.calculate_posture(
        period="2025-Q1",
        framework_compliance=82.0,
        control_effectiveness=88.0,
        audit_health=75.0,
        reporting_compliance=95.0,
    )
    trend = dashboard.posture_calc.get_trend_direction()
    print(f"  Trend: {trend.value}")

    # 5. Executive Report
    print("\n[5] Executive Summary")
    print("-" * 40)
    exec_summary = dashboard.executive_reporter.generate_executive_summary()
    print(exec_summary)

    # 6. Alerts
    print("\n[6] Dashboard Alerts")
    print("-" * 40)
    dashboard.executive_reporter.add_alert(
        AlertSeverity.WARNING, "KPI Below Target",
        "Finding Closure Rate at 78%, target is 90%", "audit_kpis",
    )
    dashboard.executive_reporter.add_alert(
        AlertSeverity.CRITICAL, "Critical Risk Identified",
        "Data Breach risk score exceeds appetite", "risk_heatmap",
    )
    unacked = dashboard.executive_reporter.get_unacknowledged_alerts()
    print(f"  Unacknowledged alerts: {len(unacked)}")
    for a in unacked:
        print(f"    [{a.severity.value:8s}] {a.title}: {a.message}")

    # 7. Dashboard Aggregation
    print("\n[7] Dashboard Aggregation")
    print("-" * 40)
    exec_dashboard = dashboard.build_executive_dashboard()
    print(f"  Executive Dashboard:")
    print(f"    Tier: {exec_dashboard['tier']}")
    print(f"    Posture Score: {exec_dashboard['posture']['posture_score']}")
    print(f"    Critical KPIs: {len(exec_dashboard['critical_kpis'])}")
    print(f"    Open Risks: {exec_dashboard['risk_summary']['open_risks']}")
    print(f"    Alerts: {len(exec_dashboard['alerts'])}")

    op_dashboard = dashboard.build_operational_dashboard()
    print(f"\n  Operational Dashboard:")
    print(f"    Tier: {op_dashboard['tier']}")
    print(f"    KPIs Tracked: {len(op_dashboard['kpi_details'])}")
    print(f"    Risks by Zone: {op_dashboard['risks_by_zone']}")

    summary = dashboard.get_dashboard_summary()
    print(f"\n  Summary: {summary}")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

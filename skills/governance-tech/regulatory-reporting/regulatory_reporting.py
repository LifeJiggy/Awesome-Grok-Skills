"""
Automated Regulatory Reporting System

Implements data collection, validation, submission automation, and
compliance reporting for GDPR, SOX, HIPAA, and Basel III.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional
from uuid import uuid4


# ─── Enums ───────────────────────────────────────────────────────────────────

class RegulatoryFramework(Enum):
    GDPR = "gdpr"
    SOX = "sox"
    HIPAA = "hipaa"
    BASEL_III = "basel_iii"


class ReportType(Enum):
    # GDPR
    ROPA = "ropa"
    DPIA = "dpia"
    BREACH_NOTIFICATION = "breach_notification"
    DSAR_RESPONSE = "dsar_response"
    # SOX
    SECTION_302 = "section_302"
    SECTION_404 = "section_404"
    MATERIAL_WEAKNESS = "material_weakness"
    CONTROL_TESTING = "control_testing"
    # HIPAA
    SECURITY_RISK_ASSESSMENT = "security_risk_assessment"
    HIPAA_BREACH = "hipaa_breach"
    COMPLIANCE_REVIEW = "compliance_review"
    # Basel III
    CAPITAL_ADEQUACY = "capital_adequacy"
    LCR = "lcr"
    NSFR = "nsfr"
    LARGE_EXPOSURE = "large_exposure"


class SubmissionChannel(Enum):
    PORTAL = "portal"
    API = "api"
    EDGAR = "edgar"
    SECURE_UPLOAD = "secure_upload"
    EMAIL = "email"


class SubmissionState(Enum):
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    FORMATTED = "formatted"
    SUBMITTED = "submitted"
    CONFIRMED = "confirmed"
    ARCHIVED = "archived"
    REVISION = "revision"
    REJECTED = "rejected"


class ValidationStatus(Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"


class DataQualityDimension(Enum):
    COMPLETENESS = "completeness"
    ACCURACY = "accuracy"
    TIMELINESS = "timeliness"
    CONSISTENCY = "consistency"
    VALIDITY = "validity"


# ─── Data Classes ────────────────────────────────────────────────────────────

@dataclass
class ReportingDeadline:
    """Regulatory reporting deadline."""
    deadline_id: str = field(default_factory=lambda: f"DL-{str(uuid4())[:6]}")
    framework: RegulatoryFramework = RegulatoryFramework.GDPR
    report_type: ReportType = ReportType.ROPA
    description: str = ""
    due_date: datetime = field(default_factory=datetime.utcnow)
    recurrence: str = "annual"  # annual, quarterly, monthly, event_driven
    submission_channel: SubmissionChannel = SubmissionChannel.PORTAL
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def days_until_due(self) -> int:
        return max(0, (self.due_date - datetime.utcnow()).days)

    @property
    def is_overdue(self) -> bool:
        return datetime.utcnow() > self.due_date


@dataclass
class DataSource:
    """Regulatory data source definition."""
    source_id: str = field(default_factory=lambda: f"SRC-{str(uuid4())[:6]}")
    name: str = ""
    system: str = ""
    connection_type: str = "api"  # api, database, file, manual
    endpoint: str = ""
    credentials_ref: str = ""
    refresh_frequency: str = "daily"
    last_refreshed: Optional[datetime] = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationRule:
    """Data validation rule."""
    rule_id: str = field(default_factory=lambda: f"VR-{str(uuid4())[:6]}")
    name: str = ""
    description: str = ""
    dimension: DataQualityDimension = DataQualityDimension.COMPLETENESS
    rule_type: str = "range"  # range, format, referential, calculation, threshold, completeness
    field: str = ""
    parameters: dict[str, Any] = field(default_factory=dict)
    framework: RegulatoryFramework = RegulatoryFramework.GDPR
    severity: str = "error"  # error, warning, info


@dataclass
class ValidationResult:
    """Result of running a validation rule."""
    validation_id: str = field(default_factory=lambda: f"VAL-{str(uuid4())[:6]}")
    rule_id: str = ""
    rule_name: str = ""
    status: ValidationStatus = ValidationStatus.PENDING
    records_checked: int = 0
    records_passed: int = 0
    records_failed: int = 0
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    executed_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def pass_rate(self) -> float:
        if self.records_checked == 0:
            return 0.0
        return self.records_passed / self.records_checked * 100


@dataclass
class RegulatoryReport:
    """Regulatory report instance."""
    report_id: str = field(default_factory=lambda: f"RPT-{str(uuid4())[:6]}")
    framework: RegulatoryFramework = RegulatoryFramework.GDPR
    report_type: ReportType = ReportType.ROPA
    title: str = ""
    period: str = ""
    data: dict[str, Any] = field(default_factory=dict)
    state: SubmissionState = SubmissionState.DRAFT
    state_history: list[dict[str, Any]] = field(default_factory=list)
    validation_results: list[ValidationResult] = field(default_factory=list)
    submission_confirmation: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    submitted_at: Optional[datetime] = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def update_state(self, new_state: SubmissionState) -> bool:
        valid_transitions = {
            SubmissionState.DRAFT: [SubmissionState.IN_REVIEW, SubmissionState.REVISION],
            SubmissionState.IN_REVIEW: [SubmissionState.APPROVED, SubmissionState.REVISION],
            SubmissionState.APPROVED: [SubmissionState.FORMATTED],
            SubmissionState.FORMATTED: [SubmissionState.SUBMITTED],
            SubmissionState.SUBMITTED: [SubmissionState.CONFIRMED, SubmissionState.REJECTED],
            SubmissionState.CONFIRMED: [SubmissionState.ARCHIVED],
            SubmissionState.REJECTED: [SubmissionState.REVISION],
            SubmissionState.REVISION: [SubmissionState.IN_REVIEW],
        }
        allowed = valid_transitions.get(self.state, [])
        if new_state in allowed:
            self.state = new_state
            self.state_history.append({
                "state": new_state.value,
                "timestamp": datetime.utcnow().isoformat(),
            })
            return True
        return False

    @property
    def validation_pass_rate(self) -> float:
        if not self.validation_results:
            return 0.0
        total_checked = sum(v.records_checked for v in self.validation_results)
        total_passed = sum(v.records_passed for v in self.validation_results)
        return total_passed / total_checked * 100 if total_checked > 0 else 0.0

    @property
    def has_errors(self) -> bool:
        return any(v.status == ValidationStatus.FAILED for v in self.validation_results)


@dataclass
class SubmissionRecord:
    """Record of a report submission."""
    submission_id: str = field(default_factory=lambda: f"SUB-{str(uuid4())[:6]}")
    report_id: str = ""
    framework: RegulatoryFramework = RegulatoryFramework.GDPR
    channel: SubmissionChannel = SubmissionChannel.PORTAL
    submitted_by: str = ""
    submitted_at: datetime = field(default_factory=datetime.utcnow)
    confirmation_code: str = ""
    status: str = "submitted"  # submitted, confirmed, rejected, error
    response_data: dict[str, Any] = field(default_factory=dict)


# ─── Core Classes ────────────────────────────────────────────────────────────

class DataCollector:
    """Collects data from various sources for regulatory reporting."""

    def __init__(self) -> None:
        self.sources: dict[str, DataSource] = {}

    def register_source(self, source: DataSource) -> None:
        self.sources[source.source_id] = source

    def collect_from_source(self, source_id: str,
                            parameters: dict[str, Any] | None = None) -> dict[str, Any]:
        source = self.sources.get(source_id)
        if not source:
            return {"error": f"Source {source_id} not found"}

        source.last_refreshed = datetime.utcnow()
        return {
            "source_id": source_id,
            "source_name": source.name,
            "system": source.system,
            "collected_at": datetime.utcnow().isoformat(),
            "record_count": 0,
            "status": "collected",
        }

    def collect_all(self) -> list[dict[str, Any]]:
        results = []
        for source_id in self.sources:
            results.append(self.collect_from_source(source_id))
        return results

    def get_stale_sources(self, max_age_hours: int = 24) -> list[DataSource]:
        cutoff = datetime.utcnow() - timedelta(hours=max_age_hours)
        return [
            s for s in self.sources.values()
            if s.last_refreshed is None or s.last_refreshed < cutoff
        ]


class ValidationEngine:
    """Multi-layer data validation engine."""

    def __init__(self) -> None:
        self.rules: dict[str, ValidationRule] = {}

    def add_rule(self, rule: ValidationRule) -> None:
        self.rules[rule.rule_id] = rule

    def validate(self, data: dict[str, Any],
                 framework: RegulatoryFramework | None = None) -> list[ValidationResult]:
        results = []
        target_rules = self.rules.values()
        if framework:
            target_rules = [r for r in target_rules if r.framework == framework]

        for rule in target_rules:
            result = self._execute_rule(rule, data)
            results.append(result)
        return results

    def _execute_rule(self, rule: ValidationRule,
                      data: dict[str, Any]) -> ValidationResult:
        result = ValidationResult(rule_id=rule.rule_id, rule_name=rule.name)
        field_value = data.get(rule.field)

        if rule.rule_type == "completeness":
            if field_value is None or field_value == "":
                result.status = ValidationStatus.FAILED
                result.errors.append(f"Field '{rule.field}' is required but missing")
                result.records_checked = 1
            else:
                result.status = ValidationStatus.PASSED
                result.records_checked = 1
                result.records_passed = 1
        elif rule.rule_type == "range":
            min_val = rule.parameters.get("min", float("-inf"))
            max_val = rule.parameters.get("max", float("inf"))
            result.records_checked = 1
            if field_value is not None and min_val <= field_value <= max_val:
                result.status = ValidationStatus.PASSED
                result.records_passed = 1
            else:
                result.status = ValidationStatus.FAILED
                result.errors.append(
                    f"Field '{rule.field}' value {field_value} "
                    f"not in range [{min_val}, {max_val}]"
                )
        elif rule.rule_type == "format":
            import re
            pattern = rule.parameters.get("pattern", ".*")
            result.records_checked = 1
            if field_value and re.match(pattern, str(field_value)):
                result.status = ValidationStatus.PASSED
                result.records_passed = 1
            else:
                result.status = ValidationStatus.FAILED
                result.errors.append(
                    f"Field '{rule.field}' does not match pattern '{pattern}'"
                )
        elif rule.rule_type == "threshold":
            threshold = rule.parameters.get("threshold", 0)
            direction = rule.parameters.get("direction", "max")
            result.records_checked = 1
            if field_value is not None:
                if (direction == "max" and field_value <= threshold) or \
                   (direction == "min" and field_value >= threshold):
                    result.status = ValidationStatus.PASSED
                    result.records_passed = 1
                else:
                    result.status = ValidationStatus.WARNING
                    result.warnings.append(
                        f"Field '{rule.field}' value {field_value} "
                        f"exceeds threshold {threshold}"
                    )
                    result.records_passed = 1
            else:
                result.status = ValidationStatus.PASSED
                result.records_passed = 1
        else:
            result.status = ValidationStatus.PASSED
            result.records_checked = 1
            result.records_passed = 1

        return result

    def get_rules_by_framework(self, framework: RegulatoryFramework) -> list[ValidationRule]:
        return [r for r in self.rules.values() if r.framework == framework]

    def get_rules_by_dimension(self, dimension: DataQualityDimension) -> list[ValidationRule]:
        return [r for r in self.rules.values() if r.dimension == dimension]


class SubmissionManager:
    """Manages report submission workflow."""

    def __init__(self) -> None:
        self.submissions: dict[str, SubmissionRecord] = {}

    def submit_report(self, report: RegulatoryReport,
                      submitted_by: str,
                      channel: SubmissionChannel | None = None) -> SubmissionRecord:
        actual_channel = channel or SubmissionChannel.PORTAL
        submission = SubmissionRecord(
            report_id=report.report_id,
            framework=report.framework,
            channel=actual_channel,
            submitted_by=submitted_by,
            confirmation_code=f"CONF-{uuid4().hex[:12].upper()}",
        )
        report.submitted_at = datetime.utcnow()
        report.update_state(SubmissionState.SUBMITTED)
        self.submissions[submission.submission_id] = submission
        return submission

    def confirm_submission(self, submission_id: str,
                           confirmation_data: dict[str, Any] | None = None) -> bool:
        submission = self.submissions.get(submission_id)
        if not submission:
            return False
        submission.status = "confirmed"
        submission.response_data = confirmation_data or {}
        return True

    def get_submissions_by_framework(self, framework: RegulatoryFramework) -> list[SubmissionRecord]:
        return [s for s in self.submissions.values() if s.framework == framework]

    def get_pending_confirmations(self) -> list[SubmissionRecord]:
        return [s for s in self.submissions.values() if s.status == "submitted"]


class ReportingCalendar:
    """Manages regulatory reporting deadlines and calendar."""

    DEADLINE_TEMPLATES: dict[ReportType, dict[str, Any]] = {
        ReportType.ROPA: {"recurrence": "continuous", "framework": RegulatoryFramework.GDPR},
        ReportType.DPIA: {"recurrence": "event_driven", "framework": RegulatoryFramework.GDPR},
        ReportType.BREACH_NOTIFICATION: {"recurrence": "event_driven", "framework": RegulatoryFramework.GDPR, "sla_hours": 72},
        ReportType.SECTION_302: {"recurrence": "quarterly", "framework": RegulatoryFramework.SOX, "days_after_period": 40},
        ReportType.SECTION_404: {"recurrence": "annual", "framework": RegulatoryFramework.SOX, "days_after_period": 60},
        ReportType.SECURITY_RISK_ASSESSMENT: {"recurrence": "annual", "framework": RegulatoryFramework.HIPAA},
        ReportType.HIPAA_BREACH: {"recurrence": "event_driven", "framework": RegulatoryFramework.HIPAA, "days_after": 60},
        ReportType.CAPITAL_ADEQUACY: {"recurrence": "quarterly", "framework": RegulatoryFramework.BASEL_III, "days_after_period": 30},
        ReportType.LCR: {"recurrence": "monthly", "framework": RegulatoryFramework.BASEL_III, "days_after_period": 30},
        ReportType.LARGE_EXPOSURE: {"recurrence": "quarterly", "framework": RegulatoryFramework.BASEL_III, "days_after_period": 30},
    }

    def __init__(self) -> None:
        self.deadlines: list[ReportingDeadline] = []

    def add_deadline(self, deadline: ReportingDeadline) -> None:
        self.deadlines.append(deadline)

    def get_upcoming(self, within_days: int = 30) -> list[ReportingDeadline]:
        cutoff = datetime.utcnow() + timedelta(days=within_days)
        return sorted(
            [d for d in self.deadlines if d.due_date <= cutoff],
            key=lambda d: d.due_date,
        )

    def get_overdue(self) -> list[ReportingDeadline]:
        return [d for d in self.deadlines if d.is_overdue]

    def get_by_framework(self, framework: RegulatoryFramework) -> list[ReportingDeadline]:
        return [d for d in self.deadlines if d.framework == framework]

    def create_standard_calendar(self, fiscal_year_end: int = 12) -> None:
        now = datetime.utcnow()
        year = now.year

        # GDPR deadlines
        self.add_deadline(ReportingDeadline(
            framework=RegulatoryFramework.GDPR,
            report_type=ReportType.ROPA,
            description="Annual Records of Processing Activities update",
            due_date=datetime(year, 3, 31),
            recurrence="annual",
        ))

        # SOX deadlines
        for quarter_end_month in [3, 6, 9, 12]:
            days_after = 40 if quarter_end_month < 12 else 60
            due = datetime(year + 1 if quarter_end_month == 12 else year,
                           quarter_end_month + 1 + (1 if quarter_end_month == 12 else 0),
                           1) + timedelta(days=days_after)
            self.add_deadline(ReportingDeadline(
                framework=RegulatoryFramework.SOX,
                report_type=ReportType.SECTION_302 if quarter_end_month < 12 else ReportType.SECTION_404,
                description=f"{'Q' + str(quarter_end_month // 3) if quarter_end_month < 12 else 'Annual'} filing",
                due_date=due,
                recurrence="quarterly" if quarter_end_month < 12 else "annual",
            ))

        # HIPAA
        self.add_deadline(ReportingDeadline(
            framework=RegulatoryFramework.HIPAA,
            report_type=ReportType.SECURITY_RISK_ASSESSMENT,
            description="Annual HIPAA Security Risk Assessment",
            due_date=datetime(year, 12, 31),
            recurrence="annual",
        ))

        # Basel III
        for q_end_month in [3, 6, 9, 12]:
            due = datetime(year + 1 if q_end_month == 12 else year,
                           q_end_month + 1 + (1 if q_end_month == 12 else 0),
                           1) + timedelta(days=30)
            self.add_deadline(ReportingDeadline(
                framework=RegulatoryFramework.BASEL_III,
                report_type=ReportType.CAPITAL_ADEQUACY,
                description=f"Q{q_end_month // 3} Capital Adequacy Report",
                due_date=due,
                recurrence="quarterly",
            ))


class RegulatoryReportGenerator:
    """Orchestrates the full regulatory reporting pipeline."""

    def __init__(self) -> None:
        self.collector = DataCollector()
        self.validator = ValidationEngine()
        self.submission_manager = SubmissionManager()
        self.calendar = ReportingCalendar()
        self.reports: dict[str, RegulatoryReport] = {}

    def generate_report(self, framework: RegulatoryFramework,
                        report_type: ReportType, title: str,
                        period: str, data: dict[str, Any]) -> RegulatoryReport:
        report = RegulatoryReport(
            framework=framework,
            report_type=report_type,
            title=title,
            period=period,
            data=data,
        )

        validation_results = self.validator.validate(data, framework)
        report.validation_results = validation_results
        self.reports[report.report_id] = report

        return report

    def get_reports_by_framework(self, framework: RegulatoryFramework) -> list[RegulatoryReport]:
        return [r for r in self.reports.values() if r.framework == framework]

    def get_draft_reports(self) -> list[RegulatoryReport]:
        return [r for r in self.reports.values() if r.state == SubmissionState.DRAFT]

    def get_submission_stats(self) -> dict[str, Any]:
        total = len(self.reports)
        submitted = sum(1 for r in self.reports.values() if r.state == SubmissionState.SUBMITTED)
        confirmed = sum(1 for r in self.reports.values() if r.state == SubmissionState.CONFIRMED)
        by_framework: dict[str, int] = {}
        for r in self.reports.values():
            key = r.framework.value
            by_framework[key] = by_framework.get(key, 0) + 1
        return {
            "total_reports": total,
            "submitted": submitted,
            "confirmed": confirmed,
            "by_framework": by_framework,
        }


# ─── Demo ────────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate automated regulatory reporting system."""
    print("=" * 70)
    print("AUTOMATED REGULATORY REPORTING SYSTEM")
    print("=" * 70)

    generator = RegulatoryReportGenerator()

    # 1. Data Sources
    print("\n[1] Data Source Registration")
    print("-" * 40)
    sources = [
        DataSource(name="ERP Financial Data", system="SAP",
                   connection_type="api", endpoint="https://sap.internal/api/financial"),
        DataSource(name="HR Employee Records", system="Workday",
                   connection_type="api", endpoint="https://workday.internal/api/hr"),
        DataSource(name="Security Logs", system="Splunk",
                   connection_type="database", endpoint="splunk://security-logs"),
    ]
    for src in sources:
        generator.collector.register_source(src)
        print(f"  Registered: {src.name} ({src.system})")

    collection_results = generator.collector.collect_all()
    print(f"  Collected from {len(collection_results)} sources")

    stale = generator.collector.get_stale_sources(max_age_hours=0)
    print(f"  Stale sources: {len(stale)}")

    # 2. Validation Rules
    print("\n[2] Validation Rules")
    print("-" * 40)
    rules = [
        ValidationRule(name="Capital Ratio Minimum", description="CET1 >= 4.5%",
                       dimension=DataQualityDimension.ACCURACY, rule_type="range",
                       field="cet1_ratio", parameters={"min": 4.5, "max": 100},
                       framework=RegulatoryFramework.BASEL_III),
        ValidationRule(name="Breach Notification SLA", description="Must report within 72h",
                       dimension=DataQualityDimension.TIMELINESS, rule_type="threshold",
                       field="hours_since_breach", parameters={"threshold": 72, "direction": "max"},
                       framework=RegulatoryFramework.GDPR),
        ValidationRule(name="Financial Data Required", description="Revenue data required",
                       dimension=DataQualityDimension.COMPLETENESS, rule_type="completeness",
                       field="revenue", framework=RegulatoryFramework.SOX),
        ValidationRule(name="Employee Count", description="Must have employee count",
                       dimension=DataQualityDimension.COMPLETENESS, rule_type="completeness",
                       field="employee_count", framework=RegulatoryFramework.HIPAA),
    ]
    for rule in rules:
        generator.validator.add_rule(rule)
        print(f"  Rule: {rule.name} ({rule.framework.value})")

    # 3. Report Generation with Validation
    print("\n[3] Report Generation & Validation")
    print("-" * 40)

    # Basel III report
    basel_data = {"cet1_ratio": 12.5, "tier1_ratio": 14.2, "total_capital_ratio": 16.8}
    basel_report = generator.generate_report(
        RegulatoryFramework.BASEL_III, ReportType.CAPITAL_ADEQUACY,
        "Q2 2025 Capital Adequacy", "2025-Q2", basel_data,
    )
    print(f"  Basel III: {basel_report.report_id}")
    print(f"    Validation pass rate: {basel_report.validation_pass_rate:.0f}%")
    for v in basel_report.validation_results:
        print(f"    {v.rule_name}: {v.status.value}")

    # GDPR report
    gdpr_data = {"hours_since_breach": 48, "data_subjects_affected": 1500}
    gdpr_report = generator.generate_report(
        RegulatoryFramework.GDPR, ReportType.BREACH_NOTIFICATION,
        "Data Breach Notification #47", "2025-07", gdpr_data,
    )
    print(f"  GDPR: {gdpr_report.report_id}")
    print(f"    Validation pass rate: {gdpr_report.validation_pass_rate:.0f}%")
    print(f"    Has errors: {gdpr_report.has_errors}")

    # SOX report with missing data
    sox_data = {"internal_controls_effective": True}
    sox_report = generator.generate_report(
        RegulatoryFramework.SOX, ReportType.SECTION_404,
        "FY2025 Internal Controls Assessment", "2025-FY", sox_data,
    )
    print(f"  SOX: {sox_report.report_id}")
    print(f"    Has errors: {sox_report.has_errors} (missing 'revenue' field)")

    # 4. Reporting Calendar
    print("\n[4] Reporting Calendar")
    print("-" * 40)
    generator.calendar.create_standard_calendar()
    upcoming = generator.calendar.get_upcoming(within_days=365)
    print(f"  Deadlines within 365 days: {len(upcoming)}")
    for dl in upcoming[:4]:
        print(f"    [{dl.framework.value:10s}] {dl.report_type.value:25s} due {dl.due_date.strftime('%Y-%m-%d')} ({dl.days_until_due}d)")

    overdue = generator.calendar.get_overdue()
    print(f"  Overdue deadlines: {len(overdue)}")

    # 5. Submission Workflow
    print("\n[5] Submission Workflow")
    print("-" * 40)

    # Move basel report through workflow
    for state_name in ["IN_REVIEW", "APPROVED", "FORMATTED"]:
        state = SubmissionState(state_name.lower())
        basel_report.update_state(state)
    print(f"  Basel report state: {basel_report.state.value}")

    submission = generator.submission_manager.submit_report(
        basel_report, "compliance_officer", SubmissionChannel.PORTAL,
    )
    print(f"  Submitted: {submission.submission_id}")
    print(f"  Confirmation: {submission.confirmation_code}")
    print(f"  Channel: {submission.channel.value}")

    generator.submission_manager.confirm_submission(submission.submission_id)
    basel_report.update_state(SubmissionState.CONFIRMED)
    print(f"  Confirmed: {basel_report.state.value}")

    # 6. Summary Statistics
    print("\n[6] Summary Statistics")
    print("-" * 40)
    stats = generator.get_submission_stats()
    print(f"  Total reports: {stats['total_reports']}")
    print(f"  Submitted: {stats['submitted']}")
    print(f"  Confirmed: {stats['confirmed']}")
    print(f"  By framework: {stats['by_framework']}")

    for fw in RegulatoryFramework:
        fw_reports = generator.get_reports_by_framework(fw)
        print(f"  {fw.value}: {len(fw_reports)} reports")

    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

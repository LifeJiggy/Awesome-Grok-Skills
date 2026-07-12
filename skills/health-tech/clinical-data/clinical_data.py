"""
Clinical Data - Clinical Trials, REDCap, CDISC, Data Validation, Adverse Events
Comprehensive module for clinical data management workflows.
"""

from __future__ import annotations

import hashlib
import json
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Callable, Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class StudyPhase(Enum):
    """Clinical trial phases."""
    PRECLINICAL = "preclinical"
    PHASE_I = "phase_1"
    PHASE_II = "phase_2"
    PHASE_III = "phase_3"
    PHASE_IV = "phase_4"


class StudyStatus(Enum):
    """Clinical trial status."""
    NOT_YET_RECRUITING = "not_yet_recruiting"
    RECRUITING = "recruiting"
    ENROLLING = "enrolling_by_invitation"
    ACTIVE = "active_not_recruiting"
    COMPLETED = "completed"
    SUSPENDED = "suspended"
    TERMINATED = "terminated"
    WITHDRAWN = "withdrawn"


class AESeverity(Enum):
    """Adverse event severity grades (CTCAE v5.0)."""
    GRADE_1 = 1  # Mild
    GRADE_2 = 2  # Moderate
    GRADE_3 = 3  # Severe
    GRADE_4 = 4  # Life-threatening
    GRADE_5 = 5  # Death


class AECausality(Enum):
    """Adverse event causality assessment."""
    DEFINITELY_RELATED = "definitely_related"
    PROBABLY_RELATED = "probably_related"
    POSSIBLY_RELATED = "possibly_related"
    UNLIKELY_RELATED = "unlikely_related"
    NOT_RELATED = "not_related"


class AEOutcome(Enum):
    """Outcome of an adverse event."""
    RECOVERED = "recovered"
    RECOVERING = "recovering"
    NOT_RECOVERED = "not_recovered"
    RECOVERED_WITH_SEQUELAE = "recovered_with_sequelae"
    FATAL = "fatal"
    UNKNOWN = "unknown"


class QueryStatus(Enum):
    """Data query lifecycle states."""
    OPEN = "open"
    ANSWERED = "answered"
    CLOSED = "closed"
    REJECTED = "rejected"


class QueryType(Enum):
    """Types of data validation queries."""
    MISSING = "missing"
    OUT_OF_RANGE = "out_of_range"
    CROSS_FIELD = "cross_field"
    LOGIC = "logic"
    PROTOCOL_DEVIATION = "protocol_deviation"
    CODED = "coded"


class ValidationSeverity(Enum):
    """Severity of validation errors."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class DataLockStatus(Enum):
    """Database lock status."""
    UNLOCKED = "unlocked"
    FROZEN = "frozen"
    LOCKED = "locked"


# ─── Dataclasses ──────────────────────────────────────────────────────────────

@dataclass
class StudyProtocol:
    """Clinical trial protocol definition."""
    protocol_id: str
    title: str
    phase: StudyPhase
    status: StudyStatus
    sponsor: str
    start_date: datetime
    estimated_end_date: datetime
    target_enrollment: int
    current_enrollment: int = 0
    sites: list[str] = field(default_factory=list)
    inclusion_criteria: list[str] = field(default_factory=list)
    exclusion_criteria: list[str] = field(default_factory=list)

    def enrollment_percent(self) -> float:
        if self.target_enrollment == 0:
            return 0.0
        return (self.current_enrollment / self.target_enrollment) * 100

    def is_enrolling(self) -> bool:
        return self.status in (
            StudyStatus.RECRUITING, StudyStatus.ENROLLING, StudyStatus.ACTIVE
        ) and self.current_enrollment < self.target_enrollment


@dataclass
class Subject:
    """A clinical trial participant."""
    subject_id: str
    study_id: str
    site_id: str
    enrollment_date: datetime
    treatment_arm: str = ""
    age: int = 0
    sex: str = ""
    race: str = ""
    ethnicity: str = ""
    status: str = "active"
    consent_date: Optional[datetime] = None
    last_visit_date: Optional[datetime] = None

    def usubjid(self) -> str:
        """Generate CDISC USUBJID format: STUDYID-SITEID-SUBJID."""
        return f"{self.study_id}-{self.site_id}-{self.subject_id}"


@dataclass
class AdverseEvent:
    """An adverse event record."""
    ae_id: str
    subject_id: str
    study_id: str
    term: str
    preferred_term: str
    soc: str  # System Organ Class
    severity: AESeverity
    causality: AECausality
    outcome: AEOutcome
    start_date: datetime
    end_date: Optional[datetime] = None
    is_serious: bool = False
    is_susar: bool = False
    concomitant_meds: list[str] = field(default_factory=list)
    action_taken: str = ""
    narrative: str = ""

    def to_sdtm_ae(self) -> dict[str, Any]:
        """Convert to SDTM AE domain format."""
        return {
            "STUDYID": self.study_id,
            "USUBJID": f"{self.study_id}-{self.subject_id}",
            "AESEQ": self.ae_id,
            "AETERM": self.term,
            "AEDECOD": self.preferred_term,
            "AEBODSYS": self.soc,
            "AESEV": self.severity.name,
            "AEREL": self.causality.value,
            "AEOUT": self.outcome.value,
            "AESTDTC": self.start_date.strftime("%Y-%m-%d"),
            "AEENDTC": self.end_date.strftime("%Y-%m-%d") if self.end_date else "",
            "AESER": "Y" if self.is_serious else "N",
            "AESEREA": "Y" if self.is_susar else "",
        }


@dataclass
class LabResult:
    """A laboratory result record."""
    lab_id: str
    subject_id: str
    study_id: str
    visit: str
    test_name: str
    test_code: str
    result_value: float
    result_unit: str
    normal_low: float
    normal_high: float
    collection_date: datetime
    abnormal_flag: str = ""

    def __post_init__(self) -> None:
        if not self.abnormal_flag:
            if self.result_value < self.normal_low:
                self.abnormal_flag = "LOW"
            elif self.result_value > self.normal_high:
                self.abnormal_flag = "HIGH"
            else:
                self.abnormal_flag = "NORMAL"

    def is_abnormal(self) -> bool:
        return self.abnormal_flag != "NORMAL"

    def percent_change_from_normal(self) -> float:
        mid = (self.normal_low + self.normal_high) / 2
        if mid == 0:
            return 0.0
        return abs(self.result_value - mid) / mid * 100


@dataclass
class DataQuery:
    """A data validation query."""
    query_id: str
    record_id: str
    field_name: str
    query_type: QueryType
    severity: ValidationSeverity
    message: str
    status: QueryStatus = QueryStatus.OPEN
    created_at: datetime = field(default_factory=datetime.utcnow)
    answered_at: Optional[datetime] = None
    answer: str = ""
    query_history: list[dict[str, str]] = field(default_factory=list)

    def close(self, answer: str) -> None:
        self.status = QueryStatus.CLOSED
        self.answer = answer
        self.answered_at = datetime.utcnow()
        self.query_history.append({
            "action": "closed",
            "answer": answer,
            "timestamp": self.answered_at.isoformat(),
        })


@dataclass
class REDCapRecord:
    """A REDCap-style data record."""
    record_id: str
    project_id: str
    redcap_event_name: str = ""
    fields: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    modified_at: datetime = field(default_factory=datetime.utcnow)
    exported: bool = False

    def to_odm(self) -> dict[str, Any]:
        """Export as ODM XML-like structure."""
        return {
            "ClinicalData": {
                "StudyOID": self.project_id,
                "MetaDataVersionOID": "v1.0",
                "SubjectData": {
                    "SubjectKey": self.record_id,
                    "StudyEvent": {
                        "StudyEventOID": self.redcap_event_name,
                        "FormData": [
                            {
                                "FormOID": field_name,
                                "ItemGroupData": {"ItemData": value},
                            }
                            for field_name, value in self.fields.items()
                        ],
                    },
                },
            }
        }


@dataclass
class ValidationRule:
    """A data validation rule definition."""
    rule_id: str
    field_name: str
    rule_type: str  # range, required, cross_field, regex, custom
    parameters: dict[str, Any] = field(default_factory=dict)
    error_message: str = ""
    severity: ValidationSeverity = ValidationSeverity.ERROR

    def evaluate(self, value: Any, record: dict[str, Any] | None = None) -> tuple[bool, str]:
        """Evaluate a validation rule against a value."""
        if self.rule_type == "required":
            if value is None or value == "":
                return False, self.error_message or f"{self.field_name} is required"

        elif self.rule_type == "range":
            if value is None:
                return True, ""
            try:
                num_val = float(value)
                low = self.parameters.get("min", float("-inf"))
                high = self.parameters.get("max", float("inf"))
                if not (low <= num_val <= high):
                    return False, self.error_message or f"{self.field_name} outside range [{low}, {high}]"
            except (TypeError, ValueError):
                return False, f"{self.field_name} must be numeric"

        elif self.rule_type == "regex":
            if value and not re.match(self.parameters.get("pattern", ""), str(value)):
                return False, self.error_message or f"{self.field_name} format invalid"

        elif self.rule_type == "cross_field" and record:
            compare_field = self.parameters.get("compare_field", "")
            op = self.parameters.get("operator", "gt")
            compare_val = record.get(compare_field)
            if value is not None and compare_val is not None:
                try:
                    v1, v2 = float(value), float(compare_val)
                    ops = {"gt": v1 > v2, "lt": v1 < v2, "eq": v1 == v2, "neq": v1 != v2}
                    if not ops.get(op, True):
                        return False, self.error_message or f"{self.field_name} must be {op} {compare_field}"
                except (TypeError, ValueError):
                    pass

        return True, ""


# ─── Service Classes ──────────────────────────────────────────────────────────

class REDCapProject:
    """Simulated REDCap project management."""

    def __init__(self, project_id: str, title: str) -> None:
        self.project_id = project_id
        self.title = title
        self._records: dict[str, REDCapRecord] = {}
        self._metadata: dict[str, dict[str, Any]] = {}
        self._audit_trail: list[dict[str, Any]] = []

    def define_field(
        self,
        field_name: str,
        field_type: str,
        label: str,
        required: bool = False,
        validation: str = "",
        choices: list[dict[str, str]] | None = None,
    ) -> None:
        """Define a project field (REDCap metadata)."""
        self._metadata[field_name] = {
            "field_name": field_name,
            "field_type": field_type,
            "field_label": label,
            "field_required": "y" if required else "n",
            "text_validation_type": validation,
            "select_choices_or_calculations": choices or [],
        }

    def import_record(self, record: REDCapRecord) -> str:
        """Import a data record."""
        record.project_id = self.project_id
        self._records[record.record_id] = record
        self._log_audit("import", record.record_id)
        return record.record_id

    def export_records(
        self, records: Optional[list[str]] = None, fields: Optional[list[str]] = None
    ) -> list[dict[str, Any]]:
        """Export records with optional field filtering."""
        target_records = self._records.values()
        if records:
            target_records = [r for r in target_records if r.record_id in records]

        results = []
        for record in target_records:
            if fields:
                filtered_fields = {k: v for k, v in record.fields.items() if k in fields}
            else:
                filtered_fields = record.fields
            results.append({
                "record_id": record.record_id,
                "project_id": record.project_id,
                **filtered_fields,
            })
        return results

    def deidentify_record(self, record_id: str) -> Optional[REDCapRecord]:
        """Remove PHI from a record for de-identification."""
        record = self._records.get(record_id)
        if not record:
            return None

        anon_record = REDCapRecord(
            record_id=f"ANON-{hashlib.sha256(record_id.encode()).hexdigest()[:8]}",
            project_id=record.project_id,
            redcap_event_name=record.redcap_event_name,
            fields={},
            metadata=record.metadata.copy(),
        )

        phi_fields = {"name", "dob", "ssn", "address", "phone", "email", "mrn", "medical_record_number"}
        for key, value in record.fields.items():
            if any(phi in key.lower() for phi in phi_fields):
                anon_record.fields[key] = "[REDACTED]"
            else:
                anon_record.fields[key] = value
        return anon_record

    def get_record_count(self) -> int:
        return len(self._records)

    def _log_audit(self, action: str, record_id: str) -> None:
        self._audit_trail.append({
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "record_id": record_id,
        })


class DataValidator:
    """Clinical data validation engine."""

    def __init__(self) -> None:
        self._rules: dict[str, list[ValidationRule]] = {}
        self._queries: list[DataQuery] = []

    def add_rule(self, field_name: str, rule: ValidationRule) -> None:
        """Add a validation rule for a field."""
        self._rules.setdefault(field_name, []).append(rule)

    def validate_record(self, record: dict[str, Any]) -> list[DataQuery]:
        """Validate a data record against all rules, generating queries for failures."""
        new_queries: list[DataQuery] = []

        for field_name, rules in self._rules.items():
            value = record.get(field_name)
            for rule in rules:
                passes, message = rule.evaluate(value, record)
                if not passes:
                    query = DataQuery(
                        query_id=f"Q-{uuid.uuid4().hex[:8]}",
                        record_id=record.get("record_id", "unknown"),
                        field_name=field_name,
                        query_type=QueryType(rule.rule_type if rule.rule_type in
                                            [e.value for e in QueryType] else "logic"),
                        severity=rule.severity,
                        message=message,
                    )
                    new_queries.append(query)
                    self._queries.append(query)
        return new_queries

    def get_open_queries(self) -> list[DataQuery]:
        return [q for q in self._queries if q.status == QueryStatus.OPEN]

    def close_query(self, query_id: str, answer: str) -> bool:
        for q in self._queries:
            if q.query_id == query_id:
                q.close(answer)
                return True
        return False

    def get_query_summary(self) -> dict[str, Any]:
        by_status: dict[str, int] = {}
        by_severity: dict[str, int] = {}
        for q in self._queries:
            by_status[q.status.value] = by_status.get(q.status.value, 0) + 1
            by_severity[q.severity.value] = by_severity.get(q.severity.value, 0) + 1
        return {"total": len(self._queries), "by_status": by_status, "by_severity": by_severity}


class AdverseEventManager:
    """Manages adverse event collection, coding, and reporting."""

    def __init__(self) -> None:
        self._events: dict[str, AdverseEvent] = {}
        self._suscritera_threshold: int = 2

    def report_ae(
        self,
        subject_id: str,
        study_id: str,
        term: str,
        preferred_term: str,
        soc: str,
        severity: AESeverity,
        causality: AECausality,
        outcome: AEOutcome,
        start_date: datetime,
        is_serious: bool = False,
    ) -> AdverseEvent:
        """Report a new adverse event."""
        ae = AdverseEvent(
            ae_id=f"AE-{uuid.uuid4().hex[:8]}",
            subject_id=subject_id,
            study_id=study_id,
            term=term,
            preferred_term=preferred_term,
            soc=soc,
            severity=severity,
            causality=causality,
            outcome=outcome,
            start_date=start_date,
            is_serious=is_serious,
        )
        if is_serious and severity in (AESeverity.GRADE_3, AESeverity.GRADE_4, AESeverity.GRADE_5):
            ae.is_susar = True

        self._events[ae.ae_id] = ae
        return ae

    def get_study_ae_summary(self, study_id: str) -> dict[str, Any]:
        """Get adverse event summary for a study."""
        study_aes = [ae for ae in self._events.values() if ae.study_id == study_id]
        total = len(study_aes)
        if total == 0:
            return {"total": 0}

        severity_counts: dict[int, int] = {}
        seriousness_count = 0
        susar_count = 0
        soc_counts: dict[str, int] = {}

        for ae in study_aes:
            severity_counts[ae.severity.value] = severity_counts.get(ae.severity.value, 0) + 1
            if ae.is_serious:
                seriousness_count += 1
            if ae.is_susar:
                susar_count += 1
            soc_counts[ae.soc] = soc_counts.get(ae.soc, 0) + 1

        return {
            "total_aes": total,
            "severity_distribution": {f"grade_{k}": v for k, v in severity_counts.items()},
            "serious_aes": seriousness_count,
            "susars": susar_count,
            "by_soc": soc_counts,
        }

    def generate_susar_report(self, study_id: str) -> list[dict[str, Any]]:
        """Generate SUSARs requiring expedited reporting."""
        susars = [
            ae.to_sdtm_ae()
            for ae in self._events.values()
            if ae.study_id == study_id and ae.is_susar
        ]
        return susars

    def get_subject_ae_history(self, subject_id: str) -> list[dict[str, Any]]:
        """Get complete AE history for a subject."""
        return [
            {
                "ae_id": ae.ae_id,
                "term": ae.preferred_term,
                "severity": ae.severity.value,
                "causality": ae.causality.value,
                "outcome": ae.outcome.value,
                "start_date": ae.start_date.isoformat(),
                "serious": ae.is_serious,
            }
            for ae in self._events.values()
            if ae.subject_id == subject_id
        ]


class CDISCDatasetBuilder:
    """Builds CDISC SDTM and ADaM datasets from clinical data."""

    def __init__(self) -> None:
        self._sdtm_domains: dict[str, list[dict[str, Any]]] = {}
        self._adam_datasets: dict[str, list[dict[str, Any]]] = {}

    def build_dm_domain(self, subjects: list[Subject]) -> list[dict[str, Any]]:
        """Build Demographics (DM) SDTM domain."""
        rows = []
        for subj in subjects:
            rows.append({
                "STUDYID": subj.study_id,
                "DOMAIN": "DM",
                "USUBJID": subj.usubjid(),
                "SUBJID": subj.subject_id,
                "RFSTDTC": subj.enrollment_date.strftime("%Y-%m-%d"),
                "AGE": subj.age,
                "SEX": subj.sex,
                "RACE": subj.race,
                "ETHNIC": subj.ethnicity,
            })
        self._sdtm_domains["DM"] = rows
        return rows

    def build_lb_domain(self, labs: list[LabResult]) -> list[dict[str, Any]]:
        """Build Laboratory (LB) SDTM domain."""
        rows = []
        for lab in labs:
            rows.append({
                "STUDYID": lab.study_id,
                "DOMAIN": "LB",
                "USUBJID": f"{lab.study_id}-{lab.subject_id}",
                "LBTEST": lab.test_name,
                "LBTESTCD": lab.test_code,
                "LBORRES": str(lab.result_value),
                "LBORRESU": lab.result_unit,
                "LBORNRLO": str(lab.normal_low),
                "LBORNRHI": str(lab.normal_high),
                "LBFLAG": lab.abnormal_flag,
                "LBDTC": lab.collection_date.strftime("%Y-%m-%d"),
            })
        self._sdtm_domains["LB"] = rows
        return rows

    def build_ae_domain(self, events: list[AdverseEvent]) -> list[dict[str, Any]]:
        """Build Adverse Events (AE) SDTM domain."""
        rows = [ae.to_sdtm_ae() for ae in events]
        self._sdtm_domains["AE"] = rows
        return rows

    def build_adsl(self, subjects: list[Subject]) -> list[dict[str, Any]]:
        """Build ADSL (Subject-Level Analysis) ADaM dataset."""
        rows = []
        for subj in subjects:
            rows.append({
                "STUDYID": subj.study_id,
                "USUBJID": subj.usubjid(),
                "SUBJID": subj.subject_id,
                "TRT01P": subj.treatment_arm,
                "AGEGR1": ">=65" if subj.age >= 65 else "<65",
                "SEX": subj.sex,
                "RACE": subj.race,
                "ITTFL": "Y",
                "SAFFL": "Y",
                "ENROLLDT": subj.enrollment_date.strftime("%Y-%m-%d"),
            })
        self._adam_datasets["ADSL"] = rows
        return rows

    def build_adae(self, events: list[AdverseEvent]) -> list[dict[str, Any]]:
        """Build ADAE (Adverse Events Analysis) ADaM dataset."""
        rows = []
        for ae in events:
            rows.append({
                "STUDYID": ae.study_id,
                "USUBJID": f"{ae.study_id}-{ae.subject_id}",
                "AESEQ": ae.ae_id,
                "AETERM": ae.term,
                "AEDECOD": ae.preferred_term,
                "AEBODSYS": ae.soc,
                "AESEV": ae.severity.name,
                "AEREL": ae.causality.value,
                "AESER": "Y" if ae.is_serious else "N",
                "DTHAET": "Y" if ae.outcome == AEOutcome.FATAL else "N",
                "TRTEMFL": "Y" if ae.causality in (
                    AECausality.DEFINITELY_RELATED,
                    AECausality.PROBABLY_RELATED,
                    AECausality.POSSIBLY_RELATED,
                ) else "",
            })
        self._adam_datasets["ADAE"] = rows
        return rows

    def get_define_xml_metadata(self) -> dict[str, Any]:
        """Generate Define-XML metadata for datasets."""
        metadata: dict[str, Any] = {"datasets": {}}
        for domain, rows in self._sdtm_domains.items():
            if rows:
                metadata["datasets"][domain] = {
                    "variables": list(rows[0].keys()),
                    "record_count": len(rows),
                }
        for dataset, rows in self._adam_datasets.items():
            if rows:
                metadata["datasets"][dataset] = {
                    "variables": list(rows[0].keys()),
                    "record_count": len(rows),
                }
        return metadata


class ClinicalTrialManager:
    """Manages overall clinical trial operations."""

    def __init__(self, protocol: StudyProtocol) -> None:
        self.protocol = protocol
        self._subjects: dict[str, Subject] = {}
        self.ae_manager = AdverseEventManager()
        self.data_validator = DataValidator()
        self.redcap = REDCapProject(protocol.protocol_id, protocol.title)
        self.cdisc_builder = CDISCDatasetBuilder()

    def enroll_subject(
        self,
        subject_id: str,
        site_id: str,
        treatment_arm: str,
        age: int,
        sex: str,
        race: str = "",
        ethnicity: str = "",
    ) -> Subject:
        """Enroll a new subject in the trial."""
        if not self.protocol.is_enrolling():
            raise ValueError("Study is not currently enrolling")

        for criterion in self.protocol.exclusion_criteria:
            if self._check_exclusion(criterion, age, sex):
                raise ValueError(f"Subject excluded: {criterion}")

        subject = Subject(
            subject_id=subject_id,
            study_id=self.protocol.protocol_id,
            site_id=site_id,
            enrollment_date=datetime.utcnow(),
            treatment_arm=treatment_arm,
            age=age,
            sex=sex,
            race=race,
            ethnicity=ethnicity,
        )
        self._subjects[subject_id] = subject
        self.protocol.current_enrollment += 1
        return subject

    def get_enrollment_status(self) -> dict[str, Any]:
        return {
            "protocol_id": self.protocol.protocol_id,
            "target": self.protocol.target_enrollment,
            "current": self.protocol.current_enrollment,
            "percent": self.protocol.enrollment_percent(),
            "is_enrolling": self.protocol.is_enrolling(),
        }

    def get_cdisc_export(self) -> dict[str, Any]:
        """Export all trial data in CDISC format."""
        subjects = list(self._subjects.values())
        aes = list(self.ae_manager._events.values())

        dm = self.cdisc_builder.build_dm_domain(subjects)
        ae_domain = self.cdisc_builder.build_ae_domain(aes)
        adsl = self.cdisc_builder.build_adsl(subjects)
        adae = self.cdisc_builder.build_adae(aes)

        return {
            "SDTM": {"DM": dm, "AE": ae_domain},
            "ADaM": {"ADSL": adsl, "ADAE": adae},
        }

    def _check_exclusion(self, criterion: str, age: int, sex: str) -> bool:
        criterion_lower = criterion.lower()
        if "age" in criterion_lower and "<" in criterion_lower:
            match = re.search(r"<\s*(\d+)", criterion_lower)
            if match and age < int(match.group(1)):
                return True
        if "sex" in criterion_lower:
            if sex.lower() not in criterion_lower:
                return True
        return False


# ─── Demo ─────────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate clinical data management capabilities."""
    print("=" * 70)
    print("CLINICAL DATA MANAGEMENT DEMONSTRATION")
    print("=" * 70)

    # 1. Study Protocol
    print("\n── 1. STUDY PROTOCOL ──")
    protocol = StudyProtocol(
        protocol_id="NCT-2024-001",
        title="Phase III Trial of DrugX in Type 2 Diabetes",
        phase=StudyPhase.PHASE_III,
        status=StudyStatus.RECRUITING,
        sponsor="PharmaCo Inc.",
        start_date=datetime(2024, 1, 15),
        estimated_end_date=datetime(2026, 6, 30),
        target_enrollment=300,
        sites=["Site-01", "Site-02", "Site-03"],
        exclusion_criteria=["Age < 18", "Pregnancy"],
    )
    print(f"  Protocol: {protocol.protocol_id} — {protocol.title}")
    print(f"  Phase: {protocol.phase.value} | Status: {protocol.status.value}")
    print(f"  Enrollment: {protocol.enrollment_percent():.0f}% ({protocol.current_enrollment}/{protocol.target_enrollment})")

    # 2. REDCap Project
    print("\n── 2. REDCAP PROJECT ──")
    project = REDCapProject(protocol.protocol_id, protocol.title)
    project.define_field("age", "text", "Age", required=True, validation="integer")
    project.define_field("bp_systolic", "text", "Systolic BP", validation="number")
    project.define_field("hba1c", "text", "HbA1c", validation="number")

    record = REDCapRecord(
        record_id="SUBJ-001",
        project_id=protocol.protocol_id,
        redcap_event_name="Baseline",
        fields={"age": 55, "bp_systolic": 138, "hba1c": 8.2},
    )
    project.import_record(record)
    print(f"  Records in project: {project.get_record_count()}")

    exported = project.export_records(fields=["age", "hba1c"])
    print(f"  Exported fields: {exported[0] if exported else 'none'}")

    deidentified = project.deidentify_record("SUBJ-001")
    print(f"  De-identified: {deidentified.record_id if deidentified else 'failed'}")

    # 3. Clinical Trial Management
    print("\n── 3. CLINICAL TRIAL MANAGEMENT ──")
    trial = ClinicalTrialManager(protocol)

    subjects = [
        trial.enroll_subject("001", "Site-01", "DrugX", 55, "M", "White"),
        trial.enroll_subject("002", "Site-01", "Placebo", 62, "F", "Black"),
        trial.enroll_subject("003", "Site-02", "DrugX", 48, "M", "Asian"),
        trial.enroll_subject("004", "Site-02", "DrugX", 71, "F", "White"),
        trial.enroll_subject("005", "Site-03", "Placebo", 58, "M", "Hispanic"),
    ]
    print(f"  Enrolled: {len(subjects)} subjects")
    print(f"  Enrollment status: {json.dumps(trial.get_enrollment_status(), indent=4)}")

    # 4. Adverse Events
    print("\n── 4. ADVERSE EVENTS ──")
    ae1 = trial.ae_manager.report_ae(
        "001", protocol.protocol_id, "headache", "Headache",
        "Nervous system disorders", AESeverity.GRADE_1,
        AECausality.POSSIBLY_RELATED, AEOutcome.RECOVERED,
        datetime.now() - timedelta(days=5),
    )
    ae2 = trial.ae_manager.report_ae(
        "002", protocol.protocol_id, "elevated ALT", "Hepatic enzyme increased",
        "Hepatobiliary disorders", AESeverity.GRADE_3,
        AECausality.PROBABLY_RELATED, AEOutcome.RECOVERING,
        datetime.now() - timedelta(days=3), is_serious=True,
    )
    ae3 = trial.ae_manager.report_ae(
        "003", protocol.protocol_id, "nausea", "Nausea",
        "Gastrointestinal disorders", AESeverity.GRADE_2,
        AECausality.DEFINITELY_RELATED, AEOutcome.RECOVERED,
        datetime.now() - timedelta(days=7),
    )
    print(f"  AE reported: {ae1.term} (Grade {ae1.severity.value})")
    print(f"  Serious AE: {ae2.term} (Grade {ae2.severity.value}, SUSAR={ae2.is_susar})")

    summary = trial.ae_manager.get_study_ae_summary(protocol.protocol_id)
    print(f"  AE summary: {json.dumps(summary, indent=4)}")

    susars = trial.ae_manager.generate_susar_report(protocol.protocol_id)
    print(f"  SUSARs requiring expedited report: {len(susars)}")

    # 5. Data Validation
    print("\n── 5. DATA VALIDATION ──")
    validator = DataValidator()
    validator.add_rule("age", ValidationRule(
        "R-AGE", "age", "range", {"min": 18, "max": 99}, "Age must be 18-99"
    ))
    validator.add_rule("hba1c", ValidationRule(
        "R-HBA1C", "hba1c", "range", {"min": 3.0, "max": 20.0}, "HbA1c must be 3-20%"
    ))
    validator.add_rule("bp_systolic", ValidationRule(
        "R-BP", "bp_systolic", "range", {"min": 60, "max": 300}, "BP out of range"
    ))

    test_records = [
        {"record_id": "SUBJ-001", "age": 55, "hba1c": 8.2, "bp_systolic": 138},
        {"record_id": "SUBJ-006", "age": 15, "hba1c": 8.2, "bp_systolic": 130},
        {"record_id": "SUBJ-007", "age": 60, "hba1c": 25.0, "bp_systolic": 125},
    ]

    for rec in test_records:
        queries = validator.validate_record(rec)
        if queries:
            for q in queries:
                print(f"  QUERY [{q.severity.value}]: {q.field_name} — {q.message}")
        else:
            print(f"  Record {rec['record_id']}: PASS")

    print(f"  Query summary: {json.dumps(validator.get_query_summary(), indent=4)}")

    # 6. CDISC Export
    print("\n── 6. CDISC EXPORT ──")
    cdisc = trial.get_cdisc_export()
    for dataset_type, datasets in cdisc.items():
        print(f"  {dataset_type}:")
        for domain, rows in datasets.items():
            print(f"    {domain}: {len(rows)} records")
            if rows:
                print(f"      Variables: {list(rows[0].keys())[:5]}...")

    define_metadata = trial.cdisc_builder.get_define_xml_metadata()
    print(f"  Define-XML datasets: {list(define_metadata['datasets'].keys())}")

    print("\n" + "=" * 70)
    print("CLINICAL DATA MANAGEMENT DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

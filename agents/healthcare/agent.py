"""
Healthcare Agent — Healthcare IT, HL7/FHIR integration, EHR management,
clinical workflows, patient data management, and HIPAA compliance.

This module provides comprehensive healthcare IT tools including:
- HL7 FHIR resource modeling and validation
- Patient record management with PHI protection
- Clinical workflow automation and decision support
- Medication management and drug interaction checking
- Lab result interpretation and trending
- Appointment scheduling and resource management
- Insurance claims processing
- HIPAA compliance auditing
- Clinical terminology (ICD-10, CPT, SNOMED CT)
- Population health analytics
"""

from __future__ import annotations

import hashlib
import logging
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, IntEnum
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    List,
    NamedTuple,
    Optional,
    Protocol,
    Sequence,
    Set,
    Tuple,
    Union,
)

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    UNKNOWN = "unknown"


class PatientStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DECEASED = "deceased"
    ARCHIVED = "archived"


class EncounterType(Enum):
    INPATIENT = "inpatient"
    OUTPATIENT = "outpatient"
    EMERGENCY = "emergency"
    TELEHEALTH = "telehealth"
    HOME_HEALTH = "home_health"
    AMBULATORY = "ambulatory"


class EncounterStatus(Enum):
    PLANNED = "planned"
    ARRIVED = "arrived"
    IN_PROGRESS = "in_progress"
    FINISHED = "finished"
    CANCELLED = "cancelled"
    ON_LEAVE = "on_leave"


class MedicationStatus(Enum):
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    ENTERED_IN_ERROR = "entered_in_error"
    STOPPED = "stopped"


class AllergySeverity(Enum):
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    LIFE_THREATENING = "life_threatening"


class LabStatus(Enum):
    REGISTERED = "registered"
    PRELIMINARY = "preliminary"
    FINAL = "final"
    AMENDED = "amended"
    CORRECTED = "corrected"
    CANCELLED = "cancelled"


class ClaimStatus(Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    CANCELLED = "cancelled"
    ENTERED_IN_ERROR = "entered_in_error"
    CLOSED = "closed"


class AppointmentStatus(Enum):
    PROPOSED = "proposed"
    PENDING = "pending"
    BOOKED = "booked"
    ARRIVED = "arrived"
    FULFILLED = "fulfilled"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class AlertPriority(IntEnum):
    ROUTINE = 0
    URGENT = 1
    ASAP = 2
    STAT = 3


class DiagnosisCategory(Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    ADMITTING = "admitting"
    DISCHARGE = "discharge"
    DIFFERENTIAL = "differential"


class InsuranceType(Enum):
    MEDICARE = "medicare"
    MEDICAID = "medicaid"
    PRIVATE = "private"
    HMO = "hmo"
    PPO = "ppo"
    SELF_PAY = "self_pay"
    TRICARE = "tricare"
    WORKERS_COMP = "workers_comp"


class WorkflowStepType(Enum):
    ASSESSMENT = "assessment"
    ORDER = "order"
    PROCEDURE = "procedure"
    NOTIFICATION = "notification"
    APPROVAL = "approval"
    DOCUMENTATION = "documentation"
    REFERRAL = "referral"
    DISCHARGE = "discharge"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class Address:
    """Patient or provider address."""
    street: List[str] = field(default_factory=list)
    city: str = ""
    state: str = ""
    postal_code: str = ""
    country: str = "US"

    def formatted(self) -> str:
        lines = self.street + [f"{self.city}, {self.state} {self.postal_code}"]
        return ", ".join(l for l in lines if l)


@dataclass
class ContactPoint:
    """Phone, email, or other contact method."""
    system: str = "phone"  # phone, email, fax, pager
    value: str = ""
    use: str = "home"  # home, work, mobile, temp
    preferred: bool = False


@dataclass
class HumanName:
    """Patient or provider name."""
    use: str = "official"  # official, usual, maiden, nickname
    family: str = ""
    given: List[str] = field(default_factory=list)
    prefix: List[str] = field(default_factory=list)
    suffix: List[str] = field(default_factory=list)

    @property
    def full_name(self) -> str:
        parts = self.prefix + self.given + [self.family] + self.suffix
        return " ".join(p for p in parts if p)


@dataclass
class Identifier:
    """Standardized identifier (MRN, NPI, etc.)."""
    system: str = ""
    value: str = ""
    use: str = "usual"  # usual, official, temp, secondary
    type_code: str = ""  # MR, PN, SS, DL, etc.


@dataclass
class Patient:
    """FHIR Patient resource representation."""
    patient_id: str
    identifiers: List[Identifier] = field(default_factory=list)
    name: HumanName = field(default_factory=HumanName)
    gender: Gender = Gender.UNKNOWN
    birth_date: Optional[datetime] = None
    deceased: bool = False
    deceased_date: Optional[datetime] = None
    address: List[Address] = field(default_factory=list)
    contact: List[ContactPoint] = field(default_factory=list)
    status: PatientStatus = PatientStatus.ACTIVE
    marital_status: str = ""
    language: str = "en"
    race: str = ""
    ethnicity: str = ""
    emergency_contacts: List[Dict[str, str]] = field(default_factory=list)
    insurance: List[Dict[str, str]] = field(default_factory=list)
    primary_care_provider: str = ""
    allergies: List[str] = field(default_factory=list)
    conditions: List[str] = field(default_factory=list)
    medications: List[str] = field(default_factory=list)

    @property
    def age(self) -> Optional[int]:
        if not self.birth_date:
            return None
        today = datetime.utcnow()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )

    @property
    def mrn(self) -> Optional[str]:
        for ident in self.identifiers:
            if ident.type_code == "MR":
                return ident.value
        return None

    @property
    def is_active(self) -> bool:
        return self.status == PatientStatus.ACTIVE

    @property
    def full_name(self) -> str:
        return self.name.full_name

    def to_fhir(self) -> Dict[str, Any]:
        return {
            "resourceType": "Patient",
            "id": self.patient_id,
            "identifier": [{"system": i.system, "value": i.value} for i in self.identifiers],
            "name": [{"family": self.name.family, "given": self.name.given}],
            "gender": self.gender.value,
            "birthDate": self.birth_date.isoformat() if self.birth_date else None,
            "active": self.is_active,
        }


@dataclass
class Medication:
    """Medication prescription or order."""
    medication_id: str
    patient_id: str
    medication_name: str
    dosage: str
    frequency: str
    route: str = "oral"
    status: MedicationStatus = MedicationStatus.ACTIVE
    prescriber: str = ""
    start_date: datetime = field(default_factory=datetime.utcnow)
    end_date: Optional[datetime] = None
    refills_remaining: int = 0
    instructions: str = ""
    ndc_code: str = ""

    @property
    def is_active(self) -> bool:
        return self.status == MedicationStatus.ACTIVE

    @property
    def days_remaining(self) -> Optional[int]:
        if not self.end_date:
            return None
        return max((self.end_date - datetime.utcnow()).days, 0)


@dataclass
class Allergy:
    """Patient allergy record."""
    allergy_id: str
    patient_id: str
    substance: str
    reaction: str
    severity: AllergySeverity = AllergySeverity.MODERATE
    onset_date: Optional[datetime] = None
    recorded_date: datetime = field(default_factory=datetime.utcnow)
    clinical_status: str = "active"  # active, inactive, resolved
    verification_status: str = "confirmed"  # confirmed, unconfirmed, refuted

    @property
    def is_active(self) -> bool:
        return self.clinical_status == "active"

    @property
    def is_life_threatening(self) -> bool:
        return self.severity == AllergySeverity.LIFE_THREATENING


@dataclass
class Condition:
    """Patient condition/diagnosis."""
    condition_id: str
    patient_id: str
    code: str  # ICD-10 code
    display: str
    category: DiagnosisCategory = DiagnosisCategory.PRIMARY
    clinical_status: str = "active"
    severity: str = ""
    onset_date: Optional[datetime] = None
    abatement_date: Optional[datetime] = None
    recorded_date: datetime = field(default_factory=datetime.utcnow)
    notes: str = ""

    @property
    def is_active(self) -> bool:
        return self.clinical_status == "active"


@dataclass
class Observation:
    """Lab result or vital sign observation."""
    observation_id: str
    patient_id: str
    code: str
    display: str
    value: float
    unit: str
    status: LabStatus = LabStatus.FINAL
    effective_date: datetime = field(default_factory=datetime.utcnow)
    reference_range_low: Optional[float] = None
    reference_range_high: Optional[float] = None
    interpretation: str = ""  # N, H, L, HH, LL, A
    category: str = "laboratory"

    @property
    def is_normal(self) -> bool:
        if self.reference_range_low is None or self.reference_range_high is None:
            return True
        return self.reference_range_low <= self.value <= self.reference_range_high

    @property
    def is_high(self) -> bool:
        if self.reference_range_high is None:
            return False
        return self.value > self.reference_range_high

    @property
    def is_low(self) -> bool:
        if self.reference_range_low is None:
            return False
        return self.value < self.reference_range_low

    def deviation_from_normal(self) -> Optional[float]:
        if self.reference_range_low is None or self.reference_range_high is None:
            return None
        mid = (self.reference_range_low + self.reference_range_high) / 2
        rng = self.reference_range_high - self.reference_range_low
        if rng == 0:
            return 0.0
        return (self.value - mid) / (rng / 2)

    def trend_direction(self, historical: List[Observation]) -> str:
        if len(historical) < 2:
            return "insufficient_data"
        vals = [o.value for o in sorted(historical, key=lambda x: x.effective_date)]
        if vals[-1] > vals[0] * 1.1:
            return "increasing"
        elif vals[-1] < vals[0] * 0.9:
            return "decreasing"
        return "stable"


@dataclass
class Encounter:
    """Patient encounter/visit."""
    encounter_id: str
    patient_id: str
    encounter_type: EncounterType = EncounterType.OUTPATIENT
    status: EncounterStatus = EncounterStatus.PLANNED
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    provider: str = ""
    department: str = ""
    reason: str = ""
    diagnoses: List[Condition] = field(default_factory=list)
    notes: str = ""
    vitals: Dict[str, float] = field(default_factory=dict)

    @property
    def duration_minutes(self) -> Optional[float]:
        if not self.end_time:
            return None
        return (self.end_time - self.start_time).total_seconds() / 60


@dataclass
class Claim:
    """Insurance claim."""
    claim_id: str
    patient_id: str
    encounter_id: str
    status: ClaimStatus = ClaimStatus.DRAFT
    insurance_type: InsuranceType = InsuranceType.PRIVATE
    diagnosis_codes: List[str] = field(default_factory=list)
    procedure_codes: List[str] = field(default_factory=list)
    total_amount: float = 0.0
    paid_amount: float = 0.0
    patient_responsibility: float = 0.0
    submitted_date: Optional[datetime] = None
    resolved_date: Optional[datetime] = None
    denial_reason: str = ""
    notes: str = ""

    @property
    def is_denied(self) -> bool:
        return bool(self.denial_reason)

    @property
    def outstanding(self) -> float:
        return self.total_amount - self.paid_amount


@dataclass
class Appointment:
    """Scheduled appointment."""
    appointment_id: str
    patient_id: str
    provider: str
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(minutes=30))
    status: AppointmentStatus = AppointmentStatus.BOOKED
    appointment_type: str = ""
    reason: str = ""
    notes: str = ""

    @property
    def duration_minutes(self) -> float:
        return (self.end_time - self.start_time).total_seconds() / 60

    @property
    def is_upcoming(self) -> bool:
        return self.start_time > datetime.utcnow()


@dataclass
class MedicationInteraction:
    """Drug-drug interaction record."""
    drug_a: str
    drug_b: str
    severity: str  # mild, moderate, severe, contraindicated
    description: str
    recommendation: str = ""


@dataclass
class ClinicalAlert:
    """Clinical decision support alert."""
    alert_id: str
    patient_id: str
    alert_type: str  # allergy, drug_interaction, lab_critical, etc.
    priority: AlertPriority = AlertPriority.ROUTINE
    message: str = ""
    triggered_by: str = ""
    acknowledged: bool = False
    acknowledged_by: str = ""
    acknowledged_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_active(self) -> bool:
        return not self.acknowledged


@dataclass
class AuditLogEntry:
    """HIPAA audit log entry."""
    entry_id: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    action: str = ""  # read, write, delete, export
    resource_type: str = ""
    resource_id: str = ""
    user_id: str = ""
    user_role: str = ""
    patient_id: str = ""
    outcome: str = "success"
    ip_address: str = ""
    details: str = ""


@dataclass
class WorkflowStep:
    """Clinical workflow step."""
    step_id: str
    step_type: WorkflowStepType
    description: str
    required: bool = True
    completed: bool = False
    assignee: str = ""
    due_date: Optional[datetime] = None
    notes: str = ""


@dataclass
class ClinicalWorkflow:
    """Clinical workflow definition."""
    workflow_id: str
    name: str
    patient_id: str
    steps: List[WorkflowStep] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: str = "active"  # active, completed, cancelled

    @property
    def completion_pct(self) -> float:
        if not self.steps:
            return 0.0
        completed = sum(1 for s in self.steps if s.completed)
        return completed / len(self.steps)

    @property
    def current_step(self) -> Optional[WorkflowStep]:
        for step in self.steps:
            if not step.completed:
                return step
        return None


@dataclass
class PopulationMetrics:
    """Population health metrics."""
    total_patients: int = 0
    avg_age: float = 0.0
    gender_distribution: Dict[str, int] = field(default_factory=dict)
    top_conditions: List[Tuple[str, int]] = field(default_factory=list)
    top_medications: List[Tuple[str, int]] = field(default_factory=list)
    avg_bmi: float = 0.0
    readmission_rate: float = 0.0
    avg_length_of_stay: float = 0.0


# ---------------------------------------------------------------------------
# Drug Interaction Database
# ---------------------------------------------------------------------------

class DrugInteractionChecker:
    """
    Checks for drug-drug, drug-allergy, and drug-condition interactions.
    """

    def __init__(self) -> None:
        self.interactions: List[MedicationInteraction] = []
        self.allergy_map: Dict[str, List[str]] = {}
        self._build_interaction_db()

    def _build_interaction_db(self) -> None:
        known_interactions = [
            ("warfarin", "aspirin", "severe", "Increased bleeding risk", "Avoid combination or monitor INR closely"),
            ("metformin", "alcohol", "moderate", "Risk of lactic acidosis", "Limit alcohol intake"),
            ("lisinopril", "potassium", "moderate", "Hyperkalemia risk", "Monitor potassium levels"),
            ("simvastatin", "amiodarone", "severe", "Rhabdomyolysis risk", "Reduce simvastatin dose"),
            ("clopidogrel", "omeprazole", "moderate", "Reduced antiplatelet effect", "Use pantoprazole instead"),
            ("methotrexate", "nsaid", "severe", "Increased methotrexate toxicity", "Avoid NSAIDs"),
            ("fluoxetine", "tramadol", "severe", "Serotonin syndrome risk", "Avoid combination"),
            ("lithium", "ibuprofen", "severe", "Lithium toxicity", "Use acetaminophen instead"),
        ]
        for a, b, sev, desc, rec in known_interactions:
            self.interactions.append(MedicationInteraction(a, b, sev, desc, rec))
            self.interactions.append(MedicationInteraction(b, a, sev, desc, rec))

    def check_interactions(self, medications: List[str]) -> List[MedicationInteraction]:
        found = []
        meds_lower = [m.lower() for m in medications]
        for interaction in self.interactions:
            if interaction.drug_a in meds_lower and interaction.drug_b in meds_lower:
                found.append(interaction)
        return found

    def check_allergy_conflict(
        self, medications: List[str], allergies: List[str]
    ) -> List[Dict[str, str]]:
        conflicts = []
        for med in medications:
            med_lower = med.lower()
            for allergy in allergies:
                allergy_lower = allergy.lower()
                if allergy_lower in med_lower or med_lower in allergy_lower:
                    conflicts.append({
                        "medication": med,
                        "allergy": allergy,
                        "severity": "potential_cross_reactivity",
                    })
        return conflicts

    def get_severity_level(self, interactions: List[MedicationInteraction]) -> str:
        if any(i.severity == "contraindicated" for i in interactions):
            return "contraindicated"
        if any(i.severity == "severe" for i in interactions):
            return "severe"
        if any(i.severity == "moderate" for i in interactions):
            return "moderate"
        if interactions:
            return "mild"
        return "none"


# ---------------------------------------------------------------------------
# FHIR Validator
# ---------------------------------------------------------------------------

class FHIRValidator:
    """Validates FHIR resource conformance."""

    def __init__(self) -> None:
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_patient(self, patient: Patient) -> Dict[str, Any]:
        self.errors = []
        self.warnings = []

        if not patient.patient_id:
            self.errors.append("Patient ID is required")
        if not patient.name.family:
            self.errors.append("Family name is required")
        if not patient.birth_date:
            self.warnings.append("Birth date is missing")
        if patient.gender == Gender.UNKNOWN:
            self.warnings.append("Gender is unknown")
        if not patient.identifiers:
            self.warnings.append("No identifiers (MRN) assigned")

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
        }

    def validate_medication(self, medication: Medication) -> Dict[str, Any]:
        self.errors = []
        self.warnings = []

        if not medication.medication_id:
            self.errors.append("Medication ID is required")
        if not medication.medication_name:
            self.errors.append("Medication name is required")
        if not medication.dosage:
            self.errors.append("Dosage is required")
        if not medication.frequency:
            self.errors.append("Frequency is required")
        if not medication.prescriber:
            self.warnings.append("Prescriber not specified")

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
        }

    def validate_observation(self, obs: Observation) -> Dict[str, Any]:
        self.errors = []
        self.warnings = []

        if not obs.observation_id:
            self.errors.append("Observation ID is required")
        if not obs.code:
            self.errors.append("Observation code is required")
        if obs.unit == "":
            self.warnings.append("Unit is missing")
        if obs.reference_range_low is not None and obs.reference_range_high is not None:
            if obs.reference_range_low > obs.reference_range_high:
                self.errors.append("Reference range low > high")

        return {
            "valid": len(self.errors) == 0,
            "errors": self.errors,
            "warnings": self.warnings,
        }


# ---------------------------------------------------------------------------
# Clinical Decision Support
# ---------------------------------------------------------------------------

class ClinicalDecisionSupport:
    """
    Clinical decision support system providing alerts,
    reminders, and evidence-based recommendations.
    """

    def __init__(self) -> None:
        self.alerts: List[ClinicalAlert] = []
        self.drug_checker = DrugInteractionChecker()
        self._alert_counter = 0

    def check_patient(self, patient: Patient, medications: List[Medication]) -> List[ClinicalAlert]:
        new_alerts = []
        active_meds = [m.medication_name for m in medications if m.is_active]

        interactions = self.drug_checker.check_interactions(active_meds)
        for interaction in interactions:
            self._alert_counter += 1
            alert = ClinicalAlert(
                alert_id=f"ALR-{self._alert_counter:04d}",
                patient_id=patient.patient_id,
                alert_type="drug_interaction",
                priority=AlertPriority.URGENT if interaction.severity == "severe" else AlertPriority.ROUTINE,
                message=f"Drug interaction: {interaction.drug_a} + {interaction.drug_b} — {interaction.description}",
                recommendation=interaction.recommendation,
                triggered_by="drug_interaction_check",
            )
            self.alerts.append(alert)
            new_alerts.append(alert)

        allergy_conflicts = self.drug_checker.check_allergy_conflict(active_meds, patient.allergies)
        for conflict in allergy_conflicts:
            self._alert_counter += 1
            alert = ClinicalAlert(
                alert_id=f"ALR-{self._alert_counter:04d}",
                patient_id=patient.patient_id,
                alert_type="allergy_conflict",
                priority=AlertPriority.STAT,
                message=f"Allergy conflict: {conflict['medication']} may react with allergy to {conflict['allergy']}",
                triggered_by="allergy_check",
            )
            self.alerts.append(alert)
            new_alerts.append(alert)

        return new_alerts

    def check_vitals(self, patient: Patient, vitals: Dict[str, float]) -> List[ClinicalAlert]:
        alerts = []
        critical_values = {
            "heart_rate": (50, 120),
            "systolic_bp": (90, 180),
            "diastolic_bp": (60, 110),
            "temperature": (35.5, 38.5),
            "oxygen_saturation": (90, 100),
            "respiratory_rate": (12, 25),
        }
        for vital_name, (low, high) in critical_values.items():
            if vital_name in vitals:
                value = vitals[vital_name]
                if value < low or value > high:
                    self._alert_counter += 1
                    alert = ClinicalAlert(
                        alert_id=f"ALR-{self._alert_counter:04d}",
                        patient_id=patient.patient_id,
                        alert_type="vital_critical",
                        priority=AlertPriority.STAT if vital_name == "oxygen_saturation" else AlertPriority.URGENT,
                        message=f"Critical {vital_name}: {value} (normal: {low}-{high})",
                        triggered_by="vital_check",
                    )
                    self.alerts.append(alert)
                    alerts.append(alert)
        return alerts

    def get_active_alerts(self, patient_id: Optional[str] = None) -> List[ClinicalAlert]:
        if patient_id:
            return [a for a in self.alerts if a.patient_id == patient_id and a.is_active]
        return [a for a in self.alerts if a.is_active]

    def acknowledge_alert(self, alert_id: str, user_id: str) -> bool:
        for alert in self.alerts:
            if alert.alert_id == alert_id:
                alert.acknowledged = True
                alert.acknowledged_by = user_id
                alert.acknowledged_at = datetime.utcnow()
                return True
        return False


# ---------------------------------------------------------------------------
# HIPAA Compliance
# ---------------------------------------------------------------------------

class HIPAACompliance:
    """
    HIPAA compliance auditing, access control, and audit logging.
    """

    def __init__(self) -> None:
        self.audit_log: List[AuditLogEntry] = []
        self.access_policies: Dict[str, List[str]] = {}
        self._log_counter = 0

    def log_access(
        self, action: str, resource_type: str, resource_id: str,
        user_id: str, user_role: str, patient_id: str,
        ip_address: str = "", outcome: str = "success"
    ) -> AuditLogEntry:
        self._log_counter += 1
        entry = AuditLogEntry(
            entry_id=f"AUD-{self._log_counter:06d}",
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            user_role=user_role,
            patient_id=patient_id,
            ip_address=ip_address,
            outcome=outcome,
        )
        self.audit_log.append(entry)
        logger.info("Audit: %s %s/%s by %s (%s)", action, resource_type, resource_id, user_id, user_role)
        return entry

    def check_access(self, user_role: str, resource_type: str, action: str) -> bool:
        key = f"{user_role}:{resource_type}:{action}"
        if key in self.access_policies:
            return True
        role_permissions = {
            "physician": ["read", "write", "order", "prescribe"],
            "nurse": ["read", "write_vitals", "administer"],
            "admin": ["read", "write", "delete", "export"],
            "billing": ["read_billing", "write_billing"],
            "lab_tech": ["read_orders", "write_results"],
            "pharmacist": ["read_orders", "verify", "dispense"],
        }
        allowed = role_permissions.get(user_role, [])
        return action in allowed or action in ["read", "write"]

    def deidentify(self, patient: Patient) -> Dict[str, Any]:
        deidentified = patient.to_fhir()
        deidentified["name"] = [{"family": "REDACTED", "given": ["REDACTED"]}]
        deidentified["birthDate"] = "1900-01-01"
        deidentified.pop("identifier", None)
        deidentified.pop("address", None)
        deidentified.pop("telecom", None)
        return deidentified

    def get_access_summary(self) -> Dict[str, Any]:
        by_action = defaultdict(int)
        by_user = defaultdict(int)
        for entry in self.audit_log:
            by_action[entry.action] += 1
            by_user[entry.user_id] += 1
        return {
            "total_events": len(self.audit_log),
            "by_action": dict(by_action),
            "by_user": dict(by_user),
            "failed_attempts": sum(1 for e in self.audit_log if e.outcome == "failure"),
        }

    def generate_compliance_report(self) -> Dict[str, Any]:
        summary = self.get_access_summary()
        return {
            "audit_events": summary["total_events"],
            "failed_access_attempts": summary["failed_attempts"],
            "unique_users": len(summary["by_user"]),
            "action_breakdown": summary["by_action"],
            "recommendations": self._generate_recommendations(summary),
        }

    def _generate_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        recs = []
        if summary["failed_attempts"] > 10:
            recs.append("Review failed access attempts for potential breach")
        if summary["total_events"] == 0:
            recs.append("No audit events recorded — verify logging is active")
        for action, count in summary["by_action"].items():
            if action == "export" and count > 50:
                recs.append(f"High export activity ({count} events) — review necessity")
        return recs


# ---------------------------------------------------------------------------
# Appointment Scheduler
# ---------------------------------------------------------------------------

class AppointmentScheduler:
    """Appointment scheduling and resource management."""

    def __init__(self) -> None:
        self.appointments: Dict[str, Appointment] = {}
        self.providers: Dict[str, Dict[str, Any]] = {}
        self._appt_counter = 0

    def register_provider(
        self, provider_id: str, name: str, specialty: str,
        available_hours: Dict[str, Tuple[int, int]] = None
    ) -> None:
        self.providers[provider_id] = {
            "name": name,
            "specialty": specialty,
            "available_hours": available_hours or {"mon": (9, 17), "tue": (9, 17), "wed": (9, 17), "thu": (9, 17), "fri": (9, 17)},
        }

    def book_appointment(
        self, patient_id: str, provider_id: str,
        start_time: datetime, duration_minutes: int = 30,
        appointment_type: str = "", reason: str = ""
    ) -> Optional[Appointment]:
        if provider_id not in self.providers:
            return None

        for appt in self.appointments.values():
            if (appt.provider == provider_id and appt.status not in (AppointmentStatus.CANCELLED, AppointmentStatus.NO_SHOW)):
                existing_end = appt.end_time
                new_end = start_time + timedelta(minutes=duration_minutes)
                if start_time < existing_end and new_end > appt.start_time:
                    return None

        self._appt_counter += 1
        appt = Appointment(
            appointment_id=f"APT-{self._appt_counter:05d}",
            patient_id=patient_id,
            provider=provider_id,
            start_time=start_time,
            end_time=start_time + timedelta(minutes=duration_minutes),
            appointment_type=appointment_type,
            reason=reason,
        )
        self.appointments[appt.appointment_id] = appt
        return appt

    def cancel_appointment(self, appointment_id: str) -> bool:
        if appointment_id in self.appointments:
            self.appointments[appointment_id].status = AppointmentStatus.CANCELLED
            return True
        return False

    def get_provider_schedule(self, provider_id: str, date: datetime) -> List[Appointment]:
        return [
            a for a in self.appointments.values()
            if a.provider == provider_id
            and a.start_time.date() == date.date()
            and a.status not in (AppointmentStatus.CANCELLED,)
        ]

    def get_available_slots(
        self, provider_id: str, date: datetime, duration_minutes: int = 30
    ) -> List[datetime]:
        if provider_id not in self.providers:
            return []
        booked = self.get_provider_schedule(provider_id, date)
        booked_times = {(a.start_time, a.end_time) for a in booked}
        available = []
        day_start = date.replace(hour=9, minute=0, second=0, microsecond=0)
        day_end = date.replace(hour=17, minute=0, second=0, microsecond=0)
        current = day_start
        while current + timedelta(minutes=duration_minutes) <= day_end:
            slot_end = current + timedelta(minutes=duration_minutes)
            overlaps = any(current < end and slot_end > start for start, end in booked_times)
            if not overlaps:
                available.append(current)
            current += timedelta(minutes=duration_minutes)
        return available


# ---------------------------------------------------------------------------
# Claims Processor
# ---------------------------------------------------------------------------

class ClaimsProcessor:
    """Insurance claims processing and validation."""

    def __init__(self) -> None:
        self.claims: Dict[str, Claim] = {}
        self._claim_counter = 0

    def submit_claim(
        self, patient_id: str, encounter_id: str,
        diagnosis_codes: List[str], procedure_codes: List[str],
        total_amount: float, insurance_type: InsuranceType = InsuranceType.PRIVATE
    ) -> Claim:
        self._claim_counter += 1
        claim = Claim(
            claim_id=f"CLM-{self._claim_counter:06d}",
            patient_id=patient_id,
            encounter_id=encounter_id,
            diagnosis_codes=diagnosis_codes,
            procedure_codes=procedure_codes,
            total_amount=total_amount,
            insurance_type=insurance_type,
            submitted_date=datetime.utcnow(),
        )
        self.claims[claim.claim_id] = claim
        return claim

    def validate_claim(self, claim_id: str) -> Dict[str, Any]:
        if claim_id not in self.claims:
            return {"valid": False, "errors": ["Claim not found"]}
        claim = self.claims[claim_id]
        errors = []
        if not claim.diagnosis_codes:
            errors.append("No diagnosis codes")
        if not claim.procedure_codes:
            errors.append("No procedure codes")
        if claim.total_amount <= 0:
            errors.append("Invalid amount")
        return {"valid": len(errors) == 0, "errors": errors}

    def process_claim(self, claim_id: str, paid_amount: float, denial_reason: str = "") -> bool:
        if claim_id not in self.claims:
            return False
        claim = self.claims[claim_id]
        claim.paid_amount = paid_amount
        claim.denial_reason = denial_reason
        claim.status = ClaimStatus.CLOSED if not denial_reason else ClaimStatus.CANCELLED
        claim.resolved_date = datetime.utcnow()
        return True

    def get_claims_by_patient(self, patient_id: str) -> List[Claim]:
        return [c for c in self.claims.values() if c.patient_id == patient_id]

    def claims_summary(self) -> Dict[str, Any]:
        total_submitted = sum(c.total_amount for c in self.claims.values())
        total_paid = sum(c.paid_amount for c in self.claims.values())
        denied = [c for c in self.claims.values() if c.is_denied]
        return {
            "total_claims": len(self.claims),
            "total_submitted": total_submitted,
            "total_paid": total_paid,
            "denied_count": len(denied),
            "denial_rate": len(denied) / len(self.claims) if self.claims else 0,
            "outstanding": total_submitted - total_paid,
        }


# ---------------------------------------------------------------------------
# Clinical Workflow Manager
# ---------------------------------------------------------------------------

class WorkflowManager:
    """Manages clinical workflows and care pathways."""

    def __init__(self) -> None:
        self.workflows: Dict[str, ClinicalWorkflow] = {}
        self._wf_counter = 0

    def create_workflow(
        self, patient_id: str, name: str, steps: List[Dict[str, str]]
    ) -> ClinicalWorkflow:
        self._wf_counter += 1
        wf_steps = [
            WorkflowStep(
                step_id=f"WS-{self._wf_counter}-{i}",
                step_type=WorkflowStepType(s.get("type", "assessment")),
                description=s.get("description", ""),
                required=s.get("required", True),
                assignee=s.get("assignee", ""),
            )
            for i, s in enumerate(steps)
        ]
        workflow = ClinicalWorkflow(
            workflow_id=f"WF-{self._wf_counter:04d}",
            name=name,
            patient_id=patient_id,
            steps=wf_steps,
        )
        self.workflows[workflow.workflow_id] = workflow
        return workflow

    def complete_step(self, workflow_id: str, step_id: str, notes: str = "") -> bool:
        if workflow_id not in self.workflows:
            return False
        for step in self.workflows[workflow_id].steps:
            if step.step_id == step_id:
                step.completed = True
                step.notes = notes
                return True
        return False

    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        if workflow_id not in self.workflows:
            return None
        wf = self.workflows[workflow_id]
        return {
            "workflow_id": workflow_id,
            "name": wf.name,
            "patient_id": wf.patient_id,
            "status": wf.status,
            "completion_pct": wf.completion_pct,
            "total_steps": len(wf.steps),
            "completed_steps": sum(1 for s in wf.steps if s.completed),
            "current_step": wf.current_step.description if wf.current_step else None,
        }

    def get_patient_workflows(self, patient_id: str) -> List[ClinicalWorkflow]:
        return [w for w in self.workflows.values() if w.patient_id == patient_id]


# ---------------------------------------------------------------------------
# Lab Result Analyzer
# ---------------------------------------------------------------------------

class LabAnalyzer:
    """Analyzes lab results, trends, and generates clinical summaries."""

    def __init__(self) -> None:
        self.results: Dict[str, List[Observation]] = defaultdict(list)

    def add_result(self, observation: Observation) -> None:
        self.results[observation.patient_id].append(observation)

    def get_patient_results(
        self, patient_id: str, code: Optional[str] = None
    ) -> List[Observation]:
        results = self.results.get(patient_id, [])
        if code:
            results = [r for r in results if r.code == code]
        return sorted(results, key=lambda x: x.effective_date, reverse=True)

    def get_critical_results(self, patient_id: str) -> List[Observation]:
        return [
            r for r in self.results.get(patient_id, [])
            if r.is_high or r.is_low
        ]

    def get_trend(self, patient_id: str, code: str) -> Dict[str, Any]:
        results = self.get_patient_results(patient_id, code)
        if len(results) < 2:
            return {"trend": "insufficient_data", "data_points": len(results)}
        values = [r.value for r in reversed(results)]
        first_half = statistics.mean(values[:len(values)//2])
        second_half = statistics.mean(values[len(values)//2:])
        change_pct = (second_half - first_half) / first_half * 100 if first_half != 0 else 0
        return {
            "trend": "increasing" if change_pct > 10 else "decreasing" if change_pct < -10 else "stable",
            "change_pct": change_pct,
            "latest": values[-1],
            "earliest": values[0],
            "data_points": len(values),
        }

    def generate_summary(self, patient_id: str) -> Dict[str, Any]:
        results = self.results.get(patient_id, [])
        critical = self.get_critical_results(patient_id)
        latest_by_code: Dict[str, Observation] = {}
        for r in results:
            if r.code not in latest_by_code or r.effective_date > latest_by_code[r.code].effective_date:
                latest_by_code[r.code] = r
        return {
            "patient_id": patient_id,
            "total_results": len(results),
            "unique_tests": len(latest_by_code),
            "critical_count": len(critical),
            "latest_results": {
                code: {"value": obs.value, "unit": obs.unit, "status": "normal" if obs.is_normal else "abnormal"}
                for code, obs in latest_by_code.items()
            },
        }


import statistics


# ---------------------------------------------------------------------------
# Population Health
# ---------------------------------------------------------------------------

class PopulationHealthAnalyzer:
    """Population-level health analytics."""

    def __init__(self) -> None:
        self.patients: List[Patient] = []
        self.encounters: List[Encounter] = []
        self.observations: List[Observation] = []

    def add_patient(self, patient: Patient) -> None:
        self.patients.append(patient)

    def add_encounter(self, encounter: Encounter) -> None:
        self.encounters.append(encounter)

    def get_metrics(self) -> PopulationMetrics:
        if not self.patients:
            return PopulationMetrics()
        ages = [p.age for p in self.patients if p.age is not None]
        gender_dist = defaultdict(int)
        for p in self.patients:
            gender_dist[p.gender.value] += 1
        condition_counts = defaultdict(int)
        for p in self.patients:
            for c in p.conditions:
                condition_counts[c] += 1
        top_conditions = sorted(condition_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        avg_age = statistics.mean(ages) if ages else 0
        readmits = len([e for e in self.encounters if e.encounter_type == EncounterType.INPATIENT])
        return PopulationMetrics(
            total_patients=len(self.patients),
            avg_age=avg_age,
            gender_distribution=dict(gender_dist),
            top_conditions=top_conditions,
            avg_bmi=25.0,
            readmission_rate=readmits / len(self.patients) * 100 if self.patients else 0,
            avg_length_of_stay=3.5,
        )


# ---------------------------------------------------------------------------
# Main demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    print("=" * 60)
    print("Healthcare Agent — Comprehensive Demo")
    print("=" * 60)

    # Create patient
    patient = Patient(
        patient_id="P001",
        identifiers=[Identifier("http://hospital.org/mrn", "MRN-12345", "usual", "MR")],
        name=HumanName(family="Smith", given=["John", "Michael"]),
        gender=Gender.MALE,
        birth_date=datetime(1980, 5, 15),
        address=[Address(street=["123 Main St"], city="Springfield", state="IL", postal_code="62701")],
        contact=[ContactPoint("phone", "555-0100", "home", True)],
    )
    print(f"\nPatient: {patient.full_name}, Age: {patient.age}, MRN: {patient.mrn}")

    # Medications
    meds = [
        Medication("M001", "P001", "Warfarin", "5mg", "daily"),
        Medication("M002", "P001", "Aspirin", "81mg", "daily"),
    ]

    # Clinical Decision Support
    cds = ClinicalDecisionSupport()
    alerts = cds.check_patient(patient, meds)
    print(f"\nClinical Alerts: {len(alerts)}")
    for a in alerts:
        print(f"  [{a.priority.name}] {a.message}")

    # FHIR Validation
    validator = FHIRValidator()
    validation = validator.validate_patient(patient)
    print(f"\nFHIR Validation: {'PASS' if validation['valid'] else 'FAIL'}")
    print(f"  Errors: {validation['errors']}")
    print(f"  Warnings: {validation['warnings']}")

    # Lab Results
    lab_analyzer = LabAnalyzer()
    lab_analyzer.add_result(Observation("O001", "P001", "glucose", "Blood Glucose", 126, "mg/dL", reference_range_low=70, reference_range_high=100))
    lab_analyzer.add_result(Observation("O002", "P001", "hba1c", "HbA1c", 7.2, "%", reference_range_low=4.0, reference_range_high=5.7))
    critical = lab_analyzer.get_critical_results("P001")
    print(f"\nCritical Results: {len(critical)}")
    for r in critical:
        print(f"  {r.display}: {r.value} {r.unit} ({'HIGH' if r.is_high else 'LOW'})")

    # HIPAA Compliance
    hipaa = HIPAACompliance()
    hipaa.log_access("read", "Patient", "P001", "dr.jones", "physician", "P001")
    hipaa.log_access("write", "Medication", "M001", "dr.jones", "physician", "P001")
    report = hipaa.generate_compliance_report()
    print(f"\nHIPAA Report: {report['audit_events']} events, {report['failed_access_attempts']} failures")

    # Appointment Scheduling
    scheduler = AppointmentScheduler()
    scheduler.register_provider("DR001", "Dr. Jones", "Internal Medicine")
    available = scheduler.get_available_slots("DR001", datetime(2025, 7, 10))
    print(f"\nAvailable slots: {len(available)}")

    # Claims
    claims = ClaimsProcessor()
    claim = claims.submit_claim("P001", "ENC001", ["E11.9"], ["99213"], 150.0)
    claims.process_claim(claim.claim_id, 120.0)
    summary = claims.claims_summary()
    print(f"\nClaims: {summary['total_claims']} total, ${summary['total_paid']:.2f} paid")

    # Clinical Workflow
    wf_mgr = WorkflowManager()
    workflow = wf_mgr.create_workflow("P001", "Admission", [
        {"type": "assessment", "description": "Initial assessment"},
        {"type": "order", "description": "Admission orders"},
        {"type": "procedure", "description": "IV placement"},
    ])
    wf_mgr.complete_step(workflow.workflow_id, workflow.steps[0].step_id, "Completed initial assessment")
    status = wf_mgr.get_workflow_status(workflow.workflow_id)
    print(f"\nWorkflow: {status['name']} - {status['completion_pct']:.0%} complete")

    # Drug Interactions
    checker = DrugInteractionChecker()
    interactions = checker.check_interactions(["warfarin", "aspirin", "metformin"])
    print(f"\nDrug Interactions: {len(interactions)} found")
    for i in interactions:
        print(f"  [{i.severity}] {i.drug_a} + {i.drug_b}: {i.description}")

    print("\n" + "=" * 60)
    print("Healthcare Agent demo complete.")
    print("=" * 60)

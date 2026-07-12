"""
Telemedicine - Video Consultation, Remote Monitoring, E-Prescribing, HIPAA Compliance
Comprehensive module for telehealth platform capabilities.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, EnumMeta, auto
from typing import Any, Callable, Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class SessionStatus(Enum):
    """Telemedicine session lifecycle states."""
    SCHEDULED = "scheduled"
    WAITING_ROOM = "waiting_room"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    FAILED = "failed"


class ConsultationType(Enum):
    """Types of telemedicine consultations."""
    LIVE_VIDEO = "live_video"
    AUDIO_ONLY = "audio_only"
    ASYNCHRONOUS = "asynchronous"
    REMOTE_MONITORING = "remote_monitoring"
    HYBRID = "hybrid"


class DeviceType(Enum):
    """Remote patient monitoring device categories."""
    BLOOD_PRESSURE_CUFF = "blood_pressure_cuff"
    GLUCOMETER = "glucometer"
    PULSE_OXIMETER = "pulse_oximeter"
    WEIGHT_SCALE = "weight_scale"
    THERMOMETER = "thermometer"
    ECG_MONITOR = "ecg_monitor"
    SPIROMETER = "spirometer"
    WEARABLE_FITNESS = "wearable_fitness"


class VitalSign(Enum):
    """Physiological measurements tracked in RPM."""
    HEART_RATE = "heart_rate"
    BLOOD_PRESSURE_SYSTOLIC = "bp_systolic"
    BLOOD_PRESSURE_DIASTOLIC = "bp_diastolic"
    OXYGEN_SATURATION = "spo2"
    BLOOD_GLUCOSE = "blood_glucose"
    BODY_WEIGHT = "body_weight"
    BODY_TEMPERATURE = "body_temperature"
    RESPIRATORY_RATE = "respiratory_rate"


class AlertSeverity(Enum):
    """Alert severity levels for monitoring alerts."""
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PrescriptionStatus(Enum):
    """E-prescription lifecycle states."""
    DRAFT = "draft"
    PENDING_SIGNATURE = "pending_signature"
    SIGNED = "signed"
    TRANSMITTED = "transmitted"
    RECEIVED_BY_PHARMACY = "received_by_pharmacy"
    DISPENSED = "dispensed"
    CANCELLED = "cancelled"
    DENIED = "denied"


class ControlledSubstanceSchedule(Enum):
    """DEA controlled substance schedules."""
    NONE = 0
    II = 2
    III = 3
    IV = 4
    V = 5


class ConsentStatus(Enum):
    """Patient consent states for telehealth."""
    PENDING = "pending"
    GRANTED = "granted"
    DENIED = "denied"
    WITHDRAWN = "withdrawn"
    EXPIRED = "expired"


# ─── Dataclasses ──────────────────────────────────────────────────────────────

@dataclass
class Provider:
    """Healthcare provider participating in telemedicine."""
    provider_id: str
    name: str
    specialty: str
    npi: str
    license_states: list[str] = field(default_factory=list)
    dea_number: str = ""
    epcs_enrolled: bool = False
    video_capable: bool = True

    def can_prescribe_controlled(self) -> bool:
        return self.epcs_enrolled and self.dea_number != ""


@dataclass
class Patient:
    """Patient participating in telehealth."""
    patient_id: str
    name: str
    date_of_birth: str
    state: str
    phone: str
    email: str
    has_video_capability: bool = True
    consent_status: ConsentStatus = ConsentStatus.PENDING

    def consent_valid(self) -> bool:
        return self.consent_status == ConsentStatus.GRANTED


@dataclass
class SessionConfig:
    """Configuration for a telemedicine session."""
    max_duration_minutes: int = 30
    allow_recording: bool = False
    enable_screen_sharing: bool = True
    enable_chat: bool = True
    enable_file_sharing: bool = False
    video_quality: str = "720p"
    encryption_enabled: bool = True
    hipaa_mode: bool = True

    def validate_hipaa(self) -> list[str]:
        issues: list[str] = []
        if not self.encryption_enabled:
            issues.append("Encryption must be enabled for HIPAA compliance")
        if not self.hipaa_mode:
            issues.append("HIPAA mode must be enabled")
        if self.allow_recording:
            issues.append("Recording enabled — ensure explicit patient consent obtained")
        return issues


@dataclass
class TelemedicineSession:
    """A complete telemedicine session record."""
    session_id: str
    provider: Provider
    patient: Patient
    consultation_type: ConsultationType
    config: SessionConfig
    status: SessionStatus = SessionStatus.SCHEDULED
    scheduled_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    notes: str = ""
    diagnosis_codes: list[str] = field(default_factory=list)
    recording_id: Optional[str] = None
    audit_log: list[dict[str, Any]] = field(default_factory=list)

    def duration_seconds(self) -> Optional[float]:
        if self.started_at and self.ended_at:
            return (self.ended_at - self.started_at).total_seconds()
        return None

    def log_event(self, event_type: str, details: str = "") -> None:
        self.audit_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "details": details,
            "session_id": self.session_id,
        })


@dataclass
class RPMSession:
    """Remote patient monitoring configuration for a patient."""
    patient: Patient
    monitoring_provider: Provider
    devices: list[DeviceType] = field(default_factory=list)
    alert_thresholds: dict[VitalSign, dict[str, float]] = field(default_factory=dict)
    monitoring_start: datetime = field(default_factory=datetime.utcnow)
    monitoring_end: Optional[datetime] = None
    reading_frequency_hours: int = 24
    alerts_enabled: bool = True

    def is_active(self) -> bool:
        now = datetime.utcnow()
        if self.monitoring_end and now > self.monitoring_end:
            return False
        return True


@dataclass
class VitalReading:
    """A single vital sign reading from an RPM device."""
    reading_id: str
    patient_id: str
    device_type: DeviceType
    vital_sign: VitalSign
    value: float
    unit: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    device_serial: str = ""
    battery_level: Optional[float] = None

    def is_within_range(self, thresholds: dict[str, float]) -> bool:
        low = thresholds.get("min")
        high = thresholds.get("max")
        if low is not None and self.value < low:
            return False
        if high is not None and self.value > high:
            return False
        return True


@dataclass
class MonitoringAlert:
    """An alert generated from RPM data."""
    alert_id: str
    patient_id: str
    vital_sign: VitalSign
    severity: AlertSeverity
    message: str
    reading_value: float
    threshold: dict[str, float]
    created_at: datetime = field(default_factory=datetime.utcnow)
    acknowledged: bool = False
    acknowledged_by: str = ""

    def acknowledge(self, by: str) -> None:
        self.acknowledged = True
        self.acknowledged_by = by


@dataclass
class Prescription:
    """An electronic prescription."""
    prescription_id: str
    provider: Provider
    patient: Patient
    medication_name: str
    medication_code: str
    dosage: str
    frequency: str
    quantity: int
    refills: int
    directions: str
    schedule: ControlledSubstanceSchedule = ControlledSubstanceSchedule.NONE
    status: PrescriptionStatus = PrescriptionStatus.DRAFT
    pharmacy_id: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    transmitted_at: Optional[datetime] = None
    epcs_verification: bool = False

    def requires_epcs(self) -> bool:
        return self.schedule != ControlledSubstanceSchedule.NONE

    def can_transmit(self) -> tuple[bool, str]:
        if self.status != PrescriptionStatus.SIGNED:
            return False, "Prescription must be signed before transmission"
        if self.requires_epcs() and not self.epcs_verification:
            return False, "EPCS identity verification required for controlled substances"
        if not self.provider.can_prescribe_controlled() and self.requires_epcs():
            return False, "Provider not enrolled in EPCS"
        return True, "Ready for transmission"


@dataclass
class AuditEntry:
    """HIPAA audit log entry."""
    entry_id: str
    timestamp: datetime
    event_type: str
    actor_id: str
    actor_role: str
    resource_type: str
    resource_id: str
    action: str
    patient_id: str
    details: dict[str, Any] = field(default_factory=dict)
    ip_address: str = ""
    session_id: str = ""


# ─── Service Classes ──────────────────────────────────────────────────────────

class VideoConsultationManager:
    """Manages live video consultation sessions."""

    def __init__(self) -> None:
        self._sessions: dict[str, TelemedicineSession] = {}
        self._waiting_room: dict[str, TelemedicineSession] = {}
        self._event_handlers: dict[str, list[Callable[..., Any]]] = {}

    def schedule_session(
        self,
        provider: Provider,
        patient: Patient,
        consultation_type: ConsultationType,
        config: SessionConfig,
        scheduled_at: datetime,
    ) -> TelemedicineSession:
        """Schedule a new telemedicine session."""
        hipaa_issues = config.validate_hipaa()
        if hipaa_issues:
            raise ValueError(f"HIPAA compliance issues: {'; '.join(hipaa_issues)}")

        if not provider.video_capable and consultation_type == ConsultationType.LIVE_VIDEO:
            raise ValueError(f"Provider {provider.name} is not video capable")

        session = TelemedicineSession(
            session_id=f"SESSION-{uuid.uuid4().hex[:10]}",
            provider=provider,
            patient=patient,
            consultation_type=consultation_type,
            config=config,
            scheduled_at=scheduled_at,
        )
        session.log_event("session_scheduled", f"Provider: {provider.name}")
        self._sessions[session.session_id] = session
        return session

    def checkin_patient(self, session_id: str) -> TelemedicineSession:
        """Patient joins the waiting room."""
        session = self._get_session(session_id)
        if session.status != SessionStatus.SCHEDULED:
            raise ValueError(f"Cannot checkin — session is {session.status.value}")
        if not session.patient.consent_valid():
            raise ValueError("Patient consent required before session")

        session.status = SessionStatus.WAITING_ROOM
        session.log_event("patient_checked_in", session.patient.name)
        self._waiting_room[session_id] = session
        return session

    def start_session(self, session_id: str) -> TelemedicineSession:
        """Provider starts the video consultation."""
        session = self._get_session(session_id)
        session.status = SessionStatus.IN_PROGRESS
        session.started_at = datetime.utcnow()
        session.log_event("session_started", f"Started at {session.started_at.isoformat()}")
        self._waiting_room.pop(session_id, None)
        return session

    def end_session(self, session_id: str, notes: str = "") -> TelemedicineSession:
        """End the video consultation."""
        session = self._get_session(session_id)
        session.status = SessionStatus.COMPLETED
        session.ended_at = datetime.utcnow()
        session.notes = notes
        session.log_event("session_ended", f"Duration: {session.duration_seconds()}s")
        return session

    def mark_no_show(self, session_id: str) -> TelemedicineSession:
        """Mark session as no-show."""
        session = self._get_session(session_id)
        session.status = SessionStatus.NO_SHOW
        session.log_event("no_show", "Patient did not join")
        return session

    def get_session_metrics(self, sessions: list[TelemedicineSession]) -> dict[str, Any]:
        """Calculate session performance metrics."""
        total = len(sessions)
        completed = sum(1 for s in sessions if s.status == SessionStatus.COMPLETED)
        no_shows = sum(1 for s in sessions if s.status == SessionStatus.NO_SHOW)
        durations = [s.duration_seconds() for s in sessions if s.duration_seconds()]
        avg_duration = sum(durations) / len(durations) if durations else 0

        return {
            "total_sessions": total,
            "completed": completed,
            "no_shows": no_shows,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
            "no_show_rate": (no_shows / total * 100) if total > 0 else 0,
            "average_duration_seconds": round(avg_duration, 1),
        }

    def _get_session(self, session_id: str) -> TelemedicineSession:
        session = self._sessions.get(session_id)
        if not session:
            raise KeyError(f"Session not found: {session_id}")
        return session


class RPMonitoringService:
    """Remote Patient Monitoring data collection and alerting."""

    def __init__(self) -> None:
        self._rpm_sessions: dict[str, RPMSession] = {}
        self._readings: dict[str, list[VitalReading]] = {}
        self._alerts: dict[str, list[MonitoringAlert]] = {}
        self._default_thresholds: dict[VitalSign, dict[str, float]] = {
            VitalSign.HEART_RATE: {"min": 50, "max": 120},
            VitalSign.BLOOD_PRESSURE_SYSTOLIC: {"min": 80, "max": 180},
            VitalSign.BLOOD_PRESSURE_DIASTOLIC: {"min": 50, "max": 110},
            VitalSign.OXYGEN_SATURATION: {"min": 90, "max": 100},
            VitalSign.BLOOD_GLUCOSE: {"min": 50, "max": 400},
            VitalSign.BODY_WEIGHT: {"min": 30, "max": 300},
            VitalSign.BODY_TEMPERATURE: {"min": 95.0, "max": 104.0},
            VitalSign.RESPIRATORY_RATE: {"min": 8, "max": 30},
        }

    def enroll_patient(self, patient: Patient, provider: Provider, devices: list[DeviceType]) -> RPMSession:
        """Enroll a patient in remote monitoring."""
        session = RPMSession(
            patient=patient,
            monitoring_provider=provider,
            devices=devices,
            alert_thresholds=dict(self._default_thresholds),
        )
        self._rpm_sessions[patient.patient_id] = session
        self._readings[patient.patient_id] = []
        self._alerts[patient.patient_id] = []
        return session

    def record_reading(self, reading: VitalReading) -> Optional[MonitoringAlert]:
        """Record a vital sign reading and check for alerts."""
        if reading.patient_id not in self._readings:
            raise KeyError(f"Patient not enrolled in RPM: {reading.patient_id}")

        self._readings[reading.patient_id].append(reading)

        rpm_session = self._rpm_sessions.get(reading.patient_id)
        if not rpm_session or not rpm_session.alerts_enabled:
            return None

        thresholds = rpm_session.alert_thresholds.get(
            reading.vital_sign, self._default_thresholds.get(reading.vital_sign, {})
        )
        if reading.is_within_range(thresholds):
            return None

        severity = self._determine_alert_severity(reading, thresholds)
        alert = MonitoringAlert(
            alert_id=f"ALERT-{uuid.uuid4().hex[:8]}",
            patient_id=reading.patient_id,
            vital_sign=reading.vital_sign,
            severity=severity,
            message=self._build_alert_message(reading, thresholds),
            reading_value=reading.value,
            threshold=thresholds,
        )
        self._alerts[reading.patient_id].append(alert)
        return alert

    def get_patient_summary(self, patient_id: str) -> dict[str, Any]:
        """Get a summary of monitoring data for a patient."""
        readings = self._readings.get(patient_id, [])
        alerts = self._alerts.get(patient_id, [])

        vital_counts: dict[str, int] = {}
        for r in readings:
            key = r.vital_sign.value
            vital_counts[key] = vital_counts.get(key, 0) + 1

        return {
            "patient_id": patient_id,
            "total_readings": len(readings),
            "total_alerts": len(alerts),
            "unacknowledged_alerts": sum(1 for a in alerts if not a.acknowledged),
            "readings_by_type": vital_counts,
            "monitoring_active": self._rpm_sessions.get(patient_id, RPMSession(
                patient=Patient("", "", "", "", "", ""), provider=Provider("", "", "", ""),
            )).is_active(),
        }

    def get_alerts(self, patient_id: str, unacknowledged_only: bool = False) -> list[MonitoringAlert]:
        alerts = self._alerts.get(patient_id, [])
        if unacknowledged_only:
            alerts = [a for a in alerts if not a.acknowledged]
        return alerts

    def _determine_alert_severity(
        self, reading: VitalReading, thresholds: dict[str, float]
    ) -> AlertSeverity:
        low = thresholds.get("min", 0)
        high = thresholds.get("max", 999)
        range_size = high - low
        deviation = 0
        if reading.value < low:
            deviation = (low - reading.value) / range_size
        elif reading.value > high:
            deviation = (reading.value - high) / range_size

        if deviation > 0.3:
            return AlertSeverity.CRITICAL
        if deviation > 0.2:
            return AlertSeverity.HIGH
        if deviation > 0.1:
            return AlertSeverity.MEDIUM
        return AlertSeverity.LOW

    def _build_alert_message(
        self, reading: VitalReading, thresholds: dict[str, float]
    ) -> str:
        return (
            f"{reading.vital_sign.value}: {reading.value} {reading.unit} "
            f"outside range [{thresholds.get('min')}, {thresholds.get('max')}]"
        )


class EPrescribingService:
    """Electronic prescribing with EPCS compliance."""

    def __init__(self) -> None:
        self._prescriptions: dict[str, Prescription] = {}
        self._pharmacies: dict[str, dict[str, str]] = {}
        self._epcs_tokens: dict[str, dict[str, Any]] = {}

    def create_prescription(
        self,
        provider: Provider,
        patient: Patient,
        medication_name: str,
        medication_code: str,
        dosage: str,
        frequency: str,
        quantity: int,
        refills: int,
        directions: str,
        schedule: ControlledSubstanceSchedule = ControlledSubstanceSchedule.NONE,
        pharmacy_id: str = "",
    ) -> Prescription:
        """Create a new electronic prescription."""
        rx = Prescription(
            prescription_id=f"RX-{uuid.uuid4().hex[:10]}",
            provider=provider,
            patient=patient,
            medication_name=medication_name,
            medication_code=medication_code,
            dosage=dosage,
            frequency=frequency,
            quantity=quantity,
            refills=refills,
            directions=directions,
            schedule=schedule,
            pharmacy_id=pharmacy_id,
        )
        rx.status = PrescriptionStatus.PENDING_SIGNATURE
        self._prescriptions[rx.prescription_id] = rx
        return rx

    def sign_prescription(
        self, prescription_id: str, epcs_token: Optional[str] = None
    ) -> Prescription:
        """Provider signs a prescription (EPCS token required for controlled substances)."""
        rx = self._prescriptions[prescription_id]
        if rx.requires_epcs():
            if not epcs_token:
                raise ValueError("EPCS two-factor authentication required for controlled substances")
            if not self._validate_epcs_token(rx.provider.provider_id, epcs_token):
                raise ValueError("Invalid EPCS token")
            rx.epcs_verification = True

        rx.status = PrescriptionStatus.SIGNED
        return rx

    def transmit_prescription(self, prescription_id: str) -> Prescription:
        """Transmit signed prescription to pharmacy via Surescripts."""
        rx = self._prescriptions[prescription_id]
        can_tx, reason = rx.can_transmit()
        if not can_tx:
            raise ValueError(reason)
        rx.status = PrescriptionStatus.TRANSMITTED
        rx.transmitted_at = datetime.utcnow()
        return rx

    def cancel_prescription(self, prescription_id: str, reason: str) -> Prescription:
        """Cancel a prescription."""
        rx = self._prescriptions[prescription_id]
        if rx.status in (PrescriptionStatus.DISPENSED,):
            raise ValueError("Cannot cancel a dispensed prescription")
        rx.status = PrescriptionStatus.CANCELLED
        return rx

    def register_epcs_token(self, provider_id: str, token_type: str) -> str:
        """Register an EPCS authentication token for a provider."""
        token = f"epcs-{uuid.uuid4().hex}"
        self._epcs_tokens[provider_id] = {
            "token": token,
            "type": token_type,
            "registered_at": datetime.utcnow().isoformat(),
        }
        return token

    def get_prescription_history(self, patient_id: str) -> list[dict[str, Any]]:
        """Get prescription history for a patient."""
        history = []
        for rx in self._prescriptions.values():
            if rx.patient.patient_id == patient_id:
                history.append({
                    "prescription_id": rx.prescription_id,
                    "medication": rx.medication_name,
                    "status": rx.status.value,
                    "created_at": rx.created_at.isoformat(),
                    "transmitted_at": rx.transmitted_at.isoformat() if rx.transmitted_at else None,
                })
        return history

    def _validate_epcs_token(self, provider_id: str, token: str) -> bool:
        stored = self._epcs_tokens.get(provider_id)
        return stored is not None and stored["token"] == token


class HIPAAComplianceManager:
    """Manages HIPAA compliance requirements for telemedicine."""

    def __init__(self) -> None:
        self._audit_log: list[AuditEntry] = []
        self._baas: dict[str, dict[str, Any]] = {}
        self._breach_incidents: list[dict[str, Any]] = []

    def log_access(
        self,
        actor_id: str,
        actor_role: str,
        resource_type: str,
        resource_id: str,
        action: str,
        patient_id: str,
        ip_address: str = "",
        session_id: str = "",
    ) -> AuditEntry:
        """Log a PHI access event for audit trail."""
        entry = AuditEntry(
            entry_id=f"AUDIT-{uuid.uuid4().hex[:8]}",
            timestamp=datetime.utcnow(),
            event_type="phi_access",
            actor_id=actor_id,
            actor_role=actor_role,
            resource_type=resource_type,
            resource_id=resource_id,
            action=action,
            patient_id=patient_id,
            ip_address=ip_address,
            session_id=session_id,
        )
        self._audit_log.append(entry)
        return entry

    def register_baa(
        self, vendor_name: str, vendor_type: str, effective_date: datetime, expires_date: datetime
    ) -> str:
        """Register a Business Associate Agreement."""
        baa_id = f"BAA-{uuid.uuid4().hex[:8]}"
        self._baas[baa_id] = {
            "vendor_name": vendor_name,
            "vendor_type": vendor_type,
            "effective_date": effective_date.isoformat(),
            "expires_date": expires_date.isoformat(),
            "status": "active",
        }
        return baa_id

    def report_breach(
        self, description: str, affected_patients: list[str], discovery_date: datetime
    ) -> dict[str, Any]:
        """Report a potential data breach."""
        breach = {
            "breach_id": f"BREACH-{uuid.uuid4().hex[:8]}",
            "description": description,
            "affected_patients": affected_patients,
            "discovery_date": discovery_date.isoformat(),
            "notification_deadline": (discovery_date + timedelta(days=60)).isoformat(),
            "status": "under_investigation",
        }
        self._breach_incidents.append(breach)
        return breach

    def get_audit_trail(
        self,
        patient_id: Optional[str] = None,
        actor_id: Optional[str] = None,
        event_type: Optional[str] = None,
        limit: int = 100,
    ) -> list[AuditEntry]:
        """Query the audit trail with optional filters."""
        results = self._audit_log
        if patient_id:
            results = [e for e in results if e.patient_id == patient_id]
        if actor_id:
            results = [e for e in results if e.actor_id == actor_id]
        if event_type:
            results = [e for e in results if e.event_type == event_type]
        return results[-limit:]

    def validate_session_hipaa(self, session: TelemedicineSession) -> list[str]:
        """Validate HIPAA compliance for a telemedicine session."""
        issues: list[str] = []
        if not session.config.encryption_enabled:
            issues.append("Session not encrypted")
        if not session.config.hipaa_mode:
            issues.append("HIPAA mode disabled")
        if session.config.allow_recording and not session.patient.consent_valid():
            issues.append("Recording enabled without patient consent")
        if session.status == SessionStatus.COMPLETED and session.duration_seconds() is None:
            issues.append("Session end time not recorded")
        return issues

    def get_compliance_dashboard(self) -> dict[str, Any]:
        """Get a summary of compliance status."""
        return {
            "total_audit_entries": len(self._audit_log),
            "active_baas": sum(1 for b in self._baas.values() if b["status"] == "active"),
            "open_breaches": sum(
                1 for b in self._breach_incidents if b["status"] == "under_investigation"
            ),
            "recent_access_count": sum(
                1 for e in self._audit_log
                if (datetime.utcnow() - e.timestamp).days < 30
            ),
        }


# ─── Demo ─────────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate telemedicine capabilities."""
    print("=" * 70)
    print("TELEMEDICINE DEMONSTRATION")
    print("=" * 70)

    # Setup providers and patients
    provider = Provider(
        provider_id="PROV-001",
        name="Dr. Sarah Chen",
        specialty="Internal Medicine",
        npi="1234567890",
        license_states=["CA", "NY", "TX"],
        dea_number="FC1234567",
        epcs_enrolled=True,
    )
    patient = Patient(
        patient_id="PAT-001",
        name="Michael Torres",
        date_of_birth="1978-06-22",
        state="CA",
        phone="555-9876",
        email="mtorres@example.com",
        consent_status=ConsentStatus.GRANTED,
    )

    # 1. Video Consultation
    print("\n── 1. VIDEO CONSULTATION ──")
    video_mgr = VideoConsultationManager()
    config = SessionConfig(max_duration_minutes=30, hipaa_mode=True)
    session = video_mgr.schedule_session(
        provider, patient, ConsultationType.LIVE_VIDEO, config, datetime.now()
    )
    print(f"  Scheduled: {session.session_id}")

    video_mgr.checkin_patient(session.session_id)
    print(f"  Status: {session.status.value}")

    video_mgr.start_session(session.session_id)
    print(f"  Session started: {session.started_at}")

    video_mgr.end_session(session.session_id, notes="Follow up in 2 weeks")
    print(f"  Session ended — Duration: {session.duration_seconds():.1f}s")

    metrics = video_mgr.get_session_metrics([session])
    print(f"  Metrics: {json.dumps(metrics, indent=4)}")

    # 2. Remote Patient Monitoring
    print("\n── 2. REMOTE PATIENT MONITORING ──")
    rpm = RPMonitoringService()
    rpm_session = rpm.enroll_patient(patient, provider, [
        DeviceType.BLOOD_PRESSURE_CUFF,
        DeviceType.PULSE_OXIMETER,
        DeviceType.GLUCOMETER,
    ])
    print(f"  Enrolled devices: {[d.value for d in rpm_session.devices]}")

    readings = [
        VitalReading("RD-001", "PAT-001", DeviceType.BLOOD_PRESSURE_CUFF,
                     VitalSign.BLOOD_PRESSURE_SYSTOLIC, 185.0, "mmHg"),
        VitalReading("RD-002", "PAT-001", DeviceType.PULSE_OXIMETER,
                     VitalSign.OXYGEN_SATURATION, 94.0, "%"),
        VitalReading("RD-003", "PAT-001", DeviceType.GLUCOMETER,
                     VitalSign.BLOOD_GLUCOSE, 320.0, "mg/dL"),
        VitalReading("RD-004", "PAT-001", DeviceType.BLOOD_PRESSURE_CUFF,
                     VitalSign.BLOOD_PRESSURE_SYSTOLIC, 125.0, "mmHg"),
    ]

    for reading in readings:
        alert = rpm.record_reading(reading)
        status = f"ALERT: {alert.severity.value} — {alert.message}" if alert else "Normal"
        print(f"  Reading {reading.vital_sign.value}={reading.value}: {status}")

    summary = rpm.get_patient_summary("PAT-001")
    print(f"  Summary: {summary['total_readings']} readings, {summary['total_alerts']} alerts")

    alerts = rpm.get_alerts("PAT-001", unacknowledged_only=True)
    if alerts:
        alerts[0].acknowledge("Dr. Chen")
        print(f"  Acknowledged alert: {alerts[0].alert_id}")

    # 3. E-Prescribing
    print("\n── 3. E-PRESCRIBING ──")
    epcs = EPrescribingService()
    token = epcs.register_epcs_token(provider.provider_id, "smart_card")
    print(f"  EPCS token registered")

    rx = epcs.create_prescription(
        provider, patient, "Lisinopril", "314076", "10mg", "Once daily",
        30, 3, "Take one tablet by mouth daily",
        ControlledSubstanceSchedule.NONE, pharmacy_id="PHARM-001",
    )
    print(f"  Created: {rx.prescription_id} | Med: {rx.medication_name}")

    rx = epcs.sign_prescription(rx.prescription_id)
    print(f"  Signed: {rx.status.value}")

    rx = epcs.transmit_prescription(rx.prescription_id)
    print(f"  Transmitted: {rx.status.value} at {rx.transmitted_at}")

    history = epcs.get_prescription_history("PAT-001")
    print(f"  Prescription history: {len(history)} entries")

    # 4. HIPAA Compliance
    print("\n── 4. HIPAA COMPLIANCE ──")
    compliance = HIPAAComplianceManager()
    compliance.log_access("PROV-001", "provider", "Patient", "PAT-001", "read", "PAT-001")
    compliance.log_access("PROV-001", "provider", "Observation", "obs-001", "read", "PAT-001")
    print(f"  Audit entries: {len(compliance._audit_log)}")

    baa_id = compliance.register_baa(
        "Zoom Healthcare", "video_platform", datetime.now(), datetime.now() + timedelta(days=365)
    )
    print(f"  BAA registered: {baa_id}")

    issues = compliance.validate_session_hipaa(session)
    print(f"  HIPAA issues: {issues if issues else 'None'}")

    dashboard = compliance.get_compliance_dashboard()
    print(f"  Dashboard: {json.dumps(dashboard, indent=4)}")

    audit_trail = compliance.get_audit_trail(patient_id="PAT-001")
    print(f"  Audit trail for PAT-001: {len(audit_trail)} entries")

    print("\n" + "=" * 70)
    print("TELEMEDICINE DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

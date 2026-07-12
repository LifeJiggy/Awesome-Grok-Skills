"""
EHR Integration - HL7 FHIR, Patient Data Exchange, SMART on FHIR, Interoperability
Comprehensive module for electronic health record integration workflows.
"""

from __future__ import annotations

import hashlib
import json
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Generator, Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class FHIRVersion(Enum):
    """Supported FHIR versions."""
    DSTU2 = "dstu2"
    STU3 = "stu3"
    R4 = "r4"
    R5 = "r5"


class ResourceOperation(Enum):
    """CRUD operations on FHIR resources."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    SEARCH = "search"
    VALIDATE = "validate"
    HISTORY = "history"
    BUNDLE = "bundle"


class ConsentScope(Enum):
    """Data access consent scopes."""
    FULL_ACCESS = "full_access"
    DEMOGRAPHICS_ONLY = "demographics_only"
    CLINICAL_SUMMARY = "clinical_summary"
    RESTRICTED = "restricted"
    EMERGENCY_ACCESS = "emergency_access"


class EndpointStatus(Enum):
    """FHIR endpoint operational status."""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    ERROR = "error"
    OFFLINE = "offline"
    TESTING = "testing"


class LaunchMode(Enum):
    """SMART on FHIR app launch modes."""
    EHR_LAUNCH = "ehr_launch"
    STANDALONE_LAUNCH = "standalone_launch"


# ─── Dataclasses ──────────────────────────────────────────────────────────────

@dataclass
class FHIRResource:
    """A generic FHIR resource wrapper."""
    resource_type: str
    resource_id: str
    version_id: str = "1"
    last_updated: datetime = field(default_factory=datetime.utcnow)
    data: dict[str, Any] = field(default_factory=dict)
    meta_profile: str = ""

    def to_bundle_entry(self) -> dict[str, Any]:
        """Convert to a FHIR Bundle entry format."""
        return {
            "fullUrl": f"urn:uuid:{self.resource_id}",
            "resource": {
                "resourceType": self.resource_type,
                "id": self.resource_id,
                "meta": {
                    "versionId": self.version_id,
                    "lastUpdated": self.last_updated.isoformat(),
                    **({"profile": self.meta_profile} if self.meta_profile else {}),
                },
                **self.data,
            },
            "request": {"method": "GET", "url": f"{self.resource_type}/{self.resource_id}"},
        }


@dataclass
class Patient(FHIRResource):
    """FHIR Patient resource."""
    family_name: str = ""
    given_names: list[str] = field(default_factory=list)
    birth_date: Optional[datetime] = None
    gender: str = "unknown"
    mrn: str = ""
    phone: str = ""
    email: str = ""
    address: str = ""
    deceased: bool = False

    def __post_init__(self) -> None:
        self.resource_type = "Patient"
        if not self.data:
            self.data = self._build_patient_data()

    def _build_patient_data(self) -> dict[str, Any]:
        name_entry = {"family": self.family_name, "given": self.given_names}
        telecom = []
        if self.phone:
            telecom.append({"system": "phone", "value": self.phone, "use": "home"})
        if self.email:
            telecom.append({"system": "email", "value": self.email, "use": "home"})
        identifier = []
        if self.mrn:
            identifier.append({
                "type": {"coding": [{"code": "MR", "display": "Medical Record Number"}]},
                "value": self.mrn,
            })
        return {
            "name": [name_entry],
            "telecom": telecom,
            "gender": self.gender,
            "birthDate": self.birth_date.strftime("%Y-%m-%d") if self.birth_date else "",
            "address": [{"line": [self.address]}] if self.address else [],
            "identifier": identifier,
            "deceasedBoolean": self.deceased,
        }

    def display_name(self) -> str:
        parts = self.given_names + [self.family_name]
        return " ".join(parts)


@dataclass
class Observation(FHIRResource):
    """FHIR Observation resource (labs, vitals)."""
    code_loinc: str = ""
    code_display: str = ""
    value_quantity: float = 0.0
    value_unit: str = ""
    status: str = "final"
    effective_date: datetime = field(default_factory=datetime.utcnow)
    patient_reference: str = ""
    interpretation: str = ""

    def __post_init__(self) -> None:
        self.resource_type = "Observation"
        if not self.data:
            self.data = self._build_observation_data()

    def _build_observation_data(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "category": [{"coding": [{"code": "vital-signs", "display": "Vital Signs"}]}],
            "code": {
                "coding": [{"system": "http://loinc.org", "code": self.code_loinc, "display": self.code_display}],
                "text": self.code_display,
            },
            "valueQuantity": {"value": self.value_quantity, "unit": self.value_unit},
            "effectiveDateTime": self.effective_date.isoformat(),
            "subject": {"reference": f"Patient/{self.patient_reference}"},
        }


@dataclass
class Condition(FHIRResource):
    """FHIR Condition resource."""
    code_icd10: str = ""
    code_display: str = ""
    clinical_status: str = "active"
    verification_status: str = "confirmed"
    onset_date: Optional[datetime] = None
    patient_reference: str = ""
    severity: str = ""

    def __post_init__(self) -> None:
        self.resource_type = "Condition"
        if not self.data:
            self.data = self._build_condition_data()

    def _build_condition_data(self) -> dict[str, Any]:
        return {
            "clinicalStatus": {"coding": [{"code": self.clinical_status}]},
            "verificationStatus": {"coding": [{"code": self.verification_status}]},
            "category": [{"coding": [{"code": "encounter-diagnosis", "display": "Encounter Diagnosis"}]}],
            "code": {
                "coding": [{"system": "http://hl7.org/fhir/sid/icd-10-cm", "code": self.code_icd10, "display": self.code_display}],
                "text": self.code_display,
            },
            "subject": {"reference": f"Patient/{self.patient_reference}"},
        }


@dataclass
class MedicationRequest(FHIRResource):
    """FHIR MedicationRequest resource."""
    medication_code: str = ""
    medication_display: str = ""
    dosage_instruction: str = ""
    status: str = "active"
    intent: str = "order"
    authored_on: datetime = field(default_factory=datetime.utcnow)
    patient_reference: str = ""
    prescriber_reference: str = ""
    quantity_value: float = 0.0
    quantity_unit: str = ""

    def __post_init__(self) -> None:
        self.resource_type = "MedicationRequest"
        if not self.data:
            self.data = self._build_rx_data()

    def _build_rx_data(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "intent": self.intent,
            "medicationCodeableConcept": {
                "coding": [{"system": "http://www.nlm.nih.gov/research/umls/rxnorm", "code": self.medication_code, "display": self.medication_display}],
                "text": self.medication_display,
            },
            "subject": {"reference": f"Patient/{self.patient_reference}"},
            "authoredOn": self.authored_on.isoformat(),
            "dosageInstruction": [{"text": self.dosage_instruction}],
            "dispenseRequest": {
                "quantity": {"value": self.quantity_value, "unit": self.quantity_unit},
            },
        }


@dataclass
class Encounter(FHIRResource):
    """FHIR Encounter resource."""
    status: str = "in-progress"
    class_code: str = "AMB"
    type_display: str = ""
    start_time: datetime = field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    patient_reference: str = ""
    service_provider: str = ""

    def __post_init__(self) -> None:
        self.resource_type = "Encounter"


@dataclass
class FHIRBundle:
    """A FHIR Bundle for transactional or batch operations."""
    bundle_type: str = "collection"
    bundle_id: str = field(default_factory=lambda: f"bundle-{uuid.uuid4().hex[:8]}")
    entries: list[FHIRResource] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_json(self) -> dict[str, Any]:
        return {
            "resourceType": "Bundle",
            "id": self.bundle_id,
            "type": self.bundle_type,
            "timestamp": self.timestamp.isoformat(),
            "total": len(self.entries),
            "entry": [entry.to_bundle_entry() for entry in self.entries],
        }


@dataclass
class SMARTSession:
    """Represents an active SMART on FHIR session."""
    session_id: str
    patient_id: str
    encounter_id: str = ""
    scopes: list[str] = field(default_factory=list)
    launch_mode: LaunchMode = LaunchMode.STANDALONE_LAUNCH
    access_token: str = ""
    refresh_token: str = ""
    expires_at: datetime = field(default_factory=lambda: datetime.utcnow() + timedelta(hours=1))
    token_type: str = "Bearer"

    def is_expired(self) -> bool:
        return datetime.utcnow() >= self.expires_at

    def has_scope(self, scope: str) -> bool:
        return scope in self.scopes


@dataclass
class EndpointConfig:
    """FHIR server endpoint configuration."""
    base_url: str
    fhir_version: FHIRVersion = FHIRVersion.R4
    status: EndpointStatus = EndpointStatus.ACTIVE
    auth_type: str = "oauth2"
    timeout_seconds: int = 30
    verify_ssl: bool = True
    custom_headers: dict[str, str] = field(default_factory=dict)


@dataclass
class ConsentRecord:
    """Patient consent for data sharing."""
    consent_id: str
    patient_id: str
    scope: ConsentScope
    granted_to: list[str] = field(default_factory=list)
    expires_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def is_valid(self) -> bool:
        if self.expires_at and datetime.utcnow() > self.expires_at:
            return False
        return self.scope != ConsentScope.RESTRICTED


@dataclass
class SearchParams:
    """FHIR search parameters."""
    resource_type: str
    filters: dict[str, str] = field(default_factory=dict)
    sort: str = ""
    count: int = 10
    include: list[str] = field(default_factory=list)
    page: int = 1

    def to_query_string(self) -> str:
        parts = []
        for key, value in self.filters.items():
            parts.append(f"{key}={value}")
        if self.sort:
            parts.append(f"_sort={self.sort}")
        parts.append(f"_count={self.count}")
        if self.include:
            parts.append(f"_include={','.join(self.include)}")
        parts.append(f"page={self.page}")
        return "&".join(parts)


# ─── Service Classes ──────────────────────────────────────────────────────────

class FHIRClient:
    """Client for interacting with a FHIR server."""

    def __init__(self, endpoint: EndpointConfig) -> None:
        self.endpoint = endpoint
        self._resource_store: dict[str, dict[str, FHIRResource]] = {}
        self._request_log: list[dict[str, Any]] = []

    def create_resource(self, resource: FHIRResource) -> FHIRResource:
        """Create a new FHIR resource."""
        key = f"{resource.resource_type}/{resource.resource_id}"
        self._resource_store[key] = resource
        self._log_request("POST", key, 201)
        return resource

    def read_resource(self, resource_type: str, resource_id: str) -> Optional[FHIRResource]:
        """Read a FHIR resource by type and ID."""
        key = f"{resource_type}/{resource_id}"
        resource = self._resource_store.get(key)
        self._log_request("GET", key, 200 if resource else 404)
        return resource

    def update_resource(self, resource: FHIRResource) -> FHIRResource:
        """Update an existing FHIR resource."""
        key = f"{resource.resource_type}/{resource.resource_id}"
        resource.version_id = str(int(resource.version_id) + 1)
        resource.last_updated = datetime.utcnow()
        self._resource_store[key] = resource
        self._log_request("PUT", key, 200)
        return resource

    def delete_resource(self, resource_type: str, resource_id: str) -> bool:
        """Delete a FHIR resource."""
        key = f"{resource_type}/{resource_id}"
        deleted = key in self._resource_store
        self._resource_store.pop(key, None)
        self._log_request("DELETE", key, 204 if deleted else 404)
        return deleted

    def search(self, params: SearchParams) -> list[FHIRResource]:
        """Search for FHIR resources."""
        results: list[FHIRResource] = []
        for key, resource in self._resource_store.items():
            if resource.resource_type == params.resource_type:
                matches = True
                for filter_key, filter_value in params.filters.items():
                    res_value = resource.data.get(filter_key, "")
                    if isinstance(res_value, list) and res_value:
                        res_value = res_value[0]
                    if filter_value.lower() not in str(res_value).lower():
                        matches = False
                        break
                if matches:
                    results.append(resource)
        self._log_request("GET", f"{params.resource_type}?{params.to_query_string()}", 200)
        start_idx = (params.page - 1) * params.count
        return results[start_idx : start_idx + params.count]

    def validate_resource(self, resource: FHIRResource) -> tuple[bool, list[str]]:
        """Validate a FHIR resource against basic rules."""
        errors: list[str] = []
        if not resource.resource_type:
            errors.append("Missing resourceType")
        if not resource.resource_id:
            errors.append("Missing resource id")
        if resource.resource_type == "Patient":
            patient = resource if isinstance(resource, Patient) else None
            if patient and not patient.family_name:
                errors.append("Patient must have a family name")
        if resource.resource_type == "Observation":
            obs = resource if isinstance(resource, Observation) else None
            if obs and not obs.code_loinc:
                errors.append("Observation must have a LOINC code")
        return (len(errors) == 0, errors)

    def get_capability_statement(self) -> dict[str, Any]:
        """Return a capability statement for the FHIR server."""
        return {
            "resourceType": "CapabilityStatement",
            "status": "active",
            "fhirVersion": self.endpoint.fhir_version.value,
            "format": ["json"],
            "rest": [{
                "mode": "server",
                "resource": [
                    {"type": "Patient", "interaction": [{"code": "read"}, {"code": "search-type"}]},
                    {"type": "Observation", "interaction": [{"code": "read"}, {"code": "search-type"}]},
                    {"type": "Condition", "interaction": [{"code": "read"}, {"code": "search-type"}]},
                    {"type": "MedicationRequest", "interaction": [{"code": "read"}, {"code": "create"}]},
                    {"type": "Encounter", "interaction": [{"code": "read"}, {"code": "search-type"}]},
                ],
            }],
        }

    def _log_request(self, method: str, path: str, status: int) -> None:
        self._request_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "method": method,
            "path": path,
            "status": status,
        })

    def get_request_log(self) -> list[dict[str, Any]]:
        return self._request_log.copy()


class SMARTOnFHIRAuth:
    """SMART on FHIR authorization handler."""

    def __init__(self) -> None:
        self._active_sessions: dict[str, SMARTSession] = {}
        self._client_registrations: dict[str, dict[str, Any]] = {}

    def register_client(
        self, client_name: str, redirect_uris: list[str], scopes: list[str]
    ) -> str:
        """Register a SMART on FHIR client application."""
        client_id = f"client-{uuid.uuid4().hex[:10]}"
        self._client_registrations[client_id] = {
            "client_name": client_name,
            "redirect_uris": redirect_uris,
            "allowed_scopes": scopes,
            "registered_at": datetime.utcnow().isoformat(),
        }
        return client_id

    def initiate_ehr_launch(
        self, client_id: str, iss: str, launch_token: str, scopes: list[str]
    ) -> dict[str, str]:
        """Simulate EHR-launch flow — returns authorization URL components."""
        if client_id not in self._client_registrations:
            raise ValueError(f"Unknown client: {client_id}")

        state = uuid.uuid4().hex
        return {
            "authorization_url": f"{iss}/authorize",
            "response_type": "code",
            "client_id": client_id,
            "redirect_uri": self._client_registrations[client_id]["redirect_uris"][0],
            "scope": " ".join(scopes),
            "state": state,
            "aud": iss,
            "launch": launch_token,
        }

    def initiate_standalone_launch(
        self, client_id: str, authorization_url: str, scopes: list[str]
    ) -> dict[str, str]:
        """Simulate standalone-launch flow."""
        if client_id not in self._client_registrations:
            raise ValueError(f"Unknown client: {client_id}")

        state = uuid.uuid4().hex
        return {
            "authorization_url": authorization_url,
            "response_type": "code",
            "client_id": client_id,
            "scope": " ".join(scopes),
            "state": state,
        }

    def exchange_code(self, client_id: str, auth_code: str, patient_id: str) -> SMARTSession:
        """Exchange authorization code for access token (simulated)."""
        if client_id not in self._client_registrations:
            raise ValueError(f"Unknown client: {client_id}")

        session = SMARTSession(
            session_id=f"session-{uuid.uuid4().hex[:10]}",
            patient_id=patient_id,
            scopes=self._client_registrations[client_id]["allowed_scopes"],
            access_token=f"access-{uuid.uuid4().hex}",
            refresh_token=f"refresh-{uuid.uuid4().hex}",
        )
        self._active_sessions[session.session_id] = session
        return session

    def refresh_token(self, session_id: str) -> Optional[SMARTSession]:
        """Refresh an expired access token."""
        session = self._active_sessions.get(session_id)
        if not session:
            return None
        session.access_token = f"access-{uuid.uuid4().hex}"
        session.expires_at = datetime.utcnow() + timedelta(hours=1)
        return session

    def validate_access(
        self, session_id: str, required_scope: str
    ) -> tuple[bool, str]:
        """Validate that a session has the required scope and is not expired."""
        session = self._active_sessions.get(session_id)
        if not session:
            return False, "Session not found"
        if session.is_expired():
            return False, "Session expired"
        if not session.has_scope(required_scope):
            return False, f"Missing scope: {required_scope}"
        return True, "Access granted"

    def revoke_session(self, session_id: str) -> bool:
        """Revoke an active session."""
        return self._active_sessions.pop(session_id, None) is not None


class TerminologyService:
    """Service for resolving medical terminology codes."""

    def __init__(self) -> None:
        self._snomed_codes: dict[str, str] = {
            "hypertension": "38341003",
            "diabetes_mellitus_type_2": "44054006",
            "pneumonia": "233678006",
            "asthma": "195967001",
            "copd": "13645005",
            "atrial_fibrillation": "49436004",
            "heart_failure": "84114007",
            "chronic_kidney_disease": "723188008",
        }
        self._loinc_codes: dict[str, str] = {
            "blood_pressure_systolic": "8480-6",
            "blood_pressure_diastolic": "8462-4",
            "heart_rate": "8867-4",
            "respiratory_rate": "9279-1",
            "body_temperature": "8310-5",
            "body_weight": "29463-7",
            "body_height": "8302-2",
            "hba1c": "4548-4",
            "glucose": "2345-7",
            "creatinine": "2160-0",
            "hemoglobin": "718-7",
            "wbc_count": "6690-2",
            "platelet_count": "777-3",
        }
        self._rxnorm_codes: dict[str, str] = {
            "aspirin": "1191",
            "metformin": "860975",
            "lisinopril": "314076",
            "warfarin": "11289",
            "atorvastatin": "83367",
            "amlodipine": "1734919",
            "omeprazole": "7646",
            "metoprolol": "69166",
            "hydrochlorothiazide": "5604",
            "amoxicillin": "723",
        }

    def lookup_snomed(self, term: str) -> Optional[str]:
        return self._snomed_codes.get(term.lower().strip())

    def lookup_loinc(self, term: str) -> Optional[str]:
        return self._loinc_codes.get(term.lower().strip())

    def lookup_rxnorm(self, term: str) -> Optional[str]:
        return self._rxnorm_codes.get(term.lower().strip())

    def resolve_code(self, system: str, term: str) -> Optional[str]:
        lookup_map = {
            "snomed": self.lookup_snomed,
            "loinc": self.lookup_loinc,
            "rxnorm": self.lookup_rxnorm,
        }
        resolver = lookup_map.get(system.lower())
        return resolver(term) if resolver else None


class ConsentManager:
    """Manages patient consent for data sharing."""

    def __init__(self) -> None:
        self._consents: dict[str, ConsentRecord] = {}

    def record_consent(
        self,
        patient_id: str,
        scope: ConsentScope,
        granted_to: list[str],
        expires_in_days: int = 365,
    ) -> ConsentRecord:
        """Record patient consent for data sharing."""
        consent = ConsentRecord(
            consent_id=f"CONSENT-{uuid.uuid4().hex[:8]}",
            patient_id=patient_id,
            scope=scope,
            granted_to=granted_to,
            expires_at=datetime.utcnow() + timedelta(days=expires_in_days),
        )
        self._consents[consent.consent_id] = consent
        return consent

    def check_consent(
        self, patient_id: str, requesting_app: str
    ) -> tuple[bool, ConsentScope]:
        """Check if a patient has granted consent to a requesting application."""
        for consent in self._consents.values():
            if consent.patient_id == patient_id:
                if consent.is_valid() and (
                    requesting_app in consent.granted_to or consent.scope == ConsentScope.FULL_ACCESS
                ):
                    return True, consent.scope
        return False, ConsentScope.RESTRICTED

    def revoke_consent(self, consent_id: str) -> bool:
        """Revoke a consent record."""
        consent = self._consents.pop(consent_id, None)
        if consent:
            consent.scope = ConsentScope.RESTRICTED
            return True
        return False


class FHIRDataExporter:
    """Export patient data as FHIR Bulk Data bundles."""

    def __init__(self, client: FHIRClient) -> None:
        self.client = client

    def export_patient_summary(self, patient: Patient) -> FHIRBundle:
        """Export a complete patient summary as a FHIR Bundle."""
        bundle = FHIRBundle(bundle_type="collection")
        bundle.entries.append(patient)

        observations = self.client.search(
            SearchParams(
                resource_type="Observation",
                filters={"subject": f"Patient/{patient.resource_id}"},
            )
        )
        bundle.entries.extend(observations)

        conditions = self.client.search(
            SearchParams(
                resource_type="Condition",
                filters={"subject": f"Patient/{patient.resource_id}"},
            )
        )
        bundle.entries.extend(conditions)

        return bundle

    def export_clinical_document(
        self, patient_id: str, document_type: str
    ) -> dict[str, Any]:
        """Export a Clinical Document Architecture (CDA) style document."""
        return {
            "document": {
                "type": document_type,
                "patient_id": patient_id,
                "sections": [
                    {"title": "Patient Demographics", "entries": []},
                    {"title": "Problem List", "entries": []},
                    {"title": "Medications", "entries": []},
                    {"title": "Allergies", "entries": []},
                    {"title": "Laboratory Results", "entries": []},
                    {"title": "Vital Signs", "entries": []},
                ],
            }
        }


# ─── Demo ─────────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate EHR integration capabilities."""
    print("=" * 70)
    print("EHR INTEGRATION DEMONSTRATION")
    print("=" * 70)

    # 1. FHIR Client
    print("\n── 1. FHIR CLIENT ──")
    endpoint = EndpointConfig(base_url="https://fhir.hospital.org/r4", fhir_version=FHIRVersion.R4)
    client = FHIRClient(endpoint)

    patient = Patient(
        resource_id="patient-001",
        family_name="Johnson",
        given_names=["Robert", "James"],
        birth_date=datetime(1955, 3, 15),
        gender="male",
        mrn="MRN-2024-001234",
        phone="555-0123",
        email="rjohnson@example.com",
    )
    created = client.create_resource(patient)
    print(f"  Created Patient: {created.display_name()} (MRN: {created.mrn})")

    # Read back
    read_patient = client.read_resource("Patient", "patient-001")
    print(f"  Read Patient: {read_patient.display_name() if read_patient else 'Not found'}")

    # Observations
    bp_systolic = Observation(
        resource_id="obs-001",
        code_loinc="8480-6",
        code_display="Systolic Blood Pressure",
        value_quantity=142.0,
        value_unit="mmHg",
        patient_reference="patient-001",
    )
    hba1c = Observation(
        resource_id="obs-002",
        code_loinc="4548-4",
        code_display="HbA1c",
        value_quantity=7.8,
        value_unit="%",
        patient_reference="patient-001",
    )
    client.create_resource(bp_systolic)
    client.create_resource(hba1c)
    print(f"  Created Observations: SBP={bp_systolic.value_quantity}, HbA1c={hba1c.value_quantity}")

    # Condition
    ht = Condition(
        resource_id="cond-001",
        code_icd10="I10",
        code_display="Essential Hypertension",
        patient_reference="patient-001",
    )
    client.create_resource(ht)
    print(f"  Created Condition: {ht.code_display}")

    # Search
    results = client.search(SearchParams(resource_type="Observation"))
    print(f"  Search Observations: {len(results)} found")

    # Validate
    valid, errors = client.validate_resource(patient)
    print(f"  Patient valid: {valid} | Errors: {errors}")

    # Capability
    cap = client.get_capability_statement()
    print(f"  Server FHIR version: {cap['fhirVersion']}")

    # 2. SMART on FHIR Auth
    print("\n── 2. SMART ON FHIR AUTH ──")
    auth = SMARTOnFHIRAuth()
    client_id = auth.register_client(
        "MyHealthApp",
        ["https://myhealthapp.com/callback"],
        ["patient/*.read", "launch"],
    )
    print(f"  Registered client: {client_id}")

    auth_params = auth.initiate_ehr_launch(
        client_id, "https://fhir.hospital.org/r4", "launch-token-abc", ["patient/*.read"]
    )
    print(f"  EHR Launch: auth_url={auth_params['authorization_url']}")
    print(f"  Scopes: {auth_params['scope']}")

    session = auth.exchange_code(client_id, "auth-code-xyz", "patient-001")
    print(f"  Session created: {session.session_id}")
    print(f"  Token expired: {session.is_expired()}")

    ok, msg = auth.validate_access(session.session_id, "patient/Observation.read")
    print(f"  Access check (Observation.read): {ok} — {msg}")

    # 3. Terminology Service
    print("\n── 3. TERMINOLOGY SERVICE ──")
    terminology = TerminologyService()
    snomed = terminology.resolve_code("snomed", "hypertension")
    loinc = terminology.resolve_code("loinc", "blood_pressure_systolic")
    rxnorm = terminology.resolve_code("rxnorm", "aspirin")
    print(f"  SNOMED 'hypertension': {snomed}")
    print(f"  LOINC 'systolic BP': {loinc}")
    print(f"  RxNorm 'aspirin': {rxnorm}")

    # 4. Consent Manager
    print("\n── 4. CONSENT MANAGER ──")
    consent_mgr = ConsentManager()
    consent = consent_mgr.record_consent(
        "patient-001", ConsentScope.CLINICAL_SUMMARY, ["MyHealthApp"]
    )
    print(f"  Consent recorded: {consent.consent_id} (scope: {consent.scope.value})")

    ok, scope = consent_mgr.check_consent("patient-001", "MyHealthApp")
    print(f"  Consent check (MyHealthApp): {ok} — scope: {scope.value}")

    ok2, scope2 = consent_mgr.check_consent("patient-001", "UnknownApp")
    print(f"  Consent check (UnknownApp): {ok2} — scope: {scope2.value}")

    # 5. Data Export
    print("\n── 5. DATA EXPORT ──")
    exporter = FHIRDataExporter(client)
    bundle = exporter.export_patient_summary(patient)
    bundle_json = bundle.to_json()
    print(f"  Bundle: {bundle_json['type']} | Entries: {bundle_json['total']}")
    for entry in bundle_json["entry"]:
        res = entry["resource"]
        print(f"    {res['resourceType']}/{res['id']}")

    cda = exporter.export_clinical_document("patient-001", "Continuity of Care Document")
    print(f"  CDA sections: {[s['title'] for s in cda['document']['sections']]}")

    print("\n" + "=" * 70)
    print("EHR INTEGRATION DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

# Healthcare Agent

> Healthcare IT platform for HL7/FHIR integration, EHR management, clinical workflows, patient data management, and HIPAA compliance.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Examples](#examples)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Architecture](#architecture)
- [Security](#security)
- [Compliance](#compliance)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Healthcare Agent provides a comprehensive healthcare IT toolkit for modern clinical applications. It implements HL7 FHIR R4 standards, HIPAA compliance requirements, and clinical best practices for patient management, decision support, and interoperability.

### Key Capabilities

- **Patient Management**: FHIR-compliant patient records with demographics, identifiers, and clinical data
- **Clinical Decision Support**: Real-time alerts for drug interactions, allergies, and critical vitals
- **Drug Interaction Checker**: Known drug-drug and drug-allergy interaction database
- **FHIR Validator**: Validates FHIR resource conformance
- **Lab Analyzer**: Result tracking, trending, and critical value detection
- **Appointment Scheduler**: Provider scheduling with conflict detection
- **Claims Processor**: Insurance claim submission and tracking
- **HIPAA Compliance**: Access logging, de-identification, and compliance reporting
- **Workflow Manager**: Clinical care pathway management

### Design Principles

1. **Patient Safety First**: Every decision prioritizes patient safety
2. **Compliance-Conscious**: HIPAA and regulatory compliance is non-negotiable
3. **Evidence-Based**: Use clinical guidelines and data to support decisions
4. **Interoperable**: Design for system integration and data exchange
5. **Precise**: Medical data demands accuracy — no approximations

---

## Features

| Category | Capabilities |
|----------|-------------|
| Patient | FHIR Patient resource, demographics, identifiers, clinical data |
| CDS | Drug interactions, allergy conflicts, vital sign monitoring |
| Medication | Prescription management, interaction checking, refill tracking |
| Lab | Result storage, trending, critical value detection |
| Scheduling | Provider booking, slot availability, conflict detection |
| Claims | Submission, validation, payment tracking, denial management |
| Compliance | Audit logging, access control, de-identification, reporting |
| Workflows | Care pathway creation, step tracking, completion monitoring |

---

## Quick Start

### Basic Usage

```python
from agents.healthcare.agent import Patient, HumanName, Gender, ClinicalDecisionSupport, Medication

# Create patient
patient = Patient(
    patient_id="P001",
    name=HumanName(family="Smith", given=["John"]),
    gender=Gender.MALE,
    birth_date=datetime(1980, 5, 15),
)

# Check drug interactions
cds = ClinicalDecisionSupport()
meds = [Medication("M001", "P001", "Warfarin", "5mg", "daily")]
alerts = cds.check_patient(patient, meds)
```

### Run the Agent

```bash
python agents/healthcare/agent.py
```

### Full Example

```python
from agents.healthcare.agent import (
    Patient, HumanName, Identifier, Gender, Address, ContactPoint,
    Medication, Allergy, Condition, Observation, Encounter, Claim,
    Appointment, ClinicalDecisionSupport, DrugInteractionChecker,
    FHIRValidator, LabAnalyzer, AppointmentScheduler, ClaimsProcessor,
    HIPAACompliance, WorkflowManager, InsuranceType, AllergySeverity,
    LabStatus, EncounterType, AppointmentStatus, MedicationStatus
)
from datetime import datetime

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

# Create medications
meds = [
    Medication("M001", "P001", "Warfarin", "5mg", "daily"),
    Medication("M002", "P001", "Aspirin", "81mg", "daily"),
]

# Clinical Decision Support
cds = ClinicalDecisionSupport()
alerts = cds.check_patient(patient, meds)
print(f"Clinical Alerts: {len(alerts)}")
for a in alerts:
    print(f"  [{a.priority.name}] {a.message}")

# FHIR Validation
validator = FHIRValidator()
validation = validator.validate_patient(patient)
print(f"FHIR Validation: {'PASS' if validation['valid'] else 'FAIL'}")

# Lab Results
lab_analyzer = LabAnalyzer()
lab_analyzer.add_result(Observation("O001", "P001", "glucose", "Blood Glucose", 126, "mg/dL",
    reference_range_low=70, reference_range_high=100))
critical = lab_analyzer.get_critical_results("P001")
print(f"Critical Results: {len(critical)}")

# HIPAA Compliance
hipaa = HIPAACompliance()
hipaa.log_access("read", "Patient", "P001", "dr.jones", "physician", "P001")
report = hipaa.generate_compliance_report()
print(f"HIPAA Report: {report['audit_events']} events")

# Appointment Scheduling
scheduler = AppointmentScheduler()
scheduler.register_provider("DR001", "Dr. Jones", "Internal Medicine")
available = scheduler.get_available_slots("DR001", datetime(2025, 7, 10))
print(f"Available slots: {len(available)}")

# Insurance Claims
claims = ClaimsProcessor()
claim = claims.submit_claim("P001", "ENC001", ["E11.9"], ["99213"], 150.0)
claims.process_claim(claim.claim_id, 120.0)
summary = claims.claims_summary()
print(f"Claims: {summary['total_claims']} total, ${summary['total_paid']:.2f} paid")

# Clinical Workflow
wf_mgr = WorkflowManager()
workflow = wf_mgr.create_workflow("P001", "Admission", [
    {"type": "assessment", "description": "Initial assessment"},
    {"type": "order", "description": "Admission orders"},
    {"type": "procedure", "description": "IV placement"},
])
wf_mgr.complete_step(workflow.workflow_id, workflow.steps[0].step_id)
status = wf_mgr.get_workflow_status(workflow.workflow_id)
print(f"Workflow: {status['name']} - {status['completion_pct']:.0%} complete")
```

---

## Installation

### From Source

```bash
git clone https://github.com/awesome-grok-skills/healthcare-agent.git
cd healthcare-agent
pip install -e .
```

### Dependencies

The Healthcare Agent uses only Python standard library modules. No external dependencies required.

### Requirements

- Python 3.8+
- No external packages required

---

## Usage

### Patient Management

```python
from agents.healthcare.agent import Patient, HumanName, Identifier, Gender

# Create patient
patient = Patient(
    patient_id="P001",
    identifiers=[Identifier("http://hospital.org/mrn", "MRN-12345", "usual", "MR")],
    name=HumanName(family="Smith", given=["John", "Michael"]),
    gender=Gender.MALE,
    birth_date=datetime(1980, 5, 15),
)

# Access patient properties
print(patient.full_name)  # "John Michael Smith"
print(patient.age)        # 46
print(patient.mrn)        # "MRN-12345"
print(patient.is_active)  # True

# FHIR serialization
fhir = patient.to_fhir()
```

### Clinical Decision Support

```python
from agents.healthcare.agent import ClinicalDecisionSupport, Medication

cds = ClinicalDecisionSupport()

# Check for drug interactions
medications = [
    Medication("M001", "P001", "Warfarin", "5mg", "daily"),
    Medication("M002", "P001", "Aspirin", "81mg", "daily"),
]

alerts = cds.check_patient(patient, medications)
for alert in alerts:
    print(f"[{alert.priority.name}] {alert.message}")

# Check vital signs
vitals = {"heart_rate": 45, "systolic_bp": 190, "oxygen_saturation": 88}
vital_alerts = cds.check_vitals(patient, vitals)
```

### Drug Interaction Checking

```python
from agents.healthcare.agent import DrugInteractionChecker

checker = DrugInteractionChecker()

# Check drug-drug interactions
interactions = checker.check_interactions(["warfarin", "aspirin", "metformin"])
for i in interactions:
    print(f"[{i.severity}] {i.drug_a} + {i.drug_b}: {i.description}")

# Check drug-allergy conflicts
conflicts = checker.check_allergy_conflict(
    medications=["penicillin", "amoxicillin"],
    allergies=["penicillin"]
)

# Get overall severity
severity = checker.get_severity_level(interactions)
```

### FHIR Validation

```python
from agents.healthcare.agent import FHIRValidator

validator = FHIRValidator()

# Validate patient resource
result = validator.validate_patient(patient)
print(f"Valid: {result['valid']}, Errors: {result['errors']}, Warnings: {result['warnings']}")

# Validate medication
from agents.healthcare.agent import Medication
med = Medication("M001", "P001", "Lisinopril", "10mg", "daily", prescriber="Dr. Jones")
result = validator.validate_medication(med)
```

### Lab Result Analysis

```python
from agents.healthcare.agent import LabAnalyzer, Observation

lab = LabAnalyzer()

# Add results
lab.add_result(Observation("O001", "P001", "glucose", "Blood Glucose", 126, "mg/dL",
    reference_range_low=70, reference_range_high=100))
lab.add_result(Observation("O002", "P001", "hba1c", "HbA1c", 7.2, "%",
    reference_range_low=4.0, reference_range_high=5.7))

# Get critical results
critical = lab.get_critical_results("P001")
for r in critical:
    print(f"CRITICAL: {r.display} = {r.value} {r.unit}")

# Get trend
trend = lab.get_trend("P001", "glucose")
print(f"Trend: {trend['trend']}, Change: {trend['change_pct']:.1f}%")

# Generate summary
summary = lab.generate_summary("P001")
```

### Appointment Scheduling

```python
from agents.healthcare.agent import AppointmentScheduler

scheduler = AppointmentScheduler()

# Register provider
scheduler.register_provider("DR001", "Dr. Jones", "Internal Medicine")

# Get available slots
slots = scheduler.get_available_slots("DR001", datetime(2025, 7, 10))
print(f"Available: {len(slots)} slots")

# Book appointment
appt = scheduler.book_appointment(
    patient_id="P001",
    provider_id="DR001",
    start_time=slots[0] if slots else datetime(2025, 7, 10, 9, 0),
    duration_minutes=30,
    reason="Annual physical"
)
```

### Insurance Claims

```python
from agents.healthcare.agent import ClaimsProcessor, InsuranceType

claims = ClaimsProcessor()

# Submit claim
claim = claims.submit_claim(
    patient_id="P001",
    encounter_id="ENC001",
    diagnosis_codes=["E11.9", "I10"],
    procedure_codes=["99213", "80053"],
    total_amount=250.0,
    insurance_type=InsuranceType.PRIVATE
)

# Validate
validation = claims.validate_claim(claim.claim_id)

# Process payment
claims.process_claim(claim.claim_id, paid_amount=200.0)

# Summary
summary = claims.claims_summary()
```

### HIPAA Compliance

```python
from agents.healthcare.agent import HIPAACompliance

hipaa = HIPAACompliance()

# Log access
hipaa.log_access("read", "Patient", "P001", "dr.jones", "physician", "P001")
hipaa.log_access("write", "Medication", "M001", "dr.jones", "physician", "P001")

# Check access permissions
allowed = hipaa.check_access("physician", "Patient", "read")  # True
allowed = hipaa.check_access("nurse", "Patient", "delete")    # False

# De-identify patient
deidentified = hipaa.deidentify(patient)

# Generate compliance report
report = hipaa.generate_compliance_report()
```

### Clinical Workflows

```python
from agents.healthcare.agent import WorkflowManager

wf_mgr = WorkflowManager()

# Create admission workflow
workflow = wf_mgr.create_workflow("P001", "Admission", [
    {"type": "assessment", "description": "Initial assessment"},
    {"type": "order", "description": "Admission orders"},
    {"type": "procedure", "description": "IV placement"},
    {"type": "notification", "description": "Notify family"},
])

# Complete steps
wf_mgr.complete_step(workflow.workflow_id, workflow.steps[0].step_id)

# Check status
status = wf_mgr.get_workflow_status(workflow.workflow_id)
print(f"Workflow: {status['name']} - {status['completion_pct']:.0%} complete")
```

---

## API Reference

### Patient

| Property/Method | Description |
|-----------------|-------------|
| `patient_id` | Unique identifier |
| `identifiers` | List of identifiers (MRN, SSN, etc.) |
| `name` | Patient name (HumanName) |
| `gender` | Gender (MALE, FEMALE, OTHER, UNKNOWN) |
| `birth_date` | Date of birth |
| `age` | Calculated age from birth_date |
| `mrn` | Medical Record Number |
| `is_active` | Active status |
| `full_name` | Full name string |
| `to_fhir()` | FHIR resource serialization |

### Medication

| Property/Method | Description |
|-----------------|-------------|
| `medication_id` | Unique identifier |
| `patient_id` | Patient reference |
| `medication_name` | Medication name |
| `dosage` | Dosage (e.g., "5mg") |
| `frequency` | Frequency (e.g., "daily") |
| `is_active` | Active status |
| `days_remaining` | Days until end_date |

### ClinicalDecisionSupport

| Method | Description |
|--------|-------------|
| `check_patient(patient, medications)` | Check drug interactions and allergies |
| `check_vitals(patient, vitals)` | Check vital signs |
| `get_active_alerts(patient_id)` | Get active alerts |
| `acknowledge_alert(alert_id, user_id)` | Acknowledge alert |

### DrugInteractionChecker

| Method | Description |
|--------|-------------|
| `check_interactions(medications)` | Check drug-drug interactions |
| `check_allergy_conflict(medications, allergies)` | Check drug-allergy conflicts |
| `get_severity_level(interactions)` | Get overall severity |

### FHIRValidator

| Method | Description |
|--------|-------------|
| `validate_patient(patient)` | Validate patient FHIR resource |
| `validate_medication(medication)` | Validate medication FHIR resource |
| `validate_observation(observation)` | Validate observation FHIR resource |

### LabAnalyzer

| Method | Description |
|--------|-------------|
| `add_result(observation)` | Add lab result |
| `get_patient_results(patient_id, code)` | Get patient results |
| `get_critical_results(patient_id)` | Get critical results |
| `get_trend(patient_id, code)` | Get result trend |
| `generate_summary(patient_id)` | Generate summary |

### AppointmentScheduler

| Method | Description |
|--------|-------------|
| `register_provider(provider_id, name, specialty)` | Register provider |
| `book_appointment(patient_id, provider_id, start_time)` | Book appointment |
| `cancel_appointment(appointment_id)` | Cancel appointment |
| `get_provider_schedule(provider_id, date)` | Get provider schedule |
| `get_available_slots(provider_id, date)` | Get available slots |

### ClaimsProcessor

| Method | Description |
|--------|-------------|
| `submit_claim(patient_id, encounter_id, ...)` | Submit claim |
| `validate_claim(claim_id)` | Validate claim |
| `process_claim(claim_id, paid_amount)` | Process payment |
| `get_claims_by_patient(patient_id)` | Get patient claims |
| `claims_summary()` | Get claims summary |

### HIPAACompliance

| Method | Description |
|--------|-------------|
| `log_access(action, resource_type, ...)` | Log data access |
| `check_access(user_role, resource_type, action)` | Check permissions |
| `deidentify(patient)` | De-identify patient data |
| `get_access_summary()` | Get access summary |
| `generate_compliance_report()` | Generate report |

### WorkflowManager

| Method | Description |
|--------|-------------|
| `create_workflow(patient_id, name, steps)` | Create workflow |
| `complete_step(workflow_id, step_id)` | Complete step |
| `get_workflow_status(workflow_id)` | Get status |
| `get_patient_workflows(patient_id)` | Get patient workflows |

---

## Configuration

### Clinical Decision Support

```python
from agents.healthcare.agent import ClinicalDecisionSupport

cds = ClinicalDecisionSupport()

# Custom vital sign thresholds
custom_thresholds = {
    "heart_rate": (60, 100),
    "systolic_bp": (100, 140),
    "diastolic_bp": (60, 90),
    "temperature": (36.0, 37.5),
    "oxygen_saturation": (95, 100),
    "respiratory_rate": (12, 20),
}
```

### HIPAA Compliance

```python
from agents.healthcare.agent import HIPAACompliance

hipaa = HIPAACompliance()

# Custom access policies
hipaa.access_policies = {
    "physician:Patient:read": True,
    "physician:Patient:write": True,
    "nurse:Patient:read": True,
    "nurse:Patient:write_vitals": True,
    "admin:Patient:delete": True,
    "billing:Patient:read_billing": True,
}
```

### Appointment Scheduler

```python
from agents.healthcare.agent import AppointmentScheduler

scheduler = AppointmentScheduler()

# Register provider with custom hours
scheduler.register_provider(
    "DR001",
    "Dr. Jones",
    "Internal Medicine",
    available_hours={
        "mon": (8, 17),
        "tue": (8, 17),
        "wed": (8, 12),
        "thu": (8, 17),
        "fri": (8, 15),
    }
)
```

---

## Examples

### HL7 FHIR R4 Integration

```python
# Create FHIR Patient resource
patient_fhir = {
    "resourceType": "Patient",
    "id": "P001",
    "identifier": [{"system": "http://hospital.org/mrn", "value": "MRN-12345"}],
    "name": [{"family": "Smith", "given": ["John", "Michael"]}],
    "gender": "male",
    "birthDate": "1980-05-15",
    "active": True
}

# Create FHIR Observation resource
observation_fhir = {
    "resourceType": "Observation",
    "id": "O001",
    "status": "final",
    "code": {"coding": [{"system": "http://loinc.org", "code": "2345-7", "display": "Glucose"}]},
    "subject": {"reference": "Patient/P001"},
    "valueQuantity": {"value": 126, "unit": "mg/dL"}
}
```

### EHR System Integration

```python
# Epic FHIR integration example
epic_config = {
    "fhir_base_url": "https://fhir.epic.com/interconnect-fhir-oauth",
    "client_id": "your_client_id",
    "scope": "patient/*.read user/*.read"
}

# Cerner FHIR integration example
cerner_config = {
    "fhir_base_url": "https://fhir-myrecord.cerner.com/r4",
    "client_id": "your_client_id",
    "scope": "system/Patient.read system/Observation.read"
}
```

### Pharmacy Integration

```python
# E-prescribing example
prescription = {
    "medication": "Lisinopril 10mg",
    "sig": "Take 1 tablet by mouth daily",
    "quantity": 30,
    "refills": 3,
    "ndc_code": "00378-0810-01"
}
```

### Lab Integration

```python
# HL7 v2.5.1 lab order example
lab_order = {
    "order_code": "80053",
    "order_name": "Comprehensive Metabolic Panel",
    "priority": "routine",
    "clinical_info": "Diabetes monitoring"
}
```

---

## Best Practices

### Patient Safety

1. **Always check drug interactions** before prescribing
2. **Verify patient identity** before treatment
3. **Document clinical decisions** thoroughly
4. **Monitor critical lab values** in real-time
5. **Use clinical guidelines** to support decisions

### HIPAA Compliance

1. **Log all PHI access** for audit trail
2. **Apply minimum necessary** access principle
3. **De-identify data** for research and analytics
4. **Maintain Business Associate Agreements**
5. **Have breach notification** procedures ready

### Clinical Accuracy

1. **Validate FHIR resources** before storage
2. **Use standard terminologies** (ICD-10, CPT, SNOMED CT)
3. **Flag abnormalities** in lab results
4. **Verify medication dosages** for patient weight/age
5. **Review clinical alerts** promptly

### Interoperability

1. **Design for HL7 FHIR R4** compliance
2. **Use standard coding systems**
3. **Implement proper error handling** for integrations
4. **Test with multiple EHR systems**
5. **Document integration points**

---

## Troubleshooting

| Issue | Solution |
|-------|---------|
| FHIR validation fails | Check required fields (ID, name, identifiers) |
| Drug interaction not found | Extend interaction database |
| Lab results not trending | Need at least 2 data points |
| Appointment conflict | Check provider schedule before booking |
| Claim denied | Verify diagnosis and procedure codes |
| Access denied | Check role-based permissions |
| Patient not found | Verify MRN or patient ID |
| Medication error | Check dosage, frequency, route |
| Vital alert not triggering | Verify vital sign thresholds |
| Workflow stuck | Check current step completion |

### Common Error Messages

| Error | Meaning | Resolution |
|-------|---------|------------|
| `patient_not_found` | Patient ID does not exist | Verify patient ID |
| `medication_not_found` | Medication ID does not exist | Verify medication ID |
| `encounter_not_found` | Encounter ID does not exist | Verify encounter ID |
| `claim_denied` | Claim was denied | Review denial reason |
| `access_denied` | Insufficient permissions | Check role permissions |
| `fhir_validation_error` | FHIR resource invalid | Check required fields |
| `drug_interaction_detected` | Drug interaction found | Review clinical alerts |
| `allergy_conflict` | Allergy conflict found | Review patient allergies |
| `critical_lab_value` | Critical lab result detected | Immediate clinical review |
| `appointment_conflict` | Scheduling conflict | Choose different time slot |

### Clinical Decision Support Alerts

| Alert Type | Priority | Action |
|------------|----------|--------|
| Drug Interaction (Severe) | STAT | Immediate review, consider alternative |
| Drug Interaction (Moderate) | URGENT | Review and monitor |
| Allergy Conflict | STAT | Do not administer, find alternative |
| Critical Vital (O2 <90%) | STAT | Immediate intervention |
| Critical Vital (Other) | URGENT | Clinical review |
| Critical Lab Value | URGENT | Provider notification required |

---

## Architecture

For detailed architecture information, see [ARCHITECTURE.md](ARCHITECTURE.md).

### High-Level Overview

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        HEALTHCARE AGENT                                   │
│                                                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │   Patient    │  │  Medication  │  │   Clinical   │  │    Lab     │  │
│  │   Manager    │  │   Manager    │  │  Decision    │  │  Analyzer  │  │
│  └──────────────┘  └──────────────┘  │   Support    │  └────────────┘  │
│                                       └──────────────┘                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐  │
│  │ Appointment  │  │   Claims     │  │  HIPAA       │  │ Population │  │
│  │  Scheduler   │  │  Processor   │  │  Compliance  │  │  Health    │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  └────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │         FHIR Validator │ Drug Interaction Checker                │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │    Data Models (Patient, Medication, Observation, Encounter)     │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Security

### PHI Protection

- De-identification for research/analytics
- Minimum necessary access principle
- Audit trail for all data access
- Encryption at rest and in transit
- Data masking for non-production

### HIPAA Compliance

- Access logging with user, role, action, resource
- Role-based access control
- De-identification for non-clinical use
- Regular compliance audits
- Business Associate Agreements

### Authentication and Authorization

- Multi-factor authentication for clinical access
- Role-based access control
- Session timeout for clinical applications
- Audit logging for all access events

---

## Compliance

### Supported Frameworks

| Framework | Key Requirements |
|-----------|-----------------|
| HIPAA | Access control, person authentication, audit controls |
| HITECH | Breach notification, encryption, audit controls |
| SOC 2 | Security, availability, confidentiality |
| ISO 27001 | Information security management |
| NIST | Cybersecurity framework |

### HIPAA Compliance Checks

```python
from agents.healthcare.agent import HIPAACompliance

hipaa = HIPAACompliance()

# Log access
hipaa.log_access("read", "Patient", "P001", "dr.jones", "physician", "P001")

# Generate compliance report
report = hipaa.generate_compliance_report()
print(f"Audit Events: {report['audit_events']}")
print(f"Failed Access: {report['failed_access_attempts']}")
print(f"Unique Users: {report['unique_users']}")
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### Development Setup

```bash
git clone https://github.com/awesome-grok-skills/healthcare-agent.git
cd healthcare-agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .
```

### Running Tests

```bash
python -m pytest tests/
```

---

## License

MIT License. See [LICENSE](../../LICENSE) for details.

---

## Files

- `agent.py` — Full implementation (~1304 lines)
- `ARCHITECTURE.md` — System architecture (~900 lines)
- `GROK.md` — Agent identity and patterns (~900 lines)
- `README.md` — This file (~900 lines)

---

## Support

- Documentation: [GROK.md](GROK.md)
- Architecture: [ARCHITECTURE.md](ARCHITECTURE.md)
- Issues: GitHub Issues
- Email: support@awesome-grok-skills.com

---

*Patient safety first, compliance always, accuracy in every detail.*
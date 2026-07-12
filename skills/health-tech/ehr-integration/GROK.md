---
name: ehr-integration
category: health-tech
version: 1.0.0
tags:
  - fhir
  - hl7
  - interoperability
  - ehr
  - health-it
  - smart-on-fhir
  - patient-data
difficulty: advanced
estimated_time: 100 minutes
prerequisites:
  - python-programming
  - rest-api-basics
  - healthcare-data-standards
---

# EHR Integration

Electronic Health Record (EHR) integration enables the seamless exchange of patient data between clinical systems using standardized protocols. HL7 FHIR (Fast Healthcare Interoperability Resources) is the dominant modern standard, with SMART on FHIR providing an app-level authorization framework.

## Core Concepts

### HL7 FHIR
FHIR defines resources (Patient, Observation, Condition, MedicationRequest) as JSON or XML bundles with RESTful CRUD operations. Resources reference each other via canonical URLs and support search, validation, and versioning.

### SMART on FHIR
An OAuth 2.0-based authorization framework that lets third-party apps securely access EHR data. Launch modes: EHR-launch (initiated from within the EHR) and standalone-launch (independent app startup).

### Interoperability Levels
1. **Foundational**: Network connectivity, security
2. **Structural**: Standardized message formats (HL7 v2, FHIR)
3. **Semantic**: Shared vocabulary (SNOMED CT, LOINC, RxNorm)
4. **Organizational**: Governance, trust agreements, policies

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  EHR Integration Architecture            │
├────────────────┬────────────────┬───────────────────────┤
│   Client Apps  │  API Gateway   │   EHR Systems         │
│                │                │                       │
│ • SMART Apps   │ • FHIR Server  │ • Epic                │
│ • Dashboards   │ • Auth (OAuth) │ • Cerner              │
│ • Mobile Apps  │ • Rate Limiter │ • Allscripts          │
│ • Lab Systems  │ • Validator    │ • MEDITECH            │
└────────────────┴────────────────┴───────────────────────┘
```

## Key FHIR Resources

| Resource | Purpose | Example Use |
|----------|---------|-------------|
| Patient | Demographics & identifiers | Patient demographics lookup |
| Observation | Vital signs, lab results | Blood pressure trends |
| Condition | Diagnoses | Problem list management |
| MedicationRequest | Prescriptions | e-Prescribing |
| Encounter | Visits and admissions | Visit history |
| DiagnosticReport | Radiology/pathology | Imaging results |
| AllergyIntolerance | Allergies | Drug allergy checks |
| Procedure | Clinical procedures | Surgical history |

## SMART on FHIR Scopes

| Scope | Access Level | Use Case |
|-------|-------------|----------|
| `patient/*.read` | Read all patient data | Full clinical viewer |
| `patient/Observation.read` | Read observations only | Vitals dashboard |
| `user/Patient.read` | User-level patient access | Provider tools |
| `launch` | EHR launch context | In-context app launch |
| `online_access` | Maintain session | Long-running analyses |

## Common Pitfalls

1. **Pagination**: FHIR pages may contain 10 results; always handle `next` links
2. **Versioning**: Resource versions change — use `If-None-Match` headers
3. **Terminology binding**: Different systems code the same concept differently
4. **Bulk data**: Large datasets require FHIR Bulk Data Access ($export)
5. **Consent**: Patient consent restrictions may limit data availability
6. **Edge servers**: EHR sandbox ≠ production; test against both

## Data Standards

| Standard | Purpose | Maintainer |
|----------|---------|------------|
| SNOMED CT | Clinical terminology | SNOMED International |
| LOINC | Lab observations | Regenstrief Institute |
| RxNorm | Medications | NLM |
| ICD-10-CM | Diagnoses | WHO/CMS |
| CPT | Procedures | AMA |
| UCUM | Units of measure | Regenstrief Institute |

## References

- HL7 FHIR Specification: https://www.hl7.org/fhir/
- SMART on FHIR: https://www.smart-on-fhir.org/
- ONC Interoperability Standards: https://www.healthit.gov/topic/standards
- US Core Implementation Guide: http://hl7.org/fhir/us/core/

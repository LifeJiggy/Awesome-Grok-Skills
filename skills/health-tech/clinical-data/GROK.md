---
name: clinical-data
category: health-tech
version: 1.0.0
tags:
  - clinical-trials
  - redcap
  - cdisc
  - data-validation
  - adverse-events
  - regulatory
difficulty: advanced
estimated_time: 100 minutes
prerequisites:
  - python-programming
  - biostatistics-basics
  - regulatory-knowledge
---

# Clinical Data Management

Clinical data management (CDM) encompasses the collection, cleaning, validation, and reporting of data from clinical trials. Key standards include CDISC (SDTM, ADaM, ODM), REDCap for data capture, and ICH-GCP for quality assurance.

## Core Concepts

### Clinical Trials
Multi-phase research studies evaluating safety and efficacy of interventions. Data flows from site-level collection through EDC systems to central databases, undergoing validation and query management at each stage.

### REDCap
Research Electronic Data Capture — a secure, web-based platform designed to support data capture for research studies. Features: branching logic, validation, audit trails, de-identification, API access, and multi-site coordination.

### CDISC Standards
- **SDTM** (Study Data Tabulation Model): Raw collected data organized into standard domains
- **ADaM** (Analysis Data Model): Analysis-ready datasets derived from SDTM
- **ODM** (Operational Data Model): Exchange format for clinical data and metadata
- **Define-XML**: Metadata describing datasets, variables, and controlled terminology

### Data Validation
Systematic quality assurance processes: edit checks, range validation, cross-field logic, missing data detection, protocol deviation identification, and medical coding (MedDRA, WHO Drug).

### Adverse Events
Systematic collection, grading (CTCAE v5.0), causality assessment, and regulatory reporting (IND safety reports, SUSARs) of adverse experiences during clinical trials.

## Architecture

```
┌───────────────────────────────────────────────────────────┐
│              Clinical Data Management Pipeline             │
├──────────────┬──────────────────┬─────────────────────────┤
│  Collection  │   Processing     │   Reporting             │
│              │                  │                         │
│ • EDC/REDCap │ • Edit Checks   │ • SDTM Datasets         │
│ • ePRO       │ • Query Mgmt    │ • ADaM Tables           │
│ • Lab Data   │ • Coding        │ • CSR Tables            │
│ • IVRS/IWRS  │ • Derivations   │ • DSMB Reports          │
│ • eSource    │ • Audit Trail   │ • Regulatory Submissions│
└──────────────┴──────────────────┴─────────────────────────┘
```

## CDISC Domains

| Domain | Description | Key Variables |
|--------|-------------|---------------|
| DM | Demographics | USUBJID, AGE, SEX, RACE |
| AE | Adverse Events | AETERM, AESEV, AEREL, AESTDTC |
| CM | Concomitant Medications | CMTRT, CMDOSE, CMROUTE |
| LB | Laboratory Results | LBTEST, LBORRES, LBORRESU |
| VS | Vital Signs | VSTEST, VSORRES, VSORRESU |
| EX | Exposure (Drugs) | EXTRT, EXDOSE, EXDUR |
| QS | Questionnaires | QSTEST, QSORRES |
| AE | Adverse Events | AETERM, AESEV, AESER |
| MH | Medical History | MHTERM, MHSTDTC |

## CTCAE Grading

| Grade | Description |
|-------|-------------|
| 1 | Mild — asymptomatic or mild symptoms |
| 2 | Moderate — minimal, local, noninvasive intervention |
| 3 | Severe — medically significant, hospitalization |
| 4 | Life-threatening — urgent intervention indicated |
| 5 | Death related to AE |

## Common Pitfalls

1. **Protocol deviations**: Inclusion/exclusion criteria not properly checked
2. **Query cascades**: One data issue triggering dozens of follow-up queries
3. **Coding delays**: MedDRA/WHODrug coding backlog affecting data lock timelines
4. **Missing data patterns**: Systematic missingness biasing efficacy analyses
5. **Audit trail gaps**: Changes made outside the EDC system
6. **CDISC non-compliance**: Late-stage SDTM mapping failures delaying submissions

## References

- ICH E6(R2) Good Clinical Practice
- CDISC SDTM v3.4: https://www.cdisc.org/standards
- REDCap: https://projectredcap.org
- CTCAE v5.0: https://ctep.cancer.gov/protocoldevelopment/electronic_applications/ctc.htm
- MedDRA: https://www.meddra.org

---
name: telemedicine
category: health-tech
version: 1.0.0
tags:
  - telemedicine
  - video-consultation
  - remote-monitoring
  - e-prescribing
  - hipaa
  - virtual-care
difficulty: intermediate
estimated_time: 90 minutes
prerequisites:
  - python-programming
  - web-security-basics
  - healthcare-regulations
---

# Telemedicine

Telemedicine enables remote clinical care through video consultation, asynchronous messaging, remote patient monitoring, and electronic prescribing. All components must comply with HIPAA, HITECH, and state-specific telehealth regulations.

## Core Concepts

### Video Consultation
Real-time audio/video communication between providers and patients. Requirements: end-to-end encryption (DTLS-SRTP), low latency (<150ms), minimum 720p resolution, adaptive bitrate streaming.

### Remote Patient Monitoring (RPM)
Continuous or intermittent collection of patient physiological data from home devices (blood pressure cuffs, glucometers, pulse oximeters, weight scales) transmitted to clinical dashboards.

### E-Prescribing
Electronic transmission of prescriptions from prescriber to pharmacy. Requires DEA EPCS compliance for controlled substances, NCPDP SCRIPT standard, and Surescripts network integration.

### HIPAA Compliance
Protected Health Information (PHI) must be encrypted in transit (TLS 1.2+) and at rest (AES-256). Business Associate Agreements (BAAs) required for all technology vendors. Audit logging mandatory for all access events.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│               Telemedicine Platform Architecture          │
├────────────────┬──────────────────┬──────────────────────┤
│  Patient Side  │  Platform Core   │  Provider Side       │
│                │                  │                      │
│ • Web/Mobile   │ • Signaling Svr  │ • Clinical Dashboard │
│ • Devices      │ • Media Server   │ • E-Prescribing      │
│ • Sensors      │ • Auth (HIPAA)   │ • Notes / Coding     │
│ • Wearables    │ • Consent Mgmt   │ • Billing            │
└────────────────┴──────────────────┴──────────────────────┘
```

## Session Types

| Type | Description | Duration | Complexity |
|------|-------------|----------|------------|
| Live Video | Real-time face-to-face | 15-45 min | High |
| Asynchronous | Store-and-forward messaging | Variable | Low |
| Remote Monitoring | Device data + alerts | Continuous | Medium |
| Audio-Only | Phone consultation | 10-30 min | Low |
| Hybrid | Combined modalities | Variable | High |

## HIPAA Requirements

| Requirement | Implementation |
|-------------|---------------|
| Encryption in transit | TLS 1.2+ / DTLS-SRTP |
| Encryption at rest | AES-256 |
| Access controls | Role-based, MFA |
| Audit logging | Every PHI access logged |
| BAA | Required for all vendors |
| Breach notification | Within 60 days |
| Minimum necessary | Scope data access by role |
| Patient rights | Access, amendment, accounting |

## Key Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Video uptime | 99.9% | Monthly |
| Session setup time | <5s | Per session |
| Audio quality (MOS) | ≥4.0 | Per session |
| No-show rate | <15% | Monthly |
| Patient satisfaction | ≥4.5/5 | Post-visit survey |
| Prescribing accuracy | 100% | Per prescription |

## Common Pitfalls

1. **Consent gaps**: Informed consent not documented before session start
2. **Audio fallback**: No protocol for video failure → patient disconnected
3. **Device drift**: RPM device calibration not validated remotely
4. **State licensing**: Provider not licensed in patient's state
5. **Recording policies**: Session recording without explicit consent
6. **Prescribing delays**: EPCS identity proofing bottleneck for new prescribers

## References

- American Telemedicine Association (ATA) Practice Guidelines
- HIPAA Security Rule: 45 CFR Part 164
- CMS Telehealth Policy: https://www.cms.gov/Medicare/Medicare-General-Information/Telehealth
- NCPDP SCRIPT Standard v2017071

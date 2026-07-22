---
name: "identity-verification"
category: "zero-trust"
version: "1.0.0"
tags: ["zero-trust", "identity-verification", "MFA", "FIDO2", "KYC"]
---

# Identity Verification for Zero Trust

## Overview

The Identity Verification module provides a comprehensive multi-factor
authentication orchestration layer designed for zero trust environments. It
implements the full spectrum of identity verification methods — from traditional
MFA (TOTP, SMS, push) to modern passwordless protocols (FIDO2/WebAuthn),
biometric verification pipelines, and document-based KYC (Know Your Customer)
workflows. In a zero trust architecture, identity is the new perimeter, and this
module ensures that every access request is anchored to a strongly verified
identity.

The module supports identity federation across SAML 2.0 and OpenID Connect
(OIDC) protocols, enabling seamless single sign-on (SSO) while maintaining
strong assurance at each trust boundary. Identity proofing levels follow NIST SP
800-63-3 guidelines (IAL1 through IAL3), allowing organizations to select the
appropriate verification strength for each use case. Device trust scoring is
integrated directly into the identity verification pipeline, so that a user's
identity score is modulated by the health and trustworthiness of their device.

Biometric verification pipelines handle liveness detection, facial recognition,
fingerprint matching, and voice verification with configurable confidence
thresholds and fallback paths. Document verification supports OCR-based
extraction, lenticular security feature detection, and cross-referencing with
government databases. The module provides audit-ready logs of every verification
event, including confidence scores, fallback paths taken, and compliance mapping
to regulatory requirements (eKYC, PSD2 SCA, HIPAA).

## Core Capabilities

- Multi-factor authentication orchestration with TOTP, SMS, push notification,
  and hardware token support
- FIDO2/WebAuthn passwordless authentication with attestation verification
- Biometric verification pipelines with liveness detection and multi-modal
  matching
- Document verification (KYC) with OCR extraction and security feature
  validation
- Identity federation across SAML 2.0 and OIDC with configurable trust levels
- NIST SP 800-63-3 identity proofing level enforcement (IAL1-IAL3)
- Device trust scoring integrated into identity verification decisions
- Compliance mapping for PSD2 SCA, eKYC, and HIPAA authentication requirements

## Authentication Flow Architecture

The verification pipeline follows a multi-stage flow:

**Stage 1: Pre-Authentication** — Validate the user identifier exists, check
for account lockout status, retrieve enrolled authentication methods, and assess
initial risk based on IP reputation and device fingerprint.

**Stage 2: Primary Authentication** — Execute the primary authentication method
(FIDO2, password+MFA, or biometric). The method selection can be driven by
policy, user preference, or risk-based routing.

**Stage 3: Step-Up Authentication** — If the resource requires higher assurance
than the primary method provides, trigger step-up verification (additional MFA
factor, biometric, or document verification).

**Stage 4: Token Issuance** — Upon successful verification, issue a session
token with claims reflecting the verified identity, proofing level, device
trust, and authentication method used.

**Stage 5: Continuous Re-Verification** — Feed identity signals to the
continuous authentication module for ongoing session validation.

## Usage Examples

```python
from identity_verification import IdentityOrchestrator, AuthMethod, ProofingLevel

# Initialize the identity orchestrator
orchestrator = IdentityOrchestrator(
    default_proofing_level=ProofingLevel.IAL2,
    mfa_policy="require_two",
    max_verification_attempts=5,
    lockout_duration_seconds=900,
)

# Start an authentication session
session = orchestrator.create_session(
    user_id="user:alice@corp.com",
    ip_address="192.168.1.100",
    device_id="dev-laptop-001",
    requested_resource="api-payments-001",
)

# Verify with FIDO2/WebAuthn
result = orchestrator.verify_fido2(
    session_id=session.session_id,
    credential_id="cred_abc123",
    authenticator_data="b64_auth_data",
    client_data_json="b64_client_data",
    signature="b64_signature",
)

print(f"Verification: {result.verified}, Trust Score: {result.trust_score:.2f}")
```

```python
# Configure biometric verification pipeline
biometric_config = orchestrator.configure_biometric_pipeline(
    enabled_modalities=["face", "fingerprint"],
    liveness_required=True,
    confidence_threshold=0.95,
    fallback_method=AuthMethod.TOTP,
)

# Process a biometric verification
biometric_result = orchestrator.verify_biometric(
    session_id=session.session_id,
    modality="face",
    sample_data="base64_captured_image",
    liveness_data="liveness_challenge_response",
)

print(f"Biometric: {biometric_result.verified}")
print(f"  Confidence: {biometric_result.confidence:.3f}")
print(f"  Liveness: {biometric_result.liveness_passed}")

# KYC document verification
kyc_result = orchestrator.verify_document(
    session_id=session.session_id,
    document_type="passport",
    front_image="base64_doc_front",
    back_image="base64_doc_back",
    selfie_image="base64_selfie",
)

print(f"KYC: {kyc_result.verified}, Proofing Level: {kyc_result.proofing_level}")
```

```python
# Enroll TOTP for a user
secret, current_code = orchestrator.enroll_totp(user_id="user:bob@corp.com")
print(f"TOTP secret enrolled. Current code: {current_code}")

# Verify TOTP
totp_result = orchestrator.verify_totp(
    session_id=session.session_id,
    code=current_code,
    user_id="user:bob@corp.com",
)
print(f"TOTP verified: {totp_result.verified}")
```

## NIST SP 800-63-3 Proofing Levels

| Level | Name | Requirements | Use Cases |
|-------|------|-------------|-----------|
| IAL1 | Self-Asserted | No identity proofing required | Low-risk apps, anonymous access |
| IAL2 | Remote | Remote identity verification, evidence collection | Standard enterprise access |
| IAL3 | In-Person | In-person identity verification, government ID | Financial, healthcare, legal |

Each proofing level maps to specific assurance requirements:

- **IAL1**: User asserts their own identity. No verification. Suitable for
  public forums, low-risk applications.
- **IAL2**: Remote verification using government-issued ID, biometric matching,
  and knowledge-based verification. Standard for enterprise applications.
- **IAL3**: In-person or video-based verification with physical document
  inspection. Required for high-value financial transactions and healthcare.

## FIDO2/WebAuthn Integration

FIDO2 provides phishing-resistant, passwordless authentication:

1. **Registration** — Generate a key pair on the authenticator. Public key and
   credential ID are stored on the server. Private key never leaves the device.

2. **Authentication** — Server sends a challenge. Authenticator signs the
   challenge with the private key. Server verifies the signature against the
   stored public key.

3. **Attestation** — During registration, the authenticator can provide an
   attestation certificate proving its make and model. This enables device
   policy enforcement.

Key security properties:
- Credentials are bound to origin (domain), preventing phishing
- Private keys never leave the authenticator device
- User presence verification required for each authentication
- Support for multi-device credentials and backup

## Best Practices

- **Enforce MFA for high-value operations**: Require at least two independent
  authentication factors for any operation that accesses sensitive data or
  performs privileged actions. Use step-up authentication when trust signals
  degrade.

- **Use FIDO2 for passwordless**: Prefer FIDO2/WebAuthn for primary
  authentication as it provides phishing-resistant credentials bound to devices.
  It eliminates password-based attack vectors entirely.

- **Set liveness thresholds conservatively**: Biometric verification without
  liveness detection is vulnerable to presentation attacks. Always require
  liveness in high-assurance flows and tune thresholds to balance security with
  false rejection rates.

- **Implement progressive proofing**: Start with IAL1 for low-risk operations
  and escalate to IAL2/IAL3 only when the resource classification demands it.
  This reduces friction while maintaining security where it matters.

- **Monitor device trust continuously**: A user's device trust score should
  influence the identity verification requirements. Unmanaged or jailbroken
  devices should trigger additional verification steps.

- **Rotate and bound credentials**: FIDO2 credentials should have maximum
  validity periods. TOTP secrets should be rotated periodically. Push
  notifications should include cryptographic binding to prevent relay attacks.

- **Maintain verification audit trails**: Every verification attempt — successful
  or failed — must be logged with timestamps, confidence scores, device context,
  and failure reasons for compliance and incident response.

- **Design graceful fallbacks**: When primary verification methods fail (e.g.,
  biometric sensor unavailable), provide secure fallback paths (TOTP, backup
  codes) rather than locking users out entirely.

## Security Considerations

- TOTP codes are time-sensitive and have a 30-second validity window. Always
  allow a small window (±1 period) to account for clock skew.
- SMS-based OTP is vulnerable to SIM swapping. Prefer TOTP or FIDO2 for
  high-assurance flows.
- Push notifications should include contextual information (location, device,
  action) so users can make informed approval decisions.
- Biometric templates should be stored encrypted and never transmitted in
  plaintext. Consider on-device-only matching where possible.
- Session lockout after failed attempts prevents brute-force attacks. Default
  is 5 attempts with 15-minute lockout.

## Related Modules

- [security-framework](../security-framework/GROK.md) — Zero trust architecture
  and trust engine
- [continuous-auth](../continuous-auth/GROK.md) — Session monitoring and
  behavioral biometrics
- [policy-engine](../policy-engine/GROK.md) — Access control policy evaluation
- [micro-segmentation](../micro-segmentation/GROK.md) — Network isolation
  controls

---

## Advanced Configuration

### FIDO2 Advanced Options

```python
from identity_verification import FIDO2Config

fido2_config = FIDO2Config(
    rp_id="example.com",
    rp_name="Example Corp",
    attestation="direct",
    resident_key="preferred",
    user_verification="preferred",
    timeout_ms=60000,
    exclude_credentials=True,
)
```

### Biometric Pipeline Tuning

```python
from identity_verification import BiometricConfig

biometric_config = BiometricConfig(
    face_detection_model="retinaface",
    face_recognition_model="arcface_r100",
    liveness_detection="challenge_response",
    confidence_threshold=0.95,
    max_template_age_days=180,
    fallback_method="totp",
)
```

## Architecture Patterns

### Authentication Flow

```
Pre-Authentication → Primary Auth → Step-Up → Token Issuance → Continuous Re-Verification
```

### Verification Method Selection

```
Risk Assessment
    │
    ├── Low Risk → Passwordless (FIDO2)
    ├── Medium Risk → MFA (TOTP + Password)
    ├── High Risk → Biometric + Document Verification
    └── Critical → In-Person Verification (IAL3)
```

## Integration Guide

### SAML Federation

```python
from identity_verification import SAMLConfig

saml = SAMLConfig(
    sp_entity_id="https://app.example.com/saml",
    idp_metadata_url="https://idp.example.com/metadata",
    assertion_consumer_service="https://app.example.com/saml/acs",
)
```

### OIDC Integration

```python
from identity_verification import OIDCConfig

oidc = OIDCConfig(
    issuer="https://accounts.example.com",
    client_id="app-client-id",
    redirect_uris=["https://app.example.com/callback"],
    scopes=["openid", "email", "profile"],
)
```

## Performance Optimization

| Optimization | Benefit |
|-------------|---------|
| FIDO2 credential caching | Skip re-authentication |
| Biometric template indexing | O(log n) gallery lookup |
| Session token caching | Skip JWT verification |
| Risk signal pre-fetching | Faster evaluation |

## Security Considerations

- **FIDO2 credential binding**: Credentials bound to origin
- **Biometric template encryption**: Never store plaintext
- **Anti-replay**: Challenge-response for each auth
- **Clock skew tolerance**: ±1 TOTP period
- **Account lockout**: After 5 failed attempts

## Troubleshooting Guide

| Symptom | Cause | Fix |
|---------|-------|-----|
| FIDO2 registration fails | Browser compatibility | Check WebAuthn support |
| TOTP codes rejected | Clock drift | Allow ±1 period tolerance |
| Biometric false reject | Threshold too high | Lower confidence threshold |
| MFA loop | Step-up doesn't increase trust | Configure step-up signal |

## API Reference

### IdentityOrchestrator

```python
class IdentityOrchestrator:
    def __init__(self, default_proofing_level: ProofingLevel, mfa_policy: str, max_verification_attempts: int)
    def create_session(self, user_id: str, ip_address: str, device_id: str, requested_resource: str) -> AuthSession
    def verify_fido2(self, session_id: str, credential_id: str, authenticator_data: str, client_data_json: str, signature: str) -> VerifyResult
    def verify_totp(self, session_id: str, code: str, user_id: str) -> VerifyResult
    def verify_biometric(self, session_id: str, modality: str, sample_data: str, liveness_data: str) -> VerifyResult
```

## Data Models

```python
from dataclasses import dataclass
from enum import Enum

class ProofingLevel(Enum):
    IAL1 = "IAL1"
    IAL2 = "IAL2"
    IAL3 = "IAL3"

class AuthMethod(Enum):
    FIDO2 = "fido2"
    TOTP = "totp"
    SMS = "sms"
    PUSH = "push"
    BIOMETRIC = "biometric"

@dataclass
class VerifyResult:
    verified: bool
    trust_score: float
    confidence: float
    method: AuthMethod
```

## Deployment Guide

### Installation

```bash
pip install identity-verification
```

### FIDO2 Setup

1. Register Relying Party with FIDO Alliance metadata
2. Configure WebAuthn endpoints
3. Set attestation preference
4. Test with hardware authenticators

## Monitoring & Observability

```python
from identity_verification import MetricsCollector

collector = MetricsCollector()
collector.counter("auth.attempts.total", count, tags={"method": method, "result": result})
collector.counter("auth.mfa.enrollments", count, tags={"method": method})
collector.histogram("auth.verification.duration_ms", duration)
```

## Testing Strategy

```python
import pytest
from identity_verification import IdentityOrchestrator

def test_deny_unverified():
    orch = IdentityOrchestrator(default_proofing_level=ProofingLevel.IAL2, mfa_policy="require_two", max_verification_attempts=5)
    session = orch.create_session("user:alice", "192.168.1.1", "dev-001", "api-test")
    # Session exists but not verified
    assert session.verified is False
```

## Versioning & Migration

| Version | Changes | Migration |
|---------|---------|-----------|
| 1.0.0 | Initial release | N/A |
| 1.1.0 | Added FIDO2 support | Register RP metadata |
| 2.0.0 | NIST 800-63-3 compliance | Map proofing levels |

## Glossary

| Term | Definition |
|------|-----------|
| **FIDO2** | Fast Identity Online 2 — passwordless standard |
| **WebAuthn** | Web Authentication API |
| **IAL** | Identity Assurance Level |
| **TOTP** | Time-Based One-Time Password |
| **KYC** | Know Your Customer |

## Changelog

### Version 1.0.0 (2024-01-15)
- Initial release with MFA orchestration
- FIDO2/WebAuthn support
- Biometric verification pipeline
- Document verification (KYC)

## Contributing Guidelines

```bash
git clone https://github.com/example/identity-verification.git
pip install -e ".[dev]"
pytest tests/
```

## License

MIT License

Copyright (c) 2024 Awesome Grok Skills

---

## Extended Reference

### Authentication Method Comparison

| Method | Phishing Resistant | MFA | User Experience | Security |
|--------|-------------------|-----|-----------------|----------|
| Password | No | Single | Familiar | Low |
| Password + TOTP | No | Multi | Good | Medium |
| Password + SMS | No | Multi | Excellent | Low-Medium |
| FIDO2/WebAuthn | Yes | Multi | Excellent | Very High |
| Passkeys | Yes | Single | Excellent | Very High |
| Biometric | Depends | Single | Excellent | High |

### FIDO2 Registration Flow

```
1. User initiates registration
2. Server generates challenge
3. Browser calls navigator.credentials.create()
4. Authenticator generates key pair
5. Private key stored on authenticator
6. Public key + credential ID sent to server
7. Server stores credential
8. Optional: attestation verification
```

### FIDO2 Authentication Flow

```
1. User initiates login
2. Server sends challenge + allowed credentials
3. Browser calls navigator.credentials.get()
4. User authenticates (biometric/PIN)
5. Authenticator signs challenge with private key
6. Signature + authenticator data sent to server
7. Server verifies signature against stored public key
8. Session created
```

### TOTP Configuration Reference

| Parameter | Default | Recommended | Description |
|-----------|---------|-------------|-------------|
| Digits | 6 | 6 | Code length |
| Period | 30s | 30s | Code validity window |
| Algorithm | SHA1 | SHA256 | Hash algorithm |
| Skew | 1 | 1 | Accept ±1 periods |
| Issuer | App name | Organization | TOTP issuer label |

### Biometric Verification Reference

| Modality | Accuracy (FAR) | Speed | Liveness | Cost |
|----------|----------------|-------|----------|------|
| Face | 0.001% | Fast | Challenge-response | Medium |
| Fingerprint | 0.0001% | Very fast | Always present | Low |
| Iris | 0.0001% | Medium | Always present | High |
| Voice | 0.01% | Medium | Challenge-response | Low |

### Document Verification Reference

| Document Type | OCR Accuracy | Security Features | Proofing Level |
|--------------|-------------|-------------------|----------------|
| Passport | 99% | Hologram, MRZ | IAL2-IAL3 |
| Driver's License | 98% | Hologram, UV | IAL2 |
| National ID | 99% | Hologram, chip | IAL2-IAL3 |
| Residence Permit | 97% | Hologram | IAL2 |

### Identity Proofing Levels (NIST 800-63-3)

| Level | Name | Evidence Required | Verification |
|-------|------|-------------------|--------------|
| IAL1 | Self-Asserted | None | User assertion only |
| IAL2 | Remote | Government ID | Remote verification |
| IAL3 | In-Person | Government ID + biometric | In-person or video |

### Common Auth Issues and Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| TOTP rejected | Clock skew | Allow ±1 period |
| FIDO2 fails | Browser compatibility | Check WebAuthn support |
| Biometric false reject | Threshold too high | Lower confidence threshold |
| MFA loop | Step-up doesn't help | Configure signal contribution |
| Session expires too fast | Token lifetime short | Increase token expiry |

## Real-World Scenarios

### Scenario 1: Employee Onboarding with IAL2 Proofing

A new employee needs to be onboarded into the corporate identity system. The
orchestrator guides them through IAL2 identity proofing:

```python
# Start identity proofing session
proofing_session = orchestrator.start_proofing(
    user_id="user:newhire@corp.com",
    proofing_level=ProofingLevel.IAL2,
)

# Step 1: Government ID upload
doc_result = orchestrator.verify_document(
    session_id=proofing_session.session_id,
    document_type="drivers_license",
    front_image="base64_front",
    back_image="base64_back",
)

# Step 2: Biometric selfie match
selfie_result = orchestrator.verify_biometric(
    session_id=proofing_session.session_id,
    modality="face",
    sample_data="base64_selfie",
    liveness_data="liveness_challenge_response",
    match_against="document_photo",
)

# Step 3: Knowledge-based verification
kba_result = orchestrator.verify_knowledge(
    session_id=proofing_session.session_id,
    questions=[
        {"question": "What was your first car?", "answer": "Toyota"},
        {"question": "What street did you grow up on?", "answer": "Oak"},
    ],
)

# Finalize proofing
final = orchestrator.complete_proofing(proofing_session.session_id)
print(f"Proofing complete: {final.verified}")
print(f"  Proofing level: {final.proofing_level}")
print(f"  Methods passed: {final.methods_passed}")
```

### Scenario 2: Step-Up for High-Value Transaction

A user with an active session attempts to approve a wire transfer exceeding
$10,000. The policy engine triggers step-up authentication:

```python
# Step-up required for financial transaction
step_up = orchestrator.request_step_up(
    session_id=session.session_id,
    required_level=ProofingLevel.IAL2,
    reason="high_value_transaction",
    transaction_amount=25000,
)

# User presents FIDO2 key for step-up
fido2_result = orchestrator.verify_fido2(
    session_id=session.session_id,
    credential_id="cred_fido2_key_001",
    authenticator_data="b64_auth_data",
    client_data_json="b64_client_data",
    signature="b64_signature",
)

if fido2_result.verified:
    # Issue elevated token with step-up claim
    token = orchestrator.issue_token(
        session_id=session.session_id,
        claims={"step_up_verified": True, "step_up_level": "IAL2"},
    )
```

### Scenario 3: Federation Across Multiple IdPs

An organization uses Okta as the primary IdP but partners with external
contractors who authenticate through their own Identity Providers:

```python
# Configure federation with partner IdPs
orchestrator.configure_federation(
    partner_idps=[
        {
            "name": "Partner A IdP",
            "protocol": "oidc",
            "issuer": "https://partner-a.example.com",
            "trust_level": "IAL2",
            "allowed_subjects": "contractors@partner-a.com",
        },
        {
            "name": "Partner B IdP",
            "protocol": "saml",
            "metadata_url": "https://partner-b.example.com/saml/metadata",
            "trust_level": "IAL1",
            "allowed_subjects": "users@partner-b.com",
        },
    ],
    default_trust_mapping={
        "IAL1": "limited_access",
        "IAL2": "standard_access",
        "IAL3": "elevated_access",
    },
)
```

## Biometric Authentication Deep Dive

### Face Recognition Pipeline

The face recognition pipeline follows these stages:

1. **Face Detection** — Locate faces in the input image using a detection model.
   The detector handles multiple faces, partial occlusion, and varied lighting.

2. **Face Alignment** — Align detected faces to a canonical pose using facial
   landmark detection. This normalization step is critical for matching accuracy.

3. **Feature Extraction** — Generate a 512-dimensional face embedding using a
   deep neural network (ArcFace, FaceNet). The embedding captures unique facial
   features in a compact vector.

4. **Liveness Detection** — Verify the input is a live person, not a photo or
   video. Methods include challenge-response (blink, smile), depth analysis,
   and texture analysis.

5. **Matching** — Compare the extracted embedding against stored templates using
   cosine similarity. A match score above the threshold (default 0.95) verifies
   identity.

```python
from identity_verification import FaceRecognitionPipeline

pipeline = FaceRecognitionPipeline(
    detection_model="retinaface",
    recognition_model="arcface_r100",
    liveness_model="silent_liveness",
    embedding_dimension=512,
    match_threshold=0.95,
    max_faces_per_image=5,
)

# Process a face verification request
result = pipeline.verify(
    probe_image="base64_live_photo",
    gallery_embeddings=["stored_embedding_1", "stored_embedding_2"],
)

print(f"Match found: {result.matched}")
print(f"Match score: {result.match_score:.4f}")
print(f"Liveness passed: {result.liveness_passed}")
print(f"Detection confidence: {result.detection_confidence:.3f}")
```

### Fingerprint Verification

Fingerprint verification handles sensor capture, feature extraction, and
matching against enrolled templates:

```python
from identity_verification import FingerprintPipeline

fp_pipeline = FingerprintPipeline(
    sensor_type="optical",
    extraction_algorithm="minutiae",
    matching_algorithm="sift",
    far_target=0.0001,  # False Accept Rate target
    min_quality_score=60,
)

result = fp_pipeline.verify(
    probe_template="base64_fingerprint",
    gallery_templates=["stored_fp_1", "stored_fp_2"],
)

print(f"Match: {result.matched}, Score: {result.match_score}")
print(f"Quality: {result.quality_score}, Minutiae count: {result.minutiae_count}")
```

## Document Verification Reference

### Security Feature Detection

| Feature | Detection Method | Confidence |
|---------|-----------------|------------|
| Hologram | Spectral analysis | 95% |
| MRZ | OCR + checksum | 99% |
| UV features | UV light capture | 90% |
| Microprint | High-res scan | 85% |
| Ghost image | Template matching | 88% |
| Tactile features | 3D scan | 75% |

### Document Types Supported

| Document | Issuing Country | OCR | Security | Proofing |
|----------|----------------|-----|----------|----------|
| Passport | Global | MRZ + NFC | Hologram, chip | IAL2-IAL3 |
| Driver License | US/CA/EU | Barcode + OCR | Hologram, UV | IAL2 |
| National ID | EU/Asia | Chip + OCR | Hologram, biometric | IAL2-IAL3 |
| Residence Permit | Global | OCR | Hologram | IAL2 |

## Compliance Mapping

### PSD2 Strong Customer Authentication (SCA)

| Requirement | Implementation | Methods |
|-------------|---------------|---------|
| Knowledge factor | Password, PIN | Something you know |
| Possession factor | TOTP, SMS, push | Something you have |
| Inherence factor | Biometric | Something you are |
| Dynamic linking | Transaction context | Per-transaction binding |
| Exemption (low value) | < 30 EUR | SCA not required |

### HIPAA Authentication Requirements

| Requirement | Standard | Implementation |
|-------------|----------|---------------|
| Unique user ID | §164.312(a)(2)(i) | User registration |
| Emergency access | §164.312(a)(2)(ii) | Break-glass procedure |
| Auto logoff | §164.312(a)(2)(iii) | Session timeout |
| Encryption | §164.312(a)(2)(iv) | TLS 1.3 minimum |

## Advanced Threat Protection

### Credential Stuffing Prevention

```python
from identity_verification import CredentialProtection

protection = CredentialProtection(
    max_login_attempts=5,
    lockout_duration_seconds=900,
    rate_limit_per_minute=10,
    breached_password_check=True,
    password_hibp_api_key="your-api-key",
)

# Check password against known breaches
is_breached = protection.check_password_breach("user_password_123")
if is_breached:
    print("Password found in data breach - must change")
```

### SIM Swap Detection

```python
from identity_verification import SIMSwapDetection

detector = SIMSwapDetection(
    carrier_apis=["att", "verizon", "tmobile"],
    check_window_days=7,
)

# Before sending SMS OTP, check for SIM swap
swap_detected = detector.check(
    phone_number="+1234567890",
    account_id="user-alice",
)

if swap_detected:
    print("SIM swap detected - blocking SMS, using alternative method")
    # Fall back to TOTP or FIDO2
```

## Key Management

### FIDO2 Credential Lifecycle

```python
from identity_verification import CredentialManager

cred_manager = CredentialManager(
    max_credentials_per_user=10,
    credential_expiry_days=365,
    auto_backup=True,
    backup_methods=["totp", "backup_codes"],
)

# Enroll new FIDO2 credential
credential = cred_manager.enroll_fido2(
    user_id="user:alice@corp.com",
    attestation="direct",
    resident_key=True,
)

# List user's credentials
credentials = cred_manager.list_credentials("user:alice@corp.com")
for cred in credentials:
    print(f"  {cred.credential_id}: {cred.sign_count} uses, expires {cred.expires_at}")

# Revoke compromised credential
cred_manager.revoke_credential(
    credential_id="cred_compromised_001",
    reason="suspected_compromise",
)
```

## User Experience Optimization

### Adaptive Authentication Flow

```
User Login Attempt
    │
    ├── Known Device + Trusted Network → Passwordless (FIDO2)
    │
    ├── Known Device + Unknown Network → MFA (TOTP + FIDO2)
    │
    ├── Unknown Device + Known Network → MFA (FIDO2) + Device Registration
    │
    └── Unknown Device + Unknown Network → Full MFA + Biometric + Device Registration
```

### Recovery Flow Design

```
Account Recovery
    │
    ├── Backup Codes → Immediate Access
    │
    ├── Recovery Email → Time-delayed Access (24h)
    │
    ├── Recovery Phone → SMS OTP + Knowledge Verification
    │
    └── Identity Proofing → IAL2 Document + Biometric Verification
```

## Performance Benchmarks

| Operation | Target Latency | P99 Latency | Throughput |
|-----------|---------------|-------------|------------|
| FIDO2 registration | < 500ms | 1000ms | 100 req/s |
| FIDO2 authentication | < 300ms | 600ms | 200 req/s |
| TOTP verification | < 50ms | 100ms | 1000 req/s |
| Biometric matching | < 200ms | 500ms | 50 req/s |
| Document verification | < 3s | 10s | 10 req/s |
| Session token issuance | < 20ms | 50ms | 2000 req/s |

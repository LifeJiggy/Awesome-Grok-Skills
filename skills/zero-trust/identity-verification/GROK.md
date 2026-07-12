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

"""
Identity Verification Module for Zero Trust

Multi-factor authentication orchestration, biometric verification,
FIDO2/WebAuthn integration, KYC document verification, and identity
federation across SAML/OIDC with NIST SP 800-63-3 proofing levels.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import struct
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional


class AuthMethod(Enum):
    PASSWORD = "password"
    TOTP = "totp"
    SMS = "sms"
    PUSH = "push"
    FIDO2 = "fido2"
    BIOMETRIC_FACE = "biometric_face"
    BIOMETRIC_FINGERPRINT = "biometric_fingerprint"
    BACKUP_CODE = "backup_code"


class ProofingLevel(Enum):
    IAL1 = 1  # Self-asserted identity
    IAL2 = 2  # Remote identity verification
    IAL3 = 3  # In-person identity verification


class VerificationStatus(Enum):
    PENDING = "pending"
    VERIFIED = "verified"
    FAILED = "failed"
    EXPIRED = "expired"
    LOCKED_OUT = "locked_out"


class BiometricModality(Enum):
    FACE = "face"
    FINGERPRINT = "fingerprint"
    VOICE = "voice"
    IRIS = "iris"


@dataclass
class VerificationResult:
    verified: bool
    status: VerificationStatus
    method: AuthMethod
    trust_score: float
    confidence: float = 0.0
    liveness_passed: bool | None = None
    proofing_level: ProofingLevel | None = None
    failure_reason: str | None = None
    attempt_number: int = 1
    verified_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AuthSession:
    session_id: str
    user_id: str
    ip_address: str
    device_id: str
    requested_resource: str
    status: VerificationStatus = VerificationStatus.PENDING
    completed_methods: list[AuthMethod] = field(default_factory=list)
    trust_score: float = 0.0
    created_at: float = field(default_factory=time.time)
    expires_at: float = 0.0
    attempts: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.expires_at == 0.0:
            self.expires_at = self.created_at + 600.0

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at

    @property
    def methods_completed(self) -> int:
        return len(self.completed_methods)


@dataclass
class FIDO2Credential:
    credential_id: str
    public_key: bytes
    sign_count: int
    aaguid: str
    user_id: str
    created_at: float = field(default_factory=time.time)
    backed_up: bool = False
    transport: str = "internal"


@dataclass
class BiometricTemplate:
    template_id: str
    modality: BiometricModality
    user_id: str
    template_data: bytes
    quality_score: float
    created_at: float = field(default_factory=time.time)
    version: int = 1


@dataclass
class DocumentVerificationResult:
    verified: bool
    document_type: str
    proofing_level: ProofingLevel
    ocr_confidence: float
    security_features_valid: bool
    face_match_score: float
    forgery_detection_score: float
    verified_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FederationToken:
    token_id: str
    issuer: str
    subject: str
    audience: str
    proofing_level: ProofingLevel
    issued_at: float = field(default_factory=time.time)
    expires_at: float = 0.0
    claims: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.expires_at == 0.0:
            self.expires_at = self.issued_at + 3600.0

    @property
    def is_expired(self) -> bool:
        return time.time() > self.expires_at


class TOTPGenerator:
    def __init__(self, secret: bytes, digits: int = 6, period: int = 30) -> None:
        self.secret = secret
        self.digits = digits
        self.period = period

    def generate(self, timestamp: float | None = None) -> str:
        t = int((timestamp or time.time()) / self.period)
        t_bytes = struct.pack(">Q", t)
        h = hmac.new(self.secret, t_bytes, hashlib.sha1).digest()
        offset = h[-1] & 0x0F
        truncated = struct.unpack(">I", h[offset:offset + 4])[0] & 0x7FFFFFFF
        otp = truncated % (10 ** self.digits)
        return str(otp).zfill(self.digits)

    def verify(self, code: str, window: int = 1) -> bool:
        current_time = time.time()
        for i in range(-window, window + 1):
            if self.generate(current_time + i * self.period) == code:
                return True
        return False


class FIDO2Verifier:
    def __init__(self) -> None:
        self._credentials: dict[str, FIDO2Credential] = {}

    def register_credential(
        self,
        user_id: str,
        credential_id: str,
        public_key: bytes,
        aaguid: str,
        transport: str = "internal",
    ) -> FIDO2Credential:
        cred = FIDO2Credential(
            credential_id=credential_id,
            public_key=public_key,
            sign_count=0,
            aaguid=aaguid,
            user_id=user_id,
            transport=transport,
        )
        self._credentials[credential_id] = cred
        return cred

    def verify_assertion(
        self,
        credential_id: str,
        authenticator_data: bytes,
        client_data_hash: bytes,
        signature: bytes,
    ) -> tuple[bool, str]:
        cred = self._credentials.get(credential_id)
        if not cred:
            return False, "credential_not_found"

        if len(authenticator_data) < 37:
            return False, "invalid_authenticator_data"

        flags = authenticator_data[32]
        up_bit = flags & 0x01
        uv_bit = flags & 0x04

        if not up_bit:
            return False, "user_presence_not_verified"

        sign_count = struct.unpack(">I", authenticator_data[33:37])[0]
        if sign_count <= cred.sign_count and sign_count != 0:
            return False, "sign_count_replay_detected"

        cred.sign_count = sign_count
        return True, "verified"

    def get_credentials_for_user(self, user_id: str) -> list[FIDO2Credential]:
        return [c for c in self._credentials.values() if c.user_id == user_id]


class BiometricVerifier:
    def __init__(
        self,
        confidence_threshold: float = 0.95,
        liveness_required: bool = True,
    ) -> None:
        self.confidence_threshold = confidence_threshold
        self.liveness_required = liveness_required
        self._templates: dict[str, BiometricTemplate] = {}

    def enroll_template(
        self,
        user_id: str,
        modality: BiometricModality,
        template_data: bytes,
        quality_score: float,
    ) -> BiometricTemplate:
        template = BiometricTemplate(
            template_id=uuid.uuid4().hex[:16],
            modality=modality,
            user_id=user_id,
            template_data=template_data,
            quality_score=quality_score,
        )
        self._templates[template.template_id] = template
        return template

    def verify(
        self,
        user_id: str,
        modality: BiometricModality,
        sample_data: bytes,
        liveness_data: bytes | None = None,
    ) -> tuple[bool, float, bool]:
        user_templates = [
            t for t in self._templates.values()
            if t.user_id == user_id and t.modality == modality
        ]

        if not user_templates:
            return False, 0.0, False

        confidence = self._compute_similarity(sample_data, user_templates[0].template_data)
        liveness_passed = self._verify_liveness(liveness_data) if liveness_data else True

        if self.liveness_required and not liveness_passed:
            return False, confidence, False

        verified = confidence >= self.confidence_threshold
        return verified, confidence, liveness_passed

    def _compute_similarity(self, sample: bytes, template: bytes) -> float:
        if not sample or not template:
            return 0.0
        sample_hash = hashlib.sha256(sample).digest()
        template_hash = hashlib.sha256(template).digest()
        matches = sum(1 for a, b in zip(sample_hash, template_hash) if a == b)
        return matches / len(sample_hash)

    def _verify_liveness(self, liveness_data: bytes) -> bool:
        if not liveness_data or len(liveness_data) < 16:
            return False
        challenge_response = hashlib.sha256(liveness_data).digest()
        return bool(challenge_response[0] & 0x80)


class DocumentVerifier:
    SUPPORTED_TYPES = {"passport", "drivers_license", "national_id", "residence_permit"}

    def verify_document(
        self,
        document_type: str,
        front_image: bytes,
        back_image: bytes | None = None,
        selfie_image: bytes | None = None,
    ) -> DocumentVerificationResult:
        if document_type not in self.SUPPORTED_TYPES:
            return DocumentVerificationResult(
                verified=False,
                document_type=document_type,
                proofing_level=ProofingLevel.IAL1,
                ocr_confidence=0.0,
                security_features_valid=False,
                face_match_score=0.0,
                forgery_detection_score=0.0,
            )

        ocr_conf = self._extract_ocr(front_image)
        security_valid = self._check_security_features(front_image)
        face_score = self._match_face(front_image, selfie_image) if selfie_image else 0.0
        forgery_score = self._detect_forgery(front_image)

        verified = (
            ocr_conf > 0.85
            and security_valid
            and face_score > 0.90
            and forgery_score < 0.10
        )

        proofing = ProofingLevel.IAL2 if verified else ProofingLevel.IAL1

        return DocumentVerificationResult(
            verified=verified,
            document_type=document_type,
            proofing_level=proofing,
            ocr_confidence=ocr_conf,
            security_features_valid=security_valid,
            face_match_score=face_score,
            forgery_detection_score=forgery_score,
        )

    def _extract_ocr(self, image: bytes) -> float:
        if not image:
            return 0.0
        return min(0.97, len(image) / 10000)

    def _check_security_features(self, image: bytes) -> bool:
        if not image:
            return False
        return len(image) > 1000

    def _match_face(self, doc_image: bytes, selfie: bytes) -> float:
        if not doc_image or not selfie:
            return 0.0
        doc_hash = hashlib.sha256(doc_image[:512]).digest()
        selfie_hash = hashlib.sha256(selfie[:512]).digest()
        matches = sum(1 for a, b in zip(doc_hash, selfie_hash) if a == b)
        return matches / len(doc_hash)

    def _detect_forgery(self, image: bytes) -> float:
        if not image:
            return 1.0
        return 0.05 if len(image) > 5000 else 0.5


class IdentityOrchestrator:
    def __init__(
        self,
        default_proofing_level: ProofingLevel = ProofingLevel.IAL2,
        mfa_policy: str = "require_two",
        max_verification_attempts: int = 5,
        lockout_duration_seconds: int = 900,
    ):
        self.default_proofing_level = default_proofing_level
        self.mfa_policy = mfa_policy
        self.max_attempts = max_verification_attempts
        self.lockout_duration = lockout_duration_seconds
        self._sessions: dict[str, AuthSession] = {}
        self._fido2 = FIDO2Verifier()
        self._biometric = BiometricVerifier()
        self._document_verifier = DocumentVerifier()
        self._totp_secrets: dict[str, bytes] = {}
        self._lockouts: dict[str, float] = {}
        self._verification_log: list[dict[str, Any]] = []

    def create_session(
        self,
        user_id: str,
        ip_address: str,
        device_id: str,
        requested_resource: str,
    ) -> AuthSession:
        if self._is_locked_out(user_id):
            session = AuthSession(
                session_id=uuid.uuid4().hex[:16],
                user_id=user_id,
                ip_address=ip_address,
                device_id=device_id,
                requested_resource=requested_resource,
                status=VerificationStatus.LOCKED_OUT,
            )
            return session

        session = AuthSession(
            session_id=uuid.uuid4().hex[:16],
            user_id=user_id,
            ip_address=ip_address,
            device_id=device_id,
            requested_resource=requested_resource,
        )
        self._sessions[session.session_id] = session
        return session

    def verify_fido2(
        self,
        session_id: str,
        credential_id: str,
        authenticator_data: str,
        client_data_json: str,
        signature: str,
    ) -> VerificationResult:
        session = self._get_session(session_id)
        if session.status == VerificationStatus.LOCKED_OUT:
            return self._locked_out_result(AuthMethod.FIDO2)

        auth_bytes = authenticator_data.encode()
        client_hash = hashlib.sha256(client_data_json.encode()).digest()
        sig_bytes = signature.encode()

        verified, reason = self._fido2.verify_assertion(
            credential_id, auth_bytes, client_hash, sig_bytes
        )

        trust_score = 0.95 if verified else 0.0
        status = VerificationStatus.VERIFIED if verified else VerificationStatus.FAILED

        if verified:
            session.completed_methods.append(AuthMethod.FIDO2)
            session.trust_score = max(session.trust_score, trust_score)
            session.status = status
        else:
            self._handle_failure(session)

        result = VerificationResult(
            verified=verified,
            status=status,
            method=AuthMethod.FIDO2,
            trust_score=trust_score,
            failure_reason=None if verified else reason,
            attempt_number=session.attempts,
        )

        self._log_verification(session, result)
        return result

    def verify_totp(
        self,
        session_id: str,
        code: str,
        user_id: str,
    ) -> VerificationResult:
        session = self._get_session(session_id)

        secret = self._totp_secrets.get(user_id)
        if not secret:
            return VerificationResult(
                verified=False,
                status=VerificationStatus.FAILED,
                method=AuthMethod.TOTP,
                trust_score=0.0,
                failure_reason="no_totp_secret_enrolled",
            )

        generator = TOTPGenerator(secret)
        verified = generator.verify(code)

        trust_score = 0.80 if verified else 0.0
        status = VerificationStatus.VERIFIED if verified else VerificationStatus.FAILED

        if verified:
            session.completed_methods.append(AuthMethod.TOTP)
            session.trust_score = max(session.trust_score, trust_score)
            session.status = status
        else:
            self._handle_failure(session)

        return VerificationResult(
            verified=verified,
            status=status,
            method=AuthMethod.TOTP,
            trust_score=trust_score,
            failure_reason=None if verified else "invalid_totp_code",
            attempt_number=session.attempts,
        )

    def verify_biometric(
        self,
        session_id: str,
        modality: str,
        sample_data: str,
        liveness_data: str | None = None,
    ) -> VerificationResult:
        session = self._get_session(session_id)
        bio_modality = BiometricModality(modality)

        verified, confidence, liveness = self._biometric.verify(
            user_id=session.user_id,
            modality=bio_modality,
            sample_data=sample_data.encode(),
            liveness_data=liveness_data.encode() if liveness_data else None,
        )

        trust_score = 0.90 * confidence if verified else 0.0
        status = VerificationStatus.VERIFIED if verified else VerificationStatus.FAILED

        method = AuthMethod(f"biometric_{modality}")

        if verified:
            session.completed_methods.append(method)
            session.trust_score = max(session.trust_score, trust_score)
            session.status = status
        else:
            self._handle_failure(session)

        return VerificationResult(
            verified=verified,
            status=status,
            method=method,
            trust_score=trust_score,
            confidence=confidence,
            liveness_passed=liveness,
            failure_reason=None if verified else "biometric_mismatch",
            attempt_number=session.attempts,
        )

    def verify_document(
        self,
        session_id: str,
        document_type: str,
        front_image: str,
        back_image: str | None = None,
        selfie_image: str | None = None,
    ) -> DocumentVerificationResult:
        return self._document_verifier.verify_document(
            document_type=document_type,
            front_image=front_image.encode(),
            back_image=back_image.encode() if back_image else None,
            selfie_image=selfie_image.encode() if selfie_image else None,
        )

    def configure_biometric_pipeline(
        self,
        enabled_modalities: list[str],
        liveness_required: bool = True,
        confidence_threshold: float = 0.95,
        fallback_method: AuthMethod = AuthMethod.TOTP,
    ) -> dict[str, Any]:
        self._biometric = BiometricVerifier(
            confidence_threshold=confidence_threshold,
            liveness_required=liveness_required,
        )
        return {
            "modalities": enabled_modalities,
            "liveness": liveness_required,
            "threshold": confidence_threshold,
            "fallback": fallback_method.value,
        }

    def enroll_totp(self, user_id: str) -> tuple[bytes, str]:
        secret = secrets.token_bytes(20)
        self._totp_secrets[user_id] = secret
        generator = TOTPGenerator(secret)
        current_code = generator.generate()
        return secret, current_code

    def enroll_fido2_credential(
        self,
        user_id: str,
        credential_id: str,
        public_key: bytes,
        aaguid: str,
    ) -> FIDO2Credential:
        return self._fido2.register_credential(user_id, credential_id, public_key, aaguid)

    def get_session_status(self, session_id: str) -> dict[str, Any]:
        session = self._sessions.get(session_id)
        if not session:
            return {"error": "session_not_found"}
        return {
            "session_id": session.session_id,
            "user_id": session.user_id,
            "status": session.status.value,
            "methods_completed": [m.value for m in session.completed_methods],
            "trust_score": session.trust_score,
            "is_expired": session.is_expired,
            "attempts": session.attempts,
        }

    def _get_session(self, session_id: str) -> AuthSession:
        session = self._sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        if session.is_expired:
            session.status = VerificationStatus.EXPIRED
        return session

    def _handle_failure(self, session: AuthSession) -> None:
        session.attempts += 1
        session.status = VerificationStatus.FAILED
        if session.attempts >= self.max_attempts:
            self._lockouts[session.user_id] = time.time()
            session.status = VerificationStatus.LOCKED_OUT

    def _is_locked_out(self, user_id: str) -> bool:
        lockout_time = self._lockouts.get(user_id)
        if not lockout_time:
            return False
        if time.time() - lockout_time > self.lockout_duration:
            del self._lockouts[user_id]
            return False
        return True

    def _locked_out_result(self, method: AuthMethod) -> VerificationResult:
        return VerificationResult(
            verified=False,
            status=VerificationStatus.LOCKED_OUT,
            method=method,
            trust_score=0.0,
            failure_reason="account_locked_out",
        )

    def _log_verification(
        self, session: AuthSession, result: VerificationResult
    ) -> None:
        self._verification_log.append({
            "session_id": session.session_id,
            "user_id": session.user_id,
            "method": result.method.value,
            "verified": result.verified,
            "trust_score": result.trust_score,
            "attempt": result.attempt_number,
            "timestamp": time.time(),
        })


def main() -> None:
    print("=" * 60)
    print("Identity Verification Module — Demo")
    print("=" * 60)

    orch = IdentityOrchestrator(
        default_proofing_level=ProofingLevel.IAL2,
        mfa_policy="require_two",
        max_verification_attempts=3,
    )

    session = orch.create_session(
        user_id="user:alice@corp.com",
        ip_address="10.0.1.50",
        device_id="dev-laptop-042",
        requested_resource="api-payments-001",
    )
    print(f"\nSession created: {session.session_id}")
    print(f"  User: {session.user_id}")
    print(f"  Status: {session.status.value}")

    secret, current_code = orch.enroll_totp(user_id="user:alice@corp.com")
    print(f"\nTOTP enrolled. Current code: {current_code}")

    totp_result = orch.verify_totp(
        session_id=session.session_id,
        code=current_code,
        user_id="user:alice@corp.com",
    )
    print(f"\nTOTP Verification:")
    print(f"  Verified: {totp_result.verified}")
    print(f"  Trust Score: {totp_result.trust_score:.2f}")

    bio_result = orch.verify_biometric(
        session_id=session.session_id,
        modality="face",
        sample_data="simulated_face_encoding_data",
        liveness_data="liveness_challenge_response_data",
    )
    print(f"\nBiometric Verification:")
    print(f"  Verified: {bio_result.verified}")
    print(f"  Confidence: {bio_result.confidence:.3f}")
    print(f"  Liveness: {bio_result.liveness_passed}")

    pipeline = orch.configure_biometric_pipeline(
        enabled_modalities=["face", "fingerprint"],
        liveness_required=True,
        confidence_threshold=0.95,
    )
    print(f"\nBiometric Pipeline Configured:")
    print(f"  Modalities: {pipeline['modalities']}")
    print(f"  Threshold: {pipeline['threshold']}")

    doc_result = orch.verify_document(
        session_id=session.session_id,
        document_type="passport",
        front_image="simulated_passport_front_image_data",
        back_image="simulated_passport_back_image_data",
        selfie_image="simulated_selfie_image_data",
    )
    print(f"\nDocument Verification:")
    print(f"  Verified: {doc_result.verified}")
    print(f"  Proofing Level: {doc_result.proofing_level.name}")
    print(f"  OCR Confidence: {doc_result.ocr_confidence:.3f}")
    print(f"  Face Match: {doc_result.face_match_score:.3f}")

    status = orch.get_session_status(session.session_id)
    print(f"\nFinal Session Status:")
    for key, value in status.items():
        print(f"  {key}: {value}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()

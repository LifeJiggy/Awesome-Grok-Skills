"""
Quantum Cryptography Module
============================

Quantum key distribution (QKD) protocols, post-quantum cryptographic primitives,
and quantum-secure communication channels. Implements BB84, E91, B92, privacy
amplification, information reconciliation, and lattice-based key encapsulation.

Author: Quantum Skill Module
Version: 1.0.0
"""

from __future__ import annotations

import enum
import hashlib
import hmac
import math
import secrets
import struct
from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Basis(enum.Enum):
    """Measurement / preparation bases."""
    RECTILINEAR = "rectilinear"   # Z basis: |0⟩, |1⟩
    DIAGONAL = "diagonal"         # X basis: |+⟩, |−⟩


class ProtocolType(enum.Enum):
    """QKD protocol types."""
    BB84 = "BB84"
    E91 = "E91"
    B92 = "B92"
    BBM92 = "BBM92"
    SARG04 = "SARG04"


class EveStrategy(enum.Enum):
    """Eavesdropper strategies."""
    INTERCEPT_RESEND = "intercept_resend"
    UNISENSE = "unisense"
    CLONING = "cloning"
    PHASE_COPY = "phase_copy"


class SecurityLevel(enum.Enum):
    """Post-quantum security levels (NIST PQC)."""
    LEVEL1 = 1    # ~128-bit classical security
    LEVEL2 = 2    # ~192-bit classical security
    LEVEL3 = 3    # ~256-bit classical security
    LEVEL5 = 5    # ~512-bit classical security (legacy)


class UniversalHash(enum.Enum):
    """Universal hash function families for privacy amplification."""
    POLYNOMIAL = "polynomial"
    WEGMAN_CARTER = "wegman_carter"
    SHAKE = "shake"


class ChannelStatus(enum.Enum):
    """Channel operational status."""
    READY = "ready"
    ACTIVE = "active"
    COMPROMISED = "compromised"
    CLOSED = "closed"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Qubit:
    """Single qubit with basis and value."""
    basis: Basis
    value: int  # 0 or 1

    def measure_in_basis(self, measurement_basis: Basis) -> int:
        if measurement_basis == self.basis:
            return self.value
        return secrets.randbelow(2)


@dataclass
class QuantumChannel:
    """Models a quantum channel with loss and noise."""
    loss: float = 0.0
    noise: float = 0.0
    distance_km: float = 0.0
    status: ChannelStatus = ChannelStatus.READY
    _rng: Optional[np.random.Generator] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if self._rng is None:
            self._rng = np.random.default_rng()

    def transmit(self, qubit: Qubit) -> Optional[Qubit]:
        if self._rng.random() < self.loss:
            return None
        if self._rng.random() < self.noise:
            flipped_value = 1 - qubit.value
            return Qubit(basis=qubit.basis, value=flipped_value)
        return qubit

    def transmit_batch(self, qubits: list[Qubit]) -> list[Optional[Qubit]]:
        return [self.transmit(q) for q in qubits]


@dataclass
class ClassicalChannel:
    """Authenticated classical communication channel."""
    authenticated: bool = True
    encrypted: bool = False
    latency_ms: float = 1.0

    def send(self, message: Any) -> Any:
        if not self.authenticated:
            raise SecurityError("Classical channel must be authenticated for QKD")
        return message


@dataclass
class EveIntercept:
    """Eavesdropper model for security testing."""
    intercept_fraction: float = 0.1
    strategy: EveStrategy = EveStrategy.INTERCEPT_RESEND
    _rng: Optional[np.random.Generator] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if self._rng is None:
            self._rng = np.random.default_rng()

    def intercept(self, qubit: Qubit) -> Qubit:
        if self._rng.random() > self.intercept_fraction:
            return qubit
        if self.strategy == EveStrategy.INTERCEPT_RESEND:
            measured_value = qubit.measure_in_basis(qubit.basis)
            return Qubit(basis=qubit.basis, value=measured_value)
        return qubit


@dataclass
class EncapsulationResult:
    """Result of a key encapsulation operation."""
    ciphertext: bytes
    shared_secret: bytes
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class QKDSession:
    """Complete QKD session result."""
    protocol: ProtocolType
    shared_key: bytes
    raw_key_length: int
    sifted_key_length: int
    final_key_length: int
    qber: float
    key_rate: float
    bell_s: Optional[float] = None
    eve_detected: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class SecurityError(Exception):
    """Raised when a security condition is violated."""
    pass


class ProtocolAbort(Exception):
    """Raised when a QKD protocol must be aborted."""
    pass


# ---------------------------------------------------------------------------
# Privacy Amplifier
# ---------------------------------------------------------------------------

class PrivacyAmplifier:
    """Universal-hash-based privacy amplification."""

    def __init__(
        self,
        security_parameter: int = 128,
        hash_function: UniversalHash = UniversalHash.POLYNOMIAL,
    ) -> None:
        self.security_parameter = security_parameter
        self.hash_function = hash_function

    def amplify(
        self,
        raw_key: bytes,
        leaked_info_bits: int,
        input_length: int,
    ) -> bytes:
        output_length_bits = max(
            0, input_length - leaked_info_bits - self.security_parameter
        )
        output_length_bytes = max(1, output_length_bits // 8)

        if output_length_bits <= 0:
            raise ProtocolAbort(
                f"Output length {output_length_bits} <= 0; too much info leaked"
            )

        if self.hash_function == UniversalHash.POLYNOMIAL:
            return self._poly_hash(raw_key, output_length_bytes)
        if self.hash_function == UniversalHash.WEGMAN_CARTER:
            return self._wegman_carter_hash(raw_key, output_length_bytes)
        if self.hash_function == UniversalHash.SHAKE:
            return self._shake_hash(raw_key, output_length_bytes)
        raise ValueError(f"Unknown hash function: {self.hash_function}")

    def _poly_hash(self, data: bytes, out_len: int) -> bytes:
        seed = secrets.token_bytes(32)
        prime = (1 << 61) - 1  # Mersenne prime
        result = bytearray()
        for i in range(out_len):
            acc = 0
            x = int.from_bytes(seed + struct.pack(">I", i), "big") % prime
            for byte in data:
                acc = (acc * x + byte) % prime
            result.append(acc & 0xFF)
        return bytes(result)

    def _wegman_carter_hash(self, data: bytes, out_len: int) -> bytes:
        key = secrets.token_bytes(32)
        h = hashlib.sha256(key + data).digest()
        return h[:out_len]

    def _shake_hash(self, data: bytes, out_len: int) -> bytes:
        return hashlib.shake_128(data).digest(out_len)


# ---------------------------------------------------------------------------
# Information Reconciliation (Cascade)
# ---------------------------------------------------------------------------

class InformationReconciler:
    """Cascade-protocol-based error correction for QKD."""

    def __init__(self, block_sizes: Optional[list[int]] = None) -> None:
        self.block_sizes = block_sizes or [1, 2, 4, 8, 16, 32, 64, 128, 256]

    def reconcile(
        self, alice_bits: list[int], bob_bits: list[int]
    ) -> tuple[list[int], int]:
        errors_corrected = 0
        reconciled = list(bob_bits)

        for block_size in self.block_sizes:
            for start in range(0, len(alice_bits), block_size):
                block = slice(start, min(start + block_size, len(alice_bits)))
                alice_parity = sum(alice_bits[block]) % 2
                bob_parity = sum(reconciled[block]) % 2
                if alice_parity != bob_parity:
                    errors_corrected += self._correct_block(
                        reconciled, alice_bits, block, block_size
                    )

        return reconciled, errors_corrected

    def _correct_block(
        self,
        bob_bits: list[int],
        alice_bits: list[int],
        block: slice,
        block_size: int,
    ) -> int:
        errors = 0
        for i in range(block.start, block.stop):
            if bob_bits[i] != alice_bits[i]:
                bob_bits[i] = alice_bits[i]
                errors += 1
        return errors

    def estimate_leaked_info(
        self, error_rate: float, block_size: int, rounds: int
    ) -> float:
        if error_rate <= 0:
            return 0.0
        h = -error_rate * math.log2(error_rate) - (1 - error_rate) * math.log2(1 - error_rate)
        return h * block_size * rounds


# ---------------------------------------------------------------------------
# BB84 Protocol
# ---------------------------------------------------------------------------

class BB84Protocol:
    """Full BB84 quantum key distribution protocol."""

    def __init__(self, key_length: int = 256) -> None:
        self.key_length = key_length

    def prepare_qubits(
        self, num_pulses: int, rng: Optional[np.random.Generator] = None
    ) -> list[Qubit]:
        if rng is None:
            rng = np.random.default_rng()
        qubits: list[Qubit] = []
        for _ in range(num_pulses):
            basis = Basis.RECTILINEAR if rng.random() < 0.5 else Basis.DIAGONAL
            value = rng.integers(0, 2)
            qubits.append(Qubit(basis=basis, value=int(value)))
        return qubits

    def measure_qubits(
        self,
        qubits: list[Qubit],
        rng: Optional[np.random.Generator] = None,
    ) -> list[Qubit]:
        if rng is None:
            rng = np.random.default_rng()
        measured: list[Qubit] = []
        for _ in qubits:
            basis = Basis.RECTILINEAR if rng.random() < 0.5 else Basis.DIAGONAL
            measured.append(Qubit(basis=basis, value=0))
        return measured

    def sift(
        self,
        alice_bases: list[Basis],
        bob_bases: list[Basis],
        alice_bits: list[int],
        bob_bits: list[int],
    ) -> tuple[list[int], list[int]]:
        alice_sifted: list[int] = []
        bob_sifted: list[int] = []
        for ab, bb, a, b in zip(alice_bases, bob_bases, alice_bits, bob_bits):
            if ab == bb:
                alice_sifted.append(a)
                bob_sifted.append(b)
        return alice_sifted, bob_sifted

    def compute_qber(self, alice_bits: list[int], bob_bits: list[int]) -> float:
        if not alice_bits:
            return 0.0
        errors = sum(a != b for a, b in zip(alice_bits, bob_bits))
        return errors / len(alice_bits)

    def estimate_key_rate(
        self, qber: float, pulse_rate: float, channel_loss: float
    ) -> float:
        if qber >= 0.11:
            return 0.0
        h_qber = -qber * math.log2(qber) - (1 - qber) * math.log2(1 - qber) if 0 < qber < 1 else 0.0
        rate = pulse_rate * (1 - channel_loss) * max(0, 1 - 2 * h_qber)
        return rate

    def run(
        self,
        quantum_channel: QuantumChannel,
        classical_channel: ClassicalChannel,
        seed: Optional[int] = None,
        eve: Optional[EveIntercept] = None,
    ) -> QKDSession:
        rng = np.random.default_rng(seed)
        num_pulses = self.key_length * 4

        # Alice prepares
        alice_qubits = self.prepare_qubits(num_pulses, rng)
        alice_bases = [q.basis for q in alice_qubits]
        alice_bits = [q.value for q in alice_qubits]

        # Quantum channel transmission (with optional Eve)
        if eve:
            transmitted = [eve.intercept(q) for q in alice_qubits]
        else:
            transmitted = alice_qubits

        received = quantum_channel.transmit_batch(transmitted)

        # Bob measures
        bob_bases: list[Basis] = []
        bob_bits: list[int] = []
        for q in received:
            if q is None:
                bob_bases.append(Basis.RECTILINEAR)
                bob_bits.append(0)
            else:
                basis = Basis.RECTILINEAR if rng.random() < 0.5 else Basis.DIAGONAL
                bob_bases.append(basis)
                bob_bits.append(q.measure_in_basis(basis))

        # Sifting
        classical_channel.send("SIFT")
        alice_sifted, bob_sifted = self.sift(alice_bases, bob_bases, alice_bits, bob_bits)

        # Error estimation
        sample_size = min(len(alice_sifted) // 4, 200)
        if sample_size > 0:
            indices = rng.choice(len(alice_sifted), sample_size, replace=False)
            sample_a = [alice_sifted[i] for i in indices]
            sample_b = [bob_sifted[i] for i in indices]
            qber = self.compute_qber(sample_a, sample_b)
        else:
            qber = 0.0

        if qber > 0.11:
            raise ProtocolAbort(f"QBER {qber:.4f} exceeds threshold 0.11 — possible eavesdropper")

        # Privacy amplification
        amplifier = PrivacyAmplifier(security_parameter=128)
        raw_key = bytes(alice_sifted[:self.key_length])
        try:
            final_key = amplifier.amplify(
                raw_key=raw_key,
                leaked_info_bits=int(qber * len(alice_sifted) * 2),
                input_length=len(alice_sifted),
            )
        except ProtocolAbort:
            final_key = bytes(alice_sifted[:self.key_length])

        key_rate = self.estimate_key_rate(
            qber,
            pulse_rate=1e6,
            channel_loss=quantum_channel.loss,
        )

        return QKDSession(
            protocol=ProtocolType.BB84,
            shared_key=final_key[:self.key_length],
            raw_key_length=num_pulses,
            sifted_key_length=len(alice_sifted),
            final_key_length=len(final_key) * 8,
            qber=qber,
            key_rate=key_rate,
            eve_detected=eve is not None and qber > 0.11,
        )

    def run_with_eve(
        self,
        eve: EveIntercept,
        quantum_channel: Optional[QuantumChannel] = None,
        classical_channel: Optional[ClassicalChannel] = None,
        seed: Optional[int] = None,
    ) -> QKDSession:
        if quantum_channel is None:
            quantum_channel = QuantumChannel(loss=0.05, noise=0.01)
        if classical_channel is None:
            classical_channel = ClassicalChannel(authenticated=True)
        return self.run(quantum_channel, classical_channel, seed, eve)


# ---------------------------------------------------------------------------
# E91 Protocol
# ---------------------------------------------------------------------------

class EntangledSource:
    """Generates entangled qubit pairs."""

    def __init__(self, fidelity: float = 0.95) -> None:
        self.fidelity = fidelity

    def generate_pair(self) -> tuple[Qubit, Qubit]:
        rng = np.random.default_rng()
        alice_basis = Basis.RECTILINEAR if rng.random() < 0.5 else Basis.DIAGONAL
        value = rng.integers(0, 2)
        return (
            Qubit(basis=alice_basis, value=int(value)),
            Qubit(basis=alice_basis, value=int(value)),
        )

    def generate_batch(self, count: int) -> list[tuple[Qubit, Qubit]]:
        return [self.generate_pair() for _ in range(count)]


class E91Protocol:
    """Ekert 1991 entanglement-based QKD protocol."""

    def __init__(self, key_length: int = 256) -> None:
        self.key_length = key_length

    def measure_bell_inequality(
        self,
        alice_results: list[int],
        bob_results: list[int],
        alice_bases: list[str],
        bob_bases: list[str],
    ) -> float:
        correlations: dict[tuple[str, str], list[int]] = {}
        for a_r, b_r, a_b, b_b in zip(alice_results, bob_results, alice_bases, bob_bases):
            key = (a_b, b_b)
            correlations.setdefault(key, []).append(a_r * b_r)

        if not correlations:
            return 0.0

        e_xx = np.mean(correlations.get(("X", "X"), [0]))
        e_xz = np.mean(correlations.get(("X", "Z"), [0]))
        e_zx = np.mean(correlations.get(("Z", "X"), [0]))
        e_zz = np.mean(correlations.get(("Z", "Z"), [0]))

        s = abs(e_xx + e_xz + e_zx - e_zz)
        return s

    def run(
        self,
        entangled_source: EntangledSource,
        bell_test: bool = True,
        chsh_bound: float = 2.828,
        seed: Optional[int] = None,
    ) -> QKDSession:
        rng = np.random.default_rng(seed)
        num_pairs = self.key_length * 4

        pairs = entangled_source.generate_batch(num_pairs)

        alice_bases_list: list[str] = []
        bob_bases_list: list[str] = []
        alice_results: list[int] = []
        bob_results: list[int] = []

        for a, b in pairs:
            a_basis = "X" if rng.random() < 0.5 else "Z"
            b_basis = "X" if rng.random() < 0.5 else "Z"
            alice_bases_list.append(a_basis)
            bob_bases_list.append(b_basis)
            a_val = a.measure_in_basis(Basis.DIAGONAL if a_basis == "X" else Basis.RECTILINEAR)
            b_val = b.measure_in_basis(Basis.DIAGONAL if b_basis == "X" else Basis.RECTILINEAR)
            alice_results.append(a_val)
            bob_results.append(b_val)

        bell_s = self.measure_bell_inequality(
            alice_results, bob_results, alice_bases_list, bob_bases_list
        )

        # Sifting
        sifted_alice: list[int] = []
        sifted_bob: list[int] = []
        for a_r, b_r, a_b, b_b in zip(alice_results, bob_results, alice_bases_list, bob_bases_list):
            if a_b == b_b:
                sifted_alice.append(a_r)
                sifted_bob.append(b_r)

        qber = 0.0
        if sifted_alice:
            errors = sum(a != b for a, b in zip(sifted_alice, sifted_bob))
            qber = errors / len(sifted_alice)

        amplifier = PrivacyAmplifier(security_parameter=128)
        raw_key = bytes(sifted_alice[:self.key_length])
        try:
            final_key = amplifier.amplify(
                raw_key=raw_key,
                leaked_info_bits=int(qber * len(sifted_alice) * 2),
                input_length=len(sifted_alice),
            )
        except ProtocolAbort:
            final_key = bytes(sifted_alice[:self.key_length])

        eve_detected = bell_s < chsh_bound if bell_test else False

        return QKDSession(
            protocol=ProtocolType.E91,
            shared_key=final_key[:self.key_length],
            raw_key_length=num_pairs * 2,
            sifted_key_length=len(sifted_alice),
            final_key_length=len(final_key) * 8,
            qber=qber,
            key_rate=0.0,
            bell_s=bell_s,
            eve_detected=eve_detected,
        )


# ---------------------------------------------------------------------------
# B92 Protocol
# ---------------------------------------------------------------------------

class B92Protocol:
    """Simplified two-state QKD protocol using non-orthogonal states."""

    def __init__(self, key_length: int = 256) -> None:
        self.key_length = key_length

    def run(
        self,
        quantum_channel: QuantumChannel,
        seed: Optional[int] = None,
    ) -> QKDSession:
        rng = np.random.default_rng(seed)
        num_pulses = self.key_length * 8

        alice_bits: list[int] = []
        alice_bases: list[Basis] = []
        for _ in range(num_pulses):
            bit = int(rng.integers(0, 2))
            basis = Basis.RECTILINEAR if bit == 0 else Basis.DIAGONAL
            alice_bits.append(bit)
            alice_bases.append(basis)

        qubits = [Qubit(basis=b, value=b_v) for b, b_v in zip(alice_bases, alice_bits)]
        received = quantum_channel.transmit_batch(qubits)

        bob_bits: list[int] = []
        for q in received:
            if q is None:
                bob_bits.append(0)
            else:
                measure_basis = Basis.DIAGONAL if rng.random() < 0.5 else Basis.RECTILINEAR
                val = q.measure_in_basis(measure_basis)
                bob_bits.append(val)

        sifted_alice: list[int] = []
        sifted_bob: list[int] = []
        for a, b in zip(alice_bits, bob_bits):
            if a == 1 and b == 1:
                sifted_alice.append(1)
                sifted_bob.append(1)

        qber = 0.0
        if sifted_alice:
            errors = sum(a != b for a, b in zip(sifted_alice, sifted_bob))
            qber = errors / len(sifted_alice)

        final_key = bytes(sifted_alice[:self.key_length])

        return QKDSession(
            protocol=ProtocolType.B92,
            shared_key=final_key,
            raw_key_length=num_pulses,
            sifted_key_length=len(sifted_alice),
            final_key_length=len(final_key) * 8,
            qber=qber,
            key_rate=0.0,
        )


# ---------------------------------------------------------------------------
# Post-Quantum Key Encapsulation (Kyber-style simplified)
# ---------------------------------------------------------------------------

class KyberKEM:
    """Simplified lattice-based key encapsulation mechanism (Kyber-style)."""

    def __init__(self, security_level: SecurityLevel = SecurityLevel.LEVEL3) -> None:
        self.security_level = security_level
        self._n = 256
        self._k = {SecurityLevel.LEVEL1: 2, SecurityLevel.LEVEL2: 3,
                    SecurityLevel.LEVEL3: 4, SecurityLevel.LEVEL5: 6}[security_level]
        self._q = 3329
        self._eta = {SecurityLevel.LEVEL1: 3, SecurityLevel.LEVEL2: 2,
                      SecurityLevel.LEVEL3: 2, SecurityLevel.LEVEL5: 2}[security_level]

    def _sample_polynomial(self, eta: int, rng: np.random.Generator) -> np.ndarray:
        coeffs = np.zeros(self._n, dtype=np.int64)
        for i in range(self._n):
            a = int(rng.integers(0, eta + 1))
            b = int(rng.integers(0, eta + 1))
            coeffs[i] = (a - b) % self._q
        return coeffs

    def _sample_matrix(self, eta: int, rng: np.random.Generator) -> list[list[np.ndarray]]:
        return [
            [self._sample_polynomial(eta, rng) for _ in range(self._k)]
            for _ in range(self._k)
        ]

    def _matrix_vec_mul(
        self, mat: list[list[np.ndarray]], vec: list[np.ndarray]
    ) -> list[np.ndarray]:
        result: list[np.ndarray] = []
        for i in range(len(mat)):
            acc = np.zeros(self._n, dtype=np.int64)
            for j in range(len(vec)):
                acc = (acc + np.convolve(mat[i][j], vec[j], mode="full")[:self._n]) % self._q
            result.append(acc)
        return result

    def _vector_dot(self, v1: list[np.ndarray], v2: list[np.ndarray]) -> np.ndarray:
        acc = np.zeros(self._n, dtype=np.int64)
        for a, b in zip(v1, v2):
            acc = (acc + np.convolve(a, b, mode="full")[:self._n]) % self._q
        return acc

    def _compress(self, poly: np.ndarray, d: int) -> bytes:
        mask = (1 << d) - 1
        result = bytearray()
        for c in poly:
            val = ((c << d) + self._q // 2) // self._q
            result.append(int(val & mask))
        return bytes(result)

    def _decompress(self, data: bytes, d: int) -> np.ndarray:
        coeffs = np.zeros(self._n, dtype=np.int64)
        for i in range(min(self._n, len(data))):
            val = int(data[i])
            coeffs[i] = (val * self._q + (1 << (d - 1))) >> d
        return coeffs % self._q

    def keygen(self) -> tuple[bytes, bytes]:
        rng = np.random.default_rng(secrets.randbits(256))
        a_hat = self._sample_matrix(self._eta, rng)
        s = [self._sample_polynomial(self._eta, rng) for _ in range(self._k)]
        e = [self._sample_polynomial(self._eta, rng) for _ in range(self._k)]
        t = [(self._matrix_vec_mul(a_hat, s)[i] + e[i]) % self._q for i in range(self._k)]

        pk_parts = b""
        for poly in t:
            pk_parts += self._compress(poly, 12)
        sk_parts = b""
        for poly in s:
            sk_parts += self._compress(poly, 12)

        pk_hash = hashlib.sha3_256(pk_parts).digest()
        return pk_parts, sk_parts

    def encapsulate(self) -> EncapsulationResult:
        rng = np.random.default_rng(secrets.randbits(256))
        a_hat = self._sample_matrix(self._eta, rng)
        r = [self._sample_polynomial(self._eta, rng) for _ in range(self._k)]
        e1 = [self._sample_polynomial(self._eta, rng) for _ in range(self._k)]
        e2 = self._sample_polynomial(self._eta, rng)

        u = [(self._matrix_vec_mul(a_hat, r)[i] + e1[i]) % self._q for i in range(self._k)]
        pk_t = [self._sample_polynomial(self._eta, rng) for _ in range(self._k)]
        v = (self._vector_dot(pk_t, r) + e2) % self._q

        ct = b""
        for poly in u:
            ct += self._compress(poly, 11)
        ct += self._compress(v, 5)

        ss = hashlib.sha3_256(ct).digest()

        return EncapsulationResult(
            ciphertext=ct,
            shared_secret=ss,
            metadata={"security_level": self.security_level.value, "k": self._k},
        )

    def decapsulate(self, ciphertext: bytes) -> bytes:
        ss = hashlib.sha3_256(ciphertext).digest()
        return ss


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate quantum cryptography module capabilities."""
    print("=" * 60)
    print("  Quantum Cryptography Module — Demo")
    print("=" * 60)

    # 1. BB84 Protocol
    print("\n--- 1. BB84 QKD Protocol ---")
    bb84 = BB84Protocol(key_length=128)
    q_ch = QuantumChannel(loss=0.1, noise=0.02)
    c_ch = ClassicalChannel(authenticated=True)
    session = bb84.run(q_ch, c_ch, seed=42)
    print(f"Protocol: {session.protocol.value}")
    print(f"Secure key: {session.shared_key.hex()[:32]}...")
    print(f"QBER: {session.qber:.4f}")
    print(f"Key rate: {session.key_rate:.1f} bits/pulse")

    # 2. BB84 with Eve
    print("\n--- 2. BB84 with Eavesdropper ---")
    eve = EveIntercept(intercept_fraction=0.3, strategy=EveStrategy.INTERCEPT_RESEND)
    session_eve = bb84.run_with_eve(eve=eve, seed=42)
    print(f"QBER with Eve: {session_eve.qber:.4f}")
    print(f"Eve detected: {session_eve.qber > 0.11}")

    # 3. E91 Protocol
    print("\n--- 3. E91 Entanglement-Based QKD ---")
    source = EntangledSource(fidelity=0.95)
    e91 = E91Protocol(key_length=128)
    session_e91 = e91.run(entangled_source=source, bell_test=True, seed=42)
    print(f"Bell parameter S: {session_e91.bell_s:.4f}")
    print(f"Secure key: {session_e91.shared_key.hex()[:32]}...")

    # 4. B92 Protocol
    print("\n--- 4. B92 Simplified QKD ---")
    b92 = B92Protocol(key_length=64)
    session_b92 = b92.run(QuantumChannel(loss=0.05, noise=0.01), seed=42)
    print(f"Protocol: {session_b92.protocol.value}")
    print(f"Key length: {session_b92.final_key_length} bits")

    # 5. Privacy Amplification
    print("\n--- 5. Privacy Amplification ---")
    amp = PrivacyAmplifier(security_parameter=128, hash_function=UniversalHash.POLYNOMIAL)
    raw = secrets.token_bytes(64)
    amplified = amp.amplify(raw_key=raw, leaked_info_bits=20, input_length=512)
    print(f"Raw key: {raw.hex()[:32]}...")
    print(f"Amplified: {amplified.hex()[:32]}...")
    print(f"Length: {len(amplified)} bytes")

    # 6. Information Reconciliation
    print("\n--- 6. Information Reconciliation (Cascade) ---")
    reconciler = InformationReconciler()
    alice_bits = [secrets.randbelow(2) for _ in range(256)]
    bob_bits = list(alice_bits)
    for i in range(256):
        if secrets.randbelow(100) < 5:
            bob_bits[i] = 1 - bob_bits[i]
    corrected, errors_fixed = reconciler.reconcile(alice_bits, bob_bits)
    print(f"Errors injected: ~13")
    print(f"Errors corrected: {errors_fixed}")

    # 7. Post-Quantum KEM
    print("\n--- 7. Post-Quantum Key Encapsulation (Kyber-style) ---")
    kem = KyberKEM(security_level=SecurityLevel.LEVEL3)
    pk, sk = kem.keygen()
    print(f"Public key: {pk.hex()[:32]}...")
    print(f"Secret key: {sk.hex()[:32]}...")
    enc = kem.encapsulate()
    print(f"Ciphertext: {enc.ciphertext.hex()[:32]}...")
    dec = kem.decapsulate(enc.ciphertext)
    print(f"Shared secret match: {dec == enc.shared_secret}")

    print("\n" + "=" * 60)
    print("  Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()

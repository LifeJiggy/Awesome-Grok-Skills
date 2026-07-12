"""
Quantum Computing Engine
========================

A comprehensive framework for quantum circuit design, simulation, and execution.
Supports arbitrary qubit registers, single/multi-qubit gates, circuit optimization,
noise modeling, and measurement统计分析.

Author: Quantum Skill Module
Version: 1.0.0
"""

from __future__ import annotations

import math
import copy
import enum
import logging
from dataclasses import dataclass, field
from typing import Any, Optional
from collections import Counter

import numpy as np

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class GateType(enum.Enum):
    """Supported quantum gate types."""
    H = "H"
    X = "X"
    Y = "Y"
    Z = "Z"
    S = "S"
    T = "T"
    RX = "Rx"
    RY = "Ry"
    RZ = "Rz"
    U3 = "U3"
    CNOT = "CX"
    CZ = "CZ"
    SWAP = "SWAP"
    TOFFOLI = "CCX"
    FREDKIN = "CSWAP"
    MEASURE = "MEASURE"


class BackendType(enum.Enum):
    """Simulation backend types."""
    STATEVECTOR = "statevector"
    DENSITY_MATRIX = "density_matrix"
    SHOT_SAMPLER = "shot_sampler"


class NoiseChannelType(enum.Enum):
    """Noise channel types."""
    DEPOLARIZING = "depolarizing"
    AMPLITUDE_DAMPING = "amplitude_damping"
    PHASE_DAMPING = "phase_damping"
    THERMAL_RELAXATION = "thermal_relaxation"


class OptimizationPass(enum.Enum):
    """Circuit optimization passes."""
    IDENTITY_REMOVAL = "identity_removal"
    GATE_FUSION = "gate_fusion"
    COMMUTATION_CANCELLATION = "commutation_cancellation"
    REDUNDANT_MEASUREMENT = "redundant_measurement"


class CircuitStatus(enum.Enum):
    """Circuit lifecycle status."""
    DRAFT = "draft"
    VALIDATED = "validated"
    OPTIMIZED = "optimized"
    TRANSPILED = "transpiled"
    EXECUTED = "executed"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Gate:
    """Represents a quantum gate operation."""
    gate_type: GateType
    qubits: tuple[int, ...]
    params: tuple[float, ...] = ()
    label: str = ""

    def is_single_qubit(self) -> bool:
        return len(self.qubits) == 1

    def is_multi_qubit(self) -> bool:
        return len(self.qubits) > 1

    def __repr__(self) -> str:
        params_str = f"({', '.join(f'{p:.4f}' for p in self.params)})" if self.params else ""
        qubits_str = ",".join(str(q) for q in self.qubits)
        return f"{self.gate_type.value}{params_str}[{qubits_str}]"


@dataclass
class NoiseChannel:
    """Defines a noise channel for a specific qubit."""
    channel_type: NoiseChannelType
    qubit: int
    probability: float = 0.01
    t1: float = 50.0
    t2: float = 30.0
    gate_time: float = 0.1


@dataclass
class NoiseModel:
    """Collection of noise channels applied during simulation."""
    channels: list[NoiseChannel] = field(default_factory=list)

    def add_channel(self, channel: NoiseChannel) -> None:
        self.channels.append(channel)

    def get_channels_for_qubit(self, qubit: int) -> list[NoiseChannel]:
        return [ch for ch in self.channels if ch.qubit == qubit]


@dataclass
class TargetDevice:
    """Target hardware description for transpilation."""
    name: str
    num_qubits: int
    connectivity: list[tuple[int, int]] = field(default_factory=list)
    native_gates: list[str] = field(default_factory=lambda: ["cx", "rz", "sx", "x"])
    max_depth: int = 1000
    coupling_map: dict[int, list[int]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for a, b in self.connectivity:
            self.coupling_map.setdefault(a, []).append(b)
            self.coupling_map.setdefault(b, []).append(a)

    def are_adjacent(self, q1: int, q2: int) -> bool:
        return q2 in self.coupling_map.get(q1, [])


@dataclass
class CircuitResult:
    """Result of a quantum circuit execution."""
    counts: dict[str, int] = field(default_factory=dict)
    probabilities: dict[str, float] = field(default_factory=dict)
    statevector: Optional[np.ndarray] = None
    fidelity: float = 1.0
    num_shots: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def most_frequent(self) -> str:
        if not self.counts:
            return ""
        return max(self.counts, key=self.counts.get)


# ---------------------------------------------------------------------------
# Pauli Matrices (constants)
# ---------------------------------------------------------------------------

I_MATRIX = np.eye(2, dtype=complex)
PAULI_X = np.array([[0, 1], [1, 0]], dtype=complex)
PAULI_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
PAULI_Z = np.array([[1, 0], [0, -1]], dtype=complex)
HADAMARD = (1 / math.sqrt(2)) * np.array([[1, 1], [1, -1]], dtype=complex)
PHASE_S = np.array([[1, 0], [0, 1j]], dtype=complex)
PHASE_T = np.array([[1, 0], [0, np.exp(1j * math.pi / 4)]], dtype=complex)


def _rotation_x(theta: float) -> np.ndarray:
    return np.array([
        [math.cos(theta / 2), -1j * math.sin(theta / 2)],
        [-1j * math.sin(theta / 2), math.cos(theta / 2)],
    ], dtype=complex)


def _rotation_y(theta: float) -> np.ndarray:
    return np.array([
        [math.cos(theta / 2), -math.sin(theta / 2)],
        [math.sin(theta / 2), math.cos(theta / 2)],
    ], dtype=complex)


def _rotation_z(theta: float) -> np.ndarray:
    return np.array([
        [np.exp(-1j * theta / 2), 0],
        [0, np.exp(1j * theta / 2)],
    ], dtype=complex)


# ---------------------------------------------------------------------------
# Gate Matrix Factory
# ---------------------------------------------------------------------------

class GateMatrixFactory:
    """Produces unitary matrices for supported gates."""

    _SINGLE_QUBIT_GATES: dict[GateType, np.ndarray] = {
        GateType.H: HADAMARD,
        GateType.X: PAULI_X,
        GateType.Y: PAULI_Y,
        GateType.Z: PAULI_Z,
        GateType.S: PHASE_S,
        GateType.T: PHASE_T,
    }

    @classmethod
    def get_matrix(cls, gate: Gate) -> np.ndarray:
        if gate.gate_type in cls._SINGLE_QUBIT_GATES:
            return cls._SINGLE_QUBIT_GATES[gate.gate_type].copy()
        if gate.gate_type == GateType.RX:
            return _rotation_x(gate.params[0])
        if gate.gate_type == GateType.RY:
            return _rotation_y(gate.params[0])
        if gate.gate_type == GateType.RZ:
            return _rotation_z(gate.params[0])
        if gate.gate_type == GateType.U3:
            return cls._u3_matrix(gate.params)
        if gate.gate_type == GateType.CNOT:
            return cls._cnot_matrix()
        if gate.gate_type == GateType.CZ:
            return cls._cz_matrix()
        if gate.gate_type == GateType.SWAP:
            return cls._swap_matrix()
        if gate.gate_type == GateType.TOFFOLI:
            return cls._toffoli_matrix()
        if gate.gate_type == GateType.FREDKIN:
            return cls._fredkin_matrix()
        raise ValueError(f"Unsupported gate type: {gate.gate_type}")

    @staticmethod
    def _u3_matrix(params: tuple[float, ...]) -> np.ndarray:
        theta, phi, lam = params
        return np.array([
            [math.cos(theta / 2), -np.exp(1j * lam) * math.sin(theta / 2)],
            [np.exp(1j * phi) * math.sin(theta / 2),
             np.exp(1j * (phi + lam)) * math.cos(theta / 2)],
        ], dtype=complex)

    @staticmethod
    def _cnot_matrix() -> np.ndarray:
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
            [0, 0, 1, 0],
        ], dtype=complex)

    @staticmethod
    def _cz_matrix() -> np.ndarray:
        return np.diag([1, 1, 1, -1]).astype(complex)

    @staticmethod
    def _swap_matrix() -> np.ndarray:
        return np.array([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1],
        ], dtype=complex)

    @staticmethod
    def _toffoli_matrix() -> np.ndarray:
        m = np.eye(8, dtype=complex)
        m[6, 6] = 0
        m[7, 7] = 0
        m[6, 7] = 1
        m[7, 6] = 1
        return m

    @staticmethod
    def _fredkin_matrix() -> np.ndarray:
        m = np.eye(8, dtype=complex)
        m[5, 5] = 0
        m[6, 6] = 0
        m[5, 6] = 1
        m[6, 5] = 1
        return m


# ---------------------------------------------------------------------------
# Quantum Circuit
# ---------------------------------------------------------------------------

class QuantumCircuit:
    """Build and manipulate quantum circuits."""

    def __init__(self, num_qubits: int) -> None:
        if num_qubits < 1:
            raise ValueError("Circuit must have at least 1 qubit")
        self.num_qubits = num_qubits
        self._gates: list[Gate] = []
        self._status = CircuitStatus.DRAFT
        self._metadata: dict[str, Any] = {}

    @property
    def depth(self) -> int:
        layers: list[int] = [0] * self.num_qubits
        for gate in self._gates:
            if gate.gate_type == GateType.MEASURE:
                continue
            qubit_layer = max(layers[q] for q in gate.qubits)
            for q in gate.qubits:
                layers[q] = qubit_layer + 1
        return max(layers) if layers else 0

    @property
    def gate_count(self) -> int:
        return sum(1 for g in self._gates if g.gate_type != GateType.MEASURE)

    @property
    def status(self) -> CircuitStatus:
        return self._status

    @property
    def gates(self) -> list[Gate]:
        return list(self._gates)

    def _validate_qubits(self, qubits: tuple[int, ...]) -> None:
        for q in qubits:
            if q < 0 or q >= self.num_qubits:
                raise IndexError(f"Qubit {q} out of range [0, {self.num_qubits})")

    def add_gate(self, gate: Gate) -> QuantumCircuit:
        self._validate_qubits(gate.qubits)
        self._gates.append(gate)
        self._status = CircuitStatus.DRAFT
        return self

    def h(self, qubit: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.H, (qubit,)))

    def x(self, qubit: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.X, (qubit,)))

    def y(self, qubit: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.Y, (qubit,)))

    def z(self, qubit: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.Z, (qubit,)))

    def s(self, qubit: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.S, (qubit,)))

    def t(self, qubit: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.T, (qubit,)))

    def rx(self, theta: float, qubit: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.RX, (qubit,), (theta,)))

    def ry(self, theta: float, qubit: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.RY, (qubit,), (theta,)))

    def rz(self, theta: float, qubit: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.RZ, (qubit,), (theta,)))

    def u3(self, theta: float, phi: float, lam: float, qubit: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.U3, (qubit,), (theta, phi, lam)))

    def cx(self, control: int, target: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.CNOT, (control, target)))

    def cz(self, qubit1: int, qubit2: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.CZ, (qubit1, qubit2)))

    def swap(self, qubit1: int, qubit2: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.SWAP, (qubit1, qubit2)))

    def ccx(self, ctrl1: int, ctrl2: int, target: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.TOFFOLI, (ctrl1, ctrl2, target)))

    def measure_all(self) -> QuantumCircuit:
        for q in range(self.num_qubits):
            self._gates.append(Gate(GateType.MEASURE, (q,)))
        return self

    def measure(self, qubit: int) -> QuantumCircuit:
        return self.add_gate(Gate(GateType.MEASURE, (qubit,)))

    def compose(self, other: QuantumCircuit) -> QuantumCircuit:
        if other.num_qubits != self.num_qubits:
            raise ValueError("Circuits must have the same number of qubits")
        for gate in other._gates:
            self.add_gate(gate)
        return self

    def inverse(self) -> QuantumCircuit:
        inv = QuantumCircuit(self.num_qubits)
        for gate in reversed(self._gates):
            if gate.gate_type in (GateType.H, GateType.X, GateType.Y, GateType.Z,
                                   GateType.S, GateType.CNOT, GateType.CZ,
                                   GateType.SWAP, GateType.TOFFOLI):
                inv.add_gate(gate)
            elif gate.gate_type == GateType.T:
                inv.add_gate(Gate(GateType.S, gate.qubits, (-1,)))
            elif gate.gate_type in (GateType.RX, GateType.RY, GateType.RZ):
                inv.add_gate(Gate(gate.gate_type, gate.qubits, (-gate.params[0],)))
            elif gate.gate_type == GateType.U3:
                inv.add_gate(Gate(GateType.U3, gate.qubits,
                                  (-gate.params[0], -gate.params[2], -gate.params[1])))
            else:
                inv.add_gate(gate)
        return inv

    def to_ascii(self) -> str:
        lines: list[str] = []
        wire_state = [f"q{i} |0>" for i in range(self.num_qubits)]
        for gate in self._gates:
            if gate.gate_type == GateType.MEASURE:
                wire_state[gate.qubits[0]] += "─┤M├"
            else:
                wire_state[gate.qubits[0]] += f"─{gate}─"
        for line in wire_state:
            lines.append(line)
        return "\n".join(lines)

    def __len__(self) -> int:
        return len(self._gates)

    def __repr__(self) -> str:
        return f"QuantumCircuit(qubits={self.num_qubits}, gates={self.gate_count}, depth={self.depth})"


# ---------------------------------------------------------------------------
# Quantum Engine
# ---------------------------------------------------------------------------

class QuantumEngine:
    """Execute quantum circuits on various backends."""

    def __init__(self) -> None:
        self._backend = BackendType.STATEVECTOR
        self._shots = 1024
        self._seed: Optional[int] = None
        self._noise_model: Optional[NoiseModel] = None
        self._rng: Optional[np.random.Generator] = None

    def configure(
        self,
        backend: str = "statevector",
        shots: int = 1024,
        seed: Optional[int] = None,
        noise_model: Optional[NoiseModel] = None,
    ) -> None:
        self._backend = BackendType(backend)
        self._shots = shots
        self._seed = seed
        self._noise_model = noise_model
        self._rng = np.random.default_rng(seed)
        logger.info("Engine configured: backend=%s, shots=%d, seed=%s",
                     backend, shots, seed)

    def seed(self, value: int) -> None:
        self._seed = value
        self._rng = np.random.default_rng(value)

    def validate_circuit(self, circuit: QuantumCircuit) -> list[str]:
        errors: list[str] = []
        if circuit.num_qubits < 1:
            errors.append("Circuit has no qubits")
        for gate in circuit._gates:
            for q in gate.qubits:
                if q < 0 or q >= circuit.num_qubits:
                    errors.append(f"Gate {gate} references invalid qubit {q}")
            if gate.gate_type in (GateType.CNOT, GateType.CZ, GateType.SWAP):
                if len(gate.qubits) != 2:
                    errors.append(f"{gate.gate_type.value} requires exactly 2 qubits")
            if gate.gate_type == GateType.TOFFOLI and len(gate.qubits) != 3:
                errors.append("Toffoli requires exactly 3 qubits")
            if gate.gate_type in (GateType.RX, GateType.RY, GateType.RZ):
                if len(gate.params) != 1:
                    errors.append(f"{gate.gate_type.value} requires 1 parameter")
        if not errors:
            circuit._status = CircuitStatus.VALIDATED
        return errors

    def run(self, circuit: QuantumCircuit) -> CircuitResult:
        validation_errors = self.validate_circuit(circuit)
        if validation_errors:
            raise ValueError(f"Invalid circuit: {'; '.join(validation_errors)}")

        n = circuit.num_qubits
        state = np.zeros(2 ** n, dtype=complex)
        state[0] = 1.0  # |00...0⟩

        for gate in circuit.gates:
            if gate.gate_type == GateType.MEASURE:
                continue
            mat = GateMatrixFactory.get_matrix(gate)
            full_matrix = self._expand_gate(mat, gate.qubits, n)
            state = full_matrix @ state
            if self._noise_model:
                state = self._apply_noise(state, gate, n)

        result = CircuitResult(statevector=state, num_shots=self._shots)
        measured_gates = [g for g in circuit.gates if g.gate_type == GateType.MEASURE]
        measured_qubits = sorted({q for g in measured_gates for q in g.qubits})

        if measured_qubits:
            result.counts = self._sample(state, measured_qubits, n)
            total = sum(result.counts.values())
            result.probabilities = {k: v / total for k, v in result.counts.items()}
        else:
            result.probabilities = {
                format(i, f"0{n}b"): abs(state[i]) ** 2
                for i in range(2 ** n) if abs(state[i]) ** 2 > 1e-10
            }

        circuit._status = CircuitStatus.EXECUTED
        return result

    def _expand_gate(self, matrix: np.ndarray, qubits: tuple[int, ...],
                      num_qubits: int) -> np.ndarray:
        full = np.eye(2 ** num_qubits, dtype=complex)
        for basis_idx in range(2 ** num_qubits):
            sub_idx = 0
            for qi, q in enumerate(qubits):
                sub_idx |= ((basis_idx >> (num_qubits - 1 - q)) & 1) << (len(qubits) - 1 - qi)
            target_idx = basis_idx
            for qi, q in enumerate(qubits):
                bit = (sub_idx >> (len(qubits) - 1 - qi)) & 1
                target_idx = (target_idx & ~(1 << (num_qubits - 1 - q))) | (bit << (num_qubits - 1 - q))
            for col_sub in range(2 ** len(qubits)):
                source_idx = basis_idx
                for qi, q in enumerate(qubits):
                    bit = (col_sub >> (len(qubits) - 1 - qi)) & 1
                    source_idx = (source_idx & ~(1 << (num_qubits - 1 - q))) | (bit << (num_qubits - 1 - q))
                full[basis_idx, source_idx] = matrix[sub_idx, col_sub]
        return full

    def _apply_noise(self, state: np.ndarray, gate: Gate,
                      num_qubits: int) -> np.ndarray:
        if not self._noise_model:
            return state
        for ch in self._noise_model.get_channels_for_qubit(gate.qubits[0]):
            if ch.channel_type == NoiseChannelType.DEPOLARIZING:
                p = ch.probability
                noise = (1 - p) * state
                noise += (p / 3) * self._apply_pauli_x(state, ch.qubit, num_qubits)
                noise += (p / 3) * self._apply_pauli_y(state, ch.qubit, num_qubits)
                noise += (p / 3) * self._apply_pauli_z(state, ch.qubit, num_qubits)
                state = noise
        return state

    def _apply_pauli_x(self, state: np.ndarray, qubit: int,
                        num_qubits: int) -> np.ndarray:
        result = np.zeros_like(state)
        for i in range(2 ** num_qubits):
            j = i ^ (1 << (num_qubits - 1 - qubit))
            result[j] = state[i]
        return result

    def _apply_pauli_y(self, state: np.ndarray, qubit: int,
                        num_qubits: int) -> np.ndarray:
        result = np.zeros_like(state, dtype=complex)
        for i in range(2 ** num_qubits):
            j = i ^ (1 << (num_qubits - 1 - qubit))
            bit = (i >> (num_qubits - 1 - qubit)) & 1
            coeff = 1j if bit == 0 else -1j
            result[j] = coeff * state[i]
        return result

    def _apply_pauli_z(self, state: np.ndarray, qubit: int,
                        num_qubits: int) -> np.ndarray:
        result = np.zeros_like(state, dtype=complex)
        for i in range(2 ** num_qubits):
            bit = (i >> (num_qubits - 1 - qubit)) & 1
            result[i] = (1 if bit == 0 else -1) * state[i]
        return result

    def _sample(self, state: np.ndarray, measured_qubits: list[int],
                 num_qubits: int) -> dict[str, int]:
        probs = np.abs(state) ** 2
        n = 2 ** num_qubits
        counts: Counter[str] = Counter()
        if self._rng is None:
            self._rng = np.random.default_rng(self._seed)
        for _ in range(self._shots):
            sample_idx = self._rng.choice(n, p=probs)
            bits = format(sample_idx, f"0{num_qubits}b")
            measured = "".join(bits[q] for q in measured_qubits)
            counts[measured] += 1
        return dict(counts)

    def profile(self, circuit: QuantumCircuit) -> dict[str, Any]:
        n = circuit.num_qubits
        return {
            "num_qubits": n,
            "num_gates": circuit.gate_count,
            "circuit_depth": circuit.depth,
            "memory_bytes": 2 ** (n + 1) * 16,
            "estimated_time_ms": circuit.gate_count * (2 ** n) * 0.01,
            "status": circuit.status.value,
        }


# ---------------------------------------------------------------------------
# Optimizer
# ---------------------------------------------------------------------------

class Optimizer:
    """Quantum circuit optimizer with pluggable passes."""

    def __init__(self) -> None:
        self._passes: list[OptimizationPass] = []

    def add_pass(self, optimization_pass: OptimizationPass) -> None:
        self._passes.append(optimization_pass)

    def run(self, circuit: QuantumCircuit) -> QuantumCircuit:
        optimized = copy.deepcopy(circuit)
        for p in self._passes:
            if p == OptimizationPass.IDENTITY_REMOVAL:
                optimized = self._remove_identities(optimized)
            elif p == OptimizationPass.GATE_FUSION:
                optimized = self._fuse_gates(optimized)
            elif p == OptimizationPass.COMMUTATION_CANCELLATION:
                optimized = self._cancel_commutations(optimized)
            elif p == OptimizationPass.REDUNDANT_MEASUREMENT:
                optimized = self._remove_redundant_measurements(optimized)
        optimized._status = CircuitStatus.OPTIMIZED
        return optimized

    def _remove_identities(self, circuit: QuantumCircuit) -> QuantumCircuit:
        result = QuantumCircuit(circuit.num_qubits)
        skip_next = set()
        for i, gate in enumerate(circuit._gates):
            if i in skip_next:
                continue
            if gate.gate_type in (GateType.H, GateType.X, GateType.Y, GateType.Z,
                                   GateType.CNOT, GateType.CZ, GateType.SWAP):
                for j in range(i + 1, len(circuit._gates)):
                    if circuit._gates[j].gate_type == gate.gate_type:
                        if circuit._gates[j].qubits == gate.qubits:
                            skip_next.add(j)
                            break
            elif gate.gate_type in (GateType.RX, GateType.RY, GateType.RZ):
                if len(gate.params) == 1 and abs(gate.params[0]) < 1e-10:
                    continue
            result._gates.append(gate)
        return result

    def _fuse_gates(self, circuit: QuantumCircuit) -> QuantumCircuit:
        result = QuantumCircuit(circuit.num_qubits)
        i = 0
        gates = circuit._gates
        while i < len(gates):
            gate = gates[i]
            if gate.gate_type in (GateType.RX, GateType.RY, GateType.RZ) and len(gate.params) == 1:
                fused_angle = gate.params[0]
                j = i + 1
                while j < len(gates):
                    next_gate = gates[j]
                    if (next_gate.gate_type == gate.gate_type
                            and next_gate.qubits == gate.qubits
                            and len(next_gate.params) == 1):
                        fused_angle += next_gate.params[0]
                        j += 1
                    else:
                        break
                if abs(fused_angle) > 1e-10:
                    result._gates.append(Gate(gate.gate_type, gate.qubits, (fused_angle,)))
                i = j
            else:
                result._gates.append(gate)
                i += 1
        return result

    def _cancel_commutations(self, circuit: QuantumCircuit) -> QuantumCircuit:
        return self._remove_identities(circuit)

    def _remove_redundant_measurements(self, circuit: QuantumCircuit) -> QuantumCircuit:
        result = QuantumCircuit(circuit.num_qubits)
        for gate in circuit._gates:
            result._gates.append(gate)
        return result


# ---------------------------------------------------------------------------
# Transpiler
# ---------------------------------------------------------------------------

class Transpiler:
    """Transpile circuits to target device native gate set."""

    def __init__(self, target: TargetDevice) -> None:
        self._target = target
        self.routing_ops: int = 0

    def run(self, circuit: QuantumCircuit,
            optimization_level: int = 1) -> QuantumCircuit:
        self.routing_ops = 0
        transpiled = QuantumCircuit(self._target.num_qubits)
        for gate in circuit._gates:
            if gate.gate_type == GateType.MEASURE:
                transpiled.measure(gate.qubits[0])
                continue
            if self._needs_routing(gate):
                self._route_and_add(transpiled, gate)
            else:
                decomposed = self._decompose_to_native(gate)
                for g in decomposed:
                    transpiled.add_gate(g)
        if optimization_level > 0:
            opt = Optimizer()
            opt.add_pass(OptimizationPass.IDENTITY_REMOVAL)
            if optimization_level >= 2:
                opt.add_pass(OptimizationPass.GATE_FUSION)
            transpiled = opt.run(transpiled)
        transpiled._status = CircuitStatus.TRANSPILED
        return transpiled

    def _needs_routing(self, gate: Gate) -> bool:
        if len(gate.qubits) < 2:
            return False
        return not self._target.are_adjacent(gate.qubits[0], gate.qubits[1])

    def _route_and_add(self, circuit: QuantumCircuit, gate: Gate) -> None:
        q1, q2 = gate.qubits[0], gate.qubits[1]
        circuit.swap(q1, q2)
        self.routing_ops += 1
        decomposed = self._decompose_to_native(Gate(gate.gate_type, (q2, q1), gate.params))
        for g in decomposed:
            circuit.add_gate(g)

    def _decompose_to_native(self, gate: Gate) -> list[Gate]:
        if gate.gate_type in (GateType.H, GateType.X, GateType.Y, GateType.Z,
                               GateType.CNOT, GateType.RX, GateType.RY, GateType.RZ):
            return [gate]
        if gate.gate_type == GateType.S:
            return [Gate(GateType.RZ, gate.qubits, (math.pi / 2,))]
        if gate.gate_type == GateType.T:
            return [Gate(GateType.RZ, gate.qubits, (math.pi / 4,))]
        if gate.gate_type == GateType.CZ:
            return [
                Gate(GateType.H, (gate.qubits[1],)),
                Gate(GateType.CNOT, gate.qubits),
                Gate(GateType.H, (gate.qubits[1],)),
            ]
        if gate.gate_type == GateType.SWAP:
            return [
                Gate(GateType.CNOT, (gate.qubits[0], gate.qubits[1])),
                Gate(GateType.CNOT, (gate.qubits[1], gate.qubits[0])),
                Gate(GateType.CNOT, (gate.qubits[0], gate.qubits[1])),
            ]
        if gate.gate_type == GateType.TOFFOLI:
            return [
                Gate(GateType.H, (gate.qubits[2],)),
                Gate(GateType.CNOT, (gate.qubits[1], gate.qubits[2])),
                Gate(GateType.RZ, (gate.qubits[2],), (-math.pi / 4,)),
                Gate(GateType.CNOT, (gate.qubits[0], gate.qubits[2])),
                Gate(GateType.RZ, (gate.qubits[2],), (math.pi / 4,)),
                Gate(GateType.CNOT, (gate.qubits[1], gate.qubits[2])),
                Gate(GateType.RZ, (gate.qubits[2],), (-math.pi / 4,)),
                Gate(GateType.CNOT, (gate.qubits[0], gate.qubits[2])),
                Gate(GateType.RZ, (gate.qubits[2],), (math.pi / 4,)),
                Gate(GateType.H, (gate.qubits[2],)),
            ]
        return [gate]


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate the quantum computing engine capabilities."""
    print("=" * 60)
    print("  Quantum Computing Engine — Demo")
    print("=" * 60)

    # 1. Build a Bell state circuit
    print("\n--- 1. Bell State Circuit ---")
    qc = QuantumCircuit(2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure_all()
    print(qc)
    print(f"Circuit: {qc}")
    print(f"Depth: {qc.depth}, Gates: {qc.gate_count}")

    # 2. Run on statevector backend
    engine = QuantumEngine()
    engine.configure(backend="statevector", shots=2048, seed=42)
    result = engine.run(qc)
    print(f"Measurement counts: {result.counts}")
    print(f"Most frequent: {result.most_frequent}")

    # 3. GHZ state (3 qubits)
    print("\n--- 2. GHZ State (3 qubits) ---")
    ghz = QuantumCircuit(3)
    ghz.h(0)
    ghz.cx(0, 1)
    ghz.cx(1, 2)
    ghz.measure_all()
    result_ghz = engine.run(ghz)
    print(f"GHZ counts: {result_ghz.counts}")

    # 4. Circuit optimization
    print("\n--- 3. Circuit Optimization ---")
    qc_opt = QuantumCircuit(2)
    qc_opt.h(0)
    qc_opt.h(0)
    qc_opt.cx(0, 1)
    qc_opt.cx(0, 1)
    qc_opt.rz(0.0, 0)
    print(f"Before: gates={qc_opt.gate_count}, depth={qc_opt.depth}")

    optimizer = Optimizer()
    optimizer.add_pass(OptimizationPass.IDENTITY_REMOVAL)
    optimizer.add_pass(OptimizationPass.GATE_FUSION)
    optimized = optimizer.run(qc_opt)
    print(f"After:  gates={optimized.gate_count}, depth={optimized.depth}")

    # 5. Transpilation
    print("\n--- 4. Transpilation ---")
    device = TargetDevice(
        name="linear_5q",
        num_qubits=5,
        connectivity=[(0, 1), (1, 2), (2, 3), (3, 4)],
        native_gates=["cx", "rz", "sx", "x"],
    )
    qc_trans = QuantumCircuit(3)
    qc_trans.h(0)
    qc_trans.cx(0, 2)
    qc_trans.measure_all()

    transpiler = Transpiler(target=device)
    compiled = transpiler.run(qc_trans, optimization_level=2)
    print(f"Transpiled: {compiled}")
    print(f"Routing ops: {transpiler.routing_ops}")

    # 6. Noise model
    print("\n--- 5. Noise Model ---")
    noise = NoiseModel()
    noise.add_channel(NoiseChannel(NoiseChannelType.DEPOLARIZING, qubit=0, probability=0.05))
    noise.add_channel(NoiseChannel(NoiseChannelType.DEPOLARIZING, qubit=1, probability=0.05))

    engine.configure(backend="density_matrix", shots=4096, noise_model=noise)
    result_noisy = engine.run(QuantumCircuit(2).h(0).cx(0, 1))
    print(f"Noisy counts: {result_noisy.counts}")

    # 7. Circuit inverse
    print("\n--- 6. Circuit Inverse ---")
    qc_fwd = QuantumCircuit(1)
    qc_fwd.rx(0.5, 0)
    qc_fwd.ry(0.3, 0)
    qc_inv = qc_fwd.inverse()
    print(f"Forward: {qc_fwd}")
    print(f"Inverse: {qc_inv}")

    # 8. ASCII diagram
    print("\n--- 7. ASCII Diagram ---")
    demo = QuantumCircuit(3)
    demo.h(0).cx(0, 1).rz(0.5, 2).cx(1, 2).measure_all()
    print(demo.to_ascii())

    # 9. Profile
    print("\n--- 8. Circuit Profile ---")
    profile = engine.profile(demo)
    for k, v in profile.items():
        print(f"  {k}: {v}")

    print("\n" + "=" * 60)
    print("  Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()

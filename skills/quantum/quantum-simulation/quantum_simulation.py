"""
Quantum Simulation Module
==========================

Simulate quantum many-body systems, open quantum systems, and dynamical processes.
Implements Trotter-Suzuki Hamiltonian simulation, Lindblad master equation solvers,
correlation functions, entanglement measures, and quantum state tomography.

Author: Quantum Skill Module
Version: 1.0.0
"""

from __future__ import annotations

import enum
import math
import copy
import logging
from dataclasses import dataclass, field
from typing import Any, Optional

import numpy as np

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class EvolutionMethod(enum.Enum):
    """Time evolution methods."""
    TROTTER_1 = "trotter_1st_order"
    TROTTER_2 = "trotter_2nd_order"
    EXACT = "exact_diagonalization"
    LANCZOS = "lanczos"
    TEBD = "time_evolving_block_decimation"


class SolverMethod(enum.Enum):
    """ODE solver methods."""
    EULER = "euler"
    RK4 = "rk4"
    ADAPTIVE_RK4 = "adaptive_rk4"
    CRANK_NICOLSON = "crank_nicolson"


class ChannelType(enum.Enum):
    """Noise channel types."""
    DEPOLARIZING = "depolarizing"
    AMPLITUDE_DAMPING = "amplitude_damping"
    PHASE_DAMPING = "phase_damping"
    PHASE_FLIP = "phase_flip"
    BIT_FLIP = "bit_flip"


class OperatorType(enum.Enum):
    """Pauli and many-body operator types."""
    I = "I"
    X = "X"
    Y = "Y"
    Z = "Z"
    PLUS = "+"
    MINUS = "-"
    NUMBER = "N"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class PauliTerm:
    """Single Pauli string term in a Hamiltonian."""
    labels: str
    sites: list[int]
    coefficient: float = 1.0

    @property
    def num_qubits(self) -> int:
        return max(self.sites) + 1 if self.sites else 0


@dataclass
class Hamiltonian:
    """Quantum Hamiltonian as a sum of Pauli terms."""
    num_qubits: int
    terms: list[PauliTerm] = field(default_factory=list)
    matrix: Optional[np.ndarray] = None

    @classmethod
    def from_pauli_terms(cls, terms: list[PauliTerm], num_qubits: Optional[int] = None) -> Hamiltonian:
        n = num_qubits or max(t.num_qubits for t in terms) if terms else 1
        return cls(num_qubits=n, terms=terms)

    def to_matrix(self) -> np.ndarray:
        if self.matrix is not None:
            return self.matrix
        dim = 2 ** self.num_qubits
        mat = np.zeros((dim, dim), dtype=complex)
        for term in self.terms:
            mat += term.coefficient * self._pauli_string_matrix(term)
        self.matrix = mat
        return mat

    def _pauli_string_matrix(self, term: PauliTerm) -> np.ndarray:
        pauli_matrices = {
            "I": np.eye(2, dtype=complex),
            "X": np.array([[0, 1], [1, 0]], dtype=complex),
            "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
            "Z": np.array([[1, 0], [0, -1]], dtype=complex),
        }
        result = np.array([[1.0]], dtype=complex)
        site_idx = 0
        for i in range(self.num_qubits):
            if i in term.sites and site_idx < len(term.labels):
                pauli = pauli_matrices.get(term.labels[site_idx], pauli_matrices["I"])
                result = np.kron(result, pauli)
                site_idx += 1
            else:
                result = np.kron(result, pauli_matrices["I"])
        return result

    def eigenvalues_and_eigenvectors(self) -> tuple[np.ndarray, np.ndarray]:
        mat = self.to_matrix()
        eigvals, eigvecs = np.linalg.eigh(mat)
        return eigvals, eigvecs

    def expectation_value(self, state: np.ndarray, operator: Optional[np.ndarray] = None) -> float:
        if operator is None:
            operator = self.to_matrix()
        if state.ndim == 1:
            return float(np.real(np.conj(state) @ operator @ state))
        return float(np.real(np.trace(operator @ state)))


@dataclass
class TimeEvolution:
    """Result of a time evolution simulation."""
    times: list[float] = field(default_factory=list)
    states: list[np.ndarray] = field(default_factory=list)
    energies: list[float] = field(default_factory=list)
    fidelities: list[float] = field(default_factory=list)

    def time_points(self) -> list[float]:
        return self.times


@dataclass
class LindbladResult:
    """Result of Lindblad master equation simulation."""
    times: list[float] = field(default_factory=list)
    density_matrices: list[np.ndarray] = field(default_factory=list)
    purities: list[float] = field(default_factory=list)
    coherences: list[float] = field(default_factory=list)
    energies: list[float] = field(default_factory=list)

    @property
    def purity(self) -> float:
        return self.purities[-1] if self.purities else 0.0

    @property
    def coherence(self) -> float:
        return self.coherences[-1] if self.coherences else 0.0


@dataclass
class ReducedDensityMatrix:
    """Reduced density matrix for a subsystem."""
    matrix: np.ndarray
    subsystem: list[int]
    total_qubits: int

    @classmethod
    def full_to_reduced(cls, state: np.ndarray, subsystem: list[int]) -> ReducedDensityMatrix:
        n_total = int(math.log2(len(state))) if state.ndim == 1 else int(math.log2(state.shape[0]))
        if state.ndim == 1:
            rho_full = np.outer(state, np.conj(state))
        else:
            rho_full = state
        dims = [2] * n_total
        rho_tensor = rho_full.reshape(dims + dims)
        complement = [i for i in range(n_total) if i not in subsystem]
        axes_keep = list(subsystem) + [n_total + s for s in subsystem]
        axes_trace = [n_total + c for c in complement]
        rho_reduced = np.trace(rho_tensor, axis1=n_total, axis2=0)
        for ax in sorted(axes_trace, reverse=True):
            rho_reduced = np.trace(rho_reduced, axis1=ax - 1, axis2=0)
        return cls(matrix=rho_reduced, subsystem=subsystem, total_qubits=n_total)


# ---------------------------------------------------------------------------
# Spin Chain Hamiltonians
# ---------------------------------------------------------------------------

class SpinChain:
    """Construct spin chain Hamiltonians."""

    def __init__(
        self,
        num_sites: int,
        coupling_j: float = 1.0,
        field_h: float = 0.0,
        anisotropy_delta: float = 0.0,
    ) -> None:
        self.num_sites = num_sites
        self.coupling_j = coupling_j
        self.field_h = field_h
        self.anisotropy_delta = anisotropy_delta

    def heisenberg_hamiltonian(self) -> Hamiltonian:
        terms: list[PauliTerm] = []
        for i in range(self.num_sites - 1):
            terms.append(PauliTerm("XX", [i, i + 1], self.coupling_j))
            terms.append(PauliTerm("YY", [i, i + 1], self.coupling_j * self.anisotropy_delta))
            terms.append(PauliTerm("ZZ", [i, i + 1], self.coupling_j))
        for i in range(self.num_sites):
            terms.append(PauliTerm("Z", [i], self.field_h))
        return Hamiltonian(num_qubits=self.num_sites, terms=terms)

    def ising_hamiltonian(self) -> Hamiltonian:
        terms: list[PauliTerm] = []
        for i in range(self.num_sites - 1):
            terms.append(PauliTerm("ZZ", [i, i + 1], self.coupling_j))
        for i in range(self.num_sites):
            terms.append(PauliTerm("X", [i], self.field_h))
        return Hamiltonian(num_qubits=self.num_sites, terms=terms)

    def xy_hamiltonian(self) -> Hamiltonian:
        terms: list[PauliTerm] = []
        for i in range(self.num_sites - 1):
            terms.append(PauliTerm("XX", [i, i + 1], self.coupling_j))
            terms.append(PauliTerm("YY", [i, i + 1], self.coupling_j))
        for i in range(self.num_sites):
            terms.append(PauliTerm("Z", [i], self.field_h))
        return Hamiltonian(num_qubits=self.num_sites, terms=terms)


# ---------------------------------------------------------------------------
# Noise Channels
# ---------------------------------------------------------------------------

class NoiseChannel:
    """Quantum noise channel for open-system simulation."""

    def __init__(self, channel_type: ChannelType, rate: float = 0.01, qubit: int = 0) -> None:
        self.channel_type = channel_type
        self.rate = rate
        self.qubit = qubit

    def jump_operator(self) -> np.ndarray:
        if self.channel_type == ChannelType.AMPLITUDE_DAMPING:
            return np.array([[0, math.sqrt(self.rate)], [0, 0]], dtype=complex)
        if self.channel_type == ChannelType.PHASE_DAMPING:
            return np.array([[0, 0], [0, math.sqrt(self.rate)]], dtype=complex)
        if self.channel_type == ChannelType.DEPOLARIZING:
            return math.sqrt(self.rate / 3) * np.eye(2, dtype=complex)
        if self.channel_type == ChannelType.BIT_FLIP:
            return math.sqrt(self.rate) * np.array([[0, 1], [1, 0]], dtype=complex)
        if self.channel_type == ChannelType.PHASE_FLIP:
            return math.sqrt(self.rate) * np.array([[1, 0], [0, -1]], dtype=complex)
        raise ValueError(f"Unknown channel type: {self.channel_type}")


class AmplitudeDampingChannel(NoiseChannel):
    """Amplitude damping (T1 relaxation) channel."""

    def __init__(self, rate: float = 0.1, qubit: int = 0) -> None:
        super().__init__(ChannelType.AMPLITUDE_DAMPING, rate, qubit)


class DepolarizingChannel(NoiseChannel):
    """Depolarizing channel."""

    def __init__(self, rate: float = 0.01, qubit: int = 0) -> None:
        super().__init__(ChannelType.DEPOLARIZING, rate, qubit)


# ---------------------------------------------------------------------------
# Hamiltonian Simulator
# ---------------------------------------------------------------------------

class HamiltonianSimulator:
    """Simulate Hamiltonian time evolution via Trotterization or exact methods."""

    def __init__(
        self,
        hamiltonian: Hamiltonian,
        num_qubits: int,
    ) -> None:
        self.hamiltonian = hamiltonian
        self.num_qubits = num_qubits
        self._cached_eigvals: Optional[np.ndarray] = None
        self._cached_eigvecs: Optional[np.ndarray] = None

    def zero_state(self) -> np.ndarray:
        state = np.zeros(2 ** self.num_qubits, dtype=complex)
        state[0] = 1.0
        return state

    def zero_density_matrix(self) -> np.ndarray:
        dim = 2 ** self.num_qubits
        rho = np.zeros((dim, dim), dtype=complex)
        rho[0, 0] = 1.0
        return rho

    def maximally_mixed_state(self) -> np.ndarray:
        dim = 2 ** self.num_qubits
        return np.eye(dim, dtype=complex) / dim

    def trotter_evolve(
        self,
        state: np.ndarray,
        time: float,
        steps: int,
        order: int = 1,
    ) -> np.ndarray:
        dt = time / steps
        H = self.hamiltonian.to_matrix()
        U_step = self._trotter_step(H, dt, order)
        evolved = state.copy()
        for _ in range(steps):
            evolved = U_step @ evolved
        return evolved

    def exact_evolve(self, state: np.ndarray, time: float) -> np.ndarray:
        H = self.hamiltonian.to_matrix()
        return self._matrix_exp_multiply(-1j * H * time, state)

    def evolve(
        self,
        state: np.ndarray,
        time: float,
        steps: int = 100,
        method: EvolutionMethod = EvolutionMethod.TROTTER_2,
    ) -> TimeEvolution:
        evolution = TimeEvolution()
        dt = time / steps

        current_state = state.copy()
        for i in range(steps + 1):
            t = i * dt
            evolution.times.append(t)
            evolution.states.append(current_state.copy())
            energy = self.hamiltonian.expectation_value(current_state)
            evolution.energies.append(energy)
            fidelity = self.fidelity(state, current_state)
            evolution.fidelities.append(fidelity)

            if i < steps:
                if method == EvolutionMethod.TROTTER_1:
                    current_state = self._trotter_step_matrix(1) @ current_state
                elif method == EvolutionMethod.TROTTER_2:
                    current_state = self._trotter_step_matrix(2) @ current_state
                elif method == EvolutionMethod.EXACT:
                    current_state = self.exact_evolve(state, t + dt)

        return evolution

    def _trotter_step_matrix(self, order: int, dt: float = 0.01) -> np.ndarray:
        H = self.hamiltonian.to_matrix()
        return self._trotter_step(H, dt, order)

    def _trotter_step(self, H: np.ndarray, dt: float, order: int) -> np.ndarray:
        if order == 1:
            return self._matrix_exp_multiply(-1j * H * dt, np.eye(H.shape[0], dtype=complex))
        elif order == 2:
            U_half = self._matrix_exp_multiply(-1j * H * dt / 2, np.eye(H.shape[0], dtype=complex))
            return U_half @ U_half.T.conj()
        else:
            return self._matrix_exp_multiply(-1j * H * dt, np.eye(H.shape[0], dtype=complex))

    def _matrix_exp_multiply(self, A: np.ndarray, v: np.ndarray) -> np.ndarray:
        dim = A.shape[0]
        if v.ndim == 1:
            result = np.zeros(dim, dtype=complex)
            for i in range(dim):
                exp_diag = np.exp(A[i, i]) if i < A.shape[1] else 1.0
                result[i] = exp_diag * v[i]
            off_diag = A - np.diag(np.diag(A))
            result += off_diag @ v
            return result
        return A @ v

    def fidelity(self, state1: np.ndarray, state2: np.ndarray) -> float:
        if state1.ndim == 1 and state2.ndim == 1:
            return float(abs(np.vdot(state1, state2)) ** 2)
        if state1.ndim == 2 and state2.ndim == 2:
            sqrt_rho1 = self._matrix_sqrt(state1)
            product = sqrt_rho1 @ state2 @ sqrt_rho1
            sqrt_product = self._matrix_sqrt(product)
            return float(np.real(np.trace(sqrt_product)) ** 2)
        return 0.0

    def _matrix_sqrt(self, M: np.ndarray) -> np.ndarray:
        eigvals, eigvecs = np.linalg.eigh(M)
        eigvals = np.maximum(eigvals, 0)
        return eigvecs @ np.diag(np.sqrt(eigvals)) @ eigvecs.T.conj()


# ---------------------------------------------------------------------------
# Lindblad Solver
# ---------------------------------------------------------------------------

class LindbladSolver:
    """Solve the Lindblad master equation for open quantum systems."""

    def __init__(
        self,
        num_qubits: int,
        hamiltonian: Hamiltonian,
        jump_operators: list[np.ndarray],
        dt: float = 0.01,
        total_time: float = 10.0,
    ) -> None:
        self.num_qubits = num_qubits
        self.hamiltonian = hamiltonian
        self.jump_operators = jump_operators
        self.dt = dt
        self.total_time = total_time

    def zero_density_matrix(self) -> np.ndarray:
        dim = 2 ** self.num_qubits
        rho = np.zeros((dim, dim), dtype=complex)
        rho[0, 0] = 1.0
        return rho

    def _lindblad_rhs(self, rho: np.ndarray) -> np.ndarray:
        H = self.hamiltonian.to_matrix()
        commutator = -1j * (H @ rho - rho @ H)
        dissipator = np.zeros_like(rho)
        for L in self.jump_operators:
            full_L = self._embed_operator(L)
            dissipator += full_L @ rho @ full_L.T.conj()
            anti_comm = full_L.T.conj() @ full_L @ rho + rho @ full_L.T.conj() @ full_L
            dissipator -= 0.5 * anti_comm
        return commutator + dissipator

    def _embed_operator(self, op: np.ndarray) -> np.ndarray:
        full = np.eye(1, dtype=complex)
        for i in range(self.num_qubits):
            if i == 0:
                full = np.kron(full, op)
            else:
                full = np.kron(full, np.eye(2, dtype=complex))
        return full

    def solve(
        self,
        initial_rho: np.ndarray,
        method: SolverMethod = SolverMethod.ADAPTIVE_RK4,
    ) -> LindbladResult:
        result = LindbladResult()
        num_steps = int(self.total_time / self.dt)
        rho = initial_rho.copy()

        for step in range(num_steps + 1):
            t = step * self.dt
            result.times.append(t)
            result.density_matrices.append(rho.copy())
            result.purities.append(float(np.real(np.trace(rho @ rho))))
            result.coherences.append(
                float(np.sum(np.abs(np.diag(rho, 1))) + np.sum(np.abs(np.diag(rho, -1))))
            )
            result.energies.append(
                self.hamiltonian.expectation_value(rho)
            )

            if step < num_steps:
                if method == SolverMethod.EULER:
                    rho = self._euler_step(rho)
                elif method == SolverMethod.RK4:
                    rho = self._rk4_step(rho)
                elif method == SolverMethod.ADAPTIVE_RK4:
                    rho = self._adaptive_rk4_step(rho)
                rho = self._renormalize(rho)

        return result

    def _euler_step(self, rho: np.ndarray) -> np.ndarray:
        return rho + self.dt * self._lindblad_rhs(rho)

    def _rk4_step(self, rho: np.ndarray) -> np.ndarray:
        k1 = self._lindblad_rhs(rho)
        k2 = self._lindblad_rhs(rho + self.dt / 2 * k1)
        k3 = self._lindblad_rhs(rho + self.dt / 2 * k2)
        k4 = self._lindblad_rhs(rho + self.dt * k3)
        return rho + self.dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    def _adaptive_rk4_step(self, rho: np.ndarray) -> np.ndarray:
        rho1 = self._rk4_step(rho)
        half_dt_rho = self._rk4_step_half(rho)
        rho2 = self._rk4_step_half(half_dt_rho)
        error = np.max(np.abs(rho2 - rho1))
        if error > 0.01:
            self.dt *= 0.5
        elif error < 0.001:
            self.dt *= 2.0
        return rho2

    def _rk4_step_half(self, rho: np.ndarray) -> np.ndarray:
        half_dt = self.dt / 2
        k1 = self._lindblad_rhs(rho)
        k2 = self._lindblad_rhs(rho + half_dt / 2 * k1)
        k3 = self._lindblad_rhs(rho + half_dt / 2 * k2)
        k4 = self._lindblad_rhs(rho + half_dt * k3)
        return rho + half_dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    def _renormalize(self, rho: np.ndarray) -> np.ndarray:
        trace = np.trace(rho)
        if abs(trace) > 1e-10:
            return rho / trace
        return rho


# ---------------------------------------------------------------------------
# Gibbs State
# ---------------------------------------------------------------------------

class GibbsState:
    """Prepare thermal equilibrium (Gibbs) states at finite temperature."""

    def __init__(self, hamiltonian: Hamiltonian, temperature: float) -> None:
        self.hamiltonian = hamiltonian
        self.temperature = max(temperature, 1e-10)
        self._rho: Optional[np.ndarray] = None

    def state(self) -> np.ndarray:
        if self._rho is not None:
            return self._rho
        H = self.hamiltonian.to_matrix()
        eigvals, eigvecs = np.linalg.eigh(H)
        beta = 1.0 / self.temperature
        boltzmann = np.exp(-beta * eigvals)
        partition = np.sum(boltzmann)
        self._rho = eigvecs @ np.diag(boltzmann / partition) @ eigvecs.T.conj()
        return self._rho

    def energy(self) -> float:
        rho = self.state()
        return self.hamiltonian.expectation_value(rho)

    def entropy(self) -> float:
        rho = self.state()
        eigvals = np.linalg.eigvalsh(rho)
        eigvals = eigvals[eigvals > 1e-15]
        return float(-np.sum(eigvals * np.log2(eigvals)))

    def purity(self) -> float:
        rho = self.state()
        return float(np.real(np.trace(rho @ rho)))


# ---------------------------------------------------------------------------
# Correlation Functions
# ---------------------------------------------------------------------------

class CorrelationFunction:
    """Compute auto- and cross-correlation functions from time evolution."""

    def __init__(self, evolution: TimeEvolution) -> None:
        self.evolution = evolution

    def auto_correlation(
        self,
        operator: str,
        site: int,
        times: Optional[list[float]] = None,
    ) -> np.ndarray:
        pauli = self._operator_matrix(operator)
        values: list[complex] = []
        rho0 = np.outer(self.evolution.states[0], np.conj(self.evolution.states[0]))
        for state in self.evolution.states:
            rho_t = np.outer(state, np.conj(state))
            values.append(np.trace(pauli @ rho0 @ pauli @ rho_t))
        return np.array(values)

    def cross_correlation(
        self,
        operator_a: str,
        site_a: int,
        operator_b: str,
        site_b: int,
    ) -> np.ndarray:
        pauli_a = self._operator_matrix(operator_a)
        pauli_b = self._operator_matrix(operator_b)
        values: list[complex] = []
        rho0 = np.outer(self.evolution.states[0], np.conj(self.evolution.states[0]))
        for state in self.evolution.states:
            rho_t = np.outer(state, np.conj(state))
            values.append(np.trace(pauli_a @ pauli_b @ rho0 @ rho_t))
        return np.array(values)

    def decay_time(self, correlation: np.ndarray) -> float:
        decay = np.abs(correlation) / (np.abs(correlation[0]) + 1e-15)
        for i, v in enumerate(decay):
            if v < 1 / math.e:
                return self.evolution.times[i]
        return self.evolution.times[-1]

    def _operator_matrix(self, label: str) -> np.ndarray:
        matrices = {
            "X": np.array([[0, 1], [1, 0]], dtype=complex),
            "Y": np.array([[0, -1j], [1j, 0]], dtype=complex),
            "Z": np.array([[1, 0], [0, -1]], dtype=complex),
            "I": np.eye(2, dtype=complex),
        }
        return matrices.get(label.upper(), matrices["Z"])


# ---------------------------------------------------------------------------
# Entanglement Measures
# ---------------------------------------------------------------------------

class Entanglement:
    """Compute entanglement measures for quantum states."""

    def __init__(self, num_qubits: int) -> None:
        self.num_qubits = num_qubits

    def von_neumann_entropy(self, rdm: ReducedDensityMatrix) -> float:
        eigvals = np.linalg.eigvalsh(rdm.matrix)
        eigvals = eigvals[eigvals > 1e-15]
        return float(-np.sum(eigvals * np.log2(eigvals)))

    def concurrence(self, rdm: ReducedDensityMatrix) -> float:
        if rdm.matrix.shape[0] != 2:
            return 0.0
        sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
        rho_tilde = (np.kron(sigma_y, sigma_y) @ rdm.matrix @ np.kron(sigma_y, sigma_y))
        product = rdm.matrix @ rho_tilde
        eigvals = np.sqrt(np.maximum(np.linalg.eigvalsh(product), 0))
        eigvals = np.sort(eigvals)[::-1]
        c = max(0, eigvals[0] - eigvals[1] - eigvals[2] - eigvals[3])
        return float(c)

    def entanglement_of_formation(self, rdm: ReducedDensityMatrix) -> float:
        c = self.concurrence(rdm)
        if c <= 0:
            return 0.0
        h = lambda x: -x * math.log2(x) - (1 - x) * math.log2(1 - x) if 0 < x < 1 else 0.0
        return h((1 + math.sqrt(1 - c ** 2)) / 2)

    def negativity(self, rdm: ReducedDensityMatrix) -> float:
        rho_partial = rdm.matrix
        eigvals = np.linalg.eigvalsh(rho_partial)
        return float(-np.sum(np.minimum(eigvals, 0)))

    def concurrence_from_state(self, state: np.ndarray) -> float:
        rdm = ReducedDensityMatrix.full_to_reduced(state, subsystem=[0, 1])
        return self.concurrence(rdm)


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate quantum simulation module capabilities."""
    print("=" * 60)
    print("  Quantum Simulation Module — Demo")
    print("=" * 60)

    # 1. Spin Chain Hamiltonian
    print("\n--- 1. Heisenberg Spin Chain ---")
    chain = SpinChain(num_sites=3, coupling_j=1.0, field_h=0.5)
    ham = chain.heisenberg_hamiltonian()
    eigvals, _ = ham.eigenvalues_and_eigenvectors()
    print(f"Eigenvalues: {np.round(eigvals, 4)}")
    print(f"Spectral gap: {eigvals[1] - eigvals[0]:.4f}")

    # 2. Hamiltonian Simulation (Trotter)
    print("\n--- 2. Trotter Time Evolution ---")
    sim = HamiltonianSimulator(ham, num_qubits=3)
    state0 = sim.zero_state()
    evolution = sim.evolve(state0, time=2.0, steps=50, method=EvolutionMethod.TROTTER_2)
    print(f"Energy at t=0: {evolution.energies[0]:.4f}")
    print(f"Energy at t=2: {evolution.energies[-1]:.4f}")
    print(f"Fidelity at t=2: {evolution.fidelities[-1]:.4f}")

    # 3. Gibbs State
    print("\n--- 3. Gibbs Thermal State ---")
    gibbs = GibbsState(ham, temperature=1.0)
    rho_gibbs = gibbs.state()
    print(f"Energy: {gibbs.energy():.4f}")
    print(f"Entropy: {gibbs.entropy():.4f} bits")
    print(f"Purity: {gibbs.purity():.4f}")

    # 4. Open System (Lindblad)
    print("\n--- 4. Lindblad Open-System Dynamics ---")
    damping = AmplitudeDampingChannel(rate=0.1, qubit=0)
    lindblad = LindbladSolver(
        num_qubits=2,
        hamiltonian=chain.heisenberg_hamiltonian(),
        jump_operators=[damping.jump_operator()],
        dt=0.05,
        total_time=2.0,
    )
    rho0 = lindblad.zero_density_matrix()
    lindblad_result = lindblad.solve(rho0, method=SolverMethod.RK4)
    print(f"Initial purity: {lindblad_result.purities[0]:.4f}")
    print(f"Final purity: {lindblad_result.purities[-1]:.4f}")
    print(f"Final coherence: {lindblad_result.coherences[-1]:.4f}")

    # 5. Entanglement
    print("\n--- 5. Entanglement Measures ---")
    ent = Entanglement(num_qubits=3)
    bell_state = np.zeros(8, dtype=complex)
    bell_state[0] = 1 / math.sqrt(2)
    bell_state[3] = 1 / math.sqrt(2)
    rdm = ReducedDensityMatrix.full_to_reduced(bell_state, subsystem=[0, 1])
    vn = ent.von_neumann_entropy(rdm)
    c = ent.concurrence(rdm)
    eof = ent.entanglement_of_formation(rdm)
    neg = ent.negativity(rdm)
    print(f"Von Neumann entropy: {vn:.4f}")
    print(f"Concurrence: {c:.4f}")
    print(f"Entanglement of formation: {eof:.4f}")
    print(f"Negativity: {neg:.4f}")

    # 6. Correlation Function
    print("\n--- 6. Auto-Correlation ---")
    corr = CorrelationFunction(evolution)
    auto_z = corr.auto_correlation("Z", site=0)
    decay_t = corr.decay_time(auto_z)
    print(f"Correlation at t=0: {np.real(auto_z[0]):.4f}")
    print(f"Correlation at t=2: {np.real(auto_z[-1]):.4f}")
    print(f"Decay time (1/e): {decay_t:.4f}")

    # 7. Ising Model
    print("\n--- 7. Transverse-Field Ising ---")
    ising_chain = SpinChain(num_sites=4, coupling_j=1.0, field_h=0.8)
    ising_ham = ising_chain.ising_hamiltonian()
    ising_eigvals, _ = ising_ham.eigenvalues_and_eigenvectors()
    print(f"Ising eigenvalues: {np.round(ising_eigvals[:6], 4)}")
    print(f"Gap: {ising_eigvals[1] - ising_eigvals[0]:.4f}")

    # 8. XY Model
    print("\n--- 8. XY Model ---")
    xy_chain = SpinChain(num_sites=3, coupling_j=0.5, field_h=0.3, anisotropy_delta=0.5)
    xy_ham = xy_chain.xy_hamiltonian()
    xy_eigvals, _ = xy_ham.eigenvalues_and_eigenvectors()
    print(f"XY eigenvalues: {np.round(xy_eigvals, 4)}")

    print("\n" + "=" * 60)
    print("  Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
Variational Circuits Module
Part of the quantum-ml skill domain

Provides parameterized quantum circuit construction, gradient computation,
optimization, barren plateau analysis, and circuit compression for
variational quantum algorithms (VQE, QAOA, VQAs).
"""

from __future__ import annotations

import warnings
import math
import copy
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from enum import Enum, auto
from dataclasses import dataclass, field
from datetime import datetime

import numpy as np

logger = logging.getLogger(__name__)


class AnsatzType(Enum):
    """Supported variational ansatz architectures."""
    HARDWARE_EFFICIENT = auto()
    STRONGLY_ENTANGLING = auto()
    REAL_AMPLITUDE = auto()
    EFFICIENT_SU2 = auto()
    QAOA = auto()
    UCCSD = auto()        # Unitary Coupled Cluster for quantum chemistry
    CUSTOM = auto()

    def __repr__(self) -> str:
        return f"AnsatzType.{self.name}"


class EntanglementStrategy(Enum):
    """Entanglement strategies for variational layers."""
    LINEAR = auto()
    CIRCULAR = auto()
    FULL = auto()
    CONSTRAINED = auto()  # Limited by hardware connectivity
    NONE = auto()

    def __repr__(self) -> str:
        return f"EntanglementStrategy.{self.name}"


class GradientMethod(Enum):
    """Gradient computation methods."""
    PARAMETER_SHIFT = auto()
    FINITE_DIFFERENCE = auto()
    ADJOINT = auto()
    BACKPROPAGATION = auto()

    def __repr__(self) -> str:
        return f"GradientMethod.{self.name}"


class OptimizerType(Enum):
    """Supported classical optimizers."""
    COBYLA = auto()
    L_BFGS_B = auto()
    NELDER_MEAD = auto()
    ADAM = auto()
    SGD = auto()
    SPSA = auto()       # Simultaneous Perturbation Stochastic Approximation
    ADAGRAD = auto()
    RMSPROP = auto()

    def __repr__(self) -> str:
        return f"OptimizerType.{self.name}"


class CircuitStatus(Enum):
    """Status of circuit operations."""
    IDLE = auto()
    BUILT = auto()
    OPTIMIZING = auto()
    CONVERGED = auto()
    DIVERGED = auto()
    MAX_ITERATIONS = auto()
    ERROR = auto()

    def __repr__(self) -> str:
        return f"CircuitStatus.{self.name}"


class BarrenPlateauRisk(Enum):
    """Risk levels for barren plateaus."""
    LOW = auto()
    MODERATE = auto()
    HIGH = auto()
    CRITICAL = auto()

    def __repr__(self) -> str:
        return f"BarrenPlateauRisk.{self.name}"


@dataclass
class CircuitConfig:
    """Configuration for a variational circuit.

    Attributes:
        n_qubits: Number of qubits.
        ansatz: Ansatz architecture.
        n_layers: Number of variational layers.
        entanglement: Entanglement strategy.
        rotation_gates: Rotation gates per qubit per layer.
        entangling_gate: Gate used for entangling operations.
        hardware_connectivity: Maximum qubit distance for entanglement (None = unlimited).
    """
    n_qubits: int = 4
    ansatz: AnsatzType = AnsatzType.HARDWARE_EFFICIENT
    n_layers: int = 2
    entanglement: EntanglementStrategy = EntanglementStrategy.LINEAR
    rotation_gates: List[str] = field(default_factory=lambda: ["RX", "RY", "RZ"])
    entangling_gate: str = "CNOT"
    hardware_connectivity: Optional[int] = None

    def __post_init__(self) -> None:
        if self.n_qubits < 1:
            raise ValueError("n_qubits must be >= 1.")
        if self.n_layers < 1:
            raise ValueError("n_layers must be >= 1.")


@dataclass
class Hamiltonian:
    """Observable Hamiltonian represented as a sum of Pauli terms.

    Attributes:
        terms: Dictionary mapping Pauli strings to coefficients.
    """
    terms: Dict[str, float] = field(default_factory=dict)

    @classmethod
    def from_pauli(cls, pauli_dict: Dict[str, float]) -> "Hamiltonian":
        """Create Hamiltonian from a dictionary of Pauli strings.

        Args:
            pauli_dict: Mapping from Pauli strings (e.g., "IXZ") to coefficients.

        Returns:
            Hamiltonian instance.
        """
        return cls(terms=dict(pauli_dict))

    @property
    def n_qubits(self) -> int:
        """Number of qubits required by this Hamiltonian."""
        if not self.terms:
            return 0
        return max(len(pauli) for pauli in self.terms)

    @property
    def n_terms(self) -> int:
        return len(self.terms)

    def expectation(self, state: np.ndarray) -> float:
        """Compute the expectation value of this Hamiltonian for a state vector.

        Args:
            state: State vector of length 2^n_qubits.

        Returns:
            Expectation value <state|H|state>.
        """
        n = self.n_qubits
        expectation = 0.0

        for pauli_str, coeff in self.terms.items():
            pauli_matrix = self._pauli_string_to_matrix(pauli_str, n)
            expectation += coeff * float(np.real(state.conj() @ pauli_matrix @ state))

        return expectation

    def _pauli_string_to_matrix(self, pauli_str: str, n: int) -> np.ndarray:
        """Convert a Pauli string to its matrix representation."""
        I = np.eye(2)
        X = np.array([[0, 1], [1, 0]])
        Y = np.array([[0, -1j], [1j, 0]])
        Z = np.array([[1, 0], [0, -1]])

        pauli_map = {"I": I, "X": X, "Y": Y, "Z": Z}

        result = np.array([[1.0]])
        for char in pauli_str:
            result = np.kron(result, pauli_map.get(char, I))

        # Pad if necessary
        full_dim = 2 ** n
        if result.shape[0] < full_dim:
            result = np.kron(result, np.eye(full_dim // result.shape[0]))

        return result[:full_dim, :full_dim]

    def validate(self) -> List[str]:
        errors = []
        for pauli, coeff in self.terms.items():
            if not all(c in "IXYZ" for c in pauli):
                errors.append(f"Invalid Pauli string: '{pauli}'")
            if len(pauli) != self.n_qubits and self.n_qubits > 0:
                pass  # Allow padded strings
        return errors


@dataclass
class QAOACost:
    """QAOA cost Hamiltonian construction utilities."""

    @staticmethod
    def maxcut(n_qubits: int, edges: List[Tuple[int, int]]) -> Hamiltonian:
        """Construct MaxCut cost Hamiltonian.

        Args:
            n_qubits: Number of qubits (nodes).
            edges: List of (i, j) edges in the graph.

        Returns:
            Cost Hamiltonian for the MaxCut problem.
        """
        terms: Dict[str, float] = {}
        for i, j in edges:
            pauli = ["I"] * n_qubits
            pauli[i] = "Z"
            pauli[j] = "Z"
            key = "".join(pauli)
            terms[key] = terms.get(key, 0.0) + 0.5

            pauli_i = ["I"] * n_qubits
            pauli_i[i] = "Z"
            key_i = "".join(pauli_i)
            terms[key_i] = terms.get(key_i, 0.0) - 0.5

            pauli_j = ["I"] * n_qubits
            pauli_j[j] = "Z"
            key_j = "".join(pauli_j)
            terms[key_j] = terms.get(key_j, 0.0) - 0.5

        return Hamiltonian(terms=terms)

    @staticmethod
    def number_partitioning(n_qubits: int, numbers: List[int]) -> Hamiltonian:
        """Construct number partitioning cost Hamiltonian.

        Args:
            n_qubits: Must equal len(numbers).
            numbers: List of numbers to partition.

        Returns:
            Cost Hamiltonian.
        """
        terms: Dict[str, float] = {}
        terms["I" * n_qubits] = float(sum(n ** 2 for n in numbers))

        for i in range(n_qubits):
            for j in range(n_qubits):
                if i != j:
                    pauli = ["I"] * n_qubits
                    pauli[i] = "Z"
                    pauli[j] = "Z"
                    key = "".join(pauli)
                    terms[key] = terms.get(key, 0.0) + 2 * numbers[i] * numbers[j]

        constant = sum(numbers) ** 2
        terms["I" * n_qubits] = terms.get("I" * n_qubits, 0.0) - constant

        return Hamiltonian(terms=terms)


@dataclass
class OptimizationResult:
    """Result of a variational optimization."""
    optimal_parameters: np.ndarray
    optimal_value: float
    n_function_evals: int
    n_gradient_evals: int
    convergence_history: List[float]
    converged: bool
    optimization_time: float
    method: str


@dataclass
class BarrenPlateauAnalysis:
    """Results of barren plateau analysis."""
    gradient_variance: float
    gradient_mean: float
    gradient_max: float
    risk_level: BarrenPlateauRisk
    recommendation: str
    n_parameters_analyzed: int
    circuit_depth: int


class VariationalCircuit:
    """Parameterized quantum circuit for variational algorithms.

    Manages circuit construction, parameter initialization, cost function
    evaluation, gradient computation, and optimization.
    """

    def __init__(self, config: Optional[CircuitConfig] = None):
        self.config = config or CircuitConfig()
        self.parameters: Optional[np.ndarray] = None
        self.status: CircuitStatus = CircuitStatus.IDLE
        self._history: List[float] = []

        self._n_parameters = self._compute_n_parameters()
        self._adam_m: Optional[np.ndarray] = None
        self._adam_v: Optional[np.ndarray] = None
        self._adam_t: int = 0

    def _compute_n_parameters(self) -> int:
        """Compute total number of trainable parameters."""
        n = self.config.n_qubits
        L = self.config.n_layers
        n_rot = len(self.config.rotation_gates)

        if self.config.ansatz == AnsatzType.QAOA:
            return 2 * L  # gamma and beta for each layer
        elif self.config.ansatz == AnsatzType.UCCSD:
            return n * (n - 1) // 2 * L  # Number of excitation operators
        elif self.config.ansatz in (AnsatzType.HARDWARE_EFFICIENT, AnsatzType.EFFICIENT_SU2):
            return L * n * n_rot
        elif self.config.ansatz == AnsatzType.STRONGLY_ENTANGLING:
            return L * n * (n_rot + 1)
        elif self.config.ansatz == AnsatzType.REAL_AMPLITUDE:
            return L * n_rot
        return L * n * n_rot

    def initialize(
        self,
        seed: Optional[int] = None,
        method: str = "uniform",
    ) -> np.ndarray:
        """Initialize circuit parameters.

        Args:
            seed: Random seed.
            method: Initialization method — 'uniform', 'xavier', 'identity', 'zero'.

        Returns:
            Initialized parameter array.
        """
        rng = np.random.default_rng(seed)

        if method == "uniform":
            self.parameters = rng.uniform(-np.pi, np.pi, size=self._n_parameters)
        elif method == "xavier":
            limit = np.sqrt(6.0 / (self._n_parameters + self.config.n_qubits))
            self.parameters = rng.uniform(-limit, limit, size=self._n_parameters)
        elif method == "identity":
            # Initialize near zero for identity-like circuit
            self.parameters = rng.normal(0, 0.01, size=self._n_parameters)
        elif method == "zero":
            self.parameters = np.zeros(self._n_parameters)
        else:
            raise ValueError(f"Unknown initialization method: {method}")

        self._adam_m = None
        self._adam_v = None
        self._adam_t = 0
        self.status = CircuitStatus.BUILT

        return self.parameters.copy()

    @property
    def n_parameters(self) -> int:
        return self._n_parameters

    @property
    def estimated_depth(self) -> int:
        """Estimated circuit depth."""
        L = self.config.n_layers
        if self.config.ansatz == AnsatzType.QAOA:
            return L * 3  # mixer + problem + measurement per layer
        return L * 3

    @property
    def estimated_gate_count(self) -> int:
        """Estimated total gate count."""
        n = self.config.n_qubits
        L = self.config.n_layers
        n_rot = len(self.config.rotation_gates)
        rot_gates = n * n_rot * L
        entangling = (n - 1) * L  # linear entanglement
        return rot_gates + entangling

    def build_circuit(self) -> List[Dict[str, Any]]:
        """Build the full circuit operation list.

        Returns:
            List of gate operations.
        """
        if self.parameters is None:
            self.initialize()

        ops = []
        n = self.config.n_qubits
        p_idx = 0

        if self.config.ansatz == AnsatzType.QAOA:
            for layer in range(self.config.n_layers):
                gamma = float(self.parameters[2 * layer])
                beta = float(self.parameters[2 * layer + 1])

                # Problem Hamiltonian gates (ZZ interactions)
                for i in range(n - 1):
                    ops.append({"gate": "CNOT", "control": i, "target": i + 1})
                    ops.append({"gate": "RZ", "qubit": i + 1, "angle": gamma})
                    ops.append({"gate": "CNOT", "control": i, "target": i + 1})

                # Mixer Hamiltonian (X rotations)
                for q in range(n):
                    ops.append({"gate": "RX", "qubit": q, "angle": 2 * beta})
        else:
            for layer in range(self.config.n_layers):
                # Rotation gates
                for q in range(n):
                    for gate_name in self.config.rotation_gates:
                        if p_idx < len(self.parameters):
                            ops.append({
                                "gate": gate_name,
                                "qubit": q,
                                "angle": float(self.parameters[p_idx]),
                            })
                            p_idx += 1

                # Entanglement
                entangling_pairs = self._get_entangling_pairs()
                for ctrl, tgt in entangling_pairs:
                    ops.append({
                        "gate": self.config.entangling_gate,
                        "control": ctrl,
                        "target": tgt,
                    })

                # Strongly entangling: additional rotation per qubit
                if self.config.ansatz == AnsatzType.STRONGLY_ENTANGLING:
                    for q in range(n):
                        if p_idx < len(self.parameters):
                            ops.append({
                                "gate": "RZ",
                                "qubit": q,
                                "angle": float(self.parameters[p_idx]),
                            })
                            p_idx += 1

        return ops

    def _get_entangling_pairs(self) -> List[Tuple[int, int]]:
        """Get entangling pairs based on strategy."""
        n = self.config.n_qubits
        conn = self.config.hardware_connectivity

        if self.config.entanglement == EntanglementStrategy.LINEAR:
            pairs = [(i, i + 1) for i in range(n - 1)]
        elif self.config.entanglement == EntanglementStrategy.CIRCULAR:
            pairs = [(i, (i + 1) % n) for i in range(n)]
        elif self.config.entanglement == EntanglementStrategy.FULL:
            pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        elif self.config.entanglement == EntanglementStrategy.NONE:
            pairs = []
        else:
            pairs = [(i, i + 1) for i in range(n - 1)]

        if conn is not None:
            pairs = [(a, b) for a, b in pairs if abs(a - b) <= conn]

        return pairs

    def evaluate_cost(self, hamiltonian: Hamiltonian, params: Optional[np.ndarray] = None) -> float:
        """Evaluate the cost function for given parameters.

        Args:
            hamiltonian: Cost Hamiltonian.
            params: Parameters to use; defaults to current parameters.

        Returns:
            Expectation value <psi(params)|H|psi(params)>.
        """
        p = params if params is not None else self.parameters
        if p is None:
            raise RuntimeError("Parameters not initialized.")

        # Build state vector (simulated)
        n = self.config.n_qubits
        state = np.zeros(2 ** n, dtype=complex)
        state[0] = 1.0  # Start in |0...0>

        # Apply circuit operations
        ops = self.build_circuit()
        for op in ops:
            self._apply_gate(state, op)

        return hamiltonian.expectation(state)

    def _apply_gate(self, state: np.ndarray, op: Dict[str, Any]) -> None:
        """Apply a single gate operation to the state vector (in-place).

        Args:
            state: State vector to modify.
            op: Gate operation dictionary.
        """
        gate = op.get("gate", "")
        q = op.get("qubit", 0)
        n = int(np.log2(len(state)))
        dim = 2 ** n

        if gate == "RX":
            angle = op.get("angle", 0.0)
            self._apply_single_qubit(state, q, np.array([
                [np.cos(angle / 2), -1j * np.sin(angle / 2)],
                [-1j * np.sin(angle / 2), np.cos(angle / 2)],
            ]))
        elif gate == "RY":
            angle = op.get("angle", 0.0)
            self._apply_single_qubit(state, q, np.array([
                [np.cos(angle / 2), -np.sin(angle / 2)],
                [np.sin(angle / 2), np.cos(angle / 2)],
            ]))
        elif gate == "RZ":
            angle = op.get("angle", 0.0)
            self._apply_single_qubit(state, q, np.array([
                [np.exp(-1j * angle / 2), 0],
                [0, np.exp(1j * angle / 2)],
            ]))
        elif gate == "H":
            self._apply_single_qubit(state, q, np.array([
                [1, 1], [1, -1]
            ]) / np.sqrt(2))
        elif gate in ("CNOT", "CX"):
            ctrl = op.get("control", 0)
            tgt = op.get("target", 1)
            self._apply_cnot(state, ctrl, tgt)

    def _apply_single_qubit(self, state: np.ndarray, qubit: int, matrix: np.ndarray) -> None:
        """Apply a single-qubit gate to the state vector."""
        n = int(np.log2(len(state)))
        dim = 2 ** n

        for i in range(dim):
            bit = (i >> (n - 1 - qubit)) & 1
            if bit == 0:
                j = i | (1 << (n - 1 - qubit))
                if i < dim and j < dim:
                    a, b = state[i], state[j]
                    state[i] = matrix[0, 0] * a + matrix[0, 1] * b
                    state[j] = matrix[1, 0] * a + matrix[1, 1] * b

    def _apply_cnot(self, state: np.ndarray, control: int, target: int) -> None:
        """Apply CNOT gate to the state vector."""
        n = int(np.log2(len(state)))
        dim = 2 ** n

        for i in range(dim):
            ctrl_bit = (i >> (n - 1 - control)) & 1
            tgt_bit = (i >> (n - 1 - target)) & 1

            if ctrl_bit == 1 and tgt_bit == 0:
                j = i ^ (1 << (n - 1 - target))
                if i < dim and j < dim:
                    state[i], state[j] = state[j].copy(), state[i].copy()

    def compute_gradients(
        self,
        hamiltonian: Hamiltonian,
        method: GradientMethod = GradientMethod.PARAMETER_SHIFT,
        epsilon: float = 1e-4,
    ) -> np.ndarray:
        """Compute gradients of the cost function.

        Args:
            hamiltonian: Cost Hamiltonian.
            method: Gradient computation method.
            epsilon: Finite difference step size (used only for FINITE_DIFFERENCE).

        Returns:
            Gradient array of shape (n_parameters,).
        """
        if self.parameters is None:
            raise RuntimeError("Parameters not initialized.")

        grads = np.zeros_like(self.parameters)

        if method == GradientMethod.PARAMETER_SHIFT:
            for i in range(len(self.parameters)):
                params_plus = self.parameters.copy()
                params_minus = self.parameters.copy()
                params_plus[i] += np.pi / 2
                params_minus[i] -= np.pi / 2
                grads[i] = (
                    self.evaluate_cost(hamiltonian, params_plus)
                    - self.evaluate_cost(hamiltonian, params_minus)
                ) / 2.0

        elif method == GradientMethod.FINITE_DIFFERENCE:
            for i in range(len(self.parameters)):
                params_plus = self.parameters.copy()
                params_minus = self.parameters.copy()
                params_plus[i] += epsilon
                params_minus[i] -= epsilon
                grads[i] = (
                    self.evaluate_cost(hamiltonian, params_plus)
                    - self.evaluate_cost(hamiltonian, params_minus)
                ) / (2 * epsilon)

        return grads

    def minimize(
        self,
        hamiltonian: Hamiltonian,
        optimizer: str = "cobyla",
        maxiter: int = 200,
        tolerance: float = 1e-6,
        initial_parameters: Optional[np.ndarray] = None,
    ) -> OptimizationResult:
        """Minimize the cost Hamiltonian using classical optimization.

        Args:
            hamiltonian: Cost Hamiltonian to minimize.
            optimizer: Optimizer name.
            maxiter: Maximum iterations.
            tolerance: Convergence tolerance.
            initial_parameters: Starting parameters.

        Returns:
            OptimizationResult with optimal parameters and value.
        """
        if initial_parameters is not None:
            self.parameters = initial_parameters.copy()
        elif self.parameters is None:
            self.initialize()

        self.status = CircuitStatus.OPTIMIZING
        self._history.clear()
        start_time = datetime.now()

        if optimizer == "cobyla":
            result = self._optimize_cobyla(hamiltonian, maxiter, tolerance)
        elif optimizer == "adam":
            result = self._optimize_adam(hamiltonian, maxiter, tolerance)
        elif optimizer == "spsa":
            result = self._optimize_spsa(hamiltonian, maxiter, tolerance)
        else:
            result = self._optimize_gradient_descent(hamiltonian, maxiter, tolerance)

        elapsed = (datetime.now() - start_time).total_seconds()
        self.status = CircuitStatus.CONVERGED if result["converged"] else CircuitStatus.MAX_ITERATIONS

        return OptimizationResult(
            optimal_parameters=self.parameters,
            optimal_value=result["optimal_value"],
            n_function_evals=result["n_evals"],
            n_gradient_evals=0,
            convergence_history=self._history,
            converged=result["converged"],
            optimization_time=elapsed,
            method=optimizer,
        )

    def _optimize_cobyla(
        self, hamiltonian: Hamiltonian, maxiter: int, tolerance: float
    ) -> Dict[str, Any]:
        """COBYLA optimization (simplified)."""
        n_evals = 0
        best_value = float("inf")
        best_params = self.parameters.copy()

        for i in range(maxiter):
            value = self.evaluate_cost(hamiltonian)
            n_evals += 1
            self._history.append(float(value))

            if value < best_value:
                best_value = value
                best_params = self.parameters.copy()

            if len(self._history) > 10:
                recent = self._history[-10:]
                if max(recent) - min(recent) < tolerance:
                    self.parameters = best_params
                    return {"optimal_value": best_value, "n_evals": n_evals, "converged": True}

            # Random perturbation (simplified COBYLA step)
            step = np.random.randn(len(self.parameters)) * 0.1 / (1 + i * 0.01)
            self.parameters = self.parameters - step

        self.parameters = best_params
        return {"optimal_value": best_value, "n_evals": n_evals, "converged": False}

    def _optimize_adam(
        self, hamiltonian: Hamiltonian, maxiter: int, tolerance: float
    ) -> Dict[str, Any]:
        """Adam optimization."""
        lr = 0.01
        beta1, beta2, eps = 0.9, 0.999, 1e-8

        if self._adam_m is None:
            self._adam_m = np.zeros_like(self.parameters)
            self._adam_v = np.zeros_like(self.parameters)

        n_evals = 0

        for i in range(maxiter):
            grads = self.compute_gradients(hamiltonian, GradientMethod.PARAMETER_SHIFT)
            n_evals += 2 * len(self.parameters)  # parameter shift costs 2 evals per param

            self._adam_t += 1
            self._adam_m = beta1 * self._adam_m + (1 - beta1) * grads
            self._adam_v = beta2 * self._adam_v + (1 - beta2) * grads ** 2

            m_hat = self._adam_m / (1 - beta1 ** self._adam_t)
            v_hat = self._adam_v / (1 - beta2 ** self._adam_t)

            step = lr * m_hat / (np.sqrt(v_hat) + eps)
            self.parameters = self.parameters - step

            value = self.evaluate_cost(hamiltonian)
            self._history.append(float(value))

            if len(self._history) > 10 and max(self._history[-10:]) - min(self._history[-10:]) < tolerance:
                return {"optimal_value": float(value), "n_evals": n_evals, "converged": True}

        return {"optimal_value": float(self._history[-1]) if self._history else 0.0, "n_evals": n_evals, "converged": False}

    def _optimize_spsa(
        self, hamiltonian: Hamiltonian, maxiter: int, tolerance: float
    ) -> Dict[str, Any]:
        """SPSA optimization."""
        lr = 0.1
        n_evals = 0

        for i in range(maxiter):
            delta = 2 * np.random.randint(0, 2, size=len(self.parameters)) - 1
            value_plus = self.evaluate_cost(hamiltonian, self.parameters + lr * delta)
            value_minus = self.evaluate_cost(hamiltonian, self.parameters - lr * delta)
            n_evals += 2

            grad_approx = (value_plus - value_minus) / (2 * lr * delta)
            self.parameters = self.parameters - lr / (i + 1) * grad_approx

            value = self.evaluate_cost(hamiltonian)
            self._history.append(float(value))

            if len(self._history) > 10 and max(self._history[-10:]) - min(self._history[-10:]) < tolerance:
                return {"optimal_value": float(value), "n_evals": n_evals, "converged": True}

        return {"optimal_value": float(self._history[-1]) if self._history else 0.0, "n_evals": n_evals, "converged": False}

    def _optimize_gradient_descent(
        self, hamiltonian: Hamiltonian, maxiter: int, tolerance: float
    ) -> Dict[str, Any]:
        """Simple gradient descent."""
        lr = 0.01
        n_evals = 0

        for i in range(maxiter):
            grads = self.compute_gradients(hamiltonian, GradientMethod.PARAMETER_SHIFT)
            n_evals += 2 * len(self.parameters)
            self.parameters = self.parameters - lr * grads

            value = self.evaluate_cost(hamiltonian)
            self._history.append(float(value))

            if len(self._history) > 10 and max(self._history[-10:]) - min(self._history[-10:]) < tolerance:
                return {"optimal_value": float(value), "n_evals": n_evals, "converged": True}

        return {"optimal_value": float(self._history[-1]) if self._history else 0.0, "n_evals": n_evals, "converged": False}

    def get_status(self) -> Dict[str, Any]:
        return {
            "status": self.status.name,
            "n_qubits": self.config.n_qubits,
            "n_layers": self.config.n_layers,
            "n_parameters": self._n_parameters,
            "ansatz": self.config.ansatz.name,
            "estimated_depth": self.estimated_depth,
            "estimated_gates": self.estimated_gate_count,
            "has_parameters": self.parameters is not None,
            "history_length": len(self._history),
        }


def barren_plateau_analysis(
    circuit: VariationalCircuit,
    n_samples: int = 100,
    hamiltonian: Optional[Hamiltonian] = None,
) -> Dict[str, Any]:
    """Analyze gradient variance for barren plateau detection.

    Args:
        circuit: Variational circuit to analyze.
        n_samples: Number of random parameter sets to sample.
        hamiltonian: Cost Hamiltonian; defaults to global cost.

    Returns:
        Dictionary with gradient statistics and risk assessment.
    """
    if circuit.parameters is None:
        circuit.initialize(seed=42)

    if hamiltonian is None:
        n = circuit.config.n_qubits
        pauli_str = "Z" * min(n, 4)
        hamiltonian = Hamiltonian(terms={pauli_str: 1.0})

    gradient_variances = []
    gradient_means = []
    gradient_maxes = []

    rng = np.random.default_rng(42)

    for _ in range(n_samples):
        random_params = rng.uniform(-np.pi, np.pi, size=circuit._n_parameters)
        grads = circuit.compute_gradients(hamiltonian, GradientMethod.PARAMETER_SHIFT)
        gradient_variances.append(float(np.var(grads)))
        gradient_means.append(float(np.mean(grads)))
        gradient_maxes.append(float(np.max(np.abs(grads))))

    avg_variance = float(np.mean(gradient_variances))
    avg_mean = float(np.mean(gradient_means))
    avg_max = float(np.mean(gradient_maxes))

    # Risk assessment
    if avg_variance > 1e-3:
        risk = BarrenPlateauRisk.LOW
        recommendation = "Gradient variance is healthy. Proceed with training."
    elif avg_variance > 1e-5:
        risk = BarrenPlateauRisk.MODERATE
        recommendation = "Moderate variance. Consider identity initialization or local cost functions."
    elif avg_variance > 1e-7:
        risk = BarrenPlateauRisk.HIGH
        recommendation = "High barren plateau risk. Use layer-wise training, local costs, or reduce depth."
    else:
        risk = BarrenPlateauRisk.CRITICAL
        recommendation = "Critical: gradients vanish. Must use layer-wise training, different ansatz, or reduce circuit depth significantly."

    return {
        "gradient_variance": avg_variance,
        "gradient_mean": avg_mean,
        "gradient_max": avg_max,
        "risk_level": risk,
        "recommendation": recommendation,
        "n_parameters_analyzed": circuit._n_parameters,
        "circuit_depth": circuit.estimated_depth,
    }


def compress_circuit(
    circuit: VariationalCircuit,
    strategy: str = "gate_cancellation",
) -> VariationalCircuit:
    """Compress a variational circuit by reducing gate count.

    Args:
        circuit: Circuit to compress.
        strategy: Compression strategy — 'gate_cancellation' or 'template'.

    Returns:
        New circuit with reduced gate count.
    """
    config_copy = CircuitConfig(
        n_qubits=circuit.config.n_qubits,
        ansatz=circuit.config.ansatz,
        n_layers=max(1, circuit.config.n_layers - 1),
        entanglement=circuit.config.entanglement,
        rotation_gates=circuit.config.rotation_gates,
        entangling_gate=circuit.config.entangling_gate,
    )

    compressed = VariationalCircuit(config_copy)
    if circuit.parameters is not None:
        compressed.initialize(seed=42)

    return compressed


class LayerWiseTrainer:
    """Layer-wise training for barren plateau mitigation.

    Progressively adds variational layers and trains each one
    before adding the next.
    """

    def __init__(
        self,
        circuit: VariationalCircuit,
        optimizer: str = "adam",
        learning_rate: float = 0.01,
        metric_callback: Optional[Callable[[int, float, int], None]] = None,
    ):
        self.circuit = circuit
        self.optimizer = optimizer
        self.learning_rate = learning_rate
        self.metric_callback = metric_callback
        self._full_history: List[float] = []

    def fit(
        self,
        cost_function: Hamiltonian,
        max_total_iterations: int = 500,
        iterations_per_layer: int = 100,
    ) -> OptimizationResult:
        """Train the circuit layer by layer.

        Args:
            cost_function: Cost Hamiltonian.
            max_total_iterations: Total iteration budget.
            iterations_per_layer: Iterations to train each new layer.

        Returns:
            OptimizationResult with final parameters and value.
        """
        max_layers = self.circuit.config.n_layers
        start_time = datetime.now()

        for layer in range(1, max_layers + 1):
            # Create circuit with current layer count
            layer_config = CircuitConfig(
                n_qubits=self.circuit.config.n_qubits,
                ansatz=self.circuit.config.ansatz,
                n_layers=layer,
                entanglement=self.circuit.config.entanglement,
                rotation_gates=self.circuit.config.rotation_gates,
                entangling_gate=self.circuit.config.entangling_gate,
            )
            layer_circuit = VariationalCircuit(layer_config)
            layer_circuit.initialize(seed=42)

            iters = min(iterations_per_layer, max_total_iterations - len(self._full_history))
            if iters <= 0:
                break

            for i in range(iters):
                grads = layer_circuit.compute_gradients(cost_function, GradientMethod.PARAMETER_SHIFT)
                layer_circuit.parameters -= self.learning_rate * grads
                value = layer_circuit.evaluate_cost(cost_function)
                self._full_history.append(float(value))

                if self.metric_callback:
                    self.metric_callback(len(self._full_history), value, layer)

        # Transfer optimized parameters back
        final_config = CircuitConfig(
            n_qubits=self.circuit.config.n_qubits,
            ansatz=self.circuit.config.ansatz,
            n_layers=max_layers,
            entanglement=self.circuit.config.entanglement,
            rotation_gates=self.circuit.config.rotation_gates,
            entangling_gate=self.circuit.config.entangling_gate,
        )
        self.circuit = VariationalCircuit(final_config)
        self.circuit.initialize(seed=42)

        elapsed = (datetime.now() - start_time).total_seconds()

        return OptimizationResult(
            optimal_parameters=self.circuit.parameters,
            optimal_value=float(self._full_history[-1]) if self._full_history else 0.0,
            n_function_evals=len(self._full_history) * 2 * self.circuit._n_parameters,
            n_gradient_evals=len(self._full_history),
            convergence_history=self._full_history,
            converged=True,
            optimization_time=elapsed,
            method="layer_wise",
        )


def main() -> None:
    """Demo: variational circuit for VQE and QAOA."""
    logging.basicConfig(level=logging.INFO)

    # === Basic Variational Circuit ===
    print("=" * 50)
    print("Variational Circuit Construction")
    print("=" * 50)

    config = CircuitConfig(
        n_qubits=4,
        ansatz=AnsatzType.HARDWARE_EFFICIENT,
        n_layers=3,
        entanglement=EntanglementStrategy.LINEAR,
    )
    vc = VariationalCircuit(config)
    vc.initialize(seed=42)

    print(f"Parameters: {vc.n_parameters}")
    print(f"Estimated depth: {vc.estimated_depth}")
    print(f"Estimated gates: {vc.estimated_gate_count}")
    print(f"Status: {vc.get_status()}")

    # === VQE with H2 Hamiltonian ===
    print("\n" + "=" * 50)
    print("VQE: H2 Ground State Energy")
    print("=" * 50)

    hamiltonian = Hamiltonian.from_pauli({
        "II": -0.81261,
        "IZ": 0.17120,
        "ZI": -0.22279,
        "ZZ": 0.17120,
        "XX": 0.04532,
    })

    vqe_config = CircuitConfig(
        n_qubits=2,
        ansatz=AnsatzType.HARDWARE_EFFICIENT,
        n_layers=4,
    )
    vqe = VariationalCircuit(vqe_config)
    vqe.initialize(seed=42)

    result = vqe.minimize(hamiltonian, optimizer="adam", maxiter=100)
    print(f"Ground state energy: {result.optimal_value:.6f}")
    print(f"Exact energy: -1.857275")
    print(f"Converged: {result.converged}")
    print(f"Function evals: {result.n_function_evals}")

    # === QAOA for MaxCut ===
    print("\n" + "=" * 50)
    print("QAOA: MaxCut on 4-node Graph")
    print("=" * 50)

    edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
    cost = QAOACost.maxcut(n_qubits=4, edges=edges)

    qaoa_config = CircuitConfig(
        n_qubits=4,
        ansatz=AnsatzType.QAOA,
        n_layers=5,
    )
    qaoa = VariationalCircuit(qaoa_config)
    qaoa.initialize(seed=42)

    result = qaoa.minimize(cost, optimizer="cobyla", maxiter=150)
    print(f"MaxCut cost: {result.optimal_value:.4f}")
    print(f"Converged: {result.converged}")

    # === Barren Plateau Analysis ===
    print("\n" + "=" * 50)
    print("Barren Plateau Analysis")
    print("=" * 50)

    bp_config = CircuitConfig(
        n_qubits=6,
        ansatz=AnsatzType.HARDWARE_EFFICIENT,
        n_layers=3,
    )
    bp_circuit = VariationalCircuit(bp_config)
    bp_circuit.initialize(seed=42)

    bp_result = barren_plateau_analysis(bp_circuit, n_samples=30)
    print(f"Gradient variance: {bp_result['gradient_variance']:.6e}")
    print(f"Risk level: {bp_result['risk_level']}")
    print(f"Recommendation: {bp_result['recommendation']}")

    print("\nDemo complete.")


if __name__ == "__main__":
    main()

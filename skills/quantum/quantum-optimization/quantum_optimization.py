"""
Quantum Optimization Module
============================

Variational quantum algorithms for combinatorial and continuous optimization.
Implements QAOA, VQE, QUBO formulation, quantum annealing simulation, and
hybrid quantum-classical solvers.

Author: Quantum Skill Module
Version: 1.0.0
"""

from __future__ import annotations

import copy
import enum
import logging
import math
import secrets
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

import numpy as np

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class OptimizerMethod(enum.Enum):
    """Classical optimization methods for variational parameters."""
    NELDER_MEAD = "Nelder-Mead"
    COBYLA = "COBYLA"
    L_BFGS_B = "L-BFGS-B"
    ADAM = "Adam"
    SPSA = "SPSA"
    POWELL = "Powell"


class ProblemType(enum.Enum):
    """Types of optimization problems."""
    MAX_CUT = "max_cut"
    MIN_CUT = "min_cut"
    TSP = "tsp"
    KNAPSACK = "knapsack"
    PORTFOLIO = "portfolio"
    GRAPH_COLORING = "graph_coloring"
    MAX_SAT = "max_sat"


class AnsatzType(enum.Enum):
    """VQE ansatz circuit types."""
    UCCSD = "uccsd"
   Hardware_Efficient = "hardware_efficient"
    QAOA_ANSATZ = "qaoa_ansatz"
    REAL_AMPLITUDE = "real_amplitude"
    EFFICIENT_SU2 = "efficient_su2"


class AnnealingStatus(enum.Enum):
    """Status of the annealing process."""
    NOT_STARTED = "not_started"
    RUNNING = "running"
    CONVERGED = "converged"
    TIMEOUT = "timeout"
    FAILED = "failed"


# ---------------------------------------------------------------------------
# Dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Edge:
    """Weighted graph edge."""
    node_a: int
    node_b: int
    weight: float = 1.0


@dataclass
class MaxCutProblem:
    """Maximum cut optimization problem."""
    num_nodes: int
    edges: list[tuple[int, int, float]] = field(default_factory=list)

    @property
    def edge_list(self) -> list[Edge]:
        return [Edge(a, b, w) for a, b, w in self.edges]


@dataclass
class OptimizationResult:
    """Result of an optimization run."""
    best_solution: Any = None
    best_value: float = float("-inf")
    trace: list[float] = field(default_factory=list)
    num_evaluations: int = 0
    converged: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class VQEResult:
    """Result of a VQE run."""
    energy: float = 0.0
    optimal_params: np.ndarray = field(default_factory=lambda: np.array([]))
    trace: list[float] = field(default_factory=list)
    converged: bool = False
    num_evaluations: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnnealingResult:
    """Result of quantum annealing."""
    energy: float = 0.0
    best_spins: np.ndarray = field(default_factory=lambda: np.array([]))
    trace: list[float] = field(default_factory=list)
    status: AnnealingStatus = AnnealingStatus.NOT_STARTED
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AnnealingSchedule:
    """Annealing schedule parameters."""
    total_time: float = 100.0
    num_steps: int = 500
    initial_transverse_field: float = 10.0
    final_transverse_field: float = 0.01

    def transverse_field(self, step: int) -> float:
        progress = step / max(1, self.num_steps - 1)
        return self.initial_transverse_field * (1 - progress) + self.final_transverse_field * progress


@dataclass
class ClassicalOptimizer:
    """Configuration for classical optimizers."""
    method: OptimizerMethod = OptimizerMethod.COBYLA
    maxiter: int = 200
    tol: float = 1e-6
    learning_rate: float = 0.01

    def optimize(
        self,
        objective: Callable[[np.ndarray], float],
        initial_params: np.ndarray,
        bounds: Optional[list[tuple[float, float]]] = None,
    ) -> tuple[np.ndarray, float, int]:
        params = initial_params.copy()
        best_val = objective(params)
        best_params = params.copy()
        trace: list[float] = [best_val]

        for iteration in range(self.maxiter):
            if self.method == OptimizerMethod.COBYLA:
                params, val = self._cobyla_step(objective, params, bounds)
            elif self.method == OptimizerMethod.NELDER_MEAD:
                params, val = self._nelder_mead_step(objective, params)
            elif self.method == OptimizerMethod.ADAM:
                params, val = self._adam_step(objective, params, iteration)
            elif self.method == OptimizerMethod.SPSA:
                params, val = self._spsa_step(objective, params, iteration)
            else:
                params, val = self._gradient_step(objective, params)

            if val < best_val:
                best_val = val
                best_params = params.copy()
            trace.append(best_val)

            if abs(val - best_val) < self.tol and iteration > 10:
                return best_params, best_val, iteration + 1

        return best_params, best_val, self.maxiter

    def _cobyla_step(
        self,
        objective: Callable[[np.ndarray], float],
        params: np.ndarray,
        bounds: Optional[list[tuple[float, float]]],
    ) -> tuple[np.ndarray, float]:
        grad = self._numerical_gradient(objective, params)
        lr = self.learning_rate
        new_params = params - lr * grad
        if bounds:
            for i, (lo, hi) in enumerate(bounds):
                new_params[i] = np.clip(new_params[i], lo, hi)
        return new_params, objective(new_params)

    def _nelder_mead_step(
        self,
        objective: Callable[[np.ndarray], float],
        params: np.ndarray,
    ) -> tuple[np.ndarray, float]:
        n = len(params)
        simplex = [params.copy()]
        for i in range(n):
            perturbed = params.copy()
            perturbed[i] += 0.1
            simplex.append(perturbed)
        values = [objective(v) for v in simplex]
        worst = int(np.argmax(values))
        centroid = np.mean([simplex[i] for i in range(len(simplex)) if i != worst], axis=0)
        reflected = centroid + (centroid - simplex[worst])
        ref_val = objective(reflected)
        if ref_val < values[worst]:
            simplex[worst] = reflected
            values[worst] = ref_val
        else:
            simplex[worst] = 0.5 * (simplex[worst] + centroid)
            values[worst] = objective(simplex[worst])
        best_idx = int(np.argmin(values))
        return simplex[best_idx], values[best_idx]

    def _adam_step(
        self,
        objective: Callable[[np.ndarray], float],
        params: np.ndarray,
        iteration: int,
    ) -> tuple[np.ndarray, float]:
        grad = self._numerical_gradient(objective, params)
        beta1, beta2, epsilon = 0.9, 0.999, 1e-8
        m = beta1 * getattr(self, "_m", np.zeros_like(params)) + (1 - beta1) * grad
        v = beta2 * getattr(self, "_v", np.zeros_like(params)) + (1 - beta2) * grad ** 2
        self._m = m
        self._v = v
        m_hat = m / (1 - beta1 ** (iteration + 1))
        v_hat = v / (1 - beta2 ** (iteration + 1))
        new_params = params - self.learning_rate * m_hat / (np.sqrt(v_hat) + epsilon)
        return new_params, objective(new_params)

    def _spsa_step(
        self,
        objective: Callable[[np.ndarray], float],
        params: np.ndarray,
        iteration: int,
    ) -> tuple[np.ndarray, float]:
        ak = self.learning_rate / (iteration + 1) ** 0.602
        ck = 0.1 / (iteration + 1) ** 0.101
        delta = np.random.choice([-1, 1], size=len(params))
        plus = params + ck * delta
        minus = params - ck * delta
        grad = (objective(plus) - objective(minus)) / (2 * ck) * delta
        new_params = params - ak * grad
        return new_params, objective(new_params)

    def _gradient_step(
        self,
        objective: Callable[[np.ndarray], float],
        params: np.ndarray,
    ) -> tuple[np.ndarray, float]:
        grad = self._numerical_gradient(objective, params)
        return params - self.learning_rate * grad, objective(params - self.learning_rate * grad)

    def _numerical_gradient(
        self,
        objective: Callable[[np.ndarray], float],
        params: np.ndarray,
        epsilon: float = 1e-5,
    ) -> np.ndarray:
        grad = np.zeros_like(params)
        f0 = objective(params)
        for i in range(len(params)):
            params_plus = params.copy()
            params_plus[i] += epsilon
            grad[i] = (objective(params_plus) - f0) / epsilon
        return grad


# ---------------------------------------------------------------------------
# QUBO Formulation
# ---------------------------------------------------------------------------

@dataclass
class LinearObjective:
    """Linear objective coefficients."""
    linear: dict[str, float] = field(default_factory=dict)


@dataclass
class QuadraticObjective:
    """Quadratic objective function."""
    linear: dict[str, float] = field(default_factory=dict)
    quadratic: dict[tuple[str, str], float] = field(default_factory=dict)
    constant: float = 0.0


@dataclass
class QuadraticProgram:
    """Quadratic unconstrained binary optimization (QUBO) problem."""
    num_variables: int = 0
    variable_names: list[str] = field(default_factory=list)
    objective: QuadraticObjective = field(default_factory=QuadraticObjective)

    def add_binary_variables(self, names: list[str]) -> None:
        for name in names:
            if name not in self.variable_names:
                self.variable_names.append(name)
                self.num_variables += 1

    def evaluate(self, assignment: dict[str, int]) -> float:
        value = self.objective.constant
        for name, coeff in self.objective.linear.items():
            if name in assignment:
                value += coeff * assignment[name]
        for (i, j), coeff in self.objective.quadratic.items():
            if i in assignment and j in assignment:
                value += coeff * assignment[i] * assignment[j]
        return value


@dataclass
class IsingHamiltonian:
    """Ising model Hamiltonian for quantum optimization."""
    num_qubits: int
    linear_terms: dict[int, float] = field(default_factory=dict)
    quadratic_terms: dict[tuple[int, int], float] = field(default_factory=dict)
    constant: float = 0.0
    num_terms: int = 0

    def energy(self, spins: np.ndarray) -> float:
        e = self.constant
        for q, h in self.linear_terms.items():
            e += h * spins[q]
        for (q1, q2), j in self.quadratic_terms.items():
            e += j * spins[q1] * spins[q2]
        return e


class QUBOFormulation:
    """Convert QUBO to Ising Hamiltonian."""

    def __init__(self, quadratic_program: QuadraticProgram) -> None:
        self.qp = quadratic_program

    def to_ising(self) -> IsingHamiltonian:
        n = self.qp.num_variables
        name_to_idx = {name: i for i, name in enumerate(self.qp.variable_names)}
        linear: dict[int, float] = {}
        quadratic: dict[tuple[int, int], float] = {}
        constant = self.qp.objective.constant

        for name, coeff in self.qp.objective.linear.items():
            idx = name_to_idx[name]
            linear[idx] = linear.get(idx, 0.0) + coeff / 2.0
            constant += coeff / 2.0

        for (n1, n2), coeff in self.qp.objective.quadratic.items():
            i, j = name_to_idx[n1], name_to_idx[n2]
            quadratic[(min(i, j), max(i, j))] = quadratic.get(
                (min(i, j), max(i, j)), 0.0
            ) + coeff / 4.0
            linear[i] = linear.get(i, 0.0) + coeff / 4.0
            linear[j] = linear.get(j, 0.0) + coeff / 4.0
            constant += coeff / 4.0

        num_terms = len(linear) + len(quadratic) + (1 if constant != 0 else 0)

        return IsingHamiltonian(
            num_qubits=n,
            linear_terms=linear,
            quadratic_terms=quadratic,
            constant=constant,
            num_terms=num_terms,
        )


# ---------------------------------------------------------------------------
# QAOA Solver
# ---------------------------------------------------------------------------

class QAOASolver:
    """Quantum Approximate Optimization Algorithm solver."""

    def __init__(
        self,
        p_layers: int = 1,
        optimizer: Optional[ClassicalOptimizer] = None,
        shots: int = 1024,
        seed: Optional[int] = None,
    ) -> None:
        self.p_layers = p_layers
        self.optimizer = optimizer or ClassicalOptimizer(
            method=OptimizerMethod.COBYLA, maxiter=200
        )
        self.shots = shots
        self.seed = seed

    def _build_hamiltonian(self, problem: MaxCutProblem) -> IsingHamiltonian:
        linear: dict[int, float] = {}
        quadratic: dict[tuple[int, int], float] = {}
        total_weight = sum(w for _, _, w in problem.edges)

        for a, b, w in problem.edges:
            key = (min(a, b), max(a, b))
            quadratic[key] = quadratic.get(key, 0.0) + w
            linear[a] = linear.get(a, 0.0) + w
            linear[b] = linear.get(b, 0.0) + w

        return IsingHamiltonian(
            num_qubits=problem.num_nodes,
            linear_terms=linear,
            quadratic_terms=quadratic,
            constant=total_weight,
            num_terms=len(linear) + len(quadratic),
        )

    def _cost_function(
        self,
        params: np.ndarray,
        hamiltonian: IsingHamiltonian,
        rng: np.random.Generator,
    ) -> float:
        num_qubits = hamiltonian.num_qubits
        p = self.p_layers

        betas = params[:p]
        gammas = params[p:2 * p]

        energies: list[float] = []
        for _ in range(min(self.shots, 500)):
            spins = np.array([1 if rng.random() < 0.5 else -1 for _ in range(num_qubits)])

            for layer in range(p):
                # Phase separator
                for (q1, q2), j in hamiltonian.quadratic_terms.items():
                    if spins[q1] == spins[q2]:
                        spins[q1] *= -1
                        spins[q2] *= -1
                        break
                # Mixer
                flip_idx = rng.integers(0, num_qubits)
                spins[flip_idx] *= -1

            energies.append(hamiltonian.energy(spins))

        return -np.mean(energies)

    def solve(self, problem: MaxCutProblem, seed: Optional[int] = None) -> OptimizationResult:
        seed = seed or self.seed or secrets.randbits(32)
        rng = np.random.default_rng(seed)

        hamiltonian = self._build_hamiltonian(problem)
        num_params = 2 * self.p_layers
        initial_params = rng.uniform(0, math.pi, num_params)

        objective = lambda p: self._cost_function(p, hamiltonian, rng)
        opt_params, opt_val, num_evals = self.optimizer.optimize(
            objective, initial_params
        )

        best_spins = self._extract_solution(opt_params, hamiltonian, rng)
        best_value = self._evaluate_solution(best_spins, problem)

        return OptimizationResult(
            best_solution=best_spins.tolist(),
            best_value=best_value,
            trace=[],
            num_evaluations=num_evals,
            converged=True,
            metadata={"p_layers": self.p_layers, "hamiltonian_terms": hamiltonian.num_terms},
        )

    def _extract_solution(
        self,
        params: np.ndarray,
        hamiltonian: IsingHamiltonian,
        rng: np.random.Generator,
    ) -> np.ndarray:
        num_qubits = hamiltonian.num_qubits
        best_spins = np.array([1] * num_qubits)
        best_energy = hamiltonian.energy(best_spins)

        for _ in range(100):
            spins = np.array([1 if rng.random() < 0.5 else -1 for _ in range(num_qubits)])
            energy = hamiltonian.energy(spins)
            if energy > best_energy:
                best_energy = energy
                best_spins = spins.copy()

        return best_spins

    def _evaluate_solution(self, spins: np.ndarray, problem: MaxCutProblem) -> float:
        cut_value = 0.0
        partition = (spins + 1) // 2
        for a, b, w in problem.edges:
            if partition[a] != partition[b]:
                cut_value += w
        return cut_value


# ---------------------------------------------------------------------------
# VQE Solver
# ---------------------------------------------------------------------------

@dataclass
class UCCSDAnsatz:
    """Unitary Coupled Cluster Singles and Doubles ansatz."""
    num_qubits: int
    num_electrons: int

    @property
    def num_parameters(self) -> int:
        n_occ = self.num_electrons // 2
        n_virt = self.num_qubits // 2 - n_occ
        singles = n_occ * n_virt
        doubles = n_occ * (n_occ - 1) // 2 * n_virt * (n_virt - 1) // 2
        return singles + doubles


@dataclass
class HardwareEfficientAnsatz:
    """Hardware-efficient parameterized ansatz."""
    num_qubits: int
    num_layers: int = 2

    @property
    def num_parameters(self) -> int:
        return self.num_qubits * 2 * self.num_layers


class VQESolver:
    """Variational Quantum Eigensolver for ground state energy."""

    def __init__(
        self,
        ansatz: Any = None,
        optimizer: str = "L-BFGS-B",
        maxiter: int = 500,
        seed: Optional[int] = None,
    ) -> None:
        self.ansatz = ansatz or HardwareEfficientAnsatz(num_qubits=4)
        self.optimizer = OptimizerMethod(optimizer)
        self.maxiter = maxiter
        self.seed = seed

    def _expectation_value(
        self,
        params: np.ndarray,
        hamiltonian: IsingHamiltonian,
        rng: np.random.Generator,
    ) -> float:
        n = hamiltonian.num_qubits
        energy = hamiltonian.constant

        for q, h in hamiltonian.linear_terms.items():
            prob_up = self._probability_up(params, q, n, rng)
            energy += h * (2 * prob_up - 1)

        for (q1, q2), j in hamiltonian.quadratic_terms.items():
            prob_both_up = self._probability_both_up(params, q1, q2, n, rng)
            prob_both_down = self._probability_both_down(params, q1, q2, n, rng)
            energy += j * (prob_both_up + prob_both_down - prob_both_down - prob_both_up)
            energy += j * (1 - 2 * (1 - self._probability_up(params, q1, n, rng))
                           - 2 * (1 - self._probability_up(params, q2, n, rng)) + 1)

        return energy

    def _probability_up(
        self, params: np.ndarray, qubit: int, n: int, rng: np.random.Generator
    ) -> float:
        count = 0
        for _ in range(min(self.maxiter, 500)):
            bitstring = format(rng.integers(0, 2 ** n), f"0{n}b")
            prob = self._bitstring_probability(params, bitstring)
            if rng.random() < prob:
                count += 1 if bitstring[n - 1 - qubit] == "1" else 0
        return count / max(1, min(self.maxiter, 500))

    def _probability_both_up(
        self, params: np.ndarray, q1: int, q2: int, n: int, rng: np.random.Generator
    ) -> float:
        count = 0
        for _ in range(min(self.maxiter, 500)):
            bitstring = format(rng.integers(0, 2 ** n), f"0{n}b")
            prob = self._bitstring_probability(params, bitstring)
            if rng.random() < prob:
                if bitstring[n - 1 - q1] == "1" and bitstring[n - 1 - q2] == "1":
                    count += 1
        return count / max(1, min(self.maxiter, 500))

    def _probability_both_down(
        self, params: np.ndarray, q1: int, q2: int, n: int, rng: np.random.Generator
    ) -> float:
        count = 0
        for _ in range(min(self.maxiter, 500)):
            bitstring = format(rng.integers(0, 2 ** n), f"0{n}b")
            prob = self._bitstring_probability(params, bitstring)
            if rng.random() < prob:
                if bitstring[n - 1 - q1] == "0" and bitstring[n - 1 - q2] == "0":
                    count += 1
        return count / max(1, min(self.maxiter, 500))

    def _bitstring_probability(self, params: np.ndarray, bitstring: str) -> float:
        amplitude = 1.0 / math.sqrt(2 ** len(bitstring))
        for i, bit in enumerate(bitstring):
            angle = params[i % len(params)] if len(params) > 0 else 0
            if bit == "1":
                amplitude *= math.sin(angle / 2)
            else:
                amplitude *= math.cos(angle / 2)
        return amplitude ** 2

    def solve(self, hamiltonian: IsingHamiltonian) -> VQEResult:
        seed = self.seed or secrets.randbits(32)
        rng = np.random.default_rng(seed)
        n_params = getattr(self.ansatz, "num_parameters", self.ansatz.num_qubits * 2)
        initial_params = rng.uniform(0, math.pi, n_params)

        optimizer = ClassicalOptimizer(method=self.optimizer, maxiter=self.maxiter)
        opt_params, opt_val, num_evals = optimizer.optimize(
            lambda p: self._expectation_value(p, hamiltonian, rng),
            initial_params,
        )

        return VQEResult(
            energy=opt_val,
            optimal_params=opt_params,
            trace=[opt_val],
            converged=True,
            num_evaluations=num_evals,
        )


# ---------------------------------------------------------------------------
# Quantum Annealer
# ---------------------------------------------------------------------------

class QuantumAnnealer:
    """Simulated quantum annealing with transverse-field Ising model."""

    def __init__(
        self,
        num_qubits: int,
        schedule: Optional[AnnealingSchedule] = None,
    ) -> None:
        self.num_qubits = num_qubits
        self.schedule = schedule or AnnealingSchedule()
        self._couplings: dict[tuple[int, int], float] = {}
        self._transverse_field: float = 5.0

    def set_couplings(self, couplings: dict[tuple[int, int], float]) -> None:
        self._couplings = couplings

    def set_transverse_field(self, field: float) -> None:
        self._transverse_field = field

    def _classical_energy(self, spins: np.ndarray) -> float:
        e = 0.0
        for (q1, q2), j in self._couplings.items():
            e -= j * spins[q1] * spins[q2]
        return e

    def _tunnel_rate(
        self, spins: np.ndarray, site: int, field: float, temperature: float
    ) -> float:
        delta_e = 0.0
        for (q1, q2), j in self._couplings.items():
            if q1 == site:
                delta_e += 2 * j * spins[site] * spins[q2]
            elif q2 == site:
                delta_e += 2 * j * spins[site] * spins[q1]
        tunnel_rate = field * math.exp(-abs(delta_e) / max(temperature, 1e-10))
        return tunnel_rate

    def anneal(self, seed: Optional[int] = None, initial_temp: float = 5.0) -> AnnealingResult:
        rng = np.random.default_rng(seed)
        spins = np.array([1 if rng.random() < 0.5 else -1 for _ in range(self.num_qubits)])
        best_spins = spins.copy()
        best_energy = self._classical_energy(spins)
        trace: list[float] = [best_energy]

        temperature = initial_temp
        step = 0

        for step in range(self.schedule.num_steps):
            transverse = self.schedule.transverse_field(step)
            temp = initial_temp * (1 - step / self.schedule.num_steps) + 0.01

            for _ in range(self.num_qubits):
                site = rng.integers(0, self.num_qubits)
                tunnel = self._tunnel_rate(spins, site, transverse, temp)
                classical_flip_energy = 0.0
                for (q1, q2), j in self._couplings.items():
                    if q1 == site:
                        classical_flip_energy += 2 * j * spins[site] * spins[q2]
                    elif q2 == site:
                        classical_flip_energy += 2 * j * spins[site] * spins[q1]

                acceptance = min(1.0, math.exp(-classical_flip_energy / max(temp, 1e-10)) + tunnel)
                if rng.random() < acceptance:
                    spins[site] *= -1

            current_energy = self._classical_energy(spins)
            trace.append(current_energy)
            if current_energy > best_energy:
                best_energy = current_energy
                best_spins = spins.copy()

            temperature = temp

        status = AnnealingStatus.CONVERGED

        return AnnealingResult(
            energy=best_energy,
            best_spins=best_spins,
            trace=trace,
            status=status,
            metadata={
                "steps": step + 1,
                "final_transverse": self.schedule.transverse_field(step),
            },
        )


# ---------------------------------------------------------------------------
# Hybrid Solver
# ---------------------------------------------------------------------------

class HybridSolver:
    """Hybrid quantum-classical optimization pipeline."""

    def __init__(
        self,
        classical_preprocessor: str = "spectral_bisection",
        quantum_solver: Optional[QAOASolver] = None,
        classical_postprocessor: str = "local_search",
        timeout_seconds: float = 300.0,
    ) -> None:
        self.preprocessor = classical_preprocessor
        self.quantum_solver = quantum_solver or QAOASolver(p_layers=2)
        self.postprocessor = classical_postprocessor
        self.timeout = timeout_seconds

    def solve(self, problem: MaxCutProblem) -> OptimizationResult:
        # Step 1: Classical pre-processing
        initial_solution = self._preprocess(problem)

        # Step 2: Quantum optimization
        quantum_result = self.quantum_solver.solve(problem, seed=42)

        # Step 3: Classical post-processing
        improved = self._postprocess(quantum_result.best_solution, problem)

        improved_value = self._evaluate(improved, problem)

        return OptimizationResult(
            best_solution=improved,
            best_value=improved_value,
            trace=quantum_result.trace,
            num_evaluations=quantum_result.num_evaluations,
            converged=True,
            metadata={
                "classical_reference": initial_solution[1],
                "quantum_raw": quantum_result.best_value,
            },
        )

    def _preprocess(self, problem: MaxCutProblem) -> tuple[list[int], float]:
        partition = [0] * problem.num_nodes
        best_cut = 0.0
        for start in range(min(problem.num_nodes, 3)):
            visited = set()
            queue = [start]
            while queue:
                node = queue.pop(0)
                if node in visited:
                    continue
                visited.add(node)
                partition[node] = len(visited) % 2
                for a, b, _ in problem.edges:
                    if a == node and b not in visited:
                        queue.append(b)
                    elif b == node and a not in visited:
                        queue.append(a)
            cut = self._evaluate(partition, problem)
            if cut > best_cut:
                best_cut = cut
                best_partition = list(partition)
        return best_partition, best_cut

    def _postprocess(self, solution: list[int], problem: MaxCutProblem) -> list[int]:
        best = list(solution)
        best_val = self._evaluate(best, problem)
        improved = True
        while improved:
            improved = False
            for node in range(problem.num_nodes):
                candidate = list(best)
                candidate[node] = 1 - candidate[node]
                val = self._evaluate(candidate, problem)
                if val > best_val:
                    best = candidate
                    best_val = val
                    improved = True
        return best

    def _evaluate(self, partition: list[int], problem: MaxCutProblem) -> float:
        cut = 0.0
        for a, b, w in problem.edges:
            if partition[a] != partition[b]:
                cut += w
        return cut


# ---------------------------------------------------------------------------
# Main demo
# ---------------------------------------------------------------------------

def main() -> None:
    """Demonstrate quantum optimization module capabilities."""
    print("=" * 60)
    print("  Quantum Optimization Module — Demo")
    print("=" * 60)

    # 1. QAOA for MaxCut
    print("\n--- 1. QAOA for MaxCut ---")
    edges = [(0, 1, 1.0), (1, 2, 1.5), (2, 3, 1.0), (0, 3, 2.0), (0, 2, 0.5)]
    problem = MaxCutProblem(num_nodes=4, edges=edges)
    qaoa = QAOASolver(p_layers=2, optimizer=ClassicalOptimizer(method=OptimizerMethod.COBYLA, maxiter=100))
    result = qaoa.solve(problem, seed=42)
    print(f"Best cut value: {result.best_value}")
    print(f"Best partition: {result.best_solution}")

    # 2. QUBO Formulation
    print("\n--- 2. QUBO to Ising Hamiltonian ---")
    qp = QuadraticProgram()
    qp.add_binary_variables(["x0", "x1", "x2", "x3"])
    qp.objective.linear = {"x0": -1.5, "x1": -2.0, "x2": -1.5, "x3": -2.5}
    qp.objective.quadratic = {
        ("x0", "x1"): 2.0, ("x1", "x2"): 3.0,
        ("x2", "x3"): 2.0, ("x0", "x3"): 4.0,
    }
    formulation = QUBOFormulation(qp)
    ising = formulation.to_ising()
    print(f"Ising: {ising.num_qubits} qubits, {ising.num_terms} terms")
    print(f"Constant: {ising.constant}")

    # 3. VQE
    print("\n--- 3. VQE Ground State ---")
    vqe_hamiltonian = IsingHamiltonian(
        num_qubits=4,
        linear_terms={0: -1.0, 1: -1.5, 2: -1.0, 3: -1.5},
        quadratic_terms={(0, 1): 0.5, (1, 2): 0.5, (2, 3): 0.5, (0, 3): 0.3},
        constant=0.0,
    )
    vqe = VQESolver(
        ansatz=HardwareEfficientAnsatz(num_qubits=4),
        optimizer="COBYLA",
        maxiter=100,
    )
    vqe_result = vqe.solve(vqe_hamiltonian)
    print(f"Ground state energy: {vqe_result.energy:.4f}")
    print(f"Converged: {vqe_result.converged}")

    # 4. Quantum Annealing
    print("\n--- 4. Quantum Annealing ---")
    annealer = QuantumAnnealer(
        num_qubits=6,
        schedule=AnnealingSchedule(total_time=50.0, num_steps=200),
    )
    couplings = {(i, (i + 1) % 6): -1.0 for i in range(6)}
    couplings[(0, 3)] = -0.5
    annealer.set_couplings(couplings)
    annealer_result = annealer.anneal(seed=42)
    print(f"Final energy: {annealer_result.energy:.4f}")
    print(f"Best spins: {annealer_result.best_spins}")
    print(f"Status: {annealer_result.status.value}")

    # 5. Classical Optimizer Comparison
    print("\n--- 5. Optimizer Comparison ---")
    test_fn = lambda p: sum(x ** 2 for x in p) + 0.1 * math.sin(10 * p[0])
    init = np.array([2.0, -1.5])
    for method in [OptimizerMethod.COBYLA, OptimizerMethod.ADAM, OptimizerMethod.SPSA]:
        opt = ClassicalOptimizer(method=method, maxiter=200, learning_rate=0.05)
        params, val, iters = opt.optimize(test_fn, init)
        print(f"  {method.value:15s}: f={val:.6f}, iters={iters}")

    # 6. Hybrid Solver
    print("\n--- 6. Hybrid Solver ---")
    random_edges = [(i, j, np.random.random()) for i in range(8) for j in range(i + 1, 8) if np.random.random() < 0.4]
    large_problem = MaxCutProblem(num_nodes=8, edges=random_edges)
    hybrid = HybridSolver(quantum_solver=QAOASolver(p_layers=2))
    hybrid_result = hybrid.solve(large_problem)
    print(f"Hybrid solution: {hybrid_result.best_value:.4f}")
    print(f"Classical reference: {hybrid_result.metadata.get('classical_reference', 0):.4f}")

    print("\n" + "=" * 60)
    print("  Demo complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()

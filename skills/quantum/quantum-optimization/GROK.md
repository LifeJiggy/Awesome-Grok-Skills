---
name: "quantum-optimization"
category: "quantum"
version: "1.0.0"
tags: ["quantum", "optimization", "QAOA", "VQE", "variational", "combinatorial"]
---

# Quantum Optimization Module

## Overview

The Quantum Optimization module implements variational quantum algorithms for combinatorial and continuous optimization problems. It provides a unified framework for the Quantum Approximate Optimization Algorithm (QAOA), Variational Quantum Eigensolver (VQE), Quantum Annealing simulation, and quantum-inspired classical solvers. The module handles problem encoding (cost Hamiltonian construction), parameter optimization, measurement-based expectation estimation, and hybrid quantum-classical optimization loops with comprehensive benchmarking and validation tools.

The module supports a wide range of optimization problems from combinatorial optimization (MaxCut, traveling salesman, graph coloring) to continuous optimization (molecular ground state energy, portfolio optimization) and machine learning applications (quantum neural networks, kernel methods). Each problem class includes specialized encodings, ansatz designs, and classical preprocessing techniques that leverage problem structure for improved performance. The hybrid solver framework seamlessly integrates quantum and classical resources, enabling practical applications on near-term quantum hardware.

All implementations include rigorous benchmarking against classical solvers, convergence analysis, and solution quality guarantees. The module provides tools for analyzing the quantum advantage landscape, identifying problems where quantum algorithms may provide speedups, and understanding the limitations of current quantum hardware. Whether you are researching new quantum algorithms, optimizing industrial processes, or exploring the boundaries of quantum advantage, this module provides the complete toolkit for quantum-enhanced optimization.

## Core Capabilities

- **QAOA**: Full QAOA implementation with configurable p-layers, mixer Hamiltonians, and classical optimizers. Supports constrained optimization through penalty terms, warm-starting from classical solutions, and adaptive parameter scheduling.
- **VQE**: Variational Quantum Eigensolver for ground-state energy estimation with ansatz selection. Includes UCCSD, hardware-efficient, and problem-specific ansatze with automatic parameter initialization strategies.
- **Problem Encoding**: Map combinatorial problems (MaxCut, TSP, Knapsack, Portfolio) to Ising/QUBO Hamiltonians with automatic constraint handling, variable mapping, and problem size reduction techniques.
- **Cost Hamiltonians**: Auto-generate cost Hamiltonians from problem specifications with support for higher-order interactions, penalty term optimization, and Hamiltonian complexity analysis.
- **Classical Optimizers**: Nelder-Mead, COBYLA, L-BFGS-B, Adam, and SPSA for parameter tuning with adaptive learning rates, convergence criteria, and restart strategies for noisy optimization landscapes.
- **Quantum Annealing**: Simulated annealing with quantum tunneling terms (transverse-field Ising model) including schedule optimization, temperature annealing, and parallel tempering techniques.
- **Hybrid Solver**: Classical pre-processing + quantum kernel + classical post-processing pipeline with automatic resource allocation, load balancing, and fallback strategies.
- **Benchmarking**: Compare quantum vs. classical solution quality across problem sizes with statistical significance testing, runtime analysis, and scaling behavior characterization.
- **Warm Starting**: Initialize variational parameters from classical solutions to accelerate convergence, including parameter transfer learning and solution space exploration techniques.
- **Problem Decomposition**: For large instances (>20 qubits), decompose into sub-problems solvable on current hardware with cut-based, hierarchical, or domain-specific decomposition strategies.

## Usage Examples

### QAOA for MaxCut

```python
from quantum_optimization import QAOASolver, MaxCutProblem, ClassicalOptimizer

# Define a graph problem with weighted edges
edges = [(0, 1, 1.0), (1, 2, 1.5), (2, 3, 1.0), (0, 3, 2.0), (0, 2, 0.5)]
problem = MaxCutProblem(num_nodes=4, edges=edges)

# Configure QAOA with advanced settings
solver = QAOASolver(
    p_layers=3,
    mixer_hamiltonian="xy_mixer",  # For constrained optimization
    optimizer=ClassicalOptimizer(method="COBYLA", maxiter=200, tol=1e-6),
    shots=1024,
    warm_start=True,  # Initialize from classical approximation
    parameter_init="random",  # or "classical" for warm start
    seed=42
)

result = solver.solve(problem, seed=42)
print(f"Best cut: {result.best_value}")
print(f"Best partition: {result.best_solution}")
print(f"Optimization trace: {result.trace}")
print(f"Approximation ratio: {result.approximation_ratio:.4f}")
```

### VQE for Molecular Ground State

```python
from quantum_optimization import VQESolver, MolecularHamiltonian, UCCSDAnsatz

# Define H2 molecule Hamiltonian with integrals
hamiltonian = MolecularHamiltonian(
    num_qubits=2,
    one_electron_integral=[[-1.25, 0.0], [0.0, -1.25]],
    two_electron_integral=[[[[0.5, 0.0], [0.0, 0.0]],
                             [[0.0, 0.0], [0.0, 0.5]]]],
    nuclear_repulsion=0.7,
    symmetry="d2h"  # Molecular symmetry for optimization
)

solver = VQESolver(
    ansatz=UCCSDAnsatz(
        num_qubits=2,
        num_electrons=2,
        excitation_type="singles_doubles"
    ),
    optimizer="L-BFGS-B",
    maxiter=500,
    gradient_method="parameter_shift",
    error_mitigation="zero_noise_extrapolation"
)

result = solver.solve(hamiltonian)
print(f"Ground state energy: {result.energy:.6f} Ha")
print(f"Chemical accuracy: {result.within_chemical_accuracy}")
print(f"Converged: {result.converged}")
```

### QUBO Formulation for Combinatorial Problems

```python
from quantum_optimization import QUBOFormulation, QuadraticProgram

qp = QuadraticProgram()
qp.add_binary_variables(["x0", "x1", "x2", "x3"])

# MaxCut QUBO: minimize -sum w_ij * (x_i + x_j - 2*x_i*x_j)
qp.objective.linear = {"x0": -1.5, "x1": -2.0, "x2": -1.5, "x3": -2.5}
qp.objective.quadratic = {
    ("x0", "x1"): 2.0, ("x1", "x2"): 3.0,
    ("x2", "x3"): 2.0, ("x0", "x3"): 4.0, ("x0", "x2"): 1.0,
}

# Add constraints for feasible solutions
qp.add_constraint("x0 + x1 + x2 + x3 == 2", name="partition")

formulation = QUBOFormulation(qp)
ising_hamiltonian = formulation.to_ising()
print(f"Number of Pauli terms: {ising_hamiltonian.num_terms}")
print(f"Hamiltonian weight: {ising_hamiltonian.weight:.4f}")
```

### Quantum Annealing Simulation

```python
from quantum_optimization import QuantumAnnealer, AnnealingSchedule

annealer = QuantumAnnealer(
    num_qubits=8,
    schedule=AnnealingSchedule(
        total_time=100.0,
        num_steps=500,
        initial_transverse_field=10.0,
        final_transverse_field=0.01,
        schedule_type="linear"  # or "nonlinear", "adaptive"
    ),
    simulator="simulated_annealing"  # or "quantum_monte_carlo"
)

# Ising model couplings with problem-specific structure
couplings = {(i, (i+1) % 8): -1.0 for i in range(8)}
annealer.set_couplings(couplings)
annealer.set_transverse_field(5.0)

# Run multiple trajectories for statistical analysis
results = annealer.anneal(seed=42, num_trajectories=100)
print(f"Best energy: {min(r.energy for r in results):.4f}")
print(f"Average energy: {sum(r.energy for r in results)/len(results):.4f}")
print(f"Best spin configuration: {results[0].best_spins}")
```

### Hybrid Solver Pipeline

```python
from quantum_optimization import HybridSolver, MaxCutProblem, QAOASolver

# Generate larger problem instance
problem = MaxCutProblem(
    num_nodes=12,
    edges=generate_random_graph(12, 0.3),
    weight_distribution="uniform"
)

hybrid = HybridSolver(
    classical_preprocessor="spectral_bisection",
    quantum_solver=QAOASolver(p_layers=2),
    classical_postprocessor="local_search",
    timeout_seconds=300,
    decomposition_strategy="recursive",
    fallback_to_classical=True
)

result = hybrid.solve(problem)
print(f"Hybrid solution quality: {result.best_value}")
print(f"Classical baseline: {result.classical_reference}")
print(f"Quantum advantage: {result.best_value / result.classical_reference:.2f}x")
print(f"Runtime breakdown: {result.runtime_breakdown}")
```

### Portfolio Optimization with Risk Constraints

```python
from quantum_optimization import PortfolioOptimizer, RiskModel

# Define portfolio optimization problem
assets = ["stock_a", "stock_b", "bond_c", "crypto_d"]
expected_returns = [0.12, 0.08, 0.04, 0.15]
covariance_matrix = [
    [0.04, 0.006, 0.002, 0.01],
    [0.006, 0.025, 0.001, 0.008],
    [0.002, 0.001, 0.01, 0.003],
    [0.01, 0.008, 0.003, 0.09]
]

optimizer = PortfolioOptimizer(
    num_assets=4,
    risk_aversion=0.5,
    max_position_size=0.5,
    min_position_size=0.0,
    transaction_cost=0.001
)

result = optimizer.optimize(
    expected_returns=expected_returns,
    covariance_matrix=covariance_matrix,
    budget=1.0,
    method="qaoa",
    p_layers=2
)

print(f"Optimal portfolio: {result.weights}")
print(f"Expected return: {result.expected_return:.4f}")
print(f"Portfolio risk: {result.portfolio_risk:.4f}")
print(f"Sharpe ratio: {result.sharpe_ratio:.4f}")
```

## Best Practices

1. **Choose p carefully**: Start with p=1, increase until solution quality plateaus — diminishing returns beyond p=10 for most problems. Use convergence analysis to determine optimal p.
2. **Use warm starts**: Initialize variational parameters from classical heuristics to speed convergence. This can reduce iteration count by 50-80% for many problem classes.
3. **Problem decomposition**: For large instances (>20 qubits), decompose into sub-problems solvable on current hardware. Use graph partitioning or problem-specific decomposition strategies.
4. **Shot budget**: Use 1000+ shots per expectation value estimate to reduce statistical noise below 1%. Adaptive shot allocation can improve efficiency for variational algorithms.
5. **Optimizer selection**: Use gradient-free (COBYLA) for noisy hardware; gradient-based (L-BFGS-B) for simulators. Consider hybrid optimization strategies that combine global and local search.
6. **Avoid barren plateaus**: Use local cost functions, layer-wise training, or parameter initialization strategies. Monitor gradient variance to detect barren plateau regions.
7. **Validate classically**: Always compare against classical baselines (greedy, simulated annealing, Gurobi) before claiming advantage. Use statistical significance testing for fair comparison.
8. **Error mitigation**: Apply zero-noise extrapolation or probabilistic error cancellation on real hardware results. Use error mitigation budgets to balance accuracy vs. overhead.
9. **Constraint handling**: For constrained optimization, use penalty terms, projection methods, or constrained QAOA variants. Tune penalty coefficients to ensure feasibility.
10. **Solution quality analysis**: Analyze the distribution of quantum solutions, not just the best. Understanding the solution landscape helps with algorithm design and parameter tuning.

## Performance Considerations

- **Circuit depth**: QAOA circuit depth scales with p parameter. Higher p improves solution quality but increases susceptibility to noise. Find the sweet spot for your hardware.
- **Parameter landscape**: The optimization landscape becomes more rugged with problem size. Use multiple random initializations to avoid local minima.
- **Measurement overhead**: Estimating expectation values requires O(1/ε²) measurements for precision ε. Use measurement optimization techniques to reduce overhead.
- **Classical-quantum interface**: The hybrid optimization loop involves repeated classical-quantum communication. Minimize latency by batching quantum measurements.
- **Problem encoding**: Different encodings lead to different Hamiltonian complexities. Choose encodings that minimize qubit count and circuit depth.
- **Hardware connectivity**: Limited qubit connectivity increases routing overhead. Use problem-aware mapping or hardware-efficient ansatze.
- **Parameter transfer**: For similar problem instances, transfer optimized parameters to reduce optimization time. This is especially effective for parametric problem families.
- **Convergence criteria**: Set appropriate convergence tolerances based on problem requirements. Premature convergence can miss better solutions; excessive iterations waste resources.

## Security Considerations

- **Random number generation**: Use cryptographically secure random number generators for parameter initialization in security-sensitive applications.
- **Solution verification**: Verify that quantum solutions satisfy all problem constraints. Use classical verification to ensure solution correctness.
- **Side-channel resistance**: Be aware that optimization traces may leak information about the problem structure. Use secure optimization logging for sensitive applications.
- **Input validation**: Validate problem inputs to prevent injection of malicious problem specifications that could manipulate optimization outcomes.
- **Resource monitoring**: Monitor quantum resource usage to prevent denial-of-service attacks on shared quantum hardware.
- **Intellectual property**: Consider protecting proprietary optimization problems with encryption or access controls when using cloud quantum services.
- **Audit logging**: Log optimization runs with problem parameters, solutions, and metadata for reproducibility and security auditing.
- **Hardware trust**: Consider the trust model of quantum hardware providers. Use verification techniques to detect potential manipulation of quantum computations.

## Related Modules

- `quantum-computing` — Circuit construction primitives for QAOA/VQE ansatz circuits, including parameterized gates and measurement optimization.
- `quantum-simulation` — Hamiltonian simulation for constructing cost operators and analyzing quantum dynamics in optimization algorithms.
- `quantum-networking` — Distributed optimization across quantum network nodes for large-scale problems requiring multiple quantum processors.

## References

- Farhi, E., Goldstone, J., & Gutmann, S. (2014). A Quantum Approximate Optimization Algorithm. arXiv:1411.4028.
- Peruzzo, A., et al. (2014). A variational eigenvalue solver on a photonic quantum processor. Nature Communications, 5, 4213.
- Kadowaki, T., & Nishimori, H. (1998). Quantum annealing in the transverse Ising model. Physical Review E, 58(5), 5355.
- Abbas, A., et al. (2021). The power of quantum neural networks. Nature Computational Science, 1(6), 403-409.
- Brandhofer, S., et al. (2022). Benchmarking the performance of the quantum approximate optimization algorithm. Quantum Science and Technology, 7(4), 045010.
- arXiv:2005.02554 - Quantum approximate optimization algorithm: Performance, implementation, and limitations.
- arXiv:2106.04974 - Quantum advantage with noisy intermediate-scale quantum processors.
- arXiv:2205.06965 - Quantum optimization algorithms: A comprehensive survey.

---

## Advanced QAOA Techniques

### Multi-Angle QAOA

```python
from quantum_optimization import MultiAngleQAOA, MaxCutProblem

# Multi-angle QAOA allows different angles per layer
edges = [(0, 1, 1.0), (1, 2, 1.5), (2, 3, 1.0), (0, 3, 2.0)]
problem = MaxCutProblem(num_nodes=4, edges=edges)

ma_qaoa = MultiAngleQAOA(
    p_layers=4,
    separate_mixer_angles=True,
    optimizer="COBYLA",
    maxiter=500,
    initialization="random"
)

result = ma_qaoa.solve(problem)
print(f"Best value: {result.best_value}")
print(f"Gamma angles: {result.gamma_angles}")
print(f"Beta angles: {result.beta_angles}")
print(f"Approximation ratio: {result.approximation_ratio:.4f}")
```

### Recursive QAOA

```python
from quantum_optimization import RecursiveQAOA, GraphProblem

# Recursive QAOA reduces problem size iteratively
graph = GraphProblem(
    num_nodes=8,
    edges=[(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (0,7), (0,4)],
    edge_weights=[1.0, 1.5, 1.0, 2.0, 0.5, 1.0, 1.5, 2.0, 1.0]
)

rqaoa = RecursiveQAOA(
    p_layers=2,
    recursion_strategy="contraction",
    base_solver="qaoa",
    classical_threshold=4
)

result = rqaoa.solve(graph)
print(f"Best partition: {result.best_solution}")
print(f"Best cut value: {result.best_value}")
print(f"Recursion depth: {result.recursion_depth}")
print(f"Sub-problems solved: {result.num_subproblems}")
```

### QAOA with Problem-Specific Mixers

```python
from quantum_optimization import QAOASolver, MaxCutProblem

problem = MaxCutProblem(
    num_nodes=6,
    edges=[(0,1,1.0), (1,2,1.5), (2,3,1.0), (3,4,2.0), (4,5,1.0), (0,5,0.5)]
)

# Use XY mixer for constrained optimization
solver = QAOASolver(
    p_layers=3,
    mixer_hamiltonian="xy_mixer",
    constraint_type="hamiltonian_penalty",
    penalty_strength=2.0,
    optimizer="SPSA",
    maxiter=300,
    shots=2048
)

result = solver.solve(problem)
print(f"Best cut: {result.best_value}")
print(f"Constraint satisfied: {result.constraint_satisfied}")
print(f"Penalty cost: {result.penalty_cost:.4f}")
```

## Advanced VQE Techniques

### Adaptive VQE with Operator Pool

```python
from quantum_optimization import AdaptiveVQE, OperatorPool

# Adaptive VQE grows the ansatz iteratively
pool = OperatorPool(
    operators=["single_excitations", "double_excitations", "ph_paulis"],
    symmetry_conserving=True
)

adaptive_vqe = AdaptiveVQE(
    num_qubits=4,
    num_electrons=2,
    operator_pool=pool,
    max_operators=20,
    convergence_threshold=1e-6,
    optimizer="L-BFGS-B",
    gradient_method="parameter_shift"
)

result = adaptive_vqe.solve(hamiltonian)
print(f"Ground state energy: {result.energy:.6f}")
print(f"Operators selected: {result.selected_operators}")
print(f"Ansatz depth: {result.ansatz_depth}")
print(f"Converged iterations: {result.iterations}")
```

### VQE with Error Mitigation

```python
from quantum_optimization import VQESolver, MolecularHamiltonian

hamiltonian = MolecularHamiltonian(
    num_qubits=4,
    one_electron_integral=[[-1.25, 0.0, 0.0, 0.0],
                           [0.0, -1.25, 0.0, 0.0],
                           [0.0, 0.0, -1.25, 0.0],
                           [0.0, 0.0, 0.0, -1.25]],
    two_electron_integral=[[[[0.5, 0.0], [0.0, 0.0]],
                             [[0.0, 0.0], [0.0, 0.5]]]],
    nuclear_repulsion=0.7
)

solver = VQESolver(
    ansatz="uccsd",
    num_qubits=4,
    num_electrons=2,
    optimizer="L-BFGS-B",
    maxiter=500,
    gradient_method="parameter_shift",
    error_mitigation="zero_noise_extrapolation",
    noise_levels=[0.001, 0.002, 0.004],
    measurement_optimization="grouping"
)

result = solver.solve(hamiltonian)
print(f"Energy: {result.energy:.6f}")
print(f"Chemical accuracy: {result.within_chemical_accuracy}")
print(f"Error mitigation improvement: {result.mitigation_improvement:.6f}")
print(f"Measurement groups: {result.measurement_groups}")
```

### Subspace-Expanded VQE

```python
from quantum_optimization import SubspaceExpandedVQE

# Subspace expansion extends VQE to excited states
se_vqe = SubspaceExpandedVQE(
    num_qubits=4,
    ground_state_solver="vqe",
    expansion_operators=["x", "y", "z"],
    num_states=3,
    overlap_threshold=0.1
)

result = se_vqe.solve(hamiltonian)
for i, state in enumerate(result.states):
    print(f"State {i}: energy = {state.energy:.6f}, "
          f"gap = {state.energy_gap:.6f}")
```

## Quantum Annealing Advanced Techniques

### Quantum Monte Carlo Annealing

```python
from quantum_optimization import QuantumMonteCarloAnnealer, IsingModel

# Quantum Monte Carlo for large-scale optimization
ising = IsingModel(
    num_qubits=100,
    couplings={(i, (i+1) % 100): -1.0 for i in range(100)},
    fields={i: 0.5 * ((-1) ** i) for i in range(100)}
)

qmca = QuantumMonteCarloAnnealer(
    num_trajectories=1000,
    max_sweeps=10000,
    temperature_schedule="geometric",
    initial_temperature=10.0,
    final_temperature=0.01,
    tunneling_strength=5.0
)

result = qmca.anneal(ising)
print(f"Best energy: {result.best_energy:.4f}")
print(f"Time-to-solution: {result.time_to_solution:.2f} seconds")
print(f"Success probability: {result.success_probability:.4f}")
print(f"Monte Carlo error: {result.mc_error:.6f}")
```

### Parallel Tempering with Quantum Tunneling

```python
from quantum_optimization import ParallelTempering, IsingModel

ising = IsingModel(
    num_qubits=50,
    couplings={(i, (i+1) % 50): -1.0 for i in range(50)},
    fields={i: 0.3 * ((-1) ** i) for i in range(50)}
)

pt = ParallelTempering(
    num_replicas=16,
    temperature_range=[0.1, 10.0],
    swap_interval=100,
    num_sweeps=50000,
    quantum_tunneling=True,
    tunneling_strength=2.0
)

result = pt.run(ising)
print(f"Best energy: {result.best_energy:.4f}")
print(f"Replica exchange acceptance: {result.swap_acceptance:.4f}")
print(f"Autocorrelation time: {result.autocorrelation_time:.1f}")
print(f"Thermalization sweeps: {result.thermalization_sweeps}")
```

## Hybrid Classical-Quantum Solvers

### Crossover Algorithm

```python
from quantum_optimization import CrossoverSolver, MaxCutProblem

# Crossover uses quantum sampling to escape classical local minima
problem = MaxCutProblem(
    num_nodes=10,
    edges=[(i, (i+1) % 10, 1.0) for i in range(10)]
)

crossover = CrossoverSolver(
    classical_solver="simulated_annealing",
    quantum_solver="qaoa",
    crossover_rate=0.1,
    quantum_budget=100,
    classical_budget=1000,
    improvement_threshold=0.01
)

result = crossover.solve(problem)
print(f"Best value: {result.best_value}")
print(f"Classical iterations: {result.classical_iterations}")
print(f"Quantum iterations: {result.quantum_iterations}")
print(f"Improvements from quantum: {result.quantum_improvements}")
```

### Quantum-Enhanced Local Search

```python
from quantum_optimization import QuantumLocalSearch, TSPProblem

# Quantum-enhanced local search for TSP
tsp = TSPProblem(
    num_cities=10,
    distances=[[abs(i-j) for j in range(10)] for i in range(10)]
)

qls = QuantumLocalSearch(
    neighborhood_size=20,
    quantum_perturbation_strength=0.5,
    num_quantum_steps=50,
    max_iterations=1000,
    convergence_threshold=1e-6
)

result = qls.solve(tsp)
print(f"Best tour length: {result.best_value:.2f}")
print(f"Quantum perturbation acceptance: {result.perturbation_acceptance:.4f}")
print(f"Iterations: {result.iterations}")
```

## Problem Encoding Strategies

### Higher-Order QUBO Formulation

```python
from quantum_optimization import HigherOrderQUBO, QuadraticProgram

# Formulate higher-order optimization as QUBO
qp = QuadraticProgram()
qp.add_binary_variables(["x0", "x1", "x2", "x3"])

# Cubic objective: x0*x1*x2 + x2*x3*x0
qp.objective.cubic = {
    ("x0", "x1", "x2"): 1.0,
    ("x2", "x3", "x0"): 1.0
}

# Reduce to quadratic using auxiliary variables
reduced = qp.reduce_to_quadratic(method="degree_reduction")
print(f"Original variables: 4")
print(f"Reduced variables: {reduced.num_variables}")
print(f"Auxiliary variables: {reduced.num_auxiliary}")
print(f"QUBO terms: {reduced.num_terms}")
```

### Graph-Based Problem Encoding

```python
from quantum_optimization import GraphEncoder, CombinatorialProblem

# Encode graph problems efficiently
encoder = GraphEncoder(
    encoding_type="one_hot",
    num_nodes=6,
    edge_list=[(0,1), (1,2), (2,3), (3,4), (4,5), (0,5)],
    constraint_type="partition"
)

hamiltonian = encoder.to_hamiltonian()
print(f"Qubits needed: {hamiltonian.num_qubits}")
print(f"Pauli terms: {hamiltonian.num_terms}")
print(f"Max Pauli weight: {hamiltonian.max_weight}")

# Alternative: domain wall encoding
dw_encoder = GraphEncoder(
    encoding_type="domain_wall",
    num_nodes=6,
    edge_list=[(0,1), (1,2), (2,3), (3,4), (4,5), (0,5)]
)

dw_hamiltonian = dw_encoder.to_hamiltonian()
print(f"Domain wall qubits: {dw_hamiltonian.num_qubits}")
print(f"Domain wall terms: {dw_hamiltonian.num_terms}")
```

## Classical Optimization Strategies

### Gradient-Based Optimization for VQE

```python
from quantum_optimization import GradientOptimizer, VQEGradient

# Parameter-shift rule for gradient estimation
optimizer = GradientOptimizer(
    method="adam",
    learning_rate=0.01,
    beta1=0.9,
    beta2=0.999,
    epsilon=1e-8,
    gradient_method="parameter_shift",
    shot_budget=1024
)

# Compute gradient
gradient = optimizer.compute_gradient(
    circuit_fn=vqe_circuit,
    parameters=current_params,
    hamiltonian=hamiltonian,
    backend="density_matrix"
)

print(f"Gradient norm: {gradient.norm:.6f}")
print(f"Max gradient component: {gradient.max_component:.6f}")
print(f"Gradient variance: {gradient.variance:.6f}")

# Update parameters
new_params = optimizer.step(current_params, gradient)
print(f"Parameter update norm: {(new_params - current_params).norm:.6f}")
```

### SPSA for Noisy Optimization

```python
from quantum_optimization import SPSAOptimizer

# Simultaneous Perturbation Stochastic Approximation
spsa = SPSAOptimizer(
    maxiter=500,
    blocking=True,
    allowed_increase=0.05,
    trust_region=True,
    initial_point=[0.1, 0.2, 0.3, 0.4],
    perturbation_factor=0.1,
    learning_rate=0.1,
    perturbation_decay=0.6
)

result = spsa.minimize(
    objective_fn=lambda x: vqe_energy(x, hamiltonian),
    initial_parameters=[0.1, 0.2, 0.3, 0.4]
)

print(f"Optimal parameters: {result.x}")
print(f"Optimal value: {result.fun:.6f}")
print(f"Function evaluations: {result.nfev}")
print(f"Converged: {result.success}")
```

## Benchmarking and Analysis

### Quantum Advantage Analysis

```python
from quantum_optimization import AdvantageAnalyzer, BenchmarkSuite

# Analyze potential quantum advantage
analyzer = AdvantageAnalyzer()

# Generate benchmark problems
suite = BenchmarkSuite(
    problem_classes=["maxcut", "tsp", "portfolio", "graph_coloring"],
    sizes=[4, 8, 12, 16, 20],
    instances_per_size=10
)

results = analyzer.analyze(
    quantum_solver="qaoa_p3",
    classical_solvers=["greedy", "simulated_annealing", "gurobi"],
    benchmark_suite=suite,
    time_budget=100.0,
    significance_level=0.05
)

for problem_class, class_results in results.items():
    print(f"\n{problem_class}:")
    print(f"  Quantum avg: {class_results.quantum_avg:.4f}")
    print(f"  Classical best: {class_results.classical_best:.4f}")
    print(f"  Advantage ratio: {class_results.advantage_ratio:.4f}")
    print(f"  Statistical significance: {class_results.significant}")
    print(f"  Problem sizes with advantage: {class_results.advantage_sizes}")
```

### Solution Quality Distribution Analysis

```python
from quantum_optimization import SolutionDistribution, QualityAnalyzer

# Analyze distribution of quantum solutions
analyzer = QualityAnalyzer()

distribution = analyzer.analyze_distribution(
    solver="qaoa",
    problem=problem,
    num_runs=100,
    shots_per_run=1024
)

print(f"Mean solution quality: {distribution.mean:.4f}")
print(f"Std deviation: {distribution.std:.4f}")
print(f"Best quality: {distribution.best:.4f}")
print(f"Worst quality: {distribution.worst:.4f}")
print(f"Skewness: {distribution.skewness:.4f}")
print(f"Kurtosis: {distribution.kurtosis:.4f}")
print(f"Quality histogram: {distribution.histogram}")
```

## Constraint Handling Techniques

### Penalty-Based Constraints

```python
from quantum_optimization import PenaltyMethod, QuadraticProgram

qp = QuadraticProgram()
qp.add_binary_variables(["x0", "x1", "x2", "x3"])

# Objective: minimize x0 + x1 + x2 + x3
qp.objective.linear = {"x0": 1, "x1": 1, "x2": 1, "x3": 1}

# Constraint: x0 + x1 + x2 + x3 == 2
qp.add_constraint("x0 + x1 + x2 + x3 == 2", name="cardinality")

penalty = PenaltyMethod(
    constraint_type="equality",
    penalty_strength=5.0,
    adaptive_penalty=True,
    penalty_update_factor=1.5,
    max_penalty=100.0
)

penalized_qubo = penalty.apply(qp)
print(f"Penalty terms added: {penalized_qubo.num_penalty_terms}")
print(f"Total QUBO terms: {penalized_qubo.num_terms}")
print(f"Optimal penalty strength: {penalty.optimal_strength:.4f}")
```

### Constrained QAOA (CQAOA)

```python
from quantum_optimization import CQAOA, MaxCutProblem

# CQAOA with constraint-preserving mixer
problem = MaxCutProblem(
    num_nodes=6,
    edges=[(0,1,1.0), (1,2,1.5), (2,3,1.0), (3,4,2.0), (4,5,1.0), (0,5,0.5)],
    constraint="equal_partition"
)

cqaoa = CQAOA(
    p_layers=3,
    mixer_type="xy_mixer",
    constraint_enforcement="hard",
    optimizer="COBYLA",
    maxiter=200
)

result = cqaoa.solve(problem)
print(f"Best cut: {result.best_value}")
print(f"Constraint satisfied: {result.constraint_satisfied}")
print(f"Penalty cost: {result.penalty_cost:.6f}")
```

## Quantum Machine Learning Applications

### Quantum Neural Network Training

```python
from quantum_optimization import QuantumNeuralNetwork, ClassificationProblem

# Train a quantum neural network
qnn = QuantumNeuralNetwork(
    num_qubits=4,
    num_layers=3,
    encoding="angle",
    ansatz="hardware_efficient",
    classifier=True,
    output_qubit=0
)

# Generate classification dataset
dataset = ClassificationProblem(
    num_features=4,
    num_samples=200,
    num_classes=2,
    separation=0.5
)

result = qnn.train(
    dataset=dataset,
    optimizer="adam",
    learning_rate=0.01,
    batch_size=32,
    epochs=100,
    shots=1024
)

print(f"Training accuracy: {result.train_accuracy:.4f}")
print(f"Test accuracy: {result.test_accuracy:.4f}")
print(f"Loss curve: {result.loss_history[:5]}")
print(f"Parameters: {result.num_parameters}")
```

### Quantum Kernel Methods

```python
from quantum_optimization import QuantumKernelSVM, FeatureMap

# Quantum kernel for classification
feature_map = FeatureMap(
    type="zz_feature_map",
    num_qubits=4,
    reps=2,
    entanglement="full"
)

kernel_svm = QuantumKernelSVM(
    feature_map=feature_map,
    C=1.0,
    kernel="quantum",
    shots=1024,
    optimization_level=2
)

result = kernel_svm.fit(X_train, y_train)
print(f"Training accuracy: {result.train_accuracy:.4f}")
print(f"Support vectors: {result.num_support_vectors}")
print(f"Kernel matrix condition: {result.kernel_condition:.4f}")
print(f"Quantum advantage estimated: {result.quantum_advantage:.4f}")
```

## Problem Decomposition Strategies

### Divide-and-Conquer for Large Problems

```python
from quantum_optimization import DivideConquerSolver, MaxCutProblem

# Solve large problems by decomposition
problem = MaxCutProblem(
    num_nodes=20,
    edges=[(i, (i+1) % 20, 1.0) for i in range(20)]
)

solver = DivideConquerSolver(
    max_subproblem_size=6,
    decomposition_method="spectral_bisection",
    overlap_size=2,
    merge_method="dp_combination",
    quantum_subproblem_solver="qaoa_p2",
    classical_fallback="gurobi"
)

result = solver.solve(problem)
print(f"Best value: {result.best_value}")
print(f"Subproblems solved: {result.num_subproblems}")
print(f"Total quantum circuits: {result.total_quantum_circuits}")
print(f"Merge overhead: {result.merge_time:.2f} s")
```

### Cut-Based Decomposition

```python
from quantum_optimization import CutBasedDecomposition, GraphProblem

graph = GraphProblem(
    num_nodes=16,
    edges=[(i, (i+1) % 16, 1.0) for i in range(16)]
)

decomposer = CutBasedDecomposition(
    max_qubits_per_fragment=6,
    num_cuts=4,
    cut_strategy="greedy",
    overlap_fraction=0.2
)

fragments = decomposer.decompose(graph)
print(f"Number of fragments: {len(fragments)}")
for i, frag in enumerate(fragments):
    print(f"  Fragment {i}: {frag.num_qubits} qubits, "
          f"{frag.num_edges} edges")

# Execute fragments and combine
combined_result = decomposer.execute_and_combine(
    fragments,
    quantum_solver="qaoa_p2",
    shots=1024
)
print(f"Combined result: {combined_result.best_value:.4f}")
```
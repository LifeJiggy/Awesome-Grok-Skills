---
name: "quantum-optimization"
category: "quantum-computing"
version: "2.0.0"
tags: ["quantum-computing", "quantum-optimization", "qaoa", "vqe", "annealing", "maxcut", "portfolio", "tsp"]
---

# Quantum Optimization

## Overview

The quantum-optimization module provides comprehensive tools for solving combinatorial and continuous optimization problems using quantum algorithms. It implements QAOA (Quantum Approximate Optimization Algorithm), VQE-based optimization, quantum annealing simulation, variational quantum eigensolver extensions, QUBO (Quadratic Unconstrained Binary Optimization) formulation, and problem-specific encodings for MaxCut, Traveling Salesman Problem (TSP), portfolio optimization, graph coloring, knapsack, and scheduling problems.

This module is designed for operations researchers, financial engineers, logistics planners, and quantum computing practitioners who need to formulate real-world optimization problems as quantum circuits, solve them on simulators or real hardware, and compare quantum solutions with classical baselines. The module includes automated problem encoding, constraint handling via penalty methods, and solution post-processing with local search improvement.

The optimization engine supports both gate-model (QAOA, VQE) and annealing-based approaches, with configurable classical optimizers, mixer operators, and constraint encoding strategies. It provides benchmarking tools to compare quantum optimization against classical solvers (greedy, simulated annealing, branch-and-bound) with quality and time metrics, enabling informed decisions about when quantum optimization provides practical advantage.

## Core Capabilities

- **QAOA Implementation**: Full QAOA with configurable number of layers (p), mixer operators (standard X-mixer, constrained mixers, XY-mixer), and classical optimizers (COBYLA, L-BFGS-B, SPSA, Nelder-Mead). Includes warm-start and recursive QAOA variants.
- **MaxCut Solver**: Exact and approximate MaxCut on arbitrary graphs with performance guarantees — QAOA achieves 0.878 approximation ratio for MaxCut on worst-case graphs. Supports weighted and unweighted graphs.
- **Traveling Salesman Problem (TSP)**: Quantum encoding of TSP using QUBO formulation with penalty-based constraint enforcement for tour validity. Includes 2-opt local search post-processing.
- **Portfolio Optimization**: Markowitz mean-variance portfolio optimization with cardinality constraints, sector limits, and transaction cost modeling. Supports both QAOA and VQE-based approaches.
- **QUBO Formulation Engine**: Convert any combinatorial optimization problem to QUBO form with automatic penalty parameter selection and constraint encoding. Includes QUBO validation and verification utilities.
- **Quantum Annealing Simulation**: Simulate quantum annealing dynamics with configurable temperature schedules, transverse field profiles, and diabatic transition modeling. Supports reverse annealing and hybrid classical-quantum annealing.
- **Graph Coloring**: Minimum vertex coloring using QUBO encoding with penalty terms for adjacency conflicts. Supports k-colorability testing and chromatic number estimation.
- **Knapsack Problem**: 0/1 and bounded knapsack with quantum encoding using multi-qubit penalty encoding. Supports multi-dimensional knapsack with resource constraints.
- **Job-Shop Scheduling**: Resource-constrained scheduling with quantum-encoded precedence and capacity constraints. Includes makespan minimization and tardiness optimization.
- **Constraint Satisfaction**: General CSP solver via quantum penalty methods with adaptive penalty tuning. Supports all-different, at-most, and custom constraint types.
- **Benchmark Suite**: Compare quantum optimization against classical solvers (greedy, simulated annealing, exact branch-and-bound) with quality and time metrics. Includes approximation ratio computation and convergence analysis.
- **Solution Post-Processing**: Decode binary quantum solutions back to problem-specific formats with constraint repair and local search improvement. Includes feasibility checking and solution validation.

## Usage Examples

### MaxCut with QAOA

```python
from quantum_optimization import (
    OptimizationEngine, ProblemType, QAOAConfig,
    GraphInput, OptimizerType
)

# Define a graph
graph = GraphInput(
    num_nodes=8,
    edges=[(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7), (7,0), (0,3), (1,5)],
    weights=[1.0, 2.0, 1.5, 1.0, 2.5, 1.0, 1.5, 2.0, 1.0, 1.5]
)

qaoa_config = QAOAConfig(
    num_layers=4,
    mixer_type="standard",
    optimizer=OptimizerType.COBYLA,
    max_iterations=200,
    convergence_threshold=1e-6
)

engine = OptimizationEngine(
    problem_type=ProblemType.MAX_CUT,
    graph=graph
)

result = engine.solve_qaoa(config=qaoa_config)
print(f"Cut value: {result.optimal_value}")
print(f"Partition: {result.solution}")
print(f"Approximation ratio: {result.approximation_ratio:.4f}")
print(f"Convergence iterations: {result.convergence_iterations}")
```

### Portfolio Optimization

```python
from quantum_optimization import (
    OptimizationEngine, ProblemType, PortfolioConfig,
    MarketData
)

market_data = MarketData(
    expected_returns=[0.08, 0.12, 0.06, 0.15, 0.10],
    covariance_matrix=[
        [0.04, 0.006, 0.002, 0.008, 0.004],
        [0.006, 0.09, 0.005, 0.012, 0.007],
        [0.002, 0.005, 0.01, 0.003, 0.002],
        [0.008, 0.012, 0.003, 0.16, 0.01],
        [0.004, 0.007, 0.002, 0.01, 0.06],
    ],
    asset_names=["AAPL", "GOOGL", "BND", "TSLA", "MSFT"]
)

portfolio_config = PortfolioConfig(
    num_assets=5,
    budget_constraint=3,  # max 3 assets
    risk_aversion=0.5,
    min_weight=0.0,
    max_weight=1.0,
    sector_limits={"tech": 2}
)

engine = OptimizationEngine(
    problem_type=ProblemType.PORTFOLIO,
    market_data=market_data
)

result = engine.solve_qaoa(config=portfolio_config)
print(f"Expected return: {result.metadata['expected_return']:.4f}")
print(f"Portfolio risk: {result.metadata['portfolio_risk']:.4f}")
print(f"Selected assets: {result.metadata['selected_assets']}")
```

### Traveling Salesman Problem

```python
from quantum_optimization import OptimizationEngine, ProblemType, TSPConfig

tsp_config = TSPConfig(
    num_cities=6,
    distance_matrix=[
        [0, 10, 15, 20, 25, 30],
        [10, 0, 35, 25, 20, 15],
        [15, 35, 0, 30, 20, 25],
        [20, 25, 30, 0, 15, 10],
        [25, 20, 20, 15, 0, 35],
        [30, 15, 25, 10, 35, 0],
    ],
    penalty_weight=10.0,
    start_city=0
)

engine = OptimizationEngine(problem_type=ProblemType.TSP)
result = engine.solve_qaoa(config=tsp_config)
print(f"Tour: {result.solution}")
print(f"Total distance: {result.optimal_value}")
```

### QUBO Formulation and Solving

```python
from quantum_optimization import QUBOFormulator, QUBOSolver

# Define a custom problem as QUBO
formulator = QUBOFormulator(num_variables=6)

# Add objective terms: minimize x0 + 2*x1 - x2 + x3*x4
formulator.add_linear_term(0, 1.0)
formulator.add_linear_term(1, 2.0)
formulator.add_linear_term(2, -1.0)
formulator.add_quadratic_term(3, 4, 1.5)

# Add constraint: x0 + x1 + x2 = 1 (exactly one selected)
formulator.add_equality_constraint([0, 1, 2], [1, 1, 1], 1, penalty=10.0)

# Convert to QUBO matrix
Q = formulator.get_qubo_matrix()
print(f"QUBO matrix size: {len(Q)}x{len(Q[0])}")

# Solve
solver = QUBOSolver(method="bruteforce")
solution = solver.solve(Q)
print(f"Optimal assignment: {solution.assignment}")
print(f"Optimal value: {solution.value}")
```

### Quantum Annealing Simulation

```python
from quantum_optimization import AnnealingSimulator, AnnealingSchedule

schedule = AnnealingSchedule(
    total_time=100.0,
    num_steps=500,
    initial_temperature=10.0,
    final_temperature=0.01,
    cooling_schedule="exponential"
)

simulator = AnnealingSimulator(
    num_qubits=8,
    schedule=schedule
)

# Solve a QUBO via simulated annealing
Q = [[-1 if i == j else 0.5 for j in range(8)] for i in range(8)]
result = simulator.anneal(Q)
print(f"Best solution: {result.best_state}")
print(f"Best energy: {result.best_energy}")
print(f"Annealing time: {result.annealing_time_ms:.1f} ms")
```

### Constraint Satisfaction

```python
from quantum_optimization import OptimizationEngine, ProblemType, CSPConfig

csp_config = CSPConfig(
    num_variables=9,
    domain_size=3,
    constraints=[
        {"type": "all_different", "variables": [0, 1, 2]},
        {"type": "all_different", "variables": [3, 4, 5]},
        {"type": "all_different", "variables": [6, 7, 8]},
        {"type": "all_different", "variables": [0, 3, 6]},
        {"type": "all_different", "variables": [1, 4, 7]},
        {"type": "all_different", "variables": [2, 5, 8]},
    ],
    penalty_weight=20.0
)

engine = OptimizationEngine(problem_type=ProblemType.CSP)
result = engine.solve_qaoa(config=csp_config)
print(f"Sudoku solution: {result.solution}")
print(f"All constraints satisfied: {result.metadata['constraints_satisfied']}")
```

## Architecture

```
quantum_optimization/
  __init__.py
  problems/
    maxcut.py               # MaxCut formulation and encoding
    tsp.py                  # Traveling Salesman Problem
    portfolio.py            # Portfolio optimization
    graph_coloring.py       # Graph coloring
    knapsack.py             # 0/1 and bounded knapsack
    scheduling.py           # Job-shop scheduling
    csp.py                  # Constraint satisfaction
  qaoa/
    qaoa_engine.py          # Core QAOA implementation
    mixers.py               # Standard, XY, constrained mixers
    warm_start.py           # Warm-start QAOA
    recursive_qaoa.py       # Recursive QAOA
  qubo/
    formulator.py           # QUBO formulation engine
    solver.py               # QUBO solvers (exact, heuristic)
    normalizer.py           # QUBO coefficient scaling
    verifier.py             # Solution verification
  annealing/
    simulator.py            # Quantum annealing simulation
    schedule.py             # Temperature schedules
    reverse_annealing.py    # Reverse annealing
  classical/
    greedy.py               # Greedy heuristic solver
    simulated_annealing.py  # Classical simulated annealing
    branch_bound.py         # Exact branch-and-bound
    local_search.py         # 2-opt, 3-opt local search
  benchmarks/
    comparison.py           # Quantum vs classical comparison
    convergence.py          # Convergence analysis
    quality_metrics.py      # Approximation ratio, gap analysis
  post_processing/
    decoder.py              # Binary-to-problem decoding
    repair.py               # Constraint repair
    local_improvement.py    # Post-solution local search
```

## Best Practices

1. **QAOA layer count**: Start with p=2-3 layers. Increase only if convergence stalls. For MaxCut, p >= 3 provides 0.878+ approximation. For constrained problems, p=5-10 is typical. Beyond p=10, barren plateaus become problematic.

2. **Penalty parameter tuning**: Start with penalty = 10x the objective scale. Use adaptive penalty schedules: increase penalty during optimization if constraints are violated, decrease if progress stalls. Lagrangian relaxation with dual variable updates provides better convergence.

3. **Mixer selection**: Use standard X-mixer for unconstrained problems. Use XY-mixer or Grover mixer for constrained optimization (preserves constraint subspace). Constrained mixers reduce search space dramatically and improve convergence.

4. **Classical optimizer choice**: COBYLA for noisy circuits (gradient-free, robust). L-BFGS-B for noiseless (gradient-based, fast convergence). SPSA for real hardware (robust to noise, 2 gradient evaluations per iteration). Nelder-Mead for small parameter spaces.

5. **Initial state**: Start from a classical feasible solution when possible. For QAOA, the problem Hamiltonian's ground state in the Z-basis is a common starting point. Warm-start QAOA uses classical solutions to initialize, improving convergence by 2-5x.

6. **QUBO scaling**: Scale all QUBO coefficients to [-1, 1] range before solving. Unscaled QUBOs cause numerical instability and poor convergence. Use the QUBO normalizer utility for automatic scaling.

7. **Annealing schedule**: For quantum annealing simulation, use exponential cooling: T(t) = T_0 * exp(-t/tau). Set tau based on problem size: tau = O(N^2) for N variables. Linear schedules work well for simple problems.

8. **Solution quality**: Always compare quantum solutions with classical baselines (greedy, local search). For small instances (N <= 20), use exact solvers for validation. Track approximation ratio across problem sizes to identify quantum advantage regimes.

9. **Constraint handling**: Encode constraints as penalty terms, not hard constraints. Adaptive penalty with Lagrangian relaxation provides better convergence than fixed penalties. Verify constraint satisfaction independently after optimization.

10. **Reproducibility**: Set optimizer seed for deterministic results. Store QUBO formulation for auditability. Log convergence history for debugging. Record all hyperparameters for result reproducibility.

## Performance Considerations

- **QAOA circuit depth**: Each QAOA layer adds 2 Hamiltonian evolution circuits. For p layers, circuit depth scales as O(p * n) where n is the number of qubits. Keep p * n below hardware connectivity limits.
- **Classical optimizer overhead**: Each QAOA iteration requires 2*n_evaluation circuits for gradient estimation (SPSA) or O(n) for finite differences. Budget 100-500 iterations for convergence, each taking seconds to minutes.
- **QUBO size scaling**: QUBO matrix size is n x n where n is the number of binary variables. For n > 1000, use sparse QUBO representations and specialized solvers (tabu search, simulated annealing).
- **Annealing time**: Quantum annealing simulation with T steps takes O(T * n^2) time for n-qubit problems. Use parallel tempering for faster convergence on rugged energy landscapes.
- **Penalty overhead**: Large penalty parameters increase the energy scale, making optimization harder. Start with moderate penalties and increase only as needed. Target penalty ratio of 10-100x the objective scale.
- **Noise impact**: QAOA is sensitive to gate noise. For depolarizing noise rate p, the approximation ratio degrades as O(1 - p * n * p_depth). Use error mitigation for circuits with > 100 gates.

## Security Considerations

- **Optimization data sensitivity**: Portfolio optimization and scheduling data may contain sensitive business information. Protect optimization inputs and outputs with appropriate access controls and encryption.
- **Quantum advantage claims**: Be cautious about claiming quantum advantage for optimization problems. Classical solvers are highly optimized and may outperform quantum approaches for many practical problem sizes. Always benchmark rigorously.
- **Random seed security**: If optimization results influence security-sensitive decisions (e.g., resource allocation, scheduling), ensure random seeds are unpredictable and properly seeded from hardware random number generators.
- **Solution verification**: Always verify that quantum optimization solutions satisfy all constraints. Infeasible solutions can have severe consequences in production scheduling or financial optimization.
- **Hybrid classical-quantum security**: When using cloud quantum backends for optimization, be aware that problem structure and solutions may be visible to the cloud provider. Use local simulators for sensitive optimization problems.

## Related Modules

- **quantum-algorithms** — VQE and QPE algorithms that drive optimization subroutines; the algorithmic backbone for variational optimization and eigenvalue-based solvers.
- **quantum-simulation** — Hamiltonian simulation methods used to simulate annealing dynamics and quantum walks for optimization. Includes noise modeling for realistic annealing simulation.
- **quantum-error-correction** — Error correction codes that protect optimization circuits on real hardware; essential for scaling to large problem instances beyond NISQ limitations.
- **quantum-cryptography** — Quantum-secure protocols for distributing optimization solutions and problem data in multi-party settings. Includes secure multi-party optimization.

## References

- Farhi, E., Goldstone, J., & Gutmann, S. (2014). A quantum approximate optimization algorithm. *arXiv:1411.4028*.
- Peruzzo, A. et al. (2014). A variational eigenvalue solver on a photonic quantum processor. *Nature Communications*, 5, 4213.
- Kadowaki, T. & Nishimori, H. (1998). Quantum annealing in the transverse Ising model. *Physical Review E*, 58(5), 5355.
- Lucas, A. (2014). Ising formulations of many NP problems. *Frontiers in Physics*, 2, 5.
- Brandhofer, S. et al. (2022). Benchmarking the performance of QAOA with warm-starting. *Quantum Science and Technology*, 8(3), 034001.
- Willsch, M. & Willsch, D. (2020). Benchmarking the quantum approximate optimization algorithm. *Quantum Information Processing*, 19(7), 197.

## Advanced Configuration

### QAOA Advanced Configuration

```python
from quantum_optimization import QAOAConfig, MixerType, ConstraintHandling

# Advanced QAOA configuration
qaoa_config = QAOAConfig(
    num_layers=6,
    mixer_type=MixerType.XY,
    optimizer="cobyla",
    max_iterations=300,
    convergence_threshold=1e-6,
    initial_point="warm_start",
    constraint_handling=ConstraintHandling.PENALTY,
    penalty_strength=10.0,
    adaptive_penalty=True,
    callback=convergence_callback,
    gradient_method="parameter_shift",
    gradient_shots=1024,
    parallel_evaluation=True,
)

engine = OptimizationEngine(
    problem_type=ProblemType.MAX_CUT,
    graph=graph,
    qaoa_config=qaoa_config,
)
```

### QUBO Advanced Configuration

```python
from quantum_optimization import QUBOFormulator, QUBOSolver, ScalingStrategy

# Advanced QUBO configuration
formulator = QUBOFormulator(
    num_variables=12,
    scaling=ScalingStrategy.ADAPTIVE,
    constraint_encoding="penalty",
    auto_scale=True,
    scale_range=(-1.0, 1.0),
)

# Add complex constraints
formulator.add_equality_constraint(
    variables=[0, 1, 2],
    coefficients=[1, 1, 1],
    target=1,
    penalty=20.0,
)

formulator.add_inequality_constraint(
    variables=[3, 4, 5],
    coefficients=[2, 1, 3],
    upper_bound=10,
    penalty=15.0,
)

Q = formulator.get_qubo_matrix()
solver = QUBOSolver(method="simulated_annealing")
solution = solver.solve(Q)
```

### Annealing Schedule Configuration

```python
from quantum_optimization import AnnealingSchedule, CoolingProfile

schedule = AnnealingSchedule(
    total_time=200.0,
    num_steps=1000,
    initial_temperature=20.0,
    final_temperature=0.001,
    cooling=CoolingProfile.COSINE,
    reannealing_interval=100,
    reannealing_factor=0.8,
    temperature_limits=(0.001, 20.0),
)

simulator = AnnealingSimulator(
    num_qubits=10,
    schedule=schedule,
    parallel_tempering=True,
    num_replicas=4,
)
```

## Architecture Patterns

### Optimization Pipeline Pattern

```python
from quantum_optimization import OptimizationPipeline, PipelineStage

pipeline = OptimizationPipeline(stages=[
    PipelineStage(
        name="problem_formulation",
        type="classical",
        processor=lambda x: formulate_qubo(x),
    ),
    PipelineStage(
        name="encoding",
        type="quantum",
        processor=lambda x: encode_qubits(x),
    ),
    PipelineStage(
        name="optimization",
        type="quantum",
        processor=lambda x: run_qaoa(x),
    ),
    PipelineStage(
        name="decoding",
        type="classical",
        processor=lambda x: decode_solution(x),
    ),
    PipelineStage(
        name="post_processing",
        type="classical",
        processor=lambda x: local_search(x),
    ),
])

result = pipeline.execute(problem)
```

### Hybrid Classical-Quantum Pattern

```python
from quantum_optimization import HybridOptimizer, ClassicalPreprocessor

# Classical preprocessor
preprocessor = ClassicalPreprocessor(
    strategy="relaxation",
    max_classical_variables=20,
    decomposition_method="gurobi",
)

# Hybrid optimization
hybrid = HybridOptimizer(
    classical_preprocessor=preprocessor,
    quantum_solver="qaoa",
    post_processor="local_search",
    switching_threshold=0.01,
)

result = hybrid.optimize(problem)
print(f"Classical preprocessing reduced variables from {problem.n_variables} to {result.reduced_variables}")
print(f"Quantum optimization improved by {result.improvement_ratio:.2%}")
```

### Benchmark Comparison Pattern

```python
from quantum_optimization import BenchmarkSuite, ClassicalSolver

benchmark = BenchmarkSuite(
    quantum_solvers=["qaoa", "vqe", "annealing"],
    classical_solvers=[
        ClassicalSolver("greedy"),
        ClassicalSolver("simulated_annealing"),
        ClassicalSolver("branch_and_bound"),
    ],
    metrics=["quality", "time", "approximation_ratio"],
    num_trials=10,
)

results = benchmark.run(problems)
print(f"Best quantum solver: {results.best_quantum}")
print(f"Best classical solver: {results.best_classical}")
print(f"Quantum advantage regime: {results.advantage_range}")
```

## Integration Guide

### Gurobi Integration

```python
from quantum_optimization import GurobiAdapter, QUBOFormulator

adapter = GurobiAdapter()

# Convert Gurobi model to QUBO
gurobi_model = adapter.create_model(problem)
Q = adapter.to_qubo(gurobi_model)

# Solve QUBO
solver = QUBOSolver(method="bruteforce")
solution = solver.solve(Q)

# Convert back to Gurobi solution
gurobi_solution = adapter.from_qubo_solution(solution, problem)
print(f"Optimal value: {gurobi_solution.objective_value}")
```

### CPLEX Integration

```python
from quantum_optimization import CPLEXAdapter

adapter = CPLEXAdapter()

# Convert CPLEX problem to QUBO
cplex_problem = adapter.create_problem(problem)
Q = adapter.to_qubo(cplex_problem)

# Solve with quantum solver
solver = QUBOSolver(method="simulated_annealing")
solution = solver.solve(Q)

# Convert back to CPLEX format
cplex_solution = adapter.from_qubo_solution(solution, problem)
```

## Performance Optimization

### Parallel QAOA Evaluation

```python
from quantum_optimization import ParallelQAOA

parallel_qaoa = ParallelQAOA(
    n_workers=8,
    batch_size=50,
    backend="aer_simulator",
)

# Run multiple QAOA instances in parallel
results = parallel_qaoa.run(
    problem=problem,
    num_instances=100,
    parameter_ranges={
        "num_layers": [2, 3, 4, 5],
        "mixer_type": ["standard", "xy"],
    },
)

print(f"Best result: {results.best}")
print(f"Total time: {results.total_time_ms:.1f} ms")
print(f"Throughput: {results.problems_per_second:.1f} problems/s")
```

### QUBO Solver Optimization

```python
from quantum_optimization import QUBOOptimizer

optimizer = QUBOOptimizer(
    strategy="multi_start",
    num_starts=10,
    local_search="2opt",
    parallel=True,
)

optimized_solution = optimizer.optimize(Q)
print(f"Improvement over initial: {optimized_solution.improvement:.2%}")
print(f"Local search improvements: {optimized_solution.local_improvements}")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. QAOA Not Converging

**Symptom**: Cost function oscillates without improvement

**Solution**:
```python
# Increase layers
qaoa_config.num_layers = 6

# Use warm start
qaoa_config.initial_point = "warm_start"

# Use better optimizer
qaoa_config.optimizer = "l-bfgs-b"
```

#### 2. QUBO Scaling Issues

**Symptom**: Numerical instability, poor solutions

**Solution**:
```python
# Scale QUBO coefficients
formulator.scaling = ScalingStrategy.ADAPTIVE
formulator.scale_range = (-1.0, 1.0)

# Use penalty tuning
formulator.auto_scale = True
formulator.penalty_strength = 10.0
```

#### 3. Annealing Stuck in Local Minima

**Symptom**: Solution quality poor, high energy

**Solution**:
```python
# Use parallel tempering
simulator.parallel_tempering = True
simulator.num_replicas = 4

# Increase annealing time
schedule.total_time = 500.0

# Use reannealing
schedule.reannealing_interval = 100
```

## API Reference

### Core Classes

#### `OptimizationEngine`
```python
class OptimizationEngine:
    def __init__(self, problem_type: ProblemType, **kwargs) -> None: ...
    def solve_qaoa(self, config: QAOAConfig) -> OptimizationResult: ...
    def solve_vqe(self, config: VQEConfig) -> OptimizationResult: ...
    def solve_annealing(self, config: AnnealingConfig) -> OptimizationResult: ...
```

## Data Models

### Optimization Result Schema

```json
{
  "problem": "maxcut",
  "status": "success",
  "optimal_value": 12,
  "solution": [0, 1, 0, 1, 0, 1, 0, 1],
  "approximation_ratio": 0.95,
  "convergence_iterations": 50,
  "execution_time_ms": 125.3,
  "circuit_depth": 45
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY quantum_optimization/ /app/quantum_optimization/
WORKDIR /app

ENV QO_BACKEND=aer_simulator
ENV QO_OPTIMIZATION_LEVEL=2

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from quantum_optimization import health_check; health_check()"

CMD ["python", "-m", "quantum_optimization.server"]
```

## Monitoring & Observability

### Metrics Collection

```python
from quantum_optimization import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("qo_cost_value", type="gauge")
collector.register_metric("qo_approximation_ratio", type="gauge")
collector.register_metric("qo_circuit_depth", type="gauge")
collector.register_metric("qo_execution_time", type="histogram")

collector.set("qo_cost_value", result.optimal_value)
collector.set("qo_approximation_ratio", result.approximation_ratio)
collector.set("qo_circuit_depth", result.circuit_depth)
collector.observe("qo_execution_time", exec_time_ms)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from quantum_optimization import OptimizationEngine, ProblemType

class TestQAOA:
    def setup_method(self):
        self.graph = GraphInput(num_nodes=4, edges=[(0,1), (1,2), (2,3), (3,0)])
    
    def test_maxcut_qaoa(self):
        engine = OptimizationEngine(problem_type=ProblemType.MAX_CUT, graph=self.graph)
        result = engine.solve_qaoa(QAOAConfig(num_layers=3))
        assert result.optimal_value >= 3
        assert result.approximation_ratio >= 0.878
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API
- **Added**: XY-mixer support
- **Added**: Warm-start QAOA
- **Improved**: 2x faster convergence
- **Fixed**: Penalty tuning issues

## Glossary

| Term | Definition |
|------|------------|
| **QAOA** | Quantum Approximate Optimization Algorithm |
| **QUBO** | Quadratic Unconstrained Binary Optimization |
| **MaxCut** | Partition graph to maximize edge cuts |
| **Approximation Ratio** | Quality of solution vs optimal |
| **Penalty Method** | Encode constraints as energy penalties |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/quantum-optimization.git
cd quantum-optimization
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Quantum Optimization Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

*Last updated: 2024-01-15*
*Version: 2.0.0*

## Advanced Patterns

### Problem Encoding Patterns

```python
from quantum_optimization import ProblemEncoder, EncodingStrategy

encoder = ProblemEncoder(
    strategy=EncodingStrategy.QUBO,
    constraint_handling="penalty",
    penalty_strength=10.0,
)

# Encode problem
qubo = encoder.encode(
    problem=optimization_problem,
    variables=decision_variables,
    constraints=problem_constraints,
)

print(f"QUBO matrix size: {qubo.shape}")
print(f"Number of variables: {qubo.num_variables}")
```

### Solution Post-Processing Patterns

```python
from quantum_optimization import SolutionPostProcessor, PostProcessStrategy

post_processor = SolutionPostProcessor(
    strategy=PostProcessStrategy.LOCAL_SEARCH,
    max_iterations=100,
    improvement_threshold=0.01,
)

# Post-process solution
improved_solution = post_processor.process(
    solution=quantum_solution,
    problem=optimization_problem,
)

print(f"Original value: {quantum_solution.value:.4f}")
print(f"Improved value: {improved_solution.value:.4f}")
print(f"Improvement: {(improved_solution.value - quantum_solution.value):.4f}")
```

### Hybrid Optimization Patterns

```python
from quantum_optimization import HybridOptimizer, HybridStrategy

hybrid = HybridOptimizer(
    strategy=HybridStrategy.CLASSICAL_PREPROCESSING,
    classical_solver="gurobi",
    quantum_solver="qaoa",
    switching_threshold=0.01,
)

# Run hybrid optimization
result = hybrid.optimize(
    problem=optimization_problem,
    max_classical_time=60,
    max_quantum_time=120,
)

print(f"Classical preprocessing reduced variables from {problem.n_variables} to {result.reduced_variables}")
print(f"Quantum optimization improved by {result.improvement_ratio:.2%}")
```

### Constraint Satisfaction Patterns

```python
from quantum_optimization import ConstraintSatisfaction, SatisfactionStrategy

satisfier = ConstraintSatisfaction(
    strategy=SatisfactionStrategy.PENALTY_METHOD,
    adaptive_penalty=True,
    penalty_update_factor=1.5,
)

# Satisfy constraints
feasible_solution = satisfier.satisfy(
    solution=infeasible_solution,
    constraints=problem_constraints,
    max_iterations=100,
)

print(f"Feasibility score: {feasible_solution.feasibility_score:.4f}")
print(f"Constraint violations: {feasible_solution.violations}")
```

### Benchmarking Patterns

```python
from quantum_optimization import BenchmarkSuite, BenchmarkStrategy

benchmark = BenchmarkSuite(
    strategy=BenchmarkStrategy.COMPARATIVE,
    quantum_solvers=["qaoa", "vqe", "annealing"],
    classical_solvers=["greedy", "simulated_annealing", "branch_bound"],
    metrics=["quality", "time", "approximation_ratio"],
    num_trials=10,
)

# Run benchmark
results = benchmark.run(problems)
print(f"Best quantum solver: {results.best_quantum}")
print(f"Best classical solver: {results.best_classical}")
print(f"Quantum advantage regime: {results.advantage_range}")
```

### Portfolio Optimization Patterns

```python
from quantum_optimization import PortfolioOptimizer, PortfolioStrategy

optimizer = PortfolioOptimizer(
    strategy=PortfolioStrategy.MEAN_VARIANCE,
    risk_aversion=0.5,
    cardinality_constraint=5,
    sector_limits={"tech": 2, "finance": 1},
)

# Optimize portfolio
portfolio = optimizer.optimize(
    expected_returns=returns,
    covariance_matrix=covariance,
    budget=1000000,
)

print(f"Expected return: {portfolio.expected_return:.4f}")
print(f"Portfolio risk: {portfolio.risk:.4f}")
print(f"Sharpe ratio: {portfolio.sharpe_ratio:.4f}")
print(f"Selected assets: {portfolio.selected_assets}")
```

### Scheduling Optimization Patterns

```python
from quantum_optimization import Scheduler, ScheduleStrategy

scheduler = Scheduler(
    strategy=ScheduleStrategy.JOB_SHOP,
    num_machines=5,
    num_jobs=20,
    objective="makespan",
)

# Optimize schedule
schedule = scheduler.optimize(
    jobs=job_list,
    machines=machine_list,
    constraints=schedule_constraints,
)

print(f"Makespan: {schedule.makespan}")
print(f"Machine utilization: {schedule.utilization:.1%}")
print(f"Schedule: {scheduleassignments}")
```

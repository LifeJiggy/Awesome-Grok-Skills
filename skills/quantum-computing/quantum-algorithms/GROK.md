---
name: "quantum-algorithms"
category: "quantum-computing"
version: "2.0.0"
tags: ["quantum-computing", "quantum-algorithms", "qiskit", "shor", "grover", "vqe", "qaoa", "hhl", "qpe"]
---

# Quantum Algorithms

## Overview

The quantum-algorithms module provides a comprehensive toolkit for implementing, simulating, and benchmarking foundational and advanced quantum algorithms. It covers the full spectrum from textbook classics (Deutsch-Jozsa, Bernstein-Vazirani, Simon's) to near-term variational algorithms (VQE, QAOA), Shor's factoring algorithm, Grover's search, quantum phase estimation, HHL for linear systems, quantum walks, and amplitude estimation. Each algorithm is wrapped in a configurable engine class that abstracts circuit construction, execution on simulators or real hardware, result interpretation, and error mitigation.

This module is designed for researchers, educators, and developers who need reproducible quantum algorithm implementations with full type safety, pluggable backends, and structured output. It integrates with Qiskit primitives and supports both statevector simulation and shot-based noisy simulation. The engine supports multiple backends (statevector, Aer, IBM Quantum, AWS Braket) and provides a unified API for circuit construction, transpilation, execution, and result analysis.

The module also includes algorithm comparison tools, resource estimation helpers, and a benchmarking suite that enables systematic evaluation of algorithm performance across different hardware topologies, noise levels, and qubit counts. All implementations follow best practices from the quantum computing community and are validated against classical exact solutions for small problem instances.

## Core Capabilities

- **Deutsch-Jozsa Algorithm**: Determine if a function is constant or balanced with a single query — the canonical demonstration of quantum parallelism. Supports arbitrary oracle construction and multi-qubit function evaluation.
- **Bernstein-Vazirani Algorithm**: Find a hidden bitstring s from an oracle that computes f(x) = s · x mod 2 — O(1) classical queries vs O(n) classical. Demonstrates the power of quantum interference for structured search problems.
- **Simon's Algorithm**: Discover a hidden period s of a 2-to-1 function — the quantum precursor to Shor's algorithm. Provides exponential speedup over classical period finding for the specific function class.
- **Grover's Search**: Unstructured search with quadratic speedup O(sqrt(N)) — amplitude amplification with configurable oracle and diffusion operators. Supports fixed-point Grover's and amplitude estimation variants.
- **Shor's Factoring Algorithm**: Integer factorization via quantum period finding — breaks RSA when run on fault-tolerant hardware. Includes modular exponentiation circuit construction and continued fraction analysis.
- **Quantum Phase Estimation (QPE**: Estimate eigenvalues of a unitary operator — core subroutine in Shor's, HHL, and many other algorithms. Supports both canonical and iterative QPE variants.
- **Variational Quantum Eigensolver (VQE)**: Hybrid classical-quantum algorithm for ground state energy estimation of molecular Hamiltonians. Includes UCCSD, ADAPT-VQE, and hardware-efficient ansatz options.
- **Quantum Approximate Optimization Algorithm (QAOA)**: Variational approach to combinatorial optimization problems (MaxCut, TSP, portfolio optimization) with configurable mixer operators and classical optimizers.
- **Harrow-Hassidim-Lloyd (HHL)**: Quantum linear systems solver with exponential speedup for sparse matrices. Includes condition number estimation and precision control via QPE register size.
- **Amplitude Estimation**: Quadratic speedup over Monte Carlo for estimating expectation values — applications in finance, risk analysis, and uncertainty quantification.
- **Quantum Walks**: Spatial search and graph traversal using discrete-time and continuous-time quantum walk operators. Applications in graph isomorphism and element distinctness.
- **Algorithm Benchmarking**: Compare algorithm performance across backends, noise levels, and qubit counts with structured metrics output. Includes circuit depth, gate count, and fidelity tracking.

## Usage Examples

### Deutsch-Jozsa Algorithm

```python
from quantum_algorithms import QuantumAlgorithmEngine, AlgorithmType, BackendConfig

# Configure for 4-qubit Deutsch-Jozsa
config = BackendConfig(
    num_qubits=4,
    shots=1024,
    backend="statevector_simulator"
)

engine = QuantumAlgorithmEngine(config=config)

# Define a balanced oracle (flips output for specific inputs)
result = engine.run_deutsch_jozsa(
    oracle_type="balanced",
    oracle_pattern=[0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1]
)

print(f"Result: {result.measurement_outcome}")  # "balanced"
print(f"Circuit depth: {result.circuit_depth}")
print(f"Execution time: {result.execution_time_ms:.1f} ms")
```

### Grover's Search Algorithm

```python
from quantum_algorithms import QuantumAlgorithmEngine, BackendConfig, GroverConfig

config = BackendConfig(num_qubits=5, shots=4096, backend="aer_simulator")
engine = QuantumAlgorithmEngine(config=config)

grover_cfg = GroverConfig(
    num_qubits=5,
    target_state="01101",
    num_iterations=3,  # optimal: floor(pi/4 * sqrt(2^n))
    auto_optimize=True
)

result = engine.run_grover(config=grover_cfg)
print(f"Found state: {result.found_state}")
print(f"Probability: {result.probability:.4f}")
print(f"Oracle calls: {result.oracle_calls}")
```

### Shor's Factoring Algorithm (Simulation Mode)

```python
from quantum_algorithms import QuantumAlgorithmEngine, BackendConfig

config = BackendConfig(num_qubits=12, shots=1, backend="statevector_simulator")
engine = QuantumAlgorithmEngine(config=config)

result = engine.run_shor(number_to_factor=15, num_qubits_used=8)
print(f"Factors: {result.factors}")           # [3, 5]
print(f"Period found: {result.period}")       # 4
print(f"QPE register size: {result.qpe_qubits}")
```

### VQE for Molecular Ground State

```python
from quantum_algorithms import QuantumAlgorithmEngine, BackendConfig, VQEConfig

config = BackendConfig(num_qubits=4, shots=8192, backend="aer_simulator")
engine = QuantumAlgorithmEngine(config=config)

vqe_config = VQEConfig(
    molecule="H2",
    bond_distance=0.735,  # Angstroms
    basis="sto-3g",
    optimizer="COBYLA",
    max_iterations=100,
    convergence_threshold=1e-6
)

result = engine.run_vqe(config=vqe_config)
print(f"Ground state energy: {result.ground_state_energy:.6f} Ha")
print(f"Exact energy: {result.exact_energy:.6f} Ha")
print(f"Chemical accuracy: {result.chemical_accuracy_mHartree:.3f} mHa")
```

### QAOA for MaxCut

```python
from quantum_algorithms import QuantumAlgorithmEngine, BackendConfig, QAOAConfig

config = BackendConfig(num_qubits=6, shots=4096, backend="aer_simulator")
engine = QuantumAlgorithmEngine(config=config)

qaoa_config = QAOAConfig(
    graph_edges=[(0,1), (1,2), (2,3), (3,4), (4,5), (5,0), (0,3)],
    num_layers=3,
    optimizer="L-BFGS-B",
    mixer="standard"
)

result = engine.run_qaoa(config=qaoa_config)
print(f"Cut value: {result.cut_value}")
print(f"Optimal partition: {result.partition}")
print(f"Approximation ratio: {result.approximation_ratio:.4f}")
```

### HHL Linear Systems Solver

```python
from quantum_algorithms import QuantumAlgorithmEngine, BackendConfig, HHLConfig

config = BackendConfig(num_qubits=8, shots=4096, backend="aer_simulator")
engine = QuantumAlgorithmEngine(config=config)

hhl_config = HHLConfig(
    matrix=[[4, 1], [1, 3]],
    vector=[1, 2],
    precision_qubits=4,
    eigenvalue_register_size=4
)

result = engine.run_hhl(config=hhl_config)
print(f"Solution: {result.solution_vector}")
print(f"Classical solution: {result.classical_reference}")
print(f"Fidelity: {result.solution_fidelity:.4f}")
```

## Architecture

```
quantum_algorithms/
  __init__.py
  engines/
    base_engine.py          # Abstract base class for all algorithm engines
    deutsch_jozsa.py        # Deutsch-Jozsa implementation
    bernstein_vazirani.py   # Bernstein-Vazirani implementation
    simon.py                # Simon's algorithm implementation
    grover.py               # Grover's search with amplitude amplification
    shor.py                 # Shor's factoring with QPE + classical post
    qpe.py                  # Quantum phase estimation (canonical + iterative)
    vqe.py                  # Variational quantum eigensolver
    qaoa.py                 # QAOA with configurable mixers
    hhl.py                  # HHL linear systems solver
    amplitude_estimation.py # Quantum amplitude estimation
    quantum_walks.py        # Discrete and continuous-time quantum walks
  oracles/
    oracle_builder.py       # Declarative oracle construction
    phase_oracles.py        # Phase oracle implementations
    amplitude_oracles.py    # Amplitude oracle implementations
  backends/
    statevector.py          # Statevector simulator backend
    aer_simulator.py        # Aer noise simulator backend
    ibm_quantum.py          # IBM Quantum hardware backend
    braket.py               # AWS Braket backend
  utils/
    circuit_optimizer.py    # Transpilation and circuit optimization
    error_mitigation.py     # Readout error mitigation, ZNE, PEC
    resource_estimator.py   # Gate count, depth, qubit estimation
    result_interpreter.py   # Measurement result parsing and analysis
  benchmarks/
    algorithm_benchmark.py  # Cross-algorithm comparison suite
    performance_metrics.py  # Execution time, fidelity, depth tracking
```

## Best Practices

1. **Circuit depth awareness**: Keep circuits shallow for NISQ backends. Use transpilation optimization levels (0-3) to reduce depth. Monitor T-gate count for fault-tolerant cost estimation.

2. **Shot count calibration**: Use at least 4096 shots for probability estimation. For Grover's search, increase to 8192+ to resolve closely-spaced eigenvalues. For VQE, use 8192 shots minimum for gradient estimation stability.

3. **Noise mitigation**: Always apply readout error mitigation, zero-noise extrapolation, or probabilistic error cancellation when running on noisy backends. Use `error_mitigation=True` in BackendConfig.

4. **Oracle construction**: Build oracles declaratively using the oracle builder helpers rather than manual gate sequences. This prevents common bugs like incorrect qubit ordering and phase convention errors.

5. **Reproducibility**: Set `seed_transpiler` and `seed_simulator` in BackendConfig for deterministic results. Store circuit QASM for auditability and cross-platform verification.

6. **Scaling validation**: Before running large instances, validate algorithm correctness on small instances (2-4 qubits) where classical verification is feasible. Compare against exact diagonalization or brute-force classical solutions.

7. **Variational algorithm convergence**: Monitor cost function convergence with early stopping. Typical VQE converges in 20-100 iterations. QAOA performance improves with circuit depth but faces barren plateaus beyond ~10 layers on random graphs.

8. **Qubit allocation**: For hybrid algorithms, partition qubits between problem and ancilla registers explicitly. Use the qubit allocator utility to avoid address conflicts and optimize qubit reuse.

9. **Result validation**: Cross-reference quantum results with classical exact solutions for small instances. Use fidelity metrics, trace distance, and statistical hypothesis testing to quantify result quality.

10. **Hardware selection**: Use statevector simulator for algorithm development, Aer for noisy simulation, and real hardware only for final validation. Match backend to algorithm requirements (e.g., QAOA needs coupling maps compatible with the problem graph).

## Performance Considerations

- **Circuit depth vs qubit count tradeoff**: More qubits enable shallower circuits for some algorithms (e.g., ancilla-based Grover), while fewer qubits require deeper circuits. Optimize for your hardware's connectivity constraints.
- **Shot noise scaling**: Variance in measurement outcomes scales as 1/sqrt(shots). For precision epsilon, you need O(1/epsilon^2) shots. Amplitude estimation reduces this to O(1/epsilon).
- **Transpilation overhead**: Aggressive transpilation can increase circuit depth by 2-5x for hardware with limited connectivity. Use the circuit optimizer to find the best depth/gate-count tradeoff.
- **Noise accumulation**: Error rates accumulate linearly with circuit depth for depolarizing noise. For a circuit of depth d with per-gate error rate p, the total error rate is approximately d*p. Keep circuits below 1000 gates for NISQ devices.
- **Classical optimizer overhead**: VQE and QAOA classical optimizers add significant wall-clock time. L-BFGS-B converges faster but requires gradient estimation (2 extra circuits per iteration). COBYLA is gradient-free but needs more iterations.
- **Memory requirements**: Statevector simulation requires 2^n complex amplitudes. For n=30 qubits, this is ~16 GB. Use shot-based simulation for larger qubit counts.
- **Parallel execution**: Submit independent circuits (e.g., gradient estimation shots) in parallel to reduce wall-clock time. Most backends support batch execution.

## Security Considerations

- **Shor's algorithm threat**: Shor's algorithm can break RSA, ECC, and other public-key cryptosystems when run on fault-tolerant quantum hardware. Current estimates suggest ~4000 logical qubits are needed to break RSA-2048. Organizations should begin migrating to post-quantum cryptography now.
- **Grover's algorithm impact**: Grover's provides quadratic speedup for brute-force search, effectively halving the security bits of symmetric ciphers. AES-128 provides 64-bit security against quantum attacks; use AES-256 for 128-bit post-quantum security.
- **Algorithmic side channels**: Variational algorithms may leak information through measurement outcomes. In multi-party quantum computing scenarios, ensure measurement results are properly authenticated and integrity-protected.
- **Reproducibility attacks**: Deterministic quantum circuits with known seeds could enable adversaries to predict outcomes. Use hardware-specific noise models and randomize where possible.
- **Resource estimation secrecy**:透露 quantum resource estimates for specific problems could reveal strategic capabilities. Treat resource estimation results as sensitive in competitive contexts.

## Related Modules

- **quantum-cryptography** — Post-quantum cryptographic primitives and QKD protocols that use algorithmic foundations from this module. Includes Kyber, Dilithium, and SPHINCS+ implementations.
- **quantum-error-correction** — Error correction codes that protect algorithm circuits from noise; essential for scaling algorithms to larger qubit counts and achieving fault-tolerant execution.
- **quantum-optimization** — Extended optimization algorithms beyond QAOA, including VQE extensions, quantum annealing simulation, and QUBO solvers for combinatorial problems.
- **quantum-simulation** — Hamiltonian simulation methods that are themselves algorithms; this module provides the algorithmic framework while quantum-simulation provides physics-specific implementations.

## References

- Nielsen, M. A. & Chuang, I. L. (2010). *Quantum Computation and Quantum Information*. Cambridge University Press.
- Grover, L. K. (1996). A fast quantum mechanical algorithm for database search. *Proceedings of the 28th Annual ACM Symposium on Theory of Computing*, 212-219.
- Shor, P. W. (1994). Algorithms for quantum computation: discrete logarithms and factoring. *Proceedings of the 35th Annual Symposium on Foundations of Computer Science*, 124-134.
- Peruzzo, A. et al. (2014). A variational eigenvalue solver on a photonic quantum processor. *Nature Communications*, 5, 4213.
- Farhi, E., Goldstone, J., & Gutmann, S. (2014). A quantum approximate optimization algorithm. *arXiv:1411.4028*.
- Harrow, A. W., Hassidim, A., & Lloyd, S. (2009). Quantum algorithm for linear systems of equations. *Physical Review Letters*, 103(15), 150502.
- Brassard, G., Hoyer, P., Mosca, M., & Tapp, A. (2002). Quantum amplitude amplification and estimation. *Contemporary Mathematics*, 305, 53-74.

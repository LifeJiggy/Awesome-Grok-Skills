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

## Advanced Configuration

### Backend Configuration Matrix

| Backend | Qubits | Noise Model | Use Case |
|---------|--------|-------------|----------|
| `statevector_simulator` | ≤30 | None | Algorithm development, verification |
| `aer_simulator` | ≤40 | Configurable | Noisy circuit testing |
| `ibm_quantum` | 5-1000+ | Hardware-calibrated | Production execution |
| `braket_simulator` | ≤25 | None | AWS ecosystem integration |
| `braket_iontrap` | ≤20 | IonQ noise model | Ion trap algorithms |
| `braket_sv` | ≤30 | None | Statevector simulation |

### Transpilation Profiles

```python
from quantum_algorithms import TranspileProfile, OptimizationLevel

# Profile 1: Speed-optimized (minimal optimization)
profile_speed = TranspileProfile(
    optimization_level=0,
    seed_transpiler=42,
    coupling_map=None,  # All-to-all
    basis_gates=["cx", "u3", "rz"]
)

# Profile 2: Balanced (default)
profile_balanced = TranspileProfile(
    optimization_level=2,
    seed_transpiler=42,
    coupling_map="ibmq_manila",
    basis_gates=["cx", "id", "rz", "sx", "x"]
)

# Profile 3: Depth-optimized (aggressive)
profile_depth = TranspileProfile(
    optimization_level=3,
    seed_transpiler=42,
    coupling_map="ibmq_mumbai",
    basis_gates=["cx", "id", "rz", "sx", "x"],
    layout_method="sabre",
    routing_method="sabre"
)
```

### Noise Model Configuration

```python
from quantum_algorithms import NoiseConfig, DepolarizingNoise, ThermalRelaxation

# Custom noise model
noise = NoiseConfig(
    depolarizing=DepolarizingNoise(
        single_qubit_rate=1e-4,
        two_qubit_rate=1e-3
    ),
    thermal_relaxation=ThermalRelaxation(
        t1_us=50.0,  # T1 relaxation time
        t2_us=70.0,  # T2 dephasing time
        gate_time_ns=35.5  # CNOT gate time
    ),
    readout_error=0.02
)

config = BackendConfig(
    num_qubits=8,
    noise_model=noise,
    shots=8192
)
```

### Advanced Algorithm Parameters

```python
# VQE with advanced configuration
vqe_advanced = VQEConfig(
    molecule="LiH",
    bond_distance=1.6,
    basis="sto-6g",
    
    # Ansatz selection
    ansatz="uccsd",
    num_electrons=4,
    num_spatial_orbitals=6,
    initial_point="scf",  # Initialize from HF solution
    
    # Optimizer configuration
    optimizer="SPSA",
    maxiter=200,
    tol=1e-6,
    blocking=True,
    allowed_increase=0.02,
    
    # Error mitigation
    error_mitigation="zne",
    zne_extrapolation="linear",
    zne_factors=[1.0, 1.5, 2.0],
    
    # Convergence criteria
    convergence_window=10,
    patience=20,
    min_improvement=1e-8
)

# QAOA with custom mixer
qaoa_advanced = QAOAConfig(
    graph_edges=[(0,1), (1,2), (2,3), (3,0)],
    num_layers=5,
    optimizer="ADAM",
    initial_point=[0.1, 0.1, 0.1, 0.1, 0.1],
    
    # Custom mixer Hamiltonian
    mixer_type="x_mixer",
    mixer_graph=None,  # Complete graph by default
    
    # Callback for convergence monitoring
    callback=convergence_callback,
    
    # Constraint handling
    penalty_strength=10.0,
    constraint_type="equality"
)
```

## Architecture Patterns

### Plugin-Based Algorithm Registry

```python
from quantum_algorithms import AlgorithmRegistry, AlgorithmPlugin

# Register custom algorithm
class MyCustomAlgorithm(AlgorithmPlugin):
    name = "custom_optimization"
    version = "1.0.0"
    requirements = {"min_qubits": 4, "max_depth": 1000}
    
    def build_circuit(self, params):
        # Custom circuit construction
        pass
    
    def interpret_results(self, counts):
        # Custom result interpretation
        pass

# Register and use
registry = AlgorithmRegistry()
registry.register(MyCustomAlgorithm)
engine = registry.create_engine("custom_optimization", config)
```

### Factory Pattern for Backend Selection

```python
from quantum_algorithms import BackendFactory, BackendType

# Automatic backend selection based on requirements
factory = BackendFactory()

# Get optimal backend for algorithm requirements
backend = factory.select(
    algorithm="vqe",
    num_qubits=20,
    max_depth=500,
    error_tolerance=0.01,
    prefer_hardware=False  # Use simulator
)

# Backend with fallback chain
backend_with_fallback = factory.create_with_fallback(
    primary=BackendType.IBM_QUANTUM,
    fallbacks=[BackendType.AER_SIMULATOR, BackendType.STATEVECTOR],
    retry_count=3
)
```

### Result Caching Architecture

```python
from quantum_algorithms import ResultCache, CacheStrategy

cache = ResultCache(
    strategy=CacheStrategy.HYBRID,
    memory_limit_mb=512,
    disk_path="/tmp/quantum_cache",
    ttl_hours=24
)

# Cache-aware execution
result = engine.run_with_cache(
    algorithm="grover",
    params={"target": "01101", "iterations": 3},
    cache_key="grover_5q_target_01101",
    force_recompute=False
)

# Cache statistics
stats = cache.get_stats()
print(f"Hit rate: {stats.hit_rate:.2%}")
print(f"Total cached: {stats.total_entries}")
```

### Modular Circuit Composition

```python
from quantum_algorithms import CircuitComposer, SubCircuit

# Compose complex circuits from sub-circuits
composer = CircuitComposer()

# Add sub-circuits
composer.add(SubCircuit("oracle", oracle_circuit))
composer.add(SubCircuit("diffusion", diffusion_circuit))
composer.add(SubCircuit("initial_state", state_prep_circuit))

# Connect with barriers and measurements
final_circuit = composer.compose(
    add_barriers=True,
    measure_all=True,
    optimize_overlap=True
)
```

## Integration Guide

### Qiskit Ecosystem Integration

```python
from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, Estimator, Sampler
from quantum_algorithms import QiskitAdapter

# Initialize runtime service
service = QiskitRuntimeService(channel="ibm_quantum")

# Create adapter
adapter = QiskitAdapter(service=service)

# Convert algorithm to Qiskit primitives
circuit = adapter.to_primitives(
    algorithm="vqe",
    config=vqe_config,
    primitive_type="estimator"
)

# Execute with Qiskit Runtime
estimator = Estimator(session=session)
job = estimator.run(circuits=[circuit], observables=[hamiltonian])
result = job.result()
```

### AWS Braket Integration

```python
from braket.devices import LocalSimulator
from braket.aws import AwsDevice
from quantum_algorithms import BraketAdapter

# Local simulation
local_device = LocalSimulator()
braket_adapter = BraketAdapter(device=local_device)

# Submit to real hardware
arn = "arn:aws:braket:::device/qpu/ionq/Harmony"
aws_device = AwsDevice(arn)
hw_adapter = BraketAdapter(device=aws_device)

# Execute VQE
result = hw_adapter.run_vqe(
    hamiltonian=molecular_hamiltonian,
    ansatz=uccsd_ansatz,
    optimizer="COBYLA",
    max_iterations=100
)
```

### PennyLane Integration

```python
import pennylane as qml
from quantum_algorithms import PennyLaneAdapter

# Convert Qiskit circuit to PennyLane
adapter = PennyLaneAdapter()

dev = qml.device("default.qubit", wires=4)

@qml.qnode(dev)
def vqe_circuit(params):
    adapter.apply_circuit(qiskit_circuit, params)
    return qml.expval(qml.PauliZ(0))

# Use PennyLane's gradient computation
gradient = qml.grad(vqe_circuit)
grad_value = gradient(vqe_params)
```

### Cirq Integration

```python
import cirq
from quantum_algorithms import CirqAdapter

# Convert to Cirq circuit
adapter = CirqAdapter()
cirq_circuit = adapter.to_cirq(qiskit_circuit)

# Execute with Cirq simulator
simulator = cirq.Simulator()
result = simulator.simulate(cirq_circuit)

# Run on Google Quantum AI
from cirq_google import EngineSampler
sampler = EngineSampler(processor_id="rainbow", project_id="my-project")
```

### REST API Integration

```python
from quantum_algorithms import QuantumAPIClient

# Connect to quantum cloud service
client = QuantumAPIClient(
    endpoint="https://quantum-api.example.com",
    api_key="your-api-key",
    timeout=300
)

# Submit job
job_id = client.submit_job(
    algorithm="vqe",
    config=vqe_config,
    backend="ibm_mumbai"
)

# Poll for results
result = client.wait_for_job(job_id, poll_interval=5)
print(f"Job status: {result.status}")
print(f"Execution time: {result.execution_time_ms}")
```

## Performance Optimization

### Circuit Optimization Techniques

1. **Gate Fusion**: Combine consecutive single-qubit gates into a single U3 gate
2. **CNOT Cancellation**: Remove redundant CNOT pairs
3. **Template Optimization**: Apply known circuit identities
4. **Qubit Routing**: Minimize SWAP operations for limited connectivity
5. **Depth Reduction**: Parallelize independent gate operations

```python
from quantum_algorithms import CircuitOptimizer

optimizer = CircuitOptimizer(
    level=3,
    target_gates=["cx", "u3"],
    coupling_map="ibmq_mumbai"
)

# Optimize circuit
optimized = optimizer.optimize(original_circuit)

# Statistics
print(f"Original depth: {original_circuit.depth()}")
print(f"Optimized depth: {optimized.depth()}")
print(f"Reduction: {(1 - optimized.depth()/original_circuit.depth())*100:.1f}%")
```

### Parallel Execution Strategy

```python
from quantum_algorithms import ParallelExecutor

executor = ParallelExecutor(
    max_workers=8,
    batch_size=100,
    backend="aer_simulator"
)

# Execute multiple circuits in parallel
circuits = [create_circuit(params) for params in parameter_list]
results = executor.execute_batch(circuits)

# Gather statistics
print(f"Total execution time: {results.total_time_ms:.1f} ms")
print(f"Average per circuit: {results.avg_time_ms:.1f} ms")
print(f"Throughput: {results.circuits_per_second:.1f} circuits/s")
```

### Memory Optimization

```python
from quantum_algorithms import MemoryOptimizer

# For large qubit counts (>25 qubits)
optimizer = MemoryOptimizer(
    strategy="chunked",
    chunk_size=20,  # Process 20 qubits at a time
    use_disk_swap=True,
    swap_path="/fast_ssd/swap"
)

# Memory-efficient statevector simulation
result = optimizer.run_statevector_simulation(
    circuit=large_circuit,
    num_qubits=30
)
```

### Gradient Estimation Optimization

```python
from quantum_algorithms import GradientEstimator

# Parameter-shift rule (exact gradients)
estimator = GradientEstimator(
    method="parameter_shift",
    shots=1024,
    concurrent_evaluations=4
)

# Compute gradient for VQE
gradient = estimator.compute(
    circuit=vqe_circuit,
    parameters=vqe_params,
    observable=hamiltonian
)

# Alternative: SPSA gradient (fewer circuits)
spsa_estimator = GradientEstimator(
    method="spsa",
    shots=2048,
    perturbation=0.01
)
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Circuit Too Deep for Hardware

**Symptom**: Transpilation fails or circuit depth exceeds hardware limits

**Solution**:
```python
# Reduce circuit depth
optimizer = CircuitOptimizer(level=3)
optimized = optimizer.optimize(circuit)

# Use approximate compilation
from quantum_algorithms import ApproxCompiler
compiler = ApproxCompiler(
    max_error=0.01,  # Allow 1% error
    target_depth=100
)
approx_circuit = compiler.compile(circuit)
```

#### 2. Measurement Statistics Insufficient

**Symptom**: High variance in results, poor convergence

**Solution**:
```python
# Increase shot count
config = BackendConfig(shots=16384)  # Double default

# Use error mitigation
config.error_mitigation = True
config.readout_mitigation_shots = 8192
```

#### 3. VQE Not Converging

**Symptom**: Energy oscillates or plateaus

**Solution**:
```python
# Try different optimizer
vqe_config.optimizer = "L-BFGS-B"  # From COBYLA

# Adjust initial point
vqe_config.initial_point = "hf"  # Hartree-Fock initial state

# Enable callback for monitoring
vqe_config.callback = lambda iter, params, energy: print(f"{iter}: {energy}")
```

#### 4. Qubit Routing Overhead

**Symptom**: Too many SWAP gates after transpilation

**Solution**:
```python
# Use hardware-efficient ansatz
vqe_config.ansatz = "hardware_efficient"
vqe_config.entanglement = "linear"  # Instead of full

# Specify coupling map during circuit construction
from quantum_algorithms import CouplingMap
circuit = engine.build_circuit(coupling_map="ibmq_mumbai")
```

#### 5. Backend Connection Issues

**Symptom**: Timeouts or connection errors with IBM Quantum

**Solution**:
```python
from quantum_algorithms import BackendPool

# Use connection pool with retry
pool = BackendPool(
    max_retries=5,
    retry_delay=30,  # seconds
    health_check_interval=60
)

# Get healthy backend
backend = pool.get_healthy_backend("ibm_mumbai")
```

## API Reference

### Core Classes

#### `QuantumAlgorithmEngine`
Main entry point for algorithm execution.

```python
class QuantumAlgorithmEngine:
    def __init__(self, config: BackendConfig) -> None: ...
    
    def run_deutsch_jozsa(self, oracle_type: str, oracle_pattern: List[int]) -> AlgorithmResult: ...
    def run_grover(self, config: GroverConfig) -> GroverResult: ...
    def run_shor(self, number_to_factor: int, num_qubits_used: int) -> ShorResult: ...
    def run_vqe(self, config: VQEConfig) -> VQEResult: ...
    def run_qaoa(self, config: QAOAConfig) -> QAOAResult: ...
    def run_hhl(self, config: HHLConfig) -> HHLResult: ...
    def run_qpe(self, config: QPEConfig) -> QPEResult: ...
    def run_amplitude_estimation(self, config: AEConfig) -> AEResult: ...
```

#### `BackendConfig`
Configuration for quantum backend execution.

```python
@dataclass
class BackendConfig:
    num_qubits: int
    shots: int = 4096
    backend: str = "aer_simulator"
    seed_transpiler: Optional[int] = None
    seed_simulator: Optional[int] = None
    noise_model: Optional[NoiseConfig] = None
    error_mitigation: bool = False
    optimization_level: int = 2
    coupling_map: Optional[str] = None
    memory: Optional[int] = None
    max_credits: int = 10
```

#### `GroverConfig`
Configuration for Grover's search algorithm.

```python
@dataclass
class GroverConfig:
    num_qubits: int
    target_state: str
    num_iterations: Optional[int] = None  # Auto-calculated if None
    auto_optimize: bool = True
    oracle_type: str = "phase"
    diffusion_type: str = "standard"
    fixed_point: bool = False
    epsilon: float = 0.01  # For fixed-point Grover
```

#### `VQEConfig`
Configuration for Variational Quantum Eigensolver.

```python
@dataclass
class VQEConfig:
    molecule: str
    bond_distance: float
    basis: str = "sto-3g"
    ansatz: str = "uccsd"
    optimizer: str = "COBYLA"
    max_iterations: int = 100
    convergence_threshold: float = 1e-6
    initial_point: Optional[str] = None
    error_mitigation: Optional[str] = None
    callback: Optional[Callable] = None
```

### Data Classes

#### `AlgorithmResult`
Base result class for all algorithm outputs.

```python
@dataclass
class AlgorithmResult:
    measurement_outcome: str
    circuit_depth: int
    gate_count: Dict[str, int]
    execution_time_ms: float
    backend: str
    shots: int
    metadata: Dict[str, Any]
```

#### `GroverResult`
Result from Grover's search algorithm.

```python
@dataclass
class GroverResult(AlgorithmResult):
    found_state: str
    probability: float
    oracle_calls: int
    iterations: int
    amplitude: float
    success_probability: float
```

#### `VQEResult`
Result from VQE execution.

```python
@dataclass
class VQEResult(AlgorithmResult):
    ground_state_energy: float
    exact_energy: float
    chemical_accuracy_mHartree: float
    optimal_parameters: np.ndarray
    convergence_history: List[float]
    num_iterations: int
    optimizer_result: OptimizeResult
```

### Enums

#### `AlgorithmType`
```python
class AlgorithmType(Enum):
    DEUTSCH_JOZSA = "deutsch_jozsa"
    BERNSTEIN_VAZIRANI = "bernstein_vazirani"
    SIMON = "simon"
    GROVER = "grover"
    SHOR = "shor"
    QPE = "qpe"
    VQE = "vqe"
    QAOA = "qaoa"
    HHL = "hhl"
    AMPLITUDE_ESTIMATION = "amplitude_estimation"
    QUANTUM_WALKS = "quantum_walks"
```

## Data Models

### Molecule Schema

```json
{
  "name": "H2",
  "atoms": [
    {"element": "H", "position": [0.0, 0.0, 0.0]},
    {"element": "H", "position": [0.0, 0.0, 0.735]}
  ],
  "charge": 0,
  "multiplicity": 1,
  "basis": "sto-3g",
  "hamiltonian": {
    "type": "molecular",
    "num_qubits": 4,
    "num_terms": 15,
    "coefficients": [0.17, -0.22, 0.17, ...],
    "pauli_labels": ["IIII", "IIIZ", "IIZI", ...]
  }
}
```

### Algorithm Result Schema

```json
{
  "algorithm": "grover",
  "status": "success",
  "execution_id": "uuid-v4",
  "timestamp": "2024-01-15T10:30:00Z",
  "input": {
    "num_qubits": 5,
    "target_state": "01101",
    "num_iterations": 3
  },
  "output": {
    "found_state": "01101",
    "probability": 0.95,
    "oracle_calls": 3
  },
  "metrics": {
    "circuit_depth": 45,
    "gate_count": {"cx": 12, "u3": 8, "measure": 5},
    "execution_time_ms": 125.3,
    "shots": 4096
  },
  "backend": {
    "name": "aer_simulator",
    "noise_model": "depolarizing",
    "seed": 42
  }
}
```

### Benchmark Result Schema

```json
{
  "benchmark_id": "uuid-v4",
  "timestamp": "2024-01-15T10:30:00Z",
  "algorithms": ["grover", "vqe", "qaoa"],
  "backends": ["aer_simulator", "ibm_mumbai"],
  "qubit_counts": [4, 8, 12, 16],
  "results": [
    {
      "algorithm": "grover",
      "backend": "aer_simulator",
      "num_qubits": 8,
      "circuit_depth": 32,
      "execution_time_ms": 45.2,
      "fidelity": 0.98
    }
  ],
  "summary": {
    "best_algorithm": "grover",
    "best_backend": "aer_simulator",
    "avg_fidelity": 0.97
  }
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY quantum_algorithms/ /app/quantum_algorithms/
WORKDIR /app

# Environment variables
ENV QUANTUM_BACKEND=aer_simulator
ENV QUANTUM_SHOTS=4096
ENV QUANTUM_OPTIMIZATION_LEVEL=2

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from quantum_algorithms import health_check; health_check()"

CMD ["python", "-m", "quantum_algorithms.server"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quantum-algorithms
  namespace: quantum
spec:
  replicas: 3
  selector:
    matchLabels:
      app: quantum-algorithms
  template:
    metadata:
      labels:
        app: quantum-algorithms
    spec:
      containers:
      - name: quantum-algorithms
        image: quantum-algorithms:latest
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "8Gi"
            cpu: "4000m"
        env:
        - name: QUANTUM_BACKEND
          value: "aer_simulator"
        - name: QUANTUM_SHOTS
          value: "4096"
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Cloud Deployment (AWS)

```yaml
# ECS Task Definition
{
  "family": "quantum-algorithms",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "2048",
  "memory": "8192",
  "containerDefinitions": [
    {
      "name": "quantum-algorithms",
      "image": "123456789.dkr.ecr.us-east-1.amazonaws.com/quantum-algorithms:latest",
      "portMappings": [
        {
          "containerPort": 8080,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "QUANTUM_BACKEND", "value": "ibm_quantum"},
        {"name": "QUANTUM_SHOTS", "value": "4096"}
      ],
      "secrets": [
        {
          "name": "IBM_QUANTUM_TOKEN",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:123456789:secret:ibm-quantum-token"
        }
      ]
    }
  ]
}
```

## Monitoring & Observability

### Metrics Collection

```python
from quantum_algorithms import MetricsCollector, MetricType

collector = MetricsCollector(
    backend="prometheus",
    endpoint="http://localhost:9090"
)

# Custom metrics
collector.register_metric(
    name="quantum_algorithm_execution_time",
    type=MetricType.HISTOGRAM,
    description="Algorithm execution time in milliseconds",
    labels=["algorithm", "backend", "num_qubits"]
)

# Record metric
collector.observe(
    metric="quantum_algorithm_execution_time",
    value=125.3,
    labels={"algorithm": "grover", "backend": "aer", "num_qubits": "5"}
)
```

### Distributed Tracing

```python
from quantum_algorithms import Tracer, SpanKind

tracer = Tracer(
    service="quantum-algorithms",
    endpoint="http://localhost:14268/api/traces"
)

# Trace algorithm execution
with tracer.start_span("grover_search", kind=SpanKind.INTERNAL) as span:
    span.set_attribute("algorithm", "grover")
    span.set_attribute("num_qubits", 5)
    
    with tracer.start_span("circuit_construction"):
        circuit = build_grover_circuit(config)
        span.set_attribute("circuit_depth", circuit.depth())
    
    with tracer.start_span("execution"):
        result = backend.run(circuit)
        span.set_attribute("execution_time_ms", result.execution_time_ms)
    
    span.set_attribute("success", True)
```

### Logging Configuration

```python
import logging
from quantum_algorithms import QuantumLogger

# Configure structured logging
logger = QuantumLogger(
    name="quantum-algorithms",
    level=logging.INFO,
    format="json",
    output="stdout"
)

# Add context
logger.add_context(
    service="quantum-algorithms",
    version="2.0.0",
    environment="production"
)

# Log with quantum-specific fields
logger.info("Algorithm execution completed",
    algorithm="grover",
    num_qubits=5,
    execution_time_ms=125.3,
    success=True
)
```

### Health Checks

```python
from quantum_algorithms import HealthCheck, HealthStatus

health = HealthCheck()

# Register checks
health.register("backend", check_backend_connection)
health.register("memory", check_memory_usage)
health.register("disk", check_disk_space)

# Run health checks
status = health.run()
print(f"Overall status: {status.overall}")  # HEALTHY, DEGRADED, UNHEALTHY
print(f"Checks: {status.checks}")
```

## Testing Strategy

### Unit Tests

```python
import pytest
from quantum_algorithms import QuantumAlgorithmEngine, BackendConfig

class TestGroverAlgorithm:
    def setup_method(self):
        self.config = BackendConfig(
            num_qubits=4,
            shots=4096,
            backend="statevector_simulator",
            seed_simulator=42
        )
        self.engine = QuantumAlgorithmEngine(config=self.config)
    
    def test_grover_finds_target(self):
        result = self.engine.run_grover(
            config=GroverConfig(num_qubits=4, target_state="1010")
        )
        assert result.found_state == "1010"
        assert result.probability > 0.5
    
    def test_grover_iterations_optimal(self):
        result = self.engine.run_grover(
            config=GroverConfig(num_qubits=4, target_state="1010", auto_optimize=True)
        )
        assert result.iterations == 3  # floor(pi/4 * sqrt(16))
```

### Integration Tests

```python
class TestVQEIntegration:
    @pytest.mark.integration
    def test_vqe_h2_molecule(self):
        config = BackendConfig(num_qubits=4, shots=8192)
        engine = QuantumAlgorithmEngine(config=config)
        
        result = engine.run_vqe(
            config=VQEConfig(molecule="H2", bond_distance=0.735)
        )
        
        # H2 ground state energy: -1.857 Ha
        assert abs(result.ground_state_energy - (-1.857)) < 0.01
        assert result.chemical_accuracy_mHartree < 1.6  # Chemical accuracy threshold
    
    @pytest.mark.integration
    @pytest.mark.hardware
    def test_vqe_on_real_hardware(self):
        config = BackendConfig(
            num_qubits=4,
            backend="ibm_manila",
            shots=8192
        )
        engine = QuantumAlgorithmEngine(config=config)
        
        result = engine.run_vqe(
            config=VQEConfig(molecule="H2", bond_distance=0.735)
        )
        assert result.status == "success"
```

### Performance Tests

```python
class TestPerformance:
    @pytest.mark.performance
    def test_grover_scaling(self):
        results = []
        for n in range(4, 13):
            config = BackendConfig(num_qubits=n, shots=4096)
            engine = QuantumAlgorithmEngine(config=config)
            
            result = engine.run_grover(
                config=GroverConfig(num_qubits=n, target_state="1" * n)
            )
            results.append({
                "num_qubits": n,
                "circuit_depth": result.circuit_depth,
                "execution_time_ms": result.execution_time_ms
            })
        
        # Verify O(sqrt(N)) scaling
        depths = [r["circuit_depth"] for r in results]
        # Check that depth scales sub-quadratically
        assert depths[-1] < depths[0] * (2**13 / 2**4)
```

### Chaos Tests

```python
class TestChaos:
    @pytest.mark.chaos
    def test_backend_failure_handling(self):
        config = BackendConfig(num_qubits=4, backend="nonexistent_backend")
        engine = QuantumAlgorithmEngine(config=config)
        
        with pytest.raises(BackendConnectionError):
            engine.run_grover(
                config=GroverConfig(num_qubits=4, target_state="1010")
            )
    
    @pytest.mark.chaos
    def test_insufficient_credits(self):
        config = BackendConfig(num_qubits=4, backend="ibm_mumbai", max_credits=0)
        engine = QuantumAlgorithmEngine(config=config)
        
        with pytest.raises(InsufficientCreditsError):
            engine.run_grover(
                config=GroverConfig(num_qubits=4, target_state="1010")
            )
```

## Versioning & Migration

### Semantic Versioning

- **Major (X.0.0)**: Breaking API changes, new algorithm types, backend deprecation
- **Minor (0.X.0)**: New features, algorithm improvements, backend additions
- **Patch (0.0.X)**: Bug fixes, documentation updates, performance improvements

### Migration Guide (v1.x → v2.0)

```python
# v1.x (deprecated)
from quantum_algorithms import GroverSearch, Backend
result = GroverSearch(num_qubits=5).search(target="01101", backend=Backend.AER)

# v2.0 (current)
from quantum_algorithms import QuantumAlgorithmEngine, BackendConfig, GroverConfig
config = BackendConfig(num_qubits=5, backend="aer_simulator")
engine = QuantumAlgorithmEngine(config=config)
result = engine.run_grover(
    config=GroverConfig(num_qubits=5, target_state="01101")
)
```

### Deprecation Schedule

| Version | Feature | Replacement | Removal |
|---------|---------|-------------|---------|
| 2.0 | `GroverSearch` class | `QuantumAlgorithmEngine.run_grover` | v3.0 |
| 2.0 | `Backend` enum | String backend names | v3.0 |
| 2.1 | `execute_circuit` function | `engine.run_*` methods | v3.0 |
| 2.1 | `CircuitBuilder` class | `CircuitComposer` | v3.1 |

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New unified `QuantumAlgorithmEngine` API
- **Breaking**: `BackendConfig` replaces multiple config classes
- **Added**: HHL linear systems solver
- **Added**: Amplitude estimation algorithm
- **Added**: Quantum walks implementation
- **Added**: Multi-backend support (IBM Quantum, AWS Braket, PennyLane)
- **Added**: Circuit optimization pipeline
- **Added**: Error mitigation framework
- **Improved**: 50% faster circuit transpilation
- **Fixed**: Memory leak in long-running simulations

#### v1.5.0 (2023-10-01)
- **Added**: QAOA with custom mixer operators
- **Added**: Fixed-point Grover's algorithm
- **Improved**: VQE convergence monitoring
- **Fixed**: Qubit ordering bug in Deutsch-Jozsa

#### v1.4.0 (2023-07-15)
- **Added**: Hardware-efficient ansatz for VQE
- **Added**: SPSA optimizer support
- **Improved**: Transpilation optimization
- **Fixed**: Statevector memory management

## Glossary

| Term | Definition |
|------|------------|
| **Amplitude Amplification** | Quantum technique to increase probability of desired measurement outcomes |
| **Ansatz** | Parameterized quantum circuit structure used in variational algorithms |
| **CNOT** | Controlled-NOT gate; two-qubit entangling gate |
| **Deutsch-Jozsa** | Algorithm to determine if function is constant or balanced |
| **Grover's Search** | Unstructured search with quadratic speedup |
| **HHL** | Harrow-Hassidim-Lloyd algorithm for linear systems |
| **NISQ** | Noisy Intermediate-Scale Quantum (50-1000 qubits) |
| **QAOA** | Quantum Approximate Optimization Algorithm |
| **QBER** | Quantum Bit Error Rate |
| **QPE** | Quantum Phase Estimation |
| **Qubit** | Quantum bit; fundamental unit of quantum information |
| **Shor's Algorithm** | Polynomial-time integer factorization |
| **Superposition** | Quantum state existing in multiple basis states simultaneously |
| **VQE** | Variational Quantum Eigensolver |
| **Variational** | Hybrid classical-quantum optimization approach |

## Contributing Guidelines

### Development Setup

```bash
# Clone repository
git clone https://github.com/example/quantum-algorithms.git
cd quantum-algorithms

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Run linting
ruff check .
mypy quantum_algorithms/
```

### Code Style

- Follow PEP 8 with line length 100
- Use type hints for all public functions
- Document public API with Google-style docstrings
- Keep functions under 50 lines
- Maximum file length: 500 lines

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Add changelog entry
6. Request review from maintainers
7. Squash and merge

### Commit Messages

```
type(scope): brief description

- Detailed change 1
- Detailed change 2

Closes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## License

MIT License

Copyright (c) 2024 Quantum Algorithms Contributors

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

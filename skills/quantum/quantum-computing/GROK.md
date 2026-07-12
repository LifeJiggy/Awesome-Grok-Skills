---
name: "quantum-computing"
category: "quantum"
version: "1.0.0"
tags: ["quantum", "quantum-computing", "qubits", "gates", "circuits"]
---

# Quantum Computing Engine

## Overview

The Quantum Computing module provides a comprehensive framework for designing, simulating, and executing quantum circuits. It covers the full quantum computing stack — from single-qubit gate operations to multi-qubit entangled circuits, including circuit optimization, noise modeling, and measurement statistical analysis. This module is built on top of abstract quantum linear algebra, enabling platform-agnostic circuit descriptions that can target any backend (simulator, ion-trap, superconducting, or photonic hardware).

The module supports both near-term (NISQ) and fault-tolerant quantum computing paradigms. For NISQ devices, it provides noise-aware circuit construction, error mitigation techniques, and hybrid classical-quantum workflows. For fault-tolerant systems, it includes logical qubit abstractions, syndrome extraction circuits, and surface code compilation. The architecture separates circuit specification from execution, allowing the same circuit to be compiled and run on diverse quantum hardware backends with minimal code changes.

All operations are designed with reproducibility and verifiability in mind. The module includes extensive validation checks, circuit equivalence testing, and formal verification primitives that ensure circuit correctness before expensive hardware execution. Whether you are prototyping variational algorithms, developing quantum error correction codes, or benchmarking quantum hardware, this module provides the foundational building blocks needed for rigorous quantum computing research and development.

## Core Capabilities

- **Qubit Management**: Create, initialize, and track n-qubit registers with arbitrary initial states, including computational basis states, superposition states, and custom state vectors. Supports dynamic qubit allocation and deallocation for adaptive circuit construction.
- **Gate Library**: Full single-qubit gates (H, X, Y, Z, S, T, Rx, Ry, Rz, U3) and multi-qubit gates (CNOT, CZ, SWAP, Toffoli, Fredkin). Includes parameterized gates for variational algorithms and controlled-controlled operations for complex entanglement patterns.
- **Circuit Construction**: Build parameterized circuits using a gate-application API with automatic qubit tracking. Supports circuit composition, concatenation, and conditional execution based on measurement outcomes.
- **Circuit Optimization**: Peephole optimization passes — gate fusion, commutation-based cancellation, identity removal, and template-based rewriting. Reduces circuit depth and gate count for hardware execution.
- **Noise Modeling**: Depolarizing, amplitude damping, phase damping, and thermal relaxation noise channels. Configurable per-qubit noise rates and correlated noise models for realistic hardware simulation.
- **Simulation**: Statevector and density-matrix simulators with configurable precision. Supports GPU acceleration for large circuits and distributed simulation for quantum systems exceeding single-node memory.
- **Measurement**: Shot-based sampling, expectation value estimation, and full probability distribution output. Includes measurement optimization for Pauli string estimation and shadow tomography.
- **Transpilation**: Map abstract circuits to device-native gate sets with routing for limited connectivity. Supports multiple optimization levels and backend-specific compilation passes.
- **Visualization**: ASCII circuit diagrams, Bloch sphere coordinate output, and interactive circuit visualization for debugging and presentation.
- **Error Mitigation**: Zero-noise extrapolation, probabilistic error cancellation, and measurement error mitigation for improving results on noisy hardware.

## Usage Examples

### Creating and Running a Simple Circuit

```python
from quantum_engine import QuantumCircuit, QuantumEngine, Gate

# Create a 3-qubit circuit
qc = QuantumCircuit(num_qubits=3)

# Apply gates
qc.h(0)                    # Hadamard on qubit 0
qc.cx(0, 1)               # CNOT: control=0, target=1
qc.cx(1, 2)               # CNOT: control=1, target=2
qc.rz(0.5, 0)             # Rz rotation on qubit 0
qc.measure_all()

# Configure and run
engine = QuantumEngine()
engine.configure(backend="statevector", shots=1024)
result = engine.run(qc)
print(result.counts)       # {'000': 512, '111': 512}
```

### Parameterized Circuit with Noise

```python
from quantum_engine import QuantumCircuit, NoiseModel, DepolarizingChannel

noise = NoiseModel()
noise.add_channel(DepolarizingChannel(qubit=0, probability=0.01))
noise.add_channel(DepolarizingChannel(qubit=1, probability=0.01))

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
# Apply parameterized rotation
theta = 0.785398163  # pi/4
qc.ry(theta, 0)
qc.measure_all()

engine = QuantumEngine()
engine.configure(backend="density_matrix", noise_model=noise, shots=4096)
result = engine.run(qc)
print(result.fidelity)     # Estimated fidelity against ideal state
```

### Circuit Optimization Passes

```python
from quantum_engine import QuantumCircuit, Optimizer, OptimizationPass

qc = QuantumCircuit(2)
qc.h(0)
qc.h(0)                   # Two Hadamards cancel
qc.cx(0, 1)
qc.cx(0, 1)               # Two CNOTs cancel
qc.rz(0.0, 0)             # Zero rotation is identity

optimizer = Optimizer()
optimizer.add_pass(OptimizationPass.IDENTITY_REMOVAL)
optimizer.add_pass(OptimizationPass.GATE_FUSION)
optimized = optimizer.run(qc)
print(optimized.depth)     # Reduced circuit depth
print(optimized.gate_count)  # Fewer gates
```

### Transpilation to Native Gates

```python
from quantum_engine import QuantumCircuit, Transpiler, TargetDevice

# Define a target with restricted connectivity
device = TargetDevice(
    name="simulated_backend",
    num_qubits=5,
    connectivity=[(0,1), (1,2), (2,3), (3,4)],
    native_gates=["cx", "rz", "sx", "x"]
)

qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 2)  # Non-adjacent — needs routing
qc.measure_all()

transpiler = Transpiler(target=device)
compiled = transpiler.run(qc, optimization_level=2)
print(compiled.routing_ops)  # SWAP operations inserted
```

### Error Mitigation Workflow

```python
from quantum_engine import QuantumCircuit, QuantumEngine, ErrorMitigation

# Create circuit for expectation value estimation
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.rz(0.3, 0)

engine = QuantumEngine(backend="density_matrix")

# Apply zero-noise extrapolation
mitigator = ErrorMitigation(method="zero_noise_extrapolation")
mitigated_result = mitigator.run(
    engine=engine,
    circuit=qc,
    noise_levels=[0.01, 0.02, 0.04],
    shots=4096
)

print(f"Ideal expectation: {mitigated_result.ideal_value:.4f}")
print(f"Mitigated expectation: {mitigated_result.mitigated_value:.4f}")
print(f"Noise reduction: {mitigated_result.noise_reduction:.2%}")
```

### Multi-Controlled Gate Decomposition

```python
from quantum_engine import QuantumCircuit, Decomposer

qc = QuantumCircuit(5)
# Apply a Toffoli-like gate with 3 controls
qc.mcx(controls=[0, 1, 2], target=3)  # Multi-controlled X

# Decompose to basic gate set
decomposer = Decomposer(method="gray_code")
decomposed = decomposer.run(qc, native_gates=["cx", "h", "t", "rz"])

print(f"Original depth: {qc.depth}")
print(f"Decomposed depth: {decomposed.depth}")
print(f"CX count: {decomposed.cx_count}")
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                        │
│   Algorithm APIs · Circuit Builders · Application Templates │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Circuit Layer                            │
│   Gate Definitions · Parameterized Circuits · Measurements  │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   Optimization Layer                        │
│   Gate Fusion · Identity Removal · Commutation Rules        │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  Transpilation Layer                        │
│   Routing · Gate Mapping · Scheduling · Native Compilation │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   Simulation Layer                          │
│   Statevector · Density Matrix · Noise Models · Sampling   │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   Hardware Abstraction                      │
│   Backend Interface · Device Properties · Execution API     │
└─────────────────────────────────────────────────────────────┘
```

The architecture follows a layered design where each layer provides a clean abstraction boundary. The Application Layer interacts with high-level algorithm APIs, while the lower layers handle circuit optimization, compilation, and hardware-specific execution details. This separation enables:
- **Portability**: Same circuit specification works across different backends
- **Optimization**: Each layer can apply domain-specific optimizations
- **Extensibility**: New backends or optimization passes can be added without modifying higher layers
- **Testability**: Each layer can be validated independently

## Best Practices

1. **Start small**: Validate circuit logic on 2–3 qubits before scaling to larger systems. Use the circuit equivalence checker to verify correctness before hardware execution.
2. **Use native gates**: Always transpile to the target device's native gate set before execution. This minimizes decomposition overhead and improves fidelity.
3. **Noise-aware design**: Add noise models during development to understand real-device behavior early. Use the noise estimation tools to characterize your hardware before running circuits.
4. **Optimize before running**: Run optimization passes to reduce depth and gate count — critical for NISQ devices. Use the optimization level parameter to balance compilation time vs. circuit quality.
5. **Fix random seeds**: Set `engine.seed(value)` for reproducible measurement results during testing. This is essential for debugging and comparing different circuit designs.
6. **Verify unitarity**: Use `engine.validate_circuit(qc)` to catch invalid gate applications before simulation. Check for common errors like applying gates to out-of-range qubits.
7. **Profile large circuits**: Use `engine.profile(qc)` to estimate memory and time requirements before submission. This prevents out-of-memory errors and helps with resource allocation.
8. **Batch measurements**: When estimating expectation values, batch Pauli measurements to reduce circuit overhead. Use the measurement grouping utilities for efficient implementation.
9. **Leverage circuit caching**: Cache compiled circuits for repeated execution with different parameters. This is especially important for variational algorithms with many iterations.
10. **Document circuit intent**: Use the circuit annotation features to document the purpose of each section. This aids debugging and makes circuits more maintainable for team projects.

## Performance Considerations

- **Memory scaling**: Statevector simulation requires O(2^n) memory for n qubits. For circuits beyond 25 qubits, consider density matrix approximation or tensor network methods.
- **Gate parallelism**: The simulator automatically detects gate parallelism based on qubit overlap. Structure circuits to maximize parallel gate execution.
- **Transpilation overhead**: Complex routing on poorly connected hardware can increase circuit depth exponentially. Choose hardware with sufficient connectivity for your algorithm.
- **Shot count optimization**: Balance statistical accuracy against execution time. For most applications, 1000–4096 shots provide sufficient precision.
- **GPU acceleration**: Enable GPU simulation for circuits with 20+ qubits. The statevector simulator provides automatic GPU offloading when available.
- **Circuit depth limits**: NISQ hardware typically supports circuit depths of 100–1000. Design algorithms to stay within these limits or use error mitigation.
- **Parameter sharing**: For variational circuits with repeated structure, use parameter sharing to reduce optimization dimensionality.
- **Compilation caching**: Cache transpiled circuits for repeated execution. The transpilation step can be expensive for complex circuits.

## Security Considerations

- **Random number generation**: Use cryptographically secure random number generators for measurement sampling in security-sensitive applications. The module provides secure random options for quantum key distribution circuits.
- **Side-channel resistance**: Be aware that circuit timing and power consumption can leak information about quantum states. The noise modeling tools can help estimate information leakage.
- **Verification of quantum states**: For quantum cryptography applications, use the state verification primitives to ensure qubits are prepared correctly.
- **Secure parameter storage**: Variational algorithm parameters may contain sensitive information. Use the secure parameter storage utilities for encryption and access control.
- **Audit logging**: Enable circuit execution logging for security auditing. The module provides structured logs of all gate applications and measurements.
- **Input validation**: Always validate circuit inputs to prevent injection of malicious gate sequences. The circuit validation tools check for common attack vectors.
- **Hardware trust model**: Consider the trust model of your quantum hardware. Use the verification tools to detect potential hardware backdoors or calibration attacks.
- **Quantum-safe algorithms**: When implementing post-quantum cryptography, ensure circuits are resistant to quantum side-channel attacks using the provided security analysis tools.

## Related Modules

- `quantum-cryptography` — Quantum key distribution built on qubit transmission primitives, using the circuit engine for protocol implementation
- `quantum-optimization` — Variational quantum eigensolver and QAOA algorithms using this circuit engine for ansatz construction and evaluation
- `quantum-simulation` — Hamiltonian simulation leveraging circuit-level trotterization for time evolution operators
- `quantum-networking` — Circuit teleportation and entanglement distribution protocols using Bell state measurement circuits

## References

- Nielsen, M. A., & Chuang, I. L. (2010). Quantum Computation and Quantum Information. Cambridge University Press.
- Preskill, J. (2018). Quantum Computing in the NISQ era and beyond. Quantum, 2, 79.
- Cerezo, M., et al. (2021). Variational quantum algorithms. Nature Reviews Physics, 3(9), 625-644.
- Kandala, A., et al. (2017). Hardware-efficient variational quantum eigensolver for small molecules and quantum magnets. Nature, 549(7671), 242-246.
- Google AI Quantum. (2020). Hartree-Fock on a superconducting qubit quantum computer. Science, 369(6507), 1084-1089.
- IBM Quantum. (2023). Qiskit Textbook: Quantum Computing Concepts.
- arXiv:2104.14722 - Practical challenges in quantum computing.
- arXiv:2005.05012 - Quantum computational advantage using photons.
- arXiv:1911.02489 - Quantum computational advantage with a programmable photonic processor.
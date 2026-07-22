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

---

## Advanced Gate Operations

### Universal Gate Set Decomposition

Every quantum computation can be decomposed into a universal gate set. The standard universal set consists of {H, T, CNOT} or equivalently {Rx, Ry, Rz, CNOT}. The following demonstrates how arbitrary single-qubit rotations are decomposed into the universal set.

```python
from quantum_engine import QuantumCircuit, GateDecomposer

# Decompose an arbitrary U3 gate into H and T gates
qc = QuantumCircuit(1)
qc.u3(theta=1.2, phi=0.8, lam=-0.3, qubit=0)

decomposer = GateDecomposer(method="kak")  # KAK decomposition
decomposed = decomposer.decompose_single_qubit(
    qc,
    target_gates=["h", "t", "cx"],
    tolerance=1e-10
)

print(f"Original gates: {qc.gate_count}")
print(f"Decomposed gates: {decomposed.gate_count}")
print(f"Gate depth: {decomposed.depth}")

# Verify equivalence
assert decomposer.verify_equivalence(qc, decomposed)
```

### Multi-Qubit Gate Decomposition

```python
from quantum_engine import QuantumCircuit, MultiQubitDecomposer

# Decompose a Fredkin (CSWAP) gate into basic gates
qc = QuantumCircuit(3)
qc.fredkin(control=0, target1=1, target2=2)

decomposer = MultiQubitDecomposer()
decomposed = decomposer.decompose_fredkin(
    qc,
    native_gates=["cx", "t", "h", "rz"]
)

print(f"CX count: {decomposed.cx_count}")
print(f"Total gate count: {decomposed.gate_count}")
print(f"Circuit depth: {decomposed.depth}")
```

### Parametric Gate Optimization

```python
from quantum_engine import QuantumCircuit, ParametricOptimizer

# Optimize parameterized rotation chains
qc = QuantumCircuit(1)
qc.rx(0.5, 0)
qc.ry(0.3, 0)
qc.rz(0.7, 0)
qc.rx(0.2, 0)
qc.ry(0.8, 0)

optimizer = ParametricOptimizer()
optimized = optimizer.merge_rotations(
    qc,
    merge_axis="same",
    combine_consecutive=True
)

print(f"Before: {qc.gate_count} gates")
print(f"After: {optimized.gate_count} gates")
print(f"Parameters preserved: {optimized.num_parameters}")
```

## Circuit Optimization Passes

### Commutation-Based Optimization

```python
from quantum_engine import QuantumCircuit, CommutationOptimizer

qc = QuantumCircuit(3)
qc.cx(0, 1)
qc.cx(1, 2)
qc.cx(0, 1)  # Can be commuted past cx(1,2)
qc.cx(1, 2)  # Pairs with previous cx(0,1)

optimizer = CommutationOptimizer()
optimized = optimizer.run(
    qc,
    rules=["cx_cx_cancel", "cx_commute_rz", "h_commute_cx"]
)

print(f"Optimization removed {qc.gate_count - optimized.gate_count} gates")
```

### Template-Based Rewriting

```python
from quantum_engine import QuantumCircuit, TemplateRewriter

# Define a peephole template
templates = [
    {
        "pattern": ["h", "cx", "h"],
        "replacement": ["cx"],
        "qubits": [0, 1]
    },
    {
        "pattern": ["t", "t", "t", "t"],
        "replacement": ["x"],
        "qubits": [0]
    }
]

qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.h(0)  # Template: h-cx-h → cx
qc.t(0)
qc.t(0)
qc.t(0)
qc.t(0)  # Template: t^4 → x

rewriter = TemplateRewriter(templates)
optimized = rewriter.apply(qc)
print(f"Gate count: {optimized.gate_count}")
```

### Circuit Cutting for Large Systems

```python
from quantum_engine import QuantumCircuit, CircuitCutter

qc = QuantumCircuit(20)
# Build a complex circuit
for i in range(19):
    qc.cx(i, i + 1)
    qc.rz(0.5 * i, i)

cutter = CircuitCutter()
subcircuits = cutter.cut(
    qc,
    max_qubits_per_subcircuit=10,
    method="wire_cutting",
    num_cuts=3,
    classical_overhead_budget=1000
)

print(f"Original qubits: {qc.num_qubits}")
print(f"Subcircuits: {len(subcircuits)}")
for i, sub in enumerate(subcircuits):
    print(f"  Subcircuit {i}: {sub.num_qubits} qubits, {sub.gate_count} gates")

# Execute subcircuits and combine results
result = cutter.execute_and_combine(
    subcircuits,
    backend="statevector",
    shots=1024
)
print(f"Combined result: {result.expectation_value:.6f}")
```

## Error Correction

### Surface Code Implementation

```python
from quantum_engine import ErrorCorrection, SurfaceCode

# Create a distance-3 surface code
surface_code = SurfaceCode(distance=3)

# Encode a logical qubit
logical_circuit = surface_code.encode(logical_state=0)

print(f"Physical qubits: {surface_code.physical_qubits}")
print(f"Logical qubits: {surface_code.logical_qubits}")
print(f"Code distance: {surface_code.distance}")
print(f"Error threshold: {surface_code.error_threshold:.4f}")

# Syndrome extraction circuit
syndrome_circuit = surface_code.syndrome_extraction()
print(f"Syndrome circuit depth: {syndrome_circuit.depth}")

# Error correction step
corrected = surface_code.correct(
    syndrome_measurements=[1, 0, 1, 0, 0],
    error_rate=0.01
)
print(f"Corrected state fidelity: {corrected.fidelity:.4f}")
```

### Stabilizer Code Verification

```python
from quantum_engine import StabilizerCode, SyndromeDecoder

# Define the Steane [[7,1,3]] code
steane = StabilizerCode(
    name="steane",
    n=7,
    k=1,
    d=3,
    stabilizers=[
        "IIIXXXX",
        "IXXIIXX",
        "XIXIXIX",
        "IIIZZZZ",
        "IZZIIZZ",
        "ZIZIZIZ"
    ]
)

print(f"Code parameters: [[{steane.n}, {steane.k}, {steane.d}]]")
print(f"Number of stabilizers: {steane.num_stabilizers}")
print(f"Error correcting capability: {(steane.d - 1) // 2}")

decoder = SyndromeDecoder(steane)
# Simulate error and decode
error_pattern = "IIIZIII"  # X error on qubit 3
syndrome = steane.compute_syndrome(error_pattern)
correction = decoder.decode(syndrome)
print(f"Syndrome: {syndrome}")
print(f"Correction: {correction}")
```

### Error Correction Threshold Analysis

```python
from quantum_engine import ThresholdAnalysis, ErrorCorrection

# Analyze threshold for different error correction codes
codes = [
    SurfaceCode(distance=3),
    SurfaceCode(distance=5),
    SurfaceCode(distance=7),
    SteaneCode(),
    ShorCode()
]

analyzer = ThresholdAnalysis()
for code in codes:
    threshold = analyzer.estimate_threshold(
        code=code,
        physical_error_rates=[0.001, 0.005, 0.01, 0.05],
        num_shots=10000
    )
    print(f"{code.name}: threshold = {threshold:.4f}")

    # Plot logical error rate vs physical error rate
    rates = analyzer.logical_error_rate_curve(
        code=code,
        physical_rates=[0.001, 0.005, 0.01, 0.05, 0.1],
        shots=10000
    )
    for phys, log in zip([0.001, 0.005, 0.01, 0.05, 0.1], rates):
        print(f"  Physical: {phys:.3f} → Logical: {log:.6f}")
```

## Hardware Backend Integration

### Backend Abstraction Layer

```python
from quantum_engine import Backend, BackendProperties

class IBMBackend(Backend):
    def __init__(self, device_name="ibmq_manila"):
        self.device_name = device_name
        self.properties = BackendProperties.load(device_name)

    def get_coupling_map(self):
        return self.properties.coupling_map

    def get_native_gates(self):
        return ["cx", "id", "rz", "sx", "x"]

    def get_error_rates(self):
        return self.properties.error_rates

    def get_calibration_data(self):
        return self.properties.calibration

# Usage
backend = IBMBackend("ibmq_manila")
print(f"Qubits: {backend.properties.num_qubits}")
print(f"Coupling map: {backend.get_coupling_map()}")
print(f"T1 times: {backend.get_calibration_data().t1_times}")
```

### Multi-Backend Execution

```python
from quantum_engine import QuantumCircuit, MultiBackendRunner

qc = QuantumCircuit(5)
qc.h(0)
for i in range(4):
    qc.cx(i, i + 1)
qc.measure_all()

runner = MultiBackendRunner(
    backends=["statevector", "density_matrix", "qasm_simulator"],
    shots=4096,
    timeout_seconds=60
)

results = runner.run(qc)
for backend_name, result in results.items():
    print(f"{backend_name}:")
    print(f"  Fidelity: {result.fidelity:.4f}")
    print(f"  Execution time: {result.execution_time:.4f} s")
```

### Hardware Characterization

```python
from quantum_engine import RandomizedBenchmarking, GateSetTomography

# Randomized benchmarking for gate error characterization
rb = RandomizedBenchmarking(
    num_qubits=1,
    sequence_lengths=[2, 4, 8, 16, 32, 64, 128],
    num_samples=100,
    shots=1024
)

rb_result = rb.run(backend="density_matrix")
print(f"Average gate error: {rb_result.error_per_gate:.6f}")
print(f"Ancilla error: {rb_result.ancilla_error:.6f}")
print(f"SPAM error: {rb_result.spam_error:.6f}")

# Gate set tomography
gst = GateSetTomography(
    num_qubits=1,
    preparation_paulis=["I", "X", "Y", "Z"],
    measurement_paulis=["I", "X", "Y", "Z"]
)

gst_result = gst.run(backend="density_matrix")
print(f"Gate set fidelity: {gst_result.fidelity:.6f}")
print(f"Process tomography matrix:\n{gst_result.process_matrix}")
```

## Quantum State Manipulation

### State Preparation Circuits

```python
from quantum_engine import QuantumCircuit, StatePreparer

# Prepare an arbitrary quantum state
target_state = [0.5, 0.5, 0.5, 0.5]  # Equal superposition
preparer = StatePreparer(method="min_rotation")

circuit = preparer.prepare(target_state)
print(f"Preparation circuit depth: {circuit.depth}")
print(f"Gate count: {circuit.gate_count}")

# Verify state preparation
from quantum_engine import StatevectorSimulator
sim = StatevectorSimulator()
result = sim.run(circuit)
assert result.fidelity(target_state) > 0.999
```

### Quantum State Tomography

```python
from quantum_engine import QuantumCircuit, StateTomography

# Prepare a state and perform tomography
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
qc.rz(0.5, 0)

tomography = StateTomography(num_qubits=2)
reconstructed_state = tomography.reconstruct(
    qc,
    num_shots=1024,
    method="maximum_likelihood"
)

print(f"State fidelity: {reconstructed_state.fidelity:.4f}")
print(f"Purity: {reconstructed_state.purity:.4f}")
print(f"Entanglement: {reconstructed_state.entanglement:.4f}")
```

## Quantum Algorithm Primitives

### Quantum Phase Estimation

```python
from quantum_engine import QuantumCircuit, PhaseEstimation

# Estimate eigenvalue of a unitary operator
pe = PhaseEstimation(
    num_counting_qubits=8,
    unitary_gate="T",  # T gate has eigenvalue e^{i*pi/4}
    method="iterative"
)

circuit = pe.build_circuit()
simulator = QuantumEngine(backend="statevector")
result = simulator.run(circuit)

estimated_phase = result.most_probable_phase()
print(f"Estimated phase: {estimated_phase:.6f}")
print(f"Exact phase: {0.25:.6f}")  # pi/4 / 2pi = 1/8
print(f"Error: {abs(estimated_phase - 0.25):.8f}")
```

### Quantum Fourier Transform

```python
from quantum_engine import QuantumCircuit, QuantumFourierTransform

qft = QuantumFourierTransform(num_qubits=4)

# Create QFT circuit
qc = qft.build_circuit()
print(f"QFT depth: {qc.depth}")
print(f"QFT gate count: {qc.gate_count}")

# Apply QFT to a computational basis state
qc.hadamard(0)
qc.phase(0.5, 0)
qc.phase(0.25, 1)
qc.qft(range(4))

simulator = QuantumEngine(backend="statevector")
result = simulator.run(qc)
print(f"QFT output distribution: {result.probabilities}")
```

### Quantum Amplitude Estimation

```python
from quantum_engine import QuantumCircuit, AmplitudeEstimation

ae = AmplitudeEstimation(
    num_state_qubits=3,
    num_evaluation_qubits=4,
    objective_qubit=0,
    oracle="marked_states"
)

circuit = ae.build_circuit()
simulator = QuantumEngine(backend="statevector")
result = simulator.run(circuit)

amplitude = result.estimated_amplitude()
confidence = result.confidence_interval()
print(f"Estimated amplitude: {amplitude:.6f}")
print(f"Confidence interval: [{confidence[0]:.6f}, {confidence[1]:.6f}]")
```

## Quantum Circuits for Machine Learning

### Variational Quantum Classifier

```python
from quantum_engine import QuantumCircuit, VariationalClassifier
import numpy as np

# Build a variational quantum classifier circuit
def build_vqc_circuit(parameters, features):
    qc = QuantumCircuit(4)
    # Data encoding layer
    for i, f in enumerate(features):
        qc.rx(f, i)
    # Variational layer
    for layer in range(3):
        for i in range(4):
            qc.ry(parameters[layer * 4 + i], i)
        for i in range(3):
            qc.cx(i, i + 1)
    return qc

# Generate training data
X_train = np.random.rand(100, 4)
y_train = np.random.choice([0, 1], size=100)

# Train classifier
classifier = VariationalClassifier(
    circuit_fn=build_vqc_circuit,
    num_parameters=12,
    optimizer="adam",
    learning_rate=0.01,
    max_iterations=100,
    shots=1024
)

result = classifier.fit(X_train, y_train)
print(f"Training accuracy: {result.accuracy:.4f}")
print(f"Final cost: {result.cost:.4f}")
```

### Quantum Kernel Estimation

```python
from quantum_engine import QuantumKernel, QuantumCircuit

def feature_map(x1, x2, num_qubits=4):
    qc = QuantumCircuit(num_qubits)
    for i in range(num_qubits):
        qc.rx(x1[i % len(x1)], i)
        qc.ry(x2[i % len(x2)], i)
    for i in range(num_qubits - 1):
        qc.cx(i, i + 1)
    return qc

kernel = QuantumKernel(
    feature_map=feature_map,
    num_qubits=4,
    shots=1024,
    backend="statevector"
)

# Compute kernel matrix
X = np.random.rand(50, 4)
K = kernel.compute_kernel_matrix(X)
print(f"Kernel matrix shape: {K.shape}")
print(f"Kernel matrix condition number: {np.linalg.cond(K):.4f}")
```

## Advanced Topics

### Quantum Circuit Synthesis

```python
from quantum_engine import CircuitSynthesizer, UnitaryMatrix

# Synthesize a circuit from a target unitary
target_unitary = UnitaryMatrix.from_pauli_terms([
    (0.5, "IX"),
    (0.5, "ZI"),
    (0.3, "XX"),
    (0.2, "ZZ")
])

synthesizer = CircuitSynthesizer(method="grape")
circuit = synthesizer.synthesize(
    target_unitary,
    num_qubits=2,
    max_depth=50,
    target_fidelity=0.9999,
    optimization_rounds=1000
)

print(f"Synthesized circuit depth: {circuit.depth}")
print(f"Gate count: {circuit.gate_count}")
print(f"Achieved fidelity: {circuit.fidelity:.6f}")
```

### Quantum Circuit Verification

```python
from quantum_engine import CircuitVerifier, EquivalenceChecker

# Verify two circuits are equivalent
qc1 = QuantumCircuit(2)
qc1.h(0)
qc1.cx(0, 1)
qc1.rz(0.5, 0)

qc2 = QuantumCircuit(2)
qc2.h(0)
qc2.cx(0, 1)
qc2.rz(0.5, 0)

checker = EquivalenceChecker(method="simulation")
result = checker.check(qc1, qc2)
print(f"Circuits equivalent: {result.equivalent}")
print(f"Max fidelity difference: {result.fidelity_difference:.10f}")

# Formal verification
verifier = CircuitVerifier()
properties = verifier.verify_properties(qc1)
print(f"Unitarity verified: {properties.is_unitary}")
print(f"Reversibility verified: {properties.is_reversible}")
print(f"Conservation laws: {properties.conservation_laws}")
```

### Quantum Resource Estimation

```python
from quantum_engine import ResourceEstimator, AlgorithmResourceProfile

# Estimate resources for a quantum algorithm
estimator = ResourceEstimator()

# Shor's algorithm resource estimation
shor_profile = AlgorithmResourceProfile(
    name="shor",
    input_size=2048,  # 2048-bit RSA
    error_correction=SurfaceCode(distance=7),
    physical_qubit_overhead=1000
)

resources = estimator.estimate(shor_profile)
print(f"Logical qubits needed: {resources.logical_qubits}")
print(f"Physical qubits needed: {resources.physical_qubits}")
print(f"Circuit depth: {resources.circuit_depth}")
print(f"T-gate count: {resources.t_gate_count}")
print(f"Estimated runtime: {resources.estimated_runtime:.2f} seconds")

# VQE resource estimation
vqe_profile = AlgorithmResourceProfile(
    name="vqe",
    molecule="H2O",
    basis_set="sto-3g",
    ansatz="uccsd",
    error_correction=None,
    physical_qubit_overhead=1
)

vqe_resources = estimator.estimate(vqe_profile)
print(f"VQE qubits: {vqe_resources.qubits}")
print(f"VQE depth: {vqe_resources.circuit_depth}")
print(f"VQE shots needed: {vqe_resources.shots}")
```

### Quantum Benchmarking Suite

```python
from quantum_engine import QuantumBenchmark, BenchmarkSuite

# Run comprehensive benchmarking suite
suite = BenchmarkSuite(
    backends=["statevector", "density_matrix"],
    qubit_counts=[2, 4, 6, 8],
    num_shots=1024
)

results = suite.run(
    benchmarks=[
        "random_circuits",
        "mirror_circuits",
        "quantum_volume",
        "cross_entropy_benchmark",
        "entanglement_capacity"
    ]
)

for qubit_count, qubit_results in results.items():
    print(f"\nQubits: {qubit_count}")
    for benchmark_name, benchmark_result in qubit_results.items():
        print(f"  {benchmark_name}: {benchmark_result.value:.4f}")
        print(f"    Std: {benchmark_result.std:.6f}")
        print(f"    Time: {benchmark_result.execution_time:.4f}s")
```

### Circuit Debugging Tools

```python
from quantum_engine import CircuitDebugger, DiagnosticTools

# Debug a circuit for common issues
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.rz(0.0, 2)  # Zero rotation
qc.cx(2, 0)

debugger = CircuitDebugger()
diagnostics = debugger.diagnose(qc)

print("Diagnostic Results:")
print(f"  Gate count: {diagnostics.gate_count}")
print(f"  Circuit depth: {diagnostics.depth}")
print(f"  Unused qubits: {diagnostics.unused_qubits}")
print(f"  Redundant gates: {diagnostics.redundant_gates}")
print(f"  Potential optimizations: {diagnostics.optimization_hints}")

# Fix identified issues
fixed = debugger.auto_fix(
    qc,
    remove_identity_gates=True,
    merge_rotation_gates=True,
    optimize_gates=True
)
print(f"Fixed circuit depth: {fixed.depth}")
print(f"Fixed gate count: {fixed.gate_count}")
```

### Quantum Circuit Serialization

```python
from quantum_engine import QuantumCircuit, CircuitSerializer

# Serialize a circuit for storage or transmission
qc = QuantumCircuit(3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)

serializer = CircuitSerializer()

# Serialize to JSON
json_data = serializer.to_json(qc)
print(f"JSON size: {len(json_data)} bytes")

# Serialize to binary
binary_data = serializer.to_binary(qc)
print(f"Binary size: {len(binary_data)} bytes")

# Deserialize
restored_qc = serializer.from_json(json_data)
assert restored_qc.equiv(qc)

# Export to OpenQASM
qasm_str = serializer.to_qasm(qc)
print(f"OpenQASM output:\n{qasm_str}")

# Import from Qiskit
qiskit_circuit = serializer.from_qiskit(qiskit_qc)
```

### Noise-Aware Circuit Compilation

```python
from quantum_engine import QuantumCircuit, NoiseAwareCompiler, NoiseModel

# Define realistic noise model
noise = NoiseModel()
for qubit in range(5):
    noise.add_gate_error("cx", qubit, 0.01 + 0.005 * qubit)
    noise.add_readout_error(qubit, [0.02, 0.03])

compiler = NoiseAwareCompiler(
    noise_model=noise,
    optimization_level=3,
    routing_strategy="sabre"
)

qc = QuantumCircuit(5)
for i in range(4):
    qc.cx(i, i + 1)
    qc.rz(0.5 * i, i)
qc.measure_all()

compiled = compiler.compile(qc)
print(f"Original depth: {qc.depth}")
print(f"Compiled depth: {compiled.depth}")
print(f"Expected fidelity: {compiled.expected_fidelity:.4f}")
print(f"Routing overhead: {compiled.routing_ops} SWAPs")
```
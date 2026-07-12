---
name: "quantum-error-correction"
category: "quantum-computing"
version: "2.0.0"
tags: ["quantum-computing", "quantum-error-correction", "surface-code", "stabilizer", "repetition", "shor", "steane"]
---

# Quantum Error Correction

## Overview

The quantum-error-correction module implements quantum error correction (QEC) codes, syndrome decoding, fault-tolerant logical operations, and threshold analysis for protecting quantum information from noise. It provides implementations of the repetition code, Shor's 9-qubit code, Steane's 7-qubit code, the 5-qubit perfect code, surface codes (rotated and unrotated), color codes, and Bacon-Shor codes.

This module is designed for quantum hardware engineers, error correction researchers, and fault-tolerant quantum computing practitioners who need to simulate QEC circuits, analyze threshold behavior under realistic noise models, design syndrome extraction circuits, and benchmark logical vs physical error rates. The module includes comprehensive noise modeling, decoder implementations, and resource estimation tools.

The module supports both phenomenological and circuit-level noise models, enabling realistic evaluation of QEC performance on actual hardware. It provides tools for threshold estimation, logical error rate scaling analysis, and fault-tolerant gate implementation via transversal operations, magic state distillation, and lattice surgery. All code implementations include configurable syndrome extraction schedules and support for real-time decoding.

## Core Capabilities

- **Repetition Code**: Simplest QEC code for bit-flip error correction — encodes 1 logical qubit into n physical qubits with n-1 stabilizer measurements. Serves as a pedagogical tool and baseline for benchmarking.
- **Shor's 9-Qubit Code**: First complete quantum error correction code — corrects arbitrary single-qubit errors using 9 physical qubits with 8 stabilizer generators. Concatenates bit-flip and phase-flip repetition codes.
- **Steane's 7-Qubit Code**: CSS code based on classical Hamming [7,4,3] code — enables transversal implementation of the full Clifford group. Important for fault-tolerant quantum computation.
- **5-Qubit Perfect Code**: Smallest code that corrects arbitrary single-qubit errors — saturates the quantum Hamming bound with 5 physical qubits and 4 syndrome bits. Optimal in qubit count for single-error correction.
- **Surface Code**: Topological code with high error threshold (~1%) — supports local stabilizer measurements and is the leading candidate for fault-tolerant quantum computing. Includes both planar and toric code variants.
- **Rotated Surface Code**: Optimized surface code layout with fewer qubits per code distance — uses face and vertex stabilizers on a rotated lattice. Reduces qubit overhead by ~2x compared to unrotated surface code.
- **Color Code**: Topological code that supports transversal implementation of non-Clifford gates — useful for universal fault-tolerant computation without magic state distillation for some gate sets.
- **Syndrome Decoding**: Minimum Weight Perfect Matching (MWPM), Union-Find, and neural network decoders for real-time error correction. Includes decoding graph construction and fault-tolerant syndrome processing.
- **Fault-Tolerant Gates**: Transversal gate implementations, magic state distillation, and lattice surgery for surface codes. Includes T-gate implementation via magic state injection and state distillation protocols.
- **Threshold Analysis**: Compute error thresholds under depolarizing, circuit-level, and phenomenological noise models. Includes finite-size scaling analysis for accurate threshold estimation.
- **Logical Error Rate**: Estimate logical error rates as a function of code distance and physical error rate. Provides analytical formulas and Monte Carlo estimation for various code families.
- **Resource Estimation**: Calculate qubit overhead, circuit depth, and T-gate count for fault-tolerant circuits. Includes surface code overhead estimation for specific algorithms (Shor, Grover, VQE).

## Usage Examples

### Repetition Code Simulation

```python
from quantum_error_correction import (
    QECEngine, CodeType, NoiseModel, DecodingMethod,
    SyndromeCircuit
)

engine = QECEngine(
    code=CodeType.REPETITION,
    code_distance=5,
    noise=NoiseModel(depolarizing_rate=0.01)
)

# Encode a logical |0> state
encoded_state = engine.encode(logical_state=[1, 0])

# Inject errors
noisy_state = engine.inject_errors(encoded_state, error_rate=0.02)

# Syndrome measurement
syndrome = engine.measure_syndrome(noisy_state)
print(f"Syndrome: {syndrome}")
print(f"Errors detected: {engine.count_errors(syndrome)}")

# Decode and correct
corrected_state = engine.correct(noisy_state, syndrome=syndrome)
fidelity = engine.compute_fidelity(corrected_state, encoded_state)
print(f"Logical fidelity after correction: {fidelity:.4f}")
```

### Surface Code Simulation

```python
from quantum_error_correction import QECEngine, CodeType, NoiseModel, DecodingMethod

engine = QECEngine(
    code=CodeType.SURFACE,
    code_distance=3,
    noise=NoiseModel(
        depolarizing_rate=0.005,
        measurement_error=0.01,
        circuit_level=True
    )
)

# Run syndrome extraction rounds
rounds = 10
syndrome_history = engine.run_syndrome_rounds(num_rounds=rounds)
print(f"Syndrome rounds completed: {len(syndrome_history)}")

# Decode using MWPM
decoder = engine.get_decoder(method=DecodingMethod.MWPM)
correction = decoder.decode(syndrome_history)
print(f"Correction operator: {correction}")

# Compute logical error rate
logical_error = engine.compute_logical_error_rate(
    syndrome_history=syndrome_history,
    correction=correction
)
print(f"Logical error rate: {logical_error:.2e}")

# Threshold analysis
threshold = engine.find_threshold(
    code_distances=[3, 5, 7],
    physical_error_rates=[0.001, 0.003, 0.005, 0.007, 0.01, 0.015],
    num_trials=1000
)
print(f"Estimated threshold: {threshold:.4f}")
```

### Shor's 9-Qubit Code

```python
from quantum_error_correction import QECEngine, CodeType, NoiseModel

engine = QECEngine(
    code=CodeType.SHOR_9,
    code_distance=3,
    noise=NoiseModel(depolarizing_rate=0.005)
)

# Full QEC cycle
encoded = engine.encode(logical_state=[1, 0])
noisy = engine.inject_errors(encoded, error_rate=0.01)
syndrome = engine.measure_syndrome(noisy)
corrected = engine.correct(noisy, syndrome=syndrome)

print(f"Shor code syndrome: {syndrome}")
print(f"Bit-flip syndrome: {syndrome[:4]}")
print(f"Phase-flip syndrome: {syndrome[4:]}")
print(f"Fidelity: {engine.compute_fidelity(corrected, encoded):.4f}")
```

### Steane's 7-Qubit Code

```python
from quantum_error_correction import QECEngine, CodeType, NoiseModel, GateType

engine = QECEngine(
    code=CodeType.STEANE_7,
    code_distance=3,
    noise=NoiseModel(depolarizing_rate=0.003)
)

# Transversal Clifford gates
logical_circuit = engine.build_transversal_gates(
    gates=[GateType.H, GateType.S, GateType.CNOT]
)
print(f"Transversal circuit depth: {logical_circuit.depth}")
print(f"Physical qubits: {logical_circuit.num_qubits}")
print(f"Fault tolerance: {logical_circuit.fault_tolerant}")

# Syndrome extraction
syndrome_circuit = engine.build_syndrome_circuit()
print(f"Syndrome circuit depth: {syndrome_circuit.depth}")
print(f"Ancilla qubits: {syndrome_circuit.ancilla_qubits}")
```

### 5-Qubit Perfect Code

```python
from quantum_error_correction import QECEngine, CodeType, NoiseModel

engine = QECEngine(
    code=CodeType.FIVE_QUBIT,
    code_distance=3,
    noise=NoiseModel(depolarizing_rate=0.005)
)

# Encode
encoded = engine.encode(logical_state=[1, 0])
print(f"Encoded in {engine.num_physical_qubits} physical qubits")
print(f"Logical qubits: {engine.num_logical_qubits}")
print(f"Stabilizers: {engine.num_stabilizers}")

# Error correction cycle
noisy = engine.inject_errors(encoded, error_rate=0.01)
syndrome = engine.measure_syndrome(noisy)
corrected = engine.correct(noisy, syndrome=syndrome)
print(f"Syndrome weight: {sum(syndrome)}")
print(f"Corrected fidelity: {engine.compute_fidelity(corrected, encoded):.4f}")
```

### Fault-Tolerant Resource Estimation

```python
from quantum_error_correction import ResourceEstimator, CodeType, GateSet

estimator = ResourceEstimator(code=CodeType.SURFACE)

# Estimate resources for a quantum algorithm
resources = estimator.estimate(
    algorithm="shor",
    input_size=2048,
    target_logical_error_rate=1e-15,
    physical_error_rate=0.001,
    gate_set=GateSet.CLIFFORD_T
)

print(f"Physical qubits needed: {resources.physical_qubits}")
print(f"Logical qubits: {resources.logical_qubits}")
print(f"Code distance: {resources.code_distance}")
print(f"T-gates: {resources.t_gate_count}")
print(f"Circuit depth: {resources.circuit_depth}")
print(f"Overhead ratio: {resources.overhead_ratio:.0f}x")
```

## Architecture

```
quantum_error_correction/
  __init__.py
  codes/
    repetition.py           # Repetition code (bit-flip)
    shor_9.py               # Shor's 9-qubit code
    steane_7.py             # Steane's 7-qubit CSS code
    five_qubit.py           # 5-qubit perfect code
    surface.py              # Surface code (planar + toric)
    rotated_surface.py      # Rotated surface code
    color_code.py           # Color code (6.6.6 and 4.8.8)
    bacon_shor.py           # Bacon-Shor code
  decoders/
    mwpm.py                 # Minimum Weight Perfect Matching
    union_find.py           # Union-Find decoder
    neural_decoder.py       # Neural network decoder
    lookup.py               # Small-code lookup decoder
  circuits/
    syndrome_extraction.py  # Syndrome measurement circuits
    transversal_gates.py    # Transversal gate implementation
    lattice_surgery.py      # Lattice surgery operations
    magic_state.py          # Magic state distillation
  noise/
    phenomenological.py     # Phenomenological noise model
    circuit_level.py        # Circuit-level noise model
    depolarizing.py         # Depolarizing channel
    biased.py               # Biased noise models
  analysis/
    threshold.py            # Threshold estimation
    logical_error.py        # Logical error rate computation
    resource_estimate.py    # Resource estimation
    scaling.py              # Finite-size scaling analysis
  utils/
    stabilizer.py           # Stabilizer formalism utilities
    decoder_graph.py        # Decoding graph construction
    code_properties.py      # Code distance, weight, structure
```

## Best Practices

1. **Code distance selection**: Use code distance d >= 3 for single-error correction, d >= 5 for practical protection. The logical error rate scales as O((p/p_th)^((d+1)/2)) where p_th is the threshold. Higher distances provide exponential suppression but increase overhead.

2. **Threshold awareness**: Surface code threshold is ~1% under circuit-level noise. If your physical error rate is below threshold, increasing code distance exponentially suppresses logical errors. Above threshold, larger codes perform worse.

3. **Syndrome extraction**: Perform multiple rounds of syndrome extraction (at least d rounds for distance-d code) to account for measurement errors. Use syndrome history for correlated decoding across rounds.

4. **Decoder selection**: MWPM provides optimal decoding but O(n^3) complexity. Union-Find is near-optimal with O(n * alpha(n)) complexity — preferred for real-time decoding. Neural decoders offer fastest inference but require training data and may not generalize.

5. **Circuit-level noise**: Always simulate circuit-level noise (gate errors, measurement errors, idle errors) rather than just phenomenological noise. Circuit-level thresholds are ~10x lower than phenomenological, making this critical for realistic evaluation.

6. **Magic state distillation**: For universal fault-tolerant computation, T gates require magic state distillation with 15-to-1 or 20-to-4 protocols. Budget ~100x qubit overhead per T gate. Use catalyzed distillation for improved efficiency.

7. **Lattice surgery**: Use lattice surgery for surface code logical operations — it's more hardware-friendly than code switching. Merge and split operations implement CNOT and measurement. Include hook error mitigation in syndrome extraction.

8. **Code concatenation**: Concatenate surface codes with itself for extreme error suppression. Two-level concatenation with d=3 surface codes achieves ~10^-10 logical error rate from 10^-3 physical error rate. Higher concatenation levels provide diminishing returns.

9. **Color code advantages**: Use color codes when you need transversal non-Clifford gates (T gate). Color codes have higher overhead than surface codes but reduce magic state distillation cost. Consider color codes for T-gate-heavy algorithms.

10. **Benchmarking**: Compare logical error rates across code distances to verify threshold behavior. Plot p_L vs p_phys on log-log scale — curves should cross at the threshold. Use statistical bootstrapping for confidence intervals on threshold estimates.

## Performance Considerations

- **Qubit overhead**: Surface code requires ~(2d)^2 physical qubits per logical qubit for code distance d. For d=7 (practical protection), this is ~200 physical qubits per logical qubit. Plan hardware accordingly.
- **Decoding latency**: MWPM decoding takes O(n^3) time where n is the number of defects. For real-time decoding (required for memory experiments), target < 1 microsecond decoding latency. Union-Find achieves this.
- **Syndrome extraction overhead**: Each syndrome extraction round requires O(d^2) gates for a distance-d surface code. For d=7, this is ~50 gates per round. With d rounds per correction cycle, total overhead is O(d^3) gates per correction.
- **Magic state distillation throughput**: A single distillation factory produces ~1 magic state every ~100 microseconds. For algorithms requiring many T gates, multiple factories are needed. Budget factory count based on T-gate count and latency requirements.
- **Classical processing**: Real-time decoding requires significant classical processing power. For a distance-7 surface code with 1000 physical qubits, decoding requires ~10^9 floating-point operations per second. Use FPGAs or ASICs for production decoders.
- **Logical clock speed**: Fault-tolerant quantum computation is slower than physical computation due to syndrome extraction and decoding overhead. Typical logical clock speed is 1-10 kHz compared to 1-10 GHz for physical gates.

## Security Considerations

- **Fault tolerance guarantees**: QEC codes provide security guarantees against noise but not against adversarial attacks. Maliciously injected errors may bypass QEC if the adversary has access to physical qubits. Use authentication codes for adversarial settings.
- **Decoding correctness**: Incorrect decoding can propagate errors and cause logical failures. Verify decoder correctness through extensive testing and comparison with known-good decoders. Use fault-tolerant syndrome extraction to prevent error propagation.
- **Resource estimation sensitivity**: Quantum resource estimates for specific algorithms may reveal strategic capabilities (e.g., timeline for breaking RSA). Treat resource estimates as sensitive in competitive or national security contexts.
- **Implementation vulnerabilities**: QEC implementations may have side-channel vulnerabilities (timing, power consumption) that leak information about encoded quantum states. Use constant-time decoders and secure hardware for sensitive applications.
- **Supply chain security**: Quantum error correction hardware must be manufactured with verified components. Tampered qubits or classical control electronics could undermine QEC guarantees. Implement hardware authentication and integrity verification.

## Related Modules

- **quantum-algorithms** — Algorithms that require error-corrected qubits for scaling; resource estimation uses algorithm-specific circuit structures. Includes fault-tolerant implementations of Shor, Grover, and VQE.
- **quantum-simulation** — Noise models and channel simulation used to test QEC codes under realistic conditions. Includes circuit-level noise simulation for accurate threshold estimation.
- **quantum-optimization** — Optimization methods for decoder design, code construction, and resource allocation in QEC systems. Includes MWPM solver optimization and code parameter tuning.
- **quantum-cryptography** — QKD protocols that benefit from QEC for protecting quantum states in transit; entanglement distillation uses error correction codes for quantum communication.

## References

- Shor, P. W. (1995). Scheme for reducing decoherence in quantum computer memory. *Physical Review A*, 52(4), R2493.
- Steane, A. M. (1996). Error correcting codes in quantum theory. *Physical Review Letters*, 77(5), 793.
- Kitaev, A. Y. (2003). Fault-tolerant quantum computation by anyons. *Annals of Physics*, 303(1), 2-30.
- Fowler, A. G. et al. (2012). Surface codes: Towards practical large-scale quantum computation. *Physical Review A*, 86(3), 032324.
- Dennis, E. et al. (2002). Topological quantum memory. *Journal of Mathematical Physics*, 43(9), 4452-4505.
- Horsman, C. et al. (2012). Surface code quantum computing by lattice surgery. *New Journal of Physics*, 14(12), 123011.
- Campbell, E. T. & Howard, M. (2017). Unified framework for magic state distillation and multiqubit gate synthesis with reduced resource cost. *Physical Review A*, 95(2), 022316.

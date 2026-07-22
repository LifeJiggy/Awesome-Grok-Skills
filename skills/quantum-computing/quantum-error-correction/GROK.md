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

## Advanced Configuration

### Surface Code Configuration

```python
from quantum_error_correction import SurfaceCodeConfig, StabilizerSchedule

# Advanced surface code configuration
surface_config = SurfaceCodeConfig(
    code_distance=5,
    lattice_type="rotated",
    stabilizer_schedule=StabilizerSchedule(
        type="phenomenological",
        rounds=10,
        measurement_error=0.01,
        reset_error=0.001,
        hook_error_mitigation=True,
    ),
    decoder_config={
        "method": "mwpm",
        "matching_graph": "phenomenological",
        "decoding_rounds": 10,
        "real_time": True,
        "max_latency_us": 1.0,
    },
    logical_gates={
        "H": "transversal",
        "S": "magic_state",
        "T": "magic_state_distillation",
        "CNOT": "lattice_surgery",
    },
)

engine = QECEngine(
    code=CodeType.SURFACE,
    config=surface_config,
    noise=NoiseModel(depolarizing_rate=0.005),
)
```

### Decoder Configuration

```python
from quantum_error_correction import DecoderConfig, DecodingMethod

decoder_config = DecoderConfig(
    method=DecodingMethod.MWPM,
    matching_graph="phenomenological",
    edge_weights=" logarithmic",
    syndrome_processing="batch",
    batch_size=100,
    parallel_decoding=True,
    n_workers=4,
    latency_target_us=1.0,
    fallback_method=DecodingMethod.UNION_FIND,
)

decoder = engine.get_decoder(config=decoder_config)
```

### Magic State Distillation Configuration

```python
from quantum_error_correction import MagicStateConfig, DistillationProtocol

magic_config = MagicStateConfig(
    protocol=DistillationProtocol.REED_MULLER,
    input_error_rate=0.01,
    output_error_rate=1e-6,
    rounds=2,
    factory_size=16,
    catalyzed=True,
    resource_count={
        "physical_qubits": 16,
        "t_gates_per_distillation": 15,
        "circuit_depth": 100,
    },
)

distiller = engine.get_distiller(config=magic_config)
```

## Architecture Patterns

### Fault-Tolerant Circuit Pattern

```python
from quantum_error_correction import FTCircuitBuilder, GateSet

builder = FTCircuitBuilder(
    code=CodeType.SURFACE,
    code_distance=5,
    gate_set=GateSet.CLIFFORD_T,
)

# Build fault-tolerant circuit
circuit = builder.build(
    logical_circuit=logical_circuit,
    syndrome_extraction_rounds=10,
    magic_state_factory_count=4,
    lattice_surgery_operations=True,
)

print(f"Physical qubits: {circuit.physical_qubits}")
print(f"Logical qubits: {circuit.logical_qubits}")
print(f"Circuit depth: {circuit.depth}")
print(f"T-gates: {circuit.t_gate_count}")
```

### Resource Estimation Pattern

```python
from quantum_error_correction import ResourceEstimator, AlgorithmType

estimator = ResourceEstimator(code=CodeType.SURFACE)

# Estimate resources for algorithm
resources = estimator.estimate(
    algorithm=AlgorithmType.SHOR,
    input_size=2048,
    target_logical_error_rate=1e-15,
    physical_error_rate=0.001,
    code_distance_range=(3, 7, 9, 11),
)

print(f"Recommended code distance: {resources.recommended_distance}")
print(f"Physical qubits: {resources.physical_qubits}")
print(f"Logical qubits: {resources.logical_qubits}")
print(f"T-gates: {resources.t_gate_count}")
print(f"Circuit depth: {resources.circuit_depth}")
print(f"Overhead ratio: {resources.overhead_ratio:.0f}x")
```

### Threshold Analysis Pattern

```python
from quantum_error_correction import ThresholdAnalyzer, CodeFamily

analyzer = ThresholdAnalyzer(
    code_family=CodeFamily.SURFACE,
    noise_models=["depolarizing", "circuit_level", "phenomenological"],
    code_distances=[3, 5, 7, 9],
    physical_error_rates=[0.001, 0.003, 0.005, 0.007, 0.01, 0.015],
    num_trials=1000,
)

threshold = analyzer.find_threshold()
print(f"Estimated threshold: {threshold.value:.4f}")
print(f"Confidence interval: [{threshold.ci_lower:.4f}, {threshold.ci_upper:.4f}]")
print(f"Finite-size scaling exponent: {threshold.scaling_exponent:.2f}")
```

## Integration Guide

### Stim Integration

```python
from quantum_error_correction import StimAdapter

adapter = StimAdapter()

# Convert to Stim circuit
stim_circuit = adapter.to_stim(
    code=CodeType.SURFACE,
    code_distance=5,
    rounds=10,
)

# Run Stim simulation
detectors, observable = adapter.run_simulation(stim_circuit, num_shots=10000)

# Decode with PyMatching
from pymatching import Matching
matching = Matching.from_detector_error_model(adapter.get_detector_error_model())
correction = matching.decode_batch(detectors)
```

### Qiskit Integration

```python
from quantum_error_correction import QiskitQECAdapter

adapter = QiskitQECAdapter()

# Convert to Qiskit circuit
qiskit_circuit = adapter.to_qiskit(
    code=CodeType.SURFACE,
    code_distance=3,
    syndrome_extraction_rounds=5,
)

# Execute on Qiskit backend
from qiskit import execute
from qiskit.providers.aer import AerSimulator

simulator = AerSimulator()
result = execute(qiskit_circuit, simulator, shots=1024).result()
counts = result.get_counts()
```

## Performance Optimization

### Decoder Optimization

```python
from quantum_error_correction import DecoderOptimizer

optimizer = DecoderOptimizer(
    target_latency_us=1.0,
    parallel_decoding=True,
    n_workers=8,
    batch_processing=True,
    batch_size=100,
)

optimized_decoder = optimizer.optimize(decoder)
print(f"Original latency: {decoder.latency_us:.2f} us")
print(f"Optimized latency: {optimized_decoder.latency_us:.2f} us")
print(f"Speedup: {decoder.latency_us/optimized_decoder.latency_us:.1f}x")
```

### Syndrome Extraction Optimization

```python
from quantum_error_correction import SyndromeOptimizer

syndrome_opt = SyndromeOptimizer(
    schedule_optimization=True,
    parallel_measurements=True,
    measurement_grouping=True,
    error_filtering=True,
)

optimized_circuit = syndrome_opt.optimize(syndrome_circuit)
print(f"Original depth: {syndrome_circuit.depth()}")
print(f"Optimized depth: {optimized_circuit.depth()}")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Threshold Not Reached

**Symptom**: Logical error rate doesn't decrease with code distance

**Solution**:
```python
# Check physical error rate
if physical_error_rate > 0.01:
    print("Physical error rate above threshold")

# Use better decoder
decoder_config.method = DecodingMethod.MWPM

# Increase syndrome rounds
surface_config.stabilizer_schedule.rounds = 20
```

#### 2. High Decoding Latency

**Symptom**: Decoder too slow for real-time decoding

**Solution**:
```python
# Use Union-Find decoder
decoder_config.method = DecodingMethod.UNION_FIND

# Enable parallel decoding
decoder_config.parallel_decoding = True
decoder_config.n_workers = 8

# Use batch processing
decoder_config.batch_processing = True
```

#### 3. Magic State Distillation Too Slow

**Symptom**: Distillation bottleneck

**Solution**:
```python
# Use catalyzed distillation
magic_config.catalyzed = True

# Increase factory count
magic_config.factory_size = 32

# Use faster protocol
magic_config.protocol = DistillationProtocol.REED_MULLER
```

## API Reference

### Core Classes

#### `QECEngine`
```python
class QECEngine:
    def __init__(self, code: CodeType, code_distance: int, noise: NoiseModel) -> None: ...
    def encode(self, logical_state: List[int]) -> np.ndarray: ...
    def inject_errors(self, state: np.ndarray, error_rate: float) -> np.ndarray: ...
    def measure_syndrome(self, state: np.ndarray) -> np.ndarray: ...
    def correct(self, state: np.ndarray, syndrome: np.ndarray) -> np.ndarray: ...
    def compute_fidelity(self, corrected: np.ndarray, original: np.ndarray) -> float: ...
    def run_syndrome_rounds(self, num_rounds: int) -> List[np.ndarray]: ...
    def find_threshold(self, code_distances: List[int], physical_error_rates: List[float], num_trials: int) -> ThresholdResult: ...
```

## Data Models

### QEC Result Schema

```json
{
  "code": "surface",
  "code_distance": 5,
  "physical_error_rate": 0.005,
  "logical_error_rate": 1e-6,
  "fidelity": 0.999999,
  "syndrome_rounds": 10,
  "decoder": "mwpm",
  "decoding_latency_us": 0.8,
  "physical_qubits": 50,
  "logical_qubits": 1
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY quantum_error_correction/ /app/quantum_error_correction/
WORKDIR /app

ENV QEC_CODE=surface
ENV QEC_DISTANCE=5
ENV QEC_DECODER=mwpm

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from quantum_error_correction import health_check; health_check()"

CMD ["python", "-m", "quantum_error_correction.server"]
```

## Monitoring & Observability

### Metrics Collection

```python
from quantum_error_correction import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("qec_logical_error_rate", type="gauge")
collector.register_metric("qec_fidelity", type="gauge")
collector.register_metric("qec_decoding_latency", type="histogram")
collector.register_metric("qec_syndrome_rate", type="gauge")

collector.set("qec_logical_error_rate", result.logical_error_rate)
collector.set("qec_fidelity", result.fidelity)
collector.observe("qec_decoding_latency", result.decoding_latency_us)
collector.set("qec_syndrome_rate", syndrome_rate)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from quantum_error_correction import QECEngine, CodeType, NoiseModel

class TestSurfaceCode:
    def setup_method(self):
        self.engine = QECEngine(
            code=CodeType.SURFACE,
            code_distance=3,
            noise=NoiseModel(depolarizing_rate=0.005),
        )
    
    def test_encode_decode(self):
        encoded = self.engine.encode([1, 0])
        noisy = self.engine.inject_errors(encoded, error_rate=0.01)
        syndrome = self.engine.measure_syndrome(noisy)
        corrected = self.engine.correct(noisy, syndrome)
        fidelity = self.engine.compute_fidelity(corrected, encoded)
        assert fidelity > 0.9
    
    def test_threshold(self):
        threshold = self.engine.find_threshold(
            code_distances=[3, 5],
            physical_error_rates=[0.005, 0.01],
            num_trials=100,
        )
        assert 0.005 < threshold.value < 0.02
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API
- **Added**: Rotated surface code
- **Added**: Magic state distillation
- **Improved**: 2x faster decoding
- **Fixed**: Threshold estimation

## Glossary

| Term | Definition |
|------|------------|
| **Surface Code** | Topological code with high threshold |
| **Syndrome** | Error detection measurement |
| **MWPM** | Minimum Weight Perfect Matching decoder |
| **Magic State** | Resource state for non-Clifford gates |
| **Threshold** | Maximum physical error rate for QEC |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/quantum-ecc.git
cd quantum-ecc
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Quantum Error Correction Contributors

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

## Data Validation

### Code Validation

```python
from quantum_error_correction import CodeValidator

validator = CodeValidator()

# Validate code properties
validator.validate_code_distance(code, expected_distance=5)
validator.validate_stabilizers(code)
validator.validate_encoding(code)
```

### Syndrome Validation

```python
from quantum_error_correction import SyndromeValidator

validator = SyndromeValidator()

# Validate syndromes
validator.validate_syndrome_history(syndrome_history)
validator.validate_correction(correction, syndrome)
```

## Advanced Patterns

### Decoder Optimization Patterns

```python
from quantum_error_correction import DecoderOptimizer, DecoderStrategy

optimizer = DecoderOptimizer(
    strategy=DecoderStrategy.MWPM,
    parallel_decoding=True,
    n_workers=8,
    batch_processing=True,
    batch_size=100,
)

# Optimize decoder
optimized_decoder = optimizer.optimize(decoder)
print(f"Original latency: {decoder.latency_us:.2f} us")
print(f"Optimized latency: {optimized_decoder.latency_us:.2f} us")
print(f"Speedup: {decoder.latency_us/optimized_decoder.latency_us:.1f}x")
```

### Syndrome Processing Patterns

```python
from quantum_error_correction import SyndromeProcessor, ProcessingStrategy

processor = SyndromeProcessor(
    strategy=ProcessingStrategy.REAL_TIME,
    buffer_size=1000,
    processing_latency_us=1.0,
    error_filtering=True,
)

# Process syndromes
corrections = processor.process(syndrome_history)
print(f"Processed {len(corrections)} syndromes")
print(f"Corrections applied: {sum(1 for c in corrections if c.applied)}")
```

### Logical Gate Implementation Patterns

```python
from quantum_error_correction import LogicalGateImpl, GateStrategy

gate_impl = LogicalGateImpl(
    strategy=GateStrategy.LATTICE_SURGERY,
    code_distance=5,
    merge_time_us=10.0,
    split_time_us=10.0,
)

# Implement logical CNOT
cnot_circuit = gate_impl.implement_cnot(
    control_logical=logical_qubit_1,
    target_logical=logical_qubit_2,
)

print(f"CNOT circuit depth: {cnot_circuit.depth()}")
print(f"Physical qubits: {cnot_circuit.num_qubits}")
```

### Magic State Distillation Patterns

```python
from quantum_error_correction import MagicStateDistiller, DistillationStrategy

distiller = MagicStateDistiller(
    strategy=DistillationStrategy.REED_MULLER,
    input_error_rate=0.01,
    output_error_rate=1e-6,
    rounds=2,
    factory_size=16,
)

# Distill magic state
magic_state = distiller.distill()
print(f"Magic state fidelity: {magic_state.fidelity:.8f}")
print(f"Distillation time: {magic_state.time_us:.2f} us")
print(f"Resource overhead: {magic_state.overhead:.1f}x")
```

### Code Construction Patterns

```python
from quantum_error_correction import CodeConstructor, ConstructionStrategy

constructor = CodeConstructor(
    strategy=ConstructionStrategy.SURFACE_CODE,
    distance=5,
    lattice_type="rotated",
)

# Construct code
code = constructor.construct()
print(f"Code distance: {code.distance}")
print(f"Number of qubits: {code.num_qubits}")
print(f"Number of stabilizers: {code.num_stabilizers}")
print(f"Encoding rate: {code.rate:.4f}")
```

### Fault-Tolerant Circuit Patterns

```python
from quantum_error_correction import FTCircuitBuilder, FTStrategy

ft_builder = FTCircuitBuilder(
    strategy=FTStrategy.TRANSVERSAL_GATES,
    code_distance=5,
    magic_state_factory_count=4,
)

# Build fault-tolerant circuit
ft_circuit = ft_builder.build(logical_circuit)
print(f"Physical qubits: {ft_circuit.physical_qubits}")
print(f"Logical qubits: {ft_circuit.logical_qubits}")
print(f"Circuit depth: {ft_circuit.depth}")
print(f"T-gates: {ft_circuit.t_gate_count}")
```

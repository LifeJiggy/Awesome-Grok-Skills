---
name: "variational-circuits"
category: "quantum-ml"
version: "1.1.0"
tags: ["quantum-ml", "variational-circuits", "VQE", "QAOA", "ansatz", "barren-plateau", "optimization", "NISQ"]
---

# Variational Circuits

## Overview

Variational circuits are parameterized quantum circuits at the heart of near-term quantum algorithms. They combine a classical optimization loop with a quantum circuit whose gate angles are continuously tunable parameters. The quantum circuit evaluates a cost function for given parameters, and a classical optimizer updates the parameters to minimize that cost. This module provides primitives for constructing, optimizing, and analyzing variational circuits used in the Variational Quantum Eigensolver (VQE), Quantum Approximate Optimization Algorithm (QAOA), and general variational quantum algorithms (VQAs).

Key challenges addressed include barren plateau mitigation, circuit depth optimization, gradient computation, and hardware-aware compilation. Variational circuits are the foundational building block for quantum machine learning, quantum chemistry simulation, and combinatorial optimization on NISQ hardware. The parameterized circuit acts as a trainable quantum function that maps input parameters to output expectation values, enabling a hybrid quantum-classical optimization paradigm.

The expressivity of a variational circuit depends on its ansatz (architecture), entanglement structure, and parameter count. Finding the right balance between expressivity and trainability is critical: circuits that are too shallow cannot represent the target function, while circuits that are too deep suffer from barren plateaus where gradients vanish exponentially. This module provides tools for navigating this trade-off, including barren plateau analysis, circuit compression, and layer-wise training strategies.

## Core Capabilities

- **Circuit construction**: Build parameterized circuits with configurable gate sets, entanglement topologies, and circuit depth. Supports hardware-efficient, strongly entangling, and custom ansatze.
- **Ansatz libraries**: Pre-built ansatze including hardware-efficient, strongly entangling, QAOA, UCCSD (for chemistry), and custom user-defined architectures. Each ansatz targets specific problem domains.
- **Parameter initialization**: Multiple initialization strategies — uniform random, Xavier-like, identity blocks, and parameter-efficient schemes. Initialization affects trainability and convergence.
- **Gradient computation**: Parameter-shift rule, finite differences, and adjoint differentiation for exact gradient evaluation. The parameter-shift rule is hardware-compatible and noise-robust.
- **Optimization loops**: Classical optimizers (COBYLA, L-BFGS-B, Nelder-Mead, Adam, SPSA) with convergence monitoring. Supports gradient-free and gradient-based methods.
- **Barren plateau detection and mitigation**: Analyze gradient variance, apply layer-wise training, local cost functions, and identity initialization to avoid barren plateaus.
- **Circuit compression**: Reduce circuit depth and gate count through gate cancellation, commutation analysis, and template optimization. Critical for hardware execution.
- **Observable evaluation**: Compute expectation values of Pauli Hamiltonians and custom observables. Supports term grouping for measurement efficiency.

## Usage Examples

### Building a Basic Variational Circuit

```python
from variational_circuits import (
    VariationalCircuit,
    CircuitConfig,
    AnsatzType,
    EntanglementStrategy,
)

config = CircuitConfig(
    n_qubits=4,
    ansatz=AnsatzType.HARDWARE_EFFICIENT,
    n_layers=3,
    entanglement=EntanglementStrategy.LINEAR,
    rotation_gates=["RX", "RY", "RZ"],
    entangling_gate="CZ",
)

vc = VariationalCircuit(config)
vc.initialize(seed=42)
print(f"Circuit: {vc.n_parameters} parameters, depth {vc.estimated_depth}")
print(f"Gate counts: {vc.gate_counts()}")
print(f"2-qubit gate depth: {vc.two_qubit_depth()}")
```

### VQE for Ground State Energy

```python
from variational_circuits import VariationalCircuit, CircuitConfig, Hamiltonian

# Define a molecular Hamiltonian (e.g., H2)
hamiltonian = Hamiltonian.from_pauli({
    "II": -0.81261,
    "IZ": 0.17120,
    "ZI": -0.22279,
    "ZZ": 0.17120,
    "XX": 0.04532,
})

config = CircuitConfig(n_qubits=2, ansatz=AnsatzType.UCCSD, n_layers=1)
vc = VariationalCircuit(config)

# Optimize to find ground state energy
result = vc.minimize(
    hamiltonian=hamiltonian,
    optimizer="cobyla",
    maxiter=200,
    tolerance=1e-6,
)

print(f"Ground state energy: {result.optimal_value:.6f}")
print(f"Exact energy: -1.8572750302")
print(f"Chemical accuracy: {abs(result.optimal_value - (-1.857275)) < 0.0016}")
print(f"Convergence iterations: {result.n_iterations}")
print(f"Final gradient norm: {result.final_gradient_norm:.6e}")
```

### QAOA for MaxCut

```python
from variational_circuits import VariationalCircuit, CircuitConfig, AnsatzType, QAOACost

# Define MaxCut problem as a graph
edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2)]
cost = QAOACost.maxcut(n_qubits=4, edges=edges)

config = CircuitConfig(
    n_qubits=4,
    ansatz=AnsatzType.QAOA,
    n_layers=5,  # p=5 QAOA
)

vc = VariationalCircuit(config)
result = vc.minimize(
    hamiltonian=cost,
    optimizer="cobyla",
    maxiter=300,
)

print(f"MaxCut value: {-result.optimal_value:.1f}")
print(f"Optimal parameters: {result.optimal_parameters}")
print(f"Approximation ratio: {result.approximation_ratio:.4f}")
```

### Gradient Variance Analysis (Barren Plateau Detection)

```python
from variational_circuits import VariationalCircuit, CircuitConfig, barren_plateau_analysis

config = CircuitConfig(
    n_qubits=8,
    ansatz=AnsatzType.HARDWARE_EFFICIENT,
    n_layers=4,
)

vc = VariationalCircuit(config)
vc.initialize(seed=42)

analysis = barren_plateau_analysis(vc, n_samples=100)
print(f"Gradient variance: {analysis['gradient_variance']:.6e}")
print(f"Barren plateau risk: {analysis['risk_level']}")
print(f"Recommended action: {analysis['recommendation']}")
print(f"Critical depth: {analysis['critical_depth']}")
```

### Parameter-Shift Gradient Computation

```python
from variational_circuits import VariationalCircuit, CircuitConfig

config = CircuitConfig(n_qubits=4, n_layers=2)
vc = VariationalCircuit(config)
vc.initialize(seed=42)

# Compute exact gradients using parameter-shift rule
gradients = vc.compute_gradients(method="parameter_shift")
print(f"Gradient shape: {gradients.shape}")
print(f"Gradient norm: {np.linalg.norm(gradients):.6f}")
print(f"Max gradient: {np.max(np.abs(gradients)):.6f}")
print(f"Gradient variance: {np.var(gradients):.6e}")

# Compare with finite differences
gradients_fd = vc.compute_gradients(method="finite_difference", epsilon=1e-4)
discrepancy = np.max(np.abs(gradients - gradients_fd))
print(f"Max discrepancy with finite differences: {discrepancy:.6e}")
```

### Circuit Compression

```python
from variational_circuits import VariationalCircuit, CircuitConfig, compress_circuit

config = CircuitConfig(n_qubits=6, n_layers=5)
vc = VariationalCircuit(config)
vc.initialize(seed=42)

original_depth = vc.estimated_depth
original_gates = vc.estimated_gate_count

compressed = compress_circuit(vc, strategy="gate_cancellation")

print(f"Original: depth={original_depth}, gates={original_gates}")
print(f"Compressed: depth={compressed.estimated_depth}, gates={compressed.estimated_gate_count}")
print(f"Compression ratio: {compressed.estimated_gate_count / original_gates:.2%}")
```

### Layer-Wise Training for Barren Plateau Mitigation

```python
from variational_circuits import VariationalCircuit, CircuitConfig, LayerWiseTrainer

config = CircuitConfig(n_qubits=6, ansatz=AnsatzType.STRONGLY_ENTANGLING, n_layers=5)
vc = VariationalCircuit(config)

trainer = LayerWiseTrainer(
    circuit=vc,
    optimizer="adam",
    learning_rate=0.01,
    metric_callback=lambda epoch, loss, depth: print(
        f"Epoch {epoch}: loss={loss:.4f}, active_layers={depth}"
    ),
)

result = trainer.fit(
    cost_function=hamiltonian,
    max_total_iterations=500,
)

print(f"Final loss: {result.final_loss:.6f}")
print(f"Layers trained: {result.n_layers_trained}")
print(f"Total iterations: {result.total_iterations}")
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Variational Circuit Architecture                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Parameter   │───>│   Quantum    │───>│ Measurement  │      │
│  │  Vector θ    │    │   Circuit    │    │   (Pauli)    │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         ↑                                       │                │
│    [θ₁, θ₂, ..., θₚ]                     <O> = Tr(ρ·O)       │
│    p tunable parameters                          │                │
│                                                  ↓                │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Parameter   │<───│   Classical  │<───│  Cost        │      │
│  │  Update      │    │   Optimizer  │    │  Function    │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                    │                                   │
│    θ_new = θ - η∇C     COBYLA/Adam/SPSA                       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Ansatz Architecture Types                    │    │
│  │  ┌─────────────┐ ┌──────────────┐ ┌──────────────────┐ │    │
│  │  │Hardware-    │ │Strongly      │ │QAOA              │ │    │
│  │  │Efficient    │ │Entangling    │ │(cost+mixer)      │ │    │
│  │  └─────────────┘ └──────────────┘ └──────────────────┘ │    │
│  │  ┌─────────────┐ ┌──────────────┐ ┌──────────────────┐ │    │
│  │  │UCCSD        │ │Custom        │ │Data              │ │    │
│  │  │(chemistry)  │ │(user-defined)│ │Reuploading       │ │    │
│  │  └─────────────┘ └──────────────┘ └──────────────────┘ │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

The variational circuit architecture follows a closed-loop optimization pattern: parameters are fed into a quantum circuit, measurements extract an expectation value, a classical cost function evaluates the result, and a classical optimizer updates the parameters. This loop repeats until convergence.

## Best Practices

1. **Initialize near the identity**: Start parameters near zero so the initial circuit approximates the identity. This keeps gradients large and avoids barren plateaus in early training.

2. **Use local cost functions**: Global cost functions (measuring all qubits) are more susceptible to barren plateaus than local cost functions (measuring few-qubit operators). Prefer local observables when possible.

3. **Apply the parameter-shift rule**: Use the parameter-shift rule for exact gradients — it avoids the exponential cost of finite differences and works on hardware without access to the state vector.

4. **Start with shallow circuits**: Begin with the minimum number of variational layers needed to achieve acceptable performance. Increase depth only when the model is demonstrably underfitting.

5. **Monitor gradient variance**: Track gradient variance across parameters. Values below 10^-6 indicate barren plateau conditions. If detected, reduce circuit depth, switch ansatz, or apply layer-wise training.

6. **Use hardware-native gates**: Design circuits using only the gate set available on target hardware (e.g., {RZ, SX, CX} for IBM). This avoids costly decomposition during transpilation.

7. **Apply circuit cutting for deep circuits**: If the circuit exceeds hardware connectivity, use circuit knitting/cutting techniques rather than SWAP networks, which add significant depth.

8. **Validate against exact diagonalization**: For small systems (up to ~20 qubits), validate variational results against exact diagonalization to ensure the optimizer finds the correct solution.

9. **Use warm starts**: For iterative problems, initialize parameters from the solution of a simpler instance. This reduces the number of optimization iterations needed.

10. **Profile circuit execution**: Measure actual execution time on target hardware before scaling up. Circuit depth and gate count directly impact fidelity on noisy devices.

## Performance Considerations

- **Gradient cost**: The parameter-shift rule requires 2p circuit evaluations per gradient (p = parameters). For 500 parameters, one gradient step needs 1000 circuit executions.
- **Circuit depth limits**: On current hardware, circuits with >100 two-qubit gates suffer significant noise. Keep total two-qubit gate count under this threshold.
- **Classical optimizer choice**: Gradient-free optimizers (COBYLA, Nelder-Mead) are more noise-robust but scale poorly with parameters. Use SPSA for noisy, high-dimensional optimization.
- **Measurement overhead**: Each Pauli term in the Hamiltonian requires a separate measurement basis. Group commuting terms to reduce the number of measurement settings.
- **Simulation scaling**: Statevector simulation scales as O(2^n) in memory. For n > 25 qubits, use MPS simulators or tensor network methods.
- **Parallelization**: Circuit evaluations for different parameters can be parallelized. Use batch execution on quantum hardware to maximize throughput.

## Security Considerations

- **Parameter leakage**: Variational circuit parameters encode the solution. Protect parameter checkpoints from unauthorized access, especially for chemistry and optimization problems with commercial value.
- **Oracle attacks**: Variational algorithms may be vulnerable to oracle manipulation that biases the optimization landscape. Validate cost function integrity.
- **Reproducibility**: Quantum measurements are probabilistic. Use fixed seeds, sufficient shots, and documented protocols for reproducible results in regulated domains.
- **Hardware trust**: When using cloud quantum hardware, the provider may observe circuit structures. Use blind quantum computing for proprietary algorithms.
- **Side-channel attacks**: Circuit execution timing may reveal information about the optimization landscape. Implement constant-time execution for security-critical applications.

## Related Modules

- `quantum-neural-networks` — High-level hybrid models built on variational circuit primitives
- `quantum-kernel-methods` — Use variational circuits as quantum feature maps for kernel computation
- `quantum-generative-models` — Generative models that optimize variational circuits to learn distributions
- `quantum-data` — Data encoding circuits that feed into variational processing layers

## References

- Peruzzo, A., et al. (2014). A variational eigenvalue solver on a photonic quantum processor. Nature Communications, 5, 4213.
- Farhi, E., et al. (2014). A quantum approximate optimization algorithm. arXiv:1411.4028.
- McClean, J. R., et al. (2018). Barren plateaus in quantum neural network training landscapes. Nature Communications, 9(1), 4812.
- Cerezo, M., et al. (2021). Variational quantum algorithms. Nature Reviews Physics, 3(9), 625-644.
- Kandala, A., et al. (2017). Hardware-efficient variational quantum eigensolver for small molecules and quantum magnets. Nature, 549(7671), 242-246.
- Grimsley, H. R., et al. (2019). An adaptive variational algorithm for exact molecular simulations on a quantum computer. Nature Communications, 10(1), 3007.
- PennyLane VQE tutorial: https://pennylane.ai/qml/demos/tutorial_vqe.html
- Qiskit QAOA tutorial: https://qiskit.org/ecosystem/machine-learning/tutorials/05_torch_qgan.html

## Advanced Configuration

### Ansatz Architecture Configuration

```python
from variational_circuits import CircuitConfig, AnsatzType, EntanglementStrategy

# Advanced ansatz configuration
config = CircuitConfig(
    n_qubits=6,
    ansatz=AnsatzType.STRONGLY_ENTANGLING,
    n_layers=4,
    entanglement=EntanglementStrategy.CIRCULAR,
    rotation_gates=["RX", "RY", "RZ"],
    entangling_gate="CZ",
    parameter_initialization="xavier",
    parameter_bounds=(-3.14, 3.14),
    entanglement_pairs_per_layer=3,
    data_reuploading=True,
    reupload_strategy="every_layer",
)

vc = VariationalCircuit(config)
vc.initialize(seed=42)
print(f"Circuit: {vc.n_parameters} parameters, depth {vc.estimated_depth}")
print(f"Entanglement pairs: {vc.entanglement_pairs}")
print(f"Two-qubit gate depth: {vc.two_qubit_depth()}")
```

### Advanced Optimizer Configuration

```python
from variational_circuits import OptimizerConfig, LearningRateSchedule

# Advanced optimizer configuration
optimizer_config = OptimizerConfig(
    name="adam",
    learning_rate=0.01,
    beta1=0.9,
    beta2=0.999,
    epsilon=1e-8,
    weight_decay=1e-4,
    amsgrad=True,
    schedule=LearningRateSchedule(
        type="cosine_annealing",
        T_max=100,
        eta_min=1e-6,
        warmup_steps=10,
    ),
    gradient_clipping=1.0,
    gradient_clipping_method="global_norm",
)

# SPSA for noisy environments
spsa_config = OptimizerConfig(
    name="spsa",
    learning_rate=0.1,
    perturbation=0.1,
    alpha=0.602,
    gamma=0.101,
    blocking=True,
    allowed_increase=0.05,
    target_update_ratio=0.1,
)
```

### Hamiltonian Configuration

```python
from variational_circuits import Hamiltonian, PauliTerm

# Construct Hamiltonian from Pauli terms
hamiltonian = Hamiltonian.from_pauli_terms([
    PauliTerm(coefficient=0.5, operators=[("Z", 0), ("I", 1), ("I", 2), ("I", 3)]),
    PauliTerm(coefficient=-0.3, operators=[("I", 0), ("Z", 1), ("I", 2), ("I", 3)]),
    PauliTerm(coefficient=0.2, operators=[("X", 0), ("X", 1), ("I", 2), ("I", 3)]),
    PauliTerm(coefficient=0.1, operators=[("Z", 0), ("Z", 1), ("Z", 2), ("I", 3)]),
])

print(f"Hamiltonian: {hamiltonian.n_terms} terms")
print(f"Hilbert space dimension: {hamiltonian.hilbert_dimension}")
print(f"Exact ground state energy: {hamiltonian.exact_ground_state_energy:.6f}")
```

## Architecture Patterns

### Variational Algorithm Pipeline

```python
from variational_circuits import VariationalPipeline, PipelineStage

pipeline = VariationalPipeline(stages=[
    PipelineStage(
        name="hamiltonian_construction",
        type="classical",
        processor=lambda x: construct_hamiltonian(x),
    ),
    PipelineStage(
        name="ansatz_design",
        type="quantum",
        processor=lambda x: design_ansatz(x),
    ),
    PipelineStage(
        name="parameter_initialization",
        type="quantum",
        processor=lambda x: initialize_parameters(x),
    ),
    PipelineStage(
        name="optimization_loop",
        type="hybrid",
        processor=lambda x: run_optimization(x),
    ),
    PipelineStage(
        name="result_extraction",
        type="classical",
        processor=lambda x: extract_results(x),
    ),
])

result = pipeline.execute(hamiltonian)
```

### Layer-Wise Training Pattern

```python
from variational_circuits import LayerWiseTrainer, TrainingConfig

# Layer-wise training for barren plateau mitigation
trainer = LayerWiseTrainer(
    circuit=vc,
    optimizer="adam",
    learning_rate=0.01,
    layer_schedule="gradual",
    freeze_previous_layers=True,
    metric_callback=lambda epoch, loss, depth: print(
        f"Epoch {epoch}: loss={loss:.4f}, active_layers={depth}"
    ),
)

result = trainer.fit(
    cost_function=hamiltonian,
    max_total_iterations=500,
    layer_patience=20,
    min_improvement=1e-4,
)

print(f"Final loss: {result.final_loss:.6f}")
print(f"Layers trained: {result.n_layers_trained}")
```

### Circuit Compression Pattern

```python
from variational_circuits import CircuitCompressor, CompressionStrategy

compressor = CircuitCompressor(
    strategy=CompressionStrategy.GATE_CANCELLATION,
    target_depth=50,
    preserve_parameters=True,
    verify_correctness=True,
)

compressed = compressor.compress(vc.circuit)
print(f"Original depth: {vc.circuit.depth()}")
print(f"Compressed depth: {compressed.depth()}")
print(f"Compression ratio: {compressed.depth()/vc.circuit.depth():.2%}")

# Verify correctness
assert compressor.verify_equivalence(vc.circuit, compressed)
```

## Integration Guide

### Scikit-learn Integration

```python
from variational_circuits import VariationalCircuit, CircuitConfig
from sklearn.base import BaseEstimator, RegressorMixin

class QuantumRegressor(BaseEstimator, RegressorMixin):
    def __init__(self, config):
        self.config = config
        self.vc = VariationalCircuit(config)
    
    def fit(self, X, y):
        hamiltonian = self._construct_hamiltonian(X, y)
        self.vc.minimize(hamiltonian=hamiltonian, optimizer="cobyla", maxiter=200)
        return self
    
    def predict(self, X):
        return np.array([self.vc.evaluate(x) for x in X])
    
    def _construct_hamiltonian(self, X, y):
        # Construct Hamiltonian from data
        pass

# Use as sklearn estimator
regressor = QuantumRegressor(CircuitConfig(n_qubits=4, n_layers=2))
regressor.fit(X_train, y_train)
predictions = regressor.predict(X_test)
```

### PyTorch Integration

```python
import torch
from variational_circuits import VariationalCircuit, CircuitConfig

class VariationalLayer(torch.nn.Module):
    def __init__(self, config):
        super().__init__()
        self.vc = VariationalCircuit(config)
        self.vc.initialize()
        self.params = torch.nn.Parameter(
            torch.tensor(self.vc.parameters, dtype=torch.float32)
        )
    
    def forward(self, x):
        self.vc.set_parameters(self.params.numpy())
        return torch.tensor(self.vc.evaluate(x.numpy()), dtype=torch.float32)

# Build hybrid model
model = torch.nn.Sequential(
    torch.nn.Linear(10, 4),
    VariationalLayer(CircuitConfig(n_qubits=4, n_layers=2)),
    torch.nn.Linear(1, 1),
)
```

## Performance Optimization

### Circuit Optimization

```python
from variational_circuits import CircuitOptimizer

optimizer = CircuitOptimizer(
    optimization_level=3,
    target_gates=["cx", "u3"],
    coupling_map="ibmq_mumbai",
)

optimized = optimizer.optimize(vc.circuit)
print(f"Original depth: {vc.circuit.depth()}")
print(f"Optimized depth: {optimized.depth()}")
print(f"Gate reduction: {(1 - optimized.depth()/vc.circuit.depth())*100:.1f}%")
```

### Parallel Execution

```python
from variational_circuits import ParallelExecutor

executor = ParallelExecutor(
    max_workers=8,
    batch_size=100,
    backend="aer_simulator",
)

circuits = [create_circuit(params) for params in parameter_list]
results = executor.execute_batch(circuits)
print(f"Total time: {results.total_time_ms:.1f} ms")
print(f"Throughput: {results.circuits_per_second:.1f} circuits/s")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Barren Plateaus

**Symptom**: Gradient variance < 1e-6, training stalls

**Solution**:
```python
# Use identity initialization
config.parameter_initialization = "identity"

# Use local cost function
hamiltonian = Hamiltonian.from_local_terms([...])

# Use layer-wise training
trainer = LayerWiseTrainer(circuit=vc)
```

#### 2. Slow Convergence

**Symptom**: Many iterations without improvement

**Solution**:
```python
# Use warm start
config.initial_point = "hf"

# Use better optimizer
config.optimizer = "l-bfgs-b"

# Increase learning rate
config.learning_rate = 0.05
```

#### 3. Circuit Depth Too Large

**Symptom**: Exceeds hardware limits

**Solution**:
```python
# Compress circuit
compressed = compress_circuit(vc, strategy="gate_cancellation")

# Reduce layers
config.n_layers = 2

# Use hardware-efficient ansatz
config.ansatz = "hardware_efficient"
```

## API Reference

### Core Classes

#### `VariationalCircuit`
```python
class VariationalCircuit:
    def __init__(self, config: CircuitConfig) -> None: ...
    def initialize(self, seed: int = 42) -> None: ...
    def minimize(self, hamiltonian: Hamiltonian, optimizer: str = "cobyla", maxiter: int = 200) -> OptimizationResult: ...
    def evaluate(self, params: Optional[np.ndarray] = None) -> float: ...
    def compute_gradients(self, method: str = "parameter_shift") -> np.ndarray: ...
```

## Data Models

### Circuit Configuration Schema

```json
{
  "name": "variational_circuit_v1",
  "n_qubits": 4,
  "ansatz": "strongly_entangling",
  "n_layers": 3,
  "entanglement": "circular",
  "rotation_gates": ["RX", "RY", "RZ"],
  "entangling_gate": "CZ",
  "parameter_initialization": "xavier"
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY variational_circuits/ /app/variational_circuits/
WORKDIR /app

ENV VC_BACKEND=default.qubit
ENV VC_OPTIMIZATION_LEVEL=2

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from variational_circuits import health_check; health_check()"

CMD ["python", "-m", "variational_circuits.server"]
```

## Monitoring & Observability

### Metrics Collection

```python
from variational_circuits import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("vc_optimization_loss", type="gauge")
collector.register_metric("vc_gradient_norm", type="gauge")
collector.register_metric("vc_circuit_depth", type="gauge")
collector.register_metric("vc_execution_time", type="histogram")

collector.set("vc_optimization_loss", loss)
collector.set("vc_gradient_norm", grad_norm)
collector.set("vc_circuit_depth", vc.circuit.depth())
collector.observe("vc_execution_time", exec_time_ms)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from variational_circuits import VariationalCircuit, CircuitConfig

class TestVariationalCircuit:
    def setup_method(self):
        self.config = CircuitConfig(n_qubits=4, n_layers=2)
        self.vc = VariationalCircuit(self.config)
    
    def test_initialization(self):
        self.vc.initialize(seed=42)
        assert self.vc.n_parameters > 0
    
    def test_evaluate(self):
        self.vc.initialize()
        energy = self.vc.evaluate()
        assert isinstance(energy, float)
    
    def test_gradient_computation(self):
        self.vc.initialize()
        grads = self.vc.compute_gradients()
        assert grads.shape == (self.vc.n_parameters,)
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New `CircuitConfig` API
- **Added**: Layer-wise training support
- **Added**: Circuit compression utilities
- **Improved**: 2x faster gradient computation
- **Fixed**: Barren plateau detection

## Glossary

| Term | Definition |
|------|------------|
| **Ansatz** | Parameterized quantum circuit architecture |
| **Barren Plateau** | Exponential vanishing of gradients |
| **Hamiltonian** | Quantum observable representing energy |
| **Parameter-Shift Rule** | Exact gradient computation method |
| **Variational** | Hybrid classical-quantum optimization |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/variational-circuits.git
cd variational-circuits
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Variational Circuits Contributors

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

### Ansatz Design Patterns

```python
from variational_circuits import AnsatzDesigner, AnsatzStrategy

designer = AnsatzDesigner(
    strategy=AnsatzStrategy.HARDWARE_EFFICIENT,
    n_qubits=4,
    n_layers=3,
    rotation_gates=["RX", "RY", "RZ"],
    entangling_gate="CZ",
    entanglement="circular",
)

# Design ansatz
ansatz = designer.design()
print(f"Ansatz depth: {ansatz.circuit_depth}")
print(f"Parameters: {ansatz.n_parameters}")
print(f"Expressivity: {ansatz.expressivity:.4f}")
```

### Optimization Landscape Patterns

```python
from variational_circuits import LandscapeAnalyzer, LandscapeStrategy

analyzer = LandscapeAnalyzer(
    strategy=LandscapeStrategy.PARAMETER_SCAN,
    resolution=50,
    parameter_range=(-3.14, 3.14),
)

# Analyze landscape
landscape = analyzer.analyze(
    circuit=variational_circuit,
    cost_function=hamiltonian,
)

print(f"Landscape smoothness: {landscape.smoothness:.4f}")
print(f"Number of local minima: {landscape.local_minima_count}")
print(f"Barren plateau risk: {landscape.barren_plateau_risk}")
```

### Gradient Analysis Patterns

```python
from variational_circuits import GradientAnalyzer, GradientStrategy

analyzer = GradientAnalyzer(
    strategy=GradientStrategy.PARAMETER_SHIFT,
    shots=1024,
    concurrent_evaluations=4,
)

# Analyze gradients
gradient_analysis = analyzer.analyze(
    circuit=variational_circuit,
    parameters=initial_params,
    cost_function=hamiltonian,
)

print(f"Gradient norm: {gradient_analysis.gradient_norm:.6f}")
print(f"Gradient variance: {gradient_analysis.gradient_variance:.6e}")
print(f"Barren plateau risk: {gradient_analysis.barren_plateau_risk}")
```

### Circuit Compression Patterns

```python
from variational_circuits import CircuitCompressor, CompressionStrategy

compressor = CircuitCompressor(
    strategy=CompressionStrategy.GATE_CANCELLATION,
    target_depth=50,
    preserve_parameters=True,
    verify_correctness=True,
)

# Compress circuit
compressed = compressor.compress(variational_circuit)
print(f"Original depth: {variational_circuit.circuit.depth()}")
print(f"Compressed depth: {compressed.circuit.depth()}")
print(f"Compression ratio: {compressed.circuit.depth()/variational_circuit.circuit.depth():.2%}")
```

### Parameter Initialization Patterns

```python
from variational_circuits import ParameterInitializer, InitStrategy

initializer = ParameterInitializer(
    strategy=InitStrategy.IDENTITY_BLOCKS,
    parameter_range=(-0.1, 0.1),
    seed=42,
)

# Initialize parameters
params = initializer.initialize(variational_circuit)
print(f"Parameter range: [{params.min():.4f}, {params.max():.4f}]")
print(f"Parameter mean: {params.mean():.4f}")
print(f"Parameter std: {params.std():.4f}")
```

### Cost Function Design Patterns

```python
from variational_circuits import CostFunctionDesigner, CostStrategy

designer = CostFunctionDesigner(
    strategy=CostStrategy.LOCAL_OBSTACLES,
    locality=2,
    weight_type="adaptive",
)

# Design cost function
cost_function = designer.design(
    hamiltonian=hamiltonian,
    circuit=variational_circuit,
)

print(f"Cost function terms: {cost_function.num_terms}")
print(f"Locality: {cost_function.locality}")
print(f"Barren plateau resistance: {cost_function.barren_plateau_resistance:.4f}")
```

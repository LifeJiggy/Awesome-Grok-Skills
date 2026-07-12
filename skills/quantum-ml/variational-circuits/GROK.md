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

---
name: "quantum-neural-networks"
category: "quantum-ml"
version: "1.1.0"
tags: ["quantum-ml", "quantum-neural-networks", "QNN", "hybrid-models", "PennyLane", "variational", "classification", "regression"]
---

# Quantum Neural Networks

## Overview

Quantum Neural Networks (QNNs) combine parameterized quantum circuits with classical neural network layers to exploit quantum entanglement and superposition for machine learning tasks. QNNs map input data into quantum states, apply trainable unitary transformations, measure observables, and feed results back into classical optimization loops. This module provides tools for building, training, and evaluating hybrid quantum-classical models using PennyLane and Qiskit backends.

QNNs are particularly effective for classification on high-dimensional datasets, quantum simulation tasks, and problems with inherent quantum structure such as molecular property prediction. The parameterized quantum circuit acts as a highly expressive feature extractor that operates in a Hilbert space of dimension 2^n, where n is the number of qubits. This exponential state space enables QNNs to capture complex correlations that would require exponentially many parameters in classical neural networks. However, practical QNN training on NISQ hardware requires careful management of circuit depth, noise, and gradient behavior.

Hybrid quantum-classical architectures allow QNNs to leverage the strengths of both paradigms: quantum circuits for nonlinear feature extraction and entanglement-based correlation capture, and classical layers for post-processing, loss computation, and parameter updates. Common applications include molecular property prediction, drug discovery, materials science, financial modeling, and pattern recognition in quantum sensor data. The module supports both simulation-based training and execution on real quantum hardware through provider backends.

## Core Capabilities

- **Hybrid model construction**: Build quantum-classical neural networks with configurable ansatz circuits, encoding strategies, and measurement schemes. Supports PennyLane, Qiskit, and Cirq backends with automatic differentiation.
- **Parameter shift gradient computation**: Compute exact gradients of quantum circuits using the parameter-shift rule for backpropagation through quantum layers. Provides O(2p) circuit evaluations where p is the number of parameters.
- **Noise-aware training**: Train QNNs in the presence of depolarizing, amplitude damping, and readout noise with built-in mitigation. Supports zero-noise extrapolation, probabilistic error cancellation, and dynamical decoupling.
- **Circuit architecture search**: Automatically evaluate and compare architectures including hardware-efficient, strongly entangling, and hardware-native ansatze. Grid search and Bayesian optimization over architecture hyperparameters.
- **Multi-qubit entanglement strategies**: Configure linear, circular, full, and custom entanglement topologies for parameterized layers. Entanglement structure directly impacts model expressivity and trainability.
- **Measurement-based feature extraction**: Extract expectation values, variances, and probabilities from configurable Pauli observables. Supports Pauli-Z, Pauli-X, Pauli-Y, and tensor product measurements.
- **Checkpointer and warm-start**: Save and restore QNN parameters across training runs with automatic best-model tracking. Supports JSON and binary checkpoint formats with metadata logging.
- **Transfer learning**: Initialize QNN parameters from pre-trained models on related tasks. Supports partial parameter freezing for fine-tuning workflows.
- **Batch processing**: Efficient batched circuit execution with automatic batching of measurement shots across samples. Reduces quantum backend overhead for large datasets.

## Usage Examples

### Building a Simple QNN Classifier

```python
from quantum_neural_networks import (
    QuantumNeuralNetwork,
    QNNConfig,
    EncodingStrategy,
    AnsatzType,
    MeasurementBasis,
)

config = QNNConfig(
    n_qubits=4,
    n_layers=3,
    ansatz=AnsatzType.STRONGLY_ENTANGLING,
    encoding=EncodingStrategy.AMPLITUDE,
    measurement=MeasurementBasis.PAULI_Z,
    entanglement="circular",
    learning_rate=0.01,
    shots=None,  # analytic mode
)

qnn = QuantumNeuralNetwork(config)
qnn.initialize_parameters(seed=42)
print(f"Trainable parameters: {qnn.n_parameters}")
print(f"Circuit depth: {qnn.circuit_depth}")
print(f"Backend: {qnn.backend}")
```

### Training a QNN on Classification Data

```python
import numpy as np
from quantum_neural_networks import QuantumNeuralNetwork, QNNConfig, AnsatzType

# Generate spiral dataset
n_samples = 200
X, y = make_spiral(n_samples, n_classes=2, n_features=4)

config = QNNConfig(
    n_qubits=4,
    n_layers=2,
    ansatz=AnsatzType.HARDWARE_EFFICIENT,
    learning_rate=0.05,
    batch_size=32,
)

qnn = QuantumNeuralNetwork(config)

# Train with Adam optimizer
history = qnn.fit(
    X_train=X,
    y_train=y,
    epochs=50,
    optimizer="adam",
    callback=lambda epoch, loss: print(f"Epoch {epoch}: loss={loss:.4f}"),
)

# Evaluate
accuracy = qnn.score(X_test, y_test)
print(f"Test accuracy: {accuracy:.3f}")

# Cross-validate
cv_scores = qnn.cross_validate(X, y, k=5)
print(f"CV accuracy: {cv_scores.mean():.3f} +/- {cv_scores.std():.3f}")
```

### Custom Ansatz with Entanglement Map

```python
from quantum_neural_networks import QuantumNeuralNetwork, QNNConfig, EntanglementMap

# Define custom entanglement: pairs of qubits to entangle in each layer
entanglement = EntanglementMap(
    pairs=[(0, 1), (1, 2), (2, 3), (0, 3)],
    strategy="layered",
)

config = QNNConfig(
    n_qubits=4,
    n_layers=4,
    ansatz="custom",
    entanglement=entanglement,
    rotation_gates=["RX", "RY", "RZ"],
    entangling_gate="CNOT",
)

qnn = QuantumNeuralNetwork(config)
qnn.initialize_parameters(seed=42)

# Inspect circuit structure
print(qnn.circuit.draw())
print(f"Entanglement pairs per layer: {entanglement.pairs}")
print(f"Total two-qubit gates: {qnn.count_2q_gates()}")
```

### Noise-Aware Training on Simulated Hardware

```python
from quantum_neural_networks import QuantumNeuralNetwork, QNNConfig, NoiseModel

noise = NoiseModel(
    depolarizing_rate=0.005,
    readout_error_rate=0.02,
    t1=50e3,  # microseconds
    t2=70e3,
    gate_time_1q=35,
    gate_time_2q=300,
)

config = QNNConfig(
    n_qubits=6,
    n_layers=3,
    noise_model=noise,
    mitigation="zero_noise_extrapolation",
    shots=1024,
)

qnn = QuantumNeuralNetwork(config)
qnn.initialize_parameters(seed=42)

# Train with noise-aware optimizer
history = qnn.fit(
    X_train=X,
    y_train=y,
    epochs=30,
    optimizer="spsa",  # gradient-free optimizer for noisy environments
    noise_aware=True,
)
```

### Feature Encoding Strategies

```python
from quantum_neural_networks import (
    QuantumNeuralNetwork,
    QNNConfig,
    EncodingStrategy,
)

strategies = {
    "angle": EncodingStrategy.ANGLE,           # one qubit per feature
    "amplitude": EncodingStrategy.AMPLITUDE,    # 2^n features in n qubits
    "iqp": EncodingStrategy.IQP,               # instantaneous quantum polynomial
    "basis": EncodingStrategy.BASIS,            # computational basis encoding
}

for name, strategy in strategies.items():
    config = QNNConfig(
        n_qubits=4,
        encoding=strategy,
        n_features=8 if strategy == EncodingStrategy.AMPLITUDE else 4,
    )
    qnn = QuantumNeuralNetwork(config)
    print(f"{name}: {qnn.n_parameters} parameters, depth {qnn.circuit_depth}")
```

### Multi-Output Regression with Custom Observables

```python
from quantum_neural_networks import QuantumNeuralNetwork, QNNConfig, Observable

# Define custom observables for multi-output regression
observables = [
    Observable.tensor([("Z", 0), ("I", 1), ("I", 2), ("I", 3)]),
    Observable.tensor([("I", 0), ("Z", 1), ("I", 2), ("I", 3)]),
    Observable.tensor([("X", 0), ("X", 1), ("I", 2), ("I", 3)]),
]

config = QNNConfig(
    n_qubits=4,
    n_layers=3,
    observables=observables,
    output_dim=3,
    loss="mse",
)

qnn = QuantumNeuralNetwork(config)
qnn.fit(X_train, y_train, epochs=100)

# Predict with uncertainty estimation
predictions, uncertainties = qnn.predict_with_uncertainty(X_test, n_samples=100)
print(f"Prediction shape: {predictions.shape}")
print(f"Uncertainty shape: {uncertainties.shape}")
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Quantum Neural Network                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Classical    │───>│   Encoding   │───>│  Variational │      │
│  │  Input Layer  │    │   Circuit    │    │   Circuit    │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                    │                    │              │
│    Feature scaling     Data encoding      Parameterized gates   │
│    Normalization       Angle/Amplitude    Rotation + Entangle   │
│                                                          │       │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐      │
│  │  Classical    │<───│ Measurement  │<───│   Quantum    │      │
│  │  Output Layer │    │   Layer      │    │   Circuit    │      │
│  └──────────────┘    └──────────────┘    └──────────────┘      │
│         │                    │                                   │
│    Activation          Pauli observables                        │
│    Post-processing     Expectation values                       │
│    Loss computation    Probabilities                            │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              Classical Optimization Loop                 │    │
│  │  ┌─────────┐  ┌──────────┐  ┌───────────────────┐     │    │
│  │  │  Adam   │─>│ Gradient │─>│ Parameter Update  │     │    │
│  │  │  SPSA   │  │  (PSR)   │  │ (momentum, LR)    │     │    │
│  │  └─────────┘  └──────────┘  └───────────────────┘     │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

The architecture follows a layered pipeline: classical data is preprocessed and encoded into quantum states, processed through parameterized quantum circuits, measured to extract classical information, and fed into classical output layers. The training loop uses gradient-based optimization with exact gradients computed via the parameter-shift rule.

## Best Practices

1. **Start with shallow circuits**: Begin with 1-2 variational layers and increase only when underfitting. Deep circuits suffer from barren plateaus where gradients vanish exponentially with depth.

2. **Choose encoding carefully**: Amplitude encoding packs exponentially more features per qubit but is harder to implement on hardware. Angle encoding is hardware-friendly but limited to one feature per qubit per rotation axis.

3. **Use parameter-shift rule for gradients**: Avoid finite-difference approximations. The parameter-shift rule gives exact gradients with a factor of 2 overhead in circuit evaluations.

4. **Monitor gradient variance**: Track gradient variance across parameters during training. If variance drops below 1e-6, the circuit is entering a barren plateau — reduce depth or change initialization.

5. **Apply noise mitigation early**: If targeting real hardware, incorporate noise models from the start. Post-hoc mitigation often cannot recover from noise-induced training failures.

6. **Regularize with entanglement constraints**: Fully entangled circuits maximize expressivity but can overfit. Start with linear or circular entanglement and increase only when needed.

7. **Use bounded parameter initialization**: Initialize parameters uniformly in [-pi, pi] to ensure the circuit explores the full Bloch sphere. Narrower ranges bias the initial circuit.

8. **Validate on classical baselines**: Always compare QNN performance against equivalent classical networks (same feature dimension, similar parameter count) to verify quantum advantage.

9. **Leverage batching for simulation**: When training on simulators, use batched circuit execution to parallelize parameter evaluations and reduce wall-clock time significantly.

10. **Save checkpoints frequently**: Quantum optimization landscapes are complex with many local minima. Save parameters at regular intervals to recover from training instability.

## Performance Considerations

- **Parameter-shift rule cost**: Each gradient evaluation requires 2p circuit executions (p = number of parameters). For 100 parameters, one gradient step needs 200 circuit evaluations. Use mini-batching to reduce per-evaluation cost.
- **Simulation vs hardware**: Statevector simulation scales as O(2^n) in memory and time. For n > 25 qubits, consider matrix product state (MPS) simulators or execute on real hardware.
- **Shot noise**: Finite measurement shots introduce variance in gradient estimates. Use at least 1024 shots for reliable gradients; 4096+ for high-precision training.
- **Entanglement depth**: Each entangling gate adds ~10-100x more classical simulation cost. Minimize two-qubit gate count while maintaining expressivity.
- **Batch size selection**: Larger batches reduce gradient variance but increase quantum backend latency. For hardware execution, batch sizes of 8-32 provide a good balance.
- **Circuit optimization**: Pre-optimize circuits by removing redundant gates, combining consecutive rotations, and using hardware-native gate sets to reduce execution time.

## Security Considerations

- **Model extraction attacks**: QNNs deployed as cloud APIs may be vulnerable to model extraction through repeated querying. Implement rate limiting and query monitoring to detect adversarial patterns.
- **Data privacy**: Quantum circuits trained on sensitive data encode information in their parameters. Ensure parameter checkpoints are encrypted at rest and access-controlled.
- **Adversarial inputs**: Quantum models can be sensitive to adversarial perturbations in input data. Test robustness against bounded perturbations in the input feature space.
- **Hardware backdoors**: When using cloud quantum hardware, ensure end-to-end encryption of circuit specifications. Circuit structure and parameters may reveal proprietary model architecture.
- **Reproducibility risks**: Quantum measurements are inherently probabilistic. Use fixed random seeds and sufficient shot counts for reproducible results in security-critical applications.

## Related Modules

- `variational-circuits` — Low-level parameterized circuit construction and optimization primitives used by QNN layers
- `quantum-kernel-methods` — Alternative quantum ML approach using kernel evaluation instead of variational circuits
- `quantum-generative-models` — Generative quantum models that share ansatz design patterns with QNNs
- `quantum-data` — Data encoding, encoding validation, and quantum dataset management utilities

## References

- Farhi, E., & Neven, H. (2018). Classification with Quantum Neural Networks on Near Term Processors. arXiv:1802.06002.
- Schuld, M., et al. (2020). Circuit-centric quantum classifiers. Physical Review A, 101(3), 032308.
- Pérez-Salinas, A., et al. (2020). Data re-uploading for a universal quantum classifier. Quantum, 4, 226.
- Abbas, A., et al. (2021). The power of quantum neural networks. Nature Computational Science, 1(6), 403-409.
- Skolik, A., et al. (2021). Quantum neural networks in the NISQ era: a review. arXiv:2104.10066.
- PennyLane documentation: https://pennylane.ai/qml/
- Qiskit Machine Learning: https://qiskit.org/machine-learning/

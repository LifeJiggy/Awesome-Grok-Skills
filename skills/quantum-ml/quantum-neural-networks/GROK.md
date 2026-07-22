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

## Advanced Configuration

### Backend Selection Matrix

| Backend | Max Qubits | Noise Model | Gradient Method | Use Case |
|---------|-----------|-------------|-----------------|----------|
| `default.qubit` | 25+ | None | Analytic | Development, validation |
| `lightning.qubit` | 30+ | None | Adjoint | Large-scale simulation |
| `ibm_qasm_simulator` | 32 | Configurable | Parameter-shift | Noisy simulation |
| `ibm_brisbane` | 127 | Hardware | Parameter-shift | Real hardware testing |
| `ionq_harmony` | 11 | IonQ noise | Parameter-shift | Ion trap algorithms |
| `amazon_braket_sv` | 25 | None | Adjoint | AWS ecosystem |

### Circuit Architecture Configuration

```python
from quantum_neural_networks import CircuitArchitecture, LayerConfig

# Define a custom circuit architecture
arch = CircuitArchitecture(
    name="custom_hybrid",
    encoding_layers=[
        LayerConfig(type="angle_encoding", axis="y", n_features=4),
        LayerConfig(type="amplitude_encoding", n_features=8),
    ],
    variational_layers=[
        LayerConfig(type="strongly_entangling", n_rotations=3, entanglement="circular"),
        LayerConfig(type="hardware_efficient", entanglement="linear"),
    ],
    measurement_config={
        "basis": "pauli_z",
        "shots": 1024,
        "mitigation": "zero_noise_extrapolation",
    }
)

qnn = QuantumNeuralNetwork.from_architecture(arch)
```

### Advanced Optimizer Configuration

```python
from quantum_neural_networks import OptimizerConfig, LearningRateSchedule

# Configure advanced optimizer
optimizer_config = OptimizerConfig(
    name="adam",
    learning_rate=0.01,
    beta1=0.9,
    beta2=0.999,
    epsilon=1e-8,
    weight_decay=1e-4,
    schedule=LearningRateSchedule(
        type="cosine_annealing",
        T_max=100,
        eta_min=1e-6,
    ),
    gradient_clipping=1.0,
    warmup_steps=10,
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
)
```

### Noise Model Configuration

```python
from quantum_neural_networks import NoiseConfig, ThermalNoise, ReadoutNoise

noise_config = NoiseConfig(
    depolarizing=0.005,
    thermal=ThermalNoise(
        t1=50e3,  # microseconds
        t2=70e3,
        gate_time_1q=35,
        gate_time_2q=300,
    ),
    readout=ReadoutNoise(
        assignment_error=[[0.98, 0.02], [0.01, 0.99]],
    ),
    crosstalk_rate=0.001,
)

config = QNNConfig(
    n_qubits=6,
    n_layers=3,
    noise_model=noise_config,
    mitigation="dynamical_decoupling",
)
```

## Architecture Patterns

### Pipeline Pattern for Multi-Stage QNN

```python
from quantum_neural_networks import QNNPipeline, PipelineStage

# Multi-stage QNN with preprocessing
pipeline = QNNPipeline(stages=[
    PipelineStage(
        name="preprocessing",
        type="classical",
        processor=lambda x: normalize_features(x),
    ),
    PipelineStage(
        name="quantum_encoder",
        type="quantum",
        processor=lambda x: encode_amplitude(x),
    ),
    PipelineStage(
        name="variational_layer",
        type="quantum",
        processor=lambda x: apply_variational_circuit(x),
    ),
    PipelineStage(
        name="measurement",
        type="quantum",
        processor=lambda x: measure_pauli_z(x),
    ),
    PipelineStage(
        name="postprocessing",
        type="classical",
        processor=lambda x: apply_softmax(x),
    ),
])

result = pipeline.execute(X_train)
```

### Ensemble Pattern for Quantum-Classical Hybrid

```python
from quantum_neural_networks import QNNEnsemble, EnsembleStrategy

# Build ensemble of QNNs with different architectures
ensemble = QNNEnsemble(
    models=[
        QuantumNeuralNetwork(QNNConfig(n_qubits=4, ansatz="hardware_efficient")),
        QuantumNeuralNetwork(QNNConfig(n_qubits=4, ansatz="strongly_entangling")),
        QuantumNeuralNetwork(QNNConfig(n_qubits=4, ansatz="custom")),
    ],
    strategy=EnsembleStrategy.STACKING,
    meta_learner="logistic_regression",
)

ensemble.fit(X_train, y_train)
accuracy = ensemble.score(X_test, y_test)
print(f"Ensemble accuracy: {accuracy:.3f}")
```

### Callback Pattern for Training Monitoring

```python
from quantum_neural_networks import TrainingCallback, CallbackEvent

class MonitoringCallback(TrainingCallback):
    def on_epoch_end(self, epoch, logs):
        if logs['gradient_variance'] < 1e-6:
            print(f"Barren plateau detected at epoch {epoch}")
            self.model.reduce_depth()
    
    def on_batch_end(self, batch, logs):
        if logs['loss'] > 10 * self.initial_loss:
            print(f"Loss explosion at batch {batch}")
            self.model.clip_gradients(1.0)

callback = MonitoringCallback()
qnn.fit(X_train, y_train, callbacks=[callback])
```

### Checkpoint and Resume Pattern

```python
from quantum_neural_networks import CheckpointManager

# Save checkpoints during training
checkpoint_mgr = CheckpointManager(
    save_dir="./checkpoints",
    save_freq=10,  # every 10 epochs
    keep_last=5,
    save_optimizer=True,
)

qnn.fit(
    X_train, y_train,
    epochs=100,
    callbacks=[checkpoint_mgr],
)

# Resume from checkpoint
latest = checkpoint_mgr.latest()
qnn.load_checkpoint(latest)
qnn.fit(X_train, y_train, epochs=50, initial_epoch=latest.epoch)
```

## Integration Guide

### Scikit-learn Integration

```python
from quantum_neural_networks import QuantumNeuralNetwork, QNNConfig
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

# QNN as sklearn estimator
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('qnn', QuantumNeuralNetwork(QNNConfig(n_qubits=4, n_layers=2)))
])

# Hyperparameter search
param_grid = {
    'qnn__n_layers': [2, 3, 4],
    'qnn__learning_rate': [0.01, 0.05, 0.1],
    'qnn__ansatz': ['hardware_efficient', 'strongly_entangling'],
}

search = GridSearchCV(pipeline, param_grid, cv=3, scoring='accuracy')
search.fit(X_train, y_train)
print(f"Best params: {search.best_params_}")
print(f"Best score: {search.best_score_:.3f}")
```

### PyTorch Integration

```python
import torch
from quantum_neural_networks import QuantumNeuralNetwork, QNNConfig

# Wrap QNN as PyTorch module
class QuantumLayer(torch.nn.Module):
    def __init__(self, config):
        super().__init__()
        self.qnn = QuantumNeuralNetwork(config)
        self.qnn.initialize_parameters()
    
    def forward(self, x):
        return self.qnn.forward(x)

# Build hybrid model
model = torch.nn.Sequential(
    torch.nn.Linear(10, 4),
    QuantumLayer(QNNConfig(n_qubits=4, n_layers=2)),
    torch.nn.Linear(1, 1),
)

optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
```

### TensorFlow/Keras Integration

```python
import tensorflow as tf
from quantum_neural_networks import QuantumNeuralNetwork, QNNConfig

# Custom Keras layer
class QuantumLayer(tf.keras.layers.Layer):
    def __init__(self, config):
        super().__init__()
        self.qnn = QuantumNeuralNetwork(config)
        self.qnn.initialize_parameters()
    
    def call(self, inputs):
        return self.qnn.forward(inputs.numpy())

# Build model
model = tf.keras.Sequential([
    tf.keras.layers.Dense(4, activation='relu'),
    QuantumLayer(QNNConfig(n_qubits=4, n_layers=2)),
    tf.keras.layers.Dense(1, activation='sigmoid'),
])
```

## Performance Optimization

### Circuit Execution Optimization

```python
from quantum_neural_networks import CircuitOptimizer

optimizer = CircuitOptimizer(
    optimization_level=3,
    target_gates=["cx", "u3"],
    coupling_map="ibmq_mumbai",
)

# Optimize QNN circuit
optimized_circuit = optimizer.optimize(qnn.circuit)
print(f"Original depth: {qnn.circuit.depth()}")
print(f"Optimized depth: {optimized_circuit.depth()}")
print(f"Gate reduction: {(1 - optimized_circuit.depth()/qnn.circuit.depth())*100:.1f}%")
```

### Batch Processing Optimization

```python
from quantum_neural_networks import BatchProcessor

processor = BatchProcessor(
    batch_size=32,
    n_workers=4,
    prefetch_factor=2,
)

# Process large datasets efficiently
results = processor.process_batch(
    model=qnn,
    data=X_large,
    strategy="parallel_circuits",
)
print(f"Processed {len(results)} samples in {results.elapsed_time:.1f}s")
print(f"Throughput: {results.samples_per_second:.1f} samples/s")
```

### Memory Optimization for Large Datasets

```python
from quantum_neural_networks import MemoryOptimizer

mem_opt = MemoryOptimizer(
    strategy="gradient_checkpointing",
    checkpoint_every=5,
    offload_to_disk=True,
    disk_path="/fast_ssd/qnn_cache",
)

# Memory-efficient training
qnn.fit(
    X_large, y_large,
    epochs=50,
    memory_optimizer=mem_opt,
)
```

### Parameter Reuse Optimization

```python
from quantum_neural_networks import ParameterSharing

# Share parameters across layers for efficiency
sharing = ParameterSharing(
    strategy="circular",
    n_unique_params=10,
    n_layers=5,
)

config = QNNConfig(
    n_qubits=4,
    n_layers=5,
    parameter_sharing=sharing,
)

qnn = QuantumNeuralNetwork(config)
print(f"Unique parameters: {qnn.n_unique_parameters}")
print(f"Total parameters: {qnn.n_total_parameters}")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Barren Plateaus Detected

**Symptom**: Gradient variance drops below 1e-6, training stalls

**Solution**:
```python
from quantum_neural_networks import QuantumNeuralNetwork, QNNConfig

# Reduce circuit depth
config = QNNConfig(
    n_qubits=4,
    n_layers=2,  # Reduce from 5
    ansatz="hardware_efficient",
    initialization="identity",  # Initialize near identity
)

# Or use local cost function
config.measurement = "local_pauli_z"  # Instead of global
```

#### 2. Training Loss Oscillates

**Symptom**: Loss bounces between values without converging

**Solution**:
```python
# Reduce learning rate
config.learning_rate = 0.005  # From 0.05

# Use gradient clipping
config.gradient_clipping = 1.0

# Switch to SPSA for noisy environments
config.optimizer = "spsa"
config.spsa_perturbation = 0.1
```

#### 3. Circuit Depth Too Large

**Symptom**: Circuit exceeds hardware limits, transpilation fails

**Solution**:
```python
from quantum_neural_networks import compress_circuit

# Compress circuit
compressed = compress_circuit(
    qnn.circuit,
    strategy="gate_cancellation",
    target_depth=100,
)
qnn.circuit = compressed
```

#### 4. Measurement Statistics Insufficient

**Symptom**: High variance in expectation values

**Solution**:
```python
config = QNNConfig(
    n_qubits=4,
    shots=4096,  # Increase from 1024
    measurement_mitigation=True,
    readout_mitigation_shots=2048,
)
```

#### 5. Overfitting on Small Datasets

**Symptom**: Training accuracy high, test accuracy low

**Solution**:
```python
config = QNNConfig(
    n_qubits=4,
    n_layers=2,  # Reduce complexity
    regularization="l2",
    regularization_strength=0.01,
    dropout=0.1,
)
```

## API Reference

### Core Classes

#### `QuantumNeuralNetwork`
Main entry point for QNN construction and training.

```python
class QuantumNeuralNetwork:
    def __init__(self, config: QNNConfig) -> None: ...
    
    def initialize_parameters(self, seed: int = 42) -> None: ...
    def fit(self, X: np.ndarray, y: np.ndarray, epochs: int = 50, **kwargs) -> TrainingHistory: ...
    def predict(self, X: np.ndarray) -> np.ndarray: ...
    def score(self, X: np.ndarray, y: np.ndarray) -> float: ...
    def cross_validate(self, X: np.ndarray, y: np.ndarray, k: int = 5) -> CVResult: ...
    def predict_with_uncertainty(self, X: np.ndarray, n_samples: int = 100) -> Tuple[np.ndarray, np.ndarray]: ...
    def save_checkpoint(self, path: str) -> None: ...
    def load_checkpoint(self, path: str) -> None: ...
```

#### `QNNConfig`
Configuration for quantum neural network.

```python
@dataclass
class QNNConfig:
    n_qubits: int
    n_layers: int = 2
    ansatz: AnsatzType = AnsatzType.HARDWARE_EFFICIENT
    encoding: EncodingStrategy = EncodingStrategy.ANGLE
    measurement: MeasurementBasis = MeasurementBasis.PAULI_Z
    entanglement: str = "linear"
    learning_rate: float = 0.01
    batch_size: int = 32
    shots: Optional[int] = None
    noise_model: Optional[NoiseModel] = None
    mitigation: Optional[str] = None
    regularization: Optional[str] = None
    regularization_strength: float = 0.01
```

### Data Classes

#### `TrainingHistory`
```python
@dataclass
class TrainingHistory:
    losses: List[float]
    accuracies: List[float]
    gradient_norms: List[float]
    gradient_variances: List[float]
    epoch_times: List[float]
    metadata: Dict[str, Any]
```

#### `QNNResult`
```python
@dataclass
class QNNResult:
    predictions: np.ndarray
    probabilities: Optional[np.ndarray]
    uncertainties: Optional[np.ndarray]
    metadata: Dict[str, Any]
```

## Data Models

### QNN Configuration Schema

```json
{
  "name": "qnn_classifier",
  "version": "1.0.0",
  "architecture": {
    "n_qubits": 4,
    "n_layers": 3,
    "ansatz": "strongly_entangling",
    "entanglement": "circular",
    "rotation_gates": ["RX", "RY", "RZ"],
    "entangling_gate": "CZ"
  },
  "training": {
    "optimizer": "adam",
    "learning_rate": 0.01,
    "epochs": 50,
    "batch_size": 32,
    "early_stopping": true,
    "patience": 10
  },
  "measurement": {
    "basis": "pauli_z",
    "shots": null,
    "mitigation": "zero_noise_extrapolation"
  }
}
```

### Training Metrics Schema

```json
{
  "training_id": "uuid-v4",
  "timestamp": "2024-01-15T10:30:00Z",
  "model": {
    "n_qubits": 4,
    "n_layers": 3,
    "n_parameters": 48
  },
  "metrics": {
    "final_loss": 0.1234,
    "final_accuracy": 0.956,
    "best_loss": 0.1234,
    "best_epoch": 45,
    "total_training_time_ms": 125000,
    "avg_epoch_time_ms": 2500
  },
  "hardware": {
    "backend": "aer_simulator",
    "shots": 1024,
    "noise_model": "depolarizing_0.005"
  }
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY quantum_neural_networks/ /app/quantum_neural_networks/
WORKDIR /app

ENV QNN_BACKEND=default.qubit
ENV QNN_SHOTS=1024
ENV QNN_OPTIMIZATION_LEVEL=2

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from quantum_neural_networks import health_check; health_check()"

CMD ["python", "-m", "quantum_neural_networks.server"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: quantum-nn
  namespace: quantum-ml
spec:
  replicas: 3
  selector:
    matchLabels:
      app: quantum-nn
  template:
    metadata:
      labels:
        app: quantum-nn
    spec:
      containers:
      - name: quantum-nn
        image: quantum-nn:latest
        resources:
          requests:
            memory: "4Gi"
            cpu: "2000m"
          limits:
            memory: "16Gi"
            cpu: "8000m"
        env:
        - name: QNN_BACKEND
          value: "lightning.qubit"
        ports:
        - containerPort: 8080
```

## Monitoring & Observability

### Metrics Collection

```python
from quantum_neural_networks import MetricsCollector

collector = MetricsCollector(backend="prometheus")

# Track training metrics
collector.register_metric("qnn_training_loss", type="gauge")
collector.register_metric("qnn_gradient_variance", type="gauge")
collector.register_metric("qnn_circuit_depth", type="gauge")
collector.register_metric("qnn_execution_time", type="histogram")

# Record during training
collector.set("qnn_training_loss", loss)
collector.set("qnn_gradient_variance", grad_var)
collector.observe("qnn_execution_time", execution_ms)
```

### Distributed Tracing

```python
from quantum_neural_networks import Tracer

tracer = Tracer(service="quantum-nn")

with tracer.start_span("training_epoch") as span:
    span.set_attribute("epoch", epoch)
    span.set_attribute("batch_size", batch_size)
    
    with tracer.start_span("circuit_execution"):
        result = qnn.forward_batch(X_batch)
        span.set_attribute("circuit_depth", qnn.circuit.depth())
    
    with tracer.start_span("gradient_computation"):
        gradients = qnn.compute_gradients(X_batch, y_batch)
        span.set_attribute("gradient_norm", np.linalg.norm(gradients))
```

### Logging Configuration

```python
import logging
from quantum_neural_networks import QuantumLogger

logger = QuantumLogger(
    name="quantum-nn",
    level=logging.INFO,
    format="json",
    output="stdout",
)

logger.info("Training started",
    n_qubits=4,
    n_layers=3,
    n_parameters=qnn.n_parameters,
)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from quantum_neural_networks import QuantumNeuralNetwork, QNNConfig

class TestQNN:
    def setup_method(self):
        self.config = QNNConfig(n_qubits=4, n_layers=2)
        self.qnn = QuantumNeuralNetwork(self.config)
    
    def test_initialization(self):
        self.qnn.initialize_parameters(seed=42)
        assert self.qnn.n_parameters > 0
    
    def test_forward_pass(self):
        self.qnn.initialize_parameters()
        X = np.random.randn(10, 4)
        output = self.qnn.forward(X)
        assert output.shape == (10, 1)
    
    def test_gradient_computation(self):
        self.qnn.initialize_parameters()
        X = np.random.randn(5, 4)
        y = np.random.randint(0, 2, (5, 1))
        grads = self.qnn.compute_gradients(X, y)
        assert grads.shape == (self.qnn.n_parameters,)
```

### Integration Tests

```python
class TestQNNIntegration:
    @pytest.mark.integration
    def test_training_convergence(self):
        config = QNNConfig(n_qubits=4, n_layers=2, learning_rate=0.05)
        qnn = QuantumNeuralNetwork(config)
        
        X, y = make_classification(n_samples=100, n_features=4)
        history = qnn.fit(X, y, epochs=30)
        
        assert history.losses[-1] < history.losses[0]
    
    @pytest.mark.integration
    def test_cross_validation(self):
        config = QNNConfig(n_qubits=4, n_layers=2)
        qnn = QuantumNeuralNetwork(config)
        
        X, y = make_classification(n_samples=100, n_features=4)
        cv_result = qnn.cross_validate(X, y, k=3)
        
        assert cv_result.mean_accuracy > 0.5
```

## Versioning & Migration

### Semantic Versioning

- **Major (X.0.0)**: Breaking API changes, new ansatz types, backend deprecation
- **Minor (0.X.0)**: New features, algorithm improvements, backend additions
- **Patch (0.0.X)**: Bug fixes, documentation updates, performance improvements

### Migration Guide (v1.x to v2.0)

```python
# v1.x (deprecated)
from quantum_neural_networks import QNN
model = QNN(n_qubits=4)
model.train(X, y)

# v2.0 (current)
from quantum_neural_networks import QuantumNeuralNetwork, QNNConfig
config = QNNConfig(n_qubits=4, n_layers=2)
model = QuantumNeuralNetwork(config)
model.fit(X, y, epochs=50)
```

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New `QNNConfig` API replaces separate config classes
- **Added**: Multi-backend support (PennyLane, Qiskit, Cirq)
- **Added**: Noise-aware training with mitigation strategies
- **Added**: Checkpoint and resume functionality
- **Improved**: 2x faster gradient computation
- **Fixed**: Memory leak in long training sessions

#### v1.1.0 (2023-09-01)
- **Added**: Data reuploading support
- **Added**: Custom ansatz architecture
- **Improved**: Gradient variance monitoring
- **Fixed**: Batch processing edge cases

## Glossary

| Term | Definition |
|------|------------|
| **Ansatz** | Parameterized quantum circuit architecture |
| **Barren Plateau** | Exponential vanishing of gradients in deep circuits |
| **Data Reuploading** | Re-encoding classical data in each variational layer |
| **Parameter-Shift Rule** | Exact gradient computation for parameterized circuits |
| **QNN** | Quantum Neural Network; hybrid quantum-classical model |
| **Variational Circuit** | Parameterized quantum circuit with trainable angles |
| **Expressivity** | Ability of a circuit to represent diverse quantum states |
| **Entanglement** | Quantum correlation between qubits |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/quantum-nn.git
cd quantum-nn
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
ruff check .
mypy quantum_neural_networks/
```

### Code Style

- Follow PEP 8 with line length 100
- Use type hints for all public functions
- Document public API with Google-style docstrings
- Keep functions under 50 lines

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation
5. Add changelog entry
6. Request review from maintainers
7. Squash and merge

## License

MIT License

Copyright (c) 2024 Quantum ML Contributors

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

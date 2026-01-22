# Quantum Computing Agent

## Overview

The **Quantum Computing Agent** provides comprehensive quantum computing capabilities including quantum circuit design, algorithm implementation, quantum key distribution, and quantum machine learning. This agent bridges classical and quantum computing paradigms.

## Core Capabilities

### 1. Quantum Circuit Design
Build and simulate quantum circuits with support for:
- **Single-Qubit Gates**: H, X, Y, Z, T, S gates
- **Multi-Qubit Gates**: CNOT, CZ, SWAP, Toffoli (CCX)
- **Parametric Gates**: RZ, RX, RY rotations
- **Measurement Operations**: Qubit to classical bit mapping
- **Circuit Visualization**: ASCII circuit diagrams

### 2. Quantum Algorithms
Implementation of fundamental quantum algorithms:

#### Deutsch-Jozsa Algorithm
Demonstrates quantum speedup for oracle problems
- Determines if function is constant or balanced
- Single-shot determination vs. classical exponential queries

#### Grover's Search Algorithm
Quadratic speedup for unstructured search
- Searches N items in O(√N) operations
- Oracle-based amplitude amplification

#### Quantum Teleportation
Quantum state transfer protocol
-Entanglement distribution
- Bell state measurement
- Classical communication requirement

### 3. Variational Quantum Eigensolver (VQE)
Hybrid quantum-classical algorithm for:
- Molecular ground state energy
- Optimization problems
- NISQ-era compatible

### 4. Quantum Key Distribution (BB84)
Quantum-safe cryptographic protocol:
- Photon polarization states
- Eavesdropping detection via error rate
- Key sifting and privacy amplification
- Security analysis

### 5. Quantum Machine Learning
Quantum-enhanced ML algorithms:
- **Quantum Kernel Classifiers**: Kernel methods on quantum states
- **Variational Quantum Classifiers**: Parameterized quantum circuits
- **Quantum Neural Networks**: Multi-layer quantum networks

## Usage Examples

### Create Quantum Circuit

```python
from quantum import QuantumCircuit, QuantumAlgorithm

circuit = QuantumCircuit(4)
circuit.h(0).cx(0, 1).h(2).cx(2, 3)
print(circuit.draw())
```

### Run Deutsch-Jozsa

```python
algo = QuantumAlgorithm()
circuit = algo.deutsch_jozsa(n=3)
print(f"Circuit depth: {circuit.depth()}")
```

### Quantum Key Distribution

```python
qkd = QuantumKeyDistribution()
key = qkd.bb84_protocol(key_length=256)
print(f"Generated key: {len(key['final_key'])} bits")
```

## Quantum Gates Reference

| Gate | Symbol | Matrix | Description |
|------|--------|--------|-------------|
| Hadamard | H | 1/√2 [[1,1],[1,-1]] | Creates superposition |
| Pauli-X | X | [[0,1],[1,0]] | Quantum NOT |
| Pauli-Y | Y | [[0,-i],[i,0]] | Rotation around Y |
| Pauli-Z | Z | [[1,0],[0,-1]] | Phase flip |
| CNOT | CX | 4×4 matrix | Controlled-NOT |
| T | T | [[1,0],[0,e^(iπ/4)]] | π/8 gate |

## Quantum States

### Basis States
- |0⟩ = [1, 0] (computational basis)
- |1⟩ = [0, 1] (computational basis)
- |+⟩ = 1/√2(|0⟩ + |1⟩) (superposition)
- |-⟩ = 1/√2(|0⟩ - |1⟩) (superposition)

### Entangled States
- Bell states: |Φ⁺⟩, |Φ⁻⟩, |Ψ⁺⟩, |Ψ⁻⟩
- GHZ states: |000⟩ + |111⟩
- W states: |001⟩ + |010⟩ + |100⟩

## Quantum Computing Platforms

### Cloud-Based Services
- **IBM Quantum**: Qiskit integration, 127+ qubits
- **Google Quantum AI**: Cirq, Sycamore processor
- **Amazon Braket**: Multiple hardware providers
- **Microsoft Azure Quantum**: Q# and various backends

### Simulators
- **Qiskit Aer**: High-performance simulation
- **Cirq**: Google's simulator
- **ProjectQ**: Swiss computing simulation

## Quantum Advantage Areas

### Current Applications
1. **Cryptography**: Post-quantum cryptography transition
2. **Chemistry**: Molecular simulation
3. **Optimization**: QAOA for combinatorial problems
4. **Machine Learning**: Quantum-enhanced ML

### Future Applications
- Drug discovery and materials science
- Financial modeling
- Climate prediction
- Artificial general intelligence

## Security Considerations

### Quantum Threats
- **Shor's Algorithm**: Breaks RSA/ECC
- **Grover's Algorithm**: Weakens symmetric crypto
- **Q-Day**: When quantum computers break current cryptography

### Post-Quantum Cryptography
- Lattice-based cryptography
- Hash-based signatures
- Code-based cryptography
- Multivariate cryptography

## Related Skills

- [Cryptography](../security/cryptography/README.md) - Classical and post-quantum crypto
- [Security Assessment](../security-assessment/penetration-testing/README.md) - Security evaluation
- [Machine Learning Operations](../ml-ops/model-deployment/README.md) - ML deployment

---

**File Path**: `skills/quantum-computing/quantum-algorithms/resources/quantum.py`

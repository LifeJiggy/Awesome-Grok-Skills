---
name: "quantum-cryptography"
category: "quantum"
version: "1.0.0"
tags: ["quantum", "cryptography", "QKD", "BB84", "post-quantum"]
---

# Quantum Cryptography Module

## Overview

The Quantum Cryptography module implements quantum key distribution (QKD) protocols, post-quantum cryptographic primitives, and quantum-secure communication channels. It covers the full lifecycle of quantum-secured key exchange — from qubit preparation and measurement through basis reconciliation, error estimation, privacy amplification, and authenticated classical post-processing. The module also includes post-quantum lattice-based encryption for hybrid classical-quantum workflows, providing defense-in-depth against both classical and quantum adversaries.

The module implements multiple QKD protocol families, including prepare-and-measure protocols (BB84, B92), entanglement-based protocols (E91, BBM92), and continuous-variable QKD for practical implementations using standard telecom components. Each protocol includes comprehensive security analysis tools, channel simulation capabilities, and parameter optimization for real-world deployment scenarios. The post-quantum cryptography component provides NIST-standardized algorithms (Kyber, Dilithium) alongside traditional QKD for hybrid security architectures.

All implementations follow the ETSI QKD interface standards and include comprehensive logging for security auditing. The module supports both simulated environments for research and development, and integration with actual quantum hardware through standardized APIs. Security proofs and finite-key analysis are built into every protocol, ensuring that key generation rates and security guarantees are mathematically rigorous even for finite block sizes encountered in practical implementations.

## Core Capabilities

- **BB84 Protocol**: Full implementation of the Bennett-Brassard 1984 QKD protocol with decoy states, including single-photon sources, weak coherent pulse sources, and measurement-device-independent (MDI) variants for enhanced security.
- **E91 Protocol**: Ekert 1991 entanglement-based QKD using Bell inequality verification, with CHSH parameter estimation and device-independent security proofs for hardware-agnostic security guarantees.
- **B92 Protocol**: Simplified two-state QKD using non-orthogonal states, optimized for low-cost implementations with minimal hardware requirements while maintaining provable security.
- **Decoy State QKD**: Decoy-state method to detect photon-number-splitting attacks, with optimized decoy intensity selection and statistical analysis for maximum secure key rate.
- **Sifting**: Classical basis reconciliation over authenticated channel, with bandwidth-efficient protocols for high-speed QKD systems and support for multiple sifting algorithms.
- **Error Estimation**: Quantum bit error rate (QBER) computation with statistical bounds, including finite-key analysis, confidence interval estimation, and adaptive error estimation for real-time parameter adjustment.
- **Privacy Amplification**: Universal hash-based key distillation from partially secure bits, with optimized implementations using Toeplitz matrices and polynomial hashing for high-throughput key generation.
- **Information Reconciliation**: Cascade protocol for error correction with adaptive parameter selection, LDPC code-based reconciliation for high efficiency, and verification procedures for error-free key extraction.
- **Post-Quantum Encryption**: Lattice-based (Kyber-style) key encapsulation, including key generation, encapsulation, and decapsulation with side-channel resistant implementations.
- **Channel Simulation**: Lossy and noisy quantum channel models with Eve intercept, supporting various eavesdropping strategies (intercept-resend, collective, coherent attacks) for security analysis and protocol optimization.

## Usage Examples

### Running BB84 Key Distribution

```python
from quantum_crypto import BB84Protocol, QuantumChannel, ClassicalChannel

# Create channels with realistic parameters
q_channel = QuantumChannel(
    loss=0.1,              # 10% channel loss
    noise=0.02,            # 2% depolarizing noise
    detector_efficiency=0.7,  # 70% detector efficiency
    dark_count_rate=1e-6   # Dark count probability
)
c_channel = ClassicalChannel(authenticated=True, latency_ms=10)

# Initialize protocol with security parameters
bb84 = BB84Protocol(
    key_length=256,
    security_parameter=128,  # 128-bit security
    max_block_size=1e6       # Block size for finite-key analysis
)

# Execute full protocol
session = bb84.run(
    quantum_channel=q_channel,
    classical_channel=c_channel,
    seed=42,
    num_pulses=100000,
    decoy_intensities=[0.1, 0.5, 1.0]  # Decoy state intensities
)

print(f"Secure key: {session.shared_key.hex()}")
print(f"QBER: {session.qber:.4f}")
print(f"Key rate: {session.key_rate:.4f} bits/pulse")
print(f"Privacy amplification factor: {session.amplification_factor:.4f}")
```

### Entanglement-Based E91 Protocol

```python
from quantum_crypto import E91Protocol, EntangledSource

source = EntangledSource(
    fidelity=0.95,
    generation_rate=1000,  # Pairs per second
    wavelength=810e-9      # Entangled photon wavelength
)

e91 = E91Protocol(
    key_length=256,
    bell_test=True,
    chsh_bound=2.828,  # Tsirelson bound
    security_parameter=128
)

session = e91.run(
    entangled_source=source,
    measurement_bases="random",  # Random basis selection
    num_rounds=10000,
    verification_rounds=100
)

print(f"Bell parameter S: {session.bell_s:.4f}")
print(f"Violation: {'Yes' if session.bell_s > 2.0 else 'No'}")
print(f"Secure key: {session.shared_key.hex()}")
print(f"Device-independent security: {session.di_security}")
```

### Privacy Amplification

```python
from quantum_crypto import PrivacyAmplifier, UniversalHash

amplifier = PrivacyAmplifier(
    security_parameter=128,
    hash_function=UniversalHash.POLYNOMIAL,
    seed_generation="cryptographic"
)

raw_key = bytes.fromhex("a1b2c3d4e5f6...")
extracted_key = amplifier.amplify(
    raw_key=raw_key,
    leaked_info_bits=20,
    input_length=len(raw_key) * 8,
    hash_seed=amplifier.generate_seed()
)

print(f"Raw key length: {len(raw_key) * 8} bits")
print(f"Amplified key: {extracted_key.hex()}")
print(f"Key reduction: {1 - len(extracted_key)/len(raw_key):.2%}")
```

### Post-Quantum Key Encapsulation

```python
from quantum_crypto import KyberKEM, SecurityLevel

kem = KyberKEM(
    security_level=SecurityLevel.LEVEL3,
    parameter_set="Kyber768",
    side_channel_resistant=True
)

# Key generation
keypair = kem.generate_keypair()
print(f"Public key size: {len(keypair.public_key)} bytes")

# Key encapsulation
encapsulation = kem.encapsulate(keypair.public_key)
print(f"Ciphertext size: {len(encapsulation.ciphertext)} bytes")
print(f"Shared secret: {encapsulation.shared_secret.hex()}")

# Key decapsulation
decapsulated = kem.decapsulate(
    keypair.private_key,
    encapsulation.ciphertext
)
assert decapsulated == encapsulation.shared_secret

# Hybrid QKD + Post-Quantum
from quantum_crypto import HybridKeyExchange
hybrid = HybridKeyExchange(qkd_key=session.shared_key, pqc_key=encapsulation.shared_secret)
final_key = hybrid.derive_key(length=256)
print(f"Hybrid key: {final_key.hex()}")
```

### Intercept-Resend Attack Simulation

```python
from quantum_crypto import BB84Protocol, EveIntercept

eve = EveIntercept(
    intercept_fraction=0.3,      # Eve intercepts 30% of qubits
    strategy="intercept_resend", # Attack strategy
    detection_probability=0.0    # Probability Eve is detected per intercept
)

bb84 = BB84Protocol(key_length=128)

# Run with eavesdropper
session = bb84.run_with_eve(eve=eve, seed=42, num_pulses=50000)

print(f"QBER with Eve: {session.qber:.4f}")
print(f"Detection threshold: 0.11")
print(f"Eve detected: {session.qber > 0.11}")
print(f"Information leaked to Eve: {session.leaked_information:.4f} bits")
print(f"Secure key after privacy amplification: {session.secure_key_length} bits")
```

### Continuous-Variable QKD Simulation

```python
from quantum_crypto import CVQKDProtocol, GaussianChannel

# Continuous-variable QKD using coherent states
channel = GaussianChannel(
    transmittance=0.5,      # 50% channel transmittance
    excess_noise=0.01,      # Excess noise in shot noise units
    electronic_noise=0.01   # Detector electronic noise
)

cvqkd = CVQKDProtocol(
    modulation_variance=4.0,  # Signal modulation variance
    reconciliation_method="multilevel",
    security_proof="composite"
)

session = cvqkd.run(
    channel=channel,
    num_symbols=1000000,
    symbol_rate=100e6  # 100 MHz symbol rate
)

print(f"Secret key rate: {session.key_rate:.2f} bits/symbol")
print(f"Channel transmittance: {session.transmittance:.4f}")
print(f"Excess noise: {session.excess_noise:.4f}")
```

## Best Practices

1. **Always authenticate the classical channel**: QKD without authentication is vulnerable to man-in-the-middle attacks. Use message authentication codes (MAC) with pre-shared keys or quantum-resistant signatures.
2. **Set QBER thresholds**: Abort key exchange if QBER exceeds ~11% (BB84) — this indicates an eavesdropper or excessive channel noise. Implement adaptive thresholds based on finite-key analysis.
3. **Use decoy states**: Always employ decoy-state method to defeat photon-number-splitting attacks on weak coherent pulse sources. Optimize decoy intensities for your channel loss and noise characteristics.
4. **Apply privacy amplification**: Never use raw sifted key directly — always amplify to remove partial information leakage. Use universal hash functions with cryptographically secure seeds.
5. **Validate Bell inequalities**: For E91, verify CHSH inequality violation before trusting entanglement-based security. Implement continuous monitoring of Bell parameters during key exchange.
6. **Hybrid approach**: Combine QKD with post-quantum KEM for defense-in-depth. Use key combination functions that are secure even if one component is compromised.
7. **Key rate optimization**: Tune pulse rate and loss budget to maximize secure key rate per second. Use finite-key analysis for realistic performance estimation in practical deployments.
8. **Regular key refresh**: Rotate QKD-derived keys frequently to bound the impact of any single compromise. Implement key lifecycle management with automatic expiration.
9. **Hardware calibration**: Regularly calibrate quantum detectors and sources to maintain specified performance. Include calibration verification in your key exchange protocol.
10. **Security auditing**: Log all key exchange events with timestamps, error rates, and security parameters. Implement intrusion detection based on statistical anomalies in QBER and key rates.

## Security Considerations

- **Finite-key effects**: Real implementations use finite block sizes, which reduce secure key rates compared to asymptotic analyses. Use the provided finite-key analysis tools for realistic security guarantees.
- **Detector vulnerabilities**: Implement measurement-device-independent (MDI) QKD to protect against detector side-channel attacks. Monitor detector performance for anomalies that may indicate tampering.
- **Side-channel resistance**: Consider timing side-channels in classical post-processing. Use constant-time implementations for all cryptographic operations.
- **Random number generation**: Use quantum random number generators for basis selection and key generation. Classical PRNGs may introduce vulnerabilities if not properly seeded.
- **Parameter estimation**: Use statistical tests to verify that measured QBER is consistent with expected channel parameters. Implement hypothesis testing for eavesdropper detection.
- **Key management**: Store quantum-generated keys securely with hardware security modules (HSMs). Implement key hierarchy with regular master key refresh.
- **Protocol security proofs**: All protocols include formal security proofs based on composable security frameworks. Verify that your implementation matches the assumptions in the security proof.
- **Post-quantum migration**: Plan for hybrid classical-quantum cryptography during the transition period. Use the provided migration assessment tools to evaluate your security posture.

## Related Modules

- `quantum-computing` — Low-level qubit and gate operations used by QKD protocol implementations, including circuit-based Bell state generation and measurement.
- `quantum-networking` — Entanglement distribution and quantum repeater infrastructure for long-distance QKD networks, including trusted node architectures.
- `quantum-simulation` — Channel noise simulation and security proof modeling for protocol analysis and optimization, including realistic hardware noise models.

## References

- Bennett, C. H., & Brassard, G. (1984). Quantum cryptography: Public key distribution and coin tossing. Proceedings of IEEE International Conference on Computers, Systems and Signal Processing, 175-179.
- Ekert, A. K. (1991). Quantum cryptography based on Bell's theorem. Physical Review Letters, 67(6), 661.
- Lo, H. K., Curty, M., & Qi, B. (2014). Measurement-device-independent quantum key distribution. Physical Review Letters, 112(13), 130503.
- Winick, A., et al. (2016). Secure key distribution for continuous-variable quantum key distribution. Physical Review X, 6(2), 021040.
- NIST Post-Quantum Cryptography Standardization. (2024). FIPS 203, 204, 205 Standards.
- ETSI QKD Standards. (2023). ETSI GS QKD 004, 008, 014.
- arXiv:2003.06557 - Advances in quantum key distribution.
- arXiv:2109.07425 - Practical challenges in quantum cryptography.
- arXiv:2201.10763 - Device-independent quantum key distribution.
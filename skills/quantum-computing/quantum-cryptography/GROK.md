---
name: "quantum-cryptography"
category: "quantum-computing"
version: "2.0.0"
tags: ["quantum-computing", "quantum-cryptography", "qkd", "post-quantum", "bb84", "e91", "lattice", "kyber"]
---

# Quantum Cryptography

## Overview

The quantum-cryptography module implements quantum key distribution (QKD) protocols, post-quantum cryptographic primitives, quantum random number generation, and quantum-secure authentication schemes. It provides production-grade implementations of BB84, E91, B92, SARG04, and decoy-state QKD protocols alongside NIST PQC candidates (Kyber, Dilithium, SPHINCS+, Falcon) for hybrid classical-quantum security.

This module is built for security engineers, cryptographers, and quantum communication researchers who need reproducible protocol simulations, channel noise modeling, eavesdropper detection, key sifting, privacy amplification, and error correction in a unified framework. It models realistic quantum channel imperfections including depolarizing noise, dark counts, misalignment, and detector dead time.

The module supports both asymptotic and finite-key security analyses, composable security proofs, and key rate optimization under realistic constraints. It integrates with network simulation tools for multi-node QKD network analysis and supports key relay, trusted node, and entanglement-based quantum network architectures.

## Core Capabilities

- **BB84 Protocol**: Full implementation of the BB84 QKD protocol with basis reconciliation, error estimation, privacy amplification, and eavesdropper detection via quantum bit error rate (QBER) thresholds. Supports single-photon and weak coherent pulse implementations.
- **E91 Protocol**: Ekert's entanglement-based QKD using Bell inequality violations (CHSH) for eavesdropper detection — demonstrates device-independent security without trusting the quantum devices.
- **B92 Protocol**: Minimal two-state QKD protocol using non-orthogonal states — the simplest BB84 variant with provable security against individual attacks.
- **SARG04 Protocol**: Improved BB84 variant robust against photon-number-splitting (PNS) attacks on weak coherent pulse sources. Provides better key rates than BB84 in the presence of multi-photon pulses.
- **Decoy-State QKD**: Multi-intensity decoy protocol that detects PNS attacks on practical QKD implementations using weak coherent states instead of single photons. Supports vacuum+weak, three-intensity, and optimal decoy strategies.
- **Quantum Random Number Generation (QRNG)**: Certified random bit generation from quantum measurements — includes min-entropy estimation, randomness extraction, and device-independent QRNG protocols.
- **Post-Quantum Cryptography**: NIST PQC-standardized algorithms: Kyber (KEM), Dilithium (signature), SPHINCS+ (hash-based signature), Falcon (signature). Includes hybrid classical+PQC modes for transition period deployment.
- **Quantum Secure Direct Communication (QSDC)**: Direct quantum transmission of messages without prior key exchange — DT-QSDC and RRDPS protocols with security analysis.
- **Quantum Digital Signatures (QDS)**: Information-theoretically secure digital signatures based on quantum states — Coppersmith-Winograd and Gottesman-Chuang schemes with practical key consumption analysis.
- **Channel Modeling**: Realistic quantum channel simulation with depolarizing noise, dephasing, amplitude damping, dark counts, detector efficiency, basis misalignment, and atmospheric turbulence for free-space links.
- **Key Rate Analysis**: Compute secret key rates under collective attacks, composable security proofs, and finite-key effects with confidence intervals.
- **Eavesdropper Detection**: Statistical QBER analysis with hypothesis testing to detect interception with configurable detection probability and false alarm rate. Includes Trojan horse attack detection.

## Usage Examples

### BB84 QKD Protocol

```python
from quantum_cryptography import (
    QKDEngine, ProtocolType, ChannelConfig,
    EavesdropperConfig, PrivacyAmplificationConfig
)

# Configure a realistic quantum channel
channel = ChannelConfig(
    distance_km=50.0,
    fiber_loss_db_per_km=0.2,
    detector_efficiency=0.9,
    dark_count_rate=1e-6,
    basis_misalignment_rad=0.02,
    depolarization_rate=0.01
)

# Configure potential eavesdropper
eve = EavesdropperConfig(
    active=True,
    intercept_strategy="intercept_resend",
    fraction_captured=0.15
)

engine = QKDEngine(
    protocol=ProtocolType.BB84,
    channel=channel,
    eavesdropper=eve,
    num_signals=100000
)

result = engine.run()
print(f"QBER: {result.qber:.4f}")              # ~0.075 if eve active
print(f"Raw key length: {result.raw_key_bits}")
print(f"Sifted key length: {result.sifted_key_bits}")
print(f"Final key length: {result.final_key_bits}")
print(f"Secret key rate: {result.key_rate_bits_per_signal:.4f}")
print(f"Eavesdropper detected: {result.eve_detected}")
print(f"Security proof: {result.security_level}")
```

### E91 Entanglement-Based QKD

```python
from quantum_cryptography import QKDEngine, ProtocolType, ChannelConfig

channel = ChannelConfig(distance_km=25.0, depolarization_rate=0.02)

engine = QKDEngine(
    protocol=ProtocolType.E91,
    channel=channel,
    num_signals=50000
)

result = engine.run()
print(f"Bell parameter S: {result.bell_s_parameter:.4f}")  # ~2.828 for ideal
print(f"CHSH violation: {result.chsh_violated}")
print(f"QBER: {result.qber:.4f}")
print(f"Final key bits: {result.final_key_bits}")
```

### Decoy-State QKD

```python
from quantum_cryptography import QKDEngine, ProtocolType, DecoyConfig

decoy = DecoyConfig(
    signal_intensity=0.8,
    decoy_intensities=[0.1, 0.5],
    num_decoy_shots=10000
)

engine = QKDEngine(
    protocol=ProtocolType.DECOY_BB84,
    decoy_config=decoy,
    num_signals=200000
)

result = engine.run()
print(f"PNS attack detected: {result.pns_detected}")
print(f"Yield estimate: {result.yield_estimate:.6f}")
print(f"Final key rate: {result.key_rate_bits_per_signal:.4f}")
```

### Quantum Random Number Generation

```python
from quantum_cryptography import QRNGEngine, MeasurementBasis

qrng = QRNGEngine(
    num_measurements=100000,
    basis=MeasurementBasis.DIAGONAL,
    min_entropy_threshold=0.95
)

result = qrng.generate()
print(f"Raw bits: {result.raw_bits}")
print(f"Min-entropy: {result.min_entropy:.4f}")
print(f"Extracted bits: {result.extracted_bits}")
print(f"Randomness certified: {result.randomness_certified}")
```

### Post-Quantum Key Encapsulation (Kyber)

```python
from quantum_cryptography import PQCKeyEncapsulation, PQCAlgorithm

kem = PQCKeyEncapsulation(algorithm=PQCAlgorithm.KYBER_768)

# Key generation
keypair = kem.generate_keypair()
print(f"Public key size: {len(keypair.public_key)} bytes")
print(f"Secret key size: {len(keypair.secret_key)} bytes")

# Encapsulation
ciphertext, shared_secret_sender = kem.encapsulate(keypair.public_key)
print(f"Ciphertext size: {len(ciphertext)} bytes")

# Decapsulation
shared_secret_receiver = kem.decapsulate(ciphertext, keypair.secret_key)
print(f"Shared secrets match: {shared_secret_sender == shared_secret_receiver}")
```

### Post-Quantum Digital Signature (Dilithium)

```python
from quantum_cryptography import PQCDigitalSignature, PQCAlgorithm

sig = PQCDigitalSignature(algorithm=PQCAlgorithm.DILITHIUM_3)

keypair = sig.generate_keypair()
message = b"Authenticate this quantum-secure message"

signature = sig.sign(message, keypair.secret_key)
valid = sig.verify(message, signature, keypair.public_key)
print(f"Signature valid: {valid}")
print(f"Signature size: {len(signature)} bytes")
```

## Architecture

```
quantum_cryptography/
  __init__.py
  qkd/
    bb84.py                 # BB84 protocol implementation
    e91.py                  # E91 entanglement-based protocol
    b92.py                  # B92 two-state protocol
    sarg04.py               # SARG04 PNS-resistant protocol
    decoy_state.py          # Decoy-state BB84 variant
    qsdc.py                 # Quantum secure direct communication
    qds.py                  # Quantum digital signatures
  pqc/
    kyber.py                # Kyber KEM (Kyber-512/768/1024)
    dilithium.py            # Dilithium signatures (Dilithium2/3/5)
    sphincs.py              # SPHINCS+ hash-based signatures
    falcon.py               # Falcon signatures
    hybrid.py               # Classical+PQC hybrid modes
  qrng/
    qrng_engine.py          # Quantum random number generation
    min_entropy.py          # Min-entropy estimation
    extractor.py            # randomness extraction (TOEPLITZ)
    device_independent.py   # Device-independent QRNG
  channel/
    noise_models.py         # Depolarizing, dephasing, amplitude damping
    detector_models.py      # Dark counts, efficiency, dead time
    atmospheric.py          # Free-space channel turbulence
    fiber_models.py         # Fiber loss and dispersion
  security/
    qber_analysis.py        # QBER monitoring and threshold testing
    key_rate.py             # Secret key rate computation
    finite_key.py           # Finite-key security analysis
    composable.py           # Composable security proofs
  utils/
    error_correction.py     # CASCADE, LDPC for QKD
    privacy_amplification.py # Toeplitz hashing
    basis_reconciliation.py # Basis sifting
    key_management.py       # Key storage and lifecycle
```

## Best Practices

1. **QBER monitoring**: Continuously monitor QBER during key exchange. A QBER above 11% for BB84 indicates eavesdropping or excessive channel noise. Set thresholds based on your security model and channel characterization.

2. **Finite-key analysis**: Always perform finite-key security analysis — asymptotic proofs are insufficient for real deployments. Use at least 10^6 signals for meaningful key rates. Finite-key effects reduce key rates by 10-30% compared to asymptotic estimates.

3. **Decoy states in practice**: Use at least 3 intensity levels (signal + 2 decoys) for reliable PNS attack detection. The vacuum + weak decoy strategy is minimum viable. Optimal decoy intensities depend on channel loss and detector characteristics.

4. **Privacy amplification**: Apply privacy amplification with Toeplitz matrix hashing. Use min-entropy (not Shannon entropy) for the security parameter — min-entropy provides composable security and is more conservative.

5. **Error correction**: Use CASCADE or LDPC codes for error correction. CASCADE is simpler but leaks more information; LDPC is more efficient but requires careful parameter tuning. Target reconciliation efficiency of 1.16x the Shannon limit.

6. **Key management**: Never reuse quantum-generated keys. Implement key retirement policies and maintain key usage counters. Store keys in tamper-resistant hardware with proper access controls. Define key lifecycle: generation, storage, usage, retirement, destruction.

7. **PQC hybrid mode**: Deploy PQC algorithms in hybrid mode (classical + PQC) during the transition period. Use Kyber-768 with X25519 for KEM hybrid, Dilithium3 with Ed25519 for signature hybrid. This provides security against both classical and quantum attacks.

8. **Channel calibration**: Calibrate channel parameters (loss, noise, misalignment) before each session. Use reference signals to estimate real-time channel conditions. Account for polarization drift in fiber-based systems and atmospheric turbulence in free-space links.

9. **Detector characterization**: Characterize detector dark counts, afterpulsing, and timing jitter regularly. These parameters directly impact achievable key rates and security bounds. Use detector tomography for accurate characterization.

10. **Side-channel resistance**: PQC implementations must resist timing attacks, power analysis, and cache attacks. Use constant-time implementations and masking countermeasures. Regularly audit implementations against side-channel vulnerabilities.

## Performance Considerations

- **Key rate vs distance**: QKD key rates decrease exponentially with distance due to fiber loss (~0.2 dB/km). At 50 km, key rates are ~1 kbit/s; at 100 km, ~1 bit/s. Use quantum repeaters or trusted nodes for longer distances.
- **Decoy-state overhead**: Decoy-state protocols require multiple intensity settings, reducing the fraction of signals used for key generation. Optimize decoy fractions to maximize key rate while maintaining security.
- **PQC performance**: Kyber-768 key generation takes ~0.1 ms, encapsulation ~0.2 ms, decapsulation ~0.3 ms on modern hardware. Dilithium3 signing takes ~0.5 ms, verification ~0.1 ms. These are fast enough for most applications.
- **Finite-key penalty**: For short key exchanges (< 10^6 signals), finite-key effects reduce key rates by 10-50%. Plan for longer exchange durations or accept lower key rates for small deployments.
- **Error correction overhead**: CASCADE requires multiple rounds of communication, adding latency. LDPC codes can be implemented with a single round-trip but require more computation. Choose based on latency constraints.
- **QRNG throughput**: Physical QRNG devices can generate random bits at 1-100 Gbit/s. Post-processing (min-entropy estimation, extraction) reduces throughput by 10-50%. Use hardware-accelerated Toeplitz hashing for high throughput.

## Security Considerations

- **Photon-number-splitting (PNS) attacks**: Weak coherent pulse implementations are vulnerable to PNS attacks without decoy states. Always use decoy states in production QKD systems.
- **Trojan horse attacks**: Adversaries can probe quantum devices with bright light to extract information. Implement optical isolators and monitoring detectors to detect Trojan horse probing.
- **Detector blinding**: Adversaries can blind single-photon detectors with bright light, then control detection outcomes. Use measurement-device-independent (MDI) QKD or detector monitoring to mitigate.
- **Side-channel leakage**: QKD implementations may leak information through timing, power consumption, or electromagnetic emissions. Use constant-time implementations and regular side-channel testing.
- **PQC standardization timeline**: NIST finalized Kyber, Dilithium, SPHINCS+, and Falcon standards in 2024. Begin migration planning now; large systems may take 2-5 years to fully transition.
- **Harvest-now-decrypt-later**: Adversaries may collect encrypted data today to decrypt with future quantum computers. Use hybrid encryption (classical + PQC) for long-lived secrets.
- **Quantum network security**: Multi-node QKD networks require trusted nodes for key relay. Each trusted node is a potential vulnerability. Use entanglement-based protocols and quantum repeaters for end-to-end security.

## Related Modules

- **quantum-algorithms** — Foundational quantum algorithms that underpin QKD security proofs (quantum Fourier transform for period finding, amplitude amplification for Grover-based attacks on classical crypto).
- **quantum-error-correction** — Error correction codes that protect quantum states in QKD channels; surface codes and stabilizer codes for fault-tolerant quantum communication and entanglement distillation.
- **quantum-simulation** — Simulate quantum channels, noise models, and eavesdropper strategies for protocol security analysis. Includes channel tomography and noise characterization tools.
- **quantum-optimization** — Optimize QKD network routing, key relay paths, and resource allocation in quantum networks. Includes key scheduling and bandwidth optimization.

## References

- Bennett, C. H. & Brassard, G. (1984). Quantum cryptography: Public key distribution and coin tossing. *Proceedings of IEEE International Conference on Computers, Systems and Signal Processing*, 175-179.
- Ekert, A. K. (1991). Quantum cryptography based on Bell's theorem. *Physical Review Letters*, 67(6), 661.
- Shor, P. W. & Preskill, J. (2000). Simple proof of security of the BB84 quantum key distribution protocol. *Physical Review Letters*, 85(2), 441.
- Scarani, V. et al. (2009). The security of practical quantum key distribution. *Reviews of Modern Physics*, 81(3), 1301.
- NIST (2024). *Post-Quantum Cryptography Standardization*. FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205 (SLH-DSA).
- Lo, H. K., Curty, M., & Qi, B. (2012). Measurement-device-independent quantum key distribution. *Physical Review Letters*, 108(13), 130503.
- Xu, F. et al. (2020). Secure quantum key distribution with realistic devices. *Reviews of Modern Physics*, 92(2), 025002.

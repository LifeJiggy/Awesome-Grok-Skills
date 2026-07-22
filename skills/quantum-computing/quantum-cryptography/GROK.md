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

## Advanced Configuration

### Channel Model Configuration

```python
from quantum_cryptography import ChannelConfig, NoiseModel, FiberModel

# Advanced channel configuration
channel = ChannelConfig(
    distance_km=100.0,
    fiber_loss_db_per_km=0.2,
    detector_efficiency=0.9,
    dark_count_rate=1e-6,
    basis_misalignment_rad=0.02,
    depolarization_rate=0.01,
    noise_model=NoiseModel(
        depolarizing=0.01,
        dephasing=0.005,
        amplitude_damping=0.002,
    ),
    fiber_model=FiberModel(
        type="standard_single_mode",
        attenuation_coefficient=0.2,
        dispersion_coefficient=17.0,
        polarization_mode_dispersion=0.1,
    ),
    detector_config={
        "type": "spm",
        "efficiency": 0.9,
        "dark_count_rate": 1e-6,
        "dead_time_ns": 50,
        "afterpulsing_probability": 0.01,
        "timing_jitter_ps": 100,
    },
)
```

### Privacy Amplification Configuration

```python
from quantum_cryptography import PrivacyAmplificationConfig, HashFunction

pa_config = PrivacyAmplificationConfig(
    hash_function=HashFunction.TOEPITZ,
    security_parameter=1e-10,
    input_length=100000,
    extract_ratio=0.1,
    seed_length=1000,
    parallel=True,
    batch_size=10000,
)

engine = QKDEngine(
    protocol=ProtocolType.BB84,
    channel=channel,
    privacy_amplification_config=pa_config,
)
```

### Error Correction Configuration

```python
from quantum_cryptography import ErrorCorrectionConfig, CodeType

ec_config = ErrorCorrectionConfig(
    code_type=CodeType.LDPC,
    code_rate=0.5,
    max_rounds=10,
    leaking_bits=True,
    leakage_estimation=True,
    target_efficiency=1.16,
)

engine = QKDEngine(
    protocol=ProtocolType.BB84,
    channel=channel,
    error_correction_config=ec_config,
)
```

### PQC Hybrid Configuration

```python
from quantum_cryptography import PQCHybridConfig, PQCAlgorithm

hybrid_config = PQCHybridConfig(
    kem_algorithm=PQCAlgorithm.KYBER_768,
    signature_algorithm=PQCAlgorithm.DILITHIUM_3,
    classical_algorithm="x25519",
    classical_signature="ed25519",
    hybrid_mode="concatenated",
    security_level="NIST Level 3",
)

# Generate hybrid keypair
keypair = hybrid_config.generate_keypair()
print(f"Hybrid public key size: {len(keypair.public_key)} bytes")
print(f"Hybrid secret key size: {len(keypair.secret_key)} bytes")
```

## Architecture Patterns

### QKD Network Architecture

```python
from quantum_cryptography import QKDNetwork, NodeConfig, LinkConfig

# Multi-node QKD network
network = QKDNetwork(
    nodes=[
        NodeConfig(id="alice", type="sender", location="office_a"),
        NodeConfig(id="bob", type="receiver", location="office_b"),
        NodeConfig(id="relay", type="trusted_node", location="data_center"),
    ],
    links=[
        LinkConfig(source="alice", target="relay", distance_km=50.0, protocol="bb84"),
        LinkConfig(source="relay", target="bob", distance_km=30.0, protocol="bb84"),
    ],
    key_management={
        "key_storage": "redis",
        "key_lifetime_hours": 24,
        "max_key_usage": 1000,
    },
)

# Establish end-to-end key
key = network.establish_key(source="alice", target="bob")
print(f"Key length: {len(key)} bits")
print(f"Key rate: {key.rate_bits_per_second:.1f} bps")
```

### PQC Migration Architecture

```python
from quantum_cryptography import PQCMigrator, MigrationStrategy

migrator = PQCMigrator(
    strategy=MigrationStrategy.HYBRID,
    target_algorithm=PQCAlgorithm.KYBER_768,
    classical_algorithm="rsa-2048",
    transition_period_months=24,
)

# Migrate existing key exchange
migrated_system = migrator.migrate(
    current_system=rsa_system,
    test_vectors=test_vectors,
)

print(f"Migration complete: {migrated_system.status}")
print(f"Hybrid mode: {migrated_system.hybrid_mode}")
print(f"Security level: {migrated_system.security_level}")
```

### QRNG Integration Pattern

```python
from quantum_cryptography import QRNGIntegrator, QRNGSource

integrator = QRNGIntegrator(
    source=QRNGSource.HARDWARE,
    device_path="/dev/qrng0",
    post_processing=True,
    min_entropy_threshold=0.95,
    extraction_method="toeplitz",
)

# Generate random bytes
random_bytes = integrator.generate_bytes(n_bytes=1024)
print(f"Generated {len(random_bytes)} random bytes")
print(f"Min-entropy: {integrator.min_entropy:.4f}")
print(f"Randomness certified: {integrator.certified}")
```

## Integration Guide

### TLS Integration

```python
from quantum_cryptography import QKDtlsIntegration, TLSConfig

tls_config = TLSConfig(
    protocol="TLS 1.3",
    cipher_suite="KYBER_768_X25519_AES_256_GCM_SHA384",
    certificate_authority="quantum_ca",
    key_rotation_hours=24,
)

tls = QKDtlsIntegration(config=tls_config)

# Wrap socket with QKD-secured TLS
secure_socket = tls.wrap_socket(raw_socket)

# Exchange data
secure_socket.send(encrypted_data)
received_data = secure_socket.recv()
```

### SSH Integration

```python
from quantum_cryptography import QKDSSHIntegration

ssh = QKDSSHIntegration(
    key_exchange="kyber_768",
    host_key="dilithium_3",
    encryption="aes_256_gcm",
    mac="hmac_sha384",
)

# Establish QKD-secured SSH connection
connection = ssh.connect(
    hostname="quantum-server.example.com",
    port=22,
    username="alice",
)

# Execute command
result = connection.execute("ls -la")
print(f"Output: {result.stdout}")
```

### VPN Integration

```python
from quantum_cryptography import QKDVPN, VPNConfig

vpn_config = VPNConfig(
    tunnel_type="ipsec",
    key_exchange="kyber_768",
    encryption="aes_256_gcm",
    key_rotation_minutes=60,
)

vpn = QKDVPN(config=vpn_config)

# Create QKD-secured VPN tunnel
tunnel = vpn.create_tunnel(
    local_endpoint="office_a.gateway.com",
    remote_endpoint="office_b.gateway.com",
)

# Route traffic through tunnel
tunnel.route traffic("10.0.0.0/8")
```

## Performance Optimization

### Key Rate Optimization

```python
from quantum_cryptography import KeyRateOptimizer

optimizer = KeyRateOptimizer(
    target_distance_km=50.0,
    protocol=ProtocolType.BB84,
    optimization_level=3,
)

# Optimize key rate parameters
optimal_params = optimizer.optimize(
    signal_intensity_range=(0.1, 1.0),
    decoy_intensities_range=(0.01, 0.5),
    batch_size_range=(1000, 100000),
)

print(f"Optimal signal intensity: {optimal_params.signal_intensity:.3f}")
print(f"Optimal decoy intensities: {optimal_params.decoy_intensities}")
print(f"Expected key rate: {optimal_params.key_rate_bps:.1f} bps")
```

### Batch Processing Optimization

```python
from quantum_cryptography import BatchProcessor

processor = BatchProcessor(
    batch_size=10000,
    n_workers=4,
    parallel=True,
    memory_limit_mb=1024,
)

# Process multiple QKD sessions in parallel
results = processor.process_batch(
    sessions=qkd_sessions,
    protocol=ProtocolType.BB84,
    channel=channel,
)

print(f"Processed {len(results)} sessions")
print(f"Total key bits: {sum(r.final_key_bits for r in results)}")
print(f"Average key rate: {np.mean([r.key_rate_bps for r in results]):.1f} bps")
```

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. High QBER

**Symptom**: QBER > 11%, key generation fails

**Solution**:
```python
# Check channel alignment
channel.basis_misalignment_rad = 0.01  # Reduce misalignment

# Increase signal intensity
decoy.signal_intensity = 0.9

# Use decoy states
engine = QKDEngine(
    protocol=ProtocolType.DECOY_BB84,
    decoy_config=decoy,
)
```

#### 2. Low Key Rate

**Symptom**: Key rate too low for practical use

**Solution**:
```python
# Optimize key rate parameters
optimizer = KeyRateOptimizer(target_distance_km=50.0)
optimal_params = optimizer.optimize()

# Use better error correction
ec_config.code_type = CodeType.LDPC
ec_config.code_rate = 0.7

# Increase batch size
engine.num_signals = 200000
```

#### 3. PQC Performance Issues

**Symptom**: PQC operations too slow

**Solution**:
```python
# Use faster algorithm
kem = PQCKeyEncapsulation(algorithm=PQCAlgorithm.KYBER_512)

# Enable hardware acceleration
config.hardware_acceleration = True

# Cache keypairs
config.cache_size = 1000
```

## API Reference

### Core Classes

#### `QKDEngine`
```python
class QKDEngine:
    def __init__(self, protocol: ProtocolType, channel: ChannelConfig, **kwargs) -> None: ...
    def run(self) -> QKDResult: ...
    def get_key(self) -> QuantumKey: ...
    def get_qber(self) -> float: ...
```

#### `PQCKeyEncapsulation`
```python
class PQCKeyEncapsulation:
    def __init__(self, algorithm: PQCAlgorithm) -> None: ...
    def generate_keypair(self) -> KeyPair: ...
    def encapsulate(self, public_key: bytes) -> Tuple[bytes, bytes]: ...
    def decapsulate(self, ciphertext: bytes, secret_key: bytes) -> bytes: ...
```

## Data Models

### QKD Result Schema

```json
{
  "protocol": "bb84",
  "status": "success",
  "qber": 0.05,
  "raw_key_bits": 100000,
  "sifted_key_bits": 50000,
  "final_key_bits": 5000,
  "key_rate_bps": 125.0,
  "eve_detected": false,
  "security_level": "composable",
  "channel": {
    "distance_km": 50.0,
    "fiber_loss_db_per_km": 0.2
  }
}
```

## Deployment Guide

### Docker Deployment

```dockerfile
FROM python:3.11-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY quantum_cryptography/ /app/quantum_cryptography/
WORKDIR /app

ENV QKD_PROTOCOL=bb84
ENV QKD_CHANNEL_DISTANCE=50.0
ENV PQC_ALGORITHM=kyber_768

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from quantum_cryptography import health_check; health_check()"

CMD ["python", "-m", "quantum_cryptography.server"]
```

## Monitoring & Observability

### Metrics Collection

```python
from quantum_cryptography import MetricsCollector

collector = MetricsCollector(backend="prometheus")

collector.register_metric("qkd_qber", type="gauge")
collector.register_metric("qkd_key_rate", type="gauge")
collector.register_metric("qkd_key_length", type="gauge")
collector.register_metric("pqc_keygen_time", type="histogram")

collector.set("qkd_qber", result.qber)
collector.set("qkd_key_rate", result.key_rate_bps)
collector.set("qkd_key_length", result.final_key_bits)
collector.observe("pqc_keygen_time", keygen_time_ms)
```

## Testing Strategy

### Unit Tests

```python
import pytest
from quantum_cryptography import QKDEngine, ProtocolType, ChannelConfig

class TestBB84:
    def setup_method(self):
        self.channel = ChannelConfig(distance_km=10.0)
    
    def test_bb84_no_eve(self):
        engine = QKDEngine(protocol=ProtocolType.BB84, channel=self.channel)
        result = engine.run()
        assert result.qber < 0.11
        assert result.eve_detected == False
    
    def test_bb84_with_eve(self):
        engine = QKDEngine(
            protocol=ProtocolType.BB84,
            channel=self.channel,
            eavesdropper=EavesdropperConfig(active=True),
        )
        result = engine.run()
        assert result.qber > 0.11
        assert result.eve_detected == True
```

## Versioning & Migration

### Changelog

#### v2.0.0 (2024-01-15)
- **Breaking**: New config API for all protocols
- **Added**: PQC hybrid mode support
- **Added**: QKD network simulation
- **Improved**: 2x faster key generation
- **Fixed**: Finite-key security analysis

## Glossary

| Term | Definition |
|------|------------|
| **BB84** | First QKD protocol using 4 quantum states |
| **QBER** | Quantum Bit Error Rate |
| **PQC** | Post-Quantum Cryptography |
| **QRNG** | Quantum Random Number Generator |
| **Privacy Amplification** | Extract secure key from partially secure raw key |
| **Decoy State** | Multi-intensity protocol to detect PNS attacks |

## Contributing Guidelines

### Development Setup

```bash
git clone https://github.com/example/quantum-crypto.git
cd quantum-crypto
python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

## License

MIT License

Copyright (c) 2024 Quantum Cryptography Contributors

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

### Key Management Lifecycle

```python
from quantum_cryptography import KeyManager, KeyLifecycle

key_manager = KeyManager(
    storage="hsm",
    rotation_interval_hours=24,
    max_key_usage=10000,
    backup_enabled=True,
)

# Generate key
key = key_manager.generate_key(
    algorithm="aes-256-gcm",
    purpose="encryption",
    metadata={"user_id": "123", "application": "email"},
)

# Use key
encrypted = key_manager.encrypt(key.id, plaintext)

# Rotate key
new_key = key_manager.rotate(key.id)

# Destroy key
key_manager.destroy(key.id)
```

### Certificate Management

```python
from quantum_cryptography import CertificateManager, CertConfig

cert_config = CertConfig(
    ca_cert="/path/to/ca.pem",
    ca_key="/path/to/ca-key.pem",
    validity_days=365,
    key_size=4096,
    hash_algorithm="sha256",
)

cert_manager = CertificateManager(config=cert_config)

# Generate certificate
cert = cert_manager.generate_cert(
    common_name="api.example.com",
    san=["api.example.com", "www.example.com"],
    organization="My Company",
    validity_days=90,
)

# Verify certificate
is_valid = cert_manager.verify_cert(cert.path)
print(f"Certificate valid: {is_valid}")

# Revoke certificate
cert_manager.revoke_cert(cert.serial)
```

### Key Exchange Protocols

```python
from quantum_cryptography import KeyExchange, Protocol

# Diffie-Hellman key exchange
dh = KeyExchange(protocol=Protocol.DIFFIE_HELLMAN)
shared_secret = dh.exchange(private_key_a, public_key_b)

# ECDH key exchange
ecdh = KeyExchange(protocol=Protocol.ECDH)
shared_secret = ecdh.exchange(private_key_a, public_key_b)

# Quantum key distribution
qkd = KeyExchange(protocol=Protocol.QKD)
shared_secret = qkd.exchange(alice_endpoint, bob_endpoint)
```

### Digital Signature Verification

```python
from quantum_cryptography import SignatureVerifier, SignatureConfig

verifier = SignatureVerifier(
    config=SignatureConfig(
        algorithm="rsa-pss",
        hash_algorithm="sha256",
        salt_length=32,
    ),
)

# Sign message
signature = verifier.sign(private_key, message)

# Verify signature
is_valid = verifier.verify(public_key, message, signature)
print(f"Signature valid: {is_valid}")

# Verify certificate chain
chain_valid = verifier.verify_chain(cert, intermediate_cert, root_cert)
print(f"Chain valid: {chain_valid}")
```

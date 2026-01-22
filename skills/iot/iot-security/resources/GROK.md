# IoT Security

Specialized skill for securing IoT devices, networks, and data flows. Covers device authentication, certificate management, threat detection, encryption, and secure communication protocols for IoT ecosystems.

## Core Capabilities

### Device Authentication & Identity
- X.509 certificate management for IoT devices
- Device identity provisioning and lifecycle management
- Pre-shared key (PSK) authentication
- Token-based authentication with JWT
- Hardware security module (HSM) integration
- Device attestation and fingerprinting

### Network Security
- IoT-specific firewall rules and filtering
- Rate limiting and DoS protection
- Network segmentation and VLANs
- VPN tunneling for remote devices
- Zero-trust network architecture
- Protocol-specific security (MQTT TLS, CoAP DTLS)

### Threat Detection & Response
- Anomaly detection in device behavior
- Brute force and intrusion detection
- Traffic pattern analysis
- Automated threat response
- Security event logging and SIEM integration
- Threat intelligence feeds

### Data Protection
- End-to-end encryption for sensor data
- Secure key storage and rotation
- Data integrity verification
- Privacy-preserving data aggregation
- Secure over-the-air (OTA) updates

### Compliance & Governance
- IoT security frameworks (NIST, CIS)
- GDPR and data privacy compliance
- Security auditing and reporting
- Device vulnerability assessment
- Security policy enforcement

## Usage Examples

### Device Registration and Authentication
```python
from iot_security import (
    IoTSecurityManager, DeviceIdentity, DeviceAuthMethod, SecurityLevel
)

security = IoTSecurityManager("org-001")

device = DeviceIdentity(
    device_id="sensor-001",
    auth_method=DeviceAuthMethod.CERTIFICATE,
    credentials={},
    security_level=SecurityLevel.HIGH
)
security.register_device(device)

cert_result = security.generate_certificate("sensor-001", validity_days=365)
auth_result = security.authenticate_device("sensor-001", {
    "certificate_id": cert_result["cert_id"]
})
```

### Security Monitoring
```python
threat_analysis = security.analyze_threat({
    "connection_attempts": 15,
    "failed_auths": 3,
    "unusual_traffic_pattern": True,
    "port_scan": False
})

dashboard = security.get_security_dashboard()
```

### Encryption
```python
encrypted = security.encrypt_payload("sensor-001", {
    "temperature": 25.5,
    "location": "warehouse-a"
})

decrypted = security.decrypt_payload("sensor-001", encrypted["encrypted_data"])
```

### Firewall Configuration
```python
from iot_security import IoTFirewall

firewall = IoTFirewall()
firewall.add_rule({
    "id": "rule-001",
    "action": "allow",
    "protocol": "tcp",
    "destination_port": 8883,
    "source_ip": "10.0.0.0/16"
})

result = firewall.check_packet({
    "source_ip": "10.0.1.50",
    "destination_port": 8883,
    "protocol": "tcp"
})

allowed = firewall.check_rate_limit("192.168.1.100", limit=100)
```

## Best Practices

1. **Certificate Lifecycle**: Implement automated certificate rotation before expiry
2. **Zero Trust**: Never trust device identity based solely on network location
3. **Minimal Attack Surface**: Disable unused ports and services on devices
4. **Firmware Signing**: Require cryptographic signatures for all firmware updates
5. **Network Segmentation**: Isolate IoT devices in dedicated network segments
6. **Monitoring**: Implement continuous security monitoring with alerting
7. **Device Hardening**: Remove default credentials and unnecessary services
8. **Incident Response**: Have documented procedures for compromised devices

## Related Skills

- [Sensor Networks](sensor-networks): Secure sensor deployment
- [Industrial IoT](industrial-iot): Industrial security implementations
- [Zero Trust](zero-trust/security-framework): Zero-trust architecture
- [Cryptography](security/cryptography): Encryption fundamentals
- [Network Engineering](networking/network-engineering): Network security

## Use Cases

- Smart building security architecture
- Industrial control system protection
- Healthcare IoT compliance
- Connected vehicle security
- Smart grid protection
- Retail IoT security
- Agricultural sensor networks
- Environmental monitoring security

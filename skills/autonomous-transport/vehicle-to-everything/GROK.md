---
name: "vehicle-to-everything"
category: "autonomous-transport"
version: "2.0.0"
tags: ["autonomous-transport", "vehicle-to-everything", "V2X", "DSRC", "C-V2X", "V2V", "V2I", "V2P", "BSM", "SPaT"]
---

# Vehicle-to-Everything (V2X) Communication

## Overview

This module provides a complete V2X communication stack for autonomous and connected vehicles, covering V2V (vehicle-to-vehicle), V2I (vehicle-to-infrastructure), V2P (vehicle-to-pedestrian), and V2N (vehicle-to-network) communication modes. It implements both the IEEE 802.11p/DSRC (Dedicated Short-Range Communications) and 3GPP C-V2X (Cellular V2X) radio access technologies, with full protocol stacks for SAE J2735 Basic Safety Messages (BSM), NTCIP 1202 SPaT/MAP, and ETSI ITS-G5 cooperative awareness.

The stack abstracts the underlying radio technology behind a unified V2X adapter API, enabling application developers to send and receive V2X messages without concern for the physical layer. It includes message encoding/decoding, cooperative perception fusion, misbehavior detection, PKI certificate management, and a standards-compliant geo-fencing engine.

## Core Capabilities

- BSM (SAE J2735) encoding and decoding with full optional data elements
- SPaT (Signal Phase and Timing) and MAP (intersection geometry) message processing
- V2V cooperative awareness and cooperative perception message exchange
- V2I RSU (Roadside Unit) communication for signal priority and traveler information
- V2P vulnerable road user (VRU) alerting via SAE J2945/9
- DSRC (IEEE 802.11p) and C-V2X (3GPP PC5 sidelink) dual-stack operation
- PKI certificate enrollment, revocation, and misbehavior detection (SCMS)
- Geo-fencing engine for zone-based message filtering and policy enforcement
- Store-and-forward for non-line-of-sight (NLOS) multi-hop message relay
- Message authentication latency budget enforcement (< 5 ms)
- Configurable transmission power, data rate, and channel selection
- Interoperability testing framework against SAE / ETSI conformance test suites

## Advanced Configuration

### Radio Stack Configuration

```yaml
v2x:
  radio:
    mode: "dual"                    # dsrc | cv2x | dual
    dsrc:
      interface: "wlan0"
      channel: 178                  # CCH (Control Channel)
      switch_list:
        - channel: 178              # CCH interval
          duration_ms: 50
        - channel: 172              # SCH1 (Service Channel)
          duration_ms: 50
      tx_power_dbm: 20
      data_rate_mbps: 6             # 6 Mbps mandatory minimum
      modulation: "OFDM"
    cv2x:
      interface: "c-v2x0"
      mode: "sidelink"              # sidelink | uplink
      resource_pool: "semi_persistent"
      tx_power_dbm: 23
      bandwidth_mhz: 10
      subchannel_count: 5
  message:
    bsm:
      enabled: true
      transmission_interval_ms: 100  # 10 Hz
      max_payload_bytes: 300
      include_path_history: true
      include_path_history_points: 15
      include_vehicle_classification: true
      include_exterior_lights: true
    spat:
      enabled: true
      query_interval_ms: 1000
    map:
      enabled: true
      cache_size: 50                # number of intersection MAPs
    tim:
      enabled: true
      update_interval_ms: 5000
  pki:
    scms_enabled: true
    certificate_store: "/etc/v2x/pki/certs"
    crl_check_interval_s: 300
    misbehavior_threshold: 10       # reports before revocation request
  geo_fencing:
    enabled: true
    rules_file: "/etc/v2x/geofence/rules.json"
    max_zones: 100
```

### Channel Allocation (DSRC)

| Channel | Frequency (MHz) | Use Case | Max Duration |
|---------|-----------------|----------|-------------|
| 172 (SCH1) | 5.860–5.870 | Vehicle safety (V2V) | 50 ms |
| 174 (SCH2) | 5.870–5.880 | Public safety | 50 ms |
| 176 (SCH3) | 5.880–5.890 | Non-safety | 50 ms |
| 178 (CCH) | 5.890–5.900 | Control (BSM, SPaT, MAP) | 50 ms |
| 180 (SCH4) | 5.900–5.910 | Personal safety (V2P) | 50 ms |

### C-V2X Resource Allocation

```
┌──────────────────────────────────────────────────┐
│          C-V2X Sidelink (PC5)                     │
│                                                    │
│  ┌────────────────────────────────────────────┐   │
│  │  Semi-Persistent Scheduling (SPS)          │   │
│  │  ┌──────┐┌──────┐┌──────┐┌──────┐         │   │
│  │  │Subch0││Subch1││Subch2││Subch3│  ...     │   │
│  │  │ V2V  ││ V2V  ││ V2I  ││ V2P  │         │   │
│  │  └──────┘└──────┘└──────┘└──────┘         │   │
│  │  Grant period: 100 ms (aligned with BSM)   │   │
│  └────────────────────────────────────────────┘   │
│                                                    │
│  Sensing-based selection:                          │
│  1. Measure RSRP on candidate subchannels          │
│  2. Select subchannel with lowest interference      │
│  3. Transmit at sensed power + margin              │
│  4. Re-select every 500 ms or on collision          │
└──────────────────────────────────────────────────┘
```

## Architecture Patterns

### V2X Stack Architecture

```
┌─────────────────────────────────────────────────────────┐
│                 APPLICATION LAYER                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ BSM      │  │ SPaT/MAP │  │ Coop     │  │ TIM /  │ │
│  │ Tx/Rx    │  │ Handler  │  │ Percep.  │  │ Traveler│ │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘ │
│       │              │              │             │      │
├───────┴──────────────┴──────────────┴─────────────┴──────┤
│                 FACADE LAYER (Unified API)                │
│  ┌──────────────────────────────────────────────────┐   │
│  │  V2XAdapter                                       │   │
│  │  send(message_type, payload, destination)         │   │
│  │  subscribe(message_type, callback)                │   │
│  └──────────────────────┬───────────────────────────┘   │
├──────────────────────────┼───────────────────────────────┤
│                 MIDDLEWARE LAYER                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐ │
│  │ Message  │  │ Geo-     │  │ Misbehavior│ │ PKI /  │ │
│  │ Codec    │  │ Fencing  │  │ Detection  │ │ SCMS   │ │
│  │ (ASN.1/ │  │ Engine   │  │ Module     │ │ Manager│ │
│  │  UPER)   │  │          │  │            │ │        │ │
│  └────┬─────┘  └────┬─────┘  └────┬──────┘  └───┬────┘ │
│       │              │              │             │      │
├───────┴──────────────┴──────────────┴─────────────┴──────┤
│                 NETWORK LAYER                             │
│  ┌──────────────┐            ┌──────────────┐            │
│  │  DSRC /      │            │  C-V2X /     │            │
│  │  IEEE 802.11p│            │  3GPP PC5    │            │
│  │  WAVE/WSMP   │            │  sidelink    │            │
│  └──────┬───────┘            └──────┬───────┘            │
├─────────┴────────────────────────────┴───────────────────┤
│                 PHYSICAL LAYER                            │
│  ┌──────────────────┐      ┌──────────────────┐         │
│  │  DSRC OBU Module  │      │  C-V2X Modem     │         │
│  │  (5.9 GHz)        │      │  (PC5 + Uu)      │         │
│  └──────────────────┘      └──────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### Message Flow — V2V Cooperative Awareness

```
 Vehicle A                    Vehicle B
    │                            │
    │  ┌──────────────────┐      │
    │  │ Generate BSM:    │      │
    │  │ - GPS position   │      │
    │  │ - Heading, speed │      │
    │  │ - Vehicle size   │      │
    │  │ - Path history   │      │
    │  │ - Exterior lights│      │
    │  └────────┬─────────┘      │
    │           │                │
    │  ┌────────▼─────────┐      │
    │  │ SCMS sign BSM    │      │
    │  │ (ECDSA + pseudonym│     │
    │  │  certificate)    │      │
    │  └────────┬─────────┘      │
    │           │                │
    │  ═════════╪═══════════════ │  Broadcast on CCH
    │           │    BSM @ 10 Hz │
    │           │───────────────▶│
    │           │                │
    │           │      ┌────────▼─────────┐
    │           │      │ Verify SCMS sig  │
    │           │      │ Check CRL        │
    │           │      │ Misbehavior eval │
    │           │      └────────┬─────────┘
    │           │               │
    │           │      ┌────────▼─────────┐
    │           │      │ Update object    │
    │           │      │ tracker (EKF)    │
    │           │      │ Predict path     │
    │           │      │ Assess collision │
    │           │      │ risk             │
    │           │      └──────────────────┘
```

### Cooperative Perception Message Exchange

```
┌──────────────────┐         ┌──────────────────┐
│   Vehicle A      │         │   Vehicle B      │
│  (Ego + Coop)    │         │  (Ego + Coop)    │
│                  │         │                  │
│  ┌──────────┐   │  CP-M   │  ┌──────────┐   │
│  │ Ego      │   │ ◀─────▶ │  │ Ego      │   │
│  │ objects  │   │         │  │ objects  │   │
│  └──────────┘   │         │  └──────────┘   │
│  ┌──────────┐   │         │  ┌──────────┐   │
│  │ Remote   │◀──┼─────────┼──│ Remote   │   │
│  │ objects  │   │         │  │ objects  │   │
│  │ (from B) │   │         │  │ (from A) │   │
│  └──────────┘   │         │  └──────────┘   │
│                  │         │                  │
│  Fusion output:  │         │  Fusion output:  │
│  360° perception │         │  360° perception │
└──────────────────┘         └──────────────────┘

CP-M = Cooperative Perception Message (SAE J3161)
  - Contains: detected objects not visible to ego vehicle
  - Each object: position, velocity, classification, confidence
  - Signed with pseudonym certificate
  - Maximum 30 objects per message
```

## Integration Guide

### Dependencies

| Component | Version | Purpose |
|-----------|---------|---------|
| `v2x-common` | >= 3.0.0 | Message definitions, ASN.1 UPER codec |
| `geo-utils` | >= 2.0.0 | GeoHash, geofence point-in-polygon |
| `crypto-pki` | >= 2.5.0 | SCMS certificate management, ECDSA verification |
| `perception-fusion` | >= 3.0.0 | Multi-sensor + cooperative perception fusion |
| `common-msgs` | >= 2.0.0 | Shared protobuf message types |
| `dsrc-driver` | >= 1.5.0 | DSRC radio hardware abstraction |
| `cv2x-driver` | >= 1.2.0 | C-V2X modem control (Qualcomm 9150, Autotalks) |

### ROS 2 Integration

```python
import rclpy
from rclpy.node import Node
from v2x_common.msg import BSM, SPaT, MAPData, CoopPerception
from v2x_common.srv import TransmitMessage, QueryCertificates
from v2x_stack import V2XAdapter, GeoFenceEngine, PKIManager

class V2XNode(Node):
    def __init__(self):
        super().__init__('v2x_node')
        self.declare_parameter('radio_mode', 'dual')
        self.declare_parameter('bsm_interval_ms', 100)

        mode = self.get_parameter('radio_mode').value
        self.adapter = V2XAdapter(radio_mode=mode)
        self.geofence = GeoFenceEngine('/etc/v2x/geofence/rules.json')
        self.pki = PKIManager('/etc/v2x/pki')

        # Publishers
        self.pub_bsm_rx = self.create_publisher(BSM, '/v2x/bsm/received', 50)
        self.pub_spat_rx = self.create_publisher(SPaT, '/v2x/spat/received', 10)
        self.pub_coop_percep = self.create_publisher(
            CoopPerception, '/v2x/coop_perception', 10)

        # Subscribers
        self.sub_bsm_tx = self.create_subscription(
            BSM, '/v2x/bsm/to_send', self._on_bsm_to_send, 10)
        self.sub_localization = self.create_subscription(
            Odometry, '/localization/odometry', self._on_localization, 10)

        # V2X receive callback
        self.adapter.on_message = self._on_v2x_message

        # Timer for BSM transmission
        interval_ms = self.get_parameter('bsm_interval_ms').value
        self.create_timer(interval_ms / 1000.0, self._transmit_bsm)

    def _on_v2x_message(self, msg_type: str, payload: bytes, metadata: dict):
        if msg_type == 'BSM':
            decoded = self.adapter.decode_bsm(payload)
            if self.pki.verify_signature(decoded):
                self.pub_bsm_rx.publish(decoded)
        elif msg_type == 'SPaT':
            decoded = self.adapter.decode_spat(payload)
            self.pub_spat_rx.publish(decoded)
        elif msg_type == 'CPM':
            decoded = self.adapter.decode_coop_perception(payload)
            self.pub_coop_percep.publish(decoded)

    def _transmit_bsm(self):
        bsm = self._build_current_bsm()
        if self.geofence.is_transmission_allowed(bsm.position):
            signed = self.pki.sign(bsm)
            self.adapter.broadcast(signed)
```

### Message Encoding (ASN.1 UPER)

```python
from v2x_common.codec import BSMCodec, SPaTCodec, MAPCodec

# Encode BSM to bytes
bsm_msg = BSMCodec.Message()
bsm_msg.header = BSMCodec.MessageHeader()
bsm_msg.header.messageID = 0  # BSM
bsm_msg.header.timeStamp = int(time.time() * 1000) & 0xFFFF
bsm_msg.data.coreData = BSMCodec.CoreData()
bsm_msg.data.coreData.lat = int(lat * 1e7)   # 1/10 microdegrees
bsm_msg.data.coreData.lon = int(lon * 1e7)
bsm_msg.data.coreData.elev = int(elev * 10)   # 10 cm units
bsm_msg.data.coreData.speed = int(speed * 50)  # 0.02 m/s units
bsm_msg.data.coreData.heading = int(heading * 80)  # 1/128 degrees

encoded_bytes = BSMCodec.encode(bsm_msg)
# Encoded size: ~50-60 bytes typical (compact UPER encoding)

# Decode BSM from bytes
decoded_msg = BSMCodec.decode(encoded_bytes)
```

## Performance Optimization

### Message Processing Latency Budget

| Stage | Budget (ms) | Notes |
|-------|-------------|-------|
| Radio RX interrupt | 0.5 | Hardware timestamp capture |
| PHY/MAC demodulation | 1.0 | 802.11p or PC5 |
| SCMS signature verification | 2.0 | ECDSA P-256 on hardware accelerator |
| CRL check | 0.5 | In-memory bloom filter |
| ASN.1 UPER decode | 0.3 | Pre-compiled codec |
| Geo-fence evaluation | 0.2 | Point-in-polygon with spatial index |
| Application callback | 0.5 | BSM object tracking update |
| **Total RX path** | **5.0** | **Budget for safety-critical processing** |

### Transmission Optimization

- **Channel switching**: On DSRC, BSMs are transmitted on both CCH and SCH1 for maximum reach. The WAVE Short Message Protocol (WSMP) header includes a channel identifier.
- **Power control**: Transmission power is dynamically adjusted based on vehicle density (measured via BSM reception rate). In dense traffic, reduce power to minimize channel congestion.
- **Congestion control**: Implements SAE J2945/1 congestion control — DCC (Decentralized Congestion Control) adjusts transmission rate and power based on channel busy ratio (CBR).
- **Message prioritization**: Safety-critical BSMs always take precedence over TIM and non-safety messages.
- **Batch reception**: On C-V2X, batch processing of multiple PC5 PDU reception reduces per-message interrupt overhead.

### Channel Busy Ratio Management

```
CBR (Channel Busy Ratio)
│
│  100% ┤ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ BLOCKED — no transmissions
│       │
│   50% ┤ ░░░░░░░░░░░░░░░░ Reduced rate + power
│       │
│   25% ┤ ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ Normal operation
│       │
│    0% ┤──────────────────── Full rate + power
│
│       ◀──────────────────▶ Time
│
│  DCC Algorithm:
│  1. Measure CBR over 100 ms window
│  2. If CBR > 50%: reduce BSM rate to 5 Hz, power to 10 dBm
│  3. If CBR > 75%: reduce BSM rate to 2 Hz, power to 5 dBm
│  4. If CBR < 25%: restore to configured defaults
```

## Security Considerations

### SCMS (Security Credential Management System)

```
┌──────────────────────────────────────────────────┐
│                  SCMS Architecture                │
│                                                    │
│  ┌──────────────┐    ┌──────────────────────┐     │
│  │  Enrollment  │    │  Pseudonym Certificate│     │
│  │  Certificate │    │  Pool (100-10000)     │     │
│  │  (Long-term) │    │  Rotate every 5 min  │     │
│  └──────┬───────┘    └──────────┬───────────┘     │
│         │                       │                  │
│         │  ┌────────────────────▼──────────┐      │
│         │  │  Linkage Value (LV) System    │      │
│         │  │  Prevents tracking across     │      │
│         │  │  pseudonym rotations          │      │
│         │  └───────────────────────────────┘      │
│         │                                          │
│  ┌──────▼───────┐    ┌──────────────────────┐     │
│  │  Misbehavior │    │  Revocation          │     │
│  │  Detection   │───▶│  (CRL + bitmap)      │     │
│  │  (MBD)       │    │  Distributed to OBU  │     │
│  └──────────────┘    └──────────────────────┘     │
└──────────────────────────────────────────────────┘
```

### Misbehavior Detection (MBD)

The MBD module monitors incoming BSMs for anomalies:

1. **Position consistency**: Check if reported GPS position is consistent with radio signal characteristics (RSSI-based ranging). Flag > 100 m discrepancy.
2. **Speed consistency**: Verify reported speed is physically plausible given acceleration limits.
3. **Platoon consistency**: In cooperative driving, check if a vehicle's reported state is consistent with platoon leader's commands.
4. **Certificate freshness**: Detect replayed BSMs with stale pseudonym certificates.
5. **Content consistency**: Compare BSM fields against expected values from prior messages (e.g., sudden teleportation).

### Threat Model

| Threat | Mitigation |
|--------|-----------|
| GPS spoofing | Cross-validate with cooperative perception and map matching |
| BSM replay attack | Pseudonym rotation every 5 min + monotonic sequence number |
| Sybil attack | Linkage value system detects same entity using multiple pseudonyms |
| DoS on CCH | DCC congestion control + rate limiting |
| Certificate forgery | ECDSA P-256 with hardware security module (HSM) |
| Eavesdropping | BSM content is privacy-preserving (pseudonyms); no encrypted V2V safety data per SAE J2735 |
| Man-in-the-middle | Not applicable for broadcast V2V (no session establishment) |
| Infrastructure compromise | Mutual authentication between OBU and RSU via enrollment certificates |

### Data Privacy

- Vehicle positions are anonymized via pseudonym certificate rotation.
- BSMs do not contain VIN or license plate; the certificate chain is designed so that only the SCMS operator can link pseudonyms to enrollment.
- Path history in BSMs is truncated to 15 points (configurable) to limit tracking granularity.
- Cloud logging services receive only aggregate statistics, never individual BSM content.

## Troubleshooting Guide

| Symptom | Probable Cause | Diagnostic Steps | Resolution |
|---------|---------------|------------------|------------|
| No BSMs received from nearby vehicles | Wrong channel; radio not tuned | Check `dsrc.channel` setting; verify radio interface is UP | Ensure CCH (178) is active; restart radio interface |
| BSMs received but decode fails | ASN.1 version mismatch | Compare BSM payload size with expected; check J2735 version | Update codec to match sender's J2735 version (v6 / v7) |
| SCMS signature verification fails | Certificate expired or revoked | Check certificate validity period; query CRL status | Refresh certificate pool; ensure CRL is up to date |
| High BSM decode latency (> 5 ms) | CPU contention or large payload | Profile decode path; check for large path history arrays | Reduce `path_history_points`; pin V2X task to isolated CPU core |
| SPaT messages not received | RSU not broadcasting or out of range | Verify RSU is powered and configured; check RSSI | Ensure RSU is within 300 m; check V2I channel assignment |
| C-V2X sidelink not establishing | Resource pool misconfiguration | Check `subchannel_count` and `bandwidth_mhz`; inspect modem logs | Align resource pool with network operator config |
| Geo-fence blocking valid transmissions | Rule file out of date | Review `/etc/v2x/geofence/rules.json`; check zone coordinates | Update geo-fence rules to match current road geometry |
| Misbehavior detector raising false positives | Aggressive thresholds in urban canyons | Check RSSI-based ranging accuracy; review detection logs | Relax `position_consistency_threshold` for GPS-challenged areas |
| Channel busy ratio exceeds 80% | Dense traffic with no DCC | Check DCC parameters; monitor CBR statistics | Enable DCC; reduce BSM rate to 5 Hz; lower TX power |

## API Reference

### `V2XAdapter`

```python
class V2XAdapter:
    def __init__(self, radio_mode: str = "dual"):
        """Initialize V2X adapter with specified radio mode.

        Args:
            radio_mode: "dsrc", "cv2x", or "dual" for simultaneous operation.
        """

    def broadcast(self, message: V2XMessage) -> None:
        """Broadcast a V2X message on all active channels.

        Automatically applies DCC rate/power limits.
        Signs the message with current pseudonym certificate.
        """

    def subscribe(self, msg_type: str, callback: Callable) -> None:
        """Subscribe to received V2X messages of the given type.

        Supported msg_type: "BSM", "SPaT", "MAP", "TIM", "CPM", "PSM"
        """

    def get_channel_busy_ratio(self) -> float:
        """Return the current channel busy ratio (0.0–1.0)."""

    def get_nearby_vehicles(self, radius_m: float = 300.0) -> List[BSM]:
        """Return list of recently received BSMs within the specified radius."""

    def switch_channel(self, channel: int, duration_ms: int) -> None:
        """Manually switch DSRC channel for V2I communication."""
```

### `PKIManager`

```python
class PKIManager:
    def __init__(self, cert_store_path: str):
        """Load PKI certificates and initialize SCMS client."""

    def sign(self, message: V2XMessage) -> SignedMessage:
        """Sign a V2X message with current pseudonym certificate."""

    def verify_signature(self, message: SignedMessage) -> bool:
        """Verify SCMS signature on a received message.

        Checks: certificate validity, signature integrity, CRL status.
        Returns False if any check fails.
        """

    def rotate_pseudonym(self) -> None:
        """Manually trigger pseudonym certificate rotation."""

    def get_certificate_status(self) -> CertificateStatus:
        """Return current certificate pool status (remaining, next rotation)."""
```

### `GeoFenceEngine`

```python
class GeoFenceEngine:
    def __init__(self, rules_file: str):
        """Load geo-fence rules from JSON configuration."""

    def is_transmission_allowed(self, position: LatLon) -> bool:
        """Check if V2X transmission is allowed at the given position."""

    def get_zone_policy(self, position: LatLon) -> ZonePolicy:
        """Return the applicable zone policy (power limits, rate limits)."""

    def add_zone(self, zone: GeoFenceZone) -> None:
        """Dynamically add a geo-fence zone at runtime."""

    def remove_zone(self, zone_id: str) -> None:
        """Remove a geo-fence zone by ID."""
```

## Data Models

### BSM (Basic Safety Message) Structure

```
BSM Message:
├── header
│   ├── messageID: 0 (BSM)
│   ├── timeStamp: uint16 (ms since minute start)
│   └── endpoints: uint8[4]
└── data
    ├── coreData
    │   ├── msgCount: uint8 (0-127, rollover)
    │   ├── temporaryID: uint32 (random, changes every 5 min)
    │   ├── heading: uint16 (0.0125° units, 0-359.9875°)
    │   ├── speed: uint16 (0.02 m/s units, 0-163.82 m/s)
    │   ├── posAccuracy: PositionalAccuracy
    │   │   ├── semimajor: uint8 (0.5 m units)
    │   │   └── semiminor: uint8 (0.5 m units)
    │   ├── posConfidence: PositionConfidenceSet
    │   ├── transmission: TransmissionState (park/neutral/drive/reverse)
    │   ├── steeringWheelAngle: int8 (1.5° units)
    │   ├── lat: int32 (1/10 microdegrees, -90° to +90°)
    │   ├── lon: int32 (1/10 microdegrees, -180° to +180°)
    │   ├── elev: int16 (10 cm units, -409.5 m to +6143.9 m)
    │   └── brakes: BrakeSystemStatus
    │       ├── wheelBrakes: bitstring[5] (FL, FR, RL, RR, spare)
    │       ├── tractionControlStatus: enum
    │       ├── antiLockBrakeStatus: enum
    │       └── brakePressure: uint8 (0-127, kPa)
    ├── pathHistory (optional)
    │   └── pathHistoryPoint[1-23]
    │       └── {lat, lon, elevation, timeOffset}
    ├── pathPrediction (optional)
    │   └── pathPredictionPoint[1-3]
    │       └── {confidenceRadius, prediction}
    └── vehicleClassification (optional)
        └── classificationData
            ├── basicType: enum (unknown/motorcycle/car/van/bus/truck)
            └── vehicleSize: {length, width, height} in cm
```

### SPaT (Signal Phase and Timing) Structure

```
SPaT Message:
├── header
│   ├── messageID: 13 (SPaT)
│   └── timeStamp: uint16
└── data
    ├── intersections[1-N]
    │   ├── intersectionID: IntersectionReferenceID
    │   │   ├── region: uint16 (optional)
    │   │   └── id: uint16
    │   ├── status: IntersectionStatusObject
    │   │   ├── manualControlIsOn: boolean
    │   │   ├── stopTimeActivated: boolean
    │   │   └── malfunctionExpIndicator: boolean
    │   └── phases[1-16]
    │       ├── phaseID: uint8 (1-16, maps to MAP lane group)
    │       ├── phaseState: enum
    │       │   (unavailable/stop-protected/stop-permitted/
    │       │    protection-allowed/permissive-clearance/
    │       │    permissive-yellow/protected-clearance/
    │       │    protected-yellow/extended-clearance/
    │       │    pending)
    │       ├── timeToChange: TimeChangeDetails
    │       │   ├── startTime: TimeOffset (0.1 s)
    │       │   ├── minEndTime: TimeOffset
    │       │   ├── maxEndTime: TimeOffset
    │       │   └── likelyTime: TimeOffset
    │       └── advisories: AdvisorySpeed[0-3]
```

### Cooperative Perception Message Structure

```
CoopPerception Message:
├── header
│   ├── messageID: 41 (CPM)
│   └── stationID: uint32
└── data
    ├── management
    │   ├── referencePosition: Position
    │   ├── referenceHeading: int16 (0.0125° units)
    │   └── generationTime: DDateTime
    ├── perceivedObjectContainer
    │   └── objects[1-30]
    │       ├── objectID: uint8
    │       ├── classification: PerceivedObjectClassification
    │       │   ├── vehicle: VehicleSubclass
    │       │   ├── pedestrian: PedestrianSubclass
    │       │   └── cyclist: CyclistSubclass
    │       ├── position
    │       │   ├── x: int16 (0.1 m, -128 m to +127 m relative)
    │       │   ├── y: int16 (0.1 m, relative)
    │       │   └── z: int8 (0.1 m, relative)
    │       ├── velocity
    │       │   ├── vx: int16 (0.01 m/s, relative)
    │       │   └── vy: int16 (0.01 m/s, relative)
    │       ├── size
    │       │   ├── width: uint16 (1 cm)
    │       │   ├── length: uint16 (1 cm)
    │       │   └── height: uint16 (1 cm)
    │       ├── confidence: ConfidenceSet
    │       │   ├── positionConfidence: uint8 (0-100%)
    │       │   └── velocityConfidence: uint8 (0-100%)
    │       └── detectedBy: uint8[4] (stationIDs that detected this object)
    └── sensorInformationContainer
        └── sensors[1-N]
            ├── sensorID: uint8
            ├── sensorType: enum
            └── detectionRange: {horizontal, vertical} in degrees
```

## Deployment Guide

### Hardware Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | Dual-core ARM Cortex-A72 | Quad-core x86-64 @ 2.0 GHz |
| RAM | 2 GB | 4 GB |
| DSRC Radio | Cohda MK5 OBU | Savari MW-OBS |
| C-V2X Modem | Qualcomm 9150 | Autotalks TEKTON3 |
| GNSS | Single-frequency with SBAS | Dual-frequency RTK + IMU |
| HSM | Software-only | NXP A71CH or Microchip ATECC608B |
| Storage | 4 GB eMMC | 32 GB NVMe (for certificate storage + logs) |

### DSRC RSU Deployment

```
                    ┌─────────────────┐
                    │   RSU Cabinet   │
                    │  ┌───────────┐  │
                    │  │ RSU 4.1   │  │  Arada / Commsignia / Kapsch
                    │  │ (5.9 GHz) │  │
                    │  └─────┬─────┘  │
                    │        │        │
                    │  ┌─────▼─────┐  │
                    │  │ Ethernet  │  │
                    │  │ Switch    │  │
                    │  └─────┬─────┘  │
                    │        │        │
                    │  ┌─────▼─────┐  │
                    │  │ Edge      │  │  Intel NUC or Advantech
                    │  │ Compute   │  │
                    │  └─────┬─────┘  │
                    │        │        │
                    │  ┌─────▼─────┐  │
                    │  │ UPS 48V   │  │  Solar-powered option
                    │  └───────────┘  │
                    └────────┬────────┘
                             │
                    ─────────┼───────── Intersection
                             │
              ───────────────┼──────────── Road
                             │
                    ◀── 300 m coverage ──▶
```

### Kubernetes Sidecar Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: v2x-stack
spec:
  template:
    spec:
      containers:
      - name: v2x-node
        image: registry.example.com/v2x-node:v2.0.0
        resources:
          limits:
            cpu: "2"
            memory: "2Gi"
        env:
        - name: RADIO_MODE
          value: "dual"
        - name: SCMS_ENABLED
          value: "true"
        securityContext:
          capabilities:
            add: ["NET_RAW", "NET_ADMIN"]  # Required for raw socket access
      - name: v2x-monitor
        image: registry.example.com/v2x-monitor:v1.0.0
        resources:
          limits:
            cpu: "0.5"
            memory: "256Mi"
```

## Monitoring and Observability

### Key Metrics

| Metric | Type | Unit | Alert Threshold |
|--------|------|------|-----------------|
| `v2x_bsm_tx_count` | Counter | messages/s | < 8 (should be 10) |
| `v2x_bsm_rx_count` | Counter | messages/s | — |
| `v2x_rx_latency_ms` | Histogram | ms | p99 > 5 |
| `v2x_tx_latency_ms` | Histogram | ms | p99 > 2 |
| `v2x_spat_rx_count` | Counter | messages/s | — |
| `v2x_cpm_rx_count` | Counter | messages/s | — |
| `v2x_channel_busy_ratio` | Gauge | 0.0–1.0 | > 0.75 |
| `v2x_pki_cert_pool_remaining` | Gauge | count | < 100 |
| `v2x_misbehavior_reports` | Counter | count | > 10/hour |
| `v2x_geo_fence_blocks` | Counter | count | — |
| `v2x_dsrc_rssi_avg` | Gauge | dBm | < -85 |
| `v2x_cv2x_psrp_avg` | Gauge | dBm | < -90 |

### Dashboard Panels

- **V2X Message Volume**: Time-series of BSM/SPaT/CPM TX and RX rates
- **RF Health**: DSRC RSSI and C-V2X PSRP heatmaps by direction
- **Channel Congestion**: CBR over time with DCC intervention markers
- **PKI Status**: Certificate pool gauge, rotation events, revocation count
- **Misbehavior Detection**: Alert count by type (position inconsistency, replay, etc.)
- **Latency Distribution**: Histogram of end-to-end V2X message processing time

### Log Format

```
[2025-06-15T14:32:01.234Z] [V2X-BSM-RX] {
  "sender_id": "0x3A7F2B1C",
  "position": {"lat": 37.4220, "lon": -122.0841},
  "speed_mps": 14.2,
  "heading_deg": 270.5,
  "rssi_dbm": -72,
  "scms_valid": true,
  "decode_latency_ms": 0.3,
  "verify_latency_ms": 1.8,
  "radio": "dsrc"
}
```

## Testing Strategy

### Conformance Testing

- **SAE J2735 v6/v7 conformance**: Verify BSM encoding/decoding against SAE reference test vectors.
- **IEEE 1609.2 conformance**: SCMS certificate handling and signature verification.
- **ETSI EN 302 637-2 conformance**: Cooperative awareness message format compliance.
- **3GPP TS 36.300 conformance**: C-V2X sidelink resource allocation.

### Interoperability Testing

- Cross-vendor OBU ↔ RSU message exchange (Cohda ↔ Arada ↔ Commsignia)
- DSRC ↔ C-V2X protocol translation gateway testing
- Multi-vendor SCMS certificate interoperability

### Performance Testing

- **Throughput**: 1000+ BSMs/second decode rate on target hardware
- **Latency**: End-to-end BSM RX → application callback < 5 ms
- **Concurrency**: 200+ simultaneous BSM sources tracked without degradation
- **Stress**: Channel busy ratio at 90% → verify DCC activation

### Security Testing

- Certificate replay attack detection (resend captured BSM → must be flagged)
- GPS spoofing detection via cooperative perception cross-validation
- SCMS certificate revocation propagation time measurement
- Fuzz testing of ASN.1 codec with malformed messages

### Simulation

- SUMO + V2X simulation: 100 vehicles broadcasting BSMs
- DSRC channel model with configurable propagation loss
- Multi-hop store-and-forward validation in non-line-of-sight scenarios

## Versioning and Migration

### Semantic Versioning

- **MAJOR**: Breaking API changes, new J2735/ETSI version support, radio technology changes.
- **MINOR**: New message types, additional security features, backward-compatible.
- **PATCH**: Bug fixes, performance improvements, configuration changes.

### Migration Guide (v1.x → v2.0)

1. Update `V2XAdapter` constructor to use `radio_mode` parameter (replaces separate `DSRCAdapter` and `CV2XAdapter` classes).
2. Migrate `BSMCodec` to new ASN.1 UPER v7 codec (v6 auto-detect on receive).
3. Update PKI configuration paths from `/etc/v2x/pki/` to `/etc/v2x/pki/certs/`.
4. Replace deprecated `GeoFence` class with `GeoFenceEngine` (new rule-file format).
5. Update ROS 2 message imports from `v2x_msgs` to `v2x_common.msg`.

### Deprecation Policy

Deprecated features emit a warning for two minor versions. SCMS certificate format changes follow SCMS release cycle (typically 12-18 months).

## Glossary

| Term | Definition |
|------|-----------|
| **BSM** | Basic Safety Message — periodic broadcast containing vehicle state (SAE J2735) |
| **SPaT** | Signal Phase and Timing — RSU broadcast of traffic signal state |
| **MAP** | Intersection geometry message describing lane connectivity (SAE J2735) |
| **TIM** | Traveler Information Message — road conditions, advisories, work zones |
| **CPM** | Cooperative Perception Message — shared detected objects (SAE J3161) |
| **DSRC** | Dedicated Short-Range Communications — 5.9 GHz 802.11p-based V2X |
| **C-V2X** | Cellular V2X — 3GPP-based V2X using PC5 sidelink |
| **PC5** | 3GPP sidelink interface for direct V2V/V2I communication |
| **OBU** | On-Board Unit — V2X radio and processing in the vehicle |
| **RSU** | Roadside Unit — V2X infrastructure at intersections/highways |
| **SCMS** | Security Credential Management System — PKI for V2X |
| **DCC** | Decentralized Congestion Control — channel access management |
| **CBR** | Channel Busy Ratio — percentage of time the channel is occupied |
| **WSMP** | WAVE Short Message Protocol — transport layer for DSRC safety messages |
| **CCH** | Control Channel — DSRC channel 178 for safety messages |
| **SCH** | Service Channel — DSRC channels for non-safety or supplementary data |
| **PER** | Packet Error Rate — ratio of corrupted/received packets |
| **MBD** | Misbehavior Detection — identifying fraudulent or erroneous V2X messages |
| **HSM** | Hardware Security Module — tamper-resistant cryptographic device |

## Changelog

### v2.0.0 (2025-06-15)

- Added C-V2X sidelink support (PC5) alongside DSRC
- Added cooperative perception message (CPM) support
- Introduced unified V2XAdapter API for dual-radio operation
- Added SCMS PKI integration with pseudonym rotation
- Added misbehavior detection module
- Added geo-fence engine with dynamic zone management
- Added DCC congestion control (SAE J2945/1)
- New deployment manifests for Kubernetes

### v1.3.0 (2025-02-01)

- Added SPaT/MAP message handling
- Added TIM message support
- Improved BSM decode performance (2x faster)

### v1.2.0 (2024-10-15)

- Added SCMS certificate management
- Added geo-fence basic support
- Fixed BSM path history encoding bug

### v1.1.0 (2024-07-01)

- Added BSM transmission with configurable interval
- Added nearby vehicle tracking via BSM reception

### v1.0.0 (2024-04-01)

- Initial release with DSRC BSM transmit/receive
- Basic ASN.1 UPER codec for SAE J2735 v6

## Contributing Guidelines

### Development Workflow

1. Fork the repository and create a feature branch from `main`.
2. Implement changes with conformance test vectors for new message types.
3. Run the full test suite including interoperability tests if available.
4. Submit a pull request with:
   - Description of changes
   - SAE/ETSI/3GPP specification references
   - Test results (conformance + performance)
5. Request review from V2X protocol and security experts.

### Code Standards

- Python: PEP 8 with `ruff` linting, `mypy` strict mode
- ASN.1 codecs must be generated from official ASN.1 definitions
- All cryptographic operations must use hardware-accelerated implementations where available
- Performance benchmarks required for all changes to the message processing pipeline

### Commit Convention

Use Conventional Commits: `feat(v2x): add C-V2X PC5 sidelink support`

## License

Apache License, Version 2.0. See the repository root `LICENSE` file for full text.

Copyright 2024-2025 Awesome Grok Skills Contributors.

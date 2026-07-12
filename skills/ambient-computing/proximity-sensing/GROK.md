---
name: "proximity-sensing"
category: "ambient-computing"
version: "2.0.0"
tags: ["proximity", "ble", "uwb", "rfid", "nfc", "presence-detection", "beacon", "indoor-positioning"]
---

# Proximity Sensing

## Overview

Proximity sensing platform for detecting nearby devices, people, and objects using BLE beacons, Ultra-Wideband (UWB), RFID, NFC, infrared, and WiFi RSSI. This module provides indoor positioning, presence detection, asset tracking, and proximity-based interactions with sub-meter accuracy. Supports contact tracing, retail analytics, smart access control, and occupancy monitoring with configurable ranging modes (immediate, near, far) and privacy-preserving signal processing.

## Core Capabilities

- **BLE Beacon Ranging**: RSSI-based proximity detection with iBeacon, Eddystone, and custom advertisement formats
- **UWB Positioning**: Centimeter-accurate distance measurement using IEEE 802.15.4z UWB
- **RFID/NFC Detection**: Passive and active RFID tag reading for asset tracking and access control
- **Multi-Source Fusion**: Combine BLE, UWB, WiFi, and magnetic field data for robust indoor positioning
- **Zone Management**: Define virtual zones (immediate, near, far) with configurable entry/exit events
- **Presence Detection**: Determine room occupancy from ambient sensing without identifying individuals
- **Contact Tracing**: Privacy-preserving proximity logging for epidemiological contact tracing
- **Asset Tracking**: Real-time location of tagged assets with movement detection and geofencing

## Usage

```python
from proximity_sensing import (
    ProximityManager, Beacon, UWBTag, Zone, ProximityEvent, RangingMode
)

# Initialize proximity manager
manager = ProximityManager()

# Register BLE beacons
manager.register_beacon(Beacon(
    beacon_id="entrance-beacon",
    uuid="E2C56DB5-DFFB-48D2-B060-D0F5A71096E0",
    major=1, minor=1,
    latitude=0.0, longitude=0.0,
    tx_power_dbm=-59,
))

# Register UWB tags
manager.register_uwb_tag(UWBTag(
    tag_id="asset-cart-01",
    tag_type="asset",
    location=(5.0, 3.0),
    battery_pct=85,
))

# Define proximity zones
manager.add_zone(Zone(
    zone_id="entrance-zone",
    name="Building Entrance",
    center=(0, 0),
    radius_m=3.0,
    ranging_mode=RangingMode.IMMEDIATE,
    on_enter="unlock-door",
    on_exit="lock-door",
))

# Start ranging
events = manager.scan(duration_s=10)
for event in events:
    print(f"{event.device_id}: {event.distance_m:.1f}m ({event.zone})")
    print(f"  Signal: {event.rssi_dbm} dBm, Mode: {event.ranging_mode.value}")

# Get nearby devices
nearby = manager.get_nearby_devices(max_distance_m=5.0)
print(f"\nNearby devices: {len(nearby)}")
for device in nearby:
    print(f"  {device['device_id']}: {device['distance_m']:.1f}m")
```

## Best Practices

- Calibrate BLE TX power per beacon — factory defaults vary by ±3 dBm
- Use median filtering on RSSI readings to reduce multipath noise (window size: 5-10 samples)
- Deploy beacons in a triangular pattern with 6-10m spacing for optimal coverage
- Use UWB for applications requiring <30cm accuracy; BLE for meter-level proximity
- Implement timeout-based presence detection — don't rely solely on beacon advertisements
- Rotate contact tracing identifiers every 15 minutes to prevent tracking
- Account for body attenuation (human body absorbs 10-15 dBm of BLE signal)
- Use WiFi RTT (802.11mc) as backup when BLE beacon density is insufficient
- Monitor beacon battery levels and signal health as part of infrastructure management
- Place beacons at 2-3m height for optimal line-of-sight propagation

## Related Modules

- **context-aware** — Proximity data feeds location context for adaptive applications
- **iot-integration** — Beacon and tag data through IoT protocol gateways
- **smart-environments** — Proximity-triggered building automation
- **ambient-intelligence** — Proximity-aware ambient intelligence experiences
- **api-security** → **authentication** — Proximity-based access control authentication

---
name: "mobile-forensics"
category: "forensics"
version: "2.0.0"
tags: ["forensics", "mobile-forensics", "android", "ios", "cell-phone-forensics"]
difficulty: "advanced"
estimated_time: "40-55 minutes"
prerequisites: ["python", "mobile-operating-systems", "forensics-fundamentals"]
---

# Mobile Forensics

## Overview

Mobile forensics extracts and analyzes digital evidence from smartphones, tablets, and wearable devices running Android, iOS, or other mobile operating systems. This module covers physical and logical extraction methods, application data analysis, messaging recovery, GPS/location history, call logs, photo EXIF data, cloud backup analysis, and mobile-specific anti-forensic bypass techniques.

## Core Capabilities

- **Physical Extraction**: Full file system extraction from Android (via fastboot/ADB) and iOS (via checkm8/graykey) for complete evidence recovery
- **Logical Extraction**: Backup-based extraction (iTunes backup, ADB backup) for accessible user data without root/jailbreak
- **Application Data Analysis**: Parse app-specific databases (WhatsApp, Telegram, Signal, WeChat) for messages, media, and contacts
- **GPS/Location Analysis**: Extract GPS coordinates from EXIF data, location services history, and app-collected location data
- **Communication Logs**: Recover call logs, SMS/MMS, email, and messaging app conversations with timestamps and contact info
- **Browser & Search History**: Extract browsing history, bookmarks, search queries, and cached web pages
- **Photo/Video Analysis**: EXIF metadata extraction, thumbnail recovery, deleted media recovery, and face detection
- **Cloud Backup Analysis**: Analyze iCloud, Google Drive, and Samsung Cloud backups for additional device data
- **Device Information**: Extract IMEI, phone number, SIM info, WiFi networks, Bluetooth paired devices
- **Anti-Forensic Detection**: Detect and bypass screen locks, encryption, factory reset protection, and data wiping tools

## Usage Examples

### Device Extraction

```python
from forensics.mobile_forensics import MobileExtractor, ExtractionType, DeviceOS

extractor = MobileExtractor(
    case_number="CASE-2026-0042",
    examiner="Dr. Sarah Chen",
)

# Extract from Android device
extraction = extractor.extract(
    device_type="Samsung Galaxy S24",
    device_os=DeviceOS.ANDROID,
    extraction_type=ExtractionType.PHYSICAL,
    connection="usb",
    bypass_screen_lock=True,
)

print(f"Extraction ID: {extraction.extraction_id}")
print(f"Device IMEI: {extraction.device_imei}")
print(f"Phone Number: {extraction.phone_number}")
print(f"OS Version: {extraction.os_version}")
print(f"Storage: {extraction.storage_total_gb:.1f} GB")
print(f"Extraction Size: {extraction.extraction_size_gb:.2f} GB")
print(f"Hash: {extraction.sha256_hash[:16]}...")
```

### Messaging Analysis

```python
from forensics.mobile_forensics import MessageAnalyzer, AppType

analyzer = MessageAnalyzer(
    extraction_path="evidence/phone_extraction/",
)

# Analyze WhatsApp messages
whatsapp = analyzer.analyze_app(
    app_type=AppType.WHATSAPP,
    date_range=("2026-06-01", "2026-07-01"),
)

print(f"WhatsApp Messages: {whatsapp.total_messages}")
print(f"Contacts: {whatsapp.unique_contacts}")
print(f"Media Files: {whatsapp.media_count}")
print(f"Deleted Recovered: {whatsapp.deleted_recovered}")

for msg in whatsapp.messages[:5]:
    direction = "OUT" if msg.is_outgoing else "IN"
    print(f"  [{msg.timestamp}] {direction} {msg.contact}: {msg.content[:50]}")
```

### Location Analysis

```python
from forensics.mobile_forensics import LocationAnalyzer

loc_analyzer = LocationAnalyzer(
    extraction_path="evidence/phone_extraction/",
)

# Extract location history
locations = loc_analyzer.extract_history(
    start_date="2026-06-28",
    end_date="2026-07-02",
    sources=["gps", "wifi", "cell_tower"],
)

print(f"Location Points: {len(locations.points)}")
print(f"Date Range: {locations.date_range}")
print(f"Unique Locations: {locations.unique_locations}")
print(f"Travel Distance: {locations.total_distance_km:.1f} km")

# Show significant locations
for loc in locations.significant_locations[:5]:
    print(f"  {loc.name or loc.address}: {loc.visit_count} visits, "
          f"avg {loc.avg_duration_minutes:.0f} min")
```

### Photo EXIF Analysis

```python
from forensics.mobile_forensics import PhotoAnalyzer

photo_analyzer = PhotoAnalyzer(
    extraction_path="evidence/phone_extraction/",
)

# Analyze photos
photo_analysis = photo_analyzer.analyze(
    include_deleted=True,
    extract_gps=True,
    detect_faces=True,
)

print(f"Total Photos: {photo_analysis.total_photos}")
print(f"With GPS: {photo_analysis.photos_with_gps}")
print(f"Deleted Recovered: {photo_analysis.deleted_recovered}")
print(f"Date Range: {photo_analysis.date_range}")

for photo in photo_analysis.photos_with_location[:5]:
    print(f"  {photo.filename} @ {photo.timestamp}")
    print(f"    GPS: {photo.latitude:.6f}, {photo.longitude:.6f}")
    print(f"    Device: {photo.camera_make} {photo.camera_model}")
```

## Best Practices

- Always document device state (screen lock, encryption status, battery level) before extraction
- Use Faraday bags to prevent remote wipe during evidence seizure and transport
- Attempt logical extraction first; physical extraction only when necessary for deleted data recovery
- Document all extraction methods and tools with version numbers for reproducibility
- Extract cloud data concurrently with physical extraction for comprehensive evidence coverage
- Analyze app databases with appropriate parsers (not raw SQLite) to handle encryption and encoding
- Verify extraction integrity with hash before and after analysis
- Account for device encryption; Android full-disk encryption may prevent physical extraction
- Extract and preserve device backups (iTunes, Google) as they may contain data not on the device
- Document all timestamps with timezone information; mobile devices often report UTC

## Related Modules

- `forensics/digital-investigation` - Investigation methodology and evidence handling
- `forensics/memory-forensics` - Device RAM analysis
- `forensics/disk-forensics` - Storage analysis for extracted data

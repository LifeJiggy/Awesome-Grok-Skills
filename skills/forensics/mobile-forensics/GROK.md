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

## Advanced Configuration

### Device Extraction Configuration

```yaml
device_extraction:
  android:
    physical:
      tools:
        - name: "ADB"
          version: "34.0"
          requires_root: true
          supports_encryption: false
          
        - name: "fastboot"
          version: "34.0"
          requires_unlock: true
          supports_encryption: false
          
        - name: "UFED"
          vendor: "Cellebrite"
          version: "7.68"
          supports_encryption: true
          
      bypass:
        screen_lock: true
        frp: true  # Factory Reset Protection
        encryption: false
        
    logical:
      tools:
        - name: "ADB Backup"
          version: "34.0"
          requires_root: false
          backup_types: ["apps", "shared", "system"]
          
      limitations:
        - "Cannot extract deleted data"
        - "Some apps block backup"
        - "Encrypted backups require password"
        
  ios:
    physical:
      tools:
        - name: "checkm8"
          version: "1.0"
          requires_jailbreak: true
          supported_devices: ["iPhone 4s - iPhone X"]
          
        - name: "GrayKey"
          vendor: "Grayshift"
          version: "4.x"
          supports_encryption: true
          supported_devices: ["iPhone 5s - iPhone 14"]
          
      bypass:
        screen_lock: true
        encryption: true
        usb_restricted_mode: true
        
    logical:
      tools:
        - name: "iTunes Backup"
          version: "12.x"
          requires_password: false
          backup_types: ["full", "encrypted"]
          
        - name: "iMazing"
          version: "2.x"
          backup_types: ["full", "selective"]
          
      limitations:
        - "Cannot extract keychain without password"
        - "Some data requires jailbreak"
        
  connection_settings:
    usb:
      timeout_seconds: 300
      retry_attempts: 3
      
    wifi:
      enabled: false
      security_note: "USB preferred for evidence integrity"
```

### Application Data Analysis Configuration

```yaml
app_analysis:
  messaging_apps:
    whatsapp:
      database: "msgstore.db"
      media_path: "WhatsApp/Media/"
      backup_path: "WhatsApp/Databases/"
      encryption: "AES-256"
      parse_deleted: true
      
    telegram:
      database: "cache4.db"
      media_path: "Telegram/"
      encryption: "SQLite encryption"
      parse_deleted: true
      
    signal:
      database: "signal.db"
      media_path: "Signal/"
      encryption: "SQLCipher"
      parse_deleted: false
      
    wechat:
      database: "EnMicroMsg.db"
      media_path: "MicroMsg/"
      encryption: "SQLCipher"
      parse_deleted: false
      
  social_media:
    facebook:
      data_path: "com.facebook.katana/"
      parse_messages: true
      parse_posts: true
      parse_photos: true
      
    instagram:
      data_path: "com.instagram.android/"
      parse_messages: true
      parse_posts: true
      parse_photos: true
      
    twitter:
      data_path: "com.twitter.android/"
      parse_messages: true
      parse_tweets: true
      parse_photos: true
      
  email_apps:
    gmail:
      database: "gmail.db"
      parse_emails: true
      parse_attachments: true
      
    outlook:
      database: "ost"
      parse_emails: true
      parse_attachments: true
      
  browser_apps:
    chrome:
      database: "History"
      parse_history: true
      parse_bookmarks: true
      parse_downloads: true
      
    safari:
      database: "History.db"
      parse_history: true
      parse_bookmarks: true
      
    firefox:
      database: "places.sqlite"
      parse_history: true
      parse_bookmarks: true
```

### Location Analysis Configuration

```yaml
location_analysis:
  sources:
    gps:
      enabled: true
      accuracy_threshold_meters: 10
      min_satellites: 4
      
    wifi:
      enabled: true
      accuracy_threshold_meters: 50
      require_ssid: true
      
    cell_tower:
      enabled: true
      accuracy_threshold_meters: 1000
      require_lac: true
      
    bluetooth:
      enabled: true
      accuracy_threshold_meters: 10
      
  significant_location_detection:
    algorithm: "dbscan"
    min_visits: 3
    min_duration_minutes: 5
    eps_meters: 100
    
  output:
    format: ["csv", "kml", "geojson"]
    include_timestamps: true
    include_accuracy: true
    include_source: true
```

## Architecture Patterns

### Mobile Extraction Pipeline

```python
class MobileExtractionPipeline:
    def __init__(self, device_detector, extraction_manager):
        self.detector = device_detector
        self.manager = extraction_manager
    
    async def extract(self, device_info: DeviceInfo) -> ExtractionResult:
        # Detect device
        device = await self.detector.detect(device_info)
        
        # Select extraction method
        method = self.select_extraction_method(device)
        
        # Perform extraction
        extraction = await self.manager.extract(device, method)
        
        # Verify integrity
        integrity = await self.verify_integrity(extraction)
        
        # Parse extracted data
        parsed_data = await self.parse_extracted_data(extraction)
        
        return ExtractionResult(
            device=device,
            method=method,
            extraction=extraction,
            integrity=integrity,
            parsed_data=parsed_data,
        )
    
    def select_extraction_method(self, device: Device) -> ExtractionMethod:
        if device.encryption_enabled and not device.can_bypass_encryption:
            return ExtractionMethod.LOGICAL
        elif device.jailbroken or device.rooted:
            return ExtractionMethod.PHYSICAL
        else:
            return ExtractionMethod.LOGICAL
```

### Application Data Parser

```python
class ApplicationDataParser:
    def __init__(self, db_parser, file_parser):
        self.db_parser = db_parser
        self.file_parser = file_parser
    
    async def parse_app_data(
        self,
        extraction_path: str,
        app_type: str,
    ) -> AppDataResult:
        # Get app-specific parser
        parser = self.get_parser(app_type)
        
        # Find database files
        db_files = await self.find_databases(extraction_path, app_type)
        
        # Parse databases
        messages = []
        contacts = []
        media = []
        
        for db_file in db_files:
            db_messages = await self.db_parser.parse(db_file, parser.message_schema)
            messages.extend(db_messages)
            
            db_contacts = await self.db_parser.parse(db_file, parser.contact_schema)
            contacts.extend(db_contacts)
        
        # Find media files
        media_files = await self.find_media_files(extraction_path, app_type)
        media.extend(media_files)
        
        # Recover deleted data
        deleted = await self.recover_deleted(db_files)
        
        return AppDataResult(
            app_type=app_type,
            messages=messages,
            contacts=contacts,
            media=media,
            deleted_recovered=deleted,
        )
```

### Location History Analyzer

```python
class LocationHistoryAnalyzer:
    def __init__(self, location_extractor, significant_detector):
        self.extractor = location_extractor
        self.detector = significant_detector
    
    async def analyze_locations(
        self,
        extraction_path: str,
        start_date: date,
        end_date: date,
    ) -> LocationAnalysisResult:
        # Extract location points
        points = await self.extractor.extract_all(extraction_path)
        
        # Filter by date range
        filtered = [
            p for p in points
            if start_date <= p.timestamp.date() <= end_date
        ]
        
        # Detect significant locations
        significant = await self.detector.detect(filtered)
        
        # Calculate statistics
        stats = self.calculate_statistics(filtered, significant)
        
        return LocationAnalysisResult(
            total_points=len(filtered),
            unique_locations=len(set((p.latitude, p.longitude) for p in filtered)),
            significant_locations=significant,
            statistics=stats,
            points=filtered,
        )
    
    def calculate_statistics(self, points, significant):
        if not points:
            return LocationStatistics()
        
        # Calculate total distance
        total_distance = 0
        for i in range(1, len(points)):
            distance = haversine(
                points[i-1].latitude, points[i-1].longitude,
                points[i].latitude, points[i].longitude,
            )
            total_distance += distance
        
        # Calculate time span
        time_span = points[-1].timestamp - points[0].timestamp
        
        return LocationStatistics(
            total_points=len(points),
            total_distance_km=total_distance,
            time_span_hours=time_span.total_seconds() / 3600,
            avg_speed_kmh=total_distance / (time_span.total_seconds() / 3600) if time_span.total_seconds() > 0 else 0,
        )
```

### Photo Analysis Engine

```python
class PhotoAnalysisEngine:
    def __init__(self, exif_parser, face_detector, thumbnail_recoverer):
        self.exif_parser = exif_parser
        self.face_detector = face_detector
        self.thumbnail_recoverer = thumbnail_recoverer
    
    async def analyze_photos(
        self,
        extraction_path: str,
        include_deleted: bool = True,
        extract_gps: bool = True,
        detect_faces: bool = True,
    ) -> PhotoAnalysisResult:
        # Find all photos
        photos = await self.find_photos(extraction_path)
        
        # Extract EXIF data
        for photo in photos:
            if extract_gps:
                photo.exif = await self.exif_parser.parse(photo.path)
        
        # Recover deleted thumbnails
        if include_deleted:
            deleted = await self.thumbnail_recoverer.recover(extraction_path)
            photos.extend(deleted)
        
        # Detect faces
        if detect_faces:
            for photo in photos:
                photo.faces = await self.face_detector.detect(photo.path)
        
        # Calculate statistics
        stats = self.calculate_statistics(photos)
        
        return PhotoAnalysisResult(
            total_photos=len(photos),
            photos_with_gps=sum(1 for p in photos if p.exif and p.exif.latitude),
            deleted_recovered=sum(1 for p in photos if p.is_recovered),
            statistics=stats,
            photos=photos,
        )
```

## Integration Guide

### Cellebrite UFED Integration

```python
class CellebriteIntegration:
    def __init__(self, ufed_api_url: str):
        self.api_url = ufed_api_url
    
    async def extract_device(self, device_info: DeviceInfo) -> ExtractionResult:
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "device_type": device_info.type,
            "manufacturer": device_info.manufacturer,
            "model": device_info.model,
            "os_version": device_info.os_version,
            "extraction_type": "physical",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/extract",
                headers=headers,
                json=payload,
            )
        
        return self.parse_extraction(response.json())
    
    async def get_extraction_status(self, extraction_id: str) -> ExtractionStatus:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/extractions/{extraction_id}",
            )
        
        return self.parse_status(response.json())
```

### GrayKey Integration

```python
class GrayKeyIntegration:
    def __init__(self, graykey_api_url: str):
        self.api_url = graykey_api_url
    
    async def start_extraction(self, device_info: DeviceInfo) -> ExtractionJob:
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "device_type": device_info.type,
            "serial_number": device_info.serial,
            "extraction_type": "full",
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/jobs",
                headers=headers,
                json=payload,
            )
        
        return self.parse_job(response.json())
    
    async def download_extraction(self, job_id: str, output_path: str) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/jobs/{job_id}/download",
            )
        
        with open(output_path, "wb") as f:
            f.write(response.content)
        
        return output_path
```

### ADB Integration

```python
class ADBIntegration:
    def __init__(self, adb_path: str):
        self.adb_path = adb_path
    
    async def detect_device(self) -> Optional[DeviceInfo]:
        cmd = [self.adb_path, "devices", "-l"]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        
        return self.parse_device_list(stdout.decode())
    
    async def backup_device(self, output_path: str, include_apps: bool = True) -> str:
        cmd = [self.adb_path, "backup"]
        
        if include_apps:
            cmd.extend(["-apk", "-shared"])
        
        cmd.extend(["-f", output_path])
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        
        return output_path
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_messages_app ON messages (app_type, timestamp);
CREATE INDEX idx_locations_timestamp ON location_points (timestamp);
CREATE INDEX idx_photos_date ON photos (capture_date);

-- Create full-text search index
CREATE INDEX idx_messages_content_search ON messages USING gin(to_tsvector('english', content));

-- Partition messages by date
CREATE TABLE messages (
    id UUID PRIMARY KEY,
    app_type VARCHAR(50),
    contact VARCHAR(100),
    content TEXT,
    timestamp TIMESTAMP,
    is_outgoing BOOLEAN
) PARTITION BY RANGE (timestamp);
```

### Caching Strategy

```python
class MobileForensicsCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    async def get_extraction_result(self, extraction_id: str) -> Optional[ExtractionResult]:
        cache_key = f"extraction:{extraction_id}"
        cached = await self.redis.get(cache_key)
        if cached:
            return ExtractionResult.from_json(cached)
        return None
    
    async def cache_extraction_result(self, extraction_id: str, result: ExtractionResult):
        cache_key = f"extraction:{extraction_id}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            result.to_json()
        )
```

### Batch Processing

```python
class MobileForensicsBatchProcessor:
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
    
    async def process_batch(self, devices: List[DeviceInfo], extractor: MobileExtractor):
        batches = [
            devices[i:i+self.batch_size]
            for i in range(0, len(devices), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            batch_results = await asyncio.gather(*[
                extractor.extract(device) for device in batch
            ])
            results.extend(batch_results)
        
        return results
```

## Security Considerations

### Evidence Encryption

```python
from cryptography.fernet import Fernet

class MobileEvidenceEncryption:
    def __init__(self, encryption_key: bytes):
        self.fernet = Fernet(encryption_key)
    
    def encrypt_evidence_metadata(self, data: str) -> str:
        """Encrypt sensitive evidence metadata"""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt_evidence_metadata(self, encrypted: str) -> str:
        """Decrypt sensitive evidence metadata"""
        return self.fernet.decrypt(encrypted.encode()).decode()
```

### Access Control

```python
class MobileForensicsAccessControl:
    def __init__(self):
        self.permissions = {}
        self.roles = {}
    
    def check_permission(self, user_id: str, action: str) -> bool:
        user_roles = self.roles.get(user_id, [])
        for role in user_roles:
            role_permissions = self.permissions.get(role, [])
            if action in role_permissions:
                return True
        return False
    
    def grant_role(self, user_id: str, role: str):
        if user_id not in self.roles:
            self.roles[user_id] = []
        self.roles[user_id].append(role)
```

### Audit Logging

```python
class MobileForensicsAuditLogger:
    def __init__(self, db):
        self.db = db
    
    async def log_event(self, event: AuditEvent):
        audit_entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow(),
            'actor_id': event.actor_id,
            'action': event.action,
            'resource_id': event.resource_id,
            'details': event.details,
            'ip_address': event.ip_address,
            'user_agent': event.user_agent,
        }
        
        await self.db.audit_logs.insert(audit_entry)
```

## Troubleshooting Guide

### Common Issues

**Issue: Device not detected**
```python
async def diagnose_device_detection():
    # Check USB connection
    devices = await adb.detect_devices()
    print(f"Detected devices: {len(devices)}")
    
    if len(devices) == 0:
        print(f"WARNING: No devices detected")
        print(f"Recommendations:")
        print(f"  1. Check USB cable connection")
        print(f"  2. Enable USB debugging (Android)")
        print(f"  3. Trust computer (iOS)")
        print(f"  4. Try different USB port")
        print(f"  5. Restart ADB service")
```

**Issue: Extraction fails**
```python
async def diagnose_extraction_failure(device_info: DeviceInfo, error: str):
    print(f"Extraction failed for {device_info.model}")
    print(f"Error: {error}")
    
    # Common errors and solutions
    solutions = {
        "encryption": "Try logical extraction or use decryption bypass",
        "connection": "Check USB connection and try different cable",
        "permission": "Ensure device is unlocked and USB debugging enabled",
        "timeout": "Increase timeout or try again",
    }
    
    for key, solution in solutions.items():
        if key in error.lower():
            print(f"Solution: {solution}")
```

**Issue: App data parsing errors**
```python
async def diagnose_app_parsing(app_type: str, extraction_path: str):
    # Check database files
    db_files = await find_databases(extraction_path, app_type)
    print(f"Database files found: {len(db_files)}")
    
    for db_file in db_files:
        print(f"  {db_file}: {os.path.getsize(db_file)} bytes")
    
    # Check encryption
    for db_file in db_files:
        is_encrypted = await check_encryption(db_file)
        if is_encrypted:
            print(f"  WARNING: {db_file} is encrypted")
            print(f"  Recommendation: Use appropriate decryption method")
```

## API Reference

### Device Extraction API

```python
# Extract device
POST /api/v1/extract
Request:
{
    "device_type": "Samsung Galaxy S24",
    "device_os": "android",
    "extraction_type": "physical",
    "connection": "usb",
    "bypass_screen_lock": true
}

Response:
{
    "extraction_id": "EXT-001",
    "device_imei": "123456789012345",
    "phone_number": "+1-555-0123",
    "os_version": "Android 14",
    "storage_total_gb": 256.0,
    "extraction_size_gb": 45.2,
    "sha256_hash": "abc123...",
    "status": "completed"
}

# Get extraction status
GET /api/v1/extraction/{extraction_id}
Response:
{
    "extraction_id": "EXT-001",
    "status": "completed",
    "progress": 100,
    "files_extracted": 150000,
    "messages_found": 25000,
    "photos_found": 5000
}
```

### Messaging Analysis API

```python
# Analyze messages
POST /api/v1/messages/analyze
Request:
{
    "extraction_id": "EXT-001",
    "app_type": "whatsapp",
    "date_range": {
        "start": "2026-06-01",
        "end": "2026-07-01"
    }
}

Response:
{
    "analysis_id": "MSG-001",
    "total_messages": 15000,
    "unique_contacts": 250,
    "media_count": 3000,
    "deleted_recovered": 500,
    "messages": [
        {
            "timestamp": "2026-06-15T14:30:00Z",
            "contact": "+1-555-0456",
            "content": "Hello, how are you?",
            "is_outgoing": false
        }
    ]
}
```

### Location Analysis API

```python
# Analyze locations
POST /api/v1/locations/analyze
Request:
{
    "extraction_id": "EXT-001",
    "start_date": "2026-06-28",
    "end_date": "2026-07-02",
    "sources": ["gps", "wifi", "cell_tower"]
}

Response:
{
    "analysis_id": "LOC-001",
    "total_points": 5000,
    "unique_locations": 150,
    "significant_locations": [
        {
            "name": "Home",
            "latitude": 40.7128,
            "longitude": -74.0060,
            "visit_count": 10,
            "avg_duration_minutes": 480
        }
    ],
    "statistics": {
        "total_distance_km": 250.5,
        "time_span_hours": 96
    }
}
```

## Data Models

### Device Info Model

```python
class DeviceInfo:
    device_id: str
    type: str  # smartphone, tablet, wearable
    manufacturer: str
    model: str
    os_type: str  # android, ios
    os_version: str
    serial_number: str
    imei: Optional[str]
    phone_number: Optional[str]
    storage_total_gb: float
    storage_used_gb: float
    encryption_enabled: bool
    screen_lock_enabled: bool
    battery_level: int
```

### Extraction Result Model

```python
class ExtractionResult:
    extraction_id: str
    case_number: str
    device: DeviceInfo
    method: str  # physical, logical
    extraction_path: str
    extraction_size_gb: float
    sha256_hash: str
    status: str  # in_progress, completed, failed
    files_extracted: int
    messages_found: int
    photos_found: int
    extracted_at: datetime
```

### Message Model

```python
class Message:
    message_id: str
    app_type: str
    contact: str
    content: str
    timestamp: datetime
    is_outgoing: bool
    is_deleted: bool
    media_attachments: List[str]
    metadata: Dict[str, Any]
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mobile-forensics-service
  namespace: forensics-production
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: mobile-forensics-service
  template:
    metadata:
      labels:
        app: mobile-forensics-service
    spec:
      containers:
      - name: mobile-forensics
        image: your-registry/mobile-forensics-service:2.0.0
        ports:
        - containerPort: 8443
        resources:
          requests:
            memory: "1Gi"
            cpu: "1000m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8443
          initialDelaySeconds: 10
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8443
          initialDelaySeconds: 30
          periodSeconds: 10
```

### Database Migration

```bash
# Run migrations
alembic upgrade head

# Verify migration status
alembic current

# Rollback if needed
alembic downgrade -1
```

## Monitoring & Observability

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge

# Extraction metrics
extractions_counter = Counter(
    'forensics_mobile_extractions_total',
    'Total mobile extractions',
    ['device_os', 'extraction_type', 'status']
)

extraction_duration = Histogram(
    'forensics_mobile_extraction_duration_seconds',
    'Mobile extraction duration',
    ['extraction_type'],
    buckets=[60, 300, 600, 1800, 3600]
)

# Analysis metrics
messages_analyzed_counter = Counter(
    'forensics_mobile_messages_analyzed_total',
    'Total messages analyzed',
    ['app_type']
)

photos_analyzed_counter = Counter(
    'forensics_mobile_photos_analyzed_total',
    'Total photos analyzed'
)

locations_extracted_counter = Counter(
    'forensics_mobile_locations_extracted_total',
    'Total locations extracted'
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Mobile Forensics",
    "panels": [
      {
        "title": "Extraction Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(forensics_mobile_extractions_total[5m])",
            "legendFormat": "{{device_os}} - {{status}}"
          }
        ]
      },
      {
        "title": "Messages Analyzed",
        "type": "pie",
        "targets": [
          {
            "expr": "rate(forensics_mobile_messages_analyzed_total[5m])",
            "legendFormat": "{{app_type}}"
          }
        ]
      }
    ]
  }
}
```

### Alerting Rules

```yaml
groups:
- name: mobile_forensics_alerts
  rules:
  - alert: HighExtractionFailureRate
    expr: rate(forensics_mobile_extractions_total{status="failed"}[5m]) / rate(forensics_mobile_extractions_total[5m]) > 0.2
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "Mobile extraction failure rate exceeds 20%"
      
  - alert: ExtractionBacklog
    expr: forensics_mobile_extractions_total{status="pending"} > 5
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "Mobile extraction backlog exceeds 5"
```

## Testing Strategy

### Unit Tests

```python
import pytest

class TestMessageAnalysis:
    def test_analyze_whatsapp(self, message_analyzer):
        result = message_analyzer.analyze_app(
            extraction_path="test_extraction/",
            app_type="whatsapp",
        )
        
        assert result.total_messages >= 0
        assert result.unique_contacts >= 0
    
    def test_extract_messages(self, message_extractor):
        messages = message_extractor.extract_messages(
            db_path="test_msgstore.db",
            app_type="whatsapp",
        )
        
        assert len(messages) >= 0
        for msg in messages:
            assert msg.timestamp is not None
```

### Integration Tests

```python
class TestEndToEndMobileForensics:
    async def test_extraction_flow(self, mobile_forensics_system):
        # Extract device
        result = await mobile_forensics_system.extract(
            device_info=DeviceInfo(
                type="smartphone",
                manufacturer="Samsung",
                model="Galaxy S24",
                os_type="android",
            ),
            extraction_type="logical",
        )
        
        assert result.extraction_id is not None
        assert result.status == "completed"
        
        # Analyze extraction
        analysis = await mobile_forensics_system.analyze(result.extraction_id)
        assert analysis.messages_found >= 0
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class MobileForensicsUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(5)
    def extract_device(self):
        self.client.post("/api/v1/extract", json={
            "device_type": f"Device-{self.device_counter}",
            "device_os": "android",
            "extraction_type": "logical",
        })
        self.device_counter += 1
    
    @task(10)
    def get_extraction(self):
        self.client.get(f"/api/v1/extraction/extraction-{self.extraction_counter}")
        self.extraction_counter += 1
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/extract", methods=["POST"])
@app.route("/api/v2/extract", methods=["POST"])
async def extract_device():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await extract_device_v2()
    return await extract_device_v1()
```

### Database Migration Strategy

```bash
# Forward migration
alembic upgrade head

# Specific version
alembic upgrade ae1027a6555

# Downgrade
alembic downgrade -1
```

## Glossary

- **ADB**: Android Debug Bridge - command-line tool for Android devices
- **checkm8**: iOS jailbreak exploit for older devices
- **GrayKey**: Commercial iOS extraction tool
- **UFED**: Universal Forensic Extraction Device by Cellebrite
- **IMEI**: International Mobile Equipment Identity
- **Logical Extraction**: Backup-based data extraction
- **Physical Extraction**: Full file system extraction
- **EXIF**: Exchangeable Image File Format - photo metadata
- **SQLCipher**: Encrypted SQLite database
- **Factory Reset Protection**: Anti-theft feature preventing unauthorized reset

## Changelog

### Version 2.0.0 (2026-07-01)
- Added iOS 17 support
- Implemented cloud backup analysis
- Enhanced app data parsing
- Added anti-forensic detection

### Version 1.5.0 (2026-01-15)
- Added Android 14 support
- Implemented location analysis
- Enhanced photo analysis

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic device extraction
- Message analysis

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def extract_device(
    device_info: DeviceInfo,
    extraction_type: str,
) -> ExtractionResult:
    """Extract data from mobile device.
    
    Args:
        device_info: Device information.
        extraction_type: Type of extraction.
    
    Returns:
        Extraction result.
    
    Raises:
        ExtractionError: If extraction fails.
    """
    pass
```

### Pull Request Process

1. Create feature branch from `main`
2. Write tests for new functionality
3. Ensure all tests pass
4. Update documentation if needed
5. Request review from team lead
6. Address review comments
7. Merge after approval

## License

MIT License

Copyright (c) 2026 Mobile Forensics Platform

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

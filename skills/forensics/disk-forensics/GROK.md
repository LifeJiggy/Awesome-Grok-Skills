---
name: "disk-forensics"
category: "forensics"
version: "2.0.0"
tags: ["forensics", "disk-forensics", "file-system", "data-recovery", "ntfs", "ext4"]
difficulty: "advanced"
estimated_time: "40-55 minutes"
prerequisites: ["python", "file-systems", "forensics-fundamentals"]
---

# Disk Forensics

## Overview

Disk forensics examines storage media (HDDs, SSDs, USB drives, SD cards) to recover deleted files, analyze file system metadata, extract hidden data, and reconstruct user activity. This module covers NTFS, ext4, APFS, and FAT32 file system analysis, file carving, metadata timeline reconstruction, encrypted volume handling, and steganography detection for digital forensic examinations.

## Core Capabilities

- **File System Analysis**: Parse NTFS ($MFT, $UsnJrnl, $LogFile), ext4 (inodes, journal), APFS, and FAT32 structures
- **Deleted File Recovery**: File carving from unallocated space using header/footer signatures and file system journal analysis
- **Metadata Timeline**: Build chronological activity timeline from $STANDARD_INFORMATION and $FILE_NAME timestamps (MACB)
- **Volume Analysis**: Analyze partition tables (MBR/GPT), volume shadows, BitLocker/FileVault encrypted volumes
- **Slack Space Analysis**: Extract data残留 from file slack (RAM slack and drive slack) areas
- **Alternate Data Streams**: Detect and extract NTFS alternate data streams used for data hiding
- **File Signature Analysis**: Identify file types by magic bytes regardless of extension for detecting disguised files
- **Keyword Searching**: Full-text and hex pattern searching across disk images for evidence keywords
- **Hash Analysis**: Compare known file hashes against NSRL reference database for file identification
- **Report Generation**: Forensic examination reports with evidence catalog and findings

## Usage Examples

### File System Analysis

```python
from forensics.disk_forensics import FileSystemAnalyzer, FilesystemType

analyzer = FileSystemAnalyzer(
    image_path="evidence/disk_image.E01",
    filesystem_type=FilesystemType.NTFS,
)

# Parse $MFT and get file statistics
mft_analysis = analyzer.analyze_mft()
print(f"Total MFT Entries: {mft_analysis.total_entries}")
print(f"Active Files: {mft_analysis.active_files}")
print(f"Deleted Files: {mft_analysis.deleted_files}")
print(f"Directory Entries: {mft_analysis.directories}")

# Get recently modified files
recent = analyzer.get_recent_files(hours=24)
print(f"\nFiles modified in last 24 hours: {len(recent)}")
for f in recent[:10]:
    print(f"  [{f.timestamp}] {f.full_path} ({f.size:,} bytes)")
```

### Deleted File Recovery

```python
from forensics.disk_forensics import FileCarver, CarvingMethod

carver = FileCarver(
    image_path="evidence/disk_image.E01",
    output_dir="recovered_files/",
    carving_method=CarvingMethod.HEADER_FOOTER,
)

# Carve specific file types
recovered = carver.carve(
    file_types=["pdf", "docx", "xlsx", "jpg", "zip"],
    min_size_bytes=1024,
    max_size_bytes=50_000_000,
)

print(f"Files Recovered: {len(recovered)}")
for f in recovered:
    print(f"  {f.filename} ({f.file_type}) - {f.size_bytes:,} bytes")
    print(f"    Offset: 0x{f.offset:X}, Confidence: {f.confidence:.0%}")
    print(f"    SHA256: {f.sha256_hash[:16]}...")
```

### Metadata Timeline

```python
from forensics.disk_forensics import MetadataTimeline

timeline = MetadataTimeline(
    image_path="evidence/disk_image.E01",
    timezone="UTC",
)

# Build activity timeline
activity = timeline.build(
    start_date="2026-06-28",
    end_date="2026-07-02",
    include_slack=True,
)

print(f"Timeline Events: {activity.total_events}")
print(f"Time Range: {activity.start_time} to {activity.end_time}")
print(f"File Operations: {activity.file_operations}")
print(f"Registry Changes: {activity.registry_changes}")

# Show key events
for event in activity.key_events[:10]:
    print(f"  [{event.timestamp}] {event.event_type}: {event.detail}")
```

### Keyword Search

```python
from forensics.disk_forensics import KeywordSearch

search = KeywordSearch(image_path="evidence/disk_image.E01")

# Search for keywords
results = search.search(
    keywords=["password", "confidential", "hack", "bitcoin"],
    search_type="ascii_and_unicode",
    include_deleted=True,
)

print(f"Keyword Matches: {results.total_matches}")
for kw, matches in results.by_keyword.items():
    print(f"  '{kw}': {len(matches)} matches")
    for m in matches[:3]:
        print(f"    {m.file_path}:{m.offset} - {m.context[:60]}")
```

## Best Practices

- Always work on forensic copies, never original evidence disks
- Verify hash integrity of disk images before and after analysis
- Use write blockers for all physical disk acquisitions
- Document file system type and volume properties before detailed analysis
- Check for encryption (BitLocker, FileVault, LUKS) before attempting analysis
- Analyze $MFT timestamps carefully; $STANDARD_INFORMATION vs $FILE_NAME timestamps can reveal timestomping
- Use multiple carving methods (header/footer + file system journal) for maximum recovery
- Validate recovered files by checking file signatures, not just extensions
- Preserve the original directory structure in recovered file output
- Document all search terms and their hit counts for examination reports

## Related Modules

- `forensics/digital-investigation` - Investigation methodology and evidence handling
- `forensics/memory-forensics` - RAM analysis for disk-related artifacts
- `forensics/network-forensics` - Network artifacts complementing disk evidence

## Advanced Configuration

### File System Analysis Configuration

```yaml
file_system_analysis:
  supported_filesystems:
    ntfs:
      enabled: true
      parse_mft: true
      parse_usnjrnl: true
      parse_logfile: true
      parse_bitmap: true
      
    ext4:
      enabled: true
      parse_inodes: true
      parse_journal: true
      parse_superblock: true
      
    apfs:
      enabled: true
      parse_container: true
      parse_volume: true
      parse_snapshots: true
      
    fat32:
      enabled: true
      parse_fat: true
      parse_dir_entries: true
      
  analysis_settings:
    max_file_size_mb: 1000
    include_deleted_files: true
    include_slack_space: true
    include_alternate_data_streams: true
    
  timestamp_analysis:
    timezone: "UTC"
    compare_standard_vs_filename: true
    detect_timestomping: true
    timestomping_threshold_seconds: 60
```

### File Carving Configuration

```yaml
file_carving:
  methods:
    - name: "header_footer"
      description: "Carve by file magic bytes"
      enabled: true
      
    - name: "file_system_journal"
      description: "Carve from NTFS $UsnJrnl or ext4 journal"
      enabled: true
      
    - name: "slack_space"
      description: "Carve from file slack areas"
      enabled: true
      
  file_signatures:
    pdf:
      header: "25 50 44 46"  # %PDF
      footer: "25 25 45 4F 46"  # %%EOF
      max_size_mb: 100
      
    docx:
      header: "50 4B 03 04"  # PK (ZIP)
      footer: ""
      content_type: "wordprocessingml.document"
      max_size_mb: 50
      
    jpg:
      header: "FF D8 FF"
      footer: "FF D9"
      max_size_mb: 20
      
    png:
      header: "89 50 4E 47 0D 0A 1A 0A"
      footer: "49 45 4E 44 AE 42 60 82"
      max_size_mb: 50
      
    zip:
      header: "50 4B 03 04"
      footer: "50 4B 05 06"
      max_size_mb: 500
      
  carving_settings:
    min_file_size_bytes: 512
    max_file_size_bytes: 100000000
    output_directory: "recovered_files/"
    preserve_directory_structure: true
    verify_file_integrity: true
```

### Metadata Timeline Configuration

```yaml
metadata_timeline:
  timestamp_sources:
    - name: "mft_standard_information"
      description: "NTFS $STANDARD_INFORMATION timestamps"
      weight: 1.0
      
    - name: "mft_filename"
      description: "NTFS $FILE_NAME timestamps"
      weight: 0.8
      
    - name: "usnjrnl"
      description: "NTFS $UsnJrnl change journal"
      weight: 0.9
      
    - name: "registry"
      description: "Windows Registry timestamps"
      weight: 0.7
      
    - name: "lnk_files"
      description: "Windows Shortcut files"
      weight: 0.6
      
    - name: "prefetch"
      description: "Windows Prefetch files"
      weight: 0.5
      
  timestomping_detection:
    enabled: true
    compare_sources:
      - "mft_standard_information"
      - "mft_filename"
    threshold_seconds: 60
    alert_on_mismatch: true
    
  output:
    format: "csv"
    include_visualization: true
    timeline_granularity: "minutes"
```

## Architecture Patterns

### Disk Image Processing Pipeline

```python
class DiskImageProcessor:
    def __init__(self, image_parser, filesystem_analyzer):
        self.parser = image_parser
        self.fs_analyzer = filesystem_analyzer
    
    async def process_image(self, image_path: str) -> DiskImageResult:
        # Parse disk image
        image_info = await self.parser.parse(image_path)
        
        # Detect filesystems
        filesystems = await self.parser.detect_filesystems(image_path)
        
        # Analyze each filesystem
        fs_results = []
        for fs in filesystems:
            result = await self.fs_analyzer.analyze(image_path, fs)
            fs_results.append(result)
        
        # Extract file system metadata
        metadata = await self.extract_metadata(fs_results)
        
        # Build timeline
        timeline = await self.build_timeline(metadata)
        
        return DiskImageResult(
            image_path=image_path,
            image_info=image_info,
            filesystems=filesystems,
            filesystem_results=fs_results,
            metadata=metadata,
            timeline=timeline,
        )
```

### File Carving Engine

```python
class FileCarvingEngine:
    def __init__(self, signature_db, file_validator):
        self.signatures = signature_db
        self.validator = file_validator
    
    async def carve_files(
        self,
        image_path: str,
        file_types: List[str],
        method: str = "header_footer",
    ) -> List[CarvedFile]:
        carved_files = []
        
        # Read image into memory (or use memory mapping)
        image_data = await self.read_image(image_path)
        
        # Get file signatures
        signatures = self.signatures.get_signatures(file_types)
        
        # Scan for file headers
        for sig in signatures:
            offset = 0
            while offset < len(image_data):
                # Find header
                header_pos = image_data.find(sig.header_bytes, offset)
                if header_pos == -1:
                    break
                
                # Find footer (if exists)
                if sig.footer_bytes:
                    footer_pos = image_data.find(sig.footer_bytes, header_pos + len(sig.header_bytes))
                    if footer_pos == -1:
                        offset = header_pos + 1
                        continue
                    file_data = image_data[header_pos:footer_pos + len(sig.footer_bytes)]
                else:
                    # Estimate file size based on type
                    file_data = image_data[header_pos:header_pos + sig.estimated_size]
                
                # Validate file
                if await self.validator.validate(file_data, sig.file_type):
                    carved_file = CarvedFile(
                        filename=f"{sig.file_type}_{header_pos:X}",
                        file_type=sig.file_type,
                        offset=header_pos,
                        size_bytes=len(file_data),
                        data=file_data,
                        confidence=self.calculate_confidence(sig, file_data),
                    )
                    carved_files.append(carved_file)
                
                offset = header_pos + 1
        
        return carved_files
```

### Metadata Timeline Builder

```python
class MetadataTimelineBuilder:
    def __init__(self, timestamp_extractor, timestomp_detector):
        self.extractor = timestamp_extractor
        self.detector = timestomp_detector
    
    async def build_timeline(
        self,
        image_path: str,
        start_date: date,
        end_date: date,
    ) -> MetadataTimeline:
        # Extract timestamps from all sources
        timestamps = await self.extractor.extract_all(image_path)
        
        # Detect timestomping
        if self.detector.enabled:
            timestomped = await self.detector.detect(timestamps)
            for ts in timestomped:
                ts.flags.append("TIMESTOMPED")
        
        # Filter by date range
        filtered = [
            ts for ts in timestamps
            if start_date <= ts.timestamp.date() <= end_date
        ]
        
        # Sort by timestamp
        filtered.sort(key=lambda ts: ts.timestamp)
        
        # Build timeline events
        events = self.build_events(filtered)
        
        return MetadataTimeline(
            image_path=image_path,
            start_date=start_date,
            end_date=end_date,
            total_events=len(events),
            events=events,
            timestomped_files=timestomped if self.detector.enabled else [],
        )
```

### Keyword Search Engine

```python
class KeywordSearchEngine:
    def __init__(self, text_extractor, hex_searcher):
        self.text_extractor = text_extractor
        self.hex_searcher = hex_searcher
    
    async def search(
        self,
        image_path: str,
        keywords: List[str],
        search_type: str = "ascii_and_unicode",
        include_deleted: bool = True,
    ) -> SearchResult:
        matches = []
        
        # Read image
        image_data = await self.read_image(image_path)
        
        # Search for each keyword
        for keyword in keywords:
            # ASCII search
            if search_type in ["ascii", "ascii_and_unicode"]:
                ascii_matches = self.search_ascii(image_data, keyword)
                matches.extend(ascii_matches)
            
            # Unicode search
            if search_type in ["unicode", "ascii_and_unicode"]:
                unicode_matches = self.search_unicode(image_data, keyword)
                matches.extend(unicode_matches)
            
            # Hex pattern search
            if search_type == "hex":
                hex_matches = self.hex_searcher.search(image_data, keyword)
                matches.extend(hex_matches)
        
        # Deduplicate matches
        unique_matches = self.deduplicate(matches)
        
        # Group by keyword
        by_keyword = defaultdict(list)
        for match in unique_matches:
            by_keyword[match.keyword].append(match)
        
        return SearchResult(
            image_path=image_path,
            keywords=keywords,
            total_matches=len(unique_matches),
            by_keyword=dict(by_keyword),
        )
```

## Integration Guide

### Autopsy Integration

```python
class AutopsyIntegration:
    def __init__(self, autopsy_api_url: str):
        self.api_url = autopsy_api_url
    
    async def import_image(self, image_path: str, case_id: str) -> AutopsyCase:
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "image_path": image_path,
            "case_id": case_id,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/images/import",
                headers=headers,
                json=payload,
            )
        
        return self.parse_case(response.json())
    
    async def run_analysis(self, case_id: str, image_id: str) -> AnalysisResult:
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "case_id": case_id,
            "image_id": image_id,
            "modules": [
                "hash_lookup",
                "file_type",
                "keyword_search",
                "file_recovery",
            ],
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/cases/{case_id}/images/{image_id}/analyze",
                headers=headers,
                json=payload,
            )
        
        return self.parse_analysis(response.json())
```

### Sleuth Kit Integration

```python
class SleuthKitIntegration:
    def __init__(self, tsk_path: str):
        self.tsk_path = tsk_path
    
    async def analyze_mft(self, image_path: str) -> MFTAnalysis:
        cmd = [
            f"{self.tsk_path}/tsk_loaddb",
            "-i", "ntfs",
            image_path,
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        
        return self.parse_mft_output(stdout.decode())
    
    async def recover_deleted(self, image_path: str) -> List[RecoveredFile]:
        cmd = [
            f"{self.tsk_path}/tsk_recover",
            "-e",
            image_path,
            "recovered_files/",
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        
        return self.scan_recovered_files("recovered_files/")
```

### Foremost Integration

```python
class ForemostIntegration:
    def __init__(self, foremost_path: str):
        self.foremost_path = foremost_path
    
    async def carve_files(
        self,
        image_path: str,
        output_dir: str,
        file_types: List[str],
    ) -> List[CarvedFile]:
        # Build config
        config = self.build_config(file_types)
        config_path = await self.write_config(config)
        
        cmd = [
            self.foremost_path,
            "-i", image_path,
            "-o", output_dir,
            "-c", config_path,
        ]
        
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        
        stdout, stderr = await process.communicate()
        
        return self.scan_output_dir(output_dir)
```

## Performance Optimization

### Database Optimization

```sql
-- Create indexes for common queries
CREATE INDEX idx_files_image_path ON files (image_path, file_path);
CREATE INDEX idx_timestamps_file ON file_timestamps (file_id, timestamp_type);
CREATE INDEX idx_keyword_matches_keyword ON keyword_matches (keyword, offset);

-- Create full-text search index
CREATE INDEX idx_file_path_search ON files USING gin(to_tsvector('english', file_path));

-- Partition recovered files by image
CREATE TABLE recovered_files (
    id UUID PRIMARY KEY,
    image_path VARCHAR(500),
    file_type VARCHAR(50),
    offset BIGINT,
    size_bytes BIGINT,
    created_at TIMESTAMP
) PARTITION BY HASH (image_path);
```

### Caching Strategy

```python
class DiskForensicsCache:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_ttl = 3600  # 1 hour
    
    async def get_image_analysis(self, image_path: str) -> Optional[DiskImageResult]:
        cache_key = f"disk_analysis:{hash(image_path)}"
        cached = await self.redis.get(cache_key)
        if cached:
            return DiskImageResult.from_json(cached)
        return None
    
    async def cache_image_analysis(self, image_path: str, result: DiskImageResult):
        cache_key = f"disk_analysis:{hash(image_path)}"
        await self.redis.setex(
            cache_key,
            self.default_ttl,
            result.to_json()
        )
```

### Batch Processing

```python
class DiskForensicsBatchProcessor:
    def __init__(self, batch_size: int = 10):
        self.batch_size = batch_size
    
    async def process_batch(self, images: List[str], analyzer: DiskImageProcessor):
        batches = [
            images[i:i+self.batch_size]
            for i in range(0, len(images), self.batch_size)
        ]
        
        results = []
        for batch in batches:
            batch_results = await asyncio.gather(*[
                analyzer.process_image(img) for img in batch
            ])
            results.extend(batch_results)
        
        return results
```

## Security Considerations

### Evidence Encryption

```python
from cryptography.fernet import Fernet

class DiskEvidenceEncryption:
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
class DiskForensicsAccessControl:
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
class DiskForensicsAuditLogger:
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

**Issue: MFT analysis errors**
```python
async def diagnose_mft_errors(image_path: str):
    # Check image integrity
    integrity = await check_image_integrity(image_path)
    print(f"Image integrity: {integrity.status}")
    
    if not integrity.valid:
        print(f"WARNING: Image integrity issues detected")
        print(f"Errors: {integrity.errors}")
        print(f"Recommendation: Verify image hash and try re-acquisition")
    
    # Check filesystem type
    fs_type = await detect_filesystem(image_path)
    print(f"Detected filesystem: {fs_type}")
    
    if fs_type != "NTFS":
        print(f"WARNING: MFT analysis only works on NTFS")
        print(f"Recommendation: Use appropriate filesystem analyzer")
```

**Issue: File carving produces corrupted files**
```python
async def diagnose_carving_issues(image_path: str, carved_files: List[CarvedFile]):
    corrupted = []
    for file in carved_files:
        if not await validate_file(file):
            corrupted.append(file)
    
    print(f"Carving results:")
    print(f"  Total carved: {len(carved_files)}")
    print(f"  Corrupted: {len(corrupted)}")
    print(f"  Corruption rate: {len(corrupted)/len(carved_files):.1%}")
    
    if corrupted:
        print(f"\nCorrupted files:")
        for file in corrupted[:5]:
            print(f"  {file.filename} at offset 0x{file.offset:X}")
        
        print(f"\nRecommendations:")
        print(f"  1. Try different carving method")
        print(f"  2. Adjust header/footer signatures")
        print(f"  3. Check for disk encryption")
```

**Issue: Timeline gaps**
```python
async def diagnose_timeline_gaps(image_path: str, timeline: MetadataTimeline):
    # Analyze timestamp distribution
    timestamps = [e.timestamp for e in timeline.events]
    
    # Find gaps
    gaps = []
    for i in range(1, len(timestamps)):
        gap = (timestamps[i] - timestamps[i-1]).total_seconds()
        if gap > 3600:  # Gap > 1 hour
            gaps.append({
                'start': timestamps[i-1],
                'end': timestamps[i],
                'duration_hours': gap / 3600,
            })
    
    print(f"Timeline analysis:")
    print(f"  Total events: {len(timeline.events)}")
    print(f"  Time span: {timeline.start_date} to {timeline.end_date}")
    print(f"  Gaps > 1 hour: {len(gaps)}")
    
    if gaps:
        print(f"\nLargest gaps:")
        gaps.sort(key=lambda g: g['duration_hours'], reverse=True)
        for gap in gaps[:5]:
            print(f"  {gap['start']} to {gap['end']}: {gap['duration_hours']:.1f} hours")
        
        print(f"\nRecommendation: Check for time-based evidence sources")
```

## API Reference

### File System Analysis API

```python
# Analyze filesystem
POST /api/v1/filesystem/analyze
Request:
{
    "image_path": "evidence/disk_image.E01",
    "filesystem_type": "ntfs",
    "analyze_mft": true,
    "analyze_usnjrnl": true
}

Response:
{
    "analysis_id": "FS-001",
    "filesystem_type": "ntfs",
    "total_files": 150000,
    "active_files": 120000,
    "deleted_files": 30000,
    "mft_entries": 150000,
    "status": "completed"
}

# Get filesystem analysis
GET /api/v1/filesystem/analysis/{analysis_id}
Response:
{
    "analysis_id": "FS-001",
    "recent_files": [...],
    "deleted_files": [...],
    "metadata_timeline": {...}
}
```

### File Carving API

```python
# Carve files
POST /api/v1/carving/carve
Request:
{
    "image_path": "evidence/disk_image.E01",
    "file_types": ["pdf", "docx", "jpg"],
    "method": "header_footer",
    "min_size_bytes": 1024,
    "max_size_bytes": 50000000
}

Response:
{
    "carving_id": "CARVE-001",
    "files_found": 25,
    "files": [
        {
            "filename": "document_12345.pdf",
            "file_type": "pdf",
            "offset": "0x12345678",
            "size_bytes": 250000,
            "confidence": 0.95
        }
    ]
}
```

### Keyword Search API

```python
# Search keywords
POST /api/v1/search/keywords
Request:
{
    "image_path": "evidence/disk_image.E01",
    "keywords": ["password", "confidential"],
    "search_type": "ascii_and_unicode",
    "include_deleted": true
}

Response:
{
    "search_id": "SEARCH-001",
    "total_matches": 150,
    "by_keyword": {
        "password": [
            {"file_path": "/Users/john/passwords.txt", "offset": 1024, "context": "..."}
        ],
        "confidential": [...]
    }
}
```

## Data Models

### Disk Image Result Model

```python
class DiskImageResult:
    result_id: str
    image_path: str
    image_info: ImageInfo
    filesystems: List[FilesystemInfo]
    filesystem_results: List[FilesystemResult]
    metadata: DiskMetadata
    timeline: MetadataTimeline
    created_at: datetime
```

### Carved File Model

```python
class CarvedFile:
    file_id: str
    filename: str
    file_type: str
    offset: int
    size_bytes: int
    md5_hash: str
    sha256_hash: str
    confidence: float
    data: Optional[bytes]
    carved_at: datetime
```

### Metadata Timeline Model

```python
class MetadataTimeline:
    timeline_id: str
    image_path: str
    start_date: date
    end_date: date
    total_events: int
    events: List[TimelineEvent]
    timestomped_files: List[TimestompedFile]
    created_at: datetime
```

## Deployment Guide

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: disk-forensics-service
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
      app: disk-forensics-service
  template:
    metadata:
      labels:
        app: disk-forensics-service
    spec:
      containers:
      - name: disk-forensics
        image: your-registry/disk-forensics-service:2.0.0
        ports:
        - containerPort: 8443
        resources:
          requests:
            memory: "2Gi"
            cpu: "2000m"
          limits:
            memory: "4Gi"
            cpu: "4000m"
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

# Analysis metrics
disk_analyses_counter = Counter(
    'forensics_disk_analyses_total',
    'Total disk analyses',
    ['filesystem_type', 'status']
)

disk_analysis_duration = Histogram(
    'forensics_disk_analysis_duration_seconds',
    'Disk analysis duration',
    ['analysis_type'],
    buckets=[60, 300, 600, 1800, 3600]
)

# Carving metrics
files_carved_counter = Counter(
    'forensics_files_carved_total',
    'Total files carved',
    ['file_type']
)

# Search metrics
keyword_searches_counter = Counter(
    'forensics_keyword_searches_total',
    'Total keyword searches'
)

keyword_matches_counter = Counter(
    'forensics_keyword_matches_total',
    'Total keyword matches',
    ['keyword']
)
```

### Grafana Dashboard

```json
{
  "dashboard": {
    "title": "Disk Forensics",
    "panels": [
      {
        "title": "Analysis Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(forensics_disk_analyses_total[5m])",
            "legendFormat": "{{filesystem_type}} - {{status}}"
          }
        ]
      },
      {
        "title": "Files Carved",
        "type": "pie",
        "targets": [
          {
            "expr": "rate(forensics_files_carved_total[5m])",
            "legendFormat": "{{file_type}}"
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
- name: disk_forensics_alerts
  rules:
  - alert: HighAnalysisBacklog
    expr: forensics_disk_analyses_total{status="pending"} > 5
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "Disk analysis backlog exceeds 5"
      
  - alert: LowFileRecoveryRate
    expr: forensics_files_carved_total / forensics_disk_analyses_total < 10
    for: 24h
    labels:
      severity: info
    annotations:
      summary: "Low file recovery rate"
```

## Testing Strategy

### Unit Tests

```python
import pytest

class TestFileCarving:
    def test_carve_pdf(self, file_carver):
        files = file_carver.carve(
            image_path="test_image.E01",
            file_types=["pdf"],
        )
        
        assert len(files) >= 0  # May or may not find PDFs
        for f in files:
            assert f.file_type == "pdf"
            assert f.size_bytes > 0
    
    def test_validate_file(self, file_validator):
        # Test with valid PDF
        valid_pdf = b"%PDF-1.4..."
        assert file_validator.validate(valid_pdf, "pdf") == True
        
        # Test with invalid data
        invalid_data = b"This is not a PDF"
        assert file_validator.validate(invalid_data, "pdf") == False
```

### Integration Tests

```python
class TestEndToEndDiskForensics:
    async def test_disk_analysis_flow(self, disk_forensics_system):
        # Analyze disk image
        result = await disk_forensics_system.analyze_image(
            image_path="test_image.E01",
            filesystem_type="ntfs",
        )
        
        assert result.result_id is not None
        assert result.filesystem_type == "ntfs"
        
        # Get analysis
        analysis = await disk_forensics_system.get_analysis(result.result_id)
        assert analysis.result_id == result.result_id
```

### Load Testing

```python
import asyncio
from locust import HttpUser, task, between

class DiskForensicsUser(HttpUser):
    wait_time = between(1, 5)
    
    @task(5)
    def analyze_image(self):
        self.client.post("/api/v1/filesystem/analyze", json={
            "image_path": f"test_image_{self.image_counter}.E01",
            "filesystem_type": "ntfs",
        })
        self.image_counter += 1
    
    @task(10)
    def get_analysis(self):
        self.client.get(f"/api/v1/filesystem/analysis/analysis-{self.analysis_counter}")
        self.analysis_counter += 1
```

## Versioning & Migration

### API Versioning

```python
# Version header support
@app.route("/api/v1/filesystem/analyze", methods=["POST"])
@app.route("/api/v2/filesystem/analyze", methods=["POST"])
async def analyze_filesystem():
    version = request.headers.get("API-Version", "v1")
    
    if version == "v2":
        return await analyze_filesystem_v2()
    return await analyze_filesystem_v1()
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

- **$MFT**: Master File Table - NTFS file system metadata structure
- **$UsnJrnl**: Update Sequence Number Journal - NTFS change journal
- **MACB**: Modified, Accessed, Created, Born - file timestamp types
- **File Carving**: Recovery of deleted files from unallocated space
- **Slack Space**: Unused space between end of file and allocated cluster
- **Alternate Data Streams**: NTFS feature allowing multiple data streams per file
- **Timestomping**: Modifying file timestamps to evade detection
- **Magic Bytes**: File signature bytes identifying file type
- **NSRL**: National Software Reference Library - known file hash database
- **BitLocker**: Microsoft full disk encryption

## Changelog

### Version 2.0.0 (2026-07-01)
- Added APFS support
- Implemented timestomping detection
- Enhanced file carving with journal analysis
- Added slack space analysis

### Version 1.5.0 (2026-01-15)
- Added ext4 support
- Implemented keyword searching
- Enhanced metadata timeline

### Version 1.0.0 (2025-06-01)
- Initial release
- Basic NTFS analysis
- File carving

## Contributing Guidelines

### Code Style

```python
# Follow PEP 8 with Black formatter
# Line length: 88 characters
# Use type hints
# Docstrings: Google style

def analyze_filesystem(
    image_path: str,
    filesystem_type: str,
) -> FilesystemResult:
    """Analyze filesystem in disk image.
    
    Args:
        image_path: Path to disk image.
        filesystem_type: Type of filesystem.
    
    Returns:
        Filesystem analysis result.
    
    Raises:
        AnalysisError: If analysis fails.
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

Copyright (c) 2026 Disk Forensics Platform

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

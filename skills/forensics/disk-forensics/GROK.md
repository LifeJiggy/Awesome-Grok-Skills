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

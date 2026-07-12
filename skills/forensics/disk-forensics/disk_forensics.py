"""
Disk Forensics Module
Part of the forensics skill domain

Provides file system analysis, deleted file recovery, metadata timeline,
keyword searching, and file signature analysis for disk images.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import hashlib
import uuid


class FilesystemType(Enum):
    NTFS = "ntfs"
    EXT4 = "ext4"
    APFS = "apfs"
    FAT32 = "fat32"
    EXFAT = "exfat"
    HFS_PLUS = "hfs_plus"


class CarvingMethod(Enum):
    HEADER_FOOTER = "header_footer"
    FILE_SYSTEM_JOURNAL = "file_system_journal"
    STATIC_SIGNATURE = "static_signature"
    BIFRSTD = "bifrost"


class EventType(Enum):
    FILE_CREATE = "file_create"
    FILE_MODIFY = "file_modify"
    FILE_ACCESS = "file_access"
    FILE_DELETE = "file_delete"
    REGISTRY_CHANGE = "registry_change"
    PREFETCH = "prefetch"
    USN_JOURNAL = "usn_journal"


@dataclass
class MFTEntry:
    entry_number: int
    filename: str
    full_path: str
    is_directory: bool
    is_deleted: bool
    size_bytes: int
    created: str
    modified: str
    accessed: str
    mft_changed: str


@dataclass
class MFTAnalysis:
    total_entries: int
    active_files: int
    deleted_files: int
    directories: int
    total_size_bytes: int
    file_types: Dict[str, int]


@dataclass
class RecentFile:
    full_path: str
    size: int
    timestamp: str
    timestamp_type: str  # $SI or $FN
    is_deleted: bool


@dataclass
class RecoveredFile:
    filename: str
    file_type: str
    size_bytes: int
    offset: int
    confidence: float
    sha256_hash: str
    md5_hash: str
    header_bytes: bytes


@dataclass
class TimelineEvent:
    timestamp: str
    event_type: EventType
    detail: str
    file_path: str
    source: str


@dataclass
class TimelineResult:
    total_events: int
    start_time: str
    end_time: str
    file_operations: int
    registry_changes: int
    key_events: List[TimelineEvent]
    events_by_type: Dict[str, int]


@dataclass
class KeywordMatch:
    file_path: str
    offset: int
    context: str
    keyword: str
    match_type: str  # ascii, unicode


@dataclass
class SearchResult:
    total_matches: int
    by_keyword: Dict[str, List[KeywordMatch]]
    files_searched: int


class FileSystemAnalyzer:
    """File system structure analysis for NTFS, ext4, etc."""

    def __init__(self, image_path: str, filesystem_type: FilesystemType = FilesystemType.NTFS):
        self.image_path = image_path
        self.fs_type = filesystem_type

    def analyze_mft(self) -> MFTAnalysis:
        entries = [
            MFTEntry(0, "$MFT", "\\$MFT", True, False, 0, "2026-07-01T08:00:00",
                     "2026-07-01T14:30:00", "2026-07-01T14:30:00", "2026-07-01T14:30:00"),
            MFTEntry(5, "Users", "\\Users", True, False, 0, "2026-06-15T10:00:00",
                     "2026-07-01T12:00:00", "2026-07-01T12:00:00", "2026-07-01T12:00:00"),
            MFTEntry(128, "report.docx", "\\Users\\john\\Documents\\report.docx", False, False,
                     245760, "2026-06-28T09:15:00", "2026-07-01T14:20:00",
                     "2026-07-01T14:25:00", "2026-07-01T14:20:00"),
            MFTEntry(256, "old_notes.txt", "\\Users\\john\\Desktop\\old_notes.txt", False, True,
                     4096, "2026-06-20T08:00:00", "2026-06-30T16:00:00",
                     "2026-06-30T16:05:00", "2026-06-30T16:00:00"),
        ]
        active = [e for e in entries if not e.is_deleted and not e.is_directory]
        deleted = [e for e in entries if e.is_deleted]
        dirs = [e for e in entries if e.is_directory]

        return MFTAnalysis(
            total_entries=85432, active_files=72150,
            deleted_files=3421, directories=9861,
            total_size_bytes=45_000_000_000,
            file_types={"docx": 1250, "pdf": 890, "jpg": 3400, "xlsx": 420, "txt": 8900},
        )

    def get_recent_files(self, hours: int = 24) -> List[RecentFile]:
        cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
        return [
            RecentFile("\\Users\\john\\Documents\\report.docx", 245760,
                       "2026-07-01T14:20:00", "$SI", False),
            RecentFile("\\Users\\john\\Downloads\\invoice.pdf", 102400,
                       "2026-07-01T14:15:00", "$SI", False),
            RecentFile("\\Users\\john\\Desktop\\screenshot.png", 512000,
                       "2026-07-01T13:50:00", "$SI", False),
        ]


class FileCarver:
    """Deleted file recovery from unallocated space."""

    FILE_SIGNATURES = {
        "pdf": {"header": b"%PDF", "footer": b"%%EOF", "max_size": 100_000_000},
        "docx": {"header": b"PK\x03\x04", "footer": None, "max_size": 50_000_000},
        "jpg": {"header": b"\xff\xd8\xff", "footer": b"\xff\xd9", "max_size": 30_000_000},
        "xlsx": {"header": b"PK\x03\x04", "footer": None, "max_size": 50_000_000},
        "zip": {"header": b"PK\x03\x04", "footer": None, "max_size": 500_000_000},
    }

    def __init__(self, image_path: str, output_dir: str = "recovered/",
                 carving_method: CarvingMethod = CarvingMethod.HEADER_FOOTER):
        self.image_path = image_path
        self.output_dir = output_dir
        self.method = carving_method

    def carve(self, file_types: Optional[List[str]] = None,
              min_size_bytes: int = 512,
              max_size_bytes: int = 50_000_000) -> List[RecoveredFile]:
        types = file_types or list(self.FILE_SIGNATURES.keys())
        recovered = []
        for ft in types:
            if ft in self.FILE_SIGNATURES:
                sig = self.FILE_SIGNATURES[ft]
                for i in range(3):  # Simulate finding files
                    data = f"recovered_{ft}_{i}".encode()
                    recovered.append(RecoveredFile(
                        filename=f"recovered_{ft}_{i}.{ft}",
                        file_type=ft, size_bytes=1024 * (i + 1) * 100,
                        offset=0x100000 * (i + 1), confidence=0.85 + i * 0.05,
                        sha256_hash=hashlib.sha256(data).hexdigest(),
                        md5_hash=hashlib.md5(data).hexdigest(),
                        header_bytes=sig["header"],
                    ))
        return recovered


class MetadataTimeline:
    """MACB timestamp timeline reconstruction."""

    def __init__(self, image_path: str, timezone: str = "UTC"):
        self.image_path = image_path
        self.timezone = timezone

    def build(self, start_date: str, end_date: str,
              include_slack: bool = False) -> TimelineResult:
        events = [
            TimelineEvent("2026-07-01T08:00:00", EventType.FILE_CREATE,
                          "Created report.docx", "\\Users\\john\\Documents\\report.docx", "$SI"),
            TimelineEvent("2026-07-01T09:30:00", EventType.FILE_MODIFY,
                          "Modified report.docx", "\\Users\\john\\Documents\\report.docx", "$USN"),
            TimelineEvent("2026-07-01T10:15:00", EventType.REGISTRY_CHANGE,
                          "USB device connected", "\\Registry\\Machine\\Enum", "RegRipper"),
            TimelineEvent("2026-07-01T14:20:00", EventType.FILE_MODIFY,
                          "Final modification report.docx", "\\Users\\john\\Documents\\report.docx", "$SI"),
            TimelineEvent("2026-07-01T14:25:00", EventType.PREFETCH,
                          "WINWORD.EXE executed", "\\Windows\\Prefetch\\", "Prefetch"),
        ]

        by_type = {}
        for e in events:
            by_type[e.event_type.value] = by_type.get(e.event_type.value, 0) + 1

        return TimelineResult(
            total_events=len(events), start_time=start_date, end_time=end_date,
            file_operations=4, registry_changes=1,
            key_events=events, events_by_type=by_type,
        )


class KeywordSearch:
    """Full-text and hex pattern searching across disk images."""

    def __init__(self, image_path: str):
        self.image_path = image_path

    def search(self, keywords: List[str], search_type: str = "ascii_and_unicode",
               include_deleted: bool = True) -> SearchResult:
        by_keyword: Dict[str, List[KeywordMatch]] = {}
        for kw in keywords:
            matches = [
                KeywordMatch("\\Users\\john\\Documents\\notes.txt", 0x1A2B,
                             f"Meeting about {kw} project plan", kw, "ascii"),
                KeywordMatch("\\Users\\john\\Desktop\\todo.txt", 0x500,
                             f"Remember to {kw} the server", kw, "ascii"),
            ]
            by_keyword[kw] = matches

        total = sum(len(m) for m in by_keyword.values())
        return SearchResult(total_matches=total, by_keyword=by_keyword, files_searched=85432)


def main():
    print("=" * 60)
    print("  Disk Forensics Demo")
    print("=" * 60)

    # MFT analysis
    print("\n--- File System Analysis ---")
    fsa = FileSystemAnalyzer("evidence/disk.E01", FilesystemType.NTFS)
    mft = fsa.analyze_mft()
    print(f"  MFT Entries: {mft.total_entries:,}")
    print(f"  Active: {mft.active_files:,}, Deleted: {mft.deleted_files:,}")
    print(f"  Directories: {mft.directories:,}")

    recent = fsa.get_recent_files(hours=24)
    for f in recent:
        print(f"    [{f.timestamp[:16]}] {f.full_path} ({f.size:,} bytes)")

    # File carving
    print("\n--- Deleted File Recovery ---")
    fc = FileCarver("evidence/disk.E01", "recovered/")
    recovered = fc.carve(file_types=["pdf", "docx", "jpg"])
    print(f"  Files recovered: {len(recovered)}")
    for f in recovered:
        print(f"    {f.filename} ({f.size_bytes:,} bytes, confidence={f.confidence:.0%})")

    # Timeline
    print("\n--- Metadata Timeline ---")
    mt = MetadataTimeline("evidence/disk.E01")
    tl = mt.build("2026-06-28", "2026-07-02")
    print(f"  Events: {tl.total_events}, File ops: {tl.file_operations}")
    for e in tl.key_events:
        print(f"    [{e.timestamp[:16]}] {e.event_type.value}: {e.detail}")

    # Keyword search
    print("\n--- Keyword Search ---")
    ks = KeywordSearch("evidence/disk.E01")
    results = ks.search(["password", "confidential", "bitcoin"])
    print(f"  Total matches: {results.total_matches}")
    for kw, matches in results.by_keyword.items():
        print(f"    '{kw}': {len(matches)} matches")


if __name__ == "__main__":
    main()

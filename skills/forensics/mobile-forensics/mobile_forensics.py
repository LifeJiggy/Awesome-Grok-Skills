"""
Mobile Forensics Module
Part of the forensics skill domain

Provides mobile device extraction, messaging analysis, location analysis,
photo EXIF analysis, and application data parsing for Android and iOS.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import uuid


class DeviceOS(Enum):
    ANDROID = "android"
    IOS = "ios"
    HARMONYOS = "harmonyos"
    KAIOS = "kaios"


class ExtractionType(Enum):
    PHYSICAL = "physical"
    LOGICAL = "logical"
    FILE_SYSTEM = "file_system"
    MANUAL = "manual"


class AppType(Enum):
    WHATSAPP = "whatsapp"
    TELEGRAM = "telegram"
    SIGNAL = "signal"
    WECHAT = "wechat"
    SMS = "sms"
    IMESSAGE = "imessage"


@dataclass
class DeviceExtraction:
    extraction_id: str
    device_type: str
    device_os: DeviceOS
    extraction_type: ExtractionType
    device_imei: str
    phone_number: str
    os_version: str
    storage_total_gb: float
    storage_used_gb: float
    extraction_size_gb: float
    sha256_hash: str
    examiner: str
    extraction_date: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def extraction_size_gb(self) -> float:
        return self.storage_used_gb * 0.85  # Approximate extraction size


@dataclass
class Message:
    message_id: str
    contact: str
    content: str
    timestamp: str
    is_outgoing: bool
    has_media: bool
    media_type: str = ""
    is_deleted: bool = False


@dataclass
class AppAnalysis:
    app_type: AppType
    total_messages: int
    unique_contacts: int
    media_count: int
    deleted_recovered: int
    messages: List[Message]
    date_range: Tuple[str, str]


@dataclass
class LocationPoint:
    latitude: float
    longitude: float
    timestamp: str
    source: str  # gps, wifi, cell_tower
    accuracy_meters: float
    altitude: float = 0.0


@dataclass
class SignificantLocation:
    name: str
    address: str
    latitude: float
    longitude: float
    visit_count: int
    avg_duration_minutes: float
    first_visit: str
    last_visit: str


@dataclass
class LocationHistory:
    points: List[LocationPoint]
    date_range: Tuple[str, str]
    unique_locations: int
    total_distance_km: float
    significant_locations: List[SignificantLocation]


@dataclass
class PhotoInfo:
    filename: str
    timestamp: str
    latitude: float
    longitude: float
    camera_make: str
    camera_model: str
    resolution: str
    file_size: int
    is_deleted: bool = False
    has_gps: bool = False
    has_faces: bool = False


@dataclass
class PhotoAnalysis:
    total_photos: int
    photos_with_gps: int
    deleted_recovered: int
    date_range: Tuple[str, str]
    photos_with_location: List[PhotoInfo]
    unique_cameras: List[str]


class MobileExtractor:
    """Mobile device evidence extraction."""

    def __init__(self, case_number: str, examiner: str):
        self.case_number = case_number
        self.examiner = examiner

    def extract(
        self, device_type: str, device_os: DeviceOS,
        extraction_type: ExtractionType = ExtractionType.PHYSICAL,
        connection: str = "usb", bypass_screen_lock: bool = False,
    ) -> DeviceExtraction:
        imei = f"35{uuid.uuid4().hex[:12]}"
        sha = hashlib.sha256(f"{device_type}{imei}{datetime.now().isoformat()}".encode()).hexdigest()

        return DeviceExtraction(
            extraction_id=f"EXT-{uuid.uuid4().hex[:8].upper()}",
            device_type=device_type, device_os=device_os,
            extraction_type=extraction_type,
            device_imei=imei, phone_number="+1-555-0123",
            os_version="Android 14" if device_os == DeviceOS.ANDROID else "iOS 17.5",
            storage_total_gb=256.0, storage_used_gb=180.0,
            extraction_size_gb=153.0, sha256_hash=sha,
            examiner=self.examiner,
        )


class MessageAnalyzer:
    """Messaging app data extraction and analysis."""

    def __init__(self, extraction_path: str):
        self.extraction_path = extraction_path

    def analyze_app(
        self, app_type: AppType,
        date_range: Optional[Tuple[str, str]] = None,
    ) -> AppAnalysis:
        messages = [
            Message(f"MSG-{i}", f"Contact_{i}", f"Message content {i}",
                    f"2026-07-01T{10+i}:00:00", i % 3 != 0, i % 5 == 0)
            for i in range(1, 21)
        ]
        deleted = [
            Message(f"MSG-DEL-{i}", f"Deleted Contact", f"Deleted message {i}",
                    f"2026-06-28T{10+i}:00:00", True, False, is_deleted=True)
            for i in range(1, 6)
        ]

        return AppAnalysis(
            app_type=app_type, total_messages=len(messages) + len(deleted),
            unique_contacts=8, media_count=12,
            deleted_recovered=len(deleted),
            messages=messages + deleted,
            date_range=date_range or ("2026-06-01", "2026-07-01"),
        )


class LocationAnalyzer:
    """GPS and location history extraction."""

    def __init__(self, extraction_path: str):
        self.extraction_path = extraction_path

    def extract_history(
        self, start_date: str, end_date: str,
        sources: Optional[List[str]] = None,
    ) -> LocationHistory:
        points = [
            LocationPoint(40.7128 + i * 0.001, -74.0060 + i * 0.001,
                          f"2026-07-01T{8+i}:00:00",
                          sources[0] if sources else "gps", 10.0)
            for i in range(12)
        ]

        sig_locs = [
            SignificantLocation("Home", "123 Main St, New York, NY",
                                40.7128, -74.0060, 45, 480, "2026-01-01", "2026-07-01"),
            SignificantLocation("Office", "456 Work Ave, New York, NY",
                                40.7580, -73.9855, 22, 540, "2026-01-01", "2026-07-01"),
            SignificantLocation("Coffee Shop", "789 Cafe St, New York, NY",
                                40.7282, -73.7949, 15, 25, "2026-03-01", "2026-07-01"),
        ]

        return LocationHistory(
            points=points, date_range=(start_date, end_date),
            unique_locations=len(sig_locs),
            total_distance_km=12.5,
            significant_locations=sig_locs,
        )


class PhotoAnalyzer:
    """Photo and media analysis with EXIF extraction."""

    def __init__(self, extraction_path: str):
        self.extraction_path = extraction_path

    def analyze(
        self, include_deleted: bool = True,
        extract_gps: bool = True, detect_faces: bool = True,
    ) -> PhotoAnalysis:
        photos = [
            PhotoInfo(f"IMG_2026070{i}_120000.jpg", f"2026-07-01T{10+i}:00:00",
                      40.7128 + i * 0.001, -74.0060 + i * 0.001,
                      "Samsung", "SM-S926B", "4000x3000", 5_000_000,
                      has_gps=True, has_faces=i < 3)
            for i in range(1, 8)
        ]

        return PhotoAnalysis(
            total_photos=1247, photos_with_gps=892,
            deleted_recovered=23,
            date_range=("2026-01-01", "2026-07-01"),
            photos_with_location=photos,
            unique_cameras=["Samsung SM-S926B", "iPhone 15 Pro"],
        )


def main():
    print("=" * 60)
    print("  Mobile Forensics Demo")
    print("=" * 60)

    # Device extraction
    print("\n--- Device Extraction ---")
    extractor = MobileExtractor("CASE-2026-0042", "Dr. Chen")
    ext = extractor.extract("Samsung Galaxy S24", DeviceOS.ANDROID,
                            ExtractionType.PHYSICAL)
    print(f"  Extraction: {ext.extraction_id}")
    print(f"  IMEI: {ext.device_imei}")
    print(f"  Phone: {ext.phone_number}")
    print(f"  OS: {ext.os_version}")
    print(f"  Size: {ext.extraction_size_gb:.1f} GB")
    print(f"  Hash: {ext.sha256_hash[:16]}...")

    # Messaging
    print("\n--- Messaging Analysis ---")
    ma = MessageAnalyzer("evidence/phone/")
    wa = ma.analyze_app(AppType.WHATSAPP)
    print(f"  WhatsApp: {wa.total_messages} msgs, {wa.unique_contacts} contacts")
    print(f"  Deleted recovered: {wa.deleted_recovered}")
    for msg in wa.messages[:3]:
        d = "OUT" if msg.is_outgoing else "IN"
        print(f"    [{msg.timestamp[:16]}] {d} {msg.contact}: {msg.content[:40]}")

    # Location
    print("\n--- Location History ---")
    la = LocationAnalyzer("evidence/phone/")
    locs = la.extract_history("2026-06-28", "2026-07-02")
    print(f"  Points: {len(locs.points)}, Unique: {locs.unique_locations}")
    print(f"  Distance: {locs.total_distance_km:.1f} km")
    for loc in locs.significant_locations:
        print(f"    {loc.name}: {loc.visit_count} visits, avg {loc.avg_duration_minutes:.0f} min")

    # Photos
    print("\n--- Photo Analysis ---")
    pa = PhotoAnalyzer("evidence/phone/")
    photos = pa.analyze()
    print(f"  Total: {photos.total_photos}, GPS: {photos.photos_with_gps}")
    print(f"  Deleted recovered: {photos.deleted_recovered}")
    for p in photos.photos_with_location[:3]:
        print(f"    {p.filename}: GPS({p.latitude:.4f}, {p.longitude:.4f})")


if __name__ == "__main__":
    main()

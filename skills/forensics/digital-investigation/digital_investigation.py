"""
Digital Investigation Module
Part of the forensics skill domain

Provides incident response, evidence collection, chain of custody,
timeline analysis, artifact recovery, and forensic reporting.
"""

from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid
import hashlib


class IncidentType(Enum):
    MALWARE = "malware"
    DATA_BREACH = "data_breach"
    PHISHING = "phishing"
    INSIDER_THREAT = "insider_threat"
    RANSOMWARE = "ransomware"
    DENIAL_OF_SERVICE = "denial_of_service"
    UNAUTHORIZED_ACCESS = "unauthorized_access"


class Severity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class IRPhase(Enum):
    PREPARATION = "preparation"
    IDENTIFICATION = "identification"
    CONTAINMENT = "containment"
    ERADICATION = "eradication"
    RECOVERY = "recovery"
    LESSONS_LEARNED = "lessons_learned"


class EvidenceType(Enum):
    DISK_IMAGE = "disk_image"
    MEMORY_DUMP = "memory_dump"
    NETWORK_CAPTURE = "network_capture"
    MOBILE_EXTRACTION = "mobile_extraction"
    CLOUD_EXPORT = "cloud_export"
    LOG_EXPORT = "log_export"


@dataclass
class Incident:
    incident_id: str
    incident_type: IncidentType
    severity: Severity
    description: str
    reported_by: str
    affected_systems: List[str]
    current_phase: IRPhase
    playbook_name: str
    created_date: str = field(default_factory=lambda: datetime.now().isoformat())
    assigned_to: str = ""


@dataclass
class EvidenceItem:
    evidence_id: str
    case_number: str
    evidence_type: EvidenceType
    source: str
    destination: str
    md5_hash: str
    sha256_hash: str
    size_bytes: int
    write_blocker_used: bool
    examiner: str
    description: str
    acquired_date: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CustodyTransfer:
    transfer_id: str
    evidence_id: str
    from_custodian: str
    to_custodian: str
    purpose: str
    condition: str
    location: str
    hash_verified: bool
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class TimelineEvent:
    timestamp: str
    source: str
    description: str
    event_type: str
    artifact_path: str = ""
    confidence: float = 1.0


@dataclass
class TimelineResult:
    case_number: str
    total_events: int
    start_time: str
    end_time: str
    key_events: List[TimelineEvent]
    sources_processed: int


@dataclass
class CustodyReport:
    case_number: str
    total_transfers: int
    evidence_count: int
    integrity_status: str
    transfers: List[CustodyTransfer]


class IncidentResponder:
    """Structured incident response lifecycle management."""

    PLAYBOOKS = {
        IncidentType.MALWARE: "malware_response",
        IncidentType.RANSOMWARE: "ransomware_response",
        IncidentType.DATA_BREACH: "data_breach_response",
        IncidentType.PHISHING: "phishing_response",
    }

    def __init__(self, organization: str, ir_team: str = "CERT",
                 playbooks_dir: str = "playbooks/"):
        self.organization = organization
        self.ir_team = ir_team
        self.playbooks_dir = playbooks_dir
        self._incidents: Dict[str, Incident] = {}

    def create_incident(
        self, incident_type: IncidentType, severity: Severity,
        description: str, reported_by: str,
        affected_systems: Optional[List[str]] = None,
    ) -> Incident:
        iid = f"INC-{uuid.uuid4().hex[:8].upper()}"
        playbook = self.PLAYBOOKS.get(incident_type, "generic_response")
        incident = Incident(
            incident_id=iid, incident_type=incident_type,
            severity=severity, description=description,
            reported_by=reported_by,
            affected_systems=affected_systems or [],
            current_phase=IRPhase.IDENTIFICATION,
            playbook_name=playbook,
        )
        self._incidents[iid] = incident
        return incident

    def execute_phase(self, incident_id: str, phase: str,
                      actions: Optional[Dict[str, Any]] = None) -> Incident:
        incident = self._incidents.get(incident_id)
        if not incident:
            raise ValueError(f"Incident {incident_id} not found")
        incident.current_phase = IRPhase(phase)
        return incident

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        return self._incidents.get(incident_id)

    def list_incidents(self, severity: Optional[Severity] = None) -> List[Incident]:
        incidents = list(self._incidents.values())
        if severity:
            incidents = [i for i in incidents if i.severity == severity]
        return incidents


class EvidenceCollector:
    """Forensic evidence acquisition and imaging."""

    def __init__(self, case_number: str, examiner: str, lab: str = ""):
        self.case_number = case_number
        self.examiner = examiner
        self.lab = lab
        self._evidence: List[EvidenceItem] = []

    def _hash_data(self, data: str) -> Tuple[str, str]:
        md5 = hashlib.md5(data.encode()).hexdigest()
        sha256 = hashlib.sha256(data.encode()).hexdigest()
        return md5, sha256

    def image_disk(
        self, source: str, destination: str,
        evidence_type: EvidenceType = EvidenceType.DISK_IMAGE,
        write_blocker: bool = True, compression: bool = True,
        description: str = "",
    ) -> EvidenceItem:
        md5, sha256 = self._hash_data(f"{source}{destination}{datetime.now().isoformat()}")
        eid = f"EVD-{uuid.uuid4().hex[:8].upper()}"
        item = EvidenceItem(
            evidence_id=eid, case_number=self.case_number,
            evidence_type=evidence_type, source=source,
            destination=destination, md5_hash=md5, sha256_hash=sha256,
            size_bytes=500_000_000_000,  # ~500GB simulated
            write_blocker_used=write_blocker,
            examiner=self.examiner, description=description,
        )
        self._evidence.append(item)
        return item

    def capture_memory(self, target_system: str, destination: str) -> EvidenceItem:
        return self.image_disk(
            source=f"MEMORY://{target_system}",
            destination=destination,
            evidence_type=EvidenceType.MEMORY_DUMP,
            description=f"Memory capture from {target_system}",
        )

    def get_evidence(self, evidence_id: str) -> Optional[EvidenceItem]:
        for e in self._evidence:
            if e.evidence_id == evidence_id:
                return e
        return None


class ChainOfCustody:
    """Digital chain of custody management."""

    def __init__(self, case_number: str):
        self.case_number = case_number
        self._transfers: Dict[str, List[CustodyTransfer]] = {}

    def transfer(
        self, evidence_id: str, from_custodian: str, to_custodian: str,
        purpose: str, condition: str, location: str,
        hash_verified: bool = True,
    ) -> CustodyTransfer:
        tid = f"COC-{uuid.uuid4().hex[:8].upper()}"
        transfer = CustodyTransfer(
            transfer_id=tid, evidence_id=evidence_id,
            from_custodian=from_custodian, to_custodian=to_custodian,
            purpose=purpose, condition=condition, location=location,
            hash_verified=hash_verified,
        )
        self._transfers.setdefault(evidence_id, []).append(transfer)
        return transfer

    def get_chain(self, evidence_id: str) -> List[CustodyTransfer]:
        return self._transfers.get(evidence_id, [])

    def generate_report(self, case_number: str) -> CustodyReport:
        all_transfers = []
        for transfers in self._transfers.values():
            all_transfers.extend(transfers)
        integrity_ok = all(t.hash_verified for t in all_transfers)
        return CustodyReport(
            case_number=case_number,
            total_transfers=len(all_transfers),
            evidence_count=len(self._transfers),
            integrity_status="VERIFIED" if integrity_ok else "COMPROMISED",
            transfers=all_transfers,
        )


class TimelineAnalyzer:
    """Cross-source forensic timeline reconstruction."""

    def __init__(self, timezone: str = "UTC",
                 time_skew_tolerance_seconds: int = 30):
        self.timezone = timezone
        self.skew_tolerance = time_skew_tolerance_seconds

    def build_timeline(
        self, case_number: str, sources: List[Dict[str, Any]],
        filters: Optional[Dict[str, Any]] = None,
    ) -> TimelineResult:
        events = []
        for i, src in enumerate(sources):
            for j in range(5):
                ts = (datetime.now() - timedelta(hours=24 - i * 4 - j)).isoformat()
                events.append(TimelineEvent(
                    timestamp=ts, source=src.get("type", "unknown"),
                    description=f"Event {j+1} from {src.get('type', 'source')}",
                    event_type="file_modification" if j % 2 == 0 else "process_execution",
                ))

        events.sort(key=lambda e: e.timestamp)
        return TimelineResult(
            case_number=case_number, total_events=len(events),
            start_time=events[0].timestamp if events else "",
            end_time=events[-1].timestamp if events else "",
            key_events=events[:15],
            sources_processed=len(sources),
        )


def main():
    print("=" * 60)
    print("  Digital Investigation Demo")
    print("=" * 60)

    # Incident response
    print("\n--- Incident Response ---")
    responder = IncidentResponder("Acme Corp")
    inc = responder.create_incident(
        IncidentType.RANSOMWARE, Severity.HIGH,
        "Ransomware on Finance workstation",
        "EDR Alert", ["FS-001", "FIN-SERVER-01"],
    )
    print(f"  Incident: {inc.incident_id} ({inc.severity.value})")
    print(f"  Phase: {inc.current_phase.value}")
    print(f"  Playbook: {inc.playbook_name}")

    responder.execute_phase(inc.incident_id, "containment")
    print(f"  Updated phase: {responder.get_incident(inc.incident_id).current_phase.value}")

    # Evidence collection
    print("\n--- Evidence Collection ---")
    ec = EvidenceCollector("CASE-2026-0042", "Dr. Sarah Chen")
    ev = ec.image_disk("\\\\FS-001\\PhysicalDrive0", "EVIDENCE/FS001.E01",
                       description="Ransomware workstation")
    print(f"  Evidence: {ev.evidence_id}")
    print(f"  MD5: {ev.md5_hash[:16]}...")
    print(f"  SHA256: {ev.sha256_hash[:16]}...")
    print(f"  Write blocker: {ev.write_blocker_used}")

    # Chain of custody
    print("\n--- Chain of Custody ---")
    coc = ChainOfCustody("CASE-2026-0042")
    t1 = coc.transfer(ev.evidence_id, "Crime Scene Team", "Forensic Lab",
                      "Examination", "Sealed", "Lab Room 3")
    t2 = coc.transfer(ev.evidence_id, "Forensic Lab", "Evidence Vault",
                      "Storage", "Opened for analysis", "Vault A")
    print(f"  Transfers: {len(coc.get_chain(ev.evidence_id))}")
    report = coc.generate_report("CASE-2026-0042")
    print(f"  Integrity: {report.integrity_status}")

    # Timeline
    print("\n--- Timeline Analysis ---")
    ta = TimelineAnalyzer()
    tl = ta.build_timeline("CASE-2026-0042", [
        {"type": "file_system"}, {"type": "event_log"}, {"type": "browser"},
    ])
    print(f"  Events: {tl.total_events}, Sources: {tl.sources_processed}")
    for e in tl.key_events[:3]:
        print(f"    [{e.timestamp[:16]}] {e.source}: {e.description}")


if __name__ == "__main__":
    main()

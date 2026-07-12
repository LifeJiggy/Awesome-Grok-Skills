"""
DNS Management Module
Part of the networking skill domain.

DNS zone management, record lifecycle, split-horizon DNS, DNSSEC concepts,
health-checked failover, and DNS analytics.
"""

from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple


class RecordType(Enum):
    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    MX = "MX"
    TXT = "TXT"
    SRV = "SRV"
    NS = "NS"
    SOA = "SOA"
    CAA = "CAA"
    PTR = "PTR"


@dataclass
class DnsRecord:
    record_type: RecordType
    name: str
    value: str
    ttl: int = 3600
    priority: int = 0
    weight: int = 1
    port: int = 0
    enabled: bool = True

    def to_zone_line(self) -> str:
        if self.record_type == RecordType.MX:
            return f"{self.name} {self.ttl} IN {self.record_type.value} {self.priority} {self.value}"
        elif self.record_type == RecordType.SRV:
            return f"{self.name} {self.ttl} IN {self.record_type.value} {self.weight} {self.port} {self.value}"
        return f"{self.name} {self.ttl} IN {self.record_type.value} {self.value}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.record_type.value, "name": self.name,
            "value": self.value, "ttl": self.ttl, "priority": self.priority,
            "enabled": self.enabled,
        }


@dataclass
class DnsZone:
    domain: str
    soa_primary: str = "ns1"
    admin_email: str = "admin"
    default_ttl: int = 3600
    serial: int = 0
    records: List[DnsRecord] = field(default_factory=list)

    def __post_init__(self):
        if self.serial == 0:
            self.serial = int(time.time())

    def add_record(self, record: DnsRecord):
        self.records.append(record)
        self.serial = int(time.time())

    def remove_record(self, name: str, record_type: Optional[RecordType] = None):
        self.records = [
            r for r in self.records
            if not (r.name == name and (record_type is None or r.record_type == record_type))
        ]

    def get_records(self, name: Optional[str] = None,
                    record_type: Optional[RecordType] = None) -> List[DnsRecord]:
        result = self.records
        if name:
            result = [r for r in result if r.name == name]
        if record_type:
            result = [r for r in result if r.record_type == record_type]
        return result

    def generate_zone_file(self) -> str:
        lines = [
            f"$ORIGIN {self.domain}.",
            f"$TTL {self.default_ttl}",
            f"@ IN SOA {self.soa_primary}.{self.domain}. {self.admin_email.replace('@', '.')}.{self.domain}. (",
            f"    {self.serial} ; Serial",
            f"    3600       ; Refresh",
            f"    900        ; Retry",
            f"    604800     ; Expire",
            f"    86400      ; Minimum TTL",
            f")",
            "",
        ]
        for rec in sorted(self.records, key=lambda r: (r.name, r.record_type.value)):
            if rec.enabled:
                lines.append(rec.to_zone_line())
        return "\n".join(lines)

    def summary(self) -> Dict[str, Any]:
        type_counts: Dict[str, int] = {}
        for r in self.records:
            t = r.record_type.value
            type_counts[t] = type_counts.get(t, 0) + 1
        return {
            "domain": self.domain,
            "total_records": len(self.records),
            "record_types": type_counts,
            "serial": self.serial,
        }


class SplitHorizonDns:
    def __init__(self, domain: str):
        self.domain = domain
        self.internal = DnsZone(domain)
        self.external = DnsZone(domain)

    def add_internal(self, record: DnsRecord):
        self.internal.add_record(record)

    def add_external(self, record: DnsRecord):
        self.external.add_record(record)

    def generate_configs(self) -> Dict[str, str]:
        return {
            "internal": self.internal.generate_zone_file(),
            "external": self.external.generate_zone_file(),
        }

    def get_views(self) -> Dict[str, Dict[str, Any]]:
        return {
            "internal": self.internal.summary(),
            "external": self.external.summary(),
        }


class DnsHealthCheckManager:
    def __init__(self):
        self._checks: Dict[str, Dict[str, Any]] = {}

    def register(self, record_name: str, check_url: str,
                 interval: int = 60, threshold: int = 3):
        self._checks[record_name] = {
            "url": check_url, "interval": interval,
            "threshold": threshold, "status": "healthy",
            "failure_count": 0, "last_check": 0.0,
        }

    def report(self, record_name: str, is_healthy: bool):
        if record_name not in self._checks:
            return
        check = self._checks[record_name]
        check["last_check"] = time.time()
        if is_healthy:
            check["failure_count"] = 0
            check["status"] = "healthy"
        else:
            check["failure_count"] += 1
            if check["failure_count"] >= check["threshold"]:
                check["status"] = "unhealthy"

    def get_status(self) -> Dict[str, str]:
        return {name: c["status"] for name, c in self._checks.items()}

    def get_details(self) -> Dict[str, Any]:
        return dict(self._checks)


class DnsAnalytics:
    def __init__(self):
        self._queries: List[Dict[str, Any]] = []
        self._nxdomain_count: int = 0

    def record_query(self, name: str, record_type: str,
                     response_time_ms: float, success: bool):
        self._queries.append({
            "name": name, "type": record_type,
            "response_time_ms": response_time_ms, "success": success,
            "timestamp": time.time(),
        })
        if not success:
            self._nxdomain_count += 1

    def get_stats(self) -> Dict[str, Any]:
        if not self._queries:
            return {"total_queries": 0}
        times = [q["response_time_ms"] for q in self._queries]
        type_counts: Dict[str, int] = {}
        for q in self._queries:
            t = q["type"]
            type_counts[t] = type_counts.get(t, 0) + 1
        return {
            "total_queries": len(self._queries),
            "avg_response_ms": round(sum(times) / len(times), 2),
            "p95_response_ms": round(sorted(times)[int(len(times) * 0.95)], 2),
            "nxdomain_count": self._nxdomain_count,
            "nxdomain_rate": round(self._nxdomain_count / len(self._queries), 4),
            "type_distribution": type_counts,
        }


class DnsRecordValidator:
    @staticmethod
    def validate_a(value: str) -> bool:
        parts = value.split(".")
        return len(parts) == 4 and all(0 <= int(p) <= 255 for p in parts)

    @staticmethod
    def validate_cname(name: str, existing: List[DnsRecord]) -> bool:
        has_a = any(r.name == name and r.record_type == RecordType.A for r in existing)
        return not has_a

    @staticmethod
    def validate_mx(value: str) -> bool:
        parts = value.split()
        return len(parts) >= 2

    @staticmethod
    def check_ttl(ttl: int) -> Tuple[bool, str]:
        if ttl < 60:
            return False, "TTL too low, minimum 60 seconds"
        if ttl > 86400:
            return True, "TTL unusually high (>24h)"
        return True, "OK"


def main():
    print("=== DNS Management Module ===")

    print("\n=== Zone Creation ===")
    zone = DnsZone("example.com", admin_email="admin@example.com")
    zone.add_record(DnsRecord(RecordType.A, "@", "93.184.216.34", ttl=3600))
    zone.add_record(DnsRecord(RecordType.A, "www", "93.184.216.34"))
    zone.add_record(DnsRecord(RecordType.CNAME, "api", "lb.example.com"))
    zone.add_record(DnsRecord(RecordType.MX, "@", "mx1.example.com", priority=10))
    zone.add_record(DnsRecord(RecordType.TXT, "@", "v=spf1 include:_spf.example.com ~all"))
    zone.add_record(DnsRecord(RecordType.SRV, "_sip._tcp", "sip.example.com", priority=10, port=5060))

    print(zone.generate_zone_file())

    print("\n=== Zone Summary ===")
    for k, v in zone.summary().items():
        print(f"  {k}: {v}")

    print("\n=== Split-Horizon DNS ===")
    split = SplitHorizonDns("corp.internal")
    split.add_internal(DnsRecord(RecordType.A, "db", "10.0.1.10"))
    split.add_internal(DnsRecord(RecordType.A, "app", "10.0.2.10"))
    split.add_external(DnsRecord(RecordType.A, "www", "203.0.113.50"))
    split.add_external(DnsRecord(RecordType.CNAME, "api", "lb.prod.example.com"))

    configs = split.generate_configs()
    print("Internal zone:")
    print(configs["internal"][:200])
    print("\nExternal zone:")
    print(configs["external"][:200])

    print("\n=== Health Checks ===")
    health = DnsHealthCheckManager()
    health.register("api.example.com", "https://api.example.com/health")
    health.register("db.example.com", "https://db.example.com/health")
    health.report("api.example.com", True)
    health.report("api.example.com", False)
    health.report("db.example.com", False)
    health.report("db.example.com", False)
    health.report("db.example.com", False)
    print(f"  Status: {health.get_status()}")

    print("\n=== DNS Analytics ===")
    analytics = DnsAnalytics()
    for i in range(50):
        analytics.record_query(f"host{i % 5}.example.com", "A", 5 + i * 0.5, True)
    analytics.record_query("nonexistent.example.com", "A", 100, False)
    analytics.record_query("typo.example.com", "A", 150, False)
    stats = analytics.get_stats()
    for k, v in stats.items():
        print(f"  {k}: {v}")

    print("\n=== Record Validation ===")
    validator = DnsRecordValidator()
    print(f"  Valid A: {validator.validate_a('192.168.1.1')}")
    print(f"  Invalid A: {validator.validate_a('999.1.1.1')}")
    print(f"  TTL check: {validator.check_ttl(300)}")

    print("\nDone.")


if __name__ == "__main__":
    main()

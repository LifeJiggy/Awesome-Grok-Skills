---
name: dns-management
category: networking
version: 2.0.0
tags: [networking, dns, domain, zone-management, resolution]
---

# DNS Management

## Overview

DNS management toolkit covering zone file generation, record type management, split-horizon DNS, DNSSEC configuration, health-checked failover, and DNS analytics. This skill provides programmatic DNS zone management, record lifecycle automation, and DNS infrastructure monitoring for reliable name resolution.

## Core Capabilities

- **Zone Management**: SOA, NS, A, AAAA, CNAME, MX, TXT, SRV record creation
- **Split-Horizon DNS**: Internal vs. external resolution for the same domain
- **DNSSEC**: Key generation, DS record management, signature rotation
- **Health-Checked Failover**: DNS-based failover with health monitoring
- **Record Validation**: Syntax checking, propagation verification, TTL optimization
- **Bulk Operations**: Zone migration, record import/export, bulk updates
- **Analytics**: Query volume analysis, response time tracking, NXDOMAIN monitoring
- **Provider Integration**: Cloudflare, Route53, Google Cloud DNS API patterns

## Usage Examples

```python
import hashlib
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

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
    enabled: bool = True

    def to_zone_line(self) -> str:
        if self.record_type == RecordType.MX:
            return f"{self.name} {self.ttl} IN {self.record_type.value} {self.priority} {self.value}"
        elif self.record_type == RecordType.SRV:
            return f"{self.name} {self.ttl} IN {self.record_type.value} {self.value}"
        return f"{self.name} {self.ttl} IN {self.record_type.value} {self.value}"

@dataclass
class HealthCheck:
    url: str
    interval: int = 60
    timeout: int = 10
    threshold: int = 3
    status: str = "healthy"
    last_check: float = 0.0
    failure_count: int = 0

class DnsZone:
    def __init__(self, domain: str, soa_primary: str = "ns1", admin_email: str = "admin"):
        self.domain = domain
        self.soa_primary = f"{soa_primary}.{domain}"
        self.admin_email = admin_email.replace("@", ".")
        self.records: List[DnsRecord] = []
        self.serial = int(time.time())

    def add_record(self, record: DnsRecord):
        self.records.append(record)
        self.serial = int(time.time())

    def remove_record(self, name: str, record_type: RecordType):
        self.records = [r for r in self.records if not (r.name == name and r.record_type == record_type)]

    def get_records(self, name: Optional[str] = None, record_type: Optional[RecordType] = None) -> List[DnsRecord]:
        result = self.records
        if name:
            result = [r for r in result if r.name == name]
        if record_type:
            result = [r for r in result if r.record_type == record_type]
        return result

    def generate_zone_file(self) -> str:
        lines = [
            f"$ORIGIN {self.domain}.",
            f"$TTL 3600",
            f"@ IN SOA {self.soa_primary}. {self.admin_email}. (",
            f"    {self.serial} ; Serial",
            f"    3600       ; Refresh",
            f"    900        ; Retry",
            f"    604800     ; Expire",
            f"    86400      ; Minimum TTL",
            f")",
            "",
        ]
        for record in sorted(self.records, key=lambda r: (r.name, r.record_type.value)):
            if record.enabled:
                lines.append(record.to_zone_line())
        return "\n".join(lines)

class SplitHorizonDns:
    def __init__(self, domain: str):
        self.internal_zone = DnsZone(domain)
        self.external_zone = DnsZone(domain)
        self.domain = domain

    def add_internal_record(self, record: DnsRecord):
        self.internal_zone.add_record(record)

    def add_external_record(self, record: DnsRecord):
        self.external_zone.add_record(record)

    def generate_view_configs(self) -> Dict[str, str]:
        return {
            "internal": self.internal_zone.generate_zone_file(),
            "external": self.external_zone.generate_zone_file(),
        }

class DnsHealthCheck:
    def __init__(self):
        self._checks: Dict[str, HealthCheck] = {}

    def register(self, record_name: str, url: str, interval: int = 60):
        self._checks[record_name] = HealthCheck(url=url, interval=interval)

    def check(self, record_name: str, is_healthy: bool = True):
        if record_name in self._checks:
            check = self._checks[record_name]
            check.last_check = time.time()
            if is_healthy:
                check.failure_count = 0
                check.status = "healthy"
            else:
                check.failure_count += 1
                if check.failure_count >= check.threshold:
                    check.status = "unhealthy"

    def get_status(self) -> Dict[str, str]:
        return {name: check.status for name, check in self._checks.items()}

class DnsAnalytics:
    def __init__(self):
        self._queries: List[Dict] = []
        self._nxdomain_count: int = 0

    def record_query(self, name: str, record_type: str, response_time_ms: float, success: bool):
        self._queries.append({
            "name": name, "type": record_type,
            "response_time_ms": response_time_ms, "success": success,
            "timestamp": time.time(),
        })
        if not success:
            self._nxdomain_count += 1

    def get_stats(self) -> Dict:
        if not self._queries:
            return {"total_queries": 0}
        response_times = [q["response_time_ms"] for q in self._queries]
        return {
            "total_queries": len(self._queries),
            "avg_response_ms": sum(response_times) / len(response_times),
            "nxdomain_count": self._nxdomain_count,
            "nxdomain_rate": self._nxdomain_count / len(self._queries),
        }
```

## Best Practices

- Use split-horzone DNS to expose different records to internal vs. external resolvers
- Set appropriate TTL values: lower for frequently changing records, higher for stable ones
- Implement DNSSEC for domains requiring authenticity guarantees
- Monitor NXDOMAIN rates to detect DNS hijacking or misconfiguration
- Use health-checked failover for high-availability DNS configurations
- Validate zone files before deployment to prevent resolution failures
- Implement DNS query logging for security auditing and analytics
- Use CNAME chains carefully to avoid resolution loops and performance issues
- Maintain at least two authoritative nameservers for redundancy
- Automate TTL reduction before planned changes to minimize cached stale records

## Related Modules

- `network-engineering` - Network infrastructure and routing
- `load-balancing` - Traffic distribution including DNS-based LB
- `sdn` - Software-defined networking
- `traffic-analysis` - Network traffic analysis

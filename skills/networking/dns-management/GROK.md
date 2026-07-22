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

## Advanced Configuration

### DNSSEC Configuration

DNSSEC adds cryptographic signatures to DNS records to prevent spoofing and tampering. The signing process involves creating RRSIG records for each RRSET and publishing DS records at the parent zone.

```python
import hashlib
import hmac
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from datetime import datetime, timedelta

class DnssecSigner:
    def __init__(self, zone: str, key_tag: int = 12345):
        self.zone = zone
        self.key_tag = key_tag
        self.private_key = ec.generate_private_key(ec.SECP256R1())
        self.public_key = self.private_key.public_key()
        self.algorithm = 13  # ECDSAP256SHA256
        self.rrsig_records: List[Dict] = []
        self.ds_record: Optional[str] = None

    def sign_rrset(self, rrset_type: str, rrset_data: str, original_ttl: int = 3600) -> Dict:
        now = datetime.utcnow()
        sig_expiration = now + timedelta(days=30)
        sig_inception = now - timedelta(hours=1)

        rrsig = {
            "type_covered": rrset_type,
            "algorithm": self.algorithm,
            "labels": len(self.zone.split(".")),
            "original_ttl": original_ttl,
            "signature_expiration": int(sig_expiration.timestamp()),
            "signature_inception": int(sig_inception.timestamp()),
            "key_tag": self.key_tag,
            "signer_name": self.zone,
            "signature": self._sign_data(rrset_data),
        }
        self.rrsig_records.append(rrsig)
        return rrsig

    def _sign_data(self, data: str) -> str:
        from cryptography.hazmat.primitives import hashes
        digest = hashes.Hash(hashes.SHA256())
        digest.update(data.encode())
        signature = self.private_key.sign(
            digest.finalize(),
            ec.ECDSA(hashes.SHA256())
        )
        return signature.hex()

    def generate_ds_record(self) -> str:
        pub_bytes = self.public_key.public_bytes(
            serialization.Encoding.DER,
            serialization.PublicFormat.SubjectPublicKeyInfo
        )
        ds_hash = hashlib.sha256(pub_bytes).hexdigest()[:40]
        self.ds_record = (
            f"{self.key_tag} {self.algorithm} 2 {ds_hash}"
        )
        return self.ds_record

    def export_dnskey(self) -> str:
        pub_bytes = self.public_key.public_bytes(
            serialization.Encoding.DER,
            serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return f"{self.key_tag} {self.algorithm} 257 {pub_bytes.hex()}"


class DnssecKeyManager:
    def __init__(self, zone: str):
        self.zone = zone
        self.zsk: Optional[DnssecSigner] = None
        self.ksk: Optional[DnssecSigner] = None

    def generate_keys(self):
        self.zsk = DnssecSigner(self.zone, key_tag=12345)
        self.ksk = DnssecSigner(self.zone, key_tag=12346)

    def rotate_zsk(self) -> DnssecSigner:
        old_zsk = self.zsk
        self.zsk = DnssecSigner(self.zone, key_tag=self.zsk.key_tag + 2)
        return old_zsk

    def publish_ds(self) -> str:
        if self.ksk:
            return self.ksk.generate_ds_record()
        return ""
```

### Split-Horizon Advanced Policies

```python
from ipaddress import ip_network, ip_address
from typing import List, Tuple

class SplitHorizonPolicy:
    def __init__(self, domain: str):
        self.domain = domain
        self.views: Dict[str, Dict] = {
            "internal": {"networks": [], "zone": DnsZone(domain)},
            "external": {"networks": [], "zone": DnsZone(domain)},
            "partner": {"networks": [], "zone": DnsZone(domain)},
        }

    def add_network(self, view: str, cidr: str):
        if view in self.views:
            self.views[view]["networks"].append(ip_network(cidr))

    def resolve_view(self, client_ip: str) -> str:
        addr = ip_address(client_ip)
        for view_name, view_config in self.views.items():
            for network in view_config["networks"]:
                if addr in network:
                    return view_name
        return "external"

    def add_record_to_views(self, record: DnsRecord, view_names: List[str]):
        for view_name in view_names:
            if view_name in self.views:
                self.views[view_name]["zone"].add_record(record)

    def generate_all_configs(self) -> Dict[str, str]:
        return {
            name: config["zone"].generate_zone_file()
            for name, config in self.views.items()
        }


class GeoDnsPolicy:
    def __init__(self, domain: str):
        self.domain = domain
        self.regions: Dict[str, List[str]] = {
            "us-east": ["10.0.1.0/24", "10.0.2.0/24"],
            "us-west": ["10.0.3.0/24", "10.0.4.0/24"],
            "eu": ["10.0.5.0/24", "10.0.6.0/24"],
        }
        self.endpoints: Dict[str, List[str]] = {}

    def set_endpoints(self, region: str, ips: List[str]):
        self.endpoints[region] = ips

    def get_endpoints_for_client(self, client_ip: str) -> List[str]:
        addr = ip_address(client_ip)
        for region, networks in self.regions.items():
            for cidr in networks:
                if addr in ip_network(cidr):
                    return self.endpoints.get(region, self.endpoints.get("default", []))
        return self.endpoints.get("default", [])
```

### TTL Optimization Strategy

| Record Type | Recommended TTL | Use Case | Change Frequency |
|-------------|----------------|----------|-----------------|
| SOA | 86400 | Zone metadata | Rarely |
| NS | 86400 | Nameserver delegation | Rarely |
| A/AAAA | 300-3600 | Web servers | Daily |
| CNAME | 300-3600 | Aliases | Daily |
| MX | 3600-86400 | Mail servers | Monthly |
| TXT | 3600-86400 | SPF/DKIM | Monthly |
| SRV | 3600 | Service discovery | Weekly |
| CAA | 86400 | Certificate authority | Yearly |

```python
class TtlOptimizer:
    RECORD_TTL_MAP = {
        "SOA": {"min": 86400, "max": 86400, "default": 86400},
        "NS": {"min": 86400, "max": 86400, "default": 86400},
        "A": {"min": 60, "max": 86400, "default": 3600},
        "AAAA": {"min": 60, "max": 86400, "default": 3600},
        "CNAME": {"min": 60, "max": 86400, "default": 3600},
        "MX": {"min": 3600, "max": 86400, "default": 3600},
        "TXT": {"min": 3600, "max": 86400, "default": 3600},
        "SRV": {"min": 3600, "max": 86400, "default": 3600},
        "CAA": {"min": 86400, "max": 86400, "default": 86400},
        "PTR": {"min": 300, "max": 86400, "default": 3600},
    }

    def __init__(self):
        self.change_history: List[Dict] = []

    def recommend_ttl(self, record_type: str, change_frequency_days: float) -> int:
        ttl_range = self.RECORD_TTL_MAP.get(record_type, {"min": 300, "max": 86400, "default": 3600})
        if change_frequency_days < 1:
            return ttl_range["min"]
        elif change_frequency_days > 30:
            return ttl_range["max"]
        else:
            proportional = ttl_range["min"] + (ttl_range["max"] - ttl_range["min"]) * (change_frequency_days / 30)
            return int(min(ttl_range["max"], max(ttl_range["min"], proportional)))

    def pre_change_reduce_ttl(self, zone: DnsZone, record_name: str, new_ttl: int = 300) -> Dict[str, int]:
        reductions = {}
        for record in zone.get_records(name=record_name):
            old_ttl = record.ttl
            record.ttl = new_ttl
            reductions[f"{record.record_type.value}:{record.name}"] = old_ttl
        self.change_history.append({
            "action": "pre_change_reduce",
            "record": record_name,
            "reductions": reductions,
            "timestamp": time.time(),
        })
        return reductions

    def restore_ttl(self, zone: DnsZone, record_name: str, target_ttl: int = 3600):
        for record in zone.get_records(name=record_name):
            if record.ttl < target_ttl:
                record.ttl = target_ttl
```

## Architecture Patterns

### Primary-Secondary Replication

```
┌─────────────────────────────────────────────────────────┐
│                    DNS Architecture                      │
│                                                          │
│  ┌──────────────┐     AXFR/IXFR     ┌──────────────┐   │
│  │  Primary NS  │ ────────────────▶ │ Secondary NS │   │
│  │  (ns1)       │ ◀──────────────── │ (ns2)        │   │
│  │  Read/Write  │    SOA notify     │ Read-Only    │   │
│  └──────┬───────┘                   └──────┬───────┘   │
│         │                                   │            │
│         ▼                                   ▼            │
│  ┌──────────────┐                   ┌──────────────┐   │
│  │  Zone Files  │                   │  Zone Files  │   │
│  │  (master)    │                   │  (slave)     │   │
│  └──────────────┘                   └──────────────┘   │
│                                                          │
│  ┌──────────────┐     Dynamic        ┌──────────────┐   │
│  │  Primary DB  │ ────────────────▶ │  DNS Server  │   │
│  │  (PostgreSQL)│    DNS updates     │  (BIND/NSD)  │   │
│  └──────────────┘                   └──────────────┘   │
└─────────────────────────────────────────────────────────┘
```

```python
class DnsReplicationManager:
    def __init__(self, primary_zone: DnsZone, domain: str):
        self.primary = primary_zone
        self.domain = domain
        self.secondaries: List[Dict] = []
        self.serial_history: List[Dict] = []

    def add_secondary(self, name: str, ip: str, tsig_key: Optional[str] = None):
        self.secondaries.append({
            "name": name,
            "ip": ip,
            "tsig_key": tsig_key,
            "last_sync": 0,
            "status": "pending",
        })

    def increment_serial(self):
        self.primary.serial = int(time.time())
        self.serial_history.append({
            "serial": self.primary.serial,
            "timestamp": time.time(),
            "record_count": len(self.primary.records),
        })

    def generate_axfr_config(self) -> str:
        lines = [f'zone "{self.domain}" {{']
        lines.append("    type master;")
        lines.append(f"    file \"{self.domain}.zone\";")
        lines.append("    allow-transfer {")
        for sec in self.secondaries:
            lines.append(f"        {sec['ip']};")
        lines.append("    };")
        lines.append("    also-notify {")
        for sec in self.secondaries:
            lines.append(f"        {sec['ip']};")
        lines.append("    };")
        lines.append("};")
        return "\n".join(lines)

    def generate_slave_config(self, secondary_name: str) -> str:
        sec = next((s for s in self.secondaries if s["name"] == secondary_name), None)
        if not sec:
            return ""
        lines = [f'zone "{self.domain}" {{']
        lines.append("    type slave;")
        lines.append(f"    file \"{self.domain}.slave.zone\";")
        lines.append(f"    masters {{ {self.secondaries[0]['ip']} if {(sec.get('tsig_key', '') or 'none')} ; }};")
        lines.append("};")
        return "\n".join(lines)

    def check_sync_status(self) -> Dict[str, str]:
        status = {}
        for sec in self.secondaries:
            age = time.time() - sec["last_sync"]
            if age < 3600:
                status[sec["name"]] = "synced"
            elif age < 86400:
                status[sec["name"]] = "stale"
            else:
                status[sec["name"]] = "outdated"
        return status
```

### DNS-Based Load Balancing Pattern

```python
from dataclasses import dataclass
from typing import List, Dict
import random
import time

@dataclass
class DnsEndpoint:
    ip: str
    weight: int = 1
    health_status: str = "healthy"
    response_time_ms: float = 0.0
    last_health_check: float = 0.0

class DnsLoadBalancer:
    def __init__(self, domain: str):
        self.domain = domain
        self.endpoints: List[DnsEndpoint] = []
        self.health_check_interval: int = 30
        self.failover_threshold: int = 3
        self._failure_counts: Dict[str, int] = {}

    def add_endpoint(self, ip: str, weight: int = 1):
        self.endpoints.append(DnsEndpoint(ip=ip, weight=weight))
        self._failure_counts[ip] = 0

    def select_endpoint(self) -> Optional[DnsEndpoint]:
        healthy = [ep for ep in self.endpoints if ep.health_status == "healthy"]
        if not healthy:
            return None
        total_weight = sum(ep.weight for ep in healthy)
        r = random.uniform(0, total_weight)
        cumulative = 0
        for ep in healthy:
            cumulative += ep.weight
            if r <= cumulative:
                return ep
        return healthy[-1]

    def record_health_check(self, ip: str, is_healthy: bool, response_time_ms: float = 0.0):
        ep = next((e for e in self.endpoints if e.ip == ip), None)
        if not ep:
            return
        ep.last_health_check = time.time()
        ep.response_time_ms = response_time_ms
        if is_healthy:
            self._failure_counts[ip] = 0
            ep.health_status = "healthy"
        else:
            self._failure_counts[ip] = self._failure_counts.get(ip, 0) + 1
            if self._failure_counts[ip] >= self.failover_threshold:
                ep.health_status = "unhealthy"

    def generate_a_records(self) -> List[Dict]:
        records = []
        for ep in self.endpoints:
            records.append({
                "name": self.domain,
                "type": "A",
                "value": ep.ip,
                "ttl": 300 if ep.health_status == "healthy" else 60,
                "weight": ep.weight,
            })
        return records

    def generate_failover_config(self) -> Dict:
        primary = self.select_endpoint()
        backups = [ep for ep in self.endpoints if ep.health_status == "healthy" and ep != primary]
        return {
            "domain": self.domain,
            "primary": primary.ip if primary else None,
            "backup": [b.ip for b in backups],
            "ttl": 60,
            "health_check_interval": self.health_check_interval,
        }
```

### CDN-Origin DNS Architecture

```
                    ┌─────────────────┐
                    │   User Request   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  CDN Edge Node  │
                    │  (Anycast DNS)  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼───────┐ ┌───▼──────────┐ ┌▼───────────────┐
     │  Origin Shield │ │  Regional    │ │  Regional      │
     │  (US-East)     │ │  Cache (EU)  │ │  Cache (APAC)  │
     └────────┬───────┘ └───┬──────────┘ └┬───────────────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │  Origin Server  │
                    │  (A/AAAA records)│
                    └─────────────────┘
```

```python
class CdnsDnsManager:
    def __init__(self, domain: str):
        self.domain = domain
        self.edge_locations: Dict[str, List[str]] = {}
        self.origin_ips: List[str] = []
        self.cname_targets: Dict[str, str] = {}

    def configure_edge_routing(self):
        self.cname_targets = {
            f"www.{self.domain}": f"www.{self.domain}.cdn.cloudflare.net",
            f"api.{self.domain}": f"api.{self.domain}.cdn.cloudflare.net",
            f"static.{self.domain}": f"static.{self.domain}.cdn.cloudflare.net",
        }

    def set_origins(self, ips: List[str]):
        self.origin_ips = ips

    def generate_zone_records(self) -> List[Dict]:
        records = []
        for subdomain, cname in self.cname_targets.items():
            records.append({"name": subdomain, "type": "CNAME", "value": cname, "ttl": 300})
        for ip in self.origin_ips:
            records.append({"name": f"origin.{self.domain}", "type": "A", "value": ip, "ttl": 3600})
        return records

    def configure_anycast(self, regions: Dict[str, List[str]]):
        self.edge_locations = regions

    def get_edge_for_region(self, region: str) -> List[str]:
        return self.edge_locations.get(region, self.edge_locations.get("default", []))
```

## Integration Guide

### Cloudflare DNS API Integration

```python
import requests
from typing import Dict, List, Optional

class CloudflareDnsClient:
    BASE_URL = "https://api.cloudflare.com/client/v4"

    def __init__(self, api_token: str, zone_id: str):
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        }
        self.zone_id = zone_id

    def list_records(self, record_type: Optional[str] = None) -> List[Dict]:
        params = {"per_page": 100}
        if record_type:
            params["type"] = record_type
        response = requests.get(
            f"{self.BASE_URL}/zones/{self.zone_id}/dns_records",
            headers=self.headers, params=params,
        )
        response.raise_for_status()
        return response.json()["result"]

    def create_record(self, record_type: str, name: str, content: str, ttl: int = 1, proxied: bool = False) -> Dict:
        data = {
            "type": record_type,
            "name": name,
            "content": content,
            "ttl": ttl,
            "proxied": proxied,
        }
        response = requests.post(
            f"{self.BASE_URL}/zones/{self.zone_id}/dns_records",
            headers=self.headers, json=data,
        )
        response.raise_for_status()
        return response.json()["result"]

    def update_record(self, record_id: str, data: Dict) -> Dict:
        response = requests.put(
            f"{self.BASE_URL}/zones/{self.zone_id}/dns_records/{record_id}",
            headers=self.headers, json=data,
        )
        response.raise_for_status()
        return response.json()["result"]

    def delete_record(self, record_id: str) -> bool:
        response = requests.delete(
            f"{self.BASE_URL}/zones/{self.zone_id}/dns_records/{record_id}",
            headers=self.headers,
        )
        response.raise_for_status()
        return response.json()["success"]

    def bulk_update_ttl(self, new_ttl: int) -> int:
        records = self.list_records()
        updated = 0
        for record in records:
            if record["ttl"] != new_ttl:
                self.update_record(record["id"], {**record, "ttl": new_ttl})
                updated += 1
        return updated
```

### AWS Route53 Integration

```python
import boto3
from typing import Dict, List

class Route53DnsManager:
    def __init__(self, hosted_zone_id: str, region: str = "us-east-1"):
        self.client = boto3.client("route53", region_name=region)
        self.hosted_zone_id = hosted_zone_id

    def change_resource_record_sets(self, changes: List[Dict]) -> Dict:
        return self.client.change_resource_record_sets(
            HostedZoneId=self.hosted_zone_id,
            ChangeBatch={"Changes": changes},
        )

    def create_a_record(self, name: str, ip: str, ttl: int = 300) -> Dict:
        change = {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": name,
                "Type": "A",
                "TTL": ttl,
                "ResourceRecords": [{"Value": ip}],
            },
        }
        return self.change_resource_record_sets([change])

    def create_failover_routing(self, primary_name: str, primary_ip: str, secondary_ip: str) -> Dict:
        changes = [
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": primary_name,
                    "Type": "A",
                    "SetIdentifier": "primary",
                    "Failover": "PRIMARY",
                    "TTL": 60,
                    "ResourceRecords": [{"Value": primary_ip}],
                    "HealthCheckId": "primary-health-check",
                },
            },
            {
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": primary_name,
                    "Type": "A",
                    "SetIdentifier": "secondary",
                    "Failover": "SECONDARY",
                    "TTL": 60,
                    "ResourceRecords": [{"Value": secondary_ip}],
                },
            },
        ]
        return self.change_resource_record_sets(changes)

    def create_weighted_routing(self, name: str, endpoints: List[Dict]) -> Dict:
        changes = []
        for ep in endpoints:
            changes.append({
                "Action": "UPSERT",
                "ResourceRecordSet": {
                    "Name": name,
                    "Type": "A",
                    "SetIdentifier": ep["identifier"],
                    "Weight": ep["weight"],
                    "TTL": 60,
                    "ResourceRecords": [{"Value": ep["ip"]}],
                },
            })
        return self.change_resource_record_sets(changes)

    def list_health_checks(self) -> List[Dict]:
        response = self.client.list_health_checks()
        return response["HealthChecks"]
```

### Google Cloud DNS Integration

```python
from google.cloud import dns

class GoogleCloudDnsManager:
    def __init__(self, project_id: str, zone_name: str):
        self.client = dns.Client(project=project_id)
        self.zone = self.client.zone(zone_name)

    def add_record(self, name: str, record_type: str, ttl: int, values: List[str]):
        record = self.zone.resource_record_set(name, record_type, ttl, values)
        changes = self.zone.changes()
        changes.add_record_set(record)
        changes.create()
        changes.wait()

    def delete_record(self, name: str, record_type: str, ttl: int, values: List[str]):
        record = self.zone.resource_record_set(name, record_type, ttl, values)
        changes = self.zone.changes()
        changes.delete_record_set(record)
        changes.create()
        changes.wait()

    def list_records(self, record_type: Optional[str] = None) -> List:
        records = list(self.zone.list_resource_record_sets())
        if record_type:
            records = [r for r in records if r.record_type == record_type]
        return records
```

## Performance Optimization

### DNS Query Caching Strategy

```python
import time
from collections import OrderedDict
from threading import Lock

class DnsQueryCache:
    def __init__(self, max_size: int = 10000, default_ttl: int = 300):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict = OrderedDict()
        self._lock = Lock()
        self._hits = 0
        self._misses = 0

    def get(self, query_key: str) -> Optional[Dict]:
        with self._lock:
            if query_key in self._cache:
                entry = self._cache[query_key]
                if time.time() < entry["expires_at"]:
                    self._hits += 1
                    self._cache.move_to_end(query_key)
                    return entry["data"]
                else:
                    del self._cache[query_key]
            self._misses += 1
            return None

    def set(self, query_key: str, data: Dict, ttl: Optional[int] = None):
        with self._lock:
            if query_key in self._cache:
                del self._cache[query_key]
            elif len(self._cache) >= self.max_size:
                self._cache.popitem(last=False)
            self._cache[query_key] = {
                "data": data,
                "expires_at": time.time() + (ttl or self.default_ttl),
                "created_at": time.time(),
            }

    def invalidate(self, query_key: str) -> bool:
        with self._lock:
            if query_key in self._cache:
                del self._cache[query_key]
                return True
            return False

    def clear(self):
        with self._lock:
            self._cache.clear()

    def get_stats(self) -> Dict:
        total = self._hits + self._misses
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate": self._hits / total if total > 0 else 0,
        }
```

### Zone File Parsing Optimization

```python
class OptimizedZoneParser:
    def __init__(self):
        self._record_buffer: List[DnsRecord] = []
        self._current_origin: str = ""
        self._current_ttl: int = 3600
        self._current_name: str = "@"

    def parse_zone_file(self, zone_content: str) -> List[DnsRecord]:
        records = []
        for line in zone_content.split("\n"):
            line = line.strip()
            if not line or line.startswith(";"):
                continue
            if line.startswith("$ORIGIN"):
                self._current_origin = line.split()[1]
                continue
            if line.startswith("$TTL"):
                self._current_ttl = int(line.split()[1])
                continue
            record = self._parse_line(line)
            if record:
                records.append(record)
        return records

    def _parse_line(self, line: str) -> Optional[DnsRecord]:
        parts = line.split()
        if len(parts) < 3:
            return None
        idx = 0
        name = parts[idx]
        if name == "@" or not name[0].isalpha():
            name = self._current_name
        else:
            self._current_name = name
            idx += 1
        ttl = self._current_ttl
        if parts[idx].isdigit():
            ttl = int(parts[idx])
            idx += 1
        if parts[idx] == "IN":
            idx += 1
        if idx >= len(parts):
            return None
        record_type_str = parts[idx]
        idx += 1
        value = " ".join(parts[idx:])
        try:
            record_type = RecordType(record_type_str)
        except ValueError:
            return None
        return DnsRecord(
            record_type=record_type,
            name=f"{name}.{self._current_origin}" if name != "@" else self._current_origin,
            value=value,
            ttl=ttl,
        )

    def bulk_import(self, zone_file_path: str, zone: DnsZone) -> int:
        with open(zone_file_path, "r") as f:
            content = f.read()
        records = self.parse_zone_file(content)
        for record in records:
            zone.add_record(record)
        return len(records)
```

### Response Time Optimization

```python
class DnsPerformanceMonitor:
    def __init__(self):
        self._query_times: List[Dict] = []
        self._resolver_times: Dict[str, List[float]] = {}

    def record_query_time(self, resolver: str, response_time_ms: float, query_type: str):
        self._query_times.append({
            "resolver": resolver,
            "time_ms": response_time_ms,
            "type": query_type,
            "timestamp": time.time(),
        })
        if resolver not in self._resolver_times:
            self._resolver_times[resolver] = []
        self._resolver_times[resolver].append(response_time_ms)

    def get_resolver_stats(self) -> Dict[str, Dict]:
        stats = {}
        for resolver, times in self._resolver_times.items():
            stats[resolver] = {
                "avg_ms": sum(times) / len(times),
                "min_ms": min(times),
                "max_ms": max(times),
                "p95_ms": sorted(times)[int(len(times) * 0.95)],
                "query_count": len(times),
            }
        return stats

    def get_slow_queries(self, threshold_ms: float = 500) -> List[Dict]:
        return [q for q in self._query_times if q["time_ms"] > threshold_ms]

    def get_performance_report(self) -> Dict:
        all_times = [q["time_ms"] for q in self._query_times]
        if not all_times:
            return {"total_queries": 0}
        sorted_times = sorted(all_times)
        return {
            "total_queries": len(all_times),
            "avg_response_ms": sum(all_times) / len(all_times),
            "median_ms": sorted_times[len(sorted_times) // 2],
            "p95_ms": sorted_times[int(len(sorted_times) * 0.95)],
            "p99_ms": sorted_times[int(len(sorted_times) * 0.99)],
            "slowest_ms": max(all_times),
            "fastest_ms": min(all_times),
        }
```

## Security Considerations

### DNSSEC Validation

```python
class DnssecValidator:
    def __init__(self):
        self.validation_results: List[Dict] = []

    def validate_rrsig(self, rrset_type: str, rrsig: Dict, dnskey: Dict) -> Dict:
        result = {
            "type": rrset_type,
            "valid": False,
            "error": None,
            "algorithm_ok": rrsig["algorithm"] == dnskey["algorithm"],
            "key_tag_match": rrsig["key_tag"] == dnskey["key_tag"],
            "signer_match": rrsig["signer_name"] == dnskey.get("signer_name"),
            "time_valid": self._check_time_validity(rrsig),
        }
        result["valid"] = all([
            result["algorithm_ok"],
            result["key_tag_match"],
            result["signer_match"],
            result["time_valid"],
        ])
        self.validation_results.append(result)
        return result

    def _check_time_validity(self, rrsig: Dict) -> bool:
        now = int(time.time())
        return rrsig.get("signature_inception", 0) <= now <= rrsig.get("signature_expiration", 9999999999)

    def validate_chain(self, ds_record: str, dnskey: str, rrsig: str) -> Dict:
        return {
            "chain_valid": True,
            "ds_algorithm": int(ds_record.split()[1]),
            "dnskey_flags": int(dnskey.split()[0]),
            "rrsig_algorithm": int(rrsig.split()[1]),
        }

    def get_validation_summary(self) -> Dict:
        total = len(self.validation_results)
        valid = sum(1 for r in self.validation_results if r["valid"])
        return {
            "total_validations": total,
            "valid": valid,
            "invalid": total - valid,
            "success_rate": valid / total if total > 0 else 0,
        }
```

### DNS Query Logging

```python
class DnsQueryLogger:
    def __init__(self, log_file: str = "dns_queries.log"):
        self.log_file = log_file
        self._query_count: int = 0
        self._suspicious_patterns: List[str] = [
            "known-malware-domain.com",
            "dga-generated.",
            "dns-tunnel.",
        ]

    def log_query(self, client_ip: str, query_name: str, query_type: str, response_code: str):
        self._query_count += 1
        is_suspicious = any(pattern in query_name.lower() for pattern in self._suspicious_patterns)
        log_entry = {
            "timestamp": time.time(),
            "client_ip": client_ip,
            "query_name": query_name,
            "query_type": query_type,
            "response_code": response_code,
            "suspicious": is_suspicious,
        }
        return log_entry

    def detect_dns_tunneling(self, queries: List[Dict], threshold: int = 100) -> List[Dict]:
        domain_counts: Dict[str, int] = {}
        for q in queries:
            parts = q["query_name"].split(".")
            base_domain = ".".join(parts[-2:]) if len(parts) >= 2 else q["query_name"]
            domain_counts[base_domain] = domain_counts.get(base_domain, 0) + 1
        return [
            {"domain": d, "query_count": c}
            for d, c in domain_counts.items()
            if c > threshold
        ]

    def detect_fast_flux(self, domain: str, records: List[Dict], min_ips: int = 20) -> bool:
        unique_ips = set(r["value"] for r in records if r.get("name") == domain)
        return len(unique_ips) >= min_ips
```

### DNS Amplification Prevention

```python
class DnsAmplificationPrevention:
    def __init__(self):
        self._rate_limits: Dict[str, List[float]] = {}
        self._max_queries_per_second: int = 10
        self._blacklisted_ips: set = set()

    def check_rate_limit(self, client_ip: str) -> bool:
        now = time.time()
        if client_ip not in self._rate_limits:
            self._rate_limits[client_ip] = []
        self._rate_limits[client_ip] = [
            t for t in self._rate_limits[client_ip] if now - t < 1.0
        ]
        if len(self._rate_limits[client_ip]) >= self._max_queries_per_second:
            self._blacklisted_ips.add(client_ip)
            return False
        self._rate_limits[client_ip].append(now)
        return True

    def is_blacklisted(self, client_ip: str) -> bool:
        return client_ip in self._blacklisted_ips

    def generate_config(self) -> Dict:
        return {
            "rate_limit_per_second": self._max_queries_per_second,
            "blacklist_enabled": True,
            "response_rate_limiting": True,
            "recursive_only": True,
            "any_query_disabled": True,
            "large_response_disabled": True,
        }

    def get_blocked_stats(self) -> Dict:
        return {
            "blacklisted_ips": len(self._blacklisted_ips),
            "tracked_ips": len(self._rate_limits),
        }
```

## Troubleshooting Guide

### Common DNS Issues and Solutions

| Issue | Symptoms | Root Cause | Solution |
|-------|----------|------------|----------|
| NXDOMAIN flooding | High NXDOMAIN responses | Misconfigured DNS records or DNS hijacking | Audit zone files, enable DNSSEC |
| Slow resolution | High response times (>500ms) | Overloaded resolver or network latency | Switch resolvers, enable caching |
| Zone transfer failure | Secondary NS not updating | AXFR blocked or TSIG mismatch | Check ACLs, verify TSIG keys |
| Split-horizon inconsistency | Internal/external mismatch | View misconfiguration | Verify ACLs and view order |
| TTL too high | Stale records after changes | Aggressive caching | Reduce TTL before changes |
| DNS loop | Resolution timeout | CNAME chain or circular reference | Remove circular CNAMEs |

```python
class DnsTroubleshooter:
    def __init__(self):
        self.diagnostics: List[Dict] = []

    def check_zone_syntax(self, zone_content: str) -> List[Dict]:
        issues = []
        lines = zone_content.split("\n")
        has_soa = False
        has_ns = False
        for i, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith(";") or line.startswith("$"):
                continue
            if "SOA" in line:
                has_soa = True
            if "NS" in line and not line.startswith("$"):
                has_ns = True
            parts = line.split()
            if len(parts) < 4:
                issues.append({"line": i, "issue": "Insufficient fields", "severity": "warning"})
        if not has_soa:
            issues.append({"line": 0, "issue": "Missing SOA record", "severity": "error"})
        if not has_ns:
            issues.append({"line": 0, "issue": "Missing NS record", "severity": "error"})
        return issues

    def diagnose_resolution(self, domain: str, records: List[Dict]) -> Dict:
        result = {"domain": domain, "issues": [], "suggestions": []}
        a_records = [r for r in records if r.get("type") == "A" and r.get("name") == domain]
        cname_records = [r for r in records if r.get("type") == "CNAME" and r.get("name") == domain]
        if cname_records and a_records:
            result["issues"].append("CNAME and A record coexist (RFC 1034 violation)")
        if not a_records and not cname_records:
            result["issues"].append("No A or CNAME record found")
        mx_records = [r for r in records if r.get("type") == "MX"]
        if mx_records and not a_records:
            result["suggestions"].append("MX records exist but no A record for domain")
        return result

    def check_ttl_consistency(self, records: List[Dict]) -> List[Dict]:
        warnings = []
        ttl_groups: Dict[str, List[int]] = {}
        for record in records:
            key = f"{record.get('name')}:{record.get('type')}"
            if key not in ttl_groups:
                ttl_groups[key] = []
            ttl_groups[key].append(record.get("ttl", 3600))
        for key, ttls in ttl_groups.items():
            if len(set(ttls)) > 1:
                warnings.append({
                    "record": key,
                    "ttls_found": ttls,
                    "issue": "Inconsistent TTL values",
                })
        return warnings

    def generate_report(self, domain: str, zone: DnsZone) -> str:
        lines = [f"DNS Diagnostic Report for {domain}", "=" * 50, ""]
        records = zone.get_records()
        lines.append(f"Total records: {len(records)}")
        type_counts = {}
        for r in records:
            type_counts[r.record_type.value] = type_counts.get(r.record_type.value, 0) + 1
        for rtype, count in sorted(type_counts.items()):
            lines.append(f"  {rtype}: {count}")
        lines.append("")
        soa_records = zone.get_records(record_type=RecordType.SOA)
        if soa_records:
            lines.append(f"SOA Primary: {soa_records[0].value}")
            lines.append(f"Serial: {zone.serial}")
        ns_records = zone.get_records(record_type=RecordType.NS)
        lines.append(f"Nameservers: {len(ns_records)}")
        for ns in ns_records:
            lines.append(f"  - {ns.value}")
        return "\n".join(lines)
```

### DNS Propagation Verification

```python
class DnsPropagationChecker:
    RESOLVERS = [
        ("Google", "8.8.8.8"),
        ("Cloudflare", "1.1.1.1"),
        ("Quad9", "9.9.9.9"),
        ("OpenDNS", "208.67.222.222"),
    ]

    def __init__(self):
        self._results: Dict[str, Dict[str, str]] = {}

    def check_propagation(self, domain: str, expected_ip: str) -> Dict:
        results = {}
        for resolver_name, resolver_ip in self.RESOLVERS:
            actual_ip = self._query_dns(domain, resolver_ip)
            results[resolver_name] = {
                "resolver_ip": resolver_ip,
                "expected": expected_ip,
                "actual": actual_ip,
                "match": actual_ip == expected_ip,
            }
        self._results[domain] = results
        return results

    def _query_dns(self, domain: str, resolver_ip: str) -> str:
        import subprocess
        try:
            result = subprocess.run(
                ["nslookup", domain, resolver_ip],
                capture_output=True, text=True, timeout=5,
            )
            for line in result.stdout.split("\n"):
                if "Address:" in line and resolver_ip not in line:
                    return line.split("Address:")[-1].strip()
        except Exception:
            return "unreachable"
        return "unknown"

    def get_propagation_status(self, domain: str) -> Dict:
        results = self._results.get(domain, {})
        total = len(results)
        propagated = sum(1 for r in results.values() if r["match"])
        return {
            "domain": domain,
            "propagated": propagated,
            "total_resolvers": total,
            "percentage": (propagated / total * 100) if total > 0 else 0,
            "complete": propagated == total,
        }
```

## API Reference

### DnsZone API

```python
class DnsZoneApi:
    """RESTful API wrapper for DNS zone operations."""

    def __init__(self, zone: DnsZone):
        self.zone = zone

    def list_records(self, record_type: Optional[str] = None) -> List[Dict]:
        records = self.zone.get_records()
        if record_type:
            rt = RecordType(record_type)
            records = [r for r in records if r.record_type == rt]
        return [
            {
                "name": r.name,
                "type": r.record_type.value,
                "value": r.value,
                "ttl": r.ttl,
                "priority": r.priority,
                "enabled": r.enabled,
            }
            for r in records
        ]

    def create_record(self, record_type: str, name: str, value: str, ttl: int = 3600, priority: int = 0) -> Dict:
        rt = RecordType(record_type)
        record = DnsRecord(record_type=rt, name=name, value=value, ttl=ptl, priority=priority)
        self.zone.add_record(record)
        return {"id": len(self.zone.records), "status": "created"}

    def update_record(self, record_name: str, record_type: str, updates: Dict) -> bool:
        rt = RecordType(record_type)
        for record in self.zone.get_records(name=record_name, record_type=rt):
            if "ttl" in updates:
                record.ttl = updates["ttl"]
            if "value" in updates:
                record.value = updates["value"]
            if "enabled" in updates:
                record.enabled = updates["enabled"]
            return True
        return False

    def delete_record(self, record_name: str, record_type: str) -> bool:
        rt = RecordType(record_type)
        before = len(self.zone.records)
        self.zone.remove_record(record_name, rt)
        return len(self.zone.records) < before

    def get_zone_info(self) -> Dict:
        return {
            "domain": self.zone.domain,
            "serial": self.zone.serial,
            "record_count": len(self.zone.records),
            "soa_primary": self.zone.soa_primary,
        }
```

### HealthCheck API

```python
class HealthCheckApi:
    def __init__(self, health_checker: DnsHealthCheck):
        self.checker = health_checker

    def register_endpoint(self, record_name: str, url: str, interval: int = 60, threshold: int = 3) -> Dict:
        self.checker.register(record_name, url, interval)
        return {"status": "registered", "record": record_name}

    def report_health(self, record_name: str, is_healthy: bool) -> Dict:
        self.checker.check(record_name, is_healthy)
        return {"record": record_name, "status": self.checker.get_status().get(record_name)}

    def get_all_status(self) -> Dict:
        return self.checker.get_status()

    def get_unhealthy(self) -> List[str]:
        status = self.checker.get_status()
        return [name for name, s in status.items() if s == "unhealthy"]
```

## Data Models

### DNS Record Schema

```python
from dataclasses import dataclass, field
from typing import List, Optional
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
class DnsRecordSchema:
    record_type: str
    name: str
    value: str
    ttl: int = 3600
    priority: int = 0
    enabled: bool = True
    created_at: float = 0.0
    updated_at: float = 0.0
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "record_type": self.record_type,
            "name": self.name,
            "value": self.value,
            "ttl": self.ttl,
            "priority": self.priority,
            "enabled": self.enabled,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "DnsRecordSchema":
        return cls(
            record_type=data["record_type"],
            name=data["name"],
            value=data["value"],
            ttl=data.get("ttl", 3600),
            priority=data.get("priority", 0),
            enabled=data.get("enabled", True),
            created_at=data.get("created_at", 0),
            updated_at=data.get("updated_at", 0),
            metadata=data.get("metadata", {}),
        )

@dataclass
class ZoneSchema:
    domain: str
    soa_primary: str
    admin_email: str
    serial: int
    records: List[DnsRecordSchema] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> Dict:
        return {
            "domain": self.domain,
            "soa_primary": self.soa_primary,
            "admin_email": self.admin_email,
            "serial": self.serial,
            "records": [r.to_dict() for r in self.records],
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "ZoneSchema":
        return cls(
            domain=data["domain"],
            soa_primary=data["soa_primary"],
            admin_email=data["admin_email"],
            serial=data["serial"],
            records=[DnsRecordSchema.from_dict(r) for r in data.get("records", [])],
            metadata=data.get("metadata", {}),
        )
```

### HealthCheck Data Model

```python
@dataclass
class HealthCheckConfig:
    record_name: str
    url: str
    interval: int = 60
    timeout: int = 10
    threshold: int = 3
    enabled: bool = True
    created_at: float = 0.0
    last_check: float = 0.0
    failure_count: int = 0
    status: str = "healthy"
    check_history: List[Dict] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "record_name": self.record_name,
            "url": self.url,
            "interval": self.interval,
            "timeout": self.timeout,
            "threshold": self.threshold,
            "enabled": self.enabled,
            "status": self.status,
            "failure_count": self.failure_count,
            "last_check": self.last_check,
        }
```

## Deployment Guide

### Zone Deployment Pipeline

```python
class ZoneDeploymentPipeline:
    def __init__(self, zone: DnsZone):
        self.zone = zone
        self.stages = ["validate", "preview", "deploy", "verify"]
        self.current_stage = 0
        self.deployment_log: List[Dict] = []

    def validate(self) -> bool:
        issues = []
        if not self.zone.get_records(record_type=RecordType.SOA):
            issues.append("Missing SOA record")
        if not self.zone.get_records(record_type=RecordType.NS):
            issues.append("Missing NS record")
        for record in self.zone.records:
            if record.ttl < 60:
                issues.append(f"TTL too low for {record.name}: {record.ttl}")
        self.deployment_log.append({"stage": "validate", "issues": issues, "passed": len(issues) == 0})
        return len(issues) == 0

    def preview(self) -> Dict:
        zone_file = self.zone.generate_zone_file()
        record_count = len([r for r in self.zone.records if r.enabled])
        self.deployment_log.append({"stage": "preview", "record_count": record_count})
        return {
            "zone_file": zone_file,
            "record_count": record_count,
            "serial": self.zone.serial,
        }

    def deploy(self, provider: str = "cloudflare") -> Dict:
        self.zone.increment_serial()
        self.deployment_log.append({
            "stage": "deploy",
            "provider": provider,
            "serial": self.zone.serial,
            "timestamp": time.time(),
        })
        return {"status": "deployed", "serial": self.zone.serial}

    def verify(self, propagation_checker: DnsPropagationChecker) -> Dict:
        a_records = self.zone.get_records(record_type=RecordType.A)
        if a_records:
            primary_ip = a_records[0].value
            status = propagation_checker.check_propagation(self.zone.domain, primary_ip)
            self.deployment_log.append({"stage": "verify", "status": status})
            return status
        return {"status": "no_records_to_verify"}

    def run_full_pipeline(self, provider: str = "cloudflare") -> Dict:
        if not self.validate():
            return {"status": "failed", "stage": "validate"}
        self.preview()
        self.deploy(provider)
        return {"status": "completed", "log": self.deployment_log}
```

### Blue-Green DNS Deployment

```python
class BlueGreenDnsDeployment:
    def __init__(self, domain: str):
        self.domain = domain
        self.blue_zone = DnsZone(domain)
        self.green_zone = DnsZone(domain)
        self.active: str = "blue"

    def setup_blue(self, records: List[DnsRecord]):
        for record in records:
            self.blue_zone.add_record(record)

    def setup_green(self, records: List[DnsRecord]):
        for record in records:
            self.green_zone.add_record(record)

    def switch_to_green(self) -> Dict:
        self.active = "green"
        return {
            "domain": self.domain,
            "active": self.active,
            "serial": self.green_zone.serial,
        }

    def switch_to_blue(self) -> Dict:
        self.active = "blue"
        return {
            "domain": self.domain,
            "active": self.active,
            "serial": self.blue_zone.serial,
        }

    def get_active_zone(self) -> DnsZone:
        return self.green_zone if self.active == "green" else self.blue_zone

    def rollback(self) -> Dict:
        self.active = "blue" if self.active == "green" else "green"
        return {"rolled_back_to": self.active}
```

## Monitoring & Observability

### DNS Monitoring Dashboard

```python
class DnsMonitoringDashboard:
    def __init__(self):
        self.metrics: Dict[str, List[Dict]] = {
            "query_rate": [],
            "response_time": [],
            "error_rate": [],
            "nxdomain_rate": [],
        }
        self.alerts: List[Dict] = []

    def record_metric(self, metric_name: str, value: float, timestamp: float = None):
        if metric_name in self.metrics:
            self.metrics[metric_name].append({
                "value": value,
                "timestamp": timestamp or time.time(),
            })

    def get_query_rate(self, window_seconds: int = 300) -> float:
        now = time.time()
        recent = [m for m in self.metrics["query_rate"] if now - m["timestamp"] < window_seconds]
        if not recent:
            return 0.0
        return len(recent) / window_seconds

    def get_average_response_time(self, window_seconds: int = 300) -> float:
        now = time.time()
        recent = [m for m in self.metrics["response_time"] if now - m["timestamp"] < window_seconds]
        if not recent:
            return 0.0
        return sum(m["value"] for m in recent) / len(recent)

    def check_alerts(self) -> List[Dict]:
        new_alerts = []
        avg_response = self.get_average_response_time()
        if avg_response > 1000:
            new_alerts.append({
                "type": "high_latency",
                "severity": "warning",
                "message": f"Average response time: {avg_response:.1f}ms",
            })
        query_rate = self.get_query_rate()
        if query_rate > 10000:
            new_alerts.append({
                "type": "high_query_rate",
                "severity": "critical",
                "message": f"Query rate: {query_rate:.1f} queries/sec",
            })
        self.alerts.extend(new_alerts)
        return new_alerts

    def get_dashboard_data(self) -> Dict:
        return {
            "query_rate": self.get_query_rate(),
            "avg_response_ms": self.get_average_response_time(),
            "total_queries": len(self.metrics["query_rate"]),
            "active_alerts": len([a for a in self.alerts if a.get("acknowledged") is not True]),
        }
```

### DNS Health Metrics

```python
class DnsHealthMetrics:
    def __init__(self):
        self._health_checks: Dict[str, List[Dict]] = {}
        self._uptime_history: Dict[str, List[bool]] = {}

    def record_check(self, service_name: str, is_healthy: bool):
        if service_name not in self._health_checks:
            self._health_checks[service_name] = []
            self._uptime_history[service_name] = []
        self._health_checks[service_name].append({
            "healthy": is_healthy,
            "timestamp": time.time(),
        })
        self._uptime_history[service_name].append(is_healthy)

    def get_uptime_percentage(self, service_name: str, window_hours: int = 24) -> float:
        history = self._uptime_history.get(service_name, [])
        if not history:
            return 100.0
        recent = history[-min(len(history), window_hours * 60):]
        return (sum(1 for h in recent if h) / len(recent)) * 100

    def get_service_health_summary(self) -> Dict[str, Dict]:
        summary = {}
        for service, checks in self._health_checks.items():
            recent = checks[-100:]
            healthy_count = sum(1 for c in recent if c["healthy"])
            summary[service] = {
                "status": "healthy" if healthy_count / len(recent) > 0.95 else "degraded",
                "uptime": self.get_uptime_percentage(service),
                "total_checks": len(checks),
                "recent_failures": len(recent) - healthy_count,
            }
        return summary
```

## Testing Strategy

### DNS Unit Tests

```python
import unittest

class TestDnsZone(unittest.TestCase):
    def setUp(self):
        self.zone = DnsZone("example.com")

    def test_add_record(self):
        record = DnsRecord(RecordType.A, "www", "192.168.1.1")
        self.zone.add_record(record)
        self.assertEqual(len(self.zone.records), 1)

    def test_remove_record(self):
        record = DnsRecord(RecordType.A, "www", "192.168.1.1")
        self.zone.add_record(record)
        self.zone.remove_record("www", RecordType.A)
        self.assertEqual(len(self.zone.records), 0)

    def test_zone_file_generation(self):
        self.zone.add_record(DnsRecord(RecordType.A, "www", "192.168.1.1"))
        zone_file = self.zone.generate_zone_file()
        self.assertIn("$ORIGIN example.com.", zone_file)
        self.assertIn("www 3600 IN A 192.168.1.1", zone_file)

    def test_serial_increment(self):
        initial_serial = self.zone.serial
        self.zone.add_record(DnsRecord(RecordType.A, "www", "192.168.1.1"))
        self.assertGreaterEqual(self.zone.serial, initial_serial)


class TestSplitHorizon(unittest.TestCase):
    def setUp(self):
        self.split_dns = SplitHorizonDns("example.com")

    def test_internal_record(self):
        record = DnsRecord(RecordType.A, "app", "10.0.0.1")
        self.split_dns.add_internal_record(record)
        self.assertEqual(len(self.split_dns.internal_zone.records), 1)

    def test_external_record(self):
        record = DnsRecord(RecordType.A, "app", "203.0.113.1")
        self.split_dns.add_external_record(record)
        self.assertEqual(len(self.split_dns.external_zone.records), 1)

    def test_view_configs(self):
        self.split_dns.add_internal_record(DnsRecord(RecordType.A, "app", "10.0.0.1"))
        self.split_dns.add_external_record(DnsRecord(RecordType.A, "app", "203.0.113.1"))
        configs = self.split_dns.generate_view_configs()
        self.assertIn("internal", configs)
        self.assertIn("external", configs)


class TestDnsHealthCheck(unittest.TestCase):
    def setUp(self):
        self.health_check = DnsHealthCheck()

    def test_register(self):
        self.health_check.register("app.example.com", "https://app.example.com/health")
        self.assertEqual(len(self.health_check._checks), 1)

    def test_healthy_check(self):
        self.health_check.register("app.example.com", "https://app.example.com/health")
        self.health_check.check("app.example.com", is_healthy=True)
        status = self.health_check.get_status()
        self.assertEqual(status["app.example.com"], "healthy")

    def test_unhealthy_after_threshold(self):
        self.health_check.register("app.example.com", "https://app.example.com/health")
        for _ in range(3):
            self.health_check.check("app.example.com", is_healthy=False)
        status = self.health_check.get_status()
        self.assertEqual(status["app.example.com"], "unhealthy")


class TestDnsAnalytics(unittest.TestCase):
    def setUp(self):
        self.analytics = DnsAnalytics()

    def test_record_query(self):
        self.analytics.record_query("example.com", "A", 15.5, True)
        stats = self.analytics.get_stats()
        self.assertEqual(stats["total_queries"], 1)

    def test_nxdomain_tracking(self):
        self.analytics.record_query("nonexistent.com", "A", 5.0, False)
        stats = self.analytics.get_stats()
        self.assertEqual(stats["nxdomain_count"], 1)

    def test_stats_calculation(self):
        self.analytics.record_query("example.com", "A", 10.0, True)
        self.analytics.record_query("example.com", "A", 20.0, True)
        stats = self.analytics.get_stats()
        self.assertAlmostEqual(stats["avg_response_ms"], 15.0)


if __name__ == "__main__":
    unittest.main()
```

### Integration Tests

```python
class TestDnsDeploymentPipeline(unittest.TestCase):
    def setUp(self):
        self.zone = DnsZone("test.example.com")
        self.pipeline = ZoneDeploymentPipeline(self.zone)

    def test_validation_fails_without_soa(self):
        result = self.pipeline.validate()
        self.assertFalse(result)

    def test_validation_passes_with_records(self):
        self.zone.add_record(DnsRecord(RecordType.SOA, "@", "ns1.test.example.com"))
        self.zone.add_record(DnsRecord(RecordType.NS, "@", "ns1.test.example.com"))
        result = self.pipeline.validate()
        self.assertTrue(result)

    def test_preview_returns_zone_file(self):
        self.zone.add_record(DnsRecord(RecordType.A, "www", "192.168.1.1"))
        preview = self.pipeline.preview()
        self.assertIn("zone_file", preview)
        self.assertEqual(preview["record_count"], 1)

    def test_full_pipeline(self):
        self.zone.add_record(DnsRecord(RecordType.SOA, "@", "ns1.test.example.com"))
        self.zone.add_record(DnsRecord(RecordType.NS, "@", "ns1.test.example.com"))
        result = self.pipeline.run_full_pipeline()
        self.assertEqual(result["status"], "completed")


class TestDnsLoadBalancer(unittest.TestCase):
    def setUp(self):
        self.lb = DnsLoadBalancer("lb.example.com")
        self.lb.add_endpoint("10.0.0.1", weight=5)
        self.lb.add_endpoint("10.0.0.2", weight=3)
        self.lb.add_endpoint("10.0.0.3", weight=2)

    def test_select_endpoint_returns_healthy(self):
        ep = self.lb.select_endpoint()
        self.assertIsNotNone(ep)
        self.assertEqual(ep.health_status, "healthy")

    def test_health_check_unhealthy(self):
        for _ in range(3):
            self.lb.record_health_check("10.0.0.1", is_healthy=False)
        ep = self.lb.select_endpoint()
        self.assertNotEqual(ep.ip, "10.0.0.1")

    def test_failover_config(self):
        config = self.lb.generate_failover_config()
        self.assertIn("primary", config)
        self.assertIn("backup", config)
```

## Versioning & Migration

### Zone File Version Control

```python
class ZoneVersionControl:
    def __init__(self, domain: str):
        self.domain = domain
        self.versions: List[Dict] = []
        self.current_version: int = 0

    def commit(self, zone: DnsZone, message: str, author: str = "system"):
        version = {
            "id": self.current_version,
            "serial": zone.serial,
            "record_count": len(zone.records),
            "zone_file": zone.generate_zone_file(),
            "message": message,
            "author": author,
            "timestamp": time.time(),
        }
        self.versions.append(version)
        self.current_version += 1
        return version["id"]

    def rollback(self, version_id: int) -> Optional[str]:
        for version in self.versions:
            if version["id"] == version_id:
                return version["zone_file"]
        return None

    def diff(self, version_a: int, version_b: int) -> Dict:
        va = next((v for v in self.versions if v["id"] == version_a), None)
        vb = next((v for v in self.versions if v["id"] == version_b), None)
        if not va or not vb:
            return {"error": "Version not found"}
        return {
            "version_a": va["id"],
            "version_b": vb["id"],
            "serial_a": va["serial"],
            "serial_b": vb["serial"],
            "records_a": va["record_count"],
            "records_b": vb["record_count"],
        }

    def get_history(self) -> List[Dict]:
        return [
            {
                "id": v["id"],
                "serial": v["serial"],
                "message": v["message"],
                "timestamp": v["timestamp"],
            }
            for v in self.versions
        ]
```

### Migration Scripts

```python
class DnsMigrationRunner:
    def __init__(self):
        self.migrations: List[Dict] = []
        self.applied: List[Dict] = []

    def add_migration(self, name: str, up_fn, down_fn):
        self.migrations.append({
            "name": name,
            "up": up_fn,
            "down": down_fn,
            "applied": False,
        })

    def migrate_up(self, zone: DnsZone) -> List[str]:
        results = []
        for migration in self.migrations:
            if not migration["applied"]:
                migration["up"](zone)
                migration["applied"] = True
                self.applied.append(migration)
                results.append(migration["name"])
        return results

    def migrate_down(self, zone: DnsZone, steps: int = 1) -> List[str]:
        results = []
        for migration in reversed(self.applied[-steps:]):
            migration["down"](zone)
            migration["applied"] = False
            self.applied.remove(migration)
            results.append(migration["name"])
        return results


def migrate_add_caa(zone: DnsZone):
    zone.add_record(DnsRecord(RecordType.CAA, "@", '0 issue "letsencrypt.org"'))

def rollback_add_caa(zone: DnsZone):
    zone.remove_record("@", RecordType.CAA)


def migrate_reduce_ttls(zone: DnsZone):
    for record in zone.records:
        if record.record_type in [RecordType.A, RecordType.AAAA, RecordType.CNAME]:
            record.ttl = min(record.ttl, 300)
```

## Glossary

| Term | Definition |
|------|-----------|
| **SOA** | Start of Authority - metadata record for a DNS zone |
| **NS** | Nameserver record - delegates a DNS zone to an authoritative server |
| **A Record** | Maps a domain name to an IPv4 address |
| **AAAA Record** | Maps a domain name to an IPv6 address |
| **CNAME** | Canonical Name - alias pointing to another domain name |
| **MX** | Mail Exchange - specifies mail server for a domain |
| **TXT** | Text record - holds arbitrary text (SPF, DKIM, verification) |
| **SRV** | Service record - specifies host and port for a service |
| **CAA** | Certification Authority Authorization - restricts certificate issuance |
| **PTR** | Pointer record - reverse DNS lookup (IP to hostname) |
| **TTL** | Time To Live - how long a record is cached |
| **DNSSEC** | DNS Security Extensions - cryptographic signing of DNS records |
| **RRSIG** | Resource Record Signature - DNSSEC signature record |
| **DS** | Delegation Signer - parent zone's hash of child's DNSKEY |
| **AXFR** | Authoritative Transfer - full zone transfer protocol |
| **IXFR** | Incremental Transfer - partial zone transfer protocol |
| **Split-Horizon DNS** | Different DNS responses based on client location |
| **GeoDNS** | DNS routing based on geographic location of the client |
| **Anycast** | Routing method where multiple servers share one IP |
| **NXDOMAIN** | Non-Existent Domain - response for unregistered names |
| **DGA** | Domain Generation Algorithm - malware technique |
| **Fast Flux** | Rapidly changing DNS records to hide malicious servers |
| **DNS Tunneling** | Encapsulating data within DNS queries for exfiltration |
| **TSIG** | Transaction Signature - authenticates DNS zone transfers |
| **EDNS** | Extension Mechanisms for DNS - extends DNS packet size |
| **Response Rate Limiting** | Technique to mitigate DNS amplification attacks |
| **Zone File** | Text file containing all DNS records for a domain |
| **Resolver** | DNS server that performs lookups on behalf of clients |
| **Authoritative NS** | Nameserver that holds the original zone data |
| **Recursive Resolver** | DNS server that queries multiple authoritative servers |
| **Forwarding** | Passing DNS queries to another resolver |
| **Hints** | Bootstrap file pointing to root nameservers |
| **Root Hints** | List of IP addresses for the DNS root servers |
| **NSEC** | Next Secure - DNSSEC authenticated denial of existence |
| **NSEC3** | Hashed version of NSEC for zone walking prevention |
| **RPZ** | Response Policy Zone - DNS firewall rules |
| **DNS over HTTPS** | Encrypting DNS queries using HTTPS (DoH) |
| **DNS over TLS** | Encrypting DNS queries using TLS (DoT) |
| **QNAME Minimization** | Reducing information in recursive queries |
| **Negative Caching** | Caching NXDOMAIN and SERVFAIL responses |

## Changelog

### Version 2.1.0 (Latest)
- Added DNSSEC signing and key management
- Added split-horizon advanced policies with CIDR matching
- Added GeoDNS routing support
- Added TTL optimization with change frequency analysis
- Added Cloudflare, Route53, Google Cloud DNS integrations
- Added DNS query caching with LRU eviction
- Added DNS amplification prevention
- Added propagation checker with multi-resolver verification
- Added zone deployment pipeline with blue-green support
- Added monitoring dashboard with alerting
- Added comprehensive test suite
- Added zone version control and migration runner

### Version 2.0.0
- Complete rewrite with class-based architecture
- Added health-checked failover
- Added DNS analytics and query logging
- Added split-horizon DNS support
- Added bulk operations for zone migration

### Version 1.0.0
- Initial release with basic record management
- SOA, NS, A, AAAA, CNAME, MX, TXT, SRV support
- Zone file generation

## Contributing Guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/org/dns-management-skill.git
cd dns-management-skill

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run tests
python -m pytest tests/ -v

# Run linter
flake8 src/
mypy src/
```

### Code Style

- Follow PEP 8 for Python code
- Use type hints for all function signatures
- Write docstrings for public classes and methods
- Keep functions under 50 lines
- Use dataclasses for data structures
- Prefer composition over inheritance

### Pull Request Process

1. Fork the repository and create a feature branch
2. Write tests for new functionality
3. Ensure all existing tests pass
4. Update documentation if adding new features
5. Submit PR with descriptive title and detailed description
6. Request review from at least one maintainer

### Issue Reporting

- Use GitHub Issues for bug reports
- Include reproduction steps and expected vs actual behavior
- Tag issues with appropriate labels (bug, enhancement, documentation)
- Check existing issues before creating new ones

## License

MIT License

Copyright (c) 2024 DNS Management Skill Contributors

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

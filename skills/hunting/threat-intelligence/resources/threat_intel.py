"""
Threat Intelligence Module
Advanced threat intelligence collection and analysis
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json


class ThreatSeverity(Enum):
    CRITICAL = 5
    HIGH = 4
    MEDIUM = 3
    LOW = 2
    INFO = 1


@dataclass
class Indicator:
    ioc_type: str
    value: str
    severity: ThreatSeverity
    source: str
    first_seen: datetime
    tags: List[str]
    context: Dict


class ThreatIntelligence:
    """Threat intelligence management"""
    
    def __init__(self):
        self.ioc_database = {}
        self.threat_actors = {}
        self.campaigns = {}
        self.ttps_matrix = {}
    
    def collect_from_feed(self, feed_url: str) -> List[Indicator]:
        """Collect IOCs from threat feed"""
        indicators = []
        
        sample_iocs = [
            {'type': 'domain', 'value': 'evil.com', 'severity': 4, 'tags': ['apt', 'c2']},
            {'type': 'ip', 'value': '192.168.1.100', 'severity': 4, 'tags': ['c2']},
            {'type': 'hash', 'value': 'md5:abc123', 'severity': 3, 'tags': ['malware']},
            {'type': 'url', 'value': 'http://evil.com/payload.exe', 'severity': 5, 'tags': ['dropper']}
        ]
        
        for ioc in sample_iocs:
            indicator = Indicator(
                ioc_type=ioc['type'],
                value=ioc['value'],
                severity=ThreatSeverity(ioc['severity']),
                source=feed_url,
                first_seen=datetime.now(),
                tags=ioc['tags'],
                context={}
            )
            indicators.append(indicator)
            self.ioc_database[ioc['value']] = indicator
        
        return indicators
    
    def enrich_indicators(self, indicators: List[Indicator]) -> List[Dict]:
        """Enrich IOCs with additional context"""
        enriched = []
        
        for indicator in indicators:
            enrichment = {
                'indicator': indicator.value,
                'type': indicator.ioc_type,
                'severity': indicator.severity.name,
                'first_seen': indicator.first_seen.isoformat(),
                'tags': indicator.tags,
                'context': self._get_context(indicator)
            }
            enriched.append(enrichment)
        
        return enriched
    
    def _get_context(self, indicator: Indicator) -> Dict:
        """Get additional context for indicator"""
        context_map = {
            'evil.com': {'threat_actor': 'APT29', 'campaign': 'Grizzly第二步'},
            '192.168.1.100': {'threat_actor': 'APT41', 'uses': ['c2', 'exfiltration']}
        }
        return context_map.get(indicator.value, {})
    
    def map_to_attack(self, enriched_indicators: List[Dict]) -> List[Dict]:
        """Map indicators to MITRE ATT&CK TTPs"""
        ttp_mapping = {
            'powershell': ['T1059.001'],
            'certutil': ['T1140'],
            'schtasks': ['T1053.005'],
            'wmic': ['T1047'],
            'psexec': ['T1021.002'],
            ' registry': ['T1547.001']
        }
        
        mapped = []
        for ind in enriched_indicators:
            ttps = []
            value_lower = ind['indicator'].lower()
            for pattern, ttp_list in ttp_mapping.items():
                if pattern in value_lower:
                    ttps.extend(ttp_list)
            
            mapped.append({
                'indicator': ind['indicator'],
                'ttps': list(set(ttps)),
                'confidence': 'high' if len(ttps) > 0 else 'low'
            })
        
        return mapped
    
    def add_threat_actor(self, 
                        name: str,
                        aliases: List[str],
                        ttps: List[str],
                        campaigns: List[str]):
        """Add threat actor to database"""
        self.threat_actors[name] = {
            'aliases': aliases,
            'ttps': ttps,
            'campaigns': campaigns,
            'first_observed': datetime.now(),
            'target_sectors': []
        }
    
    def get_actor_profile(self, actor_name: str) -> Optional[Dict]:
        """Get threat actor profile"""
        if actor_name not in self.threat_actors:
            return None
        
        actor = self.threat_actors[actor_name]
        return {
            'name': actor_name,
            'aliases': actor['aliases'],
            'ttps': actor['ttps'],
            'campaigns': actor['campaigns'],
            'first_observed': actor['first_observed'].isoformat()
        }


class IOCDatabase:
    """IOC database management"""
    
    def __init__(self):
        self.database = {}
    
    def add_ioc(self, 
                ioc_type: str,
                value: str,
                severity: ThreatSeverity,
                source: str,
                tags: Optional[List[str]] = None):
        """Add IOC to database"""
        self.database[f"{ioc_type}:{value}"] = {
            'type': ioc_type,
            'value': value,
            'severity': severity,
            'source': source,
            'tags': tags or [],
            'added': datetime.now()
        }
    
    def lookup(self, ioc_type: str, value: str) -> Optional[Dict]:
        """Look up IOC in database"""
        return self.database.get(f"{ioc_type}:{value}")
    
    def search_by_tag(self, tag: str) -> List[Dict]:
        """Search IOCs by tag"""
        results = []
        for key, ioc in self.database.items():
            if tag in ioc.get('tags', []):
                results.append(ioc)
        return results
    
    def export_yara(self) -> str:
        """Export IOCs as YARA rules"""
        yara = "rule threat_intel_iocs\n{\n    meta:\n        description = \"Generated from IOC database\"\n\n    strings:\n"
        
        for ioc in list(self.database.values())[:50]:
            yara += f'        $s{list(self.database.keys()).index(ioc["value"])} = "{ioc["value"]}"\n'
        
        yara += "    condition:\n        any of them\n}"
        
        return yara


if __name__ == "__main__":
    intel = ThreatIntelligence()
    
    indicators = intel.collect_from_feed("https://feed.example.com")
    enriched = intel.enrich_indicators(indicators)
    mapped = intel.map_to_attack(enriched)
    
    print(f"Collected {len(indicators)} IOCs")
    print(f"Enriched: {json.dumps(enriched, indent=2)}")
    print(f"Mapped to TTPs: {json.dumps(mapped, indent=2)}")
    
    db = IOCDatabase()
    for ind in indicators:
        db.add_ioc(ind.ioc_type, ind.value, ind.severity, ind.source, ind.tags)
    
    yara = db.export_yara()
    print(f"YARA rules generated ({len(yara)} chars)")

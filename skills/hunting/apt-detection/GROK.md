---
name: "apt-detection"
category: "hunting"
version: "2.0.0"
tags: ["hunting", "apt", "advanced-persistent-threats", "detection", "attribution"]
description: "Advanced persistent threat detection, tracking, and attribution framework"
---

# APT Detection

## Overview

The APT Detection module provides specialized capabilities for identifying, tracking, and attributing Advanced Persistent Threats (APTs). It combines behavioral analysis, indicator correlation, TTP mapping, and threat actor profiling to detect sophisticated adversaries that evade conventional security controls. The module supports both automated detection rules and manual investigative workflows, enabling security teams to identify long-term compromise campaigns that may span months or years.

## Core Capabilities

- **Multi-Stage Attack Detection**: Identify attacks across the kill chain from initial access through exfiltration
- **TTP-Based Detection**: Map observed activities to MITRE ATT&CK framework techniques and procedures
- **Lateral Movement Detection**: Identify horizontal movement patterns across network segments
- **Persistence Mechanism Detection**: Detect registry modifications, scheduled tasks, WMI subscriptions, and other persistence techniques
- **Command and Control Detection**: Identify C2 communications through traffic analysis, DNS anomalies, and beacon detection
- **Data Exfiltration Detection**: Detect unauthorized data transfers through volume analysis and protocol anomalies
- **Threat Actor Attribution**: Match observed TTPs against known threat actor profiles
- **Campaign Tracking**: Track adversary activity across time and correlate related incidents

## Usage Examples

### APT Campaign Detection

```python
from apt_detection import APTDetector, DetectionRule, KillChainPhase

detector = APTDetector(
    detection_rules=[
        DetectionRule(name="lateral_movement_psexec", severity="high",
                      mitre_id="T1021.002", pattern="psexec_service_install"),
        DetectionRule(name="credential_dumping", severity="critical",
                      mitre_id="T1003.001", pattern="lsass_memory_access"),
        DetectionRule(name="data_staging", severity="high",
                      mitre_id="T1074.001", pattern="large_temp_archive"),
    ]
)

# Analyze events
events = detector.load_events("security_events.json")
detections = detector.analyze(events)

for detection in detections:
    print(f"[!] APT Detection: {detection.rule_name}")
    print(f"    Kill Chain Phase: {detection.kill_chain_phase.value}")
    print(f"    Confidence: {detection.confidence}%")
    print(f"    Affected Systems: {detection.affected_systems}")
    print(f"    Time Window: {detection.first_seen} to {detection.last_seen}")
```

### Threat Actor Attribution

```python
from apt_detection import AttributionEngine, ThreatActorProfile

attribution = AttributionEngine()

# Load known threat actor profiles
attribution.load_actor_profile(ThreatActorProfile(
    name="APT29",
    aliases=["Cozy Bear"],
    primary_mitres=["T1195.002", "T1071.001", "T1059.001", "T1003.001"],
    preferred_c2=["DNS-over-HTTPS", "Domain fronting"],
    targeting=["government", "healthcare", "think-tanks"],
    tools=["WellMess", "WellMail", "SUNBURST"],
))

# Attribute based on observations
result = attribution.attribute(
    observed_techniques=["T1195.002", "T1071.001", "T1059.001"],
    observed_tools=["SUNBURST"],
    targeting_patterns=["government", "technology"],
)

print(f"Attribution Results:")
for actor, score in result.top_matches:
    print(f"  {actor.name}: {score}% confidence")
```

### Lateral Movement Analysis

```python
from apt_detection import LateralMovementAnalyzer

analyzer = LateralMovementAnalyzer()

# Analyze authentication events
movement_map = analyzer.analyze_auth_events(auth_events)

print("Lateral Movement Map:")
for path in movement_map.paths:
    print(f"  Path: {' -> '.join(path.hops)}")
    print(f"    Techniques: {path.techniques}")
    print(f"    Time span: {path.duration}")
    print(f"    Risk score: {path.risk_score}")

# Detect anomalous movement
anomalies = analyzer.detect_anomalies(movement_map)
for anomaly in anomalies:
    print(f"\n[!] Anomalous Movement: {anomaly.description}")
    print(f"    Source: {anomaly.source_system}")
    print(f"    Destination: {anomaly.dest_system}")
    print(f"    User: {anomaly.user_account}")
```

## Best Practices

- **Correlate Across Data Sources**: Combine endpoint, network, and authentication logs for comprehensive detection
- **Focus on Techniques, Not Just IOCs**: APTs frequently change infrastructure; TTPs are more persistent
- **Establish Normal First**: Understand your environment's baseline before hunting for anomalies
- **Use Multiple Confidence Levels**: Tier your detection rules by confidence to manage alert volume
- **Maintain Threat Actor Profiles**: Keep profiles updated with latest intelligence on known APT groups
- **Investigate Low-Confidence Alerts**: Low-confidence detections may indicate early-stage compromise
- **Document Investigation Findings**: Maintain detailed notes for incident response and threat intelligence
- **Share Intelligence**: Contribute to community defense through ISACs and threat intel sharing platforms

## Related Modules

- **behavioral-analysis**: Behavioral pattern analysis for anomaly detection
- **threat-intelligence**: Threat intelligence for actor profiling
- **forensic-analysis**: Forensic investigation for incident validation

---

## Kill Chain Analysis

### Lockheed Martin Cyber Kill Chain Mapping

The kill chain framework maps adversary activities to seven distinct phases, enabling defenders to identify and disrupt attacks at any stage.

```python
from apt_detection import KillChainAnalyzer, KillChainPhase
from datetime import datetime, timedelta

class KillChainTracker:
    """Track and analyze adversary activities across the kill chain."""

    def __init__(self):
        self.phases = {}
        self.events = []
        self.disruption_points = []

    def add_event(self, timestamp, phase, technique, description, confidence):
        """Add an observed event mapped to a kill chain phase."""
        event = {
            "timestamp": timestamp,
            "phase": phase,
            "technique": technique,
            "description": description,
            "confidence": confidence
        }
        self.events.append(event)

        if phase not in self.phases:
            self.phases[phase] = []
        self.phases[phase].append(event)

    def analyze_progression(self):
        """Analyze the kill chain progression and identify gaps."""
        analysis = {
            "phases_observed": len(self.phases),
            "total_events": len(self.events),
            "time_span": None,
            "gaps": [],
            "next_expected": None
        }

        phase_order = [
            KillChainPhase.RECONNAISSANCE,
            KillChainPhase.WEAPONIZATION,
            KillChainPhase.DELIVERY,
            KillChainPhase.EXPLOITATION,
            KillChainPhase.INSTALLATION,
            KillChainPhase.COMMAND_AND_CONTROL,
            KillChainPhase.ACTIONS_ON_OBJECTIVES
        ]

        observed_phases = set(self.phases.keys())
        missing_phases = [p for p in phase_order if p not in observed_phases]

        analysis["gaps"] = missing_phases

        if self.events:
            timestamps = [e["timestamp"] for e in self.events]
            analysis["time_span"] = max(timestamps) - min(timestamps)

        # Determine next expected phase
        for phase in phase_order:
            if phase not in observed_phases:
                analysis["next_expected"] = phase
                break

        return analysis

    def calculate_sophistication_score(self):
        """Calculate adversary sophistication based on kill chain coverage."""
        analysis = self.analyze_progression()

        # More phases observed = higher sophistication
        phase_score = (analysis["phases_observed"] / 7) * 50

        # Faster progression = higher sophistication
        if analysis["time_span"]:
            if analysis["time_span"] < timedelta(hours=1):
                time_score = 50
            elif analysis["time_span"] < timedelta(days=1):
                time_score = 40
            elif analysis["time_span"] < timedelta(days=7):
                time_score = 30
            else:
                time_score = 20
        else:
            time_score = 0

        return phase_score + time_score


# Example usage
tracker = KillChainTracker()

# Add observed events
tracker.add_event(
    timestamp=datetime(2024, 1, 15, 8, 0),
    phase=KillChainPhase.RECONNAISSANCE,
    technique="T1595",
    description="Active scanning of external infrastructure",
    confidence=95
)

tracker.add_event(
    timestamp=datetime(2024, 1, 15, 9, 30),
    phase=KillChainPhase.WEAPONIZATION,
    technique="T1583.001",
    description="Domain registration for phishing infrastructure",
    confidence=80
)

tracker.add_event(
    timestamp=datetime(2024, 1, 15, 10, 0),
    phase=KillChainPhase.DELIVERY,
    technique="T1566.001",
    description="Phishing email with malicious attachment",
    confidence=90
)

# Analyze progression
analysis = tracker.analyze_progression()
print(f"Kill Chain Analysis:")
print(f"  Phases observed: {analysis['phases_observed']}/7")
print(f"  Total events: {analysis['total_events']}")
print(f"  Time span: {analysis['time_span']}")
print(f"  Missing phases: {[p.value for p in analysis['gaps']]}")
print(f"  Next expected phase: {analysis['next_expected'].value if analysis['next_expected'] else 'Completed'}")

# Calculate sophistication
sophistication = tracker.calculate_sophistication_score()
print(f"\nAdversary Sophistication Score: {sophistication:.1f}/100")
```

### Kill Chain Disruption Analysis

```python
from apt_detection import DisruptionAnalyzer, DefenseControl

class KillChainDisruption:
    """Identify opportunities to disrupt adversary kill chain progression."""

    def __init__(self, kill_chain_data):
        self.kill_chain = kill_chain_data
        self.disruption_opportunities = []

    def analyze_disruption_points(self):
        """Find optimal points for disrupting the kill chain."""
        phase_controls = {
            KillChainPhase.RECONNAISSANCE: [
                DefenseControl("WAF", "Block scanning patterns", 60),
                DefenseControl("Honeypots", "Divert reconnaissance", 40),
            ],
            KillChainPhase.WEAPONIZATION: [
                DefenseControl("Email Gateway", "Block malicious attachments", 70),
                DefenseControl("Sandbox", "Detonate suspicious files", 85),
            ],
            KillChainPhase.DELIVERY: [
                DefenseControl("Email Filter", "Block phishing emails", 75),
                DefenseControl("Web Proxy", "Block malicious URLs", 65),
            ],
            KillChainPhase.EXPLOITATION: [
                DefenseControl("EDR", "Prevent exploit execution", 80),
                DefenseControl("ASLR/DEP", "Memory protection", 70),
            ],
            KillChainPhase.INSTALLATION: [
                DefenseControl("EDR", "Block malware installation", 85),
                DefenseControl("AppLocker", "Prevent unauthorized binaries", 75),
            ],
            KillChainPhase.COMMAND_AND_CONTROL: [
                DefenseControl("Firewall", "Block C2 communications", 80),
                DefenseControl("DNS Sinkhole", "Redirect C2 domains", 90),
            ],
            KillChainPhase.ACTIONS_ON_OBJECTIVES: [
                DefenseControl("DLP", "Prevent data exfiltration", 70),
                DefenseControl("UEBA", "Detect anomalous behavior", 65),
            ],
        }

        for phase in self.kill_chain.phases:
            if phase in phase_controls:
                for control in phase_controls[phase]:
                    self.disruption_opportunities.append({
                        "phase": phase,
                        "control": control.name,
                        "description": control.description,
                        "effectiveness": control.effectiveness
                    })

        return self.disruption_opportunities

    def recommend_priority_disruptions(self, top_n=3):
        """Recommend the most effective disruption points."""
        opportunities = self.analyze_disruption_points()
        sorted_opps = sorted(opportunities, key=lambda x: x["effectiveness"], reverse=True)
        return sorted_opps[:top_n]


# Example usage
disruption_analyzer = KillChainDisruption(tracker)
opportunities = disruption_analyzer.recommend_priority_disruptions()

print("Priority Disruption Recommendations:")
for i, opp in enumerate(opportunities, 1):
    print(f"\n{i}. Phase: {opp['phase'].value}")
    print(f"   Control: {opp['control']}")
    print(f"   Effectiveness: {opp['effectiveness']}%")
```

---

## Lateral Movement Detection

### Detecting Lateral Movement Patterns

```python
from apt_detection import LateralMovementDetector, MovementPattern
from collections import defaultdict
from datetime import datetime, timedelta

class LateralMovementAnalysis:
    """Analyze and detect lateral movement patterns across the network."""

    def __init__(self):
        self.auth_events = []
        self.remote_access_events = []
        self.movement_graph = defaultdict(list)
        self.detection_rules = []

    def load_auth_events(self, events):
        """Load authentication events for analysis."""
        self.auth_events.extend(events)
        self._build_movement_graph()

    def _build_movement_graph(self):
        """Build a graph of authentication movements between systems."""
        for event in self.auth_events:
            if event["success"]:
                src = event["source_system"]
                dst = event["target_system"]
                user = event["user_account"]
                timestamp = event["timestamp"]

                self.movement_graph[src].append({
                    "destination": dst,
                    "user": user,
                    "timestamp": timestamp,
                    "auth_type": event.get("auth_type", "unknown")
                })

    def detect_pass_the_hash(self):
        """Detect potential pass-the-hash attacks."""
        detections = []

        for event in self.auth_events:
            indicators = []

            # NTLM authentication from unusual source
            if event.get("auth_type") == "NTLM" and event.get("logon_type") == "Network":
                indicators.append("NTLM network logon")

            # Authentication outside normal hours
            if self._is_unusual_hour(event["timestamp"], event["user_account"]):
                indicators.append("Unusual authentication time")

            # Multiple systems accessed in short timeframe
            if self._rapid_system_access(event["user_account"], event["timestamp"]):
                indicators.append("Rapid multi-system access")

            if len(indicators) >= 2:
                detections.append({
                    "type": "Pass the Hash",
                    "severity": "high",
                    "event": event,
                    "indicators": indicators,
                    "confidence": min(90, 50 + (len(indicators) * 15))
                })

        return detections

    def detect_psexec_lateral(self):
        """Detect lateral movement via PsExec."""
        detections = []

        for event in self.remote_access_events:
            if self._is_psexec_pattern(event):
                detections.append({
                    "type": "PsExec Lateral Movement",
                    "severity": "high",
                    "source": event["source_system"],
                    "destination": event["destination_system"],
                    "mitre_id": "T1021.002",
                    "indicators": [
                        "Service creation on remote system",
                        "Named pipe communication",
                        "Process spawned by Services.exe"
                    ]
                })

        return detections

    def detect_wmi_lateral(self):
        """Detect lateral movement via WMI."""
        detections = []

        for event in self.events:
            if self._is_wmi_remote_execution(event):
                detections.append({
                    "type": "WMI Lateral Movement",
                    "severity": "high",
                    "source": event["source_system"],
                    "destination": event["target_system"],
                    "mitre_id": "T1047",
                    "indicators": [
                        "WMI process creation on remote system",
                        "Winmgmt service activity",
                        "Remote WMI namespace access"
                    ]
                })

        return detections

    def detect_rdp_lateral(self):
        """Detect lateral movement via RDP."""
        detections = []

        for event in self.auth_events:
            if self._is_rdp_lateral_movement(event):
                detections.append({
                    "type": "RDP Lateral Movement",
                    "severity": "medium",
                    "source": event["source_system"],
                    "destination": event["target_system"],
                    "mitre_id": "T1021.001",
                    "indicators": [
                        "RDP session from non-admin system",
                        "RDP to sensitive server",
                        "RDP outside business hours"
                    ]
                })

        return detections

    def _is_unusual_hour(self, timestamp, user):
        """Check if authentication occurred at unusual hour."""
        hour = timestamp.hour
        # Define unusual hours as 10 PM - 6 AM
        return hour >= 22 or hour <= 6

    def _rapid_system_access(self, user, current_time, window_minutes=30):
        """Check if user accessed multiple systems rapidly."""
        user_events = [e for e in self.auth_events
                      if e["user_account"] == user
                      and abs((e["timestamp"] - current_time).total_seconds()) < window_minutes * 60]

        unique_systems = set(e["target_system"] for e in user_events)
        return len(unique_systems) >= 3

    def _is_psexec_pattern(self, event):
        """Identify PsExec execution patterns."""
        # PsExec creates a service and uses named pipes
        indicators = [
            event.get("service_name", "").startswith("PSEXE"),
            "\\Pipe\\PSEXESVC" in str(event.get("named_pipes", [])),
            event.get("parent_process") == "services.exe"
        ]
        return any(indicators)

    def _is_wmi_remote_execution(self, event):
        """Identify WMI remote execution patterns."""
        return (
            event.get("process_name", "").lower() == "wmiprvse.exe"
            and event.get("source_system") != event.get("target_system")
        )

    def _is_rdp_lateral_movement(self, event):
        """Identify RDP lateral movement patterns."""
        return (
            event.get("auth_type") == "RDP"
            and event.get("source_system") != event.get("target_system")
        )

    def generate_movement_report(self):
        """Generate a comprehensive lateral movement report."""
        report = {
            "total_auth_events": len(self.auth_events),
            "unique_source_systems": len(set(e["source_system"] for e in self.auth_events)),
            "unique_destination_systems": len(set(e["target_system"] for e in self.auth_events)),
            "unique_users": len(set(e["user_account"] for e in self.auth_events)),
            "detections": {
                "pass_the_hash": self.detect_pass_the_hash(),
                "psexec": self.detect_psexec_lateral(),
                "wmi": self.detect_wmi_lateral(),
                "rdp": self.detect_rdp_lateral()
            }
        }

        report["total_detections"] = sum(
            len(dets) for dets in report["detections"].values()
        )

        return report


# Example usage
lateral_analyzer = LateralMovementAnalysis()

# Load authentication events
auth_events = [
    {
        "timestamp": datetime(2024, 1, 15, 2, 30),
        "source_system": "WORKSTATION-01",
        "target_system": "DC-PRIMARY",
        "user_account": "admin",
        "success": True,
        "auth_type": "NTLM",
        "logon_type": "Network"
    },
    {
        "timestamp": datetime(2024, 1, 15, 2, 31),
        "source_system": "WORKSTATION-01",
        "target_system": "FILE-SERVER",
        "user_account": "admin",
        "success": True,
        "auth_type": "NTLM",
        "logon_type": "Network"
    },
    {
        "timestamp": datetime(2024, 1, 15, 2, 32),
        "source_system": "WORKSTATION-01",
        "target_system": "DB-SERVER",
        "user_account": "admin",
        "success": True,
        "auth_type": "NTLM",
        "logon_type": "Network"
    }
]

lateral_analyzer.load_auth_events(auth_events)

# Generate report
report = lateral_analyzer.generate_movement_report()
print("Lateral Movement Analysis Report:")
print(f"  Total auth events: {report['total_auth_events']}")
print(f"  Unique systems (source): {report['unique_source_systems']}")
print(f"  Unique systems (destination): {report['unique_destination_systems']}")
print(f"  Total detections: {report['total_detections']}")
```

### Network Graph Analysis

```python
from apt_detection import NetworkGraphAnalyzer
import networkx as nx

class LateralMovementGraph:
    """Visualize and analyze lateral movement as a network graph."""

    def __init__(self):
        self.graph = nx.DiGraph()
        self.edge_weights = {}

    def add_movement(self, source, destination, user, technique, timestamp):
        """Add a lateral movement observation to the graph."""
        self.graph.add_edge(source, destination, user=user, technique=technique, timestamp=timestamp)

        # Update edge weights
        edge_key = (source, destination)
        self.edge_weights[edge_key] = self.edge_weights.get(edge_key, 0) + 1

    def find_shortest_paths(self, source, target):
        """Find all shortest paths between two systems."""
        try:
            paths = list(nx.all_shortest_paths(self.graph, source, target))
            return paths
        except nx.NetworkXNoPath:
            return []

    def identify_critical_nodes(self):
        """Identify critical systems in the movement graph using centrality."""
        betweenness = nx.betweenness_centrality(self.graph)
        degree = nx.degree_centrality(self.graph)
        pagerank = nx.pagerank(self.graph)

        critical_nodes = {}
        for node in self.graph.nodes():
            critical_nodes[node] = {
                "betweenness_centrality": betweenness.get(node, 0),
                "degree_centrality": degree.get(node, 0),
                "pagerank": pagerank.get(node, 0),
                "risk_score": (
                    betweenness.get(node, 0) * 0.4 +
                    degree.get(node, 0) * 0.3 +
                    pagerank.get(node, 0) * 0.3
                ) * 100
            }

        return dict(sorted(critical_nodes.items(), key=lambda x: x[1]["risk_score"], reverse=True))

    def detect_communities(self):
        """Detect clusters of systems with heavy lateral movement."""
        undirected = self.graph.to_undirected()
        communities = list(nx.community.greedy_modularity_communities(undirected))

        community_analysis = []
        for i, community in enumerate(communities):
            subgraph = self.graph.subgraph(community)
            community_analysis.append({
                "community_id": i,
                "systems": list(community),
                "size": len(community),
                "internal_edges": subgraph.number_of_edges(),
                "density": nx.density(subgraph)
            })

        return community_analysis

    def calculate_movement_metrics(self):
        """Calculate overall lateral movement metrics."""
        metrics = {
            "total_movements": self.graph.number_of_edges(),
            "unique_systems": self.graph.number_of_nodes(),
            "connected_components": nx.number_weakly_connected_components(self.graph),
            "average_degree": sum(dict(self.graph.degree()).values()) / self.graph.number_of_nodes() if self.graph.number_of_nodes() > 0 else 0,
            "density": nx.density(self.graph)
        }

        # Identify most common movement pairs
        sorted_edges = sorted(self.edge_weights.items(), key=lambda x: x[1], reverse=True)
        metrics["top_movement_pairs"] = sorted_edges[:10]

        return metrics


# Example usage
movement_graph = LateralMovementGraph()

# Add movements
movement_graph.add_movement("WS-01", "DC-01", "admin", "T1021.002", datetime(2024, 1, 15, 2, 30))
movement_graph.add_movement("WS-01", "FILE-01", "admin", "T1021.002", datetime(2024, 1, 15, 2, 31))
movement_graph.add_movement("DC-01", "DB-01", "admin", "T1021.006", datetime(2024, 1, 15, 2, 32))

# Find critical nodes
critical = movement_graph.identify_critical_nodes()
print("Critical Systems:")
for system, metrics in critical.items():
    print(f"  {system}: Risk Score {metrics['risk_score']:.1f}")

# Detect communities
communities = movement_graph.detect_communities()
print(f"\nDetected {len(communities)} communities:")
for comm in communities:
    print(f"  Community {comm['community_id']}: {comm['systems']} ({comm['size']} systems)")
```

---

## Persistence Detection

### Registry-Based Persistence Detection

```python
from apt_detection import PersistenceDetector, PersistenceType
import re

class RegistryPersistenceAnalyzer:
    """Detect persistence mechanisms via Windows Registry modifications."""

    SUSPICIOUS_RUN_KEYS = [
        r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",
        r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce",
        r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunServices",
        r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunServicesOnce",
        r"SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Run",
        r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\Explorer\\Run",
        r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\Shell",
        r"SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Winlogon\\Userinit",
    ]

    SUSPICIOUS_FILE_EXTENSIONS = [".exe", ".dll", ".bat", ".cmd", ".vbs", ".ps1", ".js"]

    def __init__(self):
        self.baseline_registry = {}
        self.detections = []

    def analyze_registry_changes(self, baseline, current):
        """Compare baseline and current registry state to detect persistence."""
        detections = []

        for key in self.SUSPICIOUS_RUN_KEYS:
            baseline_values = baseline.get(key, {})
            current_values = current.get(key, {})

            # New entries added
            new_entries = set(current_values.keys()) - set(baseline_values.keys())
            for entry in new_entries:
                value = current_values[entry]
                risk = self._assess_registry_entry_risk(entry, value)

                detections.append({
                    "type": "Registry Persistence",
                    "severity": risk["severity"],
                    "registry_key": key,
                    "entry_name": entry,
                    "entry_value": value,
                    "risk_indicators": risk["indicators"],
                    "mitre_id": "T1547.001",
                    "recommendation": "Investigate the new registry entry"
                })

            # Modified entries
            modified = set(baseline_values.keys()) & set(current_values.keys())
            for entry in modified:
                if baseline_values[entry] != current_values[entry]:
                    risk = self._assess_registry_entry_risk(entry, current_values[entry])
                    detections.append({
                        "type": "Registry Modification",
                        "severity": "medium",
                        "registry_key": key,
                        "entry_name": entry,
                        "old_value": baseline_values[entry],
                        "new_value": current_values[entry],
                        "risk_indicators": risk["indicators"],
                        "mitre_id": "T1547.001"
                    })

        return detections

    def _assess_registry_entry_risk(self, name, value):
        """Assess the risk level of a registry entry."""
        indicators = []
        severity = "low"

        # Check for suspicious file extensions
        for ext in self.SUSPICIOUS_FILE_EXTENSIONS:
            if value.lower().endswith(ext):
                indicators.append(f"Suspicious file extension: {ext}")
                severity = "medium"

        # Check for encoded commands
        if "-enc " in value.lower() or "-encodedcommand " in value.lower():
            indicators.append("Encoded PowerShell command")
            severity = "high"

        # Check for remote paths
        if value.startswith("\\\\") or value.startswith("\\\\"):
            indicators.append("Remote UNC path")
            severity = "high"

        # Check for obfuscated paths
        if "%appdata%" in value.lower() or "%temp%" in value.lower():
            indicators.append("User-writable directory")
            severity = "medium"

        # Check for scheduled task references
        if "schtasks" in value.lower() or "at.exe" in value.lower():
            indicators.append("Scheduled task reference")
            severity = "high"

        return {"severity": severity, "indicators": indicators}


# Example usage
registry_analyzer = RegistryPersistenceAnalyzer()

baseline = {
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run": {
        "SecurityHealth": "\"C:\\Windows\\System32\\SecurityHealthSystray.exe\"",
    }
}

current = {
    "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run": {
        "SecurityHealth": "\"C:\\Windows\\System32\\SecurityHealthSystray.exe\"",
        "Updater": "\"C:\\Users\\user\\AppData\\Local\\Temp\\update.exe\" -enc SQBmACgA...",
    }
}

detections = registry_analyzer.analyze_registry_changes(baseline, current)
print("Registry Persistence Detections:")
for detection in detections:
    print(f"\n  [{detection['severity'].upper()}] {detection['type']}")
    print(f"  Registry Key: {detection['registry_key']}")
    print(f"  Entry: {detection['entry_name']}")
    print(f"  Value: {detection['entry_value']}")
    print(f"  Risk Indicators: {detection['risk_indicators']}")
```

### Scheduled Task Persistence Detection

```python
from apt_detection import ScheduledTaskAnalyzer
import xml.etree.ElementTree as ET

class ScheduledTaskPersistence:
    """Detect persistence via Windows Scheduled Tasks."""

    def __init__(self):
        self.suspicious_patterns = []
        self.detections = []

    def analyze_scheduled_tasks(self, tasks_xml):
        """Analyze scheduled tasks for persistence indicators."""
        detections = []

        for task_xml in tasks_xml:
            try:
                root = ET.fromstring(task_xml)
                task_name = root.findtext(".//TaskName", default="Unknown")

                # Check triggers for suspicious patterns
                triggers = root.findall(".//Triggers/*")
                for trigger in triggers:
                    if self._is_suspicious_trigger(trigger):
                        detections.append({
                            "type": "Suspicious Task Trigger",
                            "severity": "medium",
                            "task_name": task_name,
                            "trigger_type": trigger.tag,
                            "details": self._extract_trigger_details(trigger)
                        })

                # Check actions for suspicious patterns
                actions = root.findall(".//Actions/*")
                for action in actions:
                    if self._is_suspicious_action(action):
                        detections.append({
                            "type": "Suspicious Task Action",
                            "severity": "high",
                            "task_name": task_name,
                            "action_type": action.tag,
                            "command": action.findtext("Command", default=""),
                            "arguments": action.findtext("Arguments", default=""),
                            "indicators": self._analyze_action_risk(action)
                        })

                # Check for hidden tasks
                settings = root.find(".//Settings")
                if settings is not None:
                    hidden = settings.find("Hidden")
                    if hidden is not None and hidden.text == "true":
                        detections.append({
                            "type": "Hidden Scheduled Task",
                            "severity": "high",
                            "task_name": task_name
                        })

            except ET.ParseError as e:
                detections.append({
                    "type": "Parse Error",
                    "severity": "low",
                    "error": str(e)
                })

        return detections

    def _is_suspicious_trigger(self, trigger):
        """Check if a task trigger is suspicious."""
        trigger_type = trigger.tag.lower()

        # Time-based triggers outside business hours
        if trigger_type == "logontrigger":
            delay = trigger.find("Delay")
            if delay is not None:
                return True

        # Remote connection triggers
        if trigger_type == "sessionidletask":
            return True

        return False

    def _is_suspicious_action(self, action):
        """Check if a task action is suspicious."""
        command = action.findtext("Command", default="").lower()

        suspicious_commands = [
            "powershell.exe", "cmd.exe", "wscript.exe", "cscript.exe",
            "mshta.exe", "regsvr32.exe", "rundll32.exe", "certutil.exe"
        ]

        return any(cmd in command for cmd in suspicious_commands)

    def _extract_trigger_details(self, trigger):
        """Extract details from a trigger element."""
        details = {}
        for child in trigger:
            if child.text:
                details[child.tag] = child.text
        return details

    def _analyze_action_risk(self, action):
        """Analyze risk indicators in a task action."""
        indicators = []
        command = action.findtext("Command", default="")
        arguments = action.findtext("Arguments", default="")

        # Check for encoded commands
        if "-enc " in arguments.lower() or "-encodedcommand " in arguments.lower():
            indicators.append("Encoded PowerShell command")

        # Check for download cradles
        download_indicators = ["invoke-webrequest", "invoke-restmethod", "wget", "curl",
                               "downloadfile", "downloadstring", "start-bitstransfer"]
        for indicator in download_indicators:
            if indicator in arguments.lower():
                indicators.append(f"Download cradle detected: {indicator}")

        # Check for suspicious paths
        if any(path in command.lower() for path in ["\\temp\\", "\\appdata\\", "\\downloads\\"]):
            indicators.append("Suspicious file path")

        return indicators


# Example usage
task_analyzer = ScheduledTaskPersistence()

sample_task_xml = """<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
      <Delay>PT30S</Delay>
    </LogonTrigger>
  </Triggers>
  <Actions>
    <Exec>
      <Command>powershell.exe</Command>
      <Arguments>-enc SQBmACgA</Arguments>
    </Exec>
  </Actions>
  <Settings>
    <Hidden>true</Hidden>
  </Settings>
</Task>"""

detections = task_analyzer.analyze_scheduled_tasks([sample_task_xml])
print("Scheduled Task Persistence Detections:")
for detection in detections:
    print(f"\n  [{detection['severity'].upper()}] {detection['type']}")
    print(f"  Task: {detection.get('task_name', 'N/A')}")
    print(f"  Details: {detection}")
```

### WMI Persistence Detection

```python
from apt_detection import WMIPersistenceAnalyzer
import subprocess
import re

class WMIPersistenceDetector:
    """Detect persistence via WMI event subscriptions."""

    def __init__(self, target_system=None):
        self.target_system = target_system
        self.detections = []

    def enumerate_wmi_persistence(self):
        """Enumerate WMI event subscriptions for persistence."""
        detections = []

        # Query for WMI event subscriptions
        queries = [
            "SELECT * FROM __EventFilter",
            "SELECT * FROM __EventConsumer",
            "SELECT * FROM __FilterToConsumerBinding"
        ]

        for query in queries:
            try:
                results = self._execute_wmi_query(query)
                for result in results:
                    risk = self._assess_wmi_subscription_risk(result)
                    if risk["is_suspicious"]:
                        detections.append({
                            "type": "WMI Persistence",
                            "severity": risk["severity"],
                            "query": query,
                            "details": result,
                            "indicators": risk["indicators"],
                            "mitre_id": "T1546.003"
                        })
            except Exception as e:
                detections.append({
                    "type": "WMI Query Error",
                    "severity": "low",
                    "error": str(e)
                })

        return detections

    def _execute_wmi_query(self, query):
        """Execute a WMI query and return results."""
        cmd = f"wmic /namespace:\\\\root\\subscription path __EventFilter get /format:list"
        # In production, use proper WMI libraries
        return []

    def _assess_wmi_subscription_risk(self, subscription):
        """Assess risk level of a WMI subscription."""
        indicators = []
        is_suspicious = False
        severity = "low"

        # Check for suspicious consumer types
        consumer_type = subscription.get("ConsumerType", "")
        if consumer_type == "CommandLineEventConsumer":
            is_suspicious = True
            indicators.append("CommandLineEventConsumer detected")
            severity = "high"

        # Check for encoded commands in command line
        command_line = subscription.get("CommandLineTemplate", "")
        if "-enc " in command_line.lower():
            is_suspicious = True
            indicators.append("Encoded PowerShell command")
            severity = "critical"

        # Check for download cradles
        download_indicators = ["invoke-webrequest", "iwr", "curl", "wget"]
        for indicator in download_indicators:
            if indicator in command_line.lower():
                is_suspicious = True
                indicators.append(f"Download cradle: {indicator}")

        # Check for persistence triggers
        query = subscription.get("Query", "")
        persistence_triggers = [
            "__InstanceCreationEvent",
            "__InstanceModificationEvent",
            "Win32_LocalTime"
        ]
        for trigger in persistence_triggers:
            if trigger in query:
                is_suspicious = True
                indicators.append(f"Persistence trigger: {trigger}")

        return {
            "is_suspicious": is_suspicious,
            "severity": severity,
            "indicators": indicators
        }


# Example usage
wmi_detector = WMIPersistenceDetector(target_system="DC-PRIMARY")
detections = wmi_detector.enumerate_wmi_persistence()
print(f"WMI Persistence Detections: {len(detections)}")
for detection in detections:
    print(f"\n  [{detection['severity'].upper()}] {detection['type']}")
    print(f"  Indicators: {detection.get('indicators', [])}")
```

---

## Command and Control Detection

### C2 Beacon Detection

```python
from apt_detection import C2Detector, BeaconAnalyzer
from collections import defaultdict
import statistics

class C2BeaconDetector:
    """Detect command and control beaconing patterns in network traffic."""

    def __init__(self):
        self.flows = []
        self.beacon_candidates = []

    def load_network_flows(self, flows):
        """Load network flow data for analysis."""
        self.flows.extend(flows)

    def detect_beaconing(self, time_window_seconds=3600, jitter_threshold=0.3):
        """Detect beaconing patterns based on regular communication intervals."""
        # Group flows by destination IP
        ip_flows = defaultdict(list)
        for flow in self.flows:
            ip_flows[flow["dst_ip"]].append(flow)

        for dst_ip, flows in ip_flows.items():
            if len(flows) < 5:
                continue

            # Sort by timestamp
            flows.sort(key=lambda x: x["timestamp"])

            # Calculate intervals between connections
            intervals = []
            for i in range(1, len(flows)):
                interval = (flows[i]["timestamp"] - flows[i-1]["timestamp"]).total_seconds()
                intervals.append(interval)

            if not intervals:
                continue

            # Calculate statistics
            mean_interval = statistics.mean(intervals)
            std_interval = statistics.stdev(intervals) if len(intervals) > 1 else 0

            # Calculate jitter (coefficient of variation)
            jitter = std_interval / mean_interval if mean_interval > 0 else 0

            # Detect beaconing pattern
            if jitter < jitter_threshold and mean_interval > 0:
                confidence = max(0, min(100, (1 - jitter) * 100))

                beacon = {
                    "destination_ip": dst_ip,
                    "mean_interval": mean_interval,
                    "jitter": jitter,
                    "confidence": confidence,
                    "connection_count": len(flows),
                    "time_span": (flows[-1]["timestamp"] - flows[0]["timestamp"]).total_seconds(),
                    "ports": list(set(f.get("dst_port", 0) for f in flows))
                }

                self.beacon_candidates.append(beacon)

        return self.beacon_candidates

    def analyze_beacon_sophistication(self, beacon):
        """Analyze the sophistication of a detected beacon."""
        sophistication = {
            "regularity_score": 0,
            "evasion_score": 0,
            "overall_score": 0
        }

        # Regularity score (lower jitter = more regular)
        if beacon["jitter"] < 0.1:
            sophistication["regularity_score"] = 100
        elif beacon["jitter"] < 0.2:
            sophistication["regularity_score"] = 75
        elif beacon["jitter"] < 0.3:
            sophistication["regularity_score"] = 50
        else:
            sophistication["regularity_score"] = 25

        # Evasion score (higher jitter may indicate evasion attempts)
        if beacon["jitter"] > 0.4:
            sophistication["evasion_score"] = 80
        elif beacon["jitter"] > 0.3:
            sophistication["evasion_score"] = 60
        elif beacon["jitter"] > 0.2:
            sophistication["evasion_score"] = 40
        else:
            sophistication["evasion_score"] = 20

        # Overall score
        sophistication["overall_score"] = (
            sophistication["regularity_score"] * 0.6 +
            sophistication["evasion_score"] * 0.4
        )

        return sophistication


# Example usage
beacon_detector = C2BeaconDetector()

# Simulated network flows with regular beaconing
from datetime import datetime, timedelta
base_time = datetime(2024, 1, 15, 0, 0, 0)

flows = []
for i in range(20):
    flows.append({
        "src_ip": "10.0.1.100",
        "dst_ip": "198.51.100.42",
        "dst_port": 443,
        "timestamp": base_time + timedelta(seconds=i * 60 + (i % 3) * 5),
        "bytes_sent": 1024,
        "bytes_received": 2048
    })

beacon_detector.load_network_flows(flows)
beacons = beacon_detector.detect_beaconing()

print("C2 Beacon Detection Results:")
for beacon in beacons:
    print(f"\n  Destination: {beacon['destination_ip']}")
    print(f"  Mean Interval: {beacon['mean_interval']:.1f} seconds")
    print(f"  Jitter: {beacon['jitter']:.3f}")
    print(f"  Confidence: {beacon['confidence']:.1f}%")
    print(f"  Connection Count: {beacon['connection_count']}")

    sophistication = beacon_detector.analyze_beacon_sophistication(beacon)
    print(f"  Sophistication Score: {sophistication['overall_score']:.1f}/100")
```

### DNS-Based C2 Detection

```python
from apt_detection import DNSC2Detector
from collections import Counter
import re

class DNSBasedC2Detector:
    """Detect C2 communications using DNS-based channels."""

    def __init__(self):
        self.dns_queries = []
        self.detections = []

    def load_dns_queries(self, queries):
        """Load DNS query data."""
        self.dns_queries.extend(queries)

    def detect_dns_tunneling(self, entropy_threshold=3.5, length_threshold=50):
        """Detect DNS tunneling via high-entropy subdomains."""
        detections = []

        for query in self.dns_queries:
            if query["query_type"] not in ["A", "AAAA", "CNAME", "TXT"]:
                continue

            subdomain = query["query_name"].split(".")[0]

            # Calculate entropy
            entropy = self._calculate_entropy(subdomain)

            # Check for long subdomains
            if len(subdomain) > length_threshold:
                detections.append({
                    "type": "DNS Tunneling",
                    "severity": "high",
                    "query": query["query_name"],
                    "entropy": entropy,
                    "length": len(subdomain),
                    "mitre_id": "T1071.004"
                })
            elif entropy > entropy_threshold:
                detections.append({
                    "type": "Suspicious DNS Query",
                    "severity": "medium",
                    "query": query["query_name"],
                    "entropy": entropy,
                    "mitre_id": "T1071.004"
                })

        return detections

    def detect_fast_flux(self, min_ips=5, time_window=3600):
        """Detect fast-flux DNS for C2 infrastructure."""
        detections = []

        # Group queries by domain
        domain_queries = defaultdict(list)
        for query in self.dns_queries:
            domain = ".".join(query["query_name"].split(".")[-2:])
            domain_queries[domain].append(query)

        for domain, queries in domain_queries.items():
            # Count unique IPs in time window
            unique_ips = set()
            for query in queries:
                if "answers" in query:
                    for answer in query["answers"]:
                        unique_ips.add(answer.get("ip", ""))

            if len(unique_ips) >= min_ips:
                detections.append({
                    "type": "Fast Flux DNS",
                    "severity": "high",
                    "domain": domain,
                    "unique_ips": len(unique_ips),
                    "query_count": len(queries),
                    "mitre_id": "T1568.001"
                })

        return detections

    def detect_dga(self):
        """Detect Domain Generation Algorithm (DGA) patterns."""
        detections = []

        for query in self.dns_queries:
            domain = query["query_name"]

            # Check for DGA characteristics
            indicators = []

            # High entropy in subdomain
            subdomain = domain.split(".")[0]
            entropy = self._calculate_entropy(subdomain)
            if entropy > 3.0:
                indicators.append(f"High entropy: {entropy:.2f}")

            # Unusual character distribution
            char_freq = Counter(subdomain.lower())
            unique_chars = len(char_freq)
            if unique_chars > len(subdomain) * 0.6:
                indicators.append(f"High character diversity: {unique_chars}")

            # No dictionary words
            if not self._contains_dictionary_words(subdomain):
                indicators.append("No dictionary words found")

            if len(indicators) >= 2:
                detections.append({
                    "type": "DGA Domain",
                    "severity": "high",
                    "domain": domain,
                    "indicators": indicators,
                    "entropy": entropy,
                    "mitre_id": "T1568.002"
                })

        return detections

    def _calculate_entropy(self, text):
        """Calculate Shannon entropy of a string."""
        import math
        if not text:
            return 0

        char_freq = Counter(text)
        text_len = len(text)
        entropy = -sum((count/text_len) * math.log2(count/text_len)
                       for count in char_freq.values())
        return entropy

    def _contains_dictionary_words(self, text, min_word_length=4):
        """Check if text contains common dictionary words."""
        common_words = [
            "login", "portal", "mail", "web", "api", "dev", "test",
            "admin", "secure", "auth", "data", "server", "client"
        ]
        text_lower = text.lower()
        return any(word in text_lower for word in common_words if len(word) >= min_word_length)


# Example usage
dns_detector = DNSBasedC2Detector()

dns_queries = [
    {
        "query_name": "aGVsbG8gd29ybGQ.example.com",
        "query_type": "A",
        "answers": [{"ip": "198.51.100.42"}]
    },
    {
        "query_name": "xK9mN2pL5jW8qR3vT6yH1bF4nM7cA0sD.example.com",
        "query_type": "TXT",
        "answers": []
    }
]

dns_detector.load_dns_queries(dns_queries)

# Detect DNS tunneling
tunneling = dns_detector.detect_dns_tunneling()
print("DNS Tunneling Detections:")
for detection in tunneling:
    print(f"  [{detection['severity'].upper()}] {detection['query']}")
    print(f"    Entropy: {detection['entropy']:.2f}")
    print(f"    Length: {detection['length']}")
```

---

## Threat Actor Attribution

### Attribution Engine

```python
from apt_detection import AttributionEngine, ThreatActorProfile, AttributionConfidence
from typing import Dict, List, Tuple

class AdvancedAttributionEngine:
    """Multi-factor attribution engine for threat actor identification."""

    def __init__(self):
        self.actor_profiles = {}
        self.observation_matrix = {}
        self.attribution_weights = {
            "mitre_techniques": 0.30,
            "tools_used": 0.25,
            "infrastructure": 0.15,
            "targeting_patterns": 0.15,
            "temporal_patterns": 0.10,
            "geopolitical_context": 0.05
        }

    def load_actor_profile(self, actor_id, profile):
        """Load a threat actor profile."""
        self.actor_profiles[actor_id] = profile

    def attribute(self, observations):
        """Perform multi-factor attribution based on observations."""
        scores = {}

        for actor_id, profile in self.actor_profiles.items():
            score = self._calculate_actor_match_score(actor_id, profile, observations)
            scores[actor_id] = score

        # Sort by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        # Calculate confidence levels
        results = []
        for actor_id, score in sorted_scores:
            confidence = self._score_to_confidence(score)
            results.append({
                "actor_id": actor_id,
                "actor_name": self.actor_profiles[actor_id]["name"],
                "score": score,
                "confidence": confidence,
                "matching_factors": self._get_matching_factors(actor_id, observations)
            })

        return results

    def _calculate_actor_match_score(self, actor_id, profile, observations):
        """Calculate match score between actor profile and observations."""
        total_score = 0

        # MITRE Techniques matching
        if "mitre_techniques" in observations and "mitre_techniques" in profile:
            technique_matches = len(
                set(observations["mitre_techniques"]) &
                set(profile["mitre_techniques"])
            )
            technique_score = (technique_matches / max(len(profile["mitre_techniques"]), 1)) * 100
            total_score += technique_score * self.attribution_weights["mitre_techniques"]

        # Tools matching
        if "tools_used" in observations and "tools_used" in profile:
            tool_matches = len(
                set(observations["tools_used"]) &
                set(profile["tools_used"])
            )
            tool_score = (tool_matches / max(len(profile["tools_used"]), 1)) * 100
            total_score += tool_score * self.attribution_weights["tools_used"]

        # Infrastructure patterns
        if "infrastructure" in observations and "known_infrastructure" in profile:
            infra_matches = len(
                set(observations["infrastructure"]) &
                set(profile["known_infrastructure"])
            )
            infra_score = (infra_matches / max(len(profile["known_infrastructure"]), 1)) * 100
            total_score += infra_score * self.attribution_weights["infrastructure"]

        # Targeting patterns
        if "targeting" in observations and "targeting" in profile:
            target_matches = len(
                set(observations["targeting"]) &
                set(profile["targeting"])
            )
            target_score = (target_matches / max(len(profile["targeting"]), 1)) * 100
            total_score += target_score * self.attribution_weights["targeting_patterns"]

        return total_score

    def _score_to_confidence(self, score):
        """Convert numerical score to confidence level."""
        if score >= 80:
            return AttributionConfidence.HIGH
        elif score >= 60:
            return AttributionConfidence.MEDIUM
        elif score >= 40:
            return AttributionConfidence.LOW
        else:
            return AttributionConfidence.UNCERTAIN

    def _get_matching_factors(self, actor_id, observations):
        """Get list of factors that match the actor profile."""
        profile = self.actor_profiles[actor_id]
        matching = []

        if "mitre_techniques" in observations:
            matches = set(observations["mitre_techniques"]) & set(profile.get("mitre_techniques", []))
            if matches:
                matching.append(f"MITRE Techniques: {matches}")

        if "tools_used" in observations:
            matches = set(observations["tools_used"]) & set(profile.get("tools_used", []))
            if matches:
                matching.append(f"Tools: {matches}")

        if "targeting" in observations:
            matches = set(observations["targeting"]) & set(profile.get("targeting", []))
            if matches:
                matching.append(f"Targeting: {matches}")

        return matching


# Example usage
attribution = AdvancedAttributionEngine()

# Load threat actor profiles
attribution.load_actor_profile("APT29", {
    "name": "APT29 (Cozy Bear)",
    "aliases": ["Cozy Bear", "The Dukes", "YTTRIUM"],
    "country": "RU",
    "motivation": "espionage",
    "sophistication": "advanced",
    "mitre_techniques": ["T1195.002", "T1071.001", "T1059.001", "T1003.001", "T1082"],
    "tools_used": ["WellMess", "WellMail", "SUNBURST", "Cobalt Strike"],
    "known_infrastructure": ["avsvmcloud.com"],
    "targeting": ["government", "think-tanks", "healthcare", "technology"]
})

attribution.load_actor_profile("APT28", {
    "name": "APT28 (Fancy Bear)",
    "aliases": ["Fancy Bear", "Sofacy", "Pawn Storm"],
    "country": "RU",
    "motivation": "espionage",
    "sophistication": "advanced",
    "mitre_techniques": ["T1566.001", "T1071.001", "T1059.001", "T1003"],
    "tools_used": ["X-Agent", "X-Tunnel", "Zebrocy", "Credential Stealer"],
    "known_infrastructure": [],
    "targeting": ["military", "government", "media", "defense"]
})

# Perform attribution
observations = {
    "mitre_techniques": ["T1195.002", "T1071.001", "T1059.001"],
    "tools_used": ["SUNBURST", "Cobalt Strike"],
    "targeting": ["government", "technology"]
}

results = attribution.attribute(observations)

print("Attribution Results:")
for result in results:
    print(f"\n  Actor: {result['actor_name']}")
    print(f"  Score: {result['score']:.1f}")
    print(f"  Confidence: {result['confidence'].value}")
    print(f"  Matching Factors:")
    for factor in result['matching_factors']:
        print(f"    - {factor}")
```

### Attribution Confidence Assessment

```python
from apt_detection import ConfidenceAssessment

class AttributionConfidenceCalculator:
    """Calculate and assess attribution confidence levels."""

    # Evidence quality weights
    EVIDENCE_WEIGHTS = {
        "direct_tool_match": 0.9,
        "infrastructure_overlap": 0.8,
        "code_similarity": 0.85,
        "behavioral_pattern_match": 0.6,
        "temporal_correlation": 0.4,
        "geopolitical_inference": 0.3,
        "unshared_ioc": 0.7,
        "shared_ioc": 0.5
    }

    def calculate_confidence(self, evidence_list):
        """Calculate overall attribution confidence from evidence."""
        if not evidence_list:
            return {
                "confidence": "uncertain",
                "score": 0,
                "factors": []
            }

        weighted_scores = []
        factors = []

        for evidence in evidence_list:
            evidence_type = evidence.get("type", "")
            weight = self.EVIDENCE_WEIGHTS.get(evidence_type, 0.5)
            quality = evidence.get("quality", 0.5)
            contribution = weight * quality

            weighted_scores.append(contribution)
            factors.append({
                "type": evidence_type,
                "weight": weight,
                "quality": quality,
                "contribution": contribution
            })

        # Calculate weighted average
        if weighted_scores:
            overall_score = (sum(weighted_scores) / len(weighted_scores)) * 100
        else:
            overall_score = 0

        # Determine confidence level
        if overall_score >= 80:
            confidence = "high"
        elif overall_score >= 60:
            confidence = "medium"
        elif overall_score >= 40:
            confidence = "low"
        else:
            confidence = "uncertain"

        return {
            "confidence": confidence,
            "score": overall_score,
            "factors": factors,
            "recommendation": self._generate_recommendation(confidence)
        }

    def _generate_recommendation(self, confidence):
        """Generate recommendation based on confidence level."""
        recommendations = {
            "high": "Strong attribution evidence. Consider sharing with partners and updating threat actor profiles.",
            "medium": "Moderate attribution confidence. Corroborate with additional evidence before high-confidence claims.",
            "low": "Weak attribution evidence. Continue investigation to gather more indicators.",
            "uncertain": "Insufficient evidence for attribution. Focus on IOC collection and behavioral analysis."
        }
        return recommendations.get(confidence, "Unable to generate recommendation.")


# Example usage
conf_calculator = AttributionConfidenceCalculator()

evidence = [
    {"type": "direct_tool_match", "quality": 0.9, "description": "SUNBURST backdoor identified"},
    {"type": "infrastructure_overlap", "quality": 0.8, "description": "C2 domain linked to known APT29 infrastructure"},
    {"type": "behavioral_pattern_match", "quality": 0.7, "description": "Supply chain compromise technique matches APT29 TTPs"}
]

result = conf_calculator.calculate_confidence(evidence)
print("Attribution Confidence Assessment:")
print(f"  Confidence Level: {result['confidence'].upper()}")
print(f"  Score: {result['score']:.1f}/100")
print(f"  Recommendation: {result['recommendation']}")
print(f"\nEvidence Factors:")
for factor in result['factors']:
    print(f"  {factor['type']}: {factor['contribution']:.2f}")
```

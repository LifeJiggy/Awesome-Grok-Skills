---
name: "threat-hunting"
category: "blue-team"
version: "2.0.0"
tags: ["blue-team", "threat-hunting", "MITRE-ATT&CK", "proactive-detection", "hypothesis"]
---

# Threat Hunting

## Overview

The Threat Hunting module provides structured methodologies for proactively searching for threats that evade automated detection. It covers hypothesis-driven hunting, MITRE ATT&CK-based threat modeling, IOB (Indicators of Behavior) development, data source collection, and hypothesis validation workflows. The module integrates with endpoint telemetry, network flows, and cloud audit logs for comprehensive hunt operations.

This skill is essential for threat hunters, senior SOC analysts, and security researchers conducting proactive threat detection beyond automated alerting.

## Core Capabilities

- **Hypothesis Development**: Structured hypothesis creation using MITRE ATT&CK techniques and threat intelligence
- **Data Collection**: Endpoint telemetry, network flow data, cloud logs, DNS logs, and authentication logs
- **Hunt Queries**: Splunk SPL, Elastic EQL/KQL, and custom detection queries for each ATT&CK technique
- **IOB Framework**: Indicators of Behavior development from threat intelligence and adversary profiles
- **Technique Coverage**: ATT&CK technique mapping with coverage gap analysis
- **Hunt Operations**: Structured hunt lifecycle from scoping to reporting
- **Machine Learning Hunts**: Anomaly detection, clustering, and statistical analysis for unknown threats
- **Threat Intelligence Integration**: Mapping CTI reports to hunt hypotheses and detection opportunities

## Usage Examples

```python
from threat_hunting import (
    HuntPlanner,
    HypothesisEngine,
    MITREMapper,
    HuntQueryLibrary,
    IOBBuilder,
    HuntReporter,
)

# --- Hypothesis Development ---
engine = HypothesisEngine()
hypothesis = engine.create_hypothesis(
    threat_actor="APT29",
    technique="T1059.001 - PowerShell",
    rationale="Recent CTI report indicates APT29 using encoded PowerShell for C2",
    data_sources=["process_creation", "script_block_logging", "module_load"],
)
print(f"Hypothesis: {hypothesis.description}")
print(f"ATT&CK: {hypothesis.technique_id}")
print(f"Priority: {hypothesis.priority}")
print(f"Data sources: {hypothesis.data_sources}")

# --- MITRE Coverage Analysis ---
mapper = MITREMapper()
coverage = mapper.analyze_coverage(
    existing_rules=["T1059.001", "T1053.005", "T1021.002"],
    target_techniques=["T1059.001", "T1053.005", "T1021.002", "T1547.001", "T1003.001"],
)
print(f"Coverage: {coverage.coverage_pct:.0f}%")
print(f"Gaps: {coverage.gaps}")

# --- Hunt Query Library ---
queries = HuntQueryLibrary()
spl_query = queries.get_query(
    technique="T1059.001",
    platform="splunk",
    data_source="process_creation",
)
print(f"SPL: {spl_query}")

# --- IOB Builder ---
iob = IOBBuilder()
indicators = iob.build_from_actor("APT29")
for ind in indicators[:5]:
    print(f"  {ind.behavior_category}: {ind.description}")

# --- Execute Hunt ---
planner = HuntPlanner()
hunt = planner.create_hunt(
    name="APT29 PowerShell Discovery",
    hypothesis=hypothesis,
    scope=["endpoints", "network"],
    duration_days=5,
)
print(f"Hunt: {hunt.hunt_id}")
print(f"Duration: {hunt.duration_days} days")

# --- Hunt Report ---
reporter = HuntReporter()
report = reporter.generate_report(
    hunt=hunt,
    findings=["Suspicious PowerShell execution on 3 workstations"],
    true_positives=1,
    false_positives=2,
)
print(f"Report sections: {len(report.sections)}")
print(f"Recommendations: {len(report.recommendations)}")
```

## Best Practices

- Start hunts with clear hypotheses tied to specific MITRE ATT&CK techniques
- Use the MITRE ATT&CK Navigator to visualize coverage gaps before starting hunts
- Collect and centralize all required data sources before beginning hunt queries
- Document every hunt including hypothesis, queries, results, and conclusions
- Use IOBs (Indicators of Behavior) rather than IOCs for advanced threat detection
- Conduct hunts regularly (weekly or bi-weekly) rather than ad-hoc
- Rotate hunt focus across different ATT&CK tactics to ensure broad coverage
- Share hunt findings with the detection engineering team to create new automated rules
- Use statistical baselines to identify anomalies that indicate unknown threats
- Prioritize hunts based on threat intelligence and organizational risk profile

## Related Modules

- **security-monitoring**: Automated detection rules developed from hunt findings
- **incident-response**: Response procedures when hunts discover active threats
- **digital-forensics**: Deep investigation of findings from hunt operations
- **threat-intelligence**: CTI feeds that inform hunt hypotheses

## Advanced Configuration

### Hunt Platform Configuration

```yaml
hunt_platform:
  data_sources:
    - name: "endpoint_telemetry"
      type: "edr"
      provider: "crowdstrike"
      retention_days: 90
    - name: "network_flows"
      type: "netflow"
      provider: "ntopng"
      retention_days: 30
    - name: "dns_logs"
      type: "dns"
      provider: "passive_dns"
      retention_days: 60
    - name: "cloud_audit"
      type: "cloudtrail"
      provider: "aws"
      retention_days: 90
```

### MITRE ATT&CK Configuration

```yaml
mitre_config:
  framework: "attack_enterprise"
  version: "14.0"
  coverage_tracking: true
  auto_map_rules: true
  exclusion_list:
    - "T1557"    # Adversary-in-the-Middle (requires network tap)
    - "T1553"    # Subvert Trust Controls (requires specific tooling)
```

### Hunt Scoping Configuration

```yaml
hunt_scope:
  max_duration_days: 5
  max_data_sources: 10
  max_analysts: 3
  priority_factors:
    - threat_intelligence: 0.4
    - business_criticality: 0.3
    - coverage_gaps: 0.2
    - analyst_expertise: 0.1
```

## Architecture Patterns

### Threat Hunt Lifecycle

```
1. Scoping
   ├── Define objectives
   ├── Identify data sources
   ├── Set timeline
   └── Assign resources

2. Hypothesis Development
   ├── Threat intelligence analysis
   ├── MITRE ATT&CK mapping
   ├── IOB development
   └── Hypothesis documentation

3. Data Collection
   ├── Source identification
   ├── Data aggregation
   ├── Data normalization
   └── Data validation

4. Analysis
   ├── Query execution
   ├── Pattern recognition
   ├── Anomaly detection
   └── Hypothesis testing

5. Reporting
   ├── Findings documentation
   ├── True/false positive classification
   ├── Detection gap analysis
   └── Recommendations
```

### IOB (Indicators of Behavior) Framework

```
Behavior Categories:
├── Execution
│   ├── Command and scripting interpreters
│   ├── Exploitation for execution
│   └── Shared modules
├── Persistence
│   ├── Boot autostart
│   ├── Scheduled tasks
│   └── Registry modification
├── Privilege Escalation
│   ├── Process injection
│   ├── Access token manipulation
│   └── Domain policy modification
├── Defense Evasion
│   ├── Obfuscated files
│   ├── Indicator removal
│   └── Masquerading
├── Credential Access
│   ├── OS credential dumping
│   ├── Brute forcing
│   └── Steal session cookies
├── Discovery
│   ├── System information
│   ├── Network discovery
│   └── Account discovery
├── Lateral Movement
│   ├── Remote services
│   ├── Use alternate authentication
│   └── Remote access tools
├── Collection
│   ├── Data from local system
│   ├── Data from network shared drive
│   └── Screen capture
├── Exfiltration
│   ├── Exfil over C2 channel
│   ├── Exfil over web service
│   └── Automated exfil
└── Command and Control
    ├── Application layer protocol
    ├── Encrypted channel
    └── Proxy
```

### Data Source Coverage Model

| ATT&CK Tactic | Required Sources | Priority |
|----------------|------------------|----------|
| Initial Access | Web proxy, Email gateway | High |
| Execution | EDR, Script block logging | Critical |
| Persistence | EDR, Registry monitoring | Critical |
| Privilege Escalation | EDR, Authentication logs | Critical |
| Defense Evasion | EDR, Binary audit logs | High |
| Credential Access | EDR, AD logs, Kerberos logs | Critical |
| Lateral Movement | Network flows, EDR, AD logs | High |
| Collection | EDR, DLP logs | Medium |
| Exfiltration | Network flows, DNS, Web proxy | High |
| C2 | Network flows, DNS, EDR | Critical |

## Integration Guide

### Splunk Hunt Integration

```python
from threat_hunting import SplunkHuntConnector

splunk = SplunkHuntConnector(
    host="splunk.internal",
    port=8089,
    token="${SPLUNK_TOKEN}",
)

# Execute hunt query
results = splunk.execute_hunt(
    query='index=endpoint sourcetype=process_creation | where LIKE(Process_Command_Line, "%-enc%") | stats count by Host, User, Process_Command_Line',
    max_results=500,
    time_range="-7d",
)
print(f"Results: {results.count}")
for r in results.data:
    print(f"  {r['Host']}: {r['Process_Command_Line'][:80]}...")
```

### Elastic Hunt Integration

```python
from threat_hunting import ElasticHuntConnector

elastic = ElasticHuntConnector(
    hosts=["https://elastic.internal:9200"],
    index_pattern="winlogbeat-*",
)

# Execute EQL query
results = elastic.execute_eql(
    query='process where event.action = "create" and process.name : "powershell.exe" and process.command_line : "*-nop* -w hidden*"',
    time_range="last-7-days",
)
print(f"Suspicious PowerShell executions: {results.count}")
```

### MITRE ATT&CK Navigator

```python
from threat_hunting import MITREENavigator

navigator = MITREENavigator()
layer = navigator.create_layer(
    name="SOC Coverage",
    scores={
        "T1059.001": 3,  # PowerShell - fully covered
        "T1053.005": 2,  # Scheduled Task - partially covered
        "T1021.002": 1,  # SMB - not covered
    },
    description="SOC detection coverage assessment",
)
navigator.export_svg(layer, "coverage_layer.svg")
```

## Performance Optimization

### Query Optimization

| Technique | Description | Impact |
|-----------|-------------|--------|
| Index filtering | Restrict to relevant indices | 10-50x faster |
| Time range scoping | Limit to hunt period | 5-10x faster |
| Field selection | Return only needed fields | 2-3x faster |
| Aggregation first | Use stats/aggregate | 10-100x faster |
| Parallel queries | Run multiple queries | Linear speedup |

### Data Aggregation Optimization

```python
from threat_hunting import DataAggregator

aggregator = DataAggregator()
aggregated = aggregator.aggregate(
    sources=["endpoint", "network", "dns", "cloud"],
    time_range="2024-01-01 to 2024-01-07",
    correlation_fields=["src_ip", "hostname", "user"],
    deduplication=True,
)
print(f"Aggregated events: {aggregated.total_events}")
print(f"Unique entities: {aggregated.unique_entities}")
```

### Hunt Progress Tracking

```python
from threat_hunting import HuntProgress

progress = HuntProgress(hunt_id="hunt-001")
progress.update(
    queries_executed=15,
    results_reviewed=5000,
    true_positives=3,
    false_positives=12,
    coverage_gaps_found=2,
)
print(f"Progress: {progress.completion_pct:.0f}%")
print(f"Time remaining: {progress.estimated_remaining_hours:.1f}h")
```

## Security Considerations

### Hunt Security Controls

| Control | Description | Implementation |
|---------|-------------|----------------|
| Data Access | Restrict hunt data access | Role-based access |
| Query Logging | Log all hunt queries | SIEM integration |
| Result Handling | Secure handling of findings | Encryption, access control |
| Infrastructure | Secure hunt environment | Dedicated workstation |
| Communications | Secure hunt communications | Encrypted channels |

### Operational Security

```
Hunt OPSEC:
├── Use non-attributable infrastructure
├── Rotate hunt personas
├── Monitor for hunt detection by adversary
├── Use passive collection where possible
├── Avoid tipping off active adversaries
└── Document all actions for accountability
```

### Data Protection

```
Sensitive Data in Hunts:
├── PII in endpoint telemetry → Mask before analysis
├── Credentials in logs → Never expose in reports
├── Network captures → Encrypt at rest
├── Hunt results → Classify appropriately
└── Adversary tools → Secure storage
```

## Troubleshooting Guide

### Common Hunt Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Insufficient Data | Gaps in telemetry | Deploy missing data sources |
| Query Timeout | Queries not completing | Optimize queries, reduce scope |
| False Positive Storm | Too many results to review | Refine queries, add context |
| No Findings | Hypothesis not validated | Refine hypothesis, try alternate |
| Access Denied | Cannot query certain sources | Request elevated access |

### Data Source Gaps

```python
from threat_hunting import CoverageAnalyzer

analyzer = CoverageAnalyzer()
coverage = analyzer.analyze(
    data_sources=["endpoint", "network", "dns"],
    target_techniques=["T1059.001", "T1053.005", "T1021.002"],
)
print(f"Coverage: {coverage.coverage_pct:.0f}%")
print(f"Gaps: {coverage.gaps}")
for gap in coverage.gaps:
    print(f"  {gap.technique}: Missing {gap.missing_source}")
```

### Query Debugging

```
Issue: Query returns no results
1. Verify data source availability
2. Check time range is correct
3. Validate field names in index
4. Test with broader query
5. Check for data ingestion delays

Issue: Query too slow
1. Add index filtering
2. Reduce time range
3. Use aggregation instead of raw events
4. Add field selection
5. Check for index optimization
```

## API Reference

### HuntPlanner

```python
class HuntPlanner:
    def create_hunt(
        name: str,
        hypothesis: Hypothesis,
        scope: list[str],
        duration_days: int,
    ) -> Hunt:
        """Create new threat hunt."""
    
    def update_progress(
        hunt_id: str,
        updates: dict,
    ) -> Hunt:
        """Update hunt progress."""

class Hunt:
    hunt_id: str
    name: str
    hypothesis: Hypothesis
    status: str
    start_date: datetime
    end_date: datetime
    findings: list[Finding]
    queries_executed: int
    results_reviewed: int
```

### HypothesisEngine

```python
class HypothesisEngine:
    def create_hypothesis(
        threat_actor: str,
        technique: str,
        rationale: str,
        data_sources: list[str],
    ) -> Hypothesis:
        """Create structured hunt hypothesis."""
    
    def suggest_hypotheses(
        threat_intel: list[dict],
        coverage_gaps: list[str],
    ) -> list[Hypothesis]:
        """Suggest hypotheses from threat intel and gaps."""

class Hypothesis:
    description: str
    technique_id: str
    threat_actor: str
    priority: str
    data_sources: list[str]
    validation_criteria: str
    status: str
```

### MITREMapper

```python
class MITREMapper:
    def analyze_coverage(
        existing_rules: list[str],
        target_techniques: list[str],
    ) -> CoverageAnalysis:
        """Analyze MITRE ATT&CK coverage."""
    
    def map_rules_to_techniques(
        rules: list[dict],
    ) -> list[Mapping]:
        """Map detection rules to ATT&CK techniques."""

class CoverageAnalysis:
    coverage_pct: float
    covered: list[str]
    gaps: list[str]
    partial: list[str]
```

## Data Models

### Hunt

```
Hunt:
  hunt_id: str
  name: str
  hypothesis: Hypothesis
  status: str
  scope: list[str]
  start_date: datetime
  end_date: datetime
  analyst: str
  findings: list[Finding]
  queries: list[Query]
  metrics: HuntMetrics
```

### Finding

```
Finding:
  finding_id: str
  hunt_id: str
  description: str
  severity: str
  true_positive: bool
  mitre_technique: str
  evidence: list[str]
  recommendation: str
  detection_rule_created: bool
  rule_id: str
```

### Query

```
Query:
  query_id: str
  hunt_id: str
  platform: str          # splunk, elastic, custom
  query_text: str
  data_sources: list[str]
  execution_time_ms: int
  result_count: int
  results_reviewed: bool
  findings: list[str]
```

## Deployment Guide

### Hunt Program Setup

```
1. Foundation
   ├── Define hunt objectives
   ├── Identify data sources
   ├── Select tools and platforms
   └── Train hunt team

2. Process
   ├── Develop hunt lifecycle
   ├── Create hypothesis templates
   ├── Establish reporting format
   └── Define success criteria

3. Execution
   ├── Start with simple hunts
   ├── Progress to complex scenarios
   ├── Build query library
   └── Track coverage

4. Maturity
   ├── Automate recurring hunts
   ├── Integrate with detection engineering
   ├── Share findings across teams
   └── Measure program effectiveness
```

### Data Source Requirements

```
Minimum data sources for comprehensive hunting:
├── EDR (endpoint telemetry)
├── Network flows (NetFlow, Zeek)
├── DNS logs (passive DNS)
├── Authentication logs (AD, SSO)
├── Cloud audit logs (CloudTrail, Activity Log)
└── Web proxy logs
```

## Monitoring & Observability

### Hunt Program Metrics

| Metric | Target | Description |
|--------|--------|-------------|
| Hunts/Quarter | 4-6 | Regular hunt cadence |
| Coverage | >80% | ATT&CK technique coverage |
| Findings/Hunt | 1-3 | Actionable findings per hunt |
| Rule Creation | >50% | Findings leading to rules |
| True Positive Rate | >70% | Validated findings ratio |

### Hunt Dashboard

```
Hunt Program Dashboard:
├── Active hunts status
├── Coverage heatmap (ATT&CK)
├── Findings by severity
├── Rule creation rate
├── Data source coverage
├── Hunt completion rate
└── Trend analysis (quarterly)
```

## Testing Strategy

### Hunt Validation

```
1. Hypothesis Validation
   ├── Red team simulation
   ├── Known-good baseline
   ├── Historical data replay
   └── Adversary emulation

2. Query Validation
   ├── True positive test cases
   ├── False positive test cases
   ├── Performance benchmarks
   └── Cross-platform consistency

3. Coverage Validation
   ├── MITRE ATT&CK coverage assessment
   ├── Data source gap analysis
   ├── Rule effectiveness testing
   └── Detection gap remediation
```

## Versioning & Migration

### Hunt Library Versioning

```
v3.0: New hunt methodologies
├── ML-based anomaly hunts
├── Cloud-native hunt techniques
└── Supply chain hunt scenarios

v2.x: Hunt additions
├── New MITRE technique coverage
├── New data source integration
└── Query library expansion

v1.0.x: Hunt refinements
├── Query optimization
├── Documentation updates
└── False positive reduction
```

## Glossary

| Term | Definition |
|------|-----------|
| ATT&CK | Adversarial Tactics, Techniques, and Common Knowledge |
| Hypothesis | Testable assumption about adversary behavior |
| IOB | Indicator of Behavior — behavioral pattern of adversary |
| IOC | Indicator of Compromise — artifact of intrusion |
| Tactic | Adversary goal (e.g., persistence, lateral movement) |
| Technique | Method used to achieve tactic |
| Procedure | Specific implementation of technique |
| Coverage | Percentage of ATT&CK techniques with detection |
| False Positive | Benign activity matching detection criteria |
| True Positive | Malicious activity correctly identified |

## Changelog

### 2.0.0 (2024-12-01)
- Added ML-based anomaly hunting
- Added cloud-native hunt techniques
- Improved MITRE coverage tracking
- Added hunt automation

### 1.2.0 (2024-08-15)
- Added IOB framework
- Added Splunk hunt integration
- Improved hypothesis generation

### 1.1.0 (2024-05-20)
- Added MITRE ATT&CK mapping
- Added query library
- Added hunt reporting

### 1.0.0 (2024-02-01)
- Initial release with basic hunt methodology
- Simple hypothesis framework
- Basic query templates

## Contributing Guidelines

### Adding New Hunt Techniques

1. Document the hypothesis
2. Create query templates for multiple platforms
3. Include true/false positive test cases
4. Map to MITRE ATT&CK technique
5. Submit PR with validation results

### Code Quality

- Type hints on all functions
- Unit tests for query parsing
- Integration tests with hunt platforms
- Documentation for new techniques

## License

MIT License

Copyright (c) 2024 Threat Hunting Contributors

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

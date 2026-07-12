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

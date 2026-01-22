"""
Compliance Agent
Regulatory compliance and audit automation
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class ComplianceFramework(Enum):
    GDPR = "gdpr"
    SOC2 = "soc2"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    ISO27001 = "iso27001"


class ComplianceChecker:
    """Check compliance requirements"""
    
    def __init__(self):
        self.requirements = {}
        self.violations = []
    
    def add_requirement(self, framework: ComplianceFramework, requirement: str, severity: str = "high"):
        """Add compliance requirement"""
        key = f"{framework.value}:{requirement}"
        self.requirements[key] = {
            "framework": framework.value,
            "requirement": requirement,
            "severity": severity,
            "checked": False,
            "passed": False
        }
    
    def check_requirement(self, key: str, evidence: Dict) -> bool:
        """Check single requirement"""
        if key not in self.requirements:
            return False
        
        self.requirements[key]["checked"] = True
        self.requirements[key]["evidence"] = evidence
        
        if key.startswith("gdpr") and "data_consent" in evidence:
            self.requirements[key]["passed"] = evidence["data_consent"]
        elif key.startswith("soc2") and "audit_log" in evidence:
            self.requirements[key]["passed"] = len(evidence["audit_log"]) > 0
        else:
            self.requirements[key]["passed"] = evidence.get("compliant", True)
        
        if not self.requirements[key]["passed"]:
            self.violations.append(key)
        
        return self.requirements[key]["passed"]
    
    def generate_report(self, framework: ComplianceFramework = None) -> Dict:
        """Generate compliance report"""
        relevant = {k: v for k, v in self.requirements.items() 
                   if not framework or v["framework"] == framework.value}
        
        checked = [v for v in relevant.values() if v["checked"]]
        passed = [v for v in checked if v["passed"]]
        
        return {
            "framework": framework.value if framework else "all",
            "total_requirements": len(relevant),
            "checked": len(checked),
            "passed": len(passed),
            "failed": len(checked) - len(passed),
            "compliance_score": len(passed) / len(checked) * 100 if checked else 0,
            "violations": self.violations,
            "generated_at": datetime.now()
        }


class AuditLogger:
    """Audit trail management"""
    
    def __init__(self):
        self.logs = []
    
    def log(self, action: str, actor: str, resource: str, details: Dict = None):
        """Create audit log entry"""
        entry = {
            "id": len(self.logs) + 1,
            "timestamp": datetime.now(),
            "action": action,
            "actor": actor,
            "resource": resource,
            "details": details or {},
            "ip_address": "192.168.1.1"
        }
        self.logs.append(entry)
        return entry
    
    def query(self, filters: Dict = None) -> List[Dict]:
        """Query audit logs"""
        results = self.logs
        if filters:
            if "actor" in filters:
                results = [l for l in results if l["actor"] == filters["actor"]]
            if "action" in filters:
                results = [l for l in results if l["action"] == filters["action"]]
            if "resource" in filters:
                results = [l for l in results if l["resource"] == filters["resource"]]
        return results
    
    def export_for_compliance(self, start_date: datetime, end_date: datetime) -> List[Dict]:
        """Export logs for compliance audit"""
        return [l for l in self.logs if start_date <= l["timestamp"] <= end_date]


class PrivacyManager:
    """Privacy data management"""
    
    def __init__(self):
        self.data_subjects = {}
        self.consent_records = []
    
    def register_data_subject(self, subject_id: str, email: str, name: str):
        """Register data subject"""
        self.data_subjects[subject_id] = {
            "email": email,
            "name": name,
            "registered_at": datetime.now(),
            "consent_given": False,
            "data_categories": []
        }
    
    def record_consent(self, subject_id: str, purpose: str, granted: bool):
        """Record consent decision"""
        self.consent_records.append({
            "subject_id": subject_id,
            "purpose": purpose,
            "granted": granted,
            "timestamp": datetime.now()
        })
        if subject_id in self.data_subjects:
            self.data_subjects[subject_id]["consent_given"] = granted
    
    def handle_data_request(self, subject_id: str, request_type: str) -> Dict:
        """Handle GDPR data subject request"""
        if subject_id not in self.data_subjects:
            return {"error": "Subject not found"}
        
        subject = self.data_subjects[subject_id]
        
        if request_type == "access":
            return {"data": subject, "all_data": "Export all personal data"}
        elif request_type == "deletion":
            del self.data_subjects[subject_id]
            return {"status": "deleted"}
        elif request_type == "portability":
            return {"data": subject, "format": "JSON"}
        elif request_type == "rectification":
            return {"status": "ready_for_update"}
        
        return {"error": "Unknown request type"}
    
    def generate_privacy_report(self) -> Dict:
        """Generate privacy impact report"""
        total_subjects = len(self.data_subjects)
        consented = sum(1 for s in self.data_subjects.values() if s["consent_given"])
        
        return {
            "total_data_subjects": total_subjects,
            "with_consent": consented,
            "consent_rate": consented / total_subjects * 100 if total_subjects > 0 else 0,
            "data_categories": list(set(
                cat for s in self.data_subjects.values() 
                for cat in s.get("data_categories", [])
            ))
        }


class SecurityAuditor:
    """Security audit operations"""
    
    def __init__(self):
        self.findings = []
        self.scans = []
    
    def run_scan(self, target: str, scan_type: str = "vulnerability") -> str:
        """Run security scan"""
        scan_id = f"scan_{len(self.scans) + 1}"
        self.scans.append({
            "id": scan_id,
            "target": target,
            "type": scan_type,
            "started_at": datetime.now(),
            "status": "running"
        })
        return scan_id
    
    def add_finding(self, scan_id: str, finding: Dict):
        """Add security finding"""
        self.findings.append({
            "scan_id": scan_id,
            **finding,
            "severity": finding.get("severity", "medium"),
            "status": "open",
            "created_at": datetime.now()
        })
    
    def generate_security_report(self, start_date: datetime = None) -> Dict:
        """Generate security audit report"""
        start_date = start_date or datetime.now() - timedelta(days=30)
        
        recent_findings = [f for f in self.findings 
                         if f["created_at"] >= start_date]
        
        by_severity = {}
        for f in recent_findings:
            sev = f["severity"]
            by_severity[sev] = by_severity.get(sev, 0) + 1
        
        return {
            "period": {"start": start_date, "end": datetime.now()},
            "total_findings": len(recent_findings),
            "by_severity": by_severity,
            "open_findings": len([f for f in recent_findings if f["status"] == "open"]),
            "critical_issues": by_severity.get("critical", 0),
            "remediations": [f["title"] for f in recent_findings if f["severity"] == "critical"]
        }


if __name__ == "__main__":
    compliance = ComplianceChecker()
    compliance.add_requirement(ComplianceFramework.GDPR, "data_consent")
    compliance.add_requirement(ComplianceFramework.SOC2, "audit_logging")
    
    compliance.check_requirement("gdpr:data_consent", {"data_consent": True})
    compliance.check_requirement("soc2:audit_logging", {"audit_log": [1, 2, 3]})
    
    report = compliance.generate_report()
    
    audit = AuditLogger()
    audit.log("CREATE", "admin@company.com", "user:123", {"action": "Created user"})
    logs = audit.query({"action": "CREATE"})
    
    privacy = PrivacyManager()
    privacy.register_data_subject("user_001", "john@example.com", "John Doe")
    privacy.record_consent("user_001", "marketing", True)
    
    security = SecurityAuditor()
    scan_id = security.run_scan("api.example.com", "vulnerability")
    security.add_finding(scan_id, {"title": "SQL Injection", "severity": "critical"})
    
    security_report = security.generate_security_report()
    
    print(f"Compliance score: {report['compliance_score']:.1f}%")
    print(f"Audit logs: {len(logs)}")
    print(f"Privacy consent rate: {privacy.generate_privacy_report()['consent_rate']:.1f}%")
    print(f"Critical security issues: {security_report['critical_issues']}")

"""
Ethics Agent
AI ethics and bias detection
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime


class BiasType(Enum):
    GENDER = "gender"
    RACE = "race"
    AGE = "age"
    SOCIOECONOMIC = "socioeconomic"
    RELIGIOUS = "religious"
    DISABILITY = "disability"
    GEOGRAPHIC = "geographic"


class BiasDetector:
    """AI bias detection"""
    
    def __init__(self):
        self.thresholds = {}
        self.audit_results = []
    
    def set_bias_threshold(self, bias_type: BiasType, threshold: float = 0.1):
        """Set acceptable bias threshold"""
        self.thresholds[bias_type.value] = threshold
    
    def analyze_model_outputs(self, predictions: List[Dict], 
                             protected_attributes: List[str]) -> Dict:
        """Analyze model for bias"""
        bias_scores = {}
        
        for attr in protected_attributes:
            if attr in predictions[0]:
                attr_values = {}
                for pred in predictions:
                    val = str(pred.get(attr, "unknown"))
                    outcome = pred.get("prediction", 0)
                    if val not in attr_values:
                        attr_values[val] = {"count": 0, "positive": 0}
                    attr_values[val]["count"] += 1
                    if outcome == 1:
                        attr_values[val]["positive"] += 1
                
                rates = {}
                for val, data in attr_values.items():
                    rates[val] = data["positive"] / data["count"] if data["count"] > 0 else 0
                
                max_rate = max(rates.values())
                min_rate = min(rates.values())
                bias_scores[attr] = max_rate - min_rate
        
        return {
            "bias_scores": bias_scores,
            "flagged": any(
                score > self.thresholds.get(attr, 0.1) 
                for attr, score in bias_scores.items()
            )
        }
    
    def generate_bias_report(self, analysis_results: Dict) -> Dict:
        """Generate bias audit report"""
        return {
            "analysis_date": datetime.now(),
            "bias_scores": analysis_results["bias_scores"],
            "flagged_attributes": [
                attr for attr, score in analysis_results["bias_scores"].items()
                if score > self.thresholds.get(attr, 0.1)
            ],
            "recommendations": self._generate_recommendations(analysis_results["bias_scores"])
        }
    
    def _generate_recommendations(self, bias_scores: Dict) -> List[str]:
        """Generate bias mitigation recommendations"""
        recommendations = []
        for attr, score in bias_scores.items():
            if score > 0.1:
                recommendations.append(f"Review {attr} representation in training data")
                recommendations.append(f"Consider re-sampling to balance {attr} groups")
                recommendations.append(f"Apply fairness constraints during training")
        return recommendations


class FairnessMetrics:
    """Fairness metrics calculator"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_equalized_odds(self, predictions: List[Dict], 
                                protected_attr: str, outcome_attr: str) -> Dict:
        """Calculate equalized odds difference"""
        groups = {}
        for pred in predictions:
            group = pred.get(protected_attr, "unknown")
            outcome = pred.get(outcome_attr, 0)
            if group not in groups:
                groups[group] = {"positive": 0, "total": 0}
            groups[group]["total"] += 1
            if outcome == 1:
                groups[group]["positive"] += 1
        
        rates = {g: d["positive"]/d["total"] if d["total"] > 0 else 0 for g, d in groups.items()}
        max_rate = max(rates.values())
        min_rate = min(rates.values())
        
        return {
            "metric": "equalized_odds",
            "group_rates": rates,
            "difference": max_rate - min_rate,
            "is_fair": (max_rate - min_rate) < 0.1
        }
    
    def calculate_demographic_parity(self, predictions: List[Dict],
                                    protected_attr: str, positive_attr: str) -> Dict:
        """Calculate demographic parity"""
        total_positive = sum(1 for p in predictions if p.get(positive_attr) == 1)
        positive_rate = total_positive / len(predictions) if predictions else 0
        
        group_rates = {}
        for pred in predictions:
            group = pred.get(protected_attr, "unknown")
            if group not in group_rates:
                group_rates[group] = {"count": 0, "positive": 0}
            group_rates[group]["count"] += 1
            if pred.get(positive_attr) == 1:
                group_rates[group]["positive"] += 1
        
        disparities = {}
        for group, data in group_rates.items():
            expected = data["count"] * positive_rate
            disparities[group] = abs(data["positive"] - expected) / max(expected, 1)
        
        return {
            "metric": "demographic_parity",
            "overall_rate": positive_rate,
            "group_rates": {g: d["positive"]/d["count"] if d["count"] > 0 else 0 for g, d in group_rates.items()},
            "max_disparity": max(disparities.values()) if disparities else 0
        }


class ComplianceChecker:
    """AI ethics compliance checking"""
    
    def __init__(self):
        self.frameworks = {}
        self.requirements = {}
    
    def add_framework(self, name: str, version: str):
        """Add compliance framework"""
        self.frameworks[name] = {"version": version, "requirements": []}
    
    def add_requirement(self, framework: str, requirement: str, mandatory: bool = True):
        """Add requirement to framework"""
        if framework not in self.frameworks:
            self.frameworks[framework] = {"version": "1.0", "requirements": []}
        self.frameworks[framework]["requirements"].append({
            "text": requirement,
            "mandatory": mandatory,
            "status": "pending"
        })
    
    def check_compliance(self, framework: str, evidence: Dict) -> Dict:
        """Check compliance with framework"""
        if framework not in self.frameworks:
            return {"error": "Framework not found"}
        
        requirements = self.frameworks[framework]["requirements"]
        results = []
        
        for req in requirements:
            compliant = True
            details = "Compliant"
            
            if "transparency" in req["text"].lower():
                compliant = evidence.get("transparency_docs", False)
                details = "Documentation present" if compliant else "Missing documentation"
            elif "fairness" in req["text"].lower():
                compliant = evidence.get("fairness_audit_passed", False)
                details = "Audit passed" if compliant else "Fairness audit not passed"
            
            results.append({
                "requirement": req["text"],
                "mandatory": req["mandatory"],
                "compliant": compliant,
                "details": details
            })
        
        mandatory_failed = [r for r in results if r["mandatory"] and not r["compliant"]]
        
        return {
            "framework": framework,
            "total_requirements": len(results),
            "compliant": len(mandatory_failed) == 0,
            "results": results,
            "compliance_score": len([r for r in results if r["compliant"]]) / len(results) * 100 if results else 0
        }


class EthicsGuidelines:
    """AI ethics guidelines generator"""
    
    def __init__(self):
        self.guidelines = {}
    
    def generate_principles(self, domain: str) -> List[Dict]:
        """Generate ethics principles for domain"""
        base_principles = [
            {
                "principle": "Transparency",
                "description": "AI systems should be transparent and explainable",
                "implementation": "Provide clear documentation and model explanations"
            },
            {
                "principle": "Fairness",
                "description": "AI systems should not discriminate",
                "implementation": "Regular bias audits and fairness testing"
            },
            {
                "principle": "Accountability",
                "description": "Clear accountability for AI decisions",
                "implementation": "Human oversight and audit trails"
            },
            {
                "principle": "Privacy",
                "description": "Protect user data and privacy",
                "implementation": "Data minimization and encryption"
            },
            {
                "principle": "Safety",
                "description": "AI systems should be safe and secure",
                "implementation": "Robust testing and monitoring"
            }
        ]
        
        if domain == "healthcare":
            base_principles.extend([
                {
                    "principle": "Clinical Oversight",
                    "description": "AI should support, not replace, clinical judgment",
                    "implementation": "Human-in-the-loop for critical decisions"
                }
            ])
        elif domain == "finance":
            base_principles.extend([
                {
                    "principle": "Consumer Protection",
                    "description": "Protect consumers from algorithmic discrimination",
                    "implementation": "Regular fairness testing on lending decisions"
                }
            ])
        
        return base_principles
    
    def generate_checklist(self, domain: str) -> List[str]:
        """Generate ethics compliance checklist"""
        checklist = [
            "Document model purpose and limitations",
            "Provide model explanations to users",
            "Conduct bias testing on protected groups",
            "Implement human oversight for critical decisions",
            "Establish data governance policies",
            "Create incident response procedures",
            "Train team on AI ethics"
        ]
        
        if domain == "healthcare":
            checklist.extend([
                "Ensure FDA/compliance requirements are met",
                "Validate on diverse patient populations",
                "Implement clinical decision support warnings"
            ])
        
        return checklist


class AuditTrail:
    """Ethics audit trail"""
    
    def __init__(self):
        self.audit_logs = []
    
    def log_decision(self, decision_type: str, decision: str, 
                    rationale: str, reviewer: str):
        """Log ethical decision"""
        self.audit_logs.append({
            "timestamp": datetime.now(),
            "type": decision_type,
            "decision": decision,
            "rationale": rationale,
            "reviewer": reviewer
        })
    
    def get_audit_report(self, start_date: datetime = None) -> Dict:
        """Generate audit report"""
        start_date = start_date or datetime.now() - timedelta(days=30)
        logs = [l for l in self.audit_logs if l["timestamp"] >= start_date]
        
        by_type = {}
        for log in logs:
            by_type[log["type"]] = by_type.get(log["type"], 0) + 1
        
        return {
            "period": {"start": start_date, "end": datetime.now()},
            "total_decisions": len(logs),
            "by_type": by_type,
            "decisions": logs[-10:]
        }


if __name__ == "__main__":
    bias = BiasDetector()
    bias.set_bias_threshold(BiasType.GENDER, 0.05)
    
    predictions = [
        {"gender": "male", "prediction": 1},
        {"gender": "male", "prediction": 1},
        {"gender": "female", "prediction": 0},
        {"gender": "female", "prediction": 0}
    ]
    
    analysis = bias.analyze_model_outputs(predictions, ["gender"])
    report = bias.generate_bias_report(analysis)
    
    fairness = FairnessMetrics()
    equalized_odds = fairness.calculate_equalized_odds(predictions, "gender", "prediction")
    
    compliance = ComplianceChecker()
    compliance.add_framework("EU_AI_Act", "1.0")
    compliance.add_requirement("EU_AI_Act", "Transparency requirements", True)
    compliance.add_requirement("EU_AI_Act", "Fairness requirements", True)
    compliance_check = compliance.check_compliance("EU_AI_Act", {
        "transparency_docs": True,
        "fairness_audit_passed": True
    })
    
    guidelines = EthicsGuidelines()
    principles = guidelines.generate_principles("healthcare")
    checklist = guidelines.generate_checklist("finance")
    
    audit = AuditTrail()
    audit.log_decision("model_deployment", "Approved", "Passed all bias tests", "Ethics Team")
    audit_report = audit.get_audit_report()
    
    print(f"Bias detected: {analysis['flagged']}")
    print(f"Equalized odds difference: {equalized_odds['difference']:.2f}")
    print(f"Compliance score: {compliance_check['compliance_score']:.1f}%")
    print(f"Ethics principles: {len(principles)}")
    print(f"Audit decisions: {audit_report['total_decisions']}")

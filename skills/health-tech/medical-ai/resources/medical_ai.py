"""
Medical AI Pipeline
Healthcare AI and diagnostic systems
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class DiagnosisType(Enum):
    PREVENTIVE = "preventive"
    ACUTE = "acute"
    CHRONIC = "chronic"
    EMERGENCY = "emergency"


@dataclass
class PatientRecord:
    patient_id: str
    name: str
    date_of_birth: datetime
    medical_history: List[str]
    allergies: List[str]
    medications: List[str]
    vital_signs: Dict[str, float]


@dataclass
class ClinicalNote:
    note_id: str
    patient_id: str
    physician_id: str
    timestamp: datetime
    diagnosis: str
    symptoms: List[str]
    recommendations: List[str]
    follow_up_required: bool


class VitalSignsAnalyzer:
    """Analyze patient vital signs"""
    
    def __init__(self):
        self.normal_ranges = {
            "heart_rate": (60, 100),
            "blood_pressure_systolic": (90, 120),
            "blood_pressure_diastolic": (60, 80),
            "temperature": (36.1, 37.2),
            "respiratory_rate": (12, 20),
            "oxygen_saturation": (95, 100),
            "blood_glucose": (70, 100)
        }
    
    def analyze(self, vital_signs: Dict[str, float]) -> Dict:
        """Analyze vital signs for abnormalities"""
        results = {}
        alerts = []
        
        for sign, value in vital_signs.items():
            if sign in self.normal_ranges:
                low, high = self.normal_ranges[sign]
                status = "normal"
                
                if value < low:
                    status = "low"
                    alerts.append(f"{sign}: {value} is below normal ({low}-{high})")
                elif value > high:
                    status = "high"
                    alerts.append(f"{sign}: {value} is above normal ({low}-{high})")
                
                results[sign] = {
                    "value": value,
                    "status": status,
                    "range": (low, high)
                }
        
        return {
            "vital_signs": results,
            "alerts": alerts,
            "critical": len([a for a in alerts if "critical" in a.lower()]) > 0
        }
    
    def calculate_news_score(self, vital_signs: Dict[str, float]) -> int:
        """Calculate National Early Warning Score"""
        score = 0
        
        if vital_signs.get("heart_rate", 0) < 40: score += 3
        elif vital_signs.get("heart_rate", 0) < 51: score += 1
        elif vital_signs.get("heart_rate", 0) > 130: score += 3
        elif vital_signs.get("heart_rate", 0) > 111: score += 2
        elif vital_signs.get("heart_rate", 0) > 91: score += 1
        
        if vital_signs.get("blood_pressure_systolic", 0) < 91: score += 3
        elif vital_signs.get("blood_pressure_systical", 0) < 101: score += 2
        elif vital_signs.get("blood_pressure_systolic", 0) > 219: score += 3
        elif vital_signs.get("blood_pressure_systolic", 0) > 200: score += 2
        
        if vital_signs.get("oxygen_saturation", 0) < 85: score += 3
        elif vital_signs.get("oxygen_saturation", 0) < 92: score += 2
        elif vital_signs.get("oxygen_saturation", 0) < 94: score += 1
        
        return score


class DrugInteractionChecker:
    """Check for drug interactions"""
    
    def __init__(self):
        self.interactions = {
            ("warfarin", "aspirin"): {"severity": "major", "effect": "increased bleeding risk"},
            ("lisinopril", "potassium"): {"severity": "moderate", "effect": "hyperkalemia"},
            ("metformin", "contrast_dye"): {"severity": "major", "effect": "lactic acidosis"},
            ("sildenafil", "nitroglycerin"): {"severity": "severe", "effect": "dangerous hypotension"}
        }
    
    def check(self, medications: List[str]) -> List[Dict]:
        """Check for drug interactions"""
        results = []
        medications_lower = [m.lower() for m in medications]
        
        for (drug1, drug2), interaction in self.interactions.items():
            if drug1 in medications_lower and drug2 in medications_lower:
                results.append({
                    "drugs": [drug1, drug2],
                    "severity": interaction["severity"],
                    "effect": interaction["effect"]
                })
        
        return results
    
    def check_allergy(self, medications: List[str], 
                     allergies: List[str]) -> List[Dict]:
        """Check for allergy conflicts"""
        results = []
        allergies_lower = [a.lower() for a in allergies]
        
        allergy_mapping = {
            "penicillin": ["amoxicillin", "ampicillin", "penicillin"],
            "sulfa": ["sulfamethoxazole", "sulfasalazine"],
            "aspirin": ["aspirin", "acetylsalicylic"]
        }
        
        for allergy, related_drugs in allergy_mapping.items():
            if allergy in allergies_lower:
                for drug in medications:
                    if drug.lower() in related_drugs:
                        results.append({
                            "allergy": allergy,
                            "drug": drug,
                            "severity": "severe"
                        })
        
        return results


class ClinicalDecisionSupport:
    """Clinical decision support system"""
    
    def __init__(self):
        self.guidelines = {}
        self.risk_models = {}
    
    def assess_cardiovascular_risk(self,
                                  age: int,
                                  gender: str,
                                  systolic_bp: float,
                                  cholesterol: float,
                                  smoker: bool,
                                  diabetic: bool) -> Dict:
        """Calculate cardiovascular disease risk"""
        base_risk = 0
        
        base_risk += (age - 40) * 0.02 if age > 40 else 0
        base_risk += 0.1 if systolic_bp > 140 else 0
        base_risk += (cholesterol - 200) * 0.001 if cholesterol > 200 else 0
        base_risk += 0.15 if smoker else 0
        base_risk += 0.1 if diabetic else 0
        base_risk += 0.05 if gender == "male" else 0
        
        return {
            "risk_score": min(1.0, base_risk),
            "risk_category": "high" if base_risk > 0.15 else "moderate" if base_risk > 0.08 else "low",
            "recommendations": self._get_cvd_recommendations(base_risk)
        }
    
    def _get_cvd_recommendations(self, risk: float) -> List[str]:
        """Get recommendations based on risk level"""
        recommendations = ["Regular exercise", "Healthy diet"]
        
        if risk > 0.15:
            recommendations.extend([
                "Consider statin therapy",
                "Frequent blood pressure monitoring",
                "Smoking cessation program"
            ])
        elif risk > 0.08:
            recommendations.extend([
                "Annual lipid panel",
                "Blood pressure monitoring"
            ])
        
        return recommendations
    
    def suggest_diagnosis(self, symptoms: List[str],
                         patient_history: List[str]) -> List[Dict]:
        """Suggest possible diagnoses based on symptoms"""
        symptom_diagnosis_map = {
            "chest_pain": ["angina", "myocardial_infarction", "gastroesophageal_reflux"],
            "shortness_of_breath": ["asthma", "copd", "heart_failure", "pneumonia"],
            "headache": ["migraine", "tension_headache", "hypertension", "meningitis"],
            "fatigue": ["anemia", "depression", "hypothyroidism", "chronic_fatigue_syndrome"]
        }
        
        possible_diagnoses = []
        for symptom in symptoms:
            if symptom in symptom_diagnosis_map:
                for diagnosis in symptom_diagnosis_map[symptom]:
                    if diagnosis not in [d["name"] for d in possible_diagnoses]:
                        possible_diagnoses.append({
                            "name": diagnosis,
                            "match_score": 0.8,
                            "type": DiagnosisType.ACUTE
                        })
        
        return sorted(possible_diagnoses, key=lambda x: x["match_score"], reverse=True)


if __name__ == "__main__":
    vital_analyzer = VitalSignsAnalyzer()
    drug_checker = DrugInteractionChecker()
    cds = ClinicalDecisionSupport()
    
    vitals = {
        "heart_rate": 85,
        "blood_pressure_systolic": 135,
        "blood_pressure_diastolic": 88,
        "temperature": 37.0,
        "oxygen_saturation": 97
    }
    
    vitals_analysis = vital_analyzer.analyze(vitals)
    news_score = vital_analyzer.calculate_news_score(vitals)
    
    medications = ["warfarin", "aspirin"]
    interactions = drug_checker.check(medications)
    
    cvd_risk = cds.assess_cardiovascular_risk(
        age=55, gender="male", systolic_bp=145,
        cholesterol=220, smoker=True, diabetic=False
    )
    
    diagnoses = cds.suggest_diagnosis(["chest_pain", "shortness_of_breath"], [])
    
    print(f"Vital signs alerts: {len(vitals_analysis['alerts'])}")
    print(f"NEWS score: {news_score}")
    print(f"Drug interactions: {len(interactions)}")
    print(f"CVD risk: {cvd_risk['risk_category']}")
    print(f"Possible diagnoses: {len(diagnoses)}")

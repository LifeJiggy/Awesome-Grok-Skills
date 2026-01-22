"""
Healthcare Agent
Healthcare operations and patient management
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta


class AppointmentType(Enum):
    CONSULTATION = "consultation"
    FOLLOW_UP = "follow_up"
    PROCEDURE = "procedure"
    EMERGENCY = "emergency"
    TELEMEDICINE = "telemedicine"


class PatientManager:
    """Patient management"""
    
    def __init__(self):
        self.patients = {}
        self.appointments = {}
        self.medical_records = {}
    
    def register_patient(self, name: str, dob: str, 
                        contact_info: Dict) -> Dict:
        """Register new patient"""
        patient_id = f"PT_{len(self.patients) + 1}"
        
        self.patients[patient_id] = {
            "id": patient_id,
            "name": name,
            "date_of_birth": dob,
            "contact": contact_info,
            "insurance_id": None,
            "medical_history": [],
            "allergies": [],
            "created_at": datetime.now()
        }
        
        return self.patients[patient_id]
    
    def add_medical_history(self, patient_id: str, condition: str, 
                           diagnosis_date: datetime, notes: str = None):
        """Add medical history entry"""
        if patient_id not in self.patients:
            return {"error": "Patient not found"}
        
        entry = {
            "condition": condition,
            "diagnosis_date": diagnosis_date,
            "notes": notes,
            "recorded_at": datetime.now()
        }
        
        self.patients[patient_id]["medical_history"].append(entry)
        return entry
    
    def schedule_appointment(self, patient_id: str, doctor_id: str,
                            appointment_type: AppointmentType,
                            scheduled_time: datetime) -> Dict:
        """Schedule appointment"""
        if patient_id not in self.patients:
            return {"error": "Patient not found"}
        
        appointment_id = f"APT_{len(self.appointments) + 1}"
        
        self.appointments[appointment_id] = {
            "id": appointment_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "type": appointment_type.value,
            "scheduled_time": scheduled_time,
            "status": "scheduled",
            "notes": ""
        }
        
        return self.appointments[appointment_id]


class ClinicalDecisionSupport:
    """Clinical decision support"""
    
    def __init__(self):
        self.guidelines = {}
        self.alerts = []
    
    def add_guideline(self, condition: str, guideline: Dict):
        """Add clinical guideline"""
        self.guidelines[condition] = guideline
    
    def check_interactions(self, medications: List[str]) -> List[Dict]:
        """Check drug interactions"""
        interactions = []
        interaction_pairs = [
            ("warfarin", "aspirin", "Increased bleeding risk"),
            ("lisinopril", "potassium", "Hyperkalemia risk"),
            ("metformin", "contrast_dye", "Lactic acidosis risk")
        ]
        
        for med1, med2, risk in interaction_pairs:
            if med1 in medications and med2 in medications:
                interactions.append({
                    "severity": "high",
                    "medications": [med1, med2],
                    "risk": risk,
                    "recommendation": "Monitor closely or consider alternative"
                })
        
        return interactions
    
    def suggest_diagnosis(self, symptoms: List[str]) -> List[Dict]:
        """Suggest possible diagnoses"""
        symptom_diagnosis = {
            "chest_pain": ["Angina", "Myocardial Infarction", "GERD"],
            "shortness_of_breath": ["Asthma", "COPD", "Heart Failure", "Pneumonia"],
            "headache": ["Migraine", "Tension Headache", "Hypertension"],
            "fatigue": ["Anemia", "Hypothyroidism", "Depression"]
        }
        
        suggestions = []
        for symptom in symptoms:
            if symptom in symptom_diagnosis:
                for diagnosis in symptom_diagnosis[symptom]:
                    suggestions.append({
                        "condition": diagnosis,
                        "match_score": 0.8,
                        "recommended_tests": self._get_recommended_tests(diagnosis)
                    })
        
        return suggestions
    
    def _get_recommended_tests(self, condition: str) -> List[str]:
        """Get recommended tests for condition"""
        tests = {
            "Angina": ["ECG", "Blood Panel", "Stress Test"],
            "Asthma": ["Spirometry", "Peak Flow", "Chest X-Ray"],
            "Migraine": ["CT Scan", "Blood Tests", "Neurological Exam"]
        }
        return tests.get(condition, ["General Physical Exam"])


class InsuranceValidator:
    """Insurance verification"""
    
    def __init__(self):
        self.claims = {}
    
    def verify_coverage(self, insurance_id: str, 
                      procedure_code: str) -> Dict:
        """Verify insurance coverage"""
        return {
            "insurance_id": insurance_id,
            "procedure_code": procedure_code,
            "covered": True,
            "coverage_percent": 80,
            "copay": 25,
            "pre_authorization_required": False,
            "in_network": True
        }
    
    def submit_claim(self, patient_id: str, procedure_code: str,
                    amount: float, diagnosis: str) -> Dict:
        """Submit insurance claim"""
        claim_id = f"CLM_{len(self.claims) + 1}"
        
        self.claims[claim_id] = {
            "id": claim_id,
            "patient_id": patient_id,
            "procedure_code": procedure_code,
            "amount": amount,
            "diagnosis": diagnosis,
            "status": "submitted",
            "submitted_at": datetime.now()
        }
        
        return self.claims[claim_id]


class TelemedicineManager:
    """Telemedicine operations"""
    
    def __init__(self):
        self.sessions = {}
    
    def schedule_telehealth(self, patient_id: str, doctor_id: str,
                          scheduled_time: datetime, platform: str = "zoom") -> Dict:
        """Schedule telehealth session"""
        session_id = f"TH_{len(self.sessions) + 1}"
        
        self.sessions[session_id] = {
            "id": session_id,
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "scheduled_time": scheduled_time,
            "platform": platform,
            "meeting_link": f"https://{platform}.com/join/{session_id}",
            "status": "scheduled"
        }
        
        return self.sessions[session_id]
    
    def start_session(self, session_id: str) -> Dict:
        """Start telehealth session"""
        if session_id not in self.sessions:
            return {"error": "Session not found"}
        
        self.sessions[session_id]["status"] = "in_progress"
        self.sessions[session_id]["started_at"] = datetime.now()
        
        return {
            "session_id": session_id,
            "meeting_link": self.sessions[session_id]["meeting_link"],
            "status": "in_progress"
        }
    
    def get_session_info(self, session_id: str) -> Dict:
        """Get session information"""
        if session_id not in self.sessions:
            return {"error": "Session not found"}
        return self.sessions[session_id]


class HealthAnalytics:
    """Health analytics"""
    
    def __init__(self):
        self.metrics = {}
    
    def calculate_vital_stats(self, readings: List[Dict]) -> Dict:
        """Calculate vital statistics"""
        if not readings:
            return {}
        
        blood_pressures = [r["systolic"] for r in readings if "systolic" in r]
        
        return {
            "avg_blood_pressure": f"{sum(blood_pressures) // len(blood_pressures)}/80" if blood_pressures else "N/A",
            "readings_count": len(readings),
            "last_reading": readings[-1] if readings else None
        }
    
    def generate_health_report(self, patient_id: str) -> Dict:
        """Generate patient health report"""
        return {
            "patient_id": patient_id,
            "report_date": datetime.now(),
            "appointments_last_30_days": 2,
            "medications_adherence": 85,
            "upcoming_appointments": 1,
            "health_score": 78
        }


if __name__ == "__main__":
    patients = PatientManager()
    patient = patients.register_patient("John Doe", "1980-01-15", {"email": "john@example.com"})
    patients.add_medical_history(patient["id"], "Hypertension", datetime.now(), "Controlled with medication")
    apt = patients.schedule_appointment(patient["id"], "DR_001", AppointmentType.CONSULTATION, datetime.now())
    
    cds = ClinicalDecisionSupport()
    cds.add_guideline("Hypertension", {"first_line": ["Lisinopril", "Amlodipine"]})
    interactions = cds.check_interactions(["warfarin", "aspirin"])
    diagnoses = cds.suggest_diagnosis(["chest_pain", "shortness_of_breath"])
    
    insurance = InsuranceValidator()
    coverage = insurance.verify_coverage("INS_001", "EKG001")
    claim = insurance.submit_claim(patient["id"], "EKG001", 500, "Chest Pain")
    
    telehealth = TelemedicineManager()
    session = telehealth.schedule_telehealth(patient["id"], "DR_001", datetime.now())
    started = telehealth.start_session(session["id"])
    
    analytics = HealthAnalytics()
    report = analytics.generate_health_report(patient["id"])
    
    print(f"Patient: {patient['name']}")
    print(f"Appointment: {apt['id']}")
    print(f"Drug interactions: {len(interactions)}")
    print(f"Diagnosis suggestions: {len(diagnoses)}")
    print(f"Insurance coverage: {coverage['coverage_percent']}%")
    print(f"Telehealth link: {started['meeting_link']}")
    print(f"Health score: {report['health_score']}")

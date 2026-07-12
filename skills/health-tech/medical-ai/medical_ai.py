"""
Medical AI - Diagnostic Imaging, Clinical Decision Support, Drug Discovery, NLP
Comprehensive module covering core medical AI capabilities.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from typing import Any, Optional


# ─── Enums ────────────────────────────────────────────────────────────────────

class ImagingModality(Enum):
    """Radiological imaging modalities."""
    XRAY = "xray"
    CT = "ct"
    MRI = "mri"
    ULTRASOUND = "ultrasound"
    PET = "pet"
    MAMMOGRAPHY = "mammography"
    RETINAL = "retinal"


class PathologyClass(Enum):
    """Common pathology classifications for diagnostic imaging."""
    NORMAL = "normal"
    PNEUMONIA = "pneumonia"
    PNEUMOTHORAX = "pneumothorax"
    CARDIOMEGALY = "cardiomegaly"
    EFFUSION = "effusion"
    MASS = "mass"
    NODULE = "nodule"
    FRACTURE = "fracture"
    HEMORRHAGE = "hemorrhage"
    INFARCTION = "infarction"


class ClinicalUrgency(Enum):
    """Triage urgency levels for clinical findings."""
    ROUTINE = auto()
    URGENT = auto()
    EMERGENT = auto()
    CRITICAL = auto()


class DrugPhase(Enum):
    """Clinical trial phases for drug discovery."""
    DISCOVERY = "discovery"
    PRECLINICAL = "preclinical"
    PHASE_I = "phase_1"
    PHASE_II = "phase_2"
    PHASE_III = "phase_3"
    PHASE_IV = "phase_4"
    APPROVED = "approved"
    REJECTED = "rejected"


class EntityType(Enum):
    """Medical entity types for clinical NLP."""
    CONDITION = "condition"
    MEDICATION = "medication"
    PROCEDURE = "procedure"
    ANATOMY = "anatomy"
    LAB_TEST = "lab_test"
    TEMPORAL = "temporal"
    DOSAGE = "dosage"
    FREQUENCY = "frequency"
    SEVERITY = "severity"
    FAMILY_MEMBER = "family_member"


# ─── Dataclasses ──────────────────────────────────────────────────────────────

@dataclass
class ImageStudy:
    """Represents a single radiological image study."""
    study_id: str
    patient_id: str
    modality: ImagingModality
    body_part: str
    acquisition_date: datetime
    pixel_data_hash: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def anonymize(self) -> ImageStudy:
        """Return a de-identified copy of the study."""
        anon_id = hashlib.sha256(self.patient_id.encode()).hexdigest()[:16]
        return ImageStudy(
            study_id=self.study_id,
            patient_id=anon_id,
            modality=self.modality,
            body_part=self.body_part,
            acquisition_date=self.acquisition_date,
            pixel_data_hash=self.pixel_data_hash,
            metadata={k: v for k, v in self.metadata.items() if k != "patient_name"},
        )


@dataclass
class DiagnosticResult:
    """Output from an AI diagnostic imaging model."""
    result_id: str
    study_id: str
    pathology: PathologyClass
    confidence: float
    urgency: ClinicalUrgency
    bounding_boxes: list[dict[str, float]] = field(default_factory=list)
    heatmap_overlay_available: bool = False
    model_version: str = "1.0.0"
    generated_at: datetime = field(default_factory=datetime.utcnow)

    def is_critical(self) -> bool:
        return self.confidence >= 0.85 and self.urgency in (
            ClinicalUrgency.EMERGENT, ClinicalUrgency.CRITICAL
        )


@dataclass
class PatientContext:
    """Patient clinical context for decision support."""
    patient_id: str
    age: int
    sex: str
    conditions: list[str] = field(default_factory=list)
    medications: list[str] = field(default_factory=list)
    allergies: list[str] = field(default_factory=list)
    lab_results: dict[str, float] = field(default_factory=dict)
    vitals: dict[str, float] = field(default_factory=dict)


@dataclass
class ClinicalRecommendation:
    """A clinical decision support recommendation."""
    recommendation_id: str
    patient_id: str
    category: str
    description: str
    evidence_level: str
    confidence: float
    contraindications: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)


@dataclass
class DrugCandidate:
    """A potential drug candidate from discovery pipeline."""
    compound_id: str
    name: str
    molecular_formula: str
    molecular_weight: float
    target_protein: str
    phase: DrugPhase
    predicted_ic50: float
    admet_scores: dict[str, float] = field(default_factory=dict)
    synthetic_accessibility: float = 0.0

    def is_viable(self) -> bool:
        """Check if compound passes minimum viability thresholds."""
        return (
            self.predicted_ic50 < 100.0
            and self.admet_scores.get("oral_bioavailability", 0) > 0.3
            and self.admet_scores.get("toxicity", 1.0) < 0.5
            and self.molecular_weight < 900
        )


@dataclass
class ClinicalEntity:
    """An extracted entity from clinical text."""
    text: str
    entity_type: EntityType
    start_char: int
    end_char: int
    confidence: float
    normalized_code: str = ""
    normalized_system: str = ""


@dataclass
class ClinicalNote:
    """A clinical note for NLP processing."""
    note_id: str
    patient_id: str
    note_type: str
    text: str
    author: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)


# ─── Abstract Base Classes ────────────────────────────────────────────────────

class DiagnosticModel(ABC):
    """Abstract base class for diagnostic imaging models."""

    @abstractmethod
    def analyze(self, study: ImageStudy) -> DiagnosticResult:
        """Analyze an imaging study and return diagnostic results."""
        ...

    @abstractmethod
    def get_supported_modalities(self) -> list[ImagingModality]:
        """Return list of imaging modalities this model supports."""
        ...


class ClinicalNLPModel(ABC):
    """Abstract base class for clinical NLP models."""

    @abstractmethod
    def extract_entities(self, note: ClinicalNote) -> list[ClinicalEntity]:
        """Extract medical entities from clinical text."""
        ...

    @abstractmethod
    def get_supported_entity_types(self) -> list[EntityType]:
        """Return entity types this model can extract."""
        ...


class DrugDiscoveryModel(ABC):
    """Abstract base class for drug discovery models."""

    @abstractmethod
    def score_candidate(self, candidate: DrugCandidate) -> float:
        """Score a drug candidate's likelihood of success."""
        ...

    @abstractmethod
    def predict_admet(self, molecular_formula: str) -> dict[str, float]:
        """Predict ADMET properties from molecular formula."""
        ...


# ─── Concrete Implementations ─────────────────────────────────────────────────

class ChestXrayAnalyzer(DiagnosticModel):
    """AI model for chest X-ray diagnosis."""

    MODEL_VERSION = "2.3.1"
    CONFIDENCE_THRESHOLD = 0.5

    def __init__(self) -> None:
        self._supported = [ImagingModality.XRAY]
        self._pathology_rules: dict[PathologyClass, list[str]] = {
            PathologyClass.PNEUMONIA: ["consolidation", "infiltrate", "air_bronchogram"],
            PathologyClass.PNEUMOTHORAX: ["lucent_area", "absent_vascular_markings"],
            PathologyClass.CARDIOMEGALY: ["cardiothoracic_ratio_gt_0_5"],
            PathologyClass.EFFUSION: ["meniscus_sign", "blunted_costophrenic_angle"],
            PathologyClass.HEMORRHAGE: ["hyperdense_area", "mass_effect"],
        }

    def analyze(self, study: ImageStudy) -> DiagnosticResult:
        if study.modality not in self._supported:
            raise ValueError(f"Unsupported modality: {study.modality}")

        detected_features = study.metadata.get("detected_features", [])
        best_pathology = PathologyClass.NORMAL
        best_confidence = 0.95

        for pathology, features in self._pathology_rules.items():
            match_count = sum(1 for f in features if f in detected_features)
            if match_count > 0:
                confidence = min(0.99, 0.5 + (match_count / len(features)) * 0.45)
                if confidence > best_confidence:
                    best_confidence = confidence
                    best_pathology = pathology

        urgency = self._determine_urgency(best_pathology, best_confidence)

        return DiagnosticResult(
            result_id=f"DR-{uuid.uuid4().hex[:12]}",
            study_id=study.study_id,
            pathology=best_pathology,
            confidence=round(best_confidence, 4),
            urgency=urgency,
            heatmap_overlay_available=True,
            model_version=self.MODEL_VERSION,
        )

    def _determine_urgency(
        self, pathology: PathologyClass, confidence: float
    ) -> ClinicalUrgency:
        critical_pathologies = {PathologyClass.PNEUMOTHORAX, PathologyClass.HEMORRHAGE}
        urgent_pathologies = {PathologyClass.PNEUMONIA, PathologyClass.EFFUSION}

        if pathology in critical_pathologies and confidence > 0.8:
            return ClinicalUrgency.CRITICAL
        if pathology in critical_pathologies:
            return ClinicalUrgency.EMERGENT
        if pathology in urgent_pathologies and confidence > 0.7:
            return ClinicalUrgency.URGENT
        return ClinicalUrgency.ROUTINE

    def get_supported_modalities(self) -> list[ImagingModality]:
        return self._supported.copy()


class ClinicalDecisionEngine:
    """Rule-based and ML-driven clinical decision support system."""

    def __init__(self) -> None:
        self._drug_interactions: dict[tuple[str, str], str] = {
            ("warfarin", "aspirin"): "Increased bleeding risk — avoid combination",
            ("metformin", "contrast_dye"): "Hold metformin 48h before/after contrast",
            ("ssri", "maoi"): "Contraindicated — risk of serotonin syndrome",
            ("methotrexate", "nsaid"): "Increased methotrexate toxicity",
            ("lithium", "ace_inhibitor"): "Risk of lithium toxicity",
        }
        self._guidelines: dict[str, list[dict[str, Any]]] = {
            "hypertension": [
                {"step": 1, "drug": "lisinopril", "dose": "10mg daily"},
                {"step": 2, "drug": "lisinopril + amlodipine", "dose": "10mg + 5mg daily"},
                {"step": 3, "drug": "lisinopril + amlodipine + HCTZ", "dose": "10mg + 5mg + 12.5mg"},
            ],
            "diabetes_t2": [
                {"step": 1, "drug": "metformin", "dose": "500mg BID"},
                {"step": 2, "drug": "metformin + semaglutide", "dose": "1000mg + 0.25mg weekly"},
                {"step": 3, "drug": "metformin + semaglutide + empagliflozin", "dose": "titrate"},
            ],
        }

    def check_drug_interactions(
        self, medications: list[str]
    ) -> list[dict[str, str]]:
        """Check for known drug-drug interactions."""
        interactions = []
        normalized = [m.lower().strip() for m in medications]
        for i, drug_a in enumerate(normalized):
            for drug_b in normalized[i + 1:]:
                pair = (drug_a, drug_b)
                reverse_pair = (drug_b, drug_a)
                interaction = self._drug_interactions.get(pair) or self._drug_interactions.get(
                    reverse_pair
                )
                if interaction:
                    interactions.append({
                        "drug_a": drug_a,
                        "drug_b": drug_b,
                        "severity": "major",
                        "description": interaction,
                    })
        return interactions

    def get_treatment_guideline(
        self, condition: str, current_step: int
    ) -> Optional[dict[str, Any]]:
        """Retrieve next treatment step from clinical guidelines."""
        guidelines = self._guidelines.get(condition.lower())
        if not guidelines:
            return None
        next_step = current_step + 1
        for guideline in guidelines:
            if guideline["step"] == next_step:
                return guideline.copy()
        return None

    def generate_recommendations(
        self, context: PatientContext
    ) -> list[ClinicalRecommendation]:
        """Generate clinical recommendations based on patient context."""
        recommendations: list[ClinicalRecommendation] = []

        interactions = self.check_drug_interactions(context.medications)
        for interaction in interactions:
            recommendations.append(ClinicalRecommendation(
                recommendation_id=f"REC-{uuid.uuid4().hex[:8]}",
                patient_id=context.patient_id,
                category="drug_interaction",
                description=interaction["description"],
                evidence_level="Level A",
                confidence=0.95,
                contraindications=[interaction["drug_a"], interaction["drug_b"]],
            ))

        if context.age > 65:
            recommendations.append(ClinicalRecommendation(
                recommendation_id=f"REC-{uuid.uuid4().hex[:8]}",
                patient_id=context.patient_id,
                category="geriatric_caution",
                description="Elderly patient — consider dose adjustments and fall risk",
                evidence_level="Level B",
                confidence=0.85,
            ))

        cr_cl = self._estimate_crcl(context)
        if cr_cl < 30:
            recommendations.append(ClinicalRecommendation(
                recommendation_id=f"REC-{uuid.uuid4().hex[:8]}",
                patient_id=context.patient_id,
                category="renal_dose_adjustment",
                description=f"Estimated CrCl {cr_cl:.0f} mL/min — adjust renally cleared drugs",
                evidence_level="Level A",
                confidence=0.90,
            ))

        return recommendations

    def _estimate_crcl(self, ctx: PatientContext) -> float:
        """Estimate creatinine clearance using Cockcroft-Gault."""
        weight = ctx.vitals.get("weight_kg", 70.0)
        scr = ctx.lab_results.get("serum_creatinine", 1.0)
        age_factor = max(0, 140 - ctx.age)
        sex_factor = 0.85 if ctx.sex.lower() == "f" else 1.0
        return (age_factor * weight * sex_factor) / (72 * max(scr, 0.1))


class MoleculeGenerator(DrugDiscoveryModel):
    """Simplified drug discovery pipeline with scoring."""

    def __init__(self) -> None:
        self._target_library: dict[str, dict[str, Any]] = {
            "EGFR": {"mw_range": (350, 550), "logp_range": (2.0, 5.0)},
            "ACE2": {"mw_range": (200, 450), "logp_range": (1.0, 4.0)},
            "PD-L1": {"mw_range": (400, 800), "logp_range": (3.0, 6.0)},
        }

    def score_candidate(self, candidate: DrugCandidate) -> float:
        """Score a drug candidate on multiple dimensions."""
        scores: list[float] = []

        mw_score = self._score_molecular_weight(candidate.molecular_weight)
        scores.append(mw_score)

        ic50_score = max(0, 1.0 - (candidate.predicted_ic50 / 200.0))
        scores.append(ic50_score)

        admet_score = sum(candidate.admet_scores.values()) / max(
            len(candidate.admet_scores), 1
        )
        scores.append(admet_score)

        sa_score = candidate.synthetic_accessibility
        scores.append(sa_score)

        return round(sum(scores) / len(scores), 4)

    def _score_molecular_weight(self, mw: float) -> float:
        """Score based on Lipinski-like molecular weight rules."""
        if 150 <= mw <= 500:
            return 1.0
        if 500 < mw <= 700:
            return 0.6
        if mw < 150:
            return 0.3
        return 0.1

    def predict_admet(self, molecular_formula: str) -> dict[str, float]:
        """Predict ADMET properties from a molecular formula string."""
        length = len(molecular_formula)
        hash_val = int(hashlib.md5(molecular_formula.encode()).hexdigest()[:8], 16)

        def seeded_float(seed: int, low: float, high: float) -> float:
            return low + ((seed % 1000) / 1000.0) * (high - low)

        return {
            "absorption": round(seeded_float(hash_val, 0.4, 0.95), 3),
            "distribution": round(seeded_float(hash_val + 1, 0.3, 0.9), 3),
            "metabolism": round(seeded_float(hash_val + 2, 0.2, 0.8), 3),
            "excretion": round(seeded_float(hash_val + 3, 0.3, 0.85), 3),
            "toxicity": round(seeded_float(hash_val + 4, 0.05, 0.7), 3),
            "oral_bioavailability": round(seeded_float(hash_val + 5, 0.1, 0.9), 3),
        }

    def get_supported_modalities(self) -> list[ImagingModality]:
        return []


class ClinicalNLPEngine(ClinicalNLPModel):
    """NLP engine for extracting structured data from clinical notes."""

    _ENTITY_PATTERNS: dict[EntityType, list[str]] = {
        EntityType.MEDICATION: [
            r"\b(aspirin|metformin|lisinopril|warfarin|amoxicillin|ibuprofen|"
            r"omeprazole|atorvastatin|metoprolol|amlodipine|prednisone|"
            r"azithromycin|hydrochlorothiazide|gabapentin|pantoprazole)\b"
        ],
        EntityType.CONDITION: [
            r"\b(hypertension|diabetes|pneumonia|atrial fibrillation|"
            r"congestive heart failure|COPD|asthma|hypothyroidism|"
            r"chronic kidney disease|anemia|depression|obesity)\b"
        ],
        EntityType.PROCEDURE: [
            r"\b(Chest X-Ray|CT scan|MRI|echocardiogram|colonoscopy|"
            r"endoscopy|biopsy|surgery|catheterization|dialysis)\b"
        ],
        EntityType.LAB_TEST: [
            r"\b(HbA1c|CBC|BMP|CMP|TSH|LDL|HDL|creatinine|BUN|"
            r"hemoglobin|platelet|WBC|INR|PTT|troponin|BNP)\b"
        ],
        EntityType.ANATOMY: [
            r"\b(heart|lungs|liver|kidney|brain|colon|pancreas|"
            r"thyroid|prostate|breast|spleen|gallbladder)\b"
        ],
        EntityType.TEMPORAL: [
            r"\b(today|yesterday|last week|last month|2 weeks ago|"
            r"3 months ago|6 months|1 year|since yesterday|recently)\b"
        ],
    }

    _SEVERITY_PATTERNS: list[str] = [
        r"\b(mild|moderate|severe|acute|chronic|critical|stable|unstable)\b"
    ]

    def __init__(self) -> None:
        self._compiled_patterns: dict[EntityType, list[re.Pattern[str]]] = {}
        for etype, patterns in self._ENTITY_PATTERNS.items():
            self._compiled_patterns[etype] = [
                re.compile(p, re.IGNORECASE) for p in patterns
            ]
        self._severity_patterns = [
            re.compile(p, re.IGNORECASE) for p in self._SEVERITY_PATTERNS
        ]

    def extract_entities(self, note: ClinicalNote) -> list[ClinicalEntity]:
        """Extract medical entities from clinical note text."""
        entities: list[ClinicalEntity] = []
        seen_spans: set[tuple[int, int]] = set()

        for etype, compiled in self._compiled_patterns.items():
            for pattern in compiled:
                for match in pattern.finditer(note.text):
                    span = (match.start(), match.end())
                    if span not in seen_spans:
                        seen_spans.add(span)
                        confidence = 0.85 + (hash(match.group()) % 15) / 100.0
                        entities.append(ClinicalEntity(
                            text=match.group(),
                            entity_type=etype,
                            start_char=match.start(),
                            end_char=match.end(),
                            confidence=round(confidence, 3),
                        ))

        for pattern in self._severity_patterns:
            for match in pattern.finditer(note.text):
                span = (match.start(), match.end())
                if span not in seen_spans:
                    seen_spans.add(span)
                    entities.append(ClinicalEntity(
                        text=match.group(),
                        entity_type=EntityType.SEVERITY,
                        start_char=match.start(),
                        end_char=match.end(),
                        confidence=0.90,
                    ))

        return sorted(entities, key=lambda e: e.start_char)

    def deidentify(self, note: ClinicalNote) -> ClinicalNote:
        """Remove PHI from clinical note text."""
        phi_patterns = [
            (r"\b\d{3}-\d{2}-\d{4}\b", "[SSN_REDACTED]"),
            (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", "[EMAIL_REDACTED]"),
            (r"\b\d{1,2}/\d{1,2}/\d{2,4}\b", "[DATE_REDACTED]"),
            (r"\b\d{3}[\s.-]\d{3}[\s.-]\d{4}\b", "[PHONE_REDACTED]"),
        ]
        deidentified_text = note.text
        for pattern, replacement in phi_patterns:
            deidentified_text = re.sub(pattern, replacement, deidentified_text)

        return ClinicalNote(
            note_id=note.note_id,
            patient_id=hashlib.sha256(note.patient_id.encode()).hexdigest()[:16],
            note_type=note.note_type,
            text=deidentified_text,
            author="[REDACTED]",
            created_at=note.created_at,
        )

    def get_supported_entity_types(self) -> list[EntityType]:
        return list(self._ENTITY_PATTERNS.keys()) + [EntityType.SEVERITY]

    def summarize(self, note: ClinicalNote) -> dict[str, Any]:
        """Generate a structured summary from a clinical note."""
        entities = self.extract_entities(note)
        by_type: dict[str, list[str]] = {}
        for entity in entities:
            key = entity.entity_type.value
            by_type.setdefault(key, []).append(entity.text)

        return {
            "note_id": note.note_id,
            "note_type": note.note_type,
            "entity_counts": {k: len(v) for k, v in by_type.items()},
            "entities": by_type,
            "text_length": len(note.text),
            "word_count": len(note.text.split()),
        }


# ─── Pipeline Orchestrator ────────────────────────────────────────────────────

class MedicalAIPipeline:
    """Orchestrates multiple medical AI components."""

    def __init__(self) -> None:
        self.imaging = ChestXrayAnalyzer()
        self.decision_engine = ClinicalDecisionEngine()
        self.drug_model = MoleculeGenerator()
        self.nlp_engine = ClinicalNLPEngine()

    def full_diagnostic_workup(
        self,
        study: ImageStudy,
        patient_context: PatientContext,
        clinical_note: Optional[ClinicalNote] = None,
    ) -> dict[str, Any]:
        """Run a complete diagnostic workup combining all AI modules."""
        results: dict[str, Any] = {"workup_id": f"WU-{uuid.uuid4().hex[:10]}"}

        diagnostic = self.imaging.analyze(study)
        results["imaging"] = {
            "pathology": diagnostic.pathology.value,
            "confidence": diagnostic.confidence,
            "urgency": diagnostic.urgency.name,
        }

        recommendations = self.decision_engine.generate_recommendations(patient_context)
        results["recommendations"] = [
            {
                "category": r.category,
                "description": r.description,
                "confidence": r.confidence,
            }
            for r in recommendations
        ]

        if clinical_note:
            nlp_result = self.nlp_engine.summarize(clinical_note)
            results["nlp_summary"] = nlp_result

        return results


# ─── Demo ─────────────────────────────────────────────────────────────────────

def main() -> None:
    """Demonstrate Medical AI capabilities."""
    print("=" * 70)
    print("MEDICAL AI DEMONSTRATION")
    print("=" * 70)

    # 1. Diagnostic Imaging
    print("\n── 1. DIAGNOSTIC IMAGING ──")
    analyzer = ChestXrayAnalyzer()
    study = ImageStudy(
        study_id="STUDY-001",
        patient_id="PATIENT-12345",
        modality=ImagingModality.XRAY,
        body_part="chest",
        acquisition_date=datetime.now(),
        metadata={"detected_features": ["consolidation", "infiltrate", "air_bronchogram"]},
    )
    result = analyzer.analyze(study)
    print(f"  Study: {study.study_id} | Modality: {study.modality.value}")
    print(f"  Finding: {result.pathology.value} | Confidence: {result.confidence:.2%}")
    print(f"  Urgency: {result.urgency.name} | Critical: {result.is_critical()}")
    print(f"  Supported modalities: {[m.value for m in analyzer.get_supported_modalities()]}")

    # Anonymize study
    anon_study = study.anonymize()
    print(f"  Anonymized patient ID: {anon_study.patient_id}")

    # 2. Clinical Decision Support
    print("\n── 2. CLINICAL DECISION SUPPORT ──")
    engine = ClinicalDecisionEngine()
    context = PatientContext(
        patient_id="PATIENT-12345",
        age=72,
        sex="M",
        conditions=["hypertension", "diabetes"],
        medications=["warfarin", "aspirin", "lisinopril"],
        lab_results={"serum_creatinine": 1.8},
        vitals={"weight_kg": 82.0, "bp_systolic": 155, "bp_diastolic": 92},
    )

    interactions = engine.check_drug_interactions(context.medications)
    print(f"  Drug interactions found: {len(interactions)}")
    for inter in interactions:
        print(f"    ⚠ {inter['drug_a']} + {inter['drug_b']}: {inter['description']}")

    guideline = engine.get_treatment_guideline("hypertension", current_step=1)
    print(f"  Next hypertension step: {guideline}")

    recs = engine.generate_recommendations(context)
    print(f"  Total recommendations: {len(recs)}")
    for rec in recs:
        print(f"    [{rec.category}] {rec.description}")

    # 3. Drug Discovery
    print("\n── 3. DRUG DISCOVERY ──")
    drug_model = MoleculeGenerator()
    candidate = DrugCandidate(
        compound_id="CMPD-001",
        name="ExperimentalKinase-42",
        molecular_formula="C22H28N4O5S",
        molecular_weight=460.55,
        target_protein="EGFR",
        phase=DrugPhase.PHASE_I,
        predicted_ic50=12.5,
        admet_scores={
            "absorption": 0.78,
            "distribution": 0.65,
            "metabolism": 0.45,
            "excretion": 0.72,
            "toxicity": 0.22,
            "oral_bioavailability": 0.61,
        },
        synthetic_accessibility=0.70,
    )
    score = drug_model.score_candidate(candidate)
    admet = drug_model.predict_admet(candidate.molecular_formula)
    print(f"  Compound: {candidate.name} | Target: {candidate.target_protein}")
    print(f"  MW: {candidate.molecular_weight} | IC50: {candidate.predicted_ic50} nM")
    print(f"  Viability: {candidate.is_viable()} | Score: {score:.4f}")
    print(f"  ADMET: {json.dumps(admet, indent=4)}")

    # 4. Clinical NLP
    print("\n── 4. CLINICAL NLP ──")
    nlp = ClinicalNLPEngine()
    note = ClinicalNote(
        note_id="NOTE-9001",
        patient_id="PATIENT-12345",
        note_type="progress",
        text=(
            "Patient is a 72-year-old male with hypertension and diabetes presenting "
            "with moderate chest pain. Current medications include warfarin, aspirin, "
            "and lisinopril. Chest X-Ray shows consolidation in right lower lobe consistent "
            "with pneumonia. HbA1c is elevated at 8.2%. Plan: start azithromycin 500mg daily "
            "for 5 days, hold metformin before CT scan scheduled for next week."
        ),
        author="Dr. Smith",
    )
    entities = nlp.extract_entities(note)
    print(f"  Entities extracted: {len(entities)}")
    for entity in entities:
        print(f"    [{entity.entity_type.value:12}] '{entity.text}' (conf: {entity.confidence:.2f})")

    summary = nlp.summarize(note)
    print(f"  Summary: {json.dumps(summary['entity_counts'], indent=4)}")

    deidentified = nlp.deidentify(note)
    print(f"  De-identified patient: {deidentified.patient_id}")
    print(f"  De-identified author: {deidentified.author}")

    # 5. Full Pipeline Workup
    print("\n── 5. FULL DIAGNOSTIC WORKUP ──")
    pipeline = MedicalAIPipeline()
    workup = pipeline.full_diagnostic_workup(study, context, note)
    print(f"  Workup ID: {workup['workup_id']}")
    print(f"  Imaging: {json.dumps(workup['imaging'], indent=4)}")
    print(f"  Recommendations: {len(workup['recommendations'])}")
    print(f"  NLP entities: {workup.get('nlp_summary', {}).get('entity_counts', {})}")

    print("\n" + "=" * 70)
    print("MEDICAL AI DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()

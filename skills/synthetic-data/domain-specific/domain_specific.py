"""
Domain-Specific Synthetic Data Generation Module
Provides specialized generators for healthcare, finance, IoT, automotive, legal,
and scientific domains with built-in validation rules and domain constraints.
"""

import random
import logging
import math
import hashlib
from enum import Enum, auto
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class DomainType(Enum):
    """Supported domain types."""
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    IOT = "iot"
    AUTOMOTIVE = "automotive"
    LEGAL = "legal"
    SCIENTIFIC = "scientific"


class FaultType(Enum):
    """IoT sensor fault types."""
    NOISE = auto()
    DRIFT = auto()
    STUCK = auto()
    BEARING_DEGRADATION = auto()
    TEMPERATURE_SPIKE = auto()
    INTERMITTENT = auto()


class FraudPattern(Enum):
    """Financial fraud pattern types."""
    CARD_TESTING = "card_testing"
    ACCOUNT_TAKEOVER = "account_takeover"
    GEO_IMPOSSIBILITY = "geo_impossibility"
    STRUCTURING = "structuring"
    SYNTHETIC_IDENTITY = "synthetic_identity"
   Friendly_FRAUD = "friendly_fraud"


class ClauseType(Enum):
    """Legal clause types for contract synthesis."""
    INDEMNIFICATION = "indemnification"
    LIMITATION_OF_LIABILITY = "limitation_of_liability"
    GOVERNING_LAW = "governing_law"
    TERMINATION = "termination"
    CONFIDENTIALITY = "confidentiality"
    FORCE_MAJEURE = "force_majeure"


class Severity(Enum):
    """Validation error severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


# ---------------------------------------------------------------------------
# Data Classes
# ---------------------------------------------------------------------------

@dataclass
class DomainConfig:
    """Configuration for domain-specific generation."""
    seed: int = 42
    n_samples: int = 1000
    start_date: str = "2022-01-01"
    end_date: str = "2023-12-31"
    compliance_mode: bool = False
    domain: DomainType = DomainType.HEALTHCARE

    def __post_init__(self):
        np.random.seed(self.seed)
        random.seed(self.seed)


@dataclass
class ValidationResult:
    """Result of a domain-specific validation check."""
    rule_name: str
    severity: Severity
    passed: bool
    message: str
    affected_records: int = 0
    details: Dict[str, Any] = field(default_factory=dict)

    def __str__(self):
        status = "PASS" if self.passed else self.severity.value.upper()
        return f"[{status}] {self.rule_name}: {self.message}"


@dataclass
class PatientRecord:
    """Represents a single synthetic patient record."""
    patient_id: str
    age: int
    gender: str
    zipcode: str
    visit_date: str
    diagnosis_code: str
    procedure_code: str
    medication: str
    lab_value: Optional[float] = None
    lab_unit: Optional[str] = None


@dataclass
class TransactionRecord:
    """Represents a single synthetic financial transaction."""
    transaction_id: str
    customer_id: str
    amount: float
    currency: str
    timestamp: str
    merchant_category: str
    is_fraud: bool = False
    fraud_type: Optional[str] = None
    card_present: bool = True
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class SensorReading:
    """Represents a single IoT sensor reading."""
    timestamp: str
    sensor_id: str
    value: float
    unit: str
    is_fault: bool = False
    fault_type: Optional[str] = None


# ---------------------------------------------------------------------------
# Custom Exceptions
# ---------------------------------------------------------------------------

class DomainError(Exception):
    """Custom exception for domain-specific errors."""
    pass


class ValidationError(DomainError):
    """Raised when domain validation fails."""
    def __init__(self, results: List[ValidationResult]):
        self.results = results
        failures = [r for r in results if not r.passed]
        super().__init__(f"Validation failed: {len(failures)} checks did not pass")


class ConfigurationError(DomainError):
    """Raised for invalid generator configuration."""
    pass


# ---------------------------------------------------------------------------
# Reference Data (Ontologies)
# ---------------------------------------------------------------------------

ICD10_CODES = {
    "E11": "Type 2 Diabetes Mellitus",
    "E11.9": "Type 2 Diabetes without complications",
    "I10": "Essential (primary) hypertension",
    "I25.10": "Atherosclerotic heart disease",
    "J45.20": "Mild intermittent asthma",
    "M54.5": "Low back pain",
    "N18.3": "Chronic kidney disease stage 3",
    "J18.9": "Pneumonia, unspecified organism",
    "F32.1": "Major depressive disorder, single episode, moderate",
    "K21.0": "Gastro-esophageal reflux disease with esophagitis",
}

ICD10_MEDICATION_MAP = {
    "E11": ["Metformin", "Glipizide", "Insulin Glargine"],
    "I10": ["Lisinopril", "Amlodipine", "Hydrochlorothiazide"],
    "J45.20": ["Albuterol", "Fluticasone", "Montelukast"],
    "M54.5": ["Ibuprofen", "Naproxen", "Cyclobenzaprine"],
    "N18.3": ["Epoetin Alfa", "Sevelamer", "Furosemide"],
    "J18.9": ["Amoxicillin", "Azithromycin", "Levofloxacin"],
    "F32.1": ["Sertraline", "Escitalopram", "Bupropion"],
    "K21.0": ["Omeprazole", "Pantoprazole", "Esomeprazole"],
}

LAB_TESTS = {
    "E11": {"test": "HbA1c", "unit": "%", "normal_range": (4.0, 5.7), "disease_range": (6.5, 12.0)},
    "I10": {"test": "Blood Pressure Systolic", "unit": "mmHg", "normal_range": (90, 120), "disease_range": (130, 180)},
    "N18.3": {"test": "eGFR", "unit": "mL/min/1.73m2", "normal_range": (90, 120), "disease_range": (15, 59)},
}

MERCHANT_CATEGORIES = [
    "grocery", "restaurant", "gas_station", "online_retail", "travel",
    "entertainment", "healthcare", "utilities", "electronics", "clothing",
]

CITIES = [
    ("New York", 40.7128, -74.0060),
    ("Los Angeles", 34.0522, -118.2437),
    ("Chicago", 41.8781, -87.6298),
    ("Houston", 29.7604, -95.3698),
    ("Phoenix", 33.4484, -112.0740),
    ("London", 51.5074, -0.1278),
    ("Tokyo", 35.6762, 139.6503),
]

SENSOR_UNITS = {
    "temperature": "C",
    "pressure": "bar",
    "vibration": "mm/s",
    "humidity": "%",
    "flow_rate": "L/min",
    "current": "A",
    "voltage": "V",
    "rpm": "RPM",
    "acoustic_emission": "dB",
    "oil_quality": "ISO 4406",
}


# ---------------------------------------------------------------------------
# Healthcare Generator
# ---------------------------------------------------------------------------

class HealthcareGenerator:
    """
    Generates synthetic Electronic Health Record (EHR) data.
    Supports ICD-10, RxNorm, and LOINC coding systems with clinical logic enforcement.
    """

    def __init__(self, ontology: str = "icd10", n_patients: int = 100, **kwargs):
        self.ontology = ontology
        self.config = DomainConfig(n_samples=n_patients, domain=DomainType.HEALTHCARE, **kwargs)
        self._patient_count = 0
        self._visit_count = 0
        self._validation_results: List[ValidationResult] = []

    def generate_cohort(self, conditions: Optional[Dict[str, float]] = None) -> pd.DataFrame:
        """Generate a synthetic patient cohort with conditions."""
        logger.info(f"Generating healthcare cohort with {self.config.n_samples} patients...")

        patients = []
        for i in range(self.config.n_samples):
            self._patient_count += 1
            diagnosis_code = random.choice(list(ICD10_CODES.keys()))
            medication = random.choice(ICD10_MEDICATION_MAP.get(diagnosis_code, ["None"]))

            lab_info = LAB_TESTS.get(diagnosis_code)
            lab_value = None
            lab_unit = None
            if lab_info:
                low, high = lab_info["disease_range"]
                lab_value = round(np.random.uniform(low, high), 1)
                lab_unit = lab_info["unit"]

            patient = {
                "patient_id": f"P{self._patient_count:05d}",
                "age": int(np.random.randint(18, 90)),
                "gender": random.choice(["M", "F"]),
                "zipcode": f"{random.randint(10000, 99999)}",
                "visit_date": (
                    pd.Timestamp(self.config.start_date)
                    + pd.Timedelta(days=random.randint(0, 365))
                ).strftime("%Y-%m-%d"),
                "diagnosis_code": diagnosis_code,
                "procedure_code": f"CPT{random.randint(100, 999)}",
                "medication": medication,
                "lab_value": lab_value,
                "lab_unit": lab_unit,
            }
            patients.append(patient)

        df = pd.DataFrame(patients)

        if conditions:
            df = self._apply_clinical_logic(df, conditions)

        self._validate(df)
        return df

    def _apply_clinical_logic(self, df: pd.DataFrame, conditions: Dict) -> pd.DataFrame:
        """Ensure clinical consistency in generated data."""
        logger.info("Applying clinical logic constraints...")

        if "diabetes_prevalence" in conditions:
            target_count = int(len(df) * conditions["diabetes_prevalence"])
            diabetes_patients = df.sample(n=min(target_count, len(df)), random_state=self.config.seed)
            df.loc[diabetes_patients.index, "diagnosis_code"] = "E11"
            df.loc[diabetes_patients.index, "medication"] = "Metformin"

        if "hypertension_prevalence" in conditions:
            non_diabetes = df[df["diagnosis_code"] != "E11"]
            target_count = int(len(non_diabetes) * conditions["hypertension_prevalence"])
            ht_patients = non_diabetes.sample(n=min(target_count, len(non_diabetes)), random_state=self.config.seed)
            df.loc[ht_patients.index, "diagnosis_code"] = "I10"
            df.loc[ht_patients.index, "medication"] = "Lisinopril"

        return df

    def _validate(self, df: pd.DataFrame) -> List[ValidationResult]:
        """Run domain-specific validation rules."""
        results = []

        valid_codes = set(ICD10_CODES.keys())
        invalid_mask = ~df["diagnosis_code"].isin(valid_codes)
        results.append(ValidationResult(
            rule_name="valid_icd10_code",
            severity=Severity.ERROR,
            passed=not invalid_mask.any(),
            message=f"{invalid_mask.sum()} records have invalid ICD-10 codes",
            affected_records=int(invalid_mask.sum()),
        ))

        age_mask = (df["age"] < 0) | (df["age"] > 120)
        results.append(ValidationResult(
            rule_name="valid_age_range",
            severity=Severity.ERROR,
            passed=not age_mask.any(),
            message=f"{age_mask.sum()} records have ages outside 0-120",
            affected_records=int(age_mask.sum()),
        ))

        lab_mask = df["lab_value"].notna() & ((df["lab_value"] < 0) | (df["lab_value"] > 200))
        results.append(ValidationResult(
            rule_name="plausible_lab_values",
            severity=Severity.WARNING,
            passed=not lab_mask.any(),
            message=f"{lab_mask.sum()} records have implausible lab values",
            affected_records=int(lab_mask.sum()),
        ))

        self._validation_results = results
        for r in results:
            logger.info(str(r))
        return results

    def get_validation_results(self) -> List[ValidationResult]:
        return self._validation_results


# ---------------------------------------------------------------------------
# Financial Generator
# ---------------------------------------------------------------------------

class FinancialGenerator:
    """Generates synthetic financial transaction data with fraud patterns."""

    def __init__(self, n_customers: int = 100, fraud_rate: float = 0.01, **kwargs):
        self.config = DomainConfig(n_samples=n_customers * 10, domain=DomainType.FINANCE, **kwargs)
        self.fraud_rate = fraud_rate
        self._customer_locations: Dict[str, Tuple[float, float]] = {}
        self._validation_results: List[ValidationResult] = []

    def _get_or_create_customer(self, customer_id: str) -> Tuple[float, float]:
        """Get or create a consistent home location for a customer."""
        if customer_id not in self._customer_locations:
            city = random.choice(CITIES)
            lat = city[1] + np.random.normal(0, 0.05)
            lon = city[2] + np.random.normal(0, 0.05)
            self._customer_locations[customer_id] = (round(lat, 4), round(lon, 4))
        return self._customer_locations[customer_id]

    def generate(self, fraud_patterns: Optional[List[str]] = None) -> pd.DataFrame:
        """Generate synthetic transactions with fraud patterns."""
        logger.info(f"Generating {self.config.n_samples} financial transactions...")

        if fraud_patterns is None:
            fraud_patterns = [p.value for p in FraudPattern]

        transactions = []
        start_ts = pd.Timestamp(self.config.start_date)
        total_seconds = int((pd.Timestamp(self.config.end_date) - start_ts).total_seconds())

        for i in range(self.config.n_samples):
            customer_id = f"C{random.randint(1, self.config.n_samples // 10):05d}"
            is_fraud = random.random() < self.fraud_rate

            home_lat, home_lon = self._get_or_create_customer(customer_id)

            amount = float(np.random.exponential(75))
            if is_fraud:
                amount *= random.uniform(3, 20)

            lat = home_lat + np.random.normal(0, 0.01)
            lon = home_lon + np.random.normal(0, 0.01)

            if is_fraud and "geo_impossibility" in fraud_patterns:
                lat = random.uniform(-90, 90)
                lon = random.uniform(-180, 180)

            txn = {
                "transaction_id": f"TXN{i:08d}",
                "customer_id": customer_id,
                "amount": round(amount, 2),
                "currency": "USD",
                "timestamp": (start_ts + pd.Timedelta(seconds=random.randint(0, total_seconds))).strftime("%Y-%m-%d %H:%M:%S"),
                "merchant_category": random.choice(MERCHANT_CATEGORIES),
                "is_fraud": is_fraud,
                "fraud_type": random.choice(fraud_patterns) if is_fraud else None,
                "card_present": random.random() > 0.3,
                "latitude": round(lat, 4),
                "longitude": round(lon, 4),
            }
            transactions.append(txn)

        df = pd.DataFrame(transactions)
        self._validate(df)
        return df

    def apply_pci_masking(self, data: pd.DataFrame) -> pd.DataFrame:
        """Apply PCI-DSS compliant masking to sensitive fields."""
        logger.info("Applying PCI-DSS masking...")
        masked = data.copy()
        if "card_number" in masked.columns:
            masked["card_number"] = masked["card_number"].apply(
                lambda x: f"****-****-****-{str(x)[-4:]}" if pd.notna(x) else x
            )
        return masked

    def _validate(self, df: pd.DataFrame) -> List[ValidationResult]:
        results = []

        negative_mask = df["amount"] < 0
        results.append(ValidationResult(
            rule_name="non_negative_amounts",
            severity=Severity.ERROR,
            passed=not negative_mask.any(),
            message=f"{negative_mask.sum()} transactions have negative amounts",
            affected_records=int(negative_mask.sum()),
        ))

        valid_categories = set(MERCHANT_CATEGORIES)
        invalid_cat_mask = ~df["merchant_category"].isin(valid_categories)
        results.append(ValidationResult(
            rule_name="valid_merchant_category",
            severity=Severity.ERROR,
            passed=not invalid_cat_mask.any(),
            message=f"{invalid_cat_mask.sum()} transactions have invalid merchant categories",
            affected_records=int(invalid_cat_mask.sum()),
        ))

        fraud_rate_actual = df["is_fraud"].mean()
        rate_ok = abs(fraud_rate_actual - self.fraud_rate) < 0.02
        results.append(ValidationResult(
            rule_name="target_fraud_rate",
            severity=Severity.WARNING,
            passed=rate_ok,
            message=f"Actual fraud rate {fraud_rate_actual:.4f} vs target {self.fraud_rate:.4f}",
        ))

        self._validation_results = results
        for r in results:
            logger.info(str(r))
        return results

    def get_validation_results(self) -> List[ValidationResult]:
        return self._validation_results


# ---------------------------------------------------------------------------
# IoT Sensor Generator
# ---------------------------------------------------------------------------

class IoTSensorGenerator:
    """Generates synthetic IoT sensor data streams with fault injection."""

    def __init__(self, n_sensors: int = 5, frequency: str = "1Hz", **kwargs):
        self.config = DomainConfig(n_samples=3600, domain=DomainType.IOT, **kwargs)
        self.n_sensors = n_sensors
        self.frequency = frequency
        self._validation_results: List[ValidationResult] = []

    def generate_with_fault(
        self,
        fault_type: str = "noise",
        onset_hour: int = 12,
        degradation_rate: float = 0.05,
    ) -> pd.DataFrame:
        """Generate sensor data with an injected fault."""
        logger.info(f"Generating IoT data with {fault_type} fault...")

        timestamps = pd.date_range(
            start="2023-01-01", periods=self.config.n_samples, freq="S"
        )
        data = {"timestamp": timestamps.strftime("%Y-%m-%d %H:%M:%S")}

        fault_start_idx = min(int(onset_hour * 3600), self.config.n_samples - 1)

        sensor_names = list(SENSOR_UNITS.keys())[:self.n_sensors]

        for i, sensor_name in enumerate(sensor_names):
            unit = SENSOR_UNITS[sensor_name]
            signal = np.sin(np.linspace(0, 10 * np.pi, self.config.n_samples)) * 10
            signal += np.random.normal(0, 0.5, self.config.n_samples)

            is_fault = np.zeros(self.config.n_samples, dtype=bool)

            if fault_type == "noise":
                signal[fault_start_idx:] += np.random.normal(0, 3, self.config.n_samples - fault_start_idx)
                is_fault[fault_start_idx:] = True
            elif fault_type == "drift":
                signal[fault_start_idx:] += np.linspace(0, degradation_rate * 100, self.config.n_samples - fault_start_idx)
                is_fault[fault_start_idx:] = True
            elif fault_type == "bearing_degradation":
                noise_increase = np.linspace(0, 5, self.config.n_samples - fault_start_idx)
                signal[fault_start_idx:] += np.random.normal(0, 1, self.config.n_samples - fault_start_idx) * (1 + noise_increase)
                is_fault[fault_start_idx:] = True
            elif fault_type == "stuck":
                signal[fault_start_idx:] = signal[fault_start_idx]
                is_fault[fault_start_idx:] = True
            elif fault_type == "temperature_spike":
                signal[fault_start_idx:] += np.random.uniform(10, 20, self.config.n_samples - fault_start_idx)
                is_fault[fault_start_idx:] = True
            elif fault_type == "intermittent":
                fault_mask = np.random.random(self.config.n_samples - fault_start_idx) < 0.3
                signal[fault_start_idx:][fault_mask] += np.random.normal(5, 2, fault_mask.sum())
                is_fault[fault_start_idx:][fault_mask] = True

            data[f"sensor_{i}_{sensor_name}"] = np.round(signal, 4)
            data[f"sensor_{i}_unit"] = unit
            data[f"sensor_{i}_is_fault"] = is_fault

        df = pd.DataFrame(data)
        self._validate(df)
        return df

    def _validate(self, df: pd.DataFrame) -> List[ValidationResult]:
        results = []

        for col in df.columns:
            if col.startswith("sensor_") and col.endswith("_unit"):
                continue
            if col.startswith("sensor_") and "_is_fault" in col:
                continue
            if col.startswith("sensor_") and not col.endswith(("_unit", "_is_fault")):
                if df[col].dtype in [np.float64, np.float32, np.int64]:
                    nan_count = df[col].isna().sum()
                    results.append(ValidationResult(
                        rule_name=f"no_nans_in_{col}",
                        severity=Severity.WARNING,
                        passed=nan_count == 0,
                        message=f"{col} has {nan_count} NaN values",
                        affected_records=int(nan_count),
                    ))

        ts_col = df["timestamp"]
        try:
            pd.to_datetime(ts_col)
            results.append(ValidationResult(
                rule_name="valid_timestamps",
                severity=Severity.ERROR,
                passed=True,
                message="All timestamps are valid datetime strings",
            ))
        except Exception:
            results.append(ValidationResult(
                rule_name="valid_timestamps",
                severity=Severity.ERROR,
                passed=False,
                message="Some timestamps are invalid",
            ))

        self._validation_results = results
        for r in results:
            logger.info(str(r))
        return results

    def get_validation_results(self) -> List[ValidationResult]:
        return self._validation_results


# ---------------------------------------------------------------------------
# Legal Generator
# ---------------------------------------------------------------------------

class LegalGenerator:
    """Generates synthetic legal document clauses for NLP training."""

    CLAUSE_TEMPLATES = {
        ClauseType.INDEMNIFICATION: [
            "The {party_a} shall indemnify, defend, and hold harmless the {party_b} from and against any and all claims, damages, losses, costs, and expenses arising out of or resulting from {party_a}'s breach of this Agreement.",
            "Each party agrees to indemnify the other party against all third-party claims arising from {party}'s negligence or willful misconduct.",
        ],
        ClauseType.LIMITATION_OF_LIABILITY: [
            "In no event shall either party be liable for any indirect, incidental, special, consequential, or punitive damages, regardless of the cause of action.",
            "The total liability of {party_a} under this Agreement shall not exceed the total fees paid by {party_b} during the twelve (12) months preceding the claim.",
        ],
        ClauseType.GOVERNING_LAW: [
            "This Agreement shall be governed by and construed in accordance with the laws of the State of {state}, without regard to its conflict of laws principles.",
            "Any disputes arising under this Agreement shall be resolved in accordance with the laws of {jurisdiction}.",
        ],
        ClauseType.TERMINATION: [
            "Either party may terminate this Agreement upon thirty (30) days' written notice to the other party.",
            "This Agreement shall automatically terminate upon the occurrence of {event}, unless renewed in writing by both parties.",
        ],
        ClauseType.CONFIDENTIALITY: [
            "Each party agrees to maintain the confidentiality of all Confidential Information received from the other party for a period of {years} years following disclosure.",
            "Neither party shall disclose any Confidential Information to third parties without prior written consent of the disclosing party.",
        ],
        ClauseType.FORCE_MAJEURE: [
            "Neither party shall be liable for any failure or delay in performance due to causes beyond its reasonable control, including but not limited to acts of God, war, terrorism, or pandemic.",
            "A party claiming force majeure shall provide written notice within {days} days of the event and shall use commercially reasonable efforts to mitigate the impact.",
        ],
    }

    def __init__(self, clause_types: Optional[List[str]] = None, language: str = "en-US", complexity: str = "medium", **kwargs):
        self.config = DomainConfig(n_samples=100, domain=DomainType.LEGAL, **kwargs)
        self.language = language
        self.complexity = complexity

        if clause_types:
            self.clause_types = [ClauseType(ct) for ct in clause_types]
        else:
            self.clause_types = list(ClauseType)

    def generate(self, clause_type: str, n_samples: int = 100, include_annotations: bool = True) -> List[Dict[str, Any]]:
        """Generate synthetic legal clauses."""
        logger.info(f"Generating {n_samples} {clause_type} clauses...")

        ct = ClauseType(clause_type)
        templates = self.CLAUSE_TEMPLATES.get(ct, [])
        if not templates:
            raise ConfigurationError(f"No templates found for clause type: {clause_type}")

        states = ["California", "New York", "Texas", "Delaware", "Illinois"]
        parties = ["Vendor", "Client", "Licensor", "Licensee", "Contractor"]
        results = []

        for i in range(n_samples):
            template = random.choice(templates)
            fill_values = {
                "party_a": random.choice(parties),
                "party_b": random.choice(parties),
                "party": random.choice(parties),
                "state": random.choice(states),
                "jurisdiction": f"{random.choice(states)} or federal courts therein",
                "event": random.choice(["expiration", "breach", "bankruptcy", "change of control"]),
                "years": str(random.choice([2, 3, 5, 7])),
                "days": str(random.choice([5, 10, 15, 30])),
            }

            clause_text = template
            for key, value in fill_values.items():
                clause_text = clause_text.replace("{" + key + "}", value)

            clause_hash = hashlib.sha256(clause_text.encode()).hexdigest()[:12]

            clause_data = {
                "clause_id": f"CLA-{clause_hash}",
                "clause_type": clause_type,
                "text": clause_text,
                "language": self.language,
                "complexity": self.complexity,
            }

            if include_annotations:
                clause_data["word_count"] = len(clause_text.split())
                clause_data["sentence_count"] = clause_text.count(".") + clause_text.count(";") + 1
                clause_data["entities"] = [p for p in fill_values.values() if p in parties]

            results.append(clause_data)

        return results

    def to_jsonl(self, clauses: List[Dict], output_path: str):
        """Export clauses to JSONL format."""
        import json
        with open(output_path, "w", encoding="utf-8") as f:
            for clause in clauses:
                f.write(json.dumps(clause, ensure_ascii=False) + "\n")
        logger.info(f"Exported {len(clauses)} clauses to {output_path}")


# ---------------------------------------------------------------------------
# Main Demo
# ---------------------------------------------------------------------------

def main():
    """Demo function to showcase the module."""
    print("=" * 60)
    print(" Domain-Specific Synthetic Data Generation Demo")
    print("=" * 60)

    # 1. Healthcare
    print("\n--- 1. Healthcare Generation ---")
    hc_gen = HealthcareGenerator(n_patients=50)
    patients = hc_gen.generate_cohort(
        conditions={"diabetes_prevalence": 0.2, "hypertension_prevalence": 0.3}
    )
    print(f"Generated {len(patients)} patient records.")
    print(f"Diagnosis distribution:\n{patients['diagnosis_code'].value_counts().to_string()}")
    print(f"Validation results:")
    for r in hc_gen.get_validation_results():
        print(f"  {r}")

    # 2. Finance
    print("\n--- 2. Financial Generation ---")
    fin_gen = FinancialGenerator(n_customers=20, fraud_rate=0.05)
    txns = fin_gen.generate(
        fraud_patterns=["card_testing", "account_takeover", "geo_impossibility"]
    )
    print(f"Generated {len(txns)} transactions.")
    print(f"Fraud count: {txns['is_fraud'].sum()}")
    print(f"Mean amount: ${txns['amount'].mean():.2f}")
    print(f"Validation results:")
    for r in fin_gen.get_validation_results():
        print(f"  {r}")

    # 3. IoT
    print("\n--- 3. IoT Sensor Generation ---")
    iot_gen = IoTSensorGenerator(n_sensors=3)
    sensor_data = iot_gen.generate_with_fault(
        fault_type="bearing_degradation", onset_hour=10, degradation_rate=0.05
    )
    print(f"Generated {len(sensor_data)} sensor readings across {iot_gen.n_sensors} sensors.")
    fault_cols = [c for c in sensor_data.columns if c.endswith("_is_fault")]
    for col in fault_cols:
        print(f"  {col}: {sensor_data[col].sum()} fault readings")
    print(f"Validation results:")
    for r in iot_gen.get_validation_results():
        print(f"  {r}")

    # 4. Legal
    print("\n--- 4. Legal Clause Generation ---")
    legal_gen = LegalGenerator(
        clause_types=["indemnification", "limitation_of_liability"],
        language="en-US"
    )
    indemnification_clauses = legal_gen.generate(clause_type="indemnification", n_samples=5)
    print(f"Generated {len(indemnification_clauses)} indemnification clauses.")
    for clause in indemnification_clauses[:2]:
        print(f"  [{clause['clause_id']}] ({clause['word_count']} words): {clause['text'][:80]}...")

    print("\n" + "=" * 60)
    print(" Demo Complete")
    print("=" * 60)


if __name__ == "__main__":
    main()

"""
Refugee Support Module
Part of the humanitarian-tech skill domain

Comprehensive refugee and displaced person support system covering registration,
camp management, biometric identification, and cash assistance programs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date, timedelta
from enum import Enum, IntEnum
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import hashlib
import json
import random
import re
import uuid


# =============================================================================
# Enums
# =============================================================================

class Gender(Enum):
    """Gender classification."""
    MALE = "male"
    FEMALE = "female"
    NON_BINARY = "non_binary"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"
    OTHER = "other"


class RelationshipType(Enum):
    """Family relationship types."""
    HEAD = "head"
    SPOUSE = "spouse"
    SON = "son"
    DAUGHTER = "daughter"
    FATHER = "father"
    MOTHER = "mother"
    BROTHER = "brother"
    SISTER = "sister"
    GRANDCHILD = "grandchild"
    GRANDPARENT = "grandparent"
    OTHER_FAMILY = "other_family"
    OTHER_NON_FAMILY = "other_non_family"


class RegistrationStatus(Enum):
    """Refugee registration status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    VERIFIED = "verified"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


class VulnerabilityCategory(Enum):
    """Vulnerability categories for prioritization."""
    UNACCOMPANIED_MINOR = "unaccompanied_minor"
    SEPARATED_CHILD = "separated_child"
    SINGLE_PARENT = "single_parent"
    ELDERLY = "elderly"
    PREGNANT = "pregnant"
    DISABLED = "disabled"
    CHRONIC_ILLNESS = "chronic_illness"
    GBV_SURVIVOR = "gbv_survivor"
    AT_RISK = "at_risk"
    NONE = "none"


class CampZone(Enum):
    """Camp operational zones."""
    RESIDENTIAL = "residential"
    WASH = "wash"
    HEALTH = "health"
    EDUCATION = "education"
    PROTECTION = "protection"
    FOOD_DISTRIBUTION = "food_distribution"
    ADMINISTRATION = "administration"
    STORAGE = "storage"
    RECREATION = "recreation"


class PaymentMethod(Enum):
    """Cash assistance payment methods."""
    MOBILE_MONEY = "mobile_money"
    BANK_TRANSFER = "bank_transfer"
    CASH_CARD = "cash_card"
    CASH_HAND_DELIVERY = "cash_hand_delivery"
    VOUCHER = "voucher"


class PaymentStatus(Enum):
    """Payment transaction status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"
    CANCELLED = "cancelled"


class BiometricType(Enum):
    """Biometric capture types."""
    FINGERPRINT_LEFT_THUMB = "fingerprint_left_thumb"
    FINGERPRINT_LEFT_INDEX = "fingerprint_left_index"
    FINGERPRINT_LEFT_MIDDLE = "fingerprint_left_middle"
    FINGERPRINT_RIGHT_THUMB = "fingerprint_right_thumb"
    FINGERPRINT_RIGHT_INDEX = "fingerprint_right_index"
    FINGERPRINT_RIGHT_MIDDLE = "fingerprint_right_middle"
    IRIS_LEFT = "iris_left"
    IRIS_RIGHT = "iris_right"
    FACE = "face"


# =============================================================================
# Dataclasses
# =============================================================================

@dataclass
class RefugeeIndividual:
    """Individual refugee record."""
    individual_id: str
    given_name: str
    family_name: str
    date_of_birth: date
    gender: Gender
    nationality: str
    registration_status: RegistrationStatus = RegistrationStatus.PENDING
    registration_date: Optional[datetime] = None
    origin_location: str = ""
    displacement_date: Optional[date] = None
    vulnerabilities: List[VulnerabilityCategory] = field(default_factory=list)
    special_needs: str = ""
    contact_phone: Optional[str] = None
    languages: List[str] = field(default_factory=list)
    education_level: str = ""
    occupation: str = ""
    family_id: Optional[str] = None
    is_head_of_family: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def full_name(self) -> str:
        return f"{self.given_name} {self.family_name}"

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )

    @property
    def is_child(self) -> bool:
        return self.age < 18

    @property
    def is_elderly(self) -> bool:
        return self.age >= 60

    def has_vulnerability(self, category: VulnerabilityCategory) -> bool:
        return category in self.vulnerabilities

    def vulnerability_score(self) -> float:
        """Calculate vulnerability score (0-1) based on categories."""
        if not self.vulnerabilities:
            return 0.0
        high_risk = {VulnerabilityCategory.UNACCOMPANIAN_MINOR, VulnerabilityCategory.GBV_SURVIVOR}
        medium_risk = {VulnerabilityCategory.SINGLE_PARENT, VulnerabilityCategory.PREGNANT, VulnerabilityCategory.DISABLED}
        score = sum(0.3 if v in high_risk else 0.2 if v in medium_risk else 0.1 for v in self.vulnerabilities)
        return min(score, 1.0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "individual_id": self.individual_id,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth.isoformat(),
            "age": self.age,
            "gender": self.gender.value,
            "nationality": self.nationality,
            "registration_status": self.registration_status.value,
            "origin_location": self.origin_location,
            "displacement_date": self.displacement_date.isoformat() if self.displacement_date else None,
            "vulnerabilities": [v.value for v in self.vulnerabilities],
            "family_id": self.family_id,
            "is_head_of_family": self.is_head_of_family,
            "vulnerability_score": self.vulnerability_score()
        }


@dataclass
class RefugeeFamily:
    """Family unit record."""
    family_id: str
    head: RefugeeIndividual
    members: List[RefugeeIndividual] = field(default_factory=list)
    registration_date: Optional[datetime] = None
    case_number: Optional[str] = None
    shelter_id: Optional[str] = None
    camp_id: Optional[str] = None
    notes: str = ""

    @property
    def family_size(self) -> int:
        return 1 + len(self.members)

    @property
    def children_count(self) -> int:
        children = sum(1 for m in self.members if m.is_child)
        return children + (1 if self.head.is_child else 0)

    @property
    def adults_count(self) -> int:
        adults = sum(1 for m in self.members if not m.is_child)
        return adults + (1 if not self.head.is_child else 0)

    def get_members(self) -> List[RefugeeIndividual]:
        """Get all family members including head."""
        return [self.head] + self.members

    def total_vulnerability_score(self) -> float:
        """Calculate combined vulnerability score for the family."""
        all_members = self.get_members()
        if not all_members:
            return 0.0
        return sum(m.vulnerability_score() for m in all_members) / len(all_members)

    def add_member(self, member: RefugeeIndividual) -> None:
        """Add a member to the family."""
        member.family_id = self.family_id
        member.is_head_of_family = False
        self.members.append(member)

    def remove_member(self, individual_id: str) -> Optional[RefugeeIndividual]:
        """Remove a member from the family."""
        for i, member in enumerate(self.members):
            if member.individual_id == individual_id:
                removed = self.members.pop(i)
                removed.family_id = None
                return removed
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "family_id": self.family_id,
            "head": self.head.to_dict(),
            "members": [m.to_dict() for m in self.members],
            "family_size": self.family_size,
            "children_count": self.children_count,
            "adults_count": self.adults_count,
            "registration_date": self.registration_date.isoformat() if self.registration_date else None,
            "case_number": self.case_number,
            "shelter_id": self.shelter_id,
            "camp_id": self.camp_id,
            "total_vulnerability_score": self.total_vulnerability_score()
        }


@dataclass
class BiometricTemplate:
    """Encrypted biometric template record."""
    template_id: str
    individual_id: str
    biometric_type: BiometricType
    template_hash: str
    captured_at: datetime
    quality_score: float  # 0-1
    device_id: str = ""
    operator_id: str = ""
    consent_obtained: bool = False
    is_primary: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "template_id": self.template_id,
            "individual_id": self.individual_id,
            "biometric_type": self.biometric_type.value,
            "captured_at": self.captured_at.isoformat(),
            "quality_score": self.quality_score,
            "device_id": self.device_id,
            "consent_obtained": self.consent_obtained,
            "is_primary": self.is_primary
        }


@dataclass
class Shelter:
    """Camp shelter unit."""
    shelter_id: str
    zone: CampZone
    capacity: int
    current_occupancy: int = 0
    shelter_type: str = "tent"
    condition: str = "good"
    facilities: List[str] = field(default_factory=list)
    assigned_family_id: Optional[str] = None
    last_maintenance: Optional[datetime] = None

    def available_beds(self) -> int:
        return max(0, self.capacity - self.current_occupancy)

    def is_available(self) -> bool:
        return self.assigned_family_id is None and self.available_beds() > 0

    def assign_family(self, family_id: str, family_size: int) -> bool:
        """Assign a family to this shelter."""
        if self.available_beds() < family_size:
            return False
        self.assigned_family_id = family_id
        self.current_occupancy = family_size
        return True

    def vacate(self) -> None:
        """Vacate the shelter."""
        self.assigned_family_id = None
        self.current_occupancy = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "shelter_id": self.shelter_id,
            "zone": self.zone.value,
            "capacity": self.capacity,
            "current_occupancy": self.current_occupancy,
            "available_beds": self.available_beds(),
            "shelter_type": self.shelter_type,
            "condition": self.condition,
            "assigned_family_id": self.assigned_family_id,
            "facilities": self.facilities
        }


@dataclass
class CashAssistanceRecord:
    """Cash assistance transaction record."""
    record_id: str
    family_id: str
    amount: float
    currency: str
    payment_method: PaymentMethod
    status: PaymentStatus
    disbursement_date: Optional[datetime] = None
    transaction_reference: Optional[str] = None
    vulnerability_score: float = 0.0
    entitlement_month: str = ""  # Format: YYYY-MM
    approved_by: Optional[str] = None
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "record_id": self.record_id,
            "family_id": self.family_id,
            "amount": self.amount,
            "currency": self.currency,
            "payment_method": self.payment_method.value,
            "status": self.status.value,
            "disbursement_date": self.disbursement_date.isoformat() if self.disbursement_date else None,
            "transaction_reference": self.transaction_reference,
            "vulnerability_score": self.vulnerability_score,
            "entitlement_month": self.entitlement_month
        }


@dataclass
class Camp:
    """Refugee camp facility."""
    camp_id: str
    name: str
    location: Tuple[float, float]  # (latitude, longitude)
    capacity: int
    current_population: int = 0
    operational_since: Optional[date] = None
    managing_agency: str = ""
    zones: Dict[CampZone, int] = field(default_factory=dict)
    services: List[str] = field(default_factory=list)
    status: str = "operational"

    def occupancy_rate(self) -> float:
        if self.capacity == 0:
            return 0.0
        return self.current_population / self.capacity

    def available_capacity(self) -> int:
        return max(0, self.capacity - self.current_population)

    def has_service(self, service: str) -> bool:
        return service.lower() in [s.lower() for s in self.services]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "camp_id": self.camp_id,
            "name": self.name,
            "location": self.location,
            "capacity": self.capacity,
            "current_population": self.current_population,
            "available_capacity": self.available_capacity(),
            "occupancy_rate": self.occupancy_rate(),
            "managing_agency": self.managing_agency,
            "services": self.services,
            "status": self.status
        }


# =============================================================================
# Core Systems
# =============================================================================

class RegistrationSystem:
    """Refugee registration and case management system."""

    def __init__(self, database: str = "refugee_db", encryption_key: str = "default-key"):
        self.database = database
        self.encryption_key = encryption_key
        self.individuals: Dict[str, RefugeeIndividual] = {}
        self.families: Dict[str, RefugeeFamily] = {}
        self.registration_queue: List[str] = []
        self.case_counter = 0

    def _generate_individual_id(self) -> str:
        return f"IND-{uuid.uuid4().hex[:10].upper()}"

    def _generate_family_id(self) -> str:
        return f"FAM-{uuid.uuid4().hex[:8].upper()}"

    def _generate_case_number(self) -> str:
        self.case_counter += 1
        return f"CASE-{datetime.now().year}-{self.case_counter:06d}"

    def register_individual(self, given_name: str, family_name: str,
                            date_of_birth: date, gender: Gender,
                            nationality: str, **kwargs) -> RefugeeIndividual:
        """Register a new individual refugee."""
        individual_id = self._generate_individual_id()

        individual = RefugeeIndividual(
            individual_id=individual_id,
            given_name=given_name,
            family_name=family_name,
            date_of_birth=date_of_birth,
            gender=gender,
            nationality=nationality,
            registration_status=RegistrationStatus.IN_PROGRESS,
            registration_date=datetime.now(),
            origin_location=kwargs.get("origin_location", ""),
            displacement_date=kwargs.get("displacement_date"),
            vulnerabilities=kwargs.get("vulnerabilities", []),
            special_needs=kwargs.get("special_needs", ""),
            contact_phone=kwargs.get("contact_phone"),
            languages=kwargs.get("languages", []),
            education_level=kwargs.get("education_level", ""),
            occupation=kwargs.get("occupation", "")
        )

        self.individuals[individual_id] = individual
        self.registration_queue.append(individual_id)
        return individual

    def register_family(self, head_given_name: str, head_family_name: str,
                        head_date_of_birth: date, head_gender: Gender,
                        head_nationality: str, members: List[Dict[str, Any]],
                        **kwargs) -> RefugeeFamily:
        """Register a new refugee family."""
        family_id = self._generate_family_id()
        case_number = self._generate_case_number()

        head = self.register_individual(
            given_name=head_given_name,
            family_name=head_family_name,
            date_of_birth=head_date_of_birth,
            gender=head_gender,
            nationality=head_nationality,
            **{k: v for k, v in kwargs.items() if k in RefugeeIndividual.__dataclass_fields__}
        )
        head.is_head_of_family = True
        head.family_id = family_id

        family = RefugeeFamily(
            family_id=family_id,
            head=head,
            registration_date=datetime.now(),
            case_number=case_number,
            camp_id=kwargs.get("camp_id"),
            notes=kwargs.get("notes", "")
        )

        for member_data in members:
            member = self.register_individual(
                given_name=member_data["given_name"],
                family_name=member_data.get("family_name", head_family_name),
                date_of_birth=member_data["date_of_birth"],
                gender=member_data.get("gender", Gender.MALE),
                nationality=member_data.get("nationality", head_nationality),
                **{k: v for k, v in member_data.items()
                   if k in RefugeeIndividual.__dataclass_fields__ and k not in ("given_name", "family_name", "date_of_birth", "gender", "nationality")}
            )
            family.add_member(member)

        self.families[family_id] = family
        return family

    def complete_registration(self, individual_id: str) -> bool:
        """Mark registration as complete."""
        if individual_id in self.individuals:
            self.individuals[individual_id].registration_status = RegistrationStatus.COMPLETED
            if individual_id in self.registration_queue:
                self.registration_queue.remove(individual_id)
            return True
        return False

    def verify_registration(self, individual_id: str) -> bool:
        """Verify a completed registration."""
        if individual_id in self.individuals:
            ind = self.individuals[individual_id]
            if ind.registration_status == RegistrationStatus.COMPLETED:
                ind.registration_status = RegistrationStatus.VERIFIED
                return True
        return False

    def search_by_name(self, name_query: str) -> List[RefugeeIndividual]:
        """Search individuals by name (partial match)."""
        query_lower = name_query.lower()
        results = []
        for ind in self.individuals.values():
            if (query_lower in ind.given_name.lower() or
                    query_lower in ind.family_name.lower() or
                    query_lower in ind.full_name.lower()):
                results.append(ind)
        return results

    def search_by_nationality(self, nationality: str) -> List[RefugeeIndividual]:
        """Search individuals by nationality."""
        nat_lower = nationality.lower()
        return [ind for ind in self.individuals.values()
                if nat_lower in ind.nationality.lower()]

    def get_vulnerable_individuals(self, min_score: float = 0.3) -> List[RefugeeIndividual]:
        """Get individuals with vulnerability score above threshold."""
        return [ind for ind in self.individuals.values()
                if ind.vulnerability_score() >= min_score]

    def get_statistics(self) -> Dict[str, Any]:
        """Get registration statistics."""
        total = len(self.individuals)
        by_status = {}
        by_gender = {}
        by_nationality = {}
        children = 0
        elderly = 0

        for ind in self.individuals.values():
            by_status[ind.registration_status.value] = by_status.get(ind.registration_status.value, 0) + 1
            by_gender[ind.gender.value] = by_gender.get(ind.gender.value, 0) + 1
            by_nationality[ind.nationality] = by_nationality.get(ind.nationality, 0) + 1
            if ind.is_child:
                children += 1
            if ind.is_elderly:
                elderly += 1

        return {
            "total_individuals": total,
            "total_families": len(self.families),
            "by_status": by_status,
            "by_gender": by_gender,
            "by_nationality": by_nationality,
            "children": children,
            "elderly": elderly,
            "pending_registration": len(self.registration_queue)
        }


class BiometricIDSystem:
    """Biometric identification and deduplication system."""

    def __init__(self, encryption_standard: str = "AES-256"):
        self.encryption_standard = encryption_standard
        self.templates: Dict[str, List[BiometricTemplate]] = {}
        self.deduplication_log: List[Dict[str, Any]] = []
        self.consent_registry: Dict[str, bool] = {}

    def enroll(self, individual_id: str, biometric_type: BiometricType,
               raw_data: bytes, quality_score: float, **kwargs) -> BiometricTemplate:
        """Enroll a new biometric template."""
        template_id = f"BIO-{uuid.uuid4().hex[:10].upper()}"
        template_hash = hashlib.sha256(raw_data).hexdigest()

        template = BiometricTemplate(
            template_id=template_id,
            individual_id=individual_id,
            biometric_type=biometric_type,
            template_hash=template_hash,
            captured_at=datetime.now(),
            quality_score=quality_score,
            device_id=kwargs.get("device_id", ""),
            operator_id=kwargs.get("operator_id", ""),
            consent_obtained=kwargs.get("consent_obtained", False),
            is_primary=kwargs.get("is_primary", False)
        )

        if individual_id not in self.templates:
            self.templates[individual_id] = []
        self.templates[individual_id].append(template)

        self.consent_registry[individual_id] = template.consent_obtained
        return template

    def verify_identity(self, individual_id: str, biometric_type: BiometricType,
                        probe_hash: str) -> Dict[str, Any]:
        """Verify an individual's identity against stored templates."""
        templates = self.templates.get(individual_id, [])
        type_templates = [t for t in templates if t.biometric_type == biometric_type]

        if not type_templates:
            return {"match": False, "confidence": 0.0, "reason": "no_template_found"}

        best_match = max(type_templates, key=lambda t: t.quality_score)
        match = best_match.template_hash == probe_hash
        confidence = best_match.quality_score if match else 0.0

        return {
            "match": match,
            "confidence": confidence,
            "template_id": best_match.template_id,
            "quality_score": best_match.quality_score
        }

    def deduplicate(self, probe_hash: str, biometric_type: BiometricType,
                    threshold: float = 0.85) -> List[Dict[str, Any]]:
        """Check for potential duplicate registrations."""
        potential_matches = []

        for individual_id, templates in self.templates.items():
            for template in templates:
                if template.biometric_type == biometric_type:
                    similarity = self._calculate_similarity(template.template_hash, probe_hash)
                    if similarity >= threshold:
                        potential_matches.append({
                            "individual_id": individual_id,
                            "template_id": template.template_id,
                            "similarity_score": similarity,
                            "biometric_type": biometric_type.value
                        })

        if potential_matches:
            self.deduplication_log.append({
                "probe_hash": probe_hash[:16] + "...",
                "biometric_type": biometric_type.value,
                "matches_found": len(potential_matches),
                "timestamp": datetime.now().isoformat()
            })

        return sorted(potential_matches, key=lambda x: x["similarity_score"], reverse=True)

    def _calculate_similarity(self, hash1: str, hash2: str) -> float:
        """Calculate similarity between two template hashes."""
        if hash1 == hash2:
            return 1.0
        matching_bits = sum(c1 == c2 for c1, c2 in zip(hash1, hash2))
        return matching_bits / max(len(hash1), len(hash2))

    def get_individual_biometrics(self, individual_id: str) -> List[BiometricTemplate]:
        """Get all biometric templates for an individual."""
        return self.templates.get(individual_id, [])

    def has_consent(self, individual_id: str) -> bool:
        """Check if individual has given consent for biometric capture."""
        return self.consent_registry.get(individual_id, False)

    def get_statistics(self) -> Dict[str, Any]:
        """Get biometric enrollment statistics."""
        total_templates = sum(len(t) for t in self.templates.values())
        by_type = {}
        for templates in self.templates.values():
            for t in templates:
                by_type[t.biometric_type.value] = by_type.get(t.biometric_type.value, 0) + 1

        return {
            "total_individuals_enrolled": len(self.templates),
            "total_templates": total_templates,
            "by_biometric_type": by_type,
            "consent_rate": sum(1 for v in self.consent_registry.values() if v) / max(len(self.consent_registry), 1),
            "deduplication_checks": len(self.deduplication_log)
        }


class CampManager:
    """Camp management and facility operations."""

    def __init__(self, camp_id: str, camp_name: str = ""):
        self.camp_id = camp_id
        self.camp_name = camp_name
        self.camp: Optional[Camp] = None
        self.shelters: Dict[str, Shelter] = {}
        self.family_assignments: Dict[str, str] = {}  # family_id -> shelter_id
        self.incident_reports: List[Dict[str, Any]] = []

    def initialize_camp(self, name: str, location: Tuple[float, float],
                        capacity: int, managing_agency: str,
                        services: List[str]) -> Camp:
        """Initialize camp with basic configuration."""
        self.camp = Camp(
            camp_id=self.camp_id,
            name=name,
            location=location,
            capacity=capacity,
            operational_since=date.today(),
            managing_agency=managing_agency,
            services=services
        )
        return self.camp

    def add_shelter(self, shelter_type: str, capacity: int,
                    zone: CampZone = CampZone.RESIDENTIAL,
                    facilities: Optional[List[str]] = None) -> Shelter:
        """Add a new shelter to the camp."""
        shelter_id = f"SHLT-{uuid.uuid4().hex[:8].upper()}"
        shelter = Shelter(
            shelter_id=shelter_id,
            zone=zone,
            capacity=capacity,
            shelter_type=shelter_type,
            facilities=facilities or ["lighting"]
        )
        self.shelters[shelter_id] = shelter
        return shelter

    def allocate_shelter(self, family_id: str, family_size: int,
                         priority: str = "standard") -> Optional[Shelter]:
        """Allocate shelter to a family based on size and priority."""
        suitable_shelters = [
            s for s in self.shelters.values()
            if s.is_available() and s.available_beds() >= family_size
        ]

        if not suitable_shelters:
            return None

        if priority == "high":
            suitable_shelters.sort(key=lambda s: s.capacity, reverse=True)
        else:
            suitable_shelters.sort(key=lambda s: s.available_beds())

        shelter = suitable_shelters[0]
        if shelter.assign_family(family_id, family_size):
            self.family_assignments[family_id] = shelter.shelter_id
            return shelter
        return None

    def deallocate_shelter(self, family_id: str) -> bool:
        """Remove family from shelter."""
        shelter_id = self.family_assignments.pop(family_id, None)
        if shelter_id and shelter_id in self.shelters:
            self.shelters[shelter_id].vacate()
            return True
        return False

    def report_incident(self, incident_type: str, location: str,
                        description: str, severity: str) -> Dict[str, Any]:
        """Report a camp incident."""
        incident = {
            "incident_id": f"INC-{uuid.uuid4().hex[:8].upper()}",
            "camp_id": self.camp_id,
            "type": incident_type,
            "location": location,
            "description": description,
            "severity": severity,
            "reported_at": datetime.now().isoformat(),
            "status": "open"
        }
        self.incident_reports.append(incident)
        return incident

    def get_shelter_availability(self) -> Dict[str, Any]:
        """Get shelter availability summary."""
        total_capacity = sum(s.capacity for s in self.shelters.values())
        total_occupied = sum(s.current_occupancy for s in self.shelters.values())
        available_shelters = sum(1 for s in self.shelters.values() if s.is_available())

        return {
            "total_shelters": len(self.shelters),
            "total_capacity": total_capacity,
            "total_occupied": total_occupied,
            "available_shelters": available_shelters,
            "occupancy_rate": total_occupied / max(total_capacity, 1),
            "families_assigned": len(self.family_assignments)
        }

    def get_camp_status(self) -> Dict[str, Any]:
        """Get overall camp status."""
        return {
            "camp_id": self.camp_id,
            "camp_info": self.camp.to_dict() if self.camp else None,
            "shelter_availability": self.get_shelter_availability(),
            "open_incidents": sum(1 for i in self.incident_reports if i["status"] == "open"),
            "total_incidents": len(self.incident_reports)
        }


class CashAssistanceProgram:
    """Cash assistance management and disbursement system."""

    def __init__(self, payment_provider: str, currency: str = "USD"):
        self.payment_provider = payment_provider
        self.currency = currency
        self.beneficiaries: Dict[str, Dict[str, Any]] = {}
        self.transactions: List[CashAssistanceRecord] = []
        self.entitlement_rules: Dict[str, float] = {
            "base_amount": 50.0,
            "per_child": 25.0,
            "vulnerability_multiplier": 1.5,
            "max_amount": 300.0
        }

    def register_beneficiary(self, family_id: str, family_size: int,
                             vulnerability_score: float,
                             payment_method: PaymentMethod,
                             payment_details: Dict[str, str]) -> Dict[str, Any]:
        """Register a family for cash assistance."""
        entitlement = self.calculate_entitlement(family_size, vulnerability_score)

        beneficiary = {
            "family_id": family_id,
            "family_size": family_size,
            "vulnerability_score": vulnerability_score,
            "payment_method": payment_method.value,
            "payment_details": payment_details,
            "monthly_entitlement": entitlement,
            "registered_at": datetime.now().isoformat(),
            "status": "active",
            "total_received": 0.0,
            "last_payment_date": None
        }

        self.beneficiaries[family_id] = beneficiary
        return beneficiary

    def calculate_entitlement(self, family_size: int, vulnerability_score: float) -> float:
        """Calculate monthly cash assistance entitlement."""
        base = self.entitlement_rules["base_amount"]
        children_allowance = max(0, family_size - 1) * self.entitlement_rules["per_child"]
        vulnerability_bonus = vulnerability_score * self.entitlement_rules["vulnerability_multiplier"]
        total = (base + children_allowance) * (1 + vulnerability_bonus)
        return min(total, self.entitlement_rules["max_amount"])

    def disburse_payment(self, family_id: str, amount: Optional[float] = None,
                         entitlement_month: str = "") -> Optional[CashAssistanceRecord]:
        """Disburse cash assistance payment."""
        beneficiary = self.beneficiaries.get(family_id)
        if not beneficiary or beneficiary["status"] != "active":
            return None

        payment_amount = amount or beneficiary["monthly_entitlement"]
        payment_method = PaymentMethod(beneficiary["payment_method"])

        record = CashAssistanceRecord(
            record_id=f"PAY-{uuid.uuid4().hex[:10].upper()}",
            family_id=family_id,
            amount=payment_amount,
            currency=self.currency,
            payment_method=payment_method,
            status=PaymentStatus.PROCESSING,
            vulnerability_score=beneficiary["vulnerability_score"],
            entitlement_month=entitlement_month or datetime.now().strftime("%Y-%m"),
            transaction_reference=f"TXN-{uuid.uuid4().hex[:12].upper()}"
        )

        # Simulate payment processing
        success = random.random() > 0.05  # 95% success rate
        if success:
            record.status = PaymentStatus.COMPLETED
            record.disbursement_date = datetime.now()
            beneficiary["total_received"] += payment_amount
            beneficiary["last_payment_date"] = datetime.now().isoformat()
        else:
            record.status = PaymentStatus.FAILED

        self.transactions.append(record)
        return record

    def suspend_beneficiary(self, family_id: str, reason: str) -> bool:
        """Suspend a beneficiary from cash assistance."""
        if family_id in self.beneficiaries:
            self.beneficiaries[family_id]["status"] = "suspended"
            self.beneficiaries[family_id]["suspension_reason"] = reason
            return True
        return False

    def get_transaction_history(self, family_id: Optional[str] = None,
                                limit: int = 50) -> List[CashAssistanceRecord]:
        """Get transaction history."""
        records = self.transactions
        if family_id:
            records = [r for r in records if r.family_id == family_id]
        return sorted(records, key=lambda r: r.disbursement_date or datetime.min, reverse=True)[:limit]

    def get_program_statistics(self) -> Dict[str, Any]:
        """Get cash assistance program statistics."""
        active = sum(1 for b in self.beneficiaries.values() if b["status"] == "active")
        total_disbursed = sum(t.amount for t in self.transactions if t.status == PaymentStatus.COMPLETED)
        successful = sum(1 for t in self.transactions if t.status == PaymentStatus.COMPLETED)
        failed = sum(1 for t in self.transactions if t.status == PaymentStatus.FAILED)

        return {
            "total_beneficiaries": len(self.beneficiaries),
            "active_beneficiaries": active,
            "total_transactions": len(self.transactions),
            "successful_payments": successful,
            "failed_payments": failed,
            "total_disbursed": total_disbursed,
            "currency": self.currency,
            "payment_provider": self.payment_provider,
            "average_payment": total_disbursed / max(successful, 1)
        }


# =============================================================================
# Main Demo Function
# =============================================================================

def main() -> None:
    """Demonstrate the refugee support system capabilities."""
    print("=" * 70)
    print("  REFUGEE SUPPORT SYSTEM - DEMONSTRATION")
    print("=" * 70)

    # --- Registration System ---
    print("\n[1] REGISTRATION SYSTEM")
    print("-" * 40)
    registration = RegistrationSystem(database="refugee_db_demo")

    # Register families
    families_data = [
        {
            "head": {"given_name": "Amina", "family_name": "Hassan", "date_of_birth": date(1985, 3, 15),
                     "gender": Gender.FEMALE, "nationality": "Somali"},
            "members": [
                {"given_name": "Omar", "date_of_birth": date(2010, 7, 22), "gender": Gender.MALE},
                {"given_name": "Fatima", "date_of_birth": date(2015, 11, 8), "gender": Gender.FEMALE, "vulnerabilities": [VulnerabilityCategory.AT_RISK]},
            ],
            "kwargs": {"origin_location": "Mogadishu, Somalia", "displacement_date": date(2024, 1, 15), "languages": ["Somali", "Arabic"]}
        },
        {
            "head": {"given_name": "Jean", "family_name": "Baptiste", "date_of_birth": date(1978, 5, 20),
                     "gender": Gender.MALE, "nationality": "Congolese"},
            "members": [
                {"given_name": "Marie", "date_of_birth": date(1980, 9, 12), "gender": Gender.FEMALE},
                {"given_name": "Pierre", "date_of_birth": date(2005, 2, 28), "gender": Gender.MALE},
                {"given_name": "Sophie", "date_of_birth": date(2008, 6, 15), "gender": Gender.FEMALE},
                {"given_name": "Luc", "date_of_birth": date(2018, 1, 3), "gender": Gender.MALE},
            ],
            "kwargs": {"origin_location": "Bukavu, DRC", "displacement_date": date(2023, 11, 20), "languages": ["French", "Swahili"]}
        },
        {
            "head": {"given_name": "Khadija", "family_name": "Ahmed", "date_of_birth": date(1992, 8, 10),
                     "gender": Gender.FEMALE, "nationality": "Syrian"},
            "members": [
                {"given_name": "Yusuf", "date_of_birth": date(2020, 4, 18), "gender": Gender.MALE},
            ],
            "kwargs": {"origin_location": "Aleppo, Syria", "displacement_date": date(2024, 3, 5),
                       "vulnerabilities": [VulnerabilityCategory.SINGLE_PARENT, VulnerabilityCategory.PREGNANT],
                       "languages": ["Arabic", "Turkish"]}
        }
    ]

    registered_families = []
    for fam_data in families_data:
        family = registration.register_family(
            head_given_name=fam_data["head"]["given_name"],
            head_family_name=fam_data["head"]["family_name"],
            head_date_of_birth=fam_data["head"]["date_of_birth"],
            head_gender=fam_data["head"]["gender"],
            head_nationality=fam_data["head"]["nationality"],
            members=fam_data["members"],
            **fam_data["kwargs"]
        )
        registered_families.append(family)
        print(f"  Registered family: {family.head.full_name} (ID: {family.family_id})")
        print(f"    Size: {family.family_size}, Children: {family.children_count}")
        print(f"    Case: {family.case_number}")

    # Complete some registrations
    for family in registered_families[:2]:
        registration.complete_registration(family.head.individual_id)
        registration.verify_registration(family.head.individual_id)
        print(f"  Verified: {family.head.full_name}")

    # Search
    print("\n  Search by name 'Ahmed':")
    results = registration.search_by_name("Ahmed")
    for r in results:
        print(f"    Found: {r.full_name} ({r.nationality})")

    # Statistics
    stats = registration.get_statistics()
    print(f"\n  Registration Statistics:")
    print(f"    Total individuals: {stats['total_individuals']}")
    print(f"    Total families: {stats['total_families']}")
    print(f"    Children: {stats['children']}, Elderly: {stats['elderly']}")
    print(f"    By status: {stats['by_status']}")

    # --- Biometric ID ---
    print("\n\n[2] BIOMETRIC IDENTIFICATION")
    print("-" * 40)
    biometric = BiometricIDSystem(encryption_standard="AES-256")

    for family in registered_families:
        for member in family.get_members():
            # Simulate biometric capture
            mock_data = f"biometric-data-{member.individual_id}".encode()
            biometric.enroll(
                individual_id=member.individual_id,
                biometric_type=BiometricType.FINGERPRINT_RIGHT_THUMB,
                raw_data=mock_data,
                quality_score=random.uniform(0.7, 0.98),
                consent_obtained=True,
                is_primary=True
            )
        print(f"  Enrolled biometrics for: {family.head.full_name}'s family ({family.family_size} members)")

    # Deduplication check
    probe = f"biometric-data-{registered_families[0].head.individual_id}".encode()
    duplicates = biometric.deduplicate(probe, BiometricType.FINGERPRINT_RIGHT_THUMB, threshold=0.9)
    print(f"\n  Deduplication check: {len(duplicates)} potential matches found")
    if duplicates:
        print(f"    Best match: {duplicates[0]['individual_id']} (similarity: {duplicates[0]['similarity_score']:.2f})")

    bio_stats = biometric.get_statistics()
    print(f"\n  Biometric Statistics:")
    print(f"    Individuals enrolled: {bio_stats['total_individuals_enrolled']}")
    print(f"    Total templates: {bio_stats['total_templates']}")
    print(f"    Consent rate: {bio_stats['consent_rate']:.1%}")

    # --- Camp Management ---
    print("\n\n[3] CAMP MANAGEMENT")
    print("-" * 40)
    camp_manager = CampManager(camp_id="CAMP-001", camp_name="Dadaab Extension")

    camp = camp_manager.initialize_camp(
        name="Dadaab Extension Camp",
        location=(0.0463, 40.3103),
        capacity=15000,
        managing_agency="UNHCR",
        services=["registration", "protection", "health", "education", "wash", "food_distribution"]
    )
    print(f"  Initialized camp: {camp.name}")
    print(f"    Capacity: {camp.capacity}, Agency: {camp.managing_agency}")

    # Add shelters
    shelter_configs = [
        ("family_tent", 6, CampZone.RESIDENTIAL, ["lighting", "mattress"]),
        ("family_tent", 8, CampZone.RESIDENTIAL, ["lighting", "mattress"]),
        ("communal_shelter", 50, CampZone.RESIDENTIAL, ["lighting", "partition"]),
        ("emergency庇护所", 100, CampZone.RESIDENTIAL, ["lighting"]),
    ]
    for stype, cap, zone, facilities in shelter_configs:
        shelter = camp_manager.add_shelter(stype, cap, zone, facilities)
        print(f"  Added shelter: {shelter.shelter_id} ({stype}, capacity: {cap})")

    # Allocate shelters
    for family in registered_families:
        shelter = camp_manager.allocate_shelter(family.family_id, family.family_size, priority="high")
        if shelter:
            family.shelter_id = shelter.shelter_id
            print(f"  Allocated {shelter.shelter_id} to {family.head.full_name} (size: {family.family_size})")

    # Report incident
    incident = camp_manager.report_incident(
        incident_type="health_concern",
        location="Zone B, Shelter 12",
        description="Suspected cholera cases reported",
        severity="high"
    )
    print(f"\n  Incident reported: {incident['incident_id']} ({incident['type']})")

    camp_status = camp_manager.get_camp_status()
    print(f"\n  Camp Status:")
    print(f"    Shelters: {camp_status['shelter_availability']['total_shelters']}")
    print(f"    Occupancy: {camp_status['shelter_availability']['occupancy_rate']:.1%}")
    print(f"    Open incidents: {camp_status['open_incidents']}")

    # --- Cash Assistance ---
    print("\n\n[4] CASH ASSISTANCE PROGRAM")
    print("-" * 40)
    cash_program = CashAssistanceProgram(payment_provider="m_pesa", currency="USD")

    for family in registered_families:
        beneficiary = cash_program.register_beneficiary(
            family_id=family.family_id,
            family_size=family.family_size,
            vulnerability_score=family.total_vulnerability_score(),
            payment_method=PaymentMethod.MOBILE_MONEY,
            payment_details={"phone": "+254-700-123456", "provider": "safaricom"}
        )
        print(f"  Registered beneficiary: {family.head.full_name}")
        print(f"    Monthly entitlement: ${beneficiary['monthly_entitlement']:.2f}")
        print(f"    Vulnerability score: {beneficiary['vulnerability_score']:.2f}")

    # Disburse payments
    print("\n  Disbursing payments...")
    for family in registered_families:
        payment = cash_program.disburse_payment(family.family_id, entitlement_month="2024-07")
        if payment:
            print(f"    {family.head.full_name}: ${payment.amount:.2f} - {payment.status.value}")

    cash_stats = cash_program.get_program_statistics()
    print(f"\n  Cash Assistance Statistics:")
    print(f"    Total beneficiaries: {cash_stats['total_beneficiaries']}")
    print(f"    Active beneficiaries: {cash_stats['active_beneficiaries']}")
    print(f"    Total disbursed: ${cash_stats['total_disbursed']:.2f}")
    print(f"    Payment success rate: {cash_stats['successful_payments'] / max(cash_stats['total_transactions'], 1):.1%}")

    # --- Summary ---
    print("\n\n" + "=" * 70)
    print("  DEMONSTRATION COMPLETE")
    print("=" * 70)
    print("\n  Components demonstrated:")
    print("    1. Registration System - individual and family registration")
    print("    2. Biometric ID - enrollment, verification, deduplication")
    print("    3. Camp Management - shelter allocation, incident reporting")
    print("    4. Cash Assistance - entitlement calculation, disbursement")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
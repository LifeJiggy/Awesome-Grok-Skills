"""
health_equity.py — Healthcare Access & Social Determinants Toolkit

Provides disparities analysis, SDOH tracking, telemedicine support, community
health worker tools, resource allocation, care matching, and chronic disease management.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime, timedelta
from collections import defaultdict


class RiskLevel(Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class InsuranceType(Enum):
    UNINSURED = "uninsured"
    MEDICAID = "medicaid"
    MEDICARE = "medicare"
    ACA_MARKETPLACE = "aca_marketplace"
    EMPLOYER = "employer"
    TRICARE = "tricare"


class CarePathway(Enum):
    DIABETES = "diabetes"
    HYPERTENSION = "hypertension"
    ASTHMA = "asthma"
    HEART_FAILURE = "heart_failure"
    DEPRESSION = "depression"


class ResourceType(Enum):
    FOOD = "food"
    HOUSING = "housing"
    TRANSPORTATION = "transportation"
    EMPLOYMENT = "employment"
    MENTAL_HEALTH = "mental_health"
    SUBSTANCE_USE = "substance_use"


class AppointmentStatus(Enum):
    SCHEDULED = "scheduled"
    CONFIRMED = "confirmed"
    COMPLETED = "completed"
    NO_SHOW = "no_show"
    CANCELLED = "cancelled"


@dataclass
class Patient:
    patient_id: str
    name: str
    date_of_birth: str
    primary_language: str = "en"
    insurance_type: InsuranceType = InsuranceType.UNINSURED
    preferred_provider_gender: str | None = None
    cultural_preferences: list[str] = field(default_factory=list)
    chronic_conditions: list[str] = field(default_factory=list)


@dataclass
class SDOHResponse:
    domain: str
    question: str
    response: str
    risk_level: RiskLevel
    score: float


@dataclass
class CommunityData:
    community_id: str
    population: int
    primary_care_physicians: int
    ed_visits_per_1000: float
    uninsured_rate: float
    median_income: float
    life_expectancy: float
    poverty_rate: float = 0.0
    food_insecurity_rate: float = 0.0
    housing_instability_rate: float = 0.0

    @property
    def pc_ratio(self) -> float:
        return self.population / max(self.primary_care_physicians, 1)


@dataclass
class ResourceReferral:
    resource_id: str
    resource_name: str
    category: ResourceType
    location: tuple[float, float]
    phone: str = ""
    hours: str = ""
    capacity: int = 0


@dataclass
class DisparityFinding:
    indicator: str
    high_value: float
    low_value: float
    ratio: float
    interpretation: str
    severity: RiskLevel


@dataclass
class AllocationResult:
    community_id: str
    allocated: int
    need_score: float
    equity_weight: float
    rationale: str


@dataclass
class Provider:
    provider_id: str
    name: str
    specialty: str
    languages: list[str]
    cultural_competencies: list[str]
    insurance_accepted: list[InsuranceType]
    location: tuple[float, float]
    accepting_patients: bool = True


@dataclass
class Appointment:
    appointment_id: str
    patient_id: str
    provider_id: str
    scheduled_time: datetime
    status: AppointmentStatus = AppointmentStatus.SCHEDULED
    interpreter_needed: bool = False
    interpreter_language: str | None = None


@dataclass
class CarePathwayStep:
    step_id: str
    name: str
    description: str
    frequency_days: int
    required: bool = True


class SDOHAssessment:
    SCREENING_QUESTIONS = {
        "food_security": [
            "Within the past 12 months, were you worried about running out of food?",
            "Within the past 12 months, did the food you bought not go far and you had less money for food?",
        ],
        "housing_stability": [
            "Are you worried about losing your housing?",
            "Have you been living in a shelter, on the street, or doubled up with others?",
        ],
        "transportation": [
            "Have you missed or delayed medical care because of transportation?",
            "Do you have a reliable way to get to medical appointments?",
        ],
        "financial_toxicity": [
            "Are you stressed about medical bills?",
            "Have you delayed or gone without medical care because of cost?",
        ],
        "social_isolation": [
            "Do you feel lonely or isolated from others?",
            "Do you have someone you can count on for help?",
        ],
    }

    RISK_KEYWORDS = {
        "high_risk": ["sometimes", "often", "always", "worried", "trouble", "delayed", "missed", "stressed", "lonely", "isolated", "no", "not"],
        "low_risk": ["never", "rarely", "stable", "reliable", "fine", "good", "have", "able"],
    }

    def __init__(self, patient_id: str):
        self.patient_id = patient_id
        self.responses: dict[str, str] = {}
        self.completed_at: datetime | None = None

    def add_response(self, domain: str, response: str) -> None:
        self.responses[domain] = response

    def _score_response(self, domain: str, response: str) -> SDOHResponse:
        response_lower = response.lower()
        high_hits = sum(1 for kw in self.RISK_KEYWORDS["high_risk"] if kw in response_lower)
        low_hits = sum(1 for kw in self.RISK_KEYWORDS["low_risk"] if kw in response_lower)

        if high_hits > low_hits:
            risk = RiskLevel.HIGH
            score = 0.8
        elif high_hits == low_hits:
            risk = RiskLevel.MODERATE
            score = 0.5
        else:
            risk = RiskLevel.LOW
            score = 0.2

        return SDOHResponse(
            domain=domain,
            question=self.SCREENING_QUESTIONS.get(domain, [""])[0],
            response=response,
            risk_level=risk,
            score=score,
        )

    def get_results(self) -> dict:
        scored = [self._score_response(domain, resp) for domain, resp in self.responses.items()]
        high_risk = [s.domain for s in scored if s.risk_level == RiskLevel.HIGH]
        moderate_risk = [s.domain for s in scored if s.risk_level == RiskLevel.MODERATE]
        total_score = sum(s.score for s in scored) / max(len(scored), 1)

        overall_risk = RiskLevel.CRITICAL if total_score > 0.7 else (
            RiskLevel.HIGH if total_score > 0.5 else (
                RiskLevel.MODERATE if total_score > 0.3 else RiskLevel.LOW
            )
        )

        self.completed_at = datetime.now()

        return {
            "patient_id": self.patient_id,
            "domains_screened": len(scored),
            "high_risk_domains": high_risk,
            "moderate_risk_domains": moderate_risk,
            "total_risk_score": round(total_score, 3),
            "overall_risk": overall_risk.value,
            "scores": {s.domain: {"score": s.score, "risk": s.risk_level.value} for s in scored},
        }


class ResourceReferralNetwork:
    def __init__(self):
        self.resources: list[ResourceReferral] = []

    def add_resource(
        self,
        resource_id: str,
        category: str,
        name: str,
        location: tuple[float, float],
        phone: str = "",
        hours: str = "",
    ) -> None:
        self.resources.append(ResourceReferral(
            resource_id=resource_id,
            resource_name=name,
            category=ResourceType(category),
            location=location,
            phone=phone,
            hours=hours,
        ))

    def _haversine_km(self, loc1: tuple[float, float], loc2: tuple[float, float]) -> float:
        lat1, lon1 = math.radians(loc1[0]), math.radians(loc1[1])
        lat2, lon2 = math.radians(loc2[0]), math.radians(loc2[1])
        dlat, dlon = lat2 - lat1, lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        return 6371 * 2 * math.asin(math.sqrt(a))

    def match_referrals(
        self,
        assessment: SDOHAssessment,
        max_distance_km: float = 25.0,
        patient_location: tuple[float, float] | None = None,
    ) -> list[dict]:
        results = assessment.get_results()
        high_risk_domains = results["high_risk_domains"]
        moderate_risk_domains = results["moderate_risk_domains"]
        needed_categories = set()

        domain_to_resource = {
            "food_security": ResourceType.FOOD,
            "housing_stability": ResourceType.HOUSING,
            "transportation": ResourceType.TRANSPORTATION,
            "financial_toxicity": ResourceType.EMPLOYMENT,
            "social_isolation": ResourceType.MENTAL_HEALTH,
        }

        for domain in high_risk_domains + moderate_risk_domains:
            if domain in domain_to_resource:
                needed_categories.add(domain_to_resource[domain])

        referrals = []
        for resource in self.resources:
            if resource.category not in needed_categories:
                continue

            if patient_location:
                distance = self._haversine_km(patient_location, resource.location)
                if distance > max_distance_km:
                    continue
            else:
                distance = 0.0

            referrals.append({
                "resource_id": resource.resource_id,
                "resource_name": resource.resource_name,
                "category": resource.category.value,
                "distance_km": round(distance, 2),
                "phone": resource.phone,
                "hours": resource.hours,
                "priority": "high" if resource.category in [ResourceType(c) for c in high_risk_domains] else "moderate",
            })

        referrals.sort(key=lambda r: (0 if r["priority"] == "high" else 1, r["distance_km"]))
        return referrals


class DisparitiesAnalyzer:
    def __init__(self):
        self.communities: dict[str, CommunityData] = {}

    def add_community_data(self, **kwargs) -> None:
        data = CommunityData(**kwargs)
        self.communities[data.community_id] = data

    def _compare(
        self,
        high: CommunityData,
        low: CommunityData,
        indicator: str,
        high_value: float,
        low_value: float,
        higher_is_worse: bool = True,
    ) -> DisparityFinding | None:
        if low_value == 0:
            return None

        ratio = high_value / low_value if not higher_is_worse else low_value / high_value
        if ratio < 1.0:
            ratio = 1.0 / ratio if ratio > 0 else 1.0
            high_value, low_value = low_value, high_value

        if ratio >= 1.5:
            severity = RiskLevel.HIGH
        elif ratio >= 1.2:
            severity = RiskLevel.MODERATE
        else:
            return None

        return DisparityFinding(
            indicator=indicator,
            high_value=round(high_value, 2),
            low_value=round(low_value, 2),
            ratio=round(ratio, 2),
            interpretation=f"{indicator} is {ratio:.1f}x higher in {high.community_id} vs {low.community_id}",
            severity=severity,
        )

    def identify_disparities(self) -> list[DisparityFinding]:
        communities = list(self.communities.values())
        if len(communities) < 2:
            return []

        communities.sort(key=lambda c: c.median_income)
        lowest_income = communities[0]
        findings: list[DisparityFinding] = []

        for community in communities[1:]:
            comparisons = [
                ("ED Visits per 1000", community.ed_visits_per_1000, lowest_income.ed_visits_per_1000, True),
                ("Uninsured Rate", community.uninsured_rate, lowest_income.uninsured_rate, True),
                ("Life Expectancy Gap", lowest_income.life_expectancy, community.life_expectancy, False),
                ("Primary Care Ratio", community.pc_ratio, lowest_income.pc_ratio, True),
            ]

            for indicator, hv, lv, worse in comparisons:
                finding = self._compare(community, lowest_income, indicator, hv, lv, worse)
                if finding:
                    findings.append(finding)

        return findings

    def get_equity_score(self, community_id: str) -> dict:
        community = self.communities.get(community_id)
        if not community:
            return {"error": "Community not found"}

        all_incomes = sorted([c.median_income for c in self.communities.values()])
        income_rank = all_incomes.index(community.median_income) / max(len(all_incomes) - 1, 1)

        all_le = sorted([c.life_expectancy for c in self.communities.values()])
        le_rank = all_le.index(community.life_expectancy) / max(len(all_le) - 1, 1)

        equity_score = (income_rank + le_rank) / 2

        return {
            "community_id": community_id,
            "equity_score": round(equity_score, 3),
            "income_percentile": round(income_rank * 100),
            "life_expectancy_percentile": round(le_rank * 100),
            "recommendation": "Priority for resource allocation" if equity_score < 0.3 else "Monitor for disparities",
        }


class ResourceAllocator:
    def __init__(self):
        self.communities: dict[str, dict] = {}
        self.allocation_history: list[dict] = []

    def add_community(
        self,
        community_id: str,
        population: int,
        disease_burden_score: float,
        access_barrier_score: float,
        existing_resources: int,
    ) -> None:
        self.communities[community_id] = {
            "population": population,
            "disease_burden": disease_burden_score,
            "access_barrier": access_barrier_score,
            "existing_resources": existing_resources,
        }

    def _compute_need_score(self, community: dict) -> float:
        need = (
            community["disease_burden"] * 0.4
            + community["access_barrier"] * 0.35
            + (1.0 - min(community["existing_resources"] / max(community["population"] / 5000, 1), 1.0)) * 0.25
        )
        return need

    def optimize(
        self,
        total_resources: int,
        resource_type: str = "general",
    ) -> list[AllocationResult]:
        scored = []
        for cid, community in self.communities.items():
            need_score = self._compute_need_score(community)
            scored.append((cid, community, need_score))

        scored.sort(key=lambda x: x[2], reverse=True)

        total_need = sum(s[2] for s in scored) or 1.0
        allocations = []

        for cid, community, need_score in scored:
            equity_weight = need_score / total_need
            raw_allocation = total_resources * equity_weight
            allocated = max(1, round(raw_allocation))

            allocations.append(AllocationResult(
                community_id=cid,
                allocated=allocated,
                need_score=round(need_score, 3),
                equity_weight=round(equity_weight, 3),
                rationale=f"Need score {need_score:.3f} — disease burden {community['disease_burden']:.1f}, "
                          f"access barriers {community['access_barrier']:.1f}",
            ))

            self.allocation_history.append({
                "community_id": cid,
                "allocated": allocated,
                "resource_type": resource_type,
                "timestamp": datetime.now().isoformat(),
            })

        return allocations


class CareMatchingEngine:
    def __init__(self):
        self.providers: list[Provider] = []

    def add_provider(self, provider: Provider) -> None:
        self.providers.append(provider)

    def find_matches(
        self,
        patient: Patient,
        specialty_required: str | None = None,
        max_distance_km: float = 50.0,
    ) -> list[dict]:
        matches = []
        for provider in self.providers:
            if not provider.accepting_patients:
                continue
            if specialty_required and provider.specialty != specialty_required:
                continue

            language_match = patient.primary_language in provider.languages
            insurance_match = patient.insurance_type in provider.insurance_accepted
            cultural_match = bool(set(patient.cultural_preferences) & set(provider.cultural_competencies))

            score = 0.0
            if language_match:
                score += 0.35
            if insurance_match:
                score += 0.30
            if cultural_match:
                score += 0.20
            if not specialty_required or provider.specialty == specialty_required:
                score += 0.15

            matches.append({
                "provider_id": provider.provider_id,
                "name": provider.name,
                "specialty": provider.specialty,
                "score": round(score, 3),
                "language_match": language_match,
                "insurance_match": insurance_match,
                "cultural_match": cultural_match,
                "languages": provider.languages,
            })

        matches.sort(key=lambda m: m["score"], reverse=True)
        return matches


class ChronicDiseaseManager:
    CARE_PATHWAYS = {
        CarePathway.DIABETES: [
            CarePathwayStep("d1", "A1C Test", "Blood glucose test every 3-6 months", 90),
            CarePathwayStep("d2", "Eye Exam", "Annual dilated eye exam", 365),
            CarePathwayStep("d3", "Foot Exam", "Annual comprehensive foot exam", 365),
            CarePathwayStep("d4", "Kidney Function", "Annual urine albumin test", 365),
        ],
        CarePathway.HYPERTENSION: [
            CarePathwayStep("h1", "Blood Pressure Check", "Monthly blood pressure monitoring", 30),
            CarePathwayStep("h2", "Medication Review", "Quarterly medication review", 90),
            CarePathwayStep("h3", "Kidney Function", "Annual kidney function test", 365),
        ],
        CarePathway.ASTHMA: [
            CarePathwayStep("a1", "Spirometry", "Annual lung function test", 365),
            CarePathwayStep("a2", "Action Plan Review", "Review asthma action plan", 180),
        ],
    }

    def __init__(self):
        self.patient_plans: dict[str, dict] = {}
        self.adherence_log: dict[str, list[dict]] = defaultdict(list)

    def create_care_plan(self, patient_id: str, pathway: CarePathway) -> dict:
        steps = self.CARE_PATHWAYS.get(pathway, [])
        plan = {
            "patient_id": patient_id,
            "pathway": pathway.value,
            "steps": [
                {
                    "step_id": step.step_id,
                    "name": step.name,
                    "due_date": (datetime.now() + timedelta(days=step.frequency_days)).isoformat(),
                    "completed": False,
                }
                for step in steps
            ],
            "created_at": datetime.now().isoformat(),
        }
        self.patient_plans[patient_id] = plan
        return plan

    def record_adherence(
        self,
        patient_id: str,
        step_id: str,
        completed: bool,
        notes: str = "",
    ) -> bool:
        plan = self.patient_plans.get(patient_id)
        if not plan:
            return False

        for step in plan["steps"]:
            if step["step_id"] == step_id:
                step["completed"] = completed
                self.adherence_log[patient_id].append({
                    "step_id": step_id,
                    "completed": completed,
                    "notes": notes,
                    "timestamp": datetime.now().isoformat(),
                })
                return True
        return False

    def get_adherence_rate(self, patient_id: str) -> float:
        log = self.adherence_log.get(patient_id, [])
        if not log:
            return 0.0
        completed = sum(1 for entry in log if entry["completed"])
        return completed / len(log)

    def get_overdue_steps(self, patient_id: str) -> list[dict]:
        plan = self.patient_plans.get(patient_id)
        if not plan:
            return []

        now = datetime.now()
        overdue = []
        for step in plan["steps"]:
            if step["completed"]:
                continue
            due = datetime.fromisoformat(step["due_date"])
            if now > due:
                overdue.append({
                    "step_id": step["step_id"],
                    "name": step["name"],
                    "due_date": step["due_date"],
                    "days_overdue": (now - due).days,
                })
        return overdue


class TelemedicineScheduler:
    def __init__(self):
        self.appointments: dict[str, Appointment] = []
        self._appt_counter = 0

    def schedule(
        self,
        patient_id: str,
        provider_id: str,
        scheduled_time: datetime,
        interpreter_needed: bool = False,
        interpreter_language: str | None = None,
    ) -> Appointment:
        self._appt_counter += 1
        appt = Appointment(
            appointment_id=f"appt_{self._appt_counter}",
            patient_id=patient_id,
            provider_id=provider_id,
            scheduled_time=scheduled_time,
            interpreter_needed=interpreter_needed,
            interpreter_language=interpreter_language,
        )
        self.appointments.append(appt)
        return appt

    def complete(self, appointment_id: str) -> bool:
        for appt in self.appointments:
            if appt.appointment_id == appointment_id:
                appt.status = AppointmentStatus.COMPLETED
                return True
        return False

    def cancel(self, appointment_id: str) -> bool:
        for appt in self.appointments:
            if appt.appointment_id == appointment_id:
                appt.status = AppointmentStatus.CANCELLED
                return True
        return False

    def get_provider_schedule(self, provider_id: str) -> list[dict]:
        return [
            {
                "appointment_id": a.appointment_id,
                "patient_id": a.patient_id,
                "time": a.scheduled_time.isoformat(),
                "status": a.status.value,
                "interpreter": a.interpreter_language if a.interpreter_needed else None,
            }
            for a in self.appointments
            if a.provider_id == provider_id
        ]

    def get_stats(self) -> dict:
        status_counts = defaultdict(int)
        interpreter_count = 0
        for a in self.appointments:
            status_counts[a.status.value] += 1
            if a.interpreter_needed:
                interpreter_count += 1
        return {
            "total_appointments": len(self.appointments),
            "by_status": dict(status_counts),
            "interpreter_needed": interpreter_count,
        }


def main() -> None:
    print("=== Health Equity Demo ===\n")

    # 1. SDOH Assessment
    print("--- SDOH Assessment ---")
    assessment = SDOHAssessment("pt_001")
    assessment.add_response("food_security", "Sometimes I worry about running out of food before I can buy more")
    assessment.add_response("housing_stability", "I have a stable place to live")
    assessment.add_response("transportation", "I often have trouble getting to my medical appointments")
    assessment.add_response("financial_toxicity", "Medical bills are causing me significant financial stress")
    assessment.add_response("social_isolation", "I feel lonely and isolated from others most days")

    results = assessment.get_results()
    print(f"  Overall risk: {results['overall_risk']}")
    print(f"  High-risk domains: {results['high_risk_domains']}")
    print(f"  Risk score: {results['total_risk_score']}")

    # 2. Resource Referral
    print("\n--- Resource Referrals ---")
    rrn = ResourceReferralNetwork()
    rrn.add_resource("fb_01", "food", "Downtown Food Bank", (40.71, -74.00), "555-0201")
    rrn.add_resource("fb_02", "food", "Eastside Pantry", (40.72, -74.01), "555-0202")
    rrn.add_resource("tr_01", "transportation", "Medicaid Transport", (40.71, -74.00), "555-0301")
    rrn.add_resource("mh_01", "mental_health", "Community Counseling", (40.70, -73.99), "555-0401")

    referrals = rrn.match_referrals(assessment, patient_location=(40.71, -74.00))
    for r in referrals:
        print(f"  [{r['priority']}] {r['resource_name']} ({r['category']}) — {r['distance_km']}km")

    # 3. Disparities Analysis
    print("\n--- Disparities Analysis ---")
    da = DisparitiesAnalyzer()
    da.add_community_data(community_id="zip_10001", population=50000, primary_care_physicians=12,
                          ed_visits_per_1000=450, uninsured_rate=0.15, median_income=35000, life_expectancy=76.2)
    da.add_community_data(community_id="zip_10025", population=75000, primary_care_physicians=8,
                          ed_visits_per_1000=620, uninsured_rate=0.28, median_income=28000, life_expectancy=72.8)

    disparities = da.identify_disparities()
    for d in disparities:
        print(f"  {d.indicator}: {d.ratio}x — {d.interpretation}")

    eq = da.get_equity_score("zip_10025")
    print(f"  Equity score (zip_10025): {eq['equity_score']} — {eq['recommendation']}")

    # 4. Resource Allocation
    print("\n--- Resource Allocation ---")
    ra = ResourceAllocator()
    ra.add_community("district_a", 10000, 0.8, 0.6, 5)
    ra.add_community("district_b", 8000, 0.5, 0.3, 12)
    ra.add_community("district_c", 12000, 0.7, 0.7, 8)

    allocation = ra.optimize(total_resources=50, resource_type="care_managers")
    for a in allocation:
        print(f"  {a.community_id}: {a.allocated} (need={a.need_score}, equity={a.equity_weight})")

    # 5. Care Matching
    print("\n--- Care Matching ---")
    cme = CareMatchingEngine()
    cme.add_provider(Provider("p1", "Dr. Amara Okafor", "primary_care", ["en", "ig"], ["nigerian", "west_african"],
                              [InsuranceType.MEDICAID, InsuranceType.UNINSURED], (40.71, -74.00)))
    cme.add_provider(Provider("p2", "Dr. Wei Zhang", "primary_care", ["en", "zh"], ["chinese"],
                              [InsuranceType.MEDICAID, InsuranceType.EMPLOYER], (40.72, -74.01)))

    patient = Patient("pt_001", "Chinwe Okafor", "1985-03-15", "ig", InsuranceType.MEDICAID,
                      cultural_preferences=["nigerian", "west_african"])
    matches = cme.find_matches(patient, specialty_required="primary_care")
    for m in matches:
        print(f"  {m['name']}: score={m['score']}, lang={m['language_match']}, ins={m['insurance_match']}")

    # 6. Chronic Disease Management
    print("\n--- Chronic Disease Management ---")
    cdm = ChronicDiseaseManager()
    plan = cdm.create_care_plan("pt_001", CarePathway.DIABETES)
    print(f"  Care plan: {plan['pathway']}, steps: {len(plan['steps'])}")
    cdm.record_adherence("pt_001", "d1", True, "A1C at 7.2%")
    cdm.record_adherence("pt_001", "d2", True, "No retinopathy")
    rate = cdm.get_adherence_rate("pt_001")
    print(f"  Adherence rate: {rate:.0%}")

    # 7. Telemedicine
    print("\n--- Telemedicine Scheduling ---")
    ts = TelemedicineScheduler()
    appt = ts.schedule("pt_001", "p1", datetime.now() + timedelta(days=3), True, "ig")
    ts.complete(appt.appointment_id)
    stats = ts.get_stats()
    print(f"  Appointments: {stats['total_appointments']}, Interpreter needed: {stats['interpreter_needed']}")


if __name__ == "__main__":
    main()

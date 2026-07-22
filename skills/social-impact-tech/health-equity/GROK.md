---
name: "health-equity"
category: "social-impact-tech"
version: "1.0.0"
tags: ["social-impact-tech", "health-equity"]
---

# Health Equity — Healthcare Access & Social Determinants Toolkit

## Overview

Health equity means that everyone has a fair and just opportunity to be as healthy as possible — requiring the removal of obstacles such as poverty, discrimination, and their consequences, including lack of access to good jobs with fair pay, quality education and housing, safe environments, and health care. This module provides a Python toolkit for building health equity platforms: analyzing healthcare access disparities, supporting telemedicine delivery, equipping community health workers, tracking social determinants of health (SDOH), optimizing health resource allocation, matching culturally competent care providers, navigating insurance systems, and managing chronic disease programs.

The toolkit models the complex interplay between social determinants and health outcomes, enabling organizations to identify disparities by geography, race/ethnicity, income, language, and insurance status. It includes SDOH screening tools, resource referral networks (using food, housing, transportation, and employment data), and care coordination workflows that bridge clinical and community-based services. The resource allocation engine uses optimization algorithms to distribute limited health resources (vaccines, screenings, care managers) to communities with the greatest need, accounting for both disease burden and access barriers.

For telemedicine platforms, the toolkit provides appointment scheduling with interpreter service integration, connectivity-aware quality optimization, and digital literacy accommodation. The chronic disease management module supports evidence-based care pathways, medication adherence tracking, remote monitoring data integration, and outcome measurement. All components are designed with HIPAA compliance considerations, data minimization principles, and explicit consent management for data sharing between clinical and social service organizations.

## Core Capabilities

- **Health Disparities Analysis**: Identify and quantify health access disparities across demographics, geographies, and social factors with statistical significance testing and visualization data.
- **Social Determinant of Health (SDOH) Tracking**: Screen patients for food insecurity, housing instability, transportation barriers, financial toxicity, and social isolation with validated instruments.
- **Telemedicine Platform Support**: Appointment scheduling, interpreter service integration, connectivity quality adaptation, digital literacy tools, and clinical documentation templates.
- **Community Health Worker (CHW) Tools**: Visit tracking, care plan management, resource referral workflows, outcome documentation, and field data collection for CHW programs.
- **Health Resource Allocation**: Optimization engine for distributing limited resources (vaccines, screenings, care managers) based on need scoring, equity weighting, and access barrier analysis.
- **Culturally Competent Care Matching**: Match patients with providers based on language, cultural background, insurance acceptance, specialty, and availability.
- **Insurance Navigation**: Plan comparison tools, eligibility checking, enrollment assistance workflows, and cost estimation for uninsured/underinsured populations.
- **Chronic Disease Management**: Evidence-based care pathways, medication adherence tracking, remote monitoring data integration, outcome measurement, and care coordination.

## Usage Examples

### SDOH Screening and Resource Referral

```python
from health_equity import SDOHAssessment, ResourceReferralNetwork

# Screen a patient for social determinants
assessment = SDOHAssessment(patient_id="pt_001")
assessment.add_response("food_security", "Sometimes I worry about running out of food")
assessment.add_response("housing_stability", "I have a stable place to live")
assessment.add_response("transportation", "I have trouble getting to appointments")
assessment.add_response("financial_toxicity", "Medical bills are causing significant stress")

results = assessment.get_results()
print(f"Risk domains: {results['high_risk_domains']}")
print(f"Total risk score: {results['total_risk_score']}")

# Connect to resource referrals
referral_network = ResourceReferralNetwork()
referral_network.add_resource("food_bank_01", "food", "Community Food Bank", (40.71, -74.00))
referral_network.add_resource("housing_01", "housing", "Emergency Shelter Network", (40.72, -74.01))

referrals = referral_network.match referrals(assessment)
for r in referrals:
    print(f"Referral: {r['resource_name']} ({r['category']}) — distance: {r['distance_km']:.1f}km")
```

### Health Disparities Dashboard

```python
from health_equity import DisparitiesAnalyzer

analyzer = DisparitiesAnalyzer()

analyzer.add_community_data(
    community_id="zip_10001",
    population=50000,
    primary_care_physicians=12,
    ed_visits_per_1000=450,
    uninsured_rate=0.15,
    median_income=35000,
    life_expectancy=76.2,
)

analyzer.add_community_data(
    community_id="zip_10025",
    population=75000,
    primary_care_physicians=8,
    ed_visits_per_1000=620,
    uninsured_rate=0.28,
    median_income=28000,
    life_expectancy=72.8,
)

disparities = analyzer.identify_disparities()
for d in disparities:
    print(f"{d['indicator']}: {d['ratio']:.2f}x disparity — {d['interpretation']}")
```

### Resource Allocation Optimization

```python
from health_equity import ResourceAllocator

allocator = ResourceAllocator()

allocator.add_community(
    community_id="district_a",
    population=10000,
    disease_burden_score=0.8,
    access_barrier_score=0.6,
    existing_resources=5,
)

allocator.add_community(
    community_id="district_b",
    population=8000,
    disease_burden_score=0.5,
    access_barrier_score=0.3,
    existing_resources=12,
)

allocation = allocator.optimize(total_resources=50, resource_type="care_managers")
for item in allocation:
    print(f"{item['community_id']}: allocated {item['allocated']} "
          f"(need_score={item['need_score']:.2f}, equity_weight={item['equity_weight']:.2f})")
```

## Best Practices

1. **Center the communities you serve**: Health equity work must be driven by the people and communities most affected by health disparities. Include community members in program design, implementation, and evaluation. Nothing about us without us.

2. **Use validated SDOH screening instruments**: Social determinant assessments should use validated tools (PRAPARE, AHC-HRSN, Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences). Avoid ad hoc screening questions that haven't been tested for reliability and cultural validity.

3. **Address root causes, not just symptoms**: Connecting a food-insecure patient to a food bank is important, but it doesn't solve food insecurity. Advocate for policy changes that address structural causes: living wages, affordable housing, Medicaid expansion, transportation infrastructure.

4. **Protect patient data rigorously**: Health equity platforms handle extremely sensitive data — social needs, immigration status, income, health conditions. Implement HIPAA-compliant data handling, explicit consent for data sharing, data minimization, and clear policies about how data is used.

5. **Measure outcomes, not just outputs**: Tracking the number of patients screened for SDOH is an output. Tracking whether screening leads to resource connection, and whether resource connection improves health outcomes, is an outcome. Design measurement systems that capture impact.

6. **Ensure linguistic and cultural competence**: Health equity platforms must support the languages and cultural contexts of the populations they serve. This means more than translation — it means culturally adapted content, community health workers from the community, and provider matching that considers cultural competence.

7. **Account for the digital divide**: Telemedicine and digital health tools can exacerbate disparities if they assume universal smartphone access, broadband internet, and digital literacy. Design for SMS-based interactions, low-bandwidth modes, and phone-based alternatives.

8. **Build for sustainability, not grant cycles**: Many health equity programs are funded by time-limited grants and collapse when funding ends. Design platforms and programs with sustainable funding models, community ownership, and open-source components that persist beyond individual grants.

9. **Validate screening tools across populations**: SDOH screening instruments developed in one population may not be valid in another. Always validate reliability, cultural appropriateness, and predictive validity before deploying a screening tool at scale.

10. **Implement feedback loops with community health workers**: CHWs are the front line of health equity work and often identify system issues that data alone cannot reveal. Build structured feedback mechanisms so CHW observations inform platform improvements and policy advocacy.

11. **Use stratified analysis for disparity measurement**: Aggregate statistics mask disparities. Always stratify outcome data by race/ethnicity, income, insurance status, language, and geography to reveal inequities hidden in averages.

12. **Design for interoperability from day one**: Health equity platforms must exchange data with EHRs, public health departments, social service organizations, and 211 referral networks. Use FHIR R4 resources and HL7 v2 interfaces to ensure data can flow across organizational boundaries.

13. **Conduct regular equity impact assessments**: Before deploying new features or policies, assess whether they might inadvertently widen disparities. A telemedicine feature that requires high-speed broadband may improve access for urban patients while excluding rural ones.

14. **Maintain community advisory boards**: Establish ongoing relationships with community organizations, patient advocates, and public health experts who can provide real-world feedback on platform design, data use, and program effectiveness.

15. **Document and share methodologies transparently**: Health equity measurement methods, scoring algorithms, and data sources should be documented openly so communities can understand and challenge how their data is being used to drive resource allocation decisions.

## Configuration

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hipaa_mode` | `bool` | `True` | Enable HIPAA-compliant data handling with encryption at rest and in transit |
| `consent_required` | `bool` | `True` | Require explicit patient consent before sharing data across organizations |
| `data_minimization` | `bool` | `True` | Collect only the minimum data necessary for the specific use case |
| `interpreter_service` | `str` | `"on-demand"` | Interpreter integration mode: `on-demand`, `pre-scheduled`, or `disabled` |
| `screening_instrument` | `str` | `"PRAPARE"` | SDOH screening instrument: `PRAPARE`, `AHC-HRSN`, or `custom` |
| `allocation_algorithm` | `str` | `"equity_weighted"` | Resource allocation strategy: `equity_weighted`, `need_based`, or `equal` |
| `language_support` | `list[str]` | `["en","es"]` | Supported languages for UI and content delivery |
| `telemedicine_bandwidth` | `str` | `"adaptive"` | Video quality mode: `high`, `medium`, `low`, or `adaptive` |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Health Equity Platform                 │
├──────────┬──────────┬──────────┬──────────┬─────────────┤
│ SDOH     │ Resource │ Tele-    │ CHW      │ Insurance   │
│ Screening│ Referral │ medicine │ Tools    │ Navigation  │
├──────────┴──────────┴──────────┴──────────┴─────────────┤
│              Resource Allocation Engine                  │
├─────────────────────────────────────────────────────────┤
│    Consent Manager  │  Data Minimizer  │  Audit Logger  │
├─────────────────────────────────────────────────────────┤
│         FHIR-Compatible Data Layer (HL7 R4)             │
└─────────────────────────────────────────────────────────┘
```

## Key Metrics

- **Disparity Ratio**: Ratio of the worst-performing to best-performing community on a given indicator (target: < 1.5x)
- **Resource Connection Rate**: Percentage of screened patients successfully connected to at least one resource
- **Care Gap Closure Rate**: Percentage of identified care gaps addressed within 30 days
- **SDOH Risk Score**: Composite score (0-100) combining food security, housing, transportation, and financial toxicity domains
- **Equity Index**: Population-weighted average of access barrier scores across all communities

## Use Cases

- **Federally Qualified Health Centers (FQHCs)**: Deploy SDOH screening at intake, connect patients to 211 resource networks, track care coordination outcomes for HRSA reporting
- **Hospital Community Health Needs Assessments**: Analyze zip-code-level disparities in ED utilization, chronic disease prevalence, and primary care access to satisfy IRS Form 990 Schedule H requirements
- **Public Health Emergency Response**: Prioritize vaccine distribution, testing sites, and therapeutics to communities with highest SDOH burden and lowest access scores
- **Medicaid Managed Care Organizations**: Meet CMS health equity requirements by integrating SDOH data into care management platforms and tracking disparities reduction
- **Community Health Worker Programs**: Equip CHWs with mobile tools for visit documentation, resource referrals, care plan tracking, and outcome measurement in the field

## Related Modules

- [accessibility-tools](../accessibility-tools/GROK.md) — Accessible health information delivery
- [community-platforms](../community-platforms/GROK.md) — Community health worker coordination and peer support
- [crisis-response](../crisis-response/GROK.md) — Health resource tracking during emergencies
- [education-access](../education-access/GROK.md) — Health literacy and patient education

## Advanced Health Data Systems

### Electronic Health Record (EHR) Integration

Modern health equity platforms must integrate with existing EHR systems to exchange patient data securely. The toolkit supports FHIR R4 resources and HL7 v2 interfaces:

```python
from health_equity import EHRIntegration, FHIRClient, PatientBundle

# Configure FHIR client
fhir_client = FHIRClient(
    base_url="https://fhir.hospital.org/r4",
    auth_type="oauth2",
    client_id="health_equity_app",
    scopes=["patient/*.read", "patient/*.write"]
)

# Create EHR integration
ehr = EHRIntegration(
    fhir_client=fhir_client,
    supported_resources=["Patient", "Condition", "Observation", "ServiceRequest"],
    sync_interval_hours=24,
    conflict_resolution="server_wins"
)

# Fetch patient data from EHR
patient_bundle = ehr.get_patient("patient_001")
print(f"Patient Data Retrieved:")
print(f"  Name: {patient_bundle.name}")
print(f"  DOB: {patient_bundle.birth_date}")
print(f"  Conditions: {len(patient_bundle.conditions)}")
print(f"  Medications: {len(patient_bundle.medications)}")

# Push SDOH assessment to EHR
sdoh_assessment = {
    "resourceType": "Observation",
    "status": "final",
    "category": [{
        "coding": [{
            "system": "http://terminology.hl7.org/CodeSystem/observation-category",
            "code": "survey"
        }]
    }],
    "code": {
        "coding": [{
            "system": "http://loinc.org",
            "code": "89555-7",
            "display": "Accountable Health Communities social determinants of health screening"
        }]
    },
    "subject": {"reference": "Patient/patient_001"},
    "effectiveDateTime": "2026-06-15",
    "valueCodeableConcept": {
        "coding": [{
            "system": "http://health-equity.example.org/sdoh",
            "code": "food_insecurity",
            "display": "Food Insecurity"
        }]
    }
}

result = ehr.push_observation(sdoh_assessment)
print(f"\nSDOH Assessment Pushed to EHR:")
print(f"  Observation ID: {result.observation_id}")
print(f"  Status: {result.status}")
print(f"  Last Updated: {result.last_updated}")
```

### Telemedicine Platform with Accessibility

```python
from health_equity import TelemedicinePlatform, VideoConference, AccessibilityFeatures

# Configure telemedicine platform
platform = TelemedicinePlatform(
    video_provider="twilio",
    bandwidth_adaptation=True,
    accessibility_features=AccessibilityFeatures(
        captions_enabled=True,
        sign_language_interpreter=True,
        screen_reader_compatible=True,
        keyboard_navigation=True,
        high_contrast_mode=True,
        font_size_adjustable=True
    ),
    interpreter_service="on-demand",
    supported_languages=["en", "es", "zh", "vi", "ar"]
)

# Schedule telemedicine appointment
appointment = platform.schedule_appointment(
    patient_id="patient_001",
    provider_id="provider_001",
    appointment_type="follow_up",
    preferred_language="es",
    accessibility_needs=["captions", "large_font"],
    interpreter_required=True,
    interpreter_language="spanish"
)

print(f"Telemedicine Appointment Scheduled:")
print(f"  Appointment ID: {appointment.appointment_id}")
print(f"  Date/Time: {appointment.datetime}")
print(f"  Provider: {appointment.provider_name}")
print(f"  Interpreter: {appointment.interpreter_name}")
print(f"  Accessibility features: {appointment.accessibility_features}")

# Start video session with quality adaptation
session = platform.start_session(
    appointment_id=appointment.appointment_id,
    patient_device="mobile",
    connection_quality="adaptive"
)

print(f"\nVideo Session:")
print(f"  Session ID: {session.session_id}")
print(f"  Video quality: {session.video_quality}")
print(f"  Audio quality: {session.audio_quality}")
print(f"  Captions enabled: {session.captions_enabled}")
print(f"  Interpreter connected: {session.interpreter_connected}")
```

### Community Health Worker (CHW) Mobile Tools

```python
from health_equity import CHWMobileApp, VisitTracker, CarePlanManager

# Configure CHW mobile app
chw_app = CHWMobileApp(
    offline_mode=True,
    gps_tracking=True,
    photo_documentation=True,
    voice_recording=True,
    data_sync_interval_hours=12
)

# Track CHW visit
visit = chw_app.record_visit(
    chw_id="chw_001",
    patient_id="patient_001",
    visit_type="home_visit",
    location=(40.7128, -74.0060),
    duration_minutes=45,
    activities=[
        "sdoh_screening",
        "medication_review",
        "care_plan_update",
        "resource_referral"
    ],
    notes="Patient reports difficulty affording medications. Referred to pharmacy assistance program.",
    photos=["patient_home_exterior.jpg"]
)

print(f"CHW Visit Recorded:")
print(f"  Visit ID: {visit.visit_id}")
print(f"  Date: {visit.visit_date}")
print(f"  Duration: {visit.duration_minutes} minutes")
print(f"  Activities: {visit.activities}")
print(f"  GPS captured: {visit.gps_captured}")

# Manage care plan
care_plan = CarePlanManager(chw_app)
patient_care_plan = care_plan.get_care_plan("patient_001")

print(f"\nCare Plan for Patient:")
print(f"  Goals: {len(patient_care_plan.goals)}")
for goal in patient_care_plan.goals:
    print(f"    - {goal.description} (target: {goal.target_date})")
    print(f"      Progress: {goal.progress:.0%}")

# Add new care plan goal
new_goal = care_plan.add_goal(
    patient_id="patient_001",
    description="Improve medication adherence",
    target_date="2026-09-15",
    interventions=["pill_organizer", "daily_reminders", "pharmacy_sync"],
    success_criteria="Take medications as prescribed 80% of days"
)
print(f"\nNew Goal Added: {new_goal.description}")
```

### Health Disparities Analytics Dashboard

```python
from health_equity import DisparitiesDashboard, StratifiedAnalysis, TrendAnalysis

# Create disparities dashboard
dashboard = DisparitiesDashboard(
    data_sources=["ehr", "claims", "sdoh_screening", "census"],
    update_frequency="daily",
    visualization_engine="plotly"
)

# Add community data with stratification
communities = [
    {
        "id": "zip_10001",
        "population": 50000,
        "demographics": {
            "white": 0.40, "black": 0.30, "hispanic": 0.20, "asian": 0.10
        },
        "health_metrics": {
            "diabetes_prevalence": 0.12,
            "hypertension_prevalence": 0.35,
            "obesity_rate": 0.38,
            "life_expectancy": 76.2
        },
        "access_metrics": {
            "primary_care_physicians_per_1000": 0.24,
            "ed_visits_per_1000": 450,
            "uninsured_rate": 0.15,
            "medicaid_coverage": 0.25
        }
    },
    {
        "id": "zip_10025",
        "population": 75000,
        "demographics": {
            "white": 0.20, "black": 0.50, "hispanic": 0.25, "asian": 0.05
        },
        "health_metrics": {
            "diabetes_prevalence": 0.18,
            "hypertension_prevalence": 0.45,
            "obesity_rate": 0.48,
            "life_expectancy": 72.8
        },
        "access_metrics": {
            "primary_care_physicians_per_1000": 0.11,
            "ed_visits_per_1000": 620,
            "uninsured_rate": 0.28,
            "medicaid_coverage": 0.35
        }
    }
]

for community in communities:
    dashboard.add_community_data(community)

# Generate disparities report
report = dashboard.generate_disparities_report(
    metrics=["diabetes_prevalence", "life_expectancy", "ed_visits_per_1000"],
    stratify_by=["race", "insurance_status"],
    time_period="current"
)

print(f"Health Disparities Report:")
print(f"  Communities analyzed: {report.communities_analyzed}")
print(f"  Metrics assessed: {report.metrics_assessed}")
print(f"  Disparities identified: {report.disparities_identified}")

for disparity in report.disparities[:5]:
    print(f"\n  {disparity.metric}:")
    print(f"    Highest: {disparity.highest_value} ({disparity.highest_community})")
    print(f"    Lowest: {disparity.lowest_value} ({disparity.lowest_community})")
    print(f"    Ratio: {disparity.ratio:.2f}x")
    print(f"    Statistical significance: {disparity.p_value:.4f}")
    print(f"    Interpretation: {disparity.interpretation}")
```

### Resource Allocation Optimization

```python
from health_equity import ResourceAllocationOptimizer, EquityScoring, NeedAssessment

# Configure resource allocation optimizer
optimizer = ResourceAllocationOptimizer(
    optimization_goal="maximize_equity",
    constraints={
        "budget_limit": 1000000,
        "minimum_per_community": 50000,
        "resource_types": ["vaccines", "screenings", "care_managers", "transportation"]
    },
    equity_weights={
        "disease_burden": 0.4,
        "access_barriers": 0.3,
        "socioeconomic_status": 0.2,
        "historical_disinvestment": 0.1
    }
)

# Add communities with need assessment
communities = [
    {
        "id": "district_a",
        "population": 10000,
        "need_scores": {
            "disease_burden": 0.8,
            "access_barriers": 0.6,
            "socioeconomic_status": 0.7,
            "historical_disinvestment": 0.5
        },
        "existing_resources": 5
    },
    {
        "id": "district_b",
        "population": 8000,
        "need_scores": {
            "disease_burden": 0.5,
            "access_barriers": 0.3,
            "socioeconomic_status": 0.4,
            "historical_disinvestment": 0.2
        },
        "existing_resources": 12
    }
]

for community in communities:
    optimizer.add_community(community)

# Optimize allocation
allocation = optimizer.optimize(total_budget=500000, resource_type="care_managers")

print(f"Resource Allocation Optimization:")
print(f"  Total budget: ${allocation.total_budget:,.2f}")
print(f"  Resource type: {allocation.resource_type}")
print(f"  Communities served: {len(allocation.allocations)}")

for item in allocation.allocations:
    print(f"\n  {item.community_id}:")
    print(f"    Population: {item.population:,}")
    print(f"    Need score: {item.need_score:.2f}")
    print(f"    Equity weight: {item.equity_weight:.2f}")
    print(f"    Allocated: {item.allocated} {allocation.resource_type}")
    print(f"    Cost: ${item.cost:,.2f}")
    print(f"    Impact estimate: {item.impact_estimate:.1%}")

# Calculate equity index
equity_index = optimizer.calculate_equity_index()
print(f"\nEquity Index: {equity_index.overall_score:.2f}")
print(f"  Access equity: {equity_index.access_equity:.2f}")
print(f"  Outcome equity: {equity_index.outcome_equity:.2f}")
print(f"  Resource equity: {equity_index.resource_equity:.2f}")
```

### Insurance Navigation and Enrollment

```python
from health_equity import InsuranceNavigator, PlanComparison, EnrollmentAssistant

# Configure insurance navigator
navigator = InsuranceNavigator(
    marketplace="healthcare_gov",
    state="NY",
    languages=["en", "es", "zh"],
    assistance_level="full"
)

# Check patient eligibility
eligibility = navigator.check_eligibility(
    patient_id="patient_001",
    household_size=4,
    household_income=45000,
    immigration_status="permanent_resident",
    current_coverage=None
)

print(f"Insurance Eligibility:")
print(f"  Medicaid eligible: {eligibility.medicaid_eligible}")
print(f"  CHIP eligible: {eligibility.chip_eligible}")
print(f"  Marketplace subsidies: {eligibility.marketplace_subsidies}")
print(f"  Estimated premium: ${eligibility.estimated_premium:.2f}/month")

# Compare plans
plans = navigator.compare_plans(
    eligibility=eligibility,
    preferences={
        "max_premium": 300,
        "max_deductible": 2000,
        "preferred_providers": ["provider_001", "provider_002"],
        "essential_benefits": ["prescription", "mental_health", "maternity"]
    }
)

print(f"\nPlan Comparison:")
for plan in plans[:3]:
    print(f"\n  {plan.plan_name}:")
    print(f"    Monthly premium: ${plan.premium:.2f}")
    print(f"    Annual deductible: ${plan.deductible:,.2f}")
    print(f"    Out-of-pocket max: ${plan.out_of_pocket_max:,.2f}")
    print(f"    Copay primary care: ${plan.copay_primary_care:.2f}")
    print(f"    Network status: {plan.network_status}")

# Assist with enrollment
enrollment = EnrollmentAssistant(navigator)
enrollment_session = enrollment.start_enrollment(
    patient_id="patient_001",
    selected_plan=plans[0],
    enrollment_period="open"
)

print(f"\nEnrollment Session:")
print(f"  Session ID: {enrollment_session.session_id}")
print(f"  Steps remaining: {enrollment_session.steps_remaining}")
print(f"  Documents needed: {enrollment_session.documents_needed}")
```

### Chronic Disease Management

```python
from health_equity import ChronicDiseaseManager, CarePathway, MedicationTracker

# Configure chronic disease management
cdm = ChronicDiseaseManager(
    supported_conditions=["diabetes", "hypertension", "asthma", "copd"],
    care_pathways="evidence_based",
    remote_monitoring=True,
    outcome_tracking=True
)

# Create care pathway for diabetic patient
care_pathway = cdm.create_care_pathway(
    patient_id="patient_001",
    condition="diabetes",
    severity="moderate",
    comorbidities=["hypertension"],
    care_team=["primary_care", "endocrinology", "nutrition", "pharmacy"]
)

print(f"Care Pathway Created:")
print(f"  Patient: {care_pathway.patient_id}")
print(f"  Condition: {care_pathway.condition}")
print(f"  Duration: {care_pathway.duration_months} months")
print(f"  Goals: {len(care_pathway.goals)}")

for goal in care_pathway.goals:
    print(f"    - {goal.description}")
    print(f"      Target: {goal.target_value} by {goal.target_date}")

# Track medication adherence
med_tracker = MedicationTracker(cdm)
adherence = med_tracker.get_adherence(
    patient_id="patient_001",
    medication="metformin",
    period_days=30
)

print(f"\nMedication Adherence:")
print(f"  Medication: {adherence.medication_name}")
print(f"  Adherence rate: {adherence.adherence_rate:.1%}")
print(f"  Doses taken: {adherence.doses_taken}/{adherence.doses_prescribed}")
print(f"  Missed doses: {adherence.missed_doses}")
print(f"  Side effects reported: {adherence.side_effects}")

# Track remote monitoring data
remote_data = cdm.get_remote_monitoring_data("patient_001")
print(f"\nRemote Monitoring Data:")
print(f"  Blood glucose readings: {len(remote_data.glucose_readings)}")
print(f"  Average glucose: {remote_data.avg_glucose:.1f} mg/dL")
print(f"  Blood pressure readings: {len(remote_data.bp_readings)}")
print(f"  Average BP: {remote_data.avg_systolic}/{remote_data.avg_diastolic}")
print(f"  Weight trend: {remote_data.weight_trend}")
```

### Care Coordination Workflows

```python
from health_equity import CareCoordinator, ReferralNetwork, HandoffProtocol

# Configure care coordination
coordinator = CareCoordinator(
    referral_network=ReferralNetwork(
        providers=["primary_care", "specialty", "behavioral_health", "social_services"],
        insurance_networks=["medicaid", "medicare", "commercial"],
        community_resources=["food_bank", "housing_assistance", "transportation"]
    ),
    handoff_protocol=HandoffProtocol(
        sbar_format=True,
        includes_goals_of_care=True,
        medication_reconciliation=True,
        follow_up_scheduling=True
    )
)

# Create care coordination plan
coordination_plan = coordinator.create_plan(
    patient_id="patient_001",
    current_setting="emergency_department",
    disposition="home",
    needs=["primary_care_follow_up", "medication_management", "social_determinants"],
    urgency="high"
)

print(f"Care Coordination Plan:")
print(f"  Patient: {coordination_plan.patient_id}")
print(f"  Current setting: {coordination_plan.current_setting}")
print(f"  Disposition: {coordination_plan.disposition}")
print(f"  Referrals needed: {len(coordination_plan.referrals)}")

for referral in coordination_plan.referrals:
    print(f"\n  Referral: {referral.service_type}")
    print(f"    Provider: {referral.provider_name}")
    print(f"    Priority: {referral.priority}")
    print(f"    Appointment: {referral.appointment_date}")
    print(f"    Notes: {referral.clinical_notes}")

# Execute handoff
handoff = coordinator.execute_handoff(
    plan_id=coordination_plan.plan_id,
    from_provider="ed_physician",
    to_provider="primary_care",
    handoff_notes="Patient presents with uncontrolled diabetes. Requires medication adjustment and SDOH screening."
)

print(f"\nHandoff Completed:")
print(f"  Handoff ID: {handoff.handoff_id}")
print(f"  From: {handoff.from_provider}")
print(f"  To: {handoff.to_provider}")
print(f"  Confirmation: {handoff.confirmation_received}")
```

### Health Equity Outcome Measurement

```python
from health_equity import OutcomeMeasurement, EquityMetric, ImpactAssessment

# Configure outcome measurement
outcome_measure = OutcomeMeasurement(
    metrics=[
        "care_gap_closure_rate",
        "preventive_screening_rate",
        "medication_adherence",
        "ed_utilization",
        "hospital_readmission",
        "patient_satisfaction"
    ],
    stratification_dimensions=["race", "ethnicity", "insurance", "language", "zip_code"],
    time_periods=["baseline", "30_day", "90_day", "annual"]
)

# Measure outcomes for population
outcomes = outcome_measure.measure_outcomes(
    population_id="medicaid_beneficiaries",
    intervention="sdoh_screening_and_referral",
    start_date="2026-01-01",
    end_date="2026-06-30"
)

print(f"Health Equity Outcomes:")
print(f"  Population: {outcomes.population_id}")
print(f"  Intervention: {outcomes.intervention}")
print(f"  Time period: {outcomes.time_period}")

for metric in outcomes.metrics:
    print(f"\n  {metric.name}:")
    print(f"    Overall: {metric.overall_value:.1%}")
    print(f"    Improvement: {metric.improvement:.1%}")
    print(f"    Disparities:")
    for disparity in metric.disparities:
        print(f"      {disparity.group}: {disparity.value:.1%} (gap: {disparity.gap:.1%})")

# Conduct impact assessment
impact = ImpactAssessment(outcome_measure)
assessment = impact.assess_impact(
    intervention="sdoh_screening_and_referral",
    outcomes=outcomes,
    cost_data={
        "intervention_cost": 150000,
        "population_served": 500,
        "time_period_months": 6
    }
)

print(f"\nImpact Assessment:")
print(f"  Cost per patient: ${assessment.cost_per_patient:,.2f}")
print(f"  ROI: {assessment.roi:.2f}")
print(f"  QALY gained: {assessment.qalys_gained:.2f}")
print(f"  Cost per QALY: ${assessment.cost_per_qalY:,.2f}")
print(f"  Equity impact score: {assessment.equity_impact_score:.2f}")
```

### Data Governance and Privacy

```python
from health_equity import DataGovernance, ConsentManager, AuditLogger

# Configure data governance
governance = DataGovernance(
    hipaa_compliant=True,
    data_minimization=True,
    purpose_limitation=True,
    retention_policy={
        "patient_identifiers": "7_years",
        "clinical_data": "10_years",
        "sdoh_data": "3_years",
        "analytics_data": "2_years"
    },
    sharing_policies={
        "internal": "allowed_with_consent",
        "research": "allowed_with_irb_approval",
        "commercial": "prohibited"
    }
)

# Manage patient consent
consent_manager = ConsentManager(governance)

consent = consent_manager.record_consent(
    patient_id="patient_001",
    consent_type="data_sharing",
    scope=["treatment", "care_coordination", "quality_improvement"],
    recipients=["primary_care", "specialist", "pharmacy"],
    expiration_date="2027-06-15",
    withdrawal_allowed=True
)

print(f"Consent Recorded:")
print(f"  Consent ID: {consent.consent_id}")
print(f"  Type: {consent.consent_type}")
print(f"  Scope: {consent.scope}")
print(f"  Recipients: {consent.recipients}")
print(f"  Expiration: {consent.expiration_date}")

# Audit logging
audit_logger = AuditLogger(governance)

audit_logger.log_access(
    user_id="provider_001",
    patient_id="patient_001",
    access_type="view",
    resource="medical_record",
    purpose="treatment",
    ip_address="192.168.1.100"
)

# Generate audit report
audit_report = audit_logger.generate_report(
    patient_id="patient_001",
    start_date="2026-01-01",
    end_date="2026-06-30"
)

print(f"\nAudit Report:")
print(f"  Total accesses: {audit_report.total_accesses}")
print(f"  Unique users: {audit_report.unique_users}")
print(f"  Access types: {audit_report.access_types}")
print(f"  Any suspicious activity: {audit_report.suspicious_activity}")
```

### Integration with Public Health Systems

```python
from health_equity import PublicHealthIntegration, ReportableDisease, SurveillanceSystem

# Configure public health integration
ph_integration = PublicHealthIntegration(
    reporting_system="state_health_dept",
    reporting_threshold="immediate",
    required_fields=["diagnosis", "patient_demographics", "location"],
    electronic_reporting=True
)

# Report notifiable condition
report = ph_integration.report_condition(
    patient_id="patient_001",
    condition="tuberculosis",
    diagnosis_date="2026-06-15",
    facility="community_health_center",
    treating_provider="provider_001",
    patient_demographics={
        "age": 45,
        "gender": "male",
        "race": "black",
        "ethnicity": "non_hispanic",
        "zip_code": "10025"
    }
)

print(f"Public Health Report Submitted:")
print(f"  Report ID: {report.report_id}")
print(f"  Condition: {report.condition}")
print(f"  Status: {report.status}")
print(f"  Acknowledgment: {report.acknowledgment_received}")

# Access surveillance data
surveillance = SurveillanceSystem(ph_integration)
health_indicators = surveillance.get_indicators(
    geography="zip_10025",
    indicators=["tb_incidence", "diabetes_prevalence", "obesity_rate"],
    time_period="2025"
)

print(f"\nSurveillance Data for zip_10025:")
for indicator in health_indicators:
    print(f"  {indicator.name}: {indicator.value} per {indicator.denominator}")
    print(f"    Trend: {indicator.trend}")
    print(f"    State comparison: {indicator.state_comparison}")
```

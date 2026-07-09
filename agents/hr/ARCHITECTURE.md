# HR Agent — System Architecture

## 1. Executive Summary

The HR Agent is a comprehensive human resources management platform covering the full employee lifecycle — from recruitment through offboarding. It provides tools for employee management, recruitment pipeline tracking, performance reviews, compensation analysis, engagement surveys, compliance tracking, training management, leave management, benefits administration, attrition analysis, organizational structure, onboarding/offboarding workflows, and HR analytics dashboards.

The system is designed as an engine-based modular architecture where each domain concern lives in its own engine with isolated state, well-typed interfaces, and no circular dependencies. The orchestrator (`HRAgent`) composes these engines behind a facade, coordinating cross-domain workflows while presenting a single, simplified API surface.

---

## 2. High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│                              HR AGENT (Orchestrator)                                  │
├──────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                      │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐   │
│  │   Employee     │  │  Recruitment   │  │  Performance   │  │  Compensation    │   │
│  │   Manager      │  │   Pipeline     │  │   Manager      │  │   Analyzer       │   │
│  │                │  │                │  │                │  │                  │   │
│  │ • Hire/Term    │  │ • Candidates   │  │ • Reviews      │  │ • Salary records │   │
│  │ • Lifecycle    │  │ • Openings     │  │ • Goals        │  │ • Benchmarks     │   │
│  │ • Search       │  │ • Funnel       │  │ • 360 feedback │  │ • Pay equity     │   │
│  │ • Analytics    │  │ • Metrics      │  │ • Summaries    │  │ • History        │   │
│  └────────────────┘  └────────────────┘  └────────────────┘  └──────────────────┘   │
│                                                                                      │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐   │
│  │  Engagement    │  │     Leave      │  │   Compliance   │  │   Training       │   │
│  │  Analyzer      │  │    Manager     │  │   Tracker      │  │   Manager        │   │
│  │                │  │                │  │                │  │                  │   │
│  │ • Surveys      │  │ • Requests     │  │ • Requirements │  │ • Programs       │   │
│  │ • Responses    │  │ • Balances     │  │ • Expirations  │  │ • Assignments    │   │
│  │ • NPS scoring  │  │ • Policies     │  │ • Renewals     │  │ • Completions    │   │
│  │ • Dept analysis│  │ • Calendar     │  │ • Reports      │  │ • Scores         │   │
│  └────────────────┘  └────────────────┘  └────────────────┘  └──────────────────┘   │
│                                                                                      │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐  ┌──────────────────┐   │
│  │  Org Chart     │  │  Onboarding    │  │  Offboarding   │  │   Benefits       │   │
│  │  Manager       │  │  Manager       │  │  Manager       │  │   Manager        │   │
│  │                │  │                │  │                │  │                  │   │
│  │ • Structure    │  │ • Plans        │  │ • Exit tasks   │  │ • Enrollments    │   │
│  │ • Team trees   │  │ • Tasks        │  │ • Knowledge    │  │ • Coverage       │   │
│  │ • Span of ctrl │  │ • Progress     │  │   transfer     │  │ • Cost tracking  │   │
│  │ • Hierarchy    │  │ • Check-ins    │  │ • Exit survey  │  │ • Dependent mgmt │   │
│  └────────────────┘  └────────────────┘  └────────────────┘  └──────────────────┘   │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐  │
│  │                           Attrition Analyzer                                   │  │
│  │  • Risk scoring  • Factor analysis  • Retention actions  • Exit interviews    │  │
│  └────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                      │
│  ┌────────────────────────────────────────────────────────────────────────────────┐  │
│  │    Data Models (Employee, Candidate, Review, Goal, Leave, Compliance, etc.)   │  │
│  └────────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Component Deep Dives

### 3.1 Employee Manager

Full employee lifecycle management: hiring, updates, termination, search, headcount analytics, salary statistics, attrition rates, and diversity metrics.

```
hire_employee() ──► update_employee() ──► terminate_employee()
      │                    │                       │
      ▼                    ▼                       ▼
  Employee record     Update fields          Set status + date
  + auto-generate ID  + salary changes       + log termination
```

**State Machine:**
```
APPLICANT ──→ HIRED ──→ ACTIVE ──→ ON_LEAVE ──→ ACTIVE
                        │
                        ▼
                   TERMINATED ──→ REHIRED (optional)
```

**Key Methods:**
```python
class EmployeeManager:
    def hire_employee(self, first_name, last_name, email, department,
                      job_title, job_level, salary, **kwargs) -> Employee
    def update_employee(self, employee_id, **kwargs) -> Optional[Employee]
    def terminate_employee(self, employee_id, reason="") -> bool
    def get_employee(self, employee_id) -> Optional[Employee]
    def get_by_department(self, department) -> List[Employee]
    def get_headcount(self) -> Dict[str, int]
    def get_salary_statistics(self) -> Dict[str, Any]
    def get_attrition_rate(self, lookback_days=365) -> float
    def get_tenure_distribution(self) -> Dict[str, int]
    def get_diversity_metrics(self) -> Dict[str, Any]
    def search(self, query: str) -> List[Employee]
```

**Employee Data Model:**
```python
@dataclass
class Employee:
    employee_id: str
    first_name: str
    last_name: str
    email: str
    department: Department
    job_title: str
    job_level: JobLevel
    employment_status: EmploymentStatus
    salary: float
    hire_date: datetime
    manager_id: Optional[str]
    performance_score: float
    engagement_score: float
    gender: Optional[str]
    location: Optional[str]

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def tenure_years(self) -> float:
        delta = datetime.utcnow() - self.hire_date
        return delta.days / 365.25

    @property
    def annual_salary(self) -> float:
        return self.salary

    @property
    def total_compensation(self) -> float:
        return self.salary * 1.3  # Includes benefits estimate
```

**Enums:**
```python
class Department(Enum):
    ENGINEERING = "engineering"
    MARKETING = "marketing"
    SALES = "sales"
    HR = "hr"
    FINANCE = "finance"
    OPERATIONS = "operations"
    LEGAL = "legal"
    CUSTOMER_SUCCESS = "customer_success"
    DESIGN = "design"
    PRODUCT = "product"

class JobLevel(Enum):
    INTERN = "intern"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    MANAGER = "manager"
    DIRECTOR = "director"
    VP = "vp"
    C_LEVEL = "c_level"

class EmploymentStatus(Enum):
    ACTIVE = "active"
    ON_LEAVE = "on_leave"
    TERMINATED = "terminated"
    PROBATION = "probation"
    RESIGNED = "resigned"
```

### 3.2 Recruitment Pipeline

Applicant tracking with stage-based funnel management, offer lifecycle, and comprehensive metrics.

```
Job Opening ──► Candidate Applied ──► Screen ──► Interview Stages ──► Offer ──► Hire
                                                                      │
                                                                      ▼
                                                              Record / Reject
```

**Funnel Stages:**
```
APPLIED ──► PHONE_SCREEN ──► TECHNICAL_INTERVIEW ──► ON_SITE ──► OFFER ──► HIRED
   │              │                │                    │          │
   ▼              ▼                ▼                    ▼          ▼
 REJECTED     REJECTED         REJECTED             REJECTED    REJECTED
```

**Metrics Calculations:**
```
conversion_rate = stage_count / previous_stage_count
time_per_stage = avg(stage_end_date - stage_start_date)
overall_conversion = hired_count / applied_count
time_to_fill = opening_close_date - opening_posted_date
time_to_hire = offer_accept_date - application_date
```

### 3.3 Performance Manager

Review cycles, goal tracking with hierarchical goals, competency ratings, 360-degree feedback with weighted scoring.

```
Create Review ──► Set Ratings ──► 360 Feedback ──► Calibration ──► Final Rating
      │                                                        │
      ▼                                                        ▼
  Add Goals ──► Track Progress ──► Complete Goal        Promotion Decision
```

**360 Feedback Weighting:**
```
Self Assessment:        15%
Peer Feedback:          25%
Manager Feedback:       35%
Upward Feedback:        25%

Weighted Score = Σ (score × weight)
```

**Goal Hierarchy (OKR Style):**
```
Company Goal (O1)
├── Department Goal (O1-KR1)
│   ├── Team Goal (O1-KR1-KR1)
│   └── Individual Goal (O1-KR1-KR2)
└── Department Goal (O1-KR2)
    └── Team Goal (O1-KR2-KR1)
```

### 3.4 Compensation Analyzer

Salary analysis, market benchmarking, pay equity audits, compensation change history.

```
Add Record ──► Set Benchmark ──► Comp vs Benchmark ──► Pay Equity Audit
      │
      ▼
  Change History ──► Avg Increase Calculation
```

**Pay Equity Calculation:**
```
competitiveness_ratio = employee_salary / market_benchmark
equity_issues = find employees where ratio < 0.95 OR ratio > 1.05
pay_gap = avg(male_salary) - avg(female_salary)
```

### 3.5 Engagement Analyzer

Survey creation, response collection, NPS calculation, department-level analysis.

```
Create Survey ──► Submit Responses ──► Calculate NPS ──► Dept Analysis ──► Trends
```

**NPS Calculation:**
```
Promoters (9-10): count
Passives (7-8):   count
Detractors (0-6): count

NPS = ((promoters - detractors) / total_responses) × 100
Range: -100 to +100
```

### 3.6 Leave Manager

Request submission, approval workflow with balance deduction, balance tracking.

```
Submit Request ──► Approve/Deny ──► Update Balance ──► Calendar View
      │
      ▼
  Cancel ──► Reverse Balance Deduction
```

**Leave Balance Model:**
```python
@dataclass
class LeaveBalance:
    employee_id: str
    year: int
    balances: Dict[str, float]  # {"vacation": 15, "sick": 10, "personal": 5}
    used: Dict[str, float]      # {"vacation": 8, "sick": 2, "personal": 1}

    def remaining(self, leave_type: str) -> float:
        return self.balances.get(leave_type, 0) - self.used.get(leave_type, 0)

    def utilization_rate(self, leave_type: str) -> float:
        total = self.balances.get(leave_type, 0)
        if total == 0:
            return 0.0
        return self.used.get(leave_type, 0) / total
```

### 3.7 Compliance Tracker

Requirement tracking, expiration alerts, renewal management, compliance reporting.

```
Add Requirement ──► Track Status ──► Monitor Expiration ──► Renewal Alert
      │
      ▼
  Compliance Report ──► Category Breakdown ──► Non-Compliant List
```

### 3.8 Training Manager

Program creation, assignment with due dates, completion tracking, score recording.

```
Create Program ──► Assign Training ──► Complete ──► Record Score
      │
      ▼
  Employee Summary ──► Required Training Check ──► Overdue Alert
```

### 3.9 Org Chart Manager

Hierarchical structure management, team trees, span of control analysis.

```
Add Employee ──► Link Manager ──► Build Team Tree ──► Calculate Depth
      │
      ▼
  Get Direct Reports ──► Span of Control ──► Flat View Export
```

**Org Tree Structure:**
```
CEO
├── VP Engineering
│   ├── Director Backend
│   │   ├── Senior Engineer 1
│   │   ├── Senior Engineer 2
│   │   └── Junior Engineer
│   └── Director Frontend
│       ├── Senior Engineer 3
│       └── Designer
├── VP Sales
│   ├── Director Enterprise
│   │   └── Account Executive 1
│   └── Director SMB
│       ├── Account Executive 2
│       └── SDR 1
└── VP Marketing
    ├── Content Lead
    └── Growth Lead
```

### 3.10 Onboarding Manager

New hire onboarding with task creation, progress tracking, buddy/mentor assignment.

```
Create Plan ──► Add Tasks ──► Complete Tasks ──► Check Progress ──► Auto-Complete
```

### 3.11 Offboarding Manager

Employee departure workflow with exit interviews, knowledge transfer tracking.

```
Create Plan ──► Add Tasks ──► Track Progress ──► Exit Interview ──► Complete
```

### 3.12 Benefits Manager

Benefits enrollment, dependent management, employer/employee cost tracking.

```
Enroll Employee ──► Add Dependents ──► Track Costs ──► Summary Report
```

### 3.13 Attrition Analyzer

Multi-factor risk scoring, retention action recommendations, exit interview analysis.

```
Assess Risk ──► Identify Factors ──► Suggest Actions ──► Track Outcomes
      │
      ▼
  High Risk List ──► Exit Reason Analysis ──► Attrition Summary
```

**Risk Scoring Algorithm:**
```
risk_score = 0

if performance_score < 3.0:
    risk_score += 25
if engagement_score < 3.0:
    risk_score += 20
if tenure_years < 1.0:
    risk_score += 15
if salary_competitiveness_ratio < 0.90:
    risk_score += 20
if manager_rating < 3.5:
    risk_score += 10
if recent_promotion == False AND tenure > 2.0:
    risk_score += 10

risk_level:
  score >= 70 → HIGH
  score >= 40 → MEDIUM
  score < 40  → LOW
```

---

## 4. Employee Lifecycle Flow

```
  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │ Recruit  │ ─► │  Hire    │ ─► │ Develop  │ ─► │ Retain   │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘
       │               │               │               │
  Job posting     Onboarding     Training         Engagement
  Interviews      Paperwork      Reviews          Surveys
  Offer           Orientation    Goals            Compensation
                  Benefits       Mentoring        Promotions
                  Compliance                      Career Path
                                                          │
                                                          ▼
  ┌──────────┐    ┌──────────┐                             │
  │  Exit    │ ◄─ │ Separate │ ◄──────────────────────────┘
  └──────────┘    └──────────┘
       │
  Offboarding    Exit Interview
  Knowledge      Final Pay
  Transfer       Rehire Eligible
```

---

## 5. Data Flow

```
                    ┌──────────────────────────┐
                    │      HR Data Input        │
                    │  • New hire info          │
                    │  • Candidate applications │
                    │  • Review scores          │
                    │  • Leave requests         │
                    │  • Training completions   │
                    └────────────┬─────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
    ┌─────────▼─────────┐ ┌─────▼──────┐ ┌────────▼────────┐
    │ EmployeeManager   │ │Recruitment │ │ PerformanceMgr   │
    │ (Register →       │ │Pipeline    │ │ (Review →        │
    │  Hire → Track)    │ │(Apply →    │ │  Goal →          │
    │                   │ │ Hire)      │ │  360 Feedback)   │
    └─────────┬─────────┘ └─────┬──────┘ └────────┬────────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
    ┌─────────▼─────────┐ ┌─────▼──────┐ ┌────────▼────────┐
    │ CompAnalyzer      │ │LeaveMgr     │ │ Compliance      │
    │ (Record →         │ │(Submit →    │ │ Tracker         │
    │  Benchmark →      │ │ Approve →   │ │ (Track →        │
    │  Equity Audit)    │ │ Balance)    │ │  Report)        │
    └─────────┬─────────┘ └─────┬──────┘ └────────┬────────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
    ┌─────────▼─────────┐ ┌─────▼──────┐ ┌────────▼────────┐
    │ TrainingMgr       │ │ Onboarding │ │ Attrition        │
    │ (Program →        │ │ Manager    │ │ Analyzer         │
    │  Assign →         │ │ (Plan →    │ │ (Risk →          │
    │  Complete)        │ │  Tasks)    │ │  Actions)        │
    └─────────┬─────────┘ └─────┬──────┘ └────────┬────────┘
              │                  │                  │
              └──────────────────┼──────────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │   HR Analytics Dashboard  │
                    │  • Headcount metrics      │
                    │  • Turnover rate          │
                    │  • Engagement scores      │
                    │  • Compliance rate         │
                    │  • Training completion    │
                    │  • Salary statistics      │
                    │  • Attrition risk map     │
                    └──────────────────────────┘
```

---

## 6. Key Metrics

| Metric | Description | Target |
|--------|-------------|--------|
| Time to Fill | Days from opening to hire | < 30 days |
| Time to Hire | Days from application to offer | < 21 days |
| Offer Acceptance Rate | Offers accepted / offers made | > 85% |
| Turnover Rate | Terminations / avg headcount | < 15% annual |
| Engagement Score | Survey average (1-5) | > 4.0 |
| NPS Score | Net Promoter Score | > 30 |
| Training Completion | Completed / assigned | > 95% |
| Compliance Rate | Compliant / total requirements | > 98% |
| Pay Equity Ratio | Comp vs benchmark | 0.95 - 1.05 |
| Attrition Risk Score | Average risk assessment | < 0.3 |
| Onboarding Completion | Tasks completed / total | > 90% in 90 days |
| Exit Interview Completion | Exits with interview / total exits | > 80% |
| Cost Per Hire | Total recruiting cost / hires | < $5,000 |
| Revenue Per Employee | Annual revenue / headcount | Industry benchmark |
| Absence Rate | Absent days / total work days | < 3% |

---

## 7. Design Patterns

| Pattern | Usage | Component |
|---------|-------|-----------|
| **State** | Employee status lifecycle | EmployeeManager |
| **Strategy** | Multiple valuation methods | CompensationAnalyzer |
| **Template Method** | Onboarding/Offboarding task lists | OnboardingManager |
| **Observer** | Threshold alerting for compliance | ComplianceTracker |
| **Factory** | Auto-generated IDs | All Managers |
| **Composite** | Org chart hierarchy | OrgChartManager |
| **Facade** | Orchestrator pattern | HRAgent |
| **Chain of Responsibility** | Goal hierarchy | PerformanceManager |
| **Command** | Leave request approval workflow | LeaveManager |
| **Memento** | Compensation change history | CompensationAnalyzer |

---

## 8. Security & Compliance

- Employee PII protected (SSN, DOB, address, bank details)
- Audit trail for all data access and modifications
- Role-based access control (HR admin, manager, employee self-service)
- Data retention policies aligned with labor law requirements
- GDPR/CCPA compliance support for data subject rights
- Encryption at rest for sensitive employee data
- Access logging for compliance audits
- Leave request approval chain enforcement
- Benefits enrollment period enforcement
- Training completion verification for compliance items

**RBAC Roles:**
```
HR_ADMIN ──── Full access to all modules
HR_MANAGER ── Department-level access
MANAGER ───── Team-level access (direct reports only)
EMPLOYEE ──── Self-service (own data only)
AUDIT ─────── Read-only access to audit logs
```

**Data Classification:**
```
PUBLIC:       Job titles, departments, office locations
INTERNAL:     Salary ranges, headcount, org structure
CONFIDENTIAL: Individual salaries, SSN, bank details, reviews
RESTRICTED:   Medical records, disciplinary actions, legal holds
```

---

## 9. Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Data Structures | dataclasses, Enum, Dict, List |
| Statistics | statistics module |
| Date/Time | datetime, timedelta |
| ID Generation | UUID (truncated) |
| Logging | Python logging module |
| Serialization | JSON (for exports) |
| Optional | SQLite, PostgreSQL |
| API Integration | REST API patterns for HRIS |

---

## 10. Scalability Considerations

| Dimension | Strategy |
|-----------|----------|
| Employee volume | Indexed by ID, department, manager |
| Recruitment pipeline | Stage-based bucketing |
| Performance reviews | Time-partitioned by review cycle |
| Training records | Indexed by employee, status |
| Compliance items | Indexed by category, expiration date |
| Leave balances | Year-partitioned |
| Engagement surveys | Survey-partitioned with response aggregation |
| Analytics queries | Pre-computed summaries for dashboards |

**Capacity Planning:**
```
Small Org (< 100):     Single instance, in-memory storage
Medium Org (100-1000): Indexed dictionaries, JSON persistence
Large Org (1000+):     Database backend, query optimization
Enterprise (10000+):   Sharded storage, read replicas, caching
```

---

## 11. Extension Points

1. **HRIS Integration**: Connect to Workday, BambooHR, SAP SuccessFactors
2. **ATS Integration**: Greenhouse, Lever, iCIMS connectors
3. **LMS Integration**: LinkedIn Learning, Coursera, internal LMS
4. **Payroll Integration**: ADP, Paychex, Gusto connectors
5. **Custom Analytics**: Plug-in dashboard widgets
6. **Workflow Automation**: Custom approval chains and notifications
7. **API Layer**: RESTful endpoints for external system integration
8. **Reporting Engine**: Custom report templates and scheduling
9. **Mobile Access**: Employee self-service mobile interface
10. **AI/ML**: Predictive attrition, performance forecasting

---

## 12. Monitoring & Observability

| Signal | Method |
|--------|--------|
| Employee headcount | `employees.get_active_count()` |
| Recruitment pipeline | `recruitment.get_metrics()` |
| Performance completion | `performance.reviews` count |
| Engagement scores | `engagement.surveys` avg scores |
| Leave utilization | `leave.get_leave_summary()` |
| Compliance rate | `compliance.compliance_report()` |
| Training completion | `training.training_completion_rate()` |
| Attrition rate | `employees.get_attrition_rate()` |
| Risk distribution | `attrition.attrition_summary()` |
| Onboarding progress | `onboarding.onboarding_progress_report()` |
| Benefits cost | `benefits.total_employer_cost()` |

---

## 13. Glossary

| Term | Definition |
|------|-----------|
| ATS | Applicant Tracking System |
| HRIS | Human Resources Information System |
| LMS | Learning Management System |
| NPS | Net Promoter Score |
| 360 Review | Multi-rater performance feedback |
| BANT | Budget, Authority, Need, Timeline (qualification) |
| PTO | Paid Time Off |
| COBRA | Consolidated Omnibus Budget Reconciliation Act |
| FMLA | Family and Medical Leave Act |
| I-9 | Employment Eligibility Verification |
| CTC | Cost to Company |
| OKR | Objectives and Key Results |
| DEI | Diversity, Equity, and Inclusion |
| EEOC | Equal Employment Opportunity Commission |

---

## 14. Appendix: Design Decisions

| Decision | Rationale |
|----------|-----------|
| In-memory storage | Simplicity; persistence layer optional |
| Auto-generated IDs | Prevent ID collisions and human error |
| Separate onboarding/offboarding | Different workflows and requirements |
| Multi-factor attrition risk | More accurate than single-factor models |
| Weighted 360 feedback | Manager feedback weighted highest for relevance |
| Leave balance tracking | Ensures policy compliance and prevents over-use |
| Compliance renewal alerts | Prevents gaps in certifications and training |
| Goal hierarchy support | Enables OKR alignment and cascading goals |
| Separate benefits manager | Benefits are complex and need dedicated tracking |
| Exit interview analytics | Identifies systemic issues and improvement areas |
| UUID-based IDs | Global uniqueness without coordination |
| UTC timestamps | Avoid timezone confusion in multi-region orgs |
| Immutable audit trail | Append-only for compliance and debugging |

---

## 15. Error Handling

### Error Categories

```
┌─────────────────────────────────────────────────────────────┐
│                     Error Hierarchy                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  HRError (base)                                              │
│  ├── ValidationError                                         │
│  │   ├── InvalidEmployeeData                                 │
│  │   ├── DuplicateEmployeeEmail                              │
│  │   ├── InvalidSalaryRange                                  │
│  │   └── MissingRequiredField                                │
│  ├── NotFoundError                                           │
│  │   ├── EmployeeNotFound                                    │
│  │   ├── CandidateNotFound                                   │
│  │   ├── ReviewNotFound                                      │
│  │   └── ComplianceItemNotFound                              │
│  ├── StateError                                              │
│  │   ├── InvalidStatusTransition                             │
│  │   ├── InsufficientLeaveBalance                            │
│  │   ├── ReviewAlreadyCompleted                               │
│  │   └── OnboardingAlreadyCompleted                          │
│  └── PermissionError                                         │
│      ├── UnauthorizedAction                                  │
│      └── InsufficientPrivileges                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Error Response Format

```python
@dataclass
class HRErrorResponse:
    error_code: str          # "EMPLOYEE_NOT_FOUND"
    error_type: str          # "NotFoundError"
    message: str             # Human-readable description
    details: Dict[str, Any]  # Context-specific data
    timestamp: datetime      # When error occurred
    request_id: Optional[str]  # For correlation

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error": {
                "code": self.error_code,
                "type": self.error_type,
                "message": self.message,
                "details": self.details,
                "timestamp": self.timestamp.isoformat(),
                "request_id": self.request_id,
            }
        }
```

### Error Handling Best Practices

```python
# ✅ CORRECT: Validate before processing
def hire_employee(self, **kwargs) -> Employee:
    if not kwargs.get("email"):
        raise ValidationError("email", "Email is required")
    if self._email_exists(kwargs["email"]):
        raise DuplicateEmployeeEmail(kwargs["email"])
    # ... proceed with hiring

# ✅ CORRECT: Use structured error responses
try:
    employee = mgr.hire_employee(email="alice@co.com", ...)
except DuplicateEmployeeEmail as e:
    logger.warning(f"Duplicate email attempt: {e.email}")
    return {"error": "Email already in use", "code": "DUPLICATE_EMAIL"}

# ❌ WRONG: Never silently swallow errors
def hire_employee(self, **kwargs):
    try:
        # ... hire logic
    except Exception:
        pass  # BUG: Silent failure, no audit trail
```

---

## 16. Testing Strategy

### Unit Test Coverage Targets

| Component | Target Coverage | Critical Paths |
|-----------|----------------|----------------|
| EmployeeManager | > 95% | Hire, terminate, search |
| RecruitmentPipeline | > 90% | Stage advancement, offer lifecycle |
| PerformanceManager | > 90% | Review creation, 360 scoring |
| CompensationAnalyzer | > 95% | Pay equity, benchmark comparison |
| LeaveManager | > 95% | Balance tracking, approval workflow |
| ComplianceTracker | > 90% | Expiration alerts, renewal |
| TrainingManager | > 85% | Assignment, completion tracking |
| AttritionAnalyzer | > 90% | Risk scoring, factor analysis |

### Test Categories

```python
# Unit tests - isolated component testing
class TestEmployeeManager:
    def test_hire_employee_creates_record(self):
        mgr = EmployeeManager()
        emp = mgr.hire_employee(
            first_name="Test", last_name="User",
            email="test@co.com", department=Department.ENGINEERING,
            job_title="Engineer", job_level=JobLevel.MID, salary=100000
        )
        assert emp.employee_id is not None
        assert emp.full_name == "Test User"

    def test_terminate_employee_sets_status(self):
        mgr = EmployeeManager()
        emp = mgr.hire_employee(...)
        result = mgr.terminate_employee(emp.employee_id, reason="Resignation")
        assert result is True
        assert mgr.get_employee(emp.employee_id).employment_status == EmploymentStatus.TERMINATED

# Integration tests - cross-component workflows
class TestOnboardingWorkflow:
    def test_full_onboarding_lifecycle(self):
        agent = HRAgent()
        emp = agent.employees.hire_employee(...)
        plan = agent.onboarding.create_plan(emp.employee_id, ...)
        # Complete all tasks
        for task in plan.tasks:
            agent.onboarding.complete_task(plan.plan_id, task.task_id)
        progress = agent.onboarding.onboarding_progress(plan.plan_id)
        assert progress["completion_rate"] == 100.0

# Edge case tests
class TestEdgeCases:
    def test_hire_duplicate_email_raises(self):
        mgr = EmployeeManager()
        mgr.hire_employee(email="dup@co.com", ...)
        with pytest.raises(DuplicateEmployeeEmail):
            mgr.hire_employee(email="dup@co.com", ...)

    def test_leave_cancel_reverses_balance(self):
        leave = LeaveManager()
        leave.set_balance("EMP001", 2025, {"vacation": 15})
        req = leave.submit_request("EMP001", LeaveType.VACATION, ...)
        leave.approve_request(req.request_id, "MGR001")
        leave.cancel_request(req.request_id)
        balance = leave.get_employee_balance("EMP001", 2025)
        assert balance.remaining("vacation") == 15
```

### Test Data Factories

```python
class HRTestDataFactory:
    """Generate realistic test data for all HR components."""

    @staticmethod
    def create_employee(department=None, job_level=None, salary=None):
        return {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "department": department or random.choice(list(Department)),
            "job_title": fake.job(),
            "job_level": job_level or random.choice(list(JobLevel)),
            "salary": salary or random.randint(50000, 200000),
            "gender": random.choice(["male", "female", "non-binary", None]),
            "performance_score": round(random.uniform(1.0, 5.0), 1),
            "engagement_score": round(random.uniform(1.0, 5.0), 1),
        }

    @staticmethod
    def create_candidate(position="Engineer", source="linkedin"):
        return {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "position_applied": position,
            "source": source,
        }

    @staticmethod
    def create_review_cycle(employees, reviewer_id):
        """Create a complete review cycle for testing."""
        reviews = []
        for emp in employees:
            review = {
                "employee_id": emp.employee_id,
                "reviewer_id": reviewer_id,
                "overall_rating": random.choice(list(ReviewRating)),
                "self_assessment_score": round(random.uniform(3.0, 5.0), 1),
                "peer_feedback_score": round(random.uniform(3.0, 5.0), 1),
                "manager_feedback_score": round(random.uniform(3.0, 5.0), 1),
                "upward_feedback_score": round(random.uniform(3.0, 5.0), 1),
            }
            reviews.append(review)
        return reviews
```

---

## 17. Deployment Guide

### Environment Requirements

```
┌─────────────────────────────────────────────────────────────┐
│                   Environment Matrix                        │
├──────────────┬──────────────┬──────────────┬───────────────┤
│   Component  │    Dev       │    Staging   │   Production  │
├──────────────┼──────────────┼──────────────┼───────────────┤
│ Python       │ 3.10+        │ 3.10+        │ 3.10+         │
│ Memory       │ 512MB        │ 2GB          │ 8GB+          │
│ Storage      │ 100MB        │ 1GB          │ 10GB+         │
│ CPU          │ 1 core       │ 2 cores      │ 4+ cores      │
│ DB           │ SQLite       │ PostgreSQL   │ PostgreSQL    │
│ Cache        │ None         │ Redis        │ Redis         │
│ Workers      │ 1            │ 2-4          │ 4-16          │
└──────────────┴──────────────┴──────────────┴───────────────┘
```

### Docker Configuration

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY agents/hr/ ./agents/hr/
COPY config/ ./config/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "from agents.hr.agent import HRAgent; HRAgent().full_status()"

# Run
CMD ["python", "-m", "agents.hr.server"]
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hr-agent
  labels:
    app: hr-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hr-agent
  template:
    metadata:
      labels:
        app: hr-agent
    spec:
      containers:
      - name: hr-agent
        image: hr-agent:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: HR_DB_URL
          valueFrom:
            secretKeyRef:
              name: hr-secrets
              key: db-url
        - name: HR_ENV
          value: "production"
```

### Deployment Checklist

```markdown
## Pre-Deployment
- [ ] All unit tests passing
- [ ] Integration tests passing
- [ ] Code review completed
- [ ] Security scan clean
- [ ] Database migrations ready
- [ ] Configuration updated for target environment
- [ ] Secrets rotated if needed

## Deployment
- [ ] Backup current database
- [ ] Run database migrations
- [ ] Deploy application code
- [ ] Verify health checks pass
- [ ] Smoke test critical paths:
  - [ ] Employee hire
  - [ ] Employee search
  - [ ] Leave request submit
  - [ ] Performance review create

## Post-Deployment
- [ ] Monitor error rates for 30 minutes
- [ ] Verify cron jobs running
- [ ] Check compliance alert schedules
- [ ] Review deployment logs
- [ ] Notify team of successful deployment
```

---

## 18. Performance Optimization

### Caching Strategy

```
┌─────────────────────────────────────────────────────────────┐
│                    Cache Layers                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  L1: In-Memory (per-request)                                │
│  ├── Employee lookups by ID                                  │
│  ├── Department enumeration                                  │
│  └── Current user session                                   │
│                                                              │
│  L2: Application Cache (TTL-based)                          │
│  ├── Headcount summaries     (TTL: 5 min)                   │
│  ├── Salary statistics       (TTL: 1 hour)                  │
│  ├── Compliance reports      (TTL: 15 min)                  │
│  ├── Org chart structure     (TTL: 10 min)                  │
│  └── Training completion     (TTL: 5 min)                   │
│                                                              │
│  L3: Database Query Cache                                   │
│  ├── Complex joins and aggregations                         │
│  ├── Historical trend data                                  │
│  └── Cross-department analytics                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### Query Optimization Patterns

```python
# ❌ BAD: N+1 query pattern
def get_team_with_reviews(manager_id):
    team = employee_manager.get_by_manager(manager_id)
    for emp in team:
        emp.reviews = performance_manager.get_reviews(emp.employee_id)  # N queries!

# ✅ GOOD: Batch loading
def get_team_with_reviews(manager_id):
    team = employee_manager.get_by_manager(manager_id)
    employee_ids = [emp.employee_id for emp in team]
    all_reviews = performance_manager.get_reviews_batch(employee_ids)  # 1 query
    # Map reviews to employees
    reviews_by_emp = defaultdict(list)
    for review in all_reviews:
        reviews_by_emp[review.employee_id].append(review)
    for emp in team:
        emp.reviews = reviews_by_emp.get(emp.employee_id, [])
    return team

# ❌ BAD: Full table scan for analytics
def get_attrition_rate_full():
    all_employees = employees.values()
    terminated = [e for e in all_employees if e.employment_status == EmploymentStatus.TERMINATED]

# ✅ GOOD: Pre-computed index
def get_attrition_rate_optimized():
    return _attrition_rate_cache.get(current_quarter)
```

### Database Indexing Recommendations

```sql
-- Employee table indexes
CREATE INDEX idx_employee_department ON employees(department);
CREATE INDEX idx_employee_status ON employees(employment_status);
CREATE INDEX idx_employee_manager ON employees(manager_id);
CREATE INDEX idx_employee_hire_date ON employees(hire_date);
CREATE INDEX idx_employee_email ON employees(email);

-- Leave requests
CREATE INDEX idx_leave_employee ON leave_requests(employee_id);
CREATE INDEX idx_leave_status ON leave_requests(status);
CREATE INDEX idx_leave_dates ON leave_requests(start_date, end_date);

-- Compliance items
CREATE INDEX idx_compliance_employee ON compliance_items(employee_id);
CREATE INDEX idx_compliance_expiration ON compliance_items(expiration_date);
CREATE INDEX idx_compliance_status ON compliance_items(status);

-- Performance reviews
CREATE INDEX idx_review_employee ON performance_reviews(employee_id);
CREATE INDEX idx_review_cycle ON performance_reviews(review_cycle_id);
CREATE INDEX idx_review_rating ON performance_reviews(overall_rating);
```

---

## 19. Internationalization (i18n) Support

### Supported Locales

| Locale | Language | Date Format | Currency | Number Format |
|--------|----------|-------------|----------|---------------|
| en-US | English | MM/DD/YYYY | USD ($) | 1,234.56 |
| en-GB | English | DD/MM/YYYY | GBP (£) | 1,234.56 |
| de-DE | German | DD.MM.YYYY | EUR (€) | 1.234,56 |
| fr-FR | French | DD/MM/YYYY | EUR (€) | 1 234,56 |
| es-ES | Spanish | DD/MM/YYYY | EUR (€) | 1.234,56 |
| ja-JP | Japanese | YYYY/MM/DD | JPY (¥) | 1,234.56 |
| zh-CN | Chinese | YYYY-MM-DD | CNY (¥) | 1,234.56 |
| ar-SA | Arabic | DD/MM/YYYY | SAR (ر.س) | ١٬٢٣٤٫٥٦ |

### Localization Keys

```yaml
# hr.messages
employee:
  hire_success: "Employee {name} hired successfully"
  terminate_success: "Employee {name} terminated. Last day: {date}"
  not_found: "Employee with ID {id} not found"

leave:
  request_submitted: "Leave request submitted for {dates}"
  request_approved: "Leave request approved by {approver}"
  balance_insufficient: "Insufficient {type} balance. Available: {available}, Requested: {requested}"

compliance:
  item_expiring: "{requirement} expires in {days} days"
  item_expired: "{requirement} has expired. Immediate action required."
  renewal_reminder: "Renewal deadline for {requirement}: {date}"

training:
  assignment_reminder: "Training '{name}' due in {days} days"
  completion_congrats: "Congratulations! You completed '{name}' with score {score}%"
```

---

## 20. Audit Trail Specification

### Audit Event Types

| Event | Description | Data Captured |
|-------|-------------|---------------|
| EMPLOYEE_CREATE | New employee hired | Full employee record snapshot |
| EMPLOYEE_UPDATE | Employee record modified | Changed fields (before/after) |
| EMPLOYEE_TERMINATE | Employee terminated | Termination reason, date, rehire eligibility |
| REVIEW_CREATE | Performance review initiated | Reviewer, employee, cycle |
| REVIEW_COMPLETE | Review finalized | Final rating, all scores |
| LEAVE_REQUEST | Leave request submitted | Request details, dates, type |
| LEAVE_APPROVE | Leave request approved | Approver, approval date |
| LEAVE_DENY | Leave request denied | Denier, denial reason |
| COMPLIANCE_ALERT | Compliance issue detected | Item, severity, deadline |
| TRAINING_COMPLETE | Training finished | Score, completion date |
| BENEFIT_ENROLL | Benefits enrollment | Plan selected, dependents |
| SALARY_CHANGE | Compensation modified | Old salary, new salary, reason |

### Audit Log Schema

```python
@dataclass
class AuditLogEntry:
    event_id: str                    # UUID
    event_type: str                  # "EMPLOYEE_UPDATE"
    timestamp: datetime              # UTC
    actor_id: str                    # Who performed the action
    actor_role: str                  # "HR_ADMIN", "MANAGER"
    target_type: str                 # "employee", "review", "leave"
    target_id: str                   # ID of affected entity
    changes: Optional[Dict]          # Before/after for updates
    ip_address: Optional[str]        # Source IP
    user_agent: Optional[str]        # Client info
    metadata: Optional[Dict]         # Additional context

    def to_json(self) -> str:
        return json.dumps({
            "event_id": self.event_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp.isoformat(),
            "actor": {"id": self.actor_id, "role": self.actor_role},
            "target": {"type": self.target_type, "id": self.target_id},
            "changes": self.changes,
            "context": {
                "ip_address": self.ip_address,
                "user_agent": self.user_agent,
            },
            "metadata": self.metadata,
        }, indent=2)
```

### Audit Retention Policy

```
┌─────────────────────────────────────────────────────────────┐
│                Retention Schedule                            │
├──────────────────┬──────────────┬───────────────────────────┤
│ Event Category   │ Retention    │ Archive After             │
├──────────────────┼──────────────┼───────────────────────────┤
│ Employee Create  │ 7 years     │ Move to cold storage      │
│ Employee Update  │ 7 years     │ Move to cold storage      │
│ Termination      │ 7 years     │ Move to cold storage      │
│ Salary Changes   │ 7 years     │ Move to cold storage      │
│ Performance Rev  │ 5 years     │ Delete or archive         │
│ Leave Requests   │ 3 years     │ Aggregate and delete      │
│ Compliance       │ 7 years     │ Move to cold storage      │
│ Training         │ 3 years     │ Aggregate and delete      │
│ System Events    │ 1 year      │ Delete                    │
└──────────────────┴──────────────┴───────────────────────────┘
```

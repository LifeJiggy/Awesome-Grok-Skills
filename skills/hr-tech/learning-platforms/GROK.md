---
name: learning-platforms
category: hr-tech
version: 1.0.0
tags:
  - learning
  - lms
  - adaptive-learning
  - skill-gap
  - compliance
  - hr-tech
  - training
  - education
difficulty: advanced
estimated_time: 50min
prerequisites:
  - python-3.11
  - pandas
  - numpy
  - scikit-learn
---

# Learning Platforms

## Purpose

Enterprise learning management system with adaptive learning paths, skill gap analysis, compliance training tracking, and learning ROI measurement. Provides personalized development experiences aligned to business objectives.

## Core Components

### 1. Learning Management System (LMS)

- **Course Catalog**: Hierarchical course taxonomy with prerequisite chains, metadata, and multi-format content support
- **Enrollment Engine**: Auto-enrollment rules based on role, level, department, and compliance requirements
- **Progress Tracking**: Granular module-level completion with time-on-task and engagement scoring
- **Certification Management**: Issuance, renewal tracking, and expiry alert workflows

### 2. Adaptive Learning Engine

- **Knowledge Assessment**: Pre-assessment quizzes calibrating learner baseline per topic
- **Dynamic Path Selection**: Recommend next modules based on demonstrated mastery gaps
- **Spaced Repetition**: Schedule review sessions at optimal intervals using Ebbinghaus curve modeling
- **Mastery Tracking**: Bayesian knowledge tracing for per-concept mastery probability estimates

### 3. Skill Gap Analysis

- **Competency Mapping**: Compare current skill inventory against role requirements
- **Gap Prioritization**: Rank gaps by business impact, urgency, and learner readiness
- **Learning Path Generation**: Auto-generate personalized curricula targeting highest-priority gaps
- **ROI Projection**: Estimate productivity gain from closing specific skill gaps

### 4. Compliance Training

- **Regulatory Mapping**: Map training requirements to specific regulations (SOX, GDPR, HIPAA, PCI-DSS)
- **Assignment Rules**: Role-based automatic assignment with due date calculation
- **Completion Tracking**: Real-time compliance status dashboards with escalation workflows
- **Audit Trail**: Immutable completion records for regulatory examination

## Data Models

```
Learner
  ├── learner_id: str
  ├── role: str
  ├── department: str
  ├── skill_inventory: List[SkillEntry]
  ├── enrolled_courses: List[Enrollment]
  ├── completed_courses: List[Completion]
  └── compliance_status: ComplianceStatus

Course
  ├── course_id: str
  ├── title: str
  ├── category: CourseCategory
  ├── modules: List[Module]
  ├── prerequisites: List[str]
  ├── estimated_hours: float
  ├── difficulty: DifficultyLevel
  └── compliance_tags: List[str]

LearningPath
  ├── path_id: str
  ├── learner_id: str
  ├── modules: List[RecommendedModule]
  ├── rationale: str
  ├── estimated_completion: date
  └── priority_score: float

ComplianceRecord
  ├── record_id: str
  ├── learner_id: str
  ├── requirement: str
  ├── course_id: str
  ├── status: ComplianceStatus
  ├── due_date: date
  └── completion_date: Optional[date]
```

## Implementation Patterns

### Adaptive Path Selection
```python
class AdaptiveEngine:
    def recommend_next(self, learner: Learner, course: Course) -> Module:
        mastery = self.assess_mastery(learner, course)
        gaps = self.identify_gaps(mastery, course)
        return self.select_optimal_module(gaps, learner.preferences)
```

### Compliance Status Check
```python
class ComplianceTracker:
    def check_status(self, learner: Learner) -> ComplianceReport:
        required = self.get_requirements(learner.role)
        completed = {c.course_id for c in learner.completed_courses}
        overdue = [r for r in required if r.due_date < date.today() and r.course_id not in completed]
        return ComplianceReport(overdue=overdue, compliance_rate=...)
```

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `mastery_threshold` | 0.80 | Bayesian mastery probability threshold |
| `spaced_repetition_interval` | 7 | Days between review sessions |
| `compliance_overdue_escalation_days` | 7 | Days after due before escalation |
| `max_simultaneous_courses` | 5 | Max concurrent active enrollments |
| `assessment_length` | 15 | Questions per adaptive assessment |

## Integration Points

- **LMS Platforms**: Moodle, Canvas, Cornerstone, Docebo via SCORM/xAPI
- **HRIS**: Workday, BambooHR for role and org data
- **Content Providers**: LinkedIn Learning, Coursera, Udemy Business via API
- **Compliance**: Thomson Reuters, NAVEX for regulatory content
- **Analytics**: xAPI Learning Record Store (LRS) for granular tracking

## Ethical Guidelines

1. Learning data must not be used for punitive performance evaluations
2. Adaptive recommendations must explain why content is suggested
3. Learners must have option to deviate from recommended paths
4. Compliance training completion must be verified, not just time-spent
5. Accessibility standards (WCAG 2.1 AA) required for all course content

## Testing Strategy

- **Adaptive Engine**: Mastery tracking accuracy, path recommendation quality
- **Compliance**: Due date calculation, escalation trigger timing
- **Gap Analysis**: Skill inventory completeness, gap prioritization accuracy
- **Integration**: SCORM/xAPI completion event processing
- **Edge Cases**: Concurrent enrollments, prerequisite chain validation

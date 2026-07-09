# Education Agent — System Architecture

## Overview

The Education Agent is a comprehensive learning management platform built with
modular sub-engines. It covers course creation and management, learner
enrollment and progress tracking, adaptive assessments with quiz grading,
certification, spaced repetition for long-term retention, learning path
optimization, gamification, and educational analytics.

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                       EducationAgent                                     │
│                   (Top-level Orchestrator)                                │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐  ┌────────────────┐  ┌──────────────────────────────┐ │
│  │  Course       │  │  Learner       │  │  Quiz                        │ │
│  │  Manager      │  │  Manager       │  │  Engine                      │ │
│  │              │  │                │  │                              │ │
│  │  - Courses   │  │  - Enrollment  │  │  - Creation                  │ │
│  │  - Modules   │  │  - Progress    │  │  - Grading                   │ │
│  │  - Lessons   │  │  - Dashboard   │  │  - Analytics                 │ │
│  └──────┬───────┘  └───────┬────────┘  └──────────────┬───────────────┘ │
│         │                  │                           │                  │
│  ┌──────┴───────┐  ┌──────┴────────┐  ┌──────────────┴───────────────┐ │
│  │  Certifi-     │  │  Spaced      │  │  Learning Path                │ │
│  │  cation       │  │  Repetition  │  │  Optimizer                    │ │
│  │  Manager      │  │  Engine      │  │                              │ │
│  │              │  │              │  │  - Path generation            │ │
│  │  - Issue     │  │  - SRS algo  │  │  - Style adaptation           │ │
│  │  - Verify    │  │  - Due items │  │  - Checkpoints                │ │
│  │  - Revoke    │  │  - Retention │  │                              │ │
│  └──────────────┘  └──────────────┘  └──────────────────────────────┘ │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                     Gamification Engine                              │ │
│  │  - Achievements, Points, Streaks, Leaderboards                      │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                     Analytics Reporting                              │ │
│  │  - Course analytics, Learner analytics, Platform overview           │ │
│  │  - At-risk learner identification                                    │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Component Deep Dives

### 1. CourseManager

**Purpose**: Full course lifecycle — creation, module/lesson management,
publishing, and catalog browsing.

```
┌─────────────────────────────────────────┐
│          CourseManager                   │
├─────────────────────────────────────────┤
│  _courses: Dict[str, Course]            │
│  _modules: Dict[str, Module]            │
│  _lessons: Dict[str, Lesson]            │
├─────────────────────────────────────────┤
│  create_course()        → Course        │
│  update_course()        → Course        │
│  get_course()           → Course        │
│  delete_course()        → bool          │
│  add_module()           → Module        │
│  add_lesson()           → Lesson        │
│  publish_course()       → bool          │
│  archive_course()       → bool          │
│  get_course_details()   → Dict          │
│  get_course_catalog()   → List[Dict]    │
└─────────────────────────────────────────┘
```

**Content Hierarchy**:
```
Course
  ├── Module 1: "Getting Started"
  │     ├── Lesson 1: "Introduction" (Video, 15min)
  │     ├── Lesson 2: "Setup" (Text, 10min)
  │     └── Lesson 3: "Quiz" (Quiz, 5min)
  ├── Module 2: "Core Concepts"
  │     ├── Lesson 4: "Variables" (Interactive, 20min)
  │     └── Lesson 5: "Functions" (Video, 25min)
  └── Module 3: "Advanced Topics"
        ├── Lesson 6: "Decorators" (Text, 15min)
        └── Lesson 7: "Final Project" (Assignment, 60min)
```

### 2. LearnerManager

**Purpose**: Enrollment management, progress tracking, learner profiles,
and dashboard generation.

```
┌──────────────────────────────────────────┐
│          LearnerManager                  │
├──────────────────────────────────────────┤
│  _enrollments: Dict[str, Enrollment]     │
│  _learner_profiles: Dict[str, Profile]   │
├──────────────────────────────────────────┤
│  create_learner_profile() → Profile      │
│  enroll_learner()         → Enrollment   │
│  update_progress()        → Enrollment   │
│  record_time_spent()      → None         │
│  get_enrollment()         → Enrollment   │
│  get_learner_enrollments() → List[Enroll]│
│  get_learner_dashboard()  → Dict         │
└──────────────────────────────────────────┘
```

**Progress Calculation**:
```
completed_lessons.count / total_course_lessons.count × 100
= progress_percent
```

### 3. QuizEngine

**Purpose**: Quiz creation, question management, grading, and analytics.

```
┌──────────────────────────────────────────┐
│            QuizEngine                    │
├──────────────────────────────────────────┤
│  _quizzes: Dict[str, Quiz]               │
│  _attempts: Dict[str, List[Attempt]]     │
├──────────────────────────────────────────┤
│  create_quiz()           → Quiz          │
│  add_question()          → str           │
│  grade_quiz()            → QuizAttempt   │
│  get_quiz_results()      → List[Attempt] │
│  get_quiz_analytics()    → Dict          │
└──────────────────────────────────────────┘
```

**Grading Pipeline**:
```
Submit Answers
  ↓
Match against correct_index
  ↓
Calculate earned_points / total_points
  ↓
Compute percentage
  ↓
Compare to passing_score
  ↓
Generate per-question feedback
  ↓
Return QuizAttempt
```

### 4. CertificationManager

**Purpose**: Certificate issuance, verification, and revocation.

```
┌──────────────────────────────────────────┐
│        CertificationManager              │
├──────────────────────────────────────────┤
│  _certificates: Dict[str, Certificate]   │
├──────────────────────────────────────────┤
│  issue_certificate()       → Certificate │
│  verify_certificate()      → Dict        │
│  revoke_certificate()      → bool        │
│  get_learner_certificates() → List[Cert] │
└──────────────────────────────────────────┘
```

### 5. SpacedRepetitionEngine

**Purpose**: Long-term memory optimization using spaced repetition
algorithms (SM-2 variant).

```
┌──────────────────────────────────────────┐
│       SpacedRepetitionEngine             │
├──────────────────────────────────────────┤
│  _items: Dict[str, SRItem]               │
├──────────────────────────────────────────┤
│  add_item()             → SRItem         │
│  record_review()        → SRItem         │
│  get_due_items()        → List[SRItem]   │
│  get_retention_stats()  → Dict           │
└──────────────────────────────────────────┘
```

**SM-2 Algorithm Flow**:
```
Record Review(quality: 0-5)
  ↓
  quality >= 4?
  ├─ YES → interval *= ease_factor, ease_factor += 0.1
  └─ NO (quality >= 3)?
       ├─ YES → interval *= 1.2
       └─ NO → reset interval to 1 day
  ↓
Update ease_factor (bounded >= 1.3)
  ↓
Set next_review = now + interval_days
```

### 6. LearningPathOptimizer

**Purpose**: Generates personalized, adaptive learning paths.

```
┌──────────────────────────────────────────┐
│      LearningPathOptimizer               │
├──────────────────────────────────────────┤
│  _paths: Dict[str, LearningPath]         │
├──────────────────────────────────────────┤
│  create_learning_path()  → LearningPath  │
│  get_path()              → LearningPath  │
│  optimize_for_style()    → LearningPath  │
└──────────────────────────────────────────┘
```

### 7. GamificationEngine

**Purpose**: Achievements, points, streaks, and leaderboards.

```
┌──────────────────────────────────────────┐
│        GamificationEngine                │
├──────────────────────────────────────────┤
│  _achievements: Dict[str, Achievement]   │
│  _earned: Dict[str, List[str]]           │
│  _points: Dict[str, int]                 │
├──────────────────────────────────────────┤
│  create_achievement()    → Achievement   │
│  award_achievement()     → bool          │
│  add_points()            → None          │
│  get_leaderboard()       → List[Dict]    │
│  get_learner_achievements() → List[Dict] │
│  get_learner_points()    → int           │
└──────────────────────────────────────────┘
```

### 8. AnalyticsReporting

**Purpose**: Course analytics, learner analytics, platform overview,
at-risk identification.

```
┌──────────────────────────────────────────┐
│        AnalyticsReporting                │
├──────────────────────────────────────────┤
│  get_course_analytics()    → Dict        │
│  get_learner_analytics()   → Dict        │
│  get_platform_overview()   → Dict        │
│  identify_at_risk_learners() → List[Dict]│
└──────────────────────────────────────────┘
```

---

## Data Flow Diagrams

### Course Creation Flow

```
Instructor Request
     │
     ▼
┌──────────────────────────────────┐
│  EducationAgent                  │
│  .create_course_with_content()   │
└────────────┬─────────────────────┘
             │
     ┌───────┼───────────┐
     ▼       ▼           ▼
  Create   Add Module  Add Lessons
  Course   (per module) (per module)
     │       │           │
     └───────┼───────────┘
             ▼
      Publish Course
             │
             ▼
     Return course_id
```

### Learner Enrollment + Progress Flow

```
Learner Enrolls
     │
     ▼
┌──────────────────────────────────┐
│  LearnerManager                  │
│  .enroll_learner()               │
└────────────┬─────────────────────┘
             │
             ▼
     Create Enrollment
     (status: NOT_STARTED)
             │
     ┌───────┼───────────────┐
     ▼       ▼               ▼
  Complete  Update         Record
  Lesson    Progress       Time
     │       │               │
     └───────┼───────────────┘
             ▼
      Calculate %
             │
     ┌───────┴───────┐
     ▼               ▼
   < 100%          = 100%
     │               │
  Continue        Complete
  Learning        Course
                     │
                     ▼
               Issue Certificate
```

### Quiz Grading Flow

```
Learner Submits Answers
     │
     ▼
┌──────────────────────────────────┐
│  QuizEngine.grade_quiz()         │
└────────────┬─────────────────────┘
             │
     ┌───────┼───────────┐
     ▼       ▼           ▼
  Match   Calculate    Check
  Answers Points       Attempts
     │       │           │
     └───────┼───────────┘
             ▼
      Compute Score
             │
             ▼
      Generate Feedback
             │
             ▼
     Return QuizAttempt
```

### Spaced Repetition Flow

```
Review Session
     │
     ▼
┌──────────────────────────────────┐
│  SR.record_review(quality)       │
└────────────┬─────────────────────┘
             │
     ┌───────┼───────────┐
     ▼       ▼           ▼
  quality  Update      Update
  >= 4?    Interval    Ease
     │       │           │
     └───────┼───────────┘
             ▼
      Set Next Review
             │
             ▼
     Schedule Review
```

---

## Design Patterns

### Composite Pattern
Courses contain Modules, which contain Lessons — a natural tree structure
traversable via the CourseManager.

### Strategy Pattern
Different learning styles (visual, auditory, kinesthetic, reading/writing)
trigger different content delivery strategies via the LearningPathOptimizer.

### Observer Pattern (At-Risk Detection)
AnalyticsReporting monitors learner activity and flags at-risk learners
based on inactivity thresholds — similar to an observer watching for
state changes.

### Template Method Pattern
The grading pipeline (match → calculate → feedback) follows a fixed template
regardless of question type. Individual question types can override specific
steps.

---

## Data Model Relationships

```
Course ─────────────────────┐
  │                         │
  ├── Module (1:N) ────────┤
  │     └── Lesson (1:N)   │
  │                         │
  ├── Quiz (1:N) ──────────┤
  │     └── Question (1:N) │
  │                         │
  ├── Enrollment (1:N) ────┤
  │     ├── Progress       │
  │     └── Time Tracking  │
  │                         │
  ├── Certificate (1:N)    │
  │                         │
  └── LearningPath (1:N)   │
                            │
Learner ────────────────────┘
  │
  ├── Profile
  ├── Achievements (N:N)
  ├── Spaced Repetition Items (1:N)
  └── Quiz Attempts (1:N)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.10+ |
| Type System | dataclasses + Enum |
| Validation | Custom validate() methods |
| Logging | stdlib logging |
| Storage | In-memory dicts (pluggable) |
| Serialization | dataclass → dict (JSON-serializable) |
| Testing | pytest + hypothesis |
| SRS Algorithm | SM-2 variant |
| Assessment | Custom grading engine |

---

## Security Considerations

1. **Content Access Control**: Lessons have access levels (Free, Enrolled,
   Premium, Instructor, Admin). Verify enrollment before serving content.
2. **Quiz Integrity**: Limit max_attempts, randomize question order, and
   timestamp all attempts for audit.
3. **Certificate Anti-Fraud**: Use unique certificate numbers with
   verification URLs. Support revocation.
4. **Learner Data Privacy**: PII (name, email) must be encrypted at rest
   and masked in logs.
5. **Plagiarism Detection**: Essay and short-answer questions can integrate
   with plagiarism detection APIs.

---

## Scalability Considerations

| Dimension | Current | Target |
|-----------|---------|--------|
| Courses | 100 | 50,000+ |
| Learners | 1,000 | 1,000,000+ |
| Concurrent sessions | 50 | 100,000+ |
| Quiz attempts/day | 500 | 500,000+ |
| Certificates issued | 1,000 | 10,000,000+ |

**Scaling Strategy**:
- Move from in-memory to PostgreSQL for persistent storage.
- Use Redis for session state and progress caching.
- Shard learner data by learner_id for horizontal scaling.
- Use CDN for video/content delivery.
- Implement event sourcing for progress tracking.

---

## Extension Points

1. **New Lesson Types**: Add to `LessonType` enum and implement content
   renderer.
2. **New Assessment Types**: Add to `AssessmentType` and implement grading
   logic in QuizEngine.
3. **LMS Integration**: Connect to Moodle, Canvas, or Blackboard via
   LTI (Learning Tools Interoperability).
4. **Video Hosting**: Integrate with Vimeo, Wistia, or YouTube for
   video lesson delivery.
5. **Payment Processing**: Add Stripe/PayPal for paid course enrollment.

---

## Configuration

```yaml
education_agent:
  course_manager:
    max_courses: 50000
    max_modules_per_course: 50
    max_lessons_per_module: 100
    auto_save_drafts: true

  learner_manager:
    max_enrollments_per_learner: 100
    inactivity_threshold_days: 7
    streak_grace_period_hours: 24

  quiz_engine:
    max_questions_per_quiz: 100
    default_time_limit_minutes: 30
    max_attempts_default: 3
    randomize_questions: true

  certification:
    certificate_validity_months: 24
    use_digital_signature: true

  spaced_repetition:
    max_items_per_learner: 1000
    default_ease_factor: 2.5
    review_reminder_enabled: true

  gamification:
    points_per_lesson: 10
    points_per_quiz_pass: 25
    streak_bonus_multiplier: 1.5
    leaderboard_update_frequency: hourly
```

---

## Performance Benchmarks

| Operation | Latency (p99) | Throughput |
|-----------|---------------|------------|
| Course creation | < 100ms | 500/s |
| Enrollment | < 50ms | 5K/s |
| Progress update | < 20ms | 50K/s |
| Quiz grading | < 100ms | 2K/s |
| Certificate issue | < 50ms | 5K/s |
| SRS due items query | < 30ms | 10K/s |
| Analytics dashboard | < 500ms | 100/s |

---

## Testing Strategy

| Test Type | Coverage Target | Tools |
|-----------|----------------|-------|
| Unit tests | 90%+ | pytest |
| Integration tests | Key flows | pytest + fixtures |
| Load tests | Throughput | locust |
| Property tests | Data invariants | hypothesis |
| E2E tests | Full learner journey | playwright |

### Unit Test Examples

```python
# Course Manager Tests
def test_create_course():
    manager = CourseManager()
    course = manager.create_course("Test Course", "Description", "inst_001")
    assert course.title == "Test Course"
    assert course.status == CourseStatus.DRAFT

def test_publish_course():
    manager = CourseManager()
    course = manager.create_course("Test", "Desc", "inst_001")
    manager.add_module(course.course_id, "Module 1")
    assert manager.publish_course(course.course_id)

# Quiz Engine Tests
def test_grade_quiz():
    engine = QuizEngine()
    quiz = engine.create_quiz("Test Quiz", "course_001", passing_score=70)
    engine.add_question(quiz.quiz_id, "What is 2+2?", ["3", "4", "5"], 1, points=10)
    attempt = engine.grade_quiz(quiz.quiz_id, "learner_001", {"q_1": 1})
    assert attempt.percentage == 100.0
    assert attempt.passed

# Spaced Repetition Tests
def test_sm2_algorithm():
    srs = SpacedRepetitionEngine()
    item = srs.add_item("learner_001", "content_001")
    
    # Quality 5 (easy recall)
    updated = srs.record_review(item.item_id, quality=5)
    assert updated.interval_days > item.interval_days
    assert updated.ease_factor >= 2.5
```

### Integration Test Examples

```python
def test_learner_journey():
    agent = EducationAgent()
    
    # Create course
    result = agent.create_course_with_content(
        title="Test Course",
        description="Test",
        instructor_id="inst_001",
        modules_data=[{
            "title": "Module 1",
            "lessons": [
                {"title": "Lesson 1", "type": "text", "duration": 10},
            ],
        }],
    )
    course_id = result["course_id"]
    
    # Learner enrolls
    profile = agent.learner_manager.create_learner_profile("Test User", "test@example.com")
    enrollment = agent.learner_manager.enroll_learner(course_id, profile.learner_id)
    
    # Complete lesson
    agent.learner_manager.update_progress(enrollment.enrollment_id, "lesson_001")
    
    # Verify progress
    dashboard = agent.learner_manager.get_learner_dashboard(profile.learner_id)
    assert dashboard["completed"] >= 1
```

### Performance Test Scenarios

| Scenario | Target | Description |
|----------|--------|-------------|
| Course search | < 10ms | Search 1K courses |
| Quiz grading | < 50ms | Grade 50 questions |
| Progress update | < 5ms | Update lesson completion |
| Analytics query | < 100ms | Platform overview |
| Certificate verify | < 10ms | Verify certificate |

---

## Deployment Architecture

### Single-Instance Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION SERVER                         │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────┐ │
│  │                  EducationAgent                        │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │ │
│  │  │ Course  │ │ Learner │ │  Quiz   │ │  Cert   │    │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │ │
│  │  │  SRS    │ │  Path   │ │  Game   │ │Analytics│    │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘    │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                  DATA LAYER                            │ │
│  │  In-Memory │ Optional DB │ Cache (Redis)              │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Video Content Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VIDEO PIPELINE                             │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  Upload → Transcode → Store → Deliver                        │
│    │         │          │         │                          │
│    ▼         ▼          ▼         ▼                          │
│  ┌─────┐  ┌─────┐   ┌─────┐  ┌─────┐                      │
│  │ S3  │  │ FFmpeg│  │ CDN │  │ HLS │                      │
│  └─────┘  └─────┘   └─────┘  └─────┘                      │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Security Architecture

### Authentication Flow

```
  Learner Login
       │
       ▼
  ┌──────────────┐
  │   Auth Service│
  │  (JWT Tokens) │
  └──────┬───────┘
         │
    ┌────┴────┐
    │ Valid?  │
    └────┬────┘
    Yes  │  No
    │    │   │
    ▼    │   ▼
  Access│  401 Unauthorized
  Content│
```

### Data Protection

| Data Type | Protection | Storage |
|-----------|------------|---------|
| Learner PII | AES-256 | Database |
| Course content | DRM | CDN |
| Quiz answers | Hashed | Database |
| Certificates | Digital signature | Database |
| Payment data | Tokenized | Payment processor |

### Assessment Integrity

- Randomize question order per attempt
- Implement time limits
- Limit attempts to prevent brute-force
- Use question banks for large pools
- Track suspicious patterns

---

## Monitoring and Observability

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| Course completion rate | Completions / enrollments | < 30% |
| Quiz pass rate | Passed / attempted | < 50% |
| Average quiz score | Mean score across quizzes | < 60% |
| Learner activity | Active learners / total | < 20% |
| API response time | 95th percentile | > 500ms |
| Error rate | Errors / total requests | > 1% |

### Learning Analytics Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│                    LEARNING DASHBOARD                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Courses    │  │  Learners   │  │ Completion  │         │
│  │    150      │  │   5,000     │  │    65%      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Quizzes    │  │ Avg Score   │  │ At-Risk     │         │
│  │    500      │  │    78%      │  │    12%      │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Data Retention Policy

| Data Type | Retention | Archive After |
|-----------|-----------|---------------|
| Course content | Indefinite | Never |
| Learner progress | 5 years | 2 years |
| Quiz attempts | 2 years | 1 year |
| Certificates | Indefinite | Never |
| Analytics data | 3 years | 1 year |
| Session data | 30 days | Immediate |

---

## Disaster Recovery

### Backup Strategy

| Data | Frequency | Method | Recovery Time |
|------|-----------|--------|---------------|
| Course content | Daily | Full dump | < 1 hour |
| Learner data | Real-time | Replication | < 5 minutes |
| Quiz data | Daily | Encrypted backup | < 2 hours |
| Certificates | Daily | Encrypted backup | < 2 hours |

### Recovery Procedures

1. **Data corruption**: Restore from last backup
2. **Service failure**: Restart and verify state
3. **Database failure**: Switch to replica
4. **Full outage**: Deploy to backup region

---

## Accessibility Features

### WCAG 2.1 Compliance

| Feature | Status | Level |
|---------|--------|-------|
| Keyboard navigation | Supported | AA |
| Screen reader support | Supported | AA |
| Color contrast | 4.5:1 minimum | AA |
| Alt text for images | Required | A |
| Captions for video | Supported | AA |
| Focus indicators | Visible | AA |

### Responsive Design Breakpoints

| Breakpoint | Width | Usage |
|------------|-------|-------|
| Mobile | < 768px | Single column |
| Tablet | 768-1024px | Two columns |
| Desktop | > 1024px | Full layout |

---

**See Also**: [GROK.md](./GROK.md) for agent identity and capabilities,
[README.md](./README.md) for quick start and API reference.
